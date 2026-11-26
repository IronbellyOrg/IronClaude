"""Pin the branch-protection ruleset JSON files (issue 702) and the guide that documents them."""

import json
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_RULESETS = _REPO / ".github" / "rulesets"
_GUIDE = _REPO / "docs" / "developer-guide" / "branch-protection.md"

# Repository admin role, bypass only through a pull request (owner decision 2026-11-25).
_ADMIN_PR_BYPASS = {
    "actor_id": 5,
    "actor_type": "RepositoryRole",
    "bypass_mode": "pull_request",
}

_BRANCH_FILES = {
    "protect-master": "refs/heads/master",
    "protect-integration": "refs/heads/integration",
}


def _load(name):
    return json.loads((_RULESETS / f"{name}.json").read_text(encoding="utf-8"))


# Other IronbellyOrg repos (issue 837): ruleset files derived from protect-master, one table of targets.
_OTHER = _RULESETS / "other-repos"

# applier: who applies; branch: candidate files (a fork lists both roles, the role is chosen on apply day);
# optional: files that may be absent (aidev02 needs a written yes); tag: conditional, skip or handoff.
_TARGETS = {
    "CPA-Manager-Plus": {"applier": "clay", "branch": ["protect-main", "protect-main-mirror"], "optional": [], "tag": "conditional"},
    "IronOrca": {"applier": "clay", "branch": ["protect-main", "protect-main-mirror"], "optional": ["protect-aidev02"], "tag": "conditional"},
    "coder_orca": {"applier": "clay", "branch": ["protect-main"], "optional": [], "tag": "skip"},
    "IronHands-CLI": {"applier": "ryan", "branch": ["protect-main", "protect-main-mirror"], "optional": [], "tag": "handoff"},
    "irondots": {"applier": "ryan", "branch": ["protect-main"], "optional": [], "tag": "handoff"},
    "ironops-marketplace": {"applier": "ryan", "branch": ["protect-main"], "optional": [], "tag": "handoff"},
}

_FULL_ROLE_FILES = {"protect-main": "refs/heads/main", "protect-aidev02": "refs/heads/aidev02"}


def _load_other(name):
    return json.loads((_OTHER / f"{name}.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("name,ref", _BRANCH_FILES.items())
def test_branch_rulesets(name, ref):
    data = _load(name)
    assert data["name"] == name
    assert data["target"] == "branch"
    assert data["enforcement"] == "active"
    # Named explicitly: the default branch moved to integration, so ~DEFAULT_BRANCH would miss master.
    assert data["conditions"]["ref_name"] == {"include": [ref], "exclude": []}
    assert data["bypass_actors"] == [_ADMIN_PR_BYPASS]
    assert sorted(r["type"] for r in data["rules"]) == [
        "deletion",
        "non_fast_forward",
        "pull_request",
    ]
    pr = next(r for r in data["rules"] if r["type"] == "pull_request")
    assert pr["parameters"]["required_approving_review_count"] == 0


def test_tag_ruleset():
    data = _load("protect-release-tags")
    assert data["name"] == "protect-release-tags"
    assert data["target"] == "tag"
    assert data["enforcement"] == "active"
    assert data["conditions"]["ref_name"] == {
        "include": ["refs/tags/v*"],
        "exclude": [],
    }
    assert data["bypass_actors"] == []
    # No creation rule: `git push origin vX.Y.Z` in the release flow must keep working.
    # `update` blocks moving an existing tag forward; `non_fast_forward` alone only blocks rewrites.
    assert sorted(r["type"] for r in data["rules"]) == [
        "deletion",
        "non_fast_forward",
        "update",
    ]


def test_no_default_branch_token_anywhere():
    for path in _RULESETS.rglob("*.json"):
        assert "~DEFAULT_BRANCH" not in path.read_text(encoding="utf-8"), path.name


def test_guide_has_apply_and_check_commands():
    text = _GUIDE.read_text(encoding="utf-8")
    assert "gh api --method POST repos/IronbellyOrg/IronClaude/rulesets --input" in text
    assert "rules/branches/master" in text
    assert "enforcement=disabled" in text
    for name in (*_BRANCH_FILES, "protect-release-tags"):
        assert f".github/rulesets/{name}.json" in text


def test_other_repos_full_role_derived():
    for name, ref in _FULL_ROLE_FILES.items():
        if not (_OTHER / f"{name}.json").exists():
            # Only a file marked optional in the table may be absent.
            assert any(name in t["optional"] for t in _TARGETS.values()), name
            continue
        expected = _load("protect-master")
        expected["name"] = name
        expected["conditions"]["ref_name"]["include"] = [ref]
        data = _load_other(name)
        assert data == expected, name
        assert sorted(r["type"] for r in data["rules"]) == ["deletion", "non_fast_forward", "pull_request"]
        assert data["bypass_actors"] == [_ADMIN_PR_BYPASS]
        pr = next(r for r in data["rules"] if r["type"] == "pull_request")
        assert pr["parameters"]["required_approving_review_count"] == 0


def test_other_repos_mirror_derived():
    expected = _load_other("protect-main")
    expected["name"] = "protect-main-mirror"
    expected["rules"] = [r for r in expected["rules"] if r["type"] != "pull_request"]
    data = _load_other("protect-main-mirror")
    assert data == expected
    assert sorted(r["type"] for r in data["rules"]) == ["deletion", "non_fast_forward"]
    assert data["bypass_actors"] == [_ADMIN_PR_BYPASS]


def test_other_repos_files_match_targets():
    on_disk = {p.stem for p in _OTHER.rglob("*.json")}
    required = {n for t in _TARGETS.values() for n in t["branch"]} - {n for t in _TARGETS.values() for n in t["optional"]}
    optional = {n for t in _TARGETS.values() for n in t["optional"]}
    assert required <= on_disk, f"missing: {sorted(required - on_disk)}"
    assert on_disk <= required | optional, f"unlisted: {sorted(on_disk - required - optional)}"


def test_guide_has_other_repos_section():
    text = _GUIDE.read_text(encoding="utf-8")
    assert "\n## Other IronbellyOrg repos\n" in text
    for repo in _TARGETS:
        assert repo in text, repo
    for path in sorted(_OTHER.rglob("*.json")):
        assert f".github/rulesets/other-repos/{path.name}" in text, path.name
    assert ".github/rulesets/other-repos/protect-aidev02.json" in text
    for token in ("$REPO", "$BRANCH", "admin:org", "ahead_by", "zz-selftest-"):
        assert token in text, token
