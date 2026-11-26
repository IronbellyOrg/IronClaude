"""Pin the commands and structure of the release procedure page (issue 826)."""

import re
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_PAGE = _REPO / "docs" / "developer-guide" / "release-procedure.md"
_TEXT = _PAGE.read_text(encoding="utf-8")

_FORK = "--repo IronbellyOrg/IronClaude"
_FORK_API = "gh api repos/IronbellyOrg/IronClaude"

# One entry per command written in Steps 2 to 6 of the page. The two commands that the page also
# states in prose (`make sync-dev`, the Step 2 ancestry check) are checked by
# test_step2_has_its_own_commands, and `--verify-tag` by test_verify_tag_on_the_release_line.
# A future step that adds a command adds a row here.
_REQUIRED_COMMANDS = (
    "/sc:pr-submit --monitor 3 --head <branch> --base integration",
    "--base integration --head <branch>",
    "gh pr create --repo IronbellyOrg/IronClaude --base master --head integration",
    "gh pr checks <n> --repo IronbellyOrg/IronClaude --watch",
    "git switch --detach <reviewed-head-sha>",
    "gh pr merge <n> --repo IronbellyOrg/IronClaude --merge --match-head-commit <reviewed-head-sha>",
    "--json state,baseRefName,headRefName,headRefOid,mergeCommit",
    "git rev-parse --verify -q <merge-sha>^2",
    "git rev-parse --verify -q <merge-sha>^3",
    "git rev-parse <merge-sha>^{tree} <reviewed-head-sha>^{tree}",
    "gh run list --repo IronbellyOrg/IronClaude --workflow Tests --event push --branch master"
    " --commit <merge-sha> --json databaseId,status,conclusion",
    "git ls-remote --tags origin vX.Y.Z",
    "git ls-remote origin 'refs/tags/vX.Y.Z^{}'",
    "git rev-parse vX.Y.Z^{commit}",
    "gh pr create --repo IronbellyOrg/IronClaude --base integration --head master",
    "gh pr view <m> --repo IronbellyOrg/IronClaude --json files --jq '.files | length'",
    "gh pr checks <m> --repo IronbellyOrg/IronClaude --watch",
    "gh pr merge <m> --repo IronbellyOrg/IronClaude --merge",
    "git merge-base --is-ancestor <merge-sha> origin/integration",
    "git switch -c post-release-vX.Y.Z origin/integration",
    "/sc:post-release vX.Y.Z",
    "gh pr view <n> --repo IronbellyOrg/IronClaude --json headRefOid --jq .headRefOid",
    "git rev-parse origin/master",
    "gh api repos/IronbellyOrg/IronClaude --jq",
    "git rev-parse <merge-sha>^1 <merge-sha>^2",
    "git tag --list vX.Y.Z",
    "git tag -a vX.Y.Z <merge-sha>",
    "git push origin vX.Y.Z",
)

_BANNED_MERGE_OPTIONS = ("--admin", "--auto", "--squash", "--rebase", "--delete-branch")


def _fenced_lines(text=_TEXT):
    """Stripped lines inside triple-backtick fences; a fence marker may be indented."""
    inside = False
    lines = []
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("```"):
            inside = not inside
        elif inside:
            lines.append(stripped)
    return lines


def _section(title_start):
    """Page text from the H2 heading that starts with title_start up to the next H2 heading."""
    out = []
    inside_fence = False
    found = False
    for line in _TEXT.split("\n"):
        if line.strip().startswith("```"):
            inside_fence = not inside_fence
        is_h2 = line.startswith("## ") and not inside_fence
        if is_h2 and found:
            break
        if is_h2 and line[3:].startswith(title_start):
            found = True
        if found:
            out.append(line)
    assert found, f"no H2 heading starts with {title_start!r}"
    return "\n".join(out)


def _h2_headings():
    inside_fence = False
    headings = []
    for line in _TEXT.split("\n"):
        if line.strip().startswith("```"):
            inside_fence = not inside_fence
        elif line.startswith("## ") and not inside_fence:
            headings.append(line[3:])
    return headings


def _slug(heading):
    """GitHub anchor: lowercase, drop characters that are not word characters, spaces or hyphens."""
    return re.sub(r"[^\w\s-]", "", heading.lower()).replace(" ", "-")


@pytest.mark.parametrize("command", _REQUIRED_COMMANDS)
def test_required_command_is_on_the_page(command):
    assert command in _TEXT


def test_step2_has_its_own_commands():
    # Whole fenced lines inside Step 2 only: the release-notes item names `make sync-dev` in prose and
    # Step 5 states the ancestry fact, so a substring test of the page or of the section text would
    # still pass after the Step 2 line was deleted.
    step2 = _fenced_lines(_section("Step 2"))
    assert "make sync-dev" in step2
    assert "git merge-base --is-ancestor origin/master origin/integration" in step2


def test_verify_tag_on_the_release_line():
    # The page also explains the flag in prose, so only the fenced release line counts.
    release_lines = [
        line for line in _fenced_lines() if line.startswith("gh release create")
    ]
    assert release_lines, "no fenced `gh release create` line"
    for line in release_lines:
        assert "--verify-tag" in line


def test_every_gh_line_names_the_fork():
    for line in _fenced_lines():
        if line.startswith("gh "):
            assert _FORK in line or line.startswith(_FORK_API), line


def test_banned_merge_options():
    for line in _fenced_lines():
        for option in _BANNED_MERGE_OPTIONS:
            assert option not in line, f"{option} in fenced line: {line}"
    inside = False
    for line in _TEXT.split("\n"):
        if line.strip().startswith("```"):
            inside = not inside
            continue
        if not inside and any(option in line for option in _BANNED_MERGE_OPTIONS):
            assert "never" in line.lower(), line


@pytest.mark.parametrize(
    "removed",
    [
        "--base master --head <branch>",
        "--limit 3",
        "Every merge to `master` therefore reaches",
    ],
)
def test_removed_text_is_gone(removed):
    assert removed not in _TEXT


def test_contents_links_resolve():
    headings = _h2_headings()
    slugs = [_slug(h) for h in headings]
    contents = _section("Contents")
    anchors = re.findall(r"\]\(#([^)]+)\)", contents)
    assert len(anchors) == 8
    for anchor in anchors:
        assert anchor in slugs, anchor
    expected = [
        "Contents",
        "What a release is here",
        "Step 1",
        "Step 2",
        "Step 3",
        "Step 4",
        "Step 5",
        "Step 6",
        "Sources",
    ]
    assert len(headings) == len(expected), headings
    for heading, start in zip(headings, expected):
        assert heading.startswith(start), (heading, start)
