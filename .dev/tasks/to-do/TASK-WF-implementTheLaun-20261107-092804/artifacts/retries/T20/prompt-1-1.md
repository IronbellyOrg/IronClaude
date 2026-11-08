f36da6ae0ef9c03a05ab78e5dc0c307562e1dc13
Review one task for spec compliance.

Task brief: ## Task 20: Report a missing L2 layer as the warning W-L2-ABSENT without refusing the launch (IR-7, owner option b)

Depends on: Task 19

Design section 13 IR-7 says the claim should refuse a governed launch while the L2 pre-push layer is absent. Task 21 records that this plan builds no L2 artifact, so a refusal would switch off every governed claim (--pipeline worktree and full) until a later plan ships, and would make the OB-H2 observation impossible because nothing could launch. The default taken here is therefore a warning, not a refusal; the owner can change it (the question was asked of the coordinator and not answered before implementation began).

In src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py, when l2_status() from Task 19 returns "absent", add the warning W-L2-ABSENT to the launch result with the reason, and let the launch continue. Do not look for any owned-hook marker or contract marker: no L2 artifact exists to match, and a header alone is not ownership proof (design section 19.2). Do not touch any existing hook file. Add W-L2-ABSENT to REMEDY with the sentence that the L2 layer is not built yet and the limits are enforced by the L1 guard only. The refusal of IR-4 (guard missing or not effective) from Task 18 is unchanged.

Update tests/skills/test_issue_orca_worktree.py with: l2_status absent gives the warning and the launch proceeds (a launch call is recorded, a pending record exists, status stays launched); a pre-push file present gives "present-unverified" and no W-L2-ABSENT; a foreign pre-push file is byte-identical before and after the claim. Record in ./artifacts/ir7-consequence.md, in plain words, that IR-7 is implemented as a warning, that the design text says refuse, why (the launch feature would be off and unobservable), and what to change when the L2 plan ships (turn the warning into a refusal in the same function).

Acceptance criteria:
- uv run pytest tests/skills/test_issue_orca_worktree.py -v passes with the L2 cases.
- With L2 absent the fake orca records the agent launch call, a pending record exists, and the result carries W-L2-ABSENT; with a foreign pre-push file present the file is byte-identical afterwards.
- ./artifacts/ir7-consequence.md exists, states the choice and the one-line change that makes it a refusal, and cites design sections 13 and 19.2.

