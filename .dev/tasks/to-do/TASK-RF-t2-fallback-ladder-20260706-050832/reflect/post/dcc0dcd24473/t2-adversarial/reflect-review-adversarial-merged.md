<!-- Provenance: produced by /sc:adversarial (Mode A) -->
<!-- Base: Variant 1 (qwen3.6-plus) -->
<!-- Incorporated: Variant 2 (glm-5.2) H1/H2/H3-framing -->
<!-- Adjudication: ground-truth-anchored against TASK-RF-t2-fallback-ladder-20260706-050832.md + phase-outputs/ + qa/ + return-contract.yaml (both sources --suspect-source) -->
<!-- Merge date: 2026-07-07 -->

# Tier-2 Adversarial-Merged Audit Report

**Target:** `TASK-RF-t2-fallback-ladder-20260706-050832.md`
**Audit base:** `d8f84f71a397ed7358b83f48d46691f82aaec51d` (head == start_commit; **working-tree diff by design** per frontmatter L46 — uncommitted task edits ARE audited)
**Ensemble:** qwen3.6-plus + glm-5.2 (kimi-k2.7-code failed, proxy_error 400); both reviews flagged `--suspect-source` and re-verified against the artifact.
**Verdict:** **CONDITIONAL PASS** — the load-bearing *additive-only, verdict-gate-preserving* guarantee holds and the full suite is green; **but** two real process/anti-bias gaps (F-01, F-02) MUST be dispositioned as documented follow-ups before this Done is considered audit-clean.

> **Verdict reconciliation.** qwen returned CONDITIONAL PASS; glm returned CONDITIONAL FAIL. Ground truth supports **neither extreme**: FAIL over-gates (the headline guarantee holds, contract is clean, suite green), while an unqualified PASS ignores glm's confirmed H2/H1. The merged verdict is CONDITIONAL PASS *with mandatory follow-ups*.

---

## 🔍 Concrete Findings (severity-ordered, ground-truth-calibrated)

<!-- Source: Variant 2 (glm-5.2), H2 — merged per Change #1; the highest-value catch, absent from Variant 1 -->
### F-01. Phase 6 Step 6.G11 anti-bias verification self-substituted (IMPORTANT — process/anti-bias, CONFIRMED)
- **Evidence:** 6.G9 consolidation returned **FAIL** (2 IMPORTANT + 5 MINOR) → a fix was applied at 6.G10. Step 6.G11 (`TASK…md:478`) then *requires*, when fixes were applied, spawning two parallel subagents (`rf-qa` + `rf-qa-qualitative`, `fix_authorization:false`) writing `qa/qa-final-verification-structural.md` and `qa/qa-final-verification-content.md`. The Task Log instead records *"Verification (6.G11-equivalent, inline): `pytest -k 'reflect or swarm'` → 2554 passed"* (`TASK…md:582`). **Ground truth:** neither `qa-final-verification-structural.md` nor `qa-final-verification-content.md` exists in `qa/` (verified on disk).
- **Impact:** The green suite cannot confirm the *non-test-covered* 6.G10 fixes were applied — specifically IMPORTANT-2 (stale `_resolve_run_transport_factory` docstring) and the orphan `pass_with_t2_fallback.yaml` fixture / import-allowlist MINORs. Independent spawned re-verification is the anti-bias purpose of 6.G11; inline pytest by the executor defeats it. The executor self-labeled the substitution ("…-equivalent, inline") — honest disclosure, but the gap remains.
- **File:line:** `TASK…md:478` (gate spec), `TASK…md:580` (6.G9 FAIL findings), `TASK…md:582` (inline substitution); absent `qa/qa-final-verification-{structural,content}.md`.
- **Severity:** `IMPORTANT` (not correctness — suite green + additive-only 0-diff hold; but the anti-bias gate was not satisfied as specified).

