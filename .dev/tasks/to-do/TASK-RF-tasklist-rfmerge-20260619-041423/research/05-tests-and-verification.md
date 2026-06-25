# Research: Tests and Verification

**Status:** Complete
**Date:** 2026-06-19
**Researcher:** R05 (Test & Verification)
**Scope:** Test-file conventions + new-test mapping + baseline. (NOT: stage map [R01], contracts-under-test [R03], MDTM template [R06].)

---

## 0. BASELINE (read-only, run 2026-06-19)

`uv run pytest tests/tasklist/ -q` (worktree root) →
```
collected 71 items
tests/tasklist/test_autowire.py .........            [ 12%]
tests/tasklist/test_prd_cli.py ...                   [ 16%]
tests/tasklist/test_prd_prompts.py ..........        [ 30%]
tests/tasklist/test_tasklist_cli.py ....(28)         [ 70%]
tests/tasklist/test_tasklist_fidelity.py ...(21)     [100%]
============================== 71 passed in 0.22s ==============================
```
- SuperClaude 4.3.5, Python 3.13.11, pytest 9.1.0, rootdir = worktree root, configfile = `pyproject.toml`.
- **Starting state: 71/71 GREEN.** Builder adds tests on top of a clean suite; any new RED is attributable to the new work.
- Per-file counts (collected): `test_tasklist_cli.py`=28, `test_tasklist_fidelity.py`=21, `test_autowire.py`=9, `test_prd_cli.py`=3, `test_prd_prompts.py`=10.
- Harness warning (benign, ignore): `VIRTUAL_ENV=/lsiopy does not match the project environment path .venv`.

**Directory existence confirmations (per R05 charge):**
- `tests/reflect/` → **DOES NOT EXIST** (`ls: cannot access 'tests/reflect': No such file or directory`). The reflect CLI tests live under `tests/cli/reflect/`.
- `tests/cli/reflect/` → **EXISTS** (79 tests collected). Use this path for any reflect-related assertions; never `tests/reflect/`.
- `tests/cli/prd/test_prompts.py` → **EXISTS** (14699 bytes), carries the staleness-protocol test model (§5 below).

---

## 1. TEST-FILE CONVENTIONS — house style by file

### 1.1 `tests/tasklist/test_tasklist_cli.py` (277 lines) — PRIMARY home for new fns

This is the canonical Click-CLI + executor-helper test file and the **primary target** for P1/P3/P4 new tests and all carried-gap tests.

- **Imports** (`tests/tasklist/test_tasklist_cli.py:10-23`): `from __future__ import annotations`; `import pytest`; `from click.testing import CliRunner`; then the unit under test:
  - `from superclaude.cli.main import main`
  - `from superclaude.cli.tasklist.commands import tasklist_group`
  - `from superclaude.cli.tasklist.executor import (_build_steps, _collect_tasklist_files, _has_high_severity)`
  - `from superclaude.cli.tasklist.gates import TASKLIST_FIDELITY_GATE`
  - `from superclaude.cli.tasklist.models import TasklistValidateConfig`
- **Test organization:** plain classes grouping by concern, no base class, no `setup_method`. Class names: `TestTasklistCLIHelp`, `TestTasklistModuleStructure`, `TestTasklistValidateExitCode`, `TestCollectTasklistFiles`, `TestBuildSteps`.
- **Fixtures used:** only pytest builtin `tmp_path`. A fresh `CliRunner()` is constructed inline per test (`:30-31`), NOT a fixture (contrast `test_prd_cli.py` which DOES use a `runner` fixture).
- **CLI-invocation pattern** (`:29-33`): `runner = CliRunner(); result = runner.invoke(tasklist_group, ["validate", "--help"]); assert result.exit_code == 0; assert "validate" in result.output`. Help-text tests assert flag presence via substring on `result.output`.
- **Module-structure pattern** (`:73-105`): import the submodule, `assert hasattr(module, "symbol")`. This is the idiom a new public fn/contract should add: e.g. assert `hasattr(executor, "<new_fn>")`.
- **Frontmatter-parsing helper pattern** (`:108-151`): writes a YAML-frontmatter `.md` into `tmp_path` via `report.write_text("---\n...---\n## ...")` then asserts `_has_high_severity(report) is True/False`. Notably it tests **fail-safe defaults**: missing report → True (`:144-146`), no-frontmatter → True (`:148-151`). New parsers (e.g. gate-results passthrough P4) should mirror this fail-safe-default convention.
- **Executor `_build_steps` pattern** (`:183-277`): build a `TasklistValidateConfig(output_dir=, roadmap_file=, tasklist_dir=)` over `tmp_path`, call `_build_steps(config)`, assert on `steps[0]` attributes: `.id == "tasklist-fidelity"`, `.output_file`, `.inputs` (list), `.gate is TASKLIST_FIDELITY_GATE`, `.timeout_seconds == 600`. **Identity assertions use `is`** for gate/contract objects.
- **Assert style:** bare `assert expr` (no unittest methods); `pytest.raises(FileNotFoundError, match="...")` for error paths (`:165-173`).

