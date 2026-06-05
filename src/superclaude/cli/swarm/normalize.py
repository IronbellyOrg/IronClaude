"""T04.01 -- COMP-008 Wave 2 normalize dispatcher.

``normalize_wave2`` is the single Wave-2 entrypoint. It receives the
``WorkerResult`` list emitted by the M3 dispatcher (COMP-007) plus a
recipe name (from :class:`NormalizationSpec.recipe`) and returns a new
``WorkerResult`` list with normalized bodies written to ``final_path``
and provenance written to ``meta_path`` as a JSON sidecar.

Contract (FR-LENSREG.NS / §3.3 / §4.1)
======================================

* Recipe selection: the registry is :data:`recipes.REGISTRY`. The
  caller supplies ``recipe_name`` -- the lens-driven default at
  preflight stamps this onto :class:`NormalizationSpec.recipe` per
  FR-020, and ``normalize_wave2`` resolves it via the REGISTRY lookup.
* Recipe contract: each registered Recipe implements
  ``normalize(raw_output: str, args: dict) -> NormalizedResult``. The
  canonical Protocol and the :class:`NormalizedResult` dataclass live
  in :mod:`superclaude.cli.swarm.recipes` (T04.02); this module
  re-exports them so callers can keep importing ``Recipe`` /
  ``NormalizedResult`` from either side. While REGISTRY entries
  remain at the M2 ``None`` sentinel, the dispatcher falls back to
  :class:`_PassthroughFallback` so the dispatcher surface lands ahead
  of the per-recipe modules (T04.03..T04.09).
* Per-worker output: each worker's normalized body is written to
  ``worker.final_path`` via write-to-tmp + ``os.replace`` (IMM-6 /
  NFR-002). The meta sidecar is written to ``worker.meta_path``
  carrying ``{recipe, schema_version, salvaged, status}``.
* AC-011 boundary: recipes own the per-worker shape transformation
  and MUST NOT score, dedupe, or reorder findings. The dispatcher
  itself never inspects body content -- it only routes the recipe
  call and persists the result.

Salvage (FR-028 / §7.4)
========================

T04.11 lands the full §7.4 ``parse_error -> success`` salvage
promotion. The decision is centralized in :func:`salvage_parse_error`
(returns the promoted ``WorkerResult``) and :func:`salvage_decision`
(returns the matching :class:`SalvageDecision` provenance record); the
dispatcher calls both so the per-worker WorkerResult and the meta
sidecar agree on the reason. Conditions for promotion -- ALL must hold:

  1. ``worker.status == "parse_error"`` -- only parse_error is
     salvageable; success / timeout / proxy_error are never promoted.
  2. ``salvage_enabled is True`` -- mirrors
     :attr:`NormalizationSpec.on_parse_error.salvage`. When False the
     decision rejects with ``reason="rejected_salvage_disabled"``.
  3. ``normalized.salvaged is True`` -- recipe explicitly signaled
     that it recovered structure from the malformed body. A recipe
     that returns ``salvaged=False`` is never promoted (even if its
     text is non-empty) so recipes can produce best-effort partial
     output without claiming success.
  4. ``normalized.text`` non-empty -- there must be a body to emit
     under the promoted status.

The decision's ``reason`` field is a stable token recorded on the
meta sidecar (``salvage_reason``) and used by the parse_error_salvage
test suite to pin every branch. Hard-failure short-circuits never call
the salvage path because no recipe was invoked -- the dispatcher emits
the sidecar with ``salvaged=False`` and no ``salvage_reason``.

Hard-failure short-circuit
==========================

``WorkerResult.status in {"timeout", "proxy_error"}`` skips
normalization (no body to normalize, no final path to write). The
meta sidecar is still emitted so the per-worker provenance surface is
uniform across all status branches -- M5 reduce and M6 resume can
read every worker's meta without conditionals.
"""

from __future__ import annotations

import dataclasses
import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from superclaude.cli.swarm.models import WorkerResult
from superclaude.cli.swarm.recipes import (
    REGISTRY,
    NormalizedResult,
    Recipe,
)


__all__ = [
    "NormalizedResult",
    "Recipe",
    "SalvageDecision",
    "normalize_wave2",
    "salvage_decision",
    "salvage_parse_error",
]


