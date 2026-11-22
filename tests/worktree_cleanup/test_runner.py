"""Task 2: the allowlisted command runner, the command line and the file header.

Each refusal below must fail if its rule is removed from ``Runner.check_allowed``. The
runner is a positive allowlist (every command must match one exact argument shape), so
the refusals include bundled and shortened spellings of the banned options.
"""

from __future__ import annotations

import ast
import subprocess
import sys

import pytest

from .conftest import LANDED, SCRIPT

REPO = "IronbellyOrg/IronClaude"
HELPER = "credential.helper=!gh auth git-credential"


def _source() -> str:
    return SCRIPT.read_text(encoding="utf-8")


# --- command line -----------------------------------------------------------


def test_help_lists_the_four_verbs_and_the_two_flags():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    for word in ("list", "archive", "retire", "prune", "--apply", "--out"):
        assert word in proc.stdout


def test_main_accepts_an_injected_runner(wc, runner_cls, tmp_path):
    runner = runner_cls()
    # no Orca answer and no git checkout here: the run reports it and exits 69, starting nothing else
    code = wc.main(
        ["list"], runner=runner, env={}, cwd=str(tmp_path), proc_root=str(tmp_path)
    )
    assert code == wc.EXIT_FAILED
    assert runner.commands and all(
        c.argv[:3]
        in (["orca", "repo", "list"], ["git", "rev-parse", "--git-common-dir"])
        for c in runner.commands
    )


def test_settings_defaults_and_idle_floor(wc):
    cfg = wc.settings({})
    assert cfg["idle_days"] == 7
    assert cfg["evidence_repo"] == "IronbellyOrg/run-evidence"
    assert wc.settings({"WORKTREE_CLEANUP_IDLE_DAYS": "3"})["idle_days"] == 3
    assert wc.settings({"WORKTREE_CLEANUP_IDLE_DAYS": "x"})["idle_days"] == 7


# --- refusals that need no working folder ---------------------------------------

BANNED = [
    # --force or -f on the removals, in every spelling and position
    ["git", "worktree", "remove", "--force", "/x"],
    ["git", "worktree", "remove", "-f", "/x"],
    ["git", "worktree", "remove", "-f", "-f", "/x"],
    ["git", "worktree", "remove", "--forc", "/x"],
    ["git", "worktree", "remove", "-fd", "/x"],
    ["git", "worktree", "remove", "/x", "--force"],
    ["orca", "worktree", "rm", "--worktree", "id:1", "--force"],
    ["orca", "worktree", "rm", "--worktree", "id:1", "-f"],
    ["orca", "worktree", "rm", "-f", "--worktree", "id:1"],
    ["orca", "worktree", "rm", "--force", "--worktree", "id:1"],
    ["orca", "worktree", "rm", "--worktree", "id:1", "--forc"],
    ["orca", "worktree", "rm", "--worktree", "id:1", "-fy"],
    ["orca", "worktree", "rm", "--worktree", "id:1", "--force=true"],
    ["orca", "worktree", "rm", "--worktree", "--force"],
    # git branch -D in every spelling, and the list form that used to return early
    ["git", "branch", "-D", "topic"],
    ["git", "branch", "-Dq", "topic"],
    ["git", "branch", "-df", "topic"],
    ["git", "branch", "-d", "-f", "topic"],
    ["git", "branch", "--delete", "--force", "topic"],
    ["git", "branch", "--del", "topic"],
    ["git", "branch", "--list", "-D", "x"],
    ["git", "branch", "-d", "topic", "other"],
    # rm, prune and clean
    ["rm", "-rf", "/x"],
    ["rm", "file"],
    ["/bin/rm", "file"],
    ["git", "worktree", "prune"],
    ["git", "worktree", "prune", "--dry-run"],
    ["git", "clean", "-fdx"],
    ["git", "clean", "-fx"],
    ["git", "clean", "-f", "-x", "--", "a"],
    # an option that writes a file from a read verb, also shortened
    ["git", "log", "--output=/tmp/x"],
    ["git", "log", "--outp=/tmp/x"],
    ["git", "diff", "--output=/tmp/x"],
    ["git", "diff", "--ext-diff"],
    ["git", "status", "-zu"],
    ["git", "log", "-n1"],
    # git options that change its behaviour
    ["git", "-c", "core.sshCommand=x", "status"],
    ["git", "-c", HELPER, "status"],
    ["git", "--git-dir=/x", "status"],
    ["git", "-C"],
    ["git"],
]


