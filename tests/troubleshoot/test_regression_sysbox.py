"""T15 sysbox regression — R-19 acceptance test. Harness §5.

calibrator: not run (pre-R-05/R-09 cards) for Fable-D3.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from tests.troubleshoot._assertions import _confidence, evaluate_validator
from tests.troubleshoot._procedures import requires_runs_in
from tests.troubleshoot.test_inline_fallback_parity import EXPECTED_IDS, load_regression

FIX = Path(__file__).parent / "fixtures"
REG = FIX / "regression" / "sysbox-20260918"


def _manifest_rows() -> list[tuple[str, str, int]]:
    rows = []
    for line in (REG / "MANIFEST").read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        path, sha, n, _src = line.split("\t")
        rows.append((path, sha, int(n)))
    return rows


@pytest.mark.parametrize(
    "param",
    ["GLM-RUN2", "Fable-D3", "Astra-A3"],
    ids=["GLM-RUN2", "Fable-D3", "Astra-A3"],
)
def test_regression_manifest_and_expected_ids(param: str) -> None:
    """R-19 T15: MANIFEST byte-copy guard + expected id sets (Astra F-C1)."""
    for rel, sha, n in _manifest_rows():
        raw = (REG / rel).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == sha, rel
        assert len(raw) == n, (rel, len(raw), n)
    vin, cin = load_regression(param)
    ids = evaluate_validator(vin).ids
    if cin is not None:
        from tests.troubleshoot._assertions import evaluate_calibrator

        ids |= evaluate_calibrator(cin).ids
    assert ids == EXPECTED_IDS[param], (param, ids)
    if param == "Fable-D3":
        assert cin is None
        assert _confidence(vin.report) == 0.72
    if param == "Astra-A3":
        assert requires_runs_in(vin.observation_text, "no") is True
