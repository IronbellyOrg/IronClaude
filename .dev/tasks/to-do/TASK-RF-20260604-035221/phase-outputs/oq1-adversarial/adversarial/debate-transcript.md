# Adversarial Debate Transcript — OQ-1 Signal B

## Metadata
- Depth: quick (Round 1 only; no rebuttals / invariant-probe / Round 3)
- Advocates: 2 (Opt-1 minimal, Opt-2a localized-deeper) — both sonnet, both read integrity.py / rerun_tasks.py / executor.py / models.py
- Convergence: HIGH on shared assumptions; substantive merits resolve to Opt-2a

## Round 1 — key points

### Opt-1 advocate (minimal)
- Strengths: fails CLOSED (safe); preserves Signal B as independent re-derivation; ~1 line, behavior-neutral, mergeable now; operator-confirmation path already surfaces the suspect seam; keeps shared `_classify_transcript` untouched.
- **Concessions:** "does not fully deliver the recovered-crash-tail UX; if recovered tails are frequent, prompt friction becomes annoying." A-001 ACCEPT, A-002 ACCEPT. Conceded the long-term direction is "design Opt-2a carefully."

### Opt-2a advocate (localized deeper)
- Decisive points: (1) `PASS_RECOVERED` IS success in the model (`is_success`, models.py:49-58) — a gate that permanently rejects it contradicts the core model; (2) the executor's PASS_RECOVERED determination is ALREADY transcript-evidence-based (`detect_error_max_turns` + `_task_completed_before_overrun` requiring completion evidence before overrun, executor.py:997-1011/2321-2330) → Opt-2a trusts a *more appropriate* transcript check, NOT a naked persisted claim; (3) `_classify_transcript` is STRUCTURALLY incompatible with recovered tails (no path to PASS_RECOVERED; error envelope → FAIL_*; rerun_tasks.py:547-593) → Opt-1's widening is a PERMANENT false negative, not a deferral; (4) blast radius stays in integrity.py (does NOT touch shared `_classify_transcript` → rerun failed-task discovery unaffected); (5) double-check PRESERVED (Signal A persisted ∧ artifacts_ok = 2 independent signals).
- Concessions: weakens the literal "independent transcript re-derivation" for recovered tasks; must be narrowly guarded (PASS_RECOVERED only; ordinary PASS still transcript-rechecked); report must surface the recovered basis; regression test mandatory.

## Convergence assessment
- A-001 (recovered tails common): BOTH ACCEPT → resolved.
- A-002 (only Opt-2a safe; Opt-2b out): BOTH ACCEPT → resolved.
- C-001/C-006 (validate vs fail-closed): resolves to Opt-2a on the merits — the Opt-1 advocate's own Weakness-#1 admission (permanent false negative) plus the executor-recovery-is-transcript-evidence point neutralize Opt-1's "independence" defense.
- Residual split: sequencing only (ship Opt-1 now vs do Opt-2a in-PR). Not a merits disagreement.
- Status: CONVERGED on Opt-2a as the correct design; Opt-1 survives only as a ship-now fallback.
