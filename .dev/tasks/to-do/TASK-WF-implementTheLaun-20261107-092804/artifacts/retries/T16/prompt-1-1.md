51c3315f35594de18f45a4f5401dd3d97a99eaa0
Review one task for spec compliance.

Task brief: ## Task 16: Port the push, git, alias, merge and benign corpus

Depends on: Task 11

Add to tests/hooks/test_launch_level_guard.py the corpus categories of design section 11 for git behaviour, taking case inputs from MR sections 8.2, 8.3 and 8.4 as historical baselines and writing expected results by hand from design section 4 (DD-2): push routes (T-ATK-1, 13, 25, 29, 50), aliases and variable subcommands (T-ATK-10, 35, 42), merges (T-ATK-48, 49, 51), the benign cases T-OK-1 to T-OK-36 that involve git and the pinned over-blocks T-OVR-1 to T-OVR-6, the amendment attacks N-ATK that concern git, the boundary cases of design section 10 that concern git (git stash push, git config --get remote.origin.url, a heredoc line all:\, git add of install_hooks.py), and the panel regression cases F1 to F8 only where their definitions can be found in the tree; the panel review file named in the design (.dev/brainstorms/20261105-170229-launch-level-hook/spec-panel-20261106/review.md) is absent, so record that in ./artifacts/f1-f8-missing.md and add regression cases only for the boundary rules the design states explicitly (typed top-level dispatch, identity loss, no-replacement binding, nonempty PR repo operand, protected destination); do not invent F-numbered cases. Add T-COR-2: replay the rows MR marks as real on a temporary bare remote and a temporary clone created by the test, asserting the remote refs before and after, so a push that should be blocked never reaches the remote and a permitted feature-branch push does. Where a result differs from the MR expectation, add a comment naming the design override (top-level typed dispatch, identity-loss allowance, no 64-id early allow, no-replacement publication, nonempty PR repo operand).

Acceptance criteria:
- uv run pytest tests/hooks/test_launch_level_guard.py -v passes with every listed corpus case present as a named test or parametrized id.
- The T-COR-2 test uses only a pytest temporary directory for the remote and the clone and asserts the remote ref list unchanged after each blocked case.
- The test module contains no expected value copied from MR without a matching row in design section 4 or an explicit override comment.
- Accepted leaks (T-ATK-26 to 28, N-ATK-7, 31 and 36) are pinned as allow with a comment citing the residual risk id (R1, R3 or R11) from design section 16.

