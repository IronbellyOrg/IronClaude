d7997c8df7f1c257d366942ecabcbc9cd41c0aac
Review one task for spec compliance.

Task brief: ## Task 5: Add the launch prompt template and the prompt subcommand

Depends on: Task 1

Create `src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md` and add the `prompt` subcommand to `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`; extend `tests/skills/test_issue_orca_worktree.py` and `tests/skills/test_issue_protocol.py`. Source: design sections 8.2 and 9.

The template has exactly four blocks, each opened by an HTML-comment marker line of the form `block:<name>` wrapped as shown in design section 9 (names `common`, `worktree`, `full`, `submit`), with the required statements of the design section 9 table: common (read `issue-summary.md` and `next-steps.md`; run each step by invoking its command through the Skill tool in this session, never by reading a command file and never inside a subagent; report a model-tier mismatch with the tier named in `next-steps.md`; never merge, never push to `master` or `main`); worktree (follow the steps up to the `Plan boundary` line; do not run `/sc:implement`, `/task`, `git commit`, `git push` or `/sc:pr-submit`; print the plan path and `Waiting for approval`, then wait; after a human replies `approved` or runs the printed implement command, run the remaining steps, still without commit, push or `/sc:pr-submit`); full (run every step through the last, leave changes in the working tree, stage nothing, finish by printing `git status --short`); submit (the owner asked for the commit and push by passing `--submit`; check that no PR is already open or merged for the branch; commit with a conventional-commit message staging `.dev/tasks` and the changed files, never `.claude/` and never `.dev/issues/`; push the current feature branch to `origin`, never `master`; run `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."`; never merge).

`prompt --template <path> --level worktree|full [--submit] --number <N> --out <file>` keeps `common` plus the level block (plus `submit` with `--submit`), drops every other block and all marker lines, replaces `<N>`, writes `--out` and prints `{"status": "written", "path": "<out>"}`. `--submit` with `--level worktree` exits 2.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_orca_worktree.py -k prompt` passes with PR-1 to PR-4 (levels keep only their own block, `--submit` adds the submit block, `--submit` with `worktree` exits 2, the rendered `full` output and the `common` block hold none of `/sc:pr-submit`, `git push`, `git commit`, `--monitor`).
- `tests/skills/test_issue_protocol.py` has ST-8: the template has exactly the four blocks, only the `submit` block contains `/sc:pr-submit --monitor 3`, `git push` and the commit instruction, and only the `worktree` block also contains those tokens (as a prohibition).
- The rendered `worktree` output contains the line telling the agent not to run `/sc:implement`, `/task`, `git commit`, `git push` or `/sc:pr-submit`.

Design section 18 of docs/designs/sc-issue-claim-pipeline-flag.md (amendments from the plan review) wins where it disagrees with this task text; judge only the acceptance criteria of this task (AC ids T5.AC1, T5.AC2, ... in the order of the 'Acceptance criteria:' bullets).
Global constraints: - Edit canonical sources under `src/superclaude/` only, then run `make sync-dev`. Never stage anything under `.claude/` (only `.claude/settings.json` is tracked). `.dev/tasks` is staged with `git add .dev/tasks`; staging is not committing.
- Python through UV only: `uv run pytest`, `uv run --no-project python <script>`. No `python -m`, no bare `pip`.
- No test calls a real `orca`, `gh`, the network or a real agent. A fake `orca` executable and a throwaway git repository are put first on `PATH`; `HOME` is a temporary directory in every test that writes the launch store.
- GitHub target is `IronbellyOrg/IronClaude` only; no Orca link flag (`--issue`, `--pr`, `--reference*`, `--linear-issue`, `--gitlab-*`) anywhere. `--agent`, `--prompt`, `--surface` appear only in the `orca agent launch` call.
- Do not build the enforcement hook of issue 394 (no `launch-level-guard.sh`, no `pre-push` hook, no hooks.json change). Only the launch record it reads is written.
- No `src/superclaude/` path inside any installed primitive (command, skill, ref, template). The skill calls the script as `<skill base>/scripts/orca_worktree.py`.
- No new ref file in `src/superclaude/skills/sc-issue-protocol/refs/` (the five-refs test stays true).
- Design: `docs/designs/sc-issue-claim-pipeline-flag.md` (this plan's source, section numbers below refer to it). Requirements: the folder `.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/` (`merged-requirements.md` as amended by `launch-levels-addendum.md`), already copied into this repository and part of the change.
Start sha: d7997c8df7f1c257d366942ecabcbc9cd41c0aac
Diff against the start snapshot: the unified diff (start snapshot to current tree, touched files only, untracked files in full) is in the file /home/coder/workspaces/worktrees/IronClaude/sc-issue-claim-pipeline-flag/.dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/artifacts/diffs/T5-r1-1.patch (read it in full); the live files are in the repository for anchor checks
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
