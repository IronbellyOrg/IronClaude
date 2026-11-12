"""Tests for scripts/reflect_cluster_pairs.py (the 50-pair cluster check sheet and its scorer)."""

from __future__ import annotations

import csv
import importlib.util
import io
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "reflect_cluster_pairs.py"
_spec = importlib.util.spec_from_file_location("reflect_cluster_pairs", SCRIPT)
cp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cp)

ARTIFACT = (
    ROOT
    / ".dev/tasks/to-do/TASK-WF-implementStages0-20261111-202912/artifacts/cluster-pairs-50.csv"
)
SNAP = json.dumps(
    {
        "file_list": [
            {"path": ".dev/tasks/to-do/T-1/T-1.md", "sha256": "x"},
            {"path": ".dev/tasks/to-do/T-1/source.md", "sha256": "y"},
            {"path": "src/a.py", "sha256": "z"},
        ]
    }
)


def _card(*evidence: str) -> str:
    return json.dumps(
        {
            "findings": [
                {
                    "id": f"F{i}",
                    "severity": "minor",
                    "category": "coverage",
                    "claim": f"Finding number {i} misses a requirement",
                    "evidence": [ev],
                }
                for i, ev in enumerate(evidence, 1)
            ]
        }
    )


def _run(root: Path, name: str, cards: dict[str, str]) -> None:
    run = root / ".dev" / "reflect" / name
    (run / "reviewer-cards").mkdir(parents=True)
    (run / "artifacts").mkdir()
    (run / "artifacts" / "input-snapshot.yaml").write_text(SNAP, encoding="utf-8")
    for fname, body in cards.items():
        (run / "reviewer-cards" / fname).write_text(body, encoding="utf-8")


def _tree(root: Path) -> None:
    """r1: a.py:10, a.py:100, plan:5, b.py:10 (not in the snapshot); r2: a.py:12, a.py:200, prose only."""
    _run(
        root,
        "pre-a",
        {
            "reviewer-1-card.yaml": _card(
                "src/a.py:10", "src/a.py:100", "plan:5", "src/b.py:10"
            ),
            "reviewer-2-card.yaml": _card("src/a.py:12", "src/a.py:200", "prose only"),
        },
    )


def _fake(n_merged: int, n_apart_same: int, n_apart_cross: int) -> list[dict]:
    out = []
    for verdict, rel, n in (
        ("merged", "same-file", n_merged),
        ("apart", "same-file", n_apart_same),
        ("apart", "cross-file", n_apart_cross),
    ):
        for i in range(n):
            out.append(
                {
                    "run": f"pre-{verdict}-{rel}",
                    "cluster_v2_verdict": verdict,
                    "file_relation": rel,
                    "reviewer_a": "r1",
                    "finding_a": f"F{i:03d}",
                    "cluster_a": "C1",
                    "claim_a": f'claim a, {i} with "quotes"',
                    "citations_a": f"source src/a.py:{i}-{i} (resolved)",
                    "reviewer_b": "r2",
                    "finding_b": f"F{i:03d}",
                    "cluster_b": "C1" if verdict == "merged" else "C2",
                    "claim_b": f"claim b {i}",
                    "citations_b": f"source src/a.py:{i}-{i} (resolved)",
                }
            )
    return out


def _filled(tmp_path: Path, rows: list[dict], labels: list[str]) -> Path:
    """Write a sheet with render() and fill its label column, as the owner would."""
    stats = cp.select(rows)[1]
    text = cp.render(rows, stats)
    comments = [line for line in text.splitlines(True) if line.startswith("#")]
    data = list(csv.DictReader(io.StringIO(text[len("".join(comments)) :])))
    for row, label in zip(data, labels):
        row["human_same_defect"] = label
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=cp.COLUMNS, lineterminator="\n")
    w.writeheader()
    w.writerows(data)
    path = tmp_path / "filled.csv"
    path.write_text("".join(comments) + buf.getvalue(), encoding="utf-8")
    return path


def _score(path: Path, capsys) -> tuple[int, str, str]:
    code = cp.main(["score", "--sheet", str(path)])
    out = capsys.readouterr()
    return code, out.out, out.err


# --- pairs -------------------------------------------------------------------------------------


