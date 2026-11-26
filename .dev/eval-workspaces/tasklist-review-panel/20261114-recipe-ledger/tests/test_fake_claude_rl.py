"""F-FAKE-RL (TESTING section 2): the fake claude is first on PATH and each of its scenarios behaves as the
integration tests expect. The repair scenario is shown to give a message that rl.reask accepts. No model starts.
"""

import json
import os
import shutil
import subprocess
import time

import pytest
import rl_support as s
from conftest import FAKES, assert_fake_first
from helpers import SW

from rl import ledger_api as api
from rl import reask, render
from scaffold import fnd

EMBER = "muse-ember-1.0"
LUNA = "gpt-6-luna"
SCENARIOS = (
    "ok",
    "problem",
    "none_found",
    "ledger_missing",
    "ledger_after_findings",
    "over_budget",
    "recipe_missing",
    "long_anchor",
    "bad_block",
    "api_error",
    "wrong_model",
    "sleep",
    "exit127",
)
ROLE = s.roles("primary")["S"]  # the ember role: C4 C5 C6 C8, four rows each
CLASSES = ROLE["recipes"]
PLAN = SW / "fixtures" / "plans" / "p_basic.md"


@pytest.fixture
def brief(tmp_path):
    """The ember brief of the primary panel, naming a candidate copy under tmp_path."""
    cand = tmp_path / "candidate.md"
    cand.write_text(PLAN.read_text(encoding="utf-8"), encoding="utf-8")
    doc = {"cand_sb": str(cand), "sha": s.SHA}
    return render.brief(ROLE, doc, s.SOURCE)["text"], fnd.flat(cand.read_text())


def call(roots, brief_text, scenario="ok", model=EMBER, **extra):
    env = roots.with_env(FAKE_SCENARIO=scenario, **extra)
    assert shutil.which("claude", path=env["PATH"]) == str(FAKES / "claude")
    return subprocess.run(
        ["claude", "-p", "--model", model, "--output-format", "json"],
        input=brief_text,
        capture_output=True,
        text=True,
        env=env,
        timeout=30,
        cwd=roots.root,
    )


def parts(r):
    ev = json.loads(r.stdout)
    return ev, ev[-1]


def log(roots):
    if not roots.call_log.exists():
        return []
    return [ln.split("\t") for ln in roots.call_log.read_text().splitlines()]


def row_ids(report):
    return [r["item"] for r in api.read(report)["rows"]]


def expected_ids(extra=0):
    return [f"{c}.{k}" for c in CLASSES for k in range(1, 4 + extra + 1)]


def test_first_claude_on_path_is_the_fake(tmp_roots):
    env = tmp_roots.with_env()
    assert shutil.which("claude", path=env["PATH"]) == str(FAKES / "claude")
    assert_fake_first(env)
    env["PATH"] = env["PATH"].split(os.pathsep, 1)[
        1
    ]  # without the fakes folder first, the check fails
    with pytest.raises(AssertionError):
        assert_fake_first(env)


def test_scenarios_and_call_log(tmp_roots, brief):
    text, cand = brief
    for i, scen in enumerate(SCENARIOS, start=1):
        r = call(tmp_roots, text, scen, FAKE_SLEEP_S="0.2")
        if scen == "exit127":
            assert r.returncode == 127 and r.stdout == ""
            assert "command not found" in r.stderr
        else:
            assert r.returncode == 0, (scen, r.stderr)
            events, res = parts(r)
            types = [e["type"] for e in events]
            tooled = ["system", "assistant", "user", "assistant", "result"]
            assert types == (
                tooled
                if scen in ("problem", "none_found")
                else ["system", "assistant", "result"]
            ), scen
            check_scenario(scen, events, res["result"], cand)
        lines = log(tmp_roots)
        assert len(lines) == i, scen
        stamp, name, model, kind = lines[-1]
        assert float(stamp) > 1e9 and (name, model, kind) == (scen, EMBER, "review")


