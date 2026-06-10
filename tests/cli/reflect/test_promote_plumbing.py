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
