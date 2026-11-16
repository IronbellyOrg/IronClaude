"""F-FAKE: the fake claude is first on PATH and each of its eight scenarios behaves as the integration tests expect."""

import json
import re
import subprocess
import time

import pytest
from conftest import FAKES, assert_fake_first
from superclaude.cli.review import findings as fnd

BRIEF = "Review plan items S3 and S7.\nreview: 1 of 3\n"
SCENARIOS = (
    "ok",
    "ledger_missing",
    "long_anchor",
    "api_error",
    "wrong_model",
    "sleep",
    "bad_block",
    "exit127",
)


def run_fake(roots, scenario, model="claude-sonnet-5-5", **extra):
    env = roots.with_env(FAKE_SCENARIO=scenario, **extra)
    return subprocess.run(
        ["claude", "-p", "--model", model, "--output-format", "json"],
        input=BRIEF,
        capture_output=True,
        text=True,
        env=env,
        timeout=30,
    )


def parts(r):
    ev = json.loads(r.stdout)
    assert [e["type"] for e in ev] == ["system", "assistant", "result"]
    return ev[1]["message"]["model"], ev[2]


def calls(roots):
    return roots.call_log.read_text().splitlines() if roots.call_log.exists() else []


def test_first_claude_on_path_is_the_fake(tmp_roots):
    env = tmp_roots.with_env()
    assert_fake_first(env)
    r = subprocess.run(
        ["bash", "-c", "command -v claude"], capture_output=True, text=True, env=env
    )
    assert r.stdout.strip() == str(FAKES / "claude")
    # the check fails when the fakes folder is not first
    env["PATH"] = env["PATH"].split(":", 1)[1]
    r = subprocess.run(
        ["bash", "-c", "command -v claude"], capture_output=True, text=True, env=env
    )
    assert r.stdout.strip() != str(FAKES / "claude")
    with pytest.raises(AssertionError):
        assert_fake_first(env)


def test_override_guard_refuses_bad_values(tmp_roots):
    with pytest.raises(AssertionError):
        tmp_roots.with_env(SW_KILL_S="9999")
    with pytest.raises(AssertionError):
        tmp_roots.with_env(SW_SB_ROOT="/home/x")


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_each_scenario_prints_json_and_logs_one_line(tmp_roots, scenario):
    r = run_fake(tmp_roots, scenario, FAKE_SLEEP_S="0.2")
    if scenario == "exit127":
        assert r.returncode == 127 and r.stdout == ""
    else:
        parts(r)
    lines = calls(tmp_roots)
    assert len(lines) == 1 and lines[0].split("\t")[1:] == [
        scenario,
        "claude-sonnet-5-5",
    ]
    run_fake(tmp_roots, scenario, FAKE_SLEEP_S="0.2")
    assert len(calls(tmp_roots)) == 2


def test_ok_has_a_valid_ledger_and_findings_block(tmp_roots):
    obs, res = parts(run_fake(tmp_roots, "ok"))
    assert obs == "claude-sonnet-5-5" and not res["is_error"]
    p = fnd.parse_block(res["result"])
    assert p["ok"] and len(p["findings"]) == 1
    rows = (
        re.search(r"```ledger-v1\n(.*?)```", res["result"], re.S).group(1).splitlines()
    )
    assert [json.loads(x)["item"] for x in rows] == ["S3", "S7"]
    assert res["result"].index("## Ledger") < res["result"].index("## Findings block")


def test_ledger_missing_has_findings_but_no_ledger(tmp_roots):
    _, res = parts(run_fake(tmp_roots, "ledger_missing"))
    assert "ledger-v1" not in res["result"] and fnd.parse_block(res["result"])["ok"]


def test_long_anchor_breaks_the_anchor_limit(tmp_roots):
    _, res = parts(run_fake(tmp_roots, "long_anchor"))
    p = fnd.parse_block(res["result"])
    assert not p["ok"] and "anchor" in p["errors"][0]["msg"]


def test_api_error_is_a_synthetic_error_result(tmp_roots):
    obs, res = parts(run_fake(tmp_roots, "api_error"))
    assert (
        obs == "<synthetic>"
        and res["is_error"]
        and res["result"].startswith("API Error")
    )


@pytest.mark.parametrize("asked", ["claude-sonnet-5-5", "claude-haiku-5-5"])
def test_wrong_model_reports_another_model(tmp_roots, asked):
    obs, res = parts(run_fake(tmp_roots, "wrong_model", model=asked))
    assert obs != asked and list(res["modelUsage"]) == [obs]


def test_sleep_waits_then_answers_and_dies_on_term(tmp_roots):
    t = time.monotonic()
    _, res = parts(run_fake(tmp_roots, "sleep", FAKE_SLEEP_S="0.5"))
    assert time.monotonic() - t >= 0.5 and fnd.parse_block(res["result"])["ok"]
    p = subprocess.Popen(
        ["claude", "-p"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        env=tmp_roots.with_env(FAKE_SCENARIO="sleep", FAKE_SLEEP_S="30"),
    )
    p.stdin.write(BRIEF)
    p.stdin.close()
    time.sleep(0.5)
    p.terminate()
    assert p.wait(timeout=5) == 143


def test_bad_block_has_a_line_that_is_not_json(tmp_roots):
    _, res = parts(run_fake(tmp_roots, "bad_block"))
    p = fnd.parse_block(res["result"])
    assert not p["ok"] and "not valid JSON" in p["errors"][0]["msg"]


def test_unknown_scenario_is_refused(tmp_roots):
    r = run_fake(tmp_roots, "nope")
    assert r.returncode == 2 and "unknown FAKE_SCENARIO" in r.stderr
