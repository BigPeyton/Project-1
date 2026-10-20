"""Lab 08: sourced FY2025 P/E limitation for Rocket Lab; standard library only.

Run: python rocketlab_lab08.py
Sources, qualifications and draft judgments: rocketlab_lab08.md.
Prices are September 10, 2026 closes, in each issuer's local currency.
"""

from datetime import date
from math import isfinite
from statistics import median

COMPARISON_DATE = "2026-09-10"
TARGET = dict(ticker="RKLB", price=61.96, eps=-0.37, currency="USD",
              price_date=COMPARISON_DATE, published="2026-02-26")
PEERS = [
    dict(ticker="RDW", price=10.87, eps=-2.28, currency="USD",
         price_date=COMPARISON_DATE, published="2026-02-25", decision="qualify"),
    dict(ticker="AVIO", price=28.01, eps=0.34, currency="EUR",
         price_date=COMPARISON_DATE, published="2026-03-31", decision="qualify"),
]


def positive(value):
    return (isinstance(value, (int, float)) and not isinstance(value, bool)
            and isfinite(value) and value > 0)


def analyze(target, peers):
    """Return usable peer multiples and a range only for positive target EPS.

    Each price and EPS pair must already use the same local currency and share
    unit. Cross-company currency conversion is unnecessary for dimensionless P/E.
    Numeric eligibility does not remove the documented economic qualifications.
    """
    cutoff = date.fromisoformat(COMPARISON_DATE)
    seen = {target["ticker"]}
    for company in [target, *peers]:
        if company["price_date"] != COMPARISON_DATE:
            raise ValueError("All prices must use the comparison date.")
        if date.fromisoformat(company["published"]) > cutoff:
            raise ValueError("Earnings must be public by the comparison date.")
    multiples = {}
    for peer in peers:
        symbol = peer["ticker"]
        if symbol in seen:
            raise ValueError("Duplicate peer or target included as its own peer.")
        seen.add(symbol)
        if (peer["decision"] in ("use", "qualify")
                and positive(peer["price"]) and positive(peer["eps"])):
            multiples[symbol] = peer["price"] / peer["eps"]
    implied = None
    if positive(target["eps"]) and multiples:
        values = list(multiples.values())
        implied = (min(values) * target["eps"],
                   median(values) * target["eps"],
                   max(values) * target["eps"])
    return multiples, implied


def main():
    print("ROCKET LAB LAB 08 - September 10, 2026 comparison")
    print("FY2025 reported diluted EPS; all fiscal year-ends December 31, 2025.")
    print("Draft AI-assisted peer decisions; see rocketlab_lab08.md.")
    for company in [TARGET, *PEERS]:
        print(f"{company['ticker']}: close {company['currency']} {company['price']:.2f}; "
              f"annual diluted EPS {company['eps']:.2f}; public by {company['published']}")
    multiples, implied = analyze(TARGET, PEERS)
    for peer in PEERS:
        symbol = peer["ticker"]
        if symbol in multiples:
            print(f"{symbol} P/E: {multiples[symbol]:.8f}x (qualified, descriptive only).")
        else:
            print(f"{symbol}: no usable positive P/E; annual EPS is nonpositive.")
    if implied is None:
        print("RKLB peer-implied price: NOT MEANINGFUL; target EPS is negative.")
        print("No peer-derived fair-value range. Do not turn a negative product into a price.")
    else:
        label = "Single-peer reference (not a range)" if len(multiples) == 1 else "Range / median"
        print(f"{label}: {implied}")
    print("Leave-one-peer-out checks:")
    for peer in PEERS:
        remaining = [p for p in PEERS if p["ticker"] != peer["ticker"]]
        kept, result = analyze(TARGET, remaining)
        description = "no target estimate" if result is None else str(result)
        print(f"Remove {peer['ticker']}: {len(kept)} usable peer multiple(s); {description}.")
    print("Avio qualifications: capital raise, business mix, IFRS versus US GAAP.")
    print("Conclusion: watch/defer; DCF remains illustrative; do not average methods.")


if __name__ == "__main__":
    main()
