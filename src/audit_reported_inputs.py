"""Reconcile transcribed filing facts; this is not a valuation or locked exercise.

Run from the project root: python src/audit_reported_inputs.py
Uses only the standard library. Source URLs and exact locators are in the JSON.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ('cash securities_current receivables contract_assets inventory '
          'prepaids_other_current ppe intangibles goodwill rou_operating '
          'rou_finance securities_noncurrent restricted_cash deferred_tax_assets '
          'other_noncurrent_assets').split()
LIABILITIES = ('payables accrued_expenses employee_benefits contract_liabilities '
               'other_current_liabilities convertible_notes_net other_borrowings_net '
               'lease_operating_noncurrent lease_finance_noncurrent '
               'deferred_tax_liabilities other_noncurrent_liabilities').split()


def main():
    data = json.loads((ROOT / 'data/reported_financials.json').read_text(encoding='utf-8'))
    lines = ['# Reported-input reconciliation', '',
             'Scope: transcribed filing arithmetic and publication dates only. '
             'Not a completed source audit, final valuation, or AI-off student exercise.', '']
    checks = []

    def check(label, actual, expected):
        if actual != expected:
            raise ValueError(f'{label}: {actual} != {expected}')
        checks.append(label)
        lines.append(f'- PASS: {label}')

    for source in ('K25', 'Q26'):
        check(f'{source} published before valuation cutoff',
              data['sources'][source]['published'] < data['valuation_cutoff'][:10], True)
    for name in ('fy2025', 'h1_2026'):
        record = data[name]
        bs, income = record['balance_sheet'], record['income_statement']
        check(f'{name}: asset components', sum(bs[k] for k in ASSETS), bs['total_assets'])
        check(f'{name}: liability components', sum(bs[k] for k in LIABILITIES), bs['total_liabilities'])
        check(f'{name}: assets = liabilities + equity', bs['total_assets'], bs['total_liabilities'] + bs['equity'])
        check(f'{name}: gross profit', income['revenue'] - income['cost_of_revenue'], income['gross_profit'])
        check(f'{name}: operating income', income['gross_profit'] - income['rd'] - income['sga'], income['operating_income'])
    fy, h1 = data['fy2025'], data['h1_2026']
    cf = h1['cash_flow']
    check('H1 cash-flow roll-forward including restricted cash',
          cf['cash_including_restricted_open'] + cf['cfo'] + cf['cfi'] + cf['cff'] + cf['fx_cash'],
          cf['cash_including_restricted_close'])
    check('H1 ending cash definition ties to balance sheet',
          h1['balance_sheet']['cash'] + h1['balance_sheet']['restricted_cash'], cf['cash_including_restricted_close'])
    check('H1 opening cash definition ties to prior balance sheet',
          fy['balance_sheet']['cash'] + fy['balance_sheet']['restricted_cash'], cf['cash_including_restricted_open'])
    check('Convertible net carrying amount vs principal less issuance costs',
          h1['convertible_principal'] - h1['unamortized_note_costs'], h1['balance_sheet']['convertible_notes_net'])
    ttm = fy['income_statement']['revenue'] - h1['h1_2025_comparative_revenue'] + h1['income_statement']['revenue']
    lines.extend(['', f'{len(checks)} checks passed.', '',
                  f'Derived TTM revenue through June 30, 2026: USD {ttm / 1000:.3f} million '
                  '(FY2025 minus H1 2025 plus H1 2026; reported acquisition scope, not organic growth).',
                  '', 'Outstanding: ' + '; '.join(data['not_yet_resolved']) + '.'])
    output = '\n'.join(lines) + '\n'
    (ROOT / 'outputs/reported-input-checks.md').write_text(output, encoding='utf-8')
    print(output)


if __name__ == '__main__':
    main()
