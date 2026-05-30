# Refactoring Plan

## Overview

- Base variant: Variant 1 (A-merged) — selected via 0.948 combined score + 6 debate points + 7-section completeness
- Variants incorporated from: Variant 2 (B-merged) + Variant 3 (C-merged)
- Change count: 4 planned changes; 2 rejected alternatives documented
- Overall risk: Low (all changes are additive or substitutional in well-bounded sections)

## Planned Changes

### Change #1 — Insert opening synthesis paragraph (incorporate from B §1)

- **Source**: Variant 2 (B), §1 "Top-line findings" (B line 12)
- **Target location in base**: New §"Top-line synthesis" inserted between A's title block (lines 1-7) and A's "Methodology & Channel Disclosure" §
- **Integration approach**: Append
- **Rationale**: Debate U-002 winner at 85% confidence (Round 2 concession from A and C advocates). A and C lack an executive synthesis paragraph; B's framing — "multiplicative compounding of two structural design choices, modulated by a decision-theoretic blind spot, propagated by a silent-green test suite" — is the tightest one-sentence summary surfaced across channels.
- **Risk level**: Low (additive; doesn't modify existing content)

### Change #2 — Refactor M3 into composite structure (incorporate from C)

- **Source**: Variant 3 (C), §"Mechanism M3 — Verdict-Direction Asymmetry and Anchoring Channel Loss (composite)" lines 64-103
- **Target location in base**: Replace A's "Theory 3 — Verdict-Direction Asymmetry" (A lines 90-112) AND A's "Secondary mechanisms" §S1/§S2 (A lines 140-153) with three subsections M3a / M3b / M3c
- **Integration approach**: Restructure (replace 2 separate sections with 1 composite section having 3 subsections)
- **Rationale**: Debate X-001 (MERGE outcome 90% confidence) and C-002 winner (90% confidence). Unanimous concession in Round 2 from A and B advocates: M3 must be preserved as composite. The three sub-mechanisms have structurally independent fixes (verdict-direction modifier; Falsification-standard card field; dual-instance-minimum) and collapsing them to one mechanism loses two fixes. C's structure (M3a primary 0.78 + M3b 0.65 + M3c 0.45) is the correct decomposition.
- **Risk level**: Medium (restructures existing section, but preserves all base evidence and adds 2 fixes)

### Change #3 — Incorporate "M4 is prevention mechanism" framing + recursion observation (from C)

- **Source**: Variant 3 (C), lines 134-135 ("M4 is the prevention mechanism for all three diagnostic mechanisms" + "Recursion-of-anti-pattern")
- **Target location in base**: A's §"Cross-theory implications" — append these two bullet points after the existing "Theory 4 is the meta-prevention layer" bullet (A line 164)
- **Integration approach**: Append two bullet points
- **Rationale**: C's "diagnostic vs preventive layer" delineation is cleaner than A's "meta-prevention layer" phrasing alone. The recursion-of-anti-pattern observation (calibration apparatus failing the same way pr86's code was failing) is itself a verification that the chosen root causes are real, not procedural artifacts.
- **Risk level**: Low (additive)

### Change #4 — Renumber Theories to use M-prefix and update Top root causes ranking

- **Source**: Variant 2 (B) and Variant 3 (C) naming convention (M1/M2/M3/M4)
- **Target location in base**: Replace "Theory 1" → "M1", "Theory 2" → "M2", "Theory 3" → "M3" (composite), "Theory 4" → "M4" throughout the document, INCLUDING in §"Top root causes (merged convergence)" (A lines 174-184)
- **Integration approach**: Rename
- **Rationale**: Two of three variants use M-prefix; A's T-prefix is the outlier. M-prefix is also more accurate (these are mechanisms, not theories — they are evidence-anchored claims about how the calibration apparatus fails, not hypotheses-to-be-tested). Unanimous structural alignment via rename.
- **Risk level**: Low (cosmetic rename, no semantic change)

## Changes NOT Being Made

### Rejected Change #1 — Move Channel-B-degradation disclosure to footer (B's structure)

- **Source proposing**: Variant 2 (B), §5 "Methodology note"
- **Rationale for rejection**: Debate C-003 winner at 95% confidence (unanimous in Round 2). The disclosure is the load-bearing limit on the entire convergence-as-evidence argument; readers must see it first. A's top-of-document placement is structurally correct.

### Rejected Change #2 — Use bottom-of-document provenance map (B's style)

- **Source proposing**: Variant 2 (B), "Provenance map" table at bottom
- **Rationale for rejection**: Debate S-003 winner at 70% confidence. A's per-section `<!-- provenance: ... -->` HTML comments are more auditable inline — readers see provenance attached to the exact section it applies to. B's map adds a layer of indirection.

## Risk Summary

| Change # | Description                          | Risk Level | Impact if Fails                                                | Rollback                                        |
|----------|--------------------------------------|------------|----------------------------------------------------------------|-------------------------------------------------|
| 1        | Insert B's §1 opening synthesis      | Low        | Reader misses synthesis — degrades readability not correctness | Delete the inserted paragraph                   |
| 2        | M3 composite refactor                | Medium     | Loss of M3b/M3c fixes if restructure misplaces content         | Restore original A T3 + §S1/§S2 from variant-1  |
| 3        | C's prevention + recursion framings  | Low        | Loss of nuance in cross-theory framing                         | Delete the two appended bullets                 |
| 4        | M-prefix rename                      | Low        | Cosmetic only                                                  | Find-replace M→Theory                           |

## Review Status

Auto-approved (non-interactive mode). Timestamp: 2026-05-26T19:35Z.