# §7.4 salvage reason tokens (stable strings recorded on meta sidecar).
SALVAGE_PROMOTED = "promoted_recipe_signal"
SALVAGE_REJECTED_NOT_PARSE_ERROR = "rejected_not_parse_error"
SALVAGE_REJECTED_DISABLED = "rejected_salvage_disabled"
SALVAGE_REJECTED_NO_RECIPE_SIGNAL = "rejected_no_recipe_signal"
SALVAGE_REJECTED_EMPTY_TEXT = "rejected_empty_text"


@dataclass(frozen=True)
class SalvageDecision:
    """§7.4 salvage decision and provenance (FR-028).

    Returned by :func:`salvage_decision` and read by the dispatcher
    when stamping the meta sidecar so the on-disk provenance agrees
    with the WorkerResult :func:`salvage_parse_error` returns.

    Attributes:
        promoted: ``True`` when status flipped ``parse_error -> success``;
            ``False`` otherwise (the worker's status is unchanged).
        reason: stable token identifying which §7.4 branch fired. One
            of the ``SALVAGE_*`` constants exported by this module.
        salvaged_text_bytes: byte count of ``normalized.text`` (0 when
            no recipe result was supplied, e.g. hard-failure path).
            Used by the meta sidecar emitter so the bytes-written
            value reflects the salvage-promoted body rather than the
            raw body.
    """

    promoted: bool
    reason: str
    salvaged_text_bytes: int = 0


def salvage_decision(
    worker_result: WorkerResult,
    *,
    normalized: NormalizedResult,
    salvage_enabled: bool = True,
) -> SalvageDecision:
    """Evaluate §7.4 salvage conditions for a single worker result.

    See module docstring (Salvage section) for the four conditions.
    The return value is a pure decision record -- this function does
    NOT mutate ``worker_result``, write the meta sidecar, or touch
    ``final_path``. Callers route the decision into
    :func:`salvage_parse_error` (for the WorkerResult) and
    :func:`_emit_meta` (for the sidecar).

    Args:
        worker_result: the pre-promotion WorkerResult from the
            dispatcher. Only ``status`` is consulted.
        normalized: the :class:`NormalizedResult` the recipe returned
            for this worker.
        salvage_enabled: mirror of
            :attr:`NormalizationSpec.on_parse_error.salvage`. Default
            ``True`` to preserve the spec's default-on policy.

    Returns:
        A :class:`SalvageDecision` recording whether §7.4 promotion
        fires and, when it does not, which condition rejected it.
    """
    text_bytes = len(normalized.text.encode("utf-8")) if normalized.text else 0
    if worker_result.status != "parse_error":
        return SalvageDecision(
            promoted=False,
            reason=SALVAGE_REJECTED_NOT_PARSE_ERROR,
            salvaged_text_bytes=text_bytes,
        )
    if not salvage_enabled:
        return SalvageDecision(
            promoted=False,
            reason=SALVAGE_REJECTED_DISABLED,
            salvaged_text_bytes=text_bytes,
        )
    if not normalized.salvaged:
        return SalvageDecision(
            promoted=False,
            reason=SALVAGE_REJECTED_NO_RECIPE_SIGNAL,
            salvaged_text_bytes=text_bytes,
        )
    if not normalized.text:
        return SalvageDecision(
            promoted=False,
            reason=SALVAGE_REJECTED_EMPTY_TEXT,
            salvaged_text_bytes=text_bytes,
        )
    return SalvageDecision(
        promoted=True,
        reason=SALVAGE_PROMOTED,
        salvaged_text_bytes=text_bytes,
    )


