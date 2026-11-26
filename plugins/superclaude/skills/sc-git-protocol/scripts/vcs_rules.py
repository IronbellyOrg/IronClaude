"""Safety constants and the argv allow-list table of the read-only ``vcs`` helper.

This file is the single source for the rules the ``sc-git-protocol`` refs repeat in
prose (a parity test compares the two). It uses the Python standard library only.

``ALLOWED`` maps each git verb the helper may run to the option tokens it may carry.
``validate_argv`` checks an argv (the verb first, without the ``git`` program name or
its global options) against the table and raises ``ForbiddenArgv`` before any process
starts. A verb alone is not enough: an option outside the table is refused, so a
write form of an allowed verb (a branch delete, a config unset, a ref write through
the symbolic-ref verb, ``hash-object -w``) never gets through.

Table entries:
  * an option token matches exactly; a token that ends in ``=`` matches as a prefix
    (``--porcelain=`` allows ``--porcelain=v2``);
  * words that do not start with ``-`` are values (revisions, paths) and are allowed,
    up to ``max_positionals`` when that is set;
  * ``one_of`` lists options of which at least one is required (the read form);
  * ``subcommand`` is a required first word (``submodule status``);
  * ``needs_index`` verbs (``read-tree``, ``add``, ``write-tree``) run only when a
    private index file outside ``.git/`` is named, so the person's own index is never
    touched.

``FORBIDDEN_FLAGS`` is a separate rule: it applies to every argv the helper prints for
the agent to run (``validate_agent_argv``). The runner's own private-index calls may
use the add verb with ``-A`` (the snapshot method needs it); a printed argv never may.
"""

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple, Optional, Sequence

# The `LL-PROTECTED` set of the launch-level guard. At run time the helper adds the
# target of refs/remotes/origin/HEAD; a resolved default only adds, never removes.
PROTECTED_BRANCHES = ("master", "main", "integration")

# The forbidden-flag list of FR-030. "-n" is the commit short option for no-verify and
# "." is a pathspec; both are matched by validate_agent_argv.
FORBIDDEN_FLAGS = (
    "--no-verify",
    "-n",
    "--amend",
    "--force",
    "-f",
    "-D",
    "--delete",
    "-A",
    "--all",
    ".",
    "-a",
    "--allow-empty",
    "--no-edit",
    "--remote",
    "--recurse-submodules=on-demand",
    "--discard-changes",
)

# Files under the project agent-host folder that may be staged.
DEV_MIRROR_ALLOW = ("settings.json",)

# The higher of 2.23 (the switch verb) and the git version that supports
# --pathspec-from-file for both add and commit. 2.25 is UNVERIFIED: the preflight task
# tests the claim on the installed git; a stated fact needs that passing test.
MIN_GIT = (2, 25)


class ForbiddenArgv(Exception):
    """An argv names a verb or option outside the allow-list, or breaks a safety rule."""


class _Spec(NamedTuple):
    options: frozenset = frozenset()
    max_positionals: Optional[int] = None
    one_of: frozenset = frozenset()
    subcommand: Optional[str] = None
    needs_index: bool = False


def _spec(
    options=(), max_positionals=None, one_of=(), subcommand=None, needs_index=False
):
    return _Spec(
        frozenset(options),
        max_positionals,
        frozenset(one_of),
        subcommand,
        needs_index,
    )


ALLOWED = {
    "rev-parse": _spec(
        [
            "--show-toplevel",
            "--show-prefix",
            "--show-cdup",
            "--show-superproject-working-tree",
            "--git-dir",
            "--git-common-dir",
            "--absolute-git-dir",
            "--git-path",
            "--is-inside-work-tree",
            "--is-bare-repository",
            "--abbrev-ref",
            "--symbolic-full-name",
            "--verify",
            "--quiet",
            "-q",
            "--short",
            "--path-format=",
        ]
    ),
    # Two words would write a symbolic ref, so at most one value is allowed.
    "symbolic-ref": _spec(["--short", "-q", "--quiet"], max_positionals=1),
    "status": _spec(
        [
            "--porcelain",
            "--porcelain=",
            "-z",
            "--branch",
            "-b",
            "--short",
            "-s",
            "--ignore-submodules=",
            "--untracked-files=",
            "-uall",
            "-unormal",
            "-uno",
            "--no-renames",
            "--renames",
            "--ahead-behind",
            "--no-ahead-behind",
        ]
    ),
    "diff": _spec(
        [
            "--name-only",
            "--name-status",
            "--numstat",
            "--stat",
            "--shortstat",
            "--raw",
            "--cached",
            "--staged",
            "--exit-code",
            "--quiet",
            "-z",
            "--no-renames",
            "--no-ext-diff",
            "--no-textconv",
            "--no-color",
            "--binary",
            "--full-index",
            "--ignore-submodules=",
            "--diff-filter=",
        ]
    ),
    "ls-files": _spec(
        [
            "-z",
            "--cached",
            "-c",
            "--others",
            "-o",
            "--modified",
            "-m",
            "--deleted",
            "-d",
            "--ignored",
            "-i",
            "--exclude-standard",
            "--stage",
            "-s",
            "--error-unmatch",
            "--full-name",
            "--eol",
            "--directory",
            "--no-empty-directory",
        ]
    ),
    "ls-tree": _spec(
        [
            "-r",
            "-t",
            "-d",
            "-z",
            "-l",
            "--long",
            "--name-only",
            "--name-status",
            "--full-name",
            "--full-tree",
            "--object-only",
            "--abbrev",
            "--abbrev=",
        ]
    ),
    "cat-file": _spec(["-e", "-t", "-s", "-p", "--batch", "--batch-check", "--buffer"]),
    "check-ignore": _spec(
        ["-q", "--quiet", "-v", "--verbose", "-n", "-z", "--stdin", "--no-index"]
    ),
    # Only the read forms; an unset, add or set form has no --get option. --file reads
    # the .gitmodules of the work tree (the one-of rule keeps it a read).
    "config": _spec(
        [
            "--get",
            "--get-regexp",
            "--file",
            "--local",
            "--worktree",
            "--show-origin",
            "-z",
            "--null",
        ],
        one_of=["--get", "--get-regexp"],
    ),
    "submodule": _spec(["--cached"], subcommand="status"),
    "for-each-ref": _spec(
        [
            "--contains",
            "--no-contains",
            "--merged",
            "--no-merged",
            "--points-at",
            "--format=",
            "--sort=",
            "--count=",
        ]
    ),
    "rev-list": _spec(
        [
            "--count",
            "--max-count=",
            "--skip=",
            "--parents",
            "--first-parent",
            "--left-right",
            "--reverse",
            "--merges",
            "--no-merges",
            "--ancestry-path",
            "--boundary",
        ]
    ),
    "log": _spec(
        [
            "--format=",
            "--pretty=",
            "--max-count=",
            "--skip=",
            "-n",
            "-z",
            "--oneline",
            "--name-only",
            "--name-status",
            "--first-parent",
            "--merges",
            "--no-merges",
            "--reverse",
            "--no-color",
            "--no-decorate",
            "--no-ext-diff",
            "--no-textconv",
            "--date=",
        ]
    ),
    "merge-base": _spec(["--is-ancestor"], max_positionals=2, one_of=["--is-ancestor"]),
    "branch": _spec(["--show-current"], max_positionals=0, one_of=["--show-current"]),
    # No -w: the helper never writes an object through this verb.
    "hash-object": _spec(["--stdin", "--path=", "--no-filters", "-t"]),
    # `git version` and the `--version` form; no other option.
    "version": _spec(max_positionals=0),
    # Private-index verbs: run only when a private index file outside .git/ is named.
    "read-tree": _spec(["--empty"], needs_index=True),
    "add": _spec(
        ["-A", "-u", "--ignore-errors", "--pathspec-from-file=", "--pathspec-file-nul"],
        needs_index=True,
    ),
    "write-tree": _spec(max_positionals=0, needs_index=True),
}


