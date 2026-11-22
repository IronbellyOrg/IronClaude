ecb11d4e9bd0ff8c6a0a18828c506d3204b88c82
Review one task for spec compliance.

Task brief: ## Task 6: Implement the eight rules in order, with their reasons and the table row

Depends on: Task 5

In `scripts/worktree_cleanup.py` add one decision function that takes the facts of Tasks 3 to 5 plus a save state (`not needed`, `needed`, `verified`, `failed: <why>`) and returns a decision (`removable` or `kept`), the first failed rule and its plain-English reason, and the table row. Apply the eight rules of source section 6 in that order with exactly the reasons shown there: rule 1 (main checkout, not our repo, this is where the script runs, locked, folder missing reported only, name guard, detached HEAD), rule 2 (no pull request, open, closed not merged, landed check UNKNOWN), rule 3 (N commits after the pull request, HEAD is not the pull request's head), rule 4 (issue open, issue lookup failed), rule 5 (changed tracked files, untracked files outside `.dev`, ignored local state with names, `.dev` files allowed only when the save state is `verified`, else "saved copy failed: <why>"), rule 6 (a process inside tolerated only while the worktree has Orca terminals open; otherwise "in use: process <pid> (<name>)"; a failed `/proc` scan keeps everything; holds another checkout; git operation in progress), rule 7 (idle fewer than the floor days, created within the floor days), rule 8 (pinned in Orca, keep file present). Every rule fails closed: a fact that could not be read keeps the worktree. In a dry run a worktree that passes with untracked or ignored `.dev/` files shows `removable` with the saved-copy cell `needed`, and one with Orca terminals open shows the note "its Orca terminals will be closed first". The table row has the columns of source section 3: repo, folder, branch, in Orca, pull request and state, issue(s) and state, idle days, size, saved copy, decision and reason. Add the table renderers (markdown and the same rows as JSON).

Acceptance criteria:
- A pure function (no process started) returns the same decision for the same facts, so tests can call it with hand-built facts.
- For every rule, a worktree that fails only that rule is kept with that rule's reason, and the reasons are the strings of source section 6.
- A worktree with only Orca terminals open and a process inside passes rule 6 in the first pass and carries the note "its Orca terminals will be closed first"; a process inside with no Orca terminal fails rule 6.
- The markdown table has the eleven columns above and the JSON has the same rows.

AC ids (in source order): T6.AC1, T6.AC2, T6.AC3, T6.AC4
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
Start sha: ecb11d4e9bd0ff8c6a0a18828c506d3204b88c82
Diff against the start snapshot: diff --git a/scripts/worktree_cleanup.py b/scripts/worktree_cleanup.py
deleted file mode 100644
index 31d1a45f2..000000000
--- a/scripts/worktree_cleanup.py
+++ /dev/null
@@ -1,1611 +0,0 @@
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


===== new file: tests/worktree_cleanup/test_rules.py =====
"""Task 6: the eight rules, their reasons, and the table. All facts are built by hand;
``decide`` is pure, so no process, folder or network is touched here."""

from __future__ import annotations

import dataclasses
import json

import pytest

NOW = 2_000_000_000.0
DAY = 86400.0


@pytest.fixture
def good(wc):
    """Facts for a worktree that passes every rule."""
    wt = wc.GitWorktree(
        "/w/wts/topic", "/w/main", "a" * 40, "topic", False, False, False, False, False
    )
    facts = wc.WorktreeFacts(
        worktree=wt,
        head="a" * 40,
        origin=wc.OriginInfo("IronbellyOrg", "IronClaude"),
        state=wc.LocalState(),
        last_commit_ts=NOW - 20 * DAY,
        git_file_mtime=NOW - 20 * DAY,
        created_ts=NOW - 30 * DAY,
        size_bytes=3 * 1024 * 1024,
        git_dir="/w/main/.git/worktrees/topic",
    )
    pr = wc.PullRequest(
        9, "MERGED", "a" * 40, "x", "2026-11-01T00:00:00Z", "t", "", (), "topic"
    )
    return wc.RuleInputs(
        facts=facts,
        now=NOW,
        pr_lookup=wc.PrLookup(True, pr),
        landed=wc.Landed("MERGED", "installed copy"),
        after=wc.AfterPr("same", 0),
        issues=wc.IssueFacts((), ()),
        procs=wc.ProcScan(True, ()),
    )


def with_facts(wc, inp, **change):
    return dataclasses.replace(inp, facts=dataclasses.replace(inp.facts, **change))


def with_wt(wc, inp, **change):
    wt = dataclasses.replace(inp.facts.worktree, **change)
    return with_facts(wc, inp, worktree=wt)


def orca(wc, **change):
    base = dict(
        worktree_id="w", selector="id:w", path="/w/wts/topic", branch="b", repo="r",
        last_activity_ms=None, is_pinned=False, live_terminal_count=0, linked_pr_hint=None, comment="",
    )  # fmt: skip
    base.update(change)
    return wc.OrcaWorktree(**base)


def state(wc, **change):
    return dataclasses.replace(wc.LocalState(), **change)


def test_a_worktree_that_passes_everything_is_removable(wc, good):
    d = wc.decide(good)
    assert (d.decision, d.rule, d.reason, d.note) == ("removable", None, "", "")
    assert d.saved_copy == "none needed"


def test_decide_is_pure_and_repeatable(wc, good, never_run_runner):
    assert wc.decide(good) == wc.decide(good)
    assert wc.decide(dataclasses.replace(good, own_folder=True)) == wc.decide(
        dataclasses.replace(good, own_folder=True)
    )
    assert never_run_runner.commands == []


def case(wc, good, name):
    """One worktree that fails only one rule: (inputs, rule number, reason)."""
    s = lambda **c: with_facts(wc, good, state=state(wc, **c))  # noqa: E731
    pr = lambda **c: dataclasses.replace(  # noqa: E731
        good, pr_lookup=wc.PrLookup(True, dataclasses.replace(good.pr_lookup.pr, **c))
    )
    cases = {
        "main": (with_wt(wc, good, is_main=True), 1, "main checkout"),
        "origin-not-ours": (with_facts(wc, good, origin=wc.OriginInfo("Other", "x")), 1, "not our repo"),
        "origin-unknown": (with_facts(wc, good, origin=None), 1, "not our repo"),
        "own-folder": (dataclasses.replace(good, own_folder=True), 1, "this is where the script runs"),
        "locked": (with_wt(wc, good, locked=True), 1, "locked"),
        "missing": (with_facts(wc, good, present=False), 1, "folder missing (reported only)"),
        "guard": (with_wt(wc, good, path="/w/wts/orca-port-x"), 1, "on the name guard (infrastructure folder)"),
        "detached": (with_wt(wc, good, detached=True, branch=None), 1, "detached HEAD"),
        "no-pr": (dataclasses.replace(good, pr_lookup=wc.PrLookup(True, None)), 2, "no pull request"),
        "pr-lookup": (dataclasses.replace(good, pr_lookup=wc.PrLookup(False, None, "boom")), 2, "pull request lookup failed: boom"),
        "pr-open": (pr(state="OPEN"), 2, "pull request #9 is open"),
        "pr-closed": (pr(state="CLOSED"), 2, "pull request #9 closed, not merged"),
        "landed-unknown": (dataclasses.replace(good, landed=wc.Landed("UNKNOWN", "x")), 2, "landed check said UNKNOWN"),
        "landed-missing": (dataclasses.replace(good, landed=None), 2, "landed check said UNKNOWN"),
        "landed-open": (dataclasses.replace(good, landed=wc.Landed("OPEN", "x")), 2, "pull request #9 is open"),
        "after-3": (dataclasses.replace(good, after=wc.AfterPr("ahead", 3)), 3, "3 commits after the pull request"),
        "after-1": (dataclasses.replace(good, after=wc.AfterPr("ahead", 1)), 3, "1 commit after the pull request"),
        "after-unknown": (dataclasses.replace(good, after=wc.AfterPr("unknown", None)), 3, "HEAD is not the pull request's head"),
        "after-missing": (dataclasses.replace(good, after=None), 3, "HEAD is not the pull request's head"),
        "issue-open": (
            dataclasses.replace(good, issues=wc.IssueFacts((wc.Issue("o/r", 21, "OPEN", ("x",)),), ())),
            4, "issue #21 is open",
        ),
        "issue-failed": (
            dataclasses.replace(good, issues=wc.IssueFacts((), ("issue lookup failed: o/r#4",))),
            4, "issue lookup failed: o/r#4",
        ),
        "issue-missing": (dataclasses.replace(good, issues=None), 4, "issue lookup failed"),
        "changed": (s(changed_tracked=["a", "b"]), 5, "2 changed tracked files"),
        "untracked": (s(untracked_outside_dev=["a"]), 5, "1 untracked file outside .dev"),
        "ignored-local": (s(ignored_unknown=[".env", "x.key"]), 5, "ignored local state: .env, x.key"),
        "state-unread": (with_facts(wc, good, state=None), 5, "ignored local state: git status could not be read"),
        "save-failed": (
            dataclasses.replace(with_facts(wc, good, state=state(wc, untracked_dev=[".dev/a"])), save_state="failed: push refused"),
            5, "saved copy failed: push refused",
        ),
        "save-unset": (with_facts(wc, good, state=state(wc, ignored_dev=[".dev/a"])), 5, "saved copy failed: no save state for the .dev files"),
        "process": (
            dataclasses.replace(good, procs=wc.ProcScan(True, ((412, "/w/wts/topic/sub", "node"),))),
            6, "in use: process 412 (node)",
        ),
        "scan-failed": (dataclasses.replace(good, procs=wc.ProcScan(False, failure="pid 5: boom")), 6, None),
        "no-scan": (dataclasses.replace(good, procs=None), 6, None),
        "nested": (with_facts(wc, good, nested_checkouts=["inner/.git"]), 6, "holds another checkout"),
        "operation": (with_facts(wc, good, operations=["MERGE_HEAD"]), 6, "git operation in progress"),
        "unread-folder": (with_facts(wc, good, failures=["3 folder entries could not be read"]), 6, "in use: the folder or its git folder could not be read in full"),
        "git-dir-unread": (with_facts(wc, good, git_dir=None), 6, "in use: the folder or its git folder could not be read in full"),
        "missing-real": (with_facts(wc, good, present=False, origin=None, head=None, state=None, git_dir=None), 1, "folder missing (reported only)"),
        "created-unknown": (with_facts(wc, good, created_ts=None), 7, "created time unknown (needs 7)"),
        "idle": (with_facts(wc, good, git_file_mtime=NOW - 2 * DAY, last_commit_ts=NOW - 3 * DAY), 7, "idle 2 days (needs 7)"),
        "idle-unknown": (with_facts(wc, good, git_file_mtime=None, last_commit_ts=None), 7, "idle time unknown (needs 7)"),
        "young": (with_facts(wc, good, created_ts=NOW - 3 * DAY), 7, "created 3 days ago (needs 7)"),
        "pinned": (dataclasses.replace(good, orca=orca(wc, is_pinned=True)), 8, "pinned in Orca"),
        "keep-file": (with_facts(wc, good, keep_file=True), 8, "keep file present"),
    }  # fmt: skip
    return cases[name]


CASE_NAMES = [
    "main", "origin-not-ours", "origin-unknown", "own-folder", "locked", "missing", "guard", "detached",
    "no-pr", "pr-lookup", "pr-open", "pr-closed", "landed-unknown", "landed-missing", "landed-open",
    "after-3", "after-1", "after-unknown", "after-missing", "issue-open", "issue-failed", "issue-missing",
    "changed", "untracked", "ignored-local", "state-unread", "save-failed", "save-unset",
    "process", "scan-failed", "no-scan", "nested", "operation", "unread-folder", "git-dir-unread",
    "missing-real", "created-unknown",
    "idle", "idle-unknown", "young", "pinned", "keep-file",
]  # fmt: skip


@pytest.mark.parametrize("name", CASE_NAMES)
def test_failing_only_one_rule_keeps_the_worktree_with_that_reason(wc, good, name):
    inp, rule, reason = case(wc, good, name)
    d = wc.decide(inp)
    assert d.decision == "kept" and d.rule == rule
    if reason is not None:
        assert d.reason == reason
    else:
        assert d.reason.startswith("in use: the process scan failed")


def test_the_first_failed_rule_is_the_one_shown(wc, good):
    inp = dataclasses.replace(
        with_facts(wc, good, keep_file=True, state=state(wc, changed_tracked=["a"])),
        pr_lookup=wc.PrLookup(True, None),
        own_folder=True,
    )
    d = wc.decide(inp)
    assert (d.rule, d.reason) == (1, "this is where the script runs")
    inp = dataclasses.replace(inp, own_folder=False)
    assert wc.decide(inp).rule == 2
    inp = dataclasses.replace(inp, pr_lookup=good.pr_lookup)
    assert wc.decide(inp).rule == 5


def test_reasons_are_the_strings_of_the_spec(wc):
    """Every reason the spec table names for rules 1 to 8 appears in the rule code."""
    import inspect

    text = (
        inspect.getsource(wc._rule1)
        + inspect.getsource(wc._rule2)
        + inspect.getsource(wc._rule3)
    )
    for words in ("main checkout", "not our repo", "this is where the script runs", "locked",
                  "folder missing (reported only)", "detached HEAD", "no pull request", "is open",
                  "closed, not merged", "landed check said UNKNOWN", "after the pull request",
                  "HEAD is not the pull request's head"):  # fmt: skip
        assert words in text, words
    text = (
        inspect.getsource(wc._rule4)
        + inspect.getsource(wc._rule5)
        + inspect.getsource(wc._rule6)
        + inspect.getsource(wc._rule7)
        + inspect.getsource(wc._rule8)
    )
    for words in ("is open", "issue lookup failed", "changed tracked file", "untracked file", "outside .dev",
                  "ignored local state:", "saved copy failed:", "in use: process", "holds another checkout",
                  "git operation in progress", "(needs", "pinned in Orca", "keep file present"):  # fmt: skip
        assert words in text, words


# -- rule 6: terminals, the save state, the dry run -------------------------------------------------


def test_a_process_inside_with_orca_terminals_open_passes_rule_6_with_the_note(
    wc, good
):
    inside = wc.ProcScan(True, ((7, "/w/wts/topic", "claude"),))
    inp = dataclasses.replace(good, procs=inside, orca=orca(wc, live_terminal_count=2))
    d = wc.decide(inp)
    assert (
        d.decision == "removable"
        and d.note == "its Orca terminals will be closed first"
    )
    # the same process without an Orca terminal fails rule 6
    d = wc.decide(
        dataclasses.replace(good, procs=inside, orca=orca(wc, live_terminal_count=0))
    )
    assert (d.decision, d.rule, d.reason) == ("kept", 6, "in use: process 7 (claude)")
    d = wc.decide(dataclasses.replace(good, procs=inside, orca=None))
    assert (d.rule, d.reason) == (6, "in use: process 7 (claude)")
    # terminals but no process: still the note
    d = wc.decide(dataclasses.replace(good, orca=orca(wc, live_terminal_count=1)))
    assert d.decision == "removable" and d.note == wc.TERMINALS_NOTE
    # terminals do not excuse another checkout or an operation, or a failed scan
    busy = with_facts(wc, good, operations=["index.lock"])
    assert (
        wc.decide(
            dataclasses.replace(
                busy, procs=inside, orca=orca(wc, live_terminal_count=2)
            )
        ).rule
        == 6
    )
    failed = wc.ProcScan(False, failure="x")
    assert (
        wc.decide(
            dataclasses.replace(
                good, procs=failed, orca=orca(wc, live_terminal_count=2)
            )
        ).rule
        == 6
    )


def test_a_process_in_a_sibling_folder_is_not_inside(wc, good):
    near = wc.ProcScan(True, ((7, "/w/wts/topic-2", "x"),))
    assert wc.decide(dataclasses.replace(good, procs=near)).decision == "removable"


@pytest.mark.parametrize(
    "files,save,decision,cell",
    [
        ({}, "not needed", "removable", "none needed"),
        ({"untracked_dev": [".dev/a"]}, "needed", "removable", "needed"),
        ({"ignored_dev": [".dev/a"]}, "verified", "removable", "saved and checked"),
        ({"untracked_dev": [".dev/a"]}, "failed: copy differs", "kept", "failed"),
    ],
)
def test_dev_files_need_a_verified_save_and_the_dry_run_shows_needed(
    wc, good, files, save, decision, cell
):
    inp = dataclasses.replace(
        with_facts(wc, good, state=state(wc, **files)), save_state=save
    )
    d = wc.decide(inp)
    assert (d.decision, d.saved_copy) == (decision, cell)


def test_a_failed_rule_before_the_save_still_shows_the_saved_copy_cell(wc, good):
    inp = dataclasses.replace(
        with_facts(wc, good, state=state(wc, untracked_dev=[".dev/a"])),
        pr_lookup=wc.PrLookup(True, None),
        save_state="needed",
    )
    d = wc.decide(inp)
    assert d.rule == 2 and d.saved_copy == "needed"


# -- the table -----------------------------------------------------------------------------------------


def make_rows(wc, good):
    inp_a = dataclasses.replace(good, orca=orca(wc, live_terminal_count=1))
    inp_b = dataclasses.replace(good, own_folder=True)
    rows = [wc.table_row(i, wc.decide(i), "IronClaude") for i in (inp_a, inp_b)]
    return rows


def test_the_markdown_table_has_the_eleven_columns_and_the_json_the_same_rows(wc, good):
    rows = make_rows(wc, good)
    assert len(wc.TABLE_COLUMNS) == 11
    md = wc.render_markdown(rows).splitlines()
    assert (
        md[0]
        == "| repo | folder | branch | in orca | pull request | issues | idle days | size | saved copy | decision | reason |"
    )
    assert md[1] == "|" + "|".join(["---"] * 11) + "|"
    assert len(md) == 2 + len(rows)
    for line, row in zip(md[2:], rows):
        assert line.count(" | ") == 10
        assert row["decision"] in line and row["folder"] in line
    doc = json.loads(wc.render_json(rows))
    assert doc["columns"] == list(wc.TABLE_COLUMNS)
    assert doc["rows"] == rows
    assert all(set(r) == set(wc.TABLE_COLUMNS) for r in doc["rows"])


def test_row_cells_for_a_removable_and_a_kept_worktree(wc, good):
    a, b = make_rows(wc, good)
    assert a == {
        "repo": "IronClaude", "folder": "topic", "branch": "topic", "in_orca": "yes",
        "pull_request": "#9 MERGED", "issues": "none found", "idle_days": "20.0", "size": "3.0 MB",
        "saved_copy": "none needed", "decision": "removable", "reason": "its Orca terminals will be closed first",
    }  # fmt: skip
    assert (
        b["decision"] == "kept"
        and b["reason"] == "this is where the script runs"
        and b["in_orca"] == "no"
    )


def test_row_cells_for_failed_lookups_and_unknowns(wc, good):
    inp = dataclasses.replace(
        with_facts(
            wc,
            good,
            size_bytes=None,
            git_file_mtime=None,
            last_commit_ts=None,
            worktree=dataclasses.replace(
                good.facts.worktree, detached=True, branch=None
            ),
        ),
        pr_lookup=wc.PrLookup(False, None, "x"),
        issues=wc.IssueFacts(
            (wc.Issue("o/r", 4, "CLOSED", ()),), ("issue lookup failed: o/r#5",)
        ),
    )
    row = wc.table_row(inp, wc.decide(inp))
    assert (
        row["pull_request"],
        row["issues"],
        row["idle_days"],
        row["size"],
        row["branch"],
    ) == (
        "lookup failed",
        "#4 CLOSED, lookup failed",
        "?",
        "?",
        "(detached)",
    )
    assert row["repo"] == "main"
    none = dataclasses.replace(inp, pr_lookup=wc.PrLookup(True, None), issues=None)
    assert wc.table_row(none, wc.decide(none))["issues"] == "lookup failed"
    assert wc.table_row(none, wc.decide(none))["pull_request"] == "none"


def test_markdown_cells_never_break_the_table(wc, good):
    row = dict(make_rows(wc, good)[0], reason="a | b\nc")
    line = wc.render_markdown([row]).splitlines()[2]
    assert line.count("|") == 12 and "\n" not in line.strip()
    assert wc.render_markdown([]).count("\n") == 2


@pytest.mark.parametrize(
    "size,text",
    [
        (None, "?"),
        (0, "0 B"),
        (1023, "1023 B"),
        (1536, "1.5 KB"),
        (5 * 1024**3, "5.0 GB"),
        (3000 * 1024**3, "3000.0 GB"),
    ],
)
def test_size_text(wc, size, text):
    assert wc._size_text(size) == text


Codegraph context: index_state=fresh checked_at=2026-11-20T18:23:04Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-687 projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-687
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep and Read floor for dependents of changed symbols (this task creates new files or edits registration lists; see the diff).

Delta diff from the previous reviewed tree (empty on the first review): diff --git a/scripts/worktree_cleanup.py b/scripts/worktree_cleanup.py
index b4259188a..7176027af 100644
--- a/scripts/worktree_cleanup.py
+++ b/scripts/worktree_cleanup.py
@@ -1602,14 +1602,15 @@ def _rule1(i: RuleInputs) -> str | None:
     wt, f = i.facts.worktree, i.facts
     if wt.is_main:
         return "main checkout"
+    if not f.present:
+        # checked before the origin: a missing folder leaves origin unread
+        return "folder missing (reported only)"
     if f.origin is None or not f.origin.is_ours:
         return "not our repo"
     if i.own_folder:
         return "this is where the script runs"
     if wt.locked:
         return "locked"
-    if not f.present:
-        return "folder missing (reported only)"
     if name_guard(wt.path):
         return "on the name guard (infrastructure folder)"
     if wt.detached or not wt.branch:
@@ -1710,8 +1711,8 @@ def _rule6(i: RuleInputs) -> tuple[str | None, str]:
         return "holds another checkout", ""
     if f.operations:
         return "git operation in progress", ""
-    if any("could not be read" in x for x in f.failures):
-        return "in use: the folder could not be read in full", ""
+    if f.git_dir is None or any("could not be read" in x for x in f.failures):
+        return "in use: the folder or its git folder could not be read in full", ""
     return None, (TERMINALS_NOTE if terminals else "")
 
 
@@ -1722,7 +1723,9 @@ def _rule7(i: RuleInputs) -> str | None:
         return f"idle time unknown (needs {floor})"
     if idle < floor:
         return f"idle {int(idle)} days (needs {floor})"
-    if age is not None and age < floor:
+    if age is None:
+        return f"created time unknown (needs {floor})"
+    if age < floor:
         return f"created {int(age)} days ago (needs {floor})"
     return None
 
diff --git a/tests/worktree_cleanup/test_rules.py b/tests/worktree_cleanup/test_rules.py
index 5b99e7697..8205ae6f4 100644
--- a/tests/worktree_cleanup/test_rules.py
+++ b/tests/worktree_cleanup/test_rules.py
@@ -27,6 +27,7 @@ def good(wc):
         git_file_mtime=NOW - 20 * DAY,
         created_ts=NOW - 30 * DAY,
         size_bytes=3 * 1024 * 1024,
+        git_dir="/w/main/.git/worktrees/topic",
     )
     pr = wc.PullRequest(
         9, "MERGED", "a" * 40, "x", "2026-11-01T00:00:00Z", "t", "", (), "topic"
@@ -130,7 +131,10 @@ def case(wc, good, name):
         "no-scan": (dataclasses.replace(good, procs=None), 6, None),
         "nested": (with_facts(wc, good, nested_checkouts=["inner/.git"]), 6, "holds another checkout"),
         "operation": (with_facts(wc, good, operations=["MERGE_HEAD"]), 6, "git operation in progress"),
-        "unread-folder": (with_facts(wc, good, failures=["3 folder entries could not be read"]), 6, "in use: the folder could not be read in full"),
+        "unread-folder": (with_facts(wc, good, failures=["3 folder entries could not be read"]), 6, "in use: the folder or its git folder could not be read in full"),
+        "git-dir-unread": (with_facts(wc, good, git_dir=None), 6, "in use: the folder or its git folder could not be read in full"),
+        "missing-real": (with_facts(wc, good, present=False, origin=None, head=None, state=None, git_dir=None), 1, "folder missing (reported only)"),
+        "created-unknown": (with_facts(wc, good, created_ts=None), 7, "created time unknown (needs 7)"),
         "idle": (with_facts(wc, good, git_file_mtime=NOW - 2 * DAY, last_commit_ts=NOW - 3 * DAY), 7, "idle 2 days (needs 7)"),
         "idle-unknown": (with_facts(wc, good, git_file_mtime=None, last_commit_ts=None), 7, "idle time unknown (needs 7)"),
         "young": (with_facts(wc, good, created_ts=NOW - 3 * DAY), 7, "created 3 days ago (needs 7)"),
@@ -145,7 +149,8 @@ CASE_NAMES = [
     "no-pr", "pr-lookup", "pr-open", "pr-closed", "landed-unknown", "landed-missing", "landed-open",
     "after-3", "after-1", "after-unknown", "after-missing", "issue-open", "issue-failed", "issue-missing",
     "changed", "untracked", "ignored-local", "state-unread", "save-failed", "save-unset",
-    "process", "scan-failed", "no-scan", "nested", "operation", "unread-folder",
+    "process", "scan-failed", "no-scan", "nested", "operation", "unread-folder", "git-dir-unread",
+    "missing-real", "created-unknown",
     "idle", "idle-unknown", "young", "pinned", "keep-file",
 ]  # fmt: skip
 

Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B1 ac=T6.AC2 at=scripts/worktree_cleanup.py:1605 anchor="a worktree that fails only that rule is kept with that rule's reason" chk=y,n,n,n family=missing-folder-reason fix=in _rule1 test not f.present before the origin test; add a test with origin None and present False covers="the reasons are the strings of source section 6" first=A1 origin=new: a missing folder is reported as "not our repo", not as "folder missing (reported only)".
F1.2 sev=blocking trigger=B4 ac=scope at=scripts/worktree_cleanup.py:1725 anchor="Every rule fails closed: a fact that could not be read keeps the worktree" chk=n,n,n,y family=fail-open-unread-fact fix=in _rule7 return a created time unknown reason when age is None; add a test first=A1 origin=new: created_ts None passes rule 7.
F1.3 sev=blocking trigger=B4 ac=scope at=scripts/worktree_cleanup.py:1713 anchor="Every rule fails closed: a fact that could not be read keeps the worktree" chk=n,n,n,y family=fail-open-unread-fact fix=in _rule6 keep the worktree when git_dir is None; add a test first=A1 origin=new: when git rev-parse --git-dir fails, operations stays empty and rule 6 passes without the git operation check.

Saved-probe re-check hit locations (may be empty): 973:    git_dir: str | None = None
1061:        facts.git_dir = os.path.normpath(os.path.join(wt.path, out.strip()))
1063:    facts.origin = parse_origin(out) if out is not None else None
1074:    if facts.git_dir is not None:
1076:            _mtime(os.path.join(facts.git_dir, name))
1081:        facts.created_ts = _mtime(os.path.join(facts.git_dir, "gitdir")) or _mtime(
1087:            if os.path.exists(os.path.join(facts.git_dir, m))
1605:    if not f.present:
1608:    if f.origin is None or not f.origin.is_ours:
1714:    if f.git_dir is None or any("could not be read" in x for x in f.failures):
1726:    if age is None:


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
