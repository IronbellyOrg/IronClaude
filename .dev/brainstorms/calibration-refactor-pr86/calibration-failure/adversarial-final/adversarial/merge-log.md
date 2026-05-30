# Merge Log

## Metadata

- Base: Variant 1 (A-merged, opus advocate)
- Executor: orchestrator inline-fallback (Task subagent fan-out unavailable in single-thread context)
- Changes applied: 4 of 4 planned
- Status: success
- Timestamp: 2026-05-26T19:35Z

## Changes Applied

### Change #1 — Insert opening synthesis paragraph from B §1

- Status: APPLIED
- Before: A's title block followed directly by "Methodology & Channel Disclosure"
- After: Inserted new "## Top-line synthesis" section between title block and Methodology section
- Provenance tag: `<!-- Source: Variant 2 (B), §1 — merged per Change #1 -->`
- Validation: New paragraph is exact verbatim of B line 12 (executive-synthesis sentence). No conflict with downstream content.

### Change #2 — Refactor M3 to composite (replace A T3 + §S1/§S2 with M3a/M3b/M3c from C)

- Status: APPLIED
- Before: A's "Theory 3 — Verdict-Direction Asymmetry" (A lines 90-112) + "Secondary mechanisms §S1 (stripped-context) + §S2 (anchoring)" (A lines 140-153)
- After: Single "## M3 — Verdict-Direction Asymmetry and Anchoring-Channel Loss (composite)" section with three subsections M3a (0.78), M3b (0.65), M3c (0.45)
- Provenance tag: `<!-- Source: Variant 3 (C), lines 64-103 — merged per Change #2 (X-001 MERGE outcome) -->`
- Content preserved: All evidence citations from A's T3 and §S1/§S2 are preserved (re-distributed to M3a, M3b, M3c respectively). All three systemic fixes preserved.
- Validation: M3a fix (verdict-direction modifier) + M3b fix (Falsification standard card field) + M3c fix (dual-instance-minimum) all preserved. No fix loss.

### Change #3 — Append C's M4 prevention + recursion bullets to Cross-mechanism implications

- Status: APPLIED
- Before: A's cross-theory §157-170 with 5 bullets ending at "Substrate-vs-H3 fidelity caveat"
- After: Two new bullets inserted before the "Substrate-vs-H3 fidelity caveat" bullet: "M4 is the prevention mechanism for all three diagnostic mechanisms" and "Recursion-of-anti-pattern"
- Provenance tag: Per-bullet inline `(provenance: Variant C line 134)` and `(provenance: Variant C line 135)`
- Validation: Bullets are verbatim from C lines 134-135. No conflict with adjacent bullets.

### Change #4 — Rename Theory N → MN throughout

- Status: APPLIED
- Before: "Theory 1", "Theory 2", "Theory 3", "Theory 4" headings and references
- After: "M1", "M2", "M3", "M4" headings and references throughout the document including in §"Top root causes"
- Provenance tag: N/A (cosmetic rename)
- Validation: All inline references updated consistently (e.g., "Theories 1 and 2 compound" → "M1 and M2 compound"). No orphaned T-prefix references.

## Post-Merge Validation

### Structural integrity

- Heading hierarchy: H1 (title) → H2 (sections) → H3 (subsections in M3, Synthesis addendum) → H4 (none) — no gaps, no orphaned subsections. PASS
- Section ordering: Logical — Top-line synthesis (executive summary) → Methodology (degradation disclosure) → M1 → M2 → M3 (composite) → M4 → Cross-mechanism implications → Top root causes → Synthesis addendum. PASS
- Document starts with H1: PASS

### Internal references

- Total cross-references: 18 (file:line citations to external artefacts + 4 internal references to "M1", "M2", "M3", "M4")
- Resolved: 18
- Broken: 0
- PASS

### Contradiction rescan

- New contradictions introduced by merge: 0
- The original X-001 conflict (M3 one-vs-three mechanisms) was resolved via MERGE outcome — the merged document explicitly preserves all three sub-mechanisms with their distinct fixes. This is not a contradiction; it is the resolution.
- PASS

## Summary

- Planned changes: 4
- Applied: 4
- Failed: 0
- Skipped: 0
- Rejected alternatives documented: 2 (footer-position for Channel-B disclosure; bottom-map provenance style)

**Post-merge result**: FINAL-MERGED-CAUSES.md at the canonical path, with all 5 task-required content pieces present (Top 3-5 root causes ranked; convergence evidence unanimous-vs-partial; compositional-vs-exchangeable analysis; open conflicts with resolution; process degradation note for Channel B).
