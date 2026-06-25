# Synthesis 06 — Error Handling, Edge Cases & Security (TDD §12–§13)

**Feature**: FR-RH2 (Headless Ensemble Fix) — drive sc:reflect Tier-2 reviewer ensemble through the swarm dispatch library.
**Target release**: 4.4.0 | **Complexity**: HIGH (0.82)
**Maps to**: TDD template §12 (Error Handling & Edge Cases) + §13 (Security Considerations).
**Source research (all code-verified)**: `research/00-prd-extraction.md` (the (M,N) divergence table, spec §5), `research/02-reflect-contract-verdict.md` (`derive_verdict` ordering + BLOCKED slugs), `research/04-swarm-transport-pool.md` (transport enum, `ModelPoolTooSmallError`, proxy contract), `research/05-swarm-reduce-merge-contract.md` (reduce/merge boundary, INV-005 arithmetic, path confinement).
**Date**: 2026-06-20 | **Status**: Complete

> **Provenance discipline**: Every value below traces to a code-verified research finding. Two reconciliation notes (D3, D6) flag where the spec's stated contract diverges from current code; both are documented as edge cases, not silently smoothed over.

---

## 12. Error Handling & Edge Cases

### 12.1 Error Categories

The FR-RH2 driver (`ensemble.py`) sits between three failure surfaces: (a) the **swarm transport/dispatch layer** (proxy I/O, pool guard, enum guard), (b) the **swarm reduce/merge layer** (M/N reduction, contract emission), and (c) the **reflect verdict layer** (`derive_verdict`, exit-code map). Errors are categorized by where they surface and how they route to the 4-state verdict.

| Category | Examples | Surfaces at | Verdict / Exit | Recovery |
|----------|----------|-------------|----------------|----------|
| Config / env-contract errors | Missing `T2ProxyUrl` / `T2ProxyKey` / all `T2Model0N` slots | `read_env` eager preflight (`openai_compat.py:159-202`) → `TransportEnvError` | `EXIT_INVALID` (swarm subrun) → routes to reflect `blocked`/exit 2 (no usable artifacts) | Operator sets the missing env vars per `~/.aienv`; no retry |
| Pool-size errors | `len(T2Model0N pool) < --reviewers` | `_resolve_run_transport_factory` eager build (`commands.py:687-688`) → `ModelPoolTooSmallError` | `EXIT_INVALID`, message on stderr, **no slot dispatched** | Add `T2Model0N` slots OR reduce `workers.count` (message is actionable) |
| CLI parse errors | `--transport bogus` (not in enum) | Click enum validation, **before any dispatch** | Non-zero exit, no partial run | Re-invoke with `openai_compat` or `stub` |
| Per-worker transport errors | non-200 / connection refused / DNS (`proxy_error`); `httpx.TimeoutException` (`timeout`); 200-but-unparseable (`parse_error`) | `OpenAICompatTransport.send` status mapping (`openai_compat.py:329-382`) | Drops the worker from M; reduce computes status on survivors | 5xx → retry once (FR-017); else drop (see §12.4) |
| Partial-failure / divergence | N requested slots reduce to M succeeded | `reduce_wave3` (`reduce.py:647-658`) + reflect `derive_verdict` | Per (M,N) table (§12.2.1) | Graceful degradation (§12.3); never a silent pass |
| Contract-integrity errors | Missing / unparseable / wrong major version / malformed load-bearing field / child crash/timeout | reflect `derive_verdict` Stage 1 (`contract.py:147-209`) | `blocked` / exit 2 | Fail-loud; investigate contract emission |

### 12.2 Edge Cases

#### 12.2.1 The (M,N) divergence table — the load-bearing partial-failure boundary

The Tier-2 fan-out is a **filtering pipeline**: N requested reviewer slots reduce to M succeeded workers (`proxy_error` / `timeout` / `parse_error` failures drop the count). `M = sum(1 for w in worker_results if w.status == "success")` (`reduce.py:648`); `N = workers_requested` if supplied else `len(worker_results)` (`reduce.py:650-653`). The verdict for **any** (M,N) is fully derivable from this table (reproduced verbatim from spec §5.3 `mn_guard_table`):

