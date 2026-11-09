acb70ba1d033199da22be7d9eeeffabeac8d5799
Review one task for spec compliance.

Task brief: T12 (plan .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/TASK-WF-designSpec-20261108-165559.md:157-168; AC ids T12.AC1.. in order of its Acceptance criteria bullets)
## Phase 7: IR-7 refusal path, switched off

## Task 12: Build the IR-7 refusal path OFF and make the separate commit E

Depends on: Task 11

In `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`, add `IR7_REFUSE = False`, `remedy()`, the two `launch_result` lookups and the IR-7 line in `cmd_launch` that replaces the comment near `:1307-1310` (source §5.3, §6.3 `remedy`, §3.2 step 7, §8.1 row 23; spec FR-060..FR-064). Add FR-103 to `tests/skills/test_issue_l2_install.py` in both switch positions (the `True` position by patching the constant inside the test) plus a source assertion that `IR7_REFUSE is False`. Run `make sync-dev` and `make verify-sync`, then make local commit E, last and separate, with the subject `feat(issue): add the IR-7 W-L2-ABSENT refusal path, switched off`; its body states that E changes no behaviour while `IR7_REFUSE` is `False` and lists the FR-065 turn-on preconditions (owner-recorded PASS for #442 OB-H1 item 1, OB-H2 and OB-H3 including the real-claim disposable-bare-remote check; owner approval; the docs moved from warning to refusal in the same commit; an upgrade path for stale hooks or the owner's acceptance of the re-claim cost).

Acceptance criteria:
- With `IR7_REFUSE = False`, a launch with L2 absent proceeds and prints the `W-L2-ABSENT` warning; with the constant patched to `True` in the test, the same launch is refused (AC-8).
- `uv run pytest tests/hooks/test_launch_level_pre_push.py tests/hooks/test_launch_level_pre_push_records.py tests/hooks/test_launch_level_guard_l2_tokens.py tests/skills/test_issue_l2_install.py tests/skills/test_issue_orca_worktree.py tests/skills/test_issue_protocol.py tests/cli/test_install_hooks.py tests/hooks/test_launch_job_identity.py` passes (AC-10), with output saved to `./artifacts/t12-ac10.log`.
- `git log --oneline -5` shows commits A, B, C, D, E in that order with E on top, `git diff HEAD~5 --stat -- tests/hooks/test_launch_level_guard.py` is empty, and nothing has been pushed.
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
Start sha: acb70ba1d033199da22be7d9eeeffabeac8d5799
Diff against the start snapshot: run `git -C /home/coder/workspaces/worktrees/IronClaude/issue-441 diff acb70ba1d033199da22be7d9eeeffabeac8d5799 -- src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py tests/skills/test_issue_l2_install.py .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/spec-deviations.md .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t12-ac10.log` (tree-ish vs worktree), and read in full every path of [src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py tests/skills/test_issue_l2_install.py .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/spec-deviations.md .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t12-ac10.log] that `git -C /home/coder/workspaces/worktrees/IronClaude/issue-441 status --porcelain --untracked-files=all -- src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py tests/skills/test_issue_l2_install.py .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/spec-deviations.md .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t12-ac10.log` shows as `??` and that is absent from `git -C /home/coder/workspaces/worktrees/IronClaude/issue-441 ls-tree -r --name-only acb70ba1d033199da22be7d9eeeffabeac8d5799`. Live files are under /home/coder/workspaces/worktrees/IronClaude/issue-441.
Delta diff from the previous reviewed tree (empty on the first review): run git diff refs/superclaude/implement/TASK-WF-designSpec-20261108-165559/retry/T12/r1-1 refs/superclaude/implement/TASK-WF-designSpec-20261108-165559/retry/T12/r1-2 -- src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py tests/skills/test_issue_l2_install.py .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/spec-deviations.md .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t12-ac10.log
Earlier blocking findings of this start (empty on the first review): F12.1 ac=scope at=tests/skills/test_issue_l2_install.py:606 anchor="Add FR-103 to `tests/skills/test_issue_l2_install.py` in both switch positions" chk=n,n,n,y family=incomplete-ir7-regression-coverage sev=blocking first=A1 origin=new fix=Add a monkeypatched-True test with an owned hook that asserts launched and no W-L2-ABSENT: The task explicitly requires FR-103, which includes the True/owned success case. The new parameterized test always establishes an absent hook, and searching the tests for IR7_REFUSE found no owned-hook test with the switch enabled. The required case is specified at .dev/brainstorms/20261108-094705-l2-pre-push-guard/merged-requirements.md:340.
F12.2 ac=T12.AC3 at=.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/spec-deviations.md:28 anchor="`git log --oneline -5` shows commits A, B, C, D, E in that order with E on top" chk=y,n,n,n family=history-ac-mismatch sev=blocking first=A1 origin=new fix=Obtain an explicit acceptance-criterion amendment for the owner-required six-commit sequence rather than deleting or rewriting the stat-fix commit: The actual top five commits are E, D, C, stat fix, B. The deviation records a sensible replacement check, but the live acceptance criterion still requires the five-entry sequence at .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/TASK-WF-designSpec-20261108-165559.md:168.
Saved-probe re-check hit locations (may be empty): tests/skills/test_issue_l2_install.py:594,605,616,639,640; src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:53,810,813,821,822,1374,1412,1696,1699,1701; .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/spec-deviations.md:25,27,28,29,30; .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/TASK-WF-designSpec-20261108-165559.md:168

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
