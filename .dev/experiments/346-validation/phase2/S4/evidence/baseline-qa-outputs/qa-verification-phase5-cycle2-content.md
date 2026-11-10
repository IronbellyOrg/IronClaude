# QA Report - Gate 2 Fix Cycle 2 Content Verification (report-qualitative, fix-cycle)

**Status:** Complete (see end of file for verdict)
**Date:** 2026-11-08

---

**Topic:** BMAD first-use directory creation in a project that never had BMAD
**Fix cycle:** 2 (last). **Fix authorization:** false (report only).
**Inputs read:** `qa/qa-consolidated-findings-phase5-cycle2.md`, `qa/qa-fix-log-phase5-cycle2.md`, `synthesis/synth-02` (lines 25-115, 436-463), `synth-03` (all 400 lines), `synth-04` (all 474 lines), `research/03` lines 174-181, 193-195, 325-327, `research/01` lines 79, 386, task file lines 161-164.

## Check (a): blocking findings 1-3 resolved by substance

### Finding 1 (synth-02 CLI mapping) - RESOLVED
- Read synth-02:31, :107, :198, :443. All four now say: no new mechanism, `bmad install`/`--version`/`--help` pass through, Stage 0 only, C only for a new, separately named command. This matches synth-03:130, :336 and synth-04:134, :158.
- Grep of `synthesis/` for "evaluates the predicate", "then installs", "predicate, then", "A alone fails", "so A alone", "Which of B, C, D": 0 matches (reproduced, not taken from the fix log).
- Cited basis R03:327 re-read: it does say the wrapper must pass `bmad install` and `bmad --version`/`--help` through unchanged and lists the 3 subcommands. Supported.
- Residual (MINOR): synth-03:123 (Option C Description) still says the wrapper "evaluates FIRST_USE(P) ... and runs the common install command before doing what the user asked", which step 2 (:130) then restricts to a new command name only.

### Finding 3 (synth-03 Option A vs Stage 0) - NOT RESOLVED BY SUBSTANCE (see V-1)
- The places now agree in wording (synth-03:86, :262, :311-313, :331, :365; synth-04:344). The contradiction was removed by redefining terms, not by evidence (details in V-1).

### Finding 2 (synth-04 F-01 only via Phase 4) - PARTLY RESOLVED (see V-2)
- Fixed and confirmed by reading: gap row F-01 (:25), Phase 3 "Conditional on a built branch" (:114), Phase 5 intro (:178) and step titles 5.2-5.4 (:185-187), step 6.1 (:246), step 6.7 (:252), checklist :319, :327-:331, :333-:334.
- Same defect class left in place elsewhere in the plan (V-2).

## Check (b): claims stronger than evidence; recommendation, plan, gap table consistent

### V-1 (IMPORTANT, blocking): "Stage 0 satisfies the CLI reading" is an unlabelled author judgement, and the A-versus-Stage-0 distinction is wording only
- Locations (all read): synth-03:86 (Option A Cons), :262 (Table 1 A cell), :311-313, :331 (Rationale 1), :365 (Dependence row 1); synth-04:341-343 (row 1 Impact), :344 (row 2), :345 (row 3); synth-02:31, :107, :443.
- Problem 1, claim beyond evidence: these places state flatly that the existing `bmad install` "already satisfies" / "satisfies this reading". No research file says that. The only research source, R03:327, says the wrapper must pass `bmad install` through and that skills "are not reachable by this option until the user has run some `bmad` command first". Only synth-03:130 labels the inference ("a consequence of the cited constraints, not a research statement"); the label was not carried to the other places. Running `bmad --help` in a never-BMAD project creates nothing; only an explicit `bmad install` does, which is the status quo that Option A itself describes as "Nothing is created on first use" (synth-03:67, :86).
- Problem 2, resolved by wording: "Option A alone does not satisfy, Stage 0 does" (synth-03:365, synth-04:344). Stage 0 (a) is decision records and (c) is a written specification; synth-04:280 says Stage 0 has "None at run time". The run-time behaviour of "A alone" and of "Stage 0" is identical (the manual command), so the distinction carries no substance. The cycle-1 contradiction (N-3) was removed by redefining "Stage 0", not by evidence.
- Problem 3, rule conflict: task file line 164 says each reading implies a mechanism (CLI = option C); line 161 says nobody may guess an answer; synth-04:339 says "Nothing in this section is answered by the author". Q2(a) in synth-04:344 now embeds the author's answer that nothing needs building for that reading, and asks the owner only whether a new command name is wanted, not whether a manual `bmad install` meets the 2026-11-07 decision.
- Required fix: (1) at every place above, mark it "synthesis inference: the only mechanism found for this reading is the existing manual `bmad install` or a new command name; whether that meets the owner's decision is the owner's call"; (2) delete the "A alone fails / with the rest of Stage 0 holds" distinction, or state it as "Stage 0 adds records and a specification, not run-time behaviour"; (3) add to Q2(a) the owner sub-question "does running `bmad install` by hand count as creation on first use".

