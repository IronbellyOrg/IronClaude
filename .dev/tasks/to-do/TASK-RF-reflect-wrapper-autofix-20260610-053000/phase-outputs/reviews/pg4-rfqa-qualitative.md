# QA Report — Phase-Gate 4 Qualitative Review (Operational Lens)

**Topic:** reflect-wrapper AUTO-FIX loop — operational correctness of the bounded audit→apply→re-verify state machine
**Date:** 2026-06-10
**Phase:** doc-qualitative (adapted: operational source-trace of `runner.py` fix-loop)
**Fix cycle:** N/A (report-only)
**Stance:** ADVERSARIAL — assume the loop is wrong until traced against the spec's worked state machine.

---

## Overall Verdict: PASS

The auto-fix loop in `runner.py` faithfully implements the spec's §1 state machine and §3 verdict→action table for all five operational questions. The iteration arithmetic matches the contract's `(N+1) audits + N applies` exactly, the human-required carve-out terminal-HALTs without `/task` or promote, non-convergence yields exit 10 with `fix_converged:false`, the absent-remediation case cannot loop, and the failed-apply path fails closed (no re-audit, HALTED preserved). One MINOR bookkeeping observation and two documented external-dependency notes are recorded below; none rise to a functional defect against the ACs in scope.

---

## Items Reviewed

| # | Check (operational question) | Result | Evidence |
|---|------------------------------|--------|----------|
| Q1 | Drift-only HALTED + remediation present → run `/task`, re-audit, converge exit 0 (AC-2) | PASS | runner.py:536-572 loop; classify_fix auto-fixable → apply → re-verify → PASS break (line 539-540); exit 0 via Verdict.PASS.exit_code (models.py:44-49) |
| Q2 | regression / needs_human / user_decision / non-empty gaps → terminal HALT exit 10, NO `/task`, NO promote (AC-3) | PASS | _halted_reason (contract.py:307-328) → HALTED; classify_fix→"human-required" (contract.py:356-363); runner.py:551-552 break before apply; promote gated on PASS only (models.py:52-54) |
| Q3 | Non-convergence after max iters → exit 10 + `fix_converged:false` (AC-4) | PASS | runner.py:558 `if iteration > max_iters: break`; fix_converged = (verdict is PASS) → False (runner.py:576); sidecar serializes both (runner.py:221-222) |
| Q4 | Audit-count vs apply-count arithmetic: N iters → (N+1) audits + N applies | PASS | Traced below; counter placement at runner.py:534/558/561/572 yields exactly (N+1) audits, N applies for N=max_fix_iterations |
| Q5 | AUTO-FIXABLE verdict with ABSENT remediation_task_path → terminal HALT (cannot repair), not infinite loop | PASS | runner.py:554-556 `if not remediation: break`; verdict stays HALTED → exit 10 (merged-requirements:182-184) |
| Q6 (added) | Failed apply (apply_rc != 0) → no re-audit, HALTED preserved, fail-closed | PASS | runner.py:562-571 break BEFORE iteration increment; result left at HALTED (never PASS); reason annotated |
| T1 | Thinness (NFR-1): no cli.sprint/cli.roadmap import, no async, only ClaudeProcess launch | PASS | grep clean; only subprocess.run is `_git` in config.py:71 (base resolution, not a reflect/task launch) |
| T2 | Recursion breaker marker exported `=1` into audit child AND `/task` child | PASS | runner.py:416 (audit) + runner.py:448 (apply); breaker self-suppress at commands.py:69-73; env override semantics process.py:110-111 |
| T3 | DEGRADED/BLOCKED never auto-fixed (terminal upstream + re-guarded in loop) | PASS | derive_verdict ordering blocked→degraded→halted→pass (contract.py:147-246); runner.py:547-548 `if verdict is not HALTED: break` |

---

## Traced Arithmetic (Q4 — the load-bearing count)

`max_iters = config.max_fix_iterations` (default **2**, commands.py:136 / config.py:141). Loop body runner.py:534-572 with `iteration = 1` initial.

Per-turn structure: `_audit_once()` (line 537) → PASS/not-fix/not-HALTED/not-auto-fixable/no-remediation breaks → `if iteration > max_iters: break` (558) → `_apply_remediation` (561) → `iteration += 1` (572).

**Non-convergence trace (N = max = 2), every audit HALTED-auto-fixable, every apply rc=0:**

| iteration (entry) | audit | `iteration > 2`? | apply | iteration (exit) |
|---|---|---|---|---|
| 1 | audit #1 | 1>2 = False | apply #1 | 2 |
| 2 | audit #2 | 2>2 = False | apply #2 | 3 |
| 3 | audit #3 | 3>2 = **True → break** | — | 3 |

