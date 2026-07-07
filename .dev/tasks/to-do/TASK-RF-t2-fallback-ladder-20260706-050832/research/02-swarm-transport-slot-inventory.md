# Research 02 — Swarm Transport & Slot Resolution Inventory

Status: Complete

Topic: File Inventory + Integration — swarm subsystem transport & slot resolution.
Scope: `src/superclaude/cli/swarm/{config.py, commands.py, transports/openai_compat.py, dispatch.py, models.py}`
Focus: EXACT current file:line groundings for the T1-slot family + fallback-transport seam, and the F1 `slot_index` root cause.

Driving design: `.dev/brainstorms/20260706-035624-reflect-t2-fallback-ladder/design.md` (§3, §4.3.1 F1, §7.1/§7.3 F3, §10 change map).

All paths relative to worktree root `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback`.
Line numbers verified by direct Read on 2026-07-06.

---

## 1. `swarm/config.py` — SwarmConfig + T2 slot family (§7.1 target)

File: `src/superclaude/cli/swarm/config.py` (186 lines total).

### Constants (the T2 pattern the new T1 family must mirror)
- `T2_PROXY_URL_ENV = "T2ProxyUrl"` — **L51**
- `T2_PROXY_KEY_ENV = "T2ProxyKey"` — **L52**
- `T2_MODEL_ENV_PREFIX = "T2Model0"` — **L57** (concatenated with a 1-based index; note the trailing `0`, so slot N → `T2Model0{N}`, single-digit suffix)
- `T2_MODEL_MAX_SLOTS = 9` — **L63**
- `__all__` export list — **L33-40** (exports the 4 constants above + `SwarmConfig` + `DEFAULT_OUTPUT_DIR`). New `T1_MODEL_ENV_PREFIX` / `T1_MODEL_MAX_SLOTS` constants must be appended here too.

### SwarmConfig dataclass
- Declared `@dataclass(frozen=True)` — **L66** (docstring L3-9 explicitly justifies `frozen=True` for INV-001/INV-016 resolved-lens immutability). **Confirmed FROZEN.**
- Field block — **L91-98**:
  - `work_dir: Path` (L91), `output_dir: Path` (L92) — required (no default)
  - `t2_proxy_url: Optional[str] = None` (L93)
  - `t2_proxy_key: Optional[str] = None` (L94)
  - `t2_models: tuple[str, ...] = ()` — **L95** ← the T2 pool field; the design's `t1_models: tuple = ()` is a parallel field. NOTE: `t2_models` is NOT the last field — three plain defaulted scalars follow it.
  - `dry_run: bool = False` (L96), `debug: bool = False` (L97), `log_level: str = "INFO"` (L98) ← **the last defaulted fields**. A new `t1_models: tuple[str, ...] = ()` field can be inserted right after L95 (adjacent to `t2_models`, keeping the pool fields grouped) — all fields have defaults so ordering among defaulted fields is unconstrained. Design §7.1 places it "parallel to T2".

### from_env classmethod
- `from_env(...)` — **L100-138** (keyword-only signature L101-110; body L111-138).
- Collector call site: `models = cls._collect_t2_models(env_map)` — **L128**; passed as `t2_models=models` in the return `cls(...)` at **L134**. Design §7.1 adds a second call `t1_models = cls._collect_models(env_map, T1_MODEL_ENV_PREFIX, T1_MODEL_MAX_SLOTS)` here.
- `env_map` resolution `env if env is not None else os.environ` — **L125**.

### _collect_t2_models (the method design §7.1 wants generalized → `_collect_models(env_map, prefix, max_slots)`)
- `@staticmethod def _collect_t2_models(env_map)` — **L178-185**. Full body:
  ```python
  @staticmethod
  def _collect_t2_models(env_map: Mapping[str, str]) -> tuple[str, ...]:
      models: list[str] = []
      for index in range(1, T2_MODEL_MAX_SLOTS + 1):
          value = env_map.get(f"{T2_MODEL_ENV_PREFIX}{index}")
          if value:
              models.append(value)
      return tuple(models)
  ```
  Range is `range(1, T2_MODEL_MAX_SLOTS + 1)` → 1-based, dense (skips empty). Generalizing to `_collect_models(env_map, prefix, max_slots)` is a mechanical prefix/max parameterization.

### Adjacent surface that also references the T2 constants (impact awareness, not in scope to change for T1 collection but worth noting)
- `missing_t2_env_vars()` — **L151-166** builds the INV-007 missing-var list from `T2_PROXY_URL_ENV`/`T2_PROXY_KEY_ENV`/`f"{T2_MODEL_ENV_PREFIX}1..{T2_MODEL_MAX_SLOTS}"` (L165). Not required by the design's T1 collection but is a sibling helper if a T1 missing-var surface is ever wanted.

