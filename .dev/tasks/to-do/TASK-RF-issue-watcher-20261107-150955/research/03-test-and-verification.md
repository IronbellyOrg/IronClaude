# Research 03: Test and Verification Infrastructure

**Topic type:** Test & Verification
**Scope:** tests/, pyproject.toml pytest section, Makefile, .github/workflows/test.yml, docs/designs/issue-watcher.md sections 12, 13, 17
**Status:** Complete
**Date:** 2026-11-07

---

## 1. Pytest configuration (pyproject.toml)

- `pyproject.toml:107` opens `[tool.pytest.ini_options]`: `testpaths = ["tests"]`, `python_files = ["test_*.py"]`, `addopts = ["-v", "--strict-markers", "--tb=short"]` (addopts at 112, `--strict-markers` at 114). No `pytest.ini`, `tox.ini` or `setup.cfg` exists (ls checked).
- `--strict-markers` is on: any `@pytest.mark.<name>` not registered is a collection ERROR. Registered markers are the `markers` list in `pyproject.toml` (about 30 names: `unit, integration, slow, thread_safety, p0, regression, recovery, autonomy, ...`) plus those added by `src/superclaude/pytest_plugin.py:20-40` (`pytest_configure` -> `addinivalue_line`). The design adds no marker, so tests/issue_watch/ should use NO custom marker; built-ins (`parametrize`, `skipif`, `skip`, `xfail`) are always allowed.
- Auto-markers: `src/superclaude/pytest_plugin.py:206-228` `pytest_collection_modifyitems` adds `unit`/`integration`/`hallucination`/`performance` by path fragment (`/unit/`, `/integration/`, ...). `tests/issue_watch/` matches none; harmless.
- Declared runtime deps: `pyproject.toml:34-43` (pytest, click, rich, pyyaml, jsonschema, jinja2, pexpect, httpx). `dev` extra `pyproject.toml:46-56`: pytest-cov, pytest-benchmark, scipy, `ruff==0.15.20` (line 54), mypy. `test` extra 57-61.
- NOT declared anywhere: pytest-xdist, pytest-timeout, hypothesis, pytest-mock, freezegun. Verified in the repo env: `uv run python -c "import xdist"`, `"import pytest_timeout"`, `"import hypothesis"` each print `ModuleNotFoundError`. `tests/conftest.py:12-15` says it outright: `collect_ignore = ["sprint/test_property_based.py"]  # requires 'hypothesis' (not a declared dependency)`.
- CI installs xdist ad hoc, `.github/workflows/test.yml:26-29`: `uv pip install -e ".[dev]" "pytest-xdist>=3.5,<4"`, with the comment "pytest-xdist is installed here, not in the `dev` extra, so uv.lock and scripts/dependency_baseline.txt (the `make verify-deps` allow-list) stay unchanged". Adding any of these to pyproject would need a baseline edit and would break AC-23 / NFR-012 (no new dependency).
- Consequence for tests/issue_watch/: no `@pytest.mark.timeout`, no `hypothesis`, no `mocker`/`freezer` fixtures. Use `subprocess.run(timeout=...)`, `Process.join(timeout)` and the design's `FakeClock` instead. Local `uv run pytest` has no `-n`, CI has `-n auto`: tests must pass both ways.

---

## 2. Test layout, package markers, imports, CLI invocation

### 2.1 Layout (verified with `ls` / loop over `tests/*/`)

- `tests/__init__.py` exists, so test modules in packaged subdirs import as `tests.<dir>.<module>`. Dirs WITH `__init__.py`: audit, audit-trail, cli_portify, contracts, hooks, integration, pipeline, pr_submit, recommend, roadmap, sc-roadmap, skills, sprint, swarm, tasklist, troubleshoot, unit, v3.3, cli/eval, cli/prd, cli/reflect. Dirs WITHOUT: agents, cli (top level), commands, core, docs.
- Basename collision rule: files in no-`__init__` dirs import by bare basename (pytest default prepend mode). `find tests -name test_cli.py` (and test_runner, test_cycle, test_record, test_audit, test_launch, test_github, test_predicates, test_no_shell, test_concurrency, test_module_boundaries) finds only `tests/cli_portify/test_cli.py`, which is inside a package. So `tests/issue_watch/__init__.py` (design C14, section 11 row) makes every planned module name safe; without it `test_cli.py` would still be importable only if no other rootless `test_cli.py` exists, but `__init__.py` removes the risk. The repo precedent for sibling imports is `from .conftest import _FAKE_BASE` (`tests/cli/reflect/test_cli_smoke.py:19`) and `from tests.pr_submit.test_conflict_scripts import (... make_repos)` (`tests/pr_submit/test_conflict_e2e.py:61-71`). Both work only because the dir is a package.
- No tracked executable file exists under `tests/`: `git ls-files -s tests | awk '$1=="100755"'` printed nothing. Every existing stub is WRITTEN AT RUNTIME into `tmp_path` and `chmod(0o755)`. The design (section 11, line 765) instead plans committed `tests/issue_watch/stubs/gh` and `stubs/orca`. Both `git check-ignore -v tests/issue_watch/stubs/gh tests/issue_watch/fixtures/_assumed_shape/x.json tests/issue_watch/__init__.py` returned exit 1 (nothing ignored), so committing is possible, but a committed stub must keep the exec bit (`git add --chmod=+x`) or, safer and in the repo's style, the test copies it into `tmp_path / "bin"` and calls `chmod(0o755)` (as `install_gh_stub` does, `test_conflict_e2e.py:145`). Recommend copy-then-chmod so xdist workers never share one path and a lost bit cannot break CI.
- `.gitignore` has no pattern matching `stubs`, `fixtures`, `*.json` under tests (grep of `.gitignore`: only `.dev/sprint-state/` and similar at lines 252-257).

