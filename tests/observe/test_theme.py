"""Colour roles: every role exists at every depth, the 16-colour floor keeps its roles apart."""

from __future__ import annotations

import pytest

from superclaude.cli.observe import theme
from superclaude.cli.observe.theme import (
    FROZEN_ROLE,
    ROLES,
    STATE_ROLE,
    style_for,
)

DEPTHS = ("standard", "256", "truecolor")
# One role per palette colour, so eight distinct colours means eight distinct roles (RB-09).
PALETTE_ROLES = (
    "attention",  # amber
    "identity",  # base
    "secondary",  # slate
    "muted",
    "state_running",  # green
    "state_settled",  # cyan
    "state_failed",  # red
    "state_frozen",  # violet
)


@pytest.mark.parametrize("depth", DEPTHS)
def test_every_role_has_a_style_at_every_depth(depth):
    for role in ROLES:
        assert style_for(role, depth) is not None


def test_no_depth_means_no_style():
    assert all(style_for(role, None) is None for role in ROLES)


def test_an_unknown_role_is_an_error_not_a_silent_default():
    with pytest.raises(KeyError):
        style_for("nonsense", "standard")


def test_the_eight_palette_roles_keep_eight_distinct_colours_at_16_colours():
    numbers = [style_for(role, "standard").color.number for role in PALETTE_ROLES]
    assert len(set(numbers)) == 8


def test_the_four_state_roles_have_four_different_codes_at_16_colours():
    roles = ("state_running", "state_settled", "state_failed", "state_frozen")
    codes = {style_for(role, "standard").color.number for role in roles}
    assert len(codes) == 4


def test_the_state_table_is_not_empty_and_names_the_minimum_keys():
    required = [
        ("workerState", "running"),
        ("workerState", "succeeded"),
        ("workerState", "failed"),
        ("dispatchStatus", "completed"),
        ("liveness", "alive"),
    ]
    assert all(key in STATE_ROLE for key in required)
    assert FROZEN_ROLE == "state_frozen"
    assert all(role in ROLES for role in (*STATE_ROLE.values(), FROZEN_ROLE))
    # A word the table does not name keeps the body role: it is never classified.
    assert ("workerState", "blocked") not in STATE_ROLE
    assert ("terminalState", "released") not in STATE_ROLE


def test_no_style_blinks_dims_or_reverses():
    for depth in DEPTHS:
        for role in ROLES:
            style = style_for(role, depth)
            assert not (style.blink or style.blink2 or style.dim or style.reverse)


def test_styles_are_distinct_objects_per_depth_and_cached_per_depth():
    standard = style_for("attention", "standard")
    truecolor = style_for("attention", "truecolor")
    assert standard is not truecolor and standard != truecolor
    assert style_for("attention", "standard") is standard
    assert truecolor.color.get_truecolor().hex == "#fab219"


def test_the_theme_module_holds_no_terminal_facts():
    text = open(theme.__file__, encoding="utf-8").read()
    for literal in (
        "Console(",
        "NO_COLOR",
        "COLUMNS",
        "stdout.encoding",
        "getpreferredencoding",
    ):
        assert literal not in text
