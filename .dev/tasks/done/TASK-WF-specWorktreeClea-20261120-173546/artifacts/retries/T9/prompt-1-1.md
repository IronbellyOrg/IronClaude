bcbec7b3496ae617b63e13242967471cef806251
Review one task for spec compliance.

Task brief: ## Task 9: Implement the `.dev` archive step with the names-only secret check

Depends on: Task 6

In `scripts/worktree_cleanup.py` implement source section 7 as one function used by the `archive` verb and by `retire` and `prune`. Order: needs the merged pull request of rule 2 and refuses without one; syncs the local clone of the evidence repo (`RUN_EVIDENCE_DIR`, cloned when missing with the repo from `RUN_EVIDENCE_REPO`; `git fetch` and fast-forward); builds the folder inside a scratch folder in that clone and, when complete, renames it into place (a failed save leaves its scratch folder, named in the log, and deletes nothing); copies untracked files that are not ignored at their relative paths into `files/`; packs the ignored files under `.dev/` (not `__pycache__`) into `ignored.tar.gz`, split into parts of the 85 MB module constant when larger; writes `saved-paths.txt` (one exact path per line: every untracked file copied and every file inside the archive, read back with `tar -tzf`, files only) and `MANIFEST.md` (source repo, branch, pull request link and title, merge date, worktree head and pull request head, worktree folder, time saved, count of files, SHA-256 of each archive part and of `saved-paths.txt`); commits with the message `archive(<repo>): <date> pr<N> <subject>`; runs `git fetch`, rebases onto `origin/main` when it moved, pushes, and on a refused push repeats from the fetch up to 3 times then fails with "saved copy failed: push refused"; verifies with `git fetch`, the same file count on `origin/main` and `git diff --quiet origin/main -- <folder>`, and prints `VERIFIED <folder> files=<n>`; the push uses `git -c credential.helper='!gh auth git-credential'` with only the environment `GH_TOKEN` and a failure to authenticate reads "saved copy failed: no credentials in the environment". Folder convention: `<source-repo>/<pr-author>/<YYYY-MM-DD>_pr<number>_<subject>/` with the UTC merge date and the branch name without the author prefix, slashes turned into hyphens. A repeat run verifies an existing folder again and checks every file now in the worktree is covered; new files go to a second folder with suffix `-r2` then `-r3`; an existing folder is never overwritten. Before copying, a names-only secret check scans the files to be saved for token-shaped content and secret-looking file names; a hit stops the save with "possible secret in <file name>" and never prints or logs the matched value. The step reads and copies and never edits anything inside the worktree. The function returns the verified folder path and the set of saved paths so Task 11 can register them with the runner.

Acceptance criteria:
- Run against a throwaway worktree and a local bare repository, the folder appears at `<repo>/<author>/<date>_pr<N>_<subject>/` with `MANIFEST.md` (all fields above), `files/`, `ignored.tar.gz` and `saved-paths.txt`, and `VERIFIED <folder> files=<n>` is returned.
- A refused push (three times), a folder that differs after the push and a failed copy each return a failure reason beginning "saved copy failed" and leave the worktree untouched.
- With the part size lowered by the test, an ignored archive is split into parts that join back to the same bytes; a second run with new files writes `-r2` and the first folder is byte-identical afterwards.
- A file containing a token-shaped string stops the save, the message names the file, and the string itself appears nowhere in the output, the log or the evidence clone.

AC ids (in source order): T9.AC1, T9.AC2, T9.AC3, T9.AC4
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
Start sha: bcbec7b3496ae617b63e13242967471cef806251
Diff against the start snapshot: diff --git a/scripts/worktree_cleanup.py b/scripts/worktree_cleanup.py
deleted file mode 100644
index 7176027af..000000000
--- a/scripts/worktree_cleanup.py
+++ /dev/null
@@ -1,1891 +0,0 @@
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
-import json
-import os
-import re
-import shlex
-import shutil
-import subprocess
-import sys
-from collections.abc import Callable, Mapping, Sequence
-from dataclasses import dataclass, field
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
-            if tail == ["origin/main"]:
-                return
-            raise RefusedCommand("git rebase is allowed only as: rebase origin/main")
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
diff --git a/tests/worktree_cleanup/test_runner.py b/tests/worktree_cleanup/test_runner.py
deleted file mode 100644
index 11e3de64f..000000000
--- a/tests/worktree_cleanup/test_runner.py
+++ /dev/null
@@ -1,641 +0,0 @@
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


