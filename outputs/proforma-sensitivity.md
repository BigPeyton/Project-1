# Own-pro-forma one-way sensitivities

AI-assisted analyst stress ranges, not issuer guidance, historical confidence bands or the human locked exercise

For each range set, change one driver at a time around the same base. Rank by absolute high-to-low outcome span separately for 2030 EBIT, 2030 FCFF and conditional USD/share. No probabilities, unit-comparable elasticities or universal importance claim.

All runs use the same base, WACC 16%, growth 3%, mature margin 12%, marginal return 16% and converted/full-award bridge. Only the named 2027-2030 operating path changes. Historical facts and 2026 remain unchanged. These are not independent student predictions.

| Base metric | Value |
|---|---:|
| ebit_2030 | 106.793313 |
| fcff_2030 | -102.064823 |
| price | 2.985305 |

## Standard ranges

| Driver / endpoint | 2030 EBIT (USD m) | 2030 FCFF (USD m) | USD/share |
|---|---:|---:|---:|
| Space-systems growth shift -5 | 37.099 | -143.360 | 2.5804 |
| Space-systems growth shift 5 | 185.772 | -56.092 | 3.4289 |
| Space-systems gross-margin shift -3 | 60.780 | -137.111 | 2.7212 |
| Space-systems gross-margin shift 3 | 152.807 | -67.019 | 3.2455 |
| R&D spending scale 90 | 145.793 | -72.815 | 3.2236 |
| R&D spending scale 110 | 67.793 | -131.315 | 2.7438 |
| Neutron recognized-revenue scale 50 | 39.293 | -140.379 | 2.5979 |
| Neutron recognized-revenue scale 150 | 174.293 | -63.751 | 3.3567 |

Largest to smallest absolute endpoint spread:
- ebit_2030: space_growth > neutron_scale > space_margin > rd_scale
- fcff_2030: space_growth > neutron_scale > space_margin > rd_scale
- price: space_growth > neutron_scale > space_margin > rd_scale

## Alternative ranges

| Driver / endpoint | 2030 EBIT (USD m) | 2030 FCFF (USD m) | USD/share |
|---|---:|---:|---:|
| Space-systems growth shift -2.5 | 70.834 | -123.277 | 2.7775 |
| Space-systems growth shift 2.5 | 145.074 | -79.684 | 3.2042 |
| Space-systems gross-margin shift -1.5 | 83.787 | -119.588 | 2.8533 |
| Space-systems gross-margin shift 1.5 | 129.800 | -84.542 | 3.1173 |
| R&D spending scale 80 | 184.793 | -43.565 | 3.4563 |
| R&D spending scale 120 | 28.793 | -160.565 | 2.5023 |
| Neutron recognized-revenue scale 90 | 93.293 | -109.728 | 2.9092 |
| Neutron recognized-revenue scale 110 | 120.293 | -94.402 | 3.0608 |

Largest to smallest absolute endpoint spread:
- ebit_2030: rd_scale > space_growth > space_margin > neutron_scale
- fcff_2030: rd_scale > space_growth > space_margin > neutron_scale
- price: rd_scale > space_growth > space_margin > neutron_scale

## Interpretation and bounds

Importance is conditional on both the output metric and the selected shock sizes. The alternative narrows growth/margin/Neutron uncertainty while widening R&D uncertainty; compare the displayed ranks instead of calling any one driver universally dominant. None of these isolated stresses warrants initiation at $61.96. Cost reductions with revenue held fixed are attribution tests, not implementable cost-cutting advice. Combined scenarios remain necessary for correlated delays, capex and funding risks.

### Space-systems growth shift
- Units: percentage points added to each 2027-2030 rate.
- Basis: Base growth 25/22/18/15%; +/-5 points is a bounded interior challenge relative to the wider combined scenario paths in revenue_assumptions.json. Backlog does not validate these rates.
- Causal link: Revenue changes segment profit, revenue-linked SG&A and working capital; 2030 sales/margin/capital anchors then affect the long-term DCF.
- Challenge: Compounding amplifies a repeated rate shift; revenue timing may be correlated with margin/capacity.
- Change evidence: Dated delivery acceptance, funded order conversion and capacity evidence.

### Space-systems gross-margin shift
- Units: percentage points added to each 2027-2030 margin.
- Basis: Base margins 34/35/36/37%; +/-3 points challenges utilization/mix within the broader scenario envelope. These are analyst bounds, not a demonstrated historical band.
- Causal link: Gross profit changes EBIT, operating taxes, cost-linked working capital and FCFF, then the transition anchor.
- Challenge: A margin shift changes production costs and associated inventory/liabilities, not just EBIT.
- Change evidence: Repeatable segment unit costs, product mix and program cost-to-complete revisions.

### R&D spending scale
- Units: percent of selected 2027-2030 dollar path.
- Basis: Base spending 350/360/375/390m; standard +/-10% tests budget variance. Alternative +/-20% deliberately stresses a larger overrun/reallocation, not management guidance.
- Causal link: Expense changes EBIT and cash taxes/FCFF; earnings retained in cash/equity; revenue is deliberately fixed for attribution.
- Challenge: Holding revenue fixed isolates cost exposure; cutting R&D could impair future products. A cost-only saving is not an implementable recommendation.
- Change evidence: Engineering staffing, technical milestones, grants and credible program budgets.

### Neutron recognized-revenue scale
- Units: percent of selected 2027-2030 revenue-equivalent path.
- Basis: Base recognition-equivalents 1/3/6/10 at $50m each; +/-50% reflects weakly evidenced commercialization, within the broad low/high scenario envelope. Narrow +/-10% is a comparison assumption, not evidence that uncertainty is small.
- Causal link: Revenue and contribution rise/fall while fixed development/commercial costs remain; SG&A and working capital respond, affecting EBIT, FCFF and value.
- Challenge: Fractional equivalents are revenue-recognition units, not launch counts. Fixed R&D/commercial overhead/capex stay in place; capacity interactions require combined scenarios.
- Change evidence: Qualified hardware, reliable cadence and signed contract recognition schedules.

Valuation control bounds: WACC 3%-30%, terminal growth 0%-8%, mature margin 4%-40%, marginal return 5%-40% are broad diagnostic limits, not empirical historical bands. Require growth below both WACC and return; funding/continuity checks remain locked. Reference underwriting uses the narrower documented WACC 14%-20% and growth 2%-4% grid.
