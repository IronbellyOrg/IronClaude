# Research: Patterns and Conventions

**Topic type:** Patterns and conventions (CLI package layout, command plus protocol skill pairs, tooling config)
**Scope:** `src/superclaude/cli/main.py`; `src/superclaude/cli/reflect/`, `src/superclaude/cli/recommend/`; their tests; `src/superclaude/commands/{reflect,issue}.md` with `src/superclaude/skills/sc-{reflect,issue}-protocol/SKILL.md`; `pyproject.toml` ruff config; atomic-write helpers.
**Status:** Complete
**Date:** 2026-11-08

---

## 1. Registering a command group in `cli/main.py`

- Every package group is registered at the bottom of `src/superclaude/cli/main.py`, after all `@main.command()` definitions, as a two-line pair: a deferred import with a fixed trailing comment, a blank line, then `main.add_command(<group>, name="<name>")`. Examples: `recommend` at `main.py:551-553`, `reflect` at `main.py:559-561` (the last pair, just before `if __name__ == "__main__":` at `main.py:564`).
- The exact import comment is `# noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports` (`main.py:519`, repeated on every pair through `main.py:559`).
- Two import forms exist:
  - from the package, relying on the package `__init__` to export the group: `from superclaude.cli.recommend import recommend_group` (`main.py:551`), `from superclaude.cli.tasklist import tasklist_group` (`main.py:531`);
  - from the `commands` module directly: `from superclaude.cli.reflect.commands import reflect_group` (`main.py:559`).
- **For sweep**: append after `main.py:561`:
  ```python
  from superclaude.cli.sweep import sweep_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports

  main.add_command(sweep_group, name="sweep")
  ```
  The package form fits the design, which routes through a lazy `__getattr__` (`docs/designs/orchestrator-mode.md:171`, `:360`).
- The console script is `superclaude = "superclaude.cli.main:main"` (`pyproject.toml:70-71`).

## 2. Package `__init__.py`: the lazy `__getattr__` precedent

- Two packages use a module-level `__getattr__` that imports `commands` only when the group is first used:
  - `src/superclaude/cli/recommend/__init__.py:12-20`
  - `src/superclaude/cli/tasklist/__init__.py:9-17`
- Shape (recommend, `__init__.py:12-17`): `def __getattr__(name: str):` with no return annotation; `if name == "recommend_group":` does a local `from .commands import recommend_group` and returns it; anything else raises `AttributeError(f"module {__name__!r} has no attribute {name!r}")`. Then `__all__ = ["recommend_group"]` (`:20`). A module docstring comes first (`:1-9`).
- `reflect/__init__.py:17-30` is the counter-example: it imports eagerly (`from .commands import reflect_group`, plus models, config and contract) and lists them in `__all__`. Do not copy it, because the design says `__init__.py` imports nothing at import time (`orchestrator-mode.md:208`).
- **For sweep**: copy the tasklist or recommend file and change the name to `sweep_group`. The design signature `def __getattr__(name: str) -> object` (`orchestrator-mode.md:360`) adds a return annotation the precedents leave out. Both are valid; the annotated form is what the design specifies.

## 3. `commands.py`: Click group style, help text, lazy imports, errors and exit codes

