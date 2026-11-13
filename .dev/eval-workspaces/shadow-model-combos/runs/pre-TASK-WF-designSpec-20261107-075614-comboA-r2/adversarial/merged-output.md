<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 3 (opus:refactorer) -->
<!-- Merge date: 2026-11-13T05:15:00Z -->
<!-- Non-base sources incorporated: V1 (analyzer/sonnet) F1,F2,F3,F4; V2 (qa/haiku) F2 (merged into MF7), F1 (evidence note) -->

# Merged verdict — reflect pre-execution audit, TASK-WF-designSpec-20261107-075614 (comboA-r2)

Audit posture: frozen spec+plan pair; facts pinned at e8db2fe6; the landed implementation and the done-package history were not audited. Blocking rule: a finding blocks when a plan executor following the plan as written would ship a wrong or unverified artifact.

## Summary counts

- Raw findings: 13 (V1: 4, V2: 2, V3: 7)
- Merged plan-facing findings: 11 (one 2-source merge: MF7 = V2 F2 + V3 F4)
- Evidence-layer notes (not plan defects): 1 (V2 F1: matrix completeness)
- Blocking: 4 (MF1, MF2, MF3, MF4 — all MAJOR)
- Non-blocking: 7 (MF5..MF11 — all MINOR)

## Merged findings

