43b2163eaeb4ba44939bdd2e758aa5c4fbb327c3
Review one task for spec compliance.

Task brief: ## Task 13: Write the pipeline, terminal, safety and output tests

Depends on: Task 12, Task 8

Create `tests/worktree_cleanup/test_pipeline.py` and `tests/worktree_cleanup/test_safety.py`. Pipeline file: decision 3 (a worktree that passes every rule with Orca terminals open and a process inside is removed under `--apply` only after `orca terminal close --worktree id:<id> --all` is confirmed and the second check finds nothing changed and no process inside; in a dry run the table says "its Orca terminals will be closed first" and no terminal is closed); a terminal close that is `unverifiable` or fails keeps the worktree; a process still inside after the close keeps it; a change appearing between the save and the close (a new commit, a tracked edit, an untracked file outside `.dev/`) keeps it; decision 1 (exactly the paths of `saved-paths.txt` are cleared including a name with a space, and an unlisted untracked file, an unlisted ignored file and every tracked file survive, and a path not in the list is refused by the runner); decision 2 (a merged worktree with a tracked edit or a later commit is kept, nothing cleared, no terminal closed, nothing archived by `prune`); the removed worktree's branch is removed with `-d` and a squash-merge refusal reports "branch kept"; a second run finds nothing more to do; two runs at once do not both remove the same worktree; folders that are not git worktrees of our repos never appear in the table and are never touched. Safety file: a recorder test runs every verb on every branch through the recording runner and fails if any recorded command is `--force` on a removal, `git branch -D`, `rm`, `git worktree prune`, a push to anything but the evidence remote, a remote branch delete, a `git clean` that is not `-f -x --` followed only by lines of that worktree's `saved-paths.txt` issued after `VERIFIED`, or an `orca terminal close` for a worktree before every other rule passed and its save was verified; every `gh` call carries `--repo <owner>/<repo>`; dry run is the default and the recorded commands contain no removal; `--apply` removes only rows marked removable; no output (table, summary, log, JSON) names an agent or a model (a test greps for a fixed list of such words); no secret is printed or written and the script never opens `~/.config/gh/hosts.yml` or `~/.env` (patch `open` and `Path.read_text` to fail on those paths); `GH_TOKEN` is read from the environment only; each refusal shape of `Runner.check_allowed` from Task 2 raises.

Acceptance criteria:
- `uv run pytest tests/worktree_cleanup/test_pipeline.py tests/worktree_cleanup/test_safety.py -v` passes.
- Mutation check by hand: removing the `VERIFIED` precondition, or letting a path outside the list through, makes a safety test fail; removing the second check makes a pipeline test fail.
- The recorder test inspects the commands of every verb (`list`, `archive`, `retire`, `prune`, with and without `--apply`), not only `prune`.
- The tests together with Tasks 8 and 10 cover every case of source section 9 (about 35 cases in four groups).