### 1.2 `tests/tasklist/test_tasklist_fidelity.py` (228 lines) — prompt + gate semantic tests

- **Imports** (`:13-19`): `from pathlib import Path`; `from superclaude.cli.pipeline.models import GateCriteria`; `from superclaude.cli.roadmap.gates import (_high_severity_count_zero, _tasklist_ready_consistent)`; `from superclaude.cli.tasklist.gates import TASKLIST_FIDELITY_GATE`; `from superclaude.cli.tasklist.prompts import build_tasklist_fidelity_prompt`.
- **Prompt-shape tests** (`TestBuildTasklistFidelityPrompt`, `:22-97`): call `build_tasklist_fidelity_prompt(Path("/tmp/roadmap.md"), Path("/tmp/tasklist/"))` then assert **substring presence** of required markers in the returned string — severity labels (`"**HIGH**:"`), frontmatter field names, `<output_format>` block, the 5 comparison dimensions, the 7-column deviation format tokens. **This is the exact pattern P1's `test_execution_context_block_shape` should follow** for a generate-side prompt (substring assertions over the builder output, no Click runner needed).
- **Layering-guard tests** (`:100-131`): assert literal guard strings (`"VALIDATION LAYERING GUARD"`, `"ROADMAP → TASKLIST alignment ONLY"`).
- **Gate semantic tests** (`TestTasklistFidelityGate`, `:134-228`): `isinstance(GATE, GateCriteria)`; `.enforcement_tier == "STRICT"`; `.required_frontmatter_fields` membership + `len(fields) == 6`; `.semantic_checks` length==2 and `{c.name for c in checks}`; **`check.check_fn is _high_severity_count_zero`** (identity to the reused fn); and **content-driven check execution**: build a frontmatter string, call `check.check_fn(content)` and assert `True`/`False`. `.min_lines == 20`.

### 1.3 `tests/tasklist/test_autowire.py` (149 lines) — state-file auto-wire

- **Imports** (`:10-17`): `import json`; `from pathlib import Path`; `import pytest`; `from superclaude.cli.roadmap.executor import read_state`.
- **Module-level helper:** `write_state(state_dir, tdd_path=None, prd_path=None)` (`:26-37`) writes a `.roadmap-state.json` with `schema_version: 1`. A `state_dir` fixture (`:20-23`) just returns `tmp_path`.
- **Pattern:** tests both `read_state()` directly AND **re-implement the auto-wire if/Path.is_file() logic inline** in the test body (`TestAutoWireLogic`, `:64-149`) to prove the documented pattern, since the real wiring lives in `commands.py`. This is the model for any test that needs to assert a documented orchestrator/CLI behavior whose code is small enough to mirror.

### 1.4 `tests/tasklist/test_prd_cli.py` (39 lines) — `--prd-file` flag parsing

- Uses a `runner` **fixture** (`:14-16`: `@pytest.fixture def runner(): return CliRunner()`). Class `TestPrdFileFlagTasklist`. Tests: flag-in-help, default-none-renders, and **invalid-path Click error** (`:32-39`): `runner.invoke(tasklist_group, ["validate", str(tmp_path), "--prd-file", "/nonexistent/prd.md"])` then `assert result.exit_code != 0` and `"does not exist" in result.output.lower() or "Error" in result.output`. **This is the model for P-flag CLI parsing tests** (e.g. carried-gap `test_slash_flag_parsing`).

### 1.5 `tests/tasklist/test_prd_prompts.py` (101 lines) — PRD/TDD supplementary-block prompt tests

