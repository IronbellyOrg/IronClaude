# .bak Reproducer Comparison (Pre-fix vs Post-fix)

**Artifact:** `/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/roadmap-opus-architect.md.bak-pre-mixed-drift-fix`

**Command:** REPORT.md:36-47 reproducer (verbatim) — prints `cl.is_pure_cosmetic`, `len(cl.cosmetic_violations)`, `len(cl.semantic_violations)`, `_template_sections_present(r)` after running the dispatcher.

| Field | Pre-fix (Step 1.5) | Post-fix (Step 6.3) | Delta |
|---|---|---|---|
| `is_pure_cosmetic` | `True` | `True` | unchanged |
| `len(cosmetic_violations)` | `22` | `24` | +2 (C12 + C13 emissions) |
| `len(semantic_violations)` | `0` | `0` | unchanged (REPORT confirmed) |
| `_template_sections_present(r)` | `False` | **`True`** | **flipped** |

## Verdict

**PASS** — the load-bearing final token flipped from `False` to `True`. The bug surfaced by the validation REPORT (`is_pure_cosmetic=True` + 22 transforms applied + `_template_sections_present` still False) is closed on the actual TUIBBS opus-architect drift artifact. The roadmap pipeline's `cli/pipeline/executor.py:349-352` halt path no longer triggers for this drift shape.

The +2 violations confirm both new C-classes fired: C12 stripped the `## Timeline Estimates (gate-bound, not date-bound)` parenthetical, and C13 renamed the non-canonical Resource H3 to its canonical form.
