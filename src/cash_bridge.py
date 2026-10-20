"""Estimated cutoff liquidity, with reported facts separate from assumptions.

Run: python src/cash_bridge.py [--write]
No network access or third-party packages. This is not a full balance sheet.
"""
import json
import math
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_inputs():
    return tuple(json.loads((ROOT / 'data' / name).read_text(encoding='utf-8'))
                 for name in ('reported_financials.json', 'capitalization.json',
                              'cash_bridge_assumptions.json'))


def estimate(reported, capital, assumptions, *, burn_multiplier=1.0,
             reserve_m=200.0, securities_haircut=0.0, atm_fraction=0.0,
             issue_price=61.96, atm_other_costs_m=0.0):
    numbers = (burn_multiplier, reserve_m, securities_haircut, atm_fraction,
               issue_price, atm_other_costs_m)
    if not all(math.isfinite(x) for x in numbers):
        raise ValueError('Inputs must be finite.')
    if burn_multiplier < 0 or reserve_m < 0 or issue_price <= 0 or atm_other_costs_m < 0:
        raise ValueError('Require nonnegative burn/reserve/costs and positive issue price.')
    if not 0 <= securities_haircut <= 1 or not 0 <= atm_fraction <= 1:
        raise ValueError('Haircut and financing fraction must be between zero and one.')
    if atm_fraction == 0 and atm_other_costs_m != 0:
        raise ValueError('No completed issuance cannot carry scenario issuance costs.')
    opening = date.fromisoformat(assumptions['opening_date'])
    cutoff = date.fromisoformat(assumptions['valuation_date'])
    days = (cutoff - opening).days
    historical_days = (opening - date.fromisoformat(assumptions['historical_start_exclusive'])).days
    if days < 0 or historical_days <= 0:
        raise ValueError('Invalid cash bridge dates.')
    h1 = reported['h1_2026']
    bs, cf = h1['balance_sheet'], h1['cash_flow']
    opening_cash = bs['cash'] / 1000
    operating_capex_use = (-cf['cfo'] + cf['capex_cash_outflow']) / 1000
    burn = operating_capex_use * days / historical_days * burn_multiplier
    lease = assumptions['h1_finance_lease_principal_m'] * days / historical_days
    exercise_source = capital['sources']['september_option_exercise']
    exercise_date = date.fromisoformat(exercise_source['measurement_date'])
    exercise_published = date.fromisoformat(exercise_source['filed'])
    exercised_cash = (capital['known_september_exercise']['exercise_proceeds_usd'] / 1e6
                      if opening < exercise_date <= cutoff and exercise_published <= cutoff else 0.0)
    gross_atm = capital['other_capital_items']['atm_authorized_gross_usd'] / 1e6 * atm_fraction
    commission = capital['other_capital_items']['atm_max_sales_commission_fraction']
    net_atm = gross_atm * (1 - commission) - atm_other_costs_m
    new_shares_m = gross_atm / issue_price
    cash = opening_cash - burn - lease + exercised_cash + net_atm
    securities = (bs['securities_current'] + bs['securities_noncurrent']) / 1000
    securities_mark = securities * (1 - securities_haircut)
    liquidity = cash + securities_mark
    if cash < 0 or liquidity < reserve_m:
        raise ValueError('Estimated liquidity cannot fund the selected cash/reserve assumptions.')
    option_proceeds = capital['derived_scenarios']['gross_option_exercise_proceeds_usd'] / 1e6
    return dict(days=days, historical_days=historical_days, opening_cash_m=opening_cash,
                estimated_operating_capex_use_m=burn, estimated_lease_principal_m=lease,
                known_option_receipt_m=exercised_cash, estimated_cash_m=cash,
                securities_before_haircut_m=securities, securities_m=securities_mark,
                excluded_restricted_cash_m=bs['restricted_cash'] / 1000,
                total_liquidity_m=liquidity, operating_reserve_m=reserve_m,
                standalone_liquidity_after_reserve_m=liquidity-reserve_m,
                hypothetical_atm_gross_m=gross_atm, hypothetical_atm_net_m=net_atm,
                hypothetical_atm_new_shares_m=new_shares_m,
                hypothetical_remaining_option_receipts_m=option_proceeds-exercised_cash)


