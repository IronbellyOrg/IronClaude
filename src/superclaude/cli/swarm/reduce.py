"""T05.01 -- COMP-009 Wave 3 reduce dispatcher.

``reduce_wave3`` is the single Wave-3 entrypoint. It receives the
``WorkerResult`` list returned by Wave-2 normalize (COMP-008,
:mod:`superclaude.cli.swarm.normalize`), the
:data:`AmalgamationMode`, and the ambient job context (status policy,
caller identity, lens, target snapshot, recommended-next-command
template + substitutions), and returns the :class:`ResultContract`
(DM-012) that the executor hands back to the caller per FR-018.

Contract surface (FR-018 / IMM-5 / AC-011)
==========================================

The reduce wave does **three** things, in this order:

1. **Status determination (IMM-5).** :func:`determine_status` reads the
   :class:`StatusPolicy` (DM-008) and the (M, N) tuple computed from
   ``worker_results`` / ``workers_requested`` and classifies the run as
   ``success`` / ``partial`` / ``failed`` per the IMM-5 truth table:

   ============  ========  ==================================
   M == N        success   (no failed slot)
   2 <= M < N    partial   (above policy.floor, below N)
   M < 2         failed    (below policy.floor)
   M == N == 2   success   (success_first tie-break; default)
   ============  ========  ==================================

   T05.03 lands the parametrized matrix test; the function lives here
   so the reduce orchestrator can route the result into the contract
   without a cross-module dance.

2. **Mode dispatch.** :func:`select_mode` returns the per-mode
   reducer that turns the worker list into a ``Optional[str]``
   merged-body. The three :data:`AmalgamationMode` values map to:

   - ``raw``              -- no merge, no merged_path (every worker's
                             ``raw_path`` is the per-worker artifact).
   - ``normalize``        -- no merge, no merged_path (every worker's
                             ``final_path`` is the per-worker artifact).
   - ``normalize+merge``  -- invoke the merge module
                             (:mod:`superclaude.cli.swarm.merge`,
                             T05.02 / COMP-010) to produce ``merged.md``;
                             ``contract.merged_path`` points at it.

   T05.04 lands the dispatch-table parametrization; the helper lives
   here so the reduce orchestrator can call it without an extra import.

3. **Contract emission (FR-018).** :func:`emit_contract` writes the
   final :class:`ResultContract` to ``return-contract.yaml`` via
   write-to-tmp + ``os.replace`` (IMM-6 / NFR-002). Emission is gated
   on status determination -- the contract is only built after IMM-5
   stamps ``status``, ``workers_succeeded``, ``workers_failed``,
   ``output_files``, and ``merged_path``. T05.07 lands the DM-012
   field-completeness test against the schema surface; the YAML
   emitter lives here so the orchestrator owns one round-trip from
   inputs to on-disk contract.

Merge trigger (FR-012 / AC-012)
================================

When ``mode == "normalize+merge"`` AND M >= ``policy.floor`` (the
mechanical-merge gate -- merging a single worker's body or zero
workers' bodies has no semantic value), the orchestrator invokes the
merge callable. The default callable lazy-imports
:func:`superclaude.cli.swarm.merge.mechanical_merge` so reduce can
land ahead of the merge module's body (T05.02 follows immediately).
Tests inject ``merge_callable=...`` to exercise the trigger surface
without depending on the merge module's concrete output.

The merge module owns the AC-012 boundary: concat sections in slot-
index order, prepend ``## From {model_label} ({elapsed_ms}ms)``, no
sort / score / dedupe / filter / rewrite. ``reduce_wave3`` itself
**never** touches body bytes -- it only writes the merge's return
value to ``output_dir / 'merged.md'`` atomically and records the
path on the contract. AC-011 / AC-012 forbid any judging transform
on this path.

Atomic + confined writes (NFR-002 / NFR-013)
=============================================

Every disk write in reduce -- ``merged.md`` and ``return-contract.yaml``
-- routes through :func:`_atomic_write_bytes`, the same tmp-file + fsync
+ ``os.replace`` shape :mod:`superclaude.cli.swarm.normalize` uses.
Both files land under the caller-supplied ``output_dir`` (NFR-013
path confinement); reduce never escapes that directory.

Default-stub friendliness
=========================

Every parameter except ``worker_results`` is optional. With no extras
the orchestrator produces a minimal but legal :class:`ResultContract`
(empty caller / target / artifacts records, status determined from
the list alone, no on-disk emission when ``output_dir`` is None). This
lets ``tests/swarm/test_reduce.py`` exercise every mode without
materializing a JobSpec, while the M5 executor wiring (later phases)
threads the full context through.
"""

