1524eedc4cb5189cdcb3aba419460759f4142577
Review one task for spec compliance.

Task brief: ## Task 1: Write the B-CTX feasibility verdict

Create ./artifacts/b-ctx-verdict.md. This is the design's step 0 (design sections 14 and 19.1): decide from evidence that already exists what the guard may rely on and what must wait. Evidence to read and cite by path and line: .dev/tasks/done/TASK-WF-authorizedNarrow-20261106-214325/artifacts/live-harness-events.jsonl and identity-integration-evidence.md, tests/hooks/test_launch_job_identity.py, the header of src/superclaude/hooks/scripts/launch-job-identity.sh, and design sections 19.1 and 19.7.

The file has four parts. First, an evidence table with one row for every lifecycle case listed under "OB-CTX / B-CTX completion evidence" in design section 19.1 (main session, subagent, nested subagent, background Bash or Monitor to Git, same-worktree human terminal, ordinary Claude session, detached or reparented job, launch wrapper, process exit and PID reuse, resume in a new process, /clear and fork, release while a job is alive), each marked observed (cite the artifact line), simulated (cite the test) or unobserved. Second, an L1 verdict line, either "L1: PROCEED" or "L1: STOP", with the reason; the L1 text guard identifies a session by its top-level session_id, so B-CTX does not block writing it, and the ship gate U1 (design section 7) stays pending. Third, an L2 verdict line, either "L2: GO" or "L2: BLOCKED"; GO only if every required case is observed, otherwise BLOCKED with the exact missing launcher or harness integration named. Fourth, the F7 result: state whether .dev/brainstorms/20261105-170229-launch-level-hook/spec-panel-20261106/review.md and the four answers under .dev/brainstorms/20261106-l2-prepush-decisions/ exist in this tree, and list each design statement that depends on a missing file as unverified.

No new probe is run against a live session by this task. The file states in one sentence that the verdict is an evidence review and not the live probe of design section 14 step 0, and it names the existing opt-in probe tests/hooks/fixtures/launch_level/live_probe.py as the way a person can run the live observation later.

Acceptance criteria:
- ./artifacts/b-ctx-verdict.md exists and contains the four parts above, with every row of the design 19.1 case list present.
- Every row marked observed cites an existing path and line of evidence; every case without such a citation is marked unobserved or simulated, never observed.
- The file contains exactly one line starting "L1:" and exactly one line starting "L2:", each with one of the allowed values.
- If the L2 line says BLOCKED, the file names the missing integration in one or more sentences a maintainer can act on.
- The F7 part lists the existence check result for the five named files and no file is invented or recreated.

