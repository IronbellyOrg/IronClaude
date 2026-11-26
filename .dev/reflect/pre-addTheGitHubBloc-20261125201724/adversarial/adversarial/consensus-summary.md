# Emerging consensus after Round 2 (input to the Round 2.5 invariant probe)

Per-point winners: S-001 Variant 1; C-001 Variant 1 (both cards agree on the finding); C-002 Variant 2; C-003 Variant 1; C-004 Variant 2 (as a Note); C-005 Variant 1; C-006 Variant 1; C-007 Variant 1; X-001 both (not a contradiction); A-001 and A-002 both QUALIFY.

Agreed findings and grades (the plan is .dev/tasks/to-do/TASK-WF-addTheGitHubBloc-20261125-201412/TASK-WF-addTheGitHubBloc-20261125-201412.md):

1. Blocking (Missing): no task adds the WRITE_VERB_CLASSIFICATION entry in tests/skills/test_worker_contract.py for the new `gh api` line that Task 1 puts in refs/claim.md. Add a read-only entry (exact stripped line), in the same edit as, or after, the final wording of the line; keep `gh api` out of SKILL.md, command and guide wording.
2. Blocking (Decision): Task 1's outcome rules do not say which wins on a failed call. Verified by the orchestrator: a failed read exits 1 and prints the raw error JSON on stdout (gh 2.103.0, issue 999999), so "any output line is a blocker" would STOP with E-BLOCKED on an unreadable list. Rule: check the exit status first; on exit 0 count only lines matching `^#[0-9]+ https://`; anything else is "could not run". Pin this in Task 6.
3. Medium: Task 6's ordering helper only checks the blocker item is after the closed-issue item; it should also check it is after the assignee items, with a mutation test that moves it ahead of them.
4. Medium: the held "Blocker check: could not run" line is only printed in Final output item 4; a later STOP (Waves 4 to 6) does not guarantee it.
5. Notes: wording traps in existing tests (A4, A5, A6), Wave 2 heading (A7), sync-dev and verify-sync not listed as plan steps (A8; ruled a Note because the workflow template makes final verification executor-owned and the plan's Constraints already name `make sync-dev`), `git diff --stat` wording (A9), the coverage record (Q3), and plan line 91 omits two other readers that do not break (tests/skills/test_issue_t1_fallback.py, tests/skills/test_issue_worker_agents.py).

Convergence: 10 of 11 diff points agreed (0.91); all three taxonomy levels covered.
