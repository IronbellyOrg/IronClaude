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
    assert suggest_alternate_model("T2Model01", env=env) == "T2Model02"


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
