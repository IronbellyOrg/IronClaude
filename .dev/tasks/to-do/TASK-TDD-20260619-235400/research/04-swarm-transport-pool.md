# Research 04 — Swarm Transport + Pool-Guard Layer

- **Topic:** Swarm transport layer (`--transport openai_compat|stub`), slot→`T2Model0N` binding, `ModelPoolTooSmallError` pool guard, `~/.aienv` preflight, Transport protocol contract.
- **Type:** API Surface Mapper
- **Scope:** `src/superclaude/cli/swarm/commands.py` (`_resolve_run_transport_factory`, `ModelPoolTooSmallError`), `transports/__init__.py` (protocol), `transports/openai_compat.py` (live proxy), `transports/stub.py` (offline deterministic), env preflight (`read_env`).
- **Status:** Complete
- **Date:** 2026-06-19

---

## 1. The Transport Protocol Contract `[CODE-VERIFIED]`

**File:** `src/superclaude/cli/swarm/transports/__init__.py:51-87`

A single-method, `@runtime_checkable` `typing.Protocol`. Structural conformance only — no base-class inheritance required.

```python
@runtime_checkable
class Transport(Protocol):
    def send(self, prompt: str, timeout: int) -> WorkerResult: ...
```

Contract terms (from the module docstring `__init__.py:20-42` and method docstring `:67-84`):

| Term | Contract |
|------|----------|
| `prompt: str` | Fully-assembled prompt body. Transport **MUST NOT re-normalize whitespace** (COMP-031) — `PromptSpec` preserved it verbatim upstream. |
| `timeout: int` | Per-call wall-clock budget in **seconds**. Default = `WorkerSpec.timeout_sec` = **180s** (NFR-010). Transports SHOULD honour it rather than block indefinitely. |
| returns `WorkerResult` | DM-013 per-worker outcome. The **transport** populates `http_code` / `attempts` / `elapsed_ms`; the **dispatch layer** fills path fields after materializing the body to disk. |

Both concrete transports also expose a `model` read-only property (not part of the Protocol, but a shared convention) and stash the raw body on the non-dataclass attribute `WorkerResult.body` so the dispatcher can materialize `raw_path` without a second `send` call.

The dispatch layer uses `isinstance(driver, Transport)` defensively because the protocol is `@runtime_checkable` (`__init__.py:38-41`).

`__all__ = ["Transport"]`.

---

## 2. Slot → `T2Model0N` Binding (the MultiModelSwarm core) `[CODE-VERIFIED]`

**File:** `src/superclaude/cli/swarm/commands.py`. The docstring at L619 reads exactly: *"Build a per-slot transport factory `(slot_index) -> Transport`."*

`_resolve_run_transport_factory(transport_kind, *, models=None, env=None, workers_requested=None) -> Callable[[int], Any]` (`commands.py:612-707`). This is the heterogeneous-fan-out generalization of the single-transport `_resolve_run_transport` (`:510-586`).

### `openai_compat` branch (`commands.py:674-703`) — the distinct-model binding

1. `config = read_env(env)` runs **eagerly at build time** (`:680`) — raises `TransportEnvError` before any slot dispatches if the contract is incomplete.
2. `pool = [m for m in config.models if m]` (`:681`) — the dense, slot-ordered tuple of `T2Model0N` ids.
3. **D2 pool guard** (`:687-688`): `if workers_requested is not None and len(pool) < workers_requested: raise ModelPoolTooSmallError(len(pool), workers_requested)`.
4. Returns `_factory(slot_index)` (`:691-701`): `model = pool[slot_index % len(pool)]`, with a per-model `cache` dict so repeated slots on the same model **reuse the same `OpenAICompatTransport` client**. One `OpenAICompatTransport` is built per *unique* model.

**Binding rule:** slot `i` → `pool[i % len(pool)]`. With a sufficient pool (`len(pool) >= workers_requested`, enforced by the guard), every slot gets a **distinct** `T2Model0N` model — no wraparound, no reuse. The modulo is a safety expression; the guard is what makes each slot distinct in practice.

### `stub` branch (`commands.py:670-673`)

`shared = _resolve_run_transport("stub", ...)` then `return lambda _slot: shared` — a **single shared `StubTransport` for every slot**. Per-slot differentiation adds no value because stub output is a pure function of `(model_id, prompt)` and the stub pool carries only lens placeholder ids (docstring `:626-630`).

### How dispatch invokes it `[CODE-VERIFIED]`

