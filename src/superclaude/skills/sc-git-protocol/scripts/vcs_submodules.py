"""Submodule fact rows of the read-only ``vcs`` helper (FR-040, design section 4.6).

``collect_submodules(git)`` builds one row per top-level registered submodule, sorted by
path, and the superproject facts around them. Every git call goes through the
``GitRunner`` passed in; this module starts no process. The runner must be made with
``person_invoked=True``: the dirty flags need ``status --ignore-submodules=none``, which
only a person-typed ``/sc:git`` line may run (a runner without it raises
``ForbiddenArgv``).

Row fields and where each comes from (a value that cannot be read is ``None``, never a
made-up clean state):

  * ``path``, and ``conflicted`` (also a stage above 0): ``ls-files --stage`` entries of
    mode 160000 plus the prefix of ``submodule status`` (``U`` is a conflict);
  * ``gitlink``: ``ls-tree HEAD -- <path>`` (the SHA the superproject HEAD records);
  * ``initialized``: the ``submodule status`` prefix is not ``-``;
  * ``head`` and ``branch``: ``rev-parse HEAD`` and ``branch --show-current`` inside the
    module (``branch`` is ``None`` when HEAD is detached);
  * ``commit_changed``, ``tracked_dirty``, ``untracked_dirty``: the ``S<c><m><u>`` field of
    ``status --porcelain=v2 --ignore-submodules=none`` of the superproject. An initialized
    module that has no status line is unchanged, so all three are ``False``;
  * ``target_local``: ``cat-file -e <gitlink>^{commit}`` inside the module (exit 0 true;
    exit 1 or 128 false, because git answers 128 for a full SHA it does not have);
  * ``contained``: ``for-each-ref --contains <head> refs/heads refs/remotes`` inside the
    module (true when any ref lists it; ``None`` when the lookup failed);
  * ``nested``: the module has its own ``.gitmodules`` file. Such a row carries the
    ``reason`` ``nested-not-inspected``; nothing inside a nested module is read.

``reason`` is ``None`` or a comma-joined list of the tokens that say why a value is
unknown beyond "the module is not initialized": ``nested-not-inspected``,
``gitlink-unknown``, ``status-unavailable``, ``submodule-status-unavailable``,
``containment-unknown``, ``gitmodules-unavailable``, ``gitmodules-url-unknown``,
``gitmodules-url-relative``, ``ancestry-unknown``, ``remote-unknown``.

Derived columns (FR-040 to FR-044), added to every row after the facts:

  * ``gitmodules_url``: the url of the work tree ``.gitmodules`` (read with
    ``config --file``), shown without credentials (the whole user part of an http, https,
    ftp or ftps url; the password of any other ``scheme://`` url). ``None`` when unknown.
  * ``remote_mismatch``: whether ``submodule.<name>.url`` of the superproject config
    differs from the ``.gitmodules`` url (an uninitialized module can hold one too, after
    ``submodule init``). ``None`` when no url is configured, the initialized state is
    unknown or the two cannot be compared. A relative ``.gitmodules`` url is not compared
    (how git resolves it is not modelled; UNVERIFIED), so it is ``None``.
  * ``url_configured``: whether ``submodule.<name>.url`` is set in the superproject config
    (``None`` when it could not be asked, which also refuses). With a relative ``.gitmodules`` url the two are
    not compared, so an uninitialized module that has one is refused as unverifiable.
  * ``fetch_mismatch``: for an initialized module, whether ``origin`` (or the remote its
    current branch tracks) has a url other than the ``.gitmodules`` url. ``submodule
    update`` fetches a missing commit from there. ``None`` when unreadable or not compared.
  * ``index_gitlink``: the commit the index records for the path (stage 0), the one
    ``submodule update`` checks out; ``None`` when unmerged or unreadable. ``update`` is
    refused with ``pointer-staged`` when it differs from ``gitlink`` (HEAD).
  * ``has_gitmodules_remote`` and ``published``: whether the module has a remote whose
    ``remote.<r>.url`` equals the ``.gitmodules`` url, and whether the module HEAD is in a
    remote-tracking ref of such a remote (local refs only, so a local observation).
    Read only for an initialized module whose HEAD differs from the gitlink; otherwise
    ``None``. A relative ``.gitmodules`` url matches no remote.
  * ``state``, first match wins: ``conflict``, ``dirty-tracked``, ``dirty-untracked``,
    ``detached-new-commits``, ``uninitialized``, ``target-not-local``,
    ``submodule-ahead`` (the gitlink is an ancestor of HEAD), ``submodule-diverged``,
    ``pointer-moved`` (HEAD is an ancestor of the gitlink), ``in-sync``. It is ``None``
    when a fact it needs is unknown; an ``--is-ancestor`` exit of 128 is such a case and
    is never read as diverged.
  * ``update`` and ``commit_pointer``: ``{ok, reason}`` (``update`` also has
    ``needs_url``), one table over the row. ``reason`` is ``None`` when ``ok``; otherwise
    the refusal token. ``update`` with ``needs_url`` true is allowed only when the
    person's line repeats the displayed ``.gitmodules`` url (FR-044); the helper cannot
    see that line, so the caller checks it.

The superproject part has ``superproject {branch, head}``, ``config`` with
``submodule_recurse`` and ``push_recurse_submodules`` as the raw configured text
(``None`` when unset, so unset and ``"false"`` differ) and ``warnings`` (one text when
``submodule.recurse`` is true).

Python 3.10 or later, standard library only.
"""

