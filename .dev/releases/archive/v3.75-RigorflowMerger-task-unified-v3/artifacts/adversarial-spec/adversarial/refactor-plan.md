# Refactoring Plan — Merge Variant C (base) with Variant A + Variant B overlays

## Overview

- **Base variant:** Variant C (sonnet:analyzer — contingent decision-tree)
- **Overlay variants:** Variant A (opus:architect — surgical) for presentation/test patterns; Variant B (opus:architect — full unification) for architectural reference content (Annexes)
- **Total planned changes:** 14 incorporations + 5 rejections (documented in §3 for transparency)
- **Overall risk:** Low. C is already the highest-scoring variant; overlays from A and B are additive (preservation patterns, release-notes framing, R3 reference appendices, break-rejection criterion).
- **Review status:** Auto-approved (non-interactive mode).
- **Convergence basis:** 86.8% over 38 diff points (CONVERGED).

---

## Planned Changes

### Change #1 — Adopt Variant A's "canonical-form-agnostic preservation test" pattern

- **Source:** Variant A §5.3 (with R2 concession refining the test to be sentinel-form-agnostic).
- **Target location in base:** C §5 test strategy. Add as new §5.2.5 (or insert into existing §5.6 "Regression tests" subsection).
- **Rationale (debate evidence):** Round 2 transcript — A conceded the original literal-string-assertion form was future-tax; revised to read canonical form from SoT constant. C's base spec does not currently include a preservation test for the carry-over strings; A's pattern fills a gap by locking the DEFER decision into CI in a way that survives future renames.
- **Integration approach:** Append. New test file `tests/skills/test_classification_sentinel_canonical.py` with one parameterized test asserting `read_canonical_sentinel_const()` produces a non-empty string that appears in the classification header output.
- **Risk level:** Low — purely additive test; no production-code change.

### Change #2 — Adopt Variant A's "Behavior changes that may surprise users" release-notes pattern

- **Source:** Variant A §6.2 (user-facing impact table).
- **Target location in base:** C §6 backward compatibility. Add as §6.5 "User-facing impact summary."
- **Rationale (debate evidence):** Round 1 — A's argument that user-facing communication is distinct from CLI-level deprecation classification. C's spec has the migration-guide table (§6.2) but not the user-facing-impact-percentage estimates that A provides.
- **Integration approach:** Replace C's bare migration-guide table with A's "what users see" framing in a new column.
- **Risk level:** Low — documentation enhancement.

### Change #3 — Carry "no new CLI flags" stance from Variant A throughout merged spec

- **Source:** Variant A §2.1 + §6.1 explicit invariant.
- **Target location in base:** C §6.1 compat guarantees.
- **Rationale (debate evidence):** A+C consensus on C-012/X-005 (80% confidence). C's spec already implies no new flags (TU-002 deferred); A makes it explicit. Strengthen by making explicit in §6.1.
- **Integration approach:** Add to C §6.1: "**CLI flag count: 8 flags. No new flags added this release.** (TU-002's `--output-type` is deferred to R3.)"
- **Risk level:** Low — explicit statement of an implicit invariant.

### Change #4 — Adopt Variant B's break-rejection criterion

- **Source:** Variant B Round 2 concession (V-B §2.4 updated).
- **Target location in base:** C §4 naming & deprecation. Add as §4.4.
- **Rationale (debate evidence):** Round 2 — B accepted C's critique that "accept breaking changes if justified" was under-constrained. The three-clause rejection criterion is portable and applies to C's framework as well: helps the decision-tree distinguish ADOPT-WITH-DEPRECATION from REJECT.
- **Integration approach:** Append. New subsection §4.4 "Break-rejection criterion":
  > A proposed behavioral break is **rejected** (not adopted-with-deprecation) if any of:
  > 1. It cannot be made backward-compatible via a 1-release shim.
  > 2. Its migration cost on the most-affected user cohort exceeds 1 hour of work.
  > 3. It depends on an unresolved investigation (DEFER-GATED in the decision-tree).
- **Risk level:** Low — policy clarification.

### Change #5 — Adopt Variant B's full YAML schema as Annex B (R3 reference)

