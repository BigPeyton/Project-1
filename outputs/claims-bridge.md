# Claims review output

USD millions. Dated proxies and assumptions; not a final enterprise value, equity valuation or complete September balance sheet.

| Claim | Reference deduction |
|---|---:|
| other_borrowings | 1.716000 |
| finance_leases_estimated | 14.761729 |
| contingent_consideration | 13.674000 |
| Accrued bridge financing issuance costs | 12.600000 |
| Accrued ATM issuance costs | 0.163000 |
| Business-combination seller payable | 0.800000 |
| **Selected claims total, before retained notes** | **43.714729** |

Estimated standalone liquidity after reserve and selected claims: $2,069.375578 million.

This figure excludes operating business value, remaining hypothetical option receipts, forward/ATM settlement cases and capped-call value. Future-flow treatment must be reconciled before using it.

## Convertible diagnostics

- June principal (reference only): 13.366000.
- September-price conversion parity, using dated remaining share population: 161.575880.
- June reported note fair value (stale-date diagnostic): 280.789000.
- Converted case: count note shares and zero note deduction.
- Retained case: exclude conversion shares and require an explicit economic claim assumption.

Operating lease payments remain in forecast operating cash costs, so no separate operating-lease deduction. Finance leases are treated as financing; exclude their future debt service from FCFF. Earn-outs, fees and seller payables must not also be paid in forecast FCFF after being deducted here.

Review details and residual limitations: docs/claims-treatment.md and data/claims.json.
