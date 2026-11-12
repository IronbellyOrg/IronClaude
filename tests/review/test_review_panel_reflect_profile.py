"""Class map and reflect profile of panel templates (reflect Tier 2 panel, Stage 1).

Task 9 added a `classes` object to the packaged review-tiers.default.json, so `tiers_sha256` of every
resolution made from the PACKAGED tier file changed BY DESIGN. That new value is pinned here
(fixtures/panel-golden-packaged-tiers.json), next to the Task 8 golden taken with the FROZEN tier file
(fixtures/panel-golden-default-live7.json), which is unchanged.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.review import panel as pnl
from superclaude.cli.review import panel_cmd

FIX = Path(__file__).parent / "fixtures"
SONNET, OPUS, HAIKU, FABLE = (
    "claude-sonnet-5-5",
    "claude-opus-5-5",
    "claude-haiku-5-5",
    "claude-fable-5-1",
)


@pytest.fixture
def tiers():
    return pnl.load_tiers()


def _panel(slots, tid="reflect-test", distinct=True):
    return {
        "schema": pnl.PANEL_SCHEMA,
        "template_id": tid,
        "version": "1.0.0",
        "distinct_across_slots": distinct,
        "apply_to": ["first"],
        "slots": slots,
    }


def _slot(sid, tier, strategy="random", count=1):
    return {"slot_id": sid, "tier": tier, "count": count, "strategy": strategy}


PRE = [_slot("t1b", "tier1b", "fixed"), _slot("t4", "tier4"), _slot("t1a", "tier1a")]


# ------------------------------------------------------------ packaged class map and golden


def test_packaged_tiers_validate_and_map_every_model(tiers):
    assert pnl.validate_tiers(tiers) == []
    ids = set(tiers["names"])
    for entry in tiers["aliases"].values():
        ids.update(entry["models"])
    for env in tiers["environments"].values():
        if isinstance(env["available"], list):
            ids.update(env["available"])
        for lst in env["stand_ins"].values():
            ids.update(lst)
    assert ids <= set(tiers["classes"])
    assert tiers["classes"][OPUS] == "opus"
    assert tiers["classes"][SONNET] == "sonnet"
    assert tiers["classes"][HAIKU] == "haiku"
    assert tiers["classes"][FABLE] == "fable"
    assert {tiers["classes"][m] for m in ids} >= {"gpt", "glm", "grok", "qwen", "muse"}


def test_packaged_tiers_hash_and_resolutions_are_pinned(tiers):
    golden = json.loads((FIX / "panel-golden-packaged-tiers.json").read_text())
    assert pnl.sha256_json(tiers) == golden["tiers_sha256"]
    for name in ("default", "live7"):
        res = pnl.resolve(
            pnl.packaged_panel(name),
            tiers,
            "anthropic-only",
            "golden-run",
            "first",
            None,
            100,
        )
        key = f"{name}|anthropic-only|first"
        assert json.dumps(res, sort_keys=True, separators=(",", ":")) == golden[key]
    frozen = json.loads((FIX / "review-tiers.frozen-1.0.0.json").read_text())
    assert pnl.sha256_json(frozen) != golden["tiers_sha256"]  # changed by design


@pytest.mark.parametrize(
    "classes",
    [[], {"claude-opus-5-5": 3}, {"claude-opus-5-5": "Opus"}, {"bad id": "opus"}],
)
def test_validate_tiers_rejects_a_malformed_class_map(tiers, classes):
    bad = {**tiers, "classes": classes}
    assert any("classes" in e for e in pnl.validate_tiers(bad))


# ------------------------------------------------------------ the reflect profile


def test_valid_reflect_template_passes(tiers):
    assert pnl.validate_panel(_panel(PRE), tiers) == []


def test_unmapped_model_invalidates_reflect_but_not_generic(tiers):
    bad = copy.deepcopy(tiers)
    del bad["classes"][SONNET]
    errors = pnl.validate_panel(_panel(PRE), bad)
    assert any(SONNET in e and "classes" in e for e in errors)
    assert pnl.validate_panel(_panel(PRE, tid="generic"), bad) == []
    assert (
        pnl.validate_panel(_panel(PRE)) == []
    )  # no tier file supplied: profile not run


def test_fable_is_rejected_by_name_and_by_absence(tiers):
    for drop_class in (False, True):
        bad = copy.deepcopy(tiers)
        bad["aliases"]["tier4"]["models"].append(FABLE)
        if drop_class:
            del bad["classes"][FABLE]
        errors = pnl.validate_panel(_panel(PRE), bad)
        assert any(FABLE in e and "Fable" in e for e in errors), errors
        assert pnl.validate_panel(_panel(PRE, tid="generic"), bad) == []


def test_tier0_slot_or_tier0_model_is_rejected(tiers):
    bad = copy.deepcopy(tiers)
    bad["aliases"]["tier0"] = {
        "alias": "claude-gw-tier0[1m]",
        "models": ["gpt-6.1-sol"],
    }
    on_tier0 = _panel([_slot("t1b", "tier1b", "fixed"), _slot("t0", "tier0")])
    assert any("tier0" in e for e in pnl.validate_panel(on_tier0, bad))
    # tier2 lists gpt-6.1-sol, which this file also lists in tier0
    holds = _panel([_slot("t1b", "tier1b", "fixed"), _slot("t2", "tier2")])
    assert any("Tier 0 model" in e for e in pnl.validate_panel(holds, bad))


def test_more_than_three_reviewers_is_rejected_only_for_reflect(tiers):
    four = [_slot("t1b", "tier1b", "fixed"), _slot("t4", "tier4", count=3)]
    assert any("at most 3" in e for e in pnl.validate_panel(_panel(four), tiers))
    assert pnl.validate_panel(_panel(four, tid="generic"), tiers) == []
    three = [_slot("t1b", "tier1b", "fixed"), _slot("t4", "tier4", count=2)]
    assert pnl.validate_panel(_panel(three), tiers) == []


def test_round_robin_needs_a_recorded_sequence(tiers):
    rr = _panel([_slot("t1b", "tier1b", "fixed"), _slot("rr", "tier1a", "round_robin")])
    assert any("--sequence" in e for e in pnl.validate_panel(rr, tiers))
    assert pnl.validate_panel(rr, tiers, sequence=4) == []
    generic = _panel(rr["slots"], tid="generic")
    assert pnl.validate_panel(generic, tiers) == []


# ------------------------------------------------------------ resolve re-checks


def test_resolve_applies_the_profile(tiers):
    res = pnl.resolve(_panel(PRE), tiers, "anthropic-only", "r1")
    assert [r["model"] for r in res["reviewers"]][0] == SONNET
    bad = copy.deepcopy(tiers)
    del bad["classes"][OPUS]
    with pytest.raises(ValueError, match="classes"):
        pnl.resolve(_panel(PRE), bad, "anthropic-only", "r1")
    with pytest.raises(ValueError, match="at most 3"):
        pnl.resolve(
            _panel([_slot("t1b", "tier1b", "fixed"), _slot("t4", "tier4", count=3)]),
            tiers,
            "anthropic-only",
            "r1",
        )
    rr = _panel([_slot("t1b", "tier1b", "fixed"), _slot("rr", "tier1a", "round_robin")])
    with pytest.raises(ValueError, match="--sequence"):
        pnl.resolve(rr, tiers, "anthropic-only", "r1")
    assert pnl.resolve(rr, tiers, "anthropic-only", "r1", sequence=2)["reviewers"]


def test_resolve_rejects_a_launch_value_outside_the_allowed_set(tiers):
    bad = copy.deepcopy(tiers)
    bad["environments"]["anthropic-only"]["launch"][SONNET] = "fable"
    with pytest.raises(ValueError, match="launch"):
        pnl.resolve(_panel(PRE), bad, "anthropic-only", "r1")
    # a generic panel resolves the same file without the profile
    assert pnl.resolve(_panel(PRE, tid="generic"), bad, "anthropic-only", "r1")


def test_resolve_rejects_a_resolved_fable_id(tiers):
    bad = copy.deepcopy(tiers)
    bad["aliases"]["tier1b"]["models"] = [FABLE]
    with pytest.raises(ValueError, match="Fable"):
        pnl.resolve(_panel(PRE), bad, "anthropic-only", "r1")


def test_generic_panel_with_four_reviewers_stays_valid(tiers):
    generic = _panel(
        [_slot("t1b", "tier1b", "fixed"), _slot("t4", "tier4", count=3)], tid="generic"
    )
    assert pnl.validate_panel(generic, tiers) == []
    assert len(pnl.resolve(generic, tiers, "anthropic-only", "r1")["reviewers"]) == 4


# ------------------------------------------------------------ CLI passes --sequence to the rule


def test_resolve_cmd_passes_sequence_into_the_round_robin_rule(tmp_path):
    tpl = _panel(
        [_slot("t1b", "tier1b", "fixed"), _slot("rr", "tier1a", "round_robin")]
    )
    path = tmp_path / "reflect-rr.json"
    path.write_text(json.dumps(tpl))
    base = [
        "resolve",
        "--template",
        str(path),
        "--run-id",
        "r1",
        "--env",
        "anthropic-only",
    ]
    runner = CliRunner()
    missing = runner.invoke(panel_cmd.command, base)
    assert missing.exit_code != 0 and "--sequence" in missing.output
    ok = runner.invoke(panel_cmd.command, [*base, "--sequence", "2"])
    assert ok.exit_code == 0, ok.output
    assert len(json.loads(ok.output)["reviewers"]) == 2