def test_pairs_cover_verdict_relation_and_exclude_same_reviewer(tmp_path):
    _tree(tmp_path)
    pairs, problems, no_claim = cp.candidates(tmp_path)
    assert problems == [] and no_claim == 0
    assert (
        len(pairs) == 12
    )  # 4 findings of r1 x 3 of r2; r1-r1 and r2-r2 pairs are not drawn
    assert all(p["reviewer_a"] != p["reviewer_b"] for p in pairs)
    merged = [p for p in pairs if p["cluster_v2_verdict"] == "merged"]
    assert [(p["finding_a"], p["finding_b"]) for p in merged] == [("F1", "F1")]
    assert merged[0]["file_relation"] == "same-file"
    assert all(
        (p["cluster_a"] == p["cluster_b"]) == (p["cluster_v2_verdict"] == "merged")
        for p in pairs
    )
    apart = [p for p in pairs if p["cluster_v2_verdict"] == "apart"]
    same = {
        (p["finding_a"], p["finding_b"])
        for p in apart
        if p["file_relation"] == "same-file"
    }
    # a path missing from the snapshot (src/b.py) still counts as a file; prose has no path
    assert same == {("F1", "F2"), ("F2", "F1"), ("F2", "F2")}
    assert sum(p["file_relation"] == "cross-file" for p in apart) == 8
    row = next(p for p in pairs if p["finding_a"] == "F4" and p["finding_b"] == "F3")
    assert row["citations_a"] == "source src/b.py:10-10 (unresolved)"
    assert row["citations_b"] == "unresolved prose only"
    assert row["claim_a"] == "Finding number 4 misses a requirement"


def test_pairs_inside_a_chained_cluster_are_not_drawn(tmp_path):
    _run(
        tmp_path,
        "pre-chain",
        {
            "reviewer-1-card.yaml": _card("src/a.py:10", "src/a.py:300"),
            "reviewer-2-card.yaml": _card("src/a.py:13"),
            "reviewer-3-card.yaml": _card("src/a.py:16"),
        },
    )
    pairs, _, _ = cp.candidates(tmp_path)
    keys = {
        (p["reviewer_a"], p["finding_a"], p["reviewer_b"], p["finding_b"])
        for p in pairs
    }
    assert keys == {
        ("reviewer-1-card", "F2", "reviewer-2-card", "F1"),
        ("reviewer-1-card", "F2", "reviewer-3-card", "F1"),
    }
    assert all(p["cluster_v2_verdict"] == "apart" for p in pairs)


def test_pairs_are_drawn_within_one_run_only(tmp_path):
    _run(tmp_path, "pre-x", {"reviewer-1-card.yaml": _card("src/a.py:10")})
    _run(tmp_path, "pre-y", {"reviewer-2-card.yaml": _card("src/a.py:10")})
    assert cp.candidates(tmp_path) == ([], [], 0)


def test_missing_citations_get_a_placeholder(tmp_path):
    bare = json.dumps(
        {"findings": [{"id": "Q1", "severity": "minor", "claim": "No evidence"}]}
    )
    _run(
        tmp_path,
        "pre-bare",
        {"reviewer-1-card.yaml": bare, "reviewer-2-card.yaml": _card("src/a.py:1")},
    )
    (pair,), _, no_claim = cp.candidates(tmp_path)
    assert no_claim == 0 and pair["claim_a"] == "No evidence"
    assert pair["citations_a"] == "(no citation)"
    assert pair["file_relation"] == "cross-file"


def test_pairs_with_a_finding_without_claim_text_are_left_out_and_counted(
    tmp_path, capsys
):
    # Q1 has no claim, Q2 a whitespace claim, Q3 a claim; r2 has two findings with claims.
    card = json.dumps(
        {
            "findings": [
                {"id": "Q1", "severity": "minor", "evidence": ["src/a.py:1"]},
                {"id": "Q2", "severity": "minor", "claim": "  ", "evidence": ["x"]},
                {"id": "Q3", "severity": "minor", "claim": "Real", "evidence": ["y"]},
            ]
        }
    )
    _run(
        tmp_path,
        "pre-noclaim",
        {
            "reviewer-1-card.yaml": card,
            "reviewer-2-card.yaml": _card("src/a.py:1", "src/a.py:500"),
        },
    )
    pairs, problems, no_claim = cp.candidates(tmp_path)
    assert problems == [] and no_claim == 4  # Q1 and Q2 each with r2's F1 and F2
    assert {(p["finding_a"], p["finding_b"]) for p in pairs} == {
        ("Q3", "F1"),
        ("Q3", "F2"),
    }
    assert all(p["claim_a"].strip() and p["claim_b"].strip() for p in pairs)
    out = tmp_path / "sheet.csv"
    assert cp.main(["sample", "--root", str(tmp_path), "--out", str(out)]) == 1
    capsys.readouterr()
    text = out.read_text(encoding="utf-8")
    assert (
        "# no claim text: 4 pairs left out (a finding has no claim text after conversion)\n"
        in text
    )
    assert "no claim text after conversion;" not in text
    assert len(cp.read_sheet(out)) == 2
    assert "# no claim text: 0 pairs left out" in cp.render(*cp.select(_fake(1, 1, 1)))


