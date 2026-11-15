"""The check scripts of bin/ (TESTING section 4): check-sandbox-gt.sh (REQ-34), check-z0-parity.sh (DR-12) and
open-manual-checks.sh (the M records). Sandboxes and run folders are invented and live under the pytest temporary folder."""

import os
import shutil
import subprocess

from helpers import SW
from order_support import make_root, run

from fixtures.runs import make_ran_runs as mk

SANDBOX_GT = SW / "bin" / "check-sandbox-gt.sh"
PARITY = SW / "bin" / "check-z0-parity.sh"
OPEN = SW / "bin" / "open-manual-checks.sh"
REQS = "REQ-08 REQ-28 REQ-31 REQ-32 REQ-33 REQ-36 REQ-40 REQ-41 REQ-44 REQ-45 REQ-38 REQ-35".split()


def env_for(tmp_path):
    e = {k: v for k, v in os.environ.items() if not k.startswith(("SW_", "RL_"))}
    e.update(
        SW_SB_ROOT=str(tmp_path / "sb"),
        RL_RUNS_ROOT=str(tmp_path / "runs"),
        NOFALLBACK="1",
        PYTHONDONTWRITEBYTECODE="1",
    )
    return e


def sh(script, tmp_path, *args):
    return subprocess.run(
        ["bash", str(script), *map(str, args)],
        capture_output=True,
        text=True,
        env=env_for(tmp_path),
    )