===== new file: tests/worktree_cleanup/test_archive.py =====
"""The .dev archive step (Task 9; Task 10 adds the remaining cases).

Everything runs in throwaway repositories under ``tmp_path`` with local bare remotes. No
test pushes to a network remote or reads a credential file. Token-shaped test strings are
built at run time from two pieces, so no secret-looking literal is committed.
"""

from __future__ import annotations

import dataclasses
import hashlib
import os
from pathlib import Path

import pytest

from .conftest import git_in
from .test_facts import facts_for, write

AUTHOR = "example-user"
MERGED = "2026-11-10T12:00:00Z"
BASE = "IronClaude/example-user/2026-11-10_pr700_topic"
UNSET = object()


@pytest.fixture(autouse=True)
def git_identity(monkeypatch):
    """The evidence commit needs an identity; the throwaway one never leaves the tests."""
    for key, value in {
        "GIT_AUTHOR_NAME": "t",
        "GIT_AUTHOR_EMAIL": "t@example.invalid",
        "GIT_COMMITTER_NAME": "t",
        "GIT_COMMITTER_EMAIL": "t@example.invalid",
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_CONFIG_NOSYSTEM": "1",
    }.items():
        monkeypatch.setenv(key, value)


def make_pr(wc, **change):
    base = dict(
        number=700, state="MERGED", head_oid="b" * 40, author=AUTHOR, merged_at=MERGED,
        title="Example title", body="", closing=(), branch=f"{AUTHOR}/topic",
    )  # fmt: skip
    base.update(change)
    return wc.PullRequest(**base)


class Case:
    """A throwaway worktree with .dev files, an evidence bare repo and a clone path."""

    def __init__(self, wc, runner_cls, repo, evidence_bare, tmp_path, replies=None):
        self.wc, self.bare = wc, evidence_bare
        self.clone = str(tmp_path / "evidence-clone")
        self.runner = runner_cls(evidence_dir=self.clone, replies=replies)
        self.path = repo.add_worktree("topic")
        write(self.path / ".dev" / "tasks" / "a b.md", "report\n")
        write(self.path / ".dev" / "local" / "run.log", "log line\n")
        write(self.path / ".dev" / "local" / "__pycache__" / "x.pyc", "skipped\n")
        self.repo, self.runner_cls = repo, runner_cls
        self.notes: list[str] = []

    def facts(self):
        _, facts = facts_for(self.wc, self.runner_cls, self.repo, self.path)
        return dataclasses.replace(
            facts, origin=self.wc.OriginInfo("IronbellyOrg", "IronClaude")
        )

    def run(self, pr=UNSET, facts=None):
        return self.wc.archive_worktree(
            self.runner, facts or self.facts(), make_pr(self.wc) if pr is UNSET else pr,
            self.clone, str(self.bare), log=self.notes.append,
        )  # fmt: skip

    def snapshot(self):
        """Every file of the worktree with its hash: unchanged means the step touched nothing."""
        seen = {}
        for dirpath, _dirs, names in os.walk(self.path):
            if ".git" in Path(dirpath).parts:
                continue
            for name in names:
                full = os.path.join(dirpath, name)
                seen[os.path.relpath(full, self.path)] = hashlib.sha256(
                    Path(full).read_bytes()
                ).hexdigest()
        return seen

    def remote_files(self, folder):
        out = git_in(self.bare, "ls-tree", "-r", "--name-only", "main", folder)
        return [n for n in out.splitlines() if n]


@pytest.fixture
def case(wc, runner_cls, throwaway_repo, evidence_bare, tmp_path):
    return Case(wc, runner_cls, throwaway_repo, evidence_bare, tmp_path)