@pytest.mark.parametrize("argv", BANNED, ids=[" ".join(a) for a in BANNED])
def test_banned_shapes_are_refused_before_any_process_starts(
    wc, never_run_runner, argv
):
    with pytest.raises(wc.RefusedCommand):
        never_run_runner.check_allowed(argv)
    with pytest.raises(wc.RefusedCommand):
        never_run_runner.run(argv)
    assert never_run_runner.commands == []


UNLISTED = [
    ["git", "reset", "--hard"],
    ["git", "reset"],
    ["git", "checkout", "topic"],
    ["git", "stash"],
    ["git", "merge", "topic"],
    ["git", "show", "HEAD"],
    ["mv", "a", "b"],
    ["find", ".", "-delete"],
    ["gh", "pr", "merge", "1", "--repo", REPO],
    ["gh", "pr", "create", "--repo", REPO],
    ["gh", "api", "repos/o/r"],
    ["orca", "automations", "create"],
    ["orca", "worktree", "create", "--name", "x"],
    ["python3", "-c", "print(1)"],
]


@pytest.mark.parametrize("argv", UNLISTED, ids=[" ".join(a) for a in UNLISTED])
def test_unlisted_commands_are_refused(wc, never_run_runner, argv):
    with pytest.raises(wc.RefusedCommand):
        never_run_runner.check_allowed(argv)
    with pytest.raises(wc.RefusedCommand):
        never_run_runner.run(argv)
    assert never_run_runner.commands == []


# --- the push to the evidence repo ----------------------------------------------


@pytest.fixture
def evidence(tmp_path):
    path = tmp_path / "evidence"
    path.mkdir()
    return path


PUSH_REFUSED = [
    ["push", "--delete", "origin", "topic"],
    ["push", "-d", "origin", "topic"],
    ["push", "-df", "origin", "topic"],
    ["push", "-fd", "origin", "topic"],
    ["push", "--dele", "origin", "topic"],
    ["push", "--del", "origin", "topic"],
    ["push", "--force", "origin", "main"],
    ["push", "--forc", "origin", "main"],
    ["push", "-f", "origin", "main"],
    ["push", "--force-with-lease", "origin", "main"],
    ["push", "--force-if-includes", "origin", "main"],
    ["push", "--mirror", "origin"],
    ["push", "--prune", "origin", "main"],
    ["push", "--all", "origin"],
    ["push", "-o", "x", "origin", "main"],
    ["push", "origin", "+main"],
    ["push", "origin", "main:main"],
    ["push", "origin", ":topic"],
    ["push", "origin", "+main:main"],
    ["push", "origin", "HEAD:refs/heads/x"],
    ["push", "origin", "refs/heads/*"],
    ["push", "upstream", "main"],
    ["push", "https://example.invalid/r.git", "main"],
    ["push", "origin"],
    ["push", "origin", "main", "other"],
    ["push"],
]


@pytest.mark.parametrize("tail", PUSH_REFUSED, ids=[" ".join(t) for t in PUSH_REFUSED])
def test_push_shapes_are_refused_inside_the_evidence_clone(
    wc, runner_cls, evidence, tail
):
    runner = runner_cls(evidence_dir=str(evidence))
    with pytest.raises(wc.RefusedCommand):
        runner.run(["git", *tail], cwd=str(evidence))
    with pytest.raises(wc.RefusedCommand):
        runner.run(["git", "-c", HELPER, *tail], cwd=str(evidence))
    assert runner.commands == []


