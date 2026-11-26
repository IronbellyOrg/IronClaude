| Status | Result |
|---|---|
| DONE | Wrote the Redesign 5 (Coverage Deflection) spec: `.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r5-coverage-deflection/DESIGN.md` (596 lines). It covers all 7 items you asked for. |
| DONE | Ran three independent reviews (`design-report/review-1.md`, `review-2.md`, `review-3.md`). Every finding from reviews 1 and 2 is fixed, and the next review confirmed each fix. |
| DONE | Applied review 3's last fix after the review limit: create `/tmp/evalsb-collab-r5` before pytest uses it for temporary folders. A one-test pytest run confirmed it works, but no fourth review was allowed, so nobody has re-reviewed it independently. |
| DONE | Wrote the return contract: `design-report/return-contract.yaml` (status succeeded). |
| NEXT | Answer the five open questions in DESIGN.md section 7.2 (Q1-Q5), starting with Q1, then build from the spec. |

NOT BUILT: no script, test or spike exists yet. This run produced the spec only.

What you should know before building:
- **The F6 brief has to decide something.** Each card tells the slow reviewer (the one still running) to "apply catalogue moves M1-M10". The spec therefore puts the move catalogue (the ten fixed investigation steps) in every reviewer's brief for the collaboration arm. Comparing that arm with the catalogue-only control (A2) then measures the cards alone. My recommendation is to keep this (Q1).
- **haiku + 2x luna will probably not run.** With haiku's 23 s per turn, the time budget allows at least one request only if haiku's final report turn takes 12.3 s or less. That is unlikely. If the timing spike measures zero allowed requests on every package, the launch script refuses that panel's collaboration arm and records why.
- **ember + 2x luna runs with the roles reversed.** Ember finishes first, so ember is the scout and the two lunas receive cards: at most one each, with different Tasks for each luna. The source plan pre-registered only sonnet + 2x luna, so the ember and haiku runs are exploratory.
- **The judge script is used without changes.** The spec calls the original `judge-one.sh` in place and checks its sha256 first. Its folder argument walks out of the `20261111-a1` folder into this redesign's folder, so nothing is written to `20261111-a1`.

Not checked: whether hooks fire on gateway models, how often each model acts on an injected card, and every timing value. The Gate 0 spikes in section 6.3 must measure these before any experiment run.
