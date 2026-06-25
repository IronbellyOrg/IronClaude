# Report-Validation Verdict — FR-DRS TDD (Fix Cycle 1)

**TDD:** `.dev/reflect-hardening/issue-3-deterministic-runtime-surface-sweep/tdd.md`
**Date:** 2026-06-21 | **Final line count:** 1,549 (was 1,443; +106 additive) — within the 1,800 Heavyweight budget.
**Persistence note:** Authored by the rf-qa fix agent; persisted by the orchestrator (agent returned content inline).
Source verification: zero-trust — every C1/C3/I2/I7/M2/M5 anchor independently re-read against live source before editing.

## Per-fix before/after

| ID | Before | After |
|----|--------|-------|
| C1 | ≥6 locations asserted §5.3 pre-filter "reads `runtime_surface_unreached`" (integer) | Corrected to the verified two-step: sweep emits integer → derivation sets `surface_unreached = "runtime_surface_unreached"` when `≥1` from a successful sweep → §5.3 gates on the derived string (SKILL.md:390-391/402/412). Owner named (sweep/CLI wrapper at `_audit_once`; `derive_verdict` fallback). New §15.4a derivation test. |
| C2 | §8.1 referenced 11 undefined types | New §8.1.1 field-shape table for all 11 (`DiffHunk`…`ContractScalars`); `LspOverlay` flagged sole opaque pass-through; framed as DESIGNED types. |
| C3 | `run_sweep` named 4× but never signatured | New §8.1.2: `run_sweep(diff, base_ref, scope_worktree, tasklist, output_dir, availability_surface, *, lsp) → SweepResult` (ledger rows + 6-scalar dict + ledger path) + how `_audit_once` builds args from `ReflectConfig`. |
| I1 | diff-acquisition unspecified | §6.3: `run_sweep` takes unified-diff text + `base_ref`; runner supplies (product), grader supplies `input/diff.patch` (eval) — one shared shape. |
| I2 | root enumeration undefined | §6.1: scan `[project.scripts]`→`[project.entry-points.*]`→CLI command roots (pyproject.toml:68-69); completeness check gates REACHED vs DEGRADE-on-partial. |
| I3 | `edge` formatter deferred (OQ-EDGE) | §7.1.1a pins canonical `f"{symbol} -> {target}"` (single-space delimiter, `root:{root_id}` rendering, `(symbol,target)` dedup, lexicographic sort). |
| I4 | AC-5 "spot-checked" | §24.2 concrete gate: run fixtures 37/39/40/41 through verdict layer, FAIL release if any clean-passes; named `test_runtime_surface_safety_regression.py`. |
| I5 | C-5 materializer search began Phase 3 | Front-loaded to Phase 1 §23.2; AC-2 grader-determinism marked conditional until located. |
| I6 | demotion detection unspecified | §19.1 + §6.4 D2: branch on presence of `runtime_surface_sweep_ran` in `return-contract.yaml` (present→narrate-only; absent→legacy LLM fallback). |
| I7 | `_halted_reason`/`_degraded_reason` additions unspecified | Phase 2 §23.2: REUSE `degraded-components` slug (`runtime-surface:backend_unavailable`) + REUSE `regression` slug (UNREACHED→`deviation_count_by_class.regression`, no new branch) — reconciled with §14.3 "not a 5th deviation class." |
| M1 | "forbid-STOP" vs SKILL "§5.3 D13" | Glossary notes same surface. |
| M2 | `models.py:95-98`/`:39-42` | → `:96` (contract_path), `:39` def + `:44-49` dict + `:33-36` enum. |
| M3 | `UnreachedSurface` shape deferred | §7.1.3 pins minimal `{symbol, requirement_id, evidence_ref}`. |
| M4 | no phase sizing; empty `complexity_score` | §23.1 t-shirt sizes (~4–6 eng-days); frontmatter `complexity_score: "0.82"`. |
| M5 | line-anchor drift | `filetype_rules.py:106-107`; `reachability.py:740`=`emit_reachability_report`; research/00 `47-49`; grader `:440`. All verified. |

## Confirmation
- All 15 fixes (C1-C3, I1-I7, M1-M5) applied in-place via surgical Edits.
- Final line count 1,549 — within budget.
- No new fabrication: every new citation independently re-read vs live source; new §8.1.1 types + `run_sweep`/`SweepResult` framed as DESIGNED/greenfield.

REPORT VALIDATION: CLEARED (fix cycle 1)

## Fix Cycle 2 (verification round)

Post-cycle-1 verifiers: **content (rf-qa-qualitative) PASS** — TDD judged implementation-ready (engineer can build
`runtime_surface.py` from §6/§7/§8 alone; C1-C3 + I1-I7 verified closed vs live SKILL.md + source). **Structural
(rf-qa) FAIL on ONE residual:** line 1374 (Phase 2 Exit Criteria) still named the integer `runtime_surface_unreached`
as the §5.3 pre-filter read target — the exact C1 mis-wiring — while the other 8 C1 locations were correctly fixed.

**Cycle-2 fix (orchestrator, surgical):** L1374 corrected to "the §5.3 forbid-STOP pre-filter gates on the DERIVED
`surface_unreached` field — set to `"runtime_surface_unreached"` when the integer `runtime_surface_unreached ≥ 1`
from a successful sweep (SKILL.md:402/412) — so the pre-filter reads `surface_unreached`, never the integer directly."
Independent grep: ZERO residual integer-as-gating-target claims; derived `surface_unreached` described 60×; 1,549 lines.

Both verifier concerns resolved.

REPORT VALIDATION: CLEARED (fix cycle 2 — residual C1 at L1374 fixed) → **PASS**
