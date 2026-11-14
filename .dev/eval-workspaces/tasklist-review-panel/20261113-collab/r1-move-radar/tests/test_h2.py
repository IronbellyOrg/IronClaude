"""T-11: H2 normaliser and the one re-ask (R-02)."""

import json

from conftest import (
    FIX,
    REPO,
    TOOLS,
    finding,
    jload,
    json_reply,
    report,
    run,
    stream_reply,
)

from superclaude.cli.review import findings as fnd

CAND = (FIX / "cand" / "candidate.md").read_text()
LONG = CAND[CAND.index("The guard keeps"):].strip()


def h2(tmp_path, text):
    src, out, errs = tmp_path / "in.md", tmp_path / "out.md", tmp_path / "h2.json"
    src.write_text(text)
    r = run(["uv", "run", "python", str(TOOLS / "h2_normalize.py"), str(src), str(out), str(errs)], cwd=REPO)
    assert r.returncode == 0, r.stderr
    return out.read_text(), jload(errs)


def h2_bytes(tmp_path, text):
    """Like h2() but byte-exact: write the input raw, return the raw output text (no newline conversion)."""
    src, out, errs = tmp_path / "inb.md", tmp_path / "outb.md", tmp_path / "h2b.json"
    src.write_bytes(text.encode())
    r = run(["uv", "run", "python", str(TOOLS / "h2_normalize.py"), str(src), str(out), str(errs)], cwd=REPO)
    assert r.returncode == 0, r.stderr
    return out.read_bytes().decode(), jload(errs)


def test_crlf_only_block_line_changes(tmp_path):
    text = report(finding(claim="y" * 400)).replace("\n", "\r\n")
    out, e = h2_bytes(tmp_path, text)
    a, b = text.splitlines(keepends=True), out.splitlines(keepends=True)
    assert len(a) == len(b) and all(x.endswith("\r\n") for x in b)
    assert [i for i, (x, y) in enumerate(zip(a, b)) if x != y] == [a.index(json.dumps(finding(claim="y" * 400)) + "\r\n")]
    assert e["ok"] and e["truncated"] == 1 and e["dropped_lines"] == 0


def test_cr_only_report_left_byte_identical(tmp_path):
    text = report(finding(claim="y" * 400)).replace("\n", "\r")
    out, e = h2_bytes(tmp_path, text)
    assert out.encode() == text.encode() and e["truncated"] == 0
    assert e["ok"] == fnd.parse_block(text)["ok"]  # the merge reads the same raw text (merge_cmd._read, newline="")


def test_long_anchor_truncated_and_still_located(tmp_path):
    anchor = LONG[:250]
    assert len(anchor) == 250
    out, e = h2(tmp_path, report(finding(anchor=anchor)))
    f = fnd.parse_block(out)["findings"][0]
    assert len(f["anchor"]) <= 200 and anchor.startswith(f["anchor"]) and e["ok"] and e["truncated"] == 1
    assert fnd.locate(CAND, f["anchor"])


def test_long_claim_truncated(tmp_path):
    out, e = h2(tmp_path, report(finding(claim="x" * 400)))
    assert len(fnd.parse_block(out)["findings"][0]["claim"]) == 300 and e["ok"]


def test_bad_severity_reported(tmp_path):
    _, e = h2(tmp_path, report(finding(), finding(id="F2", severity="HIGH")))
    assert not e["ok"] and any("severity" in x["msg"] for x in e["errors"])


def test_only_block_lines_rewritten(tmp_path):
    text = report(finding(claim="y" * 400))
    out, _ = h2(tmp_path, text)
    a, b = text.splitlines(), out.splitlines()
    assert len(a) == len(b) and [i for i, (x, y) in enumerate(zip(a, b)) if x != y] == [a.index(json.dumps(finding(claim="y" * 400)))]


def _bad():
    return report(finding(), finding(id="F2", severity="HIGH"))


