# Research 03 — Patterns & Conventions the implementation must follow

Status: Complete

Topic: Concrete patterns the new `t2_fallback` code must mirror. Repo root:
`/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback`. All paths below
are relative to that root. Evidence is file:line + symbol names.

---

## 1. Additive-kwarg threading precedent (`build_reflect_contract`)

**File:** `src/superclaude/cli/reflect/ensemble.py`

This is the exact template for the new `t2_fallback` kwarg: add a **defaulted
keyword-only** parameter to the builder signature, then emit it as a dict key in the
returned contract. The three precedent kwargs (`reviewer_isolation`,
`audit_tree_dirty`, `reviewer_grounding_root`) were added together for the L2
reviewer-isolation telemetry.

### Signature — keyword-only, appended after the pre-existing kwargs (lines 553-569)

```python
def build_reflect_contract(
    workers: list[WorkerResult],
    *,                                         # everything after is keyword-only
    swarm_merged_path: str | None = None,
    adversarial_convergence_score: float | None = None,
    adversarial_unavailable: bool = False,
    regression_present: bool = False,
    unauthorized_deviation_present: bool = False,
    needs_human_decision: bool = False,
    deviation_count_by_class: dict[str, int] | None = None,
    adversarial_report_path: str | None = None,
    reviewer_isolation: str = "disabled",       # <-- L2 additive kwargs
    audit_tree_dirty: bool = False,             # <-- defaulted CLEAN
    reviewer_grounding_root: str | None = None, # <-- defaulted None
    swarm_status: str = "success",
    adversarial_status: str | None = None,
) -> dict[str, Any] | None:
```

Exact defaults to mirror:
- `reviewer_isolation: str = "disabled"` (line 564)
- `audit_tree_dirty: bool = False` (line 565)
- `reviewer_grounding_root: str | None = None` (line 566)

### Returned dict entries (lines 635-637)

The kwargs are emitted verbatim as top-level contract keys, at the END of the returned
`dict` literal (`return {...}` starts at line 599):

```python
        "reviewer_isolation": reviewer_isolation,   # line 635
        "audit_tree_dirty": audit_tree_dirty,       # line 636
        "reviewer_grounding_root": reviewer_grounding_root,  # line 637
    }
```

### Governing docstring/comment conventions to reproduce
- The builder docstring (lines 570-578) explicitly states additive kwargs "default
  CLEAN so a direct call or a seam-less Tier-2 run still emits an all-zero,
  regression-free contract that routes PASS." Any new `t2_fallback` kwarg must default
  to the benign / no-op value for the same reason.
- Comment lines 631-634 document that reviewer-isolation fields are **pure telemetry,
  NOT verdict-bearing** — "the STOP happens in the runner before derive_verdict, so
  `audit_tree_dirty` is NOT registered in `_LOAD_BEARING_BOOL_FIELDS`." → Decide up
  front whether `t2_fallback` is telemetry-only or gated; if telemetry-only, do NOT add
  it to `_LOAD_BEARING_BOOL_FIELDS` and say so in a sibling comment.
- Load-bearing booleans are "forwarded as genuine Python `bool` (never `"true"`/`1`)"
  (docstring line 577). Match the type of the emitted value to its declared kwarg type.

**Template rule for the new kwarg:** add `t2_fallback...: <type> = <benign default>`
in the keyword-only block after the existing kwargs, then add a matching
`"t2_fallback...": t2_fallback...,` entry at the tail of the `return {...}` dict, with a
comment stating whether it is telemetry or verdict-bearing.

---

## 2. Dataclass field-ordering convention (defaulted fields appended last)

**File:** `src/superclaude/cli/reflect/models.py` — `ReflectConfig` (lines 57-109)

The dataclass mixes non-default and defaulted fields, and Python requires all defaulted
fields to come AFTER all non-defaulted ones. The codebase documents this explicitly and
new fields must be **appended at the end**:

