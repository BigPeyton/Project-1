# Estimated September cash: method and limits

Cutoff: September 10, 2026. This step estimates standalone liquidity; it does not create a complete estimated balance sheet or final equity valuation.

## Evidence and assumptions

Reported facts are in `data/reported_financials.json`; judgments are in `data/cash_bridge_assumptions.json`. The June 10-Q, filed August 10, provides the opening cash, investments, operating cash flow and capex. Page 8 reports $0.149 million of H1 finance-lease principal payments. Note 5 gives investment fair values and maturities. Source: https://www.sec.gov/Archives/edgar/data/1819994/000181999426000062/rklb-20260630.htm

Reference method: spread H1 operating cash use plus cash capex over 181 days and apply that rate to the 72 days after June 30. Add prorated lease principal payments and the verified September 2 option exercise receipt. Hold investment fair value constant. Assume no other unverified cash movement in the reference case; this is not a claim that no movement occurred. H1 CFO already includes interest, taxes and operating lease payments, so these are not added again.

Estimated cash is $2,054.985 million. Adding $258.105 million investments gives $2,313.090 million. Subtracting the provisional $200 million operating reserve leaves $2,113.090 million before other claims. Restricted cash is already outside the starting cash line and is not subtracted again.

The reserve is an analyst judgment, approximately 2.6 months of an H1 cash expense proxy (COGS + R&D + SG&A - D&A - SBC). That proxy does not capture working-capital, capex or acquisition needs. Test $100-300 million reserves, 0.5-1.5 times historical cash use and a 0-2% investment haircut. The resulting $1,970.632-2,250.387 million range is scenario analysis, not a confidence interval.

## Financing and acquisition boundaries

ATM authorizations, undrawn commitments, unsettled forwards and future option receipts are not cash received. Separate hypothetical ATM completion cases pair net proceeds with newly issued shares at $61.96, using the disclosed maximum 2% sales commission. Other fees are unquantified. This reference price is an assumption, not a reported issuance price. See `docs/share-count-and-debt.md` for sources and limitations.

Only $0.15277113 million of the full-exercise option proceeds is credited in current estimated cash. The remaining hypothetical amount is $3.70372408 million; adding the entire option-proceeds amount again would double count the known receipt.

Pending Iridium funding means standalone liquidity is not automatically distributable surplus. A transaction case must include acquired operations, consideration, debt and financing consistently. Capped calls are not current cash: the June filing's MD&A discusses potential future settlement receipts, which must be evaluated separately from the cash balance and the remaining notes.

## Integration required next

- Verify debt, lease claims, contingent consideration and other non-operating claims before the equity bridge.
- Reconcile this provisional cash estimate with the linked pro-forma. Do not insert it into June balances and plug equity to force balance.
- Value only cash flows after the valuation cutoff. Spending already deducted here must not also be discounted as future FCFF.
- Keep the operating reserve treatment consistent with working capital and terminal value; avoid counting the same reserve twice.
- Review normalization and forecast drivers next. The August 10 earnings release contains Q3 guidance, which is management's forecast, not actual results or a cash-flow forecast: https://www.sec.gov/Archives/edgar/data/1819994/000181999426000061/rklb-08102026ex991.htm

## Verification

Run `python -B -m unittest discover -s tests -v`. Six tests passed October 19: opening cash/restriction definitions, cash-security transfer conservation, paired financing proceeds/shares, no duplicate option receipts, lower liquidity under stress, and rejection of invalid/unfunded inputs. These are AI-assisted mechanical checks, not the student's locked independent exercise or final cold run.

Run `python src/cash_bridge.py` to inspect results, or add `--write` to export Markdown and JSON. The saved Markdown was generated from the successful execution. No final financial-model output or investment recommendation has been produced.
# Integration update — October 19

The later [linked statement model](three-statements.md) now provides the working cutoff cash estimate used with its FCFF forecasts: base $2,043.230454 million. The historical-rate interpolation below is preserved as a development diagnostic and must not be combined with the newer forecast as though it were the same opening state.

