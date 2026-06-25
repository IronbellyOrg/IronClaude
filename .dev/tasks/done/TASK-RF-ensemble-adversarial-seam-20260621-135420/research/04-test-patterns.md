# Research 04 — Test & Verification: Ensemble Adversarial Seam Regression Test

Status: In Progress
Date: 2026-06-21
Topic: Existing ensemble tests + how to write the regression-asserting test
Scope: tests/cli/reflect/ (ensemble stub integration, contract, no-nesting-guard) + fixtures/stubs

## TL;DR for the builder

- The home for the new test is `tests/cli/reflect/test_ensemble_stub_integration.py` (the I1-I11 family). Add an **I12** that mirrors `_run` / `_distinct_stub` exactly but injects an `adversarial_score_fn` that reports a regression, then asserts `derive_verdict(...).verdict is not Verdict.PASS` (ideally `is Verdict.HALTED`, `exit_code == 10`, `reason == "regression"`).
- **The core gap (verified):** `build_reflect_contract` (`ensemble.py:377-407`) HARDCODES `"regression_present": False` and `deviation_count_by_class.regression: 0`. The seam `AdversarialScoreFn = Callable[[list[str], Path], float | None]` (`ensemble.py:72`) only returns a **convergence float** — it carries NO deviation/regression/human-decision signal. So today there is **no path** by which a regression found by the adversarial reviewer reaches the contract. A regression-reporting seam therefore needs to return an **object/dict** carrying `regression_present=True` (etc.), and `build_reflect_contract` must thread those fields through instead of the hardcoded `False`/`0`.
- Pytest invocation: `uv run pytest tests/cli/reflect/test_ensemble_stub_integration.py -q` (12 tests, all green; ~0.24s, network-free). No custom markers on these tests.
- NFR-7 guard (`test_no_nesting_guard.py`) forbids `Task(`, `subagent`, `import anthropic`, `from anthropic`, raw `subprocess.run(`/`Popen(` and `import subprocess` in `ensemble.py`; requires `ClaudeProcess` literal present. New code/test must stay clean of those tokens.

---

## 1. The existing ensemble integration tests (I1-I11)

File: `tests/cli/reflect/test_ensemble_stub_integration.py` (452 lines). These are the
"LOAD-BEARING proof that the Tier-2 ensemble genuinely forms" (docstring, lines 1-19).
Each test drives the REAL `run_tier2_ensemble` -> `dispatch_wave1` -> `reduce_wave3` ->
`derive_verdict` path with a network-free `StubTransport` per slot. The conftest
canned-fixture `ClaudeProcess` stub is deliberately NOT used; the only injected value is
the adversarial convergence score, via the production `adversarial_score_fn` seam.

### 1a. The injected seam — how a test currently passes a FLOAT (the gap)

`test_ensemble_stub_integration.py:34-41`:

```python
_FIXED_SCORE = 0.86

def _const_score(_paths: list[str], _out: Path) -> float:
    return _FIXED_SCORE
```

This is the seam injection. The signature `(_paths: list[str], _out: Path) -> float`
matches `AdversarialScoreFn = Callable[[list[str], Path], float | None]`
(`ensemble.py:72`). It returns ONLY a float — there is no field for regression /
deviation / human-decision. THIS is the minimal-change pivot: a regression-reporting
seam must return a richer object/dict (e.g. `AdversarialScore(score=..., regression_present=True, ...)`),
and `build_reflect_contract` must consume those new fields.

### 1b. How tests inject the seam + read config.contract_path + call derive_verdict

The shared driver helper (`test_ensemble_stub_integration.py:88-102`) is the EXACT
pattern the new test should reuse:

```python
def _run(config, transport_for_slot) -> tuple[dict | None, object]:
    """Drive the real ensemble + derive_verdict; return (contract, ReflectResult)."""
    run_tier2_ensemble(
        config,
        transport_for_slot=transport_for_slot,
        adversarial_score_fn=_const_score,           # <-- the seam injection point
    )
    contract = parse_contract(config.contract_path)  # <-- reads config.contract_path
    result = derive_verdict(
        contract,
        expected_tier=2,
        allow_single_vendor=config.allow_single_vendor,
        child_rc=0,
    )
    return contract, result
```

Config builder (`test_ensemble_stub_integration.py:78-85`):

