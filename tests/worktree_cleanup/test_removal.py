"""The removal pipeline (Task 11): save, close terminals, check again, clear, remove, branch, read back.

Real git runs on throwaway repositories under ``tmp_path`` with local bare remotes; ``orca``
answers come from canned replies. Nothing here touches a real worktree.
"""

from __future__ import annotations

import dataclasses
import os
from pathlib import Path

import pytest

from .conftest import git_in, make_fake_proc
from .test_archive import Case, make_pr
from .test_facts import write

NOW = 2_000_000_000.0
DAY = 86400.0
OLD = {
    "git_file_mtime": NOW - 20 * DAY,
    "last_commit_ts": NOW - 20 * DAY,
    "created_ts": NOW - 30 * DAY,
}
GOOD_ORCA_LIST = '{"ok": true, "result": {"worktrees": []}}'


def result(wc, code=0, out="", err=""):
    return wc.Result(code, out, err)


class Setup:
    """One worktree with .dev files, ready to be removed, plus the inputs the rules need."""

    def __init__(
        self,
        wc,
        runner_cls,
        repo,
        evidence_bare,
        tmp_path,
        orca_replies=None,
        with_orca=False,
    ):
        self.wc, self.tmp = wc, tmp_path
        self.orca_calls: list[list[str]] = []
        self.orca_replies = dict(orca_replies or {})
        self.case = Case(
            wc, runner_cls, repo, evidence_bare, tmp_path, replies={"orca": self.orca}
        )
        self.with_orca = with_orca
        self.proc_root = str(make_fake_proc(tmp_path / "proc", {}))
        self.pr_head = None

    def orca(self, argv, cwd):
        self.orca_calls.append(list(argv))
        key = tuple(argv[1:3])
        handler = self.orca_replies.get(key)
        if handler is not None:
            return handler(argv, cwd)
        if key == ("worktree", "list"):
            return result(self.wc, 0, GOOD_ORCA_LIST)
        if key == ("worktree", "rm"):  # Orca removes through git, as the real one does
            git_in(self.case.repo.main, "worktree", "remove", str(self.case.path))
            return result(self.wc)
        return result(self.wc)

    @property
    def runner(self):
        return self.case.runner

    def inputs(self, pr_head=None, terminals=2, procs=None, **facts_change):
        wc = self.wc
        facts = dataclasses.replace(self.case.facts(), **OLD, **facts_change)
        pr = make_pr(wc, head_oid=pr_head or facts.head)
        orca = None
        if self.with_orca:
            orca = wc.OrcaWorktree(
                worktree_id="wid", selector="id:wid", path=str(self.case.path), branch="topic", repo="r",
                last_activity_ms=None, is_pinned=False, live_terminal_count=terminals,
                linked_pr_hint=None, comment="",
            )  # fmt: skip
        after = self.runner_after(facts, pr)
        inp = wc.RuleInputs(
            facts=facts, now=NOW, orca=orca, pr_lookup=wc.PrLookup(True, pr),
            landed=wc.Landed("MERGED", "installed copy"), after=after,
            issues=wc.IssueFacts((), ()), procs=procs or wc.ProcScan(True, ()),
        )  # fmt: skip
        return inp, pr

    def runner_after(self, facts, pr):
        return self.wc.commits_after_pr(
            self.runner, str(self.case.path), facts.head, pr.head_oid
        )

    def remove(self, inp=None, pr=None, proc_root=None):
        if inp is None:
            inp, pr = self.inputs()
        self.runner.commands.clear()
        return self.wc.remove_worktree(
            self.runner, inp, pr, self.case.clone, str(self.case.bare),
            proc_root=proc_root or self.proc_root, log=self.case.notes.append,
        )  # fmt: skip

    def verbs(self):
        out = []
        for c in self.runner.commands:
            argv = list(c.argv)
            if argv[0] == "git":  # drop the leading -c and -C options
                while argv[1] in ("-c", "-C"):
                    del argv[1:3]
                out.append(" ".join(argv[1:3]))
            else:
                out.append(" ".join(argv[:2]))
        return out


@pytest.fixture
def setup(wc, runner_cls, throwaway_repo, evidence_bare, tmp_path):
    return Setup(wc, runner_cls, throwaway_repo, evidence_bare, tmp_path)