**File:** `src/superclaude/cli/swarm/dispatch.py:334-472`. `dispatch_wave1(... transport_for_slot: Optional[Callable[[int], Transport]] = None ...)`. Per slot (`:448-460`): `slot_transport = transport_for_slot(slot_index) if transport_for_slot is not None else transport`, then `_run_worker(slot_index, slot_transport, ...)`. One `Task` per `range(workers_requested)` (`:464-472`), each calling the factory with its own `slot_index` (default-arg binding at `:444` avoids the late-binding closure trap).

### Run-time wiring `[CODE-VERIFIED]`

`run_cmd` (`commands.py:1830-1846`) builds the factory with `workers_requested=preflight_result.manifest.preflight.workers_requested`, catching `(TransportEnvError, ModelPoolTooSmallError)` and exiting `EXIT_INVALID` with the message on stderr. The resume path does the same at `:2442-2447`. `models=resolved_models` is passed from `spec.workers.models` but is **ignored for `openai_compat`** (wire models come only from the env pool).

---

## 3. `ModelPoolTooSmallError` — exact message + raise condition `[CODE-VERIFIED]`

**File:** `src/superclaude/cli/swarm/commands.py:589-609`. Subclass of `RuntimeError`.

**Constructor** (`:601-609`): `__init__(self, pool_size: int, workers_requested: int)`. Sets `self.pool_size` and `self.workers_requested`, then the exact message (f-string, `:605-608`):

```
T2 model pool has {pool_size} model(s) but the job requests {workers_requested} worker(s); each worker binds a distinct T2Model0N slot. Set at least {workers_requested} T2Model0N slot(s), or reduce workers.count to <= {pool_size}.
```

**Raise condition** (`commands.py:687-688`, inside the `openai_compat` factory branch):

```python
if workers_requested is not None and len(pool) < workers_requested:
    raise ModelPoolTooSmallError(len(pool), workers_requested)
```

Raised **eagerly at factory-build time, before any slot is dispatched**, when the live env pool (`len(pool)`, i.e. count of non-empty `T2Model0N` slots) is **strictly smaller** than `workers_requested`. `workers_requested=None` (e.g. direct unit construction) skips the check entirely.

### Why this guard exists vs INV-005 (the critical distinction) `[CODE-VERIFIED]`

The class docstring (`:589-599`) and the branch comment (`:684-686`) state it plainly: **INV-005 guards `workers.count` against `spec.workers.models` (lens placeholder ids), NOT the actual `T2Model0N` env pool the factory binds against.** So a job can pass preflight (INV-005 satisfied by enough *placeholders*) yet have fewer *real* `T2Model0N` env models than workers. Without this D2 guard, the extra slots would silently `pool[i % len]`-wrap and **reuse** a model. The guard fails loudly so the operator either adds `T2Model0N` slots or reduces `workers.count`.

- INV-005 (`preflight.py:117` `RULE_WORKERS_EXCEED_POOL = "inv005.workers_exceed_pool"`, `check_pool_size`): spec-placeholder pool, OQ-007 warn-with-defaults-vs-stop at preflight.
- INV-007 (`preflight.py:121` `RULE_EMPTY_POOL`, `check_empty_pool` `:929-957`): empty pool → `reason="env-missing"`, drives the `return-contract.yaml` failure contract.
- `ModelPoolTooSmallError` (`commands.py`): the env-pool-vs-workers gap INV-005 cannot see, checked at transport-factory build.

---

## 4. `StubTransport` — offline & deterministic `[CODE-VERIFIED]`

**File:** `src/superclaude/cli/swarm/transports/stub.py:70-183` (COMP-033 / FR-023). Backs FR-RH2.5 / NFR-RH2.4 (zero network I/O).

### No network, no clock (offline guarantee, `stub.py:33-42`)

- Module imports **only** `hashlib`, `threading`, `time`-free stdlib (actual imports `:57-59`: `hashlib`, `threading`, `typing`). No HTTP / DNS / socket / httpx. No clock dependency.
- `send()` deletes the `timeout` arg unused (`:143` `del timeout` — *"the stub has no I/O to budget against. Argument accepted to satisfy the Transport Protocol"*). No wall-clock latency introduced.
- `elapsed_ms` is a fixed constructor value (default `0`, `:97 / :113 / :153`) so timing assertions stay stable across hosts/runs.

### Determinism contract (`stub.py:11-31`)

Two modes, selected by the constructor `fixtures` arg:

