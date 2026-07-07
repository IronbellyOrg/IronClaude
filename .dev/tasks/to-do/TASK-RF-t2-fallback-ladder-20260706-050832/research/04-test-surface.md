# Research 04 — Test & Verification Surface

Status: Complete
Topic: Ground the 9 new test files (design §9) against the CURRENT test layout.
Repo root: /config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback
Evidence: file:line + names. "Unverified" where not confirmable.

---

## TWO PATH GROUNDINGS FOR THE BUILDER (reconciled with the revised design)

> Correction (post-review): these were originally framed as "BLOCKING design errors."
> The design was patched in the same session — its revised §9 now already prescribes
> `tests/swarm/` and marks `test_contract.py` as non-existent. So the two items below are
> now CONFIRMATIONS of the current design, not conflicts. The destinations are authoritative.
> (The earlier draft mis-cited design line numbers; the current design §9 is self-consistent.)

### FINDING A — Swarm tests live at `tests/swarm/`, NOT `tests/cli/swarm/`. (Design §9 agrees.)

`tests/cli/swarm/` **does not exist.** All ~130 swarm tests live at
`tests/swarm/` (has its own `tests/swarm/conftest.py` and `tests/swarm/__init__.py`).

- `tests/cli/` contains only: `eval/`, `prd/`, `reflect/` subdirs + a few loose `test_*.py`
  (test_cli_registration.py, test_init_lite.py, test_install_*.py, test_tdd_extract_prompt.py,
  test_verify_sync_hooks.py). NO `swarm/` subdir.
- The real files the design wants to EXTEND are:
  - `tests/swarm/test_config.py`  (exists — 220-odd lines, SwarmConfig)
  - `tests/swarm/test_openai_compat.py`  (exists — read_env + transport)

**Builder action:** the two swarm test targets are `tests/swarm/test_config.py` and
`tests/swarm/test_openai_compat.py` (extend in place). The revised design §9 already
prescribes exactly this — no conflict. The reflect rows (`tests/cli/reflect/...`) ARE correct.

### FINDING B — `tests/cli/reflect/test_contract.py` does NOT exist. (Design §9 agrees.)

`ls tests/cli/reflect/test_contract.py` → **No such file.** There is no `test_contract.py`
anywhere under `tests/cli/reflect/`. The revised design §9 already marks it "does NOT currently
exist" and routes the verdict-unchanged regression into `test_verdict_mapping.py`. The nearest
existing surfaces that discharge that intent:

- `tests/cli/reflect/test_verdict_mapping.py` — direct `derive_verdict()` unit tests over
  fixture contracts (the §6 verdict/exit matrix). THIS is the natural home for the
  "t2_fallback=None default → verdict unchanged" additive-only regression + F6 first-match
  `degraded-tier1` assertion.
- `tests/cli/reflect/test_ensemble_stub_integration.py` — real fan-out contract emission;
  asserts `reviewer_count`, `merge_method`, `t2_model_class_diversity`.
- `tests/cli/reflect/test_contract_status_cli.py` — CLI-level contract/status wiring (13KB).

**Builder action:** either (a) create a NEW `tests/cli/reflect/test_contract.py` for the
additive-only regression, or (b) fold those assertions into `test_verdict_mapping.py`. Do NOT
assume a pre-existing `test_contract.py` to "keep green" — it isn't there. Recommend (a): a
small new file so the design's §9 filename maps 1:1, seeded from the `_load` helper pattern below.

---

## 1. Which §9 test files ALREADY EXIST

Glob of `tests/cli/reflect/` and `tests/swarm/` (2026-07-06):

| Design §9 target | Status | Actual path |
|---|---|---|
| test_fallback_classify.py | NEW | tests/cli/reflect/ (create) |
| test_fallback_plan.py | NEW | tests/cli/reflect/ (create) |
| test_fallback_select.py | NEW | tests/cli/reflect/ (create) |
| test_fallback_slot_factory.py | NEW | tests/cli/reflect/ (create) |
| test_contract_fallback_metadata.py | NEW | tests/cli/reflect/ (create) |
| test_contract.py "(existing)" | **MISSING** — see Finding B | tests/cli/reflect/ (create new OR fold into test_verdict_mapping.py) |
| test_ensemble_fallback_stub.py | NEW | tests/cli/reflect/ (create) |
| test_config.py "(swarm)" | **EXISTS** | tests/swarm/test_config.py (extend) — NOT tests/cli/swarm/ |
| test_openai_compat.py "(swarm)" | **EXISTS** | tests/swarm/test_openai_compat.py (extend) — NOT tests/cli/swarm/ |

