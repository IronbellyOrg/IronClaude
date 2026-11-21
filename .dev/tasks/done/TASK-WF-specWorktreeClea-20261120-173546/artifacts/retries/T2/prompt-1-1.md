6cc89734a79f8ee9834b04288bf19c6c08ae4997
Review one task for spec compliance.

Task brief: ## Task 2: Create the script skeleton with the allowlisted command runner

Depends on: Task 1

Create `scripts/worktree_cleanup.py` (new, Python standard library only; modelled on the stdlib style of `scripts/merged_pr_log.py`, which has `parse_args` and `main`). Top of the file: Jay Wedgeworth's Apache-2.0 notice block (source `github.com/Simple-With-Us/AI-Fleet-Coordinator`, copyright 2026 Jay Wedgeworth, rules adapted from `scripts/fleet_lanes/retire.py`, `docs/protocols/lane-map.md` and `scripts/disk-janitor.sh`, what was changed: see `scripts/worktree_cleanup_PROVENANCE.md`, which Task 19 writes). Then a plain-English module docstring and these parts: constants (idle floor from `WORKTREE_CLEANUP_IDLE_DAYS` default 7, `RUN_EVIDENCE_REPO` default `IronbellyOrg/run-evidence`, `RUN_EVIDENCE_DIR` default `~/workspaces/run-evidence`, archive part size 85 MB as a module constant so tests can lower it, owners `IronbellyOrg` and `IronbellyGroup`, the name guard `orca-port-`, `orca-recipe-`, `orca-pristine-` as prefixes and `orca-old-patched` as an exact name, the fixed build-output list of source section 6 rule 5, exit codes 0, 64, 69); one `Runner` class that is the only way the script starts an outside program (argument list, no shell, `GH_TOKEN` passed only through the environment of `gh` and `git push`) with a `check_allowed` step, adapted from Jay's runner, that is a positive allowlist (it names the allowed command shapes: the read verbs of `git`, `gh` and `orca`, `tar`, `branch-landed.sh`, and the named write verbs of the pipeline, `git worktree remove`, `git branch -d`, `orca terminal close`, `orca worktree rm`, `xargs -0 git clean`, and in the evidence clone only `git clone`, `git fetch`, `git add`, `git commit`, `git rebase` and `git push`) and refuses every other command before any process starts, with these shapes refused even inside an allowed verb: `--force` or `-f` on `orca worktree rm` or `git worktree remove`, `git branch -D`, `rm`, `git worktree prune`, `git push` with a delete flag or a `:ref` refspec, `git push` when the working folder is not the evidence clone, and `git clean` unless it is exactly `-f -x --` (run through `xargs -0` with `GIT_LITERAL_PATHSPECS=1`) and every path on its standard input is one of the paths registered as saved and verified (the registration call is added in Task 11); the runner records every command (argument list and working folder) in a list and has one overridable `_execute` hook so tests can answer `gh`, `orca` and `branch-landed.sh` from recorded shapes while real `git` runs on throwaway repos. Add `parse_args` and `main(argv, runner=None)` with the four verbs `list`, `archive <worktree>`, `retire <worktree>` and `prune`, the flags `--apply` and `--out <dir>` (default `~/.local/state/worktree-cleanup`, chosen so nothing is written inside any worktree), dry run as the default, and the verb bodies as stubs that exit 64 with "not built yet" until Tasks 11 and 12 fill them in. The file never reads `~/.config/gh/hosts.yml` or `~/.env`. This task also creates `tests/worktree_cleanup/__init__.py`, a first `tests/worktree_cleanup/conftest.py` (the script loader and a recording runner built on `Runner`) and `tests/worktree_cleanup/test_runner.py`, so its own checks pass when it ends: the refusals of each banned shape, the refusal of an unlisted command such as `git reset`, and the `--help` output.

Acceptance criteria:
- `uv run --no-project python scripts/worktree_cleanup.py --help` lists the four verbs and the two flags; `main(["list"], runner=...)` can be called from a test with an injected runner.
- `Runner.check_allowed` raises a dedicated refusal error for each banned shape listed above before any process starts and for an unlisted command such as `git reset` (asserted in `tests/worktree_cleanup/test_runner.py`, which this task creates; Task 13 extends them across every verb).
- An `ast` scan of the file finds only standard library imports and no call to `os.remove`, `os.unlink`, `shutil.rmtree` or a command named `rm`.
- The Apache-2.0 notice block and the pointer to `scripts/worktree_cleanup_PROVENANCE.md` are at the top of the file.

