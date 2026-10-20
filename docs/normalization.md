# Historical earnings normalization

Prepared October 19, 2026 using information published before the approved September 10 close. This is AI-assisted research and an analyst policy for student review. Original labs, Edition A and reported financial data remain unchanged.

## Working conclusion

FY2025 operating loss remains $228.838 million under the conservative baseline. No operating addback has been accepted from the reviewed evidence. The separate net-income-to-EBIT bridge removes the reported tax benefit and net nonoperating income; neither is a forecast operating profit source. Contract-estimate revisions remain a business risk. Tax benefits require a separate cash-tax and loss-utilization forecast. [2025 Form 10-K, income statement, MD&A and Note 18](https://www.sec.gov/Archives/edgar/data/1819994/000181999426000013/rklb-20251231.htm).

For H1 2026, remove the $11.180 million cancellation charge from SG&A for the operating run-rate view. The cancellation creates no future vesting or expense for those awards. Result: operating loss $102.303 million and SG&A $100.430 million. Regular SBC remains an economic cost; the remaining H1 SBC is $36.497 million. [June 2026 Form 10-Q, Note 13](https://www.sec.gov/Archives/edgar/data/1819994/000181999426000062/rklb-20260630.htm).

Retain $10.244 million transaction costs and $0.183 million inventory step-up in the working baseline. This is our conservative judgment, not management's non-GAAP definition. Depreciation $17.686 million plus amortization $18.247 million reconciles to aggregate cash-flow D&A $35.933 million. [August 10 earnings release, six-month reconciliations](https://www.sec.gov/Archives/edgar/data/1819994/000181999426000061/rklb-08102026ex991.htm).

## How this feeds the project

- Keep the full reported statements as the accounting starting point. Normalization is a separate analytical layer; never plug the historical balance sheet to match it.
- The cancellation is noncash. Removing its expense also removes its cash-flow addback. Holding taxes and other components fixed, historical CFO is unchanged. Do not increase estimated September cash by $11.180 million.
- Forecast R&D, ordinary compensation and other operating costs explicitly. Historical H1 figures are not automatic full-year forecasts. Replacing canceled awards or redirecting spending could offset the apparent run-rate saving.
- Keep depreciation and amortization in EBIT, then add the appropriate noncash amount once in FCFF with reinvestment modeled. Do not substitute a narrower depreciation note for aggregate D&A without reconciling the scope.
- The accounting cash-flow statement adds back noncash SBC. The valuation must still charge its economic cost through a consistent compensation or future-dilution policy. Existing awards and future grants are different populations; do not double-charge the same grants or treat future labor as free.
- Keep acquired operations in the owned-business baseline. Forecasts must separate organic progress from acquisitions, including acquisition consideration and financing. The pending transaction requires separate treatment.
- Current retention of transaction costs is provisional. A deal-level schedule could support a different forward expense rate; a no-acquisition case must also remove growth that depends on those acquisitions. Do not extrapolate the historical charge mechanically forever.

These records address the Project 1 normalized-base and Week 2 contamination requirements. They do not yet complete the five-year statements, tax model or valuation. The prior Lab 10/11 drivers must be reviewed against this baseline rather than copied unchanged. See [the adjustment register](../data/normalization.json) for each decision, challenge and evidence that would change it.

## Reproduce and validate

From the project folder:

```text
python src/normalize_history.py
python -B -m unittest discover -s tests -v
```

The normalization command prints the reconciliation without modifying reported inputs. The saved output is [historical-normalization.md](../outputs/historical-normalization.md). Four normalization tests and ten existing bridge tests passed on October 19. Tests cover the reported-to-normalized bridge, unchanged raw data, no cash created by noncash adjustments, rejection of duplicate/post-cutoff adjustments, and aggregate D&A scope. These are AI-assisted tests, not the student's AI-off Locked Changed-Input Record or the final fresh-environment cold run.

Next: build and challenge company-specific revenue, gross-margin, R&D and SG&A assumptions before integrating the five-year statements.