def test_push_is_allowed_only_in_its_exact_shape_inside_the_evidence_clone(
    wc, runner_cls, evidence, tmp_path
):
    other = tmp_path / "other"
    other.mkdir()
    r = runner_cls(evidence_dir=str(evidence))
    r.check_allowed(["git", "push", "origin", "main"], cwd=str(evidence))
    r.check_allowed(
        ["git", "push", "--porcelain", "origin", "topic/a-1"], cwd=str(evidence)
    )
    r.check_allowed(["git", "-c", HELPER, "push", "origin", "main"], cwd=str(evidence))
    r.check_allowed(["git", "-C", str(evidence), "push", "origin", "main"])
    # not the evidence clone, or no working folder at all
    with pytest.raises(wc.RefusedCommand):
        r.check_allowed(["git", "push", "origin", "main"], cwd=str(other))
    with pytest.raises(wc.RefusedCommand):
        r.check_allowed(["git", "push", "origin", "main"])
    with pytest.raises(wc.RefusedCommand):
        r.check_allowed(
            ["git", "-C", str(other), "push", "origin", "main"], cwd=str(evidence)
        )
    # the credential helper is the only -c value, and only on a push
    with pytest.raises(wc.RefusedCommand):
        r.check_allowed(
            ["git", "-c", "core.sshCommand=x", "push", "origin", "main"],
            cwd=str(evidence),
        )
    with pytest.raises(wc.RefusedCommand):
        r.check_allowed(["git", "-c", HELPER, "fetch", "origin"], cwd=str(evidence))


PUSH = ["push", "origin", "main"]


def test_a_relative_dash_c_option_is_joined_onto_the_running_folder_not_the_process_folder(
    wc, runner_cls, evidence, tmp_path, monkeypatch
):
    """``git -C .`` means the running folder; it must not mean the folder of this process."""
    other = tmp_path / "other"
    other.mkdir()
    (evidence / "sub").mkdir()
    r = runner_cls(evidence_dir=str(evidence))
    monkeypatch.chdir(evidence)  # the process sits inside the evidence clone
    # the running folder is somewhere else: a relative -C must stay there and be refused
    for tail in (["-C", "."], ["-C", "sub"], ["-C", "sub", "-C", ".."]):
        with pytest.raises(wc.RefusedCommand):
            r.check_allowed(["git", *tail, *PUSH], cwd=str(other))
    # a chain starting from an absolute folder elsewhere stays elsewhere
    with pytest.raises(wc.RefusedCommand):
        r.check_allowed(["git", "-C", str(other), "-C", ".", *PUSH], cwd=str(evidence))
    with pytest.raises(wc.RefusedCommand):
        r.check_allowed(["git", "-C", str(other), "-C", "..", *PUSH], cwd=str(evidence))


def test_chained_dash_c_values_are_joined_one_after_the_other(
    wc, runner_cls, evidence, tmp_path, monkeypatch
):
    other = tmp_path / "other"
    other.mkdir()
    (evidence / "sub").mkdir()
    r = runner_cls(evidence_dir=str(evidence))
    monkeypatch.chdir(other)  # the process is outside the clone
    # relative to the running folder (the clone): the clone itself, so allowed
    for tail in (
        ["-C", "."],
        ["-C", "sub", "-C", ".."],
        ["-C", str(evidence), "-C", "."],
    ):
        r.check_allowed(["git", *tail, *PUSH], cwd=str(evidence))
    # one step up from the clone is not the clone
    with pytest.raises(wc.RefusedCommand):
        r.check_allowed(["git", "-C", "..", *PUSH], cwd=str(evidence))
    with pytest.raises(wc.RefusedCommand):
        r.check_allowed(
            ["git", "-C", "sub", "-C", "..", "-C", "..", *PUSH], cwd=str(evidence)
        )
    # with no running folder the process folder is the base, as it is when git starts
    with pytest.raises(wc.RefusedCommand):
        r.check_allowed(["git", "-C", ".", *PUSH])
    monkeypatch.chdir(evidence)
    r.check_allowed(["git", "-C", ".", *PUSH])