AC ids (source order):
T20.AC1: uv run pytest tests/skills/test_issue_orca_worktree.py -v passes with the L2 cases.
T20.AC2: With L2 absent the fake orca records the agent launch call, a pending record exists, and the result carries W-L2-ABSENT; with a foreign pre-push file present the file is byte-identical afterwards.
T20.AC3: ./artifacts/ir7-consequence.md exists, states the choice and the one-line change that makes it a refusal, and cites design sections 13 and 19.2.
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
Start sha: f36da6ae0ef9c03a05ab78e5dc0c307562e1dc13
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/ir7-consequence.md b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/ir7-consequence.md
new file mode 100644
index 00000000..c374b371
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/ir7-consequence.md
@@ -0,0 +1,64 @@
+# IR-7 consequence: a missing L2 layer is a warning, not a refusal
+
+## What was built
+
+IR-7 is implemented as a warning. When `l2_status()` in
+`src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` returns
+`absent` (the worktree has no executable file at git's `hooks/pre-push` path),
+`cmd_launch` adds the warning `W-L2-ABSENT` with its reason to the launch
+result and the launch goes ahead: the agent is started, the pending record is
+written and the status stays `launched`. The remedy line says the L2 layer is
+not built yet and the limits are enforced by the L1 guard only.
+
+The claim looks for no owned-hook marker and no contract marker, and it never
+creates, edits or adopts a hook file. A pre-push file that is already there
+gives `present-unverified` and no warning, and stays byte-identical.
+
+The IR-4 refusal of Task 18 (guard missing or not effective gives
+`W-ENFORCEMENT-ABSENT` and no launch) is unchanged.
+
+## What the design says
+
+Design section 13, IR-7: when the owned L2 installation is absent, the claim
+"reports W-L2-ABSENT and refuses that governed launch". Design section 19.2
+says the same: "do not launch a governed pipeline advertised as protected when
+accepted L2 is absent". So the design text says refuse, and this code does not.
+
+## Why a warning
+
+This plan builds no L2 artifact (Task 21 records that). With a refusal, `l2_status()`
+would return `absent` for every worktree, so every governed claim
+(`--pipeline worktree` and `--pipeline full`) would be refused. The launch
+feature would be switched off, and nothing could ever start, which also makes
+the OB-H2 observation impossible: it needs a real governed launch.
+
+Ownership cannot be checked either: no owned L2 hook exists to compare
+against, and design section 19.2 says "a header alone is not sufficient
+ownership proof". So `present-unverified` means only "some executable hook is
+there", never "protected".
+
+The owner was asked and had not answered when work began; the warning is the
+default taken (owner option b) and the owner can change it.
+
+## The one-line change that makes it a refusal
+
+When the L2 plan ships, in `cmd_launch` (the same function, before
+`publish_pending`, so a refusal writes no pending record and starts no agent),
+directly after the line
+
+```python
+l2_notes = [("W-L2-ABSENT", L2_ABSENT_WHY)] if l2 == "absent" else []
+```
+
+add the one line
+
+```python
+if l2_notes: return emit(launch_result("failed", l2_notes, enforcement_hook=hook))
+```
+
+That line is already written as a comment just above them in the code. That L2
+plan also has to replace `l2_status()`'s plain "is there an executable file"
+test with a check of the exact owned version and content (design section 19.2),
+reword `REMEDY["W-L2-ABSENT"]` and the claim.md and SKILL.md rows (they say the
+agent was started), and turn
+`test_ir7_l2_absent_warns_and_the_launch_proceeds` into a refusal test.
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t20-test.log b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t20-test.log
new file mode 100644
index 00000000..10d64a73
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t20-test.log
@@ -0,0 +1,5 @@
+........................................................................ [ 90%]
+........................................................................ [ 98%]
+..................                                                       [100%]
+
+============================= 929 passed in 28.27s =============================
diff --git a/src/superclaude/skills/sc-issue-protocol/SKILL.md b/src/superclaude/skills/sc-issue-protocol/SKILL.md
index 91a1268a..0ecdaf08 100644
--- a/src/superclaude/skills/sc-issue-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-issue-protocol/SKILL.md
@@ -89,7 +89,7 @@ Load `refs/claim.md` now. `<N>` is the issue number, `<D>` = `.dev/issues/<N>/`.
 6. **Wave 5, next steps.** Load `refs/chains.md`. Invoke `Skill sc-recommend` with the goal format of `refs/chains.md`; save its output verbatim to `<D>/recommend.md` from `templates/recommend-record.md`. Write `<D>/next-steps.md` from `templates/next-steps.md`, starting with the `/model` tier line and carrying the `Plan boundary: after step <K>` line. Unless `--pipeline none`, render `<D>/launch-prompt.md` with `orca_worktree.py prompt` (the script keeps the existing prompt only while a launch entry's worktree still exists).
 7. **Wave 6, post.** Post or edit (by marker) the accuracy-check comment and the claim comment (`templates/claim-comment.md`). Then continue with Wave 7 and Wave 8. A STOP in Waves 0 to 6 means no Orca call after the Wave 0 check. This skill never runs a step of `next-steps.md` (B2).
 8. **Wave 7, worktree.** `orca_worktree.py worktree --repo <R> --number <N> --base origin/<B> --source <D>` creates or reuses the worktree and copies `<D>` into it. Every failure is a warning: the claim `status` stays `success`.
-9. **Wave 8, launch.** Only when `--pipeline` is not `none` and Wave 7 `status` is `created` or `reused`: `orca_worktree.py launch --number <N> --source <D> --level <L> [--submit]` first checks that the launch-level guard would be effective (the IR-4 preflight; read only) and refuses the launch with `W-ENFORCEMENT-ABSENT` when it would not; otherwise it starts one agent in the worktree at the chosen level, behind the ccsession shim, and records the level for the enforcement hook. The agent, not this skill, runs the steps. Every failure, a refusal included, is a warning. Then print the final output of `refs/claim.md` (worktree line, tracking note, launch result with its release instruction and L1/L2 layer status lines, every warning with its remedy line), the return contract, and STOP.
+9. **Wave 8, launch.** Only when `--pipeline` is not `none` and Wave 7 `status` is `created` or `reused`: `orca_worktree.py launch --number <N> --source <D> --level <L> [--submit]` first checks that the launch-level guard would be effective (the IR-4 preflight; read only) and refuses the launch with `W-ENFORCEMENT-ABSENT` when it would not; otherwise it starts one agent in the worktree at the chosen level, behind the ccsession shim, and records the level for the enforcement hook, adding the warning `W-L2-ABSENT` when the worktree has no L2 pre-push layer (the launch still goes ahead). The agent, not this skill, runs the steps. Every failure, a refusal included, is a warning. Then print the final output of `refs/claim.md` (worktree line, tracking note, launch result with its release instruction and L1/L2 layer status lines, every warning with its remedy line), the return contract, and STOP.
 
 ## Create mode
 
@@ -133,7 +133,7 @@ launch_warning: <W- code or null>
 enforcement_hook: installed | missing | null
 ```
 
-`launch_status` is `not_requested` for `--pipeline none` and when `worktree_status` is `failed`. `worktree_match_key` is `null` for a newly created worktree. `enforcement_hook` reports the IR-4 preflight of the launch: `installed` means it passed (also when the launch then failed), `missing` means it failed and the launch was refused (`launch_status` `failed`, `launch_warning` `W-ENFORCEMENT-ABSENT`, no agent started), and `null` means no preflight ran (no agent requested, `already_launched`, or a launch that failed before the preflight). The claim `status` stays `success` through any worktree or launch warning.
+`launch_status` is `not_requested` for `--pipeline none` and when `worktree_status` is `failed`. `worktree_match_key` is `null` for a newly created worktree. `enforcement_hook` reports the IR-4 preflight of the launch: `installed` means it passed (also when the launch then failed), `missing` means it failed and the launch was refused (`launch_status` `failed`, `launch_warning` `W-ENFORCEMENT-ABSENT`, no agent started), and `null` means no preflight ran (no agent requested, `already_launched`, or a launch that failed before the preflight). `launch_warning` is the first launch code: a `launched` claim without an L2 pre-push layer carries `W-LAUNCH-NOT-CCSESSION` there when that also applies, else `W-L2-ABSENT`. The claim `status` stays `success` through any worktree or launch warning.
 
 On a STOP, also print the STOP code and its message.
 
@@ -147,7 +147,7 @@ On a STOP, also print the STOP code and its message.
 | `gh auth status` fails | STOP `E-GH-AUTH` |
 | `orca_worktree.py preflight` prints `ok: false` (Orca not installed, not running or not reachable) | STOP `E-ORCA-REQUIRED` with the script's `detail`, before any GitHub or ClickUp write |
 | Worktree step fails or needs attention (`W-ORCA-LIST-FAILED`, `W-ORIGIN-BASE-MISSING`, `W-ORIGIN-BASE-STALE`, `W-WORKTREE-CREATE-FAILED`, `W-WORKTREE-AMBIGUOUS`, `W-WORKTREE-STALE`, `W-WORKTREE-COPY-FAILED`) | Warning only: the claim `status` stays `success`; print the code with its remedy line from `refs/claim.md` |
-| Launch step fails or needs attention (`W-LAUNCH-FAILED`, `W-LAUNCH-NOT-CCSESSION`, `W-ENFORCEMENT-ABSENT`) | Warning only: the claim `status` stays `success`; print the code with its remedy line from `refs/claim.md`; no launch is attempted for a failed worktree or for `--pipeline none`. `W-ENFORCEMENT-ABSENT` means the launch was refused and no agent was started |
+| Launch step fails or needs attention (`W-LAUNCH-FAILED`, `W-LAUNCH-NOT-CCSESSION`, `W-ENFORCEMENT-ABSENT`, `W-L2-ABSENT`) | Warning only: the claim `status` stays `success`; print the code with its remedy line from `refs/claim.md`; no launch is attempted for a failed worktree or for `--pipeline none`. `W-ENFORCEMENT-ABSENT` means the launch was refused and no agent was started; `W-L2-ABSENT` means the agent was started with no L2 pre-push layer, so only the L1 guard enforces the limits |
 | Issue closed | STOP, message "Issue #N is closed; not claimed.", no writes |
 | Assigned to someone else | STOP, message names the assignee, no writes |
 | Number or URL is a pull request | STOP `E-NOT-AN-ISSUE` |
diff --git a/src/superclaude/skills/sc-issue-protocol/refs/claim.md b/src/superclaude/skills/sc-issue-protocol/refs/claim.md
index 2f6ddc78..d22f606c 100644
--- a/src/superclaude/skills/sc-issue-protocol/refs/claim.md
+++ b/src/superclaude/skills/sc-issue-protocol/refs/claim.md
@@ -123,6 +123,9 @@ Read the one JSON object it prints: `status` (`launched`, `already_launched` or
 | `W-LAUNCH-FAILED` | re-run the claim; the hand command is printed for reference (an agent started by hand is not governed by the hook). When the `detail` says the worktree's `launch-prompt.md` is not the one rendered for this claim, no agent was started and no hand command is printed: make that file match `<D>/launch-prompt.md` first, a re-run alone fails again |
 | `W-LAUNCH-NOT-CCSESSION` | this agent is NOT behind the ccsession shim, or could not be verified; close it. Orca's Claude command must be the ccsession-orca wrapper |
 | `W-ENFORCEMENT-ABSENT` | the launch was refused and no agent was started; fix each condition the `detail` names (most are fixed by running `superclaude install`; a stale installed guard or registration needs `superclaude install --force`), then claim the issue again |
+| `W-L2-ABSENT` | the L2 layer is not built yet and the limits are enforced by the L1 guard only; the agent was started |
+
+`W-L2-ABSENT` is added to a `launched` result whenever the L2 line says `absent`. The design (IR-7) asks for a refusal there; until an L2 layer is built the claim only warns, so the launch goes ahead. When `W-LAUNCH-NOT-CCSESSION` is also present it comes first: `warning` holds it and `detail` carries `also W-L2-ABSENT: ...`.
 
 ## Final output (replaces "print the path and STOP")
 
diff --git a/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py b/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py
index d4bf2b8f..a8f999bd 100644
--- a/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py
+++ b/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py
@@ -39,7 +39,9 @@ with ``--level worktree`` is a bad argument (exit 2).
 Claude Code agent in the worktree recorded in ``<D>/worktree.json``. It first
 runs the IR-4 preflight (jq, uv, Linux, the installed guard and its settings
 registrations; read only) and refuses the launch with ``W-ENFORCEMENT-ABSENT``
-when the guard would not be effective. It then publishes the launch record the enforcement hook reads
+when the guard would not be effective. A worktree without an executable
+pre-push hook only adds the warning ``W-L2-ABSENT`` (IR-7 is a warning until an
+L2 layer is built); the launch goes ahead. It then publishes the launch record the enforcement hook reads
 (``$HOME/.claude/state/launch-level/pending/<nonce>``, one word), then runs
 ``orca agent launch --surface terminal`` with a prompt that starts with
 ``[sc-launch:v1:<nonce>]``, checks the agent's screen for the ccsession shim, and
@@ -717,7 +719,17 @@ REMEDY = {
         "named above (most are fixed by running superclaude install), then "
         "claim the issue again"
     ),
+    "W-L2-ABSENT": (
+        "the L2 layer is not built yet and the limits are enforced by the L1 "
+        "guard only; the agent was started"
+    ),
 }
+# IR-7 (design section 13) says refuse; this plan builds no L2 layer, so the
+# claim warns instead and the launch goes ahead.
+L2_ABSENT_WHY = (
+    "the worktree has no executable pre-push hook at git's hook path, so no L2 "
+    "pre-push layer checks this session's pushes"
+)
 # IR-4: what the claim checks before a governed launch. It reads files and the
 # environment only and never edits any configuration.
 GUARD_COMMAND = "~/.claude/hooks/launch-level-guard.sh"
@@ -939,10 +951,11 @@ def l2_status(wt: str) -> str:
     )
 
 
-def session_report(wt: str) -> tuple[str, list[str]]:
+def session_report(wt: str, l2: str) -> tuple[str, list[str]]:
     """IR-6: how a person releases the launched session, and one line per layer.
 
-    Called only after the IR-4 preflight passed, so L1 is effective.
+    Called only after the IR-4 preflight passed, so L1 is effective. ``l2`` is
+    the l2_status() answer the launch already used, so both always agree.
     """
     store = home_dir().joinpath(*PENDING_PARTS[:-1])
     release = (
@@ -951,7 +964,6 @@ def session_report(wt: str) -> tuple[str, list[str]]:
         "(the session id is the one the session's 'Launch-level guard' block "
         "message shows)"
     )
-    l2 = l2_status(wt)
     l2_line = (
         "L2 pre-push: absent (no executable pre-push hook in this worktree; the "
         "limits are enforced by the L1 guard only)"
@@ -1198,6 +1210,12 @@ def cmd_launch(args: argparse.Namespace) -> int:
         )
     hook = "installed"
     notes: list[tuple[str, str]] = []
+    # IR-7 as a warning, before publish_pending: reads the hook path only, looks
+    # for no ownership marker (design section 19.2) and never touches the hook.
+    # To make it the design's refusal, add after the l2_notes line:
+    # if l2_notes: return emit(launch_result("failed", l2_notes, enforcement_hook=hook))
+    l2 = l2_status(wt)
+    l2_notes = [("W-L2-ABSENT", L2_ABSENT_WHY)] if l2 == "absent" else []
     word = "full-submit" if args.submit else args.level
     try:
         nonce, pending = publish_pending(word)
@@ -1255,10 +1273,10 @@ def cmd_launch(args: argparse.Namespace) -> int:
             f"({'; '.join(problems)}); do not re-run the claim, add the launch entry "
             f"to {source / RECORD_NAME} by hand"
         )
-    release, layers = session_report(wt)
+    release, layers = session_report(wt, l2)
     result = launch_result(
         "launched",
-        notes,
+        notes + l2_notes,  # the ccsession warning, when any, stays first
         terminal=handle,
         launched_at=at,
         enforcement_hook=hook,
diff --git a/tests/skills/test_issue_orca_worktree.py b/tests/skills/test_issue_orca_worktree.py
index abbd4578..0160ff47 100644
--- a/tests/skills/test_issue_orca_worktree.py
+++ b/tests/skills/test_issue_orca_worktree.py
@@ -1241,7 +1241,8 @@ def test_la4_launch_record_update_failure_never_says_to_rerun_the_claim(
         data = run_launch(fake_orca, git_repo, issue_dir)
     finally:
         issue_dir.chmod(0o755)
-    assert data["status"] == "launched" and data["warning"] is None
+    # IR-7: the scene's worktree has no pre-push hook, so W-L2-ABSENT is the warning.
+    assert data["status"] == "launched" and data["warning"] == "W-L2-ABSENT"
     assert data["launched_at"] and data["terminal"] == "term_abc"
     assert "the agent is running" in data["detail"]
     assert "do not re-run the claim" in data["detail"]
@@ -1279,7 +1280,7 @@ def test_la5_launch_shim_check_passes_on_either_text(
     launch_scene(fake_orca, git_repo, issue_dir)
     fake_orca.respond("terminal-read", {"stdout": screen})
     data = run_launch(fake_orca, git_repo, issue_dir)
-    assert data["status"] == "launched" and data["warning"] is None
+    assert data["status"] == "launched" and data["warning"] == "W-L2-ABSENT"
     assert orca_calls(fake_orca, "terminal", "read") == [
         ["terminal", "read", "--terminal", "term_abc", "--screen", "--json"]
     ]
@@ -1291,7 +1292,7 @@ def test_la5_launch_shim_check_retries_up_to_five_times(
     launch_scene(fake_orca, git_repo, issue_dir)
     plain = {"stdout": SCREEN_PLAIN}
     fake_orca.respond("terminal-read", plain, plain, {"stdout": SCREEN_OK})
-    assert run_launch(fake_orca, git_repo, issue_dir)["warning"] is None
+    assert run_launch(fake_orca, git_repo, issue_dir)["warning"] == "W-L2-ABSENT"
     assert len(orca_calls(fake_orca, "terminal", "read")) == 3
 
 
@@ -1312,6 +1313,7 @@ def test_la5_launch_shim_check_failure_keeps_the_launch_and_warns(
     data = run_launch(fake_orca, git_repo, issue_dir)
     assert data["status"] == "launched"
     assert data["warning"] == "W-LAUNCH-NOT-CCSESSION" and "close it" in data["detail"]
+    assert "; also W-L2-ABSENT: " in data["detail"]  # the ccsession warning stays first
     assert len(orca_calls(fake_orca, "terminal", "read")) == reads
 
 
@@ -1370,7 +1372,7 @@ def test_la6_launch_without_an_executable_hook_is_refused(
     [{}, {"CLAUDE_CONFIG_DIR": "same"}],
     ids=["default", "config-dir-same"],
 )
-def test_la6_launch_with_the_hook_installed_has_no_warning(
+def test_la6_launch_with_the_hook_installed_has_only_the_l2_warning(
     fake_orca: FakeOrca, git_repo: Path, issue_dir: Path, env: dict
 ) -> None:
     launch_scene(fake_orca, git_repo, issue_dir)
@@ -1379,7 +1381,8 @@ def test_la6_launch_with_the_hook_installed_has_no_warning(
     before = user_settings(fake_orca).read_bytes()
     data = run_launch(fake_orca, git_repo, issue_dir, **env)
     assert data["status"] == "launched"
-    assert data["enforcement_hook"] == "installed" and data["warning"] is None
+    assert data["enforcement_hook"] == "installed"
+    assert data["warning"] == "W-L2-ABSENT"  # the scene has no pre-push hook
     assert len(launch_calls(fake_orca)) == 1
     assert user_settings(fake_orca).read_bytes() == before
 
@@ -1473,10 +1476,37 @@ def test_ir6_l2_status_follows_the_git_hook_path(
     data = run_launch(fake_orca, git_repo, issue_dir)
     assert data["status"] == "launched"
     assert data["layers"][1].startswith(f"L2 pre-push: {expected} ")
+    # IR-7: W-L2-ABSENT exactly when the L2 line says absent.
+    assert (data["warning"] == "W-L2-ABSENT") is (expected == "absent")
+    assert ("L2 layer is not built yet" in data["detail"]) is (expected == "absent")
     if hook:  # never modified, never adopted
         assert (hook.read_bytes(), hook.stat().st_mode) == before
 
 
+# --- IR-7: a missing L2 layer is a warning, not a refusal ---------------------
+
+
+def test_ir7_l2_absent_warns_and_the_launch_proceeds(
+    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
+) -> None:
+    launch_scene(fake_orca, git_repo, issue_dir)
+    hooks = git_repo / ".git/hooks"
+    before = {p.name: p.read_bytes() for p in hooks.iterdir()}
+    data = run_launch(fake_orca, git_repo, issue_dir)
+    assert data["status"] == "launched" and data["warning"] == "W-L2-ABSENT"
+    assert data["enforcement_hook"] == "installed"
+    assert "no executable pre-push hook" in data["detail"]
+    assert "the L2 layer is not built yet" in data["detail"]
+    assert "enforced by the L1 guard only" in data["detail"]
+    assert data["layers"][1].startswith("L2 pre-push: absent ")
+    (argv,) = launch_calls(fake_orca)
+    nonce = PROMPT_RE.match(argv[9]).group(1)
+    assert [p.name for p in pending_dir(fake_orca).iterdir()] == [nonce]
+    assert "launch" in json.loads((issue_dir / "worktree.json").read_text())
+    # No hook file is created, adopted or changed.
+    assert {p.name: p.read_bytes() for p in hooks.iterdir()} == before
+
+
 # --- IR-4 preflight: one refusal per failing condition ------------------------
 
 
diff --git a/tests/skills/test_issue_protocol.py b/tests/skills/test_issue_protocol.py
index 42b3fcc5..678e7f4e 100644
--- a/tests/skills/test_issue_protocol.py
+++ b/tests/skills/test_issue_protocol.py
@@ -464,7 +464,12 @@ def test_st9_final_output_lists_the_launch_results_and_every_launch_code():
         "never merges",
     ):
         assert text in final, text
-    for code in ("W-LAUNCH-FAILED", "W-LAUNCH-NOT-CCSESSION", "W-ENFORCEMENT-ABSENT"):
+    for code in (
+        "W-LAUNCH-FAILED",
+        "W-LAUNCH-NOT-CCSESSION",
+        "W-ENFORCEMENT-ABSENT",
+        "W-L2-ABSENT",
+    ):
         assert code in claim and code in _text(SKILL), code
 
 

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

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
