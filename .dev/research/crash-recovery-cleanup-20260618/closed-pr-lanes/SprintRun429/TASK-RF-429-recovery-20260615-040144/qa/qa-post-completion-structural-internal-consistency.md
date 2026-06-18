# QA Report — Post-Completion Cross-Phase Internal-Consistency (I17 lens)

**VERDICT: FAIL**

**Topic:** Sprint Run 429 / Account-Exhaustion Recovery — full integrated flow (detect → policy → executor → persistence → resume → halt-UX → events → nominator)
**Date:** 2026-06-18
**Phase:** report-validation (post-completion cross-phase structural QA)
**Fix cycle:** N/A
**Fix authorization:** false (report-only)
**Stance:** Adversarial. Verified against actual source files, not manifest claims.

---

## Overall Verdict: FAIL

The 5 named invariants in the spawn prompt all PASS individually. However, the
adversarial cross-phase sweep surfaced **one CRITICAL integrated-flow break** and
**two IMPORTANT consistency defects** that sit *between* the named invariants — exactly
where the manifest asserts the flow "holds together." The CRITICAL finding falsifies
manifest fact #1 ("executor re-spawn → halt") and the in-code claim at executor.py:1894-1895
that "the halt-UX can detect exhaustion regardless of spawn path."

---

## Items Reviewed (the 5 named invariants)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `"provider_exhaustion"` literal byte-identical written (executor) ↔ read (rerun_tasks) | PASS | Written: executor.py:1026,1087,1898,2245. Read: rerun_tasks.py:1188 `entry.get("failure_class") == "provider_exhaustion"`. Byte-identical. |
| 2 | `halt_reason="provider_exhaustion"` set in executor matches `_exhaustion_halt`/`account_exhaustion_output` (models.py) + `write_summary` read | PASS | Set: executor.py:1898,2245. Read: models.py:864 `halted.halt_reason != "provider_exhaustion"`, models.py:870 `tr.failure_class == "provider_exhaustion"`. `write_summary` (logging_.py:343) calls `sprint.account_exhaustion_output()`. Same literal everywhere. |
| 3 | `FAIL_PROVIDER_EXHAUSTED ∈ is_failure`; `PROVIDER_EXHAUSTED ∈ is_terminal`, `∉ is_failure` (diagnostic-bundle safety) | PASS | models.py:66 (in is_failure). models.py:435 (in is_terminal). models.py:454-458 is_failure = {INCOMPLETE,HALT,TIMEOUT,ERROR} — PROVIDER_EXHAUSTED absent. Confirmed: single-session path breaks at executor.py:2296 BEFORE the `status.is_failure` diagnostic block at 2298, AND PROVIDER_EXHAUSTED ∉ is_failure, so no diagnostic bundle is collected for an exhaustion halt. Invariant holds. |
| 4 | Every `PhaseStatus` member in BOTH `STATUS_STYLES` and `STATUS_ICONS`; PROVIDER_EXHAUSTED in both; no member missing | PASS | PhaseStatus has 14 members (models.py:402-422). STATUS_STYLES (tui.py:43-59) = 14 entries incl. PROVIDER_EXHAUSTED:56. STATUS_ICONS (tui.py:63-76) = 14 entries incl. PROVIDER_EXHAUSTED:73. Enumerated both dicts member-by-member: PENDING,RUNNING,PASS,PASS_NO_SIGNAL,PASS_NO_REPORT,PASS_RECOVERED,PREFLIGHT_PASS,PASS_MISSING_CHECKPOINT,INCOMPLETE,HALT,PROVIDER_EXHAUSTED,TIMEOUT,ERROR,SKIPPED — all present in both. No member missing. |
| 5 | Detector `resolved_model` (captured by `_RE_ALL_ACCOUNT`) flows to `suggest_alternate_model` + halt UX | PASS | `_RE_ALL_ACCOUNT` named group `model` (monitor.py:41-42) → `ProviderFailureSignal.resolved_model` (monitor.py:288,328) → executor stores `exhausted_model = signal.resolved_model or ""` (executor.py:1089,2139) → persisted `phase_result.exhausted_model` (1899,2246) → `_exhaustion_halt` returns it (models.py:874) → `suggest_alternate_model(exhausted_model)` (models.py:887,920). Chain intact. `suggest_alternate_model` None-safe (aienv.py:112-119, returns None never fabricates). |

**All 5 named invariants: PASS.**

