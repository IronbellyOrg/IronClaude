# QA Report — P6 Content Lens: Domain Accuracy

**Verdict: PASS**

> FILENAME NOTE: the spawn prompt named `qa-content-domain-accuracy-report.md`,
> but that path already holds the **P5** domain-accuracy report (its line 1 is
> "P5 Content Lens: Domain Accuracy (Layer 5 UX / Suggester)"). To avoid
> clobbering the P5 artifact this P6 report is written to
> `qa-content-domain-accuracy-p6-report.md`. The orchestrator should reconcile
> the naming.

**Topic:** Sprint Run 429 / Account-Exhaustion Recovery — P6 (execution-log events + nominator exclusion + docs)
**Date:** 2026-06-18
**Phase:** task-qualitative (single content lens: domain-accuracy)
**Fix cycle:** N/A (fix_authorization: false — report only)
**Stance:** Adversarial / zero-trust. Goal was to find ≥3 ways the P6 semantics are wrong. Result: every domain-accuracy claim held against source. The one apparent contradiction in the manifest's doc summary resolved correctly on close reading (see candidate-defect note #1).

---

## Scope

Report ONLY on the domain-accuracy content lens — whether the implemented
semantics are *correct in the problem domain*: do events fire at the right
re-route/halt points; does the nominator exclusion actually prevent an infra
failure from getting a product-bug bundle; do the KNOWLEDGE.md facts match the
code. Structural/format checks, other lenses, and the rest of the 15-item
task-qualitative checklist are out of scope for this spawn.

---

## Items Reviewed
| # | Check (domain-accuracy sub-claim) | axis | Result | Evidence |
|---|-----------------------------------|------|--------|----------|
| 1a | `session_reset` fires once per account-rotation re-spawn (on RETRY) | none | PASS | executor.py:1070-1081 (per-task) + 2127-2137 (single-session): `write_session_reset` is inside `if action is Action.RETRY_NEW_SESSION:`, emitted immediately before `continue`. |
| 1b | `account_exhaustion_halt` fires when the loop gives up (HALT_MODEL_SWITCH / cap) | none | PASS | executor.py:1082-1101 (`HALT_MODEL_SWITCH`→`FAIL_PROVIDER_EXHAUSTED`, emit, `break`) + 2138-2149 (single-session→`PhaseStatus.PROVIDER_EXHAUSTED`, emit, `break`). |
| 1c | No event fires on the non-exhaustion / normal-ladder path | none | PASS | Whole block gated `if reset_policy is not None` AND `if signal.kind in (SINGLE_ACCOUNT_LIMIT, ALL_ACCOUNT_COOLDOWN)`. NONE/OPERATION_TIMEOUT fall through (executor.py:1102, 2150) to the unchanged status ladder. Edge#1 clean-success-then-429 → `PASS_RECOVERED` with NO emit (executor.py:1055-1057). |
| 1d | Halt event emitted by latch-tripping worker only (no double-emit) | none | PASS | Latch-precheck path (executor.py:1019-1028) sets `FAIL_PROVIDER_EXHAUSTED` but does NOT call `write_account_exhaustion_halt`; only the worker concluding HALT_MODEL_SWITCH (line 1094) emits. |
| 1e | Both events None-guarded; logger threaded to both `_run_one_task` call sites | none | PASS | All 4 emit sites wrapped `if logger is not None:`. Threading: `_run_one_task(..., logger=None)` (executor.py:984); `logger=logger` at call sites 1257 + 1375/1473; single-session loop uses module `logger`. |
| 2a | `select_default_recoverable_tasks` alone is insufficient (only selects fail_recoverable) | none | PASS | rerun_tasks.py:1180 filters `entry.get("status") != "fail_recoverable"` → continue. A `fail_provider_exhausted` task is already excluded by status; the explicit `failure_class=="provider_exhaustion"` guard (1188) is purely defensive. |
| 2b | The fallback filter is the real guard for the realistic leak | none | PASS | rerun_tasks.py:1459-1474: the `if not default_ids:` legacy transcript-discovery fallback nominates ALL non-PASS tasks; it explicitly drops `FAIL_PROVIDER_EXHAUSTED` (`if _status is not TaskStatus.FAIL_PROVIDER_EXHAUSTED`). Only path where a re-routed infra failure could leak into auto-nomination. |
| 2c | Exclusion cannot live in the nominator (`nominate({})` empty-dict context) | none | PASS | `ManualNominator.nominate(context)` returns `list(self.tasks)` verbatim, ignoring `context` (recovery.py:160-161). Callers pass literal `{}` (rerun_tasks.py:1452,1454,1475). No `DriftNominator` exists (recovery.py only: `Nominator`/`ManualNominator`/`ReflectReportNominator`). |
| 3a | re-route-not-wait: no sleeps/backoff added | none | PASS | grep `sleep|backoff|jitter` = 0 hits in recovery_policy.py and in both 429 re-spawn blocks (executor.py:1042-1101, 2119-2150). RETRY path goes straight to `continue` (re-spawn). |
| 3b | infra-not-product-bug: `PhaseStatus.PROVIDER_EXHAUSTED` in `is_terminal` not `is_failure` | none | PASS | models.py:435 PROVIDER_EXHAUSTED ∈ `PhaseStatus.is_terminal`; models.py:453-459 `PhaseStatus.is_failure` = {INCOMPLETE,HALT,TIMEOUT,ERROR} — PROVIDER_EXHAUSTED NOT present. (Distinct: `TaskStatus.FAIL_PROVIDER_EXHAUSTED` IS in `TaskStatus.is_failure`, models.py:66 — both facts stated correctly in KNOWLEDGE.md:296-301.) |
| 3c | cap ≈ pool size (default 8) | none | PASS | recovery_policy.py:46 `max_session_resets: int = 8  # ≈ account-pool size`; spec §8 Q5. |
| 3d | fresh resume budget (new process = new SessionResetPolicy) | none | PASS | `SessionResetPolicy(...)` constructed per-phase inside the executor (executor.py:1356, 1924); a resume is a new process → fresh instance → `_exhaustion_attempts=0`. KNOWLEDGE.md:307. |
| 3e | KNOWLEDGE.md facts (re-route headline, four-way, latch bound, halt seam) match code | none | PASS | KNOWLEDGE.md:284-319 cross-checked: subtype-trap, storm bound `≤cap+(K−1)` matches UNLOCKED-spawn + shared-budget design (executor.py:1058-1068), exclusion split matches 2a/2b. |

