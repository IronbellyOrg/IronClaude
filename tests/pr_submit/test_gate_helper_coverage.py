"""FX5 per-helper coverage test — the reported face of the conftest collector.

The ``pytest_generate_tests`` hook in ``tests/pr_submit/conftest.py`` parametrizes
this single test one case per registered gate helper (``GATE_LOAD_BEARING_HELPERS``),
so each enforced helper reports as its own green/red test id. The actual
existence + coverage (negative & differential present) + drift-alarm assertions live
in the conftest and are exposed here via the ``assert_gate_helper_coverage`` fixture,
keeping this module marker-free and free of any hardcoded helper list.

A registered helper missing its negative or differential test, a registered helper
that no longer resolves (silent rename), a registry/HELPER_TEST_MAP divergence, or a
NEW unregistered gate-shaped module-level helper each FAILs here.
"""

from __future__ import annotations


def test_gate_helper_has_negative_and_differential(
    gate_helper, assert_gate_helper_coverage
) -> None:
    """Each registered gate helper carries a negative + differential test pair.

    ``gate_helper`` is parametrized by the conftest ``pytest_generate_tests`` hook;
    ``assert_gate_helper_coverage`` is the conftest-provided assertion runner.
    """
    assert_gate_helper_coverage(gate_helper)
