"""Tests for FR-G4 reproducible artifact layout (R-074 / D-0074 / T04.13).

Pins the contract :mod:`superclaude.cli.eval.artifact_layout` exposes:

* :func:`compose_run_dir` returns
  ``<output_root>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/``.
* :func:`compose_run_id` is deterministic for ``(started_at, suite_name)``
  and varies when either input changes.
* :func:`allocate_per_eval_paths` creates a per-eval subtree with the
  three pinned entries (``logs.jsonl``, ``tty.transcript``,
  ``artifacts/``).
* :func:`parse_run_dir_components` round-trips the ``(date, run-id)``
  pair encoded by a constructed run-dir.

These tests cover the FR-G4 acceptance criteria from
``.dev/releases/current/cliEval/phase-4-tasklist.md`` (§T04.13).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from superclaude.cli.eval.artifact_layout import (
    ARTIFACTS_SUBDIR_NAME,
    LOGS_JSONL_NAME,
    PER_EVAL_DIRNAME,
    PerEvalPaths,
    RUN_DIR_PREFIX,
    RunDirComponents,
    TTY_TRANSCRIPT_NAME,
    allocate_per_eval_paths,
    compose_per_eval_dir,
    compose_run_dir,
    compose_run_id,
    parse_run_dir_components,
)


# ---------------------------------------------------------------------------
# compose_run_id — determinism + variation
# ---------------------------------------------------------------------------


def test_compose_run_id_shape() -> None:
    """Run-id matches ``<HHMMSSZ>-<8-hex>`` shape."""

    rid = compose_run_id("2026-05-20T15:58:38Z", suite_name="real")
    assert re.fullmatch(r"\d{6}Z-[0-9a-f]{8}", rid), rid


def test_compose_run_id_deterministic_for_same_inputs() -> None:
    """Same ``(started_at, suite_name)`` -> same id (FR-G4 AC)."""

    a = compose_run_id("2026-05-20T15:58:38Z", suite_name="real")
    b = compose_run_id("2026-05-20T15:58:38Z", suite_name="real")
    assert a == b


def test_compose_run_id_changes_with_suite_name() -> None:
    """Different suite -> different id even at the same timestamp."""

    a = compose_run_id("2026-05-20T15:58:38Z", suite_name="real")
    b = compose_run_id("2026-05-20T15:58:38Z", suite_name="other")
    assert a != b
    # Same time-of-day prefix; only the hash tail differs.
    assert a.split("-")[0] == b.split("-")[0]


def test_compose_run_id_changes_with_timestamp() -> None:
    """Different start timestamp -> different id."""

    a = compose_run_id("2026-05-20T15:58:38Z", suite_name="real")
    b = compose_run_id("2026-05-20T15:58:39Z", suite_name="real")
    assert a != b


def test_compose_run_id_handles_naive_iso() -> None:
    """ISO instants without a tz are interpreted as UTC for the time prefix.

    The hash tail incorporates the literal ``started_at`` string so two
    callers spelling the same instant differently see different tails
    (this keeps ``compose_run_id`` injective in ``started_at``). The
    ``HHMMSSZ`` prefix matches because both spellings denote the same
    wall-clock UTC instant.
    """

    naive = compose_run_id("2026-05-20T15:58:38", suite_name="real")
    aware = compose_run_id("2026-05-20T15:58:38Z", suite_name="real")
    assert naive.split("-")[0] == aware.split("-")[0]


def test_compose_run_id_handles_offset_form() -> None:
    """``+00:00`` is accepted as an alias for ``Z``."""

    offset = compose_run_id("2026-05-20T15:58:38+00:00", suite_name="real")
    z_form = compose_run_id("2026-05-20T15:58:38Z", suite_name="real")
    # The raw ``started_at`` string is what hashes; ``+00:00`` and ``Z``
    # are *different* strings so the hash tails diverge. The time prefix
    # is the part that must match.
    assert offset.split("-")[0] == z_form.split("-")[0]


def test_compose_run_id_rejects_bad_iso() -> None:
    """Garbage timestamps raise ``ValueError`` rather than producing junk."""

    with pytest.raises(ValueError):
        compose_run_id("not-an-iso", suite_name="real")
    with pytest.raises(ValueError):
        compose_run_id("", suite_name="real")


# ---------------------------------------------------------------------------
# compose_run_dir — layout shape
# ---------------------------------------------------------------------------


def test_compose_run_dir_shape(tmp_path: Path) -> None:
    """Run-dir matches ``<root>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/``."""

    run_dir = compose_run_dir(tmp_path, "2026-05-20T15:58:38Z", suite_name="real")
    rel = run_dir.relative_to(tmp_path).parts
    assert rel[0] == ".dev"
    assert rel[1] == "eval-runs"
    assert rel[2] == "2026-05-20"
    # Last segment is the run-id; shape pinned by compose_run_id tests.
    assert re.fullmatch(r"\d{6}Z-[0-9a-f]{8}", rel[3])


def test_compose_run_dir_anchored_at_run_dir_prefix(tmp_path: Path) -> None:
    """The constructed path sits under :data:`RUN_DIR_PREFIX`."""

    run_dir = compose_run_dir(tmp_path, "2026-05-20T15:58:38Z", suite_name="real")
    assert RUN_DIR_PREFIX.as_posix() in run_dir.as_posix()


def test_compose_run_dir_does_not_create_directory(tmp_path: Path) -> None:
    """Composition is path-construction only; no mkdir side-effect."""

    run_dir = compose_run_dir(tmp_path, "2026-05-20T15:58:38Z", suite_name="real")
    assert not run_dir.exists()


def test_compose_run_dir_deterministic_same_inputs(tmp_path: Path) -> None:
    """Same inputs -> same run-dir path."""

    a = compose_run_dir(tmp_path, "2026-05-20T15:58:38Z", suite_name="real")
    b = compose_run_dir(tmp_path, "2026-05-20T15:58:38Z", suite_name="real")
    assert a == b


# ---------------------------------------------------------------------------
# Per-eval subtree
# ---------------------------------------------------------------------------


def test_compose_per_eval_dir_shape(tmp_path: Path) -> None:
    """``<run_dir>/per-eval/<eval_id>/`` is the per-eval dir."""

    run_dir = tmp_path / "run"
    eval_dir = compose_per_eval_dir(run_dir, "E1")
    rel = eval_dir.relative_to(run_dir).parts
    assert rel == (PER_EVAL_DIRNAME, "E1")


def test_compose_per_eval_dir_rejects_path_traversal(tmp_path: Path) -> None:
    """Path-traversal candidates raise rather than escaping the subtree."""

    run_dir = tmp_path / "run"
    with pytest.raises(ValueError):
        compose_per_eval_dir(run_dir, "../escape")
    with pytest.raises(ValueError):
        compose_per_eval_dir(run_dir, "")
    with pytest.raises(ValueError):
        compose_per_eval_dir(run_dir, "has slash/in-it")


def test_allocate_per_eval_paths_creates_subtree(tmp_path: Path) -> None:
    """FR-G4 AC: ``logs.jsonl``, ``tty.transcript``, ``artifacts/`` exist.

    The directory entries themselves are created; the two files are
    *not* materialised — the runner / PtyDriver opens them on first
    write so an unused eval leaves a clean directory.
    """

    run_dir = tmp_path / "run"
    paths = allocate_per_eval_paths(run_dir, "E1")

    assert isinstance(paths, PerEvalPaths)
    assert paths.eval_dir.is_dir()
    assert paths.artifacts_dir.is_dir()
    # Files are pinned by path but not pre-created.
    assert paths.logs_jsonl.name == LOGS_JSONL_NAME
    assert paths.tty_transcript.name == TTY_TRANSCRIPT_NAME
    assert paths.artifacts_dir.name == ARTIFACTS_SUBDIR_NAME
    assert not paths.logs_jsonl.exists()
    assert not paths.tty_transcript.exists()


def test_allocate_per_eval_paths_idempotent(tmp_path: Path) -> None:
    """Re-allocating an existing per-eval subtree is a no-op for state."""

    run_dir = tmp_path / "run"
    first = allocate_per_eval_paths(run_dir, "E1")
    # Drop a file into artifacts/ so we can confirm a re-allocation does
    # not wipe existing state.
    sentinel = first.artifacts_dir / "sentinel.txt"
    sentinel.write_text("kept", encoding="utf-8")
    second = allocate_per_eval_paths(run_dir, "E1")
    assert first == second
    assert sentinel.read_text(encoding="utf-8") == "kept"


def test_allocate_per_eval_paths_create_false(tmp_path: Path) -> None:
    """``create=False`` returns paths without touching disk."""

    run_dir = tmp_path / "run"
    paths = allocate_per_eval_paths(run_dir, "E1", create=False)
    assert not paths.eval_dir.exists()
    assert not paths.artifacts_dir.exists()


# ---------------------------------------------------------------------------
# parse_run_dir_components — inverse of compose_run_dir
# ---------------------------------------------------------------------------


def test_parse_run_dir_components_roundtrip(tmp_path: Path) -> None:
    """``parse_run_dir_components(compose_run_dir(...))`` recovers inputs."""

    started_at = "2026-05-20T15:58:38Z"
    run_dir = compose_run_dir(tmp_path, started_at, suite_name="real")
    parsed = parse_run_dir_components(run_dir)
    assert isinstance(parsed, RunDirComponents)
    assert parsed.date_segment == "2026-05-20"
    assert parsed.run_id == compose_run_id(started_at, suite_name="real")


def test_parse_run_dir_components_rejects_non_layout_path(tmp_path: Path) -> None:
    """Paths outside the FR-G4 layout raise ``ValueError`` loudly."""

    with pytest.raises(ValueError):
        parse_run_dir_components(tmp_path / "not" / "the" / "layout")


def test_parse_run_dir_components_tolerates_trailing_subpath(tmp_path: Path) -> None:
    """Trailing segments after the run-id (per-eval/...) still parse."""

    run_dir = compose_run_dir(tmp_path, "2026-05-20T15:58:38Z", suite_name="real")
    inner = run_dir / PER_EVAL_DIRNAME / "E1"
    parsed = parse_run_dir_components(inner)
    assert parsed.date_segment == "2026-05-20"
    assert re.fullmatch(r"\d{6}Z-[0-9a-f]{8}", parsed.run_id)
