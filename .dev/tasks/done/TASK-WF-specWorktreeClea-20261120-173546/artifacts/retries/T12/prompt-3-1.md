44f5941e9fc784d4934bd6650ea57ab811cc7d1a
Review one task for spec compliance.

Task brief: ## Task 12: Implement the four verbs, the per-repo lock, the output files and the exit codes

Depends on: Task 11

In `scripts/worktree_cleanup.py` fill in the verb bodies: `list` prints the table for every worktree of every repo of ours and never removes; `archive <worktree>` runs only the archive step of Task 9 on one worktree (its help text states that the patch-and-bundle save of tracked edits or later commits mentioned in source section 7 is not built); `retire <worktree>` removes one worktree under `--apply` after the archive step when needed, must be run from outside the worktree, accepts a path or a unique folder name and exits 64 for an unknown or ambiguous selector or a worktree that is not removable; `prune` runs the same decision code on all worktrees in the same run and, with `--apply` only, removes the removable ones through Task 11, while without `--apply` it prints the table and writes `<out dir>/prune-<UTC timestamp>.md` and the `.json` of the same rows plus a `commands` list in that `.json` holding every command the runner ran (argument lists and working folders). One lock file per repo in the output folder using `fcntl.flock` with a non-blocking exclusive lock and no file deletion: a run that cannot take a repo's lock skips that repo and says "another run holds the lock". Print one summary (how many removed, kept and failed, and the first reason of each kept group). Exit codes: 0 when the run completed, 64 for a usage error or a `retire` of a worktree that is not removable, 69 when a lookup or a removal failed (the table still shows what happened). A second run after a removal finds nothing more to do. Folders that are not git worktrees of our repos never appear. No output names an agent or a model.

Acceptance criteria:
- `list` and `prune` without `--apply` record no removal command; with `--apply`, only rows marked removable are processed.
- Two runs started against the same repo cannot both remove the same worktree (the second reports the lock); a run after a successful removal reports nothing to do.
- The three exit codes behave as described (0 completed, 64 usage or non-removable `retire`, 69 lookup or removal failure) and the summary line carries the three counts.
- `prune` writes both output files under `--out` and writes nothing inside any worktree; the JSON holds `rows` and `commands`.

