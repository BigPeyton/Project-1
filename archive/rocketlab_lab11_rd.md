# Lab 11 — Rocket Lab: revenue growth and R&D sensitivity

## Status and question

Which assumptions drive my company's forecast and value, and what explains their effects?

## Model and reproduction

The original Lab 10 model is unchanged. Each run loads an independent model and
deep-copies the same base inputs, changes one input path, and recalculates the
linked income statement, balance sheet and cash flow for FY2026–FY2030.

Run `python rocketlab_lab11.py` with `rocketlab_lab10.py` in the same folder.
No third-party packages are required.

- [Script](rocketlab_lab11.py)
- [Visible output: inputs, signed changes, spans, checks and statement trace](rocketlab_lab11_output.md)
- [Full five-year statement and input details for every run](rocketlab_lab11_details.json)
- [R&D prediction draft saved before the changed runs](rocketlab_lab11_rd_prediction_draft.md)
- [Original Lab 10 assumptions and filing sources](rocketlab_lab10.md)

Amounts are USD millions except dollars per share. FCFE means free cash flow to
equity. The model is an annual-baseline classroom scenario, not a fully updated
September 2026 investment valuation. Historical inputs were retained from Lab 10;
no new financial observations were generated.

## Inputs and rationale

| Driver | Lower: 2026, 2027, 2028, 2029, 2030 | Base | Higher |
|---|---|---|---|
| Revenue growth (%) | 35, 30, 25, 20, 15 | 40, 35, 30, 25, 20 | 45, 40, 35, 30, 25 |
| R&D expense (USD millions) | 232, 240, 248, 256, 264 | 290, 300, 310, 320, 330 | 348, 360, 372, 384, 396 |

Revenue growth shifts ±5 **percentage points** in every year. R&D is multiplied
by 0.8 or 1.2: a **20% relative change** in each year's dollar expense. All other
independent assumptions, including gross margin, stay at base. Outputs such as
taxes, cash and retained earnings recalculate.

These are proposed judgment ranges, not guidance, probabilities or confidence
intervals. Growth tests weaker/stronger delivery and contract conversion. R&D
tests lower development expense or spending pressure around the base path.
The lower R&D path is below the $270.716 million recorded for 2025 in Lab 10;
it should be understood as a counterfactual, not a prediction of a spending cut.

