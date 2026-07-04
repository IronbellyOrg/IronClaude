# Research: tests & conventions

Status: Complete
Date: 2026-07-03
Researcher: R5 (Deep tier) — Test & Verification infrastructure

Worktree root (all paths absolute): `/config/workspace/IronClaude/.dev/worktrees/pr209-harden`

TRACK GOAL context: additively harden RF QA + /sc:reflect vs PR #209 F1–F4 by
authoring two NEW deterministic test artifacts — **FX3**
(`tests/pr_submit/test_setup_questions_resolution.py`, AST introspection of
`contract_setup/questions.py`) and **FX5** (a `tests/pr_submit/conftest.py`
collector that enumerates gate helpers and FAILs if any lacks a negative +
differential test).

---

## 1. `tests/pr_submit/conftest.py` — current fixtures, collectors, hooks

File: `tests/pr_submit/conftest.py` (82 lines). Read in full.

**Fixtures defined (all function-scoped, plain `@pytest.fixture`):**

| Fixture | Line | Purpose |
|---|---|---|
| `load_fixture` | :20 | Returns a loader closure reading JSON from `fixtures/`. |
| `mock_gh` | :30 | Monkeypatches `superclaude.pr_submit.detection._fetch_payload` to a recorder fake; records `calls`, controllable `payload`. |
| `mock_monitor` | :54 | Records Monitor-arm calls. |
| `fixture_findings` | :68 | Loads `fixtures/finding-medium-high.json`. |
| `tmp_skill_dir` | :76 | `tmp_path`-based skill/output dir. |

**Collectors / hooks: NONE.** `tests/pr_submit/conftest.py` defines **no**
`pytest_collection_modifyitems`, no `pytest_generate_tests`, no
`pytest_configure`, no collector classes. It is a pure fixture module. Module
constant `FIXTURES_DIR = Path(__file__).parent / "fixtures"` (:17).

**Where collection hooks DO live (repo-wide):**
- `src/superclaude/pytest_plugin.py:206` defines the ONLY
  `pytest_collection_modifyitems` in the codebase (auto-marks by dir/filename:
  `/unit/`→unit, `/integration/`→integration, `*hallucination*`,
  `*performance*`). Also `pytest_configure` (:20), `pytest_runtest_setup`
  (:148), `pytest_runtest_makereport` (:172), `pytest_report_header` (:199).
- Grep for `pytest_collection_modifyitems` / `pytest_generate_tests` across
  `tests/**` returned **zero** hits — no test-level conftest uses either hook.

**How to add an FX5 collector without breaking existing collection:**

Pytest invokes **all** registered implementations of a given hook (the global
plugin hook + any package-scoped conftest hook both run), so adding a new hook
to `tests/pr_submit/conftest.py` does NOT override or conflict with the
plugin's `pytest_collection_modifyitems`. Two idiomatic, additive options:

- **Option A (recommended) — `pytest_generate_tests(metafunc)` in
  `tests/pr_submit/conftest.py`.** Enumerate the gate helpers (via AST/import
  introspection of the gate-helper module) and `metafunc.parametrize(...)` a
  dedicated coverage test (e.g.
  `test_gate_helper_has_negative_and_differential`) with one param per helper.
  Each helper becomes its own reported test id and FAILs individually when its
  negative/differential test is missing. This is the cleanest "collector that
  FAILs per-helper" and coexists with the plugin hook. The parametrize
  precedent already exists in this suite (see §2).
- **Option B — a plain test module + module-level `@pytest.mark.parametrize`**
  (e.g. `tests/pr_submit/test_gate_coverage.py`) rather than a conftest hook.
  Simplest and matches the dominant pr_submit precedent, but the enumeration
  lives in the test file, not `conftest.py`. If the FX5 spec strictly wants the
  enumeration in `conftest.py`, use Option A.

Note on "FAIL" semantics: a `pytest_collection_modifyitems` hook can only
mutate collected items (add markers, deselect) — it CANNOT cleanly assert-fail.
To make a missing-coverage case a red test, use `pytest_generate_tests`
(Option A) or a normal parametrized test (Option B). Raising inside a
collection hook produces a collection ERROR (aborts collection of the package),
which is a blunter, less-diagnostic signal — avoid it.

---

## 2. Existing `test_contract_setup_*.py` patterns

Six files: `test_contract_setup_{diagnosis, evidence, pr_submit_integration,
questions, validation, writer}.py`. Read fully:
`test_contract_setup_questions.py`; read in part:
`test_contract_setup_validation.py`.

