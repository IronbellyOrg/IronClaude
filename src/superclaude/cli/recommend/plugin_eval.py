"""Plugin synthetic-eval: precondition self-check (HARD-BLOCK) + adoption gate.

Step 5.5 — preconditions: dispatch on `kind` and REUSE the install_mcp checks
(``check_mcp_server_installed`` / ``check_binary_available`` — both fail-closed to
False) plus ``Path.exists()`` for ``file_present``. ``failure_mode: hard`` is the
OQ2-RESOLVED HARD-BLOCK: NO degraded-data fallback — abort the plugin eval with the
``failure_message``. ``warn`` records a warning and continues; ``skip`` drops the
dependent eval.

Step 5.6 — adoption gate: with/without-resource delta vs thresholds
(``pass_rate +>=0.10`` OR ``tokens -<=-0.20`` with ``must_not_regress: [pass_rate]``)
-> ``adoption_status`` on the plugin-table row via the atomic ``LookupCache.save()``
writer (``.claude/cache/sc-recommend-plugin.yaml``).

No ``anthropic`` import; the MCP/binary checks are subprocess-based and imported,
not reimplemented.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from superclaude.cli.install_mcp import (
    check_binary_available,
    check_mcp_server_installed,
)

from .cache import LookupCache, compute_surface_hash

# Adoption-gate thresholds (round-4 suite-level adoption_gate / research/03 §5).
THRESHOLD_PASS_RATE_DELTA = 0.10
THRESHOLD_TOKEN_DELTA = -0.20
MUST_NOT_REGRESS = ("pass_rate",)


class PluginPreconditionError(RuntimeError):
    """Raised on a HARD-BLOCK precondition failure (no degraded fallback)."""


def check_precondition(precondition: dict) -> bool:
    """Return True if the single precondition is satisfied.

    Dispatches on ``kind``; reuses install_mcp checks for server/binary and
    ``Path.exists()`` for files. Unknown kinds are treated as unsatisfied.
    """
    kind = precondition.get("kind")
    if kind == "mcp_server_installed":
        return check_mcp_server_installed(precondition.get("server", ""))
    if kind == "binary_available":
        return check_binary_available(precondition.get("binary", ""))
    if kind == "file_present":
        return Path(precondition.get("path", "")).exists()
    return False


def run_preconditions(preconditions: list[dict]) -> list[dict]:
    """Run all preconditions BEFORE any eval runs.

    Raises ``PluginPreconditionError`` on the FIRST ``failure_mode: hard`` failure
    (the OQ2-RESOLVED HARD-BLOCK — no degraded fallback). Returns the list of
    non-hard issues (``warn``/``skip``) so the caller can record them.
    """
    issues: list[dict] = []
    for pc in preconditions:
        if check_precondition(pc):
            continue
        mode = pc.get("failure_mode", "hard")
        message = pc.get("failure_message", f"precondition not met: {pc.get('kind')}")
        if mode == "hard":
            raise PluginPreconditionError(message)
        if mode in ("warn", "skip"):
            issues.append(
                {"precondition": pc, "failure_mode": mode, "message": message}
            )
        else:
            # Unknown failure_mode is conservatively treated as hard.
            raise PluginPreconditionError(
                f"unknown failure_mode {mode!r} for precondition {pc.get('kind')!r}; "
                f"treating as hard. {message}"
            )
    return issues


def evaluate_adoption(with_resource: dict, without_resource: dict) -> dict:
    """Compute the adoption verdict from with/without-resource aggregates.

    Threshold (research/03 §5): pass_rate +>=0.10 OR token -<=-0.20, AND pass_rate
    must not regress. Returns ``{adoption_status, pass_rate_delta, token_delta,
    regressed}`` where adoption_status is ``evaluated_positive``/``evaluated_negative``.
    """
    pass_rate_delta = round(
        with_resource["pass_rate"] - without_resource["pass_rate"], 4
    )
    base_tokens = without_resource.get("mean_tokens", 0) or 0
    if base_tokens:
        token_delta = round(
            (with_resource.get("mean_tokens", 0) - base_tokens) / base_tokens, 4
        )
    else:
        token_delta = 0.0

    # must_not_regress guard: pass_rate may not drop.
    regressed = pass_rate_delta < 0 and "pass_rate" in MUST_NOT_REGRESS

    improved = (
        pass_rate_delta >= THRESHOLD_PASS_RATE_DELTA
        or token_delta <= THRESHOLD_TOKEN_DELTA
    )
    positive = improved and not regressed
    return {
        "adoption_status": "evaluated_positive" if positive else "evaluated_negative",
        "pass_rate_delta": pass_rate_delta,
        "token_delta": token_delta,
        "regressed": regressed,
    }


def patch_plugin_row(
    *,
    plugin_path: Path,
    key: str,
    verdict: dict,
    date: str | None = None,
) -> dict:
    """Patch the plugin-table row's adoption_status + eval_history (atomic writer).

    Returns the verdict dict. The plugin table is a separate YAML
    (``.claude/cache/sc-recommend-plugin.yaml``) sharing the LookupCache schema.
    """
    surface_hash = compute_surface_hash()
    cache = LookupCache.load_or_create(plugin_path, surface_hash)
    row = cache.get_row(key)
    if row is None:
        row = {"key": key, "native_fallback": False}
    row["adoption_status"] = verdict["adoption_status"]
    history = row.setdefault("eval_history", [])
    history.append(
        {
            "date": date or datetime.now(timezone.utc).isoformat(),
            "pass_rate_delta": verdict["pass_rate_delta"],
            "token_delta": verdict["token_delta"],
            "regressed": verdict["regressed"],
            "verdict": verdict["adoption_status"],
        }
    )
    cache.upsert_row(row)
    cache.save()
    return verdict
