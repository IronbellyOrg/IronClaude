import ast
import json
import pathlib

import pytest

from p15common import harnesslib as H

SP = H.SP
P11 = H.P11


def cfg_for(tmp_path, **kw):
    base = dict(root=tmp_path / "e9", design_id="p15-E9", pattern_root=r"p15/e9", run_rx=r"g9[bc]h?-r\d+",
                decision_path=tmp_path / "decision.toml", loop_steps=["R1", "V1", "R2", "V2", "R3"], coordinator_steps=set())
    base.update(kw)
    return H.ExpConfig(**base)


def p11(run, step):
    return (P11 / "runs" / run / f"PROMPT-{step}.md").read_text()


def test_frozen_shas():
    assert H.sha_text(H.frozen_cmd()) == H.CMD_SHA
    assert H.sha_text(H.frozen_rules()) == H.RULES_SHA
    assert H.arm_rules(cfg_for(pathlib.Path("/nonexistent")), False) == H.frozen_rules()


def test_prompt_identity_r1_v1_r2_aud(tmp_path):
    sb = str(P11 / "runs/a3-r1")
    assert H.wrap(sb, H.new_brief("R1"), True) == p11("a3-r1", "R1")
    assert H.wrap(sb, H.new_brief("V1", "F1, F2"), False) == p11("a3-r1", "V1")
    assert H.wrap(sb, H.new_brief("R2"), True) == p11("a3-r1", "R2")
    # audit: build a real sandbox in a temp experiment dir and compare after replacing the sandbox path
    cfg = cfg_for(tmp_path)
    spec = H.RunSpec(run="g9b-r1", arm="g9b", arm_label="t", stratum="sonnet", block=1, block_order=["g9b"], rep=1)
    H.build_runs(cfg, [spec])
    ad, brief, cmdpart = H.prep_audit(cfg, "g9b-r1", 1)
    assert cmdpart == H.CMDPART
    text = H.wrap(ad, brief, True).replace(str(ad), str(P11 / "runs/a3-r1/aud"))
    assert text == p11("a3-r1", "AUD")
    assert (ad / "command.md").read_text() == H.frozen_cmd()
    st = H.load(cfg, "g9b-r1")
    assert st["schema"] == "p15-run/1" and st["block"] == 1 and st["block_order"] == ["g9b"] and st["stratum"] == "sonnet"
    assert st["cmd_sha"] == H.CMD_SHA and st["rules_sha"] == H.RULES_SHA and st["insertion_sha"] == ""


def test_prompt_identity_r3():
    sb = str(P11 / "runs/a3-r6")
    assert H.wrap(sb, H.new_brief("R3"), True) == p11("a3-r6", "R3")


def anchor_line():
    lines = H.frozen_rules().split("\n")
    for ln in lines:
        if ln.strip() and lines.count(ln) == 1 and len(ln) > 20:
            return ln
    raise AssertionError("no unique line")


def test_insertion_placed_once_after_anchor(tmp_path):
    ins = tmp_path / "ins.txt"
    ins.write_text("INSERTED-LINE-ONE\nINSERTED-LINE-TWO\n")
    anchor = anchor_line()
    cfg = cfg_for(tmp_path, insertion_file=ins, insertion_anchor=anchor)
    rules = H.arm_rules(cfg, True)
    lines = rules.split("\n")
    i = lines.index(anchor)
    assert lines[i + 1:i + 3] == ["INSERTED-LINE-ONE", "INSERTED-LINE-TWO"]
    assert rules.count("INSERTED-LINE-ONE") == 1
    assert [l for j, l in enumerate(H.frozen_rules().split("\n"))] == [l for l in lines if not l.startswith("INSERTED-LINE")]
    bad = cfg_for(tmp_path, insertion_file=ins, insertion_anchor="this line does not exist in the rules")
    with pytest.raises(AssertionError):
        H.arm_rules(bad, True)
    spec = H.RunSpec(run="g9c-r1", arm="g9c", arm_label="t", stratum="sonnet", block=1, block_order=["g9c"], rep=1, uses_insertion=True)
    H.build_runs(cfg, [spec])
    st = H.load(cfg, "g9c-r1")
    assert st["insertion_sha"] == H.sha_text(ins.read_text()) and st["rules_sha"] == H.sha_text(rules)


