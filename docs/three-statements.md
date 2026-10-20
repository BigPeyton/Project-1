# Linked statements and signed FCFF

Prepared October 19, 2026 with a September 10 information cutoff. These standalone projections are working analyst scenarios, not reported future accounts or a final investment recommendation. Assumptions are AI-assisted and require student ownership and review.

## What is now linked

The model starts from the reported June balance sheet, projects Q3 and Q4, then 2027-2030. Full-year 2026 income and cash flow combine actual H1 with projected H2. Each year has an income statement, balance sheet and cash-flow statement. Equity rolls forward from prior equity and specific earnings/financing entries; it is never a balancing plug.

The opening reclassification preserves all $4,187.374 million of reported assets and $695.221 million of liabilities. It separately identifies $32.150 million customer-financing receivables and $15.371 million unpaid capex. Existing intangibles use the published remaining amortization schedule. Other extracted claims and their settlement assumptions are disclosed; the remaining ordinary liability pool is not mislabeled as trade payables or an exact DPO measure. [June Form 10-Q, balance sheet, Notes 3/10 and supplemental cash flows](https://www.sec.gov/Archives/edgar/data/1819994/000181999426000062/rklb-20260630.htm).

## How cash follows the forecast

- Receivables use collection days; contract assets and prepaids use revenue ratios; inventory uses cost days. The ordinary-liability pool uses a cost ratio; customer advances use a revenue ratio. Reducing advance funding consumes cash. Targets and their downside/upside shifts are explicit.
- New PP&E additions increase assets; depreciation reduces them. Paying the old capex payable reduces cash and the liability, with no second PP&E addition. D&A is already inside the operating-cost forecasts and is added back once for cash flow.
- Future compensation is modeled as paid in cash, including the economic cost represented by ordinary SBC. No future SBC addback creates free cash. Actual H1 SBC remains reported. This is a cash-replacement scenario, not a prediction of award settlement; existing-award dilution remains separate.
- Operating lease expense stays in operating costs. Finance leases have asset depreciation, interest and principal schedules. Loan interest and principal are excluded from FCFF; financial-asset interest is excluded as well.
- Cash taxes use an explicitly approximate positive-profit rate and a small revenue-based minimum, with no automatic refund in loss years or unverified NOL credit. Deferred-tax balances run off on an assumed schedule; book tax and cash tax remain separate.
- Marketable securities can be sold to maintain the $200 million cash floor. External financing is never inserted in the default run. The conditional-equity diagnostic must be explicitly enabled and shows its price, fees, proceeds and shares.

The full values, basis, challenges and change evidence are in [statement_assumptions.json](../data/statement_assumptions.json). June annualized working-capital ratios provide a starting point, not proof of sustainable efficiency. Future capex paths, 9% PP&E depreciation, tax rates, settlement dates and financing terms are assumptions.

## September timing and capital bridge

The old cash bridge prorated historical burn. The integrated model instead allocates Q3 operating flows, working-capital changes and investment evenly over the quarter, taking 72/92 before September 10. The known September option exercise receipt is entirely before the cutoff. Both the estimated cutoff balance sheet and the cash roll-forward to December reconcile.

**Base estimated cutoff cash is $2,043.230454 million**, versus $2,054.985307 million in the earlier interpolation. Use the integrated value with these FCFF forecasts; the old estimate remains a development diagnostic. Neither is reported September cash, and neither includes unverified ATM completion proceeds.

Only remaining Q3 FCFF and Q4 FCFF enter 2026's future valuation cash flow. Subsequent years follow. The exported schedule includes separate dates and actual/365 intervals for discounting. The 2026 annual CFO/CFI/CFF columns still cover the full year; they must not be mistaken for the post-cutoff FCFF row.

Selected cutoff claims excluding notes total $43.715696 million in this schedule. The function exports those claims, cash, securities, reserve, remaining option receipts and customer-financing book reference as `cutoff_bridge_inputs`. The latter is a separate asset-value question, not automatic risk-free cash. Converted notes have zero separate debt claim; their book carrying value is only an accounting reference. Retained-note market-value sensitivity remains unfinished.

Other borrowings, finance-lease principal, financing fees and seller/earnout claims affect projected cash and liabilities, but not operating FCFF. Deduct their cutoff economic claims once in the valuation bridge. Unpaid capex instead affects FCFF and is not an extra bridge deduction. Existing contract-loss provision is released against forecast costs already included in operating expenses, then reversed in indirect CFO. This changes reported-style EBIT presentation without creating cash or charging the same operating loss twice.

The primary model assumes remaining notes convert at the start of Q4 and remaining existing options exercise in Q4. Those are scenarios, not verified events. Pending Iridium, new acquisition financing, unsettled forwards and capped-call value are not silently added; their separate valuation treatment remains required.

## Results and funding failure

| Result | Base | Downside | Upside |
|---|---:|---:|---:|
| 2030 cash, $m | 1,318.589 | 200.000, conditional on financing | 1,857.100 |
| New external equity needed, net $m | 0 | 314.688 | 0 |

The first default downside run stopped in 2030 with an external-funding gap of $314.687718 million to preserve the reserve. The failure was retained and converted into a regression test. An explicitly enabled financing diagnostic assumes $30.98/share and a 2% fee, requiring approximately 10.365072 million new shares. This financing is uncommitted. Without it, the scenario is not funded as specified; weakening the cash floor would not prove long-term solvency.

Base 2030 FCFF is **-$102.065 million**, despite positive operating and net income. Negative FCFF is preserved in every base forecast period. Investment and working capital explain the gap. A valuation must address the transition to sustainable cash generation explicitly; it cannot simply attach a profitable terminal year to these losses.

Future equity counts belong in financing/dilution analysis. A valuation must not count future equity proceeds as free value or charge both the same financing shortfall in signed FCFF and an inconsistent dilution adjustment.

## Limits that remain material

This is an aggregated pro-forma. Operating lease balances use a steady-renewal approximation; unidentified current lease accruals remain within the ordinary-liability pool. Residual noncurrent assets and goodwill are held constant. Customer financing is held at book value without new loans or collections. Deferred taxes use an assumed runoff instead of a jurisdictional schedule. The cash-compensation convention differs from actual equity settlement. Earnout settlement is shown as a cash-equivalent claim even though actual terms can include stock. These assumptions must remain visible and be stressed where material; passing accounting checks does not validate them.

Capex must be challenged against the capacity required by revenue growth. A complete, unconditional market-price conclusion also requires the pending-acquisition treatment, remaining capital sensitivities, WACC, a defensible terminal transition and comparable valuation.

## Reproduction and validation

From the project directory:

```text
python src/three_statements.py
python src/three_statements.py --case upside
python src/three_statements.py --case downside
python src/three_statements.py --case downside --allow-conditional-equity
python -B -m unittest discover -s tests -v
```

The plain downside command is expected to fail with the preserved funding gap. The conditional command prints a distinct scenario; it does not repair the actual financing constraint.

Saved outputs: [base](../outputs/three-statements-base.md), [upside](../outputs/three-statements-upside.md), [conditional downside](../outputs/three-statements-downside.md), and [machine-readable results](../outputs/three-statements.json).

All 36 current unit tests pass. Eleven new checks cover opening-source reconciliation, five-year articulation, deliberate cash/equity corruption, cutoff timing, option receipts, unpaid capex, claim settlements, customer advances, funding/dilution, negative FCFF and invalid inputs. These are development tests, not the published training-case reconciliation, student's locked AI-off exercise or README-only fresh-environment cold run. No elapsed cold-run time or student prediction is claimed.

Next: establish dated WACC inputs and a sustainable cash-flow transition, then integrate the final capital bridge and valuation sensitivities. Retain the funding failure as a decision condition.
