# QA Report — Phase Gate 4 Determinism Lens (bare-review parity gate)

**Topic:** sc-bare-review M8/M9 migration — rebuilt parity gate hermeticity + determinism
**Date:** 2026-06-16
**Phase:** doc-qualitative (adapted: test-gate determinism/hermeticity audit)
**Fix cycle:** N/A (fix_authorization: FALSE — report only)
**Stance:** Adversarial — assumed the gate was flaky/non-hermetic; hunted for the nondeterminism source.

---

## Overall Verdict: PASS

The rebuilt gate is hermetic (stub transport only, no network/socket/token), the two
wall-clock-dependent body fields (`generated`, `elapsed_ms`) are both pinned to constants on the
CLI path, the byte comparison is order-robust (sorted multiset), the timeout slot calls `send`
exactly once (no retry-overflow because `on_timeout=False`), and three consecutive runs produced
byte-identical results (16 passed each, 0 flakes).

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Hermetic: `--transport stub` only, no `openai_compat`/network/tokens | PASS | Test invokes CLI with `--transport stub` (parity.py:268-270). Patches `swarm_commands._resolve_run_transport` to return scenario transport ONLY for `kind=="stub"`, delegating other kinds untouched (parity.py:242-247). `openai_compat` branch unreachable — never passed; even if reached, `read_env` raises before any socket (commands.py:656-665). `test_stub_transport.py:138-151` actively guards `socket.socket` and asserts no socket call. StubTransport imports only `hashlib`/`threading` (stub.py:57-59). |
| 2 | Wall-clock `generated` frontmatter field PINNED | PASS | Test monkeypatches `superclaude.cli.swarm.recipes.bare_review_v1.iso_now` → `FIXED_GENERATED="2026-06-01T17:59:55Z"` (parity.py:250-253). Recipe reads `generated = args.get("generated") or iso_now()` (bare_review_v1.py:260); inline path does NOT thread `generated` into recipe_args (commands.py:1833-1838 only sets target/target_checksum), so the patched `iso_now` is the source. All 12 golden bodies carry the pinned value (grep confirmed). |
| 2b | SECOND wall-clock field `elapsed_ms` — flake risk PROBED | PASS | `elapsed_ms` is rendered into every body (bare_review_v1.py:305) and `_send_once` measures real wall-clock `int((monotonic()-start)*1000)` (dispatch.py:188-191), backfilling the stub's 0. **This was my prime flake hypothesis** (a slow host rounding to 1ms). Disproven: the recipe reads `elapsed_ms = args.get("elapsed_ms", 0)` (bare_review_v1.py:257) from the SHARED `recipe_args` dict, which `normalize_wave2` forwards verbatim to every worker (normalize.py:548-554) WITHOUT injecting the per-worker measured elapsed. The key is absent → default `0` always. Same mechanism pins `reviewer_model_id`/`model_label` to `""`. Golden bodies confirm `elapsed_ms: 0` universally. The measured wall-clock never reaches the byte-compared body. |
| 3 | Byte comparison order-robust (sorted multiset, not per-index) | PASS | StubTransport serves `fixtures[counter % len]` under a lock in call order; slot↔fixture binding NOT guaranteed under concurrent dispatch (stub.py:161-177, docstring lines 28-31). Dispatch fans out via `ParallelExecutor` (dispatch.py:424,463-474), so which thread gets which fixture is scheduling-dependent. Gate compares `sorted(cli_bodies) == sorted(golden)` (parity.py:329) — order-independent. No per-index body comparison exists. Per-slot CONTRACT assertions use sorted status multisets (parity.py:394) and count/bool fields, never index-bound bodies. |
| 4 | `partial-with-timeout` retry-overflow safe | PASS | `_ScriptedTransport.send` is lock-guarded with a counter; plan exhaustion returns `("timeout", None)` raising TimeoutError — never a spurious success body (parity.py:130-140). More importantly the overflow CANNOT occur on this path: default `RetryPolicy.on_timeout=False` (models.py:152), and `retry_policy` returns `first` immediately for a timeout (`should_retry` stays False, dispatch.py:258-262). The CLI uses the default WorkerSpec (`inline_job.workers`, commands.py:1802). So the timeout slot calls `send` exactly ONCE. The guard is correct defensive belt-and-suspenders, not load-bearing. Timeout slot writes no `.final.md` (normalize.py:424-435 short-circuits timeout/proxy_error) → golden has 2 bodies, M=2, status=partial (verified). |
| 5 | Empirical determinism — 3 identical runs | PASS | See 3-Run Evidence below. 16 passed, 0 flakes, each run. |
| 6 | Contract assertions touch no unpinned wall-clock field | PASS | Gate asserts only `status`, `output_files[].status`, `workers_succeeded`, `workers_requested`, `caller_metadata.suspect`, `recommended_next_command`, `len(output_files)` (parity.py:363-478). None are timestamps. The contract is NOT byte-compared whole; `return-contract.yaml` golden carries `elapsed_ms: 0` (pinned via same mechanism) and no compared timestamp field. |

## Summary
- Checks passed: 7 / 7 (6 numbered + the elapsed_ms sub-probe)
- Checks failed: 0
- Critical issues: 0
- Confidence: Verified 7/7 | Unverifiable 0 | Unchecked 0 | Confidence: 100.0%
- Tool engagement: Read 6 | Grep 4 | Glob 0 | Bash 5 (each call mapped to a specific claim)

## Issues Found
None.

## 3-Run Evidence (raw, `uv run pytest tests/swarm/test_bare_review_parity.py -q`)

```
=== RUN 1 ===  16 passed in 0.36s
=== RUN 2 ===  16 passed in 0.35s
=== RUN 3 ===  16 passed in 0.34s
```

Full-suite cross-check (parity + stub_transport, `-v`): 28 passed in 0.37s, 0 SKIPPED / XFAIL / ERROR.

## Adversarial Notes (where I looked hardest for a flake and found none)
- **`elapsed_ms` real-clock leak (prime suspect):** A real `time.monotonic()` delta is measured per
  attempt and IS rendered into the byte-compared body — but it is severed from the body by the
  shared-`recipe_args` forwarding (no per-worker injection on the inline CLI path). If a future change
  threaded per-worker `elapsed_ms` into `recipe_args`, the body byte-match WOULD begin to flake on
  loaded hosts. **Recommend (non-blocking):** a one-line comment in the gate or recipe-args assembly
  noting that per-worker `elapsed_ms` MUST NOT be threaded into the shared recipe_args or the
  frozen-golden byte-match becomes wall-clock-dependent. Not a defect in the current code — the
  current path is deterministic.
- **Injection seam correctness:** dispatch is called with `transport_for_slot=` (the factory), not
  `transport=`. The factory's stub branch calls module-global `_resolve_run_transport("stub", ...)`
  (commands.py:654), which IS the patched name — so the scenario transport genuinely flows to every
  slot. Had the factory inlined StubTransport construction, the patch would have been a no-op and the
  gate would silently test default-hash bodies. It does not; the seam holds.
- **Concurrency × multiset:** the sorted-multiset comparison is the right call given the
  lock-order/scheduling ambiguity of `fixtures[counter % len]`. No per-index assumption anywhere.

## QA Complete