**Default mode (`fixtures=None`, the recommended dispatch-test mode):** body is a **pure function of `(model_id, prompt)`** (`_next_body` `:179-182`):

```python
digest = hashlib.sha256(f"{self._model_id}\0{prompt}".encode("utf-8")).hexdigest()[:16]
return f"stub:{self._model_id}:{digest}\n"
```

Pure-function output sidesteps `ThreadPoolExecutor` scheduling ambiguity — byte-identical across runs **regardless of which thread runs the call** (`:20-24`). This satisfies the AC "Outputs are deterministic across runs given identical inputs."

**Fixtures mode (`fixtures=[...]` supplied):** serves `fixtures[counter % len(fixtures)]` under an internal `threading.Lock` (`_next_body` `:173-177`), counter incremented per call. Concurrent `send` calls receive distinct entries in **lock-acquisition order**; determinism here is per-(call-index, fixture-corpus), and the caller decides whether the slot↔fixture binding matters (`:26-31`).

### Outcome recording (`stub.py:122-159`)

Every `send` returns a `WorkerResult` with `status="success"`, `http_code=200`, `attempts=1`, `elapsed_ms` = constructor value, `model_id` = `model_label` = constructor `model_id` (default `"stub-model-00"`, `:67`). Body stashed on non-dataclass `result.body` (`:158`), mirroring `OpenAICompatTransport._build_result`.

**Constructor validation** (`:99-112`): empty `model_id` → `ValueError`; negative `elapsed_ms` → `ValueError`; empty `fixtures` sequence when supplied → `ValueError`. `__all__ = ["StubTransport"]`.

---

## 5. `OpenAICompatTransport` — the live `:4000/cli` proxy transport `[CODE-VERIFIED]`

**File:** `src/superclaude/cli/swarm/transports/openai_compat.py:205-437` (COMP-032 / FR-022). httpx driver for any OpenAI-compatible Chat Completions endpoint.

### How it reads base URL / key / model `[CODE-VERIFIED]`

The transport itself does **not** read env — it is constructed with explicit `base_url`, `api_key`, `model` (`:236-257`). The env contract is read by the module-level `read_env()` (`:159-202`), which the factory calls. Per instance:

- `self._base_url = base_url.rstrip("/")` (`:252`) — trailing slashes stripped so `.../cli` and `.../cli/` both work.
- `endpoint` property (`:264-267`): `f"{self._base_url}{_CHAT_COMPLETIONS_PATH}"` where `_CHAT_COMPLETIONS_PATH = "/chat/completions"` (`:122`). **The Chat-Completions suffix is appended at send time.**
- `send()` (`:284-382`): POSTs `{"model": self._model, "messages": [{"role":"user","content":prompt}], "temperature": self._temperature}` (default `temperature=0.2`, `:243`) with header `Authorization: Bearer <api_key>` (`:311-314`). `timeout` → `httpx.Timeout(float(effective_timeout))` (`:327`), default 180s when ≤0 (`:117`, `:310`).
- One instance is bound to ONE `model`; thread-safe via a shared `httpx.Client` (`:206-213`, `:257`). Tests inject a `client` (e.g. `httpx.MockTransport`) and retain close ownership (`:269-276`).

### Status mapping (`openai_compat.py:34-58`, code `:329-382`)

| status | condition |
|--------|-----------|
| `success` | HTTP 200 + parseable Chat-Completions shape + non-empty `choices[0].message.content` (`:368-382`, `_extract_content` `:409-436`). |
| `parse_error` | HTTP 200 but body not JSON / no `choices` / empty content (`:369-375`). |
| `proxy_error` | any non-200 (`:360-366`) OR non-timeout `httpx.RequestError` (connection refused, DNS, read/protocol error) routed through `_build_result` so **model identity is preserved** (F-P3-5, `:337-355`). |
| `timeout` | `httpx.TimeoutException` (`:329-336`); `http_code=None`, `elapsed_ms` = actual elapsed at raise. |

`_build_result` (`:384-407`) stamps `model_id` = `model_label` = `self._model`, `attempts=1`, and stashes `result.body`. **No response cache** (NFR-014 / AC-015, `:79-85`) — every `send` issues a fresh request.

### Routing guard (AC-010, `:67-77`)

Only addresses OpenAI-compatible Chat-Completions endpoints. The T2 proxy presents that surface backed by upstream providers; routing constraints live at proxy-config time. The `tests/swarm/` T03.20 grep test enforces that **no host-vendor URL or host-vendor model id appears in any transport-config source.**

