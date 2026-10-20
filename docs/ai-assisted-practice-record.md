# AI-assisted changed-input rehearsal — NOT the required locked exercise

Prepared and executed by the assistant on October 19, 2026 at the student's request. This repeats a previously known result. It is not a human-authored prediction, an AI-off execution, an independently precommitted exercise or a recorded cold run. The separate locked-changed-input-record.md remains blank.

## Setup and expected behavior

- Input: WACC, 16% to 18% (increase of two percentage points).
- Held fixed: base operating scenario; 3% terminal growth; 12% mature EBIT margin; 16% marginal ROIC; existing converted/full-award equity bridge and 655.006167 million shares.
- AI-authored expectation, with prior result already known: conditional per-share value decreases on this tested interval. Signed cash flows do not justify a claim of global WACC monotonicity.
- AI-authored expected decision effect: WATCH/DEFER remains appropriate at the $61.96 cutoff price; a lower modeled value does not resolve the transaction-scope and funding limitations.
- No repository precommit or human AI-off attestation is claimed. The expectation was included in the rehearsal execution script, not independently locked by the student.

## Actual execution

Live HTTP requests to the same application engine, in order: `/result.json`, `/result.json?wacc=18`, `/result.json`.

Started: 2026-10-19T21:32:54.073530+00:00. Finished: 2026-10-19T21:32:54.193796+00:00. Measured request/check elapsed time: 0.120668 seconds. This timing excludes document preparation and does not measure a cold run.

| Result | Before | After WACC change | Reset |
|---|---:|---:|---:|
| WACC | 16% | 18% | 16% |
| Conditional price, USD/share | 2.985305156470462 | 2.749821860661706 | 2.985305156470462 |
| Operating EV, USD millions | -105.93019493130856 | -260.1732059115289 | -105.93019493130856 |
| Participating shares, millions | 655.006167 | 655.006167 | 655.006167 |

Price declined by $0.2354832958087556/share, or 7.888081233449795%. Displayed prices are $2.99 and $2.75; calculate changes from unrounded values. The reset result exactly matched the reference result. Maximum balance-sheet residual was approximately 4.55e-13 million, terminal continuity residual approximately 5.68e-14 million, and bridge residual zero in all three runs. No unexpected failure occurred in these requests.

## Interpretation and verification

Observed direction matches the already-known expectation. The assistant's interpretation remains WATCH/DEFER because the sensitivity further weakens support for initiating at the reference quote. The app displays the adopted reference recommendation and does not automatically compute a new committee judgment; an unchanged on-screen label alone is not evidence of a reasoned decision effect.

The student may reproduce this rehearsal by resetting to base, entering 18 for WACC, recalculating and resetting again. That is useful verification but does not turn this known, AI-assisted result into the required independent exercise. A fresh independently authored, precommitted prediction and execution with AI closed remain outstanding.
