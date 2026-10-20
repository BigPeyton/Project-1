"""Conditional market-implied diagnostics using the existing standalone engine."""
import copy
import json
import math
from pathlib import Path
from three_statements import load_inputs, project
from valuation import assumptions as valuation_assumptions, value
from equity_bridge import assumptions as bridge_assumptions, bridge

ROOT = Path(__file__).resolve().parents[1]


def assumptions():
    return json.loads((ROOT/'data/reverse_dcf_assumptions.json').read_text())


def bounded_root(fn, target, bounds, intervals=40):
    """Sample the declared interval before bisection; refuse an unbracketed root."""
    lo, hi = bounds
    if not all(math.isfinite(x) for x in (lo, hi, target)) or lo >= hi or target <= 0:
        raise ValueError('Finite ordered bounds and positive target required.')
    if not isinstance(intervals, int) or intervals < 2:
        raise ValueError('At least two grid intervals required.')
    grid = [dict(input=lo+(hi-lo)*i/intervals) for i in range(intervals+1)]
    for row in grid:
        row['price'] = fn(row['input'])
        if not math.isfinite(row['price']): raise ValueError('Nonfinite model output.')
    differences = [b['price']-a['price'] for a,b in zip(grid,grid[1:])]
    increasing = all(d >= 0 for d in differences)
    decreasing = all(d <= 0 for d in differences)
    if not (increasing or decreasing):
        raise ValueError('Sampled interval is not monotonic; isolate a root before solving.')
    result = dict(bounds=list(bounds), grid=grid, sampled_monotonic=True,
                  minimum_price=min(x['price'] for x in grid),
                  maximum_price=max(x['price'] for x in grid), root=None)
    if not result['minimum_price'] <= target <= result['maximum_price']:
        return dict(result,status='not bracketed within declared bounds')
    for _ in range(100):
        mid=(lo+hi)/2; p=fn(mid)
        if not math.isfinite(p): raise ValueError('Nonfinite solver output.')
        if (p < target) == increasing: lo=mid
        else: hi=mid
    root=(lo+hi)/2; actual=fn(root)
    if abs(actual-target) > 1e-7*max(1,target):
        raise ValueError('Root does not reproduce target; possible discontinuity.')
    return dict(result,root=root,reproduced_price=actual,status='solved within declared bounds')


def terminal_requirement(v, b, target, roic, tax):
    """Invert a fixed converted/exercised bridge; USD millions throughout."""
    if not all(math.isfinite(x) for x in (target,roic,tax)) or target <= 0:
        raise ValueError('Positive finite target and finite parameters required.')
    g,w=v['growth'],v['wacc']
    if not 0 <= g < min(w,roic) or not 0 <= tax < 1:
        raise ValueError('Invalid terminal growth, return or tax rate.')
    if b['mode'] != 'converted' or b['unallocated_claim_shortfall'] > 0:
        raise ValueError('Use a positive-residual fixed converted bridge.')
    final=v['transition'][-1]
    net_bridge=b['equity']-v['enterprise_value']
    required_ev=target*b['shares']-net_bridge
    pv_terminal=required_ev-v['pv_explicit_fcff']
    terminal=pv_terminal*(1+w)**final['years_after_cutoff']
    fcff=terminal*(w-g)
    nopat=fcff/(1-g/roic)
    revenue=final['revenue']*(1+g)
    margin=nopat/(1-tax)/revenue
    return dict(required_enterprise_value=required_ev,required_pv_terminal=pv_terminal,
                required_terminal_value=terminal,required_2041_fcff=fcff,
                modeled_2041_fcff=v['terminal']['fcff'],
                required_to_modeled_fcff=fcff/v['terminal']['fcff'],
                fixed_2041_revenue=revenue,implied_2041_ebit_margin=margin,
                exceeds_100_percent_margin=margin>1,
                reconstructed_price=(v['pv_explicit_fcff']+terminal/(1+w)**final['years_after_cutoff']+net_bridge)/b['shares'])


