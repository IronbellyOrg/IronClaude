52d91b4f4e7deb8d52877f8cb67cb359519e008a
Review one task for spec compliance.

Task brief: T7 (plan .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/TASK-WF-designSpec-20261108-165559.md:100-109; AC ids T7.AC1.. in order of its Acceptance criteria bullets)
## Task 7: Make l2_status, the session report and cmd_launch use the real L2 state

Depends on: Task 6

In the same `orca_worktree.py`, change `l2_status(wt)` to the read-only re-check of source §3.4 returning a `(state, reason)` tuple (spec FR-024, FR-041), change `session_report` to take that tuple and print its line (about `:1032`, `:1061-1067`, callers near `:1311-1312` and `:1376`; source §12 OC-2), set `L2_ABSENT_WHY` and `REMEDY["W-L2-ABSENT"]` (FR-043..FR-045), rewrite the comment near `:794-795` and the docstring near `:49-51`, and add steps 4-6 of the `cmd_launch` order in source §3.2. The `present-unverified` state is removed (AC-6) and a `core.hooksPath` case reports `unsupported` (OC-6). `W-L2-ABSENT` stays a warning.

Acceptance criteria:
- `l2_status` and `install_l2` report the same state for the same tree, including `conflict` and `unsupported`.
- `grep -rn present-unverified src tests` prints nothing once Task 8's test and claim.md edits land; the remaining hits are listed in `./artifacts/t7-present-unverified.md` until then.
- `cmd_launch` still launches when L2 is absent and prints the `W-L2-ABSENT` warning.
Global constraints: ## Constraints

