# Adversarial Debate Transcript

## Metadata

- Depth: standard
- Rounds completed: 2 (Round 1 statements, Round 2 rebuttals) plus Round 2.5 invariant probe; Round 3 not run (depth standard)
- Convergence achieved: 100% (25 of 25 diff points have an agreed class, severity and fix location)
- Convergence threshold: 80%
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 3 (sonnet, haiku, opus)
- Source parts kept as separate files: `debate-round1.md`, `debate-round2.md`, `invariant-probe.md`; they are reproduced below (Round 1 and 2) or referenced (probe)

## Round 1: Advocate Statements

Condensed from the three advocate returns (sonnet for V1, haiku for V2, opus for V3). Per-point lists are complete; prose sections are shortened without dropping any claim.

### Variant 1 Advocate (sonnet, analyzer)

**Position.** V1 is strongest on correctness: it alone found the write-verb audit (C-002), the single launch warning field (C-004) and the ST-4 collision as a full finding. V3 is better on dependency order and on how to classify the red window; V2 is thin but accurate.

**Steelman V3.** Plan-structure integrity: no task depends on Task 3 although Tasks 7 and 9 consume its flags and STOP codes (plan:124, plan:153); V1 called the order "sound". V3 also found the `--repo` ban in test_issue_command.py:99-103 and the fork-safety template gap. **Steelman V2.** Precision (no wrong citations); the dropped-safeguards finding at MEDIUM is right because a timeout without "check Orca" can create duplicate agents; the only card to flag the Orca-dependency constraint.

**Strengths.** C-002 verified (AUDIT_ROOTS covers skills/commands/agents; WRITE_VERB_RE matches git commit/push/add and gh pr; the plan folder has no mention of test_worker_contract). C-001 verified at test_issue_protocol.py:131-141. C-003 and C-004 interface gaps. ST-4 as a finding with exact colliding lines. `-k "FO or worktree"` selects the whole module.

**Weaknesses of others.** V2 misses both HIGH items, C-004, ST-4, the Task 3 edge; its zero-Regression count understates risk. V3 misses C-002 and overstates ARG-1 (Task 1 has a bad-subcommand case) and spends three findings on LOW organisation points.

**Concessions.** V1 missed C-009 and the `--repo` trap and C-013; labelling C-001 Regression HIGH is a stretch (Drift is more accurate); C-002 is a plan omission (Drift HIGH would be stricter); finding 6 bundles four pins.

**Shared assumptions.** A-002 QUALIFY (design silent on launch shape and warning precedence); A-003 ACCEPT; A-004 QUALIFY; A-005 QUALIFY.

**Per-point positions.** S-001 V1/V3; S-002 merge; C-001 V1; C-002 V1; C-003 V1; C-004 V1; C-005 V1; C-006 merge; C-007 V3; C-008 V2; C-009 V3; C-010 V2; C-011 V3; C-012 V1; C-013 V3; C-014 V1; C-015 V1; X-001 merge; X-002 V3; X-003 V2; X-004 V2; A-002..A-005 as above.

### Variant 2 Advocate (haiku, qa)

**Position.** V2 is strongest on launch-safety omissions and restrained classification, not completeness.

**Steelman V1.** Fidelity includes existing repository contracts: the exact-line classification audit (test_worker_contract.py:1155-1161 rejects unclassified lines) can survive into final delivery and matters more than a transient inventory failure. **Steelman V3.** Dependencies and orchestrator summaries are executable instructions: plan:124 omits Task 3 while plan:130 requires matching its text; F4 catches the Wave 8 summary.

**Strengths.** F1 MEDIUM justified (D:211 requires "check Orca" and the ungoverned-hand-command warning); LA-7 separate from ARG-1; ARG-1 LOW because Task 1 and Task 5 already require exit-2 cases; the Orca-dependency constraint.

**Weaknesses of others.** V1 F1 and V3 F1 overstate HIGH Regression for a planned intermediate state; V3 F9 (no early lint gate) is qualified because the implement protocol runs extras per task (sc-implement-protocol SKILL.md:132-154) though they do not change the verdict; V3 F10 is organisational advice.

**Concessions.** V2 missed inventory ordering, the write-verb audit, the warning ambiguity, ST-5/ST-6, the Task 3 edge, stale command text and the fork-scan gap; those misses weaken completeness.

**Shared assumptions.** A-002 QUALIFY; A-003 REJECT (per-task extras exist beyond the acceptance checks, though they cannot change a verdict); A-004 QUALIFY (immutability starts at first task start, implementation repairs are allowed: managed-workspace.md:44); A-005 REJECT (no universal green-between-tasks requirement).

**Per-point positions.** S-001 merge; S-002 V2; C-001 merge; C-002 V1; C-003 V3 (advisory); C-004 V1; C-005 V3 (advisory); C-006 merge; C-007 merge; C-008 merge (V2 severity); C-009 V3; C-010 V2; C-011 merge; C-012 V1; C-013 V3; C-014 V1; C-015 V1; X-001 merge; X-002 merge (description LOW, flow omissions higher); X-003 V2; X-004 V2; A-002..A-005 as above.

### Variant 3 Advocate (opus, refactorer)

**Position.** V3 reads the plan's structure most closely: the only card with C-009, the `--repo` trap (U-004) and C-013; it grades stale SKILL.md text as a contract mismatch. Weaknesses: it missed C-002 and gave its one Regression label to a transient red test.

**Verified facts.** test_issue_protocol.py:131-141 (C-001); plan:97, :124, :153 (no task depends on Task 3); test_issue_command.py:102 `assert "--repo" not in text`; test_worker_contract.py:1098-1101 and :2199-2206 confirm C-002; plan:42 asks Task 1 to test a missing required argument that `preflight` does not have.

