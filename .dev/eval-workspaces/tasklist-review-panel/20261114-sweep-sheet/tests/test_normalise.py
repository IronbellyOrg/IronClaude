"""H2 normaliser (REQ-02; DESIGN 11.2 row H2)."""

import json
import textwrap

from helpers import SW

from scaffold import fnd
from scaffold.normalise import normalise_file, normalise_report

REPORTS = SW / "fixtures" / "reports"


def load(name):
    return (REPORTS / f"{name}.md").read_text()


def findings(text):
    """Finding objects by id, read from the raw lines so a report that fails parse_block can still be read."""
    objs = []
    for line in fnd.lenient_lines(text):
        try:
            objs.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return {f["id"]: f for f in objs if "prior" not in f}


def candidate_for(text):
    """A candidate document that holds every quote of the report, wrapped at 60 columns."""
    quotes = []
    for f in findings(text).values():
        quotes += [f["anchor"]] + ([f["anchor2"]] if f.get("anchor2") else [])
    return "# Spec\n\n" + textwrap.fill("  ".join(quotes), 60) + "\n"


def test_fixtures_have_the_stated_lengths():
    f = findings(load("anchor_250"))
    assert len(fnd.flat(f["F1"]["anchor"])) == 250
    assert len(fnd.flat(f["F2"]["anchor2"])) > 200
    assert len(fnd.flat(findings(load("claim_301"))["F1"]["claim"])) == 301


def test_anchor_250_survives():
    text = load("anchor_250")
    before = findings(text)["F1"]["anchor"]
    out, info = normalise_report(text)
    after = findings(out)["F1"]["anchor"]
    assert len(fnd.flat(after)) == 200
    assert before.startswith(after)
    assert fnd.locate(candidate_for(text), after)
    assert fnd.parse_block(out)["ok"] is True
    assert info["ok"] is True and info["unrepaired"] == []


def test_prefix_is_exact_quote():
    text = load("anchor_250")
    cand = candidate_for(text)
    out, _ = normalise_report(text)
    for fid, key in (("F1", "anchor"), ("F2", "anchor2")):
        before, after = findings(text)[fid][key], findings(out)[fid][key]
        assert fnd.flat(before).startswith(after)
        assert fnd.locate(cand, after)
        # the cut quote starts where the full quote starts
        assert fnd.locate(cand, after)[0][0] == fnd.locate(cand, before)[0][0]


def test_claim_301_cut():
    text = load("claim_301")
    before = findings(text)["F1"]["claim"]
    out, info = normalise_report(text)
    after = findings(out)["F1"]["claim"]
    assert len(fnd.flat(after)) == 300
    assert fnd.flat(before).startswith(after)
    assert info["changed"] == [{"line": 8, "id": "F1", "fields": ["claim"]}]
    # the anchor was inside its limit, so its text is not touched
    assert findings(out)["F1"]["anchor"] == findings(text)["F1"]["anchor"]


def test_anchor2_cut():
    text = load("anchor_250")
    out, info = normalise_report(text)
    f2 = findings(out)["F2"]
    assert len(fnd.flat(f2["anchor2"])) == 200
    assert fnd.flat(findings(text)["F2"]["anchor2"]).startswith(f2["anchor2"])
    # F2's short anchor and its claim are untouched; only anchor2 is named
    assert f2["anchor"] == findings(text)["F2"]["anchor"]
    assert [c["fields"] for c in info["changed"] if c["id"] == "F2"] == [["anchor2"]]


def test_result_parses_ok():
    for name in ("anchor_250", "claim_301"):
        text = load(name)
        assert fnd.parse_block(text)["ok"] is False  # over the limits before H2
        out, info = normalise_report(text)
        assert fnd.parse_block(out)["ok"] is True
        assert info["ok"] is True


def test_idempotent(tmp_path):
    for name in ("anchor_250", "claim_301"):
        once, info1 = normalise_report(load(name))
        twice, info2 = normalise_report(once)
        assert twice == once
        assert info2["changed"] == [] and info2["ok"] is True
        assert info1["changed"]
    src = tmp_path / "r.md"
    src.write_text(load("anchor_250"))
    out_dir = tmp_path / "normalised"
    normalise_file(src, out_dir, "r1")
    first = {p.name: p.read_bytes() for p in out_dir.iterdir()}
    src.write_text((out_dir / "r1.md").read_text())
    normalise_file(src, out_dir, "r1")
    second = {p.name: p.read_bytes() for p in out_dir.iterdir()}
    assert first.keys() == {"r1.md", "h2.json"}
    assert second["r1.md"] == first["r1.md"]


def test_lines_still_failing_are_kept_not_dropped(tmp_path):
    good = load("claim_301")
    head, _, rest = good.partition("```findings-v1\n")
    bad_json = "{not json"
    short = json.dumps(
        {
            "id": "F9",
            "severity": "MAJOR",
            "blocking": False,
            "category": "other",
            "anchor": "too short",
            "claim": "x",
        }
    )
    text = head + "```findings-v1\n" + bad_json + "\n" + short + "\n" + rest
    out, info = normalise_report(text)
    assert bad_json in out and short in out  # the lines are still in the text
    assert info["ok"] is False
    assert [(u["line"], u["text"]) for u in info["unrepaired"]] == [
        (8, bad_json),
        (9, short),
    ]
    assert "valid JSON" in info["unrepaired"][0]["msg"]
    assert "anchor" in info["unrepaired"][1]["msg"]
    # the long claim on the third line is still cut
    assert findings(out)["F1"]["claim"] and len(findings(out)["F1"]["claim"]) == 300

    src = tmp_path / "bad.md"
    src.write_text(text)
    normalise_file(src, tmp_path / "n", "r2")
    h2 = json.loads((tmp_path / "n" / "h2.json").read_text())
    assert [u["rid"] for u in h2["unrepaired"]] == ["r2", "r2"]
    assert h2["reports"]["r2"]["ok"] is False


def test_report_without_block_is_unchanged_and_reported():
    text = "review: 1 of 3\n\nno findings block here\n"
    out, info = normalise_report(text)
    assert out == text
    assert info["ok"] is False and info["unrepaired"][0]["line"] == 0


def test_line_ending_and_other_lines_are_preserved():
    text = load("claim_301")
    out, _ = normalise_report(text)
    a, b = text.splitlines(keepends=True), out.splitlines(keepends=True)
    assert len(a) == len(b)
    assert [i for i in range(len(a)) if a[i] != b[i]] == [7]
    assert out.endswith("```\n")


def test_cut_does_not_leave_a_trailing_space():
    # 199 letters then a space then more: the cut at 200 ends on the space, which flat() would strip
    anchor = "a" * 199 + " bbbbbbbbbbbb"
    line = json.dumps(
        {
            "id": "F1",
            "severity": "MAJOR",
            "blocking": False,
            "category": "other",
            "anchor": anchor,
            "refs": [],
            "claim": "c",
        }
    )
    text = f"## Findings block\n\n```findings-v1\n{line}\n```\n"
    out, _ = normalise_report(text)
    got = findings(out)["F1"]["anchor"]
    assert got == "a" * 199
    assert normalise_report(out)[0] == out
