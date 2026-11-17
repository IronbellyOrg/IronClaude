"""Tests for scripts/reflect_shadow_exit.py (Stage 2 shadow-exit aggregator) on synthetic shadow run directories."""

from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from superclaude.cli.main import main
from superclaude.cli.review import manifest as mf

ROOT = Path(__file__).resolve().parents[3]
_spec = importlib.util.spec_from_file_location(
    "reflect_shadow_exit", ROOT / "scripts" / "reflect_shadow_exit.py"
)
se = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(se)

FIXTURE = Path(__file__).parent / "fixtures" / "panel_lint_legacy"
RESOLVE = [
    "review", "panel", "resolve", "--template", "@reflect-pre", "--run-id", "r1",
    "--kind", "first", "--env", "anthropic-only", "--strict-distinct",
]  # fmt: skip
RESOLUTION = CliRunner().invoke(main, RESOLVE).output
H = "a" * 64


def legacy_run(root: Path, name: str, **changes) -> Path:
    """A recorded-style legacy run: the 1.8.0 fixture (no panel/ directory)."""
    d = root / name
    shutil.copytree(FIXTURE, d)
    contract = yaml.safe_load((d / "return-contract.yaml").read_text())
    contract.update(changes)
    (d / "return-contract.yaml").write_text(yaml.safe_dump(contract, sort_keys=False))
    return d


def shadow_run(
    root: Path,
    name: str,
    *,
    state: str = "published",
    complete: int = 3,
    audit: str = '{"wave": 5, "step": "5.0", "outcome": "ok"}\n',
    card_class: dict[int, str] | None = None,
    telemetry: dict | None = None,
    **top,
) -> Path:
    """A clean synthetic shadow run: legacy fixture + panel/ with manifest, resolution and card headers."""
    d = legacy_run(root, name)
    contract = yaml.safe_load((d / "return-contract.yaml").read_text())
    tel = (
        contract.get("telemetry") if isinstance(contract.get("telemetry"), dict) else {}
    )
    tel.update(
        reviewer_personas=["analyzer", "qa", "refactorer"],
        reviewer_models=["sonnet", "haiku", "opus"],
        executor_class_resolved=True,
        panel_parity=True,
        cluster_agreement=0.8,
        findings_block_compliance_rate=1.0,
    )
    tel.update(telemetry or {})
    contract["telemetry"] = tel
    contract.update(top)
    (d / "return-contract.yaml").write_text(yaml.safe_dump(contract, sort_keys=False))
    frozen = {
        "snapshot_ref": "artifacts/input-snapshot.yaml", "snapshot_sha256": H,
        "input_tree_sha256": H, "template_sha256": H, "tiers_sha256": H,
        "brief_template_sha256": H, "schema_ids": ["review-panel/1"],
    }  # fmt: skip
    m = mf.new_manifest(
        run_id=name, frozen=frozen, engine_requested="shadow", engine_effective="shadow"
    )
    stages = list(mf.STATES[1:])
    upto = stages.index(state) + 1 if state in stages else 0
    for stage in stages[:upto]:
        payload = (
            {"reviewers_requested": 3, "reviewers_resolved": 3}
            if stage == "resolved"
            else {}
        )
        mf.advance_stage(m, stage, payload)
    if state == "failed":
        mf.fail(m, "deadline")
    m["reviewers_complete"] = complete
    mf.save(d / "panel" / "manifest.json", m)
    (d / "panel" / "resolution.json").write_text(RESOLUTION)
    (d / "panel" / "cards").mkdir()
    for n, r in enumerate(json.loads(RESOLUTION)["reviewers"], 1):
        cls = (card_class or {}).get(n) or {
            "claude-sonnet-5-5": "sonnet",
            "claude-haiku-5-5": "haiku",
            "claude-opus-5-5": "opus",
        }[r["model"]]
        (d / "panel/cards" / f"reviewer-{n}.md").write_text(
            f"persona: {['analyzer', 'qa', 'refactorer'][n - 1]}\nmodel_class: {cls}\nmodel: {r['model']}\n\n## Findings block\n"
        )
    (d / "audit.log").write_text(audit)
    return d


def runs_root(tmp_path: Path, shadows: int = 20, legacy: int = 3) -> Path:
    root = tmp_path / "reflect"
    for i in range(legacy):
        legacy_run(root, f"pre-legacy-{i}")
    for i in range(shadows):
        shadow_run(root, f"pre-shadow-{i:02d}")
    return root


