---
spec_source: v2.25.1-release-spec.md
complexity_score: 0.5
primary_persona: analyzer
---

# 1. Executive Summary

This roadmap delivers two tightly scoped fixes to the CLI pipeline with a risk-first execution order:

1. **Restore tool schema availability in subprocess invocations** by adding `--tools default` in `ClaudeProcess.build_command()` per **FR-001.1** and **FR-001.2**.
2. **Eliminate Linux argument-length failures** by replacing the current hardcoded embed limit with a kernel-aligned derived limit and guarding the full composed `-p` argument per **FR-ATL.1** and **FR-ATL.2**.

The critical analyzer conclusion is that **FR-ATL.5 / FR-ATL.5-IMPLICIT** is the primary gating decision. The empirical `--file` validation determines whether the current fallback path is trustworthy or whether Phase 1.5 remediation must activate. That gate should run first because it changes downstream implementation scope, validation strategy, and release risk.

The roadmap prioritizes:

- Early elimination of the highest-uncertainty path
- Minimal edit surface
- Strict adherence to architectural constraints
- Regression containment through focused tests first, then targeted broader validation

## Delivery Objectives

1. Satisfy all 15 extracted requirements without scope expansion.
2. Preserve backward compatibility and avoid new imports per **NFR-001.2** and **NFR-ATL.1**.
3. Convert the current failure mode from crash to deterministic fallback per **NFR-ATL.2**.
4. Produce third-party verifiable evidence for the blocking `--file` behavior decision.

---

# 2. Phased Implementation Plan with Milestones

## Phase 0 — Blocking Validation Gate: `--file` Empirical Behavior
**Purpose:** Resolve the highest-risk uncertainty before code changes.

### Scope
- **FR-ATL.5a**
- **FR-ATL.5-IMPLICIT**

### Actions
1. Verify CLI prerequisite:
   - Run `claude --print -p "hello" --max-turns 1`
   - Confirm exit code 0 and usable authenticated environment.
2. Run timestamped sentinel validation:
   - Use a unique `PINEAPPLE`-style sentinel in a test file.
   - Execute bare-path `--file` invocation exactly in the mode relevant to the pipeline.
3. Record result as one of:
   - `WORKING`
   - `BROKEN`
   - `CLI FAILURE`
4. Capture evidence:
   - Command used
   - Output observed
   - Exit code
   - Timestamp
   - Minimal interpretation

### Milestone M0
- Blocking gate resolved.
- One of two downstream paths selected:
  - **Path A:** `WORKING` → Phase 1.5 marked N/A
  - **Path B:** `BROKEN` → Phase 1.5 activates

### Analyzer Priority
This phase is mandatory because it collapses the largest ambiguity in the release. Without it, later test passes could give false confidence while the oversized-input fallback remains non-functional.

### Timeline Estimate
- **0.5 day**

---

## Phase 1 — Command Construction Fix: Add `--tools default`
**Purpose:** Restore subprocess tool schema discovery with minimal blast radius.

### Scope
- **FR-001.1**
- **FR-001.2**

### Actions
1. Update `ClaudeProcess.build_command()` in the single permitted edit point:
   - Insert `--tools`, `default`
   - Preserve placement between `--no-session-persistence` and `--max-turns`
2. Confirm no change to:
   - Existing required flags
   - `extra_args` passthrough
   - Conditional `--model` behavior
3. Read subclass files before finalizing to confirm inheritance assumptions remain valid.

### Milestone M1
- `build_command()` emits `--tools default` in the required position.
- Existing command structure remains intact.

### Analyzer Priority
This is a low-surface, high-leverage fix. It should land early because it directly addresses Phase 2 sprint failures and reduces ambiguity in later integrated validation.

### Timeline Estimate
- **0.5 day**

---

## Phase 1.5 — Conditional Fallback Remediation
**Purpose:** Activate only if Phase 0 proves bare-path `--file` delivery is broken.

### Scope
- **FR-ATL.5b**

### Conditional Trigger
- Only execute if Phase 0 result is `BROKEN`.

### Actions
1. Fix `remediate_executor.py:177` to use inline embedding instead of broken `--file` behavior.
2. Fix fallback paths in:
   - `executor.py`
   - `validate_executor.py`
   - `tasklist/executor.py`
3. Preserve scope boundary:
   - Do not generalize beyond the explicitly identified files.
