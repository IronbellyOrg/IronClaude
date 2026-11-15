"""AO-1 leak lint (REQ-07). Every ground-truth and text file below is invented and built in tmp_path by the test."""

import builtins
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
from helpers import SW

from scaffold import lint

LINT_PY = SW / "scaffold" / "lint.py"
LEAK = "rotate before each tangerine"  # a four-word run of the invented description
HASH = re.compile(r"hash=([0-9a-f]{12})\b")


def make_gt(tmp_path, name="synthetic-gt.json"):
    gt = {
        "doc_id": "zebra-ledger-9",
        "title": "Harvest Ledger Overhaul",
        "items": [
            {
                "id": "G1",
                "class": "C1",
                "blocking_in_implement": True,
                "description": f"Marmalade kettles must {LEAK} audit pass",
                "plan_quote": "Run `orchard/billing/ledger_sync.py` after every harvest closes",
            }
        ],
    }
    p = tmp_path / name
    p.write_text(json.dumps(gt), encoding="utf-8")
    return p


def run(gt, *files, extra=()):
    return lint.main(["--gt-glob", str(gt), *map(str, files), *extra])


def test_seeded_leak_fails(tmp_path, capsys):
    gt = make_gt(tmp_path)
    target = tmp_path / "target.md"
    target.write_text(
        "intro line\nnothing here\nplease Rotate Before\neach tangerine today\n",
        encoding="utf-8",
    )
    assert run(gt, target) == 1
    out = capsys.readouterr().out
    assert str(target) in out
    assert f"{target}:3:" in out  # the phrase starts on line 3 and wraps to line 4
    assert HASH.search(out).group(1) == lint.phrase_hash(LEAK)
    for word in ("rotate", "tangerine", "kettles", "Rotate"):
        assert word not in out


def test_seeded_leak_fails_as_a_process(tmp_path):
    gt = make_gt(tmp_path)
    target = tmp_path / "target.md"
    target.write_text(f"x\n{LEAK}\n", encoding="utf-8")
    r = subprocess.run(
        [sys.executable, "-I", str(LINT_PY), "--gt-glob", str(gt), str(target)],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 1
    assert f"{target}:2:" in r.stdout and HASH.search(r.stdout)
    assert "tangerine" not in r.stdout + r.stderr


def test_clean_passes(tmp_path, capsys):
    gt = make_gt(tmp_path)
    target = tmp_path / "target.md"
    # three-word overlaps and a reordered run are not four-word sequences of the description
    target.write_text(
        "rotate before each audit\ntangerine each before rotate\n",
        encoding="utf-8",
    )
    assert run(gt, target) == 0
    assert "0 hit(s)" in capsys.readouterr().out


def test_forbidden_name_fails(tmp_path, capsys):
    gt = make_gt(tmp_path)
    by_id = tmp_path / "id.md"
    by_id.write_text("one\nsee Zebra-Ledger-9 for details\n", encoding="utf-8")
    by_title = tmp_path / "title.md"
    by_title.write_text("the harvest ledger overhaul plan\n", encoding="utf-8")
    by_path = tmp_path / "path.md"
    by_path.write_text(
        "a\nb\nc\nopen orchard/billing/ledger_sync.py now\n", encoding="utf-8"
    )
    by_flag = tmp_path / "flag.md"
    by_flag.write_text("the mango protocol\n", encoding="utf-8")
    near = tmp_path / "near.md"
    near.write_text(
        "zebra-ledger-90 and ledger_sync.pyc stay unflagged\n", encoding="utf-8"
    )
    assert run(gt, near) == 0
    capsys.readouterr()
    for f, line in ((by_id, 2), (by_title, 1), (by_path, 4), (by_flag, 1)):
        assert run(gt, f, extra=["--forbid", "Mango Protocol"]) == 1
        out = capsys.readouterr().out
        assert f"{f}:{line}: leak name" in out
        assert HASH.search(out)
        for secret in ("zebra", "harvest", "orchard", "ledger_sync", "mango"):
            assert secret not in out


def test_walks_folders_and_skips_the_ground_truth_itself(tmp_path, capsys):
    gt = make_gt(tmp_path)
    folder = tmp_path / "scan" / "deep"
    folder.mkdir(parents=True)
    (folder / "a.txt").write_text(f"{LEAK}\n", encoding="utf-8")
    (tmp_path / "scan" / "b.txt").write_text("clean text\n", encoding="utf-8")
    assert run(gt, tmp_path / "scan") == 1
    assert f"{folder / 'a.txt'}:1:" in capsys.readouterr().out
    assert (
        run(gt, gt) == 2
    )  # the only target is the ground-truth file: nothing left to scan
    assert "nothing to scan" in capsys.readouterr().err


def test_nothing_is_opened_without_gt_glob(tmp_path, monkeypatch, capsys):
    target = tmp_path / "target.md"
    target.write_text("text\n", encoding="utf-8")

    def refuse(*a, **k):
        raise AssertionError("a path was opened without --gt-glob")

    monkeypatch.setattr(builtins, "open", refuse)
    monkeypatch.setattr(Path, "read_text", refuse)
    monkeypatch.setattr(Path, "open", refuse)
    assert lint.main([str(target)]) == 2
    assert "--gt-glob is required" in capsys.readouterr().err
    assert lint.main(["--all"]) == 2


def test_bad_ground_truth_is_reported_without_content(tmp_path, capsys):
    bad = tmp_path / "bad-gt.json"
    bad.write_text("{secret phrase here", encoding="utf-8")
    target = tmp_path / "target.md"
    target.write_text("x\n", encoding="utf-8")
    assert run(bad, target) == 2
    assert "secret" not in capsys.readouterr().err
    assert lint.main(["--gt-glob", str(tmp_path / "none-*.json"), str(target)]) == 2


def test_no_real_ground_truth_path_in_lint_source():
    src = LINT_PY.read_text(encoding="utf-8")
    assert not re.search(r"ground-truth\S*\.json|ground-truth\*|/ground-truth", src)


def test_fixtures_clean(tmp_path, capsys):
    """AO-1 over SW/fixtures and the other DESIGN 13.1 folders that exist, against an invented ground truth."""
    gt = make_gt(tmp_path)
    targets = lint.default_targets(SW)
    assert SW / "fixtures" in targets and SW / "cards" in targets
    files = lint.expand_targets(targets)
    assert {f.name for f in files} >= {"schema.json", "README.md", "C1.json", "C8.json"}
    assert run(gt, *targets, extra=["--forbid", "orchard billing"]) == 0, (
        capsys.readouterr().out
    )


@pytest.mark.freeze
def test_real_files_against_real_gt():
    """Written, not run by the build. A maintainer gives the real ground-truth glob in LINT_REAL_GT_GLOB (never hard-coded)."""
    pattern = os.environ.get("LINT_REAL_GT_GLOB")
    assert pattern, (
        "LINT_REAL_GT_GLOB is not set: a maintainer must pass the real ground-truth glob"
    )
    assert lint.main(["--gt-glob", pattern, "--all"]) == 0
