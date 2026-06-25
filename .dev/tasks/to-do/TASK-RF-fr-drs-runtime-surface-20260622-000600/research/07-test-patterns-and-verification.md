# R7 — Test Patterns & Verification (FR-DRS)

Status: Complete
Date: 2026-06-22
Researcher: R7 (of 8)
Topic: Map existing `tests/cli/reflect/` conventions so the builder writes accurate, idiomatic test-creation items for the 3 new test files + the §15.4a derivation test.
Track goal: Implement FR-DRS + 3 integration paths. R7 owns pytest test conventions + the 4 test surfaces.

All paths are relative to worktree root `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/`.
Evidence tags: `[CODE-VERIFIED]` = read the actual file:line this turn; `[SPEC]` = from the TDD/spec (the test files do not exist yet — they are SPEC to build).

---

## 1. Existing `tests/cli/reflect/` conventions

### 1.1 Directory contents `[CODE-VERIFIED]`

`tests/cli/reflect/` (15 files): `conftest.py`, `__init__.py` (empty), `fixtures/` (subpkg),
`test_base_precedence.py`, `test_classify_fix.py`, `test_cli_smoke.py`, `test_docs_cli_parity.py`,
`test_ensemble_stub_integration.py`, `test_ensemble_unit.py`, `test_fix_loop.py`,
`test_marker_suppression.py`, `test_no_nesting_guard.py`, `test_promote_plumbing.py`,
`test_runner_e2e.py`, `test_verdict_mapping.py`, `test_writeback.py`.

`tests/cli/reflect/fixtures/` (YAML contract fixtures + empty `__init__.py`): `autofixable_drift.yaml`,
`autofixable_drift_no_path.yaml`, `blocked_unknown_major.yaml`, `blocked_with_drift.yaml`,
`degraded_serena.yaml`, `degraded_single_vendor.yaml`, `degraded_tier1.yaml`, `degraded_with_drift.yaml`,
`halted_regression.yaml`, `human_required_needs_decision.yaml`, `pass.yaml`, `postfix_pass.yaml`,
`tolerant_unknown_field.yaml`.

> Each fixture is a full `return-contract.yaml` (≈12–28 lines of contract fields). Example `pass.yaml`
> (`tests/cli/reflect/fixtures/pass.yaml:1-28` `[CODE-VERIFIED]`): `contract_version: "1.3.0"`, `status: success`,
> `mode: post`, `tier_reached: 2`, `deviation_count_by_class: {authorized,necessary,drift,regression}`, etc.
> **FR-DRS note:** none of the 13 existing fixtures carry the six `runtime_surface_*` scalars — they are at
> `contract_version: "1.3.0"`. The contract surface FR-DRS populates is `1.6.0` (TDD §8.3). New unit tests that
> need a `runtime_surface_*`-bearing contract construct the dict in-test (the §15.2/§15.4a pattern below), they
> do NOT depend on the existing fixtures.

### 1.2 conftest fixtures (`tests/cli/reflect/conftest.py` `[CODE-VERIFIED]`)

| Fixture | Lines | What it provides |
|---------|-------|------------------|
| `FIXTURES_DIR` (module const) | :17 | `Path(__file__).resolve().parent / "fixtures"` — imported as `from .conftest import FIXTURES_DIR` |
| `cli_runner` | :40-43 | fresh Click `CliRunner()` |
| `temp_tasklist` | :46-55 | writes a minimal MDTM tasklist (frontmatter `start_commit` + `reflect_post: ""` stub + body) to `tmp_path`, returns `Path`. Carries `_FAKE_BASE` so `<BASE>` resolves without git |
| `patch_git` | :58-80 | monkeypatches `config._git` → returns `_FAKE_HEAD` for `rev-parse HEAD`, `_FAKE_BASE` for `merge-base`. Exposes `.base`/`.head` for assertions |
| `patch_runner_env` | :83-95 | stubs `runner._child_env`→`{}` and `runner.shutil.which`→`/usr/bin/claude` so the launch preflight passes under test isolation |
| `make_claude_process_stub` | :98-138 | **Idiom-B single-launch factory builder.** `factory = make_claude_process_stub("pass.yaml", rc=0)`; the returned `MagicMock`'s `.wait()` writes the chosen fixture into `<output_dir>/return-contract.yaml` then returns `rc`. `fixture_name=None` / `write_contract=False` → writes NO contract (routes `blocked`) |
| `make_claude_process_sequence` | :141-188 | **Idiom-B sequence factory builder** for the bounded fix-loop: `make_claude_process_sequence([("autofixable_drift.yaml",0),(None,0),("postfix_pass.yaml",0)])`. Each `ClaudeProcess(**kwargs)` construction pops the next `(fixture, rc)`; `None` writes no contract (apply-`/task` step) |

