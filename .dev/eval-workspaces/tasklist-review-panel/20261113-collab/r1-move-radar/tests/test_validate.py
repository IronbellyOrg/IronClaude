"""T-9: msg-validate.sh accepts radar lines and rejects with the right reason."""

import json

import pytest
from conftest import CAT, R1, TOOLS, run

BASE = {"v": "panel-msg/1", "id": "m-t4-1-08", "run": "el2-c1-r3/P", "from": "radar", "to": "t4-1", "t": 1763062000123, "kind": "move"}


def validate(line, text):
    env = json.dumps({"line": line if isinstance(line, str) else json.dumps(line), "text": text})
    r = run(["bash", str(TOOLS / "msg-validate.sh"), str(R1 / "config" / "catalogue.json"), "t2b-1", "t4-1,t3-1"], stdin=env + "\n")
    rej = [json.loads(x)["reject"] for x in r.stderr.splitlines()]
    return r.returncode, r.stdout.strip(), rej


def test_accepts_move_and_src_check():
    assert validate(dict(BASE, move="M5"), CAT["moves"]["M5"])[0] == 0
    rc, out, _ = validate(BASE, CAT["src_text"])
    assert rc == 0 and json.loads(out) == BASE
    assert validate(dict(BASE, to="t2b-1", move="M2"), CAT["moves"]["M2"] + CAT["observable_suffix"])[0] == 0


def test_too_long():
    short = json.dumps(dict(BASE, move="M5"))
    line = json.dumps(dict(BASE, move="M5", run=BASE["run"] + "x" * (601 - len(short))))
    assert len(line.encode()) == 601
    assert validate(line, CAT["moves"]["M5"])[2] == ["too_long"]
    ok = json.dumps(dict(BASE, move="M5", run=BASE["run"] + "x" * (600 - len(short))))
    assert len(ok.encode()) == 600 and validate(ok, CAT["moves"]["M5"])[0] == 0


@pytest.mark.parametrize("key", ["claim", "verdict", "blocking", "severity", "category", "note", "anchor", "items", "extra"])
def test_bad_key(key):
    assert validate(dict(BASE, move="M5", **{key: "x"}), CAT["moves"]["M5"])[2] == [f"bad_key:{key}"]


def test_bad_field_from():
    assert validate(dict(BASE, move="M5", **{"from": "t4-1"}), CAT["moves"]["M5"])[2] == ["bad_field:from"]


def test_bad_move():
    assert validate(dict(BASE, move="M11"), "x")[2] == ["bad_move"]


def test_leak_text_differs():
    assert validate(dict(BASE, move="M5"), CAT["moves"]["M5"] + " see Task 3")[2] == ["leak"]


def test_leak_suffix_on_reading_move():
    assert validate(dict(BASE, move="M5"), CAT["moves"]["M5"] + CAT["observable_suffix"])[2] == ["leak"]


def test_not_json():
    assert validate("{not json", "x")[2] == ["not_json"]