def salvage_parse_error(
    worker_result: WorkerResult,
    *,
    normalized: NormalizedResult,
    salvage_enabled: bool = True,
) -> WorkerResult:
    """Promote ``parse_error -> success`` per §7.4 when salvageable.

    Returns a new ``WorkerResult`` (via ``dataclasses.replace``):

    * On promotion: ``status="success"`` and ``bytes`` reflects the
      recipe's salvaged body (encoded UTF-8 byte count).
    * On rejection (any §7.4 condition unmet): the input worker is
      returned via ``dataclasses.replace`` with no field changes.

    This function intentionally **does not** write the meta sidecar
    or ``final_path``; the dispatcher owns those writes so the salvage
    decision and the on-disk artifacts stay atomic together.

    Args:
        worker_result: the pre-promotion WorkerResult.
        normalized: the recipe's :class:`NormalizedResult`.
        salvage_enabled: §7.4 config gate (default ``True`` per the
            ``NormalizationSpec.on_parse_error.salvage=True`` default).

    Returns:
        A new ``WorkerResult`` -- promoted to ``success`` when §7.4
        conditions hold, otherwise an unchanged copy of the input.
    """
    decision = salvage_decision(
        worker_result,
        normalized=normalized,
        salvage_enabled=salvage_enabled,
    )
    if not decision.promoted:
        return dataclasses.replace(worker_result)
    return dataclasses.replace(
        worker_result,
        status="success",
        bytes=decision.salvaged_text_bytes,
    )


class _PassthroughFallback:
    """Pre-T04.02 fallback recipe used when REGISTRY[name] is ``None``.

    The :data:`recipes.REGISTRY` ships with M2-era sentinel ``None``
    values for every recipe name; T04.03..T04.09 swap them for real
    Recipe objects. While that sequence is in flight, the dispatcher
    needs *some* callable to route through so the M3->M4 handshake can
    be exercised. The passthrough returns the raw body unchanged with
    ``salvaged=False`` -- it is intentionally NOT registered into the
    REGISTRY because doing so would mask a "recipe missing" bug.
    """

    def normalize(
        self, raw_output: str, args: dict[str, Any]
    ) -> NormalizedResult:
        del args
        return NormalizedResult(text=raw_output, salvaged=False)


def _resolve_recipe(name: str) -> Recipe:
    """Look up ``name`` in :data:`recipes.REGISTRY`.

    Returns the registered Recipe when it conforms to the Protocol.
    Returns a passthrough fallback when REGISTRY carries the M2
    sentinel ``None`` (pre-T04.03..T04.09). Raises ``KeyError`` when
    the name is not registered at all -- this surfaces lens validator
    drift (FR-LENSREG.NS / U-008 should have caught it at preflight).
    Raises ``TypeError`` when the registered value is neither ``None``
    nor a Protocol-conforming object.
    """
    if name not in REGISTRY:
        raise KeyError(
            f"recipe {name!r} not registered in recipes.REGISTRY; "
            f"known: {sorted(REGISTRY)}"
        )
    entry = REGISTRY[name]
    if entry is None:
        return _PassthroughFallback()
    if isinstance(entry, Recipe):
        return entry
    raise TypeError(
        f"recipe {name!r} (type {type(entry).__name__}) does not "
        f"implement Recipe Protocol (normalize(raw_output, args) -> "
        f"NormalizedResult)"
    )


