"""The OB-CTX coverage checker must fail when it should."""

import importlib.util
import json
from pathlib import Path

import pytest

PATH = Path(__file__).parent / "fixtures" / "launch_level" / "ob_ctx_check.py"
spec = importlib.util.spec_from_file_location("ob_ctx_check", PATH)
oc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oc)

SID = "3852709b-a75d-4700-b122-1bad0f82d54c"


def line(**over):
    event = {
        "session_id": SID,
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": "echo 1"},
        "tool_use_id": "toolu_01abc",
    }
    event.update(over)
    return {k: v for k, v in event.items() if v is not None}


def run(events, **kw):
    text = "\n".join(json.dumps(e) for e in events)
    return oc.check(oc.jsonl_records(text), [SID], **kw)


def preds(result):
    return [p for p, _, _ in result["violations"]]


def test_good_run_has_no_violations_and_counts_rows():
    prompt = {"session_id": SID, "hook_event_name": "UserPromptSubmit", "prompt": "hi"}
    events = [
        prompt,
        line(),
        line(hook_event_name="PostToolUse"),
        line(tool_input={"run_in_background": True}, tool_use_id="t2"),
        line(tool_name="Monitor", tool_use_id="t3"),
        line(
            agent_id="a1",
            agent_type="general-purpose",
            tool_name="Read",
            tool_use_id="t4",
        ),
        line(tool_name="mcp__x__codegraph_node", tool_use_id="t5"),
    ]
    result = run(events)
    assert result["violations"] == []
    c = result["counts"]
    assert (
        c[("R1", "ups")] == 1
        and c[("R2", "pret_main")] == 1
        and c[("R2", "post_main")] == 1
    )
    assert c[("R3", "pret_main")] == 1 and c[("R4", "pret_main")] == 1
    assert c[("R10", "pret_sub")] == 1 and c[("other", "pret_main")] == 1


@pytest.mark.parametrize(
    "bad, pred",
    [
        (line(session_id=None), "P4"),
        (line(session_id=12345), "P1"),
        (line(session_id="has space"), "P1"),
        (line(agent_id=7, agent_type="x"), "P3"),
        (line(agent_id="a1", agent_type="x", session_id="other-session"), "P3"),
        (line(tool_use_id=None), "P2"),
        (line(tool_input="not an object"), "P2"),
        (line(hook_event_name="Stop"), "P2"),
        ({"session_id": SID, "hook_event_name": "UserPromptSubmit"}, "P2"),
    ],
)
def test_bad_line_is_reported(bad, pred):
    result = run([line(), bad])
    assert pred in preds(result)


def test_empty_file_is_void_not_pass():
    result = oc.check(oc.jsonl_records(""), [SID])
    assert preds(result) == ["VOID"]
    assert oc.render(result).splitlines()[-1] == "OB-CTX-CHECK violations=1"


def test_store_column_skips_absent_lines_and_voids_when_none_governed():
    text = "1\t/h\tunset\t" + json.dumps(line(session_id="coord-1")) + "\tabsent\n"
    result = oc.check(oc.tsv_records(text), store_column=True)
    assert preds(result) == ["VOID"]
    both = text + "2\t/h\tunset\t" + json.dumps(line()) + "\t1 2 /store/" + SID + "\n"
    assert oc.check(oc.tsv_records(both), [SID], store_column=True)["violations"] == []


def test_verdicts_p5():
    gov = json.dumps({"status": "governed", "session_id": SID})
    wrapped = json.dumps({"tool_response": {"stdout": gov + "\n"}})
    assert run([line()], verdict_text=wrapped)["violations"] == []
    assert "P5" in preds(run([line()], verdict_text=""))
    assert "P5" in preds(run([line()], verdict_text=json.dumps({"status": "unknown"})))
    assert "P5" in preds(
        run(
            [line()], verdict_text=json.dumps({"status": "governed", "session_id": "x"})
        )
    )
    three_ordinary = "\n".join([json.dumps({"status": "ordinary"})] * 3)
    assert "P5" in preds(run([line()], verdict_text=three_ordinary))


def test_human_file_p6():
    good = (
        'human shell (cwd /w): {"status": "ordinary"}\n'
        f'governed job child 42 (cwd /w): {{"status": "governed", "session_id": "{SID}"}}\n'
    )
    assert run([line()], human_text=good)["violations"] == []
    assert "P6" in preds(run([line()], human_text=good.replace("ordinary", "governed")))
    assert "P6" in preds(run([line()], human_text="no job found\n"))


def test_complete_p8_needs_every_required_row():
    assert "P8" in preds(run([line()], complete=True))


def test_cli_exit_code_and_final_line(tmp_path, capsys):
    good = tmp_path / "good.jsonl"
    good.write_text(json.dumps(line()) + "\n")
    assert oc.main(["--jsonl", str(good), "--session", SID]) == 0
    assert capsys.readouterr().out.splitlines()[-1] == "OB-CTX-CHECK violations=0"
    empty = tmp_path / "empty.jsonl"
    empty.write_text("")
    assert oc.main(["--jsonl", str(empty)]) == 1
    assert "VOID" in capsys.readouterr().out
