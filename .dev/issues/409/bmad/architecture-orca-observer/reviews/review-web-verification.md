# Review: web and reality verification of ARCHITECTURE-SPINE.md

- Spine: `_bmad-output/planning-artifacts/orca-observer/architecture/ARCHITECTURE-SPINE.md` (not edited)
- Brownfield repo (read only): `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp`
- Reviewer lens: every committed decision web-researched or reality-checked; versions, existence and fit, live defaults
- Date: 2026-11-08
- Method: PyPI JSON API, endoflife.date API, upstream changelogs, official docs, plus a throwaway Python 3.10.20 venv under `/tmp` with rich 15.0.0, jsonschema 4.26.0 and click 8.5.1 installed and probed (signatures and actual output). Repo facts checked with grep on the brownfield checkout.

## Verdict: FAIL

Blocking: 1. Minor: 7.

Every version in the Stack table is correct as of 2026-11-08, and every named Rich, jsonschema and stdlib API exists with the stated shape. The failure is one platform claim the spine commits to without checking the stdlib: "`--once` covers every platform".

## Findings

### F1 (blocking): `--once` is not cross-platform, and on Windows the registration import would break the whole `superclaude` CLI

- Spine: AD-14 "Interactive mode is POSIX only; `--once` covers every platform"; AD-11 "`--once` ... needs no raw mode on any platform"; AD-1 diagram `commands --> keys`; AD-2 deferred `from superclaude.cli.observe.commands import observe_group` in `cli/main.py`; AD-5 production runner uses `start_new_session=True` and `os.killpg(SIGKILL)`.
- Reality: `termios` and `tty` are Unix only (https://docs.python.org/3.10/library/termios.html, https://docs.python.org/3.10/library/tty.html). `os.killpg` is Unix only (https://docs.python.org/3.10/library/os.html#os.killpg). `start_new_session` is POSIX only (https://docs.python.org/3.10/library/subprocess.html#subprocess.Popen).
- Effect: `commands.py` imports `keys.py`, which imports `termios`/`tty`. On Windows that import raises `ImportError`. Because AD-2 imports `observe.commands` at module level in `cli/main.py`, every `superclaude` command would fail to start on Windows once the block lands, not only `observe`. The `--once` timeout path would also hit `AttributeError` on `os.killpg`.
- Repo context: the package declares `Operating System :: OS Independent` (`pyproject.toml` classifiers), and `install_mcp.py:136` already branches on `platform.system() == "Windows"`, so Windows is not out of scope for the CLI as a whole. The house `install_mcp._bounded` (`install_mcp.py:769-788`) does use `start_new_session` and `os.killpg`, so mirroring it inherits a POSIX-only runner.
- Fix: either drop the "every platform" claim and state the observer is POSIX only (and keep the main.py import safe on Windows), or make `keys.py` import lazily inside the interactive path only and give the runner a non-POSIX branch (`process.kill()` when `os.killpg` is absent). Add a test that imports `superclaude.cli.main` with `termios` hidden.

### F2 (minor): Rich floor `>=13.0.0` reads an empty `NO_COLOR` as "set", against no-color.org

- Spine: AD-13 "`no_color` is true when `NO_COLOR` is set and non-empty ... passed explicitly as `color_system=None`, `no_color=True`." Stack keeps `rich>=13.0.0`.
- Reality: no-color.org: "when present and not an empty string (regardless of its value), prevents the addition of ANSI color" (https://no-color.org/). Rich 13.0.0 computes `"NO_COLOR" in self._environ` (https://raw.githubusercontent.com/Textualize/rich/v13.0.0/rich/console.py, line 743). Rich 14.0.0 (2025-03-30) changed this: "An empty `NO_COLOR` env var is now considered disabled" (https://github.com/Textualize/rich/pull/3675, https://github.com/Textualize/rich/blob/master/CHANGELOG.md). Probe on rich 15.0.0: `NO_COLOR=""` gives `no_color=False`, `"1"` and `"yes"` give `True`.
- Effect: the spine only says what is passed when the policy is true. If `make_console` leaves `no_color` as `None` in the false case, a user with `NO_COLOR=""` on Rich 13.x gets colour suppressed by Rich itself, contradicting AD-13 and making output depend on the installed Rich.
- Fix: `make_console` always passes `no_color=policy.no_color` and an explicit `color_system`, never leaving `no_color` as `None`; or raise the floor to `rich>=14.0.0`.

### F3 (minor): Rich reads `COLUMNS` (and `NO_COLOR`) itself unless overridden

- Spine: AD-13 "no other module constructs a `Console` or reads `NO_COLOR`, `COLUMNS` or the stream encoding."
- Reality: rich 15.0.0 `console.py` reads `COLUMNS` at lines 685 and 1030 and `NO_COLOR` at 728 when the matching arguments are not given (installed source in the probe venv; upstream https://github.com/Textualize/rich/blob/master/rich/console.py).
- Fix: state that `make_console` always passes `width` (and `height` where used) from the policy, so the "only `terminal.py` decides" rule holds in fact and not just in our code.

### F4 (minor): `safe_box=True` does not give ASCII boxes, and Rich's own table overflow emits a non-ASCII ellipsis

- Spine: AD-13 "`ascii` ... `box.ASCII`, `safe_box=True`"; CD-5 truncation glyph `>`.
- Reality: `safe_box` defaults to `True` and only "Restrict[s] box options that don't render on legacy Windows" (rich 15.0.0 `console.py:611`; `box.py` `substitute()`: legacy-Windows substitution needs `safe`, ASCII substitution needs `options.ascii_only`, which is driven by a non-UTF encoding, not by `--ascii`). Probe: a `Table(box=box.ASCII)` too wide for a 20-column console with colour off printed `| aaaaaaaaaaaaaaa… |`, i.e. Rich added U+2026 itself (default column `overflow="ellipsis"`).
- Effect: with `--ascii` on a UTF-8 terminal, any cell Rich squeezes gets `…`, breaking the ASCII guarantee and the `>` glyph rule. `safe_box=True` adds nothing on POSIX.
- Fix: pass `box.ASCII` explicitly on every box-drawing renderable in ASCII mode, set `overflow="crop"` or `"fold"` with `no_wrap` on columns so only the `terminal.py` truncation helper truncates, and drop `safe_box` from the rule or say it is the default.

### F5 (minor): pytest floor `>=7.0.0` admits pytest 9.0.x, where `--strict-markers` in `addopts` is silently ignored

- Spine: AD-16 "R2 placeholder tests (T19, T51) are skipped with a registered marker ... (pytest runs with `--strict-markers`)". Repo `pyproject.toml` sets `--strict-markers` in `addopts`.
- Reality: pytest 9.1.0 (2026-06-13) changelog: "Fixed a regression in pytest 9.0 where `--strict-markers` and `--strict-config` specified through `addopts` were silently ignored" (https://github.com/pytest-dev/pytest/issues/14442, https://docs.pytest.org/en/stable/changelog.html). 9.0.0 was released 2025-11-05.
- Fix: either raise the dev/test floor to exclude 9.0.x (`pytest>=7,!=9.0.*`) or add the `strict_markers = true` ini option, which pytest 9 recommends.

### F6 (minor): Textual fail branch silently raises the Rich floor

- Spine: Stack "rich ... repo floor >=13.0.0 kept"; "textual 8.2.8 ... added only if the key-reader spike fails".
- Reality: textual 8.2.8 `requires_dist` includes `rich>=14.2.0` (https://pypi.org/pypi/textual/8.2.8/json).
- Fix: note that the fail branch makes the effective floor `rich>=14.2.0` and record that as a stack change.

### F7 (minor): `tty.setcbreak` on Python 3.10/3.11 returns nothing and flushes pending input

- Spine: AD-14 "enters cbreak mode through `termios`/`tty` and restores the saved attributes".
- Reality: Python 3.10 signature `tty.setcbreak(fd, when=termios.TCSAFLUSH)`, return value `None` (https://docs.python.org/3.10/library/tty.html; probe confirms). Returning the old attributes was added in 3.12 (https://docs.python.org/3.12/library/tty.html). `TCSAFLUSH` discards input typed before the switch.
- Fix: say the saved attributes come from `termios.tcgetattr(fd)` before the call (the 3.10 floor rules out using the return value), and choose `when=termios.TCSANOW` or accept the flush deliberately; the "no key lost" spike criterion should cover it.

### F8 (minor): the "verified latest" claims carry no source

- Spine Stack table says "verified latest on 2026-11-08" for five packages with no URL; the source `stack.md` labels its table "primary sources, nothing run: UNVERIFIED as run facts" and contains no URLs.
- Reality: all five values are correct (see Self-Audit), so this is traceability only.
- Fix: add the PyPI URLs and check date to the Stack table or `stack.md`.

Count note: F2 to F8 are seven minor findings; F1 is the only blocking one.

## Self-Audit: what was checked and confirmed correct

| Claim | Result | Source |
| --- | --- | --- |
| rich 15.0.0 latest | Correct, released 2026-04-12, requires Python >=3.9 | https://pypi.org/pypi/rich/json |
| click 8.5.1 latest | Correct, released 2026-11-06, requires Python >=3.10 | https://pypi.org/pypi/click/json |
| jsonschema 4.26.0 latest | Correct, released 2026-01-07, requires Python >=3.10 | https://pypi.org/pypi/jsonschema/json |
| pytest 9.2.0 latest | Correct, released 2026-10-27, requires Python >=3.10 | https://pypi.org/pypi/pytest/json |
| textual 8.2.8 latest | Correct, released 2026-06-30 | https://pypi.org/pypi/textual/json |
| pexpect floor >=4.9 | Matches repo; 4.9.0 (2023-11-25) is still latest | https://pypi.org/pypi/pexpect/json |
| Python 3.10 end of life 2026-10-01 | Correct; last release 3.10.22 on 2026-10-01 | https://endoflife.date/api/python/3.10.json, PEP 619 |
| Repo floors | `requires-python >=3.10`, `rich>=13.0.0`, `click>=8.0.0`, `jsonschema>=4.0.0`, `pytest>=7.0.0`, `pexpect>=4.9` all match | brownfield `pyproject.toml` |
| `Console(color_system=None, no_color=True, safe_box=True, record=True, file=...)` | All parameters exist in rich 15.0.0; `color_system=None` removes all SGR, `no_color=True` alone keeps bold (`\x1b[1m` seen), so passing both is right | probe; https://rich.readthedocs.io/en/stable/reference/console.html |
| `export_text()` | Exists, `(clear=True, styles=False)`; output had no ESC | probe |
| `rich.box.ASCII`, `rich.cells.cell_len`, `rich.text.Text`, `markup=False`, `Live(screen=True)` | All exist; `cell_len("中a") == 3` | probe |
| Rich honours `NO_COLOR` natively | Yes; `no_color` argument since 9.7.0 (2021-01-09); empty value treated as unset since 14.0.0 | Rich CHANGELOG |
| `Draft7Validator.check_schema` | Exists in 4.26.0 and raises `SchemaError` on a bad schema | probe; https://python-jsonschema.readthedocs.io/en/stable/api/ |
| hatchling `packages = ["src/superclaude"]` ships non-Python files | Yes, selection is directory based; files matched by `.gitignore` are excluded, and the repo `.gitignore` has no `*.json` or `fixtures` rule; repo already ships non-Python data under `src/superclaude` and loads it with `importlib.resources` (`cli/roadmap/templates.py`) | https://hatch.pypa.io/latest/config/build/ |
| `importlib.resources.files` in 3.10 | Exists (added 3.9); `joinpath` with several parts worked on 3.10.20 for an installed package | probe; https://docs.python.org/3.10/library/importlib.html#importlib.resources.files |
| `tty.setcbreak`, `os.killpg`, `start_new_session`, `time.monotonic` | All exist on 3.10 (POSIX for the first three, see F1, F7) | probe; Python 3.10 docs |
| NO_COLOR convention | Any non-empty value | https://no-color.org/ |
| House seams cited | `_find_orca` (`install_user_setup.py:198`), `_bounded` Popen/DEVNULL/`start_new_session`/`killpg` (`install_mcp.py:769-788`), `Runner = Callable[[list, float], tuple]` (`install_codegraph.py:43`), `OutputMonitor` with `threading.Event` (`sprint/monitor.py:443,455`), `# noqa: E402,I001` deferred registration before `if __name__ == "__main__":` (`main.py:519-564`) | brownfield repo grep |
| click `add_command(cmd, name=...)` | Exists | https://click.palletsprojects.com/en/stable/api/#click.Group.add_command |

Not checked: a real hatchling wheel build of the new subpackage (inferred from docs and the existing roadmap templates precedent); Textual behaviour; anything on Windows (F1 is from the docs, not a Windows run).
