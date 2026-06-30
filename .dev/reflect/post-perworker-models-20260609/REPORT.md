# Reflect Report — Per-Worker Model Differentiation (UC-2, deep)

- **mode:** post · **tier_reached:** 2 (heterogeneous ensemble: sonnet + haiku reviewers + Tier-1 grounding)
- **driving requirement:** "Wire per-worker model differentiation so a single swarm job uses all configured `.aienv` models heterogeneously (one `OpenAICompatTransport` per `T2Model0N` slot), instead of binding only `T2Model01` across all workers."
- **diff:** `dispatch.py`, `commands.py`, `tests/swarm/test_commands_run.py` (working tree, uncommitted)
- **verdict:** requirement **SATISFIED** for per-slot differentiation (live-proven: one 4-worker job used 4 distinct models). One **HIGH** defect introduced on the `--resume` path + 3 minor drifts. No regression (2206 stub tests pass).

## Deviation register

### D1 — Regression/Drift (HIGH, reachable): `--resume` reassigns models per slot
`commands.py:1857-1886` builds `resume_transport_factory` and calls `dispatch_wave1(..., transport_for_slot=resume_transport_factory)` with `workers_requested=len(remaining_indices)`. Dispatch passes synthetic slot indices `0..K-1` to the factory, which maps `pool[new_pos % len(pool)]` (`commands.py:631`). `worker.index` is reindexed back to the original slot only *after* the model was chosen (`commands.py:1875-1886`). **Consequence:** a worker that originally ran on `pool[3]` (deepseek) and failed is retried on `pool[0]` (kimi) — the per-slot model identity is not preserved across resume. Under the old single-model behavior all slots shared `T2Model01`, so resume was model-stable; this change introduced the divergence.
**Fix applied:** wrap the resume factory so synthetic position `j` resolves the ORIGINAL slot's model: `transport_for_slot=lambda new_pos: resume_transport_factory(remaining_indices[new_pos])`.

### D2 — Drift (MED, latent, NOT reachable under `.aienv`): env-pool size unguarded
The factory pool comes from `read_env().models` (`commands.py:625`, `openai_compat.py:181-201`) and maps `pool[i % len(pool)]`. INV-005 (`preflight.py:1808-1811`, `check_pool_size`) validates `workers.count` against `spec.workers.models` (lens placeholders), **not** the env pool the factory actually uses. If the env pool is smaller than the worker count, slots silently wrap and reuse models with no warning. Not reachable under the normal `.aienv` contract (4 models, 3-/4-worker lenses). **Recommended follow-up (not fixed):** before dispatch, assert/warn `len(read_env().models) >= workers_requested` for `openai_compat`.

### D3 — Drift (LOW): stale docstring contradicts new behavior
`commands.py:518-523` (`_resolve_run_transport` docstring) still says per-slot model differentiation is "intentionally out of scope ... tracked separately." Now false. **Fix applied:** docstring updated to point at `_resolve_run_transport_factory`.

### D4 — Drift (LOW): test only inspects `factory(0)`
`tests/swarm/test_commands_run.py` asserts `factory(0) is StubTransport` but not cross-slot behavior. Legitimate update (param changed `transport`→`transport_for_slot`) but marginally weaker than the original F-P3-1 assertion. **Fix applied:** assert the factory returns a StubTransport for multiple slots.

### D5 — Necessary (LOW, latent): synthetic results lack `model_id`
`dispatch.py:171-186` synthesizes `WorkerResult` on raised `TimeoutError`/`Exception` without `model_id`; the new `worker_done` log emits `result.model_id` (empty there). Not reachable with bundled transports — `openai_compat` routes timeout/network/non-200/parse through `_build_result` which stamps `model_id` (`openai_compat.py:329-401`); `stub` always returns success. Left as-is; documented.

### D6 — OK (INFO): cache check-then-set race is benign
`commands.py:629-641` caches one transport per model via a plain dict mutated under `ParallelExecutor`. Under INV-005 (count ≤ pool ⇒ distinct model per slot) no two slots share a key concurrently, so no contention; worst case (wraparound, see D2) is a redundant transport, not corruption.

## Evidence-validator
All cited `file:line` re-grounded against current working tree during Tier-1 reads and reviewer passes. Zero citations dropped (flagged for spot-check per protocol). Confirmed live: 4-worker `edge-case-hunt` run emitted 4 distinct `model_id`s = the 4 `.aienv` models.

## Disposition
Fix D1 (HIGH defect), D3, D4 now; document D2 as follow-up; D5/D6 informational. Re-run stub suite after fixes.

## Post-fix verification (applied)
- D1 (HIGH resume defect): FIXED — resume now maps synthetic pos → original slot's model (`commands.py` `_resume_slot_transport`).
- D3 (docstring), D4 (test strengthened to multi-slot): FIXED.
- D2 (env-pool guard): documented follow-up, not reachable under `.aienv`.
- Stub regression suite: 2205 passed + 12 skipped (1 pre-existing flaky SIGKILL test passes in isolation; F821 `Logger` pre-exists on master — both unrelated).
- Real-proxy confirmation (3 tests, live, 162.87s): 4-worker job uses all 4 `.aienv` models; 3-worker uses 3; 2 reliable models both http=200. Per-worker differentiation proven end-to-end.
