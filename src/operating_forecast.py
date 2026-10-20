"""Revenue-linked operating forecasts; no cash-flow or per-share valuation yet."""
import json
import math
import copy
from pathlib import Path
from revenue_forecast import forecast as revenue_forecast
from normalize_history import normalize

ROOT = Path(__file__).resolve().parents[1]
PATHS = ('continuing_launch_margin', 'space_margin', 'neutron_contribution_margin',
         'neutron_fixed_commercial_cost', 'rd', 'sga_fixed', 'sga_revenue_fraction')


def load_inputs():
    return tuple(json.loads((ROOT/'data'/name).read_text(encoding='utf-8')) for name in
                 ('reported_financials.json', 'revenue_assumptions.json',
                  'normalization.json', 'operating_assumptions.json'))


def validate(reported, revenue, inputs, case):
    if inputs['cutoff'] != revenue['cutoff'] or inputs['cutoff'] != reported['valuation_cutoff']:
        raise ValueError('Inconsistent information cutoffs.')
    if inputs['units'] != 'USD millions; margins and expense ratios are decimal fractions':
        raise ValueError('Operating inputs must use USD millions and decimal rates.')
    for source in inputs['sources'].values():
        if source['published'] >= inputs['cutoff'][:10]:
            raise ValueError('Evidence requires cutoff timestamp review.')
    h = inputs['historical_checks']
    if not math.isclose(h['h1_launch_gross_profit']+h['h1_space_gross_profit'],
                        reported['h1_2026']['income_statement']['gross_profit']/1000,
                        rel_tol=0, abs_tol=1e-9):
        raise ValueError('Historical segment gross profit does not reconcile.')
    c = inputs['cases'][case]
    for path in PATHS:
        values = c[path]
        if len(values) != 4 or any(not math.isfinite(v) for v in values):
            raise ValueError('Require four finite values for '+path)
        if 'margin' in path:
            if any(v < -1 or v > 1 for v in values):
                raise ValueError('Margin outside modeled range [-100%, 100%].')
        elif any(v < 0 for v in values):
            raise ValueError('Negative expense input.')
        if path == 'sga_revenue_fraction' and any(v > 1 for v in values):
            raise ValueError('SG&A fraction must be a decimal, not whole percent.')
    for q in ('q3', 'q4'):
        if any(not math.isfinite(v) for v in c[q].values()):
            raise ValueError('Nonfinite quarterly expense input.')
        if not -1 <= c[q]['gross_margin'] <= 1 or min(c[q]['rd'], c[q]['sga']) < 0:
            raise ValueError('Invalid quarterly margin or expense.')


def complete_row(row):
    row['cost_of_revenue'] = row['total_revenue']-row['gross_profit']
    row['operating_expenses'] = row['rd']+row['sga']
    row['operating_income'] = row['gross_profit']-row['operating_expenses']
    row['gross_margin'] = row['gross_profit']/row['total_revenue']
    row['operating_margin'] = row['operating_income']/row['total_revenue']
    return row


def forecast(reported, revenue, normalization, inputs, case='base'):
    validate(reported, revenue, inputs, case)
    sales = revenue_forecast(reported, revenue, case)
    c, rc = inputs['cases'][case], revenue['cases'][case]
    historical = reported['h1_2026']['income_statement']
    quarters = []
    for q in ('q3', 'q4'):
        quarters.append(complete_row(dict(period=q, total_revenue=rc[q+'_total'],
                            gross_profit=rc[q+'_total']*c[q]['gross_margin'],
                            rd=c[q]['rd'], sga=c[q]['sga'])))
    first = dict(sales[0])
    for key in ('gross_profit', 'rd', 'sga'):
        first[key] = historical[key]/1000 + sum(q[key] for q in quarters)
    first = complete_row(first)
    adjustment = normalize(reported, normalization)['h1_2026']['adjustment']/1000
    first['historical_cancellation_adjustment'] = adjustment
    first['normalized_operating_income'] = first['operating_income']+adjustment
    first['normalized_sga'] = first['sga']-adjustment
    rows = [first]
    for i, sales_row in enumerate(sales[1:]):
        row = dict(sales_row)
        row['continuing_launch_gross_profit'] = row['continuing_launch']*c['continuing_launch_margin'][i]
        row['space_gross_profit'] = row['space_systems']*c['space_margin'][i]
        row['neutron_contribution'] = row['incremental_neutron']*c['neutron_contribution_margin'][i]
        row['neutron_fixed_commercial_cost'] = c['neutron_fixed_commercial_cost'][i]
        row['neutron_gross_profit'] = row['neutron_contribution']-row['neutron_fixed_commercial_cost']
        row['gross_profit'] = row['continuing_launch_gross_profit']+row['space_gross_profit']+row['neutron_gross_profit']
        row['rd'] = c['rd'][i]
        row['sga_fixed'] = c['sga_fixed'][i]
        row['sga_revenue_linked'] = c['sga_revenue_fraction'][i]*row['total_revenue']
        row['sga'] = row['sga_fixed']+row['sga_revenue_linked']
        complete_row(row)
        row['historical_cancellation_adjustment'] = 0.0
        row['normalized_operating_income'] = row['operating_income']
        row['normalized_sga'] = row['sga']
        rows.append(row)
    g = revenue['management_guidance']
    q3 = quarters[0]
    return dict(annual=rows, quarters_2026=quarters,
                q3_margin_in_guidance=g['gaap_gross_margin_low'] <= q3['gross_margin'] <= g['gaap_gross_margin_high'],
                q3_opex_in_guidance=g['gaap_opex_low'] <= q3['operating_expenses'] <= g['gaap_opex_high'])


