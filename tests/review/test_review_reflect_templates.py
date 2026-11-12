"""The packaged reflect panel templates and the K1 hard exclusion scenarios (contract item 8)."""

from __future__ import annotations

import json

import pytest
from click.testing import CliRunner

from superclaude.cli.main import main
from superclaude.cli.review import panel as pnl

SONNET, OPUS, HAIKU = "claude-sonnet-5-5", "claude-opus-5-5", "claude-haiku-5-5"
NAMES = [
    "reflect-pre",
    "reflect-pre-x2",
    "reflect-enterprise",
    "reflect-lite",
    "reflect-post",
    "reflect-post-x2",
]
ENV = "anthropic-only"


@pytest.fixture(scope="module")
def tiers():
    return pnl.load_tiers()


def _res(tiers, name, *, executor=None, strict=False, kind="first"):
    hard = [m for m, c in tiers["classes"].items() if c == executor] if executor else []
    return pnl.resolve(
        pnl.packaged_panel(name),
        tiers,
        ENV,
        "r1",
        kind,
        hard_exclude=hard,
        strict_distinct=strict,
    )


def _models(res):
    return [r["model"] for r in res["reviewers"]]


@pytest.mark.parametrize("name", NAMES)
def test_template_is_valid_and_has_one_fixed_slot(tiers, name):
    panel = pnl.packaged_panel(name)
    assert panel["template_id"] == name
    assert pnl.validate_panel(panel, tiers, sequence=1) == []
    assert [s["strategy"] for s in panel["slots"]].count("fixed") == 1
    assert not {s["tier"] for s in panel["slots"]} & {"tier0"}
    assert pnl.load_panel(f"@{name}") == panel


def test_template_slots_match_the_design():
    def slots(name):
        return [
            (s["slot_id"], s["tier"], s["strategy"])
            for s in pnl.packaged_panel(name)["slots"]
        ]

    pre = [
        ("t1b", "tier1b", "fixed"),
        ("t4", "tier4", "random"),
        ("t1a", "tier1a", "random"),
    ]
    x2 = [("t4", "tier4", "fixed"), ("t1a", "tier1a", "random")]
    lite = [
        ("t1b", "tier1b", "fixed"),
        ("t4", "tier4", "random"),
        ("t2", "tier2", "random"),
    ]
    assert (
        slots("reflect-pre")
        == slots("reflect-enterprise")
        == slots("reflect-post")
        == pre
    )
    assert slots("reflect-pre-x2") == slots("reflect-post-x2") == x2
    assert slots("reflect-lite") == lite
    for name in NAMES:
        panel = pnl.packaged_panel(name)
        assert panel["distinct_across_slots"] is True and panel["apply_to"] == ["first"]


@pytest.mark.parametrize("name", ["reflect-pre", "reflect-enterprise", "reflect-post"])
@pytest.mark.parametrize("strict", [False, True])
def test_pre_resolves_to_sonnet_haiku_opus_with_three_classes(tiers, name, strict):
    res = _res(tiers, name, strict=strict)
    assert _models(res) == [SONNET, HAIKU, OPUS]
    assert len({tiers["classes"][m] for m in _models(res)}) == 3


def test_pre_x2_resolves_to_haiku_and_opus_when_the_executor_is_sonnet(tiers):
    for name in ("reflect-pre-x2", "reflect-post-x2"):
        res = _res(tiers, name, executor="sonnet", strict=True)
        assert _models(res) == [HAIKU, OPUS]
    # without an exclusion the random t1a slot may also draw sonnet: haiku stays the anchor
    plain = _res(tiers, "reflect-pre-x2")
    assert _models(plain)[0] == HAIKU and _models(plain)[1] in (OPUS, SONNET)


def test_executor_sonnet_exhausts_tier1b_and_the_x2_fallback_has_two_reviewers(tiers):
    with pytest.raises(pnl.ExclusionExhausted) as err:
        _res(tiers, "reflect-pre", executor="sonnet", strict=True)
    assert err.value.tier == "tier1b"
    fallback = _res(tiers, "reflect-pre-x2", executor="sonnet", strict=True)
    assert len(fallback["reviewers"]) == 2


def test_executor_haiku_skips_the_t4_slot(tiers):
    res = _res(tiers, "reflect-pre", executor="haiku", strict=True)
    assert _models(res) == [SONNET, OPUS]
    assert [s["slot_id"] for s in res["skipped_slots"]] == ["t4"]
    assert res["excluded"]["classes"] == ["haiku"]


def test_executor_opus_with_strict_distinctness_yields_sonnet_and_haiku(tiers):
    res = _res(tiers, "reflect-pre", executor="opus", strict=True)
    assert _models(res) == [SONNET, HAIKU]
    assert len(set(_models(res))) == 2
    assert [s["slot_id"] for s in res["skipped_slots"]] == ["t1a"]


def test_lite_is_sonnet_haiku_haiku_soft_and_sonnet_haiku_strict(tiers):
    assert _models(_res(tiers, "reflect-lite")) == [SONNET, HAIKU, HAIKU]
    strict = _res(tiers, "reflect-lite", strict=True)
    assert _models(strict) == [SONNET, HAIKU]
    assert [s["slot_id"] for s in strict["skipped_slots"]] == ["t2"]


def test_re_review_keeps_only_the_fixed_anchor(tiers):
    assert _models(_res(tiers, "reflect-pre", kind="re-review")) == [SONNET]


def test_cli_reflect_pre_with_executor_sonnet_names_exclusion_exhausted():
    res = CliRunner().invoke(
        main,
        [
            "review", "panel", "resolve", "--template", "@reflect-pre", "--run-id", "r1",
            "--kind", "first", "--env", ENV, "--hard-exclude-class", "sonnet",
            "--strict-distinct",
        ],
    )  # fmt: skip
    assert res.exit_code != 0
    assert "ExclusionExhausted" in res.output and "tier1b" in res.output


def test_cli_reflect_pre_resolves_without_exclusion():
    res = CliRunner().invoke(
        main,
        ["review", "panel", "resolve", "--template", "@reflect-pre", "--run-id", "r1", "--env", ENV],
    )  # fmt: skip
    assert res.exit_code == 0, res.output
    assert [r["model"] for r in json.loads(res.output)["reviewers"]] == [
        SONNET,
        HAIKU,
        OPUS,
    ]
