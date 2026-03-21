---
spec_source: "release-spec-accept-spec-change.md"
complexity_score: 0.65
primary_persona: architect
---

## 1. Executive summary

This roadmap delivers a controlled spec-hash reconciliation capability for the roadmap pipeline with two tightly scoped surfaces:

1. A new `accept-spec-change` CLI path that updates `.roadmap-state.json` only when evidence-backed accepted deviations exist.
2. A single-cycle executor auto-resume path that safely detects post-`spec-fidelity` spec patches and re-enters resume flow without re-running upstream phases.

From an architecture perspective, the highest-priority concerns are:

- preserving state integrity during all write paths
- preventing loops or unintended re-entry in `execute_roadmap()`
- keeping `spec_patch.py` isolated as a leaf module
- enforcing evidence-based acceptance rather than implicit spec drift
- maintaining backward compatibility for existing roadmap callers

The implementation should be treated as a reliability-focused change to the roadmap control plane, not as a broad pipeline refactor.

## 2. Phased implementation plan with milestones

### Phase 0 — Architecture lock and implementation readiness

**Objective:** Freeze design boundaries before touching execution flow.

**Scope**
- Confirm architectural constraints and dependency direction.
- Confirm target files and ownership boundaries.
- Confirm test matrix for CLI, state, and resume-cycle behavior.

**Requirements addressed**
- FR-2.24.2.8
- FR-2.24.2.11
- Architectural Constraints 1-10
- NFR-4
- NFR-5

**Actions**
1. Define module responsibilities:
   - `spec_patch.py`: deviation scan, hash recompute, prompt/abort, atomic state update
   - `commands.py`: CLI wiring only
   - `executor.py`: auto-resume trigger, disk re-read sequence, recursion guard, logging
2. Lock dependency direction:
   - `commands.py → spec_patch.py`
   - `executor.py → spec_patch.py`
   - no reverse imports
3. Confirm data model expectations for `DeviationRecord`, especially absent `id` handling.
4. Confirm PyYAML dependency addition path.
5. Confirm operator-facing documentation for exclusive access constraint.

**Milestone**
- Approved architecture note covering file boundaries, import boundaries, and test plan.

**Architect recommendation**
- Do not begin executor changes until module isolation and recursion-guard placement are explicitly agreed. The failure cost is higher in `executor.py` than in the CLI layer.

---

### Phase 1 — Build `spec_patch.py` leaf module

**Objective:** Implement the spec-acceptance mechanism as an isolated, testable module.

**Scope**
- state file lookup
- spec hash recomputation
- accepted deviation scan
- interactive confirmation handling
- atomic `spec_hash` update
- confirmation output

**Requirements addressed**
- FR-2.24.2.1
- FR-2.24.2.2
- FR-2.24.2.3
- FR-2.24.2.3a
- FR-2.24.2.3b
- FR-2.24.2.4
- FR-2.24.2.4a
- FR-2.24.2.4b
- FR-2.24.2.4c
- FR-2.24.2.4d
- FR-2.24.2.4e
- FR-2.24.2.4f
- FR-2.24.2.5
- FR-2.24.2.5a
- FR-2.24.2.5b
- FR-2.24.2.5c
- FR-2.24.2.6
- FR-2.24.2.7
- NFR-1
- NFR-2
- NFR-3
- NFR-4

**Actions**
1. Implement state discovery and read:
   - load `.roadmap-state.json` from `output_dir`
   - fail fast with exact missing-state error path
2. Implement spec-file hashing:
   - load `spec_file` from state
   - recompute `sha256(spec_file.read_bytes())`
   - fail fast if spec file missing
3. Implement idempotency gate:
   - compare `current_hash` against `state["spec_hash"]`
   - treat absent/null/empty `spec_hash` as mismatch
   - use byte-exact hex equality only
4. Implement deviation evidence scanner:
   - glob `dev-*-accepted-deviation.md`
   - parse YAML frontmatter with PyYAML
   - match only `disposition: ACCEPTED` case-insensitively
   - match only boolean `spec_update_required: true`
   - warn and continue on parse failures
   - fail with zero-records message if no valid matches
5. Implement interactive confirmation:
   - print evidence summary with ID, severity, affected sections, rationale
   - accept only `y` or `Y`
   - abort cleanly for all other cases
   - in non-interactive mode with `auto_accept=False`, exit 0 with `Aborted.`
6. Implement atomic write:
   - write `.roadmap-state.json.tmp`
   - `os.replace()` into place
   - preserve all non-`spec_hash` keys verbatim
7. Implement confirmation output:
   - old hash truncated to 12 chars
   - new hash truncated to 12 chars
   - accepted deviation IDs
   - guidance to run `roadmap run --resume`

