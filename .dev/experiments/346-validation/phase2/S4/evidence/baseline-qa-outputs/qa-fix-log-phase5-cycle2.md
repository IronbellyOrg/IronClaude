# Gate 2 fix log, fix cycle 2 (phase 5, last cycle)

**Status:** Complete
**Date:** 2026-11-08

---

## Finding 1 (IMPORTANT, blocking): synth-02 maps the CLI reading to "evaluates the predicate, then installs" (option C)

- Re-read: `synthesis/synth-02-target-gaps-external.md` line 31 (table "Reading of first use") and line 198 (Owner Q2 row) before editing.
- Evidence checked: `research/03-startup-flow-home-and-user-level-claude.md` line 327 (A3 C.5): the wrapper "must pass `bmad install` and `bmad --version`/`--help` through unchanged"; subcommands in 6.9.0 are `install`, `status`, `uninstall`. Same position as synth-03 Option C step 2 and synth-04 Phase 4 branch table.
- Fixed in `synth-02-target-gaps-external.md`:
  - line 31: the CLI-reading row now says no new mechanism, `bmad install` already creates the directories, wrapper passes `install`, `--version`, `--help` through unchanged, Stage 0 only; option C only for a new, separately named command; Options column changed from "C" to "A (documentation half, with the rest of Stage 0); C only for a new command name"; Source cell now cites R03 A3 C.5.
  - line 198 (Owner Q2 row): "a `bmad` command (C)" reworded to the same position. The question stays unanswered.
  - Grep sweep found two more occurrences of the same stale idea and corrected them: the F-01 Notes cell (was "Which of B, C, D fires at the right moment") and the "Option C" bullet under "What the external facts change" (added that C matters only for a new command name).
- Sweep result: Grep of the whole `synthesis/` folder for "evaluates the predicate", "then installs" and "predicate, then" after the edits finds no occurrence in synth-01 to synth-04. The remaining "B, C, D" hits (synth-03:320 and :386, synth-04:113, :407, :454) are the statement that the command and predicate are identical across triggers, which stays true for a new-command C, and were left as they are. One more hit, `synth-01-problem-current-state.md:479` ("the choice among B, C, D cannot yet be determined"), is outside the files named in the findings and does not state the CLI mechanism; I briefly edited it and then restored the exact original text to respect the binding scope guard (only synth files named in the findings). It is therefore unchanged; it is a MINOR wording point for the orchestrator, not a blocking item.
- Status: FIXED.

---

## Finding 3 (IMPORTANT, blocking): synth-03 says Option A alone fails the decision, while Stage 0 only satisfies the CLI reading

