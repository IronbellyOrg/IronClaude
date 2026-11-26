from conftest import candidate, finding, report
from superclaude.cli.review import findings as F

from r3lib import findings_io

CAND = candidate()


def p1():
    return report(
        [
            finding("F1", "only", "unpassable-check"),
            finding("F2", "never"),
            finding("F3", "reread", "contradiction"),
        ]
    )


def test_three_plus_two():
    p2 = [
        finding("C1", "mustnot", claim="new one"),
        finding("C2", "cmd", claim="new two"),
    ]
    text, log = findings_io.combine(p1(), p2)
    res = F.parse_block(text)
    assert res["ok"] and len(res["findings"]) == 5
    assert [f["id"] for f in res["findings"]] == ["F1", "F2", "F3", "P2-F1", "P2-F2"]
    assert [f["origin"] for f in res["findings"]] == ["own"] * 3 + ["peer"] * 2
    sealed = F.parse_block(p1())["findings"]
    for a, b in zip(res["findings"][:3], sealed):
        assert {k: v for k, v in a.items() if k != "origin"} == b
    assert text.rstrip().endswith("verdict: PASS") and text.count("```findings-v1") == 1


def test_two_blocks_yield_one():
    t = report([finding("F1", "only"), finding("F2", "never")], blocks=2)
    text, _ = findings_io.combine(t, [])
    res = F.parse_block(text)
    assert (
        res["ok"]
        and text.count("```findings-v1") == 1
        and [f["id"] for f in res["findings"]] == ["F1", "F2"]
    )


def test_dupe_dropped_and_p2x():
    t = report(
        [finding("P2-F1", "only"), finding("F2", "never", claim="same claim text here")]
    )
    dup = finding("C1", "never", claim="same claim text here")
    new = finding("C2", "mustnot", claim="new")
    text, log = findings_io.combine(t, [dup, new])
    ids = [f["id"] for f in F.parse_block(text)["findings"]]
    assert log["p2_dupe_dropped"] == 1 and ids == ["P2-F1", "F2", "P2X-F1"]


def test_long_anchor_selfcheck():
    a = F.flat(CAND)[:250]
    text, _ = findings_io.combine(report([finding("F1", a)]), [])
    f = F.parse_block(text)["findings"][0]
    assert len(f["anchor"]) == 200 and F.parse_block(text)["ok"]