---

## 2. `swarm/transports/openai_compat.py` — the F3 file (hard-coded to T2)

File: `src/superclaude/cli/swarm/transports/openai_compat.py` (445 lines total).

### Import block (design cites ~L98-103) — CONFIRMED exact
- **L98-103**:
  ```python
  from superclaude.cli.swarm.config import (
      T2_MODEL_ENV_PREFIX,
      T2_MODEL_MAX_SLOTS,
      T2_PROXY_KEY_ENV,
      T2_PROXY_URL_ENV,
  )
  ```
  Imports EXACTLY the four T2 constants — **hard-coded to T2, confirmed**. This is the seam that design §7.3 generalizes: `read_env_for_pool(model_prefix, max_slots, proxy_url_env, proxy_key_env)` accepts these as parameters instead of closing over the T2 module constants.
- `from superclaude.cli.swarm.models import WorkerResult` — **L104**.
- `__all__` — **L106-111**: exports `OpenAICompatTransport`, `TransportConfig`, `TransportEnvError`, `read_env`. The new `read_env_for_pool` should be added here.

### read_env full body (design cites ~L159-202) — CONFIRMED exact
- `def read_env(env: Optional[Mapping[str, str]] = None) -> TransportConfig:` — **L159** (docstring L160-176; body L177-202).
- Body highlights:
  - `env_map = env if env is not None else os.environ` — **L177**
  - `base_url = (env_map.get(T2_PROXY_URL_ENV) or "").strip()` — **L178**
  - `api_key = (env_map.get(T2_PROXY_KEY_ENV) or "").strip()` — **L179**
  - slot loop `for index in range(1, T2_MODEL_MAX_SLOTS + 1):` reading `f"{T2_MODEL_ENV_PREFIX}{index}"` — **L182-185** (same 1-based dense pattern as config `_collect_t2_models`)
  - `missing` accumulation for url/key/models — **L187-193** (models-missing token `f"{T2_MODEL_ENV_PREFIX}1..{T2_MODEL_MAX_SLOTS}"` at L193)
  - `if missing: raise TransportEnvError(tuple(missing))` — **L195-196**
  - `return TransportConfig(base_url=..., api_key=..., models=tuple(models))` — **L198-202**
- **Design §7.3 shape**: keep `read_env(env=None)` as a thin wrapper bound to the T2 constants that delegates to `read_env_for_pool(model_prefix=T2_MODEL_ENV_PREFIX, max_slots=T2_MODEL_MAX_SLOTS, proxy_url_env=T2_PROXY_URL_ENV, proxy_key_env=T2_PROXY_KEY_ENV, env=env)`. That keeps every existing caller (commands.py L677 import, and all tests) byte-valid.

### TransportEnvError (T2-specific message)
- `class TransportEnvError(RuntimeError)` — **L125-141**. `__init__(self, missing: tuple[str, ...])` — **L134-141**. Message is **T2-hardcoded** (L138-140):
  ```python
  f"T2 proxy env contract incomplete; missing: {names}. "
  f"Set {T2_PROXY_URL_ENV}, {T2_PROXY_KEY_ENV}, and at least "
  f"one {T2_MODEL_ENV_PREFIX}1..{T2_MODEL_MAX_SLOTS} slot."
  ```
  If the T1 path reuses the T2 proxy (design §7.3 decision — reuse T2 proxy url/key, vary only model id), this message stays accurate for the proxy portion but names `T2Model0N` for the slot portion. A pool-parameterized reader would ideally interpolate the actual prefix; low-risk since design §7.3 catches the raise into `terminal_reason: fallback_config_missing` rather than surfacing the text.

### TransportConfig shape (the return type read_env_for_pool must also produce)
- `@dataclass(frozen=True) class TransportConfig` — **L144-156**. Fields (**L154-156**):
  ```python
  base_url: str
  api_key: str
  models: tuple[str, ...]
  ```
  Frozen; no defaults (all three required). `read_env_for_pool` returns the same shape — no schema change needed. The `models` tuple is the pool the caller (commands.py) turns into the per-slot factory.

### Mental change-map entry (F3)
`openai_compat.py` is one of the **three** swarm files the fallback work touches (design §7.3 / §10 change map row): generalize `read_env → read_env_for_pool(model_prefix, max_slots, proxy_url_env, proxy_key_env)` + keep thin T2 wrapper. Risk = medium (shared env reader; every primary dispatch and test flows through it).

---

