# Diff Analysis: Merge-Conflict Resolution Comparison

## Metadata
- Generated: 2026-06-04
- Variants compared: 3 (variant-1-proposed, variant-2-ours, variant-3-theirs)
- Total differences found: 1 (structural/cosmetic)
- Categories: structural (0), content (1), contradictions (0), unique (0), shared assumptions (1)
- Similarity (ours↔theirs differing-fraction): 0.0855% — **below 10% threshold → `variants_too_similar` path active**

## Method
Comparison performed at two levels:
1. **Byte-level** (`diff`): PROPOSED == OURS verbatim; PROPOSED vs THEIRS differs on exactly 1 line (436).
2. **AST-level** (`ast.parse` + node-set extraction): all three variants expose an **identical set of 66 fully-qualified test nodes** across 12 classes. OURS and THEIRS added the **same 4 nodes** relative to BASE:
   - `TestSignaturesChecker._write_md_fixture_with_allowlist`
   - `TestSignaturesChecker.test_phantom_id_honors_explicit_non_references_for_milestone_d_ids`
   - `TestSignaturesChecker.test_phantom_id_backward_compatible_without_explicit_non_references`
   - `TestSignaturesChecker.test_phantom_id_bare_d_still_resolves_when_spec_uses_bare_d`

## Structural Differences
| # | Area | Variant 1 (proposed) | Variant 2 (ours) | Variant 3 (theirs) | Severity |
|---|------|----------------------|------------------|--------------------|----------|
| — | (none) | identical class/heading structure | identical | identical | — |

No structural differences. Heading hierarchy, class ordering, and method ordering identical across all three.

## Content Differences
| # | Topic | Variant 1 (proposed) | Variant 2 (ours) | Variant 3 (theirs) | Severity |
|---|-------|----------------------|------------------|--------------------|----------|
| C-001 | Section-header comment (line 436) | `# R5 (PR #111 port, commit 861047c2): MD-family + Explicit non-references allowlist` | same as proposed | `# TASK-RF-20260531-044100 Phase 6: MD-family + Explicit non-references allowlist` | Low |

C-001 is a **comment-only** difference. It is not parsed by Python, not collected by pytest, and changes no assertion, fixture, or expected value. Taxonomy auto-tag: **L1 (surface)** — signal terms "comment", "wording", "presentation". Both labels describe the same code block; they differ only in provenance attribution (branch-local port label vs. master task-id label).

## Contradictions
| # | Point of Conflict | Position | Impact |
|---|-------------------|----------|--------|
| — | (none) | — | — |

No contradictions. Critically, the 113-line added block — including all 3 MD-family test bodies and the `_write_md_fixture_with_allowlist` helper — is **byte-identical** between OURS and THEIRS. There is zero divergence in any expected-value assertion (e.g., both assert `len(sig_findings) == 0` for the M{n}-D{nn} + allowlist case; both assert the same drift/phantom counts).

## Unique Contributions
| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| — | (none) | No variant carries any unique test node | — |

Every test node present in any variant is present in all three. There is no unique coverage on either side to preserve or drop.

## Shared Assumptions
| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | The MD-family canonical form is `M\d+-D-?\d+` (per `superclaude.contracts.ID_PATTERNS["MD"]`), so `M1-D01` and `M2-D01` resolve as distinct IDs and the bare-`D` allowlist exempts only roadmap-internal sequence indices | Both sides' identical test bodies assert this (zero signatures findings for the M{n}-D{nn}+allowlist fixture) | If the production canonicalizer's MD pattern drifted from the contract, BOTH sides' tests would fail identically — the merge does not mask this | STATED (verified against contract) |

## Summary
- Total structural differences: 0
- Total content differences: 1 (C-001, Low/L1 cosmetic)
- Total contradictions: 0
- Total unique contributions: 0
- Total shared assumptions surfaced: 1 (STATED: 1, UNSTATED: 0, CONTRADICTED: 0)
- Highest-severity items: none above Low
- **Conclusion**: variants substantially identical (99.91%). Only diff point is C-001, a comment-header provenance label.