4. Re-run targeted validation on oversized-input paths after remediation.

### Milestone M1.5
- All affected fallback paths no longer depend on broken `--file` behavior.
- Conditional branch closed with deterministic behavior.

### Analyzer Priority
This phase exists to prevent silent context loss. If `--file` is broken, the current oversized-input path may appear successful while actually depriving the model of source content.

### Timeline Estimate
- **0.5–1.0 day** if activated
- **0 days** if Phase 0 result is `WORKING`

---

## Phase 2 — Argument-Length Guard Refactor
**Purpose:** Align embed sizing with Linux command-line constraints and guard the actual composed prompt.

### Scope
- **FR-ATL.1**
- **FR-ATL.2**

### Actions
1. Replace hardcoded embed limit with module-level constants:
   - `_MAX_ARG_STRLEN`
   - `_PROMPT_TEMPLATE_OVERHEAD`
   - `_EMBED_SIZE_LIMIT`
2. Set `_EMBED_SIZE_LIMIT = _MAX_ARG_STRLEN - _PROMPT_TEMPLATE_OVERHEAD`.
3. Add required module-level assertion immediately after constant definitions:
   - Enforce `_PROMPT_TEMPLATE_OVERHEAD >= 4096`
   - Include kernel margin rationale and measured template peak
4. Remove dead code:
   - No `import resource`
   - Remove stale `# 100 KB` comment
5. Update guard logic to measure the actual composed `-p` argument:
   - `step.prompt + "\n\n" + embedded`
6. Ensure:
   - Warning log references “composed prompt”
   - Boundary behavior uses `<=`
   - Adjacent comment explains why `<=` is intentional

### Milestone M2
- Embed guard reflects actual Linux argument constraint.
- Crash path becomes deterministic fallback path.
- Self-documenting constants replace magic numbers.

### Analyzer Priority
This phase addresses a correctness defect with direct operational failure impact. The main concern is not code complexity but boundary correctness and faithful modeling of OS constraints.

### Timeline Estimate
- **1.0 day**

---

## Phase 3 — Targeted Regression and Boundary Tests
**Purpose:** Lock fixes in with focused tests before broader execution.

### Scope
- **FR-001.3**
- **FR-ATL.3**
- **FR-ATL.4**

### Actions
1. Add and update command tests:
   - New `test_tools_default_in_command`
   - Update `test_required_flags`
   - Update `test_stream_json_matches_sprint_flags`
2. Rename misleading test:
   - `test_100kb_guard_fallback` → `test_embed_size_guard_fallback`
3. Update test docstrings/comments to reference `_EMBED_SIZE_LIMIT`
4. Add composed-string overflow test:
   - Embedded content at ~90% of `_EMBED_SIZE_LIMIT`
   - Prompt large enough to exceed combined limit
   - Assert fallback behavior and `--file` extra args presence where applicable
5. Validate exact-boundary behavior:
   - At-limit composed input uses inline embedding, not fallback

### Milestone M3
- New regression tests pass.
- Boundary behavior is explicitly covered.
- Naming and documentation align with implementation reality.

### Analyzer Priority
Targeted tests are critical because these defects are easy to reintroduce via “small cleanup” edits. The roadmap emphasizes precise regression coverage rather than broad but shallow test expansion.

### Timeline Estimate
- **1.0 day**

---

## Phase 4 — Integrated Validation and Release Readiness
**Purpose:** Verify no regressions across affected pipeline surfaces.

### Scope
- **NFR-001.1**
- **NFR-001.2**
- **NFR-ATL.1**
- **NFR-ATL.2**
- **NFR-ATL.3**
- **NFR-ATL.4**

### Actions
1. Run targeted suites first:
   - `uv run pytest tests/pipeline/test_process.py -v`
   - Relevant roadmap and sprint tests
2. Run broader affected suite:
   - `uv run pytest tests/pipeline/ tests/roadmap/ tests/sprint/ -v`
3. Run full suite if targeted validations are clean:
   - `uv run pytest`
4. Verify no new imports in changed files.
5. Review changed files for:
   - Zero magic numbers in guard logic
   - Required inline comments
   - Correct flag ordering
6. Compare subprocess startup timing with and without `--tools default` for **NFR-001.1**.

### Milestone M4
- All acceptance criteria and non-functional checks validated.
- Release is ready for completion signoff.

