# Synthesis 07 — §14 Observability & Monitoring + §15 Testing Strategy

> **TDD sections:** 14 (Observability & Monitoring), 15 (Testing Strategy)
> **Feature:** FR-RH2 — Drive sc:reflect Tier-2 reviewer ensemble through the swarm CLI (headless ensemble fix)
> **Sources:** research `00-prd-extraction.md`, `04-swarm-transport-pool.md`, `05-swarm-reduce-merge-contract.md`, `07-nfr7-guard-test-harness.md`; verified against `src/superclaude/cli/reflect/contract.py` (`_degraded_reason`, L249-304) and `src/superclaude/cli/swarm/{reduce.py,models.py,transports/stub.py}`.
> **Template alignment:** §14 = Logging / Metrics / Tracing / Alerts / Dashboards; §15 = Test Pyramid + Unit / Integration / Backward-compat test-case tables.
> **No fabrication:** every verdict/exit-code, reason slug, and field name is traced to spec text or read code. `[UNVERIFIED]` marks `ensemble.py`-internal names not yet in code (module does not exist yet).

---

## 14. Observability & Monitoring

This feature is a headless CLI pipeline, not a long-running service, so observability is **artifact-and-exit-code-based**, not metric-server-based. A Tier-2 run is observed in three ways: (1) a terminal `done.json` sentinel that a poller can read to learn the outcome without parsing the rich contract; (2) the process exit code and the reflect `return-contract.yaml` verdict it derives from; (3) optional live surfaces — swarm `--detached`/tmux background run and the swarm `--tui` dashboard — for the inner `t2-swarm/` subrun (NFR-RH2.7).

### 14.1 The `done.json` terminal-status sentinel (pollable)

Per NFR-RH2.7 the headless Tier-2 subrun MUST be pollable. The swarm reduce layer already emits a terminal-status sentinel; reflect's `t2-swarm/` subrun inherits it. `[CODE-VERIFIED: reduce.py emit_done_sentinel L402-459, models.py DoneSentinel L1423/L1479-1481]`

| Property | Value | Source |
|----------|-------|--------|
| Filename | `done.json` (`DONE_SENTINEL_FILENAME`) | reduce.py L140 |
| Location | `<contract_path>.parent/done.json` — co-located with `return-contract.yaml` | reduce.py L456 |
| Write semantics | atomic: tmp + fsync + `os.replace`; `atomic_write: true` always-on | reduce.py `_atomic_write_bytes`; DoneSentinel L1479 |
| Serialization | `json.dumps(to_dict(sentinel), sort_keys=True, indent=2) + "\n"` | reduce.py L457 |
| `terminal_status` | `ResultStatus` Literal — `success` / `partial` / `failed` (enum-enforced in `__post_init__`) | models.py L1480, L1483-1489 |
| `contract_path` | absolute path to `return-contract.yaml` (lets a poller locate the rich record) | models.py L1481 |

Sentinel shape (sorted keys):

```json
{
  "atomic_write": true,
  "contract_path": "<abs path to return-contract.yaml>",
  "terminal_status": "success"
}
```

> **Note:** The kill path (`commands._emit_killed_done_sentinel`) bypasses the dataclass because `"killed"` is deliberately NOT in `ResultStatus`; only the IMM-5 reduce path (`success`/`partial`/`failed`) goes through the guarded dataclass. `[CODE-VERIFIED: reduce.py L429-432]` A poller therefore distinguishes a clean terminal run (sentinel with one of the three enum values, written atomically) from a killed run (out-of-enum `killed`).

**Polling contract:** a watcher waits for `done.json` to appear (atomic `os.replace` means it is never observed half-written), reads `terminal_status` for the swarm subrun verdict, then opens `contract_path` for the full record. This is the inner-loop observability primitive for NFR-RH2.7; the reflect verdict (below) is the outer-loop one.

### 14.2 `--detached` / tmux and `--tui` (NFR-RH2.7 live surfaces)