@pytest.fixture
def setup_orca(wc, runner_cls, throwaway_repo, evidence_bare, tmp_path):
    return Setup(
        wc, runner_cls, throwaway_repo, evidence_bare, tmp_path, with_orca=True
    )


def index_of(verbs, start):
    return next(i for i, v in enumerate(verbs) if v.startswith(start))


def last_index_of(verbs, start):
    return max(i for i, v in enumerate(verbs) if v.startswith(start))


# -- the whole removal, in order --------------------------------------------------------------


def test_a_worktree_orca_does_not_list_is_removed_with_git_in_the_right_order(setup):
    path = setup.case.path
    done = setup.remove()
    assert done.status == "removed", done.reason
    assert done.verified.startswith("VERIFIED ") and done.branch == "removed"
    assert not path.exists()
    assert (
        Path(setup.case.clone) / "IronClaude" / "example-user"
    ).is_dir()  # the save is in the clone
    verbs = setup.verbs()
    push = index_of(verbs, "push")
    clear = index_of(verbs, "xargs")
    remove = index_of(verbs, "worktree remove")
    branch = index_of(verbs, "branch -d")
    assert push < clear < remove < branch < last_index_of(verbs, "worktree list")
    # Orca never listed it: the only Orca call is the read back
    orca = [c.argv for c in setup.runner.commands if c.argv[0] == "orca"]
    assert orca == [["orca", "worktree", "list", "--json"]]
    assert done.steps[0].startswith("saved: VERIFIED") and done.steps[-1] == "read back"
    cleared = setup.runner.commands[clear]
    assert (
        cleared.argv == ["xargs", "-0", "git", "clean", "-f", "-x", "--"]
        and cleared.stdin_paths == 2
    )
    assert cleared.cwd == str(path)
    # the removal runs from the repo's main checkout, never from inside the worktree
    removal = setup.runner.commands[remove]
    assert removal.cwd == str(setup.case.repo.main) and removal.argv[-1] == str(path)


def test_the_orca_path_closes_terminals_after_the_save_and_before_the_clear(setup_orca):
    done = setup_orca.remove()
    assert done.status == "removed", done.reason
    verbs = setup_orca.verbs()
    order = [
        index_of(verbs, "push"),
        index_of(verbs, "orca terminal"),
        last_index_of(verbs, "status"),  # the re-check reads, after the close
        index_of(verbs, "xargs"),
        index_of(verbs, "orca worktree"),
        index_of(verbs, "branch --list"),
        last_index_of(verbs, "orca worktree"),  # the read back lists it again
    ]
    assert order == sorted(order) and len(set(order)) == len(order)
    assert [
        "orca",
        "terminal",
        "close",
        "--worktree",
        "id:wid",
        "--all",
    ] in setup_orca.orca_calls
    assert ["orca", "worktree", "rm", "--worktree", "id:wid"] in setup_orca.orca_calls
    assert not any(
        v.startswith("worktree remove") for v in verbs
    )  # Orca did the removal
    assert done.branch == "removed with the worktree" or done.branch == "removed"


def test_no_recorded_command_is_forbidden(setup_orca):
    assert setup_orca.remove().status == "removed"
    evidence = os.path.realpath(setup_orca.case.clone)
    for c in setup_orca.runner.commands:
        argv = c.argv
        if (
            argv[0] != "xargs"
        ):  # the one -f of the whole run is the clean, checked below
            assert "--force" not in argv and "-D" not in argv and "-f" not in argv
        assert argv[0] not in ("rm", "mv") and ["worktree", "prune"] != argv[1:3]
        assert not (argv[0] == "git" and "--delete" in argv)
        if "push" in argv:
            assert os.path.realpath(c.cwd) == evidence and argv[-2:] == [
                "origin",
                "main",
            ]
        if "git" in argv[:1] and "clean" in argv:
            raise AssertionError("git clean must run only through xargs")
    clean = [c for c in setup_orca.runner.commands if c.argv[0] == "xargs"]
    assert len(clean) == 1 and clean[0].argv[1:] == [
        "-0",
        "git",
        "clean",
        "-f",
        "-x",
        "--",
    ]


# -- fail closed at every step ---------------------------------------------------------------------


