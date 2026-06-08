"""T05.02 / T05.09 -- merge.py mechanical-only boundary test.

Pins the AC-012 / NFR-009 contract:
:func:`superclaude.cli.swarm.merge.mechanical_merge` concatenates the
per-worker ``final_path`` bodies verbatim, in slot-index order, with a
single ``## From {model_label} ({elapsed_ms}ms)`` provenance header
prepended per section -- nothing else.

This is one of the two test files explicitly named as a PR-review-
discipline guard (the other is the recipe boundary). The file path is
flagged in the CI workflow so any PR that touches it is forced
through human review.

Three-worker fixture (per acceptance criterion):
* worker indices arrive out of order (2, 0, 1) so the test pins the
  slot-index sort and rules out source-list ordering as the cause of
  any pass.
* each worker body uses a distinct sentinel string so the test can
  assert that every body lands intact and no body has been edited,
  filtered, or reordered relative to its peers.
* model labels and elapsed_ms differ per slot to lock the provenance
  header format.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.swarm.merge import mechanical_merge
from superclaude.cli.swarm.models import WorkerResult


def _write_worker(
    tmp_path: Path,
    *,
    index: int,
    model_label: str,
    elapsed_ms: int,
    body: str,
) -> WorkerResult:
    final_path = tmp_path / f"worker-{index:02d}.final.md"
    final_path.write_text(body, encoding="utf-8")
    return WorkerResult(
        index=index,
        path=str(final_path),
        raw_path=str(tmp_path / f"worker-{index:02d}.raw.md"),
        meta_path=str(tmp_path / f"worker-{index:02d}.meta.json"),
        final_path=str(final_path),
        model_id=f"model-id-{index}",
        model_label=model_label,
        bytes=len(body.encode("utf-8")),
        status="success",
        attempts=1,
        elapsed_ms=elapsed_ms,
    )


@pytest.fixture()
def three_workers(tmp_path: Path) -> list[WorkerResult]:
    return [
        _write_worker(
            tmp_path,
            index=2,
            model_label="claude-haiku-4.5",
            elapsed_ms=2222,
            body="SENTINEL_TWO body text -- worker 2.",
        ),
        _write_worker(
            tmp_path,
            index=0,
            model_label="gpt-5-codex",
            elapsed_ms=1111,
            body="SENTINEL_ZERO body text -- worker 0.",
        ),
        _write_worker(
            tmp_path,
            index=1,
            model_label="gemini-2.5-pro",
            elapsed_ms=3333,
            body="SENTINEL_ONE body text -- worker 1.",
        ),
    ]


def test_three_worker_concat_preserves_slot_index_order(
    three_workers: list[WorkerResult],
) -> None:
    merged = mechanical_merge(three_workers)
    pos_zero = merged.find("SENTINEL_ZERO")
    pos_one = merged.find("SENTINEL_ONE")
    pos_two = merged.find("SENTINEL_TWO")
    assert -1 < pos_zero < pos_one < pos_two, (
        "merge must order sections by WorkerResult.index regardless of "
        f"input order; got positions zero={pos_zero}, one={pos_one}, two={pos_two}"
    )


def test_each_section_carries_only_provenance_header(
    three_workers: list[WorkerResult],
) -> None:
    merged = mechanical_merge(three_workers)
    assert "## From gpt-5-codex (1111ms)" in merged
    assert "## From gemini-2.5-pro (3333ms)" in merged
    assert "## From claude-haiku-4.5 (2222ms)" in merged
    # Header is the only structural addition; the only level-2 headings
    # in the merged body are the three provenance headers.
    assert merged.count("\n## ") + (1 if merged.startswith("## ") else 0) == 3


def test_each_worker_body_is_verbatim(
    three_workers: list[WorkerResult],
) -> None:
    merged = mechanical_merge(three_workers)
    assert "SENTINEL_ZERO body text -- worker 0." in merged
    assert "SENTINEL_ONE body text -- worker 1." in merged
    assert "SENTINEL_TWO body text -- worker 2." in merged


def test_merge_does_not_reorder_within_section(tmp_path: Path) -> None:
    # A body whose lines would sort to a different order than authored;
    # if merge ever sorts, this test fails.
    body = "zebra\nalpha\nmango\n"
    worker = _write_worker(
        tmp_path,
        index=0,
        model_label="m",
        elapsed_ms=10,
        body=body,
    )
    merged = mechanical_merge([worker])
    z = merged.find("zebra")
    a = merged.find("alpha")
    m = merged.find("mango")
    assert -1 < z < a < m


def test_merge_does_not_deduplicate_across_workers(tmp_path: Path) -> None:
    duplicate = "DUPLICATE_FINDING line.\n"
    workers = [
        _write_worker(
            tmp_path, index=0, model_label="m0", elapsed_ms=1, body=duplicate,
        ),
        _write_worker(
            tmp_path, index=1, model_label="m1", elapsed_ms=2, body=duplicate,
        ),
    ]
    merged = mechanical_merge(workers)
    assert merged.count("DUPLICATE_FINDING") == 2


def test_merge_handles_empty_worker_list() -> None:
    assert mechanical_merge([]) == ""


def test_merge_handles_missing_final_path_gracefully(tmp_path: Path) -> None:
    """A failed worker may have an empty ``final_path``; the section
    still emits with its provenance header so slot-index alignment
    survives downstream readers."""
    workers = [
        _write_worker(
            tmp_path, index=0, model_label="m0", elapsed_ms=1, body="real",
        ),
        WorkerResult(
            index=1,
            model_label="m1",
            elapsed_ms=2,
            status="parse_error",
        ),
    ]
    merged = mechanical_merge(workers)
    assert "## From m0 (1ms)" in merged
    assert "## From m1 (2ms)" in merged
    assert "real" in merged


def test_merge_handles_final_path_pointing_at_missing_file() -> None:
    """``final_path`` set but the file doesn't exist on disk -- e.g. a
    timeout-then-promoted worker whose normalize step never ran. The
    section still emits (empty body) so the slot is visible in merged.md
    rather than silently dropped."""
    worker = WorkerResult(
        index=0,
        final_path="/no/such/path/worker-00.final.md",
        model_label="m",
        elapsed_ms=42,
        status="timeout",
    )
    merged = mechanical_merge([worker])
    assert "## From m (42ms)" in merged
