"""Tests for scripts/reflect_verdict_replay.py (offline derive_verdict replay of recorded pre contracts)."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "scripts" / "reflect_verdict_replay.py"
_spec = importlib.util.spec_from_file_location("reflect_verdict_replay", SCRIPT)
rv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rv)

FIXTURE = Path(__file__).parent / "fixtures" / "panel_lint_legacy"


def run_dir(root: Path, name: str, **changes) -> Path:
    """A recorded-run directory: the 1.8.0 legacy fixture contract with `changes` applied."""
    d = root / name
    d.mkdir(parents=True)
    contract = yaml.safe_load((FIXTURE / "return-contract.yaml").read_text())
    contract.update(changes)
    (d / "return-contract.yaml").write_text(yaml.safe_dump(contract, sort_keys=False))
    return d


def shadow_dir(root: Path, name: str, **changes) -> Path:
    d = run_dir(root, name, **changes)
    (d / "panel").mkdir()
    (d / "panel/manifest.json").write_text(json.dumps({"reviewers_resolved": 3}))
    return d


def test_self_replay_reports_zero_differences(tmp_path, capsys):
    runs = tmp_path / "runs"
    run_dir(runs, "pre-a")
    run_dir(runs, "pre-b", status="success", citations_dropped=0)
    assert rv.main(["--runs-root", str(runs)]) == 0
    out = capsys.readouterr().out
    assert "differences: 0" in out and "new degraded reasons: 0" in out
    assert "self-replay" in out and "legacy runs replayed: 2" in out


def test_replaying_the_legacy_runs_as_the_shadow_set_is_also_clean(tmp_path, capsys):
    runs = tmp_path / "runs"
    a = run_dir(runs, "pre-a")
    b = run_dir(runs, "pre-b", status="success", citations_dropped=0)
    assert (
        rv.main(["--runs-root", str(runs), "--shadow", str(a), "--shadow", str(b)]) == 0
    )
    assert "differences: 0" in capsys.readouterr().out


def test_synthetic_shadow_with_a_new_degraded_reason_exits_nonzero(tmp_path, capsys):
    runs = tmp_path / "runs"
    run_dir(runs, "pre-a")  # legacy: degraded / verification-skipped
    shadow = shadow_dir(tmp_path / "shadow", "pre-new", adversarial_unavailable=True)
    assert rv.main(["--runs-root", str(runs), "--shadow", str(shadow)]) == 1
    out = capsys.readouterr().out
    assert (
        "new degraded reasons: 1" in out and "pre-new: adversarial-unavailable" in out
    )


def test_shadow_with_a_reason_the_legacy_set_already_has_is_not_new(tmp_path, capsys):
    runs = tmp_path / "runs"
    run_dir(runs, "pre-a")  # degraded / verification-skipped
    shadow = shadow_dir(tmp_path / "shadow", "pre-same")  # same contract: same reason
    assert rv.main(["--runs-root", str(runs), "--shadow", str(shadow)]) == 0
    assert "new degraded reasons: 0" in capsys.readouterr().out


def test_paired_run_whose_reason_changed_is_listed_and_flagged(tmp_path, capsys):
    runs = tmp_path / "runs"
    run_dir(runs, "pre-a")
    shadow = shadow_dir(tmp_path / "shadow", "pre-a", adversarial_unavailable=True)
    assert rv.main(["--runs-root", str(runs), "--shadow", str(shadow)]) == 1
    out = capsys.readouterr().out
    assert "differences: 1" in out
    assert (
        "legacy degraded/verification-skipped -> shadow degraded/adversarial-unavailable"
        in out
    )


def test_legacy_set_skips_shadow_runs_other_versions_and_bad_files(tmp_path, capsys):
    runs = tmp_path / "runs"
    run_dir(runs, "pre-ok")
    shadow_dir(runs, "pre-shadow")
    run_dir(runs, "pre-old", contract_version="1.7.0")
    (runs / "pre-empty").mkdir()
    bad = run_dir(runs, "pre-bad")
    (bad / "return-contract.yaml").write_bytes(b"\xff\xfe: [")
    (runs / "other-run").mkdir()
    legacy, skipped = rv.legacy_runs(runs)
    assert [d.name for d in legacy] == ["pre-ok"]
    assert dict(skipped) == {
        "pre-shadow": "has panel/manifest.json (a shadow run)",
        "pre-old": "contract_version '1.7.0'",
        "pre-empty": "no return-contract.yaml",
        "pre-bad": "unreadable or unparseable",
    }
    assert rv.main(["--runs-root", str(runs)]) == 0
    assert "skipped: 4" in capsys.readouterr().out


def test_unusable_shadow_directory_is_skipped_not_fatal(tmp_path, capsys):
    runs = tmp_path / "runs"
    run_dir(runs, "pre-a")
    empty = tmp_path / "shadow-empty"
    empty.mkdir()
    assert rv.main(["--runs-root", str(runs), "--shadow", str(empty)]) == 0
    out = capsys.readouterr().out
    assert "skipped shadow-empty: shadow: no return-contract.yaml" in out
    assert "shadow runs replayed: 0" in out


def test_derive_arguments_are_the_documented_ones():
    assert rv.DERIVE_ARGS == {"expected_tier": 2, "child_rc": 0}
    assert rv.SINGLE_VENDOR_MODES == (False, True)
    header = rv.__doc__
    for text in ("expected_tier=2", "child_rc=0", "allow_single_vendor"):
        assert text in header


def test_a_reason_hidden_behind_single_vendor_is_found_by_the_lenient_replay(
    tmp_path, capsys
):
    runs = tmp_path / "runs"
    run_dir(runs, "pre-a", t2_vendor_diversity="single")
    shadow = shadow_dir(
        tmp_path / "shadow",
        "pre-s",
        t2_vendor_diversity="single",
        adversarial_unavailable=True,
    )
    # strict: both runs say single-vendor, so nothing is new; lenient: adversarial-unavailable shows
    assert rv.replay(runs / "pre-a") == ("degraded", "single-vendor")
    assert rv.replay(shadow) == ("degraded", "single-vendor")
    assert rv.replay(shadow, allow_single_vendor=True) == (
        "degraded",
        "adversarial-unavailable",
    )
    assert rv.main(["--runs-root", str(runs), "--shadow", str(shadow)]) == 1
    out = capsys.readouterr().out
    assert (
        "== allow_single_vendor=True" in out and "pre-s: adversarial-unavailable" in out
    )


def test_self_replay_runs_derive_verdict_again(tmp_path, monkeypatch):
    runs = tmp_path / "runs"
    run_dir(runs, "pre-a")
    calls = []
    real = rv.replay
    monkeypatch.setattr(
        rv, "replay", lambda d, allow=False: calls.append(d.name) or real(d, allow)
    )
    assert rv.main(["--runs-root", str(runs)]) == 0
    assert (
        calls.count("pre-a") == 4
    )  # legacy and shadow side, for each of the two modes


def test_missing_runs_root_is_a_usage_error(tmp_path, capsys):
    assert rv.main(["--runs-root", str(tmp_path / "nope")]) == 2


def test_script_writes_nothing(tmp_path):
    runs = tmp_path / "runs"
    run_dir(runs, "pre-a")
    before = sorted(p.relative_to(tmp_path).as_posix() for p in tmp_path.rglob("*"))
    rv.main(["--runs-root", str(runs)])
    assert (
        sorted(p.relative_to(tmp_path).as_posix() for p in tmp_path.rglob("*"))
        == before
    )


@pytest.mark.skipif(
    not any((ROOT / ".dev" / "reflect").glob("pre-*/return-contract.yaml")),
    reason="no recorded reflect runs in this checkout",
)
def test_recorded_runs_replay_against_themselves(capsys):
    assert rv.main([]) == 0
    assert "differences: 0" in capsys.readouterr().out
