# Operating forecast: gross profit, R&D and SG&A

Prepared October 19, 2026 using the September 10 information boundary. Working analyst assumptions, not management long-term guidance or the student's independent AI-off judgment. Revenue remains the separately saved scenario build.

## Historical and guidance anchors

The first-half segment gross profits reconcile to $161.069 million consolidated gross profit. R&D remains total-company expense: the filing does not provide a stand-alone Neutron R&D budget. Reported costs include compensation and depreciation; the future model must not subtract those expenses a second time. [June 10-Q, Note 18 and MD&A](https://www.sec.gov/Archives/edgar/data/1819994/000181999426000062/rklb-20260630.htm).

For Q3, management guided GAAP gross margin of 29-31% and operating expenses of $143-149 million. Our base uses 30% and $146 million, split into $85 million R&D and $61 million SG&A. The split is ours. Q4 margin of 32%, R&D of $88 million and SG&A of $64 million are also analyst estimates. The downside deliberately misses guidance; it is not constrained to management's range. [August earnings release](https://www.sec.gov/Archives/edgar/data/1819994/000181999426000061/rklb-08102026ex991.htm).

## What changed from the labs

Lab 10's 2026 R&D assumption was $290 million. The updated estimate is $335.942 million, combining actual H1 with the quarterly cost build. The original $330 million 2030 R&D assumption becomes $390 million in the working base. These changes reflect a new spending scenario; the company has not endorsed those amounts.

Instead of a single company margin rising to 43%, the final-project working model separates continuing launch, space systems and incremental Neutron costs from 2027. The base consolidated margin reaches about 36.1% in 2030. R&D and overhead remain substantial as revenue grows. All archived lab inputs and outputs remain unchanged.

## Cost architecture

| Cost driver | Working base, 2027-2030 | Why it is separate |
|---|---|---|
| Continuing launch gross margin | 43%, 44%, 45%, 45% | Tracks launch mix and utilization without applying mature economics to Neutron |
| Space systems gross margin | 34%, 35%, 36%, 37% | Tracks contract execution, integration and manufacturing mix |
| Neutron contribution before fixed commercial costs | 20%, 25%, 30%, 35% of incremental revenue | Isolates revenue-linked production cost from costs that persist without revenue |
| Neutron fixed commercial costs, $m | 25, 30, 35, 40 | Commercial production/launch readiness persists through delays |
| Total-company R&D, $m | 350, 360, 375, 390 | Development is a dollar commitment, not an automatic percentage reduction when sales slip |
| Fixed SG&A, $m | 150, 157.5, 165.375, 173.64375 | Models continuing overhead growing 5% annually |
| Revenue-linked SG&A | 8% of revenue | Adds selling/support costs as the business scales |

The Neutron fixed/variable cost split is weakly evidenced and is not a disclosed budget. Commercial readiness costs are intended to cover production/launch operations; engineering development stays in R&D. Existing-business production overhead stays in its margin. These buckets must be nonoverlapping. Test both additional overruns and removal of the separate readiness-cost allowance for possible overlap before finalizing value.

SG&A's fixed/variable decomposition is also an analyst convention. It preserves overhead through a downturn rather than assuming the entire expense falls with revenue. Transaction/administrative costs remain within that allowance; no separate automatic addback is taken. The upside funds larger dollar expenses despite better margins. The downside sustains R&D above the base while revenue and utilization disappoint.

For each path, [operating_assumptions.json](../data/operating_assumptions.json) records values, basis, challenge and evidence that would change it. Those records complement the revenue and normalization challenge records. They are not real partner feedback.

## Operating implications

The working base has EBIT of approximately -$244.6 million in 2026, -$15.0 million in 2029 and +$106.8 million in 2030. The downside remains loss-making through 2030; the upside reaches positive EBIT in 2028. Those are conditional model outputs, not forecast assurances.

The 2026 annual projection retains the actual first-half $11.180 million cancellation charge. The separate normalized view removes that charge once, giving 2026 normalized EBIT of -$233.453 million. It does not change historical CFO, and it is never removed again from later years. No regular compensation or R&D is treated as free.

In the zero-incremental-Neutron-revenue stress, base R&D and commercial fixed costs remain. Revenue-linked SG&A declines, while the rest of the operating assumptions stay fixed. 2030 EBIT falls by $135 million, from +$106.793 million to -$28.207 million. This demonstrates dependence on Neutron in this operating scenario. It is not yet a valuation stress or a recommendation, and it is not an abandonment scenario with cost wind-down.

## Validation and remaining integration

Run `python src/operating_forecast.py` for the [visible output](../outputs/operating-forecast.md). Six new tests cover the historical/normalized boundary, dollar-for-dollar R&D impact, single-count margin impact, persistent costs with zero Neutron revenue, guidance diagnostics and rejection of invalid inputs or hindsight. All 25 current unit tests passed on October 19. Tests are AI-assisted; they do not replace the published training benchmark, student AI-off record or fresh-environment cold run.

Next, connect operating results to receivables, inventory, customer advances, capex, asset/depreciation schedules, cash taxes and financing. Keep reported H1 separate and build the remaining 2026 period before linking five annual statements. The DCF must include only cash flows after September 10 and retain negative FCFF.

Positive EBIT is not positive free cash flow: investment, working capital and taxes are still missing. A persistently loss-making downside also needs an explicit recovery/restructuring or other defensible terminal treatment; do not insert an unsupported profitable terminal year merely to obtain a value. Pending Iridium remains outside these standalone projections and must be addressed before interpreting the market-price comparison.