**Conventions observed:**
- **Module docstring** cites the driving spec/research doc + acceptance area
  (e.g. `test_contract_setup_questions.py:1-21` cites
  `TASK-RF-detection-contract-20260701-164700/research/03-validation-tests.md`
  and `merged-requirements.md §4`).
- **`from __future__ import annotations`** at top of every file.
- **Imports the REAL package surface only** — no mocks of the module under
  test. E.g.
  `from superclaude.pr_submit.contract_setup.questions import SETUP_QUESTIONS, SetupAnswers`
  (`test_contract_setup_questions.py:33-36`);
  `validation.validate_candidate`, `candidate.derive_candidate`,
  `evidence.EvidenceBundle`.
- **Local builder helpers** prefixed `_` construct in-memory inputs:
  `_bundle(...)` (:62) builds an `EvidenceBundle`; `_augment_review(...)`
  (:109); in validation file `_write_probe(...)`, `_findings_bundle(...)`
  (:~95-104), `_augment_findings_review()`, `_augment_inline_finding_comment()`.
- **Test naming**: long behavioural sentences —
  `test_setup_question_sequence_contains_all_16_questions_in_order` (:122),
  `test_setup_defaults_are_suggestions_not_lock_values_without_evidence` (:136),
  `test_probe_pr_question_default_respects_operator_answer` (:272).
- **Assertion style**: direct `assert` with a tuple/message second arg for
  diagnostics (`assert required_field in missing, (missing, required_field)`
  :163; `assert report.result == "passed", report.blockers` validation:123).
  Structural assertions on `.provenance[key].observed`,
  `.required_unobserved()`, `report.result in {"passed","failed"}`,
  `report.blockers`, `report.checks` (a list of named checks; pattern
  `next(c for c in report.checks if c.name == "...")`).
- **`tmp_path` for all filesystem writes** — deriver only reads
  `evidence.probe_dir`; tests point it at `tmp_path` so nothing under the repo
  is written (docstring :18-20). No `.dev/pr-monitor/` artifacts touched.
- **Regression tests are explicitly tagged in the docstring with the PR # and
  finding id.** PR #209 findings already have named regression tests:
  - F2 (app-slug wrong bucket):
    `test_augment_app_slug_dedicated_field_selects_observed_slug` (:211),
    `..._legacy_decline_bucket_still_supported` (:247).
  - F3 (`probe_pr` vs nonexistent `pr_number` answer field):
    `test_probe_pr_question_default_respects_operator_answer` (:272-288).
  - F4 (`_path_resolves` all-None list):
    `test_severity_path_all_none_does_not_resolve` (validation:180-197), plus
    context notes at validation:132, :158, :183.

**AST / static-introspection precedent (grep repo-wide):**
- **`import ast` is well-established in the test suite** — 16+ test files use
  it, e.g. `tests/test_cleanup_audit_structure.py:12`,
  `tests/swarm/test_no_scoring_engine.py:73` (parses source & `ast.walk` at
  :170/:183/:210), `tests/swarm/test_inv012_tui_opt_in.py:42` (`ast.parse(source,
  filename=str(path))` :708, `NodeVisitor` mutants :777-817),
  `tests/roadmap/test_threshold_registry.py:27`,
  `tests/roadmap/test_verify_implementation.py:26`, and several `src/` modules
  (`cli/audit/wiring_gate.py:18`, `tools/arch_lint.py:49`). **Idiom**:
  `tree = ast.parse(Path(...).read_text(), filename=str(path))` then
  `for node in ast.walk(tree): ...` / a `ast.NodeVisitor` subclass.
- **`import inspect`** is also used (e.g.
  `tests/roadmap/test_verify_implementation.py`, several `tests/cli/eval/*`), so
  `inspect.getsource` / `inspect.signature` is available as an alternative to
  raw AST if FX3 prefers importing the module.
- **Within `tests/pr_submit/` there is NO existing `import ast`/`inspect`
  introspection.** So **FX3 introduces the AST-introspection pattern into the
  `pr_submit` suite** (but does NOT introduce it to the repo — abundant
  precedent elsewhere to mirror). Recommend mirroring the
  `tests/swarm/test_no_scoring_engine.py` idiom (parse module source by path,
  walk for `FunctionDef`/`ClassDef`), pointing at
  `src/superclaude/pr_submit/contract_setup/questions.py`.

**Parametrize precedent in `tests/pr_submit/`:** module-level
`@pytest.mark.parametrize` is already used in `test_skill_parse.py`,
`test_loop_guard.py`, `test_validation_gate.py`, `test_edge_cases.py`,
`test_pre_pr_checks.py` — so FX5 Option B (parametrized coverage test) matches
existing suite style.

