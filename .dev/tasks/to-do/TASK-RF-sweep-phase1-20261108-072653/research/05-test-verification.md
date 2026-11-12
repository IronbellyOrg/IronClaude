# Research: Test and Verification

**Topic type:** Test infrastructure, patterns and verification commands
**Scope:** pyproject.toml pytest config, tests/conftest.py, src/superclaude/pytest_plugin.py, subprocess mocking, tmp_path/CliRunner use, markdown pinning tests, AST import checks, directory snapshot diffs, real-git tests, Makefile targets, CI workflows, docs/designs/orchestrator-mode.md section 11
**Status:** Complete
**Date:** 2026-11-08

---

## 1. Pytest configuration

- No `pytest.ini` exists at the repo root (checked with `ls`). Config lives only in `pyproject.toml:107-148` (`[tool.pytest.ini_options]`).
- `testpaths = ["tests"]`, `python_files = ["test_*.py"]`, `python_classes = ["Test*"]`, `python_functions = ["test_*"]` (`pyproject.toml:108-111`).
- `addopts = ["-v", "--strict-markers", "--tb=short"]` (`pyproject.toml:112-116`). `--strict-markers` means any unregistered marker is a collection error.
- `integration` IS registered: `"integration: Integration tests"` (`pyproject.toml:119`). `unit` (118) and `slow` (122) are also registered. Confirmed live: `uv run pytest --markers` lists `@pytest.mark.integration: Integration tests`. So design section 11's claim (`docs/designs/orchestrator-mode.md:731`) holds: no new marker and no `pyproject.toml` edit is needed.
- No `--import-mode`, `rootdir` or `conftest` setting in `pyproject.toml` (grep for `importmode|rootdir|conftest` found nothing), so pytest runs in the default `prepend` import mode.
- Ruff: `line-length = 88`, `target-version = "py310"` (`pyproject.toml:173-175`); lint rules `E, F, I, N, W, TID` (`pyproject.toml:184`). Test files are linted too (CI runs `ruff check src/ tests/`, see section 9).

## 2. Root conftest and the superclaude pytest plugin

`tests/conftest.py`:
- `collect_ignore` skips `sprint/test_property_based.py` (`tests/conftest.py:13-15`).
- Session autouse `_pollution_snapshot` asserts `docs/mistakes/*.md` and `docs/memory/solutions_learned.jsonl` are unchanged after the session (`tests/conftest.py:28-79`). Sweep tests must not write there (they will not, if every write stays in `tmp_path`).
- Function autouse `_redirect_reflexion_writes(tmp_path, monkeypatch)` sets `REFLEXION_OUTPUT_DIR` (`tests/conftest.py:82-117`). It already takes `tmp_path` and `monkeypatch`, so a sweep autouse fixture that also uses them composes cleanly.
- Shared fixtures: `sample_context`, `low_confidence_context`, `sample_implementation`, `failing_implementation`, `temp_memory_dir` (`tests/conftest.py:120-225`). None is relevant to sweep.

`src/superclaude/pytest_plugin.py`:
- `pytest_configure` registers `confidence_check`, `self_check`, `reflexion`, `complexity(level)` (`pytest_plugin.py:20-42`).
- Fixtures: `confidence_checker` (45), `self_check_protocol` (58), `reflexion_pattern` (71), `token_budget` (96), `pm_context` (117).
- `pytest_runtest_setup` skips `confidence_check` tests below 70% (`pytest_plugin.py:148-169`); `pytest_runtest_makereport` records failures of `reflexion` tests (`pytest_plugin.py:172-196`). Sweep tests should carry neither marker.
- Auto-markers, `pytest_collection_modifyitems` (`pytest_plugin.py:206-228`): `unit` if `"/unit/"` is in the file path (219-220), else `integration` if `"/integration/"` is in the path (221-222); `hallucination` / `performance` by file-name substring (225-228).