- Lines 82-83 (comment):
  ```
  # Auto-fix evolution (D1/D3/D6): appended AFTER all existing non-default
  # fields to respect the dataclass field-ordering rule.
  ```
  Followed by `base_override: str | None` / `fix: bool` / `max_fix_iterations: int`
  (lines 84-86 — these are non-defaulted, placed before the defaulted block starts).
- The defaulted block begins at line 90 (`transport: str = "openai_compat"`) and each
  subsequent addition carries a `# §5.1` / `# L2` provenance comment: `reviewers: int =
  3` (93), `isolate_reviewers: bool = False` (100), `audit_tree_dirty: bool = False`
  (101), `reviewer_grounding_root: Path | None = None` (107), `reachability: bool =
  True` (109).
- Note `ReflectConfig` is a **plain `@dataclass`** (line 57), NOT frozen.
- A second dataclass at models.py line 117 (`@dataclass`) also carries
  `audit_tree_dirty: bool = False` (151) and `reviewer_grounding_root: str | None =
  None` (152) — the contract-side mirror of the same fields.

**SwarmConfig ordering confirmation** — `src/superclaude/cli/swarm/config.py` lines
91-98:
```python
    work_dir: Path            # non-default
    output_dir: Path          # non-default
    t2_proxy_url: Optional[str] = None   # defaulted block starts here
    t2_proxy_key: Optional[str] = None
    t2_models: tuple[str, ...] = ()
    dry_run: bool = False
    debug: bool = False
    log_level: str = "INFO"
```
Same rule: two non-defaulted fields first, then the defaulted block. A new
`SwarmConfig` field (e.g. a fallback tuple) must be appended to the END of the defaulted
block with a matching kwarg in `from_env` (see §3/§4) and an entry in the `Attributes:`
docstring (lines 74-88).

**Template rule:** append any new defaulted field at the tail of the defaulted block,
add a provenance comment, and if the dataclass has a `from_env`/constructor mirror,
thread the field there too and update the class docstring `Attributes:` list.

---

## 3. Collector generalization (`_collect_t2_models` → `_collect_models`)

**File:** `src/superclaude/cli/swarm/config.py`

Current concrete collector (lines 178-185):
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

Supporting constants (lines 57, 63):
- `T2_MODEL_ENV_PREFIX = "T2Model0"` (single trailing zero — the slot suffix is a single
  digit `0N`, so `f"{prefix}{index}"` yields `T2Model01`..`T2Model09`).
- `T2_MODEL_MAX_SLOTS = 9` (bounded because the documented suffix is a single digit).

The generalized shape requested — `_collect_models(env_map, prefix, max_slots)` — is a
mechanical parameterization: replace the two hard-coded references
(`T2_MODEL_ENV_PREFIX`, `T2_MODEL_MAX_SLOTS`) with the `prefix` / `max_slots`
parameters, keep the "skip empty/None slots so the tuple stays dense" body (the `if
value:` guard), and keep the `list → tuple` return. Preserve it as a `@staticmethod`.
The existing `_collect_t2_models` should then become a thin caller
`return cls._collect_models(env_map, T2_MODEL_ENV_PREFIX, T2_MODEL_MAX_SLOTS)` (or the
call site in `from_env` line 128 is updated), so the fallback ladder can call
`_collect_models(env_map, <FALLBACK_PREFIX>, <FALLBACK_MAX>)` with its own constant pair.

**Density / ceiling behaviors that tests already lock (must be preserved):**
- empty-string / missing slots are skipped, tuple stays dense —
  `tests/swarm/test_config.py::test_from_env_skips_empty_t2_model_slots` (100-106).
- only slots `1..MAX` are probed, `MAX+1` ignored —
  `test_from_env_respects_max_slot_ceiling` (109-117).
- These tests parameterize over `T2_MODEL_ENV_PREFIX` / `T2_MODEL_MAX_SLOTS` imported
  from the module, so a generalized helper keyed off the same constants keeps them green.