- **Naming.** The group function is `<name>_group`, declared with an explicit name string: `@click.group("recommend")` / `def recommend_group() -> None:` (`recommend/commands.py:34-35`); `@click.group("reflect")` / `def reflect_group():` (`reflect/commands.py:53-54`). Subcommands use `@<group>.command("<verb>")` with an explicit name, for example `@cache_group.command("get")` (`recommend/commands.py:57`) and `@reflect_group.command("contract-status")` (`reflect/commands.py:82`). Nested groups use `@recommend_group.group("cache")` (`recommend/commands.py:51`).
- **Group docstring.** One summary line, a paragraph, then an `Examples:` block of literal `superclaude <group> ...` lines; the body is `pass` (`recommend/commands.py:36-48`, `reflect/commands.py:55-67`). Tests assert a fragment of this docstring in `--help` output (`tests/cli/test_cli_registration.py:66-69`).
- **Module docstring.** It says that heavy imports are deferred into command bodies "to keep `superclaude --help` fast" (`recommend/commands.py:6-8`; `reflect/commands.py:4-5`, "house convention").
- **Lazy imports inside the command body.** For example `from .cache import LookupCache, compute_surface_hash` inside `cache_get` (`recommend/commands.py:67`), and `from superclaude.pr_submit.contract_setup import (...)` inside `contract_status` (`reflect/commands.py:105-112`). Module-level imports are limited to the standard library and `click` (`recommend/commands.py:18-24`; `reflect/commands.py:15-24`).
- **Module constants.** Private `_UPPER_SNAKE` names at the top, each with a comment explaining why: `_DEFAULT_CACHE` (`recommend/commands.py:26`), `_BLOCKED_EXIT = 2` (`reflect/commands.py:41-42`), `_TMUX_SESSION_PREFIX` (`reflect/commands.py:39`).
- **Option style.** One `@click.option(` per flag, keyword arguments on separate lines, a `help=` string ending in a period, and `type=click.Path(path_type=Path)` for path options (`recommend/commands.py:59-64`). A flag whose Python name differs from the option uses a second positional argument: `"--validate", "run_validation"` (`reflect/commands.py:83-88`); the `--json` form is `"--json", "as_json", is_flag=True` (`eval/commands.py:769-773`, `sprint/commands.py:703-707`). For a repeatable `--run`, Click's `multiple=True` produces the `tuple[str, ...]` the design signature expects (`orchestrator-mode.md:437`). Unverified: no `multiple=True` example was read in the two scoped packages.
- **Errors.** Messages go to stderr with `click.echo(..., err=True)`, followed by an explicit `sys.exit(<code>)`:
  - `recommend/commands.py:73-74`: prefix `[recommend cache get]` and exit 1. Bracketed `[<group> <verb>]` prefixes are the recommend convention (`:108-112`, `:121-126`, `:142`), and they match the design's `[sweep <stage>]` prefix (`orchestrator-mode.md:445`, `:106`, `:110`).
  - `reflect/commands.py:389-391, 428`: `except ValueError as exc:` echoes `Error: {exc}` to stderr, then `sys.exit(_BLOCKED_EXIT)`.
  - `reflect/commands.py:442-469`: a catch-all `except Exception` writes a best-effort sidecar and then re-raises.
- **Exit codes in one place.** reflect keeps its codes on the enum, `Verdict.exit_code` (`reflect/models.py:38-49`); the commands docstring says they are "never hardcoded a second time" (`reflect/commands.py:5-7`). The command ends with `sys.exit(exit_code)` (`reflect/commands.py:484`).
- **Click exceptions elsewhere.** `sprint/commands.py:906, 925` raise `click.UsageError`, which Click maps to exit 2 by itself; `sprint/commands.py:729` raises `click.ClickException`, which exits 1. The design maps `click.UsageError` and `BindingError` to exit 2, everything else to exit 1, and only `commands.run` calls `sys.exit` (`orchestrator-mode.md:445`). Both forms have house precedent.
- **JSON output.** `click.echo(json.dumps(row, ensure_ascii=False))` prints one JSON object on stdout (`recommend/commands.py:75`). Diagnostics go to stderr, so stdout carries only the JSON, which is what the skill parses (`orchestrator-mode.md:653`).

## 4. Subprocess wrappers and how tests mock them

