"""Entry point of the read-only ``vcs`` helper (FR-010, FR-012, NFR-006 to NFR-009).

Run it as ``uv run --no-project python <skill-dir>/scripts/vcs.py <verb> ...``. Every
verb prints one JSON object through ``emit`` and the exit code is:

  * 0   JSON was printed, whatever its ``status`` (a refusal is a result, not a failure);
  * 64  usage error (unknown verb or option); nothing is printed on stdout;
  * 69  a lookup failed (git missing, a timeout, a directory that cannot be entered,
        an unexpected git exit code); the reason goes to stderr, nothing to stdout.

Every object carries ``vcs_contract: "1"`` (a reader that sees another value refuses
with ``helper-missing``, NFR-009), ``verb``, ``status`` and ``reason``.

``emit`` is the single printing place (NFR-006, NFR-007): keys are sorted, no field is
dropped, a list longer than 200 entries is cut to 200 and the top-level ``truncated``
flag is set, and an object whose JSON is above 64 KiB is replaced by a short refusal
(``output-too-large``). The cap is for display only; a verb that needs the full list
(the commit set) writes it to a file, never to this JSON.

``preflight`` (design section 4.3) reports the facts the protocols check before a
local-history write. It names its refusal in ``reason`` in this order: ``detached-head``,
``protected-branch``, ``operation-in-progress``, ``index-locked``, ``git-too-old``
(FR-032). A missing ``refs/remotes/origin/HEAD`` is a ``notice``, not a refusal.

``check-message --file <f> [--implement]`` judges a drafted commit message with the rule
of ``vcs_plan.check_message`` (FR-039, FR-066): ``ok``, or ``refused`` with the violated
rule in ``reason`` and ``rule`` and the header length in ``header_len``. It writes
nothing; a file that cannot be read is exit 69.

``submodules [--cwd <dir>]`` prints ``superproject {branch, head}``, ``config``, ``warnings``
and ``rows`` (FR-040 to FR-042; the columns are listed in ``vcs_submodules``): one row per
top-level registered submodule, sorted by path, each with its ``state`` and the ``update``
and ``commit_pointer`` eligibility objects. It reads with a person-invoked runner, so only
a line the person typed (``/sc:git submodule status`` and the other submodule lines) may
call it. It writes nothing; outside a repository it is ``refused`` with ``not-a-repo``.

``snapshot_lossless`` is false when a content filter would change what a snapshot of
the work tree stores. The exact list: any config key ``filter.<name>.clean``,
``filter.<name>.smudge`` or ``filter.<name>.process`` (the long-running form of the
same filter), or ``core.autocrlf`` equal to ``true``. ``core.autocrlf=input`` and other
filter keys such as ``required`` do not count.

``stage-plan [--path <p>...] [--cwd <dir>]`` (path mode) plans the add and the commit of the named repository-relative paths, or,
with no path, a pathless commit of the index as the person staged it (FR-031, FR-035,
FR-038, FR-062 c to e, FR-063). It prints ``commit_paths``, ``skipped [{path, why}]``,
``add_argv`` and ``commit_argv`` (the words after ``git``), ``message_path`` and
``pathspec_file {path, content, sha256}`` (the agent writes both files outside the work
tree; the helper writes none), ``s_count`` and ``truncated``. ``status`` is ``ok``,
``nothing`` or ``refused``; a refusal prints no argv. A path may start with ``-``: give it
as ``--path=-name``. It writes nothing.

``stage-plan --ledger <file> --run-dir <dir> [--package <dir>] [--candidate]`` (ledger
mode; FR-060, FR-062, FR-073 to FR-076, FR-108) finds the one boundary of the implement
ledger that needs a commit and plans it: ``key``, ``attempt``, ``parent``, ``tasks``,
``commit_paths`` (S), the argv and the pathspec file (``commit-paths-<key>-a<n>.txt``
beside the sidecar). Refusals: ``no-due-boundary``, ``out-of-protocol``, ``unsettled``,
``ledger-corrupt``, ``sidecar-corrupt``, ``sidecar-mismatch``, the path refusals and the
checks ``no-snapshot``, ``branch-unproven``, ``branch-changed``, ``head-moved``,
``foreign-change``, ``no-accepted-tree`` and ``changed-after-review`` (with ``paths``).
``--candidate`` runs after the prepared line and prints ``candidate_tree`` (parent plus
S, built in a private index; ``pin-conflict`` when ``boundary_ref`` exists with another
target). Relative paths are read from ``--cwd``. It writes no ref, index entry or file.

``verify --key <64 hex> --attempt <n> --parent <40 hex> --candidate-ref <ref>
--worktree-ref <ref> --exit <int> [--ledger <f>] [--sidecar <f>]`` (FR-036, FR-108,
FR-113, FR-130) says what the history proves for one prepared attempt: ``status`` is
``committed`` (with ``sha``), ``pending`` (HEAD is the parent), one of the classes
``blocked-by-host``, ``hook-failed``, ``hook-rewrite``, ``hook-rewrite-evidence``,
``hook-rewrite-committed``, ``hook-rewrite-pinned`` or ``commit-error``, ``uncertain``
(``reason`` names the missing proof), ``interrupted`` (``--exit`` above 128, not
classified) or ``refused`` (``unknown-attempt``, ``parent-mismatch``, ``sidecar-corrupt``).
``--exit`` is the commit call's shell status; give -1 when a host hook refused the call
(``--exit=-1``). Every result carries ``head_before``, ``head_after``, ``proof``, and the
outside-S comparison: ``outside`` (``unchanged``, ``outside-changed``,
``outside-unverified``, ``deferred`` or ``not-compared``), ``outside_changed`` (the full
count) and ``outside_paths``. The rewrite classes with a tree also print ``rewritten_tree``
and ``rewritten_ref``. S is the ``commit-paths-<key>-a<n>.txt`` file beside the sidecar.
It writes nothing and retries nothing.

``reconcile --ledger <f> --sidecar <f> --run-dir <d> [--package <d>] --flag on|off``
(FR-102 to FR-108, FR-132, DD-5) says what every boundary of the implement ledger is and
the one action this run may take. ``--flag`` says whether this invocation carries
``--commit-tasks``. It prints ``boundaries`` (each with ``key``, ``label``, ``members``,
``state``, ``action``, ``reason``, ``parent``, ``head``, ``attempt``, ``next_attempt``,
``sha`` for ``record-recovered``, and ``paths`` and ``detail`` when a retry is denied),
``runs`` and ``segments`` (the sidecar lines it used and the ledger lines each covers) and
``no_grant_lines``; or ``status`` ``refused`` with ``sidecar-corrupt``, ``sidecar-mismatch``,
``ledger-corrupt`` or ``plan-changed``. The agent performs only the named action: ``prepare``
and ``retry`` go to ``stage-plan``, ``record-recovered`` and ``record-skipped`` are one
appended line, the three ``stop-*`` actions end the run with the owner's choices, ``none``
needs nothing. ``--sidecar`` must be the ``commits.md`` of the run (a missing file is read
as no sidecar). It writes nothing.

``resolve-check --key <hex or unique prefix> --ledger <f> --sidecar <f> [--run-dir <d>]
[--package <d>]`` (FR-120 to FR-126, FR-116) says which owner answers may be recorded for
an unsettled boundary. It prints ``key``, ``label``, ``members``, ``state``, ``choices``
(``abandon`` always, then ``adopt`` when it holds), ``basis`` (``candidate`` or
``accepted``), ``differs`` (paths of S whose object id, mode or presence differ between
the basis tree and HEAD; null when the tree is unavailable), ``head``, ``parent``,
``attempt``, ``quiescent`` and ``quiescence``. ``status`` ``ok`` offers at least ``abandon``;
when ``adopt`` is not offered ``reason`` is ``adopt-not-descendant`` or ``adopt-unverifiable``
(``detail`` says why). ``status`` ``refused`` offers nothing: ``unknown-boundary``,
``ambiguous-key``, ``already-settled``, ``prefix-too-short`` (a prefix below 12 characters,
not in the design's list) and the refusals of ``reconcile`` for a corrupt ledger or sidecar
or a changed plan. Without ``--run-dir`` and ``--package`` the layout is read from the
paths (``<package>/artifacts/commits.md`` beside ``<package>/progress.md`` is managed). It
writes nothing; the executor appends the one ``resolved`` line.

Python 3.10 or later, standard library only.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

from vcs_plan import (
    GitRunner,
    LookupFailed,
    check_message,
    plan_ledger,
    plan_stage,
    reconcile,
    refused_message,
    resolve_check,
    verify_commit,
)
from vcs_rules import MIN_GIT, PROTECTED_BRANCHES
from vcs_submodules import collect_submodules

CONTRACT = "1"
MAX_LIST = 200
MAX_BYTES = 64 * 1024
EXIT_USAGE = 64
EXIT_LOOKUP = 69

ORIGIN_HEAD = "refs/remotes/origin/HEAD"
ORIGIN_PREFIX = "refs/remotes/origin/"
# The marker kinds of FR-010, each with the names that git keeps for it.
OPERATION_MARKERS = (
    ("merge", ("MERGE_HEAD",)),
    ("rebase", ("rebase-merge", "rebase-apply")),
    ("cherry-pick", ("CHERRY_PICK_HEAD",)),
    ("revert", ("REVERT_HEAD",)),
    ("bisect", ("BISECT_LOG",)),
)
_FILTER_KEY = re.compile(r"^filter\.[^\s]+\.(clean|smudge|process)$", re.IGNORECASE)
_VERSION = re.compile(r"(\d+)\.(\d+)(?:\.(\d+))?")


# --- the one printing place -------------------------------------------------------------
def _cap(value: Any) -> Tuple[Any, bool]:
    """Return ``value`` with every list cut to ``MAX_LIST`` and whether any was cut."""
    if isinstance(value, dict):
        capped = False
        out = {}
        for key, item in value.items():
            out[key], hit = _cap(item)
            capped = capped or hit
        return out, capped
    if isinstance(value, (list, tuple)):
        items, capped = [], len(value) > MAX_LIST
        for item in list(value)[:MAX_LIST]:
            new, hit = _cap(item)
            items.append(new)
            capped = capped or hit
        return items, capped
    return value, False


def emit_text(obj: Dict[str, Any]) -> str:
    """The JSON line ``emit`` prints for ``obj`` (the same input gives the same bytes)."""
    body, capped = _cap(obj)
    body["vcs_contract"] = CONTRACT
    body["truncated"] = bool(body.get("truncated")) or capped
    text = json.dumps(body, sort_keys=True)
    size = len(text.encode("ascii"))
    if size > MAX_BYTES:
        text = json.dumps(
            {
                "reason": "output-too-large",
                "size": size,
                "status": "refused",
                "truncated": False,
                "vcs_contract": CONTRACT,
                "verb": obj.get("verb"),
            },
            sort_keys=True,
        )
    return text + "\n"


def emit(obj: Dict[str, Any], stream=None) -> int:
    """Print ``obj`` as one JSON line and return the exit code (always 0)."""
    (stream or sys.stdout).write(emit_text(obj))
    return 0


# --- preflight --------------------------------------------------------------------------
def _ask(
    git: GitRunner, argv: Sequence[str], ok: Tuple[int, ...] = (0,)
) -> Tuple[int, str]:
    """Run one read; any exit code outside ``ok`` (a timeout included) is a failed lookup."""
    rc, out = git.run(argv)
    if rc not in ok:
        raise LookupFailed(f"git {argv[0]} exited {rc}")
    return rc, out


def _config_value(git: GitRunner, key: str) -> Optional[str]:
    rc, out = _ask(git, ["config", "--get", key], ok=(0, 1))
    return out.rstrip("\n") if rc == 0 else None


def _git_path(git: GitRunner, name: str) -> str:
    _, out = _ask(git, ["rev-parse", "--git-path", name])
    return os.path.join(git.top, out.rstrip("\n"))


def _operation_in_progress(git: GitRunner) -> Optional[str]:
    for kind, names in OPERATION_MARKERS:
        if any(os.path.exists(_git_path(git, name)) for name in names):
            return kind
    return None


def _parse_version(text: str) -> Optional[Tuple[int, ...]]:
    found = _VERSION.search(text)
    if not found:
        return None
    return tuple(int(n) for n in found.groups() if n is not None)


def _snapshot_lossless(git: GitRunner) -> bool:
    rc, out = _ask(git, ["config", "--get-regexp", r"^filter\."], ok=(0, 1))
    if rc == 0:
        for line in out.splitlines():
            if _FILTER_KEY.match(line.split(None, 1)[0]):
                return False
    return (_config_value(git, "core.autocrlf") or "").strip().lower() != "true"


def _origin_head_target(git: GitRunner) -> Optional[str]:
    """The branch name ``refs/remotes/origin/HEAD`` points at, when that ref resolves."""
    rc, out = _ask(git, ["symbolic-ref", "-q", ORIGIN_HEAD], ok=(0, 1))
    if rc != 0:
        return None
    rc, _ = _ask(git, ["rev-parse", "--verify", "--quiet", ORIGIN_HEAD], ok=(0, 1))
    target = out.strip()
    if rc != 0 or not target.startswith(ORIGIN_PREFIX):
        return None
    return target[len(ORIGIN_PREFIX) :]


def run_preflight(
    cwd: str, make_runner: Callable[..., GitRunner] = GitRunner
) -> Dict[str, Any]:
    """Collect the preflight facts for the repository that holds ``cwd``.

    ``make_runner`` builds the git runner (a test passes a subclass). Raises
    ``LookupFailed`` when a read cannot be completed; an OS error (git missing, a
    directory that cannot be entered) passes through for the caller to map to 69.
    """
    rc, out = make_runner(cwd).run(["rev-parse", "--show-toplevel"])
    if rc == 128:  # not a repository, or a bare one (no work tree)
        return {
            "vcs_contract": CONTRACT,
            "verb": "preflight",
            "status": "refused",
            "reason": "not-a-repo",
        }
    if rc != 0:
        raise LookupFailed(f"git rev-parse exited {rc}")
    top = out.rstrip("\n")
    git = make_runner(top)

    _, name = _ask(git, ["branch", "--show-current"])
    branch = name.strip() or None
    rc, ref = _ask(git, ["symbolic-ref", "-q", "HEAD"], ok=(0, 1))
    symbolic_ref = ref.strip() if rc == 0 else None
    detached = symbolic_ref is None

    default = _origin_head_target(git)
    if detached:
        protected = {"value": True, "reason": "detached-head"}
    elif branch in PROTECTED_BRANCHES:
        protected = {"value": True, "reason": "protected-name"}
    elif default is not None and branch == default:
        protected = {"value": True, "reason": "origin-head-target"}
    else:
        protected = {"value": False, "reason": "not-protected"}

    operation = _operation_in_progress(git)
    index_lock = os.path.exists(_git_path(git, "index.lock"))
    _, version_text = _ask(git, ["--version"])
    version = _parse_version(version_text)
    min_ok = version is not None and version >= MIN_GIT

    refusals = (
        ("detached-head", detached),
        ("protected-branch", protected["value"] and not detached),
        ("operation-in-progress", operation is not None),
        ("index-locked", index_lock),
        ("git-too-old", not min_ok),
    )
    reason = next((token for token, hit in refusals if hit), None)
    notice = None
    if default is None:
        notice = (
            "default branch unknown: refs/remotes/origin/HEAD is not set; protected "
            f"names: {', '.join(PROTECTED_BRANCHES)}. Local fix: "
            "git remote set-head origin <branch>"
        )
    return {
        "vcs_contract": CONTRACT,
        "verb": "preflight",
        "status": "refused" if reason else "ok",
        "reason": reason,
        "top": top,
        "branch": branch,
        "symbolic_ref": symbolic_ref,
        "detached": detached,
        "protected": protected,
        "operation_in_progress": operation,
        "index_lock": index_lock,
        "hooks_path": _config_value(git, "core.hooksPath"),
        "submodule_recurse": _config_value(git, "submodule.recurse"),
        "push_recurse_submodules": _config_value(git, "push.recurseSubmodules"),
        "git_version": ".".join(map(str, version)) if version else None,
        "min_git_ok": min_ok,
        "default_branch_known": default is not None,
        "notice": notice,
        "snapshot_lossless": _snapshot_lossless(git),
    }


def _cmd_preflight(args: argparse.Namespace) -> Dict[str, Any]:
    return run_preflight(args.cwd, make_runner=GitRunner)


# --- check-message ----------------------------------------------------------------------
def run_check_message(path: str, implement: bool = False) -> Dict[str, Any]:
    """Read the message file ``path`` and judge it (the rule is ``vcs_plan.check_message``).

    A file that cannot be read raises ``OSError`` (exit 69). Bytes that are not UTF-8
    are refused with the rule ``encoding``; the header is counted on a lossy decode.
    """
    with open(path, "rb") as handle:
        raw = handle.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        header = raw.decode("utf-8", errors="replace").split("\n", 1)[0]
        result = refused_message(
            "encoding", len(header), "the message file is not valid UTF-8"
        )
    else:
        result = check_message(text, implement=implement)
    result["vcs_contract"] = CONTRACT
    return result


def _cmd_check_message(args: argparse.Namespace) -> Dict[str, Any]:
    return run_check_message(args.file, implement=args.implement)


# --- submodules -------------------------------------------------------------------------
def run_submodules(
    cwd: str, make_runner: Callable[..., GitRunner] = GitRunner
) -> Dict[str, Any]:
    """Collect the submodule rows of the repository that holds ``cwd``.

    The runner is person-invoked: the dirty flags need ``--ignore-submodules=none``.
    """
    rc, out = make_runner(cwd, person_invoked=True).run(
        ["rev-parse", "--show-toplevel"]
    )
    if rc == 128:  # not a repository, or a bare one (no work tree)
        return {
            "vcs_contract": CONTRACT,
            "verb": "submodules",
            "status": "refused",
            "reason": "not-a-repo",
        }
    if rc != 0:
        raise LookupFailed(f"git rev-parse exited {rc}")
    git = make_runner(out.rstrip("\n"), person_invoked=True)
    return {
        "vcs_contract": CONTRACT,
        "verb": "submodules",
        "status": "ok",
        "reason": None,
        **collect_submodules(git),
    }


def _cmd_submodules(args: argparse.Namespace) -> Dict[str, Any]:
    return run_submodules(args.cwd, make_runner=GitRunner)


# --- stage-plan -------------------------------------------------------------------------
def run_stage_plan(
    cwd: str,
    paths: Optional[Sequence[str]],
    make_runner: Callable[..., GitRunner] = GitRunner,
    *,
    ledger: Optional[str] = None,
    run_dir: Optional[str] = None,
    package: Optional[str] = None,
    candidate: bool = False,
) -> Dict[str, Any]:
    """Plan the add and the commit of ``paths`` (None: a pathless commit) for ``cwd``'s repository.

    With ``ledger`` (and ``run_dir``, ``package``, ``candidate``) it plans ledger mode
    instead; relative arguments are read from ``cwd``.
    """
    rc, out = make_runner(cwd).run(["rev-parse", "--show-toplevel"])
    if rc == 128:  # not a repository, or a bare one (no work tree)
        return {
            "vcs_contract": CONTRACT,
            "verb": "stage-plan",
            "status": "refused",
            "reason": "not-a-repo",
        }
    if rc != 0:
        raise LookupFailed(f"git rev-parse exited {rc}")
    git = make_runner(out.rstrip("\n"))
    if ledger is not None:

        def resolve(p: str) -> str:
            return os.path.abspath(os.path.join(cwd, p))

        body = plan_ledger(
            git,
            resolve(ledger),
            resolve(run_dir),
            resolve(package) if package is not None else None,
            candidate,
        )
    else:
        body = plan_stage(git, paths)
    return {"vcs_contract": CONTRACT, "verb": "stage-plan", **body}


def _cmd_stage_plan(args: argparse.Namespace) -> Dict[str, Any]:
    paths = None if args.path is None else [p for group in args.path for p in group]
    return run_stage_plan(
        args.cwd,
        paths,
        make_runner=GitRunner,
        ledger=args.ledger,
        run_dir=args.run_dir,
        package=args.package,
        candidate=args.candidate,
    )


# --- verify -----------------------------------------------------------------------------
def run_verify(
    cwd: str,
    key: str,
    attempt: int,
    parent: str,
    candidate_ref: str,
    worktree_ref: str,
    exit_code: Optional[int] = None,
    ledger: Optional[str] = None,
    sidecar: Optional[str] = None,
    make_runner: Callable[..., GitRunner] = GitRunner,
) -> Dict[str, Any]:
    """Ask what the history proves for one prepared attempt (``vcs_plan.verify_commit``).

    Relative ``ledger`` and ``sidecar`` paths are read from ``cwd``.
    """
    rc, out = make_runner(cwd).run(["rev-parse", "--show-toplevel"])
    if rc == 128:  # not a repository, or a bare one (no work tree)
        return {
            "vcs_contract": CONTRACT,
            "verb": "verify",
            "status": "refused",
            "reason": "not-a-repo",
        }
    if rc != 0:
        raise LookupFailed(f"git rev-parse exited {rc}")
    git = make_runner(out.rstrip("\n"))

    def resolve(p: Optional[str]) -> Optional[str]:
        return os.path.abspath(os.path.join(cwd, p)) if p else None

    body = verify_commit(
        git,
        key,
        attempt,
        parent,
        candidate_ref,
        worktree_ref,
        exit_code,
        resolve(ledger),
        resolve(sidecar),
    )
    return {"vcs_contract": CONTRACT, "verb": "verify", **body}


def _cmd_verify(args: argparse.Namespace) -> Dict[str, Any]:
    return run_verify(
        args.cwd,
        args.key,
        args.attempt,
        args.parent,
        args.candidate_ref,
        args.worktree_ref,
        args.exit,
        ledger=args.ledger,
        sidecar=args.sidecar,
        make_runner=GitRunner,
    )


# --- reconcile --------------------------------------------------------------------------
def run_reconcile(
    cwd: str,
    ledger: str,
    sidecar: str,
    run_dir: str,
    package: Optional[str],
    flag: bool,
    make_runner: Callable[..., GitRunner] = GitRunner,
) -> Dict[str, Any]:
    """Reconcile the boundaries of an implement run (``vcs_plan.reconcile``).

    Relative paths are read from ``cwd``.
    """
    rc, out = make_runner(cwd).run(["rev-parse", "--show-toplevel"])
    if rc == 128:  # not a repository, or a bare one (no work tree)
        return {
            "vcs_contract": CONTRACT,
            "verb": "reconcile",
            "status": "refused",
            "reason": "not-a-repo",
        }
    if rc != 0:
        raise LookupFailed(f"git rev-parse exited {rc}")
    git = make_runner(out.rstrip("\n"))

    def resolve(p: str) -> str:
        return os.path.abspath(os.path.join(cwd, p))

    body = reconcile(
        git,
        resolve(ledger),
        resolve(sidecar),
        resolve(run_dir),
        resolve(package) if package is not None else None,
        flag,
    )
    return {"vcs_contract": CONTRACT, "verb": "reconcile", **body}


def _cmd_reconcile(args: argparse.Namespace) -> Dict[str, Any]:
    return run_reconcile(
        args.cwd,
        args.ledger,
        args.sidecar,
        args.run_dir,
        args.package,
        args.flag == "on",
        make_runner=GitRunner,
    )


# --- resolve-check ----------------------------------------------------------------------
def run_resolve_check(
    cwd: str,
    key: str,
    ledger: str,
    sidecar: str,
    run_dir: Optional[str] = None,
    package: Optional[str] = None,
    make_runner: Callable[..., GitRunner] = GitRunner,
) -> Dict[str, Any]:
    """Say which owner answers hold for the boundary ``key`` selects (``vcs_plan.resolve_check``).

    Relative paths are read from ``cwd``.
    """
    rc, out = make_runner(cwd).run(["rev-parse", "--show-toplevel"])
    if rc == 128:  # not a repository, or a bare one (no work tree)
        return {
            "vcs_contract": CONTRACT,
            "verb": "resolve-check",
            "status": "refused",
            "reason": "not-a-repo",
        }
    if rc != 0:
        raise LookupFailed(f"git rev-parse exited {rc}")
    git = make_runner(out.rstrip("\n"))

    def resolve(p: Optional[str]) -> Optional[str]:
        return os.path.abspath(os.path.join(cwd, p)) if p else None

    body = resolve_check(
        git, key, resolve(ledger), resolve(sidecar), resolve(run_dir), resolve(package)
    )
    return {"vcs_contract": CONTRACT, "verb": "resolve-check", **body}


def _cmd_resolve_check(args: argparse.Namespace) -> Dict[str, Any]:
    return run_resolve_check(
        args.cwd,
        args.key,
        args.ledger,
        args.sidecar,
        run_dir=args.run_dir,
        package=args.package,
        make_runner=GitRunner,
    )


# --- argument parsing and dispatch ------------------------------------------------------
def _hex(length: int) -> Callable[[str], str]:
    pattern = re.compile(f"^[0-9a-f]{{{length}}}$")

    def check(value: str) -> str:
        if not pattern.match(value):
            raise argparse.ArgumentTypeError(
                f"expected {length} lower-case hex characters"
            )
        return value

    return check


def _ref(value: str) -> str:
    if not re.match(r"^refs/[A-Za-z0-9._/-]+$", value):
        raise argparse.ArgumentTypeError("expected a full ref name under refs/")
    return value


def _positive(value: str) -> int:
    if not value.isdigit() or int(value) < 1:
        raise argparse.ArgumentTypeError("expected a whole number of 1 or more")
    return int(value)


class _Parser(argparse.ArgumentParser):
    """Argparse that exits 64 (not 2) on a usage error."""

    def error(self, message: str):
        self.print_usage(sys.stderr)
        self.exit(EXIT_USAGE, f"{self.prog}: usage error: {message}\n")


VERBS: Dict[str, Callable[[argparse.Namespace], Dict[str, Any]]] = {
    "preflight": _cmd_preflight,
    "check-message": _cmd_check_message,
    "submodules": _cmd_submodules,
    "stage-plan": _cmd_stage_plan,
    "verify": _cmd_verify,
    "reconcile": _cmd_reconcile,
    "resolve-check": _cmd_resolve_check,
}


def build_parser() -> argparse.ArgumentParser:
    parser = _Parser(prog="vcs", description="Read-only git facts for /sc:git.")
    verbs = parser.add_subparsers(dest="verb", required=True, metavar="<verb>")
    pre = verbs.add_parser("preflight", help="facts to check before a local write")
    pre.add_argument("--cwd", default=None, help="directory inside the repository")
    sub = verbs.add_parser("submodules", help="state and eligibility of each submodule")
    sub.add_argument("--cwd", default=None, help="directory inside the repository")
    plan = verbs.add_parser("stage-plan", help="plan an add or a commit of paths")
    plan.add_argument("--cwd", default=None, help="directory inside the repository")
    plan.add_argument(
        "--path",
        action="append",
        nargs="+",
        default=None,
        help="a repository-relative path (repeat or list several; none: pathless commit)",
    )
    plan.add_argument(
        "--ledger", default=None, help="ledger mode: the implement ledger"
    )
    plan.add_argument("--run-dir", default=None, help="ledger mode: the run folder")
    plan.add_argument(
        "--package", default=None, help="ledger mode: the managed package"
    )
    plan.add_argument(
        "--candidate",
        action="store_true",
        help="ledger mode: build the frozen candidate tree after the prepared line",
    )
    ver = verbs.add_parser("verify", help="what the history proves after a commit call")
    ver.add_argument("--cwd", default=None, help="directory inside the repository")
    ver.add_argument(
        "--key", required=True, type=_hex(64), help="the full boundary key"
    )
    ver.add_argument("--attempt", required=True, type=_positive)
    ver.add_argument(
        "--parent", required=True, type=_hex(40), help="the prepared parent"
    )
    ver.add_argument(
        "--candidate-ref", required=True, type=_ref, help="the pinned candidate tree"
    )
    ver.add_argument(
        "--worktree-ref", required=True, type=_ref, help="the pinned worktree tree"
    )
    ver.add_argument(
        "--exit",
        required=True,
        type=int,
        help="the commit call's shell status; -1 when a host hook refused the call",
    )
    ver.add_argument("--ledger", default=None, help="the implement ledger")
    ver.add_argument("--sidecar", default=None, help="the commits.md of the run")
    rec = verbs.add_parser(
        "reconcile", help="the state of every boundary and the one action of this run"
    )
    rec.add_argument("--cwd", default=None, help="directory inside the repository")
    rec.add_argument("--ledger", required=True, help="the implement ledger")
    rec.add_argument("--sidecar", required=True, help="the commits.md of the run")
    rec.add_argument("--run-dir", required=True, help="the run folder")
    rec.add_argument("--package", default=None, help="the managed package folder")
    rec.add_argument(
        "--flag",
        required=True,
        choices=("on", "off"),
        help="whether this invocation carries --commit-tasks",
    )
    res = verbs.add_parser(
        "resolve-check", help="which owner answers hold for an unsettled boundary"
    )
    res.add_argument("--cwd", default=None, help="directory inside the repository")
    res.add_argument(
        "--key", required=True, help="the full boundary key or a unique prefix of it"
    )
    res.add_argument("--ledger", required=True, help="the implement ledger")
    res.add_argument("--sidecar", required=True, help="the commits.md of the run")
    res.add_argument("--run-dir", default=None, help="the run folder (legacy)")
    res.add_argument("--package", default=None, help="the managed package folder")
    msg = verbs.add_parser("check-message", help="check a drafted commit message")
    msg.add_argument("--file", required=True, help="the message file to check")
    msg.add_argument(
        "--implement",
        action="store_true",
        help="also require the task lines and Implement-* trailers",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.verb == "stage-plan":
        if (args.ledger is None) != (args.run_dir is None):
            parser.error("--ledger and --run-dir go together")
        if args.ledger is None and (args.package or args.candidate):
            parser.error("--package and --candidate need --ledger and --run-dir")
        if args.ledger is not None and args.path is not None:
            parser.error("--path and --ledger are separate modes")
    if getattr(args, "cwd", None) is None:
        args.cwd = os.getcwd()
    try:
        return emit(VERBS[args.verb](args))
    except (LookupFailed, OSError) as err:
        sys.stderr.write(f"vcs {args.verb}: lookup failed: {err}\n")
        return EXIT_LOOKUP


if __name__ == "__main__":
    sys.exit(main())
