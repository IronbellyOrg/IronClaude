"""Tests for ``stage-plan`` in path mode (T-01 path mode, T-23, T-26, T-27).

Path mode plans an add or a commit of paths the person named (``/sc:git add`` and
``/sc:git commit <path>...``), or of the index as staged (a pathless commit). Every
case runs on a real temporary repository. The plan reads only: the helper writes no
ref, no index entry and no file, and the message file and the pathspec file are the
agent's to write outside the work tree (DD-4).
"""

from __future__ import annotations

import hashlib
import importlib
import json
import os
import re
import subprocess
import sys
import tempfile

import pytest

from .conftest import SCRIPTS, SHA40, LedgerBuilder, SidecarBuilder, git_in


@pytest.fixture
def vcs(scripts_dir):
    return importlib.import_module("vcs")


@pytest.fixture
def plan(vcs):
    """``plan(repo, *paths)`` runs the verb; no path at all plans a pathless commit."""

    def run(repo, *paths):
        return vcs.run_stage_plan(str(repo.work), list(paths) if paths else None)

    return run


def skipped_map(result):
    return {item["path"]: item["why"] for item in result["skipped"]}


def masked(text):
    """``text`` with the random token of the temporary file names removed.

    ``message_path`` and the default pathspec file carry a random token, so that another
    user of a shared temporary folder cannot guess the names; everything else in a plan is
    byte-identical on the same inputs."""
    return re.sub(
        r"(vcs-(?:message|pathspec)-[0-9a-f]{16})-[0-9a-f]{16}", r"\1-TOKEN", text
    )


def pathspec_entries(result):
    content = result["pathspec_file"]["content"]
    assert content.endswith("\0")
    return content[:-1].split("\0")


# --- literal paths (T-23) ----------------------------------------------------------------
LITERAL_NAMES = [":(glob)*", "-nfile.txt", "has space.txt", "d/how to merge.md"]


def test_names_with_pathspec_magic_are_passed_literally(repo, plan):
    for name in LITERAL_NAMES:
        repo.write(name, "x\n")
    repo.write("other.txt", "not named\n")
    result = plan(repo, *LITERAL_NAMES)
    assert result["status"] == "ok"
    assert result["commit_paths"] == sorted(LITERAL_NAMES)
    assert result["skipped"] == []
    assert result["s_count"] == 4
    assert pathspec_entries(result) == sorted(LITERAL_NAMES)
    assert "other.txt" not in result["commit_paths"]


def test_the_plan_is_deterministic_and_order_independent(repo, plan, vcs):
    for name in LITERAL_NAMES:
        repo.write(name, "x\n")
    first = plan(repo, *LITERAL_NAMES)
    second = plan(repo, *reversed(LITERAL_NAMES))
    assert masked(vcs.emit_text(first)) == masked(vcs.emit_text(second))


def test_repeated_and_dotted_forms_of_one_path_count_once(repo, plan):
    repo.write("a.txt", "x\n")
    result = plan(repo, "a.txt", "./a.txt", "a.txt")
    assert result["commit_paths"] == ["a.txt"]
    assert result["s_count"] == 1


def test_the_pathspec_file_hash_is_the_sha256_of_its_content(repo, plan):
    repo.write("a.txt", "x\n")
    repo.write("b.txt", "x\n")
    result = plan(repo, "b.txt", "a.txt")
    file = result["pathspec_file"]
    assert file["content"] == "a.txt\0b.txt\0"
    assert file["sha256"] == hashlib.sha256(file["content"].encode()).hexdigest()
    assert result["add_argv"][2] == f"--pathspec-from-file={file['path']}"


def test_the_temporary_files_are_named_outside_the_work_tree_and_not_written(
    repo, plan
):
    repo.write("a.txt", "x\n")
    result = plan(repo, "a.txt")
    work = os.path.realpath(repo.work)
    for path in (result["message_path"], result["pathspec_file"]["path"]):
        assert os.path.isabs(path)
        assert not os.path.realpath(path).startswith(work + os.sep)
        assert not os.path.exists(path)  # the helper never writes them (DD-4)


# --- deletions and absent paths ------------------------------------------------------------
def test_a_deletion_is_staged(repo, plan):
    repo.write("gone.txt", "x\n")
    repo.commit("add gone")
    os.remove(repo.work / "gone.txt")
    result = plan(repo, "gone.txt")
    assert result["status"] == "ok"
    assert result["commit_paths"] == ["gone.txt"]
    assert result["skipped"] == []


def test_a_path_gone_from_index_but_present_in_head_is_a_deletion(repo, plan):
    repo.write("gone.txt", "x\n")
    repo.commit("add gone")
    repo.git("rm", "-q", "--cached", "gone.txt")
    os.remove(repo.work / "gone.txt")
    assert plan(repo, "gone.txt")["commit_paths"] == ["gone.txt"]


def test_a_path_absent_from_all_three_places_is_skipped(repo, plan):
    result = plan(repo, "never-existed.txt")
    assert skipped_map(result) == {"never-existed.txt": "absent"}
    assert result["status"] == "nothing"
    assert result["commit_paths"] == []


# --- the path rules --------------------------------------------------------------------------
def test_a_path_under_a_gitlink_is_skipped(submodule_repo, plan):
    repo = submodule_repo
    repo.write("real.txt", "x\n")
    result = plan(repo, "libs/lib/lib.txt", "libs/lib", "real.txt")
    assert skipped_map(result) == {"libs/lib/lib.txt": "gitlink", "libs/lib": "gitlink"}
    assert result["commit_paths"] == ["real.txt"]


def test_a_gitlink_staged_in_the_index_only_is_skipped(submodule_repo, plan):
    repo = submodule_repo
    sub = repo.work / repo.sub_path
    git_in(sub, "config", "user.name", "t")
    git_in(sub, "config", "user.email", "t@example.invalid")
    (sub / "more.txt").write_text("more\n", encoding="utf-8")
    git_in(sub, "add", "-A")
    git_in(sub, "commit", "-q", "-m", "more")
    repo.git("add", "--", repo.sub_path)  # the pointer change is now staged
    result = plan(repo, repo.sub_path)
    assert skipped_map(result) == {repo.sub_path: "gitlink"}