**Steelman V1.** Strongest on runtime consequence: every new `git push`, `git commit` or `gh pr` line must be classified by exact text and no task says so; also C-004, C-012 and the precise ARG-1 point. **Steelman V2.** Highest citation accuracy and widest unit count; right to grade C-008 MEDIUM; sole finder of C-010.

**Strengths.** C-009; U-004; C-007 including the Wave 8 part of claim step 7; C-013 (the submit block's "check that no PR is already open" implies a gh pr call that needs --repo and is also a write-verb hit); C-005 whole-token rule (`--pr` prefixes `--prompt`).

**Weaknesses of others.** V1 calls the order sound yet plan:124/153 show the gap; V2 misses both confirmed test breaks and treats ARG-1 as LOW although plan:42 asks for an unwritable test.

**Concessions.** V3 missed C-002 (High); finding 1 should be Drift HIGH, not Regression; finding 5 overstated (Task 5 tests one exit-2 case, plan:103); the _FORK_FILES scope claim was not confirmed by the calibrator; C-008 deserves MEDIUM.

**Shared assumptions.** A-002 QUALIFY (C-003 and C-005 show design defects that must go back into source.md); A-003 ACCEPT (every acceptance check in Tasks 1 to 6 is filtered); A-004 QUALIFY (naming the test files in Tasks 2 and 5 lets the executor fix C-002); A-005 QUALIFY (matters only for per-task commits; Drift, not Regression).

**Per-point positions.** S-001 merge; S-002 V1; C-001 merge; C-002 V1; C-003 merge; C-004 V1; C-005 merge; C-006 merge; C-007 V3; C-008 merge (V2 severity); C-009 V3; C-010 V2; C-011 V3; C-012 V1; C-013 merge; C-014 V1; C-015 merge; X-001 merge (call it Drift); X-002 V3; X-003 V2; X-004 V1 (MEDIUM); A-002..A-005 as above.

### Round 1 convergence

Every one of the 25 diff points has a majority position across the three advocates. Identical labels from all three advocates on 11 of 25 points (C-002, C-004, C-006, C-009, C-010, C-012, C-014, X-001, X-003, A-002, A-004); the other 14 are 2-to-1 or merge-compatible. Points decided 2-to-1: X-004 (LOW over MEDIUM), A-003 (ACCEPT over REJECT), A-005 (QUALIFY over REJECT). Convergence on majority agreement: 25 of 25 = 1.00. This counts agreement on the superior approach, not agreement on severity labels; severity disagreements (C-001, C-007, C-008) are carried into Round 2.

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

## Round 2.5: Invariant Probe

See `invariant-probe.md` in this folder (14 findings: 3 ADDRESSED, 11 UNADDRESSED; 1 HIGH, 6 MEDIUM, 4 LOW unaddressed). The HIGH item (INV-007, fork safety of the launch prompt) blocked convergence until it was recorded as a blocking finding; the gate result and its resolution are written in that file.

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---|---|
| S-001 | V1/V3 | 75% | Advisory channel retained; V2 has none |
| S-002 | V2 | 80% | After Round 2 all advocates dropped Regression; restraint wins |
| C-001 | V1/V3 | 85% | Both found it; Drift MEDIUM, self-heals at Task 4 / Task 7 gates |
| C-002 | V1 | 95% | Unanimous; verified at tests/skills/test_worker_contract.py:1090-1155, 2199-2208; Drift HIGH |
| C-003 | V1 | 80% | Finding with fix; design defect, design first |
| C-004 | V1 | 90% | Unanimous; unique |
| C-005 | V1 | 80% | Finding; V3 supplies the whole-token rule; design first |
| C-006 | merge | 85% | V1 grouping + V3/V2 splits; plan only |
| C-007 | V3 | 85% | Steps MEDIUM, description LOW; plan only |
| C-008 | V2 | 85% | MEDIUM agreed after Round 2 |
| C-009 | V3 | 95% | Unanimous; plan:124, plan:153 |
| C-010 | V2 | 90% | Unanimous; LOW |
| C-011 | V3 | 70% | Reduced to a note after the Q6 extras fact |
| C-012 | V1 | 85% | Unanimous; issue.md:71, :100 |
| C-013 | V3 | 85% | Plan finding; INV-007 raises it to blocking (security) |
| C-014 | V1 | 70% | LOW note |
| C-015 | V1 | 70% | LOW note |
| X-001 | merge | 90% | Drift, not Regression |
| X-002 | V3 | 80% | Split by surface |
| X-003 | V2 | 85% | MEDIUM |
| X-004 | V2 | 75% | LOW-MEDIUM; 2 of 3 advocates |
| A-002 | QUALIFY | 90% | 3 of 3; design silent on some points |
| A-003 | QUALIFY | 70% | Round 1 ACCEPT/ACCEPT/REJECT; Round 2: extras exist (non-gating, weak signal) |
| A-004 | QUALIFY | 85% | 3 of 3; implementation repairs allowed after start |
| A-005 | QUALIFY | 80% | Green needed at acceptance gates and the end |

## Convergence Assessment

- Points resolved: 25 of 25
- Alignment: 100%
- Threshold: 80%
- Taxonomy coverage: L1 4, L2 14, L3 7 points, all debated (AD-5 satisfied; no forced round)
- Invariant gate: initially BLOCKED_BY_INVARIANTS (INV-007, HIGH, UNADDRESSED); resolved by recording it as a blocking finding (B-3) in the merged card; MEDIUM items are warnings
- Status: CONVERGED (with the invariant resolution recorded in invariant-probe.md)
- Unresolved points: none; one wording dispute (Wave 6 hand-off overlap) closed as "real overlap, no separate defect"