- **Imports** (`:14-17`): `from superclaude.cli.tasklist.prompts import (build_tasklist_fidelity_prompt, build_tasklist_generate_prompt)`.
- **Module constants** (`:19-24`): `ROADMAP = Path("roadmap.md")`, `TASKLIST_DIR`, `TDD`, `PRD`, and marker strings `PRD_MARKER = "Supplementary PRD"`, `TDD_MARKER = "Supplementary TDD"`.
- **A/B/C/D scenario matrix** (docstring `:3-8`): parametrize the four combinations of `tdd_file`/`prd_file` ∈ {None, set}. Each scenario asserts marker presence/absence + **ordering** (`tdd_pos < prd_pos`, `:54-57`) + **interaction-note-only-when-both** (`:89-94`) + **baseline-identical-without-supplements** (`:96-101`: `build(...) == build(..., tdd_file=None, prd_file=None)`). This `==` baseline-equivalence assertion is the model for **P5 advisory-determinism** (same input → identical output) and for any "new block must not alter the no-arg baseline" guard.

### 1.6 `tests/skills/test_task_builder_merge.py` (535 lines) — PR-01..PR-07 content gate

This is the **content-gate model** for asserting that documented behavior (markers introduced by each RFMerger landing) exists in the source-of-truth markdown. The new sc:tasklist work is analogous: the generator behavior is partly in `SKILL.md` (skill body) + partly in Python (`prompts.py`/`executor.py`/`commands.py`). Content-gate tests target the markdown; Python-contract tests target the modules.

- **Source-of-truth path resolution** (`:20-27`): `REPO_ROOT = Path(__file__).resolve().parents[2]`; then `SKILL_PATH = REPO_ROOT / "src" / "superclaude" / "skills" / "task-builder" / "SKILL.md"`, `RF_QA_PATH = .../agents/rf-qa.md`, etc. **Asserts against `src/superclaude/` (source of truth), NOT the `.claude/` mirror** — comment at `:9-11` explains why.
- **Module-scoped text fixtures** (`:30-52`): `@pytest.fixture(scope="module") def skill_text() -> str: return SKILL_PATH.read_text(encoding="utf-8")` (one per file).
- **Assertion idiom:** substring presence (`assert "TB-Add-1" in rf_qa_text`), `.count(tag) >= 2` for "appears in both prompt and checklist" (`:148-151`, `:200`, `:217`), and `@pytest.mark.parametrize("tag", [...])` over marker lists (`:72-103`).
- **PR-01 Execution Context assertions** (`TestPR01ExecutionContextHeader`, `:159-217`): keys to reuse for the **P1 mapping** — assert `"EXECUTION_CONTEXT_INSTRUCTION" in skill_text` + `"## Execution Context" in skill_text` (`:170-171`); forbidden-form guard `"NO specific file:line references"` + `"path.py:NN"` (`:178-179`); REQUIRED + `"GOAL-only"`/`"References-only"` graceful-degradation (`:186-188`); `skill_text.count("## Execution Context") >= 2` (instructions + schema example, `:200`).
- **PR-03 DNSP assertions** (`TestPR03DnspSyntheticFinding`, `:446-534`): keys for **P3 mapping** — `"DNSP Synthetic Finding Protocol"`, `"paradigm-neutral"` (`:453-455`); parametrized emission-contract fields `["severity: HIGH", 'source: "synthetic-dnsp"', "affected_range", "evidence", "recommendation"]` (`:457-472`); all-agents-fail guard `"All-agents-fail guard"`/`"all-agents-fail"` (`:474-480`); dedup-key literal `"(assigned_files_range, escalation_ladder_exhaust_point)"` + `"found N times"` (`:482-486`); applies-to-A.8/A.10/A.10.5 (`:488-493`); per-agent `synthetic-dnsp` presence in rf-analyst/rf-qa/rf-qa-qualitative; `INV-012` composition cited across `skill_text, rf_qa_text, rf_analyst_text` (`:524-534`).
- **PR-04 Gate-Results-Passthrough** (`TestPR04GateResultsPassthrough`, `:225-287`): keys for **P4 mapping** — `"Inherited Structural Verdict"` + `"PR-04 Gate Results Passthrough"`; INV-002 re-inject (`:237-241`), INV-010 dynamic enumerate (`:243-250`), INV-019 anti-inflation (`:252-257`), missing/malformed fallback (`:259-264`).
- **PR-02 Retry Monotonicity** (`TestPR02RetryMonotonicityGuards`, `:378-438`): keys for **P2 mapping** — `"Retry Monotonicity Protocol"`, `"strictly shrink"`/`"strict non-shrink"`, `"Precedence rule (regression > monotonicity)"`, `"Independent counters"`/`"tracked independently"`, INV-012 dedup composition.
- **PR-07 5-axis** (`TestPR07AdversarialCategoryNaming`, `:295-371`): parametrized axes `["Drift","Contradictions","Omissions","Weakened criteria","Invented content"]`; `"Five Adversarial Axes"`, overlay-not-replacement, drift-axis-inactive baseline, `"| # | Check | axis | Result | Evidence |"` table header literal (`:342`).

