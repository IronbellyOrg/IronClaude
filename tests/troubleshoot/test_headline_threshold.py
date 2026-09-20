"""T11 headline threshold — R-10 acceptance test. Harness §3 T11."""

from __future__ import annotations

from pathlib import Path

from tests.troubleshoot._assertions import (
    CalibratorInputs,
    _calibrated,
    _confidence,
    evaluate_calibrator,
    load_fixture,
)

FIX = Path(__file__).parent / "fixtures"


def _cal(fx_path: Path) -> float:
    fx = load_fixture(fx_path)
    if "calibrated" in fx.meta:
        return float(fx.meta["calibrated"])  # type: ignore[arg-type]
    texts = [t for n, t in fx.files.items() if n.lower().startswith("calibration")]
    cal = _calibrated(texts)
    if cal is not None:
        return cal
    conf = _confidence(fx.files.get("REPORT.md", fx.files.get("card.md", "")))
    return 0.0 if conf is None else conf


def test_threshold_separates_pos_and_neg_fixtures() -> None:
    """R-10: every pos calibrated < 0.5; every neg calibrated >= 0.5."""
    pos = [_cal(p) for p in FIX.glob("assertions/C1/*/pos.md")]
    pos += [_cal(p) for p in FIX.glob("assertions/A1/*/pos.md")]
    neg = [_cal(p) for p in FIX.glob("assertions/C1/*/neg*.md")]
    neg += [_cal(p) for p in FIX.glob("assertions/A1/*/neg.md")]
    assert pos and neg, (pos, neg)
    assert all(v < 0.5 for v in pos), pos
    assert all(v >= 0.5 for v in neg), neg
    assert 0.5 in neg, neg


def test_missing_confidence_is_undetermined() -> None:
    """R-10 GB-05: missing confidence evaluates as 0.0 and C1 fires."""
    inp = CalibratorInputs(
        card="## Claim\nRoot cause: the outcome is `clone-failed`.\n",
        calibrated=None,
    )
    result = evaluate_calibrator(inp)
    assert result.verdict == "ESCALATE", result
