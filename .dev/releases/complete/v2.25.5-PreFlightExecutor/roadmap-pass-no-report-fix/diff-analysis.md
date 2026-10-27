---
total_diff_points: 12
shared_assumptions_count: 18
---

## Shared Assumptions and Agreements

1. **Root cause**: `PASS_NO_REPORT` occurs when `exit_code == 0` but no agent-written result file exists; fix is a deterministic executor-side fallback.
2. **Solution approach**: "Option D" — `_write_preliminary_result()` called before `_determine_phase_status()`.
3. **Function signature**: `(config: SprintConfig, phase: Phase, started_at: float) -> bool`
4. **Sentinel content**: Exactly `EXIT_RECOMMENDATION: CONTINUE\n`
5. **Freshness guard**: `exists() AND st_size > 0 AND st_mtime >= started_at` → no-op, return `False`
6. **Zero-byte treatment**: Treated as absent; overwritten with sentinel.
7. **Stale file treatment**: Overwritten with sentinel.
8. **Error handling**: `try/except OSError` → WARNING log, return `False`, no exception raised.
9. **Injection guard**: `if exit_code == 0` only.
10. **Ordering invariant**: `_write_preliminary_result()` → `_determine_phase_status()` → `_write_executor_result_file()` is non-negotiable.
11. **No signature change**: `_determine_phase_status()` signature remains untouched.
12. **Enum preservation**: `PhaseStatus.PASS_NO_REPORT` stays in enum and remains reachable via direct calls.
13. **Non-zero paths**: TIMEOUT, ERROR, INCOMPLETE, PASS_RECOVERED paths entirely untouched.
14. **Preflight isolation**: Python/skip phases never reach new code.
15. **Prompt injection**: `## Result File` appended as last `##` section in `build_prompt()`.
16. **Modified files**: `executor.py`, `process.py`, `test_executor.py`, `test_phase8_halt_fix.py`.
17. **No new dependencies**: stdlib only (`pathlib`, `os`, `logging`, `datetime`).
18. **TOCTOU risk acknowledged**: Single-threaded assumption documented; `O_EXCL` deferred to future parallel work.

---

## Divergence Points

### 1. Phase numbering and phase count

- **Opus**: 5 phases (P1–P5), starting from "Phase 1"
- **Haiku**: 6 phases (Phase 0–Phase 5), with an explicit "Phase 0" for baseline/reconnaissance
- **Impact**: Haiku's Phase 0 elevates pre-implementation verification to a named milestone with a delivery estimate (0.25 phase-days), making it a trackable unit of work. Opus folds the same work into Phase 1 without a separate milestone or estimate. Haiku's approach reduces the risk of skipping baseline validation under schedule pressure.

### 2. Timeline quantification

- **Opus**: Qualitative effort labels only (Small / Medium / Small / Small)
- **Haiku**: Explicit phase-day estimates (0.25 / 0.5 / 0.25 / 0.25 / 0.75 / 0.5 = 2.5 phase-days total)
- **Impact**: Haiku provides actionable scheduling data. Opus avoids potentially misleading precision. Haiku's estimates are more useful for sprint planning; Opus's labels avoid false confidence on uncertain estimates.

### 3. Test phase placement

- **Opus**: Tests written within the same phase as each implementation step (P2 writes unit tests, P3 writes integration tests, P4 writes prompt test)
- **Haiku**: Tests consolidated into a dedicated Phase 4 after all implementation phases complete
- **Impact**: Opus's interleaved approach validates each increment before proceeding — faster feedback loop, lower risk of compound errors. Haiku's consolidated approach risks encoding incorrect assumptions in tests written after implementation but offers a cleaner separation of concerns.

### 4. Stale file overwrite coverage as a distinct test case

- **Opus**: T-006 explicitly named and assigned to P3 (stale HALT from prior run → overwritten with CONTINUE)
- **Haiku**: Covered in Phase 4 test matrix but not assigned a named test identifier
- **Impact**: Minor. Both cover the scenario. Opus's explicit T-006 label makes traceability to spec success criteria cleaner.

### 5. Debug telemetry detail

- **Opus**: Log result as `option_d` vs `option_a_or_noop` (domain-specific terminology from spec)
- **Haiku**: Log as `executor-preliminary` vs `agent-written/no-op` (semantic description)
- **Impact**: Haiku's labels are more self-explanatory in log output for operators unfamiliar with internal naming conventions. Opus's labels map directly to spec option identifiers, useful for debugging against the spec.

### 6. `mkdir` behavior specification

- **Opus**: Explicitly calls out `mkdir(parents=True, exist_ok=True)` before write
- **Haiku**: States "Create parent directory if needed" without specifying flags
- **Impact**: Opus is more precise and directly implementable. Haiku's phrasing is sufficient guidance but leaves flag selection to the implementer.

