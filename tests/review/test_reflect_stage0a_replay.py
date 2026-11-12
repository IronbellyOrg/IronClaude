"""Tests for scripts/reflect_stage0a_replay.py on synthetic run directories built in tmp_path."""

from __future__ import annotations

import importlib.util
import json
import socket
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "reflect_stage0a_replay.py"
_spec = importlib.util.spec_from_file_location("reflect_stage0a_replay", SCRIPT)
replay = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(replay)

SNAP = json.dumps(
    {
        "file_list": [
            {"path": ".dev/tasks/to-do/T-1/T-1.md", "sha256": "x"},
            {"path": ".dev/tasks/to-do/T-1/source.md", "sha256": "y"},
            {"path": "src/a.py", "sha256": "z"},
        ]
    }
)


def _finding(i: int, evidence: str, **extra) -> dict:
    return {
        "id": f"F{i}",
        "severity": "minor",
        "category": "coverage",
        "claim": f"Finding number {i} misses a requirement",
        "evidence": [evidence],
        **extra,
    }


def _run(
    root: Path, name: str, cards: dict | None = None, snapshot: str | None = SNAP
) -> Path:
    run = root / ".dev" / "reflect" / name
    run.mkdir(parents=True)
    if cards is not None:
        (run / "reviewer-cards").mkdir()
        for fname, body in cards.items():
            text = body if isinstance(body, str) else json.dumps(body)
            (run / "reviewer-cards" / fname).write_text(text, encoding="utf-8")
    if snapshot is not None:
        (run / "artifacts").mkdir()
        (run / "artifacts" / "input-snapshot.yaml").write_text(
            snapshot, encoding="utf-8"
        )
    return run


def _report(root: Path) -> str:
    return replay.render(replay.collect(root))


# --- conversion share and the 90% gate ------------------------------------------------------


def test_share_at_exactly_90_percent_passes(tmp_path):
    good = [_finding(i, f"src/a.py:{i * 10}") for i in range(1, 10)]
    bad = [_finding(10, "no line ref here")]
    _run(tmp_path, "pre-a", {"reviewer-1-card.yaml": {"findings": good + bad}})
    data = replay.collect(tmp_path)
    s = data["summary"]
    assert (s["units"], s["converted"], s["share"]) == (10, 9, 0.9)
    text = replay.render(data)
    assert "Conversion share: 9/10 = 90.00%" in text
    assert "Reference value (at least 90%): met; no gate" in text
    assert "PASS" not in text and "FAIL" not in text


def test_share_below_90_percent_is_a_baseline_and_stops_nothing(tmp_path):
    good = [_finding(i, f"src/a.py:{i * 10}") for i in range(1, 9)]
    bad = [_finding(9, "plan:5"), _finding(10, "prose only")]
    _run(
        tmp_path,
        "pre-a",
        {"reviewer-1-card.yaml": {"findings": good + bad}},
        snapshot=None,
    )
    text = _report(tmp_path)
    assert "Conversion share: 8/10 = 80.00%" in text
    assert "Reference value (at least 90%): not met; no gate" in text
    assert replay.BASELINE_NOTE in text
    assert "FAIL" not in text and "must not ship" not in text
    assert "| unresolved citation: no path:line ref | 1 |" in text
    assert "| unresolved citation: no plan path | 1 |" in text


def test_unlisted_card_counts_as_one_unconverted_unit_and_is_listed(tmp_path):
    good = [_finding(i, f"src/a.py:{i * 10}") for i in range(1, 10)]
    _run(
        tmp_path,
        "pre-a",
        {
            "reviewer-1-card.yaml": {"findings": good},
            "reviewer-2-card.md": "# prose only\n",
        },
    )
    data = replay.collect(tmp_path)
    assert (data["summary"]["units"], data["summary"]["converted"]) == (10, 9)
    text = replay.render(data)
    assert "| unlisted | 1 | 1 | 0 | 1 | 0.00% |" in text
    assert (
        "`.dev/reflect/pre-a/reviewer-cards/reviewer-2-card.md`: no pipe table" in text
    )


def test_sidecars_and_summary_are_not_cards_and_are_listed(tmp_path):
    _run(
        tmp_path,
        "pre-a",
        {
            "reviewer-1-card.yaml": {"findings": [_finding(1, "src/a.py:1")]},
            "reviewer-1-calibration.yaml": "C: 0.5\n",
            "summary.md": "# summary\n",
        },
    )
    data = replay.collect(tmp_path)
    assert data["summary"]["cards"] == 1
    assert sorted(why for _, why in data["skipped_files"]) == [
        "calibration sidecar",
        "summary, not a card",
    ]


