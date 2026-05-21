"""FR-G4 reproducible artifact layout for the cliEval harness.

Roadmap row R-074 / Deliverable D-0074 (Task T04.13) pins the on-disk
shape of every ``superclaude eval run`` invocation::

    <output_root>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/
        summary.md
        summary.json
        summary.yaml
        junit.xml          (only when --junit is set)
        per-eval/
            <eval_id>/
                logs.jsonl
                tty.transcript
                artifacts/

This module is the *single source of truth* for that layout. Callers
build paths through :func:`compose_run_dir` and
:func:`allocate_per_eval_paths` so the layout cannot drift between the
CLI, the Reporter (T03.13 / D-0055), and the per-eval JSONL emitter
(T03.05 / D-0049).

Determinism
-----------

``compose_run_id(started_at, suite_name)`` returns the same string for
the same inputs. The run-id encodes the UTC time-of-day (``HHMMSSZ``)
plus the first 8 hex chars of ``sha256(suite_name + "\\n" + started_at)``
so two runs at the same instant against the same suite collide on the
same path — the FR-G4 acceptance criterion the phase-4 tasklist pins
("Run-id is deterministic for a given start timestamp + suite name").

AC12 / scratch-root allowlist
-----------------------------

This module only *constructs* paths; it never resolves or validates
them against the AC12 (T01.19 / D-0016) scratch-root allowlist. The
caller (``commands.eval_run``) passes the constructed path through
:func:`~superclaude.cli.eval.config.resolve_scratch_root` before any
``mkdir`` so the allowlist remains the single enforcement boundary.
The default ``output_root=Path.cwd()`` combined with
``RUN_DIR_PREFIX = .dev/eval-runs`` lands inside the canonical AC12
prefix automatically; operators supplying an explicit ``--output-dir``
bypass this module entirely and the AC12 check stays the gate.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

__all__ = [
    "ARTIFACTS_SUBDIR_NAME",
    "LOGS_JSONL_NAME",
    "PER_EVAL_DIRNAME",
    "PerEvalPaths",
    "RUN_DIR_PREFIX",
    "RunDirComponents",
    "TTY_TRANSCRIPT_NAME",
    "allocate_per_eval_paths",
    "compose_per_eval_dir",
    "compose_run_dir",
    "compose_run_id",
    "parse_run_dir_components",
]


# ---------------------------------------------------------------------------
# Layout constants
# ---------------------------------------------------------------------------


RUN_DIR_PREFIX: Path = Path(".dev/eval-runs")
"""Repo-relative root for every per-run artifact tree.