The spec routes the Tier-2 ensemble through the swarm dispatch library in-process by default; the `superclaude swarm run --lens reflect-review` **CLI** is the optional `--detached` observability variant (PRD §1.2 in-scope; NFR-RH2.7). The available live surfaces for the `t2-swarm/` subrun:

| Surface | What it gives the operator | Trigger | Caveat |
|---------|----------------------------|---------|--------|
| `--detached` / tmux | Headless background run; outcome observed later via `done.json` + `return-contract.yaml` | swarm `--detached`/tmux on the t2-swarm subrun (NFR-RH2.7) | reflect's own runner must NOT add a raw `subprocess.run`/`Popen` for this — it goes through the swarm CLI surface / `ClaudeProcess` (FR-RH2.8 AC-3) |
| `done.json` sentinel | Terminal status without parsing YAML (§14.1) | always emitted by reduce | `killed` bypasses the dataclass (out-of-enum) |
| `--tui` dashboard | Live per-worker progress for the subrun | swarm `--tui` available for the t2-swarm subrun (NFR-RH2.7) | `--tui` single-writer gate is a known swarm fragility (memory `reference_swarm_tui_fr1_parallelexecutor_print.md`); not load-bearing for reflect verdict correctness |

> **CRITICAL (FR-RH2.8 / NFR-RH2.2):** No raw `subprocess.run`/`Popen` may be added to the reflect package for the detached launch. The no-nesting guard (`test_no_nesting_guard.py`, extended to `ensemble.py` per FR-RH2.8) enforces this: the swarm fan-out goes through the swarm dispatch library / `ClaudeProcess`, never a hand-rolled `Popen`. `[CODE-VERIFIED: 07 Part 2; PRD FR-RH2.8 AC-3]`

### 14.3 Verdict / exit-code surface table (what each terminal state surfaces)

The reflect verdict→exit-code map is **unchanged** by FR-RH2 (FR-RH2.7 AC-1, NFR-RH2.6). The (M,N) divergence guard table (spec §5.3) routes each ensemble outcome into one of these four states. `[CODE-VERIFIED: contract.py _degraded_reason L249-304; PRD §5, §5.4]`

| Terminal state | Verdict | Exit code | (M,N) condition that routes here | reason-slug surfaced |
|----------------|---------|-----------|----------------------------------|----------------------|
| Faithful Tier-2 | `pass` | **0** | `M>=2 AND >=2 distinct succeeded model classes` | `pass` |
| One-reviewer / N→M collapse to 1 | `degraded` | **11** | `M==1` (`--reviewers 1`, OR N>1 with N−1 failures) | `single-reviewer-fallback` (and/or `degraded-tier1` when `tier_reached==1`) |
| Survivors collapsed onto one class | `degraded` | **11** | `M>=2 but <2 distinct model classes` | `degraded-model-diversity` |
| Empty ensemble | `blocked` | **2** | `M==0` (all workers failed / no usable artifacts) | `ensemble-empty` |
| (Pre-existing) audit-found problem / tier mismatch | `halted` | **10** | status success but tier mismatch / audit problem | `tier-mismatch` (pre-existing path, unchanged) |

> **`derive_verdict` ordering** (spec §5.4, FR-RH2.9 dependency): `blocked → degraded → halted → pass`. `blocked` (M==0) is ordered **ahead** of `degraded`, so an empty ensemble is never silently degraded. `[PRD §5.4]`

### 14.4 Degraded reason slugs (grounded in `_degraded_reason`)

The three FR-RH2-relevant degraded slugs map onto **existing** triggers in `contract._degraded_reason` (first-match ordering); FR-RH2 adds no new verdict branch, it feeds the existing triggers from a *computed* contract. `[CODE-VERIFIED: contract.py L249-304]`

| Reason slug | Trigger condition (verbatim from `_degraded_reason`) | contract.py line | Spec (M,N) row |
|-------------|------------------------------------------------------|------------------|----------------|
| `single-reviewer-fallback` | `contract.get("merge_method") == "single-reviewer-fallback"` (Trigger 10) | L280-281 | M==1 |
| `degraded-model-diversity` | `mcd = contract.get("t2_model_class_diversity"); mcd is not None and mcd != "full"` (Trigger 7) | L267-269 | M>=2, <2 distinct classes |
| `degraded-tier1` | `expected_tier >= 2 and tier_reached == 1` (Trigger 6) | L263-264 | M==1 (when reduce sets `tier_reached:1`) |

