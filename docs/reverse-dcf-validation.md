# Reverse-DCF development validation

October 19, 2026. AI-assisted development checks; not the student's Locked Changed-Input Record or recorded fresh-environment cold run.

- Independent algebraic toy case: equity 100, 10 shares, net bridge 20, explicit PV 30, WACC 10%, terminal date one year, growth 2%. Target price 10 implies terminal PV 50, terminal value 55 and terminal FCFF 4.4. Shared reverse calculations reconcile these known values.
- Existing model round trip: substituting its own price recovers its own terminal FCFF and 12% base mature margin, preserving inputs.
- Bounded solver: increasing/decreasing known linear roots reconcile; an unbracketed target returns no root. Reversed/nonfinite bounds, nonfinite outputs, a nonmonotonic sampled path and a discontinuous pseudo-root fail loudly.
- Market-target round trip: base/upside implied WACC and residual terminal calculations each reproduce $61.96. Base root is below Treasury; upside is above it. The visible report preserves that distinction.
- Development first failure: report save revealed a missing string-concatenation operator after a conditional wording edit (TypeError). Corrected the operator and added a report-rendering regression check. No financial inputs changed. A subsequent file-write PermissionError required workspace write approval; it was an environment permission issue, not a model result.
- Highest-risk conclusion remains the operating/transaction/terminal thesis, not numerical root accuracy. Bounded margin, lower margin/ROIC, funding and capitalization scenarios expose relevant weaknesses, but do not replace independently supported assumptions or the final cold run.

No elapsed time or student-authored prediction is invented for this development record. The final validation record must preserve actual first failure, elapsed time, decision effect and must-fix items from its separate protocol.
