"""The safety cases (Task 13): a recorder over every verb, and the outputs, the credentials, the refusals.

Everything runs on throwaway repositories under ``tmp_path`` with a local bare repository
standing in for the evidence repo. The runner records every command and, for the two risky
ones, checks its precondition at the moment the command would start.
"""

from __future__ import annotations

import builtins
import io
import json
import os
import re
from pathlib import Path

import pytest

from .conftest import git_in
from .test_archive import git_identity  # noqa: F401 - autouse: the evidence commit needs an identity
from .test_facts import write
from .test_pipeline import open_terminals
from .test_runner import BANNED, HELPER, PUSH_REFUSED, UNLISTED
from .test_verbs import World

# Built at run time from two pieces: a harmless stand-in, never a real credential.
TOKEN = "placeholder-" + "credential-value"

WORDS = re.compile(
    r"\b(claude|anthropic|openai|gpt|gemini|llm|copilot|codex|opus|sonnet|haiku|agents?|models?)\b",
    re.IGNORECASE,
)


@pytest.fixture
def spy_cls(runner_cls):
    """A recording runner that checks the preconditions of the clear and of the terminal close."""

    class Spy(runner_cls):
        bare = None  # the evidence remote: what a save must have reached before anything is cleared
        ready: frozenset[str] = (
            frozenset()
        )  # worktrees every rule passed for, from the dry run

        def _saved_lists(self):
            names = git_in(
                self.bare, "ls-tree", "-r", "--name-only", "main"
            ).splitlines()
            return [
                set(git_in(self.bare, "show", f"main:{n}").splitlines())
                for n in names
                if n.endswith("/saved-paths.txt")
            ]

        def _execute(self, argv, cwd, stdin):
            if self.bare is not None and argv[:2] == ["xargs", "-0"]:
                wanted = {p for p in (stdin or b"").decode().split("\0") if p}
                assert wanted in self._saved_lists(), (
                    "git clean was issued before a verified save listed exactly these paths"
                )
            if self.bare is not None and argv[:3] == ["orca", "terminal", "close"]:
                name = argv[4].removeprefix("id:id-")
                assert name in self.ready, (
                    f"terminals closed before every rule passed: {name}"
                )
                assert self._saved_lists(), (
                    "terminals closed before the save was verified"
                )
            return super()._execute(argv, cwd, stdin)

    return Spy


def drop_options(args):
    args = list(args)
    while args and args[0] in ("-c", "-C"):
        del args[:2]
    return args


def forbidden(rec, clone):
    """Why a recorded command is never allowed, or an empty list."""
    argv, why = list(rec.argv), []
    prog = os.path.basename(argv[0])
    if prog == "rm":
        why.append("rm")
    if prog == "xargs" and argv != ["xargs", "-0", "git", "clean", "-f", "-x", "--"]:
        why.append("xargs that is not the exact clean")
    if prog == "orca":
        if "--force" in argv or "-f" in argv:
            why.append("--force on an orca command")
        if argv[1:3] == ["worktree", "rm"] and len(argv) != 5:
            why.append("orca worktree rm with extra arguments")
    if prog == "git":
        args = drop_options(argv[1:])
        verb = args[0] if args else ""
        if verb == "worktree" and args[1:2] == ["prune"]:
            why.append("git worktree prune")
        if (
            verb == "worktree"
            and args[1:2] == ["remove"]
            and ("--force" in args or "-f" in args)
        ):
            why.append("--force on git worktree remove")
        if verb == "branch" and ("-D" in args or "-f" in args or "--force" in args):
            why.append("git branch -D")
        if verb == "clean":
            why.append("git clean outside the exact xargs shape")
        if verb == "push":
            if not (rec.cwd == clone and args == ["push", "origin", "main"]):
                why.append("a push to anything but the evidence remote's main")
        if any(t.startswith(":") or t == "--delete" for t in args) or (
            verb == "push" and "-d" in args
        ):
            why.append("a remote branch delete")
    return why


