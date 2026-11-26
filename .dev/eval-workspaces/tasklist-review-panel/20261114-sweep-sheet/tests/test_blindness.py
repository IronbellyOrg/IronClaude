"""DESIGN 9.3 and 11.3: the judge cannot tell the arm. The merged report carries no telemetry (TESTING section 4, REQ-34 blindness)."""

from panel_support import ANCHOR, make_world

KEYS = ("probe", "src", "class", "ledger-v1")


def test_merged_report_has_no_telemetry_keys(tmp_roots):
    w = make_world(tmp_roots)
    r = w.run("SS", "ss", env={"FAKE_PROBE": "first", "FAKE_ANCHOR": ANCHOR})
    assert r.returncode == 0, r.stderr
    assert r.json("run.json")["check_ran"] is True

    # the control: what the merge reads does carry the keys and the ledger block, so the absence below means something
    for rid in ("t2b-1", "t4-1", "t3-1"):
        fed = (r.dir / "normalised" / f"{rid}.md").read_text()
        assert '"probe"' in fed and '"class"' in fed and "ledger-v1" in fed, rid

    merged = r.dir / "merged" / "merged-1.md"
    ledger = r.dir / "merged" / "ledger.json"
    assert merged.read_text().strip() and ledger.read_text().strip()
    assert r.json("run.json")["merge_refused"] is False
    for path in (merged, ledger):
        text = path.read_text()
        for key in KEYS:
            assert key not in text, f"{key!r} found in {path.name}"
