"""py/audits.py (DESIGN 2.8, R-07, R-09)."""
import hashlib
import json

from conftest import CANDIDATE, PKGS, R2, REAL_EVAL, SOURCE, pyrun, run

QUOTE = "the guide shows the new wording in every example"


def pkgdir(world):
    pd = world.tmp / "pkg"
    (pd / "reviews").mkdir(parents=True)
    (pd / "sweeper").mkdir()
    (pd / "board/msgs").mkdir(parents=True)
    sb = world.tmp / "sb"
    (sb / "repo").mkdir(parents=True)
    (sb / "cand").mkdir()
    (sb / "repo/a.txt").write_text("results of scoring are elsewhere\n")
    run(["git", "init", "-q"], cwd=sb / "repo", check=True)
    run(["git", "add", "-A"], cwd=sb / "repo", check=True)
    run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "s"], cwd=sb / "repo", check=True)
    (sb / "cand/candidate.md").write_text(CANDIDATE)
    (sb / "cand/source.md").write_text(SOURCE)
    h = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()  # noqa: E731
    (pd / "inputs.json").write_text(json.dumps({"sandbox": str(sb), "candidate_sha256": h(sb / "cand/candidate.md"),
                                                "source_sha256": h(sb / "cand/source.md")}))
    (pd / "board/msgs/board.jsonl").write_text("")
    gt = world.tmp / "gt.json"
    gt.write_text(json.dumps({"items": [{"id": "GT1", "plan_quote": QUOTE, "description": "d"}]}))
    return pd, sb, gt


def tu(name, inp):
    return {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "x", "name": name, "input": inp}]}}


def audit(world, pd, gt):
    r = pyrun("audits.py", "run", "--pkgdir", str(pd), "--gt", str(gt), env=world.env)
    return r.returncode, json.loads((pd / "audit.json").read_text())


def test_clean_fixture_passes(world):
    pd, sb, gt = pkgdir(world)
    hook_cmd = f"/usr/bin/bash {R2}/bin/hooks/receiver-hook.sh --board {world.sbr}/board/x"
    tr = [{"type": "system", "subtype": "hook", "content": hook_cmd}, tu("Read", {"file_path": str(sb / "repo/a.txt")}),
          {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "x", "content": "results of scoring"}]}}]
    (pd / "reviews/t4-1.attempt1.json").write_text(json.dumps(tr))
    assert audit(world, pd, gt) == (0, {"ok": True, "violations": [], "gt_checked": True})


def test_board_12_char_gt_substring(world):
    pd, _, gt = pkgdir(world)
    (pd / "board/msgs/board.jsonl").write_text(json.dumps({"cmd": "grep xx " + QUOTE[4:16] + " yy"}) + "\n")
    rc, a = audit(world, pd, gt)
    assert rc == 1 and a["violations"][0]["rule"] == "ground_truth_text"
    assert a["violations"][0]["where"] == "board.cmd"


def test_board_11_char_ok(world):
    pd, _, gt = pkgdir(world)
    # 11 shared characters, bordered by characters the quote does not have there
    (pd / "board/msgs/board.jsonl").write_text(json.dumps({"cmd": "xx" + QUOTE[4:15] + "yy"}) + "\n")
    assert audit(world, pd, gt)[0] == 0


def test_board_anchor_overlap_is_a_note_not_a_violation(world):
    """Smoke 2026-11-13: an anchor copied from the plan shared " `tests/skil" with a ground-truth quote of the same plan."""
    pd, _, gt = pkgdir(world)
    (pd / "board/msgs/board.jsonl").write_text(json.dumps({"id": "f-0", "anchor": "xx " + QUOTE[4:16] + " yy"}) + "\n")
    rc, a = audit(world, pd, gt)
    assert rc == 0 and a["ok"] and a["violations"] == []
    assert [(n["rule"], n["id"]) for n in a["notes"]] == [("anchor_gt_overlap", "f-0")]
    assert len(a["notes"][0]["hit"]) == 12 and a["notes"][0]["hit"] in QUOTE


def test_gone_sandbox_carries_previous_sandbox_verdicts(world):
    """/tmp sandboxes vanish; a re-audit keeps the read-only verdicts recorded while the sandbox existed."""
    import shutil
    pd, sb, gt = pkgdir(world)
    assert audit(world, pd, gt)[0] == 0
    shutil.rmtree(sb)
    rc, a = audit(world, pd, gt)
    assert rc == 0 and a["sandbox_checks"] == "carried-from-previous-audit"
    (pd / "audit.json").write_text(json.dumps({"ok": False, "violations": [{"rule": "read_only", "detail": "M x"}]}))
    rc, a = audit(world, pd, gt)
    assert rc == 1 and [x["rule"] for x in a["violations"]] == ["read_only"]