No net-new symbol names exist yet anywhere: grep across `tests/` + `src/superclaude/cli` for
`t2_fallback`, `read_env_for_pool`, `make_fallback_slot_factory`, `T1Model`, `t1_models`
returns **zero hits** — all fallback surface is greenfield.

### Existing `tests/swarm/test_config.py` — what it asserts (extend, don't clobber)
Docstring "T01.09 — SwarmConfig dataclass + path resolution" (test_config.py:1). Imports from
`superclaude.cli.swarm.config`: `DEFAULT_OUTPUT_DIR, T2_MODEL_ENV_PREFIX, T2_MODEL_MAX_SLOTS,
T2_PROXY_KEY_ENV, T2_PROXY_URL_ENV, SwarmConfig` (test_config.py:19-26). Asserts:
- frozen dataclass + FrozenInstanceError on mutating `t2_models` (test_config.py:32-52)
- `SwarmConfig.from_env(work_dir, output_dir, env=dict)` happy path →
  `cfg.t2_models == ("vendor/model-a","b","c")`, `missing_t2_env_vars() == ()` (test_config.py:57-79)
- empty slot skip → dense tuple (test_config.py:95-105)
- max-slot ceiling `T2_MODEL_MAX_SLOTS` (test_config.py:108-119)
- missing-env totality (no raise) + `missing_t2_env_vars()` partial reporting (test_config.py:123-160)
- `resolve_path` absolute/relative/string (test_config.py:165-190)
- `os.environ` fallback when `env=None` (test_config.py:195-215)

**§9 delta (T1 pool):** new tests must mirror these with a `T1Model0N` collection and a
`t1_models` empty-tuple default. All existing tests read `env=` explicit dict via
`SwarmConfig.from_env(...)` — the fixture pattern to reuse is the plain `env={...}` dict; no
conftest fixture needed (uses only `tmp_path`, `monkeypatch`).

### Existing `tests/swarm/test_openai_compat.py` — what it asserts (extend, don't clobber)
Docstring "T03.05 — OpenAICompatTransport" (test_openai_compat.py:1). Imports
`OpenAICompatTransport, TransportConfig, TransportEnvError, read_env` from
`...transports.openai_compat`, plus `WorkerResult` and `Transport` (test_openai_compat.py:38-45).
Key patterns:
- `_make_transport(handler)` builds a real transport over `httpx.Client(transport=
  httpx.MockTransport(handler))` — **network-free HTTP via httpx.MockTransport** (test_openai_compat.py:73-80).
- send() outcome matrix: 200→success, 4xx/5xx→proxy_error, unparseable→parse_error,
  timeout→timeout, ConnectError→proxy_error preserving model identity (test_openai_compat.py:118-244).
- `read_env(env_dict)` happy path → `TransportConfig(base_url, api_key, models=("m-alpha",...))`,
  empty slot skipped, whitespace stripped (test_openai_compat.py:305-330).
- `read_env` missing-var → `TransportEnvError` with `.missing` listing `T2ProxyUrl`/`T2ProxyKey`/
  `T2Model0*` (test_openai_compat.py:333-360).
- env-gated live lane `@pytest.mark.skipif(not _LIVE_ENV_PRESENT)` reads `T2ProxyUrl/Key/Model01`
  from real `os.environ` (test_openai_compat.py:368-410).

**§9 delta (F3):** `read_env` current signature is `read_env(env: Optional[Mapping]=None)`
(openai_compat.py:159) — it hardcodes `T2_PROXY_URL_ENV`, `T2_PROXY_KEY_ENV`,
`T2_MODEL_ENV_PREFIX`, `T2_MODEL_MAX_SLOTS` (openai_compat.py:179-204). The F3 test must prove a
new `read_env_for_pool(model_prefix, max_slots, proxy_url_env, proxy_key_env)` reads a **T1** pool,
AND that the thin `read_env()` wrapper still passes every existing T2 assertion above (the whole
existing test body is the regression harness — do not delete it).

---

## 2. conftest fixtures

