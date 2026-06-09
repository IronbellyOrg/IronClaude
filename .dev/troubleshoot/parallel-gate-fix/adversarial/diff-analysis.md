# Diff Analysis: gate-fix option comparison

## Metadata
- Variants: 2 — A (clamp 2–5), B (exempt final phase)
- Focus: correctness (this case), generality, FP/FN risk, maintainability
- Both target the same function: `_check_parallel_instructions` (gates.py:197-227)

## Structural Differences
| # | Area | Variant A | Variant B | Severity |
|---|------|-----------|-----------|----------|
| S-001 | Edit size | 1 token (`>= 2` → `2..5`) | ~5 lines (compute max, exempt final, iterate work phases) | Low |
| S-002 | New control flow | none | `max(phase_numbers)` + exclusion predicate | Low |

## Content Differences (the substance)
| # | Topic | Variant A | Variant B | Severity |
|---|-------|-----------|-----------|----------|
| C-001 | Selection principle | Positional window (phase number ≤ 5) | Semantic (exempt the final/completion phase) | **High** |
| C-002 | Correctness on THIS run (work 2–6, completion 7) | Passes — but by *also dropping* the legitimate Phase 6 check (FN) | Passes — checks 2–6, exempts only 7 (no FP, no FN) | **High** |
| C-003 | Generality across task length | Magic `5` fails short tasks (completion ≤5 still FP) and long tasks (work 6+ unchecked, FN) | Keys on final-phase invariant → correct at any length | **High** |
| C-004 | Maintainability | Leaves unexplained `5`; encodes a "≤5 work phases" convention the template already violates | Self-documenting; docstring becomes true to intent | Medium |
| C-005 | Immediate unblock of the live halt | Yes (Phase 7 no longer checked) | Yes (Phase 7 exempt) | Low (tie) |

## Unique Contributions
| # | Variant | Contribution | Value |
|---|---------|-------------|-------|
| U-001 | A | Minimal diff, zero new control flow → trivially reviewable, no new-logic bug surface | Medium |
| U-002 | B | Symmetry with the EXISTING Phase-1 exemption: the gate already starts at ≥2 (exempts setup); B exempts the other bookend (completion) — consistent rule | **High** |
| U-003 | B | Fixes the bug *class*, not the instance | **High** |

## Shared Assumptions (A-NNN)
| # | Assumption | Classification | Note |
|---|-----------|----------------|------|
| A-001 | "The final phase is a sequential completion/presentation phase where parallelism is inapplicable" | STATED in B, implicit in A | Grounded in the MDTM anti-orphaning convention (completion items live in the final phase). Holds by construction of the PRD task template. |
| A-002 | "Literal keywords (parallel/concurrent/…) in prose reliably indicate parallel execution" | UNSTATED (both inherit it) | Pre-existing gate heuristic limitation; **out of scope** for this decision — neither option changes it. Flagged for awareness. |
