"""Shared test support for scripts/worktree_cleanup.py.

Tests never touch a real worktree: git runs only on throwaway repositories under
``tmp_path``, and ``gh``, ``orca`` and the landed-check helper are answered from
canned replies by the recording runner below. The reply shapes are hand-written from
the spec and the tool help, not literal captures of live output.
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "worktree_cleanup.py"

# A made-up lookup location for the landed check: no real file is read or run from it.
LANDED = "/h/.claude/skills/sc-closeout-protocol/scripts/branch-landed.sh"


def load_script():
    spec = importlib.util.spec_from_file_location("worktree_cleanup", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["worktree_cleanup"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="session")
def wc():
    """The script module, loaded once."""
    return load_script()


@pytest.fixture(scope="session")
def runner_cls(wc):
    """A Runner whose outside programs are answered from canned replies.

    ``replies`` maps a program name (``gh``, ``orca``, ``bash``) to a callable
    ``(argv, cwd) -> Result | None``. ``git``, ``tar`` and ``xargs`` really run when
    ``real_git`` is true (on throwaway folders only). A command with no canned reply
    gets exit code 127 and is never started.
    """

    class RecordingRunner(wc.Runner):
        def __init__(
            self, replies=None, real_git=True, evidence_dir=None, landed_paths=(LANDED,)
        ):
            super().__init__(
                evidence_dir=evidence_dir, landed_paths=tuple(landed_paths)
            )
            self.replies = dict(replies or {})
            self.real_git = real_git

        def _execute(self, argv, cwd, stdin):
            prog = os.path.basename(argv[0])
            handler = self.replies.get(prog)
            if handler is not None:
                answer = handler(argv, cwd)
                if answer is not None:
                    return answer
            if prog in ("git", "tar", "xargs") and self.real_git:
                self._require_throwaway(argv, cwd)
                return super()._execute(argv, cwd, stdin)
            return wc.Result(127, "", f"no canned reply for {argv}")

        def _require_throwaway(self, argv, cwd):
            """A real process starts only inside this test's tmp folder: fail loudly otherwise."""
            root = self.confine_root
            places = [cwd]
            for i, tok in enumerate(argv[:-1]):
                if tok == "-C":
                    places.append(os.path.join(cwd or "", argv[i + 1]))
            if os.path.basename(argv[0]) == "tar":
                places.append(argv[-1])
            for place in places:
                real = os.path.realpath(place) if place else ""
                if (
                    not root
                    or not place
                    or not (real == root or real.startswith(root + os.sep))
                ):
                    raise AssertionError(
                        f"a real {argv[0]} would start outside the test tmp folder: "
                        f"cwd={cwd!r} argv={argv}"
                    )

    RecordingRunner.confine_root = None
    return RecordingRunner


@pytest.fixture(autouse=True)
def _confine_real_processes(runner_cls, tmp_path):
    """Real git, tar and xargs may start only under this test's tmp_path."""
    runner_cls.confine_root = os.path.realpath(tmp_path)
    yield
    runner_cls.confine_root = None


class NeverRun:
    """A reply table whose handlers fail the test if a process would start."""

    def __getitem__(self, key):  # pragma: no cover - used only on failure
        raise AssertionError(f"a process would have started: {key}")


@pytest.fixture
def never_run_runner(runner_cls, tmp_path):
    """A runner that raises if a command is actually executed."""

    class Guard(runner_cls):
        def _execute(self, argv, cwd, stdin):
            raise AssertionError(f"command reached execution: {argv}")

    return Guard(evidence_dir=str(tmp_path / "evidence"))


# --- a throwaway repository --------------------------------------------------------

GITIGNORE = ".dev/local/\n.env\n__pycache__/\n.venv/\n"


