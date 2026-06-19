# Research Notes: Per-Phase Turn-Budget Model for the Sprint Runner

**Date:** 2026-06-18
**Scenario:** A (Explicit — fully-specified design spec with exact anchors)
**Depth Tier:** Deep
**Track Count:** 1
**Spec (source of truth):** `.dev/brainstorms/20260618-per-phase-turn-budget/merged-requirements-FINAL.md` (spec_version 3.0)
**Branch:** perPhaseturnBudget
**Status:** Complete

> All `file:line` anchors below were RE-READ LIVE in this worktree on 2026-06-18 during task-builder
> scope discovery and match the FINAL spec exactly. Re-Read each at edit time (the spec itself warns anchors
> can drift).

---

## EXISTING_FILES

### Source files to modify (src/superclaude/cli/sprint/)
- **executor.py** — the sprint runner. Key live anchors (verified 2026-06-18):
  - `1777-1780` — global pre-loop `ledger = TurnLedger(initial_budget=config.max_turns * len(config.active_phases), reimbursement_rate=0.8)` (R-1 DELETE target).
  - `1782` — `shadow_metrics = ShadowGateMetrics()` (R-10 accumulator constructed alongside this; R-1 keeps this neighbor).
  - `1786-1788` `remediation_log`, `1793` `SprintGatePolicy(config)`, `1796` `all_gate_results` — pre-loop infra that MUST stay pre-loop (R-1 "leave neighbors in place").
  - `1813` — `for phase in config.active_phases:` serial loop (K-2 sequential-phase invariant).
  - `1819-1820` python `continue`; `1823-1834` skip `continue` (R-8 — construction sits AFTER these).
  - `1838` — `tasks = _parse_phase_tasks(phase, config)`; `1839` — `if tasks:` (R-2 construct fresh ledger BETWEEN these).
  - `1856-1867` — `execute_phase_tasks(... ledger=ledger ...)` call; `ledger=` @ `1860` (task branch consumer).
  - `2281-2287` — legacy `run_post_phase_wiring_hook(..., ledger=ledger, ...)`; `ledger=ledger` @ `2285` (R-6 / D-3; legacy branch consumer).
  - `2414-2418` — post-loop `build_kpi_report(gate_results=..., remediation_log=..., turn_ledger=ledger)`; `turn_ledger=ledger` @ `2417` (R-10 swap accumulator in).
  - `2419-2420` — `kpi_path = config.results_dir / "gate-kpi-report.md"; kpi_path.write_text(...)` (persisted artifact).
- **models.py** — `TurnLedger` dataclass `1011-1124` (R-7 UNCHANGED — no new method). Field defaults `1024-1034` (`consumed=0, reimbursed=0, wiring_turns_used=0, wiring_turns_credited=0, wiring_budget_exhausted=0, wiring_analyses_count=0`). `__post_init__` RLock `1036-1042`. `available()` `1044-1046` (`initial_budget - consumed + reimbursed`). `debit` monotonicity `1048-1053`. `try_launch` `1066-1081`. `can_run_wiring_gate` `1120-1124`.
- **kpi.py** — `build_kpi_report` signature `151-158` (`turn_ledger: TurnLedger | None = None` @ `156`). Wiring reader `192-197` (`if turn_ledger is not None` @192; reads `.wiring_turns_used` @193, `max(0, .wiring_turns_credited)` @195, `.wiring_analyses_count`→`report.wiring_analyses_run` @197). `GateKPIReport` format `140-143`.
- **commands.py** — `--max-turns` option `~88-92`, help="Max agent turns per phase (default: 100)" (C1 — NO change).

### Test files (tests/sprint/)
- **test_models.py** (exists, 50986 bytes) — `TestTurnLedger` class. Reuse for TM-2, TM-6.
- **test_turn_ledger_concurrency.py** (exists, 1550 bytes) — Reuse for TM-12 (K>1).
- **test_multi_phase.py** (exists, 6292 bytes) — Reuse/promote-to-golden for TM-7 (characterization).
- **test_per_phase_budget.py** — DOES NOT EXIST → NEW file for TM-0, TM-1, TM-5, TM-8, TM-9, TM-10, TM-11, TM-13, TM-14.

