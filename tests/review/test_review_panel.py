"""Panel template, tier aliases and resolution (PN1, shared contract C1-C3)."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from superclaude.cli.review import panel as pnl


@pytest.fixture
def tiers():
    return pnl.load_tiers()


@pytest.fixture
def tpl():
    return pnl.load_panel()


def test_default_files_validate(tiers, tpl):
    assert pnl.validate_tiers(tiers) == []
    assert pnl.validate_panel(tpl) == []
    assert pnl.validate_panel(tpl, tiers) == []


@pytest.mark.parametrize(
    "mutate, needle",
    [
        (lambda o: o.update(bogus=1), "unknown key"),
        (lambda o: o["slots"][1].update(tier="tier9"), "not defined"),
        (lambda o: o["slots"][1].update(count=0), "count"),
        (lambda o: o["slots"][1].update(count=5), "count"),
        (lambda o: o["slots"][1].update(strategy="fixed"), "fixed"),
        (lambda o: o["slots"][1].update(slot_id="t1b"), "duplicate"),
        (
            lambda o: o["slots"].extend(
                [
                    {
                        "slot_id": "t4",
                        "tier": "tier4",
                        "count": 4,
                        "strategy": "random",
                    },
                    {
                        "slot_id": "t5",
                        "tier": "tier4",
                        "count": 3,
                        "strategy": "random",
                    },
                ]
            ),
            "total",
        ),
        (lambda o: o.update(apply_to=["sometimes"]), "apply_to"),
        (lambda o: o.update(apply_to=[]), "apply_to"),
        (lambda o: o.update(schema="review-panel/2"), "schema"),
        (lambda o: o.update(version="1.0"), "version"),
        (lambda o: o.update(template_id="Bad Id"), "template_id"),
        (lambda o: o.update(distinct_across_slots="yes"), "distinct_across_slots"),
        (lambda o: o["slots"][0].update(strategy="sometimes"), "strategy"),
        (lambda o: o["slots"][0].update(extra=1), "unknown key"),
        (
            lambda o: o["slots"].__setitem__(0, dict(o["slots"][1], slot_id="t2b")),
            "fixed",
        ),
    ],
)
def test_panel_schema_errors(tiers, tpl, mutate, needle):
    obj = copy.deepcopy(tpl)
    mutate(obj)
    errors = pnl.validate_panel(obj, tiers)
    assert errors, "mutation must be caught"
    assert any(needle in e for e in errors), errors


def test_panel_total_of_nine_reviewers_is_rejected(tiers, tpl):
    obj = copy.deepcopy(tpl)
    obj["slots"] = [
        {"slot_id": "a", "tier": "tier1b", "count": 3, "strategy": "fixed"},
        {"slot_id": "b", "tier": "tier2", "count": 3, "strategy": "random"},
        {"slot_id": "c", "tier": "tier3", "count": 3, "strategy": "random"},
    ]
    errors = pnl.validate_panel(obj, tiers)
    assert any("total" in e for e in errors), errors


def test_panel_two_fixed_slots_are_rejected(tiers, tpl):
    obj = copy.deepcopy(tpl)
    obj["slots"][1]["strategy"] = "fixed"
    assert any("fixed" in e for e in pnl.validate_panel(obj, tiers))


def test_panel_without_fixed_slot_is_rejected(tiers, tpl):
    obj = copy.deepcopy(tpl)
    obj["slots"][0]["strategy"] = "random"
    assert any("fixed" in e for e in pnl.validate_panel(obj, tiers))


def test_tier_schema_errors(tiers):
    def bad(mutate):
        obj = copy.deepcopy(tiers)
        mutate(obj)
        return pnl.validate_tiers(obj)

    assert any(
        "duplicate" in e
        for e in bad(lambda o: o["aliases"]["tier2"]["models"].append("gpt-6.1-sol"))
    )
    assert any(
        "available" in e
        for e in bad(
            lambda o: o["environments"]["anthropic-only"]["stand_ins"].update(
                tier2=["not-served"]
            )
        )
    )
    assert any(
        "tier" in e
        for e in bad(
            lambda o: o["environments"]["anthropic-only"]["stand_ins"].update(
                tier9=["claude-haiku-5-5"]
            )
        )
    )
    assert any("schema" in e for e in bad(lambda o: o.update(schema="x")))
    assert any(
        "models" in e for e in bad(lambda o: o["aliases"]["tier2"].update(models=[]))
    )
    assert any(
        "alias" in e
        for e in bad(
            lambda o: o["aliases"]["tier2"].update(alias="bad alias with spaces")
        )
    )


# --- resolve_slot (C3) -----------------------------------------------------


def _models(tiers, tier):
    return tiers["aliases"][tier]["models"]


def test_stand_in_for_tier3_when_only_haiku_available(tiers):
    r = pnl.resolve_slot(
        _models(tiers, "tier3"),
        "random",
        "s",
        ["claude-haiku-5-5"],
        ["claude-haiku-5-5"],
    )
    assert r["model"] == "claude-haiku-5-5"
    assert r["stand_in"] is True
    assert r["fallback_depth"] == 0


def test_no_model_available_raises(tiers):
    with pytest.raises(pnl.NoModelAvailable):
        pnl.resolve_slot(
            _models(tiers, "tier3"), "random", "s", ["claude-haiku-5-5"], []
        )


def test_tier1b_falls_back_to_depth_1_and_2(tiers):
    models = _models(tiers, "tier1b")
    r1 = pnl.resolve_slot(models, "fixed", None, ["gpt-6.1-sol"], [])
    assert (r1["model"], r1["fallback_depth"], r1["stand_in"]) == (
        "gpt-6.1-sol",
        1,
        False,
    )
    r2 = pnl.resolve_slot(models, "fixed", None, ["muse-wonder-full-1.0"], [])
    assert (r2["model"], r2["fallback_depth"]) == ("muse-wonder-full-1.0", 2)
    r0 = pnl.resolve_slot(models, "fixed", None, "all", [])
    assert (r0["model"], r0["fallback_depth"]) == ("claude-sonnet-5-5", 0)
    assert r0["fallbacks"] == ["gpt-6.1-sol", "muse-wonder-full-1.0"]


def test_fallbacks_wrap_around_after_the_chosen_model():
    r = pnl.resolve_slot(["a", "b", "c", "d"], "round_robin", 2, "all", [])
    assert r["model"] == "c"
    assert r["fallbacks"] == ["d", "a", "b"]


def test_random_is_reproducible_and_inside_candidates(tiers):
    models = _models(tiers, "tier2")
    first = pnl.resolve_slot(models, "random", "123|t3|1", "all", [])
    for _ in range(20):
        assert pnl.resolve_slot(models, "random", "123|t3|1", "all", []) == first
    seen = {
        pnl.resolve_slot(models, "random", f"s{i}", ["glm-5.3", "grok-4.7"], [])[
            "model"
        ]
        for i in range(40)
    }
    assert seen <= {"glm-5.3", "grok-4.7"}
    assert len(seen) == 2


def test_exclude_applies_only_when_another_candidate_exists():
    models = ["a", "b"]
    for i in range(30):
        assert (
            pnl.resolve_slot(models, "random", f"s{i}", "all", [], exclude=("a",))[
                "model"
            ]
            == "b"
        )
    only = pnl.resolve_slot(["a"], "random", "s", "all", [], exclude=("a",))
    assert only["model"] == "a"


def test_distinct_across_slots(tiers, tpl):
    t = copy.deepcopy(tiers)
    t["aliases"]["tier2"]["models"] = ["m1", "m2"]
    t["aliases"]["tier3"]["models"] = ["m1", "m2"]
    t["environments"]["x"] = {"available": "all", "stand_ins": {}, "launch": {}}
    for run in ("a", "b", "c", "d", "e"):
        out = pnl.resolve(tpl, t, "x", run)
        by_id = {r["reviewer_id"]: r["model"] for r in out["reviewers"]}
        # two candidates: the second slot instance must differ from the first one
        assert by_id["t3-1"] != by_id["t2-1"]


def test_reordering_alias_list_changes_fixed_result_without_code_change(
    tiers, tpl, tmp_path
):
    t = copy.deepcopy(tiers)
    t["aliases"]["tier1b"]["models"] = ["gpt-6.1-sol", "claude-sonnet-5-5"]
    path = tmp_path / "tiers.json"
    path.write_text(json.dumps(t))
    loaded = pnl.load_tiers(str(path))
    out = pnl.resolve(tpl, loaded, "gateway", "run")
    assert out["reviewers"][0]["model"] == "gpt-6.1-sol"
    base = pnl.resolve(tpl, tiers, "gateway", "run")
    assert base["reviewers"][0]["model"] == "claude-sonnet-5-5"


def test_adding_a_model_family_is_a_data_edit_only(tiers, tpl, tmp_path):
    t = copy.deepcopy(tiers)
    t["aliases"]["tier3"]["models"] = ["acme-1"]
    t["environments"]["acme"] = {
        "available": ["acme-1", "claude-sonnet-5-5"],
        "stand_ins": {"tier2": ["claude-sonnet-5-5"]},
        "launch": {"acme-1": "acme-launcher", "claude-sonnet-5-5": "sonnet"},
    }
    t["names"]["acme-1"] = "Acme One"
    assert pnl.validate_tiers(t) == []
    path = tmp_path / "t.json"
    path.write_text(json.dumps(t))
    out = pnl.resolve(tpl, pnl.load_tiers(str(path)), "acme", "run")
    ids = {r["reviewer_id"]: r for r in out["reviewers"]}
    assert ids["t3-1"]["model"] == "acme-1" and ids["t3-1"]["launch"] == "acme-launcher"
    assert ids["t3-1"]["model_name"] == "Acme One"
    assert ids["t2-1"]["stand_in"] is True


# --- resolve (C3) ------------------------------------------------------------


def test_anthropic_only_resolution_for_three_run_ids(tiers, tpl):
    for run in ("b1-r1", "b1-r2", "x"):
        out = pnl.resolve(tpl, tiers, "anthropic-only", run)
        assert out["schema"] == "review-panel-resolution/1"
        assert out["environment"] == "anthropic-only"
        assert out["review_kind"] == "first"
        rows = {r["reviewer_id"]: r for r in out["reviewers"]}
        assert list(rows) == ["t1b-1", "t2-1", "t3-1", "t3-2"]
        assert rows["t1b-1"]["model"] == "claude-sonnet-5-5"
        assert rows["t1b-1"]["launch"] == "sonnet"
        assert rows["t1b-1"]["fallback_depth"] == 0
        assert rows["t1b-1"]["stand_in"] is False
        for rid in ("t2-1", "t3-1", "t3-2"):
            assert rows[rid]["model"] == "claude-haiku-5-5"
            assert rows[rid]["launch"] == "haiku"
            assert rows[rid]["fallback_depth"] == 0
            assert rows[rid]["stand_in"] is True
        assert rows["t3-1"]["seed"].endswith("|t3|1") and rows["t3-2"]["seed"].endswith(
            "|t3|2"
        )
        assert rows["t1b-1"]["seed"] is None


def test_re_review_resolves_only_the_anchor(tiers, tpl):
    out = pnl.resolve(tpl, tiers, "anthropic-only", "b1-r1", review_kind="re-review")
    assert [r["reviewer_id"] for r in out["reviewers"]] == ["t1b-1"]
    assert out["review_kind"] == "re-review"


def test_resolution_is_byte_identical_for_equal_inputs(tiers, tpl):
    a = json.dumps(pnl.resolve(tpl, tiers, "anthropic-only", "r1"), sort_keys=True)
    b = json.dumps(
        pnl.resolve(copy.deepcopy(tpl), copy.deepcopy(tiers), "anthropic-only", "r1"),
        sort_keys=True,
    )
    assert a == b


def test_gateway_resolution_prints_launch_null(tiers, tpl):
    out = pnl.resolve(tpl, tiers, "gateway", "run")
    assert all(r["launch"] is None for r in out["reviewers"])
    assert out["reviewers"][0]["model"] == "claude-sonnet-5-5"
    assert all(r["stand_in"] is False for r in out["reviewers"])
    assert len(out["template_sha256"]) == 64 and len(out["tiers_sha256"]) == 64


def test_round_robin_uses_sequence(tiers):
    tpl = {
        "schema": "review-panel/1",
        "template_id": "rr",
        "version": "1.0.0",
        "distinct_across_slots": False,
        "apply_to": ["first"],
        "slots": [
            {"slot_id": "a", "tier": "tier1b", "count": 1, "strategy": "fixed"},
            {"slot_id": "b", "tier": "tier3", "count": 2, "strategy": "round_robin"},
        ],
    }
    assert pnl.validate_panel(tpl, tiers) == []
    n = len(tiers["aliases"]["tier3"]["models"])
    out = pnl.resolve(tpl, tiers, "gateway", "run", sequence=n)
    models = tiers["aliases"]["tier3"]["models"]
    got = [r["model"] for r in out["reviewers"] if r["slot_id"] == "b"]
    assert got == [models[0], models[1]]


def test_select_env_precedence():
    assert pnl.select_env("gateway", {}) == "gateway"
    assert (
        pnl.select_env(
            None, {"SUPERCLAUDE_REVIEW_ENV": "anthropic-only", "T3Model01": "x"}
        )
        == "anthropic-only"
    )
    assert pnl.select_env(None, {"T3Model01": "x"}) == "gateway"
    assert pnl.select_env(None, {"T3Model01": ""}) == "anthropic-only"
    assert pnl.select_env(None, {}) == "anthropic-only"


def test_template_lookup_precedence(tmp_path, monkeypatch):
    home = tmp_path / "home"
    proj = tmp_path / "proj"
    for d in (home / ".superclaude", proj / ".superclaude"):
        d.mkdir(parents=True)
    base = pnl.load_panel()

    def write(path, tid):
        obj = copy.deepcopy(base)
        obj["template_id"] = tid
        path.write_text(json.dumps(obj))
        return path

    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("SUPERCLAUDE_REVIEW_PANEL", raising=False)
    monkeypatch.chdir(proj)
    assert pnl.load_panel()["template_id"] == "default"
    write(home / ".superclaude" / "review-panel.json", "from-user")
    assert pnl.load_panel()["template_id"] == "from-user"
    write(proj / ".superclaude" / "review-panel.json", "from-project")
    assert pnl.load_panel()["template_id"] == "from-project"
    env_file = write(tmp_path / "env.json", "from-env")
    monkeypatch.setenv("SUPERCLAUDE_REVIEW_PANEL", str(env_file))
    assert pnl.load_panel()["template_id"] == "from-env"
    explicit = write(tmp_path / "explicit.json", "from-flag")
    assert pnl.load_panel(str(explicit))["template_id"] == "from-flag"


def test_tier_file_lookup_precedence(tmp_path, monkeypatch):
    home = tmp_path / "home"
    (home / ".superclaude").mkdir(parents=True)
    proj = tmp_path / "proj"
    proj.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("SUPERCLAUDE_REVIEW_TIERS", raising=False)
    monkeypatch.chdir(proj)
    base = pnl.load_tiers()
    user = copy.deepcopy(base)
    user["version"] = "9.0.0"
    (home / ".superclaude" / "review-tiers.json").write_text(json.dumps(user))
    assert pnl.load_tiers()["version"] == "9.0.0"
    envf = copy.deepcopy(base)
    envf["version"] = "8.0.0"
    (tmp_path / "e.json").write_text(json.dumps(envf))
    monkeypatch.setenv("SUPERCLAUDE_REVIEW_TIERS", str(tmp_path / "e.json"))
    assert pnl.load_tiers()["version"] == "8.0.0"


def test_invalid_template_file_is_rejected(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"schema": "review-panel/1"}))
    with pytest.raises(ValueError):
        pnl.load_panel(str(bad))


def test_packaged_defaults_are_read_through_importlib_resources():
    root = Path(pnl.__file__).parent / "data"
    assert (root / "review-panel.default.json").is_file()
    assert (root / "review-tiers.default.json").is_file()


def test_round_robin_skips_excluded_models_when_another_is_free():
    r = pnl.resolve_slot(["a", "b", "c"], "round_robin", 0, "all", [], exclude=("a",))
    assert r["model"] == "b"
    only = pnl.resolve_slot(["a"], "round_robin", 0, "all", [], exclude=("a",))
    assert only["model"] == "a"
