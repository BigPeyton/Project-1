# Downside and comparable-company review

Prepared October 19, 2026. Information cutoff: September 10, 2026 at 4 PM Eastern. Visible results: [downside exit](../outputs/downside-exit.md) and [comparables](../outputs/comparables.md). These are working analyses, not a completed committee recommendation.

## Downside has a real financing consequence

The original five-year downside remains unchanged and fails its 2030 funding requirement. Do not turn its conditional equity issuance into a free asset or a guaranteed financing solution. A separate orderly-exit scenario stops the same downside operations at December 2029, before new funding is required. The statement engine now supports an explicitly shortened horizon for this alternative; the standard project outputs still show all five years. Every pre-exit period matches the original downside, and no 2030 loss or financing flow is included in the exit valuation.

Forecast asset recoveries use explicit analyst haircuts: receivables 90%, contract assets 50%, inventory 40%, prepaids 10%, PP&E 30%, intangibles 5%, finance ROU assets 50%, restricted cash 100%; goodwill and other listed residual assets zero. All listed ordinary operating liabilities, customer advances, noncurrent operating leases and deferred tax liabilities are settled. Closure cost is 100 million. These are not appraised values, documented termination costs, legal priority estimates or management guidance. Restricted-cash release is a particularly conditional assumption.

Net operating exit recovery is approximately 58.687 million. Release the 200 million operating reserve excluded from the cutoff equity bridge once at exit. Cash/securities and separate financial receivables are not recovered a second time. Financial claims remain deducted in the equity bridge; their remaining balances enter the separate liquidity sufficiency check, not a duplicate value deduction. The assumed exit can cover the modeled obligations without new financing; raising closure cost to 1,000 million causes an explicit failure rather than a fabricated healthy recovery.

The resulting cutoff FCFF strategy value is -1,315.811 million, giving an if-converted/full-option-exercise illustration of $0.9682/share. That value is below the option strike and note conversion threshold. The intrinsic-only allocation diagnostic instead leaves the notes outstanding and options unexercised, giving $0.9515/share. Neither includes detailed instrument time value. This is not an observed liquidation distribution or guaranteed minimum. Discounted operating strategy value and undiscounted exit liquidity answer different questions; cash returns, taxes and discounting conventions prevent treating the liquidity check as the valuation numerator. A legal/timing-specific cash distribution analysis would be a separate method.

PPE recovery of 10% rather than 30%, and closure cost of 250 rather than 100 million, each lower value in executable tests. An earlier intervention could preserve value; a delayed, forced exit could destroy more. The downside is a conditional capital-allocation failure case, not a forecast of bankruptcy. Decision implication: without credible financing or a supported restructuring plan, deteriorating execution supports do-not-initiate rather than assuming distant growth solves liquidity.

## Peer policy and evidence dates

The [peer policy](peer-policy.md) was saved before the numerical refresh. It retains the Lab 8 candidates, Redwire and Avio, with business qualifications. The final project adds EV/revenue and equity/revenue to the original P/E exercise because negative target earnings still prevent a meaningful P/E-derived price. No peer was added to move the result toward the stock quote.

Redwire's [2025 filing](https://www.sec.gov/Archives/edgar/data/1819810/000181981026000029/rdw-20251231.htm) supplies annual revenue/operating earnings. Its [June 2026 filing](https://www.sec.gov/Archives/edgar/data/1819810/000181981026000124/rdw-20260630.htm), filed August 6, supplies debt, cash, leases and the August 3 share count. Principal debt is used rather than its net amount after issuance costs. These are dated proxies, not a complete September financing roll-forward. Edge Autonomy's partial-year inclusion and acquisition charges materially limit comparability.

Avio's [annual report](https://avio-data.teleborsa.it/2026%2FAvio-2025-Annual-Report_20260331_093610.pdf) supplies consolidated revenue of 583.690 million euros and reported EBIT of 11.966 million. Its lower net-of-pass-through revenue and adjusted EBIT are deliberately not substituted. Its [July 31 notice](https://www.emarketstorage.it/sites/default/files/comunicati/2026-07/20260731_187680.pdf) provides issued shares and treasury shares, giving 46.162614 million circulating shares.