def test_a_path_in_the_extra_gitlink_list_is_skipped(repo, vcs):
    plan_mod = importlib.import_module("vcs_plan")
    repo.write("q0mod/file.txt", "x\n")
    result = plan_mod.plan_stage(
        plan_mod.GitRunner(repo.work), ["q0mod/file.txt"], extra_gitlinks=["q0mod"]
    )
    assert skipped_map(result) == {"q0mod/file.txt": "gitlink"}


def test_gitignored_paths_are_skipped(repo, plan):
    repo.write(".gitignore", "*.log\nbuild/\n")
    repo.commit("ignore")
    repo.write("x.log", "x\n")
    repo.write("build/out.txt", "x\n")
    repo.write("keep.txt", "x\n")
    result = plan(repo, "x.log", "build/out.txt", "keep.txt")
    assert skipped_map(result) == {"x.log": "ignored", "build/out.txt": "ignored"}
    assert result["commit_paths"] == ["keep.txt"]


def test_a_tracked_file_that_matches_an_ignore_rule_is_not_skipped(repo, plan):
    repo.write(".gitignore", "*.log\n")
    repo.commit("ignore")
    repo.write("kept.log", "v1\n")
    repo.git("add", "-f", "--", "kept.log")
    repo.git("commit", "-q", "-m", "force add")
    repo.write("kept.log", "v2\n")
    assert plan(repo, "kept.log")["commit_paths"] == ["kept.log"]


def test_a_path_under_the_legacy_run_folder_is_skipped(repo, plan):
    repo.write(".dev/implement/run-1/ledger.md", "x\n")
    repo.write("a.txt", "x\n")
    result = plan(repo, ".dev/implement/run-1/ledger.md", "a.txt")
    assert skipped_map(result) == {
        ".dev/implement/run-1/ledger.md": "legacy-run-folder"
    }
    assert result["commit_paths"] == ["a.txt"]
    assert ".dev/implement" not in json.dumps(
        result["add_argv"] + result["commit_argv"]
    )
    assert ".dev/implement" not in result["pathspec_file"]["content"]


def test_the_legacy_run_folder_is_skipped_even_when_it_is_not_ignored(repo, plan):
    # The folder is not gitignored: the rule must hold with no ignore file at all.
    assert not (repo.work / ".gitignore").exists()
    repo.write(".dev/implement/run-2/commits.md", "x\n")
    result = plan(repo, ".dev/implement/run-2/commits.md")
    assert skipped_map(result) == {
        ".dev/implement/run-2/commits.md": "legacy-run-folder"
    }
    assert result["status"] == "nothing"


def test_legacy_run_folder_rule_wins_over_the_ignore_rule(repo, plan):
    repo.write(".gitignore", ".dev/implement/\n")
    repo.commit("ignore")
    repo.write(".dev/implement/run-3/ledger.md", "x\n")
    result = plan(repo, ".dev/implement/run-3/ledger.md")
    assert skipped_map(result) == {
        ".dev/implement/run-3/ledger.md": "legacy-run-folder"
    }


def test_a_folder_that_only_looks_like_the_run_folder_is_not_skipped(repo, plan):
    repo.write(".dev/implementation/notes.md", "x\n")
    repo.write(".dev/implement-notes.md", "x\n")
    result = plan(repo, ".dev/implementation/notes.md", ".dev/implement-notes.md")
    assert result["skipped"] == []


@pytest.mark.parametrize(
    "bad", ["/etc/passwd", "../escape.txt", "a/../../escape.txt", "a/../b.txt"]
)
def test_absolute_and_dotdot_paths_are_refused_as_outside_repo(repo, plan, bad):
    repo.write("a.txt", "x\n")
    result = plan(repo, bad, "a.txt")
    assert result["status"] == "refused"
    assert result["reason"] == "outside-repo"
    assert skipped_map(result)[bad] == "outside-repo"
    assert result["add_argv"] == [] and result["commit_argv"] == []


def test_a_path_through_a_symlink_to_the_outside_is_refused(repo, plan, tmp_path):
    outside = tmp_path / "elsewhere"
    outside.mkdir()
    (outside / "f.txt").write_text("x\n", encoding="utf-8")
    os.symlink(outside, repo.work / "link")
    result = plan(repo, "link/f.txt")
    assert result["status"] == "refused"
    assert result["reason"] == "outside-repo"
    assert skipped_map(result) == {"link/f.txt": "outside-repo"}


def test_a_symlink_that_is_itself_the_path_is_staged_as_a_link(repo, plan, tmp_path):
    os.symlink(tmp_path, repo.work / "link")
    result = plan(repo, "link")
    assert result["status"] == "ok"
    assert result["commit_paths"] == ["link"]


def test_a_dev_copy_path_is_refused_and_named(repo, plan):
    repo.write(".claude/cache/sc-recommend-lookup.yaml", "x\n")
    result = plan(repo, ".claude/cache/sc-recommend-lookup.yaml")
    assert result["status"] == "refused"
    assert result["reason"] == "dev-copy-path"
    assert skipped_map(result) == {
        ".claude/cache/sc-recommend-lookup.yaml": "dev-copy-path"
    }
    assert ".claude/cache/sc-recommend-lookup.yaml" in result["detail"]


def test_a_tracked_dev_copy_path_is_refused_and_suggests_no_command(repo, plan):
    # T-27: tracking a file is not authority to stage it.
    repo.write(".claude/skills/x/SKILL.md", "v1\n")
    repo.commit("track the dev copy")
    repo.write(".claude/skills/x/SKILL.md", "v2\n")
    result = plan(repo, ".claude/skills/x/SKILL.md", "README.md")
    assert result["status"] == "refused"
    assert result["reason"] == "dev-copy-path"
    assert ".claude/skills/x/SKILL.md" in result["detail"]
    assert "git" not in result["detail"].lower()
    assert result["add_argv"] == [] and result["commit_argv"] == []
    assert result["pathspec_file"] is None and result["message_path"] is None