from __future__ import annotations

import json
import os
import tempfile
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Optional

import yaml

from superclaude.cli.swarm.models import (
    AmalgamationMode,
    Artifacts,
    CallerInfo,
    CallerMetadata,
    ContractTarget,
    DoneSentinel,
    ResultContract,
    ResultStatus,
    StatusPolicy,
    WorkerResult,
    to_dict,
)

__all__ = [
    "MergeCallable",
    "determine_status",
    "emit_contract",
    "emit_done_sentinel",
    "reduce_wave3",
    "regenerate_merge_on_resume",
    "select_mode",
]


# Default file names for reduce-emitted artifacts. Kept module-level so
# the M5 executor and the T05.07 contract-emission test can pin the
# exact landing paths without re-deriving them from the orchestrator.
MERGED_FILENAME = "merged.md"
CONTRACT_FILENAME = "return-contract.yaml"
DONE_SENTINEL_FILENAME = "done.json"


MergeCallable = Callable[[list[WorkerResult]], str]
"""Signature the merge module (T05.02 / COMP-010) implements.

``mechanical_merge(worker_results) -> str`` returns the concatenated
body (provenance header per section + verbatim concat in slot-index
order). The merge module owns the AC-012 boundary; ``reduce_wave3``
only consumes the returned string and writes it to disk.
"""


# ---------------------------------------------------------------------------
# Status determination -- IMM-5 success-first matrix (T05.03 surface).
# ---------------------------------------------------------------------------


def determine_status(
    workers_succeeded: int,
    workers_requested: int,
    policy: Optional[StatusPolicy] = None,
) -> ResultStatus:
    """Classify the run per the IMM-5 status truth table.

    The full matrix lives in the module docstring; this function is
    the canonical implementation called by :func:`reduce_wave3` and
    parametrized by ``tests/swarm/test_imm5_status.py`` (T05.03).

    Args:
        workers_succeeded: M -- number of workers whose
            :attr:`WorkerResult.status` ended at ``success``
            (post-salvage promotion per §7.4).
        workers_requested: N -- number of workers requested by the
            preflight manifest. Equal to
            :attr:`Manifest.preflight.workers_requested`.
        policy: optional :class:`StatusPolicy`. Defaults to the
            IMM-5 surface (``floor=2``, ``success_first=True``,
            ``partial_threshold=2``).

    Returns:
        One of :data:`ResultStatus` -- ``success`` / ``partial`` /
        ``failed``. Edge cases:

        - ``workers_requested == 0`` -> ``failed`` (no slots to grade;
          M is necessarily < floor).
        - ``workers_succeeded > workers_requested`` -- invariant
          violation; treated as ``success`` (the IMM-5 floor / partial
          rules cannot fire when M >= N).
        - ``workers_succeeded < 0`` or ``workers_requested < 0`` --
          callers' problem; we clamp at zero before applying the
          matrix so the function stays total.
    """
    effective_policy = policy if policy is not None else StatusPolicy()
    # Lowercase mirrors of the IMM-5 (M, N) tuple; the matrix docstring
    # uses M/N for spec parity, but the local names stay PEP-8 lower.
    m = max(0, int(workers_succeeded))
    n = max(0, int(workers_requested))
    floor = effective_policy.floor
    success_first = effective_policy.success_first
    partial_threshold = effective_policy.partial_threshold

    # IMM-5 success-first tie-break: M == N == 2 resolves to success
    # when the policy carries success_first=True. Evaluated first so
    # the partial-window check below never claims this slot.
    if success_first and m == n == 2:
        return "success"
    # M == N (and M > 0) -- every requested slot succeeded.
    if m >= n and n > 0:
        return "success"
    # partial window: floor <= M < N. partial_threshold mirrors floor
    # by default but is exposed so callers can widen the failed/partial
    # boundary independently.
    if m >= max(floor, partial_threshold) and m < n:
        return "partial"
    # Below floor -- failed regardless of N.
    return "failed"


