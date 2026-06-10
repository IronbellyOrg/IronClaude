"""AC-2 / AC-4 + fail-closed falsifiers for the bounded audit->apply->re-verify loop.

Drives the real ``ReflectRunner.run`` with the sequence-aware Idiom-B factory so
successive launches write different contracts. Asserts the EXACT call-count
arithmetic ((N+1) audits + N applies), the apply env_vars recursion marker, the
DEGRADED/BLOCKED-never-auto-fixed guard, and the failed-apply fail-closed break.
"""

from __future__ import annotations

from unittest.mock import patch

import yaml

from superclaude.cli.reflect.config import resolve_config
from superclaude.cli.reflect.models import Verdict
from superclaude.cli.reflect.runner import ReflectRunner

_PATCH_TARGET = "superclaude.cli.reflect.runner.ClaudeProcess"
_MARKER = "SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE"


def _config(tasklist, **overrides):
    params = dict(depth="standard", model="test-model")
    params.update(overrides)
    return resolve_config(str(tasklist), **params)


def _sidecar(config) -> dict:
    return yaml.safe_load(
        (config.output_dir / "wrapper-result.yaml").read_text(encoding="utf-8")
    )


def test_convergence_exit0_three_launches(
    temp_tasklist, patch_git, patch_runner_env, make_claude_process_sequence
) -> None:
    """AC-2: drift-only HALTED -> apply -> re-audit PASS. 2 audits + 1 apply = 3 launches."""
    config = _config(temp_tasklist, fix=True)
    factory = make_claude_process_sequence(
        [
            ("autofixable_drift.yaml", 0),  # audit #1 -> HALTED auto-fixable
            (None, 0),  # apply #1 (/task) -> writes no contract
            ("postfix_pass.yaml", 0),  # audit #2 -> PASS (converged)
        ]
    )
    with patch(_PATCH_TARGET, side_effect=factory) as mock_cls:
        result = ReflectRunner(config).run()
    assert result.verdict is Verdict.PASS
    assert result.verdict.exit_code == 0
    assert result.fix_converged is True
    assert result.fix_iterations == 1
    assert mock_cls.call_count == 3  # (N+1)=2 audits + N=1 apply
    # AC: the APPLY launch carries the recursion marker and a /task prompt.
    apply_kwargs = mock_cls.call_args_list[1].kwargs
    assert apply_kwargs["env_vars"] == {_MARKER: "1"}
    assert apply_kwargs["prompt"].startswith("/task ")
    # The audit launch ALSO carries the marker (contract 3.1).
    assert mock_cls.call_args_list[0].kwargs["env_vars"] == {_MARKER: "1"}
    sc = _sidecar(config)
    assert sc["fix_iterations"] == 1
    assert sc["fix_converged"] is True


def test_non_convergence_exit10_five_launches(
    temp_tasklist, patch_git, patch_runner_env, make_claude_process_sequence
) -> None:
    """AC-4: never converges with --max-fix-iterations 2 -> 3 audits + 2 applies = 5 launches."""
    config = _config(temp_tasklist, fix=True, max_fix_iterations=2)
    factory = make_claude_process_sequence(
        [
            ("autofixable_drift.yaml", 0),  # audit #1
            (None, 0),  # apply #1
            ("autofixable_drift.yaml", 0),  # audit #2 (still HALTED)
            (None, 0),  # apply #2
            ("autofixable_drift.yaml", 0),  # audit #3 -> iteration 3 > max 2 -> break
        ]
    )
    with patch(_PATCH_TARGET, side_effect=factory) as mock_cls:
        result = ReflectRunner(config).run()
    assert result.verdict is Verdict.HALTED
    assert result.verdict.exit_code == 10
    assert result.fix_converged is False
    assert result.fix_iterations == 2
    assert mock_cls.call_count == 5  # (N+1)=3 audits + N=2 applies
    sc = _sidecar(config)
    assert sc["fix_iterations"] == 2
    assert sc["fix_converged"] is False


