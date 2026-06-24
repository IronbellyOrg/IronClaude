"""L1b restricted-profile guard — reflect REVIEW children launch restricted.

Asserts on CONSTRUCTION KWARGS / ``build_command()`` output (TST-3: telemetry
over transcript-scraping), never on a child transcript:

- the Tier-1 grounded-audit child (``runner._audit_once``) is constructed with
  ``reviewer_profile=True``;
- the Mode-A adversarial scorer (``ensemble.run_adversarial_scorer``) is likewise
  restricted;
- the remediation executor (``runner._apply_remediation``) is NOT restricted
  (it must retain write tools to apply fixes);
- the two-sided ``build_command()`` falsifier: the restricted profile OMITS
  ``--tools default`` and ``--dangerously-skip-permissions`` while the default
  profile still EMITS both (proving no regression for non-reflect callers).

Falsifier discipline: fails-before (``build_command()`` emitted both tokens
unconditionally; no ``reviewer_profile`` kwarg existed) and passes-after (L1b
design (a) landed).
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from superclaude.cli.pipeline.process import ClaudeProcess
from superclaude.cli.reflect.config import resolve_config
from superclaude.cli.reflect.ensemble import run_adversarial_scorer
from superclaude.cli.reflect.runner import ReflectRunner

_RUNNER_PATCH = "superclaude.cli.reflect.runner.ClaudeProcess"
_ENSEMBLE_PATCH = "superclaude.cli.reflect.ensemble.ClaudeProcess"


def _config(tasklist, **overrides):
    params = dict(depth="standard", model="test-model")
    params.update(overrides)
    return resolve_config(str(tasklist), **params)


# --- (a) Tier-1 grounded-audit child is restricted ------------------------


def test_tier1_audit_child_is_restricted(
    temp_tasklist, patch_git, patch_runner_env, make_claude_process_stub
) -> None:
    config = _config(temp_tasklist)
    factory = make_claude_process_stub("pass.yaml", rc=0)
    with patch(_RUNNER_PATCH, side_effect=factory) as mock_cls:
        ReflectRunner(config).run()
    mock_cls.assert_called_once()
    assert mock_cls.call_args.kwargs.get("reviewer_profile") is True, (
        "Tier-1 audit child must be launched with reviewer_profile=True (L1b)"
    )


# --- (b) Mode-A adversarial scorer is restricted --------------------------


def test_adversarial_scorer_is_restricted(
    temp_tasklist, patch_git, make_claude_process_stub, tmp_path
) -> None:
    config = _config(temp_tasklist)
    output_dir = tmp_path / "adv"
    # rc=1 short-circuits run_adversarial_scorer to return None right after the
    # ClaudeProcess construction (which is all we assert on).
    factory = make_claude_process_stub(None, rc=1, write_contract=False)
    with patch(_ENSEMBLE_PATCH, side_effect=factory) as mock_cls:
        run_adversarial_scorer([], output_dir, config=config)
    mock_cls.assert_called_once()
    assert mock_cls.call_args.kwargs.get("reviewer_profile") is True, (
        "adversarial scorer must be launched with reviewer_profile=True (L1b)"
    )


# --- (c) Remediation executor is NOT restricted ---------------------------


def test_remediation_executor_is_not_restricted(
    temp_tasklist, patch_git, patch_runner_env, make_claude_process_stub
) -> None:
    config = _config(temp_tasklist)
    factory = make_claude_process_stub(None, rc=0, write_contract=False)
    with patch(_RUNNER_PATCH, side_effect=factory) as mock_cls:
        ReflectRunner(config)._apply_remediation("/tmp/remediation-task.md", 1)
    mock_cls.assert_called_once()
    # The remediation executor must retain write tools — it must NOT be restricted.
    assert mock_cls.call_args.kwargs.get("reviewer_profile", False) is False, (
        "remediation executor must NOT be restricted (it applies fixes)"
    )


# --- (d) Two-sided build_command falsifier --------------------------------


def _common_kwargs(tmp_path):
    return dict(
        prompt="x",
        output_file=tmp_path / "o.json",
        error_file=tmp_path / "e.log",
        model="m1",
    )


def test_build_command_restricted_omits_tools_and_skip_permissions(tmp_path) -> None:
    cmd = ClaudeProcess(
        **_common_kwargs(tmp_path), reviewer_profile=True
    ).build_command()
    assert "--dangerously-skip-permissions" not in cmd
    assert "--tools" not in cmd
    assert "default" not in cmd
    # --no-session-persistence is KEPT in the restricted profile.
    assert "--no-session-persistence" in cmd


def test_build_command_default_still_emits_tools_and_skip_permissions(tmp_path) -> None:
    cmd = ClaudeProcess(**_common_kwargs(tmp_path)).build_command()
    # Default profile (all existing non-reflect callers) is byte-identical: it
    # MUST still emit both tokens — the no-regression half of the falsifier.
    assert cmd == [
        "claude",
        "--print",
        "--verbose",
        "--dangerously-skip-permissions",
        "--no-session-persistence",
        "--tools",
        "default",
        "--max-turns",
        "100",
        "--output-format",
        "stream-json",
        "--model",
        "m1",
    ]