---

## 3. Do FX3/FX5 complement or duplicate existing tests?

- **`probe_pr`** appears in tests ONLY in `test_contract_setup_questions.py`
  (F3 regression `test_probe_pr_question_default_respects_operator_answer`,
  :272-288). That test is **behavioural/value-based** (calls `derive_default`
  and asserts the returned value). **FX3 is structural/static** — AST-introspect
  `questions.py` to assert e.g. every `SetupQuestion.derive_default` references
  an attribute that actually exists on `SetupAnswers` (the F3 root cause was a
  reference to a nonexistent `answers.pr_number`). This **complements** the
  behavioural test: FX3 catches the class of "default reads a field that isn't
  on the answers dataclass" for ALL 16 questions at once, not just `probe_pr`.
  → complementary, not duplicative.
- **`_path_resolves`** (F4 root cause) is referenced in tests only inside
  `test_contract_setup_validation.py` (comments at :132/:158/:183 and the
  behavioural regression `test_severity_path_all_none_does_not_resolve` :180).
  It is a private helper in the validation/candidate module, exercised
  indirectly. FX5's "gate helper needs negative + differential test"
  enforcement would ensure `_path_resolves` (and siblings) each carry BOTH a
  negative (all-None → does-not-resolve) and a differential (present-key →
  resolves) test. The F4 pair already exists
  (`test_severity_path_all_none_does_not_resolve` negative +
  `test_severity_path_present_is_field_backed_and_distinct_from_null`
  differential, :156-197) — so **FX5 would find that helper already covered and
  should PASS for it**, while catching any OTHER gate helper lacking the pair.
  → complementary (enforcement/meta-coverage), not duplicative.

**Implication for the task:** FX3/FX5 are meta-guards over the source, not
re-tests of behaviour. They should be authored to PASS against the current
(post-F1–F4-fix) tree and FAIL only on regression/new-helper-without-coverage.
R1 owns `questions.py` and R2 owns the gate helpers — FX3/FX5 must consume
whatever the CURRENT symbol inventory is (do not hardcode a stale helper list;
enumerate via AST/import at test time).

---

## 4. Verification commands (verified against the worktree Makefile + pyproject)

**Run the pr_submit suite (UV, verified pattern):**
```
uv run pytest tests/pr_submit/ -v
```
Single new file:
`uv run pytest tests/pr_submit/test_setup_questions_resolution.py -v`.
Note: `pyproject.toml addopts` already includes `-v --strict-markers --tb=short`
(pyproject.toml:109-113), so `-v` is redundant but harmless. **`--strict-markers`
means any NEW `@pytest.mark.<x>` must be registered in `pyproject.toml
[markers]` or collection errors** — FX3/FX5 should avoid custom markers (or
register them).

**Scoped ruff for changed paths** (per repo discipline: scope ruff to changed
files, do NOT run a repo-wide `ruff format` — memory
`reference_ruff_version_mismatch_worktree`). CI runs BOTH check and
format-check (see §5), so run both, scoped:
```
uv run ruff check tests/pr_submit/test_setup_questions_resolution.py tests/pr_submit/conftest.py
uv run ruff format --check tests/pr_submit/test_setup_questions_resolution.py tests/pr_submit/conftest.py
```
(memory `reference_make_lint_vs_ci_ruff_format`: `make lint` runs only
`ruff check`; CI ALSO runs `ruff format --check src/ tests/` — a green
`make lint` is NOT a green CI. Always run the scoped `ruff format --check`.)

**Make targets (verified in `Makefile`):**
| Target | Line | Body |
|---|---|---|
| `make test` | :13 | `uv run pytest` (whole suite). |
| `make lint` | :48 | `lint-architecture` + `uv run ruff check .` (repo-wide check; NO format). |
| `make format` | :53 | `uv run ruff format .` (repo-wide — AVOID; reformats ~106 files per memory). |
| `make sync-dev` | :109 | Copies `src/superclaude/{skills,agents,commands,hooks,templates}` → `.claude/`. |
| `make verify-sync` | :166 | Diffs `src/` ↔ `.claude/`, exits 1 on drift. |
| `make verify` | :28 | Package/plugin/health smoke. |

**Relevance to THIS task:** the two new artifacts are pure Python test files
under `tests/pr_submit/` — they touch NO `src/superclaude/{skills,agents,...}`,
so **`make sync-dev` / `make verify-sync` are NOT triggered by FX3/FX5 alone**.
(If R1/R2/etc. edit `contract_setup` source that is pure Python under
`src/superclaude/pr_submit/`, that is also not a sync-dev surface — sync-dev
only mirrors skills/agents/commands/hooks/templates, not the Python package.
Still run `make verify-sync` before commit as a cheap guard, and it is a
mandatory pre-push gate in CI regardless.) The full-suite gate is
`uv run pytest`.

