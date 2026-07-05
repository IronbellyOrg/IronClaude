"""T05.04 -- Three amalgamation modes dispatch (FR-011 / R-102).

Pins the :func:`superclaude.cli.swarm.reduce.select_mode` dispatch table
and the artifact-set guarantee each :data:`AmalgamationMode` makes to
callers:

    ====================  ==============================================
    Mode                  Per-run on-disk artifacts (under ``output_dir``)
    ====================  ==============================================
    ``raw``               return-contract.yaml only (per-worker
                          ``raw_path`` files already on disk; reduce
                          never writes ``merged.md``).
    ``normalize``         return-contract.yaml only (per-worker
                          ``final_path`` files already on disk; reduce
                          never writes ``merged.md``).
    ``normalize+merge``   return-contract.yaml AND ``merged.md`` (when
                          ``workers_succeeded >= policy.floor``).
    ====================  ==============================================

The dispatch surface has three independently checked properties:

1. **Dispatch correctness** -- :func:`select_mode` returns the exact
   reducer registered for each mode; unknown modes raise
   :class:`ValueError` listing the accepted set.
2. **Per-mode artifact set** -- ``reduce_wave3`` end-to-end under each
   mode lands the right files under ``output_dir`` and stamps the
   right ``merged_path`` on the contract.
3. **Reducer return semantics** -- ``raw`` / ``normalize`` reducers
   always return ``None`` (no merged body); ``normalize+merge`` returns
   the merge callable's body when the floor gate is satisfied and
   ``None`` otherwise.

Complements ``test_reduce.py`` (orchestrator integration) and
``test_imm5_status.py`` (status matrix). This file is the canonical
parametrization for FR-011 / R-102.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.swarm.models import (
    AmalgamationMode,
    StatusPolicy,
    WorkerResult,
)
from superclaude.cli.swarm.reduce import (
    CONTRACT_FILENAME,
    MERGED_FILENAME,
    MergeCallable,
    reduce_wave3,
    select_mode,
)

# ---------------------------------------------------------------------------
# Fixture helpers -- mirror tests/swarm/test_reduce.py shapes so the two
# files share an interpretive model without an importable common module.
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
        status=status,  # type: ignore[arg-type]
        elapsed_ms=elapsed_ms,
    )


def _capturing_merge() -> tuple[list[list[WorkerResult]], MergeCallable]:
    """Return a (call-log, merge-callable) pair.

    The callable records each invocation's argument list and returns a
    deterministic synthetic merge body so the test can assert that the
    artifact landed on disk verbatim.
    """
    calls: list[list[WorkerResult]] = []

    def _merge(workers: list[WorkerResult]) -> str:
        calls.append(list(workers))
        return "MERGED:" + ",".join(str(w.index) for w in workers) + "\n"

    return calls, _merge


# ---------------------------------------------------------------------------
# 1. Dispatch correctness -- the table itself.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("mode", ["raw", "normalize", "normalize+merge"])
def test_select_mode_returns_a_callable_for_every_amalgamation_mode(
    mode: AmalgamationMode,
) -> None:
    reducer = select_mode(mode)
    assert callable(reducer)


def test_select_mode_returns_distinct_reducer_per_mode() -> None:
    """The three modes route through three different reducer functions."""
    raw = select_mode("raw")
    normalize = select_mode("normalize")
    merge = select_mode("normalize+merge")
    # All three reducers are distinct callables -- no accidental
    # collapse of the dispatch table.
    assert raw is not normalize
    assert normalize is not merge
    assert raw is not merge


@pytest.mark.parametrize(
    "bad_mode",
    ["", "raw+normalize", "merge", "RAW", "normalize-merge", "unknown"],
)
def test_select_mode_rejects_unknown_modes(bad_mode: str) -> None:
    with pytest.raises(ValueError, match="amalgamation_mode"):
        select_mode(bad_mode)  # type: ignore[arg-type]


def test_select_mode_error_lists_accepted_modes() -> None:
    """The error string enumerates the accepted modes for operator triage."""
    with pytest.raises(ValueError) as excinfo:
        select_mode("not-a-mode")  # type: ignore[arg-type]
    message = str(excinfo.value)
    assert "raw" in message
    assert "normalize" in message
    assert "normalize+merge" in message


# ---------------------------------------------------------------------------
# 2. Reducer return semantics -- direct invocation.
# ---------------------------------------------------------------------------


def test_raw_reducer_returns_none_regardless_of_workers() -> None:
    reducer = select_mode("raw")
    calls, merge = _capturing_merge()
    body = reducer(
        [_worker(0), _worker(1)],
        merge_callable=merge,
        workers_succeeded=2,
        policy=StatusPolicy(),
    )
    assert body is None
    # raw must never call the injected merge callable.
    assert calls == []


def test_normalize_reducer_returns_none_regardless_of_workers() -> None:
    reducer = select_mode("normalize")
    calls, merge = _capturing_merge()
    body = reducer(
        [_worker(0), _worker(1), _worker(2)],
        merge_callable=merge,
        workers_succeeded=3,
        policy=StatusPolicy(),
    )
    assert body is None
    # normalize must never call the injected merge callable.
    assert calls == []


def test_normalize_merge_reducer_invokes_merge_when_floor_met() -> None:
    reducer = select_mode("normalize+merge")
    calls, merge = _capturing_merge()
    body = reducer(
        [_worker(0), _worker(1), _worker(2)],
        merge_callable=merge,
        workers_succeeded=3,
        policy=StatusPolicy(),
    )
    assert body == "MERGED:0,1,2\n"
    assert len(calls) == 1
    assert [w.index for w in calls[0]] == [0, 1, 2]


def test_normalize_merge_reducer_skips_merge_below_floor() -> None:
    """``workers_succeeded < policy.floor`` -> reducer returns None, no call."""
    reducer = select_mode("normalize+merge")
    calls, merge = _capturing_merge()
    body = reducer(
        [_worker(0)],
        merge_callable=merge,
        workers_succeeded=1,  # below default floor=2
        policy=StatusPolicy(),
    )
    assert body is None
    assert calls == []


def test_normalize_merge_reducer_respects_custom_floor() -> None:
    """A higher floor demotes a 2-worker run to no-merge."""
    reducer = select_mode("normalize+merge")
    calls, merge = _capturing_merge()
    body = reducer(
        [_worker(0), _worker(1)],
        merge_callable=merge,
        workers_succeeded=2,
        policy=StatusPolicy(floor=3),
    )
    assert body is None
    assert calls == []


# ---------------------------------------------------------------------------
# 3. Per-mode artifact set -- end-to-end via reduce_wave3.
# ---------------------------------------------------------------------------


def test_raw_mode_artifact_set_contract_only(tmp_path: Path) -> None:
    """``raw`` mode lands ``return-contract.yaml`` only; no ``merged.md``."""
    workers = [_worker(0), _worker(1), _worker(2)]
    _, merge = _capturing_merge()

    contract = reduce_wave3(
        workers,
        mode="raw",
        output_dir=tmp_path,
        merge_callable=merge,
    )

    children = sorted(p.name for p in tmp_path.iterdir())
    assert children == [CONTRACT_FILENAME]
    assert contract.merged_path is None
    assert contract.amalgamation_mode == "raw"


def test_normalize_mode_artifact_set_contract_only(tmp_path: Path) -> None:
    """``normalize`` mode lands ``return-contract.yaml`` only; no ``merged.md``."""
    workers = [_worker(0), _worker(1), _worker(2)]
    _, merge = _capturing_merge()

    contract = reduce_wave3(
        workers,
        mode="normalize",
        output_dir=tmp_path,
        merge_callable=merge,
    )

    children = sorted(p.name for p in tmp_path.iterdir())
    assert children == [CONTRACT_FILENAME]
    assert contract.merged_path is None
    assert contract.amalgamation_mode == "normalize"


def test_normalize_merge_mode_artifact_set_includes_merged(tmp_path: Path) -> None:
    """``normalize+merge`` mode lands BOTH ``return-contract.yaml`` AND ``merged.md``."""
    workers = [_worker(0), _worker(1), _worker(2)]
    _, merge = _capturing_merge()

    contract = reduce_wave3(
        workers,
        mode="normalize+merge",
        output_dir=tmp_path,
        merge_callable=merge,
    )

    children = sorted(p.name for p in tmp_path.iterdir())
    assert children == sorted([CONTRACT_FILENAME, MERGED_FILENAME])
    assert contract.merged_path == str(tmp_path / MERGED_FILENAME)
    assert contract.amalgamation_mode == "normalize+merge"
    # Merged body lands verbatim from the merge callable.
    assert (tmp_path / MERGED_FILENAME).read_text(encoding="utf-8") == "MERGED:0,1,2\n"


# ---------------------------------------------------------------------------
# Parametrized cross-mode matrix -- one row per mode, asserts the
# exact (artifact_names, merged_path_is_set) shape so a regression that
# (a) writes merged.md in a no-merge mode, or (b) skips merged.md in
# normalize+merge, fails with a single pointer.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "mode, expected_files, merged_path_set",
    [
        ("raw", [CONTRACT_FILENAME], False),
        ("normalize", [CONTRACT_FILENAME], False),
        ("normalize+merge", sorted([CONTRACT_FILENAME, MERGED_FILENAME]), True),
    ],
)
def test_mode_artifact_set_matrix(
    tmp_path: Path,
    mode: AmalgamationMode,
    expected_files: list[str],
    merged_path_set: bool,
) -> None:
    workers = [_worker(0), _worker(1)]
    _, merge = _capturing_merge()

    contract = reduce_wave3(
        workers,
        mode=mode,
        output_dir=tmp_path,
        merge_callable=merge,
    )

    children = sorted(p.name for p in tmp_path.iterdir())
    assert children == expected_files
    assert (contract.merged_path is not None) == merged_path_set
    assert contract.amalgamation_mode == mode
