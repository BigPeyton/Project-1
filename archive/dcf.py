"""Labs 05/06: training validation and illustrative Rocket Lab DCF.

All monetary inputs are in USD millions, except the resulting value per share.
"""

import math

# Editable inputs
STARTING_FCFF = 100.0
GROWTH_RATES = [0.08, 0.06, 0.05, 0.04, 0.03]
WACC = 0.10
TERMINAL_GROWTH = 0.03
NON_OPERATING_CASH = 50.0
DEBT = 300.0
DILUTED_SHARES = 50.0

# Training controls: decimal shifts (0.01 means one percentage point).
WACC_VALUES = [0.09, 0.10, 0.11]
TERMINAL_GROWTH_VALUES = [0.02, 0.03, 0.04]
TARGET_PRICE = 30.00
LOWER_SHIFT = -0.05
UPPER_SHIFT = 0.10

# Rocket Lab classroom estimates; sources and limitations: rocketlab_lab06.md.
COMPANY_REVENUE_BASE = 601.799
COMPANY_REVENUE_GROWTH = [0.30, 0.30, 0.25, 0.20, 0.15]
COMPANY_FCFF_MARGINS = [-0.40, -0.20, -0.05, 0.05, 0.10]
COMPANY_WACC = 0.18
COMPANY_TERMINAL_GROWTH = 0.03
COMPANY_CASH = 1098.824
COMPANY_DEBT = 154.111  # Provisional book debt; excludes leases.
COMPANY_SHARES = 530.664781  # Historical EPS denominator, millions.
COMPANY_WACC_VALUES = [0.16, 0.18, 0.20]
COMPANY_G_VALUES = [0.02, 0.03, 0.04]
COMPANY_TARGET_PRICE = 61.96  # Sep 10, 2026, 4 PM EDT close.
COMPANY_LOWER_SHIFT = -0.05
COMPANY_UPPER_SHIFT = 0.10  # Uniform FCFF-margin shift, not growth shift.


def project(start, rates):
    if len(rates) != 5 or any(not math.isfinite(g) or g <= -1 for g in rates):
        raise ValueError("Provide five finite growth rates above -100%.")
    values = []
    for rate in rates:
        start *= 1 + rate
        values.append(start)
    return values


def value(path, wacc, growth, cash, debt, shares):
    if len(path) != 5 or not all(math.isfinite(x) for x in [*path, wacc, growth, cash, debt, shares]):
        raise ValueError("Provide five cash flows and finite inputs.")
    if shares <= 0 or wacc <= -1 or growth <= -1 or growth >= wacc:
        raise ValueError("Require positive shares and -100% < terminal growth < WACC.")
    if path[-1] <= 0:
        raise ValueError("Terminal FCFF must be positive for this going-concern scenario.")
    explicit = sum(cf / (1 + wacc) ** year for year, cf in enumerate(path, 1))
    terminal = path[-1] * (1 + growth) / (wacc - growth)
    pv_terminal = terminal / (1 + wacc) ** 5
    ev = explicit + pv_terminal
    equity = ev + cash - debt
    return explicit, terminal, pv_terminal, ev, equity, equity / shares


def print_values(path, result):
    for year, cf in enumerate(path, 1):
        print(f"FCFF Year {year}: {cf:.4f}")
    labels = ["Present value of explicit FCFF", "Terminal value at Year 5",
              "Present value of terminal value", "Enterprise value", "Equity value",
              "Value per diluted share"]
    for label, number in zip(labels, result):
        print(f"{label}: {number:.4f}")
    ratio = f"{result[2] / result[3]:.4f}" if result[3] != 0 else "undefined (zero EV)"
    print(f"Present value of terminal value as a share of enterprise value: {ratio}")


def print_grid(path, waccs, growths, cash, debt, shares):
    print("\nSensitivity: value per diluted share (USD)")
    print("WACC / g " + "".join(f"{g:>12.1%}" for g in growths))
    prices = []
    for w in waccs:
        cells = []
        for g in growths:
            try:
                price = value(path, w, g, cash, debt, shares)[-1]
                prices.append(price)
                cells.append(f"{price:12.2f}")
            except ValueError:
                cells.append(f"{'invalid':>12}")
        print(f"{w:8.1%} " + "".join(cells))
    if prices:
        print(f"Grid range: ${min(prices):.2f} to ${max(prices):.2f}")


def bisect_price(price_function, target, lower, upper):
    if not all(math.isfinite(x) for x in [target, lower, upper]) or lower >= upper:
        raise ValueError("Require finite target and lower < upper.")
    low_error = price_function(lower) - target
    high_error = price_function(upper) - target
    if abs(low_error) <= 1e-8:
        return lower
    if abs(high_error) <= 1e-8:
        return upper
    if low_error * high_error > 0:
        return None
    for _ in range(200):
        middle = (lower + upper) / 2
        error = price_function(middle) - target
        if abs(error) <= 1e-8:
            return middle
        if low_error * error <= 0:
            upper = middle
        else:
            lower, low_error = middle, error
    raise ValueError("Bisection did not converge to the price tolerance.")


def print_reverse(price_function, target, lower, upper, variable, fixed):
    print(f"\nReverse DCF: {variable}")
    print(f"Target: ${target:.2f}; shift bracket: {lower * 100:+.2f} to {upper * 100:+.2f} percentage points")
    print(f"Held fixed: {fixed}")
    try:
        solution = bisect_price(price_function, target, lower, upper)
        if solution is None:
            print("No solution in that bracket.")
            print(f"Endpoint prices: ${price_function(lower):.4f}, ${price_function(upper):.4f}")
        else:
            print(f"Solved shift: {solution * 100:+.4f} percentage points")
            print(f"Repriced value: ${price_function(solution):.8f}")
    except ValueError as error:
        print(f"Invalid reverse DCF: {error}")