### 2.2 How existing tests invoke Click commands

- Preferred in-process: `click.testing.CliRunner`. 70 test files use it (`grep -rl CliRunner tests | wc -l` = 70). Two styles:
  - Root app: `from click.testing import CliRunner` (`tests/cli/test_cli_registration.py:24`), `from superclaude.cli.main import main` (line 26), `runner.invoke(main, ["--help"])` (line 63), `runner.invoke(main, [name, "--help"])` (line 103).
  - Group object directly: `from superclaude.cli.reflect.commands import reflect_group` (`tests/cli/reflect/test_cli_smoke.py:15`), `cli_runner.invoke(reflect_group, ["--help"])` (line 49), with a fixture `def cli_runner() -> CliRunner: return CliRunner()` (`tests/cli/reflect/conftest.py:41-43`).
- Installed Click is 8.5.1 (`uv run python -c "import click"` and `uv.lock` line 109 `version = "8.5.1"`); `pyproject.toml:36` floor is `click>=8.0.0`. `grep -rn mix_stderr tests src` finds nothing: no test uses `CliRunner(mix_stderr=...)`, so do not (it was removed in Click 8.2). Use `result.output`, `result.stderr`, `result.exit_code` only after checking against 8.0 semantics: on Click 8.0/8.1 `result.stderr` raises unless `mix_stderr=False`, so for stderr assertions that must hold at the floor, prefer the subprocess style below. (Unverified: no CI job runs the Click floor; `uv.lock` pins 8.5.1.)
- Exit-code assertions: `CliRunner` captures `SystemExit` into `result.exit_code`, so `sys.exit(75)`/`ctx.exit(75)` is assertable in-process. Real-process exit codes (and `fcntl.flock` between processes) need a subprocess.
- Subprocess style (when a real exit code, stdout/stderr split, env or PATH is under test): `tests/swarm/test_inv012_tui_opt_in.py:130-143`:
  ```python
  if _superclaude_cli_available():
      cmd: list[str] = ["superclaude", "swarm", *args]
  else:
      cmd = [sys.executable, "-m", "superclaude.cli.main", "swarm", *args]
  return subprocess.run(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
      stderr=subprocess.PIPE, env=_piped_env(), text=True, check=False, timeout=30)
  ```
  `src/superclaude/cli/main.py` ends with `if __name__ == "__main__": main()` (last lines of the file), so `[sys.executable, "-m", "superclaude.cli.main", "issue-watch", ...]` works with no PATH lookup of `superclaude`; this is the right form for the PATH-stub e2e test because PATH is then dedicated to the stubs. The other precedent resolves the console script and skips if absent: `tests/cli/eval/test_exit_codes.py:70-80` (`Path(sys.executable).parent / "superclaude"`, then `shutil.which`, else `pytest.skip`). Every subprocess call has `timeout=` (30, 60, 120, 180 seen).
- Patching style for external effects in non-stub tests: `monkeypatch.setattr(setup.shutil, "which", lambda name: ...)` and `monkeypatch.setattr(setup.subprocess, "run", fake_run)` (`tests/cli/test_install_user_setup.py:261, 281-282`). The design replaces this with an injected `Runner`, so `test_no_shell` (only `runner.py` may import `subprocess`) stays satisfiable.

---

## 3. The PATH-stub pattern (quoted, with file:line)

Source files: `tests/pr_submit/test_conflict_scripts.py` (helper `make_repos`, dataclass `Repos`) and `tests/pr_submit/test_conflict_e2e.py` (richer stubs). The e2e test imports `Repos`, `make_repos`, `_merge_tree_works` from the scripts file (`test_conflict_e2e.py:61-71`).

**Step 1: a private bin dir and a calls log inside `tmp_path`; the base stub records argv and prints `{}`** (`test_conflict_scripts.py:165-177`):
```python
bin_dir = tmp_path / "bin"
bin_dir.mkdir()
gh_calls = tmp_path / "gh-calls.log"
gh = bin_dir / "gh"
gh.write_text(
    "#!/usr/bin/env bash\n"
    f"printf '%s\\n' \"$*\" >> '{gh_calls}'\n"
    "printf '{}\\n'\n",
    encoding="utf-8",
)
gh.chmod(0o755)
```
**Step 2: PATH prepended in an env dict that is handed to every `subprocess.run`, never set globally** (`test_conflict_scripts.py:60-64, 178-179`):
```python
def _base_env(home: Path) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(_FIXED_IDENTITY)
    env["HOME"] = str(home)
    return env
...
env = _base_env(home)
env["PATH"] = f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}"
```
`_FIXED_IDENTITY` (lines 48-57) = `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, fixed author/committer name and email, `GIT_TERMINAL_PROMPT=0`, `LC_ALL=C`. `HOME` points into `tmp_path/"home"` (line 165).

**Step 3: a scenario-driven stub: `case "$1 $2"` on the verb, canned JSON served from a file the test rewrites, unknown call recorded then failed** (`test_conflict_e2e.py:118-146`):
```python
_GH_STUB = """#!/usr/bin/env bash
printf '%s\\n' "$*" >> '@CALLS@'
case "$1 $2" in
  "pr view") cat '@PR_VIEW@' ;;
  "repo view")
    printf '%s\\n' \\
      '{"mergeCommitAllowed":true,...}' ;;
  "api repos/"*"/check-runs?per_page=1") printf '1\\n' ;;
  "api repos/"*"/status") printf '0\\n' ;;
  *) printf 'unexpected gh call: %s\\n' "$*" >&2; exit 1 ;;
esac
"""
def install_gh_stub(repos):
    pr_view = repos.root / "gh-pr-view.json"
    stub = repos.bin_dir / "gh"
    stub.write_text(_GH_STUB.replace("@CALLS@", str(repos.gh_calls)).replace("@PR_VIEW@", str(pr_view)), encoding="utf-8")
    stub.chmod(0o755)
    return pr_view
