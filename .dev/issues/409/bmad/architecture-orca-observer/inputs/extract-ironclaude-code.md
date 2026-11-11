# Extract: IronClaude CLI code facts for `superclaude observe`

Source: `/home/coder/workspaces/IronClaude` (read-only; codegraph index 2026-11-07, 0 changes since). Extracted 2026-11-08.
All paths relative to that repo. `src/superclaude/cli/observe/` does not exist yet (dir listing of `src/superclaude/cli/`).

## 1. CLI registration (`src/superclaude/cli/main.py`)

- Root group object: `main`, a plain `@click.group()` with `@click.version_option(...)` (main.py:18-20). Console script `superclaude = "superclaude.cli.main:main"` (pyproject.toml:71).
- No LazyGroup / `importlib` lazy loading. Pattern is a module-bottom deferred import, one block per subpackage, then `main.add_command(...)` (main.py:519-561; 11 registrations: sprint, roadmap, cleanup-audit, tasklist, cli_portify, prd, eval, swarm, recommend, init-lite, reflect).
- Exact block (main.py:519-521):

```python
from superclaude.cli.sprint import sprint_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports

main.add_command(sprint_group, name="sprint")
```
- Some import from `<pkg>.commands` instead of the package `__init__` (e.g. eval, main.py:543-545; reflect, main.py:559-561).
- Next-step note: an `observe_group` would be one more such block before `if __name__ == "__main__":` (main.py:564).

## 2. `_find_orca()` (`src/superclaude/cli/install_user_setup.py:198-221`)

- Signature `def _find_orca() -> str | None:` (198). Candidates `_ORCA_CLIS = ("orca-ide", "orca")` (35), tried in that order.
- Search: `shutil.which(name)` only (PATH). No env var, no fixed paths.
- Probe: runs `[path, "skills", "list", "--json"]` with `capture_output=True, text=True, timeout=10, stdin=DEVNULL` (209-215); accepts only if returncode 0 and a topic named `orca-cli` is in the JSON `topics` (216, 219). Docstring: bare `orca` on Linux is often the GNOME screen reader (201-202).
- Failure: `OSError`, `SubprocessError`, `ValueError`, `AttributeError` swallowed per candidate (217-218); returns `None` if none pass (221). Never raises.

```python
198 def _find_orca() -> str | None:
204     for name in _ORCA_CLIS:
205         path = shutil.which(name)
206         if not path:
207             continue
208         try:
209             probe = subprocess.run(
210                 [path, "skills", "list", "--json"],
211                 capture_output=True, text=True, timeout=10,
214                 stdin=subprocess.DEVNULL,
215             )
216             topics = json.loads(probe.stdout).get("topics", [])
217         except (OSError, subprocess.SubprocessError, ValueError, AttributeError):
218             continue
219         if probe.returncode == 0 and any(t.get("name") == "orca-cli" for t in topics):
220             return path
221     return None
```
(docstring 199-203 omitted; lines 211-213 condensed onto one line above.)
- Next-step note: it is a private helper in an install module; reuse means importing a `_`-prefixed name or moving it.

## 3. Rich Live pattern (`src/superclaude/cli/sprint/tui.py`)

- Class `SprintTUI(config, console: Console | None = None)`; `self.console = console or Console()` (tui.py:83-85): Console is injected, default constructed bare.
- `start()` builds `Live(self._render(), console=self.console, refresh_per_second=2, screen=False, redirect_stdout=_redirect, redirect_stderr=_redirect)` then `.start()` (tui.py:119-127). `_redirect` is False only when env `SUPERCLAUDE_SPRINT_RENDER_DIAG=1` (tui.py:118). `stop()` calls `_live.stop()` (130-134). No `with Live(...)` context manager.
- Push model: executor calls `update(sprint_result, monitor_state, current_phase)` which does `self._live.update(self._render())` (tui.py:136-152). Any render exception sets `_live_failed = True`, logs, prints to stderr and stops further updates; the sprint continues (tui.py:160-172).
- `_render() -> Panel`: composes `_build_header`, `_build_phase_table`, `_build_progress`, optional `_build_error_panel`, `_build_active_panel` into `rich.console.Group`, wrapped in `Panel(title=..., border_style="blue", padding=(1, 2))` (tui.py:174-217). Pure helpers at module bottom (`_format_tokens`, `_render_bar`, `_truncate`, ... tui.py:588-640).
- Keyboard input: none in tui.py (no termios/tty/readchar/stdin; grep over `src/superclaude/cli`). Only `sys.stdin.isatty()` checks elsewhere (sprint/commands.py:503, install_mcp.py:490).
- Tests importing `sprint.tui`: tests/sprint/{test_tui.py, test_tui_gate_column.py, test_tui_redirect_gate.py, test_tui_v2_wave2.py, test_preflight.py, test_integration_lifecycle.py}. The ones read call `tui._render()` and print it to a capture console rather than starting Live: `Console(file=output, width=80, force_terminal=True)` (tests/sprint/test_tui.py:33-39), and construct `SprintTUI(config, console=Console(file=StringIO(), width=80))` (test_tui.py:59). Widths 100 / 160 in other files (test_tui_gate_column.py:32, test_tui_v2_wave2.py:83). No `color_system=None` in these fixtures. Whether test_tui_redirect_gate.py starts a real Live: UNVERIFIED (not read).
- Next-step note: observer can copy inject-Console + pure `_render()` + render-to-StringIO testing as-is.