def test_a_tracked_edit_or_a_commit_after_the_pull_request_does_nothing(wc, setup_orca):
    edit = setup_orca.case.path / "README.md"
    edit.write_text("edited\n", encoding="utf-8")
    done = setup_orca.remove()
    assert (done.status, done.reason) == ("kept", "1 changed tracked file")
    assert (
        setup_orca.runner.commands == [] and setup_orca.orca_calls == []
    )  # no archive, close or clear
    assert (
        edit.exists() and (setup_orca.case.path / ".dev" / "tasks" / "a b.md").exists()
    )
    # a commit made after the pull request's last commit
    edit.write_text("example\n", encoding="utf-8")
    inp, pr = setup_orca.inputs()
    old_head = pr.head_oid
    write(setup_orca.case.path / "later.txt")
    git_in(setup_orca.case.path, "add", "later.txt")
    git_in(setup_orca.case.path, "commit", "-q", "-m", "after the pull request")
    inp, pr = setup_orca.inputs(pr_head=old_head)
    done = setup_orca.remove(inp, pr)
    assert (done.status, done.reason) == ("kept", "1 commit after the pull request")
    assert setup_orca.runner.commands == [] and setup_orca.orca_calls == []


@pytest.mark.parametrize(
    "answer", [(0, '{"unverifiable": true}'), (1, ""), (0, "closed but UNVERIFIABLE")]
)
def test_an_unconfirmed_terminal_close_keeps_the_worktree_and_clears_nothing(
    wc, setup_orca, answer
):
    setup_orca.orca_replies[("terminal", "close")] = lambda argv, cwd: result(
        wc, *answer
    )
    done = setup_orca.remove()
    assert (done.status, done.reason) == ("failed", "Orca terminal close not confirmed")
    assert setup_orca.case.path.exists()
    assert not any(c.argv[0] == "xargs" for c in setup_orca.runner.commands)
    assert (setup_orca.case.path / ".dev" / "tasks" / "a b.md").exists()


def test_a_change_made_while_the_terminals_closed_keeps_the_worktree(wc, setup_orca):
    path = setup_orca.case.path

    def busy_terminal(argv, cwd):
        write(path / "notes-made-by-the-terminal.txt")  # an agent was still working
        return result(wc)

    setup_orca.orca_replies[("terminal", "close")] = busy_terminal
    done = setup_orca.remove()
    assert (done.status, done.reason) == (
        "kept",
        "changed since the terminals were closed",
    )
    assert path.exists() and not any(
        c.argv[0] == "xargs" for c in setup_orca.runner.commands
    )


def test_a_saved_file_edited_after_the_save_is_never_cleared(wc, setup_orca):
    path = setup_orca.case.path

    def edits_a_saved_file(argv, cwd):
        (path / ".dev" / "tasks" / "a b.md").write_text(
            "newer bytes\n", encoding="utf-8"
        )
        return result(wc)

    setup_orca.orca_replies[("terminal", "close")] = edits_a_saved_file
    done = setup_orca.remove()
    assert (done.status, done.reason) == (
        "kept",
        "changed since the terminals were closed",
    )
    assert (path / ".dev" / "tasks" / "a b.md").read_text() == "newer bytes\n"


def test_a_process_still_inside_after_the_close_keeps_the_worktree(wc, setup_orca):
    proc = make_fake_proc(setup_orca.tmp / "busy-proc", {42: str(setup_orca.case.path)})
    done = setup_orca.remove(proc_root=str(proc))
    assert (done.status, done.reason) == (
        "kept",
        "a process is still inside after its Orca terminals were closed",
    )
    assert not any(c.argv[0] == "xargs" for c in setup_orca.runner.commands)
    failing = make_fake_proc(setup_orca.tmp / "bad-proc", {43: "file"})
    done = setup_orca.remove(proc_root=str(failing))
    # a scan that cannot be read is a lookup failure, not a verdict
    assert done.status == "failed" and "process scan failed" in done.reason
    assert not any(c.argv[0] == "xargs" for c in setup_orca.runner.commands)


def _assert_nothing_cleared_or_removed(setup, done, why):
    assert done.status == "failed", (done.status, done.reason)
    assert why in done.reason, done.reason
    verbs = setup.verbs()
    assert not any(
        v.startswith(("xargs", "worktree remove", "worktree rm")) for v in verbs
    )
    assert (
        setup.case.path / ".dev" / "tasks" / "a b.md"
    ).exists() or not setup.case.path.exists()


