c0a2a47c45e8d90de978e8a4f3e7978676c4a592
Review one task for spec compliance.

Task brief: T6 (plan .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/TASK-WF-designSpec-20261108-165559.md:90-98; AC ids T6.AC1.. in order of its Acceptance criteria bullets)
## Task 6: Add the L2 install helpers to orca_worktree.py

Depends on: Task 5

In `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`, add the source §6.3 symbols for install: an `env=` parameter on `run()` (about `:123-125`, which has none today), `clean_git_env`, `publish_no_replace`, `l2_data_expected`, `L2_VERSION_LINE` and `install_l2(wt)` following the internal flow S1..S4 and T4 in source §3.3 (spec FR-031..FR-039, NFR-006 supported git versions, NFR-011 concurrent installers converge on one identical pair). Take the data file's HOME from `home_dir()` (about `:874`, source §12 OC-8), after settling U-8 by reading the Orca launch path to see whether `cmd_launch` sets the agent's HOME; report an unsafe hooks directory and a git config read error as `unsupported` (OC-9, OC-10); report a differing data file as `conflict` without overwriting (OC-12). Settle U-1 from the git release notes and put the floor in the installer reason text; pick the self-test timeout under `DEFAULT_TIMEOUT` (about `:79`) and document it (U-14(c)); propose reason wording for the states in U-13.

Acceptance criteria:
- `install_l2` publishes the hook and data file without replacing any existing file, leaves `pre-commit` and sample hooks unchanged, leaves no private subdirectory behind, and returns one of the source §7.4 states with a reason.
- `uv run python -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` succeeds, and the U-1, U-8, U-13 and U-14(c) findings and choices are written in `./artifacts/t6-install-choices.md`.
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
Start sha: c0a2a47c45e8d90de978e8a4f3e7978676c4a592
Diff against the start snapshot: run `git -C /home/coder/workspaces/worktrees/IronClaude/issue-441 diff c0a2a47c45e8d90de978e8a4f3e7978676c4a592 -- src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t6-install-choices.md` (tree-ish vs worktree), and read in full every path of [src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t6-install-choices.md] that `git -C /home/coder/workspaces/worktrees/IronClaude/issue-441 status --porcelain --untracked-files=all -- src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t6-install-choices.md` shows as `??` and that is absent from `git -C /home/coder/workspaces/worktrees/IronClaude/issue-441 ls-tree -r --name-only c0a2a47c45e8d90de978e8a4f3e7978676c4a592`. Live files are under /home/coder/workspaces/worktrees/IronClaude/issue-441.
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
