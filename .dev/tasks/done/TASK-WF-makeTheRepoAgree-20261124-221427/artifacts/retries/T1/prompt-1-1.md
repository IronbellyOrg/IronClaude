ad1a6e03d995f241ff80859f700ad640c0e39ae9
Review one task for spec compliance.

Task brief: ## Task 1: Protect refs/heads/integration in the L2 pre-push hook and its mirror

Edit `src/superclaude/hooks/scripts/launch-level-pre-push.sh`: line 17 becomes `L2_PROTECTED=(refs/heads/main refs/heads/master refs/heads/integration)`, the header comment at lines 8-9 names all three refs, and line 2 is bumped to `# launch-level-pre-push-version: 2` (the hook is byte-pinned and the installer replaces an installed hook only when the version line differs, so existing worktrees pick the fix up). Copy the finished file byte-for-byte over `plugins/superclaude/hooks/scripts/launch-level-pre-push.sh` (keep the executable bit). Update the version string `L2_VERSION_LINE` in `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` (line 877) and the pins `L2_VERSION_LINE` and `L2_HOOK_SHA256` in `tests/cli/test_install_hooks.py` (lines 1100-1101, new sha256 of the hook file). In `orca_worktree.py` `_l2_selftest` (loop at line 1363) add `refs/heads/integration` to the refs that must be refused with `L2-UNKNOWN` when the data file is gone.

Acceptance criteria (ids):
T1.AC1: `grep -n L2_PROTECTED src/superclaude/hooks/scripts/launch-level-pre-push.sh plugins/superclaude/hooks/scripts/launch-level-pre-push.sh` shows `refs/heads/integration` in both, and the two files are byte-identical.
T1.AC2: `tests/cli/test_install_hooks.py` (mirror, executable, version-line and sha256-pin tests), `tests/hooks/test_launch_level_pre_push.py::test_t23_hook_sha256_pinned_with_version_line`, `tests/skills/test_issue_l2_install.py` and `tests/skills/test_issue_orca_worktree.py` pass; `tests/hooks/test_launch_job_identity.py` (own protected-ref list, unchanged) still passes.
T1.AC3: After `make sync-dev`, `make verify-sync` passes and no `.claude/` path other than `.claude/settings.json` is staged.
Global constraints: - One pull request, base `integration`, branch `fix/default-branch-integration`, opened only through `/sc:pr-submit --monitor 3` against `IronbellyOrg/IronClaude`. Never merge, never touch SuperClaude-Org, no Orca link flags, no model flag, never Opus.
- Edit only `src/superclaude/**`, `tests/**`, `plugins/superclaude/hooks/scripts/launch-level-pre-push.sh` (a committed byte-identical mirror with no generator: `scripts/build_superclaude_plugin.py` writes `dist/` only) and the two root files `CLAUDE.md` and `.github/PULL_REQUEST_TEMPLATE.md`.
- Do not touch `docs/generated`, `docs/testing`, the `/sc:impact` and `/sc:auggie-review` diff examples, release tooling (`/sc:post-release`, `release-procedure.md`), or any text that says master is the production branch. Change no ABSOLUTE RULE wording in `CLAUDE.md` other than branch names.
- Never stage `.claude/` mirrors (only `.claude/settings.json` is tracked); `.dev/tasks` is staged. Commit only on the feature branch with `Co-Authored-By: Claude Code <noreply@anthropic.com>`.
- Follow-ups to list in the PR body, not fix here: the L1 command guard `src/superclaude/hooks/scripts/launch-level-guard.sh` (line 59 text, line 736 `master | main`) still classifies only master and main as PROTECTED (the L2 hook is the backstop); release tooling that assumes master.
Start sha: ad1a6e03d995f241ff80859f700ad640c0e39ae9
Diff against the start snapshot: diff --git a/plugins/superclaude/hooks/scripts/launch-level-pre-push.sh b/plugins/superclaude/hooks/scripts/launch-level-pre-push.sh
index 767c8a8d5..c74b73c63 100755
--- a/plugins/superclaude/hooks/scripts/launch-level-pre-push.sh
+++ b/plugins/superclaude/hooks/scripts/launch-level-pre-push.sh
@@ -1,12 +1,12 @@
 #!/bin/bash -p
-# launch-level-pre-push-version: 1
+# launch-level-pre-push-version: 2
 # Launch-level L2 git pre-push hook, IronbellyOrg/IronClaude issue #441.
 # Installed by the claim as <git-common-dir>/hooks/pre-push next to its data
 # file pre-push.launch-level (line 1: pinned HOME, line 2: pinned uv directory).
 # The actor is decided first by the launch-job identity selector; an ordinary
 # push exits 0 at once and silently, without reading stdin. A governed push to
-# refs/heads/main or refs/heads/master is refused; an unknown actor is refused
-# only for those two refs. Exit 0 allows, 1 refuses, 2 refuses a malformed
+# refs/heads/main, refs/heads/master or refs/heads/integration is refused; an
+# unknown actor is refused only for those three refs. Exit 0 allows, 1 refuses, 2 refuses a malformed
 # stream. Arguments are ignored; no file is written and git is never called.
 # -p: bash ignores BASH_ENV, ENV, SHELLOPTS and imported functions. Linux only.
 