from __future__ import annotations

import os
import re
from typing import Any, Dict, List, Optional, Tuple

from vcs_plan import GitRunner

_TRUE_WORDS = ("true", "yes", "on", "1")
_RECURSE_WARNING = (
    "submodule.recurse is true: a later plain push may push submodules too"
)
_USERINFO = re.compile(r"^(?P<scheme>[A-Za-z][A-Za-z0-9+.-]*)://(?P<user>[^/?#]*)@")
_USERINFO_SCHEMES = ("http", "https", "ftp", "ftps")
# The refusal token of `update` for each state it never serves (FR-041).
_UPDATE_REFUSALS = {
    "conflict": "conflict",
    "dirty-tracked": "submodule-dirty",
    "dirty-untracked": "submodule-dirty",
    "detached-new-commits": "detached-new-commits",
    "submodule-ahead": "submodule-ahead",
    "submodule-diverged": "submodule-diverged",
    "in-sync": "in-sync",
}


def _read(git: GitRunner, argv: List[str], directory: Optional[str] = None):
    """Run one read; returns ``(rc, stdout)`` (rc 124 is a timeout)."""
    return git.run(argv, directory=directory)


def _config(git: GitRunner, key: str) -> Optional[str]:
    rc, out = _read(git, ["config", "--get", key])
    return out.rstrip("\n") if rc == 0 else None


def _gitlinks(git: GitRunner) -> Dict[str, bool]:
    """Path to ``conflicted`` for every gitlink entry of the index."""
    rc, out = _read(git, ["ls-files", "-z", "--stage"])
    if rc != 0:
        return {}
    found: Dict[str, bool] = {}
    for record in out.split("\0"):
        meta, _, path = record.partition("\t")
        fields = meta.split()
        if len(fields) == 3 and fields[0] == "160000":
            found[path] = found.get(path, False) or fields[2] != "0"
    return found


def _prefixes(git: GitRunner, paths: List[str]) -> Optional[Dict[str, str]]:
    """Path to the one-character prefix of ``submodule status``; ``None`` if it failed."""
    rc, out = _read(git, ["submodule", "status"])
    if rc != 0:
        return None
    found: Dict[str, str] = {}
    for line in out.splitlines():
        sha_and_tail = line[1:].partition(" ")[2]
        for path in paths:
            if sha_and_tail == path or sha_and_tail.startswith(path + " ("):
                found[path] = line[0]
    return found


