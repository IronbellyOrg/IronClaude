2997c7f4abe7ad2cea3b1bb2100aae36841b5a67
Review one task for spec compliance.

Task brief: ## Task 19: State release instructions and layer status in the claim output, and pin re-claim behaviour (IR-5, IR-6)

Depends on: Task 18

In src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py add to the launched-claim result and its printed text the IR-6 information of design section 13: how a person releases the session (in their own terminal run rm on sessions/<session id> and sessions/<session id>.ok under ~/.claude/state/launch-level/, with the session id taken from the "Launch-level guard" block message), and the status of each layer (L1 guard: effective, from the Task 18 preflight result; L2 pre-push: from a new function l2_status() that returns "absent" when the git path hooks/pre-push of the worktree is not an executable file and "present-unverified" otherwise, so the printed line always agrees with the preflight and never claims ownership of a hook it did not build). Add test cases in tests/skills/test_issue_orca_worktree.py that assert the result fields and printed text, and extend the existing re-claim test la2 (do not add a duplicate) to pin IR-5: a claim whose worktree record already has a launch entry launches nothing and writes no new pending record, and after the launch entry is removed from both the record and the git-dir mirror the next launch writes a new pending record with a different nonce (never resuming an earlier session).

Update src/superclaude/skills/sc-issue-protocol/refs/claim.md (Wave 8 section) to describe the release instructions and the layer status lines.

Acceptance criteria:
- A launched claim in the fake-orca test prints the release instruction containing the store path and both file names, and a layer line for L1 and for L2.
- Two launches in the same test home with the launch entry removed in between create two pending records with different names.
- uv run pytest tests/skills/test_issue_orca_worktree.py tests/skills/test_issue_protocol.py -v passes.

