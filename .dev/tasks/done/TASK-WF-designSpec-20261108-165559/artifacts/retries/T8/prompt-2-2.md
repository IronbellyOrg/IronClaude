3851253a08fdc4892244403619b23ce7e7a12ffc
Review one task for spec compliance.

Task brief: T8 (plan .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/TASK-WF-designSpec-20261108-165559.md:111-120; AC ids T8.AC1.. in order of its Acceptance criteria bullets)
## Task 8: Test install and status, update claim.md, and make commit B

Depends on: Task 7

Create `tests/skills/test_issue_l2_install.py` with FR-102 and its forgery and publication subgroups (spec FR-024, FR-030..FR-045; this satisfies AC-5). In `tests/skills/test_issue_orca_worktree.py`, update `test_ir6_l2_status_follows_the_git_hook_path` (about `:1686-1730`), the remedy assertion near `:1728` (OC-6), the `present-unverified` claim.md assertion near `:1672` (OC-4) and the `W-L2-ABSENT` text assertions (FR-105). Update the `:127` remedy row and `:129` paragraph of `src/superclaude/skills/sc-issue-protocol/refs/claim.md` (OC-4 moves this edit into B). Switch the hook placement in `tests/hooks/test_launch_level_pre_push.py` from the test-local copy to `install_l2`. Run `make sync-dev` and `make verify-sync`, stage only these paths plus `.dev/tasks`, and make local commit B with a `feat(issue): ...` subject; the body records the OC-2, OC-4, OC-6, OC-8, OC-9, OC-10 and OC-12 resolutions and the `core.hooksPath` behaviour change for owner review.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_l2_install.py tests/skills/test_issue_orca_worktree.py tests/skills/test_issue_protocol.py tests/hooks/test_launch_level_pre_push.py` passes; `tests/skills/test_issue_protocol.py` is unchanged and still lists `W-L2-ABSENT`.
- `grep -rn present-unverified src tests` prints nothing (AC-6).
- `make verify-sync` passes and commit B lists no `.claude/` path.
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
Start sha: 3851253a08fdc4892244403619b23ce7e7a12ffc
Diff against the start snapshot: run `git -C /home/coder/workspaces/worktrees/IronClaude/issue-441 diff 3851253a08fdc4892244403619b23ce7e7a12ffc -- src/superclaude/skills/sc-issue-protocol/refs/claim.md src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py tests/hooks/test_launch_level_pre_push.py tests/skills/test_issue_l2_install.py tests/skills/test_issue_orca_worktree.py` (tree-ish vs worktree), and read in full every path of [src/superclaude/skills/sc-issue-protocol/refs/claim.md src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py tests/hooks/test_launch_level_pre_push.py tests/skills/test_issue_l2_install.py tests/skills/test_issue_orca_worktree.py] that `git -C /home/coder/workspaces/worktrees/IronClaude/issue-441 status --porcelain --untracked-files=all -- src/superclaude/skills/sc-issue-protocol/refs/claim.md src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py tests/hooks/test_launch_level_pre_push.py tests/skills/test_issue_l2_install.py tests/skills/test_issue_orca_worktree.py` shows as `??` and that is absent from `git -C /home/coder/workspaces/worktrees/IronClaude/issue-441 ls-tree -r --name-only 3851253a08fdc4892244403619b23ce7e7a12ffc`. Live files are under /home/coder/workspaces/worktrees/IronClaude/issue-441.
Delta diff from the previous reviewed tree (empty on the first review): run `git -C /home/coder/workspaces/worktrees/IronClaude/issue-441 diff e266d9a570342bd247a67ae51abd707bb10815be 6aea054c993f18d439fbc9b04b9e4463212af62f -- src/superclaude/skills/sc-issue-protocol/refs/claim.md src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py tests/hooks/test_launch_level_pre_push.py tests/skills/test_issue_l2_install.py tests/skills/test_issue_orca_worktree.py`. Commit B (HEAD, 1090b609) was amended in the repair; its body is `git -C /home/coder/workspaces/worktrees/IronClaude/issue-441 log -1 --format=%B HEAD`.
Earlier blocking findings of this start (empty on the first review): 
F2.1 sev=blocking trigger=B4 ac=scope at=tests/skills/test_issue_l2_install.py:241 anchor="A test that needs a second uid (U-7) is `skipif` with a reason when none is available." chk=n,n,n,y family=missing-test-case fix=add the FR-102 forgery cases "wrong uid" (hook and data file owned by another uid, `skipif` with a reason when no second uid is available, per source U-7) and "wrong mode" (a byte-identical hook at e.g. 0o775/0o777 with a valid data file); if the code is meant to keep D-3's definition, record that divergence in commit B's body first=A1 origin=late: the FR-102 forgery subgroup (merged-requirements.md:338) lists "wrong uid or mode" as a case that must not read `owned`, and source U-7 (source.md:750) says the foreign-owner forgery tests are `skipif` with a reason when no second uid exists. The file had neither, and `_l2_entry_verdict` had no uid or mode check on the hook entry.
Saved-probe re-check hit locations (may be empty): `grep -n -E 'st_uid|0o022|geteuid' src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py tests/skills/test_issue_l2_install.py` (probe ./artifacts/retries/T8/probe-2-1.md) now hits orca_worktree.py:1184-1185 (data file), :1217 and :1219 (new hook-entry uid and mode checks), :1338 (hooks dir); test_issue_l2_install.py:253 (root skipif), :274-275 (faked geteuid on _l2_entry_verdict), :344-346 (hooks-dir test).

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