```python
def _config(temp_tasklist: Path, *, reviewers: int = 3) -> object:
    return resolve_config(
        str(temp_tasklist),
        depth="deep",          # required so expected_tier resolves to 2 (quick floors to standard)
        model="test-model",
        transport="stub",
        reviewers=reviewers,
    )
```

### 1c. The canonical positive/negative assertion convention

`_i1_positive_holds(contract)` (lines 105-118) is the NFR-RH2.3 falsifier reference set:
`tier_reached == 2`, `merge_method != "single-reviewer-fallback"`, `reviewer_count >= 2`,
`t2_model_class_diversity == "full"`. The I1 positive test asserts it is `True`; every
negative witness (I2/I4/I5/I6) asserts it is `False`.

The PASS assertion shape (I1, lines 140-151) — what the new regression test must INVERT:

```python
assert contract["status"] == "success"
assert result.verdict is Verdict.PASS
assert result.verdict.exit_code == 0
```

The DEGRADED negative shape (I4, lines 222-228) — the closest existing template for a
"derive_verdict does NOT return pass" assertion:

```python
assert result.verdict is Verdict.DEGRADED
assert result.verdict.exit_code == 11
assert _i1_positive_holds(contract) is False
```

The new test will instead assert `Verdict.HALTED` / `exit_code == 10` / `reason == "regression"`
(see Section 5).

---

## 2. Stub transport / fixture setup (cheap 2-reviewer ensemble)

### 2a. StubTransport + the production model-id scheme

`test_ensemble_stub_integration.py:69-76`:

```python
def _distinct_stub(slot_index: int) -> StubTransport:
    """One StubTransport per slot with a DISTINCT, vendor-distinct model_id."""
    return StubTransport(model_id=stub_model_id(slot_index))
```

- `StubTransport` imported from `superclaude.cli.swarm.transports.stub`
  (`test_ensemble_stub_integration.py:32`).
- `stub_model_id(slot_index)` imported from `superclaude.cli.reflect.ensemble`
  (line 29); it returns `f"{vendor}-stub-{slot_index:02d}"` over the
  `_STUB_VENDOR_POOL = ("qwen", "deepseek", "gpt", "mistral")` (`ensemble.py:78-84`),
  so distinct slots are both model-class- AND vendor-distinct (PASS-eligible).

`transport_for_slot` is the factory passed into `run_tier2_ensemble`
(type `TransportFactory = Callable[[int], Transport]`, `ensemble.py:71`). For a
2-reviewer-survives ensemble, the simplest cheap config is `reviewers=3` with
`_distinct_stub` (3 distinct survivors -> `reviewer_count==3`, diversity `full`,
tier 2). That is exactly what I1 / I7 / I8 / I9 use and is the cheapest "healthy
ensemble" to layer a regression-only signal onto.

### 2b. The failing-transport helper (only needed for M-reduction tests)

`_FailingTransport` (`test_ensemble_stub_integration.py:43-67`) returns a
`WorkerResult(status="proxy_error", http_code=None)` so `reduce_wave3` drops it from M.
The new regression test does NOT need this — it wants a healthy 2+ survivor ensemble
(so the contract WOULD pass on diversity grounds) and the regression must come solely
from the seam. Use `_distinct_stub` for all slots.

### 2c. WorkerResult construction (unit-level alternative)

`WorkerResult` imported from `superclaude.cli.swarm.models`
(`test_ensemble_stub_integration.py:31`). Unit tests construct it directly, e.g.
`test_ensemble_unit.py:159-162`:

```python
WorkerResult(index=0, status="success", model_id="model-a")
```

`build_reflect_contract(workers, adversarial_convergence_score=0.86)` is called
directly at `test_ensemble_unit.py:170`. A unit-level companion test (asserting the
contract gets `regression_present=True` when the seam reports it) could live in
`test_ensemble_unit.py`, but the HEADLINE acceptance (derive_verdict != pass) belongs
in the integration file because it exercises the full `run_tier2_ensemble` ->
`parse_contract` -> `derive_verdict` path.

### 2d. Required fixtures: `temp_tasklist`, `patch_git`

Both from `tests/cli/reflect/conftest.py`:
- `temp_tasklist` (conftest.py:46-55) writes a minimal MDTM tasklist with
  `start_commit` set so `<BASE>` resolves without git.
