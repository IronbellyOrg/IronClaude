BLOCKING_COUNT: 3

# Gate 2 consolidated findings, fix cycle 2 (the last allowed cycle)

Sources: `qa/qa-verification-phase5-cycle1-content.md` (agent report, FAIL, Important 3) and `qa/qa-verification-phase5-cycle1-structural.md` (agent report, PASS, Minor 4). All 8 cycle-1 blocking findings are confirmed fixed by the structural agent; the content agent confirms 7 of 8 fixed in substance and finding 6 (Option C for the CLI reading) as partly fixed, which produced N-1 to N-3. Synthesis files are under `synthesis/`. Not SYSTEMIC: 3 blocking findings now versus 8 in cycle 1.

| # | Reporter severity | Final severity | Reason for any change | Blocking | Finding | Originating report | Target synth file | Proposed fix |
|---|---|---|---|---|---|---|---|---|
| 1 | IMPORTANT (N-1); structure agent: MINOR (N2, same defect) | IMPORTANT | Structure agent graded the same stale text MINOR; kept at the content agent's grade because it is a false statement of the recommended mechanism that contradicts Sections 6 to 8. Not a downgrade. | yes | `synth-02-target-gaps-external.md` lines 31 and 198 still map the CLI reading to a wrapper that "evaluates the predicate, then installs" (Option C). That contradicts the corrected synth-03 and synth-04, which say `bmad install` passes through unchanged and the CLI reading gets Stage 0 only (option C only for a new, separately named command). The cycle-1 fix log never lists synth-02. | content verification (N-1); structural verification (N2) | synthesis/synth-02-target-gaps-external.md | Reword both places to the Stage 0 / new-command-name position; Grep the whole synthesis folder for any other "evaluates the predicate, then installs" or equivalent phrasing and correct every occurrence. |
| 2 | IMPORTANT (N-2) | IMPORTANT | | yes | `synth-04-plan-questions-evidence.md` lines 25, 118-123, 186, 319, 327-328: gap F-01 is closed only via Phase 4, and Phase 3, step 5.3 and the checklist lines need the shipped first-use block; under the CLI reading no Phase 4 branch is built, so none of them has a target. | content verification | synthesis/synth-04-plan-questions-evidence.md | Add the CLI-reading statement for F-01 (Stage 0 only, no shipped block). Mark Phase 3, steps 5.2 to 5.4 and the checklist lines at :319 and :327-328 as conditional on a built Phase 4 branch (B3, D3 or a new-command C), so the plan is consistent under every owner reading. |
| 3 | IMPORTANT (N-3) | IMPORTANT | | yes | `synth-03-options-recommendation.md` lines 86 and 330 say Option A alone fails the decision; lines 310-312 and 364 (and `synth-04:344`) say Stage 0 only satisfies the CLI reading. | content verification | synthesis/synth-03-options-recommendation.md | Reconcile Rationale 1 and Option A Cons with reading (1): state that Option A (documentation half) satisfies the CLI reading only together with Stage 0, and fails the decision for the slash-skill and session-open readings. Make lines 86, 330, 310-312, 364 and synth-04:344 say the same. |

## Severity changes

none. No finding was downgraded. Row 1 merges a structure-agent MINOR with the content agent's IMPORTANT and keeps the higher grade (evidence: the stale text at synth-02:31 and :198 contradicts synth-03:130, :321, :335, :364 and synth-04:134, :158, :344 as the content report records).

## Notes (MINOR, not acted on, never rechecked)

- M-1 (content): the Section 9 intro still says the owner questions are "copied", though Q2(b) is reworded.
- M-2 (content): a new command name is placed in the `bmad` wrapper, which a different name would not pass through.
- N1 (structure): synth-04 steps 4C.1 and 4C.4 still say "chosen subcommands", contradicting 4C.2.
- N3 (structure): step 2.5 quotes only the `_bmad/` condition for the manual command, while step 2.2 also requires no `.claude/skills/bmad-*`.
- N4 (structure): synth-03 is missing a blank line before the "Feasibility statement" heading.
- The Minor rows 9 to 31 of `qa/qa-consolidated-findings-phase5.md`.

review 2 of 3 complete; if the next verification fails the gate HALTS