## Additional adversarial cross-phase checks (between the named invariants)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 6 | Per-task spawn path actually HALTS the sprint on provider-exhaustion | **FAIL (CRITICAL)** | executor.py:1838-1917 — per-task phase branch. On any non-all-pass it sets `status=PhaseStatus.ERROR` (1882), sets `phase_result.halt_reason="provider_exhaustion"` (1898), then unconditionally `continue`s (1917). It NEVER sets `sprint_result.outcome=HALTED` or `sprint_result.halt_phase`. |
| 7 | `halt_reason` persisted on per-task path is reachable by the halt-UX | **FAIL (CRITICAL, same root)** | `_exhaustion_halt` short-circuits to `None` when `self.halt_phase is None` (models.py:858-859). Per-task path never sets `halt_phase` (only 2295/2326 do, both single-session-path). So per-task `halt_reason="provider_exhaustion"` is dead data — `resume_command`/`account_exhaustion_output` never surface it. |
| 8 | Enum-value vs string-literal confusion (`"provider_exhausted"` vs `"provider_exhaustion"`) | PASS | Only one `"provider_exhausted"` occurrence: the PhaseStatus enum VALUE at models.py:419. All `halt_reason`/`failure_class` comparisons use `"provider_exhaustion"`. No cross-confusion. |
| 9 | Per-task orchestration-level halt covered by a test | **FAIL (IMPORTANT)** | The HALTED orchestration tests (test_executor.py:434/497/525/591) all use `_run_single_session_provider_cooldown` (single-session path only). `test_provider_exhaustion_single_429_stops_at_cap` (846-883) MANUALLY constructs `PhaseResult(status=ERROR, halt_reason=...)` (868-877) — it does not exercise the per-task phase loop. No test asserts the per-task phase loop yields `outcome==HALTED`/`halt_phase==N`. The gap that hides Finding 6 from CI. |

---

## Summary
- Named invariants passed: 5 / 5
- Additional cross-phase checks: 4 (8 total checks run beyond the 5)
- Checks failed: 3 (Findings 6, 7, 9; 6 & 7 share one root cause)
- Critical issues: 1 root cause (Findings 6+7)
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | executor.py:1882,1898,1917 | Per-task spawn path collapses a provider-exhaustion to `PhaseStatus.ERROR`, sets `halt_reason="provider_exhaustion"`, then `continue`s to the next phase. It never sets `sprint_result.outcome=HALTED` or `sprint_result.halt_phase`. A 429/account-exhaustion that lands on the per-task execution path does NOT halt the sprint — the sprint runs the remaining phases against an exhausted account pool. This directly falsifies manifest fact #1 ("executor re-spawn → halt"). | After deriving `halt_reason` (1896-1900), if any task is `provider_exhaustion`, set `sprint_result.outcome=SprintOutcome.HALTED`, `sprint_result.halt_phase=phase.number`, and `break` instead of falling through to `continue` (1917) — mirroring the single-session branch at 2293-2296. Consider promoting the phase `status` to `PhaseStatus.PROVIDER_EXHAUSTED` for symmetry (keeps it out of `is_failure`, avoids the diagnostic-bundle collector — the diagnostic-bundle-safety invariant from #3). |
| 2 | CRITICAL | models.py:858-859 vs executor.py:1898 | The in-code claim at executor.py:1894-1895 ("the halt-UX can detect exhaustion regardless of spawn path (IP-3/IP-5)") is FALSE. `_exhaustion_halt` returns `None` whenever `self.halt_phase is None`, and the per-task path never sets `halt_phase`. The per-task `halt_reason`/`exhausted_model` are written but unreachable by `resume_command`/`account_exhaustion_output`. Same root cause as Issue 1. | Fixing Issue 1 (setting `halt_phase` on the per-task path) makes the persisted `halt_reason` reachable and resolves this. Until then, the comment at 1894-1895 overclaims and should not be trusted. |
| 3 | IMPORTANT | tests/sprint/test_executor.py | No orchestration-level test exercises the per-task phase loop's exhaustion-halt. `test_provider_exhaustion_single_429_stops_at_cap` hand-builds the `PhaseResult`; the HALTED tests are single-session only. This is why Findings 1 & 2 passed the full suite (manifest fact #5: "1228 sprint tests pass") undetected — the suite is green because the broken path is unexercised. | Add an integration test that runs the per-task phase loop (`tasks=` inventory) through `execute_sprint`/`run_sprint` with an all-account-cooldown fixture and asserts `result.outcome == SprintOutcome.HALTED` and `result.halt_phase == N`. It will fail against current code, proving Finding 1. |

## Notes on the "≥5 errors" framing
The adversarial prompt posited ≥5 internal-consistency errors. The verified finding count
is 3 (2 CRITICAL sharing one root cause + 1 IMPORTANT test gap). I did NOT manufacture
additional findings to reach a target count — the 5 named invariants genuinely PASS, and
fabricating defects to hit a quota would itself violate zero-trust QA. The single CRITICAL
root cause (per-task path never halts) is severe enough to fail the gate on its own: it
breaks the headline integrated-flow guarantee the manifest exists to certify.

## Recommendations
1. **Block release of the per-task exhaustion path** until Issue 1 is fixed. The single-session path is correct and fully wired; the per-task path detects + persists but does not act.
2. Add the orchestration-level per-task halt test (Issue 3) FIRST (red), then fix executor.py (green) — TDD ordering proves the fix.
3. Re-run this cross-phase QA after the fix; specifically re-verify that `_exhaustion_halt` returns non-None on a per-task halt and that `account_exhaustion_output()` renders the re-route block.
4. Correct or remove the overclaiming comment at executor.py:1894-1895 once behavior matches.

---

## Confidence Gate

- **Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 8 | Grep: 6 | Glob: 0 | Bash: 6
- All 9 checks (5 named + 4 cross-phase) verified with direct file:line tool evidence. Every PASS cites the exact lines read; every FAIL cites the exact lines that conflict. No item relied on the manifest or another report.
- No web research required (all claims are local source-truth; Tavily not engaged).

## QA Complete