AC ids (source order):
T16.AC1: uv run pytest tests/hooks/test_launch_level_guard.py -v passes with every listed corpus case present as a named test or parametrized id.
T16.AC2: The T-COR-2 test uses only a pytest temporary directory for the remote and the clone and asserts the remote ref list unchanged after each blocked case.
T16.AC3: The test module contains no expected value copied from MR without a matching row in design section 4 or an explicit override comment.
T16.AC4: Accepted leaks (T-ATK-26 to 28, N-ATK-7, 31 and 36) are pinned as allow with a comment citing the residual risk id (R1, R3 or R11) from design section 16.
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
Start sha: 51c3315f35594de18f45a4f5401dd3d97a99eaa0
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/f1-f8-missing.md b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/f1-f8-missing.md
new file mode 100644
index 00000000..58c6bd3e
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/f1-f8-missing.md
@@ -0,0 +1,20 @@
+# Panel findings F1 to F8: source file missing (Task 16)
+
+Checked 2026-11-07 in the worktree `issue-394-launch-level-hook`.
+
+- `.dev/brainstorms/20261105-170229-launch-level-hook/spec-panel-20261106/review.md` is absent.
+- `ls .dev/brainstorms/20261105-170229-launch-level-hook/spec-panel-20261106` printed:
+  `ls: cannot access '.dev/brainstorms/20261105-170229-launch-level-hook/spec-panel-20261106': No such file or directory`
+- The parent directory `.dev/brainstorms/20261105-170229-launch-level-hook/` holds only
+  `adversarial/`, `enrichment/`, `merged-requirements.md`, `return-contract.yaml` and `seed-brief.md`.
+- `find .dev -type d -name "spec-panel*"` finds no spec-panel directory for this hook (only
+  `.dev/troubleshoot-meta/20260610T141100Z/spec-panel`, its copy under `.dev/research/...`, and
+  `.dev/brainstorms/20260618-per-phase-turn-budget/spec-panel`, all unrelated).
+- `grep -rln "spec-panel-20261106" --include=*.md .` (excluding `.claude/`) finds the name only as a
+  reference: in `docs/designs/sc-issue-launch-level-hook.md`, the plan file of this package, its
+  `artifacts/b-ctx-verdict.md` and T1 retry prompts, `.dev/issues/394/` notes, the
+  `TASK-WF-implementDocsDes-20261106-210206` package and `.dev/reflect/pre-implementTheLaun-20261107093251/`.
+  None of these is the review itself.
+
+Consequence for Task 16: no F-numbered case was written. The corpus tests cite MR sections 8.3 and
+8.4 and design sections 4, 5, 10 and 16 only.
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t16-test.log b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t16-test.log
new file mode 100644
index 00000000..a259a900
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t16-test.log
@@ -0,0 +1,64 @@
+$ uv run pytest tests/hooks/test_launch_level_guard.py -k "ATK or OK or OVR or NATK or COR" -q
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-394-launch-level-hook
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, anyio-4.16.0
+collected 3561 items
+
+tests/hooks/test_launch_level_guard.py ................................. [  0%]
+........................................................................ [  2%]
+........................................................................ [  4%]
+........................................................................ [  6%]
+........................................................................ [  9%]
+........................................................................ [ 11%]
+........................................................................ [ 13%]
+........................................................................ [ 15%]
+........................................................................ [ 17%]
+........................................................................ [ 19%]
+........................................................................ [ 21%]
+........................................................................ [ 23%]
+........................................................................ [ 25%]
+........................................................................ [ 27%]
+........................................................................ [ 29%]
+........................................................................ [ 31%]
+........................................................................ [ 33%]
+........................................................................ [ 35%]
+........................................................................ [ 37%]
+........................................................................ [ 39%]
+........................................................................ [ 41%]
+........................................................................ [ 43%]
+........................................................................ [ 45%]
+........................................................................ [ 47%]
+........................................................................ [ 49%]
+........................................................................ [ 51%]
+........................................................................ [ 53%]
+........................................................................ [ 55%]
+........................................................................ [ 57%]
+........................................................................ [ 59%]
+........................................................................ [ 61%]
+........................................................................ [ 63%]
+........................................................................ [ 65%]
+........................................................................ [ 67%]
+........................................................................ [ 69%]
+........................................................................ [ 71%]
+........................................................................ [ 73%]
+........................................................................ [ 75%]
+........................................................................ [ 77%]
+........................................................................ [ 79%]
+........................................................................ [ 81%]
+........................................................................ [ 83%]
+........................................................................ [ 85%]
+........................................................................ [ 87%]
+........................................................................ [ 89%]
+........................................................................ [ 91%]
+........................................................................ [ 93%]
+........................................................................ [ 95%]
+........................................................................ [ 97%]
+........................................................................ [100%]
+
+======================= 3561 passed in 305.90s (0:05:05) =======================
+
+$ uv run pytest tests/hooks/test_launch_level_guard.py -q  (full file, summary line)
+======================= 3561 passed in 310.47s (0:05:10) =======================
diff --git a/tests/hooks/test_launch_level_guard.py b/tests/hooks/test_launch_level_guard.py
index 402d7964..065c8080 100644
--- a/tests/hooks/test_launch_level_guard.py
+++ b/tests/hooks/test_launch_level_guard.py
@@ -3839,3 +3839,372 @@ def test_trn_routes_never_write_approval(tmp_path):
         _approve(tmp_path, text)
     assert _session_files(tmp_path) == [SID]
     _assert_decision(_run(_skill("sc:implement"), tmp_path), tmp_path, "LL-IMPL", "W")
