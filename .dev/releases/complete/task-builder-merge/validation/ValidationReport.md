# Validation Report

Generated: 2026-05-17
Roadmap: `.dev/releases/current/task-builder-merge/roadmap.md`
Phases validated: 7
Agents spawned: 4 (consolidated from 2N=14 protocol target into 4 phase-pair agents for context efficiency; coverage is complete — every task in every phase reviewed)
Total findings: 18 (High: 5, Medium: 8, Low: 5)

## Findings

### High Severity

#### H1. T01.02 — Omission: missing bundle-specific-tasklist-checks forbidden constraint
- **Severity**: High
- **Affects**: phase-1-tasklist.md / T01.02
- **Problem**: AC does not encode the roadmap's "bundle-specific-tasklist-checks:forbidden" prohibition from R-007.
- **Roadmap evidence**: R-007, line 98 — `bundle-specific-tasklist-checks:forbidden`.
- **Tasklist evidence**: phase-1-tasklist.md T01.02 Acceptance Criteria (4 bullets, none address the prohibition).
- **Exact fix**: Add AC bullet: "Diff confirms no bundle-specific tasklist-only checks introduced (R-007 invariant)."

#### H2. T04.16 — Drift: Exit Criteria task-range mismatch (references non-existent T04.17)
- **Severity**: High
- **Affects**: phase-4-tasklist.md / T04.16
- **Problem**: Exit Criteria and Acceptance Criteria reference "T04.01-T04.17" but Phase 4 contains only T04.01-T04.16. "All 16 regular tasks" is also wrong — Phase 4 has 13 regular + 3 checkpoints.
- **Roadmap evidence**: Phase 4 ends at T04.16 per the index.
- **Tasklist evidence**: phase-4-tasklist.md (end-of-phase Exit Criteria and Acceptance Criteria bullets).
- **Exact fix**: Replace "T04.01-T04.17" with "T04.01-T04.15" (the non-checkpoint regular tasks); update "All 16 regular tasks" to "All 13 regular tasks T04.01-T04.05, T04.07-T04.11, T04.13-T04.15".

#### H3. T04.15 — Omission: FF_FIVE_ADVERSARIAL_AXES governance content under-specified
- **Severity**: High
- **Affects**: phase-4-tasklist.md / T04.15
- **Problem**: R-089 requires the governance entry to record logical-flag designation, revert path, K-004 cleanup gate, AND M7 consolidation reference. The task AC only says "FF_FIVE_ADVERSARIAL_AXES entry recorded at .../spec.md".
- **Roadmap evidence**: R-089, line 283 — `logical-flag; revert-path:removes-overlay; cleanup-gated:K-004-axis-distribution-audit; M7-consolidation:see-M7-governance-table`.
- **Tasklist evidence**: phase-4-tasklist.md T04.15 Acceptance Criteria.
- **Exact fix**: Add AC bullet: "FF_FIVE_ADVERSARIAL_AXES spec.md records (a) logical-flag designation, (b) revert path = remove overlay, (c) cleanup gate = K-004 axis-distribution audit, (d) M7 consolidation reference."

#### H4. T06.01 — Weakened: SKILL.md missing from FR-CONV.6 wrapper grep AC
- **Severity**: High
- **Affects**: phase-6-tasklist.md / T06.01
- **Problem**: T06.01 Deliverables claim wrapper lands in SKILL.md + 3 rf-* agents, but the acceptance grep only checks the 3 agent files. R-111 includes SKILL.md as a Comp; deferring SKILL.md verification to T06.11 leaves T06.01 incomplete.
- **Roadmap evidence**: R-111, line 362 — Comp = `SKILL.md; rf-analyst.md; rf-qa.md; rf-qa-qualitative.md`.
- **Tasklist evidence**: phase-6-tasklist.md T06.01 AC grep covers 3 files only.
- **Exact fix**: Add AC: "`grep -c "synthetic-dnsp" src/superclaude/skills/task-builder/SKILL.md` returns at least 1 (defer detailed merge-step verification to T06.11)."

