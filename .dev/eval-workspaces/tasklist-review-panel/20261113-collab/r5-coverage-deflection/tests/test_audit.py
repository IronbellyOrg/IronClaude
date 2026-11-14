"""T-18: contamination and read-only audit (R-07, R-09, MR:970)."""
import json

from conftest import CT
from r5 import audit
from test_tagger_collab import make_run


def gt(tmp, quote, desc="nothing here"):
    p = tmp / "gt.json"
    p.write_text(json.dumps({"items": [{"id": "GT1", "plan_quote": quote, "description": desc}]}))
    return [p]


def test_static_window(env):
    cat = env["cfg"] / "catalogue.md"
    cat.write_text(cat.read_text() + "\nM11. zzQWERTYUIOPASzz\n")
    assert not audit.static(gt(env["tmp"], "QWERTYUIOPAS and more"))["ok"]  # 12 shared characters
    assert audit.static(gt(env["tmp"], "QWERTYUIOPA# and more"))["ok"]  # 11 shared characters


def test_static_description_path(env):
    t = env["cfg"] / "templates" / "finish.txt"
    t.write_text(t.read_text() + " refs/zz-only-in-gt.md")
    r = audit.static(gt(env["tmp"], "unrelated quote text", desc="the plan never edits refs/zz-only-in-gt.md"))
    assert not r["ok"] and r["violations"]["finish.txt"][0].endswith(":GT1:path")


def prepare(env):
    d = make_run(env)
    for rid, model in json.loads((d / "run.json").read_text())["models"].items():
        (d / "reviews" / f"{rid}.meta.json").write_text(json.dumps({"model_ok": True, "expected_model": model}))
    text = audit.cov.render_card(["T9"], 2, False)
    (d / "board" / "delivered" / "t1b-1.jsonl").write_text(json.dumps(
        {"id": "c-t1b-1-1", "t": 1, "status": "delivered", "template": "card-1.txt",
         "text_sha256": __import__("hashlib").sha256(text.encode()).hexdigest()}) + "\n")
    return d


def test_package_pass(env):
    d = prepare(env)
    assert audit.package(d)["status"] == "pass"


def test_free_text_card_fails(env):
    d = prepare(env)
    with open(d / "board" / "msgs" / "watcher.jsonl", "a") as f:
        f.write(json.dumps({"v": "panel-msg/1", "id": "c-x", "run": f"row/{CT}", "from": "watcher", "to": "t1b-1", "t": 1,
                            "kind": "coverage", "items": ["T1"], "claim": "free text"}) + "\n")
    r = audit.package(d)
    assert r["status"] == "quarantined" and not r["checks"]["no_free_text"]["ok"]


def transcript(d, path_read):
    (d / "reviews" / "t4-1.attempt1.json").write_text(json.dumps([
        {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Read", "input": {"file_path": path_read}}]}}]))


def test_transcript_reflect_fails(env):
    d = prepare(env)
    transcript(d, "/tmp/x/.dev/reflect/x")
    assert not audit.package(d)["checks"]["transcripts"]["ok"]


def test_transcript_other_session_fails(env):
    d = prepare(env)
    transcript(d, "/home/coder/.claude/projects/-tmp-x/abc.jsonl")
    assert not audit.package(d)["checks"]["transcripts"]["ok"]


def test_dirty_sandbox_fails(env):
    d = prepare(env)
    (env["sb"] / CT / "repo" / "new.txt").write_text("x")
    assert not audit.package(d)["checks"]["read_only"]["ok"]


def test_changed_candidate_fails(env):
    d = prepare(env)
    c = env["sb"] / "cand" / CT / "candidate.md"
    c.write_text(c.read_text() + "x")
    assert not audit.package(d)["checks"]["read_only"]["ok"]
