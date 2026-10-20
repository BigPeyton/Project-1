"""Working operating DCF; five linked years followed by an explicit maturity fade.

No equity bridge or investment recommendation is implied by this module.
"""
import copy
import json
import math
from datetime import date
from pathlib import Path
from three_statements import load_inputs, project, FundingGap

ROOT = Path(__file__).resolve().parents[1]


def assumptions():
    return json.loads((ROOT/'data/valuation_assumptions.json').read_text())


def discount_rate(model, capital, a):
    d = a['discount_rate']
    # Converted-note scenario: exclude the same notes from debt weights.
    shares = (capital['derived_scenarios']['august_common_plus_preferred']
              + capital['known_september_exercise']['shares']
              + capital['remaining_notes']['conversion_shares'])/1e6
    equity = shares*d['reference_price']
    b = model['cutoff_balance_sheet']
    debt = b['other_debt']+b['finance_leases']
    ke = d['risk_free']+d['beta']*d['equity_risk_premium']
    weight = debt/(equity+debt)
    wacc = (1-weight)*ke+weight*d['debt_cost']*(1-d['immediate_interest_tax_shield'])
    return dict(cost_of_equity=ke, equity_market_proxy=equity, debt_market_proxy=debt,
                debt_weight=weight, calculated_wacc=wacc, selected_wacc=d['selected_wacc'])


def terminal_value(nopat_next, growth, roic, wacc):
    if not all(math.isfinite(v) for v in (nopat_next, growth, roic, wacc)):
        raise ValueError('Nonfinite terminal input.')
    if not 0 <= growth < wacc or not 0 <= growth < roic or nopat_next <= 0:
        raise ValueError('Need positive NOPAT, 0 <= g < WACC and g < ROIC.')
    reinvestment = nopat_next*growth/roic
    fcff = nopat_next-reinvestment
    return dict(nopat=nopat_next, reinvestment=reinvestment, fcff=fcff,
                reinvestment_rate=growth/roic, value=fcff/(wacc-growth))


def discounted_value(schedule, terminal, terminal_time, wacc):
    if not all(math.isfinite(x) for x in (wacc,terminal,terminal_time)) or wacc <= 0 or terminal_time <= 0:
        raise ValueError('Invalid discount rate or terminal date.')
    if not schedule or any(not math.isfinite(r['fcff']) or
                           not 0 < r['years_after_cutoff'] <= terminal_time for r in schedule):
        raise ValueError('Cash flows must be finite and strictly after the cutoff.')
    if any(x['years_after_cutoff'] >= y['years_after_cutoff'] for x,y in zip(schedule,schedule[1:])):
        raise ValueError('Cash-flow dates must be strictly ordered.')
    pv_flows = sum(r['fcff']/(1+wacc)**r['years_after_cutoff'] for r in schedule)
    pv_terminal = terminal/(1+wacc)**terminal_time
    ev = pv_flows+pv_terminal
    return dict(pv_explicit_fcff=pv_flows, pv_terminal=pv_terminal, enterprise_value=ev,
                terminal_share=pv_terminal/ev if ev > 0 else None)


def transition(model, a, case, growth=None, wacc=None):
    if model['total_net_equity_raised'] > 0:
        raise ValueError('Conditional financing requires a separate funding/ownership valuation; cannot bypass this gate.')
    if model['case'] != case:
        raise ValueError('Statement scenario and valuation scenario must match.')
    if case not in a['cases']:
        raise ValueError('No supported sustainable transition for this case.')
    t, c = a['terminal'], a['cases'][case]
    g = t['growth'] if growth is None else growth
    n = t['last_transition_year']-t['first_transition_year']+1
    if n < 2 or len(c['growth_path']) != n or model['annual'][-1]['year'] != t['first_transition_year']-1:
        raise ValueError('Transition must immediately follow linked statements and have a complete growth path.')
    margin, tax, roic = c['mature_ebit_margin'], t['tax_rate'], c['mature_incremental_roic']
    effective_wacc = a['discount_rate']['selected_wacc'] if wacc is None else wacc
    terminal_value(1, g, roic, effective_wacc)
    if not 0 < margin < 1 or not 0 <= tax < 1:
        raise ValueError('Invalid mature margin or tax rate.')
    previous, final = model['annual'][-2:]
    net_investment = final['cash_capex']-final['da']+final['delta_wc']
    delta_sales = final['total_revenue']-previous['total_revenue']
    if net_investment <= 0 or delta_sales <= 0:
        raise ValueError('2030 capital-efficiency anchor needs positive investment and revenue increase.')
    anchor_sc = delta_sales/net_investment
    mature_sc = roic/(margin*(1-tax))
    start_margin = final['operating_income']/final['total_revenue']
    path = list(c['growth_path'])
    # g sensitivities change the final explicit growth as well as perpetuity.
    path[-1] = g
    if any(not math.isfinite(v) or v < 0 for v in path):
        raise ValueError('Transition growth must be nonnegative and finite.')
    sales = final['total_revenue']
    cutoff = date.fromisoformat(a['cutoff'][:10])
    buffer = final['balance_sheet']['cash']+final['balance_sheet']['securities']-model['cutoff_bridge_inputs']['operating_reserve']
    rows=[]
    for i, rate in enumerate(path):
        year = t['first_transition_year']+i
        weight = (i+1)/n
        sales *= 1+rate
        ebit_margin = start_margin+weight*(margin-start_margin)
        sc = anchor_sc+weight*(mature_sc-anchor_sc)
        next_growth = path[i+1] if i+1<n else g
        reinvestment = sales*next_growth/sc
        ebit = sales*ebit_margin
        cash_tax = max(ebit*tax, sales*0.0011)
        nopat = ebit-cash_tax
        fcff = nopat-reinvestment
        buffer += fcff
        if buffer < 0:
            raise ValueError(f'{year}: transition exhausts conservative unlevered liquidity buffer.')
        rows.append(dict(year=year, end=f'{year}-12-31', revenue=sales, growth=rate,
                         ebit_margin=ebit_margin, ebit=ebit, cash_tax=cash_tax, nopat=nopat,
                         sales_to_incremental_capital=sc, reinvestment=reinvestment, fcff=fcff,
                         unlevered_liquidity_buffer=buffer,
                         years_after_cutoff=(date(year,12,31)-cutoff).days/365))
    return rows, dict(anchor_sales_to_capital=anchor_sc, mature_sales_to_capital=mature_sc,
                      anchor_net_reinvestment=net_investment)


