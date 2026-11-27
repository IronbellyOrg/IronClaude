7e2975a8ec824b14a861476610a250af9ec53522
Review one task for spec compliance.

Task brief: Task T3 "Add the direct place-before-archive test". In `tests/skills/test_workflow_remediation.py`, next to `test_place_fails_when_leaf_missing_or_not_empty`, add a test that builds a package with `make_pkg`, calls `rm.reserve` and `repaired_copy`, and then calls `rm.place` without calling `rm.archive`. The existing guard in `place` (`E-REMEDIATE-SOURCE`, "must be archived before place") is already in the code, so this test protects current behavior and is expected to pass on the unchanged baseline.
AC ids:
- T3.AC1: `rm.place` raises `rm.RemediateError` with `code == "E-REMEDIATE-SOURCE"`.
- T3.AC2: After the refusal the old package is still in `.dev/tasks/to-do/<OLD>` with its plan and contract unchanged (compare against `sha` of the plan and the original contract text), nothing exists under `.dev/tasks/archive/`, and the reserved leaf is still empty.
- T3.AC3: No change to `place` in `src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py` is made for this task.
Global constraints:
- Base every change on `integration`, not the issue's stale `master`. Edit canonical files under `src/superclaude/`, `tests/` and `.dev/README.md`, plus the four existing plugin mirrors named in Task 7. Never edit or stage anything under `.claude/` except through `make sync-dev`, and never stage generated `.claude/` content.
- No new metadata writer, none or forced flag field, placement guard, dependency, contract version, agent or reflection mirror. `place` keeps its existing refusal (the `E-REMEDIATE-SOURCE` check before any write).
- Keep the pull request 705 safeguards untouched.
- Keep the already-resolved findings intact: the `archive-undo.txt` conflict refusal, non-overwriting moves and rollback tests in `tests/skills/test_workflow_remediation.py`.
- Do not modify, move or archive any live task package to reproduce the defect, and leave `docs/designs/surgical-remediation.md` unchanged.
- Make no commit, push or pull request as part of this plan.
Start sha: 7e2975a8ec824b14a861476610a250af9ec53522
Diff against the start snapshot: Touched files: `tests/skills/test_workflow_remediation.py` (modified: the new function `test_place_refuses_while_old_package_is_still_in_to_do` starts at line 384, inserted before `test_archive_never_overwrites_existing_destination`; the formatter then reflowed the function once) and `.dev/tasks/to-do/TASK-WF-issueSummary-20261126-161245/artifacts/t3-check.log` (new evidence log: line 3 is the full-file pytest summary, line 4 ruff check, line 5 ruff format check, line 7 the new test alone). Run `git diff 7e2975a8ec824b14a861476610a250af9ec53522 -- tests/skills/test_workflow_remediation.py src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py` to see the diff; the script `remediate.py` is expected to have no change since the start snapshot.
Codegraph context: index_state: fresh; checked_at: 2026-11-26T17:51:38Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-703; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-703. Call codegraph only when index_state: fresh, never to widen scope. Q2b: the change adds one test function only; no symbol that other code depends on changed.
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