def test_gone_sandbox_without_previous_audit_fails_closed(world):
    import shutil
    pd, sb, gt = pkgdir(world)
    shutil.rmtree(sb)
    rc, a = audit(world, pd, gt)
    assert rc == 1 and a["violations"][0]["rule"] == "read_only"


def test_repo_paths_on_the_board_are_not_ground_truth_text(world):
    """Smoke 2026-11-13: items `tests/skills/x.py` overlapped a ground-truth quote that names tests/skills/test_issue_protocol.py."""
    pd, _, gt = pkgdir(world)
    gt.write_text(json.dumps({"items": [{"id": "GT1", "plan_quote": "the whole `tests/skills/test_issue_protocol.py` file passes"}]}))
    line = {"items": ["tests/skills/test_issue_protocol.py:3", "tests/skills/test_worker_contract.py"],
            "cmd": "grep -rln worker tests/skills/test_issue_protocol.py"}
    (pd / "board/msgs/board.jsonl").write_text(json.dumps(line) + "\n")
    assert audit(world, pd, gt)[0] == 0
    line["cmd"] = "grep -rln ' file passes' tests/"   # 12 characters of the quote's prose, not a path
    (pd / "board/msgs/board.jsonl").write_text(json.dumps(line) + "\n")
    rc, a = audit(world, pd, gt)
    assert rc == 1 and a["violations"][0]["where"] == "board.cmd"


def test_board_items_with_gt_substring_still_violate(world):
    pd, _, gt = pkgdir(world)
    (pd / "board/msgs/board.jsonl").write_text(json.dumps({"anchor": "none", "items": [QUOTE[2:20]]}) + "\n")
    rc, a = audit(world, pd, gt)
    assert rc == 1 and a["violations"][0]["where"] == "board.items"


def test_reviewer_reads_ground_truth(world):
    pd, _, gt = pkgdir(world)
    (pd / "reviews/t4-1.attempt1.json").write_text(json.dumps([tu("Read", {"file_path": "/x/20261111-a1/P/ground-truth.json"})]))
    rc, a = audit(world, pd, gt)
    assert rc == 1 and a["violations"][0]["rule"].startswith("reviewer_read:")


def test_sweeper_names_reviews_dir(world):
    pd, _, gt = pkgdir(world)
    (pd / "sweeper/sw-1.json").write_text(json.dumps([tu("Bash", {"command": "ls /tmp/x/reviews/"})]))
    rc, a = audit(world, pd, gt)
    assert rc == 1 and a["violations"][0]["rule"] == "sweeper_read:reviews_dir"


def test_dirty_sandbox(world):
    pd, sb, gt = pkgdir(world)
    (sb / "repo/new.txt").write_text("x")
    rc, a = audit(world, pd, gt)
    assert rc == 1 and a["violations"][0]["rule"] == "read_only"


def test_changed_candidate(world):
    pd, sb, gt = pkgdir(world)
    (sb / "cand/candidate.md").write_text("changed")
    rc, a = audit(world, pd, gt)
    assert rc == 1 and a["violations"][0]["rule"] == "candidate_changed"


def test_real_catalogue_against_real_ground_truth():
    gts = [str(REAL_EVAL / p / "ground-truth.json") for p in PKGS]
    r = pyrun("audits.py", "catalogue", "--gt", *gts)
    assert r.returncode == 0, r.stdout
    assert json.loads(r.stdout)["ok"]


def _brief_text():
    return (R2 / "config/brief-a1.tmpl").read_text()


def test_brief_a1_short_overlap_is_a_note_not_a_violation(world):
    # the shared A1 brief matched designSpec GT3 on ", or when th" and marked the package invalid in every row (fix 2026-11-14)
    pd, _, gt = pkgdir(world)
    gt.write_text(json.dumps({"items": [{"id": "GT1", "plan_quote": "zz cond, or when the literal off line zz", "description": "d"}]}))
    assert ", or when th" in _brief_text()
    rc, a = audit(world, pd, gt)
    assert rc == 0 and a["ok"] and a["violations"] == []
    assert any(n["rule"] == "brief_gt_overlap" and n["where"] == "brief_a1" for n in a["notes"])


def test_brief_a1_long_overlap_still_violates(world):
    pd, _, gt = pkgdir(world)
    flat = " ".join(_brief_text().split())
    gt.write_text(json.dumps({"items": [{"id": "GT1", "plan_quote": "zz " + flat[100:160] + " zz", "description": "d"}]}))
    rc, a = audit(world, pd, gt)
    assert rc == 1
    assert any(x["rule"] == "ground_truth_text" and x["where"] == "brief_a1" for x in a["violations"])
