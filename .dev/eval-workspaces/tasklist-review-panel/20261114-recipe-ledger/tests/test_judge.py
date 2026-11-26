"""REQ-43 and REQ-05 (judge): the judge brief is the original one byte for byte, the judge model is named in one file,
the batch audit flags what it must, the second judge sample is round(0.15 n) and repeatable, and the anonymised merged
report carries no run id, reviewer id, path or arm marker. No model starts: the scripts are called without --go, in
--dry or --audit-only mode, with the fake claude first on PATH, and the fake's call log must stay empty."""

import hashlib
import json
import os
import re
import subprocess

import pytest
from helpers import REPO, SW

from analysis import judge_audit as ja
from fixtures.judge import make_judge as mj

EVAL = REPO / ".dev" / "eval-workspaces" / "tasklist-review-panel" / "20261111-a1"
JJ = (
    EVAL / "tools" / "tmp-scripts" / "judge-one.sh"
)  # read only: the one script this test reads from the study folder
JUDGE_MODEL = "claude-opus-5-5"
ONE, BATCH, ANON = (
    SW / "bin" / n for n in ("judge-one.sh", "judge-batch.sh", "anon.sh")
)


def brief_lines(path):
    """The lines from `BRIEF="` to the closing `why."` of a judge script."""
    lines = path.read_text(encoding="utf-8").split("\n")
    start = next(i for i, ln in enumerate(lines) if ln.startswith('BRIEF="'))
    end = next(i for i in range(start, len(lines)) if lines[i].endswith('why."'))
    return lines[start : end + 1]


def sha(lines):
    return hashlib.sha256(("\n".join(lines) + "\n").encode()).hexdigest()


def run(cmd, env):
    return subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=SW)


def calls(roots):
    return roots.call_log.read_text(encoding="utf-8") if roots.call_log.exists() else ""


def test_judge_brief_sha_equals_jj():
    mine = brief_lines(ONE)
    cited = JJ.read_text(encoding="utf-8").split("\n")[11:23]  # lines 12 to 23
    assert len(mine) == len(cited) == 12
    assert sha(mine) == sha(cited)
    assert mine == cited


def test_model_is_opus_only_in_judge():
    hits = [
        str(p.relative_to(SW))
        for sub in ("bin", "rl", "scaffold", "analysis")
        for p in sorted((SW / sub).rglob("*"))
        if p.is_file()
        and "__pycache__" not in p.parts
        and JUDGE_MODEL in p.read_text(encoding="utf-8", errors="replace")
    ]
    assert hits == ["bin/judge-one.sh"]
    assert (
        len(re.findall(rf"--model {JUDGE_MODEL}\b", ONE.read_text(encoding="utf-8")))
        == 1
    )


@pytest.mark.slow
def test_judge_scripts_refuse_without_go_or_nofallback(tmp_roots):
    env = tmp_roots.with_env()
    no_nofb = {k: v for k, v in env.items() if k != "NOFALLBACK"}
    d = str(tmp_roots.root / "scoring")
    for argv, e in (
        ([ONE, "x", "doc-x"], env),  # NOFALLBACK=1 but no --go
        ([ONE, "--go", "x", "doc-x"], no_nofb),  # --go but no NOFALLBACK
        ([BATCH, "--scoring-dir", d, "--runs", "r1"], env),
        ([BATCH, "--go", "--scoring-dir", d, "--runs", "r1"], no_nofb),
    ):
        r = run(["bash", *map(str, argv)], e)
        assert r.returncode == 4, (argv, r.stdout, r.stderr)
        assert "E_" in r.stderr
    assert calls(tmp_roots) == "" and not (tmp_roots.root / "scoring").exists()