def test_a_git_status_that_cannot_be_read_after_the_close_is_a_failure(wc, setup_orca):
    path = setup_orca.case.path

    def breaks_the_checkout(argv, cwd):
        (path / ".git").rename(path / ".git-off")  # git no longer finds a repo here
        return result(wc)

    setup_orca.orca_replies[("terminal", "close")] = breaks_the_checkout
    done = setup_orca.remove()
    _assert_nothing_cleared_or_removed(
        setup_orca, done, "git status could not be read after the terminals were closed"
    )


def test_a_folder_that_vanishes_during_the_close_is_a_failure(wc, setup_orca):
    path = setup_orca.case.path

    def folder_unreadable(argv, cwd):
        os.rename(path, str(path) + "-moved")
        return result(wc)

    setup_orca.orca_replies[("terminal", "close")] = folder_unreadable
    done = setup_orca.remove()
    _assert_nothing_cleared_or_removed(
        setup_orca, done, "the folder could not be read after the terminals were closed"
    )


def test_a_head_that_cannot_be_read_after_the_close_is_a_failure(
    wc, setup_orca, monkeypatch
):
    inp, pr = setup_orca.inputs()
    real = wc.gather_facts

    def headless(runner, wt, orca=None):
        return dataclasses.replace(real(runner, wt, orca), head=None)

    monkeypatch.setattr(
        wc, "gather_facts", headless
    )  # the only read left is the re-check
    done = setup_orca.remove(inp, pr)
    _assert_nothing_cleared_or_removed(
        setup_orca, done, "HEAD could not be read after the terminals were closed"
    )


def test_a_saved_file_that_cannot_be_read_at_the_re_check_is_a_failure(wc, setup_orca):
    path = setup_orca.case.path

    def saved_file_becomes_a_folder(argv, cwd):
        saved = path / ".dev" / "tasks" / "a b.md"
        saved.unlink()
        saved.mkdir()  # still there, but its bytes cannot be read
        return result(wc)

    setup_orca.orca_replies[("terminal", "close")] = saved_file_becomes_a_folder
    done = setup_orca.remove()
    assert done.status == "failed", (done.status, done.reason)
    assert "a saved file could not be read" in done.reason
    assert not any(v.startswith("xargs") for v in setup_orca.verbs())


def test_an_unknown_relation_to_the_pull_request_at_the_re_check_is_a_failure(
    wc, setup_orca, monkeypatch
):
    inp, pr = setup_orca.inputs()
    monkeypatch.setattr(
        wc, "commits_after_pr", lambda *a, **k: wc.AfterPr("unknown", None, "no clone")
    )
    done = setup_orca.remove(inp, pr)
    assert (done.status, done.reason) == ("failed", "re-check failed: no clone")
    assert not any(v.startswith("xargs") for v in setup_orca.verbs())


def test_a_first_decision_that_could_not_read_a_fact_is_a_failure_not_a_verdict(
    wc, setup_orca
):
    inp, pr = setup_orca.inputs()
    unreadable = dataclasses.replace(
        inp,
        after=wc.AfterPr(
            "unknown", None, "HEAD or the pull request's last commit is not known"
        ),
    )
    done = setup_orca.remove(unreadable, pr)
    assert (
        done.status == "failed" and done.reason == "HEAD is not the pull request's head"
    )
    assert setup_orca.runner.commands == []  # nothing ran: no save, no close, no clear


def test_a_failed_save_stops_before_anything_else(
    wc, runner_cls, throwaway_repo, evidence_bare, tmp_path
):
    setup = Setup(
        wc, runner_cls, throwaway_repo, evidence_bare, tmp_path, with_orca=True
    )
    (setup.case.path / ".dev" / "local" / "run.log").write_text(
        "key " + "gh" + "p_" + "A1b2C3d4" * 4 + "\n"
    )
    done = setup.remove()
    assert done.status == "failed" and done.reason.startswith(
        "saved copy failed: possible secret in"
    )
    assert setup.orca_calls == [] and setup.runner.commands == []
    assert setup.case.path.exists()


