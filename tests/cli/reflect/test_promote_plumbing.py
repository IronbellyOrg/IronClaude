"""AC-5: O1 promote (default) vs O2 --no-promote prompt plumbing.

The wrapper plumbs the promote flag into the `/sc:reflect` prompt (`--no-promote`
emitted only when promote is off). The actual task-adapter directory move is
reflect-internal Wave 7, NOT re-implemented in the wrapper (contract Section 5) --
so these assert the prompt STRING + sidecar promote plumbing, not a dir move.
"""

from __future__ import annotations

from superclaude.cli.reflect.commands import reflect_group
from superclaude.cli.reflect.config import resolve_config
from superclaude.cli.reflect.runner import ReflectRunner


def _config(tasklist, **overrides):
    params = dict(depth="standard", model="test-model")
    params.update(overrides)
    return resolve_config(str(tasklist), **params)


def test_o1_default_prompt_omits_no_promote(temp_tasklist, patch_git) -> None:
    """O1: bare run (promote default True) -> prompt does NOT contain --no-promote."""
    config = _config(temp_tasklist, promote=True)
    prompt = ReflectRunner(config)._build_prompt()
    assert "--no-promote" not in prompt
    assert config.promote is True


def test_o2_no_promote_prompt_contains_no_promote(temp_tasklist, patch_git) -> None:
    """O2: run --no-promote -> prompt DOES contain --no-promote."""
    config = _config(temp_tasklist, promote=False)
    prompt = ReflectRunner(config)._build_prompt()
    assert "--no-promote" in prompt
    assert config.promote is False


def test_default_promote_is_on_regression_guard(
    temp_tasklist, patch_git, cli_runner
) -> None:
    """FR-5 regression guard: the bare `run <file>` CLI default is promote-on.

    Exercised via --print-command so no launch occurs; the printed prompt must
    NOT carry --no-promote when no promote flag is passed (default flip to True).
    """
    result = cli_runner.invoke(
        reflect_group,
        ["run", str(temp_tasklist), "--print-command"],
    )
    assert result.exit_code == 0
    assert "/sc:reflect --mode post" in result.output
    assert "--no-promote" not in result.output


def test_default_prompt_omits_no_reachability(temp_tasklist, patch_git) -> None:
    """FR-RH1: bare run (reachability default True) -> prompt omits --no-reachability."""
    config = _config(temp_tasklist)
    assert config.reachability is True
    prompt = ReflectRunner(config)._build_prompt()
    assert "--no-reachability" not in prompt


def test_no_reachability_prompt_contains_it_exactly_once(
    temp_tasklist, patch_git
) -> None:
    """FR-RH1: reachability=False -> prompt contains --no-reachability exactly once."""
    config = _config(temp_tasklist, reachability=False)
    assert config.reachability is False
    prompt = ReflectRunner(config)._build_prompt()
    assert prompt.split().count("--no-reachability") == 1


def test_cli_default_print_command_omits_no_reachability(
    temp_tasklist, patch_git, cli_runner
) -> None:
    """FR-RH1: bare CLI run --print-command (default-on) omits --no-reachability."""
    result = cli_runner.invoke(
        reflect_group, ["run", str(temp_tasklist), "--print-command"]
    )
    assert result.exit_code == 0
    assert "--no-reachability" not in result.output


def test_cli_no_reachability_print_command_emits_it(
    temp_tasklist, patch_git, cli_runner
) -> None:
    """FR-RH1: CLI run --no-reachability --print-command forwards --no-reachability."""
    result = cli_runner.invoke(
        reflect_group,
        ["run", str(temp_tasklist), "--no-reachability", "--print-command"],
    )
    assert result.exit_code == 0
    assert "--no-reachability" in result.output


def test_tmux_inner_command_forwards_disabled_reachability(
    temp_tasklist, patch_git
) -> None:
    """FR-RH1: --tmux --no-reachability -> the inner foreground reflect run carries
    --no-reachability exactly once so the gate is not silently re-enabled."""
    from superclaude.cli.reflect.commands import _build_inner_command

    enabled = _config(temp_tasklist, reachability=True)
    assert "--no-reachability" not in _build_inner_command(enabled)

    disabled = _config(temp_tasklist, reachability=False)
    assert _build_inner_command(disabled).count("--no-reachability") == 1


def test_runner_forwards_promoting_into_derive_verdict(
    temp_tasklist, patch_git, patch_runner_env, make_claude_process_stub, monkeypatch
) -> None:
    """P1 promote plumbing: the single derive_verdict call site forwards
    ``promoting=config.promote`` (not a hardcoded default). Spies on derive_verdict,
    delegating to the real impl, and asserts the captured ``promoting`` kwarg matches
    ``config.promote`` for both promote=True and promote=False.

    RED pre-fix: the call site does not pass ``promoting`` -> the spy captures ``None``
    (assertion fails), OR ``derive_verdict`` has no ``promoting`` param yet (TypeError).
    """
    from unittest.mock import patch

    import superclaude.cli.reflect.runner as runner_mod
    from superclaude.cli.reflect.contract import derive_verdict as real_derive_verdict

    captured: dict = {}

    def _spy(contract, **kwargs):
        captured["promoting"] = kwargs.get("promoting")
        return real_derive_verdict(contract, **kwargs)

    monkeypatch.setattr(runner_mod, "derive_verdict", _spy)

    # promote=True -> the call site must forward promoting=True.
    config = _config(temp_tasklist, promote=True)
    factory = make_claude_process_stub("pass.yaml", rc=0)
    with patch("superclaude.cli.reflect.runner.ClaudeProcess", side_effect=factory):
        ReflectRunner(config).run()
    assert captured["promoting"] is True

    # promote=False -> the call site must forward promoting=False (not a hardcoded True).
    captured.clear()
    config2 = _config(temp_tasklist, promote=False)
    factory2 = make_claude_process_stub("pass.yaml", rc=0)
    with patch("superclaude.cli.reflect.runner.ClaudeProcess", side_effect=factory2):
        ReflectRunner(config2).run()
    assert captured["promoting"] is False
