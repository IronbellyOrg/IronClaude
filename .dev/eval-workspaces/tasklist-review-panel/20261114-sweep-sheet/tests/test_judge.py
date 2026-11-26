"""REQ-43, DESIGN 11.3: the judge copy, the batch, the audit and the second-judge sample.
Every judge call goes to tests/fakes/claude; every ground-truth and score file is invented in tmp_path."""

import hashlib
import json
import subprocess
import sys

from helpers import REPO, SW
from judge_support import (
    ROWS,
    brief_of,
    jj_brief,
    make_inputs,
    make_judge_dir,
    make_run,
    score_for,
)

from scaffold import judge

BATCH = SW / "bin" / "judge-batch.sh"
ONE = SW / "bin" / "judge-one.sh"
OPUS = "claude-opus-5-5"
EVAL = REPO / ".dev/eval-workspaces/tasklist-review-panel/20261111-a1"


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# --- the brief and the model ---------------------------------------------------------------------------------------


def test_judge_brief_sha():
    mine, jj = brief_of(ONE), jj_brief()
    assert mine.startswith('BRIEF="You are a blind scoring judge') and len(
        mine.splitlines()
    ) == len(jj.splitlines())
    assert sha(mine) == sha(jj)
    # the only difference between the two scripts is where the paths come from, not what the judge is told
    assert 'unreadable write score.json with zeros and say why."' in mine


def test_model_is_opus_only_in_judge():
    hits = {}
    for sub in ("bin", "sweep", "scaffold"):
        for p in (SW / sub).rglob("*"):
            if p.is_file() and "__pycache__" not in p.parts:
                n = p.read_text(encoding="utf-8", errors="replace").count(OPUS)
                if n:
                    hits[str(p.relative_to(SW))] = n
    assert hits == {"bin/judge-one.sh": 1}, hits


def test_judge_one_calls_opus_through_the_fake(tmp_roots):
    cand, gt = make_inputs(tmp_roots.root)
    d = tmp_roots.root / "scoring" / "j0abc12"
    d.mkdir(parents=True)
    (d / "merged-anon.md").write_text("# a merged report\n")
    r = subprocess_run(
        tmp_roots,
        [ONE, d, gt / "p1.json", cand / "p1" / "candidate.md", "p1"],
        FAKE_JUDGE_SCORE="1",
    )
    assert r.returncode == 0 and r.stdout.startswith("OK blind/p1/j0abc12"), r.stderr
    calls = tmp_roots.call_log.read_text().splitlines()
    assert [c.split("\t")[2] for c in calls] == [OPUS]
    assert (d / "judge.started").is_file() and (d / "judge.json").is_file()
    # a finished folder is skipped, not judged again
    r = subprocess_run(
        tmp_roots, [ONE, d, gt / "p1.json", cand / "p1" / "candidate.md"]
    )
    assert (
        r.stdout.startswith("SKIP")
        and len(tmp_roots.call_log.read_text().splitlines()) == 1
    )


def test_judge_one_refuses_a_folder_in_the_study(tmp_roots):
    cand, gt = make_inputs(tmp_roots.root)
    d = EVAL / "arms" / "scoring" / "zz-refused"
    r = subprocess_run(
        tmp_roots, [ONE, d, gt / "p1.json", cand / "p1" / "candidate.md"]
    )
    assert r.returncode == 2 and "E_NOT_WRITABLE" in r.stderr
    assert not d.exists() and not tmp_roots.call_log.exists()


def subprocess_run(roots, argv, **env):
    return subprocess.run(
        ["bash", *map(str, argv)],
        capture_output=True,
        text=True,
        env=roots.with_env(**env),
    )


# --- the audit ----------------------------------------------------------------------------------------------------


def test_audit_flags_error_with_score_file(tmp_path):
    # a score file exists beside an API error: it is still a problem (DESIGN 10 row 20)
    d = make_judge_dir(tmp_path, "j1", judge="api_error", score=score_for())
    assert "api_error" in judge.audit_one(d)
    # the same error told only by stderr
    d = make_judge_dir(
        tmp_path, "j2", score=score_for(), err="API Error: 529 overloaded_error\n"
    )
    assert "api_error" in judge.audit_one(d)
    # controls: a clean folder passes, and a stale or missing score is flagged on its own
    assert judge.audit_one(make_judge_dir(tmp_path, "j3", score=score_for())) == []
    assert judge.audit_one(make_judge_dir(tmp_path, "j4")) == ["no_score"]
    stale = make_judge_dir(tmp_path, "j5", score=score_for(), started_age=60)
    assert "score_stale" in judge.audit_one(stale)
    fresh = make_judge_dir(tmp_path, "j5b", score=score_for(), started_age=-60)
    assert judge.audit_one(fresh) == []
    assert judge.audit_one(make_judge_dir(tmp_path, "j6", judge="not json")) == [
        "judge_unparseable",
        "no_score",
    ]
    out = judge.audit([tmp_path / n for n in ("j1", "j2", "j3")])
    assert (out["checked"], out["bad"]) == (3, 2)