| M-condition | verdict | exit-code | reason-slug | Test case |
|-------------|---------|-----------|-------------|-----------|
| `M==0` (all workers failed / no usable artifacts) | `blocked` | `2` | `ensemble-empty` *(see D3 reconciliation below)* | An M==0 outcome routes `blocked` (exit 2), NOT `degraded` — untrustworthy audit, never a silent degrade |
| `M==1` (≥N−1 failed, or `--reviewers 1`) | `degraded` | `11` | `single-reviewer-fallback` | 1-reviewer stub run OR 3-slot run that loses 2 workers; both reach the SAME path by design (FR-RH2.6 negative witness) |
| `M>=2` but `<2 distinct model classes` (survivors collapsed onto one class) | `degraded` | `11` | `degraded-model-diversity` | `--reviewers 3` with one `proxy_error` → M==2; if the 2 survivors are the same model class → `degraded-model-diversity`, never PASS |
| `M>=2` AND `>=2 distinct classes` | `pass-eligible` | `0` | `pass` | `--reviewers 3` with one `proxy_error` → M==2; if the 2 survivors are ≥2 distinct classes → PASS-eligible (`t2_model_class_diversity:full`) |

**Diversity and `reviewer_count` are measured over the SUCCEEDED workers (M), not the requested slots (N)** (FR-RH2.4 / FR-RH2.9). `t2_model_class_diversity == "full"` is computed over the **distinct `model_id`s of the M succeeded workers** (≥ the expected distinct-class count) — so two survivors that resolved to the same model class do NOT count as `full`. A 3-slot run that loses 2 workers lands on `M==1` by design, not as a special case.

> **D3 reconciliation note — `ensemble-empty` slug does NOT exist in `contract.py` today (cross-refs §22 Open Question).**
> The spec's (M,N) table names `ensemble-empty` as the M==0 reason-slug. **This slug does not exist in the reflect verdict layer today.** The current BLOCKED reason-slugs emitted by `derive_verdict` (`research/02` §1–2, code-verified against `contract.py:147-209`) are: `timeout`, `child-crash`, `contract-missing`, `contract-version-missing`, `unknown-major-version`, `malformed-degraded-components`, `malformed-contract-boolean`. There is **no `M==0` branch and no `ensemble-empty` slug** in `derive_verdict`. This collides with **FR-RH2.7** ("verdict map unchanged"; `derive_verdict` and the `Verdict` exit-code map are explicitly out of scope to change). Two reconciliation options, to be settled at §22 Open Question:
> - **Option A (deliberate recorded change)**: add a new `derive_verdict` M==0 BLOCKED branch emitting `ensemble-empty`. This is a *deliberate, recorded* amendment to the verdict layer and must be called out against FR-RH2.7's "unchanged" claim (the exit-code map stays unchanged — only a new slug is added within the existing `blocked`/exit-2 verdict). The mapping layer (`ensemble.py`) would surface M==0 as a contract state (e.g. zero usable `output_files`, no `tier_reached`) that the new branch keys on.
> - **Option B (map onto an existing trigger)**: route M==0 onto an existing BLOCKED trigger without a new slug — e.g. `ensemble.py` emits no usable reflect contract (or a contract with a malformed/absent load-bearing field), so the existing `contract-missing` / `malformed-*` Stage-1 guards fire `blocked`/exit 2. This preserves FR-RH2.7 literally (no `derive_verdict` change) at the cost of a less specific slug.
> Either way the **verdict/exit-code is the same** (`blocked`/exit 2); only the slug fidelity differs. The choice is recorded as an Open Question, not silently resolved.

#### 12.2.2 Worker-status → M mapping

`reduce_wave3` counts `success` only (`reduce.py:648`). Failure statuses drop the worker from M (spec §5.3 `worker_status_to_m`, code-verified `research/04` §5 status mapping):