```
(abridged; the repo-view JSON line has three keys.) Templating uses `str.replace` on `@NAME@` tokens so the bash is not an f-string with escaped braces.

**Step 4: per-run knobs through env vars the stub reads** (`test_conflict_scripts.py:1691-1719`, `test_conflict_e2e.py:466-481, 503-515`): `GH_STUB_RUNS`/`GH_STUB_STATUSES` (value `FAIL` makes the stub print `HTTP 502` to stderr and exit 1), `UV_STUB_CALLS` (log path), `UV_STUB_LOCK` (canned file). `env = {**repos.env, "GH_STUB_RUNS": runs, ...}`.

**Step 5: asserting the log.** `Repos.gh_call_lines()` (`test_conflict_scripts.py:155-158`) returns `gh_calls.read_text().splitlines()` or `[]` when the file is absent. Typical assertions: `assert repos.gh_call_lines() == [], "the probe must not call gh"` (line 250); `assert_no_retrigger_call` loops over lines with `line.startswith(allowed)` and rejects tokens such as `--method`, `-f` (`test_conflict_e2e.py:178-186`). A hang/timeout stub: a fake `timeout` that exits 124 (`test_conflict_scripts.py:1510-1517`). A restricted PATH (only symlinks to chosen tools, `PATH=str(bin_dir)`) at lines 1555-1571.

**Caveats an implementer must handle (the existing pattern is NOT enough for the design's asserts):**
1. Flat argv log. `printf '%s\\n' "$*"` joins argv with spaces, so an element containing a space or newline is indistinguishable. The design asserts "launch argv equals the 12-element list" (AC-8) and the D3 prompt is a multi-word string. The watcher stubs must log one argv element per record: e.g. `for a in "$@"; do printf '%s\0' "$a"; done >> "$LOG"; printf '\n--END--\n'`, or write JSON with `jq -n '$ARGS.positional' --args "$@"` (`jq` is on PATH here: `/usr/bin/jq`; CI ubuntu runners ship jq; `_merge_tree_works()` already requires it, `test_conflict_scripts.py:69`). Preferred: `printf '%s\\0' "$@"` with a record separator, parsed with `split("\\0")`. This is a new variation, not an existing helper.
2. Real `gh` and `orca` are on the PATH here (`which gh orca` -> `/home/coder/.local/bin/gh`, `/home/coder/.config/orca/linux-orca-cli-shim/orca`). That is why the design adds a guard: `assert shutil.which("gh", path=env["PATH"]) == str(stub)` (pass `path=` so no process-global PATH mutation is needed). The existing pattern never asserts this.
3. The stubs must not need `git`: the spec says "stub `gh`, `git` and `orca` executables" (`spec-final.md:112`) but design section 12 lists only `stubs/gh` and `stubs/orca`. `origin_repo.py` shells to `git remote get-url origin`; the e2e test either builds a real tmp git repo with `git init` + `git remote add origin <url>` under `_FIXED_IDENTITY`, as `make_repos` does, or ships a third `stubs/git`. Design section 12 says "No test runs a real ... git", so this needs a decision in the task file (a stub `git` that answers `-C <abs> remote get-url origin`).
4. Stub scripts use `#!/usr/bin/env bash`; tests that need bash/jq use a capability skip: `pytestmark = pytest.mark.skipif(not _merge_tree_works(), reason=...)` (`test_conflict_e2e.py:75-78`) and `@pytest.mark.skipif(shutil.which("uv") is None, ...)` (line 698). CI is ubuntu-latest so bash is present.
5. The sleeping stub for AC-19 (`gh_timeout`): the production timeout is 20 s (design section 14), so the stub must exit-sleep controllably and the test must lower the timeout through the config/Clock seam, not wait 20 s. Existing precedent for time-bounded subprocess waits: `holder.wait(timeout=60)` (`tests/unit/test_ccsession_tag.py:4509`).

---

## 4. Fixtures and hooks every test in tests/issue_watch/ inherits (collision map)