def test_merged_pairs_match_the_replay_clusters(tmp_path):
    _tree(tmp_path)
    data = cp.replay.collect(tmp_path)
    clusters = data["card_runs"][0]["cluster"]["clusters"]
    expected = {
        tuple(sorted((m["reviewer_id"], m["id"]) for m in c["members"]))
        for c in clusters
        if len(c["members"]) == 2 and not c["chained"]
    }
    pairs, _, _ = cp.candidates(tmp_path)
    got = {
        ((p["reviewer_a"], p["finding_a"]), (p["reviewer_b"], p["finding_b"]))
        for p in pairs
        if p["cluster_v2_verdict"] == "merged"
    }
    assert got == expected


# --- sampling ----------------------------------------------------------------------------------


def test_select_draws_25_per_side_with_a_file_mix_and_a_fixed_seed():
    pool = _fake(30, 40, 40)
    rows, stats = cp.select(pool)
    assert stats["rows"] == 50 and stats["shortfall"] == {"merged": 0, "apart": 0}
    assert stats["sampled"][("merged", "same-file")] == 25
    assert stats["sampled"][("apart", "same-file")] == 13
    assert stats["sampled"][("apart", "cross-file")] == 12
    assert [r["pair_id"] for r in rows] == [f"P{i:02d}" for i in range(1, 51)]
    assert all(r["human_same_defect"] == "" for r in rows)
    assert rows == cp.select(list(reversed(pool)))[0]  # input order does not matter
    assert rows != cp.select(pool, seed=1)[0]
    text = cp.render(rows, stats)
    assert text == cp.render(*cp.select(pool))
    assert "# status: COMPLETE\n" in text and "# shortfall: none\n" in text
    assert f"seed {cp.SEED}" in text


def test_select_fills_a_short_file_group_from_the_other():
    rows, stats = cp.select(_fake(25, 3, 40))
    assert stats["sampled"][("apart", "same-file")] == 3
    assert stats["sampled"][("apart", "cross-file")] == 22
    assert stats["rows"] == 50


def test_shortfall_is_written_in_the_header_and_reported_insufficient(tmp_path):
    rows, stats = cp.select(_fake(1, 5, 3))
    assert stats["shortfall"] == {"merged": 24, "apart": 17}
    text = cp.render(rows, stats)
    assert "# rows: 9 of 50 (merged 1 of 25; apart 8 of 25)\n" in text
    assert "# shortfall: merged 24; apart 17\n" in text
    assert "# status: INSUFFICIENT PAIRS (9 rows; fewer than 50)\n" in text
    path = tmp_path / "s.csv"
    path.write_text(text, encoding="utf-8")
    assert len(cp.read_sheet(path)) == 9  # the comment lines are skipped by the reader


def test_sample_cli_writes_a_deterministic_sheet_and_exits_1_when_short(
    tmp_path, capsys
):
    _tree(tmp_path)
    out = tmp_path / "out" / "sheet.csv"
    assert cp.main(["sample", "--root", str(tmp_path), "--out", str(out)]) == 1
    printed = capsys.readouterr().out
    assert "INSUFFICIENT PAIRS: 12 rows, fewer than 50; not a pass" in printed
    first = out.read_bytes()
    assert cp.main(["sample", "--root", str(tmp_path), "--out", str(out)]) == 1
    assert out.read_bytes() == first
    text = first.decode()
    assert str(tmp_path) not in text
    rows = cp.read_sheet(out)
    assert len(rows) == 12
    assert all(r["human_same_defect"] == "" for r in rows)
    assert all(r["claim_a"] and r["claim_b"] and r["citations_a"] for r in rows)
    assert "# shortfall: merged 24; apart 14\n" in text


