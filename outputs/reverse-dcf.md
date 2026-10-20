# Market-implied expectations and long-term challenges

Information cutoff: 2026-09-10T16:00:00-04:00. Historical target price: $61.96.
Price source: https://stockanalysis.com/stocks/rklb/history/ (September 10 row only).

Standalone, fixed converted/full-exercise bridge; no pending Iridium, optional forward/ATM/capped-call proceeds or customer-loan recovery.

These are AI-assisted development calculations, not the student AI-off locked exercise. Each test holds other assumptions fixed; no probability or unique market forecast is inferred.

## base

Reference modeled price: $2.9853.

**Reverse WACC:** 3.6831%, reproducing $61.9600; prior-day Treasury reference 4.83%. The root is below Treasury. This is a mathematical diagnostic, not a recommended required return. Monotonicity was sampled over the declared interval and the root checked by repricing; no global claim is made.

**Reverse mature margin:** not bracketed within declared bounds.
The 4%-80% margin interval produces $2.3251-$10.1724. The entire margin/capital-efficiency transition changes together. The 80% bound is an extreme diagnostic, not an economically supported case.

**Residual terminal requirement (explicit cash flows held fixed):**

- Required operating EV: 38,522.859 million USD.
- Required 2041 FCFF: 42,489.371 million versus modeled 440.768 million (96.4x).
- At fixed 2041 sales of 6,027.595 million, implied EBIT margin is 1156.8%.

This isolated terminal jump violates continuity with the unchanged explicit path. It identifies the missing economic burden; it is not an admissible replacement forecast. A margin above 100% cannot be supported by ordinary operating sales under this model.

| One-at-a-time challenge | Old | New | USD/share or failure |
|---|---:|---:|---|
| lower mature margin | 12% | 8% | 2.6261 |
| lower incremental ROIC | 16% | 10% | 2.7978 |

| WACC (g held at 3%) | USD/share |
|---|---:|
| 14% | 3.3582 |
| 16% | 2.9853 |
| 18% | 2.7498 |
| 20% | 2.5976 |

## upside

Reference modeled price: $6.7259.

**Reverse WACC:** 5.0375%, reproducing $61.9600; prior-day Treasury reference 4.83%. The root is only slightly above Treasury. This is a mathematical diagnostic, not a recommended required return. Monotonicity was sampled over the declared interval and the root checked by repricing; no global claim is made.

**Reverse mature margin:** not bracketed within declared bounds.
The 4%-80% margin interval produces $4.1337-$18.4432. The entire margin/capital-efficiency transition changes together. The 80% bound is an extreme diagnostic, not an economically supported case.

**Residual terminal requirement (explicit cash flows held fixed):**

- Required operating EV: 38,494.060 million USD.
- Required 2041 FCFF: 40,815.326 million versus modeled 1,433.750 million (28.5x).
- At fixed 2041 sales of 11,245.099 million, implied EBIT margin is 569.4%.

This isolated terminal jump violates continuity with the unchanged explicit path. It identifies the missing economic burden; it is not an admissible replacement forecast. A margin above 100% cannot be supported by ordinary operating sales under this model.

| One-at-a-time challenge | Old | New | USD/share or failure |
|---|---:|---:|---|
| lower mature margin | 20% | 8% | 4.6673 |
| lower incremental ROIC | 20% | 10% | 6.0700 |

| WACC (g held at 3%) | USD/share |
|---|---:|
| 14% | 8.1853 |
| 16% | 6.7259 |
| 18% | 5.7395 |
| 20% | 5.0461 |

## Decision implication

The current standalone revenue, profitability and reinvestment paths do not underwrite the cutoff quote. A substantially different operating path, transaction economics or other omitted value would need independent support. This is not proof that every possible Rocket Lab strategy is worth less than the price. Lower margin/return stresses challenge the working valuation but do not change the proposed no-initiation decision at $61.96. See docs/committee-decision.md for the provisional committee action and triggers.