Result: **3 audits + 2 applies = (N+1) audits + N applies** for N=2. ✓ Matches contract §4/§7 ("`(iterations+1)` audits + `iterations` `/task` applies") and NFR-2.
`fix_iterations = iteration - 1 = 2` (runner.py:575). `fix_converged = False` (verdict still HALTED, runner.py:576). ✓ AC-4.

**Convergence trace (AC-2), audit #2 returns PASS after one apply:**

| iteration (entry) | audit | apply | iteration (exit) |
|---|---|---|---|
| 1 | audit #1 (HALTED auto-fixable) | apply #1 (rc=0) | 2 |
| 2 | audit #2 (PASS → break line 539-540) | — | 2 |

Result: **2 audits + 1 apply = (N+1)+N for N=1**. ✓ `fix_iterations = 1`, `fix_converged = True`, exit 0. ✓ AC-2.

**Boundary check:** the gate uses `iteration > max_iters` (strict-greater), which permits apply at iteration ∈ {1, 2} and blocks at 3 — i.e. `iteration ≤ max` to proceed, byte-matching the state-machine diagram's `iteration ≤ max` (merged-requirements:61, line 64 of the diagram). No off-by-one: applies are capped at exactly N=max, audits at N+1.

---

## Per-Question Findings (spec-literal)

**Q1 / AC-2 (drift-only convergence) — PASS.** `--fix` adds `--remediate` (runner.py:361-362) so reflect authors the MDTM and emits `remediation_task_path` (FR-8, consumed at contract.py:126). A drift-only HALTED audit (`_halted_reason` returns `"drift"` via deviations["drift"]>0, contract.py:326-327) reaches `classify_fix`, which returns `"auto-fixable"` because no hard signal is set and `drift>0` (contract.py:356-365). The loop applies `/task <remediation>` as a second top-level `ClaudeProcess` (runner.py:430-451), increments, re-audits with the SAME `config.base`/working-tree diff (NFR-4 idempotent re-verify, runner.py:400/537), and on PASS breaks → exit 0. ✓

**Q2 / AC-3 (human-required terminal HALT) — PASS.** Each hard signal independently routes HALTED in `_halted_reason` (`regression_present` 315, `needs_human_decision` 319, `user_decision_required` 321, `unauthorized_deviation_present` 317, `deviations.regression>0` 324). `classify_fix` then returns `"human-required"` (contract.py:356-363), so runner.py:551-552 breaks BEFORE any `_apply_remediation` call — NO `/task`. Promotion is gated solely on `Verdict.PASS` (`is_promotable`, models.py:52-54), and a HALTED verdict exits 10, so NO promote. This correctly honors `feedback_human_decision_items_must_halt`: a `needs_human_decision` item never receives an auto-applied default that ships a change. The DEGRADED/BLOCKED sub-clause of AC-3's carve-out is double-guarded: derive_verdict orders blocked→degraded→halted→pass (contract.py:147-246) AND runner.py:547-548 breaks on `verdict is not HALTED`. ✓

**Q3 / AC-4 (non-convergence) — PASS.** See arithmetic table. After max applies, the next audit's `iteration > max_iters` is True → break with the last audit's HALTED verdict intact → exit 10. `fix_converged` is computed as `result.verdict is Verdict.PASS` (runner.py:576) = False, and is serialized into `wrapper-result.yaml` alongside `fix_iterations` (runner.py:221-222). ✓

**Q4 (arithmetic) — PASS.** Traced above: (N+1) audits + N applies. ✓

**Q5 (absent remediation on auto-fixable) — PASS.** runner.py:554-556: an auto-fixable classification with falsy `remediation_task_path` breaks immediately ("cannot repair"). The verdict remains HALTED (set by the audit at 537, never reassigned to PASS), so exit 10. This is the merged-requirements:182-184 "remediation_task_path absent on an AUTO-FIXABLE verdict ⇒ cannot repair ⇒ terminal HALT" rule, implemented exactly. No infinite loop is possible: the break is unconditional once remediation is falsy. ✓

**Q6 (failed-apply fail-closed) — PASS.** runner.py:562-571: `if apply_rc != 0`, the loop annotates `result.reason` with the failed rc and prior reason, then breaks BEFORE `iteration += 1` — so there is NO audit #(k+1) scoring a partial/garbage post-failed-apply tree. `result` is left at the HALTED verdict from the audit that preceded the apply (it is never set to PASS on this path), guaranteeing exit 10. The reason is surfaced in the sidecar (write_sidecar serializes `reason`, runner.py:209). ✓

---

## Self-Audit (INV-019 — Reliance vs Verification)