def test_audit_counts_match_merged_rows(tmp_path):
    assert judge.ledger_counts("no table in this text\n") == (0, 0)
    d = make_judge_dir(tmp_path, "ok", score=score_for())
    assert judge.ledger_counts((d / "merged-anon.md").read_text()) == (4, 1)
    assert judge.audit_one(d) == []
    for name, kw in (
        ("bad_total", {"ledger_rows_total": 5}),
        ("bad_blocking", {"ledger_rows_blocking": 2}),
    ):
        bad = make_judge_dir(tmp_path, name, score=score_for(**kw))
        assert judge.audit_one(bad) == ["rows_mismatch"], kw
    # a report with another number of rows is judged against its own rows
    rows = ROWS + (("L5", "open", "yes"),)
    d5 = make_judge_dir(tmp_path, "five", rows=rows, score=score_for(rows=rows))
    assert judge.ledger_counts((d5 / "merged-anon.md").read_text()) == (5, 2)
    assert judge.audit_one(d5) == []


# --- the second-judge sample --------------------------------------------------------------------------------------


def test_second_judge_sample_15_percent_seeded():
    ids = [f"r{i:02d}" for i in range(60)]
    s = judge.sample(ids, 7)
    assert len(s) == round(0.15 * 60) == 9 and set(s) <= set(ids)
    assert (
        s == judge.sample(ids, 7) == judge.sample(ids[::-1], 7)
    )  # repeatable, order free
    assert (
        len({tuple(judge.sample(ids, k)) for k in range(1, 11)}) > 1
    )  # the seed matters
    for n, want in ((7, 1), (20, 3), (40, 6), (75, 11), (3, 0)):
        assert len(judge.sample([f"x{i}" for i in range(n)], 1)) == want, n
    # the script form that bin/judge-batch.sh calls gives the same ids
    r = subprocess.run(
        [sys.executable, "-I", str(SW / "scaffold" / "judge.py"), "sample", "7", *ids],
        capture_output=True,
        text=True,
    )
    assert r.stdout.split() == s


# --- the batch, against the fake ----------------------------------------------------------------------------------


def batch_world(roots, n=7):
    runs = roots.root / "runs" / "stage1"
    names = [f"ss-p1-r{i}" for i in range(1, n + 1)]
    for name in names:
        make_run(runs, name, roots.sb)
    cand, gt = make_inputs(roots.root)
    scoring = roots.root / "scoring" / "stage1"
    argv = [BATCH, "stage1", "--runs", runs, "--scoring", scoring, "--gt-dir", gt]
    argv += ["--cand-root", cand, "--seed", "7", "--jobs", "2"]
    return runs, names, scoring, argv


def test_batch_judges_every_run_and_a_seeded_sample_again(tmp_roots):
    runs, names, scoring, argv = batch_world(tmp_roots)
    r = subprocess_run(tmp_roots, argv, FAKE_JUDGE_SCORE="1")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "BATCH stage=stage1 runs=7 second=1 bad=0" in r.stdout
    calls = [c.split("\t")[2] for c in tmp_roots.call_log.read_text().splitlines()]
    assert calls == [OPUS] * 8  # 7 judges plus round(0.15 * 7) = 1 second judge
    summary = json.loads((scoring / "judge-batch.json").read_text())
    assert summary["runs_judged"] == 7 and summary["audit_bad"] == 0
    assert summary["second_sample"] == judge.sample(names, 7)
    labels = sorted(p.name for p in scoring.iterdir() if p.is_dir())
    assert len(labels) == 8 and all(len(x) == 7 and x[0] == "j" for x in labels)
    for lab in labels:
        assert (scoring / lab / "score.json").is_file()
        text = (scoring / lab / "merged-anon.md").read_text()
        assert not any(n in text or n in str(scoring / lab) for n in names)
    # the key sits in the run folder, never in the scoring folder
    key = json.loads((runs / names[0] / "scoring" / "label-key.json").read_text())
    assert key["run"] == names[0] and key["label"] in labels
    assert not list(scoring.rglob("label-key.json"))


def test_batch_invalidates_a_score_beside_an_api_error_and_reruns(tmp_roots):
    runs, names, scoring, argv = batch_world(tmp_roots, n=3)
    r = subprocess_run(tmp_roots, argv, FAKE_JUDGE_SCORE="1", FAKE_SCENARIO="api_error")
    assert r.returncode == 1 and "BATCH_BAD" in r.stderr, r.stdout + r.stderr
    dirs = [p for p in scoring.iterdir() if p.is_dir()]
    assert dirs and all(not (d / "score.json").exists() for d in dirs)
    assert all(list(d.glob("score.json.invalid-api_error")) for d in dirs)
    audit = json.loads((scoring / "judge-audit.json").read_text())
    assert audit["bad"] == len(dirs)
    # run it again with a working judge: the invalidated runs are judged again, the labels are kept
    r = subprocess_run(tmp_roots, argv, FAKE_JUDGE_SCORE="1")
    assert r.returncode == 0, r.stdout + r.stderr
    assert sorted(p.name for p in scoring.iterdir() if p.is_dir()) == sorted(
        d.name for d in dirs
    )
    assert all((d / "score.json").is_file() for d in dirs)


def test_batch_refuses_what_it_cannot_judge(tmp_roots):
    runs, names, scoring, argv = batch_world(tmp_roots, n=2)
    i = argv.index("--gt-dir")
    no_gt_option = argv[:i] + argv[i + 2 :]
    missing_gt_folder = argv[: i + 1] + [tmp_roots.root / "nope"] + argv[i + 2 :]
    for bad in (no_gt_option, missing_gt_folder):
        r = subprocess_run(tmp_roots, bad)
        assert r.returncode == 2 and "E_ARG" in r.stderr, r.stderr
    assert not tmp_roots.call_log.exists()  # nothing was judged