### 1.7 `tests/cli/reflect/` — fixtures + conftest + parity

- **`conftest.py`** (189 lines): provides reusable fixtures the new tests can adopt if any reflect-adjacent CLI behavior is tested:
  - `cli_runner` (`:40-43`) → fresh `CliRunner`.
  - `temp_tasklist` (`:46-56`) → writes a minimal MDTM frontmatter+body file with `start_commit`/`reflect_post` from `_TASKLIST_TEMPLATE` (`:23-37`).
  - `patch_git` (`:58-81`) → monkeypatches `config._git` to return fake BASE/HEAD SHAs so resolve works without a real repo.
  - `patch_runner_env` (`:83-96`) → stubs `runner._child_env` + `runner.shutil.which`.
  - `make_claude_process_stub` (`:98-138`) and `make_claude_process_sequence` (`:141-188`) → **Idiom-B factory**: patch `superclaude.cli.reflect.runner.ClaudeProcess` with a `**kwargs`→MagicMock whose `.wait()` writes a chosen fixture `return-contract.yaml` into `<output_dir>/` then returns an rc. This is the model for stubbing a subprocess that writes an artifact then exits.
- **`test_marker_suppression.py`** (143 lines): env-marker recursion-breaker tests using `monkeypatch.setenv`/`delenv`. Uses `patch("superclaude.cli.reflect.runner.ClaudeProcess")` + `mock_cls.assert_not_called()`. Also a **source-contract test** (`:112-143`): reads `src/superclaude/skills/sc-reflect-protocol/SKILL.md` via `parents[3]` and asserts the skill body contains specific control text — the model for skill-body-text contract tests when the logic lives in markdown not Python.
- **`test_docs_cli_parity.py`** (121 lines): **doc⇆CLI parity guard**. Introspects the Click command (`from superclaude.cli.reflect.commands import run`, iterates `run.params`, filters `click.Option`) to derive the real flag set, scans the guide markdown's option bullets, and asserts `documented == cli` (no phantom, no missing). `test_documented_defaults_match_cli_defaults` derives the active boolean-flag side / value default from the Click `Option`. **This is the model the doc-fanout facts-sheet memory calls for: any new sc:tasklist CLI flag added with user-facing docs should get a parity test of this shape.** Guide path resolved via `parents[3]` from `tests/cli/reflect/<file>`.

### 1.8 `tests/cli/test_verify_sync_hooks.py` (V1-V7, 222 lines)

- Subprocess-runs `make verify-sync` (`_run_verify_sync`, `:58-66`) and asserts on `result.returncode` + `result.stdout` substrings (`"=== Hooks ==="`, `"MISSING ..."`, `"DRIFT"`, `"DIFFERS"`).
- `pytestmark` skips when `make`/`jq` absent (`:49-55`). **WARNING in docstring** (`:11-25`): these mutate real repo files and **must NOT run under pytest-xdist**. Not a primary target for the new work, but it is the proof that `make verify-sync` is itself test-covered — relevant context for the sync gate (§4).

### 1.9 Bounded-loop / monotonicity / DNSP audit-test models (for P2 + P3 escalation + P5)

These `tests/audit/` files are the **closest existing analogues** for the P2 bounded-loop guard tests and the P3 DNSP-escalation tests. They model the halt-emitter behavior in pure Python and assert byte-exact contract strings.

