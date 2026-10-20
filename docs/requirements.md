# Requirements and reuse checklist

Status as of October 19, 2026 pre-recording review: financial model, adopted conditional rationale, operating-driver application and review PDFs exist. 105 tests pass; six saved reports reproduce; an unrecorded fresh-copy/venv check also passes. The own-pro-forma range-ranking gap was corrected. Independent locked exercise, recorded cold run, videos/transcripts, final publication/access and receipt remain incomplete. See pre-recording-review.md for findings. Historical labs and AI-assisted rehearsals are not automatic fulfillment of final independent evidence.

Authority: the student's pasted Brightspace assignment, 300-point analytic rubric, and subsequent Edition A email; the course repository's Project 1 brief, submission architecture, checklist, and relevant lab instructions. Course snapshot: `../../fin439_repo_audit/FIN43900-Fall2026-main/`.

| Requirement | Related prior work | Final work / evidence needed | Status |
|---|---|---|---|
| Buy-side user, no existing position, horizon, target/security, action and constraints | Labs 3, 4, 12 | Explicit decision scope; valuation date, currency and share basis | Adopted rationale and memo specify mandate/horizon/cutoff/share basis; fund sizing and margin-of-safety limits remain committee conditions |
| Edition A unchanged; Edition B and evolution table | Original Edition A found | Preserve original; separate accurate provenance note; write Edition B from verified analysis | Original archived/attached unchanged; dated addendum and B table in PDF; AI-off authorship and receipt not established |
| Historical input sources, dates, units, definitions and exclusions | Labs 4, 6, 8, 10 | Input ledger linked to filings; coherent information cutoff | Core FY2025/H1 verified; expand for remaining valuation inputs |
| Normalized base year and contamination record | Labs 3, 10 | Reconcile filing; document adjustments and reasons, including items deliberately not normalized | Working reconciliation and forecast integration complete; assumptions qualified |
| Five-year company-specific three-statement forecast | Lab 10 | Revalidate drivers and opening balance sheet; expose full statements | Working integrated scenarios and outputs complete; assumptions subject to review |
| Balance sheet, cash-flow/cash, and filing reconciliation checks | Labs 9, 10 | Fresh executable checks and visible results; deliberate failure and recovery | Development tests pass; corruption/funding failures tested; cold run pending |
| FCFF DCF driven by pro-forma operating forecast | Labs 6, 10 | Replace final FCFE valuation with signed FCFF; reconcile taxes, D&A, capex and operating working capital | Base/upside FCFF integrated; continuing downside rejected for funding and separate conditional exit modeled |
| WACC and sustainable terminal convention | Labs 6, 10 | Dated, supported inputs; WACC > growth; defend reinvestment | Working 16% rate and explicit reinvestment transition; beta and mature assumptions require further challenge |
| Enterprise-to-equity/per-share bridge | Labs 6, 10 | Consistent cash, investments, debt, dilution and share count; no double counting | Working integrated bridge and instrument branches complete; exact capitalization, claim fair values and transaction scope still qualified |
| Causal low/base/high and downside that can change action | Lab 11 | Rerun named linked scenarios in final engine | Base/upside and separate conditional exit quantified; unfunded downside fails; memo carries conditional range/action and reversal triggers |
| Own-pro-forma one-way sensitivities and range-dependent ranking | Labs 10, 11; live course requirement 8 | Company operating drivers, units/ranges, EBIT/FCFF/value effects and alternate ranking | Added four bounded drivers and two range sets; proforma-sensitivity.md/.json; 7 new tests; exposed in app |
| WACC-growth grid and terminal-value share | Lab 6 | Recompute with final engine and show assumptions | Operating EV, conditional if-converted per-share grid and terminal share visible |
| Reverse DCF or market-implied expectation | Lab 6 | A feasible implied result or explicit bounded impossibility with decision interpretation | Reverse WACC reprices quote; bounded margin search and residual terminal burden explicitly qualified; outputs/reverse-dcf.md |
| Peer policy set before peer selection | Labs 7, 8 | Preserve criteria; revalidate selected peers and exclusions | Original candidates retained, extended policy saved before numerical refresh; qualified RDW/AVIO |
| At least one enterprise and one equity multiple | Lab 8 | Consistent dated EV/revenue and suitable equity multiple; do not force P/E for losses | EV/revenue including all leases and P/S calculated, dated definitions/translation explicit |
| Transaction evidence only if defensible | Lab 8 | Explicit inclusion or exclusion rationale; control, synergy and timing context | Explicit exclusion documented; pending Iridium lacks matched standalone control/synergy/time basis |
| Explain method disagreement; conditional range/action | Labs 8, 12 | Interpret results without mechanical averaging; monitoring/reversal triggers | Adopted WATCH/DEFER rationale and memo review copy include scenario envelope, method disagreement and triggers; recording/final freeze pending |
| Driver challenge record: value, basis, challenge, change evidence | Labs 10, 11 | Record every load-bearing driver; accurately attribute real partner input | Data records cover normalization/revenue/costs/statements/terminal/claims, peer/exit qualifications and app bounds; no invented partner review |
| Known-answer reconciliation | Labs 5, 6, 9 | Execute published training benchmark against final relevant functions | All twelve official Lab 5 answers pass against shared DCF helpers; final frozen validation record pending |
| Independent input definition/source check | Lab sources | Verify a load-bearing input independently; record effect | Cancellation, aggregate D&A and CFO rechecked to primary SEC filing; disposition and effect in validation-and-ai-use.md |
| Locked Changed-Input Record | Prior prediction files are AI drafts | Student authors a new AI-off prediction before execution; preserve timestamp, old/new inputs and units, predicted/actual directions and decision effect | Student action later |
| Boundary, monotonicity, bridge and peer consistency tests | Labs 6-11 | Relevant passing and intentional failing cases against final engine | Statement/terminal boundaries, WACC/growth, equity cash/share and peer date/currency/definition invariants pass |
| Highest-risk test and fresh-environment cold run | Prior lab checks | Record first failure, elapsed time, diagnosis, fix and decision; README-only reproduction | Funding failure tested; unrecorded assistant fresh-copy/venv check passed; required recording/log still pending |
| Independently checked AI output | Prior AI-assisted work | Accepted/corrected/qualified/rejected output with independent evidence | AI normalization claim accepted with qualification using SEC evidence and cash-flow reconciliation; record in validation-and-ai-use.md |
| Minimal bounded adjustable application | User accepted GitHub requirement | Base reset, visible checks and live input/result change; invalid case and recovery | Implemented; controls/live HTTP checks pass; Peyton reported successful visual change/reset/fail/recover walkthrough; recording pending |
| Visible executed output and usable repository | Existing lab outputs | Final inputs, full statements, valuation, checks and decision visible without running code | outputs/README.md indexes saved evidence; local app/setup work; remote final-project publication/access not verified |
| Research-Evolution.pdf | Labs 3, 4, 12 | Original A, final B, dated change/evidence/attribution table | Updated seven-page review PDF; original bytes attached, dated addendum and B included; baseline provenance limits disclosed |
| Decision memo <=2 pages or deck <=8 main slides | Lab 12 | Default two-page memo, consistent with final results | Two-page review PDF created/visually checked; student-adopted rationale and conditional range retained |
| Validation-and-AI-Use.pdf | Prior lab records | Frozen accurate final record; matching repository record | Six-page review PDF matches Markdown source; rehearsal disclosed; independent exercise/cold run and final freeze remain pending |
| Video 1 <=3 minutes, evolution and AI-output check | Lab 12 narrative | Student recording and corrected timestamped transcript | Student action later |
| Video 2 <=5 minutes, code and high-risk validation | Lab 12 narrative | Student recording and corrected timestamped transcript | Student action later |
| Video 3 <=5 minutes, live demo then committee defense | Recording tools available | First-minute live change/reset/fail/recover; student defense and corrected transcript | Student action later |
| Manifest, accessibility and frozen versions | Official template copied | Complete 11 required rows and mark optional deployment appropriately; verify links | Open |
| Brightspace submission and receipt | Deadline confirmed | Student submission by October 19, 11:59 PM Eastern; inspect receipt | Student action last |

## Rubric checkpoints

Decision usefulness 45; data integrity 45; financial judgment 60; technical usability 45; validation/reproducibility 75; professional communication 30. Total 300.

For each phase: check final requirements, related lab logic, and consistency across artifacts. Do not count historical AI-written prediction drafts as a human AI-off record, scripts as actual transcripts, simulated reviews as partner feedback, or file existence as a submission receipt.

Lab 13 is the portfolio mandate work for Project 2. Preserve it in the original workspace; it is not a missing Rocket Lab modeling component. The optional ungraded readiness feedback path does not remove the mandatory final validation evidence.
