873c4222069ec08167ef4153612220811f9fc9db
Review one task for spec compliance.

Task brief: T4 (plan .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/TASK-WF-designSpec-20261108-165559.md:67-76; AC ids T4.AC1.. in order of its Acceptance criteria bullets)
## Task 4: Write the hook test matrix

Depends on: Task 3

Create `tests/hooks/test_launch_level_pre_push.py` as the spec FR-100 hook test matrix, covering T-01..T-24, T-16a/b/c, T-STALE-1 and the FR-101 leak pins, using the fixture rules in source §10.1 (real git with `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM` set to `/dev/null`, a temporary HOME, `git worktree add` in tmp, remote `for-each-ref` checked before and after every push, a governed actor from the selector's `prepare`/`run` with a fake store, modelled on `LocalPushFixture` in `tests/hooks/test_launch_job_identity.py:1175-1283` but defined in the new file). Until Task 8, place the hook with a direct test-local copy (source §8.2). Map each test to its requirement as in source §10.2 and §10.4 (AC-1..AC-4, AC-7).

Acceptance criteria:
- A governed push to `refs/heads/main` and to `refs/heads/master` is refused and the remote refs are unchanged; the same pushes by a human succeed (AC-1, AC-2).
- An unknown identity is refused only for main and master and allowed for any other branch, with the FR-008 diagnostic (AC-3, OD-2).
- `uv run pytest tests/hooks/test_launch_level_pre_push.py` passes; tests needing a second uid are `skipif` with a stated reason when none exists.
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
Start sha: 873c4222069ec08167ef4153612220811f9fc9db
Diff against the start snapshot: run `git -C /home/coder/workspaces/worktrees/IronClaude/issue-441 diff 873c4222069ec08167ef4153612220811f9fc9db -- tests/hooks/test_launch_level_pre_push.py .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t4-matrix-map.md` (tree-ish vs worktree), and read in full every path of [tests/hooks/test_launch_level_pre_push.py .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t4-matrix-map.md] that `git -C /home/coder/workspaces/worktrees/IronClaude/issue-441 status --porcelain --untracked-files=all -- tests/hooks/test_launch_level_pre_push.py .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t4-matrix-map.md` shows as `??` and that is absent from `git -C /home/coder/workspaces/worktrees/IronClaude/issue-441 ls-tree -r --name-only 873c4222069ec08167ef4153612220811f9fc9db`. Live files are under /home/coder/workspaces/worktrees/IronClaude/issue-441.
Delta diff from the previous reviewed tree (empty on the first review): run `git -C /home/coder/workspaces/worktrees/IronClaude/issue-441 diff ef0e24d5e2cac621a59bff4caace1d133fe26096 -- tests/hooks/test_launch_level_pre_push.py .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t4-matrix-map.md` (previous reviewed tree r1-1 vs worktree)
Earlier blocking findings of this start (empty on the first review): F1.1 ac=scope at=tests/hooks/test_launch_level_pre_push.py:659 anchor=tests/hooks/test_launch_level_pre_push.py:659 chk=n,y,n,n family=second-uid-test fix=Add `-c safe.directory=*` (or `GIT_CONFIG_COUNT`/`safe.directory` in the env) to the setpriv git call, give uid 65534 a planted or real foreign record, and assert the `job record foreign|unreadable` why rather than bare `L2-UNKNOWN`: `test_t16c_real_second_uid` cannot pass when its skip condition is false. It runs `git -C <root-owned clone> push` as uid 65534 with `GIT_CONFIG_GLOBAL=/dev/null` (:93) and no `safe.directory`; git 2.47.3 (installed) stops with "detected dubious ownership" (exit 128) before any hook runs, so `"L2-UNKNOWN" in result.stderr` (:663) fails. The map row (t4-matrix-map.md:28) presents it as the real-second-uid T-16c test. It only ever skips in this environment, so the reported pass count is unaffected.
F2.1 ac=scope at=tests/hooks/test_launch_level_pre_push.py:657 anchor=tests/hooks/test_launch_level_pre_push.py:657 chk=n,n,y,n family=second-uid-test-chmod fix=Copy the repo into a fresh world-readable directory under the test's own tmp_path, or stop at tmp_path, instead of chmodding its parents: the loop at :654-657 adds group/other read+execute to every parent of the test's tmp dir up to `/tmp`, i.e. pytest's shared base temp dirs (`/tmp/pytest-of-<user>`, normally 0700), which are outside the test's declared outputs and expose other tests' temp data to other users. It runs only as root with setpriv present (skipped here).
Saved-probe re-check hit locations (may be empty): probe .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/retries/T4/probe-1-1.md re-run: second-uid-test hits tests/hooks/test_launch_level_pre_push.py:649,650,663,669 and t4-matrix-map.md:28; second-uid-test-chmod hits (640-690) :657,:659,:662,:667

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
