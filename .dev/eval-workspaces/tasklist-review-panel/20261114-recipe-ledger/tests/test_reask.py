"""REQ-27, DR-8: the ember re-ask (rl/reask.py). The condition is tested with a fake clock passed as an argument; the
call, the acceptance rule and the folder version are tested with an injected `run` callable, so no process starts here
(the real call against the fake claude is Task 13).
"""

import json
import re
import time

import pytest
from helpers import SW

from fixtures.reports import make_rl_reports as rep
from rl import cli, ledger_api, reask, rowcheck
from rl import lens as lens_mod

EMBER = "t2b-1"
MODEL = "muse-ember-1.0"
VALUES = lens_mod.values()


def allowed(b, now, role=True, missing=True, asked=False):
    return reask.reask_allowed(role, missing, asked, now, b)


# ---------------------------------------------------------------- the condition (REQ-27)


def test_condition_with_fake_clock():
    # b = 100: the limit is 135 s, so a re-ask may end by 135
    assert allowed(100, 81) and allowed(100, 105)
    assert not allowed(100, 105.01)
    # b = 122: the limit is 164.7 s
    assert allowed(122, 134.7)
    assert not allowed(122, 134.8)


def test_boundary_is_inclusive():
    assert 105 + 30 == pytest.approx(1.35 * 100, abs=1e-9)
    assert allowed(100, 105)
    assert allowed(100, 105 + 5e-10) and not allowed(100, 105 + 5e-9)
    assert allowed(122, 134.7)  # 134.7 + 30 and 1.35 * 122 differ only in the last bits
    assert allowed(0, -30)  # the equality case with a zero b


def test_constants_come_from_values_json():
    assert reask.constants() == (30, 1.35)
    assert VALUES["reask"] == {"fixed_s": 30, "factor": 1.35}