def _matches(token: str, options: frozenset) -> bool:
    return token in options or any(
        o.endswith("=") and token.startswith(o) for o in options
    )


def _check_index_file(verb: str, index_file: Optional[str]) -> None:
    if not index_file:
        raise ForbiddenArgv(f"{verb}: needs a private index file (none named)")
    if ".git" in Path(index_file).parts:
        raise ForbiddenArgv(
            f"{verb}: the private index must be outside .git/: {index_file}"
        )


def validate_argv(argv: Sequence[str], *, index_file: Optional[str] = None) -> None:
    """Raise ``ForbiddenArgv`` unless ``argv`` (verb first) fits the ``ALLOWED`` table.

    ``index_file`` is the private ``GIT_INDEX_FILE`` the caller will set, if any.
    """
    words = list(argv)
    if not words:
        raise ForbiddenArgv("empty argv")
    verb = "version" if words[0] == "--version" else words[0]
    spec = ALLOWED.get(verb)
    if spec is None:
        raise ForbiddenArgv(f"verb not allowed: {words[0]}")
    if spec.needs_index:
        _check_index_file(verb, index_file)
    rest = words[1:]
    if spec.subcommand is not None:
        if not rest or rest[0] != spec.subcommand:
            raise ForbiddenArgv(f"{verb}: only the {spec.subcommand} form is allowed")
        rest = rest[1:]
    seen, positionals, past_dd = set(), 0, False
    for token in rest:
        if past_dd or not token.startswith("-") or token == "-":
            positionals += 1
        elif token == "--":
            past_dd = True
        elif _matches(token, spec.options):
            seen.add(token)
        else:
            raise ForbiddenArgv(f"{verb}: option not allowed: {token}")
    if spec.max_positionals is not None and positionals > spec.max_positionals:
        raise ForbiddenArgv(f"{verb}: too many values")
    if spec.one_of and not (seen & spec.one_of):
        raise ForbiddenArgv(f"{verb}: needs one of {sorted(spec.one_of)}")


# Options whose next word is a value (a message or a file), not a flag.
_VALUE_OPTIONS = ("-m", "-F", "--message", "--file")
_FORBIDDEN_SHORT = {f[1] for f in FORBIDDEN_FLAGS if len(f) == 2 and f[0] == "-"}


def validate_agent_argv(argv: Sequence[str]) -> None:
    """Raise ``ForbiddenArgv`` when an argv printed for the agent holds a forbidden flag.

    Checks every token of ``FORBIDDEN_FLAGS``: long options also by their name before
    ``=``, short options inside a cluster such as ``-am``, and ``.`` as a pathspec.
    Words after ``--`` are paths, so only ``.`` is checked there; the word after a
    message or file option is a value and is skipped.
    """
    past_dd = skip = False
    for token in argv:
        if past_dd:
            if token == ".":
                raise ForbiddenArgv("forbidden pathspec: .")
            continue
        if token == "--":
            past_dd = True
        elif skip:
            skip = False
        elif token in _VALUE_OPTIONS:
            skip = True
        elif token in FORBIDDEN_FLAGS:
            raise ForbiddenArgv(f"forbidden flag: {token}")
        elif token.startswith("--"):
            if token.split("=", 1)[0] in FORBIDDEN_FLAGS:
                raise ForbiddenArgv(f"forbidden flag: {token}")
        elif token.startswith("-") and len(token) > 2:
            if _FORBIDDEN_SHORT & set(token[1:]):
                raise ForbiddenArgv(f"forbidden flag in cluster: {token}")
