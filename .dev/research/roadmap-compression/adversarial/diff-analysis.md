# Diff Analysis: Roadmap Compression Strategy Comparison

## Metadata
- Generated: 2026-04-15
- Variants compared: 3
- Total differences found: 19
- Categories: structural (4), content (7), contradictions (4), unique contributions (4)

---

## Structural Differences

| # | Area | Position A | Position B | Position C | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Output format | YAML structured data | YAML with embedded full-text chunks | TSV/CSV tabular | High |
| S-002 | Compression model | Lossy (strips prose) | Lossless (preserves full text of diffs) | Lossy (keyword tags from prose) | High |
| S-003 | Cross-file dependency | Independent (each file compressed alone) | Dependent (requires both files for pre-comparison) | Independent (each file compressed alone) | High |
| S-004 | Non-table content handling | One-line summaries | Full preservation or hash stubs | Metadata header with compressed key-value pairs | Medium |

---

## Content Differences

| # | Topic | Position A | Position B | Position C | Severity |
|---|-------|-----------|-----------|-----------|----------|
| C-001 | Acceptance criteria handling | STRIPPED entirely | PRESERVED verbatim in differing chunks | Compressed to keyword tags | High |
| C-002 | Dependency graph fidelity | Lossless u2014 deps array per task | Lossless u2014 full table preserved | Lossless u2014 DEPS column in TSV | Low |
| C-003 | Integration point preservation | Structured YAML array | Full text in phase chunks | Structured TSV section | Medium |
| C-004 | Compression ratio (Opus) | ~75-80% reduction | ~5-10% reduction (realistic) | ~65-70% reduction | High |
| C-005 | Compression ratio (Haiku) | ~75-80% reduction | ~5-10% reduction (realistic) | ~65-70% reduction | High |
| C-006 | Diff tool compatibility | Requires YAML-aware diff | Standard diff works on full-text chunks | Standard line-by-line diff works perfectly | Medium |
| C-007 | Reconstructability | Non-recoverable (lossy) | Fully recoverable with originals | Non-recoverable (lossy) | Medium |

---

## Contradictions

| # | Point of Conflict | Position A | Position B | Impact |
|---|-------------------|-----------|-----------|--------|
| X-001 | Can AC differences be detected in diff output? | NO u2014 AC is stripped, so two tasks with different AC look identical if other fields match | YES u2014 full AC text preserved in differing chunks | High u2014 AC differences are a primary source of meaningful roadmap divergence |
| X-002 | Is pre-comparison required? | NO u2014 each file compressed independently | YES u2014 hash comparison required before compression | High u2014 user requirement is to compress BEFORE feeding to diff tool |
| X-003 | Can the compressed output serve as a standalone artifact? | YES u2014 YAML registry is self-contained and machine-readable | PARTIALLY u2014 hash stubs reference the other file | YES u2014 TSV is self-contained |
| X-004 | AC keyword extraction consistency | N/A (AC stripped) | N/A (AC preserved verbatim) | Position C: unbounded vocabulary creates false-positive diffs | Medium |

---

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|-------------|-------|
| U-001 | Position A | Machine-readable YAML output enables programmatic merge tools beyond text diff | High |
| U-002 | Position B | Chunk-level semantic alignment makes diffs structurally meaningful (phase-vs-phase) | Medium |
| U-003 | Position C | AC keyword tags preserve SOME semantic content while achieving good compression | High |
| U-004 | Position C | TSV normalization eliminates markdown formatting noise that creates false diffs | Medium |

---

## Shared Assumptions

| # | Assumption | Classification | Impact |
|---|-----------|----------------|--------|
| A-001 | The diff/merge tool (deef) operates on text files and benefits from smaller input | STATED | The entire compression motivation |
| A-002 | Task IDs are the primary alignment key between roadmaps | UNSTATED | If IDs don't align (Haiku uses JTBD-001, PERSONA-001 etc. that Opus doesn't have), ID-based matching fails |
| A-003 | The compressed output will be consumed by an LLM (deef), not a traditional diff tool | UNSTATED | LLMs can handle lossy compression and reconstruct meaning from keyword tags; traditional diff tools cannot |
| A-004 | Phase numbering is consistent between files | UNSTATED | Opus and Haiku both use 6 phases but scope them differently; Phase 1 in Opus (implementation) vs Phase 1 in Haiku (architecture planning) cover different work |

---

## Summary
- Total structural differences: 4
- Total content differences: 7
- Total contradictions: 4
- Total unique contributions: 4
- Total shared assumptions: 4 (UNSTATED: 3, STATED: 1)
- Highest-severity items: S-001, S-002, S-003, C-001, C-004, C-005, X-001, X-002
