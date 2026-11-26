# Owner decisions for the Sweep Sheet validation (DESIGN.md section 15.1)

## 1. G0 selection-recall floor: 0.45, pooled (confirmed by the owner, 2026-11-15)

- Pre-register it with this wording: "an estimate, not a validated figure". Report the measured selection recall with its range whatever the result.
- It is a go/no-go gate for spending model runs, not a claim that the sheet helps. A pass says the sheet can contain the right item; whether reviewers act on it is measured separately.
- Basis (recomputed 2026-11-15 from the ten rows of the coverage table in `.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md`, section 3.1(d)): mean of the lower ends of the selection estimates 0.480 (0.506 without the experimental C3 row); mean of the upper ends 0.740; mid-point 0.610. All inputs are unmeasured estimates, so the floor is not independent of the design it tests.
- Chance of passing, assuming 20 to 40 hold-out issues (binomial calculation, not measured): true recall 0.25: 0 to 4%; 0.35: 12 to 24%; 0.48: 63 to 70%; 0.61: 95 to 99%; 0.74: 100%.
- Do not raise it: at 0.50 the mid-point case passes only about 90% of the time.
- Not done yet: the value is not written into `config/prereg.json`. That happens at the freeze (`analysis/analyze.py prereg`), which is plan step 14 and has not been run.

## 2. to 4. Adopted under the owner's order of 2026-11-15 ("adversarially debate all 3 sets of defaults; if they pass, proceed with them; if not, refactor and then proceed")

Debates: three advocates each (Haiku-alias, Sonnet, Sonnet) plus a fault-finder; no Opus. Opus is not in any session's model usage. The Haiku alias resolved on this gateway to `gpt-6.1-sol` for at least some advocate turns (the session transcripts record that model name), so the "Haiku" advocate was not Claude Haiku. Debate depth standard; the orchestrator and merge were done by the Sonnet session, scoring condensed, so the verdicts are not an independent score. After the debates the sweep-sheet tests pass again (749 passed, 4 deselected) with the edits in place.

| # | Default | Verdict | Adopted value |
|---|---|---|---|
| 2 | Per-class act bands | FAIL on the numbers-only default (no measure, no comparison rule, no consequence), refactored | The eight numbers unchanged (C1 0.10-0.40, C2 0.20-0.45, C3 0.03-0.15, C4 0.50-0.75, C5 0.35-0.60, C6 0.05-0.30, C7 0.15-0.35, C8 0.40-0.65) with the registration text of `DESIGN.md` section 15.1a: the measure, a 95% Wilson rule (under 10 item-runs "not assessable"), a report-only consequence, and a may-not list. See `results/debate/1-act-bands/VERDICT.md`. |
| 3 | CB-2 | PASS | Leave `briefs/cb2.txt` verbatim in every arm; count the `## Ledger` headings in Z0 and K. No file changed. See `results/debate/2-cb2-verbatim/VERDICT.md` (note: "owner decision if above 0" has no content yet). |
| 4 | K-arm lead-in | PASS | Approve `briefs/k-lead.txt` as drafted. No file changed. See `results/debate/3-k-lead/VERDICT.md`. |

Limits recorded by the debates: the act-band numbers are unmeasured planning values; nothing computes the new act-band measure or flag yet (`analysis/analyze.py`, `prereg()` and the tests were not edited, so the rule is applied by hand until a follow-up adds code and tests); the act-band text is not in `config/prereg.json` yet (that is plan step 14, the freeze, which has not been run); the BD-3 fix and probe-driven additions were not re-debated.

Commit id: none yet (nothing committed).

## Still open

- The freeze go (plan step 14), the document list (D1), and sharing of one control (D2): see `20261114-collab-process/PROCESS.md` section 8.
