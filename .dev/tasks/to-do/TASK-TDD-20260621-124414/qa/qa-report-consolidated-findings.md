# Report-Validation Consolidated Findings (Gate 6G)

**Date:** 2026-06-21 | **TDD:** `.dev/reflect-hardening/issue-3-deterministic-runtime-surface-sweep/tdd.md` (1,443 lines)
**Lenses (9):** template-conformance PASS, internal-consistency PASS, evidence-quality PASS(+4 minor), completeness PASS,
**actionability FAIL (3 CRIT/7 IMP/4 MIN)**, numbers-metrics PASS(0), crossref-chain PASS, **domain-accuracy FAIL (1 IMP/2 min)**, tier-budget PASS.

## Consolidated Verdict: FAIL → fix cycle 1

Seven of nine lenses PASS; citation fidelity verified exceptional across all lenses (~60 distinct file:line claims
independently confirmed; greenfield claim true). The FAIL is driven by the actionability + domain-accuracy lenses,
which converge on **C1** (the single most load-bearing finding) plus genuine implementability gaps (C2/C3, I1-I7).
All are surgical content additions, not a rewrite. The TDD is ~1,443 lines; headroom to ~1,800 absorbs the additions.

## CRITICAL (must fix)

| ID | Location(s) | Issue | Fix |
|----|-------------|-------|-----|
| C1 | FR-006 (~L286), §6.3 (~L436), §11.1 step6 (~L674), AC-4 (~L1300), glossary (~L1400) — NOT §8.2 L600 / §14.2 L892 which already say "drives" | TDD says the §5.3 pre-filter **"reads `runtime_surface_unreached`"** (integer). Live SKILL.md §5.3 gates on a DERIVED field `surface_unreached` (string), SET from a SUCCESSFUL sweep with `runtime_surface_unreached ≥ 1` (SKILL.md:390-391, 402, 412). Confirmed by 2 lenses (actionability + domain-accuracy). The derivation step + owner are unspecified → AC-4 wiring targets the wrong field. | Add the derivation: the sweep (or `derive_verdict`) sets `surface_unreached = "runtime_surface_unreached"` when `runtime_surface_unreached ≥ 1` from a successful sweep; the §5.3 pre-filter reads `surface_unreached`. Correct all ≥5 locations to name the real field + derivation; add the derivation to the §15 test plan. |
| C2 | §8.1 (~L582-589) | 6-unit signatures reference ~11 types defined nowhere (`DiffHunk`, `SurfaceAllowlist`, `TaggedSurface`, `LspOverlay`, `ReferrerEdge`, `TestCommentTable`, `EntrypointRoot`, `PartitionedReferrers`, `DegradeVerdict`, `RootwalkResult`, `ContractScalars`). Only `RuntimeSurfaceLedgerRow` is modeled. | Add a §8.1.x "Input & intermediate types" subsection with a field table per type (as §7.1.2 does), OR explicitly mark which are opaque pass-throughs vs which `runtime_surface.py` must define. |
| C3 | §8.1 (`run_sweep` named L580/589/636/671) | The orchestrator `run_sweep` — the entry point BOTH the product path (Phase 2) and eval path (Phase 3) call — has no signature. | Add a concrete `run_sweep(...)` signature row to §8.1 (params e.g. `diff`, `base`, `output_dir`, `tasklist`, `availability_surface`; named return type), and state how `_audit_once` builds those args from `ReflectConfig`. |

## IMPORTANT (must fix per zero-leniency)

