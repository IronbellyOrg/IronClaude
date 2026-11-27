# Calibration of reviewer-3 card (blind calibrator, opus alias)

Calibrated C = 0.84 (Citation grounding 0.90, Coverage completeness 0.75, Deviation-classification clarity 0.80, Risk surface coverage 0.90, Recommendation actionability 0.85). Just below 0.85. No citation was false.

Blocking rows checked with Read: rows 1, 2, 3, 4, 6, 7, 8, 9 true; row 5 partly UNVERIFIED (needs `git ls-files commands/sc-git.md` to settle whether the file is tracked; `tests/docs/test_retired_docs_absent.py:33` does check the filesystem). Spot checks of rows 10 to 15 true.
- Row 1 overstated in two places: Task 27 runs no tests; Task 30's failure on plugin parity not shown. Confirmed: `tests/commands/test_workflow_command.py:204-220`, `tests/skills/test_implement_saved_prompt_rule.py:20,91-93`, `tests/skills/test_review_severity_rule.py:382-396`; Task 26 check (plan 307), Task 31 `-k "implement or ..."`, Task 34 second check (plan 388) fail before Task 38 (plan 426). The calibrator adds that `tests/commands/test_routing_plugin_parity.py:41` (includes `implement`) also breaks between Task 26 and Task 38.
- Row 3: `tests/skills/test_task_workspace_lifecycle.py:611` `_TRANSIENT` has four reasons; lines 684-688 reject any other `E-RESUME-NEEDED reason=` in `retry.md`, `ledger.md`, `SKILL.md`; `refs/retry.md:498`; Task 31 (plan 354) adds two; no task 26-38 updates `_TRANSIENT`.
- Row 6: `archive_workspace.py:44-46` (`_HEADER`) and `:67` (`_ARCH`) left out of Task 9; `refs/ledger.md:127, 232, 238`; implement `SKILL.md:72` writes the header first so a new legacy ledger is header-only; defect comes from DD-8 (`source.md:102`).
- Row 9: label "Blocking (Decision)" but graded MEDIUM (inconsistent).
Unverified: whether `commands/sc-git.md` is tracked and the 21-file count; `tests/hooks/test_launch_level_guard.py` (no line given, not read); "implement does not stage product files" (no citation); `README.md:9`, `source.md:192` not read.
