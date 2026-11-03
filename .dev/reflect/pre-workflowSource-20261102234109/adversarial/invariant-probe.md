# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Consensus probed: C-001 remedy = smoke pytest (`-k "doc or primitive or how_we_work or severity"`) then full `make test` as a Task 66 acceptance criterion, smoke run on Task 26, delivered off-plan (A-002).

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | An off-plan delivery (orchestrator instruction or `/sc:workflow` re-run) puts the remedy under the executor's gate either way | UNADDRESSED | HIGH | `/sc:implement` grades each task only against that task's AC and the plan Constraints (`~/.claude/skills/sc-implement-protocol/refs/qa.md:15`; `src/superclaude/commands/implement.md:11`) and "Will Not treat lint or tests as the pass/fail" (`implement.md:91`); only a `/sc:workflow` re-run puts the AC in the plan; debate-transcript.md Round 2 treats both paths as equivalent |
| INV-002 | guard_conditions | `make test` passes on this branch before the plan runs | UNADDRESSED | HIGH | No baseline recorded; `make test` = `uv run pytest` over all `tests` (`Makefile:13-15`, `pyproject.toml:108`); plan forbids code changes (tasklist:23), so a pre-existing unrelated failure would halt Task 66 (E-HALT-QA, sc-implement-protocol SKILL.md:33). Needs a baseline and "no new failures" wording |
| INV-003 | guard_conditions | "both exit 0" is checkable evidence | UNADDRESSED | MEDIUM | qa.md:9 and :31 reject "tests pass" without a `path:line`; Task 6 precedent saves `./artifacts/t6-tests.log` (tasklist:89); remedy names no log |
| INV-004 | collection_boundaries | The smoke `-k` selection covers the files the plan edits | UNADDRESSED | MEDIUM | Covers HOW-WE-WORK (test_how_we_work_*.py) for Task 6; no selected test reads `src/superclaude/rules/core/changelog_maintenance.md` (only `tests/unit/test_cli_install.py:172`, not selected); Task 26 smoke is near-empty |
| INV-005 | collection_boundaries | "doc" selects only documentation tests | UNADDRESSED | LOW | Substring match also selects doctor tests (`tests/cli/eval/test_doctor.py`, `tests/unit/test_cli_doctor.py`); noise only |
| INV-006 | interaction_effects | Catching doc-test failures at Task 66 is early enough | UNADDRESSED | MEDIUM | `tests/docs/test_tavily_doc_alignment.py:77-114` and `tests/docs/test_retired_docs_absent.py:37-49` scan all docs; MCP-doc tasks (2, 13, 29, D02) carry no pytest AC |
| INV-007 | count_divergence | Smoke per item, full suite once at end | ADDRESSED | LOW | Smoke on Tasks 6/26/66, full suite only on Task 66 (tasklist:581-589), relying on in-order execution (A-003) |
| INV-008 | sufficiency_challenge | The remedy alone satisfies source.md:47-50 | UNADDRESSED | HIGH | Falsified by: an earlier task halting (Task 66 never runs, SKILL.md:33); unknown baseline (INV-002); instruction delivery (INV-001); no evidence log (INV-003). The markdownlint half is carried per task (tasklist:27; `make lint` is ruff only, Makefile:48-50) |

## Summary

- **Total findings**: 8
- **ADDRESSED**: 1
- **UNADDRESSED**: 7
  - HIGH: 3 (INV-001, INV-002, INV-008)
  - MEDIUM: 3 (INV-003, INV-004, INV-006)
  - LOW: 1 (INV-005)

Note: the fault-finder reported INV-004 and INV-008 as partly addressed; the protocol allows only ADDRESSED/UNADDRESSED, so partial items are recorded UNADDRESSED.

CONVERGENCE BLOCKED: 3 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-001, INV-002, INV-008
These invariant violations must be resolved before convergence can be declared.
Action: depth=standard has no Round 3; the items are carried into the merged verdict as required additions to the C-001 remedy and the run is marked partial.

WARNING: 3 MEDIUM-severity UNADDRESSED invariant(s) detected
Items: INV-003, INV-004, INV-006