# ---------------------------------------------------------------------------
# Mode dispatch -- (T05.04 surface).
# ---------------------------------------------------------------------------


def _reducer_raw(
    worker_results: list[WorkerResult],
    *,
    merge_callable: Optional[MergeCallable],
    workers_succeeded: int,
    policy: StatusPolicy,
) -> Optional[str]:
    """``raw`` mode -- no merge; merged_path stays None."""
    del worker_results, merge_callable, workers_succeeded, policy
    return None


def _reducer_normalize(
    worker_results: list[WorkerResult],
    *,
    merge_callable: Optional[MergeCallable],
    workers_succeeded: int,
    policy: StatusPolicy,
) -> Optional[str]:
    """``normalize`` mode -- no merge; each worker's final_path is the artifact."""
    del worker_results, merge_callable, workers_succeeded, policy
    return None


def _reducer_normalize_merge(
    worker_results: list[WorkerResult],
    *,
    merge_callable: Optional[MergeCallable],
    workers_succeeded: int,
    policy: StatusPolicy,
) -> Optional[str]:
    """``normalize+merge`` mode -- invoke the merge module when M >= floor.

    The gate (``workers_succeeded >= policy.floor``) mirrors the §5
    spec's "merged_path is null when workers_succeeded < 2" rule: a
    single body's concat with itself has no semantic value, and zero
    bodies have nothing to concat. When the gate fails the orchestrator
    leaves ``merged_path`` as None and the merged file is not written.
    """
    if workers_succeeded < policy.floor:
        return None
    callable_ = merge_callable if merge_callable is not None else _default_merge
    return callable_(list(worker_results))


_MODE_DISPATCH: dict[AmalgamationMode, Callable[..., Optional[str]]] = {
    "raw": _reducer_raw,
    "normalize": _reducer_normalize,
    "normalize+merge": _reducer_normalize_merge,
}


def select_mode(mode: AmalgamationMode) -> Callable[..., Optional[str]]:
    """Return the per-mode reducer callable for ``mode``.

    T05.04 / FR-011 dispatch table. The returned callable has the
    signature::

        (worker_results, *, merge_callable, workers_succeeded, policy) -> Optional[str]

    and returns the merged-body string (``normalize+merge`` mode when
    ``workers_succeeded >= policy.floor``) or ``None`` (every other
    case). The orchestrator (:func:`reduce_wave3`) is the canonical
    caller; tests exercise this surface directly to verify each mode
    produces the expected artifact set:

    - ``raw``              -> no merge, no ``merged.md``. Per-worker
                              ``raw_path`` is the artifact.
    - ``normalize``        -> no merge, no ``merged.md``. Per-worker
                              ``final_path`` is the artifact.
    - ``normalize+merge``  -> invoke the merge module to produce
                              ``merged.md``; per-worker ``final_path``
                              files remain on disk.

    Unknown modes raise :class:`ValueError` listing the accepted set.
    """
    if mode not in _MODE_DISPATCH:
        raise ValueError(
            f"amalgamation_mode must be one of {sorted(_MODE_DISPATCH)}, got {mode!r}"
        )
    return _MODE_DISPATCH[mode]


# Module-private alias preserved for callers that imported the
# underscore-prefixed name before the T05.04 deliverable surfaced the
# public dispatch helper. The orchestrator uses the public name below.
_select_mode = select_mode