- `patch_git` (conftest.py:58-80) stubs `config._git` so `resolve_config` works
  without a real repo.

Every integration test takes `(temp_tasklist, patch_git)`. The new test must too.
The conftest `make_claude_process_stub` / `make_claude_process_sequence` factories are
NOT used by the stub-integration file (they are the canned-contract path the
integration suite deliberately avoids).

---

## 3. How derive_verdict routes a regression (the assertion target)

`contract.py:130-246`, ordering `blocked -> degraded -> halted -> pass` (first-match-wins).
For a HEALTHY ensemble carrying a regression, the relevant routing is:

- BLOCKED rows (child_rc != 0, contract None, bad version, malformed bool) — NOT hit
  if the seam threads a real `True` bool and the contract is otherwise well-formed.
  **Important:** `regression_present` is in `_LOAD_BEARING_BOOL_FIELDS`
  (`contract.py:47-57`); a present value that is not a real Python `bool` routes
  BLOCKED `malformed-contract-boolean` (lines 200-209). So the seam MUST set an actual
  `True`, not `"true"`/`1`.
- DEGRADED — `_degraded_reason` (lines 249-304). A healthy 2-distinct-survivor stub run
  with a non-None convergence score returns `None` here (no degradation). Good — the
  regression must be the FIRST non-degraded trigger so it does not get masked by a
  degrade.
- HALTED — `_halted_reason` (lines 307-328). `contract.get("regression_present") is True`
  -> returns `"regression"` (`contract.py:315-316`). ALSO
  `deviations["regression"] > 0` -> `"regression"` (lines 323-324). Either path yields
  the `regression` slug.
- PASS — only reached if status success AND tier matches AND no halt. The regression
  must pre-empt this.

So the assertion target: `result.verdict is Verdict.HALTED`, `result.reason == "regression"`,
`result.verdict.exit_code == 10`. Verdict exit codes (`models.py:39-48`):
PASS=0, HALTED=10, DEGRADED=11, BLOCKED=2.

### The build_reflect_contract gap (root cause for the task)

`ensemble.py:377-407` — the returned dict hardcodes (lines 385-390, 401-404):

```python
"deviation_count_by_class": {"authorized": 0, "necessary": 0, "drift": 0, "regression": 0},
...
"regression_present": False,
"unauthorized_deviation_present": False,
"needs_human_decision": False,
"user_decision_required": False,
```

The seam result (`adversarial_score_fn`, called at `ensemble.py:229-232`) feeds ONLY
`adversarial_convergence_score` into `build_reflect_contract` (line 237). Therefore:
no matter what the adversarial reviewer finds, `regression_present` stays `False` and
`deviation_count_by_class.regression` stays `0`, and `derive_verdict` can NEVER route
`regression` from an ensemble run. **The new test, written against TODAY's code, will
FAIL (it will see Verdict.PASS) — which is the point: it is the red test that proves
the gap.** It goes green once `AdversarialScoreFn` is widened to carry the regression
signal and `build_reflect_contract` threads it through.

The reference fixture for the target contract SHAPE is
`tests/cli/reflect/fixtures/halted_regression.yaml`, which sets
`regression_present: true` + `deviation_count_by_class.regression: 1` + `status: partial`
and routes HALTED. (That fixture is consumed by the canned-contract verdict-mapping
tests, not the live ensemble path; it documents the field shape the widened seam should
produce.)

---

## 4. NFR-7 no-nesting guard — what the new code/test must avoid

File: `tests/cli/reflect/test_no_nesting_guard.py`. Two tests scan `ensemble.py`
(`_ENSEMBLE_SRC`, line 31):

- `test_layer_b_wrapper_module_has_no_agent_imports` (lines 106-124): for both
  `runner.py` and `ensemble.py`, asserts `"ClaudeProcess"` IS present and that NONE of
  `("import anthropic", "from anthropic", "subagent", "Task(")` appear (lines 121-124).
- `test_ensemble_launches_only_via_claudeprocess_no_raw_subprocess` (lines 167-179):
  asserts `ensemble.py` has no `subprocess.run(`/`Popen(` call
  (`_RAW_SUBPROCESS_CALL_RE`, line 49) and no `import subprocess` / `from subprocess`
  (`_IMPORT_SUBPROCESS_RE`, lines 50-52).

