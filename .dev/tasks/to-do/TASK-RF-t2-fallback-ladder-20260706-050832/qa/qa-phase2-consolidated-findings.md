# Phase 2 Consolidated QA Findings

**Task:** `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/.dev/tasks/to-do/TASK-RF-t2-fallback-ladder-20260706-050832/TASK-RF-t2-fallback-ladder-20260706-050832.md`
**Date:** 2026-07-06
**Inputs:**
- `qa-phase2-completeness-report.md` — PASS (0 issues)
- `qa-phase2-additive-report.md` — PASS (0 issues)
- `qa-phase2-honesty-report.md` — FAIL (3 IMPORTANT issues)

## Overall Consolidated Verdict: FAIL

FAIL because the verdict-honesty lens reported issues. Completeness and additive-only lenses each reported PASS with zero findings.

## Deduplicated Findings

| ID | Severity | Originating Lens | Affected File(s) | Finding | Required Fix |
|---|---|---|---|---|---|
| P2-HON-001 | IMPORTANT | verdict-honesty | `tests/cli/reflect/test_verdict_mapping.py` and/or `tests/cli/reflect/test_contract_fallback_metadata.py` | No test proves the design §8 degraded-with-fallback-metadata counter-case: a degraded outcome carrying a populated `t2_fallback.terminal_reason` (e.g. `fallback_pool_exhausted`) must still return the real first-match verdict reason `degraded-tier1`. Source is currently correct (`contract.py` ignores `t2_fallback`) but the behavior is not pinned by a test. | Add a test that builds/loads a Tier-1 degraded contract, sets `merge_method: single-reviewer-fallback`, attaches a populated `t2_fallback` block with `terminal_reason: fallback_pool_exhausted`, and asserts `derive_verdict(...).reason == "degraded-tier1"` AND `contract["t2_fallback"]["terminal_reason"] == "fallback_pool_exhausted"`. |
| P2-HON-002 | IMPORTANT | verdict-honesty | `tests/cli/reflect/test_contract_fallback_metadata.py` | `test_populated_fallback_metadata_does_not_change_verdict` compares verdict enum and exit code but not returned reason, leaving a hole where fallback metadata could change reason text while preserving PASS/0. | Extend the test to assert `with_fallback.reason == without_fallback.reason`. |
| P2-HON-003 | IMPORTANT | verdict-honesty | `tests/cli/reflect/test_contract_fallback_metadata.py` | The no-proxy-leak assertion checks env-var-name fragments only, missing lower-case/value leak shapes. | Broaden the forbidden-string list to include `T1ProxyUrl`, `T2ProxyUrl`, `proxy_url`, `proxy_key`, `api_key`, `base_url`, `http://`, `https://`, `:4000/cli`, while preserving the legitimate `proxy_error` status token. Keep the YAML dump as the searched source. |

## Passing Lens Results Preserved

- Completeness lens: all 14 §6 `t2_fallback` fields emitted; `TERMINAL_REASONS` and `TIER2_CERTIFICATION_BASES` match design §6 exactly; both fixtures and both new test assertion families exist.
- Additive-only lens: `t2_fallback` is the last defaulted keyword-only param; no existing returned-dict key changed type/meaning; `contract.py` diff empty; no `_LOAD_BEARING_BOOL_FIELDS` member added; null-fallback verdict-unchanged regression is genuine.

## Fix Routing

Consolidated verdict is FAIL. Step 2.G6 must run exactly one serialized fix agent with `fix_authorization: true` to address P2-HON-001, P2-HON-002, and P2-HON-003. All three are test-hardening additions; `contract.py` must remain unchanged and no `t2_fallback` gating may be introduced.