**Milestone**
- `spec_patch.py` fully functional and independently testable, with no subprocess usage and no executor coupling.

**Architect recommendation**
- Keep parsing, prompting, and atomic write in separate internal functions. This keeps failure modes localized and simplifies later executor reuse.

---

### Phase 2 — CLI command integration

**Objective:** Expose the manual acceptance workflow without expanding CLI surface area.

**Scope**
- wire `accept-spec-change` into `commands.py`
- preserve zero optional CLI arguments
- keep behavior operator-safe by default

**Requirements addressed**
- FR-2.24.2.5
- FR-2.24.2.6
- FR-2.24.2.7
- Architectural Constraint 8
- NFR-4
- NFR-5

**Actions**
1. Add `accept-spec-change` command with required `output_dir` semantics.
2. Ensure no CLI flag exists for `auto_accept`.
3. Route command directly to `spec_patch.py` entrypoint.
4. Document exclusive access constraint in command help or docstring.

**Milestone**
- Manual operator workflow available and constrained to safe defaults.

**Architect recommendation**
- Resist adding convenience flags in this release. The spec explicitly constrains the CLI surface; breaking that boundary increases long-term control-plane complexity.

---

### Phase 3 — Executor auto-resume integration

**Objective:** Add a single guarded auto-resume cycle after `spec-fidelity` failure.

**Scope**
- extend `execute_roadmap()` with backward-compatible `auto_accept`
- detect spec patch conditions after failed pipeline run
- perform disk-reread state synchronization
- resume exactly once
- log cycle lifecycle

**Requirements addressed**
- FR-2.24.2.8
- FR-2.24.2.9
- FR-2.24.2.9a
- FR-2.24.2.9b
- FR-2.24.2.10
- FR-2.24.2.10a
- FR-2.24.2.10b
- FR-2.24.2.11
- FR-2.24.2.12
- FR-2.24.2.13
- NFR-1
- NFR-3

**Actions**
1. Extend `execute_roadmap()` signature:
   - add `auto_accept: bool = False`
   - preserve all existing callers
2. Capture `initial_spec_hash` at function entry.
3. Add local `_spec_patch_cycle_count = 0`.
4. After `execute_pipeline()` returns with spec-fidelity FAIL, evaluate all trigger conditions:
   - cycle count not exhausted
   - accepted deviation files exist with required metadata and `mtime > started_at`
   - current spec hash differs from `initial_spec_hash`
5. If all conditions hold:
   - emit cycle entry log messages
   - increment guard before cycle entry
   - perform 6-step disk-reread sequence:
     1. re-read state from disk
     2. recompute spec hash
     3. atomically write `spec_hash`
     4. re-read state again
     5. rebuild steps
     6. call `_apply_resume(post_write_state, steps)`
6. Re-run from resume point and allow only one cycle.
7. If second run still fails spec-fidelity:
   - fall through to normal failure path
   - pass only post-resume results to `_format_halt_output`
8. Emit completion and suppression logs per spec.

**Milestone**
- Executor supports one safe spec-patch resume cycle with no loop potential and no in-memory stale state reuse.

**Architect recommendation**
- The disk-reread boundary is the most important invariant in this phase. Treat any attempt to reuse in-memory state as a release blocker.

---

### Phase 4 — Reliability, regression, and contract testing

**Objective:** Prove safety properties and edge-case behavior before release.

**Scope**
- unit and integration tests for CLI behavior
- resume-cycle trigger tests
- state preservation tests
- atomic failure and abort-path tests

**Requirements addressed**
- SC-1 through SC-15
- NFR-1
- NFR-2
- NFR-3
- NFR-4
- NFR-5

**Actions**
1. Add CLI-path tests for:
   - missing state file
   - missing spec file
   - hash already current
   - zero matching deviation records
   - invalid YAML warnings with continue behavior
   - non-interactive abort
   - explicit user abort
   - confirmation output formatting
2. Add state integrity tests for:
   - only `spec_hash` changed
   - no write on abort
   - double-run idempotency
   - atomic write failure fallback
3. Add executor integration tests for:
   - `auto_accept=True` skips prompt
   - `auto_accept=False` preserves prompt behavior
   - all three conditions required for cycle trigger
   - `started_at` absent fails closed
   - proper ISO timestamp conversion before mtime comparison
   - guard fires once only
   - suppression logging
   - normal failure after exhausted cycle
4. Add explicit verification that `spec_patch.py` contains no subprocess invocation path.

**Milestone**
- All measurable success criteria covered by automated validation and review.

**Architect recommendation**
- Prioritize scenario-based integration tests over isolated helper tests for the executor path. The main risk is cross-function state choreography, not pure computation.

---

### Phase 5 — Release hardening and operator documentation

**Objective:** Make operational constraints explicit and prevent misuse.