---

## Summary
- Checks passed: 13 / 13
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

**Confidence:** Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 9 | Grep: 0 | Glob: 0 | Bash: 4 (each grep/sed call mapped to a specific sub-claim)

(Tool-engagement minimum: 13 sub-claims, 13 tool-backed verifications. Every Read/Bash call targeted a specific cited line range or claim — no padding.)

---

## Adversarial candidate-defect notes (claims I actively tried to break)

1. **Apparent `is_terminal` vs `is_failure` contradiction.** The lens prompt and
   KNOWLEDGE.md reference "infra-not-product-bug" with `is_terminal` framing, while
   spec §4 Layer 2 says the *TaskStatus* goes into the `is_failure` set. Treated as a
   likely contradiction. **Resolved — not a defect:** two different enums.
   `TaskStatus.FAIL_PROVIDER_EXHAUSTED` is correctly in `TaskStatus.is_failure` (so
   resume re-runs it; models.py:66). `PhaseStatus.PROVIDER_EXHAUSTED` is correctly in
   `PhaseStatus.is_terminal` but NOT `PhaseStatus.is_failure` (so the single-session
   halt does not write a product-bug diagnostic; models.py:435 vs 453-459). KNOWLEDGE.md:296-301
   states BOTH distinctly. The user's bullet-3 phrasing is the PhaseStatus fact and is correct.

2. **Double-emit on K>1 halt.** Suspected every worker observing the tripped latch
   would emit `account_exhaustion_halt`, producing N halt events. **Resolved — not a
   defect:** the latch-precheck path (executor.py:1019-1028) classifies the task
   FAIL_PROVIDER_EXHAUSTED *without* emitting; only the single HALT_MODEL_SWITCH worker
   emits (line 1094). One halt event, as the manifest claims.

3. **Defensive guard overstated as load-bearing.** Suspected the manifest overstated
   that `select_default` "alone is insufficient." **Resolved — manifest correct:**
   `select_default` filters on `status == "fail_recoverable"`, so a
   `fail_provider_exhausted` status is already excluded there; the `failure_class` guard
   (1188) is genuinely defensive. The real auto-nomination leak is the transcript-discovery
   fallback, correctly filtered at the caller (1473).

4. **Hidden sleep/backoff.** Grepped the policy module and both re-spawn blocks for
   `sleep|backoff|jitter`. Zero hits — re-route-not-wait holds. (Spec §3.1 permits an
   optional 0-2s jitter; none added — consistent, not a defect.)

No domain-accuracy defect survived verification.

---

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- None — no `## Inherited Structural Verdict` in the spawn prompt (single-lens content spawn). Standalone behavior; nothing relied upon.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Event-firing-point correctness — Read executor.py:1042-1101 + 2119-2150 (emit sites bracketed by RETRY/HALT branches; NONE/TIMEOUT fall-through confirmed).
- Nominator-exclusion real-guard claim — Read rerun_tasks.py:1159-1196 (function) + 1455-1475 (caller fallback filter) + recovery.py:149-161 (nominator ignores context; no DriftNominator).
- KNOWLEDGE.md fact↔code parity — Read models.py:46-68 + 399-459 vs KNOWLEDGE.md:296-319 (distinguished TaskStatus.is_failure vs PhaseStatus.is_terminal).
- re-route-not-wait — Bash grep for sleep/backoff/jitter across recovery_policy.py + both executor 429 blocks (0 hits).

## Recommendations
- None for this lens. Domain-accuracy semantics are correct. Proceed (subject to other P6 lenses / the Phase 7 QA gate).
- Orchestrator: reconcile the report filename collision (P5 report already occupies `qa-content-domain-accuracy-report.md`).

## QA Complete
