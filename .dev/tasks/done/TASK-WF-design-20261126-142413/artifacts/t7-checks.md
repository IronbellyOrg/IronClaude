# Task 7 aggregate checks

Run on 2026-11-26 in the worktree of branch `clayphi/issue-599`, with ruff 0.17.3 (the project pins 0.15.20; see `./baseline-pytest.md`).

complete-suite verification: blocked until the commit

The complete `uv run pytest` run on the committed tree, guard test included, has not been run. It is not a task of this plan; the commit step of the story and the run after it do that, and its failures are compared by node id with `./artifacts/baseline-pytest.md`.

## Commands, exit codes and counts

| Check | Command | Exit code | Observed result | Evidence |
|---|---|---|---|---|
| Edit size | `git diff --stat -- src/superclaude/skills/sc-reflect-protocol/SKILL.md` | 0 | 1 insertion, 1 deletion; `wc -l` 2007 before and 2007 after | `./t7-edit-check.txt`, `./t7-wc-before.txt` |
| Old text gone | `git grep -n "manual planning or" -- src/superclaude` | 1 (no match) | prints nothing | `./t7-edit-check.txt` |
| Route-table tests | `uv run pytest tests/cli/reflect/test_remediation_route_table.py -v` | 0 | 10 passed, 0 failed; `test_phase_a_depth_delegation_row` and `test_review_only_decision_stays_written_down` (the two that failed in Task 2) now PASSED | `./t7-route-table-pytest.log` |
| Reflect directory, guard deselected | `uv run pytest tests/cli/reflect --deselect tests/cli/reflect/test_shadow_skill_contract.py::test_skill_changes_are_confined_to_the_allowed_sections` | 0 | 366 passed, 1 deselected, 0 failed, 0 errors. The baseline failures are two node ids in `tests/cli/eval/`, outside this directory, so no failure here is absent from the baseline | `./t7-reflect-pytest-summary.txt` |
| Lint | `uv run ruff check src/ tests/` | 0 | All checks passed | `./t7-ruff.txt` |
| Format | `uv run ruff format --check src/ tests/` | 1 | 6 files would be reformatted: exactly the six that Task 1 listed (`src/superclaude/examples/release-spec-template.md`, `.../sc-cleanup-audit-protocol/rules/dynamic-use-checklist.md`, `.../sc-pr-submit-protocol/SKILL.md`, `.../sc-reflect-protocol/refs/grader-extensions.md`, `.../sc-validate-tests-protocol/SKILL.md`, `src/superclaude/templates/documents/release-spec-template.md`). None of the seven edited files is listed | `./t7-ruff.txt` |
| Mutation check | `uv run python ./artifacts/t7-mutation-check.py` from the repository root | 0 | unmutated run: 5 of 5 pass; nine mutation cases each failed exactly the expected functions; restored run: 5 of 5 pass; 0 mismatches | `./t7-mutation.log` |
| Mirror | `make sync-dev`, then `make verify-sync` | 0, 0 | `All components in sync.` | `./t7-sync-verify.txt` |
| Changed paths | `git status --short` | 0 | besides `.dev/` paths, only the seven edited files: `contract.py`, `models.py`, `SKILL.md`, `session-memory.md`, `test_remediation_route_table.py`, `test_verdict_mapping.py`, `test_fix_loop.py` | `./t7-git-status.txt` |

## Departures

- `make format` was not run. Task 1's `uv run ruff format --check .` exited 1 on the unmodified tree, so the plan's Constraints require a departure from spec step 5: formatting was done per edited file with `uv run ruff format <file>`, and the `src/ tests/` format check lists only the six files of the baseline. This is a necessary deviation, recorded here as the Constraints order.
- The guard test `tests/cli/reflect/test_shadow_skill_contract.py::test_skill_changes_are_confined_to_the_allowed_sections` was deselected in the reflect-directory run above, as the Constraints order. That run is not the complete suite.
