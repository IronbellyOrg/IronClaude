# R5 — Integration Points: Swarm Transport Layer + Proxy Env Contract (NFR-RH2.8 + Stub Proof)

- **Status:** Complete
- **Date:** 2026-06-20
- **Researcher:** R5 (Transports / Proxy Contract)
- **Scope:** `src/superclaude/cli/swarm/transports/{stub.py,openai_compat.py,__init__.py}`, `config.py` (env constants), `commands.py` (transport factory seam)
- **Worktree root:** `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3`
- **Method:** Full Read of all three transport files + targeted grep. All line anchors verified against the on-disk files at research time (zero-trust). TDD line-anchor claims from the task prompt are RE-VERIFIED below against actual current line numbers.

---

## 1. StubTransport — network-free deterministic transport (the FR-RH2.5 injection point)

**File:** `src/superclaude/cli/swarm/transports/stub.py`

### Class definition
- `class StubTransport:` defined at **stub.py:70**.
- `__all__ = ["StubTransport"]` at **stub.py:64**.
- Default model id constant `_DEFAULT_MODEL_ID = "stub-model-00"` at **stub.py:67**.

### EVERY import in stub.py (proves network-free)
From the import block **stub.py:55–61**:
- L55 `from __future__ import annotations`
- L57 `import hashlib`
- L58 `import threading`
- L59 `from typing import Optional, Sequence`
- L61 `from superclaude.cli.swarm.models import WorkerResult`

**VERDICT — NETWORK-FREE CONFIRMED.** Only stdlib `hashlib` + `threading` + `typing`, plus the in-package `WorkerResult` dataclass. **NO `httpx`, NO `socket`, NO `os`, NO `time`, NO DNS/HTTP.** (Note: the docstring at L36–38 claims it imports "hashlib + threading + time", but `time` is NOT actually imported — the body uses a fixed `elapsed_ms`, no clock call. The docstring slightly over-lists; the executable imports are network/clock-free either way. Flagged as a minor docstring-vs-code discrepancy.)

### `send` method — deterministic `success` WorkerResult
- `def send(self, prompt: str, timeout: int) -> WorkerResult:` at **stub.py:122**.
- `del timeout` (timeout intentionally unused — "the stub has no I/O to budget against") at **stub.py:143**.
- The returned `WorkerResult` is constructed at **stub.py:146–154** with fixed fields:
  - `status="success"` (L150)
  - `http_code=200` (L151)
  - `attempts=1` (L152)
  - `elapsed_ms=self._elapsed_ms` (L153) — `elapsed_ms` is the constructor-fixed value, default `0` (constructor default at **stub.py:97**, `elapsed_ms: int = 0`).
  - `model_id` / `model_label` both = `self._model_id` (L147–148).
- Raw body stashed on the non-dataclass attr `result.body = body` at **stub.py:158** (mirrors `openai_compat._build_result`).

### Body determinism (`_next_body`, stub.py:161–182)
- **Default mode** (no `fixtures`): body = pure function of `(model_id, prompt)`:
  `digest = sha256(f"{model_id}\0{prompt}").hexdigest()[:16]` (**stub.py:179–181**), returning `f"stub:{model_id}:{digest}\n"` (**stub.py:182**). Byte-deterministic across runs/threads.
- **Fixtures mode** (`fixtures` seq supplied): serves `fixtures[counter % len(fixtures)]` under `threading.Lock` (**stub.py:173–177**), counter advanced under lock so concurrent `send` calls get distinct entries in lock-acquisition order.

### Constructor (stub.py:92–115)
Signature: `__init__(self, model_id="stub-model-00", *, fixtures=None, elapsed_ms=0)`. Validates non-empty `model_id` (L99–100) and non-negative `elapsed_ms` (L101–104); rejects empty `fixtures` tuple (L109–112). Holds `self._lock = threading.Lock()` (L114) and `self._counter = 0` (L115).