def test_other_evidence_clone_verbs_have_one_exact_shape(
    wc, runner_cls, evidence, tmp_path
):
    other = tmp_path / "other"
    other.mkdir()
    r = runner_cls(evidence_dir=str(evidence))
    ok = [
        ["git", "fetch", "origin"],
        ["git", "fetch", "--quiet", "origin"],
        ["git", "add", "--", "worktree-a/manifest.md", "worktree-a/part-01"],
        ["git", "commit", "-m", "save worktree-a"],
        ["git", "commit", "--quiet", "-m", "save worktree-a"],
        ["git", "rebase", "origin/main"],
        ["git", "rebase", "--abort"],
    ]
    for argv in ok:
        r.check_allowed(argv, cwd=str(evidence))
        with pytest.raises(wc.RefusedCommand):
            r.check_allowed(argv, cwd=str(other))
    refused = [
        ["git", "fetch", "--all"],
        ["git", "fetch", "--prune", "origin"],
        ["git", "fetch", "upstream"],
        ["git", "add", "-A"],
        ["git", "add", "."],
        ["git", "add", "--", ":(top)x"],
        ["git", "add", "--", "../x"],
        ["git", "commit", "-a", "-m", "x"],
        ["git", "commit", "--amend", "-m", "x"],
        ["git", "commit", "-m", "-x"],
        ["git", "rebase", "-i", "origin/main"],
        ["git", "rebase", "--interactive", "origin/main"],
        ["git", "rebase", "main"],
    ]
    for argv in refused:
        with pytest.raises(wc.RefusedCommand):
            r.check_allowed(argv, cwd=str(evidence))


def test_clone_only_into_the_evidence_folder(wc, runner_cls, evidence, tmp_path):
    r = runner_cls(evidence_dir=str(evidence))
    r.check_allowed(["git", "clone", f"https://github.com/{REPO}.git", str(evidence)])
    with pytest.raises(wc.RefusedCommand):
        r.check_allowed(
            ["git", "clone", f"https://github.com/{REPO}.git", str(tmp_path / "x")]
        )
    with pytest.raises(wc.RefusedCommand):
        r.check_allowed(
            [
                "git",
                "clone",
                "--mirror",
                f"https://github.com/{REPO}.git",
                str(evidence),
            ]
        )
    with pytest.raises(wc.RefusedCommand):
        r.check_allowed(["git", "clone", "--depth", "1", "u", str(evidence)])
    with pytest.raises(wc.RefusedCommand):
        runner_cls().check_allowed(["git", "clone", "u", "/e"])


# --- gh, orca, the landed check -----------------------------------------------------


def test_gh_has_three_shapes_and_an_explicit_repo_of_our_owners(wc, never_run_runner):
    ok = [
        [
            "gh",
            "pr",
            "list",
            "--repo",
            REPO,
            "--head",
            "b",
            "--state",
            "all",
            "--json",
            "number",
            "--limit",
            "5",
        ],
        ["gh", "pr", "view", "700", "--repo", REPO, "--json", "state,mergedAt"],
        ["gh", "issue", "view", "5", "--repo", "ironbellygroup/other"],
    ]
    for argv in ok:
        never_run_runner.check_allowed(argv)
    refused = [
        ["gh", "pr", "list", "--head", "x"],
        ["gh", "pr", "list", "--repo", REPO, "--repo", REPO],
        ["gh", "pr", "list", "--repo", "SuperClaude-Org/SuperClaude_Framework"],
        ["gh", "pr", "list", "--repo", REPO, "--web"],
        ["gh", "pr", "list", "--repo", REPO, "-R", "o/r"],
        ["gh", "pr", "list", "--repo", "bad repo"],
        ["gh", "pr", "view", "--repo", REPO],
        ["gh", "pr", "view", "x1", "--repo", REPO],
        ["gh", "pr", "view", "7", "8", "--repo", REPO],
        ["gh", "issue", "list", "--repo", REPO],
        ["gh", "repo", "clone", REPO, "/e"],
        ["gh", "pr", "list", "--repo"],
    ]
    for argv in refused:
        with pytest.raises(wc.RefusedCommand):
            never_run_runner.check_allowed(argv)


ORCA_OK = [
    ["orca", "repo", "list", "--json"],
    ["orca", "repo", "list"],
    ["orca", "worktree", "list", "--json"],
    ["orca", "worktree", "ps", "--json"],
    ["orca", "reference", "list", "--worktree", "id:1", "--json"],
    ["orca", "terminal", "list", "--worktree", "id:1"],
    ["orca", "worktree", "rm", "--worktree", "id:1"],
]