> **`ensemble-empty` (M==0 → blocked/exit2)** is the spec's reason-slug for the empty-ensemble path (PRD §5). It routes through the **blocked** branch (ordered ahead of degraded), not through `_degraded_reason`. The slug name is spec-supplied; the mechanism (M==0 → blocked → exit 2) is the load-bearing contract. `[PRD §5, §5.4]` `[UNVERIFIED: exact "ensemble-empty" string is spec vocabulary; the blocked path is CODE-VERIFIED as a pre-existing verdict.]`

### 14.5 Logging — per-reviewer ensemble facts

The ensemble must log the raw execution facts from which the verdict is computed, so a degraded/blocked outcome is diagnosable from the artifact set (not just the exit code). These derive from the swarm `WorkerResult` records (DM-013) and the reduce M/N computation. `[CODE-VERIFIED: reduce.py L647-658; models.py WorkerResult L1117-1128]`

| Logged fact | Field / source | Log level | Why |
|-------------|----------------|-----------|-----|
| M / N (succeeded / requested) | `workers_succeeded` (M, reduce.py L648) / `workers_requested` (N, L650-653) | INFO | The N→M divergence is the verdict driver (FR-RH2.9); M/N must be visible |
| Per-reviewer `model_id` | `WorkerResult.model_id` (models.py L1122) | INFO | Diversity is computed over **distinct `model_id`s of the M succeeded workers** (FR-RH2.4 AC-4) |
| Per-reviewer `status` | `WorkerResult.status` ∈ `success`/`timeout`/`parse_error`/`proxy_error` (L1130-1136) | INFO (success) / WARN (non-success) | Only `success` counts toward M (spec §5.1); non-success drops the slot |
| Per-reviewer `elapsed_ms` | `WorkerResult.elapsed_ms` (L1128; printed in merge provenance header) | INFO | Latency + the `## From {model_label} ({elapsed_ms}ms)` provenance header |
| Computed diversity | `t2_model_class_diversity` (full vs not) on the reflect contract | INFO | The PASS-vs-degraded discriminator (Trigger 7) |
| `merge_method` | `single-reviewer-fallback` vs adversarial | INFO | The M==1 discriminator (Trigger 10) |

> **Diversity is measured over M, not N** (FR-RH2.4 AC-4, FR-RH2.9): two *surviving* workers that resolved to the same model class do NOT count as `full`. The log must therefore carry the distinct-`model_id` count of the **succeeded** workers, not the requested slot count. `[PRD FR-RH2.4, FR-RH2.9]`

---

## 15. Testing Strategy

The load-bearing risk this feature must retire is the **conftest mock gap**: today `make_claude_process_stub` (`tests/cli/reflect/conftest.py` L98-138) makes the stubbed `ClaudeProcess.wait()` copy a hand-authored `fixtures/*.yaml` into `return-contract.yaml`, so `pass.yaml` L4 `tier_reached: 2` is a **typed constant**, never a computed result. "Tier 2 works" was a fixture asserted against itself — no dispatch, no reduce, no reviewers ever ran. `[CODE-VERIFIED: 07 Part 3]` FR-RH2.5's integration proof is therefore the load-bearing test: it must run the **real** `dispatch_wave1 → reduce_wave3 → derive_verdict` flow under an injected `StubTransport`, NOT the canned-fixture path.

### 15.1 Test Pyramid

