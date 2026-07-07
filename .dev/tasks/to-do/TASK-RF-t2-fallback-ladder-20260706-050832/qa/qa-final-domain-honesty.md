# QA Report — Step 6.G8 Reflect-Fallback Verdict-Honesty DOMAIN Lens

**Topic:** Tier-2 fallback model ladder — verdict-honesty guarantee
**Date:** 2026-07-07
**Phase:** report-validation (domain honesty lens)
**Fix cycle:** N/A (report-only, fix_authorization: false)
**Stance:** ADVERSARIAL — assumed the honesty guarantee was broken in ≥5 subtle ways and hunted for each.

---

## Overall Verdict: PASS

No CRITICAL or IMPORTANT verdict-honesty break found. The core structural guarantee
(design §1) holds end-to-end: **the fallback controller injects only the additive,
gate-invisible `t2_fallback` telemetry block; every verdict-bearing field is recomputed
by `build_reflect_contract` from the augmented `WorkerResult` success set, and the
unchanged `derive_verdict` chain certifies/degrades on its own existing rules.** Three
LOW/INFO observations are recorded below — none is structurally capable of producing a
false PASS.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Controller never sets a degraded field itself; only leaves contributing set short | PASS | `run_fallback_ladder` returns `LadderOutcome(contributing_workers, ledger, metadata)`. `run_tier2_ensemble` sets `normalized_workers = ladder_outcome.contributing_workers` (ensemble.py:374) then `build_reflect_contract(..., t2_fallback=fallback_metadata)` (L490). `build_reflect_contract` hardcodes `degraded_components: []` (L790) and recomputes `tier_reached`/`merge_method`/`t2_model_class_diversity`/`t2_vendor_diversity` from `succeeded` (L731-737, L767-768). No degraded/halt field is authored by the controller. |
| 2 | `evaluate_quorum.satisfies_tier2` never over-certifies vs `derive_verdict` | PASS | fallback.py:157-161 gate = `count>=2 AND mcd=='full' AND (vendor=='multi' OR allow_single_vendor)`. Each conjunct maps to avoiding a degrade trigger: count>=2 ⇒ `tier_reached==2` avoids T6 (contract.py:271) & `merge_method==adversarial` avoids T10 (:288); mcd=='full' avoids T7 (:276); vendor gate avoids T8 (:280). `allow_single_vendor` is the SAME `config.allow_single_vendor` in both `evaluate_quorum` (fallback.py:424) and `derive_verdict` (runner.py:545) — no flag divergence. `WorkerStatus` vocab = {success,timeout,parse_error,proxy_error} (swarm/models.py:69), all-3 failures fallback-eligible, so the success/eligible partition is total. |
| 3 | T6 `degraded-tier1` precedes T10 `single-reviewer-fallback` on §8 counter-case | PASS | `_degraded_reason` is first-match; T6 at contract.py:271-272 executes before T10 at :288-289. Counter-case (1 success → `tier_reached=1`, `merge_method=single-reviewer-fallback`) returns `degraded-tier1`. contract.py is byte-unchanged: `git diff HEAD -- contract.py` empty (rc=0); not in `git status` M-list. |
| 4 | `t2_fallback.terminal_reason` is telemetry ALONGSIDE the real reason, never the gate | PASS | `grep t2_fallback contract.py` → 0 matches (rc=1). `grep terminal_reason contract.py` → 0 (rc=1). End-to-end: `grep t2_fallback\|terminal_reason\|certified_with_fallback\|certification_basis` across runner.py+commands.py+models.py → 0 (rc=1). Verdict flows solely through `derive_verdict(contract, ...)` (runner.py:542). Gate is blind to the entire fallback block, including its nested keys. |
| 5 | No proxy key/url leaks into any emitted contract | PASS | Emitted `t2_fallback` (build_fallback_metadata) + ledger (`_ledger_entry`) carry only: policy strings, `ladder` slot NAMES, `model_id` (model identifier, e.g. `T1Model01` — not a URL), derived `vendor`, `status`, slot-name `attempt_id`s. Proxy creds (`pool_config.base_url`/`api_key`) are confined to the `_build_transport` closure (ensemble.py:269-278) and never written to a `WorkerResult` field or metadata. `grep` for value-bearing url/key in ensemble/fallback finds only env-var NAME strings and the `api_key=pool_config.api_key` transport-constructor arg. |
| 6 | needs_human_decision degrade branch (binding None) still exists & structurally blocks real dispatch | PASS | ensemble.py:230-235: `if _T1_PROXY_BINDING is None:` returns `_gated_factory` that RAISES `TransportEnvError` on invocation → caught in run_fallback_ladder (fallback.py:471) → `terminal_reason=fallback_config_missing` → degrade. No `OpenAICompatTransport` is ever constructed on this branch (no network). Branch is present even though `_T1_PROXY_BINDING` is now the confirmed non-None dict (ensemble.py:193-198). |
| 7 | Enabled openai_compat arm degrades incomplete env to `fallback_config_missing` (lazy), no crash | PASS | Confirmed branch returns `_lazy_openai_factory` WITHOUT reading env at resolve time (ensemble.py:286). `read_env_for_pool` is deferred INTO the factory body (:259), invoked inside `_dispatch_one_fallback`'s eager `transport_for_fallback_slot(slot_name)` (fallback.py:372), inside the try/except (:459-474). `read_env_for_pool` uses `.get() or ""` and raises exactly `TransportEnvError` on missing url/key/models (openai_compat.py:186-205) — no KeyError. Pool-too-short raises `ModelPoolTooSmallError` (make_fallback_slot_factory) — also caught. Both → `fallback_config_missing` degrade, never a crash. |

