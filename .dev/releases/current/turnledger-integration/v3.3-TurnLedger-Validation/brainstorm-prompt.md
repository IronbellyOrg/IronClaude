# Release Brainstorm Prompt: v3.3 TurnLedger Validation & Hardening

## Invocation

```
/sc:brainstorm --depth deep --strategy adversarial
```

---

## Preamble: Ground Truth Protocol

**CRITICAL**: Before designing anything, you MUST read the actual code state. Prior analysis artifacts (QA reflections, gap analyses) are STALE — the code has been updated since they were written. The QA reflections report T04 as "skipped" and T02 as "incomplete" — this is NO LONGER TRUE. The architectural refactor is COMPLETE.

### Step 0: Verify Code State (MANDATORY before any design work)

Read these files to establish ground truth:

1. **Sprint executor** — `src/superclaude/cli/sprint/executor.py`
   - Verify `execute_sprint()` constructs: TurnLedger, ShadowGateMetrics, DeferredRemediationLog, SprintGatePolicy, all_gate_results
   - Verify `execute_sprint()` calls `execute_phase_tasks()` for task-inventory phases (v3.1-T04)
   - Verify `execute_sprint()` calls `run_post_phase_wiring_hook()` (v3.2-T02)
   - Verify `execute_sprint()` calls `build_kpi_report()` after phase loop (v3.1-T07)
   - Verify `_parse_phase_tasks()` exists and returns `list[TaskEntry] | None`
   - Verify `_resolve_wiring_mode()` is called (not dead code)
   - Verify `_log_shadow_findings_to_remediation_log()` exists
   - Verify `_format_wiring_failure()` and `_recheck_wiring()` exist
   - Verify BLOCKING path has format → debit → recheck lifecycle

2. **TurnLedger model** — `src/superclaude/cli/sprint/models.py` (offset=487, limit=60)
   - Verify wiring extensions: `debit_wiring()`, `credit_wiring()`, `can_run_wiring_gate()`
   - Verify `wiring_analyses_count` field
   - Verify SprintConfig scope fields: `wiring_gate_enabled`, `wiring_gate_grace_period`, `SHADOW_GRACE_INFINITE`
   - Verify `__post_init__()` derivation logic

3. **Roadmap convergence** — `src/superclaude/cli/roadmap/convergence.py`
   - Verify `DeviationRegistry.merge_findings()` stores `files_affected`
   - Verify `budget_snapshot` field on RunMetadata
   - Verify budget logging in progress messages

4. **Roadmap executor** — `src/superclaude/cli/roadmap/executor.py` (offset=555, limit=80)
   - Verify `load_or_create()` receives 3 args (path, release_id, spec_hash)
   - Verify `merge_findings()` calls pass 3 args (structural, semantic, run_number)
   - Verify `_run_remediation()` converts dicts to Finding objects
   - Verify `TurnLedger(initial_budget=MAX_CONVERGENCE_BUDGET, ...)`
   - Verify wiring-verification `source_dir` points to `src/superclaude`

5. **Pipeline trailing gate** — `src/superclaude/cli/pipeline/trailing_gate.py`
   - Verify `TrailingGateResult` spec-deviation docstring
   - Verify `resolve_gate_mode()`, `DeferredRemediationLog`, `attempt_remediation()` exist

6. **KPI module** — `src/superclaude/cli/sprint/kpi.py`
   - Verify `wiring_analyses_run`, `wiring_remediations_attempted`, `wiring_net_cost` fields
   - Verify `format_report()` includes new fields

7. **Wiring gate** — `src/superclaude/cli/audit/wiring_gate.py`
   - Verify frontmatter contract docstring
   - Verify `check_wiring_report()` wrapper

8. **Test suite** — run `uv run pytest tests/ --tb=short` and record pass/fail counts

Document your findings as a "Code State Snapshot" section in your output before proceeding with design.

---

## Release Objective

Design a comprehensive validation, testing, and hardening release (v3.3) that:

1. **Validates** the sprint executor architectural refactor completed in the prior session
2. **Tests** every wiring point with unit and integration tests
3. **Builds an eval framework** to detect "components built but unreachable" bugs
4. **Closes remaining QA gaps** from v3.05, v3.1, v3.2
5. **Fixes pipeline weaknesses** that allowed these bugs to ship

