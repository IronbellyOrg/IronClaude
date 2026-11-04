"""Behavior tests for the /sc:issue origin-repo resolver and claim-URL check.

Enforcement type: EXECUTABLE (script behavior). The script is loaded by path,
the same way test_workflow_archive.py loads archive_workspace.py.
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

_SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py"
)
_spec = importlib.util.spec_from_file_location("origin_repo", _SCRIPT)
orr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(orr)

ORIGIN = "IronbellyOrg/IronClaude"


# --- origin URL parsing -------------------------------------------------------


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/IronbellyOrg/IronClaude",  # https
        "https://github.com/IronbellyOrg/IronClaude.git",  # https + .git suffix
        "https://github.com/IronbellyOrg/IronClaude/",  # https + trailing /
        "https://github.com/IronbellyOrg/IronClaude.git/",  # .git + trailing /
        "git@github.com:IronbellyOrg/IronClaude",  # ssh
        "git@github.com:IronbellyOrg/IronClaude.git",  # ssh + .git suffix
        "git@github.com:IronbellyOrg/IronClaude/",  # ssh + trailing /
        "https://github.com/IronbellyOrg/IronClaude\n",  # git output newline
    ],
)
def test_github_origin_forms_parse_to_owner_repo(url):
    assert orr.parse_origin_url(url) == ORIGIN


@pytest.mark.parametrize(
    "url",
    [
        "https://gitlab.com/IronbellyOrg/IronClaude.git",
        "git@bitbucket.org:IronbellyOrg/IronClaude.git",
        "https://github.com/IronbellyOrg",
        "/srv/git/IronClaude.git",
        "",
    ],
)
def test_non_github_origin_does_not_parse(url):
    assert orr.parse_origin_url(url) is None


# --- running the script in a real temporary repository ------------------------


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def _repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    return repo


def _run(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(_SCRIPT), *args],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )


def test_non_github_origin_exits_nonzero_with_e_no_origin(tmp_path):
    repo = _repo(tmp_path)
    _git(repo, "remote", "add", "origin", "https://gitlab.com/IronbellyOrg/IronClaude.git")
    result = _run(repo)
    assert result.returncode == orr.EXIT_NO_ORIGIN != 0
    assert "E-NO-ORIGIN" in result.stderr
    assert result.stdout == ""


def test_missing_origin_exits_nonzero_with_e_no_origin(tmp_path):
    repo = _repo(tmp_path)
    result = _run(repo)
    assert result.returncode == orr.EXIT_NO_ORIGIN != 0
    assert "E-NO-ORIGIN" in result.stderr


def test_missing_origin_with_other_remote_still_e_no_origin(tmp_path):
    repo = _repo(tmp_path)
    _git(repo, "remote", "add", "upstream", "https://github.com/SomeParent/Framework.git")
    result = _run(repo)
    assert result.returncode == orr.EXIT_NO_ORIGIN
    assert "E-NO-ORIGIN" in result.stderr


def test_only_origin_is_read_when_another_remote_exists(tmp_path):
    repo = _repo(tmp_path)
    _git(repo, "remote", "add", "upstream", "https://github.com/SomeParent/Framework.git")
    _git(repo, "remote", "add", "origin", "git@github.com:IronbellyOrg/IronClaude.git")
    result = _run(repo)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == ORIGIN
    assert "SomeParent" not in result.stdout


def test_claim_mode_prints_repo_and_number(tmp_path):
    repo = _repo(tmp_path)
    _git(repo, "remote", "add", "origin", "https://github.com/IronbellyOrg/IronClaude")
    result = _run(repo, "--claim", "https://github.com/IronbellyOrg/IronClaude/issues/302")
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == {"repo": ORIGIN, "number": 302}


def test_claim_mode_foreign_url_exits_with_distinct_code(tmp_path):
    repo = _repo(tmp_path)
    _git(repo, "remote", "add", "origin", "https://github.com/IronbellyOrg/IronClaude")
    result = _run(repo, "--claim", "https://github.com/octocat/Hello-World/issues/1")
    assert result.returncode == orr.EXIT_FOREIGN_REPO
    assert orr.EXIT_FOREIGN_REPO not in (0, orr.EXIT_NO_ORIGIN)
    assert "E-FOREIGN-REPO" in result.stderr
    assert result.stdout == ""


def test_claim_mode_without_origin_reports_e_no_origin_first(tmp_path):
    repo = _repo(tmp_path)
    result = _run(repo, "--claim", "302")
    assert result.returncode == orr.EXIT_NO_ORIGIN
    assert "E-NO-ORIGIN" in result.stderr


def test_bad_arguments_exit_2(tmp_path):
    repo = _repo(tmp_path)
    result = _run(repo, "--no-such-flag")
    assert result.returncode == 2


# --- claim argument versus origin (E-FOREIGN-REPO, design section 20 item 4) --


@pytest.mark.parametrize(
    ("arg", "number"),
    [
        ("302", 302),
        ("#302", 302),
        ("https://github.com/IronbellyOrg/IronClaude/issues/302", 302),  # same repo
        ("https://github.com/ironbellyorg/ironclaude/issues/302", 302),  # case-insensitive
        ("https://github.com/IronbellyOrg/IronClaude/issues/302/", 302),  # trailing /
        ("https://github.com/IronbellyOrg/IronClaude/issues/302#issuecomment-9", 302),  # fragment
        ("https://github.com/IronbellyOrg/IronClaude/issues/302?x=1", 302),  # query
        ("http://github.com/IronbellyOrg/IronClaude/issues/302", 302),  # http scheme
        ("github.com/IronbellyOrg/IronClaude/issues/302", 302),  # no scheme
        ("www.github.com/IronbellyOrg/IronClaude/issues/302", 302),  # no scheme, www.
        ("https://www.github.com/IronbellyOrg/IronClaude/issues/302", 302),  # www.
        ("git@github.com:IronbellyOrg/IronClaude/issues/302", 302),  # git@ form
    ],
)
def test_claim_on_origin_returns_issue_number(arg, number):
    assert orr.check_claim(arg, ORIGIN) == number


@pytest.mark.parametrize(
    "arg",
    [
        "https://github.com/octocat/IronClaude/issues/1",  # foreign owner
        "https://github.com/IronbellyOrg/OtherRepo/issues/1",  # same owner, different repo
        "https://github.com/IronbellyOrg/IronClaudeX/issues/1",  # repo-name prefix
        "https://github.com/IronbellyOrg/IronClaud/issues/1",  # origin repo is a prefix of it
        "https://github.com/IronbellyOrgX/IronClaude/issues/1",  # owner-name prefix
        "https://github.com/IronbellyOrg/no-such-repo-sc-issue-probe/issues/999999999",
        "https://gitlab.com/IronbellyOrg/IronClaude/issues/1",  # not GitHub
        "https://github.com/IronbellyOrg",  # no repository
        "github.com/octocat/Hello-World/issues/1",  # no scheme, foreign
        "www.github.com/IronbellyOrg/IronClaudeX/issues/1",  # no scheme, prefix
        "git@github.com:octocat/Hello-World.git",  # git@ form, foreign
        "git@bitbucket.org:IronbellyOrg/IronClaude.git",  # git@ form, not GitHub
    ],
)
def test_claim_url_on_another_repo_is_e_foreign_repo(arg):
    with pytest.raises(orr.ClaimError) as exc:
        orr.check_claim(arg, ORIGIN)
    assert exc.value.code == "E-FOREIGN-REPO"
    assert exc.value.exit_code == orr.EXIT_FOREIGN_REPO


@pytest.mark.parametrize(
    "arg",
    [
        "https://github.com/IronbellyOrg/IronClaude/pull/302",
        "https://github.com/IronbellyOrg/IronClaude/pull/302/",
        "https://github.com/IronbellyOrg/IronClaude/pull/302#discussion_r1",
    ],
)
def test_pull_url_on_origin_is_rejected_not_parsed(arg):
    with pytest.raises(orr.ClaimError) as exc:
        orr.check_claim(arg, ORIGIN)
    assert exc.value.code == "E-NOT-AN-ISSUE"
    assert exc.value.exit_code == orr.EXIT_NOT_AN_ISSUE


def test_pull_url_on_foreign_repo_is_e_foreign_repo():
    with pytest.raises(orr.ClaimError) as exc:
        orr.check_claim("https://github.com/octocat/Hello-World/pull/302", ORIGIN)
    assert exc.value.code == "E-FOREIGN-REPO"


@pytest.mark.parametrize(
    ("origin", "arg"),
    [
        ("Org302/Repo456", "https://github.com/Org302/Repo456"),
        ("Org302/Repo456", "https://github.com/Org302/Repo456/"),
        ("Org302/Repo456", "https://github.com/Org302/Repo456/issues"),
        ("IronbellyOrg/IronClaude302", "https://github.com/IronbellyOrg/IronClaude302/tree/main"),
    ],
)
def test_digits_in_owner_or_repo_never_become_n(origin, arg):
    with pytest.raises(orr.ClaimError) as exc:
        orr.check_claim(arg, origin)
    assert exc.value.code == "E-NOT-AN-ISSUE"


def test_digits_in_owner_and_repo_do_not_replace_the_issue_segment():
    assert orr.check_claim("https://github.com/Org302/Repo456/issues/7", "Org302/Repo456") == 7


@pytest.mark.parametrize(
    "arg",
    [
        "",
        "abc",
        "0",
        "-3",
        "302abc",
        "https://github.com/IronbellyOrg/IronClaude/issues/abc",
        "https://github.com/IronbellyOrg/IronClaude/issues/302/comments",
        "github.com/IronbellyOrg/IronClaude",  # origin, no scheme, no issue path
        "git@github.com:IronbellyOrg/IronClaude.git",  # origin remote URL, no issue path
    ],
)
def test_other_arguments_are_not_an_issue(arg):
    with pytest.raises(orr.ClaimError) as exc:
        orr.check_claim(arg, ORIGIN)
    assert exc.value.code == "E-NOT-AN-ISSUE"


def test_script_imports_only_standard_library():
    import ast

    tree = ast.parse(_SCRIPT.read_text(encoding="utf-8"))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
    assert names <= set(sys.stdlib_module_names)