AC ids (source order):
T1.AC1: ./artifacts/b-ctx-verdict.md exists and contains the four parts above, with every row of the design 19.1 case list present.
T1.AC2: Every row marked observed cites an existing path and line of evidence; every case without such a citation is marked unobserved or simulated, never observed.
T1.AC3: The file contains exactly one line starting "L1:" and exactly one line starting "L2:", each with one of the allowed values.
T1.AC4: If the L2 line says BLOCKED, the file names the missing integration in one or more sentences a maintainer can act on.
T1.AC5: The F7 part lists the existence check result for the five named files and no file is invented or recreated.
Global constraints: - docs/designs/sc-issue-launch-level-hook.md is the authority for this plan. The requirements file .dev/brainstorms/20261105-170229-launch-level-hook/merged-requirements.md (called MR below) is the historical baseline for requirement ids and the test corpus; where the design says it overrides MR (design section 11, DD-2), the design wins. .dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/launch-levels-addendum.md defines the claim side; the hook interface rules IR-1 to IR-7 in design section 13 win over it.
- This branch builds on open PR 425 (ironbelly/sc-issue-claim-pipeline-flag). The claim code in src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py already writes the launch record and marks the prompt (IR-1, IR-2); do not rebuild that.
- The L1 guard is one flat bash script using only bash, jq, sed and tr: exit 0 allows, exit 2 blocks, no onFailure, no Python, no git or network call on ordinary classification. No new runtime service, managed settings deployment, shell parser, hook forwarding framework or git config migration (design section 1).
- Do not change src/superclaude/hooks/scripts/launch-job-identity.sh or tests/hooks/test_launch_job_identity.py. A conflict found with it goes into the record of Task 14, not into that file.
- Ordinary sessions are never blocked by any failure (FR-L-53). Only a positively identified governed session fails closed.
- Live observations (OB-H1, OB-H2, OB-H3, OB-CTX) need real governed sessions or real launches. This plan runs none of them and never launches a governed agent on a real issue or pushes to a real protected branch. They stay pending (a skipped test with a stated reason), never reported as passed. Tests use a temporary HOME and temporary bare remotes.
- Acceptance claims cover the routes the tests exercise. Nothing here claims universal merge protection or defence against a hostile agent (design sections 1 and 12).
- Gate: Task 1 writes the B-CTX verdict. If ./artifacts/b-ctx-verdict.md contains the line "L1: STOP", stop the run at Task 1 and report that verdict; do not start Task 2 or any later task. Every task after Task 1 depends on that verdict.
- Existing tests: any task that changes a check in src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py also migrates the shared test fixture launch_scene in tests/skills/test_issue_orca_worktree.py (it writes only a bare shell stub today) and names every test whose result changes. Test code must unset CLAUDE_CONFIG_DIR and control which jq is on PATH, so results do not depend on the developer's machine.
- Edit only under src/superclaude/, plugins/superclaude/hooks/, tests/, docs/ and this package's ./artifacts/; run make sync-dev after hook or skill edits. The plugin copy of every hook script and hooks.json stays byte-identical to its src copy. Generated .claude/ mirrors made by make sync-dev stay out of the commit.
- UV only: run tests with uv run pytest.
- Findings of the issue analysis that this plan answers: F2 (Task 15), F3 (Task 14), F4 (Tasks 18 to 20), F6 (Task 22), F7 (Task 1). F5 (pending records are not pruned) is accepted under owner decision O-15 and is stated in Task 22.
Start sha: 1524eedc4cb5189cdcb3aba419460759f4142577
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/b-ctx-verdict.md b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/b-ctx-verdict.md
new file mode 100644
index 00000000..6d92c5bd
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/b-ctx-verdict.md
@@ -0,0 +1,55 @@
+# B-CTX feasibility verdict (issue #394)
+
+This verdict is an evidence review of existing artifacts. It is not the live log-only probe of design section 14 step 0. A person can run the live observation later with the existing opt-in probe `tests/hooks/fixtures/launch_level/live_probe.py`. No new probe was run against a live session by this task.
+
+Evidence read:
+- E = `.dev/tasks/done/TASK-WF-authorizedNarrow-20261106-214325/artifacts/identity-integration-evidence.md` (24 lines)
+- J = `.dev/tasks/done/TASK-WF-authorizedNarrow-20261106-214325/artifacts/live-harness-events.jsonl` (6 rows: rows 1-3 governed run, rows 4-6 ordinary run)
+- D = `docs/designs/sc-issue-launch-level-hook.md` sections 14 and 19.1 to 19.7
+- T = `tests/hooks/test_launch_job_identity.py` and the header of `src/superclaude/hooks/scripts/launch-job-identity.sh`
+
+## Evidence table (cases listed under "OB-CTX / B-CTX completion evidence", D:504)
+
+| Case | Status | Evidence |
+|---|---|---|
+| Main session | observed | J rows 1-3 (governed Bash rewritten without a permission decision, selector returns the original session UUID, CLI exit 0); E:7 |
+| Subagent | unobserved | E:19 says nested-subagent event variants were not observed; no row of J is a subagent call |
+| Nested subagent | unobserved | E:19; D:563 |
+| Background Bash to Git | simulated | E:10 (old governed background jobs refused in real-Git fixtures, subprocess tests, integration-tests.log:12-27 cited there); test T:1292 (test_real_git_old_governed_background_human_same_clone_reset_and_release) |
+| Monitor to Git | unobserved | E:17 lists Monitor outside the supported contract; D:563 |
+| Same-worktree human terminal | simulated | E:10 (concurrent same-clone human pushes to main and master selected ordinary and advanced the fixture refs); test T:1292 (same test as above, human terminal case); not a live Claude session |
+| Ordinary Claude session | observed | J rows 4-6 (unchanged input hash, no rewrite, selector ordinary, exit 0); E:7 |
+| Detached or reparented job | simulated, with a stated limit | E:12 (deliberate setsid escape was unselected and advanced the local fixture main; killed-supervisor identity was unknown); tests T:1430 (test_real_git_deliberate_setsid_escape_is_unselected_not_retained) and T:473 (test_intentional_new_session_escape_explicitly_unselected) |
+| Launch wrapper | unobserved | E:19 says claim launcher provisioning and the effective-runtime preflight remain the next integration step |
+| Process exit and PID reuse | simulated | D:563 (controlled subprocess tests exercise stale process data); tests T:318 (test_old_orphan_keeps_origin_new_ordinary_and_forged_environment_do_not) and T:362 (test_corrupt_or_stale_job_record_is_unknown_not_human); not a live observation |
+| Resume in a new process | simulated | E:10 (two new jobs for the same logical id were both recognized, "labelled controlled resume rather than CLI resume"); real CLI resume unobserved, E:19; test T:1399 (test_real_git_controlled_resume_same_logical_id_new_job_not_live_cli_resume) |
+| /clear and fork | unobserved | E:19; D:563 |
+| Release while a job is alive | simulated | E:10 (after explicit release the old jobs reported ordinary/released and the fixture refs advanced); tests T:421 (test_release_live_job_and_invalid_bound_state) and T:1292 |
+
+Observed: 2 of 13 rows. Simulated: 6. Unobserved: 5. No row is claimed as passed beyond what the cited artifact shows.
+
+## L1 verdict
+
+L1: PROCEED
+
+Reason: the L1 text guard identifies a session by the top-level `session_id` of the hook payload, and the identity foundation already shows a top-level string id on a governed and on an ordinary actual CLI call (J rows 1 and 4, E:7). B-CTX concerns the process-context selector that the L2 pre-push layer needs (D:491-506), so it does not block writing the L1 script. The ship gate U1 (D:201) stays pending: no real governed launch at `full` or `--submit` until OB-H1 item 1 shows the parent `session_id` in subagent and nested-subagent payloads.
+
+## L2 verdict
+
+L2: BLOCKED
+
+Missing launcher or harness integration, named exactly: (1) a live observation of subagent, nested-subagent, background-Bash-to-Git and Monitor-to-Git process trees with the same-worktree human terminal at the same time; (2) a live observation of resume in a new Claude process, `/clear`, fork and auto mode (E:19); (3) the claim launcher provisioning the governed level record for the actual logical session and checking the adapter runtime before it advertises protection (E:19, D:565); (4) a verified install place for the shared `hooks/pre-push` file (U28, D:377,457). Until these exist, L2 cannot be built or claimed.
+
+## F7 result: design evidence files that are absent from this tree
+
+Checked on 2026-11-07 with a file-existence test in the working tree of this branch:
+
+| File named by the design | Where named | Exists |
+|---|---|---|
+| `.dev/brainstorms/20261105-170229-launch-level-hook/spec-panel-20261106/review.md` | D:19 | no |
+| `.dev/brainstorms/20261106-l2-prepush-decisions/q1-install-place/run-4/merged-answer.md` | D:540 | no |
+| `.dev/brainstorms/20261106-l2-prepush-decisions/q2-chaining/run-4/merged-q2-answer.md` | D:541 | no |
+| `.dev/brainstorms/20261106-l2-prepush-decisions/q3-removal/run-4/merged-answer.md` | D:542 | no |
+| `.dev/brainstorms/20261106-l2-prepush-decisions/q4-testing/run-4/answer-merged.md` | D:543 | no |
+
+`git log --all` shows no commit touching `.dev/brainstorms/20261106-l2-prepush-decisions`. Design statements that depend on these files are unverified: the panel findings and the full guard boundary table (D:19), the placement and chaining choices of section 19.2 (D:510-514), the removal behaviour of section 19.4 and the test target of section 19.5 (D:540-543). No file was invented or recreated.

