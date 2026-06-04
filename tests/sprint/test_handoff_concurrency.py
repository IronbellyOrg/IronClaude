"""Stage-3 M2/L4 — concurrent JSONL writers, zero corruption over >=1000 writes.

Spins up >=4 threads each calling the now-lock-guarded ``SprintLogger._jsonl`` in
a tight loop (>=1000 total writes), then reads the JSONL back and asserts no lost
/ torn / interleaved lines and that the exact multiset of payloads survives. This
would FAIL against the pre-Stage-3 lock-free ``_jsonl`` (interleaved partial
writes) and PASS against the locked one.
"""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from superclaude.cli.sprint.logging_ import SprintLogger
from superclaude.cli.sprint.models import Phase, SprintConfig

_N_THREADS = 4
_PER_THREAD = 300  # 4 * 300 = 1200 total writes (> 1000)


def _config(tmp_path: Path) -> SprintConfig:
    pf = tmp_path / "phase-1-tasklist.md"
    pf.write_text("# Phase 1\n")
    index = tmp_path / "tasklist-index.md"
    index.write_text("index\n")
    return SprintConfig(
        index_path=index,
        release_dir=tmp_path,
        phases=[Phase(number=1, file=pf, name="Phase 1")],
        start_phase=1,
        end_phase=1,
        max_turns=100,
    )


@pytest.mark.slow
@pytest.mark.nfr_benchmark
def test_jsonl_concurrent_writers_no_corruption(tmp_path: Path) -> None:
    config = _config(tmp_path)
    logger = SprintLogger(config)

    def _writer(tid: int) -> None:
        for i in range(_PER_THREAD):
            logger._jsonl(
                {
                    "event": "task_complete",
                    "phase": 1,
                    "task_id": f"T{tid:02d}.{i:04d}",
                    "status": "pass",
                    "turns": i,
                    "duration_sec": 0.01,
                }
            )

    with ThreadPoolExecutor(max_workers=_N_THREADS) as pool:
        list(pool.map(_writer, range(_N_THREADS)))

    raw = config.execution_log_jsonl.read_text()
    lines = [line for line in raw.splitlines() if line.strip()]
    total_expected = _N_THREADS * _PER_THREAD

    # (a) no lost / torn writes — exact line count.
    assert len(lines) == total_expected, (
        f"expected {total_expected} JSONL lines, got {len(lines)} (lost/torn writes)"
    )

    # (b) every line is well-formed JSON (no interleaving/tearing).
    parsed = []
    for line in lines:
        parsed.append(json.loads(line))  # raises on a torn/interleaved line

    # (c) the exact multiset of payloads survives.
    got = sorted(p["task_id"] for p in parsed)
    expected = sorted(
        f"T{tid:02d}.{i:04d}" for tid in range(_N_THREADS) for i in range(_PER_THREAD)
    )
    assert got == expected, "payload multiset mismatch — some writes lost or duplicated"