Matches the canonical AC12 prefix declared by
:func:`superclaude.cli.eval.config._default_allowed_scratch_roots` so a
default-resolved run-dir always lands inside the allowlist.
"""

PER_EVAL_DIRNAME: str = "per-eval"
LOGS_JSONL_NAME: str = "logs.jsonl"
TTY_TRANSCRIPT_NAME: str = "tty.transcript"
ARTIFACTS_SUBDIR_NAME: str = "artifacts"


# Run-id digest configuration
_RUN_ID_HASH_LEN: int = 8
_TIME_SEGMENT_FMT: str = "%H%M%SZ"
_DATE_SEGMENT_FMT: str = "%Y-%m-%d"


# Eval-id allowlist — the FR-SCH2 regex pinned by the schema (kept
# defensive here so this module rejects out-of-band ids at the layout
# boundary rather than producing path-traversal candidates).
_EVAL_ID_RE = re.compile(r"^[A-Za-z0-9_.-]{1,64}$")


# ---------------------------------------------------------------------------
# ISO instant parsing
# ---------------------------------------------------------------------------


def _parse_iso(started_at: str) -> datetime:
    """Parse ``started_at`` as an ISO 8601 instant in UTC.

    Accepts both ``Z`` suffix and ``+00:00`` style offsets. Naive
    timestamps are interpreted as UTC. The return value is always
    timezone-aware and normalised to UTC so subsequent ``strftime``
    calls render the same string across hosts.
    """

    if not isinstance(started_at, str) or not started_at.strip():
        raise ValueError(
            f"started_at must be a non-empty ISO 8601 string; got {started_at!r}"
        )
    s = started_at.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(s)
    except ValueError as exc:
        raise ValueError(
            f"started_at {started_at!r} is not a valid ISO 8601 instant: {exc}"
        ) from exc
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


# ---------------------------------------------------------------------------
# Run-id + run-dir composition
# ---------------------------------------------------------------------------


def compose_run_id(started_at: str, suite_name: str = "") -> str:
    """Return the per-run identifier for ``(started_at, suite_name)``.

    Shape: ``<HHMMSSZ>-<8-hex>`` where the 8-hex tail is the first
    :data:`_RUN_ID_HASH_LEN` chars of
    ``sha256(suite_name + "\\n" + started_at)``.

    The id is deterministic — calling this twice with the same inputs
    yields the same string — which is exactly the FR-G4 acceptance
    criterion ("Run-id is deterministic for a given start timestamp +
    suite name"). The hash incorporates ``suite_name`` so two
    simultaneous runs against different suites cannot collide on the
    same id.
    """

    dt = _parse_iso(started_at)
    time_segment = dt.strftime(_TIME_SEGMENT_FMT)
    digest = hashlib.sha256(
        (str(suite_name) + "\n" + started_at).encode("utf-8")
    ).hexdigest()[:_RUN_ID_HASH_LEN]
    return f"{time_segment}-{digest}"


def compose_run_dir(
    output_root: Path | str,
    started_at: str,
    suite_name: str = "",
) -> Path:
    """Return ``<output_root>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/``.

    The path is **constructed**, not created — the caller is responsible
    for ``mkdir(parents=True, exist_ok=True)`` *after* the AC12 (T01.19)
    scratch-root allowlist has validated it.

    Arguments
    ---------
    output_root:
        Anchor directory under which the ``.dev/eval-runs/`` subtree is
        rooted. Operators routinely pass :func:`Path.cwd` so the layout
        lands inside the repo's canonical AC12 prefix.
    started_at:
        ISO 8601 instant marking when the run started. Used for the
        ``<YYYY-MM-DD>`` date segment + the ``HHMMSSZ`` half of the
        run-id.
    suite_name:
        Stable identifier for the suite being executed (``--suite``
        value). Folded into the run-id hash so runs against different
        suites cannot collide.
    """

    dt = _parse_iso(started_at)
    date_segment = dt.strftime(_DATE_SEGMENT_FMT)
    run_id = compose_run_id(started_at, suite_name)
    return Path(output_root) / RUN_DIR_PREFIX / date_segment / run_id


# ---------------------------------------------------------------------------
# Per-eval subtree
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PerEvalPaths:
    """Resolved paths inside a single per-eval subtree.

    Every path is rooted at :attr:`eval_dir`; :attr:`artifacts_dir` is a
    directory while :attr:`logs_jsonl` and :attr:`tty_transcript` are
    individual file paths. Consumers should treat the dataclass as the
    canonical surface for the FR-G4 per-eval contract rather than
    re-deriving filenames from string constants.
    """

    eval_dir: Path
    logs_jsonl: Path
    tty_transcript: Path
    artifacts_dir: Path


def compose_per_eval_dir(run_dir: Path | str, eval_id: str) -> Path:
    """Return ``<run_dir>/per-eval/<eval_id>/``.

    Validates ``eval_id`` against the FR-SCH2 character set so a
    crafted id cannot escape the per-eval subtree via path-traversal
    components.
    """

    if not isinstance(eval_id, str) or not _EVAL_ID_RE.match(eval_id):
        raise ValueError(
            f"eval_id {eval_id!r} fails the FR-SCH2 [A-Za-z0-9_.-]{{1,64}} guard"
        )
    return Path(run_dir) / PER_EVAL_DIRNAME / eval_id


def allocate_per_eval_paths(
    run_dir: Path | str,
    eval_id: str,
    *,
    create: bool = True,
) -> PerEvalPaths:
    """Return + optionally create the per-eval subtree paths.

    When ``create=True`` (the default), the per-eval directory and the
    ``artifacts/`` subdirectory are created via ``mkdir(parents=True,
    exist_ok=True)``. The :data:`LOGS_JSONL_NAME` and
    :data:`TTY_TRANSCRIPT_NAME` files are *not* touched — they are
    opened lazily by the runner / PtyDriver on first write.

    Idempotent: re-allocating an existing per-eval subtree returns the
    same paths and leaves the on-disk state intact.
    """

    eval_dir = compose_per_eval_dir(run_dir, eval_id)
    artifacts_dir = eval_dir / ARTIFACTS_SUBDIR_NAME
    paths = PerEvalPaths(
        eval_dir=eval_dir,
        logs_jsonl=eval_dir / LOGS_JSONL_NAME,
        tty_transcript=eval_dir / TTY_TRANSCRIPT_NAME,
        artifacts_dir=artifacts_dir,
    )
    if create:
        artifacts_dir.mkdir(parents=True, exist_ok=True)
    return paths


# ---------------------------------------------------------------------------
# Inverse: parse a run-dir back into (date, run-id)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RunDirComponents:
    """Parsed ``(date_segment, run_id)`` pair for a constructed run-dir."""

    date_segment: str
    run_id: str


def parse_run_dir_components(run_dir: Path | str) -> RunDirComponents:
    """Return the ``(date_segment, run_id)`` pair encoded by ``run_dir``.

    Walks the path looking for the ``.dev/eval-runs/`` prefix and takes
    the next two segments as ``(date, run-id)``. Raises
    :class:`ValueError` if the path does not match the FR-G4 layout —
    useful as a structural assertion at the seam between the CLI and
    the Reporter so a misrouted write fails loudly.
    """

    parts = Path(run_dir).parts
    # Walk back-to-front so a path like ``/.../.dev/eval-runs/<d>/<r>/...``
    # still matches even if extra segments trail after the run-id.
    eval_runs_idx: int | None = None
    for i in range(len(parts) - 1):
        if parts[i] == ".dev" and i + 1 < len(parts) and parts[i + 1] == "eval-runs":
            eval_runs_idx = i + 1
    if eval_runs_idx is None:
        raise ValueError(
            f"run_dir {run_dir!r} is not anchored at .dev/eval-runs/"
        )
    if eval_runs_idx + 2 >= len(parts):
        raise ValueError(
            f"run_dir {run_dir!r} is missing the <date>/<run-id> tail "
            "under .dev/eval-runs/"
        )
    return RunDirComponents(
        date_segment=parts[eval_runs_idx + 1],
        run_id=parts[eval_runs_idx + 2],
    )
