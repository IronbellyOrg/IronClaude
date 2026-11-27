"""Tests for the ``preflight`` verb of the vcs helper (T-08).

Real git runs only on the throwaway repositories of the ``repo`` fixture. The helper
reads the configuration of the person on purpose (its runner drops every inherited
``GIT_*`` variable), so these tests run it through a runner that adds
``GIT_CONFIG_NOSYSTEM`` and an empty global config, and each test gets an empty
``HOME``. Without that, a filter in ``/etc/gitconfig`` (git-lfs, for example) would
make ``snapshot_lossless`` false in every repository on the machine.

The test of the ``--pathspec-from-file`` floor shows only that the installed git
accepts the option for both ``add`` and ``commit``; that the floor is 2.25 stays
UNVERIFIED, because the oldest git is not available here.
"""

from __future__ import annotations

import importlib
import re
import types

import pytest

from .conftest import git_in


@pytest.fixture(autouse=True)
def empty_home(tmp_path, monkeypatch):
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(home / ".config"))


@pytest.fixture
def vcs(scripts_dir):
    """The ``vcs`` module with ``run_preflight`` bound to a config-isolated runner."""
    module = importlib.import_module("vcs")
    plan = importlib.import_module("vcs_plan")

    class Isolated(plan.GitRunner):
        def _environment(self, index_file):
            env = super()._environment(index_file)
            env["GIT_CONFIG_NOSYSTEM"] = "1"
            env["GIT_CONFIG_GLOBAL"] = "/dev/null"
            return env

    def run_preflight(cwd, make_runner=Isolated):
        return module.run_preflight(cwd, make_runner=make_runner)

    return types.SimpleNamespace(run_preflight=run_preflight, Isolated=Isolated)


@pytest.fixture
def plan(scripts_dir):
    return importlib.import_module("vcs_plan")


@pytest.fixture
def rules(scripts_dir):
    return importlib.import_module("vcs_rules")


@pytest.fixture
def feature(repo):
    """The repository switched to an unprotected branch."""
    repo.git("switch", "-q", "-c", "feature/x")
    return repo


def test_clean_feature_branch_is_ok(vcs, feature):
    out = vcs.run_preflight(str(feature.work))
    assert out["vcs_contract"] == "1"
    assert out["verb"] == "preflight"
    assert out["status"] == "ok"
    assert out["reason"] is None
    assert out["branch"] == "feature/x"
    assert out["symbolic_ref"] == "refs/heads/feature/x"
    assert out["detached"] is False
    assert out["protected"] == {"value": False, "reason": "not-protected"}
    assert out["operation_in_progress"] is None
    assert out["index_lock"] is False
    assert out["min_git_ok"] is True
    assert re.match(r"\d+\.\d+", out["git_version"])
    assert out["top"] == str(feature.work.resolve())
    assert out["hooks_path"] is None
    assert out["submodule_recurse"] is None
    assert out["push_recurse_submodules"] is None


def test_detached_head_is_protected_and_refused(vcs, repo):
    repo.git("checkout", "-q", "--detach")
    out = vcs.run_preflight(str(repo.work))
    assert out["detached"] is True
    assert out["branch"] is None
    assert out["symbolic_ref"] is None
    assert out["protected"] == {"value": True, "reason": "detached-head"}
    assert (out["status"], out["reason"]) == ("refused", "detached-head")


@pytest.mark.parametrize("name", ["master", "main", "integration"])
def test_fixed_protected_names(vcs, repo, name):
    repo.git("checkout", "-q", "-B", name)
    out = vcs.run_preflight(str(repo.work))
    assert out["protected"] == {"value": True, "reason": "protected-name"}
    assert (out["status"], out["reason"]) == ("refused", "protected-branch")


