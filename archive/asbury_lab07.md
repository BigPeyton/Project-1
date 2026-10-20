# Lab 07 — Asbury comparable-company analysis

## Purpose and prior DCF

Compare Asbury's earnings with the market P/E multiples of similar businesses.
The user reran the prior DCF and shared output: the illustrative Rocket Lab
scenario was $2.1433/share, with a $1.91–$2.51 sensitivity range. Its cash-flow
recovery assumption remains unverified. Today's Asbury case is a separate
training exercise, not a peer valuation of Rocket Lab.

The DCF sensitivity range varies the discount rate and terminal growth rate;
the broader valuation also depends on revenue growth, cash-flow margins, and
the assumed move to positive cash flow in 2029.

Question to investigate (AI-assisted): How do we decide whether another company's
business and earnings are comparable enough to apply its P/E to our target?

## Method

P/E = share price / annual earnings per share. A 10x multiple means investors
pay $10 for $1 of annual earnings. Implied target price = peer P/E * target EPS.
Share price is the market price of one ownership share. Annual diluted EPS
measures annual earnings attributable to common shareholders per diluted
weighted-average share. Dividing price by EPS normalizes the comparison for
different share counts and company sizes; share prices alone do not do this.
Positive, representative earnings and comparable business economics matter.
A low P/E can reflect weaker growth or greater risk, or unusually high earnings.
Unlike DCF, this method uses how the market prices other companies' earnings.
Do not add cash or subtract debt from a P/E-derived share price.

## Peer policy

Use publicly traded franchised vehicle retailers with new/used vehicle sales,
meaningful parts/service operations, and positive earnings on a consistent basis.
Compare geography, financing activities, and acquisitions before choosing peers.

- **AutoNation: use, with a financing caveat.** Its core dealership activities
  resemble Asbury's; AutoNation Finance deserves attention when comparing risk.
- **Group 1: qualify and include.** Its dealership business fits, but U.S./U.K.
  operations and the 2024 acquisition of 54 Inchcape dealerships limit comparability.

These decisions were prepared with AI assistance, and the user reviewed the
write-up and said it looked good. This does not establish a completed partner
discussion or an independently made pre-calculation decision.

## Frozen inputs and evidence

| Company | Role | Dec. 31, 2024 closing price (USD/share) | FY2024 total GAAP diluted EPS (USD/share) |
|---|---|---:|---:|
| Asbury (ABG) | Target | 243.03 | 21.50 |
| AutoNation (AN) | Peer | 169.84 | 16.92 |
| Group 1 (GPI) | Qualified peer | 421.48 | 36.81 |

Inputs come from the instructor's worked case, which links company releases and
proxy filings. This exercise reproduces those frozen inputs; it does not claim
independent verification of the underlying filings. Annual earnings were released
after the price date, so this is retrospective rather than a tradable point-in-time
analysis. Use total GAAP diluted EPS, not adjusted or continuing-operations EPS;
price and EPS must use the same stock-split basis.

## Calculation and verified checks

Run `python comps_lab07.py` from `C:\Users\Peyto\.codex`.

| Check | Result |
|---|---:|
| AutoNation P/E | 10.037825x |
| Group 1 P/E | 11.450149x |
| Median peer P/E | 10.743987x |
| Asbury implied minimum | $215.81 |
| Asbury at peer median | $231.00 |
| Asbury implied maximum | $246.18 |
| Remove GPI: AN reference estimate | $215.81 |
| Change from full-peer estimate | -$15.18 |

Example: `(421.48 / 36.81) * 21.50` gives Asbury's price at Group 1's multiple.
All calculations retain full precision; only displayed results are rounded.
Subtracting displayed prices can produce a different penny than subtracting
unrounded values, which explains the reported $15.18 change.

The user ran the calculator in the VS Code terminal and shared output matching
every course check above. Removing AN also produced $246.18, a +$15.18 change.
AI ran additional checks covering duplicate peers, target exclusion, missing,
zero, negative and nonfinite inputs, zero/one usable peer, and invalid target EPS.
Those checks passed. The calculator uses only the Python standard library and
does not fetch data or install packages.

## Interpretation and limitations

Removing the higher-multiple Group 1 lowers the estimate. With only AutoNation
left, there is one reference estimate rather than a peer range. Peer decisions
should change for business reasons, not to obtain a preferred price.

Asbury's historical $243.03 price lies inside the two-peer band. This does not
establish fair value or an attractive investment. Two observations provide little
protection against peer selection error, and growth, risk, financing, and unusual
earnings can justify different multiples. Negative or zero EPS makes this positive
P/E comparison not meaningful; do not invent or silently adjust earnings.

## Contribution and remaining steps

The user reran the prior DCF, ran the comparable-company calculator, shared both
outputs, and reviewed the write-up. AI prepared the code and explanations and
checked the calculations. Partner discussion, a personal hand calculation, and
a prediction made before seeing the peer-removal output have not been confirmed.

Complete any outstanding personal explanation and hand-calculation activities,
then upload the `.py` and `.md` files to the coursework GitHub repository. Submit the
file links through Brightspace > Quizzes > Lab 07 when instructed. Nothing in this
document establishes that upload or submission has occurred.

## Course sources

- [Lab 07](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/lab-07-comparable-policy.md)
- [Worked case and underlying source locators](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/teach-comps-worked-example.md)
- [Session 07 slides](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/slides-session-07.md)
