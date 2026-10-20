# Share reconciliation checks

Executed October 19, 2026 against `data/capitalization.json` using Python decimal arithmetic for proceeds. All seven checks passed:

1. Common plus participating preferred = 639,410,989 shares.
2. Adding full existing RSUs and options = 652,398,422 shares.
3. Adding remaining disclosed note-conversion shares = 655,006,167 shares.
4. Full option exercise at the disclosed weighted-average strike produces $3,856,495.21.
5. The known 140,157-option exercise transfers shares to common without increasing the full-exercise total.
6. That exercise produces $152,771.13.
7. The converted-note scenario specifies zero note deduction.

Scope: arithmetic and consistent scenario bookkeeping only. These checks do not verify exact September capitalization, final valuation, an exhaustive dilution model or the student's independent locked exercise.