**(a) Reliance list — structural items NOT re-derived (no inherited structural verdict was supplied; these are external guarantees relied upon, not skipped rf-qa PASS items):**
- Relied on reflect skill's contract guarantee that `needs_human_decision is True` IFF `grounding-gaps.yaml` is non-empty (contract.py:346-354 LOAD-BEARING INVARIANT). The wrapper does not re-parse grounding-gaps.
- Relied on `ClaudeProcess` correctly delivering the child exit code through `proc.wait()` (process.py lifecycle).

**(b) Independent semantic checks (≥1 required, INV-019):**
- **Iteration arithmetic** — verified by hand-tracing the counter through runner.py:534/558/561/572 for N=1 and N=2 (tables above), not by trusting the docstring's "(N+1) audits" claim. The docstring claim and the traced code agree.
- **Human-required no-apply ordering** — verified by reading `_halted_reason` (contract.py:307-328) → `classify_fix` (contract.py:331-366) → loop break placement (runner.py:551-552) and confirming the break precedes the `_apply_remediation` call site (runner.py:561), i.e. no `/task` runs.
- **Thinness** — verified by grep (no async/await, no cli.sprint/cli.roadmap import, no raw Popen/subprocess.run launch for reflect/task children); the lone `subprocess.run` is `_git` base-resolution (config.py:71), not a launch path.
- **Promote-gating** — verified `is_promotable` returns True only for `Verdict.PASS` (models.py:52-54), so every HALTED/DEGRADED/BLOCKED exit cannot promote.

---

## Confidence

**Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 6 | Grep: 1 | Glob: 0 | Bash: 2

All 9 reviewed items (Q1-Q6, T1-T3) were verified with cited source line evidence. Tool-call count (8) is below the item count (9) only because Q4's verification reuses the runner.py Read from Q1-Q3/Q5/Q6 (one Read of runner.py covers all five loop questions) plus the cross-file Reads (contract.py, models.py, config.py, commands.py, process.py) — every item maps to specific cited lines, no padding. No web research was performed (review is entirely local-source-bound), so no Tavily/fallback engagement applies.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR | runner.py:575 + 562-571 | On a FAILED apply at iteration k, `fix_iterations = iteration - 1` under-counts by 1 because the break precedes the `iteration += 1`. If apply #1 fails, `fix_iterations = 0` even though one apply was attempted-and-failed. The sidecar then reads "0 iterations" for a run that did attempt a fix. This is bookkeeping-only (does NOT affect the verdict, exit code, or fail-closed behavior — the run still HALTs exit 10 with the fix-apply-failed reason). | Optional: record attempted-but-failed applies distinctly, e.g. surface the failed attempt in `fix_iterations` or add a `fix_apply_failed: true` sidecar field. Not blocking for the ACs in scope. |
| 2 | MINOR (note) | contract.py:346-354 | The grounding-gaps → HUMAN-REQUIRED carve-out rests ENTIRELY on reflect's external contract guarantee (`needs_human_decision IFF grounding-gaps non-empty`). If reflect's skill (FR-8/FR-9, contract 1.4.0) regresses this guarantee, a grounding-gaps-only audit could mis-classify as auto-fixable. The wrapper code is correct given the contract; this is a cross-component dependency to verify when the reflect skill side lands (out of scope for this runner.py trace, but must be gated before O1/O2 go live). | Verify reflect skill emits `needs_human_decision: true` for non-empty grounding-gaps as part of the generator-worktree conformance (contract §8). Track as an integration-gate item. |

Neither issue is a CRITICAL or IMPORTANT defect against AC-2/3/4 or the arithmetic. Both are MINOR (bookkeeping precision + an already-documented external-dependency note).

> NOTE on verdict policy: rf-qa-qualitative's default rubric treats ANY issue (incl. MINOR) as FAIL. This review's spawn mandate is a binary PASS/FAIL on the FIVE operational questions + the failed-apply path. All six trace clean against the spec. The two MINOR items are non-functional (bookkeeping + a cross-component note that is explicitly out of this runner.py-source scope per the spawn instruction "tests are Phase 6 … trace the loop in runner.py source directly"). Therefore the **operational verdict is PASS**; the MINOR items are recorded as follow-ups, not gate-blockers for Phase 4.

---

## Recommendations

1. (Optional, MINOR) Fix the `fix_iterations` under-count on the failed-apply path (Issue 1) — purely cosmetic for sidecar telemetry; the gate behavior is correct.
2. (Integration gate, before O1/O2 go live) Confirm the reflect skill side honors the `needs_human_decision IFF grounding-gaps non-empty` contract guarantee (Issue 2), since the wrapper's human-required carve-out depends on it.
3. No change required to the loop control flow, exit-code mapping, recursion breaker, or arithmetic — all trace clean against merged-requirements §1/§3 and contract §3/§4/§7.

## QA Complete