def _atomic_write_text(path: Path, content: str) -> int:
    """Write ``content`` to ``path`` via tmp file + ``os.replace`` (IMM-6).

    Returns the number of bytes written. The tmp file lives in the
    same directory as ``path`` so ``os.replace`` stays atomic across
    filesystem boundaries. Parent directory is created if it does not
    exist (mirrors the executor's expectation that the output dir is
    materialized before the first wave write).
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    data = content.encode("utf-8")
    fd, tmp_name = tempfile.mkstemp(
        prefix=path.name + ".",
        suffix=".tmp",
        dir=str(path.parent),
    )
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, str(path))
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise
    return len(data)


def _read_raw(worker: WorkerResult) -> str:
    """Resolve a worker's raw body for the recipe call.

    Two source paths, in priority order:

    1. ``worker.body`` -- the in-memory raw body the transport stashes
       on the WorkerResult (mirrors :mod:`transports.stub` /
       :mod:`transports.openai_compat`). Preferred because it avoids
       a round-trip through disk when the dispatcher hands the
       results straight to normalize_wave2.
    2. ``worker.raw_path`` -- the on-disk raw file the dispatcher
       materialized. Used when normalize is invoked standalone (e.g.
       M6 resume reads from disk because the in-memory body was lost
       to the prior process).

    Returns an empty string when neither source is available so the
    recipe sees a stable shape; the recipe is responsible for the
    empty-body branch.
    """
    body = getattr(worker, "body", None)
    if isinstance(body, str):
        return body
    if worker.raw_path:
        try:
            return Path(worker.raw_path).read_text(encoding="utf-8")
        except OSError:
            return ""
    return ""


def _emit_meta(
    meta_path: Path,
    *,
    recipe_name: str,
    schema_version: str,
    salvaged: bool,
    status: str,
    error: Optional[str],
    bytes_written: int,
    salvage_reason: Optional[str] = None,
) -> None:
    """Atomically emit the per-worker meta sidecar (``*.meta.json``).

    Fields recorded (FR-027 / INV-016 surface alignment):

    * ``recipe`` -- the recipe name resolved from
      :data:`NormalizationSpec.recipe`.
    * ``schema_version`` -- the normalize schema version (defaults to
      ``"1.0"`` per §4.1 spec block). Mirrors
      :attr:`NormalizationSpec.schema_version`.
    * ``salvaged`` -- §7.4 salvage flag. ``True`` when the dispatcher
      promoted ``parse_error -> success`` based on the recipe's
      salvage signal (full conditions in :func:`salvage_decision`).
    * ``status`` -- the post-normalize status. Mirrors the returned
      WorkerResult's ``status`` so a caller reading only the sidecar
      sees the same terminal classification.
    * ``error`` -- optional recipe-exception message; omitted when
      normalization succeeded cleanly.
    * ``bytes`` -- byte count written to ``final_path``; 0 when
      normalization produced no body (e.g. hard-failure branches).
    * ``salvage_reason`` -- §7.4 stable token (one of the ``SALVAGE_*``
      constants) recording which branch fired. Present on every
      sidecar where a recipe ran (success / parse_error / salvage),
      omitted on hard-failure short-circuits where the recipe was
      never invoked.
    """
    payload: dict[str, Any] = {
        "recipe": recipe_name,
        "schema_version": schema_version,
        "salvaged": salvaged,
        "status": status,
        "bytes": bytes_written,
    }
    if error:
        payload["error"] = error
    if salvage_reason is not None:
        payload["salvage_reason"] = salvage_reason
    _atomic_write_text(
        meta_path,
        json.dumps(payload, sort_keys=True, indent=2) + "\n",
    )


def _normalize_one(
    worker: WorkerResult,
    recipe: Recipe,
    recipe_name: str,
    args: dict[str, Any],
    schema_version: str,
    *,
    salvage_enabled: bool = True,
) -> WorkerResult:
    """Apply ``recipe`` to a single worker; return a new WorkerResult.

    Hard-failure branches (``timeout`` / ``proxy_error``) skip
    normalization but still emit the meta sidecar so M5 / M6 surfaces
    can iterate sidecars uniformly. The success/parse_error branches
    invoke the recipe; an exception raised by the recipe downgrades
    the worker to ``parse_error`` with the exception message recorded
    on the sidecar. The §7.4 salvage promotion is delegated to
    :func:`salvage_parse_error` / :func:`salvage_decision`; ``salvage_enabled``
    mirrors :attr:`NormalizationSpec.on_parse_error.salvage`.
    """
    meta_path = Path(worker.meta_path) if worker.meta_path else None

    # Hard-failure short-circuit -- no body to normalize, no final
    # file to write. Sidecar still emitted (uniform surface). No
    # salvage_reason recorded -- the recipe never ran, so the §7.4
    # branch cannot be classified.
    if worker.status in {"timeout", "proxy_error"}:
        if meta_path is not None:
            _emit_meta(
                meta_path,
                recipe_name=recipe_name,
                schema_version=schema_version,
                salvaged=False,
                status=worker.status,
                error=None,
                bytes_written=0,
            )
        return dataclasses.replace(worker)

    raw = _read_raw(worker)

    try:
        result = recipe.normalize(raw, args)
    except Exception as exc:  # noqa: BLE001 -- intentional broad catch
        # Recipe raised -- treat as a non-salvageable parse_error.
        # The synthesized NormalizedResult has salvaged=False so
        # salvage_decision will reject with
        # "rejected_no_recipe_signal", recorded on the sidecar.
        error = f"{type(exc).__name__}: {exc}"
        synthetic = NormalizedResult(text="", salvaged=False, error=error)
        downgraded = dataclasses.replace(worker, status="parse_error", bytes=0)
        decision = salvage_decision(
            downgraded,
            normalized=synthetic,
            salvage_enabled=salvage_enabled,
        )
        if meta_path is not None:
            _emit_meta(
                meta_path,
                recipe_name=recipe_name,
                schema_version=schema_version,
                salvaged=False,
                status="parse_error",
                error=error,
                bytes_written=0,
                salvage_reason=decision.reason,
            )
        return downgraded

    # §7.4 salvage promotion -- conditions centralized in
    # salvage_decision / salvage_parse_error so the WorkerResult and
    # the meta sidecar agree on both the outcome and the reason.
    decision = salvage_decision(
        worker,
        normalized=result,
        salvage_enabled=salvage_enabled,
    )
    promoted = salvage_parse_error(
        worker,
        normalized=result,
        salvage_enabled=salvage_enabled,
    )

    bytes_written = 0
    if worker.final_path and result.text:
        bytes_written = _atomic_write_text(Path(worker.final_path), result.text)

    if meta_path is not None:
        _emit_meta(
            meta_path,
            recipe_name=recipe_name,
            schema_version=schema_version,
            salvaged=bool(result.salvaged),
            status=promoted.status,
            error=result.error,
            bytes_written=bytes_written,
            salvage_reason=decision.reason,
        )

    return dataclasses.replace(promoted, bytes=bytes_written)


def normalize_wave2(
    worker_results: list[WorkerResult],
    recipe_name: str,
    *,
    schema_version: str = "1.0",
    recipe_args: Optional[dict[str, Any]] = None,
    salvage_enabled: bool = True,
) -> list[WorkerResult]:
    """Apply ``recipe_name`` to every worker; return a new result list.

    Args:
        worker_results: the list returned by
            :func:`superclaude.cli.swarm.dispatch.dispatch_wave1`.
            Each entry MUST carry ``meta_path`` and ``final_path``
            populated by the dispatcher so the sidecar emission and
            atomic write have stable targets.
        recipe_name: the recipe key resolved from
            :class:`NormalizationSpec.recipe`. Looked up in
            :data:`recipes.REGISTRY`. Unknown names raise ``KeyError``
            (lens validator drift -- should have been caught at
            preflight per FR-LENSREG.NS / U-008). Sentinel ``None``
            entries (pre-T04.03..T04.09) fall back to passthrough.
        schema_version: the normalize schema version recorded on each
            meta sidecar. Defaults to ``"1.0"`` per §4.1 spec block;
            mirrors :attr:`NormalizationSpec.schema_version` so the
            sidecar agrees with the JobSpec value.
        recipe_args: optional kwargs forwarded verbatim to every
            recipe call. Recipe-specific shape; AC-011 forbids any
            scoring / dedup / reorder semantics. Defaults to ``{}``.
        salvage_enabled: §7.4 ``parse_error -> success`` salvage
            policy gate (FR-028). Mirrors
            :attr:`NormalizationSpec.on_parse_error.salvage`. Default
            ``True`` to preserve the spec's default-on policy. When
            ``False`` no worker is ever promoted -- the dispatcher
            still calls the recipe and records ``salvaged`` on the
            sidecar, but the status stays ``parse_error`` and the
            sidecar's ``salvage_reason`` is
            ``"rejected_salvage_disabled"``.

    Returns:
        A new ``list[WorkerResult]`` with the same length and order as
        ``worker_results``. Each entry is a fresh dataclass
        (``dataclasses.replace``); the input list is not mutated.
        ``status`` is updated only on the salvage-promotion or
        recipe-exception branches; ``bytes`` reflects the
        ``final_path`` payload (0 on hard-failure branches).
    """
    recipe = _resolve_recipe(recipe_name)
    args = recipe_args or {}
    return [
        _normalize_one(
            worker,
            recipe,
            recipe_name,
            args,
            schema_version,
            salvage_enabled=salvage_enabled,
        )
        for worker in worker_results
    ]
