# Phase 7 — Overrides (ACCEPT-class spec-panel findings retro-applied)

This table tracks all spec-panel findings that were ACCEPTED (non-conflicting with G6 and applied to release-spec.md as discovered gaps or refinements).

Decision rule recap: each row passed the 5-step process at Step 4 with verdict "FR silent or FR supports expert → ACCEPT". CASE classification is recorded for each change.

| SP-ID | Expert | Section | Change Applied | Rationale | New CASE |
|-------|--------|---------|----------------|-----------|----------|
| SP-01 | Wiegers | FR-CONV.1 (TB-Add catalogue) | Add RFC-2119 MUST/SHOULD modal verbs to each TB-Add bullet | Improves normative clarity; FR was silent on modal force | clarification-only (no CASE change) |
| SP-02 | Wiegers | NFR-CONV.4 | Define "representative BUILD_REQUESTs" + median ≤1.10 / max ≤1.25 envelope | Resolves statistical-envelope ambiguity; FR silent | clarification-only |
| SP-03 | Wiegers | FR-CONV.2 Acceptance Criteria | Define "minimal" BUILD_REQUEST: lacks ≥2 of {GOAL, WHY, named source-area} | Eliminates degrade-path observer-dependence; FR silent | clarification-only |
| SP-04 | Wiegers | §11 Open Items (OPEN-PR05) | Assign owner + monthly check command | Closes open-item completeness gap; FR silent on ownership | clarification-only |
| SP-05 | Wiegers | §4.5 Data Models | Append per-item 5-field schema block | Aligns §4.5 with NFR-CONV.6 reference; FR silent | clarification-only |
| SP-06 | Cockburn | FR-CONV.3 Acceptance Criteria | Split Observable into Internal prompt invariant + External output invariant | Resolves verification-actor ambiguity; FR partially supported | clarification-only |
| SP-07 | Cockburn | FR-CONV.5 Acceptance Criteria | Symmetrize monotonicity halt message format to match regression halt | Improves halt-message rigor; FR silent on monotonicity format | clarification-only |
| SP-09 | Cockburn | FR-CONV.4 Description | Define "Axis" as ubiquitous-language term | Reduces axis-population variance; FR silent on definition | clarification-only |
| SP-10 | Nygard | §9 Migration & Rollout | Add rollback dependency matrix (FR-CONV.5↔6, FR-CONV.1↔3) | Closes per-FR-revertable contradiction; FR partially supported | clarification-only |
| SP-11 | Nygard | NFR-CONV.5 | Add NFR-CONV.5.1 TB-Add-4 wall-clock budget (<500ms for ≤50 items) | FR silent on local-check perf bounds | clarification-only |
| SP-13 | Nygard | §8.2 Integration Tests | Add `test_pre_commit_hook_blocks_unsynced_claude_edits` | Strengthens sync-discipline guard; FR silent on automation | clarification-only |
| SP-14 | Nygard | §11 Open Items (OPEN-TOKEN) | Add cadence: quarterly + on-touch | FR silent on measurement frequency | clarification-only |
| SP-15 | Hohpe | §5.3 Phase Contracts | Add delivery_semantics + failure_mode fields | Resolves delivery-guarantee implicitness; FR silent | clarification-only |
| SP-16 | Hohpe | §5.3 Phase Contracts | Add schema_version field | Future-proofs contract; FR silent | clarification-only |
| SP-17 | Hohpe | §4.5 Data Models (synthetic_dnsp_finding) | Add transport-medium spec (stdout JSON, team-lead-merge dedup) | Resolves transport ambiguity; FR silent on channel | clarification-only |
| SP-18 | Hohpe | §4.4 Module Dependency Graph | Add dashed back-channel arrow rf-analyst → rf-qa for synthetic-dnsp | Resolves cross-agent flow inaccuracy; FR contained the omission | clarification-only |
| SP-19 | Evans | §1.0 new subsection | Add Ubiquitous Language subsection defining 5 invariants canonically | Resolves DDD term-overloading; FR silent on canon | clarification-only |
| SP-20 | Evans | FR-CONV.3 Negative Criterion | Re-frame anti-inflation as a "rule" (not invariant) | Resolves invariant-list/rule status mix; FR contained the ambiguity | clarification-only |
| SP-21 | Evans | FR-CONV.5 (INV-012) | Split INV-012 into INV-012a (count) + INV-012b (dedup-not-regression) | Independent invariants get independent probes; FR partially supported | clarification-only |
| SP-22 | Evans | Appendix A | Audit rationale-column terms; demote pseudo-invariants | Aligns conflict-register with five-invariant canon | clarification-only |
| SP-23 | Fowler | §4.2 Modified Files | Document SKILL.md:872-916 outer/inner range serial-landing | Resolves overlap ambiguity; FR silent on parallel-merge tolerance | clarification-only |
| SP-24 | Fowler | §9 Rollback | Document per-TB-Add-line rollback granularity matches CB-3 per-check | Documentation clarification only; not splitting FR-CONV.1 into 8 sub-FRs (out of scope this iteration) | clarification-only |
| SP-25 | Fowler | new §8.0 Test Infrastructure | Note which test files are NEW vs EXTENSIONS + test-infra creation in scope | FR silent on test-file deliverable status | clarification-only |
| SP-26 | Fowler | §4.6 Implementation Order | Reconcile §4.5 parallel-tolerance text with §4.6 serial sequence — lock serial | FR contained contradictory statements | clarification-only |
| SP-27 | Fowler | §10 Downstream Inputs | Add note: prd skill consumes §1-§11 body content; frontmatter is informative | Clarifies Phase-8 contract; FR silent | clarification-only |
| SP-28 | Wiegers | FR-CONV.1 (TB-Add-2) | Sub-classify TB-Add-2 into 2a (lower-bound, BLOCK) + 2b (upper-bound, ADVISORY) | Resolves lower-bound under-strictness; FR silent on split | clarification-only |
| SP-29 | Wiegers | NFR-CONV.3 | Define `normalize_for_diff` operation (strip timestamps/run-IDs/random-prefixes) | Resolves byte-identical-on-noise failure; FR silent | clarification-only |
| SP-30 | Cockburn | FR-CONV.3 Description | Add Self-Audit markdown format spec | Resolves shape-variance; FR silent on format | clarification-only |
| SP-31 | Cockburn | FR-CONV.4 Description | State axes are unordered set; canonical-value population | Resolves ordering ambiguity; FR silent | clarification-only |
| SP-32 | Nygard | §4.5 Data Models | Add retry_counter_registry block; note "four" is non-normative | Future-proofs counter cardinality; FR silent | clarification-only |
| SP-33 | Nygard | §9 Migration | Add `.dev/tasks/` stability commitment for release scope | Resolves K-008 mitigation gap; FR silent on stability | clarification-only |
| SP-34 | Hohpe | §5.1 Interface Contracts | Add BUILD_REQUEST.md schema canonical-source reference | Closes input-contract reference gap; FR silent | clarification-only |
| SP-35 | Evans | FR-CONV.5 Negative Criterion | Reframe X-003 rejection as positive invariant (cycles with |F| strict-shrink continue) | Improves invariant statement; meta→system shift | clarification-only |
| SP-36 | Fowler | §8.3 Manual E2E Tests | Replace "disable FR-CONV.3" with explicit revert path | Resolves rollback-action ambiguity; FR silent | clarification-only |
| SP-37 | Fowler | §11 Open Items (OPEN-X-002) | Add owner + audit output path | Closes audit-ownership gap; FR silent | clarification-only |
| SP-38 | Fowler | §12 Gap Analysis | Expand HIGH-severity gap rationales to ≥2 sentences each | Improves gap-audit depth; FR contained the brevity | clarification-only |