Module-level SHA constants in conftest: `_FAKE_BASE = "1111…"` (:20), `_FAKE_HEAD = "2222…"` (:21) `[CODE-VERIFIED]`.
`from .conftest import _FAKE_HEAD` is imported by `test_runner_e2e.py:20` for resume assertions.

### 1.3 Import style `[CODE-VERIFIED]`

Every test file opens with `from __future__ import annotations`, then stdlib, then third-party (`yaml`,
`pytest`), then `superclaude.cli.reflect.*`, then `from .conftest import …`. Concrete examples:

- `test_verdict_mapping.py:8-15`: `from __future__ import annotations` → `import yaml` →
  `from superclaude.cli.reflect.contract import derive_verdict` →
  `from superclaude.cli.reflect.models import Verdict` → `from .conftest import FIXTURES_DIR`.
- `test_runner_e2e.py:9-20`: adds `import re`, `from unittest.mock import patch`,
  `from superclaude.cli.reflect.config import resolve_config`,
  `from superclaude.cli.reflect.runner import ReflectRunner`, `from .conftest import _FAKE_HEAD`.
- `test_classify_fix.py:9-12`: pure-function imports only (`classify_fix, derive_verdict`, `Verdict`).
- `test_ensemble_unit.py:3-26`: `import inspect`, `import ast` (inline), plus the swarm seam imports.

### 1.4 Assertion idioms `[CODE-VERIFIED]`

The reflect suite has **strong, repeated assertion idioms** the FR-DRS tests MUST mirror:

1. **Identity, not truthiness, on verdicts:** `assert result.verdict is Verdict.PASS` (the `is` enum identity),
   then `assert result.verdict.exit_code == 0` — the exit code is asserted as an **exact value**
   (`== 0 / 10 / 11 / 2`), **never** `!= 0`. (`test_verdict_mapping.py:27-28, 39-40, 51-52`;
   docstring `:5` "the exact `Verdict` and its `.exit_code` (==0/10/11/2, never just !=0)".)
2. **Reason-slug assertion:** failure-path tests assert `result.reason == "timeout"` / `"child-crash"` /
   `"malformed-contract-boolean"` / `"status-failed"` / `"frontmatter-stale"`
   (`test_verdict_mapping.py:107, 217, 244, 276`; `test_runner_e2e.py:101, 198`).
3. **Mock call-count arithmetic:** `assert mock_cls.call_count == 3 # (N+1)=2 audits + N=1 apply`
   (`test_fix_loop.py:53, 85, 101`), `mock_cls.assert_called_once()` (`test_runner_e2e.py:48`),
   `mock_cls.assert_not_called()` (`test_runner_e2e.py:155`).
4. **kwargs inspection on the launch:** `mock_cls.call_args.kwargs["max_turns"] == config.max_turns == 250`
   (`test_runner_e2e.py:50`), `mock_cls.call_args_list[1].kwargs["env_vars"] == {_MARKER: "1"}`
   (`test_fix_loop.py:56`).
5. **Control assertion alongside the falsifier:** several tests assert the bad case BLOCKS *and* a companion
   control still PASSES, in the same test body (`test_verdict_mapping.py:219-225` timeout-subset companion,
   `:255-260` over-block control). FR-DRS safety tests should follow this "falsifier + control" shape.