def _default_merge(worker_results: list[WorkerResult]) -> str:
    """Lazy-import :func:`superclaude.cli.swarm.merge.mechanical_merge`.

    The merge module (T05.02 / COMP-010) lands in the same phase as
    reduce; deferring the import to call time lets reduce land first
    without a hard import dependency. The ImportError surface is
    intentional -- callers in modes that don't need merge (raw /
    normalize) never trigger the lazy import; only ``normalize+merge``
    callers see it, and by the time M5 wires real runs the merge
    module exists.
    """
    from superclaude.cli.swarm.merge import mechanical_merge

    return mechanical_merge(worker_results)


# ---------------------------------------------------------------------------
# Atomic write helper -- mirrors normalize._atomic_write_text.
# ---------------------------------------------------------------------------


def _atomic_write_bytes(path: Path, data: bytes) -> int:
    """Write ``data`` to ``path`` via tmp file + ``os.replace`` (IMM-6).

    Same shape as :func:`superclaude.cli.swarm.normalize._atomic_write_text`
    but bytes-typed because the YAML emitter feeds us pre-encoded
    payload. Parent directory is created if missing (mirrors the
    executor's contract that the output dir is materialized at preflight).
    """
    path.parent.mkdir(parents=True, exist_ok=True)
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


# ---------------------------------------------------------------------------
# Contract emission -- (T05.07 surface).
# ---------------------------------------------------------------------------


def emit_contract(contract: ResultContract, output_dir: Path) -> Path:
    """Atomically write ``contract`` to ``output_dir / return-contract.yaml``.

    The YAML payload routes through :func:`superclaude.cli.swarm.models.to_dict`
    (which recurses into nested dataclasses + ``list[<dataclass>]``)
    and ``yaml.safe_dump`` with ``sort_keys=False`` so the on-disk
    order mirrors the DM-012 declaration order callers parse against.

    T05.07 lands the DM-012 field-completeness test; this emitter is
    deliberately thin so that test pins the contract surface rather
    than emitter-specific serialization quirks.

    Args:
        contract: the :class:`ResultContract` to serialize.
        output_dir: the caller-supplied output root (NFR-013 path
            confinement). The file lands at
            ``output_dir / 'return-contract.yaml'``.

    Returns:
        The absolute :class:`Path` to the emitted contract.
    """
    target = Path(output_dir) / CONTRACT_FILENAME
    payload = to_dict(contract)
    body = yaml.safe_dump(payload, sort_keys=False, allow_unicode=True)
    _atomic_write_bytes(target, body.encode("utf-8"))
    return target


# ---------------------------------------------------------------------------
# Done sentinel emission -- T07.13 / FR-027 / DM-017.
# ---------------------------------------------------------------------------


