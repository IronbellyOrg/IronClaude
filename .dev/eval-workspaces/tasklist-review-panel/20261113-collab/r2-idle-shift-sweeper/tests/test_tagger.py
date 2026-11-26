"""py/tagger.py (R-10)."""
import json
import sys

from conftest import PY, pyrun, report

sys.path.insert(0, str(PY))
from _lib import findings  # noqa: E402

FACT_ANCHOR = "so that every greeting uses the new wording"


def board(tmp, delivered=("f-0",)):
    b = tmp / "board"
    (b / "msgs").mkdir(parents=True)
    (b / "state").mkdir()
    facts = [{"id": "f-0", "move": "M1", "anchor": FACT_ANCHOR, "items": ["tests/x.py", "CHANGELOG.md:3"], "cmd": "grep -rn x tests/"},
             {"id": "f-1", "move": "M1", "anchor": "completely different sentence here", "items": ["docs/other.md"], "cmd": "ls docs"}]
    (b / "msgs/board.jsonl").write_text("".join(json.dumps(f) + "\n" for f in facts))
    (b / "state/t4-1.delivered").write_text("".join(d + "\n" for d in delivered))
    return b


def F(**kw):
    f = {"id": "F1", "severity": "MAJOR", "blocking": True, "category": "other", "anchor": "unrelated words here ok", "refs": [], "claim": "c"}
    f.update(kw)
    return f


def tag(tmp, f, *flags, delivered=("f-0",)):
    b = board(tmp, delivered)
    (tmp / "r.md").write_text(report([f]))
    r = pyrun("tagger.py", "--report", str(tmp / "r.md"), "--board-dir", str(b), "--rid", "t4-1", "--out", str(tmp / "t4-1.final.md"), *flags)
    assert r.returncode == 0, r.stderr
    res = findings().parse_block((tmp / "t4-1.final.md").read_text())
    assert res["ok"] and len(res["findings"]) == 1
    return res["findings"][0]["origin"]


def test_overlap_12_is_peer(tmp_path):
    assert len(FACT_ANCHOR[3:15]) == 12
    assert tag(tmp_path, F(anchor="AB" + FACT_ANCHOR[3:15] + "ZZZZ")) == "peer"


def test_overlap_11_is_own(tmp_path):
    assert tag(tmp_path, F(anchor="ZZ" + FACT_ANCHOR[3:14] + "QQQQQQQQQQ")) == "own"


def test_refs_names_delivered_item(tmp_path):
    assert tag(tmp_path, F(refs=["CHANGELOG.md:9"])) == "peer"


def test_claim_path_token(tmp_path):
    assert tag(tmp_path, F(claim="The test tests/x.py:3 still asserts the old wording.")) == "peer"


def test_undelivered_fact_does_not_tag(tmp_path):
    assert tag(tmp_path, F(refs=["docs/other.md"], anchor="completely different sentence here")) == "own"


def test_nonreceiver_all_own(tmp_path):
    assert tag(tmp_path, F(refs=["CHANGELOG.md"]), "--nonreceiver") == "own"


def test_isolated_attempt_all_own(tmp_path):
    assert tag(tmp_path, F(refs=["CHANGELOG.md"]), "--isolated") == "own"


def test_one_block_kept(tmp_path):
    tag(tmp_path, F())
    assert (tmp_path / "t4-1.final.md").read_text().count("```findings-v1") == 1