- **The `_git` seam.** It lives in `reflect/config.py:64-78`: `def _git(cwd: Path, *args: str) -> str` runs `subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, check=True, text=True, timeout=10)` and returns `result.stdout.strip()`. Its docstring (`:67-69`) says it raises `subprocess.SubprocessError`/`OSError` so callers can fall back fail-closed. The design's `_git(cwd, *args, timeout)` and `_orca(*args, timeout)` seams (`orchestrator-mode.md:385-386`) follow this shape, adding a timeout parameter and a typed exception (`GitCallFailed`).
- **Mocking the seam by module attribute.** Tests import the module and replace the function: `monkeypatch.setattr(config_mod, "_git", _fake_git)`, where `_fake_git(cwd, *args)` branches on `args[0]` (`tests/cli/reflect/conftest.py:58-80`). `test_cli_smoke.py:266` and `:287` use the same pattern with a `MagicMock(side_effect=...)`, and `:284` raises `subprocess.CalledProcessError(128, [...])` to simulate a git failure.
- **Mocking `subprocess.run` inside the module under test.** For example `patch("superclaude.cli.sprint.rerun_tasks.subprocess.run")` (`tests/sprint/test_rerun_tasks_failure_modes.py:316`) and `monkeypatch.setattr(preflight_mod.subprocess, "run", _raise_timeout)` (`tests/sprint/test_preflight.py:564`).
- **Mocking binary lookup.** `monkeypatch.setattr(runner_mod.shutil, "which", lambda name: "/usr/bin/claude")` (`tests/cli/reflect/conftest.py:95`).
- **For sweep**: mock `probes._orca` and `probes._git` with `monkeypatch.setattr(probes_mod, "_orca", fake)`. A recording fake (one that appends every argv to a list) fits the design's NFR-003 argv-recording test (`orchestrator-mode.md:340-343`).
- **AST import-boundary test precedent.** `tests/swarm/test_concurrency_python_only.py:39-80` uses `ast` to flag real `import subprocess` statements and `subprocess.X(...)` calls while ignoring docstrings, with module-level `pytestmark` (`:48`), `REPO_ROOT = Path(__file__).resolve().parents[2]` (`:50`) and `frozenset` forbidden sets (`:57-80`). Its docstring (`:29-36`) adds a "mutation guarantee": the detector must be shown to flag a synthetic offending source. Use this as the template for the design's NFR-004 test (no `os`, `shutil`, `subprocess` or `click` imports in `classify.py`/`report.py`; `orchestrator-mode.md:210-216`).

## 5. Dataclass and typing style

- **Future import.** Every module in reflect, recommend and swarm starts with `from __future__ import annotations` (34 of 34 files; for example `reflect/models.py:19`, `recommend/models.py:11`, `swarm/atomic.py:7`). The two `__init__.py` files with a lazy `__getattr__` do not have it (`recommend/__init__.py`, `tasklist/__init__.py`).
- **Typing.** PEP 604 unions (`Path | None`, `str | None`) appear throughout, for example `reflect/models.py:69, 71`. `Callable`/`Mapping` come from `collections.abc` and `Any`/`Literal`/`TYPE_CHECKING` from `typing` (`reflect/fallback.py:9, 13`). Built-in generics (`dict[str, str]`, `list[str]`, `tuple[str, ...]`) are used, for example `reflect/config.py:83` and `reflect/commands.py:514`. Target is `py310` (`pyproject.toml:175`); mypy uses `python_version = "3.10"` and `disallow_untyped_defs = false` (`pyproject.toml:208-216`), so annotations are expected but not enforced.
- **Dataclasses.**
  - Mutable `@dataclass` is used for config objects that get changed after creation: `ReflectConfig` (`reflect/models.py:57-107`). Fields with defaults come after fields without them, and comments explain why each field exists.
  - `@dataclass(frozen=True)` is used for pure value objects: `FallbackDecision`, `QuorumState`, `LadderOutcome` (`reflect/fallback.py:66-93`). Frozen dataclasses are common across the CLI (55 occurrences in 27 files, most in `eval/` and `swarm/`).
  - Defaults are mutable-safe: `field(default_factory=lambda: _CACHE_DIR / "...")` (`recommend/models.py:31-40`).
  - Each class has a docstring, and the domain values are a `str, Enum` (`class Verdict(str, Enum)`, `reflect/models.py:26-54`).
  - The design wants every sweep type frozen, with class and state names as `str` constants in tuples rather than enums (`orchestrator-mode.md:190-191`, `:449`). That matches the frozen value-object precedent; the `str` constants deliberately differ from reflect's `Enum`.
