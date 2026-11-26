# Design: sc:reflect remediation pins and dead-field cleanup (issue 599, after pull request 653)

Type: component. Format: spec. Source requirements: `.dev/brainstorms/20261126-120549-reflect-remediate-depth-after-pr-653/merged-requirements.md` (R-01 to R-07). That file is the source of truth for the reasons; this document fixes the interfaces, the exact edits and the test contracts so a plan can be built from it without new decisions.

Grounding: index_state: fresh, checked_at 2026-11-26T13:09:58Z, projectPath `/home/coder/workspaces/worktrees/IronClaude/issue-599`; tools used: `codegraph_status`, `codegraph_search`, `codegraph_callers`, `codegraph_impact`, `codegraph_node` (symbolsOnly). The lookup for the field name `remediation_task_path` returned no definition row (graph:empty: dataclass attributes are not indexed as symbols), so field uses were confirmed with `git grep` and Read. Caller rows give definition lines only; every cited `file:line` below was re-read.

## 1. Decision constraints (fixed)

- Owner decision of 26 Nov 2026: `--depth deep` stays review-only. Phase A calls `sc:workflow-protocol` with `--depth standard --handoff none` at every reflect depth. No `plan_depth`, no `Plan depth` prompt line, no change to `runner.py` route logic.
- Contract stays `1.9.0`. The schema key `remediation_task_path` stays in the `SKILL.md` §9.1 block (`SKILL.md:829`, pinned by `test_shadow_skill_contract.py:43-50`) and in the lint allow-list (`panel_lint.py:115`). The eight YAML fixtures keep the key.
- Edit surface: `src/superclaude/`, `docs/developer-guide/`, `tests/cli/reflect/`. No plugin copy of the reflect skill exists, so `make sync-dev` then `make verify-sync` is the whole mirror step.

## 2. Component map