def test_an_ignored_dev_copy_path_is_still_refused_not_dropped(repo, plan):
    # The project ignores the dev-copy folder except settings.json.
    repo.write(".gitignore", ".claude/*\n!.claude/settings.json\n")
    repo.commit("ignore")
    repo.write(".claude/cache/sc-recommend-lookup.yaml", "x\n")
    repo.write(".claude/settings.json", "{}\n")
    refused = plan(repo, ".claude/cache/sc-recommend-lookup.yaml")
    assert refused["status"] == "refused"
    assert refused["reason"] == "dev-copy-path"
    assert plan(repo, ".claude/settings.json")["commit_paths"] == [
        ".claude/settings.json"
    ]


def test_the_dev_settings_file_is_allowed(repo, plan):
    repo.write(".claude/settings.json", "{}\n")
    assert plan(repo, ".claude/settings.json")["commit_paths"] == [
        ".claude/settings.json"
    ]


def test_a_nested_claude_folder_is_not_the_dev_copy(repo, plan):
    repo.write("docs/.claude/notes.md", "x\n")
    assert plan(repo, "docs/.claude/notes.md")["status"] == "ok"


@pytest.mark.parametrize(
    "name", ["a,b.txt", "line\nbreak.txt", "bell\x07.txt", "tab\tx.txt"]
)
def test_a_name_the_ledger_cannot_carry_is_refused(repo, plan, name):
    repo.write(name, "x\n")
    result = plan(repo, name)
    assert result["status"] == "refused"
    assert result["reason"] == "path-unrepresentable"
    assert skipped_map(result) == {name: "path-unrepresentable"}


def test_a_directory_entry_is_skipped(repo, plan):
    repo.write("d/inner.txt", "x\n")
    result = plan(repo, "d", "d/")
    assert skipped_map(result) == {"d": "directory-entry"}
    assert result["status"] == "nothing"


def test_a_refusal_keeps_every_skipped_path_listed(repo, plan):
    repo.write("a.txt", "x\n")
    repo.write("x,y.txt", "x\n")
    result = plan(repo, "x,y.txt", "missing.txt", "a.txt")
    assert result["status"] == "refused"
    assert skipped_map(result) == {
        "x,y.txt": "path-unrepresentable",
        "missing.txt": "absent",
    }


# --- status nothing ----------------------------------------------------------------------------
def test_nothing_when_the_named_paths_have_no_change(repo, plan):
    result = plan(repo, "README.md")
    assert result["status"] == "nothing"
    assert result["reason"] == "no-change"
    assert result["add_argv"] == [] and result["commit_argv"] == []


def test_a_changed_path_with_an_unchanged_one_is_planned_whole(repo, plan):
    repo.write("a.txt", "x\n")
    result = plan(repo, "README.md", "a.txt")
    assert result["status"] == "ok"
    assert result["commit_paths"] == ["README.md", "a.txt"]


# --- the 200-entry display cap ------------------------------------------------------------------
def test_a_long_path_list_is_cut_in_the_json_but_not_in_the_pathspec_file(
    repo, plan, vcs
):
    names = [f"many/f{i:03d}.txt" for i in range(250)]
    for name in names:
        repo.write(name, "x\n")
    result = plan(repo, *names)
    assert result["truncated"] is True
    assert result["s_count"] == 250
    assert pathspec_entries(result) == sorted(names)
    shown = json.loads(vcs.emit_text(result))
    assert shown["truncated"] is True
    assert len(shown["commit_paths"]) == 200
    assert shown["s_count"] == 250
    assert shown["pathspec_file"]["content"] == result["pathspec_file"]["content"]


def test_a_short_list_is_not_truncated(repo, plan):
    repo.write("a.txt", "x\n")
    assert plan(repo, "a.txt")["truncated"] is False


# --- the verb writes nothing (FR-011) ---------------------------------------------------------------
def test_planning_writes_no_ref_index_entry_or_file(repo, plan):
    repo.write("a.txt", "x\n")
    repo.write("tracked.txt", "v1\n")
    repo.commit("tracked")
    repo.write("tracked.txt", "v2\n")
    repo.git("add", "--", "tracked.txt")

    index = repo.work / ".git" / "index"

    def snapshot():
        return (
            repo.git("for-each-ref"),
            repo.git("diff", "--cached", "--raw"),
            repo.git("status", "--porcelain=v1", "--untracked-files=all"),
            sorted(p.name for p in repo.work.iterdir()),
        )

    def index_state():  # no git call here: the helper alone is measured
        return index.read_bytes(), os.stat(index).st_mtime_ns

    before = snapshot()
    index_before = index_state()
    plan(repo, "a.txt", "tracked.txt")
    plan(repo)
    assert index_state() == index_before
    assert snapshot() == before


# --- pathless commit: S is the index change set (FR-038, FR-117, T-26) ------------------------------
def test_pathless_s_is_the_index_change_set(repo, plan):
    repo.write("one.txt", "1\n")
    repo.write("two.txt", "2\n")
    repo.write("unstaged.txt", "3\n")
    repo.git("add", "--", "one.txt", "two.txt")
    result = plan(repo)
    assert result["status"] == "ok"
    assert result["commit_paths"] == ["one.txt", "two.txt"]
    assert result["s_count"] == 2
    assert result["add_argv"] == []
    assert result["pathspec_file"] is None
    assert result["commit_argv"] == ["commit", "-F", result["message_path"]]


def test_pathless_s_holds_a_partly_staged_file_once_and_adds_nothing_unstaged(
    repo, plan
):
    repo.write("part.txt", "v1\n")
    repo.commit("part")
    repo.write("part.txt", "v2\n")
    repo.git("add", "--", "part.txt")
    repo.write("part.txt", "v3\n")  # an unstaged edit on top of the staged one
    result = plan(repo)
    assert result["commit_paths"] == ["part.txt"]
    assert "--only" not in result["commit_argv"]


def test_pathless_s_names_deletions_and_both_ends_of_a_rename(repo, plan):
    repo.write("old.txt", "same\nlines\nhere\n")
    repo.write("gone.txt", "x\n")
    repo.commit("two files")
    repo.git("mv", "old.txt", "new.txt")
    repo.git("rm", "-q", "--", "gone.txt")
    assert plan(repo)["commit_paths"] == ["gone.txt", "new.txt", "old.txt"]


