"""bin/reviewer.sh argv against RR:48 (design section 4; R-05) and its H2/retry paths."""

import hashlib
import json
import re
import shlex
from pathlib import Path

from r4help import DE, EVAL, R4, fixture, jsonl, make_sbr, now_ms, run


def rr48_tokens():
    line = (EVAL / "tools" / "run-reviewer.sh").read_text().splitlines()[47]
    seg = line[line.index("claude -p"):line.index(" <<<")]
    return shlex.split(seg.replace('"$MODEL"', "MODEL"))


def panel(env, tmp_path, k=1, settings=None, hang_s=60):
    make_sbr(env, [DE])
    sbr = Path(env["R4_SBR"])
    cand = sbr / "cand" / DE / "candidate.md"
    pd = tmp_path / "row" / DE
    (pd / "reviews").mkdir(parents=True)
    t0 = now_ms()
    (pd / "panel.json").write_text(json.dumps({
        "pkg": DE, "sandbox": str(sbr / "sb" / DE / "repo"), "cand": str(cand), "src": str(sbr / "cand" / DE / "source.md"),
        "cand_sha": hashlib.sha256(cand.read_bytes()).hexdigest(), "t0_ms": t0, "hang_ms": t0 + hang_s * 1000, "finish_ms": t0 + 30_000,
        "k": k, "settings": settings or {}, "helper": str(sbr / "board" / "bin" / "card")}))
    return pd


def argv_log(env):
    return jsonl(Path(env["FAKE_LOG"]) / "argv.jsonl")


def check_argv(argv, model, extra=()):
    exp = rr48_tokens()
    exp.remove("--no-session-persistence")
    exp = [model if t == "MODEL" else t for t in exp]
    i = argv.index("--session-id")
    assert re.fullmatch(r"[0-9a-f-]{36}", argv[i + 1])
    got = argv[:i] + argv[i + 2:]
    exp_after = exp[1:]  # drop the program name
    exp_after.insert(exp_after.index("--permission-mode"), "__SID__")
    exp_after.remove("__SID__")
    assert got == exp_after + list(extra)


def test_a1_argv(env, tmp_path):
    fixture(env, {"default": {"calls": 1}}, tmp_path)
    pd = panel(env, tmp_path)
    r = run(["bash", R4 / "bin" / "reviewer.sh", pd, "t4-1", "gpt-6-luna", "adjudicator", 0], env=env)
    assert r.returncode == 0, r.stderr
    log = argv_log(env)
    assert len(log) == 1
    check_argv(log[0]["argv"], "gpt-6-luna")
    assert log[0]["cwd"].endswith(f"sb/{DE}/repo")
    assert not log[0]["brief_has_adjudicator"] and not log[0]["brief_has_flagger"]
    meta = json.load(open(pd / "reviews" / "t4-1.meta.json"))
    assert meta["model_ok"] and meta["final_ok"] and meta["attempts"] == 1 and meta["retry_isolated"] is False
    assert (pd / "reviews" / "t4-1.transcript.jsonl").exists() and (pd / "reviews" / "t4-1.final.md").exists()
    assert set(json.load(open(pd / "reviews" / "t4-1.cost.json"))) == {"attempts", "total_wall_s", "total_output_tokens_all"}


def test_collab_argv_adds_only_settings(env, tmp_path):
    fixture(env, {"default": {"calls": 1}}, tmp_path)
    sf = tmp_path / "settings.json"
    sf.write_text(json.dumps({"hooks": {}}))
    pd = panel(env, tmp_path, settings={"t4-1": str(sf)})
    run(["bash", R4 / "bin" / "reviewer.sh", pd, "t4-1", "gpt-6-luna", "adjudicator", 1], env=env)
    a = argv_log(env)[0]
    check_argv(a["argv"], "gpt-6-luna", extra=("--settings", str(sf)))
    assert a["brief_has_adjudicator"] and not a["brief_has_flagger"]


def test_flagger_brief(env, tmp_path):
    fixture(env, {"default": {"calls": 1}}, tmp_path)
    pd = panel(env, tmp_path, k=2)
    run(["bash", R4 / "bin" / "reviewer.sh", pd, "t2b-1", "muse-ember-1.0", "flagger", 1], env=env)
    assert argv_log(env)[0]["brief_has_flagger"]


def test_k0_brief_isolated(env, tmp_path):
    fixture(env, {"default": {"calls": 1}}, tmp_path)
    pd = panel(env, tmp_path, k=0)
    run(["bash", R4 / "bin" / "reviewer.sh", pd, "t4-1", "gpt-6-luna", "adjudicator", 1], env=env)
    a = argv_log(env)[0]
    assert not a["brief_has_adjudicator"] and "--settings" not in a["argv"]