AC ids (in source order): T13.AC1, T13.AC2, T13.AC3, T13.AC4
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
Start sha: 43b2163eaeb4ba44939bdd2e758aa5c4fbb327c3
Diff against the start snapshot: diff --git a/scripts/worktree_cleanup.py b/scripts/worktree_cleanup.py
deleted file mode 100644
index 68f51ddce..000000000
--- a/scripts/worktree_cleanup.py
+++ /dev/null
@@ -1,3119 +0,0 @@
-#!/usr/bin/env python3
-# Rules adapted from three files in https://github.com/Simple-With-Us/AI-Fleet-Coordinator
-# (scripts/fleet_lanes/retire.py, docs/protocols/lane-map.md, scripts/disk-janitor.sh),
-# Copyright 2026 Jay Wedgeworth, licensed under the Apache License, Version 2.0.
-# Changed by IronClaude: the rules, the runner, the archive step and every command are
-# rewritten for git worktrees of IronbellyOrg repos. See scripts/worktree_cleanup_PROVENANCE.md.
-"""Remove git worktrees of our own repos once their work is finished, and nothing else.
-
-A worktree is removed only when all eight rules hold: it is a linked worktree of one of
-our repos, its own pull request is merged, nothing was added after that pull request,
-every issue it relates to is closed, nothing unsaved is in it, nothing but its own Orca
-terminals is using it, it has been idle for the idle floor, and it is not pinned.
-Untracked and ignored files under ``.dev/`` are first saved to the evidence repo and
-checked against GitHub. Every step fails closed: if anything cannot be read or
-completed, the worktree is kept and the reason is shown.
-
-Verbs (a dry run unless --apply is given):
-  list                 table of every worktree of every repo of ours, never removes
-  archive <worktree>   only the save step, never removes
-  retire <worktree>    remove one worktree whose work is safe
-  prune                the same decision for every worktree
-
-Environment (names only; credentials come from the environment and nowhere else):
-  GH_TOKEN                     token for gh, for the landed check (it runs gh) and for the
-                               push to the evidence repo; no other command gets it
-  RUN_EVIDENCE_REPO            default IronbellyOrg/run-evidence
-  RUN_EVIDENCE_DIR             local clone, default ~/workspaces/run-evidence
-  WORKTREE_CLEANUP_IDLE_DAYS   idle floor in days, default 7
-
-Usage:
-  uv run --no-project python scripts/worktree_cleanup.py <verb> [--apply] [--out DIR]
-"""
-
-from __future__ import annotations
-
-import argparse
-import dataclasses
-import hashlib
-import json
-import os
-import re
-import shlex
-import shutil
-import subprocess
-import sys
-import tarfile
-import time
-from collections.abc import Callable, Iterator, Mapping, Sequence
-from dataclasses import dataclass, field
-from datetime import datetime, timezone
-from pathlib import Path, PurePosixPath
-from typing import Any
-
-# --- constants -------------------------------------------------------------
-
-IDLE_DAYS_DEFAULT = 7
-EVIDENCE_REPO_DEFAULT = "IronbellyOrg/run-evidence"
-EVIDENCE_DIR_DEFAULT = "~/workspaces/run-evidence"
-DEFAULT_OUT = "~/.local/state/worktree-cleanup"
-
-# GitHub refuses a file over 100 MB; ignored archives are split into parts of this size.
-# A module constant so a test can lower it.
-ARCHIVE_PART_BYTES = 85 * 1024 * 1024
-
-OWNERS = ("ironbellyorg", "ironbellygroup")
-
-# Second guard: infrastructure and port folders are never touched, even if git lists them.
-NAME_GUARD_PREFIXES = ("orca-port-", "orca-recipe-", "orca-pristine-")
-NAME_GUARD_EXACT = ("orca-old-patched",)
-
-# Ignored names that are build output or generated copies, not local state (rule 5).
-BUILD_OUTPUT_NAMES = frozenset(
-    {
-        "__pycache__",
-        ".venv",
-        ".codegraph",
-        ".ruff_cache",
-        ".pytest_cache",
-        ".mypy_cache",
-        "node_modules",
-        "dist",
-        "build",
-        "uv.lock",
-    }
-)
-BUILD_OUTPUT_PATHS = (
-    (".serena", "cache"),
-    (".claude", "agents"),
-    (".claude", "commands"),
-    (".claude", "hooks"),
-    (".claude", "skills"),
-    (".claude", "templates"),
-)
-
-EXIT_OK = 0
-EXIT_USAGE = 64
-EXIT_FAILED = 69
-
-VERBS = ("list", "archive", "retire", "prune")
-
-CREDENTIAL_HELPER = "credential.helper=!gh auth git-credential"
-
-# Environment names that carry a credential. Only gh, the landed check (it runs gh) and
-# the push to the evidence repo get them. The clone and the fetch of the evidence repo
-# get none and rely on the stored login of the person running the script, which this
-# script never reads.
-TOKEN_NAMES = ("GH_TOKEN", "GITHUB_TOKEN")
-
-LANDED_CHECK_RELATIVE = "skills/sc-closeout-protocol/scripts/branch-landed.sh"
-
-# A branch the evidence clone may push: no colon, plus sign or star in it.
-_BRANCH_RE = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9._/-]*$")
-_REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
-
-
-def default_landed_paths() -> tuple[str, ...]:
-    """The three places the landed check is looked for, in the order Task 1 recorded."""
-    checkout = Path(__file__).resolve().parents[1]
-    return (
-        os.path.expanduser("~/.claude/" + LANDED_CHECK_RELATIVE),
-        str(checkout / ".claude" / LANDED_CHECK_RELATIVE),
-        str(checkout / "src" / "superclaude" / LANDED_CHECK_RELATIVE),
-    )
-
-
-# --- the one runner --------------------------------------------------------
-
-
-class RefusedCommand(Exception):
-    """A command the allowlist does not name, or one of the always-banned shapes."""
-
-
-@dataclass
-class CommandRecord:
-    argv: list[str]
-    cwd: str | None
-    stdin_paths: int = 0
-
-
-@dataclass
-class Result:
-    returncode: int
-    stdout: str = ""
-    stderr: str = ""
-
-
-def _plain(token: str) -> str:
-    """A plain argument: never empty and never shaped like an option, a forced ref or a pathspec magic."""
-    if not token or token[0] in "-+:":
-        raise RefusedCommand(f"argument not accepted: {token!r}")
-    return token
-
-
-def _match(
-    tail: list[str],
-    flags: frozenset[str] = frozenset(),
-    values: frozenset[str] = frozenset(),
-    prefixes: tuple[str, ...] = (),
-    allow_dashdash: bool = False,
-) -> tuple[list[str], list[str]]:
-    """Check ``tail`` against one exact option shape; return (arguments, paths after --).
-
-    Every token that starts with ``-`` must be named in ``flags``, be one of the ``values``
-    options (which takes the next token as its value), or start with one of ``prefixes``.
-    There is no deny list: a bundled short option or a shortened long option is not named,
-    so it is refused.
-    """
-    args: list[str] = []
-    paths: list[str] = []
-    i = 0
-    while i < len(tail):
-        tok = tail[i]
-        if tok == "--":
-            if not allow_dashdash:
-                raise RefusedCommand("`--` is not accepted here")
-            paths = tail[i + 1 :]
-            if not paths or any(not p for p in paths):
-                raise RefusedCommand("`--` must be followed by paths")
-            break
-        if tok in flags:
-            pass
-        elif tok in values:
-            i += 1
-            if i >= len(tail) or not tail[i] or tail[i].startswith("-"):
-                raise RefusedCommand(f"{tok} needs a value")
-        elif any(tok.startswith(p) for p in prefixes):
-            pass
-        elif tok.startswith("-"):
-            raise RefusedCommand(f"option not on the allowlist: {tok}")
-        else:
-            args.append(_plain(tok))
-        i += 1
-    return args, paths
-
-
-def _count(args: list[str], low: int, high: int | None, what: str) -> None:
-    if len(args) < low or (high is not None and len(args) > high):
-        raise RefusedCommand(f"{what} takes a different number of arguments")
-
-
-# git read verbs: the exact options, the exact option prefixes, the least and most plain
-# arguments, and whether ``-- <paths>`` is accepted. Nothing outside this table is a read verb.
-_GitShape = tuple[frozenset[str], tuple[str, ...], int, int | None, bool]
-_GIT_READ_SHAPES: dict[str, _GitShape] = {
-    "status": (
-        frozenset({"--porcelain", "-z", "--ignored", "--untracked-files=all"}),
-        (),
-        0,
-        0,
-        False,
-    ),
-    "rev-parse": (
-        frozenset(
-            {
-                "--git-dir",
-                "--git-common-dir",
-                "--show-toplevel",
-                "--verify",
-                "--abbrev-ref",
-            }
-        ),
-        (),
-        0,
-        None,
-        False,
-    ),
-    "log": (frozenset({"-1"}), ("--format=",), 0, None, True),
-    "ls-files": (
-        frozenset({"-z", "--others", "--ignored", "--exclude-standard", "--cached"}),
-        (),
-        0,
-        0,
-        True,
-    ),
-    "ls-tree": (frozenset({"-r", "--name-only", "-z"}), (), 1, None, False),
-    "merge-base": (frozenset({"--is-ancestor"}), (), 2, 2, False),
-    "rev-list": (frozenset({"--count"}), (), 1, None, False),
-    "diff": (frozenset({"--quiet"}), (), 0, None, True),
-}
-
-_GH_VALUE_FLAGS = frozenset({"--repo", "--head", "--state", "--json", "--limit"})
-
-
-@dataclass
-class Runner:
-    """The only way this script starts an outside program.
-
-    ``check_allowed`` is a positive allowlist: a command is accepted only when it matches
-    one complete argument shape, and everything else is refused before any process
-    starts. Every command that passes is recorded (argument list and working folder), so
-    a test can read the whole list.
-    """
-
-    evidence_dir: str | None = None
-    commands: list[CommandRecord] = field(default_factory=list)
-    # The three places branch-landed.sh may be run from (compared by real path).
-    landed_paths: tuple[str, ...] = field(default_factory=default_landed_paths)
-    # Paths saved and verified in the evidence repo, per worktree folder (real path).
-    saved_paths: dict[str, set[str]] = field(default_factory=dict)
-    # Worktree selectors whose Orca terminals may be closed (every other rule passed
-    # and the save is verified).
-    close_authorized: set[str] = field(default_factory=set)
-
-    # -- authorization registered by the pipeline --------------------------------
-
-    def register_saved(self, worktree: str, paths: list[str]) -> None:
-        self.saved_paths.setdefault(os.path.realpath(worktree), set()).update(paths)
-
-    def authorize_close(self, selector: str) -> None:
-        self.close_authorized.add(selector)
-
-    # -- the allowlist ---------------------------------------------------------
-
-    def _in_evidence_dir(self, cwd: str | None) -> bool:
-        if not self.evidence_dir or cwd is None:
-            return False
-        return os.path.realpath(cwd) == os.path.realpath(self.evidence_dir)
-
-    def _is_landed_check(self, path: str) -> bool:
-        real = os.path.realpath(path)
-        return any(real == os.path.realpath(p) for p in self.landed_paths)
-
-    def check_allowed(
-        self,
-        argv: list[str],
-        cwd: str | None = None,
-        stdin: bytes | None = None,
-    ) -> None:
-        if not argv:
-            raise RefusedCommand("empty command")
-        prog = os.path.basename(argv[0])
-        if prog == "git":
-            self._check_git(argv[1:], cwd)
-        elif prog == "gh":
-            self._check_gh(argv[1:])
-        elif prog == "orca":
-            self._check_orca(argv[1:])
-        elif prog == "tar":
-            if not (
-                len(argv) == 3 and argv[1] == "-tzf" and argv[2] and argv[2][0] != "-"
-            ):
-                raise RefusedCommand("tar is allowed only as: tar -tzf <archive>")
-        elif prog == "xargs":
-            self._check_xargs(argv[1:], cwd, stdin)
-        elif prog == "bash" and len(argv) == 3 and self._is_landed_check(argv[1]):
-            self._check_landed_arg(argv[2])
-        elif prog != "bash" and len(argv) == 2 and self._is_landed_check(argv[0]):
-            self._check_landed_arg(argv[1])
-        else:
-            raise RefusedCommand(f"command not on the allowlist: {shlex.join(argv)}")
-
-    @staticmethod
-    def _check_landed_arg(arg: str) -> None:
-        if not (arg.isascii() and arg.isdigit()):
-            raise RefusedCommand("branch-landed.sh takes one pull request number")
-
-    # git ----------------------------------------------------------------------
-
-    def _check_git(self, args: list[str], cwd: str | None) -> None:
-        rest = list(args)
-        helper = False
-        while rest and rest[0] in ("-C", "-c"):
-            flag = rest.pop(0)
-            if not rest or not rest[0] or rest[0].startswith("-"):
-                raise RefusedCommand("git option without a value")
-            value = rest.pop(0)
-            if flag == "-c":
-                if value != CREDENTIAL_HELPER:
-                    raise RefusedCommand(
-                        f"git -c is allowed only for {CREDENTIAL_HELPER}"
-                    )
-                helper = True
-            else:
-                cwd = value
-        if not rest or rest[0].startswith("-"):
-            raise RefusedCommand("git needs a verb after -C and -c")
-        verb, tail = rest[0], rest[1:]
-        if helper and verb != "push":
-            raise RefusedCommand(
-                "the credential helper option is allowed only on the evidence push"
-            )
-        if verb in _GIT_READ_SHAPES:
-            flags, prefixes, low, high, dashdash = _GIT_READ_SHAPES[verb]
-            plain, _paths = _match(
-                tail, flags, prefixes=prefixes, allow_dashdash=dashdash
-            )
-            _count(plain, low, high, f"git {verb}")
-        elif verb == "remote":
-            if not (len(tail) == 2 and tail[0] == "get-url"):
-                raise RefusedCommand(
-                    "git remote is allowed only as: remote get-url <name>"
-                )
-            _plain(tail[1])
-        elif verb == "config":
-            if not (len(tail) == 2 and tail[0] == "--get"):
-                raise RefusedCommand(
-                    "git config is allowed only as: config --get <key>"
-                )
-            _plain(tail[1])
-        elif verb == "worktree":
-            self._check_git_worktree(tail)
-        elif verb == "branch":
-            self._check_git_branch(tail)
-        elif verb in ("clone", "fetch", "add", "commit", "rebase", "push"):
-            self._check_git_evidence(verb, tail, cwd)
-        else:
-            raise RefusedCommand(f"git {verb} is not on the allowlist")
-
-    @staticmethod
-    def _check_git_worktree(tail: list[str]) -> None:
-        if tail in (["list"], ["list", "--porcelain"]):
-            return
-        if len(tail) == 2 and tail[0] == "remove":
-            _plain(tail[1])
-            return
-        raise RefusedCommand(
-            "git worktree is allowed only as: list [--porcelain], remove <path> "
-            "(never --force, never prune)"
-        )
-
-    @staticmethod
-    def _check_git_branch(tail: list[str]) -> None:
-        if tail == ["--show-current"]:
-            return
-        if len(tail) == 2 and tail[0] in ("--list", "-d"):
-            _plain(tail[1])
-            return
-        raise RefusedCommand(
-            "git branch is allowed only as: --show-current, --list <name>, -d <name> "
-            "(never -D)"
-        )
-
-    def _check_git_evidence(self, verb: str, tail: list[str], cwd: str | None) -> None:
-        if verb == "clone":
-            if not (len(tail) == 2 and self.evidence_dir):
-                raise RefusedCommand(
-                    "git clone is allowed only as: clone <url> <evidence folder>"
-                )
-            _plain(tail[0])
-            if os.path.realpath(tail[1]) != os.path.realpath(self.evidence_dir):
-                raise RefusedCommand(
-                    "git clone is allowed only into the evidence folder"
-                )
-            return
-        if not self._in_evidence_dir(cwd):
-            raise RefusedCommand(f"git {verb} runs only inside the evidence clone")
-        if verb == "fetch":
-            if tail in (["origin"], ["--quiet", "origin"]):
-                return
-            raise RefusedCommand("git fetch is allowed only as: fetch [--quiet] origin")
-        if verb == "add":
-            if len(tail) < 2 or tail[0] != "--":
-                raise RefusedCommand("git add is allowed only as: add -- <paths>")
-            for p in tail[1:]:
-                if not p or p[0] == ":" or ".." in p.split("/"):
-                    raise RefusedCommand(f"git add path not accepted: {p!r}")
-            return
-        if verb == "commit":
-            if len(tail) >= 2 and tail[:-2] in ([], ["--quiet"]) and tail[-2] == "-m":
-                _plain(tail[-1])
-                return
-            raise RefusedCommand(
-                "git commit is allowed only as: commit [--quiet] -m <message>"
-            )
-        if verb == "rebase":
-            if tail in (["origin/main"], ["--abort"]):
-                return
-            raise RefusedCommand(
-                "git rebase is allowed only as: rebase origin/main, or rebase --abort"
-            )
-        # push
-        rest = tail[1:] if tail[:1] == ["--porcelain"] else tail
-        if len(rest) == 2 and rest[0] == "origin":
-            branch = rest[1]
-            if _BRANCH_RE.match(branch) and ".." not in branch:
-                return
-        raise RefusedCommand(
-            "git push is allowed only as: push [--porcelain] origin <branch>; it never "
-            "deletes, forces or rewrites a ref"
-        )
-
-    # gh -----------------------------------------------------------------------
-
-    @staticmethod
-    def _check_gh(args: list[str]) -> None:
-        if args[:2] == ["pr", "list"]:
-            want = 0
-        elif args[:2] in (["pr", "view"], ["issue", "view"]):
-            want = 1
-        else:
-            raise RefusedCommand(f"gh {' '.join(args[:2])} is not on the allowlist")
-        tail = args[2:]
-        plain, _ = _match(tail, values=_GH_VALUE_FLAGS)
-        _count(plain, want, want, "gh")
-        if want and not (plain[0].isascii() and plain[0].isdigit()):
-            raise RefusedCommand("gh view takes one number")
-        repos = [tail[i + 1] for i, t in enumerate(tail[:-1]) if t == "--repo"]
-        if len(repos) != 1 or not _REPO_RE.match(repos[0]):
-            raise RefusedCommand("gh needs exactly one --repo <owner>/<repo>")
-        if repos[0].split("/")[0].lower() not in OWNERS:
-            raise RefusedCommand("gh may only name a repo of our own owners")
-
-    # orca ---------------------------------------------------------------------
-
-    def _check_orca(self, args: list[str]) -> None:
-        head, tail = args[:2], args[2:]
-        if head in (["repo", "list"], ["worktree", "list"], ["worktree", "ps"]):
-            if tail in ([], ["--json"]):
-                return
-        elif head in (["reference", "list"], ["terminal", "list"]):
-            if (
-                len(tail) in (2, 3)
-                and tail[0] == "--worktree"
-                and _plain(tail[1])
-                and tail[2:] in ([], ["--json"])
-            ):
-                return
-        elif head == ["worktree", "rm"]:
-            if len(tail) == 2 and tail[0] == "--worktree" and _plain(tail[1]):
-                return
-            raise RefusedCommand(
-                "orca worktree rm is allowed only as: worktree rm --worktree <selector> "
-                "(never --force)"
-            )
-        elif head == ["terminal", "close"]:
-            if (
-                len(tail) == 3
-                and tail[0] == "--worktree"
-                and tail[2] == "--all"
-                and _plain(tail[1])
-            ):
-                if tail[1] in self.close_authorized:
-                    return
-                raise RefusedCommand(
-                    "orca terminal close before every other rule passed and the save was verified"
-                )
-            raise RefusedCommand(
-                "orca terminal close is allowed only as: terminal close --worktree <selector> --all"
-            )
-        raise RefusedCommand(f"orca {' '.join(args)} is not on the allowlist")
-
-    # xargs git clean ------------------------------------------------------------
-
-    def _check_xargs(
-        self, args: list[str], cwd: str | None, stdin: bytes | None
-    ) -> None:
-        if args != ["-0", "git", "clean", "-f", "-x", "--"]:
-            raise RefusedCommand(
-                "xargs is allowed only as: xargs -0 git clean -f -x --"
-            )
-        if cwd is None or stdin is None:
-            raise RefusedCommand("git clean needs a worktree folder and a path list")
-        allowed = self.saved_paths.get(os.path.realpath(cwd), set())
-        paths = [p for p in stdin.decode("utf-8", "surrogateescape").split("\0") if p]
-        if not paths:
-            raise RefusedCommand("git clean with no paths")
-        outside = [p for p in paths if p not in allowed]
-        if outside:
-            raise RefusedCommand(
-                f"git clean refused for a path not in the saved list: {outside[0]}"
-            )
-
-    # -- running ---------------------------------------------------------------
-
-    def run(
-        self,
-        argv: list[str],
-        cwd: str | None = None,
-        stdin: bytes | None = None,
-    ) -> Result:
-        self.check_allowed(argv, cwd, stdin)
-        n_paths = len([p for p in stdin.split(b"\0") if p]) if stdin else 0
-        self.commands.append(CommandRecord(list(argv), cwd, n_paths))
-        return self._execute(argv, cwd, stdin)
-
-    @staticmethod
-    def _git_verb(args: list[str]) -> str:
-        rest = list(args)
-        while rest and rest[0] in ("-C", "-c"):
-            del rest[:2]
-        return rest[0] if rest else ""
-
-    def _needs_token(self, argv: list[str]) -> bool:
-        """The token goes only to gh, the landed check (it runs gh) and the evidence push."""
-        prog = os.path.basename(argv[0])
-        if prog == "gh":
-            return True
-        if prog == "bash" and len(argv) > 1 and self._is_landed_check(argv[1]):
-            return True
-        if prog != "bash" and self._is_landed_check(argv[0]):
-            return True
-        return prog == "git" and self._git_verb(argv[1:]) == "push"
-
-    def _env_for(self, argv: list[str]) -> dict[str, str]:
-        env = dict(os.environ)
-        env["GIT_TERMINAL_PROMPT"] = "0"
-        # A read such as git status must not refresh the index of the worktree it reads.
-        env["GIT_OPTIONAL_LOCKS"] = "0"
-        env.pop("GIT_EXTERNAL_DIFF", None)
-        if os.path.basename(argv[0]) == "xargs":
-            env["GIT_LITERAL_PATHSPECS"] = "1"
-        if not self._needs_token(argv):
-            for name in TOKEN_NAMES:
-                env.pop(name, None)
-        return env
-
-    def _execute(self, argv: list[str], cwd: str | None, stdin: bytes | None) -> Result:
-        try:
-            proc = subprocess.run(
-                argv,
-                cwd=cwd,
-                input=stdin,
-                capture_output=True,
-                env=self._env_for(argv),
-                check=False,
-            )
-        except OSError as exc:
-            return Result(127, "", f"{type(exc).__name__}: {exc}")
-        return Result(
-            proc.returncode,
-            proc.stdout.decode("utf-8", "replace"),
-            proc.stderr.decode("utf-8", "replace"),
-        )
-
-
-# --- Orca facts (read only) --------------------------------------------------
-
-ORCA_UNAVAILABLE = "Orca unavailable"
-
-
-@dataclass(frozen=True)
-class OrcaRepo:
-    id: str
-    path: str
-    name: str
-
-
-@dataclass(frozen=True)
-class OrcaWorktree:
-    """One row of ``orca worktree ps --json``.
-
-    ``linked_pr_hint`` is Orca's own pull request record. It is only a hint: no rule reads
-    it as proof of a merge (only gh decides rule 2).
-    """
-
-    worktree_id: str
-    selector: str  # id:<worktree_id>, the form every Orca verb takes
-    path: str
-    branch: str
-    repo: str
-    last_activity_ms: float | None
-    is_pinned: bool
-    live_terminal_count: int
-    linked_pr_hint: Mapping[str, Any] | None
-    comment: str
-    # Orca's linkedIssue as (repo or None, number); only a source of issue numbers for rule 4
-    linked_issue: tuple[str | None, int] | None = None
-
-
-@dataclass(frozen=True)
-class OrcaReference:
-    raw: Mapping[str, Any]
-
-
-@dataclass(frozen=True)
-class OrcaTerminal:
-    handle: str
-    worktree_id: str
-    title: str
-
-
-@dataclass(frozen=True)
-class OrcaRead:
-    """The outcome of one Orca read: its rows, or the reason Orca gave no facts."""
-
-    ok: bool
-    items: tuple[Any, ...] = ()
-    reason: str = ""
-
-    @property
-    def unavailable(self) -> str | None:
-        return None if self.ok else f"{ORCA_UNAVAILABLE}: {self.reason}"
-
-
-def _unavailable(reason: str) -> OrcaRead:
-    return OrcaRead(False, (), reason)
-
-
-def _orca_rows(text: str, key: str) -> list[dict[str, Any]] | str:
-    """The list under ``result.<key>`` of an Orca reply, or the reason it is not usable."""
-    try:
-        doc = json.loads(text)
-    except (ValueError, TypeError):
-        return "the reply is not JSON"
-    if isinstance(doc, dict) and doc.get("ok") is False:
-        return "Orca reported an error"
-    body = doc.get("result") if isinstance(doc, dict) and "result" in doc else doc
-    rows = body.get(key) if isinstance(body, dict) else body
-    if not isinstance(rows, list) or not all(isinstance(r, dict) for r in rows):
-        return f"no {key} list in the reply"
-    return rows
-
-
-def _str(row: Mapping[str, Any], key: str) -> str | None:
-    value = row.get(key)
-    return value if isinstance(value, str) and value else None
-
-
-def _repo_from_url(url: str) -> str | None:
-    """owner/repo of a github.com issue or pull request URL."""
-    found = re.search(r"github\.com/([\w.-]+/[\w.-]+)/(?:issues|pull)/\d+", url)
-    return found.group(1) if found else None
-
-
-def _issue_from_orca(value: Any) -> tuple[str | None, int] | None:
-    """(repo or None, number) from Orca's linkedIssue; anything unreadable is None."""
-    if not isinstance(value, dict):
-        return None
-    number = value.get("number")
-    if isinstance(number, bool) or not isinstance(number, int) or number < 1:
-        return None
-    url = value.get("url")
-    return (_repo_from_url(url) if isinstance(url, str) else None), number
-
-
-def parse_orca_repos(text: str) -> OrcaRead:
-    rows = _orca_rows(text, "repos")
-    if isinstance(rows, str):
-        return _unavailable(rows)
-    repos = []
-    for row in rows:
-        rid, path = _str(row, "id"), _str(row, "path")
-        if rid is None or path is None:
-            return _unavailable("a repo row has no id or path")
-        name = _str(row, "displayName") or _str(row, "name") or os.path.basename(path)
-        repos.append(OrcaRepo(rid, path, name))
-    return OrcaRead(True, tuple(repos))
-
-
-def parse_orca_worktrees(text: str) -> OrcaRead:
-    rows = _orca_rows(text, "worktrees")
-    if isinstance(rows, str):
-        return _unavailable(rows)
-    worktrees = []
-    for row in rows:
-        wid, path = _str(row, "worktreeId"), _str(row, "path")
-        pinned, live = row.get("isPinned"), row.get("liveTerminalCount")
-        activity, pr = row.get("lastActivityAt"), row.get("linkedPR")
-        comment = row.get("comment")
-        if wid is None or path is None:
-            return _unavailable("a worktree row has no worktreeId or path")
-        if not isinstance(pinned, bool):
-            return _unavailable("a worktree row has no isPinned flag")
-        if isinstance(live, bool) or not isinstance(live, int) or live < 0:
-            return _unavailable("a worktree row has no liveTerminalCount")
-        if activity is not None and (
-            isinstance(activity, bool) or not isinstance(activity, (int, float))
-        ):
-            return _unavailable("a worktree row has a bad lastActivityAt")
-        if pr is not None and not isinstance(pr, dict):
-            return _unavailable("a worktree row has a bad linkedPR")
-        if comment is not None and not isinstance(comment, str):
-            return _unavailable("a worktree row has a bad comment")
-        worktrees.append(
-            OrcaWorktree(
-                worktree_id=wid,
-                selector=f"id:{wid}",
-                path=path,
-                branch=_str(row, "branch") or "",
-                repo=_str(row, "repo") or "",
-                last_activity_ms=activity,
-                is_pinned=pinned,
-                live_terminal_count=live,
-                linked_pr_hint=pr,
-                comment=comment or "",
-                linked_issue=_issue_from_orca(row.get("linkedIssue")),
-            )
-        )
-    return OrcaRead(True, tuple(worktrees))
-
-
-def parse_orca_references(text: str) -> OrcaRead:
-    rows = _orca_rows(text, "references")
-    if isinstance(rows, str):
-        return _unavailable(rows)
-    return OrcaRead(True, tuple(OrcaReference(dict(r)) for r in rows))
-
-
-def parse_orca_terminals(text: str) -> OrcaRead:
-    rows = _orca_rows(text, "terminals")
-    if isinstance(rows, str):
-        return _unavailable(rows)
-    terminals = []
-    for row in rows:
-        handle = _str(row, "handle")
-        if handle is None:
-            return _unavailable("a terminal row has no handle")
-        terminals.append(
-            OrcaTerminal(
-                handle=handle,
-                worktree_id=_str(row, "worktreeId") or "",
-                title=_str(row, "title") or "",
-            )
-        )
-    return OrcaRead(True, tuple(terminals))
-
-
-def _orca_read(runner: Runner, argv: list[str], parse: Any) -> OrcaRead:
-    """Run one read verb and parse it; a failed run or a bad reply is "Orca unavailable"."""
-    res = runner.run(argv)
-    if res.returncode != 0:
-        return _unavailable(f"the command exited with {res.returncode}")
-    return parse(res.stdout)
-
-
-def read_orca_repos(runner: Runner) -> OrcaRead:
-    return _orca_read(runner, ["orca", "repo", "list", "--json"], parse_orca_repos)
-
-
-def read_orca_worktrees(runner: Runner) -> OrcaRead:
-    return _orca_read(
-        runner, ["orca", "worktree", "ps", "--json"], parse_orca_worktrees
-    )
-
-
-def read_orca_references(runner: Runner, selector: str) -> OrcaRead:
-    argv = ["orca", "reference", "list", "--worktree", selector, "--json"]
-    return _orca_read(runner, argv, parse_orca_references)
-
-
-def read_orca_terminals(runner: Runner, selector: str) -> OrcaRead:
-    argv = ["orca", "terminal", "list", "--worktree", selector, "--json"]
-    return _orca_read(runner, argv, parse_orca_terminals)
-
-
-def repos_or_current(
-    read: OrcaRead, current_repo: OrcaRepo
-) -> tuple[list[OrcaRepo], str]:
-    """The repos to scan: Orca's list, or the current checkout's repo alone when Orca gave none.
-
-    The second value is the note the table prints when the fallback was used.
-    """
-    if read.ok:
-        return list(read.items), ""
-    return [
-        current_repo
-    ], f"{read.unavailable}; scanning the current checkout's repo only"
-
-
-# --- local facts: git, files and processes (read only) -----------------------
-
-KEEP_FILE = ".worktree-keep"
-
-# Files and folders in a worktree's own git folder that show an operation in progress.
-GIT_OPERATION_MARKERS = (
-    "MERGE_HEAD",
-    "CHERRY_PICK_HEAD",
-    "REVERT_HEAD",
-    "BISECT_LOG",
-    "rebase-merge",
-    "rebase-apply",
-    "index.lock",
-)
-
-
-@dataclass(frozen=True)
-class GitWorktree:
-    """One entry of ``git worktree list --porcelain``."""
-
-    path: str
-    repo_path: str  # the repo folder git was asked from
-    head: str
-    branch: str | None  # short branch name, None when detached
-    detached: bool
-    bare: bool
-    locked: bool
-    prunable: bool
-    is_main: bool  # the first porcelain entry is the main checkout
-
-
-def parse_worktree_porcelain(text: str, repo_path: str) -> list[GitWorktree]:
-    entries: list[GitWorktree] = []
-    blocks = [b for b in text.split("\n\n") if b.strip()]
-    for index, block in enumerate(blocks):
-        path = head = ""
-        branch: str | None = None
-        flags = {"detached": False, "bare": False, "locked": False, "prunable": False}
-        for line in block.splitlines():
-            key, _, value = line.partition(" ")
-            if key == "worktree":
-                path = value
-            elif key == "HEAD":
-                head = value
-            elif key == "branch":
-                branch = value.removeprefix("refs/heads/")
-            elif key in flags:
-                flags[key] = True
-        if path:
-            entries.append(
-                GitWorktree(
-                    path=path,
-                    repo_path=repo_path,
-                    head=head,
-                    branch=branch,
-                    is_main=index == 0,
-                    **flags,
-                )
-            )
-    return entries
-
-
-@dataclass(frozen=True)
-class Discovery:
-    worktrees: tuple[GitWorktree, ...]
-    failures: tuple[str, ...]
-
-
-def discover_worktrees(runner: Runner, repos: Sequence[OrcaRepo]) -> Discovery:
-    """Every worktree of every repo, found with git so worktrees Orca does not list are covered."""
-    found: dict[str, GitWorktree] = {}
-    failures: list[str] = []
-    for repo in repos:
-        res = runner.run(["git", "worktree", "list", "--porcelain"], cwd=repo.path)
-        if res.returncode != 0:
-            failures.append(f"git worktree list failed in {repo.path}")
-            continue
-        for entry in parse_worktree_porcelain(res.stdout, repo.path):
-            found.setdefault(os.path.realpath(entry.path), entry)
-    return Discovery(tuple(found.values()), tuple(failures))
-
-
-def name_guard(path: str) -> bool:
-    """Second guard: infrastructure and port folders, matched at the start of the folder name."""
-    name = os.path.basename(path.rstrip("/"))
-    return name.startswith(NAME_GUARD_PREFIXES) or name in NAME_GUARD_EXACT
-
-
-@dataclass(frozen=True)
-class OriginInfo:
-    owner: str
-    repo: str
-
-    @property
-    def is_ours(self) -> bool:
-        return self.owner.lower() in OWNERS
-
-
-def parse_origin(url: str) -> OriginInfo | None:
-    """Owner and repo of a GitHub remote URL (https, ssh or scp style); None otherwise."""
-    text = url.strip()
-    if "github.com" not in text.lower():
-        return None
-    parts = [
-        p for p in re.split(r"[/:]", text.removesuffix("/").removesuffix(".git")) if p
-    ]
-    if len(parts) < 2:
-        return None
-    return OriginInfo(owner=parts[-2], repo=parts[-1])
-
-
-@dataclass
-class LocalState:
-    """``git status --porcelain --ignored`` split into the groups rules 5 needs."""
-
-    changed_tracked: list[str] = field(default_factory=list)
-    untracked_outside_dev: list[str] = field(default_factory=list)
-    untracked_dev: list[str] = field(default_factory=list)
-    ignored_build: list[str] = field(default_factory=list)
-    ignored_generated: list[str] = field(default_factory=list)
-    ignored_dev: list[str] = field(default_factory=list)
-    ignored_unknown: list[str] = field(default_factory=list)
-
-
-def _is_generated_copy(parts: tuple[str, ...]) -> bool:
-    pairs = set(zip(parts, parts[1:]))
-    return any(pair in pairs for pair in BUILD_OUTPUT_PATHS)
-
-
-def classify_status(raw: str) -> LocalState:
-    """Split the output of ``git status --porcelain -z --ignored --untracked-files=all``."""
-    state = LocalState()
-    items = raw.split("\0")
-    i = 0
-    while i < len(items):
-        item = items[i]
-        i += 1
-        if len(item) < 4 or item[2] != " ":
-            continue
-        xy, path = item[:2], item[3:]
-        if "R" in xy or "C" in xy:
-            i += 1  # the next field is the original path of a rename or copy
-        parts = PurePosixPath(path).parts
-        under_dev = bool(parts) and parts[0] == ".dev"
-        if xy == "??":
-            (state.untracked_dev if under_dev else state.untracked_outside_dev).append(
-                path
-            )
-        elif xy == "!!":
-            if under_dev:
-                state.ignored_dev.append(path)
-            elif any(p in BUILD_OUTPUT_NAMES for p in parts):
-                state.ignored_build.append(path)
-            elif _is_generated_copy(parts):
-                state.ignored_generated.append(path)
-            else:
-                state.ignored_unknown.append(path)
-        else:
-            state.changed_tracked.append(path)
-    return state
-
-
-@dataclass
-class WorktreeFacts:
-    """Everything read about one worktree. A missing value is None; the reason is in failures."""
-
-    worktree: GitWorktree
-    present: bool = True
-    head: str | None = None
-    origin: OriginInfo | None = None
-    git_dir: str | None = None
-    state: LocalState | None = None
-    last_commit_ts: float | None = None
-    git_file_mtime: float | None = None  # newest of HEAD, index and logs/HEAD
-    created_ts: float | None = None
-    orca_activity_ts: float | None = None
-    keep_file: bool = False
-    operations: list[str] = field(default_factory=list)
-    nested_checkouts: list[str] = field(default_factory=list)
-    size_bytes: int | None = None
-    failures: list[str] = field(default_factory=list)
-
-    def newest_activity(self) -> float | None:
-        known = [
-            t
-            for t in (self.git_file_mtime, self.last_commit_ts, self.orca_activity_ts)
-            if t is not None
-        ]
-        return max(known) if known else None
-
-    def idle_days(self, now: float) -> float | None:
-        newest = self.newest_activity()
-        return None if newest is None else max(now - newest, 0.0) / 86400
-
-    def age_days(self, now: float) -> float | None:
-        return (
-            None if self.created_ts is None else max(now - self.created_ts, 0.0) / 86400
-        )
-
-
-def _mtime(path: str) -> float | None:
-    try:
-        return os.stat(path).st_mtime
-    except OSError:
-        return None
-
-
-def walk_worktree(top: str) -> tuple[int, list[str], list[str]]:
-    """Walk the folder read-only: (size in bytes, nested checkouts, read errors)."""
-    size = 0
-    nested: list[str] = []
-    errors: list[str] = []
-
-    def on_error(exc: OSError) -> None:
-        errors.append(f"{exc.filename}: {exc.strerror}")
-
-    for dirpath, dirnames, filenames in os.walk(
-        top, followlinks=False, onerror=on_error
-    ):
-        at_top = dirpath == top
-        if ".git" in dirnames:
-            dirnames[:] = [d for d in dirnames if d != ".git"]  # never descend into one
-            if not at_top:
-                nested.append(os.path.relpath(os.path.join(dirpath, ".git"), top))
-        if ".git" in filenames and not at_top:
-            nested.append(os.path.relpath(os.path.join(dirpath, ".git"), top))
-        for fname in filenames:
-            try:
-                size += os.lstat(os.path.join(dirpath, fname)).st_size
-            except OSError as exc:
-                errors.append(f"{exc.filename}: {exc.strerror}")
-    return size, nested, errors
-
-
-def gather_facts(
-    runner: Runner,
-    wt: GitWorktree,
-    orca: OrcaWorktree | None = None,
-) -> WorktreeFacts:
-    """Read the facts of one worktree. Every failed read is a note, never an exception."""
-    facts = WorktreeFacts(worktree=wt)
-    if orca is not None and orca.last_activity_ms is not None:
-        facts.orca_activity_ts = orca.last_activity_ms / 1000
-    if not os.path.isdir(wt.path):
-        facts.present = False
-        return facts
-
-    def read(argv: list[str], what: str) -> str | None:
-        res = runner.run(argv, cwd=wt.path)
-        if res.returncode != 0:
-            facts.failures.append(f"{what} failed")
-            return None
-        return res.stdout
-
-    out = read(["git", "rev-parse", "HEAD"], "git rev-parse HEAD")
-    facts.head = out.strip() if out is not None else None
-    out = read(["git", "rev-parse", "--git-dir"], "git rev-parse --git-dir")
-    if out is not None:
-        facts.git_dir = os.path.normpath(os.path.join(wt.path, out.strip()))
-    out = read(["git", "remote", "get-url", "origin"], "git remote get-url origin")
-    facts.origin = parse_origin(out) if out is not None else None
-    out = read(
-        ["git", "status", "--porcelain", "-z", "--ignored", "--untracked-files=all"],
-        "git status",
-    )
-    facts.state = classify_status(out) if out is not None else None
-    out = read(["git", "log", "-1", "--format=%ct"], "git log")
-    if out is not None and out.strip().isdigit():
-        facts.last_commit_ts = float(out.strip())
-    elif out is not None:
-        facts.failures.append("git log gave no commit time")
-    if facts.git_dir is not None:
-        times = [
-            _mtime(os.path.join(facts.git_dir, name))
-            for name in ("HEAD", "index", os.path.join("logs", "HEAD"))
-        ]
-        known = [t for t in times if t is not None]
-        facts.git_file_mtime = max(known) if known else None
-        facts.created_ts = _mtime(os.path.join(facts.git_dir, "gitdir")) or _mtime(
-            os.path.join(wt.path, ".git")
-        )
-        facts.operations = [
-            m
-            for m in GIT_OPERATION_MARKERS
-            if os.path.exists(os.path.join(facts.git_dir, m))
-        ]
-    facts.keep_file = os.path.exists(os.path.join(wt.path, KEEP_FILE))
-    size, nested, errors = walk_worktree(wt.path)
-    facts.size_bytes, facts.nested_checkouts = size, nested
-    if errors:
-        facts.failures.append(f"{len(errors)} folder entries could not be read")
-    return facts
-
-
-def is_own_folder(worktree_path: str, own_paths: Sequence[str] | None = None) -> bool:
-    """True when the worktree holds this script or its working folder (compared by real path)."""
-    own = (
-        own_paths if own_paths is not None else (os.getcwd(), os.path.abspath(__file__))
-    )
-    top = os.path.realpath(worktree_path)
-    return any(
-        os.path.realpath(p) == top or os.path.realpath(p).startswith(top + os.sep)
-        for p in own
-    )
-
-
-@dataclass(frozen=True)
-class ProcScan:
-    ok: bool
-    cwds: tuple[
-        tuple[int, str, str], ...
-    ] = ()  # (pid, real working folder, command name)
-    notes: tuple[str, ...] = ()
-    failure: str = ""
-
-
-def scan_processes(
-    proc_root: str = "/proc",
-    my_uid: int | None = None,
-    readlink: Callable[[str], str] = os.readlink,
-    uid_of: Callable[[str], int] | None = None,
-) -> ProcScan:
-    """Read ``<proc_root>/<pid>/cwd`` for every process.
-
-    An entry that exited meanwhile is ignored, another user's entry is noted and ignored,
-    and any other error means the scan failed (which keeps every worktree).
-    """
-    my_uid = os.getuid() if my_uid is None else my_uid
-    uid_of = uid_of or (lambda p: os.stat(p).st_uid)
-    try:
-        names = os.listdir(proc_root)
-    except OSError as exc:
-        return ProcScan(False, failure=f"cannot list {proc_root}: {exc.strerror}")
-    cwds: list[tuple[int, str, str]] = []
-    notes: list[str] = []
-    for name in sorted(n for n in names if n.isdigit()):
-        pid, entry = int(name), os.path.join(proc_root, name)
-        try:
-            target = readlink(os.path.join(entry, "cwd"))
-        except (FileNotFoundError, ProcessLookupError):
-            continue  # exited meanwhile
-        except PermissionError:
-            try:
-                owner = uid_of(entry)
-            except FileNotFoundError:
-                continue
-            except OSError as exc:
-                return ProcScan(False, failure=f"pid {pid}: {exc.strerror}")
-            if owner != my_uid:
-                notes.append(f"pid {pid}: another user's process, ignored")
-                continue
-            return ProcScan(
-                False, failure=f"pid {pid}: permission denied for its own user"
-            )
-        except OSError as exc:
-            return ProcScan(False, failure=f"pid {pid}: {exc.strerror}")
-        try:
-            with open(os.path.join(entry, "comm"), encoding="utf-8") as handle:
-                command = handle.read().strip()
-        except OSError:
-            command = "?"
-        cwds.append((pid, os.path.realpath(target), command or "?"))
-    return ProcScan(True, tuple(cwds), tuple(notes))
-
-
-def processes_inside(scan: ProcScan, worktree_path: str) -> list[tuple[int, str]]:
-    """(pid, command) of every process whose working folder is inside the worktree."""
-    top = os.path.realpath(worktree_path)
-    return [
-        (pid, command)
-        for pid, cwd, command in scan.cwds
-        if cwd == top or cwd.startswith(top + os.sep)
-    ]
-
-
-# --- GitHub facts: own pull request, landed check, issues ---------------------
-
-PR_JSON_FIELDS = "number,state,headRefOid,author,mergedAt,title,body,closingIssuesReferences,headRefName"
-LANDED_TOKENS = ("MERGED", "OPEN", "CLOSED", "NONE", "UNKNOWN")
-# The labels of the three lookup places of the landed check, in the order of Task 1.
-LANDED_LABELS = ("installed copy", "checkout copy", "in-checkout fallback")
-
-
-def _gh(runner: Runner, argv: list[str]) -> Result:
-    """Run gh through the runner; a refused shape is a failed call, not a crash."""
-    try:
-        return runner.run(["gh", *argv])
-    except RefusedCommand as exc:
-        return Result(126, "", f"refused: {exc}")
-
-
-def _first_line(text: str) -> str:
-    lines = text.strip().splitlines()
-    return lines[0][:160] if lines else ""
-
-
-def _not_found(res: Result) -> bool:
-    """gh says the number does not exist (as opposed to a failed or unreachable lookup)."""
-    text = res.stderr.lower()
-    return res.returncode != 0 and any(
-        w in text
-        for w in ("could not resolve", "not found", "no issue", "no pull request")
-    )
-
-
-@dataclass(frozen=True)
-class IssueRef:
-    repo: str | None  # owner/repo, None when the text did not say
-    number: int
-
-
-@dataclass(frozen=True)
-class PullRequest:
-    number: int
-    state: str  # MERGED, OPEN or CLOSED
-    head_oid: str
-    author: str
-    merged_at: str | None
-    title: str
-    body: str
-    closing: tuple[IssueRef, ...]
-    branch: str
-
-
-@dataclass(frozen=True)
-class PrLookup:
-    ok: bool
-    pr: PullRequest | None = None
-    reason: str = ""
-
-
-def _repo_of_closing_ref(row: Mapping[str, Any]) -> str | None:
-    repo = row.get("repository")
-    if not isinstance(repo, dict):
-        return None
-    full = repo.get("nameWithOwner")
-    if isinstance(full, str) and "/" in full:
-        return full
-    owner, name = repo.get("owner"), repo.get("name")
-    login = owner.get("login") if isinstance(owner, dict) else owner
-    if isinstance(login, str) and isinstance(name, str):
-        return f"{login}/{name}"
-    return None
-
-
-def parse_pull_requests(text: str) -> list[PullRequest] | None:
-    """Rows of ``gh pr list --json ...``; None when the reply cannot be read."""
-    try:
-        rows = json.loads(text)
-    except (ValueError, TypeError):
-        return None
-    if not isinstance(rows, list):
-        return None
-    found: list[PullRequest] = []
-    for row in rows:
-        if not isinstance(row, dict):
-            return None
-        number, state = row.get("number"), row.get("state")
-        if isinstance(number, bool) or not isinstance(number, int):
-            return None
-        if not isinstance(state, str):
-            return None
-        author = row.get("author")
-        login = author.get("login") if isinstance(author, dict) else None
-        closing = tuple(
-            IssueRef(_repo_of_closing_ref(c), c["number"])
-            for c in (row.get("closingIssuesReferences") or [])
-            if isinstance(c, dict) and isinstance(c.get("number"), int)
-        )
-        found.append(
-            PullRequest(
-                number=number,
-                state=state.upper(),
-                head_oid=str(row.get("headRefOid") or ""),
-                author=login if isinstance(login, str) else "",
-                merged_at=row.get("mergedAt") or None,
-                title=str(row.get("title") or ""),
-                body=str(row.get("body") or ""),
-                closing=closing,
-                branch=str(row.get("headRefName") or ""),
-            )
-        )
-    return found
-
-
-def find_pull_request(runner: Runner, repo_slug: str, branch: str | None) -> PrLookup:
-    """The worktree's own pull request: the newest merged one, else the newest of any state."""
-    if not branch:
-        return PrLookup(True, None, "detached HEAD, so no branch to look up")
-    res = _gh(
-        runner,
-        [
-            "pr", "list", "--repo", repo_slug, "--head", branch, "--state", "all",
-            "--limit", "30", "--json", PR_JSON_FIELDS,
-        ],
-    )  # fmt: skip
-    if res.returncode != 0:
-        return PrLookup(False, None, f"gh pr list failed: {_first_line(res.stderr)}")
-    rows = parse_pull_requests(res.stdout)
-    if rows is None:
-        return PrLookup(False, None, "gh pr list gave an unreadable reply")
-    if not rows:
-        return PrLookup(True, None, "no pull request for the branch")
-    merged = [r for r in rows if r.state == "MERGED"]
-    if merged:
-        return PrLookup(True, max(merged, key=lambda r: (r.merged_at or "", r.number)))
-    return PrLookup(True, max(rows, key=lambda r: r.number))
-
-
-@dataclass(frozen=True)
-class Landed:
-    token: str  # one of LANDED_TOKENS; only MERGED lets rule 2 pass
-    via: str  # which lookup place answered
-    reason: str = ""
-
-
-def landed_check(
-    runner: Runner,
-    repo_slug: str,
-    pr_number: int,
-    main_checkout: str,
-    which: Callable[[str], str | None] = shutil.which,
-) -> Landed:
-    """MERGED, OPEN, CLOSED, NONE or UNKNOWN for one pull request number.
-
-    branch-landed.sh is looked for in the three places of Task 1 (it reads ``origin`` of
-    the folder it runs in, so it runs in the repo's main checkout, and needs jq). When it
-    is in none of them, ``gh pr view`` gives the same MERGED-or-not answer.
-    """
-    for path, label in zip(runner.landed_paths, LANDED_LABELS):
-        if not os.path.isfile(path):
-            continue
-        if which("jq") is None:
-            return Landed("UNKNOWN", label, "jq is not installed")
-        try:
-            res = runner.run(["bash", path, str(pr_number)], cwd=main_checkout)
-        except RefusedCommand as exc:
-            return Landed("UNKNOWN", label, f"refused: {exc}")
-        tokens = [
-            ln.strip() for ln in res.stdout.splitlines() if ln.strip() in LANDED_TOKENS
-        ]
-        if tokens:
-            return Landed(tokens[-1], label)
-        return Landed(
-            "UNKNOWN", label, f"the landed check gave no answer (exit {res.returncode})"
-        )
-    res = _gh(
-        runner,
-        ["pr", "view", str(pr_number), "--repo", repo_slug, "--json", "state,mergedAt"],
-    )
-    why = "landed check said UNKNOWN"
-    if res.returncode != 0:
-        return Landed("UNKNOWN", "gh pr view", f"{why}: gh pr view failed")
-    try:
-        doc = json.loads(res.stdout)
-    except (ValueError, TypeError):
-        doc = None
-    state = doc.get("state") if isinstance(doc, dict) else None
-    if state == "MERGED" and doc.get("mergedAt"):
-        return Landed("MERGED", "gh pr view")
-    if state in ("OPEN", "CLOSED"):
-        return Landed(state, "gh pr view")
-    return Landed("UNKNOWN", "gh pr view", f"{why}: unreadable reply")
-
-
-@dataclass(frozen=True)
-class AfterPr:
-    relation: str  # same, ancestor, ahead or unknown
-    commits_after: int | None
-    reason: str = ""
-
-
-def commits_after_pr(
-    runner: Runner, worktree_path: str, head: str | None, pr_head_oid: str
-) -> AfterPr:
-    """Rule 3 data: is HEAD the pull request's last commit (or an ancestor), and how far ahead."""
-    if not head or not pr_head_oid:
-        return AfterPr(
-            "unknown", None, "HEAD or the pull request's last commit is not known"
-        )
-    if head == pr_head_oid:
-        return AfterPr("same", 0)
-    res = runner.run(
-        ["git", "merge-base", "--is-ancestor", head, pr_head_oid], cwd=worktree_path
-    )
-    if res.returncode == 0:
-        return AfterPr("ancestor", 0)
-    if res.returncode != 1:
-        return AfterPr(
-            "unknown", None, "the pull request's last commit is not in this clone"
-        )
-    count = runner.run(
-        ["git", "rev-list", "--count", f"{pr_head_oid}..{head}"], cwd=worktree_path
-    )
-    if count.returncode == 0 and count.stdout.strip().isdigit():
-        return AfterPr("ahead", int(count.stdout.strip()))
-    return AfterPr("ahead", None, "could not count the commits after the pull request")
-
-
-@dataclass(frozen=True)
-class Issue:
-    repo: str
-    number: int
-    state: str  # OPEN or CLOSED
-    sources: tuple[str, ...]
-
-
-@dataclass(frozen=True)
-class IssueFacts:
-    issues: tuple[Issue, ...]
-    failures: tuple[str, ...]
-
-    @property
-    def open_issues(self) -> list[Issue]:
-        return [i for i in self.issues if i.state != "CLOSED"]
-
-    @property
-    def none_found(self) -> bool:
-        return not self.issues and not self.failures
-
-
-_REF_RE = re.compile(r"(?<![\w/.-])(?:([\w.-]+/[\w.-]+))?#(\d+)\b")
-_NAME_NUMBER_RE = re.compile(r"(?<!\d)(\d{2,4})(?!\d)")
-
-
-def refs_in_text(text: str) -> list[IssueRef]:
-    """Every ``#N`` and ``owner/repo#N`` in a text."""
-    return [IssueRef(m.group(1), int(m.group(2))) for m in _REF_RE.finditer(text or "")]
-
-
-def numbers_in_name(name: str) -> list[int]:
-    """Numbers of 2 to 4 digits in a branch or folder name."""
-    return [int(n) for n in _NAME_NUMBER_RE.findall(name or "")]
-
-
-def _lookup_issue(runner: Runner, repo: str, number: int) -> tuple[str | None, str]:
-    """(state, outcome): outcome is found, missing or failed."""
-    res = _gh(runner, ["issue", "view", str(number), "--repo", repo, "--json", "state"])
-    if res.returncode != 0:
-        return None, "missing" if _not_found(res) else "failed"
-    try:
-        state = json.loads(res.stdout).get("state")
-    except (ValueError, TypeError, AttributeError):
-        return None, "failed"
-    return (state.upper(), "found") if isinstance(state, str) else (None, "failed")
-
-
-def _is_pull_request(runner: Runner, repo: str, number: int) -> bool | None:
-    res = _gh(runner, ["pr", "view", str(number), "--repo", repo, "--json", "state"])
-    if res.returncode == 0:
-        return True
-    return False if _not_found(res) else None
-
-
-def collect_issues(
-    runner: Runner,
-    repo_slug: str,
-    pr: PullRequest | None,
-    branch: str | None,
-    folder: str,
-    orca: OrcaWorktree | None = None,
-    references: OrcaRead | None = None,
-) -> IssueFacts:
-    """Issues behind a worktree, from every place of rule 4; any failed lookup is recorded."""
-    # (reference, source, is it known to be an issue already)
-    wanted: list[tuple[IssueRef, str, bool]] = []
-    if pr is not None:
-        wanted += [(ref, "closing reference", True) for ref in pr.closing]
-        wanted += [
-            (r, "title or body", False) for r in refs_in_text(f"{pr.title}\n{pr.body}")
-        ]
-    for number in numbers_in_name(branch or ""):
-        wanted.append((IssueRef(None, number), "branch name", False))
-    for number in numbers_in_name(os.path.basename(folder.rstrip("/"))):
-        wanted.append((IssueRef(None, number), "folder name", False))
-    if orca is not None:
-        wanted += [(r, "Orca card comment", False) for r in refs_in_text(orca.comment)]
-        if orca.linked_issue is not None:
-            repo, number = orca.linked_issue
-            wanted.append((IssueRef(repo, number), "Orca linked issue", True))
-    unread: list[str] = []
-    if references is not None and not references.ok:
-        # a source that could not be read keeps the worktree, like a failed lookup
-        unread.append(f"issue lookup failed: {references.unavailable}")
-    if references is not None and references.ok:
-        for item in references.items:
-            raw = item.raw
-            kind, number, url = raw.get("kind"), raw.get("number"), raw.get("url")
-            if (
-                isinstance(kind, str)
-                and "issue" in kind.lower()
-                and isinstance(number, int)
-                and not isinstance(number, bool)
-            ):
-                repo = _repo_from_url(url) if isinstance(url, str) else None
-                wanted.append((IssueRef(repo, number), "Orca reference", True))
-
-    sources: dict[tuple[str, int], list[str]] = {}
-    known: dict[tuple[str, int], bool] = {}
-    names: dict[tuple[str, int], str] = {}  # the spelling of the repo seen first
-    for ref, source, is_issue in wanted:
-        repo = ref.repo or repo_slug
-        key = (repo.lower(), ref.number)
-        names.setdefault(key, repo)
-        sources.setdefault(key, [])
-        if source not in sources[key]:
-            sources[key].append(source)
-        known[key] = known.get(key, False) or is_issue
-
-    issues: list[Issue] = []
-    failures: list[str] = list(unread)
-    for key, where in sources.items():
-        repo, number = names[key], key[1]
-        label = f"{repo}#{number}"
-        if not known[key]:
-            is_pr = _is_pull_request(runner, repo, number)
-            if is_pr is None:
-                failures.append(f"issue lookup failed: {label}")
-                continue
-            if is_pr:
-                continue  # a pull request number is not an issue
-        state, outcome = _lookup_issue(runner, repo, number)
-        if outcome == "found" and state is not None:
-            issues.append(Issue(repo, number, state, tuple(where)))
-        elif outcome == "missing" and not known[key]:
-            continue  # a number in a name or text that is no issue of that repo
-        else:
-            failures.append(f"issue lookup failed: {label}")
-    return IssueFacts(tuple(issues), tuple(failures))
-
-
-# --- the eight rules and the table ----------------------------------------------
-
-SAVE_NOT_NEEDED = "not needed"
-SAVE_NEEDED = "needed"
-SAVE_VERIFIED = "verified"
-SAVE_FAILED_PREFIX = "failed: "
-TERMINALS_NOTE = "its Orca terminals will be closed first"
-
-TABLE_COLUMNS = (
-    "repo",
-    "folder",
-    "branch",
-    "in_orca",
-    "pull_request",
-    "issues",
-    "idle_days",
-    "size",
-    "saved_copy",
-    "decision",
-    "reason",
-)
-
-
-@dataclass
-class RuleInputs:
-    """Every fact the eight rules read. Built by hand in tests; no process is started to decide."""
-
-    facts: WorktreeFacts
-    now: float
-    idle_floor_days: int = IDLE_DAYS_DEFAULT
-    orca: OrcaWorktree | None = None
-    pr_lookup: PrLookup | None = None
-    landed: Landed | None = None
-    after: AfterPr | None = None
-    issues: IssueFacts | None = None
-    procs: ProcScan | None = None
-    save_state: str = SAVE_NOT_NEEDED
-    own_folder: bool = False
-    # False when the Orca worktree list could not be read: pinned and terminal facts are unknown
-    orca_known: bool = True
-
-
-# Reasons that come from a fact that could not be read (a lookup failure, exit 69).
-UNREAD_PREFIXES = (
-    "pull request lookup failed",
-    "landed check said UNKNOWN",
-    "issue lookup failed",
-    "ignored local state: git status could not be read",
-    "in use: the process scan failed",
-    "in use: the folder or its git folder could not be read",
-    "idle time unknown",
-    "created time unknown",
-    "Orca unavailable",
-)
-
-
-@dataclass(frozen=True)
-class Decision:
-    decision: str  # removable or kept
-    rule: int | None  # the first rule that failed, 1 to 8
-    reason: str
-    note: str = ""
-    saved_copy: str = "none needed"
-    unread: bool = False  # the reason is a fact that could not be read, not a verdict
-
-
-def _plural(n: int, word: str) -> str:
-    return f"{n} {word}" if n == 1 else f"{n} {word}s"
-
-
-def _has_dev_files(state: LocalState | None) -> bool:
-    return bool(state and (state.untracked_dev or state.ignored_dev))
-
-
-def saved_copy_cell(state: LocalState | None, save_state: str) -> str:
-    if not _has_dev_files(state):
-        return "none needed"
-    if save_state == SAVE_VERIFIED:
-        return "saved and checked"
-    if save_state.startswith(SAVE_FAILED_PREFIX):
-        return "failed"
-    return "needed"
-
-
-def _rule1(i: RuleInputs) -> str | None:
-    wt, f = i.facts.worktree, i.facts
-    if wt.is_main:
-        return "main checkout"
-    if not f.present:
-        # checked before the origin: a missing folder leaves origin unread
-        return "folder missing (reported only)"
-    if f.origin is None or not f.origin.is_ours:
-        return "not our repo"
-    if i.own_folder:
-        return "this is where the script runs"
-    if wt.locked:
-        return "locked"
-    if name_guard(wt.path):
-        return "on the name guard (infrastructure folder)"
-    if wt.detached or not wt.branch:
-        return "detached HEAD"
-    return None
-
-
-def _rule2(i: RuleInputs) -> str | None:
-    lookup = i.pr_lookup
-    if lookup is None or not lookup.ok:
-        why = lookup.reason if lookup else "not looked up"
-        return f"pull request lookup failed: {why}"
-    pr = lookup.pr
-    if pr is None:
-        return "no pull request"
-    if pr.state == "OPEN":
-        return f"pull request #{pr.number} is open"
-    if pr.state != "MERGED":
-        return f"pull request #{pr.number} closed, not merged"
-    token = i.landed.token if i.landed else "UNKNOWN"
-    if token == "MERGED":
-        return None
-    if token == "OPEN":
-        return f"pull request #{pr.number} is open"
-    if token == "CLOSED":
-        return f"pull request #{pr.number} closed, not merged"
-    if token == "NONE":
-        return "no pull request"
-    return "landed check said UNKNOWN"
-
-
-def _rule3(i: RuleInputs) -> str | None:
-    after = i.after
-    if after is None or after.relation == "unknown":
-        return "HEAD is not the pull request's head"
-    if after.relation == "ahead":
-        if after.commits_after is None:
-            return "HEAD is not the pull request's head"
-        return f"{_plural(after.commits_after, 'commit')} after the pull request"
-    return None
-
-
-def _rule4(i: RuleInputs) -> str | None:
-    found = i.issues
-    if found is None:
-        return "issue lookup failed"
-    if found.failures:
-        return (
-            found.failures[0]
-            if found.failures[0].startswith("issue lookup failed")
-            else "issue lookup failed"
-        )
-    opened = found.open_issues
-    if opened:
-        return f"issue #{opened[0].number} is open" + (
-            f" (and {len(opened) - 1} more)" if len(opened) > 1 else ""
-        )
-    return None
-
-
-def _rule5(i: RuleInputs) -> str | None:
-    s = i.facts.state
-    if s is None:
-        return "ignored local state: git status could not be read"
-    if s.changed_tracked:
-        return f"{_plural(len(s.changed_tracked), 'changed tracked file')}"
-    if s.untracked_outside_dev:
-        return f"{_plural(len(s.untracked_outside_dev), 'untracked file')} outside .dev"
-    if s.ignored_unknown:
-        shown = ", ".join(s.ignored_unknown[:3])
-        more = (
-            f" and {len(s.ignored_unknown) - 3} more"
-            if len(s.ignored_unknown) > 3
-            else ""
-        )
-        return f"ignored local state: {shown}{more}"
-    if _has_dev_files(s):
-        if i.save_state.startswith(SAVE_FAILED_PREFIX):
-            return f"saved copy failed: {i.save_state[len(SAVE_FAILED_PREFIX) :]}"
-        if i.save_state not in (SAVE_NEEDED, SAVE_VERIFIED):
-            return "saved copy failed: no save state for the .dev files"
-    return None
-
-
-def _rule6(i: RuleInputs) -> tuple[str | None, str]:
-    """(reason, note). A process inside is tolerated only while Orca terminals are open."""
-    f = i.facts
-    scan = i.procs
-    if scan is None or not scan.ok:
-        why = scan.failure if scan else "no scan"
-        return f"in use: the process scan failed ({why}), so everything is kept", ""
-    inside = processes_inside(scan, f.worktree.path)
-    terminals = i.orca is not None and i.orca.live_terminal_count > 0
-    if inside and not terminals:
-        pid, name = inside[0]
-        return f"in use: process {pid} ({name})", ""
-    if f.nested_checkouts:
-        return "holds another checkout", ""
-    if f.operations:
-        return "git operation in progress", ""
-    if f.git_dir is None or any("could not be read" in x for x in f.failures):
-        return "in use: the folder or its git folder could not be read in full", ""
-    return None, (TERMINALS_NOTE if terminals else "")
-
-
-def _rule7(i: RuleInputs) -> str | None:
-    idle, age = i.facts.idle_days(i.now), i.facts.age_days(i.now)
-    floor = i.idle_floor_days
-    if idle is None:
-        return f"idle time unknown (needs {floor})"
-    if idle < floor:
-        return f"idle {int(idle)} days (needs {floor})"
-    if age is None:
-        return f"created time unknown (needs {floor})"
-    if age < floor:
-        return f"created {int(age)} days ago (needs {floor})"
-    return None
-
-
-def _rule8(i: RuleInputs) -> str | None:
-    if not i.orca_known:
-        return "Orca unavailable, so whether it is pinned is unknown"
-    if i.orca is not None and i.orca.is_pinned:
-        return "pinned in Orca"
-    if i.facts.keep_file:
-        return "keep file present"
-    return None
-
-
-def decide(i: RuleInputs) -> Decision:
-    """The eight rules in order; the first that fails is the reason. Pure: starts no process."""
-    cell = saved_copy_cell(i.facts.state, i.save_state)
-    note = ""
-    for number, rule in enumerate(
-        (_rule1, _rule2, _rule3, _rule4, _rule5, _rule6, _rule7, _rule8), 1
-    ):
-        if number == 6:
-            reason, note = _rule6(i)
-        else:
-            reason = rule(i)
-        if reason is not None:
-            after_unknown = number == 3 and (
-                i.after is None
-                or i.after.relation == "unknown"
-                or i.after.commits_after is None
-            )
-            unread = reason.startswith(UNREAD_PREFIXES) or after_unknown
-            return Decision("kept", number, reason, "", cell, unread)
-    return Decision("removable", None, "", note, cell)
-
-
-def _size_text(size: int | None) -> str:
-    if size is None:
-        return "?"
-    value = float(size)
-    for unit in ("B", "KB", "MB", "GB"):
-        if value < 1024 or unit == "GB":
-            return f"{value:.0f} {unit}" if unit == "B" else f"{value:.1f} {unit}"
-        value /= 1024
-    return f"{size} B"
-
-
-def table_row(i: RuleInputs, d: Decision, repo_name: str = "") -> dict[str, str]:
-    f = i.facts
-    pr = i.pr_lookup.pr if i.pr_lookup and i.pr_lookup.ok else None
-    skipped = d.rule == 1 and i.pr_lookup is None  # rule 1 stops before any lookup
-    if skipped:
-        pr_cell = "n/a"
-    elif i.pr_lookup is None or not i.pr_lookup.ok:
-        pr_cell = "lookup failed"
-    else:
-        pr_cell = f"#{pr.number} {pr.state}" if pr else "none"
-    if i.issues is None:
-        issue_cell = "n/a" if skipped else "lookup failed"
-    else:
-        parts = [f"#{x.number} {x.state}" for x in i.issues.issues]
-        parts += ["lookup failed"] * len(i.issues.failures)
-        issue_cell = ", ".join(parts) if parts else "none found"
-    idle = f.idle_days(i.now)
-    reason = d.reason or d.note
-    return {
-        "repo": repo_name or os.path.basename(f.worktree.repo_path.rstrip("/")),
-        "folder": os.path.basename(f.worktree.path.rstrip("/")),
-        "branch": f.worktree.branch or "(detached)",
-        "in_orca": "yes" if i.orca is not None else "no",
-        "pull_request": pr_cell,
-        "issues": issue_cell,
-        "idle_days": "?" if idle is None else f"{idle:.1f}",
-        "size": _size_text(f.size_bytes),
-        "saved_copy": d.saved_copy,
-        "decision": d.decision,
-        "reason": reason,
-    }
-
-
-def render_json(
-    rows: Sequence[Mapping[str, str]],
-    commands: Sequence[Mapping[str, Any]] | None = None,
-    summary: Mapping[str, Any] | None = None,
-) -> str:
-    doc: dict[str, Any] = {
-        "columns": list(TABLE_COLUMNS),
-        "rows": [dict(r) for r in rows],
-    }
-    if commands is not None:
-        doc["commands"] = [dict(c) for c in commands]
-    if summary is not None:
-        doc["summary"] = dict(summary)
-    return json.dumps(doc, indent=2)
-
-
-def render_markdown(rows: Sequence[Mapping[str, str]]) -> str:
-    def cell(value: str) -> str:
-        return str(value).replace("|", "/").replace("\n", " ")
-
-    head = "| " + " | ".join(c.replace("_", " ") for c in TABLE_COLUMNS) + " |"
-    rule = "|" + "|".join("---" for _ in TABLE_COLUMNS) + "|"
-    body = ["| " + " | ".join(cell(r[c]) for c in TABLE_COLUMNS) + " |" for r in rows]
-    return "\n".join([head, rule, *body]) + "\n"
-
-
-# --- the .dev archive step (save before removing) ---------------------------------
-
-EVIDENCE_BRANCH = "main"
-PUSH_ATTEMPTS = 3
-ARCHIVE_NAME = "ignored.tar.gz"
-SAVED_PATHS_NAME = "saved-paths.txt"
-MANIFEST_NAME = "MANIFEST.md"
-
-# Names that look like secrets; matched on the saved path, never on the content.
-SECRET_NAME_RE = re.compile(
-    r"(^|/)(\.env(\..*)?|\.netrc|id_(rsa|dsa|ecdsa|ed25519)|credentials(\.json)?"
-    r"|secrets?(\.(json|ya?ml|env|txt))?|.*\.(pem|key|p12|pfx|keystore))$",
-    re.IGNORECASE,
-)
-# Token-shaped content. Only the file name is ever reported, never the matched text.
-SECRET_CONTENT_RES = tuple(
-    re.compile(p)
-    for p in (
-        rb"(?<![A-Za-z0-9_-])gh[pousr]_[A-Za-z0-9]{20,}",
-        rb"(?<![A-Za-z0-9_-])github_pat_[A-Za-z0-9_]{20,}",
-        rb"(?<![A-Za-z0-9_-])sk-(?:ant-)?[A-Za-z0-9_-]{20,}",
-        rb"(?<![A-Za-z0-9_-])AKIA[0-9A-Z]{16}",
-        rb"xox[abprs]-[A-Za-z0-9-]{10,}",
-        rb"AIza[0-9A-Za-z_-]{35}",
-        rb"-----BEGIN [A-Z ]*PRIVATE KEY-----",
-        rb"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
-    )
-)
-_AUTH_FAILURE_WORDS = (
-    "could not read username",
-    "authentication failed",
-    "terminal prompts disabled",
-    "invalid username or password",
-    "no credentials",
-)
-
-
-@dataclass(frozen=True)
-class ArchiveResult:
-    ok: bool
-    reason: str = ""  # begins "saved copy failed" when ok is false
-    folder: str = (
-        ""  # relative to the evidence clone; empty when there was nothing to save
-    )
-    files: int = 0
-    saved_paths: frozenset[str] = (
-        frozenset()
-    )  # worktree-relative; what Task 11 registers
-    verified: str = ""  # the VERIFIED line
-    # SHA-256 of each saved path as it was when saved; the removal re-checks them
-    digests: Mapping[str, str] = field(default_factory=dict)
-    scratch: str = ""  # a partial folder left behind by a failed save, named in the log
-
-
-def _fail(why: str, scratch: str = "") -> ArchiveResult:
-    return ArchiveResult(False, f"saved copy failed: {why}", scratch=scratch)
-
-
-def _sha256(path: str) -> str:
-    digest = hashlib.sha256()
-    with open(path, "rb") as handle:
-        for block in iter(lambda: handle.read(1 << 20), b""):
-            digest.update(block)
-    return digest.hexdigest()
-
-
-def file_has_secret(path: str) -> bool:
-    """True when the file holds token-shaped content. The match itself is never kept."""
-    keep = 256  # longest token shape that can straddle two blocks
-    tail = b""
-    with open(path, "rb") as handle:
-        for block in iter(lambda: handle.read(1 << 20), b""):
-            data = tail + block
-            if any(rx.search(data) for rx in SECRET_CONTENT_RES):
-                return True
-            tail = data[-keep:]
-    return False
-
-
-def first_secret(worktree: str, rels: Sequence[str]) -> str | None:
-    """The first saved path whose name or content looks like a secret, else None."""
-    for rel in rels:
-        if SECRET_NAME_RE.search(rel) or file_has_secret(os.path.join(worktree, rel)):
-            return rel
-    return None
-
-
-def check_save_paths(worktree: str, rels: Sequence[str]) -> str | None:
-    """Why a path cannot be saved safely (None when all can): only plain regular files."""
-    top = os.path.realpath(worktree)
-    for rel in rels:
-        parts = PurePosixPath(rel).parts
-        if (
-            not rel
-            or "\n" in rel
-            or "\0" in rel
-            or rel.startswith("/")
-            or ".." in parts
-        ):
-            return f"unusable file name {rel!r}"
-        full = os.path.join(worktree, rel)
-        if os.path.islink(full) or not os.path.isfile(full):
-            return f"{rel} is not a regular file"
-        if not os.path.realpath(full).startswith(top + os.sep):
-            return f"{rel} is outside the worktree"
-    return None
-
-
-class _PartWriter:
-    """A write-only stream that rolls over to a new part file every ``limit`` bytes."""
-
-    def __init__(self, folder: str, limit: int) -> None:
-        self.folder, self.limit = folder, limit
-        self.parts: list[str] = []
-        self._handle: Any = None
-        self._room = 0
-
-    def write(self, data: bytes) -> int:
-        view = memoryview(data)
-        while len(view):
-            if self._handle is None or self._room == 0:
-                if self._handle is not None:
-                    self._handle.close()
-                path = os.path.join(
-                    self.folder, f"{ARCHIVE_NAME}.part-{len(self.parts) + 1:03d}"
-                )
-                self.parts.append(path)
-                self._handle, self._room = open(path, "xb"), self.limit
-            chunk = view[: self._room]
-            self._handle.write(chunk)
-            self._room -= len(chunk)
-            view = view[len(chunk) :]
-        return len(data)
-
-    def flush(self) -> None:
-        if self._handle is not None:
-            self._handle.flush()
-
-    def close(self) -> None:
-        if self._handle is not None:
-            self._handle.close()
-            self._handle = None
-
-
-class _ChainReader:
-    """Reads several part files back as one byte stream."""
-
-    def __init__(self, parts: Sequence[str]) -> None:
-        self._parts, self._handle = list(parts), None
-
-    def read(self, size: int = -1) -> bytes:
-        out = b""
-        while size < 0 or len(out) < size:
-            if self._handle is None:
-                if not self._parts:
-                    break
-                self._handle = open(self._parts.pop(0), "rb")
-            block = self._handle.read(-1 if size < 0 else size - len(out))
-            if not block:
-                self._handle.close()
-                self._handle = None
-                continue
-            out += block
-        return out
-
-
-def archive_parts(folder: str) -> list[str]:
-    """The archive files of a saved folder, in joining order (one file, or numbered parts)."""
-    single = os.path.join(folder, ARCHIVE_NAME)
-    if os.path.isfile(single):
-        return [single]
-    return sorted(
-        os.path.join(folder, n)
-        for n in os.listdir(folder)
-        if n.startswith(f"{ARCHIVE_NAME}.part-")
-    )
-
-
-def archive_members(parts: Sequence[str]) -> Iterator[tuple[str, str]]:
-    """(path, sha256) of every regular file inside the archive, read back from its bytes."""
-    with tarfile.open(fileobj=_ChainReader(parts), mode="r|gz") as tar:
-        for member in tar:
-            if not member.isfile():
-                continue
-            digest, source = hashlib.sha256(), tar.extractfile(member)
-            for block in iter(lambda: source.read(1 << 20), b""):
-                digest.update(block)
-            yield member.name, digest.hexdigest()
-
-
-def _write_archive(folder: str, worktree: str, rels: Sequence[str]) -> list[str]:
-    writer = _PartWriter(folder, ARCHIVE_PART_BYTES)
-    try:
-        with tarfile.open(fileobj=writer, mode="w|gz") as tar:
-            for rel in rels:
-                tar.add(os.path.join(worktree, rel), arcname=rel, recursive=False)
-    finally:
-        writer.close()
-    if len(writer.parts) == 1:
-        os.rename(writer.parts[0], os.path.join(folder, ARCHIVE_NAME))
-        return [os.path.join(folder, ARCHIVE_NAME)]
-    return writer.parts
-
-
-def _clean_name(text: str) -> str:
-    return re.sub(r"[^A-Za-z0-9._-]+", "-", text).strip(".-")
-
-
-def folder_name(pr: PullRequest, repo_slug: str) -> tuple[str, str] | None:
-    """(relative folder, subject) by the folder convention; None when a part is missing."""
-    author, merged = _clean_name(pr.author), (pr.merged_at or "")[:10]
-    if not author or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", merged):
-        return None
-    branch = pr.branch
-    first, _, rest = branch.partition("/")
-    if rest and first.lower() == pr.author.lower():
-        branch = rest
-    subject = _clean_name(branch.replace("/", "-"))
-    if not subject:
-        return None
-    repo = _clean_name(repo_slug.split("/")[-1])
-    return f"{repo}/{author}/{merged}_pr{pr.number}_{subject}", subject
-
-
-def evidence_url(evidence_repo: str) -> str:
-    """The clone address: a path or full address is used as given, owner/name means GitHub."""
-    if os.path.isabs(evidence_repo) or "://" in evidence_repo:
-        return evidence_repo
-    return f"https://github.com/{evidence_repo}.git"
-
-
-def sync_evidence_clone(
-    runner: Runner, evidence_dir: str, evidence_repo: str
-) -> str | None:
-    """Clone when missing, then fetch and fast-forward. Returns a failure reason or None."""
-    if not os.path.isdir(os.path.join(evidence_dir, ".git")):
-        if os.path.exists(evidence_dir) and os.listdir(evidence_dir):
-            return "the evidence folder exists and is not a clone"
-        parent = os.path.dirname(os.path.abspath(evidence_dir))
-        os.makedirs(parent, exist_ok=True)
-        res = runner.run(
-            ["git", "clone", evidence_url(evidence_repo), evidence_dir], cwd=parent
-        )
-        if res.returncode != 0:
-            return "the evidence repo could not be cloned"
-    if (
-        runner.run(["git", "fetch", "--quiet", "origin"], cwd=evidence_dir).returncode
-        != 0
-    ):
-        return "the evidence repo could not be fetched"
-    if runner.run(["git", "rebase", "origin/main"], cwd=evidence_dir).returncode != 0:
-        runner.run(["git", "rebase", "--abort"], cwd=evidence_dir)
-        return "the evidence clone could not be brought up to date"
-    return None
-
-
-def _folder_digests(clone: str, folder: str) -> dict[str, set[str]]:
-    """path -> digests of what a saved folder holds (copied files and archive members)."""
-    base, found = os.path.join(clone, folder), {}
-    top = os.path.join(base, "files")
-    for dirpath, _dirs, names in os.walk(top):
-        for name in names:
-            full = os.path.join(dirpath, name)
-            found.setdefault(
-                os.path.relpath(full, top).replace(os.sep, "/"), set()
-            ).add(_sha256(full))
-    parts = archive_parts(base)
-    if parts:
-        for name, digest in archive_members(parts):
-            found.setdefault(name, set()).add(digest)
-    return found
-
-
-def _count_files(folder: str) -> int:
-    return sum(len(names) for _d, _s, names in os.walk(folder))
-
-
-def _verify_folder(runner: Runner, clone: str, folder: str) -> str | None:
-    """Fetch, then the folder on origin/main must match the local one. None means verified."""
-    if runner.run(["git", "fetch", "--quiet", "origin"], cwd=clone).returncode != 0:
-        return "the evidence repo could not be fetched to check the copy"
-    listed = runner.run(
-        [
-            "git",
-            "ls-tree",
-            "-r",
-            "--name-only",
-            "-z",
-            f"origin/{EVIDENCE_BRANCH}",
-            folder,
-        ],
-        cwd=clone,
-    )
-    remote = [n for n in listed.stdout.split("\0") if n]
-    if listed.returncode != 0 or len(remote) != _count_files(
-        os.path.join(clone, folder)
-    ):
-        return "the copy on origin/main has a different file count"
-    same = runner.run(
-        ["git", "diff", "--quiet", f"origin/{EVIDENCE_BRANCH}", "--", folder], cwd=clone
-    )
-    if same.returncode != 0:
-        return "the copy differs from origin/main"
-    return None
-
-
-def _push(runner: Runner, clone: str) -> str | None:
-    """fetch, rebase when origin moved, push; up to three tries. None means pushed."""
-    for _ in range(PUSH_ATTEMPTS):
-        if runner.run(["git", "fetch", "--quiet", "origin"], cwd=clone).returncode != 0:
-            return "the evidence repo could not be fetched"
-        if runner.run(["git", "rebase", "origin/main"], cwd=clone).returncode != 0:
-            runner.run(["git", "rebase", "--abort"], cwd=clone)
-            return "the evidence clone could not be rebased"
-        res = runner.run(
-            ["git", "-c", CREDENTIAL_HELPER, "push", "origin", EVIDENCE_BRANCH],
-            cwd=clone,
-        )
-        if res.returncode == 0:
-            return None
-        if any(w in res.stderr.lower() for w in _AUTH_FAILURE_WORDS):
-            return "no credentials in the environment"
-    return "push refused"
-
-
-def _manifest(
-    facts: WorktreeFacts, pr: PullRequest, repo_slug: str, saved_at: str, count: int,
-    sums: Mapping[str, str],
-) -> str:  # fmt: skip
-    def one_line(text: str) -> str:
-        return " ".join(text.split()).replace("|", "/")
-
-    rows = "\n".join(f"| {name} | {sums[name]} |" for name in sorted(sums))
-    return (
-        f"# Saved copy of {os.path.basename(facts.worktree.path)}\n\n"
-        f"- source repo: {repo_slug}\n"
-        f"- branch: {facts.worktree.branch}\n"
-        f"- pull request: [#{pr.number} {one_line(pr.title)}](https://github.com/{repo_slug}/pull/{pr.number})\n"
-        f"- merge date: {(pr.merged_at or '')[:10]}\n"
-        f"- worktree head: {facts.head}\n"
-        f"- pull request head: {pr.head_oid}\n"
-        f"- worktree folder: {facts.worktree.path}\n"
-        f"- saved at (UTC): {saved_at}\n"
-        f"- files saved: {count}\n\n"
-        f"## Checksums (SHA-256)\n\n| file | sha256 |\n|---|---|\n{rows}\n"
-    )
-
-
-def archive_worktree(
-    runner: Runner,
-    facts: WorktreeFacts,
-    pr: PullRequest | None,
-    evidence_dir: str,
-    evidence_repo: str,
-    now: datetime | None = None,
-    log: Callable[[str], None] | None = None,
-) -> ArchiveResult:
-    """Save the untracked and ignored ``.dev`` files of a merged worktree and verify the copy.
-
-    Reads and copies only: nothing inside the worktree is changed. Every failure reason
-    begins "saved copy failed" and a failed save deletes nothing (its scratch folder stays
-    and is named in the log).
-    """
-    say = log or (lambda _m: None)
-    if pr is None or pr.state != "MERGED":
-        return _fail("no merged pull request")
-    if facts.state is None or facts.origin is None or not facts.present:
-        return _fail("the worktree facts could not be read")
-    worktree, repo_slug = (
-        facts.worktree.path,
-        f"{facts.origin.owner}/{facts.origin.repo}",
-    )
-    untracked = sorted(set(facts.state.untracked_dev))
-    ignored = sorted(
-        p
-        for p in set(facts.state.ignored_dev)
-        if "__pycache__" not in PurePosixPath(p).parts
-    )
-    if not untracked and not ignored:
-        return ArchiveResult(True, verified="nothing to save")
-    problem = check_save_paths(worktree, untracked + ignored)
-    if problem:
-        return _fail(problem)
-    try:
-        secret = first_secret(worktree, untracked + ignored)
-        digests_now = {
-            p: _sha256(os.path.join(worktree, p)) for p in untracked + ignored
-        }
-    except (OSError, ValueError) as exc:
-        return _fail(f"a file could not be read ({type(exc).__name__})")
-    if secret:
-        return _fail(f"possible secret in {secret}")
-    naming = folder_name(pr, repo_slug)
-    if naming is None:
-        return _fail(
-            "the pull request has no author, merge date or branch name to file it under"
-        )
-    base, subject = naming
-    problem = sync_evidence_clone(runner, evidence_dir, evidence_repo)
-    if problem:
-        return _fail(problem)
-
-    # what earlier saves of this pull request already hold, byte for byte
-    candidates = [base, f"{base}-r2", f"{base}-r3"]
-    existing = [c for c in candidates if os.path.isdir(os.path.join(evidence_dir, c))]
-    held: dict[str, set[str]] = {}
-    try:
-        for folder in existing:
-            for path, digests in _folder_digests(evidence_dir, folder).items():
-                held.setdefault(path, set()).update(digests)
-    except (OSError, tarfile.TarError, EOFError) as exc:
-        return _fail(
-            f"an earlier saved folder could not be read ({type(exc).__name__})"
-        )
-    # an earlier folder counts as covering a file only after it is verified on origin/main
-    for folder in existing:
-        why = _verify_folder(runner, evidence_dir, folder)
-        if why:
-            return _fail(why)
-    todo_untracked = [p for p in untracked if digests_now[p] not in held.get(p, set())]
-    todo_ignored = [p for p in ignored if digests_now[p] not in held.get(p, set())]
-    every = frozenset(untracked + ignored)
-    if existing and not todo_untracked and not todo_ignored:
-        n = _count_files(os.path.join(evidence_dir, existing[-1]))
-        return ArchiveResult(
-            True,
-            "",
-            existing[-1],
-            n,
-            every,
-            f"VERIFIED {existing[-1]} files={n}",
-            digests_now,
-        )
-    free = [c for c in candidates if c not in existing]
-    if not free:
-        return _fail("this pull request already has three saved folders")
-    folder = free[0]
-    final = os.path.join(evidence_dir, folder)
-    partial = os.path.join(
-        os.path.dirname(final), f".{os.path.basename(final)}.partial-{os.getpid()}"
-    )
-    say(f"saving into {partial}")
-    saved_at = (now or datetime.now(timezone.utc)).strftime("%Y-%m-%dT%H:%M:%SZ")
-    try:
-        os.makedirs(partial)
-        for rel in todo_untracked:
-            target = os.path.join(partial, "files", rel)
-            os.makedirs(os.path.dirname(target), exist_ok=True)
-            shutil.copy2(os.path.join(worktree, rel), target)
-        parts = _write_archive(partial, worktree, todo_ignored)
-        in_archive = sorted(name for name, _digest in archive_members(parts))
-        if in_archive != sorted(todo_ignored):
-            return _fail(
-                "the archive does not list the files it was made from", partial
-            )
-        if len(parts) == 1:
-            listing = runner.run(["tar", "-tzf", parts[0]], cwd=partial)
-            names = sorted(
-                n for n in listing.stdout.split("\n") if n and not n.endswith("/")
-            )
-            if listing.returncode != 0 or names != in_archive:
-                return _fail("tar could not read the archive back", partial)
-        saved = sorted(todo_untracked + in_archive)
-        with open(
-            os.path.join(partial, SAVED_PATHS_NAME), "w", encoding="utf-8"
-        ) as handle:
-            handle.write("".join(f"{p}\n" for p in saved))
-        sums = {os.path.basename(p): _sha256(p) for p in parts}
-        sums[SAVED_PATHS_NAME] = _sha256(os.path.join(partial, SAVED_PATHS_NAME))
-        with open(
-            os.path.join(partial, MANIFEST_NAME), "w", encoding="utf-8"
-        ) as handle:
-            handle.write(_manifest(facts, pr, repo_slug, saved_at, len(saved), sums))
-        os.makedirs(os.path.dirname(final), exist_ok=True)
-        os.rename(partial, final)
-    except (OSError, ValueError, tarfile.TarError) as exc:
-        return _fail(f"copy failed ({type(exc).__name__})", partial)
-
-    date = (pr.merged_at or "")[:10]
-    suffix = folder[len(base) :]
-    message = f"archive({base.split('/')[0]}): {date} pr{pr.number} {subject}{suffix}"
-    if runner.run(["git", "add", "--", folder], cwd=evidence_dir).returncode != 0:
-        return _fail("the saved folder could not be staged")
-    if (
-        runner.run(
-            ["git", "commit", "--quiet", "-m", message], cwd=evidence_dir
-        ).returncode
-        != 0
-    ):
-        return _fail("the evidence commit failed")
-    problem = _push(runner, evidence_dir)
-    if problem:
-        return _fail(problem)
-    problem = _verify_folder(runner, evidence_dir, folder)
-    if problem:
-        return _fail(problem)
-    n = _count_files(final)
-    return ArchiveResult(
-        True, "", folder, n, every, f"VERIFIED {folder} files={n}", digests_now
-    )
-
-
-# --- the removal pipeline (steps 1 to 7 of "what a removal is") ------------------
-
-
-@dataclass(frozen=True)
-class RemovalResult:
-    status: str  # removed, kept (a safe stop) or failed (a step went wrong; exit 69)
-    reason: str = ""
-    steps: tuple[str, ...] = ()  # what ran, in order, for the table and the log
-    branch: str = ""  # branch removed, kept, or removed with the worktree
-    verified: str = ""  # the VERIFIED line of the save, when there was one
-
-
-def _refusal_text(text: str) -> str:
-    for line in text.splitlines():
-        if line.strip():
-            return line.strip()[:200]
-    return "no message"
-
-
-def _inside(path: str, top: str) -> bool:
-    real, base = os.path.realpath(path), os.path.realpath(top)
-    return real == base or real.startswith(base + os.sep)
-
-
-def remove_worktree(
-    runner: Runner,
-    inp: RuleInputs,
-    pr: PullRequest,
-    evidence_dir: str,
-    evidence_repo: str,
-    proc_root: str = "/proc",
-    log: Callable[[str], None] | None = None,
-) -> RemovalResult:
-    """Remove one removable worktree, step by step; every step fails closed (apply only).
-
-    Callers run this only under ``--apply``. A worktree that is not removable by the eight
-    rules is refused here too, so a tracked edit or a commit after the pull request is never
-    archived, never has terminals closed and is never cleared.
-    """
-    say = log or (lambda _m: None)
-    steps: list[str] = []
-    facts, orca = inp.facts, inp.orca
-    wt = facts.worktree
-    if _has_dev_files(facts.state) and inp.save_state == SAVE_NOT_NEEDED:
-        inp = dataclasses.replace(inp, save_state=SAVE_NEEDED)
-    first = decide(inp)
-    if first.decision != "removable":
-        return RemovalResult("failed" if first.unread else "kept", first.reason)
-    main_checkout = wt.repo_path
-    if _inside(main_checkout, wt.path):
-        return RemovalResult(
-            "failed", "the repo folder is inside the worktree; run from outside it"
-        )
-
-    # 1. save
-    verified, digests = "", {}
-    if _has_dev_files(facts.state):
-        saved = archive_worktree(
-            runner, facts, pr, evidence_dir, evidence_repo, log=say
-        )
-        if not saved.ok:
-            return RemovalResult("failed", saved.reason, tuple(steps))
-        runner.register_saved(wt.path, sorted(saved.saved_paths))
-        verified, digests = saved.verified, saved.digests
-        steps.append(f"saved: {verified}")
-
-    # 2. close the Orca terminals, only now: every rule passed and the save is verified
-    if orca is not None and orca.live_terminal_count > 0:
-        runner.authorize_close(orca.selector)
-        closed = runner.run(
-            ["orca", "terminal", "close", "--worktree", orca.selector, "--all"]
-        )
-        if (
-            closed.returncode != 0
-            or "unverifiable" in (closed.stdout + closed.stderr).lower()
-        ):
-            return RemovalResult(
-                "failed",
-                "Orca terminal close not confirmed",
-                tuple(steps),
-                verified=verified,
-            )
-        steps.append("closed Orca terminals")
-
-    # 3. check again: a terminal may have been working
-    # A fact that cannot be read is a lookup failure (failed, exit 69); a fact that was read
-    # and differs is a change (kept).
-    again = gather_facts(runner, wt, orca)
-    unreadable = ""
-    if not again.present:
-        unreadable = "the folder could not be read"
-    elif again.state is None:
-        unreadable = "git status could not be read"
-    elif again.head is None:
-        unreadable = "HEAD could not be read"
-    else:
-        for p in sorted(digests):
-            saved_path = os.path.join(wt.path, p)
-            if os.path.lexists(saved_path) and _safe_sha(saved_path) is None:
-                unreadable = "a saved file could not be read"
-                break
-    if unreadable:
-        return RemovalResult(
-            "failed",
-            f"re-check failed: {unreadable} after the terminals were closed",
-            tuple(steps),
-            verified=verified,
-        )
-    changed = (
-        again.state != facts.state
-        or again.head != facts.head
-        or any(
-            p in digests and _safe_sha(os.path.join(wt.path, p)) != digests[p]
-            for p in digests
-        )
-    )
-    after = commits_after_pr(runner, wt.path, again.head, pr.head_oid)
-    if after.relation == "unknown":
-        return RemovalResult(
-            "failed",
-            f"re-check failed: {after.reason}",
-            tuple(steps),
-            verified=verified,
-        )
-    if changed or after.relation not in ("same", "ancestor"):
-        return RemovalResult(
-            "kept",
-            "changed since the terminals were closed",
-            tuple(steps),
-            verified=verified,
-        )
-    scan = scan_processes(proc_root)
-    if not scan.ok:
-        return RemovalResult(
-            "failed",
-            f"in use: the process scan failed ({scan.failure})",
-            tuple(steps),
-            verified=verified,
-        )
-    if processes_inside(scan, wt.path):
-        return RemovalResult(
-            "kept",
-            "a process is still inside after its Orca terminals were closed",
-            tuple(steps),
-            verified=verified,
-        )
-    steps.append("checked again")
-
-    # 4. clear exactly the saved files
-    if digests:
-        paths = sorted(digests)
-        stdin = b"".join(p.encode("utf-8", "surrogateescape") + b"\0" for p in paths)
-        cleared = runner.run(
-            ["xargs", "-0", "git", "clean", "-f", "-x", "--"], cwd=wt.path, stdin=stdin
-        )
-        if cleared.returncode != 0:
-            return RemovalResult(
-                "failed",
-                f"clearing the saved files failed: {_refusal_text(cleared.stderr)}",
-                tuple(steps),
-                verified=verified,
-            )
-        steps.append(f"cleared {len(paths)} saved files")
-
-    # 5. remove the worktree
-    if orca is not None:
-        removal = runner.run(
-            ["orca", "worktree", "rm", "--worktree", orca.selector], cwd=main_checkout
-        )
-    else:
-        removal = runner.run(["git", "worktree", "remove", wt.path], cwd=main_checkout)
-    if removal.returncode != 0:
-        why = _refusal_text(removal.stderr or removal.stdout)
-        return RemovalResult(
-            "failed", f"removal refused: {why}", tuple(steps), verified=verified
-        )
-    steps.append("removed the worktree")
-
-    # 6. the local branch, with -d only
-    branch_note = _remove_branch(runner, main_checkout, wt.branch)
-    steps.append(f"branch: {branch_note}")
-
-    # 7. read back
-    problem = _read_back(runner, wt, orca, main_checkout)
-    if problem:
-        return RemovalResult("failed", problem, tuple(steps), branch_note, verified)
-    steps.append("read back")
-    return RemovalResult("removed", "", tuple(steps), branch_note, verified)
-
-
-def _safe_sha(path: str) -> str | None:
-    try:
-        return _sha256(path)
-    except OSError:
-        return None
-
-
-def _remove_branch(runner: Runner, main_checkout: str, branch: str | None) -> str:
-    if not branch:
-        return "none"
-    listed = runner.run(["git", "branch", "--list", branch], cwd=main_checkout)
-    if listed.returncode == 0 and not listed.stdout.strip():
-        return "removed with the worktree"
-    res = runner.run(["git", "branch", "-d", branch], cwd=main_checkout)
-    if res.returncode == 0:
-        return "removed"
-    if "not fully merged" in res.stderr.lower():
-        return "kept (not fully merged, as after a squash merge)"
-    return f"kept ({_refusal_text(res.stderr)})"
-
-
-def _read_back(
-    runner: Runner, wt: GitWorktree, orca: OrcaWorktree | None, main_checkout: str
-) -> str | None:
-    """None when the folder is gone and neither git nor Orca lists the worktree."""
-    if os.path.exists(wt.path):
-        return "removed in git but the folder is still there"
-    listed = runner.run(["git", "worktree", "list", "--porcelain"], cwd=main_checkout)
-    if listed.returncode != 0:
-        return "read back failed: git worktree list failed"
-    gone = os.path.normpath(wt.path)
-    if any(
-        os.path.normpath(e.path) == gone
-        for e in parse_worktree_porcelain(listed.stdout, main_checkout)
-    ):
-        return "removed but git still lists the worktree"
-    seen = runner.run(["orca", "worktree", "list", "--json"], cwd=main_checkout)
-    if seen.returncode != 0:
-        return "read back failed: orca worktree list failed"
-    # judged for every worktree, also one Orca did not list before the removal
-    still = orca_lists(
-        seen.stdout, wt.path, orca.worktree_id if orca is not None else ""
-    )
-    if still is None:
-        return "read back failed: the orca worktree list could not be read"
-    return "removed in git but still listed in Orca" if still else None
-
-
-def orca_lists(text: str, path: str, worktree_id: str) -> bool | None:
-    """Does an ``orca worktree list --json`` reply hold this worktree? None: unreadable.
-
-    Paths and ids are compared for equality, never as text, so a sibling whose name starts
-    with this one's is not mistaken for it.
-    """
-    try:
-        doc = json.loads(text)
-    except (ValueError, TypeError):
-        return None
-    if isinstance(doc, dict) and doc.get("ok") is False:
-        return None  # an Orca error reply cannot be read as "not listed"
-    wanted = {os.path.normpath(path), os.path.realpath(path)}
-    stack: list[Any] = [doc]
-    while stack:
-        node = stack.pop()
-        if isinstance(node, dict):
-            for key, value in node.items():
-                if (
-                    key in ("path", "worktreeId", "id")
-                    and isinstance(value, str)
-                    and value
-                ):
-                    if worktree_id and value == worktree_id:
-                        return True
-                    if os.path.normpath(value) in wanted:
-                        return True
-                stack.append(value)
-        elif isinstance(node, list):
-            stack.extend(node)
-    return False
-
-
-# --- command line ----------------------------------------------------------
-
-
-def settings(env: Mapping[str, str]) -> dict[str, object]:
-    raw = env.get("WORKTREE_CLEANUP_IDLE_DAYS", "")
-    try:
-        idle = int(raw) if raw else IDLE_DAYS_DEFAULT
-    except ValueError:
-        idle = IDLE_DAYS_DEFAULT
-    return {
-        "idle_days": max(idle, 0),
-        "evidence_repo": env.get("RUN_EVIDENCE_REPO", EVIDENCE_REPO_DEFAULT),
-        "evidence_dir": os.path.expanduser(
-            env.get("RUN_EVIDENCE_DIR", EVIDENCE_DIR_DEFAULT)
-        ),
-    }
-
-
-def parse_args(argv: list[str] | None) -> argparse.Namespace:
-    parser = argparse.ArgumentParser(
-        prog="worktree_cleanup",
-        description=(
-            "Remove git worktrees of our own repos once their work is finished. "
-            "A dry run unless --apply is given."
-        ),
-        epilog="Flags of every verb: --apply (really remove) and --out DIR (table files and locks).",
-    )
-    sub = parser.add_subparsers(
-        dest="verb", required=True, metavar="{" + ",".join(VERBS) + "}"
-    )
-    sub.add_parser(
-        "list", help="print the table of every worktree; never removes anything"
-    )
-    p_archive = sub.add_parser(
-        "archive",
-        help="save one worktree's .dev files to the evidence repo; never removes anything",
-        description=(
-            "Save the untracked and ignored .dev files of one merged worktree to the "
-            "evidence repo and check the copy against GitHub; removes nothing. "
-            "Not built: the patch-and-bundle save of tracked edits or later commits "
-            "that the spec mentions. A worktree with such changes is never archived."
-        ),
-    )
-    p_archive.add_argument("worktree", help="worktree path or unique folder name")
-    p_retire = sub.add_parser(
-        "retire", help="remove one worktree whose work is safe (needs --apply)"
-    )
-    p_retire.add_argument("worktree", help="worktree path or unique folder name")
-    sub.add_parser(
-        "prune",
-        help="run the same decision for every worktree (removes only with --apply)",
-    )
-    for p in sub.choices.values():
-        p.add_argument(
-            "--apply",
-            action="store_true",
-            help="actually remove; without it nothing is removed",
-        )
-        p.add_argument(
-            "--out",
-            type=Path,
-            default=None,
-            help=f"folder for the table files and locks (default {DEFAULT_OUT}); never inside a worktree",
-        )
-    return parser.parse_args(argv)
-
-
-# --- the four verbs ------------------------------------------------------------
-
-
-@dataclass
-class Entry:
-    """One worktree with everything its decision rests on."""
-
-    inp: RuleInputs
-    pr: PullRequest | None
-    decision: Decision
-    repo_name: str
-
-
-@dataclass
-class Found:
-    worktrees: list[tuple[GitWorktree, OrcaWorktree | None]]
-    notes: list[str]
-    failures: list[str]
-    orca_known: bool = True  # False when the Orca worktree list could not be read
-
-
-def _current_repo(runner: Runner, cwd: str) -> OrcaRepo | None:
-    """The main checkout of the repo the script was started in, or None."""
-    res = runner.run(["git", "rev-parse", "--git-common-dir"], cwd=cwd)
-    if res.returncode != 0 or not res.stdout.strip():
-        return None
-    common = os.path.normpath(os.path.join(cwd, res.stdout.strip()))
-    top = os.path.dirname(common) if os.path.basename(common) == ".git" else common
-    return OrcaRepo("current", top, os.path.basename(top))
-
-
-def find_worktrees(runner: Runner, cwd: str) -> Found:
-    """Every git worktree of every repo Orca knows (or the current repo when it knows none)."""
-    notes: list[str] = []
-    failures: list[str] = []
-    repos_read = read_orca_repos(runner)
-    if repos_read.ok:
-        repos = list(repos_read.items)
-    else:
-        current = _current_repo(runner, cwd)
-        if current is None:
-            failures.append(
-                f"{repos_read.unavailable}, and the current folder is not a git checkout"
-            )
-            return Found([], notes, failures)
-        repos, note = repos_or_current(repos_read, current)
-        notes.append(note)
-    listed = read_orca_worktrees(runner)
-    by_path: dict[str, OrcaWorktree] = {}
-    if listed.ok:
-        by_path = {os.path.realpath(w.path): w for w in listed.items}
-    else:
-        notes.append(
-            f"{listed.unavailable}; no worktree can be removed while Orca cannot be read"
-        )
-    found = discover_worktrees(runner, repos)
-    failures.extend(found.failures)
-    pairs = [(wt, by_path.get(os.path.realpath(wt.path))) for wt in found.worktrees]
-    return Found(pairs, notes, failures, orca_known=listed.ok)
-
-
-def assess(
-    runner: Runner,
-    cfg: Mapping[str, object],
-    wt: GitWorktree,
-    orca: OrcaWorktree | None,
-    scan: ProcScan,
-    now: float,
-    own_paths: Sequence[str],
-    orca_known: bool = True,
-) -> Entry:
-    """Read every fact of one worktree and apply the eight rules."""
-    facts = gather_facts(runner, wt, orca)
-    inp = RuleInputs(
-        facts=facts,
-        now=now,
-        idle_floor_days=int(cfg["idle_days"]),  # type: ignore[call-overload]
-        orca=orca,
-        procs=scan,
-        own_folder=is_own_folder(wt.path, own_paths),
-        orca_known=orca_known,
-    )
-    pr: PullRequest | None = None
-    repo_name = os.path.basename(wt.repo_path.rstrip("/"))
-    if _rule1(inp) is None and facts.origin is not None:
-        slug = f"{facts.origin.owner}/{facts.origin.repo}"
-        repo_name = facts.origin.repo
-        lookup = find_pull_request(runner, slug, wt.branch)
-        landed = after = None
-        if lookup.ok and lookup.pr is not None:
-            pr = lookup.pr
-            if pr.state == "MERGED":
-                landed = landed_check(runner, slug, pr.number, wt.repo_path)
-                after = commits_after_pr(runner, wt.path, facts.head, pr.head_oid)
-        refs = read_orca_references(runner, orca.selector) if orca else None
-        issues = collect_issues(runner, slug, pr, wt.branch, wt.path, orca, refs)
-        inp = dataclasses.replace(
-            inp, pr_lookup=lookup, landed=landed, after=after, issues=issues
-        )
-    if _has_dev_files(facts.state):
-        inp = dataclasses.replace(inp, save_state=SAVE_NEEDED)
-    return Entry(inp, pr, decide(inp), repo_name)
-
-
-def _assess_all(
-    runner: Runner,
-    cfg: Mapping[str, object],
-    found: Found,
-    now: float,
-    proc_root: str,
-    cwd: str,
-) -> list[Entry]:
-    scan = scan_processes(proc_root)
-    own = [cwd, os.path.abspath(__file__)]
-    return [
-        assess(runner, cfg, wt, orca, scan, now, own, found.orca_known)
-        for wt, orca in found.worktrees
-    ]
-
-
-def resolve_selector(
-    found: Found, selector: str
-) -> tuple[tuple[GitWorktree, OrcaWorktree | None] | None, str]:
-    """A worktree by path or by unique folder name: (match, problem)."""
-    real = os.path.realpath(os.path.expanduser(selector))
-    by_path = [p for p in found.worktrees if os.path.realpath(p[0].path) == real]
-    if by_path:
-        return by_path[0], ""
-    named = [
-        p
-        for p in found.worktrees
-        if os.path.basename(p[0].path.rstrip("/")) == selector
-    ]
-    if len(named) == 1:
-        return named[0], ""
-    if named:
-        return None, f"{selector} matches {len(named)} worktrees; give the full path"
-    return None, f"{selector} is not a git worktree of one of our repos"
-
-
-class RepoLocks:
-    """One lock file per repo in the output folder (flock, non-blocking). Files are never deleted."""
-
-    def __init__(self, out: Path) -> None:
-        self.out = out
-        self._held: dict[str, Any] = {}
-        self.error = ""  # why the last acquire failed, when it was not a held lock
-
-    def acquire(self, repo_path: str) -> bool:
-        import fcntl
-
-        key = os.path.realpath(repo_path)
-        if key in self._held:
-            return True
-        self.error = ""
-        name = "lock-" + hashlib.sha256(key.encode()).hexdigest()[:12] + ".lock"
-        try:
-            self.out.mkdir(parents=True, exist_ok=True)
-            handle = open(self.out / name, "a")
-        except OSError as exc:
-            self.error = (
-                f"lock could not be taken: {exc.strerror or type(exc).__name__}"
-            )
-            return False
-        try:
-            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
-        except OSError:
-            handle.close()
-            return False
-        self._held[key] = handle
-        return True
-
-    def release_all(self) -> None:
-        for handle in self._held.values():
-            handle.close()  # closing drops the lock; the file stays
-        self._held.clear()
-
-
-def _command_log(runner: Runner) -> list[dict[str, Any]]:
-    return [
-        {"argv": c.argv, "cwd": c.cwd, "stdin_paths": c.stdin_paths}
-        for c in runner.commands
-    ]
-
-
-def _apply_removal(
-    runner: Runner,
-    cfg: Mapping[str, object],
-    entry: Entry,
-    locks: RepoLocks,
-    proc_root: str,
-    note: Callable[[str], None],
-) -> tuple[str, str, str]:
-    """(status, reason, saved copy cell) for one removable worktree under --apply."""
-    if entry.pr is None:
-        return "failed", "no merged pull request to remove it under", ""
-    if not locks.acquire(entry.inp.facts.worktree.repo_path):
-        if locks.error:
-            return "failed", locks.error, ""
-        return "kept", "another run holds the lock", ""
-    try:
-        done = remove_worktree(
-            runner, entry.inp, entry.pr, str(cfg["evidence_dir"]),
-            str(cfg["evidence_repo"]), proc_root, note,
-        )  # fmt: skip
-    except (OSError, RefusedCommand) as exc:
-        return "failed", f"{type(exc).__name__} while removing", ""
-    cell = "saved and checked" if done.verified else ""
-    reason = done.reason or f"branch {done.branch}"
-    return done.status, reason, cell
-
-
-def _summarize(
-    rows: Sequence[Mapping[str, str]], entries: Sequence[Entry], applied: bool
-) -> dict[str, Any]:
-    removed = sum(1 for r in rows if r["decision"] == "removed")
-    failed = sum(
-        1
-        for r, e in zip(rows, entries)
-        if r["decision"] == "failed" or (r["decision"] == "kept" and e.decision.unread)
-    )
-    removable = sum(1 for r in rows if r["decision"] == "removable")
-    kept = len(rows) - removed - failed - removable
-    groups: dict[str, list[str]] = {}
-    for r, e in zip(rows, entries):
-        if r["decision"] in ("kept", "removable") and e.decision.rule is not None:
-            groups.setdefault(f"rule {e.decision.rule}", []).append(r["reason"])
-    first = {
-        name: (reasons[0], len(reasons)) for name, reasons in sorted(groups.items())
-    }
-    return {
-        "removed": removed, "kept": kept + removable, "failed": failed,
-        "removable": removable, "dry_run": not applied, "first_reasons": first,
-    }  # fmt: skip
-
-
-def _summary_text(s: Mapping[str, Any]) -> str:
-    lines = [f"summary: removed {s['removed']}, kept {s['kept']}, failed {s['failed']}"]
-    if s["dry_run"] and s["removable"]:
-        lines[0] += f" ({s['removable']} removable; dry run, nothing was removed)"
-    if not s["removed"] and not s["removable"]:
-        lines.append("nothing more to do")
-    for name, (reason, count) in s["first_reasons"].items():
-        lines.append(
-            f"  kept at {name}: {reason} ({count} worktree{'s' if count != 1 else ''})"
-        )
-    return "\n".join(lines)
-
-
-def _inside_any(path: Path, found: Found) -> bool:
-    return any(_inside(str(path), wt.path) for wt, _orca in found.worktrees)
-
-
-def _run_verb(
-    args: argparse.Namespace,
-    runner: Runner,
-    cfg: Mapping[str, object],
-    now: float,
-    proc_root: str,
-    cwd: str,
-) -> int:
-    out = Path(args.out) if args.out else Path(os.path.expanduser(DEFAULT_OUT))
-    found = find_worktrees(runner, cwd)
-    for note in found.notes:
-        print(f"note: {note}")
-    for why in found.failures:
-        print(f"failed: {why}", file=sys.stderr)
-    failures = len(found.failures)
-    locks = RepoLocks(out)
-    log = lambda m: print(f"log: {m}")  # noqa: E731
-    # nothing is ever written inside a worktree: checked for every verb before any write
-    if _inside_any(out.expanduser(), found):
-        print("error: --out must not be inside a worktree", file=sys.stderr)
-        return EXIT_USAGE
-    try:
-        if args.verb in ("archive", "retire"):
-            return _one_worktree(
-                args, runner, cfg, found, now, proc_root, cwd, locks, log
-            )
-        if args.verb == "prune":
-            try:  # created before any removal starts, so a bad folder stops the run first
-                out.mkdir(parents=True, exist_ok=True)
-            except OSError as exc:
-                print(f"error: --out cannot be used: {exc.strerror}", file=sys.stderr)
-                return EXIT_FAILED
-        entries = _assess_all(runner, cfg, found, now, proc_root, cwd)
-        rows = []
-        for entry in entries:
-            row = table_row(entry.inp, entry.decision, entry.repo_name)
-            if (
-                args.verb == "prune"
-                and args.apply
-                and entry.decision.decision == "removable"
-            ):
-                status, reason, cell = _apply_removal(
-                    runner, cfg, entry, locks, proc_root, log
-                )
-                row["decision"], row["reason"] = status, reason
-                row["saved_copy"] = cell or row["saved_copy"]
-            rows.append(row)
-        summary = _summarize(rows, entries, bool(args.apply and args.verb == "prune"))
-        print(render_markdown(rows))
-        print(_summary_text(summary))
-        if args.verb == "prune":
-            stamp = datetime.fromtimestamp(now, timezone.utc).strftime("%Y%m%dT%H%M%SZ")
-            try:
-                (out / f"prune-{stamp}.md").write_text(
-                    render_markdown(rows), encoding="utf-8"
-                )
-                (out / f"prune-{stamp}.json").write_text(
-                    render_json(rows, _command_log(runner), summary), encoding="utf-8"
-                )
-            except OSError as exc:
-                print(
-                    f"error: the output files could not be written: {exc.strerror}",
-                    file=sys.stderr,
-                )
-                return EXIT_FAILED
-        return EXIT_FAILED if failures or summary["failed"] else EXIT_OK
-    finally:
-        locks.release_all()
-
-
-def _one_worktree(
-    args: argparse.Namespace,
-    runner: Runner,
-    cfg: Mapping[str, object],
-    found: Found,
-    now: float,
-    proc_root: str,
-    cwd: str,
-    locks: RepoLocks,
-    log: Callable[[str], None],
-) -> int:
-    match, problem = resolve_selector(found, args.worktree)
-    if match is None:
-        print(f"error: {problem}", file=sys.stderr)
-        # a repo whose worktree list failed may hold it: a lookup failure, not a usage error
-        return EXIT_FAILED if found.failures else EXIT_USAGE
-    wt, orca = match
-    if args.verb == "retire" and _inside(cwd, wt.path):
-        print("error: run retire from outside the worktree", file=sys.stderr)
-        return EXIT_USAGE
-    entry = assess(
-        runner,
-        cfg,
-        wt,
-        orca,
-        scan_processes(proc_root),
-        now,
-        [cwd, os.path.abspath(__file__)],
-        found.orca_known,
-    )
-    row = table_row(entry.inp, entry.decision, entry.repo_name)
-    d = entry.decision
-    if args.verb == "archive":
-        if d.rule is not None and d.rule < 6:
-            print(render_markdown([row]))
-            print(f"error: cannot archive: {d.reason}", file=sys.stderr)
-            return EXIT_FAILED if d.unread else EXIT_USAGE
-        if not locks.acquire(wt.repo_path):
-            print(
-                f"error: {locks.error or 'another run holds the lock'}", file=sys.stderr
-            )
-            return EXIT_FAILED
-        try:
-            saved = archive_worktree(
-                runner, entry.inp.facts, entry.pr, str(cfg["evidence_dir"]),
-                str(cfg["evidence_repo"]), log=log,
-            )  # fmt: skip
-        except (OSError, RefusedCommand) as exc:
-            print(f"error: saved copy failed: {type(exc).__name__}", file=sys.stderr)
-            return EXIT_FAILED
-        if not saved.ok:
-            print(f"error: {saved.reason}", file=sys.stderr)
-            return EXIT_FAILED
-        print(saved.verified)
-        return EXIT_OK
-    # retire
-    print(render_markdown([row]))
-    if d.decision != "removable":
-        print(f"error: not removable: {d.reason}", file=sys.stderr)
-        return EXIT_FAILED if d.unread else EXIT_USAGE
-    if not args.apply:
-        print("dry run: nothing was removed; add --apply to remove it")
-        return EXIT_OK
-    status, reason, _cell = _apply_removal(runner, cfg, entry, locks, proc_root, log)
-    print(f"{status}: {reason}")
-    if status == "removed":
-        return EXIT_OK
-    return EXIT_FAILED if status == "failed" else EXIT_USAGE
-
-
-def main(
-    argv: list[str] | None = None,
-    runner: Runner | None = None,
-    env: Mapping[str, str] | None = None,
-    now: float | None = None,
-    proc_root: str = "/proc",
-    cwd: str | None = None,
-) -> int:
-    args = parse_args(argv)
-    env = os.environ if env is None else env
-    cfg = settings(env)
-    runner = runner or Runner(evidence_dir=str(cfg["evidence_dir"]))
-    try:
-        return _run_verb(
-            args,
-            runner,
-            cfg,
-            time.time() if now is None else now,
-            proc_root,
-            cwd or os.getcwd(),
-        )
-    except RefusedCommand as exc:
-        print(f"internal error: a command was refused: {exc}", file=sys.stderr)
-        return EXIT_FAILED
-
-
-if __name__ == "__main__":
-    sys.exit(main())


