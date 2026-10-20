# Integrated enterprise-to-equity bridge

Prepared October 19, 2026, using the September 10, 2026 close information boundary. This is a working standalone valuation and instrument-sensitivity step, not the completed committee recommendation. See [visible results](../outputs/equity-bridge.md), [machine-readable results](../outputs/equity-bridge.json) and [assumption/challenge record](../data/equity_bridge_assumptions.json).

## Numerator and denominator

Start with each scenario's operating EV and matching integrated cutoff cash. Add securities, deduct the 200 million operating-cash reserve, and deduct identified financial claims once. The other-debt/finance-lease/earn-out/fee/seller claims total 43.715696 million. Their payments are excluded from FCFF. Operating working-capital liabilities remain in operating forecasts; unpaid capex is already in forecast cash capex; neither is another bridge deduction. Operating leases remain an operating expense. Goodwill and operating intangible assets are not extra assets on top of DCF.

The reference assigns zero recovery to the separate customer-financing asset and zero capped-call credit. This is a deliberately conservative convention, not proof that either asset is worthless. Loan interest is excluded from FCFF, allowing a separate recovery sensitivity without duplicate operating income. Additional unverified ATM issuance and forward settlement are separate paired sensitivities. Known September exercise cash is already in cutoff cash. Only 3.703724 million of remaining hypothetical option exercise receipts is added; the share denominator counts remaining options once. Those receipts are treated as immediate for equity allocation, an approximation to the later assumed statement settlement. No future-year balance-sheet cash is added to present value.

Full vesting of existing RSUs and full exercise of remaining options produce 655.006167 million participating shares with note conversion, or 652.398422 million with notes retained. These are disclosed-population scenarios, not a verified September diluted count. Future compensation remains an economic operating cost, rather than free recurring SBC. Weighted-average option strike is a simplification, and existing option time value is not fully priced.

## Convertible branches

The [quarterly filing](https://www.sec.gov/Archives/edgar/data/1819994/000181999426000062/rklb-20260630.htm), Note 11, supplies the 4.25% coupon, semiannual schedule and February 2029 maturity. Note 6 provides a June fair value. The filing also describes conversion eligibility and settlement choices. Those terms do not establish conversion actually happened by our cutoff.

Four branches are visible:

- **If converted:** conversion shares participate; note debt deduction is zero. Base value is approximately $2.9853 and upside $6.7259. Base is below the approximately $5.13 principal conversion threshold, so this is a conditional illustration, not an automatic rational election at model value.
- **Retained, September-price parity diagnostic:** omit note shares and deduct 161.575880 million. This uses the dated share population and observed stock-price reference; it omits time value and is not a note quote.
- **Retained, stale June fair-value diagnostic:** omit note shares and deduct 280.789 million. This demonstrates sensitivity to an economic claim rather than automatically using principal; the date mismatch remains explicit.
- **Intrinsic-only diagnostic:** discount remaining scheduled coupons and principal at an assumed 6%, giving a 12.933957 million straight-debt floor. Jointly solve ordinary equity, remaining option intrinsic claims and the greater of note floor or conversion parity. Base retains the notes; upside converts. This deliberately omits option time value, detailed credit/settlement/make-whole terms and is **not a convertible fair-value model** or a substitute for a dated note quote.

All branches hold operating FCFF/WACC fixed to isolate claim allocation. They do not regenerate retained-note GAAP income statements: the linked statement reference assumes Q4 conversion. Since FCFF removes financing interest and financing-specific taxes, the operating cash flows do not directly depend on this allocation. A final financing policy may still change liquidity, WACC and investment capacity. Do not label these branches fully reforecast financing cases.

Negative residual equity is shown with its claim shortfall and a zero limited-liability common payoff, not silently treated as a healthy funded company. This is distinct from flooring operating EV: the negative strategy value remains in the numerator. The actual base/upside residual equity is positive.

## Paired instrument sensitivities

The filing's Note 12 supplies the forward share population and April 2028 proceeds interval. The MD&A supplies capped-call settlement timing and maximum payout. The [August 13 authorization](https://www.sec.gov/Archives/edgar/data/1819994/000175392626001463/g085846_8k.htm) anchors ATM capacity and commissions. These are contract/authorization facts, not verified cutoff receipts.

For forwards, discount future proceeds and add all participating settlement shares; do not discount the share count. April 30 is an assumed settlement date, not a verified tranche date. Exact settlement elections and adjustments remain open. For capped calls, discount a maximum-payoff scenario separately; that maximum is not guaranteed, especially in the weak operating case. No new shares accompany capped-call proceeds.

ATM scenarios pair hypothetical immediate net proceeds with gross proceeds divided by issue price. At issuance above modeled value, existing holders can benefit from a transfer from new investors; that is financing arithmetic, not better operating performance. Fees reduce value. No post-cutoff announcement is used to claim these proceeds were received. Tests verify that issuing at modeled fair value is neutral before fees and dilutive after fees.

Each row changes one assumption relative to the if-converted reference. Do not combine all favorable rows into an asserted confidence interval. The WACC/growth table is also conditional on that share/claim convention.

## Scope and next decision work

Pending Iridium is excluded consistently: no acquired operations, acquisition cash consideration, transaction issuance or undrawn bridge debt is added. Existing accrued fees still remain a claim. The historical market price may incorporate the transaction and other expectations that this standalone model omits. Therefore the large model/quote gap does not by itself prove an actionable mispricing.

The downside still requires outside funding and has no supported recovery/exit valuation. It has no fabricated price. Required next work: defensible downside treatment, peer policy and comparable values, market-implied expectations, and a conditional action/range with reversal triggers. The student must review assumptions and own the judgment. The student AI-off locked prediction and final cold run remain outstanding.

Development checks cover cash/claim settlement neutrality, known-versus-remaining option receipts, conversion exclusivity, fair-price issuance, forward timing, finite inputs, liquidity gates and equity/share reconciliation. None substitutes for external source verification or instrument pricing evidence.