| ID | Location | Issue | Fix |
|----|----------|-------|-----|
| I1 | §8.1 `tag_surfaces` / §6.1 TAG | Diff-acquisition contract missing — how `diff_hunks` is produced (git diff text? patch file? pre-parsed) and which caller supplies it (runner vs grader). | Specify the diff-acquisition contract so product + eval paths provably share one input shape. |
| I2 | §8.1 `rootwalk_entrypoints` / §6.1 ROOTWALK | Root-enumeration algorithm unspecified (what is scanned to produce `EntrypointRoot`s; `[project.scripts]`? CLI registrations?). Incomplete enumeration silently turns REACHED→DEGRADE. | Define the root-enumeration algorithm + completeness check. |
| I3 | §7.1.1 `edge` (OQ-EDGE) | `edge` formatter (delimiter, root rendering, dedup) unpinned; the determinism golden-file test (R3/§12.4) compares ledger bytes → non-authorable without it. | Pin the canonical `edge` format in §7.1.1. |
| I4 | §24.2 / §15.6 (AC-5) | AC-5 (safety preserved) gated only by "spot-checked" — not a pass/fail procedure for the whole reason FR-RSR exists. | Replace with a concrete regression assertion: run the pre-FR-DRS safety fixtures, assert verdict/prose layer still suppresses clean-PASS, named fixtures + expected verdicts. |
| I5 | §15.3 C-5 / §22.1 / §23.2 Phase 3 | The `evals.json → eval_metadata.json` materializer is "not located"/UNVERIFIED; AC-2 (headline) depends on it but Phase 3 starts by locating it. | Front-load the materializer search to Phase 1 so AC-2 reachability is known before product wiring; or mark AC-2's grader-determinism conditional until located. |
| I6 | §6.4 D2 / §19.1 / R2 | The bare-`claude -p` "conditional demotion + LLM-fallback" never specifies HOW the skill detects the module already ran. | Specify the detection signal: e.g., "if `return-contract.yaml` already carries `runtime_surface_sweep_ran`, narrate only; else run legacy LLM emission." |
| I7 | Phase 2 / §11.1 step6 | "Add consumer triggers in `contract.py` (`_halted_reason`/`_degraded_reason`)" — exact predicate/returned slug unspecified, and ambiguous vs §14.3 "UNREACHED is not a 5th deviation class" (maps to existing regression/drift). | Specify the exact `_halted_reason`/`_degraded_reason` additions (predicate, returned slug, UNREACHED→regression mapping), reconciled with §14.3. |

## MINOR (fix for hygiene)

| ID | Location | Issue | Fix |
|----|----------|-------|-----|
| M1 | §8.2/§6.3/glossary | "forbid-STOP pre-filter" label vs SKILL.md's actual "§5.3 D13 pre-filter precedence." | Align label or note they are the same surface. |
| M2 | §6.2/§7.5 | `models.py:95-98`→ property at :96; `models.py:39-42`→ enum at :39 (and the exit-code dict is at ~:45-48 per evidence lens). | Tighten the two models.py citations. |
| M3 | §7.1.3 `UnreachedSurface` | Element shape deferred entirely to SKILL §9.1 — minimally pin (does each entry carry `symbol`/`requirement_id`/`evidence_ref`?). | Add a minimal field list or cross-link the exact §9.1 sub-shape. |
| M4 | §23 / frontmatter | No phase effort sizing; `complexity_score` frontmatter empty. | Add rough per-phase sizing; populate `complexity_score` (HIGH already in class). |
| M5 | evidence lens I-1..I-4 + domain m2 | Line-anchor drift: `filetype_rules.py:105-107`→`:106-107`; `reachability.py:740` description (it's the report emitter, not "scalar frontmatter"); research/00 ad-hoc-name block `45-49`→`46-50`; grader `:445`/`:440` metadata-read. | Correct these citation line-anchors. |

## Cosmetic non-fixes (acknowledged, no action)
Template "Completeness Status" scaffolding omission (acceptable — self-checklist not deliverable); ToC formatting
divergence; reduction-precedence abbreviation variety; bare `§10.6`/`§10.9` SKILL.md qualifier. Not gating.

## Fix scope for 6G.11
Apply C1, C2, C3, I1-I7, M1-M5 in-place to the TDD. Keep within the 1,800-line Heavyweight budget. The fixes are
additive specification (new §8.1 type subsection + run_sweep signature + C1 derivation step) — net realistic growth
to ~1,520-1,600 lines, still within budget.
