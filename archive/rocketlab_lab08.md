# Lab 08 - Rocket Lab peer evidence and valuation comparison

**Target:** Rocket Lab (NASDAQ: RKLB). **Comparison date:** September 10, 2026,
matching the market-price date in the saved Week 3 work.

## Define / Discover

Question: can comparable companies' annual reported P/E multiples support a
Rocket Lab equity value per share, and what does that add to the Week 3 DCF?

Rocket Lab earns revenue through launch services and space systems. Its FY2025
reported diluted EPS was negative. See [RKLB 2025 10-K][rklb], Item 1, Business;
Note 20, Segments; and F-6 / Note 19, F-43, EPS.

The research needs are business fit, date-consistent prices, earnings public by
the comparison date, and whether positive-earnings P/E is applicable. A relevant
business need not have usable earnings for this method.

## Initial peer policy

Investigate listed operating companies with meaningful space launch, spacecraft,
or satellite hardware businesses and exposure to institutional or commercial
space customers, engineering development, and contract execution risk. Qualify
differences in scale, maturity, geography, customer mix, and launch/manufacturing
mix. Exclude investment vehicles and businesses driven mainly by unrelated
activities or operating satellite communications networks.

Assess business fit separately from numerical eligibility. Use positive annual
reported diluted EPS for numerical peer P/E, never silently replace it with
adjusted earnings. Use same-date prices and earnings already public on that
date, with matching currency and share units within each ratio. Investigate two
candidates and retain excluded inputs and reasons. Do not revise the policy to
achieve a preferred price. No substantive policy revision was made.

Rejection criteria: weak operating overlap, materially different economic drivers,
or untraceable inputs. Nonpositive EPS excludes a numerical P/E, even when the
business remains relevant. Missing information remains unresolved.

## Two candidate decisions - judgments

| Candidate | Decision | Business reasoning and source locator | Numerical treatment |
|---|---|---|---|
| Redwire (NYSE: RDW) | Qualify for business comparison | Spacecraft, solar arrays, and docking systems overlap with space systems. Edge Autonomy adds aircraft exposure. [10-K][rdw], Item 1, Space Segment Business Strategy / Space Infrastructure; [release][rdw-release], FY2025 highlights | Exclude from positive P/E inputs: annual EPS is negative. Retain as a researched candidate. |
| Avio S.p.A. (Milan: AVIO) | Qualify | Vega launch and Ariane propulsion work overlaps with launch. European institutional programs and defense propulsion limit comparability. [Annual report][avio], pp. 5-6, Letter to Shareholders | Positive reported EPS allows a descriptive multiple, subject to capital structure and accounting qualifications. It cannot overcome negative target EPS. |

These candidates address different parts of Rocket Lab, rather than providing two
interchangeable full-company matches. Neither is ranked as the better investment.

## Frozen inputs and evidence

All fiscal years end **December 31, 2025**. These annual reports/results were
public before September 10, 2026. No quarterly EPS was annualized or substituted.

| Company | September 10, 2026 close | FY2025 reported diluted EPS | Currency per share | Evidence public date | Earnings locator |
|---|---:|---:|---|---|---|
| RKLB | 61.96 | -0.37 | USD | February 26, 2026 | [10-K][rklb], F-6 and Note 19, F-43; [SEC filing date][rklb-date] |
| RDW | 10.87 | -2.28 | USD | February 25, 2026 | [Annual results release][rdw-release], Consolidated Statements of Operations and Comprehensive Income (Loss), year-ended-2025 column, basic and diluted loss per common share |
| AVIO | 28.01 | 0.34 | EUR | Annual report available March 31, 2026; results presentation dated March 12 | [Annual report][avio], consolidated income statement p. 211 and Note 3.39 p. 254; [filing announcement][avio-date]; [results presentation][avio-results] |

Price locators: Stock Analysis historical-data tables, **September 10, 2026 row,
Close column**, for [RKLB][rklb-price], [RDW][rdw-price], and [Milan AVIO][avio-price].
These are opened secondary market-data sources, not exchange-certified data.
The RKLB close matches the saved Lab 06 record. Use each local market's closing
price; they share a trading date but not an identical closing instant.

Avio's EUR 0.34 is consolidated diluted EPS; EUR 0.35 is basic EPS. Its separate
parent-company EPS is not the selected input. Note 3.39 also describes warrant
conversions and the November 2025 capital increase. The annual weighted-average
share denominator therefore limits interpretation against the later price.