def test_origin_head_target_is_protected(vcs, repo):
    repo.git("push", "-q", "origin", "main:trunk")
    repo.git("fetch", "-q", "origin")
    repo.git("remote", "set-head", "origin", "trunk")
    repo.git("switch", "-q", "-c", "trunk")
    out = vcs.run_preflight(str(repo.work))
    assert out["default_branch_known"] is True
    assert out["notice"] is None
    assert out["protected"] == {"value": True, "reason": "origin-head-target"}
    assert out["reason"] == "protected-branch"


def test_origin_head_unset_is_reported_not_blocking(vcs, feature):
    out = vcs.run_preflight(str(feature.work))
    assert out["default_branch_known"] is False
    assert out["notice"].startswith("default branch unknown: refs/remotes/origin/HEAD")
    assert "git remote set-head origin <branch>" in out["notice"]
    assert out["status"] == "ok"


def test_origin_head_that_does_not_resolve_is_unknown(vcs, feature):
    """A symbolic ref that points at a missing remote-tracking branch adds nothing."""
    feature.git("symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/gone")
    feature.git("switch", "-q", "-c", "gone")
    out = vcs.run_preflight(str(feature.work))
    assert out["default_branch_known"] is False
    assert out["protected"]["value"] is False


def test_merge_in_progress(vcs, repo):
    repo.write("a.txt", "base\n")
    repo.commit("base")
    repo.git("switch", "-q", "-c", "f1")
    repo.write("a.txt", "one\n")
    repo.commit("one")
    repo.git("switch", "-q", "-c", "f2", "main")
    repo.write("a.txt", "two\n")
    repo.commit("two")
    rc, _ = repo.git("merge", "f1", check=False)
    assert rc != 0
    out = vcs.run_preflight(str(repo.work))
    assert out["operation_in_progress"] == "merge"
    assert (out["status"], out["reason"]) == ("refused", "operation-in-progress")


@pytest.mark.parametrize(
    "marker, kind",
    [
        ("CHERRY_PICK_HEAD", "cherry-pick"),
        ("REVERT_HEAD", "revert"),
        ("BISECT_LOG", "bisect"),
        ("rebase-merge/", "rebase"),
        ("rebase-apply/", "rebase"),
    ],
)
def test_other_operation_markers(vcs, feature, marker, kind):
    path = feature.work / ".git" / marker
    if marker.endswith("/"):
        path.mkdir()
    else:
        path.write_text("x\n", encoding="utf-8")
    out = vcs.run_preflight(str(feature.work))
    assert out["operation_in_progress"] == kind


def test_index_lock_present(vcs, feature):
    (feature.work / ".git" / "index.lock").write_text("", encoding="utf-8")
    out = vcs.run_preflight(str(feature.work))
    assert out["index_lock"] is True
    assert (out["status"], out["reason"]) == ("refused", "index-locked")


def test_old_git_is_refused(vcs, feature):
    class OldGit(vcs.Isolated):
        def run(self, argv, **kw):
            if list(argv) == ["--version"]:
                return 0, "git version 2.19.0\n"
            return super().run(argv, **kw)

    out = vcs.run_preflight(str(feature.work), make_runner=OldGit)
    assert out["git_version"] == "2.19.0"
    assert out["min_git_ok"] is False
    assert (out["status"], out["reason"]) == ("refused", "git-too-old")


def test_unparseable_version_is_not_ok(vcs, feature):
    class OddGit(vcs.Isolated):
        def run(self, argv, **kw):
            if list(argv) == ["--version"]:
                return 0, "something else\n"
            return super().run(argv, **kw)

    out = vcs.run_preflight(str(feature.work), make_runner=OddGit)
    assert out["git_version"] is None
    assert out["min_git_ok"] is False


def test_precedence_names_the_first_refusal(vcs, repo):
    repo.git("checkout", "-q", "--detach")
    (repo.work / ".git" / "index.lock").write_text("", encoding="utf-8")
    assert vcs.run_preflight(str(repo.work))["reason"] == "detached-head"


def test_snapshot_lossless_default_true(vcs, feature):
    assert vcs.run_preflight(str(feature.work))["snapshot_lossless"] is True


