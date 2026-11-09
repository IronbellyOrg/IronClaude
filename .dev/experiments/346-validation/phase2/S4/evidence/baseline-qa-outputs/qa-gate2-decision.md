GATE2_DECISION: FAIL (cycle 1), second fix cycle required

Review count: review 1 (three reports) and the cycle-1 verification (review 2) are done; the cycle-2 verification will be review 3. After cycle 2 any open blocking finding means HALT and ask the user.

SEVERITY_DOWNGRADES: 0

(The `## Severity changes` section of `qa/qa-consolidated-findings-phase5.md` lists one change: row 8 went from the structure agent's MINOR UP to IMPORTANT; that is an upgrade, not a downgrade. No reporter CRITICAL or IMPORTANT finding was downgraded.)

## Inputs read

| Report | Verdict | Counts |
|---|---|---|
| qa/analyst-synthesis-accuracy.md | PASS | Critical 0, Important 0, Minor 8 |
| qa/qa-synthesis-structure.md | FAIL | Critical 0, Important 4, Minor 11 |
| qa/qa-synthesis-qualitative-report.md | FAIL | Critical 0, Important 5, Minor 10 |
| qa/qa-consolidated-findings-phase5.md | BLOCKING_COUNT: 8 | 31 rows |
| qa/qa-fix-log-phase5-cycle1.md | 8 fixed, 0 not fixed | |
| qa/qa-verification-phase5-cycle1-structural.md | PASS | Critical 0, Important 0, Minor 4; all 8 fixes confirmed against code |
| qa/qa-verification-phase5-cycle1-content.md | FAIL | Critical 0, Important 3 (N-1, N-2, N-3), Minor 2; findings 1 to 5, 7, 8 resolved, finding 6 partly resolved |

## Open blocking findings entering fix cycle 2

| ID | Target | Finding |
|---|---|---|
| N-1 | synthesis/synth-02-target-gaps-external.md lines 31 and 198 | Still map the CLI reading to a wrapper that "evaluates the predicate, then installs" (option C); contradicts the corrected synth-03 and synth-04 (Stage 0 only, `bmad install` passes through unchanged). The cycle-1 fix log never lists synth-02. Fix: reword both to the Stage 0 / new-command-name position. (The structure agent's minor note N2 is the same defect.) |
| N-2 | synthesis/synth-04-plan-questions-evidence.md lines 25, 118-123, 186, 319, 327-328 | Gap F-01 closure, Phase 3 and test step 5.3 and the checklist lines assume a shipped first-use block under every reading; under the CLI reading no Phase 4 branch builds it. Fix: add the CLI-reading statement for F-01; mark Phase 3, steps 5.2 to 5.4 and the checklist lines conditional on a built Phase 4 branch. |
| N-3 | synthesis/synth-03-options-recommendation.md lines 86 and 330 vs 310-312 and 364 | "Option A alone fails the decision" vs "Stage 0 only satisfies the CLI reading". Fix: reconcile Rationale 1 and Option A Cons with reading (1). |

Minor notes (not acted on): Section 9 intro still says the owner questions are "copied" though Q2(b) is reworded (M-1); a new command name is placed in the `bmad` wrapper which a different name would not pass through (M-2); synth-04 steps 4C.1 and 4C.4 still say "chosen subcommands" (structure N1); step 2.5 quotes only the `_bmad/` condition (structure N3); a missing blank line in synth-03 (structure N4); plus the other Minor rows 9 to 31 of the cycle-1 consolidated file.

## Final (after fix cycle 2, review 3 of 3)

Cycle-2 verification reports read: qa/qa-verification-phase5-cycle2-structural.md (PASS, Critical 0, Important 0, Minor 3; findings 1 to 3 judged fixed) and qa/qa-verification-phase5-cycle2-content.md (FAIL, Critical 0, Important 2, Minor 4).

SEVERITY_DOWNGRADES (total across cycle-1 and cycle-2 consolidated files): 0 (both `## Severity changes` sections: cycle 1 lists one upgrade, cycle 2 says `none`; no downgrade lines).

Open blocking findings (content agent; executor re-read the cited report text qa-verification-phase5-cycle2-content.md lines 29-42):

- V-1 (IMPORTANT): "Stage 0 satisfies the CLI reading" is an unlabelled author inference, repeated flatly at synth-03:86, :262, :311-313, :331, :365; synth-04:341-345; synth-02:31, :107, :443. Only synth-03:130 labels it as inference; no research file says it (R03:327 says only that the wrapper must pass `bmad install` through and skills are not reachable until a `bmad` command has run). The "A alone fails / A with Stage 0 holds" distinction is wording only (Stage 0 has no run-time behaviour, synth-04:280), and Q2(a) at synth-04:344 now embeds the author's answer, against task-file line 161 ("nobody may guess an answer") and synth-04:339. Required fix: (1) mark each place "synthesis inference: the only mechanism found for this reading is the existing manual `bmad install` or a new command name; whether that meets the owner's decision is the owner's call"; (2) delete the "A alone fails / with the rest of Stage 0 holds" distinction or state it as "Stage 0 adds records and a specification, not run-time behaviour"; (3) add to Q2(a) the owner sub-question "does running `bmad install` by hand count as creation on first use".
- V-2 (IMPORTANT): the plan is still inconsistent under the CLI reading. Gap rows F-05, F-06, F-08 (synth-04:29, :30, :32) close via Phase 3/4/5 steps that under the CLI reading are not built (synth-04:178, :114, :327-328); Phase 7 steps 7.8 to 7.10 (synth-04:268-270) are unconditional; the Phase 4 heading at synth-04:125 says "exactly one branch" against :19, :134 and :320 ("at most one"/"No branch"); synth-03:323 (Stage 2) has no condition. Required fix: add the condition "only if a Phase 4 branch is built; under the CLI reading with no new command, none" to rows F-05, F-06, F-08, steps 7.8 to 7.10, the Phase 4 heading ("at most one") and synth-03:323.

GATE2_FINAL: FAIL - HALT

## User exception applied (2026-11-07)

The user explicitly accepted this second exception to the 3-review limit, for Gate 2. The executor made the V-1 and V-2 edits itself (synth-02 lines 31, 198, 443; synth-03 Option A Cons, Table 1 A cell, diagram row (1), Stage 1 CLI text, Stage 2 row, Rationale rows 1 and 6, Dependence row 1; synth-04 Section 8 intro, F-01, F-05, F-06, F-08, phase-selection row, Phase 4 heading, steps 7.8 to 7.10, Section 9 rows 2 and 3), read the edited places back, searched synthesis/ for the old phrasing (no match), and ran no fourth agent review. Q1 and Q2 stay unanswered; Q2(a) gained the owner sub-question "does running `bmad install` by hand count as creation on first use".

GATE2_FINAL: PASS (user-accepted exception, 3 reviews plus manual edits; no fourth review)