`tests/conftest.py` (225 lines), applies to the whole tree:
- `collect_ignore = ["sprint/test_property_based.py"]` (lines 13-15).
- Session-scoped autouse `_pollution_snapshot` (lines 28-79): snapshots `docs/mistakes/*.md` names and the size of `docs/memory/solutions_learned.jsonl` at session start and ASSERTS at teardown that neither changed. A watcher test that writes under the repo's `docs/` would fail the whole session. All state must go to `tmp_path`.
- Function-scoped autouse `_redirect_reflexion_writes(tmp_path, monkeypatch)` (lines 82-117): only `monkeypatch.setenv("REFLEXION_OUTPUT_DIR", str(tmp_path / "docs" / "memory"))`; it does NOT create the directory (docstring lines 111-115 explain why), so `tmp_path` is still empty when the test body starts. A test asserting "state dir is empty / nothing written" is safe if it uses `tmp_path` itself, but safer to use a child (`tmp_path / "state"`) because the env var `REFLEXION_OUTPUT_DIR` exists in `os.environ` of every test; scrub it (or build the subprocess env from a small allow-list) in the e2e test so the stubbed child sees a minimal env.
- Plain fixtures: `sample_context` (120), `low_confidence_context` (140), `sample_implementation` (160), `failing_implementation` (184), `temp_memory_dir` (205, creates `tmp_path/docs/memory` with `mkdir(parents=True)`: do not combine it with any fixture that also creates that path).
`src/superclaude/pytest_plugin.py` (auto-loaded entry point `pyproject.toml:76`): fixtures `confidence_checker` (45), `self_check_protocol` (58), `reflexion_pattern` (71), `token_budget` (96), `pm_context` (117); hooks `pytest_runtest_setup` (148, only acts on `@pytest.mark.confidence_check`), `pytest_runtest_makereport` (172, only on `reflexion`), `pytest_collection_modifyitems` (206-228, path-based markers).
Collision conclusion: the design's fixture names `FakeRunner`, `FakeClock`, `FakeLauncher`, `CrashingStore`, `tmp_state` do not collide with any of the above. Directory-level `conftest.py` files shadow rather than collide (pr_submit: `load_fixture`, `mock_gh`, `mock_monitor`, `fixture_findings`, `tmp_skill_dir`, `assert_gate_helper_coverage` at `tests/pr_submit/conftest.py:28-257`; swarm: `imm_coverage_map`, `inv_coverage_map`; reflect: `cli_runner`, `temp_tasklist`, `patch_git`, `patch_runner_env`, `make_claude_process_stub`). `tests/issue_watch/conftest.py` may define `cli_runner` locally, same as reflect (`tests/cli/reflect/conftest.py:40-43`). Avoid the name `mock_gh` (exists in pr_submit; harmless across dirs but confusing).
Style helpers in the repo's idiom: `tmp_path` (pytest built-in) for every dir; `monkeypatch.setenv`/`setattr` for env/attrs; `REPO_ROOT = Path(__file__).resolve().parents[2]` for repo paths from `tests/<pkg>/test_*.py` (`tests/swarm/test_contract_surface.py:74`; a `tests/issue_watch/test_*.py` file is at the same depth so `parents[2]` is the repo root); `from __future__ import annotations` first import in new test files (`test_conflict_e2e.py:23`, `test_cli_smoke.py:8`).

---

## 5. xdist-safety rules visible in the repo

- CI: `.github/workflows/test.yml:40-47` `pytest -v --tb=short --color=yes -n auto --maxfail=3 --ignore=tests/cli/test_verify_sync_hooks.py` (comment lines 41-45: "the suite passed under xdist locally"; "4 [CPUs] on public-repo runners"). The `swarm-marker-matrix` job (lines 49-80) and the `lint` job's final step (lines 137-142) run pytest without `-n`.
- The only written xdist rule in the tests: `tests/cli/test_verify_sync_hooks.py:7-15` "DO NOT RUN WITH pytest-xdist: the tests mutate real repository files in `src/superclaude/hooks/` ... would race on shared files". Translation: no test may write into the checkout; everything goes to `tmp_path` (unique per test, per worker).
- No `worker_id` / `PYTEST_XDIST_WORKER` handling exists in `tests/` (grep for `xdist|worker_id|PYTEST_XDIST` shows only the verify-sync docstring and an unrelated sprint helper arg). So there are no session-scoped shared temp dirs to copy. Rules for tests/issue_watch/: (1) per-test state dir under `tmp_path`; (2) set `XDG_STATE_HOME`/`HOME` via `monkeypatch.setenv` or the subprocess `env=`, never rely on the real `~/.local/state`; (3) do not mutate `os.environ["PATH"]` in a way that outlives the test (use `monkeypatch`); (4) no fixed ports, no fixed `/tmp` names; (5) session-scoped fixtures only for read-only data; (6) the multiprocess lock test uses its own `tmp_path` store (design C11, `issue-watcher.md:92`).
- `-n auto` workers are separate processes, so `fcntl.flock` between two test workers cannot interact unless they share a path; per-test `tmp_path` guarantees they do not.
- Python floor: CI runs 3.10 (`test.yml:22`); this machine runs 3.11.15 (`uv run python -c "import sys"`), 3.13.5 system, and `uv python list --only-installed` shows no 3.10. So locally nothing catches 3.11-only APIs. ruff's `target-version = "py310"` (`pyproject.toml:175`) with `select = [E,F,I,N,W,TID]` (line 184) does NOT flag `datetime.UTC`, `tomllib`, `enum.StrEnum`, `typing.Self`, `ExceptionGroup`, `asyncio.timeout`. A cheap self-check before finishing: `grep -rnE 'tomllib|datetime\.UTC|StrEnum|import Self|ExceptionGroup|asyncio\.timeout' src/superclaude/cli/issue_watch tests/issue_watch`. The design already states the rule (section 13, `issue-watcher.md:805`).

---

## 6. The gates: exact commands, what each does, cost, local caveats

Design section 13 (`docs/designs/issue-watcher.md:793-803`) lists seven gates; section 17 AC-23 says "gates in section 13 pass". All seven source citations were re-read in this checkout and hold (see section 9).