Also package-wide over `cli/reflect/*.py` (excluding `__init__.py`):
- `test_no_sprint_or_roadmap_import_anywhere_in_reflect_pkg` (lines 127-135): no
  `from/import ...sprint` or `...roadmap`.
- `test_no_async_await_anywhere_in_reflect_pkg` (lines 138-147): no `async def` /
  `await ` CODE (anchored regexes, docstring prose is fine).

Implication for the widened seam: keep the new `AdversarialScoreFn` return type a plain
dataclass/dict in `ensemble.py` (or `models.py`); do NOT introduce any agent-surface
import, raw subprocess, or async. The test file itself must not contain `Task(` or
`subagent` literals (it won't if it just injects a Python callable returning a value).

---

## 5. Concrete sketch of the new test (I12) — prose, not final code

Add to `tests/cli/reflect/test_ensemble_stub_integration.py`, after I11 (line 452).
Mirror the I4 negative-witness shape exactly, swapping the degradation cause for a
seam-reported regression on an OTHERWISE-HEALTHY ensemble.

**Seam stub** (parallel to `_const_score`, lines 39-41). Its return type depends on R2's
widened `AdversarialScoreFn` contract — coordinate with R2's design. Two likely shapes:

- If the widened seam returns a small dataclass/dict, e.g.
  `AdversarialScore(convergence_score=0.86, regression_present=True, deviation_counts={"regression": 1, ...})`:
  ```python
  def _regression_score(_paths, _out):
      return AdversarialScore(convergence_score=_FIXED_SCORE, regression_present=True, ...)
  ```
- Keep `convergence_score` non-None (0.86 like `_FIXED_SCORE`) so the `null-convergence`
  DEGRADED trigger (`contract.py:283-285`) does NOT fire and mask the regression. The
  regression must be the first NON-degraded trigger.

**Body** (mirrors `_run` at lines 88-102 with the regression seam):

```python
def test_i12_seam_regression_does_not_pass(temp_tasklist, patch_git) -> None:
    config = _config(temp_tasklist, reviewers=3)          # 3 distinct survivors -> healthy, diversity full
    run_tier2_ensemble(
        config,
        transport_for_slot=_distinct_stub,                # all-healthy, so no degrade
        adversarial_score_fn=_regression_score,           # seam reports a regression
    )
    contract = parse_contract(config.contract_path)
    result = derive_verdict(
        contract, expected_tier=2,
        allow_single_vendor=config.allow_single_vendor, child_rc=0,
    )

    # HEADLINE ACCEPTANCE: a seam-reported regression is NOT a pass.
    assert result.verdict is not Verdict.PASS
    # Sharper: it routes the HALTED/regression slug + exit 10.
    assert result.verdict is Verdict.HALTED
    assert result.verdict.exit_code == 10
    assert result.reason == "regression"
    # Provenance: the regression signal actually reached the contract (closes the gap).
    assert contract is not None
    assert contract["regression_present"] is True          # was hardcoded False before the fix
    # Healthy-ensemble guard: the verdict is NOT a masking DEGRADED.
    assert contract["t2_model_class_diversity"] == "full"
    assert result.verdict is not Verdict.DEGRADED
```

**Red-then-green note for the builder:** Against TODAY's `build_reflect_contract`
(`regression_present` hardcoded `False`), this test asserts `is not Verdict.PASS` and
will FAIL with `result.verdict is Verdict.PASS` — proving the gap. It turns green only
after the seam is widened AND `build_reflect_contract` threads the regression fields
through. If the task wants the headline test to be the SOLE new integration test, the
single load-bearing line is `assert result.verdict is not Verdict.PASS`; the sharper
HALTED/exit-10/reason assertions document the intended routing.

**Optional unit companion** (in `test_ensemble_unit.py`, mirroring U5 at lines 157-175):
construct `WorkerResult`s directly, call the WIDENED `build_reflect_contract(..., <regression args>)`,
and assert the returned dict has `regression_present is True` and
`deviation_count_by_class["regression"] == 1`. This isolates the contract-builder change
from the full fan-out path.

---

## 6. Pytest invocation (verified)

```bash
uv run pytest tests/cli/reflect/test_ensemble_stub_integration.py -q
```

Confirmed run on this worktree: **12 passed in 0.24s** (network-free, no markers).
For the full reflect suite: `uv run pytest tests/cli/reflect/ -q`. To run just the new
test by name once added: `uv run pytest tests/cli/reflect/test_ensemble_stub_integration.py -k i12 -q`.
No pytest markers are applied to any test in this file (no `@pytest.mark.*` decorators);
the only marker in the reflect dir is the `@pytest.mark.xfail` on the Layer-A test in
`test_no_nesting_guard.py:79-90` (unrelated).

---

## 7. Key file:line index (for the builder)

| Claim | Location |
|---|---|
| Seam type `AdversarialScoreFn = Callable[[list[str], Path], float \| None]` | `src/superclaude/cli/reflect/ensemble.py:72` |
| Seam injected as float in tests (`_const_score`) | `tests/cli/reflect/test_ensemble_stub_integration.py:39-41` |
| Shared driver `_run` (inject seam, parse_contract, derive_verdict) | `test_ensemble_stub_integration.py:88-102` |
| `_config` helper (depth=deep, transport=stub, reviewers) | `test_ensemble_stub_integration.py:78-85` |
| `_distinct_stub` + `stub_model_id` healthy survivor | `test_ensemble_stub_integration.py:69-76`; `ensemble.py:81-84` |
| `_i1_positive_holds` falsifier set | `test_ensemble_stub_integration.py:105-118` |
| I4 DEGRADED negative-witness assertion template | `test_ensemble_stub_integration.py:222-228` |
| Seam call site (only feeds convergence float) | `ensemble.py:221-232` |
| `build_reflect_contract` hardcodes regression False / 0 | `ensemble.py:377-407` (esp. 385-390, 401) |
| `derive_verdict` ordering + regression HALTED routing | `src/superclaude/cli/reflect/contract.py:130-246`, `307-328` |
| `regression_present` is a load-bearing bool (must be real `True`) | `contract.py:47-57`, `200-209` |
| Verdict exit codes PASS=0/HALTED=10/DEGRADED=11/BLOCKED=2 | `src/superclaude/cli/reflect/models.py:39-48` |
| `halted_regression.yaml` reference contract shape | `tests/cli/reflect/fixtures/halted_regression.yaml:11,22` |
| NFR-7 guard scans ensemble.py for banned tokens | `tests/cli/reflect/test_no_nesting_guard.py:31,106-124,167-179` |
| `temp_tasklist` / `patch_git` fixtures | `tests/cli/reflect/conftest.py:46-55, 58-80` |
| `WorkerResult` import + direct construction (unit path) | `test_ensemble_stub_integration.py:31`; `test_ensemble_unit.py:159-170` |

---

Status: Complete

## Summary

The headline acceptance test belongs in `tests/cli/reflect/test_ensemble_stub_integration.py`
as a new I12, modeled on the I4 DEGRADED negative-witness. It reuses `_config(..., reviewers=3)`,
`_distinct_stub` (a healthy all-survivor ensemble so no degradation masks the result),
injects a regression-reporting `adversarial_score_fn`, then `parse_contract(config.contract_path)`
+ `derive_verdict(..., expected_tier=2, child_rc=0)` and asserts `result.verdict is not
Verdict.PASS` (sharpened to `Verdict.HALTED` / `exit_code == 10` / `reason == "regression"`).

The verified root-cause gap: today's seam `AdversarialScoreFn` returns only a `float |
None` convergence score, and `build_reflect_contract` (`ensemble.py:377-407`) HARDCODES
`regression_present: False` and `deviation_count_by_class.regression: 0`. So a regression
found by the adversarial reviewer can never reach the contract, and `derive_verdict` can
never route `regression` from an ensemble run. The new test, written against current code,
will FAIL (seeing `Verdict.PASS`) — that is the intended red proof of the gap. It goes
green once `AdversarialScoreFn` is widened to carry the regression signal (a real Python
`True`, since `regression_present` is a load-bearing bool that routes BLOCKED if malformed)
and `build_reflect_contract` threads it through. Pytest invocation `uv run pytest
tests/cli/reflect/test_ensemble_stub_integration.py -q` (12 tests, all green, no markers,
~0.24s). NFR-7 guard requires the new code keep `ClaudeProcess` present and avoid `Task(`,
`subagent`, `anthropic` imports, raw subprocess, and async in `ensemble.py`.