---

## Workstream 1: Architectural Validation

### Context
The sprint executor was refactored to:
- Construct TurnLedger, ShadowGateMetrics, DeferredRemediationLog, SprintGatePolicy in `execute_sprint()`
- Delegate to `execute_phase_tasks()` when a phase has a task inventory (via `_parse_phase_tasks()`)
- Fall back to `ClaudeProcess` subprocess for freeform-prompt phases
- Call `run_post_phase_wiring_hook()` from both code paths
- Accumulate `TrailingGateResult` objects in `all_gate_results`
- Call `build_kpi_report()` at sprint completion with real data

### Design Questions
- How do we verify the delegation logic is correct for ALL phase types?
- How do we verify `_parse_phase_tasks()` correctly distinguishes task-inventory from freeform phases?
- How do we verify the ClaudeProcess fallback path still works identically to pre-refactor?
- What invariants must hold across both execution paths (per-task vs per-phase)?

### Prior Artifacts (READ BUT VERIFY — may be stale)
- Gap analysis: `.dev/releases/current/turnledger-integration/v3.1/roadmap-gap-analysis-merged.md`
- Gap remediation tasklist: `.dev/releases/current/turnledger-integration/v3.1/gap-remediation-tasklist.md` (T04 details)
- QA reflection: `.dev/releases/current/turnledger-integration/v3.1/execution-qa-reflection.md` (**STALE** — reports T04 as skipped)

---

## Workstream 2: Unit Test Coverage

### Wiring Points to Test

| Wiring Point | Source | Target | What to Assert |
|-------------|--------|--------|----------------|
| TurnLedger construction | `execute_sprint()` | `TurnLedger.__init__` | Budget = `max_turns * len(active_phases)`, rate = 0.8 |
| ShadowGateMetrics construction | `execute_sprint()` | `ShadowGateMetrics.__init__` | Constructed before phase loop |
| DeferredRemediationLog construction | `execute_sprint()` | `DeferredRemediationLog.__init__` | `persist_path` under `results_dir` |
| SprintGatePolicy construction | `execute_sprint()` | `SprintGatePolicy.__init__` | Receives `config` |
| Phase delegation | `execute_sprint()` | `execute_phase_tasks()` | Called when `_parse_phase_tasks()` returns tasks |
| Phase fallback | `execute_sprint()` | `ClaudeProcess` | Called when `_parse_phase_tasks()` returns None |
| Post-phase wiring hook | `execute_sprint()` | `run_post_phase_wiring_hook()` | Called for EVERY phase (both paths) |
| Anti-instinct hook returns | `run_post_task_anti_instinct_hook()` | `TrailingGateResult` | Returns tuple, not bare TaskResult |
| Gate result accumulation | phase loop | `all_gate_results` | Extends after each phase |
| Failed gate → remediation log | phase loop | `remediation_log.append()` | Only for `not gr.passed` |
| KPI report call | after phase loop | `build_kpi_report()` | Receives `all_gate_results`, `remediation_log`, `ledger` |
| KPI report write | after phase loop | `gate-kpi-report.md` | Written to `results_dir` |
| Wiring mode resolution | `run_post_task_wiring_hook()` | `_resolve_wiring_mode()` | Not `config.wiring_gate_mode` directly |
| Shadow findings → remediation log | shadow mode | `_log_shadow_findings_to_remediation_log()` | Called with findings |
| BLOCKING remediation lifecycle | full mode | `_format_wiring_failure()` → debit → `_recheck_wiring()` | Full cycle |
| Convergence registry args | `_run_convergence_spec_fidelity()` | `load_or_create(path, release_id, spec_hash)` | 3 args |
| Convergence merge args | `_run_checkers()` | `merge_findings(structural, [], run_number)` | 3 args, correct positions |
| Convergence remediation | `_run_remediation()` | dict → Finding conversion | No AttributeError |
| Budget constants | `_run_convergence_spec_fidelity()` | `TurnLedger(MAX_CONVERGENCE_BUDGET, ...)` | 61, not 46 |