| `WorkerResult.status` | Counts toward M? | Source / note |
|------------------------|------------------|---------------|
| `success` | **counts toward M** | HTTP 200 + parseable Chat-Completions + non-empty `choices[0].message.content` (`openai_compat.py:368-382`); stub always returns `success` (`stub.py:122-159`) |
| `proxy_error` | does NOT count | any non-200 OR non-timeout `httpx.RequestError`; retry-once-then-drop per swarm §7 matrix (5xx only) |
| `timeout` | does NOT count | `httpx.TimeoutException` (`openai_compat.py:329-336`); no retry |
| `parse_error` | does NOT count | HTTP 200 but body not JSON / no `choices` / empty content (`openai_compat.py:369-375`). **Salvage may promote `parse_error → success` upstream (swarm §7.4); post-salvage status governs M** |

#### 12.2.3 Additional edge cases

| Scenario | Expected Behavior | Test Case |
|----------|-------------------|-----------|
| `ModelPoolTooSmallError` — `len(T2Model0N pool) < workers_requested` | **Eager raise at transport-factory build time, BEFORE any slot is dispatched** (`commands.py:687-688`). Exact message: `"T2 model pool has {pool_size} model(s) but the job requests {workers_requested} worker(s); each worker binds a distinct T2Model0N slot. Set at least {workers_requested} T2Model0N slot(s), or reduce workers.count to <= {pool_size}."` Caught in `run_cmd` → `EXIT_INVALID` with message on stderr (`commands.py:1830-1846`). | Set 2 `T2Model0N` slots, request `--reviewers 3`: assert `ModelPoolTooSmallError(2, 3)` raised eagerly, no slot dispatched, exit `EXIT_INVALID` |
| `ModelPoolTooSmallError` vs INV-005 — the gap INV-005 cannot see | INV-005 guards `workers.count` against `spec.workers.models` (lens **placeholder** ids), NOT the live `T2Model0N` env pool the factory binds. A job can pass preflight (enough placeholders) yet have fewer real env models than workers. The D2 guard fails loudly instead of silently `pool[i % len]`-wrapping and reusing a model. | Job with enough placeholders but 2 real `T2Model0N`, `--reviewers 3`: INV-005 passes preflight, `ModelPoolTooSmallError` still fires at factory build |
| `--transport` unknown enum value | Rejected at **Click parse** (enum validation), before any dispatch — non-zero exit, **no partial run** (spec §5.3 `transport_enum`; `research/04`). Accepted: `[openai_compat, stub]`. | `--transport bogus` → Click usage error, exit ≠ 0, zero workers dispatched |
| Two `return-contract.yaml` files (path confinement) | Reflect parses ONLY `<output_dir>/return-contract.yaml` (the file `reflect.derive_verdict` reads via the runner-pinned path; `contract.py:65`, `_make_result:120`). It MUST NOT parse `<output_dir>/t2-swarm/return-contract.yaml` (swarm DM-012; consumed by `ensemble.py` only). The two schemas are **disjoint** — they share only the key name `status`, with different semantics (swarm IMM-5 worker verdict ≠ reflect tier-success). | Assert `derive_verdict` is handed only the reflect-pinned path; assert no walk into `t2-swarm/`; assert swarm DM-012 keys (`workers_succeeded`, `amalgamation_mode`, `merged_path`, `output_files`) never reach `derive_verdict` raw |
| Verdict ordering — first-match-wins | `derive_verdict` evaluates `blocked → degraded → halted → pass` (first match returns; `contract.py:130-246`). **M==0 `blocked` is ordered structurally AHEAD of `degraded`**: a contract with zero trustworthy signal (missing / unparseable / wrong major version / malformed load-bearing field / child crash) returns `blocked` BEFORE `_degraded_reason`/`_halted_reason` ever run. This is the M==0 → blocked/exit-2 guarantee: zero trustworthy signal never leaks to a degrade/halt/pass evaluation. | Assert a contract that would otherwise look "degraded" but is malformed returns `blocked` (exit 2), not `degraded` (exit 11) |
| INV-005 arithmetic gap in `reduce_wave3` (D6) | `workers_failed = sum(1 for w in worker_results if w.status != "success")` counts against `len(worker_results)`, while N = `workers_requested` may differ (`reduce.py:649-653`). If `workers_requested > len(worker_results)`, the emitted contract's `succeeded + failed != requested` — INV-005 (`succeeded+failed==requested`) does NOT mechanically hold inside this function. The dataclass defers INV-005 to the emitter (`models.py:982-986`); `reduce_wave3` does not re-check it. *(See D6 note below.)* | Pass `workers_requested=4` with only 3 `WorkerResult`s: assert the emitted contract may show `succeeded + failed == 3 != 4`; document that the mapping layer must reconcile M against the original N, not `len(worker_results)` |

