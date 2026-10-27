# D-0049: Per-Iteration Logic (4a–4d) — Implementation Spec

## Task

T08.02 — Implement Per-Iteration Logic (4a–4d) (R-053)

## Deliverable

`src/superclaude/cli/cli_portify/steps/panel_review.py` — per-iteration functions

## Implementation

### Functions

**4a Expert Focus / Finding parsing:**
- `parse_quality_scores(content: str) -> dict[str, float]` — extracts clarity, completeness, testability, consistency from colon or table format
- `count_unaddressed_criticals(content: str) -> int` — counts CRITICAL lines not preceded by [RESOLVED]/[INCORPORATED]/[DISMISSED]

**4b Finding Incorporation:**
- `capture_section_hashes(content: str) -> dict[str, str]` — captures SHA-256 hashes per ## section for additive-only enforcement
- `verify_additive_only(old_hashes, updated) -> list[str]` (utils.py) — returns violations list

**4c Panel Critique / Quality Scoring:**
- `compute_overall_score(scores: dict) -> float` — mean of 4 dimensions

**4d Convergence Scoring:**
- Wired into `ConvergenceEngine` via `IterationResult(unaddressed_criticals=...)`
- Convergence = zero unaddressed CRITICALs (FR-032)
- `downstream_ready` gate (overall >= 7.0) is separate per T08.05

## Verification

```
uv run pytest tests/cli_portify/test_panel_review.py -v
uv run pytest tests/cli_portify/test_section_hashing.py -v
```

**Result:** 25/25 + 14/14 = 39 passed