def test_cannot_repair_absent_path_halts_no_apply(
    temp_tasklist, patch_git, patch_runner_env, make_claude_process_sequence
) -> None:
    """AUTO-FIXABLE verdict with remediation_task_path: null -> terminal HALT, no /task."""
    config = _config(temp_tasklist, fix=True)
    factory = make_claude_process_sequence([("autofixable_drift_no_path.yaml", 0)])
    with patch(_PATCH_TARGET, side_effect=factory) as mock_cls:
        result = ReflectRunner(config).run()
    assert result.verdict is Verdict.HALTED
    assert result.verdict.exit_code == 10
    assert mock_cls.call_count == 1  # one audit, NO apply
    assert result.fix_iterations == 0


def test_human_required_halts_no_apply(
    temp_tasklist, patch_git, patch_runner_env, make_claude_process_sequence
) -> None:
    """AC-3 e2e: needs_human_decision -> terminal HALT exit 10, NO /task, NO promote."""
    config = _config(temp_tasklist, fix=True)
    factory = make_claude_process_sequence([("human_required_needs_decision.yaml", 0)])
    with patch(_PATCH_TARGET, side_effect=factory) as mock_cls:
        result = ReflectRunner(config).run()
    assert result.verdict is Verdict.HALTED
    assert result.verdict.exit_code == 10
    assert mock_cls.call_count == 1
    assert result.fix_iterations == 0


def test_degraded_with_drift_never_autofixed(
    temp_tasklist, patch_git, patch_runner_env, make_claude_process_sequence
) -> None:
    """Falsifier (e): DEGRADED audit carrying drift>0 is NEVER auto-fixed (untrusted)."""
    config = _config(temp_tasklist, fix=True)
    factory = make_claude_process_sequence([("degraded_with_drift.yaml", 0)])
    with patch(_PATCH_TARGET, side_effect=factory) as mock_cls:
        result = ReflectRunner(config).run()
    assert result.verdict is Verdict.DEGRADED
    assert result.verdict.exit_code == 11
    assert result.fix_iterations == 0
    assert mock_cls.call_count == 1  # no apply launched


def test_blocked_with_drift_never_autofixed(
    temp_tasklist, patch_git, patch_runner_env, make_claude_process_sequence
) -> None:
    """Falsifier (e) parallel: BLOCKED audit carrying drift>0 is NEVER auto-fixed."""
    config = _config(temp_tasklist, fix=True)
    factory = make_claude_process_sequence([("blocked_with_drift.yaml", 0)])
    with patch(_PATCH_TARGET, side_effect=factory) as mock_cls:
        result = ReflectRunner(config).run()
    assert result.verdict is Verdict.BLOCKED
    assert result.verdict.exit_code == 2
    assert result.fix_iterations == 0
    assert mock_cls.call_count == 1  # no apply launched


def test_failed_apply_fails_closed_no_reaudit(
    temp_tasklist, patch_git, patch_runner_env, make_claude_process_sequence
) -> None:
    """Falsifier (f): a failed /task apply (rc!=0) must NOT re-audit; stays HALTED, never PASS."""
    config = _config(temp_tasklist, fix=True)
    factory = make_claude_process_sequence(
        [
            ("autofixable_drift.yaml", 0),  # audit #1 -> HALTED auto-fixable WITH path
            (None, 1),  # apply #1 fails (rc=1), writes no contract
        ]
    )
    with patch(_PATCH_TARGET, side_effect=factory) as mock_cls:
        result = ReflectRunner(config).run()
    assert result.verdict is Verdict.HALTED
    assert result.verdict.exit_code == 10  # fail-closed; NEVER exit 0 / PASS
    assert result.fix_converged is False
    assert mock_cls.call_count == 2  # exactly 1 audit + 1 apply, NO audit #2
    # The failed-apply rc is surfaced in the sidecar reason.
    sc = _sidecar(config)
    assert "fix-apply-failed" in sc["reason"]
    assert "rc=1" in sc["reason"]
