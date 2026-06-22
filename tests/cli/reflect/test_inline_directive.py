"""Tests for the FR-INLINE execution directive appended by ``_build_prompt``.

The reflect runner appends a natural-language directive instructing the headless
``claude --print`` agent to run the reflect protocol INLINE (top-level) rather than
delegating the whole run into a worker subagent (which would degrade Tier-2 review to a
single-reviewer fallback). These tests assert the directive is present, appended exactly
once, ends the prompt, and carries its load-bearing phrases -- so the test fails if the
directive is removed or doubled.

The directive is best-effort defense-in-depth; the STRUCTURAL enforcement is EV-1 (the
Wave-4 ORCHESTRATOR-VERIFIES-ON-DISK adversarial-merge gate in sc-reflect 1.5.1).
"""

from __future__ import annotations

from superclaude.cli.reflect.config import resolve_config
from superclaude.cli.reflect.runner import ReflectRunner

# The verbatim opener and closer of the inline directive in runner.py._build_prompt.
_DIRECTIVE_OPENER = "Execute this reflect run INLINE"
_DIRECTIVE_CLOSER = "degrade to a single-reviewer fallback."


def _config(tasklist, **overrides):
    params = dict(depth="standard", model="test-model")
    params.update(overrides)
    return resolve_config(str(tasklist), **params)


def test_inline_directive_present_with_load_bearing_phrases(
    temp_tasklist, patch_git
) -> None:
    """The built prompt contains the directive's load-bearing phrases."""
    prompt = ReflectRunner(_config(temp_tasklist))._build_prompt()
    assert "INLINE" in prompt
    assert "Do NOT delegate" in prompt
    assert ("Wave 3" in prompt) or ("Wave 4" in prompt)


def test_inline_directive_appended_exactly_once(temp_tasklist, patch_git) -> None:
    """The directive is appended exactly once (fails if doubled)."""
    prompt = ReflectRunner(_config(temp_tasklist))._build_prompt()
    assert prompt.count(_DIRECTIVE_OPENER) == 1
    assert prompt.count(_DIRECTIVE_CLOSER) == 1


def test_inline_directive_ends_the_prompt(temp_tasklist, patch_git) -> None:
    """The directive is the tail of the prompt (fails if removed)."""
    prompt = ReflectRunner(_config(temp_tasklist))._build_prompt()
    assert prompt.rstrip().endswith(_DIRECTIVE_CLOSER)
