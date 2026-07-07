# Phase 4 Consolidated QA Findings

**Task:** TASK-RF-t2-fallback-ladder-20260706-050832
**Date:** 2026-07-07
**Inputs:**
- `qa-phase4-completeness-report.md` — PASS (1 MEDIUM, 2 LOW, 2 INFO)
- `qa-phase4-nofork-report.md` — PASS (3 INFORMATIONAL/MINOR)
- `qa-phase4-actionability-report.md` — PASS (2 MINOR)

## Overall Consolidated Verdict: FAIL

All three lenses returned PASS on their required checks, but non-CRITICAL findings exist (1 MEDIUM + several LOW/MINOR). Per the "any issue of any severity ⇒ FAIL" gate rule, the consolidated verdict is FAIL and Step 4.G6 runs the serialized fix agent. No finding is CRITICAL; the T2 primary path is byte-for-byte intact (2255 swarm tests green) and `swarm/models.py` is unchanged.

## Deduplicated Findings

| ID | Severity | Lens | Location | Finding | Fix decision |
|---|---|---|---|---|---|
| P4-COMP-F1 | MEDIUM | completeness | `commands.py _resolve_run_transport_factory` | The parameterized T1 branch is currently unexercised: no test passes non-default T1 params, and the live T1 fallback path (`resolve_t1_fallback_factory`) uses `read_env_for_pool` + `make_fallback_slot_factory` directly, bypassing this resolver. | FIX: add a unit test asserting `_resolve_run_transport_factory("openai_compat", model_prefix="T1Model0", proxy_url_env="T1ProxyUrl", proxy_key_env="T1ProxyKey", env=…)` reads the T1 pool (proves the Step 4.3 parameterization works). |
| P4-ACT-M1 | MINOR | actionability | `test_openai_compat.py` T1 missing-var | T1 missing-var coverage asymmetric with T2 (only all-missing case). | FIX: add a partial-absence T1 `read_env_for_pool` test (e.g. `T1ProxyKey` absent, others present) asserting `"T1ProxyKey" in .missing`. |
| P4-ACT-M2 | MINOR | actionability | `test_openai_compat.py` wrapper==pool | Equivalence test uses only 2 model slots → can't detect a slot-count divergence alone. | FIX: broaden the delegation test to a dense-skip / near-ceiling shape so `via_wrapper == via_pool` also certifies slot-count equivalence. |
| P4-NOFORK-1 | INFORMATIONAL | no-fork | `commands.py` pool-param defaults | Pool-param defaulting uses truthiness (`max_slots or T2_...`) not `is None`; a future `max_slots=0`/empty prefix would silently fall back to T2. No current caller triggers it. | FIX (cheap hardening): switch the 4 `or`-defaults to `... if x is not None else CONST`. Keeps T2 (None→T2) byte-identical; makes the T1 param path robust for Phase 5. |
| P4-NOFORK-3 | MINOR (out-of-scope file) | no-fork | `src/superclaude/cli/sprint/aienv.py:52` | Docstring cross-reference `Mirrors :meth:`SwarmConfig._collect_t2_models`` points at the method renamed to `_collect_models` in this change. Stale pointer, no runtime effect. | FIX (direct-consequence doc cleanup): update the pointer to `_collect_models`. Authorized for the serialized fix agent as a rename side-effect, not scope creep. |
| P4-COMP-F2 | LOW (cosmetic) | completeness | `openai_compat.py TransportEnvError` message | Message names "T2" even when a T1 pool read fails. `.missing` tuple is accurate (T1 names); message is folded into `fallback_config_missing` telemetry, never operator-surfaced on the fallback path. | ACCEPT: documented. `.missing` (load-bearing) is correct; parameterizing the core exception message is broader churn than the folded-telemetry benefit warrants and risks the widely-used T2 message text. |
| P4-COMP-F3 | LOW (cosmetic) | completeness | `commands.py ModelPoolTooSmallError` message | Message names "T2Model0N" even though T1 pool-too-small is reachable via `make_fallback_slot_factory`. Folded into `fallback_config_missing`; never operator-surfaced. | ACCEPT: documented (same rationale as F2). |
| P4-COMP-F4/F5, P4-NOFORK-2, P4-ACT-obs | INFO | multiple | various | No T1 `missing_t2_env_vars()` sibling (deliberate); gated-arm fixed-tuple correctness (PASS-strengthener); config `_collect_models` no-strip vs transport strip (pre-existing T2-vs-config asymmetry, not introduced). | No action. Pre-existing whitespace asymmetry is out of scope (changing it would alter the primary T2 config path). |

## Fix Routing

Consolidated verdict is FAIL. Step 4.G6 runs exactly ONE serialized fix agent (I20) with `fix_authorization: true` to apply: P4-COMP-F1 (test), P4-ACT-M1 (test), P4-ACT-M2 (test), P4-NOFORK-1 (source hardening, T2 byte-equivalent), P4-NOFORK-3 (aienv docstring). P4-COMP-F2/F3 are ACCEPTED with documentation. INFO items require no action. `swarm/models.py` stays unchanged; the T2 primary path stays byte-equivalent.