def report():
    inputs=load_inputs(); va=valuation_assumptions(); ba=bridge_assumptions(); a=assumptions()
    if a['cutoff'] != va['cutoff']: raise ValueError('Cutoffs differ.')
    target=va['discount_rate']['reference_price']; cases={}
    for case in ('base','upside'):
        model=project(*inputs,case=case)
        def price(config=va,wacc=None):
            return bridge(model,value(model,config,case,wacc=wacc),inputs[-1],ba)['price']
        v=value(model,va,case); b=bridge(model,v,inputs[-1],ba)
        def margin_price(margin):
            changed=copy.deepcopy(va); changed['cases'][case]['mature_ebit_margin']=margin
            return price(changed)
        # The low margin bound can fail liquidity in some cases; surface that failure.
        try:
            margin=bounded_root(margin_price,target,a['margin_bounds'],a['grid_intervals'])
        except ValueError as error:
            margin=dict(status='model rejected the declared search',error=str(error),root=None)
        wacc=bounded_root(lambda w: price(wacc=w),target,a['wacc_bounds'],a['grid_intervals'])
        terminal=terminal_requirement(v,b,target,va['cases'][case]['mature_incremental_roic'],va['terminal']['tax_rate'])
        stresses=[]
        for label,key,new in [('lower mature margin','mature_ebit_margin',.08),
                              ('lower incremental ROIC','mature_incremental_roic',.10)]:
            changed=copy.deepcopy(va); changed['cases'][case][key]=new
            try: stresses.append(dict(label=label,old=va['cases'][case][key],new=new,price=price(changed)))
            except ValueError as error: stresses.append(dict(label=label,old=va['cases'][case][key],new=new,failure=str(error)))
        cases[case]=dict(reference_price=b['price'],wacc_root=wacc,margin_root=margin,
                         terminal_requirement=terminal,assumption_stresses=stresses,
                         wacc_sensitivity=[dict(wacc=w,price=price(wacc=w)) for w in va['discount_rate']['wacc_grid']])
    return dict(cutoff=a['cutoff'],target_price=target,price_source=a['price_source'],
                risk_free=va['discount_rate']['risk_free'],cases=cases,
                scope='Standalone, fixed converted/full-exercise bridge; no pending Iridium, optional forward/ATM/capped-call proceeds or customer-loan recovery.')


def render(r):
    lines=['# Market-implied expectations and long-term challenges','',
           f'Information cutoff: {r["cutoff"]}. Historical target price: ${r["target_price"]:.2f}.',
           f'Price source: {r["price_source"]} (September 10 row only).', '', r['scope'], '',
           'These are AI-assisted development calculations, not the student AI-off locked exercise. '
           'Each test holds other assumptions fixed; no probability or unique market forecast is inferred.','']
    for case,c in r['cases'].items():
        t=c['terminal_requirement']; w=c['wacc_root']; m=c['margin_root']
        lines += [f'## {case}', '', f'Reference modeled price: ${c["reference_price"]:.4f}.', '',
                  f'**Reverse WACC:** {w["root"]:.4%}, reproducing ${w["reproduced_price"]:.4f}; '
                  f'prior-day Treasury reference {r["risk_free"]:.2%}. '+
                  ('The root is below Treasury. ' if w['root'] < r['risk_free'] else 'The root is only slightly above Treasury. ')+
                  'This is a mathematical diagnostic, not a recommended required return. '
                  'Monotonicity was sampled over the declared interval and the root checked by repricing; no global claim is made.', '',
                  '**Reverse mature margin:** '+m['status']+'.']
        if 'maximum_price' in m:
            lines += [f'The {m["bounds"][0]:.0%}-{m["bounds"][1]:.0%} margin interval produces '
                      f'${m["minimum_price"]:.4f}-${m["maximum_price"]:.4f}. '
                      'The entire margin/capital-efficiency transition changes together. '
                      'The 80% bound is an extreme diagnostic, not an economically supported case.']
        else: lines += [m.get('error','')]
        lines += ['', '**Residual terminal requirement (explicit cash flows held fixed):**', '',
                  f'- Required operating EV: {t["required_enterprise_value"]:,.3f} million USD.',
                  f'- Required 2041 FCFF: {t["required_2041_fcff"]:,.3f} million versus modeled {t["modeled_2041_fcff"]:,.3f} million '
                  f'({t["required_to_modeled_fcff"]:.1f}x).',
                  f'- At fixed 2041 sales of {t["fixed_2041_revenue"]:,.3f} million, implied EBIT margin is {t["implied_2041_ebit_margin"]:.1%}.', '',
                  'This isolated terminal jump violates continuity with the unchanged explicit path. '
                  'It identifies the missing economic burden; it is not an admissible replacement forecast. '
                  'A margin above 100% cannot be supported by ordinary operating sales under this model.', '',
                  '| One-at-a-time challenge | Old | New | USD/share or failure |', '|---|---:|---:|---|']
        for s in c['assumption_stresses']:
            outcome=f'{s["price"]:.4f}' if 'price' in s else s['failure']
            lines.append(f'| {s["label"]} | {s["old"]:.0%} | {s["new"]:.0%} | {outcome} |')
        lines += ['', '| WACC (g held at 3%) | USD/share |', '|---|---:|']
        for row in c['wacc_sensitivity']: lines.append(f'| {row["wacc"]:.0%} | {row["price"]:.4f} |')
        lines += ['']
    lines += ['## Decision implication','',
              'The current standalone revenue, profitability and reinvestment paths do not underwrite the cutoff quote. '
              'A substantially different operating path, transaction economics or other omitted value would need independent support. '
              'This is not proof that every possible Rocket Lab strategy is worth less than the price. '
              'Lower margin/return stresses challenge the working valuation but do not change the proposed no-initiation decision at $61.96. '
              'See docs/committee-decision.md for the provisional committee action and triggers.']
    return '\n'.join(lines)+'\n'


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(); parser.add_argument('--save',action='store_true'); args=parser.parse_args()
    r=report()
    if args.save:
        (ROOT/'outputs/reverse-dcf.md').write_text(render(r),encoding='utf-8')
        (ROOT/'outputs/reverse-dcf.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
        print('Saved reverse-DCF outputs.')
    else: print(render(r),end='')