> **D6 reconciliation note — INV-005 arithmetic gap in `reduce_wave3`.**
> `research/05` §1.1 + Gap 4 (code-verified) flags that `workers_failed` is counted against `len(worker_results)` while N may be `workers_requested`. The identity `succeeded + failed == requested` is therefore **not guaranteed inside `reduce_wave3`**: a caller passing `workers_requested > len(worker_results)` (e.g. slots that never produced a `WorkerResult` at all, vs. slots that produced a failed one) emits a contract where `M + workers_failed != N`. Real M5 wiring passes the preflight-recorded N so *retried* slots count against the original N — but a slot that produced no `WorkerResult` entry is invisible to `workers_failed`. **Design implication for `ensemble.py`**: when mapping swarm execution facts → reflect verdict vocabulary, compute the M==0/M==1 boundary from **M against the original requested N (preflight-recorded)**, not from `M + workers_failed`; do not assume the swarm contract's three count fields are internally consistent. This is a documented invariant gap, not a blocker.

### 12.3 Graceful Degradation

The whole FR-RH2 design is a graceful-degradation ladder: a Tier-2 ensemble that loses reviewers does NOT crash and does NOT silently pass — it degrades to the lowest trustworthy verdict the surviving signal supports. Degradation is **always a non-PASS** (`is_promotable ⇔ PASS`, `models.py:51-54`); the audit never claims a clean result it cannot back.

| Component Failure | Degraded Experience | Fallback Behavior |
|-------------------|---------------------|-------------------|
| 1 of N workers fails (`proxy_error`/`timeout`), M stays ≥2 with ≥2 classes | Full Tier-2 audit on the survivors | `pass-eligible` (exit 0); diversity computed over M survivors, not N slots |
| Survivors collapse onto a single model class (M≥2, <2 distinct classes) | Audit ran but lacks model-class diversity → untrustworthy | `degraded` / `degraded-model-diversity` (exit 11), never PASS |
| Down to a single reviewer (M==1) | No adversarial cross-check possible | `degraded` / `single-reviewer-fallback` and/or `tier_reached:1` (exit 11); same path as `--reviewers 1` negative witness |
| All workers fail (M==0) | No usable audit signal at all | `blocked` (exit 2); fail-loud, ordered ahead of degraded |
| Adversarial merge stage cannot run (`adversarial_unavailable:true`) | Reviewers ran but no convergence score | `degraded` / `adversarial-unavailable` (exit 11); the swarm `mechanical_merge` concat is NEVER promoted to the adversarial verdict |
| Live proxy unavailable (CI, no credits) | Ensemble formation still provable | `--transport stub` lane: real `dispatch_wave1`/`reduce_wave3` over deterministic network-free `StubTransport`, zero network I/O (FR-RH2.5 / NFR-RH2.4) |
| Chain-critical capability loss (serena/auggie/evidence-validator down) | Audit produced output but a trust-critical tool was missing | `degraded` / `degraded-components` (exit 11) via exact membership in `_DEGRADED_COMPONENTS_HALT_SET` |

### 12.4 Retry & Recovery Strategies

The swarm dispatch layer retries on exactly one signature (5xx), **once, with a 2s backoff**; everything else fails fast and drops the worker. The per-call wall-clock budget is **180s** (`_DEFAULT_TIMEOUT_SEC = 180` / `WorkerSpec.timeout_sec`, NFR-010; `dispatch.py:124`, `:244`). Per-worker retry policy is code-verified against the swarm §7 matrix (`dispatch.py:202-273`; defaults `on_5xx=True`, `on_5xx_backoff_sec=2`, `on_4xx=False`, `on_timeout=False` at `dispatch.py:224-225`; the configured backoff is slept at `dispatch.py:269-271` before the single retry) and `WorkerResult.attempts` semantics (`models.py:1117-1128`: `attempts=1` no retry, `attempts=2` 5xx retried once). This matches synth-08 §17.2.

