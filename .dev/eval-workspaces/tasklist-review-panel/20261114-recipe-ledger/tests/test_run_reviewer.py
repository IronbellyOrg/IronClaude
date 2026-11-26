"""bin/run-reviewer.sh against the fake claude (DESIGN 9.2, 8 row 6, REQ-30): one attempt, the refusals, the hang guard,
the meta.json keys and their agreement with rl.rowcheck._dropped. No model starts."""

import hashlib
import json
import os
import subprocess
import time

import pytest
import rl_support as s
from conftest import FAKES
from helpers import SW

from rl import render, rowcheck
from scaffold import fnd

pytestmark = pytest.mark.slow

SCRIPT = SW / "bin" / "run-reviewer.sh"
EMBER, SONNET = "muse-ember-1.0", "claude-sonnet-5-5"
DOC, RID = "doc1", "S"
KEYS = {
    "reviewer_id",
    "expected_model",
    "observed_model",
    "model_ok",
    "findings_block",
    "block_ok",
    "attempt",
    "wall_s",
    "output_tokens_main",
    "output_tokens_all",
    "exit",
    "hang_s",
    "status",
    "killed",
    "invalid",
    "error",
    "prompt_sha256",
}


@pytest.fixture
def box(tmp_roots):
    """A sandbox repo under SW_SB_ROOT, a candidate, an ember brief file and a run folder."""
    root = tmp_roots.root
    (tmp_roots.sb / DOC / "repo").mkdir(parents=True)
    cand = root / "candidate.md"
    cand.write_text(
        (SW / "fixtures" / "plans" / "p_basic.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    text = render.brief(
        s.roles("primary")["S"], {"cand_sb": str(cand), "sha": s.SHA}, s.SOURCE
    )["text"]
    brief = root / "brief.txt"
    brief.write_text(text, encoding="utf-8")
    tmp = root / "tmp"
    tmp.mkdir()
    tmp_roots.env["TMPDIR"] = str(tmp)
    tmp_roots.brief, tmp_roots.run, tmp_roots.tmp = brief, root / "run", tmp
    return tmp_roots


def run(box, scenario="ok", model=EMBER, hang="60", used="0", env=None, drop=()):
    env = env or {}
    if (
        "PATH" in env
    ):  # the spy test puts a wrapper of the fake first; with_env would refuse that
        e = dict(box.env, FAKE_SCENARIO=scenario, **env)
    else:
        e = box.with_env(FAKE_SCENARIO=scenario, **env)
    for k in drop:
        e.pop(k, None)
    args = [str(SCRIPT), str(box.run), DOC, RID, model, str(box.brief), hang]
    return subprocess.run(
        ["bash", *args, *([used] if used != "0" else [])],
        capture_output=True,
        text=True,
        env=e,
        timeout=60,
    )


def meta(box):
    return json.loads((box.run / "reviews" / f"{RID}.meta.json").read_text())


def calls(box):
    return box.call_log.read_text().splitlines() if box.call_log.exists() else []


def test_ok_run_writes_the_files_and_the_keys(box):
    r = run(box)
    assert r.returncode == 0, r.stderr
    m = meta(box)
    assert set(m) == KEYS
    assert (m["status"], m["killed"], m["invalid"], m["error"]) == (
        "ok",
        False,
        False,
        False,
    )
    assert (m["model_ok"], m["block_ok"], m["findings_block"]) == (True, True, True)
    assert m["prompt_sha256"] == hashlib.sha256(box.brief.read_bytes()).hexdigest()
    assert (m["hang_s"], m["attempt"], m["exit"], m["expected_model"]) == (
        60,
        1,
        0,
        EMBER,
    )
    assert m["observed_model"] == EMBER and m["wall_s"] >= 0
    rev = box.run / "reviews"
    for name in (
        "attempt1.json",
        "attempt1.err",
        "attempt1.md",
        "attempt1.meta.json",
        "md",
        "meta.json",
        "cost.json",
    ):
        assert (rev / f"{RID}.{name}").is_file(), name
    assert json.loads((rev / f"{RID}.cost.json").read_text())["attempts"] == 1
    assert (rev / f"{RID}.md").read_text().startswith("review: 1 of 3")
    assert len(calls(box)) == 1
    assert (
        list(box.tmp.glob("rl-block.*")) == []
    )  # the temporary H2 copy is gone (uv leaves its own lock file)


def test_one_attempt_cwd_and_read_only_flags(box, tmp_path):
    spy = tmp_path / "spy"
    spy.mkdir()
    out = tmp_path / "spy.out"
    (spy / "claude").write_text(
        f'#!/usr/bin/env bash\n{{ pwd; echo "$@"; }} >>{out}\nexec {FAKES}/claude "$@"\n'
    )
    (spy / "claude").chmod(0o755)
    r = run(box, env={"PATH": f"{spy}{os.pathsep}{box.env['PATH']}"})
    assert r.returncode == 0, r.stderr
    cwd, argv = out.read_text().splitlines()
    assert cwd == str(box.sb / DOC / "repo")
    assert f"-p --model {EMBER} --output-format json --no-session-persistence" in argv
    assert (
        "--permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit"
        in argv
    )


def test_missing_ledger_block_is_not_a_block_error(box):
    run(box, "ledger_missing")
    m = meta(box)
    assert (m["block_ok"], m["status"], m["invalid"]) == (True, "ok", False)


def test_block_ok_is_decided_after_h2_and_the_report_stays_raw(box):
    run(box, "long_anchor")
    m = meta(box)
    assert (m["block_ok"], m["status"]) == (True, "ok")
    raw = json.loads((box.run / "reviews" / f"{RID}.attempt1.json").read_text())[-1][
        "result"
    ]
    assert (
        box.run / "reviews" / f"{RID}.md"
    ).read_text() == raw + "\n"  # jq -r ends the text with a newline, as in RR
    assert fnd.parse_block(raw)["ok"] is False  # it only parses after H2


@pytest.mark.parametrize(
    ("scenario", "status", "model_ok"),
    [
        ("bad_block", "invalid", True),
        ("wrong_model", "invalid", False),
        ("api_error", "error", False),
        ("exit127", "error", False),
    ],
)
def test_failures_are_recorded_and_agree_with_rowcheck(box, scenario, status, model_ok):
    r = run(box, scenario)
    assert r.returncode == 0, r.stderr
    m = meta(box)
    assert (m["status"], m["model_ok"]) == (status, model_ok)
    assert (m["invalid"], m["error"], m["killed"]) == (
        status == "invalid",
        status == "error",
        False,
    )
    assert rowcheck._dropped(box.run / "reviews", RID) is True
    assert len(calls(box)) == 1  # one attempt, no retry


def test_ok_is_not_dropped_by_rowcheck(box):
    run(box)
    assert rowcheck._dropped(box.run / "reviews", RID) is False


def test_sleeping_reviewer_is_killed_by_the_guard(box):
    t = time.monotonic()
    r = run(box, "sleep", hang="1.5", env={"FAKE_SLEEP_S": "30"})
    assert r.returncode == 0, r.stderr
    assert time.monotonic() - t < 15
    m = meta(box)
    assert (m["status"], m["killed"], m["invalid"], m["error"]) == (
        "killed",
        True,
        False,
        False,
    )
    assert m["hang_s"] == 1.5 and m["exit"] in (124, 137)
    assert rowcheck._dropped(box.run / "reviews", RID) is True
    assert len(calls(box)) == 1


def test_time_already_used_shortens_the_guard(box):
    t = time.monotonic()
    run(box, "sleep", hang="100", used="99", env={"FAKE_SLEEP_S": "30"})
    assert time.monotonic() - t < 15
    m = meta(box)
    assert (m["status"], m["hang_s"]) == ("killed", 100)


def test_refused_without_nofallback(box):
    r = run(box, drop=("NOFALLBACK",))
    assert r.returncode == 4 and "NOFALLBACK" in r.stderr
    assert calls(box) == [] and not box.run.exists()


def test_refused_for_a_model_outside_the_allowlist(box):
    r = run(box, model="gpt-6.1-sol")
    assert r.returncode == 4 and "E_MODEL" in r.stderr
    assert calls(box) == [] and not box.run.exists()


def test_refused_on_the_sibling_sandbox_root(box):
    r = run(box, env={"SW_SB_ROOT": "/tmp/evalsb-sweep"})
    assert r.returncode == 4 and calls(box) == []


def test_usage_errors_exit_2(box):
    assert (
        subprocess.run(
            ["bash", str(SCRIPT)], capture_output=True, env=box.env
        ).returncode
        == 2
    )
    assert run(box, hang="soon").returncode == 2
    (box.brief).unlink()
    assert run(box).returncode == 2


def test_script_text_keeps_k2_and_k4():
    text = SCRIPT.read_text()
    assert "claude-opus-5-5" not in text
    assert "--disallowedTools Edit Write NotebookEdit" in text
    assert "NOFALLBACK" in text and "sw_assert_model" in text
    assert SCRIPT.read_text().index("rl-env.sh") < SCRIPT.read_text().index("common.sh")