## PATTERNS_AND_CONVENTIONS
- UV only: `uv run pytest tests/sprint/... -v` (CLAUDE.md). Never `python -m` / bare `pip`.
- Pytest markers in use; TM-0 requires `@pytest.mark.regression`.
- Source-of-truth is `src/superclaude/` — this is sprint-runner CLI code (NOT a skill/agent/command), so NO `make sync-dev` and NO staging under `.claude/`.
- Feature-branch workflow: work lives on `perPhaseturnBudget`.
- `TurnLedger` is a frozen-shape dataclass; `_lock` is a non-field attr created in `__post_init__` (excluded from `__eq__`/`asdict`).
- Reconciliation pattern: `try_launch` debits `minimum_allocation` (=5) at launch; task helper reconciles to actual at `executor.py:1125-1132` (debit/credit the delta).

## GAPS_AND_QUESTIONS
- NONE. The spec records `oq_status: "OQ-1 RESOLVED (Position A); OQ-2 RESOLVED (hybrid). No open questions remain."` Both prior open questions are adjudicated and applied in-spec (Position A accumulator; hybrid resume wording). No codebase ambiguity surfaced during anchor verification.
- K-3 pre-merge grep (`grep -rn "\.wiring_turns\|\.wiring_analyses\|turn_ledger=" src/superclaude/cli/sprint`) re-run during scope discovery: the ONLY post-loop ledger-wiring consumer remains `executor.py:2417` → `kpi.py:192-197`. Confirms R-10's single arg-swap site.

## RECOMMENDED_OUTPUTS
- ONE MDTM task file (Template 02, complex) under the task dir, design-only, for a FUTURE `/task` execution session. Spec referenced as the authoritative source in frontmatter `spec_path` and `related_docs`.

## SUGGESTED_PHASES
- Phase 1 (Pre-flight / grounding): re-Read anchors live, K-3 pre-merge grep, confirm branch.
- Phase 2 (Source edits — executor.py): R-1 delete global construction; R-10 construct accumulator @1782; R-2 fresh per-phase ledger @1838-1839 with K-2 comment; R-5 gate comment/log strings; R-6 legacy wiring docstring delta; R-10 per-phase add-sites (after 1917 task / after 2287 legacy) + arg swap @2417.
- Phase 3 (Model/docstring touch-ups — models.py): R-7 optional per-instance monotonicity docstring tighten (NO method change).
- Phase 4 (Tests): NEW test_per_phase_budget.py (TM-0,1,5,8,9,10,11,13,14); reuse test_models.py (TM-2,6), test_turn_ledger_concurrency.py (TM-12), test_multi_phase.py (TM-7).
- Phase 5 (Validation): `uv run pytest` the four files; TM-0 mandatory-regression gate.
- Phase 6 (QA + reflect-post + completion).

## TEMPLATE_NOTES
- Template 02 (complex): discovery → edits → tests → validation → QA → completion. Conditional/safety-net behavior (gate-as-net) and per-file granularity (one item per R-/TM-).
- Tier Deep: 3 source files + 4 test files, 10 R-items + 15 TM-items, concurrency + KPI telemetry.
- Granularity: ONE checklist item per R-item (R-1..R-10) and ONE per test-matrix item (TM-0..TM-14), each with its Done-Definition tied to the R-/TM- ID and its anchor.
- Carried risks K-1/K-2/K-3 encoded as DoD notes / explicit items (K-2 construction-site comment; K-3 pre-merge grep item; K-1 documented + pinned by TM-13).

## AMBIGUITIES_FOR_USER
None — intent is clear from the spec and verified codebase. The spec is design-only, fully adjudicated, and every requirement carries an explicit anchor + change + verification. This is a handoff for a FUTURE execution session; the task file must NOT implement now.
