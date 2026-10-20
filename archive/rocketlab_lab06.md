# Lab 06: Rocket Lab (RKLB)

Work date: September 10, 2026

Status: `dcf.py` prints the validated training case and the illustrative company valuation, sensitivity grid, and reverse-DCF bracket result. A draft conditional recommendation is included below. Company assumptions remain provisional.

## Source

[Rocket Lab Corporation, 2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1819994/000181999426000013/rklb-20251231.htm), fiscal year ended December 31, 2025.

Monetary model inputs will use USD millions; shares will use millions; prices will use USD per share. The cash flow statement reports USD thousands, so the figures below are divided by 1,000.

## Input table

| Input | Value | Unit | Period / as-of date | Exact source locator or assumption status |
|---|---|---|---|---|
| Operating cash flow | -165.521 | USD millions | Year ended December 31, 2025 | 2025 Form 10-K, Consolidated Statements of Cash Flows, F-8, 2025 column, “Net cash used in operating activities”: (165,521) thousand |
| Capital expenditures (positive amount to subtract) | 156.285 | USD millions | Year ended December 31, 2025 | Same statement, F-8, 2025 column, “Purchases of property, equipment and software”: (156,285) thousand |
| Cash interest paid | 24.548 | USD millions | Year ended December 31, 2025 | Consolidated Statements of Cash Flows (Continued), F-9, 2025 column, “Cash paid for interest”: 24,548 thousand |
| Tax rate for the interest adjustment | unresolved | Percent | unresolved | A justified modeling assumption is still needed; no rate has been selected |
| Starting FCFF | unresolved; formula below | USD millions | Year ended December 31, 2025 | Derived from the three sourced cash flow figures and the unresolved tax assumption |
| Explicit FCFF forecast, Years 1–5 | -312.935480, -203.408062, -63.565019, 76.278023, 175.439453; illustrative estimate | USD millions per year | Forecast years 2026–2030, using FY2025 as the historical base | Draft scenario derived below from assumed revenue growth and FCFF margins; not company guidance or a validated forecast |
| WACC | 18%; provisional classroom estimate | Percent per year | Prepared September 10, 2026; mixed input dates disclosed below | CAPM cost of equity 18%; simplified weighted calculation about 17.94%, rounded to 18%. Debt market value and convertible treatment remain unresolved |
| Terminal growth | 3%; analyst estimate | Nominal percent per year | 2031 onward; selected September 10, 2026 | June 17, 2026 FOMC projections, Table 1, longer-run real GDP and PCE inflation medians; rationale below. 3% < 18% WACC |
| Non-operating cash | 1098.824; estimate of available non-operating assets | USD millions | December 31, 2025 | F-5 balance sheet: cash 828.660 + current securities 187.917 + non-current securities 82.247; excludes restricted cash 4.885 |
| Debt | 154.111; book-value proxy, excluding leases | USD millions | December 31, 2025 | F-5: net convertible notes 152.395 + other net borrowings 1.716; current borrowings zero. Note 12, F-30: convertible principal 155.654 less issuance costs/discount 3.259 reconciles to 152.395 |
| Diluted weighted-average shares | 530.664781 | Millions of shares | Year ended December 31, 2025 | Note 19, F-43, EPS denominator: 530,664,781 actual shares. Basic equals diluted because potential additional shares are antidilutive in a loss year |
| Target market price | 61.96 | USD per share | September 10, 2026, 4:00 PM EDT close | [Stock Analysis RKLB statistics](https://stockanalysis.com/stocks/rklb/statistics/), quote header; use regular-session close, not after-hours price |

## Cash, debt, and share modeling choices

The cash input assumes all unrestricted cash and securities are non-operating. This is an estimate: no minimum operating-cash reserve has been deducted. A required reserve would reduce the cash addition.

Debt uses a simplified book-value proxy, not market value or gross principal. Lease liabilities are excluded under this provisional convention; revisit lease treatment for consistency with the forecast. Convertible debt is treated as debt, without also adding conversion shares. The historical EPS denominator follows the lab requirement; it is not a current fully diluted capitalization estimate.

These choices are provisional modeling assumptions, not additional facts reported by the company. The computed company valuation is an illustrative scenario subject to these limitations.

## Starting FCFF calculation

Using the lab's formula, with `t` representing the tax rate for the interest adjustment:

```text
FCFF = operating cash flow + cash interest paid × (1 − t) − capex
     = -165.521 + 24.548 × (1 − t) − 156.285
     = -297.258 − 24.548 × t  (USD millions)
```

At a hypothetical 0% tax rate, this equals -297.258 million. This is a diagnostic calculation, not a selected tax assumption or finalized input. FCFF remains negative for tax rates from 0% through 100%.

Positive percentage growth applied to negative FCFF makes the cash outflow larger. The model therefore uses the explicit five-year FCFF scenario below rather than compounding historical negative FCFF.

## Five-year FCFF scenario — illustrative estimate

Prepared September 10, 2026, using the supplied 2025 annual report only. This is a draft classroom scenario, not a forecast incorporating all information available today. Later quarterly filings and guidance have not yet been incorporated.

### Historical evidence

Revenue was $244.592 million in 2023, $436.214 million in 2024, and $601.799 million in 2025 (F-6, revenue total). Operating cash flow remained negative in all three years (F-8). Item 7, Liquidity and Capital Resources, page 51, anticipates significantly higher capital and operating expenditures. Growth alone therefore does not establish cash-flow profitability. Source: the linked 2025 Form 10-K.

### Assumptions and calculation

Use revenue multiplied by an assumed FCFF margin to make each forecast amount traceable. FCFF margin means unlevered cash flow after operating taxes, capital expenditure and working-capital investment, divided by revenue. It is not an operating-profit margin. These assumed margins summarize those components; a detailed operating forecast has not yet been built.

All percentages below are analyst-selected classroom estimates. The filing supports the historical starting point and investment risks, not these specific percentages or the assumed profitability date.

| Year | Assumed revenue growth | Forecast revenue, USD millions | Assumed FCFF margin | Forecast FCFF, USD millions |
|---|---:|---:|---:|---:|
| 2026 | 30% | 782.338700 | -40% | -312.935480 |
| 2027 | 30% | 1017.040310 | -20% | -203.408062 |
| 2028 | 25% | 1271.300388 | -5% | -63.565019 |
| 2029 | 20% | 1525.560465 | 5% | 76.278023 |
| 2030 | 15% | 1754.394535 | 10% | 175.439453 |

```text
Revenue(year) = Revenue(previous year) * (1 + assumed revenue growth)
FCFF(year) = Revenue(year) * assumed FCFF margin
Example 2026: 601.799 * 1.30 * (-0.40) = -312.935480 million
```

Calculations retain full precision internally; displayed values are rounded to six decimal places. Extra decimal places support reproducibility, not forecast certainty.

The scenario assumes continued sales expansion with declining percentage growth. Cash burn initially remains substantial; subsequent margin improvement assumes better operating efficiency and lower reinvestment needs relative to revenue. Positive FCFF in 2029 and a 10% FCFF margin in 2030 are hypotheses to challenge, not conclusions established by the filing. No launch date or project success is treated as certain.

The least-supported driver is the margin improvement. A useful downside check is to delay that improvement by a year. Before relying on a perpetual terminal value, assess whether the final year's cash flow represents sustainable operations and adequate reinvestment; the five-year horizon may be too short for this company.

The unresolved historical interest tax adjustment does not enter this direct forecast: future cash taxes are embedded in the assumed FCFF margins. The WACC estimate, terminal-growth assumption, and timestamped target price are documented separately in this file.

### Additional debt limitation identified during review

Note 6, F-26 reports convertible-note fair value of $2185.440 million versus carrying value of $152.395 million at December 31, 2025. This makes the existing book-debt proxy a material simplification. Resolve convertible valuation and dilution consistently before treating the final equity valuation as decision-ready; do not both subtract the full convertible claim and count the same conversion shares.

## WACC estimate

Selected working discount rate: **18% annually**, an estimate for the classroom scenario. This is not a fully resolved current market-value WACC.

| Component | Working input | Source / status / date |
|---|---:|---|
| Risk-free rate | 4.95% | [U.S. Treasury daily par yields](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value_month=202609&type=daily_treasury_yield_curve), September 10, 2026 row, 10 Yr column |
| Equity beta | 2.61 | [Stock Analysis](https://stockanalysis.com/stocks/rklb/statistics/), Stock Price Statistics, Beta (5Y), retrieved September 10, 2026; exact regression endpoint/frequency not established |
| Equity risk premium | 5% | Lab 06 classroom assumption; not a measured current market premium |
| Equity market value E | 37080 million USD | Stock Analysis, Total Valuation, market capitalization 37.08B on the retrieved September 10 page; vendor-rounded value |
| Debt weighting proxy D | 157.370 million USD | December 31, 2025 proxy: Note 12 convertible principal 155.654 + F-5 other net borrowings 1.716; excludes leases; not current debt market value |
| Pretax borrowing-cost proxy | 4.25% | Note 12, F-30, convertible coupon as of December 31, 2025; classroom debt-note-rate shortcut, not a current refinancing yield |
| Immediate interest tax shield | 0% | Modeling estimate: assume no immediately usable marginal shield during losses. Not the statutory tax rate or a permanent tax assumption |

```text
Cost of equity = risk-free rate + beta * equity risk premium
               = 4.95% + 2.61 * 5% = 18.00%
After-tax debt-cost proxy = 4.25% * (1 - 0%) = 4.25%
Equity weight = 37080 / (37080 + 157.370) = 99.5774%
Debt weight = 157.370 / (37080 + 157.370) = 0.4226%
WACC proxy = equity weight * 18.00% + debt weight * 4.25%
           = 17.9419%, rounded to 18%
```

The weighting calculation mixes current market equity with historical principal/book debt. It therefore does not yet satisfy a strict same-date market-value weighting requirement. Convertible coupons reflect conversion benefits and may understate a straight-debt borrowing rate. The fair-value discrepancy noted above is material; the tiny debt weight here must not be interpreted as proof that convertible claims are immaterial.

Use 18% as a transparent provisional scenario assumption while convertible treatment remains unresolved. Test 16%, 18%, and 20% in the company sensitivity grid to examine discount-rate dependence; this range is analyst-selected, not a statistical confidence interval. Keep the original 9%–11% grid for training validation.

The 0% immediate shield assumption is specific to this WACC shortcut. It does not silently finalize the separate historical FCFF tax adjustment or the future cash-tax assumptions embedded in forecast margins.

## Terminal growth assumption

Use **3% nominal annual FCFF growth from 2031 onward**, with 2%, 3%, and 4% as sensitivity cases. These are analyst-selected assumptions, not Rocket Lab guidance.

The [June 17, 2026 FOMC projections](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260617.htm), Table 1, show longer-run median real GDP growth of 2% and PCE inflation of 2%. Together these provide a rough 4% nominal economic-growth reference. This is an approximation, not an official nominal GDP forecast: PCE inflation is not the GDP deflator. A 3% nominal company cash-flow assumption sits below that reference and implies about 0.98% real cash-flow growth at 2% inflation, since 1.03 / 1.02 - 1 = 0.009804.

The selected rate describes a mature business, after the explicit forecast. It does not extend the scenario's high revenue-growth assumptions indefinitely. Using it immediately after 2030 assumes sustainable cash generation, stable margins, and adequate reinvestment by then. The scenario has not demonstrated that maturity; a longer transition period may be needed. The discount rate and cash flows are both nominal USD quantities.

```text
2030 scenario FCFF = 175.439453 million (rounded)
2031 FCFF = 2030 FCFF * 1.03 = 180.702637 million
Terminal value at end-2030 = 2031 FCFF / (WACC - terminal growth)
                          = 180.702637 / (0.18 - 0.03)
                          = 1204.684247 million
```

The calculation uses the unrounded scenario internally. This terminal value is an end-2030 amount, not today's enterprise value or equity value. It must be discounted five periods in the lab's annual convention and combined with explicit cash flows. That convention uses the FY2025 base and is not a precise September 10, 2026 valuation-date model.

Check passed: 3% is below 18%; all company grid combinations (WACC 16%, 18%, 20%; growth 2%, 3%, 4%) also satisfy growth < WACC. The implemented grid marks invalid editable combinations as invalid; this behavior was tested.

## Validation completed

The Lab 05 training model was rerun and the user supplied all 12 output lines. They matched the expected training results, including enterprise value 1624.8685, equity value 1374.8685, value per diluted share 27.4974, and terminal-value present value / enterprise value 0.7240. These are training results, not Rocket Lab results.

## Computed scenario results

Run command: `python dcf.py`. The first 12 lines preserve the original training output, followed by the training grid and reverse DCF, then the separately labeled Rocket Lab blocks.

Training checks passed: all 12 baseline outputs, all nine grid cells, and a reverse growth shift of +1.7779 percentage points producing $30.00. Additional checks covered unreachable targets, exact endpoint roots, invalid growth rates, and reversed bounds.

Company results using the assumptions above:

| Measure | Result |
|---|---:|
| PV of five explicit cash flows, USD millions | -333.9421 |
| PV of terminal value, USD millions | 526.5786 |
| Enterprise value, USD millions | 192.6364 |
| Equity value, USD millions | 1137.3494 |
| Value per historical diluted weighted-average share, USD | 2.1433 |
| Value / target market price | 0.0346x |

The ratio is outside the lab's 0.5x–2x band. Do not tune inputs merely to match the price. The most distrusted forecast assumption is the FCFF-margin improvement: its timing is unverified. The historical capitalization bridge and five-year maturity assumption also limit the comparison.

Terminal-value PV / enterprise value is 273.35%. This exceeds 100% because the explicit-period PV is negative; it is not an arithmetic error.

| WACC / terminal growth | 2% | 3% | 4% |
|---|---:|---:|---:|
| 16% | $2.29 | $2.39 | $2.51 |
| 18% | $2.07 | $2.14 | $2.22 |
| 20% | $1.91 | $1.96 | $2.02 |

The base case is centered. Values decrease down each column and increase across each row. The corner range is $1.91–$2.51.

Company reverse DCF solves a uniform shift in all five FCFF margins, holding the revenue path, WACC, terminal growth, cash, debt and shares fixed. The shifted Year 5 FCFF also changes the terminal-value base. This differs from the training growth-rate shift because the company forecast crosses from negative to positive cash flow.

At the $61.96 target, there is **no solution within the -5 to +10 percentage-point margin-shift bracket**. The endpoint prices are $1.2965 and $3.8367. Neither endpoint is reported as a solved answer. This bracket cannot explain the market price under the fixed scenario; it does not establish mispricing or the market's actual growth forecast.

## Unresolved inputs and interpretation limits

- **Historical FCFF:** The interest tax adjustment is unresolved, so the historical FCFF row remains a formula, not a finalized point estimate. It is not used to generate the explicit forecast. The training result is retained and labeled separately.
- **WACC and debt:** 18% is a provisional estimate. Market-value debt weighting and consistent convertible-debt/dilution treatment are unresolved; the calculation uses the disclosed historical debt proxy. This limitation also affects the equity bridge.
- **Forecast:** Revenue growth and FCFF margins are AI-assisted classroom estimates, not management guidance. Positive FCFF in 2029 and maturity after 2030 are unverified assumptions. The company outputs must remain labeled illustrative.
- **Dates:** The annual model uses a FY2025 base and five full discount periods. It has not incorporated subsequent quarterly financials or adjusted the discount periods to the September 10, 2026 quote date.
- **Reverse DCF:** The chosen variable is a uniform FCFF-margin shift. No solution exists in the tested bracket; no market-implied growth rate has been established. Do not present the result as proof of mispricing.

Further research could examine updated filings, the cash-flow turnaround, and convertible treatment. The present submission should disclose these gaps rather than imply that they have been resolved or change assumptions solely to match the price.

## Explanation to review before submitting

The training case validates the calculations. For Rocket Lab, the explicit path allows early losses and later positive cash flow. WACC discounts those cash flows; terminal growth governs cash flow after Year 5. The grid tests those two assumptions while holding the forecast and equity bridge fixed. The reverse DCF changes all five FCFF margins by the same number of percentage points while holding revenues and the other listed inputs fixed. Its failed bracket means that this particular range of margin improvements cannot produce the target price.

The most important judgment is whether the assumed cash-flow recovery is defensible. The low valuation is conditional on that scenario, the high discount rate, the five-year horizon, and the provisional capitalization inputs.

## Conditional recommendation

**Draft classroom call: Watch/defer.** Initiate only if an updated, sourced forecast and consistent treatment of cash, convertible debt, and dilution support a value per share above the then-current market price; otherwise remain on the watchlist. A price decline alone would not resolve the model's outstanding assumptions.

Under the current illustrative assumptions, the base value is $2.14 per share and the sensitivity range is $1.91–$2.51, versus the recorded $61.96 target. The reverse DCF has no solution within the tested -5 to +10 percentage-point FCFF-margin shift. These results do not support initiating under this scenario, but they do not prove that the market is wrong.

**Monitor:** Cash burn in the next quarterly filing, using operating cash flow minus capital expenditures, compared with the same period a year earlier. If the filing presents year-to-date amounts, compare matching year-to-date periods or derive standalone quarters consistently. Track whether cash burn narrows or widens, and examine the reasons before revising the forecast. This monitoring measure is not FCFF because it omits the after-tax interest add-back.

The scenario assumes positive annual FCFF in 2029. Persistent or widening cash burn would challenge that turnaround date; narrowing burn would be evidence to investigate, not sufficient proof by itself. Reassess the forecast and valuation when the next filing arrives.

This wording is an AI-assisted draft for the student's review. It does not assert independent research, teammate participation, or work the student has not performed.

## Submission

GitHub artifact links: unresolved; this file has not been published.

Submit individually using GitHub links to `dcf.py` and `rocketlab_lab06.md`. Upload only these coursework files, not the surrounding `.codex` application folder.

- [ ] Review the forecast assumptions and conditional call; revise any wording that does not reflect your judgment.
- [x] Run `python dcf.py` and check the training and company output (completed; output supplied in chat).
- [ ] Upload both files to the coursework GitHub repository and verify the saved contents.
- [ ] Copy each file's GitHub page link and submit through Brightspace > Quizzes > Lab 06.

[Session 06 slides and checkout instructions](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-03/slides-session-06.md)

[Lab 06 instructions](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-03/lab-06-sensitivity-and-reverse-dcf.md)