def test_values_extra_inside_values_sentence():
    extra = ", hints=.dev/orca-command-refactor/review/hints-1.md"
    for step in ("R1", "R2", "R3", "V1"):
        b = H.new_brief(step, "F1", values_extra=extra)
        line = [ln for ln in b.split("\n") if "Values:" in ln][0]
        assert f"{extra}." in line and line.count("Values:") == 1
        assert line.index("Values:") < line.index("hints=")
        assert extra not in H.new_brief(step, "F1")


def write_state(cfg, run, **kw):
    d = cfg.runs_dir / run
    d.mkdir(parents=True, exist_ok=True)
    st = {"run": run, "stratum": "sonnet", "loop_model": "sonnet", "block": 1, "done": [], "log": {}, "launched": {},
          "pending": [], "lost": False, "complete": False, "relaunch": {}, "manual": []}
    st.update(kw)
    json.dump(st, open(d / "state.json", "w"))


def test_launch_never_more_than_max_and_aud_sonnet(tmp_path, capsys):
    cfg = cfg_for(tmp_path)
    for i in range(1, 5):
        write_state(cfg, f"g9b-r{i}", pending=["R1"], block=i)
    write_state(cfg, "g9bh-r1", stratum="haiku", loop_model="haiku", pending=["R1"], block=1)
    write_state(cfg, "g9b-r9", loop_model="haiku", pending=["AUD", "AUD2"], block=1)
    runs = H.run_names(cfg)
    out = H.launch_phase(cfg, runs, 3)
    text = capsys.readouterr().out
    assert len(out) == 3 and text.count("LAUNCH") == 3
    first = text
    assert "g9bh-r1" not in text                    # Sonnet blocks go before Haiku blocks
    assert all(l.endswith("model=sonnet") for l in text.splitlines() if "PROMPT-AUD" in l)
    assert H.launch_phase(cfg, runs, 3) == []        # cap reached by what is running
    H.launch_phase(cfg, runs, 10)
    text = first + capsys.readouterr().out
    assert "PROMPT-AUD.md model=sonnet" in text and "PROMPT-AUD2.md model=sonnet" in text
    assert text.count("LAUNCH") == 7
    assert "g9bh-r1/PROMPT-R1.md model=haiku" in text


def test_coordinator_steps_never_launched(tmp_path, capsys):
    cfg = cfg_for(tmp_path, loop_steps=["R1", "PK1", "V1"], coordinator_steps={"PK1", "J1"})
    write_state(cfg, "g9b-r1", pending=["PK1", "J1", "R1"])
    out = H.launch_phase(cfg, ["g9b-r1"], 6)
    text = capsys.readouterr().out
    assert out == [("g9b-r1", "R1")] and "PK1" not in text and "J1" not in text
    assert H.load(cfg, "g9b-r1")["pending"] == ["PK1", "J1"]


def _line(role, mid, out_tokens, content):
    return json.dumps({"type": role if role == "user" else "assistant", "uuid": mid + str(out_tokens),
                       "message": {"role": role, "id": mid, "model": "claude-sonnet-5-5", "content": content,
                                   "usage": {"output_tokens": out_tokens}}})


def test_scan_transcripts_dedupes_message_ids(tmp_path):
    f = tmp_path / "t1.output"
    first = "Read /x/p15/e9/runs/g9b-r1/PROMPT-R1.md and follow it exactly."
    lines = [json.dumps({"type": "user", "message": {"role": "user", "content": first}}),
             _line("assistant", "m1", 10, [{"type": "text", "text": "a"}]),
             _line("assistant", "m1", 40, [{"type": "text", "text": "a"}]),
             _line("assistant", "m1", 40, [{"type": "text", "text": "a"}]),
             _line("assistant", "m2", 5, [{"type": "tool_use", "name": "SubagentHandback", "input": {"message": "DONE x"}}])]
    f.write_text("\n".join(lines))
    (tmp_path / "other.output").write_text(json.dumps({"type": "user", "message": {"role": "user", "content": "hello"}}))
    found = H.scan_transcripts(str(tmp_path / "*.output"), r"p15/e9", r"g9[bc]h?-r\d+")
    c = found[("g9b-r1", "R1")][0]
    assert c["tokens"] == 45 and c["done"] is True and c["models"] == ["claude-sonnet-5-5"]
    assert H.pick_transcript([c], "haiku", warn=False) is None


