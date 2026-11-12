"""Panel contract lint (lint_panel_contract): pass cases P1-P10 and fail cases F1-F20 of the lint design."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
import yaml

from superclaude.cli.reflect import panel_lint as pl
from superclaude.cli.reflect.contract import _LOAD_BEARING_BOOL_FIELDS

LEGACY = Path(__file__).parent / "fixtures" / "panel_lint_legacy"
SKILL = (
    Path(__file__).resolve().parents[3]
    / "src/superclaude/skills/sc-reflect-protocol/SKILL.md"
)
LEGACY_CONTRACT = yaml.safe_load((LEGACY / "return-contract.yaml").read_text())


def make(
    tmp_path,
    *,
    mutate=None,
    manifest=None,
    panel_file=False,
    no_adv=False,
    mv_merge=None,
    audit=None,
    drop_cards=(),
    raw=None,
    name="run",
):
    """Copy the legacy fixture to tmp_path/name and apply the variant; returns the run directory."""
    dst = tmp_path / name
    shutil.copytree(LEGACY, dst)
    contract = yaml.safe_load((LEGACY / "return-contract.yaml").read_text())
    if mutate:
        mutate(contract)
    text = raw if raw is not None else yaml.safe_dump(contract, sort_keys=False)
    (dst / "return-contract.yaml").write_text(text)
    if manifest is not None:
        (dst / "panel").mkdir()
        (dst / "panel/manifest.json").write_text(json.dumps(manifest))
    if panel_file:
        (dst / "panel").mkdir(exist_ok=True)
        (dst / "panel/resolution.json").write_text("{}")
    if no_adv:
        shutil.rmtree(dst / "adversarial")
    if mv_merge:
        (dst / "adversarial/merged-verdict.yaml").write_text(
            f"merge_method: {mv_merge}\n"
        )
    if audit is not None:
        (dst / "audit.log").write_text(audit)
    for n in drop_cards:
        (dst / f"reviewer-cards/reviewer-{n}-card.yaml").unlink()
    return dst


def own(run):
    return yaml.safe_load((run / "return-contract.yaml").read_text())


def bump(n, m):
    return (
        f"B bump rule: the contract leaves 1.8.0 ({n} stable-key violation(s), {m} EV-2 value violation(s)); "
        "a new stable key or merge_method value needs a contract version bump, which this plan does not make"
    )


def no_fallback_set(c):
    c["adversarial_unavailable"] = True
    c["merge_method"] = "single-reviewer-fallback"


FALLBACK_AUDIT = '{"wave":5,"step":"5.0","outcome":"F2"}\n'
NO_VERDICT_MISSING = (
    "L6 EV-1: neither a merged adversarial verdict nor a loud fallback is on disk "
    "(merged-verdict: {mv}; fallback missing: {missing})"
)
ALL_MISSING = "adversarial_unavailable: true, merge_method: single-reviewer-fallback, audit.log F2/F3 row"


# ------------------------------------------------------------ constants


@pytest.mark.parametrize(
    "heading, constant",
    [
        ("### 9.1 Stable contract (contract_version: 1.8.0)", pl.STABLE_FIELDS_1_8_0),
        ("### 9.2 Telemetry (non-stable)", pl.TELEMETRY_FIELDS),
    ],
)
def test_pinned_field_lists_match_skill_md(heading, constant):
    live = pl.extract_field_list(SKILL.read_text(encoding="utf-8"), heading)
    added, removed = (
        sorted(set(live) - set(constant)),
        sorted(set(constant) - set(live)),
    )
    assert not added and not removed, f"SKILL.md added {added}, removed {removed}"
    assert list(constant) == live


def test_constant_sizes_and_load_bearing_import():
    # 26 telemetry names of the original section 9.2 plus the `telemetry` block that Task 19 added to it
    assert len(pl.STABLE_FIELDS_1_8_0) == 110 and len(pl.TELEMETRY_FIELDS) == 27
    assert pl.LOAD_BEARING_BOOLS is _LOAD_BEARING_BOOL_FIELDS
    assert (
        "citations_dropped_extrapolated" in pl.STABLE_FIELDS_1_8_0
        and "citations_dropped_extrapolated" in pl.TELEMETRY_FIELDS
    )


# ------------------------------------------------------------ pass cases


def test_p1_legacy_fixture_passes():
    assert pl.lint_panel_contract(LEGACY, LEGACY_CONTRACT) == []


def test_p2_panel_directory_with_manifest_passes(tmp_path):
    run = make(tmp_path, manifest={"reviewers_resolved": 3}, panel_file=True)
    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == []


def test_p3_no_manifest_takes_the_count_from_reviewer_cards(tmp_path):
    run = make(tmp_path)
    assert not (run / "panel").exists()
    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == []


@pytest.mark.parametrize(
    "mutate",
    [
        lambda c: c.setdefault("telemetry", {}).update(panel_engine="shadow"),
        lambda c: c.update(degraded_components=[]),
        lambda c: c.update(verification_ran=None),
        lambda c: c.update(adversarial_convergence_score=None),
        lambda c: c.update(
            reviewer_cards=[f"/elsewhere/{Path(p).name}" for p in c["reviewer_cards"]]
        ),
    ],
    ids=[
        "p4-telemetry-keys",
        "p5-telemetry-name-top-level",
        "p6-verification-null",
        "p7-score-null",
        "p10-cards-moved",
    ],
)
def test_other_pass_variants(tmp_path, mutate):
    run = make(tmp_path, mutate=mutate)
    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == []


def test_p8_loud_fallback_passes(tmp_path):
    run = make(tmp_path, mutate=no_fallback_set, no_adv=True, audit=FALLBACK_AUDIT)
    assert pl.lint_panel_contract(run, own(run)) == []


def test_p9_tier_one_passes(tmp_path):
    def t1(c):
        c["tier_reached"] = 1
        c["merge_method"] = None

    run = make(tmp_path, mutate=t1, no_adv=True)
    assert pl.lint_panel_contract(run, own(run)) == []


# ------------------------------------------------------------ fail cases


def test_f1_extra_stable_key_is_named(tmp_path):
    run = make(tmp_path, mutate=lambda c: c.update(cluster_agreement=1.0))
    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == [
        "L2 stable keys: top-level key 'cluster_agreement' is not in the 1.8.0 stable field list or the telemetry block",
        bump(1, 0),
    ]


def test_f2_merge_method_panel_fails(tmp_path):
    # merge_method is not a parity field, so only L3 and B appear
    run = make(tmp_path, mutate=lambda c: c.update(merge_method="panel"))
    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == [
        "L3 merge_method: 'panel' is not a legal 1.8.0 value (EV-2: 'adversarial' or 'single-reviewer-fallback')",
        bump(0, 1),
    ]


def test_f3_f4_contract_version(tmp_path):
    run = make(tmp_path, mutate=lambda c: c.update(contract_version="1.9.0"))
    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == [
        "L1 contract_version: expected '1.8.0', got '1.9.0'"
    ]
    run = make(tmp_path, mutate=lambda c: c.pop("contract_version"), name="run2")
    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == [
        "L1 contract_version: expected '1.8.0', got None"
    ]


def test_f5_unusable_contract_gives_only_l0(tmp_path):
    run = make(tmp_path, raw="- a list\n")
    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == [
        "L0 contract: return-contract.yaml is missing, unparseable or not a mapping"
    ]
    (run / "return-contract.yaml").unlink()
    assert len(pl.lint_panel_contract(run, LEGACY_CONTRACT)) == 1


def test_non_utf8_files_do_not_crash_the_lint(tmp_path):
    run = make(tmp_path)
    (run / "return-contract.yaml").write_bytes(b"contract_version: \xff\xfe\n")
    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == [
        "L0 contract: return-contract.yaml is missing, unparseable or not a mapping"
    ]
    # a non-UTF-8 merged verdict counts as unparseable; a non-UTF-8 audit.log has no F2/F3 row
    run = make(tmp_path, mutate=no_fallback_set, no_adv=True, name="run2")
    (run / "audit.log").write_bytes(b"\xff\xfe F2\n")
    assert pl.lint_panel_contract(run, own(run)) == [
        NO_VERDICT_MISSING.format(mv="absent", missing="audit.log F2/F3 row")
    ]
    run = make(tmp_path, name="run3")
    (run / "adversarial/merged-verdict.yaml").write_bytes(b"\xff\xfe\n")
    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == [
        NO_VERDICT_MISSING.format(mv="unparseable", missing=ALL_MISSING)
    ]


def test_f6_telemetry_must_be_a_mapping(tmp_path):
    run = make(tmp_path, mutate=lambda c: c.update(telemetry=[1]))
    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == [
        "L2 stable keys: 'telemetry' must be a mapping, got list"
    ]


@pytest.mark.parametrize("value, shown", [("0.852", "'0.852'"), (1, "1")])
def test_f7_f8_convergence_score_type(tmp_path, value, shown):
    run = make(tmp_path, mutate=lambda c: c.update(adversarial_convergence_score=value))
    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == [
        f"L4 adversarial_convergence_score: expected a float or null, got {shown}"
    ]


@pytest.mark.parametrize(
    "mutate, line",
    [
        (
            lambda c: c.update(regression_present="false"),
            "L5 regression_present: expected a real boolean, got 'false'",
        ),
        (
            lambda c: c.pop("adversarial_unavailable"),
            "L5 adversarial_unavailable: expected a real boolean, got None",
        ),
        (
            lambda c: c.update(verification_ran=1),
            "L5 verification_ran: expected a real boolean, got 1",
        ),
    ],
    ids=["f9", "f10", "f11"],
)
def test_f9_f10_f11_booleans(tmp_path, mutate, line):
    run = make(tmp_path, mutate=mutate)
    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == [line]


def test_f12_manifest_requires_more_cards_than_held(tmp_path):
    run = make(tmp_path, manifest={"reviewers_resolved": 4}, panel_file=True)
    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == [
        "L6 EV-1: reviewer-cards/ holds 3 card(s), fewer than the required 4 (reviewers_resolved from panel/manifest.json)"
    ]


def test_f13_without_manifest_a_missing_card_fails(tmp_path):
    run = make(tmp_path, drop_cards=(3,))
    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == [
        "L6 EV-1: reviewer-cards/ holds 2 card(s), fewer than the required 3 (len(reviewer_cards))"
    ]


def test_f14_minimum_two_cards(tmp_path):
    run = make(
        tmp_path, mutate=lambda c: c.update(reviewer_cards=[]), drop_cards=(2, 3)
    )
    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == [
        "L6 EV-1: reviewer-cards/ holds 1 card(s), fewer than the required 2 (minimum 2)",
        "L7 parity reviewer_cards: panel [] differs from matched legacy "
        "['reviewer-1-card.yaml', 'reviewer-2-card.yaml', 'reviewer-3-card.yaml']",
    ]


def test_f15_manifest_with_a_string_count(tmp_path):
    run = make(tmp_path, manifest={"reviewers_resolved": "3"}, panel_file=True)
    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == [
        "L6 EV-1: panel/manifest.json is not a JSON object with a positive integer reviewers_resolved"
    ]


def test_manifest_without_the_key_uses_reviewer_cards(tmp_path):
    run = make(tmp_path, manifest={"other": 1})
    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == []
    run = make(tmp_path, manifest=["not", "an", "object"], name="run2")
    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == [
        "L6 EV-1: panel/manifest.json is not a JSON object with a positive integer reviewers_resolved"
    ]


def test_ev1_with_and_without_a_manifest_agree_on_the_same_cards(tmp_path):
    with_manifest = make(tmp_path, manifest={"reviewers_resolved": 3}, panel_file=True)
    without = make(tmp_path, name="run2")
    assert (
        pl.lint_panel_contract(with_manifest, LEGACY_CONTRACT)
        == pl.lint_panel_contract(without, LEGACY_CONTRACT)
        == []
    )


def test_f16_no_verdict_and_no_fallback(tmp_path):
    run = make(tmp_path, no_adv=True)
    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == [
        NO_VERDICT_MISSING.format(mv="absent", missing=ALL_MISSING)
    ]


def test_f17_fallback_without_audit_row(tmp_path):
    run = make(tmp_path, mutate=no_fallback_set, no_adv=True)
    assert pl.lint_panel_contract(run, own(run)) == [
        NO_VERDICT_MISSING.format(mv="absent", missing="audit.log F2/F3 row")
    ]


def test_f18_merged_verdict_with_the_fallback_method_is_not_enough(tmp_path):
    run = make(tmp_path, mv_merge="single-reviewer-fallback")
    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == [
        NO_VERDICT_MISSING.format(
            mv="merge_method 'single-reviewer-fallback'", missing=ALL_MISSING
        )
    ]


def test_unparseable_merged_verdict_is_reported(tmp_path):
    run = make(tmp_path)
    (run / "adversarial/merged-verdict.yaml").write_text("key: [unclosed\n")
    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == [
        NO_VERDICT_MISSING.format(mv="unparseable", missing=ALL_MISSING)
    ]


@pytest.mark.parametrize(
    "field, value, legacy",
    [
        ("t2_vendor_diversity", "single", "multi"),
        ("calibrator_diversity", "full", "degraded"),
    ],
)
def test_f19_f20_parity(tmp_path, field, value, legacy):
    run = make(tmp_path, mutate=lambda c: c.update({field: value}))
    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == [
        f"L7 parity {field}: panel {value!r} differs from matched legacy {legacy!r}"
    ]


def test_lint_does_not_write(tmp_path):
    run = make(tmp_path, manifest={"reviewers_resolved": 3})
    before = sorted(str(p.relative_to(run)) for p in run.rglob("*"))
    pl.lint_panel_contract(run, LEGACY_CONTRACT)
    assert sorted(str(p.relative_to(run)) for p in run.rglob("*")) == before


def test_ev1_reads_reviewers_resolved_from_a_manifest_written_by_the_manifest_module(
    tmp_path,
):
    """Task 17's manifest carries reviewers_resolved as a top-level key; the lint takes the required count from it."""
    from superclaude.cli.review import manifest as mf

    h = "a" * 64
    frozen = {
        "snapshot_ref": "artifacts/input-snapshot.yaml",
        "snapshot_sha256": h,
        "input_tree_sha256": h,
        "template_sha256": h,
        "tiers_sha256": h,
        "brief_template_sha256": h,
        "schema_ids": ["review-panel/1"],
    }
    for resolved, expected in ((3, []), (4, 1)):
        m = mf.new_manifest(
            run_id="r1",
            frozen=frozen,
            engine_requested="shadow",
            engine_effective="shadow",
        )
        mf.advance_stage(
            m,
            "resolved",
            {"reviewers_requested": resolved, "reviewers_resolved": resolved},
        )
        run = make(tmp_path, name=f"run{resolved}")
        mf.save(run / "panel" / "manifest.json", m)
        lines = pl.lint_panel_contract(run, LEGACY_CONTRACT)
        if expected == []:
            assert lines == []
        else:
            assert lines == [
                "L6 EV-1: reviewer-cards/ holds 3 card(s), fewer than the required 4 (reviewers_resolved from panel/manifest.json)"
            ]