- **`tests/audit/test_monotonicity_halt_F_5_5_5.py`** (398 lines, filename has `# ruff: noqa: N999`): imports a **shared pure-Python emitter** `from _halt_emitter import (HALT_MONOTONICITY_TEMPLATE, CycleState, HaltLog, run_fix_cycle)` via `sys.path.insert(0, str(Path(__file__).resolve().parent))` (`:52-59`, the `tests/audit/_halt_emitter.py` helper module — there is no conftest extending the path). Fixtures build `CycleState(cycle=, fail_set={...}, pass_set={...})` lists; `run_fix_cycle(...)` returns a `HaltLog` with `.halt_message`, `.lines`, `.cycles_started`, `.transitions`. Assertions: byte-exact halt string (`"[HALT-MONOTONICITY] |F|=5"`), byte-length (25), cycle-3-never-started, per-gate `counter=2/3`, 4-step ordering (regression→monotonicity→hard-cap→proceed), empty-F-set short-circuit, **negative case `TestStrictShrinkDoesNotHalt`** (`|F|=5,4` must NOT halt — over-firing guard). Also a SKILL.md source-contract preflight (`TestSkillContractWiringPresent`).
- **`tests/audit/test_regression_halt_pass1_fail2.py`** (559 lines): same `_halt_emitter`. Models **regression-precedence**: PASS@1/FAIL@2 fixtures in both shrinking (`|F|=5,4`) and non-shrinking (`|F|=5,5`) cardinality, proving regression fires by per-item PASS→FAIL flip NOT by `|F|` comparison, and that monotonicity is NEVER consulted on a regressed transition (`"HALT-MONOTONICITY" not in joined`). Includes a **counterfactual** (`:362-389`) proving monotonicity WOULD have fired absent the regression. Em-dash byte-sequence assertions (`EM_DASH_BYTES = b"\xe2\x80\x94"`, exactly one, at offset 32). Negative cases: no-flip and FAIL→PASS-is-not-regression.
- **`tests/audit/test_synthetic_dnsp_dedup_not_regression.py`** (TEST-022): proves a synthetic-dnsp finding with identical `dedup_key` across cycles is a DEDUP (contributes 1 to `|F|`), NOT a regression — the **P2 ∩ P3 composition** test (INV-012). Shrinking case proceeds to cycle 3.
- **DNSP per-path tests** (full set, 5 files): `test_dnsp_twice_exhaust.py` (TEST-018: all 5 fixed fields populated, `severity HIGH`, `source synthetic-dnsp`, 7-field schema), `test_dnsp_dedup_collapse.py` (TEST-019: within-cycle collapse cardinality=1 + `found_n_times=2`), `test_dnsp_all_agents_fail_bypass.py` (TEST-020: 3 mutually-exclusive cohort paths A/B/C; Path A `success_count==0` → no synthetic + escalation), `test_dnsp_does_not_serialize_cohort.py` (TEST-021/INV-021: N-1 siblings overlap exhausted partition's synthesis). These model **P3's `test_dnsp_all_agents_fail_escalates`** and `test_dnsp_synthetic_provenance` if the sc:tasklist generator gets the same DNSP partition contract; if the tasklist DNSP is lighter-weight (prompt-marker only), the simpler `test_task_builder_merge.py::TestPR03DnspSyntheticFinding` content-gate shape (§1.6) applies instead.
- **Execution-context audit tests** (P1 shape precedent): `test_execution_context_full.py` (TEST-004: all three DM-001 bullets References/Source areas/Key constraints in order between frontmatter and first `### T<PP>.<TT>`), `test_execution_context_minimal_buildrequest.py` (TEST-005: References-only degradation; Source-areas/Key-constraints **physically absent**), `test_execution_context_no_file_paths.py` (TEST-006/NFR-CONV.3: rendered block has NO `src/` or `file:line` — positive + negative leaky-fixture path). These use a `FIXTURE = Path(__file__).parent / "fixtures" / "execution_context" / "*.md"` convention. **`test_execution_context_block_shape` (P1) for sc:tasklist should mirror the §1.2 prompt-substring style if testing the generate prompt, OR the §1.6 content-gate style if testing the SKILL.md instruction text — pick by where the spec lands the P1 block (R01/R03 own that decision).**

---

## 2. NEW-TEST MAPPING (spec §8.1 / tdd §15.2)

Each row: test → target file → authoring note (house-style to copy) → discovery-item it carries. All citations point at the model test to mirror.

| New test | Target file | Authoring note (model + style) | Discovery item carried |
|---|---|---|---|
| `test_execution_context_block_shape` (P1) | `tests/tasklist/test_tasklist_cli.py` | If the P1 block is rendered by a prompt builder: call the builder (no CliRunner) and substring-assert the `## Execution Context` markers + forbidden `file:line` form, mirroring `test_tasklist_fidelity.py::TestBuildTasklistFidelityPrompt` (§1.2) and the PR-01 content-gate assertions (§1.6, `test_task_builder_merge.py:170-200`). If rendered into SKILL.md, use the §1.6 source-of-truth `read_text()` content-gate. | P1: task-level Execution Context block exists with declared bullets + no path leakage. |
| `test_dnsp_synthetic_provenance` (P3) | `tests/tasklist/test_tasklist_cli.py` **AND** `tests/skills/test_task_builder_merge.py` | tasklist_cli side: assert the generator/prompt emits `source: synthetic-dnsp` + `severity: HIGH` + the never-blank fields (model `test_dnsp_twice_exhaust.py` §1.9 for the 7-field schema, or §1.6 PR-03 parametrized field list if marker-only). merge side: extend `TestPR03DnspSyntheticFinding` parametrized-field assertions. | P3: synthetic finding provenance (`synthetic-dnsp` source tag) is stamped on partition-failure findings. |
| `test_dnsp_all_agents_fail_escalates` (P3) | `tests/tasklist/test_tasklist_cli.py` | Model `test_dnsp_all_agents_fail_bypass.py` (§1.9, Path A `success_count==0` → NO synthetic + escalation activates). Pure-Python cohort-path assertion or prompt-marker presence. | P3: all-agents-fail guard — zero successful partitions does NOT emit synthetic; escalation runs instead. |
| `test_gate_results_passthrough` (P4) | `tests/tasklist/test_tasklist_cli.py` | If passthrough is parsing a verdict file: mirror `_has_high_severity` frontmatter-parse + **fail-safe-default** pattern (§1.1, `:108-151`). If it is prompt-injection of an inherited verdict: mirror `test_task_builder_merge.py::TestPR04GateResultsPassthrough` (§1.6) incl. missing/malformed fallback. | P4: structural gate verdict is passed through (Inherited Structural Verdict) with fallback on missing/malformed. |
| `test_no_reflect_skips_stage_10_5` (carried gap) | `tests/tasklist/test_tasklist_cli.py` | CLI-flag-driven stage gating: invoke `tasklist_group` with the no-reflect flag via `CliRunner` (or call `_build_steps`/executor) and assert the Stage-10.5 step is absent from `steps`. Model `TestBuildSteps` step-list assertions (§1.1, `:183-200` — `len(steps)`, `steps[N].id`). | Carried gap: `--no-reflect` (or equiv) skips Stage 10.5 advisory entirely. |
| `test_stage_10_5_advisory_ships_all_verdicts` (carried gap) | `tests/tasklist/test_tasklist_cli.py` | Assert that when Stage 10.5 runs, every advisory verdict is emitted (not dropped/filtered). Model: build steps/output and assert presence of each verdict marker (substring over output, §1.2 style). | Carried gap: Stage 10.5 advisory output is complete (ships ALL verdicts, no silent drop). |
| `test_slash_flag_parsing` (carried gap) | `tests/tasklist/test_tasklist_cli.py` | Click flag-parse test. Model `test_prd_cli.py::TestPrdFileFlagTasklist` (§1.4): flag-in-`--help`, invalid value → `exit_code != 0`. Use a `runner` fixture or inline `CliRunner()`. | Carried gap: the new slash/flag (e.g. `--slash`/`/sc:task` naming flag) parses correctly + appears in help. |
| `test_sc_task_naming` | `tests/tasklist/test_tasklist_cli.py` | Assert generated tasklist items carry the `/sc:task`-compatible naming/IDs the generator must emit. Substring/regex over generated output or prompt (§1.2 style). Confirm exact token with R01/R03 contract before pinning the literal. | sc:task compliance-tier naming integration (item IDs / compliance-tier tags). |
| stale-token-prevention assertion | model lives in `tests/cli/prd/test_prompts.py` (CONFIRMED exists) | Model `TestInvestigationPromptStalenessProtocol` (`tests/cli/prd/test_prompts.py:124-141`): assert prompt contains `"Documentation Staleness Protocol"`, `"[CODE-VERIFIED]"`, `"[CODE-CONTRADICTED]"`, `"[UNVERIFIED]"`, `"EXIT_RECOMMENDATION: CONTINUE"`. For sc:tasklist, add the analogous staleness-marker assertion to the tasklist prompt test (`test_tasklist_fidelity.py` or `test_prd_prompts.py`). NOTE: the path is `tests/cli/prd/test_prompts.py`, NOT `tests/tasklist/test_prd_prompts.py` (which has NO staleness refs — confirmed via grep). | Prevents stale-token / un-verified-claim drift in the generated prompt. |
| **P2 bounded-loop guard tests** (set) | `tests/tasklist/test_tasklist_cli.py` (if loop logic in executor/Python) **OR** `tests/skills/test_task_builder_merge.py` + a new audit-style file (if loop logic in SKILL.md + emitter) | Five sub-assertions, each with a direct model in §1.9: (a) **full-set re-validation** — re-validate the entire set each pass, not a delta; (b) **monotonicity** — `|F|` strictly-shrink-or-halt, model `test_monotonicity_halt_F_5_5_5.py`; (c) **regression** — PASS→FAIL flip halts with precedence over monotonicity, model `test_regression_halt_pass1_fail2.py`; (d) **1-extra-pass cap=2-total** — bounded at 2 total passes (NOT the 3-cap of task-builder; pin the literal from spec — R03 owns), assert no 3rd pass started; (e) **Stage-10.5 non-overlap** — the extra-pass loop and Stage 10.5 advisory do not double-count / overlap. Use pure-Python `run_fix_cycle`-style helper if the merger ports `_halt_emitter`, else content-gate the SKILL.md protocol markers (`"Retry Monotonicity Protocol"`, `"regression > monotonicity"`, `"Do NOT consult subsequent steps"`). Include negative cases (slow-shrink does NOT halt). | P2: bounded extra-validation loop with monotonicity + regression halt, 2-total cap, no Stage-10.5 overlap. |
| **P5 advisory-determinism test** | `tests/tasklist/test_tasklist_cli.py` (or `test_tasklist_fidelity.py`) | Two assertions: (1) advisory NEVER alters scored tiers — build output with advisory on vs off and assert the **scored-tier portion is identical** (`==` on the scored-tier slice); (2) same roadmap → same scored tiers (determinism): call the generator/prompt twice on identical input and assert `==`. Model: `test_prd_prompts.py::test_baseline_identical_without_supplements` (§1.5, `:96-101`) — the `build(...) == build(...)` baseline-equivalence idiom. | P5: advisory layer is non-authoritative (does not mutate scored tiers) and the scored-tier result is deterministic. |

**Key disambiguation for the builder:**
- `test_dnsp_synthetic_provenance` is dual-homed: a tasklist-CLI/prompt assertion AND a `test_task_builder_merge.py` content-gate extension (per R05 charge).
- Whether P2/P3 get pure-Python emitter tests (`_halt_emitter` style) vs content-gate tests depends on **where the spec lands the logic** (Python executor vs SKILL.md prose) — that placement decision is owned by R01 (stage map) and R03 (contracts). R05 documents both candidate shapes; the builder picks per the merged spec.

---

## 3. EXACT UV TEST COMMANDS (verbatim, run from worktree root)

Primary new-test suite:
```
uv run pytest tests/tasklist/ -v
```

Adjacent tasklist suites (PRD/autowire, run together):
```
uv run pytest tests/tasklist/test_prd_cli.py tests/tasklist/test_prd_prompts.py tests/tasklist/test_autowire.py -v
```

Reflect CLI suite (parity + marker + conftest fixtures — NOTE `tests/cli/reflect/`, NOT `tests/reflect/`):
```
uv run pytest tests/cli/reflect/ -v
```

Content-gate suite (PR-01..PR-07 markers in source-of-truth markdown):
```
uv run pytest tests/skills/test_task_builder_merge.py -v
```

Audit bounded-loop / DNSP analogues (when P2/P3 use the pure-Python emitter model):
```
uv run pytest tests/audit/test_monotonicity_halt_F_5_5_5.py tests/audit/test_regression_halt_pass1_fail2.py tests/audit/test_synthetic_dnsp_dedup_not_regression.py -v
uv run pytest tests/audit/test_dnsp_twice_exhaust.py tests/audit/test_dnsp_dedup_collapse.py tests/audit/test_dnsp_all_agents_fail_bypass.py tests/audit/test_dnsp_does_not_serialize_cohort.py -v
```

Staleness-protocol model:
```
uv run pytest tests/cli/prd/test_prompts.py -v
```

---

## 4. SYNC / LINT / FORMAT GATES (mandatory before declaring done / pushing)

Source-of-truth discipline: if the work touches `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (or any skill/agent/command), edit `src/` FIRST, then sync, then verify.

```
make sync-dev                              # src/superclaude/{skills,agents,commands} -> .claude/
make verify-sync                           # confirm src/ and .claude/ match (CI-friendly; itself covered by tests/cli/test_verify_sync_hooks.py V1-V7)
make lint                                  # ruff check ONLY
uv run ruff format --check src/ tests/     # SEPARATE CI gate — `make lint` does NOT run this (per memory: make lint != CI ruff format)
```

**Ordering rule:** `make sync-dev` → `make verify-sync` must pass before commit (the pre-commit `verify-sync` local hook enforces it). `make lint` green is NOT sufficient for CI — `uv run ruff format --check src/ tests/` is a distinct gate that CI runs and `make lint` does not. Run both.

Note: `tests/cli/test_verify_sync_hooks.py` mutates real repo files and must NOT run under pytest-xdist; it skips if `make`/`jq` are unavailable.

---

## 5. STALENESS-TOKEN MODEL — confirmed path

The staleness-prevention test model lives at **`tests/cli/prd/test_prompts.py`** (CONFIRMED to exist, 14699 bytes). The relevant class is `TestInvestigationPromptStalenessProtocol` at `tests/cli/prd/test_prompts.py:124-141`. It asserts the prompt-builder output contains:
- `"Documentation Staleness Protocol"`
- `"[CODE-VERIFIED]"`, `"[CODE-CONTRADICTED]"`, `"[UNVERIFIED]"`
- `"EXIT_RECOMMENDATION: CONTINUE"`

**Disambiguation (important):** `tests/tasklist/test_prd_prompts.py` (the supplementary-block tests, §1.5) has **NO** staleness references (`grep -i "stale|staleness|token"` → empty). The staleness model is in `tests/cli/prd/`, not `tests/tasklist/`. The builder should mirror the `tests/cli/prd/test_prompts.py:124-141` shape when adding a stale-token-prevention assertion to the tasklist prompt.

---

## 6. SUMMARY

- **Baseline GREEN:** `tests/tasklist/` = **71/71 passed** (clean starting state). Builder's new RED is attributable to new work only.
- **Directory facts:** `tests/reflect/` does NOT exist; `tests/cli/reflect/` DOES (79 tests); `tests/cli/prd/test_prompts.py` DOES (staleness model).
- **Primary new-test home:** `tests/tasklist/test_tasklist_cli.py` (P1, P3, P4, all carried gaps, P5, sc-task-naming). Uses `tmp_path`, inline `CliRunner()`, bare `assert`, `is`-identity for gate/contract objects, fail-safe-default frontmatter parsing, `_build_steps` step-list assertions.
- **Prompt-shape model** (P1 generate-side, P5 determinism): `tests/tasklist/test_tasklist_fidelity.py` substring assertions + `tests/tasklist/test_prd_prompts.py` `build(...) == build(...)` baseline-equivalence.
- **Content-gate model** (P1/P3/P4 SKILL.md markers): `tests/skills/test_task_builder_merge.py` — `parents[2]` source-of-truth paths, module-scoped `*_text` fixtures, parametrized marker lists, `.count(tag) >= 2`.
- **Bounded-loop / DNSP model** (P2, P3 escalation): `tests/audit/` `_halt_emitter` pure-Python emitter (`CycleState`/`run_fix_cycle`/`HaltLog`), byte-exact contract strings, mandatory negative cases (slow-shrink/no-flip must NOT halt). The 2-total cap (NOT 3) and Stage-10.5 non-overlap literals are spec-owned by R01/R03 — pin from the merged spec, do not invent.
- **Doc⇆CLI parity model** (new CLI flags with docs): `tests/cli/reflect/test_docs_cli_parity.py` — introspect `run.params`, assert documented==cli flag set.
- **Gate commands:** `make sync-dev` → `make verify-sync` → `make lint` → `uv run ruff format --check src/ tests/` (the format check is a SEPARATE CI gate that `make lint` omits).
- **Open decision deferred to R01/R03:** for each of P1/P2/P3/P4, whether the test is a Python-module contract test or a SKILL.md content-gate test depends on where the merged spec lands the logic. R05 provides both candidate shapes per item.

**Status:** Complete
