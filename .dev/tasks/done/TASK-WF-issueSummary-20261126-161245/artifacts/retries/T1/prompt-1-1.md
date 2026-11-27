4f3e9ea1a38a6b4dc7abd7878bad36df43ea8470
Review one task for spec compliance.

Task brief: Task T1 "Scope the existing-warning check in archive to real unresolved items". In `src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py`, `archive` (single caller: `main`, which wires the `archive` subcommand) sets `had_marker = re.search("superseded", text, re.I)` over the whole contract text and then skips adding the warning. Replace that predicate with a small helper (for example `_has_superseded_warning(text)`) that looks only at the items of the top-level `unresolved` key, using the existing `_key_idx`, `_block_end` and the same block and inline-list shapes `_add_unresolved` already handles. It returns true only when an item, after stripping surrounding whitespace and one pair of single or double quotes, begins with the word SUPERSEDED, case-insensitively. A mention elsewhere (an item that merely says another package "is superseded", the `superseded_by` key, any other key) must not count. Leave `_contract_edit`, `_add_unresolved`, `_set_key`, the move, the undo record and `restore` unchanged, so byte-exact restoration still holds.
AC ids:
- T1.AC1: `archive` on a contract whose only mention is an unrelated narrative sentence inside an `unresolved` item (the shape of the contract in the TASK-WF-blockerStage4-20261117-170451 package, read as evidence only) now adds exactly one `SUPERSEDED by <new-id>` item.
- T1.AC2: The three existing genuine-warning cases in `test_existing_superseded_gets_no_second_item` (SUPERSEDED, superseded, Superseded) still leave the archived contract byte-identical to the input.
- T1.AC3: The list-form and restore cases in `test_unresolved_forms_and_restore_is_byte_identical`, `test_missing_contract_gets_minimal_partial_and_restore_removes_it` and `test_restore_keeps_preexisting_artifacts_dir` still pass unchanged.
- T1.AC4: A genuine warning written in the inline flow form (`unresolved: ["SUPERSEDED by hand", "x"]`) is recognized and no second item is added.
Global constraints:
- Base every change on `integration`, not the issue's stale `master`. Edit canonical files under `src/superclaude/`, `tests/` and `.dev/README.md`, plus the four existing plugin mirrors named in Task 7. Never edit or stage anything under `.claude/` except through `make sync-dev`, and never stage generated `.claude/` content.
- No new metadata writer, none or forced flag field, placement guard, dependency, contract version, agent or reflection mirror. `place` keeps its existing refusal (the `E-REMEDIATE-SOURCE` check before any write).
- Keep the pull request 705 safeguards untouched.
- Keep the already-resolved findings intact: the `archive-undo.txt` conflict refusal, non-overwriting moves and rollback tests in `tests/skills/test_workflow_remediation.py`.
- Do not modify, move or archive any live task package to reproduce the defect, and leave `docs/designs/surgical-remediation.md` unchanged.
- Make no commit, push or pull request as part of this plan.
Start sha: 4f3e9ea1a38a6b4dc7abd7878bad36df43ea8470
Diff against the start snapshot: Touched files: `src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py` (modified), `.dev/tasks/to-do/TASK-WF-issueSummary-20261126-161245/artifacts/t1-check.log` (new, evidence log for the AC checks; read it from disk). Run `git diff 4f3e9ea1a38a6b4dc7abd7878bad36df43ea8470 -- src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py` in your head from this hunk summary, or read the file: the diff adds a new function `_has_superseded_warning(text)` after `_contract_edit` and changes the single line in `archive` from `had_marker = re.search("superseded", text, re.I) is not None` to `had_marker = _has_superseded_warning(text)`. The new function (lines 404-428 of the file) splits the text into lines, finds the first top-level `unresolved` key with `_key_idx`, reads an inline `[...]` list by splitting on commas or a block list by matching `^\s*-\s+(.*)$` over `lines[i+1:_block_end(lines, i)]`, and returns true when any item, stripped and with leading quote characters removed, matches `superseded\b` case-insensitively at its start.
Codegraph context: index_state: fresh; checked_at: 2026-11-26T17:51:38Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-703; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-703. Call codegraph only when index_state: fresh, never to widen scope. Q2b dependents not in the diff: `archive` has one caller, `main` (remediate.py, the `add("archive", ...)` line), unchanged; tests call `rm.archive` directly.
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
