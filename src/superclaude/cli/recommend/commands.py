"""Recommend CLI commands -- Click command group for ``superclaude recommend``.

Exposes the deterministic-helper surface the ``sc-recommend`` skill shells out
to between Agent calls: lookup-cache read/write (``cache get`` / ``cache put``),
telemetry append (``telemetry append``), and the opt-in ``--eval`` pipeline
(``eval run``). Heavy imports are deferred inside each command body to keep
``superclaude --help`` fast, mirroring the ``cli/tasklist`` precedent
(``commands.py:96``). The hot/cold dispatch orchestration itself lives in skill
prose; this module owns only the file/eval operations.

The precise subcommand set that *owns dispatch* is contingent on the Phase 2
Python-vs-skill boundary decision (Step 2.1). At MVP this group declares only
the boundary-independent deterministic helpers; any dispatch-owning subcommand
(or a thin ``executor.py`` orchestration shim) is authored in the relevant
Phase 4/5 item ONLY if the chosen boundary option requires it.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click

_DEFAULT_CACHE = Path(".claude/cache/sc-recommend-lookup.yaml")
_DEFAULT_EVENTS = Path(".claude/cache/sc-recommend-events.jsonl")

# --eval mode panel selector. Constrained to the spec's closed mode set;
# default ``none`` preserves the OQ1-RESOLVED opt-in (auto-eval was REJECTED).
EVAL_MODES = ["none", "quick", "normal", "deep"]


@click.group("recommend")
def recommend_group() -> None:
    """sc-recommend lookup-cache deterministic helpers.

    Backs the ``sc-recommend`` skill's hot/cold-path dispatch with file and
    eval operations a Haiku subagent cannot perform (writing files, hashing,
    aggregation). The skill shells to these subcommands via
    ``Bash(uv run python -m superclaude.cli.recommend ...)``.

    Examples:
        superclaude recommend cache get spec-generation
        superclaude recommend telemetry append --mode delegate --cache-result hit --classification-key spec-generation --duration-ms 4200
        superclaude recommend eval run --mode quick --key spec-generation
    """
    pass


@recommend_group.group("cache")
def cache_group() -> None:
    """Deterministic lookup-cache file operations (read/write rows)."""
    pass


@cache_group.command("get")
@click.argument("key")
@click.option(
    "--cache-path",
    type=click.Path(path_type=Path),
    default=_DEFAULT_CACHE,
    help="Path to the lookup-cache YAML. Default: .claude/cache/sc-recommend-lookup.yaml.",
)
def cache_get(key: str, cache_path: Path) -> None:
    """Print the cached row for KEY as JSON, or exit 1 if absent."""
    from .cache import LookupCache, compute_surface_hash

    surface_hash = compute_surface_hash()
    cache = LookupCache.load_or_create(cache_path.resolve(), surface_hash)
    row = cache.get_row(key)
    if row is None:
        click.echo(f"[recommend cache get] No row for key {key!r}", err=True)
        sys.exit(1)
    click.echo(json.dumps(row, ensure_ascii=False))


@cache_group.command("put")
@click.option(
    "--cache-path",
    type=click.Path(path_type=Path),
    default=_DEFAULT_CACHE,
    help="Path to the lookup-cache YAML. Default: .claude/cache/sc-recommend-lookup.yaml.",
)
@click.option(
    "--row-json",
    required=True,
    help="A single cache row encoded as a JSON object (must include a 'key' field).",
)
def cache_put(cache_path: Path, row_json: str) -> None:
    """Upsert one row (given as --row-json) into the lookup cache via the atomic writer.

    Under Option P the per-row ``source_hash`` is the CLI's deterministic job, NOT
    the cold-path Haiku's: a Haiku-supplied row carries only the ``source_path`` it
    Read in Phase 0 Step C, and this command recomputes ``source_hash`` (Read +
    sha256) and stamps ``last_validated_at`` on write. Any ``source_hash`` present
    in ``--row-json`` is discarded and recomputed so the parent never trusts a
    Haiku-computed hash. Without this, a cold-inserted row would lack a valid
    ``source_hash`` and the next hot-path lookup would always return
    ``miss_validation_stale`` — the cache would never warm.
    """
    from datetime import datetime, timezone

    from .cache import LookupCache, compute_source_hash, compute_surface_hash

    row = json.loads(row_json)
    if not isinstance(row, dict) or "key" not in row:
        click.echo(
            "[recommend cache put] --row-json must be a JSON object with a 'key' field",
            err=True,
        )
        sys.exit(1)

    # Deterministically (re)compute the per-row source_hash from source_path so the
    # next hot-path dispatch can validate the row. native_fallback rows have no
    # candidate source and are exempt. Discard any Haiku-supplied source_hash.
    row.pop("source_hash", None)
    if not row.get("native_fallback"):
        source_path = row.get("source_path")
        if not source_path:
            click.echo(
                "[recommend cache put] non-native rows must include 'source_path' so "
                "the CLI can compute source_hash (Option P: hashing is the CLI's job)",
                err=True,
            )
            sys.exit(1)
        src = Path(source_path)
        if not src.exists():
            click.echo(
                f"[recommend cache put] source_path {source_path!r} does not exist; "
                "cannot compute source_hash",
                err=True,
            )
            sys.exit(1)
        row["source_hash"] = compute_source_hash(src.read_bytes())
        row["last_validated_at"] = datetime.now(timezone.utc).isoformat()

    surface_hash = compute_surface_hash()
    cache = LookupCache.load_or_create(cache_path.resolve(), surface_hash)
    cache.upsert_row(row)
    cache.save()
    click.echo(f"[recommend cache put] Committed row {row['key']!r} to {cache_path}")


@recommend_group.group("telemetry")
def telemetry_group() -> None:
    """Append-only telemetry JSONL operations."""
    pass


@telemetry_group.command("append")
@click.option("--mode", required=True, help="Invocation mode (e.g. delegate, plugin).")
@click.option(
    "--cache-result",
    required=True,
    help="One of the closed 6-value cache_result enum.",
)
@click.option(
    "--classification-key",
    required=True,
    help="The classifier key (or 'unknown' on no-match).",
)
@click.option(
    "--duration-ms", type=int, required=True, help="Wall-clock duration in ms."
)
@click.option(
    "--events-path",
    type=click.Path(path_type=Path),
    default=_DEFAULT_EVENTS,
    help="Path to the telemetry JSONL. Default: .claude/cache/sc-recommend-events.jsonl.",
)
def telemetry_append(
    mode: str,
    cache_result: str,
    classification_key: str,
    duration_ms: int,
    events_path: Path,
) -> None:
    """Append exactly one telemetry event line (5 fields) to the JSONL."""
    from .telemetry import append_event

    try:
        append_event(
            events_path.resolve(),
            mode=mode,
            cache_result=cache_result,
            classification_key=classification_key,
            duration_ms=duration_ms,
        )
    except ValueError as exc:
        click.echo(f"[recommend telemetry append] {exc}", err=True)
        sys.exit(1)
    click.echo(f"[recommend telemetry append] event appended to {events_path}")


@recommend_group.group("eval")
def eval_group() -> None:
    """Per-row / plugin ``--eval`` pipeline (opt-in; default mode none)."""
    pass


@eval_group.command("run")
@click.option(
    "--mode",
    type=click.Choice(EVAL_MODES),
    default="none",
    help="Eval panel: none (no-op), quick (opus x1), normal (opus+sonnet x2), deep (opus+sonnet+haiku x3).",
)
@click.option(
    "--key",
    default=None,
    help="The lookup-cache row key to evaluate (best_model populated on this row).",
)
@click.option(
    "--cache-path",
    type=click.Path(path_type=Path),
    default=_DEFAULT_CACHE,
    help="Path to the lookup-cache YAML.",
)
@click.option(
    "--iteration",
    type=int,
    default=1,
    help="Eval iteration number (results dir suffix).",
)
@click.option(
    "--eval-runs-dir",
    type=click.Path(path_type=Path),
    default=None,
    help="Per-iteration eval-runs dir. Default: .claude/cache/eval-runs/iteration-<N>/.",
)
@click.option(
    "--assertions-file",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="JSON file: {eval_name, assertions:[{text,type,value}]} graded against each run.",
)
@click.option(
    "--tier", default="balanced", help="best_model tier (quality|speed|cost|balanced)."
)
def eval_run(
    mode: str,
    key: str | None,
    cache_path: Path,
    iteration: int,
    eval_runs_dir: Path | None,
    assertions_file: Path | None,
    tier: str,
) -> None:
    """Finalize the per-row best_model eval panel for --key under --mode.

    Option P: the SKILL.md prose emits the parallel per-(model, run) Agent fan-out
    (the CLI cannot spawn Agents) and each Agent writes its deliverable +
    timing.json under the eval-runs tree. THIS subcommand owns the deterministic
    half — grade each deliverable, aggregate per model, select best_model, write
    `row-<key>-results.json`, and patch the lookup row's best_model + eval_history
    via the atomic writer. No `anthropic` import; no in-process model call.
    """
    if mode == "none":
        click.echo(
            "[recommend eval run] mode=none -> no evaluation performed (opt-in default)."
        )
        return
    if not key:
        click.echo("[recommend eval run] --key is required when mode != none", err=True)
        sys.exit(1)

    from .eval_pipeline import collect_run_records, finalize_eval

    runs_dir = eval_runs_dir or (
        Path(".claude/cache/eval-runs") / f"iteration-{iteration}"
    )
    runs_dir = runs_dir.resolve()

    eval_name = key
    assertions: list[dict] = []
    if assertions_file is not None:
        spec = json.loads(assertions_file.read_text(encoding="utf-8"))
        eval_name = spec.get("eval_name", key)
        assertions = spec.get("assertions", [])

    runs = collect_run_records(
        eval_runs_dir=runs_dir,
        key=key,
        mode=mode,
        eval_name=eval_name,
        assertions=assertions,
    )
    results = finalize_eval(
        key=key,
        iteration=iteration,
        mode=mode,
        runs=runs,
        eval_runs_dir=runs_dir,
        cache_path=cache_path.resolve(),
        tier=tier,
    )
    best = results["best_model"]
    verdict = (
        "model-agnostic (hint suppressed)" if best.get("suppressed") else best["model"]
    )
    click.echo(
        f"[recommend eval run] key={key} mode={mode} -> best_model={verdict} "
        f"(confidence={best['confidence']}); results: {runs_dir / f'row-{key}-results.json'}"
    )


_DEFAULT_PLUGIN_CACHE = Path(".claude/cache/sc-recommend-plugin.yaml")


@eval_group.command("plugin")
@click.option(
    "--key",
    required=True,
    help="Plugin-table row key (the plugin/resource identifier).",
)
@click.option(
    "--preconditions-file",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="JSON file: a list of precondition dicts (kind/server/binary/path/failure_mode/failure_message).",
)
@click.option(
    "--with-resource-file",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help="JSON file: with-resource aggregate {pass_rate, mean_tokens}.",
)
@click.option(
    "--without-resource-file",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help="JSON file: without-resource aggregate {pass_rate, mean_tokens}.",
)
@click.option(
    "--plugin-cache-path",
    type=click.Path(path_type=Path),
    default=_DEFAULT_PLUGIN_CACHE,
    help="Path to the plugin-table YAML.",
)
@click.option(
    "--date",
    default=None,
    help="Optional ISO date override for the eval_history entry.",
)
def eval_plugin(
    key: str,
    preconditions_file: Path | None,
    with_resource_file: Path,
    without_resource_file: Path,
    plugin_cache_path: Path,
    date: str | None,
) -> None:
    """Run the plugin adoption gate: preconditions (HARD-BLOCK) -> adoption verdict -> row patch.

    Wires the orphaned ``plugin_eval`` helpers into a real caller (F4 remediation). The
    Agent fan-out that produces the with/without-resource eval panels is the skill's job;
    this subcommand owns the deterministic half — the precondition HARD-BLOCK, the adoption
    verdict, and the atomic plugin-row patch. ``run_preconditions`` is called FIRST and a
    ``failure_mode: hard`` failure aborts with exit 1 (no degraded fallback).
    """
    from .plugin_eval import (
        PluginPreconditionError,
        evaluate_adoption,
        patch_plugin_row,
        run_preconditions,
    )

    preconditions = (
        json.loads(preconditions_file.read_text(encoding="utf-8"))
        if preconditions_file is not None
        else []
    )
    try:
        issues = run_preconditions(preconditions)
    except PluginPreconditionError as exc:
        click.echo(
            f"[recommend eval plugin] HARD-BLOCK precondition failed: {exc}", err=True
        )
        sys.exit(1)
    for issue in issues:
        click.echo(
            f"[recommend eval plugin] precondition {issue['failure_mode']}: {issue['message']}",
            err=True,
        )

    with_resource = json.loads(with_resource_file.read_text(encoding="utf-8"))
    without_resource = json.loads(without_resource_file.read_text(encoding="utf-8"))
    verdict = evaluate_adoption(with_resource, without_resource)
    patch_plugin_row(
        plugin_path=plugin_cache_path.resolve(),
        key=key,
        verdict=verdict,
        date=date,
    )
    click.echo(
        f"[recommend eval plugin] key={key} -> {verdict['adoption_status']} "
        f"(pass_rate_delta={verdict['pass_rate_delta']}, token_delta={verdict['token_delta']}, "
        f"regressed={verdict['regressed']}); patched {plugin_cache_path}"
    )


@recommend_group.command("dispatch")
@click.option(
    "--key", default=None, help="classification_key emitted by the Haiku classifier."
)
@click.option(
    "--native-likely",
    is_flag=True,
    default=False,
    help="Set when the classifier judged the task better done natively.",
)
@click.option(
    "--delta",
    type=float,
    default=1.0,
    help="confidence_top2_delta from the classifier (< 0.10 -> miss_low_confidence).",
)
@click.option(
    "--cache-path",
    type=click.Path(path_type=Path),
    default=_DEFAULT_CACHE,
    help="Path to the lookup-cache YAML.",
)
@click.option(
    "--budget-used",
    type=int,
    default=0,
    help="Cumulative hot-path tokens already spent.",
)
@click.option(
    "--budget-limit", type=int, default=10000, help="Hot-path token budget ceiling."
)
def dispatch_cmd(
    key: str | None,
    native_likely: bool,
    delta: float,
    cache_path: Path,
    budget_used: int,
    budget_limit: int,
) -> None:
    """Option-P deterministic hot-path dispatch (scan/validate/budget).

    Consumes the Haiku classifier's output and prints a JSON DispatchResult:
    a hot HIT carries the row's filled prompt_envelope_template + best_model hint;
    a MISS carries one of the closed-enum miss reasons (the skill then spawns the
    cold-path Agent); NATIVE means recommend native tooling (no cold path). This
    subcommand does NOT write telemetry — the skill logs exactly one event per
    invocation once the final outcome (incl. any cold_inserted) is known.
    """
    from .dispatch import dispatch

    result = dispatch(
        classification_key=key,
        native_likely=native_likely,
        confidence_top2_delta=delta,
        cache_path=cache_path.resolve(),
        budget_tokens_used=budget_used,
        budget_limit=budget_limit,
    )
    click.echo(json.dumps(result.to_dict(), ensure_ascii=False))
