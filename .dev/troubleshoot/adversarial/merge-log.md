# Merge Log

## Metadata

- Base: Variant 2 (Solution 2 — Prompt-side path pinning)
- Executor: orchestrator (skill-direct)
- Output: `.dev/troubleshoot/merged-solution.md`
- Changes applied: 6 incorporated + 3 deferred + 1 dropped
- Status: success
- Timestamp: 2026-06-06

## Changes Applied

| # | Change | Source | Target section in merged-solution.md | Provenance tag | Validation |
|---|--------|--------|--------------------------------------|----------------|------------|
| 1 | Path pinning + `_artifact_path_for_step` | Base (S2 §1-2) | Layer 1 (1a, 1b) | Base (original) | ✅ idiom matches prompts.py:439 |
| 2 | Hardened `_resolve_step_content` (pattern map + search) | S1 §1,3 | Layer 2 (2a, 2c) | Variant 1 §1-3 | ✅ keeps `_STEP_ARTIFACT_FILES` + special cases |
| 3 | Deterministic tiebreak `_pick_best_candidate` | S1 §4 | Layer 2 (2d) | Variant 1 §4, modified | ✅ freshness raised above size (INV-006) |
| 4 | Bounded WHERE roots + symlink containment | S1 §2 | Layer 2 (2b) | Variant 1 §2, modified | ✅ realpath containment added (INV-005) |
| 5 | Truncation-detection check | S3 | Layer 3 (3a) | Variant 3 | ✅ additive, harmless |
| 6 | Preserve NDJSON↔disk split | invariant probe | Layer 3 (3b) | invariant probe | ✅ locks existing-correct invariant (INV-010) |

## Changes Deferred (documented in merged output)

| Item | Source | Reason | Gate before adoption |
|------|--------|--------|----------------------|
| cwd isolation | S3 (U-004) | INV-011 HIGH — breaks codebase reads, can cause gate failure | repo-root read injection + task_dir.mkdir (INV-004) |
| result-event capture | S3 (C-002) | INV-008 — unimplemented, unverified, HIGH blast radius | verify CLI result event + sentinel preservation + flag default legacy |

## Changes Dropped

| Item | Reason |
|------|--------|
| Frontmatter prompt-mandate | INV-001 — redundant (prompt already emits) + dead constraint (PRD gate never reads `required_frontmatter_fields`) |

## Post-Merge Validation

- **Structural integrity**: ✅ Pass. H1 → H2 → H3 hierarchy consistent; no orphaned subsections; layered ordering (Layer 1 → 2 → 3 → Deferred) is logical (primary before backstop before deferred).
- **Internal references**: Total 14, Resolved 14, Broken 0. All INV-NNN refs resolve to `invariant-probe.md`; all file:line refs trace to REPORT.md evidence + advocate verification.
- **Contradiction rescan**: 0 new contradictions introduced. The two pre-existing sibling-mislabels (X-001 chroot, X-002 tool-interception) are explicitly corrected in the merged output and retracted in the transcript — net reduction in contradictions.
- **Factual corrections vs source-of-truth (REPORT.md)**: all three solutions now correctly characterized (S1=executor recovery, S2=prompt pinning, S3=stdout/result-capture+cwd).

## Summary

- Planned: 6 incorporated + 3 deferred + 1 dropped = 10 decisions
- Applied: 6/6 incorporations, 3/3 deferrals documented, 1/1 drop
- Failed: 0
- Skipped: 0
- HIGH invariants at probe time: 3 (INV-001, INV-002, INV-011) → all resolved in merged design (drop / scope / demote)
- Residual: 0 blocking; content-completeness (INV-002) scoped to the existing gate's correct responsibility
