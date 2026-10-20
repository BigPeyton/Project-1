# Lab 12 — Rocket Lab analysis, CDNS review and reflection

Prepared October 1, 2026. My company: **Rocket Lab (RKLB)**. Partner company: **CDNS**.

This is the consolidated current report. Earlier Lab 12 templates remain working files; use this report with the presentation script and existing evidence.

## 1. Presentation and evidence

[Full presentation script and prepared answers](rocketlab_lab12_script.md) · [Detailed evidence outline](rocketlab_lab12_outline.md) · [Assignment](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-06/lab-12-proforma-present.md)

| Evidence | Use |
|---|---|
| [Lab 06 DCF](rocketlab_lab06.md), [code](dcf.py) | Earlier forecast, price, enterprise-to-equity bridge and reverse DCF |
| [Lab 08 peers](rocketlab_lab08.md), [output](rocketlab_lab08_output.txt), [code](rocketlab_lab08.py) | Redwire/Avio decisions and negative-earnings limitation |
| [Lab 10 sources and assumptions](rocketlab_lab10.md), [statements](rocketlab_lab10_output.txt), [code](rocketlab_lab10.py) | History, linked forecast, funding, checks and share reconciliation |
| [Lab 11 current report](rocketlab_lab11_rd.md), [visible output](rocketlab_lab11_output.md), [code](rocketlab_lab11.py) | Growth/R&D inputs, results and accounting trace |
| [Detailed scenario data](rocketlab_lab11_details.json), [prediction disclosure](rocketlab_lab11_rd_prediction_draft.md) | Saved assumptions, outputs and earlier requirement status |

## 2. Full analysis summary — explanation

**Selection and initial view:** The proposed selection rationale is that Rocket Lab connects a growth opportunity with a difficult cash-generation question. Launch services and space systems require development, equipment and working capital. Public filings make it possible to test the financial implications. The proposed progression in my thinking is from focusing on sales growth to examining the investment and funding required to produce it. These personal statements are drafted for review, not recovered evidence of my original thoughts.

**Company and evidence:** Saved FY2025 history includes revenue of $601.799 million, gross profit of $207.181 million, R&D of $270.716 million and operating cash flow of −$165.521 million. Lab 10 links to the FY2023–FY2025 filings with table locators. Filings use USD thousands; the model uses USD millions, with shares separately in millions. Reported revenue growth is not automatically organic growth.

**Pro-forma:** The forecast starts at December 31, 2025 and projects FY2026–FY2030. Judgment paths include revenue growth of 40%, 35%, 30%, 25%, 20%; gross margins of 35%, 38%, 40%, 42%, 43%; R&D of $290–330 million; and capex of $160–200 million. Growth and margins need support from delivery and cost evidence. Customer advances fund some operations but create delivery obligations. The forecast explicitly models working capital, noncash note conversion and use of existing securities.

Signed FCFE is −$310.673m, −$222.702m, −$116.934m, −$9.260m and +$83.956m. Net income becomes positive before FCFE because investment still consumes cash. Saved balance-sheet, liquidity and roll-forward checks pass in all five years. Cash exceeds the $100m floor. Passing accounting checks does not establish forecast realism.

**Valuation basis:** All values below are USD. The models use the year-end 2025 baseline and annual discount periods, not a fully updated September or October valuation date.

| Method | Result/share | Shares, millions | Key conventions |
|---|---:|---:|---|
| Earlier FCFF DCF, prepared Sept. 10 | $2.1433 | 530.664781 | 18% provisional WACC, 3% terminal growth, historical weighted-average shares |
| Positive-FCFE classroom convention | $1.23 | 619.894349 | 15% cost of equity, 3% terminal growth; negative explicit FCFE excluded from this convention only |
| Signed FCFE plus starting excess liquidity | $2.002 | 619.894349 | Includes loss-year cash outflows; headline method for Lab 11 |
| Signed value, comparison denominator only | $1.93 | 641.739433 | Same baseline equity value with a different denominator; not an updated forecast |

The FCFF bridge is enterprise value $192.6364m + cash/securities $1,098.824m − debt proxy $154.111m = equity $1,137.3494m. Convertible treatment and the historical share basis are material limitations. The linked FCFE method instead adds starting excess liquidity to signed discounted equity cash flows and terminal value. It does not subtract converted/repaid debt again, count securities-sale proceeds as FCFE, or add ending cash again.

The terminal assumptions materially affect value. The 94.53% terminal contribution belongs specifically to the positive-FCFE classroom convention. Its sustainable terminal year assumes reinvestment slows after the explicit expansion period; that transition needs economic support.

The saved quote was $74.63 on September 24, 2026 at 1:46 PM EDT. The comparison uses 641.739433 million shares, but changing the denominator does not incorporate later financing proceeds, acquisitions or operations. The gap is a research question, not proof of current mispricing.