| Component | File | Change | Requirement |
|---|---|---|---|
| Delegation table row | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:624` | text edit inside one line | R-01 |
| Developer guide | `docs/developer-guide/session-memory.md:33,59,79` | three text edits | R-02 |
| Result contract reader | `src/superclaude/cli/reflect/contract.py:124-128` | delete one kwarg, reword its comment | R-03 |
| Result data model | `src/superclaude/cli/reflect/models.py:148-150` | delete one field, reword its comment | R-03 |
| Test docstring | `tests/cli/reflect/test_fix_loop.py:95` | one docstring line | R-04 |
| Route-table pin | `tests/cli/reflect/test_remediation_route_table.py` | add helpers, test A (4 functions), test B (1 function) | R-05 |
| Verdict pin | `tests/cli/reflect/test_verdict_mapping.py` | add one case | R-06 |
| Verification order | none (procedure) | sequence of commands | R-07 |

Not changed (confirmed): `runner.py` (reads only `remediation_plan_path`, `runner.py:765`), `panel_lint.py`, `SKILL.md` §9.1, `refs/remediation-handoff.md`, `commands/reflect.md`, both `HOW-WE-WORK.md` copies, the fixtures.

## 3. Interface specifications

### 3.1 `ReflectResult` (`models.py`, dataclass)

- Before: fields `verdict, status, tier_reached, reason, report_path, contract_path, deviations, child_exit_code, write_status, fix_iterations, fix_converged, remediation_task_path, remediation_plan_path, ...` (`models.py:126-151` and later telemetry fields).
- After: the same list without `remediation_task_path`. `remediation_plan_path: str | None = None` stays, with its default, in the same position relative to its neighbours.
- Consumers (confirmed by `git grep "ReflectResult("` over `src tests scripts`): constructions at `commands.py:406,448`, `contract.py:114`, `runner.py:615,652,669,696`, `tests/cli/reflect/test_writeback.py:42,182`. All use keywords; only `contract.py:126` passes the removed field. `scripts/reflect_shadow_exit.py`, `scripts/reflect_verdict_replay.py` and `tests/swarm/test_coder_tier_env_2026_10.py` do not mention the field or construct the type. `ReflectResult` is exported in `superclaude/cli/reflect/__init__.py:20,26`; an outside importer that passes the removed kwarg would get a `TypeError` (accepted residual risk, with the fallback in section 6).

### 3.2 `_make_result` (`contract.py:104`)

Signature unchanged: `(verdict: Verdict, *, reason: str, contract: dict | None, child_rc: int) -> ReflectResult`. The `ReflectResult(...)` call inside it loses the line `remediation_task_path=c.get("remediation_task_path"),` and keeps `remediation_plan_path=c.get("remediation_plan_path"),`. `derive_verdict` (`contract.py:138`) is unchanged: `(contract, *, expected_tier, allow_single_vendor, child_rc, promoting=False)`.

### 3.3 Exact text edits

All strings are literal; whitespace outside the quoted text is preserved.

1. `SKILL.md:624`, last table cell only.
   - Old: `None; surface the report path and recommend manual planning or `--depth deep``
   - New: `None; surface the report path and recommend manual planning`
   - The line keeps its other cells and `--depth standard --handoff none` in the third cell. No line is added or removed.
2. `session-memory.md:33`: `sc-reflect-protocol/SKILL.md:376` becomes `sc-reflect-protocol/SKILL.md:576` (the `.gitignore` rule is in the paragraph at `SKILL.md:576`; `:376` is now the Phase B bullet).
3. `session-memory.md:59`:
   - Old: `Subfolder keys follow the same split. For example, `/sc:reflect` overwrites `reflect/last-pass-{slug}.md` whole and writes `reflect/handoff-{slug}-{timestamp}.md` once (`sc-reflect-protocol/SKILL.md:592-594`).`
   - New: `Subfolder keys follow the same split. For example, `/sc:reflect` overwrites `reflect/last-pass-{slug}.md` whole (`sc-reflect-protocol/SKILL.md:581`). It no longer writes `reflect/handoff-*.md` files: they were retired in 6.1.0 (`sc-reflect-protocol/SKILL.md:588`, section 6.3 "Handoff files"), and existing ones are left in place.`
4. `session-memory.md:79`, last cell: `sc-reflect-protocol/SKILL.md:262,376-378,590-600` becomes `sc-reflect-protocol/SKILL.md:262,576-598` (`:262` is correct; §6.3 spans `:574-598`; `:588` stays inside the range).
5. `contract.py:124-127`: remove the kwarg line `remediation_task_path=c.get("remediation_task_path"),`; replace the two FR-8 comment lines and the 1.8.0 comment line with one comment block above `remediation_plan_path=...`: "FR-8: the wrapper only READS the plan path reflect emits (contract 1.8.0: the `sc:workflow` `<slug>.md` tasklist); None when reflect authored none, and on older contracts." Wrap at 88 columns. The block must not contain the text `remediation_task_path`.
6. `models.py:148-150`: delete the field line `remediation_task_path: str | None = None`; replace the two-line comment above `remediation_plan_path` with: "Contract 1.8.0: the ``sc:workflow`` tasklist ``<slug>.md`` the wrapper runs via ``/sc:implement``." Wrap at 88 columns; must not contain `remediation_task_path`. The comment at `models.py:143-145` ("consumed remediation pointer (FR-8)") stays true and is untouched.
7. `test_fix_loop.py:95`: the docstring line becomes `    """AUTO-FIXABLE verdict with no remediation_plan_path -> terminal HALT, no apply."""` (88 columns; the limit is `pyproject.toml:175`, `line-length = 88`). The test body is untouched.

## 4. Test contracts

### 4.1 Helpers in `test_remediation_route_table.py`

The module already defines `_ROOT`, `_REF`, `_SKILL`, `_CMD` (`:13-16`) and `_row` (`:21`). Add two helpers, and keep the existing five tests unchanged:

- `_region(text, start, end)`: asserts `text.count(start) == 1` and `text.count(end) == 1` and that `start` comes first; returns the text from `start` up to `end`. A missing or renamed anchor fails with the anchor in the message.
- `_depth_tokens(text)`: returns `re.findall(r"--depth\s+([^\s`]+)", text)`.

### 4.2 Test A: Phase A planning depth is `standard` at each site

One function per site, so a failure names the site. Anchors and today's tokens (verified by running the pattern per line, see `diff-analysis.md` F-5):

| Function | Region | Anchors | Tokens today | After R-01 |
|---|---|---|---|---|
| `test_phase_a_depth_ref_region` | `refs/remediation-handoff.md` Phase A (`:28-76`) | start `### Phase A`, end `### Phase B` | `['standard']` | same |
| `test_phase_a_depth_skill_region` | `SKILL.md` Phase A bullets (`:374-375`) | start `- **Phase A`, end `- **Phase B` | `['standard']` | same |
| `test_phase_a_depth_delegation_row` | the `sc:workflow-protocol` table row (`SKILL.md:624`) | the single line starting `` | `sc:workflow-protocol` (skill, not agent) `` | `['standard', 'deep']` (red) | `['standard']` (green) |