def test_sample_cli_without_recorded_runs_writes_an_empty_insufficient_sheet(
    tmp_path, capsys
):
    out = tmp_path / "sheet.csv"
    assert cp.main(["sample", "--root", str(tmp_path / "none"), "--out", str(out)]) == 1
    assert "INSUFFICIENT PAIRS: 0 rows" in capsys.readouterr().out
    assert cp.read_sheet(out) == []


def test_sample_cli_reports_an_unwritable_output(tmp_path, capsys):
    assert cp.main(["sample", "--root", str(tmp_path), "--out", str(tmp_path)]) == 2
    assert "cannot write" in capsys.readouterr().err


def test_malformed_cards_do_not_crash_the_sampler(tmp_path):
    _run(
        tmp_path,
        "pre-bad",
        {
            "reviewer-1-card.yaml": "findings: [\n",
            "reviewer-2-card.md": "# prose only\n",
            "reviewer-3-card.txt": "x",
        },
    )
    assert cp.candidates(tmp_path) == ([], [], 0)


# --- score -------------------------------------------------------------------------------------


def test_score_reports_confusion_precision_and_recall(tmp_path, capsys):
    rows = cp.select(_fake(25, 13, 12))[0]
    # rows 1-25 merged, 26-50 apart: merged 20 yes / 5 no, apart 2 yes / 23 no
    labels = ["yes"] * 20 + ["no"] * 5 + ["Y", " TRUE "] + ["n", "False"] + ["no"] * 21
    code, out, err = _score(_filled(tmp_path, rows, labels), capsys)
    assert (code, err) == (0, "")
    assert out.splitlines() == [
        "pairs scored: 50",
        "confusion: TP=20 FP=5 FN=2 TN=23",
        "precision: 0.8000 (20/25)",
        "recall: 0.9091 (20/22)",
        "status: SCORED",
    ]


def test_reading_form_hides_the_verdict_and_its_answers_score_like_the_sheet(
    tmp_path, capsys
):
    rows = cp.select(_fake(25, 13, 12))[0]
    labels = ["yes"] * 20 + ["no"] * 5 + ["y", "yes"] + ["n", "no"] + ["no"] * 21
    sheet = _filled(tmp_path, rows, ["" for _ in labels])
    form = tmp_path / "form.md"
    assert cp.main(["form", "--sheet", str(sheet), "--out", str(form)]) == 0
    text = form.read_text(encoding="utf-8")
    assert "merged" not in text and "apart" not in text  # the verdict is not shown
    assert text.count("\nANSWER P") == 50 and "src/a.py" not in text  # short citations
    # a person fills the ANSWER lines; the commas and quotes of a claim never touch the columns
    answers = text
    for i, label in enumerate(labels, 1):
        answers = answers.replace(f"ANSWER P{i:02d}: ", f"ANSWER P{i:02d}: {label}", 1)
    filled = tmp_path / "answers.md"
    filled.write_text(answers, encoding="utf-8")
    code = cp.main(["score", "--sheet", str(sheet), "--answers", str(filled)])
    out = capsys.readouterr().out
    assert code == 0 and "confusion: TP=20 FP=5 FN=2 TN=23" in out


def test_an_answer_for_an_unknown_pair_is_an_error(tmp_path, capsys):
    rows = cp.select(_fake(25, 13, 12))[0]
    sheet = _filled(tmp_path, rows, ["yes"] * 50)
    bad = tmp_path / "answers.md"
    bad.write_text("ANSWER P99: yes\n", encoding="utf-8")
    assert cp.main(["score", "--sheet", str(sheet), "--answers", str(bad)]) == 1
    assert "unknown pair(s): P99" in capsys.readouterr().err


def test_scoring_an_unfilled_sheet_fails_naming_the_missing_labels(tmp_path, capsys):
    rows = cp.select(_fake(25, 13, 12))[0]
    code, out, err = _score(_filled(tmp_path, rows, [""] * 50), capsys)
    assert code == 1 and out == ""
    assert "missing human_same_defect label for 50 pair(s): P01, P02" in err
    assert "P50" in err


def test_scoring_a_partly_filled_sheet_names_only_the_missing_labels(tmp_path, capsys):
    rows = cp.select(_fake(25, 13, 12))[0]
    labels = ["yes"] * 50
    labels[6] = labels[41] = ""
    code, _, err = _score(_filled(tmp_path, rows, labels), capsys)
    assert code == 1
    assert "missing human_same_defect label for 2 pair(s): P07, P42" in err


