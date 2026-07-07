# QA Report — Report Validation (Step 4.G3, no-fork/additive lens)

**Topic:** reflect Tier-2 fallback model ladder — additive-only T1 slot resolution
**Date:** 2026-07-07
**Phase:** report-validation (no-fork/additive lens, report-only)
**Fix authorization:** false

## Overall Verdict: PASS

The adversarial hypothesis ("primary T2 path broken in ≥3 ways") is NOT borne out. The T2 path is preserved byte-for-byte.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `read_env(env=None)` keeps EXACT public signature (thin wrapper) | PASS | `openai_compat.py` signature unchanged; body delegates to `read_env_for_pool(...T2 constants...)`. All 24 call sites valid (single positional/empty arg). Parity test asserts wrapper == pool reader. |
| 2 | `_resolve_run_transport_factory` defaults reproduce T2 byte-for-byte; primary sites pass no new params; D2 guard + `pool[i%len]` unchanged | PASS | New params all `Optional[...]=None`. Primary sites (run/resume/reflect T2) pass none → T2 constants. `read_env_for_pool` body is the verbatim old-`read_env` body (only constants→params substituted). D2 guard + positional map unchanged. |
| 3 | `_collect_models` is a generalization, not copy-paste | PASS | Single method with one loop `range(1, max_slots+1)`; called twice (T2 + T1). No `_collect_t2_models` body survives. |
| 4 | No proxy creds surface out of resolver closures | PASS | `base_url`/`api_key` used only inside transport closures; never returned/logged. Error echoes carry env-var NAMES only (`TransportEnvError.missing`). |
| 5 | T1 arm does NOT hard-code creds active; gated `_T1_PROXY_BINDING=None`; degrades | PASS | Sentinel None; `_gated_factory` raises `TransportEnvError` on invocation; real-dispatch path unreachable while None. |
| 6 | Full swarm suite green + `swarm/models.py` diff empty | PASS | `uv run pytest tests/swarm/ -q` → 2255 passed, 26 skipped; `git diff -- swarm/models.py` empty. |

## Summary
- Checks passed: 6 / 6
- Critical issues: 0

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | INFORMATIONAL | `commands.py` pool-param defaults, `ensemble.py` resolver | Pool-param defaulting uses truthiness (`max_slots or T2_MODEL_MAX_SLOTS`) rather than `is None`. A future caller passing `max_slots=0`/empty prefix would silently fall back to T2. No current caller triggers this. | Optional hardening: `... if x is not None else CONST`. Not required for acceptance. |
| 2 | INFORMATIONAL | verify-item wording vs `reflect/ensemble.py` | The gated arm lives in `resolve_t1_fallback_factory` in `reflect/ensemble.py`, not `openai_compat.py` (which stays pool-agnostic). Substance satisfied; location note only. | None. |
| 3 | MINOR (OUT-OF-SCOPE) | `src/superclaude/cli/sprint/aienv.py:52` | Docstring cross-reference `Mirrors :meth:`SwarmConfig._collect_t2_models`` points at the method renamed to `_collect_models`. Stale doc pointer, no runtime effect. Not one of the four scope files. | If touched later: update to `_collect_models`. |

## Recommendations

Green light for the no-fork/additive lens. Optional non-blocking follow-ups: harden the two `or`-defaults (Finding 1) and refresh the `sprint/aienv.py:52` docstring pointer (Finding 3).

## QA Complete