def test_audit_flags_error_with_score_file(tmp_path):
    cases = mj.write_scoring(tmp_path / "s")
    assert ja.audit_one(cases["ok"]) == []
    assert (cases["err_score"] / "score.json").is_file()
    assert ja.audit_one(cases["err_score"]) == ["api_error"]
    assert ja.audit_one(cases["err_stderr"]) == ["api_error"]
    assert ja.audit_one(cases["bad_json"]) == ["judge_unparseable"]
    assert ja.audit_one(cases["no_score"]) == ["no_score"]
    assert ja.audit_one(cases["stale"]) == ["stale_score"]
    result = ja.audit(tmp_path / "s")
    assert result["total"] == 8 and result["bad"] == 7
    assert {i["label"] for i in result["items"] if i["ok"]} == {"ok"}


def test_audit_invalidate_renames_flagged_scores(tmp_path):
    cases = mj.write_scoring(tmp_path / "s")
    ja.audit(tmp_path / "s", invalidate=True)
    assert (
        not (cases["err_score"] / "score.json").exists()
        and (cases["err_score"] / "score.json.invalid").is_file()
    )
    assert (cases["ok"] / "score.json").is_file()
    assert ja.audit(tmp_path / "s")["bad"] == 7  # still bad: the judge has to run again


def test_audit_counts_match_merged_rows(tmp_path):
    cases = mj.write_scoring(tmp_path / "s")
    text = (cases["ok"] / "merged-anon.md").read_text(encoding="utf-8")
    assert ja.merged_rows(text) == (mj.ROWS, mj.BLOCKING)
    assert ja.audit_one(cases["rows_total"]) == ["rows_total_mismatch"]
    assert ja.audit_one(cases["rows_blocking"]) == ["rows_blocking_mismatch"]
    # the real merge output counts the same way
    raw = mj.RAW.format(run="r", sha="0" * 64)
    assert ja.merged_rows(raw) == (mj.ROWS, mj.BLOCKING)


@pytest.mark.parametrize("n", [1, 3, 7, 10, 20, 30, 45, 75])
def test_second_judge_sample_15_percent_seeded(n):
    runs = [f"run-{i:03d}" for i in range(n)]
    s1 = ja.sample(runs, 20261115)
    assert (
        len(s1) == round(0.15 * n) and len(set(s1)) == len(s1) and set(s1) <= set(runs)
    )
    assert s1 == ja.sample(
        list(reversed(runs)), 20261115
    )  # same seed, same sample, whatever the order given
    if n >= 20:
        assert s1 != ja.sample(runs, 1)  # another seed picks another sample


