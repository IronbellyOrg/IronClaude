279eeef4a0fe7a43f5fea61dff96307e813d8ebc
Review one task for spec compliance.

Task brief: ## Task 11: Implement the removal pipeline: terminal close, second check, exact-path clear, removal, branch, read back

Depends on: Task 9

In `scripts/worktree_cleanup.py` implement steps 1 to 7 of source section 3 ("What a removal is, in order") for one removable worktree under `--apply`, each step failing closed with the reason shown: save (the archive step of Task 9 when the worktree holds untracked or ignored `.dev/` files; without `VERIFIED` stop); close the Orca terminals only when it has any, only after every other rule passed and the save is verified, with `orca terminal close --worktree id:<id> --all` (an `unverifiable` or failed close keeps the worktree: "Orca terminal close not confirmed"); the second check after the close, re-reading `git status`, the untracked and ignored lists, HEAD against the pull request's head and the process scan, where any change since the save keeps it ("changed since the terminals were closed") and any process still inside keeps it ("a process is still inside after its Orca terminals were closed"); clear exactly the saved files by registering the verified `saved-paths.txt` paths with the `Runner` and running `git clean -f -x --` on those paths through `xargs -0` with `GIT_LITERAL_PATHSPECS=1`, never a path outside the list, never `-d`, never a tracked file; remove the worktree (`orca worktree rm --worktree id:<id>` without `--force` when Orca lists it, else `git worktree remove <path>` without `--force`, run from the repo's main checkout and never from inside the worktree, and a refusal keeps it with the refusal text); remove the local branch with `git branch -d` only (check first whether Orca already removed it; a "not fully merged" refusal after a squash merge is reported as "branch kept", not an error); then read back that the folder is gone and that neither `git worktree list` nor `orca worktree list` shows it. A worktree with tracked edits or a commit after the pull request is never archived, never has terminals closed and is never cleared (decision 2). In a dry run none of these steps runs.

Acceptance criteria:
- The order of recorded commands (asserted by the tests of Task 13) is: archive commands, `orca terminal close`, the re-check reads, `xargs -0 git clean -f -x --`, the removal, `git branch -d`, the read-back reads.
- `git clean` is issued only after `VERIFIED` and only with paths from `saved-paths.txt`; a path not in the list is refused by the runner before any process starts.
- No recorded command contains `--force`, `-D`, `rm`, `worktree prune`, a remote delete or a push outside the evidence clone.
- A worktree with a tracked edit, or a commit after the pull request, produces no archive, no terminal close and no clear.
- When Orca still lists the worktree at the read back, the result is "removed in git but still listed in Orca": a failed row (exit 69), because no deregister command is proven.

AC ids (in source order): T11.AC1, T11.AC2, T11.AC3, T11.AC4, T11.AC5
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
Start sha: 279eeef4a0fe7a43f5fea61dff96307e813d8ebc
Diff against the start snapshot: diff --git a/scripts/worktree_cleanup.py b/scripts/worktree_cleanup.py
deleted file mode 100644
index a72689648..000000000
--- a/scripts/worktree_cleanup.py
+++ /dev/null
@@ -1,2388 +0,0 @@
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
-            True, "", existing[-1], n, every, f"VERIFIED {existing[-1]} files={n}"
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
-    return ArchiveResult(True, "", folder, n, every, f"VERIFIED {folder} files={n}")
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


===== new file: tests/worktree_cleanup/test_removal.py =====
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
from .test_archive import UNSET, Case, git_identity, make_pr  # noqa: F401 - the fixture is autouse
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
    assert done.status == "kept" and "process scan failed" in done.reason


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
