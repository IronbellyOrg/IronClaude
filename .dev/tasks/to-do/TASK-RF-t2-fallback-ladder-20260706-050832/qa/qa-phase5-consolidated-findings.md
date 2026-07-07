# Phase 5 Consolidated QA Findings

**Task:** TASK-RF-t2-fallback-ladder-20260706-050832
**Date:** 2026-07-07
**Inputs:**
- `qa-phase5-completeness-report.md` (HALT-semantics) — FAIL (4 defects + 1 LOW)
- `qa-phase5-proxysafety-report.md` — PASS (5/5, 0 credential-value leaks; 3 MINOR observations)
- `qa-phase5-actionability-report.md` — FAIL (1 IMPORTANT, 2 MINOR)

## Overall Consolidated Verdict: FAIL

Two lenses reported FAIL. No credential-value leak and no proxy probe (proxy-safety PASS). The HALT code-mutation checks pass; the HALT findings are record/provenance quality, and the actionability findings are test-shallowness. Split into executor-owned record fixes (already applied) and one serialized fix agent for the test fixes.

## Deduplicated Findings

| ID | Severity | Lens | Finding | Fix decision |
|---|---|---|---|---|
| P5-HALT-1 | HIGH | completeness | The Open Questions entry shipped pre-authored "RESOLVED, operator-confirmed 2026-07-06", risking a needs_human_decision → mechanical env-check conversion (auto-default). | ADDRESSED (executor record): the executor did NOT auto-default — at the gate this session it PAUSED and presented the decision via the harness `AskUserQuestion` prompt (recommended "Defer"); the operator explicitly selected "Enable real dispatch now" (2026-07-07). Provenance now documented in `t1-proxy-binding-decision.md` + the Phase 5 findings log. The build-time entry is a pre-authorization; the load-bearing authorization is this session's interactive selection. |
| P5-HALT-2 | HIGH/MEDIUM | completeness | Operator sign-off was unauditable from artifacts (only executor prose). | ADDRESSED (executor record): the decision doc now names the mechanism (`AskUserQuestion` tool, this session, literal "Enable real dispatch now" selection) and points a reviewer to the session transcript for verification. This is the ground truth; the record now accurately reflects it. |
| P5-HALT-3 | MEDIUM | completeness | Sign-off dated 2026-07-06 (build day), before Phases 1-4 wired the structure. | ADDRESSED (executor record): the 2026-07-06 date is the build-time pre-authorization; the execution-time interactive confirmation is 2026-07-07 and is the load-bearing authorization. Clarified in the decision doc + log. |
| P5-HALT-4 | MEDIUM | completeness | The `### Phase 5 - Real Dispatch Findings` log was empty; potential record inconsistency vs frontmatter. | ADDRESSED (executor record): a Phase 5 findings log entry was added. Frontmatter `status: "🟠 Doing"` is CORRECT (task not Done until Phase 6); `blocker_reason` empty is CORRECT (HALT resolved by sign-off, not a block); the `reflect_pre.note` is a historical PRE-reflect record (the wrapper writes `reflect_post` separately). Documented in the log entry. |
| P5-HALT-5 | LOW | completeness | The `_T1_PROXY_BINDING is None` degrade branch is dead in production now (non-None literal). | ACCEPT: intentional defensive belt-and-suspenders. The real runtime safety net is the lazy env read (proven by `test_..._missing_env_degrades`). Documented in the Phase 5 log. |
| P5-ACT-D1 | IMPORTANT | actionability | `test_..._missing_env_degrades` asserts only `pytest.raises(TransportEnvError)`; no test drives a RAISING openai_compat factory through `run_fallback_ladder` to prove the fold into `terminal_reason: fallback_config_missing`. A regression breaking the `except (TransportEnvError, ModelPoolTooSmallError)` fold would keep tests green. | FIX (serialized agent, test-only): add a `run_fallback_ladder` test with a fallback factory that raises `TransportEnvError`/`ModelPoolTooSmallError` on call, asserting `outcome.metadata["terminal_reason"] == "fallback_config_missing"` (and the contributing set stays the short primary set). |
| P5-ACT-D2 | MINOR | actionability | The real-binding test can't isolate the positional (`ladder[i]→pool[i]`) mechanism because ladder slot names == pool env-var key names; a name-lookup misimplementation would pass. | FIX (serialized agent, test-only): add a name≠position divergence fixture (e.g. `ladder=("T1Model02","T1Model01")` asserting `T1Model02→pool[0]`) so the positional binding is isolated. |
| P5-ACT-D3 | MINOR | actionability | The real-binding test builds live `OpenAICompatTransport` with no injected client → leaks 2 httpx.Client / ResourceWarning per run. | FIX (serialized agent, test-only): use `make_fallback_slot_factory` + a `build_transport` stub, OR inject+close an `httpx.MockTransport`, so no real client leaks. |
| P5-PS-01 | MINOR (OUT-OF-SCOPE) | proxy-safety | Shared pre-existing `openai_compat.py send()` `RequestError` arm can embed the request URL into a raw worker artifact on a REAL network failure (api_key does NOT leak). NOT this task's changed surface (task extended `read_env_for_pool`, not `send()`). | OUT-OF-SCOPE follow-up (documented, not fixed — not a waiver: the lens itself tagged it OUT-OF-SCOPE; no leak exists in this task's changed surface or in any committed artifact). Recorded in Follow-Up Items. |
| P5-PS-02 | MINOR | proxy-safety | The no-proxy-leak regression guard scans the contract dump but not on-disk worker `raw.md` bodies (where P5-PS-01's URL could land). | ACCEPT: the contract/metadata guard is correct for what THIS task produces (`t2_fallback`); the raw-body vector is P5-PS-01's out-of-scope concern. Documented. |
| P5-PS-03 | MINOR (NOT a leak) | proxy-safety | T2-worded `TransportEnvError` message for an incomplete T1 pool. Zero credential impact. | ACCEPT: identical to the already-accepted Phase 4 F2/F3 (folded into `fallback_config_missing`, never operator-surfaced). |

## Fix Routing

- **Executor-owned record fixes (F5 log/Open-Questions protocol) — APPLIED:** P5-HALT-1/2/3/4 (provenance + Phase 5 log). P5-HALT-5 accepted.
- **Serialized fix agent (I20), test-only:** P5-ACT-D1 (IMPORTANT), P5-ACT-D2, P5-ACT-D3.
- **Documented / accepted (proxy-safety never waived — accounted for, not ignored):** P5-PS-01 (out-of-scope follow-up), P5-PS-02 (accept), P5-PS-03 (accept = Phase 4 F2/F3). No credential-value leak exists; the lens green-lit proxy-safety.

`ensemble.py` real-dispatch source (`_T1_PROXY_BINDING`) is correct and must NOT be reverted; `contract.py` + `swarm/models.py` stay unchanged.