AC ids (source order):
T19.AC1: A launched claim in the fake-orca test prints the release instruction containing the store path and both file names, and a layer line for L1 and for L2.
T19.AC2: Two launches in the same test home with the launch entry removed in between create two pending records with different names.
T19.AC3: uv run pytest tests/skills/test_issue_orca_worktree.py tests/skills/test_issue_protocol.py -v passes.
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
Start sha: 2997c7f4abe7ad2cea3b1bb2100aae36841b5a67
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t19-test.log b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t19-test.log
new file mode 100644
index 00000000..85c6c9ed
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t19-test.log
@@ -0,0 +1,5 @@
+........................................................................ [ 90%]
+........................................................................ [ 98%]
+..................                                                       [100%]
+
+============================= 928 passed in 27.01s =============================
diff --git a/src/superclaude/skills/sc-issue-protocol/SKILL.md b/src/superclaude/skills/sc-issue-protocol/SKILL.md
index 635a7944..91a1268a 100644
--- a/src/superclaude/skills/sc-issue-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-issue-protocol/SKILL.md
@@ -89,7 +89,7 @@ Load `refs/claim.md` now. `<N>` is the issue number, `<D>` = `.dev/issues/<N>/`.
 6. **Wave 5, next steps.** Load `refs/chains.md`. Invoke `Skill sc-recommend` with the goal format of `refs/chains.md`; save its output verbatim to `<D>/recommend.md` from `templates/recommend-record.md`. Write `<D>/next-steps.md` from `templates/next-steps.md`, starting with the `/model` tier line and carrying the `Plan boundary: after step <K>` line. Unless `--pipeline none`, render `<D>/launch-prompt.md` with `orca_worktree.py prompt` (the script keeps the existing prompt only while a launch entry's worktree still exists).
 7. **Wave 6, post.** Post or edit (by marker) the accuracy-check comment and the claim comment (`templates/claim-comment.md`). Then continue with Wave 7 and Wave 8. A STOP in Waves 0 to 6 means no Orca call after the Wave 0 check. This skill never runs a step of `next-steps.md` (B2).
 8. **Wave 7, worktree.** `orca_worktree.py worktree --repo <R> --number <N> --base origin/<B> --source <D>` creates or reuses the worktree and copies `<D>` into it. Every failure is a warning: the claim `status` stays `success`.
-9. **Wave 8, launch.** Only when `--pipeline` is not `none` and Wave 7 `status` is `created` or `reused`: `orca_worktree.py launch --number <N> --source <D> --level <L> [--submit]` first checks that the launch-level guard would be effective (the IR-4 preflight; read only) and refuses the launch with `W-ENFORCEMENT-ABSENT` when it would not; otherwise it starts one agent in the worktree at the chosen level, behind the ccsession shim, and records the level for the enforcement hook. The agent, not this skill, runs the steps. Every failure, a refusal included, is a warning. Then print the final output of `refs/claim.md` (worktree line, tracking note, launch result, every warning with its remedy line), the return contract, and STOP.
+9. **Wave 8, launch.** Only when `--pipeline` is not `none` and Wave 7 `status` is `created` or `reused`: `orca_worktree.py launch --number <N> --source <D> --level <L> [--submit]` first checks that the launch-level guard would be effective (the IR-4 preflight; read only) and refuses the launch with `W-ENFORCEMENT-ABSENT` when it would not; otherwise it starts one agent in the worktree at the chosen level, behind the ccsession shim, and records the level for the enforcement hook. The agent, not this skill, runs the steps. Every failure, a refusal included, is a warning. Then print the final output of `refs/claim.md` (worktree line, tracking note, launch result with its release instruction and L1/L2 layer status lines, every warning with its remedy line), the return contract, and STOP.
 
 ## Create mode
 
diff --git a/src/superclaude/skills/sc-issue-protocol/refs/claim.md b/src/superclaude/skills/sc-issue-protocol/refs/claim.md
index 41cb3d94..2f6ddc78 100644
--- a/src/superclaude/skills/sc-issue-protocol/refs/claim.md
+++ b/src/superclaude/skills/sc-issue-protocol/refs/claim.md
@@ -116,7 +116,7 @@ Runs only when `--pipeline` is not `none` and the Wave 7 `status` is `created` o
 
 `uv run --no-project python "<skill base>/scripts/orca_worktree.py" launch --number <N> --source <D> --level <L> [--submit]`
 
-Read the one JSON object it prints: `status` (`launched`, `already_launched` or `failed`), `warning`, `detail`, `terminal`, `launched_at`, `enforcement_hook` and `hand_command`. Before anything else the script runs the IR-4 preflight, which reads files and the environment only and never edits configuration: `jq` and `uv` on `PATH`, a Linux host, `~/.claude/hooks/launch-level-guard.sh` installed, executable and at version 1, the guard registered on `UserPromptSubmit` and on `PreToolUse` for every governed tool in `$HOME/.claude/settings.json`, `launch-job-identity.sh` registered on Bash `PreToolUse`, no `disableAllHooks` in the user or worktree project settings, and `CLAUDE_CONFIG_DIR` unset or equal to `$HOME/.claude`. When any fails it refuses the launch: `status` `failed`, `warning` `W-ENFORCEMENT-ABSENT`, `enforcement_hook` `missing`, a `detail` naming each failed condition, no agent and no launch record. It verifies the claim process only, not the environment the agent will run in. When all pass (`enforcement_hook` `installed`), the script starts one agent behind the ccsession shim in the worktree and records the level where the enforcement hook of issue 394 can read it. A `launch` entry in `<D>/worktree.json` makes it return `already_launched` without calling Orca. Every failure is a warning, never a STOP: the claim `status` stays `success`. Remedy lines of the launch codes:
+Read the one JSON object it prints: `status` (`launched`, `already_launched` or `failed`), `warning`, `detail`, `terminal`, `launched_at`, `enforcement_hook`, `hand_command`, `release` and `layers`. `release` and `layers` are set only for `launched` (null otherwise): `release` is the one-line release instruction (a person runs `rm` in their own terminal on `sessions/<session id>` and `sessions/<session id>.ok` under the store `~/.claude/state/launch-level/` of the claim's HOME; the session id is the one the session's 'Launch-level guard' block message shows), and `layers` is two status lines, `L1 guard: effective` (the IR-4 preflight passed) and `L2 pre-push: absent` or `L2 pre-push: present-unverified`. The L2 line comes from `git rev-parse --git-path hooks/pre-push` in the worktree (so `core.hooksPath` and linked worktrees are honoured): `absent` when that path is not an executable file, `present-unverified` otherwise. The script never claims, inspects the content of, or edits that hook. Before anything else the script runs the IR-4 preflight, which reads files and the environment only and never edits configuration: `jq` and `uv` on `PATH`, a Linux host, `~/.claude/hooks/launch-level-guard.sh` installed, executable and at version 1, the guard registered on `UserPromptSubmit` and on `PreToolUse` for every governed tool in `$HOME/.claude/settings.json`, `launch-job-identity.sh` registered on Bash `PreToolUse`, no `disableAllHooks` in the user or worktree project settings, and `CLAUDE_CONFIG_DIR` unset or equal to `$HOME/.claude`. When any fails it refuses the launch: `status` `failed`, `warning` `W-ENFORCEMENT-ABSENT`, `enforcement_hook` `missing`, a `detail` naming each failed condition, no agent and no launch record. It verifies the claim process only, not the environment the agent will run in. When all pass (`enforcement_hook` `installed`), the script starts one agent behind the ccsession shim in the worktree and records the level where the enforcement hook of issue 394 can read it. A `launch` entry in `<D>/worktree.json` makes it return `already_launched` without calling Orca. Every failure is a warning, never a STOP: the claim `status` stays `success`. Remedy lines of the launch codes:
 
 | Code | Remedy line |
 |---|---|
@@ -131,7 +131,7 @@ Print, in this order:
 1. The `next-steps.md` path, then `Worktree: <path> (<status>)`, adding `, matched by <match_key>` when `match_key` is not null (a newly created worktree has none). For `match_key` `basename` or `branch` add "reused a worktree not created by /sc:issue". For `record` after `W-ORCA-LIST-FAILED` add "unverified: Orca could not be listed".
 2. "`.dev/issues/<N>/` in the worktree is untracked: do not stage it" only when `tracked_known` is true and `tracked_files` is empty. When `tracked_known` is false, print nothing about tracking. Add "run `make sync-dev` there first" when `<wt>/.claude/` is absent and a step of `next-steps.md` needs a primitive that is not synced into the worktree.
 3. The launch result:
-   - `launched`: "Agent launched in <wt> (level <L>[, submit]). It stops at the plan boundary and waits; reply `approved` in its tab to let it continue." For `full`: "It runs every step and stops after implementation." For `full` with `--submit`: "It then commits, pushes <branch> and opens the PR through /sc:pr-submit; it never merges."
+   - `launched`: "Agent launched in <wt> (level <L>[, submit]). It stops at the plan boundary and waits; reply `approved` in its tab to let it continue." For `full`: "It runs every step and stops after implementation." For `full` with `--submit`: "It then commits, pushes <branch> and opens the PR through /sc:pr-submit; it never merges." Then print the JSON's `release` line and the two `layers` lines (`L1 guard` first, then `L2 pre-push`) verbatim.
    - `already_launched`: "agent already launched at <launched_at>" plus the script's `detail`, which names the two files that hold the `launch` entry (`<D>/worktree.json` and a file in the worktree's git directory); the user removes the entry from both to launch again.
    - `--pipeline none`: "No agent launched. Open <wt> and run .dev/issues/<N>/next-steps.md there."
 4. Every warning, the worktree one first: the code, its `detail`, and its remedy line from the two tables above. For `W-LAUNCH-FAILED`, also print the launch JSON's `hand_command` when it is not null (the remedy line promises it), and tell the user that an agent started by hand is not governed by the enforcement hook.