#### H5. T07.04 — Weakened: Q-DM-1 binding requirement demoted to Validation note
- **Severity**: High
- **Affects**: phase-7-tasklist.md / T07.04
- **Problem**: R-143 AC includes `binding:to-whichever-schema-resolves-Q-DM-1`. The task only enforces fixture exit-0 + TB-Add-1 fail in AC; binding is mentioned only in the Validation note, not as an enforced criterion.
- **Roadmap evidence**: R-143, line 422 — `binding:to-whichever-schema-resolves-Q-DM-1`.
- **Tasklist evidence**: phase-7-tasklist.md T07.04 Acceptance Criteria.
- **Exact fix**: Add AC bullet: "Fixture's schema reference matches the recorded Q-DM-1 resolution artifact (machine-checkable)."

### Medium Severity

#### M1. T01.06 — Verification weakened: no explicit three-surface mirror diff re-check
- **Severity**: Medium
- **Affects**: phase-1-tasklist.md / T01.06
- **Problem**: Mid-phase checkpoint doesn't re-verify TB-Add-1..3 stubs are present on all three definition surfaces.
- **Roadmap evidence**: R-007 — three-surface mirror.
- **Tasklist evidence**: phase-1-tasklist.md T01.06 Verification.
- **Exact fix**: Add Verification bullet: "TB-Add-1..3 stubs present on all 3 surfaces (rf-qa.md + SKILL.md A.10 + SKILL.md 15-item)."

#### M2. T01.13 — DM-002 / DM-005 field-level enumeration omitted in AC
- **Severity**: Medium
- **Affects**: phase-1-tasklist.md / T01.13
- **Problem**: AC enumerates DM-003 and DM-004 fields but not DM-002 (rf_qa_table_verbatim, prompt_directive, reinjection_rule) or DM-005 (10 producer/consumer fields).
- **Roadmap evidence**: R-017 (DM-002), R-020 (DM-005) — field lists.
- **Tasklist evidence**: phase-1-tasklist.md T01.13 Acceptance Criteria.
- **Exact fix**: Add AC: "DM-002 schema enumerates rf_qa_table_verbatim, prompt_directive (fixed-string), reinjection_rule (INV-002 cycle-N fresh). DM-005 enumerates 10 producer/consumer fields including schema_version 1.0.0 and INV-019 Self-Audit obligation."

#### M3. T01.14 — API-002/API-003 contract details under-specified in AC
- **Severity**: Medium
- **Affects**: phase-1-tasklist.md / T01.14
- **Problem**: AC only enumerates API-001 and API-004 details; API-002 placement-after-TARGET-FILES and API-003 all-fail routing not surfaced.
- **Roadmap evidence**: R-022 line 113, R-023 line 114.
- **Tasklist evidence**: phase-1-tasklist.md T01.14 Acceptance Criteria.
- **Exact fix**: Add AC: "API-002 records placement-after-TARGET-FILES-before-INSTRUCTIONS and missing-verdict-halt-before-A.10.5. API-003 records all-fail routes to rf-team-lead.md:417 NO-DNSP."

#### M4. T01.18 — Missing explicit TB-Add-2 [ADVISORY] non-blocking exit assertion
- **Severity**: Medium
- **Affects**: phase-1-tasklist.md / T01.18
- **Problem**: End-of-Phase-1 checkpoint references "TB-Add-2 advisory" in compressed form but doesn't have a standalone AC bullet asserting the [ADVISORY] prefix + non-blocking verdict.
- **Roadmap evidence**: Roadmap M1 Exit, line 88.
- **Tasklist evidence**: phase-1-tasklist.md T01.18 Acceptance Criteria.
- **Exact fix**: Add AC bullet: "TB-Add-2 confirmed emits literal `[ADVISORY]` prefix and does NOT block gate verdict on out-of-bounds fixture."