Each ratio pairs a local-currency ordinary/common share price with the issuer's
reported EPS in that currency. Do not divide a USD quote by EUR earnings or use
an ADR without checking its ratio. P/E is dimensionless, so currency conversion
alone does not solve economic comparability. IFRS versus US GAAP and the capital
raise remain qualifications; the reported EPS is not rewritten as adjusted or
pro-forma earnings. No claim of a normalized, current-capitalization P/E is made.

## Implement and validate

Run `python rocketlab_lab08.py`. It adapts the Lab 07 positive-earnings method to
the sourced inputs above and checks dates, duplicate peers, and EPS eligibility.
It contains no Asbury inputs. AI reran the original Lab 07 calculator separately
and reproduced its saved results; that remains a training check only.

```text
Avio reported-basis P/E = EUR 28.01 / EUR 0.34 = 82.38235294x
Reverse arithmetic check: 82.38235294 * 0.34 = 28.01 (rounded)
```

This is a descriptive historical-earnings ratio, not an accepted Rocket Lab
valuation multiple. A high P/E can reflect a small earnings denominator as well
as expectations; it does not establish growth or attractiveness by itself.

**Supported limitation:** Rocket Lab's EPS is -USD 0.37. Multiplying a positive
peer P/E by that loss would produce a negative arithmetic product, not an
economically defensible equity price. Redwire cannot supply a positive earnings
multiple either. Therefore the result is **no meaningful P/E-derived target
price or range**, not zero value. Cash and debt adjustments cannot repair this.

Prediction written before the Lab 08 removal run: removing Redwire will
leave Avio's descriptive ratio unchanged; removing Avio will leave no usable
positive peer P/E. Neither action resolves the target's negative earnings.

| Check | Result | Interpretation |
|---|---|---|
| Full candidate set | Avio 82.38235294x; no RKLB estimate | One descriptive positive peer multiple, negative target EPS |
| Remove RDW | Avio unchanged; no RKLB estimate | RDW was already numerically ineligible |
| Remove AVIO | No usable peer multiple; no RKLB estimate | Lose the sole positive peer multiple and its information |

Execution confirmed all three outcomes above; the run is saved in
`rocketlab_lab08_output.txt`. Validation also passed for zero, missing and
nonfinite target EPS, a hypothetical positive-EPS control, duplicate peers,
and rejection of future-dated earnings or mismatched price dates. The control
is a code check, not a substitute company or submitted valuation.

The user subsequently ran `python rocketlab_lab08.py` in the VS Code PowerShell
terminal and shared the complete output. It matches the verified run, including
Avio's 82.38235294x ratio, the negative-EPS limitation, and both peer-removal
results. This confirms the user's calculator run; it does not establish a
separate personal hand calculation or partner discussion.

To resolve the earnings obstacle for a future annual P/E analysis requires
positive, representative reported target earnings and defensible peer inputs.
A later profitable quarter alone does not change FY2025 EPS. A restatement would
need documentary support. For this fixed date/basis, the limitation stands;
the lab does not require switching valuation methods.

## Evolve - compare with the saved DCF

The existing `dcf.py` was rerun and reproduced the Week 3 Rocket Lab result.
See [the saved Lab 06 assumptions](rocketlab_lab06.md) and [DCF code](dcf.py).

| Method | Company's result and date | Main assumption or limitation |
|---|---|---|
| Week 3 DCF | USD 2.1433/share base; USD 1.91-2.51 sensitivity range; prepared September 10, 2026 | Illustrative FY2025-base forecast, five annual discount periods, WACC 16-20%, terminal growth 2-4%; cash-flow recovery, capital bridge and date alignment unresolved |
| Peer P/E | No meaningful RKLB value; September 10, 2026 prices and FY2025 annual EPS | Negative target EPS; RDW also loss-making; AVIO business, capital and accounting qualifications |

The DCF assumes future cash generation, while this P/E exercise uses reported
annual earnings. They need not both be usable. The peer evidence does not confirm
or refute the numerical DCF range; it identifies why earnings multiples cannot
provide an independent valuation check here. Do not average a numerical scenario
with an unavailable valuation.

