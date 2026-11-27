"""Shared test support for the ``vcs`` helper of the sc-git-protocol skill.

Git runs only on throwaway repositories under ``tmp_path``. The layout follows
``tests/worktree_cleanup/conftest.py`` (the ``git_in`` helper, a throwaway repository
and a local bare remote); nothing here contacts a network address.

Fixtures: ``repo``, ``ledger_builder``, ``sidecar_builder``, ``hook_emulator``,
``submodule_repo``, ``scripts_dir`` and ``archive_mod``. The ``real_framework`` marker is registered here
with ``pytest_configure`` (``--strict-markers`` is on and ``pyproject.toml`` is not
edited).
"""

from __future__ import annotations

import importlib.util
import os
import signal
import subprocess
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE_SCRIPT = (
    ROOT / "src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py"
)
SCRIPTS = ROOT / "src/superclaude/skills/sc-git-protocol/scripts"

SHA40 = "0123456789abcdef0123456789abcdef01234567"
SHA64 = "0123456789abcdef" * 4


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "real_framework: compares a hook emulator with the real hook framework; "
        "skipped when pre-commit is not on PATH",
    )


@pytest.fixture(autouse=True)
def vcs_git_identity(monkeypatch):
    """A throwaway identity and no user or system git config for every test here."""
    for key, value in {
        "GIT_AUTHOR_NAME": "t",
        "GIT_AUTHOR_EMAIL": "t@example.invalid",
        "GIT_COMMITTER_NAME": "t",
        "GIT_COMMITTER_EMAIL": "t@example.invalid",
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_TERMINAL_PROMPT": "0",
    }.items():
        monkeypatch.setenv(key, value)


def git_in(cwd, *args, config=(), check=True):
    """Run git on a throwaway repository only (never on a real worktree).

    ``config`` is a list of ``key=value`` strings passed as ``-c`` options.
    Returns stdout; with ``check=False`` returns ``(returncode, stdout)``.
    """
    env = dict(os.environ)
    env.update(
        GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0"
    )
    opts = []
    for item in config:
        opts += ["-c", item]
    done = subprocess.run(
        ["git", *opts, *args],
        cwd=cwd,
        env=env,
        check=check,
        capture_output=True,
        text=True,
    )
    return done.stdout if check else (done.returncode, done.stdout)


# --- a throwaway repository with a local bare remote ---------------------------------
class Repo:
    """A work tree on ``main`` whose ``origin`` is a local bare repository."""

    def __init__(self, root: Path):
        self.root = root
        self.work = root / "work"
        self.bare = root / "origin.git"
        self.work.mkdir(parents=True)
        git_in(root, "init", "-q", "--bare", "-b", "main", str(self.bare))
        git_in(self.work, "init", "-q", "-b", "main")
        git_in(self.work, "config", "user.name", "t")
        git_in(self.work, "config", "user.email", "t@example.invalid")
        self.write("README.md", "example\n")
        self.commit("first")
        git_in(self.work, "remote", "add", "origin", str(self.bare))
        git_in(self.work, "push", "-q", "-u", "origin", "main")

    def git(self, *args, **kw):
        return git_in(self.work, *args, **kw)

    def write(self, rel: str, text: str) -> Path:
        path = self.work / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def commit(self, message: str) -> str:
        """Stage everything, commit, and return the new commit sha."""
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)
        return self.git("rev-parse", "HEAD").strip()


@pytest.fixture
def repo(tmp_path):
    return Repo(tmp_path / "repo")