# --- null convergence scores -----------------------------------------------------------------


def _contract(run: Path, body: dict | str) -> None:
    text = body if isinstance(body, str) else json.dumps(body)
    (run / "return-contract.yaml").write_text(text, encoding="utf-8")


def test_null_score_causes(tmp_path):
    null = {"tier_reached": 2, "adversarial_convergence_score": None}
    _contract(
        _run(tmp_path, "pre-srf"), {**null, "merge_method": "single-reviewer-fallback"}
    )
    skip = _run(tmp_path, "pre-skip")
    _contract(skip, {**null, "merge_method": "adversarial"})
    (skip / "adversarial").mkdir()
    (skip / "adversarial" / "merge-log.md").write_text(
        "Log: variants substantially identical\n"
    )
    _contract(
        _run(tmp_path, "pre-illegal"),
        "tier_reached: 2\nmerge_method: inline-orchestrator   # not spawned\nconvergence_score: null\n",
    )
    _contract(_run(tmp_path, "pre-other"), null)
    _contract(_run(tmp_path, "pre-und-nodir"), {**null, "merge_method": "adversarial"})
    und = _run(tmp_path, "pre-und-log")
    _contract(und, {**null, "merge_method": "adversarial"})
    (und / "adversarial").mkdir()
    (und / "adversarial" / "merge-log.md").write_text("Debate ran two rounds.\n")
    _contract(
        _run(tmp_path, "pre-t1"),
        {"tier_reached": 1, "adversarial_convergence_score": None},
    )
    _contract(_run(tmp_path, "pre-num"), {**null, "adversarial_convergence_score": 0.9})
    _contract(
        _run(tmp_path, "pre-nokey"), {"tier_reached": 2, "merge_method": "adversarial"}
    )
    _contract(_run(tmp_path, "pre-bad"), "a: [\n")

    data = replay.collect(tmp_path)
    causes = {c["run"]: c["cause"] for c in data["contracts"] if c.get("counts")}
    assert causes == {
        "pre-srf": "single-reviewer-fallback",
        "pre-skip": "skipped-similar debate",
        "pre-illegal": "illegal merge_method value",
        "pre-other": "other",
        "pre-und-nodir": "undetermined",
        "pre-und-log": "undetermined",
    }
    text = replay.render(data)
    assert "Found 6 null scores" in text
    assert "skip marker at .dev/reflect/pre-skip/adversarial/merge-log.md:1" in text
    assert "merge_method: not spawned" in text
    assert "Cause not determined:" in text
    assert (
        "- `pre-und-nodir`: merge_method is adversarial and the run has no adversarial/ directory"
        in text
    )
    assert (
        "- `pre-und-log`: merge_method is adversarial and none of the 1 text file(s)"
        in text
    )
    assert (
        "Tier-2 contracts with no score key at all (not counted as null): `pre-nokey`."
        in text
    )
    assert "Null scores outside tier 2 (not counted): `pre-t1`." in text
    assert "`pre-bad` (not parsable (" in text
    assert (
        "By cause: skipped-similar debate 1, single-reviewer-fallback 1, illegal merge_method value 1, other 1, undetermined 2."
        in text
    )


def test_every_cause_determined_says_so(tmp_path):
    _contract(
        _run(tmp_path, "pre-srf"),
        {
            "tier_reached": 2,
            "adversarial_convergence_score": None,
            "merge_method": "single-reviewer-fallback",
        },
    )
    text = _report(tmp_path)
    assert "Every counted null score has a determined cause." in text


# --- calibration --------------------------------------------------------------------------------


