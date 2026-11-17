# Task 7 record: what was re-pinned and what changed in the fixtures

## Test list run before any edit (after Tasks 2 to 6)

`uv run pytest` over the eight files of the Task 7 acceptance line: 2 failed, 272 passed.

- `tests/skills/test_review_severity_mapping.py::test_medium_tier_follows_the_untouched_s1_s5_bullets` failed on the pin "asks the user once per loop whether to open an issue".
- `tests/skills/test_implement_severity_static.py::test_p1_output_style_exempts_implement_severity_model` failed on the exact-equality pin of the old S2 sentence.

## Edits (only the two that failed)

- `test_review_severity_mapping.py`: the pragmatic Medium pin now reads "asks the user once per run, and again at any escalation halt, whether to open an issue". The spec-panel "once per loop" pins are untouched (they move in stage 4).
- `test_implement_severity_static.py`: the S2 equality is replaced by a consequence check (S2 opens "- Minor findings never fail a review:", holds "never starts a fix pass", "Medium and Note findings are not rechecked in later rounds" and "Only blocking findings produce FAIL."). The S4 equality and the `qa.md` pins are unchanged.
- `test_review_severity_rule.py`: not edited. `S_OPENINGS`, `S1_S3_FILES` and `S5_FILES` unchanged; no registry dispatch added.
- `test_review_prompt_overrides.py`: not edited; it passed without a change (its output-style pins on "never to meet a quota" and the zero-finding wording still hold).

## Fixtures and plan tables

`tests/skills/fixtures/review_severity_cap_edits.yaml`, `tests/skills/fixtures/review_severity_sweep_edits.yaml`, `.dev/review-severity-rule/cap-edits.yaml` and `.dev/review-severity-rule/sweep-edits.yaml`: none changed. Tasks 3 to 6 did not change the `new` text of any row, so no row was updated.

## Sweep-edit paragraph check

`test_j_every_sweep_edits_row_holds` was run (it is in `./artifacts/t7-pytest.log`, which ends "274 passed") after the stage 1 print paragraph was in place in `sc-implement-protocol`. It passed. No sweep-edit row names a file of `sc-implement-protocol`, so no row needed re-pinning for that paragraph. `test_ej_fixtures_are_byte_copies_of_the_plan_tables` and `test_h_implement_protocol_plugin_twins_byte_equal` also passed in the same run.

## Result

`./artifacts/t7-pytest.log`: 274 passed.
