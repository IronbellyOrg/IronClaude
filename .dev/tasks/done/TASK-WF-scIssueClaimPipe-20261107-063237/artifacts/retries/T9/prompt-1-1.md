b26ebf510b511fde9bcb03f6f2a03e8da16d6272
Review one task for spec compliance.

Task brief: ## Task 9: Update the user guide and routing guide, then sync

Depends on: Task 7

Edit `docs/user-guide/commands.md` (the `/sc:issue` section starting at its `### /sc:issue` heading and its table row), `src/superclaude/core/HOW-WE-WORK.md` (the `/sc:issue` row of the "Other commands" table) and copy that file byte-for-byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. Source: design sections 1, 4 and 12.

In the user guide: update the usage lines, add the two flags with the four levels (`worktree` default stops at an approved plan, `full` implements without commit or push, `full` with `--submit` commits, pushes a feature branch and opens a PR through `/sc:pr-submit --monitor 3`, `none` creates the worktree and launches no agent), state that no level merges and that Orca is required (`E-ORCA-REQUIRED`), and add examples. In the routing row replace "then stops without running them" with a statement that a claim also creates a worktree and launches an agent at the chosen level and never merges. Then run `make sync-dev`.

Acceptance criteria:
- `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` reports no difference, and `uv run pytest tests/core tests/commands tests/skills tests/recommend tests/cli/test_issue_body_templates.py -q` passes.
- `make sync-dev` completes and `make verify-sync` passes; `git status --short` shows no path under `.claude/` staged.
- `make lint` passes and `uv run ruff format --check src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py tests/skills/test_issue_orca_worktree.py` passes with the ruff version the repository pins.
- `grep -rn 'src/superclaude' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core src/superclaude/hooks` shows no hit introduced by this change.

Design section 18 of docs/designs/sc-issue-claim-pipeline-flag.md (amendments from the plan review) wins where it disagrees with this task text; judge only the acceptance criteria of this task (AC ids T9.AC1, T9.AC2, ... in the order of the 'Acceptance criteria:' bullets).
Global constraints: - Edit canonical sources under `src/superclaude/` only, then run `make sync-dev`. Never stage anything under `.claude/` (only `.claude/settings.json` is tracked). `.dev/tasks` is staged with `git add .dev/tasks`; staging is not committing.
- Python through UV only: `uv run pytest`, `uv run --no-project python <script>`. No `python -m`, no bare `pip`.
- No test calls a real `orca`, `gh`, the network or a real agent. A fake `orca` executable and a throwaway git repository are put first on `PATH`; `HOME` is a temporary directory in every test that writes the launch store.
- GitHub target is `IronbellyOrg/IronClaude` only; no Orca link flag (`--issue`, `--pr`, `--reference*`, `--linear-issue`, `--gitlab-*`) anywhere. `--agent`, `--prompt`, `--surface` appear only in the `orca agent launch` call.
- Do not build the enforcement hook of issue 394 (no `launch-level-guard.sh`, no `pre-push` hook, no hooks.json change). Only the launch record it reads is written.
- No `src/superclaude/` path inside any installed primitive (command, skill, ref, template). The skill calls the script as `<skill base>/scripts/orca_worktree.py`.
- No new ref file in `src/superclaude/skills/sc-issue-protocol/refs/` (the five-refs test stays true).
- Design: `docs/designs/sc-issue-claim-pipeline-flag.md` (this plan's source, section numbers below refer to it). Requirements: the folder `.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/` (`merged-requirements.md` as amended by `launch-levels-addendum.md`), already copied into this repository and part of the change.
Start sha: b26ebf510b511fde9bcb03f6f2a03e8da16d6272
Diff against the start snapshot: the unified diff (start snapshot to current tree, touched files only, untracked files in full) is in the file /home/coder/workspaces/worktrees/IronClaude/sc-issue-claim-pipeline-flag/.dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/artifacts/diffs/T9-r1-1.patch (read it in full); the live files are in the repository for anchor checks
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
