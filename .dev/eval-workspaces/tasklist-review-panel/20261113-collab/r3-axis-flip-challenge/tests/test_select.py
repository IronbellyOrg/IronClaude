import json

from conftest import R3, candidate, finding

from r3lib import digest

CAND = candidate()
ROUTING = json.loads((R3 / "config/routing.json").read_text())


def test_selection():
    fs = [
        finding("F1", "only", "unpassable-check"),
        finding(
            "F2",
            "never",
            "missing-requirement",
            claim="The artifact path artifacts/x.md is outside the edit scope.",
        ),
        finding("F3", "reread", "contradiction"),
        finding(
            "F4", "cmd", "unpassable-check", claim="The check at line 162 cannot pass."
        ),
        finding("F5", "every", "data-loss"),
        finding("F6", "mustnot", "other"),
        finding("F7", "This sentence is not in the candidate at all", "contradiction"),
        finding("F8", "every", "missing-requirement"),
    ]
    log = []
    sel = digest.select(fs, CAND, ROUTING, "reading", log)
    assert [f["id"] for f in sel] == ["F1", "F3", "F8"]
    reasons = {x["id"]: x["reason"] for x in log}
    assert reasons["F2"] == "skipped_surface" and reasons["F4"] == "skipped_surface"
    assert reasons["F5"] == "skipped_category" and reasons["F6"] == "skipped_category"
    assert reasons["F7"] == "skipped_anchor_missing"