### Analyzer Priority
The key here is sequencing: targeted tests should fail fast on localized issues before broader suite execution consumes more time and obscures diagnosis.

### Timeline Estimate
- **0.5–1.0 day**

---

# 3. Risk Assessment and Mitigation Strategies

## High-Priority Risks

### 1. `--file` fallback is broken
- **Mapped requirements:** **FR-ATL.5**, **FR-ATL.5a**, **FR-ATL.5b**, **FR-ATL.5-IMPLICIT**
- **Impact:** High
- **Likelihood:** Highest identified in extraction
- **Mitigation:**
  1. Run Phase 0 first.
  2. Treat result as release-gating evidence.
  3. If `BROKEN`, activate Phase 1.5 immediately.
- **Residual concern:** Prior fallback behavior may have produced misleadingly “successful” but context-incomplete runs.

### 2. Flag-position tests fail after `--tools default` insertion
- **Mapped requirements:** **FR-001.1**, **FR-001.3**
- **Impact:** Low
- **Likelihood:** Moderate during implementation
- **Mitigation:**
  1. Update targeted tests in the same change set as the command fix.
  2. Preserve exact placement between session-control flags.

### 3. Embed guard still models the wrong payload size
- **Mapped requirements:** **FR-ATL.2**
- **Impact:** High
- **Likelihood:** Moderate if only `embedded` is measured
- **Mitigation:**
  1. Guard the full composed prompt only.
  2. Add explicit boundary and overflow tests.
  3. Confirm warning log language matches behavior.

## Medium-Priority Risks

### 4. Subclass behavior bypasses base-class fix
- **Mapped requirements:** **FR-001.2**
- **Impact:** Low
- **Likelihood:** Low
- **Mitigation:**
  1. Confirm inheritance chain before merge.
  2. Do not duplicate fix at call sites.

### 5. Overhead constant becomes stale over time
- **Mapped requirements:** **FR-ATL.1**, **NFR-ATL.4**
- **Impact:** Medium
- **Likelihood:** Low
- **Mitigation:**
  1. Encode rationale in inline comments.
  2. Enforce assertion with measured-peak rationale.
  3. Keep constant centrally defined for future adjustment.

### 6. Non-inheriting executors also need `--tools default`
- **Mapped concern:** OQ-4
- **Impact:** Medium
- **Likelihood:** Unknown
- **Mitigation:**
  1. Assess after Phase 0.
  2. Do not widen scope unless empirical evidence justifies it.

## Low-Priority but Tracked Risks

### 7. Performance regression from `--tools default`
- **Mapped requirements:** **NFR-001.1**
- **Mitigation:** Lightweight timing comparison during Phase 4.

### 8. Linux-first fix leaves Windows limitation unresolved
- **Mapped constraint:** Out of scope
- **Mitigation:** Record explicitly as deferred; do not dilute current release scope.

---

# 4. Resource Requirements and Dependencies

## Engineering Resources

1. **Primary implementer**
   - Backend/CLI familiarity
   - Responsible for Phases 1, 2, 3
2. **Validation owner**
   - Executes Phase 0 empirical check
   - Verifies reproducible evidence
3. **Reviewer**
   - Focus on command construction, boundary conditions, and scope control

## Technical Dependencies

### 1. `claude` CLI
- Required for **FR-ATL.5a** and **FR-ATL.5-IMPLICIT**
- Must be installed, authenticated, and able to complete `--print` requests

### 2. Linux kernel `MAX_ARG_STRLEN`
- Governs **FR-ATL.1** and **FR-ATL.2**
- Must be treated as compile-time constant, not runtime-discoverable

### 3. `ClaudeProcess` base class
- Shared delivery point for **FR-001.1** and **FR-001.2**
- Single authorized edit point

### 4. `executor.py` embed pipeline
- Governs core argument-size behavior for **FR-ATL.1** through **FR-ATL.4**

## Tooling / Execution Constraints

1. Use **UV only** for tests:
   - `uv run pytest`
2. No new imports in modified files per **NFR-ATL.1**
3. No scope expansion into deferred items:
   - stdin delivery
   - prompt compression
   - Windows 32 KB support
   - sprint orchestration redesign

---

# 5. Success Criteria and Validation Approach

## Primary Success Criteria Mapping

