"""FIN 43900 Lab 10: Rocket Lab, FY2026-2030 classroom scenario.
USD millions; shares in millions. See rocketlab_lab10.md for evidence and limits.
Run: python rocketlab_lab10.py
Failure tests: --break-cash or --stress-funding. No third-party packages.
"""
import math
import sys

# Forecast choices are JUDGMENTS, not company guidance (details in the notes).
GROWTH = [0.40, 0.35, 0.30, 0.25, 0.20]
GROSS_MARGIN = [0.35, 0.38, 0.40, 0.42, 0.43]
SGA_REVENUE = [0.23, 0.21, 0.19, 0.17, 0.16]
RD = [290.0, 300.0, 310.0, 320.0, 330.0]
CAPEX = [160.0, 170.0, 180.0, 190.0, 200.0]
AMORTIZATION = [29.730, 28.755, 27.718, 25.512, 21.690]
DEPRECIATION_RATE = 25.369 / 194.838  # FY2025 depreciation / opening net PP&E
INVENTORY_DAYS = 158.407 / 394.618 * 365
AR_RATIO, CONTRACT_ASSET_RATIO = 39.001 / 601.799, 61.606 / 601.799
PREPAID_RATIO, PAYABLE_RATIO = 89.953 / 601.799, 72.699 / 394.618
CONTRACT_LIABILITY_RATIO = 195.438 / 601.799
MINIMUM_CASH, COST_OF_EQUITY, TERMINAL_GROWTH = 100.0, 0.15, 0.03
TAX_RATE = 0.25
MARKET_PRICE = 74.63
MARKET_TIMESTAMP = 'September 24, 2026, 1:46 PM EDT (intraday)'
# Complete June 30 capitalization: 2026 Q2 10-Q p. 5 and S-4/A section 5.05.
# Supplemental denominator comparison only, NOT an updated operating valuation.
REPORTED_COMMON = 598.180438
REPORTED_PREFERRED = 40.951250
REMAINING_NOTE_SHARES = 2.607745
COMPARISON_SHARES = REPORTED_COMMON + REPORTED_PREFERRED + REMAINING_NOTE_SHARES

# FY2025 10-K F-5. Other assets/liabilities are explicit fixed residual groups.
OPENING = dict(year=2025, revenue=601.799, cash=828.660, securities=270.164,
    receivables=39.001, contract_assets=61.606, inventory=158.407,
    prepaids=89.953, ppe=319.473, intangibles=224.746,
    other_assets=332.468, payables=72.699, contract_liabilities=195.438,
    notes=152.395, other_debt=1.716, other_liabilities=180.376,
    equity=1721.854, shares=543.574552 + 45.951250)
NOTE_PRINCIPAL = 155.654
CONVERSION_SHARES = NOTE_PRINCIPAL * 195.1029 / 1000
ASSETS = ['cash', 'securities', 'receivables', 'contract_assets', 'inventory',
          'prepaids', 'ppe', 'intangibles', 'other_assets']
LIABILITIES = ['payables', 'contract_liabilities', 'notes', 'other_debt',
               'other_liabilities']


def balance_gap(row):
    return sum(row[k] for k in ASSETS) - sum(row[k] for k in LIABILITIES) - row['equity']


def working_capital(row):
    return (row['receivables'] + row['contract_assets'] + row['inventory']
            + row['prepaids'] - row['payables'] - row['contract_liabilities'])


def check(row, prior=None):
    """Reject inconsistent statements and unfunded cash; never plug equity."""
    gap = balance_gap(row)
    problems = []
    if any(not math.isfinite(v) for v in row.values() if isinstance(v, (int, float))):
        problems.append('non-finite input or output')
    if abs(gap) > 1e-6:
        problems.append('balance sheet does not balance')
    if row['cash'] < MINIMUM_CASH - 1e-6:
        problems.append('cash below floor; no committed revolver assumed')
    if any(row[k] < -1e-6 for k in ASSETS + LIABILITIES) or row['shares'] <= 0:
        problems.append('negative asset/liability or invalid shares')
    if prior:
        expected = {
            'cash': prior['cash'] + row['cfo'] - row['capex'] + row['security_sale'] - row['repayment'],
            'ppe': prior['ppe'] + row['capex'] - row['depreciation'],
            'intangibles': prior['intangibles'] - row['amortization'],
            'equity': prior['equity'] + row['net_income'] + row['conversion'],
            'notes': prior['notes'] - row['conversion'],
            'other_debt': prior['other_debt'] - row['repayment'],
            'shares': prior['shares'] + row['new_shares'],
            'securities': prior['securities'] - row['security_sale'],
        }
        for key, value in expected.items():
            if abs(row[key] - value) > 1e-6:
                problems.append(key + ' roll-forward fails')
    if problems:
        raise ValueError(f"FY{row['year']}: gap {gap:.3f}; " + '; '.join(problems))


