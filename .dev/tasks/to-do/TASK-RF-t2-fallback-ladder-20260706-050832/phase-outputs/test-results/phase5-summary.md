# Phase 5 Test Summary

## Overall Result

PASSED

## Counts

| Total | Passed | Failed | Skipped/Deselected |
|---:|---:|---:|---:|
| 54 | 54 | 0 | 187 deselected |

## Scope

`uv run pytest tests/cli/reflect/ -k "fallback or resolve_t1 or ensemble_fallback" -v` — the reflect fallback / resolver / ensemble-fallback surface with real T1-proxy dispatch ENABLED (`_T1_PROXY_BINDING` set).

## Key Phase 5 tests (network-free, real binding)

| Test | Verdict |
|---|---|
| `test_resolve_t1_fallback_factory_stub_arm_returns_live_transport` | PASS |
| `test_resolve_t1_fallback_factory_openai_compat_missing_env_degrades` | PASS (empty T1 env → `TransportEnvError` on factory call → `fallback_config_missing`) |
| `test_resolve_t1_fallback_factory_openai_compat_real_binding_is_slot_name_keyed` | PASS (F1: `T1Model01→pool[0]` `qwen-t1`, `T1Model02→pool[1]` `deepseek-t1`, injected env only) |
| `test_incident_replay_certifies_tier2_with_fallback` | PASS |
| `test_counter_case_both_fallbacks_fail_stays_degraded_tier1` | PASS |
| ensemble gate ENGAGE/SKIP (`test_ensemble_fallback_engage.py`) | PASS |

## Scoped Lint

- `uv run ruff check` on `ensemble.py`, `test_ensemble_fallback_stub.py`, `test_cli_smoke.py`: All checks passed.
- `uv run ruff format --check`: 3 files already formatted.

## Regression note (Phase 3 flag fallout, resolved / to-be-resolved)

Running the FULL reflect suite surfaced 3 failures that were consequences of the Step 3.3 `--tier2-fallback` flag addition (not the Phase 5 binding), because the narrower Phase 3 test scope did not exercise them:
- `test_cli_smoke.py::test_tmux_inner_command_forwards_isolate_reviewers` / `..._no_isolate_reviewers` — the `SimpleNamespace` config mocks lacked `tier2_fallback_enabled`, which `_build_inner_command` now reads. FIXED this session: added the field to both mocks + a light assertion validating the new tmux `--tier2-fallback`/`--no-tier2-fallback` forwarding.
- `test_docs_cli_parity.py::test_documented_flags_match_cli_flags` — the real `--tier2-fallback`/`--no-tier2-fallback` flag is not yet in `docs/guides/reflect-cli-tools-guide.md`. This is Step 6.1's designated deliverable (document the flag); it will turn green once the guide's `### Key options` section documents the flag. Currently the only remaining red test; 239/240 reflect tests pass.

## Command

`uv run pytest tests/cli/reflect/ -k "fallback or resolve_t1 or ensemble_fallback" -v 2>&1`