**Reverse DCF:** The earlier model targeted the saved September 10 close of $61.96. Uniformly shifting all five FCFF margins by −5 to +10 percentage points produced endpoint values of $1.2965 and $3.8367, with revenue, WACC, terminal growth, cash, debt and shares fixed. The changed last-year cash flow also changes terminal value. No solution exists in that tested bracket; no market-implied growth rate was established.

**Peers:** Redwire and Avio offer qualified space-systems and launch comparisons. Redwire's reported earnings are negative. Avio's saved reported-basis P/E is 82.38×, but RKLB's negative annual EPS prevents a meaningful positive-earnings P/E target. Unavailable peer value is not zero value. Different DCF conventions and an unavailable peer target should not be averaged.

## 3. Sensitivity and supported conclusion

Only one input path changes in each run: annual revenue growth ±5 percentage points, or annual R&D spending ±20%. Values use signed FCFE plus starting excess liquidity, 619.894349 million scenario shares, 15% cost of equity and 3% terminal growth from the FY2025 baseline.

| Scenario | FY2030 operating profit, $m | FY2030 FCFE, $m | USD/share |
|---|---:|---:|---:|
| Base | 268.841 | 83.956 | 2.002 |
| Lower growth | 161.905 | 18.454 | 1.338 |
| Higher growth | 393.600 | 158.922 | 2.760 |
| Lower R&D | 334.841 | 133.456 | 2.631 |
| Higher R&D | 202.841 | 34.456 | 1.357 |

Growth has the larger low-to-high value span over these ranges: $1.423/share versus $1.274/share for R&D, using unrounded results. The ranking depends on unequal ranges and units; it is neither a probability nor a universal importance ranking. Saved checks pass, and the restored base matches exactly.

The higher-R&D trace is $330m → $396m expense, −$66m operating profit, −$16.5m tax in profitable FY2030, and −$49.5m net income/FCFE. The value reduction also reflects the other forecast years and terminal effects. Lower R&D mechanically helps because future development benefits are not linked to revenue in this model; the result does not recommend a spending cut.

**Conclusion:** Watch/defer while researching whether growth, margin improvement and funding are consistent with development milestones and investment needs. Delays or overruns would prompt a combined review of revenue timing, R&D, capex and funding. A current investment comparison also needs date-aligned operating and capitalization information.

## 4. Confirmed CDNS opening

My partner and I started by discussing what makes CDNS attractive and its value drivers. I then suggested that he choose more company-specific value drivers.

## 5. CDNS exchange

**Question:** “What makes CDNS attractive, and what source supports the business feature you are relying on?”

**Partner Answer:** “I see recurring business as an attractive feature. I need to connect that to a forecast and price rather than assume an attractive business is automatically an attractive investment.”

**My follow-up:** “Which drivers would make your forecast more specific to CDNS?”

**Partner answer:** “I would investigate recurring-contract growth and the timing of hardware/IP deliveries instead of relying only on total revenue growth. These would be proposed explanatory drivers, not assumptions already implemented and tested.”

**Model/valuation question:** “How would each driver reach the statements and valuation?”

**Partner answer:** “I would separate the relevant revenue streams and link delivery or contract assumptions to recognized revenue. Then I would model associated costs, working capital and cash collection. Only the resulting cash-flow change should enter valuation. I cannot claim a new value before implementing those links.”

**My follow-up:** “Good. Changing recognition timing does not automatically change cash by the same amount. Show the collection and contract-balance effects explicitly.”

**Sensitivity/interpretation question:** “Which driver matters most, what ranges did you test, and what would change your conclusion?”

**Partner answer:** “That ranking remains unresolved without a computed table. I would justify low/base/high ranges, test one input at a time and report the resulting cash-flow and value spans. Weaker contract growth, delivery slippage or less favorable cash conversion would challenge my thesis.”

**My feedback:** Keep the company-specific business explanation, but distinguish a promising driver from a demonstrated sensitivity result. Implement and check the links before describing a quantitative ranking.

## 6. Evidence check — actual source inspection, joint discussion

