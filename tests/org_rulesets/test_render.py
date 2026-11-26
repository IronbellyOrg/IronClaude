"""Rendering, branch set, digest and comparison (pure functions, no process)."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

RULES = Path(__file__).resolve().parents[2] / ".github" / "rulesets"


def parsed(name):
    return json.loads((RULES / name).read_text(encoding="utf-8"))


def test_branch_bodies_equal_the_files(orr):
    assert orr.render_branch("master") == parsed("protect-master.json")
    assert orr.render_branch("integration") == parsed("protect-integration.json")


def test_tag_body_equals_the_file_and_has_the_update_rule(orr):
    body = orr.render_tags()
    assert body == parsed("protect-release-tags.json")
    types = {rule["type"] for rule in body["rules"]}
    assert types == {"deletion", "non_fast_forward", "update"}


def test_other_branch_changes_only_name_and_ref(orr):
    body = orr.render_branch("main")
    expected = parsed("protect-master.json")
    expected["name"] = "protect-main"
    expected["conditions"]["ref_name"]["include"] = ["refs/heads/main"]
    assert body == expected


@pytest.mark.parametrize(
    "bad", ["", "feat/*", "a~b", "refs/heads/x", "~DEFAULT_BRANCH"]
)
def test_bad_branch_names_raise(orr, bad):
    with pytest.raises(ValueError):
        orr.render_branch(bad)


def test_no_body_holds_the_default_branch_placeholder(orr):
    bodies = orr.plan_bodies(["main", "master", "integration"])
    assert "~DEFAULT_BRANCH" not in json.dumps(bodies)


def test_render_returns_a_fresh_copy(orr):
    first = orr.render_branch("master")
    first["rules"].clear()
    assert orr.render_branch("master")["rules"]


@pytest.mark.parametrize(
    ("default", "existing", "expected"),
    [
        ("master", {"master"}, ["master"]),
        ("main", {"master"}, ["master", "main"]),
        ("integration", {"integration", "master"}, ["integration", "master"]),
        ("main", {"integration", "master"}, ["integration", "master", "main"]),
    ],
)
def test_branch_set(orr, default, existing, expected):
    got = orr.branch_set(default, existing)
    assert got == expected
    assert len(got) == len(set(got))


def test_branch_set_refuses_an_empty_default(orr):
    with pytest.raises(ValueError):
        orr.branch_set("", {"master"})


def test_plan_bodies_order(orr):
    names = [b["name"] for b in orr.plan_bodies(["main", "master", "integration"])]
    assert names == [
        "protect-release-tags",
        "protect-integration",
        "protect-master",
        "protect-main",
    ]


def test_plan_bodies_does_not_repeat_a_branch(orr):
    names = [b["name"] for b in orr.plan_bodies(["master", "master"])]
    assert names == ["protect-release-tags", "protect-master"]


def test_digest_is_stable_and_sensitive(orr):
    bodies = orr.plan_bodies(["master", "integration"])
    assert orr.payload_digest(bodies) == orr.payload_digest(copy.deepcopy(bodies))
    changed = copy.deepcopy(bodies)
    changed[1]["enforcement"] = "evaluate"
    assert orr.payload_digest(changed) != orr.payload_digest(bodies)
    assert orr.payload_digest(list(reversed(bodies))) != orr.payload_digest(bodies)


SERVER = {
    "id": 7,
    "source": "acme-one",
    "source_type": "Repository",
    "node_id": "RRS_x",
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-02T00:00:00Z",
    "current_user_can_bypass": "never",
    "_links": {"self": {"href": "https://example.invalid"}},
}


def test_compare_equal_and_server_keys_ignored(orr):
    body = orr.render_branch("master")
    assert orr.compare_bodies(body, copy.deepcopy(body)) == []
    assert orr.compare_bodies(body, {**copy.deepcopy(body), **SERVER}) == []


def test_compare_ignores_rule_and_actor_order(orr):
    body = orr.render_branch("master")
    remote = copy.deepcopy(body)
    remote["rules"].reverse()
    remote["bypass_actors"].reverse()
    assert orr.compare_bodies(body, remote) == []


def _diff(orr, mutate):
    body = orr.render_branch("master")
    remote = copy.deepcopy(body)
    mutate(remote)
    return "\n".join(orr.compare_bodies(body, remote))


def test_compare_names_each_kind_of_difference(orr):
    extra_rule = _diff(
        orr, lambda r: r["rules"].append({"type": "required_signatures"})
    )
    assert "required_signatures" in extra_rule

    extra_actor = _diff(
        orr,
        lambda r: r["bypass_actors"].append(
            {"actor_id": 1, "actor_type": "OrganizationAdmin", "bypass_mode": "always"}
        ),
    )
    assert "OrganizationAdmin" in extra_actor

    def reviews(r):
        r["rules"][2]["parameters"]["required_approving_review_count"] = 2

    assert "required_approving_review_count" in _diff(orr, reviews)

    assert "enforcement" in _diff(orr, lambda r: r.update(enforcement="disabled"))

    def other_ref(r):
        r["conditions"]["ref_name"]["include"] = ["refs/heads/other"]

    assert "conditions" in _diff(orr, other_ref)
    assert "surprise" in _diff(orr, lambda r: r.update(surprise=True))


def test_compare_reports_a_missing_rule(orr):
    assert "deletion" in _diff(orr, lambda r: r["rules"].pop(0))


def test_rendering_does_not_depend_on_the_working_folder(orr, tmp_path, monkeypatch):
    before = (orr.render_branch("integration"), orr.render_tags())
    monkeypatch.chdir(tmp_path)
    assert (orr.render_branch("integration"), orr.render_tags()) == before