def test_calibration_sources_and_uncalibrated_counts(tmp_path):
    embedded = {
        "findings": [_finding(1, "src/a.py:10"), _finding(2, "src/a.py:50")],
        "calibration": {
            "per_finding": {
                "F1": {"finding_confidence": 0.8},
                "F2": {"verdict": "confirmed"},
            }
        },
    }
    run = _run(
        tmp_path,
        "pre-a",
        {
            "reviewer-1-card.yaml": embedded,
            "reviewer-2-card.yaml": {
                "findings": [_finding(1, "src/a.py:10"), _finding(2, "src/a.py:90")]
            },
            "reviewer-3-card.yaml": {"findings": [_finding(1, "src/a.py:200")]},
        },
    )
    (run / "artifacts" / "reviewer-2-calibration.yaml").write_text(
        "per_finding:\n  - {id: F1, finding_confidence: 0.6}\n"
    )
    (run / "artifacts" / "t1-calibration.yaml").write_text(
        "per_finding: {F1: 0.1}\n"
    )  # T1 card, not a sidecar
    data = replay.collect(tmp_path)
    cal = {c["card"].rsplit("/", 1)[1]: c["calibration"] for c in data["cards"]}
    assert cal["reviewer-1-card.yaml"]["source"] == "embedded"
    assert cal["reviewer-1-card.yaml"]["per_finding"] == {
        "F1": ("numeric", 0.8),
        "F2": ("non-numeric entry", None),
    }
    assert cal["reviewer-2-card.yaml"]["source"] == "sidecar"
    assert cal["reviewer-2-card.yaml"]["per_finding"] == {
        "F1": ("numeric", 0.6),
        "F2": ("no entry", None),
    }
    assert cal["reviewer-3-card.yaml"] == {
        "source": "none",
        "per_finding": {"F1": ("no entry", None)},
    }
    text = replay.render(data)
    assert "| embedded | 1 | 2 | 1 | 1 | 0 |" in text
    assert "| sidecar | 1 | 2 | 1 | 0 | 1 |" in text
    assert "| none | 1 | 1 | 0 | 0 | 1 |" in text
    assert "Uncalibrated findings: 3 of 5." in text
    assert (
        "`.dev/reflect/pre-a/reviewer-cards/reviewer-1-card.yaml` (embedded): F2"
        in text
    )
    # The numeric confidences reach cluster_v2: the cluster of the two F1 findings has a support value.
    cluster = data["card_runs"][0]["cluster"]
    joined = next(c for c in cluster["clusters"] if len(c["reviewers"]) == 2)
    assert joined["member_scores"] == [0.8, 0.6]


def test_run_level_sidecar_section_and_markdown_sidecar(tmp_path):
    run = _run(
        tmp_path,
        "pre-a",
        {
            "reviewer-1-card.yaml": {"findings": [_finding(1, "src/a.py:10")]},
            "reviewer-2-card.yaml": {"findings": [_finding(1, "src/a.py:10")]},
        },
    )
    (run / "artifacts" / "calibration.yaml").write_text(
        "cards:\n  reviewer-1:\n    per_finding: {F1: 0.7}\n"
    )
    (run / "reviewer-cards" / "reviewer-2-calibration.md").write_text(
        "- F1 finding_confidence: 0.4\n"
    )
    cal = {
        c["card"].rsplit("/", 1)[1]: c["calibration"]
        for c in replay.collect(tmp_path)["cards"]
    }
    assert cal["reviewer-1-card.yaml"]["per_finding"]["F1"] == ("numeric", 0.7)
    assert cal["reviewer-2-card.yaml"]["per_finding"]["F1"] == ("numeric", 0.4)


# --- clusters and agreement with the merged verdict --------------------------------------------


def test_agreement_formula_with_the_merged_verdict(tmp_path):
    run = _run(
        tmp_path,
        "pre-a",
        {
            "reviewer-1-card.yaml": {"findings": [_finding(1, "src/a.py:10")]},
            "reviewer-2-card.yaml": {"findings": [_finding(1, "src/a.py:12")]},
        },
    )
    (run / "adversarial").mkdir()
    merged = {"findings": [_finding(1, "src/a.py:11"), _finding(2, "src/a.py:500")]}
    (run / "adversarial" / "merged-verdict.yaml").write_text(json.dumps(merged))
    nomerged = _run(
        tmp_path,
        "pre-b",
        {"reviewer-1-card.yaml": {"findings": [_finding(1, "src/a.py:1")]}},
    )
    (nomerged / "adversarial").mkdir()
    (nomerged / "adversarial" / "merged-verdict.yaml").write_text("verdict: pass\n")
    text = _report(tmp_path)
    assert (
        "agreement = (recorded merged-verdict findings that fall in a multi-reviewer cluster)"
        in text
    )
    assert "This number is descriptive and seeds no gate." in text
    assert (
        "Merged verdicts read: 1 of 2; findings read: 2; falling in a multi-reviewer cluster: 1; agreement: 1/2 = 50.00%"
        in text
    )
    assert "| `pre-a` | 2 | 1 | 1 | 50.00% |" in text
    assert "- `pre-b`: not a YAML mapping with a findings" in text
    assert "Totals over 2 runs: 3 clustered findings, 2 clusters" in text