---

## 5. CI test integration (verified against `.github/workflows/`)

Workflows present: `test.yml`, `quick-check.yml`, `boundary-guard.yml`,
`contract3-generator-constraint-lint.yml`, `readme-quality-check.yml`,
`pull-sync-framework.yml`, `publish-pypi.yml`.

**`.github/workflows/test.yml`:**
- Triggers on push/PR to `master`, `integration` (+ `workflow_dispatch`).
- Matrix Python 3.10 / 3.11 / 3.12.
- **Runs `make sync-dev` BEFORE pytest** (audit tests assert src↔.claude
  parity; mirrors are gitignored so CI materialises them) — test.yml:46-51.
- Test step: `pytest -v --tb=short --color=yes` (test.yml:56).
- Coverage step (3.10 only): `pytest --cov=superclaude --cov-report=xml
  --cov-report=term` → uploaded to Codecov with **`fail_ci_if_error: false`**
  (test.yml:59-70). **No hard coverage threshold gate** — Codecov upload is
  non-blocking; there is no `--cov-fail-under` in `addopts` or CI.
- `swarm-marker-matrix` lane runs `pytest tests/swarm/ -m <marker>` (not
  relevant to pr_submit).
- A lint lane runs `ruff check src/ tests/` (test.yml:131-133) **and**
  `ruff format --check src/ tests/` (test.yml:135-137) — confirms new test
  files MUST pass `ruff format --check`.
- Plugin-load + fixtures smoke: `pytest --trace-config | grep superclaude`
  (test.yml:161-163), `pytest --fixtures | grep -E "(confidence_checker|...)"`.

**`.github/workflows/quick-check.yml`:**
- `pytest tests/unit/ -v --tb=short -x` (:33) — note: only `tests/unit/`, so
  `tests/pr_submit/` is NOT in the quick-check pytest lane; it runs in
  `test.yml`.
- `ruff check src/ tests/` (:37) + `ruff format --check src/ tests/` (:41).
- `make verify-sync` (:49) — sync gate is enforced in CI.

**Coverage config** (`pyproject.toml:147-165`): `[tool.coverage.run] source =
["src/superclaude"]`, omits tests; `[tool.coverage.report] exclude_lines`
covers `pragma: no cover`, `raise NotImplementedError`, etc. **No `fail_under`**
→ coverage is reported, not gated.

**Marker registration**: `pyproject.toml:114-146` registers all custom markers
under `--strict-markers`. FX3/FX5 adding an unregistered marker would ERROR in
CI — keep them marker-free or register.

---

## Summary for FX3 / FX5 authors

1. **`tests/pr_submit/conftest.py` has NO collection hooks** — it is pure
   fixtures. Adding a `pytest_generate_tests` (FX5 Option A) is safe and
   additive; the only `pytest_collection_modifyitems` in the repo is in
   `src/superclaude/pytest_plugin.py:206` and pytest runs both, so no conflict.
   A conftest hook cannot cleanly "FAIL" — use `pytest_generate_tests`
   parametrization (per-helper red test) or a plain parametrized test module.
2. **AST introspection is idiomatic repo-wide** (`import ast` in 16+ test
   files; mirror `tests/swarm/test_no_scoring_engine.py`), but **NEW to
   `tests/pr_submit/`** — FX3 introduces it locally, not to the repo. `inspect`
   is also available as an alternative.
3. **FX3/FX5 complement, do not duplicate** existing F3/F4 behavioural
   regressions (`test_probe_pr_question_default_respects_operator_answer`;
   `test_severity_path_all_none_does_not_resolve` + its differential). They are
   meta/structural guards; enumerate the CURRENT symbol inventory at test time —
   do NOT hardcode helper lists (R1/R2 own those sources).
4. **Verification**: `uv run pytest tests/pr_submit/ -v`; scoped
   `uv run ruff check <files>` AND `uv run ruff format --check <files>` (CI
   gates both; `make lint` misses the format check). `make sync-dev`/
   `verify-sync` are NOT triggered by test-only additions but `verify-sync` is a
   mandatory CI gate.
5. **CI**: `test.yml` matrix 3.10–3.12, runs `make sync-dev` then full `pytest`;
   coverage uploaded to Codecov but **non-blocking (no threshold)**;
   `--strict-markers` is on — avoid unregistered markers.

Evidence is file:line throughout; nothing left Unverified.