def _gitlink_sha(git: GitRunner, path: str) -> Optional[str]:
    rc, out = _read(git, ["ls-tree", "-z", "HEAD", "--", path])
    if rc != 0:
        return None
    meta = out.split("\0", 1)[0].partition("\t")[0].split()
    return meta[2] if len(meta) == 3 and meta[0] == "160000" else None


def _index_gitlink_sha(git: GitRunner, path: str) -> Optional[str]:
    """The commit the index (stage 0) records for ``path``: the one ``submodule update``
    checks out. ``None`` when it cannot be read or the entry is unmerged."""
    rc, out = _read(git, ["ls-files", "-z", "--stage", "--", path])
    if rc != 0:
        return None
    for record in out.split("\0"):
        meta, _, name = record.partition("\t")
        fields = meta.split()
        if (
            name == path
            and len(fields) == 3
            and fields[0] == "160000"
            and fields[2] == "0"
        ):
            return fields[1]
    return None


def _status_fields(git: GitRunner) -> Optional[Dict[str, Tuple[bool, bool, bool]]]:
    """Path to ``(commit_changed, tracked_dirty, untracked_dirty)`` for each submodule line."""
    rc, out = _read(git, ["status", "--porcelain=v2", "-z", "--ignore-submodules=none"])
    if rc != 0:
        return None
    found: Dict[str, Tuple[bool, bool, bool]] = {}
    records = iter(out.split("\0"))
    for record in records:
        kind = record[:1]
        if kind == "2":  # a rename or copy: the next record is the original path
            next(records, None)
            continue
        # "1": 9 fields before the path; "u": 10 fields before the path.
        fields = record.split(" ", 10 if kind == "u" else 8)
        if kind not in ("1", "u") or len(fields) < (11 if kind == "u" else 9):
            continue
        sub = fields[2]
        if sub.startswith("S") and len(sub) == 4:
            found[fields[-1]] = (sub[1] == "C", sub[2] == "M", sub[3] == "U")
    return found


def _bool_or_none(rc: int) -> Optional[bool]:
    return True if rc == 0 else False if rc in (1, 128) else None


def _row(
    git: GitRunner,
    path: str,
    conflicted: bool,
    prefix: Optional[str],
    changes: Optional[Dict[str, Tuple[bool, bool, bool]]],
) -> Dict[str, Any]:
    reasons: List[str] = []
    gitlink = _gitlink_sha(git, path)
    if gitlink is None:
        reasons.append("gitlink-unknown")
    if prefix is None:
        reasons.append("submodule-status-unavailable")
    initialized = None if prefix is None else prefix != "-"
    row: Dict[str, Any] = {
        "path": path,
        "gitlink": gitlink,
        "index_gitlink": _index_gitlink_sha(git, path),
        "initialized": initialized,
        "conflicted": conflicted or prefix == "U",
        "head": None,
        "branch": None,
        "commit_changed": None,
        "tracked_dirty": None,
        "untracked_dirty": None,
        "target_local": None,
        "contained": None,
        "nested": None,
    }
    if initialized:
        rc, out = _read(git, ["rev-parse", "--verify", "--quiet", "HEAD"], path)
        head = out.strip() if rc == 0 and out.strip() else None
        row["head"] = head
        rc, out = _read(git, ["branch", "--show-current"], path)
        row["branch"] = (out.strip() or None) if rc == 0 else None
        if changes is None:
            reasons.append("status-unavailable")
        else:
            row["commit_changed"], row["tracked_dirty"], row["untracked_dirty"] = (
                changes.get(path, (False, False, False))
            )
        if gitlink is not None:
            rc, _ = _read(git, ["cat-file", "-e", gitlink + "^{commit}"], path)
            row["target_local"] = _bool_or_none(rc)
        if head is not None:
            rc, out = _read(
                git,
                ["for-each-ref", "--contains", head, "refs/heads", "refs/remotes"],
                path,
            )
            if rc == 0:
                row["contained"] = bool(out.strip())
            else:
                reasons.append("containment-unknown")
        row["nested"] = os.path.isfile(os.path.join(git.top, path, ".gitmodules"))
        if row["nested"]:
            reasons.append("nested-not-inspected")
    row["reason"] = ",".join(reasons) or None
    return row


