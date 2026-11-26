0485473088722c7e639a7cdf36aa2060cef168ac
Review one task for spec compliance.

Task brief: Task T7 "Update the four plugin mirrors and the generated development copies". Depends on Task 1 and Task 6. Copy the final canonical files to their existing plugin mirrors byte for byte: `src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py` to `plugins/superclaude/skills/sc-workflow-protocol/scripts/remediate.py`; `src/superclaude/skills/sc-workflow-protocol/SKILL.md` to `plugins/superclaude/skills/sc-workflow-protocol/SKILL.md`; `src/superclaude/skills/sc-workflow-protocol/refs/remediation.md` to `plugins/superclaude/skills/sc-workflow-protocol/refs/remediation.md`; and `src/superclaude/commands/workflow.md` to `plugins/superclaude/commands/workflow.md`. Then run `make sync-dev` so the generated `.claude/` copies match, and do not stage the generated `.claude/` content. There is no plugin mirror of `remediation-handoff.md`; do not invent one.
AC ids:
- T7.AC1: `cmp` reports no difference for each of the four source and mirror pairs.
- T7.AC2: `make verify-sync` is clean, and `git status --short` shows no change under `.claude/` (generated copies are gitignored).
- T7.AC3: With the dev extra installed (`uv sync --extra dev`, ruff pinned in `pyproject.toml`), `uv run pytest tests/skills -q`, `make lint` and `uv run ruff format --check` on `src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py` and `tests/skills/test_workflow_remediation.py` all pass.
- T7.AC4: `git status --short` is printed and lists only the planned source, test, README and mirror files.
Global constraints:
- Base every change on `integration`, not the issue's stale `master`. Edit canonical files under `src/superclaude/`, `tests/` and `.dev/README.md`, plus the four existing plugin mirrors named in Task 7. Never edit or stage anything under `.claude/` except through `make sync-dev`, and never stage generated `.claude/` content.
- No new metadata writer, none or forced flag field, placement guard, dependency, contract version, agent or reflection mirror. `place` keeps its existing refusal (the `E-REMEDIATE-SOURCE` check before any write).
- Keep the pull request 705 safeguards untouched.
- Keep the already-resolved findings intact: the `archive-undo.txt` conflict refusal, non-overwriting moves and rollback tests in `tests/skills/test_workflow_remediation.py`.
- Do not modify, move or archive any live task package to reproduce the defect, and leave `docs/designs/surgical-remediation.md` unchanged.
- Make no commit, push or pull request as part of this plan.
Start sha: 0485473088722c7e639a7cdf36aa2060cef168ac
Diff against the start snapshot: Touched files since the start snapshot: `plugins/superclaude/skills/sc-workflow-protocol/scripts/remediate.py` (modified: byte copy of the source script; the other three mirrors were already copied during Task 6 and are unchanged since this task started), and the evidence log `.dev/tasks/to-do/TASK-WF-issueSummary-20261126-161245/artifacts/t7-check.log` (new). Log lines: 2-5 `cmp` result for the four pairs; 7-8 `uv sync --extra dev` installed `ruff==0.15.20`; 9-11 `make sync-dev`; 13-15 `make verify-sync` ("All components in sync."); 17-19 `make lint` ("All checks passed!"); 21 the ruff format check ("2 files already formatted"); 22-26 the `tests/skills` run ("2431 passed, 2 skipped"); 27-40 the `git status --short` listing. Run `git diff 0485473088722c7e639a7cdf36aa2060cef168ac --stat` for the diff. Check byte equality of the four pairs and the git status yourself with Read/Grep/Glob where you can.
Codegraph context: index_state: fresh; checked_at: 2026-11-26T17:51:38Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-703; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-703. Call codegraph only when index_state: fresh, never to widen scope. Q2b: file copies only; no symbol changed in this task.
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