# --- the implement ledger (grammar: refs/ledger.md, regexes: archive_workspace.py) -----
class LedgerBuilder:
    """Appends ledger lines in the closed grammar; ``write()`` saves them.

    Every method returns ``self`` so calls chain. The lines are built from the
    grammar, not copied from a real run; ``archive_workspace._parse_ledger`` is the
    check that they match.
    """

    def __init__(self, path: Path):
        self.path = path
        self.lines: list[str] = []

    def add(self, line: str):
        self.lines.append(line)
        return self

    def header(
        self, source="./TASK-WF-x-20261001-063000.md", created="2026-10-01T06:30:00Z"
    ):
        return self.add(f"# implement ledger — source: {source} — created: {created}")

    def plan(self, plan_sha="0" * 64, source_sha="1" * 64):
        return self.add(f"PLAN: sha256={plan_sha} source_sha256={source_sha}")

    def start(self, tid, sha=SHA40):
        return self.add(f"T{tid}: start sha={sha}")

    def _verdict(self, tid, status, verdict, files):
        return self.add(
            f"T{tid}: {status} verdict={verdict} ac=T{tid}.AC1 "
            f"evidence=src/foo.py:12,T{tid}.AC1 "
            f"extras=lint:skip,typecheck:skip,test:skip files={files}"
        )

    def complete(self, tid, verdict="compliant", files="src/foo.py"):
        return self._verdict(tid, "complete", verdict, files)

    def blocked(self, tid, verdict="missing", files="src/foo.py"):
        return self._verdict(tid, "blocked", verdict, files)

    def ruling(
        self, tid, text="accept the gap — scope was deferred — cost-if-wrong: none"
    ):
        return self.add(f"T{tid}: Ruling: {text}")

    def retry_open(self, tid, n=3, checkpoint=SHA40, tier="T2Model02"):
        return self.add(
            f"T{tid}: retry n={n} step=open checkpoint={checkpoint} tier={tier}"
        )

    def retry_revert(self, tid, n=3):
        supersedes = "none" if n == 3 else f"T{tid}_brief-{n - 1}.md"
        return self.add(
            f"T{tid}: retry n={n} step=revert "
            f"brief=./artifacts/retries/T{tid}_brief-{n}.md supersedes={supersedes}"
        )

    def retry_review(self, tid, n=3):
        return self.add(f"T{tid}: retry n={n} step=review")

    def halt(self, tid, review=2, reason="budget"):
        return self.add(f"T{tid}: halt review={review} reason={reason}")

    def final(self, status="pass", evidence="src/foo.py:12", state="2" * 64):
        return self.add(f"FINAL: {status} evidence={evidence} state={state}")

    def archive(self, rest="start id=TASK-WF-x-20261001-063000 token=0123456789abcdef"):
        return self.add(f"ARCHIVE: {rest}")

    def text(self) -> str:
        return "".join(line + "\n" for line in self.lines)

    def write(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(self.text(), encoding="utf-8")
        return self.path


@pytest.fixture
def ledger_builder(tmp_path):
    """Factory: ``ledger_builder()`` or ``ledger_builder(path)`` gives a builder."""

    def make(path=None):
        return LedgerBuilder(
            Path(path) if path else tmp_path / "ledger" / "progress.md"
        )

    return make


@pytest.fixture(scope="session")
def archive_mod():
    """``archive_workspace.py`` loaded by path (the same way tests/skills does)."""
    spec = importlib.util.spec_from_file_location("archive_workspace", ARCHIVE_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --- the sidecar commits.md (line forms: FR-100 and FR-120) -----------------------------
class SidecarBuilder:
    """Appends ``commits.md`` lines in the forms of FR-100 and FR-120."""

    def __init__(self, path: Path):
        self.path = path
        self.lines: list[str] = []

    @staticmethod
    def ledger_k(ledger: Path) -> int:
        """FR-102: newline bytes, plus one when the file is not empty and unterminated."""
        data = Path(ledger).read_bytes()
        return data.count(b"\n") + (1 if data and not data.endswith(b"\n") else 0)

    def raw(self, line: str):
        self.lines.append(line)
        return self

    def run(
        self, n, mode="on", ledger_lines=0, branch="refs/heads/feature/x",
        revoked=False, at="2026-10-01T06:30:00Z", args="--commit-tasks",
        source="./plan.md", worktree="wt1",
    ):  # fmt: skip
        reason = " reason=revoked" if revoked else ""
        return self.raw(
            f"run {n}: commit-tasks={mode}{reason} ledger-lines={ledger_lines} "
            f'branch={branch} at={at} args="{args}" source={source} worktree={worktree}'
        )

    def prepared(
        self, ids, key=SHA64, attempt=1, parent=SHA40, branch="refs/heads/feature/x",
        paths=SHA64, accepted="refs/superclaude/boundary/a", plan="-", source="-",
    ):  # fmt: skip
        return self.raw(
            f"T{ids}: commit prepared key={key} attempt={attempt} parent={parent} "
            f"branch={branch} paths={paths} accepted={accepted} plan={plan} source={source}"
        )

    def commit(
        self, ids, key=SHA64, attempt=1, sha=SHA40, recovered=False,
        outside_changed=None, wt=None,
    ):  # fmt: skip
        word = "recovered" if recovered else "sha"
        extra = ""
        if outside_changed is not None:
            extra = f" outside-changed={outside_changed} wt={wt}"
        return self.raw(
            f"T{ids}: commit {word}={sha} key={key} attempt={attempt}{extra}"
        )

    def skipped(self, ids, key=SHA64, reason="empty"):
        return self.raw(f"T{ids}: commit skipped key={key} reason={reason}")

    def refused(
        self, ids, key=SHA64, attempt=1, reason="hook-failed", rewritten=None,
        uncertain=False,
    ):  # fmt: skip
        word = "uncertain" if uncertain else "refused"
        extra = f" rewritten={rewritten}" if rewritten else ""
        return self.raw(
            f"T{ids}: commit {word} key={key} attempt={attempt} reason={reason}{extra}"
        )

    @staticmethod
    def _quote(text: str) -> str:
        return text.replace("\\", "\\\\").replace('"', '\\"')

    def resolved_abandoned(self, ids, key=SHA64, at="2026-10-02", quote="abandon it"):
        return self.raw(
            f'T{ids}: commit resolved key={key} as=abandoned at={at} quote="{self._quote(quote)}"'
        )

    def resolved_adopted(
        self, ids, key=SHA64, head=SHA40, basis="candidate", differs=0,
        at="2026-10-02", quote="adopt it",
    ):  # fmt: skip
        return self.raw(
            f"T{ids}: commit resolved key={key} as=adopted head={head} basis={basis} "
            f'differs={differs} at={at} quote="{self._quote(quote)}"'
        )

    def write(self, trailing_newline=True):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        text = "\n".join(self.lines)
        if trailing_newline and self.lines:
            text += "\n"
        self.path.write_text(text, encoding="utf-8")
        return self.path


@pytest.fixture
def sidecar_builder(tmp_path):
    return SidecarBuilder(tmp_path / "ledger" / "commits.md")


# --- a superproject with a file:// submodule ----------------------------------------------
class SubmoduleRepo(Repo):
    """A superproject on ``main`` with one submodule at ``libs/lib`` named ``lib``.

    ``protocol.file.allow=always`` is set only in the superproject's own local config
    and as a ``-c`` option on the commands that clone; no global or system config is
    touched.
    """

    sub_path = "libs/lib"

    def __init__(self, root: Path):
        super().__init__(root)
        self.sub_origin = root / "lib-origin"
        self.sub_origin.mkdir()
        git_in(self.sub_origin, "init", "-q", "-b", "main")
        git_in(self.sub_origin, "config", "user.name", "t")
        git_in(self.sub_origin, "config", "user.email", "t@example.invalid")
        (self.sub_origin / "lib.txt").write_text("lib\n", encoding="utf-8")
        git_in(self.sub_origin, "add", "-A")
        git_in(self.sub_origin, "commit", "-q", "-m", "lib first")
        self.git("config", "protocol.file.allow", "always")
        self.git(
            "submodule", "add", "--name", "lib", sub_url(self.sub_origin), self.sub_path,
            config=["protocol.file.allow=always"],
        )  # fmt: skip
        self.git("commit", "-q", "-m", "add submodule")
        self.git("push", "-q", "origin", "main")


def sub_url(path: Path) -> str:
    return "file://" + str(path)


@pytest.fixture
def submodule_repo(tmp_path):
    return SubmoduleRepo(tmp_path / "super")


# --- a hook-manager emulator (FR-118) -------------------------------------------------------
# The hook below replays the command sequence of ``pre_commit/staged_files_only.py`` from
# the pre-commit framework, version 4.6.2 as installed from PyPI by ``uv run --with
# pre-commit`` (the version the spike in test_precommit_spike.py ran against; see
# artifacts/precommit-spike.md). Under ``git commit --only`` the hook sees a temporary
# index (HEAD plus the commit set S), so every change outside S counts as "unstaged".
#   1. tree = git write-tree
#   2. git diff-index --ignore-submodules --binary --exit-code --no-color --no-ext-diff tree --
#   3. exit 1 with a diff: save it as patch<time>-<pid> in the cache folder, then
#      git -c submodule.recurse=0 checkout -- .
#   4. run the hook action
#   5. git apply --whitespace=nowarn <patch> (retry with core.autocrlf=false; on failure
#      check out again and apply once more)
# There is no signal handler, as in the framework: a SIGKILL (or SIGTERM) during step 4
# leaves the person's edit only in the saved patch. The intent-to-add step of the
# framework is not replayed (not needed by the cases in FR-118 covered here).
_HOOK_TEMPLATE = """#!/bin/sh
PATCH_DIR='{patch_dir}'
ACTION='{action_script}'
tree=$(git write-tree) || exit 1
mkdir -p "$PATCH_DIR"
tmp="$PATCH_DIR/diff.$$"
git diff-index --ignore-submodules --binary --exit-code --no-color --no-ext-diff "$tree" -- > "$tmp"
rc=$?
patch=
if [ "$rc" -eq 1 ] && [ -s "$tmp" ]; then
    patch="$PATCH_DIR/patch$(date +%s)-$$"
    mv "$tmp" "$patch"
    git -c submodule.recurse=0 checkout -- . || exit 1
elif [ "$rc" -gt 1 ]; then
    rm -f "$tmp"
    exit 1
else
    rm -f "$tmp"
fi
sh "$ACTION"
arc=$?
if [ -n "$patch" ]; then
    if ! git apply --whitespace=nowarn "$patch" &&
       ! git -c core.autocrlf=false apply --whitespace=nowarn "$patch"; then
        git -c submodule.recurse=0 checkout -- .
        git apply --whitespace=nowarn "$patch"
    fi
fi
exit $arc
"""

# The hook action is a separate script so the real framework can run the same one as a
# ``repo: local`` hook. The first word of the action file picks the behavior.
_ACTION_TEMPLATE = """#!/bin/sh
read -r kind target < '{action_file}'
case "$kind" in
    pass) exit 0 ;;
    exit1) exit 1 ;;
    rewrite_exit1) echo rewritten-by-hook >> "$target"; exit 1 ;;
    rewrite_add) echo rewritten-by-hook >> "$target"; git add -- "$target"; exit 0 ;;
    block) : > '{started}'; exec sleep 600 ;;
esac
exit 2
"""

HOOK_ACTIONS = ("pass", "exit1", "rewrite_exit1", "rewrite_add", "block")


class HookEmulator:
    """Installs the framework-replay ``pre-commit`` hook in a ``Repo``.

    ``set_action(kind, target=None)`` picks what the hook does between the stash step
    and the restore step. ``commit(paths)`` runs ``git commit --only`` on those paths;
    ``start_blocked_commit(paths)`` starts one in its own process group and waits until
    the hook is blocked, so a test can kill the group.
    """

    def __init__(self, repo: Repo, folder: Path):
        self.repo = repo
        self.folder = folder
        self.cache = folder / "cache"
        self.action_file = folder / "action"
        self.action_script = folder / "action.sh"
        self.started = folder / "started"
        folder.mkdir(parents=True, exist_ok=True)
        self.action_script.write_text(
            _ACTION_TEMPLATE.format(action_file=self.action_file, started=self.started),
            encoding="utf-8",
        )
        hook = repo.work / ".git" / "hooks" / "pre-commit"
        hook.write_text(
            _HOOK_TEMPLATE.format(
                patch_dir=self.cache, action_script=self.action_script
            ),
            encoding="utf-8",
        )
        hook.chmod(0o755)
        self.set_action("pass")

    def set_action(self, kind: str, target: str | None = None):
        assert kind in HOOK_ACTIONS, kind
        self.action_file.write_text(f"{kind} {target or '-'}\n", encoding="utf-8")

    def _argv(self, paths, message):
        return ["git", "commit", "-q", "--only", "-m", message, "--", *paths]

    def commit(self, paths, message="task commit", timeout=60):
        """Run the commit; returns the CompletedProcess (never raises on rc != 0)."""
        return subprocess.run(
            self._argv(paths, message),
            cwd=self.repo.work,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

    def start_blocked_commit(self, paths, message="task commit", wait=30):
        """Start a commit whose hook blocks; returns the Popen once the hook has begun."""
        self.set_action("block")
        proc = subprocess.Popen(
            self._argv(paths, message),
            cwd=self.repo.work,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        deadline = time.monotonic() + wait
        while not self.started.exists():
            if proc.poll() is not None or time.monotonic() > deadline:
                if proc.poll() is None:
                    os.killpg(proc.pid, signal.SIGKILL)
                out = proc.communicate(timeout=30)
                raise AssertionError(f"hook never reached the block action: {out}")
            time.sleep(0.05)
        return proc

    @staticmethod
    def kill_group(proc, sig=signal.SIGKILL):
        os.killpg(proc.pid, sig)
        proc.communicate(timeout=30)

    def patches(self) -> list[Path]:
        """The patch files the hook saved (the framework keeps them after a restore)."""
        return sorted(self.cache.glob("patch*")) if self.cache.is_dir() else []


@pytest.fixture
def hook_emulator(repo, tmp_path):
    return HookEmulator(repo, tmp_path / "hook-emulator")


# --- the helper scripts folder (created by a later task) -----------------------------------
def use_scripts_dir(monkeypatch, folder: Path = SCRIPTS) -> Path:
    """Put the helper scripts folder first on ``sys.path``; skip while it is absent."""
    if not folder.is_dir():
        pytest.skip(f"helper scripts folder does not exist yet: {folder}")
    monkeypatch.syspath_prepend(str(folder))
    return folder


@pytest.fixture
def scripts_dir(monkeypatch):
    return use_scripts_dir(monkeypatch)
