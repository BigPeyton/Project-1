"""One-way operating-driver attribution with explicit range-dependent rankings."""
import copy
import json
import math
from pathlib import Path
from three_statements import load_inputs, project
from valuation import value, assumptions as va
from equity_bridge import bridge, assumptions as ba
ROOT=Path(__file__).resolve().parents[1]


def assumptions():
    return json.loads((ROOT/'data/proforma_sensitivity_assumptions.json').read_text())


def apply_drivers(inputs,case,changes):
    specs=assumptions()['drivers']
    if set(changes)-set(specs): raise ValueError('Unknown operating driver.')
    values={key:spec['default'] for key,spec in specs.items()}
    for key,raw in changes.items():
        try: v=float(raw)
        except (ValueError,TypeError): raise ValueError(f'{key}: finite numeric input required.') from None
        low,high=specs[key]['bounds']
        if not math.isfinite(v) or not low<=v<=high: raise ValueError(f'{key}: allowed range {low} to {high}.')
        values[key]=v
    changed=copy.deepcopy(inputs); rev=changed[1]['cases'][case]; op=changed[3]['cases'][case]
    rev['space_growth_2027_2030']=[v+values['space_growth']/100 for v in rev['space_growth_2027_2030']]
    op['space_margin']=[v+values['space_margin']/100 for v in op['space_margin']]
    op['rd']=[v*values['rd_scale']/100 for v in op['rd']]
    rev['neutron_revenue_equivalents_2026_2030']=[v*values['neutron_scale']/100 for v in rev['neutron_revenue_equivalents_2026_2030']]
    return changed,values


def evaluate(changes=None):
    inputs,values=apply_drivers(load_inputs(),'base',changes or {})
    model=project(*inputs); valuation=value(model,va()); equity=bridge(model,valuation,inputs[-1],ba())
    return dict(inputs=values,metrics=dict(ebit_2030=model['annual'][-1]['operating_income'],
                fcff_2030=model['annual'][-1]['fcff'],price=equity['price']),
                annual=[dict(year=r['year'],revenue=r['total_revenue'],ebit=r['operating_income'],
                             future_fcff=r['future_fcff'],cash=r['balance_sheet']['cash']) for r in model['annual']],
                cutoff_cash=model['cutoff_bridge_inputs']['cash'],enterprise_value=valuation['enterprise_value'],
                changed_paths=dict(space_growth=inputs[1]['cases']['base']['space_growth_2027_2030'],
                    space_margin=inputs[3]['cases']['base']['space_margin'],rd=inputs[3]['cases']['base']['rd'],
                    neutron_equivalents=inputs[1]['cases']['base']['neutron_revenue_equivalents_2026_2030']))


def report():
    a=assumptions(); base=evaluate(); ranges={}
    for name in ('standard','alternative'):
        cases=[]
        for key,spec in a['drivers'].items():
            outcomes=[]
            for endpoint in spec[name]:
                try: outcomes.append(dict(value=endpoint,result=evaluate({key:endpoint})))
                except ValueError as error: outcomes.append(dict(value=endpoint,failure=str(error)))
            spans={metric:abs(outcomes[1]['result']['metrics'][metric]-outcomes[0]['result']['metrics'][metric])
                   for metric in base['metrics']} if all('result' in o for o in outcomes) else None
            cases.append(dict(driver=key,label=spec['label'],bounds=spec[name],outcomes=outcomes,spans=spans))
        ranks={metric:[c['driver'] for c in sorted([c for c in cases if c['spans'] is not None],key=lambda c:c['spans'][metric],reverse=True)] for metric in base['metrics']}
        ranges[name]=dict(cases=cases,rankings=ranks)
    return dict(cutoff=a['cutoff'],classification=a['classification'],base=base,ranges=ranges,
                ranking_changed={m:ranges['standard']['rankings'][m]!=ranges['alternative']['rankings'][m] for m in base['metrics']},
                rule=a['ranking_method'])


def render(r):
    lines=['# Own-pro-forma one-way sensitivities','',r['classification'], '',r['rule'],'',
           'All runs use the same base, WACC 16%, growth 3%, mature margin 12%, marginal return 16% and converted/full-award bridge. Only the named 2027-2030 operating path changes. Historical facts and 2026 remain unchanged. These are not independent student predictions.','',
           '| Base metric | Value |','|---|---:|']
    lines += [f'| {k} | {v:.6f} |' for k,v in r['base']['metrics'].items()]
    for name,group in r['ranges'].items():
        lines += ['',f'## {name.title()} ranges','', '| Driver / endpoint | 2030 EBIT (USD m) | 2030 FCFF (USD m) | USD/share |', '|---|---:|---:|---:|']
        for c in group['cases']:
            for o in c['outcomes']:
                if 'failure' in o: lines.append(f'| {c["label"]} {o["value"]} | FAIL: {o["failure"]} | - | - |')
                else:
                    m=o['result']['metrics']; lines.append(f'| {c["label"]} {o["value"]} | {m["ebit_2030"]:.3f} | {m["fcff_2030"]:.3f} | {m["price"]:.4f} |')
        lines+=['','Largest to smallest absolute endpoint spread:']
        for metric,rank in group['rankings'].items(): lines.append(f'- {metric}: '+ ' > '.join(rank))
    lines += ['', '## Interpretation and bounds','',
              'Importance is conditional on both the output metric and the selected shock sizes. The alternative narrows growth/margin/Neutron uncertainty while widening R&D uncertainty; compare the displayed ranks instead of calling any one driver universally dominant. '
              'None of these isolated stresses warrants initiation at $61.96. Cost reductions with revenue held fixed are attribution tests, not implementable cost-cutting advice. '
              'Combined scenarios remain necessary for correlated delays, capex and funding risks.','']
    for key,spec in assumptions()['drivers'].items():
        lines += [f'### {spec["label"]}',f'- Units: {spec["unit"]}.',f'- Basis: {spec["basis"]}',f'- Causal link: {spec["causal_link"]}',f'- Challenge: {spec["challenge"]}',f'- Change evidence: {spec["change_evidence"]}','']
    lines += ['Valuation control bounds: '+assumptions()['valuation_control_bounds']]
    return '\n'.join(lines)+'\n'


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--save',action='store_true');args=p.parse_args();r=report()
    if args.save:
        (ROOT/'outputs/proforma-sensitivity.md').write_text(render(r),encoding='utf-8')
        (ROOT/'outputs/proforma-sensitivity.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
        print('Saved operating sensitivity and ranking report.')
    else: print(render(r),end='')