diff --git a/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py b/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py
index 562ef754..d4bf2b8f 100644
--- a/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py
+++ b/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py
@@ -44,8 +44,10 @@ when the guard would not be effective. It then publishes the launch record the e
 ``orca agent launch --surface terminal`` with a prompt that starts with
 ``[sc-launch:v1:<nonce>]``, checks the agent's screen for the ccsession shim, and
 writes a ``launch`` entry into ``worktree.json``. It prints ``{status, warning,
-detail, terminal, launched_at, enforcement_hook, hand_command}`` with ``status``
-``launched``, ``failed`` or ``already_launched``.
+detail, terminal, launched_at, enforcement_hook, hand_command, release,
+layers}`` with ``status`` ``launched``, ``failed`` or ``already_launched``;
+``release`` (how a person releases the session) and ``layers`` (one status line
+for L1 and one for L2) are set only for ``launched``, else null.
 """
 
 from __future__ import annotations
@@ -917,6 +919,49 @@ def enforcement_preflight(wt: str) -> list[str]:
     return failures
 
 
+def l2_status(wt: str) -> str:
+    """IR-6: the L2 pre-push layer of the worktree, read only.
+
+    ``absent`` when git's ``hooks/pre-push`` path for ``wt`` (``core.hooksPath``
+    and the common git directory of a linked worktree honoured) is not an
+    executable file, else ``present-unverified``: this file did not build that
+    hook, so it never claims to know what the hook enforces.
+    """
+    res = run(["git", "-C", wt, "rev-parse", "--git-path", "hooks/pre-push"])
+    out = res.out.strip()
+    if not res.ok or not out:
+        return "absent"
+    hook = Path(wt) / out  # a relative answer is relative to wt
+    return (
+        "present-unverified"
+        if hook.is_file() and os.access(hook, os.X_OK)
+        else "absent"
+    )
+
+
+def session_report(wt: str) -> tuple[str, list[str]]:
+    """IR-6: how a person releases the launched session, and one line per layer.
+
+    Called only after the IR-4 preflight passed, so L1 is effective.
+    """
+    store = home_dir().joinpath(*PENDING_PARTS[:-1])
+    release = (
+        "to release this session, a person runs in their own terminal: "
+        f'rm "{store}/sessions/<session id>" "{store}/sessions/<session id>.ok" '
+        "(the session id is the one the session's 'Launch-level guard' block "
+        "message shows)"
+    )
+    l2 = l2_status(wt)
+    l2_line = (
+        "L2 pre-push: absent (no executable pre-push hook in this worktree; the "
+        "limits are enforced by the L1 guard only)"
+        if l2 == "absent"
+        else "L2 pre-push: present-unverified (a pre-push hook exists; the claim "
+        "did not build it and does not check what it enforces)"
+    )
+    return release, ["L1 guard: effective (the IR-4 preflight passed)", l2_line]
+
+
 def publish_pending(word: str) -> tuple[str, Path]:
     """Write ``pending/<nonce>`` (mode 0600, directories 0700); return nonce, path."""
     base = home_dir()
@@ -1062,6 +1107,8 @@ def launch_result(status: str, notes: list[tuple[str, str]], **fields: object) -
         "launched_at": None,
         "enforcement_hook": None,
         "hand_command": None,
+        "release": None,
+        "layers": None,
     }
     base.update(fields)
     return base
@@ -1208,12 +1255,15 @@ def cmd_launch(args: argparse.Namespace) -> int:
             f"({'; '.join(problems)}); do not re-run the claim, add the launch entry "
             f"to {source / RECORD_NAME} by hand"
         )
+    release, layers = session_report(wt)
     result = launch_result(
         "launched",
         notes,
         terminal=handle,
         launched_at=at,
         enforcement_hook=hook,
+        release=release,
+        layers=layers,
     )
     if unrecorded:
         result["detail"] = "; ".join(filter(None, [result["detail"], unrecorded]))
diff --git a/tests/skills/test_issue_orca_worktree.py b/tests/skills/test_issue_orca_worktree.py
index cdeffc78..abbd4578 100644
--- a/tests/skills/test_issue_orca_worktree.py
+++ b/tests/skills/test_issue_orca_worktree.py
@@ -1143,6 +1143,13 @@ def test_la2_launch_nonce_is_fresh_for_every_launch(
 ) -> None:
     wt = launch_scene(fake_orca, git_repo, issue_dir)
     first = run_launch(fake_orca, git_repo, issue_dir)
+    (first_nonce,) = [p.name for p in pending_dir(fake_orca).iterdir()]
+    # IR-5: with the launch entry in place a re-claim launches nothing and
+    # writes no new pending record.
+    again = run_launch(fake_orca, git_repo, issue_dir)
+    assert again["status"] == "already_launched"
+    assert len(launch_calls(fake_orca)) == 1
+    assert [p.name for p in pending_dir(fake_orca).iterdir()] == [first_nonce]
     record = json.loads((issue_dir / "worktree.json").read_text())
     del record["launch"]
     (issue_dir / "worktree.json").write_text(json.dumps(record))
@@ -1157,10 +1164,16 @@ def test_la2_launch_nonce_is_fresh_for_every_launch(
         and str(issue_dir / "worktree.json") in blocked["detail"]
     )
     assert first["status"] == "launched"
+    assert len(list(pending_dir(fake_orca).iterdir())) == 1
     mirror.unlink()
-    run_launch(fake_orca, git_repo, issue_dir)
-    nonces = {PROMPT_RE.match(c[9]).group(1) for c in launch_calls(fake_orca)}
-    assert len(nonces) == 2 and len(list(pending_dir(fake_orca).iterdir())) == 2
+    # Removed from both the record and the git-dir mirror: a new launch with a
+    # new nonce, never a resumed earlier session.
+    assert run_launch(fake_orca, git_repo, issue_dir)["status"] == "launched"
+    calls = launch_calls(fake_orca)
+    nonces = [PROMPT_RE.match(c[9]).group(1) for c in calls]
+    assert len(calls) == 2 and nonces[0] == first_nonce != nonces[1]
+    assert sorted(p.name for p in pending_dir(fake_orca).iterdir()) == sorted(nonces)
+    assert not any("--resume" in arg or "--continue" in arg for c in calls for arg in c)
 
 
 @pytest.mark.parametrize(
@@ -1381,6 +1394,89 @@ def test_la6_launch_refusal_comes_before_any_shim_check(
     assert "W-LAUNCH-NOT-CCSESSION" not in data["detail"]
 
 
+# --- IR-6: release instructions and layer status ------------------------------
+
+
+def test_ir6_launched_result_states_the_release_and_both_layers(
+    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
+) -> None:
+    launch_scene(fake_orca, git_repo, issue_dir)
+    data = run_launch(fake_orca, git_repo, issue_dir)
+    assert data["status"] == "launched"
+    store = fake_orca.home / ".claude/state/launch-level"
+    release = data["release"]
+    assert f'rm "{store}/sessions/<session id>" "{store}/sessions/<session id>.ok"' in (
+        release
+    )
+    assert "own terminal" in release and "'Launch-level guard' block" in release
+    l1, l2 = data["layers"]
+    assert l1.startswith("L1 guard: effective")
+    assert l2.startswith("L2 pre-push: absent")  # git init makes only *.sample hooks
+    # Not launched: neither field is set.
+    again = run_launch(fake_orca, git_repo, issue_dir)
+    assert again["status"] == "already_launched"
+    assert again["release"] is None and again["layers"] is None
+    wave8, final = (
+        (SCRIPT.parents[1] / "refs/claim.md").read_text().split("## Final output")
+    )
+    assert "sessions/<session id>.ok" in wave8 and "present-unverified" in wave8
+    for text in ("`release`", "`layers`", "L1 guard", "L2 pre-push"):
+        assert text in final, text
+
+
+def test_ir6_refused_launch_has_no_release_or_layers(
+    fake_orca: FakeOrca, git_repo: Path, issue_dir: Path
+) -> None:
+    launch_scene(fake_orca, git_repo, issue_dir, hook=None)
+    data = run_launch(fake_orca, git_repo, issue_dir)
+    assert_refused(fake_orca, data)
+    assert data["release"] is None and data["layers"] is None
+
+
+@pytest.mark.parametrize(
+    ("case", "expected"),
+    [
+        ("no-file", "absent"),
+        ("not-executable", "absent"),
+        ("foreign-executable", "present-unverified"),
+        ("hooks-path", "present-unverified"),
+        ("hooks-path-elsewhere", "absent"),
+    ],
+)
+def test_ir6_l2_status_follows_the_git_hook_path(
+    fake_orca: FakeOrca,
+    git_repo: Path,
+    issue_dir: Path,
+    tmp_path: Path,
+    case: str,
+    expected: str,
+) -> None:
+    # The scene's worktree is a linked worktree: git keeps its hooks in the
+    # main checkout's common directory, or in core.hooksPath when set.
+    launch_scene(fake_orca, git_repo, issue_dir)
+    default = git_repo / ".git/hooks/pre-push"
+    elsewhere = tmp_path / "hooks-elsewhere"
+    elsewhere.mkdir()
+    hook = {
+        "no-file": None,
+        "not-executable": default,
+        "foreign-executable": default,
+        "hooks-path": elsewhere / "pre-push",
+        "hooks-path-elsewhere": default,
+    }[case]
+    if case.startswith("hooks-path"):
+        git(git_repo, "config", "core.hooksPath", str(elsewhere))
+    if hook:
+        hook.write_text("#!/bin/sh\n# someone else's hook\nexit 0\n")
+        hook.chmod(0o644 if case == "not-executable" else 0o755)
+        before = (hook.read_bytes(), hook.stat().st_mode)
+    data = run_launch(fake_orca, git_repo, issue_dir)
+    assert data["status"] == "launched"
+    assert data["layers"][1].startswith(f"L2 pre-push: {expected} ")
+    if hook:  # never modified, never adopted
+        assert (hook.read_bytes(), hook.stat().st_mode) == before
+
+
 # --- IR-4 preflight: one refusal per failing condition ------------------------
 
 

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