<!-- Source: Variant 3, F1 (debate C-004; blocking upgraded by debate from card's false) -->
- **MF1** [MAJOR, blocking=true, confidence 0.85, category missing-requirement] Spec: a draft_guard_unavailable halt reports unavailable. Engage rows 3/8 halt before any request, so the fold is None and guard_status maps 'no record' to released. No task places the halt override and no AC tests it; Task 3 asserts released for no record. Fix: Task 3 or Task 8 must place the halt override (SKILL-level, at halt time) and an AC must assert `merge_guard: unavailable` on the engage-failure exit. Cites spec:112, spec:135-140, plan:61, plan:124.

<!-- Source: Variant 1, F1 (debate C-001) -->
- **MF2** [MAJOR, blocking=true, confidence 0.80, category contradiction] Fold returns a dict (subscripted in Task 5 acceptance) but decision functions read guard.phase/.baseline by attribute; plan never fixes the type or Phase string values, so Task 4 and Task 5 criteria can conflict — two implementers can each pass their own task's ACs and produce mutually incompatible modules. Fix: Task 3 pins the representation (e.g. a frozen dataclass OR a plain dict, plus Phase as str-Enum with pinned values) and Task 5's AC matches it. Cites spec:187-192, spec:118-119, plan:90, plan:56.

<!-- Source: Variant 1, F2 (debate C-002) -->
- **MF3** [MAJOR, blocking=true, confidence 0.80, category unpassable-check] resume_decision row 4 must re-enter release_decision but has no cycle_id/target_sha/applied_edits inputs; Task 4's criterion gives no expected action/cause for row 4, so the contract is unimplementable as stated and a wrong re-entry result cannot fail any AC. Fix: pin whether row 4 returns a decision or a SKILL-consumed marker, extend the signature (or document the SKILL-side inputs), and state the expected action/cause in the row-4 AC. Cites spec:109, spec:166, plan:70, plan:77.

<!-- Source: Variant 1, F3 (debate C-003; sibling of MF1) -->
- **MF4** [MAJOR, blocking=true, confidence 0.75, category missing-requirement] Fold row for settled(any, skipped, user_override) does not set disabled_cause, yet guard_status keys user_override off it; plan tests fold and status separately (status AC uses constructed inputs, not fold-produced records), so a wrong report of off/unavailable would ship. Fix: the fold ACs add the user_override row asserting disabled_cause, and the guard_status AC consumes fold-produced records. Cites spec:206, spec:112, plan:60-61.

<!-- Source: Variant 3, F2 (debate C-005) -->
- **MF5** [MINOR, blocking=false, confidence 0.70, category missing-requirement] The S5a and Wave 6 pre-push sentences are checked 'byte-identical' only against their recorded literal START text, so an edit inside the pinned sentence after its prefix (the edit O4 forbids) passes Task 10's AC. Fix: Task 1 records the full pinned sentences, not their start text. Cites spec:342, spec:377, plan:33, plan:154.

<!-- Source: Variant 3, F3 (debate C-006) -->
- **MF6** [MINOR, blocking=false, confidence 0.65, category missing-requirement] A ready request settled not_applied must return to RELEASE_PENDING when a failed release preceded it. Task 3's fold AC tests only the HELD result, so a fold hard-coding HELD for ready not_applied passes. Fix: add the failed-release-preceded variant to the fold ACs. Cites spec:201, plan:60.

<!-- Source: Variant 2 F2 + Variant 3 F4 merged (debate C-007) -->
- **MF7** [MINOR, blocking=false, confidence 0.70, category missing-requirement] Tasks 9, 10, 12 and 13 consume ./artifacts/pre-build-gate.md (Task 1 output) but none declares 'Depends on: Task 1'; Task 8 lists it directly, against the spec's rule to declare every consumed output. Transitive order is preserved; hygiene deviation only. Fix: add the four Depends-on lines. Cites spec:363, plan:120-122, 134-137, 148-154, 179-182, 190-199.

<!-- Source: Variant 3, F5 (debate C-008) -->
- **MF8** [MINOR, blocking=false, confidence 0.55, category contradiction] Task 9's body allows adding a WRITE_VERB_CLASSIFICATION entry if a gh pr/gh api line is unavoidable, but its AC permits no edit to existing test expectations except those of Tasks 2, 5, 7 and 8, excluding Task 9's own entry. Fix: add Task 9 to the AC's exception list. Cites plan:137, plan:142.

<!-- Source: Variant 3, F6 (debate C-009) -->
- **MF9** [MINOR, blocking=false, confidence 0.70, category contradiction] Constraints restate the owner decision as 'release gate for G4 and G5' and Task 12 names only G4/G5 as OPEN, but spec section 8 and plan line 24 make G1 live, G2 live, G4, G5 and G6 the release gate. Fix: carry the five-gate list in Constraints and Task 12. Cites spec:326, plan:24-26, plan:182.

<!-- Source: Variant 3, F7 (debate C-010) -->
- **MF10** [MINOR, blocking=false, confidence 0.70, category missing-requirement] The 'no file:NNN pointer' rule for new protocol prose is stated (Constraints, Task 8 body) but no AC tests it: Task 8's protocol test checks only for src/superclaude, and Tasks 9/10 check only the two forbidden words. Fix: extend the protocol test with a file:NNN absence assertion. Cites spec:369, plan:23, plan:124-128, plan:143.

<!-- Source: Variant 1, F4 (debate C-011, downgraded to MINOR on steelman) -->
- **MF11** [MINOR, blocking=false, confidence 0.60, category contradiction] Spec section 3 says resume reconciles unsettled requests at any ordinal, but resume row 2 returns REPORT_HELD first below ordinal 3 or in off mode; plan pins row-2 precedence without noting that it consciously overrides the reconcile-before-edit phrasing (vacuous below ordinal 3, where nothing mutates). Fix: one sentence in Task 4 noting the precedence and why it is safe. Cites spec:58, spec:164-165, plan:76.

## Evidence-layer note (not a plan defect)

<!-- Source: Variant 2, F1 (debate C-012) -->
- The Step-1B.0 Pass-2 inferred matrix (45 rows) omits three requirement-bearing spans — the loop-guard enumeration update (spec:242), the state-machine overlay note (spec:243) and the public package exports (spec:291) — all covered by Tasks 2, 10 and 5 respectively. The 45/45 union coverage therefore measures the extraction, not the full spec body. Recorded in the report header and the Inferred-requirements postscript; no plan change required.

## Verdict

**blocking-findings-present** — 4 blocking findings (MF1-MF4) against executing the plan as written; all four are plan-text fixes (pin the type, pin the row-4 result, add two fold/status ACs), not redesigns. Convergence 1.00 (14/14 dispositioned; confidence-weighted 0.71).