---

## 6. The `~/.aienv` / T2 proxy preflight contract `[CODE-VERIFIED]`

### `read_env` — the eager env preflight `[CODE-VERIFIED]`

**File:** `src/superclaude/cli/swarm/transports/openai_compat.py:159-202`.

```python
def read_env(env: Optional[Mapping[str, str]] = None) -> TransportConfig:
```

Reads `env` (default `os.environ`, `:177`), strips each value:

- `base_url` ← `T2ProxyUrl` (`:178`)
- `api_key` ← `T2ProxyKey` (`:179`)
- `models` ← loops `index in range(1, T2_MODEL_MAX_SLOTS + 1)`, `T2Model0{index}`, appending non-empty stripped values (`:181-185`). **Dense** (empty slots skipped), **slot-ordered** (`T2Model01` first).

Builds `missing` list and raises `TransportEnvError(tuple(missing))` (`:187-196`) if `T2ProxyUrl` empty, `T2ProxyKey` empty, OR no `T2Model0N` resolves. Returns a `frozen=True` `TransportConfig(base_url, api_key, models)` (`:144-156`, `:198-202`).

`TransportEnvError` message (`:125-141`): `f"T2 proxy env contract incomplete; missing: {names}. Set {T2_PROXY_URL_ENV}, {T2_PROXY_KEY_ENV}, and at least one {T2_MODEL_ENV_PREFIX}1..{T2_MODEL_MAX_SLOTS} slot."` and carries `.missing` tuple. This structured failure is the Wave-0 anchor for the INV-007 empty-pool path (`:28-30`).

### The exact env-var constants `[CODE-VERIFIED]`

**File:** `src/superclaude/cli/swarm/config.py:48-63`:

```python
T2_PROXY_URL_ENV = "T2ProxyUrl"
T2_PROXY_KEY_ENV = "T2ProxyKey"
T2_MODEL_ENV_PREFIX = "T2Model0"     # concatenated with 1-based index → T2Model01..T2Model09
T2_MODEL_MAX_SLOTS = 9               # single-digit "0N" suffix ceiling
```

`SwarmConfig.from_env` (`config.py:100-138`) reads the same vars **non-raising** (missing → `None` / empty tuple, `:119-124`); the structured raise lives at dispatch/transport-build time (INV-007), keeping config construction total. `SwarmConfig.missing_t2_env_vars()` (`:151-166`) is the INV-007 helper listing absent vars before opening the live transport.

**Preflight needs:** `T2ProxyUrl`, `T2ProxyKey`, and `T2Model0N ≥ reviewer slots` — the `ModelPoolTooSmallError` D2 guard (§3) is exactly the "`T2Model0N` count ≥ `workers_requested`" enforcement.

### `~/.aienv` is loaded by the shell, not the swarm `[CODE-VERIFIED]`

`grep -rn "aienv" src/superclaude/cli/swarm/` → **no hits**. The swarm never opens or parses an `.aienv` file. The operator's `~/.aienv` is a shell-level convention (per memory `feedback_aienv_only_proxy_contract.md`) that exports `T2ProxyUrl` / `T2ProxyKey` / `T2Model01..NN` into the process environment; the swarm consumes them purely via `read_env`/`os.environ`.

### Proxy contract constraint (base + models ONLY) `[CODE-VERIFIED for the negative]`

`grep -rn ":4000|:8317|/v1|/cli"` over `src/superclaude/cli/swarm/` → **no `:4000`, no `:8317`, no `/cli`, no `/v1` literal anywhere in transport/config code** (only doc/comment hits in lens templates and a docstring *example* URL `https://proxy.example.com/v1`). The base URL is supplied **entirely** from `T2ProxyUrl`; the only suffix the code appends is `/chat/completions` (`openai_compat.py:122`). Per the project memory contract: use base `:4000/cli` and models `T2Model01..NN` **ONLY**; **NEVER** probe `:4000/v1` or `:8317`. The code respects this by hardcoding nothing — whatever `T2ProxyUrl` says (e.g. `…:4000/cli`) gets `/chat/completions` appended, and nothing else is constructed.

---

## Key Takeaways