AC ids (in source order): T2.AC1, T2.AC2, T2.AC3, T2.AC4
Global constraints: ## Constraints

- Safety for this whole run (set by the issue owner): tests use throwaway git repositories, a local bare repository standing in for the evidence repo, and a fake runner with recorded `gh`, `git` and `orca` replies. No task and no test runs the script with `--apply` against real worktrees, removes, moves or clears any real worktree or file, creates or switches on an Orca automation (the definition is a file, status "written, not switched on"), closes a real Orca terminal, or pushes to `IronbellyOrg/run-evidence`. The only run against the real workspace is a dry run (Task 20).
- The script never uses `--force` on `orca worktree rm` or `git worktree remove`, never `git branch -D`, never `rm`, never `git worktree prune`, never pushes anywhere but the evidence repo's clone, and never deletes a remote branch. The only force flag in the whole script is `git clean -f -x --` on exact paths listed in a verified `saved-paths.txt` (source sections 3, 6 and 8, decision 1).
- The script never deletes a file or folder itself (no `rm`, no `shutil.rmtree`, no `unlink`): its lock files stay in place under `fcntl.flock`, and a scratch folder left by a failed save stays and is named in the log. This plan chose that so "never rm" holds without exception.
- Python standard library only, no model call, no agent or model name in any output, credentials only from the environment (`GH_TOKEN`), no credential file is ever opened by the script, no secret is printed or written (source sections 5, 6 and 9).
- The 11 decisions of source section 8 are final. Out of scope (source section 10): where worktrees live (#289, #322), Jay's other pieces, the closeout itself (#668, so `/sc:closeout` and its files and tests are not changed), any shared or remote branch, anything that is not a git worktree of our repos.
- The change to the separate `IronbellyOrg/run-evidence` repo (source section 15, step 5) is prepared as text under `./artifacts/` and not applied by this plan; no other repo is pushed to.
- The spec mentions that `archive` by hand "can still save" tracked edits and later commits "as a patch and a bundle" (source section 7, "What is not saved"). It gives no step, format or folder for it, so it is not built; Task 12 records that in the verb's help text so it is not a silent drop.
- Where the spec is silent this plan decides, and says so in the task: `/sc:worktrees` goes on the never-as-worker list (Task 16); outside an IronClaude checkout the command stops and runs nothing (Task 14); the default `--out` folder is `~/.local/state/worktree-cleanup` so nothing is ever written inside a worktree (Task 2); `/sc:closeout` is left unchanged (this constraint).
- Edit only under `src/superclaude/`, `scripts/`, `tests/`, `docs/`, `plugins/superclaude/skills/sc-recommend/refs/`, `CHANGELOG.md` and `NOTICE`; run `make sync-dev` after editing `src/superclaude/` and never edit the `.claude/` copies. Plain English and no em or en dashes in every new file. A command file must not point at another primitive through a `src/superclaude/...` path.
- The pull request for this change is opened by the finishing step of the run, `/sc:pr-submit --monitor 3` (source section 15, step 7), after the last task; no task of this plan opens it.
- Corrections the implementer made to this plan before the first task started, from the advisory reflect review of the plan (the list is in `./artifacts/plan-corrections.md`): Task 1 (the item 1 fallback, the open pull request proof, item 7), Task 2 (a positive allowlist runner and its own first tests), Tasks 3 to 5 (their own tests, so no check waits for a later task), Task 7 (shared fixtures only), Tasks 11 and 12 (Orca read back, the command list in the JSON), Task 14 (the write-verb classification), Task 19 (15 rows), Task 20 (dependencies).
Start sha: 6cc89734a79f8ee9834b04288bf19c6c08ae4997
Diff against the start snapshot: 
===== new file: scripts/worktree_cleanup.py =====
#!/usr/bin/env python3
# Rules adapted from three files in https://github.com/Simple-With-Us/AI-Fleet-Coordinator
# (scripts/fleet_lanes/retire.py, docs/protocols/lane-map.md, scripts/disk-janitor.sh),
# Copyright 2026 Jay Wedgeworth, licensed under the Apache License, Version 2.0.
# Changed by IronClaude: the rules, the runner, the archive step and every command are
# rewritten for git worktrees of IronbellyOrg repos. See scripts/worktree_cleanup_PROVENANCE.md.
"""Remove git worktrees of our own repos once their work is finished, and nothing else.

A worktree is removed only when all eight rules hold: it is a linked worktree of one of
our repos, its own pull request is merged, nothing was added after that pull request,
every issue it relates to is closed, nothing unsaved is in it, nothing but its own Orca
terminals is using it, it has been idle for the idle floor, and it is not pinned.
Untracked and ignored files under ``.dev/`` are first saved to the evidence repo and
checked against GitHub. Every step fails closed: if anything cannot be read or
completed, the worktree is kept and the reason is shown.

Verbs (a dry run unless --apply is given):
  list                 table of every worktree of every repo of ours, never removes
  archive <worktree>   only the save step, never removes
  retire <worktree>    remove one worktree whose work is safe
  prune                the same decision for every worktree

Environment (names only; credentials come from the environment and nowhere else):
  GH_TOKEN                     token for gh and for the push to the evidence repo
  RUN_EVIDENCE_REPO            default IronbellyOrg/run-evidence
  RUN_EVIDENCE_DIR             local clone, default ~/workspaces/run-evidence
  WORKTREE_CLEANUP_IDLE_DAYS   idle floor in days, default 7

Usage:
  uv run --no-project python scripts/worktree_cleanup.py <verb> [--apply] [--out DIR]
"""

from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

# --- constants -------------------------------------------------------------

IDLE_DAYS_DEFAULT = 7
EVIDENCE_REPO_DEFAULT = "IronbellyOrg/run-evidence"
EVIDENCE_DIR_DEFAULT = "~/workspaces/run-evidence"
DEFAULT_OUT = "~/.local/state/worktree-cleanup"

# GitHub refuses a file over 100 MB; ignored archives are split into parts of this size.
# A module constant so a test can lower it.
ARCHIVE_PART_BYTES = 85 * 1024 * 1024

OWNERS = ("ironbellyorg", "ironbellygroup")

# Second guard: infrastructure and port folders are never touched, even if git lists them.
NAME_GUARD_PREFIXES = ("orca-port-", "orca-recipe-", "orca-pristine-")
NAME_GUARD_EXACT = ("orca-old-patched",)

# Ignored names that are build output or generated copies, not local state (rule 5).
BUILD_OUTPUT_NAMES = frozenset(
    {
        "__pycache__",
        ".venv",
        ".codegraph",
        ".ruff_cache",
        ".pytest_cache",
        ".mypy_cache",
        "node_modules",
        "dist",
        "build",
        "uv.lock",
    }
)
BUILD_OUTPUT_PATHS = (
    (".serena", "cache"),
    (".claude", "agents"),
    (".claude", "commands"),
    (".claude", "hooks"),
    (".claude", "skills"),
    (".claude", "templates"),
)

EXIT_OK = 0
EXIT_USAGE = 64
EXIT_FAILED = 69

VERBS = ("list", "archive", "retire", "prune")

CREDENTIAL_HELPER = "credential.helper=!gh auth git-credential"


# --- the one runner --------------------------------------------------------


class RefusedCommand(Exception):
    """A command the allowlist does not name, or one of the always-banned shapes."""


@dataclass
class CommandRecord:
    argv: list[str]
    cwd: str | None
    stdin_paths: int = 0


@dataclass
class Result:
    returncode: int
    stdout: str = ""
    stderr: str = ""


@dataclass
class Runner:
    """The only way this script starts an outside program.

    ``check_allowed`` is a positive allowlist: it names the allowed command shapes and
    refuses everything else before any process starts. Every command that passes is
    recorded (argument list and working folder), so a test can read the whole list.
    """

    evidence_dir: str | None = None
    commands: list[CommandRecord] = field(default_factory=list)
    # Paths saved and verified in the evidence repo, per worktree folder (real path).
    saved_paths: dict[str, set[str]] = field(default_factory=dict)
    # Worktree selectors whose Orca terminals may be closed (every other rule passed
    # and the save is verified).
    close_authorized: set[str] = field(default_factory=set)

    # -- authorization registered by the pipeline --------------------------------

    def register_saved(self, worktree: str, paths: list[str]) -> None:
        self.saved_paths.setdefault(os.path.realpath(worktree), set()).update(paths)

    def authorize_close(self, selector: str) -> None:
        self.close_authorized.add(selector)

    # -- the allowlist ---------------------------------------------------------

    def _in_evidence_dir(self, cwd: str | None) -> bool:
        if not self.evidence_dir or cwd is None:
            return False
        return os.path.realpath(cwd) == os.path.realpath(self.evidence_dir)

    def check_allowed(
        self,
        argv: list[str],
        cwd: str | None = None,
        stdin: bytes | None = None,
    ) -> None:
        if not argv:
            raise RefusedCommand("empty command")
        prog = os.path.basename(argv[0])
        if prog == "git":
            self._check_git(argv[1:], cwd)
        elif prog == "gh":
            self._check_gh(argv[1:])
        elif prog == "orca":
            self._check_orca(argv[1:])
        elif prog == "tar":
            if not (len(argv) == 3 and argv[1] == "-tzf"):
                raise RefusedCommand("tar is allowed only as: tar -tzf <archive>")
        elif prog == "xargs":
            self._check_xargs(argv[1:], cwd, stdin)
        elif prog == "bash" and len(argv) == 3 and self._is_landed_check(argv[1]):
            self._check_landed_args(argv[2])
        elif self._is_landed_check(argv[0]) and len(argv) == 2:
            self._check_landed_args(argv[1])
        else:
            raise RefusedCommand(f"command not on the allowlist: {shlex.join(argv)}")

    @staticmethod
    def _is_landed_check(path: str) -> bool:
        return path.replace("\\", "/").endswith(
            "sc-closeout-protocol/scripts/branch-landed.sh"
        )

    @staticmethod
    def _check_landed_args(arg: str) -> None:
        if not arg.lstrip("#").isdigit():
            raise RefusedCommand("branch-landed.sh takes one pull request number")

    # git ----------------------------------------------------------------------

    _GIT_READ = {
        "status",
        "rev-parse",
        "log",
        "ls-files",
        "merge-base",
        "diff",
        "show",
        "cat-file",
        "for-each-ref",
        "rev-list",
        "show-ref",
        "check-ignore",
    }
    _GIT_EVIDENCE_ONLY = {"clone", "fetch", "add", "commit", "rebase", "push"}

    def _check_git(self, args: list[str], cwd: str | None) -> None:
        rest = list(args)
        in_clone_dir = False
        while rest and rest[0] in ("-C", "-c"):
            flag = rest.pop(0)
            if not rest:
                raise RefusedCommand("git option without a value")
            value = rest.pop(0)
            if flag == "-c":
                if value != CREDENTIAL_HELPER:
                    raise RefusedCommand(
                        f"git -c is allowed only for {CREDENTIAL_HELPER}"
                    )
            else:
                cwd = value
        in_clone_dir = self._in_evidence_dir(cwd)
        if not rest:
            raise RefusedCommand("git with no verb")
        verb, tail = rest[0], rest[1:]
        if verb in self._GIT_READ:
            return
        if verb == "remote":
            if tail[:1] == ["get-url"] and len(tail) == 2:
                return
            raise RefusedCommand("git remote is allowed only as: remote get-url <name>")
        if verb == "config":
            if tail[:1] == ["--get"] and len(tail) == 2:
                return
            raise RefusedCommand("git config is allowed only as: config --get <key>")
        if verb == "worktree":
            self._check_git_worktree(tail)
            return
        if verb == "branch":
            self._check_git_branch(tail)
            return
        if verb in self._GIT_EVIDENCE_ONLY:
            self._check_git_evidence(verb, tail, in_clone_dir, rest)
            return
        raise RefusedCommand(f"git {verb} is not on the allowlist")

    @staticmethod
    def _check_git_worktree(tail: list[str]) -> None:
        if tail[:1] == ["list"]:
            return
        if tail[:1] == ["prune"]:
            raise RefusedCommand(
                "git worktree prune is never run: a missing folder can mean a disk is not mounted"
            )
        if tail[:1] == ["remove"]:
            extras = [t for t in tail[1:] if t.startswith("-")]
            if extras or len(tail) != 2:
                raise RefusedCommand(
                    "git worktree remove takes one path and no option, never --force"
                )
            return
        raise RefusedCommand("git worktree is allowed only as: list, remove <path>")

    @staticmethod
    def _check_git_branch(tail: list[str]) -> None:
        if tail[:1] == ["--list"] or tail[:1] == ["--show-current"]:
            return
        if tail[:1] == ["-d"] and len(tail) == 2 and not tail[1].startswith("-"):
            return
        if "-D" in tail or "--delete" in tail:
            raise RefusedCommand("git branch -D is never run, only git branch -d")
        raise RefusedCommand(
            "git branch is allowed only as: --list, --show-current, -d <name>"
        )

    def _check_git_evidence(
        self, verb: str, tail: list[str], in_clone_dir: bool, rest: list[str]
    ) -> None:
        if verb == "clone":
            # clone <url-or-repo> <evidence dir>
            if (
                len(tail) == 2
                and self.evidence_dir
                and (os.path.realpath(tail[1]) == os.path.realpath(self.evidence_dir))
            ):
                return
            raise RefusedCommand("git clone is allowed only into the evidence folder")
        if not in_clone_dir:
            raise RefusedCommand(f"git {verb} runs only inside the evidence clone")
        if verb == "push":
            bad = {
                "--delete",
                "-d",
                "--force",
                "-f",
                "--force-with-lease",
                "--mirror",
                "--prune",
                "--all",
            }
            if any(t in bad or t.startswith("--force") for t in tail):
                raise RefusedCommand("git push never deletes a branch and never forces")
            if any(
                t.startswith(":") or ":" in t.lstrip("+")
                for t in tail
                if not t.startswith("-")
            ):
                raise RefusedCommand(
                    "git push never uses a delete or rewriting refspec"
                )
            if any(t.startswith("+") for t in tail):
                raise RefusedCommand("git push never forces a refspec")
            return
        if verb == "rebase" and any(
            t.startswith("-i") or t == "--interactive" for t in tail
        ):
            raise RefusedCommand("git rebase is never interactive")

    # gh -----------------------------------------------------------------------

    def _check_gh(self, args: list[str]) -> None:
        if len(args) >= 2 and args[:2] in (
            ["pr", "list"],
            ["pr", "view"],
            ["issue", "view"],
            ["issue", "list"],
        ):
            if "--repo" not in args and "-R" not in args:
                raise RefusedCommand("gh needs an explicit --repo <owner>/<repo>")
            return
        if len(args) >= 3 and args[:2] == ["repo", "clone"]:
            if self.evidence_dir and os.path.realpath(
                args[3] if len(args) > 3 else ""
            ) == os.path.realpath(self.evidence_dir):
                return
            raise RefusedCommand(
                "gh repo clone is allowed only into the evidence folder"
            )
        raise RefusedCommand(f"gh {' '.join(args[:2])} is not on the allowlist")

    # orca ---------------------------------------------------------------------

    def _check_orca(self, args: list[str]) -> None:
        head = args[:2]
        if head in (
            ["repo", "list"],
            ["worktree", "list"],
            ["worktree", "ps"],
            ["reference", "list"],
            ["terminal", "list"],
        ):
            return
        if head == ["worktree", "rm"]:
            if "--force" in args or "-f" in args:
                raise RefusedCommand("orca worktree rm is never run with --force")
            return
        if head == ["terminal", "close"]:
            if "--all" not in args or "--worktree" not in args:
                raise RefusedCommand(
                    "orca terminal close needs --worktree <selector> --all"
                )
            sel = (
                args[args.index("--worktree") + 1]
                if args.index("--worktree") + 1 < len(args)
                else ""
            )
            if sel not in self.close_authorized:
                raise RefusedCommand(
                    "orca terminal close before every other rule passed and the save was verified"
                )
            return
        raise RefusedCommand(f"orca {' '.join(head)} is not on the allowlist")

    # xargs git clean ------------------------------------------------------------

    def _check_xargs(
        self, args: list[str], cwd: str | None, stdin: bytes | None
    ) -> None:
        if args != ["-0", "git", "clean", "-f", "-x", "--"]:
            raise RefusedCommand(
                "xargs is allowed only as: xargs -0 git clean -f -x --"
            )
        if cwd is None or stdin is None:
            raise RefusedCommand("git clean needs a worktree folder and a path list")
        allowed = self.saved_paths.get(os.path.realpath(cwd), set())
        paths = [p for p in stdin.decode("utf-8", "surrogateescape").split("\0") if p]
        if not paths:
            raise RefusedCommand("git clean with no paths")
        outside = [p for p in paths if p not in allowed]
        if outside:
            raise RefusedCommand(
                f"git clean refused for a path not in the saved list: {outside[0]}"
            )

    # -- running ---------------------------------------------------------------

    def run(
        self,
        argv: list[str],
        cwd: str | None = None,
        stdin: bytes | None = None,
    ) -> Result:
        self.check_allowed(argv, cwd, stdin)
        n_paths = len([p for p in stdin.split(b"\0") if p]) if stdin else 0
        self.commands.append(CommandRecord(list(argv), cwd, n_paths))
        return self._execute(argv, cwd, stdin)

    def _env_for(self, argv: list[str]) -> dict[str, str]:
        env = dict(os.environ)
        env["GIT_TERMINAL_PROMPT"] = "0"
        if os.path.basename(argv[0]) == "xargs":
            env["GIT_LITERAL_PATHSPECS"] = "1"
        return env

    def _execute(self, argv: list[str], cwd: str | None, stdin: bytes | None) -> Result:
        try:
            proc = subprocess.run(
                argv,
                cwd=cwd,
                input=stdin,
                capture_output=True,
                env=self._env_for(argv),
                check=False,
            )
        except OSError as exc:
            return Result(127, "", f"{type(exc).__name__}: {exc}")
        return Result(
            proc.returncode,
            proc.stdout.decode("utf-8", "replace"),
            proc.stderr.decode("utf-8", "replace"),
        )


# --- command line ----------------------------------------------------------


def settings(env: Mapping[str, str]) -> dict[str, object]:
    raw = env.get("WORKTREE_CLEANUP_IDLE_DAYS", "")
    try:
        idle = int(raw) if raw else IDLE_DAYS_DEFAULT
    except ValueError:
        idle = IDLE_DAYS_DEFAULT
    return {
        "idle_days": max(idle, 0),
        "evidence_repo": env.get("RUN_EVIDENCE_REPO", EVIDENCE_REPO_DEFAULT),
        "evidence_dir": os.path.expanduser(
            env.get("RUN_EVIDENCE_DIR", EVIDENCE_DIR_DEFAULT)
        ),
    }


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="worktree_cleanup",
        description=(
            "Remove git worktrees of our own repos once their work is finished. "
            "A dry run unless --apply is given."
        ),
        epilog="Flags of every verb: --apply (really remove) and --out DIR (table files and locks).",
    )
    sub = parser.add_subparsers(
        dest="verb", required=True, metavar="{" + ",".join(VERBS) + "}"
    )
    sub.add_parser(
        "list", help="print the table of every worktree; never removes anything"
    )
    p_archive = sub.add_parser(
        "archive",
        help="save one worktree's .dev files to the evidence repo; never removes anything",
    )
    p_archive.add_argument("worktree", help="worktree path or unique folder name")
    p_retire = sub.add_parser(
        "retire", help="remove one worktree whose work is safe (needs --apply)"
    )
    p_retire.add_argument("worktree", help="worktree path or unique folder name")
    sub.add_parser(
        "prune",
        help="run the same decision for every worktree (removes only with --apply)",
    )
    for p in sub.choices.values():
        p.add_argument(
            "--apply",
            action="store_true",
            help="actually remove; without it nothing is removed",
        )
        p.add_argument(
            "--out",
            type=Path,
            default=None,
            help=f"folder for the table files and locks (default {DEFAULT_OUT}); never inside a worktree",
        )
    return parser.parse_args(argv)