def removal_like(rec):
    a = rec.argv
    return (
        a[:2] == ["xargs", "-0"]
        or a[:3] == ["orca", "terminal", "close"]
        or a[:3] == ["orca", "worktree", "rm"]
        or (a[0] == "git" and drop_options(a[1:])[:2] == ["worktree", "remove"])
        or (a[0] == "git" and drop_options(a[1:])[:2] == ["branch", "-d"])
    )


class Recorder:
    """One world with every branch the rules tell apart, and every verb run on it."""

    def __init__(self, wc, spy_cls, repo, bare, tmp_path, capsys):
        self.world = w = World(wc, spy_cls, repo, bare, tmp_path)
        self.capsys, self.bare, self.runs, self.text, self.docs = (
            capsys,
            bare,
            [],
            [],
            [],
        )
        w.runner.bare = bare
        w.add("done")
        w.add("plain", dev=False)
        w.add("open", state="OPEN")
        edited = w.add("edited")
        (edited / "README.md").write_text("edited\n", encoding="utf-8")
        open_terminals(wc, w, "done", count=1)

    def run(self, *argv, expect):
        code = self.world.run(*argv)
        assert code == expect, (argv, code, expect)
        out, err = self.capsys.readouterr()
        self.text += [out, err]
        self.runs.append((argv, list(self.world.runner.commands)))
        # every run is stamped with the same ``now``, so each run's files replace the last
        for p in self.world.out.glob("prune-*"):
            self.text.append(p.read_text(encoding="utf-8"))
            if p.suffix == ".json":
                self.docs.append((argv, json.loads(p.read_text(encoding="utf-8"))))
            p.unlink()

    def all_commands(self):
        return [c for _argv, cmds in self.runs for c in cmds]


def run_every_verb(rec):
    rec.run("list", expect=0)
    rec.run("prune", expect=0)
    # what the dry run marked removable is the only thing a terminal may be closed for
    rec.world.runner.ready = frozenset(
        r["folder"] for r in rec.docs[-1][1]["rows"] if r["decision"] == "removable"
    )
    rec.run("archive", "done", expect=0)
    rec.run("retire", "done", expect=0)  # a dry run
    rec.run("archive", "open", expect=64)
    rec.run("archive", "edited", expect=64)
    rec.run("retire", "open", "--apply", expect=64)
    rec.run("retire", "edited", "--apply", expect=64)
    rec.run("retire", "main", "--apply", expect=64)
    # --apply on the verbs that never remove: list and archive
    rec.run("list", "--apply", expect=0)
    rec.run("archive", "done", "--apply", expect=0)
    # retire --apply on a removable row (terminals open: close, check again, clear, removal)
    rec.run("retire", "done", "--apply", expect=0)
    # prune --apply removes the other removable row
    rec.run("prune", "--apply", expect=0)
    rec.run("list", expect=0)
    rec.run("prune", "--apply", expect=0)


@pytest.fixture
def recorded(wc, spy_cls, throwaway_repo, evidence_bare, tmp_path, capsys, monkeypatch):
    monkeypatch.setenv("GH_TOKEN", TOKEN)
    monkeypatch.setenv("GITHUB_TOKEN", TOKEN)
    rec = Recorder(wc, spy_cls, throwaway_repo, evidence_bare, tmp_path, capsys)
    run_every_verb(rec)
    return rec


# -- the recorder ---------------------------------------------------------------------------------


def test_no_command_of_any_verb_on_any_branch_is_forbidden(recorded):
    clone = recorded.world.clone
    problems = [
        (c.argv, why) for c in recorded.all_commands() if (why := forbidden(c, clone))
    ]
    assert problems == []
    assert any(c.argv[0] == "git" and "push" in c.argv for c in recorded.all_commands())


