"""py/h2_normalize.py (R-02)."""
import json
import sys

from conftest import PY, pyrun, report

sys.path.insert(0, str(PY))
from _lib import findings  # noqa: E402
from h2_normalize import normalize  # noqa: E402

LONG = ("When the plan edits the greeting module it must also update every caller of the greeting function, including "
        "the command line entry point, the web handler, the scheduled job, the documentation examples and the release "
        "notes, and each of those places has to show the same new wording.")
CAND = f"# Plan\n\n## Task 1: Greeting\n{LONG}\n"


def F(**kw):
    f = {"id": "F1", "severity": "MAJOR", "blocking": True, "category": "contradiction", "anchor": LONG[:60], "refs": [], "claim": "c"}
    f.update(kw)
    return f


def test_long_anchor_truncated_and_located():
    assert len(LONG) >= 250
    norm, info = normalize(report([F(anchor=LONG[:250])]))
    res = findings().parse_block(norm)
    assert info["truncated"]["anchor"] == 1 and res["ok"] and len(res["findings"]) == 1
    a = res["findings"][0]["anchor"]
    assert len(a) <= 200 and LONG.startswith(a)
    assert findings().locate(CAND, a)


def test_long_claim_cut_to_300():
    norm, info = normalize(report([F(claim="w " * 200)]))
    res = findings().parse_block(norm)
    assert info["truncated"]["claim"] == 1 and res["ok"] and len(res["findings"][0]["claim"]) <= 300


def test_bad_severity_needs_reask():
    norm, info = normalize(report([F(severity="HIGH")]))
    assert info["needs_reask"] and not info["block_ok"]
    assert any("severity" in e["msg"] for e in info["errors"])


def test_clean_report_unchanged(tmp_path):
    text = report([F()])
    (tmp_path / "r.md").write_text(text)
    r = pyrun("h2_normalize.py", "--report", str(tmp_path / "r.md"), "--out", str(tmp_path / "n.md"), "--json", str(tmp_path / "h.json"))
    assert r.returncode == 0
    info = json.loads((tmp_path / "h.json").read_text())
    assert info["block_ok"] and not info["needs_reask"] and (tmp_path / "n.md").read_text() == text
