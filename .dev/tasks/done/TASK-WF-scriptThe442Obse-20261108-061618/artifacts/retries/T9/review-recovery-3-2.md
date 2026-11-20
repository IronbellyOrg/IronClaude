Earlier blocking findings: none given (first review, prior-findings slot empty).

T9.AC1 met. Citations:
- T9.AC1@.dev/issues/442/observation-runbook.md:765 and :764 hold the new wording. `grep -n 'not representative'` prints nothing (rc=1). `grep -n 'must be.*typed by a person'` prints nothing (rc=1). `grep -c 'orca terminal send'` prints 1 (line 765).
- Line 769 now says the LL-TAMPER block applies only to a governed session, so the release `rm` is run from the driving agent's own shell. Line 767 names `gh_fork api ... -X PUT` (session-gov.sh:421, :423, both checked against the live lines). Line 764 records the owner authorization of 2026-11-08 for T1 to T4 and cites plan Constraints line 19 (checked, and the plan's line 24 backs the :765 citation).
- Section 6 starts at .dev/issues/442/observation-runbook.md:837 and ends at :860. It names all 20 `.sh` files in /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/ (cleanup, cleanup-selftest, driver, driver-helpers, driver-selftest, evidence, evidence-selftest, lib, lib-selftest, runbook-selftest, selftest, session-a, session-a-selftest, session-a2, session-gov, session-gov-selftest, setup, setup-github, setup-github-selftest, setup-selftest), plus `prompts/`. It names no missing script.
- The run order is at :839-848. The `--apply` rule is at :850 (cleanup.sh:3, :21 checked). The `NEEDS_INPUT` and `BLOCKED login-isolated-home` stops are at :852-858 (driver.sh:56/58/102, driver-helpers.sh:35, setup.sh:169-170 all checked).
- Handoff: .dev/issues/442/handoff-runbook.md:63 is the new paragraph under "What is left". It says the scripts exist and the live run is Task 10.

T9.AC2 met. Citations:
- T9.AC2@.dev/issues/442/scripts/runbook-selftest.sh:15-88 and selftest.sh:133 (the T9 hook).
- I did not run selftest.sh (outside the read-only command list). Instead I re-derived every runbook-dependent check by hand.
  - Each quoted fragment in sections 4.2 and 6 is on the script line it cites.
  - No cited file is a self-test.
  - There are more than 6 pairs.
  - Every section 6 line carries a citation.
  - The anchors match: runbook 228 `### 2.1 Session `, 505 `# F1:`, 520 `jq -sr '(map(`, 536 `#### 2.2.1 Ses`, 698 `## 3.`.
  - The other self-tests read runbook lines 62-136, 228-472, 505-520 and 536-697. All of those lie before the edited block (762 onward), so the edit did not shift them.
  - `bash -n` passes on every script in the folder.
- The saved evidence .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/t9-selftest.txt:341 prints `SELFTEST_OK` and has no FAIL line. Its mtime (2026-11-17 08:16) is older than the runbook (2026-11-18 19:00) and evidence.sh (2026-11-18 22:48). So it is not proof for the current tree, and the orchestrator should re-run `bash .dev/issues/442/scripts/selftest.sh` once.

Findings (none blocking):
F1.1 ac=T9.AC2 at=.dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/t9-selftest.txt:341 anchor=none chk=n,n,n,n family=stale-evidence fix=re-run selftest.sh on the current tree and refresh the artifact: the saved SELFTEST_OK output predates later edits to the runbook and to evidence.sh
F1.2 ac=T9.AC1 at=.dev/issues/442/observation-runbook.md:850 anchor=none chk=n,n,n,n family=thin-apply-rule fix=optional: add one clause saying `--apply` is refused until observation-results.md exists, since `REFUSED apply` is quoted but not explained: the rule is stated (default prints and deletes nothing; `--apply` acts) so the AC is met
