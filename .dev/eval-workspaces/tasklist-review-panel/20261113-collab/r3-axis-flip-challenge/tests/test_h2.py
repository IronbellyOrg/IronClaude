from conftest import candidate, finding, report
from superclaude.cli.review import findings as F

from r3lib import findings_io

CAND = candidate()


def _long(n):
    s = F.flat(CAND)
    return s[:n]


def test_long_anchor_truncated_not_dropped():
    a = _long(250)
    t = report([finding("F1", a)])
    out, info = findings_io.normalise_text(t)
    assert info["exit"] == 0 and info["would_drop"] == 0
    f = F.parse_block(out)["findings"][0]
    assert len(f["anchor"]) == 200 and F.locate(CAND, f["anchor"])


def test_long_claim_truncated():
    t = report([finding("F1", "only", claim="x " * 175)])
    out, info = findings_io.normalise_text(t)
    assert info["exit"] == 0 and len(F.parse_block(out)["findings"][0]["claim"]) == 300


def test_bad_severity_exit3():
    t = report([finding("F1", "only", severity="HIGH")])
    _, info = findings_io.normalise_text(t)
    assert info["exit"] == 3 and "severity" in info["errors"][0]["msg"]


def test_minor_blocking_exit3():
    _, info = findings_io.normalise_text(
        report([finding("F1", "only", severity="MINOR", blocking=True)])
    )
    assert info["exit"] == 3


def test_missing_heading_exit4():
    _, info = findings_io.normalise_text(report([finding("F1", "only")], heading=False))
    assert info["exit"] == 4


def test_valid_block_unchanged():
    t = report([finding("F1", "only"), finding("F2", "never")])
    out, info = findings_io.normalise_text(t)
    assert out == t and info["exit"] == 0