def check_scenario(scen, events, report, cand):
    res = events[-1]
    obs = events[1]["message"]["model"]
    assert events[0]["subtype"] == "init" and events[0]["model"] == EMBER
    if scen == "api_error":
        assert obs == "<synthetic>" and res["is_error"]
        assert report.startswith("API Error") and list(res["modelUsage"]) == [obs]
        return
    assert obs == (EMBER if scen != "wrong_model" else "claude-haiku-5-5")
    assert not res["is_error"] and list(res["modelUsage"]) == [obs]
    ledger, block = api.read(report), fnd.parse_block(report)
    if scen in ("ok", "sleep"):
        assert row_ids(report) == expected_ids() and not ledger["ledger_missing"]
        assert [r["verdict"] for r in ledger["rows"]] == ["OK"] * 16
        assert block["ok"] and len(block["findings"]) == 1
        assert fnd.flat(block["findings"][0]["anchor"]) in cand
        assert report.index("## Ledger") < report.index("## Findings block")
        assert report.startswith("review: 1 of 3\n")
    elif scen == "problem":
        problems = [r for r in ledger["rows"] if r["verdict"] == "PROBLEM"]
        assert [p["item"] for p in problems] == ["C4.1"]
        row = api.check(problems, {"candidate": cand})[0]
        assert row["quote_plan_ok"] and row["quote_other_ok"] and row["supported"]
        assert row["corpus"] == "candidate"
        finding = block["findings"][0]
        assert finding["blocking"] and fnd.flat(row["quote_plan"]) in fnd.flat(
            finding["anchor"]
        )
        assert (
            "An implementer who follows the stated text as written builds"
            in finding["claim"]
        )
        use, result = (
            events[1]["message"]["content"][0],
            events[2]["message"]["content"][0],
        )
        assert use["name"] == "Bash" and result["tool_use_id"] == use["id"]
        assert fnd.flat(row["quote_plan"]) in fnd.flat(result["content"])
        linked = api.link_demote(report, api.check(ledger["rows"], {"candidate": cand}))
        assert linked["links"] == {"F1": "C4.1"} and not any(linked["demoted"].values())
    elif scen == "none_found":
        assert row_ids(report) == [f"{c}.1" for c in CLASSES]
        assert all(
            r["ran"] == "NONE FOUND" and not r["quote_plan"] for r in ledger["rows"]
        )
        assert (
            events[2]["message"]["content"][0]["content"] == ""
        )  # a search with no hit
    elif scen == "ledger_missing":
        assert ledger["ledger_missing"] and block["ok"] and "ledger-v1" not in report
    elif scen == "ledger_after_findings":
        assert ledger["ledger_missing"] and ledger["reason"] == "ledger_after_findings"
        assert block["ok"] and "```ledger-v1" in report
    elif scen == "over_budget":
        assert row_ids(report) == expected_ids(extra=1)
    elif scen == "recipe_missing":
        assert row_ids(report) == [i for i in expected_ids() if not i.startswith("C8.")]
        assert block["ok"]
    elif scen == "long_anchor":
        anchor = block["findings"][0]["anchor"] if block["ok"] else None
        assert anchor is None  # the parser refuses an anchor above 200 characters
        long = [ln for ln in report.splitlines() if ln.startswith('{"id":"F1"')][0]
        assert len(json.loads(long)["anchor"]) == 250
        assert json.loads(long)["anchor"] in cand
    elif scen == "bad_block":
        assert not block["ok"] and "not valid JSON" in block["errors"][0]["msg"]
        assert not ledger["ledger_missing"]
    elif scen == "wrong_model":
        assert obs != EMBER


def test_unknown_scenario_and_hand_set_repair_are_refused(tmp_roots, brief):
    text, _ = brief
    r = call(tmp_roots, text, "nope")
    assert r.returncode == 2 and "unknown FAKE_SCENARIO" in r.stderr
    r = call(tmp_roots, text, "repair")
    assert r.returncode == 2 and "repair brief" in r.stderr


def test_scenario_by_model(tmp_roots, brief):
    text, _ = brief
    by_model = f"{EMBER}=ledger_missing {LUNA}=none_found"
    for model in (EMBER, LUNA, "claude-haiku-5-5"):
        r = call(tmp_roots, text, "ok", model, FAKE_SCENARIO_BY_MODEL=by_model)
        assert r.returncode == 0
    assert [(m, n) for _, n, m, _ in log(tmp_roots)] == [
        (EMBER, "ledger_missing"),
        (LUNA, "none_found"),
        ("claude-haiku-5-5", "ok"),
    ]