def test_pathless_s_is_not_widened_when_dev_tasks_is_staged_afterwards(repo, plan):
    repo.write("one.txt", "1\n")
    repo.git("add", "--", "one.txt")
    frozen = plan(repo)
    repo.write(".dev/tasks/to-do/t1/t1.md", "task\n")
    repo.git("add", "--", ".dev/tasks")
    assert frozen["commit_paths"] == ["one.txt"]
    assert ".dev/tasks" not in json.dumps(frozen)
    # a new call is a new freeze: it sees the later index, the earlier result does not move
    assert plan(repo)["commit_paths"] == [".dev/tasks/to-do/t1/t1.md", "one.txt"]


def test_pathless_with_an_empty_index_is_nothing(repo, plan):
    repo.write("unstaged.txt", "x\n")
    result = plan(repo)
    assert result["status"] == "nothing"
    assert result["reason"] == "empty"
    assert result["commit_argv"] == []


def test_pathless_refuses_a_staged_dev_copy_path(repo, plan):
    repo.write(".claude/agents/x.md", "x\n")
    repo.git("add", "--", ".claude/agents/x.md")
    result = plan(repo)
    assert result["status"] == "refused"
    assert result["reason"] == "dev-copy-path"


def test_pathless_refuses_a_staged_legacy_run_folder_path(repo, plan):
    # A commit with no path takes the whole index, so leaving the path out of S would still
    # commit it: the plan refuses and prints no argv.
    repo.write(".dev/implement/run-1/ledger.md", "x\n")
    repo.write("one.txt", "1\n")
    repo.git("add", "--", ".dev/implement/run-1/ledger.md", "one.txt")
    result = plan(repo)
    assert result["status"] == "refused"
    assert result["reason"] == "legacy-run-folder"
    assert ".dev/implement/run-1/ledger.md" in result["detail"]
    assert result["commit_paths"] == []
    assert result["commit_argv"] == []
    assert skipped_map(result) == {
        ".dev/implement/run-1/ledger.md": "legacy-run-folder"
    }


def test_pathless_refuses_a_staged_gitlink(submodule_repo, plan):
    repo = submodule_repo
    sub = repo.work / repo.sub_path
    git_in(sub, "config", "user.name", "t")
    git_in(sub, "config", "user.email", "t@example.invalid")
    (sub / "more.txt").write_text("more\n", encoding="utf-8")
    git_in(sub, "add", "-A")
    git_in(sub, "commit", "-q", "-m", "more")
    repo.git("add", "--", repo.sub_path)  # the pointer change is now staged
    result = plan(repo)
    assert result["status"] == "refused"
    assert result["reason"] == "gitlink"
    assert result["commit_argv"] == []


def test_the_temp_file_names_differ_between_two_worktrees_and_between_calls(
    repo, plan, vcs, tmp_path
):
    # Same HEAD, same staged path: the work tree is part of the digest in the name, and a
    # random token makes every call's names unguessable (a planted symlink cannot hit them).
    other = tmp_path / "second-worktree"
    repo.git("worktree", "add", "-q", "--detach", str(other))
    repo.write("same.txt", "1\n")
    repo.git("add", "--", "same.txt")
    (other / "same.txt").write_text("1\n", encoding="utf-8")
    git_in(other, "add", "--", "same.txt")
    first = plan(repo)
    second = vcs.run_stage_plan(str(other), None)
    assert first["commit_paths"] == second["commit_paths"] == ["same.txt"]
    assert first["head_before"] == second["head_before"]
    name = re.compile(r"vcs-message-([0-9a-f]{16})-([0-9a-f]{16})\.txt$")
    one, two = (name.search(p["message_path"]) for p in (first, second))
    assert (
        one and two and one.group(1) != two.group(1)
    )  # the digest tells worktrees apart
    again = name.search(plan(repo)["message_path"])
    assert again and again.group(1) == one.group(1)  # same inputs, same digest
    assert again.group(2) != one.group(2)  # but never the same name twice


def test_pathless_on_a_repository_with_no_commit_yet(tmp_path, plan, vcs):
    root = tmp_path / "fresh"
    root.mkdir()
    git_in(root, "init", "-q", "-b", "main")
    (root / "a.txt").write_text("x\n", encoding="utf-8")
    git_in(root, "add", "--", "a.txt")
    result = vcs.run_stage_plan(str(root), None)
    assert result["status"] == "ok"
    assert result["commit_paths"] == ["a.txt"]
    assert result["head_before"] is None


def test_the_result_names_head(repo, plan):
    repo.write("a.txt", "x\n")
    assert plan(repo, "a.txt")["head_before"] == repo.git("rev-parse", "HEAD").strip()


# --- the command line ----------------------------------------------------------------------------------
def run_cli(repo, *args):
    done = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "vcs.py"),
            "stage-plan",
            "--cwd",
            str(repo.work),
            *args,
        ],
        capture_output=True,
        text=True,
    )
    return done


def test_cli_prints_one_json_object_and_exits_zero(repo):
    repo.write("-nfile.txt", "x\n")
    repo.write("b.txt", "x\n")
    done = run_cli(repo, "--path=-nfile.txt", "--path", "b.txt")
    assert done.returncode == 0, done.stderr
    data = json.loads(done.stdout)
    assert data["verb"] == "stage-plan"
    assert data["vcs_contract"] == "1"
    assert data["commit_paths"] == ["-nfile.txt", "b.txt"]


def test_cli_accepts_several_values_after_one_path_option(repo):
    repo.write("a.txt", "x\n")
    repo.write("b.txt", "x\n")
    done = run_cli(repo, "--path", "a.txt", "b.txt")
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout)["commit_paths"] == ["a.txt", "b.txt"]


def test_cli_without_a_path_is_the_pathless_plan(repo):
    repo.write("one.txt", "1\n")
    repo.git("add", "--", "one.txt")
    done = run_cli(repo)
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout)["commit_paths"] == ["one.txt"]


def test_cli_outside_a_repository_is_refused(tmp_path):
    folder = tmp_path / "plain"
    folder.mkdir()
    done = subprocess.run(
        [sys.executable, str(SCRIPTS / "vcs.py"), "stage-plan", "--cwd", str(folder)],
        capture_output=True,
        text=True,
    )
    assert done.returncode == 0
    data = json.loads(done.stdout)
    assert (data["status"], data["reason"]) == ("refused", "not-a-repo")


