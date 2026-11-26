dcae47b2859470105c45d17ceb241301e8a4e45a
Review one task for spec compliance.

Task brief: Task T5 "Describe all three routing thresholds in the package-layout README". In `.dev/README.md`, replace the two bullets "Surgical route" and "Regenerate route" (they route by blocker count alone) with text that matches the ordered rule in `src/superclaude/skills/sc-workflow-protocol/refs/remediation.md` section 1: zero blockers takes the none route first, whatever the HIGH and Medium counts; otherwise surgical requires blockers at most 3 and HIGH-labelled findings at most 5 and Medium findings at most 9 together; otherwise regenerate (at most once per run). Keep the copy-then-archive-then-place description, the 2 fix cycle cap and a pointer to that ref as the authority.
AC ids:
- T5.AC1: The README states all three thresholds (3, 5, 9), the zero-blocker rule and the regenerate fallback, and names the ref as the authoritative source.
- T5.AC2: The numbers agree with `route()` in `src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py` and the parametrized `test_route` cases in `tests/skills/test_workflow_remediation.py`.
Global constraints:
- Base every change on `integration`, not the issue's stale `master`. Edit canonical files under `src/superclaude/`, `tests/` and `.dev/README.md`, plus the four existing plugin mirrors named in Task 7. Never edit or stage anything under `.claude/` except through `make sync-dev`, and never stage generated `.claude/` content.
- No new metadata writer, none or forced flag field, placement guard, dependency, contract version, agent or reflection mirror. `place` keeps its existing refusal (the `E-REMEDIATE-SOURCE` check before any write).
- Keep the pull request 705 safeguards untouched.
- Keep the already-resolved findings intact: the `archive-undo.txt` conflict refusal, non-overwriting moves and rollback tests in `tests/skills/test_workflow_remediation.py`.
- Do not modify, move or archive any live task package to reproduce the defect, and leave `docs/designs/surgical-remediation.md` unchanged.
- Make no commit, push or pull request as part of this plan.
Start sha: dcae47b2859470105c45d17ceb241301e8a4e45a
Diff against the start snapshot: Touched files: `.dev/README.md` (modified: lines 63 and 64, the "Surgical route" and "Regenerate route" bullets, are replaced) and `.dev/tasks/to-do/TASK-WF-issueSummary-20261126-161245/artifacts/t5-check.log` (new evidence log: lines 1-2 list the two README bullets, lines 19-23 are the output of `remediate.py route` for the counts B/H/M = 0/9/20, 3/5/9, 4/0/0, 1/6/0 and 1/0/10, in that order). Run `git diff dcae47b2859470105c45d17ceb241301e8a4e45a -- .dev/README.md` to see the diff.
Codegraph context: index_state: fresh; checked_at: 2026-11-26T17:51:38Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-703; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-703. Call codegraph only when index_state: fresh, never to widen scope. Q2b: Markdown documentation only; no code symbol changed.
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
