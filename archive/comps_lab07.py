"""Lab 07: frozen Asbury P/E comparison; standard library only."""

from math import isfinite
from statistics import median

# Editable inputs: USD/share; Dec. 31, 2024 prices and FY2024 total GAAP
# diluted EPS released afterward. This is a retrospective training case.
TARGET = {"ticker": "ABG", "price": 243.03, "eps": 21.50}
PEERS = [
    {"ticker": "AN", "price": 169.84, "eps": 16.92},
    {"ticker": "GPI", "price": 421.48, "eps": 36.81},
]


def positive_number(value):
    return (isinstance(value, (int, float)) and not isinstance(value, bool)
            and isfinite(value) and value > 0)


def ticker(company):
    return str(company.get("ticker") or "").strip().upper()


def analyze(target, peers):
    target_symbol = ticker(target)
    target_eps = target.get("eps")
    target_price = target.get("price")
    print("ASBURY CASE: retrospective FY2024 comparison")
    print("Prices and EPS in USD/share; full precision retained until display.")
    if positive_number(target_price) and positive_number(target_eps):
        print(f"{target_symbol} observed P/E (not a peer): "
              f"{target_price / target_eps:.6f}x")
    else:
        print("Target observed P/E: not meaningful (invalid price or EPS).")

    valid = []
    seen = set()
    for peer in peers:
        symbol = ticker(peer)
        if not symbol:
            print("Peer excluded: missing ticker.")
            continue
        if symbol == target_symbol:
            print(f"{symbol} excluded: target cannot be its own peer.")
            continue
        if symbol in seen:
            print(f"{symbol} excluded: duplicate ticker (first entry retained).")
            continue
        seen.add(symbol)
        price, eps = peer.get("price"), peer.get("eps")
        if not positive_number(price) or not positive_number(eps):
            print(f"{symbol} P/E: not meaningful (invalid price or EPS).")
            continue
        multiple = price / eps
        valid.append((symbol, multiple))
        print(f"{symbol} P/E: {multiple:.6f}x")

    if not valid:
        print("No usable peers; no estimate.")
        return
    multiples = [value for _, value in valid]
    midpoint = median(multiples)
    print(f"Peer median P/E: {midpoint:.6f}x")
    if not positive_number(target_eps):
        print("Target implied prices: not meaningful (invalid target EPS).")
        for symbol, _ in valid:
            print(f"Remove {symbol}: no estimate.")
        return

    full_estimate = midpoint * target_eps
    if len(valid) == 1:
        print(f"One-peer reference estimate: ${full_estimate:.2f}; no range.")
    else:
        print(f"Peer-implied range: ${min(multiples) * target_eps:.2f}"
              f" to ${max(multiples) * target_eps:.2f}")
        print(f"At peer median: ${full_estimate:.2f}")
    print("Leave-one-peer-out checks:")
    for symbol, _ in valid:
        remaining = [value for name, value in valid if name != symbol]
        if not remaining:
            print(f"Remove {symbol}: no usable peers; no estimate.")
        else:
            estimate = median(remaining) * target_eps
            label = "one-peer reference; no range" if len(remaining) == 1 else "median estimate"
            print(f"Remove {symbol}: ${estimate:.2f}; "
                  f"change ${estimate - full_estimate:+.2f} ({label}).")
    print("P/E implies an equity price directly: no cash/debt adjustment.")


if __name__ == "__main__":
    analyze(TARGET, PEERS)
