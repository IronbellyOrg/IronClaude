<!-- Merged output. Base: variant-3-original.md (V3, reviewer 3, refactorer). Merge date: 2026-11-17. Plan: refactor-plan.md (6 changes). -->
<!-- Provenance tags: "Base (original)" = unchanged V3 text; "Base (original, modified)" = V3 text altered per plan; "Variant N <ref> per Change #N" = inserted from that variant. -->
persona: refactorer
model_class: opus
reviewer: 3

# Reviewer 3 card (refactorer), merged
<!-- Source: Base (original) F1 -->
- F1 MAJOR blocking: deleting review-panel.default.json breaks goldens calling packaged_panel("default") (.dev/tasks/to-do/TASK-WF-makeTheWonsolRev-20261117-130446/TASK-WF-makeTheWonsolRev-20261117-130446.md:51, :77, :55; tests/review/test_review_panel_exclusion.py:22-23,58-63; panel-golden-default-live7.json:2-5; panel-golden-packaged-tiers.json:2; test_review_panel_reflect_profile.py:77-79); the exclusion golden uses the frozen tier copy so the tier bump does not change it; renaming keys to classic ends the "old resolutions did not move" byte-identity proof unless a frozen copy of the old template is kept.
<!-- Source: Base (original, modified): appended sentence from Variant 1 F2 (test_review_cli.py:52-62,76) per Change #1. Reason: C-002, 85%; V1 range :91-100 deliberately not carried (those tests still pass with a 3-slot template). -->
- F2 MAJOR blocking: tpl fixture (tests/review/test_review_panel.py:19-21) becomes wonsol; about 8 tests hard-code the 4-slot shape (:38, :226, :240, :257, :272, :290, :306); fix: point the fixture at @classic. tests/review/test_review_cli.py:52-62 and :76 also pin the 4-slot ids and a t1b-1 re-review.
<!-- Source: Base (original) F3 -->
- F3 MAJOR non-blocking: existing review-tiers.json overrides (panel.py:470-475, :227-228) lack tier5a-c, so the new default fails for those users; one doc sentence needed.
<!-- Source: Variant 1 F3 (@default removal) per Change #2. Inserted after F3 as the plan directs; id F10 per numbering rule. -->
- F10 MAJOR non-blocking: deleting review-panel.default.json also removes the @default selector and template_id default (panel.py:447-455; tests/review/test_review_telemetry.py:29 literal); the plan states this only implicitly. Keep an alias or state the break.
<!-- Source: Base (original) F4, modified per Change #4 (Variant 2 F4 content; re-grade MINOR -> blocking). Reason: X-002, 2 of 3 advocates said minor but adjudicated blocking because the Task 5 acceptance check cannot pass as written. -->
- F4 MAJOR blocking (re-graded from MINOR): default_template_name() returns a panel (.dev/tasks/to-do/TASK-WF-makeTheWonsolRev-20261117-130446/TASK-WF-makeTheWonsolRev-20261117-130446.md:63) vs the pointer value (.dev/tasks/to-do/TASK-WF-makeTheWonsolRev-20261117-130446/TASK-WF-makeTheWonsolRev-20261117-130446.md:77). Task 4 line 63 and Task 5 line 77 give incompatible return contracts for default_template_name(); the Task 5 acceptance check cannot pass as written.
<!-- Source: Base (original) F5 -->
- F5 MINOR: pointer-switch test cannot swap the data folder (panel.py:423, :439); must patch pnl._default, not default_template_name.
<!-- Source: Base (original) F6 -->
- F6 MINOR: claude-gw-tier5a/5b/5c[1m] aliases not in the launcher registry (ccsession-models.json:71-120); panel.py:671 prints them.
<!-- Source: Base (original) F7 -->
- F7 MINOR: third copy of load/validate logic; _PACKAGED_NAME duplicates _TEMPLATE_ID (panel.py:32, :427); smaller option: DEFAULT_TEMPLATE constant loaded through @ path.
<!-- Source: Base (original) F8 -->
- F8 MINOR: .dev/tasks/to-do/TASK-WF-makeTheWonsolRev-20261117-130446/TASK-WF-makeTheWonsolRev-20261117-130446.md:80 claim about test_ccsession_tiers.py matching muse-ember-1.0 is false.
<!-- Source: Base (original) F9 -->
- F9 MINOR: record template_id continuity (default vs wonsol/classic) in telemetry not stated (source.md:5; tests/review/test_review_telemetry.py:29).
<!-- Source: Variant 1 F5 / Variant 3 advocate (plugin mirror) per Change #3. -->
- F11 MINOR non-blocking: tests/skills/test_review_brief_placement.py:129-134 requires plugins/superclaude/rules/prompts/document_review_loop_prompts.md to be byte-identical to the source rules file; Constraints list no plugins/ path, so a Task 6 edit of that rules file breaks the test. (V1 F5 also cites plugins/superclaude/rules/prompts/document_review_loop_prompts.md as a mirror of a file Task 6 may edit.) Confidence 80% (C-007).
<!-- Source: Variant 2 F3 / X-003 per Change #5. Classified Necessary deviation, non-blocking (V2 F3 blocking rejected: fixed-slot semantics make the anchor deterministic, C-003). -->
- F12 MINOR non-blocking (Necessary deviation): Task 1 gives tier5a two models (muse-wonder-1.0 then claude-sonnet-5-5) against source.md:5 "three single-model tier aliases" (.dev/tasks/to-do/TASK-WF-makeTheWonsolRev-20261117-130446/TASK-WF-makeTheWonsolRev-20261117-130446.md:29-33). resolve_slot makes a fixed slot take the first available model, and the fallback keeps the anthropic-only anchor on Sonnet instead of a Haiku stand-in; the plan should say it departs from the source on purpose. Confidence 75% (C-003).
<!-- Source: Advocate note A-001 per Change #6(a). -->
- F13 MINOR non-blocking: under --strict-distinct a skipped non-anchor seat silently shrinks wonsol to two reviewers (panel.py:647-656).
<!-- Source: Advocate note A-003 per Change #6(b). -->
- F14 MINOR non-blocking: keeping review-panel.default.json as a frozen packaged template, no longer the fallback, would keep the goldens and outside @default users working; the plan did not weigh it.
calibration_self: 0.8
reviewer_model_self_report: claude-gw-tier1a[1m]