===== new file: tests/worktree_cleanup/test_pipeline.py =====
"""The removal pipeline end to end, through the verbs (Task 13).

Every case runs ``main`` on a throwaway repository under ``tmp_path`` with a local bare
repository standing in for the evidence repo and canned ``gh`` and ``orca`` replies. Nothing
here touches a real worktree, a real Orca terminal or the real evidence repo.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

from .conftest import git_in, make_fake_proc
from .test_archive import git_identity  # noqa: F401 - autouse: the evidence commit needs an identity
from .test_facts import write
from .test_verbs import World


@pytest.fixture
def world(wc, runner_cls, throwaway_repo, evidence_bare, tmp_path):
    return World(wc, runner_cls, throwaway_repo, evidence_bare, tmp_path)


def open_terminals(wc, world, name, count=2, on_close=None, close_reply=None):
    """Orca lists ``name`` with live terminals; ``on_close`` runs when the terminals are closed."""
    world.listed = {name}
    path = world.paths[name]

    def orca(argv, cwd):
        key = tuple(argv[1:3])
        if key == ("worktree", "ps"):
            rows = [{"worktreeId": f"id-{name}", "path": str(path), "isPinned": False,
                     "liveTerminalCount": count, "lastActivityAt": None, "linkedPR": None, "comment": ""}]  # fmt: skip
            return wc.Result(
                0, json.dumps({"ok": True, "result": {"worktrees": rows}}), ""
            )
        if key == ("terminal", "close"):
            if on_close is not None:
                on_close()
            return close_reply or wc.Result(0, "", "")
        return World.orca(world, argv, cwd)

    world.runner.replies["orca"] = orca


def position(world, predicate):
    for i, c in enumerate(world.runner.commands):
        if predicate(c.argv):
            return i
    return None


def cleared(world):
    return any(c.argv[:2] == ["xargs", "-0"] for c in world.runner.commands)


def closed_terminals(world):
    return any(
        c.argv[:3] == ["orca", "terminal", "close"] for c in world.runner.commands
    )


# -- decision 3: terminals open and a process inside ---------------------------------------------------------------


def test_terminals_and_a_process_inside_are_closed_first_and_the_second_check_runs(
    wc, world, tmp_path, capsys
):
    world.add("done")
    path = world.paths["done"]
    proc = make_fake_proc(tmp_path / "proc-busy", {42: str(path)})
    world.proc = str(proc)
    open_terminals(
        wc, world, "done", on_close=lambda: os.rename(proc / "42", tmp_path / "exited")
    )  # closing the terminals ends the process
    # a dry run says what would happen and closes nothing
    assert world.run("prune") == 0
    assert "its Orca terminals will be closed first" in capsys.readouterr().out
    assert not closed_terminals(world) and path.exists()
    # under --apply the close comes first, then the second check, then the clear, then the removal
    assert world.run("prune", "--apply") == 0
    assert not path.exists()
    close = position(world, lambda a: a[:3] == ["orca", "terminal", "close"])
    assert world.runner.commands[close].argv[3:] == [
        "--worktree",
        "id:id-done",
        "--all",
    ]
    status = position(world, lambda a: "status" in a and a[0] == "git")
    last_status = max(
        i
        for i, c in enumerate(world.runner.commands)
        if "status" in c.argv and c.argv[0] == "git"
    )
    clear = position(world, lambda a: a[:2] == ["xargs", "-0"])
    removal = position(world, lambda a: a[:3] == ["orca", "worktree", "rm"])
    assert status is not None and close < last_status < clear < removal


@pytest.mark.parametrize(
    "reply", [(0, '{"unverifiable": true}'), (1, ""), (0, "closed, UNVERIFIABLE")]
)
def test_a_terminal_close_that_is_unverifiable_or_fails_keeps_the_worktree(
    wc, world, reply
):
    world.add("done")
    path = world.paths["done"]
    open_terminals(wc, world, "done", close_reply=wc.Result(reply[0], reply[1], ""))
    assert world.run("prune", "--apply") == 69
    assert path.exists() and (path / ".dev" / "tasks" / "note.md").exists()
    assert not cleared(world)
    assert not any(c.argv[1:3] == ["worktree", "remove"] for c in world.runner.commands)


def test_a_process_still_inside_after_the_close_keeps_the_worktree(
    wc, world, tmp_path, capsys
):
    world.add("done")
    path = world.paths["done"]
    world.proc = str(make_fake_proc(tmp_path / "proc-stuck", {42: str(path)}))
    open_terminals(wc, world, "done")  # the close succeeds, the process does not end
    assert world.run("prune", "--apply") == 0
    assert (
        "a process is still inside after its Orca terminals were closed"
        in capsys.readouterr().out
    )
    assert closed_terminals(world) and path.exists() and not cleared(world)


def _new_commit(path):
    git_in(path, "commit", "--allow-empty", "-q", "-m", "late")


def _tracked_edit(path):
    (path / "README.md").write_text("edited meanwhile\n", encoding="utf-8")


def _untracked_outside_dev(path):
    write(path / "stray-notes.txt")


@pytest.mark.parametrize(
    "change", [_new_commit, _tracked_edit, _untracked_outside_dev],
    ids=["new commit", "tracked edit", "untracked file outside .dev"],
)  # fmt: skip
def test_a_change_between_the_save_and_the_close_keeps_the_worktree(
    wc, world, capsys, change
):
    world.add("done")
    path = world.paths["done"]
    open_terminals(wc, world, "done", on_close=lambda: change(path))
    assert world.run("prune", "--apply") == 0
    assert "changed since the terminals were closed" in capsys.readouterr().out
    assert path.exists() and (path / ".dev" / "tasks" / "note.md").exists()
    assert not cleared(world)
    assert not any(c.argv[1:3] == ["worktree", "rm"] for c in world.runner.commands)


# -- decision 2: no save of tracked edits or later commits ----------------------------------------------------------


def test_a_merged_worktree_with_a_tracked_edit_is_kept_and_nothing_is_done(
    world, capsys
):
    path = world.add("edited")
    _tracked_edit(path)
    assert world.run("prune", "--apply") == 0
    assert "changed tracked file" in capsys.readouterr().out
    assert path.exists() and (path / ".dev" / "tasks" / "note.md").exists()
    assert not cleared(world) and not closed_terminals(world)
    assert not Path(world.clone).exists()  # nothing was archived by prune
    assert not any("push" in c.argv for c in world.runner.commands)


def test_a_merged_worktree_with_a_commit_after_the_pull_request_is_kept_and_nothing_is_done(
    wc, world, capsys
):
    path = world.add("later")
    merged_head = world.head("later")
    _new_commit(path)

    def stale_pull_request(argv):  # the pull request ended at the earlier commit
        rows = [{"number": 700, "state": "MERGED", "headRefOid": merged_head,
                 "headRefName": "later", "author": {"login": "example-user"},
                 "mergedAt": "2026-11-10T12:00:00Z", "title": "t", "body": "",
                 "closingIssuesReferences": []}]  # fmt: skip
        return wc.Result(0, json.dumps(rows), "")

    world.gh_override[("pr", "list")] = stale_pull_request
    assert world.run("prune", "--apply") == 0
    assert "later" in capsys.readouterr().out
    assert path.exists() and (path / ".dev" / "tasks" / "note.md").exists()
    assert not cleared(world) and not closed_terminals(world)
    assert not Path(world.clone).exists()
    assert not any("push" in c.argv for c in world.runner.commands)


# -- the branch ---------------------------------------------------------------------------------------------------------


def test_the_branch_is_removed_with_d_and_a_squash_merge_refusal_reports_kept(
    world, capsys
):
    world.add("done")
    squashed = world.add("squashed")
    write(squashed / "feature.txt")
    git_in(squashed, "add", "feature.txt")
    git_in(squashed, "commit", "-q", "-m", "work that main never received")
    assert world.run("prune", "--apply") == 0
    shown = capsys.readouterr().out
    assert not world.paths["done"].exists() and not squashed.exists()
    branch_commands = [c.argv for c in world.runner.commands if "branch" in c.argv]
    assert branch_commands and all("-D" not in a for a in branch_commands)
    assert git_in(world.repo.main, "branch", "--list", "done").strip() == ""
    # git refuses -d after a squash merge: the branch stays and that is not an error
    assert "squashed" in git_in(world.repo.main, "branch", "--list", "squashed")
    assert "failed 0" in shown


# -- a second run, two runs, folders that are not worktrees ----------------------------------------------------------------


def test_a_second_run_finds_nothing_more_to_do(world, capsys):
    world.add("done")
    assert world.run("prune", "--apply") == 0
    capsys.readouterr()
    assert world.run("prune", "--apply") == 0
    assert "nothing more to do" in capsys.readouterr().out
    assert world.removal_commands() == []


def test_two_runs_at_once_do_not_both_remove_the_same_worktree(wc, world, capsys):
    world.add("done")
    first = wc.RepoLocks(world.out)  # the run that is already removing
    assert first.acquire(str(world.repo.main)) is True
    try:
        assert world.run("prune", "--apply") == 0
        pruned = capsys.readouterr().out
        assert world.run("retire", "done", "--apply") == 64  # it was not removed
        retired = capsys.readouterr().out
    finally:
        first.release_all()
    assert "another run holds the lock" in pruned
    assert "another run holds the lock" in retired
    # a worktree skipped because of the lock is work left to do, not "nothing more to do"
    assert "nothing more to do" not in pruned
    assert world.paths["done"].exists() and world.removal_commands() == []


def test_folders_that_are_not_worktrees_of_our_repos_never_appear_and_are_never_touched(
    world, capsys
):
    world.add("done")
    wts = world.repo.root / "wts"
    strays = [wts / "plain-folder", wts / "orca-port-3000", wts / "coder-orca-port"]
    for stray in strays:
        stray.mkdir()
        write(stray / "keep.txt")
    assert world.run("prune", "--apply") == 0
    shown = capsys.readouterr().out
    for stray in strays:
        assert stray.name not in shown
        assert (stray / "keep.txt").exists()


# -- decision 1: exactly the saved paths are cleared --------------------------------------------------------------------------


def test_exactly_the_listed_paths_are_cleared_and_nothing_else(
    wc, runner_cls, throwaway_repo, tmp_path
):
    path = throwaway_repo.add_worktree("topic")
    listed = ".dev/tasks/a b.md"  # a name with a space
    for rel in (listed, ".dev/tasks/unlisted.md", ".dev/local/unlisted-ignored.log"):
        write(path / rel)
    runner = runner_cls(evidence_dir=str(tmp_path / "evidence"))
    runner.register_saved(str(path), [listed])
    stdin = listed.encode() + b"\0"
    done = runner.run(
        ["xargs", "-0", "git", "clean", "-f", "-x", "--"], cwd=str(path), stdin=stdin
    )
    assert done.returncode == 0, done.stderr
    assert not (path / listed).exists()
    assert (
        path / ".dev" / "tasks" / "unlisted.md"
    ).exists()  # an untracked file not listed
    assert (
        path / ".dev" / "local" / "unlisted-ignored.log"
    ).exists()  # an ignored file not listed
    assert (path / "README.md").exists()  # a tracked file
    # a path that is not in the saved list is refused before any process starts
    with pytest.raises(wc.RefusedCommand):
        runner.run(
            ["xargs", "-0", "git", "clean", "-f", "-x", "--"],
            cwd=str(path),
            stdin=b".dev/tasks/unlisted.md\0",
        )
    assert (path / ".dev" / "tasks" / "unlisted.md").exists()


# -- the facts the design leans on, on throwaway repositories only ----------------------------------------------------------


def test_git_worktree_remove_without_force_refuses_dirty_and_removes_ignored_only(
    throwaway_repo,
):
    repo = throwaway_repo
    untracked = repo.add_worktree("untracked")
    write(untracked / "new.txt")
    edited = repo.add_worktree("edited")
    (edited / "README.md").write_text("edited\n", encoding="utf-8")
    ignored = repo.add_worktree("ignored")
    write(ignored / ".venv" / "lib" / "x.py")
    for path in (untracked, edited):
        with pytest.raises(subprocess.CalledProcessError):
            git_in(repo.main, "worktree", "remove", str(path))
        assert path.exists()
    git_in(repo.main, "worktree", "remove", str(ignored))
    assert not ignored.exists()


def test_git_branch_d_refuses_after_a_squash_merge(throwaway_repo):
    repo = throwaway_repo
    path = repo.add_worktree("topic")
    write(path / "feature.txt")
    git_in(path, "add", "feature.txt")
    git_in(path, "commit", "-q", "-m", "work")
    git_in(repo.main, "worktree", "remove", str(path))
    with pytest.raises(subprocess.CalledProcessError) as refused:
        git_in(repo.main, "branch", "-d", "topic")
    assert "not fully merged" in refused.value.stderr


===== new file: tests/worktree_cleanup/test_safety.py =====
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
    rec.run("archive", "done", expect=0)
    rec.run("retire", "done", expect=0)  # a dry run
    rec.run("archive", "open", expect=64)
    rec.run("archive", "edited", expect=64)
    rec.run("retire", "open", "--apply", expect=64)
    rec.run("retire", "edited", "--apply", expect=64)
    rec.run("retire", "main", "--apply", expect=64)
    rec.world.runner.ready = frozenset({"done"})
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
        if "--apply" not in argv:
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
