"""Deterministic best_model tier selection (core R3 — NEW, no repo precedent).

Given per-model aggregated results, pick the best model under one of four tiers,
applying the 0.70 pass-rate floor for speed/cost and suppressing the hint when the
winner's confidence (separation vs runner-up) is below 0.5 (the row is then treated
as model-agnostic). Pure + deterministic; no model calls; no `anthropic` import.

Tier rules (merged-requirements.md:248-257 / research/03 §4):
  - quality:  highest pass_rate; tie-break lower mean tokens.
  - speed:    lowest mean duration among models with pass_rate > 0.70.
  - cost:     lowest mean tokens among models with pass_rate > 0.70.
  - balanced (default): normalize (1-pass_rate), tokens, duration each to [0,1]
                across the panel; weighted sum 0.5/0.25/0.25; lowest score wins.
  - confidence = normalized separation of the winner vs runner-up on the tier's
                deciding metric; if < 0.5 the hint is SUPPRESSED.
"""

from __future__ import annotations

QUALITY_FLOOR = 0.70
CONFIDENCE_SUPPRESS_BELOW = 0.5
# balanced composite weights: 0.5 quality, 0.25 cost, 0.25 speed.
W_QUALITY, W_COST, W_SPEED = 0.5, 0.25, 0.25


def _norm(value: float, lo: float, hi: float) -> float:
    """Min-max normalize to [0,1]; 0 when the panel has no spread."""
    if hi <= lo:
        return 0.0
    return (value - lo) / (hi - lo)


def _balanced_scores(results: dict[str, dict]) -> dict[str, float]:
    """Composite score per model (lower is better)."""
    pass_rates = [r["pass_rate"] for r in results.values()]
    tokens = [r["mean_tokens"] for r in results.values()]
    durations = [r["mean_duration_s"] for r in results.values()]
    pr_lo, pr_hi = min(1 - p for p in pass_rates), max(1 - p for p in pass_rates)
    tk_lo, tk_hi = min(tokens), max(tokens)
    du_lo, du_hi = min(durations), max(durations)
    scores: dict[str, float] = {}
    for model, r in results.items():
        scores[model] = (
            W_QUALITY * _norm(1 - r["pass_rate"], pr_lo, pr_hi)
            + W_COST * _norm(r["mean_tokens"], tk_lo, tk_hi)
            + W_SPEED * _norm(r["mean_duration_s"], du_lo, du_hi)
        )
    return scores


def _confidence(values: dict[str, float], winner: str, *, lower_wins: bool) -> float:
    """Normalized separation of winner vs runner-up on the deciding metric.

    1.0 when the winner is the only candidate or maximally separated; 0.0 when the
    winner and runner-up are tied (or the panel has no spread).
    """
    if len(values) < 2:
        return 1.0
    ordered = sorted(values.values(), reverse=not lower_wins)
    win_val, runner_val = ordered[0], ordered[1]
    spread = max(values.values()) - min(values.values())
    if spread <= 0:
        return 0.0
    return min(1.0, abs(runner_val - win_val) / spread)


def _agnostic(tier: str, based_on, confidence: float) -> dict:
    return {
        "model": None,
        "tier": tier,
        "based_on": based_on,
        "confidence": round(confidence, 4),
        "suppressed": True,
    }


def select_best_model(
    per_model_results: dict[str, dict],
    tier: str = "balanced",
    based_on=None,
) -> dict:
    """Select the best model under `tier`, or a model-agnostic result if suppressed.

    `per_model_results` maps model -> {pass_rate, mean_tokens, mean_duration_s, ...}.
    Returns {model, tier, based_on, confidence} on a confident pick, or a
    model-agnostic result (model=None, suppressed=True) when confidence < 0.5 or no
    model clears the floor.
    """
    if not per_model_results:
        return _agnostic(tier, based_on, 0.0)

    if tier == "quality":
        # highest pass_rate, tie-break lower mean tokens.
        max_pr = max(r["pass_rate"] for r in per_model_results.values())
        top = {m: r for m, r in per_model_results.items() if r["pass_rate"] == max_pr}
        if len(top) == 1:
            # Clear quality winner -> confidence from pass_rate separation.
            winner = next(iter(top))
            metric = {m: r["pass_rate"] for m, r in per_model_results.items()}
            confidence = _confidence(metric, winner, lower_wins=False)
        else:
            # Quality tie -> tie-break on lower mean tokens; confidence from the
            # token separation WITHIN the tied-top group (the tie-break is the real
            # decision, so a clear cheaper equal-quality model IS a confident pick).
            winner = min(top, key=lambda m: top[m]["mean_tokens"])
            metric = {m: top[m]["mean_tokens"] for m in top}
            confidence = _confidence(metric, winner, lower_wins=True)

    elif tier in ("speed", "cost"):
        floored = {
            m: r for m, r in per_model_results.items() if r["pass_rate"] > QUALITY_FLOOR
        }
        if not floored:
            return _agnostic(tier, based_on, 0.0)
        key = "mean_duration_s" if tier == "speed" else "mean_tokens"
        winner = min(floored, key=lambda m: floored[m][key])
        metric = {m: r[key] for m, r in floored.items()}
        confidence = _confidence(metric, winner, lower_wins=True)

    else:  # balanced (default)
        tier = "balanced"
        scores = _balanced_scores(per_model_results)
        winner = min(scores, key=lambda m: scores[m])
        confidence = _confidence(scores, winner, lower_wins=True)

    if confidence < CONFIDENCE_SUPPRESS_BELOW:
        return _agnostic(tier, based_on, confidence)

    return {
        "model": winner,
        "tier": tier,
        "based_on": based_on,
        "confidence": round(confidence, 4),
    }
