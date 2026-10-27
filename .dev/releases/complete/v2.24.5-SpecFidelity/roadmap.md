---
spec_source: v2.25.1-release-spec.md
complexity_score: 0.5
adversarial: true
---

# Roadmap: v2.24.5 SpecFidelity — Tools Default & Arg-Too-Long Fixes

## Executive Summary

This release delivers two independent bug fixes sharing a single delivery mechanism (`build_command()`):

1. **FIX-001**: Add `--tools default` to subprocess commands so Claude can discover tool schemas (TodoWrite, Bash, etc.) during pipeline execution.
2. **FIX-ARG-TOO-LONG**: Replace a hardcoded 200 KB embed limit with a kernel-derived 120 KB constant and guard the full composed prompt string, preventing `OSError [Errno 7]` crashes.

A **Phase 0 blocking gate** determines whether `--file` fallback works at all, branching the plan into two completion scenarios. This gate runs first because it collapses the largest ambiguity in the release — without it, later test passes could give false confidence while the oversized-input fallback remains non-functional. Prior fallback behavior may have produced misleadingly "successful" but context-incomplete runs.

Total scope: 4–8 files, ~50 lines of production code, ~80 lines of test code.

### Delivery Objectives

1. Satisfy all 15 extracted requirements without scope expansion.
2. Preserve backward compatibility and avoid new imports per NFR-001.2 and NFR-ATL.1.
3. Convert the current failure mode from crash to deterministic fallback per NFR-ATL.2.
4. Produce third-party verifiable evidence for the blocking `--file` behavior decision.

---

## Phased Implementation Plan

### Phase 0 — Empirical Validation Gate (BLOCKING)

**Objective**: Determine if `claude --print --file /path` delivers file content to the model.

**Why this is blocking**: This phase is mandatory because it collapses the largest ambiguity in the release. The `--file` behavior determines downstream implementation scope (Phase 1.5 activation), validation strategy, and release risk. Without empirical evidence, later test passes could mask non-functional fallback paths.

| Step | Action | Requirement |
|------|--------|-------------|
| 0.1 | Verify CLI prerequisite: `claude --print -p "hello" --max-turns 1` exits 0 | FR-ATL.5-IMPLICIT |
| 0.2 | Run PINEAPPLE sentinel test: write unique token to temp file, invoke `claude --print --file /tmp/sentinel.txt`, check output contains token | FR-ATL.5a |
| 0.3 | Record result as **WORKING** or **BROKEN** with full evidence (command, output, exit code, timestamp) | FR-ATL.5a |

**Gate Decision**:
- **WORKING** → Phase 1.5 is N/A, proceed to Phases 1.1/1.2
- **BROKEN** → Phase 1.5 activates after Phase 1.2

**Milestone**: Phase 0 result documented. All subsequent phases unblocked.

---

### Phase 1.1 — FIX-001: `--tools default` Flag

**Objective**: Enable tool schema discovery in all `ClaudeProcess` subprocesses.

**Why this phase is early**: This is a low-surface, high-leverage fix that directly addresses sprint execution failures. Landing it early reduces ambiguity in later integrated validation.

| Step | Action | Requirement |
|------|--------|-------------|
| 1.1.1 | Read `ClaudeProcess.build_command()` and all subclasses to confirm no `super()` bypasses | Risk 3 |
| 1.1.2 | Add `"--tools", "default"` between `--no-session-persistence` and `--max-turns` in `build_command()` | FR-001.1 |
| 1.1.3 | Verify all pre-existing flags unchanged, `extra_args` passthrough intact | FR-001.2 |
| 1.1.4 | Run `uv run pytest tests/pipeline/test_process.py -v` — all existing tests pass (update positional assertions if needed) | Risk 4, NFR-001.2 |

**Files touched**: `src/superclaude/cli/pipeline/process.py`

**Parallelism**: Runs in parallel with Phase 1.2 (different files, no shared code paths).

**Milestone**: `--tools default` in all inherited `build_command()` calls.

---

### Phase 1.2 — FIX-ARG-TOO-LONG: Constants & Guard