# =============================================================================================
# Ledger mode (FR-060, FR-062, FR-073 to FR-076, FR-108, FR-110; T-01, T-19 parts)
# =============================================================================================
# Each case builds a real repository, a real implement ledger and a sidecar, the Q0 files
# (``q0-head``, ``q0-branch``, the Q0 pin) and the accepted pin, the way the executor does.
PIN = "refs/superclaude/implement"
SIDE_RUN_ON = {"mode": "on", "ledger_lines": 0, "branch": "refs/heads/main"}


def private_tree(repo, *paths):
    """A tree made with a private index: HEAD plus the work tree (the Q0 method), or, with
    ``paths``, HEAD plus only those paths."""
    with tempfile.TemporaryDirectory() as folder:
        env = {**os.environ, "GIT_INDEX_FILE": os.path.join(folder, "index")}
        out = ""
        steps = (
            ["read-tree", "HEAD"],
            ["add", "--", *paths] if paths else ["add", "-A"],
            ["write-tree"],
        )
        for args in steps:
            out = subprocess.run(
                ["git", *args],
                cwd=repo.work,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
    return out


class Scene:
    """A ledger, a sidecar and the Q0 and accepted proofs of a plan run in ``repo``."""

    def __init__(self, repo, vcs, managed=False, slug="plan1"):
        self.repo, self.vcs, self.slug, self.managed = repo, vcs, slug, managed
        self.ordinals = {}
        if managed:
            self.pkg = repo.work / ".dev/tasks/to-do" / slug
            self.run_dir = self.pkg
            self.ledger_path = self.pkg / "progress.md"
            self.side_path = self.pkg / "artifacts/commits.md"
            self.retries = self.pkg / "artifacts/retries"
        else:
            self.pkg = None
            self.run_dir = repo.work / ".dev/implement" / slug
            self.ledger_path = self.run_dir / "ledger.md"
            self.side_path = self.run_dir / "commits.md"
            self.retries = self.run_dir / "retries"
        self.ledger = LedgerBuilder(self.ledger_path).header()
        if managed:
            self.ledger.plan()
        self.side = SidecarBuilder(self.side_path).run(1, **SIDE_RUN_ON)

    def start(self, tid, *, nogit=False):
        """Q0: pin the start tree, record ``q0-head`` and ``q0-branch``, write the start line."""
        self.ordinals[tid] = self.ordinals.get(tid, 0) + 1
        if nogit:
            self.ledger.start(tid, sha="nogit")
            return
        tree = private_tree(self.repo)
        self.repo.git("update-ref", f"{PIN}/{self.slug}/T{tid}", tree)
        folder = self.retries / f"T{tid}"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "q0-head").write_text(self.repo.git("rev-parse", "HEAD"), "utf-8")
        (folder / "q0-branch").write_text(
            self.repo.git("symbolic-ref", "HEAD"), "utf-8"
        )
        self.ledger.start(tid, sha=tree)

    def accept(self, tid, files, pin=True):
        """Pin the accepted tree (FR-073) and write the first ``complete`` line."""
        if pin:
            ref = f"{PIN}/{self.slug}/accepted/T{tid}-s{self.ordinals[tid]}"
            self.repo.git("update-ref", ref, private_tree(self.repo))
        self.ledger.complete(tid, files=",".join(files))

    def write(self):
        self.ledger.write()
        self.side.write()

    def plan(self, **kw):
        self.write()
        return self.vcs.run_stage_plan(
            str(self.repo.work),
            None,
            ledger=str(self.ledger_path),
            run_dir=str(self.run_dir),
            package=str(self.pkg) if self.pkg else None,
            **kw,
        )


@pytest.fixture
def scene(repo, vcs):
    def make(managed=False):
        repo.write("src/a.py", "old\n")
        repo.write("src/b.py", "old\n")
        repo.commit("base")
        return Scene(repo, vcs, managed)

    return make


def one_task(scene, managed=False, files=("src/a.py",)):
    s = scene(managed)
    s.start("1")
    s.repo.write("src/a.py", "new\n")
    s.accept("1", list(files))
    return s


def refs_and_index(repo):
    index = repo.work / ".git" / "index"
    return (
        repo.git("for-each-ref"),
        repo.git("diff", "--cached", "--raw"),
        index.read_bytes(),
        os.stat(index).st_mtime_ns,
    )


# --- the due boundary and S ----------------------------------------------------------------
def test_ledger_mode_plans_the_due_boundary(scene, repo):
    s = one_task(scene)
    head = repo.git("rev-parse", "HEAD").strip()
    result = s.plan()
    assert result["status"] == "ok", result
    assert result["tasks"] == ["1"]
    assert re.fullmatch("[0-9a-f]{64}", result["key"])
    assert (result["attempt"], result["parent"]) == (1, head)
    assert result["commit_paths"] == ["src/a.py"] and result["s_count"] == 1
    spec = result["pathspec_file"]
    folder = os.path.realpath(s.side_path.parent)
    assert spec["path"] == os.path.join(folder, f"commit-paths-{result['key']}-a1.txt")
    assert spec["content"] == "src/a.py\0"
    assert spec["sha256"] == hashlib.sha256(b"src/a.py\0").hexdigest()
    assert result["commit_argv"][:3] == ["--literal-pathspecs", "commit", "--only"]
    assert result["boundary_ref"] == f"{PIN}/plan1/boundary/{result['key']}-a1"
    assert result["accepted"] == [f"{PIN}/plan1/accepted/T1-s1"]


def test_s_is_the_union_of_the_anchor_files_and_ignores_a_later_rereview(scene, repo):
    s = scene()
    s.start("1")
    s.start("2")
    repo.write("src/a.py", "new\n")
    repo.write("src/b.py", "new\n")
    s.accept("1", ["src/a.py"])
    s.accept("2", ["src/b.py"])
    repo.write("src/c.py", "new\n")
    s.ledger.complete("1", files="src/c.py")  # a re-review line of task 1
    result = s.plan()
    assert result["status"] == "ok", result
    assert result["tasks"] == ["1", "2"]
    assert result["commit_paths"] == ["src/a.py", "src/b.py"]