### `tests/cli/reflect/conftest.py` (188 lines) — reflect fixture set
`FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"` (conftest.py:17). Constants
`_FAKE_BASE` (40×'1'), `_FAKE_HEAD` (40×'2') (conftest.py:20-21).

| Fixture | Signature | Provides |
|---|---|---|
| `cli_runner` | `() -> CliRunner` | fresh Click `CliRunner` (conftest.py:40-43) |
| `temp_tasklist` | `(tmp_path) -> Path` | writes minimal MDTM tasklist w/ `start_commit=_FAKE_BASE` + `reflect_post: ""` stub; returns path (conftest.py:46-55) |
| `patch_git` | `(monkeypatch)` | stubs `superclaude.cli.reflect.config._git` → `_FAKE_HEAD` for `rev-parse HEAD`, `_FAKE_BASE` for `merge-base`; returns `_Git` class exposing `.base`/`.head` (conftest.py:58-80) |
| `patch_runner_env` | `(monkeypatch)` | stubs `runner._child_env` → `{}` and `runner.shutil.which` → `/usr/bin/claude` so binary preflight passes (conftest.py:83-95) |
| `make_claude_process_stub` | `() -> builder(fixture_name=None, rc=0, write_contract=True)` | Idiom-B factory: `.start()` no-op, `.wait()` writes `<output_dir>/return-contract.yaml` from `FIXTURES_DIR/<fixture_name>` then returns rc; `fixture_name=None`→no contract (verdict routes `blocked`) (conftest.py:98-138) |
| `make_claude_process_sequence` | `() -> builder(steps: list[tuple[str\|None,int]])` | SEQUENCE-aware factory for the bounded fix-loop; each `ClaudeProcess(**kwargs)` pops next `(fixture,rc)`; exhausted→`(None,0)` (conftest.py:141-188) |

Usage of stub factories: `patch("superclaude.cli.reflect.runner.ClaudeProcess", side_effect=factory)`
(conftest.py:105, 152). The factory keys on `kwargs["output_file"]` → `output_dir = output_file.parent`.

**For §9 fallback tests:** classify/plan/select/slot_factory are pure-unit (no subprocess) → they
need NO conftest fixture beyond maybe `temp_tasklist`/`patch_git` for a `resolve_config`. The
stub-integration file reuses `temp_tasklist` + `patch_git` (see §3). The
`make_claude_process_stub` fixture is deliberately NOT used by the real-fan-out ensemble tests.

### `tests/swarm/conftest.py` (79 lines) — marker registry only
Provides NO transport/config fixtures. It only pins the IMM/INV coverage maps and exposes two
session fixtures `imm_coverage_map` / `inv_coverage_map` (conftest.py:39-79). Swarm tests build
their own transports inline (httpx.MockTransport) and read `SwarmConfig.from_env(env=dict)`
directly. **The new swarm §9 tests will not depend on this conftest** — they use `tmp_path` +
explicit `env` dicts, matching test_config.py / test_openai_compat.py.

---

## 3. Stub/injection pattern — WorkerResult / transport_for_slot / dispatch / normalize

### Seam types (source)
- `TransportFactory = Callable[[int], Transport]` (ensemble.py:106) — a **slot_index → Transport** callable.
- `run_tier2_ensemble(config, *, transport_for_slot: TransportFactory | None = None,
  adversarial_score_fn=...)` (ensemble.py:171-175). When `transport_for_slot` is None it falls back
  to `resolve_t2_transport_factory(...)` (ensemble.py:201). This is THE injection seam for
  network-free ensemble tests.
- `WorkerStatus = Literal["success","timeout","parse_error","proxy_error"]` (swarm/models.py:69) —
  the 4-value enum the classify test keys off. `ResultStatus = Literal["success","partial","failed"]`
  (models.py:68) is the CONTRACT status, distinct from WorkerStatus.
