"""Live 7-reviewer panel (1x T1b, 1x T2, 1x T2b, 2x T3, 2x T4) and placeholder tiers (refs #346)."""

from __future__ import annotations

import copy
import json

import pytest
from click.testing import CliRunner

from superclaude.cli.main import main
from superclaude.cli.review import panel as pnl

IDS = ["t1b-1", "t2-1", "t2b-1", "t3-1", "t3-2", "t4-1", "t4-2"]


@pytest.fixture
def tiers():
    return pnl.load_tiers()


@pytest.fixture
def live7():
    return pnl.load_panel("@live7")


def test_live7_is_valid_and_has_seven_reviewers(tiers, live7):
    assert pnl.validate_panel(live7) == []
    assert pnl.validate_panel(live7, tiers) == []
    assert live7["template_id"] == "live7"
    assert sum(s["count"] for s in live7["slots"]) == 7
    assert {s["slot_id"]: s["count"] for s in live7["slots"]} == {
        "t1b": 1,
        "t2": 1,
        "t2b": 1,
        "t3": 2,
        "t4": 2,
    }


def test_default_panel_is_unchanged_by_live7(tiers):
    default = pnl.load_panel()
    assert default["template_id"] == "default"
    assert sum(s["count"] for s in default["slots"]) == 4


def test_anthropic_only_resolves_to_one_sonnet_and_six_haiku(tiers, live7):
    out = pnl.resolve(live7, tiers, "anthropic-only", "run-a")
    assert [r["reviewer_id"] for r in out["reviewers"]] == IDS
    models = [r["model"] for r in out["reviewers"]]
    assert models[0] == "claude-sonnet-5-5"
    assert models[1:] == ["claude-haiku-5-5"] * 6
    assert [r["stand_in"] for r in out["reviewers"]] == [False] + [True] * 6
    assert out["reviewers"][2]["tier"] == "tier2b"
    assert out["reviewers"][2]["alias"] == "claude-gw-tier2b[1m]"


def test_re_review_resolves_only_the_anchor(tiers, live7):
    out = pnl.resolve(live7, tiers, "anthropic-only", "run-a", "re-review")
    assert [r["reviewer_id"] for r in out["reviewers"]] == ["t1b-1"]


def _placeholder_tier2b(tiers):
    t = copy.deepcopy(tiers)
    t["aliases"]["tier2b"] = {
        "alias": "claude-gw-tier2b[1m]",
        "placeholder": True,
        "models": [],
    }
    return t


def test_packaged_tier2b_has_the_owner_supplied_models_in_order(tiers):
    assert tiers["aliases"]["tier2b"] == {
        "alias": "claude-gw-tier2b[1m]",
        "models": ["gpt-6.1-terra", "glm-5.3", "Qwen3.8-max", "muse-wonder-1.0"],
    }
    assert all(m in tiers["names"] for m in tiers["aliases"]["tier2b"]["models"])


def test_gateway_resolves_all_seven_with_the_packaged_tier2b(tiers, live7):
    out = pnl.resolve(live7, tiers, "gateway", "run-a")
    got = {r["reviewer_id"]: r for r in out["reviewers"]}
    assert list(got) == IDS
    assert got["t1b-1"]["model"] == "claude-sonnet-5-5"
    assert got["t2b-1"]["model"] in tiers["aliases"]["tier2b"]["models"]
    assert got["t2b-1"]["alias"] == "claude-gw-tier2b[1m]"
    assert got["t2-1"]["model"] != got["t2b-1"]["model"]
    # Tier 4 lists one model, so both draws are that model: the distinctness rule only
    # applies while another candidate exists.
    assert got["t4-1"]["model"] == got["t4-2"]["model"] == "gpt-6-luna"
    assert all(not r["stand_in"] for r in out["reviewers"])


def test_gateway_fails_closed_for_a_placeholder_tier2b(tiers, live7):
    t = _placeholder_tier2b(tiers)
    assert pnl.validate_tiers(t) == []
    with pytest.raises(pnl.NoModelAvailable) as exc:
        pnl.resolve(live7, t, "gateway", "run-a")
    assert exc.value.tier == "tier2b"
    assert "tier2b" in str(exc.value)
    assert "placeholder" in str(exc.value)


def test_resolution_is_deterministic(tiers, live7):
    a = pnl.resolve(live7, tiers, "anthropic-only", "run-a")
    b = pnl.resolve(live7, tiers, "anthropic-only", "run-a")
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def test_placeholder_tier_rules(tiers):
    base = _placeholder_tier2b(tiers)

    def errs(mutate):
        t = copy.deepcopy(base)
        mutate(t)
        return pnl.validate_tiers(t)

    assert errs(lambda t: None) == []
    assert any(
        "placeholder tier must have an empty models list" in e
        for e in errs(lambda t: t["aliases"]["tier2b"].update(models=["glm-5.3"]))
    )
    assert any(
        "placeholder must be a boolean" in e
        for e in errs(lambda t: t["aliases"]["tier2b"].update(placeholder="yes"))
    )
    # without the flag an empty list is still an error
    assert any(
        "models must be a non-empty list" in e
        for e in errs(lambda t: t["aliases"]["tier2b"].pop("placeholder"))
    )


def test_environment_variable_can_select_a_packaged_panel(monkeypatch):
    monkeypatch.setenv("SUPERCLAUDE_REVIEW_PANEL", "@live7")
    assert pnl.load_panel()["template_id"] == "live7"
    # an explicit argument still wins over the variable
    assert pnl.load_panel("@live7")["template_id"] == "live7"


def test_unknown_or_malformed_packaged_names_are_rejected():
    with pytest.raises(ValueError, match="no packaged panel template 'nope'"):
        pnl.load_panel("@nope")
    with pytest.raises(ValueError, match="invalid packaged panel name"):
        pnl.load_panel("@../x")


def test_cli_resolves_live7_by_name():
    res = CliRunner().invoke(
        main,
        [
            "review",
            "panel",
            "resolve",
            "--template",
            "@live7",
            "--env",
            "anthropic-only",
            "--run-id",
            "x",
        ],
    )
    assert res.exit_code == 0, res.output
    data = json.loads(res.output)
    assert data["template_id"] == "live7"
    assert [r["reviewer_id"] for r in data["reviewers"]] == IDS


def test_cli_gateway_live7_resolves_seven_reviewers():
    res = CliRunner().invoke(
        main,
        [
            "review",
            "panel",
            "resolve",
            "--template",
            "@live7",
            "--env",
            "gateway",
            "--run-id",
            "x",
        ],
    )
    assert res.exit_code == 0, res.output
    data = json.loads(res.output)
    assert [r["reviewer_id"] for r in data["reviewers"]] == IDS
    assert data["reviewers"][2]["alias"] == "claude-gw-tier2b[1m]"


def test_cli_gateway_live7_fails_closed_with_a_placeholder_tier_file(tmp_path, tiers):
    f = tmp_path / "tiers.json"
    f.write_text(json.dumps(_placeholder_tier2b(tiers)))
    res = CliRunner().invoke(
        main,
        [
            "review",
            "panel",
            "resolve",
            "--template",
            "@live7",
            "--tiers",
            str(f),
            "--env",
            "gateway",
            "--run-id",
            "x",
        ],
    )
    assert res.exit_code != 0
    assert "tier2b" in res.output