| Error Type | Retry Strategy | Max Attempts | Backoff / Budget |
|------------|----------------|--------------|------------------|
| Swarm dispatch 5xx (server error) | **Retry once** with **2s backoff** (`on_5xx_backoff_sec=2`), then drop | 2 (`attempts=2`) | Single retry after a 2s backoff sleep (`dispatch.py:269-271`); per-call budget 180s (`elapsed_ms` excludes the backoff sleep) |
| 4xx / non-200 non-5xx (`proxy_error`) | **No retry** — drop worker, decrement M | 1 (`attempts=1`) | N/A — fails fast |
| Connection refused / DNS / read error (`proxy_error`) | **No retry** — drop worker; model identity preserved (F-P3-5) | 1 | N/A |
| Worker timeout (`httpx.TimeoutException`, `timeout`) | **No retry** — drop worker, decrement M | 1 | Default **180s** wall-clock per call (NFR-010) |
| 200-but-unparseable (`parse_error`) | **No retry** at transport; salvage may promote upstream (swarm §7.4) | 1 | Post-salvage status governs M |
| Env-contract / pool-size / enum errors | **No retry** — eager raise, fail-loud | 0 | N/A — caught before dispatch |
| Stub transport | No I/O to retry against; `del timeout` (`stub.py:143`); fixed `elapsed_ms` | 1 (always `success`) | No clock dependency |

**Recovery routing**: a dropped worker reduces M; the run does not abort — `reduce_wave3` computes status on the survivors and emits the contract. Recovery is the (M,N) ladder of §12.2.1, not a wait-and-retry loop. There is **no response cache** (NFR-014 / AC-015, `openai_compat.py:79-85`): every `send` issues a fresh request, so retries never serve stale bodies.

---

## 13. Security Considerations

FR-RH2 introduces an **external proxy fan-out** (Tier-2 reviewers run on `T2Model0N` models reached over an OpenAI-compatible HTTP proxy) and consumes **untrusted reviewer output** back into the reflect verdict. The two principal security concerns are therefore (1) keeping the proxy contract tight (no rogue endpoints, no credential leakage) and (2) never trusting reviewer output raw. Both are addressed by construction, not by runtime policy.

### 13.1 Threat Model