def test_sample_script_agrees_with_function():
    runs = [f"run-{i:02d}" for i in range(20)]
    r = subprocess.run(
        [
            "uv",
            "run",
            "--frozen",
            "--project",
            str(REPO),
            "python",
            str(SW / "analysis" / "judge_audit.py"),
            "sample",
            "--seed",
            "7",
            *runs,
        ],
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    assert (
        r.returncode == 0
        and r.stdout.split() == ja.sample(runs, 7)
        and len(r.stdout.split()) == 3
    )


def test_merged_report_has_no_arm_marker(tmp_path):
    runs = mj.write_runs(tmp_path / "runs")
    run_dir = runs["synth-rl-1"]
    raw = (run_dir / "merged" / "merged-1.md").read_text(encoding="utf-8")
    for needle in (
        "probe",
        "src",
        "class",
        "ledger-v1",
        "synth-rl-1",
        "a1-1",
        "/home/someone",
    ):
        assert needle in raw  # the fixture really carries them
    out = tmp_path / "anon" / "merged-anon.md"
    env = {**os.environ, "NOFALLBACK": "1", "PYTHONDONTWRITEBYTECODE": "1"}
    r = run(["bash", str(ANON), str(run_dir), "j1", str(out), "5"], env)
    assert r.returncode == 0, r.stderr
    anon = out.read_text(encoding="utf-8")
    for needle in (
        "probe",
        "src",
        "class",
        "ledger-v1",
        "synth-rl-1",
        "a1-1",
        "b2-1",
        "c3-1",
        "/home",
        "/tmp",
        " RL",
    ):
        assert needle not in anon, needle
    assert sorted(set(re.findall(r"\bR\d\b", anon))) == ["R1", "R2", "R3"]
    assert ja.merged_rows(anon) == (mj.ROWS, mj.BLOCKING)  # the table survives
    assert (
        "The table row says 5 where the text says 4." in anon
    )  # and so does the finding text
    assert ja.leaks(anon, "synth-rl-1", mj.IDS) == []


def test_anon_numbering_depends_on_label_and_seed(tmp_path):
    run_dir = mj.write_runs(tmp_path / "runs")["synth-rl-1"]
    raw = (run_dir / "merged" / "merged-1.md").read_text(encoding="utf-8")
    maps = {
        tuple(sorted(ja.anonymise(raw, "synth-rl-1", mj.IDS, 3, f"j{n}")[1].items()))
        for n in range(8)
    }
    assert len(maps) > 1  # not always the same order
    again = ja.anonymise(raw, "synth-rl-1", mj.IDS, 3, "j1")
    assert again == ja.anonymise(raw, "synth-rl-1", mj.IDS, 3, "j1")


def test_anon_refuses_a_run_without_merged_report(tmp_path):
    run_dir = mj.write_runs(tmp_path / "runs")["synth-k-1"]
    (run_dir / "merged" / "merged-1.md").unlink()
    env = {**os.environ, "NOFALLBACK": "1", "PYTHONDONTWRITEBYTECODE": "1"}
    r = run(["bash", str(ANON), str(run_dir), "j1", str(tmp_path / "o.md")], env)
    assert r.returncode == 3 and not (tmp_path / "o.md").exists()


@pytest.mark.slow
def test_batch_dry_and_audit_only_start_no_judge(tmp_roots):
    runs = tmp_roots.root / "runs"
    names = [(f"synth-{i}", "doc-x") for i in range(7)]
    mj.write_runs(runs, names)
    scoring = tmp_roots.root / "scoring"
    env = tmp_roots.with_env()
    base = [
        "bash",
        str(BATCH),
        "--dry",
        "--seed",
        "11",
        "--runs-dir",
        str(runs),
        "--scoring-dir",
        str(scoring),
    ]
    r = run([*base, "--runs", *[n for n, _ in names]], env)
    assert r.returncode == 0, r.stderr
    rows = [
        ln.split("\t")
        for ln in (scoring / "labels.tsv").read_text(encoding="utf-8").splitlines()
    ]
    assert len(rows) == 7 + round(0.15 * 7) == 8
    assert sorted(x[3] for x in rows).count("second") == 1
    assert len({x[0] for x in rows}) == 8  # the labels are distinct
    assert all((scoring / x[0] / "merged-anon.md").is_file() for x in rows)
    assert "no judge started" in r.stdout
    once = (scoring / "labels.tsv").read_text(encoding="utf-8")
    assert run([*base, "--runs", *[n for n, _ in names]], env).returncode == 0
    assert (scoring / "labels.tsv").read_text(encoding="utf-8") == once  # repeatable
    # a stage selects runs by prefix
    assert run([*base, "synth"], env).returncode == 0
    # audit-only: no judge output yet, so every folder is bad
    r = run(["bash", str(BATCH), "--audit-only", "--scoring-dir", str(scoring)], env)
    assert r.returncode == 1 and "bad = 8" in r.stdout
    audit = json.loads((scoring / "judge_audit.json").read_text(encoding="utf-8"))
    assert audit["bad"] == audit["total"] == 8
    assert all(
        "no_judge_json" in i["flags"] and "no_score" in i["flags"]
        for i in audit["items"]
    )
    assert calls(tmp_roots) == ""


@pytest.mark.slow
def test_batch_audit_only_on_synthetic_judge_folders(tmp_roots):
    mj.write_scoring(tmp_roots.root / "scoring")
    r = run(
        [
            "bash",
            str(BATCH),
            "--audit-only",
            "--scoring-dir",
            str(tmp_roots.root / "scoring"),
        ],
        tmp_roots.with_env(),
    )
    assert r.returncode == 1
    assert "BAD err_score: api_error" in r.stdout and "bad = 7" in r.stdout
    assert "BAD ok" not in r.stdout