**Objective**: Replace magic numbers with derived constants and guard the full composed prompt.

**Why this ordering**: The guard refactor addresses a correctness defect with direct operational failure impact. It is independent of Phase 1.1 at the file level, enabling parallel implementation.

| Step | Action | Requirement |
|------|--------|-------------|
| 1.2.1 | Define three module-level constants in `executor.py`: `_MAX_ARG_STRLEN = 128 * 1024`, `_PROMPT_TEMPLATE_OVERHEAD = 8 * 1024`, `_EMBED_SIZE_LIMIT = _MAX_ARG_STRLEN - _PROMPT_TEMPLATE_OVERHEAD` | FR-ATL.1 |
| 1.2.2 | Add `assert _PROMPT_TEMPLATE_OVERHEAD >= 4096` with rationale message immediately after definitions | FR-ATL.1 |
| 1.2.3 | Add inline comments to all three constants per spec | FR-ATL.1, NFR-ATL.4 |
| 1.2.4 | Remove stale `# 100 KB` comment and any `import resource` line | FR-ATL.1 |
| 1.2.5 | Change embed guard to measure `composed = step.prompt + "\n\n" + embedded` with `<=` operator | FR-ATL.2 |
| 1.2.6 | Update warning log to report "composed prompt" and actual byte count | FR-ATL.2 |
| 1.2.7 | Add code comment explaining `<=` is intentional | FR-ATL.2 |

**Files touched**: `src/superclaude/cli/roadmap/executor.py`

**Parallelism**: Runs in parallel with Phase 1.1 (different files, no shared code paths).

**Milestone**: Embed guard uses derived constants and measures full composed string.

---

### Phase 1.5 — Conditional: `--file` Fallback Remediation

**Activation**: Only if Phase 0 result is **BROKEN**.

**Why conditional**: This phase exists to prevent silent context loss. If `--file` is broken, the current oversized-input path may appear successful while actually depriving the model of source content.

| Step | Action | Requirement |
|------|--------|-------------|
| 1.5.1 | Fix `remediate_executor.py:177` — replace `--file` with inline embedding | FR-ATL.5b |
| 1.5.2 | Fix fallback paths in `executor.py`, `validate_executor.py`, `tasklist/executor.py` | FR-ATL.5b |
| 1.5.3 | Run affected test suites to confirm no regression | NFR-ATL.3 |

**If WORKING**: Mark Phase 1.5 as N/A in release notes.

**Files touched (if activated)**: `remediate_executor.py`, `validate_executor.py`, `tasklist/executor.py`, `executor.py`

**Milestone**: All fallback paths deliver file content regardless of `--file` status.

---

### Phase 2 — Test Coverage

**Objective**: Add regression tests that lock in the new behavior. Targeted tests should fail fast on localized issues before broader validation consumes more time.

**Sequencing constraint**: Must run after both Phases 1.1 and 1.2 complete, because the `--tools default` insertion changes the flag list structure and any positional test assertions must account for the final state.

| Step | Action | Requirement |
|------|--------|-------------|
| 2.1 | Add `test_tools_default_in_command` in `tests/pipeline/test_process.py` | FR-001.3 |
| 2.2 | Update `test_required_flags` to assert `--tools` and `default` present | FR-001.3 |
| 2.3 | Update `test_stream_json_matches_sprint_flags` similarly | FR-001.3 |
| 2.4 | Rename `test_100kb_guard_fallback` → `test_embed_size_guard_fallback`, update docstrings | FR-ATL.3 |
| 2.5 | Add `test_prompt_plus_embedded_exceeds_limit`: 90% file + large prompt → fallback fires | FR-ATL.4 |
| 2.6 | Add at-limit boundary test: input exactly `_EMBED_SIZE_LIMIT` bytes → inline embedding (not fallback) | FR-ATL.2 (boundary) |

**Files touched**: `tests/pipeline/test_process.py`, `tests/roadmap/test_executor.py` (or equivalent)

**Milestone**: All six new/updated tests green under `uv run pytest -v`.

---