def emit_done_sentinel(
    terminal_status: ResultStatus,
    contract_path: Path | str,
) -> Path:
    """Atomically write ``done.json`` next to the result contract.

    DM-017 fixes the sentinel as a 3-field record (``atomic_write``,
    ``terminal_status``, ``contract_path``) written verbatim after
    :class:`SwarmState.state` flips to ``terminal``. FR-027 / FR-029 /
    FR-014 require the sentinel so detached / tmux callers can poll a
    single file (``until [ -f done.json ]``) without parsing the
    contract or attaching to the executor process.

    The function is intentionally narrow:

      * **Co-located.** The sentinel lands in ``contract_path.parent`` so
        ``done.json`` and ``return-contract.yaml`` share an output dir;
        the caller never has to thread two paths through the executor.
      * **Atomic.** The write routes through :func:`_atomic_write_bytes`
        (tmp file + ``fsync`` + ``os.replace``) so a mid-write SIGKILL
        leaves either no file or the prior file -- never a half-written
        sentinel that an ``until [ -f done.json ]`` poll would treat as
        complete (IMM-6 / NFR-002).
      * **DoneSentinel-validated.** The payload is built through the
        :class:`DoneSentinel` dataclass so its ``__post_init__`` rejects
        out-of-enum ``terminal_status`` values before the bytes hit
        disk. The kill path (``commands._emit_killed_done_sentinel``)
        bypasses the dataclass because ``"killed"`` is intentionally not
        in :data:`ResultStatus`; the IMM-5 reduce path lands here and
        every legal value (``success`` / ``partial`` / ``failed``) flows
        through the dataclass guard.
      * **JSON-shaped.** :func:`to_dict` is a thin ``dataclasses.asdict``
        wrapper; ``json.dumps(..., sort_keys=True, indent=2)`` mirrors
        the kill writer's on-disk shape so both flavours parse uniformly.

    Args:
        terminal_status: the IMM-5 verdict (``success`` / ``partial`` /
            ``failed``). Same value
            :attr:`ResultContract.status` carries.
        contract_path: absolute path the executor emitted
            ``return-contract.yaml`` to. The sentinel is written to
            ``Path(contract_path).parent / "done.json"`` and the
            stringified ``contract_path`` is stamped onto the sentinel
            so consumers can locate the rich record from the marker.

    Returns:
        Absolute :class:`Path` to the emitted ``done.json``.
    """
    contract = Path(contract_path)
    sentinel = DoneSentinel(
        atomic_write=True,
        terminal_status=terminal_status,
        contract_path=str(contract),
    )
    target = contract.parent / DONE_SENTINEL_FILENAME
    body = json.dumps(to_dict(sentinel), sort_keys=True, indent=2) + "\n"
    _atomic_write_bytes(target, body.encode("utf-8"))
    return target


# ---------------------------------------------------------------------------
# Recommended-next-command rendering (FR-018 / DM-012).
# ---------------------------------------------------------------------------


def _render_recommended_next_command(
    template: str, substitutions: Mapping[str, str]
) -> str:
    """Apply ``substitutions`` to ``template`` via ``str.format_map``.

    The DM-012 contract carries the *rendered* command string (in
    contrast to JobSpec's unrendered template). The renderer uses
    ``str.format_map`` with a defaultdict so missing placeholders
    pass through unchanged rather than raising -- callers that want
    strict missing-key detection layer that check at preflight (M2
    schema layer), not here.
    """
    if not template:
        return ""

    class _Defaults(dict):
        def __missing__(self, key: str) -> str:  # type: ignore[override]
            return "{" + key + "}"

    return template.format_map(_Defaults(substitutions))


# ---------------------------------------------------------------------------
# Resume merge regeneration -- T06.02 / INV-010.
# ---------------------------------------------------------------------------


def regenerate_merge_on_resume(
    output_dir: Path, mode: AmalgamationMode
) -> Optional[Path]:
    """INV-010 -- delete a stale ``merged.md`` so resume rewrites it.

    The acceptance contract (phase-6-tasklist §T06.02 / roadmap row
    R-111) requires that, when a job is resumed under
    ``amalgamation_mode == "normalize+merge"``, the orchestrator never
    keep a ``merged.md`` produced by the previous (possibly crashed
    mid-merge) run. The merged body is a pure function of the
    re-dispatched workers' ``final_path`` contents and provenance
    headers; persisting the old file across a resume would leak the
    pre-crash worker set (or, worse, a half-written byte block from
    the kill that interrupted the previous write) into the resumed
    contract.

    The helper is intentionally narrow:

        * Mode-guarded -- ``raw`` / ``normalize`` never write
          ``merged.md`` so deletion is a no-op for those modes. The
          guard keeps the helper safe to call unconditionally from the
          resume orchestrator without branching on mode.
        * Idempotent -- a missing ``merged.md`` is not an error; the
          first resume after a clean preflight (no merge yet written)
          and every subsequent resume both succeed.
        * Filesystem-only -- the helper does **not** invoke the merge
          callable. Regeneration happens on the next
          :func:`reduce_wave3` call (the resume orchestrator runs Wave
          2 normalize → Wave 3 reduce), at which point the merge
          dispatch writes a fresh body atomically via
          :func:`_atomic_write_bytes`.

    Args:
        output_dir: the job's output root (the same path the original
            run's :func:`reduce_wave3` wrote to). Resolved through
            :class:`pathlib.Path` to accept ``str`` / ``os.PathLike``
            callers.
        mode: the :data:`AmalgamationMode` from the manifest. Only
            ``"normalize+merge"`` triggers the deletion.

    Returns:
        The :class:`Path` of the stale file when it existed and was
        deleted (so the resume orchestrator can log the cleanup);
        ``None`` when the file did not exist or when ``mode`` was not
        ``"normalize+merge"``.
    """
    if mode != "normalize+merge":
        return None
    stale = Path(output_dir) / MERGED_FILENAME
    try:
        stale.unlink()
    except FileNotFoundError:
        return None
    return stale