def test_score_rejects_a_label_outside_the_vocabulary(tmp_path, capsys):
    rows = cp.select(_fake(25, 13, 12))[0]
    labels = ["yes"] * 50
    labels[2] = "maybe"
    code, _, err = _score(_filled(tmp_path, rows, labels), capsys)
    assert code == 1
    assert "label not in yes/no/y/n/true/false for 1 pair(s): P03='maybe'" in err


def test_score_reports_zero_denominators_as_undefined(tmp_path, capsys):
    path = tmp_path / "sheet.csv"
    path.write_text(
        "pair_id,cluster_v2_verdict,human_same_defect\n"
        + "".join(f"P{i:02d},apart,no\n" for i in range(1, 51)),
        encoding="utf-8",
    )
    code, out, _ = _score(path, capsys)
    assert code == 0
    assert out.splitlines() == [
        "pairs scored: 50",
        "confusion: TP=0 FP=0 FN=0 TN=50",
        "precision: undefined (0/0)",
        "recall: undefined (0/0)",
        "status: SCORED",
    ]


def test_score_with_fewer_than_50_rows_is_insufficient_never_a_pass(tmp_path, capsys):
    rows = cp.select(_fake(3, 2, 2))[0]
    code, out, _ = _score(_filled(tmp_path, rows, ["yes"] * 7), capsys)
    assert code == 1
    assert "status: INSUFFICIENT PAIRS (7 rows; fewer than 50; not a pass)" in out
    assert "SCORED" not in out


@pytest.mark.parametrize(
    ("body", "code", "message"),
    [
        (None, 2, "cannot read sheet"),
        ("", 2, "has no header row"),
        ("# only a comment\n", 2, "has no header row"),
        (
            "pair_id,cluster_v2_verdict\nP01,merged\n",
            2,
            "lacks the column(s): human_same_defect",
        ),
        (
            "pair_id,cluster_v2_verdict,human_same_defect\n",
            1,
            "the sheet has no pair rows",
        ),
        (
            "pair_id,cluster_v2_verdict,human_same_defect\nP01,maybe,yes\n",
            1,
            "P01: cluster_v2_verdict 'maybe' is not merged or apart",
        ),
        (
            "pair_id,cluster_v2_verdict,human_same_defect\nP01,merged,yes\nP01,apart,no\n",
            1,
            "duplicate pair_id P01",
        ),
        ("pair_id,cluster_v2_verdict,human_same_defect\nP01\n", 1, "pair(s): P01"),
        ("pair_id,cluster_v2_verdict,human_same_defect\n,merged,\n", 1, "data row 1"),
    ],
)
def test_score_reports_bad_sheets_without_crashing(
    tmp_path, capsys, body, code, message
):
    path = tmp_path / "sheet.csv"
    if body is not None:
        path.write_text(body, encoding="utf-8")
    got, out, err = _score(path, capsys)
    assert got == code
    assert message in err and out == ""


def test_score_skips_spreadsheet_saved_comments_and_a_bom(tmp_path, capsys):
    path = tmp_path / "sheet.csv"
    path.write_text(
        '﻿"# rows: 1 of 50, saved by a spreadsheet",,\n'
        "pair_id,cluster_v2_verdict,human_same_defect\n"
        ",,\n"
        "P01,merged,yes\n",
        encoding="utf-8",
    )
    code, out, _ = _score(path, capsys)
    assert "confusion: TP=1 FP=0 FN=0 TN=0" in out
    assert code == 1  # one row is fewer than 50


# --- the generated artifact --------------------------------------------------------------------


@pytest.mark.skipif(
    not ARTIFACT.is_file(), reason="sheet not generated in this checkout"
)
def test_generated_sheet_has_50_rows_and_blank_labels():
    rows = cp.read_sheet(ARTIFACT)
    assert len(rows) == 50
    assert all(r["human_same_defect"] == "" for r in rows)
    assert sum(r["cluster_v2_verdict"] == "merged" for r in rows) == 25
    assert {r["file_relation"] for r in rows} == {"same-file", "cross-file"}
    assert all(r["claim_a"].strip() and r["claim_b"].strip() for r in rows)
    assert all(r["citations_a"] and r["citations_b"] for r in rows)
    text = ARTIFACT.read_text(encoding="utf-8")
    assert "no claim text after conversion;" not in text  # the old lookup placeholder
    assert all(
        not r[c].startswith("(no claim") for r in rows for c in ("claim_a", "claim_b")
    )
    assert "# status: COMPLETE\n" in text and "# shortfall: none\n" in text
    assert "\n# no claim text: " in text