@pytest.mark.parametrize("argv", ORCA_OK, ids=[" ".join(a) for a in ORCA_OK])
def test_orca_allowed_shapes(never_run_runner, argv):
    never_run_runner.check_allowed(argv)


def test_orca_other_shapes_are_refused(wc, never_run_runner):
    for argv in (
        ["orca", "repo", "list", "--all"],
        ["orca", "worktree", "ps", "--watch"],
        ["orca", "terminal", "list"],
        ["orca", "terminal", "list", "--worktree", "id:1", "--all"],
        ["orca", "worktree", "rm"],
        ["orca", "worktree", "rm", "--worktree", "id:1", "extra"],
        ["orca", "worktree"],
        ["orca"],
    ):
        with pytest.raises(wc.RefusedCommand):
            never_run_runner.check_allowed(argv)


def test_orca_terminal_close_needs_authorization(wc, never_run_runner):
    argv = ["orca", "terminal", "close", "--worktree", "id:7", "--all"]
    with pytest.raises(wc.RefusedCommand):
        never_run_runner.check_allowed(argv)
    never_run_runner.authorize_close("id:7")
    never_run_runner.check_allowed(argv)
    # another worktree, a missing --all or an extra option is still refused
    for other in (
        ["orca", "terminal", "close", "--worktree", "id:8", "--all"],
        ["orca", "terminal", "close", "--worktree", "id:7"],
        ["orca", "terminal", "close", "--worktree", "id:7", "--all", "--force"],
        ["orca", "terminal", "close", "--all", "--worktree", "id:7"],
    ):
        with pytest.raises(wc.RefusedCommand):
            never_run_runner.check_allowed(other)


def test_landed_check_only_from_the_lookup_locations(wc, never_run_runner):
    never_run_runner.check_allowed(["bash", LANDED, "12"])
    never_run_runner.check_allowed([LANDED, "12"])
    elsewhere = "/tmp/evil/sc-closeout-protocol/scripts/branch-landed.sh"
    for argv in (
        ["bash", elsewhere, "12"],
        [elsewhere, "12"],
        ["bash", "/tmp/evil.sh", "12"],
        ["bash", LANDED, "abc"],
        ["bash", LANDED, "12", "13"],
        ["bash", LANDED],
        ["bash", "-c", "echo hi"],
        ["bash", LANDED + "/../../../x.sh", "12"],
    ):
        with pytest.raises(wc.RefusedCommand):
            never_run_runner.check_allowed(argv)


def test_default_lookup_locations_follow_the_recorded_order(wc):
    paths = wc.default_landed_paths()
    assert len(paths) == 3
    tail = "skills/sc-closeout-protocol/scripts/branch-landed.sh"
    assert paths[0].endswith("/.claude/" + tail)
    assert paths[1].endswith("/.claude/" + tail)
    assert paths[2].endswith("/src/superclaude/" + tail)
    assert paths[0] != paths[1]


# --- git clean ----------------------------------------------------------------------


def test_git_clean_only_for_registered_saved_paths(wc, never_run_runner, tmp_path):
    wt = tmp_path / "wt"
    wt.mkdir()
    argv = ["xargs", "-0", "git", "clean", "-f", "-x", "--"]
    never_run_runner.register_saved(str(wt), [".dev/a b.txt", ".dev/c.log"])
    ok = b".dev/a b.txt\0.dev/c.log\0"
    never_run_runner.check_allowed(argv, cwd=str(wt), stdin=ok)
    with pytest.raises(wc.RefusedCommand):
        never_run_runner.check_allowed(argv, cwd=str(wt), stdin=ok + b"other.txt\0")
    with pytest.raises(wc.RefusedCommand):
        never_run_runner.check_allowed(argv, cwd=str(wt), stdin=b"")
    with pytest.raises(wc.RefusedCommand):
        never_run_runner.check_allowed(argv, cwd=str(tmp_path), stdin=ok)
    for other in (
        ["xargs", "-0", "git", "clean", "-f", "-d", "-x", "--"],
        ["xargs", "-0", "git", "clean", "-fx", "--"],
        ["xargs", "-0", "git", "clean", "-f", "-x"],
        ["xargs", "git", "clean", "-f", "-x", "--"],
        ["xargs", "-0", "rm", "--"],
    ):
        with pytest.raises(wc.RefusedCommand):
            never_run_runner.check_allowed(other, cwd=str(wt), stdin=ok)


