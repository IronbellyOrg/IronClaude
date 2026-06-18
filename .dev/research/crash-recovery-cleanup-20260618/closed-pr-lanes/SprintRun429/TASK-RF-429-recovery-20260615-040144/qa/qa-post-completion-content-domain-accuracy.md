# QA Report — Post-Completion Cross-Phase (Domain-Accuracy Lens)

**VERDICT: FAIL** — 1 IMPORTANT integration gap (per-task path never surfaces the
account-exhaustion halt UX / model-switch resume; falls back to a `--start` resume
that re-runs the exhausted model — the exact anti-pattern the spec forbids).
7 of 7 named contracts otherwise verified PASS at the code level.

**Topic:** Sprint Run 429 / Account-Exhaustion Recovery
**Date:** 2026-06-18
**Phase:** doc-qualitative (post-completion cross-phase, I17 lens — domain accuracy)
**Fix authorization:** false (report-only)
**Stance:** adversarial / zero-trust — read actual source + spec, not the manifests.

---

## Overall Verdict: FAIL

The 7 explicitly-named domain contracts are each individually correct in the code
that implements them. The FAIL is one **integrated-behavior** gap that only shows
up when you trace the per-task (task-delegation) spawn path end-to-end through to
the terminal halt UX — which is the path the real 429 transcripts
(`phase-3-task-T03.14-output.txt`, per-task-named) actually exercise.

---

## Contracts Reviewed (the 7 named + integration trace)

| # | Contract | Result | Evidence |
|---|----------|--------|----------|
| 1 | Re-route never wait (no sleep/backoff) | PASS | `recovery_policy.py` pure decide, no sleep. `executor.py:1081` RETRY=`continue` (re-spawn), `:2137` single-session=`continue`. The only `time.sleep` near recovery (`:2099`) is the pre-existing TUI 2 Hz poll, outside the re-spawn decision. grep `sleep\|backoff\|\.wait(` in recovery_policy/aienv = 0 recovery hits. |
| 2 | Infra ≠ product-bug (PROVIDER_EXHAUSTED short-circuits diagnostic bundle) | PASS | Only ONE `DiagnosticCollector` call site: `executor.py:2301`, inside `if status.is_failure:` at `:2298`. Guarded by explicit `if status == PROVIDER_EXHAUSTED: …break` at `:2293` (before 2298). Double-guarded: `PhaseStatus.PROVIDER_EXHAUSTED ∈ is_terminal` (`models.py:435`) but **∉ is_failure** (`models.py:453-459`). Per-task path ends at `continue` (`:1917`) and never reaches the 2298 block at all. |
| 3 | Storm bound = ≤cap+(K−1), NOT strictly ≤cap (unlocked-spawn/locked-latch) | PASS | `_run_one_task`: latch precheck under `guard` (`:1019-1022`), spawn UNLOCKED (`:1030-1038`), budget claim + latch trip under `guard` (`:1066-1085`). Test `test_executor.py:931` asserts `cap <= calls["n"] <= cap + (len(tasks)-1)`. Infinite-loop guard test `:972` asserts exactly `cap` spawns. |
| 4 | Fresh resume budget — new process builds a new SessionResetPolicy | PASS | Per-phase construction (`executor.py:1356` per-task; `:1924` single-session). Budget is in-memory `_exhaustion_attempts` (`recovery_policy.py:47`), never persisted to cross-run `recovery_history`. A resume re-enters `run_sprint` and reconstructs the policy → fresh `cap`. |
| 5 | Single-line halt UX + None-safe suggester (never fabricates an alias) | PARTIAL→FAIL | Builder produces single-line resume (`models.py:1223`/`:1238`); None-safe branch (`:1226-1240`) gives generic guidance, no fabricated alias. `suggest_alternate_model` returns `None` (never invents) at `aienv.py:111-112,118`. **BUT** this UX is unreachable on the per-task path — see Issues Found #1. |
| 6 | OQ-1 = os.environ reader (option A); OQ-2 = select_default filter (option a); alternatives documented-not-shipped | PASS | OQ-1: `aienv.py:9-26` ships os.environ reader, documents rejected file-parser (option B). OQ-2: `rerun_tasks.py:1182-1189` `select_default_recoverable_tasks` excludes `failure_class=="provider_exhaustion"`; `run_rerun_tasks` fallback filter `:1460-1473` excludes `FAIL_PROVIDER_EXHAUSTED`. |
| 7 | Detector keys on LAST result event `is_error`+`api_error_status`, never `subtype` | PASS | `monitor.py:_provider_failure_from_text:302-321` — overwrite-no-break loop keeps last `{"type":"result"}` (`:313-314`), reads `is_error`+`api_error_status` (`:319-320`). Docstring + offline classifier (`rerun_tasks.py:592`) share the same core. Regexes (`monitor.py:41-44`) match spec §2 verbatim. |

---