## Summary

- Checks passed: 7 / 7 core verification points (+ contract.py-unchanged sub-check)
- Checks failed: 0
- Critical honesty breaks: 0
- Important honesty breaks: 0
- LOW/INFO observations: 3 (none affects verdict honesty)
- Issues fixed in-place: 0 (report-only)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| O1 | LOW (telemetry, NOT honesty) | fallback.py:217-248 `select_contributing_set`; ensemble.py:374 | On the enabled path, the contributing set is trimmed to the smallest tier-2-satisfying subset even when no fallback was dispatched, so a healthy 3-primary run reports `reviewer_count=2` where the disabled path would report 3. No false PASS is reachable: a subset is only ever ≤ the full set in diversity, and `select_contributing_set` returns a subset ONLY when it genuinely satisfies the gate (≥2 real reviewers); otherwise it returns all successes and the gate degrades on tier1/diversity. Design-sanctioned ("smallest satisfying set", §4.2). | None required for honesty. Optionally document the enabled-path reviewer_count delta so telemetry consumers don't read it as reviewer loss. |
| O2 | LOW (robustness, NOT honesty) | fallback.py:459-474 | The dispatch try/except catches only `(TransportEnvError, ModelPoolTooSmallError)`. Any OTHER failure raised by `dispatch`/`stamp`/`normalize` propagates out of `run_tier2_ensemble` → non-zero child exit → `derive_verdict` routes BLOCKED (fail-loud, honest). Blast radius is asymmetric: an incomplete env degrades gracefully, but a transient dispatch fault becomes a hard BLOCKED rather than a graceful degrade. | None required for honesty (BLOCKED is the correct fail-loud outcome). Consider widening only if graceful degrade on transient dispatch faults is desired. |
| O3 | INFO | fallback.py:194-199 | `plan_next_attempt`'s `diversity_unrepairable` branch tests `vendor_diversity != "multi"` without consulting `allow_single_vendor`. Unreachable when `allow_single_vendor=True` (the `quorum.satisfies_tier2` short-circuit at fallback.py:180 returns `certified` first), so the slug is never mislabeled in practice. Pure telemetry regardless — not gate-read. | None. |

## Adversarial Hunt Log (the ≥5 suspected breaks, each dispositioned)

1. **Flag divergence over-cert** (evaluate_quorum vs derive_verdict use different `allow_single_vendor`) → DISPROVEN: both read `config.allow_single_vendor` (fallback.py:424, runner.py:545).
2. **Non-eligible failure status inflating `original_primary_pool_fully_succeeded`** → DISPROVEN: `WorkerStatus` has exactly 4 values, all 3 non-success are fallback-eligible; the partition is total, so `len(eligible_failures)==0` ⇔ all primaries succeeded.
3. **`select_contributing_set` all-successes fallback (L248) certifying a non-satisfying ≥2 set as PASS** → DISPROVEN: that path yields `tier_reached=2` + degrade on T7/T8 (or tier1 if <2); `certification_basis=not_certified`; verdict degrades (exit 11). If the full set satisfied, the size=len iteration would have returned it before the fallback, so the fallback is only reached when even the full set degrades.
4. **Nested `t2_fallback` key colliding with a gate-read top-level field** → DISPROVEN: block is nested under `contract["t2_fallback"]`; gate reads top-level keys only; grep confirms 0 reads.
5. **Proxy cred leak via `model_id` carrying a URL** → DISPROVEN: pool models come from `T1Model0N` identifier env vars; base_url/api_key stay in the `_build_transport` closure.
6. **Eager env read at resolve crashing the run before the catch** → DISPROVEN: read is lazy (deferred into the returned factory), executed inside the controller's try.

## Confidence

**Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 6 | Grep: 0 (via Bash) | Glob: 0 | Bash: 8 (grep/git/sed/ls). Total tool calls (14) ≥ checklist items (8).

- No UNCHECKED items.
- No UNVERIFIABLE items.
- contract.py-unchanged verified via `git diff HEAD` (empty) — independent of the review-artifact claim.

## Recommendations

- Green light on the verdict-honesty DOMAIN lens. The guarantee is structural (recompute-over-worker-set), not per-field promise.
- O1/O2/O3 are optional hardening/documentation items; none blocks the gate.

## QA Complete
