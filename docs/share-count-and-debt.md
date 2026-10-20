# Share-count and convertible-debt decision

Prepared October 19, using the September 10, 2026 information cutoff. This is a working modeling convention, not a verified exact September 10 capitalization.

## Starting point

The August 13 prospectus provides a newer, coherent August 7 common/preferred/award schedule than the June comparison used in Lab 10. Source: [424B5, Dilution, S-23](https://www.sec.gov/Archives/edgar/data/1819994/000175392626001459/g085845_424b5.htm).

| Component | Millions of shares | Basis |
|---|---:|---|
| Common outstanding | 598.459739 | August 7 reported count |
| Participating preferred, as converted | 40.951250 | August 7 disclosed conversion shares |
| Existing RSUs | 9.449364 | Assume all disclosed awards vest |
| Existing options | 3.538069 | Full exercise scenario; $1.09 weighted-average strike |
| Remaining convertible-note shares | 2.607745 | June 25 schedule carried forward as an explicitly dated proxy |
| **Working full-conversion scenario** | **655.006167** | Excludes separate forwards, ATM and acquisition scenarios |

The note share count is corroborated by the [August 26 merger prospectus, Annex A section 5.05(a)](https://www.sec.gov/Archives/edgar/data/1819994/000175392626001639/g085904_424b3.htm). Its publication date does not make its June measurement current.

## Consistent alternatives for the model

- **Converted notes:** 655.006167 million scenario shares; zero deduction for the converted notes. Other debts and claims still need separate treatment.
- **Notes retained:** 652.398422 million scenario shares; deduct a separately specified economic note claim. Corrected in the subsequent claims review: $13.366 million principal is not an acceptable current market-value proxy. Note 6 reports June fair value of $280.789 million; this is also not a September quote. See `claims-treatment.md` for dated diagnostics.
- Full exercise provides $3.85649521 million gross proceeds across the disclosed option population. Credit those proceeds once when using full option shares. Do not also apply the treasury-stock method. If intrinsic value is below the exercise price, use an unexercised branch instead; exercise cannot be justified only by the observed market quote.
- Include preferred participation once in shares; do not also deduct it as a separate preferred claim. Neither scenario is a GAAP weighted-average diluted EPS denominator.

The September 4 [Form 4](https://investors.rocketlabcorp.com/node/13271/html) reports a September 2 exercise of 140,157 options at $1.09. Within the full-exercise scenario, this transfers 140,157 shares from options to common, leaving the combined total unchanged. Cash received is $152,771.13 and reduces remaining hypothetical exercise proceeds by the same amount. Secondary sales of those shares do not add shares or corporate cash. Other award movements have not been exhaustively rolled forward.

## Financing uncertainty stays visible

The SEC submissions index returned 29 filings dated August 1 through September 10. Selected relevant documents reviewed: the August 10 10-Q, August 13 capital-raising prospectus and two 8-Ks, August 24 S-4/A, August 26 final merger prospectus, and September 4 option-exercise Form 4. This establishes the reviewed scope, not a claim to have read every document.

The [August 13 financing 8-K](https://www.sec.gov/Archives/edgar/data/1819994/000175392626001463/g085846_8k.htm) permits up to $1.944369826 billion gross issuance with sales commissions up to 2%. Authorization does not establish sales or cash received by September 10. Use paired cash/share sensitivity cases, not a cash-only addition. Do not use the later September 15 completion report to backfill the cutoff.

The earlier 7.4512 million-share collared forward population is separately disclosed in the June 10-Q; no associated proceeds were received in H1. Settlement must pair the relevant shares with discounted net proceeds under its terms. Do not silently omit it from the final analysis or treat borrowed hedge shares as newly issued company shares.

Iridium was still pending in the reviewed pre-cutoff filings. Any transaction case must include acquired operations, consideration cash, debt and new shares together. A standalone case must identify that exclusion and qualify comparison with a market price reflecting transaction expectations.

Unissued plan reserves are excluded from existing dilution. Existing award vesting, future SBC economics, capped calls and unobserved financing remain explicit limitations/sensitivities. No capped-call asset credit has been assumed at this stage.

## Next step

Reconcile the June balance sheet into a documented September opening estimate: cash burn, known financing, restricted/operating cash, investments and debt/lease claims. Preserve the reported balance sheet separately from estimates. Then normalize historical operating results and choose the forecast drivers. No final valuation is produced by this share-count step.
