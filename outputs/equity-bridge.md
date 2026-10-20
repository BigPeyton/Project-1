# Working enterprise-to-equity bridge

Working standalone instrument sensitivities. The separate downside-exit, comparables and committee memo provide the conditional range/action; instrument and transaction qualifications remain.

USD millions / million shares; prices USD per share. Reference excludes customer-loan recovery, capped-call credit, forward settlement and unverified additional ATM issuance. Pending Iridium operations and transaction funding/consideration are excluded together. These omissions limit comparison with market price.

| Case / instrument treatment | Equity | Shares | Per share | Model value supports conversion at principal threshold? |
|---|---:|---:|---:|---|
| base: if_converted | 1,955.393 | 655.006167 | 2.9853 | False |
| base: retained_at_quote_parity | 1,793.817 | 652.398422 | 2.7496 | False |
| base: retained_at_stale_june_fair_value | 1,674.604 | 652.398422 | 2.5668 | False |
| base: intrinsic_only_diagnostic | 1,942.459 | 652.398422 | 2.9774 | False |
| upside: if_converted | 4,405.511 | 655.006167 | 6.7259 | True |
| upside: retained_at_quote_parity | 4,243.935 | 652.398422 | 6.5051 | True |
| upside: retained_at_stale_june_fair_value | 4,124.722 | 652.398422 | 6.3224 | True |
| upside: intrinsic_only_diagnostic | 4,405.511 | 655.006167 | 6.7259 | True |

Retained quote parity is not a note quote; June fair value is stale. The intrinsic-only diagnostic uses a 12.933957 straight-debt floor and conversion parity, omitting option time value and detailed terms. It is NOT a market fair-value estimate. Base if-converted results are conditional on conversion, not an automatic economic election.

## Reference bridge detail

| Row | Base | Upside |
|---|---:|---:|
| operating_value | -105.930195 | 2,315.388793 |
| cutoff_cash | 2,043.230454 | 2,072.028764 |
| securities | 258.105000 | 258.105000 |
| operating_cash_reserve | -200.000000 | -200.000000 |
| customer_financing | 0.000000 | 0.000000 |
| capped_calls | 0.000000 | 0.000000 |
| new_financing_cash_pv | 0.000000 | 0.000000 |
| other_debt | -1.716000 | -1.716000 |
| finance_leases | -14.762696 | -14.762696 |
| earnout | -13.674000 | -13.674000 |
| financing_fee_payable | -12.763000 | -12.763000 |
| seller_payable | -0.800000 | -0.800000 |
| remaining_option_receipts | 3.703724 | 3.703724 |
| retained_note_claim | 0.000000 | 0.000000 |

## One change at a time, relative to if-converted reference

| Case | Change | Per share | Shares | Equity adjustment |
|---|---|---:|---:|---:|
| base | no remaining option exercise | 2.9952 | 651.608255 | -3.704 |
| base | operating reserve 100 | 3.1380 | 655.006167 | 100.000 |
| base | operating reserve 300 | 2.8326 | 655.006167 | -100.000 |
| base | customer loan book recovery | 3.0344 | 655.006167 | 32.150 |
| base | capped call maximum payoff, discounted | 3.2014 | 655.006167 | 141.569 |
| base | forward minimum_proceeds | 3.5128 | 662.457367 | 371.683 |
| base | forward maximum_proceeds | 3.7117 | 662.457367 | 503.419 |
| base | hypothetical full ATM at 61.96 | 5.6249 | 686.387216 | 1,905.482 |
| base | hypothetical full ATM at 30.98 | 5.3790 | 717.768266 | 1,905.482 |
| upside | no remaining option exercise | 6.7553 | 651.608255 | -3.704 |
| upside | operating reserve 100 | 6.8786 | 655.006167 | 100.000 |
| upside | operating reserve 300 | 6.5732 | 655.006167 | -100.000 |
| upside | customer loan book recovery | 6.7750 | 655.006167 | 32.150 |
| upside | capped call maximum payoff, discounted | 6.9420 | 655.006167 | 141.569 |
| upside | forward minimum_proceeds | 7.2113 | 662.457367 | 371.683 |
| upside | forward maximum_proceeds | 7.4102 | 662.457367 | 503.419 |
| upside | hypothetical full ATM at 61.96 | 9.1945 | 686.387216 | 1,905.482 |
| upside | hypothetical full ATM at 30.98 | 8.7925 | 717.768266 | 1,905.482 |

Future forward cash is discounted; full new share participation is counted now. ATM cases are hypothetical immediate financing at specified prices, not verified completed transactions. These are not probabilities or an independently defensible high/low valuation range.

## Base if-converted WACC-growth sensitivity

| WACC | Growth | Per share |
|---|---:|---:|
| 14% | 2% | 3.3432 |
| 14% | 3% | 3.3582 |
| 14% | 4% | 3.3761 |
| 16% | 2% | 2.9851 |
| 16% | 3% | 2.9853 |
| 16% | 4% | 2.9855 |
| 18% | 2% | 2.7550 |
| 18% | 3% | 2.7498 |
| 18% | 4% | 2.7439 |
| 20% | 2% | 2.6042 |
| 20% | 3% | 2.5976 |
| 20% | 4% | 2.5901 |

Continuing downside still fails funding; the separate downside-exit report values a conditional alternative. See the committee memo for WATCH/DEFER, with transaction scope unresolved. Known September option cash is already in cutoff cash; only remaining hypothetical exercise receipts appear above. Future financing proceeds and extra funding dilution from the conditional statements are not added on top of negative FCFF.

Full assumptions and limitations: docs/equity-bridge.md and data/equity_bridge_assumptions.json.