---

## 4. Frozen-dataclass constraints

**`SwarmConfig` IS frozen** — `src/superclaude/cli/swarm/config.py` line 66:
`@dataclass(frozen=True)`. The module docstring (lines 3-9) explains why: in-place
mutation would "silently break INV-001 / INV-016 (resolved-lens immutability)."

Adding a defaulted field to a frozen dataclass needs **nothing special at the dataclass
level** beyond field-ordering (§2) — frozen only blocks post-construction assignment,
not additional fields. BUT the frozen construction pattern imposes two mechanical
follow-throughs:
1. `SwarmConfig` is built via the `from_env` classmethod (lines 100-138), which resolves
   every field and passes them all to `cls(...)` in one shot (lines 129-138). A new
   field must be:
   - added as a `from_env` keyword parameter (if externally supplied) OR resolved
     internally (like `models = cls._collect_t2_models(env_map)` at line 128), and
   - included in the single `return cls(... new_field=... )` construction call.
2. Because the instance is immutable, you cannot stamp the field after construction; it
   must be computed before the `cls(...)` call. `_resolve_output_dir` (168-176) and
   `_collect_t2_models` (178-185) are the precedent static resolvers that run *before*
   construction — a fallback-ladder resolver should follow the same "resolve, then
   construct" shape.

Frozen probe tests to keep green: `tests/swarm/test_config.py`
`test_swarm_config_is_frozen_dataclass` (32-37) and `test_mutating_frozen_field_raises`
(40-48). `tests/swarm/test_models_frozen.py` documents the project's freeze policy
(Option C): **contract/source-of-truth records frozen, accumulator/state records
mutable** — `SwarmConfig` sits on the frozen side.

(Contrast: `ReflectConfig` in reflect/models.py is a plain non-frozen `@dataclass` and is
mutated in-flight — e.g. `runner.run()` sets `reviewer_grounding_root` AFTER a snapshot,
per the comment at models.py lines 102-107. If the new field lives on `ReflectConfig`,
no frozen constraint applies; if it lives on `SwarmConfig`, the resolve-then-construct
rule applies.)

---

## 5. Test conventions (stub injection, factories, patch targets)

### Swarm config tests — `tests/swarm/test_config.py`
- Pure-`env`-dict injection, no monkeypatch needed: build an explicit
  `env = { T2_PROXY_URL_ENV: ..., f"{T2_MODEL_ENV_PREFIX}1": ... }` and pass
  `SwarmConfig.from_env(work_dir=tmp_path, env=env)` (lines 56-79). Constants are
  imported from the module (lines 18-25) so tests never hard-code the literal env-var
  names — mirror this for any fallback prefix constant.
- `os.environ` fallback path uses `monkeypatch.setenv` + `monkeypatch.delenv(...,
  raising=False)` to null out sibling slots for determinism (lines 193-209).
- Frozen assertions read `cfg.__dataclass_params__.frozen` and expect
  `dataclasses.FrozenInstanceError` on assignment (lines 32-48).

### Reflect ensemble tests — `tests/cli/reflect/`