def main(
    argv: list[str] | None = None,
    runner: Runner | None = None,
    env: Mapping[str, str] | None = None,
) -> int:
    args = parse_args(argv)
    env = os.environ if env is None else env
    cfg = settings(env)
    runner = runner or Runner(evidence_dir=str(cfg["evidence_dir"]))
    out = args.out or Path(os.path.expanduser(DEFAULT_OUT))
    _ = (runner, out)  # used by the verbs below
    print(f"worktree_cleanup {args.verb}: not built yet", file=sys.stderr)
    return EXIT_USAGE


if __name__ == "__main__":
    sys.exit(main())


===== new file: tests/worktree_cleanup/__init__.py =====


===== new file: tests/worktree_cleanup/conftest.py =====
"""Shared test support for scripts/worktree_cleanup.py.

Tests never touch a real worktree: git runs only on throwaway repositories under
``tmp_path``, and ``gh``, ``orca`` and the landed-check helper are answered from
canned replies by the recording runner below. The reply shapes are hand-written from
the spec and the tool help, not literal captures of live output.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "worktree_cleanup.py"


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
        def __init__(self, replies=None, real_git=True, evidence_dir=None):
            super().__init__(evidence_dir=evidence_dir)
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
                return super()._execute(argv, cwd, stdin)
            return wc.Result(127, "", f"no canned reply for {argv}")

    return RecordingRunner


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


===== new file: tests/worktree_cleanup/test_runner.py =====
"""Task 2: the allowlisted command runner, the command line and the file header.

