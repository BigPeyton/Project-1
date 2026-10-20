"""Reconcile reported earnings to an explicitly limited operating run-rate view."""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_inputs():
    return tuple(json.loads((ROOT / 'data' / name).read_text(encoding='utf-8'))
                 for name in ('reported_financials.json', 'normalization.json'))


def normalize(reported, policy):
    if policy['units'] != 'USD thousands':
        raise ValueError('Normalization inputs must be USD thousands.')
    accepted = {p: [] for p in ('fy2025', 'h1_2026')}
    seen = set()
    for item in policy['adjustments']:
        amount = item['expense_amount']
        if item['id'] in seen:
            raise ValueError('Duplicate normalization adjustment.')
        seen.add(item['id'])
        if not math.isfinite(amount) or amount < 0:
            raise ValueError('Expense adjustment must be finite and nonnegative.')
        if item['period'] not in accepted or item['line'] not in ('sga', 'rd', 'cost_of_revenue'):
            raise ValueError('Unsupported operating adjustment scope.')
        source = policy['sources'][item['source_id']]
        if source['published'] > policy['information_cutoff'][:10]:
            raise ValueError('Post-cutoff normalization evidence.')
        if item['treatment'] == 'remove_from_run_rate':
            if not item['noncash_sbc']:
                raise ValueError('New adjustment types require a separate cash reconciliation.')
            accepted[item['period']].append(item)
        elif item['treatment'] != 'retain':
            raise ValueError('Unknown normalization treatment.')
    result = {}
    for period, adjustments in accepted.items():
        facts = reported[period]['income_statement']
        tax = facts.get('tax_expense', 0) - facts.get('tax_benefit', 0)
        other = facts['pretax_income'] - facts['operating_income']
        if facts['net_income'] + tax - other != facts['operating_income']:
            raise ValueError('Reported net income to EBIT does not reconcile.')
        normalized = dict(facts)
        for item in adjustments:
            normalized[item['line']] -= item['expense_amount']
        normalized_ebit = (normalized['revenue'] - normalized['cost_of_revenue']
                           - normalized['rd'] - normalized['sga'])
        delta = sum(i['expense_amount'] for i in adjustments)
        if normalized_ebit != facts['operating_income'] + delta:
            raise ValueError('Normalized operating statement does not articulate.')
        result[period] = dict(net_income=facts['net_income'], tax_expense_signed=tax,
                              total_other_income=other, reported_ebit=facts['operating_income'],
                              adjustment=delta, normalized_ebit=normalized_ebit,
                              normalized_sga=normalized['sga'],
                              normalized_margin=normalized_ebit/facts['revenue'])
    cf = reported['h1_2026']['cash_flow']
    release = policy['h1_2026_release_crosscheck']
    if release['depreciation'] + release['amortization'] != cf['depreciation_amortization']:
        raise ValueError('Aggregate D&A does not reconcile across sources.')
    if sum(release['sbc_'+line] for line in ('cost_of_revenue', 'rd', 'sga')) != cf['sbc']:
        raise ValueError('SBC operating allocations do not reconcile.')
    cancellation = sum(i['expense_amount'] for i in accepted['h1_2026'])
    if cancellation > cf['sbc']:
        raise ValueError('Removed SBC exceeds total reported SBC.')
    h1 = result['h1_2026']
    h1['remaining_sbc'] = cf['sbc'] - cancellation
    # Presentation-only illustration holding reported taxes and every other CFO component fixed.
    # A noncash expense removal must be offset by removing its cash-flow addback.
    h1['illustrative_cfo_unchanged'] = cf['cfo'] + h1['adjustment'] - cancellation
    return result


def render(result):
    lines = ['# Historical earnings normalization', '',
             'USD millions; FY2025 is twelve months, H1 2026 is six months. '
             'Analyst operating view, not a restatement or cash-flow forecast.', '',
             '| Reconciliation | FY2025 | H1 2026 |', '|---|---:|---:|']
    labels = [('Reported net income', 'net_income'), ('Add signed tax expense (benefit)', 'tax_expense_signed'),
              ('Subtract total other income, net', 'total_other_income'), ('Reported operating income (EBIT)', 'reported_ebit'),
              ('Accepted operating expense removal', 'adjustment'), ('Normalized operating income (EBIT)', 'normalized_ebit'),
              ('Normalized SG&A', 'normalized_sga')]
    for label, key in labels:
        lines.append(f'| {label} | {result["fy2025"][key]/1000:,.3f} | {result["h1_2026"][key]/1000:,.3f} |')
    h1 = result['h1_2026']
    lines += ['', f'H1 normalized operating margin: {h1["normalized_margin"]:.2%}.',
              f'H1 SBC retained after the cancellation removal: ${h1["remaining_sbc"]/1000:,.3f} million.',
              f'Historical H1 operating cash flow remains ${h1["illustrative_cfo_unchanged"]/1000:,.3f} million.', '',
              'Only the identified RSU cancellation is removed. Regular SBC, R&D, depreciation/amortization, '
              'transaction costs and inventory step-up remain in operating costs. '
              'The FY2025 operating adjustment is zero under this conservative policy.', '',
              'Source locators, challenges and change evidence: data/normalization.json. '
              'Interpretation and forecast integration: docs/normalization.md.']
    return '\n'.join(lines) + '\n'


if __name__ == '__main__':
    print(render(normalize(*load_inputs())), end='')