| Threat | Likelihood | Impact | Mitigation |
|--------|------------|--------|------------|
| Rogue/unexpected proxy endpoint — code probes `:4000/v1` or `:8317` instead of the contracted `:4000/cli` base | L | H | **Proxy contract by construction**: transport/config code hardcodes NO host/port/path (`research/04` §5; grep over `cli/swarm/` finds no `:4000`/`:8317`/`/v1`/`/cli` literal). Base URL comes 100% from `T2ProxyUrl`; the only appended suffix is `/chat/completions` (`openai_compat.py:122`). Whatever `T2ProxyUrl` resolves to (`…:4000/cli`) gets `/chat/completions` appended and nothing else is constructed — `:4000/v1` and `:8317` are unreachable |
| Credential leakage — `T2ProxyKey` / `ANTHROPIC_DEFAULT_*` exposed in logs, artifacts, or stripped from child env | M | H | `_child_env` preserves `T2ProxyKey` / `ANTHROPIC_DEFAULT_*` into the child process env from `os.environ` (never hardcoded, never echoed). Key is sent only as `Authorization: Bearer <api_key>` header (`openai_compat.py:311-314`); no response cache writes bodies-with-headers to disk (NFR-014). Env vars flow var→`os.environ`→child, never into the contract or merged artifacts |
| Untrusted reviewer output trusted as verdict — a malicious/compromised reviewer model emits a fabricated "all clear" that promotes to PASS | M | H | **`suspect: true` framing**: the `reflect-review` lens marks every reviewer artifact `suspect: true` (FR-RH2.2); reviews are NEVER trusted raw. They are routed through `/sc:adversarial` Mode A as the downstream scorer (FR-RH2.3). Swarm `mechanical_merge` is a scoring-free concat and MUST NOT be treated as the adversarial verdict (`merge.py` boundary; FR-RH2.3 AC) |
| Prompt injection via reviewer brief / target content — adversarial text in the audited material hijacks a reviewer | M | M | **Injection guard on the lens**: the `reflect-review` lens embeds `schema.CANONICAL_INJECTION_GUARD_SENTENCE` (FR-RH2.2 dependency), the same canonical guard `bare-review` uses; the worker is framed as a heterogeneous reviewer treating target content as data, not instructions. Reviewer output is further quarantined by `suspect:true` + adversarial scoring (above) |
| Silent degrade leaks to PASS — a partial/untrustworthy ensemble (M<2, no diversity, malformed contract) is promoted | L | H | **Verdict ordering `blocked → degraded → halted → pass`, first-match-wins** (`contract.py:130-246`); strict `is True`/`is False` identity (not truthiness) + F0/F2/list-shape fail-closed guards stop a malformed-but-truthy field leaking past identity checks into PASS (`research/02` §1, takeaways 4–5) |
| Path traversal / cross-run contamination — reflect parses the wrong `return-contract.yaml` or swarm writes outside its output dir | L | M | **Path confinement (two contracts)**: reflect parses ONLY its runner-pinned `<output_dir>/return-contract.yaml`, never the `t2-swarm/` subdir (§12.2.3). Swarm writes are confined to the caller-supplied `output_dir` (NFR-013); `emit_contract` always targets `<output_dir>/return-contract.yaml` via atomic tmp+fsync+`os.replace` (`reduce.py:369-394`) |
| Network exfiltration in CI / credit burn on every test | L | M | **`--transport stub`** drives the real wrapper over a stdlib-only, network-free `StubTransport` (imports only `hashlib`/`threading`; `del timeout`; pure-function body) — zero HTTP/DNS/socket, zero credits (FR-RH2.5 / NFR-RH2.4; `research/04` §4) |

### 13.2 Security Controls

| Control | Implementation | Verification |
|---------|----------------|--------------|
| Proxy endpoint allow-listing | No host/port/path literal in transport/config code; base URL solely from `T2ProxyUrl`, only `/chat/completions` appended (`openai_compat.py:122,252,264-267`) | `tests/swarm/` T03.20 grep test: no host-vendor URL or host-vendor model id in any transport-config source; `research/04` §5 negative-grep finding |
| Env-contract preflight | `read_env` (`openai_compat.py:159-202`) reads `T2ProxyUrl`/`T2ProxyKey`/dense `T2Model01..09` from `os.environ`; raises `TransportEnvError(tuple(missing))` if incomplete, BEFORE any dispatch | `read_env` preflight unit test; NFR-RH2.8 (`uv run pytest` over swarm transport tests); swarm never opens an `.aienv` file (grep finds no `aienv` hits) |
| Credential confinement (`_child_env`) | `T2ProxyKey` / `ANTHROPIC_DEFAULT_*` preserved into child env from `os.environ`; key transmitted only as `Authorization: Bearer` header; no cache persists request bodies (NFR-014) | Child-env preservation test (asserts proxy key + `ANTHROPIC_DEFAULT_*` present in spawned env, absent from contract/merged artifacts) |
| Untrusted-input quarantine (`suspect:true`) | `reflect-review` lens emits `suspect: true` + `recommended_next_command_template` handing artifacts to `/sc:adversarial` with `{suspect_files}` substitution (FR-RH2.2) | Lens passes the swarm lens validator (same gate as `bare-review`); asserts `suspect:true` + `/sc:adversarial` in template (FR-RH2.2 AC) |
| Injection guard | `schema.CANONICAL_INJECTION_GUARD_SENTENCE` embedded in the `reflect-review` lens brief (FR-RH2.2 dependency) | Lens-validator gate + assertion that the canonical guard sentence is present in the rendered per-reviewer brief |
| Scoring-boundary enforcement (no trust in mechanical merge) | `merge.py::mechanical_merge` is an 8-LOC verbatim concat; sort/rank/score/judge/dedup/filter/rewrite are DISALLOWED — scoring lives in `/sc:adversarial` (`merge.py:9-29` boundary contract) | ≤30-LOC ceiling test, PR-touch review check, 3-worker boundary test, scoring-engine grep audit (`research/05` §2.1 four guards); FR-RH2.3 AC ("no scoring/ranking/dedup in `swarm/merge.py`") |
| Verdict fail-closed ordering | `derive_verdict` `blocked → degraded → halted → pass` first-match-wins; strict identity checks; F0 (non-zero `child_rc`), F2 (non-bool load-bearing field), malformed-list guards all → `blocked` (`contract.py:130-246`) | Existing reflect contract/verdict tests pass unchanged (FR-RH2.7 / NFR-RH2.6); guard-specific unit tests for each fail-closed defense |
| Path confinement | Reflect parses only the runner-pinned reflect contract path; swarm writes confined to `output_dir` with atomic replace (NFR-013) | Assert `derive_verdict` never walks `t2-swarm/`; assert swarm artifacts stay under `output_dir`; the two-`return-contract.yaml` disjoint-schema fact (`research/05` §6) |
| No-nesting guarantee (NFR-7) | No `Task(`/`subagent_type` fan-out, no raw `subprocess.run`/`Popen` in the reflect package; ensemble forms via in-process swarm-library import (FR-RH2.8) | `test_no_nesting_guard.py` Layer B (extended to `ensemble.py`); NFR-RH2.1/NFR-RH2.2 anchored regexes |