def value(model, a, case='base', wacc=None, growth=None):
    w = a['discount_rate']['selected_wacc'] if wacc is None else wacc
    g = a['terminal']['growth'] if growth is None else growth
    # Validate the actual requested rate before any projection.
    terminal_value(1, g, a['cases'].get(case,{}).get('mature_incremental_roic',0), w)
    rows, anchor = transition(model,a,case,g,wacc=w)
    final=rows[-1]
    terminal = terminal_value(final['nopat']*(1+g),g,a['cases'][case]['mature_incremental_roic'],w)
    # At steady state reinvestment and FCFF must grow smoothly with sales.
    if abs(terminal['fcff']-final['fcff']*(1+g)) > 1e-7:
        raise ValueError('Terminal cash flow fails continuity check.')
    schedule=copy.deepcopy(model['future_fcff_schedule'])+rows
    result=discounted_value(schedule,terminal['value'],final['years_after_cutoff'],w)
    return dict(case=case,wacc=w,growth=g,transition=rows,anchor=anchor,terminal=terminal,
                schedule=schedule,**result)


def build_report():
    inputs=load_inputs(); a=assumptions(); results={}
    for case in ('base','upside'):
        model=project(*inputs,case=case)
        results[case]=value(model,a,case)
    base=project(*inputs)
    rate=discount_rate(base,inputs[-1],a)
    grid=[dict(wacc=w,growth=g,enterprise_value=value(base,a,wacc=w,growth=g)['enterprise_value'])
          for w in a['discount_rate']['wacc_grid'] for g in a['discount_rate']['terminal_growth_grid']]
    try:
        project(*inputs,case='downside')
    except FundingGap as error:
        downside=str(error)
    else:
        downside='Funding now passes; a separately supported recovery/terminal scenario is still required.'
    return dict(rate=rate,cases=results,grid=grid,downside_gate=downside)


def render(report):
    d=report['rate']
    lines=['# Working WACC and sustainable cash-flow transition','',
           'USD millions. Standalone operating enterprise values, NOT share prices or an investment recommendation. '
           'This report isolates operating value; see equity-bridge, downside-exit, comparables and the committee memo for the integrated conditional decision. Pending transaction scope remains a limitation.','',
           f'Calculated WACC proxy {d["calculated_wacc"]:.4%}; selected working rate {d["selected_wacc"]:.1%}. '
           f'Cost of equity {d["cost_of_equity"]:.4%}; debt weight {d["debt_weight"]:.4%}.','',
           '| Case | PV explicit FCFF through 2040 | PV terminal | Operating EV | Terminal share of EV |',
           '|---|---:|---:|---:|---:|']
    for case,r in report['cases'].items():
        share='not meaningful' if r['terminal_share'] is None else f'{r["terminal_share"]:.1%}'
        lines.append(f'| {case} | {r["pv_explicit_fcff"]:,.3f} | {r["pv_terminal"]:,.3f} | {r["enterprise_value"]:,.3f} | {share} |')
    lines+=['','A negative operating EV is the net present cost of continuing this specified strategy. '
            'It is not a negative stock price, observed market EV, or an estimated liquidation value. '
            'Management flexibility and alternative strategies require separate analysis; no automatic zero floor is applied.','',
            'A terminal share above 100% means the present value of the explicit cash flows is negative. '
            'It is a warning about dependence on later success, not a calculation error.','',
            'Downside valuation gate: '+report['downside_gate'],
            'No unsupported recovery, zero-value liquidation assumption or funding proceeds are inserted to complete a low-case valuation.','']
    for case,r in report['cases'].items():
        lines += [f'## {case} transition','',
                  '| Year | Revenue | EBIT margin | NOPAT | Net reinvestment | FCFF |','|---|---:|---:|---:|---:|---:|']
        for row in r['transition']:
            lines.append(f'| {row["year"]} | {row["revenue"]:,.3f} | {row["ebit_margin"]:.2%} | {row["nopat"]:,.3f} | {row["reinvestment"]:,.3f} | {row["fcff"]:,.3f} |')
        lines+=['',f'First stable year 2041 FCFF: {r["terminal"]["fcff"]:,.3f}; reinvestment/NOPAT: {r["terminal"]["reinvestment_rate"]:.2%}.','']
    lines+=['## Base operating-EV sensitivity','', '| WACC | Growth | EV |','|---|---:|---:|']
    for r in report['grid']:
        lines.append(f'| {r["wacc"]:.0%} | {r["growth"]:.0%} | {r["enterprise_value"]:,.3f} |')
    lines+=['','Higher perpetual growth also requires more reinvestment. Growth need not increase value when incremental returns are below the discount rate. '
            'WACC effects on signed cash flows must be tested, not assumed globally monotonic.','',
            'Sources, assumptions and challenges: docs/wacc-and-transition.md and data/valuation_assumptions.json. '
            'This development run does not satisfy the student AI-off prediction or final cold-run requirement.']
    return '\n'.join(lines)+'\n'


if __name__=='__main__':
    print(render(build_report()),end='')
