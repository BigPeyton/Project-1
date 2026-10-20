# Revenue forecast: working assumptions

Prepared October 19 using the September 10, 2026 information boundary. These are AI-assisted analyst scenarios for student review. They update the final project without changing historical lab deliverables.

## Why revise Lab 10

Lab 10 used 40% 2026 growth on $601.799 million of 2025 sales, implying $842.519 million for 2026. With $434.414 million already reported in H1 and $257.5 million as the Q3 guidance midpoint, that leaves only $150.605 million for Q4. Such a decline is possible, but would need an explicit disruption case. It should not survive automatically as the updated base case.

The new base is actual H1 $434.414 million plus Q3 $257.5 million plus an analyst Q4 estimate of $280 million: **$971.914 million for 2026**. Management guided only Q3 revenue of $250-265 million; it did not provide our Q4 or long-term forecast. The same release guided Q3 GAAP gross margin of 29-31% and operating expenses of $143-149 million. Those are constraints to examine in the next cost-model step, not permission to substitute adjusted margins. [August 10 earnings release](https://www.sec.gov/Archives/edgar/data/1819994/000181999426000061/rklb-08102026ex991.htm).

## Company-specific architecture

Use continuing launch services, space systems and incremental Neutron revenue. The first two reconcile to H1 reported segment revenue of $108.249 million and $326.165 million. Launch count times the company's launch-price metric is not an exact GAAP revenue formula because recognition timing differs. June backlog is context, not cash or a revenue schedule. Neutron pad delivery also does not establish a successful commercial launch. [June Form 10-Q, Note 18 and MD&A](https://www.sec.gov/Archives/edgar/data/1819994/000181999426000062/rklb-20260630.htm).

For 2026, choose consolidated Q3/Q4 revenue and a launch allocation; space systems is the residual. This avoids inventing separately guided segment figures. For 2027-2030, grow each continuing business separately, then add the incremental Neutron ramp once. Already owned acquired businesses are inside the starting revenues; do not add their sales again.

| Driver | Downside | Base | Upside |
|---|---|---|---|
| Q3 / Q4 total, $m | 240 / 240 | 257.5 / 280 | 265 / 310 |
| Q3 / Q4 launch allocation, $m | 45 / 50 | 57.5 / 65 | 65 / 75 |
| Continuing launch growth, 2027-2030 | 5 / 5 / 5 / 5% | 15 / 12 / 10 / 8% | 20 / 18 / 15 / 12% |
| Space systems growth, 2027-2030 | 12 / 10 / 8 / 6% | 25 / 22 / 18 / 15% | 35 / 30 / 25 / 20% |
| Neutron recognized-service equivalents, 2026-2030 | 0 / 0 / 0 / 1 / 3 | 0 / 1 / 3 / 6 / 10 | 0 / 2 / 5 / 10 / 16 |
| Revenue per Neutron equivalent, $m | 45 | 50 | 55 |

Apart from the Q3 guidance anchors, these numerical paths are analyst judgments. No probability or statistical confidence is assigned. Each path has its value, basis, challenge and change evidence in [revenue_assumptions.json](../data/revenue_assumptions.json).

The Neutron equivalents describe an amount of recognized service revenue, not a verified physical flight manifest. The $45-55 million amounts lack independently verified contracted pricing in this evidence set and are explicitly weak assumptions. Do not describe them as company guidance or prices extracted from a bundled spacecraft-and-launch award. The five-year base reaches $500 million incremental Neutron revenue in 2030; the project must show a zero-ramp stress so that this uncertainty remains decision-visible.

Even the downside is a growing business, with slower execution rather than a catastrophic shutdown. A complete loss of Neutron revenue and an additional launch disruption are appropriate later high-risk stresses. Future space-system revenue requires new orders as well as delivery of current backlog. Growth rates cannot be justified solely by today's backlog balance.

## Boundaries before valuation

- Pending Iridium operations, synergies, purchase consideration and acquisition financing are excluded together. This standalone forecast is one component of the analysis. A comparison with the market price must address the transaction or defer action pending its resolution.
- Q3 guidance remains an estimate at the September 10 cutoff. No subsequent quarterly outcome or September 15 financing update is used.
- FY2026 revenue combines actual and forecast periods. Before discounting, construct the post-September-10 cash-flow stub. The full-year statements are a reporting view, not all future cash flow.
- Link upside to capacity investment and working capital. Link delay downside to continuing R&D and fixed costs. Do not let lower revenue automatically erase development spending.
- The base remains high-growth in 2030. A direct jump to perpetual low growth requires a defensible transition and reinvestment policy; extend the valuation fade if necessary rather than manufacturing terminal cash flow.

## Verification and next step

Run `python src/revenue_forecast.py` for the [saved visible output](../outputs/revenue-forecast.md). Five new revenue tests verify historical/forecast separation, additive segment reconciliation, isolated Neutron removal, invalid inputs and source timing. All 19 project unit tests passed. They do not establish economic accuracy, complete the final model validation or replace the student's AI-off exercise.

Next: build gross profit, R&D and SG&A paths around this revenue structure, checking the historical normalization and Q3 guidance. Then add working capital, capex, taxes, financing and the three-statement/FCFF link.