- **Model module boundary.** The docstring of `reflect/models.py:8-12` states it is "types only" and imports nothing from sibling modules. This is the same rule as the design's `models.py` row (`orchestrator-mode.md:209`).
- **Isolation guardrails in docstrings.** reflect modules list them explicitly: no imports from `sprint`/`roadmap`, zero `async def` (`reflect/runner.py:8-12`, `reflect/models.py:8-12`). Sweep modules can state their B1-B5 boundaries the same way.

## 6. Ruff configuration (`pyproject.toml`)

- `[tool.ruff]`: `line-length = 88`, `target-version = "py310"`, `exclude = ["docs/"]`, and `extend-exclude = [".dev/", "tests/audit/fixtures/syntax_error.py"]` (`pyproject.toml:173-181`).
- `[tool.ruff.lint]`: `select = ["E", "F", "I", "N", "W", "TID"]`; `ignore = ["E501", "N818"]` (`pyproject.toml:183-193`). N818 is ignored, so exception classes may omit the `Error` suffix. This matters for the design's `BindingError` and `GitCallFailed` (`orchestrator-mode.md:380, 387`): either name passes.
- `TID` banned API: `anthropic`, `anthropic.AsyncAnthropic` and `anthropic.Anthropic` are banned (`pyproject.toml:203-206`). Sweep has no reason to touch them.
- There is no `[tool.ruff.lint.isort]` or `[tool.ruff.format]` section (a grep for `isort` and `tool.ruff.format` in `pyproject.toml` found nothing), so ruff's default isort applies: standard library, third party, first party, each group separated by a blank line (seen in `reflect/runner.py:20-37`). `I001` is suppressed only on the deferred imports in `main.py`.
- `N` (pep8-naming) applies. PyYAML overrides use `# noqa: N802 (PyYAML API)` (`reflect/runner.py:77`).

## 7. Atomic file writes: is there a helper to reuse?

- **The repository already uses temp file plus `os.link` exclusive publish, which is the design's mechanism** (`orchestrator-mode.md:99-117`):
  - `src/superclaude/cli/sprint/recovery.py:412-459`: `tempfile.mkstemp(dir=..., prefix=".lock.tmp.")`, `os.write`, `os.close`, then `os.link(tmp_name, lock_path)` with `except FileExistsError:` (`:424-434`). The comment at `:414-423` gives the same reason the design gives: with link-after-write, a file "only ever becomes visible already fully written". There is no `fsync`, and the temp file is unlinked in `finally`.
  - `src/superclaude/cli/install_ccsession.py:72-88`: `NamedTemporaryFile(dir=..., prefix=".ccsession-env-", delete=False)`, `os.link(staged_path, env)`, `except FileExistsError: pass`, and `staged_path.unlink(missing_ok=True)` in `finally`.
  - Neither is a reusable public helper. Both are inline blocks inside larger functions, and neither has the `-2`..`-99` suffix loop or the `fsync` step the design needs.
- **Shared `os.replace` helpers.** These do not fit, because the design rejects `os.replace`: it overwrites an existing target (`orchestrator-mode.md:116`).
  - `superclaude.cli.swarm.atomic.write_prepared_bytes(path, data) -> int` (`swarm/atomic.py:14-39`) is the only CLI module that exists only to hold an atomic-write helper: `mkstemp` in the same directory, `fsync`, `os.replace`, unlink on error.
  - Private copies of the same pattern: `reflect/runner.py:81-100` (`_atomic_write_text`, temp name with pid and uuid), `init_lite.py:221-240` (`_atomic_write`), `recommend/cache.py:159-190`, `install_hooks.py:485-493` (`_atomic_write_json`), `sprint/rerun_tasks.py:684`, `swarm/normalize.py:264`.