AI inspected the [CDNS FY2025 revenue note](https://www.sec.gov/Archives/edgar/data/813672/000081367226000016/R11.htm) during preparation.

**Claim examined:** Recurring revenue is a substantial part of CDNS's reported business.

**Locator:** Revenue note, recurring/up-front table, fiscal 2025 column. It reports 76% recognized over time plus 4% other recurring, totaling 80% recurring; up-front revenue is 20%. The same note identifies hardware/IP deliveries as affecting this mix. These are shares of revenue, not growth rates or renewal rates. [Source](https://www.sec.gov/Archives/edgar/data/813672/000081367226000016/R11.htm)

**Calculation:** 76% + 4% = 80%; 80% + 20% = 100%.

**Result:** The source and arithmetic support the historical mix claim. They do not establish future growth, retention, cash timing or fair value.

**Exchange:** I explain that the 80% figure cannot be used as an 80% renewal assumption. My partner agrees to keep the historical mix separate from future contract-growth assumptions. No model repair is claimed.

## 7. Explanation back and feedback given

**My explanation back:** “Your proposed CDNS conclusion is that its recurring business merits further analysis, but a purchase decision needs a supported valuation. Recurring-contract growth and delivery timing are proposed operating drivers. The biggest limitation is that you have not yet translated them into a checked cash-flow model and tested a ranking.”

**Partner correction:** “Yes. I am not claiming a verified buy price or saying recurring revenue guarantees growth.”

**Evidence-backed strength:** The business thesis points to an identifiable filing disclosure rather than relying solely on a general technology-growth story. The revenue-mix check supports that limited historical claim.

**Specific improvement:** Build and test company-specific operating assumptions and show how they affect cash flow. Preserve the distinction between historical disclosure, forecast judgment and computed results. This elaborates on my confirmed suggestion.

## 8. As presenter — answers and feedback

| Question about RKLB | Answer | Evidence |
|---|---|---|
| Why Rocket Lab, and what supports the growth-versus-cash concern? | It combines expansion with development and investment needs. FY2025 revenue was $601.799m while operating cash flow was −$165.521m. | Lab 10 history and filing links |
| Why are there different values per share? | FCFF and FCFE forecasts, discount rates, financing treatment and share denominators differ. The signed-FCFE headline is $2.002 on 619.894349m shares; the separate comparison denominator gives $1.93. | Lab 06 and Lab 10 valuation sections |
| Does more R&D reduce FCFE by the full expense increase? | In FY2030, taxes offset $16.5m of the $66m increase, leaving a $49.5m FCFE decline. Loss years have different modeled tax effects. | Lab 11 statement trace |
| Does the lower-R&D result justify cutting development spending? | No. The model captures the cost but not its possible technical or revenue benefits. | Lab 11 limitation |
| Is growth always the most important driver? | No. It has the larger effect over the selected ranges. Other ranges and linked economic effects could change the result. | Lab 11 inputs and output spans |

**Explanation back by reviewer:** “Your call is watch/defer. Growth leads over the tested ranges, with R&D also important. Your largest concern is whether the modeled growth and investment can coexist, and the annual baseline does not represent current fair value.”

**Correction:** I clarify that $2.002 and $1.93 are different share-basis presentations of the annual-baseline signed model. Neither is a newly updated market valuation.

**Strength received:** The R&D example explains input → operating profit → taxes → net income → FCFE with numbers that reconcile to saved results.

**Improvement received:** Test a combined development scenario that links revenue timing, R&D and capex rather than interpreting an isolated expense change as a complete business outcome.

## 9. Response and reflection

| Decision | Action and reason | Status |
|---|---|---|
| Keep | Signed cash flows and accounting checks expose the cash needed during loss years | Existing work retained |
| Keep | One-input sensitivities clearly isolate the calculation mechanism | Existing work retained; ranking qualified by ranges |
| Revise communication | Show date, method and shares next to every value to address the share-basis confusion | Included in this report and prepared script |
| Investigate | Link RKLB milestones and deliveries to growth, R&D and capex, following the development-spending challenge | Proposed research; no new model run |
| Investigate | Align operating data and capitalization to a common valuation date | Outstanding research |

**Effect on conclusion:** In this, watch/defer remains appropriate because the exchange identifies limitations rather than supplies new operating evidence or a recalculated valuation. I would not change an output just to match a price or answer a challenge.

**Effect on research priority:** My first priority becomes whether technical progress and investment support the revenue path. The CDNS discussion reinforces the value of explaining broad financial assumptions with company-specific operating drivers.

**Question that prompts reconsideration:** “Does a higher value under lower R&D mean the company should cut spending?” It exposes the difference between a mechanical cost sensitivity and a real business decision with future benefits and risks.

**What I understand better:** Positive earnings do not guarantee positive FCFE. Investment and working-capital needs matter, as do the assumptions connecting development spending to future revenue. Similarly, a large recurring-revenue share does not by itself supply a forecast or valuation.

## 10. Checkout text and delivery status

**Checkout text:** “My Lab 12 materials include my Rocket Lab analysis and presentation, existing model outputs, and the CDNS review discussion. The report explains valuation conventions, traces the R&D sensitivity, and records proposed research and limitations.”

Use GitHub links to this report, the script and the existing visible outputs after upload. No repository URL was supplied, so live file links cannot be generated or verified here. GitHub publication and course checkout have not been performed.

| Requirement | Material supplied | Actual status |
|---|---|---|
| Selection-to-valuation explanation | Full script, summary and evidence links | Prepared |
| Valuation reasoning | Methods, bridge, dates, shares, peers and reverse DCF | Written |
| Sensitivity interpretation | Base/changed results, causal trace and range qualifications | Written using saved results |
| Partner questions and review | Three question areas, source check, explanation back, strength and improvement |
| Response and reflection | Keep/revise/investigate decisions, conclusion effect and research priority |
| GitHub checkout | Packaged files and prepared checkout text | Upload/submission not performed |