# --- read verbs and named write verbs: exact shapes ------------------------------------


def test_read_and_named_write_shapes_are_allowed(wc, never_run_runner):
    ok = [
        ["git", "status", "--porcelain", "-z", "--ignored"],
        ["git", "status", "--untracked-files=all"],
        ["git", "worktree", "list"],
        ["git", "worktree", "list", "--porcelain"],
        ["git", "worktree", "remove", "/some/path"],
        ["git", "branch", "-d", "topic"],
        ["git", "branch", "--list", "topic"],
        ["git", "branch", "--show-current"],
        ["git", "remote", "get-url", "origin"],
        ["git", "config", "--get", "remote.origin.url"],
        ["git", "rev-parse", "HEAD"],
        ["git", "rev-parse", "--verify", "HEAD"],
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        ["git", "-C", "/some/wt", "rev-parse", "--show-toplevel"],
        ["git", "log", "-1", "--format=%H", "HEAD"],
        ["git", "log", "--format=%H", "a..b", "--", "p"],
        ["git", "ls-files", "-z", "--others", "--ignored", "--exclude-standard"],
        ["git", "ls-tree", "-r", "--name-only", "HEAD"],
        ["git", "merge-base", "--is-ancestor", "a", "b"],
        ["git", "rev-list", "--count", "a..b"],
        ["git", "diff", "--quiet", "HEAD", "--", "p"],
        ["tar", "-tzf", "/x/ignored.tar.gz"],
        ["bash", LANDED, "12"],
    ]
    for argv in ok:
        never_run_runner.check_allowed(argv)
    for argv in (
        ["tar", "-xzf", "/x/a.tar.gz"],
        ["tar", "-tzf", "-x"],
        ["tar", "-tzf"],
        ["git", "status", "--short"],
        ["git", "status", "x"],
        ["git", "worktree", "list", "--verbose"],
        ["git", "worktree", "remove"],
        ["git", "worktree", "remove", "-x"],
        ["git", "worktree", "add", "/x"],
        ["git", "remote", "add", "o", "u"],
        ["git", "remote", "get-url"],
        ["git", "config", "--set", "a", "b"],
        ["git", "config", "user.name", "x"],
        ["git", "merge-base", "a"],
        ["git", "rev-list", "a", "--"],
        ["git", "log", "--format"],
        ["git", "rev-parse", "+x"],
        ["git", "rev-parse", ":/x"],
    ):
        with pytest.raises(wc.RefusedCommand):
            never_run_runner.check_allowed(argv)


# --- recording ---------------------------------------------------------------