**Scope**
- document concurrency assumptions
- document accepted deviation workflow
- document manual vs internal-only auto-accept paths

**Requirements addressed**
- NFR-5
- FR-2.24.2.8
- FR-2.24.2.12
- FR-2.24.2.13

**Actions**
1. Document command usage:
   - when to run `accept-spec-change`
   - requirement for evidence-backed deviation files
   - expected follow-up `roadmap run --resume`
2. Document exclusive access constraint:
   - no concurrent `accept-spec-change` with `roadmap run`
3. Document internal-only nature of `auto_accept`.
4. Document known mtime-resolution limitation and any rationale if `>=` is chosen instead of strict `>`.

**Milestone**
- Release package includes implementation, tests, and operator-facing constraints.

**Architect recommendation**
- Documentation is part of the safety model here. NFR-5 is not optional polish; it is a control required because locking is intentionally out of scope.

## 3. Risk assessment and mitigation strategies

### High-priority architectural risks

1. **State corruption during write path**
   - Affects: FR-2.24.2.6, FR-2.24.2.10, NFR-1
   - Risk: partial or accidental overwrite of non-`spec_hash` state keys
   - Mitigation:
     - enforce `.tmp` + `os.replace()` everywhere
     - preserve all non-`spec_hash` keys verbatim
     - add tests diffing pre/post state except `spec_hash`

2. **Infinite or repeated resume loops**
   - Affects: FR-2.24.2.11, FR-2.24.2.13
   - Risk: recursive control-flow instability in roadmap execution
   - Mitigation:
     - local `_spec_patch_cycle_count`
     - increment before cycle entry
     - explicit exhausted-cycle suppression path
     - integration test for two successive calls having independent counters

3. **Stale in-memory state causing wrong resume behavior**
   - Affects: FR-2.24.2.10, SC-7
   - Risk: `_apply_resume()` evaluates outdated hash or steps
   - Mitigation:
     - mandatory disk re-read before and after atomic write
     - rebuild steps immediately before `_apply_resume()`
     - treat reuse of original state object as invalid design

4. **Unsafe auto-accept behavior**
   - Affects: FR-2.24.2.8, Risk Inventory item 5
   - Risk: unreviewed spec hash acceptance
   - Mitigation:
     - no public CLI flag
     - internal-only threading
     - code review focus on all `execute_roadmap(auto_accept=...)` call sites

5. **False-positive deviation matching**
   - Affects: FR-2.24.2.4, FR-2.24.2.4c
   - Risk: quoted `"true"` or malformed YAML causing unintended acceptance
   - Mitigation:
     - strict boolean check for `spec_update_required`
     - explicit warning-and-skip parse behavior
     - tests for absent fields and invalid types

### Secondary delivery risks

1. **mtime resolution edge cases**
   - Affects: FR-2.24.2.9a
   - Mitigation:
     - preserve documented limitation
     - if implementation chooses `>=`, document rationale and cover with tests

2. **Undefined behavior when deviation `id` is absent**
   - Affects: data model integrity
   - Mitigation:
     - decide in Phase 0 whether absent `id` is parse failure
     - enforce consistently in parser and tests

3. **Concurrency unsupported but not visible to operators**
   - Affects: NFR-5
   - Mitigation:
     - docstring/help text warning
     - release notes callout

## 4. Resource requirements and dependencies

### Engineering roles

1. **Primary backend/architect implementer**
   - owns `spec_patch.py`
   - owns `executor.py` integration
   - owns state integrity invariants

2. **QA/reliability engineer**
   - owns regression and integration test matrix
   - validates abort/no-write/idempotency behavior
   - validates log and resume-cycle behavior

3. **Maintainer/reviewer**
   - verifies architectural constraints
   - verifies no subprocess usage in `spec_patch.py`
   - verifies backward compatibility of `execute_roadmap()`

### Code and module touchpoints

- New module:
  - `spec_patch.py`
- Modified modules:
  - `commands.py`
  - `executor.py`
- Tests:
  - 2 focused test files minimum:
    - CLI/spec-patch behavior
    - executor resume-cycle behavior

### External and internal dependencies

1. **PyYAML >= 6.0**
   - Required for YAML frontmatter parsing
   - Critical to FR-2.24.2.4 implementation

2. **Python stdlib**
   - `hashlib`, `os`, `sys`, `json`, `pathlib`, `datetime`
   - Required for hashing, atomic writes, state IO, timestamp conversion

3. **Click**
   - Required for command registration and CLI integration

4. **Executor internals**
   - `_apply_resume`
   - `_build_steps`
   - `_format_halt_output`
   - `execute_pipeline`
   - `read_state`

### Environmental assumptions

- POSIX is primary target for atomic write guarantee.
- Exclusive access is assumed during command execution.
- No file-locking layer is added in this release.

