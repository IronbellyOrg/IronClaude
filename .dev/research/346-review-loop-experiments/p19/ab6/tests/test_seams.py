"""Mock-transport tests of the ab6 A2 shadow seam, the replay driver and the gate scorer.  No test calls Jev or needs the key."""
import json
import os
import pathlib
import subprocess
import sys

import pytest

import seamlib as S
import a2_observability as A2
import replay as R
import score_gates as G

HERE = pathlib.Path(__file__).resolve().parent.parent
ORIG = S.SP / "p17" / "in" / "spec-original.md"


@pytest.fixture(scope="module")
def orig_text():
    return ORIG.read_text(encoding="utf-8")


@pytest.fixture()
def runner_factory(tmp_path):
    made = []

    def make(seam="a2", mode="ok", **kw):
        r = S.Runner(seam=seam, mode="mock", out_dir=tmp_path / f"{seam}-{mode}-{len(made)}", mock_mode=mode, **kw)
        made.append(r)
        return r
    with S.mock_env():
        yield make


# ----------------------------------------------------------------------------- answer validation
def _item(orig_text):
    _, _, items, _ = A2.build_items(orig_text, pathlib.Path("/tmp") / "ab6-test-scratch", "orig")
    return items[0]


def test_valid_answer_is_usable(runner_factory, orig_text):
    r = runner_factory("a2", "ok", chooser=lambda req: {n: "can_pass" for n in req["questions"]})
    out = r.ask(_item(orig_text))
    assert out["status"] == "ok" and out["usable"] and out["choice"] == "can_pass" and out["fallback"] is None


def test_option_outside_the_question_is_invalid_not_usable(runner_factory, orig_text):
    r = runner_factory("a2", "ok", chooser=lambda req: {n: "can_pass" for n in req["questions"]})
    # a body whose choice is not an option of the question fails the strict validator
    def bad(req):
        body = S._choice_body(req, {n: "can_pass" for n in req["questions"]})
        for a in body["answers"].values():
            a["choice"] = "maybe"
        return S.MockStep(200, body)
    r.transport.script = bad
    out = r.ask(_item(orig_text))
    assert out["status"] == "invalid" and not out["usable"] and out["fallback"].startswith("invalid:")


def test_insufficient_is_a_fallback_with_no_hint(runner_factory, orig_text):
    r = runner_factory("a2", "insufficient")
    out = r.ask(_item(orig_text))
    assert out["status"] == "ok" and not out["usable"] and out["fallback"] == "insufficient"


@pytest.mark.parametrize("mode,reason", [("malformed", "invalid:not_json"), ("timeout", "unavailable:timeout"), ("http500", "unavailable:http_500"),
                                         ("wrongmodel", "invalid:model_mismatch")])
def test_every_error_is_a_fallback(runner_factory, orig_text, mode, reason):
    r = runner_factory("a2", mode)
    out = r.ask(_item(orig_text))
    assert not out["usable"] and out["fallback"] == reason
    if mode in ("timeout", "http500"):
        assert len(r.transport.calls) == 2            # exactly one retry (J1.5), no more




# ----------------------------------------------------------------------------- caps and hint form




def test_a2_line_cap(runner_factory, orig_text, tmp_path):
    r = runner_factory("a2", "ok", chooser=lambda req: {n: "cannot_pass" for n in req["questions"]})
    res = A2.run_spec(orig_text, "orig", tmp_path / "scr", r)
    assert len(res["lines"]) == 8
    assert all("not a finding" in ln and ln.startswith("UNVERIFIED A2-") for ln in res["lines"])




# ----------------------------------------------------------------------------- prefilter determinism and accepted findings






# ----------------------------------------------------------------------------- packet limits, privacy