Delta diff from the previous reviewed tree (empty on the first review): diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/b-ctx-verdict.md b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/b-ctx-verdict.md
index 641408f1..6d92c5bd 100644
--- a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/b-ctx-verdict.md
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/b-ctx-verdict.md
@@ -15,16 +15,16 @@ Evidence read:
 | Main session | observed | J rows 1-3 (governed Bash rewritten without a permission decision, selector returns the original session UUID, CLI exit 0); E:7 |
 | Subagent | unobserved | E:19 says nested-subagent event variants were not observed; no row of J is a subagent call |
 | Nested subagent | unobserved | E:19; D:563 |
-| Background Bash to Git | simulated | E:10 (old governed background jobs refused in real-Git fixtures, subprocess tests, integration-tests.log:12-27 cited there); T |
+| Background Bash to Git | simulated | E:10 (old governed background jobs refused in real-Git fixtures, subprocess tests, integration-tests.log:12-27 cited there); test T:1292 (test_real_git_old_governed_background_human_same_clone_reset_and_release) |
 | Monitor to Git | unobserved | E:17 lists Monitor outside the supported contract; D:563 |
-| Same-worktree human terminal | simulated | E:10 (concurrent same-clone human pushes to main and master selected ordinary and advanced the fixture refs); not a live Claude session |
+| Same-worktree human terminal | simulated | E:10 (concurrent same-clone human pushes to main and master selected ordinary and advanced the fixture refs); test T:1292 (same test as above, human terminal case); not a live Claude session |
 | Ordinary Claude session | observed | J rows 4-6 (unchanged input hash, no rewrite, selector ordinary, exit 0); E:7 |