def _display_url(url: Optional[str]) -> Optional[str]:
    """``url`` without credentials (see the module docstring)."""
    found = _USERINFO.match(url) if url else None
    if not found:
        return url
    user = found["user"]
    if found["scheme"].lower() in _USERINFO_SCHEMES:
        keep = ""
    elif ":" in user:
        keep = user.split(":", 1)[0] + "@"
    else:
        return url
    return f"{found['scheme']}://{keep}{url[found.end() :]}"


def _is_relative(url: str) -> bool:
    return url.startswith(("./", "../"))


def _gitmodules(git: GitRunner) -> Optional[Dict[str, Tuple[str, Optional[str]]]]:
    """Path to ``(name, url)`` from the work tree ``.gitmodules``; ``None`` if unreadable."""
    rc, out = _read(
        git,
        ["config", "--file", ".gitmodules", "-z", "--get-regexp",
         r"^submodule\..*\.(path|url)$"],
    )  # fmt: skip
    if rc != 0:
        return None
    fields: Dict[str, Dict[str, str]] = {}
    for record in out.split("\0"):
        key, _, value = record.partition("\n")
        name, _, field = key[len("submodule.") :].rpartition(".")
        if key.startswith("submodule.") and name:
            fields.setdefault(name, {})[field] = value
    return {
        f["path"]: (name, f.get("url")) for name, f in fields.items() if "path" in f
    }


def _ancestor(git: GitRunner, path: str, older: str, newer: str) -> Optional[bool]:
    """Whether ``older`` is an ancestor of ``newer`` in the module; ``None`` if unknown.

    Exit 1 is "no"; exit 128 (and a timeout) is "unknown", never "no".
    """
    rc, _ = _read(git, ["merge-base", "--is-ancestor", older, newer], path)
    return True if rc == 0 else False if rc == 1 else None


def _remote_urls(git: GitRunner, path: str) -> Optional[Dict[str, str]]:
    """Remote name to url for the module; ``{}`` when it has none, ``None`` if unreadable.

    A remote can hold several ``url`` values: git fetches from the first (the others are
    extra push urls), so the first one listed is the one kept.
    """
    rc, out = _read(git, ["config", "-z", "--get-regexp", r"^remote\..*\.url$"], path)
    if rc == 1:
        return {}
    if rc != 0:
        return None
    found: Dict[str, str] = {}
    for record in out.split("\0"):
        key, _, value = record.partition("\n")
        if key.startswith("remote.") and key.endswith(".url"):
            found.setdefault(key[len("remote.") : -len(".url")], value)
    return found


def _fetch_mismatch(
    git: GitRunner, path: str, branch: Optional[str], url: str
) -> Optional[bool]:
    """Whether a remote the module fetches from by default (``origin``, and the remote its
    current branch tracks) has a url other than ``url``; ``None`` if that is unreadable.

    ``submodule update`` runs a plain ``git fetch`` inside the module, so the module's own
    remote decides where a missing commit comes from, not the superproject's url setting.
    """
    remotes = _remote_urls(git, path)
    if remotes is None:
        return None
    names = {"origin"}
    if branch:
        rc, out = _read(git, ["config", "--get", f"branch.{branch}.remote"], path)
        if rc == 0 and out.strip():
            names.add(out.strip())
        elif rc != 1:
            return None
    return any(name in remotes and remotes[name] != url for name in names)


def _published(
    git: GitRunner, path: str, head: str, url: Optional[str]
) -> Tuple[Optional[bool], Optional[bool]]:
    """``(has_gitmodules_remote, published)`` for the module HEAD (local refs only)."""
    if url is None:
        return None, None
    remotes = _remote_urls(git, path)
    if remotes is None:
        return None, None
    names = [] if _is_relative(url) else [n for n, u in remotes.items() if u == url]
    if not names:
        return False, False
    unknown = False
    for name in names:
        rc, out = _read(
            git, ["for-each-ref", "--contains", head, f"refs/remotes/{name}"], path
        )
        if rc != 0:
            unknown = True
        elif out.strip():
            return True, True
    return True, None if unknown else False


