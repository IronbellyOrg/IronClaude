---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-issueSummary-20261126-161245
version: "1"
priority: Medium
created_date: "2026-11-26"
---

# Finish the five surgical-remediation follow-ups (issue 703)

Source: ./source.md
Goal: The five leftovers of the merged surgical-remediation feature are closed on the integration baseline: `archive` recognizes only a real SUPERSEDED warning, the reflection handoff says repairs happen on a copy, `.dev/README.md` describes all three routing thresholds, the workflow documents promise only the recording that actually happens, and the rule "archive before place" has a direct test. Source files and the four existing plugin mirrors agree byte for byte.

## Constraints

- Base every change on `integration` (the repository default), not the issue's stale `master`. Edit canonical files under `src/superclaude/`, `tests/` and `.dev/README.md`, plus the four existing plugin mirrors named in Task 7. Never edit or stage anything under `.claude/` except through `make sync-dev`, and never stage generated `.claude/` content.
- No new metadata writer, none or forced flag field, placement guard, dependency, contract version, agent or reflection mirror. `place` keeps its existing refusal at `src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py` (the `E-REMEDIATE-SOURCE` check before any write).
- Keep the pull request 705 safeguards untouched: the read/edit-only `workflow-reviser`, the untrusted-report rule, the post-edit digest check, fail-closed behavior, and the coordinator-supplied `diff -w` rule in `src/superclaude/skills/sc-workflow-protocol/refs/remediation.md`.
- Keep the already-resolved findings intact: the `archive-undo.txt` conflict refusal, non-overwriting moves and rollback tests in `tests/skills/test_workflow_remediation.py`.
- Do not modify, move or archive any live task package to reproduce the defect, and leave `docs/designs/surgical-remediation.md` (historical design) unchanged.
- Make no commit, push or pull request as part of this plan.

## Phase 1: Correct warning detection in archive

## Task 1: Scope the existing-warning check in archive to real unresolved items

In `src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py`, `archive` (single caller: `main`, which wires the `archive` subcommand) sets `had_marker = re.search("superseded", text, re.I)` over the whole contract text and then skips adding the warning. Replace that predicate with a small helper (for example `_has_superseded_warning(text)`) that looks only at the items of the top-level `unresolved` key, using the existing `_key_idx`, `_block_end` and the same block and inline-list shapes `_add_unresolved` already handles. It returns true only when an item, after stripping surrounding whitespace and one pair of single or double quotes, begins with the word SUPERSEDED, case-insensitively. A mention elsewhere (an item that merely says another package "is superseded", the `superseded_by` key, any other key) must not count. Leave `_contract_edit`, `_add_unresolved`, `_set_key`, the move, the undo record and `restore` unchanged, so byte-exact restoration still holds.

Acceptance criteria:
- `archive` on a contract whose only mention is an unrelated narrative sentence inside an `unresolved` item (the shape of the contract in the TASK-WF-blockerStage4-20261117-170451 package, read as evidence only) now adds exactly one `SUPERSEDED by <new-id>` item.
- The three existing genuine-warning cases in `test_existing_superseded_gets_no_second_item` (SUPERSEDED, superseded, Superseded) still leave the archived contract byte-identical to the input.
- The list-form and restore cases in `test_unresolved_forms_and_restore_is_byte_identical`, `test_missing_contract_gets_minimal_partial_and_restore_removes_it` and `test_restore_keeps_preexisting_artifacts_dir` still pass unchanged.
- A genuine warning written in the inline flow form (`unresolved: ["SUPERSEDED by hand", "x"]`) is recognized and no second item is added.

## Phase 2: Regression tests

## Task 2: Add the unrelated-mention regression tests for archive

Depends on: Task 1

In `tests/skills/test_workflow_remediation.py`, next to `test_existing_superseded_gets_no_second_item`, add tests that call `rm.archive(repo, pkg, "none")` and `rm.archive(repo, pkg, new)` on contracts built from `BASE_CONTRACT` with: an `unresolved` item that mentions "another package is superseded" mid-sentence; a top-level `superseded_by: other-id` key with no warning item; and a genuine inline-list warning. Reuse the `repo`, `make_pkg` and `top_keys` helpers. Assert the narrative and key cases end with exactly one item starting `SUPERSEDED` and that `rm.restore(repo, OLD)` returns the contract byte-identical, and that the genuine inline case adds nothing.

Acceptance criteria:
- The narrative-mention and key-only tests fail when run against the pre-Task-1 `archive` (confirm once by temporarily reverting the predicate in a scratch copy, not in the working tree) and pass after it.
- The genuine inline-list test passes both before and after the fix.
- `uv run pytest tests/skills/test_workflow_remediation.py -v` passes with no existing test changed or deleted.

## Task 3: Add the direct place-before-archive test

In `tests/skills/test_workflow_remediation.py`, next to `test_place_fails_when_leaf_missing_or_not_empty`, add a test that builds a package with `make_pkg`, calls `rm.reserve` and `repaired_copy`, and then calls `rm.place` without calling `rm.archive`. The existing guard in `place` (`E-REMEDIATE-SOURCE`, "must be archived before place") is already in the code, so this test protects current behavior and is expected to pass on the unchanged baseline.

