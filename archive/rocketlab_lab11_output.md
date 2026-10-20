# Rocket Lab Lab 11 — visible sensitivity output

Generated UTC: 2026-09-29T18:17:06.845418+00:00

Dollar amounts are USD millions except value per share. Paths are FY2026–FY2030.
Value uses Lab 10 funding-adjusted signed FCFE plus initial excess liquidity.
Annual-baseline classroom scenario; not an updated market valuation.

## Inputs, results and changes from the original base

| Driver / case | Actual input path (units shown) | Operating profit | Change | FCFE | Change | Value/share | Change | Checks |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Revenue growth / Lower | 35, 30, 25, 20, 15 % | 161.905 | -106.936 | 18.454 | -65.502 | 1.338 | -0.664 | PASS all 5 years |
| Revenue growth / Base | 40, 35, 30, 25, 20 % | 268.841 | +0.000 | 83.956 | +0.000 | 2.002 | +0.000 | PASS all 5 years |
| Revenue growth / Higher | 45, 40, 35, 30, 25 % | 393.600 | +124.759 | 158.922 | +74.966 | 2.760 | +0.758 | PASS all 5 years |
| R&D expense / Lower | 232, 240, 248, 256, 264 USD million | 334.841 | +66.000 | 133.456 | +49.500 | 2.631 | +0.629 | PASS all 5 years |
| R&D expense / Base | 290, 300, 310, 320, 330 USD million | 268.841 | +0.000 | 83.956 | +0.000 | 2.002 | +0.000 | PASS all 5 years |
| R&D expense / Higher | 348, 360, 372, 384, 396 USD million | 202.841 | -66.000 | 34.456 | -49.500 | 1.357 | -0.645 | PASS all 5 years |

## Output spans: maximum minus minimum

| Output | Revenue-growth span | R&D-expense span | Larger driver over these ranges |
|---|---:|---:|---|
| FY2030 operating profit ($m) | 231.694 (3/3 valid) | 132.000 (3/3 valid) | Revenue growth |
| FY2030 FCFE ($m) | 140.468 (3/3 valid) | 99.000 (3/3 valid) | Revenue growth |
| Signed-FCFE value ($/share) | 1.423 (3/3 valid) | 1.274 (3/3 valid) | Revenue growth |

## Accounting and isolation evidence

Every run starts from a deep independent copy of all base inputs.
Only the named driver differs; this is asserted before running the linked model.
Each valid year passes the original balance-sheet, liquidity and roll-forward checks.
Restored base inputs, all five statement rows, checks and valuations: EXACT MATCH.
Comparison tolerance for base restoration: zero (unrounded Python values).
Accounting-check tolerance: 0.000001 USD million.
Original Lab 10 source SHA256 unchanged: 42e7e33f9e030c525bd405e85d153a65614db8a9d29c691daa84c83bc33fccfd

| Run | Maximum absolute balance gap ($m) | Minimum cash ($m) |
|---|---:|---:|
| Revenue growth / Lower | 0.000000000001 | 370.306 |
| Revenue growth / Base | 0.000000000000 | 439.256 |
| Revenue growth / Higher | 0.000000000000 | 472.470 |
| R&D expense / Lower | 0.000000000000 | 613.016 |
| R&D expense / Base | 0.000000000000 | 439.256 |
| R&D expense / Higher | 0.000000000000 | 211.383 |

## Selected trace: higher R&D versus base, FY2030

| Line ($m) | Base | Higher R&D | Change |
|---|---:|---:|---:|
| revenue | 2217.930 | 2217.930 | +0.000 |
| gross_profit | 953.710 | 953.710 | +0.000 |
| cost_of_sales | 1264.220 | 1264.220 | +0.000 |
| sga | 354.869 | 354.869 | +0.000 |
| rd | 330.000 | 396.000 | +66.000 |
| operating_income | 268.841 | 202.841 | -66.000 |
| tax | 67.210 | 50.710 | -16.500 |
| net_income | 201.631 | 152.131 | -49.500 |
| inventory | 507.481 | 507.481 | +0.000 |
| payables | 232.903 | 232.903 | +0.000 |
| change_wc | 38.753 | 38.753 | +0.000 |
| depreciation | 99.388 | 99.388 | +0.000 |
| amortization | 21.690 | 21.690 | +0.000 |
| cfo | 283.956 | 234.456 | -49.500 |
| capex | 200.000 | 200.000 | +0.000 |
| fcfe | 83.956 | 34.456 | -49.500 |