**Provisional call:** watch/defer. **Evidence most likely to change that call:**
a credible operating forecast showing the timing and funding of cash generation,
with cash, convertibles, dilution and discount periods aligned to the valuation
date. These are analytical judgments.

## Review

**Criticism:** The weakest support is the assumed move to positive FCFF in 2029
and a 10% FCFF margin in 2030. The sensitivity grid changes WACC and terminal
growth, not that operating path. It is not a comprehensive fair-value range.

**Response: accept.** The saved model explicitly labels those margins as
assumptions. The 10-K's cash-flow statement, F-8, records negative operating cash
flow and capital investment; it does not establish this forecast's recovery
date. Retain the output as an illustrative scenario and withhold a decision-ready
fair-value range until an operating forecast supports it.

| Additional criticism | Disposition | Evidence and effect |
|---|---|---|
| Date mismatch | Accept | `dcf.py` discounts five complete annual periods from the FY2025 base; it is not rolled forward precisely to September 10, 2026. Earnings availability alone does not fix DCF timing. |
| Capitalization mismatch | Accept | DCF uses historical cash, a book-debt proxy and historical weighted-average shares. [RKLB 10-K][rklb], Notes 6, 12, 19 and 23, identify convertible and share considerations. Updated consistent debt/dilution treatment is needed. |
| EPS versus FCFF confusion | Reject as a proposed substitution | EPS is the annual accounting denominator for P/E. DCF forecasts unlevered cash flow. Negative EPS does not require zero future cash-flow value, and positive EBITDA cannot silently replace EPS. |
| Current fair value is established by the DCF output | Unresolved / not supported | Arithmetic is reproducible, but forecast and capitalization inputs are provisional. Neither the model-price gap nor the failed reverse-DCF bracket proves mispricing. |

**One skeptical question:** What operating and financing evidence supports positive
FCFF by 2029 and a sustainable 10% FCFF margin by 2030, after launch development,
capital expenditure, working capital, and any additional dilution?

**Answer:** The current source set does not establish those milestones.
Revenue growth alone is insufficient. I would need a sourced bridge from sales
and gross profit to operating spending, cash taxes, reinvestment and financing,
with downside cases for delays. Until then, watch/defer is more defensible than
relying on the narrow sensitivity band.

## Reflect - conditional conclusion

**Call: watch/defer.** The peers illuminate different operating activities
but do not supply a usable Rocket Lab P/E valuation. The DCF yields an
illustrative USD 1.91-2.51 range under its fixed forecast, not a comprehensive or
decision-ready fair-value interval. Withhold a final fair-value range because
the recovery path, date alignment, and capital structure need better evidence.

Initiation would require an updated, defensible valuation and downside analysis
supporting adequate upside to the then-current price after funding and dilution.
If that evidence fails to develop, continue deferring or choose do not initiate.
Do not choose a new peer, adjust earnings, or tune the forecast solely to close
the gap with the recorded USD 61.96 share price.

## Source register

Sources opened during this work; price data are secondary, company filings are
primary. Avio's report is the issuer document hosted by Teleborsa. Its official
filing announcement independently establishes availability before the cutoff.

[rklb]: https://www.sec.gov/Archives/edgar/data/1819994/000181999426000013/rklb-20251231.htm
[rklb-date]: https://www.sec.gov/Archives/edgar/data/1819994/000181999426000013/0001819994-26-000013-index.html
[rdw]: https://www.sec.gov/Archives/edgar/data/1819810/000181981026000029/rdw-20251231.htm
[rdw-release]: https://ir.rdw.com/sec-filings/all-sec-filings/content/0001819810-26-000017/exhibit991redwire12312025e.htm
[avio]: https://avio-data.teleborsa.it/2026%2FAvio-2025-Annual-Report_20260331_093610.pdf
[avio-date]: https://www.emarketstorage.it/sites/default/files/comunicati/2026-03/20260331_180952.pdf
[avio-results]: https://avio-data.teleborsa.it/2026%2F2026_03_12-Avio-FY-2025-results_v19_20260312_045151.pdf
[rklb-price]: https://stockanalysis.com/stocks/rklb/history/
[rdw-price]: https://stockanalysis.com/stocks/rdw/history/
[avio-price]: https://stockanalysis.com/quote/bit/AVIO/history/

Course: [Lab 08](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/lab-08-deal-triangulation.md)
and [Session 08 slides](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/slides-session-08.md).