def test_a_removal_that_git_refuses_keeps_the_worktree_with_the_refusal_text(
    wc, runner_cls, throwaway_repo, evidence_bare, tmp_path
):
    setup = Setup(wc, runner_cls, throwaway_repo, evidence_bare, tmp_path)

    def refuse(argv, cwd):
        return (
            result(
                wc,
                128,
                "",
                "fatal: contains modified or untracked files, use --force to delete it",
            )
            if argv[1:3] == ["worktree", "remove"]
            else None
        )

    setup.case.runner = runner_cls(
        evidence_dir=setup.case.clone, replies={"git": refuse}
    )
    done = setup.remove()
    assert done.status == "failed"
    assert (
        done.reason
        == "removal refused: fatal: contains modified or untracked files, use --force to delete it"
    )
    assert setup.case.path.exists()
    assert not any("--force" in c.argv for c in setup.runner.commands)


def test_removed_in_git_but_still_listed_in_orca_is_a_failed_row(wc, setup_orca):
    path = setup_orca.case.path
    setup_orca.orca_replies[("worktree", "list")] = lambda argv, cwd: result(
        wc, 0, f'{{"worktrees": [{{"path": "{path}"}}]}}'
    )
    done = setup_orca.remove()
    assert (done.status, done.reason) == (
        "failed",
        "removed in git but still listed in Orca",
    )
    assert not path.exists()  # the removal itself happened


def test_an_orca_read_back_that_fails_is_a_failed_row_when_orca_listed_the_worktree(
    wc, setup_orca
):
    setup_orca.orca_replies[("worktree", "list")] = lambda argv, cwd: result(
        wc, 1, "", "orca down"
    )
    done = setup_orca.remove()
    assert (
        done.status == "failed"
        and done.reason == "read back failed: orca worktree list failed"
    )


def test_a_squash_merged_branch_is_reported_kept_not_an_error(
    wc, runner_cls, throwaway_repo, evidence_bare, tmp_path
):
    setup = Setup(wc, runner_cls, throwaway_repo, evidence_bare, tmp_path)
    path = setup.case.path
    write(path / "feature.txt")
    git_in(path, "add", "feature.txt")
    git_in(path, "commit", "-q", "-m", "feature")
    done = setup.remove()
    assert done.status == "removed", done.reason
    assert done.branch == "kept (not fully merged, as after a squash merge)"
    assert "topic" in git_in(throwaway_repo.main, "branch", "--list", "topic")


def test_a_worktree_with_nothing_to_save_skips_the_archive_and_the_clear(
    wc, runner_cls, throwaway_repo, evidence_bare, tmp_path
):
    setup = Setup(wc, runner_cls, throwaway_repo, evidence_bare, tmp_path)
    import shutil

    shutil.rmtree(
        setup.case.path / ".dev"
    )  # a throwaway folder: nothing under .dev remains
    done = setup.remove()
    assert done.status == "removed" and done.verified == ""
    assert not any(c.argv[0] == "xargs" for c in setup.runner.commands)
    assert not any("push" in c.argv for c in setup.runner.commands)
    assert not Path(setup.case.clone).exists()


def test_the_repo_folder_inside_the_worktree_is_refused(wc, setup):
    inp, pr = setup.inputs()
    wt = dataclasses.replace(inp.facts.worktree, repo_path=str(setup.case.path / "sub"))
    inp = dataclasses.replace(inp, facts=dataclasses.replace(inp.facts, worktree=wt))
    done = setup.remove(inp, pr)
    assert done.status == "failed" and "run from outside it" in done.reason
    assert setup.runner.commands == []


def test_a_sibling_whose_name_starts_with_the_removed_one_is_not_still_listed(
    wc, setup_orca
):
    path = str(setup_orca.case.path)
    sibling = f'{{"worktrees": [{{"path": "{path}-fix", "worktreeId": "wid-2::{path}-fix"}}]}}'
    setup_orca.orca_replies[("worktree", "list")] = lambda argv, cwd: result(
        wc, 0, sibling
    )
    done = setup_orca.remove()
    assert done.status == "removed", done.reason


def test_an_unreadable_orca_list_after_a_removal_is_a_failed_read_back(wc, setup_orca):
    setup_orca.orca_replies[("worktree", "list")] = lambda argv, cwd: result(
        wc, 0, "<html>"
    )
    done = setup_orca.remove()
    assert (done.status, done.reason) == (
        "failed",
        "read back failed: the orca worktree list could not be read",
    )


