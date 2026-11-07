be9c4760758d45905f8e54a9da8099fd55ec11ae
Review one task for spec compliance.

Task brief: ## Task 3: Add the --pipeline and --submit flags to the /sc:issue command file

Edit `src/superclaude/commands/issue.md` and `tests/commands/test_issue_command.py`. Source: design section 4 and section 11 (new STOPs).

In `src/superclaude/commands/issue.md`: add `version: "1.1.0"` to the frontmatter; extend `argument-hint`, the Usage block, the Options table (rows `--pipeline`: mode claim, default `worktree`, values `worktree`, `full`, `none`; `--submit`: mode claim, default off, no value), Examples (`--claim 302`, `--claim 302 --pipeline none`, `--claim 302 --pipeline full`, `--claim 302 --pipeline full --submit`) and the Outputs table (claim also produces `launch-prompt.md` and `worktree.json`). Rewrite the claim bullet and the Will list so a claim now also creates or reuses the worktree and launches one agent at the chosen level and never merges. In Will Not replace "Run any next-step command (brainstorm, design, workflow, implement, troubleshoot)" with "Run `/sc:implement`, `/task`, a commit, a push or `/sc:pr-submit` itself (the launched agent may, at the level the user chose)" and add "Pass an Orca link flag" and "Merge anything".

Add three STOP rules after the existing ones and before Activation, in this order: `--pipeline` or `--submit` with `--create` is STOP `E-CLAIM-ONLY-FLAG` ("--pipeline and --submit apply to --claim only"); a `--pipeline` value that is not `worktree`, `full` or `none` (or `--pipeline` with no value) is STOP listing the three values; `--submit` with a value, or without `--pipeline full`, is STOP `E-SUBMIT-NEEDS-FULL` ("--submit needs --pipeline full"). `E-CREATE-ONLY-FLAG` for `--depth`, `--mode`, `--type` with `--claim` stays the first rule. Update `tests/commands/test_issue_command.py`: the Options-table test lists exactly seven flags with the new values and defaults; the STOP-rule test requires the new codes before `## Activation`; add a check that Will Not names `/sc:implement`, `/task`, a commit, a push and `/sc:pr-submit` and no longer contains "Run any next-step command"; check `version: "1.1.0"`.

Acceptance criteria:
- `uv run pytest tests/commands/test_issue_command.py` passes, covering pins ST-1, ST-2 and ST-3 of design section 13.
- `grep -n "src/superclaude" src/superclaude/commands/issue.md` finds nothing.

Design section 18 of docs/designs/sc-issue-claim-pipeline-flag.md (amendments from the plan review) wins where it disagrees with this task text; judge only the acceptance criteria of this task (AC ids T3.AC1, T3.AC2, ... in the order of the 'Acceptance criteria:' bullets).
Global constraints: - Edit canonical sources under `src/superclaude/` only, then run `make sync-dev`. Never stage anything under `.claude/` (only `.claude/settings.json` is tracked). `.dev/tasks` is staged with `git add .dev/tasks`; staging is not committing.
- Python through UV only: `uv run pytest`, `uv run --no-project python <script>`. No `python -m`, no bare `pip`.
- No test calls a real `orca`, `gh`, the network or a real agent. A fake `orca` executable and a throwaway git repository are put first on `PATH`; `HOME` is a temporary directory in every test that writes the launch store.
- GitHub target is `IronbellyOrg/IronClaude` only; no Orca link flag (`--issue`, `--pr`, `--reference*`, `--linear-issue`, `--gitlab-*`) anywhere. `--agent`, `--prompt`, `--surface` appear only in the `orca agent launch` call.
- Do not build the enforcement hook of issue 394 (no `launch-level-guard.sh`, no `pre-push` hook, no hooks.json change). Only the launch record it reads is written.
- No `src/superclaude/` path inside any installed primitive (command, skill, ref, template). The skill calls the script as `<skill base>/scripts/orca_worktree.py`.
- No new ref file in `src/superclaude/skills/sc-issue-protocol/refs/` (the five-refs test stays true).
- Design: `docs/designs/sc-issue-claim-pipeline-flag.md` (this plan's source, section numbers below refer to it). Requirements: the folder `.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/` (`merged-requirements.md` as amended by `launch-levels-addendum.md`), already copied into this repository and part of the change.
Start sha: be9c4760758d45905f8e54a9da8099fd55ec11ae
Diff against the start snapshot: the unified diff (start snapshot to current tree, touched files only, untracked files in full) is in the file /home/coder/workspaces/worktrees/IronClaude/sc-issue-claim-pipeline-flag/.dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/artifacts/diffs/T3-r1-1.patch (read it in full); the live files are in the repository for anchor checks
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