<!-- Source: Variant 2 (glm-5.2), H1 — merged per Change #2; severity recalibrated CRITICAL→IMPORTANT per Change #7 -->
### F-02. Exit-11 carve-out applied to a label outside its named class (IMPORTANT — governance/traceability)
- **Evidence:** The terminal-gate rule authorizes a documented benign exit-11 *"degraded (single-reviewer-fallback / single-vendor)"* to be judged by `return-contract.yaml` (`TASK…md:499`). The actual `reflect_post.reason` is **`null-convergence`** (frontmatter L37) — a different label. The run in fact reached `tier_reached: 2` with **full** model-class + **multi**-vendor diversity (two heterogeneous reviewers), so it is *not* the single-vendor case the carve-out literally names.
- **Impact:** The executor applied the carve-out by its *rationale* ("environmental, not a content failure") rather than its literal predicate. That judgment is **substantively defensible** — `null-convergence` here is caused by the convergence-scorer + verification tools being unavailable (`verification_skip_reason: tool-unavailable`, `adversarial_convergence_score: null`), against a **clean** contract (`status: success`, `regression: 0`, `degraded_components: []`), consistent with memory `reference_reflect_exit11_degraded_benign`. But the carve-out text should be widened (or the judgment explicitly recorded) so `null-convergence`-from-tool-unavailability is an *in-class* environmental degrade rather than an ad-hoc extension.
- **File:line:** frontmatter L37 (`reason`), `TASK…md:499` (carve-out wording), `TASK…md:586-596` (executor's benign judgment + contract evidence).
- **Severity:** `IMPORTANT` (governance). **Disposition: document the interpretation — do NOT reverse Done.** The contract evidence supports the benign judgment.

<!-- Source: Variant 2 (glm-5.2) H3 + Variant 1 (qwen) #4 — merged per Change #3; "Security" tag dropped per project norm -->
### F-03. `needs_human_decision` HALT sign-off is operator-attested-only (IMPORTANT — auditability)
- **Evidence:** The `_T1_PROXY_BINDING` real-dispatch enablement rests on the executor's own log of an interactive `AskUserQuestion` sign-off (Phase 5 log). `reflect_pre` was **not reconciled** post-execution — the executor explicitly notes *"the frontmatter `reflect_pre.note`… is a historical PRE-reflect record, not reconciled by execution."* Also `reflect_pre.coverage_pct: 1.0` with `tcs: 0` (frontmatter L23/L25) is an odd pairing for a HALT treated as a genuinely open decision.
- **Impact:** The HALT *mechanism* functioned (it blocked real dispatch until sign-off); the *authenticity* of the sign-off cannot be confirmed from the artifact alone. Weight real-dispatch enablement as operator-attested-only.
- **File:line:** frontmatter `reflect_pre` block (L20-29); Open Questions §1; Phase 5 - Real Dispatch Findings.
- **Severity:** `IMPORTANT` (auditability — **not** framed as security, per project norm).

<!-- Source: Variant 1 (qwen) #2 + Variant 2 (glm) M1 — both agreed -->
### F-04. `sprint/aienv.py` modified outside the §10 change map (MINOR — scope)
- **Evidence:** Task Summary lists `src/superclaude/cli/sprint/aienv.py` as modified; the task concedes it is *"outside §10 change map — a docstring-only xref fix, the authorized consequence of the design-sanctioned `_collect_t2_models`→`_collect_models` rename."* No design-revision or operator sign-off trace is cited for the scope extension.
- **Impact:** Even docstring-only out-of-map edits set a scope-creep precedent and complicate cherry-pick/replay. "Docstring-only" is the executor's claim.
- **File:line:** Task Summary "Files modified"; Phase 6 disposition bullet 4.
- **Severity:** `MINOR` (process). **Action:** diff `aienv.py` against base to confirm zero functional change.

<!-- Source: Variant 1 (qwen) #1 + Variant 2 (glm) M2 — both agreed; downgraded IMPORTANT→MINOR per Change #6 -->
### F-05. Test-surface count drift: 8 delivered vs 7/6 enumerated (MINOR — traceability)
- **Evidence:** Task Summary claims 8 new reflect test files including `test_ensemble_fallback_engage.py`; the 6.G2 conformance lens and 6.2 output-verification enumerate **7** (`TASK…md:451,493`), while Phase-6 log/Task-Summary elsewhere say "§9-enumerated **6**" (`TASK…md:527,593`). **Ground truth:** all 8 files exist on disk, run green in the 2554-passed suite, and the two extras (`test_ensemble_fallback_engage.py`, `test_fallback_config.py`) are documented as authorized over-delivery.
- **Impact:** Real but low: the internal "7 vs 6" inconsistency is a doc blemish; the file is present, exercised, and documented — not a masking risk.
- **File:line:** `TASK…md:451,493,515,527,593`; `tests/cli/reflect/test_ensemble_fallback_engage.py` (exists).
- **Severity:** `MINOR` (downgraded from qwen's IMPORTANT: the "untracked → silent regression" concern is refuted by on-disk presence + green suite).

<!-- Source: Variant 1 (qwen) #5 — unique catch, absent from Variant 2 -->
### F-06. Eager→lazy transport-factory resolution is undocumented design drift (MINOR — design)
- **Evidence:** Phase 6 findings: *"the openai_compat T1 arm initially read env EAGERLY at resolve time… Fixed by deferring the env read into a lazy `_lazy_openai_factory`."* Not reflected in `design.md §7.3` or the checklist.
- **Impact:** Lazy factory evaluation defers `TransportEnvError` to dispatch time (late-fail vs early-fail). Covered by `test_resolve_t1_fallback_factory_openai_compat_missing_env_degrades`, but it is a silent deviation from the planned eager-validation contract.
- **File:line:** Phase 6 - Final QA & Verification Findings (eager→lazy bullet).
- **Severity:** `MINOR` (test-covered design drift).

<!-- Source: Variant 2 (glm) H4 — downgraded HIGH→LOW per Change #8 -->
### F-07. `1 xpassed` in the final suite — dispositioned but test unnamed (LOW — rigor)
- **Evidence:** Final suite: *"2554 passed, 28 skipped, 1 xpassed, 0 failed"* (`final-fulltest-raw.txt:2600`). **Ground truth:** `final-fulltest-summary.md:23` dispositions it — *"The 1 xpassed and 28 skipped are pre-existing suite conditions unrelated to this change set (tmux-detached skips, environment-gated cases)."*
- **Impact:** Low. glm's HIGH "silent-regression" concern is refuted by the existing disposition + additive-only 0-diff on `contract.py`. Residual: the specific xpassed test name is not recorded.
- **Severity:** `LOW` (name-the-test rigor only).

---

## 🎯 Suspect-Source Files for Downstream Scrutiny
<!-- Source: Variant 1 (qwen), suspect-source table — preserved from base -->

| File Path | Risk | Reason for Scrutiny |
|-----------|------|---------------------|
| `src/superclaude/cli/reflect/ensemble.py` | **HIGH** | `_T1_PROXY_BINDING` sentinel, `resolve_t1_fallback_factory`, lazy `_lazy_openai_factory`, post-`normalize_wave2` controller seam. Import-cycle, late-fail, proxy-binding risk. |
| `src/superclaude/cli/reflect/fallback.py` | **HIGH** | `plan_next_attempt` state machine, F4 deadline clamping, `build_fallback_metadata`. Off-by-one ladder escalation, wall-clock race, metadata schema drift. |
| `src/superclaude/cli/swarm/transports/openai_compat.py` | **MEDIUM** | `read_env_for_pool` credential parsing; `TransportEnvError` masking; F-06 eager→lazy propagation. |
| `src/superclaude/cli/sprint/aienv.py` | **MEDIUM** | F-04: out-of-§10 edit — diff to confirm docstring-only. |
| `tests/cli/reflect/test_ensemble_fallback_engage.py` | **LOW** | F-05: exists + green; verify no mocked network / additive-only bypass. |

---

## 📊 Pass/Fail Signals
<!-- Source: Variant 1 (qwen) signal table — updated with ground truth + V2 findings -->

| Signal | Status | Evidence |
|--------|--------|----------|
| **Additive-Only Guarantee** | ✅ PASS | `contract.py` + `swarm/models.py` 0-diff (Steps 2.6/4.7/6.G4); no new `WorkerStatus`/`WorkerResult`; `regression: 0`. |
| **Verdict-Gate Integrity** | ✅ PASS | F6 first-match `degraded-tier1` (T6) precedes T10; verdict map unchanged; genuine failure still degrades to exit 11. |
| **Exit-11 Benign Judgment** | ⚠️ CONDITIONAL | Contract clean (success/tier-2/0-regression), but reason `null-convergence` is outside the *named* carve-out (F-02) — document the interpretation. |
| **Anti-Bias Final Verification** | ❌ GAP | 6.G11 spawned re-verification substituted by inline pytest (F-01); required spawn outputs absent. |
| **HALT Auditability** | ⚠️ CONDITIONAL | Operator sign-off attested only in executor log; `reflect_pre` unreconciled (F-03). |
| **Test Coverage** | ✅ PASS | 2554 passed / 0 failed; 1 xpassed dispositioned pre-existing (F-07). |
| **Proxy Safety** | ✅ PASS | No credential values read/printed/staged; names only; P5-PS-01 pre-existing/out-of-scope. |

---

## 📝 Mandatory Follow-Ups for Downstream Scorer

1. **(F-01, blocking-for-audit-clean)** Either run the two 6.G11 spawned verification subagents (`rf-qa` + `rf-qa-qualitative`) confirming each of the 7 consolidated 6.G9 findings was addressed — especially the **non-test-covered** IMPORTANT-2 stale docstring + orphan-fixture MINORs — writing `qa/qa-final-verification-{structural,content}.md`; **or** explicitly accept the inline-pytest substitution as a recorded risk with the two non-test-covered fixes manually re-confirmed.
2. **(F-02)** Widen the terminal-gate carve-out text (or record a standing interpretation) so `null-convergence`-from-tool-unavailability is an **in-class** environmental degrade, judged by `return-contract.yaml`. Do **not** reverse Done — the contract evidence supports benign.
3. **(F-03)** Archive the interactive HALT sign-off transcript alongside `phase-outputs/plans/t1-proxy-binding-decision.md`, or mark real-dispatch enablement operator-attested-only; reconcile or annotate the stale `reflect_pre`.
4. **(F-04)** Diff `src/superclaude/cli/sprint/aienv.py` against base — confirm strictly docstring/comment, zero functional change.
5. **(F-05)** Reconcile the §9 test-surface enumeration (7 vs 6) with the delivered 8; formally record `test_ensemble_fallback_engage.py` + `test_fallback_config.py` as authorized over-delivery in §9.
6. **(F-06)** Confirm `_lazy_openai_factory` propagates `TransportEnvError` to the controller `try/except` (no silent swallow); note the eager→lazy shift in `design.md §7.3`.
7. **(F-07)** Record the specific xpassed test name for the audit trail.

---
*Adversarial merge of 2 Tier-2 reviews. NOT converged on headline verdict (55%); base-selected by combined score (V1 0.825 vs V2 0.742) and best-of-breed findings grafted with ground-truth calibration. See `adversarial/` for diff-analysis, debate-transcript, invariant-probe, base-selection, refactor-plan, merge-log.*