**Risk for the sweep subprocess guard (design `orchestrator-mode.md:731`):** the auto-marker tests the WHOLE absolute path string (`str(item.fspath)`, `pytest_plugin.py:216`). If the checkout ever lives under a directory named `integration` (CLAUDE.md's worktree examples include a worktree named `integration`), every sweep test gets the `integration` marker, and a guard written as `request.node.get_closest_marker("integration")` would step aside for ALL of them. `Item.add_marker` appends to `own_markers`, so `own_markers` does not help either. Recommended guard check: read the marker the test function itself carries, `any(m.name == "integration" for m in getattr(request.function, "pytestmark", []))`, which only sees decorator marks. (Pytest internals for `add_marker`/`own_markers`: from knowledge of pytest, Unverified in this repo.) The file names `test_readonly.py`, `test_probes_allowlist.py` etc. contain no `hallucination`, `performance` or `benchmark`, so no filename auto-marker fires.

## 3. Does `tests/sweep/` need `__init__.py`? Yes.

- 19 test folders have `__init__.py`, including `tests/__init__.py`, `tests/swarm/`, `tests/recommend/`, `tests/sprint/`, `tests/roadmap/`, `tests/skills/`, `tests/integration/`, `tests/unit/` (`find tests -maxdepth 2 -name __init__.py`). Folders without one: `tests/cli/`, `tests/core/`, `tests/commands/`, `tests/agents/`, `tests/docs/`. Sub-packages with conftests do have one: `tests/cli/reflect/__init__.py`, `tests/cli/eval/__init__.py`, `tests/cli/prd/__init__.py`.
- Basename collision is real: `tests/cli/test_cli_registration.py` sits in a folder WITHOUT `__init__.py`, so in prepend mode it imports as the top-level module `test_cli_registration`. A `tests/sweep/test_cli_registration.py` without `tests/sweep/__init__.py` would also import as `test_cli_registration` and fail collection with an import-file-mismatch error. Other existing basenames the design reuses: `tests/sprint/test_cli_contract.py`, `tests/roadmap/test_cli_contract.py` (both in packages, so no clash once sweep is a package). Existing `conftest.py` files: `tests/swarm/conftest.py`, `tests/cli/reflect/conftest.py`, and 15 more (listed by `find tests -name conftest.py`).
- **Builder instruction:** create an empty `tests/sweep/__init__.py` in the same step as `tests/sweep/conftest.py` (step 1.8), or with the first sweep test file (step 1.4a `test_readonly.py`) if that step lands first. Then `tests/sweep/test_cli_registration.py` imports as `tests.sweep.test_cli_registration`.
- Fixture data folder: follow `tests/cli/reflect/conftest.py:17` (`FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"`) and put captured Orca output under `tests/sweep/fixtures/`.

## 4. Subprocess mocking patterns in existing tests

- `monkeypatch.setattr(subprocess, ...)` at the test level: **no hits** in `tests/` (grep `monkeypatch\.setattr\(\s*subprocess|monkeypatch\.setattr\("subprocess`). There is no existing "patch subprocess to raise" guard to copy.
- `patch("subprocess.Popen")` as a context manager: `tests/roadmap/test_executor.py:357`. `patch("subprocess.run")` with a string target: no hit.
- Patching a module-bound name: `monkeypatch.setattr` on a module's `subprocess`/`run` in `tests/cli/test_install_user_setup.py`, `tests/cli/eval/test_retry_policy.py`, `tests/sprint/test_preflight.py` (grep hits; lines not read).
- **Seam patching (the pattern design section 11 names):** `tests/cli/reflect/conftest.py:58-80`, fixture `patch_git(monkeypatch)` imports the module (`import superclaude.cli.reflect.config as config_mod`, line 65), defines `_fake_git(cwd, *args)` returning canned output keyed on `args[0]` (67-72), applies `monkeypatch.setattr(config_mod, "_git", _fake_git)` (74), and returns a small class exposing the canned values for assertions (76-80). For sweep, `patch_orca`/`patch_git` should follow this shape but also append every argv to a list the fixture returns (the design requires recording, `orchestrator-mode.md:730`).
- Autouse conftest fixture that neutralises a process launch: `tests/sprint/conftest.py:32-55`, `_stub_phase_narrative(request, monkeypatch)` with a per-module opt-out read from `request.module.__name__` (39-40) and a note that a name bound by `from x import y` must be patched in the importing module too (46-55). The sweep guard follows this shape, with the opt-out keyed on the `integration` marker instead of the module name.
- **Guard coverage caveat:** patching `subprocess.run`, `subprocess.Popen`, `os.system` on the modules only catches calls made through the module attribute. If `probes.py` does `from subprocess import run`, the guard misses it. The design's seams call `subprocess.run` (Unverified: `probes.py` does not exist yet; `ls src/superclaude/cli/sweep` fails). Builder should require `import subprocess` + `subprocess.run(...)` in `probes.py`, or the AST test should pin it.
- Patching `os` functions to raise for the publication cases: `tests/sprint/test_recovery.py:610-615` (`monkeypatch.setattr(os, "link", _always_exists)` where `_always_exists` raises `FileExistsError`); `tests/roadmap/test_validate_executor.py:588,607` (`monkeypatch.setattr(os, "replace", boom)`). Use these for the `test_cli_contract.py` link-failure and `os.unlink`-raises cases.

## 5. `tmp_path` and `CliRunner` patterns

- `CliRunner` is used in 70+ test files (grep). Two registration-test shapes:
  - `tests/recommend/test_cli_registration.py:1-35`: module docstring "CLI registration surface test ... (CliRunner, no subprocess)", a `runner()` fixture returning `CliRunner()` (12-13), `runner.invoke(main, ["recommend", "--help"])` (25).
  - `tests/swarm/test_cli_registration.py:98-104`: `CliRunner().invoke(main, ["swarm", "--help"])` and an exit-code check; lines 147-169 show that `importlib.reload` of a CLI package must restore the original group in `finally`, because `superclaude.cli.main` registered the original object. `test_cli_registration.py` for sweep (NFR-006 lazy import) should NOT reload; check `sys.modules` instead (for example, `del sys.modules[...]` via `monkeypatch.delitem(sys.modules, ..., raising=False)` then import and assert `"superclaude.cli.sweep.commands" not in sys.modules` before `sweep_group` is read). Exact approach Unverified (design names the property, not the method).
  - `tests/cli/reflect/conftest.py:40-43`: a `cli_runner` fixture.
- `main` import: `from superclaude.cli.main import main`; groups are registered at the bottom of `src/superclaude/cli/main.py:519-561` with `main.add_command(<group>, name=...)` (sweep's registration line goes there; owned by researcher 2).
- Click version installed: 8.5.1 (`uv run python -c "import click; ..."`). In Click 8.2 and later `CliRunner` keeps stderr separate: parse JSON from `result.stdout`, read `[sweep publish] ...` lines from `result.stderr` (Click behaviour from knowledge, Unverified in this repo; no existing test reads `result.stderr` from a `CliRunner` result).
- `tmp_path` layout pattern: `tests/skills/test_reflect_input_snapshot.py:112-129` (`pkg` fixture builds a package tree under `tmp_path` and returns `(wu, files)`). `HOME` relocation: `tests/pr_submit/test_conflict_scripts.py:60-64` sets `env["HOME"] = str(home)`; for in-process code use `monkeypatch.setenv("HOME", str(tmp_path / "home"))` and `monkeypatch.setenv("XDG_STATE_HOME", ...)`.

## 6. Markdown command and skill pinning tests

- Model file for `tests/commands/test_sweep_command.py`: `tests/commands/test_impact_command.py` (a recent command plus `-protocol` skill pair, issue #323).
  - Module docstring states what is pinned and "CI-safe: pure file-content assertions" (`test_impact_command.py:1-10`).
  - Paths built from the repo: `_REPO = Path(__file__).resolve().parents[2]`, `_COMMAND = _REPO / "src" / "superclaude" / "commands" / "impact.md"`, `_SKILL = .../skills/sc-impact-protocol/SKILL.md` (17-19). Tests read the `src/` copy, never `.claude/`.
  - Helpers: `_text` (125-126), `_frontmatter` naive `key: value` parse of the first `---` block (129-134), `_allowed` splits `allowed-tools` on `", "` (137-138), `_section(text, heading)` (141-142).
  - Pins: frontmatter name and `argument-hint` flags (145-158); `"> Skill sc:impact-protocol"` inside `## Activation` (161-162); skill `name` (165-166); exact allowed-tools set equality (169-170); banned wildcard and mutating tokens (173-182); `~/.claude/...` path present and every `src/superclaude/...` match whitelisted (198-203, the NFR-011 shape); installed path before project `.claude/` path for dual-surface lookups (206-212).
- `tests/commands/` has NO `__init__.py` (section 3), and no `test_sweep_command.py` basename exists anywhere, so a new file there is safe.
- `tests/skills/test_worker_contract.py` (edit at step 1.19, FR-023): reads `src/superclaude/core/WORKER-CONTRACT.md` via `CONTRACT_PATH` (`test_worker_contract.py:18-19`); the never-as-worker tuple is `NEVER_AS_WORKER` (245-254, currently 8 entries); the test is named `test_never_as_worker_list_names_all_seven_commands` (545-546) although the tuple has eight. Adding `/sc:sweep` means appending to `NEVER_AS_WORKER`; renaming the test is optional (semantics owned by researcher 3). Rule phrases live in `RULE_PHRASES` (25) and are parametrized at 540-542, so a WC-14 entry there gets its own test automatically.
- Routing tests to edit or keep green (FR-024): `tests/core/test_how_we_work_routing_table.py` (47 `def test_`), `tests/recommend/test_routing_refresh.py` (24), `tests/commands/test_routing_plugin_parity.py` (2), all present (`ls`; `grep -c '^def test_'`).
- Dual-surface guard for new primitives: `tests/skills/test_primitive_dual_surface_lookup.py` exists (CLAUDE.md names it); run it after adding the sweep command and skill.
- `make lint-architecture` (CI step, section 9) also checks the pair: a command with `## Activation` must have `src/superclaude/skills/sc-<name>-protocol/` (`Makefile:369-384`), every `sc-*-protocol` skill must have `src/superclaude/commands/<name>.md` (385-395), command files warn above 200 lines and fail above 500 (398-410), paired commands need `## Activation` (413-426), and skill frontmatter needs `name:`, `description:`, `allowed-tools:` (429-431).

## 7. AST import check (NFR-004) and snapshot diff (NFR-001) precedents

**AST import check, model:** `tests/swarm/test_concurrency_python_only.py`.
- Forbidden module set as a `frozenset` (`test_concurrency_python_only.py:57-64`).
- `ast.NodeVisitor` subclass with `visit_Import` (198-203, takes `alias.name.split(".", 1)[0]`) and `visit_ImportFrom` (205-212, uses `node.module or ""`).
- `_scan_module(path)` does `ast.parse(source, filename=str(path))` then visits (224-230).
- Existence guard so a missing target cannot pass vacuously (233-242).
- Mutation tests prove the visitor flags a synthetic offender (`test_audit_detects_mutation_subprocess_import`, 357-366).
- Other AST users (grep `ast\.(Import|ImportFrom)`): `tests/swarm/test_no_scoring_engine.py`, `tests/swarm/test_inv012_tui_opt_in.py`, `tests/audit/test_wiring_gate.py`, `tests/roadmap/test_threshold_registry.py`.
- For sweep: one test over `src/superclaude/cli/sweep/classify.py` and `report.py`, forbidden roots `{"subprocess", "click", "os", "shutil"}` (design `orchestrator-mode.md:739`), plus one synthetic mutation case. Note the visitor also catches `from os import path` (root `os`) and `import os.path`; `pathlib` is allowed, since its root is not `os`.

**Snapshot diff, nearest precedent:** `tests/skills/test_reflect_input_snapshot.py:99-109`, `snapshot()` walks `rglob("*")`, skips non-files and cache dirs, and hashes `(relpath, sha256)` rows. The sweep NFR-001 test needs more per entry: path, size, `st_mtime_ns`, SHA-256 (design `orchestrator-mode.md:737`), and it must also record directories, so "the output directory when new" shows up as an added entry. Recommended shape: `{rel: (is_dir, size, st_mtime_ns, sha256-or-None)}` per root (repo root `tmp_path/root`, `HOME`, each XDG dir), taken before and after `CliRunner().invoke(main, ["sweep", "run", ...])`, then assert the added keys are exactly `{".dev/sweeps", ".dev/sweeps/<report>.md"}` (or just the report when the folder existed), and changed and removed are empty. `st_mtime_ns` users already exist: `tests/sprint/test_resume.py`, `tests/roadmap/test_state.py` (grep hits; lines not read).

## 8. Real-git test in `tmp_path` (the one `integration` test)

No existing test runs git in `tmp_path` AND is marked `integration`; the integration-marked tests (`tests/sprint/e2e_real/*`, `tests/sprint/test_preflight.py:315...`, `tests/roadmap/test_convergence_wiring.py:86...`) are not git-in-tmp tests (grep `pytest\.mark\.integration`; files not read in full). Combine two patterns:
- **Git helper with isolated config:** `tests/unit/test_eval_runner_master_checkout.py:22-30`. `_git(cwd, *args)` strips every `GIT_*` variable from `os.environ`, sets `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1`, and runs `subprocess.run(["git", *args], cwd=cwd, env=env, capture_output=True, text=True, check=True)`. Repo creation: `git init -q -b <branch>`, then `-c user.name=... -c user.email=... commit -q --allow-empty -m init` (33-48). A fuller identity block: `tests/pr_submit/test_conflict_scripts.py:48-64` (`_FIXED_IDENTITY` with author, committer, `GIT_TERMINAL_PROMPT=0`, `LC_ALL=C`; `HOME` moved).
- **Skip when git is missing:** `tests/pr_submit/test_conflict_scripts.py:46` (`GIT = shutil.which("git")`) with a module `pytestmark = pytest.mark.skipif(...)` (88-91). For a single test, use `@pytest.mark.skipif(shutil.which("git") is None, reason="git not installed")` stacked with `@pytest.mark.integration`.
- **The four SPEC assertions** (design `orchestrator-mode.md:737`): (1) control, a file outside `.dev/sweeps/` shows in `git status --porcelain`; (2) `git check-ignore -q .dev/sweeps/x.md` exits 0; (3) `git check-ignore -q .dev/tasks/to-do/x.md` exits 1; (4) writing a file under `.dev/sweeps/` leaves `git status --porcelain` byte-identical. The tmp repo must use the REAL repo `.gitignore` (copy `REPO_ROOT / ".gitignore"` into the tmp repo), or the test does not prove FR-025. Current `.gitignore` has `.dev/worktrees/` (242), `.dev/pr-monitor/` (250), `.dev/sprint-state/` (254) and the `!.dev/tasks/**` re-includes (83-85); no `.dev/sweeps` line yet (grep).
- This test calls real `subprocess.run`, so the autouse guard must step aside for it (section 2 risk: key the opt-out on `request.function`'s own `pytestmark`).
- CI runs it: the main test job has no `-m` filter (section 9), and `ubuntu-latest` has git. It needs no history, so the shallow `fetch-depth: 1` clone that skips `tests/troubleshoot/backtest/test_git_replay_integration.py:56-68` does not affect it.

## 9. Makefile targets and CI

Makefile (exact recipes):
- `test`: `uv run pytest` (`Makefile:13-15`); the whole suite, `-v --strict-markers --tb=short` from addopts.
- `lint: lint-architecture` then `uv run ruff check .` (`Makefile:48-50`). So `make lint` runs the architecture checks first.
- `format`: `uv run ruff format .` (`Makefile:53-55`).
- `sync-dev`: copies `src/superclaude/skills/*/` (those with `SKILL.md`, skipping `__*` dirs and `__init__.py`/`__pycache__`) into `.claude/skills/`, plus agents, commands and more (`Makefile:109-...`; read 109-121).
- `verify-sync`: `diff -rq --exclude='__init__.py' --exclude='__pycache__'` per skill against `.claude/skills/<name>`, with MISSING reported as drift (`Makefile:166-178`, rest not read).
- `lint-architecture`: `Makefile:362-431+` (see section 6).

CI, `.github/workflows/test.yml`:
- Job `test`: `uv pip install -e ".[dev]" "pytest-xdist>=3.5,<4"` (29), `make sync-dev` (38), then `pytest -v --tb=short --color=yes -n auto --maxfail=3 --ignore=tests/cli/test_verify_sync_hooks.py` (47). So **every** `tests/sweep/` test, including the `integration` one, runs in CI **under xdist**. Sweep tests must be order-independent and isolated per worker: per-test `tmp_path`, `monkeypatch` only, no module-level mutable state, no `importlib.reload` without restore (`tests/swarm/test_cli_registration.py:155-169`).
- Job `swarm-marker-matrix`: `pytest tests/swarm/ -m imm|inv` (78-80); not relevant.
- Job `lint`: `ruff check src/ tests/` (102), `ruff format --check src/ tests/` (106), the plugin and fixture checks (110, 114), `make verify-deps` (123), `make sync-dev` (127), `make verify-sync` (131), `make lint-architecture` (135), then the serial `tests/cli/test_verify_sync_hooks.py` (142). New test files must pass `ruff format --check` (ruff pinned at `ruff==0.15.20`, `pyproject.toml:54`).
- Other workflows: `boundary-guard.yml`, `contract3-generator-constraint-lint.yml` (not read; Unverified whether they touch sweep).

## 10. Design section 11 test plan mapped to patterns

Source: `docs/designs/orchestrator-mode.md:724-747`. All files are new unless marked edit.

| Test file (design step) | Design line | Pattern to follow (file:line) | Command |
|---|---|---|---|
| `tests/sweep/__init__.py` (empty; with 1.8 or 1.4a) | implied by section 3 here | `tests/swarm/__init__.py`, `tests/cli/reflect/__init__.py` | (collection) `uv run pytest --collect-only -q tests/sweep` |
| `tests/sweep/conftest.py` (1.8): `patch_orca`, `patch_git` recording fakes; autouse guard on `subprocess.run`, `subprocess.Popen`, `os.system` that steps aside for `integration`; fixed `now`; `tmp_path` layout with `HOME` and `XDG_STATE_HOME` | 728-733 | seam fakes `tests/cli/reflect/conftest.py:58-80`; autouse opt-out `tests/sprint/conftest.py:32-55`; fixtures folder `tests/cli/reflect/conftest.py:17`; `tmp_path` tree `tests/skills/test_reflect_input_snapshot.py:112-129` | `uv run pytest tests/sweep -v` |
| `tests/sweep/test_readonly.py` (1.4a, extended 1.11): `_git` argv `--no-optional-locks` at index 1, `-C <path>`, `GIT_OPTIONAL_LOCKS=0`; one git argv per worktree; the real-git test; snapshot diff | 737 | argv recording via `patch_git` above; real git `tests/unit/test_eval_runner_master_checkout.py:22-48` + skip `tests/pr_submit/test_conflict_scripts.py:46,88-91`; snapshot `tests/skills/test_reflect_input_snapshot.py:99-109` (extend with size, `st_mtime_ns`, dirs) | `uv run pytest tests/sweep/test_readonly.py -v`; real-git only: `uv run pytest tests/sweep/test_readonly.py -m integration -v` |
| `tests/sweep/test_probes_allowlist.py`: exact templates, `ValueError` negatives, `$ORCA_CLI_COMMAND`, result classes, budget, byte-limit boundaries, failure modes, `parse_status` | 738 | argv recording fakes as above; `pytest.raises(ValueError)` + `pytest.mark.parametrize` (as in `tests/skills/test_worker_contract.py:540-542`); env via `monkeypatch.setenv`/`delenv`; budget clock: inject a fake clock through the seam (no existing pattern found; Unverified) | `uv run pytest tests/sweep/test_probes_allowlist.py -v` |
| `tests/sweep/test_classify.py`: one parametrized case per rule, `RULES` order pin, D9 join fixtures, SP-07, FR-012 to FR-015, AST import test | 739 | parametrize + pure-function asserts; AST `tests/swarm/test_concurrency_python_only.py:57-64,198-230,233-242,357-366` | `uv run pytest tests/sweep/test_classify.py -v` |
| `tests/sweep/test_report.py`: heading order, sorts, injection fixture, truncation, byte-equal re-render, version line, `Report complete` last line | 740 | heading order like `tests/commands/test_impact_command.py:109-120` (`_HEADINGS` list) applied to rendered text; pure-function asserts | `uv run pytest tests/sweep/test_report.py -v` |
| `tests/sweep/test_cli_registration.py`: `sweep --help`, `sweep run --help` exit 0; lazy import (NFR-006) | 741 | `tests/recommend/test_cli_registration.py:1-35`; reload caution `tests/swarm/test_cli_registration.py:147-169` | `uv run pytest tests/sweep/test_cli_registration.py -v` |
| `tests/sweep/test_cli_contract.py`: run id, binding, window parser, root/output, JSON v1 golden keys, `stem.md`/`stem-2.md`, exit codes, publication failures, `os.unlink` raise | 742 | `CliRunner().invoke(main, [...])`; `os` patches `tests/sprint/test_recovery.py:610-615`, `tests/roadmap/test_validate_executor.py:588,607`; JSON from `result.stdout`, stderr line from `result.stderr` (Click 8.5.1) | `uv run pytest tests/sweep/test_cli_contract.py -v` |
| `tests/commands/test_sweep_command.py` (1.16): section 7.6 assertions | 743 | `tests/commands/test_impact_command.py:17-19,125-212` | `uv run pytest tests/commands/test_sweep_command.py -v` |
| `tests/skills/test_worker_contract.py` (edit, 1.19): section 8 pins | 744 | `NEVER_AS_WORKER` `test_worker_contract.py:245-254`; `RULE_PHRASES` 25, parametrized 540-542 | `uv run pytest tests/skills/test_worker_contract.py -v` |
| `tests/core/test_how_we_work_routing_table.py`, `tests/recommend/test_routing_refresh.py` (edits); `tests/commands/test_routing_plugin_parity.py` (unchanged) | 745 | existing files (semantics: researcher 3) | `uv run pytest tests/core/test_how_we_work_routing_table.py tests/recommend/test_routing_refresh.py tests/commands/test_routing_plugin_parity.py -v` |

NFR-012 has no test file; it is checked by the gates of steps 1.25 to 1.27 (`orchestrator-mode.md:747`).

## 11. Verification command set for the task file

Per step (fast):
- `uv run pytest tests/sweep -v` (design `orchestrator-mode.md:747`)
- `uv run pytest tests/sweep/<file>.py -v` per new file
- `uv run pytest tests/sweep -m integration -v` (the one real-git test only)
- `uv run pytest tests/sweep -m "not integration" -v` (the pure unit set)
- `uv run pytest tests/commands/test_sweep_command.py tests/skills/test_worker_contract.py -v`
- `uv run pytest tests/core/test_how_we_work_routing_table.py tests/recommend/test_routing_refresh.py tests/commands/test_routing_plugin_parity.py tests/skills/test_primitive_dual_surface_lookup.py -v`

Repo gates (final steps, mirroring CI):
- `uv run ruff check src/ tests/` and `uv run ruff format --check src/ tests/` (CI `test.yml:102,106`); fix with `uv run ruff format src/superclaude/cli/sweep tests/sweep`
- `make sync-dev` then `make verify-sync` (CI `test.yml:127,131`)
- `make lint-architecture` (CI `test.yml:135`)
- `uv run pytest -n auto --maxfail=3 --ignore=tests/cli/test_verify_sync_hooks.py` to mirror CI's xdist run (needs `pytest-xdist`, which CI installs separately and which is not in the `dev` extra per `test.yml:26-29`). Checked: the local venv has `pytest 9.2.0` and NO `pytest-xdist` (`uv pip list`), so locally use `make test` (`uv run pytest`) unless the operator installs xdist first.
- Grep gate for NFR-011: `grep -rn 'src/superclaude' src/superclaude/commands/sweep.md src/superclaude/skills/sc-sweep-protocol` (CLAUDE.md rule; design step 1.28).
- Live collection check already run here: `uv run pytest --collect-only -q tests/cli` collects 2472 tests in 4.68 s with no errors; the same command on `tests/sweep` is the cheap check that `__init__.py` and the conftest load.

## Summary

1. **Config is ready; no `pyproject.toml` edit.** `integration` is registered (`pyproject.toml:119`) under `--strict-markers` (114). There is no `pytest.ini`.
2. **`tests/sweep/__init__.py` is required.** Without it, `tests/sweep/test_cli_registration.py` collides with `tests/cli/test_cli_registration.py`, whose folder has no `__init__.py`, so both import as the top-level module `test_cli_registration`.
3. **Guard risk.** The plugin auto-adds `integration` to any test whose absolute path contains `/integration/` (`pytest_plugin.py:216-222`). The autouse subprocess guard should therefore key its opt-out on the function's own `pytestmark`, not on `get_closest_marker`. The guard also misses `from subprocess import run`, so `probes.py` should call `subprocess.run` through the module.
4. **Patterns to copy.** Seam fakes: `tests/cli/reflect/conftest.py:58-80`. Autouse opt-out: `tests/sprint/conftest.py:32-55`. AST import check: `tests/swarm/test_concurrency_python_only.py:57-242`. Snapshot: `tests/skills/test_reflect_input_snapshot.py:99-109`, extended with size, `st_mtime_ns` and directories. Real git: `tests/unit/test_eval_runner_master_checkout.py:22-48` plus a `shutil.which("git")` skip. Command pins: `tests/commands/test_impact_command.py`. `os` failure patches: `tests/sprint/test_recovery.py:615`.
5. **CI runs every sweep test, including the real-git one, under xdist** (`test.yml:47`), and runs `ruff check` and `ruff format --check` on `tests/` (102, 106). Locally xdist is not installed, so use `make test`. The main command is `uv run pytest tests/sweep -v`. The full command set is in section 11.