**This is exactly what the FR-RH2.5 integration test injects** to exercise the parallel-dispatch / ensemble path with zero credits and zero network. The `success` outcome is unconditional — every `send` returns a parseable success WorkerResult.

---

## 2. `openai_compat.read_env` — the T2 proxy env contract

**File:** `src/superclaude/cli/swarm/transports/openai_compat.py`

- `def read_env(env: Optional[Mapping[str, str]] = None) -> TransportConfig:` at **openai_compat.py:159**. **TDD claim L159 — VERIFIED exact.**
- Env source: `env_map = env if env is not None else os.environ` at **openai_compat.py:177**. **Reads from `os.environ` (process env), NOT from any `.aienv` file in-code.** There is no file read, no dotenv parse, no path open anywhere in `openai_compat.py`. (`import os` at L91; `import json`, `import time`, `import httpx` are the only other imports — L90–96.)

### Env vars read (constants resolved from `config.py`)
`read_env` reads three logical groups via constants imported from `cli/swarm/config.py` (**openai_compat.py:98–103**):
- `T2_PROXY_URL_ENV` → literal **`"T2ProxyUrl"`** (`config.py:51`) — read at **openai_compat.py:178**, `.strip()`ed.
- `T2_PROXY_KEY_ENV` → literal **`"T2ProxyKey"`** (`config.py:52`) — read at **openai_compat.py:179**, `.strip()`ed.
- `T2_MODEL_ENV_PREFIX` → literal **`"T2Model0"`** (`config.py:57`) + index `1..T2_MODEL_MAX_SLOTS`, where `T2_MODEL_MAX_SLOTS = 9` (`config.py:63`). Loop at **openai_compat.py:182–185** iterates `range(1, 10)` building `f"{T2_MODEL_ENV_PREFIX}{index}"` = **`T2Model01` .. `T2Model09`** (dense — empty slots skipped, L184–185).
  - **NOTE on the prefix:** the prefix literal is `"T2Model0"` (trailing zero baked in) so `index=1` → `T2Model01`, `index=9` → `T2Model09`. This matches the `.aienv` `T2Model01..T2ModelNN` contract exactly. The `models` tuple is dense + ordered by slot index (L181–185, 198–202).

### `TransportEnvError` raise condition
- `class TransportEnvError(RuntimeError):` at **openai_compat.py:125**.
- Missing-list assembled at **openai_compat.py:187–193**: appends `T2_PROXY_URL_ENV` if base empty (L188–189), `T2_PROXY_KEY_ENV` if key empty (L190–191), and `f"{T2_MODEL_ENV_PREFIX}1..{T2_MODEL_MAX_SLOTS}"` if no model slot resolved (L192–193).
- Raise at **openai_compat.py:195–196**: `if missing: raise TransportEnvError(tuple(missing))`. **TDD claim L187–196 — VERIFIED exact** (the missing-assembly + raise span L187–196).
- Returns frozen `TransportConfig(base_url, api_key, models)` at **openai_compat.py:198–202**. `TransportConfig` is `@dataclass(frozen=True)` at **openai_compat.py:144–156** (fields `base_url`, `api_key`, `models: tuple[str, ...]`).

**Contract summary:** ALL of `T2ProxyUrl`, `T2ProxyKey`, and ≥1 `T2Model0N` slot are mandatory; any absent → `TransportEnvError` listing the missing names. Read exclusively from `os.environ` (or an injected mapping in tests).

---

## 3. Request URL construction + Auth header + send() status mapping

**File:** `src/superclaude/cli/swarm/transports/openai_compat.py`