AC ids (in source order): T12.AC1, T12.AC2, T12.AC3, T12.AC4
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
Start sha: 44f5941e9fc784d4934bd6650ea57ab811cc7d1a
Diff against the start snapshot: diff --git a/scripts/worktree_cleanup.py b/scripts/worktree_cleanup.py
deleted file mode 100644
index e2cb459cb..000000000
--- a/scripts/worktree_cleanup.py
+++ /dev/null
@@ -1,2642 +0,0 @@
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
-
-
-@dataclass(frozen=True)
-class Decision:
-    decision: str  # removable or kept
-    rule: int | None  # the first rule that failed, 1 to 8
-    reason: str
-    note: str = ""
-    saved_copy: str = "none needed"
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
-            return Decision("kept", number, reason, "", cell)
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
-    if i.pr_lookup is None or not i.pr_lookup.ok:
-        pr_cell = "lookup failed"
-    else:
-        pr_cell = f"#{pr.number} {pr.state}" if pr else "none"
-    if i.issues is None:
-        issue_cell = "lookup failed"
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
-def render_json(rows: Sequence[Mapping[str, str]]) -> str:
-    return json.dumps(
-        {"columns": list(TABLE_COLUMNS), "rows": [dict(r) for r in rows]}, indent=2
-    )
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
-        return RemovalResult("kept", first.reason)
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
-    again = gather_facts(runner, wt, orca)
-    changed = (
-        again.state is None
-        or again.state != facts.state
-        or again.head != facts.head
-        or any(
-            p in digests and _safe_sha(os.path.join(wt.path, p)) != digests[p]
-            for p in digests
-        )
-    )
-    after = commits_after_pr(runner, wt.path, again.head, pr.head_oid)
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
-            "kept",
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
-def main(
-    argv: list[str] | None = None,
-    runner: Runner | None = None,
-    env: Mapping[str, str] | None = None,
-) -> int:
-    args = parse_args(argv)
-    env = os.environ if env is None else env
-    cfg = settings(env)
-    runner = runner or Runner(evidence_dir=str(cfg["evidence_dir"]))
-    out = args.out or Path(os.path.expanduser(DEFAULT_OUT))
-    _ = (runner, out)  # used by the verbs below
-    print(f"worktree_cleanup {args.verb}: not built yet", file=sys.stderr)
-    return EXIT_USAGE
-
-
-if __name__ == "__main__":
-    sys.exit(main())
diff --git a/tests/worktree_cleanup/test_removal.py b/tests/worktree_cleanup/test_removal.py
deleted file mode 100644
index d7496067d..000000000
--- a/tests/worktree_cleanup/test_removal.py
+++ /dev/null
@@ -1,558 +0,0 @@
-"""The removal pipeline (Task 11): save, close terminals, check again, clear, remove, branch, read back.
-
-Real git runs on throwaway repositories under ``tmp_path`` with local bare remotes; ``orca``
-answers come from canned replies. Nothing here touches a real worktree.
-"""
-
-from __future__ import annotations
-
-import dataclasses
-import os
-from pathlib import Path
-
-import pytest
-
-from .conftest import git_in, make_fake_proc
-from .test_archive import UNSET, Case, git_identity, make_pr  # noqa: F401 - the fixture is autouse
-from .test_facts import write
-
-NOW = 2_000_000_000.0
-DAY = 86400.0
-OLD = {
-    "git_file_mtime": NOW - 20 * DAY,
-    "last_commit_ts": NOW - 20 * DAY,
-    "created_ts": NOW - 30 * DAY,
-}
-GOOD_ORCA_LIST = '{"ok": true, "result": {"worktrees": []}}'
-
-
-def result(wc, code=0, out="", err=""):
-    return wc.Result(code, out, err)
-
-
-class Setup:
-    """One worktree with .dev files, ready to be removed, plus the inputs the rules need."""
-
-    def __init__(
-        self,
-        wc,
-        runner_cls,
-        repo,
-        evidence_bare,
-        tmp_path,
-        orca_replies=None,
-        with_orca=False,
-    ):
-        self.wc, self.tmp = wc, tmp_path
-        self.orca_calls: list[list[str]] = []
-        self.orca_replies = dict(orca_replies or {})
-        self.case = Case(
-            wc, runner_cls, repo, evidence_bare, tmp_path, replies={"orca": self.orca}
-        )
-        self.with_orca = with_orca
-        self.proc_root = str(make_fake_proc(tmp_path / "proc", {}))
-        self.pr_head = None
-
-    def orca(self, argv, cwd):
-        self.orca_calls.append(list(argv))
-        key = tuple(argv[1:3])
-        handler = self.orca_replies.get(key)
-        if handler is not None:
-            return handler(argv, cwd)
-        if key == ("worktree", "list"):
-            return result(self.wc, 0, GOOD_ORCA_LIST)
-        if key == ("worktree", "rm"):  # Orca removes through git, as the real one does
-            git_in(self.case.repo.main, "worktree", "remove", str(self.case.path))
-            return result(self.wc)
-        return result(self.wc)
-
-    @property
-    def runner(self):
-        return self.case.runner
-
-    def inputs(self, pr_head=None, terminals=2, procs=None, **facts_change):
-        wc = self.wc
-        facts = dataclasses.replace(self.case.facts(), **OLD, **facts_change)
-        pr = make_pr(wc, head_oid=pr_head or facts.head)
-        orca = None
-        if self.with_orca:
-            orca = wc.OrcaWorktree(
-                worktree_id="wid", selector="id:wid", path=str(self.case.path), branch="topic", repo="r",
-                last_activity_ms=None, is_pinned=False, live_terminal_count=terminals,
-                linked_pr_hint=None, comment="",
-            )  # fmt: skip
-        after = self.runner_after(facts, pr)
-        inp = wc.RuleInputs(
-            facts=facts, now=NOW, orca=orca, pr_lookup=wc.PrLookup(True, pr),
-            landed=wc.Landed("MERGED", "installed copy"), after=after,
-            issues=wc.IssueFacts((), ()), procs=procs or wc.ProcScan(True, ()),
-        )  # fmt: skip
-        return inp, pr
-
-    def runner_after(self, facts, pr):
-        return self.wc.commits_after_pr(
-            self.runner, str(self.case.path), facts.head, pr.head_oid
-        )
-
-    def remove(self, inp=None, pr=None, proc_root=None):
-        if inp is None:
-            inp, pr = self.inputs()
-        self.runner.commands.clear()
-        return self.wc.remove_worktree(
-            self.runner, inp, pr, self.case.clone, str(self.case.bare),
-            proc_root=proc_root or self.proc_root, log=self.case.notes.append,
-        )  # fmt: skip
-
-    def verbs(self):
-        out = []
-        for c in self.runner.commands:
-            argv = list(c.argv)
-            if argv[0] == "git":  # drop the leading -c and -C options
-                while argv[1] in ("-c", "-C"):
-                    del argv[1:3]
-                out.append(" ".join(argv[1:3]))
-            else:
-                out.append(" ".join(argv[:2]))
-        return out
-
-
-@pytest.fixture
-def setup(wc, runner_cls, throwaway_repo, evidence_bare, tmp_path):
-    return Setup(wc, runner_cls, throwaway_repo, evidence_bare, tmp_path)
-
-
-@pytest.fixture
-def setup_orca(wc, runner_cls, throwaway_repo, evidence_bare, tmp_path):
-    return Setup(
-        wc, runner_cls, throwaway_repo, evidence_bare, tmp_path, with_orca=True
-    )
-
-
-def index_of(verbs, start):
-    return next(i for i, v in enumerate(verbs) if v.startswith(start))
-
-
-def last_index_of(verbs, start):
-    return max(i for i, v in enumerate(verbs) if v.startswith(start))
-
-
-# -- the whole removal, in order --------------------------------------------------------------
-
-
-def test_a_worktree_orca_does_not_list_is_removed_with_git_in_the_right_order(setup):
-    path = setup.case.path
-    done = setup.remove()
-    assert done.status == "removed", done.reason
-    assert done.verified.startswith("VERIFIED ") and done.branch == "removed"
-    assert not path.exists()
-    assert (
-        Path(setup.case.clone) / "IronClaude" / "example-user"
-    ).is_dir()  # the save is in the clone
-    verbs = setup.verbs()
-    push = index_of(verbs, "push")
-    clear = index_of(verbs, "xargs")
-    remove = index_of(verbs, "worktree remove")
-    branch = index_of(verbs, "branch -d")
-    assert push < clear < remove < branch < last_index_of(verbs, "worktree list")
-    # Orca never listed it: the only Orca call is the read back
-    orca = [c.argv for c in setup.runner.commands if c.argv[0] == "orca"]
-    assert orca == [["orca", "worktree", "list", "--json"]]
-    assert done.steps[0].startswith("saved: VERIFIED") and done.steps[-1] == "read back"
-    cleared = setup.runner.commands[clear]
-    assert (
-        cleared.argv == ["xargs", "-0", "git", "clean", "-f", "-x", "--"]
-        and cleared.stdin_paths == 2
-    )
-    assert cleared.cwd == str(path)
-    # the removal runs from the repo's main checkout, never from inside the worktree
-    removal = setup.runner.commands[remove]
-    assert removal.cwd == str(setup.case.repo.main) and removal.argv[-1] == str(path)
-
-
-def test_the_orca_path_closes_terminals_after_the_save_and_before_the_clear(setup_orca):
-    done = setup_orca.remove()
-    assert done.status == "removed", done.reason
-    verbs = setup_orca.verbs()
-    order = [
-        index_of(verbs, "push"),
-        index_of(verbs, "orca terminal"),
-        last_index_of(verbs, "status"),  # the re-check reads, after the close
-        index_of(verbs, "xargs"),
-        index_of(verbs, "orca worktree"),
-        index_of(verbs, "branch --list"),
-        last_index_of(verbs, "orca worktree"),  # the read back lists it again
-    ]
-    assert order == sorted(order) and len(set(order)) == len(order)
-    assert [
-        "orca",
-        "terminal",
-        "close",
-        "--worktree",
-        "id:wid",
-        "--all",
-    ] in setup_orca.orca_calls
-    assert ["orca", "worktree", "rm", "--worktree", "id:wid"] in setup_orca.orca_calls
-    assert not any(
-        v.startswith("worktree remove") for v in verbs
-    )  # Orca did the removal
-    assert done.branch == "removed with the worktree" or done.branch == "removed"
-
-
-def test_no_recorded_command_is_forbidden(setup_orca):
-    assert setup_orca.remove().status == "removed"
-    evidence = os.path.realpath(setup_orca.case.clone)
-    for c in setup_orca.runner.commands:
-        argv = c.argv
-        if (
-            argv[0] != "xargs"
-        ):  # the one -f of the whole run is the clean, checked below
-            assert "--force" not in argv and "-D" not in argv and "-f" not in argv
-        assert argv[0] not in ("rm", "mv") and ["worktree", "prune"] != argv[1:3]
-        assert not (argv[0] == "git" and "--delete" in argv)
-        if "push" in argv:
-            assert os.path.realpath(c.cwd) == evidence and argv[-2:] == [
-                "origin",
-                "main",
-            ]
-        if "git" in argv[:1] and "clean" in argv:
-            raise AssertionError("git clean must run only through xargs")
-    clean = [c for c in setup_orca.runner.commands if c.argv[0] == "xargs"]
-    assert len(clean) == 1 and clean[0].argv[1:] == [
-        "-0",
-        "git",
-        "clean",
-        "-f",
-        "-x",
-        "--",
-    ]
-
-
-# -- fail closed at every step ---------------------------------------------------------------------
-
-
-def test_a_tracked_edit_or_a_commit_after_the_pull_request_does_nothing(wc, setup_orca):
-    edit = setup_orca.case.path / "README.md"
-    edit.write_text("edited\n", encoding="utf-8")
-    done = setup_orca.remove()
-    assert (done.status, done.reason) == ("kept", "1 changed tracked file")
-    assert (
-        setup_orca.runner.commands == [] and setup_orca.orca_calls == []
-    )  # no archive, close or clear
-    assert (
-        edit.exists() and (setup_orca.case.path / ".dev" / "tasks" / "a b.md").exists()
-    )
-    # a commit made after the pull request's last commit
-    edit.write_text("example\n", encoding="utf-8")
-    inp, pr = setup_orca.inputs()
-    old_head = pr.head_oid
-    write(setup_orca.case.path / "later.txt")
-    git_in(setup_orca.case.path, "add", "later.txt")
-    git_in(setup_orca.case.path, "commit", "-q", "-m", "after the pull request")
-    inp, pr = setup_orca.inputs(pr_head=old_head)
-    done = setup_orca.remove(inp, pr)
-    assert (done.status, done.reason) == ("kept", "1 commit after the pull request")
-    assert setup_orca.runner.commands == [] and setup_orca.orca_calls == []
-
-
-@pytest.mark.parametrize(
-    "answer", [(0, '{"unverifiable": true}'), (1, ""), (0, "closed but UNVERIFIABLE")]
-)
-def test_an_unconfirmed_terminal_close_keeps_the_worktree_and_clears_nothing(
-    wc, setup_orca, answer
-):
-    setup_orca.orca_replies[("terminal", "close")] = lambda argv, cwd: result(
-        wc, *answer
-    )
-    done = setup_orca.remove()
-    assert (done.status, done.reason) == ("failed", "Orca terminal close not confirmed")
-    assert setup_orca.case.path.exists()
-    assert not any(c.argv[0] == "xargs" for c in setup_orca.runner.commands)
-    assert (setup_orca.case.path / ".dev" / "tasks" / "a b.md").exists()
-
-
-def test_a_change_made_while_the_terminals_closed_keeps_the_worktree(wc, setup_orca):
-    path = setup_orca.case.path
-
-    def busy_terminal(argv, cwd):
-        write(path / "notes-made-by-the-terminal.txt")  # an agent was still working
-        return result(wc)
-
-    setup_orca.orca_replies[("terminal", "close")] = busy_terminal
-    done = setup_orca.remove()
-    assert (done.status, done.reason) == (
-        "kept",
-        "changed since the terminals were closed",
-    )
-    assert path.exists() and not any(
-        c.argv[0] == "xargs" for c in setup_orca.runner.commands
-    )
-
-
-def test_a_saved_file_edited_after_the_save_is_never_cleared(wc, setup_orca):
-    path = setup_orca.case.path
-
-    def edits_a_saved_file(argv, cwd):
-        (path / ".dev" / "tasks" / "a b.md").write_text(
-            "newer bytes\n", encoding="utf-8"
-        )
-        return result(wc)
-
-    setup_orca.orca_replies[("terminal", "close")] = edits_a_saved_file
-    done = setup_orca.remove()
-    assert (done.status, done.reason) == (
-        "kept",
-        "changed since the terminals were closed",
-    )
-    assert (path / ".dev" / "tasks" / "a b.md").read_text() == "newer bytes\n"
-
-
-def test_a_process_still_inside_after_the_close_keeps_the_worktree(wc, setup_orca):
-    proc = make_fake_proc(setup_orca.tmp / "busy-proc", {42: str(setup_orca.case.path)})
-    done = setup_orca.remove(proc_root=str(proc))
-    assert (done.status, done.reason) == (
-        "kept",
-        "a process is still inside after its Orca terminals were closed",
-    )
-    assert not any(c.argv[0] == "xargs" for c in setup_orca.runner.commands)
-    failing = make_fake_proc(setup_orca.tmp / "bad-proc", {43: "file"})
-    done = setup_orca.remove(proc_root=str(failing))
-    assert done.status == "kept" and "process scan failed" in done.reason
-
-
-def test_a_failed_save_stops_before_anything_else(
-    wc, runner_cls, throwaway_repo, evidence_bare, tmp_path
-):
-    setup = Setup(
-        wc, runner_cls, throwaway_repo, evidence_bare, tmp_path, with_orca=True
-    )
-    (setup.case.path / ".dev" / "local" / "run.log").write_text(
-        "key " + "gh" + "p_" + "A1b2C3d4" * 4 + "\n"
-    )
-    done = setup.remove()
-    assert done.status == "failed" and done.reason.startswith(
-        "saved copy failed: possible secret in"
-    )
-    assert setup.orca_calls == [] and setup.runner.commands == []
-    assert setup.case.path.exists()
-
-
-def test_a_removal_that_git_refuses_keeps_the_worktree_with_the_refusal_text(
-    wc, runner_cls, throwaway_repo, evidence_bare, tmp_path
-):
-    setup = Setup(wc, runner_cls, throwaway_repo, evidence_bare, tmp_path)
-
-    def refuse(argv, cwd):
-        return (
-            result(
-                wc,
-                128,
-                "",
-                "fatal: contains modified or untracked files, use --force to delete it",
-            )
-            if argv[1:3] == ["worktree", "remove"]
-            else None
-        )
-
-    setup.case.runner = runner_cls(
-        evidence_dir=setup.case.clone, replies={"git": refuse}
-    )
-    done = setup.remove()
-    assert done.status == "failed"
-    assert (
-        done.reason
-        == "removal refused: fatal: contains modified or untracked files, use --force to delete it"
-    )
-    assert setup.case.path.exists()
-    assert not any("--force" in c.argv for c in setup.runner.commands)
-
-
-def test_removed_in_git_but_still_listed_in_orca_is_a_failed_row(wc, setup_orca):
-    path = setup_orca.case.path
-    setup_orca.orca_replies[("worktree", "list")] = lambda argv, cwd: result(
-        wc, 0, f'{{"worktrees": [{{"path": "{path}"}}]}}'
-    )
-    done = setup_orca.remove()
-    assert (done.status, done.reason) == (
-        "failed",
-        "removed in git but still listed in Orca",
-    )
-    assert not path.exists()  # the removal itself happened
-
-
-def test_an_orca_read_back_that_fails_is_a_failed_row_when_orca_listed_the_worktree(
-    wc, setup_orca
-):
-    setup_orca.orca_replies[("worktree", "list")] = lambda argv, cwd: result(
-        wc, 1, "", "orca down"
-    )
-    done = setup_orca.remove()
-    assert (
-        done.status == "failed"
-        and done.reason == "read back failed: orca worktree list failed"
-    )
-
-
-def test_a_squash_merged_branch_is_reported_kept_not_an_error(
-    wc, runner_cls, throwaway_repo, evidence_bare, tmp_path
-):
-    setup = Setup(wc, runner_cls, throwaway_repo, evidence_bare, tmp_path)
-    path = setup.case.path
-    write(path / "feature.txt")
-    git_in(path, "add", "feature.txt")
-    git_in(path, "commit", "-q", "-m", "feature")
-    done = setup.remove()
-    assert done.status == "removed", done.reason
-    assert done.branch == "kept (not fully merged, as after a squash merge)"
-    assert "topic" in git_in(throwaway_repo.main, "branch", "--list", "topic")
-
-
-def test_a_worktree_with_nothing_to_save_skips_the_archive_and_the_clear(
-    wc, runner_cls, throwaway_repo, evidence_bare, tmp_path
-):
-    setup = Setup(wc, runner_cls, throwaway_repo, evidence_bare, tmp_path)
-    import shutil
-
-    shutil.rmtree(
-        setup.case.path / ".dev"
-    )  # a throwaway folder: nothing under .dev remains
-    done = setup.remove()
-    assert done.status == "removed" and done.verified == ""
-    assert not any(c.argv[0] == "xargs" for c in setup.runner.commands)
-    assert not any("push" in c.argv for c in setup.runner.commands)
-    assert not Path(setup.case.clone).exists()
-
-
-def test_the_repo_folder_inside_the_worktree_is_refused(wc, setup):
-    inp, pr = setup.inputs()
-    wt = dataclasses.replace(inp.facts.worktree, repo_path=str(setup.case.path / "sub"))
-    inp = dataclasses.replace(inp, facts=dataclasses.replace(inp.facts, worktree=wt))
-    done = setup.remove(inp, pr)
-    assert done.status == "failed" and "run from outside it" in done.reason
-    assert setup.runner.commands == []
-
-
-def test_a_sibling_whose_name_starts_with_the_removed_one_is_not_still_listed(
-    wc, setup_orca
-):
-    path = str(setup_orca.case.path)
-    sibling = f'{{"worktrees": [{{"path": "{path}-fix", "worktreeId": "wid-2::{path}-fix"}}]}}'
-    setup_orca.orca_replies[("worktree", "list")] = lambda argv, cwd: result(
-        wc, 0, sibling
-    )
-    done = setup_orca.remove()
-    assert done.status == "removed", done.reason
-
-
-def test_an_unreadable_orca_list_after_a_removal_is_a_failed_read_back(wc, setup_orca):
-    setup_orca.orca_replies[("worktree", "list")] = lambda argv, cwd: result(
-        wc, 0, "<html>"
-    )
-    done = setup_orca.remove()
-    assert (done.status, done.reason) == (
-        "failed",
-        "read back failed: the orca worktree list could not be read",
-    )
-
-
-def test_a_worktree_orca_did_not_list_but_orca_still_lists_after_a_git_removal_is_failed(
-    wc, setup
-):
-    path = setup.case.path
-    body = (
-        '{"ok": true, "result": {"worktrees": '
-        f'[{{"worktreeId": "x::{path}", "path": "{path}"}}]}}}}'
-    )
-    setup.orca_replies[("worktree", "list")] = lambda argv, cwd: result(wc, 0, body)
-    done = setup.remove()
-    assert (done.status, done.reason) == (
-        "failed",
-        "removed in git but still listed in Orca",
-    )
-    assert not path.exists()
-    verbs = setup.verbs()
-    assert "worktree remove" in verbs and not any(
-        v.startswith("orca worktree rm") for v in verbs
-    )
-
-
-@pytest.mark.parametrize(
-    "answer,reason",
-    [
-        ((1, "", "orca down"), "read back failed: orca worktree list failed"),
-        (
-            (0, "<html>", ""),
-            "read back failed: the orca worktree list could not be read",
-        ),
-        (
-            (0, '{"ok": false, "error": "x"}', ""),
-            "read back failed: the orca worktree list could not be read",
-        ),
-    ],
-)
-def test_a_bad_orca_list_after_a_git_removal_is_a_failed_read_back(
-    wc, setup, answer, reason
-):
-    setup.orca_replies[("worktree", "list")] = lambda argv, cwd: result(wc, *answer)
-    done = setup.remove()
-    assert (done.status, done.reason) == ("failed", reason)
-    assert not setup.case.path.exists()
-
-
-def test_a_clean_orca_list_after_a_git_removal_is_a_pass(wc, setup):
-    setup.orca_replies[("worktree", "list")] = lambda argv, cwd: result(
-        wc, 0, '{"ok": true, "result": {"worktrees": []}}'
-    )
-    assert setup.remove().status == "removed"
-
-
-def test_orca_lists_compares_paths_and_ids_for_equality(wc):
-    body = '{"result": {"worktrees": [{"worktreeId": "w1::/x/docs-354-fix", "path": "/x/docs-354-fix"}]}}'
-    assert wc.orca_lists(body, "/x/docs-354", "w0::/x/docs-354") is False
-    assert wc.orca_lists(body, "/x/docs-354-fix", "other") is True
-    assert wc.orca_lists(body, "/elsewhere", "w1::/x/docs-354-fix") is True
-    assert (
-        wc.orca_lists(body, "/x/docs-354-fix/", "other") is True
-    )  # a trailing slash is the same folder
-    assert (
-        wc.orca_lists("[]", "/x", "w") is False
-        and wc.orca_lists("{}", "/x", "w") is False
-    )
-    assert (
-        wc.orca_lists("not json", "/x", "w") is None
-        and wc.orca_lists("", "/x", "w") is None
-    )
-    # an Orca error reply cannot be read as "not listed"
-    assert wc.orca_lists('{"ok": false}', "/x", "w") is None
-    # an empty id never matches, and a row with no id field is not a match
-    assert (
-        wc.orca_lists('{"worktrees": [{"id": "", "path": "/other"}]}', "/x", "")
-        is False
-    )
-    assert wc.orca_lists('{"worktrees": [{"path": "/other"}]}', "/x", "w") is False
-    assert wc.orca_lists('{"worktrees": [{"path": ""}]}', "", "w") is False
-    # a symlinked parent folder is still the same worktree
-    assert (
-        wc.orca_lists('{"worktrees": [{"path": "/tmp/./a/../b"}]}', "/tmp/b", "")
-        is True
-    )
-
-
-def test_the_helper_for_refusal_text_does_not_shadow_the_earlier_one(wc):
-    assert (
-        wc._first_line("") == ""
-    )  # the pull request lookup helper keeps its own behaviour
-    assert wc._refusal_text("") == "no message"
-    assert wc._refusal_text("\n  first\nsecond") == "first"
-
-
-def test_git_clean_is_refused_for_any_path_that_was_not_saved(wc, setup):
-    """The runner itself refuses a clean of an unregistered path, whatever the pipeline does."""
-    other = setup.case.path / "keep-me.txt"
-    write(other)
-    with pytest.raises(wc.RefusedCommand):
-        setup.runner.run(
-            ["xargs", "-0", "git", "clean", "-f", "-x", "--"],
-            cwd=str(setup.case.path),
-            stdin=b"keep-me.txt\0",
-        )
-    assert other.exists()
diff --git a/tests/worktree_cleanup/test_rules.py b/tests/worktree_cleanup/test_rules.py
deleted file mode 100644
index 2fc8fb4ce..000000000
--- a/tests/worktree_cleanup/test_rules.py
+++ /dev/null
@@ -1,770 +0,0 @@
-"""Task 6: the eight rules, their reasons, and the table. All facts are built by hand;
-``decide`` is pure, so no process, folder or network is touched here."""
-
-from __future__ import annotations
-
-import dataclasses
-import json
-
-import pytest
-
-NOW = 2_000_000_000.0
-DAY = 86400.0
-
-
-@pytest.fixture
-def good(wc):
-    """Facts for a worktree that passes every rule."""
-    wt = wc.GitWorktree(
-        "/w/wts/topic", "/w/main", "a" * 40, "topic", False, False, False, False, False
-    )
-    facts = wc.WorktreeFacts(
-        worktree=wt,
-        head="a" * 40,
-        origin=wc.OriginInfo("IronbellyOrg", "IronClaude"),
-        state=wc.LocalState(),
-        last_commit_ts=NOW - 20 * DAY,
-        git_file_mtime=NOW - 20 * DAY,
-        created_ts=NOW - 30 * DAY,
-        size_bytes=3 * 1024 * 1024,
-        git_dir="/w/main/.git/worktrees/topic",
-    )
-    pr = wc.PullRequest(
-        9, "MERGED", "a" * 40, "x", "2026-11-01T00:00:00Z", "t", "", (), "topic"
-    )
-    return wc.RuleInputs(
-        facts=facts,
-        now=NOW,
-        pr_lookup=wc.PrLookup(True, pr),
-        landed=wc.Landed("MERGED", "installed copy"),
-        after=wc.AfterPr("same", 0),
-        issues=wc.IssueFacts((), ()),
-        procs=wc.ProcScan(True, ()),
-    )
-
-
-def with_facts(wc, inp, **change):
-    return dataclasses.replace(inp, facts=dataclasses.replace(inp.facts, **change))
-
-
-def with_wt(wc, inp, **change):
-    wt = dataclasses.replace(inp.facts.worktree, **change)
-    return with_facts(wc, inp, worktree=wt)
-
-
-def orca(wc, **change):
-    base = dict(
-        worktree_id="w", selector="id:w", path="/w/wts/topic", branch="b", repo="r",
-        last_activity_ms=None, is_pinned=False, live_terminal_count=0, linked_pr_hint=None, comment="",
-    )  # fmt: skip
-    base.update(change)
-    return wc.OrcaWorktree(**base)
-
-
-def state(wc, **change):
-    return dataclasses.replace(wc.LocalState(), **change)
-
-
-def test_a_worktree_that_passes_everything_is_removable(wc, good):
-    d = wc.decide(good)
-    assert (d.decision, d.rule, d.reason, d.note) == ("removable", None, "", "")
-    assert d.saved_copy == "none needed"
-
-
-def test_decide_is_pure_and_repeatable(wc, good, never_run_runner):
-    assert wc.decide(good) == wc.decide(good)
-    assert wc.decide(dataclasses.replace(good, own_folder=True)) == wc.decide(
-        dataclasses.replace(good, own_folder=True)
-    )
-    assert never_run_runner.commands == []
-
-
-def case(wc, good, name):
-    """One worktree that fails only one rule: (inputs, rule number, reason)."""
-    s = lambda **c: with_facts(wc, good, state=state(wc, **c))  # noqa: E731
-    pr = lambda **c: dataclasses.replace(  # noqa: E731
-        good, pr_lookup=wc.PrLookup(True, dataclasses.replace(good.pr_lookup.pr, **c))
-    )
-    cases = {
-        "main": (with_wt(wc, good, is_main=True), 1, "main checkout"),
-        "origin-not-ours": (with_facts(wc, good, origin=wc.OriginInfo("Other", "x")), 1, "not our repo"),
-        "origin-unknown": (with_facts(wc, good, origin=None), 1, "not our repo"),
-        "own-folder": (dataclasses.replace(good, own_folder=True), 1, "this is where the script runs"),
-        "locked": (with_wt(wc, good, locked=True), 1, "locked"),
-        "missing": (with_facts(wc, good, present=False), 1, "folder missing (reported only)"),
-        "guard": (with_wt(wc, good, path="/w/wts/orca-port-x"), 1, "on the name guard (infrastructure folder)"),
-        "detached": (with_wt(wc, good, detached=True, branch=None), 1, "detached HEAD"),
-        "no-pr": (dataclasses.replace(good, pr_lookup=wc.PrLookup(True, None)), 2, "no pull request"),
-        "pr-lookup": (dataclasses.replace(good, pr_lookup=wc.PrLookup(False, None, "boom")), 2, "pull request lookup failed: boom"),
-        "pr-open": (pr(state="OPEN"), 2, "pull request #9 is open"),
-        "pr-closed": (pr(state="CLOSED"), 2, "pull request #9 closed, not merged"),
-        "landed-unknown": (dataclasses.replace(good, landed=wc.Landed("UNKNOWN", "x")), 2, "landed check said UNKNOWN"),
-        "landed-missing": (dataclasses.replace(good, landed=None), 2, "landed check said UNKNOWN"),
-        "landed-open": (dataclasses.replace(good, landed=wc.Landed("OPEN", "x")), 2, "pull request #9 is open"),
-        "after-3": (dataclasses.replace(good, after=wc.AfterPr("ahead", 3)), 3, "3 commits after the pull request"),
-        "after-1": (dataclasses.replace(good, after=wc.AfterPr("ahead", 1)), 3, "1 commit after the pull request"),
-        "after-unknown": (dataclasses.replace(good, after=wc.AfterPr("unknown", None)), 3, "HEAD is not the pull request's head"),
-        "after-missing": (dataclasses.replace(good, after=None), 3, "HEAD is not the pull request's head"),
-        "issue-open": (
-            dataclasses.replace(good, issues=wc.IssueFacts((wc.Issue("o/r", 21, "OPEN", ("x",)),), ())),
-            4, "issue #21 is open",
-        ),
-        "issue-failed": (
-            dataclasses.replace(good, issues=wc.IssueFacts((), ("issue lookup failed: o/r#4",))),
-            4, "issue lookup failed: o/r#4",
-        ),
-        "issue-missing": (dataclasses.replace(good, issues=None), 4, "issue lookup failed"),
-        "changed": (s(changed_tracked=["a", "b"]), 5, "2 changed tracked files"),
-        "untracked": (s(untracked_outside_dev=["a"]), 5, "1 untracked file outside .dev"),
-        "ignored-local": (s(ignored_unknown=[".env", "x.key"]), 5, "ignored local state: .env, x.key"),
-        "state-unread": (with_facts(wc, good, state=None), 5, "ignored local state: git status could not be read"),
-        "save-failed": (
-            dataclasses.replace(with_facts(wc, good, state=state(wc, untracked_dev=[".dev/a"])), save_state="failed: push refused"),
-            5, "saved copy failed: push refused",
-        ),
-        "save-unset": (with_facts(wc, good, state=state(wc, ignored_dev=[".dev/a"])), 5, "saved copy failed: no save state for the .dev files"),
-        "process": (
-            dataclasses.replace(good, procs=wc.ProcScan(True, ((412, "/w/wts/topic/sub", "node"),))),
-            6, "in use: process 412 (node)",
-        ),
-        "scan-failed": (dataclasses.replace(good, procs=wc.ProcScan(False, failure="pid 5: boom")), 6, None),
-        "no-scan": (dataclasses.replace(good, procs=None), 6, None),
-        "nested": (with_facts(wc, good, nested_checkouts=["inner/.git"]), 6, "holds another checkout"),
-        "operation": (with_facts(wc, good, operations=["MERGE_HEAD"]), 6, "git operation in progress"),
-        "unread-folder": (with_facts(wc, good, failures=["3 folder entries could not be read"]), 6, "in use: the folder or its git folder could not be read in full"),
-        "git-dir-unread": (with_facts(wc, good, git_dir=None), 6, "in use: the folder or its git folder could not be read in full"),
-        "missing-real": (with_facts(wc, good, present=False, origin=None, head=None, state=None, git_dir=None), 1, "folder missing (reported only)"),
-        "created-unknown": (with_facts(wc, good, created_ts=None), 7, "created time unknown (needs 7)"),
-        "idle": (with_facts(wc, good, git_file_mtime=NOW - 2 * DAY, last_commit_ts=NOW - 3 * DAY), 7, "idle 2 days (needs 7)"),
-        "idle-unknown": (with_facts(wc, good, git_file_mtime=None, last_commit_ts=None), 7, "idle time unknown (needs 7)"),
-        "young": (with_facts(wc, good, created_ts=NOW - 3 * DAY), 7, "created 3 days ago (needs 7)"),
-        "pinned": (dataclasses.replace(good, orca=orca(wc, is_pinned=True)), 8, "pinned in Orca"),
-        "keep-file": (with_facts(wc, good, keep_file=True), 8, "keep file present"),
-    }  # fmt: skip
-    return cases[name]
-
-
-CASE_NAMES = [
-    "main", "origin-not-ours", "origin-unknown", "own-folder", "locked", "missing", "guard", "detached",
-    "no-pr", "pr-lookup", "pr-open", "pr-closed", "landed-unknown", "landed-missing", "landed-open",
-    "after-3", "after-1", "after-unknown", "after-missing", "issue-open", "issue-failed", "issue-missing",
-    "changed", "untracked", "ignored-local", "state-unread", "save-failed", "save-unset",
-    "process", "scan-failed", "no-scan", "nested", "operation", "unread-folder", "git-dir-unread",
-    "missing-real", "created-unknown",
-    "idle", "idle-unknown", "young", "pinned", "keep-file",
-]  # fmt: skip
-
-
-@pytest.mark.parametrize("name", CASE_NAMES)
-def test_failing_only_one_rule_keeps_the_worktree_with_that_reason(wc, good, name):
-    inp, rule, reason = case(wc, good, name)
-    d = wc.decide(inp)
-    assert d.decision == "kept" and d.rule == rule
-    if reason is not None:
-        assert d.reason == reason
-    else:
-        assert d.reason.startswith("in use: the process scan failed")
-
-
-def test_the_first_failed_rule_is_the_one_shown(wc, good):
-    inp = dataclasses.replace(
-        with_facts(wc, good, keep_file=True, state=state(wc, changed_tracked=["a"])),
-        pr_lookup=wc.PrLookup(True, None),
-        own_folder=True,
-    )
-    d = wc.decide(inp)
-    assert (d.rule, d.reason) == (1, "this is where the script runs")
-    inp = dataclasses.replace(inp, own_folder=False)
-    assert wc.decide(inp).rule == 2
-    inp = dataclasses.replace(inp, pr_lookup=good.pr_lookup)
-    assert wc.decide(inp).rule == 5
-
-
-def test_reasons_are_the_strings_of_the_spec(wc):
-    """Every reason the spec table names for rules 1 to 8 appears in the rule code."""
-    import inspect
-
-    text = (
-        inspect.getsource(wc._rule1)
-        + inspect.getsource(wc._rule2)
-        + inspect.getsource(wc._rule3)
-    )
-    for words in ("main checkout", "not our repo", "this is where the script runs", "locked",
-                  "folder missing (reported only)", "detached HEAD", "no pull request", "is open",
-                  "closed, not merged", "landed check said UNKNOWN", "after the pull request",
-                  "HEAD is not the pull request's head"):  # fmt: skip
-        assert words in text, words
-    text = (
-        inspect.getsource(wc._rule4)
-        + inspect.getsource(wc._rule5)
-        + inspect.getsource(wc._rule6)
-        + inspect.getsource(wc._rule7)
-        + inspect.getsource(wc._rule8)
-    )
-    for words in ("is open", "issue lookup failed", "changed tracked file", "untracked file", "outside .dev",
-                  "ignored local state:", "saved copy failed:", "in use: process", "holds another checkout",
-                  "git operation in progress", "(needs", "pinned in Orca", "keep file present"):  # fmt: skip
-        assert words in text, words
-
-
-# -- rule 6: terminals, the save state, the dry run -------------------------------------------------
-
-
-def test_a_process_inside_with_orca_terminals_open_passes_rule_6_with_the_note(
-    wc, good
-):
-    inside = wc.ProcScan(True, ((7, "/w/wts/topic", "claude"),))
-    inp = dataclasses.replace(good, procs=inside, orca=orca(wc, live_terminal_count=2))
-    d = wc.decide(inp)
-    assert (
-        d.decision == "removable"
-        and d.note == "its Orca terminals will be closed first"
-    )
-    # the same process without an Orca terminal fails rule 6
-    d = wc.decide(
-        dataclasses.replace(good, procs=inside, orca=orca(wc, live_terminal_count=0))
-    )
-    assert (d.decision, d.rule, d.reason) == ("kept", 6, "in use: process 7 (claude)")
-    d = wc.decide(dataclasses.replace(good, procs=inside, orca=None))
-    assert (d.rule, d.reason) == (6, "in use: process 7 (claude)")
-    # terminals but no process: still the note
-    d = wc.decide(dataclasses.replace(good, orca=orca(wc, live_terminal_count=1)))
-    assert d.decision == "removable" and d.note == wc.TERMINALS_NOTE
-    # terminals do not excuse another checkout or an operation, or a failed scan
-    busy = with_facts(wc, good, operations=["index.lock"])
-    assert (
-        wc.decide(
-            dataclasses.replace(
-                busy, procs=inside, orca=orca(wc, live_terminal_count=2)
-            )
-        ).rule
-        == 6
-    )
-    failed = wc.ProcScan(False, failure="x")
-    assert (
-        wc.decide(
-            dataclasses.replace(
-                good, procs=failed, orca=orca(wc, live_terminal_count=2)
-            )
-        ).rule
-        == 6
-    )
-
-
-def test_a_process_in_a_sibling_folder_is_not_inside(wc, good):
-    near = wc.ProcScan(True, ((7, "/w/wts/topic-2", "x"),))
-    assert wc.decide(dataclasses.replace(good, procs=near)).decision == "removable"
-
-
-@pytest.mark.parametrize(
-    "files,save,decision,cell",
-    [
-        ({}, "not needed", "removable", "none needed"),
-        ({"untracked_dev": [".dev/a"]}, "needed", "removable", "needed"),
-        ({"ignored_dev": [".dev/a"]}, "verified", "removable", "saved and checked"),
-        ({"untracked_dev": [".dev/a"]}, "failed: copy differs", "kept", "failed"),
-    ],
-)
-def test_dev_files_need_a_verified_save_and_the_dry_run_shows_needed(
-    wc, good, files, save, decision, cell
-):
-    inp = dataclasses.replace(
-        with_facts(wc, good, state=state(wc, **files)), save_state=save
-    )
-    d = wc.decide(inp)
-    assert (d.decision, d.saved_copy) == (decision, cell)
-
-
-def test_a_failed_rule_before_the_save_still_shows_the_saved_copy_cell(wc, good):
-    inp = dataclasses.replace(
-        with_facts(wc, good, state=state(wc, untracked_dev=[".dev/a"])),
-        pr_lookup=wc.PrLookup(True, None),
-        save_state="needed",
-    )
-    d = wc.decide(inp)
-    assert d.rule == 2 and d.saved_copy == "needed"
-
-
-# -- the table -----------------------------------------------------------------------------------------
-
-
-def make_rows(wc, good):
-    inp_a = dataclasses.replace(good, orca=orca(wc, live_terminal_count=1))
-    inp_b = dataclasses.replace(good, own_folder=True)
-    rows = [wc.table_row(i, wc.decide(i), "IronClaude") for i in (inp_a, inp_b)]
-    return rows
-
-
-def test_the_markdown_table_has_the_eleven_columns_and_the_json_the_same_rows(wc, good):
-    rows = make_rows(wc, good)
-    assert len(wc.TABLE_COLUMNS) == 11
-    md = wc.render_markdown(rows).splitlines()
-    assert (
-        md[0]
-        == "| repo | folder | branch | in orca | pull request | issues | idle days | size | saved copy | decision | reason |"
-    )
-    assert md[1] == "|" + "|".join(["---"] * 11) + "|"
-    assert len(md) == 2 + len(rows)
-    for line, row in zip(md[2:], rows):
-        assert line.count(" | ") == 10
-        assert row["decision"] in line and row["folder"] in line
-    doc = json.loads(wc.render_json(rows))
-    assert doc["columns"] == list(wc.TABLE_COLUMNS)
-    assert doc["rows"] == rows
-    assert all(set(r) == set(wc.TABLE_COLUMNS) for r in doc["rows"])
-
-
-def test_row_cells_for_a_removable_and_a_kept_worktree(wc, good):
-    a, b = make_rows(wc, good)
-    assert a == {
-        "repo": "IronClaude", "folder": "topic", "branch": "topic", "in_orca": "yes",
-        "pull_request": "#9 MERGED", "issues": "none found", "idle_days": "20.0", "size": "3.0 MB",
-        "saved_copy": "none needed", "decision": "removable", "reason": "its Orca terminals will be closed first",
-    }  # fmt: skip
-    assert (
-        b["decision"] == "kept"
-        and b["reason"] == "this is where the script runs"
-        and b["in_orca"] == "no"
-    )
-
-
-def test_row_cells_for_failed_lookups_and_unknowns(wc, good):
-    inp = dataclasses.replace(
-        with_facts(
-            wc,
-            good,
-            size_bytes=None,
-            git_file_mtime=None,
-            last_commit_ts=None,
-            worktree=dataclasses.replace(
-                good.facts.worktree, detached=True, branch=None
-            ),
-        ),
-        pr_lookup=wc.PrLookup(False, None, "x"),
-        issues=wc.IssueFacts(
-            (wc.Issue("o/r", 4, "CLOSED", ()),), ("issue lookup failed: o/r#5",)
-        ),
-    )
-    row = wc.table_row(inp, wc.decide(inp))
-    assert (
-        row["pull_request"],
-        row["issues"],
-        row["idle_days"],
-        row["size"],
-        row["branch"],
-    ) == (
-        "lookup failed",
-        "#4 CLOSED, lookup failed",
-        "?",
-        "?",
-        "(detached)",
-    )
-    assert row["repo"] == "main"
-    none = dataclasses.replace(inp, pr_lookup=wc.PrLookup(True, None), issues=None)
-    assert wc.table_row(none, wc.decide(none))["issues"] == "lookup failed"
-    assert wc.table_row(none, wc.decide(none))["pull_request"] == "none"
-
-
-def test_markdown_cells_never_break_the_table(wc, good):
-    row = dict(make_rows(wc, good)[0], reason="a | b\nc")
-    line = wc.render_markdown([row]).splitlines()[2]
-    assert line.count("|") == 12 and "\n" not in line.strip()
-    assert wc.render_markdown([]).count("\n") == 2
-
-
-@pytest.mark.parametrize(
-    "size,text",
-    [
-        (None, "?"),
-        (0, "0 B"),
-        (1023, "1023 B"),
-        (1536, "1.5 KB"),
-        (5 * 1024**3, "5.0 GB"),
-        (3000 * 1024**3, "3000.0 GB"),
-    ],
-)
-def test_size_text(wc, size, text):
-    assert wc._size_text(size) == text
-
-
-# --- Task 8: the removal and keep cases, on real throwaway facts ---------------------------------
-#
-# Each case below builds the facts from a real throwaway worktree (or from fake gh replies for
-# the issue places) and changes one thing; the reason text is asserted, not only the decision.
-
-from .conftest import git_in  # noqa: E402
-from .test_facts import facts_for, gh_fake, issue_reply, write  # noqa: E402
-
-SLUG = "IronbellyOrg/IronClaude"
-NOT_FOUND = (
-    1,
-    "",
-    "GraphQL: Could not resolve to an issue or pull request with the number",
-)
-OLD = {
-    "git_file_mtime": NOW - 20 * DAY,
-    "last_commit_ts": NOW - 20 * DAY,
-    "created_ts": NOW - 30 * DAY,
-}
-
-
-def real_inputs(wc, runner_cls, repo, name, good, mutate=None, **change):
-    """Inputs whose local facts come from a real throwaway worktree made old enough to pass rule 7."""
-    path = repo.add_worktree(name)
-    if mutate:
-        mutate(path)
-    _, facts = facts_for(wc, runner_cls, repo, path)
-    facts = dataclasses.replace(
-        facts, origin=wc.OriginInfo("IronbellyOrg", "IronClaude"), **OLD
-    )
-    facts = dataclasses.replace(facts, **change)
-    return dataclasses.replace(good, facts=facts, after=wc.AfterPr("same", 0))
-
-
-def test_removable_case_merged_clean_idle_8_days_no_process_no_terminal_issue_closed(
-    wc, runner_cls, throwaway_repo, good
-):
-    inp = real_inputs(
-        wc,
-        runner_cls,
-        throwaway_repo,
-        "removable",
-        good,
-        git_file_mtime=NOW - 8 * DAY,
-        last_commit_ts=NOW - 8 * DAY,
-    )
-    inp = dataclasses.replace(
-        inp,
-        issues=wc.IssueFacts(
-            (wc.Issue("o/r", 5, "CLOSED", ("closing reference",)),), ()
-        ),
-    )
-    d = wc.decide(inp)
-    assert (d.decision, d.reason, d.note) == ("removable", "", "")
-    row = wc.table_row(inp, d, "IronClaude")
-    assert row["issues"] == "#5 CLOSED" and row["idle_days"] == "8.0"
-
-
-@pytest.mark.parametrize(
-    "name",
-    ["orca-port-evidence", "orca-recipe-x", "orca-pristine-y", "orca-old-patched"],
-)
-def test_the_name_guard_keeps_infrastructure_folders(
-    wc, runner_cls, throwaway_repo, good, name
-):
-    d = wc.decide(real_inputs(wc, runner_cls, throwaway_repo, name, good))
-    assert (d.decision, d.rule, d.reason) == (
-        "kept",
-        1,
-        "on the name guard (infrastructure folder)",
-    )
-
-
-def test_coder_orca_port_is_not_caught_by_the_name_guard(
-    wc, runner_cls, throwaway_repo, good
-):
-    assert (
-        wc.decide(
-            real_inputs(wc, runner_cls, throwaway_repo, "coder-orca-port", good)
-        ).decision
-        == "removable"
-    )
-
-
-def test_a_real_main_checkout_is_kept(wc, runner_cls, throwaway_repo, good):
-    _, facts = facts_for(wc, runner_cls, throwaway_repo, throwaway_repo.main)
-    facts = dataclasses.replace(facts, origin=wc.OriginInfo("IronbellyOrg", "x"), **OLD)
-    d = wc.decide(dataclasses.replace(good, facts=facts))
-    assert (d.rule, d.reason) == (1, "main checkout")
-
-
-def test_a_real_detached_head_and_a_real_locked_worktree_are_kept(
-    wc, runner_cls, throwaway_repo, good
-):
-    wts = throwaway_repo.add_standard_worktrees()
-    for name, reason in (("detached", "detached HEAD"), ("locked", "locked")):
-        _, facts = facts_for(wc, runner_cls, throwaway_repo, wts[name])
-        facts = dataclasses.replace(
-            facts, origin=wc.OriginInfo("IronbellyOrg", "x"), **OLD
-        )
-        d = wc.decide(dataclasses.replace(good, facts=facts))
-        assert (d.rule, d.reason) == (1, reason), name
-
-
-def test_a_folder_that_is_gone_is_reported_and_never_pruned(
-    wc, runner_cls, throwaway_repo, good
-):
-    import shutil
-
-    path = throwaway_repo.add_worktree("vanished")
-    shutil.rmtree(path)
-    _, facts = facts_for(wc, runner_cls, throwaway_repo, path)
-    d = wc.decide(dataclasses.replace(good, facts=facts))
-    assert (d.decision, d.rule, d.reason) == (
-        "kept",
-        1,
-        "folder missing (reported only)",
-    )
-
-
-def test_idle_six_days_and_created_three_days_ago(wc, runner_cls, throwaway_repo, good):
-    six = real_inputs(
-        wc,
-        runner_cls,
-        throwaway_repo,
-        "six",
-        good,
-        git_file_mtime=NOW - 6 * DAY,
-        last_commit_ts=NOW - 6 * DAY,
-    )
-    assert (wc.decide(six).rule, wc.decide(six).reason) == (7, "idle 6 days (needs 7)")
-    young = real_inputs(
-        wc, runner_cls, throwaway_repo, "young", good, created_ts=NOW - 3 * DAY
-    )
-    assert (wc.decide(young).rule, wc.decide(young).reason) == (
-        7,
-        "created 3 days ago (needs 7)",
-    )
-    custom = dataclasses.replace(six, idle_floor_days=5)
-    assert wc.decide(custom).decision == "removable"
-
-
-# -- rule 5, on real local state ------------------------------------------------------------------
-
-
-@pytest.mark.parametrize(
-    "mutate,reason",
-    [
-        (lambda p: write(p / "README.md", "edited\n"), "1 changed tracked file"),
-        (lambda p: write(p / "loose.txt"), "1 untracked file outside .dev"),
-        (
-            lambda p: write(p / ".env", "NAME=placeholder\n"),
-            "ignored local state: .env",
-        ),
-    ],
-    ids=["tracked-edit", "untracked-outside-dev", "ignored-env-file"],
-)
-def test_unsaved_local_state_keeps_the_worktree_with_its_reason(
-    wc, runner_cls, throwaway_repo, good, mutate, reason
-):
-    inp = real_inputs(wc, runner_cls, throwaway_repo, "dirty", good, mutate=mutate)
-    d = wc.decide(inp)
-    assert (d.decision, d.rule, d.reason) == ("kept", 5, reason)
-
-
-def test_an_unknown_ignored_name_is_local_state(wc, runner_cls, throwaway_repo, good):
-    def mutate(path):
-        write(path / ".venv" / "lib" / "x.py")  # build output, allowed
-        write(path / ".env", "NAME=placeholder\n")  # unknown, keeps it
-
-    d = wc.decide(
-        real_inputs(wc, runner_cls, throwaway_repo, "unknown", good, mutate=mutate)
-    )
-    assert d.reason == "ignored local state: .env"
-
-
-def test_ignored_build_output_and_generated_copies_are_not_a_reason_to_keep(
-    wc, runner_cls, throwaway_repo, good
-):
-    names = [
-        "pkg/__pycache__/m.pyc", ".venv/lib/x.py", ".codegraph/db", ".ruff_cache/c", ".pytest_cache/c",
-        ".mypy_cache/c", "node_modules/p/i.js", "dist/a.whl", "build/b.o", "uv.lock",
-        ".serena/cache/c.json", ".claude/agents/a.md", ".claude/commands/c.md",
-        ".claude/hooks/h.sh", ".claude/skills/s.md", ".claude/templates/t.md",
-    ]  # fmt: skip
-
-    def mutate(path):
-        exclude = path.parent.parent / "main" / ".git" / "info" / "exclude"
-        with exclude.open("a", encoding="utf-8") as handle:
-            handle.write(
-                ".codegraph/\n.ruff_cache/\n.pytest_cache/\n.mypy_cache/\nbuild/\nuv.lock\n"
-            )
-            handle.write(
-                ".claude/commands/\n.claude/hooks/\n.claude/skills/\n.claude/templates/\n"
-            )
-        for rel in names:
-            write(path / rel)
-
-    inp = real_inputs(wc, runner_cls, throwaway_repo, "buildout", good, mutate=mutate)
-    assert inp.facts.state.ignored_unknown == [], inp.facts.state.ignored_unknown
-    assert len(inp.facts.state.ignored_build) + len(
-        inp.facts.state.ignored_generated
-    ) == len(names)
-    assert wc.decide(inp).decision == "removable"
-
-
-# -- rule 6, on real git operations and a fake process table ---------------------------------------
-
-
-@pytest.mark.parametrize(
-    "marker",
-    [
-        "MERGE_HEAD",
-        "CHERRY_PICK_HEAD",
-        "REVERT_HEAD",
-        "rebase-merge",
-        "rebase-apply",
-        "BISECT_LOG",
-        "index.lock",
-    ],
-)
-def test_a_git_operation_in_progress_keeps_the_worktree(
-    wc, runner_cls, throwaway_repo, good, marker
-):
-    from pathlib import Path
-
-    path = throwaway_repo.add_worktree("busy")
-    _, probe = facts_for(wc, runner_cls, throwaway_repo, path)
-    target = Path(probe.git_dir) / marker
-    if marker.startswith("rebase"):
-        target.mkdir()
-    else:
-        write(target, "0" * 40 + "\n")
-    clean = real_inputs(
-        wc, runner_cls, throwaway_repo, "busy-clean", good
-    )  # a clean sibling passes
-    assert wc.decide(clean).decision == "removable"
-    _, facts = facts_for(wc, runner_cls, throwaway_repo, path)
-    facts = dataclasses.replace(facts, origin=wc.OriginInfo("IronbellyOrg", "x"), **OLD)
-    d = wc.decide(dataclasses.replace(good, facts=facts))
-    assert (d.decision, d.rule, d.reason) == ("kept", 6, "git operation in progress")
-
-
-def test_a_real_fake_proc_process_inside_and_a_failing_scan(
-    wc, runner_cls, throwaway_repo, good, tmp_path
-):
-    from .conftest import make_fake_proc
-
-    inp = real_inputs(wc, runner_cls, throwaway_repo, "watched", good)
-    wt = inp.facts.worktree.path
-    inside = wc.scan_processes(str(make_fake_proc(tmp_path / "p1", {77: wt})))
-    d = wc.decide(dataclasses.replace(inp, procs=inside))
-    assert (d.rule, d.reason) == (6, "in use: process 77 (proc77)")
-    bad = wc.scan_processes(str(make_fake_proc(tmp_path / "p2", {78: "file"})))
-    d = wc.decide(dataclasses.replace(inp, procs=bad))
-    assert d.decision == "kept" and d.rule == 6 and "scan failed" in d.reason
-    # every worktree is kept while the scan fails
-    other = real_inputs(wc, runner_cls, throwaway_repo, "other", good)
-    assert wc.decide(dataclasses.replace(other, procs=bad)).rule == 6
-
-
-# -- rules 2 and 3: squash merge and a reused branch -----------------------------------------------------
-
-
-def test_a_squash_merged_pull_request_is_judged_landed_from_its_state(
-    wc, runner_cls, throwaway_repo, good
-):
-    path = throwaway_repo.add_worktree("squashed")
-    write(path / "feature.txt")
-    git_in(path, "add", "feature.txt")
-    git_in(path, "commit", "-q", "-m", "feature")
-    head = git_in(path, "rev-parse", "HEAD").strip()
-    on_base = git_in(throwaway_repo.main, "branch", "--contains", head).split()
-    assert "main" not in on_base  # the commits are not on the base
-    pr = dataclasses.replace(good.pr_lookup.pr, head_oid=head)
-    runner = runner_cls()
-    after = wc.commits_after_pr(runner, str(path), head, head)
-    facts = dataclasses.replace(
-        facts_for(wc, runner_cls, throwaway_repo, path)[1],
-        origin=wc.OriginInfo("IronbellyOrg", "x"),
-        **OLD,
-    )
-    decided = wc.decide(
-        dataclasses.replace(
-            good, facts=facts, pr_lookup=wc.PrLookup(True, pr), after=after
-        )
-    )
-    assert decided.decision == "removable"
-    assert runner.commands == []  # same commit: no ancestry question was asked
-
-
-def test_a_merged_pull_request_whose_branch_was_reused_keeps_the_worktree(
-    wc, runner_cls, throwaway_repo, good
-):
-    path = throwaway_repo.add_worktree("reused")
-    pr_head = git_in(path, "rev-parse", "HEAD").strip()
-    write(path / "later.txt")
-    git_in(path, "add", "later.txt")
-    git_in(path, "commit", "-q", "-m", "new work on the old branch")
-    head = git_in(path, "rev-parse", "HEAD").strip()
-    after = wc.commits_after_pr(runner_cls(), str(path), head, pr_head)
-    facts = dataclasses.replace(
-        facts_for(wc, runner_cls, throwaway_repo, path)[1],
-        origin=wc.OriginInfo("IronbellyOrg", "x"),
-        **OLD,
-    )
-    d = wc.decide(dataclasses.replace(good, facts=facts, after=after))
-    assert (d.decision, d.rule, d.reason) == (
-        "kept",
-        3,
-        "1 commit after the pull request",
-    )
-
-
-# -- rule 4, an open issue through each of the four places -------------------------------------------------
-
-
-def test_an_open_issue_keeps_the_worktree_through_each_of_the_four_places(
-    wc, runner_cls, good
-):
-    def decided(pr, branch, orca_row, table):
-        runner = runner_cls(replies={"gh": gh_fake(wc, table)})
-        found = wc.collect_issues(runner, SLUG, pr, branch, "/w/wts/plain", orca_row)
-        return wc.decide(dataclasses.replace(good, issues=found))
-
-    base = good.pr_lookup.pr
-
-    def open_issue(n):
-        return {
-            ("pr", "view", str(n), SLUG): NOT_FOUND,
-            ("issue", "view", str(n), SLUG): issue_reply("OPEN"),
-        }
-
-    # 1. closing reference
-    pr = dataclasses.replace(base, closing=(wc.IssueRef(None, 31),))
-    d = decided(pr, "topic", None, {("issue", "view", "31", SLUG): issue_reply("OPEN")})
-    assert (d.rule, d.reason) == (4, "issue #31 is open")
-    # 2. a #N in the pull request body
-    pr = dataclasses.replace(base, body="Fixes #32.")
-    assert decided(pr, "topic", None, open_issue(32)).reason == "issue #32 is open"
-    # 3. a number in the branch name
-    assert (
-        decided(base, "docs-333-topic", None, open_issue(333)).reason
-        == "issue #333 is open"
-    )
-    # 4. Orca's card comment
-    card = dataclasses.replace(
-        wc.parse_orca_worktrees(
-            (
-                __import__("pathlib").Path(__file__).parent
-                / "fixtures"
-                / "orca_worktree_ps.json"
-            ).read_text()
-        ).items[0],
-        comment="sc:issue IronbellyOrg/IronClaude#34",
-    )
-    assert decided(base, "topic", card, open_issue(34)).reason == "issue #34 is open"
-    # a closed issue in the same place does not keep it
-    closed = {
-        ("pr", "view", "34", SLUG): NOT_FOUND,
-        ("issue", "view", "34", SLUG): issue_reply("CLOSED"),
-    }
-    assert decided(base, "topic", card, closed).decision == "removable"
-
-
-def test_an_issue_lookup_that_fails_keeps_the_worktree(wc, runner_cls, good):
-    runner = runner_cls(
-        replies={"gh": gh_fake(wc, {("pr", "view", "44", SLUG): NOT_FOUND})}
-    )
-    pr = dataclasses.replace(good.pr_lookup.pr, body="see #44")
-    found = wc.collect_issues(runner, SLUG, pr, "topic", "/w/wts/plain")
-    d = wc.decide(dataclasses.replace(good, issues=found))
-    assert (d.rule, d.reason) == (4, f"issue lookup failed: {SLUG}#44")
-
-
-def test_rule_4_none_found_passes_and_the_table_says_so(wc, runner_cls, good):
-    runner = runner_cls(replies={"gh": gh_fake(wc, {})})
-    found = wc.collect_issues(runner, SLUG, None, "topic", "/w/wts/plain")
-    inp = dataclasses.replace(good, issues=found)
-    assert wc.decide(inp).decision == "removable"
-    assert wc.table_row(inp, wc.decide(inp))["issues"] == "none found"
diff --git a/tests/worktree_cleanup/test_runner.py b/tests/worktree_cleanup/test_runner.py
deleted file mode 100644
index a5183ecd0..000000000
--- a/tests/worktree_cleanup/test_runner.py
+++ /dev/null
@@ -1,642 +0,0 @@
-"""Task 2: the allowlisted command runner, the command line and the file header.
-
-Each refusal below must fail if its rule is removed from ``Runner.check_allowed``. The
-runner is a positive allowlist (every command must match one exact argument shape), so
-the refusals include bundled and shortened spellings of the banned options.
-"""
-
-from __future__ import annotations
-
-import ast
-import subprocess
-import sys
-
-import pytest
-
-from .conftest import LANDED, SCRIPT
-
-REPO = "IronbellyOrg/IronClaude"
-HELPER = "credential.helper=!gh auth git-credential"
-
-
-def _source() -> str:
-    return SCRIPT.read_text(encoding="utf-8")
-
-
-# --- command line -----------------------------------------------------------
-
-
-def test_help_lists_the_four_verbs_and_the_two_flags():
-    proc = subprocess.run(
-        [sys.executable, str(SCRIPT), "--help"],
-        capture_output=True,
-        text=True,
-        check=False,
-    )
-    assert proc.returncode == 0
-    for word in ("list", "archive", "retire", "prune", "--apply", "--out"):
-        assert word in proc.stdout
-
-
-def test_main_accepts_an_injected_runner_and_exits_usage_for_a_stub(wc, runner_cls):
-    runner = runner_cls()
-    assert wc.main(["list"], runner=runner, env={}) == wc.EXIT_USAGE
-    assert runner.commands == []
-
-
-def test_settings_defaults_and_idle_floor(wc):
-    cfg = wc.settings({})
-    assert cfg["idle_days"] == 7
-    assert cfg["evidence_repo"] == "IronbellyOrg/run-evidence"
-    assert wc.settings({"WORKTREE_CLEANUP_IDLE_DAYS": "3"})["idle_days"] == 3
-    assert wc.settings({"WORKTREE_CLEANUP_IDLE_DAYS": "x"})["idle_days"] == 7
-
-
-# --- refusals that need no working folder ---------------------------------------
-
-BANNED = [
-    # --force or -f on the removals, in every spelling and position
-    ["git", "worktree", "remove", "--force", "/x"],
-    ["git", "worktree", "remove", "-f", "/x"],
-    ["git", "worktree", "remove", "-f", "-f", "/x"],
-    ["git", "worktree", "remove", "--forc", "/x"],
-    ["git", "worktree", "remove", "-fd", "/x"],
-    ["git", "worktree", "remove", "/x", "--force"],
-    ["orca", "worktree", "rm", "--worktree", "id:1", "--force"],
-    ["orca", "worktree", "rm", "--worktree", "id:1", "-f"],
-    ["orca", "worktree", "rm", "-f", "--worktree", "id:1"],
-    ["orca", "worktree", "rm", "--force", "--worktree", "id:1"],
-    ["orca", "worktree", "rm", "--worktree", "id:1", "--forc"],
-    ["orca", "worktree", "rm", "--worktree", "id:1", "-fy"],
-    ["orca", "worktree", "rm", "--worktree", "id:1", "--force=true"],
-    ["orca", "worktree", "rm", "--worktree", "--force"],
-    # git branch -D in every spelling, and the list form that used to return early
-    ["git", "branch", "-D", "topic"],
-    ["git", "branch", "-Dq", "topic"],
-    ["git", "branch", "-df", "topic"],
-    ["git", "branch", "-d", "-f", "topic"],
-    ["git", "branch", "--delete", "--force", "topic"],
-    ["git", "branch", "--del", "topic"],
-    ["git", "branch", "--list", "-D", "x"],
-    ["git", "branch", "-d", "topic", "other"],
-    # rm, prune and clean
-    ["rm", "-rf", "/x"],
-    ["rm", "file"],
-    ["/bin/rm", "file"],
-    ["git", "worktree", "prune"],
-    ["git", "worktree", "prune", "--dry-run"],
-    ["git", "clean", "-fdx"],
-    ["git", "clean", "-fx"],
-    ["git", "clean", "-f", "-x", "--", "a"],
-    # an option that writes a file from a read verb, also shortened
-    ["git", "log", "--output=/tmp/x"],
-    ["git", "log", "--outp=/tmp/x"],
-    ["git", "diff", "--output=/tmp/x"],
-    ["git", "diff", "--ext-diff"],
-    ["git", "status", "-zu"],
-    ["git", "log", "-n1"],
-    # git options that change its behaviour
-    ["git", "-c", "core.sshCommand=x", "status"],
-    ["git", "-c", HELPER, "status"],
-    ["git", "--git-dir=/x", "status"],
-    ["git", "-C"],
-    ["git"],
-]
-
-
-@pytest.mark.parametrize("argv", BANNED, ids=[" ".join(a) for a in BANNED])
-def test_banned_shapes_are_refused_before_any_process_starts(
-    wc, never_run_runner, argv
-):
-    with pytest.raises(wc.RefusedCommand):
-        never_run_runner.check_allowed(argv)
-    with pytest.raises(wc.RefusedCommand):
-        never_run_runner.run(argv)
-    assert never_run_runner.commands == []
-
-
-UNLISTED = [
-    ["git", "reset", "--hard"],
-    ["git", "reset"],
-    ["git", "checkout", "topic"],
-    ["git", "stash"],
-    ["git", "merge", "topic"],
-    ["git", "show", "HEAD"],
-    ["mv", "a", "b"],
-    ["find", ".", "-delete"],
-    ["gh", "pr", "merge", "1", "--repo", REPO],
-    ["gh", "pr", "create", "--repo", REPO],
-    ["gh", "api", "repos/o/r"],
-    ["orca", "automations", "create"],
-    ["orca", "worktree", "create", "--name", "x"],
-    ["python3", "-c", "print(1)"],
-]
-
-
-@pytest.mark.parametrize("argv", UNLISTED, ids=[" ".join(a) for a in UNLISTED])
-def test_unlisted_commands_are_refused(wc, never_run_runner, argv):
-    with pytest.raises(wc.RefusedCommand):
-        never_run_runner.check_allowed(argv)
-    with pytest.raises(wc.RefusedCommand):
-        never_run_runner.run(argv)
-    assert never_run_runner.commands == []
-
-
-# --- the push to the evidence repo ----------------------------------------------
-
-
-@pytest.fixture
-def evidence(tmp_path):
-    path = tmp_path / "evidence"
-    path.mkdir()
-    return path
-
-
-PUSH_REFUSED = [
-    ["push", "--delete", "origin", "topic"],
-    ["push", "-d", "origin", "topic"],
-    ["push", "-df", "origin", "topic"],
-    ["push", "-fd", "origin", "topic"],
-    ["push", "--dele", "origin", "topic"],
-    ["push", "--del", "origin", "topic"],
-    ["push", "--force", "origin", "main"],
-    ["push", "--forc", "origin", "main"],
-    ["push", "-f", "origin", "main"],
-    ["push", "--force-with-lease", "origin", "main"],
-    ["push", "--force-if-includes", "origin", "main"],
-    ["push", "--mirror", "origin"],
-    ["push", "--prune", "origin", "main"],
-    ["push", "--all", "origin"],
-    ["push", "-o", "x", "origin", "main"],
-    ["push", "origin", "+main"],
-    ["push", "origin", "main:main"],
-    ["push", "origin", ":topic"],
-    ["push", "origin", "+main:main"],
-    ["push", "origin", "HEAD:refs/heads/x"],
-    ["push", "origin", "refs/heads/*"],
-    ["push", "upstream", "main"],
-    ["push", "https://example.invalid/r.git", "main"],
-    ["push", "origin"],
-    ["push", "origin", "main", "other"],
-    ["push"],
-]
-
-
-@pytest.mark.parametrize("tail", PUSH_REFUSED, ids=[" ".join(t) for t in PUSH_REFUSED])
-def test_push_shapes_are_refused_inside_the_evidence_clone(
-    wc, runner_cls, evidence, tail
-):
-    runner = runner_cls(evidence_dir=str(evidence))
-    with pytest.raises(wc.RefusedCommand):
-        runner.run(["git", *tail], cwd=str(evidence))
-    with pytest.raises(wc.RefusedCommand):
-        runner.run(["git", "-c", HELPER, *tail], cwd=str(evidence))
-    assert runner.commands == []
-
-
-def test_push_is_allowed_only_in_its_exact_shape_inside_the_evidence_clone(
-    wc, runner_cls, evidence, tmp_path
-):
-    other = tmp_path / "other"
-    other.mkdir()
-    r = runner_cls(evidence_dir=str(evidence))
-    r.check_allowed(["git", "push", "origin", "main"], cwd=str(evidence))
-    r.check_allowed(
-        ["git", "push", "--porcelain", "origin", "topic/a-1"], cwd=str(evidence)
-    )
-    r.check_allowed(["git", "-c", HELPER, "push", "origin", "main"], cwd=str(evidence))
-    r.check_allowed(["git", "-C", str(evidence), "push", "origin", "main"])
-    # not the evidence clone, or no working folder at all
-    with pytest.raises(wc.RefusedCommand):
-        r.check_allowed(["git", "push", "origin", "main"], cwd=str(other))
-    with pytest.raises(wc.RefusedCommand):
-        r.check_allowed(["git", "push", "origin", "main"])
-    with pytest.raises(wc.RefusedCommand):
-        r.check_allowed(
-            ["git", "-C", str(other), "push", "origin", "main"], cwd=str(evidence)
-        )
-    # the credential helper is the only -c value, and only on a push
-    with pytest.raises(wc.RefusedCommand):
-        r.check_allowed(
-            ["git", "-c", "core.sshCommand=x", "push", "origin", "main"],
-            cwd=str(evidence),
-        )
-    with pytest.raises(wc.RefusedCommand):
-        r.check_allowed(["git", "-c", HELPER, "fetch", "origin"], cwd=str(evidence))
-
-
-def test_other_evidence_clone_verbs_have_one_exact_shape(
-    wc, runner_cls, evidence, tmp_path
-):
-    other = tmp_path / "other"
-    other.mkdir()
-    r = runner_cls(evidence_dir=str(evidence))
-    ok = [
-        ["git", "fetch", "origin"],
-        ["git", "fetch", "--quiet", "origin"],
-        ["git", "add", "--", "worktree-a/manifest.md", "worktree-a/part-01"],
-        ["git", "commit", "-m", "save worktree-a"],
-        ["git", "commit", "--quiet", "-m", "save worktree-a"],
-        ["git", "rebase", "origin/main"],
-        ["git", "rebase", "--abort"],
-    ]
-    for argv in ok:
-        r.check_allowed(argv, cwd=str(evidence))
-        with pytest.raises(wc.RefusedCommand):
-            r.check_allowed(argv, cwd=str(other))
-    refused = [
-        ["git", "fetch", "--all"],
-        ["git", "fetch", "--prune", "origin"],
-        ["git", "fetch", "upstream"],
-        ["git", "add", "-A"],
-        ["git", "add", "."],
-        ["git", "add", "--", ":(top)x"],
-        ["git", "add", "--", "../x"],
-        ["git", "commit", "-a", "-m", "x"],
-        ["git", "commit", "--amend", "-m", "x"],
-        ["git", "commit", "-m", "-x"],
-        ["git", "rebase", "-i", "origin/main"],
-        ["git", "rebase", "--interactive", "origin/main"],
-        ["git", "rebase", "main"],
-    ]
-    for argv in refused:
-        with pytest.raises(wc.RefusedCommand):
-            r.check_allowed(argv, cwd=str(evidence))
-
-
-def test_clone_only_into_the_evidence_folder(wc, runner_cls, evidence, tmp_path):
-    r = runner_cls(evidence_dir=str(evidence))
-    r.check_allowed(["git", "clone", f"https://github.com/{REPO}.git", str(evidence)])
-    with pytest.raises(wc.RefusedCommand):
-        r.check_allowed(
-            ["git", "clone", f"https://github.com/{REPO}.git", str(tmp_path / "x")]
-        )
-    with pytest.raises(wc.RefusedCommand):
-        r.check_allowed(
-            [
-                "git",
-                "clone",
-                "--mirror",
-                f"https://github.com/{REPO}.git",
-                str(evidence),
-            ]
-        )
-    with pytest.raises(wc.RefusedCommand):
-        r.check_allowed(["git", "clone", "--depth", "1", "u", str(evidence)])
-    with pytest.raises(wc.RefusedCommand):
-        runner_cls().check_allowed(["git", "clone", "u", "/e"])
-
-
-# --- gh, orca, the landed check -----------------------------------------------------
-
-
-def test_gh_has_three_shapes_and_an_explicit_repo_of_our_owners(wc, never_run_runner):
-    ok = [
-        [
-            "gh",
-            "pr",
-            "list",
-            "--repo",
-            REPO,
-            "--head",
-            "b",
-            "--state",
-            "all",
-            "--json",
-            "number",
-            "--limit",
-            "5",
-        ],
-        ["gh", "pr", "view", "700", "--repo", REPO, "--json", "state,mergedAt"],
-        ["gh", "issue", "view", "5", "--repo", "ironbellygroup/other"],
-    ]
-    for argv in ok:
-        never_run_runner.check_allowed(argv)
-    refused = [
-        ["gh", "pr", "list", "--head", "x"],
-        ["gh", "pr", "list", "--repo", REPO, "--repo", REPO],
-        ["gh", "pr", "list", "--repo", "SuperClaude-Org/SuperClaude_Framework"],
-        ["gh", "pr", "list", "--repo", REPO, "--web"],
-        ["gh", "pr", "list", "--repo", REPO, "-R", "o/r"],
-        ["gh", "pr", "list", "--repo", "bad repo"],
-        ["gh", "pr", "view", "--repo", REPO],
-        ["gh", "pr", "view", "x1", "--repo", REPO],
-        ["gh", "pr", "view", "7", "8", "--repo", REPO],
-        ["gh", "issue", "list", "--repo", REPO],
-        ["gh", "repo", "clone", REPO, "/e"],
-        ["gh", "pr", "list", "--repo"],
-    ]
-    for argv in refused:
-        with pytest.raises(wc.RefusedCommand):
-            never_run_runner.check_allowed(argv)
-
-
-ORCA_OK = [
-    ["orca", "repo", "list", "--json"],
-    ["orca", "repo", "list"],
-    ["orca", "worktree", "list", "--json"],
-    ["orca", "worktree", "ps", "--json"],
-    ["orca", "reference", "list", "--worktree", "id:1", "--json"],
-    ["orca", "terminal", "list", "--worktree", "id:1"],
-    ["orca", "worktree", "rm", "--worktree", "id:1"],
-]
-
-
-@pytest.mark.parametrize("argv", ORCA_OK, ids=[" ".join(a) for a in ORCA_OK])
-def test_orca_allowed_shapes(never_run_runner, argv):
-    never_run_runner.check_allowed(argv)
-
-
-def test_orca_other_shapes_are_refused(wc, never_run_runner):
-    for argv in (
-        ["orca", "repo", "list", "--all"],
-        ["orca", "worktree", "ps", "--watch"],
-        ["orca", "terminal", "list"],
-        ["orca", "terminal", "list", "--worktree", "id:1", "--all"],
-        ["orca", "worktree", "rm"],
-        ["orca", "worktree", "rm", "--worktree", "id:1", "extra"],
-        ["orca", "worktree"],
-        ["orca"],
-    ):
-        with pytest.raises(wc.RefusedCommand):
-            never_run_runner.check_allowed(argv)
-
-
-def test_orca_terminal_close_needs_authorization(wc, never_run_runner):
-    argv = ["orca", "terminal", "close", "--worktree", "id:7", "--all"]
-    with pytest.raises(wc.RefusedCommand):
-        never_run_runner.check_allowed(argv)
-    never_run_runner.authorize_close("id:7")
-    never_run_runner.check_allowed(argv)
-    # another worktree, a missing --all or an extra option is still refused
-    for other in (
-        ["orca", "terminal", "close", "--worktree", "id:8", "--all"],
-        ["orca", "terminal", "close", "--worktree", "id:7"],
-        ["orca", "terminal", "close", "--worktree", "id:7", "--all", "--force"],
-        ["orca", "terminal", "close", "--all", "--worktree", "id:7"],
-    ):
-        with pytest.raises(wc.RefusedCommand):
-            never_run_runner.check_allowed(other)
-
-
-def test_landed_check_only_from_the_lookup_locations(wc, never_run_runner):
-    never_run_runner.check_allowed(["bash", LANDED, "12"])
-    never_run_runner.check_allowed([LANDED, "12"])
-    elsewhere = "/tmp/evil/sc-closeout-protocol/scripts/branch-landed.sh"
-    for argv in (
-        ["bash", elsewhere, "12"],
-        [elsewhere, "12"],
-        ["bash", "/tmp/evil.sh", "12"],
-        ["bash", LANDED, "abc"],
-        ["bash", LANDED, "12", "13"],
-        ["bash", LANDED],
-        ["bash", "-c", "echo hi"],
-        ["bash", LANDED + "/../../../x.sh", "12"],
-    ):
-        with pytest.raises(wc.RefusedCommand):
-            never_run_runner.check_allowed(argv)
-
-
-def test_default_lookup_locations_follow_the_recorded_order(wc):
-    paths = wc.default_landed_paths()
-    assert len(paths) == 3
-    tail = "skills/sc-closeout-protocol/scripts/branch-landed.sh"
-    assert paths[0].endswith("/.claude/" + tail)
-    assert paths[1].endswith("/.claude/" + tail)
-    assert paths[2].endswith("/src/superclaude/" + tail)
-    assert paths[0] != paths[1]
-
-
-# --- git clean ----------------------------------------------------------------------
-
-
-def test_git_clean_only_for_registered_saved_paths(wc, never_run_runner, tmp_path):
-    wt = tmp_path / "wt"
-    wt.mkdir()
-    argv = ["xargs", "-0", "git", "clean", "-f", "-x", "--"]
-    never_run_runner.register_saved(str(wt), [".dev/a b.txt", ".dev/c.log"])
-    ok = b".dev/a b.txt\0.dev/c.log\0"
-    never_run_runner.check_allowed(argv, cwd=str(wt), stdin=ok)
-    with pytest.raises(wc.RefusedCommand):
-        never_run_runner.check_allowed(argv, cwd=str(wt), stdin=ok + b"other.txt\0")
-    with pytest.raises(wc.RefusedCommand):
-        never_run_runner.check_allowed(argv, cwd=str(wt), stdin=b"")
-    with pytest.raises(wc.RefusedCommand):
-        never_run_runner.check_allowed(argv, cwd=str(tmp_path), stdin=ok)
-    for other in (
-        ["xargs", "-0", "git", "clean", "-f", "-d", "-x", "--"],
-        ["xargs", "-0", "git", "clean", "-fx", "--"],
-        ["xargs", "-0", "git", "clean", "-f", "-x"],
-        ["xargs", "git", "clean", "-f", "-x", "--"],
-        ["xargs", "-0", "rm", "--"],
-    ):
-        with pytest.raises(wc.RefusedCommand):
-            never_run_runner.check_allowed(other, cwd=str(wt), stdin=ok)
-
-
-# --- read verbs and named write verbs: exact shapes ------------------------------------
-
-
-def test_read_and_named_write_shapes_are_allowed(wc, never_run_runner):
-    ok = [
-        ["git", "status", "--porcelain", "-z", "--ignored"],
-        ["git", "status", "--untracked-files=all"],
-        ["git", "worktree", "list"],
-        ["git", "worktree", "list", "--porcelain"],
-        ["git", "worktree", "remove", "/some/path"],
-        ["git", "branch", "-d", "topic"],
-        ["git", "branch", "--list", "topic"],
-        ["git", "branch", "--show-current"],
-        ["git", "remote", "get-url", "origin"],
-        ["git", "config", "--get", "remote.origin.url"],
-        ["git", "rev-parse", "HEAD"],
-        ["git", "rev-parse", "--verify", "HEAD"],
-        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
-        ["git", "-C", "/some/wt", "rev-parse", "--show-toplevel"],
-        ["git", "log", "-1", "--format=%H", "HEAD"],
-        ["git", "log", "--format=%H", "a..b", "--", "p"],
-        ["git", "ls-files", "-z", "--others", "--ignored", "--exclude-standard"],
-        ["git", "ls-tree", "-r", "--name-only", "HEAD"],
-        ["git", "merge-base", "--is-ancestor", "a", "b"],
-        ["git", "rev-list", "--count", "a..b"],
-        ["git", "diff", "--quiet", "HEAD", "--", "p"],
-        ["tar", "-tzf", "/x/ignored.tar.gz"],
-        ["bash", LANDED, "12"],
-    ]
-    for argv in ok:
-        never_run_runner.check_allowed(argv)
-    for argv in (
-        ["tar", "-xzf", "/x/a.tar.gz"],
-        ["tar", "-tzf", "-x"],
-        ["tar", "-tzf"],
-        ["git", "status", "--short"],
-        ["git", "status", "x"],
-        ["git", "worktree", "list", "--verbose"],
-        ["git", "worktree", "remove"],
-        ["git", "worktree", "remove", "-x"],
-        ["git", "worktree", "add", "/x"],
-        ["git", "remote", "add", "o", "u"],
-        ["git", "remote", "get-url"],
-        ["git", "config", "--set", "a", "b"],
-        ["git", "config", "user.name", "x"],
-        ["git", "merge-base", "a"],
-        ["git", "rev-list", "a", "--"],
-        ["git", "log", "--format"],
-        ["git", "rev-parse", "+x"],
-        ["git", "rev-parse", ":/x"],
-    ):
-        with pytest.raises(wc.RefusedCommand):
-            never_run_runner.check_allowed(argv)
-
-
-# --- recording ---------------------------------------------------------------
-
-
-def test_every_allowed_command_is_recorded_with_its_working_folder(
-    runner_cls, tmp_path
-):
-    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
-    runner = runner_cls()
-    res = runner.run(["git", "rev-parse", "--git-dir"], cwd=str(tmp_path))
-    assert res.returncode == 0
-    assert [c.argv for c in runner.commands] == [["git", "rev-parse", "--git-dir"]]
-    assert runner.commands[0].cwd == str(tmp_path)
-
-
-# --- the file itself ------------------------------------------------------------
-
-
-def test_only_standard_library_imports():
-    tree = ast.parse(_source())
-    names = set()
-    for node in ast.walk(tree):
-        if isinstance(node, ast.Import):
-            names.update(a.name.split(".")[0] for a in node.names)
-        elif isinstance(node, ast.ImportFrom) and node.level == 0:
-            names.add((node.module or "").split(".")[0])
-    assert names, "no imports found"
-    assert names <= set(sys.stdlib_module_names), sorted(
-        names - set(sys.stdlib_module_names)
-    )
-
-
-def test_no_call_that_deletes_a_file_and_no_rm_command():
-    tree = ast.parse(_source())
-    banned_attrs = {"remove", "unlink", "rmtree", "rmdir", "removedirs"}
-    for node in ast.walk(tree):
-        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
-            assert node.func.attr not in banned_attrs, ast.dump(node.func)
-        # no argument list that starts with the string "rm"
-        if isinstance(node, ast.List) and node.elts:
-            first = node.elts[0]
-            if isinstance(first, ast.Constant) and first.value == "rm":
-                raise AssertionError("an argument list starts with rm")
-
-
-def test_subprocess_is_started_only_inside_execute():
-    tree = ast.parse(_source())
-    owners = []
-    for fn in ast.walk(tree):
-        if isinstance(fn, ast.FunctionDef):
-            for node in ast.walk(fn):
-                if (
-                    isinstance(node, ast.Attribute)
-                    and isinstance(node.value, ast.Name)
-                    and node.value.id == "subprocess"
-                    and node.attr
-                    in {"run", "Popen", "call", "check_call", "check_output"}
-                ):
-                    owners.append(fn.name)
-    assert owners and set(owners) == {"_execute"}
-
-
-def test_apache_notice_block_and_provenance_pointer_are_at_the_top():
-    head = "\n".join(_source().splitlines()[:8])
-    assert "Jay Wedgeworth" in head
-    assert "Apache License, Version 2.0" in head
-    assert "scripts/worktree_cleanup_PROVENANCE.md" in head
-
-
-def test_the_file_never_names_a_credential_file():
-    text = _source()
-    assert "hosts.yml" not in text
-    assert "~/.env" not in text
-    assert "'.env'" not in text and '".env"' not in text
-
-
-def test_no_dash_characters_in_the_script_and_its_tests():
-    # Built from code points so these files hold no such character themselves.
-    for path in (
-        SCRIPT,
-        *SCRIPT.parents[1].joinpath("tests", "worktree_cleanup").glob("*.py"),
-    ):
-        text = path.read_text(encoding="utf-8")
-        assert chr(0x2013) not in text and chr(0x2014) not in text, path
-
-
-# --- the credential goes only where the plan allows it ------------------------------------
-
-
-def _env(runner, argv, monkeypatch):
-    monkeypatch.setenv("GH_TOKEN", "placeholder-not-a-secret")
-    monkeypatch.setenv("GITHUB_TOKEN", "placeholder-not-a-secret")
-    return runner._env_for(argv)
-
-
-@pytest.mark.parametrize(
-    "argv",
-    [
-        ["git", "status", "--porcelain"],
-        ["git", "worktree", "remove", "/x"],
-        ["git", "branch", "-d", "topic"],
-        ["git", "fetch", "origin"],
-        ["git", "clone", "u", "/e"],
-        ["git", "commit", "-m", "x"],
-        ["git", "-C", "/e", "fetch", "origin"],
-        ["orca", "worktree", "ps", "--json"],
-        ["orca", "terminal", "close", "--worktree", "id:1", "--all"],
-        ["tar", "-tzf", "/x/a.tar.gz"],
-        ["xargs", "-0", "git", "clean", "-f", "-x", "--"],
-    ],
-    ids=lambda a: " ".join(a),
-)
-def test_token_is_not_given_to_other_children(runner_cls, monkeypatch, argv):
-    env = _env(runner_cls(), argv, monkeypatch)
-    assert "GH_TOKEN" not in env and "GITHUB_TOKEN" not in env
-
-
-@pytest.mark.parametrize(
-    "argv",
-    [
-        ["gh", "pr", "list", "--repo", REPO],
-        ["bash", LANDED, "5"],
-        [LANDED, "5"],
-        ["git", "push", "origin", "main"],
-        ["git", "-c", HELPER, "push", "origin", "main"],
-        ["git", "-C", "/e", "push", "origin", "main"],
-    ],
-    ids=lambda a: " ".join(a),
-)
-def test_token_is_given_to_gh_the_landed_check_and_git_push(
-    runner_cls, monkeypatch, argv
-):
-    env = _env(runner_cls(), argv, monkeypatch)
-    assert env.get("GH_TOKEN") == "placeholder-not-a-secret"
-    assert env.get("GITHUB_TOKEN") == "placeholder-not-a-secret"
-
-
-def test_literal_pathspecs_only_for_the_clean_command(runner_cls, monkeypatch):
-    r = runner_cls()
-    assert (
-        _env(r, ["xargs", "-0", "git", "clean", "-f", "-x", "--"], monkeypatch)[
-            "GIT_LITERAL_PATHSPECS"
-        ]
-        == "1"
-    )
-    assert "GIT_LITERAL_PATHSPECS" not in _env(r, ["git", "status"], monkeypatch)
-
-
-def test_external_diff_hook_is_removed_from_every_child(runner_cls, monkeypatch):
-    monkeypatch.setenv("GIT_EXTERNAL_DIFF", "x")
-    env = runner_cls()._env_for(["git", "diff", "--quiet"])
-    assert "GIT_EXTERNAL_DIFF" not in env