| Gate (command) | What it actually runs | Measured here | Caveat for the implementer |
|---|---|---|---|
| `uv run pytest tests/issue_watch/ -v` | pytest with `addopts` `-v --strict-markers --tb=short` (`pyproject.toml:112-116`), serial, no xdist | `tests/issue_watch/` does not exist yet; no timing possible | `-v` is already in addopts (duplicate is harmless). The loop for development; add `-x -q` to shorten. |
| `make test` (`Makefile:13-15`) | `echo` then `uv run pytest` over `testpaths = ["tests"]`: the WHOLE suite, serial | Collection only: `uv run pytest --collect-only -q` = 17,096 tests collected in 17.56 s (19.2 s wall); with `tests/pr_submit tests/cli`: 4,256 tests in 5.47 s. Full run time is NOT recorded anywhere I could find (`grep` of `Makefile` for minutes/seconds/passed found nothing; CI log not available). UNVERIFIED. | Too large to run in an agent turn without an owner decision; machine has 28 cores (`nproc`) but xdist is NOT installed locally (`import xdist` fails), so `-n auto` is unavailable here without `uv pip install pytest-xdist` (a local env change; and it must not enter `pyproject.toml`). It includes `tests/cli/test_verify_sync_hooks.py`, which rewrites real files in `src/superclaude/hooks/` and `install_hooks.py` in place (docstring lines 7-15): never run it while other edits or sessions touch this worktree. CI excludes it from the parallel job and runs it serially in the lint job (`test.yml:47, 137-142`). Also `.claude/skills` does not exist in this worktree (`ls .claude` = `agent-memory cache settings.json`), so audit tests asserting src/.claude byte parity fail locally until `make sync-dev` has run (CI does it first, `test.yml:32-38`). Recommended affected subset instead of the whole suite: `uv run pytest tests/issue_watch/ tests/cli/test_cli_registration.py tests/swarm/test_cli_registration.py tests/recommend/test_cli_registration.py -q` (the registration tests iterate `main.commands`; no test asserts an exact top-level command set, so adding `issue-watch` cannot break them: grep of `set(main.commands`, `== EXPECTED`, `len(main.commands` over `*registration*.py` found nothing; `tests/cli/test_cli_registration.py:31-49` `EXPECTED_TOP_LEVEL_COMMANDS` is only used to loop `--help`, lines 102-106). |
| `make lint` (`Makefile:48-50`) | `lint: lint-architecture`, then `uv run ruff check .` | `uv run ruff check .` -> "All checks passed!" in 0.06 s on the current tree. `uv run python -m superclaude.tools.arch_lint --check-contracts src/superclaude/contracts/__init__.py --scan-paths src/superclaude/cli/` -> "arch-lint: PASS" in 0.9 s | `lint-architecture` (`Makefile:362-493`) runs checks 1-4, 6, 8-11; only Check 11 (lines 467-476) touches `src/superclaude/cli/`: flags rebinding of `contracts.__all__` names (`ID_PATTERNS`, `CONVERGENCE_THRESHOLDS`, `GATE_FIELD_NAMES`, `THRESHOLDS`, `RETURN_CONTRACTS`, `AdversarialReturn`, ...), a string literal equal to an `ID_PATTERNS` body (e.g. `FR-\d+(?:\.\d+)?`, `contracts/__init__.py:72-76`), or a class named like a canonical class. Opt-out marker `# arch-lint: allow-duplicate <reason>` exists but the design says none is needed. Do not write requirement-id regexes (`FR-\d+`) in the new package or in docstring-adjacent constants. Note: a file named `*_validator.py`, `gates.py` or `structural_checkers.py` triggers the Contract-3 PR-body check (`.github/workflows/contract3-generator-constraint-lint.yml` paths filter); the planned module names (runner, github, predicates, record, launch, audit, cycle, cli) avoid it. |
| `uv run ruff format --check src/ tests/` (`test.yml:106`) | format check, no make target (`make format` at `Makefile:53-55` REWRITES) | Local `uv run ruff` resolves to `/usr/local/bin/ruff` **0.17.3** (`.venv/bin/ruff` does not exist; `which -a ruff` shows one binary), NOT the pinned 0.15.20 (`pyproject.toml:54`, `uv.lock` line 1563-1564). With 0.17.3: "12 files would be reformatted, 1757 files already formatted"; the 12 are all Markdown files (`src/superclaude/skills/**/*.md`, `src/superclaude/examples/release-spec-template.md`, `tests/roadmap/fixtures/recurrence/*/*.md`): 0.17 formats Python code blocks inside `.md`. With the pinned version: `uvx --offline ruff@0.15.20 format --check src/ tests/` -> "1204 files already formatted"; `uvx --offline ruff@0.15.20 check src/ tests/` -> "All checks passed!". | Run the pinned form locally: `uvx --offline ruff@0.15.20 format --check src/ tests/` (works offline, cached) and `uvx --offline ruff@0.15.20 check src/ tests/`. A bare `uv run ruff format --check src/ tests/` is red here for reasons unrelated to the task. Do not put Python code blocks in new `.md` fixtures under `tests/`. The `ruff format` run must also cover `tests/issue_watch/*.py`, so format new test files (`uvx ruff@0.15.20 format <files>`) before the check. |
| `make verify-deps` (`Makefile:356-359`) | `uv run python scripts/verify_deps.py` then `echo EXIT=$$?`: compares `uv pip list --format=json` names with `scripts/dependency_baseline.txt` (95 lines); exit 0 subset OK, 1 extra package, 2 baseline missing (`scripts/verify_deps.py:1-14`) | not run (it audits the live env; harmless but depends on local env); `uv pip list | wc -l` = 29 lines | CI audits a separate lock-resolved env via `UV_PROJECT_ENVIRONMENT` (`test.yml:116-123`). Passes as long as no import in the new package needs a package outside the stdlib + declared deps. Stdlib only is the design (`fcntl`, `json`, `subprocess`, `re`, `os`, `time`, `datetime`, `hashlib`, `dataclasses`, `click`). |
| `make sync-dev` (`Makefile:109-...`) | copies `src/superclaude/{skills,agents,commands,hooks,templates}` to `.claude/` (gitignored) | not run | Preparation only. `.claude/` contents must never be staged (project CLAUDE.md). The task touches none of those source dirs. |
| `make verify-sync` (`Makefile:166-...`) | compares `src/superclaude/*` against `.claude/*`; exit 1 on drift ("Drift detected! Run 'make sync-dev'", `Makefile:351`) | not run | Currently would report MISSING because `.claude/skills` is absent here; run `make sync-dev` first. Unaffected by the change. |