def test_a_managed_run_adds_the_package_files_but_not_other_packages(scene, repo):
    s = one_task(scene, managed=True)
    pkg = f".dev/tasks/to-do/{s.slug}"
    repo.write(f"{pkg}/{s.slug}.md", "plan\n")
    repo.write(f"{pkg}/artifacts/notes.md", "notes\n")
    repo.write(".dev/tasks/to-do/other/other.md", "another package\n")
    # the path file of an earlier attempt is not part of S (its hash would include itself)
    repo.write(f"{pkg}/artifacts/commit-paths-{'a' * 64}-a1.txt", "x")
    result = s.plan()
    assert result["status"] == "ok", result
    package_files = {
        f"{pkg}/progress.md",
        f"{pkg}/{s.slug}.md",
        f"{pkg}/artifacts/commits.md",
        f"{pkg}/artifacts/notes.md",
        f"{pkg}/artifacts/retries/T1/q0-head",
        f"{pkg}/artifacts/retries/T1/q0-branch",
    }
    assert set(result["commit_paths"]) == {"src/a.py"} | package_files
    assert result["commit_paths"] == sorted(result["commit_paths"])
    assert result["s_count"] == len(package_files) + 1
    content = result["pathspec_file"]["content"]
    assert "other" not in content and "commit-paths-" not in content


def test_a_legacy_ledger_path_in_files_is_skipped(scene, repo):
    s = one_task(scene, files=("src/a.py", ".dev/implement/plan1/ledger.md"))
    result = s.plan()
    assert result["status"] == "ok", result
    assert skipped_map(result) == {
        ".dev/implement/plan1/ledger.md": "legacy-run-folder"
    }
    assert result["commit_paths"] == ["src/a.py"]
    assert "ledger.md" not in json.dumps(
        result["commit_argv"]
    )  # only the path file is named
    assert ".dev/implement" not in result["pathspec_file"]["content"]


def test_a_directory_entry_in_files_refuses(scene):
    s = one_task(scene, files=("src",))
    result = s.plan()
    assert (result["status"], result["reason"]) == ("refused", "directory-entry")
    assert skipped_map(result) == {"src": "directory-entry"}
    assert result["add_argv"] == [] and result["commit_argv"] == []


def test_the_other_path_refusals_hold_in_ledger_mode(scene):
    s = one_task(scene, files=("src/a.py", ".claude/skills/x/SKILL.md"))
    result = s.plan()
    assert (result["status"], result["reason"]) == ("refused", "dev-copy-path")


def test_unchanged_files_are_nothing(scene):
    s = scene()
    s.start("1")
    s.accept("1", ["README.md"])  # the task changed nothing
    result = s.plan()
    assert (result["status"], result["reason"]) == ("nothing", "no-change")
    assert re.fullmatch("[0-9a-f]{64}", result["key"]) and result["tasks"] == ["1"]
    assert result["commit_argv"] == []


def test_a_mixed_batch_is_nothing_with_the_mixed_reason(scene, repo):
    s = scene()
    s.start("1")
    s.start("2")
    repo.write("src/a.py", "new\n")
    s.accept("1", ["src/a.py"])
    s.accept("2", ["src/a.py"])
    # ledger lines: header 1, starts 2-3, complete 4 and 5. Run 2 (off) covers line 5 only.
    s.side.run(2, "off", ledger_lines=4, branch="refs/heads/main")
    result = s.plan()
    assert (result["status"], result["reason"]) == ("nothing", "mixed-authorization")
    assert result["tasks"] == ["1", "2"]


# --- finding the boundary ----------------------------------------------------------------------
def test_an_empty_ledger_has_no_due_boundary(scene):
    s = scene()
    result = s.plan()
    assert (result["status"], result["reason"]) == ("refused", "no-due-boundary")


def test_an_unfinished_task_is_not_due(scene):
    s = scene()
    s.start("1")
    assert s.plan()["reason"] == "no-due-boundary"


def test_a_completion_in_an_off_segment_is_not_due(scene, repo):
    s = one_task(scene)
    s.side = SidecarBuilder(s.side_path).run(1, "off", ledger_lines=0, branch="-")
    assert s.plan()["reason"] == "no-due-boundary"


def test_a_later_start_is_out_of_protocol(scene, repo):
    s = one_task(scene)
    s.start("2")
    result = s.plan()
    assert (result["status"], result["reason"]) == ("refused", "out-of-protocol")


def test_a_prepared_boundary_whose_head_moved_is_unsettled(scene):
    s = one_task(scene)
    key = s.plan()["key"]
    s.side.prepared("1", key=key, parent=SHA40)  # HEAD is not the prepared parent
    result = s.plan()
    assert (result["status"], result["reason"]) == ("refused", "unsettled")
    assert result["key"] == key


def test_a_prepared_boundary_at_its_parent_gets_the_next_attempt(scene, repo):
    s = one_task(scene)
    first = s.plan()
    head = first["parent"]
    s.side.prepared(
        "1", key=first["key"], parent=head
    )  # crashed before any result line
    second = s.plan()
    assert second["status"] == "ok", second
    assert second["attempt"] == 2 and second["key"] == first["key"]
    assert second["pathspec_file"]["path"].endswith("-a2.txt")
    s.side.prepared("1", key=first["key"], attempt=2, parent=head)
    s.side.refused("1", key=first["key"], attempt=2, reason="hook-failed")
    third = s.plan()  # a refused attempt with HEAD at the parent may be retried
    assert third["attempt"] == 3


def test_a_settled_boundary_is_not_due_again(scene):
    s = one_task(scene)
    key = s.plan()["key"]
    s.side.skipped("1", key=key)
    assert s.plan()["reason"] == "no-due-boundary"


def spoil_sidecar(s):
    s.side.raw("not a sidecar line")


def spoil_run_offset(s):
    s.side = SidecarBuilder(s.side_path).run(1, "on", ledger_lines=99)


def spoil_ledger(s):
    s.ledger.add("garbage")


