# B-CTX feasibility verdict (issue #394)

This verdict is an evidence review of existing artifacts. It is not the live log-only probe of design section 14 step 0. A person can run the live observation later with the existing opt-in probe `tests/hooks/fixtures/launch_level/live_probe.py`. No new probe was run against a live session by this task.

Evidence read:
- E = `.dev/tasks/done/TASK-WF-authorizedNarrow-20261106-214325/artifacts/identity-integration-evidence.md` (24 lines)
- J = `.dev/tasks/done/TASK-WF-authorizedNarrow-20261106-214325/artifacts/live-harness-events.jsonl` (6 rows: rows 1-3 governed run, rows 4-6 ordinary run)
- D = `docs/designs/sc-issue-launch-level-hook.md` sections 14 and 19.1 to 19.7
- T = `tests/hooks/test_launch_job_identity.py` and the header of `src/superclaude/hooks/scripts/launch-job-identity.sh`

## Evidence table (cases listed under "OB-CTX / B-CTX completion evidence", D:504)

| Case | Status | Evidence |
|---|---|---|
| Main session | observed | J rows 1-3 (governed Bash rewritten without a permission decision, selector returns the original session UUID, CLI exit 0); E:7 |
| Subagent | unobserved | E:19 says nested-subagent event variants were not observed; no row of J is a subagent call |
| Nested subagent | unobserved | E:19; D:563 |
| Background Bash to Git | simulated | E:10 (old governed background jobs refused in real-Git fixtures, subprocess tests, integration-tests.log:12-27 cited there); test T:1292 (test_real_git_old_governed_background_human_same_clone_reset_and_release) |
| Monitor to Git | unobserved | E:17 lists Monitor outside the supported contract; D:563 |
| Same-worktree human terminal | simulated | E:10 (concurrent same-clone human pushes to main and master selected ordinary and advanced the fixture refs); test T:1292 (same test as above, human terminal case); not a live Claude session |
| Ordinary Claude session | observed | J rows 4-6 (unchanged input hash, no rewrite, selector ordinary, exit 0); E:7 |
| Detached or reparented job | simulated, with a stated limit | E:12 (deliberate setsid escape was unselected and advanced the local fixture main; killed-supervisor identity was unknown); tests T:1430 (test_real_git_deliberate_setsid_escape_is_unselected_not_retained) and T:473 (test_intentional_new_session_escape_explicitly_unselected) |
| Launch wrapper | unobserved | E:19 says claim launcher provisioning and the effective-runtime preflight remain the next integration step |
| Process exit and PID reuse | simulated | D:563 (controlled subprocess tests exercise stale process data); tests T:318 (test_old_orphan_keeps_origin_new_ordinary_and_forged_environment_do_not) and T:362 (test_corrupt_or_stale_job_record_is_unknown_not_human); not a live observation |
| Resume in a new process | simulated | E:10 (two new jobs for the same logical id were both recognized, "labelled controlled resume rather than CLI resume"); real CLI resume unobserved, E:19; test T:1399 (test_real_git_controlled_resume_same_logical_id_new_job_not_live_cli_resume) |
| /clear and fork | unobserved | E:19; D:563 |
| Release while a job is alive | simulated | E:10 (after explicit release the old jobs reported ordinary/released and the fixture refs advanced); tests T:421 (test_release_live_job_and_invalid_bound_state) and T:1292 |

Observed: 2 of 13 rows. Simulated: 6. Unobserved: 5. No row is claimed as passed beyond what the cited artifact shows.

## L1 verdict

L1: PROCEED

Reason: the L1 text guard identifies a session by the top-level `session_id` of the hook payload, and the identity foundation already shows a top-level string id on a governed and on an ordinary actual CLI call (J rows 1 and 4, E:7). B-CTX concerns the process-context selector that the L2 pre-push layer needs (D:491-506), so it does not block writing the L1 script. The ship gate U1 (D:201) stays pending: no real governed launch at `full` or `--submit` until OB-H1 item 1 shows the parent `session_id` in subagent and nested-subagent payloads.

## L2 verdict

L2: BLOCKED

Missing launcher or harness integration, named exactly: (1) a live observation of subagent, nested-subagent, background-Bash-to-Git and Monitor-to-Git process trees with the same-worktree human terminal at the same time; (2) a live observation of resume in a new Claude process, `/clear`, fork and auto mode (E:19); (3) the claim launcher provisioning the governed level record for the actual logical session and checking the adapter runtime before it advertises protection (E:19, D:565); (4) a verified install place for the shared `hooks/pre-push` file (U28, D:377,457). Until these exist, L2 cannot be built or claimed.

## F7 result: design evidence files that are absent from this tree

Checked on 2026-11-07 with a file-existence test in the working tree of this branch:

| File named by the design | Where named | Exists |
|---|---|---|
| `.dev/brainstorms/20261105-170229-launch-level-hook/spec-panel-20261106/review.md` | D:19 | no |
| `.dev/brainstorms/20261106-l2-prepush-decisions/q1-install-place/run-4/merged-answer.md` | D:540 | no |
| `.dev/brainstorms/20261106-l2-prepush-decisions/q2-chaining/run-4/merged-q2-answer.md` | D:541 | no |
| `.dev/brainstorms/20261106-l2-prepush-decisions/q3-removal/run-4/merged-answer.md` | D:542 | no |
| `.dev/brainstorms/20261106-l2-prepush-decisions/q4-testing/run-4/answer-merged.md` | D:543 | no |

`git log --all` shows no commit touching `.dev/brainstorms/20261106-l2-prepush-decisions`. Design statements that depend on these files are unverified: the panel findings and the full guard boundary table (D:19), the placement and chaining choices of section 19.2 (D:510-514), the removal behaviour of section 19.4 and the test target of section 19.5 (D:540-543). No file was invented or recreated.
