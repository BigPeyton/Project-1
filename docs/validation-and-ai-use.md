# Validation and AI use — working record

Prepared October 19, 2026. This repository source is rendered in the review copy of Validation-and-AI-Use.pdf; it is not a final frozen submission. Student-only evidence and the recorded cold run are still missing. Mechanical test success is not proof that the finance assumptions are true.

## Decision, version and information boundary

User: buy-side portfolio manager with no existing RKLB position. Action: WATCH/DEFER at the September 10, 2026 close of $61.96. Peyton reviewed and adopted the AI-assisted rationale on October 19. Proposed horizon: three to five years. See [committee rationale](committee-decision.md).

All valuation facts must have been available by September 10, 2026, 4 PM Eastern. Research/coding performed later does not authorize later financial information. Dated original Edition A is preserved unchanged; its AI-assistance history is disclosed rather than relabeled AI-off. No original Brightspace receipt has been verified.

The latest [development audit](../outputs/development-validation.md) records actual run time, elapsed seconds, environment, test names, first unexpected failure in that run and source/data/test hashes. Its [JSON](../outputs/development-validation.json) contains the full file hash map. This identifies the tested code/data snapshot, not a final repository commit or hash of every submission artifact. Final commit/tag and frozen document hashes: **pending**.

## Material data and convention ledger

Full raw values and source locators remain in the linked data records; USD millions unless indicated otherwise. Forecasts are analyst assumptions, not issuer facts.

| Input | Source / as-of and availability | Definition and transformation | Exclusion / principal risk |
|---|---|---|---|
| FY2025 revenue 601.799; EBIT -228.838 | [reported inputs](../data/reported_financials.json), K25; Dec 31, 2025, filed Feb 26, 2026 | Raw thousands divided by 1,000; reported annual consolidated operations | Acquired scope is not organic growth; no arbitrary base-year addback |
| H1 2026 revenue 434.414; CFO -134.407 | Same ledger, Q26; June 30, filed Aug 10 | Six months, not annual; cash-flow cash includes restricted cash | Do not value pre-cutoff cash flow again |
| H1 D&A 35.933 | Q26 cash-flow statement, June 30 / Aug 10; [normalization](../data/normalization.json) | Aggregate depreciation AND amortization; not depreciation alone | No second expense deduction or mismatched addback |
| H1 cancellation charge 11.180 | Q26 Note 13; June 30 / Aug 10 | Separate run-rate normalization; remove expense and its noncash addback together | Does not create cash; ordinary compensation remains a cost |
| Quote 61.96 USD/share | [reported inputs](../data/reported_financials.json), September 10 historical Close | Cutoff reference, not the provider's current header quote | Retrieved later; original downloaded quote snapshot absent |
| Cash/securities and financial claims | [statements](../data/statement_assumptions.json), [claims](../data/claims.json), [bridge](../data/equity_bridge_assumptions.json) | June facts rolled to a modeled September cutoff; $200m operating reserve; claims deducted once | Cutoff cash is estimated; recovery and timing uncertain |
| Participating shares and instruments | [capitalization](../data/capitalization.json), August 7 schedule published August 13 plus known pre-cutoff exercise | Actual shares / 1m; converted/full-award scenario 655.006167m; retained notes use separate denominator and claim | No asserted exact September cap table; optional proceeds paired with shares |
| Five-year forecast | [revenue](../data/revenue_assumptions.json), [operations](../data/operating_assumptions.json), [statements](../data/statement_assumptions.json) | Company-specific drivers; reported H1 plus forecast H2; dated source and challenge records | Neutron cadence, margin, R&D, reinvestment and funding are uncertain |
| WACC and terminal assumptions | [valuation inputs](../data/valuation_assumptions.json) | 16% selected WACC, 3% terminal growth; dated Treasury/ERP and archived beta; growth investment charged | Beta not independently replicated; long-term margins/ROIC are analyst judgments |
| RDW/Avio comparison | [peer inputs](../data/peer_inputs.json), [policy](peer-policy.md) | September 10 quotes, FY2025 revenue, lease-consistent EV/revenue and separate equity P/S | Different currency units kept within each ratio; heterogeneous scope; two peers insufficient for statistical range |
| Downside recovery | [exit inputs](../data/downside_exit_assumptions.json) | Conditional 2029 orderly exit, explicit haircuts and closure costs | Not an appraisal, guaranteed floor or legal insolvency waterfall |

