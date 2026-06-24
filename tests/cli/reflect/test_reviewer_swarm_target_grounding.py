"""D1 fix (design b) — telemetry-honesty: ``reviewer_isolation`` must not overclaim.

The /sc:reflect post-execution audit (D1, MEDIUM-HIGH Drift) found that with
``--isolate-reviewers`` ON, only the two ``ClaudeProcess`` children (the Tier-1
audit child and the adversarial scorer) are actually snapshot-``cwd``-grounded,
while the text-in/out Tier-2 swarm workers' review target is still the LIVE
``config.tasklist_path``. Yet the emitted ``reviewer_isolation`` reported the
unqualified ``"snapshot"`` — an overclaim.

Design (b) (telemetry-honesty narrowing) introduces the value
``"snapshot-children-only"``: emitted on the snapshot-success path to truthfully
say "the ClaudeProcess children are grounded in the snapshot; the swarm workers
are not." This test asserts the operator-visible ``ReflectResult.reviewer_isolation``
(written at ``runner.py:682``) is that honest value on the clean-committable path,
while confirming the two children ARE still grounded (the value is honest, not a
regression of grounding).

Falsifier discipline (NOT exempt): this asserts the POST-fix value, so on the
pre-fix tree — where the runner emits the unqualified ``"snapshot"`` — the test
FAILS. After the design-(b) edits land it PASSES. The fail-before baseline is
captured at ``phase-outputs/test-results/d1-failbefore.txt``.
"""

from __future__ import annotations

from unittest.mock import patch

from superclaude.cli.reflect.config import resolve_config
from superclaude.cli.reflect.runner import ReflectRunner

_CP = "superclaude.cli.reflect.runner.ClaudeProcess"
_CREATE = "superclaude.cli.reflect.runner.create_review_snapshot"
_TEARDOWN = "superclaude.cli.reflect.runner.teardown_review_snapshot"


def _config(tasklist, **overrides):
    params = dict(depth="standard", model="test-model", isolate_reviewers=True)
    params.update(overrides)
    return resolve_config(str(tasklist), **params)


def test_snapshot_success_reports_children_only_not_full_snapshot(
    temp_tasklist, patch_git, patch_runner_env, make_claude_process_stub
) -> None:
    """The honest value is emitted: children grounded, swarm workers not.

    Mirrors ``test_reviewer_isolation_gate::test_clean_committable_grounds_reviewers_in_snapshot``
    but asserts the design-(b) honest telemetry value ``"snapshot-children-only"``
    instead of the overclaiming ``"snapshot"``. FAILS on the pre-fix tree.
    """
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
    # The two ClaudeProcess children ARE still grounded in the snapshot — the
    # honest value reflects partial isolation, it does NOT remove grounding.
    assert mock_cls.call_args.kwargs.get("cwd") == snapshot
    mock_teardown.assert_called_once()

    # The operator-visible telemetry must NOT overclaim full snapshot isolation.
    assert result.reviewer_isolation == "snapshot-children-only", (
        "reviewer_isolation must report the honest 'snapshot-children-only' on the "
        "snapshot path (only the ClaudeProcess children are grounded; the text-in/out "
        f"swarm workers read the live tasklist path), got {result.reviewer_isolation!r}"
    )
    assert result.reviewer_isolation != "snapshot", (
        "the unqualified 'snapshot' is the D1 overclaim and must no longer be emitted "
        "when the swarm-worker target is still the live path"
    )
    # The grounding-root telemetry still points at the snapshot (children are there).
    assert result.reviewer_grounding_root == str(snapshot)


def test_disabled_path_unchanged_when_isolation_off(
    temp_tasklist, patch_git, patch_runner_env, make_claude_process_stub
) -> None:
    """Default-OFF is untouched: no snapshot, telemetry stays ``"disabled"``.

    Guards against the design-(b) edit leaking the new value onto the flag-off
    (#153) path. Falsifier-relevant only as a regression guard; it passes both
    before and after the fix because the default path never changes.
    """
    config = _config(temp_tasklist, isolate_reviewers=False)
    factory = make_claude_process_stub("pass.yaml", rc=0)
    with (
        patch(_CP, side_effect=factory),
        patch(_CREATE) as mock_create,
    ):
        result = ReflectRunner(config).run()
    # Flag-off path never probes/snapshots and reports the unchanged disabled value.
    mock_create.assert_not_called()
    assert result.reviewer_isolation == "disabled"
    assert result.reviewer_grounding_root is None
