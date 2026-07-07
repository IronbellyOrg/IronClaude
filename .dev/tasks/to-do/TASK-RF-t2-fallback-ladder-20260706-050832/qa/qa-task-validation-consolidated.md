# Consolidated Task-File Validation Findings (A.10 + A.10.25)

Task file: `TASK-RF-t2-fallback-ladder-20260706-050832.md`
Source reports: `qa-task-validation-b2-report.md` (FAIL), `qa-task-validation-structure-report.md` (FAIL), `qa-task-research-alignment-report.md` (PASS, refinements).
Fix authorization: the single fix agent applies ALL of the below in-place, then verifies.

## CRITICAL

**C1 — Circular import via `stamp` module-level default (phase-structure CRITICAL).**
Step 3.4 (and the `run_fallback_ladder` signature in Step 1.5 / the fallback.py engine) defaults `stamp: Callable = _stamp_worker_paths`. `_stamp_worker_paths` is defined in `ensemble.py:691`; a module-level default in `fallback.py` forces `from .ensemble import _stamp_worker_paths`, and Step 3.6 makes `ensemble.py` import `run_fallback_ladder` from `fallback.py` → the exact `ensemble ↔ fallback` cycle Phase 1 exists to break.
FIX (design §4.3 already corrected to match): make `stamp` a **REQUIRED keyword param with NO module-level default** in `run_fallback_ladder`. The ensemble seam (Step 3.6) already passes `stamp=_stamp_worker_paths` explicitly (it owns the symbol); tests inject their own stub. `dispatch=dispatch_wave1` / `normalize=normalize_wave2` KEEP their defaults — `dispatch.py`/`normalize.py` are leaf swarm modules that never import reflect, so no cycle. Update Step 1.5 (fallback.py engine — the `run_fallback_ladder` signature) AND Step 3.4 to reflect `stamp` required-no-default, and add to Phase 1 Objective #1 / Step 1.5 an explicit "fallback.py imports ONLY from leaf swarm modules (swarm.dispatch, swarm.normalize) and reflect._diversity — NEVER from reflect.ensemble" invariant + a verification that `python -c "import superclaude.cli.reflect.fallback"` has no circular import.

## IMPORTANT

**I1 — Reflect test-file count wrong: "5 new" → "7 new" (b2 IMPORTANT).**
Lines 121, 424, 464 say "5 new reflect test files"; the task actually creates 7 (items 1.11–1.14, 2.4, 3.7, 3.8) — line 464 even lists 7 filenames after saying "5". Fix all three occurrences to "7 new" and make the Phase-6 structural-conformance QA lens (line 424) and the Post-Completion Glob-verify (line 464) enumerate all 7 correct filenames.

**I2 — Handoff-path inconsistency (phase-structure IMPORTANT).**
Steps 2.6/4.7/5.1/5.2/5.3/6.1 write to `TASK-…/{reviews,plans,reports}/` but only `phase-outputs/{...}` subdirs are created (Handoff File Convention + Step 1.2). Standardize ALL handoff writes to `phase-outputs/{reviews,plans,reports,discovery,test-results}/` and ensure each writing item either relies on Step 1.2 having created the subdirs OR carries a `mkdir -p` create-if-needed. No item may write to a subdir that no item creates.

**I3 — Anti-orphaning: completion items in separate `## Post-Completion Actions` (phase-structure IMPORTANT).**
The POST reflect wrapper item + Update-to-Done sit outside Phase 6's ordering. Internal order IS correct (POST penultimate, Done last, Done gated on POST exit 0). Minimal-risk fix: keep the section but add an explicit gate cross-reference so the completion items are unambiguously the terminal gated steps of the task (Phase 6 completion gate → Post-Completion Actions → POST gate exit 0 → Update-to-Done), and confirm no NON-completion work lives after the Done item. Do NOT introduce a downstream-skill offer after Done.

**I4 — Plan dispatch-vs-escalate ordering not test-closed (alignment IMPORTANT-1; design §4.2 now corrected).**
The design now states the SEQUENTIAL ordering invariant: `T1Model01` is ALWAYS the first fallback dispatched (keyed off `attempts_made`) even when >1 primary failed; `T1Model02` only after `T1Model01` has run and quorum is still unmet. Update the plan unit-test item (1.12/1.13 area, `test_fallback_plan.py`) to add an explicit case: first controller pass with 2 primary failures → asserts `plan_next_attempt` returns `dispatch T1Model01` (NOT `T1Model02`).

## MINOR

- **M1 (b2)** — Undefined provenance shorthand (I16, I20, M3, M4, GAP-2, L3, L5, F1–F7) never defined in-file. Add a one-line legend near the top of `## Detailed Task Instructions` (or the Task Overview) mapping each tag, OR strip the tags from item bodies. Keep F1–F7 (they map to design findings) and add the legend.
- **M2 (b2)** — Step 5.3 output path ambiguous ("…test_ensemble_fallback_stub.py OR a new test_resolve_t1_factory.py"). Pin to ONE filename and make the Post-Completion Glob-verify list it.
- **M3 (b2)** — Step 1.5 bundles docstring+imports+3 dataclasses+frozenset+predicate+type-alias. Optional: split the 3 frozen dataclasses (FallbackDecision/QuorumState/LadderOutcome) into their own sub-item from the `is_fallback_eligible` predicate + `FALLBACK_ELIGIBLE_STATUSES`. Low priority — apply only if it doesn't balloon the item count.
- **M4 (phase-structure)** — Step 6.G9 Glob `qa-final-*.md` over-matches verification/consolidated files on repeat cycles. Pin the glob to the specific expected report filenames.
- **M5 (phase-structure)** — Post-Completion item 3 says "Create" the `### Task Summary` that already exists in the template. Change "Create" → "Populate".
- **M6 (alignment MINOR-1)** — `fallback_attempts_failed` terminal_reason enum token has no emission producer branch. Add a note/item ensuring `run_fallback_ladder` emits it (all attempted slots terminal-failed AND quorum still unmet, distinct from `fallback_pool_exhausted`).
- **M7 (alignment MINOR-2)** — `run_fallback_ladder` (Step 3.4) under-specifies derivation of `build_fallback_metadata`'s `tier2_certification_basis` / `terminal_reason` / `original_primary_pool_fully_succeeded`. Add a one-line derivation note (certification_basis = primary_only vs primary_plus_fallback from whether any fallback is in the contributing set; original_primary_pool_fully_succeeded = no primary failure).
- **M8 (alignment MINOR-3)** — ensure the per-attempt ledger `vendor` field is threaded via the `_diversity._vendor_from_model_id` import (moved with the diversity helpers in Phase 1).

## Verification after fix
- Re-grep the task file: no `stamp: Callable = _stamp_worker_paths` default; no "5 new reflect"; no handoff write to an uncreated subdir; shorthand legend present; Step 5.3 path pinned; plan test case for first-pass-2-failures present.
- Item count remains ~94 (±a few if M3 split applied). All items keep the 5-field B2 body.
