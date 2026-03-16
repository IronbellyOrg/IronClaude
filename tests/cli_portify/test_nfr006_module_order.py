"""Tests for NFR-006: Mandated module generation order.

Verifies that MANDATED_STEP_ORDER in registry.py matches the exact
13-module sequence required by NFR-006 and AC-012.

NFR-006 mandated order:
    models → gates → prompts → config → inventory → monitor →
    process → executor → tui → logging_ → diagnostics → commands → __init__
"""

from __future__ import annotations

import pytest

from superclaude.cli.cli_portify.registry import (
    MANDATED_STEP_ORDER,
    assert_step_order,
    get_step_order,
)


# ---------------------------------------------------------------------------
# NFR-006 reference order (single source of truth for these tests)
# ---------------------------------------------------------------------------

NFR006_ORDER: tuple[str, ...] = (
    "models",
    "gates",
    "prompts",
    "config",
    "inventory",
    "monitor",
    "process",
    "executor",
    "tui",
    "logging_",
    "diagnostics",
    "commands",
    "__init__",
)


class TestNFR006ModuleOrder:
    """Assert MANDATED_STEP_ORDER matches NFR-006 exactly (AC-012)."""

    def test_nfr006_step_count(self):
        """MANDATED_STEP_ORDER contains exactly 13 module steps."""
        assert len(MANDATED_STEP_ORDER) == 13

    def test_nfr006_exact_order(self):
        """MANDATED_STEP_ORDER matches NFR-006 sequence exactly."""
        assert MANDATED_STEP_ORDER == NFR006_ORDER

    def test_nfr006_get_step_order_matches(self):
        """get_step_order() returns the same sequence as MANDATED_STEP_ORDER."""
        assert get_step_order() == MANDATED_STEP_ORDER

    def test_nfr006_consecutive_pairs_ordered(self):
        """Each consecutive pair in MANDATED_STEP_ORDER appears in NFR-006 order."""
        order_index = {name: i for i, name in enumerate(NFR006_ORDER)}
        for i in range(len(MANDATED_STEP_ORDER) - 1):
            step_a = MANDATED_STEP_ORDER[i]
            step_b = MANDATED_STEP_ORDER[i + 1]
            assert order_index[step_a] < order_index[step_b], (
                f"Step '{step_a}' must appear before '{step_b}' in NFR-006 order"
            )

    def test_nfr006_assert_step_order_passes_for_valid(self):
        """assert_step_order() does not raise for the correct NFR-006 order."""
        assert_step_order(list(NFR006_ORDER))  # must not raise

    def test_nfr006_assert_step_order_raises_for_swapped(self):
        """assert_step_order() raises AssertionError when two entries are swapped."""
        swapped = list(NFR006_ORDER)
        swapped[0], swapped[1] = swapped[1], swapped[0]  # swap models ↔ gates
        with pytest.raises(AssertionError):
            assert_step_order(swapped)

    def test_nfr006_all_module_names_present(self):
        """Every NFR-006 module name appears in MANDATED_STEP_ORDER."""
        for name in NFR006_ORDER:
            assert name in MANDATED_STEP_ORDER, (
                f"Module '{name}' missing from MANDATED_STEP_ORDER"
            )

    def test_nfr006_commands_before_init(self):
        """commands appears immediately before __init__ in NFR-006 order."""
        order = list(MANDATED_STEP_ORDER)
        commands_idx = order.index("commands")
        init_idx = order.index("__init__")
        assert commands_idx == init_idx - 1, (
            "commands must immediately precede __init__"
        )

    def test_nfr006_models_is_first(self):
        """models is the first module in NFR-006 order."""
        assert MANDATED_STEP_ORDER[0] == "models"

    def test_nfr006_init_is_last(self):
        """__init__ is the last module in NFR-006 order."""
        assert MANDATED_STEP_ORDER[-1] == "__init__"