Pending Iridium operations, consideration and associated financing are excluded together. Optional forward/ATM/capped-call and customer-financing outcomes are separate sensitivities. A standalone gap to the observed quote does not settle the combined-company valuation.

## Independent source/definition check and AI-output disposition

**AI output checked:** the model's claim that removing the identified cancellation charge improves the analytical earnings view without improving historical cash flow. **Independent evidence:** Rocket Lab's [June 2026 Form 10-Q](https://www.sec.gov/Archives/edgar/data/1819994/000181999426000062/rklb-20260630.htm), Note 13 and the six-month cash-flow statement, re-opened October 19. Note 13 identifies the 11.180m one-time SBC expense. The cash-flow statement reports total SBC 47.677m, aggregate D&A 35.933m and CFO -134.407m. These are pre-cutoff disclosures; no subsequent outcome is used.

**Disposition: accept with qualification.** Removing 11.180m from expense and the corresponding noncash addback leaves CFO unchanged. The filing supports the accounting treatment, not a lasting spending reduction: reallocated R&D or replacement compensation could offset the benefit. Normalization tests preserve raw data and reconcile the result. Decision effect: no invented cash or equity-value benefit from a noncash presentation change. This is an AI-assisted external-source check.

## Validation register

| Claim / risk | Test and expected behavior | Actual evidence / disposition | Decision implication |
|---|---|---|---|
| DCF arithmetic | Twelve published Lab 5 training answers against shared valuation helpers | test_valuation.py, test_official_lab05_known_answer; PASS in latest audit | Supports arithmetic only; does not validate RKLB assumptions |
| Input definitions / normalization | Filing cross-check above; no cash created by noncash expense removal | test_normalization.py; PASS; D&A and CFO checked to filing | Prevents overstated cash and false normalization benefit |
| Statement integrity | Filing/opening reconciliation, annual and interim balance/cash/equity checks; corrupted data rejected | test_three_statements.py; PASS | Broken articulation stops the result |
| Funding failure, highest-risk development probe | Run original continuing downside without assumed equity | Stops in 2030: approximately 314.688m additional net funding needed; captured in audit | Unsupported continuation cannot justify initiation; alternative exit is conditional |
| DCF boundaries / direction | Invalid growth/rate rejected; continuity; WACC direction on tested domain; growth direction tied to returns | test_valuation.py; PASS | More growth is not automatically more value; reinvestment matters |
| Equity allocation | Cash/claims/shares reconcile; reject double-counted note claims and unpaired financing | test_equity_bridge.py; PASS | Reference conversion is conditional; claim sensitivities remain material |
| Peer definitions | Dates, currency/period consistency, treasury shares, lease-inclusive EV and P/S bridge checks | test_downside_and_comparables.py; PASS | Do not average conflicting methods or manufacture meaningful P/E |
| Market-implied expectation | Known-answer inverse algebra and quote round trip; no extrapolated unbracketed root | test_reverse_dcf.py; PASS | Current paths do not support the cutoff price; missing scope remains a limitation |
| Application controls | Engine equality; changed WACC then reset; invalid/nonfinite/duplicate inputs; no stale output; downside fails | test_app.py; PASS | Demonstration uses the same financial engine, not hand-coded display values |
| Own-pro-forma driver attribution | Four one-at-a-time 2027-2030 drivers; same base; compare EBIT, FCFF and value ranks under two range sets | test_proforma_sensitivity.py; PASS; standard: space growth first; alternative: R&D first | Importance depends on the selected ranges; cost-only savings are not implementable advice |
| Reproduction | Recompute six saved valuation/sensitivity reports and compare JSON and Markdown exactly | Latest development audit records each result | Current saved outputs match code; not a recorded cold run |
| Human locked changed input | Human prediction and precommit BEFORE fresh execution, AI closed during both | **PENDING**; [blank record](locked-changed-input-record.md) | Cannot be replaced by any AI-assisted test above |
| Recorded cold run | Fresh environment, README only, preserve first failure and elapsed time | **PENDING**; [protocol](cold-run-protocol.md) | Final reproduction/readiness evidence still required |

The suite now contains 105 tests, including live HTTP export/error/recovery and seven new operating-driver tests. [Reverse-DCF development failures](reverse-dcf-validation.md) retain the earlier rendering error and permission issue; the latest successful run does not erase them. No test failure is silently rewritten as a pass. Model-invalid input and expected funding rejection are successful guard checks, not unexpected test failures. No browser surface was available for an automated visual preview; HTTP and HTML-content checks do not claim visual inspection.

Pre-recording course review identified a previously incomplete requirement: explicit one-way operating sensitivities and range-dependent rankings. This was corrected with four bounded 2027-2030 controls, two declared range sets, same-base comparisons and outputs/proforma-sensitivity.md/.json. Standard ranges: space growth +/-5pp, space margin +/-3pp, R&D 90%-110% and Neutron recognition 50%-150%. Alternative: +/-2.5pp, +/-1.5pp, R&D 80%-120% and Neutron 90%-110%. These are justified analyst stress choices, not historical confidence bands or company guidance. Source/challenge/change-evidence records are in data/proforma_sensitivity_assumptions.json. Baseline valuation is unchanged.

**Unrecorded fresh-environment development check:** October 19, 22:02:34-22:02:50 UTC, CPython 3.13.15 on this Windows computer, fresh project copy and new virtual environment. The README setup/audit commands passed, followed by live base/R&D-change/invalid/reset checks. Measured total 15.973 seconds; no unexpected failure. Full environment/command output: outputs/pre-recording-clean-run.json. This was assistant-executed and unrecorded, so it does not complete the required recorded cold run. All 19 archived originals also matched their inventory hashes during review.

Application-stage environment record: the first attempt to save the development audit was blocked by a workspace PermissionError on outputs/development-validation.json. An authorized rerun saved it. The subsequent saved audit reports its own measured elapsed time and no unexpected failure in that run; it does not erase this earlier write failure. The running app's base/change/reset, boundary rejection, downside rejection, evidence links and JSON download were also checked over HTTP on port 8765. No recording or visual inspection is inferred from those requests.

## Named AI-use register

### Student-reported application walkthrough

Subsequent assistant-run rehearsal: [ai-assisted-practice-record.md](ai-assisted-practice-record.md) preserves the known WACC example, AI-authored expectation, actual results/timing and decision interpretation. This is supplementary AI-assisted evidence only; it is excluded from the human locked-record requirement. The student requested to repeat it for verification, but completion of that subsequent repetition has not been reported.

On October 19, Peyton reported opening the application and observing $2.99/share at 16% WACC; changing WACC to 18% and recalculating displayed $2.75; reset restored 16% and $2.99. The invalid-boundary button displayed the growth-below-WACC error with no valuation, and a second reset recovered the base. Peyton reported that the application looked good. The assistant subsequently rechecked the same results and rejection/recovery over live HTTP. Visual confirmation is attributed to Peyton, not an assistant browser inspection. This was an AI-guided practice walkthrough, with no recording or independently precommitted prediction claimed. It does not fulfill the locked exercise or recorded cold run.

| Tool / exposed model | Date | Material task / output | Independent check | Disposition / decision effect |
|---|---|---|---|---|
| OpenAI Codex; exact historical backend model/version not verified | Earlier labs; dates in archive/history | Edition A and reusable research/model code | Original files/hash inventory; later filing and architecture review | Preserve originals and disclose assistance; do not label A independently AI-off |
| OpenAI Codex; exact runtime model identifier not exposed in project evidence | Oct 19, 2026 | Financial-source extraction and normalization | SEC filing tables / Note 13, arithmetic, raw-data preservation | Accept or qualify field by field; cancellation does not create cash |
| Same | Oct 19 | Statements, DCF, claims, peers, reverse DCF and tests | Published Lab 5 known answers, filing comparisons, cross-method challenges | Use with limitations; tests alone do not independently prove forecasts |
| Same | Oct 19 | Proposed WATCH/DEFER rationale and drafting | Evidence review; Peyton explicitly adopted rationale in conversation | Adopted student judgment after AI-assisted drafting; no claim of unaided authorship |
| Same | Oct 19 | Local application and validation documentation | Engine/report equality, input/failure/reset tests, live HTTP smoke checks | Accept software workflow after checks; browser visual review and recorded demo remain separate |

The user discussed Astra/high settings, but a preference or requested setting is not proof of an exact backend model/version. Do not invent that identifier. External sources are independent evidence; a second AI agreement is not validation. No simulated partner feedback is presented as real peer feedback. The archived AI-written prediction drafts are ineligible for the new human locked record.

## Limitations and must-fix items

Highest economic uncertainty: transaction scope, commercially achieved cash flows, mature profitability/returns, funding and security claims. They drive the conditional action in the committee rationale. Monitor reported execution, liquidity relative to the $200m reserve and funding commitments; revisit the recommendation when the stated evidence changes.

Before submission: complete the independent locked exercise; record the fresh-environment cold run; review source/capitalization limitations; prepare and inspect final PDFs; record three actual videos and correct their transcripts; complete the manifest and access checks; freeze versions and preserve the Brightspace receipt. No upload or submission is implied by this record.

## Retained changed-input rehearsal - AI-assisted, known result

Peyton elected to retain this rehearsal as disclosed. It is supplementary validation, not fulfillment of the human AI-off locked-record requirement. The full practice source is docs/ai-assisted-practice-record.md. No repository precommit, independent prediction, unaided execution or subsequent student repetition is asserted.

| Field | Preserved rehearsal evidence |
|---|---|
| Author and prior knowledge | AI assistant; result already known from earlier walkthrough |
| Material input / old to new | WACC 16% to 18%, increase of two percentage points |
| Held fixed | Base scenario; terminal growth 3%; mature EBIT margin 12%; marginal ROIC 16%; converted/full-award bridge, 655.006167m shares |
| AI-authored expectation | Conditional value decreases on the already-tested interval; no global monotonicity assertion for signed cash flows |
| Expected decision effect | WATCH/DEFER remains at the $61.96 cutoff price; a lower value does not resolve funding/transaction limitations |
| Precommit | None. Expectation was in the execution script, not independently locked by the student |
| Execution | Live application HTTP requests: base, WACC 18%, base reset |
| Start / finish UTC | 2026-10-19T21:32:54.073530+00:00 / 2026-10-19T21:32:54.193796+00:00 |
| Elapsed time | 0.120668 seconds for requests/checks only, excluding preparation; not cold-run timing |
| Before / after price | 2.985305156470462 to 2.749821860661706 USD/share; decrease of 0.2354832958087556 or 7.888081233449795% |
| Before / after operating EV | -105.93019493130856 to -260.1732059115289 USD millions |
| Reconciliation and failure | Direction matches known expectation; reset exactly restores base; no unexpected HTTP failure; bridge residual zero |
| Actual decision interpretation | Assistant retains WATCH/DEFER because value weakens further; unchanged on-screen reference label alone is not evidence of a reasoned committee decision |

The separate locked exercise and recorded cold run remain pending. This record preserves actual provenance rather than relabeling the rehearsal as independent work.