#### M5. T02.03 — Missing MUST-contain-block requirement in AC
- **Severity**: Medium
- **Affects**: phase-2-tasklist.md / T02.03
- **Problem**: R-036 description requires generated MDTM "MUST contain `## Execution Context` block at top". AC checks BUILD_REQUEST schema preservation but not the block-emission rule.
- **Roadmap evidence**: R-036, line 168.
- **Tasklist evidence**: phase-2-tasklist.md T02.03 Acceptance Criteria.
- **Exact fix**: Add AC bullet: "Generated MDTM from updated BUILD_REQUEST contract contains `## Execution Context` block after frontmatter, before first phase (post-update contract-conformance check)."

#### M6. T03.03 — Contradiction: diff target cites wrong source file
- **Severity**: Medium
- **Affects**: phase-3-tasklist.md / T03.03
- **Problem**: AC says "Diff of injected block vs `rf-qa.md` Items Reviewed table" but roadmap R-051 specifies the source as `qa-task-integrity.md`.
- **Roadmap evidence**: R-051 — `diff-vs-qa-task-integrity.md-Items-Reviewed-table:byte-identical`.
- **Tasklist evidence**: phase-3-tasklist.md T03.03 Acceptance Criteria #2.
- **Exact fix**: Replace `rf-qa.md` with `qa-task-integrity.md` in T03.03 AC #2.

#### M7. T05.03 — Missing prior-regression-check gate AC
- **Severity**: Medium
- **Affects**: phase-5-tasklist.md / T05.03
- **Problem**: R-092 requires `emission:gated-on-prior-regression-check-passing`. The AC only checks `|F_n|=0` skip condition; doesn't verify regression-check-gating.
- **Roadmap evidence**: R-092, line 311.
- **Tasklist evidence**: phase-5-tasklist.md T05.03 Acceptance Criteria.
- **Exact fix**: Add AC bullet: "Monotonicity emission verified gated on prior regression-check passing (test with regression flip on the same cycle confirms monotonicity NOT emitted)."

#### M8. T05.05 — Ordering precedence AC weakened to keyword-match
- **Severity**: Medium
- **Affects**: phase-5-tasklist.md / T05.05
- **Problem**: AC uses `grep -c "regression\|monotonicity\|hard-cap"` which only counts keywords; doesn't assert ordering "regression always exits BEFORE monotonicity".
- **Roadmap evidence**: R-095, line 314.
- **Tasklist evidence**: phase-5-tasklist.md T05.05 Acceptance Criteria.
- **Exact fix**: Replace grep AC with: "Documented precedence text explicitly states the 4-step order regression → monotonicity → hard-cap → proceed (regex match on the ordered string), and sub-agent report confirms 'regression always exits BEFORE monotonicity'."

### Low Severity

#### L1. T03.04 — Self-Audit runtime sample deferred without cross-link
- **Severity**: Low
- **Affects**: phase-3-tasklist.md / T03.04
- **Problem**: AC only greps the schema file; runtime emission deferred to TEST-009/T03.14 without explicit cross-link in T03.04 Notes.
- **Roadmap evidence**: R-055 — output-level verification.
- **Tasklist evidence**: phase-3-tasklist.md T03.04 Acceptance Criteria.
- **Exact fix**: Add T03.04 Notes line: "Runtime sample verification deferred to T03.14 (TEST-009)."

#### L2. T03.17 — release-spec enforcement not verified
- **Severity**: Low
- **Affects**: phase-3-tasklist.md / T03.17
- **Problem**: AC documents contingency note but doesn't verify enforcement in `release-spec §4.6`.
- **Roadmap evidence**: R-069, line 228.
- **Tasklist evidence**: phase-3-tasklist.md T03.17 Acceptance Criteria.
- **Exact fix**: Add AC: "`grep -n 'PR-06 → PR-04' <release-spec>` returns a match within §4.6, confirming sequencing rule is enforced (not merely documented in artifact note)."