- **Source:** Variant B §3.3 (~50 lines of YAML).
- **Target location in base:** Append as Annex B "R3 reference: tier-keywords.yaml schema (future)."
- **Rationale (debate evidence):** U-002 (90% confidence) — B's YAML schema is the most concrete artifact in any variant. Even though TU-005 defers to R3, having the schema in the merged spec gives R3 a no-rework starting point. Unanimous concession from A and C.
- **Integration approach:** Append as Annex B, with a header note: "**This annex documents the proposed schema for R3 (TU-005 single source of truth). It is NOT shipped in v3.75. It is preserved here so R3 release-planning can reference it directly.**"
- **Risk level:** Low — documentation; no production effect in v3.75.

### Change #6 — Adopt Variant B's skill sub-directory tree as Annex C (R3 reference)

- **Source:** Variant B §3.1 (full directory tree).
- **Target location in base:** Append as Annex C "R3 reference: sc-task-protocol skill sub-file layout (future)."
- **Rationale (debate evidence):** U-003 (85% confidence) — B's sub-directory tree documents how TU-006 + TU-005 + TU-002 land together. Same rationale as Change #5.
- **Integration approach:** Append as Annex C, with same "future R3" header note as Change #5.
- **Risk level:** Low — documentation.

### Change #7 — Distill Variant B's RK-U-1..6 into merged §6.3 (only deferred-candidate risks carry)

- **Source:** Variant B §6.3 (6 risks).
- **Target location in base:** C §6.3 risks table.
- **Rationale (debate evidence):** U-004 (70% confidence) — B's risk table surfaces risks A and C don't enumerate, specifically for the deferred candidates (TU-002/005/006/Q1/Q2). These should be carried forward as "risks-attached-to-deferred-candidates" so that R3 planning has the risk inventory pre-built.
- **Integration approach:** Carry these B risks into merged §6.3 as a new sub-table "Risks for deferred R3 work (informational; not in v3.75 scope):"
  - RK-U-1 (TU-002 routing reclassification)
  - RK-U-2 (YAML SoT brittleness)
  - RK-U-3 (Q1/Q2 partial-unification if A-005 finds consumer)
  - RK-U-4 (sub-file sync expansion)
  - RK-U-5 (widened keyword telemetry spike)
  - RK-U-6 (TU-002/005/006 PR ordering)
- **Risk level:** Low — documentation; these risks already exist in the project, just made explicit.

### Change #8 — Add INV-002 implementation note to §3.5 (BLOCKED state)

- **Source:** Round 2.5 invariant probe — INV-002 (MEDIUM, UNADDRESSED).
- **Target location in base:** C §3.5 BLOCKED state spec.
- **Rationale (debate evidence):** Invariant probe identified that in-flight task behavior at the release boundary is unspecified. Mitigation requires one sentence.
- **Integration approach:** Append to §3.5: "**Release-boundary note (INV-002 mitigation):** Tasks initiated before TU-004 deployment continue under their original classification. The BLOCKED state applies only to tasks initiated after deployment. No in-flight reclassification occurs."
- **Risk level:** Low.

### Change #9 — Add INV-005 audit log ordering contract to §3.7

- **Source:** Round 2.5 invariant probe — INV-005 (MEDIUM, UNADDRESSED).
- **Target location in base:** C §3.7 audit log infrastructure.
- **Rationale (debate evidence):** Invariant probe identified that multiple audit-log write paths (TU-001, TU-004, `--skip-compliance`) need ordering / atomicity contract. Mitigation requires one sentence.
- **Integration approach:** Append to §3.7: "**Concurrency contract (INV-005 mitigation):** Audit log writes within a single task lifecycle MUST be serialized through a single writer. Ordering is preserved per-task, not globally. Implementation: `audit.py` uses a per-task write lock; cross-task ordering is timestamp-based but not strictly serial."
- **Risk level:** Low — implementation guidance.

### Change #10 — Add "Considered and not adopted" subsection documenting Variant B's full-slate position

- **Source:** Debate transcript notes-for-downstream — "Contested points: B's full-slate adoption is the contested position. Should be documented in the merged output as 'considered and not adopted' with reasoning."
- **Target location in base:** New §1.7 "Considered and not adopted."
- **Rationale (debate evidence):** Transparency principle from sc:adversarial-protocol — document what was considered and rejected. B's full-slate position deserves explicit documentation so future readers understand it was evaluated.
- **Integration approach:** New subsection enumerating B's proposed full slate (TU-002, TU-005, TU-006, Q1/Q2 with shim, new `--output-type` flag, 3.0.0 major bump) with brief rationale why each was deferred to R3.
- **Risk level:** Low — documentation.