def tree_digest(folder: Path):
    return {
        str(p.relative_to(folder)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(folder.rglob("*"))
        if p.is_file()
    }


# -- the saved folder ---------------------------------------------------------------------------


def test_the_folder_appears_with_every_part_and_is_verified(case):
    before = case.snapshot()
    result = case.run()
    assert result.ok, result.reason
    assert result.folder == BASE
    folder = Path(case.clone) / BASE
    assert {p.name for p in folder.iterdir()} == {
        "MANIFEST.md",
        "files",
        "ignored.tar.gz",
        "saved-paths.txt",
    }
    assert (folder / "files" / ".dev" / "tasks" / "a b.md").read_text() == "report\n"
    saved = (folder / "saved-paths.txt").read_text().splitlines()
    assert saved == [
        ".dev/local/run.log",
        ".dev/tasks/a b.md",
    ]  # the pycache file is not saved
    assert result.saved_paths == frozenset(saved)
    n = sum(1 for p in folder.rglob("*") if p.is_file())
    assert result.verified == f"VERIFIED {BASE} files={n}" and result.files == n
    assert len(case.remote_files(BASE)) == n  # the same files are on origin/main
    assert case.snapshot() == before  # the worktree is untouched
    manifest = (folder / "MANIFEST.md").read_text()
    for field in (
        "source repo: IronbellyOrg/IronClaude", "branch: topic",
        "[#700 Example title](https://github.com/IronbellyOrg/IronClaude/pull/700)",
        "merge date: 2026-11-10", f"worktree head: {case.facts().head}", f"pull request head: {'b' * 40}",
        f"worktree folder: {case.path}", "saved at (UTC): ", "files saved: 2",
        "ignored.tar.gz", "saved-paths.txt",
    ):  # fmt: skip
        assert field in manifest, field
    for name in ("ignored.tar.gz", "saved-paths.txt"):
        digest = hashlib.sha256((folder / name).read_bytes()).hexdigest()
        assert f"| {name} | {digest} |" in manifest


def test_the_commit_message_follows_the_convention(case):
    assert case.run().ok
    subject = git_in(case.bare, "log", "-1", "--format=%s", "main").strip()
    assert subject == "archive(IronClaude): 2026-11-10 pr700 topic"


def test_the_step_refuses_without_a_merged_pull_request_and_with_nothing_to_save(
    wc, case
):
    for pr in (None, make_pr(wc, state="OPEN"), make_pr(wc, state="CLOSED")):
        result = case.run(pr=pr)
        assert (
            not result.ok
            and result.reason == "saved copy failed: no merged pull request"
        )
    assert not Path(case.clone).exists()
    empty = dataclasses.replace(case.facts(), state=wc.LocalState())
    result = case.run(facts=empty)
    assert result.ok and result.verified == "nothing to save" and result.folder == ""


def test_a_pull_request_without_an_author_or_merge_date_is_refused(wc, case):
    for change in ({"author": ""}, {"merged_at": None}, {"merged_at": "yesterday"}):
        result = case.run(pr=make_pr(wc, **change))
        assert result.reason.startswith(
            "saved copy failed: the pull request has no author"
        )


def test_the_branch_prefix_is_dropped_only_when_it_is_the_author(wc):
    pr = make_pr(wc, branch="example-user/docs-354-x/y")
    assert (
        wc.folder_name(pr, "IronbellyOrg/IronClaude")[0]
        == "IronClaude/example-user/2026-11-10_pr700_docs-354-x-y"
    )
    pr = make_pr(wc, branch="someone-else/docs-354")
    assert wc.folder_name(pr, "IronbellyOrg/IronClaude")[1] == "someone-else-docs-354"


# -- failures: each starts with "saved copy failed" and leaves the worktree alone --------------------


def _result(wc, code, out="", err=""):
    return wc.Result(code, out, err)


def test_a_push_refused_three_times_fails_with_push_refused(
    wc, runner_cls, throwaway_repo, evidence_bare, tmp_path
):
    pushes = []

    def handler(argv, cwd):
        if "push" in argv:
            pushes.append(argv)
            return _result(wc, 1, "", "! [rejected] main -> main (fetch first)")
        return None

    c = Case(
        wc,
        runner_cls,
        throwaway_repo,
        evidence_bare,
        tmp_path,
        replies={"git": handler},
    )
    before = c.snapshot()
    result = c.run()
    assert not result.ok and result.reason == "saved copy failed: push refused"
    assert len(pushes) == 3
    assert pushes[0][:4] == ["git", "-c", wc.CREDENTIAL_HELPER, "push"]
    assert c.snapshot() == before
    assert c.remote_files(BASE) == []  # nothing reached the remote


def test_a_push_that_fails_to_authenticate_names_the_credentials(
    wc, runner_cls, throwaway_repo, evidence_bare, tmp_path
):
    def handler(argv, cwd):
        if "push" in argv:
            return _result(
                wc,
                128,
                "",
                "fatal: could not read Username for 'https://x.invalid': terminal prompts disabled",
            )
        return None

    c = Case(
        wc,
        runner_cls,
        throwaway_repo,
        evidence_bare,
        tmp_path,
        replies={"git": handler},
    )
    result = c.run()
    assert result.reason == "saved copy failed: no credentials in the environment"


def test_a_refused_push_that_succeeds_on_the_second_try_after_a_rebase(
    wc, runner_cls, throwaway_repo, evidence_bare, tmp_path
):
    seen = {"n": 0}

    def handler(argv, cwd):
        if "push" in argv:
            seen["n"] += 1
            if seen["n"] == 1:
                return _result(wc, 1, "", "! [rejected]")
        return None

    c = Case(
        wc,
        runner_cls,
        throwaway_repo,
        evidence_bare,
        tmp_path,
        replies={"git": handler},
    )
    result = c.run()
    assert result.ok and seen["n"] == 2
    assert len(c.remote_files(BASE)) == result.files


@pytest.mark.parametrize(
    "verb,answer,reason",
    [
        ("diff", (1, "", ""), "saved copy failed: the copy differs from origin/main"),
        (
            "ls-tree",
            (0, "one\0", ""),
            "saved copy failed: the copy on origin/main has a different file count",
        ),
    ],
)
def test_a_folder_that_differs_after_the_push_fails(
    wc, runner_cls, throwaway_repo, evidence_bare, tmp_path, verb, answer, reason
):
    def handler(argv, cwd):
        return _result(wc, *answer) if verb in argv else None

    c = Case(
        wc,
        runner_cls,
        throwaway_repo,
        evidence_bare,
        tmp_path,
        replies={"git": handler},
    )
    before = c.snapshot()
    result = c.run()
    assert not result.ok and result.reason == reason
    assert c.snapshot() == before


def test_a_failed_copy_leaves_a_named_scratch_folder_and_the_worktree_untouched(
    wc, case, monkeypatch
):
    def broken(src, dst, **kw):
        raise OSError("disk full")

    monkeypatch.setattr(wc.shutil, "copy2", broken)
    before = case.snapshot()
    result = case.run()
    assert result.reason == "saved copy failed: copy failed (OSError)"
    assert result.scratch and Path(result.scratch).is_dir()
    assert result.scratch in " ".join(case.notes)  # the log names it
    assert not (Path(case.clone) / BASE).exists()
    assert case.snapshot() == before


def test_the_evidence_clone_that_cannot_be_made_is_a_failure(
    wc, runner_cls, throwaway_repo, tmp_path
):
    c = Case(wc, runner_cls, throwaway_repo, tmp_path / "no-such-repo.git", tmp_path)
    result = c.run()
    assert result.reason == "saved copy failed: the evidence repo could not be cloned"


# -- split archives, repeats and -r2 ----------------------------------------------------------------


def test_a_large_ignored_archive_is_split_into_parts_that_join_back(
    wc, case, monkeypatch
):
    monkeypatch.setattr(wc, "ARCHIVE_PART_BYTES", 2048)
    blob = os.urandom(
        10_000
    )  # does not compress, so the archive is larger than one part
    (case.path / ".dev" / "local" / "big.bin").write_bytes(blob)
    result = case.run()
    assert result.ok, result.reason
    folder = Path(case.clone) / result.folder
    parts = sorted(p for p in folder.iterdir() if ".part-" in p.name)
    assert len(parts) >= 5 and not (folder / "ignored.tar.gz").exists()
    assert all(p.stat().st_size <= 2048 for p in parts)
    joined = b"".join(p.read_bytes() for p in parts)
    import io
    import tarfile

    with tarfile.open(fileobj=io.BytesIO(joined), mode="r:gz") as tar:
        assert tar.extractfile(".dev/local/big.bin").read() == blob
    assert set(wc.archive_parts(str(folder))) == {str(p) for p in parts}
    manifest = (folder / "MANIFEST.md").read_text()
    assert all(
        f"| {p.name} | {hashlib.sha256(p.read_bytes()).hexdigest()} |" in manifest
        for p in parts
    )
    assert ".dev/local/big.bin" in (folder / "saved-paths.txt").read_text()


def test_a_repeat_run_verifies_and_a_run_with_new_files_writes_r2(wc, case):
    first = case.run()
    assert first.ok and first.folder == BASE
    before = tree_digest(Path(case.clone) / BASE)
    commits = git_in(case.bare, "rev-list", "--count", "main").strip()
    again = case.run()
    assert again.ok and again.folder == BASE and again.verified == first.verified
    assert (
        git_in(case.bare, "rev-list", "--count", "main").strip() == commits
    )  # nothing new pushed
    write(case.path / ".dev" / "tasks" / "later.md", "new\n")
    second = case.run()
    assert second.ok and second.folder == f"{BASE}-r2"
    assert (
        tree_digest(Path(case.clone) / BASE) == before
    )  # the first folder is byte-identical
    saved = (
        (Path(case.clone) / second.folder / "saved-paths.txt").read_text().splitlines()
    )
    assert saved == [".dev/tasks/later.md"]
    assert second.saved_paths == frozenset(
        {".dev/local/run.log", ".dev/tasks/a b.md", ".dev/tasks/later.md"}
    )
    assert (
        git_in(case.bare, "log", "-1", "--format=%s", "main")
        .strip()
        .endswith("topic-r2")
    )
    third = case.run()
    assert (
        third.ok and third.folder == f"{BASE}-r2"
    )  # covered by the two folders together


def test_a_file_changed_since_the_save_is_saved_again_not_assumed_covered(wc, case):
    assert case.run().ok
    write(case.path / ".dev" / "tasks" / "a b.md", "edited after the save\n")
    result = case.run()
    assert result.ok and result.folder == f"{BASE}-r2"
    assert (
        Path(case.clone) / result.folder / "files" / ".dev" / "tasks" / "a b.md"
    ).read_text() == "edited after the save\n"
    assert (
        Path(case.clone) / BASE / "files" / ".dev" / "tasks" / "a b.md"
    ).read_text() == "report\n"


def test_an_existing_folder_is_never_overwritten_and_three_is_the_limit(wc, case):
    assert case.run().ok
    for name in ("two", "three", "four"):
        write(case.path / ".dev" / "tasks" / f"{name}.md", name)
        result = case.run()
        if name == "four":
            assert (
                result.reason
                == "saved copy failed: this pull request already has three saved folders"
            )
        else:
            assert result.ok
    assert sorted(p.name for p in (Path(case.clone) / "IronClaude" / AUTHOR).iterdir() if not p.name.startswith(".")) == [
        "2026-11-10_pr700_topic", "2026-11-10_pr700_topic-r2", "2026-11-10_pr700_topic-r3",
    ]  # fmt: skip


# -- the names-only secret check -----------------------------------------------------------------------


def token_like(prefix="gh" + "p_"):
    return (
        prefix + "A1b2C3d4" * 4
    )  # assembled at run time; no literal token is committed


def test_a_token_shaped_string_stops_the_save_and_is_never_shown(wc, case, capsys):
    secret = token_like()
    (case.path / ".dev" / "local" / "notes.log").write_text(
        f"line\nkey = {secret}\n", encoding="utf-8"
    )
    before = case.snapshot()
    result = case.run()
    assert not result.ok
    assert result.reason == "saved copy failed: possible secret in .dev/local/notes.log"
    assert secret not in result.reason and secret not in " ".join(case.notes)
    out = capsys.readouterr()
    assert secret not in out.out and secret not in out.err
    assert case.snapshot() == before
    # the evidence clone was never made, and so cannot hold the value; any file of it is clean too
    assert not Path(case.clone).exists()
    for p in Path(case.clone).rglob("*") if Path(case.clone).exists() else []:
        if p.is_file():
            assert secret.encode() not in p.read_bytes()
    assert case.remote_files(BASE) == []


def test_the_secret_check_finds_a_token_split_across_read_blocks(wc, tmp_path):
    secret = token_like()
    path = tmp_path / "f.log"
    path.write_bytes(b"x" * ((1 << 20) - 10) + secret.encode() + b"y" * 50)
    assert wc.file_has_secret(str(path)) is True
    clean = tmp_path / "clean.log"
    clean.write_bytes(b"x" * ((1 << 20) + 5000))
    assert wc.file_has_secret(str(clean)) is False


@pytest.mark.parametrize(
    "prefix", ["github" + "_pat_", "sk" + "-", "AKIA", "xox" + "b-"]
)
def test_other_token_shapes_are_found(wc, tmp_path, prefix):
    path = tmp_path / "f.txt"
    tail = (
        "A1B2C3D4E5F6G7H8J9K0L1M2N3O4P5Q6R7S8"
        if prefix != "AKIA"
        else "A1B2C3D4E5F6G7H8"
    )
    path.write_text(f"v = {prefix}{tail}\n", encoding="utf-8")
    assert wc.file_has_secret(str(path))


@pytest.mark.parametrize(
    "name",
    [
        ".dev/.env",
        ".dev/x/.env.local",
        ".dev/id_rsa",
        ".dev/k.pem",
        ".dev/a.key",
        ".dev/credentials.json",
        ".dev/secrets.yaml",
        ".dev/.netrc",
    ],
)
def test_secret_looking_file_names_stop_the_save(wc, case, name):
    write(case.path / name, "harmless\n")
    result = case.run(
        facts=dataclasses.replace(case.facts(), state=_with_ignored(wc, case, name))
    )
    assert result.reason == f"saved copy failed: possible secret in {name}"


def _with_ignored(wc, case, name):
    state = case.facts().state
    return dataclasses.replace(state, untracked_dev=[*state.untracked_dev, name])


def test_ordinary_file_names_and_text_do_not_trip_the_check(wc, tmp_path):
    for name in (
        ".dev/tasks/report.md",
        ".dev/keys-notes.md",
        ".dev/skeleton.txt",
        ".dev/environment.md",
    ):
        assert not wc.SECRET_NAME_RE.search(name), name
    path = tmp_path / "ok.md"
    path.write_text(
        "a branch called ghp_x and sk-short are not tokens\n", encoding="utf-8"
    )
    assert not wc.file_has_secret(str(path))


def test_only_plain_regular_files_are_saved(wc, case):
    link = case.path / ".dev" / "tasks" / "link.md"
    link.symlink_to(case.path / ".dev" / "tasks" / "a b.md")
    state = case.facts().state
    state = dataclasses.replace(
        state, untracked_dev=[*state.untracked_dev, ".dev/tasks/link.md"]
    )
    result = case.run(facts=dataclasses.replace(case.facts(), state=state))
    assert (
        result.reason == "saved copy failed: .dev/tasks/link.md is not a regular file"
    )
    bad = dataclasses.replace(case.facts().state, untracked_dev=[".dev/../README.md"])
    assert case.run(
        facts=dataclasses.replace(case.facts(), state=bad)
    ).reason.startswith("saved copy failed: unusable file name")


def test_the_step_never_runs_a_command_the_runner_would_refuse(wc, case):
    assert case.run().ok
    verbs = {
        tuple(c.argv[:2]) if c.argv[0] != "git" else tuple(c.argv[1:2])
        for c in case.runner.commands
    }
    assert not any(
        "-D" in c.argv or "--force" in c.argv or "-f" in c.argv
        for c in case.runner.commands
    )
    assert ("add",) in verbs and ("commit",) in verbs and ("tar", "-tzf") in verbs


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