def report(reported, capital, assumptions):
    base = estimate(reported, capital, assumptions,
                    burn_multiplier=assumptions['base_burn_multiplier'],
                    reserve_m=assumptions['base_operating_reserve_m'],
                    securities_haircut=assumptions['base_securities_haircut'],
                    atm_fraction=assumptions['base_atm_completion_fraction'],
                    issue_price=assumptions['atm_reference_issue_price_usd'],
                    atm_other_costs_m=assumptions['base_atm_other_expenses_m'])
    lines = ['# September 10 estimated cash bridge', '',
             'USD millions. Estimates use only pre-cutoff sources. This is a standalone '
             'liquidity estimate, not reported September cash, a complete balance sheet, '
             'distributable surplus, or final equity value.', '',
             '| Component | Amount |', '|---|---:|']
    fields = [('Reported June cash', 'opening_cash_m'),
              ('Estimated operating/capex use (deduct)', 'estimated_operating_capex_use_m'),
              ('Estimated finance-lease principal (deduct)', 'estimated_lease_principal_m'),
              ('Known September option receipt (add)', 'known_option_receipt_m'),
              ('Estimated September cash', 'estimated_cash_m'),
              ('Investments at June fair value (assumed unchanged)', 'securities_m'),
              ('Estimated cash plus investments', 'total_liquidity_m'),
              ('Analyst operating reserve (deduct)', 'operating_reserve_m'),
              ('Standalone liquidity after reserve; before other claims', 'standalone_liquidity_after_reserve_m')]
    lines.extend(f'| {label} | {base[key]:,.3f} |' for label, key in fields)
    lines += ['', f'Historical-rate interpolation: {base["days"]} / {base["historical_days"]} days. '
              'No separate interest-income addition; it is already embedded in historical CFO.', '',
              '## Liquidity assumptions', '',
              '| Scenario | Cash estimate | After reserve and investment haircut |', '|---|---:|---:|']
    cases = {}
    for s in assumptions['liquidity_scenarios']:
        result = estimate(reported, capital, assumptions, burn_multiplier=s['burn_multiplier'],
                          reserve_m=s['reserve_m'], securities_haircut=s['securities_haircut'])
        cases[s['name']] = result
        lines.append(f'| {s["name"]} | {result["estimated_cash_m"]:,.3f} | '
                     f'{result["standalone_liquidity_after_reserve_m"]:,.3f} |')
    lines += ['', '## Separate hypothetical ATM cases', '',
              'Illustrative issuance at $61.96 with 2% commission, before unquantified other expenses. '
              'These are not observed completion amounts or statistical bounds.', '',
              '| Authorized amount assumed issued | Net cash added | New shares, millions |', '|---|---:|---:|']
    financing = {}
    for fraction in (0.0, 0.5, 1.0):
        result = estimate(reported, capital, assumptions, atm_fraction=fraction)
        financing[str(fraction)] = result
        lines.append(f'| {fraction:.0%} | {result["hypothetical_atm_net_m"]:,.3f} | '
                     f'{result["hypothetical_atm_new_shares_m"]:,.6f} |')
    lines += ['', 'Restricted cash is excluded from the starting cash figure already; no second deduction. '
              'Undrawn loans, unsettled forwards and future option receipts are not current cash.', '',
              f'Full-exercise bridge may add only the remaining ${base["hypothetical_remaining_option_receipts_m"]:.6f} million '
              'option receipts beyond cash already included, subject to the award and exercise assumptions.', '',
              'Pending acquisition funding, other claims, omitted cash movements and the dated investment values '
              'must remain visible. Do not discount pre-cutoff spending again in the future FCFF forecast.']
    return '\n'.join(lines)+'\n', dict(reference=base, liquidity_cases=cases, financing_cases=financing)


if __name__ == '__main__':
    text, values = report(*load_inputs())
    if '--write' in sys.argv:
        (ROOT / 'outputs/cash-bridge.md').write_text(text, encoding='utf-8')
        (ROOT / 'outputs/cash-bridge.json').write_text(json.dumps(values, indent=2)+'\n', encoding='utf-8')
    print(text)