Each refusal below must fail if its rule is removed from ``Runner.check_allowed``.
"""

from __future__ import annotations

import ast
import subprocess
import sys

import pytest

from .conftest import SCRIPT


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


def test_main_accepts_an_injected_runner_and_exits_usage_for_a_stub(wc, runner_cls):
    runner = runner_cls()
    assert wc.main(["list"], runner=runner, env={}) == wc.EXIT_USAGE
    assert runner.commands == []


def test_settings_defaults_and_idle_floor(wc):
    cfg = wc.settings({})
    assert cfg["idle_days"] == 7
    assert cfg["evidence_repo"] == "IronbellyOrg/run-evidence"
    assert wc.settings({"WORKTREE_CLEANUP_IDLE_DAYS": "3"})["idle_days"] == 3
    assert wc.settings({"WORKTREE_CLEANUP_IDLE_DAYS": "x"})["idle_days"] == 7


# --- refusals ----------------------------------------------------------------

BANNED = [
    (["git", "worktree", "remove", "--force", "/x"], None),
    (["git", "worktree", "remove", "-f", "/x"], None),
    (["git", "worktree", "remove", "-f", "-f", "/x"], None),
    (["orca", "worktree", "rm", "--worktree", "id:1", "--force"], None),
    (["git", "branch", "-D", "topic"], None),
    (["git", "branch", "--delete", "--force", "topic"], None),
    (["rm", "-rf", "/x"], None),
    (["rm", "file"], None),
    (["git", "worktree", "prune"], None),
    (["git", "clean", "-fdx"], None),
    (["git", "clean", "-f", "-x", "--", "a"], None),
]


@pytest.mark.parametrize("argv,cwd", BANNED)
def test_banned_shapes_are_refused_before_any_process_starts(
    wc, never_run_runner, argv, cwd
):
    with pytest.raises(wc.RefusedCommand):
        never_run_runner.run(argv, cwd=cwd)
    assert never_run_runner.commands == []


def test_banned_shapes_raise_the_dedicated_error(wc, never_run_runner):
    for argv, _ in BANNED:
        with pytest.raises(wc.RefusedCommand):
            never_run_runner.check_allowed(argv)


def test_push_rules(wc, runner_cls, tmp_path):
    evidence = tmp_path / "evidence"
    evidence.mkdir()
    other = tmp_path / "other"
    other.mkdir()
    r = runner_cls(evidence_dir=str(evidence))
    # allowed inside the evidence clone
    r.check_allowed(["git", "push", "origin", "main"], cwd=str(evidence))
    r.check_allowed(
        ["git", "-c", wc.CREDENTIAL_HELPER, "push", "origin", "main"], cwd=str(evidence)
    )
    # refused: delete flag, delete refspec, force, not the evidence clone, other -c
    for argv in (
        ["git", "push", "--delete", "origin", "topic"],
        ["git", "push", "origin", ":topic"],
        ["git", "push", "origin", "+main:main"],
        ["git", "push", "--force", "origin", "main"],
        ["git", "push", "-f", "origin", "main"],
    ):
        with pytest.raises(wc.RefusedCommand):
            r.check_allowed(argv, cwd=str(evidence))
    with pytest.raises(wc.RefusedCommand):
        r.check_allowed(["git", "push", "origin", "main"], cwd=str(other))
    with pytest.raises(wc.RefusedCommand):
        r.check_allowed(["git", "-c", "core.sshCommand=x", "push"], cwd=str(evidence))


UNLISTED = [
    ["git", "reset", "--hard"],
    ["git", "checkout", "topic"],
    ["git", "stash"],
    ["git", "merge", "topic"],
    ["mv", "a", "b"],
    ["find", ".", "-delete"],
    ["gh", "pr", "merge", "1", "--repo", "o/r"],
    ["gh", "pr", "create", "--repo", "o/r"],
    ["gh", "api", "repos/o/r"],
    ["orca", "automations", "create"],
    ["orca", "worktree", "create", "--name", "x"],
    ["python3", "-c", "print(1)"],
]


@pytest.mark.parametrize("argv", UNLISTED)
def test_unlisted_commands_are_refused(wc, never_run_runner, argv):
    with pytest.raises(wc.RefusedCommand):
        never_run_runner.check_allowed(argv)
    with pytest.raises(wc.RefusedCommand):
        never_run_runner.run(argv)
    assert never_run_runner.commands == []


def test_gh_calls_need_an_explicit_repo(wc, never_run_runner):
    with pytest.raises(wc.RefusedCommand):
        never_run_runner.check_allowed(["gh", "pr", "list", "--head", "x"])
    never_run_runner.check_allowed(["gh", "pr", "list", "--repo", "o/r", "--head", "x"])
    never_run_runner.check_allowed(["gh", "issue", "view", "5", "--repo", "o/r"])


def test_orca_terminal_close_needs_authorization(wc, never_run_runner):
    argv = ["orca", "terminal", "close", "--worktree", "id:7", "--all"]
    with pytest.raises(wc.RefusedCommand):
        never_run_runner.check_allowed(argv)
    never_run_runner.authorize_close("id:7")
    never_run_runner.check_allowed(argv)
    # another worktree is still refused
    with pytest.raises(wc.RefusedCommand):
        never_run_runner.check_allowed(
            ["orca", "terminal", "close", "--worktree", "id:8", "--all"]
        )


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
    with pytest.raises(wc.RefusedCommand):
        never_run_runner.check_allowed(
            ["xargs", "-0", "git", "clean", "-f", "-d", "-x", "--"],
            cwd=str(wt),
            stdin=ok,
        )


def test_read_and_named_write_shapes_are_allowed(wc, never_run_runner):
    ok = [
        ["git", "status", "--porcelain"],
        ["git", "worktree", "list", "--porcelain"],
        ["git", "worktree", "remove", "/some/path"],
        ["git", "branch", "-d", "topic"],
        ["git", "branch", "--list", "topic"],
        ["git", "remote", "get-url", "origin"],
        ["git", "rev-parse", "HEAD"],
        ["git", "merge-base", "--is-ancestor", "a", "b"],
        ["gh", "pr", "list", "--repo", "o/r", "--head", "b", "--state", "all"],
        ["orca", "repo", "list", "--json"],
        ["orca", "worktree", "ps", "--json"],
        ["orca", "worktree", "rm", "--worktree", "id:1"],
        ["tar", "-tzf", "/x/ignored.tar.gz"],
        [
            "bash",
            "/h/.claude/skills/sc-closeout-protocol/scripts/branch-landed.sh",
            "12",
        ],
    ]
    for argv in ok:
        never_run_runner.check_allowed(argv)
    with pytest.raises(wc.RefusedCommand):
        never_run_runner.check_allowed(["tar", "-xzf", "/x/a.tar.gz"])
    with pytest.raises(wc.RefusedCommand):
        never_run_runner.check_allowed(["bash", "/tmp/evil.sh", "12"])


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
        # no argv list that starts with the string "rm"
        if isinstance(node, ast.List) and node.elts:
            first = node.elts[0]
            if isinstance(first, ast.Constant) and first.value == "rm":
                raise AssertionError("an argument list starts with rm")


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


def test_no_dash_characters_in_the_script():
    text = _source()
    assert "–" not in text and "—" not in text


Codegraph context: index_state=fresh checked_at=2026-11-20T18:23:04Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-687 projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-687
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep and Read floor for dependents of changed symbols (this task creates new files or edits registration lists; see the diff).

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