| Level | Coverage Target | Tools | What it proves here | FR/NFR |
|-------|-----------------|-------|---------------------|--------|
| Unit | Lens + ensemble binding + guard logic | `uv run pytest`, `pytest.mark.parametrize` | `reflect-review` lens registers + validates; slot→`T2Model0N` binding + `ModelPoolTooSmallError`; diversity from proxy `model_id`s; verdict map unchanged; no-nesting guard extended to `ensemble.py`; swarm merge stays scoring-free | FR-RH2.1, .2, .3, .4, .8; NFR-RH2.1, .2, .5 |
| **Integration (load-bearing)** | Real dispatch→reduce→derive under `--transport stub` | `uv run pytest`, `StubTransport`, no httpx | The ensemble **actually forms**: tier 2 / merge≠fallback / reviewer_count≥2 / diversity full computed from stubbed reviewers; negative + partial-failure witnesses | FR-RH2.4, .5, .6, .9; NFR-RH2.3, .4 |
| Backward-compat | Existing reflect suite green unchanged | `uv run pytest tests/cli/reflect -q` | Verdict map, contract shape, runner, write-back all preserved | FR-RH2.7; NFR-RH2.6 |
| (No new) E2E / Perf / Security | n/a | n/a | Out of scope: live-proxy E2E burns credits (the stub lane replaces it for CI); no perf/security surface added | PRD §1.2 out-of-scope |

> **Anti-pattern the integration level exists to kill:** a `pass.yaml`-driven e2e can be 100% green while `ensemble.py`'s real dispatch→reduce→derive is broken or absent — the test and the thing-under-test share the same fabricated witness. The stub-integration level breaks that loop by computing the witness from real (stubbed) reviewer outputs. `[CODE-VERIFIED: 07 Part 4]`

### 15.2 Unit Tests

File: `tests/cli/reflect/test_ensemble_unit.py` (new) + extensions to `tests/cli/reflect/test_no_nesting_guard.py` (existing) + assertions against `tests/swarm/`-style lens/merge guards. `[UNVERIFIED: ensemble.py function names — module not yet created (07 Gaps); names below are the TDD's canonical proposals.]`

| # | Component / Function | Test case | Expected result | FR/NFR acceptance |
|---|----------------------|-----------|-----------------|-------------------|
| U1 | `reflect-review` lens registration | Register lens; run the swarm lens validator (same gate as `bare-review`) | Lens registered + passes validator; emits `suspect: true` and a `recommended_next_command_template` containing `/sc:adversarial` with `{suspect_files}` substitution | FR-RH2.2 AC-1, AC-2 |
| U2 | `reflect-review` lens config | Inspect `default_workers` and model binding | `default_workers ∈ [2,4]`; lens does NOT hard-code a Claude model (models come from `T2Model0N` env pool, not `spec.workers.models`) | FR-RH2.2 AC-3 |
| U3 | `ensemble` slot→model binding | Build the per-slot transport factory with pool ≥ reviewers; inspect each slot's bound model | Each slot `i` binds a **distinct** `T2Model0N` (`pool[i % len(pool)]`, guard ensures no wraparound/reuse) | FR-RH2.1 AC-2; NFR-RH2.5 |
| U4 | `ModelPoolTooSmallError` guard | Build factory with `workers_requested > len(pool)` | Raises `ModelPoolTooSmallError(pool_size, workers_requested)` **eagerly at build time**, before any slot dispatches | FR-RH2.1; NFR-RH2.5 (pool guard) |
| U5 | Diversity source | Compute `t2_model_class_diversity` from succeeded `WorkerResult.model_id`s vs from `ANTHROPIC_DEFAULT_*` alias count | Diversity derived from **distinct proxy `model_id`s of M succeeded workers**, NOT from `ANTHROPIC_DEFAULT_*` alias count | FR-RH2.4 AC-4; NFR-RH2.5 |
| U6 | Verdict map unchanged | Call `derive_verdict` on the four verdict fixtures | `pass→0`, `halted→10`, `degraded→11`, `blocked→2` unchanged | FR-RH2.7 AC-1; NFR-RH2.6 |
| U7 | No-nesting guard extended to `ensemble.py` | Run extended `test_no_nesting_guard.py` (Layer B + raw-subprocess looped over `_NO_NEST_SRCS = [runner.py, ensemble.py]`) | `ensemble.py` contains `ClaudeProcess`, NO `Task(`/`subagent`/`import anthropic`/`from anthropic`, NO raw `subprocess.run`/`Popen`/`import subprocess` | FR-RH2.8 AC-1, AC-3; NFR-RH2.1, .2 |
| U8 | Swarm merge stays scoring-free | Run swarm merge boundary guards (LOC ceiling + boundary test) after FR-RH2 | `swarm/merge.py` ≤30 LOC, no scoring/ranking/dedup added; boundary tests green | FR-RH2.3 AC-2 |

