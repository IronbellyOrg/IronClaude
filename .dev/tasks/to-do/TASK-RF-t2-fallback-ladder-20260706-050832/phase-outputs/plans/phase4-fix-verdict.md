# Phase 4 Fix Verdict — Step 4.G6 (I20, serialized fix agent)

**Task:** TASK-RF-t2-fallback-ladder-20260706-050832
**Date:** 2026-07-07
**Agent:** rf-qa (serialized fix agent, `fix_authorization: true`)
**Consolidated verdict fixed:** FAIL → all authorized fixes applied, verification green.

## Overall Result: PASS

All five authorized fixes applied correctly. T2 primary path byte-equivalent
(full swarm suite green: 2255 baseline + 4 new tests = 2259 passed, 26 skipped).
`models.py` and `contract.py` diffs confirmed empty. Two ACCEPTED findings
recorded (no code change). No new issues introduced.

## Fixes Applied

| ID | Type | File | What changed |
|---|---|---|---|
| P4-NOFORK-1 | source hardening (T2 byte-equiv) | `src/superclaude/cli/swarm/commands.py` | In `_resolve_run_transport_factory` openai_compat branch, changed all FOUR `read_env_for_pool` defaults from truthiness (`X or CONST`) to `X if X is not None else CONST` form (`model_prefix`, `max_slots`, `proxy_url_env`, `proxy_key_env`). Byte-equivalent for every current caller (all pass `None` → constant); removes a future `max_slots=0` / empty-prefix silent-T2-fallback footgun. Verified NO other truthiness default exists in this function (the `models ... or "stub-model-00"` default lives in the separate `_resolve_run_transport`, not the factory). |
| P4-NOFORK-3 | docstring-only | `src/superclaude/cli/sprint/aienv.py` (line 52) | Updated stale cross-reference `Mirrors :meth:`SwarmConfig._collect_t2_models`` → `_collect_models` (method renamed in this Phase-4 change; confirmed current name at `config.py:196`, old name only survives in that method's own docstring as "Generalizes the former `_collect_t2_models`"). No code/behavior change. Nothing else in aienv.py touched. |
| P4-COMP-F1 | new tests | `tests/swarm/test_openai_compat.py` | Added `test_resolve_factory_t1_branch_binds_per_slot_models` (imports `_resolve_run_transport_factory` from `superclaude.cli.swarm.commands`; T1 env dict; `factory(0).model=="m-a"`, `factory(1).model=="m-b"` proving Step 4.3 parameterized T1 pass-through binds per-slot models) and `test_resolve_factory_t1_pool_too_small_raises` (single-model T1 pool + `workers_requested=2` raises `ModelPoolTooSmallError`, imported from same module). Network-free: env dicts drive `read_env_for_pool`; `OpenAICompatTransport` constructed but never `.send()`-called. |
| P4-ACT-M1 | new test | `tests/swarm/test_openai_compat.py` | Added `test_read_env_for_pool_partial_absence_t1_missing_key`: T1 env with `T1ProxyUrl`+`T1Model01` present, `T1ProxyKey` absent → `TransportEnvError` with `"T1ProxyKey" in .missing` and `"T1ProxyUrl" not in .missing`. Restores T1/T2 missing-var coverage symmetry. |
| P4-ACT-M2 | new test | `tests/swarm/test_openai_compat.py` | Added `test_read_env_wrapper_delegates_with_dense_skip_and_slot_count` (added as a SECOND delegation test, preserving the existing 2-model `test_read_env_wrapper_delegates_to_pool_reader` regression): env has empty interior slot `T2Model03=""` (dense-skip) + later slot `T2Model04="m-d"`; asserts `read_env(env) == read_env_for_pool(...)` AND `models == ("m-alpha","m-beta","m-d")` / `len==3` so wrapper==pool now certifies slot-count + dense-skip equivalence, not just the happy path. |

## ACCEPTED — No Code Change (recorded per task instruction)

| ID | Location | Acceptance rationale |
|---|---|---|
| P4-COMP-F2 | `openai_compat.py TransportEnvError` message | Message names "T2" even on a T1 pool-read failure, but `.missing` tuple (the load-bearing structured field) is accurate (carries the real T1 names), and the message is folded into `terminal_reason: fallback_config_missing` — never operator-surfaced on the fallback path. Parameterizing the core exception message is broader churn than the folded-telemetry benefit warrants and risks the widely-asserted T2 message text. Left as-is. |
| P4-COMP-F3 | `commands.py ModelPoolTooSmallError` message | Same rationale: names "T2Model0N" even though T1 pool-too-small is reachable; structured `pool_size`/`workers_requested` guard is accurate; message folded into `fallback_config_missing`, never operator-surfaced. Left as-is. |

INFO items (P4-COMP-F4/F5, P4-NOFORK-2, P4-ACT-obs) require no action — no change.

## Commands Run (all UV)

| Command | Result |
|---|---|
| `uv run pytest tests/swarm/test_config.py tests/swarm/test_openai_compat.py -q` | 50 passed |
| `uv run pytest tests/swarm/ -q` | **2259 passed, 26 skipped** (baseline 2255+4 new; T2 byte-equivalent, no regressions) |
| `uv run pytest tests/cli/reflect/test_ensemble_fallback_stub.py tests/cli/reflect/test_ensemble_fallback_engage.py -q` | 5 passed |
| `uv run ruff check <3 changed files>` | All checks passed |
| `uv run ruff format --check <3 changed files>` | 3 files already formatted (no reformat needed) |
| `git diff --stat -- src/superclaude/cli/swarm/models.py` | empty ✓ |
| `git diff --stat -- src/superclaude/cli/reflect/contract.py` | empty ✓ |

## Hard-Constraint Verification

- T2 primary path byte-equivalent: PASS — full swarm suite green at 2259 (= 2255 baseline + 4 net-new tests); the 4 default changes are `None`→constant identical for every current caller.
- `swarm/models.py` unmodified: PASS (empty diff).
- `contract.py` unmodified: PASS (empty diff).
- UV-only, no `.claude/` edits, nothing staged/committed: PASS.
- Files modified confined to the 3 authorized paths (`commands.py`, `sprint/aienv.py`, `tests/swarm/test_openai_compat.py`): PASS.

## Adversarial Self-Audit

- Did I break the T2 primary path? No — the hardening is provably `None`→constant equivalent, and the full 2255-test baseline stayed green (only +4 from my own additions).
- Did I break a message-asserting test? No — I did NOT touch the `TransportEnvError`/`ModelPoolTooSmallError` message strings (F2/F3 accepted); no test asserting those messages changed. The existing 2-model `test_read_env_wrapper_delegates_to_pool_reader` was preserved intact (M2 added as a second test).
- Did I churn the wrong file? No — `models.py` and `contract.py` diffs empty; only the 3 authorized files changed; ruff clean with no reformat.
