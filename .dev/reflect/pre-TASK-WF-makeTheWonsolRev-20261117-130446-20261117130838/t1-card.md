# T1 reflection card (UC-1, pre-execution)

Spec: `.dev/tasks/to-do/TASK-WF-makeTheWonsolRev-20261117-130446/source.md` (6 lines)
Plan: `.dev/tasks/to-do/TASK-WF-makeTheWonsolRev-20261117-130446/TASK-WF-makeTheWonsolRev-20261117-130446.md` (6 tasks, 4 phases)

## Coverage (Step 1B.0: Pass 1 found no labeled IDs; Pass 2 inferred rows, every quote contiguous in source.md)

| Row | Verbatim quote (source.md) | Citation | Plan task | Result |
|-----|----------------------------|----------|-----------|--------|
| INF-001 | "add wonsol as a new packaged panel template" | source.md:3 | Task 2 | covered |
| INF-002 | "make it the product default for ALL runs" | source.md:3 | Task 4 | covered |
| INF-003 | "the product default must not be hard coded" | source.md:3 | Task 4 (pointer file + default_template_name) | covered |
| INF-004 | "precedence must keep working" | source.md:3 | Task 4 acceptance | covered |
| INF-005 | "confirm the product default can support a 3 reviewer panel" | source.md:3 | Task 2, Task 4, Task 5 acceptance | covered |
| INF-006 | "wonsol needs three single-model tier aliases" | source.md:5 | Task 1 | covered |
| INF-007 | "exactly one slot must be fixed" | source.md:5 | Task 2 | covered |
| INF-008 | "so new tiers must get stand-ins" | source.md:5 | Task 1 | covered |
| INF-009 | "the template id must not start with reflect-" | source.md:5 | Constraints, Task 2 | covered |
| INF-010 | "keep it as a packaged template, for example classic" | source.md:5 | Task 3 | covered |
| INF-011 | "decide whether recorded template_id default" | source.md:5 | Task 5 (goldens), Task 3 (id `classic`) | partial: telemetry and manifest fixtures other than the two golden JSONs are not enumerated |
| INF-012 | "every consumer of the default" | source.md:5 | Tasks 4, 5, 6 | covered |
| INF-013 | "a regression test that the default resolves to a template by reference" | source.md:5 | Task 5 | covered |
| INF-014 | "the change must be made on a new branch from origin/master" | source.md:6 | Constraints (process; not a task) | covered |

parsed_count 0, inferred_count 14, coverage_pct (parsed) null, coverage_pct_union 13.5/14 = 0.96, coverage_degraded: parsed-sparse (Step 1B.2b: inferred_count > parsed_count; forbids the Tier 1 stop).

## Grounded observations (cited, Read in this run)

- The hard-coded fallback is `_default("review-panel.default.json")` in `load_panel` (`src/superclaude/cli/review/panel.py:459`); `find_path` (`panel.py:397`) holds the lookup precedence. Task 4 names both.
- `resolve_slot` (`panel.py:536-547`): `fixed` takes `candidates[0]`; `random` picks among all available candidates. Task 1 relies on this and was verified by draft resolve runs for both environments.
- `validate_panel` (`panel.py:160-256`) requires exactly one `fixed` slot and 1..8 reviewers: the 3-reviewer default is legal.
- `tests/review/test_review_panel_live7.py:42` asserts `default["template_id"] == "default"` and 4 reviewers; `tests/review/test_review_panel.py:360` asserts `"default"`; `:401` asserts the file `review-panel.default.json` exists. Task 5 and Task 3 change these.
- The one real consumer of the default is `src/superclaude/rules/prompts/document_review_loop_prompts.md:70`.

## Risks seen by Tier 1 (for the reviewers)

- R-A: Task 3 deletes `review-panel.default.json`; `test_review_panel_exclusion.py` and the golden `panel-golden-default-live7.json` may resolve the default by template id `default` (UNVERIFIED which).
- R-B: Task 1 changes `review-tiers.default.json`; `test_review_panel_reflect_profile.py` notes `tiers_sha256` depends on `classes` (UNVERIFIED how the frozen tier copy interacts).
- R-C: the plan ships a default the owner chose against the pre-registered result; the plan states that in Constraints and Task 6.
- R-D: an existing user's `~/.superclaude/review-panel.json` or `SUPERCLAUDE_REVIEW_PANEL` silently keeps the old behaviour (intended precedence), not mentioned for users in docs.

Calibrated confidence: see `artifacts/t1-calibration.md`.