### Phase 3 — Integration Validation

**Objective**: Full suite passes, no regressions, all success criteria met including performance baseline.

| Step | Action | Requirement |
|------|--------|-------------|
| 3.1 | Run targeted suites first: `uv run pytest tests/pipeline/test_process.py -v` and relevant roadmap/sprint tests | NFR-ATL.3 |
| 3.2 | Run broader suite: `uv run pytest tests/pipeline/ tests/roadmap/ tests/sprint/ -v` — 100% pass | NFR-ATL.3 |
| 3.3 | Run full suite if targeted validations are clean: `uv run pytest` | NFR-ATL.3 |
| 3.4 | Verify zero new imports in changed files | NFR-ATL.1 |
| 3.5 | Confirm `superclaude sprint run` completes Phase 2 without `InputValidationError` | SC-2 |
| 3.6 | Test with spec file ~115 KB to confirm no `OSError [Errno 7]` | SC-3 |
| 3.7 | Verify constants have inline comments (code review) | NFR-ATL.4 |
| 3.8 | Lightweight timing comparison: subprocess startup with and without `--tools default` to close NFR-001.1 | NFR-001.1 |

**Milestone**: Release candidate validated. All 10 success criteria confirmed.

---

## Risk Assessment & Mitigation

| # | Risk | Prob | Impact | Mitigation | Phase | Residual Concern |
|---|------|------|--------|------------|-------|------------------|
| 1 | `--file` fallback broken | **80%** | High | Phase 0 gate + Phase 1.5 contingency | 0, 1.5 | Prior fallback behavior may have produced misleadingly "successful" but context-incomplete runs |
| 2 | `--tools default` enables unintended tool | Low | Medium | Default set is stable; same as interactive mode | 1.1 | None — default toolset is well-characterized |
| 3 | Subclass bypasses `super()` in `build_command()` | Low | Low | Read all subclasses in Step 1.1.1 | 1.1 | None if verified |
| 4 | Index-based test assertions break from flag insertion | Low | Low | Phase 1.1 lands before Phase 2 test run | 1.1, 2 | None — sequencing eliminates this |
| 5 | 8 KB overhead too conservative | Low | Low | Full-string guard (FR-ATL.2) is real safety net | 1.2 | None — composed-string measurement catches all cases |
| 6 | Future template exceeds 8 KB overhead | Low | Medium | Named constant with rationale comment, easy to update; assertion catches degradation | 1.2 | Overhead constant could become stale if templates grow substantially without updating the constant |
| 7 | Windows 32 KB limit | Low | Medium | Deferred (out of scope); Linux-first is correct | — | Explicitly recorded as deferred; do not dilute current release scope |
| 8 | Non-inheriting executors lack `--tools default` | Low | Medium | Tracked as OQ-4; assess post-Phase 0, codebase search recommended | 3 | Unknown population of non-`ClaudeProcess` executors |

---

## Resource Requirements & Dependencies

### Engineering Resources

| Role | Responsibility | Phases |
|------|---------------|--------|
| Primary implementer | Backend/CLI familiarity; executes Phases 1.1, 1.2, 2 | 1.1, 1.2, 1.5, 2 |
| Validation owner | Executes Phase 0 empirical check; verifies reproducible evidence | 0, 3 |
| Reviewer | Focus on command construction, boundary conditions, scope control | All |

### External Dependencies

| Dependency | Type | Impact | Required By |
|------------|------|--------|-------------|
| `claude` CLI (installed, authenticated) | External binary | Blocks Phase 0 entirely | Phase 0 |
| Linux `MAX_ARG_STRLEN` = 128 KB | OS constant | Design assumption for all embed guard logic | Phase 1.2 |
| `ClaudeProcess` base class (`process.py`) | Internal | FIX-001 inheritance propagation | Phase 1.1 |
| `executor.py` embed pipeline | Internal | FIX-ARG-TOO-LONG constant/guard changes | Phase 1.2 |

### Files Modified (Worst Case — Phase 1.5 Activated)