**Transport-factory injection (the `transport_for_slot` seam).** The ensemble driver
`run_tier2_ensemble(config, *, transport_for_slot=None, adversarial_score_fn=None, ...)`
(ensemble.py lines 171-179) takes a **per-slot transport factory** and an
**adversarial-score function** as injectable seams. Tests pass network-free stubs:
- `tests/cli/reflect/test_ensemble_stub_integration.py`:
  - `_distinct_stub(slot_index) -> StubTransport` returns
    `StubTransport(model_id=stub_model_id(slot_index))` — one distinct vendor per slot
    (lines 89-95). `stub_model_id` is the production helper (ensemble.py 116-119).
  - `_const_score(_paths, _out) -> AdversarialResult` returns a clean-default
    `AdversarialResult` so no adversarial `ClaudeProcess` launches (lines 43-60).
  - `_FailingTransport` is a hand-rolled class exposing `.model` property + `.send(prompt,
    timeout)` returning a `WorkerResult(status="proxy_error", http_code=None)` (lines
    63-86) — the pattern for simulating a proxy failure without network.
  - Driver invoked via helper `_run(config, transport_for_slot)` →
    `run_tier2_ensemble(config, transport_for_slot=..., adversarial_score_fn=_const_score)`
    then `parse_contract(config.contract_path)` + `derive_verdict(...)` (lines 108-122).
  - "No `ClaudeProcess` constructed" is asserted by patching it to a `_boom` that raises
    (`with patch.object(ensemble_mod, "ClaudeProcess", _boom)` lines 154-157) — the
    idiom for proving the credit-free path took no live launch.
- `tests/cli/reflect/test_ensemble_unit.py`:
  - Direct builder unit tests construct `WorkerResult(index=, status="success",
    model_id=)` lists and call `build_reflect_contract(workers, ...)` directly,
    asserting on the returned dict keys — see
    `test_u11_build_reflect_contract_threads_regression_fields` (lines 299-339). This is
    the exact test shape to add for a `t2_fallback` contract key: one call WITH the new
    kwarg asserting the emitted value, one call WITHOUT it asserting the benign default.
  - `resolve_config(str(temp_tasklist), depth=, model=, transport="stub", reviewers=)`
    is the config factory used across tests (stub integration `_config`, lines 98-105).
  - `runner`-level tests patch with `patch.object(runner_mod, "run_tier2_ensemble",
    autospec=True)` and `patch.object(runner_mod, "ClaudeProcess")` (lines 440, 465-466)
    — the seam boundary for asserting routing without executing the ensemble.

**Fixtures (`tests/cli/reflect/conftest.py`):**
- `temp_tasklist` (line 47) — writes a tasklist into `tmp_path` and returns its `Path`.
- `patch_git` (line 59) — monkeypatches git state so `resolve_config` is deterministic
  offline. Almost every ensemble test takes `(temp_tasklist, patch_git)`.
- `make_claude_process_stub` (line 99) — factory fixture that fabricates a
  `ClaudeProcess` returning a canned contract (used by the tests that DO want a stubbed
  child rather than the real fan-out).

**Model-routing / live-transport binding.** `resolve_t2_transport_factory(transport, *,
reviewers, models=None, env=None)` (ensemble.py 140-168) is where `stub` returns a
per-slot `StubTransport` factory and the live path delegates to the swarm factory
`_resolve_run_transport_factory(transport, models=..., env=..., workers_requested=...)`.
This `models=` / `env=` threading is the plausible injection point for a fallback ladder
(a fallback pool would be a second `models`-like list resolved from a fallback prefix).

**Golden/no-network guardrails already present:** `test_no_anthropic_routing.py`,
`test_no_claude_isms.py`, `test_no_forbidden_proxy_literals` (ensemble_unit
`test_u9`, line 241) — any new code must avoid hard-coded proxy literals / Anthropic
model ids in executable code; use the `~/.aienv` `T2Model0N` contract only.

---

## 6. Sync + lint discipline (CLAUDE.md + Makefile)

**Source-of-truth rule (CLAUDE.md).** Edit under `src/superclaude/` ONLY; `.claude/` is
gitignored sync-dev output (except `.claude/settings.json`). Never `git add .claude/...`;
if `git add` needs `-f` on a `.claude/` path, STOP. For this task the changed code lives
in `src/superclaude/cli/reflect/` and `src/superclaude/cli/swarm/` (pure Python, not
skill/agent `.md`), so **sync-dev is NOT triggered by these `.py` edits** — `make
sync-dev` only mirrors `src/superclaude/{skills,agents,commands,...}` → `.claude/`. Run
`make verify-sync` before committing only as the standard CI-parity check; it will pass
untouched because no synced component changed.

