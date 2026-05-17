# Merge Log — Validation Spec Synthesis

## Metadata

- **Base variant:** variant-2 (combined score 0.947)
- **Executor:** sc:adversarial merge-executor (Step 5)
- **Plan applied:** refactor-plan.md (14 planned changes; 3 rejected alternatives)
- **Output:** `validation-spec.md` (at output root)
- **Status:** success
- **Timestamp:** 2026-05-15

## Changes Applied

| # | Change | Status | Provenance Tag | Validation |
|---|---|---|---|---|
| 1 | Executive section reframe to three-clause verdict | Applied | `<!-- Source: V2 § 1 + V1 § 1 + V3 § 11 (restructured) -->` | Three-clause structure verified |
| 2 | Insert TU/ME positive-validation overlay (§ 2) | Applied | `<!-- Source: V1 §§ 2–3 (incorporated as defense overlay) -->` | All 8 TUs + 5 named MEs present |
| 3 | Adopt V3 empirical evidence (§ 3) | Applied | `<!-- Source: V3 § 2 (in-flight MDTM enumeration) -->` | 96-file count + 149+ ref count preserved |
| 4 | Restructure INV-04 frame around parse-vs-semantic (§ 4) | Applied | `<!-- Source: V3 § 7 + V2 § 2.3 (parse-vs-semantic restructure) -->` | Both layers explicit |
| 5 | Preserve V2 § 3 CR-TASK-* attacks with V1 asymmetry edit (§ 5) | Applied | `<!-- Source: V2 § 3 + V1 R2 asymmetry distinction -->` | All 10 CR-TASK attacks preserved; AC-ATK-10 amended |
| 6 | Preserve V2 §§ 4–5 verbatim (§ 6) | Applied | `<!-- Source: V2 §§ 4–5 (CR-DEP, CR-DIST, CR-REF, CR-DOC) -->` | Bucket-condensation + 67-vs-65 + CR-DOC-01 disambiguation preserved |
| 7 | Adopt V3 §§ 3–5 sequencing-constraint probes (§ 7) | Applied | `<!-- Source: V3 §§ 3–5 (S-1, S-2, S-3 probes) -->` | All three constraint probes + mitigations preserved |
| 8 | Adopt V3 § 6 post-CR-DEP-03 residual-reference probe (§ 8) | Applied | `<!-- Source: V3 § 6 (CR-DEP-06 proposal) -->` | CR-DEP-06 proposal text preserved |
| 9 | Merge V2 § 6 + V3 § 9 invariant attack table (§ 9) | Applied | `<!-- Source: V2 § 6 + V3 § 9 (merged invariant table) -->` | All 5 invariant rows present; V3 augmentations integrated |
| 10 | Append V3 scenarios H-1..H-4 after V2 scenarios A..G (§ 10) | Applied | `<!-- Source: V2 § 7 (scenarios A..G) + V3 § 8 (scenarios H-1..H-4) -->` | 11 scenarios total |
| 11 | Consolidated AC list AC-ATK-01..18 + AC-SM-01..12 (§ 11) | Applied | `<!-- Source: V2 § 8 (AC-ATK-01..15) + V3 § 10 (AC-ATK-16..18) + V1 § 7 (AC-SM-01..12) -->` | 30 ACs total |
| 12 | Preserve V2 §§ 9–11 verbatim (tradeoffs / FMs / evidence audit; §§ 12–14) | Applied | `<!-- Source: V2 §§ 9–11 -->` | All 8 tradeoffs + 8 FMs + 4 evidence gaps preserved |
| 13 | Add V1 § 6 residual-risk section (§ 15) | Applied | `<!-- Source: V1 § 6 (5 honest concessions) -->` | All 5 concessions preserved |
| 14 | Verdict synthesis to three-clause verdict (§ 16) | Applied | `<!-- Source: V1 § 7 + V2 § 12 + V3 § 11 (synthesized) -->` | Three-clause structure preserved |

## Post-Merge Validation

### Structural Integrity

- ✅ Pass — heading hierarchy consistent (H1 → H2 → H3, no orphaned subsections, no level gaps)
- ✅ Pass — section ordering is logical (frontmatter → verdict → defense overlay → empirical evidence → per-CR attacks → sequencing probes → invariant tables → scenarios → ACs → tradeoffs → FMs → evidence audit → residual risks → final verdict)
- ✅ Pass — document starts with frontmatter + H1

### Internal References

- Total cross-references: 64 (line numbers in source plan, § N references in merged spec, AC-ATK-NN, AC-SM-NN, CR-IDs, TU-N, ME-N, INV-NNN)
- Resolved: 64
- Broken: 0

### Contradiction Re-Scan

Re-ran contradiction detection on merged document.

- New contradictions introduced: 0
- Carry-forward contradictions: 6 (X-001..X-006) — resolved per debate (winner adopted with rationale)

### Provenance Annotations

- Total annotation tags applied: 14 (one per applied change)
- Document header: `<!-- Provenance: This document was produced by /sc:adversarial. Base: variant-2. Merge date: 2026-05-15. -->`
- All sections traceable to source variant(s)

## Summary

- Planned changes: 14
- Applied successfully: 14
- Failed: 0
- Skipped: 0

**Final status: success.** Merged validation spec written to `.dev/releases/current/task-sc-task-directional-merge/validation-spec/validation-spec.md`.

## Return Contract

```yaml
merged_output_path: ".dev/releases/current/task-sc-task-directional-merge/validation-spec/validation-spec.md"
convergence_score: 0.86
artifacts_dir: ".dev/releases/current/task-sc-task-directional-merge/validation-spec/adversarial/"
status: "success"
base_variant: "variant-2"
unresolved_conflicts: 5
fallback_mode: false
failure_stage: null
invocation_method: "skill-direct"
unaddressed_invariants: []  # 1 HIGH UNADDRESSED resolved in Round 3 via CR-FM-03 content-level extension
```

**Unresolved conflicts (5)** are reasoned non-resolutions, not failures:
- S-001 (section count) — cosmetic; no superior shape exists
- S-005 (frontmatter stance label) — cosmetic
- A-001 (INV-01..INV-05 completeness) — out of scope; would require sixth-invariant proposal
- C-014 (md5 collision) — accepted as mitigation but classified adversarial-only LOW
- Two further low-severity diff points within U-001..U-018 where both stances were adopted side-by-side
