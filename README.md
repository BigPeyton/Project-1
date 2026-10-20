# Rocket Lab - FIN 439 Project 1

Working project; not ready for submission. Prepared October 19, 2026.

Decision/user: a buy-side committee with no RKLB holding; WATCH/DEFER at the September 10, 2026 close of $61.96. The conditional standalone scenario envelope is approximately $1-$7/share, with transaction, financing and claim limitations. See the memo for conditions and reversal triggers. Runtime/environment declaration: requirements.txt (standard library only).

## Open the application

Use Python 3.10 or newer. The application uses the Python standard library only: no package installs, API keys or network data requests are needed. From the `rocketlab_project1` folder in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -B src\validate_project.py
.\.venv\Scripts\python.exe -B src\app.py
```

If Windows does not recognize `python`, use `py -3 -m venv .venv` for the first command. Activation is unnecessary because subsequent commands address the environment's interpreter directly. On macOS/Linux, use `python3 -m venv .venv` then `.venv/bin/python` for the same script commands.

Open **http://127.0.0.1:8765** in your browser. Keep the terminal running; Ctrl+C stops the app. If the port is occupied, run the app with `--port 8766` and open the printed address. The server listens only on this computer and does not publish the project.

Start with base. Change WACC from 16 to 18 and select **Recalculate**; **Reset to base** restores the reference. **Test invalid boundary** deliberately sets growth equal to WACC and shows an error without a stale result; reset recovers. **Test downside funding** shows the original unfunded downside's failure rather than inventing financing. These are already demonstrated development examples, not a fresh student locked exercise.

The controls accept percentages as numbers (16 means 16%). Changing the scenario selector retains your entered valuation controls; **Load upside defaults** loads the complete upside reference. Expand the three statements, bridge and long-term transition; **Download this run (JSON)** preserves inputs/results. The displayed recommendation is the student-adopted reference and is not automatically changed by a sensitivity. Runs do not overwrite data files. Assumptions and financial limits appear on the page and in its evidence links.

Four operating controls affect the linked 2027-2030 statements: space-growth shift (-5 to +5 percentage points), space gross-margin shift (-3 to +3 points), R&D spending scale (80%-120%), and Neutron recognized-revenue scale (50%-150%). Defaults are 0, 0, 100 and 100. For a recording rehearsal, change R&D scale from 100 to 110: 2030 EBIT falls by $39m and the conditional price becomes about $2.74. Use **Compare with restored base** to read EBIT, FCFF and value changes, then reset. This is an AI-assisted known example, not the independent locked exercise. The [operating sensitivity report](outputs/proforma-sensitivity.md) explains causal links, bounds and rankings under two different range sets.

For a timed, saved development audit, use `.\.venv\Scripts\python.exe -B src\validate_project.py --save`. This writes `outputs/development-validation.md` and `.json`, including test results, source/data/test hashes and saved-report comparisons. It does not satisfy the recorded cold run. Follow [the cold-run protocol](docs/cold-run-protocol.md) for that separate evidence. Preserve the [human locked prediction](docs/locked-changed-input-record.md) with AI closed during prediction and execution.

## Start here

- Written review package: [two-page decision memo](deliverables/Decision-Memo.pdf), [research evolution](deliverables/Research-Evolution.pdf), and [validation / AI use](deliverables/Validation-and-AI-Use.pdf). Matching repository copies are in docs/. [Document QA](docs/document-review.md) records the checks. These are review copies with missing evidence disclosed, not a complete submission.

- [Requirements checklist](docs/requirements.md): project requirements, related labs, and evidence still needed.
- [Current status](docs/status.md): completed preparation and next steps.
- [Source audit](docs/source-audit.md): reported inputs, verification history and remaining qualifications.
- [Cash estimate](docs/cash-bridge-method.md) and [claims treatment](docs/claims-treatment.md): dated facts, explicit assumptions and equity-bridge integration rules.
- [Historical normalization](docs/normalization.md) and [visible reconciliation](outputs/historical-normalization.md): reported versus operating run-rate earnings, with recurring costs retained.
- [Progress review](docs/progress-review.md): verified preparation, corrections and remaining requirements.
- [Revenue assumptions](docs/revenue-forecast.md) and [visible scenarios](outputs/revenue-forecast.md): company-specific working forecast, ready for cost-model integration.
- [Operating forecast](docs/operating-forecast.md) and [visible results](outputs/operating-forecast.md): gross profit, R&D, SG&A and EBIT scenarios, including a zero-Neutron-revenue stress.
- [Linked statements and FCFF](docs/three-statements.md): [base](outputs/three-statements-base.md), [upside](outputs/three-statements-upside.md), and [conditional downside](outputs/three-statements-downside.md). The integrated cutoff estimate supersedes the earlier historical-burn cash bridge for valuation.
- [WACC and terminal transition](docs/wacc-and-transition.md) and [visible operating DCF](outputs/valuation-transition.md): dated inputs, explicit maturity/reinvestment assumptions and operating-EV sensitivity. These are not final per-share values.
- [Integrated equity bridge](docs/equity-bridge.md) and [per-share sensitivities](outputs/equity-bridge.md): converted/retained notes, existing awards, cash/claims, forward/capped-call/ATM alternatives underlying the conditional memo.
- [Downside and peer review](docs/downside-and-comparables.md): [orderly-exit scenario](outputs/downside-exit.md), [comparable multiples](outputs/comparables.md), and [policy](docs/peer-policy.md). Recovery assumptions and peer qualifications remain explicit.
- [Market-implied expectations](outputs/reverse-dcf.md) and [committee rationale](docs/committee-decision.md): bounded reverse DCF, margin/return challenges, conditional range and triggers; rationale adopted by Peyton.
- [Historical archive](archive/inventory.csv): original lab copies with SHA256 hashes and source paths.
- [Submission manifest](project-submission-manifest.csv): unfilled official course template.
- [Validation and AI-use register](docs/validation-and-ai-use.md) and [timed development audit](outputs/development-validation.md): evidence map, provenance, failures and remaining required work.

The archive preserves earlier work. Archived outputs are not the final valuation, new validation, or proof of submission. Final code will live in `src`, explicit inputs in `data`, tests in `tests`, visible results in `outputs`, and submission files in `deliverables`.

The local adjustable interface is implemented. Peyton adopted the AI-assisted committee rationale and reported a successful visual change/reset/fail/recover walkthrough. The assistant's HTTP/control checks also passed; no assistant visual browser inspection is claimed. Final submission documents, the independent exercise, recorded cold run and actual videos/transcripts remain incomplete.

## Run the working financial model

Use Python 3 from this project folder. These scripts use the standard library; no third-party dependencies or credentials are required.

```text
python src/three_statements.py
python src/three_statements.py --case upside
python src/valuation.py
python src/equity_bridge.py
python src/downside_exit.py
python src/comparables.py
python src/reverse_dcf.py
python src/proforma_sensitivity.py
python -B -m unittest discover -s tests -v
```

`python src/three_statements.py --case downside` deliberately stops at the modeled 2030 funding gap. To inspect the distinct scenario with assumed external equity, run `python src/three_statements.py --case downside --allow-conditional-equity`. That option does not establish financing availability. The separate `downside_exit.py` models a conditional 2029 orderly exit with explicit unverified recovery haircuts and closure costs. Saved outputs expose results without running code. Current test count: 105 passing; the final recorded cold run remains outstanding. Add `--save` to the equity-bridge, downside-exit, comparables, reverse-dcf or proforma-sensitivity command to refresh its Markdown/JSON outputs.

The initial filing-data audit is available: run `python src/audit_reported_inputs.py` from this folder. It uses the standard library and writes `outputs/reported-input-checks.md`. This verifies reported-data arithmetic, not the final financial model.
