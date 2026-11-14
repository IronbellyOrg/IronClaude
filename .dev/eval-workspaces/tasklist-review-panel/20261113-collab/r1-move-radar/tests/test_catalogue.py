"""T-1: the frozen catalogue (DESIGN.md 6.1 T-1, R-07)."""

import hashlib
import json
import re

from conftest import A1DIR, FIX, R1, REPO, TOOLS, jload, run

SRCREQ = REPO / ".dev/brainstorms/20261113-163248-panel-collaboration/merged-requirements.md"
PKGS = ["TASK-WF-designSpec-20261107-075614", "TASK-WF-makeTheAliasOnly-20261105-051649", "TASK-WF-design-20261108-041415"]
CAT = R1 / "config" / "catalogue.json"


def src_moves():
    """Move texts from the 'Move (text sent to a reviewer)' column of SRCREQ section 2.0 (the table at lines 184-193)."""
    lines = SRCREQ.read_text().splitlines()[183:193]
    rows = {}
    for ln in lines:
        m = re.match(r"^\| (M\d+) \| (.+?) \| (?:search|reading|either)", ln)
        if m:
            rows[m.group(1)] = m.group(2)
    return rows


def catcheck(cat, gts):
    r = run(["uv", "run", "python", str(TOOLS / "collab_summary.py"), "catcheck", str(cat), *map(str, gts)])
    return r.returncode, json.loads(r.stdout)


def test_texts_equal_the_source_column():
    cat, src = jload(CAT), src_moves()
    assert sorted(src, key=lambda m: int(m[1:])) == [f"M{i}" for i in range(1, 11)]
    assert cat["moves"] == src


def test_observable_set_and_rendered_length():
    cat = jload(CAT)
    assert cat["observable"] == ["M1", "M2", "M4", "M7"]
    for mid, text in cat["moves"].items():
        rendered = text + (cat["observable_suffix"] if mid in cat["observable"] else "")
        assert len(rendered) <= 300, mid
    assert len(cat["src_text"]) <= 300 and len(cat["finish_text"]) <= 300


def test_pin_matches_catalogue_sha256():
    want = (R1 / "config" / "catalogue.sha256").read_text().split()[0]
    assert hashlib.sha256(CAT.read_bytes()).hexdigest() == want
    assert jload(R1 / "manifest.json")["catalogue_sha256"] == want


def test_r07_detects_a_planted_plan_quote(tmp_path):
    gt = jload(FIX / "ground-truth.json")
    quote = next(i["plan_quote"] for i in gt["items"] if len(i.get("plan_quote", "")) >= 12)
    cat = jload(CAT)
    cat["moves"]["M3"] += " " + quote[:20]  # a 12-char window of a quote must be caught
    planted = tmp_path / "planted.json"
    planted.write_text(json.dumps(cat))
    rc, out = catcheck(planted, [FIX / "ground-truth.json"])
    assert rc == 1 and out["pass"] is False and out["hits"]


def test_r07_real_catalogue_has_zero_ground_truth_hits():
    gts = [A1DIR / p / "ground-truth.json" for p in PKGS]
    assert all(g.exists() for g in gts)
    rc, out = catcheck(CAT, gts)
    assert rc == 0 and out == {"ground_truth_files": 3, "hits": [], "pass": True}
