# BUILD REQUEST

Source: user
SPEC: .dev/brainstorms/20260618-per-phase-turn-budget/merged-requirements-FINAL.md

GOAL: Build a design-only MDTM task file that, when later executed via /task, implements the
per-phase turn-budget model for the sprint runner per the FINAL spec (spec_version 3.0). The task file
must cover every requirement R-1..R-10, every test-matrix item TM-0..TM-14, and the three carried risks
K-1/K-2/K-3 — each as a granular checklist item or explicit Done-Definition note tied to its R-/TM-/K- ID
and its live file:line anchor. This is a HANDOFF for a FUTURE execution session on branch perPhaseturnBudget.
Do NOT implement now.

WHY: `run_sprint` builds ONE global TurnLedger before the phase loop sized
`max_turns * len(active_phases)` (executor.py:1777-1780) and shares it across all phases, contradicting the
documented "Max agent turns per phase" unit (commands.py:92). A heavy early phase drains the shared pool and
later phases get SKIPPED tasks → PhaseStatus.ERROR (observed: 3 phases × max_turns 100 errored at phase 5/6).
The fix gives each phase a fresh ledger sized max_turns × len(tasks), making per-phase independence structural,
while a read-only sprint-level wiring accumulator preserves the sprint-cumulative KPI telemetry contract in
gate-kpi-report.md (the post-loop build_kpi_report at executor.py:2414-2418 reads kpi.py:192-197).

TASK_ID_PREFIX: TASK-RF

TEMPLATE: 02
# Complex: discovery → source edits → tests → validation → QA → completion. Conditional safety-net behavior,
# per-file granularity, concurrency + KPI-telemetry subsystems.

QA_INTENSITY: standard

QA_GATE_REQUIREMENTS: FINAL_ONLY
# One final QA validation gate before task completion. Standard intensity (per I22): minimum 7 agents
# (3 rf-qa structural + 3 rf-qa-qualitative content + 1 domain). Encode each agent as its own `- [ ]` item
# with a fully embedded lens-specific prompt, serialized fix authorization (M3/I20), adversarial framing.
# The generated task file is code+tests (not a >500-line document and not a source-material transformation),
# so an M4/I21 source-document fidelity gate is NOT applicable here — do not add one.

VALIDATION_REQUIREMENTS: UV-only test execution is the validation surface.
  `uv run pytest tests/sprint/test_per_phase_budget.py tests/sprint/test_models.py::TestTurnLedger
   tests/sprint/test_turn_ledger_concurrency.py tests/sprint/test_multi_phase.py -v` must pass.
  Also: `make lint` clean on touched files. NEVER python -m or bare pip. NEVER stage anything under .claude/.

TESTING_REQUIREMENTS: UNIT + INTEGRATION
  Test files: NEW tests/sprint/test_per_phase_budget.py (TM-0,1,5,8,9,10,11,13,14); reuse existing
  tests/sprint/test_models.py::TestTurnLedger (TM-2, TM-6), tests/sprint/test_turn_ledger_concurrency.py
  (TM-12), tests/sprint/test_multi_phase.py (TM-7, promote to golden). TM-0 is the MANDATORY regression test
  carrying @pytest.mark.regression. Each TM-item is its own checklist item with the exact assertion from the
  spec's §6 Test Matrix as its Done-Definition.

POST_REFLECT_GATE: ENABLED
  TASK_FILE: .dev/tasks/to-do/TASK-RF-per-phase-turn-budget-20260618-160752/TASK-RF-per-phase-turn-budget-20260618-160752.md

EXECUTION_CONTEXT_INSTRUCTION: Populate the `## Execution Context` section:
  - References: BUILD_REQUEST GOAL verbatim; WHY summary; spec merged-requirements-FINAL.md (R-1..R-10,
    TM-0..TM-14, K-1/K-2/K-3); seed-brief.md; PANEL-REVIEW.md; reflect-pre-spec.md.
  - Source areas: sprint runner executor (run_sprint phase loop + legacy branch + post-loop KPI build),
    TurnLedger model, KPI report builder, sprint test suite. NAME THESE AS MODULES — no file:line in the header.
  - Key constraints: design-only (do not implement now); UV-only test execution; never stage .claude/;
    TurnLedger model itself is UNCHANGED (no new method); accumulator is read-only (no shared budget pool).

DOCUMENTATION STALENESS WARNINGS:
  None. Every file:line anchor in the spec was RE-READ LIVE in this worktree on 2026-06-18 during scope
  discovery and matches exactly: executor.py 1777-1780 / 1782 / 1813 / 1819-1834 / 1838-1839 / 1856-1867
  (ledger= @1860) / 2281-2287 (ledger= @2285) / 2414-2418 (turn_ledger=ledger @2417) / 2419-2420;
  models.py TurnLedger 1011-1124 (available() 1044-1046, defaults 1024-1034, RLock 1036-1042); kpi.py
  build_kpi_report 151-158 (turn_ledger @156), wiring reader 192-197; commands.py ~88-92 (--max-turns help
  "Max agent turns per phase"). NOTE the spec warns REPORT.md anchors 1651-1653/1119-1130 are DRIFTED — the
  live anchors are 1777-1780 / 1125-1132. Use ONLY the spec's verified live anchors, never the drifted ones.

RESEARCH DIR: .dev/tasks/to-do/TASK-RF-per-phase-turn-budget-20260618-160752/research/
  (research-notes.md at the task dir root carries the full verified anchor map; the spec file itself is the
   primary research artifact — read merged-requirements-FINAL.md in full.)

OPEN QUESTIONS: None — OQ-1 (Position A accumulator) and OQ-2 (hybrid resume wording) are RESOLVED in-spec.

GRANULARITY REQUIREMENT: ONE checklist item per R-item (R-1..R-10) in the source-edit phases, and ONE per
  test-matrix item (TM-0..TM-14) in the test phase. Do NOT batch ("apply all R-items" / "write all tests").
  Each item's Context must cite the live anchor; each item's Done-Definition/Verification must restate the
  spec's verification clause for that R-/TM- ID. Carried risks: K-2 → construction-site comment item (R-2);
  K-3 → pre-merge grep item near the end of edits; K-1 → DoD note on R-6 + pinned by TM-13.

CRITICAL — DESIGN-ONLY HANDOFF: The generated task file describes WHAT a future executor will do. It is not
  executed in this session. Items must be self-contained (B2), evidence-anchored, and reference
  merged-requirements-FINAL.md as the spec. Do NOT stage or commit anything under .claude/.