def test_sleep_waits_and_dies_on_term(tmp_roots, brief):
    text, _ = brief
    t = time.monotonic()
    assert call(tmp_roots, text, "sleep", FAKE_SLEEP_S="0.5").returncode == 0
    assert time.monotonic() - t >= 0.5
    p = subprocess.Popen(
        ["claude", "-p"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        env=tmp_roots.with_env(FAKE_SCENARIO="sleep", FAKE_SLEEP_S="30"),
    )
    p.stdin.write(text)
    p.stdin.close()
    time.sleep(0.5)
    p.terminate()
    assert p.wait(timeout=5) == 143


# ---------------------------------------------------------------- repair


def first_message(roots, text, scenario):
    return parts(call(roots, text, scenario))[1]["result"]


@pytest.mark.parametrize("scenario", ["ledger_missing", "ledger_after_findings"])
def test_repair_keeps_the_findings_block_and_is_accepted(tmp_roots, brief, scenario):
    text, _ = brief
    original = first_message(tmp_roots, text, scenario)
    assert api.read(original)["ledger_missing"]
    # the variables still name the broken scenario: the brief alone selects the repair
    r = call(tmp_roots, reask.repair_prompt(original), scenario)
    assert r.returncode == 0
    events, res = parts(r)
    assert [e["type"] for e in events] == ["system", "assistant", "result"]
    repaired = res["result"]
    assert [x[1:] for x in log(tmp_roots)[-1:]] == [["repair", EMBER, "repair"]]
    assert row_ids(repaired) == [f"{c}.1" for c in CLASSES]
    assert repaired.count("## Ledger") == 1 and repaired.count("```ledger-v1") == 1
    assert repaired.index("## Ledger") < repaired.index("## Findings block")
    assert (
        fnd.parse_block(repaired)["findings"] == fnd.parse_block(original)["findings"]
    )
    assert reask._findings_lines(repaired) == reask._findings_lines(original)
    assert reask.accept(original, repaired) == (True, "accepted")


def test_run_reask_calls_the_fake_and_accepts(tmp_roots, brief):
    text, _ = brief
    original = first_message(tmp_roots, text, "ledger_missing")
    env = tmp_roots.with_env(FAKE_SCENARIO="ledger_missing")

    def run(argv, stdin_text, cwd):
        p = subprocess.run(
            argv, input=stdin_text, capture_output=True, text=True, env=env, cwd=cwd
        )
        return p.returncode, p.stdout, p.stderr

    rec = reask.run_reask(original, EMBER, tmp_roots.root, run=run)
    assert rec["accepted"] and rec["reason"] == "accepted" and rec["model_ok"]
    assert not api.read(rec["message"])["ledger_missing"]
    assert [x[1:] for x in log(tmp_roots)] == [
        ["ledger_missing", EMBER, "review"],
        ["repair", EMBER, "repair"],
    ]


def test_repair_switches(tmp_roots, brief):
    """FAKE_REPAIR_EDIT makes the repaired findings block differ (the re-ask must reject it); FAKE_REPAIR_PROBLEM adds a
    PROBLEM row whose plan quote no findings line is linked to (the check must not promote it)."""
    text, _ = brief
    original = first_message(tmp_roots, text, "ledger_missing")
    edited = parts(
        call(tmp_roots, reask.repair_prompt(original), FAKE_REPAIR_EDIT="1")
    )[1]["result"]
    assert not api.read(edited)["ledger_missing"]
    assert reask._findings_lines(edited) != reask._findings_lines(original)
    assert reask.accept(original, edited) == (False, "findings_differ")
    cand = tmp_roots.root / "candidate.md"
    probed = parts(
        call(
            tmp_roots,
            reask.repair_prompt(original),
            FAKE_REPAIR_PROBLEM="1",
            FAKE_CAND=str(cand),
        )
    )[1]["result"]
    assert reask.accept(original, probed) == (True, "accepted")
    first = api.read(probed)["rows"][0]
    flat = fnd.flat(cand.read_text())
    assert first["verdict"] == "PROBLEM" and first["item"] == f"{CLASSES[0]}.1"
    assert (
        fnd.flat(first["quote_plan"]) in flat and fnd.flat(first["quote_other"]) in flat
    )
    assert first["quote_plan"] != first["quote_other"]
    assert first["quote_plan"] not in fnd.parse_block(probed)["findings"][0]["anchor"]