def test_reask_still_bad_drops_line(runner):
    runner.plan(f"replay {runner.file(json_reply(_bad()))}", f"replay {runner.file(stream_reply(_bad()))}")
    r = runner.run(collab=0)
    assert r.returncode == 0, r.stderr
    m = runner.meta()
    assert m["dropped_lines"] == 1 and isinstance(m["reask_s"], (int, float)) and runner.calls() == 2
    a2 = runner.argv(2)
    assert "--resume" in a2 and a2[a2.index("--resume") + 1] == "sess-1" and "stream-json" in a2 and "--settings" not in a2
    assert "parser errors" in (runner.stub / "stdin.2").read_text()


def test_reask_good_gives_zero_dropped(runner):
    runner.plan(f"replay {runner.file(json_reply(_bad()))}", f"replay {runner.file(stream_reply(report(finding())))}")
    assert runner.run(collab=0).returncode == 0
    m = runner.meta()
    assert m["dropped_lines"] == 0 and m["reask_s"] is not None
    assert fnd.parse_block((runner.d / "reviews" / "t2b-1.md").read_text())["ok"]
    assert jload(runner.d / "reviews" / "t2b-1.cost.json")["total_output_tokens_all"] == 150  # attempt 100 + re-ask 50


def test_no_reask_when_clean(runner):
    runner.plan(f"replay {runner.file(json_reply(report(finding())))}")
    assert runner.run(collab=0).returncode == 0
    assert runner.calls() == 1 and runner.meta()["reask_s"] is None and runner.meta()["dropped_lines"] == 0


def test_dropped_counts_lines_not_errors(tmp_path):
    # one bad line among two: 1 dropped, 1 kept
    _, e = h2(tmp_path, report(finding(), finding(id="F2", severity="HIGH")))
    assert e["dropped_lines"] == 1 and e["kept_lines"] == 1
    # wrong heading: the parser keeps nothing, both block lines are dropped (one line-0 error only)
    text = report(finding(), finding(id="F2")).replace("## Findings block", "## Findings")
    _, e = h2(tmp_path, text)
    assert len(e["errors"]) == 1 and e["dropped_lines"] == 2 and e["kept_lines"] == 0
    # two blocks: a block-level notice, no dropped line
    two = report(finding()) + "\n```findings-v1\n" + json.dumps(finding(id="F9")) + "\n```\n"
    _, e = h2(tmp_path, two)
    assert not e["ok"] and e["dropped_lines"] == 0 and e["kept_lines"] == 1


def test_runner_wrong_heading_reports_all_lines_dropped(runner):
    text = report(finding(), finding(id="F2")).replace("## Findings block", "## Findings")
    runner.plan(f"replay {runner.file(json_reply(text))}", f"replay {runner.file(stream_reply(text))}")
    assert runner.run(collab=0).returncode == 0
    assert runner.meta()["dropped_lines"] == 2 and runner.calls() == 2


def test_reask_with_fewer_kept_lines_is_not_taken(runner):
    runner.plan(f"replay {runner.file(json_reply(_bad()))}", f"replay {runner.file(stream_reply(report()))}")
    assert runner.run(collab=0).returncode == 0
    m = runner.meta()
    assert m["dropped_lines"] == 1 and len(fnd.parse_block((runner.d / "reviews" / "t2b-1.md").read_text())["findings"]) == 1


def test_other_line_separators_before_block(tmp_path):
    # U+2028 and a form feed in the prose: splitlines() counts them as line breaks, so the rewrite must too
    text = report(finding(claim="z" * 400)).replace("Covered everything.", "Covered\u2028every\x0cthing.")
    out, e = h2(tmp_path, text)
    assert e["ok"] and e["dropped_lines"] == 0 and e["truncated"] == 1
    assert len(fnd.parse_block(out)["findings"][0]["claim"]) == 300
    assert out.replace(json.dumps(finding(claim="z" * 300)), "X") == text.replace(json.dumps(finding(claim="z" * 400)), "X")