6. **One function per case — NO `@pytest.mark.parametrize` anywhere in the reflect suite** `[CODE-VERIFIED]`
   (grep of `test_ensemble_unit.py`, `test_classify_fix.py`, `test_verdict_mapping.py` found zero
   `parametrize`). Each scenario is its own named `def test_<scenario>() -> None:` with a one-line docstring
   stating the AC/falsifier. The §15.4a 4-row truth table and the N∈{0,1,2} invariant SHOULD therefore be
   **explicit per-row `def test_…`** functions (or a small in-body loop), matching house style, NOT a parametrize
   decorator. Return type `-> None` is annotated on every test fn.

### 1.5 ReflectConfig / contract construction in tests `[CODE-VERIFIED]`

Two construction patterns, pick by test layer:

**(a) Pure-function / verdict-layer tests — load a fixture dict, call the pure function directly.**
`test_verdict_mapping.py:18-19`:
```python
def _load(name: str) -> dict:
    return yaml.safe_load((FIXTURES_DIR / name).read_text(encoding="utf-8"))
```
then `derive_verdict(_load("pass.yaml"), expected_tier=2, allow_single_vendor=False, child_rc=0)`
(`:24-26`). For mutated-field cases the test loads the base dict and mutates a key in-place before calling:
`contract = _load("pass.yaml"); contract["verification_ran"] = False; derive_verdict(contract, …)`
(`test_verdict_mapping.py:156-161`). **This is the dominant pattern the §15.4a derivation test and the
verdict-layer slice of the safety-regression test should use** — no runner, no mocks, just `dict → function →
assert verdict/exit_code/reason`.

**(b) End-to-end runner tests — build a real `ReflectConfig` via `resolve_config`, patch `ClaudeProcess`.**
Local helper repeated in both `test_runner_e2e.py:33-36` and `test_fix_loop.py:23-26`:
```python
_PATCH_TARGET = "superclaude.cli.reflect.runner.ClaudeProcess"
def _config(tasklist, **overrides):
    params = dict(depth="standard", model="test-model")
    params.update(overrides)
    return resolve_config(str(tasklist), **params)
```
Body pattern (`test_runner_e2e.py:39-51`):
```python
config = _config(temp_tasklist)
factory = make_claude_process_stub("pass.yaml", rc=0)
with patch(_PATCH_TARGET, side_effect=factory) as mock_cls:
    result = ReflectRunner(config).run()
assert result.verdict is Verdict.PASS
```
Fixtures `temp_tasklist, patch_git, patch_runner_env, make_claude_process_stub` are taken as test args together
(the standard 4-fixture quartet for any runner-driven test). The sidecar is read back via a
`wrapper-result.yaml` helper (`test_fix_loop.py:29-32` `_sidecar`), and the written `reflect_post` block via a
frontmatter regex helper (`test_runner_e2e.py:23-31` `_FM_RE` + `_read_reflect_post`).

**Write-back unit pattern** (`test_writeback.py:41-52, 61-72`): build a `ReflectResult(...)` dataclass directly
(no runner), write a tasklist to `tmp_path`, call `write_reflect_post(path, result, head=…, reviewed_at=…)`,
assert the returned status string and re-parse the frontmatter.

---

## 2. Structure for each NEW test file

The TDD names three new pytest files under `tests/cli/reflect/` plus the §15.4a derivation test. The module
under test is `src/superclaude/cli/reflect/runtime_surface.py` with orchestrator `run_sweep(...) -> SweepResult`
and six pure units `tag_surfaces / find_referrers / partition_referrers / degrade_oracle / rootwalk_entrypoints
/ reduce_ledger` (TDD §8.1 lines 622-629 `[SPEC]`). Build the test files against THESE names.

### 2.1 `tests/cli/reflect/test_runtime_surface.py` — UNIT (the 6 units + count invariant) `[SPEC: TDD §15.2 :1010-1029]`

