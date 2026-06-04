"""Tests for the deterministic best_model tier selection (core R3).

Each tier's rule is asserted against a hand-constructed fixture with a known
correct answer; the 0.70 floor and the < 0.5 confidence suppression are tested
explicitly.
"""

from __future__ import annotations

from superclaude.cli.recommend.best_model import select_best_model


def _m(pass_rate, mean_tokens, mean_duration_s, n_runs=1):
    return {
        "pass_rate": pass_rate,
        "mean_tokens": mean_tokens,
        "mean_duration_s": mean_duration_s,
        "n_runs": n_runs,
    }


class TestBestModelTiers:
    def test_quality_picks_highest_pass_rate_tiebreak_tokens(self):
        # opus + sonnet tie on pass_rate; sonnet has fewer tokens -> tie-break wins.
        results = {
            "opus": _m(0.90, 90_000, 70),
            "sonnet": _m(0.90, 40_000, 40),
            "haiku": _m(0.50, 10_000, 20),
        }
        best = select_best_model(results, "quality")
        assert best["model"] == "sonnet"
        assert best["tier"] == "quality"

    def test_speed_respects_70pct_floor(self):
        # haiku is fastest but below the 0.70 floor -> NOT chosen; opus is the
        # fastest model that clears the floor.
        results = {
            "opus": _m(0.95, 90_000, 70),
            "sonnet": _m(0.90, 40_000, 90),
            "haiku": _m(0.50, 10_000, 5),  # fastest but fails floor
        }
        best = select_best_model(results, "speed")
        assert best["model"] == "opus"

    def test_cost_respects_70pct_floor(self):
        # haiku is cheapest but below the floor -> NOT chosen; sonnet is the
        # cheapest model clearing the floor.
        results = {
            "opus": _m(0.95, 90_000, 70),
            "sonnet": _m(0.90, 40_000, 40),
            "haiku": _m(0.50, 10_000, 20),  # cheapest but fails floor
        }
        best = select_best_model(results, "cost")
        assert best["model"] == "sonnet"

    def test_speed_cost_floor_none_qualify_suppresses(self):
        # No model clears the 0.70 floor -> model-agnostic.
        results = {"opus": _m(0.60, 90_000, 70), "sonnet": _m(0.50, 40_000, 40)}
        best = select_best_model(results, "speed")
        assert best.get("suppressed") is True
        assert best["model"] is None

    def test_balanced_weighted_sum_picks_expected(self):
        # opus dominates all three normalized axes -> clear balanced winner.
        results = {
            "opus": _m(0.95, 10_000, 20),
            "sonnet": _m(0.70, 50_000, 50),
            "haiku": _m(0.60, 90_000, 90),
        }
        best = select_best_model(results, "balanced")
        assert best["model"] == "opus"
        assert best["tier"] == "balanced"

    def test_balanced_is_default_tier(self):
        results = {
            "opus": _m(0.95, 10_000, 20),
            "sonnet": _m(0.60, 90_000, 90),
        }
        best = select_best_model(results)  # no tier arg
        assert best["tier"] == "balanced"
        assert best["model"] == "opus"

    def test_confidence_below_half_suppresses_hint(self):
        # Two near-identical top models (quality) with a distant third create a
        # tiny normalized gap -> confidence < 0.5 -> hint suppressed.
        results = {
            "opus": _m(0.851, 90_000, 70),
            "sonnet": _m(0.850, 40_000, 40),
            "haiku": _m(0.40, 10_000, 20),
        }
        best = select_best_model(results, "quality")
        assert best.get("suppressed") is True
        assert best["model"] is None
        assert best["confidence"] < 0.5

    def test_based_on_recorded(self):
        results = {"opus": _m(0.95, 10_000, 20), "sonnet": _m(0.50, 90_000, 90)}
        best = select_best_model(results, "quality", based_on="iteration-3")
        assert best["based_on"] == "iteration-3"
