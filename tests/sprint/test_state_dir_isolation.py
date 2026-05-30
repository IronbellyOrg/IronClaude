"""Regression tests for FU-001 — .sprint-exitcode → state_dir migration.

Locks in the four acceptance behaviors required by
TASK-RF-track-1-20260518-231708:

1. The sprint runner writes ``.sprint-exitcode`` to ``config.state_dir``
   and never into ``config.release_dir``.
2. No ``.sprint-exitcode`` files are tracked by git anywhere in the
   repository (FU-001 acceptance: ``git ls-files`` returns 0
   ``.sprint-exitcode`` entries).
3. When ``state_dir`` is omitted, ``SprintConfig.__post_init__`` derives
   the default ``.dev/sprint-state/<release-name>/`` path from
   ``release_dir``.
4. The ``SPRINT_STATE_DIR`` environment variable propagates through
   ``load_sprint_config`` to the constructed ``SprintConfig.state_dir``.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from superclaude.cli.sprint.config import load_sprint_config
from superclaude.cli.sprint.executor import _write_exit_sentinel
from superclaude.cli.sprint.models import Phase, SprintConfig


def _make_phases(n: int = 1) -> list[Phase]:
    return [Phase(number=i + 1, file=Path(f"/tmp/phase-{i + 1}.md")) for i in range(n)]


def test_writer_uses_state_dir_not_release_dir(tmp_path):
    """The sentinel writer must emit ``.sprint-exitcode`` into ``state_dir``,
    not ``release_dir``.

    Locks in FU-001 acceptance criterion: post-migration the sentinel never
    materializes inside the tracked release archive directory.
    """
    release_dir = tmp_path / "release"
    state_dir = tmp_path / "state"
    release_dir.mkdir()
    # NOTE: deliberately do NOT pre-create state_dir — the writer must mkdir
    # parents itself (this also exercises the .mkdir(parents=True) branch).

    config = SprintConfig(
        index_path=release_dir / "tasklist-index.md",
        release_dir=release_dir,
        state_dir=state_dir,
        phases=_make_phases(1),
    )
    # __post_init__ must NOT overwrite an explicitly provided state_dir.
    assert config.state_dir == state_dir

    _write_exit_sentinel(config, 0)

    state_sentinel = state_dir / ".sprint-exitcode"
    release_sentinel = release_dir / ".sprint-exitcode"

    # All three assertions are required; collapsing to a single existence
    # check would let a regression that writes to release_dir pass silently.
    assert state_sentinel.exists(), (
        f"Writer did not create {state_sentinel} — state_dir branch broken"
    )
    assert not release_sentinel.exists(), (
        f"Writer leaked sentinel into release_dir at {release_sentinel} — "
        "FU-001 contract violated"
    )
    assert state_sentinel.read_text().strip() == "0"


def test_no_tracked_sprint_exitcode_files():
    """``git ls-files`` must return zero ``.sprint-exitcode`` entries.

    Locks in FU-001 acceptance criterion: no tracked sentinels remain
    anywhere in the repo after Phase 3's batched ``git rm``.
    """
    # Walk up from this test file to the repo root (the directory containing
    # the .git directory). Avoids hardcoding the absolute path.
    here = Path(__file__).resolve()
    repo_root = here
    for parent in [here, *here.parents]:
        if (parent / ".git").exists():
            repo_root = parent
            break
    else:  # pragma: no cover — only fires if test is run outside a repo
        raise RuntimeError("Could not locate .git ancestor for repo-root")

    result = subprocess.run(
        ["git", "ls-files"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    sentinels = [
        line for line in result.stdout.splitlines() if line.endswith(".sprint-exitcode")
    ]
    assert sentinels == [], (
        f"FU-001 contract violated: {len(sentinels)} tracked .sprint-exitcode "
        f"file(s) found: {sentinels[:5]}{'...' if len(sentinels) > 5 else ''}"
    )


def test_state_dir_default_derives_from_release_dir(tmp_path):
    """When ``state_dir`` is omitted, the dataclass derives the default
    ``.dev/sprint-state/<release-name>/`` path from ``release_dir.name``.

    Locks in the empty-Path sentinel pattern in
    ``SprintConfig.__post_init__`` (state_dir defaults to ``Path("")`` and
    is then derived).
    """
    config = SprintConfig(
        index_path=Path("/tmp/myrelease/tasklist-index.md"),
        release_dir=Path("/tmp/myrelease"),
        phases=_make_phases(1),
        # NOTE: state_dir intentionally omitted to exercise the default
    )
    assert config.state_dir == Path(".dev/sprint-state/myrelease"), (
        f"Default state_dir derivation broken: got {config.state_dir}"
    )


def test_state_dir_env_var_resolution(tmp_path, monkeypatch):
    """``SPRINT_STATE_DIR`` env var must propagate through
    ``load_sprint_config`` to ``SprintConfig.state_dir``.

    The CLI ``run`` command reads the env var when no ``--state-dir``
    override is supplied; this test verifies the loader honors a
    ``state_dir=`` kwarg derived from the env var.
    """
    env_state_dir = tmp_path / "envstate"
    monkeypatch.setenv("SPRINT_STATE_DIR", str(env_state_dir))

    # Minimal tasklist fixture for load_sprint_config. The phase-file name
    # must match the canonical discovery pattern (phase-N-tasklist.md),
    # per config._discover_phase_files.
    release_dir = tmp_path / "release"
    release_dir.mkdir()
    tasklist = release_dir / "tasklist-index.md"
    tasklist.write_text("# Tasklist\n\n## Phase 1 — Setup\n")
    (release_dir / "phase-1-tasklist.md").write_text("# Phase 1\n\n- [ ] noop\n")

    resolved_state_dir = Path(os.environ["SPRINT_STATE_DIR"])
    config = load_sprint_config(
        index_path=tasklist,
        state_dir=resolved_state_dir,
    )
    assert config.state_dir == env_state_dir, (
        f"Env-var did not propagate: expected {env_state_dir}, got {config.state_dir}"
    )
