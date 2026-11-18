# Diff Analysis: reflect-pre reviewer-card comparison (shadow06)

## Metadata
- Generated: 2026-11-13T00:18:30Z
- Variants compared: 3 (V1 analyzer/sonnet, V2 qa/haiku, V3 refactorer/opus)
- Total differences found: 10
- Categories: structural (1), content (1), contradictions (1), unique (6), shared assumptions (1)

## Structural Differences
| # | Area | V1 | V2 | V3 | Severity |
|----|------|----|----|----|----------|
| S-001 | Findings shape | 5 narrative findings + block | 0 defects, 1 coverage observation | 4 narrative findings + "what I checked" section | Low (V2's zero-defect shape differs; both valid) |

## Content Differences
| # | Topic | V1 | V2 | V3 | Severity |
|----|-------|----|----|----|----------|
| C-001 | Plugin mirror distribution gap | F3 MINOR: plugin hooks.json surface unnamed in steps; staging unclear (tasklist:61 vs :64) | not addressed | F1 MAJOR: steps omit the hand-maintained plugin mirror entirely (sync-dev never writes plugins/; byte-identical mirror tests exist) | Medium (V3's account is broader and names the mechanism; V1 flags the same surface more narrowly) |

## Contradictions
| # | Point of Conflict | V1 | V2 | V3 | Impact |
|----|-------------------|----|----|----|--------|
| X-001 | Is T2.AC5 "record the official updatedInput contract" (tasklist:53) a plan defect? | F4 MAJOR: self-referential, executor compares its own output with itself | Explicit rebuttal of the T1 concern: "Recording an official contract in an evidence artifact does not authorize treating the implementation as that contract" — i.e., not a defect | silent | Medium (severity disagreement, not factual; affects whether the merged report carries a MAJOR) |

## Unique Contributions
| # | Variant | Contribution | Value |
|----|---------|--------------|-------|
| U-001 | V3 | "do not stage mirrors" (tasklist:61) read literally forbids staging the tracked plugin mirror; constraint says only ".claude mirrors" (tasklist:25) — executor could ship without the plugin copy | High |
| U-002 | V3 | Interim verify-sync failure window between Task 1 and Task 3 (script added at T1, listed at T3) not declared expected | Low |
| U-003 | V3 | Spec's "launcher/harness" ambiguity: no task makes an existing launcher write the governed record; launcher half is documentation only | Medium |
| U-004 | V1 | Plan's stdlib-Python exception cites a "bash-only limit" the source spec never states | Medium |
| U-005 | V1 | The stdlib-only/UV/no-new-deps constraint (INF-003, INF-008) has no acceptance criterion; an executor could import a third-party module and still pass | Medium |
| U-006 | V1 | Task 1 ACs use undefined pass criteria ("defined tested outcomes", "documented completion semantics") | Low |

## Shared Assumptions
| # | Agreement Source | Assumption | Classification | Promoted |
|----|------------------|------------|----------------|----------|
| A-001 | All three cards audit the plan as a plan with the landed tree as context | A plan defect remains reportable at full severity even though this execution landed correctly | UNSTATED | Yes → [SHARED-ASSUMPTION] diff point |
| A-002 | V1 C-001 + V3 F1/F2 both rely on it | The plugin mirror under plugins/ is required distribution surface (stated in tasklist:64 AC itself) | STATED | No |

## Summary
- Structural: 1; Content: 1; Contradictions: 1; Unique: 6; Shared assumptions surfaced: 2 (UNSTATED 1, STATED 1)
- Highest-severity items: C-001 (Medium), X-001 (Medium), U-001 (High value)
- Similarity check: differences >> 10% of comparable items; debate proceeds
