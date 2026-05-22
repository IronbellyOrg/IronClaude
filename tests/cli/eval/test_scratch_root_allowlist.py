"""Tests for ``superclaude.cli.eval.config.resolve_scratch_root`` (AC12).

Covers cliEval Phase 1 / Task T01.19 acceptance criteria (Deliverable
D-0016, Roadmap R-016 / AC12). The helper is the single ingress point for
the AC12 scratch-root allowlist; it MUST reject any path that does not
resolve under ``/tmp/eval-runs``, the repo ``.dev/eval-runs`` directory,
or a CLI-supplied ``--output-dir``.

Cross-links:
* AC12 / R-016 (this task, T01.19)
* COMP-005 ``EvalConfig.allowed_scratch_roots`` (T01.01 — single source of
  truth for the allowlist)
* FR-ISO2 (T02.08) and NFR-SEC2 (T02.09) — defense-in-depth layered guards
  inside ``HomeIsolation`` that re-apply the same containment check.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.eval import (
    SCRATCH_ROOT_VIOLATION_EXIT_CODE,
    EvalConfig,
    ScratchRootViolation,
    resolve_scratch_root,
)
from superclaude.cli.eval import config as config_module


# --- exit-code mapping -----------------------------------------------------


def test_scratch_root_violation_exit_code_is_two() -> None:
    """Aligns with the loader-error trio so operators see a single exit 2."""

    assert SCRATCH_ROOT_VIOLATION_EXIT_CODE == 2


# --- positive: paths under the canonical allowlist pass --------------------


def test_accepts_path_under_tmp_eval_runs(tmp_path: Path) -> None:
    """``/tmp/eval-runs/<sub>`` is the canonical M1 scratch root."""

    target = Path("/tmp/eval-runs") / "suite-A" / "E1" / "home"
    resolved = resolve_scratch_root(target)
    assert resolved == target.resolve()


def test_resolve_scratch_root_rejects_bare_prefix() -> None:
    """Spec H4 — the bare allowlist prefix itself MUST be rejected.

    INVERTED from the prior ``test_accepts_tmp_eval_runs_root_itself`` per
    OQ-1 / Step 2.2: accepting the bare prefix made the AC12 check a
    tautology (operator could point ``--output-dir`` at the allowlist root
    and pollute it). Phase 3 Step 3.1 removes the ``resolved == prefix``
    accept branch in ``config.py``; only strict sub-paths pass.
    Until 3.1 lands, this test is EXPECTED to be RED.
    """

    with pytest.raises(ScratchRootViolation):
        resolve_scratch_root("/tmp/eval-runs")


def test_accepts_immediate_subdir_of_allowlist_root() -> None:
    """Spec H4 acceptance criterion #2 — ``/tmp/eval-runs/x`` passes.

    Positive companion to ``test_resolve_scratch_root_rejects_bare_prefix``.
    Proves strict sub-paths are still accepted after H4's ``resolved ==
    prefix`` removal. May be GREEN today (current ``is_relative_to`` already
    accepts sub-paths) and MUST remain GREEN after Phase 3 Step 3.1.
    """

    target = Path("/tmp/eval-runs/x")
    resolved = resolve_scratch_root(target)
    assert resolved == target.resolve()


def test_accepts_path_under_dev_eval_runs(tmp_path: Path) -> None:
    """Repo-relative ``.dev/eval-runs`` resolves against process CWD."""

    repo_relative = Path(".dev/eval-runs") / "suite-A" / "E1"
    resolved = resolve_scratch_root(repo_relative)
    assert resolved == repo_relative.resolve()


# --- positive: --output-dir extends the allowlist for the call only -------


def test_accepts_path_under_output_dir(tmp_path: Path) -> None:
    """A CLI-supplied ``--output-dir`` is added to the allowlist for the call."""

    output_dir = tmp_path / "custom-out"
    target = output_dir / "suite-A" / "E1"
    resolved = resolve_scratch_root(target, output_dir=output_dir)
    assert resolved == target.resolve()


def test_output_dir_is_call_scoped_not_persistent(tmp_path: Path) -> None:
    """Passing ``output_dir`` once must not leak into later calls."""

    output_dir = tmp_path / "custom-out"
    resolve_scratch_root(output_dir / "ok", output_dir=output_dir)

    with pytest.raises(ScratchRootViolation):
        resolve_scratch_root(output_dir / "later")


# --- negative: non-allowlisted prefixes are rejected ----------------------


@pytest.mark.parametrize(
    "candidate",
    [
        "/home/user/foo",
        "/var/lib/eval-runs",
        "/etc/passwd",
        "/root/.claude",
        "/usr/local/share",
        "/tmp/other-runs",  # close-but-not-quite prefix
    ],
)
def test_rejects_non_allowlisted_paths(candidate: str) -> None:
    """Every non-allowlisted prefix must raise ``ScratchRootViolation``."""

    with pytest.raises(ScratchRootViolation) as excinfo:
        resolve_scratch_root(candidate)

    err = excinfo.value
    assert err.path == Path(candidate)
    assert err.resolved == Path(candidate).expanduser().resolve(strict=False)
    # The resolved allowlist used for the check is recorded so doctor /
    # reporter callers can render it verbatim.
    assert err.allowed
    assert Path("/tmp/eval-runs").resolve() in err.allowed


def test_violation_message_includes_offending_path() -> None:
    """Forensic detail must survive into the exception message."""

    with pytest.raises(ScratchRootViolation) as excinfo:
        resolve_scratch_root("/home/user/foo")

    rendered = str(excinfo.value)
    assert "/home/user/foo" in rendered
    assert "AC12" in rendered


# --- allowlist sourcing: no module hard-codes a copy -----------------------


def test_allowlist_source_is_evalconfig(monkeypatch: pytest.MonkeyPatch) -> None:
    """Helper must read the allowlist from the supplied EvalConfig only.

    Mutating ``EvalConfig.allowed_scratch_roots`` (via a fresh instance)
    must change which paths pass — proving the function does not embed a
    second hard-coded copy of the allowlist.
    """

    sole_root = Path("/tmp/custom-eval-roots")
    config = EvalConfig(allowed_scratch_roots=(sole_root,))

    # Default allowlist would have accepted this; the narrowed config rejects.
    with pytest.raises(ScratchRootViolation):
        resolve_scratch_root("/tmp/eval-runs/foo", config=config)

    # And the narrowed allowlist accepts a path under its single entry.
    resolved = resolve_scratch_root(sole_root / "x", config=config)
    assert resolved == (sole_root / "x").resolve()


def test_default_config_yields_canonical_allowlist() -> None:
    """``EvalConfig()`` defaults are the M1 canonical allowlist (no drift)."""

    config = EvalConfig()
    assert Path("/tmp/eval-runs") in config.allowed_scratch_roots
    assert Path(".dev/eval-runs") in config.allowed_scratch_roots


# --- internals: ergonomics + resolution semantics --------------------------


def test_accepts_str_path_input() -> None:
    """``str`` ergonomics: callers should not have to wrap in ``Path``."""

    resolved = resolve_scratch_root("/tmp/eval-runs/sub")
    assert isinstance(resolved, Path)
    assert resolved == Path("/tmp/eval-runs/sub").resolve()


def test_relative_path_segments_cannot_escape(tmp_path: Path) -> None:
    """Resolution must collapse ``..`` so traversal cannot bypass the check."""

    # Construct a path that textually contains ``/tmp/eval-runs`` but
    # resolves OUTSIDE the allowlist via ``..`` traversal.
    escaping = Path("/tmp/eval-runs/../etc/passwd")
    with pytest.raises(ScratchRootViolation):
        resolve_scratch_root(escaping)


def test_uses_expanduser_for_home_anchors() -> None:
    """``~``-prefixed paths must be expanded before allowlist comparison."""

    # ``~`` resolves to the real $HOME, which is never on the AC12 list.
    with pytest.raises(ScratchRootViolation):
        resolve_scratch_root("~/eval-runs/foo")


def test_resolve_prefix_helper_handles_relative_and_absolute(tmp_path: Path) -> None:
    """The internal prefix resolver must accept relative + absolute inputs."""

    assert config_module._resolve_prefix(Path("/tmp/eval-runs")) == Path(
        "/tmp/eval-runs"
    ).resolve()
    assert config_module._resolve_prefix(Path(".dev/eval-runs")) == Path(
        ".dev/eval-runs"
    ).resolve()