**Exact commands (Makefile):**
- `make sync-dev` → target at Makefile line 109 (copies `src/superclaude/{skills,agents,
  commands,hooks,...}` → `.claude/`). Not needed for `.py`-only changes but harmless.
- `make verify-sync` → target at Makefile line 166; on drift it prints
  "❌ Drift detected! Run 'make sync-dev' to fix" (line 351). Run before commit.
- `make lint` → target line 48; body (lines 48-50) is `lint: lint-architecture` +
  `uv run ruff check .`. **`make lint` runs `ruff check` ONLY — it does NOT run `ruff
  format --check`.**
- `make format` → target line 53, body `uv run ruff format .` (line 55).

**CI-format gap (memory `reference_make_lint_vs_ci_ruff_format`, confirmed by Makefile):**
CI separately runs `ruff format --check src/ tests/`, which `make lint` does not cover.
Green `make lint` ≠ green CI format. Before pushing, the new code + tests MUST pass:

```
uv run ruff format --check <changed .py files>
```

**Scope discipline (memory `reference_ruff_version_mismatch_worktree`):** do NOT run a
bare `uv run ruff format src/ tests/` in a worktree — the worktree `.venv` ruff can
differ from CI ruff and reformat ~100 unrelated files. Scope `ruff format --check` (and
any `ruff format`) to ONLY the files this task changes; if a broad run already fired,
`git checkout HEAD -- <out-of-scope files>` to revert the collateral reformats.

**Net checklist for the implementer:**
1. Edit only `src/superclaude/cli/reflect/*.py`, `src/superclaude/cli/swarm/*.py`, and
   `tests/**` — no `.claude/` staging.
2. `uv run ruff check <changed files>` (or `make lint`).
3. `uv run ruff format --check <changed files>` — scoped, not repo-wide.
4. `make verify-sync` (passes; no synced component touched).
5. `uv run pytest tests/cli/reflect tests/swarm -q` (or the specific new/affected tests).

---

## Summary of load-bearing conventions

1. **Additive kwarg = keyword-only param with benign default (appended after existing
   kwargs) + matching dict key at the tail of the `return {...}`**, with a comment
   stating telemetry-vs-verdict; benign default so seam-less/direct calls still PASS.
   Precedent: `build_reflect_contract` reviewer_isolation/audit_tree_dirty/
   reviewer_grounding_root (ensemble.py 564-566, 635-637).
2. **Dataclass defaulted fields append LAST** with provenance comments; confirmed for
   both `ReflectConfig` (plain, models.py 82-109) and frozen `SwarmConfig` (config.py
   91-98).
3. **`_collect_t2_models` (config.py 178-185)** generalizes to
   `_collect_models(env_map, prefix, max_slots)` by parameterizing the two constants;
   keep the dense-tuple `if value:` skip and `@staticmethod`.
4. **`SwarmConfig` is frozen** (config.py 66) → resolve fields with static helpers
   BEFORE the single `cls(...)` call in `from_env`; no post-construction stamping.
5. **Test seams:** inject `transport_for_slot` per-slot factories + `adversarial_score_fn`
   into `run_tier2_ensemble`; use `StubTransport(model_id=stub_model_id(i))`, hand-rolled
   `_FailingTransport`, `env`-dict `SwarmConfig.from_env`, `patch.object(...,
   "ClaudeProcess", _boom)` for no-launch proofs; `temp_tasklist`/`patch_git` fixtures;
   direct `build_reflect_contract(workers, ...)` dict-key assertions (with/without the new
   kwarg).
6. **Build/lint:** `.py`-only edits don't need sync-dev, but run `make verify-sync`.
   `make lint` = `ruff check` only; CI also runs `ruff format --check src/ tests/` — run
   `uv run ruff format --check <changed files>` **scoped** (worktree ruff drift can
   reformat ~100 files). Never stage `.claude/`.