## Summary
- Named contracts verified: 6/7 PASS, 1 PARTIAL (UX correct but unreachable on the primary path)
- Integration gaps found: 1 IMPORTANT
- Critical issues: 0
- Confidence: Verified 7/7 | Unverifiable 0 | Unchecked 0 | Confidence 100%
- Tool engagement: Read 9 | Grep 8 | Glob 0 | Bash (find/cat) 4

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | `executor.py:1838-1917` (per-task phase block) vs `models.py:858` (`_exhaustion_halt` gates on `halt_phase`) | **Per-task provider exhaustion never surfaces the account-exhaustion halt UX and re-runs the exhausted model.** On the per-task delegation path a 429-exhausted phase collapses to `PhaseStatus.ERROR` (`:1882`) and persists `phase_result.halt_reason="provider_exhaustion"` (`:1898`), then `continue`s (`:1917`). It does **not** set `sprint_result.halt_phase` and does **not** break the sprint loop. `sprint_result.halt_phase` is assigned ONLY at `:2295`/`:2326` — both inside the **single-session** branch (≥`:1923`). Because `SprintResult._exhaustion_halt()` returns `None` when `halt_phase is None` (`models.py:858-859`), the whole exhaustion-aware chain is dead on this path: `account_exhaustion_output()` returns `""` (`:914-915`) and `resume_command()` falls through to the generic `--start {N} --end` form (`models.py:897-901`). That generic resume re-runs the **same exhausted model** — the precise anti-pattern the `resume_command` docstring (`models.py:850-851`) and UX-contract #6 warn against ("recovered by a MODEL SWITCH, not by re-running the same model at the same phase"). The 429 ground-truth transcripts referenced by the spec (`phase-3-task-T03.14-output.txt`) are per-task-named, so this is the **primary** real-world scenario, not an edge. The misleading comment at `models.py:853-854` claims halt_reason is "derived from per-task `failure_class` on the per-task path" — the *phase-level* derivation happens, but `halt_phase` is never set, so `_exhaustion_halt()` can never locate it. | In the per-task phase block, when any `task_result.failure_class == "provider_exhaustion"`, set `sprint_result.outcome = SprintOutcome.HALTED` and `sprint_result.halt_phase = phase.number`, then `break` the phase loop (mirroring the single-session short-circuit at `:2293-2296`) — instead of `continue`ing to the next phase against a dead pool. Add an end-to-end test: per-task phase exhausts → `SprintResult.account_exhaustion_output()` is non-empty AND `resume_command()` carries `--model`. |

### Why IMPORTANT and not CRITICAL
No data loss, no product-bug bundle misfire (contract #2 holds on every path), no crash. Prior successful task state IS preserved (results appended at `:1911`), and `halt_reason`/`exhausted_model` ARE persisted to `phase-N-result.json`, so a manual operator can recover. The damage is (a) the operator gets a resume command that re-pins the exhausted model rather than the model-switch command the entire P5 layer was built to emit, and (b) the sprint keeps launching subsequent phases against the exhausted pool instead of halting cleanly (UX-contract #5 "clean halt" is not honored on this path). Recoverable-but-wrong UX on the primary path ⇒ IMPORTANT.

---

## Adversarial axes I probed and that PASSED (negative results, for trust)
- **`decide` off-by-one** (`recovery_policy.py:68-71`): `attempt < cap` ⇒ RETRY, so `attempt == cap` ⇒ HALT — exactly `cap` spawns. Test `:972`/`:936` confirms. Not a bug.
- **`subtype:"success"` trap** (contract #7): detector reads `is_error`/`api_error_status`, never `subtype`. The offline classifier (`rerun_tasks.py:584-585`) reads `subtype` only for the *legacy* error-prefix ladder, but the 429 branch (`:592-605`) sits ABOVE it and uses the shared structured-field core. Not a bug.
- **Completed-then-trailing-429** (edge #1): gated by `_task_completed_before_overrun` on both live (`executor.py:1055`) and offline (`rerun_tasks.py:603`) via the shared `completed_before_overrun_from_text` core ⇒ PASS_RECOVERED, no re-spawn. Not a bug.
- **Cross-run budget poisoning** (contract #4 / edge #4): budget is in-memory only; not folded into `recovery_history`. Not a bug.
- **Diagnostic bundle on per-task FAIL_PROVIDER_EXHAUSTED**: per-task path `continue`s at `:1917` and never reaches the `:2298` diagnostic block; single-session path is short-circuited at `:2293`. Bundle never fires for exhaustion. Not a bug (contract #2 robustly holds — this is the same code locus as Issue #1 but the *bundle-suppression* dimension is correct; only the *halt-UX-surfacing* dimension is broken).

---

## Self-Audit

**(a) Reliance list — manifest claims NOT independently re-verified (relied on):**
- Relied on manifest fact #5 (1228 sprint tests pass / 21 pre-existing failures) — did not re-run the suite; out of scope for the domain-accuracy lens.
- Relied on manifest claim of "no broken imports" — verified `recovery_policy.py` imports `monitor.ProviderFailure` and `aienv` imports `swarm.config` symbols by reading, not by executing.

**(b) Independent semantic checks (≥1 required):**
- Contract #2 bundle-suppression — independently traced ALL `DiagnosticCollector` call sites via grep (1 hit) + read both guards (`:2293`, `:2298`) + the `is_failure` membership set (`models.py:453-459`). Manifest asserted membership tuple; I verified the *control flow* that consumes it.
- Issue #1 — independently traced `halt_phase` assignment (grep: 2 sites, both single-session) → `_exhaustion_halt` gate (`models.py:858`) → `account_exhaustion_output`/`resume_command` fall-through. The manifest's fact #1 ("full flow holds … → exhaustion-aware halt UX (P5)") asserts this chain holds on every path; my own tool work shows it does NOT hold on the per-task path. This is the inflation the manifest's green self-report masked.

---

## Recommendations
1. **Fix Issue #1** before shipping: wire the per-task phase block to set `halt_phase`/`HALTED` and break on `failure_class == "provider_exhaustion"`, then add the missing end-to-end halt-UX test. This is the single blocker.
2. After the fix, re-run this domain-accuracy lens to confirm `account_exhaustion_output()` is non-empty and `resume_command()` carries `--model` for a per-task exhaustion fixture.

## QA Complete