The [September 10 results release](https://www.emarketstorage.it/sites/default/files/comunicati/2026-09/20260910_188984.pdf) carries a 16:45:23 Milan dissemination time, equivalent to 10:45:23 Eastern, before our cutoff. Use its June balance sheet and net-financial-position reconciliation. Its current/noncurrent lease amounts are separated from financial debt and NCI. Book NCI is a proxy. Pending Advent issuance/proceeds are excluded together, consistent with the pre-cutoff announcement; a later closing is not a cutoff fact.

Historical local closes, independently reopened during this refresh: [Redwire](https://stockanalysis.com/stocks/rdw/history/) and [Avio](https://stockanalysis.com/quote/bit/AVIO/history/). Local closes share a date, not an identical instant. Each ratio pairs price, financial amounts and share units in its own currency. Currency conversion is unnecessary for these dimensionless multiples.

## Matched definitions and qualifications

Before calculation, the numerical mapping explicitly adopted **EV including all lease liabilities**, accommodating US GAAP and IFRS classifications. EV adds identified debt/noncommon claims, NCI and leases, and deducts unrestricted cash/liquid investments. Ordinary operating payables/customer advances are not debt additions. Gross borrowing/principal, book lease claims and book NCI are transparent proxies; no provider EV label is silently reused.

Target DCF keeps operating leases in operating costs. To map lease-inclusive peer EV into the existing target bridge, subtract target operating lease claims once. June noncurrent claims are 104.378 million; current claims use a 10.816 million year-end balance carried forward as a proxy, grounded in [Rocket Lab's annual Note 16](https://www.sec.gov/Archives/edgar/data/1819994/000181999426000013/rklb-20251231.htm). This is not a reported September current balance. A +/-5 million sensitivity is retained in the JSON. Finance leases remain in the ordinary target equity bridge and are not deducted twice. The translation does not make all lease economics identical.

P/S is already an equity multiple: multiply by target revenue and divide by its issued common-equivalent population, including participating preferred. Do not add target cash or subtract debt again. Its basic-equivalent denominator differs from the full-award if-converted EV bridge. The labels preserve that difference. Unvested awards and options are not fully priced in peer market equity.

Full cash subtraction may be aggressive where advances fund operations. The outputs separately halve the peer cash deduction to reveal this sensitivity. That test does not assert cash is legally restricted. Avio's minority investments and differing pass-through/development accounting add limitations. Both companies have financing/capital-structure uncertainty. These caveats qualify numerical usefulness; they cannot be erased by a median.

## Results and method disagreement

RDW: EV/revenue 6.715x and P/S 8.102x. AVIO: EV/revenue 1.316x and P/S 2.215x. Applied consistently as described, the EV method gives target illustrations of $4.18-$9.14/share; P/S gives $2.08-$7.62 on its different share/capital basis. These endpoints are individual qualified peer indications, not confidence bounds. Removing either peer leaves one indication and removes any cross-peer range.

DCF explicitly charges for losses and reinvestment before distant cash generation. Sales multiples embed what investors expect for each peer's future margins, growth and financing, and apply those expectations to a historical denominator. P/S does not separately recognize Rocket Lab's net cash; EV does. These differences explain why outputs disagree. **Do not mechanically average them.**

The reported operating margins are roughly -68.5% for Redwire and 2.1% for Avio; company-specific charges and presentation conventions matter. They do not independently support a repeatable 12%-20% mature consolidated margin for Rocket Lab. Those terminal assumptions remain ambitious analyst judgments needing operational evidence and stress, not peer-validated facts.

No transaction multiple is used. Pending Iridium and other acquisition references lack the matched standalone financial, control/synergy and time basis needed here. This is an explicit exclusion, not an assertion that acquisition history is irrelevant.

## Validation and next step

All 80 development tests pass. New tests cover truncation without funding, exit solvency failure, recovery/closure direction, reserve and claim counting, currency scaling, time-zone cutoff, treasury-share exclusion, fiscal-period consistency, leave-one-peer-out dependence, equity/EV definitions and peer cash sensitivity. No recorded student prediction or partner feedback is invented.

Next: calculate market-implied expectations/reverse DCF, stress the weak long-term assumptions and assemble a provisional conditional decision range with monitoring/reversal triggers. Student ownership, the AI-off locked changed-input record, final cold run, documents and recordings still remain.
