# Discovery — plugin-eval gate surface (Step 2.2)

**Date:** 2026-06-03

## `plugin_eval.py` public functions (verbatim contracts)

```python
class PluginPreconditionError(RuntimeError): ...

def run_preconditions(preconditions: list[dict]) -> list[dict]:
    # Raises PluginPreconditionError on the FIRST failure_mode: hard failure (HARD-BLOCK, no fallback).
    # Unknown failure_mode → treated as hard (raises). warn/skip → appended to issues list, continues.
    # Returns the list of warn/skip issue dicts.

def evaluate_adoption(with_resource: dict, without_resource: dict) -> dict:
    # with_resource/without_resource carry pass_rate + mean_tokens.
    # THRESHOLD_PASS_RATE_DELTA = 0.10 ; THRESHOLD_TOKEN_DELTA = -0.20 ; MUST_NOT_REGRESS = ("pass_rate",)
    # positive = (pass_rate_delta >= 0.10 OR token_delta <= -0.20) AND not regressed.
    # regressed = pass_rate_delta < 0.
    # Returns {adoption_status: evaluated_positive|evaluated_negative, pass_rate_delta, token_delta, regressed}.

def patch_plugin_row(*, plugin_path: Path, key: str, verdict: dict, date: str | None = None) -> dict:
    # LookupCache.load_or_create(plugin_path, surface_hash) → get_row(key) (or new {key, native_fallback:False})
    # → sets row["adoption_status"]=verdict["adoption_status"], appends eval_history entry → upsert_row → save (atomic).
    # Returns the verdict dict.
```

`check_precondition(precondition: dict) -> bool` dispatches on `kind` ∈ {mcp_server_installed, binary_available, file_present}.

## `commands.py` Click-group registration pattern to mirror

- Top group: `@recommend_group.group("eval")` → `eval_group()` (commands.py:194).
- Subcommand: `@eval_group.command("run")` with stacked `@click.option(...)`; body defers heavy imports (`from .eval_pipeline import ...`), validates, calls helpers, `click.echo` result, `sys.exit(1)` on failure.
- Module-level constants: `_DEFAULT_CACHE = Path(".claude/cache/sc-recommend-lookup.yaml")`, `EVAL_MODES = ["none","quick","normal","deep"]`, `import json, sys`, `from pathlib import Path`, `import click`.

## New subcommand plan (Step 2.3) — `recommend eval plugin`

`@eval_group.command("plugin")` with options:
- `--key` (required) — plugin-table row key.
- `--preconditions-file` (Path, JSON list of precondition dicts).
- `--with-resource-file` / `--without-resource-file` (Path, JSON dicts with pass_rate + mean_tokens).
- `--plugin-cache-path` (Path, default `.claude/cache/sc-recommend-plugin.yaml`).
- `--date` (str, optional).

Body: defer-import `run_preconditions, evaluate_adoption, patch_plugin_row, PluginPreconditionError` from `.plugin_eval`; load JSON inputs; call `run_preconditions(preconditions)` FIRST inside try/except — on `PluginPreconditionError` print to stderr + `sys.exit(1)` (HARD-BLOCK, no catch-and-continue); then `evaluate_adoption(...)` → `patch_plugin_row(...)`; echo the verdict + patched path.

## Plugin cache path

`.claude/cache/sc-recommend-plugin.yaml` (separate from the lookup cache; shares LookupCache schema).
