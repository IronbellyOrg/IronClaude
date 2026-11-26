import json

from conftest import finding

from r3lib import findings_io


def stream(path, chunks, result=None):
    ev = [{"type": "system", "subtype": "init", "session_id": "s"}]
    ev += [
        {
            "type": "assistant",
            "message": {"model": "m", "content": [{"type": "text", "text": c}]},
        }
        for c in chunks
    ]
    if result is not None:
        ev.append({"type": "result", "result": result, "session_id": "s"})
    path.write_text("\n".join(json.dumps(e) for e in ev) + "\n")
    return path


def test_salvage_two_complete(tmp_path):
    c1, c2 = json.dumps(finding("C1", "only")), json.dumps(finding("C2", "never"))
    s = stream(tmp_path / "s.jsonl", [c1 + "\n", c2 + "\n", c1[:40]])
    lines, log = findings_io.extract_p2_lines(s)
    assert [x["id"] for x in lines] == ["C1", "C2"] and log["p2_lines_salvaged"] == 2


def test_repeat_last_wins_and_non_c_ignored(tmp_path):
    a = finding("C1", "only", claim="first")
    b = finding("C1", "only", claim="second")
    x = finding("F9", "never")
    s = stream(
        tmp_path / "s.jsonl",
        [json.dumps(a) + "\n" + json.dumps(x) + "\n" + json.dumps(b) + "\n"],
    )
    lines, _ = findings_io.extract_p2_lines(s)
    assert len(lines) == 1 and lines[0]["claim"] == "second"


def test_result_block_wins(tmp_path):
    c1 = json.dumps(finding("C1", "only", claim="from text"))
    r = (
        "## Findings block\n```findings-v1\n"
        + json.dumps(finding("C1", "only", claim="from result"))
        + "\n```\nverdict: PASS\n"
    )
    s = stream(tmp_path / "s.jsonl", [c1 + "\n"], result=r)
    lines, log = findings_io.extract_p2_lines(s)
    assert lines[0]["claim"] == "from result" and log["p2_lines_salvaged"] == 0