@pytest.mark.parametrize(
    "key, value",
    [
        ("filter.lfs.clean", "git-lfs clean -- %f"),
        ("filter.lfs.smudge", "git-lfs smudge -- %f"),
        ("filter.x.process", "git-lfs filter-process"),
        ("core.autocrlf", "true"),
    ],
)
def test_snapshot_lossless_false(vcs, feature, key, value):
    feature.git("config", key, value)
    assert vcs.run_preflight(str(feature.work))["snapshot_lossless"] is False


@pytest.mark.parametrize(
    "key, value", [("core.autocrlf", "input"), ("filter.x.required", "true")]
)
def test_snapshot_lossless_ignores_other_settings(vcs, feature, key, value):
    feature.git("config", key, value)
    assert vcs.run_preflight(str(feature.work))["snapshot_lossless"] is True


def test_config_values_are_reported(vcs, feature):
    feature.git("config", "core.hooksPath", ".githooks")
    feature.git("config", "submodule.recurse", "true")
    feature.git("config", "push.recurseSubmodules", "check")
    out = vcs.run_preflight(str(feature.work))
    assert out["hooks_path"] == ".githooks"
    assert out["submodule_recurse"] == "true"
    assert out["push_recurse_submodules"] == "check"


def test_not_a_repository(vcs, tmp_path):
    plain = tmp_path / "plain"
    plain.mkdir()
    out = vcs.run_preflight(str(plain))
    assert (out["status"], out["reason"]) == ("refused", "not-a-repo")
    assert out["vcs_contract"] == "1"


def test_inside_a_submodule_the_default_comes_from_its_own_refs(vcs, submodule_repo):
    sub = submodule_repo.work / submodule_repo.sub_path
    git_in(sub, "switch", "-q", "-c", "work")
    git_in(sub, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")
    git_in(sub, "push", "-q", "origin", "HEAD:refs/heads/lib")
    git_in(sub, "fetch", "-q", "origin")
    git_in(sub, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/lib")
    git_in(sub, "switch", "-q", "-c", "lib")
    out = vcs.run_preflight(str(sub))
    assert out["top"] == str(sub.resolve())
    assert out["default_branch_known"] is True
    assert out["protected"] == {"value": True, "reason": "origin-head-target"}
    # the superproject has no origin/HEAD of its own, so it knows no default
    git_in(submodule_repo.work, "switch", "-q", "-c", "lib")
    top = vcs.run_preflight(str(submodule_repo.work))
    assert top["top"] == str(submodule_repo.work.resolve())
    assert top["default_branch_known"] is False
    assert top["protected"]["value"] is False


def test_installed_git_accepts_pathspec_from_file_for_add_and_commit(repo, rules):
    """Shows the installed git accepts the option; the 2.25 floor stays UNVERIFIED."""
    version = tuple(
        int(n)
        for n in re.search(r"(\d+)\.(\d+)", git_in(repo.work, "--version")).groups()
    )
    assert version >= rules.MIN_GIT
    repo.git("switch", "-q", "-c", "feature/p")
    repo.write("one.txt", "1\n")
    repo.write("two.txt", "2\n")
    listing = repo.root / "paths.txt"
    listing.write_text("one.txt\n", encoding="utf-8")
    repo.git("add", f"--pathspec-from-file={listing}")
    assert repo.git("diff", "--cached", "--name-only").split() == ["one.txt"]
    listing.write_text("one.txt\ntwo.txt\n", encoding="utf-8")
    repo.git("add", f"--pathspec-from-file={listing}")
    repo.git("commit", "-q", "-m", "p")
    repo.write("one.txt", "1b\n")
    repo.write("two.txt", "2b\n")
    repo.write("three.txt", "3\n")
    repo.git("commit", "-q", "-m", "q", "--only", f"--pathspec-from-file={listing}")
    assert repo.git("show", "--name-only", "--format=", "HEAD").split() == [
        "one.txt",
        "two.txt",
    ]
    assert repo.git("status", "--porcelain").strip() == "?? three.txt"
