# Synthesis-Gate Verdict (Step 5.19) — TASK-TDD-20260619-235400

**Date:** 2026-06-20
**Pre-fix verdict:** FAIL (1 IMPORTANT + 2 minor; 8-agent gate, 7 PASS / 1 FAIL).
**Action:** fixes applied in-place. Re-verification pending Step 5.20.

## Fixes applied (rf-qa, fix_authorization, code-grounded — see qa/qa-synthesis-fixes-applied.md)
- **S1 (IMPORTANT) — synth-06 §12.4:** 5xx retry "Immediate" → "retry once with **2s backoff** (`on_5xx_backoff_sec=2`)". Verified `dispatch.py:46,224-225,269-273` (backoff slept before the single retry); timeout 180s (`:124,244`). Now consistent with synth-08 §17.2.
- **S2 (MINOR) — synth-08 §19.6:** wrong tmux-subprocess citation `commands.py:267-274` → corrected to **`reflect/commands.py:320`** (the `subprocess.run(["tmux","new-session",...])` in `_launch_tmux`, def L311, attach/kill L325/327). Confirmed `runner.py` + `ensemble.py` have NO raw subprocess → the `{runner.py, ensemble.py}` ban scope genuinely leaves the legit tmux call untouched.
- **S3 (MINOR) — synth-09 §22 Q6:** aligned to flag that a new `derive_verdict` M==0 branch MODIFIES the verdict-derivation path FR-RH2.7 pins as unchanged (deliberate recorded amendment, not a free rename); cross-refs synth-06 §12 + `spec.md:303`.

## Binding ASSEMBLY directives for rf-assembler (Phase 6) — recorded, no synth-file edit
- **S4 — Neutralize internal "(Dn)" directive labels.** The synth files carry orchestration scaffolding labels ("(D1)".."(D7)" research-gate directives, and per-file "Decision Dn") that COLLIDE across files (synth-08 D3=`max_fix_iterations` cap vs synth-09 D3=`ensemble-empty`; synth-09 banner mislabels the recipe directive). These tokens are NOT in spec.md. The assembler MUST strip/neutralize the bare "(Dn)" research-gate-directive citations in the published TDD (keep the substantive content). The §6.4 Key Design Decisions table keeps its own self-contained rows.
- **S5 — §6 sub-numbering.** synth-03 uses §6.6/§6.7; template §6 ends at §6.5 (Multi-Tenancy, correctly skipped as N/A). Assembler should place the Reuse & Consolidation Audit as "§6.5 Reuse & Consolidation Audit" (replacing the skipped multi-tenancy slot) or fold it under §6.4 — no §6.5 gap implied. Architecture Status Note folds under §6.

## Cosmetic minors (left as-is; report-validation + fidelity gates will catch anything material)
Off-by-one citation nits (decorator-line vs class-line ±1 in several models.py cites; synth-03 bare_review.py:66→:67; synth-04 "19 top-level keys" aggregate count). All named symbols exist at cited loci.

**Post-fix status:** IMPORTANT contradiction resolved; minors fixed; assembly directives recorded. Proceed to Step 5.20 verification.