def run(root: Path, capsys, *extra) -> tuple[int, str]:
    code = se.main(["--runs-root", str(root), *extra])
    return code, capsys.readouterr().out


# ------------------------------------------------------------ the overall line (AC1)


def test_twenty_clean_runs_pass(tmp_path, capsys):
    code, out = run(runs_root(tmp_path), capsys)
    assert code == 0, out
    assert "OVERALL: PASS (shadow runs 20 of 20)" in out
    assert "MALFORMED audit.log rows: 0" in out
    assert (
        "EV-1 failure rate" in out
        and "n/a" not in out.split("EV-1 failure rate")[1].splitlines()[0]
    )
    assert "cluster_agreement (20 run(s)): min 0.800" in out
    assert "findings-block compliance rate (mean over 20 run(s)): 1.000" in out


def test_one_malformed_run_fails(tmp_path, capsys):
    root = runs_root(tmp_path, shadows=19)
    shadow_run(root, "pre-shadow-19", audit='{"wave": 4, "outcome": "MALFORMED"}\n')
    code, out = run(root, capsys)
    assert code == 1
    assert "MALFORMED audit.log rows: 1" in out and "OVERALL: FAIL" in out
    assert "pre-shadow-19: 1 MALFORMED row(s)" in out


def test_twelve_clean_runs_are_insufficient(tmp_path, capsys):
    code, out = run(runs_root(tmp_path, shadows=12), capsys)
    assert code == 3
    assert "OVERALL: INSUFFICIENT-RUNS (shadow runs 12 of 20)" in out


def test_a_parity_failure_recorded_true_but_recomputed_false_fails(tmp_path, capsys):
    root = runs_root(tmp_path, shadows=19)
    shadow_run(
        root, "pre-shadow-19", card_class={2: "opus"}
    )  # recorded panel_parity stays true
    code, out = run(root, capsys)
    assert code == 1
    assert "pre-shadow-19: FAILS" in out and "recorded true but recomputed false" in out


def test_a_run_frozen_under_another_tier_file_is_not_read_with_todays_mapping(
    tmp_path, capsys
):
    root = runs_root(tmp_path, shadows=19)
    d = shadow_run(root, "pre-shadow-19")
    res = json.loads((d / "panel/resolution.json").read_text())
    res["tiers_sha256"] = "b" * 64
    (d / "panel/resolution.json").write_text(json.dumps(res))
    code, out = run(root, capsys)
    assert code == 1
    assert "pre-shadow-19: FAILS" in out and "tier file hash differs" in out


def test_an_unreadable_manifest_fails_instead_of_vanishing(tmp_path, capsys):
    root = runs_root(tmp_path, shadows=20)
    shadow_run(root, "pre-shadow-20")
    (root / "pre-shadow-20/panel/manifest.json").write_text("{not json")
    code, out = run(root, capsys)
    assert code == 1
    assert "pre-shadow-20 (manifest unreadable)" in out


def test_a_missing_audit_log_is_not_zero_malformed_rows(tmp_path, capsys):
    root = runs_root(tmp_path, shadows=19)
    d = shadow_run(root, "pre-shadow-19")
    (d / "audit.log").unlink()
    code, out = run(root, capsys)
    assert code == 1
    assert "pre-shadow-19: audit.log missing or unreadable" in out


def test_a_legacy_model_that_is_neither_an_id_nor_a_class_is_not_proven(
    tmp_path, capsys
):
    root = runs_root(tmp_path, shadows=19)
    shadow_run(
        root,
        "pre-shadow-19",
        telemetry={"reviewer_models": ["gateway-alias", "haiku", "opus"]},
    )
    code, out = run(root, capsys)
    assert code == 1
    assert "neither a mapped model id nor a class name" in out


def test_a_missing_legacy_rotation_cannot_be_recomputed(tmp_path, capsys):
    root = runs_root(tmp_path, shadows=19)
    shadow_run(root, "pre-shadow-19", telemetry={"reviewer_models": None})
    code, out = run(root, capsys)
    assert code == 1 and "legacy rotation" in out