- Owner decision OD-1: L2 covers only the tested local Bash surface. The B-CTX gaps (Monitor, a `setsid` child, a killed supervisor) stay documented limits (source §9.1, LIM-1..LIM-3, LIM-10); no task closes them.
- Owner decision OD-2: an `unknown` identity refuses only pushes whose destination is exactly `refs/heads/main` or `refs/heads/master`, with a diagnostic, and allows every other push (source §7.1, sequence §4.3).
- Owner decision OD-3: the IR-7 refusal code path is built but OFF. `IR7_REFUSE = False`, `W-L2-ABSENT` stays a warning, and the code goes in its own clearly marked commit E after every L2 commit. Turning it on is out of scope.
- The requirements are `.dev/brainstorms/20261108-094705-l2-pre-push-guard/merged-requirements.md` ("the spec"; FR, NFR, AC, LIM and T IDs refer to it). The design (./source.md) adds no requirement; where code and spec disagree, use the proposed resolution in source §12 and list it in that commit's body for owner review.
- Placement (source §1): one shared, owned `hooks/pre-push` found by git's default lookup. Never replace a foreign hook, migrate `core.hooksPath`, forward to another hook, install stubs, or change `hooks.json` or any git configuration. Publish files without replacing an existing file.
- Each UNVERIFIED item in source §11 (U-1..U-14) is settled by the check that item names, in the task that needs it; never assume an answer. A test that needs a second uid (U-7) is `skipif` with a reason when none is available.
- Edit sources under `src/superclaude/` and their `plugins/superclaude/` byte mirrors, then run `make sync-dev` and `make verify-sync`. Never stage any `.claude/` path. Stage only `src/`, `plugins/`, `tests/`, `docs/` and `.dev/tasks/` paths; `.dev/tasks/` is always staged with `git add .dev/tasks`.
- Installed primitives name only `~/.claude/...` or `${0%/*}` paths (NFR-003): `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` gains no hit.
- Read only, never edited: `tests/hooks/test_launch_level_guard.py` (NFR-009, #440) and `.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/`.
- Commits are local only, each ending with the line `Co-Authored-By: Claude Code <noreply@anthropic.com>`. No push and no pull request.
- Python runs through `uv run` only.
Start sha: 52d91b4f4e7deb8d52877f8cb67cb359519e008a
Diff against the start snapshot: run `git -C /home/coder/workspaces/worktrees/IronClaude/issue-441 diff 52d91b4f4e7deb8d52877f8cb67cb359519e008a -- src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t7-present-unverified.md .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t7-smoke.py` (tree-ish vs worktree), and read in full every path of [src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t7-present-unverified.md .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t7-smoke.py] that `git -C /home/coder/workspaces/worktrees/IronClaude/issue-441 status --porcelain --untracked-files=all -- src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t7-present-unverified.md .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t7-smoke.py` shows as `??` and that is absent from `git -C /home/coder/workspaces/worktrees/IronClaude/issue-441 ls-tree -r --name-only 52d91b4f4e7deb8d52877f8cb67cb359519e008a`. Live files are under /home/coder/workspaces/worktrees/IronClaude/issue-441.
Delta diff from the previous reviewed tree (empty on the first review): diff --git a/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t7-present-unverified.md b/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t7-present-unverified.md
index 8d6e4a78..24ca8353 100644
--- a/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t7-present-unverified.md
+++ b/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t7-present-unverified.md
@@ -8,20 +8,20 @@ File: `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` (uncom
 - `install_l2` (line 1335) reports through `l2_status` at S2 (entry exists) and S6 (after publish), mapped by `_l2_as_install` (line 1047): `owned` becomes `installed` (S6) or `owned` (S2), `absent` becomes `unavailable`. This closes T6 findings F1.3 (a raced `absent` at S6 is now `unavailable`) and F1.5 (one path).
 - T6 F1.1: a missing packaged hook gives the FR-033 fixed text "the packaged pre-push hook is not installed (run superclaude install)" (`L2_WHY_NOT_INSTALLED`).
 - T6 F1.4: the git-2.31 hint is only in `L2_WHY_GIT` (rev-parse failed); a path mismatch says only "git's pre-push hook path is not <hooks>/pre-push".
-- FR-033 item 1: a config read failure or a git failure is `absent` in `_l2_preconditions`, so `install_l2` returns `unavailable` (was `unsupported` in T6).
+- FR-033 and OC-10: a config read failure or a git failure is `absent` in `_l2_preconditions` (what `l2_status` reports, FR-041), and `install_l2` maps it to `unsupported`, nothing written (as in T6; review r1-1 F1.1).
 - `cmd_launch` (line 1675): source §3.2 steps 4-6 before `publish_pending`: `install_l2(wt)` (advisory), then `l2_status(wt)` (the reported answer), then `W-L2-ABSENT` with `L2_ABSENT_WHY + reason` when the state is not `owned`. The launch proceeds (IR-7 stays a warning; `IR7_REFUSE` itself comes in commit E, owner decision OD-3).
 - `session_report(wt, l2, inode)` takes the `(state, reason)` pair and prints `L2 pre-push: owned (...)` or `L2 pre-push: <state> (<reason>; the limits are enforced by the L1 guard only)`.
 
 ## Divergences (for commit B's body and owner review)
 
-1. A git or config failure, a missing packaged hook, missing uv, or bad data paths: `l2_status` says `absent`, `install_l2` says `unavailable` (FR-031's install states have no `absent`).
+1. A git or config failure: `l2_status` says `absent` (FR-041), `install_l2` says `unsupported` (FR-033, OC-10). A missing packaged hook, missing uv, or bad data paths: `l2_status` says `absent`, `install_l2` says `unavailable` (FR-031's install states have no `absent`).
+4. An owned `pre-push` entry whose data file is missing reports `conflict` `data-file-differs` in both functions (for commit B's OC-12 note).
 2. An unsafe hooks directory: `unsupported` in both functions, while FR-041 lists it under `absent` (OC-9 choice kept from T6).
 3. With no `pre-push` entry, `l2_status` reports `absent` "no pre-push hook" even when the packaged hook is also missing; the entry check runs first because no entry means no L2 regardless of the package.
 
 ## Remaining old-state hits outside the file (fixed in T8)
 
 - `src/superclaude/skills/sc-issue-protocol/refs/claim.md:120` (`present-unverified` in the launch JSON description) and `:127` (W-L2-ABSENT remedy "the L2 layer is not built yet").
-- `src/superclaude/skills/sc-issue-protocol/SKILL.md:92` (Wave 8 text names `present-unverified`).
 - `tests/skills/test_issue_orca_worktree.py:1672`, `:1691`, `:1692` (`present-unverified` expectations), `:1728` and `:1746` ("L2 layer is not built yet"), `:1745` ("no executable pre-push hook").
 
 ## Tests (`uv run pytest tests/skills/test_issue_orca_worktree.py`): 6 failed, 157 passed
@@ -47,4 +47,5 @@ no-packaged: install=('unavailable', 'the packaged pre-push hook is not installe
 hookspath: install=('unsupported', 'core.hooksPath is set, ...') status=('unsupported', 'core.hooksPath is set, ...')
 linked: install=('installed', '') status=('owned', '')
 linked in common dir: True
+not-a-repo: install=('unsupported', 'git-failed: git rev-parse failed (...)') status=('absent', 'git-failed: git rev-parse failed (...)')
 ```
diff --git a/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t7-smoke.py b/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t7-smoke.py
index 6272a6a9..a233750f 100644
--- a/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t7-smoke.py
+++ b/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t7-smoke.py
@@ -64,4 +64,7 @@ subprocess.run([*g, "commit", "-q", "--allow-empty", "-m", "i"], check=True)
 subprocess.run([*g, "worktree", "add", "-q", str(base / "lw")], check=True)
 both("linked", base / "lw")
 print("linked in common dir:", (m / ".git/hooks/pre-push").is_file())
+nr = base / "not-a-repo"
+nr.mkdir()
+both("not-a-repo", nr)
 shutil.rmtree(base)
diff --git a/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py b/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py
index f6a0b4bf..1f08e3c0 100644
--- a/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py
+++ b/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py
@@ -50,7 +50,7 @@ when the guard would not be effective. It then installs the owned L2
 pre-push hook (``install_l2``, advisory) and re-checks it read-only
 (``l2_status``); any state other than ``owned`` adds the warning
 ``W-L2-ABSENT`` with the reason, and the launch goes ahead (IR-7 stays a
-warning while ``IR7_REFUSE`` is off). It then publishes the launch record the enforcement hook reads
+warning; an off ``IR7_REFUSE`` switch arrives in a later commit). It then publishes the launch record the enforcement hook reads
 (``$HOME/.claude/state/launch-level/pending/<nonce>``, one word), then runs
 ``orca agent launch --surface terminal`` with a prompt that starts with
 ``[sc-launch:v1:<nonce>]``, checks the agent's screen for the ccsession shim, and
@@ -1290,7 +1290,7 @@ def _l2_preconditions(
     """Source §3.3 S1 / §3.4: ('', '', hooks dir) when L2 can be checked, else a verdict.
 
     Verdicts use ``l2_status``'s states; a git failure is ``absent`` (FR-041),
-    which ``install_l2`` reports as ``unavailable`` (FR-033 item 1). Only
+    which ``install_l2`` reports as ``unsupported`` (FR-033, OC-10). Only
     ``create`` makes a missing hooks directory; without it a missing one is
     ``absent``.
     """
@@ -1342,7 +1342,9 @@ def install_l2(wt: str) -> tuple[str, str]:
     env = clean_git_env()
     state, why, hooks = _l2_preconditions(wt, env)
     if hooks is None:
-        return _l2_as_install(state, why)
+        # With create=True, `absent` here is only a config or git failure:
+        # FR-033 and OC-10 make that `unsupported`, nothing written.
+        return ("unsupported" if state == "absent" else state), why
     why, packaged, expected = _l2_packaged()
     if why:
         return "unavailable", why
@@ -1671,7 +1673,7 @@ def cmd_launch(args: argparse.Namespace) -> int:
     # Source §3.2 steps 4-6, before publish_pending: claim the L2 hook (its
     # answer is advisory), re-check it read-only (that answer is the one the
     # launch reports), and warn when it is not owned. IR-7 stays a warning
-    # while IR7_REFUSE is off (owner decision OD-3).
+    # (owner decision OD-3; the off IR7_REFUSE switch comes in a later commit).
     install_l2(wt)
     l2, l2_reason = l2_status(wt)
     l2_notes = [("W-L2-ABSENT", L2_ABSENT_WHY + l2_reason)] if l2 != "owned" else []
Earlier blocking findings of this start (empty on the first review): A1 r1-1 F1.1 blocking src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1304 ac=scope chk=n,n,n,y family=l2-install-state-config first=A1 origin=new: a config-read or git failure makes install_l2 return `unavailable`; OC-10 (source.md:780) and FR-033 (merged-requirements.md:179) say `unsupported`, nothing written.
A1 r1-1 F1.2 minor src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1293 ac=scope chk=n,y,n,n family=l2-install-state-config first=A1 origin=new: the _l2_preconditions docstring cites FR-033 item 1 for `unavailable`; FR-033 says `unsupported`.
A1 r1-1 F1.3 minor .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t7-present-unverified.md:24 ac=T7.AC2 chk=n,y,n,n family=t7-hit-list first=A1 origin=new: the hit list names SKILL.md:92, which does not contain present-unverified.
A1 r1-1 F1.4 minor src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:53 ac=scope chk=n,n,n,n family=ir7-refuse-forward-ref first=A1 origin=new: the docstring names IR7_REFUSE before commit E defines it.
A1 r1-1 F1.5 minor src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1225 ac=scope chk=n,n,n,n family=l2-data-missing first=A1 origin=new: an owned entry with a missing data file reports `conflict data-file-differs`; state it in commit B's OC-12 note.
A1 r1-1 F1.6 minor src/superclaude/skills/sc-issue-protocol/scripts/__pycache__/orca_worktree.cpython-311.pyc:1 ac=T7.AC2 chk=n,n,n,n family=t7-hit-list first=A1 origin=new: a stale gitignored .pyc still holds the old strings; no action.
Saved-probe re-check hit locations (may be empty): orca_worktree.py:1304 and :1313 (probe family l2-install-state-config after-hits: the two absent sources l2_status keeps per FR-041; install_l2:1347 maps them to unsupported per FR-033/OC-10). Probe file: .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/retries/T7/probe-1-1.md

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