===== new file: tests/worktree_cleanup/test_verbs.py =====
"""The four verbs (Task 12): list, archive, retire and prune, their lock, files and exit codes.

Git runs on throwaway repositories under ``tmp_path`` with a local bare evidence remote;
``gh`` and ``orca`` answer from canned replies. Nothing here touches a real worktree.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import os
import time
from pathlib import Path

import pytest

from .conftest import git_in, make_fake_proc
from .test_archive import git_identity  # noqa: F401 - autouse: the evidence commit needs an identity
from .test_facts import write

FAR = time.time() + 30 * 86400  # every worktree looks 30 days idle and old enough


class World:
    """A throwaway repo with worktrees, canned gh and orca replies, and an evidence remote."""

    def __init__(self, wc, runner_cls, repo, evidence_bare, tmp_path, listed=()):
        self.wc, self.repo, self.tmp, self.bare = wc, repo, tmp_path, evidence_bare
        self.clone = str(tmp_path / "evidence-clone")
        self.out = tmp_path / "out"
        self.proc = str(make_fake_proc(tmp_path / "proc", {}))
        self.states: dict[str, str] = {}  # branch -> pull request state
        self.paths: dict[str, Path] = {}
        self.listed = set(listed)  # worktrees Orca lists
        self.gh_override = {}
        self.orca_calls: list[list[str]] = []
        self.runner = runner_cls(
            evidence_dir=self.clone, replies={"gh": self.gh, "orca": self.orca}
        )

    def add(self, name, state="MERGED", dev=True):
        path = self.repo.add_worktree(name)
        if dev:
            write(path / ".dev" / "tasks" / "note.md", f"{name}\n")
        self.paths[name] = path
        self.states[name] = state
        return path

    def head(self, name):
        return git_in(self.paths[name], "rev-parse", "HEAD").strip()

    def gh(self, argv, cwd):
        wc = self.wc
        key = tuple(argv[1:3])
        if key in self.gh_override:
            return self.gh_override[key](argv)
        if key == ("pr", "list"):
            branch = argv[argv.index("--head") + 1]
            state = self.states.get(branch)
            rows = []
            if state:
                rows = [
                    {
                        "number": 700, "state": state, "headRefOid": self.head(branch),
                        "headRefName": branch, "author": {"login": "example-user"},
                        "mergedAt": "2026-11-10T12:00:00Z" if state == "MERGED" else None,
                        "title": "t", "body": "", "closingIssuesReferences": [],
                    }
                ]  # fmt: skip
            return wc.Result(0, json.dumps(rows), "")
        if key == ("pr", "view"):
            return wc.Result(
                0,
                json.dumps({"state": "MERGED", "mergedAt": "2026-11-10T12:00:00Z"}),
                "",
            )
        return wc.Result(1, "", "unexpected gh call")

    def orca(self, argv, cwd):
        wc = self.wc
        self.orca_calls.append(list(argv))
        key = tuple(argv[1:3])
        if key == ("repo", "list"):
            repos = [
                {"id": "r1", "path": str(self.repo.main), "displayName": "example"}
            ]
            return wc.Result(
                0, json.dumps({"ok": True, "result": {"repos": repos}}), ""
            )
        if key == ("worktree", "ps"):
            rows = [
                {
                    "worktreeId": f"id-{n}", "path": str(p), "isPinned": False,
                    "liveTerminalCount": 0, "lastActivityAt": None, "linkedPR": None, "comment": "",
                }
                for n, p in self.paths.items() if n in self.listed and p.exists()
            ]  # fmt: skip
            return wc.Result(
                0, json.dumps({"ok": True, "result": {"worktrees": rows}}), ""
            )
        if key == ("worktree", "list"):
            return wc.Result(0, '{"ok": true, "result": {"worktrees": []}}', "")
        if key == ("reference", "list"):
            return wc.Result(0, '{"ok": true, "result": {"references": []}}', "")
        if key == ("worktree", "rm"):
            name = next(n for n, p in self.paths.items() if f"id:id-{n}" == argv[4])
            git_in(self.repo.main, "worktree", "remove", str(self.paths[name]))
            return wc.Result(0, "", "")
        return wc.Result(0, "", "")

    def env(self):
        return {"RUN_EVIDENCE_DIR": self.clone, "RUN_EVIDENCE_REPO": str(self.bare)}

    def run(self, *argv, cwd=None, out=True):
        extra = ["--out", str(self.out)] if out else []
        self.runner.commands.clear()
        return self.wc.main(
            [*argv, *extra], runner=self.runner, env=self.env(), now=FAR,
            proc_root=self.proc, cwd=cwd or str(self.tmp),
        )  # fmt: skip

    def verbs(self):
        return [" ".join(c.argv[:3]) for c in self.runner.commands]

    def removal_commands(self):
        return [
            c.argv for c in self.runner.commands
            if c.argv[:3] in (["git", "worktree", "remove"], ["orca", "worktree", "rm"])
            or c.argv[:2] == ["xargs", "-0"]
            or c.argv[1:3] == ["branch", "-d"]
            or c.argv[:3] == ["orca", "terminal", "close"]
            or "push" in c.argv
        ]  # fmt: skip

    def snapshot(self):
        seen = {}
        for path in self.paths.values():
            for dirpath, _dirs, names in os.walk(path):
                if ".git" in Path(dirpath).parts:
                    continue
                for n in names:
                    full = os.path.join(dirpath, n)
                    seen[full] = hashlib.sha256(Path(full).read_bytes()).hexdigest()
        return seen


@pytest.fixture
def world(wc, runner_cls, throwaway_repo, evidence_bare, tmp_path):
    return World(wc, runner_cls, throwaway_repo, evidence_bare, tmp_path)


def table_lines(text):
    return [ln for ln in text.splitlines() if ln.startswith("| ")]


# -- list and prune without --apply: a table, no removal ---------------------------------------


def test_list_prints_the_table_and_records_no_removal_command(world, capsys):
    world.add("done")
    world.add("open", state="OPEN")
    before = world.snapshot()
    assert world.run("list", out=False) == 0
    shown = capsys.readouterr().out
    lines = table_lines(shown)
    assert (
        lines[0].startswith("| repo | folder | branch | in orca |")
        and lines[0].count(" | ") == 10
    )
    by_folder = {
        ln.split(" | ")[1]: ln for ln in lines[1:]
    }  # the dashes row is not a "| " line
    assert (
        "removable" in by_folder["done"]
        and "pull request #700 is open" in by_folder["open"]
    )
    assert "main" in by_folder and "main checkout" in by_folder["main"]
    assert world.removal_commands() == []
    assert world.snapshot() == before
    assert (
        "summary: removed 0, kept 3, failed 0 (1 removable; dry run, nothing was removed)"
        in shown
    )
    assert not world.out.exists()  # list writes no files


def test_prune_without_apply_writes_both_files_and_nothing_inside_a_worktree(
    wc, world, capsys
):
    world.add("done")
    before = world.snapshot()
    assert world.run("prune") == 0
    md = list(world.out.glob("prune-*.md"))
    js = list(world.out.glob("prune-*.json"))
    assert len(md) == 1 and len(js) == 1
    doc = json.loads(js[0].read_text())
    assert set(doc) >= {"columns", "rows", "commands", "summary"}
    assert {r["folder"] for r in doc["rows"]} == {"main", "done"}
    assert (
        all(set(c) == {"argv", "cwd", "stdin_paths"} for c in doc["commands"])
        and doc["commands"]
    )
    assert doc["summary"]["dry_run"] is True and doc["summary"]["removed"] == 0
    assert md[0].read_text() == wc.render_markdown(doc["rows"])
    assert world.removal_commands() == [] and world.snapshot() == before
    # both files are under --out, which is outside every worktree
    assert all(
        not str(p).startswith(str(path))
        for p in (*md, *js)
        for path in world.paths.values()
    )
    assert (
        world.paths["done"].exists()
        and (world.paths["done"] / ".dev" / "tasks" / "note.md").exists()
    )
    assert "(1 removable; dry run, nothing was removed)" in capsys.readouterr().out


def test_removable_row_with_terminals_open_says_they_will_be_closed_first(
    wc, world, capsys
):
    world.add("done")
    world.listed = {"done"}

    def with_terminals(argv, cwd):
        if tuple(argv[1:3]) == ("worktree", "ps"):
            rows = [{"worktreeId": "id-done", "path": str(world.paths["done"]), "isPinned": False,
                     "liveTerminalCount": 2, "lastActivityAt": None, "linkedPR": None, "comment": ""}]  # fmt: skip
            return wc.Result(
                0, json.dumps({"ok": True, "result": {"worktrees": rows}}), ""
            )
        return World.orca(world, argv, cwd)

    world.runner.replies["orca"] = with_terminals
    assert world.run("list", out=False) == 0
    assert "its Orca terminals will be closed first" in capsys.readouterr().out
    assert not any(
        a[:3] == ["orca", "terminal", "close"]
        for a in [c.argv for c in world.runner.commands]
    )


# -- prune --apply: only removable rows are processed ------------------------------------------------


def test_prune_apply_removes_only_the_removable_rows_and_a_second_run_has_nothing_to_do(
    world, capsys
):
    world.add("done")
    world.add("open", state="OPEN")
    world.add("plain", dev=False)
    assert world.run("prune", "--apply") == 0
    shown = capsys.readouterr().out
    assert not world.paths["done"].exists() and not world.paths["plain"].exists()
    assert (
        world.paths["open"].exists()
        and (world.paths["open"] / ".dev" / "tasks" / "note.md").exists()
    )
    assert "summary: removed 2, kept 2, failed 0" in shown
    removed_paths = {
        c[-1]
        for c in world.removal_commands()
        if c[:3] == ["git", "worktree", "remove"]
    }
    assert removed_paths == {str(world.paths["done"]), str(world.paths["plain"])}
    cleared = [c for c in world.runner.commands if c.argv[:2] == ["xargs", "-0"]]
    assert len(cleared) == 1 and cleared[0].cwd == str(world.paths["done"])
    doc = json.loads(next(world.out.glob("prune-*.json")).read_text())
    decisions = {r["folder"]: r["decision"] for r in doc["rows"]}
    assert decisions == {
        "main": "kept",
        "done": "removed",
        "plain": "removed",
        "open": "kept",
    }
    # the save reached the evidence remote before the clear
    assert (
        git_in(world.bare, "ls-tree", "-r", "--name-only", "main").count("note.md") == 1
    )
    # a second run after the removal: nothing more to do
    assert world.run("prune", "--apply") == 0
    assert "nothing more to do" in capsys.readouterr().out
    assert world.removal_commands() == []


def test_removal_through_orca_when_orca_lists_the_worktree(world, capsys):
    world.add("done")
    world.listed = {"done"}
    assert world.run("prune", "--apply") == 0
    assert ["orca", "worktree", "rm", "--worktree", "id:id-done"] in world.orca_calls
    assert not world.paths["done"].exists()
    assert not any(
        c.argv[:3] == ["git", "worktree", "remove"] for c in world.runner.commands
    )


# -- the lock ---------------------------------------------------------------------------------------------


def test_a_second_run_cannot_remove_what_a_run_holding_the_lock_is_removing(
    wc, world, capsys
):
    world.add("done")
    holder = wc.RepoLocks(world.out)
    assert holder.acquire(str(world.repo.main)) is True
    try:
        assert world.run("prune", "--apply") == 0
    finally:
        holder.release_all()
    shown = capsys.readouterr().out
    assert "another run holds the lock" in shown
    assert world.paths["done"].exists() and world.removal_commands() == []
    locks = list(world.out.glob("lock-*.lock"))
    assert len(locks) == 1 and locks[0].exists()  # the lock file is never deleted
    # once the first run is over the lock is free and the removal goes through
    assert world.run("prune", "--apply") == 0
    assert (
        not world.paths["done"].exists()
        and len(list(world.out.glob("lock-*.lock"))) == 1
    )


def test_the_lock_is_per_repo(wc, tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    a.mkdir()
    b.mkdir()
    one, two = wc.RepoLocks(tmp_path / "o"), wc.RepoLocks(tmp_path / "o")
    assert one.acquire(str(a)) and one.acquire(str(a))  # the same run may ask again
    assert two.acquire(str(a)) is False and two.acquire(str(b)) is True
    one.release_all()
    two.release_all()
    assert wc.RepoLocks(tmp_path / "o").acquire(str(a)) is True


# -- retire ------------------------------------------------------------------------------------------------


def test_retire_by_folder_name_or_path_removes_one_worktree_under_apply(world, capsys):
    world.add("done")
    world.add("other")
    assert world.run("retire", "done") == 0  # dry run: nothing happens
    assert world.paths["done"].exists() and "dry run" in capsys.readouterr().out
    assert world.removal_commands() == []
    assert world.run("retire", str(world.paths["done"]) + "/", "--apply") == 0
    assert not world.paths["done"].exists() and world.paths["other"].exists()
    assert world.run("retire", "other", "--apply") == 0
    assert not world.paths["other"].exists()


def test_retire_exit_64_for_unknown_ambiguous_not_removable_or_run_from_inside(
    wc, world, runner_cls, capsys
):
    world.add("done")
    world.add("open", state="OPEN")
    assert world.run("retire", "nope", "--apply") == 64
    assert "is not a git worktree of one of our repos" in capsys.readouterr().err
    assert world.run("retire", "open", "--apply") == 64
    assert "not removable: pull request #700 is open" in capsys.readouterr().err
    assert (
        world.run("retire", "main", "--apply") == 64
    )  # the main checkout is never removable
    assert (
        world.run("retire", "done", "--apply", cwd=str(world.paths["done"] / ".dev"))
        == 64
    )
    assert "outside the worktree" in capsys.readouterr().err
    assert world.paths["done"].exists() and world.removal_commands() == []
    # two worktrees with the same folder name in two repos: ambiguous
    found = wc.Found(
        [(wc.GitWorktree(f"/a/{n}", "/a", "h", "b", False, False, False, False, False), None) for n in ("same",)]
        + [(wc.GitWorktree("/b/same", "/b", "h", "b", False, False, False, False, False), None)],
        [], [],
    )  # fmt: skip
    match, problem = wc.resolve_selector(found, "same")
    assert match is None and "matches 2 worktrees" in problem
    assert wc.resolve_selector(found, "/b/same")[0] is found.worktrees[1]


# -- archive -------------------------------------------------------------------------------------------------


def test_archive_saves_and_prints_verified_and_removes_nothing(world, capsys):
    world.add("done")
    before = world.snapshot()
    assert world.run("archive", "done") == 0
    shown = capsys.readouterr().out
    assert any(
        ln.startswith("VERIFIED IronClaude/") or ln.startswith("VERIFIED example/")
        for ln in shown.splitlines()
    )
    assert world.snapshot() == before and world.paths["done"].exists()
    assert not any(
        c[:3] == ["git", "worktree", "remove"] for c in world.removal_commands()
    )
    assert world.run("archive", "done") == 0  # a repeat verifies the same folder


def test_archive_refuses_a_worktree_with_a_tracked_edit_or_without_a_merged_request(
    world, capsys
):
    path = world.add("edited")
    (path / "README.md").write_text("edited\n", encoding="utf-8")
    assert world.run("archive", "edited") == 64
    assert "cannot archive: 1 changed tracked file" in capsys.readouterr().err
    world.add("unmerged", state="OPEN")
    assert world.run("archive", "unmerged") == 64
    assert not Path(world.clone).exists()  # nothing was cloned or saved


# -- exit codes --------------------------------------------------------------------------------------------------


def test_exit_69_when_a_lookup_fails_and_the_table_still_shows_it(wc, world, capsys):
    world.add("done")
    world.gh_override[("pr", "list")] = lambda argv: wc.Result(1, "", "HTTP 502")
    assert world.run("prune") == 69
    shown = capsys.readouterr().out
    assert "pull request lookup failed" in shown and "failed 1" in shown
    assert world.removal_commands() == []


def test_exit_69_when_a_removal_fails_and_the_summary_carries_the_three_counts(
    wc, runner_cls, throwaway_repo, evidence_bare, tmp_path, capsys
):
    w = World(wc, runner_cls, throwaway_repo, evidence_bare, tmp_path)
    w.add("done")

    def refuse(argv, cwd):
        if argv[1:3] == ["worktree", "remove"]:
            return wc.Result(128, "", "fatal: refused")
        return None

    w.runner.replies["git"] = refuse
    assert w.run("prune", "--apply") == 69
    shown = capsys.readouterr().out
    assert "summary: removed 0, kept 1, failed 1" in shown
    assert w.paths["done"].exists()


def test_exit_64_when_out_is_inside_a_worktree(world, capsys):
    path = world.add("done")
    assert world.run("prune", "--out", str(path / "inside"), out=False) == 64
    assert "--out must not be inside a worktree" in capsys.readouterr().err
    assert not (path / "inside").exists()
    assert world.removal_commands() == []


def test_exit_69_when_no_repo_can_be_found(wc, runner_cls, tmp_path, capsys):
    runner = runner_cls(evidence_dir=str(tmp_path / "e"))
    code = wc.main(
        ["list"], runner=runner, env={}, cwd=str(tmp_path), proc_root=str(tmp_path)
    )
    assert code == 69
    assert "not a git checkout" in capsys.readouterr().err


def test_a_folder_that_is_not_a_git_worktree_never_appears(world, capsys):
    world.add("done")
    stray = world.repo.root / "wts" / "stray-folder"
    stray.mkdir()
    write(stray / "file.txt")
    assert world.run("list", out=False) == 0
    assert "stray-folder" not in capsys.readouterr().out
    assert (stray / "file.txt").exists()


def test_the_orca_repo_list_failing_falls_back_to_the_current_repo_and_says_so(
    wc, world, capsys
):
    world.add("done")

    def orca_down(argv, cwd):
        return wc.Result(1, "", "down")

    world.runner.replies["orca"] = orca_down
    # unreadable Orca facts (pinned, terminals) are a lookup failure: exit 69, nothing removable
    assert world.run("list", out=False, cwd=str(world.repo.main)) == 69
    shown = capsys.readouterr().out
    assert "note: Orca unavailable" in shown and "current checkout" in shown
    assert "| done |" in shown
    assert "Orca unavailable, so whether it is pinned is unknown" in shown
    assert "removable" not in shown.replace("no worktree can be removed", "")


def test_an_unreadable_orca_never_lets_a_pinned_worktree_be_removed(wc, world, capsys):
    world.add("done")
    world.listed = {"done"}

    def pinned_but_unreadable(argv, cwd):
        if tuple(argv[1:3]) == ("worktree", "ps"):
            return wc.Result(0, "<html>", "")  # Orca answered, but not with a list
        return World.orca(world, argv, cwd)

    world.runner.replies["orca"] = pinned_but_unreadable
    assert world.run("prune", "--apply") == 69
    assert world.paths["done"].exists() and world.removal_commands() == []
    assert "failed 1" in capsys.readouterr().out
    assert world.run("retire", "done", "--apply") == 69
    assert world.paths["done"].exists() and world.removal_commands() == []


# -- every unreadable fact is a lookup failure (exit 69), for every verb ----------------------------------------------


def test_a_landed_check_that_says_unknown_is_exit_69_for_prune_retire_and_archive(
    wc, world, capsys
):
    world.add("done")
    world.gh_override[("pr", "view")] = lambda argv: wc.Result(1, "", "HTTP 502")
    assert world.run("prune") == 69
    assert "landed check said UNKNOWN" in capsys.readouterr().out
    assert world.run("retire", "done", "--apply") == 69
    assert world.run("archive", "done") == 69
    assert world.paths["done"].exists() and world.removal_commands() == []


def test_a_pull_request_lookup_that_fails_is_exit_69_for_retire_and_archive(
    wc, world, capsys
):
    world.add("done")
    world.gh_override[("pr", "list")] = lambda argv: wc.Result(1, "", "HTTP 502")
    assert world.run("retire", "done", "--apply") == 69
    assert "pull request lookup failed" in capsys.readouterr().err
    assert world.run("archive", "done") == 69
    assert world.run("prune") == 69


def test_a_selector_in_a_repo_whose_worktree_list_failed_is_exit_69(wc, world, capsys):
    world.add("done")

    def list_fails(argv, cwd):
        return (
            wc.Result(128, "", "fatal") if argv[1:3] == ["worktree", "list"] else None
        )

    world.runner.replies["git"] = list_fails
    assert world.run("retire", "done", "--apply") == 69
    assert "git worktree list failed" in capsys.readouterr().err


# -- the output folder -------------------------------------------------------------------------------------------


def test_archive_and_retire_also_refuse_an_output_folder_inside_a_worktree(
    world, capsys
):
    path = world.add("done")
    for verb in (("archive", "done"), ("retire", "done", "--apply"), ("list",)):
        assert world.run(*verb, "--out", str(path / ".dev" / "out"), out=False) == 64
        assert "--out must not be inside a worktree" in capsys.readouterr().err
    assert not (path / ".dev" / "out").exists() and world.removal_commands() == []
    assert path.exists()


def test_an_output_folder_that_cannot_be_used_stops_before_any_removal(world, capsys):
    world.add("done")
    blocker = world.tmp / "a-file"
    blocker.write_text("not a folder\n", encoding="utf-8")
    assert world.run("prune", "--apply", "--out", str(blocker / "sub"), out=False) == 69
    assert "--out cannot be used" in capsys.readouterr().err
    assert world.paths["done"].exists() and world.removal_commands() == []
    # retire and archive hit the same problem when they take the lock
    assert (
        world.run("retire", "done", "--apply", "--out", str(blocker / "sub"), out=False)
        == 69
    )
    assert "lock could not be taken" in capsys.readouterr().out
    assert world.paths["done"].exists() and world.removal_commands() == []
    assert world.run("archive", "done", "--out", str(blocker / "sub"), out=False) == 69
    assert "lock could not be taken" in capsys.readouterr().err


def test_output_files_that_cannot_be_written_give_exit_69_after_the_table(
    wc, world, capsys, monkeypatch
):
    world.add("done")

    def refuse(self, *a, **k):
        raise OSError(30, "Read-only file system")

    monkeypatch.setattr(Path, "write_text", refuse)
    assert world.run("prune") == 69
    shown = capsys.readouterr()
    assert "summary:" in shown.out  # the table and the summary were printed first
    assert "the output files could not be written" in shown.err


# -- a fact that cannot be read at the re-check is a failure (exit 69); a change is a plain "kept" -----------------------


def _break_the_recheck(wc, world, monkeypatch, case):
    """Let the first read of the worktree through; make the read after the save fail."""
    plain = str(world.paths["plain"])
    if case == "scan":
        calls = []
        real_scan = wc.scan_processes

        def scan(*a, **k):
            calls.append(1)
            return (
                real_scan(*a, **k)
                if len(calls) == 1
                else wc.ProcScan(False, failure="x")
            )

        monkeypatch.setattr(wc, "scan_processes", scan)
        return
    seen = []
    real = wc.gather_facts

    def facts(runner, wt, orca=None):
        got = real(runner, wt, orca)
        if wt.path != plain:
            return got
        seen.append(1)
        if len(seen) == 1:
            return got
        if case == "status":
            return dataclasses.replace(got, state=None)
        return dataclasses.replace(got, present=False)

    monkeypatch.setattr(wc, "gather_facts", facts)


@pytest.mark.parametrize("case", ["status", "folder", "scan"])
def test_prune_apply_exits_69_when_the_re_check_cannot_read_a_fact(
    wc, world, capsys, monkeypatch, case
):
    world.add("plain", dev=False)
    _break_the_recheck(wc, world, monkeypatch, case)
    assert world.run("prune", "--apply") == 69
    shown = capsys.readouterr().out
    assert "failed 1" in shown
    doc = json.loads(next(world.out.glob("prune-*.json")).read_text())
    assert {r["folder"]: r["decision"] for r in doc["rows"]}["plain"] == "failed"
    assert doc["summary"]["failed"] == 1
    assert world.paths["plain"].exists()
    assert world.removal_commands() == []


@pytest.mark.parametrize("case", ["status", "folder", "scan"])
def test_retire_apply_exits_69_when_the_re_check_cannot_read_a_fact(
    wc, world, capsys, monkeypatch, case
):
    world.add("plain", dev=False)
    _break_the_recheck(wc, world, monkeypatch, case)
    assert world.run("retire", "plain", "--apply") == 69
    assert world.paths["plain"].exists() and world.removal_commands() == []


def test_a_real_change_during_the_terminal_close_is_still_kept(wc, world, capsys):
    world.add("done")
    world.listed = {"done"}
    path = world.paths["done"]

    def busy(argv, cwd):
        key = tuple(argv[1:3])
        if key == ("worktree", "ps"):
            rows = [{"worktreeId": "id-done", "path": str(path), "isPinned": False,
                     "liveTerminalCount": 1, "lastActivityAt": None, "linkedPR": None, "comment": ""}]  # fmt: skip
            return wc.Result(
                0, json.dumps({"ok": True, "result": {"worktrees": rows}}), ""
            )
        if key == ("terminal", "close"):
            write(path / "made-by-the-terminal.txt")  # an agent was still working
            return wc.Result(0, "", "")
        return World.orca(world, argv, cwd)

    world.runner.replies["orca"] = busy
    assert world.run("prune", "--apply") == 0
    assert "changed since the terminals were closed" in capsys.readouterr().out
    assert path.exists()
    assert not any(c[:2] == ["xargs", "-0"] for c in world.removal_commands())
    assert world.run("retire", "done", "--apply") == 64
    assert path.exists()


Codegraph context: index_state=fresh checked_at=2026-11-20T18:23:04Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-687 projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-687
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep and Read floor for dependents of changed symbols (this task creates new files or edits registration lists; see the diff).

Delta diff from the previous reviewed tree (empty on the first review): diff --git a/scripts/worktree_cleanup.py b/scripts/worktree_cleanup.py
index be90d5250..68f51ddce 100644
--- a/scripts/worktree_cleanup.py
+++ b/scripts/worktree_cleanup.py
@@ -2405,7 +2405,7 @@ def remove_worktree(
         inp = dataclasses.replace(inp, save_state=SAVE_NEEDED)
     first = decide(inp)
     if first.decision != "removable":
-        return RemovalResult("kept", first.reason)
+        return RemovalResult("failed" if first.unread else "kept", first.reason)
     main_checkout = wt.repo_path
     if _inside(main_checkout, wt.path):
         return RemovalResult(
@@ -2443,10 +2443,31 @@ def remove_worktree(
         steps.append("closed Orca terminals")
 
     # 3. check again: a terminal may have been working
+    # A fact that cannot be read is a lookup failure (failed, exit 69); a fact that was read
+    # and differs is a change (kept).
     again = gather_facts(runner, wt, orca)
+    unreadable = ""
+    if not again.present:
+        unreadable = "the folder could not be read"
+    elif again.state is None:
+        unreadable = "git status could not be read"
+    elif again.head is None:
+        unreadable = "HEAD could not be read"
+    else:
+        for p in sorted(digests):
+            saved_path = os.path.join(wt.path, p)
+            if os.path.lexists(saved_path) and _safe_sha(saved_path) is None:
+                unreadable = "a saved file could not be read"
+                break
+    if unreadable:
+        return RemovalResult(
+            "failed",
+            f"re-check failed: {unreadable} after the terminals were closed",
+            tuple(steps),
+            verified=verified,
+        )
     changed = (
-        again.state is None
-        or again.state != facts.state
+        again.state != facts.state
         or again.head != facts.head
         or any(
             p in digests and _safe_sha(os.path.join(wt.path, p)) != digests[p]
@@ -2454,6 +2475,13 @@ def remove_worktree(
         )
     )
     after = commits_after_pr(runner, wt.path, again.head, pr.head_oid)
+    if after.relation == "unknown":
+        return RemovalResult(
+            "failed",
+            f"re-check failed: {after.reason}",
+            tuple(steps),
+            verified=verified,
+        )
     if changed or after.relation not in ("same", "ancestor"):
         return RemovalResult(
             "kept",
@@ -2464,7 +2492,7 @@ def remove_worktree(
     scan = scan_processes(proc_root)
     if not scan.ok:
         return RemovalResult(
-            "kept",
+            "failed",
             f"in use: the process scan failed ({scan.failure})",
             tuple(steps),
             verified=verified,
diff --git a/tests/worktree_cleanup/test_removal.py b/tests/worktree_cleanup/test_removal.py
index d7496067d..f05fa853e 100644
--- a/tests/worktree_cleanup/test_removal.py
+++ b/tests/worktree_cleanup/test_removal.py
@@ -316,7 +316,112 @@ def test_a_process_still_inside_after_the_close_keeps_the_worktree(wc, setup_orc
     assert not any(c.argv[0] == "xargs" for c in setup_orca.runner.commands)
     failing = make_fake_proc(setup_orca.tmp / "bad-proc", {43: "file"})
     done = setup_orca.remove(proc_root=str(failing))
-    assert done.status == "kept" and "process scan failed" in done.reason
+    # a scan that cannot be read is a lookup failure, not a verdict
+    assert done.status == "failed" and "process scan failed" in done.reason
+    assert not any(c.argv[0] == "xargs" for c in setup_orca.runner.commands)
+
+
+def _assert_nothing_cleared_or_removed(setup, done, why):
+    assert done.status == "failed", (done.status, done.reason)
+    assert why in done.reason, done.reason
+    verbs = setup.verbs()
+    assert not any(
+        v.startswith(("xargs", "worktree remove", "worktree rm")) for v in verbs
+    )
+    assert (
+        setup.case.path / ".dev" / "tasks" / "a b.md"
+    ).exists() or not setup.case.path.exists()
+
+
+def test_a_git_status_that_cannot_be_read_after_the_close_is_a_failure(wc, setup_orca):
+    path = setup_orca.case.path
+
+    def breaks_the_checkout(argv, cwd):
+        (path / ".git").rename(path / ".git-off")  # git no longer finds a repo here
+        return result(wc)
+
+    setup_orca.orca_replies[("terminal", "close")] = breaks_the_checkout
+    done = setup_orca.remove()
+    _assert_nothing_cleared_or_removed(
+        setup_orca, done, "git status could not be read after the terminals were closed"
+    )
+
+
+def test_a_folder_that_vanishes_during_the_close_is_a_failure(wc, setup_orca):
+    path = setup_orca.case.path
+
+    def folder_unreadable(argv, cwd):
+        os.rename(path, str(path) + "-moved")
+        return result(wc)
+
+    setup_orca.orca_replies[("terminal", "close")] = folder_unreadable
+    done = setup_orca.remove()
+    _assert_nothing_cleared_or_removed(
+        setup_orca, done, "the folder could not be read after the terminals were closed"
+    )
+
+
+def test_a_head_that_cannot_be_read_after_the_close_is_a_failure(
+    wc, setup_orca, monkeypatch
+):
+    inp, pr = setup_orca.inputs()
+    real = wc.gather_facts
+
+    def headless(runner, wt, orca=None):
+        return dataclasses.replace(real(runner, wt, orca), head=None)
+
+    monkeypatch.setattr(
+        wc, "gather_facts", headless
+    )  # the only read left is the re-check
+    done = setup_orca.remove(inp, pr)
+    _assert_nothing_cleared_or_removed(
+        setup_orca, done, "HEAD could not be read after the terminals were closed"
+    )
+
+
+def test_a_saved_file_that_cannot_be_read_at_the_re_check_is_a_failure(wc, setup_orca):
+    path = setup_orca.case.path
+
+    def saved_file_becomes_a_folder(argv, cwd):
+        saved = path / ".dev" / "tasks" / "a b.md"
+        saved.unlink()
+        saved.mkdir()  # still there, but its bytes cannot be read
+        return result(wc)
+
+    setup_orca.orca_replies[("terminal", "close")] = saved_file_becomes_a_folder
+    done = setup_orca.remove()
+    assert done.status == "failed", (done.status, done.reason)
+    assert "a saved file could not be read" in done.reason
+    assert not any(v.startswith("xargs") for v in setup_orca.verbs())
+
+
+def test_an_unknown_relation_to_the_pull_request_at_the_re_check_is_a_failure(
+    wc, setup_orca, monkeypatch
+):
+    inp, pr = setup_orca.inputs()
+    monkeypatch.setattr(
+        wc, "commits_after_pr", lambda *a, **k: wc.AfterPr("unknown", None, "no clone")
+    )
+    done = setup_orca.remove(inp, pr)
+    assert (done.status, done.reason) == ("failed", "re-check failed: no clone")
+    assert not any(v.startswith("xargs") for v in setup_orca.verbs())
+
+
+def test_a_first_decision_that_could_not_read_a_fact_is_a_failure_not_a_verdict(
+    wc, setup_orca
+):
+    inp, pr = setup_orca.inputs()
+    unreadable = dataclasses.replace(
+        inp,
+        after=wc.AfterPr(
+            "unknown", None, "HEAD or the pull request's last commit is not known"
+        ),
+    )
+    done = setup_orca.remove(unreadable, pr)
+    assert (
+        done.status == "failed" and done.reason == "HEAD is not the pull request's head"
+    )
+    assert setup_orca.runner.commands == []  # nothing ran: no save, no close, no clear
 
 
 def test_a_failed_save_stops_before_anything_else(
diff --git a/tests/worktree_cleanup/test_verbs.py b/tests/worktree_cleanup/test_verbs.py
index 010d686c6..cb2f36aad 100644
--- a/tests/worktree_cleanup/test_verbs.py
+++ b/tests/worktree_cleanup/test_verbs.py
@@ -6,6 +6,7 @@ Git runs on throwaway repositories under ``tmp_path`` with a local bare evidence
 
 from __future__ import annotations
 
+import dataclasses
 import hashlib
 import json
 import os
@@ -583,3 +584,93 @@ def test_output_files_that_cannot_be_written_give_exit_69_after_the_table(
     shown = capsys.readouterr()
     assert "summary:" in shown.out  # the table and the summary were printed first
     assert "the output files could not be written" in shown.err
+
+
+# -- a fact that cannot be read at the re-check is a failure (exit 69); a change is a plain "kept" -----------------------
+
+
+def _break_the_recheck(wc, world, monkeypatch, case):
+    """Let the first read of the worktree through; make the read after the save fail."""
+    plain = str(world.paths["plain"])
+    if case == "scan":
+        calls = []
+        real_scan = wc.scan_processes
+
+        def scan(*a, **k):
+            calls.append(1)
+            return (
+                real_scan(*a, **k)
+                if len(calls) == 1
+                else wc.ProcScan(False, failure="x")
+            )
+
+        monkeypatch.setattr(wc, "scan_processes", scan)
+        return
+    seen = []
+    real = wc.gather_facts
+
+    def facts(runner, wt, orca=None):
+        got = real(runner, wt, orca)
+        if wt.path != plain:
+            return got
+        seen.append(1)
+        if len(seen) == 1:
+            return got
+        if case == "status":
+            return dataclasses.replace(got, state=None)
+        return dataclasses.replace(got, present=False)
+
+    monkeypatch.setattr(wc, "gather_facts", facts)
+
+
+@pytest.mark.parametrize("case", ["status", "folder", "scan"])
+def test_prune_apply_exits_69_when_the_re_check_cannot_read_a_fact(
+    wc, world, capsys, monkeypatch, case
+):
+    world.add("plain", dev=False)
+    _break_the_recheck(wc, world, monkeypatch, case)
+    assert world.run("prune", "--apply") == 69
+    shown = capsys.readouterr().out
+    assert "failed 1" in shown
+    doc = json.loads(next(world.out.glob("prune-*.json")).read_text())
+    assert {r["folder"]: r["decision"] for r in doc["rows"]}["plain"] == "failed"
+    assert doc["summary"]["failed"] == 1
+    assert world.paths["plain"].exists()
+    assert world.removal_commands() == []
+
+
+@pytest.mark.parametrize("case", ["status", "folder", "scan"])
+def test_retire_apply_exits_69_when_the_re_check_cannot_read_a_fact(
+    wc, world, capsys, monkeypatch, case
+):
+    world.add("plain", dev=False)
+    _break_the_recheck(wc, world, monkeypatch, case)
+    assert world.run("retire", "plain", "--apply") == 69
+    assert world.paths["plain"].exists() and world.removal_commands() == []
+
+
+def test_a_real_change_during_the_terminal_close_is_still_kept(wc, world, capsys):
+    world.add("done")
+    world.listed = {"done"}
+    path = world.paths["done"]
+
+    def busy(argv, cwd):
+        key = tuple(argv[1:3])
+        if key == ("worktree", "ps"):
+            rows = [{"worktreeId": "id-done", "path": str(path), "isPinned": False,
+                     "liveTerminalCount": 1, "lastActivityAt": None, "linkedPR": None, "comment": ""}]  # fmt: skip
+            return wc.Result(
+                0, json.dumps({"ok": True, "result": {"worktrees": rows}}), ""
+            )
+        if key == ("terminal", "close"):
+            write(path / "made-by-the-terminal.txt")  # an agent was still working
+            return wc.Result(0, "", "")
+        return World.orca(world, argv, cwd)
+
+    world.runner.replies["orca"] = busy
+    assert world.run("prune", "--apply") == 0
+    assert "changed since the terminals were closed" in capsys.readouterr().out
+    assert path.exists()
+    assert not any(c[:2] == ["xargs", "-0"] for c in world.removal_commands())
+    assert world.run("retire", "done", "--apply") == 64
+    assert path.exists()

Earlier blocking findings of this start (empty on the first review): F1.5 sev=blocking trigger=B1 ac=T12.AC3 at=scripts/worktree_cleanup.py:2458 anchor="69 lookup or removal failure" chk=y,n,n,n family=exit-code-recheck fix=when the re-check after the terminals are closed cannot read a fact (git status gives None, the process scan fails, or the relation to the pull request is unknown), have remove_worktree return a failed status so prune counts it in failed and retire exits 69 first=A1 origin=late: remove_worktree returns kept for an unreadable re-check, so prune --apply exits 0 with failed 0 and retire exits 64.

Saved-probe re-check hit locations (may be empty): 2408:        return RemovalResult("failed" if first.unread else "kept", first.reason)
2411:        return RemovalResult(
2422:            return RemovalResult("failed", saved.reason, tuple(steps))
2437:            return RemovalResult(
2449:    unreadable = ""
2451:        unreadable = "the folder could not be read"
2453:        unreadable = "git status could not be read"
2455:        unreadable = "HEAD could not be read"
2460:                unreadable = "a saved file could not be read"
2462:    if unreadable:
2463:        return RemovalResult(
2465:            f"re-check failed: {unreadable} after the terminals were closed",
2478:    if after.relation == "unknown":
2479:        return RemovalResult(
2481:            f"re-check failed: {after.reason}",
2485:    if changed or after.relation not in ("same", "ancestor"):
2486:        return RemovalResult(
2494:        return RemovalResult(
2501:        return RemovalResult(
2517:            return RemovalResult(
2534:        return RemovalResult(
2546:        return RemovalResult("failed", problem, tuple(steps), branch_note, verified)
2548:    return RemovalResult("removed", "", tuple(steps), branch_note, verified)


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
