persona: analyzer
model_class: sonnet
reviewer: 1

# Reviewer 1 card (analyzer)
- F1 MAJOR blocking (test-fixture/plan completeness): Task 3 deletes review-panel.default.json but goldens and tests resolve the default by name. tests/review/fixtures/panel-golden-default-live7.json:2-5 keys "default|anthropic-only|first" etc.; tests/review/test_review_panel_exclusion.py:59-62 (packaged_panel(name)); tests/review/test_review_panel_reflect_profile.py:77-79 (for name in ("default", "live7")); tests/review/fixtures/panel-golden-packaged-tiers.json:2; src/superclaude/cli/review/panel.py:433-435. Task 5 does not name the key rename; fix: rename to classic|... and regenerate.
- F2 MAJOR blocking: the tpl fixture tests/review/test_review_panel.py:20-21 (load_panel()) becomes the 3-slot wonsol; :272 expects ["t1b-1","t2-1","t3-1","t3-2"]; :288-290 expects ["t1b-1"]; :306 expects claude-sonnet-5-5 on gateway; :237-240, :217-226, :91-100; tests/review/test_review_cli.py:52-57 and :76. Task 5 names one assertion. Fix: pin tpl to @classic and list the tests.
- F3 MAJOR non-blocking: deleting the file removes @default and template_id default (panel.py:447-455); tests/review/test_review_telemetry.py:29 literal. Keep an alias or state the break.
- F4 MINOR: .dev/tasks/to-do/TASK-WF-makeTheWonsolRev-20261117-130446/TASK-WF-makeTheWonsolRev-20261117-130446.md:80 says tests/unit/test_ccsession_tiers.py matched muse-ember-1.0; reviewer's grep found no match; gateway aliases claude-gw-tier5a/5b/5c[1m] not defined elsewhere.
- F5 MINOR: plugins/superclaude/rules/prompts/document_review_loop_prompts.md mirrors a file Task 6 may edit; Constraints list no plugin path.
calibration_self: 0.8
reviewer_model_self_report: claude-gw-tier1b[1m]