R&D is company-relevant: Rocket Lab's 2025 annual report attributes the increase
in R&D to Neutron progress, staff costs and prototype spending for spacecraft
and components. It also identifies potential additional R&D and capital needs
from development setbacks. The ±20% width is an analyst judgment; the filing
does not establish that specific range. [2025 annual report](https://www.sec.gov/Archives/edgar/data/1819994/000181999426000013/rklb-20251231.htm)

The modeled R&D line is total company R&D, not a separately disclosed Neutron
budget. A spending change alone is not a complete Neutron-delay scenario: such
a scenario could also affect revenue timing, capex and financing.

## Results and signed differences from base

| Scenario | 2030 operating profit | Change | 2030 FCFE | Change | Value/share | Change |
|---|---:|---:|---:|---:|---:|---:|
| Base | 268.841 | 0.000 | 83.956 | 0.000 | 2.002 | 0.000 |
| Lower revenue growth | 161.905 | -106.936 | 18.454 | -65.502 | 1.338 | -0.664 |
| Higher revenue growth | 393.600 | +124.759 | 158.922 | +74.966 | 2.760 | +0.758 |
| Lower R&D | 334.841 | +66.000 | 133.456 | +49.500 | 2.631 | +0.629 |
| Higher R&D | 202.841 | -66.000 | 34.456 | -49.500 | 1.357 | -0.645 |

Value uses the existing funding-adjusted signed-FCFE method plus starting excess
liquidity and 619.894349 million scenario shares. Negative forecast cash flows
remain included. The positive-FCFE-only classroom convention is retained in the
JSON details but is not used for the headline comparison. The cost of equity,
terminal growth, cash floor and share count remain unchanged.

Each run passes the model's existing valuation checks. This does not eliminate
economic limitations: the terminal formula extrapolates the changed final-year
operating profit into a sustainable terminal year, so a persistent R&D change
also affects terminal value. This is not merely a temporary expense test.

## Output spans and draft interpretation

| Output span: maximum minus minimum | Revenue growth | R&D expense |
|---|---:|---:|
| FY2030 operating profit, USD millions | 231.694 | 132.000 |
| FY2030 FCFE, USD millions | 140.468 | 99.000 |
| Value, USD/share | 1.423 | 1.274 |

All three cases are valid for each output and driver. Differences and spans
use unrounded numbers; subtracting displayed numbers may differ by 0.001.

Revenue growth has the larger effect **over these ranges**. Annual growth
changes compound through the sales base, changing gross profit, SG&A and
working-capital needs while the dollar R&D and capex paths remain fixed.
R&D expense directly changes operating profit and cash generation without
changing the sales base in this model.

The ranges have different units and widths. A ±5-point growth path and a ±20%
expense path are not equally sized shocks in a standardized sense. The ranking
is conditional on those choices, not proof that growth is inherently more important.
A sensitivity table also does not assign probabilities to the scenarios.

For the higher-R&D trace, FY2030 R&D rises from 330 to 396, so operating profit
falls 66. Pretax profit remains positive, and tax falls by 66 × 25% = 16.5.
Net income falls 49.5. Revenue, working-capital investment, D&A, capex and debt
repayment are unchanged, so FCFE falls by the same 49.5:
34.456 - 83.956 = -49.500. Cash and equity also decline through the linked statements.
Earlier loss years receive no immediate modeled tax benefit, so a 25% tax
offset should not be applied indiscriminately to every forecast year.

**Economic limitation:** lower R&D mechanically improves this model's results,
but the model does not connect spending to technical milestones, launch success,
future products or revenue. It cannot establish that cutting R&D creates value.

## Reconciliation of the prediction

The original prediction was saved in a separate file before R&D runs. These
actuals were added afterward; the original estimate has not been rewritten.

| Higher-R&D change | Pre-run prediction | Actual change |
|---|---|---|
| FY2030 operating profit | -66 million | -66.000 million |
| FY2030 FCFE | About -49.5 million | -49.500 million |
| Value per share | Down roughly 0.5–0.6 | -0.645 |

The operating and FCFE predictions match the model's arithmetic. The valuation
decline is about $0.045 larger than the upper magnitude of the rough predicted
range. The estimate did not fully capture the five-year cash-flow timing,
absence of loss-year tax benefits and terminal effect. The predicted larger
growth spans were observed. The asymmetry between the lower/higher R&D share-
value changes reflects the model's nonlinear tax treatment across forecast years.

## Verification

All six driver/case runs pass accounting and funding checks in all five years.
The lowest cash balance across the tested runs is $211.383 million, above the
$100 million floor. Each run asserts that only the selected independent input
has changed; full snapshots are retained in the JSON.

The restored base matches the initial inputs, statements, checks and valuations
exactly using unrounded values (zero restoration tolerance). Accounting checks
use 0.000001 USD million tolerance. The original Lab 10 source hash is unchanged.

## Review

> I would retain revenue growth and R&D expense because they test both the sales
> opportunity and development-cost exposure in Rocket Lab's forecast. I treat
> the ±5-point growth and ±20% R&D ranges as judgment scenarios, not probabilities.
> Growth has the larger effect over these ranges, but R&D produces a substantial
> value-per-share span of $1.274 compared with growth's $1.423.
>
> The higher-R&D case reduces 2030 operating profit by $66 million and FCFE by
> $49.5 million. The tax reduction explains the difference in that profitable
> year. I should not interpret the higher modeled value from lower R&D as proof
> that Rocket Lab should cut spending, because the model omits R&D's possible
> future benefits.
>
> My proposed research priority is to examine the connection between development
> spending, technical milestones and future deliveries, then challenge whether
> the revenue path is achievable with the assumed R&D and capex. This analysis
> does not establish a current buy/sell conclusion because the annual baseline
> omits subsequent developments and the quoted market price is dated.

### Partner Exchange 1: prediction and units

**Question:** Does higher R&D mean adding 20 percentage points, and
are you assuming that more R&D automatically creates more revenue?

**Response:** No. R&D is a dollar input multiplied by 1.2, so 2030
expense changes from $330 million to $396 million. The same proportional change
applies to each year's own base amount. Revenue assumptions remain unchanged
in that run. This isolates the expense effect, not the full economic return on R&D.

### Exchange 2: numerical check

**Question:** Why does $66 million of additional R&D reduce final-year
FCFE by only $49.5 million?

**Response:** Final-year pretax income remains positive. The model's
25% tax rate reduces tax by $16.5 million, so the net income and cash-flow effect
is -$49.5 million. I can reproduce the displayed difference as
$34.456 million minus $83.956 million. Capex, working capital, D&A and revenue
remain unchanged in this R&D comparison.

### Exchange 3: ranking and company comparison

**Question:** Could your chosen ranges explain the ranking, and could
my company have a different leading driver?

**Response:** Yes. Growth compounds through all five years, and the
growth and R&D ranges measure different kinds of shocks. Another company may
have different operating leverage, development spending and cash requirements.
We need its actual assumptions and outputs to explain the difference; raw
dollar changes alone do not provide a fair cross-company ranking.

[Assignment instructions](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-06/lab-11-proforma-what-if.md)
