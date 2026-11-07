## Round 2: Rebuttals

Orchestrator-verified fact given to all rebuttal advocates: the implement protocol's Q6 step (`/home/coder/.claude/skills/sc-implement-protocol/SKILL.md:132-154`) runs lint, typecheck and tests after each task as extras, records pass, fail or unrelated-red, and never changes the task verdict; the whole-list final review is advisory.

### Variant 1 Advocate (sonnet), rebuttal

**Responses to criticisms.**
- C-001 and C-002 conceded as Drift (plan omissions; the final state is correct), not Regression.
- Q6 makes the red windows visible but non-gating, and runs after the verdict. It would probably record the C-001 red as `unrelated-red`, because the failing file test_issue_protocol.py does not overlap the touched files of Tasks 1, 2, 3, 5 or 6 (SKILL.md:154); the executor sees a weak signal.
- C-003 and C-005 conceded as inherited design defects: source.md:158 and :195 need a tracked-file fact the worktree output (source.md:177) does not carry; source.md:350 gives ST-4 no matching rule.
- C-008 conceded to V2: a timeout writes no `launch` entry, so a re-run is not caught by `already_launched`; only the dropped "check Orca before re-running" text (source.md:211, D9 at :377) guards against a duplicate agent.

**Updated assessment.**
- C-001 self-heals: Task 4's acceptance runs the whole test_issue_protocol.py (plan:89), which gates the script row; the template row's window ends at the Task 7 gate (plan:133). The fix is a one-line table row in files the plan already edits.
- C-002 is different: the write-verb tests (test_worker_contract.py:2199-2208) fail with certainty, the fix is a classification entry in a test file no task names, and Task 7's acceptance (`tests/skills`) catches it late with no instruction on the fix.
- C-007: description (SKILL.md:3) LOW; SKILL.md:87-88 stale on steps 6 and 7 is MEDIUM because Task 4 touches step 7 only to "continue to the worktree step" and Task 7 never adds the Wave 5 prompt call or Wave 8 to those steps, so a reader following SKILL.md stops before the launch.
- A-003 QUALIFY; A-005 REJECT as a universal rule.

**New evidence.** New issue (LOW): Task 4 and Task 7 both rewrite the same Wave 6 hand-off (plan:84, plan:128). Task 4's text points to "Wave 8, added by a later task", its ST-6 check may pass against text that Task 7 replaces, and no task owns the final wording.

**Final positions.** C-001 Drift / MEDIUM / plan finding. C-002 Drift / HIGH / plan finding (guaranteed failure, unnamed file, caught late). C-003 Drift / LOW-MEDIUM / inherited design defect. C-005 Drift / LOW-MEDIUM / inherited design defect. C-007 description LOW, steps 6 and 7 MEDIUM / plan finding. C-008 Drift / MEDIUM / plan finding. New (Wave 6 double rewrite) Drift / LOW / plan finding.

### Variant 2 Advocate (haiku), rebuttal

**Responses.** (a) Accepts C-001 and C-002 as Drift, not Regression: C-001 MEDIUM (later inventory gates require repair); C-002 HIGH as a planning omission (the new prose certainly triggers the exact-line classification, test_worker_contract.py:1155-1161, and no task names the classification file; HIGH describes certain late repair, not certain defective delivery, and non-gating extras do not resolve it). (b) C-008 stays MEDIUM (source.md:211-213 requires timeout recovery advice and keeping the pending state after a shim failure; losing it risks duplicate or ungoverned agents). Concedes C-007's operational summary deserves MEDIUM while the description stays LOW (SKILL.md:87-88 omits prompt generation and stops). (c) The Task 4 / Task 7 overlap on the Wave 6 hand-off is real but not a separate defect: plan:124-133 makes Task 7 depend on Task 4, assigns the final wording to Task 7 and reruns the skill tests, which contradicts "no task owns final wording".

**New evidence.** None found.

**Final positions.** C-001 Drift / MEDIUM. C-002 Drift / HIGH. C-008 Drift / MEDIUM. C-007 Drift / LOW description, MEDIUM operational steps. Wave 6 overlap: no demonstrated deviation. New issue: none.

### Variant 3 Advocate (opus), rebuttal

**Responses.** (a) Accepts Drift MEDIUM for C-001 and Drift HIGH for C-002; its own Regression HIGH becomes Drift MEDIUM. C-001 clears itself (Task 4 runs the whole test_issue_protocol.py, plan:89; Task 7 runs tests/skills, plan:133). C-002 is worse: `_check_all_classified` (test_worker_contract.py:1155-1161) fails on every unclassified `git push`, `git commit` or `gh pr` line over skills and commands (:1090-1101); the design's change table (source.md:309-310) leaves that test file out; the first gate that catches it is Task 7 and nothing tells the executor how to fix it; per-task extras would probably record it as `unrelated-red` (implement SKILL.md:154), a weak signal. (b) Advocate 2 is right on the Wave 6 hand-off: Task 4 writes a temporary hand-off (plan:84), Task 7 depends on Task 4 (plan:124) and replaces it with the final output of design section 7 (plan:128, source.md:147, :155); the only leftover is that ST-6 never gets its Wave 8 half, already part of C-006. (c) Withdraws most of C-011: the implement protocol detects `make lint` and runs it after every task (SKILL.md:146; Makefile:48-50), never changing a verdict (SKILL.md:152); the format check is not among the per-task extras so `ruff format --check` runs only in Task 9 (a note); "Task 2 too large" stays as advice; moving design-doc edits to Phase 3 differs from source.md:405 but is Drift LOW as both phases ship in one PR.

**New evidence (Drift, LOW, fix in the plan).** Design source.md:194 says a create that times out must be followed by a second list while a nonzero exit fails at once; Task 1's `run()` helper returns the same failed result for a timeout, a nonzero exit and a missing binary (plan:34); Task 2 needs to tell them apart (plan:56) and no FO case tests a create timeout (plan:62; FO-11 covers opaque JSON and zero or two new ids); the wording at source.md:165 "a timeout is a failed command" encourages the merge. Effect: a worktree created during a timeout is reported `failed` with no record; a rerun recovers it through the marker lookup.

**Final positions.** C-001 Drift/MEDIUM, plan only (add the files-table rows in Tasks 1 and 5). C-002 Drift/HIGH, plan (name test_worker_contract.py in Tasks 2, 5 and 7) then add the file to source.md:309-310. C-003, C-004, C-005, C-013 Drift/MEDIUM, change the design (source.md) first. C-006, C-007 (steps MEDIUM, description LOW), C-008 MEDIUM, C-009 MEDIUM, C-010 LOW: plan only, the design already says what is needed. Wave 6 overlap: no separate defect, folded into C-006. C-011 note/LOW, plan only. New create-timeout item Drift/LOW, plan (Task 1 marks timeouts, Task 2 adds a create-timeout FO case), optionally reword source.md:165.

## Round 2 convergence

After Round 2 every diff point has a stated final class, severity and fix location with no remaining disagreement between the three advocates, except one wording dispute (Wave 6 overlap: real overlap, no separate defect). Points moved by rebuttal: C-001 and C-002 Regression -> Drift (X-001 closed); C-003 and C-005 plan finding -> inherited design defect; C-007 split (description LOW, steps MEDIUM; X-002 closed); C-008 MEDIUM (X-003 closed); ARG-1 part of C-006 LOW-to-MEDIUM kept at the C-006 level (X-004 closed); C-011 reduced to a note; new item N-001 (create timeout, LOW). Convergence: 25 of 25 diff points = 1.00 (threshold 0.80).