## 3. `swarm/commands.py` — `_resolve_run_transport_factory` + the pool[slot_index % len] map (F1 resolver)

File: `src/superclaude/cli/swarm/commands.py`.

- `class ModelPoolTooSmallError(RuntimeError)` — **L589-609**. `__init__(self, pool_size: int, workers_requested: int)` — **L601-609** (message is T2-worded: "T2 model pool has {pool_size} model(s)…", L604-608).
- `def _resolve_run_transport_factory(transport_kind, *, models=None, env=None, workers_requested=None) -> Callable[[int], Any]:` — **L612-707** (signature L612-618; docstring L619-668; body L669-707).
- Body, `openai_compat` branch:
  - `config = read_env(env)` (eager TransportEnvError) — **L680** (imports `OpenAICompatTransport, read_env` at L675-678)
  - `pool = [m for m in config.models if m]` — **L681**
  - **ModelPoolTooSmallError guard** (design cites ~L687-688) — **CONFIRMED L687-688**:
    ```python
    if workers_requested is not None and len(pool) < workers_requested:
        raise ModelPoolTooSmallError(len(pool), workers_requested)
    ```
  - `cache: dict[str, Any] = {}` — **L689**
  - inner `def _factory(slot_index: int) -> Any:` — **L691** (returns at L703)
  - **the positional mapping** (design cites ~L691-692) — **CONFIRMED L692**:
    ```python
    model = pool[slot_index % len(pool)]
    ```
  - per-model transport caching (L693-700), `return transport` (L701), `return _factory` (L703).
- `stub` branch: `shared = _resolve_run_transport("stub", ...)` then `return lambda _slot: shared` — **L670-673** (all slots share one stub, so slot_index is irrelevant for stub — matches design §7.2 note "stub pool already certifies").
- Call sites of the factory: run path `_resolve_run_transport_factory(...)` — **L1835** (guarded by `except (TransportEnvError, ModelPoolTooSmallError)` at L1840); resume path — **L2442** (guarded L2447).

**F1 relevance:** This is the resolver whose returned `_factory(slot_index)` maps `slot_index → pool[slot_index % len(pool)]`. Design §4.3.1 requires the fallback ladder to bypass this positional map and resolve by ladder-slot NAME, because a 1-worker fallback always feeds `slot_index == 0` (see §4 below). Design §7.3/§10 parameterizes this resolver on env prefix/pool (or adds `_resolve_fallback_transport`) so the `ModelPoolTooSmallError`/`TransportEnvError` guards are inherited by the T1 path. Risk = medium (shared with primary path).

---

## 4. `swarm/dispatch.py` — `dispatch_wave1` (the F1 root cause)

File: `src/superclaude/cli/swarm/dispatch.py`.

- `def dispatch_wave1(...)` — **L334** (signature block L334-407). Relevant params:
  - `transport_for_slot: Optional[Callable[[int], Transport]] = None` — **L338** (the per-slot factory; docstring L372-391 describes it as `(slot_index) -> Transport`).
- `workers_requested = preflight_result.manifest.preflight.workers_requested` — **L412** (guard `if workers_requested <= 0` at L413).
- **Factory call site** (design cites ~L453-459) — **CONFIRMED L444-460**. The closure `_make_callable(slot_index)` (L444) builds `_call()` which resolves the transport:
  ```python
  slot_transport = (
      transport_for_slot(slot_index)      # L454
      if transport_for_slot is not None
      else transport
  )
  return _run_worker(
      slot_index, slot_transport, prompt, effective_spec, logger   # L458-459
  )
  ```
  So `transport_for_slot` is invoked with the SAME integer that indexes the fan-out.
- **Task construction over `range(workers_requested)`** (design cites ~L464-471) — **CONFIRMED L464-472**:
  ```python
  tasks = [
      Task(
          id=f"worker-{index:02d}",
          description=f"swarm worker slot {index}",
          execute=_make_callable(index),
          depends_on=[],
      )
      for index in range(workers_requested)      # L471
  ]
  ```
  Re-keying loop also `for index in range(workers_requested)` — **L485** (synthesizes a `proxy_error` WorkerResult per missing slot, L490).

