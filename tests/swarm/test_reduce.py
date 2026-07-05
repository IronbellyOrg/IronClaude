"""T05.01 -- Wave 3 reduce orchestrator integration tests.

Pins the contract surface that :func:`superclaude.cli.swarm.reduce.reduce_wave3`
exposes:

1. **Status determination** -- IMM-5 success / partial / failed branch
   selection drives the contract's ``status`` field. The full IMM-5
   matrix has its own parametrized suite (T05.03 /
   ``test_imm5_status.py``); this file pins the orchestration glue
   (status is computed, stamped on the contract, and gates emission).
2. **Mode dispatch** -- the three :data:`AmalgamationMode` values
   produce the right artefacts on disk: ``raw`` and ``normalize``
   never write ``merged.md`` and the contract's ``merged_path`` stays
   None; ``normalize+merge`` invokes the merge callable, writes
   ``merged.md`` atomically under ``output_dir``, and records the
   path on the contract.
3. **Merge trigger** -- the ``normalize+merge`` reducer calls the
   injected ``merge_callable`` exactly once with the worker list, and
   the callable's return value lands on disk. The trigger also
   respects the ``M >= policy.floor`` gate (single-worker or
   no-worker runs in ``normalize+merge`` mode produce no merge).
4. **Contract emission** -- ``return-contract.yaml`` is written
   atomically under ``output_dir``, carries every DM-012 field after
   round-tripping through ``yaml.safe_load``, and the
   ``recommended_next_command`` placeholder is substituted from the
   provided template + substitutions dict.
5. **Output confinement** -- both emitted files land under the
   caller-supplied ``output_dir``; reduce never writes outside it.

The full DM-012 schema-presence audit lives in T05.07
(``test_contract_emission.py``); this file pins the orchestrator-level
guarantees so a regression in either the merge trigger or the
emission gate fails immediately.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable

import pytest
import yaml

from superclaude.cli.swarm.models import (
    Artifacts,
    CallerInfo,
    CallerMetadata,
    ContractTarget,
    ResultContract,
    StatusPolicy,
    WorkerResult,
)
from superclaude.cli.swarm.reduce import (
    CONTRACT_FILENAME,
    MERGED_FILENAME,
    determine_status,
    emit_contract,
    reduce_wave3,
)

# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------


def _worker(
    index: int,
    *,
    status: str = "success",
    model_label: str = "stub-model",
    body: str = "",
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
        bytes=len(body.encode("utf-8")) if body else 0,
        status=status,  # type: ignore[arg-type]
        attempts=1,
        elapsed_ms=elapsed_ms,
    )


def _capturing_merge() -> tuple[
    list[list[WorkerResult]], Callable[[list[WorkerResult]], str]
]:
    """Return a (call-log, merge-callable) pair.

    The callable records each invocation's argument list so the test
    can assert exactly-once invocation and slot-order preservation,
    and returns a deterministic synthetic merge body.
    """
    calls: list[list[WorkerResult]] = []

    def _merge(workers: list[WorkerResult]) -> str:
        calls.append(list(workers))
        sections = [
            f"## From {w.model_label} ({w.elapsed_ms}ms)\nbody-{w.index}"
            for w in workers
        ]
        return "\n\n".join(sections) + "\n"

    return calls, _merge


# ---------------------------------------------------------------------------
# Status determination (orchestration-glue smoke; full matrix lives in T05.03).
# ---------------------------------------------------------------------------


def test_status_success_when_every_worker_succeeds(tmp_path: Path) -> None:
    workers = [_worker(0), _worker(1), _worker(2)]
    contract = reduce_wave3(workers, mode="normalize", output_dir=tmp_path)
    assert contract.status == "success"
    assert contract.workers_succeeded == 3
    assert contract.workers_failed == 0
    assert contract.workers_requested == 3


def test_status_partial_when_some_workers_fail(tmp_path: Path) -> None:
    workers = [_worker(0), _worker(1), _worker(2, status="timeout")]
    contract = reduce_wave3(workers, mode="normalize", output_dir=tmp_path)
    assert contract.status == "partial"
    assert contract.workers_succeeded == 2
    assert contract.workers_failed == 1


def test_status_failed_when_below_floor(tmp_path: Path) -> None:
    workers = [
        _worker(0, status="parse_error"),
        _worker(1, status="parse_error"),
        _worker(2, status="proxy_error"),
    ]
    contract = reduce_wave3(workers, mode="normalize", output_dir=tmp_path)
    assert contract.status == "failed"
    assert contract.workers_succeeded == 0


def test_status_success_first_tiebreak_for_two_of_two(tmp_path: Path) -> None:
    """IMM-5 ``M == N == 2 && success_first`` -> success (not partial)."""
    workers = [_worker(0), _worker(1)]
    contract = reduce_wave3(workers, mode="normalize", output_dir=tmp_path)
    assert contract.status == "success"


def test_status_policy_override_respected(tmp_path: Path) -> None:
    """A custom StatusPolicy with floor=3 demotes a 2-of-3 run to failed."""
    workers = [_worker(0), _worker(1), _worker(2, status="timeout")]
    contract = reduce_wave3(
        workers,
        mode="normalize",
        output_dir=tmp_path,
        status_policy=StatusPolicy(floor=3, partial_threshold=3),
    )
    assert contract.status == "failed"


# ---------------------------------------------------------------------------
# Mode dispatch -- the three amalgamation modes (acceptance criterion).
# ---------------------------------------------------------------------------


def test_raw_mode_writes_contract_only_no_merge(tmp_path: Path) -> None:
    workers = [_worker(0), _worker(1), _worker(2)]
    calls, merge = _capturing_merge()

    contract = reduce_wave3(
        workers,
        mode="raw",
        output_dir=tmp_path,
        merge_callable=merge,
    )

    # raw mode never merges.
    assert calls == []
    assert contract.merged_path is None
    assert not (tmp_path / MERGED_FILENAME).exists()
    # Contract still emitted.
    assert (tmp_path / CONTRACT_FILENAME).exists()
    assert contract.amalgamation_mode == "raw"


def test_normalize_mode_writes_contract_only_no_merge(tmp_path: Path) -> None:
    workers = [_worker(0), _worker(1), _worker(2)]
    calls, merge = _capturing_merge()

    contract = reduce_wave3(
        workers,
        mode="normalize",
        output_dir=tmp_path,
        merge_callable=merge,
    )

    assert calls == []
    assert contract.merged_path is None
    assert not (tmp_path / MERGED_FILENAME).exists()
    assert (tmp_path / CONTRACT_FILENAME).exists()
    assert contract.amalgamation_mode == "normalize"


def test_normalize_merge_invokes_merge_and_writes_merged_file(tmp_path: Path) -> None:
    workers = [_worker(0), _worker(1), _worker(2)]
    calls, merge = _capturing_merge()

    contract = reduce_wave3(
        workers,
        mode="normalize+merge",
        output_dir=tmp_path,
        merge_callable=merge,
    )

    # Merge invoked exactly once with the worker list in slot order.
    assert len(calls) == 1
    assert [w.index for w in calls[0]] == [0, 1, 2]
    # merged.md landed under output_dir; merged_path records it.
    expected = tmp_path / MERGED_FILENAME
    assert expected.exists()
    assert contract.merged_path == str(expected)
    body = expected.read_text(encoding="utf-8")
    # Every worker's synthetic section is present in slot order.
    assert "body-0" in body and "body-1" in body and "body-2" in body
    assert body.index("body-0") < body.index("body-1") < body.index("body-2")


def test_normalize_merge_skips_merge_below_floor(tmp_path: Path) -> None:
    """M < policy.floor (default 2) leaves merged_path None even in merge mode."""
    workers = [
        _worker(0),
        _worker(1, status="parse_error"),
        _worker(2, status="timeout"),
    ]
    calls, merge = _capturing_merge()

    contract = reduce_wave3(
        workers,
        mode="normalize+merge",
        output_dir=tmp_path,
        merge_callable=merge,
    )

    # Single successful worker -> no merge invoked.
    assert calls == []
    assert contract.merged_path is None
    assert not (tmp_path / MERGED_FILENAME).exists()
    # Contract still emitted with the (failed) status.
    assert (tmp_path / CONTRACT_FILENAME).exists()
    assert contract.status == "failed"


def test_unknown_mode_raises(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="amalgamation_mode"):
        reduce_wave3([_worker(0)], mode="not-a-mode", output_dir=tmp_path)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Contract emission -- gating, atomic write, output confinement.
# ---------------------------------------------------------------------------


def test_contract_round_trips_through_yaml(tmp_path: Path) -> None:
    workers = [_worker(0), _worker(1)]
    calls, merge = _capturing_merge()

    reduce_wave3(
        workers,
        mode="normalize+merge",
        output_dir=tmp_path,
        merge_callable=merge,
        job_id="job-abc",
        started="2026-06-01T12:00:00Z",
        finished="2026-06-01T12:00:30Z",
        elapsed_ms=30000,
        lens="bare_review",
        lens_source="registry",
    )

    contract_path = tmp_path / CONTRACT_FILENAME
    payload = yaml.safe_load(contract_path.read_text(encoding="utf-8"))

    # Spot-check the DM-012 surface; T05.07 owns the full enumeration.
    assert payload["contract_version"] == "1.0"
    assert payload["status"] == "success"
    assert payload["job_id"] == "job-abc"
    assert payload["started"] == "2026-06-01T12:00:00Z"
    assert payload["finished"] == "2026-06-01T12:00:30Z"
    assert payload["elapsed_ms"] == 30000
    assert payload["lens"] == "bare_review"
    assert payload["lens_source"] == "registry"
    assert payload["amalgamation_mode"] == "normalize+merge"
    assert payload["workers_requested"] == 2
    assert payload["workers_succeeded"] == 2
    assert payload["workers_failed"] == 0
    assert payload["merged_path"] is not None
    # output_files round-trip as DM-013 dicts.
    assert isinstance(payload["output_files"], list)
    assert len(payload["output_files"]) == 2
    assert payload["output_files"][0]["index"] == 0


def test_recommended_next_command_template_substitution(tmp_path: Path) -> None:
    workers = [_worker(0), _worker(1)]
    contract = reduce_wave3(
        workers,
        mode="normalize",
        output_dir=tmp_path,
        recommended_next_command_template="/sc:foo --merged {merged} --job {job}",
        recommended_next_command_substitutions={"merged": "X.md", "job": "j-1"},
    )
    assert contract.recommended_next_command == "/sc:foo --merged X.md --job j-1"


def test_output_confinement_no_writes_outside_output_dir(tmp_path: Path) -> None:
    """Both emitted files (merged.md + return-contract.yaml) land under output_dir."""
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    workers = [_worker(0), _worker(1)]
    _, merge = _capturing_merge()

    reduce_wave3(
        workers,
        mode="normalize+merge",
        output_dir=output_dir,
        merge_callable=merge,
    )

    children = sorted(p.name for p in output_dir.iterdir())
    assert children == sorted([MERGED_FILENAME, CONTRACT_FILENAME])
    # No siblings or escapees in tmp_path.
    siblings = sorted(p.name for p in tmp_path.iterdir())
    assert siblings == ["out"]


def test_emit_to_disk_false_skips_writes(tmp_path: Path) -> None:
    """Explicit emit_to_disk=False returns the contract dataclass only."""
    workers = [_worker(0), _worker(1)]
    _, merge = _capturing_merge()

    contract = reduce_wave3(
        workers,
        mode="normalize+merge",
        output_dir=tmp_path,
        merge_callable=merge,
        emit_to_disk=False,
    )

    assert isinstance(contract, ResultContract)
    assert not (tmp_path / CONTRACT_FILENAME).exists()
    assert not (tmp_path / MERGED_FILENAME).exists()
    # merged_path is None because the merged.md write was skipped.
    assert contract.merged_path is None


def test_no_output_dir_returns_contract_only(tmp_path: Path) -> None:
    """No output_dir -> no disk writes; contract returned in-memory."""
    workers = [_worker(0), _worker(1)]
    _, merge = _capturing_merge()

    contract = reduce_wave3(
        workers,
        mode="normalize",
        merge_callable=merge,
    )

    assert isinstance(contract, ResultContract)
    # No paths in tmp_path because output_dir was never supplied.
    assert sorted(p.name for p in tmp_path.iterdir()) == []


# ---------------------------------------------------------------------------
# Direct callable surfaces (T05.03 / T05.07 will go deeper).
# ---------------------------------------------------------------------------


def test_determine_status_smoke_branches() -> None:
    """Smoke-test each IMM-5 branch routes correctly. Full matrix lives in T05.03."""
    assert determine_status(3, 3) == "success"
    assert determine_status(2, 3) == "partial"
    assert determine_status(1, 3) == "failed"
    assert determine_status(0, 3) == "failed"
    # IMM-5 tie-break.
    assert determine_status(2, 2) == "success"
    # Tie-break disabled -> still success because M >= N.
    assert determine_status(2, 2, StatusPolicy(success_first=False)) == "success"
    # N == 0 -> failed.
    assert determine_status(0, 0) == "failed"


def test_emit_contract_writes_to_supplied_dir(tmp_path: Path) -> None:
    contract = ResultContract(status="success")
    path = emit_contract(contract, tmp_path)
    assert path == tmp_path / CONTRACT_FILENAME
    assert path.exists()
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert payload["status"] == "success"
    assert payload["contract_version"] == "1.0"


def test_emit_contract_atomic_no_tmp_leftovers(tmp_path: Path) -> None:
    """Atomic write leaves no .tmp siblings on success."""
    contract = ResultContract(status="success")
    emit_contract(contract, tmp_path)
    tmp_files = [p for p in tmp_path.iterdir() if p.suffix == ".tmp"]
    assert tmp_files == []


# ---------------------------------------------------------------------------
# Contract construction details (nested records preserved).
# ---------------------------------------------------------------------------


def test_caller_and_metadata_passthrough(tmp_path: Path) -> None:
    """Caller-supplied identity records land verbatim on the contract."""
    caller = CallerInfo(
        skill="sc-bare-review", invocation_label="audit-1", kind="claude"
    )
    meta = CallerMetadata(suspect=True, tier="T2")
    target = ContractTarget(
        path="src/auth.py",
        checksum="abc123def456",  # pragma: allowlist secret (fake test fixture)
        truncated=False,
    )
    artifacts = Artifacts(manifest_path="m.json", state_path="s.json")

    contract = reduce_wave3(
        [_worker(0), _worker(1)],
        mode="normalize",
        output_dir=tmp_path,
        caller=caller,
        caller_metadata=meta,
        target=target,
        artifacts=artifacts,
    )

    assert contract.caller.skill == "sc-bare-review"
    assert contract.caller.kind == "claude"
    assert contract.caller_metadata.suspect is True
    assert contract.caller_metadata.tier == "T2"
    assert contract.target.path == "src/auth.py"
    assert contract.artifacts.manifest_path == "m.json"


def test_workers_requested_override_drives_status(tmp_path: Path) -> None:
    """N can exceed len(worker_results) -- e.g. a slot was lost mid-run."""
    workers = [_worker(0), _worker(1)]  # only 2 results received
    contract = reduce_wave3(
        workers,
        mode="normalize",
        output_dir=tmp_path,
        workers_requested=4,  # but 4 were requested
    )
    # M=2, N=4 -> partial (2 <= M < N).
    assert contract.workers_requested == 4
    assert contract.workers_succeeded == 2
    assert contract.status == "partial"


def test_output_files_preserves_slot_order(tmp_path: Path) -> None:
    workers = [_worker(2), _worker(0), _worker(1)]  # un-sorted on input
    contract = reduce_wave3(workers, mode="normalize", output_dir=tmp_path)
    # reduce preserves input order verbatim -- it doesn't re-sort
    # (sorting is the dispatcher's job, COMP-007).
    assert [w.index for w in contract.output_files] == [2, 0, 1]


# ---------------------------------------------------------------------------
# Merge callable surface (injection contract for T05.02).
# ---------------------------------------------------------------------------


def test_merge_callable_default_lazy_imports_merge_module(tmp_path: Path) -> None:
    """No explicit merge_callable -> reduce attempts to import merge.mechanical_merge.

    Since T05.02 lands the real merge module, the lazy import must
    succeed OR the test must catch a clean ImportError. This pins
    the surface so when T05.02 lands, reduce automatically routes
    through it. Pre-T05.02 we accept ImportError.
    """
    workers = [_worker(0), _worker(1)]
    try:
        contract = reduce_wave3(
            workers,
            mode="normalize+merge",
            output_dir=tmp_path,
            # No merge_callable -> default lazy import path.
        )
    except ImportError:
        # Pre-T05.02: merge module not yet present. Acceptable.
        pytest.skip("merge module not yet implemented (T05.02)")
    else:
        # Post-T05.02: merged.md must exist + merged_path on contract.
        assert contract.merged_path is not None
        assert (tmp_path / MERGED_FILENAME).exists()