- **Recommendation.** No existing helper implements the design's `_publish`, so write it fresh in `sweep/commands.py` as the design says (`orchestrator-mode.md:88`, `:442`). Model the link-and-`FileExistsError` handling on `sprint/recovery.py:424-434` and the `fsync` step on `swarm/atomic.py:28-31`. Do not import from `swarm` or `sprint`: reflect copies helpers locally instead of importing across subcommand packages (`reflect/commands.py:11-12`, `reflect/runner.py:14-17`), and the design's boundary table allows `commands.py` only its own modules plus `click`, `json` and `os` (`orchestrator-mode.md:213`). One difference to note: the design creates the temp file with `os.open(..., O_WRONLY | O_CREAT | O_EXCL, 0o666)` and a deterministic `.<stem>.<pid>.tmp` name (`orchestrator-mode.md:107`), not `mkstemp`. Both precedents use `mkstemp`/`NamedTemporaryFile`, which create the file with mode `0o600`.

## 8. Thin command plus protocol skill pairs

### 8.1 Command file frontmatter (`src/superclaude/commands/*.md`)

- Fields in order: `name`, `description` (a quoted one-liner), `category`, `complexity`, `mcp-servers: [...]`, `personas: [...]`, `argument-hint: "..."`, and optionally `allowed-tools` (`issue.md:1-9`, `graph.md:1-10`, `reflect.md:1-11`). `name` is the bare command name (`name: issue`, `name: graph`), not `sc:`-prefixed.
- `allowed-tools` is a comma-plus-space separated list. `issue.md` and `reflect.md` have no `allowed-tools`. `graph.md:9` is the precedent for a thin, restricted command: `allowed-tools: Skill, Bash(codegraph init --yes *), Bash(codegraph init -i)`. Sweep's design asks for `allowed-tools: Skill` only (`orchestrator-mode.md:646`).
- **Bash permission pattern syntax.** Current primitives use the space-star form `Bash(<cmd> *)`: `graph.md:9`, and `sc-swarm-wizard-protocol/SKILL.md:7` `Bash(uv run superclaude swarm *)`. The colon-star form `Bash(<cmd>:*)` appears in only one place, `help.md:6`. The design writes the skill's tools as `Bash(superclaude sweep run:*), Bash(uv run --frozen --no-sync superclaude sweep run:*)` (`orchestrator-mode.md:652`). Both forms are accepted by Claude Code (Unverified against Claude Code docs in this pass), but the more recent house style is space-star. The builder should keep the design's literal, because the design's test asserts those exact strings (`orchestrator-mode.md:657`), or change the design and the test together. Flag this as a decision.
- **Body headings.** `issue.md` uses H1 `# /sc:issue: <Title>`, then `## Triggers` ("Explicit only: ..."), `## Usage` (a `text` fenced block), `## Options` (a table with Flag/Default/Values/Meaning columns), `## STOP rules`, `## Examples`, `## Outputs`, `## Boundaries` (**Will:** / **Will Not:**), `## Activation`, and `## Related Commands` (`issue.md:11-101`). `graph.md` has a shorter set: `# /sc:graph`, `## Usage`, `## Options`, `## Activation`, `## Init`, `## Unattended mode`, `## Boundaries` (`graph.md:12-82`).

### 8.2 The `## Activation` block (how the command names its skill)

- Fixed wording (`issue.md:87-93`, `reflect.md:146-151`, `graph.md:41-46`):
  ```
  ## Activation

  **MANDATORY**: Before executing any protocol steps, invoke:
  > Skill sc:<name>-protocol

  Do NOT proceed with protocol execution using only this command file.
  The full behavioral specification is in `~/.claude/skills/sc-<name>-protocol/SKILL.md`.
  ```