def test_missing_snapshot_is_counted_and_resolves_nothing(tmp_path):
    _run(
        tmp_path,
        "pre-a",
        {"reviewer-1-card.yaml": {"findings": [_finding(1, "src/a.py:10")]}},
        snapshot=None,
    )
    data = replay.collect(tmp_path)
    assert data["card_runs"][0]["snapshot"] == "missing"
    assert data["card_runs"][0]["cluster"]["citations"] == {
        "resolved": 0,
        "unresolved": 1,
        "malformed": 0,
    }
    assert "`pre-a` (missing)" in replay.render(data)


def test_malformed_files_are_reported_not_raised(tmp_path):
    run = _run(
        tmp_path,
        "pre-a",
        {
            "reviewer-1-card.yaml": "findings: [\n",
            "reviewer-2-card.yaml": {"findings": ["not a mapping"]},
        },
        snapshot="file_list: [\n",
    )
    (run / "adversarial").mkdir()
    (run / "adversarial" / "merged-verdict.yaml").write_text("findings: [\n")
    _contract(run, "- just a list\n")
    (run / "artifacts" / "reviewer-1-calibration.yaml").write_text("per_finding: [\n")
    text = _report(tmp_path)
    assert "reviewer-1-card.yaml`: not a YAML mapping" in text
    assert (
        "`pre-a` (not parsable (ScannerError))" in text
        or "`pre-a` (not parsable (ParserError))" in text
    )
    assert "`pre-a` (not a mapping)" in text
    assert "reviewer-1-calibration.yaml` (not parsable (" in text
    assert "| entry N is not a mapping | 1 |" in text


# --- no dispatch, determinism, output path --------------------------------------------------


def _forbid(*_a, **_k):
    raise AssertionError(
        "the replay must not open a network connection or start a process"
    )


def test_main_dispatches_no_model_and_is_deterministic(tmp_path, monkeypatch, capsys):
    run = _run(
        tmp_path,
        "pre-a",
        {"reviewer-1-card.yaml": {"findings": [_finding(1, "src/a.py:10")]}},
    )
    _contract(
        run,
        {
            "tier_reached": 2,
            "adversarial_convergence_score": None,
            "merge_method": "none",
        },
    )
    monkeypatch.setattr(socket.socket, "connect", _forbid)
    monkeypatch.setattr(socket, "create_connection", _forbid)
    monkeypatch.setattr(subprocess, "Popen", _forbid)
    monkeypatch.setattr("os.system", _forbid)
    out1, out2 = tmp_path / "o1" / "r.md", tmp_path / "o2" / "r.md"
    assert replay.main(["--root", str(tmp_path), "--out", str(out1)]) == 0
    assert replay.main(["--root", str(tmp_path), "--out", str(out2)]) == 0
    assert out1.read_bytes() == out2.read_bytes()
    text = out1.read_text()
    assert str(tmp_path) not in text
    assert "(baseline, no gate)" in capsys.readouterr().out


def test_default_output_path(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert replay.default_out(tmp_path) == Path("artifacts") / "stage0a-report.md"
    package = tmp_path / ".dev" / "tasks" / "to-do" / replay.PLAN_ID
    package.mkdir(parents=True)
    assert replay.default_out(tmp_path) == package / "artifacts" / "stage0a-report.md"


def test_no_runs_gives_a_baseline_report_without_raising(tmp_path):
    text = _report(tmp_path)
    assert "Conversion share: 0/0 = n/a" in text
    assert "Reference value (at least 90%): n/a (nothing measured); no gate" in text
    assert replay.BASELINE_NOTE in text


@pytest.mark.parametrize("plan_key", ["card_dirs", "merged", "nulls"])
def test_plan_numbers_are_stated_with_the_difference(tmp_path, plan_key):
    text = _report(tmp_path)
    assert (
        f"say {replay.PLAN_NUMBERS[plan_key]}; difference -{replay.PLAN_NUMBERS[plan_key]}"
        in text
    )
