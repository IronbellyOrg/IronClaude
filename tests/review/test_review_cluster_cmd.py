"""`superclaude review cluster`: clusters.json, clusters_kept.json, invalid cards, determinism."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.main import main


def _line(fid, path, start, end, refs, blocking=True):
    return json.dumps(
        {
            "id": fid,
            "severity": "MAJOR" if blocking else "MINOR",
            "blocking": blocking,
            "category": "other",
            "claim": f"claim {fid}",
            "refs": refs,
            "citations": [
                {"role": "plan", "path": path, "line_start": start, "line_end": end}
            ],
        }
    )


def _card(lines, calibration=None, fenced=True):
    text = (
        "review card\n\n## Findings block\n\n```findings-v2\n"
        + "\n".join(lines)
        + "\n```\n"
    )
    if calibration is not None:
        body = "calibration:\n  per_finding:\n" + "".join(
            f"    {k}: {{finding_confidence: {v}}}\n" for k, v in calibration.items()
        )
        text += "\n```yaml\n" + body + "```\n" if fenced else "\n" + body
    return text


@pytest.fixture
def run_dir(tmp_path):
    cards = tmp_path / "cards"
    cards.mkdir()
    (cards / "r1.md").write_text(
        _card(
            [
                _line("F1", "plan.md", 10, 12, ["R-1"]),
                _line("F2", "plan.md", 40, 41, ["R-2"]),
            ],
            {"F1": 0.9, "F2": 0.8},
        )
    )
    (cards / "r2.md").write_text(
        _card([_line("G1", "plan.md", 11, 12, ["R-1"])], {"G1": 0.7})
    )
    snap = tmp_path / "input-snapshot.yaml"
    snap.write_text("file_list:\n  - path: plan.md\n    sha256: abc\n")
    return tmp_path


def _run(run_dir, *extra, out="out"):
    args = [
        "review", "cluster", str(run_dir / "cards"),
        "--snapshot", str(run_dir / "input-snapshot.yaml"),
        "--out", str(run_dir / out), *extra,
    ]  # fmt: skip
    return CliRunner().invoke(main, args)


def _members(result):
    return sorted(
        (m["reviewer_id"], m["id"]) for c in result["clusters"] for m in c["members"]
    )


def test_two_cards_write_clusters_with_the_agreement(run_dir):
    res = _run(run_dir)
    assert res.exit_code == 0, res.output
    data = json.loads((run_dir / "out/panel/clusters.json").read_text())
    assert _members(data) == [("r1", "F1"), ("r1", "F2"), ("r2", "G1")]
    assert len(data["clusters"]) == 2
    # cluster {F1, G1}: support 1.0; cluster {F2}: 0.8 / 1.6 = 0.5; mean 0.75
    assert data["cluster_agreement"] == 0.75
    assert json.loads(res.output)["cluster_agreement"] == 0.75
    assert [c["state"] for c in data["cards"]] == ["complete", "complete"]
    assert not (run_dir / "out/panel/clusters_kept.json").exists()


def test_a_clean_card_is_complete_only_with_its_coverage_context(run_dir):
    (run_dir / "cards" / "r3.md").write_text(_card([]))

    def state(res):
        assert res.exit_code == 0, res.output
        data = json.loads((run_dir / "out/panel/clusters.json").read_text())
        return {c["reviewer_id"]: c["state"] for c in data["cards"]}["r3"]

    assert state(_run(run_dir)) == "invalid"
    cover = run_dir / "coverage.json"
    cover.write_text(json.dumps({"r3": {"assigned": ["R-1"], "observed": ["R-1"]}}))
    assert state(_run(run_dir, "--coverage", str(cover))) == "complete"
    # a nonempty coverage_rows is accepted when the assigned slice names it
    row = json.loads(_line("H1", "plan.md", 5, 6, ["R-1"]))
    row["coverage_rows"] = ["R-1"]
    (run_dir / "cards" / "r3.md").write_text(_card([json.dumps(row)]))
    assert state(_run(run_dir, "--coverage", str(cover))) == "complete"


def test_kept_pass_drops_unkept_ids_and_leaves_clusters_json_alone(run_dir):
    _run(run_dir)
    clusters = run_dir / "out/panel/clusters.json"
    before = clusters.read_bytes()
    kept = run_dir / "kept.txt"
    kept.write_text("F1\nG1\n")
    res = _run(run_dir, "--kept", str(kept))
    assert res.exit_code == 0, res.output
    assert clusters.read_bytes() == before
    data = json.loads((run_dir / "out/panel/clusters_kept.json").read_text())
    assert _members(data) == [("r1", "F1"), ("r2", "G1")]
    assert data["cluster_agreement"] == 1.0
    first = (run_dir / "out/panel/clusters_kept.json").read_bytes()
    _run(run_dir, "--kept", str(kept))
    assert (run_dir / "out/panel/clusters_kept.json").read_bytes() == first
    assert clusters.read_bytes() == before


def test_running_twice_is_byte_identical(run_dir):
    _run(run_dir)
    first = (run_dir / "out/panel/clusters.json").read_bytes()
    _run(run_dir)
    assert (run_dir / "out/panel/clusters.json").read_bytes() == first
    assert sorted(p.name for p in (run_dir / "out").rglob("*") if p.is_file()) == [
        "clusters.json"
    ]


def test_kept_line_can_pin_one_reviewer(run_dir):
    (run_dir / "cards/r2.md").write_text(
        _card([_line("F1", "plan.md", 11, 12, ["R-1"])], {"F1": 0.7})
    )
    kept = run_dir / "kept.txt"
    kept.write_text("# validator output\nr1:F1\nr1:F2\n")
    assert _run(run_dir, "--kept", str(kept)).exit_code == 0
    data = json.loads((run_dir / "out/panel/clusters_kept.json").read_text())
    assert _members(data) == [("r1", "F1"), ("r1", "F2")]


def test_invalid_card_is_reported_and_left_out_of_the_agreement(run_dir):
    (run_dir / "cards/bad.md").write_text(
        "card\n\n## Findings block\n\n```findings-v2\n{not json\n```\n"
    )
    res = _run(run_dir)
    assert res.exit_code == 0, res.output
    data = json.loads((run_dir / "out/panel/clusters.json").read_text())
    bad = next(c for c in data["cards"] if c["reviewer_id"] == "bad")
    assert bad["state"] == "invalid" and bad["errors"]
    assert data["invalid_reviewers"] == ["bad"]
    assert data["complete_reviewers"] == ["r1", "r2"]
    assert data["cluster_agreement"] == 0.75
    assert json.loads(res.output)["invalid"] == ["bad"]


def test_a_card_with_no_findings_block_is_invalid_not_a_crash(run_dir):
    (run_dir / "cards/none.md").write_text("just prose\n")
    res = _run(run_dir)
    assert res.exit_code == 0, res.output
    assert json.loads(res.output)["invalid"] == ["none"]


def test_fewer_than_two_valid_blocks_gives_null_agreement(run_dir):
    (run_dir / "cards/r2.md").write_text("no block\n")
    assert _run(run_dir).exit_code == 0
    data = json.loads((run_dir / "out/panel/clusters.json").read_text())
    assert data["cluster_agreement"] is None


def test_sidecar_and_unfenced_calibration(run_dir):
    (run_dir / "cards/r1.md").write_text(
        _card(
            [
                _line("F1", "plan.md", 10, 12, ["R-1"]),
                _line("F2", "plan.md", 40, 41, ["R-2"]),
            ],
            {"F1": 0.9, "F2": 0.8},
            fenced=False,
        )
    )
    (run_dir / "cards/r2.md").write_text(
        _card([_line("G1", "plan.md", 11, 12, ["R-1"])])
    )
    side = run_dir / "cal.json"
    side.write_text(json.dumps({"r2": {"G1": 0.7}}))
    assert _run(run_dir, "--calibration", str(side)).exit_code == 0
    data = json.loads((run_dir / "out/panel/clusters.json").read_text())
    assert data["cluster_agreement"] == 0.75 and data["uncalibrated"] == []


def test_calibration_coverage_is_reported(run_dir):
    res = _run(run_dir)
    assert json.loads(res.output)["calibrated_findings"] == "3/3"
    data = json.loads((run_dir / "out/panel/clusters.json").read_text())
    assert data["calibration_coverage"] == {
        "clustered_findings": 3,
        "calibrated_findings": 3,
    }


def test_calibration_ids_that_do_not_match_the_finding_ids_show_as_zero_coverage(
    run_dir,
):
    """Followed literally, a sidecar keyed R1-F1... against cards whose findings are F1... joins nothing."""
    side = run_dir / "cal.json"
    side.write_text(
        json.dumps({"r1": {"R1-F1": 0.9, "R1-F2": 0.8}, "r2": {"R2-G1": 0.7}})
    )
    for name in ("r1", "r2"):  # cards without an embedded block
        text = (run_dir / f"cards/{name}.md").read_text()
        (run_dir / f"cards/{name}.md").write_text(text.split("\n```yaml")[0] + "\n")
    res = _run(run_dir, "--calibration", str(side))
    assert res.exit_code == 0, res.output
    out = json.loads(res.output)
    assert out["calibrated_findings"] == "0/3" and out["cluster_agreement"] is None
    data = json.loads((run_dir / "out/panel/clusters.json").read_text())
    assert data["calibration_coverage"]["calibrated_findings"] == 0
    assert len(data["uncalibrated_findings"]) == 3


def test_kept_pass_reports_coverage_of_the_kept_findings(run_dir):
    kept = run_dir / "kept.txt"
    kept.write_text("F1\nG1\n")
    res = _run(run_dir, "--kept", str(kept))
    assert json.loads(res.output)["calibrated_findings"] == "2/2"


def test_cards_are_not_modified_and_an_empty_dir_is_an_error(run_dir):
    before = {p.name: p.read_bytes() for p in (run_dir / "cards").iterdir()}
    _run(run_dir)
    assert {p.name: p.read_bytes() for p in (run_dir / "cards").iterdir()} == before
    empty = run_dir / "empty"
    empty.mkdir()
    res = CliRunner().invoke(
        main,
        ["review", "cluster", str(empty), "--snapshot", str(run_dir / "input-snapshot.yaml"), "--out", str(run_dir / "o2")],
    )  # fmt: skip
    assert res.exit_code != 0 and "no *.md cards" in res.output
    assert not Path(run_dir / "o2").exists()


def test_review_help_lists_cluster():
    res = CliRunner().invoke(main, ["review", "--help"])
    assert res.exit_code == 0 and "cluster" in res.output
