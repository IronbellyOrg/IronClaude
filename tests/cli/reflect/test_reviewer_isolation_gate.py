"""L2 reviewer-isolation snapshot gate — STOP-on-dirty / snapshot grounding / teardown.

Exercises the gate via the opt-in (``isolate_reviewers=True``), per the pinned
flag-gated stance (the default flag-off path is covered by the existing e2e
suite and must NOT snapshot or STOP). Asserts on EMITTED telemetry +
construction kwargs (TST-3: never transcript scraping):

1. dirty/uncommitted target -> ``status == "stopped-precondition"``, exit 2,
   ``reviewer_isolation == "stopped-precondition"``, and NO reviewer fan-out
   (``ClaudeProcess`` never constructed).
2. clean committable target -> a snapshot is created, the Tier-1 child is grounded
   in ``<output>/_review-snapshot`` (via the ``cwd`` kwarg), and the emitted
   ``reviewer_grounding_root`` telemetry points at the snapshot, NOT the live tree.
3. finally-teardown -> the snapshot is torn down even when the audit loop raises.

Falsifier discipline: fails-before (no gate / no telemetry / no snapshot) and
passes-after (L2 landed).
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from superclaude.cli.reflect.config import resolve_config
from superclaude.cli.reflect.models import Verdict
from superclaude.cli.reflect.runner import ReflectRunner

_CP = "superclaude.cli.reflect.runner.ClaudeProcess"
_CREATE = "superclaude.cli.reflect.runner.create_review_snapshot"
_TEARDOWN = "superclaude.cli.reflect.runner.teardown_review_snapshot"


def _config(tasklist, **overrides):
    params = dict(depth="standard", model="test-model", isolate_reviewers=True)
    params.update(overrides)
    return resolve_config(str(tasklist), **params)


def test_dirty_uncommitted_target_stops_with_no_fanout(
    temp_tasklist, patch_git, patch_runner_env, make_claude_process_stub
) -> None:
    """Case 1: a dirty audit target STOPs before any reviewer launches."""
    config = _config(temp_tasklist)
    config.audit_tree_dirty = True  # force the COR-1 dirty STOP
    factory = make_claude_process_stub("pass.yaml", rc=0)
    with (
        patch(_CP, side_effect=factory) as mock_cls,
        patch(_CREATE) as mock_create,
    ):
        result = ReflectRunner(config).run()
    assert result.status == "stopped-precondition"
    assert result.verdict is Verdict.BLOCKED
    assert result.verdict.exit_code == 2
    assert result.reason == "dirty"
    assert result.reviewer_isolation == "stopped-precondition"
    # No reviewer fan-out AND no snapshot was even attempted on the dirty STOP.
    mock_cls.assert_not_called()
    mock_create.assert_not_called()


def test_clean_committable_grounds_reviewers_in_snapshot(
    temp_tasklist, patch_git, patch_runner_env, make_claude_process_stub
) -> None:
    """Case 2: a clean committable target snapshots and grounds reviewers in it."""
    config = _config(temp_tasklist)
    config.audit_tree_dirty = False
    snapshot = config.output_dir / "_review-snapshot"
    factory = make_claude_process_stub("pass.yaml", rc=0)
    with (
        patch(_CP, side_effect=factory) as mock_cls,
        patch(_CREATE, return_value=(snapshot, None)) as mock_create,
        patch(_TEARDOWN) as mock_teardown,
    ):
        result = ReflectRunner(config).run()
    mock_create.assert_called_once()
    # The Tier-1 audit child is grounded in the snapshot, NOT the live worktree.
    assert mock_cls.call_args.kwargs.get("cwd") == snapshot
    assert snapshot != config.tasklist_path.parent
    assert snapshot.name == "_review-snapshot"
    # Emitted telemetry points at the snapshot. The honest value is
    # "snapshot-children-only" (D1 fix): only the ClaudeProcess children are
    # snapshot-grounded; the swarm workers still read the live path.
    assert result.reviewer_isolation == "snapshot-children-only"
    assert result.reviewer_grounding_root == str(snapshot)
    # Teardown always runs (finally).
    mock_teardown.assert_called_once()


def test_snapshot_torn_down_when_audit_loop_raises(
    temp_tasklist, patch_git, patch_runner_env
) -> None:
    """Case 3: the finally teardown removes the snapshot even on an exception."""
    config = _config(temp_tasklist)
    config.audit_tree_dirty = False
    snapshot = config.output_dir / "_review-snapshot"
    boom = MagicMock(side_effect=RuntimeError("audit blew up"))
    with (
        patch(_CREATE, return_value=(snapshot, None)),
        patch(_TEARDOWN) as mock_teardown,
        patch.object(ReflectRunner, "_audit_once", boom),
    ):
        with pytest.raises(RuntimeError, match="audit blew up"):
            ReflectRunner(config).run()
    # The finally teardown ran despite the loop raising.
    mock_teardown.assert_called_once()
    assert mock_teardown.call_args.args[1] == snapshot


def test_stop_reason_propagates_from_snapshot_helper(
    temp_tasklist, patch_git, patch_runner_env, make_claude_process_stub
) -> None:
    """A snapshot-helper STOP (e.g. head-moved) surfaces as stopped-precondition."""
    config = _config(temp_tasklist)
    config.audit_tree_dirty = False
    factory = make_claude_process_stub("pass.yaml", rc=0)
    with (
        patch(_CP, side_effect=factory) as mock_cls,
        patch(_CREATE, return_value=(None, "head-moved-precondition")),
    ):
        result = ReflectRunner(config).run()
    assert result.status == "stopped-precondition"
    assert result.reason == "head-moved-precondition"
    assert result.verdict.exit_code == 2
    assert result.reviewer_isolation == "stopped-precondition"
    mock_cls.assert_not_called()