**Unit pass criteria / commands:**

```
uv run pytest tests/cli/reflect/test_ensemble_unit.py -v
uv run pytest tests/cli/reflect/test_no_nesting_guard.py -v
uv run pytest tests/swarm/test_merge_loc_ceiling.py tests/swarm/test_merge_mechanical_only.py -v
```

### 15.3 Integration Tests (the load-bearing proof)

File: `tests/cli/reflect/test_ensemble_stub_integration.py` (new — does NOT exist yet, `[CODE-VERIFIED: 07 Part 1 inventory]`). **Mirror-shape** of `tests/swarm/test_commands_run.py::test_run_cmd_stub_transport_dispatches_workers_not_noop` (L507-568) — replicate the *structure* (real dispatch under an injected stub transport + results==N + behavioral-artifact witnesses), authored against the reflect ensemble's own API. NOT reuse-by-import (different package/transport), NOT extract-shared. `[CODE-VERIFIED: 07 Part 5 reuse verdict]`

> **CRITICAL — avoids the conftest mock gap (FR-RH2.5 AC-3):** these tests MUST NOT reuse `make_claude_process_stub`'s canned-fixture path (the `ClaudeProcess` MagicMock whose `.wait()` copies `fixtures/*.yaml` into `return-contract.yaml`). That path short-circuits the entire ensemble and re-creates the exact gap that hid the original Tier-2 defect. Instead, inject a `StubTransport` at the **transport** seam and let `dispatch_wave1 → reduce_wave3 → derive_verdict` run for real, so `tier_reached`/`merge_method`/diversity are **computed from stubbed reviewer outputs**, then mapped by `derive_verdict`. The contract is **produced by the real reduce step**, never pre-written. `[CODE-VERIFIED: 07 Part 3, Part 4]`