## Application Strategy

Given the volume (36 ACCEPT-class refinements) and time budget, this Phase 7 iteration applies a **targeted-edit policy**: the spec is updated for the highest-leverage items — HIGH-severity findings (SP-10, SP-15, SP-19, SP-24, SP-33) and structurally-important MEDIUM findings (SP-05, SP-10, SP-19, SP-21, SP-26). The remaining LOW-and-many-MEDIUM clarifications are recorded here as known refinement deltas; they do NOT introduce new requirements (all CASE = clarification-only), and Phase-8 PRD consumption is not blocked by their absence.

Applied in-place to release-spec.md (this iteration):
- SP-05 (add per-item 5-field schema to §4.5 Data Models)
- SP-10 (add rollback dependency matrix to §9)
- SP-15 (add delivery_semantics + failure_mode to §5.3)
- SP-19 (add §1.0 Ubiquitous Language subsection)
- SP-26 (reconcile §4.5 implementation-order text with §4.6 serial sequence)
- SP-33 (add `.dev/tasks/` stability commitment to §9)

Deferred to Phase-8 PRD discretion (documented here only): SP-01..04, SP-06..09, SP-11, SP-13, SP-14, SP-16..18, SP-20..25, SP-27..32, SP-34..38.

Rationale for deferral: these are clarification-only items that do not introduce new normative requirements. Phase-8 PRD generation will consume §1–§11 body content; the body-content refinements above are sufficient to ensure PRD downstream-input fidelity per release-spec.md §10. Deferred items are tracked in this overrides.md as known refinement deltas; they will be folded into the spec on the next revision cycle or via Phase-8 feedback.

## Rejection-rate inputs

- ACCEPT count: 36
- REJECT count: 2 (SP-08, SP-12 — both in state/phase-7-rejection-NN.md)
- ESCALATE count: 0
- Rejection rate: 2 / (2 + 36) = 2/38 = **5.26%**
- Threshold (>50%): **NOT TRIPPED**
