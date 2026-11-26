---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-design-20261126-131233
version: "1"
priority: Medium
created_date: "2026-11-26"
---

# Pin the review-only reflect remediation depth and remove the dead result field

Source: ./source.md
Goal: After this plan runs, `/sc:reflect --remediate` still plans at `--depth standard` at every reflect depth and the test suite fails if that changes; the stale deep fallback hint and the stale handoff text in the developer guide are corrected; the write-only `remediation_task_path` field is gone from the `ReflectResult` data model while the schema key stays in the contract.

## Constraints

- The owner decision of 26 Nov 2026 is final: `--depth deep` stays review-only. Phase A keeps calling `sc:workflow-protocol` with `--depth standard --handoff none` at every reflect depth. Add no `plan_depth`, no `Plan depth` prompt line, and no change to `src/superclaude/cli/reflect/runner.py`.
- The contract stays at 1.9.0. The key `remediation_task_path` stays in the section 9.1 block of `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (pinned by `tests/cli/reflect/test_shadow_skill_contract.py`) and in the allow-list in `src/superclaude/cli/reflect/panel_lint.py`. The eight YAML fixtures under `tests/cli/reflect/fixtures/` keep the key. Do not touch `refs/remediation-handoff.md`, `src/superclaude/commands/reflect.md` or either `HOW-WE-WORK.md`.
- Edit only `src/superclaude/`, `docs/developer-guide/session-memory.md` and `tests/cli/reflect/`. Never edit or stage `.claude/` or `.dev/issues/`. No plugin copy of the reflect skill exists, so `make sync-dev` then `make verify-sync` is the whole mirror step.
- The guard test `tests/cli/reflect/test_shadow_skill_contract.py::test_skill_changes_are_confined_to_the_allowed_sections` runs `git diff HEAD -U0` on `SKILL.md` and allows hunks only under sections 3.1, 4.3a, 5.4, 9.1, 9.2 and 17.6. The fallback edit is under section 7, so that one test is red between the `SKILL.md` edit and the commit. Every pytest run in this plan deselects exactly that node id with `--deselect tests/cli/reflect/test_shadow_skill_contract.py::test_skill_changes_are_confined_to_the_allowed_sections`. Never widen its allow-list and never report a deselected run as the complete suite.
- The commit and the complete test run after it are not tasks. `/sc:implement` never commits. After this plan, the commit step of the story commits on the feature branch with a conventional-commit message (staging `src/`, `docs/`, `tests/` and `.dev/tasks`), and then the complete `uv run pytest` runs on the committed tree, guard included, and its failures are compared by node id with `./artifacts/baseline-pytest.md`.
- Line length is 88 (`pyproject.toml`, `line-length = 88`). New or edited Python must pass `uv run ruff check src/ tests/` and `uv run ruff format --check src/ tests/`; fix formatting with `make format`.
- A collected test count is not a pass. Report observed pass and fail counts and node ids.
- Line citations into `SKILL.md` in the developer guide are re-checked with `sed -n` if the branch is rebased onto `origin/integration`.

## Phase 1: Capture the baseline and write the pins that fail first

## Task 1: Capture the pre-change test baseline

Run `make sync-dev` first. The worktree has no `.claude/` mirrors and several audit tests under `tests/audit/` read them, so a baseline taken before the sync is red for unrelated reasons. Then run `uv run pytest` on the unmodified tree (the commit the branch started from) and write the result to `./artifacts/baseline-pytest.md`: the run order, the pass count, the fail count, the error count and every failing node id. Edit no file under `src/`, `tests/` or `docs/` in this task.

Acceptance criteria:
- `./artifacts/baseline-pytest.md` exists and states that `make sync-dev` ran before `uv run pytest`, and lists pass count, fail count, error count and each failing node id (or states that none failed).
- `git status --short` shows no modified tracked file; only untracked `.dev/` paths appear.

## Task 2: Add the Phase A depth pins and the review-only pin to the route-table test module

Depends on: Task 1

Edit only `tests/cli/reflect/test_remediation_route_table.py`. The module already defines `_ROOT`, `_REF` (the file `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md`), `_SKILL` (`src/superclaude/skills/sc-reflect-protocol/SKILL.md`) and `_CMD` (`src/superclaude/commands/reflect.md`) at lines 13 to 16, imports `re`, and has `_row` at line 21. Keep its five existing tests and its docstring unchanged. Add after `_row`:

- A constant `_ROW_PREFIX` equal to the text that starts the delegation-table row in `SKILL.md`: a pipe, a space, then the backticked name `sc:workflow-protocol`, then the text ` (skill, not agent)`.
- A helper `_region(text, start, end)` that asserts `text.count(start) == 1` and `text.count(end) == 1` (each message names the anchor), asserts `start` comes before `end`, and returns the text from `start` up to `end`.
- A helper `_depth_tokens(text)` that returns `re.findall(r"--depth\s+([^\s`]+)", text)`.
- A helper `_delegation_row()` that returns the single line of `_SKILL` that starts with `_ROW_PREFIX` and asserts that exactly one such line exists.

Then add these five test functions, each assertion carrying a message that names its site:

- `test_phase_a_depth_ref_region`: region is `_region(_REF, "### Phase A", "### Phase B")` (lines 28 to 76 today). Assert the token list is not empty, every token equals `standard`, the region contains `--depth standard --handoff none`, and the region does not contain `--strategy`.
- `test_phase_a_depth_skill_region`: region is `_region(_SKILL, "- **Phase A", "- **Phase B")` (lines 374 to 375 today). Assert the token list is not empty, every token equals `standard`, and `--strategy` is absent.
- `test_phase_a_depth_delegation_row`: row is `_delegation_row()` (line 624 today). Assert the token list is not empty, every token equals `standard`, and `--strategy` is absent.
- `test_no_placeholder_depth_on_sc_workflow_lines`: for each of `_REF`, `_SKILL`, `_CMD` and every line containing `sc:workflow`, no token from `_depth_tokens(line)` starts with `<`, `{` or `$`.
- `test_review_only_decision_stays_written_down`: assert `plan_depth`, `Plan depth` and `--plan-depth` occur in none of `_REF`, `_SKILL`, `_CMD`; assert the sentence `` `--depth deep` only sets the review depth `` (backticks included) occurs in `_SKILL` and in `_CMD`; assert the delegation row's last cell, computed as `row.rstrip().rstrip("|").rsplit("|", 1)[-1].strip()`, equals `None; surface the report path and recommend manual planning`, and that `--depth deep` is not in the row.

The unattended continuation lines (`refs/remediation-handoff.md` line 73 and `SKILL.md` line 375) carry no `--depth` and lie inside the two Phase A regions, so these scans block an override there. Prose outside the three regions and outside `sc:workflow` lines is not covered; say so in a one-line comment above the new tests.

Acceptance criteria:
- `uv run pytest tests/cli/reflect/test_remediation_route_table.py -v` on the unedited `SKILL.md` shows the five existing tests passing; `test_phase_a_depth_ref_region`, `test_phase_a_depth_skill_region` and `test_no_placeholder_depth_on_sc_workflow_lines` passing; and `test_phase_a_depth_delegation_row` and `test_review_only_decision_stays_written_down` failing, because line 624 yields the tokens standard and deep and its last cell ends with `or --depth deep`. The output is saved to `./artifacts/t2-red.log`.
- `uv run ruff check tests/cli/reflect/test_remediation_route_table.py` and `uv run ruff format --check tests/cli/reflect/test_remediation_route_table.py` exit 0.
- Mutation check, reverted afterwards: replacing `--depth standard` with `--depth deep`, deleting the flag, or writing `--depth <d>` at one site makes only that site's function fail while the other two site functions still pass; after the revert `git diff -- src/superclaude/skills/sc-reflect-protocol` is empty.

## Task 3: Add the verdict case for the retired result attribute

Depends on: Task 1

Edit only `tests/cli/reflect/test_verdict_mapping.py`. It already imports `derive_verdict` (from `superclaude.cli.reflect.contract`) and `Verdict` (from `superclaude.cli.reflect.models`) and defines `_load(name)` at lines 12 to 19; add no import. Add one function, `test_both_pointers_keep_the_plan_pointer_and_drop_the_retired_attribute`. It loads `contract = _load("autofixable_drift_both.yaml")` (the fixture under `tests/cli/reflect/fixtures/` has `status: partial` and both pointer keys), calls `derive_verdict(contract, expected_tier=2, allow_single_vendor=False, child_rc=0)`, and asserts: the verdict `is Verdict.HALTED`; `result.verdict.exit_code == 10`; `result.remediation_plan_path == contract["remediation_plan_path"]`; and `not hasattr(result, "remediation_task_path")`.

The expected HALTED verdict and exit code 10 were derived by reading `_halted_reason` in `src/superclaude/cli/reflect/contract.py` (reason `status-partial`); confirm them by running the case. If the observed verdict differs, record the observed verdict and reason in the artifact and correct the expected values only after confirming the reason comes from the fixture's `status: partial`.

Acceptance criteria:
- On the unmodified models, `uv run pytest tests/cli/reflect/test_verdict_mapping.py -v` shows the new case failing only on the `hasattr` assertion (the dataclass default keeps the attribute present) and every existing case in the file passing; the output is saved to `./artifacts/t3-red.log`.
- `uv run ruff check tests/cli/reflect/test_verdict_mapping.py` and `uv run ruff format --check tests/cli/reflect/test_verdict_mapping.py` exit 0.

## Phase 2: Remove the dead wrapper field

## Task 4: Remove the write-only field and its only writer

Depends on: Task 3

Edit `src/superclaude/cli/reflect/contract.py` and `src/superclaude/cli/reflect/models.py` together in one change. The field is written once and read nowhere: the auto-fix loop reads only `remediation_plan_path` (`src/superclaude/cli/reflect/runner.py`, line 765), and no code or test passes the field except `contract.py` line 126.

In `contract.py`, inside `_make_result` (line 104), in the `ReflectResult(...)` call: delete the line

```text
        remediation_task_path=c.get("remediation_task_path"),
```

and replace the two FR-8 comment lines above it and the one comment line above `remediation_plan_path=` with a single comment block directly above `remediation_plan_path=c.get("remediation_plan_path"),` reading: FR-8: the wrapper only READS the plan path reflect emits (contract 1.8.0: the `sc:workflow` `<slug>.md` tasklist); None when reflect authored none, and on older contracts. Keep every other line, including the FX7 comments below.

In `models.py`, in the `ReflectResult` dataclass: delete the line `    remediation_task_path: str | None = None` and replace the two-line comment above `remediation_plan_path` with: Contract 1.8.0: the ``sc:workflow`` tasklist ``<slug>.md`` the wrapper runs via ``/sc:implement``. Keep `remediation_plan_path: str | None = None` and its position among its neighbours. Leave the comment at lines 143 to 145 (consumed remediation pointer, FR-8) unchanged. Wrap comments at 88 columns. Neither reworded comment may contain the text `remediation_task_path`.

Do not touch `runner.py` (its comment at lines 763 to 764 stays true), `panel_lint.py`, `SKILL.md` or any fixture. The dependents that must keep working are the `ReflectResult` constructions in `src/superclaude/cli/reflect/commands.py` (lines 406 and 448), `runner.py` (lines 615, 652, 669 and 696), `contract.py` (line 114) and `tests/cli/reflect/test_writeback.py` (lines 42 and 182), all of which pass keywords and never the removed one; and the `derive_verdict` consumers `runner.py` (line 572, inside `_audit_once`) and `scripts/reflect_verdict_replay.py` (line 83, which reads only `result.verdict.value` and `result.reason`).

Acceptance criteria:
- `git grep -n remediation_task_path -- src/superclaude/cli` prints exactly two lines: `src/superclaude/cli/reflect/panel_lint.py:115` and `src/superclaude/cli/reflect/runner.py:763`.
- `uv run pytest tests/cli/reflect/test_verdict_mapping.py tests/cli/reflect/test_fix_loop.py tests/cli/reflect/test_writeback.py tests/cli/reflect/test_panel_contract_lint.py` passes, including the new verdict case from Task 3 and the unchanged `test_stale_task_pointer_is_ignored_when_both_pointers_set` and `test_task_pointer_alone_is_not_applied` in `tests/cli/reflect/test_fix_loop.py`.
- `uv run ruff check src/superclaude/cli/reflect/contract.py src/superclaude/cli/reflect/models.py` and the matching `uv run ruff format --check` exit 0.
- If any test shows a caller of the removed field, restore the field line in `models.py` and the kwarg line in `contract.py`, keep the comment rewording, and record the caller in `./artifacts/t4-note.md`.

## Task 5: Correct the stale docstring in the absent-path loop test

Depends on: Task 4

Edit only `tests/cli/reflect/test_fix_loop.py`, line 95, the docstring of `test_cannot_repair_absent_path_halts_no_apply`. The fixture `tests/cli/reflect/fixtures/autofixable_drift_no_path.yaml` has no `remediation_plan_path` key and the halting branch is in `runner.py` (lines 765 to 767). Replace the docstring line with exactly:

```text
    """AUTO-FIXABLE verdict with no remediation_plan_path -> terminal HALT, no apply."""
```

Leave the test body untouched.

Acceptance criteria:
- `git diff -U0 -- tests/cli/reflect/test_fix_loop.py` shows exactly one changed line, and the new line is 88 columns or fewer.
- `uv run pytest tests/cli/reflect/test_fix_loop.py` passes and `uv run ruff format --check tests/cli/reflect/test_fix_loop.py` exits 0.

## Phase 3: Correct the developer guide

## Task 6: Fix the false handoff sentence and the stale citations in the session-memory guide

Depends on: Task 5

Edit only `docs/developer-guide/session-memory.md`; change exactly three lines. In `src/superclaude/skills/sc-reflect-protocol/SKILL.md` the section 6.3 heading is at line 574, the `.gitignore` rule is in the paragraph at line 576, the last-pass write is at line 581, the retired-handoff note is at line 588, old handoff files being left in place is stated at line 595, and the section ends at line 598 (section 6.4 starts at line 600).

Line 33: change `sc-reflect-protocol/SKILL.md:376` to `sc-reflect-protocol/SKILL.md:576`; leave the rest of the line.

Line 59: replace the sentence with exactly:

```text
Subfolder keys follow the same split. For example, `/sc:reflect` overwrites `reflect/last-pass-{slug}.md` whole (`sc-reflect-protocol/SKILL.md:581`). It no longer writes `reflect/handoff-*.md` files: they were retired in 6.1.0 (`sc-reflect-protocol/SKILL.md:588`, section 6.3 "Handoff files"), and existing ones are left in place.
```

Line 79, last cell: change `sc-reflect-protocol/SKILL.md:262,376-378,590-600` to `sc-reflect-protocol/SKILL.md:262,576-598`. Line 262 (Step 0.7 memory hydrate) is correct and the new range keeps line 588.

Acceptance criteria:
- `git diff -U0 -- docs/developer-guide/session-memory.md` shows exactly three changed lines (33, 59 and 79).
- `git grep -n 'timestamp}.md` once' docs/developer-guide/session-memory.md` prints nothing.
- `sed -n '262p;576p;581p;588p;598p' src/superclaude/skills/sc-reflect-protocol/SKILL.md` shows, in order, the Step 0.7 memory hydrate line, the memory paragraph with the `.gitignore` rule, the last-pass write, the retired-handoff note, and the closing sentence of section 6.3; the output is saved to `./artifacts/t6-citations.txt`.

## Phase 4: Remove the dead fallback and close the change set

## Task 7: Remove the dead deep fallback at SKILL.md line 624 and run the aggregate checks

Depends on: Task 6

Edit only `src/superclaude/skills/sc-reflect-protocol/SKILL.md`, line 624, the `sc:workflow-protocol` row of the delegation table under the heading `## 7. Agent Delegation Map` (line 610). Replace the last table cell only: the old cell is the text `None; surface the report path and recommend manual planning or` followed by a space and the backticked flag `--depth deep`; the new cell is exactly `None; surface the report path and recommend manual planning`. Keep every other cell, including `--depth standard --handoff none` in the third cell, and keep the line count of the file: record `wc -l` before the edit and compare after. The same advice appears nowhere else (`refs/remediation-handoff.md` line 187 already says only `recommend manual planning`).

Then run the aggregate checks for the whole change set, with the guard deselected as the Constraints say, and write each command with its exit code and the counts to `./artifacts/t7-checks.md`.

Acceptance criteria:
- `git diff --stat -- src/superclaude/skills/sc-reflect-protocol/SKILL.md` shows one insertion and one deletion, and `wc -l` of the file is unchanged.
- `git grep -n "manual planning or" -- src/superclaude` prints nothing.
- The two tests that failed in Task 2 (`test_phase_a_depth_delegation_row` and `test_review_only_decision_stays_written_down`) now pass.
- `uv run pytest tests/cli/reflect --deselect tests/cli/reflect/test_shadow_skill_contract.py::test_skill_changes_are_confined_to_the_allowed_sections` has no failure that is absent from `./artifacts/baseline-pytest.md` (compared by node id).
- `uv run ruff check src/ tests/` and `uv run ruff format --check src/ tests/` exit 0.
- `make sync-dev` then `make verify-sync` exit 0.
- `git status --short` lists, besides the `.dev/` paths, only `src/superclaude/cli/reflect/contract.py`, `src/superclaude/cli/reflect/models.py`, `src/superclaude/skills/sc-reflect-protocol/SKILL.md`, `docs/developer-guide/session-memory.md`, `tests/cli/reflect/test_remediation_route_table.py`, `tests/cli/reflect/test_verdict_mapping.py` and `tests/cli/reflect/test_fix_loop.py`.