Coverage target **> 90%** (pure functions, no LLM, no network — §15.1 :1003). One named `def test_…() -> None:`
per unit + the count-invariant assertion. Imports per §1.3: `from __future__ import annotations`, then
`from superclaude.cli.reflect.runtime_surface import (tag_surfaces, find_referrers, partition_referrers,
degrade_oracle, rootwalk_entrypoints, reduce_ledger, run_sweep, SweepResult, ...types...)`.

| # | Unit fn | Representative input (TDD §15.2 table :1016-1021) | Assert |
|---|---------|---------------------------------------------------|--------|
| 1 | `tag_surfaces` | diff adding a decorated `/ai` handler; + an unknown-lang symbol | symbol tagged with its `runtime_surface_requirements` id; unknown-lang → DEGRADE-tagged |
| 2 | `find_referrers` | symbol with 2 production callers + 1 test caller | 3 referrer edges found; tool-loss path sets `degraded_components` |
| 3 | `partition_referrers` | mixed referrer set incl. inline-test module | production/test classification matches the §2 lang table; inline-test counted as test |
| 4 | `degrade_oracle` | `[project.scripts]`-wired entrypoint (case 39 shape) | `DegradeVerdict.degraded is True`, `runtime_surface_degraded: true`, NOT UNREACHED, NOT Regression |
| 5 | `rootwalk_entrypoints` | symbol reachable from a CLI root (case 38 shape) | `RootwalkResult.status == "REACHED"`, `unreached: 0` |
| 6 | `reduce_ledger` | symbol with only test/comment referrers (case 41 shape) | verdict UNREACHED; `runtime_surface_unreached == 1`; `len(unreached_surfaces) == 1` by construction |

**Count-invariant unit assertion (AC-3, TDD :1023 `[SPEC]`):** one dedicated reducer test constructs ledger rows
with **N symbols reduced to UNREACHED** and asserts
`len(result.unreached_surfaces) == result.runtime_surface_unreached == N` **for N ∈ {0, 1, 2}**. Because the
reducer computes both from the same row set this is by-construction (computed, not asserted-on-LLM). Per house
style (§1.4 item 6, no parametrize) write this as three explicit cases (`test_count_invariant_zero`,
`_one`, `_two`) or a single test with an in-body `for n in (0, 1, 2):` loop calling `reduce_ledger` on a row set
sized to `n`. The DEGRADE-exclusion sub-assertion (a DEGRADE symbol is never added to `unreached_surfaces`,
FR-003 :283) belongs here too.

**Fast-path unit** (TDD §17.2 :1134 `[SPEC]`): a non-surface diff → `run_sweep` returns
`SweepResult` with `scalars["runtime_surface_sweep_ran"] == False`, `ledger_path is None`, no ledger write.

Command (TDD :1027-1028 `[SPEC]`): `uv run pytest tests/cli/reflect/test_runtime_surface.py -v`.

### 2.2 `tests/cli/reflect/test_runtime_surface_eval_determinism.py` — INTEGRATION ≥3-run `[SPEC: TDD §15.3 :1031-1053]`

**This is the acceptance bar (AC-2), not a coverage test.** The 5 `case_dir`-backed cases (evals.json ids 37–41,
`cases/uc2-*/`) run through the eval harness where the grader invokes the **same** `runtime_surface.run_sweep()`
module (TDD :1033). The determinism gate: run the harness **3×** and assert the per-case `grading.json` is
**byte-identical run-to-run** with **zero variance** (TDD :1043 `[SPEC]`). This is the exact criterion the
prose-only implementation failed (dynamic-dispatch was 0/3→1/3 — TDD :1043).

Structure (house idioms applied):
- Drive 3 iterations (`for _ in range(3):` or 3 explicit iteration dirs), each invoking the grader/harness over
  the same `cases/uc2-*/` inputs, collecting the resulting `grading.json` (or per-case grading dict).
