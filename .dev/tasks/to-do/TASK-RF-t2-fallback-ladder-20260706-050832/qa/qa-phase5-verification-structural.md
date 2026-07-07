# QA Report — Phase 5 Fix-Cycle Verification (Step 5.G2, structural)

**Topic:** TASK-RF-t2-fallback-ladder — Phase 5 real-dispatch fix cycle re-verification
**Date:** 2026-07-07
**Phase:** fix-cycle (report-only, `fix_authorization: false`)
**Fix cycle:** 1 (post-consolidated-findings verification)
**Stance:** ADVERSARIAL — assumed a finding was left unaddressed, a proxy value leaked, the real-dispatch binding was reverted, or HALT provenance was inadequate. Verified independently; modified nothing.

---

## Overall Verdict: PASS

All three actionability fixes (P5-ACT-D1/D2/D3) are present, correct, and genuinely exercise real code paths. No proxy credential value leaked into source or committed artifacts. The `_T1_PROXY_BINDING` real-dispatch binding is intact (non-None dict, NAME-strings only). `contract.py` and `swarm/models.py` are byte-unchanged. HALT provenance now documents the interactive `AskUserQuestion` sign-off, the no-auto-default stance, and the build-time vs execution-time distinction. Both test suites are green. One MINOR documentation observation is recorded (non-blocking; the load-bearing execution-time record supersedes it).

**Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 7 | Grep: 0 (folded into Bash) | Glob: 0 | Bash: 6
(No web research required — all claims are local source-truth.)

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | P5-ACT-D1: raising-factory test folds into `fallback_config_missing`, parametrized over BOTH `TransportEnvError` + `ModelPoolTooSmallError` | PASS | `test_ensemble_fallback_stub.py:267-305` — `@pytest.mark.parametrize("raising_factory", [_raising_transport_env_factory, _raising_pool_too_small_factory], ids=["transport_env_error","model_pool_too_small"])`. `_raising_transport_env_factory` raises `TransportEnvError` (L114-123); `_raising_pool_too_small_factory` raises `ModelPoolTooSmallError(1,2)` (L126-134). Drives REAL `run_fallback_ladder`, asserts `terminal_reason == "fallback_config_missing"` (L301), `certified_with_fallback is False` (L302), contributing set stays `["deepseek-primary"]` (L305). **Source fold confirmed genuine:** `fallback.py:471 except (TransportEnvError, ModelPoolTooSmallError):` → `fallback.py:473 terminal_reason = "fallback_config_missing"` — both types caught, exact reason. Test is not a tautology. |
| 2 | P5-ACT-D2: reversed-ladder test isolates POSITIONAL binding (name-lookup misimpl would fail) | PASS | `test_ensemble_fallback_stub.py:360-389` — `test_resolve_t1_fallback_factory_openai_compat_binding_is_positional_not_name`. Ladder `("T1Model02","T1Model01")` DIVERGES from pool order; asserts `bind("T1Model02").model == "qwen-t1"` (pool[0]) and `bind("T1Model01").model == "deepseek-t1"` (pool[1]). A same-name env-key lookup would bind `T1Model02→deepseek-t1` and fail. Positional binding isolated. |
| 3 | P5-ACT-D3: real-binding tests close every transport; `-W error::ResourceWarning` green | PASS | `_closing_factory` contextmanager (L137-162) tracks + `.close()`s every transport in `finally`. BOTH real-binding tests use it (L355, L385). Ran `uv run pytest tests/cli/reflect/test_ensemble_fallback_stub.py -W error::ResourceWarning -q` → **8 passed, no ResourceWarning**. (Fix agent's honesty note re: httpx 0.28.1 lacking `Client.__del__` is accurate; the `.close()` is the correct durable hygiene fix regardless.) |
| 4 | PROXY-SAFETY (never waived): no proxy VALUE in source/committed artifacts; `_T1_PROXY_BINDING` NAME-strings + int only; fixture values confined to test file | PASS | `ensemble.py:193-198` — `_T1_PROXY_BINDING` = `{"model_prefix":"T1Model0","proxy_url_env":"T1ProxyUrl","proxy_key_env":"T1ProxyKey","max_slots":T1_MODEL_MAX_SLOTS}` — env-var NAME strings + one int ceiling, **zero values**. `grep :4000` in `src/…/reflect/` → none. `grep -rln "t1-proxy:4000\|unit-test-key" src/ tests/` → **only `test_ensemble_fallback_stub.py`**. Case-sensitive value hunt across the whole task dir returned ONLY forbidden-string search-target tokens (in QA reports) and "no `:4000/v1` probe" prose — no real credential value. Committed fixtures `pass_with_t2_fallback.yaml`/`pass_no_t2_fallback.yaml` → no proxy strings. |
| 5 | HALT-INTEGRITY (never waived): provenance documents (a) `AskUserQuestion` mechanism, (b) no auto-default, (c) build-time vs execution-time distinction; internally consistent | PASS (1 MINOR obs) | (a) `t1-proxy-binding-decision.md:11` names the `AskUserQuestion` tool, the literal "Enable real dispatch now" selection, and points to the session transcript; Phase 5 log L548 + Open Questions L517 corroborate. (b) Phase 5 log L548 "HALT honored (not auto-defaulted): the executor PAUSED at the gate and presented the decision … recommended default 'Defer'". (c) Decision doc L11 + Open Questions L516-517 + Phase 5 log L546/L548 distinguish the 2026-07-06 build-time pre-authorization from the 2026-07-07 load-bearing execution-time interactive confirmation. Records are mutually consistent under the stated pre-authorization/load-bearing framing. See MINOR observation below. |
| 6 | Real-dispatch binding NOT reverted; `contract.py`/`swarm/models.py` diffs empty | PASS | `_T1_PROXY_BINDING: dict \| None = {…}` non-None (`ensemble.py:193`); `git status --porcelain` shows `ensemble.py` = ` M` (binding present, not reverted). `git status --porcelain -- contract.py swarm/models.py` → **empty** (unchanged); neither appears in `git diff --stat -- src/`. |
| 7 | `test_ensemble_fallback_stub.py` + `test_ensemble_fallback_engage.py` green | PASS | `uv run pytest …stub.py …engage.py -q` → **10 passed** (stub 8 + engage 2) in 0.21s. |

## Summary

- Checks passed: 7 / 7
- Checks failed: 0
- Critical issues: 0
- Proxy-safety leaks: 0 (never waived — verified clean)
- HALT-integrity defects: 0 (1 MINOR documentation observation, non-blocking)
- Issues fixed in-place: 0 (report-only)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR (observation) | Task file `### Open Questions` L516 | The build-time HUMAN-DECISION entry retains the phrase "the executor proceeds with the confirmed binding and does NOT halt for sign-off" and a title "RESOLVED, operator-confirmed 2026-07-06". Read in isolation, this describes the exact mechanical-env-check → auto-default behavior that P5-HALT-1 flagged; it is redeemed ONLY by the execution-time sub-bullet L517 + Phase 5 log L548 documenting that the executor actually DID pause and present `AskUserQuestion`. The tension is reconcilable (build-time pre-authorization vs load-bearing execution-time confirmation) and was already dispositioned in `qa-phase5-consolidated-findings.md` P5-HALT-1/3, so it is NOT a FAIL — but the residual L516 wording is a latent trap for a future reader who skips the sub-bullet. | OPTIONAL: append a one-clause pointer in L516 (e.g. "— but see the 2026-07-07 execution-time confirmation below, which is the load-bearing sign-off") so the entry cannot be misread as sanctioning auto-default. Documentation-only; does not affect code or verdict. |

## Notes on Unverifiable Ground Truth (disclosed, not a gap)

The *actual* operator selection ("Enable real dispatch now") lives in the interactive session transcript, which is outside my inspection surface. I verified that the record NAMES the mechanism and POINTS to where it is verifiable (as P5-HALT-2 required) — I did NOT and cannot independently re-observe the `AskUserQuestion` tool call itself. This is inherent to interactive sign-off and is the intended audit path; it does not lower the structural verdict because the deliverable under Step 5.G2 is the *documentation* of the sign-off, which is complete and consistent.

## Actions Taken

None — `fix_authorization: false`, report-only.

## Recommendations

- PROCEED to Phase 6. All Step 5.G2 verify criteria (1-7) PASS; proxy-safety clean; HALT provenance documented and consistent; binding intact; tests green.
- OPTIONAL (Phase 6 or follow-up): apply the MINOR L516 wording pointer above to harden the Open Questions entry against isolated misreading.
- Carry forward the already-logged OUT-OF-SCOPE follow-up P5-PS-01 (shared `openai_compat.py send()` URL-in-raw-artifact) — correctly dispositioned as not this task's changed surface; no action here.

## QA Complete