@pytest.mark.parametrize(
    ("spoil", "reason"),
    [
        (spoil_sidecar, "sidecar-corrupt"),
        (spoil_run_offset, "sidecar-mismatch"),
        (spoil_ledger, "ledger-corrupt"),
    ],
)
def test_a_corrupt_sidecar_ledger_or_run_line_is_refused(scene, spoil, reason):
    s = one_task(scene)
    spoil(s)
    result = s.plan()
    assert (result["status"], result["reason"]) == ("refused", reason)
    assert result["add_argv"] == [] and result["commit_argv"] == []


# --- the staging checks (FR-054, FR-073 to FR-075), one refusal token each -------------------------
def sc_branch_changed(s):
    s.start("1")
    s.repo.write("src/a.py", "new\n")
    s.accept("1", ["src/a.py"])
    s.repo.git("switch", "-q", "-c", "other")


def sc_branch_unproven(s):
    s.start("1")
    s.repo.write("src/a.py", "new\n")
    s.accept("1", ["src/a.py"])
    os.remove(s.retries / "T1" / "q0-branch")


def sc_head_moved(s):
    s.start("1")
    s.repo.write("src/a.py", "new\n")
    s.accept("1", ["src/a.py"])
    s.repo.write("src/z.py", "z\n")
    s.repo.git("add", "--", "src/z.py")
    s.repo.git("commit", "-q", "-m", "someone else committed")


def sc_foreign_change(s):
    s.repo.write(
        "src/a.py", "the person's edit\n"
    )  # uncommitted, before the task starts
    s.start("1")
    s.repo.write("src/a.py", "the task's edit\n")
    s.accept("1", ["src/a.py"])


def sc_changed_after_review(s):
    s.start("1")
    s.repo.write("src/a.py", "new\n")
    s.accept("1", ["src/a.py"])
    s.repo.write("src/a.py", "rewritten by a lint step\n")


def sc_no_accepted_tree(s):
    s.start("1")
    s.repo.write("src/a.py", "new\n")
    s.accept("1", ["src/a.py"], pin=False)


def sc_no_snapshot(s):
    s.start("1", nogit=True)
    s.repo.write("src/a.py", "new\n")
    s.accept("1", ["src/a.py"], pin=False)


CHECK_CASES = {
    "branch-changed": sc_branch_changed,
    "branch-unproven": sc_branch_unproven,
    "head-moved": sc_head_moved,
    "foreign-change": sc_foreign_change,
    "changed-after-review": sc_changed_after_review,
    "no-accepted-tree": sc_no_accepted_tree,
    "no-snapshot": sc_no_snapshot,
}


@pytest.mark.parametrize("token", sorted(CHECK_CASES))
@pytest.mark.parametrize("managed", [False, True], ids=["legacy", "managed"])
def test_each_staging_check_produces_its_refusal_token(scene, token, managed):
    s = scene(managed)
    CHECK_CASES[token](s)
    result = s.plan()
    assert (result["status"], result["reason"]) == ("refused", token), result
    assert result["add_argv"] == [] and result["commit_argv"] == []
    assert result["pathspec_file"] is None and result["message_path"] is None
    assert re.fullmatch("[0-9a-f]{64}", result["key"]) and result["tasks"] == ["1"]


def test_a_persons_uncommitted_change_in_a_task_file_is_a_foreign_change(scene):
    s = scene()
    sc_foreign_change(s)
    result = s.plan()
    assert result["reason"] == "foreign-change"
    assert result["paths"] == ["src/a.py"]
    assert "src/a.py" in result["detail"]


def test_a_path_rewritten_after_review_is_named(scene):
    s = scene()
    sc_changed_after_review(s)
    result = s.plan()
    assert result["reason"] == "changed-after-review"
    assert result["paths"] == ["src/a.py"]
    assert "src/a.py" in result["detail"]
    advice = " ".join(result["advice"])
    assert f"restore --source={PIN}/plan1/accepted/T1-s1 -- src/a.py" in advice
    assert "compare first: this overwrites any newer edit" in advice


def test_package_evidence_is_not_a_product_path(scene, repo):
    # A managed run appends to codegraph.md and the like after the review; only the
    # product paths are compared with the accepted tree (FR-132).
    s = one_task(scene, managed=True)
    repo.write(f".dev/tasks/to-do/{s.slug}/artifacts/codegraph.md", "later line\n")
    assert s.plan()["status"] == "ok"


def test_a_batch_checks_every_member(scene, repo):
    s = scene()
    s.start("1")
    s.start("2")
    repo.write("src/a.py", "new\n")
    repo.write("src/b.py", "new\n")
    s.accept("1", ["src/a.py"])
    s.accept("2", ["src/b.py"])
    assert s.plan()["status"] == "ok"
    repo.write("src/b.py", "linted\n")
    result = s.plan()
    assert (result["reason"], result["paths"]) == ("changed-after-review", ["src/b.py"])


# --- --candidate (FR-108) -----------------------------------------------------------------------
def prepare(s, first):
    """Append the prepared line the executor writes between the plan and the candidate."""
    s.side.prepared(
        "1",
        key=first["key"],
        parent=first["parent"],
        paths=first["pathspec_file"]["sha256"],
        accepted=",".join(first["accepted"]),
    )


@pytest.mark.parametrize("managed", [False, True], ids=["legacy", "managed"])
def test_candidate_builds_the_tree_and_writes_no_ref_or_index_entry(
    scene, repo, managed
):
    s = one_task(scene, managed=managed)
    first = s.plan()
    prepare(s, first)
    s.write()
    before = refs_and_index(repo)
    result = s.plan(candidate=True)
    assert result["status"] == "ok", result
    assert refs_and_index(repo) == before
    assert result["attempt"] == 1 and result["key"] == first["key"]
    tree = result["candidate_tree"]
    assert re.fullmatch("[0-9a-f]{40}", tree)
    assert tree == private_tree(repo, *result["commit_paths"])
    sidecar = f".dev/tasks/to-do/{s.slug}/artifacts/commits.md"
    if managed:
        # the frozen prepared bytes are in the tree (and the prepared line is among them)
        saved = repo.git("cat-file", "-p", f"{tree}:{sidecar}")
        assert saved == s.side_path.read_text(encoding="utf-8")
        assert f"commit prepared key={first['key']}" in saved
    else:
        assert repo.git("ls-tree", "-r", "--name-only", tree).split() == [
            "README.md",
            "src/a.py",
            "src/b.py",
        ]
    again = s.plan(candidate=True)  # byte-identical on the same inputs
    assert masked(s.vcs.emit_text(again)) == masked(s.vcs.emit_text(result))