- Assert run[0] == run[1] == run[2] for each of ids 37–41 — compare the **serialized bytes** (or
  `json.loads`-normalized dicts) so the assertion is on identity, not on "passed" (matching §1.4 item 1's
  exact-value discipline). A passing-but-varying result must FAIL this gate.
- Per-case expected outcomes (TDD §15.3 table :1037-1041 `[SPEC]`): 37→unreached 1/regression 1/tier 2;
  38→all-zero/tier 1; 39→degraded true/regression 0/tier 1; 40→degraded true/status partial/tier 1;
  41→unreached 1/regression 1/tier 2 + the `yaml_list_len_eq` count invariant.

**Load-bearing dependency to surface as a task RISK (TDD :1055 carry-forward C-5 `[SPEC]`):** the grader reads
per-eval `eval_metadata.json` (grader.py:440, no-metadata skip at :442), NOT `evals.json` directly. The
materializer that turns `evals.json` → per-eval `eval_metadata.json` (and copies `cases/uc2-*/expected.yaml` +
`input/` into `iterations/iteration-N/eval-<name>/`) was **not located** and is **UNVERIFIED**. The integration
test assumes it exists and runs before the grader. **The task item MUST instruct: verify this materializer
exists/runs during implementation** (this is R5's eval-wiring territory — R7 flags it as the precondition the
determinism test depends on, does not own it).

Command (TDD :1051-1052 `[SPEC]`): `uv run pytest tests/cli/reflect/test_runtime_surface_eval_determinism.py -v`
(the harness invocation `uv run python .dev/eval-workspaces/sc-reflect/grader.py <iterations/iteration-N/>` is the
inner step, TDD :1049).

### 2.3 `tests/cli/reflect/test_runtime_surface_safety_regression.py` — AC-5 SAFETY GATE `[SPEC: TDD §24.2 :1415 + §15.6 :1098]`

**Concrete pass/fail gate, NOT a spot-check (TDD :1415 explicit).** Runs the **four named fixtures — cases 37,
39, 40, 41 — through the verdict layer** and asserts the expected verdict/`status` per case; the gate **FAILS the
release if ANY of the four clean-passes its surface.** Per-case expected (TDD §24.2 :1415 `[SPEC]`):

| Case id | Case | Expected at the verdict layer | Falsifier (FAIL release if…) |
|---------|------|-------------------------------|------------------------------|
| 37 | `uc2-unwired-surface-passes` | FAIL-pre / PASS-post; `runtime_surface_unreached ≥ 1` + regression 1; never clean-pass | the unwired surface clean-passes |
| 39 | `uc2-surface-dynamic-dispatch` | DEGRADE; regression 0; no false-UNREACHED | a DEGRADE is mis-routed UNREACHED, or it clean-passes |
| 40 | `uc2-surface-degraded-backend` (`backend:none`) | Grounding Gap + `status: partial`; no hard-STOP; no clean-pass | it hard-STOPs OR clean-passes |
| 41 | `uc2-surface-test-only-ref` | UNREACHED; no clean-pass | the test/comment-only surface clean-passes |

> Note: cases 37/41 also appear in §15.3 (id 38 the positive REACHED control is **deliberately excluded** from
> the AC-5 gate — the gate is about *never clean-passing an unwired surface*, so the always-clean control would
> only dilute it).

Structure: this is a **verdict-layer** test (TDD :1098 / :1415 "through the verdict layer"), so it follows the
`test_verdict_mapping.py` pattern (§1.5a): construct each case's `runtime_surface_*`-bearing contract dict (from
the case's `expected.yaml` / the module output), feed it through the verdict + prose layer
(`derive_verdict` / the §10.6 Grounding-Gap + §5.3 derivation chain), and assert `verdict`/`status` is NOT a
clean PASS. Use the "falsifier + control" idiom (§1.4 item 5): each case asserts the surface is suppressed AND
(where applicable) that a genuinely-reachable control is NOT over-blocked. Annotate every test fn `-> None` with
a docstring naming the AC-5 falsifier.