### Change #11 — Adopt Variant B's three-release plan as supplementary narrative in §7

- **Source:** Variant B §7.1 (3-release proposal).
- **Target location in base:** C §7 release-split.
- **Rationale (debate evidence):** C's release-split-protocol invocation in §7.3 already commits to whatever the protocol recommends. B's three-release narrative complements C's by spelling out the R3 release explicitly (rather than C's "deferred bundle" framing). After Round 2/3 concessions, C added target windows; merging with B's effort estimates strengthens R3 plannability.
- **Integration approach:** Replace C §7.1 with a richer §7.1 that includes B's effort estimates (R1: 3-5 days, R2: 7-10 days, R3: 5-7 days) AND C's target windows (R3 within 2 cycles, R4 no later than v3.9).
- **Risk level:** Low — narrative enhancement.

### Change #12 — Replace C §1.2 verdict-matrix TL;DR per C's R2 concession

- **Source:** Variant C Round 2 concession — add TL;DR ahead of the verdict matrix.
- **Target location in base:** C §1.2.
- **Rationale (debate evidence):** B's critique of decision-tree spec-reading overhead was accepted by C in Round 2. Adding the TL;DR matches A's lean presentation while preserving the matrix for reviewers.
- **Integration approach:** Insert TL;DR ahead of the verdict matrix:
  > **TL;DR (ships in v3.75):** TU-001, TU-003, TU-004, TU-007 (task-side); SE-001, SE-002+SE-003 paired, SE-004, SE-005 (sprint-side); TUI top-5 (P-05/P-02/P-03/P-07/P-01); audit log infrastructure.
  > **Deferred to R3 (future):** TU-002, TU-005, TU-006, Q1, Q2.
  > **Deferred to R4 (later):** SE-006.
- **Risk level:** Low — presentation enhancement.

### Change #13 — Bump version per C-013 winner (2.2.0)

- **Source:** Variant C §1.1 version-bump rationale; debate C-013 winner (C, 60% confidence).
- **Target location in base:** C §1.1.
- **Rationale (debate evidence):** A's 2.1.0 too quiet; B's 3.0.0 signals breaking changes that aren't in v3.75 itself. C's 2.2.0 minor signals "behavioral changes are present but gated by runway."
- **Integration approach:** Already in base C; no change needed. Mark as confirmed.
- **Risk level:** None.

### Change #14 — Reference invariant-probe.md in merged spec §9 acceptance criteria

- **Source:** invariant-probe.md (from this pipeline).
- **Target location in base:** C §9 acceptance criteria.
- **Rationale (debate evidence):** The invariant-probe.md gate passes (0 HIGH UNADDRESSED) — should be documented as a release-acceptance line for traceability.
- **Integration approach:** Add to §9: "**Convergence and invariant gates:** Adversarial pipeline at convergence 86.8% (CONVERGED). Invariant probe: 0 HIGH-severity UNADDRESSED. See `artifacts/adversarial-spec/adversarial/invariant-probe.md` for full findings."
- **Risk level:** None — provenance.

---

## Changes NOT being made (rejected alternatives with rationale)

### Rejection #1 — Adopt Variant B's full-slate (TU-002 + TU-005 + TU-006 + Q1+Q2 with shim) in v3.75

- **Source:** Variant B §1.2 + §2.4 + §3.3 + §3.1 + §4.2 + §4.3.
- **Why rejected:** A+C consensus on X-001..X-003, X-005..X-007 (avg 78% confidence). Round 3 — both A and C maintained the deferral position; B did not produce evidence that the full-slate's combined complexity (TU-002 routing change + TU-005 SoT YAML + TU-006 sub-files + Q1/Q2 renames + new `--output-type` flag + 3.0.0 major bump) is shippable in a single release on top of v3.7's 57-failure sprint baseline. The risk surface is too wide for the convergence margin (which selected the conservative path).
- **What carries instead:** B's YAML schema (Annex B), B's sub-file tree (Annex C), and B's three-release narrative (§7) become R3 release-planning starting points.

### Rejection #2 — Adopt Variant B's `--output-type` CLI flag (even narrowed to 2 values)

- **Source:** Variant B §2.3 + R2 concession to narrow to `{auto|override}`.
- **Why rejected:** C-012/X-005 winners A+C (80% confidence). Even narrowed, adding a flag is a surface change; A+C consensus is to keep the flag surface at 8 this release. The `--output-type` flag belongs with TU-002 in R3.
- **What carries instead:** Detection rules and gate tables documented in Annex B (with TU-005 schema) for R3 reference.