## 5. Success criteria and validation approach

### Validation strategy by requirement cluster

#### A. CLI/manual acceptance validation
- Validate FR-2.24.2.1 through FR-2.24.2.7
- Prove:
  - missing files fail with exact messages
  - evidence scan is strict and safe
  - abort path does not write
  - success path writes only `spec_hash`

**Mapped success criteria**
- SC-1
- SC-2
- SC-3
- SC-4
- SC-11
- SC-12

#### B. Executor auto-resume validation
- Validate FR-2.24.2.8 through FR-2.24.2.13
- Prove:
  - `auto_accept` is backward-compatible
  - trigger requires all three conditions
  - disk-reread sequence is respected
  - recursion guard limits cycle to one
  - post-cycle failure returns normal halt behavior

**Mapped success criteria**
- SC-5a
- SC-5b
- SC-6
- SC-7
- SC-8
- SC-9
- SC-10
- SC-13
- SC-14
- SC-15

#### C. Safety and non-functional validation
- Validate NFR-1 through NFR-5
- Prove:
  - atomic write integrity
  - no writes on abort
  - idempotent re-execution
  - no subprocess invocation in `spec_patch.py`
  - exclusive access constraint is documented

### Release gate

This roadmap should not be considered complete until all of the following are true:

1. All 15 success criteria are explicitly tested or review-verified.
2. No architectural constraint is violated.
3. `execute_roadmap()` remains backward-compatible.
4. Operator documentation for concurrency and workflow constraints is present.
5. Manual and auto-resume paths both demonstrate correct behavior against real state files.

## 6. Timeline estimates per phase

Given the **MEDIUM** complexity score of **0.65**, the implementation should be scheduled as a short, tightly reviewed change set rather than a multi-release program.

### Estimated phase breakdown

1. **Phase 0 — Architecture lock and readiness**
   - Estimate: **0.5 day**
   - Output:
     - design confirmation
     - parser behavior decisions
     - test matrix

2. **Phase 1 — `spec_patch.py` implementation**
   - Estimate: **1.0-1.5 days**
   - Output:
     - working leaf module
     - atomic write path
     - evidence scanner
     - prompt/abort flow

3. **Phase 2 — CLI integration**
   - Estimate: **0.5 day**
   - Output:
     - wired `accept-spec-change` command
     - help/docs constraints

4. **Phase 3 — Executor auto-resume integration**
   - Estimate: **1.0-1.5 days**
   - Output:
     - `auto_accept` threading
     - guarded cycle trigger
     - disk-reread resume sequence
     - logging

5. **Phase 4 — Reliability and regression testing**
   - Estimate: **1.0-1.5 days**
   - Output:
     - automated coverage for SC-1 through SC-15
     - regression confidence on abort, idempotency, and cycle behavior

6. **Phase 5 — Release hardening and documentation**
   - Estimate: **0.5 day**
   - Output:
     - operator guidance
     - concurrency caveats
     - final release readiness

### Total estimate
- **4.5-6.0 engineering days**

### Milestone sequence

1. **M1:** Architecture approved
2. **M2:** Manual `accept-spec-change` workflow complete
3. **M3:** Executor one-cycle auto-resume complete
4. **M4:** Success criteria validated
5. **M5:** Release hardened and documented

## 7. Requirement coverage map

### Manual acceptance path
- FR-2.24.2.1
- FR-2.24.2.2
- FR-2.24.2.3
- FR-2.24.2.3a
- FR-2.24.2.3b
- FR-2.24.2.4
- FR-2.24.2.4a
- FR-2.24.2.4b
- FR-2.24.2.4c
- FR-2.24.2.4d
- FR-2.24.2.4e
- FR-2.24.2.4f
- FR-2.24.2.5
- FR-2.24.2.5a
- FR-2.24.2.5b
- FR-2.24.2.5c
- FR-2.24.2.6
- FR-2.24.2.7

### Executor auto-resume path
- FR-2.24.2.8
- FR-2.24.2.9
- FR-2.24.2.9a
- FR-2.24.2.9b
- FR-2.24.2.10
- FR-2.24.2.10a
- FR-2.24.2.10b
- FR-2.24.2.11
- FR-2.24.2.12
- FR-2.24.2.13

### Non-functional controls
- NFR-1
- NFR-2
- NFR-3
- NFR-4
- NFR-5

## 8. Final architect recommendation

Ship this as a **single focused release** with strict scope control.

The design is sound if and only if these four invariants remain true:

1. `spec_patch.py` stays isolated and subprocess-free.
2. every state write uses atomic replace semantics.
3. the executor resume cycle can fire only once per invocation.
4. resume decisions are made from disk-reloaded state, not stale memory.

If any of those are weakened during implementation, the roadmap should pause for redesign rather than proceed.