+
+
+# --- Task 16: push, git, alias, merge and benign corpus; T-COR-2 -------------
+#
+# Expected results are written by hand from design sections 4 and 5 (DD-2), not
+# copied from the MR corpus columns; "override:" marks a row whose result
+# differs from MR section 8.3/8.4. <R> of MR section 8.4 is the path /tmp/r.git.
+# Accepted leaks are pinned as allow with their residual id of design section 16.
+
+R16 = "/tmp/r.git"
+SEND_PACK = f"git send-pack {R16} HEAD:refs/heads/main"
+CONFIG_PUSH = "git config remote.origin.push refs/heads/feature:refs/heads/main"
+
+CORPUS16 = [
+    # Push routes.
+    ("ATK-1", "git push origin a:b `echo c:main`", PUSHFORM),
+    ("ATK-13", "git push origin --all", PUSHFORM),
+    ("ATK-25", "GIT=git; $GIT push origin main", PUSHFORM),
+    ("ATK-29", 'A=">" git push origin HEAD:main', PUSHFORM),
+    ("ATK-50", 'bash -c "git push origin main"', PUSHFORM),
+    # Aliases and variable subcommands.
+    ("ATK-10", "git rebase -x 'git -c alias.p=push p origin HEAD:main' HEAD~1", UNK),
+    ("ATK-35", "Q=sh git rebase -x 'git pu$Q origin HEAD:main' HEAD~1", UNK),
+    ("ATK-42", "git -c alias.ci=commit ci", UNK),
+    # Merges.
+    ("ATK-48", "curl -X PUT https://api.github.com/repos/o/r/pulls/5/merge", MERGE),
+    ("ATK-49", "git pull", MERGE),
+    ("ATK-51", "gh pr merge 5", MERGE),
+    # Accepted leaks, pinned allow.
+    ("ATK-26", "G=gi; ${G}t push origin main", NONE4),  # R1
+    ("ATK-27", "GH=gh; $GH pr merge 5", NONE4),  # R1
+    ("ATK-28", "$'\\x67it' push origin main", NONE4),  # R1
+    ("NATK-7", "/usr/bin/gi[t] push origin HEAD:main", NONE4),  # R1
+    ("NATK-31", "rm -rf ~/.{claude,x}/state", NONE4),  # R3
+    ("NATK-36", "flock /tmp/l gh mm 5", NONE4),  # R17 (gh alias, U24)
+    # Benign rows that involve git or gh (T-OK-10, 11, 13, 14, 35 and 36 do not).
+    ("OK-1", "git status", NONE4),
+    ("OK-2", "git diff", NONE4),
+    ("OK-3", "git log --oneline", NONE4),
+    ("OK-4", "git fetch origin", NONE4),
+    ("OK-5", "git add .dev/tasks", NONE4),
+    ("OK-6", "git checkout -b x", NONE4),
+    ("OK-7", "git commit -m x", COMMIT),
+    ("OK-8", "gh pr view 5", NONE4),
+    ("OK-9", "gh api repos/o/r/pulls", NONE4),
+    ("OK-12", "grep -rn push docs/", NONE4),
+    ("OK-15", "git push -u origin feature", PUSH_OK),
+    (
+        "OK-16",
+        f'gh pr create {REPO_FLAG} --base master --head f --title "docs: explain'
+        ' git hooks" --body "x"',
+        SUBMIT,
+    ),
+    ("OK-17", 'git commit -m "fix git handling"', COMMIT),
+    ("OK-18", "git push origin 3f2a9c1e:feature/x", PUSH_OK),
+    ("OK-19", "gh api repos/o/r/commits/abc123/check-runs --jq .total_count", NONE4),
+    (
+        "OK-20",
+        "REPO=\"$(git remote get-url origin | sed -E 's#(git@|https://)github.com"
+        "[:/]##; s#\\.git$##')\"",
+        NONE4,
+    ),
+    ("OK-21", 'git update-ref "refs/superclaude/implement/p/T1" "$start"', NONE4),
+    (
+        "OK-22",
+        'idx=$(mktemp); GIT_INDEX_FILE="$idx" git read-tree HEAD && '
+        'GIT_INDEX_FILE="$idx" git add -A && start=$(GIT_INDEX_FILE="$idx" '
+        'git write-tree); rm -f "$idx"',
+        NONE4,
+    ),
+    (
+        "OK-23",
+        '# NUL-separated revert domain of tree $1\ngit -C "$top" update-ref "$ref"'
+        ' "$now" ""\nif [[ ! $last =~ step=revert ]]; then :; fi',
+        NONE4,
+    ),
+    (
+        "OK-24",
+        "git -c merge.conflictStyle=zdiff3 -c rerere.enabled=false merge-tree"
+        " --write-tree a b",
+        NONE4,
+    ),
+    ("OK-25", 'echo "use git for hooks"', NONE4),
+    ("OK-26", 'grep -rn "git worktree" docs/', NONE4),
+    ("OK-27", "git status 2>&1 | tail -5", NONE4),
+    ("OK-28", "git commit -m x > /tmp/log 2>&1", COMMIT),
+    (
+        "OK-29",
+        f"gh pr create {REPO_FLAG} \\\n  --base master --head f --title x --body y",
+        SUBMIT,
+    ),
+    ("OK-30", "git commit -F - <<EOF\nfix: use git for hooks\nEOF", COMMIT),
+    ("OK-31", "git rebase origin/master", NONE4),
+    ("OK-32", "git log --cherry-pick --left-right a...b", NONE4),
+    # override: MR allows at FS; H4 needs the --repo operand in the segment of
+    # `pr create`, and the newline puts it in the next segment, so REPO at FS.
+    ("OK-33", f"gh pr create \\\n  {REPO_FLAG} --title x --body y", SUBMIT_REPO),
+    ("OK-34", "gh pr view 5 \\\n  --json mergeable,mergeStateStatus", NONE4),
+    # Pinned over-blocks.
+    ("OVR-1", "git log --grep merge", MERGE),
+    (
+        "OVR-2",
+        'gh pr create --repo o/r --title "x" --body "this pull request fixes git'
+        ' hooks"',
+        MERGE,
+    ),
+    ("OVR-3", "git log --oneline | grep push", PUSHFORM),
+    ("OVR-4", 'gh pr create --repo o/r --title "fix api docs"', GHWRITE),
+    ("OVR-5", "git config --get-regexp alias.", UNK),
+    ("OVR-6", "git \\\ncommit -m x", UNK),
+    # Amendment attacks that concern git (N-ATK-39 is the Write test below).
+    ("NATK-1", "gi\\\nt push origin HEAD:main", UNK),
+    ("NATK-2", 'bash -c "gi\\\nt push origin HEAD:main"', UNK),
+    ("NATK-3", "git$'' push origin HEAD:main", PUSHFORM),
+    ("NATK-4", 'g$""it push origin HEAD:main', PUSHFORM),
+    ("NATK-5", f"if true; then {SEND_PACK}; fi", UNK),
+    ("NATK-6", f"find . -maxdepth 0 -exec {SEND_PACK} \\;", PUSHFORM),
+    ("NATK-8", f"if true; then {CONFIG_PUSH}; fi", UNK),
+    ("NATK-9", f"env -u FOO {CONFIG_PUSH}", UNK),
+    ("NATK-10", f"flock /tmp/l {CONFIG_PUSH}", UNK),
+    # Second step of N-ATK-8, 9, 10 and 39: the canonical push is allowed at FS;
+    # a pre-set push config is residual R11 (the agent cannot set one).
+    ("NATK-8-step2", "git push origin feature", PUSH_OK),  # R11
+    ("NATK-11", f"timeout -s KILL 30 {SEND_PACK}", PUSHFORM),
+    ("NATK-12", f"git rebase -x '{SEND_PACK}' HEAD~1", PUSHFORM),
+    ("NATK-13", f"taskset -c 0 {SEND_PACK}", PUSHFORM),
+    ("NATK-14", "git rebase -x 'gi\\\nt push origin HEAD:main' HEAD~1", UNK),
+    ("NATK-15", "git$'' -c x.y=z push origin HEAD:main", PUSHFORM),
+    ("NATK-16", "git$'' merge other --no-edit", MERGE),
+    ("NATK-17", "gi\\\nt merge other --no-edit", UNK),
+    ("NATK-18", "git$'' commit --allow-empty -m x", COMMIT),
+    ("NATK-19", "gi\\\nt commit --allow-empty -m x", UNK),
+    (
+        "NATK-37",
+        "sudo -u coder git remote set-url --push origin https://github.com/evil/x",
+        UNK,
+    ),
+    # Design section 10, git rows.
+    ("EDGE-title", 'gh pr create --repo o/r --title "docs: explain git hooks"', SUBMIT),
+    ("EDGE-stash", "git stash push -m wip", PUSHFORM),
+    ("EDGE-stash-u", "git stash -u -m x", NONE4),
+    ("EDGE-pipe", "git push origin f 2>&1 | tail -5", PUSHFORM),
+    ("EDGE-slashes", "git push origin x:refs/heads//main", PUSH_OK),
+    ("EDGE-c-remote", "git -c remote.origin.push=x:main push origin f", UNK),
+    # The section 5.1 table calls `config` NONE; G2 (`remote.`) makes it UNKNOWN,
+    # which is the section 10 row, R8 (d).
+    ("EDGE-config-url", "git config --get remote.origin.url", UNK),
+    ("EDGE-heredoc", "cat > Makefile <<EOF\nall:\\\n\techo x\nEOF", UNK),
+    ("EDGE-scope", 'git commit -m "fix(ccsession): x"', ESCAPE),
+    ("EDGE-install-hooks", "git add src/superclaude/cli/install_hooks.py", TAMPER),
+    # Regression: nonempty PR repo operand (H4).
+    ("REG-repo-option", "gh pr create --repo --title x", SUBMIT_REPO),
+    # A value option with no value at all is UNKNOWN (G4: "a value-taking Git/gh
+    # option with no following value adds UNKNOWN"), which precedes SUBMIT.
+    ("REG-repo-dangling", "gh pr create --title x --repo", UNK),
+    ("REG-repo-empty-eq", "gh pr create --repo= --title x", SUBMIT_REPO),
+    ("REG-repo-R", "gh pr create -R o/r --title x", SUBMIT),
+    ("REG-repo-eq", "gh pr create --repo=o/r --title x", SUBMIT),
+    # Regression: protected destination (one `refs/heads/` or `heads/` stripped).
+    ("REG-prot-refs", "git push origin x:refs/heads/main", PROTECTED),
+    ("REG-prot-heads", "git push origin x:heads/master", PROTECTED),
+    ("REG-prot-u", "git push -u origin master", PROTECTED),
+    ("REG-prot-twice", "git push origin x:refs/heads/refs/heads/main", PUSH_OK),
+    ("REG-prot-head", "git push origin x:HEAD", PUSHFORM),
+]
+assert len({row[0] for row in CORPUS16}) == len(CORPUS16), "duplicate corpus id"
+
+
+@pytest.mark.parametrize(
+    "command, level, msg_id",
+    [
+        pytest.param(command, level, msg_id, id=f"{row_id}-{level}")
+        for row_id, command, ids in CORPUS16
+        for level, msg_id in zip(LEVEL_ORDER, ids)
+    ],
+)
+def test_corpus16(tmp_path, command, level, msg_id):
+    # T-COR-1, Task 16 rows.
+    _git_case(tmp_path, command, level, msg_id)
+
+
+@pytest.mark.parametrize("level", LEVEL_ORDER)
+def test_corpus16_natk39_write_git_config(tmp_path, level):
+    # N-ATK-39: the Write of the push redirect is TAMPER; its second step is the
+    # NATK-8-step2 row (R11).
+    _bind(tmp_path, *LEVEL_FILES[level])
+    content = '[remote "origin"]\n\tpush = refs/heads/feature:refs/heads/main\n'
+    result = _run(_edit("Write", "~/.config/git/config", content=content), tmp_path)
+    _assert_decision(result, tmp_path, "LL-TAMPER", level)
+
+
+@pytest.mark.parametrize(
+    "payload",
+    [
+        {
+            "hook_event_name": "PostToolUse",
+            "session_id": SID,
+            "tool_name": "Bash",
+            "tool_input": {
+                "hook_event_name": "PreToolUse",
+                "command": "git push origin main",
+            },
+        },
+        {
+            "hook_event_name": "PreToolUse",
+            "session_id": SID,
+            "tool_name": "Read",
+            "tool_input": {"tool_name": "Bash", "command": "git push origin main"},
+        },
+    ],
+    ids=["REG-dispatch-nested-event", "REG-dispatch-nested-tool"],
+)
+def test_corpus16_typed_top_level_dispatch(tmp_path, payload):
+    # Regression: only the top-level event and tool_name dispatch. A nested
+    # PreToolUse under PostToolUse is a bound other event (LL-BROKEN); a nested
+    # Bash under Read is the Read tool (NONE).
+    _bind(tmp_path, "full-submit")
+    result = _run(payload, tmp_path)
+    if payload["hook_event_name"] == "PostToolUse":
+        _assert_decision(result, tmp_path, "LL-BROKEN", "FS")
+    else:
+        _assert_decision(result, tmp_path, None, "FS")
+
+
+@pytest.mark.parametrize(
+    "sid", [None, "bad id!"], ids=["REG-idloss-missing", "REG-idloss-invalid"]
+)
+def test_corpus16_identity_loss_push_allowed(tmp_path, sid):
+    # Regression (design section 10 row 3): no readable id, store non-empty with
+    # a bound worktree session: allowed silently, no enforcement claim.
+    _bind(tmp_path, "worktree")
+    payload = _bash("git push origin main")
+    if sid is None:
+        del payload["session_id"]
+    else:
+        payload["session_id"] = sid
+    result = _run(payload, tmp_path)
+    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
+
+
+def test_corpus16_no_replacement_binding(tmp_path):
+    # Regression (B8): a later marker with a full-submit record never replaces
+    # the worktree binding; the record is consumed and a push stays blocked at W.
+    _pending(tmp_path, "worktree")
+    _run(_prompt(_marker() + " plan"), tmp_path)
+    _assert_bound(tmp_path, SID, "worktree")
+    record = _pending(tmp_path, "full-submit", NONCE2)
+    result = _run(_prompt(_marker(NONCE2) + " plan"), tmp_path)
+    assert (result.returncode, result.stderr) == (0, b"")
+    _assert_bound(tmp_path, SID, "worktree")
+    assert not record.exists()
+    result = _run(_bash("git push origin feature"), tmp_path)
+    _assert_decision(result, tmp_path, "LL-PUSH", "W", text=True)
+
+
+# T-COR-2: the real push attacks of MR section 8.3 (and the N-ATK push rows),
+# adapted to a temporary clone whose HEAD (feature) is ahead of remote main.
+# Leaks T-ATK-26 and T-ATK-28 are real but residual R1, so they are not replayed.
+COR2_ATTACKS = {
+    "ATK-1": "git push origin feature:x `echo feature:main`",
+    "ATK-2": "git push origin feature:x \\\nfeature:main",
+    "ATK-4": "/usr/lib/git-core/git-push origin HEAD:main",
+    "ATK-5": "$(git --exec-path)/git-push origin HEAD:main",
+    "ATK-10": "git rebase -x 'git -c alias.p=push p origin HEAD:main' HEAD~1",
+    "ATK-11": "git status \\\\\ngit -c alias.p=push p origin HEAD:main",
+    "ATK-13": "git push origin --all",
+    "ATK-14": "git push origin --mirror",
+    "ATK-25": "GIT=git; $GIT push origin HEAD:main",
+    "ATK-29": 'A=">" git push origin HEAD:main',
+    "ATK-32": 'git -c "x.y=a status" push origin HEAD:main',
+    "ATK-34": "X=sh git rebase -x 'git -c alias.p=pu$X p origin HEAD:main' HEAD~1",
+    "ATK-35": "Q=sh git rebase -x 'git pu$Q origin HEAD:main' HEAD~1",
+    "ATK-36": "git rebase -x 'git `echo pu`sh origin HEAD:main' HEAD~1",
+    "ATK-37": "$'git' push origin HEAD:main",
+    "ATK-38": "echo feature:main | xargs git push origin feature:feature",
+    "ATK-39": "git push origin 'feature:ma''in'",
+    "ATK-40": 'g""it push origin HEAD:main',
+    "ATK-41": "\\git push origin HEAD:main",
+    "ATK-45": "git --attr-source HEAD push origin HEAD:main",
+    "ATK-50": 'bash -c "git push origin HEAD:main"',
+    "ATK-57": "git rebase -x 'G=gi; ${G}t push origin HEAD:main' HEAD~1",
+    "NATK-1": "gi\\\nt push origin HEAD:main",
+    "NATK-2": 'bash -c "gi\\\nt push origin HEAD:main"',
+    "NATK-3": "git$'' push origin HEAD:main",
+    "NATK-4": 'g$""it push origin HEAD:main',
+    "NATK-5": "if true; then git send-pack {R} HEAD:refs/heads/main; fi",
+    "NATK-6": "find . -maxdepth 0 -exec git send-pack {R} HEAD:refs/heads/main \\;",
+    "NATK-11": "timeout -s KILL 30 git send-pack {R} HEAD:refs/heads/main",
+    "NATK-12": "git rebase -x 'git send-pack {R} HEAD:refs/heads/main' HEAD~1",
+    "NATK-13": "taskset -c 0 git send-pack {R} HEAD:refs/heads/main",
+    "NATK-15": "git$'' -c x.y=z push origin HEAD:main",
+}
+
+
+def test_cor2_replay_real_attacks(tmp_path):
+    # T-COR-2: the guard runs first on each command and only a command it allows
+    # is executed, in a clone of a bare remote under tmp_path (never a real one).
+    git = shutil.which("git")
+    if git is None:
+        pytest.skip("git is not installed")
+    remote, clone = tmp_path / "remote.git", tmp_path / "clone"
+    env = {
+        "HOME": str(tmp_path / "githome"),
+        "PATH": os.environ.get("PATH", ""),
+        "GIT_CONFIG_NOSYSTEM": "1",
+        "GIT_CONFIG_GLOBAL": os.devnull,
+        "GIT_TERMINAL_PROMPT": "0",
+        "GIT_AUTHOR_NAME": "t",
+        "GIT_AUTHOR_EMAIL": "t@t",
+        "GIT_COMMITTER_NAME": "t",
+        "GIT_COMMITTER_EMAIL": "t@t",
+    }
+
+    def sh(command, cwd=clone):
+        return subprocess.run(
+            [BASH, "-c", command], cwd=cwd, env=env, capture_output=True, timeout=30
+        )
+
+    def refs():
+        out = subprocess.run(
+            [git, "--git-dir", str(remote), "for-each-ref"],
+            env=env,
+            capture_output=True,
+            check=True,
+            timeout=30,
+        )
+        return out.stdout.decode()
+
+    def commit(name):
+        (clone / name).write_text(name)
+        assert sh(f"git add {name} && git commit -q -m {name}").returncode == 0
+
+    clone.mkdir()
+    assert sh(f"git init -q --bare {remote}", cwd=tmp_path).returncode == 0
+    assert sh(f"git init -q -b main && git remote add origin {remote}").returncode == 0
+    commit("a")
+    assert sh("git push -q origin main").returncode == 0
+    assert sh("git checkout -q -b feature").returncode == 0
+    commit("b")
+    assert sh("git push -q origin feature").returncode == 0
+    commit("c")
+    before = refs()
+    assert "refs/heads/main" in before and "refs/heads/feature" in before
+
+    for row_id, command in COR2_ATTACKS.items():
+        command = command.replace("{R}", str(remote))
+        for level in LEVEL_ORDER:
+            guard = tmp_path / "guard" / f"{row_id}-{level}"
+            _bind(guard, *LEVEL_FILES[level])
+            result = _run(_bash(command), guard)
+            if result.returncode == 0:
+                sh(command)
+            assert result.returncode == 2, (row_id, level)
+            assert refs() == before, (row_id, level)
+
+    # The permitted canonical push: blocked below FS, allowed and real at FS.
+    for level in LEVEL_ORDER:
+        guard = tmp_path / "guard" / f"permitted-{level}"
+        _bind(guard, *LEVEL_FILES[level])
+        result = _run(_bash("git push origin feature"), guard)
+        assert result.returncode == (0 if level == "FS" else 2), level
+        if level == "FS":
+            assert sh("git push -q origin feature").returncode == 0
+    head = sh("git rev-parse HEAD").stdout.decode().strip()
+    after = refs()
+    assert after != before
+    assert f"{head} commit\trefs/heads/feature" in after
+    main = [line for line in before.splitlines() if line.endswith("refs/heads/main")]
+    assert main and main[0] in after.splitlines()

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
