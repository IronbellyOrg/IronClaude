"""Unit tests for the P5 ``~/.aienv`` model-alias suggester (429 recovery).

All tests inject the alias environment via the ``env=`` seam of
:func:`suggest_alternate_model` (option A, os.environ reader) so a unit run never
reads the real ``~/.aienv``. The cooldown body embeds the *resolved* model
(e.g. ``claude-opus-4-8``), so the suggester must match against the resolved id
as well as the short alias, and must be None-safe (never fabricate an alias).
"""

from __future__ import annotations

import pytest

from superclaude.cli.sprint.aienv import suggest_alternate_model


@pytest.mark.unit
def test_suggest_alternate_for_opus_resolved_model_returns_sonnet():
    env = {
        "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-4-8",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-5",
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "claude-haiku-4-5",
    }
    # Matched by the resolved model id (what the cooldown body carries).
    assert suggest_alternate_model("claude-opus-4-8", env=env) == "sonnet"


@pytest.mark.unit
def test_suggest_alternate_for_opus_alias_returns_sonnet():
    env = {
        "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-4-8",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-5",
    }
    # Matched by the short alias as well.
    assert suggest_alternate_model("opus", env=env) == "sonnet"


@pytest.mark.unit
def test_suggest_alternate_for_proxy_slot_returns_next_slot():
    env = {
        "T2Model01": "qwen3.6-plus",
        "T2Model02": "glm-4.6",
    }
    # The suggestion is passed to ``claude --model``, so it is the model id.
    assert suggest_alternate_model("T2Model01", env=env) == "glm-4.6"
    assert suggest_alternate_model("qwen3.6-plus", env=env) == "glm-4.6"


@pytest.mark.unit
def test_no_alternate_returns_none_safe():
    # Only one slot present → no distinct alternate → None (never fabricate).
    env = {"ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-4-8"}
    assert suggest_alternate_model("claude-opus-4-8", env=env) is None


@pytest.mark.unit
def test_unknown_model_returns_none():
    env = {
        "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-4-8",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-5",
    }
    # A model not present in the alias set has no defined rotation → None.
    assert suggest_alternate_model("some-unconfigured-model", env=env) is None


@pytest.mark.unit
def test_identical_resolved_model_is_not_suggested():
    # opus and sonnet resolve to the SAME model → no DISTINCT alternate → None
    # (suggesting the same model under a second alias would not re-route).
    env = {
        "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-4-8",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-opus-4-8",
    }
    assert suggest_alternate_model("claude-opus-4-8", env=env) is None


@pytest.mark.unit
def test_coder_tier2_rotation_suggests_the_next_model_id():
    """Coder env after the tier change: Muse first, then Grok (Tier 2)."""
    env = {
        "T2Model01": "muse-spark-1.3",
        "T2Model01_WINDOW": "950000",
        "T2_WINDOW": "500000",
        "T2Model02": "grok-4.7",
        "T2Model02_WINDOW": "500000",
    }
    assert suggest_alternate_model("muse-spark-1.3", env=env) == "grok-4.7"
    # Window lines are never read as model slots.
    assert suggest_alternate_model("950000", env=env) is None


@pytest.mark.unit
def test_without_anthropic_slots_the_builtin_aliases_rotate():
    """Coder #270 removes ANTHROPIC_DEFAULT_*: fall back to Claude Code's aliases."""
    env = {"T2Model01": "muse-spark-1.3"}
    assert suggest_alternate_model("opus", env=env) == "sonnet"
    assert suggest_alternate_model("haiku", env=env) == "muse-spark-1.3"
