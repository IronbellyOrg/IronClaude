# Research: CLI Subcommand Package Pattern
**Status:** Complete
**Date:** 2026-06-08
---

## TL;DR — the precedent for `superclaude reflect run`

Both `prd` and `roadmap` are Click sub-command **packages** under `src/superclaude/cli/<name>/`. The minimal, reusable convention (stripped of pipeline-specific extras) is:

| reflect file | role | precedent |
|---|---|---|
| `__init__.py` | export the group + key public types | `prd/__init__.py:10-14` |
| `commands.py` | `@click.group("reflect")` + `@reflect_group.command()` `run` + all `@click.option`s; lazy-imports config/runner inside the function body | `prd/commands.py:14-145`, `roadmap/commands.py:14-90` |
| `config.py` | `resolve_config(...)` — turn CLI args into a validated dataclass; raises `ValueError` on bad input | `prd/config.py:46-159` |
| `models.py` | `@dataclass` config + result types; Enums for verdict/status | `prd/models.py:169-283` |
| `runner.py` | orchestration class `.run()` returning a result dataclass with an `outcome` field | `PrdExecutor` referenced at `prd/commands.py:113,140-145` |
| `contract.py` | (reflect-specific) parse `return-contract.yaml` → verdict; isolated per Risk §10 (no precedent file — new) |

Registration in `main.py` is a deferred import + `main.add_command(...)` at module bottom.

---

## 1. main.py registration — verbatim (the load-bearing part)

`src/superclaude/cli/main.py:400-434` — every group is registered the SAME way: a deferred import (after all `@main.command()` defs, with the `noqa: E402,I001` comment explaining the deferral avoids circular imports), then `main.add_command(...)`:

```python
# main.py:400-402
from superclaude.cli.sprint import sprint_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports
main.add_command(sprint_group, name="sprint")

# main.py:404-406
from superclaude.cli.roadmap import roadmap_group  # noqa: E402,I001  ...
main.add_command(roadmap_group, name="roadmap")

# main.py:420-422
from superclaude.cli.prd.commands import prd_group  # noqa ...
main.add_command(prd_group, name="prd")

# main.py:424-426
from superclaude.cli.eval.commands import eval_group  # noqa ...
main.add_command(eval_group, name="eval")
```

(Full list registered at main.py:400-434: sprint, roadmap, cleanup-audit, tasklist, cli_portify, prd, eval, recommend, init-lite.)

### Exact lines the reflect group needs (append right after `init-lite`, before `if __name__ == "__main__":` at main.py:437)

```python
from superclaude.cli.reflect.commands import reflect_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports

main.add_command(reflect_group, name="reflect")
```

Notes:
- Two import-source styles coexist: import from the **package** (`from superclaude.cli.roadmap import roadmap_group`, relying on `__init__.py` re-export) vs. import from the **module** (`from superclaude.cli.prd.commands import prd_group`). The newest groups (prd:420, eval:424) import directly from `.commands` — **follow that** for reflect.
- `name="reflect"` is passed explicitly even though `@click.group("reflect")` already names it. prd/roadmap pass `name=` redundantly; cli_portify (main.py:418) omits it. Pass it explicitly, matching prd/roadmap.
- The deferred-import + `noqa: E402,I001` comment is mandatory to keep lint green (imports intentionally not at top of file).

---

## 2. The Click group + command idiom (verbatim shapes to copy)

### Group declaration — `prd/commands.py:14-29`

```python
@click.group("prd")
def prd_group():
    """Generate Product Requirements Documents via multi-step pipeline.
    ...
    Examples:
        superclaude prd run "Build a user auth system" --product my-app
    """
    pass
```

`roadmap/commands.py:14-29` is identical in shape (`@click.group("roadmap")` + docstring with `Examples:` block + `pass`). For reflect: `@click.group("reflect")` with a docstring whose `Examples:` show `superclaude reflect run <tasklist> --tmux`, etc.

### The `run` subcommand idiom — `prd/commands.py:32-145`

The `run` subcommand hangs off the group via `@prd_group.command()` (no explicit name ⇒ Click derives `run` from the function name). Options stack above the function; each maps positionally to a typed parameter:

```python
@prd_group.command()                      # → subcommand name = "run"
@click.argument("request")                # positional arg
@click.option("--product", "-p", default=None, help="...")
@click.option("--where", "-w", multiple=True, help="... (repeatable).")
@click.option(
    "--spec", "-s", multiple=True,
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    help="...",
)
@click.option("--output", "-o", default=None, help="...")
@click.option(
    "--tier",
    type=click.Choice(["lightweight", "standard", "heavyweight"], case_sensitive=False),
    default="standard", help="...",
)
@click.option("--max-turns", type=int, default=300, help="...")
@click.option("--model", default="", help="...")
@click.option("--dry-run", is_flag=True, help="...")
@click.option("--debug", is_flag=True, help="...")
def run(
    request: str,
    product: str | None,
    where: tuple[str, ...],
    spec: tuple[str, ...],
    output: str | None,
    tier: str,
    max_turns: int,
    model: str,
    dry_run: bool,
    debug: bool,
) -> None:
    """Execute the PRD generation pipeline.

    REQUEST is a natural-language description ...
    """
    from .config import resolve_config           # LAZY import inside body
    from .executor import PrdExecutor

    try:
        config = resolve_config(request, product=product, where=where if where else None, ...)
    except ValueError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)

    if dry_run:
        click.echo("Dry run: config validated successfully.")
        click.echo(f"  Request: {config.user_message}")
        ...
        return

    executor = PrdExecutor(config)
    result = executor.run()

    if result.outcome != "success":
        click.echo(f"Pipeline finished with outcome: {result.outcome}", err=True)
        sys.exit(1)
```

Key conventions extracted (all verifiable in `prd/commands.py`):

| Convention | Evidence |
|---|---|
| `from __future__ import annotations` at top → enables `str \| None` hints | `prd/commands.py:7` |
| `import sys` for exit codes; `import click` | `prd/commands.py:9,11` |
| Option→param mapping: `--max-turns` → `max_turns` (kebab→snake auto); custom dest via 2nd positional arg, e.g. roadmap's `@click.option("--output", "output_dir", ...)` | `roadmap/commands.py:44-50` |
| `multiple=True` ⇒ param is a `tuple[str, ...]`; passed downstream as `where if where else None` | `prd/commands.py:42-45,93,118` |
| Enum-ish flags via `click.Choice([...], case_sensitive=False)` | `prd/commands.py:64-68`, `roadmap/commands.py:52-56` |
| Boolean flags via `is_flag=True` | `prd/commands.py:80-89` |
| **Lazy imports of config/executor inside the function body** (not module top) — keeps group import cheap + dodges circular imports | `prd/commands.py:112-113`, `roadmap` does the same |
| `--dry-run` short-circuits with `click.echo` summary + `return` (exit 0) BEFORE constructing the executor | `prd/commands.py:132-138` |
| Full type hints on every param + `-> None` return | `prd/commands.py:90-101` |
| Docstrings: triple-quoted, first line summary, positional ARG documented in CAPS, `Examples:` block | `prd/commands.py:102-111` |

### Exit-code handling (the spec's "fail-closed" maps directly here)

Exit codes are produced by `sys.exit(1)` raised from inside the command body — NOT by returning a value and NOT by `ctx.exit()`. Two paths:
- Config/validation failure: `except ValueError ... click.echo(..., err=True); sys.exit(1)` (`prd/commands.py:128-130`).
- Pipeline non-success: `if result.outcome != "success": ... sys.exit(1)` (`prd/commands.py:143-145`).
- Success / dry-run: plain `return` (Click defaults to exit 0).

For reflect's fail-closed behavior: any parse failure, timeout, or non-promotable verdict ⇒ `click.echo(<reason>, err=True); sys.exit(1)`. A clean parse with a passing verdict ⇒ `return`.

---

## 3. `config.py` precedent — `resolve_config(...)`

`prd/config.py:46-159` defines a module-level **function** `resolve_config(request, *, product=None, ...) -> PrdConfig`. Pattern:

- Signature: first positional is the primary input, everything else keyword-only (`*,`) with defaults (`prd/config.py:46-59`).
- Validates inputs and **raises `ValueError`** with a human-readable message (`prd/config.py:93-97` tier check; `:102-107` resume-step regex check). The command body catches this `ValueError`.
- Resolves paths with `Path(output).resolve()` and falls back to a sensible default dir when omitted (`prd/config.py:109-124`). For reflect, this is where the spec's "output dir template" + "depth floor" defaulting belongs.
- Module-level constants for defaults/validation: `_VALID_TIERS = frozenset({...})` (`prd/config.py:22`), `_STEP_ID_PATTERN = re.compile(...)` (`prd/config.py:26-33`). Reflect equivalents: default timeout `3600`, output-dir template, depth floor.
- Returns a constructed dataclass (`PrdConfig(...)`, `prd/config.py:144-159`), applying `value or default` coalescing (e.g. `max_turns or 300` at `:154`).
- Carries NFR guardrails as module docstring lines: "Zero `async def`/`await`" and "No imports from superclaude.cli.sprint or .roadmap" (`prd/config.py:6-7`). Reflect should state analogous isolation guardrails (esp. the Risk §10 contract-isolation rule).

For reflect, `resolve_config` derives: launch inputs (tasklist path, depth floor applied, timeout default 3600, output dir resolved), promotion mode (`--no-promote` default vs `--promote`), `--allow-single-vendor`, `--tmux`/`--print-command`/`--dry-run` flags → a `ReflectConfig` dataclass.

---

## 4. `models.py` precedent — dataclasses + enums

`prd/models.py` is the template for reflect's `models.py`:

- `from __future__ import annotations` + `from dataclasses import dataclass, field` + `from enum import Enum` + `from pathlib import Path` (`prd/models.py:10-17`).
- **Config dataclass**: `@dataclass class PrdConfig(PipelineConfig)` with typed fields + `field(default_factory=...)` for mutable/computed defaults (`prd/models.py:169-197`). reflect's config dataclass should likewise hold the derived launch inputs. (Note: PrdConfig subclasses a shared `PipelineConfig` from `superclaude.cli.pipeline.models`; reflect's thin wrapper likely does NOT need that base — a standalone `@dataclass` is fine. Confirm against R01/R04 — Unverified whether reflect needs pipeline base.)
- **Computed views via `@property`**: e.g. `research_dir` returns `self.task_dir / "research"` (`prd/models.py:199-212`). Use for reflect's derived output sub-paths.
- **Enum for status/verdict**: `class PrdStepStatus(Enum)` with string values + `@property is_terminal/is_success/is_failure` helper predicates (`prd/models.py:99-161`). This is the precedent for reflect's **verdict enum** (e.g. PASS/FAIL/BLOCKED) with an `is_promotable`-style predicate.
- **Result dataclass with `outcome` field**: `PrdStepResult` (`prd/models.py:220-234`) and aggregate `PrdPipelineResult` with `outcome: str = "success"` (`prd/models.py:242-259`) — the command body keys off `result.outcome`. reflect's runner should return a result dataclass exposing a verdict + an `outcome`-like field the command checks for fail-closed.
- Result types can carry helper methods (`resume_command()` builds a CLI string, `prd/models.py:261-272`).

---

## 5. `runner.py` / orchestration precedent

In prd, the orchestration class is `PrdExecutor` (referenced `prd/commands.py:113,140-145`; defined in `prd/executor.py`, 55KB — much heavier than the reflect wrapper needs). The contract the command relies on is small and clean:

```python
executor = PrdExecutor(config)      # construct from the resolved config dataclass
result = executor.run()             # single .run() entrypoint, returns a result dataclass
if result.outcome != "success":     # command branches on result.outcome
    ...; sys.exit(1)
```

`prd/__init__.py:11` re-exports `PrdExecutor` so it's importable from the package. For reflect, name the class `ReflectRunner` (in `runner.py`), constructed from `ReflectConfig`, with a `.run() -> ReflectResult` method that: derive → launch ClaudeProcess (the `/sc:reflect -p` subprocess) → parse `return-contract.yaml` (delegating to `contract.py`) → derive verdict → write frontmatter → return a result whose `outcome`/verdict the command checks. Keep it THIN (no 8-step pipeline machinery — prd/roadmap's `executor.py`, `gates.py`, `convergence.py`, `monitor.py`, `prompts.py` are pipeline-specific and out of scope for a wrapper).

---