### 13.3 Sensitive Data Handling

| Data Type | Classification | Encryption | Access Control |
|-----------|----------------|------------|----------------|
| `T2ProxyKey` (proxy bearer token) | Confidential / credential | In transit: TLS to proxy + `Authorization: Bearer` header; never persisted (no response cache, NFR-014) | Read from `os.environ` only (operator `~/.aienv` export); confined to child env via `_child_env`; never written to contract/merged/log artifacts |
| `ANTHROPIC_DEFAULT_*` env (model routing) | Confidential / config | In transit only (env→child process) | Preserved into child env from `os.environ`; not echoed into artifacts |
| `T2ProxyUrl` / `T2Model0N` (proxy endpoint + model ids) | Internal / config | N/A (endpoint identifiers) | From `os.environ`; the only proxy surface; no other host/port/path constructed |
| Reviewer output artifacts (`output_files[].final_path`) | Untrusted input (`suspect:true`) | At rest under run `output_dir` | Quarantined as `suspect:true`; consumed only via `/sc:adversarial`, never trusted raw |
| Audited target content (the tasklist/spec under review) | Per source classification | At rest under `output_dir` | Sent verbatim to proxy reviewers (COMP-031 no re-normalization); injection-guarded at the lens |

---

## Cross-References & Open Items

- **D3 → §22 Open Question**: the `ensemble-empty` M==0 slug does not exist in `contract.py`; pick Option A (new `derive_verdict` BLOCKED branch, deliberate recorded change against FR-RH2.7) or Option B (route M==0 onto an existing BLOCKED trigger, preserves FR-RH2.7 literally). Verdict/exit-code identical either way (`blocked`/exit 2); only slug fidelity differs. **Unresolved — record at §22.**
- **D6 → INV-005 invariant gap**: `reduce_wave3` may emit `succeeded + failed != requested` when `workers_requested > len(worker_results)`; `ensemble.py` must compute the (M,N) boundary from M vs the preflight-recorded N, not from `M + workers_failed`.
- **OI-1 dependency**: the swarm DM-012 → reflect contract field-correspondence (`research/05` §7) is the BLOCKING GATE for FR-RH2.3; `ensemble.py` must synthesize `tier_reached` / `merge_method` / `t2_model_class_diversity` / `reviewer_count` from swarm raw facts (`workers_succeeded`, `amalgamation_mode`, `merged_path`, distinct `output_files[].model_id`) — none of these reflect verdict fields exist on the swarm contract.
- **`[UNVERIFIED]` carried from research**: `ensemble.py` does not yet exist (`research/05` Gap 1); the path-confinement contracts (§12.2.3, §13.1) are design rules to implement, not current enforcement (`research/05` Gap 2). The `~/.aienv` file format/loader is an operator convention outside this repo (`research/04` Gap).

**Status: Complete**