### 7. Insertion point specification for `_write_preliminary_result()` in source

- **Opus**: "after `_write_crash_recovery_log()`, before `_write_executor_result_file()`" — position relative to neighboring functions
- **Haiku**: No equivalent insertion position guidance for function definition placement
- **Impact**: Opus provides more actionable guidance for the implementer. Haiku leaves file organization to discretion.

### 8. Open questions (OQ) tracking

- **Opus**: Explicitly tracks 8 named open questions (OQ-001 through OQ-008) with Phase 1 tasks to resolve each
- **Haiku**: Resolves the same concerns implicitly under "Verify key structural assumptions" without named identifiers
- **Impact**: Opus's named OQ tracking is more rigorous for a spec-driven workflow where questions need to be closed before code changes. Haiku is lighter and faster for an experienced implementer.

### 9. Sentinel contract comment in `_determine_phase_status()`

- **Opus**: Explicitly calls out adding a sentinel contract comment at the CONTINUE parsing point in Phase 2 (NFR-006)
- **Haiku**: Mentions documenting sentinel contract in Phase 5 "implementation notes" and classifier comment, but not as a discrete code-change task
- **Impact**: Opus's placement of this documentation task earlier (P2) ensures the contract is captured alongside the implementation, not as a post-hoc note. Haiku's Phase 5 placement risks omission if Phase 5 is time-compressed.

### 10. Architectural recommendation section

- **Haiku**: Includes an explicit "Architect Recommendation Summary" section with 5 principles (keep fix narrow, treat sequencing as architecture, preserve authority boundaries, document concurrency debt, test full file-state matrix)
- **Opus**: No equivalent synthesis section; principles are distributed across phase descriptions and risk table
- **Impact**: Haiku's summary section is valuable for architectural review and onboarding; provides a single-page decision rationale. Opus requires reading the full document to extract the same principles.

### 11. Resource requirements: team roles

- **Haiku**: Explicitly specifies 3 roles (1 backend/CLI engineer, 1 QA reviewer, lightweight architecture review)
- **Opus**: No team role specification
- **Impact**: Haiku is more useful for project management and staffing. Opus assumes a single implementer, which may be accurate for this scope but leaves resourcing implicit.

### 12. Success criteria layering

- **Opus**: 13 named success criteria (SC-001 through SC-013) cross-referenced to phases and tests
- **Haiku**: 13 equivalent criteria organized into 5 semantic layers (Functional / Backward Compatibility / Prompt Contract / validation approach layers)
- **Impact**: Opus's numbered SC references enable direct traceability from test to criterion. Haiku's layered structure is more readable for review but requires manual mapping to test IDs.

---

## Areas Where One Variant Is Clearly Stronger

**Opus is stronger in:**
- Spec traceability — explicit OQ/FR/SC/T/RISK identifiers throughout enable precise cross-referencing
- Implementation precision — `mkdir(parents=True, exist_ok=True)`, function insertion position, exact test names
- Incremental validation — tests written within each phase prevent compound assumption errors
- Sentinel contract documentation timing — captured in P2 alongside the implementation, not deferred

**Haiku is stronger in:**
- Timeline concreteness — 2.5 phase-day estimate is actionable for sprint planning
- Architectural synthesis — "Architect Recommendation Summary" provides a clean decision rationale
- Log label readability — `executor-preliminary` vs `agent-written/no-op` is more operator-friendly
- Team/resourcing clarity — explicit role specifications
- Validation layering — 5-layer validation approach is a clearer quality gate framework

---

## Areas Requiring Debate to Resolve

1. **Test placement strategy**: Interleaved (Opus) vs. consolidated (Haiku). The interleaved approach provides faster feedback but increases phase complexity. The consolidated approach is cleaner but risks encoding errors. Resolution should be driven by team familiarity with the codebase.

2. **Open question tracking formalism**: Named OQ identifiers (Opus) vs. implicit checklist (Haiku). For a spec with known unknowns, named tracking is safer. Debate: does the overhead of OQ management add value for a 2–3 day patch?

3. **Debug log terminology**: `option_d`/`option_a_or_noop` vs. `executor-preliminary`/`agent-written/no-op`. Both are valid; a merge should pick one convention and apply it consistently. The spec's own terminology (Option D) suggests Opus's labels have better spec alignment.

4. **Sentinel contract comment timing**: P2 (Opus) vs. P5 (Haiku). Given the risk of omission under time pressure, Opus's earlier placement is defensible. However, if the comment requires understanding the full implementation context, P5 may produce a higher-quality comment.