### URL construction — base is 100% from `T2ProxyUrl`; only `/chat/completions` appended
- `_CHAT_COMPLETIONS_PATH = "/chat/completions"` at **openai_compat.py:122**. **TDD claim L122 — VERIFIED exact.**
- `base_url` stored as `self._base_url = base_url.rstrip("/")` at **openai_compat.py:252** (trailing slashes stripped; the base value flows from `config.base_url` → `read_env` → `T2ProxyUrl`, via the factory at `commands.py:579,696`).
- `endpoint` property: `return f"{self._base_url}{_CHAT_COMPLETIONS_PATH}"` at **openai_compat.py:265–267**. The POST targets `self.endpoint` at **openai_compat.py:324**.
- **NO host/port/scheme literal is hardcoded.** The entire base comes from the env value; only the constant suffix `/chat/completions` is appended. Confirms NFR-RH2.8's "base 100% from T2ProxyUrl".

### Authorization Bearer header
- Built in `send` at **openai_compat.py:311–314**: `headers = {"Authorization": f"Bearer {self._api_key}", "Content-Type": "application/json"}`. **TDD claim L311–314 — VERIFIED exact** (the `headers` dict literal spans L311–314). `self._api_key` = `config.api_key` = `T2ProxyKey`.

### send() status mapping (openai_compat.py:284–382)
- `def send(self, prompt: str, timeout: int) -> WorkerResult:` at **openai_compat.py:284**.
- Effective timeout: `timeout if timeout and timeout > 0 else _DEFAULT_TIMEOUT_SEC` (**L310**); applied as `httpx.Timeout(float(effective_timeout))` (**L327**).
- Outcome branches (**TDD claim L329–382 — VERIFIED**, branch order/anchors below):
  - **`timeout`** — `except httpx.TimeoutException:` at **L329–336** → `_build_result(status="timeout", http_code=None, body="")`, elapsed captured at raise point.
  - **`proxy_error` (network, non-timeout)** — `except httpx.RequestError as exc:` at **L337–355** → `_build_result(status="proxy_error", http_code=None, body=str(exc))` (conn-refused / DNS / read / protocol errors; preserves model identity rather than letting dispatch's `except Exception` fallback strip it — comment L338–348).
  - **`proxy_error` (non-200)** — `if response.status_code != 200:` at **L360–366** → `_build_result(status="proxy_error", http_code=response.status_code, body=body_text)`. Covers all 4xx/5xx.
  - **`parse_error`** — 200 but `_extract_content(...) is None` at **L368–375** → `_build_result(status="parse_error", http_code=200, body=body_text)`.
  - **`success`** — 200 + parseable `choices[0].message.content` non-empty at **L377–382** → `_build_result(status="success", http_code=200, body=content)`.
- `_extract_content` (**openai_compat.py:409–436**) returns `None` on: non-JSON (`JSONDecodeError`, L420–421), non-dict payload (L422–423), missing/empty `choices` (L424–425), non-dict first choice (L427–429), missing `message` (L430–432), or non-str/empty `content` (L433–435). `None` drives `parse_error`.
- `_build_result` (**openai_compat.py:384–407**) always stamps `model_id`/`model_label`=`self._model`, `attempts=1` (L399), `http_code`, `elapsed_ms`, `bytes`; stashes raw body on non-dataclass `result.body` (**L406**).

Mapping confirmed exactly as the prompt states: **200+parseable→success; 200-unparseable→parse_error; non-200→proxy_error; timeout→timeout; other-network→proxy_error.**

---

## 4. NFR-RH2.8 CRITICAL — forbidden-literal grep (host/port/path in executable code)

**Command run** (in `src/superclaude/cli/swarm/`):
```
grep -rn ':4000' transports/ commands.py
grep -rn ':8317' transports/ commands.py
grep -rn '/v1'   transports/ commands.py
grep -rn '/cli'  transports/ commands.py
```

**Results:**
- `:4000` → **NO MATCH** (zero occurrences, executable or docstring).
- `:8317` → **NO MATCH** (zero occurrences).
- `/cli` → **NO MATCH** (zero occurrences).
- `/v1` → **3 matches, ALL in docstrings, ZERO in executable code:**
  - `openai_compat.py:17` — module docstring example `https://proxy.example.com/v1`.
  - `openai_compat.py:217` — `__init__` docstring example `https://proxy.example.com/v1`.
  - `openai_compat.py:219` — `__init__` docstring `either .../v1 or .../v1/ work`.

**VERDICT — NFR-RH2.8 SATISFIED in current code.** No `:4000`, `:8317`, `/cli`, or `/v1` host/port/path literal exists in any **executable** statement in `transports/` or `commands.py`. The only `/v1` hits are illustrative docstring examples (TDD's stated exception). The request base is 100% sourced from `T2ProxyUrl` via `read_env`→`TransportConfig.base_url`→`OpenAICompatTransport.base_url` (`commands.py:579, 696`); the only appended literal is the constant `/chat/completions` (`openai_compat.py:122`), which is the OpenAI-compatible API suffix, not a host/port/`/v1`/`/cli` segment. **This grounds U9.**

> Caveat (scope): this grep covered exactly the prompt-specified surface (`transports/` + `commands.py`). A hardening test for U9 should assert the same over the whole `cli/swarm/` package executable code (R6's lane). The `.aienv`-contract proof is that the base never contains a hardcoded `:4000/cli` — it is *operator-supplied* via env; the code neither hardcodes nor validates the specific `/cli` suffix.

---

## 5. Retry / timeout matrix relevant to worker status (transport side)

The **transport itself records a single-attempt outcome** (`attempts=1` always, `openai_compat.py:399`); the retry policy wraps `send` externally (dispatch — R3's lane). What lives in `transports/`:

- **Per-call timeout default:** `_DEFAULT_TIMEOUT_SEC = 180` at **openai_compat.py:117** (mirrors `WorkerSpec.timeout_sec` / NFR-010). Used when caller passes `timeout<=0` (L310). **Confirms the 180s default lives in the transport.**
- **timeout → `status="timeout"`, no retry at transport level** (L329–336); dispatch decides retry. Module docstring (L54–58) states timeout is the per-call wall-clock budget.
- **5xx / 4xx → `proxy_error`** (any non-200, L360–366). The retry-once-on-5xx-with-backoff matrix is **NOT in the transport** — module docstring **openai_compat.py:50–53** explicitly says: *"The retry-once-on-5xx matrix is enforced by T03.09 `retry_policy` wrapping this send call; the transport itself records a single-attempt outcome (`attempts=1`)."* So "5xx → retry once / 2s backoff / then drop" and "4xx/conn-refused → no retry" live in **dispatch.py (R3's scope)**, not here.
- **conn-refused / DNS / network (non-timeout) → `proxy_error`, http_code=None** (L337–355); model identity preserved.

**Transport-side confirmation:** status mapping (which feeds the retry decision) is in `openai_compat.py` as above; the retry/backoff arithmetic itself is in dispatch.py (R3). Default per-call wall-clock budget `180s` is anchored in the transport at L117.

---

## 6. `Transport` base/protocol class + the method signature the factory binds per slot

**File:** `src/superclaude/cli/swarm/transports/__init__.py`

- `@runtime_checkable` (**__init__.py:51**) `class Transport(Protocol):` (**__init__.py:52**). A `typing.Protocol` (imported L46), NOT an inheritance base — implementations conform structurally. `@runtime_checkable` so dispatch can `isinstance(driver, Transport)` defensively (docstring L40–41).
- Single method: `def send(self, prompt: str, timeout: int) -> WorkerResult:` at **__init__.py:67**. `__all__ = ["Transport"]` at **__init__.py:87**.
- Both concrete drivers implement this exact signature: `StubTransport.send` (**stub.py:122**) and `OpenAICompatTransport.send` (**openai_compat.py:284**). Each also exposes a `model` read-only property (`stub.py:117–120`, `openai_compat.py:259–262`).

### Factory binding seam (in `commands.py` — overlaps R3's dispatch seam; documented here only at the construction site)
There is **NO `ensemble.py`** in `cli/swarm/` (files: commands, config, dispatch, __init__, logging_, merge, models, normalize, preflight, reduce, schema, state, tmux, tui). The "ensemble"/fan-out is `dispatch.py::dispatch_wave1` (R3). The transport-construction seam is two factory functions in `commands.py`:

- **`_resolve_run_transport`** (single transport) — `commands.py:566–586`:
  - `stub` → `StubTransport(model_id=...)` (**commands.py:566–570**).
  - `openai_compat` → `config = read_env(env)` then `OpenAICompatTransport(base_url=config.base_url, api_key=config.api_key, model=config.models[0])` (**commands.py:571–582**). Base 100% from env.
- **`_resolve_run_transport_factory`** (per-slot `(slot_index) -> Transport`) — `commands.py:612–707`:
  - `stub` → single shared `StubTransport` for all slots (**commands.py:670–673**, `lambda _slot: shared`).
  - `openai_compat` → `read_env(env)` eagerly (raises `TransportEnvError` before dispatch, **L680**); pool = dense `config.models` (**L681**); **D2 guard** `ModelPoolTooSmallError` if `len(pool) < workers_requested` (**L687–688**, class at L589–609); per-slot `_factory(slot_index)` binds `pool[slot_index % len(pool)]`, one `OpenAICompatTransport(base_url=config.base_url, api_key=config.api_key, model=model)` cached per unique model (**L691–701**). Base/key 100% from env; per-slot only the `model` varies.
- `dispatch_wave1` accepts `transport_for_slot: Optional[Callable[[int], Transport]]` at **dispatch.py:338** and invokes it per slot at **dispatch.py:454–455**. (Deep dispatch behaviour = R3.)

---

## SUMMARY (mandatory close-out items)

**(a) StubTransport import list — proves network-free:**
`from __future__ import annotations` (L55), `import hashlib` (L57), `import threading` (L58), `from typing import Optional, Sequence` (L59), `from superclaude.cli.swarm.models import WorkerResult` (L61). **No httpx, no socket, no os, no time, no DNS/HTTP — NETWORK-FREE CONFIRMED.** (Minor: docstring L36–38 mentions `time` but it is not actually imported.)

**(b) NFR-RH2.8 forbidden-literal grep result (`transports/` + `commands.py`, executable code):**
`:4000` = NONE, `:8317` = NONE, `/cli` = NONE, `/v1` = 3 hits but **all docstring examples** (`openai_compat.py:17,217,219`), **zero in executable code.** Base is 100% from `T2ProxyUrl`; only constant `/chat/completions` appended. **NFR-RH2.8 SATISFIED. Grounds U9.** (Recommend R6 widen the test grep to the full `cli/swarm/` package executable surface.)

**(c) `read_env` env-var contract:**
Reads from `os.environ` (or injected mapping), NOT an `.aienv` file in-code (`openai_compat.py:177`). Mandatory: `T2ProxyUrl` (config.py:51), `T2ProxyKey` (config.py:52), and ≥1 of `T2Model01..T2Model09` (prefix `"T2Model0"` config.py:57 × slots 1..9, `T2_MODEL_MAX_SLOTS=9` config.py:63). Models tuple is dense + slot-ordered. Any missing → `TransportEnvError(tuple(missing))` (`openai_compat.py:195–196`) listing the absent names. `read_env` at `openai_compat.py:159`.

**Cross-references (do NOT duplicate):** dispatch fan-out + retry/backoff arithmetic = R3 (dispatch.py); the FR-RH2.5 test itself + U9 grep test = R6; contract/return-shape = R2; reflect pkg = R1; lens = R4.

**Unverified / flags:**
- The TDD line anchors cited in the prompt (L159, L122, L187–196, L311–314, L329–382) all matched the current on-disk line numbers exactly — no drift at research time.
- Minor docstring-vs-code discrepancy: `stub.py:36–38` lists `time` among imports; `time` is not imported in stub.py (no functional impact — `elapsed_ms` is a fixed constructor value).