# ---------------------------------------------------------------------------
# Orchestrator -- the public Wave-3 entrypoint.
# ---------------------------------------------------------------------------


def reduce_wave3(
    worker_results: list[WorkerResult],
    mode: AmalgamationMode = "normalize+merge",
    *,
    output_dir: Optional[Path] = None,
    workers_requested: Optional[int] = None,
    status_policy: Optional[StatusPolicy] = None,
    job_id: str = "",
    started: str = "",
    finished: str = "",
    elapsed_ms: int = 0,
    caller: Optional[CallerInfo] = None,
    caller_metadata: Optional[CallerMetadata] = None,
    lens: str = "",
    lens_source: str = "",
    target: Optional[ContractTarget] = None,
    artifacts: Optional[Artifacts] = None,
    recommended_next_command_template: str = "",
    recommended_next_command_substitutions: Optional[Mapping[str, str]] = None,
    merge_callable: Optional[MergeCallable] = None,
    emit_to_disk: Optional[bool] = None,
    resume: bool = False,
) -> ResultContract:
    """Compute status, trigger merge, emit the final :class:`ResultContract`.

    The orchestrator runs the three reduce steps -- status, merge,
    contract -- in order. Contract emission is gated on status
    determination: the contract is constructed only after IMM-5
    stamps ``status`` so the on-disk artefact never reflects a
    pre-classification snapshot.

    Args:
        worker_results: the post-Wave-2 list returned by
            :func:`superclaude.cli.swarm.normalize.normalize_wave2`.
            Each entry's ``status`` is read for M-counting; ``index``
            ordering is preserved into ``contract.output_files``.
        mode: the :data:`AmalgamationMode`. Defaults to
            ``"normalize+merge"`` mirroring :class:`JobSpec`.
        output_dir: caller-supplied output root (NFR-013). When
            supplied, ``merged.md`` and ``return-contract.yaml`` land
            under this path. When ``None`` the orchestrator skips all
            disk writes and returns the contract instance only -- this
            is the path tests use to exercise mode dispatch without
            materializing files.
        workers_requested: N for the IMM-5 matrix. Defaults to
            ``len(worker_results)`` so callers that hand reduce a
            complete list get the natural N. Real M5 wiring passes
            the preflight-recorded value so retried slots count
            against the original N.
        status_policy: :class:`StatusPolicy`; defaults to the IMM-5
            surface (``floor=2``, ``success_first=True``,
            ``partial_threshold=2``).
        job_id, started, finished, elapsed_ms: standard contract
            timestamps + identifier; empty / zero defaults satisfy
            the no-arg test path while real wiring threads them
            through.
        caller, caller_metadata, lens, lens_source, target, artifacts:
            ambient context copied verbatim onto the contract. Empty
            defaults satisfy the no-arg path.
        recommended_next_command_template,
            recommended_next_command_substitutions: rendered via
            :func:`_render_recommended_next_command` and stamped on
            ``contract.recommended_next_command``.
        merge_callable: optional override for the merge module entry
            point. Defaults to lazy import of
            :func:`superclaude.cli.swarm.merge.mechanical_merge`.
            Tests inject a stub to verify the trigger surface in
            isolation from the merge module's body.
        emit_to_disk: opt-in / opt-out for disk emission. Defaults
            to ``True`` when ``output_dir`` is supplied, ``False``
            otherwise. Explicit ``False`` even with ``output_dir`` set
            skips both the merged.md write and the contract write
            (orchestrator returns the dataclass only).
        resume: T06.02 / INV-010 resume hook. When ``True`` AND
            ``mode == "normalize+merge"`` AND ``output_dir`` is
            supplied, any pre-existing ``merged.md`` under
            ``output_dir`` is deleted before merge dispatch via
            :func:`regenerate_merge_on_resume`. This guarantees a
            stale or partially-written merge from the previous run
            never persists across a resume: the merge dispatch below
            then writes a fresh body (when M >= floor) or leaves the
            slot empty (when M < floor). No-op for ``raw`` /
            ``normalize`` modes -- those modes never write
            ``merged.md`` so there is nothing to clean.

    Returns:
        The :class:`ResultContract` with every DM-012 field stamped.
        ``merged_path`` is populated only when ``mode == "normalize+merge"``,
        M >= ``policy.floor``, and ``output_dir`` is non-None.
    """
    effective_policy = status_policy if status_policy is not None else StatusPolicy()

    # Step 1 -- M / N counts and IMM-5 status determination.
    workers_succeeded = sum(1 for w in worker_results if w.status == "success")
    workers_failed = sum(1 for w in worker_results if w.status != "success")
    effective_n = (
        int(workers_requested) if workers_requested is not None else len(worker_results)
    )
    status = determine_status(
        workers_succeeded=workers_succeeded,
        workers_requested=effective_n,
        policy=effective_policy,
    )

    # Step 2 -- mode dispatch + merge trigger.
    reducer = select_mode(mode)
    merged_body = reducer(
        worker_results,
        merge_callable=merge_callable,
        workers_succeeded=workers_succeeded,
        policy=effective_policy,
    )

    # Resolve disk-emission policy: explicit override wins; otherwise
    # derive from output_dir presence.
    should_emit = emit_to_disk if emit_to_disk is not None else output_dir is not None

    # T06.02 / INV-010 -- resume hook. When resuming a job that ran
    # under normalize+merge, drop any stale merged.md from the previous
    # run so a kill-mid-merge crash never leaves a half-written body on
    # disk competing with the about-to-be-regenerated one. The deletion
    # is unconditional once mode == "normalize+merge" (the helper
    # guards the no-op case for raw / normalize). The fresh write
    # happens below via _atomic_write_bytes when M >= floor.
    if resume and output_dir is not None and should_emit:
        regenerate_merge_on_resume(Path(output_dir), mode)

    merged_path: Optional[str] = None
    if merged_body is not None and output_dir is not None and should_emit:
        merged_target = Path(output_dir) / MERGED_FILENAME
        _atomic_write_bytes(merged_target, merged_body.encode("utf-8"))
        merged_path = str(merged_target)

    # Step 3 -- assemble the contract. Stamped *after* status so
    # emission is gated behind classification (acceptance criterion:
    # "Contract emission gated behind status determination").
    rendered_next = _render_recommended_next_command(
        recommended_next_command_template,
        recommended_next_command_substitutions or {},
    )

    contract = ResultContract(
        contract_version="1.0",
        status=status,
        job_id=job_id,
        started=started,
        finished=finished,
        elapsed_ms=elapsed_ms,
        caller=caller if caller is not None else CallerInfo(),
        lens=lens,
        lens_source=lens_source,
        target=target if target is not None else ContractTarget(),
        workers_requested=effective_n,
        workers_succeeded=workers_succeeded,
        workers_failed=workers_failed,
        output_files=list(worker_results),
        amalgamation_mode=mode,
        merged_path=merged_path,
        caller_metadata=caller_metadata
        if caller_metadata is not None
        else CallerMetadata(),
        recommended_next_command=rendered_next,
        artifacts=artifacts if artifacts is not None else Artifacts(),
    )

    if should_emit and output_dir is not None:
        emit_contract(contract, Path(output_dir))

    return contract