def _state(git: GitRunner, row: Dict[str, Any], reasons: List[str]) -> Optional[str]:
    """The derived state of one row, or ``None`` when a fact it needs is unknown."""
    if row["initialized"] is None:
        return None
    if row["conflicted"]:
        return "conflict"
    if row["initialized"] is False:  # every dirty and containment fact is null here
        return "uninitialized"
    if row["tracked_dirty"] is None or row["untracked_dirty"] is None:
        return None
    if row["tracked_dirty"]:
        return "dirty-tracked"
    if row["untracked_dirty"]:
        return "dirty-untracked"
    head, link = row["head"], row["gitlink"]
    if head is None or link is None:
        return None
    if head != link and row["branch"] is None:
        if row["contained"] is None:
            return None
        if not row["contained"]:
            return "detached-new-commits"
    # Equal means the target is local, so this cannot hide a later state.
    if head == link:
        return "in-sync"
    if row["target_local"] is None:
        return None
    if not row["target_local"]:
        return "target-not-local"
    path = row["path"]
    ahead = _ancestor(git, path, link, head)
    behind = _ancestor(git, path, head, link) if ahead is False else None
    if ahead is None or (ahead is False and behind is None):
        reasons.append("ancestry-unknown")
        return None
    if ahead:
        return "submodule-ahead"
    return "pointer-moved" if behind else "submodule-diverged"


def _update_eligibility(row: Dict[str, Any]) -> Dict[str, Any]:
    """FR-041 and FR-044 as one table over the row."""

    def no(reason: str) -> Dict[str, Any]:
        return {"ok": False, "reason": reason, "needs_url": False}

    state = row["state"]
    # FR-044: any module with a configured url, whatever its state. An uninitialized module
    # can hold one too (`submodule init` never overwrites it), and the clone uses it.
    if row["remote_mismatch"]:
        return no("remote-mismatch")
    if state is None:
        return no("state-unknown")
    if state in _UPDATE_REFUSALS:
        return no(_UPDATE_REFUSALS[state])
    # `submodule update` checks out the commit the index records, which `gitlink` (HEAD)
    # does not show once a different pointer is staged.
    if row["index_gitlink"] is None:
        return no("state-unknown")
    if row["index_gitlink"] != row["gitlink"]:
        return no("pointer-staged")
    if state == "uninitialized":
        if row["gitmodules_url"] is None:
            return no("gitmodules-url-unknown")
        # A configured url the (relative) .gitmodules url cannot be compared with would
        # be the clone source: not provably the one the person is shown.
        if row["url_configured"] is not False and row["remote_mismatch"] is None:
            return no("remote-unverifiable")
        return {"ok": True, "reason": None, "needs_url": True}
    if row["remote_mismatch"] is None:
        return no("remote-unverifiable")
    # The module is clean here; no commit may be orphaned.
    if state == "target-not-local":
        # git fetches inside the module, from its own remote.
        if row["fetch_mismatch"] is None:
            return no("remote-unverifiable")
        if row["fetch_mismatch"]:
            return no("remote-mismatch")
        if row["contained"] is None:
            return no("containment-unknown")
        if not row["contained"]:
            return no("detached-new-commits")
    return {"ok": True, "reason": None, "needs_url": False}