@pytest.mark.parametrize("managed", [False, True], ids=["legacy", "managed"])
def test_the_commit_the_argv_makes_has_exactly_the_candidate_tree(scene, repo, managed):
    s = one_task(scene, managed=managed)
    repo.write("unrelated.txt", "staged by the person\n")
    repo.git("add", "--", "unrelated.txt")
    first = s.plan()
    prepare(s, first)
    result = s.plan(candidate=True)
    spec = result["pathspec_file"]
    with open(spec["path"], "w", encoding="utf-8", newline="") as handle:
        handle.write(spec["content"])
    with open(result["message_path"], "w", encoding="utf-8") as handle:
        handle.write("feat: the task\n")
    try:
        git_in(repo.work, *result["add_argv"])
        git_in(repo.work, *result["commit_argv"])
    finally:
        os.remove(spec["path"])
        os.remove(result["message_path"])
    assert repo.git("rev-parse", "HEAD^{tree}").strip() == result["candidate_tree"]
    assert repo.git("rev-parse", "HEAD^").strip() == result["parent"]
    assert repo.git("diff", "--cached", "--name-only").split() == ["unrelated.txt"]


def test_candidate_takes_names_with_pathspec_magic_literally(scene, repo):
    s = scene()
    s.start("1")
    for name in ("a*b.txt", "axb.txt", "has space.txt", "-nfile.txt"):
        repo.write(name, "new\n")
    s.accept("1", ["a*b.txt", "has space.txt", "-nfile.txt"])
    first = s.plan()
    assert first["status"] == "ok", first
    prepare(s, first)
    tree = s.plan(candidate=True)["candidate_tree"]
    names = repo.git("ls-tree", "-r", "--name-only", tree).split("\n")
    assert "a*b.txt" in names and "has space.txt" in names and "-nfile.txt" in names
    assert "axb.txt" not in names  # the decoy a glob would have matched


def test_no_ledger_plan_argv_holds_an_fr063_token(scene):
    from .test_argv_shape import FR063_FORBIDDEN

    s = one_task(scene, managed=True)
    result = s.plan()
    for argv in (result["add_argv"], result["commit_argv"]):
        assert argv
        for token in argv:
            assert (
                token not in FR063_FORBIDDEN
                and token.split("=")[0] not in FR063_FORBIDDEN
            )


def test_candidate_refuses_a_pin_with_another_target_and_accepts_the_same_one(
    scene, repo
):
    s = one_task(scene)
    first = s.plan()
    prepare(s, first)
    ref = first["boundary_ref"]
    repo.git("update-ref", ref, repo.git("rev-parse", "HEAD^{tree}").strip())
    refused = s.plan(candidate=True)
    assert (refused["status"], refused["reason"]) == ("refused", "pin-conflict")
    assert refused.get("candidate_tree") is None
    tree = private_tree(repo, "src/a.py")
    repo.git("update-ref", ref, tree)
    again = s.plan(candidate=True)
    assert again["status"] == "ok" and again["candidate_tree"] == tree


def test_candidate_needs_a_prepared_attempt_at_its_parent(scene):
    s = one_task(scene)
    first = s.plan()
    assert s.plan(candidate=True)["reason"] == "no-due-boundary"
    s.side.prepared("1", key=first["key"], parent=SHA40)
    assert s.plan(candidate=True)["reason"] == "head-moved"


def test_candidate_runs_the_staging_checks_too(scene):
    s = one_task(scene)
    first = s.plan()
    prepare(s, first)
    s.repo.write("src/a.py", "rewritten by a lint step\n")
    assert s.plan(candidate=True)["reason"] == "changed-after-review"


def test_ledger_plans_are_deterministic_and_write_nothing(scene, repo):
    s = one_task(scene, managed=True)
    first = s.plan()
    before = refs_and_index(repo)
    again = s.plan()
    assert masked(s.vcs.emit_text(first)) == masked(s.vcs.emit_text(again))
    assert refs_and_index(repo) == before
    assert not os.path.exists(first["pathspec_file"]["path"])  # the agent writes it


# --- the command line ---------------------------------------------------------------------------
def test_cli_ledger_mode_prints_the_plan(scene, repo):
    s = one_task(scene, managed=True)
    s.write()
    done = run_cli(
        repo,
        "--ledger",
        str(s.ledger_path),
        "--run-dir",
        str(s.run_dir),
        "--package",
        str(s.pkg),
    )
    assert done.returncode == 0, done.stderr
    data = json.loads(done.stdout)
    assert (data["verb"], data["status"]) == ("stage-plan", "ok")
    assert "src/a.py" in data["commit_paths"]


def test_cli_resolves_relative_ledger_arguments_against_cwd(scene, repo):
    s = one_task(scene)
    s.write()
    done = run_cli(
        repo,
        "--ledger",
        ".dev/implement/plan1/ledger.md",
        "--run-dir",
        ".dev/implement/plan1",
    )
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout)["status"] == "ok"


@pytest.mark.parametrize(
    "args",
    [
        ["--ledger", "l.md"],
        ["--run-dir", "d"],
        ["--ledger", "l.md", "--run-dir", "d", "--path", "a.txt"],
        ["--candidate"],
        ["--package", "p"],
    ],
    ids=[
        "no-run-dir",
        "no-ledger",
        "path-and-ledger",
        "candidate-alone",
        "package-alone",
    ],
)
def test_cli_usage_errors_exit_64(repo, args):
    done = run_cli(repo, *args)
    assert done.returncode == 64
    assert done.stdout == ""


def test_cli_a_missing_ledger_is_a_failed_lookup(repo):
    done = run_cli(repo, "--ledger", "nope.md", "--run-dir", "nope")
    assert done.returncode == 69 and done.stdout == ""