- `WorkerResult` dataclass (swarm/models.py:1019-1129; corrected per cross-file check
  against research 02 §5) fields incl. `index` (L1110), `final_path` (L1114), `model_id`
  (L1115), `status` (L1118). `__post_init__` (models.py:1123-1129 — corrected from an earlier
  "1010-1012" mis-cite; research 02 §5 is authoritative) raises `ValueError` on a status
  outside the 4-value `WorkerStatus`. (Earlier docstring/line cites in this bullet were
  approximate; research 02's WorkerResult groundings are the authoritative ones.)
- swarm `dispatch_wave1(...)` (dispatch.py:334) and `normalize(...)` /
  `normalize_wave2(...)` (normalize.py:248, 508) are the real dispatch/normalize seams the §9
  `test_ensemble_fallback_stub.py` should inject stubs for (F2 stamp→normalize→`final_path`).

### Canonical example — `tests/cli/reflect/test_ensemble_stub_integration.py`
This is THE reference for building fake WorkerResults + injecting transports without network.
Docstring calls it "the LOAD-BEARING proof that the Tier-2 ensemble genuinely forms" over the
real `dispatch_wave1 → reduce_wave3 → derive_verdict` path (test_ensemble_stub_integration.py:1-14).

Two injection idioms co-exist there:
1. **StubTransport per slot** — `_distinct_stub(slot_index) -> StubTransport(model_id=
   stub_model_id(slot_index))` gives distinct, vendor-distinct models (test_ensemble_stub_integration.py:106-113).
   `StubTransport` (swarm/transports/stub.py) is a real in-process `Transport`: `send()` returns a
   deterministic `WorkerResult(status="success", http_code=200, attempts=1)` with body
   `stub:{model_id}:{sha256(prompt)[:16]}` — **no HTTP/DNS/socket** (stub.py:1-70 docstring).
2. **Hand-rolled failing transport** — `class _FailingTransport` with `.model` property and
   `send(prompt, timeout) -> WorkerResult(status="proxy_error", http_code=None, attempts=1)` then
   `result.body = ""` (test_ensemble_stub_integration.py:57-80). This is the pattern to copy for
   fabricating a specific failure without a fixture.

Driver helper `_run(config, transport_for_slot)`:
```
run_tier2_ensemble(config, transport_for_slot=transport_for_slot, adversarial_score_fn=_const_score)
contract = parse_contract(config.contract_path)
result  = derive_verdict(contract, expected_tier=2, allow_single_vendor=..., child_rc=0)
```
(test_ensemble_stub_integration.py:96-121). Config built via `resolve_config(str(temp_tasklist),
depth="deep", model="test-model", transport="stub", reviewers=N)` (test_ensemble_stub_integration.py:82-88).
Adversarial score is injected through the production `adversarial_score_fn` seam returning a const
`AdversarialResult(convergence_score=0.86, regression_present=False, ...)` — never by patching
`ClaudeProcess` (test_ensemble_stub_integration.py:40-70). I1 additionally asserts NO
`ClaudeProcess` is constructed by patching `ensemble_mod.ClaudeProcess` to a `_boom` raiser
(test_ensemble_stub_integration.py:150-160).

A per-slot **factory** variant (F1/F3-style routing) appears at test_ensemble_stub_integration.py:207-210:
```
def factory(slot_index: int):
    if slot_index == 2:
        return _FailingTransport("stub-model-02")
    ...
```
— exactly the shape `test_ensemble_fallback_stub.py` needs to inject dispatch/normalize/stamp stubs
and replay the §8 incident + counter-case.

`reviewer_count` is asserted ONLY in test_ensemble_stub_integration.py today (grep) — e.g.
`int(contract["reviewer_count"]) >= 2` (test_ensemble_stub_integration.py:163). The new
`test_contract_fallback_metadata.py` (`reviewer_count == contributing, not attempts`) extends this
witness family.

---

## 4. How verdict tests build contracts — `derive_verdict` + `_load`

`tests/cli/reflect/test_verdict_mapping.py`:
- Imports `from superclaude.cli.reflect.contract import derive_verdict` and
  `from superclaude.cli.reflect.models import Verdict` (test_verdict_mapping.py:11-12).
- Fixture-dir helper: `from .conftest import FIXTURES_DIR` then
  ```
  def _load(name: str) -> dict:
      return yaml.safe_load((FIXTURES_DIR / name).read_text(encoding="utf-8"))
  ```
  (test_verdict_mapping.py:14-18). **This is the `_load` helper + yaml fixture dir the §9
  contract/verdict tests should reuse.**
- Call shape: `derive_verdict(_load("pass.yaml"), expected_tier=2, allow_single_vendor=False,
  child_rc=0)` then assert `result.verdict is Verdict.PASS` and `result.verdict.exit_code == 0`
  (test_verdict_mapping.py:21-89). Exit codes asserted exactly: PASS=0, HALTED=10, DEGRADED=11
  (and BLOCKED=2 per module docstring first-match order blocked→degraded→halted→pass,
  test_verdict_mapping.py:1-6).

### Fixture YAML corpus — `tests/cli/reflect/fixtures/`
21 `*.yaml` contracts + `__init__.py` + `reviewer-personas/`. Directly relevant to §9:
- `pass.yaml`, `postfix_pass.yaml`, `halted_regression.yaml`
- `degraded_serena.yaml`, `degraded_tier1.yaml` (← F6 first-match `degraded-tier1`),
  `degraded_single_vendor.yaml`, `degraded_with_drift.yaml`
- `blocked_unknown_major.yaml`, `blocked_with_drift.yaml`
- `autofixable_drift.yaml`, `autofixable_drift_no_path.yaml`
- `human_required_needs_decision.yaml`, `tolerant_unknown_field.yaml`
- `reachability_*.yaml` (6 reachability-gate fixtures)

**§9 delta:** `test_contract_fallback_metadata.py` (and the new/`test_contract.py` additive-only
regression) will likely need one or two NEW fixture YAMLs carrying a `t2_fallback:` block plus a
counterpart with `t2_fallback: null` (the "None default → verdict unchanged" proof). Add them
under `tests/cli/reflect/fixtures/` and load via the `_load` helper. Assert NO proxy keys
(`T2ProxyUrl`/`T2ProxyKey`/`T1ProxyKey`) leak into the dumped contract YAML.

---

## 5. Pytest invocation + markers

- `[tool.pytest.ini_options]` (pyproject.toml:108): `testpaths = ["tests"]`,
  `addopts = ["-v","--strict-markers","--tb=short"]` (pyproject.toml:112-116). Because
  `--strict-markers` is on, any `@pytest.mark.<x>` must be registered in the `markers` list
  (pyproject.toml:118-146+).
- Relevant registered markers: `unit`, `integration`, and swarm-specific `imm`/`inv`
  (pyproject.toml:142-143). There is **no `reflect` or `swarm` marker** — those are DIRECTORY
  names, selected by path/`-k`, not by marker. The new fallback tests do NOT need a new marker
  (plain unit tests); if the builder wants a selector, `-k fallback` works on the filenames.
- **Scoped command confirmation:** the design's §"quick command" (design.md:714) is
  `uv run pytest tests/ -k "reflect or swarm"`. `-k` matches test-node IDs, which include the
  path segment — so `tests/cli/reflect/...` matches "reflect" and `tests/swarm/...` matches
  "swarm". ✅ CONFIRMED correct AS LONG AS the swarm tests land in `tests/swarm/` (Finding A) —
  they do. (If a file/test name also contains "reflect"/"swarm" it's still caught.) A tighter,
  path-explicit alternative that avoids `-k` name collisions:
  `uv run pytest tests/cli/reflect tests/swarm/test_config.py tests/swarm/test_openai_compat.py -q`.

---

## Builder cheat-sheet (paths + reuse)

- New reflect unit/contract/stub tests → `tests/cli/reflect/` (dir exists, conftest.py present).
- Swarm config/transport tests → **`tests/swarm/test_config.py` + `tests/swarm/test_openai_compat.py`**
  (EXTEND existing files; ignore §9's `tests/cli/swarm/` path).
- `test_contract.py "(existing)"` is a misnomer — CREATE it new under `tests/cli/reflect/` (or fold
  into `test_verdict_mapping.py`).
- Reuse `_load(name)` + `FIXTURES_DIR` from `test_verdict_mapping.py` / conftest for YAML contracts.
- Reuse `_distinct_stub` / `_FailingTransport` / `_run` / `resolve_config(..., transport="stub")`
  patterns from `test_ensemble_stub_integration.py` for the network-free fallback fan-out (F1/F2).
- Reuse `httpx.MockTransport(handler)` + `read_env(env_dict)` patterns from
  `test_openai_compat.py` for F3 `read_env_for_pool`.
- Reuse `SwarmConfig.from_env(work_dir, env={...})` + `T2_MODEL_ENV_PREFIX`/`T2_MODEL_MAX_SLOTS`
  constants from `test_config.py` for the `T1Model0N` / `t1_models` tests.
- All fallback symbols (`t2_fallback`, `read_env_for_pool`, `make_fallback_slot_factory`,
  `T1Model*`, `t1_models`) are greenfield — zero existing references to preserve.