def test_oversize_packet_is_refused_locally_without_a_call(runner_factory, orig_text):
    r = runner_factory("a2", "ok")
    it = _item(orig_text)
    it["state"]["check"] = "x " * 120_000
    ok, big = R.enforce_packet_limit([it], S.decision())
    assert ok == [] and big == [it]
    out = r.ask(it)                                              # the adapter itself refuses an over-limit request: no call
    assert out["fallback"] == "refused:oversize" and r.transport.calls == []




def test_scrub_removes_everything_the_guard_refuses():
    t = "gh api repos/IronbellyOrg/IronClaude/pulls at /home/coder/x see https://github.com/IronbellyOrg/IronClaude and a@b.example"
    s = S.scrub(t)
    for bad in ("IronbellyOrg", "/home/", "github.com", "@b.example"):
        assert bad not in s




# ----------------------------------------------------------------------------- budget refusal (J4)








def test_dry_run_is_the_default_and_writes_no_answers(monkeypatch, tmp_path):
    monkeypatch.setattr(R, "OUT", tmp_path / "out")
    assert R.main(["--seam", "a2", "--specs", "orig"]) == 0
    assert (tmp_path / "out" / "a2" / "orig.dry.json").exists() and not (tmp_path / "out" / "a2" / "orig.json").exists()


# ----------------------------------------------------------------------------- golden test on the original spec
def test_golden_a2_original(orig_text, tmp_path):
    rows, analysis, items, lint_all = A2.build_items(orig_text, tmp_path / "scr", "orig")
    assert len(rows) == 32 and [r["id"] for r in rows if r["kind"] == "step"] == [f"7.2#{i}" for i in range(1, 8)]
    flagged = {a["id"]: sorted({f["check"] for f in a["code_flags"]}) for a in analysis if a["code_flags"]}
    assert set(flagged) == {"AC-C1", "AC-C4", "AC-C5", "AC-0.3", "AC-0.4"}
    assert "D20" in flagged["AC-C5"] and "D20" in flagged["AC-0.3"] and "D21" in flagged["AC-C1"] and "D21" in flagged["AC-C4"]
    assert "PHASE" in flagged["AC-0.4"] and "EXEC" in flagged["AC-0.4"]                 # lint PHASE (D11) + the YAML-on-markdown execution (D12)
    assert sorted(f["lines"][0] for f in lint_all) == [83, 92, 194]                    # widened lint: PATH, PATH, PHASE
    assert len(items) == 27 and all(i["row_id"] not in flagged for i in items)         # only rows that passed every code check reach Jev
    ac_c4 = next(a for a in analysis if a["id"] == "AC-C4")
    assert any("probe" in e["cmd"] and e.get("flag") for e in ac_c4["exec"])           # the raw table-source copy behaves differently from the unescaped command
    ac_03 = next(a for a in analysis if a["id"] == "AC-0.3")
    assert any(e.get("verdict") == "probe not caught" for e in ac_03["exec"])
    y = next(a for a in analysis if a["id"] == "7.2#4")
    assert any("markdown report: exit 1" in e["verdict"] for e in y["exec"])
    lines = A2.make_lines(analysis, [])
    assert len(lines) == 5 and lines[0].startswith("UNVERIFIED A2-1")                  # five code-flagged rows, no Jev answers






# ----------------------------------------------------------------------------- A3 logic on a synthetic diff
OLD = "\n".join(["# t", "rule one says a", "rule two says b", "rule three says c", "end"])
NEW = "\n".join(["# t", "rule one says A changed", "rule two says b", "rule three says c", "end"])
R2 = """## Blocking findings

### L1

#### L1.t1-1 (F1)

- claim: rule one is still wrong.
- anchor: "rule one says A changed"

### L2

#### L2.t1-1 (F2)

- claim: rule three is wrong.
- anchor: "rule three says c"

## Other findings
"""






# ----------------------------------------------------------------------------- controls




# ----------------------------------------------------------------------------- replay + gates end to end on mock output






# ----------------------------------------------------------------------------- the --live branch rehearsed with a patched network layer (no network, fake key)
