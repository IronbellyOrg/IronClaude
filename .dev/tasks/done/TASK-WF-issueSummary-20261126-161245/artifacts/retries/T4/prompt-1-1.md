a0f2eb0653da8aa65f211ccf1a4ce2879d39b88b
Review one task for spec compliance.

Task brief: Task T4 "Say "on a copy" in the reflection handoff". In `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md` (the bullet that says Wave 4R "repairs blocking findings surgically in place"), change the wording so it says Wave 4R repairs blocking findings surgically on a copy and places the repaired plan as a new package, or regenerates the plan as a new package that supersedes the old one. Keep the rest of that bullet, including the ban on hand-editing a placed plan. This file has no plugin mirror; do not create one.
AC ids:
- T4.AC1: `grep -n "in place" src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md` no longer matches the Wave 4R sentence, and the sentence agrees with `src/superclaude/skills/sc-workflow-protocol/refs/remediation.md` section 2 (repair on a copy, archive the original, place a new package).
- T4.AC2: Tests that read this handoff file still pass: `uv run pytest tests/cli/reflect -q`.
Global constraints:
- Base every change on `integration`, not the issue's stale `master`. Edit canonical files under `src/superclaude/`, `tests/` and `.dev/README.md`, plus the four existing plugin mirrors named in Task 7. Never edit or stage anything under `.claude/` except through `make sync-dev`, and never stage generated `.claude/` content.
- No new metadata writer, none or forced flag field, placement guard, dependency, contract version, agent or reflection mirror. `place` keeps its existing refusal (the `E-REMEDIATE-SOURCE` check before any write).
- Keep the pull request 705 safeguards untouched.
- Keep the already-resolved findings intact: the `archive-undo.txt` conflict refusal, non-overwriting moves and rollback tests in `tests/skills/test_workflow_remediation.py`.
- Do not modify, move or archive any live task package to reproduce the defect, and leave `docs/designs/surgical-remediation.md` unchanged.
- Make no commit, push or pull request as part of this plan.
Start sha: a0f2eb0653da8aa65f211ccf1a4ce2879d39b88b
Diff against the start snapshot: Touched files: `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md` (modified: one phrase on line 81 changed from "repairs blocking findings surgically in place, or regenerates" to "repairs blocking findings surgically on a copy and places the repaired plan as a new package that supersedes the old one, or regenerates") and `.dev/tasks/to-do/TASK-WF-issueSummary-20261126-161245/artifacts/t4-check.log` (new evidence log: line 1-2 is the grep for "in place" with no match, line 3 the new sentence, line 6 the `tests/cli/reflect` result). Run `git diff a0f2eb0653da8aa65f211ccf1a4ce2879d39b88b -- src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md` to see the diff.
Codegraph context: index_state: fresh; checked_at: 2026-11-26T17:51:38Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-703; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-703. Call codegraph only when index_state: fresh, never to widen scope. Q2b: Markdown reference text only; no code symbol changed.
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