| # | Test case | Setup (real flow, `--transport stub`) | Positive assertions (must hold) | Negative assertions (must FAIL here) | FR/NFR acceptance |
|---|-----------|----------------------------------------|----------------------------------|--------------------------------------|-------------------|
| I1 | **Positive witness (≥2 reviewers)** | Real reflect Tier-2 driver, `--transport stub` returning ≥2 **distinct** reviewer responses; no network I/O; no `ClaudeProcess` canned-fixture patch | `tier_reached == 2`; `merge_method != "single-reviewer-fallback"`; `reviewer_count == M >= 2`; `t2_model_class_diversity == "full"`; `derive_verdict → Verdict.PASS` / exit 0 | n/a | FR-RH2.4 (all AC), FR-RH2.5 AC-1/2/3; NFR-RH2.3, .4 |
| I2 | **Negative witness (1 reviewer)** | Same real flow, `--reviewers 1` (or stub returns a single response) | reduce sets `tier_reached == 1` and/or `merge_method == "single-reviewer-fallback"`; `derive_verdict → Verdict.DEGRADED` / exit 11; reason `single-reviewer-fallback` (and/or `degraded-tier1`) | The I1 positive assertions FAIL: `reviewer_count < 2`, `tier_reached != 2`, diversity != "full" — proving the proof is falsifiable, not vacuous | FR-RH2.6 (both AC); NFR-RH2.3 |
| I3 | **Partial-failure 2-of-3, 2 distinct classes** | `--reviewers 3`, stub drives one worker to `proxy_error` (after retry); the 2 survivors are distinct model classes | `M == 2`; `t2_model_class_diversity == "full"`; PASS-eligible (`status:success`); exit 0 | n/a | FR-RH2.9 AC-1 (PASS branch) |
| I4 | **Partial-failure 2-of-3, duplicate survivor classes** | `--reviewers 3`, 1 failure, the 2 survivors resolve to the **same** model class | `M == 2` but `t2_model_class_diversity != "full"`; `derive_verdict → DEGRADED` / exit 11; reason `degraded-model-diversity` | The I3/I1 PASS assertions FAIL: diversity != "full", not PASS-eligible | FR-RH2.9 AC-1 (degraded branch); FR-RH2.4 AC-4 |
| I5 | **M==1 from N>1 (N−1 failures)** | `--reviewers 3`, stub drives 2 workers to failure → M==1 | `single-reviewer-fallback` and/or `tier_reached == 1`; DEGRADED / exit 11 — same path as `--reviewers 1`, by design not special-case | I1 PASS assertions FAIL | FR-RH2.9 AC-2 |
| I6 | **All-fail M==0** | `--reviewers 3`, stub drives all workers to `proxy_error`/`timeout` → M==0, no usable artifacts | `derive_verdict → Verdict.BLOCKED` / exit **2** (ordered ahead of degraded); reason `ensemble-empty`; NOT a silent degrade | DEGRADED/exit11 must NOT be returned (blocked precedes degraded) | FR-RH2.9 AC-3; PRD §5.4 ordering |
| I7 | **Return-contract shape preserved** | Run I1 then inspect the reflect `return-contract.yaml` + `write_reflect_post` output + sidecar | Existing fields keep names/semantics; `reflect_post:` field **set/order unchanged**; sidecar keeps its fields | n/a | FR-RH2.7 AC-2 |
| I8 | **Path-confinement** | Run I1 with a `t2-swarm/` subrun present | `reflect.derive_verdict` parses only `<output_dir>/return-contract.yaml`; does NOT parse `t2-swarm/return-contract.yaml` directly (disjoint schemas) | n/a | PRD §5.3 path_confinement |

**Integration pass criteria / commands:**

```
uv run pytest tests/cli/reflect/test_ensemble_stub_integration.py -v
```

- **Mutation-catching contrast:** the same harness that GREENs on I1 (≥2 distinct reviewers) MUST go RED (degraded/blocked) on I2, I4, I5, I6 — proving the assertions are wired to *observed* reviewer count + computed diversity, not a fixture constant. `[CODE-VERIFIED: 07 Part 5 negative-witness contract]`
- **Zero network I/O (NFR-RH2.4):** the `StubTransport` is stdlib-only (`hashlib`/`threading`), `del timeout`, fixed `elapsed_ms`, pure-function body — no httpx/socket import is reachable. `[CODE-VERIFIED: 04 §4 stub.py]`
- **Grounding for the negative witnesses:** `derive_verdict`'s degraded triggers already key on `merge_method == "single-reviewer-fallback"` (Trigger 10, contract.py L280-281), `t2_model_class_diversity != "full"` (Trigger 7, L267-269), and `expected_tier>=2 and tier_reached==1` (Trigger 6, L263-264) — so a real 1-reviewer reduce deterministically routes DEGRADED/exit11. The negative witnesses are grounded in real verdict logic, not a fixture. `[CODE-VERIFIED: 07 Part 4]`

### 15.4 Backward-Compatibility Tests (NFR-RH2.6)

The existing reflect suite is the **regression floor**: it pins the verdict-mapping + write-back contracts that `ensemble.py` feeds into. These MUST stay green **without modification** (FR-RH2.7 AC-3, NFR-RH2.6). `[CODE-VERIFIED: 07 Gaps — backward-compat suite content]`