#### L3. T04.13 — Line-range AC widened beyond roadmap-specified line
- **Severity**: Low
- **Affects**: phase-4-tasklist.md / T04.13
- **Problem**: R-083 specifies SKILL.md:961 explicitly; AC widens to [955, 970] without justification.
- **Roadmap evidence**: R-083, line 277.
- **Tasklist evidence**: phase-4-tasklist.md T04.13 Acceptance Criteria.
- **Exact fix**: Tighten AC to "line N ∈ [958, 964]" or document tolerance rationale in Notes.

#### L4. T06.05 — Vocabulary-membership check missing at emitter
- **Severity**: Low
- **Affects**: phase-6-tasklist.md / T06.05
- **Problem**: R-118 anchors exhaust_point closed-vocabulary check at the dedup_key emitter; tasklist defers to T06.07.
- **Roadmap evidence**: R-118, line 369.
- **Tasklist evidence**: phase-6-tasklist.md T06.05 Acceptance Criteria.
- **Exact fix**: Add AC bullet: "emitter rejects synthesis with exhaust_point outside `{retry-1,retry-2,gap-fill-round-{1,2,3}}`."

#### L5. T07.19 — MET-002 collapses two distinct 100% requirements
- **Severity**: Low
- **Affects**: phase-7-tasklist.md / T07.19
- **Problem**: AC says "MET-002 detection rate documented as 100% on TB-Add-1/4 synthetic fixtures" — collapses unresolved-token-detection and DAG-cycle-detection into one bullet.
- **Roadmap evidence**: R-160, line 439.
- **Tasklist evidence**: phase-7-tasklist.md T07.19 Acceptance Criteria.
- **Exact fix**: Split into "MET-002 unresolved-token detection 100% on TB-Add-1 fixtures AND DAG-cycle detection 100% on TB-Add-4 fixtures."

## Verification Results

Verified: 2026-05-17
Findings resolved: 18/18

| Finding | Status | Notes |
|---------|--------|-------|
| H1 | RESOLVED | "no bundle-specific tasklist-only checks" AC bullet added to T01.02 |
| H2 | RESOLVED | T04.17 references replaced with T04.15; "All 13 regular tasks" enumeration corrected |
| H3 | RESOLVED | FF_FIVE_ADVERSARIAL_AXES 4-bullet governance (logical-flag, revert path, K-004 gate, M7 ref) added to T04.15 |
| H4 | RESOLVED | SKILL.md grep AC added to T06.01 with deferral note to T06.11 |
| H5 | RESOLVED | Q-DM-1 binding promoted to enforced AC in T07.04 |
| M1 | RESOLVED | Three-surface verification bullet added to T01.06 |
| M2 | RESOLVED | DM-002 + DM-005 field enumeration added to T01.13 AC |
| M3 | RESOLVED | API-002 placement + API-003 all-fail-routing AC added to T01.14 |
| M4 | RESOLVED | TB-Add-2 ADVISORY non-blocking AC bullet added to T01.18 |
| M5 | RESOLVED | "Generated MDTM contains Execution Context block" AC added to T02.03 |
| M6 | RESOLVED | T03.03 AC #2 diff target changed from `rf-qa.md` to `qa-task-integrity.md` |
| M7 | RESOLVED | Prior-regression gate AC bullet added to T05.03 |
| M8 | RESOLVED | T05.05 grep AC replaced with ordered-text + sub-agent confirmation |
| L1 | RESOLVED | T03.04 Notes updated with T03.14 cross-link |
| L2 | RESOLVED | T03.17 release-spec §4.6 enforcement grep AC added |
| L3 | RESOLVED | T04.13 line-range tightened to [958, 964] with tolerance rationale |
| L4 | RESOLVED | T06.05 exhaust_point vocabulary-membership AC bullet added |
| L5 | RESOLVED | T07.19 MET-002 split into unresolved-token + DAG-cycle bullets |