def put(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def clean_tree(tmp_path):
    put(tmp_path / "sb" / "DOC1" / "repo" / "src" / "app.py", "print('hello')\n")
    put(tmp_path / "sb" / "cand" / "DOC1" / "candidate.md", "# plan\n")
    put(tmp_path / "runs" / "run1" / "briefs" / "t2b-1.txt", "review the plan\n")
    # a .git folder is not searched
    put(
        tmp_path / "sb" / "DOC1" / "repo" / ".git" / "info" / "x", "ground-truth.json\n"
    )


def test_sandbox_gt_check_finds_a_planted_trap_and_is_silent_when_clean(tmp_path):
    clean_tree(tmp_path)
    r = sh(SANDBOX_GT, tmp_path)
    assert r.returncode == 0 and r.stdout == "" and r.stderr == ""

    # a ground-truth file name, a field name in a brief, and a ground-truth file name inside another file
    secret = "SECRETPHRASE-do-not-print"
    trap = put(
        tmp_path / "sb" / "DOC1" / "repo" / "docs" / "ground-truth.json",
        f'{{"description": "{secret}"}}\n',
    )
    field = put(
        tmp_path / "runs" / "run1" / "briefs" / "t4-1.txt",
        f"check plan_quote {secret}\n",
    )
    named = put(
        tmp_path / "sb" / "cand" / "DOC1" / "notes.md",
        f"see ground-truth-ho1.json {secret}\n",
    )
    r = sh(SANDBOX_GT, tmp_path)
    assert r.returncode == 1
    assert sorted(r.stdout.split("\n")[:-1]) == sorted(map(str, (trap, field, named)))
    assert secret not in r.stdout + r.stderr  # a path per hit, never a matching line

    # explicit folders: only those are searched; a missing one is a usage error
    r = sh(SANDBOX_GT, tmp_path, tmp_path / "runs" / "run1" / "briefs")
    assert r.returncode == 1 and r.stdout.strip() == str(field)
    assert sh(SANDBOX_GT, tmp_path, tmp_path / "nowhere").returncode == 2

    # the Z0-raw sandbox is searched by file name only (its documents may talk about ground truth)
    raw_doc = put(
        tmp_path / "sb" / "DOC1" / "repo-raw" / "notes.md",
        "the ground-truth.json holds plan_quote\n",
    )
    assert str(raw_doc) not in sh(SANDBOX_GT, tmp_path).stdout
    raw_trap = put(tmp_path / "sb" / "DOC1" / "repo-raw" / "ground-truth.json", "{}\n")
    assert str(raw_trap) in sh(SANDBOX_GT, tmp_path).stdout

    # the trap removed: silent again
    for p in (trap, field, named, raw_doc, raw_trap):
        p.unlink()
    r = sh(SANDBOX_GT, tmp_path)
    assert r.returncode == 0 and r.stdout == ""


def test_sandbox_gt_check_searches_spike_run_briefs(tmp_path):
    # bin/run-spike.sh writes runs/spike-timing/<run>/ and runs/spike-compliance/<run>/, one level deeper than runs/<id>/
    clean_tree(tmp_path)
    for spike, run_id in (
        ("spike-timing", "timing-rl-1"),
        ("spike-compliance", "compliance-1"),
    ):
        brief = tmp_path / "runs" / spike / run_id / "briefs" / "t2b-1.txt"
        put(brief, "review the plan\n")
        assert sh(SANDBOX_GT, tmp_path).stdout == ""
        brief.write_text("check plan_quote here\n", encoding="utf-8")
        r = sh(SANDBOX_GT, tmp_path)
        assert r.returncode == 1 and r.stdout.strip() == str(brief)
        brief.unlink()
    assert sh(SANDBOX_GT, tmp_path).returncode == 0


def test_sandbox_gt_check_is_silent_with_no_sandbox_at_all(tmp_path):
    r = sh(SANDBOX_GT, tmp_path)
    assert r.returncode == 0 and r.stdout == ""


def test_z0_parity_prints_a_stable_hash(tmp_path):
    cand = SW / "fixtures" / "plans" / "p_basic.md"
    put(
        tmp_path / "sb" / "cand" / "DOC1" / "candidate.md",
        cand.read_text(encoding="utf-8"),
    )
    first = sh(PARITY, tmp_path, "DOC1")
    second = sh(PARITY, tmp_path, "DOC1")
    assert first.returncode == 0, first.stderr
    h = first.stdout.strip()
    assert len(h) == 64 and set(h) <= set("0123456789abcdef")
    assert second.stdout.strip() == h
    # a different candidate gives a different hash; a source changes the brief too
    put(tmp_path / "sb" / "cand" / "DOC2" / "candidate.md", "# another plan\n")
    other = sh(PARITY, tmp_path, "DOC2")
    assert other.returncode == 0 and other.stdout.strip() != h
    shutil.copy(
        SW / "fixtures" / "plans" / "source.md",
        tmp_path / "sb" / "cand" / "DOC1" / "source.md",
    )
    assert sh(PARITY, tmp_path, "DOC1").stdout.strip() != h
    # no sandbox: refused
    r = sh(PARITY, tmp_path, "NOPE")
    assert r.returncode == 2 and "E_SANDBOX" in r.stderr


def test_open_manual_checks_lists_open_records(tmp_path):
    root = make_root(tmp_path / "root")
    r = run(OPEN, root)
    assert r.returncode == 0, r.stderr
    lines = r.stdout.splitlines()
    for req in REQS:
        assert any(ln.startswith("OPEN") and f" {req} " in ln for ln in lines), req
    assert lines[-1] == "open: 12 of 12"

    # records closed by a person's files and lines drop out of the open list
    reviews = "\n".join(
        f"| C{n} | DONE | A. Reader | 2026-11-20 |" for n in range(1, 9)
    )
    put(root / "recipes" / "REVIEWS.md", reviews + "\n")
    put(root / "results" / "ran-audit.md", "19 of 20 agree\n")
    put(root / "results" / "attestations.md", "REQ-33: exit 0\nREQ-44: exit 0\n")
    put(root / "config" / "prereg.json", "{}\n")
    put(root / "config" / "values.json", '{"spike": {"runs": 5, "c_luna": 2.2}}\n')
    put(
        root / "recipes" / "README.md",
        "B. Reader, 2026-11-21: each row is specific, not a restatement of the heading\n",
    )
    r = run(OPEN, root)
    done = {ln.split()[1] for ln in r.stdout.splitlines() if ln.startswith("done")}
    assert done == {
        "REQ-08",
        "REQ-28",
        "REQ-33",
        "REQ-44",
        "REQ-41",
        "REQ-32",
        "REQ-38",
    }
    assert r.stdout.splitlines()[-1] == "open: 5 of 12"
    # a half-filled review row, a spike of 3 runs and the ablation (never closed by a file) stay open
    put(
        root / "recipes" / "REVIEWS.md",
        reviews.replace("| A. Reader |", "| |", 1) + "\n",
    )
    put(root / "config" / "values.json", '{"spike": {"runs": 3, "c_luna": 2.2}}\n')
    out = run(OPEN, root).stdout
    assert "OPEN REQ-08" in out and "OPEN REQ-32" in out and "OPEN REQ-35" in out


def test_the_real_records_are_listed():
    r = subprocess.run(["bash", str(OPEN)], capture_output=True, text=True)
    assert r.returncode == 0
    for req in REQS:
        assert f" {req} " in r.stdout, req


def test_ran_audit_prints_rows_with_their_transcripts(tmp_path):
    runs = mk.build(tmp_path / "runs")
    r = sh(OPEN, tmp_path, "ran-audit", tmp_path / "runs")
    assert r.returncode == 0, r.stderr
    n = r.stdout.count("=== row ")
    assert 0 < n <= 20
    assert r.stdout.count("ran_status:") == n and r.stdout.count("transcript: ") == n
    assert "Bash:" in r.stdout and "attempt1.json" in r.stdout
    again = sh(OPEN, tmp_path, "ran-audit", tmp_path / "runs")
    assert again.stdout == r.stdout  # seeded sample, same rows
    small = sh(OPEN, tmp_path, "ran-audit", runs[0], "--rows", 2)
    assert small.stdout.count("=== row ") <= 2
    assert sh(OPEN, tmp_path, "ran-audit", tmp_path / "nowhere").returncode == 2