def test_the_recorder_itself_catches_every_forbidden_shape(wc):
    rec = lambda *argv, cwd=None: wc.CommandRecord(list(argv), cwd)  # noqa: E731
    bad = [
        rec("rm", "-rf", "x"),
        rec("git", "branch", "-D", "x"),
        rec("git", "worktree", "prune"),
        rec("git", "worktree", "remove", "--force", "x"),
        rec("orca", "worktree", "rm", "--worktree", "id:1", "--force"),
        rec("git", "push", "origin", "main", cwd="/elsewhere"),
        rec("git", "push", "origin", ":topic", cwd="/clone"),
        rec("git", "push", "--delete", "origin", "topic", cwd="/clone"),
        rec("git", "clean", "-fdx"),
        rec("xargs", "-0", "git", "clean", "-fdx"),
    ]
    for r in bad:
        assert forbidden(r, "/clone"), r.argv
    assert forbidden(rec("git", "push", "origin", "main", cwd="/clone"), "/clone") == []
    assert (
        forbidden(rec("xargs", "-0", "git", "clean", "-f", "-x", "--"), "/clone") == []
    )


def test_a_dry_run_records_no_removal_and_apply_removes_only_removable_rows(recorded):
    world = recorded.world
    for argv, commands in recorded.runs:
        if "--apply" not in argv or argv[0] in ("list", "archive"):
            assert not [c.argv for c in commands if removal_like(c)], argv
    # the dry run of prune said which rows are removable; --apply removed exactly those
    dry = next(doc for argv, doc in recorded.docs if argv == ("prune",))
    removable = {r["folder"] for r in dry["rows"] if r["decision"] == "removable"}
    assert removable == {"done", "plain"}
    removed = set()
    for argv, commands in recorded.runs:
        if "--apply" not in argv:
            continue
        for c in commands:
            if c.argv[:3] == ["orca", "worktree", "rm"]:
                removed.add(c.argv[4].removeprefix("id:id-"))
            elif c.argv[0] == "git" and drop_options(c.argv[1:])[:2] == [
                "worktree",
                "remove",
            ]:
                removed.add(Path(c.argv[-1]).name)
    assert removed == removable
    assert world.paths["open"].exists() and world.paths["edited"].exists()
    assert not world.paths["done"].exists() and not world.paths["plain"].exists()


def test_the_clear_and_the_terminal_close_come_after_the_verified_save(recorded):
    # the runner checked the exact paths and the save at the moment each would start; here
    # the order of the recorded commands says the same
    # (a later run may find the folder already saved and push nothing, so the whole record counts)
    verbs = [c.argv for c in recorded.all_commands()]
    pushes = [i for i, a in enumerate(verbs) if a[0] == "git" and "push" in a]
    risky = [
        i
        for i, a in enumerate(verbs)
        if a[:2] == ["xargs", "-0"] or a[:3] == ["orca", "terminal", "close"]
    ]
    assert pushes and risky and min(pushes) < min(risky)
    closes = [
        c
        for c in recorded.all_commands()
        if c.argv[:3] == ["orca", "terminal", "close"]
    ]
    assert len(closes) == 1 and closes[0].argv[3:] == [
        "--worktree",
        "id:id-done",
        "--all",
    ]


def test_every_gh_call_names_its_repo(recorded):
    calls = [
        c.argv for c in recorded.all_commands() if os.path.basename(c.argv[0]) == "gh"
    ]
    assert calls
    for argv in calls:
        assert "--repo" in argv, argv
        assert re.fullmatch(r"IronbellyOrg/[\w.-]+", argv[argv.index("--repo") + 1]), (
            argv
        )


# -- outputs and credentials ------------------------------------------------------------------------------


def test_no_output_holds_a_forbidden_word_or_a_secret(recorded):
    world = recorded.world
    pieces = list(recorded.text)  # stdout, stderr and the prune files of every run
    for root, _dirs, names in os.walk(world.clone):
        if ".git" in Path(root).parts:
            continue
        for n in names:
            if n.endswith((".md", ".txt")):
                pieces.append((Path(root) / n).read_text(encoding="utf-8"))
    text = "\n".join(pieces)
    assert "VERIFIED" in text and "summary:" in text
    assert WORDS.findall(text) == []
    assert TOKEN not in text