### Missing Test Files (from v3.05 QA)
- `tests/roadmap/test_convergence_wiring.py` — 7 integration tests for `_run_convergence_spec_fidelity()` wiring
- `tests/roadmap/test_convergence_e2e.py` — 6 E2E tests for success criteria SC-1 through SC-6

---

## Workstream 3: Integration Tests

### TurnLedger Lifecycle Tests
Prove the full debit/credit/reimbursement cycle flows through production:

1. **Convergence path** (v3.05): `execute_fidelity_with_convergence()` → debit CHECKER_COST → run checkers → credit CONVERGENCE_PASS_CREDIT → reimburse_for_progress
2. **Sprint per-task path** (v3.1): `execute_sprint()` → `execute_phase_tasks()` → hooks → debit/credit
3. **Sprint per-phase path** (v3.2): `execute_sprint()` → ClaudeProcess → `run_post_phase_wiring_hook()` → `debit_wiring()` → `credit_wiring()`
4. **Cross-path**: Sprint with mixed phases (some task-inventory, some freeform) — verify ledger state is coherent across both paths

### End-to-End Scenarios
- Sprint with `gate_rollout_mode="shadow"`: verify metrics recorded, no status changes
- Sprint with `gate_rollout_mode="soft"`: verify reimbursement on PASS, warnings on FAIL
- Sprint with `gate_rollout_mode="full"`: verify FAIL propagation, remediation lifecycle
- Sprint with `gate_rollout_mode="off"`: verify no analysis, no budget impact
- Sprint interrupted mid-execution: verify KPI report still written, remediation log persisted

---

## Workstream 4: Reachability Eval Framework

### The Bug Class
The v3.1/v3.2 gap analyses discovered a recurring pattern: **components are built (classes defined, helper functions written, tests pass in isolation) but never wired into the production entry point** (`execute_sprint()`). This is the "components built but unreachable" bug class.

### Detection Approach Options
Brainstorm at least 3 approaches:

**A. Static call-chain analysis**: Parse the AST of `execute_sprint()` and trace all reachable functions. Compare against a "required reachability set" declared in the spec. Any spec-required function NOT in the call chain = gap.

**B. Runtime instrumentation**: Monkey-patch key functions with call counters during integration tests. After test execution, assert all expected functions were called at least once.

**C. Import/symbol analysis**: For each module that declares public symbols, verify each symbol has at least one production call site (not just test call sites). This catches `SprintGatePolicy`-style dead definitions.

**D. Spec-driven wiring manifest**: Each release spec declares a `wiring_manifest` section listing every function → call-site pair. The eval framework reads this manifest and verifies each pair with `ast.parse()` + `ast.walk()`.

### Prior Analysis
- Pipeline weakness analyses identified this gap across all 3 releases:
  - `.dev/releases/current/turnledger-integration/v3.05/pipeline-weakness-analysis.md`
  - `.dev/releases/current/turnledger-integration/v3.1/pipeline-weakness-analysis.md`
  - `.dev/releases/current/turnledger-integration/v3.2/pipeline-weakness-analysis.md`

---

## Workstream 5: Remaining QA Gaps

### v3.05 Gaps (from execution-qa-reflection.md — VERIFY AGAINST CODE)
- T07: `tests/roadmap/test_convergence_wiring.py` — 7 tests for registry construction, merge_findings, dict access, budget params, E2E pass/fail
- T08: Wiring-verification `source_dir` — may already be fixed (verify `executor.py:429`)
- T10: PASS log message missing budget info (partially done)
- T11: `tests/roadmap/test_convergence_e2e.py` — 6 tests for SC-1 through SC-6
- T12: Smoke test convergence path
- T14: Regenerate wiring-verification artifact

### v3.2 Gaps (from execution-qa-reflection.md — VERIFY AGAINST CODE)
- T02: `run_post_phase_wiring_hook()` call in `execute_sprint()` — may already be wired (VERIFY)
- T17-T22: All verification tasks (integration tests, regression suite, gap closure audit)

---

## Workstream 6: Pipeline Weakness Fixes

### Weaknesses Identified (cross-release consensus)

