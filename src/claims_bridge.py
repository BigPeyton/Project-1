"""Claims classification and dated bridge diagnostics, not a final valuation."""
import json
from pathlib import Path
from cash_bridge import load_inputs, estimate

ROOT = Path(__file__).resolve().parents[1]


def reconcile_claims(claims, cash):
    leases = claims['finance_leases']
    june_lease_total = leases['annual_total_current_and_noncurrent'] - leases['h1_principal_paid']
    lease_estimate = june_lease_total - cash['estimated_lease_principal_m']
    if abs(june_lease_total - leases['june_noncurrent_reported'] - leases['june_current_estimated']) > 1e-8:
        raise ValueError('Finance lease current/noncurrent reconciliation fails.')
    contingent = claims['contingent_consideration']
    if abs(contingent['prior_amount'] + contingent['acquisition_addition'] + contingent['remeasurement'] - contingent['amount']) > 1e-8:
        raise ValueError('Contingent consideration roll-forward fails.')
    deductions = {
        'other_borrowings': claims['other_borrowings']['amount'],
        'finance_leases_estimated': lease_estimate,
        'contingent_consideration': contingent['amount'],
    }
    deductions.update({x['name']: x['amount'] for x in claims['accrued_financing_and_seller_claims']})
    if any(v < 0 for v in deductions.values()):
        raise ValueError('Claim deductions must be nonnegative.')
    notes = claims['convertible_notes']
    parity = notes['remaining_conversion_shares_m'] * notes['reference_stock_price']
    if notes['converted_claim_deduction'] != 0:
        raise ValueError('Converted notes cannot also be deducted as debt.')
    return dict(deductions=deductions, deductions_total_m=sum(deductions.values()),
                remaining_finance_leases_m=lease_estimate,
                note_conversion_parity_diagnostic_m=parity,
                note_june_fair_value_diagnostic_m=notes['fair_value_june'],
                note_principal_reference_only_m=notes['principal_june'],
                liquidity_after_selected_claims_m=cash['standalone_liquidity_after_reserve_m']-sum(deductions.values()))


def note_treatment(mode, capital, claims, retained_claim_m=None):
    if mode == 'converted':
        if retained_claim_m not in (None, 0):
            raise ValueError('Do not subtract retained debt and count conversion shares.')
        return capital['derived_scenarios']['full_vesting_full_exercise_notes_converted']/1e6, 0.0
    if mode != 'retained' or retained_claim_m is None:
        raise ValueError('Retained notes require an explicit economic claim; no principal default.')
    import math
    if not math.isfinite(retained_claim_m) or retained_claim_m < 0:
        raise ValueError('Retained claim must be finite and nonnegative.')
    return capital['derived_scenarios']['full_vesting_full_exercise_notes_retained']/1e6, retained_claim_m


def main():
    r, c, a = load_inputs()
    cash = estimate(r, c, a, reserve_m=a['base_operating_reserve_m'])
    claims = json.loads((ROOT / 'data/claims.json').read_text(encoding='utf-8'))
    values = reconcile_claims(claims, cash)
    lines = ['# Claims review output', '', 'USD millions. Dated proxies and assumptions; '
             'not a final enterprise value, equity valuation or complete September balance sheet.', '',
             '| Claim | Reference deduction |', '|---|---:|']
    lines += [f'| {k} | {v:,.6f} |' for k,v in values['deductions'].items()]
    lines += [f'| **Selected claims total, before retained notes** | **{values["deductions_total_m"]:,.6f}** |', '',
              f'Estimated standalone liquidity after reserve and selected claims: '
              f'${values["liquidity_after_selected_claims_m"]:,.6f} million.', '',
              'This figure excludes operating business value, remaining hypothetical option receipts, '
              'forward/ATM settlement cases and capped-call value. Future-flow treatment must be reconciled before using it.', '',
              '## Convertible diagnostics', '',
              f'- June principal (reference only): {values["note_principal_reference_only_m"]:.6f}.',
              f'- September-price conversion parity, using dated remaining share population: '
              f'{values["note_conversion_parity_diagnostic_m"]:.6f}.',
              f'- June reported note fair value (stale-date diagnostic): {values["note_june_fair_value_diagnostic_m"]:.6f}.',
              '- Converted case: count note shares and zero note deduction.',
              '- Retained case: exclude conversion shares and require an explicit economic claim assumption.', '',
              'Operating lease payments remain in forecast operating cash costs, so no separate operating-lease deduction. '
              'Finance leases are treated as financing; exclude their future debt service from FCFF. '
              'Earn-outs, fees and seller payables must not also be paid in forecast FCFF after being deducted here.', '',
              'Review details and residual limitations: docs/claims-treatment.md and data/claims.json.']
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
