# Diff Analysis: structural_checkers.py Merge-Conflict Resolution Comparison

## Metadata
- Generated: 2026-06-04 (ISO date)
- Variants compared: 3 (variant-1 = ours/R0R1, variant-2 = theirs/master, variant-3 = proposed-resolution)
- Mode: A (compare existing files), depth=quick
- Total differences found: 4 (all L1 surface-level / comment-only)
- Categories: structural (0), content (4 comment-only), contradictions (0), unique (1), shared assumptions (1)

## Ground-Truth Established Before Debate
- `diff` of comment-stripped executable code across all three variants = **identical** (proven: `grep -vE '^\s*#' | diff` yields 0 lines for resolved-vs-ours; ours-vs-theirs executable code also proven identical earlier).
- All 3 variants pass `ast.parse` (syntactically valid Python).
- Proposed resolution's MD-family logic executed in isolation: 18/18 assertions PASS (canonicalization, milestone-distinctness, contract-token coverage, allowlist-extension regex, non-MD regression).
- Contract anchor: `contracts.ID_PATTERNS["MD"] = r"M\d+-D-?\d+"` (verified at `src/superclaude/contracts/__init__.py:71`).

## Structural Differences
None. All three variants have identical heading/section/symbol structure (same functions, same order, same signatures).

| # | Area | V1 (ours) | V2 (theirs) | V3 (proposed) | Severity |
|---|------|-----------|-------------|---------------|----------|
| S-001 | Symbol set & order | identical | identical | identical | Low (none) |

## Content Differences
The ONLY differences are in **comments** (provenance attribution). Executable code is byte-identical.

| # | Topic | V1 (ours) Approach | V2 (theirs) Approach | V3 (proposed) | Severity |
|---|-------|--------------------|----------------------|---------------|----------|
| C-001 | MD-canon comment (hunk 1) | Rich: DISTINCT-forms rationale + arch-lint Rule 2 note + PR#111 provenance | Terse one-liner + TASK-RF ref | Rich (V1) + appended TASK-RF ref | Low |
| C-002 | non-refs anchor comment (hunk 2) | PR#111 provenance | TASK-RF ref + **foreign-repo absolute path** `/config/workspace/TUIBBS-scp/...L665` | PR#111 + TASK-RF ref; **foreign path dropped** | Low |
| C-003 | D3 allowlist comment in check_signatures (hunk 3) | PR#111 provenance | TASK-RF ref | PR#111 + TASK-RF ref | Low |
| C-004 | "We also track source family" comment placement | placed just above `roadmap_canon` (accurate: "handled by own branch below") | placed in "Build canonical-form" block (phrased "intentionally not suppressed") | V1 placement kept (single block, no duplicate) | Low |

## Contradictions
None across executable code. One latent risk noted as shared assumption (A-001).

| # | Point of Conflict | V1 Position | V2 Position | V3 Position | Impact |
|---|-------------------|-------------|-------------|-------------|--------|
| X-001 | (none) | — | — | — | — |

## Unique Contributions
| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | V2 (theirs) | Canonical-anchor absolute path `/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/roadmap.md L665` | **Low / negative** — points at a *different repository* not present in this tree; rot-prone; rejected from V3 |
| U-002 | V1 (ours) | arch-lint Rule 2 rationale ("NOT a duplicate of any contracts.ID_PATTERNS body") | **High** — load-bearing maintenance guidance; preserved in V3 |

## Shared Assumptions
| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | The MD tokenizer/canonicalizer in `spec_parser.py` (concurrently being merged by a sibling agent) ends up emitting `family=="MD"` tokens that match `ID_PATTERNS["MD"]`. All 3 variants depend on this — the checker's `if family == "MD"` branch is dead code if `spec_parser` never tags any token `MD`. | All variants share identical MD branch | Medium (cross-file) | UNSTATED → promoted |

## Summary
- Total structural differences: 0
- Total content differences: 4 (all comment-only, all Low)
- Total contradictions: 0
- Total unique contributions: 2 (U-001 rejected, U-002 preserved)
- Total shared assumptions surfaced: 1 (UNSTATED: 1)
- Highest-severity items: none High in executable code; A-001 (Medium) is the only cross-cutting risk and is out-of-scope for this file (owned by sibling spec_parser.py merge).
- Similarity check: comment-stripped diff < 10% → variants substantially identical on the dimension that affects runtime. Per FR-006 `variants_too_similar`, debate is reduced to comment-quality adjudication only.