def test_an_extra_stable_key_fails_through_the_lint(tmp_path, capsys):
    root = runs_root(tmp_path, shadows=19)
    shadow_run(
        root, "pre-shadow-19", cluster_agreement=1.0
    )  # a panel key at the top level
    code, out = run(root, capsys)
    assert code == 1
    assert (
        "top-level key 'cluster_agreement'" in out
        and "pre-shadow-19: lint or manifest problems" in out
    )


def test_ev1_failures_above_the_legacy_rate_fail(tmp_path, capsys):
    root = runs_root(tmp_path, shadows=19)
    bad = shadow_run(root, "pre-shadow-19")
    shutil.rmtree(bad / "adversarial")
    code, out = run(root, capsys)
    assert code == 1
    assert "shadow 1/20 = 0.050; legacy baseline 0/3 = 0.000" in out
    assert "EV-1 failure rate is higher than the legacy baseline" in out


def test_a_new_degraded_reason_in_the_verdict_replay_fails(tmp_path, capsys):
    root = runs_root(tmp_path, shadows=19)
    shadow_run(root, "pre-shadow-19", adversarial_unavailable=True)
    code, out = run(root, capsys)
    assert code == 1
    assert "pre-shadow-19: adversarial-unavailable" in out
    assert "verdict replay found a new degraded reason" in out


# ------------------------------------------------------------ manifests and counts


def test_failed_manifest_fails_and_unfinished_ones_are_not_counted(tmp_path, capsys):
    root = runs_root(tmp_path, shadows=12)
    shadow_run(root, "pre-shadow-f", state="failed")
    shadow_run(root, "pre-shadow-w", state="dispatched")
    code, out = run(root, capsys)
    assert code == 1
    assert "FAILED manifest: pre-shadow-f" in out
    assert "incomplete (not counted): pre-shadow-w (state dispatched)" in out
    assert "shadow runs counted: 12 of 20" in out


def test_stage2_counts(tmp_path, capsys):
    root = runs_root(tmp_path, shadows=18)
    shadow_run(
        root, "pre-shadow-18", complete=2, telemetry={"executor_class_resolved": False}
    )
    shadow_run(root, "pre-shadow-19", complete=2)
    code, out = run(root, capsys)
    assert "2-of-3 shortfalls: 2" in out
    assert "executor_class_resolved false): 1" in out


def test_empty_distributions_print_n_a(tmp_path, capsys):
    root = tmp_path / "reflect"
    shadow_run(
        root,
        "pre-shadow-0",
        telemetry={"cluster_agreement": None, "findings_block_compliance_rate": None},
    )
    code, out = run(root, capsys)
    assert "cluster_agreement: n/a" in out
    assert "findings-block compliance rate (mean over 0 run(s)): n/a" in out


def test_the_required_count_is_an_option(tmp_path, capsys):
    code, out = run(runs_root(tmp_path, shadows=2), capsys, "--required", "2")
    assert code == 0 and "OVERALL: PASS (shadow runs 2 of 2)" in out


# ------------------------------------------------------------ the current repository (AC2)


def test_the_current_repository_reports_without_crashing(capsys):
    """The recorded runs of this checkout (any number of shadow runs, 0 included) give a report and a documented exit."""
    if not (ROOT / ".dev" / "reflect").is_dir():
        pytest.skip("no recorded reflect runs in this checkout")
    code, out = run(ROOT / ".dev" / "reflect", capsys)
    assert code in set(se.EXIT.values())
    assert "Stage 2 shadow-exit report" in out and "of 20 required" in out
    assert out.rstrip().splitlines()[-1].startswith("OVERALL: ")


def test_exit_codes_are_documented():
    assert se.EXIT == {"PASS": 0, "FAIL": 1, "INSUFFICIENT-RUNS": 3}
    assert (
        "Exit codes: 0 PASS, 1 FAIL, 3 INSUFFICIENT-RUNS, 2 usage error" in se.__doc__
    )


def test_a_missing_runs_root_is_a_usage_error(tmp_path):
    assert se.main(["--runs-root", str(tmp_path / "nope")]) == 2


def test_report_file_and_no_other_writes(tmp_path, capsys):
    root = runs_root(tmp_path, shadows=1)
    before = sorted(p.relative_to(root).as_posix() for p in root.rglob("*"))
    out_file = tmp_path / "report.md"
    code, out = run(root, capsys, "--out", str(out_file))
    assert out_file.read_text() == out
    assert sorted(p.relative_to(root).as_posix() for p in root.rglob("*")) == before