Acceptance criteria:
- `rm.place` raises `rm.RemediateError` with `code == "E-REMEDIATE-SOURCE"`.
- After the refusal the old package is still in `.dev/tasks/to-do/<OLD>` with its plan and contract unchanged (compare against `sha` of the plan and the original contract text), nothing exists under `.dev/tasks/archive/`, and the reserved leaf is still empty.
- No change to `place` in `src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py` is made for this task.

## Phase 3: Documentation alignment

## Task 4: Say "on a copy" in the reflection handoff

In `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md` (the bullet that says Wave 4R "repairs blocking findings surgically in place"), change the wording so it says Wave 4R repairs blocking findings surgically on a copy and places the repaired plan as a new package, or regenerates the plan as a new package that supersedes the old one. Keep the rest of that bullet, including the ban on hand-editing a placed plan. This file has no plugin mirror; do not create one.

Acceptance criteria:
- `grep -n "in place" src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md` no longer matches the Wave 4R sentence, and the sentence agrees with `src/superclaude/skills/sc-workflow-protocol/refs/remediation.md` section 2 (repair on a copy, archive the original, place a new package).
- Tests that read this handoff file still pass: `uv run pytest tests/cli/reflect -q`.

## Task 5: Describe all three routing thresholds in the package-layout README

In `.dev/README.md`, replace the two bullets "Surgical route" and "Regenerate route" (they route by blocker count alone) with text that matches the ordered rule in `src/superclaude/skills/sc-workflow-protocol/refs/remediation.md` section 1: zero blockers takes the none route first, whatever the HIGH and Medium counts; otherwise surgical requires blockers at most 3 and HIGH-labelled findings at most 5 and Medium findings at most 9 together; otherwise regenerate (at most once per run). Keep the copy-then-archive-then-place description, the 2 fix cycle cap and a pointer to that ref as the authority.

Acceptance criteria:
- The README states all three thresholds (3, 5, 9), the zero-blocker rule and the regenerate fallback, and names the ref as the authoritative source.
- The numbers agree with `route()` in `src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py` and the parametrized `test_route` cases in `tests/skills/test_workflow_remediation.py`.

## Task 6: Narrow the recording promises to what is actually written

Make one consistent statement in `src/superclaude/skills/sc-workflow-protocol/SKILL.md` (Wave 4R paragraph that says `--remediate none` records the counts and the chosen route), `src/superclaude/skills/sc-workflow-protocol/refs/remediation.md` (the paragraph after the `route` command that says a forced route is recorded as forced), and `src/superclaude/commands/workflow.md` (the `--remediate` option row, and the `Will` sentence that says the route and finding counts are recorded in the package contract). The true behavior, from `remediate.py`: `route` only prints `{"route": ..., "forced": ...}`; `place` writes `supersedes`, `remediation_route: surgical` and `finding_counts` for the surgical route; `mark` writes them for the regenerate route (its CLI route is restricted to regenerate); no helper writes a none route or a durable forced flag. So `none` prints the counts and route and changes nothing, a forced route is reported as forced in the printed result only, and the contract carries route and counts only for a placed or marked package. Also check the sentence in `refs/remediation.md` section 1 row 1 that says Medium and Note findings "are written to the contract as follow-up candidates": confirm by reading `SKILL.md` Wave 5 and `refs/return-contract.md` whether any step writes them on the none route, and narrow that sentence the same way if nothing does. Add no writer.

Acceptance criteria:
- None of the three files says that the none route, or the forced flag, is recorded in the contract; each says what is printed and what `place` or `mark` writes.
- Wording agrees across `SKILL.md`, `refs/remediation.md` and `commands/workflow.md`, and the reflect-result lines (`reflect_status`, `reflect_report_path` recorded in the contract) are left as they are because they are written.
- `uv run pytest tests/skills/test_workflow_remediation.py tests/commands/test_workflow_command.py tests/agents/test_workflow_reviser_readonly.py -q` passes, including the check that the coordinator supplies the `diff -w` output.

## Phase 4: Mirrors and synchronization

## Task 7: Update the four plugin mirrors and the generated development copies

Depends on: Task 1, Task 6

Copy the final canonical files to their existing plugin mirrors byte for byte: `src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py` to `plugins/superclaude/skills/sc-workflow-protocol/scripts/remediate.py`; `src/superclaude/skills/sc-workflow-protocol/SKILL.md` to `plugins/superclaude/skills/sc-workflow-protocol/SKILL.md`; `src/superclaude/skills/sc-workflow-protocol/refs/remediation.md` to `plugins/superclaude/skills/sc-workflow-protocol/refs/remediation.md`; and `src/superclaude/commands/workflow.md` to `plugins/superclaude/commands/workflow.md`. Then run `make sync-dev` so the generated `.claude/` copies match, and do not stage the generated `.claude/` content. There is no plugin mirror of `remediation-handoff.md`; do not invent one.

Acceptance criteria:
- `cmp` reports no difference for each of the four source and mirror pairs.
- `make verify-sync` is clean, and `git status --short` shows no change under `.claude/` (generated copies are gitignored).
- With the dev extra installed (`uv sync --extra dev`, ruff pinned in `pyproject.toml`), `uv run pytest tests/skills -q`, `make lint` and `uv run ruff format --check` on `src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py` and `tests/skills/test_workflow_remediation.py` all pass.
- `git status --short` is printed and lists only the planned source, test, README and mirror files.