| # | Test file (existing) | What it pins | Must stay green because |
|---|----------------------|--------------|--------------------------|
| B1 | `tests/cli/reflect/test_verdict_mapping.py` (277 L) | Calls `derive_verdict` directly; §6 matrix (PASS/0, HALTED/10, DEGRADED/11, BLOCKED/2), first-match ordering, single-vendor flag (L67-88), fail-loud unknown major version (L119-128), NFR-8 unknown-field tolerance (L131-140), F0/F2/F5 fail-closed fixes (L204-277) | FR-RH2.7 AC-1: verdict map + exit codes unchanged |
| B2 | `tests/cli/reflect/test_runner_e2e.py` (221 L) | Drives real `ReflectRunner.run` with `ClaudeProcess` patched to Idiom-B factory; verdict + exit + `reflect_post.verdict` write-back for pass/halted/degraded/blocked, G1 `max_turns==250` (L49-50), G2 resume short-circuit (L142-172), FR-6 fail-closed write-back (L175-221) | FR-RH2.7 AC-3: runner contract preserved |
| B3 | `tests/cli/reflect/test_writeback.py` (173 L) | `write_reflect_post`/`write_sidecar`: atomic write-back preserves body byte-for-byte + §6 block (L61-104), compare-mismatch → `frontmatter-stale` no-overwrite + sidecar (L106-136), CRLF round-trip → `written` (L139-172) | FR-RH2.7 AC-2: `reflect_post:` field set/order + sidecar fields unchanged |

**Backward-compat pass criteria / command:**

```
uv run pytest tests/cli/reflect -q
```

Pass criterion (NFR-RH2.6): the **entire** `tests/cli/reflect` directory is green, with B1/B2/B3 unmodified. If `ensemble.py` changes the launch path such that `make_claude_process_stub` needs an ensemble-aware variant, that variant is **additive** — the existing B1/B2/B3 assertions are not edited. `[UNVERIFIED: whether `pass.yaml` gains reviewer fields is a TDD design choice (07 Gaps); the constraint is that B1/B2/B3 stay green either way.]`

### 15.5 FR-RH2 acceptance traceability (every test maps to a criterion)

| FR/NFR | Acceptance criterion | Covered by |
|--------|----------------------|------------|
| FR-RH2.1 | Tier-2 via swarm dispatch; distinct `T2Model0N` per slot; Tier-1 unchanged | U3, U7, B2 |
| FR-RH2.2 | `reflect-review` lens registers + validates; `suspect:true` + `/sc:adversarial {suspect_files}`; `default_workers∈[2,4]` | U1, U2 |
| FR-RH2.3 | Consumes per-reviewer `final_path`; no scoring in `swarm/merge.py`; convergence score on contract | U8, I1 |
| FR-RH2.4 | tier 2 / merge≠fallback / reviewer_count≥2 / diversity full (over M) | I1, U5 |
| FR-RH2.5 | Real flow under `--transport stub`, zero I/O, NOT canned-fixture path | I1 (+ §15.3 CRITICAL note) |
| FR-RH2.6 | 1-reviewer degrades; positive assertions FAIL | I2 |
| FR-RH2.7 | verdict map + exit codes; `reflect_post:` field set/order; sidecar; existing tests unmodified | U6, I7, B1, B2, B3 |
| FR-RH2.8 | no `Task(`/`subagent`/`anthropic`/raw `subprocess` in `ensemble.py`; amendment on record | U7 |
| FR-RH2.9 | 2-of-3 PASS-iff-2-classes; M==1 fallback; M==0 blocked exit2 | I3, I4, I5, I6 |
| NFR-RH2.3 | non-vacuous: positive + falsifying witness, both real path | I1 + I2 |
| NFR-RH2.4 | credit-free CI, zero network I/O | I1 (StubTransport stdlib-only) |
| NFR-RH2.5 | diversity from distinct proxy `model_id`s | U5, I1, I4 |
| NFR-RH2.6 | existing reflect tests pass unchanged | B1, B2, B3 |

---

**Status: Complete** — §14 (Observability & Monitoring) and §15 (Testing Strategy) synthesized, template-aligned, every test mapped to an FR-RH2/NFR-RH2 acceptance criterion. Code-verified anchors: `contract.py` `_degraded_reason` triggers, `reduce.py`/`models.py` `done.json` sentinel + M/N + `WorkerResult`, `stub.py` zero-I/O determinism, `test_no_nesting_guard.py` extension shape. `[UNVERIFIED]` confined to `ensemble.py` internal names (module not yet created) and the spec-vocabulary `ensemble-empty` slug string.