def render(*inputs):
    cases = {case: forecast(*inputs, case=case) for case in inputs[3]['cases']}
    lines = ['# Working operating forecast', '',
             'USD millions. As-of September 10 scenarios prepared October 19. '
             'Operating profit (EBIT), not net income, free cash flow or a valuation. '
             'FY2026 includes actual H1 expenses; later periods are analyst projections.', '',
             '## Base operating statement', '',
             '| Year | Revenue | Cost of revenue | Gross profit | Gross margin | R&D | SG&A | EBIT |',
             '|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in cases['base']['annual']:
        lines.append(f'| {r["year"]} | {r["total_revenue"]:,.3f} | {r["cost_of_revenue"]:,.3f} | '
                     f'{r["gross_profit"]:,.3f} | {r["gross_margin"]:.1%} | {r["rd"]:,.3f} | '
                     f'{r["sga"]:,.3f} | {r["operating_income"]:,.3f} |')
    first = cases['base']['annual'][0]
    lines += ['', f'FY2026 separate normalized EBIT: {first["normalized_operating_income"]:,.3f}, '
              f'after removing only the historical {first["historical_cancellation_adjustment"]:,.3f} '
              'noncash cancellation charge. This does not create cash or alter the reported H1 record.', '',
              '## EBIT across linked revenue/cost scenarios', '',
              '| Case | 2026 | 2027 | 2028 | 2029 | 2030 |', '|---|---:|---:|---:|---:|---:|']
    for case, result in cases.items():
        lines.append('| '+case+' | '+' | '.join(f'{r["operating_income"]:,.3f}' for r in result['annual'])+' |')
    lines += ['', '## Q3 guidance comparison', '',
              '| Case | Gross margin | R&D | SG&A | Total opex | Margin / opex inside guidance |',
              '|---|---:|---:|---:|---:|---|']
    for case, result in cases.items():
        q = result['quarters_2026'][0]
        lines.append(f'| {case} | {q["gross_margin"]:.1%} | {q["rd"]:.3f} | {q["sga"]:.3f} | '
                     f'{q["operating_expenses"]:.3f} | {result["q3_margin_in_guidance"]} / {result["q3_opex_in_guidance"]} |')
    lines += ['', 'Management Q3 GAAP guidance: gross margin 29-31%; operating expenses 143-149. '
              'The downside deliberately misses both. The quarterly expense split and all later paths are analyst assumptions.', '',
              '## Base Neutron cost visibility', '',
              '| Year | Incremental revenue | Contribution before fixed commercial cost | Fixed commercial cost | Gross profit |',
              '|---|---:|---:|---:|---:|']
    for r in cases['base']['annual'][1:]:
        lines.append(f'| {r["year"]} | {r["incremental_neutron"]:.3f} | {r["neutron_contribution"]:.3f} | '
                     f'{r["neutron_fixed_commercial_cost"]:.3f} | {r["neutron_gross_profit"]:.3f} |')
    lines += ['', 'R&D remains separately expensed at the total-company level. Fixed commercial costs '
              'remain even if incremental Neutron revenue is zero. This cost split is an analyst assumption, '
              'not a disclosed program budget. D&A and ordinary SBC remain inside operating costs.', '',
              '## Zero incremental Neutron revenue stress', '',
              'Set the base Neutron revenue ramp to zero; retain base R&D and fixed commercial readiness costs. '
              'The revenue-linked SG&A allowance falls mechanically. This is an isolated operating stress, '
              'not a complete shutdown or abandonment scenario.', '',
              '| Year | Base EBIT | Zero-ramp EBIT | Change |', '|---|---:|---:|---:|']
    zero_inputs = copy.deepcopy(inputs)
    zero_inputs[1]['cases']['base']['neutron_revenue_equivalents_2026_2030'] = [0]*5
    zero = forecast(*zero_inputs)['annual']
    for base, stress in zip(cases['base']['annual'], zero):
        lines.append(f'| {base["year"]} | {base["operating_income"]:.3f} | {stress["operating_income"]:.3f} | '
                     f'{stress["operating_income"]-base["operating_income"]:.3f} |')
    lines += ['',
              'Costs are linked to revenue scenarios, but taxes, reinvestment, funding and full statements '
              'remain unfinished. Do not interpret EBIT break-even as cash break-even or a recommendation.', '',
              'Sources and driver challenges: data/operating_assumptions.json; explanation: docs/operating-forecast.md.']
    return '\n'.join(lines)+'\n'


if __name__ == '__main__':
    print(render(*load_inputs()), end='')
