persona: qa
model_class: haiku
reviewer: 2

# Reviewer 2 card (qa)
- F1 MAJOR blocking: existing default-dependent tests missing from Task 5 (tests/review/test_review_panel.py:19-21, :265-290, :303-306, :30-38 vs plan .dev/tasks/to-do/TASK-WF-makeTheWonsolRev-20261117-130446/TASK-WF-makeTheWonsolRev-20261117-130446.md:77-80, :42-47).
- F2 MAJOR blocking: golden migration conflicts with deleting default: .dev/tasks/to-do/TASK-WF-makeTheWonsolRev-20261117-130446/TASK-WF-makeTheWonsolRev-20261117-130446.md:51 vs :77; tests/review/test_review_panel_exclusion.py:53-71 and tests/review/test_review_panel_reflect_profile.py:74-88.
- F3 MAJOR blocking: Task 1 gives anchor alias two models (muse-wonder-1.0 then claude-sonnet-5-5) while source.md:5 says "three single-model tier aliases"; stand-ins only for tier5b, tier5c (.dev/tasks/to-do/TASK-WF-makeTheWonsolRev-20261117-130446/TASK-WF-makeTheWonsolRev-20261117-130446.md:29-33).
- F4 MAJOR blocking: default_template_name() return contract contradicts between Task 4 (.dev/tasks/to-do/TASK-WF-makeTheWonsolRev-20261117-130446/TASK-WF-makeTheWonsolRev-20261117-130446.md:63) and Task 5 (.dev/tasks/to-do/TASK-WF-makeTheWonsolRev-20261117-130446/TASK-WF-makeTheWonsolRev-20261117-130446.md:77).
- F5 MINOR non-blocking: coverage matrix omits requirement spans (source.md:2, :5, :6: PR mechanism, never stage .claude/, plan-only, --depth standard, --handoff none).
calibration_self: 0.94
reviewer_model_self_report: not exposed