Each of the three asserts, in order: the anchors exist (inside `_region` or an equivalent unique-line lookup for the row); the token list is not empty (a deleted flag cannot pass vacuously); every token equals `standard`; `--strategy` does not occur in the region (workflow plans deep for `--strategy enterprise` with no `--depth`, `sc-workflow-protocol/SKILL.md:57`). The ref function also asserts `--depth standard --handoff none` occurs in its region. Both Phase A regions contain the unattended continuation lines (`remediation-handoff.md:73`, `SKILL.md:375`), which carry no `--depth`: the scan blocks an override there.

`test_no_placeholder_depth_on_sc_workflow_lines`: for each of `_REF`, `_SKILL`, `_CMD`, for every line containing `sc:workflow`, no token from `_depth_tokens(line)` starts with `<`, `{` or `$`. Green today (the captures on those lines are ref `:3` `deep`, `:72` `standard`; skill `:374` `standard`, `:624` `standard` and `deep`; command `:107` and `:302` `deep`).

### 4.3 Test B: the review-only decision stays written down

One function, `test_review_only_decision_stays_written_down`. Asserts:

- `plan_depth`, `Plan depth` and `--plan-depth` occur in none of `_REF`, `_SKILL`, `_CMD` (absent today; the opt-in prompt block is `remediation-handoff.md:117-139`).
- the sentence `` `--depth deep` only sets the review depth `` (backticks included) occurs in `_SKILL` (`SKILL.md:363`) and in `_CMD` (`commands/reflect.md:107`).
- the delegation row's last cell, from `row.rstrip().rstrip("|").rsplit("|", 1)[-1].strip()`, equals `None; surface the report path and recommend manual planning`, and `--depth deep` is not in the row.

Red on today's tree (the old fallback), green after R-01. Not pinned: the "deep alone" row literal, because the real row at `remediation-handoff.md:13` has backticks and the rule is already stated at `SKILL.md:365`.

### 4.4 Verdict case in `test_verdict_mapping.py`

One function, `test_both_pointers_keep_the_plan_pointer_and_drop_the_retired_attribute`. It reuses the existing imports and `_load` (`test_verdict_mapping.py:12-19`); no new imports. Steps: `contract = _load("autofixable_drift_both.yaml")`; `result = derive_verdict(contract, expected_tier=2, allow_single_vendor=False, child_rc=0)`. Asserts: `result.verdict is Verdict.HALTED`; `result.verdict.exit_code == 10`; `result.remediation_plan_path == contract["remediation_plan_path"]`; `not hasattr(result, "remediation_task_path")`. The fixture has `status: partial` (line 2) and both pointers (lines 27-28). The expected verdict was derived by reading `_halted_reason` (`contract.py:361`, `status-partial`); confirm it by running the case before relying on it. Red before R-03 (the dataclass default makes `hasattr` true), green after.