### Rejection #3 — Adopt Variant B's 3.0.0 major version bump

- **Source:** Variant B §1.1.
- **Why rejected:** C-013 winner C (60% confidence). 3.0.0 signals breaking changes in v3.75 itself, but v3.75 ships only **limited migration-guide-addressable** breaks (TU-001/004/007/SE-001/SE-002+003 paired). Major bump is premature. C's 2.2.0 (or alternatively a 2.1.x patch series) better matches the actual change surface.
- **What carries instead:** When R3 ships Q1/Q2 renames and TU-002/005/006, that release earns the major bump. v3.75 stays minor.

### Rejection #4 — Adopt Variant A's "Zero breaking changes" framing in merged spec

- **Source:** Variant A §10 variant signature + §6.1.
- **Why rejected:** X-004 winner C (65% confidence). A's framing is technically inaccurate: TU-001 #2 + #3 (CRITICAL FAIL on empty STRICT output / missing header) IS a behavioral break for STRICT users. A conceded this in Round 1 ("TU-001 IS a behavioral break for STRICT users"). The merged spec uses C's "limited migration-guide-addressable runways" framing.
- **What carries instead:** A's user-facing impact table (Change #2) — accurate communication of the changes without the "zero breaks" hyperbole.

### Rejection #5 — Adopt Variant A's literal-string carry-over preservation tests

- **Source:** Variant A §5.3 original form (before R2 concession).
- **Why rejected:** A conceded in Round 2 that the literal-string form was a future-tax. The canonical-form-agnostic form (Change #1 above) is what's adopted.
- **What carries instead:** Change #1 (canonical-form-agnostic preservation test).

---

## Risk Summary

| Change | Risk | Impact | Rollback |
|--------|------|--------|----------|
| #1 (canonical-form-agnostic test) | Low | Low — additive test | Remove test file |
| #2 (user-impact framing) | Low | Low — doc enhancement | Revert §6.5 |
| #3 (no-new-flags invariant) | Low | Low — explicit doc | Remove §6.1 line |
| #4 (break-rejection criterion) | Low | Low — policy doc | Remove §4.4 |
| #5 (Annex B YAML schema) | Low | Low — future-reference doc | Remove Annex B |
| #6 (Annex C sub-file tree) | Low | Low — future-reference doc | Remove Annex C |
| #7 (B risks distillation) | Low | Low — doc | Remove §6.3 sub-table |
| #8 (INV-002 release-boundary note) | Low | Low — implementation guidance | Remove sentence |
| #9 (INV-005 audit log contract) | Low | Low — implementation guidance | Remove sentence |
| #10 ("Considered and not adopted") | Low | Low — transparency doc | Remove §1.7 |
| #11 (three-release narrative) | Low | Low — doc enhancement | Revert §7.1 |
| #12 (verdict-matrix TL;DR) | Low | Low — presentation | Remove TL;DR |
| #13 (2.2.0 confirmation) | None | None | n/a |
| #14 (invariant gate reference) | None | None — provenance | Remove line |

**Overall risk:** All 14 changes are Low or No-risk. No structural changes to the base; all are additive overlays or explicit documentation of already-implied positions.

---

## Review Status

- **Status:** Auto-approved (non-interactive mode).
- **Approval timestamp:** 2026-05-14.
- **Approver:** sc-adversarial-protocol pipeline (debate-orchestrator).

---

## Provenance summary (for merge executor)

| Source | Sections / blocks in merged output |
|--------|------------------------------------|
| Variant C (base) | §1 (with TL;DR overlay), §2, §3 (with INV-002/INV-005 notes), §4 (with §4.4 break-rejection), §5 (with §5.2.5 preservation test), §6 (with §6.3 deferred-risks sub-table, §6.5 user-impact), §7 (with three-release narrative overlay), §8, §9 (with invariant-gate reference), §10 |
| Variant A (overlay) | §5.2.5 (preservation test), §6.5 (user-impact framing), §6.1 (no-new-flags invariant) |
| Variant B (overlay + annex) | §4.4 (break-rejection criterion), §6.3 sub-table (deferred-risks), §7.1 (effort estimates), Annex B (YAML schema), Annex C (sub-file tree) |
| Adversarial synthesis | §1.7 (Considered and not adopted), §9 invariant-gate line, INV-002 / INV-005 mitigation notes |