def git_in(cwd, *args):
    """Run git on a throwaway repository only (never on a real worktree)."""
    env = dict(os.environ)
    env.update(
        GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0"
    )
    ident = ["-c", "user.name=t", "-c", "user.email=t@example.invalid"]
    done = subprocess.run(
        ["git", *ident, *args],
        cwd=cwd,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    return done.stdout


class ThrowawayRepo:
    """A repository under ``tmp_path`` with an ``origin`` URL that is never contacted."""

    def __init__(
        self, root: Path, origin="https://github.com/IronbellyOrg/example.git"
    ):
        self.root = root
        self.main = root / "main"
        self.main.mkdir(parents=True)
        git_in(self.main, "init", "-q", "-b", "main")
        (self.main / ".gitignore").write_text(GITIGNORE, encoding="utf-8")
        (self.main / "README.md").write_text("example\n", encoding="utf-8")
        git_in(self.main, "add", "-A")
        git_in(self.main, "commit", "-q", "-m", "first")
        git_in(self.main, "remote", "add", "origin", origin)
        # more ignored names, kept out of the tracked .gitignore so no test edits a tracked file
        exclude = self.main / ".git" / "info" / "exclude"
        with exclude.open("a", encoding="utf-8") as handle:
            handle.write("node_modules/\ndist/\n.claude/agents/\n.serena/cache/\n")

    def add_worktree(self, name: str) -> Path:
        path = self.root / "wts" / name
        path.parent.mkdir(exist_ok=True)
        git_in(self.main, "worktree", "add", "-q", "-b", name, str(path))
        return path

    def use_local_bare_origin(self) -> Path:
        """Point ``origin`` at a local bare repository (never a network address) and push main."""
        bare = self.root / "origin.git"
        git_in(self.root, "init", "-q", "--bare", "-b", "main", str(bare))
        git_in(self.main, "remote", "set-url", "origin", str(bare))
        git_in(self.main, "push", "-q", "origin", "main")
        return bare

    def add_standard_worktrees(self) -> dict[str, Path]:
        """One linked worktree for each local state the rules tell apart."""
        wts = {
            name: self.add_worktree(name)
            for name in STANDARD_NAMES
            if name != "detached"
        }
        detached = self.root / "wts" / "detached"
        git_in(self.main, "worktree", "add", "-q", "--detach", str(detached))
        wts["detached"] = detached
        (wts["tracked-edit"] / "README.md").write_text("edited\n", encoding="utf-8")
        for rel in (".dev/tasks/a.md", ".dev/local/run.log"):
            target = wts["dev-files"] / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("x\n", encoding="utf-8")
        (wts["env-file"] / ".env").write_text("NAME=placeholder\n", encoding="utf-8")
        for rel in ("pkg/__pycache__/m.pyc", ".venv/lib/x.py"):
            target = wts["build-only"] / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("x\n", encoding="utf-8")
        git_in(self.main, "worktree", "lock", str(wts["locked"]))
        return wts


STANDARD_NAMES = (
    "clean", "tracked-edit", "dev-files", "env-file", "build-only", "detached", "locked",
)  # fmt: skip


@pytest.fixture
def throwaway_repo(tmp_path):
    return ThrowawayRepo(tmp_path / "repo")


@pytest.fixture
def local_origin_repo(tmp_path):
    """A throwaway repository whose origin is a local bare repository."""
    repo = ThrowawayRepo(tmp_path / "repo")
    repo.bare = repo.use_local_bare_origin()
    return repo


@pytest.fixture
def evidence_bare(tmp_path):
    """A second local bare repository standing in for the evidence repo, with one commit."""
    seed = tmp_path / "evidence-seed"
    seed.mkdir()
    git_in(seed, "init", "-q", "-b", "main")
    (seed / "README.md").write_text("evidence\n", encoding="utf-8")
    git_in(seed, "add", "-A")
    git_in(seed, "commit", "-q", "-m", "first")
    bare = tmp_path / "evidence.git"
    git_in(tmp_path, "init", "-q", "--bare", "-b", "main", str(bare))
    git_in(seed, "push", "-q", str(bare), "main")
    return bare


def make_fake_proc(root: Path, entries: dict) -> Path:
    """A fake /proc: pid -> cwd target, None for no cwd link, 'file' for a plain file."""
    root.mkdir(parents=True, exist_ok=True)
    for pid, target in entries.items():
        entry = root / str(pid)
        entry.mkdir()
        (entry / "comm").write_text(f"proc{pid}\n", encoding="utf-8")
        if target == "file":
            (entry / "cwd").write_text("not a link\n", encoding="utf-8")
        elif target is not None:
            (entry / "cwd").symlink_to(target)
    (root / "self").mkdir()  # a non-numeric name is skipped
    return root