CI jobs touching the change (`.github/workflows/test.yml`): `test` (lines 11-47: setup-uv, `uv pip install -e ".[dev]" "pytest-xdist>=3.5,<4"`, `make sync-dev`, pytest `-n auto --maxfail=3 --ignore=tests/cli/test_verify_sync_hooks.py`), `lint` (82-142: `ruff check src/ tests/` line 102, `ruff format --check src/ tests/` line 106, plugin-load check 108-110, fixtures check 112-114, `make verify-deps` 123, `make sync-dev` 127, `make verify-sync` 131, `make lint-architecture` 135, verify-sync hook tests serial 137-142), `doctor-check` (144-189: `superclaude install` + `superclaude doctor --verbose`; unaffected unless `main.py` import breaks), `test-summary` (191-200). `boundary-guard.yml` only triggers on swarm merge paths; `contract3-generator-constraint-lint.yml` only on `gates.py`, `structural_checkers.py`, `*_validator.py`. Neither is relevant.

---

## 7. Writing the cross-cutting tests with no new dependency or marker

Each recipe names the in-repo precedent to copy.

1. **AST import-graph test (`test_module_boundaries.py`, NFR-014, AC-25).** Design table `issue-watcher.md:233-242`. Parse each `src/superclaude/cli/issue_watch/<mod>.py` with `ast.parse(path.read_text(encoding="utf-8"))`, collect `ast.Import` / `ast.ImportFrom` (resolve `level > 0` relative imports against the package name), and compare to an allow-table dict. Precedent: `tests/swarm/test_output_confinement.py:21, 331-357` (`import ast`; `_calls_named` / `ast.walk`), `tests/swarm/test_parallel_executor_routing.py:343-364` (offender list joined into the assert message). Copy the "mutation guard" idea (`test_parallel_executor_routing.py:372-406`): also feed the detector a synthetic bad module string (`ast.parse("from superclaude.cli.cycle import x\n")`) and assert it is flagged, so the test cannot pass vacuously. Path idiom: `REPO_ROOT = Path(__file__).resolve().parents[2]`. Remember `from __future__ import annotations` and `if TYPE_CHECKING:` imports are real `ImportFrom` nodes; decide whether TYPE_CHECKING imports count (design says `record` imports `predicates` "types only", `issue-watcher.md:239`). The design also requires "no module named `select`": assert no `.py` basename `select` in the package dir.
2. **No-shell AST test (`test_no_shell.py`, NFR-004, AC-21).** Walk every module: fail on `ast.keyword(arg="shell")` whose value is truthy constant, on `os.system`/`os.popen` calls, and on any `import subprocess` / `from subprocess import` outside `runner.py`. Same precedent and same mutation-guard trick. `tests/swarm/test_parallel_executor_routing.py` also shows the "AST tolerates docstring mentions" argument (lines 349-352), important because the design docstrings will say "shell=False".
3. **Concurrency test (`test_concurrency.py`, FR-017, AC-11): two real processes, no new package.** The repo has NO use of the `multiprocessing` module in `tests/` (`grep -rn "import multiprocessing|from multiprocessing|ProcessPoolExecutor|os.fork(" tests` matched only a docstring in `test_parallel_executor_routing.py`). Two repo precedents for real lock contention: (a) `subprocess.Popen([sys.executable, "-c", "import fcntl, sys, time; f = open(sys.argv[1], 'a'); fcntl.flock(f, fcntl.LOCK_EX); print('held', flush=True); time.sleep(...)", path], stdout=PIPE, text=True)`, wait for the `held` line, then act, `holder.kill()`; `holder.wait(timeout=60)` (`tests/unit/test_ccsession_tag.py:4496-4518`: it also proves a killed holder frees the lock); (b) in-process `fcntl.flock(lock_file, LOCK_EX | LOCK_NB)` on an open file while the code under test runs in a subprocess (`tests/hooks/test_freshness_subagent_start_policy.py:72-89`). `flock` conflicts between two separate `open()`s even in one process, so FR-017's "exit 75 `lock_held`" can be shown by holding the lock from the test and running `once`; the design's "two `multiprocessing` processes ... one launch total" can use `multiprocessing.get_context("spawn")` (the default `fork` is Linux's default on 3.10/3.11 and is risky under xdist/pytest threads); with spawn, the target must be a module-level function in an importable module, which works because `tests/issue_watch/__init__.py` makes it `tests.issue_watch.test_concurrency` and `spawn` forwards the parent's `sys.path`. Every `Process.join()` needs a `timeout=` (no pytest-timeout), and an `assert p.exitcode is not None` after join. Either way the store is `tmp_path / "state"` created by `init-state`, never a shared path. UNVERIFIED: whether a `multiprocessing` test is stable under `-n auto` on CI (no precedent in repo); the subprocess form (a) has precedent in a suite that runs under xdist.
4. **Crash injection by `SystemExit` (`test_crash_injection.py`, NFR-005, AC-22).** `CrashingStore(real, crash_at="C1".."C5")` raises `SystemExit` at the named point (design 7.6 table `issue-watcher.md:525-531`). In-repo precedent for treating `SystemExit` as a crash-like exception: parametrised `[KeyboardInterrupt, SystemExit]` with ids `["sigint", "sysexit"]` (`tests/cli/eval/test_eval_lifecycle.py:642-650`). Facts that make it faithful: `SystemExit` is a `BaseException`, so `except Exception` in production code does not swallow it; `pytest.raises(SystemExit)` catches it; under `CliRunner` it becomes `result.exit_code` (so call the cycle function directly for crash points, use `CliRunner` for exit-code tests). Differences from a real kill that the test must compensate for: `finally`/`with` blocks DO run on `SystemExit` (the lock is released, a `tempfile` cleanup could run), but a real SIGKILL leaves the lock file unlocked (kernel frees it) and leaves an orphan `dispatch.json.*.tmp` at C2; the C2 case therefore should plant an orphan tmp file by hand and assert the next cycle ignores it (design 7.6 row C2).
5. **Time without sleeping.** `FakeClock(now, mono)` with `advance(s)` (design `issue-watcher.md:777`); no `time.sleep` anywhere; for the `test_fifty_cycles` / `test_acceptance_property` cases advance the fake clock by hours between cycles. No `freezegun`.
6. **Property-style tests without hypothesis (design C15, `issue-watcher.md:96`).** Table-driven `@pytest.mark.parametrize` over a fixed hostile corpus plus `random.Random(seed)`-generated strings (a literal seed in the test). `property_based` is a registered marker (`pyproject.toml:135`) but its text says hypothesis and the only user, `tests/sprint/test_property_based.py:83-125`, is in `collect_ignore` (`tests/conftest.py:14`); recommended: do not tag, to avoid `-m property_based` selecting a test that does not use hypothesis. (Judgment, not a repo rule.)
7. **Hostile-text test (`test_no_text.py`, AC-7).** Use sentinel strings like `PWNED-TITLE` in `FakeRunner` replies and `rg`-style assertion over the audit file, store file, recorded launch prompt and captured stdout/stderr (`CliRunner` `result.output`, or the files under `tmp_path`).
8. **Marker contract test (`test_marker_contract.py`).** Reads `src/superclaude/skills/sc-issue-protocol/refs/claim.md` and `templates/claim-comment.md` "through the dual surface" (design `issue-watcher.md:791`): the repo CLAUDE.md rule (project CLAUDE.md "Never Hardcode `src/superclaude/` Paths in Installed Primitives") applies to primitives, not to tests; tests already use `REPO_ROOT / "src/superclaude/..."` (`tests/hooks/test_freshness_subagent_start_policy.py:92`, `tests/pr_submit/test_conflict_scripts.py:40-44`). Dual surface here = installed `~/.claude/skills/...` first or the checkout copy; in CI `~/.claude` has no skills, so the checkout path must be the guaranteed one. Unverified: the exact dual-surface helper the design intends (another researcher covers `origin_repo.py`/`claim.md`).

---

## 8. Acceptance criteria (section 17) mapped to test files (INFERRED by the researcher; the design gives file names in sections 11/12 and AC text in 17 but no AC-to-file table)

Design section 17 intro (`issue-watcher.md:870`): "All criteria run under `uv run pytest tests/issue_watch/` with fakes or PATH stubs only." 25 ACs. Files named in section 11 (`issue-watcher.md:761-765`): per-module `test_{runner,github,predicates,record,launch,audit,cycle,cli}.py`; cross-cutting `test_{cli_e2e,security_invariants,crash_injection,concurrency,no_shell,no_text,origin_parity,marker_contract,find_orca_parity,module_boundaries,slo_helper}.py`; `fixtures/_assumed_shape/*.json`; `stubs/gh`, `stubs/orca`.

| AC | Likely home | Fake or stub |
|---|---|---|
| AC-1, AC-2, AC-5, AC-12, AC-15 | `test_cycle.py`, `test_github.py` | `FakeRunner` argv script, `FakeClock` |
| AC-3, AC-4 | `test_predicates.py` (tables) | none (pure) |
| AC-6, AC-10, AC-18 | `test_record.py`, `test_cycle.py` | `tmp_state`, `FakeClock` |
| AC-7 | `test_launch.py`, `test_no_text.py`, `test_security_invariants.py` | `FakeLauncher`, hostile corpus |
| AC-8, AC-9 | `test_launch.py`, `test_cli.py` | `FakeLauncher` outcomes table |
| AC-11 | `test_concurrency.py`, `test_record.py` | real processes / real flock on `tmp_path` |
| AC-13, AC-14, AC-17 | `test_cli.py`, `test_audit.py` | `CliRunner` (design FR-026 verbs: `once`, `status`, `check-config`, `reset`, `init-state`) |
| AC-16 | `test_origin_parity.py` | compares with `origin_repo.py` (`parse_origin_url`) |
| AC-19 | `test_cli_e2e.py` | sleeping PATH stub `gh` |
| AC-20 | `test_security_invariants.py` | argv prefix scan over `FakeRunner.calls` |
| AC-21 | `test_no_shell.py` | AST |
| AC-22 | `test_crash_injection.py`, `test_cycle.py::test_fifty_cycles` | `CrashingStore` |
| AC-23 | the gates of section 6 above | n/a |
| AC-24 | `test_slo_helper.py` | fixture audit log |
| AC-25 | `test_module_boundaries.py`, `test_find_orca_parity.py`, `test_origin_parity.py` | AST, parity |

---

## 9. Verification of the design's own citations (sections 12, 13, 17 and the C-rows that touch tests)

| Design claim (location) | Result in this checkout |
|---|---|
| `make test` at `Makefile:13-15` (s13) | HOLDS: line 13 `test:`, 14 echo, 15 `uv run pytest` |
| `make lint` at `Makefile:48-50` | HOLDS: 48 `lint: lint-architecture`, 50 `uv run ruff check .` |
| `make verify-deps` at `Makefile:356-358` | HOLDS (356 target, 357 echo, 358 `uv run python scripts/verify_deps.py`; line 359 `echo EXIT=...` also belongs to the target) |
| `make verify-sync` `Makefile:166`, `make sync-dev` `Makefile:109`, format `Makefile:53-55` | HOLD |
| Check 11 `Makefile:467-476` (C9) | HOLDS |
| `test.yml:47` (`-n auto`), `:106` (format check), `:123` (verify-deps), `:131` (verify-sync), `:135` (lint-architecture), `:22` (python 3.10) | ALL HOLD (re-read the file) |
| `pyproject.toml:16` (python floor), `:54` (ruff pin), `:71` (entry point), `:114` (`--strict-markers`), `:135` (`property_based`), `:174-184` (ruff config) | ALL HOLD |
| C14: `tests/cli_portify/test_cli.py` already exists | HOLDS (only `test_cli.py` in tests/) |
| C15: no hypothesis | HOLDS, and stronger: `tests/conftest.py:14` already `collect_ignore`s the hypothesis test; xdist and pytest-timeout are also absent locally |
| C11: tests run under xdist in CI | HOLDS (`test.yml:47`); but xdist is NOT installed in the local env and not declared in `pyproject.toml` |
| s12 "stub dir prepended to PATH as in `tests/pr_submit/test_conflict_e2e.py`" | PARTLY: the PATH prepend is built in `tests/pr_submit/test_conflict_scripts.py:178-179` (`make_repos`), and `test_conflict_e2e.py` imports it (lines 61-71); stubs there are written at runtime, not committed files |
| s13 table "`uv run ruff format --check src/ tests/`" as a gate | HOLDS in CI; LOCALLY red for unrelated Markdown files because the local ruff is 0.17.3 not 0.15.20 (see section 6) |
| s13 "`make verify-sync` unaffected" | HOLDS in design terms; locally `.claude/skills` is absent so it fails until `make sync-dev` |

---

## Status: Complete

## Summary

1. **How tests are written here.** Tests live under `tests/<pkg>/` with `__init__.py` (needed for `tests/issue_watch/`, which keeps `test_cli.py` unambiguous), use `tmp_path`/`monkeypatch`, `click.testing.CliRunner` (in-process: `runner.invoke(group, [...])`, `tests/cli/reflect/test_cli_smoke.py:49`) or `subprocess.run([sys.executable, "-m", "superclaude.cli.main", ...], timeout=...)` (`tests/swarm/test_inv012_tui_opt_in.py:130-143`). The PATH-stub pattern: write a bash script into `tmp_path/"bin"`, `chmod(0o755)`, prepend that dir to PATH inside an env dict passed to every `subprocess.run`, log `"$*"` to a calls file, serve canned JSON by `case "$1 $2"` (`tests/pr_submit/test_conflict_scripts.py:165-179`, `tests/pr_submit/test_conflict_e2e.py:118-146`). No tracked executable files exist under `tests/`.
2. **Hard constraints.** `--strict-markers` (`pyproject.toml:114`): add no marker. No xdist/timeout/hypothesis/mock plugin is declared (CI installs xdist ad hoc, `test.yml:26-29`; adding to the `dev` extra breaks `make verify-deps`): use `FakeClock`, subprocess/`join` timeouts, seeded `random`. Autouse `_pollution_snapshot` (`tests/conftest.py:28-79`) fails the session if tests write under repo `docs/mistakes` or `docs/memory`. Python 3.10 is the CI floor and is not installed locally (3.11.15 here), and local ruff is 0.17.3 (pin 0.15.20), so use `uvx --offline ruff@0.15.20 format --check src/ tests/` and `... check src/ tests/` (both pass on the current tree).
3. **Gates / time.** `uv run pytest tests/issue_watch/ -v` is the loop. `make test` runs the whole serial suite (17,096 tests collected in 17.6 s; run time not recorded anywhere, UNVERIFIED) and includes `test_verify_sync_hooks.py` that rewrites real source files: do not run it as a whole here; run `tests/issue_watch/` plus the three `*registration*` test files, then `make sync-dev && make verify-sync`, `make verify-deps`, `make lint` (lint-architecture Check 11 scans `src/superclaude/cli/`), pinned ruff format/check.

## Gaps and Unverified

- Full-suite runtime: not recorded in repo (no CI log access); `make test` was not run. UNVERIFIED.
- Whether a `multiprocessing` lock test is stable under `-n auto` in CI: no precedent in `tests/`; the `subprocess`+`fcntl.flock` form has precedent (`tests/unit/test_ccsession_tag.py:4496-4518`). UNVERIFIED for multiprocessing.
- Design section 12 lists only `stubs/gh` and `stubs/orca`; spec-final line 112 also names a stub `git`, and `origin_repo.read_origin` shells to `git`. The e2e test needs a decision: stub `git` or a real tmp git repo with `GIT_CONFIG_GLOBAL=/dev/null` (as `make_repos`). Not decided by the design.
- Existing stubs log `"$*"` (flat); the design's exact-argv assertions (AC-8 12-element launch argv, prompt with spaces) need a one-element-per-record log. No existing helper does this.
- Click 8.0 floor vs 8.5.1 installed: `result.stderr` semantics differ; no CI job exercises the floor. UNVERIFIED which form is safe for stderr assertions in `CliRunner`; the subprocess form avoids the question.
- Python 3.10 behaviour cannot be exercised locally (no 3.10 interpreter installed; `uv python list --only-installed` shows 3.11 and 3.13); only CI catches 3.11-only APIs. `uv run --python 3.10` was not tried (would need a download).
- `make verify-deps`, `make sync-dev`, `make verify-sync` were read but not run (they audit or write the local env / `.claude/`).
- Dual-surface lookup helper for `test_marker_contract.py`: design says "read through the dual surface" but no test helper exists; scope belongs to the integration researcher.