def project(break_cash=False, stress_funding=False):
    prior, rows = OPENING.copy(), []
    check(prior)
    for i, year in enumerate(range(2026, 2031)):
        r = dict(year=year)
        r['revenue'] = prior['revenue'] * (1 + GROWTH[i])
        r['gross_profit'] = r['revenue'] * GROSS_MARGIN[i]
        r['cost_of_sales'] = r['revenue'] - r['gross_profit']
        r['sga'], r['rd'] = r['revenue'] * SGA_REVENUE[i], RD[i]
        # D&A is embedded in these reported-style costs, NOT subtracted twice.
        r['depreciation'] = prior['ppe'] * DEPRECIATION_RATE
        r['amortization'] = min(AMORTIZATION[i], prior['intangibles'])
        r['operating_income'] = r['gross_profit'] - r['sga'] - r['rd']
        # Full note conversion at the start of FY2026: noncash financing.
        r['conversion'] = prior['notes'] if i == 0 else 0.0
        r['new_shares'] = CONVERSION_SHARES if i == 0 else 0.0
        r['notes'] = prior['notes'] - r['conversion']
        r['shares'] = prior['shares'] + r['new_shares']
        r['interest'] = prior['other_debt'] * 0.06
        r['pretax'] = r['operating_income'] - r['interest']
        r['tax'] = max(r['pretax'], 0) * TAX_RATE
        r['net_income'] = r['pretax'] - r['tax']
        r['receivables'] = r['revenue'] * AR_RATIO
        r['contract_assets'] = r['revenue'] * CONTRACT_ASSET_RATIO
        r['inventory'] = r['cost_of_sales'] * INVENTORY_DAYS / 365
        r['prepaids'] = r['revenue'] * PREPAID_RATIO
        r['payables'] = r['cost_of_sales'] * PAYABLE_RATIO
        r['contract_liabilities'] = r['revenue'] * CONTRACT_LIABILITY_RATIO
        r['other_assets'], r['other_liabilities'] = prior['other_assets'], prior['other_liabilities']
        r['capex'] = CAPEX[i] + (1000.0 if stress_funding and i == 0 else 0.0)
        r['ppe'] = prior['ppe'] + r['capex'] - r['depreciation']
        r['intangibles'] = prior['intangibles'] - r['amortization']
        r['repayment'] = prior['other_debt'] if i == 0 else 0.0
        r['other_debt'] = prior['other_debt'] - r['repayment']
        r['equity'] = prior['equity'] + r['net_income'] + r['conversion']
        r['change_wc'] = working_capital(r) - working_capital(prior)
        r['change_advances'] = r['contract_liabilities'] - prior['contract_liabilities']
        # Compensation, including future awards, is assumed paid in cash.
        # Therefore no SBC addback and no cost-free dilution assumption.
        r['cfo'] = r['net_income'] + r['depreciation'] + r['amortization'] - r['change_wc']
        r['fcfe'] = r['cfo'] - r['capex'] - r['repayment']
        r['security_sale'] = prior['securities'] if i == 0 else 0.0
        r['securities'] = prior['securities'] - r['security_sale']
        r['opening_cash'] = prior['cash']
        r['cash'] = prior['cash'] + r['fcfe'] + r['security_sale']
        if break_cash and i == 0:
            r['cash'] = prior['cash']
        r['assets'] = sum(r[k] for k in ASSETS)
        r['liabilities_equity'] = sum(r[k] for k in LIABILITIES) + r['equity']
        check(r, prior)
        rows.append(r)
        prior = r
    return rows


def value(rows):
    prior = OPENING
    for r in rows:
        check(r, prior)
        prior = r
    if not COST_OF_EQUITY > TERMINAL_GROWTH >= 0:
        raise ValueError('Require cost of equity > terminal growth >= 0.')
    last = rows[-1]
    # Sustainable terminal year: fixed 2030 operating ratios, no debt,
    # capex covers depreciation, intangible replacement and growing net PP&E.
    terminal_ni = last['operating_income'] * (1 + TERMINAL_GROWTH) * (1 - TAX_RATE)
    terminal_fcfe = terminal_ni - TERMINAL_GROWTH * (last['ppe'] + working_capital(last))
    if last['fcfe'] <= 0 or terminal_fcfe <= 0:
        raise ValueError('No positive sustainable terminal FCFE; extend/rebuild forecast.')
    pv_terminal = terminal_fcfe / (COST_OF_EQUITY - TERMINAL_GROWTH) / (1 + COST_OF_EQUITY) ** 5
    pv_positive = sum(max(r['fcfe'], 0) / (1 + COST_OF_EQUITY) ** t for t, r in enumerate(rows, 1))
    pv_negative = sum(min(r['fcfe'], 0) / (1 + COST_OF_EQUITY) ** t for t, r in enumerate(rows, 1))
    # Course convention requested: only positive forecast FCFE is valued.
    course_value = pv_positive + pv_terminal
    # Separate signed-FCFE bridge: negative years consume existing resources.
    # Cash earns zero in this model, so adding initial excess liquidity does
    # not also capitalize interest income. Do not add ending cash again.
    initial_excess_liquidity = OPENING['cash'] + OPENING['securities'] - MINIMUM_CASH
    funding_adjusted = initial_excess_liquidity + course_value + pv_negative
    return dict(course_value=course_value, course_per_share=course_value / last['shares'],
        funding_adjusted=funding_adjusted, adjusted_per_share=funding_adjusted / last['shares'],
        pv_terminal=pv_terminal, pv_negative=pv_negative, pv_positive=pv_positive,
        terminal_fcfe=terminal_fcfe, shares=last['shares'])


