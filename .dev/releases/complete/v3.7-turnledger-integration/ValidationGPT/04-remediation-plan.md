# Remediation Plan

## Phase R1: Roadmap-spec contradictions

- [ ] **GAP-H005** (HIGH, SMALL): Add `duration_ms` to the audit schema.
  - File: `roadmap.md:47`
  - Action: EDIT
  - Change: expand the declared schema from 9 fields to include `duration_ms` and align wording with FR-7.1.
  - Verification: roadmap schema exactly matches spec example fields.
  - Dependencies: []

- [ ] **GAP-H006** (HIGH, SMALL): Correct audit fixture flush semantics.
  - File: `roadmap.md:48-49`
  - Action: EDIT
  - Change: replace “auto-flushes on session end” with per-test auto-flush; keep session-end summary as separate behavior.
  - Verification: fixture description matches FR-7.3 bullet list.
  - Dependencies: []

## Phase R2: Missing coverage — HIGH

- [ ] **GAP-H001** (HIGH, SMALL): Add FR-1.19 explicit test task.
  - File: `roadmap.md:78-91`
  - Action: ADD
  - Change: add a Phase 2A task for `SHADOW_GRACE_INFINITE` value + grace-period behavior.
  - Verification: task table explicitly names FR-1.19 and shadow-mode semantics.
  - Dependencies: []

- [ ] **GAP-H002** (HIGH, SMALL): Add FR-1.20 explicit test task.
  - File: `roadmap.md:78-91`
  - Action: ADD
  - Change: add a Phase 2A task for `__post_init__()` config derivation fields and defaults.
  - Verification: task table explicitly names derived fields.
  - Dependencies: []

- [ ] **GAP-H003** (HIGH, SMALL): Add FR-1.21 explicit test task.
  - File: `roadmap.md:78-91`
  - Action: ADD
  - Change: add a Phase 2A or 2D task for `check_wiring_report()` wrapper invocation and delegation behavior.
  - Verification: task table explicitly names wrapper-call validation.
  - Dependencies: []

- [ ] **GAP-H004** (HIGH, SMALL): Add FR-2.1a explicit lifecycle test task.
  - File: `roadmap.md:99-106`
  - Action: ADD
  - Change: add convergence regression-handler reachability/invocation/logging/budget assertions.
  - Verification: Phase 2B line item explicitly names `handle_regression()` path.
  - Dependencies: []

- [ ] **GAP-H007** (HIGH, TRIVIAL): Fix misleading requirement-count claim.
  - File: `roadmap.md:271`
  - Action: EDIT
  - Change: replace “13 requirements” with a clearly scoped aggregation note or remove the count.
  - Verification: roadmap metadata no longer understates atomic requirement surface.
  - Dependencies: []

## Phase R3: Partial coverage — MEDIUM

- [ ] **GAP-M001** (MEDIUM, SMALL): Strengthen FR-4.1 manifest scope.
  - File: `roadmap.md:58-61,175`
  - Action: EDIT
  - Change: explicitly commit initial manifest to all 13 authoritative entries, not just executor.py entry points.
  - Verification: manifest task references full v3.1/v3.2/v3.05 surface.
  - Dependencies: []

- [ ] **GAP-M002** (MEDIUM, SMALL): Add FR-5.2 positive-case test.
  - File: `roadmap.md:156-158`
  - Action: ADD
  - Change: include a synthetic known-good case before the missing-implementation case.
  - Verification: both positive and negative checker tests are listed.
  - Dependencies: []

- [ ] **GAP-M003** (MEDIUM, MEDIUM): Expand FR-6.1 gap closure details.
  - File: `roadmap.md:124-127`
  - Action: EDIT
  - Change: enumerate exact missing assertions/deliverables for T07, T11, T12, T14.
  - Verification: each gap ID has a concrete closure statement.
  - Dependencies: []

- [ ] **GAP-M004** (MEDIUM, MEDIUM): Expand FR-6.2 T17-T22 into explicit closure items.
  - File: `roadmap.md:128-129`
  - Action: SPLIT
  - Change: break grouped suite into per-gap deliverables or acceptance bullets.
  - Verification: T17 through T22 are each traceable.
  - Dependencies: []

- [ ] **GAP-M005** (MEDIUM, TRIVIAL): Downgrade or tighten SC-8 claim until FR-6 is explicit.
  - File: `roadmap.md:255`
  - Action: EDIT
  - Change: align SC-8 wording to underlying detailed tasks.
  - Verification: success criterion is no stronger than planned work.
  - Dependencies: ["GAP-M003", "GAP-M004"]

- [ ] **GAP-M006** (MEDIUM, TRIVIAL): Tighten SC-12 after audit fixes.
  - File: `roadmap.md:259`
  - Action: EDIT
  - Change: keep SC-12 but align it with corrected FR-7.1/FR-7.3 wording.
  - Verification: success criterion no longer inherits contradiction.
  - Dependencies: ["GAP-H005", "GAP-H006"]

## Phase R4: Low cleanup

- [ ] **GAP-L001** (LOW, TRIVIAL): Add explicit stop conditions to checkpoints A-D.
  - File: `roadmap.md:64,133,160,179`
  - Action: EDIT
  - Change: add failure/stop conditions to each checkpoint.
  - Verification: each checkpoint has pass and stop criteria.
  - Dependencies: []

- [ ] **GAP-L002** (LOW, TRIVIAL): Make FR-5.3 traceability explicit.
  - File: `roadmap.md:150`
  - Action: EDIT
  - Change: append a note that FR-5.3 is satisfied by FR-4 reachability gate work.
  - Verification: direct traceability present.
  - Dependencies: []

## Projected Impact

If all remediations are applied:
- Projected coverage: ~96%+
- Projected findings: 0 HIGH, 0 CONFLICTING, 0 MISSING, a small number of possible LOW cleanup items
- Projected verdict: GO or strong CONDITIONAL_GO pending revalidation
- Estimated effort: SMALL-to-MEDIUM roadmap rewrite, no code changes required for validation artifact correction