-| Detached or reparented job | simulated, with a stated limit | E:12 (deliberate setsid escape was unselected and advanced the local fixture main; killed-supervisor identity was unknown) |
+| Detached or reparented job | simulated, with a stated limit | E:12 (deliberate setsid escape was unselected and advanced the local fixture main; killed-supervisor identity was unknown); tests T:1430 (test_real_git_deliberate_setsid_escape_is_unselected_not_retained) and T:473 (test_intentional_new_session_escape_explicitly_unselected) |
 | Launch wrapper | unobserved | E:19 says claim launcher provisioning and the effective-runtime preflight remain the next integration step |
-| Process exit and PID reuse | simulated | D:563 (controlled subprocess tests exercise stale process data); not a live observation |
-| Resume in a new process | simulated | E:10 (two new jobs for the same logical id were both recognized, "labelled controlled resume rather than CLI resume"); real CLI resume unobserved, E:19 |
+| Process exit and PID reuse | simulated | D:563 (controlled subprocess tests exercise stale process data); tests T:318 (test_old_orphan_keeps_origin_new_ordinary_and_forged_environment_do_not) and T:362 (test_corrupt_or_stale_job_record_is_unknown_not_human); not a live observation |
+| Resume in a new process | simulated | E:10 (two new jobs for the same logical id were both recognized, "labelled controlled resume rather than CLI resume"); real CLI resume unobserved, E:19; test T:1399 (test_real_git_controlled_resume_same_logical_id_new_job_not_live_cli_resume) |
 | /clear and fork | unobserved | E:19; D:563 |
-| Release while a job is alive | simulated | E:10 (after explicit release the old jobs reported ordinary/released and the fixture refs advanced) |
+| Release while a job is alive | simulated | E:10 (after explicit release the old jobs reported ordinary/released and the fixture refs advanced); tests T:421 (test_release_live_job_and_invalid_bound_state) and T:1292 |
 
 Observed: 2 of 13 rows. Simulated: 6. Unobserved: 5. No row is claimed as passed beyond what the cited artifact shows.
 

Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B4 ac=scope at=.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/b-ctx-verdict.md:18 anchor="simulated (cite the test)" chk=n,n,n,y family=simulated-rows-cite-no-test fix=cite the covering tests in tests/hooks/test_launch_job_identity.py for the simulated rows first=A1 origin=new covers="simulated (cite the test)": only the background-Bash row names the test file and without a line; the other five simulated rows cite the evidence file or the design only.

Saved-probe re-check hit locations (may be empty): 18:| Background Bash to Git 
20:| Same-worktree human terminal 
22:| Detached or reparented job 
24:| Process exit and PID reuse 
25:| Resume in a new process 
27:| Release while a job is alive 


Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
