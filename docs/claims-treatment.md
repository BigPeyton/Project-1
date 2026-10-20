# Debt and other claims: working treatment

Integration update: [three-statements.md](three-statements.md) implements the working settlement schedules and exports `cutoff_bridge_inputs`. Its cutoff claims excluding notes are 43.715696 million and base estimated cash is 2043.230454 million. The small lease-claim change reflects Q3 interpolation instead of the earlier H1 burn rate. Use the integrated inputs together for valuation; older subtotals below are preserved review history. Market-value sensitivities and pending-transaction treatment remain open.

Reviewed October 19 for the September 10, 2026 cutoff. Financial amounts below are USD millions. Sources and exact locators are recorded in `data/claims.json`. This is a classification decision and dated estimate; the final operating forecast still must implement the matching cash-flow treatment.

## Correction to the earlier convertible assumption

The initial retained-note illustration used principal of 13.366 as an expressly provisional proxy. This review rejects that shortcut for market-value analysis. The [June 10-Q, Note 6, page 21](https://www.sec.gov/Archives/edgar/data/1819994/000181999426000062/rklb-20260630.htm) reports note fair value of 280.789, versus net carrying amount of 13.129. Conversion optionality makes principal materially different from the claim's economic value.

At the September quote, the dated remaining conversion-share population has parity of 2.607745 million shares x $61.96 = 161.5758802 million. This is a conversion-value diagnostic, excluding time value, coupon and settlement effects; it is not a September convertible quote. The June fair value is also not a September quote. Neither is silently substituted for a current fair value.

Keep the primary **if-converted** scenario: include 2.607745 million note shares and deduct zero note debt. For a retained-note sensitivity, remove those shares and require an explicit economic claim assumption. The function has no automatic principal default. An intrinsic valuation below the conversion threshold also requires review of the settlement assumption; do not assume observed market price equals model fair value.

This correction belongs in the eventual AI-output validation/evolution record. The original lab files remain unchanged.

## Claim map

| Item | Working treatment | Limitation / matching forecast requirement |
|---|---|---|
| Other borrowings: 1.716 | Deduct carrying-value proxy | June balance carried forward; not verified September fair value. Trinity was already repaid, so do not label this residual Trinity debt. |
| Finance leases: estimated 14.761729 | Deduct estimated total remaining liability | Includes current portion. Annual total 14.970 less H1 principal 0.149 gives June estimate 14.821; deduct the same 0.059271 interim payment already used in the cash estimate. No new finance lease/FX/modification assumed. |
| Operating leases | No separate bridge deduction | Keep lease payments/occupancy costs and renewals in operating forecasts. Debt and multiple definitions must use the same convention. |
| Acquisition earn-outs: 13.674 | Deduct reported fair-value claim, carried forward | Includes potential cash and stock settlement; do not also add stock dilution for the same claim or subtract payment in FCFF. |
| Accrued bridge financing fees: 12.600 | Deduct pending settlement/classification check | Period supplemental disclosure, assumed still unpaid; not a verified cutoff balance. |
| Accrued ATM fees: 0.163 | Deduct on the same assumption | These preexisting fees are distinct from commissions on a hypothetical new issuance. |
| Seller payable: 0.800 | Deduct on the same assumption | Remove if paid and already reflected in estimated cash. |
| Trade payables, customer advances and ordinary accruals | Operating working capital | Do not subtract all balance-sheet liabilities from enterprise value. |
| Unpaid capex: 15.371 | Schedule payment in capex/payable roll-forward | Not a second debt deduction if payment is in forecast cash capex. |
| Contract-loss provision: 4.657 | Model fulfillment losses and provision unwind | Do not leave fixed forever or deduct both provision and future operating cost. |
| Deferred taxes: 10.146 liability | Reconcile tax reversals with cash taxes | No automatic face-value debt deduction; avoid separately capitalizing tax benefits already in forecast. |
| Undrawn acquisition bridge: 3,600 | No standalone debt/cash entry | A commitment is not funded debt. Accrued fees above are separate. |
| Participating preferred | Included once in share denominator | No additional preferred-value subtraction. |

Finance lease liability classification is grounded in the [2025 10-K, Note 16, F-37/F-38](https://www.sec.gov/Archives/edgar/data/1819994/000181999426000013/rklb-20251231.htm). June noncurrent finance leases are 14.468; inferred current balance is 0.353. The inference assumes no other liability changes and must not be relabeled reported data. Treat finance leases as financing: exclude their future principal and interest from FCFF while preserving depreciation/reinvestment economics and lease-asset replacement. Operating leases follow the operating-cost convention instead.

The acquisition fair-value roll-forward is 7.634 + 5.654 + 0.386 = 13.674. Motiv's contingent consideration can settle in stock; the deduction represents a claim on existing holders, not necessarily cash spending. Avoid deducting the entire other-liabilities balance in addition to these identified components.

## Reference bridge subtotal

Selected claims excluding converted notes total **43.714729**. Estimated standalone cash/investments after the operating reserve, **2,113.090307**, less those claims leaves **2,069.375578**. This is only a balance-sheet adjustment to a future operating valuation, not enterprise value, equity value, available dividends or a recommendation. Remaining hypothetical option proceeds and paired financing cases are separate.

The three accrued fee/seller items total 13.563 and have uncertain cutoff settlement status. Show a sensitivity removing them only with the corresponding cash/FCFF treatment, not by silently erasing obligations. Changing a payment from an unpaid claim into lower cash should leave net shareholder value unchanged, all else equal.

## Additional assets and transaction scope

The June MD&A describes capped-call contracts with maximum aggregate future receipts of approximately 201.9 across 2028-29 tranches. That is a contractual potential payoff, not current cash or fair value. Zero asset credit remains a conservative reference convention; the final analysis must show a discounted payoff sensitivity. Do not assume capped-call coverage equals only the remaining notes.

Customer-financing receivables require a choice between operating investment and separate asset valuation, with their interest/cash flows treated consistently. Do not add goodwill or operating acquired intangibles on top of DCF value. Iridium consideration, operations, financing and issuance must move together in any transaction case.

No separate NCI or defined-benefit pension liability was identified in the reviewed statements and annual benefits note. This is a limited review finding, not proof that no other claim can exist. Unclassified residual liabilities, contingent-claim remeasurement and cash settlement timing remain model-integration checks.

## Verification and next step

`python -B -m unittest discover -s tests -v` checks lease payment consistency, conversion/debt exclusivity, contingent-claim reconciliation and exclusion of unfunded commitments from this bridge. These are AI-assisted checks, not the student's locked independent exercise.

Next: normalize historical operations and build the linked forecast. Ensure every claim either affects future FCFF or the bridge once. Final bridge sign-off depends on that integration.