**F1 ROOT CAUSE — confirmed exactly:** `dispatch_wave1` indexes tasks `0..workers_requested-1` (L471) and hands each local `index` straight to `transport_for_slot(slot_index)` (L454). A one-worker fallback `WorkerSpec(count=1)` ⇒ `workers_requested == 1` ⇒ the ONLY task is `index == 0` ⇒ the factory is always called with `slot_index == 0`. Through `_resolve_run_transport_factory._factory` (commands.py L692) that maps to `pool[0 % len(pool)] == pool[0] == T1Model01`. So a naive second fallback attempt would re-select `pool[0]` (`T1Model01`) again and the `T1Model02 → pool[1]` escalation (design AC #2/#3/#4) would be **mechanically unreachable**. This is precisely why design §4.3.1 mandates a slot-NAME-keyed `make_fallback_slot_factory` (`ladder[i] → pool[i]`) owned by the controller, called with the slot NAME from `plan_next_attempt`, NOT the positional `slot_index` the one-worker dispatch emits.

---

## 5. `swarm/models.py` — WorkerStatus + WorkerResult fields (no change needed; confirm read surface)

File: `src/superclaude/cli/swarm/models.py`.

- **WorkerStatus Literal** — **L69** (CONFIRMED exact, matches design §3):
  ```python
  WorkerStatus = Literal["success", "timeout", "parse_error", "proxy_error"]
  ```
  Four values only. `parse_error` salvage-promotion to `success` is a Wave-2 normalize concern, not encoded on the type. Design §3 `FALLBACK_ELIGIBLE_STATUSES = {"timeout","proxy_error","parse_error"}` classifies over exactly these.
- **WorkerResult** — `@dataclass` (NOT frozen) at **L1019-1129**. Field block **L1110-1121**:
  ```python
  index: int = 0            # L1110  ← fallback ledger attempt_id "role:index" derives from this
  path: str = ""            # L1111
  raw_path: str = ""        # L1112
  meta_path: str = ""       # L1113
  final_path: str = ""      # L1114  ← the stamped post-normalize path fallback.py/ledger reads
  model_id: str = ""        # L1115  ← diversity axes (model-class + vendor) derive from this
  model_label: str = ""     # L1116
  bytes: int = 0            # L1117
  status: WorkerStatus = "success"   # L1118  ← quorum eligibility classifier
  http_code: Optional[int] = None    # L1119
  attempts: int = 1         # L1120
  elapsed_ms: int = 0       # L1121
  ```
  `__post_init__` validates `status ∈ WorkerStatus` — **L1123-1129**.
- **Confirmed:** all four fields the fallback controller/ledger read exist and are stable — `status` (L1118), `model_id` (L1115), `index` (L1110), `final_path` (L1114). Design §10 marks `swarm/models.py` as **no change** (deliberate, §3): no new WorkerStatus value, no new WorkerResult field. Confirmed correct — the four read fields already exist.

---

## Summary

- **config.py (§7.1):** `SwarmConfig` is `@dataclass(frozen=True)` (L66). T2 constants at L51/L52/L57/L63; `__all__` L33-40. `t2_models: tuple[str,...] = ()` at L95 (NOT the last field — `dry_run`/`debug`/`log_level` L96-98 follow). `from_env` L100-138 with collector call at L128 / return kwarg at L134. `_collect_t2_models` L178-185 (1-based dense loop) is the method to generalize to `_collect_models(env_map, prefix, max_slots)`.
- **openai_compat.py (F3):** import block L98-103 pulls EXACTLY the 4 T2 constants — hard-coded to T2, confirmed. `read_env` L159-202 (T2-only body). `TransportEnvError` L125-141 (T2-worded message). `TransportConfig` L144-156 (frozen; base_url/api_key/models, all required). This is the shared env reader to parameterize into `read_env_for_pool` + thin T2 wrapper (medium risk).
- **commands.py (F1 resolver):** `ModelPoolTooSmallError` L589-609; guard at **L687-688**. `_resolve_run_transport_factory` L612-707; inner `_factory(slot_index)` L691 with positional map `pool[slot_index % len(pool)]` at **L692**. Call sites L1835 (run) / L2442 (resume), both guarded on `(TransportEnvError, ModelPoolTooSmallError)`.
- **dispatch.py (F1 root):** `dispatch_wave1` L334; `transport_for_slot(slot_index)` call at **L454**; tasks built over `range(workers_requested)` at **L464-472** (L471). A 1-worker WorkerSpec ⇒ `workers_requested==1` ⇒ only `index==0` ⇒ factory always called with `slot_index==0` ⇒ `pool[0]` (`T1Model01`) every time. Root cause of why fallback MUST resolve by slot NAME (design §4.3.1), confirmed.
- **models.py:** `WorkerStatus` Literal L69 (4 values). `WorkerResult` (non-frozen dataclass) L1019-1129 carries `status` (L1118), `model_id` (L1115), `index` (L1110), `final_path` (L1114) — all four fallback-read fields present. No change needed (design §10), confirmed.

No Unverified items — every line number above was confirmed by direct Read of the current worktree tree on 2026-07-06.
