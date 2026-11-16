"""bin/anon.sh (DESIGN 11.3, REQ-43): random label, reviewer ids R1..Rn, paths redacted. Invented reports only."""

import re
import subprocess
from pathlib import Path

import pytest
from helpers import REPO, SW
from judge_support import RIDS, merged_report

ANON = SW / "bin" / "anon.sh"
RUN_NAME = "ss-p1-r3"  # an arm name inside the run path: the judge must never see it


def run_anon(roots, src, out, **kw):
    return subprocess.run(
        ["bash", str(ANON), str(src), str(out)],
        capture_output=True,
        text=True,
        env=roots.with_env(**kw),
    )


@pytest.fixture
def report(tmp_roots):
    run = tmp_roots.root / "runs" / "stage1" / RUN_NAME
    (run / "merged").mkdir(parents=True)
    src = run / "merged" / "merged-1.md"
    text = merged_report(run, tmp_roots.sb)
    # one claim names the run folder and a study path, as a reviewer quoting a path could
    text += f"\nnote: see {run}/briefs/t3-1.txt and {SW}/cards/C4.json\n"
    src.write_text(text)
    return src, text


def test_ids_replaced_by_r1_to_rn_in_sorted_order(tmp_roots, report):
    src, text = report
    r = run_anon(tmp_roots, src, tmp_roots.root / "out")
    assert r.returncode == 0, r.stderr
    out = (tmp_roots.root / "out" / r.stdout.strip() / "merged-anon.md").read_text()
    # t2b-1, t3-1, t4-1 sort in that order -> R1, R2, R3, in every place they occurred
    assert sorted(RIDS) == list(RIDS)
    for rid in RIDS:
        assert rid not in out
    assert "- R1: report <redacted>, block ok true" in out
    assert "- R3: report <redacted>, block ok true" in out
    assert "| L1 | open | yes | medium | MAJOR | - | R1, R2 |" in out
    assert "#### L1.R1 (F1)" in out
    assert not re.search(r"\bt[0-9]+[a-z]*-[0-9]+\b", out)
    # the text that is not an id or a path is untouched: same number of lines, same ledger
    assert len(out.splitlines()) == len(text.splitlines())
    assert out.count("\n| L") == text.count("\n| L")


def test_a_word_like_test_1_is_not_a_reviewer_id(tmp_roots, report):
    src, text = report
    src.write_text(text + "claim: rerun test-1 and text-2 first.\n")
    r = run_anon(tmp_roots, src, tmp_roots.root / "out")
    out = (tmp_roots.root / "out" / r.stdout.strip() / "merged-anon.md").read_text()
    assert "rerun test-1 and text-2 first." in out


def test_paths_redacted(tmp_roots, report):
    src, _ = report
    r = run_anon(tmp_roots, src, tmp_roots.root / "out")
    out = (tmp_roots.root / "out" / r.stdout.strip() / "merged-anon.md").read_text()
    assert "candidate: <candidate file> sha256" in out
    assert "report <redacted>" in out
    assert "note: see <RUN>/briefs/R2.txt and <SW>/cards/C4.json" in out
    # no arm, run, sandbox or study path is left
    for leak in (RUN_NAME, "/tmp/", str(SW), str(REPO), "cand/p1"):
        assert leak not in out, leak
    # the word "report" in prose is not touched
    assert "The step names a file that the report cannot reach." in out


def test_label_random_and_new_each_time(tmp_roots, report):
    src, _ = report
    out = tmp_roots.root / "out"
    labels = []
    for _ in range(12):
        r = run_anon(tmp_roots, src, out)
        assert r.returncode == 0, r.stderr
        labels.append(r.stdout.strip())
    assert all(re.fullmatch(r"j[0-9a-f]{6}", x) for x in labels)
    assert len(set(labels)) == 12  # a label is never reused
    assert sorted(p.name for p in out.iterdir()) == sorted(labels)
    for x in labels:
        assert [p.name for p in (out / x).iterdir()] == ["merged-anon.md"]


def test_arm_not_in_any_output_name(tmp_roots, report):
    src, _ = report
    r = run_anon(tmp_roots, src, tmp_roots.root / "out")
    folder = tmp_roots.root / "out" / r.stdout.strip()
    assert RUN_NAME not in str(folder) and RUN_NAME not in r.stdout + r.stderr


def test_refuses_output_outside_write_scope(tmp_roots, report):
    src, _ = report
    r = run_anon(tmp_roots, src, "/var/tmp/sw-anon-refused")
    assert r.returncode == 2 and "E_NOT_WRITABLE" in r.stderr
    assert not Path("/var/tmp/sw-anon-refused").exists()


def test_missing_source_refused(tmp_roots):
    r = run_anon(tmp_roots, tmp_roots.root / "nope.md", tmp_roots.root / "out")
    assert r.returncode == 2 and "E_ARG" in r.stderr
