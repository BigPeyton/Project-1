"""Unfunded continuation versus a separately assumed orderly exit before failure."""
import json
import math
from pathlib import Path
from three_statements import load_inputs,project,FundingGap
from valuation import discounted_value
from equity_bridge import bridge,assumptions as bridge_assumptions
ROOT=Path(__file__).resolve().parents[1]


def assumptions():
    return json.loads((ROOT/'data/downside_exit_assumptions.json').read_text())


def evaluate(a=None):
    a=assumptions() if a is None else a
    if not math.isfinite(a['closure_cost']) or a['closure_cost']<0:
        raise ValueError('Closure cost must be finite and nonnegative.')
    if any(not math.isfinite(x) or not 0<=x<=1 for x in a['recoveries'].values()):
        raise ValueError('Recovery rates must be between zero and one.')
    if set(a['recoveries']) & {'cash','securities','customer_financing'}:
        raise ValueError('Nonoperating cash/financial assets cannot be recovered a second time.')
    inputs=load_inputs(); m=project(*inputs,case='downside',end_year=a['exit_year'])
    bs=m['annual'][-1]['balance_sheet']
    receipts={k:bs[k]*fraction for k,fraction in a['recoveries'].items()}
    allowed={'ordinary_liabilities','contract_liabilities','operating_lease_noncurrent',
             'deferred_tax_liabilities','capex_payable','contract_loss_provision'}
    if set(a['settle_operating_liabilities'])!=allowed or len(a['settle_operating_liabilities'])!=len(allowed):
        raise ValueError('Settlement map must cover each operating claim once; financial claims belong to the bridge.')
    payments={k:bs[k] for k in sorted(allowed)}
    net=sum(receipts.values())-sum(payments.values())-a['closure_cost']
    financing_exit=sum(bs[k] for k in ('notes','other_debt','finance_leases','earnout','financing_fee_payable','seller_payable'))
    actual_cash_check=bs['cash']+bs['securities']+net-financing_exit
    if actual_cash_check<0:
        raise ValueError('Assumed exit cannot pay modeled obligations; a recovery waterfall is required.')
    terminal=net+m['cutoff_bridge_inputs']['operating_reserve']
    schedule=m['future_fcff_schedule']
    v=dict(case='downside',**discounted_value(schedule,terminal,schedule[-1]['years_after_cutoff'],a['wacc']))
    eq=bridge(m,v,inputs[-1],bridge_assumptions())
    diagnostic=bridge(m,v,inputs[-1],bridge_assumptions(),mode='intrinsic_only',option_mode='intrinsic')
    return dict(exit_year=a['exit_year'],closure_cost=a['closure_cost'],asset_recoveries=receipts,
                operating_settlements=payments,net_exit_recovery=net,reserve_release=m['cutoff_bridge_inputs']['operating_reserve'],
                terminal_exit_cashflow=terminal,exit_financial_claims=financing_exit,
                exit_cash_sufficiency=actual_cash_check,schedule=schedule,valuation=v,
                equity_if_converted=eq,intrinsic_only_diagnostic=diagnostic,
                new_financing=m['total_net_equity_raised'])


def render(r):
    lines=['# Downside: continuation failure and assumed orderly exit','',
           'The unchanged five-year downside fails funding in 2030. This separate analyst scenario stops operations at the end of '+str(r['exit_year'])+
           '. No new financing or profitable perpetual recovery is assumed. Recoveries/closure costs are unverified scenario judgments, not a guaranteed floor.','',
           '| Exit component, USD millions | Amount |','|---|---:|']
    for k,v in r['asset_recoveries'].items(): lines.append(f'| recover {k} | {v:,.3f} |')
    for k,v in r['operating_settlements'].items(): lines.append(f'| settle {k} | {-v:,.3f} |')
    for k in ('closure_cost','net_exit_recovery','reserve_release','terminal_exit_cashflow','exit_cash_sufficiency'):
        lines.append(f'| {k} | {r[k]:,.3f} |')
    lines+=['',f'Operating strategy EV: {r["valuation"]["enterprise_value"]:,.3f} million.',
            f'Conditional if-converted value: {r["equity_if_converted"]["price"]:.4f}/share.',
            f'Intrinsic-only note/option allocation diagnostic: {r["intrinsic_only_diagnostic"]["price"]:.4f}/share.',
            'No cash/securities are added twice: cutoff cash is in the equity bridge; only the previously excluded operating reserve is released at exit. '
            'Financial obligations remain in the bridge and are used separately in the exit liquidity check, not deducted twice from value.','',
            'This is a cutoff FCFF capital-budgeting valuation. Exit cash sufficiency is an undiscounted liquidity check, not the valuation numerator. '
            'Financing returns, risk discounting and the cash-reserve convention differ; do not present the result as an observed liquidation distribution.','',
            'The scenario can change the action toward do-not-initiate if execution deteriorates and financing/credible restructuring is absent. '
            'Earlier shutdown, legal restrictions, realization delays, contract damages and lower recoveries can change this result materially.']
    return '\n'.join(lines)+'\n'


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(); p.add_argument('--save',action='store_true'); args=p.parse_args(); r=evaluate()
    if args.save:
        (ROOT/'outputs/downside-exit.md').write_text(render(r),encoding='utf-8')
        (ROOT/'outputs/downside-exit.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
        print('Saved downside-exit outputs.')
    else: print(render(r),end='')