def table(title, rows, fields):
    print('\n' + title + ' (USD millions, except shares)')
    print(f"{'Line':<27}" + ''.join(f"{r['year']:>13}" for r in rows))
    for label, key in fields:
        print(f'{label:<27}' + ''.join(f'{r[key]:>13,.3f}' for r in rows))


def share_comparison(v):
    """Re-express the baseline on one disclosed, as-converted denominator.

    All notes are already removed in the baseline valuation. Add ONLY remaining
    note shares to reported shares (which already contain completed conversions).
    Later cash raised/acquisitions are not in the numerator: no current fair-value
    conclusion can be drawn from this denominator-only comparison.
    """
    if COMPARISON_SHARES <= 0:
        raise ValueError('Invalid comparison share count.')
    return dict(shares=COMPARISON_SHARES,
        course_per_share=v['course_value'] / COMPARISON_SHARES,
        adjusted_per_share=v['funding_adjusted'] / COMPARISON_SHARES,
        market_equivalent=MARKET_PRICE * COMPARISON_SHARES)


def main():
    rows = project('--break-cash' in sys.argv, '--stress-funding' in sys.argv)
    table('INCOME STATEMENT', rows, [(k.replace('_', ' ').title(), k) for k in
        ['revenue', 'cost_of_sales', 'gross_profit', 'sga', 'rd', 'operating_income', 'interest', 'pretax', 'tax', 'net_income']])
    table('BALANCE SHEET', rows, [(k.replace('_', ' ').title(), k) for k in
        ASSETS + ['assets'] + LIABILITIES + ['equity', 'liabilities_equity', 'shares']])
    table('CASH FLOW', rows, [(label, key) for label, key in [
        ('Net income','net_income'), ('+ Depreciation','depreciation'), ('+ Amortization','amortization'),
        ('- Change in net WC','change_wc'), ('Operating cash flow','cfo'), ('- Capex','capex'),
        ('- Debt repayment','repayment'), ('FCFE (signed)','fcfe'), ('+ Securities sold','security_sale'),
        ('Opening cash','opening_cash'), ('Ending cash','cash'), ('Noncash debt conversion','conversion')]])
    print('\nCHECKS: no revolver and no new cash equity financing assumed.')
    for r in rows:
        print(f"FY{r['year']}: gap 0.000; cash >= {MINIMUM_CASH:.0f}; roll-forwards PASS"
              + ('; NEGATIVE FCFE' if r['fcfe'] < 0 else '; positive FCFE'))
    v = value(rows)
    print(f"\nLab positive-FCFE convention: ${v['course_per_share']:.2f} per share")
    print(f"PV of positive FCFE: ${v['pv_positive']:.3f} million")
    print(f"PV of negative FCFE (excluded ONLY in lab convention): ${v['pv_negative']:.3f} million")
    print(f"Sustainable FY2031 FCFE: ${v['terminal_fcfe']:.3f} million")
    print(f"PV of terminal value: ${v['pv_terminal']:.3f} million")
    print(f"Terminal share of lab value: {100*v['pv_terminal']/v['course_value']:.2f}%")
    print(f"Funding-adjusted signed-FCFE + initial excess liquidity: ${v['adjusted_per_share']:.2f} per share")
    print(f"Scenario common-equivalent shares: {v['shares']:.6f} million")
    print(f"Market quote: ${MARKET_PRICE:.2f}; {MARKET_TIMESTAMP}.")
    comparison = share_comparison(v)
    print('\nSAME-SHARE-BASIS COMPARISON (denominator adjustment only)')
    print(f"June 30 disclosed shares, with remaining notes converted: {comparison['shares']:.6f} million")
    print(f"Baseline lab value on this basis: ${comparison['course_per_share']:.2f} per share")
    print(f"Baseline funding-adjusted value on this basis: ${comparison['adjusted_per_share']:.2f} per share")
    print(f"Market-equivalent total on the SAME basis: ${comparison['market_equivalent']:.3f} million")
    print('Not actual basic market capitalization; not a fully diluted option valuation.')
    print('The annual baseline is not a fully updated September 2026 valuation; see notes.')


if __name__ == '__main__':
    main()