def _commit_pointer_eligibility(row: Dict[str, Any]) -> Dict[str, Any]:
    """FR-042 conditions 2 to 4 as one table over the row."""

    def no(reason: str) -> Dict[str, Any]:
        return {"ok": False, "reason": reason}

    if (
        row["initialized"] is False
        or row["conflicted"]
        or row["tracked_dirty"]
        or row["untracked_dirty"]
    ):
        return no("submodule-dirty")
    if None in (row["initialized"], row["tracked_dirty"], row["untracked_dirty"]):
        return no("state-unknown")
    if row["head"] is None or row["gitlink"] is None:
        return no("state-unknown")
    if row["head"] == row["gitlink"]:
        return no("in-sync")
    if row["has_gitmodules_remote"] is None:
        return no("containment-unknown")
    if not row["has_gitmodules_remote"]:
        return no("submodule-unpublished reason=no-gitmodules-remote")
    if row["contained"] is None:
        return no("containment-unknown")
    if not row["contained"]:
        return no("detached-new-commits")
    if row["published"] is None:
        return no("containment-unknown")
    if not row["published"]:
        return no("submodule-unpublished")
    return {"ok": True, "reason": None}


def _derive(
    git: GitRunner,
    row: Dict[str, Any],
    modules: Optional[Dict[str, Tuple[str, Optional[str]]]],
) -> None:
    """Add the derived columns to a fact row (see the module docstring)."""
    reasons: List[str] = []
    entry = None if modules is None else modules.get(row["path"])
    name, url = entry if entry else (None, None)
    if modules is None:
        reasons.append("gitmodules-unavailable")
    if url is None:
        reasons.append("gitmodules-url-unknown")
    relative = url is not None and _is_relative(url)
    if relative:
        reasons.append("gitmodules-url-relative")
    row["gitmodules_url"] = _display_url(url)

    mismatch = configured = None
    if row["initialized"] is not None and name is not None and url is not None:
        # Exit 1 is "not set"; any other failure leaves it unknown, never "not set".
        rc, out = _read(git, ["config", "--get", f"submodule.{name}.url"])
        configured = True if rc == 0 else False if rc == 1 else None
        if rc == 0 and not relative:
            mismatch = out.rstrip("\n") != url
    row["remote_mismatch"] = mismatch
    row["url_configured"] = configured
    row["fetch_mismatch"] = None
    if row["initialized"] and url is not None and not relative:
        row["fetch_mismatch"] = _fetch_mismatch(git, row["path"], row["branch"], url)

    row["has_gitmodules_remote"] = row["published"] = None
    if (
        row["initialized"]
        and row["head"] is not None
        and row["gitlink"] is not None
        and row["head"] != row["gitlink"]
    ):
        row["has_gitmodules_remote"], row["published"] = _published(
            git, row["path"], row["head"], url
        )
        if row["has_gitmodules_remote"] is None:
            reasons.append("remote-unknown")

    row["state"] = _state(git, row, reasons)
    row["update"] = _update_eligibility(row)
    row["commit_pointer"] = _commit_pointer_eligibility(row)
    row["reason"] = ",".join(filter(None, [row["reason"], *reasons])) or None


def collect_submodules(git: GitRunner) -> Dict[str, Any]:
    """Collect the superproject facts and one derived row per registered submodule.

    ``git`` is a ``GitRunner`` made with ``person_invoked=True`` for the work tree top.
    """
    links = _gitlinks(git)
    paths = sorted(links)
    prefixes = _prefixes(git, paths) if paths else {}
    changes = _status_fields(git) if paths else {}
    modules = _gitmodules(git) if paths else {}
    rows = [
        _row(
            git,
            path,
            links[path],
            None if prefixes is None else prefixes.get(path),
            changes,
        )
        for path in paths
    ]
    for row in rows:
        _derive(git, row, modules)
    rc, out = _read(git, ["branch", "--show-current"])
    branch = (out.strip() or None) if rc == 0 else None
    rc, out = _read(git, ["rev-parse", "--verify", "--quiet", "HEAD"])
    head = out.strip() if rc == 0 and out.strip() else None
    recurse = _config(git, "submodule.recurse")
    warnings = []
    if recurse is not None and recurse.strip().lower() in _TRUE_WORDS:
        warnings.append(_RECURSE_WARNING)
    return {
        "superproject": {"branch": branch, "head": head},
        "config": {
            "submodule_recurse": recurse,
            "push_recurse_submodules": _config(git, "push.recurseSubmodules"),
        },
        "rows": rows,
        "warnings": warnings,
    }
