

---
total_diff_points: 12
shared_assumptions_count: 14
---

# Diff Analysis: Opus Architect vs Haiku Architect Roadmaps

## 1. Shared Assumptions and Agreements

Both variants agree on the following foundational elements:

1. **Execution mode is phase-level**, not per-task — both explicitly recommend this scoping
2. **`Phase.execution_mode: str = "claude"`** as the default field addition
3. **`TaskEntry.command: str = ""`** for command extraction
4. **`TaskEntry.classifier`** field for classifier metadata
5. **`PhaseStatus.PREFLIGHT_PASS`** enum addition with `is_success=True`, `is_failure=False`
6. **`subprocess.run(shell=False, capture_output=True, timeout=120)`** as execution mechanism
7. **`shlex.split()`** for command tokenization
8. **Classifier registry** as `CLASSIFIERS: dict[str, Callable[[int, str, str], str]]` with `empirical_gate_v1` built-in
9. **New file `classifiers.py`** under `src/superclaude/cli/sprint/`
10. **`AggregatedPhaseReport.to_markdown()`** reuse for result files — no parser changes
11. **Evidence artifacts** with stdout (10KB), stderr (2KB), exit code, duration, classification
12. **Single-line rollback** as a hard architectural requirement
13. **`click.ClickException`** on invalid execution mode values
14. **Result format compatibility with `_determine_phase_status()`** as the core contract

## 2. Divergence Points

### D-01: Phase Count and Granularity
- **Opus**: 5 phases — combines artifact generation with executor (Phase 3), combines integration with skip mode (Phase 4)
- **Haiku**: 7 phases (0–6) — separates executor (Phase 3) from artifact generation (Phase 4), adds an explicit Phase 0 for architecture confirmation
- **Impact**: Haiku's finer granularity offers clearer milestones and easier checkpoint validation. Opus's consolidated phases reduce coordination overhead but create larger, riskier deliverables per phase.

### D-02: Phase 0 — Architecture Confirmation
- **Opus**: No equivalent phase; jumps directly into data model work
- **Haiku**: Includes a dedicated "Phase 0: Architecture confirmation and design freeze" (0.5 day) to confirm symbol ownership, freeze data model, and resolve open questions before coding
- **Impact**: Haiku's approach reduces rework risk at the cost of a half-day delay. For a 0.55 complexity feature, this may be warranted given the cross-domain nature (parsing, execution, reporting, integration).

### D-03: Preflight Module Placement
- **Opus**: Explicitly creates `src/superclaude/cli/sprint/preflight.py` as a new module
- **Haiku**: States "Preflight executor logic in existing sprint execution module or a tightly scoped new module" — leaves placement open
- **Impact**: Opus is more decisive here. A dedicated `preflight.py` is cleaner for separation of concerns and aligns with the single-line rollback requirement.

### D-04: Test Organization and Counts
- **Opus**: Specifies "14 unit + 8 integration tests" as concrete targets, all in `tests/cli/sprint/test_preflight.py`
- **Haiku**: Describes test categories and coverage areas without committing to specific counts or file structure
- **Impact**: Opus's specificity makes success criteria more measurable. Haiku's flexibility allows test structure to evolve with implementation.

### D-05: Evidence File Path Convention
- **Opus**: Uses `artifacts/<task_id>/evidence.md` consistently
- **Haiku**: Notes "artifacts/D-NNNN/evidence.md or artifacts/<task_id>/evidence.md" — acknowledges ambiguity
- **Impact**: Minor. Both converge on the same structure, but Haiku's hedging suggests the spec's task ID format wasn't fully resolved.

### D-06: PhaseStatus Enum Placement
- **Opus**: Adds to existing enum at "PhaseStatus enum location" (treats as known)
- **Haiku**: Lists "Models/status/reporting definitions" as an impacted area, acknowledges uncertainty about where `PhaseStatus` lives
- **Impact**: Opus assumes more codebase familiarity. Haiku's caution may avoid misplacing the change but signals less certainty.

### D-07: Timeline Presentation
- **Opus**: Uses qualitative labels (Small, Medium, Small-Medium) — avoids day estimates
- **Haiku**: Provides explicit day ranges (0.5–2 days per phase, 6.5–8.5 total)
- **Impact**: Haiku's estimates enable project planning. Opus deliberately avoids commitments, which is consistent with the CLAUDE.md instruction to "avoid giving time estimates."

