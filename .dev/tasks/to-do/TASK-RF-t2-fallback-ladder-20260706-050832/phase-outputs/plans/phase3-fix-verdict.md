# Phase 3 Fix Verdict — Step 3.G6 (I20 serialized fix agent)

**Task:** TASK-RF-t2-fallback-ladder-20260706-050832
**Date:** 2026-07-06
**Fix authorization:** true | **Scope:** test-only, `tests/cli/reflect/` only
**Final result:** PASS — all 6 actionability findings remediated, 25/25 tests green, zero source changes.

## What changed

### NEW `tests/cli/reflect/test_ensemble_fallback_engage.py` (P3-ACT-001 + P3-ACT-004 + P3-ACT-005 stub arm)
Drives the REAL `run_tier2_ensemble` (which owns the `tier2_fallback_enabled` gate, wires real `stamp=_stamp_worker_paths`, and resolves real `resolve_t1_fallback_factory("stub")`), network-free. Copies `_FailingTransport` + `_const_score`/`AdversarialResult` from `test_ensemble_stub_integration.py`.
- `_factory`: slot 0 → `StubTransport(model_id=stub_model_id(0))` (real vendor-distinct success `qwen-stub-00`); slots 1/2 → `_FailingTransport` (proxy_error, fallback-eligible).
- **Test A `test_gate_on_engages_ladder_and_certifies_tier2`**: `tier2_fallback_enabled=True`, `output_dir=tmp_path/"on"`. Asserts `t2_fallback is not None`, `engaged is True`, `certified_with_fallback is True`, `tier_reached == 2`, `reviewer_count == 2`, verdict PASS/exit 0.
- **Test B `test_gate_off_skips_ladder_and_degrades_tier1`**: `tier2_fallback_enabled=False`, `output_dir=tmp_path/"off"`. Asserts `t2_fallback` absent/None, `tier_reached == 1`, `reviewer_count == 1`, verdict DEGRADED/`degraded-tier1`/exit 11.
- Contract isolation via separate `tmp_path/"on"` vs `tmp_path/"off"` output dirs.

### EDIT `tests/cli/reflect/test_ensemble_fallback_stub.py`
- **P3-ACT-003**: `_incident_primaries` realigned to §8 — survivor `deepseek-primary` at index 1; failures at index 0 (`proxy_error`) and index 2 (`parse_error`) → ids `primary:00` / `primary:02`.
- **P3-ACT-002**: exact `primary_failures_preserved == ["primary:00", "primary:02"]`.
- **P3-ACT-006**: added `engaged is True`, `fallback_attempt_count == 1`, `exhausted is False` to the incident test.
- **P3-ACT-005 (remainder)**: added `test_resolve_t1_fallback_factory_openai_compat_arm_is_env_gated` — openai_compat arm raises `TransportEnvError` (`_T1_PROXY_BINDING is None` safe-degrade); stub arm returns a transport-like object without raising.

## Commands run
| Command | Result |
|---|---|
| `uv run pytest test_ensemble_fallback_stub.py test_ensemble_fallback_engage.py test_fallback_config.py -q` | 10 passed |
| `uv run pytest test_ensemble_stub_integration.py -q` | 15 passed (disabled/primary path byte-equivalent) |
| combined re-run after ruff reformat (25 items) | 25 passed |
| `uv run ruff check <2 changed files>` | All checks passed |
| `uv run ruff format --check` | flagged stub file → formatted that file only |
| `git diff --stat -- src/` | only pre-existing Phase 3 source edits (NOT touched by the fix agent) |

## Constraint compliance
- No `src/` modified; `contract.py` byte-unchanged; disabled path proven byte-equivalent (15/15). UV-only. `.claude/` untouched. Nothing staged/committed.

## Findings status
P3-ACT-001 fixed · P3-ACT-002 fixed · P3-ACT-003 fixed · P3-ACT-004 fixed (real stamp wired via `run_tier2_ensemble`) · P3-ACT-005 fixed (stub arm via engage test + gated openai_compat unit) · P3-ACT-006 fixed. Completeness/seam MINOR/INFO items required no fix (carried forward as notes).