def extensions():
    training = project(STARTING_FCFF, GROWTH_RATES)
    print_grid(training, WACC_VALUES, TERMINAL_GROWTH_VALUES,
               NON_OPERATING_CASH, DEBT, DILUTED_SHARES)
    fixed = f"FCFF {STARTING_FCFF}; WACC {WACC}; terminal growth {TERMINAL_GROWTH}; cash {NON_OPERATING_CASH}; debt {DEBT}; shares {DILUTED_SHARES}"
    if any(g + bound <= -1 for g in GROWTH_RATES for bound in [LOWER_SHIFT, UPPER_SHIFT]):
        print("Invalid reverse DCF bracket: annual growth reaches -100% or below.")
    else:
        print_reverse(lambda shift: value(project(STARTING_FCFF, [g + shift for g in GROWTH_RATES]),
                      WACC, TERMINAL_GROWTH, NON_OPERATING_CASH, DEBT, DILUTED_SHARES)[-1],
                      TARGET_PRICE, LOWER_SHIFT, UPPER_SHIFT, "uniform explicit growth-rate shift", fixed)

    print("\nROCKET LAB -- illustrative estimates; provisional cash/debt/share treatment")
    print("Nominal USD millions; FY2025 base, five annual periods. See rocketlab_lab06.md.")
    revenues = project(COMPANY_REVENUE_BASE, COMPANY_REVENUE_GROWTH)
    if len(COMPANY_FCFF_MARGINS) != 5:
        raise ValueError("Provide five FCFF margins.")
    path = [r * m for r, m in zip(revenues, COMPANY_FCFF_MARGINS)]
    result = value(path, COMPANY_WACC, COMPANY_TERMINAL_GROWTH,
                   COMPANY_CASH, COMPANY_DEBT, COMPANY_SHARES)
    print_values(path, result)
    print_grid(path, COMPANY_WACC_VALUES, COMPANY_G_VALUES,
               COMPANY_CASH, COMPANY_DEBT, COMPANY_SHARES)
    fixed = (f"revenues {revenues}; baseline margins {COMPANY_FCFF_MARGINS}; "
             f"WACC {COMPANY_WACC}; terminal growth {COMPANY_TERMINAL_GROWTH}; "
             f"cash {COMPANY_CASH}; debt {COMPANY_DEBT}; shares {COMPANY_SHARES}")
    print_reverse(lambda shift: value([r * (m + shift) for r, m in zip(revenues, COMPANY_FCFF_MARGINS)],
                  COMPANY_WACC, COMPANY_TERMINAL_GROWTH, COMPANY_CASH, COMPANY_DEBT, COMPANY_SHARES)[-1],
                  COMPANY_TARGET_PRICE, COMPANY_LOWER_SHIFT, COMPANY_UPPER_SHIFT,
                  "uniform FCFF-margin shift (includes Year 5 terminal base)", fixed)
    print("A price-consistent scenario is not proof of mispricing.")
    if COMPANY_TARGET_PRICE > 0:
        ratio = result[-1] / COMPANY_TARGET_PRICE
        print(f"\nValue / market price: {ratio:.4f}x; "
              f"{'inside' if 0.5 <= ratio <= 2 else 'outside'} the 0.5x-2x band.")
    print("Most distrusted assumption: FCFF-margin improvement; the profitability date is unverified.")


def main() -> None:
    if TERMINAL_GROWTH >= WACC:
        print("Error: terminal growth must be less than WACC.")
        return

    if len(GROWTH_RATES) != 5:
        print("Error: provide exactly five yearly growth rates.")
        return

    fcff_values = []
    fcff = STARTING_FCFF
    for growth_rate in GROWTH_RATES:
        fcff *= 1 + growth_rate
        fcff_values.append(fcff)

    pv_explicit_fcff = sum(
        yearly_fcff / (1 + WACC) ** year
        for year, yearly_fcff in enumerate(fcff_values, start=1)
    )
    terminal_value_year_5 = fcff_values[-1] * (1 + TERMINAL_GROWTH) / (
        WACC - TERMINAL_GROWTH
    )
    pv_terminal_value = terminal_value_year_5 / (1 + WACC) ** 5
    enterprise_value = pv_explicit_fcff + pv_terminal_value
    equity_value = enterprise_value + NON_OPERATING_CASH - DEBT
    value_per_share = equity_value / DILUTED_SHARES
    pv_terminal_share = pv_terminal_value / enterprise_value

    for year, yearly_fcff in enumerate(fcff_values, start=1):
        print(f"FCFF Year {year}: {yearly_fcff:.4f}")
    print(f"Present value of explicit FCFF: {pv_explicit_fcff:.4f}")
    print(f"Terminal value at Year 5: {terminal_value_year_5:.4f}")
    print(f"Present value of terminal value: {pv_terminal_value:.4f}")
    print(f"Enterprise value: {enterprise_value:.4f}")
    print(f"Equity value: {equity_value:.4f}")
    print(f"Value per diluted share: {value_per_share:.4f}")
    print(
        "Present value of terminal value as a share of enterprise value: "
        f"{pv_terminal_share:.4f}"
    )


if __name__ == "__main__":
    main()
    try:
        extensions()
    except ValueError as error:
        print(f"Error: {error}")
