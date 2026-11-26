"""lib/card.jq and its callers (design 6.1 test_card_validator; R-06 verification set)."""

import json

import collab
from r4help import R4, first_card_anchor, jsonl, make_board, post, run

KEYS = ["v", "id", "run", "from", "to", "t", "kind", "move", "anchor", "category", "severity"]


def card(**kw):
    d = {"v": "panel-msg/1", "id": "c0", "run": "row/pkg", "from": "t2b-1", "to": "t4-1", "t": 1763063000123,
         "kind": "card", "move": "M3", "anchor": "every acceptance criterion passes", "category": "unpassable-check", "severity": "MAJOR"}
    d.update(kw)
    return json.dumps({k: d[k] for k in KEYS if k in d} | {k: v for k, v in d.items() if k not in KEYS}, separators=(",", ":"))


def jqcheck(lines, flagger="t2b-1"):
    out = run(["jq", "-R", "-r", "--arg", "flagger", flagger, "-f", R4 / "lib" / "card.jq"], input="\n".join(lines) + "\n").stdout
    return out.splitlines()


GOOD = [card(move="M3", category="unpassable-check"), card(id="c1", move="M4", category="contradiction"),
        card(id="c2", move="M9", category="missing-requirement"), card(id="c3", move="M5", category="safety", severity="CRITICAL")]


def test_good_cards_pass_unchanged():
    assert jqcheck(GOOD) == GOOD


def bad_lines():
    d = json.loads(card())
    claim = card(claim="this is wrong")
    verdict = card(verdict="FAIL")
    move_kind = card(kind="move")
    m1 = card(move="M1")
    short = card(anchor="x" * 11)
    from_luna = card(**{"from": "t4-1"})
    note = card(note="hi")
    long = json.dumps(d | {"anchor": "a" * 200}, separators=(",", ":"))
    pad = 601 - len(long.encode())
    long601 = long.replace('"run":"row/pkg"', '"run":"' + "r" * (7 + pad) + '"')
    return {"claim": claim, "verdict": verdict, "category_on_move": move_kind, "M1": m1, "anchor11": short,
            "from_luna": from_luna, "note": note, "bytes601": long601}


def test_bad_lines_rejected_by_schema():
    bl = bad_lines()
    assert len(bl["bytes601"].encode()) == 601
    for name, ln in bl.items():
        if name == "bytes601":
            continue
        assert jqcheck([ln]) == [], name


def test_caller_drops_601_byte_line(tmp_path):
    bl = bad_lines()
    assert jqcheck([bl["bytes601"]]) == [bl["bytes601"]]  # schema-valid: only the caller's byte check rejects it
    f = tmp_path / "msgs.jsonl"
    f.write_text("\n".join(GOOD + list(bl.values())) + "\n")
    assert collab.valid_cards(str(f), "t2b-1") == GOOD


def test_third_post_over_cap(tmp_path):
    board, cf = make_board(tmp_path)
    for n in range(2):
        r = post(board, cf, anchor=first_card_anchor(n=n), cap=2)
        assert r.returncode == 0, r.stderr
    r = post(board, cf, anchor=first_card_anchor(n=2), cap=2)
    assert r.returncode == 1 and "refused: over_cap" in r.stderr
    ev = jsonl(board / "metrics" / "t2b-1.jsonl")
    assert any(e["ev"] == "post_rejected" and e["reason"] == "over_cap" for e in ev)
    lines = (board / "msgs" / "t2b-1.jsonl").read_text().splitlines()
    assert jqcheck(lines) == lines and len(lines) == 2