@@ -14,7 +14,7 @@ LC_ALL=C
 export LC_ALL
 set -f
 
-L2_PROTECTED=(refs/heads/main refs/heads/master)
+L2_PROTECTED=(refs/heads/main refs/heads/master refs/heads/integration)
 L2_HOOKS=${0%/*}
 L2_DATA=$L2_HOOKS/pre-push.launch-level
 L2_HOME=
diff --git a/src/superclaude/hooks/scripts/launch-level-pre-push.sh b/src/superclaude/hooks/scripts/launch-level-pre-push.sh
index 767c8a8d5..c74b73c63 100755
--- a/src/superclaude/hooks/scripts/launch-level-pre-push.sh
+++ b/src/superclaude/hooks/scripts/launch-level-pre-push.sh
@@ -1,12 +1,12 @@
 #!/bin/bash -p
-# launch-level-pre-push-version: 1
+# launch-level-pre-push-version: 2
 # Launch-level L2 git pre-push hook, IronbellyOrg/IronClaude issue #441.
 # Installed by the claim as <git-common-dir>/hooks/pre-push next to its data
 # file pre-push.launch-level (line 1: pinned HOME, line 2: pinned uv directory).
 # The actor is decided first by the launch-job identity selector; an ordinary
 # push exits 0 at once and silently, without reading stdin. A governed push to
-# refs/heads/main or refs/heads/master is refused; an unknown actor is refused
-# only for those two refs. Exit 0 allows, 1 refuses, 2 refuses a malformed
+# refs/heads/main, refs/heads/master or refs/heads/integration is refused; an
+# unknown actor is refused only for those three refs. Exit 0 allows, 1 refuses, 2 refuses a malformed
 # stream. Arguments are ignored; no file is written and git is never called.
 # -p: bash ignores BASH_ENV, ENV, SHELLOPTS and imported functions. Linux only.
 
@@ -14,7 +14,7 @@ LC_ALL=C
 export LC_ALL
 set -f
 
-L2_PROTECTED=(refs/heads/main refs/heads/master)
+L2_PROTECTED=(refs/heads/main refs/heads/master refs/heads/integration)
 L2_HOOKS=${0%/*}
 L2_DATA=$L2_HOOKS/pre-push.launch-level
 L2_HOME=
diff --git a/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py b/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py
index 1ff1a7b20..d010b0e88 100644
--- a/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py
+++ b/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py
@@ -874,7 +874,7 @@ L2_ABSENT_WHY = "the owned L2 pre-push hook is not in effect for this worktree:
 GUARD_COMMAND = "~/.claude/hooks/launch-level-guard.sh"
 IDENTITY_COMMAND = "~/.claude/hooks/launch-job-identity.sh"
 GUARD_VERSION_LINE = "# launch-level-guard-version: 2"
-L2_VERSION_LINE = "# launch-level-pre-push-version: 1"
+L2_VERSION_LINE = "# launch-level-pre-push-version: 2"
 GOVERNED_TOOLS = (
     "Bash",
     "Skill",
@@ -1360,7 +1360,7 @@ def _l2_selftest(wt: str, staged: Path, data_copy: Path, env: Mapping[str, str])
     if not hook(push("refs/heads/main")).ok:
         return "main-push"
     data_copy.unlink()
-    for ref in ("refs/heads/main", "refs/heads/master"):
+    for ref in ("refs/heads/main", "refs/heads/master", "refs/heads/integration"):
         res = hook(push(ref))
         if res.rc != 1 or "L2-UNKNOWN" not in res.err:
             return "no-data-refusal"
diff --git a/tests/cli/test_install_hooks.py b/tests/cli/test_install_hooks.py
index eced5642b..a9f36a6f5 100644
--- a/tests/cli/test_install_hooks.py
+++ b/tests/cli/test_install_hooks.py
@@ -1097,8 +1097,8 @@ def test_launch_level_guard_script_is_packaged_listed_executable_and_mirrored():
 
 # T-23 / NFR-008: a byte change to the packaged L2 hook without a version bump
 # fails here. Bump L2_VERSION_LINE in the hook and here, then re-pin the sha256.
-L2_VERSION_LINE = "# launch-level-pre-push-version: 1"
-L2_HOOK_SHA256 = "d8a12f0302ceb78f2ced14e3c3dec72984e9fe1c7c911374ebff0de3ec88645b"
+L2_VERSION_LINE = "# launch-level-pre-push-version: 2"
+L2_HOOK_SHA256 = "c2b559e5c62720944a97190da724ee74caa7487234d9a401ce4a20f9586cc26c"
 
 
 def test_launch_level_pre_push_script_is_packaged_listed_executable_and_mirrored():

Codegraph context
index_state: absent
checked_at: n/a
worktree_root: /home/coder/workspaces/worktrees/IronClaude/fix-default-branch-integration
projectPath: n/a
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep/Read floor.

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