- `graph.md:46` adds "Pass the user's subcommand and flags unchanged." Sweep needs the same sentence, since the skill forwards the arguments verbatim to the CLI.
- The skill reference is `> Skill sc:<name>-protocol` (colon form, matching the skill's `name:`), and the file path uses the hyphen form `sc-<name>-protocol`. Tests check the literal `"> Skill sc:graph-protocol"` (`tests/commands/test_graph_command.py:122-123`).
- **Dual surface.** `graph.md:16` and `sc-graph-protocol/SKILL.md:15` name both `~/.claude/...` and the project `.claude/...` copy. The design wants the Activation block to name the project `.claude/skills/sc-sweep-protocol/SKILL.md` copy as well (`orchestrator-mode.md:647`). `issue.md`/`reflect.md` name only the installed path, so `sc-graph-protocol/SKILL.md:15` is the wording model.

### 8.3 Skill frontmatter (`src/superclaude/skills/sc-<name>-protocol/SKILL.md`)

- Fields: `name: sc:<name>-protocol`, a quoted `description`, `allowed-tools`, and optionally `version` (`sc-issue-protocol/SKILL.md:1-5`, `sc-graph-protocol/SKILL.md:1-5`, `sc-reflect-protocol/SKILL.md:1-6`).
- After the frontmatter comes an HTML comment `<!-- Extended metadata (for documentation, not parsed): category / complexity / mcp-servers -->` (`sc-issue-protocol/SKILL.md:7-11`, `sc-graph-protocol/SKILL.md:7-11`).
- Then an H1 (`# sc:graph-protocol`, `sc-graph-protocol/SKILL.md:13`) and a "Backs `/sc:graph` (`~/.claude/commands/sc/graph.md`, or the project `.claude/commands/sc/graph.md`)" line (`:15`), a pattern sweep can copy.
- **Narrow allowlist precedent.** `sc-graph-protocol/SKILL.md:4` lists exact Bash literals, for example `Bash(codegraph --version), Bash(codegraph status), ...`, plus `Read`. Sweep's skill (`Bash(...sweep run...)` twice, plus `Read`) is a narrower version of the same approach.

### 8.4 How a skill calls the `superclaude` CLI

- `sc-recommend/SKILL.md:77, 309, 324` uses `uv run superclaude recommend ...`. `sc-swarm-wizard-protocol/SKILL.md:7` allows `Bash(uv run superclaude swarm *)`. `sc-tasklist-protocol/SKILL.md:1162` uses a bare `superclaude reflect run ...`. `sc-init-lite-protocol/SKILL.md:63` says "shell out to `superclaude init-lite` with the resolved flags via Bash and relay its output", with plain `Bash` allowed (`:4`).
- **No existing skill uses the design's PATH-first, then `uv run --frozen --no-sync` on "command not found" fallback** (grep for `uv run --frozen` and `command not found` across `src/superclaude/{skills,commands}` found only an unrelated README line, `ccsession-tag/README.md:693`). This is a new pattern; the design specifies it in full (`orchestrator-mode.md:653`).
- Stale docstring: `recommend/commands.py:41` says the skill calls `uv run python -m superclaude.cli.recommend`, but `recommend/` has no `__main__.py` and the skill actually uses `uv run superclaude recommend`. Do not copy the `python -m` form, which would also break the UV rule.

### 8.5 Command and skill drift-guard tests

- `tests/commands/test_graph_command.py` is the closest template for the design's `tests/commands/test_sweep_command.py` (`orchestrator-mode.md:657`):
  - path constants via `_REPO = Path(__file__).resolve().parents[2]` (`:16-19`);
  - a minimal frontmatter parser that splits on `---` and partitions on `:` (`:97-102`);
  - `_allowed()` splits `allowed-tools` on `", "` (`:105-106`);
  - an exact-set equality check on the command's and skill's allowed tools (`:126-137`);
  - `_section(text, heading)` slices the text from a heading to the next `## ` (`:109-110`).
  - None of the design's sweep literals contain `", "`, so `_allowed()` works for them unchanged.
- **CLI registration tests.**
  - `tests/recommend/test_cli_registration.py:1-39`: `CliRunner().invoke(main, ["recommend", "--help"])`, asserts exit 0 and that each subcommand name appears.
  - `tests/cli/test_cli_registration.py:31-49`: `EXPECTED_TOP_LEVEL_COMMANDS` is a fixed snapshot that is already missing `swarm` and `reflect`. It is only used to run `--help` on each name (`:95-106`), not checked for equality with the registered commands, so adding `sweep` is optional and nothing breaks if it is left out.
- **Group-level smoke tests.** These invoke the group object directly: `cli_runner.invoke(reflect_group, ["run", "--help"])` and loop over a list of expected flags (`tests/cli/reflect/test_cli_smoke.py:45-55`). The `cli_runner` fixture is defined in `tests/cli/reflect/conftest.py:40-43`.

## 9. Naming summary for the new files

| Item | Convention | Evidence |
|---|---|---|
| Package | `src/superclaude/cli/sweep/` (snake_case, single word) | `cli/recommend/`, `cli/reflect/` |
| Group object | `sweep_group`, `@click.group("sweep")` | `recommend/commands.py:34-35` |
| Subcommand | `@sweep_group.command("run")`, function `run` | `reflect/commands.py:336` (`def run(`) |
| Registration | `main.add_command(sweep_group, name="sweep")` after `main.py:561` | `main.py:551-561` |
| Private helpers | leading underscore: `_git`, `_publish`, `_parse_window` | `reflect/config.py:64`, `reflect/commands.py:492-561` |
| Constants | `_UPPER_SNAKE` private, `UPPER_SNAKE` public (`EVAL_MODES`) | `recommend/commands.py:26-31` |
| stderr prefix | `[sweep <stage>]` | `recommend/commands.py:73` |
| Command file | `src/superclaude/commands/sweep.md`, `name: sweep` | `issue.md:2`, `graph.md:2` |
| Skill dir | `src/superclaude/skills/sc-sweep-protocol/SKILL.md`, `name: sc:sweep-protocol` | `sc-graph-protocol/SKILL.md:2` |
| Tests | `tests/cli/sweep/` with `conftest.py`, plus `tests/commands/test_sweep_command.py` | `tests/cli/reflect/`, `tests/commands/test_graph_command.py` |

The `tests/cli/sweep/` location is inferred from the reflect precedent; the design may name a different test location, which researcher 5 covers.

---

## Summary

1. **Registration and package shape.** Register `sweep_group` with the deferred-import pair at the end of `cli/main.py` (after `:561`), using the exact `# noqa: E402,I001  # intentional: ...` comment. Copy the lazy `__getattr__` from `recommend/__init__.py:12-20` or `tasklist/__init__.py:9-17`; reflect's eager `__init__` is the wrong model. Write `commands.py` with module-level imports limited to the standard library and `click`, imports inside command bodies, `[sweep <stage>]` stderr prefixes, `click.echo(json.dumps(...))` on stdout, and explicit `sys.exit`. Click's `UsageError` gives exit 2 natively.
2. **Python style.** Every module has `from __future__ import annotations`, PEP 604 unions, `collections.abc.Callable`, `@dataclass(frozen=True)` value objects (`reflect/fallback.py:66-93`), and docstrings that state each module's boundaries. Ruff selects `E,F,I,N,W,TID` and ignores `E501` and `N818`, so `GitCallFailed` passes. Subprocess seams are module-level `_git`/`_orca` functions that tests replace with `monkeypatch.setattr(mod, "_git", fake)` (`tests/cli/reflect/conftest.py:58-80`). The AST import-guard template is `tests/swarm/test_concurrency_python_only.py`.
3. **Atomic write: no reusable helper.** The `os.link` exclusive-publish idiom already exists inline at `sprint/recovery.py:424-434` and `install_ccsession.py:75-88`, and the `fsync` step at `swarm/atomic.py:28-31`. Every shared helper uses `os.replace`, which the design rejects, so `_publish` is written fresh in `sweep/commands.py`.
4. **Command and skill files.** The thin-command model is `graph.md`: `allowed-tools: Skill...`, the fixed `## Activation` block with `> Skill sc:<name>-protocol`, and the dual-surface wording. `tests/commands/test_graph_command.py` is the drift-test template.
5. **Open decision.** The design's `Bash(...:*)` allowlist form differs from the space-star house style (`graph.md:9`, `sc-swarm-wizard-protocol/SKILL.md:7`). No skill yet uses the PATH-first, `uv run --frozen --no-sync` fallback.
