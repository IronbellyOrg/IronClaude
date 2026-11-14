import json

from conftest import ANCH, cand_line, candidate

from r3lib import digest

CAND = candidate()
SRC = ["t2b-1"]


def line(**kw):
    o = {
        "v": "panel-msg/1",
        "id": "m-t4-1-1",
        "run": "r/p",
        "from": "t2b-1",
        "to": "t4-1",
        "t": 1,
        "kind": "challenge",
        "move": "M3",
        "anchor": cand_line(ANCH["only"]),
    }
    o.update(kw)
    return json.dumps(o)


def test_rejects():
    cases = [
        (line(anchor=cand_line(ANCH["only"]) + "x" * 500), "too_long"),
        (json.dumps({**json.loads(line()), "claim": "c"}), "forbidden_key:claim"),
        (json.dumps({**json.loads(line()), "category": "c"}), "forbidden_key:category"),
        (json.dumps({**json.loads(line()), "x": 1}), "forbidden_key:x"),
        (line(kind="card"), "bad_kind"),
        (
            line(anchor="This text is nowhere in the candidate file"),
            "anchor_not_in_candidate",
        ),
    ]
    for ln, why in cases:
        ok, r = digest.validate_line(ln, CAND, "t4-1", SRC)
        assert not ok and r == why, (r, why)
    ok, r = digest.validate_line(line(**{"from": "t4-1"}), CAND, "t4-1", ["t4-1"])
    assert not ok and r == "self_or_unknown_source"


def test_accepts():
    for k, m in (("only", "M3"), ("never", "M8"), ("cmd", "M4")):
        assert digest.validate_line(
            line(anchor=cand_line(ANCH[k]), move=m), CAND, "t4-1", SRC
        ) == (True, "ok")


def test_digest_cap_drops_last():
    meta = {"to": "t4-1", "run": "r/" + "p" * 300, "t_ms": 1}
    slots = [
        {"anchor": cand_line(ANCH[k]), "move": "M3", "from": "t2b-1"}
        for k in ("only", "never", "reread", "every")
    ]
    lines = digest.render_lines(slots, meta)
    assert len("\n".join(lines).encode()) > 1800
    kept, dropped = digest.cap_digest(slots, meta)
    assert len(kept) < len(slots) and kept == slots[: len(kept)]
