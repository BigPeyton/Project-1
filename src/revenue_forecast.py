"""Scenario revenue build, separate from costs, cash flow and valuation."""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_inputs():
    return tuple(json.loads((ROOT / 'data' / name).read_text(encoding='utf-8'))
                 for name in ('reported_financials.json', 'revenue_assumptions.json'))


def forecast(reported, assumptions, case='base'):
    f = assumptions['facts']
    if assumptions['years'] != list(range(2026, 2031)):
        raise ValueError('Require five annual periods, 2026-2030.')
    for source in assumptions['sources'].values():
        # All current sources predate the cutoff day. Same-day evidence needs a timestamp review.
        if source['published'] >= assumptions['cutoff'][:10]:
            raise ValueError('Source requires cutoff timestamp review.')
    if not math.isclose(f['h1_2026_launch'] + f['h1_2026_space_systems'],
                        reported['h1_2026']['income_statement']['revenue']/1000, abs_tol=1e-9):
        raise ValueError('H1 segment revenue does not reconcile to the filing.')
    c = assumptions['cases'][case]
    for key in ('continuing_launch_growth_2027_2030', 'space_growth_2027_2030'):
        path = c[key]
        if len(path) != 4 or any(not math.isfinite(v) or v <= -1 for v in path):
            raise ValueError('Invalid four-year growth path.')
    ramp = c['neutron_revenue_equivalents_2026_2030']
    if len(ramp) != 5 or ramp[0] != 0:
        raise ValueError('Require five Neutron values and no separate 2026 addition.')
    amounts = [c[k] for k in ('q3_total', 'q3_launch', 'q4_total', 'q4_launch',
                              'neutron_revenue_per_equivalent')] + ramp
    if any(not math.isfinite(v) or v < 0 for v in amounts):
        raise ValueError('Revenue inputs must be finite and nonnegative.')
    if any(c[q+'_launch'] > c[q+'_total'] for q in ('q3', 'q4')):
        raise ValueError('Launch revenue cannot exceed quarterly total.')
    continuing = f['h1_2026_launch'] + c['q3_launch'] + c['q4_launch']
    space = f['h1_2026_space_systems'] + sum(c[q+'_total']-c[q+'_launch'] for q in ('q3', 'q4'))
    previous_total = reported['fy2025']['income_statement']['revenue']/1000
    rows = []
    for i, year in enumerate(assumptions['years']):
        if i:
            continuing *= 1 + c['continuing_launch_growth_2027_2030'][i-1]
            space *= 1 + c['space_growth_2027_2030'][i-1]
        neutron = ramp[i] * c['neutron_revenue_per_equivalent']
        total = continuing + space + neutron
        rows.append(dict(year=year, continuing_launch=continuing, incremental_neutron=neutron,
                         total_launch=continuing+neutron, space_systems=space,
                         total_revenue=total, revenue_growth=total/previous_total-1))
        previous_total = total
    return rows


def render(reported, assumptions):
    cases = {c: forecast(reported, assumptions, c) for c in assumptions['cases']}
    lines = ['# Working revenue scenarios', '',
             'USD millions. Analyst assumptions as of September 10; prepared October 19. '
             'Standalone owned business, excluding pending Iridium. Not final valuation results.', '',
             '| Case | 2026 | 2027 | 2028 | 2029 | 2030 |', '|---|---:|---:|---:|---:|---:|']
    for case, rows in cases.items():
        lines.append('| '+case+' | '+' | '.join(f'{r["total_revenue"]:,.3f}' for r in rows)+' |')
    lines += ['', '## Base composition', '',
              '| Year | Continuing launch pool | Incremental Neutron | Space systems | Total | YoY growth |',
              '|---|---:|---:|---:|---:|---:|']
    for r in cases['base']:
        lines.append(f'| {r["year"]} | {r["continuing_launch"]:,.3f} | {r["incremental_neutron"]:,.3f} | '
                     f'{r["space_systems"]:,.3f} | {r["total_revenue"]:,.3f} | {r["revenue_growth"]:.1%} |')
    c = assumptions['cases']['base']
    old = reported['fy2025']['income_statement']['revenue']/1000*1.4
    implied_q4 = old-assumptions['facts']['h1_2026_total']-c['q3_total']
    lines += ['', '## 2026 bridge and lab comparison', '',
              f'- Actual H1: {assumptions["facts"]["h1_2026_total"]:.3f}.',
              f'- Base Q3: {c["q3_total"]:.3f}; management-guidance midpoint, still a forecast.',
              f'- Base Q4: {c["q4_total"]:.3f}; analyst assumption.',
              f'- Base FY2026: {cases["base"][0]["total_revenue"]:.3f}.',
              f'- Archived Lab 10 40% growth implies FY2026 {old:.3f} and Q4 {implied_q4:.3f} '
              'after actual H1 and base Q3. This is a reason to revisit the old assumption, not proof of the new forecast.', '',
              '2026 contains historical revenue. Final DCF must isolate post-cutoff cash flows and avoid '
              'counting pre-cutoff cash use twice. Neutron revenue equivalents are analyst recognition units, '
              'not verified launch counts or prices. Backlog is context, not extra revenue added to these rows.', '',
              'Costs, reinvestment, taxes and funding are integrated separately in three_statements.py. '
              'A revenue-only downside cannot establish an investment recommendation.', '',
              'Sources and every driver challenge: data/revenue_assumptions.json; interpretation: docs/revenue-forecast.md.']
    return '\n'.join(lines)+'\n'


if __name__ == '__main__':
    print(render(*load_inputs()), end='')