def test_attach_tokens_sets_coordinator_zero(tmp_path, monkeypatch):
    cfg = cfg_for(tmp_path, loop_steps=["R1", "PK1"], coordinator_steps={"PK1"}, pattern_root=r"e9")
    write_state(cfg, "g9b-r1", log={"R1": {}, "PK1": {"verdict": "x"}})
    f = tmp_path / "t.output"
    f.write_text("\n".join([json.dumps({"type": "user", "message": {"role": "user", "content": f"Read {cfg.root}/runs/g9b-r1/PROMPT-R1.md and follow it exactly."}}),
                            _line("assistant", "m1", 77, [{"type": "text", "text": "DONE"}])]))
    monkeypatch.setenv("AB_TASKS_GLOB", str(tmp_path / "*.output"))
    H.attach_tokens(cfg)
    log = H.load(cfg, "g9b-r1")["log"]
    assert log["R1"]["output_tokens"] == 77 and log["PK1"]["output_tokens"] == 0 and log["PK1"]["kind"] == "coordinator"


def test_requeue_once_then_lost(tmp_path):
    cfg = cfg_for(tmp_path)
    write_state(cfg, "g9b-r1", launched={"R1": "t"})
    assert H.requeue(cfg, "g9b-r1", "R1", "x") == "requeued"
    assert H.load(cfg, "g9b-r1")["pending"] == ["R1"]
    assert H.requeue(cfg, "g9b-r1", "R1", "x") == "lost"
    assert H.load(cfg, "g9b-r1")["lost"] is True


def test_parse_verify():
    res, ok = H.parse_verify("| F1 | confirm | real |\n| F2 | reject | not in spec |\nconfirmed: F1", ["F1", "F2"])
    assert ok and res["F1"][0] == "confirm" and res["F2"][0] == "reject"
    res, ok = H.parse_verify("garbage", ["F1"])
    assert not ok and res["F1"][0] == "confirm"


def test_telemetry_line(tmp_path):
    cfg = cfg_for(tmp_path, coordinator_steps={"J1"})
    write_state(cfg, "g9b-r1", arm="g9b")
    line = H.telemetry(cfg, "g9b-r1", "J1", {"jev": {"status_counts": {"ok": 2}, "input_tokens": 500}})
    assert line["schema"] == "p15-telemetry/1" and line["kind"] == "coordinator" and line["model"] is None
    assert line["jev_calls"] == 2 and line["output_tokens"] == 0
    assert json.loads((cfg.root / "telemetry.jsonl").read_text().splitlines()[0]) == line


def test_no_cost_check_in_tooling():
    """D6: no comparison of a running token/dollar total against a limit inside any launch or advance function."""
    root = pathlib.Path(H.__file__).parent
    words = ("token", "usd", "cost", "budget", "spent", "dollar")
    bad = []
    for src in root.glob("*.py"):
        tree = ast.parse(src.read_text())
        for fn in ast.walk(tree):
            if isinstance(fn, ast.FunctionDef) and any(k in fn.name for k in ("launch", "advance", "queue", "transitions", "status")):
                for cmp_ in ast.walk(fn):
                    if isinstance(cmp_, ast.Compare):
                        names = [n.id for n in ast.walk(cmp_) if isinstance(n, ast.Name)] + \
                                [n.attr for n in ast.walk(cmp_) if isinstance(n, ast.Attribute)] + \
                                [n.value for n in ast.walk(cmp_) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
                        if any(w in str(x).lower() for x in names for w in words):
                            bad.append((src.name, fn.name, ast.unparse(cmp_)))
    assert not bad, bad