| # | Weakness | Severity | Fix |
|---|----------|----------|-----|
| 1 | Wiring verification targets markdown dir, not source | CRITICAL | Change `source_dir` in `executor.py:429` — **may already be fixed (VERIFY)** |
| 2 | No call-chain reachability gate | CRITICAL | New pipeline gate: parse AST, verify spec-required functions are reachable from entry points |
| 3 | 0-files-analyzed produces silent PASS | CRITICAL | Add assertion: `files_analyzed > 0` or FAIL |
| 4 | Spec-fidelity checks roadmap-vs-spec, never impl-vs-spec | HIGH | New pipeline stage or eval: compare implementation against spec declarations |
| 5 | Convergence mode disables spec-fidelity gate | CRITICAL | Remove `gate=None` bypass when `convergence_enabled=True` |

### Prior Analysis
- `.dev/releases/current/turnledger-integration/v3.05/pipeline-weakness-analysis.md` (5 weaknesses)
- `.dev/releases/current/turnledger-integration/v3.1/pipeline-weakness-analysis.md` (5 weaknesses)
- `.dev/releases/current/turnledger-integration/v3.2/pipeline-weakness-analysis.md` (5 weaknesses)

---

## Additional Context Files

### Original Specs (for validation against)
- v3.05: `.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- v3.1: `.dev/releases/backlog/v3.1_Anti-instincts__/anti-instincts-gate-unified.md`
- v3.2: `.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md`

### Gap Analysis Reports (authoritative for what bugs were found)
- v3.05: `.dev/releases/current/turnledger-integration/v3.05/roadmap-gap-analysis-merged.md`
- v3.1: `.dev/releases/current/turnledger-integration/v3.1/roadmap-gap-analysis-merged.md`
- v3.2: `.dev/releases/current/turnledger-integration/v3.2/roadmap-gap-analysis-merged.md`

### Gap Remediation Tasklists (what was planned to fix)
- v3.05: `.dev/releases/current/turnledger-integration/v3.05/gap-remediation-tasklist.md` (15 tasks)
- v3.1: `.dev/releases/current/turnledger-integration/v3.1/gap-remediation-tasklist.md` (14 tasks)
- v3.2: `.dev/releases/current/turnledger-integration/v3.2/gap-remediation-tasklist.md` (22 tasks)

### QA Reflections (STALE — code updated since these were written)
- v3.05: `.dev/releases/current/turnledger-integration/v3.05/execution-qa-reflection.md`
- v3.1: `.dev/releases/current/turnledger-integration/v3.1/execution-qa-reflection.md`
- v3.2: `.dev/releases/current/turnledger-integration/v3.2/execution-qa-reflection.md`

### Test Files (existing coverage)
- `tests/sprint/test_executor.py` — core executor tests
- `tests/sprint/test_anti_instinct_sprint.py` — anti-instinct hook tests
- `tests/sprint/test_e2e_trailing.py` — trailing gate E2E
- `tests/sprint/test_kpi_report.py` — KPI builder tests
- `tests/sprint/test_backward_compat_regression.py` — backward compat
- `tests/roadmap/test_convergence.py` — convergence engine tests
- `tests/pipeline/test_trailing_gate.py` — trailing gate infrastructure
- `tests/pipeline/test_full_flow.py` — pipeline flow tests
- `tests/integration/test_sprint_wiring.py` — wiring hook integration

---

## Output Format

Produce a release specification with:

1. **Code State Snapshot** — verified findings from Step 0
2. **Release Scope** — what's in/out
3. **Phased Implementation Plan** — ordered by dependency
4. **Test Matrix** — every test to write, mapped to wiring point
5. **Eval Framework Design** — chosen approach + specification
6. **Pipeline Fix Specification** — exact changes to each pipeline component
7. **Risk Assessment** — what could go wrong with each workstream
8. **Success Criteria** — measurable conditions for release completion
9. **Estimated Effort** — per workstream

---

## Constraints

- **UV only** — `uv run pytest`, not `python -m pytest`
- **No mock-free evals** — evals must be third-party verifiable (per project feedback memory)
- **Branch**: create from current `v3.0-v3.2-Fidelity` branch
- **Test baseline**: 4858 passed, 3 pre-existing failures, 0 regressions
- **Do NOT modify production code** in this brainstorm — design only
