"""T06.02 -- INV-010 resume regenerates ``merged.md`` unconditionally.

Pins the resume-hook contract on
:func:`superclaude.cli.swarm.reduce.reduce_wave3` (and the standalone
:func:`superclaude.cli.swarm.reduce.regenerate_merge_on_resume`
helper). Roadmap row R-111 (INV-010) requires that when a swarm job
is resumed under ``amalgamation_mode == "normalize+merge"``, the
orchestrator never preserves a ``merged.md`` produced by the prior
(possibly crashed mid-merge) run -- the file is deleted before merge
dispatch, and the next reduce call writes a fresh body (when
M >= floor) or leaves no merged.md at all (when M < floor).

The acceptance contract this module pins (phase-6-tasklist.md §T06.02):

    * **Stale merge never persists post-resume** -- a pre-existing
      ``merged.md`` under ``output_dir`` is deleted before regen.
    * **Provenance header reflects re-dispatch elapsed_ms** -- the
      regenerated body carries the *current* worker_results'
      ``model_label`` / ``elapsed_ms`` values, not the stale ones.
    * **Regen unconditional when mode == "normalize+merge"** -- the
      hook fires even if M < floor (no replacement body is written,
      but the stale file is still removed).
    * **No-op for raw / normalize modes** -- those modes never write
      ``merged.md`` so the hook does nothing.
    * **Pre/post-resume ``merged.md`` differs when workers re-dispatched**
      -- the byte-level comparison shows divergence so a caller diffing
      the files sees the re-dispatch landed.

The hook is exercised through two surfaces:

    1. The standalone :func:`regenerate_merge_on_resume` helper --
       deterministic, filesystem-only, returns the deleted path for
       logging.
    2. The :func:`reduce_wave3` ``resume=True`` parameter -- the
       integration surface the M6 resume orchestrator (T06.04) calls
       to fold cleanup + Wave 3 + contract emission into one pass.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable

import pytest

# INV-010 resume merge regen (T08.03 / NFR-007). Module-level marker so
# every test in this file is selected by ``pytest -m inv``.
pytestmark = pytest.mark.inv

from superclaude.cli.swarm.models import StatusPolicy, WorkerResult
from superclaude.cli.swarm.reduce import (
    CONTRACT_FILENAME,
    MERGED_FILENAME,
    reduce_wave3,
    regenerate_merge_on_resume,
)


# ---------------------------------------------------------------------------
# Fixture helpers -- mirror tests/swarm/test_reduce.py builders so the
# resume tests stay structurally aligned with the baseline Wave 3 suite.
# ---------------------------------------------------------------------------


def _worker(
    index: int,
    *,
    status: str = "success",
    model_label: str = "stub-model",
    elapsed_ms: int = 100,
) -> WorkerResult:
    return WorkerResult(
        index=index,
        path=f"worker-{index:02d}.md",
        raw_path=f"worker-{index:02d}.raw.md",
        meta_path=f"worker-{index:02d}.meta.json",
        final_path=f"worker-{index:02d}.final.md",
        model_id=f"model-{index}",
        model_label=model_label,
        bytes=0,
        status=status,  # type: ignore[arg-type]
        attempts=1,
        elapsed_ms=elapsed_ms,
    )


def _labeled_merge() -> Callable[[list[WorkerResult]], str]:
    """Merge stub that stamps per-worker provenance headers in the body.

    The body shape mirrors the mechanical merge contract (AC-012):
    ``## From {model_label} ({elapsed_ms}ms)`` per section, slot-index
    ordering. Using model_label + elapsed_ms in the body lets the
    resume tests assert byte-level provenance changes between
    pre-resume and post-resume runs without depending on the real
    merge module's file-read path.
    """

    def _merge(workers: list[WorkerResult]) -> str:
        sections = []
        for w in workers:
            sections.append(
                f"## From {w.model_label} ({w.elapsed_ms}ms)\n\n"
                f"body-{w.index}\n"
            )
        return "\n".join(sections)

    return _merge


STALE_BODY: str = (
    "## From stale-model (9999ms)\n\n"
    "STALE-BODY-FROM-PRIOR-RUN — must not survive resume.\n"
)


# ---------------------------------------------------------------------------
# regenerate_merge_on_resume -- standalone helper contract
# ---------------------------------------------------------------------------


def test_helper_deletes_stale_merged_when_mode_is_normalize_merge(
    tmp_path: Path,
) -> None:
    stale = tmp_path / MERGED_FILENAME
    stale.write_text(STALE_BODY, encoding="utf-8")

    deleted = regenerate_merge_on_resume(tmp_path, "normalize+merge")

    assert deleted == stale
    assert not stale.exists()


def test_helper_no_op_when_mode_is_raw(tmp_path: Path) -> None:
    stale = tmp_path / MERGED_FILENAME
    stale.write_text(STALE_BODY, encoding="utf-8")

    result = regenerate_merge_on_resume(tmp_path, "raw")

    assert result is None
    # raw mode never writes merged.md; the file is left alone (the
    # helper does not police pre-existing artifacts from other modes).
    assert stale.exists()
    assert stale.read_text(encoding="utf-8") == STALE_BODY


def test_helper_no_op_when_mode_is_normalize(tmp_path: Path) -> None:
    stale = tmp_path / MERGED_FILENAME
    stale.write_text(STALE_BODY, encoding="utf-8")

    result = regenerate_merge_on_resume(tmp_path, "normalize")

    assert result is None
    assert stale.exists()


def test_helper_idempotent_when_no_stale_file(tmp_path: Path) -> None:
    """First resume after a clean preflight (no merge written yet)."""
    assert not (tmp_path / MERGED_FILENAME).exists()
    result = regenerate_merge_on_resume(tmp_path, "normalize+merge")
    assert result is None


def test_helper_accepts_pathlike_and_str(tmp_path: Path) -> None:
    stale = tmp_path / MERGED_FILENAME
    stale.write_text(STALE_BODY, encoding="utf-8")

    deleted = regenerate_merge_on_resume(str(tmp_path), "normalize+merge")

    assert deleted is not None
    assert Path(deleted) == stale
    assert not stale.exists()


# ---------------------------------------------------------------------------
# reduce_wave3 resume=True integration -- the hook fires inline.
# ---------------------------------------------------------------------------


def test_resume_overwrites_stale_merge_with_redispatched_provenance(
    tmp_path: Path,
) -> None:
    """Pre/post resume merged.md differs when workers re-dispatched.

    Matches the §T06.02 validation: "Pre/post-resume merged.md
    differs when workers re-dispatched."
    """
    # Pre-stage a stale merged.md from a notional prior run.
    stale = tmp_path / MERGED_FILENAME
    stale.write_text(STALE_BODY, encoding="utf-8")
    stale_bytes = stale.read_bytes()

    # Re-dispatched workers carry fresh model_label / elapsed_ms.
    workers = [
        _worker(0, model_label="fresh-model-a", elapsed_ms=111),
        _worker(1, model_label="fresh-model-b", elapsed_ms=222),
        _worker(2, model_label="fresh-model-c", elapsed_ms=333),
    ]

    contract = reduce_wave3(
        workers,
        mode="normalize+merge",
        output_dir=tmp_path,
        merge_callable=_labeled_merge(),
        resume=True,
    )

    assert stale.exists()  # regenerated, not just deleted
    fresh_bytes = stale.read_bytes()
    assert fresh_bytes != stale_bytes
    body = stale.read_text(encoding="utf-8")

    # Stale provenance must be gone.
    assert "STALE-BODY-FROM-PRIOR-RUN" not in body
    assert "stale-model" not in body
    assert "9999ms" not in body

    # Re-dispatch provenance must be present, in slot order.
    assert "## From fresh-model-a (111ms)" in body
    assert "## From fresh-model-b (222ms)" in body
    assert "## From fresh-model-c (333ms)" in body
    assert body.index("fresh-model-a") < body.index("fresh-model-b")
    assert body.index("fresh-model-b") < body.index("fresh-model-c")

    # The contract reflects the regenerated artifact.
    assert contract.merged_path == str(stale)
    assert contract.amalgamation_mode == "normalize+merge"
    assert contract.workers_succeeded == 3


def test_resume_writes_merge_when_no_stale_file_present(tmp_path: Path) -> None:
    """First resume after preflight (no prior merge) still writes a body."""
    assert not (tmp_path / MERGED_FILENAME).exists()

    workers = [
        _worker(0, model_label="m-a", elapsed_ms=10),
        _worker(1, model_label="m-b", elapsed_ms=20),
    ]

    contract = reduce_wave3(
        workers,
        mode="normalize+merge",
        output_dir=tmp_path,
        merge_callable=_labeled_merge(),
        resume=True,
    )

    merged = tmp_path / MERGED_FILENAME
    assert merged.exists()
    body = merged.read_text(encoding="utf-8")
    assert "## From m-a (10ms)" in body
    assert "## From m-b (20ms)" in body
    assert contract.merged_path == str(merged)


def test_resume_deletes_stale_merge_even_when_below_floor(
    tmp_path: Path,
) -> None:
    """Regen unconditional when mode == normalize+merge.

    When the re-dispatched workers' M < policy.floor, the merge
    dispatch returns None (no replacement body). The stale file from
    the prior run MUST still be removed -- the acceptance criterion
    "Stale merge never persists post-resume" is mode-gated, not
    floor-gated. Leaving the stale body on disk would leak the
    pre-crash worker set into the resumed contract.
    """
    stale = tmp_path / MERGED_FILENAME
    stale.write_text(STALE_BODY, encoding="utf-8")

    # Only one worker succeeds -- below the default floor of 2.
    workers = [
        _worker(0, model_label="surviving", elapsed_ms=50),
        _worker(1, status="parse_error"),
        _worker(2, status="timeout"),
    ]
    calls: list[list[WorkerResult]] = []

    def merge(ws: list[WorkerResult]) -> str:  # pragma: no cover - not invoked
        calls.append(list(ws))
        return "should-not-be-called"

    contract = reduce_wave3(
        workers,
        mode="normalize+merge",
        output_dir=tmp_path,
        merge_callable=merge,
        resume=True,
    )

    # Merge callable not invoked (M < floor).
    assert calls == []
    # But the stale file is still gone.
    assert not stale.exists()
    # And the contract reports no merged_path.
    assert contract.merged_path is None
    assert contract.status == "failed"


def test_resume_false_preserves_existing_behavior(tmp_path: Path) -> None:
    """``resume=False`` (the default) does not delete pre-existing files.

    Outside resume, callers may have legitimate reasons to hold a
    pre-existing merged.md (e.g. a test fixture). The hook must only
    fire on opt-in.
    """
    stale = tmp_path / MERGED_FILENAME
    stale.write_text(STALE_BODY, encoding="utf-8")

    workers = [
        _worker(0, model_label="x", elapsed_ms=5),
        _worker(1, model_label="y", elapsed_ms=6),
    ]

    contract = reduce_wave3(
        workers,
        mode="normalize+merge",
        output_dir=tmp_path,
        merge_callable=_labeled_merge(),
        resume=False,
    )

    # The atomic write still overwrites merged.md on the success
    # path (this is the existing reduce_wave3 contract), so the
    # stale body is gone here too -- but via os.replace, not via
    # the resume hook. The difference: resume=False does NOT delete
    # the file *before* dispatch; resume=True does.
    assert (tmp_path / MERGED_FILENAME).exists()
    body = (tmp_path / MERGED_FILENAME).read_text(encoding="utf-8")
    assert "STALE-BODY-FROM-PRIOR-RUN" not in body
    assert contract.merged_path == str(stale)


def test_resume_no_op_for_raw_mode(tmp_path: Path) -> None:
    """raw mode never writes merged.md; the hook must not touch the dir.

    A stale merged.md left by an earlier run that used normalize+merge
    is NOT this hook's problem when the resume runs under raw mode.
    The hook narrowly guards the normalize+merge path; the caller is
    responsible for any cross-mode cleanup.
    """
    leftover = tmp_path / MERGED_FILENAME
    leftover.write_text(STALE_BODY, encoding="utf-8")

    workers = [_worker(0), _worker(1)]
    calls: list[list[WorkerResult]] = []

    def merge(ws: list[WorkerResult]) -> str:  # pragma: no cover - not invoked
        calls.append(list(ws))
        return ""

    contract = reduce_wave3(
        workers,
        mode="raw",
        output_dir=tmp_path,
        merge_callable=merge,
        resume=True,
    )

    assert calls == []
    assert contract.merged_path is None
    # raw mode does not touch merged.md -- the file survives.
    assert leftover.exists()
    assert leftover.read_text(encoding="utf-8") == STALE_BODY


def test_resume_no_op_for_normalize_mode(tmp_path: Path) -> None:
    """Same contract as raw: normalize mode leaves merged.md alone."""
    leftover = tmp_path / MERGED_FILENAME
    leftover.write_text(STALE_BODY, encoding="utf-8")

    workers = [_worker(0), _worker(1)]

    contract = reduce_wave3(
        workers,
        mode="normalize",
        output_dir=tmp_path,
        merge_callable=_labeled_merge(),
        resume=True,
    )

    assert contract.merged_path is None
    assert leftover.exists()
    assert leftover.read_text(encoding="utf-8") == STALE_BODY


def test_resume_still_emits_contract(tmp_path: Path) -> None:
    """Resume hook does not interfere with contract emission."""
    stale = tmp_path / MERGED_FILENAME
    stale.write_text(STALE_BODY, encoding="utf-8")

    workers = [_worker(0), _worker(1), _worker(2)]

    reduce_wave3(
        workers,
        mode="normalize+merge",
        output_dir=tmp_path,
        merge_callable=_labeled_merge(),
        resume=True,
    )

    assert (tmp_path / CONTRACT_FILENAME).exists()


def test_resume_emit_to_disk_false_skips_hook(tmp_path: Path) -> None:
    """``emit_to_disk=False`` short-circuits all disk writes, including the hook.

    The resume hook is keyed off ``should_emit`` so callers wanting an
    in-memory contract (tests, dry-runs) get one without filesystem
    side effects.
    """
    stale = tmp_path / MERGED_FILENAME
    stale.write_text(STALE_BODY, encoding="utf-8")

    reduce_wave3(
        [_worker(0), _worker(1)],
        mode="normalize+merge",
        output_dir=tmp_path,
        merge_callable=_labeled_merge(),
        resume=True,
        emit_to_disk=False,
    )

    # Stale file preserved -- no disk side effects when emit_to_disk=False.
    assert stale.exists()
    assert stale.read_text(encoding="utf-8") == STALE_BODY


# ---------------------------------------------------------------------------
# Kill-mid-merge simulation -- the canonical T06.02 §3 verification.
# ---------------------------------------------------------------------------


def test_kill_mid_merge_then_resume_yields_clean_redispatched_body(
    tmp_path: Path,
) -> None:
    """Compose the scenario described in §T06.02 step 3:

    "kill mid-merge; resume; assert new merged.md reflects re-dispatched
    workers."

    The mid-merge kill is simulated by leaving a partially-written
    body on disk that mixes stale provenance with a truncation
    artifact (the file ends without a trailing newline -- a tell-tale
    sign of fsync-then-replace not having completed). The resume
    path must replace this artifact wholesale; partial bytes from the
    crash must not survive into the regenerated body.
    """
    partial = tmp_path / MERGED_FILENAME
    partial.write_bytes(
        b"## From stale-model (9999ms)\n\n"
        b"PARTIAL-BYTES-FROM-KILLED-WRIT"  # truncated mid-word
    )
    pre_resume_bytes = partial.read_bytes()
    assert pre_resume_bytes.endswith(b"WRIT")

    # The resume orchestrator (T06.04) re-runs Wave 2 normalize on the
    # remaining workers and hands the merged set to reduce_wave3.
    redispatched = [
        _worker(0, model_label="redispatched-a", elapsed_ms=42),
        _worker(1, model_label="redispatched-b", elapsed_ms=84),
        _worker(2, model_label="redispatched-c", elapsed_ms=126),
    ]

    reduce_wave3(
        redispatched,
        mode="normalize+merge",
        output_dir=tmp_path,
        merge_callable=_labeled_merge(),
        resume=True,
    )

    post_bytes = partial.read_bytes()
    assert post_bytes != pre_resume_bytes
    # The partial-byte artifact must not survive.
    assert b"PARTIAL-BYTES-FROM-KILLED-WRIT" not in post_bytes
    # The re-dispatched provenance is present.
    body = post_bytes.decode("utf-8")
    assert "## From redispatched-a (42ms)" in body
    assert "## From redispatched-b (84ms)" in body
    assert "## From redispatched-c (126ms)" in body


# ---------------------------------------------------------------------------
# Public surface -- regenerate_merge_on_resume is exported.
# ---------------------------------------------------------------------------


def test_helper_exported_from_reduce() -> None:
    from superclaude.cli.swarm import reduce as reduce_mod

    assert "regenerate_merge_on_resume" in reduce_mod.__all__
    assert callable(reduce_mod.regenerate_merge_on_resume)


# ---------------------------------------------------------------------------
# StatusPolicy override -- the floor check still applies under resume.
# ---------------------------------------------------------------------------


def test_resume_respects_custom_status_policy_floor(tmp_path: Path) -> None:
    """A caller-supplied StatusPolicy still gates the merge dispatch.

    The resume hook fires *before* the merge dispatch and is mode-only.
    Floor-policy-dependent behavior (no merge body, no merged_path)
    must still flow through ``_reducer_normalize_merge``.
    """
    stale = tmp_path / MERGED_FILENAME
    stale.write_text(STALE_BODY, encoding="utf-8")

    workers = [
        _worker(0, model_label="ok-a", elapsed_ms=10),
        _worker(1, model_label="ok-b", elapsed_ms=20),
        _worker(2, status="timeout"),
    ]
    # Custom floor=3 demotes the 2-of-3 run below the merge gate.
    # (M==N==2 would trigger the IMM-5 success_first tiebreak; using
    # N=3 keeps the partial / failed branch reachable.)
    contract = reduce_wave3(
        workers,
        mode="normalize+merge",
        output_dir=tmp_path,
        merge_callable=_labeled_merge(),
        resume=True,
        status_policy=StatusPolicy(floor=3, partial_threshold=3),
    )

    # Stale file is still removed (mode-gated).
    assert not stale.exists()
    # But no replacement body because M < custom floor.
    assert contract.merged_path is None
    assert contract.status == "failed"


# ---------------------------------------------------------------------------
# Output confinement -- the hook never escapes output_dir.
# ---------------------------------------------------------------------------


def test_helper_never_touches_files_outside_output_dir(tmp_path: Path) -> None:
    """The hook deletes exactly ``output_dir/merged.md`` and nothing else."""
    stale = tmp_path / MERGED_FILENAME
    stale.write_text(STALE_BODY, encoding="utf-8")

    # Sibling files in the same directory must survive.
    sibling = tmp_path / "other-artifact.md"
    sibling.write_text("not the merge file", encoding="utf-8")
    contract_stub = tmp_path / CONTRACT_FILENAME
    contract_stub.write_text("prior contract", encoding="utf-8")

    # A file outside output_dir must also survive (defense in depth).
    outside_dir = tmp_path.parent / f"outside-{tmp_path.name}"
    outside_dir.mkdir()
    try:
        outside = outside_dir / MERGED_FILENAME
        outside.write_text("outside merged", encoding="utf-8")

        regenerate_merge_on_resume(tmp_path, "normalize+merge")

        assert not stale.exists()
        assert sibling.read_text(encoding="utf-8") == "not the merge file"
        assert contract_stub.read_text(encoding="utf-8") == "prior contract"
        assert outside.exists()
        assert outside.read_text(encoding="utf-8") == "outside merged"
    finally:
        # Best-effort cleanup of the sibling tmp dir we created.
        for p in outside_dir.iterdir():
            p.unlink()
        outside_dir.rmdir()