### 2.4 §15.4a `surface_unreached` derivation test `[SPEC: TDD §15.4a :1070-1081]`

**Where it lives:** the TDD does not pin a separate filename; §15.6 :1097 maps AC-4 to "§15.4a derivation test"
and §15.4a calls it "a unit-testable transform … MUST be covered". The derivation owner is
`runner._audit_once` (same merge point as the six scalars, FR-005/FR-006). **Recommendation:** host it in
`test_runtime_surface.py` (the unit file) as `def test_surface_unreached_derivation_*()` since it is a pure
integer→string transform unit; OR, if the derivation is exercised through the runner, add it to
`test_runner_e2e.py` (the §5.3-pre-filter-reads-derived-string half is a runner/consumer assertion). The task
item should let the builder choose by where the derivation function actually lands, but the **default is the unit
file**. (R7 flags: confirm the derivation owner's home with R3 consumer-wiring; R7 owns only the test shape.)

**The 4-row truth table (TDD §15.4a :1074-1079 `[SPEC]`):**

| Given (integer scalar from sweep) | Sweep status | Expected `surface_unreached` | Expected §5.3 effect |
|-----------------------------------|--------------|------------------------------|----------------------|
| `runtime_surface_unreached == 0` | successful (REACHED) | `null` | no force; STOP rows may fire |
| `runtime_surface_unreached == 1` | successful (UNREACHED) | `"runtime_surface_unreached"` (literal string) | force Tier 2 + `status: partial` |
| `runtime_surface_unreached == 2` | successful | `"runtime_surface_unreached"` | force Tier 2 + `status: partial` |
| `runtime_surface_degraded == true`, `unreached == 0` | degrade-only | `null` | NOT forced via this pre-filter (degrade path is independent) |

Two-part assertion (TDD :1081): (1) the derivation transform in isolation (integer → derived string), then
(2) the §5.3 pre-filter reads the derived string — proving producer→derivation→consumer is wired to the
deterministic value, not an LLM-typed one (closes the C1 gap). Per house style, write 4 explicit `def test_…`
functions (one per row) — `0`, `1`, `2`, `degrade-only` — NOT a parametrize. The literal expected value is the
**string** `"runtime_surface_unreached"` (the field-name-as-sentinel, SKILL.md:412), not a bool — assert exact
string identity.

---

## 3. Verification / validation commands the task items MUST run `[CODE-VERIFIED]`

| Purpose | Command | Source |
|---------|---------|--------|
| Unit suite (the 6 units + count invariant + derivation) | `uv run pytest tests/cli/reflect/test_runtime_surface.py -v` | TDD :1028 `[SPEC]` |
| Determinism integration gate (≥3-run, AC-2) | `uv run pytest tests/cli/reflect/test_runtime_surface_eval_determinism.py -v` | TDD :1052 `[SPEC]` |
| AC-5 safety-regression gate | `uv run pytest tests/cli/reflect/test_runtime_surface_safety_regression.py -v` | TDD :1098/:1415 `[SPEC]` |
| Whole reflect suite (regression guard) | `uv run pytest tests/cli/reflect/ -v` | house pattern |
| Eval harness inner step (grader invokes the module) | `uv run python .dev/eval-workspaces/sc-reflect/grader.py <iterations/iteration-N/>` | TDD :1049 `[SPEC]` (R5 owns the grader wiring) |
| **ruff format check (CI-equivalent — MANDATORY, separate from lint)** | `uv run ruff format --check src/ tests/` | see §3.1 |
| Lint | `make lint` (= `lint-architecture` + `uv run ruff check .` ONLY, Makefile:48-50 `[CODE-VERIFIED]`) | Makefile |
| Component sync gate | `make verify-sync` (Makefile:166 `[CODE-VERIFIED]`) | CLAUDE.md / Makefile |
| UV-only | All Python ops via `uv run …` — never `python -m` / bare `pip` / `python script.py` | CLAUDE.md ABSOLUTE RULE |

### 3.1 The `make lint` ≠ `ruff format --check` split — CALLED OUT `[CODE-VERIFIED]`

`make lint` (Makefile:48-50) runs `lint-architecture` + `uv run ruff check .` — **`ruff check` ONLY**. There is a
**separate** `make format` target (Makefile:53-55) that runs `uv run ruff format .` (a mutating format, not a
check). **Neither `make lint` runs `ruff format --check`.** CI runs `ruff format --check` as a distinct gate
(memory `make_lint_vs_ci_ruff_format`: "green make lint ≠ green CI format"). **Therefore the task MUST add an
explicit item: `uv run ruff format --check …` before pushing** — a green `make lint` does NOT cover it, and
`make format` mutates rather than verifying. Scope ruff to the changed files only — a broad bare
`uv run ruff format .` reformats ~106 unrelated files due to a worktree-venv ruff version mismatch
(memory `ruff_version_mismatch_worktree`). Prefer
`uv run ruff format --check src/superclaude/cli/reflect/ tests/cli/reflect/` to stay surgical.

### 3.2 `make verify-sync` applicability

FR-DRS's test files are pure `tests/` additions and the module is `src/superclaude/cli/reflect/runtime_surface.py`
— **none of these are `.claude/` sync-dev output**, so the test-creation items themselves do not require
`make sync-dev`. `make verify-sync` becomes load-bearing only for the SKILL.md edits (R6's territory). Include
`make verify-sync` as a final cross-cutting gate (AC-6, TDD :1006) so the SKILL changes elsewhere in the task
don't silently drift; the test items can run it as the closing sync check.

---

## 4. Coverage target & acceptance bar `[SPEC: TDD §15.1 :1003, §15 :997]`

- **Coverage target: > 90%** for `runtime_surface.py` unit tests (pure functions, no LLM, no network) — TDD
  §15.1 :1003.
- **The acceptance bar is DETERMINISM, not coverage %** — TDD §15 :997 ("Determinism is the acceptance bar, not
  coverage percentage") and §15.3 :1043 (zero variance across ≥3 runs). The task's done-definition for the
  test surface is: (a) unit suite green at >90% coverage, (b) the 5 uc2 cases identical across ≥3 runs, (c) the
  AC-5 gate FAILs on any clean-pass and passes on the 4 fixtures, (d) count invariant green for N∈{0,1,2}, (e)
  `ruff format --check` + `make verify-sync` clean.
- AC→test coverage map (TDD §15.6 :1092-1099 `[SPEC]`): AC-1→§15.2 reducer/emit units; AC-2→§15.3 determinism
  gate; AC-3→§15.2 count-invariant unit + §15.4 grader re-check; AC-4→§15.4a derivation test; AC-5→§24.2 safety
  gate (`test_runtime_surface_safety_regression.py`); AC-6→§15.1 sync/lint tier.

---

## 5. Builder guidance — idioms to encode verbatim in the task items

1. Every new test file: `from __future__ import annotations` header; `-> None` on every test fn; one named
   `def test_<scenario>` per case; **no `@pytest.mark.parametrize`** (zero usages in the reflect suite — use
   explicit functions or an in-body loop).
2. Verdict assertions: `assert result.verdict is Verdict.X` (enum identity) **then** exact
   `assert result.verdict.exit_code == <0|10|11|2>`; reason slugs asserted by exact string.
3. Pure-function tests (units, derivation, safety verdict-layer): `dict → function → assert` — the
   `_load(name)` + in-place field mutation pattern from `test_verdict_mapping.py:18-19, 156-161`. Build the
   `runtime_surface_*` contract dict in-test (existing fixtures are 1.3.0 and lack the six scalars).
4. Runner-driven tests (if any determinism/safety case needs the full pipe): the 4-fixture quartet
   `temp_tasklist, patch_git, patch_runner_env, make_claude_process_stub` + `_config()` helper +
   `patch("superclaude.cli.reflect.runner.ClaudeProcess", side_effect=factory)`.
5. Determinism test asserts **byte/dict identity across 3 runs**, not "passed" — a varying-but-passing result
   must fail.
6. Safety test is a **gate** (FAIL release on any clean-pass), 4 fixtures (37/39/40/41), verdict-layer.
7. Always-UV; add the explicit `uv run ruff format --check src/superclaude/cli/reflect/ tests/cli/reflect/`
   item (make lint does NOT cover it); scope ruff to changed dirs to dodge the version-mismatch mass reformat.
8. Flag (do not own) the UNVERIFIED eval materializer (TDD :1055 C-5) as a precondition the determinism test
   depends on — hand to R5's eval-wiring items.

---

## Gaps and Questions

- **§15.4a derivation-test home is not pinned by the TDD.** R7 recommends `test_runtime_surface.py` (unit
  transform) by default; the consumer-read half may belong in `test_runner_e2e.py`. Final home depends on where
  the derivation function lands (R3 consumer-wiring). The task item should phrase it as "host the integer→string
  derivation unit + the §5.3-reads-derived-string assertion where the derivation owner lives; default the unit
  file."
- **Eval materializer (evals.json → eval_metadata.json) is UNVERIFIED** (TDD :1055). The ≥3-run determinism test
  depends on it. R5 owns the eval-path wiring; R7 only flags it as a hard precondition.
- **No `runtime_surface_*`-bearing fixture exists yet.** New unit/safety tests construct the contract dict
  in-test. If R5's eval cases produce reusable `expected.yaml` fixtures, the safety-regression test could load
  those instead of hand-building dicts — coordinate with R5 to avoid duplicate fixture authorship.
- **Coverage measurement command not pinned by the TDD.** House `pyproject.toml` supports
  `uv run pytest --cov=superclaude` (CLAUDE.md). The task can add
  `--cov=superclaude.cli.reflect.runtime_surface --cov-report=term-missing` to the unit-suite item to evidence
  the >90% bar.

## Stale Documentation Found

- None in the test surface. Note for adjacent context: the existing fixtures are `contract_version: "1.3.0"`
  while FR-DRS populates the `1.6.0` field set; and `ensemble.REFLECT_CONTRACT_VERSION = "1.0"` (ensemble.py:59)
  is stale vs the SKILL-declared `1.6.0` (TDD §8.3 :694) — a producer-side reconcile item, not a test item, but
  any new fixture the test files author should use the correct version to avoid propagating the stale literal.

## Summary

The `tests/cli/reflect/` suite has tight, repeatable conventions the FR-DRS test items must mirror:
`from __future__ import annotations` + `-> None` on every test; **one function per case, no parametrize**;
verdict assertions as enum-identity (`is Verdict.X`) + exact `exit_code == 0/10/11/2` + exact reason slug; two
construction patterns — **(a) pure `dict→function→assert`** via `_load()`+field-mutation (the model for the unit,
derivation, and safety-verdict-layer tests) and **(b) runner-driven** via the 4-fixture quartet + `_config()` +
`patch(ClaudeProcess, side_effect=factory)`. The three new files: `test_runtime_surface.py` (6 unit fns + the
N∈{0,1,2} count-invariant + fast-path + the §15.4a derivation), `test_runtime_surface_eval_determinism.py` (run
the 5 uc2 cases 37–41 ×3, assert grading.json byte-identical — AC-2 is the acceptance bar, not coverage),
`test_runtime_surface_safety_regression.py` (cases 37/39/40/41 through the verdict layer, FAIL on any
clean-pass — AC-5 gate). §15.4a hosts the 4-row truth table (`0→null`, `1→"runtime_surface_unreached"`,
`2→"…"`, degrade-only`→null`), default home the unit file. Verification commands: `uv run pytest` on each new
file + the whole reflect dir, **the MANDATORY-but-separate `uv run ruff format --check src/ tests/`** (make lint
runs ruff *check* only — Makefile:48-50 verified), and `make verify-sync` as the AC-6 closing gate. Coverage >90%
on the pure functions; the eval materializer is an UNVERIFIED precondition (hand to R5).