1. **Transport Protocol** = one `@runtime_checkable` method `send(prompt: str, timeout: int) -> WorkerResult`. Verbatim prompt (no whitespace re-normalize, COMP-031); transport fills `http_code`/`attempts`/`elapsed_ms`; raw body stashed on non-dataclass `WorkerResult.body`. Default timeout 180s (NFR-010).
2. **Slot→model binding** is in `_resolve_run_transport_factory` (`commands.py:612-707`). For `openai_compat`: slot `i` → `pool[i % len(pool)]`, one cached `OpenAICompatTransport` per unique `T2Model0N`. The D2 pool guard ensures `len(pool) >= workers_requested`, so each slot gets a **distinct** model. For `stub`: one shared `StubTransport` for all slots.
3. **`ModelPoolTooSmallError`** (`commands.py:589-609`) raises **eagerly at factory build** iff `workers_requested is not None and len(pool) < workers_requested`. Exact message: `"T2 model pool has {pool_size} model(s) but the job requests {workers_requested} worker(s); each worker binds a distinct T2Model0N slot. Set at least {workers_requested} T2Model0N slot(s), or reduce workers.count to <= {pool_size}."` It catches the gap **INV-005 cannot** — INV-005 checks spec *placeholders*, this checks the live `T2Model0N` env pool.
4. **`StubTransport` stays offline + deterministic** via stdlib-only imports (`hashlib`/`threading`), `del timeout` (no I/O to budget), fixed `elapsed_ms` (default 0), and a pure-function body `stub:{model_id}:{sha256(model_id\0prompt)[:16]}\n` that is byte-identical across runs and thread schedules. This backs FR-RH2.5 / NFR-RH2.4 zero-network-I/O.
5. **Env contract** is read by `read_env` (`openai_compat.py:159-202`) from `os.environ`: `T2ProxyUrl` + `T2ProxyKey` + dense slot-ordered `T2Model01..T2Model09` (prefix `T2Model0`, max 9 slots; `config.py:51-63`). Missing → `TransportEnvError`. The swarm **never reads an `.aienv` file** — the shell exports those vars.
6. **Proxy contract:** base URL comes 100% from `T2ProxyUrl` (only `/chat/completions` appended); models only from `T2Model0N`. No `:4000`/`:8317`/`/v1`/`/cli` literal exists in transport/config code — the "`:4000/cli` only, never `:4000/v1` or `:8317`" rule is honoured by hardcoding nothing.

## Gaps and Questions

- **`[UNVERIFIED]` — Phase-1 single-model `_resolve_run_transport` vs factory:** `_resolve_run_transport` (`:510-586`) binds only `config.models[0]`. It is now only used as the stub-branch builder the factory delegates to; the live single-transport path appears superseded by the per-slot factory in `run_cmd`. Not a contradiction, but worth a callout if the TDD reasons about which path dispatches `openai_compat` (answer: the factory at `:1835`, not `_resolve_run_transport` directly).
- **`[UNVERIFIED]` — `~/.aienv` exact format/loader:** The actual `~/.aienv` file and the shell mechanism that loads it into `os.environ` are outside this codebase (a host/operator convention per memory). The swarm side is fully verified; the file-side contract is asserted from project memory, not code in this repo.
- **`[UNVERIFIED]` — FR-RH2.5 / NFR-RH2.4 spec text:** These requirement ids come from the task prompt; I verified the *behaviour* (zero network I/O, deterministic per-slot output) in `stub.py`, but did not open the ReflectHardening spec to confirm the exact FR/NFR wording maps to this transport. The code behaviour matches the described intent.

## Summary

The swarm transport layer is a thin `typing.Protocol` (`Transport.send(prompt, timeout) -> WorkerResult`) with two concrete drivers selected by `--transport`. `stub` (`StubTransport`) is a stdlib-only, network-free, byte-deterministic in-process driver (one shared instance across slots) backing CI / dry-run / zero-I/O requirements. `openai_compat` (`OpenAICompatTransport`) is the live httpx driver that POSTs to `<T2ProxyUrl>/chat/completions` with `Authorization: Bearer <T2ProxyKey>`, one instance per `T2Model0N` model. The heterogeneous fan-out lives in `_resolve_run_transport_factory`, which binds worker slot `i` to `pool[i % len(pool)]` and — guarded by `ModelPoolTooSmallError` (raised eagerly when `len(pool) < workers_requested`) — guarantees each slot a **distinct** model rather than silently wrapping/reusing. The `T2Model0N` env pool is read by `read_env` from `os.environ` (never from an `.aienv` file in-code), and the proxy contract is enforced by construction: the code hardcodes no host/port/path, so base `:4000/cli` + models `T2Model01..NN` are the only surface, and `:4000/v1` / `:8317` are never reachable.
