"""lib/render-fact.sh: DESIGN 2.5.3 template and trimming."""
import json

from conftest import BIN, R2, run

CAT = json.loads((R2 / "config/catalogue.json").read_text())["moves"]


def render(f):
    r = run(["bash", str(BIN / "lib/render-fact.sh"), "--catalogue", str(R2 / "config/catalogue.json"), "--line", json.dumps(f)])
    assert r.returncode == 0, r.stderr
    return r.stdout.rstrip("\n")


BASE = {"move": "M1", "anchor": "the plan phrase here", "items": ["tests/a.py", "CHANGELOG.md:3"], "cmd": "grep -rn x tests/"}


def test_fixed_template():
    out = render({**BASE, "n": 2}).split("\n")
    assert out == ["Search result to check yourself (not a finding; no conclusion attached).",
                   f"Move M1: {CAT['M1']}", 'Plan text searched: "the plan phrase here"', "Command: grep -rn x tests/",
                   "Paths: tests/a.py, CHANGELOG.md:3", "Count: 2",
                   "Before you cite any path above, open it or re-run the command yourself. Decide for yourself whether anything here is a defect."]


def test_catalogue_text_verbatim():
    for m in ("M1", "M2", "M7", "M6", "M9"):
        assert f"Move {m}: {CAT[m]}" in render({**BASE, "move": m})


def test_n_zero_never_a_count():
    out = render({**BASE, "n": 0})
    assert "Count:" not in out and "Re-run this command yourself: its result is not shown here." in out


def test_optional_lines_omitted():
    out = render({"move": "M2", "cmd": "ls tests"})
    assert "Plan text searched" not in out and "Paths:" not in out and "Count" not in out


def test_trim_items_then_anchor():
    items = [("tests/" + "x" * 190 + f"{i}.py") for i in range(8)]
    out = render({**BASE, "items": items})
    assert len(out) <= 1500 and 'Plan text searched' in out and 0 < out.count("tests/x") < 8
    out2 = render({**BASE, "items": items, "cmd": "grep " + "y" * 1300})
    assert len(out2) <= 1500 and "Paths:" not in out2 and "Plan text searched" not in out2
