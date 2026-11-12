"""K1 hard exclusion and strict distinctness in panel resolution (reflect Tier 2 panel, Stage 1).

The byte-identity golden is taken with a FROZEN copy of review-tiers.default.json
(fixtures/review-tiers.frozen-1.0.0.json). The packaged tier file will gain a `classes` object, which
changes `tiers_sha256`; the frozen copy keeps this golden valid after that change.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from superclaude.cli.review import panel as pnl

FIX = Path(__file__).parent / "fixtures"
SONNET, OPUS, HAIKU = "claude-sonnet-5-5", "claude-opus-5-5", "claude-haiku-5-5"


@pytest.fixture(scope="module")
def frozen_tiers():
    return json.loads((FIX / "review-tiers.frozen-1.0.0.json").read_text())


def _panel(slots, distinct=True):
    return {
        "schema": pnl.PANEL_SCHEMA,
        "template_id": "kernel-test",
        "version": "1.0.0",
        "distinct_across_slots": distinct,
        "apply_to": ["first"],
        "slots": slots,
    }


REFLECT_PRE = _panel(
    [
        {"slot_id": "t1b", "tier": "tier1b", "count": 1, "strategy": "fixed"},
        {"slot_id": "t4", "tier": "tier4", "count": 1, "strategy": "random"},
        {"slot_id": "t1a", "tier": "tier1a", "count": 1, "strategy": "random"},
    ]
)


def _models(res):
    return [r["model"] for r in res["reviewers"]]


# ------------------------------------------------------------ byte identity (AC1)


GOLDEN = json.loads((FIX / "panel-golden-default-live7.json").read_text())


@pytest.mark.parametrize("key", sorted(GOLDEN))
@pytest.mark.parametrize("explicit", [False, True])
def test_no_exclusion_is_byte_identical_to_golden(frozen_tiers, key, explicit):
    name, env, kind = key.split("|")
    extra = {"hard_exclude": (), "strict_distinct": False} if explicit else {}
    res = pnl.resolve(
        pnl.packaged_panel(name),
        frozen_tiers,
        env,
        "golden-run",
        kind,
        None,
        100,
        **extra,
    )
    assert json.dumps(res, sort_keys=True, separators=(",", ":")) == GOLDEN[key]
    assert "skipped_slots" not in res and "excluded" not in res


# ------------------------------------------------------------ resolve_slot (AC2)


def test_excluded_model_is_the_fixed_anchor(frozen_tiers):
    models = frozen_tiers["aliases"]["tier1b"]["models"]
    assert pnl.resolve_slot(models, "fixed", None, "all", [])["model"] == SONNET
    out = pnl.resolve_slot(models, "fixed", None, "all", [], hard_exclude=[SONNET])
    assert out["model"] == models[1]
    assert SONNET not in out["fallbacks"]


def test_fixed_anchor_with_only_the_excluded_model_is_exhausted(frozen_tiers):
    models = frozen_tiers["aliases"]["tier1b"]["models"]
    with pytest.raises(pnl.ExclusionExhausted):
        pnl.resolve_slot(
            models, "fixed", None, [SONNET, OPUS], [], hard_exclude=[SONNET]
        )


@pytest.mark.parametrize("strategy", ["random", "round_robin"])
def test_emptied_pool_does_not_readmit_the_excluded_model(strategy):
    # soft exclusion alone: today's behaviour re-admits the only candidate
    soft = pnl.resolve_slot(["a"], strategy, 3, "all", [], ["a"])
    assert soft["model"] == "a"
    # with a hard exclusion the pool is never refilled
    with pytest.raises(pnl.ExclusionExhausted):
        pnl.resolve_slot(["a", "b"], strategy, 3, "all", [], ["a"], hard_exclude=["b"])
    with pytest.raises(pnl.ExclusionExhausted):
        pnl.resolve_slot(["a"], strategy, 3, "all", [], hard_exclude=["a"])


@pytest.mark.parametrize("strategy", ["fixed", "random", "round_robin"])
def test_no_primary_or_fallback_is_an_excluded_model(strategy):
    for seed in range(6):
        out = pnl.resolve_slot(
            ["a", "b", "c"], strategy, seed, "all", [], hard_exclude=["b"]
        )
        assert out["model"] != "b" and "b" not in out["fallbacks"]


def test_strict_distinct_removes_models_already_chosen():
    out = pnl.resolve_slot(
        ["a", "b"], "random", 1, "all", [], ["a"], strict_distinct=True
    )
    assert out["model"] == "b"
    with pytest.raises(pnl.ExclusionExhausted):
        pnl.resolve_slot(["a"], "fixed", None, "all", [], ["a"], strict_distinct=True)


def test_stand_in_is_used_only_after_filtering():
    # a candidate survives the filter: the stand-in stays unused
    out = pnl.resolve_slot(["a", "b"], "fixed", None, "all", ["s"], hard_exclude=["a"])
    assert (out["model"], out["stand_in"]) == ("b", False)
    # nothing available from the models: the stand-in is used
    out = pnl.resolve_slot(["a", "b"], "fixed", None, ["s"], ["s"], hard_exclude=["a"])
    assert (out["model"], out["stand_in"]) == ("s", True)
    # filtering empties the models: the stand-in is tried, filtered the same way
    out = pnl.resolve_slot(["a"], "fixed", None, ["a", "s"], ["s"], hard_exclude=["a"])
    assert (out["model"], out["stand_in"]) == ("s", True)
    with pytest.raises(pnl.ExclusionExhausted):
        pnl.resolve_slot(
            ["a"], "fixed", None, ["a", "s"], ["s"], hard_exclude=["a", "s"]
        )


def test_exhaustion_is_a_no_model_available_but_only_when_exclusion_caused_it():
    assert issubclass(pnl.ExclusionExhausted, pnl.NoModelAvailable)
    with pytest.raises(pnl.ExclusionExhausted):
        pnl.resolve_slot(["a"], "fixed", None, "all", [], hard_exclude=["a"])
    with pytest.raises(pnl.NoModelAvailable) as err:
        pnl.resolve_slot(["a"], "fixed", None, ["z"], [], hard_exclude=["a"])
    assert not isinstance(err.value, pnl.ExclusionExhausted)


# ------------------------------------------------------------ resolve (scenarios of the contract)


def test_executor_sonnet_makes_the_anchor_fatal(frozen_tiers):
    with pytest.raises(pnl.ExclusionExhausted) as err:
        pnl.resolve(
            REFLECT_PRE,
            frozen_tiers,
            "anthropic-only",
            "r1",
            hard_exclude=[SONNET],
            strict_distinct=True,
        )
    assert err.value.tier == "tier1b" and type(err.value) is pnl.ExclusionExhausted


def test_executor_haiku_skips_the_t4_slot(frozen_tiers):
    res = pnl.resolve(
        REFLECT_PRE,
        frozen_tiers,
        "anthropic-only",
        "r1",
        hard_exclude=[HAIKU],
        strict_distinct=True,
    )
    assert _models(res) == [SONNET, OPUS]
    assert [s["slot_id"] for s in res["skipped_slots"]] == ["t4"]
    assert res["excluded"] == {"models": [HAIKU], "classes": []}


def test_executor_opus_with_strict_distinctness_has_no_duplicate(frozen_tiers):
    res = pnl.resolve(
        REFLECT_PRE,
        frozen_tiers,
        "anthropic-only",
        "r1",
        hard_exclude=[OPUS],
        strict_distinct=True,
    )
    assert _models(res) == [SONNET, HAIKU]
    assert len(set(_models(res))) == len(_models(res))
    assert [s["slot_id"] for s in res["skipped_slots"]] == ["t1a"]


def test_strict_distinct_alone_records_the_additive_keys(frozen_tiers):
    res = pnl.resolve(
        REFLECT_PRE, frozen_tiers, "anthropic-only", "r1", strict_distinct=True
    )
    assert len(set(_models(res))) == len(res["reviewers"])
    assert res["excluded"] == {"models": [], "classes": []}
    assert "skipped_slots" in res


def test_excluded_classes_come_from_the_class_map_when_present(frozen_tiers):
    tiers = {**frozen_tiers, "classes": {HAIKU: "haiku", OPUS: "opus"}}
    res = pnl.resolve(REFLECT_PRE, tiers, "anthropic-only", "r1", hard_exclude=[HAIKU])
    assert res["excluded"] == {"models": [HAIKU], "classes": ["haiku"]}


def test_soft_distinct_without_exclusion_still_repeats_a_model(frozen_tiers):
    # live7 in anthropic-only is 1 Sonnet + 6 Haiku today: soft distinctness re-admits Haiku
    res = pnl.resolve(
        pnl.packaged_panel("live7"), frozen_tiers, "anthropic-only", "r1", "first"
    )
    assert _models(res).count(HAIKU) == 6