| File | Phase | Change Type |
|------|-------|-------------|
| `src/superclaude/cli/pipeline/process.py` | 1.1 | Add 2 list elements |
| `src/superclaude/cli/roadmap/executor.py` | 1.2 | Constants + guard rewrite |
| `remediate_executor.py` | 1.5 | Fallback path fix (conditional) |
| `validate_executor.py` | 1.5 | Fallback path fix (conditional) |
| `tasklist/executor.py` | 1.5 | Fallback path fix (conditional) |
| `tests/pipeline/test_process.py` | 2 | 3 test updates/additions |
| `tests/roadmap/test_executor.py` | 2 | 2 test rename/additions |

### Tooling Constraints

- **UV only** for all test execution (`uv run pytest`)
- No new imports in modified files per NFR-ATL.1
- No scope expansion into deferred items: stdin delivery, prompt compression, Windows 32 KB support, sprint orchestration redesign

---

## Success Criteria Validation Matrix

| # | Criterion | Validated By | Phase |
|---|-----------|--------------|-------|
| SC-1 | `--tools default` in all subprocess commands | `test_tools_default_in_command` + `test_required_flags` | 2 |
| SC-2 | Phase 2 sprint succeeds without `InputValidationError` | Manual `superclaude sprint run` | 3 |
| SC-3 | No `OSError [Errno 7]` for inputs ≤120 KB | Manual test with ~115 KB spec | 3 |
| SC-4 | Fallback fires for oversized composed inputs | `test_prompt_plus_embedded_exceeds_limit` | 2 |
| SC-5 | Existing tests pass unchanged | `uv run pytest` full suite | 3 |
| SC-6 | New regression tests pass | `uv run pytest -v` on new tests | 2 |
| SC-7 | Phase 0 result recorded | Release notes documentation | 0 |
| SC-8 | Zero new imports | `grep` audit of changed files | 3 |
| SC-9 | Constants self-documenting | Code review of inline comments | 1.2 |
| SC-10 | At-limit boundary correct (`<=`) | Boundary test case | 2 |

---

## Timeline Estimates

### Implementation Effort (Single Implementer)

| Phase | Description | Estimated Effort | Parallelism |
|-------|-------------|-----------------|-------------|
| 0 | Empirical validation gate | 15–30 min | Sequential (blocks all) |
| 1.1 | `--tools default` flag | 15–30 min | Parallel with 1.2 (after Phase 0) |
| 1.2 | Constants & guard rewrite | 30–45 min | Parallel with 1.1 (after Phase 0) |
| 1.5 | `--file` remediation (conditional) | 30–60 min | Sequential (after 1.2, only if BROKEN) |
| 2 | Test coverage | 30–45 min | After 1.1 + 1.2 (+ 1.5 if activated) |
| 3 | Integration validation + performance timing | 20–40 min | After Phase 2 |

**Implementation effort (WORKING path)**: ~2–3 hours
**Implementation effort (BROKEN path)**: ~3–4 hours

### Delivery Elapsed Time (Including Review & Environment)

Accounting for Phase 0 environment setup, review cycles, and coordination overhead:

**Delivery elapsed (WORKING path)**: 1–2 days
**Delivery elapsed (BROKEN path)**: 2–3 days

### Critical Path

1. FR-ATL.5-IMPLICIT → FR-ATL.5a (Phase 0 gate)
2. Decision on FR-ATL.5b (Phase 1.5 activation)
3. FR-001.1 / FR-001.2 ‖ FR-ATL.1 / FR-ATL.2 (parallel implementation)
4. FR-001.3 / FR-ATL.3 / FR-ATL.4 (test coverage)
5. NFR-001.1 / NFR-ATL.1–4 (integration validation)

---

## Open Questions for Post-Release

- **OQ-2**: Stdin prompt delivery as `MAX_ARG_STRLEN` bypass — deferred to v2.26
- **OQ-4**: Non-`ClaudeProcess` executors needing `--tools default` — assess after Phase 0, track for next release if needed
- **OQ-6**: Completeness of executor inventory — codebase search for subprocess invocation patterns recommended before v2.26
