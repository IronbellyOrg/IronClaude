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
    assert sorted(r["type"] for r in data["rules"]) == ["deletion", "non_fast_forward"]


def test_no_default_branch_token_anywhere():
    for path in _RULESETS.glob("*.json"):
        assert "~DEFAULT_BRANCH" not in path.read_text(encoding="utf-8"), path.name


def test_guide_has_apply_and_check_commands():
    text = _GUIDE.read_text(encoding="utf-8")
    assert "gh api --method POST repos/IronbellyOrg/IronClaude/rulesets --input" in text
    assert "rules/branches/master" in text
    assert "enforcement=disabled" in text
    for name in (*_BRANCH_FILES, "protect-release-tags"):
        assert f".github/rulesets/{name}.json" in text
