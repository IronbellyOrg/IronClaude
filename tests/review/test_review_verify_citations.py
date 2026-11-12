"""`superclaude review verify-citations`: advisory flags, the re-read set, and nothing dropped."""

from __future__ import annotations

import json

import pytest
from click.testing import CliRunner

from superclaude.cli.main import main


def _line(fid, path, start, end, quote=None):
    cit = {"role": "source", "path": path, "line_start": start, "line_end": end}
    if quote:
        cit["quote"] = quote
    return json.dumps(
        {
            "id": fid,
            "severity": "MAJOR",
            "blocking": True,
            "category": "other",
            "claim": f"claim {fid}",
            "refs": ["R-1"],
            "citations": [cit],
        }
    )


def _card(*lines):
    return (
        "card\n\n## Findings block\n\n```findings-v2\n" + "\n".join(lines) + "\n```\n"
    )


@pytest.fixture
def repo(tmp_path):
    root = tmp_path / "repo"
    (root / "src").mkdir(parents=True)
    (root / "src/a.py").write_text(
        "alpha beta gamma delta\nsecond line here\nthird line\n"
    )
    outside = tmp_path / "secret.txt"
    outside.write_text("x\n")
    (root / "src/link.txt").symlink_to(outside)
    cards = tmp_path / "cards"
    cards.mkdir()
    (cards / "r1.md").write_text(
        _card(
            _line("OK", "src/a.py", 1, 2, "alpha beta gamma delta"),
            _line("NOFILE", "src/nope.py", 1, 1),
            _line("RANGE", "src/a.py", 2, 9),
            _line("QUOTE", "src/a.py", 1, 1, "words that are not in the file"),
            _line("OUTSIDE", "src/link.txt", 1, 1),
        )
    )
    (cards / "r2.md").write_text(_card(_line("UNLISTED", "src/other.py", 1, 1)))
    snap = tmp_path / "input-snapshot.yaml"
    snap.write_text(
        "file_list:\n  - path: src/a.py\n  - path: src/nope.py\n  - path: src/link.txt\n"
    )
    return tmp_path, root


def _run(tmp, root, out="out"):
    return CliRunner().invoke(
        main,
        [
            "review", "verify-citations", "--cards", str(tmp / "cards"),
            "--snapshot", str(tmp / "input-snapshot.yaml"), "--root", str(root),
            "--out", str(tmp / out),
        ],
    )  # fmt: skip


def _result(tmp, out="out"):
    return json.loads((tmp / out / "panel/precheck.json").read_text())


def _by_id(result):
    return {(r["reviewer_id"], r["finding_id"]): r for r in result["citations"]}


def test_each_flag_and_a_clean_citation(repo):
    tmp, root = repo
    res = _run(tmp, root)
    assert res.exit_code == 0, res.output
    rows = _by_id(_result(tmp))
    assert rows[("r1", "OK")]["flag"] is None
    assert rows[("r1", "NOFILE")]["flag"] == "missing-file"
    assert rows[("r1", "RANGE")]["flag"] == "out-of-range"
    quote = rows[("r1", "QUOTE")]
    assert quote["flag"] == "quote-not-found" and quote["advisory"] is True
    assert rows[("r1", "NOFILE")]["advisory"] is False
    assert rows[("r1", "RANGE")]["advisory"] is False


def test_path_outside_the_snapshot_or_the_root_is_missing_file(repo):
    tmp, root = repo
    _run(tmp, root)
    rows = _by_id(_result(tmp))
    assert rows[("r2", "UNLISTED")]["flag"] == "missing-file"
    assert rows[("r2", "UNLISTED")]["reason"] == "not-in-snapshot"
    assert rows[("r1", "OUTSIDE")]["flag"] == "missing-file"
    assert rows[("r1", "OUTSIDE")]["reason"] == "outside-root"


def test_reread_set_lists_every_flagged_citation(repo):
    tmp, root = repo
    _run(tmp, root)
    result = _result(tmp)
    flagged = {
        (r["reviewer_id"], r["finding_id"]) for r in result["citations"] if r["flag"]
    }
    assert flagged == {("r1", f) for f in ("NOFILE", "RANGE", "QUOTE", "OUTSIDE")} | {
        ("r2", "UNLISTED")
    }
    assert {
        (r["reviewer_id"], r["finding_id"]) for r in result["reread_set"]
    } == flagged
    assert result["flagged"] == 5 and result["checked"] == 6
    assert result["by_flag"] == {
        "missing-file": 3,
        "out-of-range": 1,
        "quote-not-found": 1,
    }


def _keys(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from _keys(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _keys(v)


def test_nothing_is_dropped_and_no_card_changes(repo):
    tmp, root = repo
    before = {p.name: p.read_bytes() for p in (tmp / "cards").iterdir()}
    _run(tmp, root)
    assert not [k for k in _keys(_result(tmp)) if "drop" in k]
    assert {p.name: p.read_bytes() for p in (tmp / "cards").iterdir()} == before
    assert sorted(p.name for p in (tmp / "out").rglob("*") if p.is_file()) == [
        "precheck.json"
    ]


def test_running_twice_is_byte_identical(repo):
    tmp, root = repo
    _run(tmp, root)
    first = (tmp / "out/panel/precheck.json").read_bytes()
    _run(tmp, root)
    assert (tmp / "out/panel/precheck.json").read_bytes() == first


def test_empty_cards_dir_is_an_error(repo):
    tmp, root = repo
    (tmp / "empty").mkdir()
    res = CliRunner().invoke(
        main,
        ["review", "verify-citations", "--cards", str(tmp / "empty"), "--snapshot", str(tmp / "input-snapshot.yaml"), "--out", str(tmp / "o")],
    )  # fmt: skip
    assert res.exit_code != 0 and "no *.md cards" in res.output


def test_review_help_lists_verify_citations():
    res = CliRunner().invoke(main, ["review", "--help"])
    assert res.exit_code == 0 and "verify-citations" in res.output
