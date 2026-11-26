a3e873ab03e3279e8dd71dbcb6a22f79d802215d
Review one task for spec compliance.

Task brief: Task 5 of the plan /home/coder/workspaces/worktrees/IronClaude/run-ledger/.dev/tasks/to-do/TASK-WF-remediationSourc-20261126-181052/TASK-WF-remediationSourc-20261126-181052.md (read lines 68-76 of that plan for the full Task 5 text and AC). Summary: in src/superclaude/cli/sweep/models.py add `run_source: str | None = None` as the last field of the frozen dataclass SweepContext, and in src/superclaude/cli/sweep/report.py make _header append `sanitize(ctx.run_source)` as one more header line when it is not None. Callers that must keep working unchanged: the one SweepContext(...) construction in each of src/superclaude/cli/sweep/commands.py, tests/sweep/test_classify.py, tests/sweep/test_probes_allowlist.py, tests/sweep/test_readonly.py and tests/sweep/test_report.py. Add two tests to tests/sweep/test_report.py: test_header_has_no_run_source_line_by_default and test_header_prints_run_source_line_when_set.
Acceptance criteria:
T5.AC1: `uv run pytest tests/sweep -v` passes, including both new tests; no existing golden or snapshot in tests/sweep/ changes.
T5.AC2: A report built with run_source=None is byte-identical to the report before this change.
Global constraints: UV only. Not allowed: orca orchestration reset, deleting a Run, Orca link flags, editing ~/.claude/settings.json, installing a crontab, scheduling, adding the hook to hooks.json, committing, pushing, PRs, GitHub writes. src/superclaude/cli/main.py is not edited. src/superclaude/cli/sweep/probes.py ALLOWED_ORCA is unchanged. Behaviour decisions are fixed by the source: no new sweep flag.
Start sha: a3e873ab03e3279e8dd71dbcb6a22f79d802215d
Diff against the start snapshot: run `git diff a3e873ab03e3279e8dd71dbcb6a22f79d802215d -- src/superclaude/cli/sweep/models.py src/superclaude/cli/sweep/report.py tests/sweep/test_report.py` from /home/coder/workspaces/worktrees/IronClaude/run-ledger (tracked files; the snapshot holds all earlier work). Run state of the code graph: index_state: fresh, checked_at: 2026-11-26T18:23:53Z, worktree_root: /home/coder/workspaces/worktrees/IronClaude/run-ledger, projectPath: /home/coder/workspaces/worktrees/IronClaude/run-ledger. call codegraph only when index_state: fresh, never to widen scope.
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
