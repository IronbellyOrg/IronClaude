"""T-19: cleanup removes only the session files of its own row (R-46)."""

import json

from conftest import PKG, TOOLS, run


def test_cleanup_only_own_row(root, tmp_path):
    sb = tmp_path / "sb"
    proj = tmp_path / "projects"
    enc = "".join(c if c.isalnum() else "-" for c in f"{sb}/{PKG}/repo")
    (proj / enc).mkdir(parents=True)
    for row, sid in (("el2-c1-r1", "aaa"), ("el2-c0-r1", "bbb")):
        rv = root / "runs" / row / PKG / "reviews"
        rv.mkdir(parents=True)
        (rv / "t4-1.meta.json").write_text(json.dumps({"session_ids": [sid]}))
        (proj / enc / f"{sid}.jsonl").write_text("{}\n")
    (proj / enc / "aaa-dir.jsonl").mkdir()  # never a directory
    r = run(["bash", str(TOOLS / "cleanup-sessions.sh"), "el2-c1-r1", "--root", str(root), "--sb", str(sb), "--projects", str(proj)])
    assert r.returncode == 0, r.stderr
    assert not (proj / enc / "aaa.jsonl").exists() and (proj / enc / "bbb.jsonl").exists() and (proj / enc / "aaa-dir.jsonl").is_dir()
    assert "DELETED" in (root / "runs" / "el2-c1-r1" / "cleanup.log").read_text()