### 4.5 Must stay green unchanged

`test_shadow_skill_contract.py:43-50` (1.9.0 block), `test_panel_contract_lint.py`, `test_remediation_source_template.py`, `test_fix_loop.py:195-225` (both pointers; task pointer alone) and `:228-245` (apply verb at each depth), and the five existing tests in the route-table module.

## 5. Verification procedure (R-07, in this order)

1. `make sync-dev`, then a baseline `uv run pytest` at `862384852`; record pass and fail counts and failing node ids. The worktree has no `.claude/` mirrors, so a baseline before `make sync-dev` is red for unrelated reasons.
2. Add test A, test B and the verdict case; run them and confirm the expected red set: test A's delegation-row function, test B, and the verdict case. The other test A functions pass.
3. Make edits R-01 to R-04.
4. `uv run pytest tests/cli/reflect --deselect tests/cli/reflect/test_shadow_skill_contract.py::test_skill_changes_are_confined_to_the_allowed_sections`.
5. `uv run ruff check src/ tests/` and `uv run ruff format --check src/ tests/` exit 0 (fix with `make format`); `make sync-dev` then `make verify-sync` exit 0; `git grep -n remediation_task_path -- src/superclaude/cli` prints exactly `panel_lint.py:115` and `runner.py:763`; `git grep -n "manual planning or" -- src/superclaude` prints nothing; `sed -n '262p;576p;581p;588p;598p'` on `SKILL.md` shows the text each citation claims.
6. Commit on the feature branch with a conventional-commit message. `/sc:implement` never commits, so the commit is a separate authorized step (the story's commit step). Stage `src/`, `docs/`, `tests/` and `.dev/tasks`; never `.claude/` or `.dev/issues/`.
7. Run the complete `uv run pytest` on the committed tree. The guard test `test_skill_changes_are_confined_to_the_allowed_sections` (`test_shadow_skill_contract.py:53-76`) runs `git diff HEAD -U0` on `SKILL.md` and allows hunks only under §3.1, §4.3a, §5.4, §9.1, §9.2 and §17.6; the R-01 edit is under §7 (`SKILL.md:610-663`), so the test is red until the commit and green after. Compare failures by node id with the baseline. A collected test count is not a pass; a deselected run is never reported as the full suite. Without a commit, report the final verification as blocked.

## 6. Risks and limits (design level)

- The pins read instruction text, not a runtime call. The unattended continuation relies on workflow's default `standard` (`commands/workflow.md:42`); a changed default is not caught (residual).
- Prose outside the three regions and outside `sc:workflow` lines is not scanned; the `--strategy` assertion and the placeholder scan are the only guards beyond depth tokens.
- The installed copy `~/.claude/skills/sc-reflect-protocol/` keeps the old fallback until `superclaude install` runs; a live manual run uses the old text until then.
- Outside importers of `ReflectResult`: if the full suite shows a caller, restore the field (`models.py` one line, `contract.py` one line) and keep the comment fixes.
- If a new test line is flagged by `ruff format --check`, run `make format` and re-run step 5.

## 7. Traceability

| Requirement | Edit | Test | Red before, green after |
|---|---|---|---|
| R-01 | 3.3 item 1 | test A (row), test B | yes |
| R-02 | 3.3 items 2-4 | `git grep` and `sed -n` checks (step 5) | n/a (docs) |
| R-03 | 3.3 items 5-6 | verdict case; `git grep` count | yes |
| R-04 | 3.3 item 7 | existing test unchanged | n/a |
| R-05 | 4.1-4.3 | test A, test B | row function and test B red before R-01 |
| R-06 | 4.4 | verdict case | yes |
| R-07 | section 5 | ordered commands | n/a |

Decisions are all made; none is left for planning. The plan should keep section 5 as an ordered step list, with step 6 (commit) marked as outside `/sc:implement`.