def test_every_allowed_command_is_recorded_with_its_working_folder(
    runner_cls, tmp_path
):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    runner = runner_cls()
    res = runner.run(["git", "rev-parse", "--git-dir"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert [c.argv for c in runner.commands] == [["git", "rev-parse", "--git-dir"]]
    assert runner.commands[0].cwd == str(tmp_path)


# --- the file itself ------------------------------------------------------------


def test_only_standard_library_imports():
    tree = ast.parse(_source())
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0:
            names.add((node.module or "").split(".")[0])
    assert names, "no imports found"
    assert names <= set(sys.stdlib_module_names), sorted(
        names - set(sys.stdlib_module_names)
    )


def test_no_call_that_deletes_a_file_and_no_rm_command():
    tree = ast.parse(_source())
    banned_attrs = {"remove", "unlink", "rmtree", "rmdir", "removedirs"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            assert node.func.attr not in banned_attrs, ast.dump(node.func)
        # no argument list that starts with the string "rm"
        if isinstance(node, ast.List) and node.elts:
            first = node.elts[0]
            if isinstance(first, ast.Constant) and first.value == "rm":
                raise AssertionError("an argument list starts with rm")


def test_subprocess_is_started_only_inside_execute():
    tree = ast.parse(_source())
    owners = []
    for fn in ast.walk(tree):
        if isinstance(fn, ast.FunctionDef):
            for node in ast.walk(fn):
                if (
                    isinstance(node, ast.Attribute)
                    and isinstance(node.value, ast.Name)
                    and node.value.id == "subprocess"
                    and node.attr
                    in {"run", "Popen", "call", "check_call", "check_output"}
                ):
                    owners.append(fn.name)
    assert owners and set(owners) == {"_execute"}


def test_apache_notice_block_and_provenance_pointer_are_at_the_top():
    head = "\n".join(_source().splitlines()[:8])
    assert "Jay Wedgeworth" in head
    assert "Apache License, Version 2.0" in head
    assert "scripts/worktree_cleanup_PROVENANCE.md" in head


def test_the_file_never_names_a_credential_file():
    text = _source()
    assert "hosts.yml" not in text
    assert "~/.env" not in text
    assert "'.env'" not in text and '".env"' not in text


def test_no_dash_characters_in_the_script_and_its_tests():
    # Built from code points so these files hold no such character themselves.
    for path in (
        SCRIPT,
        *SCRIPT.parents[1].joinpath("tests", "worktree_cleanup").glob("*.py"),
    ):
        text = path.read_text(encoding="utf-8")
        assert chr(0x2013) not in text and chr(0x2014) not in text, path


# --- the credential goes only where the plan allows it ------------------------------------


def _env(runner, argv, monkeypatch):
    monkeypatch.setenv("GH_TOKEN", "placeholder-not-a-secret")
    monkeypatch.setenv("GITHUB_TOKEN", "placeholder-not-a-secret")
    return runner._env_for(argv)


@pytest.mark.parametrize(
    "argv",
    [
        ["git", "status", "--porcelain"],
        ["git", "worktree", "remove", "/x"],
        ["git", "branch", "-d", "topic"],
        ["git", "fetch", "origin"],
        ["git", "clone", "u", "/e"],
        ["git", "commit", "-m", "x"],
        ["git", "-C", "/e", "fetch", "origin"],
        ["orca", "worktree", "ps", "--json"],
        ["orca", "terminal", "close", "--worktree", "id:1", "--all"],
        ["tar", "-tzf", "/x/a.tar.gz"],
        ["xargs", "-0", "git", "clean", "-f", "-x", "--"],
    ],
    ids=lambda a: " ".join(a),
)
def test_token_is_not_given_to_other_children(runner_cls, monkeypatch, argv):
    env = _env(runner_cls(), argv, monkeypatch)
    assert "GH_TOKEN" not in env and "GITHUB_TOKEN" not in env


@pytest.mark.parametrize(
    "argv",
    [
        ["gh", "pr", "list", "--repo", REPO],
        ["bash", LANDED, "5"],
        [LANDED, "5"],
        ["git", "push", "origin", "main"],
        ["git", "-c", HELPER, "push", "origin", "main"],
        ["git", "-C", "/e", "push", "origin", "main"],
    ],
    ids=lambda a: " ".join(a),
)
def test_token_is_given_to_gh_the_landed_check_and_git_push(
    runner_cls, monkeypatch, argv
):
    env = _env(runner_cls(), argv, monkeypatch)
    assert env.get("GH_TOKEN") == "placeholder-not-a-secret"
    assert env.get("GITHUB_TOKEN") == "placeholder-not-a-secret"


def test_literal_pathspecs_only_for_the_clean_command(runner_cls, monkeypatch):
    r = runner_cls()
    assert (
        _env(r, ["xargs", "-0", "git", "clean", "-f", "-x", "--"], monkeypatch)[
            "GIT_LITERAL_PATHSPECS"
        ]
        == "1"
    )
    assert "GIT_LITERAL_PATHSPECS" not in _env(r, ["git", "status"], monkeypatch)


def test_external_diff_hook_is_removed_from_every_child(runner_cls, monkeypatch):
    monkeypatch.setenv("GIT_EXTERNAL_DIFF", "x")
    env = runner_cls()._env_for(["git", "diff", "--quiet"])
    assert "GIT_EXTERNAL_DIFF" not in env
