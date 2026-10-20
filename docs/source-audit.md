# Source audit - pending final verification

Do not treat this file as a completed source ledger. The student approved September 10, 2026, regular market close (4:00 PM Eastern) as the valuation/information cutoff. Keep historical measurement dates separate from publication dates and quote dates. Exclude information published after this cutoff. Edition A remains unchanged at its September 1 date.

## Sources to reconcile

- FY2025 10-K: https://www.sec.gov/Archives/edgar/data/1819994/000181999426000013/rklb-20251231.htm
- Q2 2026 10-Q: https://www.sec.gov/Archives/edgar/data/1819994/000181999426000062/rklb-20260630.htm
- Lab 10 citations and prior assumptions: `../archive/rocketlab_lab10.md`.
- Peer policy and citations: `../archive/rocketlab_lab08.md`.

These are source leads, not approval to reuse every number or forecast. Verify publication timing against the selected information cutoff and record the exact filing table/section for each material input.

## Issues discovered in the archived code

1. Lab 10 values FCFE. The final model must calculate FCFF from the same operating forecast. Retain negative forecast cash flows.
2. Lab 10 opens with FY2025 balances, while its market comparison uses a September quote and a later share denominator. Its own comments say that this is not a fully updated September valuation. Resolve the numerator, denominator and timing together.
3. The model assumes conversion of notes and adds conversion shares. A final bridge must either retain debt with the corresponding share basis or consistently model conversion; it must not subtract converted debt and add conversion shares twice.
4. Separate operating cash needs from excess cash; examine investment liquidity and avoid adding projected ending cash on top of initial liquidity and discounted flows.
5. Review contract assets, customer financing, contract liabilities and acquisition effects before classifying operating working capital. Contract liabilities can finance growth but should not become an unexplained perpetual financing benefit.
6. Explicitly justify terminal margins, tax convention and reinvestment. Positive terminal cash flow does not establish that terminal assumptions are sustainable.
7. Review SBC, R&D, acquisitions, one-time costs and contract-estimate revisions. An adjustment needs evidence and economic reasoning, not merely a desire to improve earnings.
8. Peer analysis needs both enterprise and equity multiples, consistent reporting periods and quote dates. Negative P/E is not a usable valuation multiple or zero value.

## Required ledger fields

Input ID; value; units/currency; accounting definition; measurement/as-of date; publication date; URL; source section; raw-to-model transformation; fact/normalization/forecast/output classification; exclusions; verification status; decision sensitivity.

No final current-market recommendation may be inferred from the archived lab values.

## First verification pass - completed October 19

Machine-readable facts and source locators: `../data/reported_financials.json`.
Arithmetic evidence: `../outputs/reported-input-checks.md` (16 checks passed).
Reproduce from the project root: `python src/audit_reported_inputs.py`.

Subsequent share review: see `share-count-and-debt.md` and `../data/capitalization.json`. The August 13 prospectus supplies an August 7 capitalization schedule newer than the cover-page August 5 count discussed below. The documented full-conversion/vesting/exercise scenario is 655.006167 million shares, not an exact September total.

The SEC filing indexes confirm the 2025 10-K was filed February 26, 2026 and the June 2026 10-Q on August 10, 2026, both before the cutoff. The September 10 historical Close column confirms $61.96; do not use the provider's current quote header.

Amounts below are USD millions except actual shares and price. These remain reported facts, not a completed September capitalization or normalized model.

| Item | FY2025 / December 31 | H1 2026 / June 30 | Treatment |
|---|---:|---:|---|
| Revenue | 601.799 (12 months) | 434.414 (6 months) | Different period lengths; do not compare as annual growth |
| Cash and equivalents | 828.660 | 2,129.485 | Excludes restricted cash |
| Current + noncurrent securities | 270.164 | 258.105 | Sum two disclosed lines; liquidity/operating needs still require judgment |
| Convertible notes, net carrying value | 152.395 | 13.129 | June principal is 13.366; distinguish book value, principal and conversion economics |
| Other borrowings, net | 1.716 | 1.716 | Does not include all lease obligations |
| Common outstanding | 543,574,552 | 598,180,438 | Use outstanding, not issued or weighted-average EPS shares |
| Preferred outstanding | 45,951,250 | 40,951,250 | Participating economic interest; reconcile conversion terms |

The cover page separately reports 598,350,482 common shares as of August 5. Do not silently pair that count with June preferred, note conversions and cash as though all were measured September 10. The final bridge needs a documented estimate and sensitivity if exact cutoff balances are unavailable.

TTM revenue through June is derived as 601.799 - 267.067 + 434.414 = 769.146 million. It includes the reported acquisition scope and is not a measure of organic growth. H1 cash flows reconcile to balance-sheet cash only after including restricted cash at both endpoints.

Search surfaced a September 15 financing-completion announcement. It is after our cutoff and must not supply September 10 cash/share facts or hindsight about completed financing. The financing authorization and pending acquisition already disclosed before the cutoff remain relevant risks. The current search is not an exhaustive intervening-filings review.

Remaining before freezing valuation inputs: intervening disclosures, options/RSUs/forwards and convertibles, lease treatment, cash roll-forward, normalization and forecast/WACC assumptions. The core reported-data pass is complete; the full financial-input audit is not.

Execution note: the first audit run reached report writing and was blocked by a workspace permission error. The authorized rerun saved the report successfully. This was a file-write failure, not a failed financial reconciliation, and is not the final fresh-environment cold run.