1. **Subprocess commands include `--tools default`**
   - Validate **FR-001.1**
   - Confirm flag adjacency and position

2. **Existing command behavior remains intact**
   - Validate **FR-001.2**
   - Confirm required flags, conditional `--model`, and `extra_args` passthrough

3. **Regression tests lock in tool flag behavior**
   - Validate **FR-001.3**

4. **Embed constants are derived and self-documenting**
   - Validate **FR-ATL.1**
   - Validate **NFR-ATL.4**

5. **Guard measures full composed prompt**
   - Validate **FR-ATL.2**

6. **Legacy “100KB” naming removed**
   - Validate **FR-ATL.3**

7. **Composed-overflow fallback is covered**
   - Validate **FR-ATL.4**

8. **`--file` behavior is empirically classified**
   - Validate **FR-ATL.5a**
   - Validate **FR-ATL.5-IMPLICIT**

9. **Conditional remediation is completed if needed**
   - Validate **FR-ATL.5b**

10. **Non-functional safety holds**
   - Validate **NFR-001.1**, **NFR-001.2**, **NFR-ATL.1**, **NFR-ATL.2**, **NFR-ATL.3**

## Validation Strategy

### A. Evidence-first validation
1. Phase 0 empirical proof before implementation branch finalization
2. Store explicit result for later auditability

### B. Targeted unit/regression validation
1. Run `tests/pipeline/test_process.py`
2. Run updated roadmap/sprint tests covering embed behavior
3. Confirm new and renamed tests pass

### C. Boundary validation
1. Exact at-limit case
2. Embedded-under-limit but composed-over-limit case
3. Small-input no-regression case

### D. Broader compatibility validation
1. Affected test directories
2. Full suite if localized checks are clean

### E. Static review validation
1. No new imports
2. Required comments present
3. No stale magic-number references
4. Flag placement preserved

---

# 6. Timeline Estimates per Phase

## Baseline Timeline
Assumes normal development flow and no major environmental blocker.

1. **Phase 0 — Blocking Validation Gate**
   - **Estimate:** 0.5 day

2. **Phase 1 — Command Construction Fix**
   - **Estimate:** 0.5 day

3. **Phase 1.5 — Conditional Fallback Remediation**
   - **Estimate:** 0.5–1.0 day if activated
   - **Estimate:** 0 days if not activated

4. **Phase 2 — Argument-Length Guard Refactor**
   - **Estimate:** 1.0 day

5. **Phase 3 — Targeted Regression and Boundary Tests**
   - **Estimate:** 1.0 day

6. **Phase 4 — Integrated Validation and Release Readiness**
   - **Estimate:** 0.5–1.0 day

## Total Estimated Duration

### If Phase 0 result is `WORKING`
- **Total:** 3.5–4.0 days

### If Phase 0 result is `BROKEN`
- **Total:** 4.0–5.0 days

## Critical Path
1. **FR-ATL.5-IMPLICIT**
2. **FR-ATL.5a**
3. Decision on **FR-ATL.5b**
4. **FR-001.1** / **FR-001.2**
5. **FR-ATL.1** / **FR-ATL.2**
6. **FR-001.3** / **FR-ATL.3** / **FR-ATL.4**
7. Non-functional validation

## Recommended Sequencing Summary
1. Resolve empirical uncertainty first.
2. Apply minimal command fix next.
3. Refactor size guard after fallback-path confidence is known.
4. Lock boundaries with tests.
5. Run integrated validation last.

---

# Roadmap Completion Checklist

1. **Phase 0 complete**
   - **FR-ATL.5-IMPLICIT**
   - **FR-ATL.5a**

2. **Command fix complete**
   - **FR-001.1**
   - **FR-001.2**

3. **Conditional branch resolved**
   - **FR-ATL.5b** if required

4. **Embed guard refactor complete**
   - **FR-ATL.1**
   - **FR-ATL.2**

5. **Tests complete**
   - **FR-001.3**
   - **FR-ATL.3**
   - **FR-ATL.4**

6. **Non-functional checks complete**
   - **NFR-001.1**
   - **NFR-001.2**
   - **NFR-ATL.1**
   - **NFR-ATL.2**
   - **NFR-ATL.3**
   - **NFR-ATL.4**

7. **Release readiness confirmed**
   - All 10 success criteria validated
   - Open questions reduced to only explicitly deferred items