- Re-read before editing: `synth-03-options-recommendation.md` Option A Cons (line 86), Rationale row 1 (line 330), the Section 7 reading table (lines 310-312), the "Dependence on the owner readings" row 1 (line 364) and `synth-04-plan-questions-evidence.md` line 344 (Open Questions row 2).
- Evidence checked: the Stage 0 definition at synth-03 Section 7 (Stage 0 (b) is Option A's documentation half); the cited research basis for "the existing `bmad install` already creates the directories" is the synth-03 Option C step 2 reasoning from `research/03-...md` line 327 (A3 C.5) and `research/01-...` (installer writes per project); nothing new was introduced.
- One uniform statement now appears in every place: Option A (its documentation half) satisfies the CLI reading only together with the rest of Stage 0, and fails the decision for the slash-skill and session-open readings.
- Fixed:
  - `synth-03` Option A Cons (line 86): reworded accordingly.
  - `synth-03` Rationale row 1 (line 330): reworded accordingly; A stays as the documentation half of Stage 0.
  - `synth-03` Section 7 reading table row (1) (lines 310-312): now starts "Stage 0 only".
  - `synth-03` "Dependence on the owner readings" row 1 (line 364): states that Stage 0 holds A's documentation half, that A alone does not satisfy the reading, and that A fails readings 2 and 3.
  - `synth-03` Table 1 row "Which reading of first use it satisfies", Option A cell: was "None; the user types the documented command"; now "None by itself ... satisfies the CLI reading only together with the rest of Stage 0 ...; fails the slash-skill and session-open readings". Same defect found by Grep.
  - `synth-04` Open Questions row 2 (line 344), reading (a): same sentence added. Two more places with the same gap found by Grep: row 1 Impact cell ("If no: C ... for a CLI trigger; ... otherwise only the documentation half (A)") now says Stage 0 only for the CLI reading, C only for a new command; row 3 Impact cell "(Q1 any, Q2 a) leaves A and C" now adds "with Stage 0 only as the recommendation (C only for a new, separately named command)".
- Q1 and Q2 stay unanswered in every place (no owner decision was added).
- Status: FIXED.

---

## Finding 2 (IMPORTANT, blocking): synth-04 closes gap F-01 only through Phase 4, but under the CLI reading no Phase 4 branch is built

- Re-read before editing: `synth-04-plan-questions-evidence.md` gap map row F-01 (line 25), Phase 3 steps 3.1 to 3.6 ("embedded in the Phase 4 block", lines 118-123), Phase 5 steps 5.2 to 5.4 (lines 185-187), Phase 6 steps 6.1 and 6.7, and the Integration Checklist lines (319, 327-328 and the (v)(1) to (v)(3) lines).
- Evidence checked: the plan's own Phase 4 branch table (CLI reading: "No branch (Stage 0 only); 4C only if the owner asks for a new, separately named command") and synth-03 Section 7 Stage 1; no new fact was introduced, so no research citation was needed beyond the ones those rows already carry.
- Fixed in `synth-04-plan-questions-evidence.md`:
  - line 25 (F-01 gap row): adds the CLI-reading statement (Stage 0 only, no shipped block, no Phase 4 branch; 4C only for a new command name) and marks Phase 4 as "only when one is built".
  - Phase 3 Dependencies paragraph: new "Conditional on a built branch" sentence: the shared block exists only if a Phase 4 branch is built; otherwise steps 3.1 to 3.6 stay a documented specification (Stage 0 (c)) and "embedded in the Phase 4 block" has no target.
  - Phase 5 intro: states steps 5.1 and 5.6 apply under every reading and steps 5.2 to 5.5 need a built branch. Step titles for 5.2, 5.3 and 5.4 now carry the condition ("only if ... built"). Step 5.5 was already "For 4B and 4D only".
  - Phase 6 step 6.1 (driver-table row) and step 6.7 (run-only facts observed in the Phase 5 test) made conditional on a built branch; otherwise the facts stay UNVERIFIED in Section 9 (the register in Section 9 already carries them).
  - Integration Checklist: the "Shared command ..." line (:319), the static-pin and execution-test line (:327), the branch-specific proofs line (:328), the three (v)(1) to (v)(3) lines, the run-only facts line and the rollback line are now conditional on a built Phase 4 branch.
- Left as is on purpose: the "chosen subcommands" wording in 4C.1 and 4C.4 (cycle-2 MINOR N1) and any other Notes-section item; none was acted on.
- Status: FIXED.

---

## Closing counts and checks

- Findings in scope (BLOCKING_COUNT): 3 (rows 1 to 3 of `qa/qa-consolidated-findings-phase5-cycle2.md`).
- Fixes applied: 3 (finding 1, finding 2, finding 3).
- Findings not fixed: 0. Fixes applied plus findings not fixed = 3 = BLOCKING_COUNT.
- Files edited: `synthesis/synth-02-target-gaps-external.md`, `synthesis/synth-03-options-recommendation.md`, `synthesis/synth-04-plan-questions-evidence.md` and this log. `synth-01` was edited once and restored byte for byte (see finding 1); it is unchanged.
- MINOR items (the Notes section of the findings file, M-1, M-2, N1, N3, N4 and the cycle-1 MINOR rows) were not acted on.
- No evidence was invented: every added sentence restates what synth-03 Option C step 2, synth-03 Section 7 Stage 0 and Stage 1, the synth-04 Phase 4 branch table, or research 03 line 327 (A3 C.5) already say. No owner decision was added; Q1 and Q2 stay unanswered everywhere.
- Checks run after the edits: Grep of `synthesis/` for "evaluates the predicate", "then installs", "predicate, then" returns 0 matches; Grep for "A alone fails" and "so A alone" returns 0 matches; Grep for the new condition wording in synth-04 finds 11 matching lines.
- No product-code edit, no commit, no push, nothing staged, no test run.
