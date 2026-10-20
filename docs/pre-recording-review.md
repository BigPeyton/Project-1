# Pre-recording review - October 19, 2026

## Conclusion

The financial model and application are ready for a recording rehearsal after refreshing the app. The submission is not fully compliant or ready to submit. The independent human locked exercise remains absent; the retained example is AI-assisted and already known. The actual recorded cold run and three videos/transcripts are still needed. This review does not predict a grade or waive requirements.

## Findings corrected

1. **Material requirement gap:** the live course brief's requirement 8 calls for own-pro-forma one-at-a-time sensitivities, causal driver interpretation and a test of range-dependent ranking. Existing WACC/mature-margin/ROIC sensitivities and combined cases did not fully demonstrate this. Added space growth, space gross margin, R&D scale and Neutron recognized-revenue scale; two explicit range sets; 2030 EBIT, FCFF and value comparisons; full driver basis/challenge/change-evidence. App now exposes those operating drivers and a comparison against the original base. No historical data or baseline valuation changed.
2. **Range rationale:** all controls now have a documented basis and limitations in data/proforma_sensitivity_assumptions.json. The wide valuation-control limits are diagnostic bounds, not empirical historical bands. Operating sensitivities hold other paths, including five-year capex, fixed for attribution; they do not prove spare production capacity or validate implementable R&D cuts. Combined scenarios remain essential.
3. **Setup/dependency declaration:** added requirements.txt identifying Python 3.10+ and no third-party runtime dependencies; added .gitignore for environments, caches, temporary review copies and credentials. PDF-authoring dependencies remain separate.
4. **Stale status language:** corrected the operating DCF/equity report and README wording that said completed components were still missing. Updated review PDFs with current test counts and operating sensitivity findings. Historical milestone paragraphs remain historical.
5. **Evidence navigation:** added outputs/README.md so a grader can find the decision, input assumptions, full statements, values, sensitivities and checks without running the model.

## Verification

- 105 unit/integration tests pass. Six saved JSON/Markdown reports reproduce exactly; the baseline $2.9853, upside $6.7259 and existing conditional downside are unchanged.
- Fresh local project copy, new venv, CPython 3.13.15: README setup/audit and live change/error/reset passed in 15.973 seconds with no unexpected failure. This is assistant development evidence, not a recorded student cold run. Existing development environment remains Python 3.12.14.
- All 19 archived files match their recorded SHA256 hashes. Edition A is preserved unchanged with candid provenance, not relabeled AI-off; no baseline receipt has been verified.
- User previously visually confirmed base/WACC/reset/fail/recover. New operating controls require a quick refresh/rehearsal before recording. Assistant checked their engine and HTTP behavior; no assistant visual-browser inspection is claimed.
- No credential-like files were found in the project filename scan. No actual video or corrected transcript files exist yet. This is not a claim to have scanned unrelated user directories or verified a remote publication.
- Review PDFs must match their Markdown sources and repository copies; document-build.json identifies their current hashes. Recording should use the revised app and documents.

## Financial qualifications to defend on camera

- The $1-$7 figure is a conditional standalone scenario envelope, not a universal price target. WACC/financing sensitivities can fall outside it. Pending transaction operations and funding are excluded together.
- Base value does not automatically support note conversion; explain the conditional share basis and separate retained-note/intrinsic-only diagnostics. Do not use basic EPS shares as the diluted economic denominator.
- Base operating EV is negative because the specified strategy has net present costs; cutoff nonoperating liquidity supports positive equity value. It is not a negative stock price. Cutoff cash is estimated.
- Downside continuation fails funding; the orderly exit uses unverified recoveries/closure costs and is not a guaranteed floor. Hypothetical ATM proceeds are not committed financing.
- Revenue growth does not equal free cash flow. Regular compensation, R&D, capex and working capital matter. Mature profitability, marginal returns, beta and funding remain qualified assumptions.
- Among the four tested operating drivers, standard ranges rank space growth first; alternative ranges rank R&D first for all three outputs. Ranking is conditional on range choices, not universal causal importance. Do not mechanically average peer/DCF values.
- Passing tests establishes arithmetic/behavior, not the truth of financial assumptions. AI assistance, the preserved baseline provenance and missing independent exercise must be described accurately.

## Recording sequence and remaining evidence

1. Record the fresh-environment README-only cold run and retain its actual first failure, elapsed time, version, risk test, current decision and must-fix items. The unrecorded rehearsal above can prepare you but cannot supply the recording.
2. Video 1 (maximum 3:00): unchanged A, dated addendum, B/change evidence and one source-checked AI output. Do not claim Edition A was independently AI-off.
3. Video 2 (maximum 5:00): open the submitted code, explain data -> linked statements -> FCFF -> DCF -> equity allocation, run relevant tests and show a highest-risk failure. Do not just read the README.
4. Video 3 (maximum 5:00): first-minute live product demo. Change an operating control, explain EBIT/FCFF/value against the base, reset, trigger invalid growth/WACC and recover. Then defend WATCH/DEFER with the app on screen. The prior WACC demo still works; the operating control better demonstrates the company's pro-forma.
5. Correct transcripts against the actual recordings and supply true timestamps/durations. No prepared script is an actual transcript. Complete the 12-row manifest, freeze versions, verify instructor access, submit and retain the receipt.

## Open items that this review cannot declare complete

- Independent locked prediction/commit/execution: missing. The user elected to retain the disclosed AI-assisted rehearsal; this is not evidence of an instructor exception.
- Recorded cold run, all three actual videos and corrected transcripts: missing.
- Original Edition A receipt/AI-off compliance: not established; available original preserved under professor's clarification.
- Final manifest, GitHub project publication/instructor access, video links/access, frozen commit and Brightspace receipt: not verified. Git was not on PATH during this review, and the public repository fetch failed; do not infer that the local final project has been uploaded.

Course authority checked live: https://raw.githubusercontent.com/CinderZhang/FIN43900-Fall2026/main/projects/project-1-corporate-finance-application.md (requirements 8 and 10; validation and Video 3). Brightspace's 300-point rubric and October 19, 11:59 PM deadline remain controlling.