## 6. `contract.py` — no direct precedent (reflect-specific, isolated)

Neither prd nor roadmap has a `contract.py`. The closest analogues are roadmap's parser modules (`roadmap/remediate_parser.py`, `roadmap/spec_parser.py`) which are standalone parse modules with no Click/subprocess coupling. Per the spec's Risk §10 ("isolated per Risk"), `contract.py` should be a **pure module**: takes the path/text of `return-contract.yaml`, parses it, maps to a verdict enum (defined in `models.py`), and is independently unit-testable with zero imports from `commands.py`/`runner.py` (depend only on `models.py`). This mirrors how prd keeps `config.py` free of executor imports and forbids cross-pipeline imports (`prd/config.py:7` NFR-PRD.7). Mark verdict-mapping arithmetic/thresholds as constants here.

---

## 7. Conventions summary (apply across all 6 reflect files)

| Convention | Source of truth |
|---|---|
| `from __future__ import annotations` first line of every module | `prd/commands.py:7`, `prd/config.py:10`, `prd/models.py:10` |
| Module docstring stating purpose + NFR/isolation guardrails | `prd/config.py:1-8`, `prd/models.py:1-8` |
| Google-ish docstrings (`Args:`/`Returns:`/`Raises:`) on public funcs | `prd/config.py:60-90` |
| Full type hints everywhere, `-> None`/`-> PrdConfig` returns | throughout prd |
| Defaults & validation patterns as module-level constants (`frozenset`, compiled regex) | `prd/config.py:22,26` |
| Validation raises `ValueError`; command catches → `click.echo(err=True)` + `sys.exit(1)` | `prd/config.py:93`, `prd/commands.py:128-130` |
| Exit codes via `sys.exit(1)`; success via plain `return` (Click ⇒ 0) | `prd/commands.py:130,145` |
| Lazy imports of heavy deps inside command body | `prd/commands.py:112-113` |
| `__init__.py` re-exports group + key public types via `__all__` | `prd/__init__.py:10-14` |
| No cross-subcommand-package imports (prd forbids importing sprint/roadmap) | `prd/config.py:7`, `prd/models.py:7` |

---

## Summary

**Verified.** `prd` and `roadmap` are the precedent Click sub-command packages; both follow one convention the reflect builder should copy 1:1.

**Registration (main.py:400-434):** every group = deferred import (`# noqa: E402,I001` comment) + `main.add_command(group, name="...")` at file bottom. Newest groups import from `.commands`. Reflect needs exactly two new lines after `init-lite` (before `if __name__ == "__main__":` at main.py:437):
```python
from superclaude.cli.reflect.commands import reflect_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports
main.add_command(reflect_group, name="reflect")
```

**Group + `run` subcommand (prd/commands.py:14-145):** `@click.group("reflect")` → `@reflect_group.command()` def `run(...)`; options stacked as decorators (kebab→snake auto-mapping, `multiple=True`→tuple, `click.Choice(case_sensitive=False)` for enums, `is_flag=True` for booleans). Heavy imports (`config`, `runner`) are LAZY inside the function body. `--dry-run` short-circuits with echo+`return`.

**6-file mapping:** `__init__.py` (re-export group+types), `commands.py` (group+`run`+options), `config.py` (`resolve_config()` raising `ValueError`, defaults: timeout 3600, output-dir template, depth floor), `models.py` (`@dataclass ReflectConfig`, verdict `Enum` with predicate `@property`, `ReflectResult` with `outcome` field), `runner.py` (`ReflectRunner(config).run() -> ReflectResult` — thin: derive→launch→parse→verdict→frontmatter), `contract.py` (pure, isolated `return-contract.yaml`→verdict parser depending only on `models.py`).

**Exit codes / fail-closed:** `sys.exit(1)` from the command body on validation `ValueError` or non-success `result.outcome`; plain `return` on success.

**Caveats:** PrdConfig subclasses a shared `PipelineConfig`; the thin reflect wrapper likely needs only a standalone `@dataclass` — confirm against R01/R04 (Unverified). prd/roadmap's pipeline machinery (`executor.py` 55KB, `gates.py`, `convergence.py`, `monitor.py`, `prompts.py`) is OUT of scope for a wrapper; do not replicate it.

**Status:** Complete
