persona: refactorer
model_class: opus
reviewer: 3

# Reviewer 3 card (refactorer)
- F1 MAJOR blocking: deleting review-panel.default.json breaks goldens calling packaged_panel("default") (.dev/tasks/to-do/TASK-WF-makeTheWonsolRev-20261117-130446/TASK-WF-makeTheWonsolRev-20261117-130446.md:51, :77, :55; tests/review/test_review_panel_exclusion.py:22-23,58-63; panel-golden-default-live7.json:2-5; panel-golden-packaged-tiers.json:2; test_review_panel_reflect_profile.py:77-79); the exclusion golden uses the frozen tier copy so the tier bump does not change it; renaming keys to classic ends the "old resolutions did not move" byte-identity proof unless a frozen copy of the old template is kept.
- F2 MAJOR blocking: tpl fixture (tests/review/test_review_panel.py:19-21) becomes wonsol; about 8 tests hard-code the 4-slot shape (:38, :226, :240, :257, :272, :290, :306); fix: point the fixture at @classic.
- F3 MAJOR non-blocking: existing review-tiers.json overrides (panel.py:470-475, :227-228) lack tier5a-c, so the new default fails for those users; one doc sentence needed.
- F4 MINOR: default_template_name() returns a panel (.dev/tasks/to-do/TASK-WF-makeTheWonsolRev-20261117-130446/TASK-WF-makeTheWonsolRev-20261117-130446.md:63) vs the pointer value (.dev/tasks/to-do/TASK-WF-makeTheWonsolRev-20261117-130446/TASK-WF-makeTheWonsolRev-20261117-130446.md:77).
- F5 MINOR: pointer-switch test cannot swap the data folder (panel.py:423, :439); must patch pnl._default, not default_template_name.
- F6 MINOR: claude-gw-tier5a/5b/5c[1m] aliases not in the launcher registry (ccsession-models.json:71-120); panel.py:671 prints them.
- F7 MINOR: third copy of load/validate logic; _PACKAGED_NAME duplicates _TEMPLATE_ID (panel.py:32, :427); smaller option: DEFAULT_TEMPLATE constant loaded through @ path.
- F8 MINOR: .dev/tasks/to-do/TASK-WF-makeTheWonsolRev-20261117-130446/TASK-WF-makeTheWonsolRev-20261117-130446.md:80 claim about test_ccsession_tiers.py matching muse-ember-1.0 is false.
- F9 MINOR: record template_id continuity (default vs wonsol/classic) in telemetry not stated (source.md:5; tests/review/test_review_telemetry.py:29).
calibration_self: 0.8
reviewer_model_self_report: claude-gw-tier1a[1m]