### D-08: Missing Command Handling in Python-Mode Tasks
- **Opus**: Not explicitly addressed — assumes command will always be present
- **Haiku**: Explicitly calls out "Missing command in a python-mode task should be treated explicitly as failure or validation error"
- **Impact**: Haiku identifies an edge case Opus misses. A python-mode task with no command is a realistic parsing error that should fail fast.

### D-09: Open Question Resolution Style
- **Opus**: Provides a dedicated section with concrete recommendations for all 5 open questions (OQ-001 through OQ-005)
- **Haiku**: Folds open question decisions into Phase 0 work items — defers resolution to the design freeze milestone
- **Impact**: Opus front-loads decisions, enabling parallel implementation sooner. Haiku's deferral is more process-rigorous but delays implementation start.

### D-10: OQ-005 Ordering Constraint Resolution
- **Opus**: Takes a strong position — "preflight runs all python-mode phases in declared order before the loop. If a python phase appears after claude phases in the index, it still runs first — document this explicitly"
- **Haiku**: Does not address ordering semantics beyond stating preflight runs before Claude phases
- **Impact**: Opus identifies a non-obvious behavioral consequence (reordering) and recommends documenting it. This is important for user expectations.

### D-11: Risk Severity Assessments
- **Opus**: Rates classifier bugs as "Low"
- **Haiku**: Rates classifier misclassification as "Low-Medium"
- **Impact**: Minor divergence. Haiku's slightly higher rating reflects concern about downstream promotion/halt decisions — reasonable given classifiers gate phase outcomes.

### D-12: Contingency Planning
- **Opus**: Focuses on architectural mitigations (timeouts as backstops, POSIX-mode note for Windows)
- **Haiku**: Includes explicit contingency actions per risk (e.g., "block release until report generation is aligned; do not patch `_determine_phase_status()`")
- **Impact**: Haiku's contingency plans are more actionable for a team executing the roadmap. Opus's are more architecturally informative.

## 3. Areas Where One Variant Is Clearly Stronger

### Opus is stronger in:
- **Open question resolution** — provides concrete, actionable recommendations for all 5 OQs rather than deferring
- **Ordering semantics** (OQ-005) — identifies and documents the reordering implication
- **File placement decisiveness** — commits to `preflight.py` as a new module
- **Test specificity** — concrete test counts enable clear success/failure criteria
- **Pipe buffer deadlock analysis** — identifies a real risk with `capture_output=True` on nested Claude calls

### Haiku is stronger in:
- **Phase granularity** — separating executor from artifact generation reduces per-phase risk
- **Architecture confirmation phase** — explicit design freeze prevents rework
- **Edge case identification** — missing command in python-mode tasks
- **Contingency planning** — actionable fallback plans per risk
- **Resource requirements** — identifies three distinct roles (engineer, QA, architect/reviewer)
- **Release gate criteria** — explicit ship conditions beyond just "tests pass"

## 4. Areas Requiring Debate to Resolve

1. **Should there be a Phase 0?** Opus's approach starts coding immediately; Haiku's adds a design freeze. For a team with strong codebase familiarity, Phase 0 may be overhead. For cross-team work, it's essential. Recommend: include Phase 0 but timebox to 2 hours, not half a day.

2. **Separate or combined executor + artifact phases?** Opus bundles them (Phase 3); Haiku separates them (Phases 3 & 4). The artifact generation depends tightly on the executor, so testing them separately adds overhead. Recommend: keep combined but add an internal milestone checkpoint.

3. **Missing command handling** — Haiku raises this; Opus doesn't. This needs resolution: should a python-mode task with empty command fail at parse time (validation error) or at execution time (task failure)? Parse-time is safer.

4. **Timeline estimates vs. no estimates** — Opus follows the CLAUDE.md instruction to avoid estimates; Haiku provides them. For roadmap consumers who need to plan, Haiku's approach is more useful. For internal sprint execution by Claude, estimates are irrelevant.

5. **Ordering guarantee documentation** — Opus's recommendation to document that python phases always run first (regardless of index position) needs validation against user expectations. Some users may expect declared order to be preserved across modes.