def test_condition_reads_no_wall_clock(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("a clock was read")

    for name in ("time", "monotonic", "perf_counter", "sleep"):
        monkeypatch.setattr(time, name, boom)
    assert allowed(100, 81) and not allowed(100, 106)


def test_never_for_luna_even_with_large_b():
    # luna's role in the lens table has reask false, so no clock and no b can allow it
    for now in (0, 50, 1000):
        assert not allowed(1000, now, role=False)
    table = lens_mod.load()
    for panel in table["panels"].values():
        for role in panel["roles"].values():
            if role["model"] == "gpt-6-luna":
                assert role["reask"] is False


def test_only_when_ledger_missing():
    assert allowed(100, 50)
    assert not allowed(100, 50, missing=False)
    assert not allowed(100, 50, missing=None)


def test_only_once():
    assert allowed(100, 50, asked=False)
    assert not allowed(100, 50, asked=True)


def test_haiku_and_sonnet_never():
    table = lens_mod.load()["panels"]
    assert [r["rid"] for r in table["primary"]["roles"].values() if r["reask"]] == [
        EMBER
    ]
    for name in ("haiku", "sonnet"):
        for role in table[name]["roles"].values():
            assert role["reask"] is False
            assert not allowed(1000, 0, role=role["reask"])


# ---------------------------------------------------------------- the repair prompt (DESIGN 7.6, verbatim)


def design_quote():
    """The blockquote that follows `Draft wording` in DESIGN.md 7.6, with its `> ` marks removed."""
    text = (SW / "DESIGN.md").read_text(encoding="utf-8").splitlines()
    start = next(i for i, ln in enumerate(text) if ln.startswith("**Mechanism.**"))
    after = next(i for i in range(start, len(text)) if text[i].startswith("> "))
    lines = []
    for ln in text[after:]:
        if not ln.startswith(">"):
            break
        lines.append(ln[2:] if ln.startswith("> ") else "")
    return lines


def test_repair_prompt_equals_the_design_quote():
    lines = design_quote()
    assert lines[1:] == ["BEGIN", "{the original final message}", "END"]
    assert reask.REPAIR_HEAD == lines[0]
    assert (
        reask.repair_prompt("{the original final message}") == "\n".join(lines) + "\n"
    )
    # the sentence the fake claude keys on, and the original message sits between the lines BEGIN and END
    assert reask.repair_prompt("x\ny\n").startswith(
        "Your final message was kept as your review"
    )
    assert reask.repair_prompt("x\ny\n").endswith("\nBEGIN\nx\ny\nEND\n")


def test_command_is_the_design_call():
    argv = reask.command(MODEL)
    assert " ".join(argv) == (
        f"timeout 30 claude -p --model {MODEL} --output-format json --no-session-persistence "
        "--permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit"
    )
    assert reask.model_of(argv) == MODEL


def test_default_run_refuses_a_model_outside_the_allowlist_and_a_missing_nofallback(
    monkeypatch,
):
    monkeypatch.setenv("NOFALLBACK", "1")
    with pytest.raises(ValueError, match="E_MODEL"):
        reask.default_run(reask.command("qwen-9"), "x", ".")
    monkeypatch.delenv("NOFALLBACK")
    with pytest.raises(RuntimeError, match="E_NOFALLBACK"):
        reask.default_run(reask.command(MODEL), "x", ".")


# ---------------------------------------------------------------- the acceptance rule


FINDING = rep.finding("F1", rep.Q["ndjson"], "The format name is not defined.")
ROWS = [rep.problem_row("C4.1"), rep.row("C5.1"), rep.row("C6.1"), rep.row("C8.1")]


def original(lines=(FINDING,)):
    return rep.message(rep.findings_part(list(lines)))


def repaired(rows=ROWS, lines=(FINDING,)):
    return rep.standard(rows, list(lines))


def test_original_has_no_ledger():
    assert ledger_api.read(original())["ledger_missing"] is True
    assert ledger_api.read(repaired())["ledger_missing"] is False


def test_accepted_when_ledger_parses_and_findings_equal():
    assert reask.accept(original(), repaired()) == (True, "accepted")
    # other prose may differ; only the ledger and the findings block count
    other = repaired().replace("Two recipe rows", "Four recipe rows")
    assert reask.accept(original(), other)[0] is True
    # equal as parsed JSON lines: spacing inside a line is not a difference
    spaced = json.dumps(json.loads(FINDING), indent=None, separators=(", ", ": "))
    assert reask.accept(original(), repaired(lines=(spaced,)))[0] is True


def test_rejected_when_findings_differ():
    for lines in (
        (rep.finding("F1", rep.Q["ndjson"], "A different claim."),),
        (FINDING, rep.finding("F2", rep.Q["count"], "A second finding.")),
        (),
    ):
        ok, why = reask.accept(original(), repaired(lines=lines))
        assert (ok, why) == (False, "findings_differ"), lines
    # the same lines in another order are not equal either
    two = (FINDING, rep.finding("F2", rep.Q["count"], "A second finding."))
    assert reask.accept(original(two), repaired(lines=two[::-1])) == (
        False,
        "findings_differ",
    )


@pytest.mark.parametrize(
    "name, reason",
    [
        ("ledger_missing", "no_block"),
        ("ledger_after_findings", "ledger_after_findings"),
        ("ledger_twice", "block_twice"),
        ("ledger_unclosed", "unclosed"),
    ],
)
def test_rejected_when_the_ledger_does_not_parse(name, reason):
    bad = rep.build(name).report
    assert reask.accept(bad, bad) == (False, f"ledger_missing:{reason}")


def test_rejected_when_the_repair_breaks_the_findings_block():
    broken = repaired().replace("```findings-v1", "```findings-v1\n```findings-v1")
    assert reask.accept(original(), broken)[0] is False


# ---------------------------------------------------------------- the call, with an injected run


def events(model, message, is_error=False, tokens=40):
    return json.dumps(
        [
            {"type": "system", "subtype": "init", "model": model},
            {
                "type": "assistant",
                "parent_tool_use_id": None,
                "message": {"model": model, "content": []},
            },
            {
                "type": "result",
                "is_error": is_error,
                "result": message,
                "modelUsage": {model: {"outputTokens": tokens}},
            },
        ]
    )


class Runner:
    """An injectable `run` that records its calls and advances a fake clock by `took` seconds per call."""

    def __init__(self, out=None, rc=0, took=12.5, exc=None):
        self.calls, self.out, self.rc, self.took, self.exc = [], out, rc, took, exc
        self.now = 0.0

    def clock(self):
        return self.now

    def __call__(self, argv, stdin, cwd):
        self.calls.append((argv, stdin, cwd))
        self.now += self.took
        if self.exc:
            raise self.exc
        return self.rc, self.out, ""


def test_run_reask_accepted():
    run = Runner(events(MODEL, repaired()))
    rec = reask.run_reask(original(), MODEL, "/tmp/sb", run, run.clock)
    assert rec["accepted"] is True and rec["reason"] == "accepted"
    assert rec["message"] == repaired() and rec["seconds"] == 12.5
    assert rec["model_ok"] and rec["observed_model"] == MODEL
    assert rec["output_tokens_all"] == 40 and rec["killed"] is False
    ((argv, stdin, cwd),) = run.calls
    assert argv == reask.command(MODEL) and cwd == "/tmp/sb"
    assert stdin == reask.repair_prompt(original())


@pytest.mark.parametrize(
    "run, reason",
    [
        (Runner(events(MODEL, repaired(lines=())), took=5), "findings_differ"),
        (Runner(events(MODEL, original()), took=5), "ledger_missing:no_ledger_heading"),
        (Runner(events("claude-haiku-5-5", repaired())), "wrong_model"),
        (Runner(events(MODEL, repaired()), rc=124, took=30), "killed"),
        (Runner(events(MODEL, repaired()), rc=137, took=35), "killed"),
        (Runner(events(MODEL, "API Error: 529", is_error=True)), "call_failed"),
        (Runner(events(MODEL, repaired()), rc=1), "call_failed"),
        (Runner(events(MODEL, "  \n")), "no_result"),
        (Runner("not json"), "no_result"),
        (Runner(exc=FileNotFoundError("claude")), "error:FileNotFoundError"),
    ],
)
def test_run_reask_keeps_the_original_on_any_failure(run, reason):
    rec = reask.run_reask(original(), MODEL, "/tmp/sb", run, run.clock)
    assert rec["accepted"] is False and rec["reason"] == reason
    assert "message" not in rec and rec["asked"] is True
    assert rec["seconds"] == run.took and len(run.calls) == 1


def test_model_identity():
    assert reask.model_ok(MODEL, MODEL) and reask.model_ok(MODEL, MODEL + "-build")
    assert reask.model_ok("Muse-Ember-1.0", MODEL)
    for obs in ("", "<synthetic>", "claude-haiku-5-5", f"{MODEL},claude-haiku-5-5"):
        assert not reask.model_ok(MODEL, obs)


# ---------------------------------------------------------------- the folder version and the subcommand


def make_run(tmp_path, report, asked=None):
    run = tmp_path / "run"
    (run / "lens").mkdir(parents=True)
    (run / "reviews").mkdir()
    for role, r in lens_mod.render("primary", True, 100, VALUES["c"]).items():
        info = dict(r, panel="primary", role=role, doc="d", b=100, has_source=True)
        (run / "lens" / f"{r['rid']}.json").write_text(
            json.dumps(info), encoding="utf-8"
        )
    (run / "reviews" / f"{EMBER}.md").write_text(report, encoding="utf-8")
    if asked is not None:
        (run / "reviews" / f"{EMBER}.reask.json").write_text(
            json.dumps({"asked": asked, "accepted": False, "reason": "call_failed"}),
            encoding="utf-8",
        )
    cand, src = tmp_path / "candidate.md", tmp_path / "source.md"
    cand.write_text(rep.plan_text(), encoding="utf-8")
    src.write_text(rep.source_text(), encoding="utf-8")
    return run, cand, src


def record(run):
    return json.loads(
        (run / "reviews" / f"{EMBER}.reask.json").read_text(encoding="utf-8")
    )


def test_do_reask_accepted_writes_the_files(tmp_path):
    run, _, _ = make_run(tmp_path, original())
    fake = Runner(events(MODEL, repaired()))
    rec = reask.do_reask(run, EMBER, "/tmp/sb", 81, None, fake, fake.clock)
    assert rec["allowed"] and rec["accepted"] and "message" not in rec
    rv = run / "reviews"
    assert (rv / f"{EMBER}.md").read_text(encoding="utf-8") == repaired()
    assert (rv / f"{EMBER}.reask.md").read_text(encoding="utf-8") == repaired()
    assert (rv / f"{EMBER}.preask.md").read_text(encoding="utf-8") == original()
    assert record(run) == rec and rec["seconds"] == 12.5
    assert rec["now_s"] == 81 and rec["b_s"] == 100 and rec["rid"] == EMBER


def test_do_reask_rejected_leaves_the_report(tmp_path):
    run, _, _ = make_run(tmp_path, original())
    fake = Runner(events(MODEL, repaired(lines=())))
    rec = reask.do_reask(run, EMBER, "/tmp/sb", 81, None, fake, fake.clock)
    assert rec["allowed"] and not rec["accepted"] and rec["reason"] == "findings_differ"
    rv = run / "reviews"
    assert (rv / f"{EMBER}.md").read_text(encoding="utf-8") == original()
    assert sorted(p.name for p in rv.iterdir()) == [
        f"{EMBER}.md",
        f"{EMBER}.reask.json",
    ]


def test_do_reask_makes_no_call_when_it_is_not_allowed(tmp_path):
    def never(*a):
        raise AssertionError("a call was made")

    cases = {
        "too_late": (original(), EMBER, 106, None),
        "ledger_present": (repaired(), EMBER, 10, None),
        "role_not_reasked": (original(), "t4-1", 10, None),
    }
    for why, (report, rid, now, b) in cases.items():
        run, _, _ = make_run(tmp_path / why, report)
        if rid != EMBER:
            (run / "reviews" / f"{rid}.md").write_text(report, encoding="utf-8")
        rec = reask.do_reask(run, rid, "/tmp/sb", now, b, never)
        assert (
            rec["allowed"] is False and rec["reason"] == why and rec["asked"] is False
        )
    # --b 1 (the launcher test of a late clock): nothing is allowed
    run, _, _ = make_run(tmp_path / "b1", original())
    assert reask.do_reask(run, EMBER, "/tmp/sb", 5, 1, never)["reason"] == "too_late"


def test_do_reask_only_once(tmp_path):
    run, _, _ = make_run(tmp_path, original())
    fake = Runner(events(MODEL, repaired(lines=())))
    reask.do_reask(run, EMBER, "/tmp/sb", 10, None, fake, fake.clock)
    first = record(run)
    assert first["asked"] and first["reason"] == "findings_differ"
    again = reask.do_reask(run, EMBER, "/tmp/sb", 10, None, fake, fake.clock)
    assert again["allowed"] is False and again["reason"] == "already_asked"
    assert (
        len(fake.calls) == 1 and record(run) == first
    )  # the record of the call is kept


def test_repaired_rows_are_never_promoted(tmp_path):
    """Check 10 of DESIGN 7.2: the repaired ledger may demote, but its PROBLEM row is not promoted (via_reask)."""
    run, cand, src = make_run(tmp_path, original())
    plain = rowcheck.check_run(
        run, cand, src
    )  # no ledger: nothing to promote either way
    assert plain["ledger_missing"] == [EMBER] and plain["promoted"] == 0
    fake = Runner(events(MODEL, repaired()))
    assert reask.do_reask(run, EMBER, "/tmp/sb", 50, None, fake, fake.clock)["accepted"]
    out = rowcheck.check_run(run, cand, src, via_reask=[EMBER])
    assert out["ledger_missing"] == [] and out["rows_per_reviewer"][EMBER] == 4
    assert out["promoted"] == 0 and out["promotion_failures"] == []
    led = json.loads(
        (run / "check" / f"{EMBER}.ledger.json").read_text(encoding="utf-8")
    )
    assert led["via_reask"] is True and led["rows"][0]["supported"]
    assert (run / "check" / f"{EMBER}.checked.md").read_text(
        encoding="utf-8"
    ) == repaired()
    # the same report without the mark is promoted: the mark is what stops it
    out = rowcheck.check_run(run, cand, src)
    assert out["promoted"] == 1


def test_cli_registers_reask_and_keeps_the_other_commands():
    assert list(cli.COMMANDS) == [
        "lens",
        "check",
        "reask",
        "plan",
        "briefs",
        "prepare-merge",
        "record",
    ]
    ns = cli.build_parser().parse_args(
        ["reask", "--run", "r", "--rid", EMBER, "--cwd", "c", "--now-s", "81.5"]
    )
    assert (ns.run_dir, ns.rid, ns.cwd, ns.now_s, ns.b) == ("r", EMBER, "c", 81.5, None)


def test_cli_usage_error_exits_2(capsys):
    assert cli.main(["reask", "--rid", EMBER]) == 2
    assert "--run, --cwd, --now-s" in capsys.readouterr().err


def test_cli_not_allowed_makes_no_call_and_records_it(tmp_path, capsys):
    run, _, _ = make_run(tmp_path, original())
    argv = ["reask", "--run", str(run), "--rid", EMBER, "--cwd", "/tmp/sb"]
    assert cli.main([*argv, "--now-s", "500"]) == 0
    printed = json.loads(capsys.readouterr().out)
    assert printed["allowed"] is False and printed["reason"] == "too_late"
    assert record(run) == printed
    assert (run / "reviews" / f"{EMBER}.md").read_text(encoding="utf-8") == original()


def test_cli_fails_soft_with_the_test_hook(tmp_path, capsys, monkeypatch):
    run, _, _ = make_run(tmp_path, original())
    monkeypatch.setenv("RL_FORCE_EXC", "reask")
    code = cli.main(
        [
            "reask",
            "--run",
            str(run),
            "--rid",
            EMBER,
            "--cwd",
            "/tmp/sb",
            "--now-s",
            "10",
        ]
    )
    cap = capsys.readouterr()
    assert code == 0 and "RL_FORCE_EXC=reask" in cap.err
    rec = record(run)
    assert rec["accepted"] is False and rec["reason"] == "error:RuntimeError"
    assert rec["asked"] is True and json.loads(cap.out) == rec
    assert (run / "reviews" / f"{EMBER}.md").read_text(encoding="utf-8") == original()


def test_cli_fails_soft_on_a_missing_lens_file(tmp_path, capsys):
    run, _, _ = make_run(tmp_path, original())
    (run / "lens" / f"{EMBER}.json").unlink()
    assert (
        cli.main(
            [
                "reask",
                "--run",
                str(run),
                "--rid",
                EMBER,
                "--cwd",
                "/tmp",
                "--now-s",
                "1",
            ]
        )
        == 0
    )
    assert record(run)["reason"] == "error:FileNotFoundError"
    assert re.search(r"reask failed: FileNotFoundError", capsys.readouterr().err)
