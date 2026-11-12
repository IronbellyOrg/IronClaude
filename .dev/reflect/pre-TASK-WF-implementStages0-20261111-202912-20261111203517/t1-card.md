# Tier 1 reflection card (UC-1 pre-execution)

- Plan: .dev/tasks/to-do/TASK-WF-implementStages0-20261111-202912/TASK-WF-implementStages0-20261111-202912.md
- Spec (real, pointed to by source.md): .dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md sha256 54a8dce2...c4e45
- Prior T1 pass by the plan author (unvalidated, not independent): .dev/reflect/pre-TASK-WF-implementStages0-20261111-202912-20261111203500/REPORT.md
- coverage_degraded: parsed-sparse (source.md carries no labelled requirement ids; spec has none either, headings are the only structure)
- Tier forced to 2 by `--tier 2`.
- Hypothesis source: orchestrator inline (requirements-analyst not spawned; coverage map built from spec headings and plan tasks).

## Coverage matrix (spec heading span -> plan task)

| Spec span (merged-requirements.md) | Plan task(s) | Status |
|---|---|---|
| Finding format 291-357 | 1, 2, 3, 12, 13 | covered |
| Q4 Engine, K1 contract, templates, forbidden models 187-264 | 8, 9, 10, 11 | covered |
| When the panel is called D1-D5 117-143 | 18 | covered |
| Adapter sketches: Execution contract, Pre adapter, Shadow 358-386 | 17, 19 | covered |
| Staged migration 401-415 (Stages 0-2 exit rows) | 1-20 (exit tooling 5, 20; exit facts 14, 16) | covered, exits need human data |
| Return-contract mapping 416-456 | constraint (1.8.0 unchanged), 15 | covered by constraint only |
| Contract compatibility gate 461-473 | 6, 15, 16 | covered |
| First measurement 522-545 | 4, 7 | covered (design only) |
| Cost model 474-501 | none | unmapped (check if any Stage 0-2 requirement) |
| Risks 502-521 | none | unmapped (check if any Stage 0-2 requirement) |
| Open items 546-560, UNVERIFIED 582-593 | 14 (S-ID only) | partial |

## Leads for reviewers (unverified suspicions, each needs a citation or must be dropped)

- L1: Task 10 acceptance names an `@reflect-pre` resolve that only works after Task 11 ("once Task 11 lands"), so Task 10 cannot be closed on its own acceptance.
- L2: Task 14 acceptance asks for "a clean git status for the probe window" in a worktree that is already dirty (staged and untracked package files).
- L3: Task 19 records `judge_identity` and `judge_class_collision` after the debate; the spec lists the judge-exclusion input and the contract field that carries judge identity as UNVERIFIED (lines 584-585) and no task verifies it.
- L4: Spec Cost model (474-501) and Risks (502-521) may hold Stage 0-2 requirements with no task.
- L5: Task 4 expects 7 null convergence scores; confirm the number exists in the spec or the recorded data.
- L6: Prior pass R-5: Task 19 does not say what shadow does when `panel_parity` is false.
- L7: Task 9 relies on a `launch` field and a `round_robin` strategy and `--sequence`; confirm they exist in `panel.py` and the tiers file; confirm cited line numbers (panel.py 380, 427; panel_cmd.py 18-52; contract.py 47-57, 138; findings.py 90-196, 321-337).
- L8: Task 15 puts a checker into `src/superclaude/cli/reflect/panel_lint.py`; spec names only the test file.

## Calibration inputs

Self-reported confidence: 0.80 (coverage looks complete on headings; details unverified).
