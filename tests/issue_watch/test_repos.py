"""``repos.yaml`` validation, the short name and the model tiers (design 4.4, 5.7, 5.8)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

from superclaude.cli.issue_watch import repos
from superclaude.cli.issue_watch.repos import ReposError, parse_repos

from .conftest import FakeRunner, result, write_repos

ALL = ("tier0", "tier1a", "tier1b", "tier2", "tier2b", "tier3", "tier4")
MEMBER = ("tier2", "tier3", "tier4")


def good() -> dict:
    return {
        "schema_version": 1,
        "orgs": ["IronbellyOrg", "IronbellyGroup"],
        "grants": ["issue.hold"],
        "repos": [
            {
                "repo": "IronbellyOrg/IronClaude",
                "enabled": True,
                "checkout": "/abs/IronClaude",
                "merge_method": "squash",
                "release_merge_method": "merge",
                "release_head": "integration",
                "reviewers": ["augment", "codex"],
                "merge_safety_files": [".github/workflows/**"],
                "max_in_flight": 3,
            }
        ],
    }


def parse(doc: dict, listed: tuple[str, ...] | None = ALL):
    return parse_repos(yaml.safe_dump(doc), listed)


def test_a_clean_file_is_accepted_with_the_defaults():
    rdoc = parse(good())
    entry = rdoc.repos[0]
    assert entry.short == "ironclaude"
    assert (entry.plan_tier, entry.worker_tier, entry.orchestrator_tier) == (
        "tier1b",
        "tier2",
        "tier1b",
    )
    assert entry.max_in_flight == 3 and entry.checkout == Path("/abs/IronClaude")
    assert rdoc.has_grant("issue.hold") and not rdoc.has_grant("pr.merge")
    assert rdoc.get("ironbellyorg/ironclaude") is entry  # compared case-insensitively
    assert rdoc.owner_listed("ironbellyorg")


def _mutated(path: list, value: object) -> dict:
    doc = good()
    node = doc
    for key in path[:-1]:
        node = node[key]
    if value is KeyError:
        del node[path[-1]]
    else:
        node[path[-1]] = value
    return doc


BAD = [
    pytest.param(lambda d: d, "not a mapping", id="top level is a list"),
    pytest.param(_mutated(["schema_version"], 2), None, id="schema_version 2"),
    pytest.param(_mutated(["schema_version"], True), None, id="schema_version true"),
    pytest.param(_mutated(["orgs"], []), None, id="no orgs"),
    pytest.param(_mutated(["repos", 0, "repo"], "no-slash"), None, id="repo pattern"),
    pytest.param(
        _mutated(["repos", 0, "repo"], "Other/Repo"), None, id="owner not in orgs"
    ),
    pytest.param(
        _mutated(["repos", 0, "enabled"], "yes"), None, id="enabled not a bool"
    ),
    pytest.param(
        _mutated(["repos", 0, "checkout"], "relative/path"),
        None,
        id="relative checkout",
    ),
    pytest.param(
        _mutated(["repos", 0, "merge_method"], "fast-forward"), None, id="merge_method"
    ),
    pytest.param(
        _mutated(["repos", 0, "release_merge_method"], "x"), None, id="release method"
    ),
    pytest.param(
        _mutated(["repos", 0, "merge_method"], []), None, id="merge_method list"
    ),
    pytest.param(
        _mutated(["repos", 0, "release_merge_method"], {}),
        None,
        id="release method mapping",
    ),
    pytest.param(
        _mutated(["repos", 0, "release_head"], "bad branch!"), None, id="release_head"
    ),
    pytest.param(_mutated(["repos", 0, "reviewers"], []), None, id="empty reviewers"),
    pytest.param(
        _mutated(["repos", 0, "reviewers"], ["bot"]), None, id="unknown reviewer"
    ),
    pytest.param(
        _mutated(["repos", 0, "merge_safety_files"], None), None, id="safety files null"
    ),
    pytest.param(
        _mutated(["repos", 0, "merge_safety_files"], "x"), None, id="safety files text"
    ),
    pytest.param(
        _mutated(["repos", 0, "merge_safety_files"], [""]), None, id="empty glob"
    ),
    pytest.param(
        _mutated(["repos", 0, "max_in_flight"], 0), None, id="max_in_flight 0"
    ),
    pytest.param(
        _mutated(["repos", 0, "max_in_flight"], 11), None, id="max_in_flight 11"
    ),
    pytest.param(
        _mutated(["repos", 0, "max_in_flight"], True), None, id="max_in_flight bool"
    ),
    pytest.param(_mutated(["repos", 0, "plan_effort"], ""), None, id="empty effort"),
    pytest.param(
        _mutated(["repos", 0, "worker_effort"], 5), None, id="effort not text"
    ),
    pytest.param(
        _mutated(["repos", 0, "plan_tier"], "claude-gw-tier2"),
        None,
        id="model id as tier",
    ),
    pytest.param(_mutated(["plan_tier"], "tier9"), None, id="unknown tier"),
    pytest.param(_mutated(["worker_tier"], 2), None, id="tier not text"),
    pytest.param(
        _mutated(["orchestrator_tier"], "opus"), None, id="model name as tier"
    ),
]


@pytest.mark.parametrize(("doc", "_"), BAD)
def test_every_validation_failure_is_repos_invalid(doc, _):
    doc = doc if isinstance(doc, dict) else ["a", "list"]
    with pytest.raises(ReposError) as err:
        parse(doc)
    assert err.value.reason == "repos_invalid"


def test_unparseable_yaml_and_a_repo_listed_twice_are_refused():
    with pytest.raises(ReposError):
        parse_repos("a: [unclosed", ALL)
    doc = good()
    doc["repos"].append(dict(doc["repos"][0], repo="ironbellyorg/ironclaude"))
    with pytest.raises(ReposError):
        parse(doc)


def test_safety_files_empty_list_is_valid_and_absent_means_the_default():
    doc = good()
    doc["repos"][0]["merge_safety_files"] = []
    assert parse(doc).repos[0].merge_safety_files == ()  # no hold, Clay's word
    del doc["repos"][0]["merge_safety_files"]
    assert parse(doc).repos[0].merge_safety_files is None  # the default list of wave 7


def test_reach_daily_max_reads_any_other_value_as_zero_by_the_spec_text():
    """Design 4.4 (finding F23 of issue 675 calls this a contradiction): implemented as written."""
    for value, want in (
        (7, 7),
        (0, 0),
        (50, 50),
        (51, 0),
        (-1, 0),
        ("x", 0),
        (True, 0),
        (None, 0),
    ):
        doc = good()
        doc["repos"][0]["reach_daily_max"] = value
        assert parse(doc).repos[0].reach_daily_max == want, value


def test_max_in_flight_defaults_to_three_and_a_duplicate_short_name_is_refused():
    doc = good()
    del doc["repos"][0]["max_in_flight"]
    assert parse(doc).repos[0].max_in_flight == 3
    doc["repos"].append({"repo": "IronbellyGroup/Iron-Claude", "enabled": True})
    with pytest.raises(ReposError):  # both give "ironclaude"
        parse(doc)
    assert repos.short_name("IronbellyOrg/IronClaude") == "ironclaude"
    assert repos.short_name("o/A.very_long-repo-name-here") == "averylongrepo"[:12]
    assert len(repos.short_name("o/abcdefghijklmnopqrstuvwxyz")) == 12
    doc = good()
    doc["repos"].append({"repo": "IronbellyOrg/---", "enabled": True})
    with pytest.raises(ReposError):  # no letter or digit left
        parse(doc)


# --- tiers (5.8) ---------------------------------------------------------------------


def test_the_real_ccsession_help_lists_seven_tiers():
    from .conftest import TIERS_TEXT

    assert repos.parse_tiers(TIERS_TEXT) == ALL
    assert repos.parse_tiers("no tiers here") == ()


def test_listed_tiers_reads_ccsession_help_through_the_runner():
    from .conftest import TIERS_TEXT

    runner = FakeRunner({("ccsession", "--help"): result(stdout=TIERS_TEXT)})
    assert repos.listed_tiers(runner, 5) == ALL
    assert runner.argvs() == [("ccsession", "--help")]
    for bad in (
        result(returncode=1),
        result(timed_out=True),
        result(spawn_error="X"),
        result(stdout="nothing"),
    ):
        assert repos.listed_tiers(FakeRunner({("ccsession", "--help"): bad}), 5) is None


def test_a_tier_name_is_valid_and_a_model_id_an_unlisted_tier_and_an_unreadable_list_are_not():
    doc = good()
    doc["worker_tier"] = "tier2"
    assert parse(doc).worker_tier == "tier2"
    for bad in ("claude-gw-tier2", "tier9", "claude-opus-5-5", ""):
        doc["worker_tier"] = bad
        with pytest.raises(ReposError):
            parse(doc)
    doc["worker_tier"] = "tier2"
    for unreadable in (None, ()):
        with pytest.raises(ReposError):
            parse(doc, unreadable)


def test_a_missing_key_takes_its_default_and_a_repo_value_beats_the_top_level_one():
    doc = good()
    doc["plan_tier"] = "tier0"
    doc["repos"][0]["worker_tier"] = "tier3"
    entry = parse(doc).repos[0]
    assert (entry.plan_tier, entry.worker_tier, entry.orchestrator_tier) == (
        "tier0",
        "tier3",
        "tier1b",
    )
    doc["repos"][0]["plan_tier"] = "tier4"
    assert parse(doc).repos[0].plan_tier == "tier4"
    assert parse(doc).plan_tier == "tier0"  # the top-level default is still there


def test_effort_levels_fall_back_to_the_top_level_value():
    doc = good()
    doc["worker_effort"] = "high"
    doc["repos"][0]["plan_effort"] = "max"
    entry = parse(doc).repos[0]
    assert (entry.plan_effort, entry.worker_effort) == ("max", "high")


def test_a_tier_missing_from_a_members_list_falls_once_to_the_next_listed_tier():
    assert repos.resolve_tier("tier2", ALL) == ("tier2", None)
    assert repos.resolve_tier("tier1b", MEMBER) == (
        "tier2",
        "tier1b",
    )  # tiers.md: 1b to 2
    assert repos.resolve_tier("tier0", MEMBER) == ("tier2", "tier0")
    assert repos.fallback_tier("tier2b", MEMBER) == "tier3"


def test_a_configured_tier_with_no_listed_tier_after_it_gives_no_tier():
    assert repos.resolve_tier("tier4", ("tier2", "tier3")) == (None, "tier4")
    assert repos.fallback_tier("tier4", ALL) is None
    assert repos.fallback_tier("not-a-tier", ALL) is None


def test_load_repos_reads_the_file_and_the_tier_list(tmp_path):
    from .conftest import TIERS_TEXT

    orch = tmp_path / "orch"
    orch.mkdir()
    write_repos(orch)
    runner = FakeRunner({("ccsession", "--help"): result(stdout=TIERS_TEXT)})
    rdoc = repos.load_repos(orch, runner, 5)
    assert [r.repo for r in rdoc.repos] == [
        "IronbellyOrg/IronClaude",
        "IronbellyGroup/example",
    ]
    assert rdoc.tiers == ALL
    for broken in (tmp_path / "missing",):
        with pytest.raises(ReposError):
            repos.load_repos(broken, runner, 5)
    (orch / "repos.yaml").write_bytes(b"\xff\xfe")
    with pytest.raises(ReposError):
        repos.load_repos(orch, runner, 5)
    (orch / "repos.yaml").write_text("x: " + "y" * (2 * 1024 * 1024))
    with pytest.raises(ReposError):
        repos.load_repos(orch, runner, 5)


def test_no_unsafe_yaml_load_and_no_new_dependency():
    source = Path(repos.__file__).read_text(encoding="utf-8")
    assert re.search(r"yaml\.load\(", source) is None
    assert "yaml.safe_load(" in source