### V-2 (IMPORTANT, blocking): the plan is still inconsistent under the CLI reading (same defect class as finding 2)
- synth-04:30 (gap row F-06) closes F-06 via "Phase 5, steps 5.2 to 5.5", but synth-04:178 says those steps "have no target and are not added" under the CLI reading, and :327-:328 make them conditional. The gap table says closed; the plan says not built.
- synth-04:29 (F-05) closes via Phase 3 step 3.3 (a shipped block prints the broken-install message); under the CLI reading no block ships (:114). synth-04:32 (F-08) closes via Phase 4 steps 4B.4/4D.3 with no CLI-reading statement.
- synth-04:268-270 (Phase 7 steps 7.8, 7.9, 7.10) are unconditional: "A project that already has `_bmad/` ... is never touched ... FIRST_USE(P)", "first use never reinstalls it", "the block reports the install as incomplete". Under the CLI reading there is no FIRST_USE(P) enforcement and the manual command stays unguarded (F-04, :28), so "never touched" is stronger than the evidence.
- synth-04:125 heading says "exactly one branch", against :19 ("at most one"), :134 ("No branch") and :320 ("At most one").
- synth-03:323 (Stage 2 "inside the plan") says "Add the missing delivery proof for the chosen option" with no condition; under the CLI reading nothing is chosen.
- Required fix: add the same "only if a Phase 4 branch is built; under the CLI reading with no new command, none" condition to rows F-05, F-06, F-08 (:29, :30, :32), steps 7.8-7.10, the Phase 4 heading ("at most one") and synth-03:323.

## Check (c): Feasibility statement and both owner questions

- Feasibility statement present at synth-03:341-347 (heading at :341 lacks the preceding blank line, a MINOR format note already known as N4). Quoted evidence re-checked: R01:386 ("a non-interactive install is ..."), R01:79 ("NO consumer of `global_target_dir`"), R03:178-180 (both "NEEDS OTHER-REPO CHANGE: NO" lines and the "would become YES" sentence). All match. Stop condition "not triggered" is consistent with synth-04:17 and :346. PASS for this sub-check.
- Q1 present and unanswered at synth-03:361 and synth-04:343 (decision text matches task file line 163). PASS.
- Q2 present and unanswered at synth-03:361 and synth-04:344, but see V-1: Q2(a) now contains the author's position. Q2(b) is reworded ("named bootstrap skill") with the task-file wording kept in a parenthesis; accepted as a disclosed rewording (M-1 stays MINOR).

## Notes (MINOR, not blocking, not rechecked later)
- synth-03:123 Option C Description still describes the wrapper as evaluating the predicate and installing before the user's command (see Finding 1 residual).
- synth-04 table 5.1 row `test-57:331-336` points at "step 5.3 case f" for all branches although step 5.3 is conditional.
- synth-02:80 says "a new test row is needed in every case"; under the CLI reading synth-04:178 adds none.
- Known and unchanged: M-1, M-2, N1, N3, N4 from the consolidated findings.

## Self-Audit
- Files read: both inputs in full; synth-03 lines 1-400 and synth-04 lines 1-474 in full (two paged reads each); synth-02 lines 25-115 and 436-463; research/03 lines 174-181, 193-195, 325-327; research/01 grep hits at lines 79 and 386; task file lines 161-164.
- Searches reproduced by me: Grep of `synthesis/` for the stale phrases (0 matches); Grep for "exactly one (branch|trigger)" (found synth-04:125 against :19, :134, :320); Grep of R01 and R03 for the quoted Feasibility evidence (lines matched); Grep of synth-01 for wrapper/option C wording (no stale mechanism text).
- Claims independently verified: 3 fix-log findings re-read at their edited locations; 11 Feasibility/Q1/Q2 citations; 14 line references used in V-1 and V-2.
- Not verified (UNVERIFIED): the fix log's claim that synth-01 was restored byte for byte (not diffed); product code and tests were not opened (out of scope for this check); no test or installer was run.
- Why two blocking findings and not zero: the fixes made wording agree, but V-1 shows the agreement rests on an inference no research file states and on a distinction (A alone vs Stage 0) with no run-time difference, and V-2 shows five places that still contradict the new CLI-reading position. Tool engagement: Read 14 | Grep 9 | Glob 1 | Bash 0. Read+Grep+Glob calls (24) exceed the number of checks made (3 checks, about 25 sub-claims), so the suspect-review rule is not triggered.
- Confidence: Verified 3/3 checks | Unverifiable 0 | Unchecked 0 | Confidence 100% (of checks made; check (a) and (b) FAIL, check (c) PASS).

## Verdict: FAIL

- Blocking issues unresolved or new: 2 (V-1 IMPORTANT, V-2 IMPORTANT). CRITICAL 0, IMPORTANT 2, MINOR 4 (notes).
- Finding 1 resolved; finding 2 partly resolved; finding 3 not resolved by substance.
- This was the last allowed fix cycle (review 2 of 3 per the consolidated findings file): the gate HALTS and goes to the user.

**Status:** Complete