def test_the_token_goes_only_to_gh_the_landed_check_and_the_evidence_push(recorded):
    runner = recorded.world.runner

    def wants_token(argv):
        prog = os.path.basename(argv[0])
        return (
            prog == "gh"
            or (prog == "bash" and argv[1].endswith("branch-landed.sh"))
            or (prog == "git" and "push" in argv)
        )

    for c in recorded.all_commands():
        env = runner._env_for(c.argv)
        assert ("GH_TOKEN" in env) == wants_token(c.argv), c.argv
        assert ("GITHUB_TOKEN" in env) == wants_token(c.argv), c.argv


def test_the_script_never_opens_a_credential_file(
    wc, spy_cls, throwaway_repo, evidence_bare, tmp_path, capsys, monkeypatch
):
    home = tmp_path / "home"
    hosts = home / ".config" / "gh" / "hosts.yml"
    envfile = home / ".env"
    for f in (hosts, envfile):
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("# placeholder, never read\n", encoding="utf-8")
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("GH_TOKEN", TOKEN)  # the token comes from the environment only
    guarded = {os.path.realpath(hosts), os.path.realpath(envfile)}
    attempts = []

    def watch(real):
        def wrapper(file, *args, **kwargs):
            if (
                isinstance(file, (str, bytes, os.PathLike))
                and os.path.realpath(file) in guarded
            ):
                attempts.append(str(file))
                raise PermissionError("credential file")
            return real(file, *args, **kwargs)

        return wrapper

    # Path.open is its own entry point (it keeps a reference to the original io.open)
    for owner, name in (
        (builtins, "open"), (io, "open"), (os, "open"), (Path, "open"),
    ):  # fmt: skip
        monkeypatch.setattr(owner, name, watch(getattr(owner, name)))
    rec = Recorder(wc, spy_cls, throwaway_repo, evidence_bare, tmp_path, capsys)
    run_every_verb(rec)
    assert attempts == []
    # the guard really works: an ordinary open of the guarded file fails
    with pytest.raises(PermissionError):
        Path(hosts).read_text()
    assert len(attempts) == 1


# -- every refusal shape of the runner ---------------------------------------------------------------------


@pytest.mark.parametrize("argv", BANNED + UNLISTED, ids=lambda a: " ".join(a))
def test_each_refusal_shape_raises_before_any_process_starts(
    wc, never_run_runner, argv
):
    with pytest.raises(wc.RefusedCommand):
        never_run_runner.check_allowed(list(argv))
    assert never_run_runner.commands == []


@pytest.mark.parametrize("tail", PUSH_REFUSED, ids=lambda t: " ".join(t))
def test_each_push_refusal_shape_raises_inside_the_evidence_clone(
    wc, runner_cls, tmp_path, tail
):
    clone = tmp_path / "clone"
    clone.mkdir()
    runner = runner_cls(evidence_dir=str(clone))
    for prefix in (["git"], ["git", "-c", HELPER]):
        with pytest.raises(wc.RefusedCommand):
            runner.check_allowed([*prefix, *tail], cwd=str(clone))
    assert runner.commands == []


def test_a_clean_that_is_not_the_exact_shape_or_not_saved_is_refused(
    wc, runner_cls, tmp_path
):
    repo = tmp_path / "wt"
    repo.mkdir()
    write(repo / "a.txt")
    runner = runner_cls(evidence_dir=str(tmp_path / "evidence"))
    for argv in (
        ["xargs", "-0", "git", "clean", "-fdx"],
        ["xargs", "-0", "git", "clean", "-f", "-x", "--", "a.txt"],
        ["git", "clean", "-f", "-x", "--", "a.txt"],
    ):
        with pytest.raises(wc.RefusedCommand):
            runner.check_allowed(argv, cwd=str(repo), stdin=b"a.txt\0")
    # the exact shape is refused until the path is registered as saved
    exact = ["xargs", "-0", "git", "clean", "-f", "-x", "--"]
    with pytest.raises(wc.RefusedCommand):
        runner.check_allowed(exact, cwd=str(repo), stdin=b"a.txt\0")
    runner.register_saved(str(repo), ["a.txt"])
    runner.check_allowed(exact, cwd=str(repo), stdin=b"a.txt\0")