## 4. Subprocess conventions

- Direct `subprocess.run([...], capture_output=True, text=True, timeout=N, stdin=DEVNULL)`, argv list, no shell: `_find_orca` (install_user_setup.py:209-215).
- Bounded argv runner `_bounded(argv, timeout, *, capture)` (install_mcp.py:769-794): `Popen` without shell, `stdin=DEVNULL`, `stderr=DEVNULL`, `start_new_session=True`, `communicate(timeout=...)`; on timeout `os.killpg(pid, SIGKILL)` and (per docstring, 773) re-raises `TimeoutExpired`. Wrapper `_run_argv(argv, timeout) -> (returncode, stdout)` (install_mcp.py:804-806).
- Injectable runner seam: `Runner = Callable[[list, float], tuple]`, commented "run(argv, timeout) -> (returncode, stdout)" (install_codegraph.py:42-43); functions take `run: Runner` as a parameter (install_codegraph.py:89, 97, 125, 271). Tests swap it: `def fake_run(argv, timeout)` + `monkeypatch.setattr(install_mcp, "_run_argv", fake_run)` (tests/cli/test_install_codegraph.py:428-435).
- Another seam: `step_runner: Optional[Callable[[PortifyStep], tuple[int, str, bool]]]` (cli_portify/executor.py:465, 476).
- Exception: `_run_command` uses `shell=True` with the user's shell on non-Windows (install_mcp.py:119-148); the only `shell=True` in `src/superclaude/cli`.
- Next-step note: the `Runner` callable + `fake_run` monkeypatch is the house seam for faking the Orca CLI.

## 5. Packaging and test layout

- `requires-python = ">=3.10"` (pyproject.toml:16).
- Runtime deps, all floors with no caps: `pytest>=7.0.0`, `click>=8.0.0`, `rich>=13.0.0`, `pyyaml>=6.0`, `jsonschema>=4.0.0`, `jinja2>=3.0`, `pexpect>=4.9`, `httpx>=0.27` (pyproject.toml:34-43). Dev pins `ruff==0.15.20`, `mypy>=1.0` (54-55).
- textual: NOT a dependency (no `textual` match in pyproject.toml).
- pytest: `testpaths = ["tests"]`, `test_*.py`, addopts `-v --strict-markers --tb=short` (pyproject.toml:107-116); markers declared from line 117, so new markers must be registered.
- Layout: `tests/<pkg>/` mirrors `src/superclaude/cli/<pkg>/` for subpackages (tests/sprint, roadmap, swarm, recommend, tasklist, cli_portify, pipeline); single-module CLI tests sit in `tests/cli/` (e.g. tests/cli/test_install_codegraph.py). No `tests/observe/` yet.
- `NO_COLOR` / `color_system` / `legacy_windows` / `safe_box` / `ascii_only`: zero hits in `src/superclaude/cli`. The only `NO_COLOR` in `src/` is a shell script, `src/superclaude/skills/ccsession-tag/ccsession:1567-1569`. `force_terminal=True` appears only in tests (section 3).
- Next-step note: color/ASCII handling for observe is new ground; relying on Rich's built-in `NO_COLOR` support costs no code (UNVERIFIED against the installed Rich version).

## 6. JSON export and schema conventions

- `--json` flag: `@click.option("--json", "as_json", is_flag=True, help=...)` (eval/commands.py:768-773; also near 926-927, 1226, 1638). Output via `click.echo(json.dumps(payload, indent=2, sort_keys=True))` (eval/commands.py:887-893, 968-969; also 1202).
- `schema_version` fields: int `1` in roadmap (roadmap/executor.py:2111, 3223; roadmap/convergence.py:309); strings `"phase-1"`/`"phase-2"` in audit (audit/scanner_schema.py:81-87, 120, 168); `SCHEMA_VERSION` constant in recommend/cache.py:115, 168 (docstring says version 2, line 11); required string in swarm schema (swarm/schema.py:330-337). No single house type.
- jsonschema: `from jsonschema import Draft7Validator`, `Draft7Validator.check_schema(JOB_SPEC_SCHEMA)` at import, module-level `_JOB_SPEC_VALIDATOR`, `validate(spec) -> list[SchemaValidationFailure]` (swarm/schema.py:68, 474-475, 741); eval loader maps `jsonschema.exceptions.ValidationError` (eval/loader.py:40, 183).
- Next-step note: `--json`/`as_json` + `sort_keys=True` + an int `schema_version` + a Draft7 schema test matches existing practice.