def test_a_worktree_orca_did_not_list_but_orca_still_lists_after_a_git_removal_is_failed(
    wc, setup
):
    path = setup.case.path
    body = (
        '{"ok": true, "result": {"worktrees": '
        f'[{{"worktreeId": "x::{path}", "path": "{path}"}}]}}}}'
    )
    setup.orca_replies[("worktree", "list")] = lambda argv, cwd: result(wc, 0, body)
    done = setup.remove()
    assert (done.status, done.reason) == (
        "failed",
        "removed in git but still listed in Orca",
    )
    assert not path.exists()
    verbs = setup.verbs()
    assert "worktree remove" in verbs and not any(
        v.startswith("orca worktree rm") for v in verbs
    )


@pytest.mark.parametrize(
    "answer,reason",
    [
        ((1, "", "orca down"), "read back failed: orca worktree list failed"),
        (
            (0, "<html>", ""),
            "read back failed: the orca worktree list could not be read",
        ),
        (
            (0, '{"ok": false, "error": "x"}', ""),
            "read back failed: the orca worktree list could not be read",
        ),
    ],
)
def test_a_bad_orca_list_after_a_git_removal_is_a_failed_read_back(
    wc, setup, answer, reason
):
    setup.orca_replies[("worktree", "list")] = lambda argv, cwd: result(wc, *answer)
    done = setup.remove()
    assert (done.status, done.reason) == ("failed", reason)
    assert not setup.case.path.exists()


def test_a_clean_orca_list_after_a_git_removal_is_a_pass(wc, setup):
    setup.orca_replies[("worktree", "list")] = lambda argv, cwd: result(
        wc, 0, '{"ok": true, "result": {"worktrees": []}}'
    )
    assert setup.remove().status == "removed"


def test_orca_lists_compares_paths_and_ids_for_equality(wc):
    body = '{"result": {"worktrees": [{"worktreeId": "w1::/x/docs-354-fix", "path": "/x/docs-354-fix"}]}}'
    assert wc.orca_lists(body, "/x/docs-354", "w0::/x/docs-354") is False
    assert wc.orca_lists(body, "/x/docs-354-fix", "other") is True
    assert wc.orca_lists(body, "/elsewhere", "w1::/x/docs-354-fix") is True
    assert (
        wc.orca_lists(body, "/x/docs-354-fix/", "other") is True
    )  # a trailing slash is the same folder
    assert (
        wc.orca_lists("[]", "/x", "w") is False
        and wc.orca_lists("{}", "/x", "w") is False
    )
    assert (
        wc.orca_lists("not json", "/x", "w") is None
        and wc.orca_lists("", "/x", "w") is None
    )
    # an Orca error reply cannot be read as "not listed"
    assert wc.orca_lists('{"ok": false}', "/x", "w") is None
    # an empty id never matches, and a row with no id field is not a match
    assert (
        wc.orca_lists('{"worktrees": [{"id": "", "path": "/other"}]}', "/x", "")
        is False
    )
    assert wc.orca_lists('{"worktrees": [{"path": "/other"}]}', "/x", "w") is False
    assert wc.orca_lists('{"worktrees": [{"path": ""}]}', "", "w") is False
    # a symlinked parent folder is still the same worktree
    assert (
        wc.orca_lists('{"worktrees": [{"path": "/tmp/./a/../b"}]}', "/tmp/b", "")
        is True
    )


def test_the_helper_for_refusal_text_does_not_shadow_the_earlier_one(wc):
    assert (
        wc._first_line("") == ""
    )  # the pull request lookup helper keeps its own behaviour
    assert wc._refusal_text("") == "no message"
    assert wc._refusal_text("\n  first\nsecond") == "first"


def test_git_clean_is_refused_for_any_path_that_was_not_saved(wc, setup):
    """The runner itself refuses a clean of an unregistered path, whatever the pipeline does."""
    other = setup.case.path / "keep-me.txt"
    write(other)
    with pytest.raises(wc.RefusedCommand):
        setup.runner.run(
            ["xargs", "-0", "git", "clean", "-f", "-x", "--"],
            cwd=str(setup.case.path),
            stdin=b"keep-me.txt\0",
        )
    assert other.exists()
