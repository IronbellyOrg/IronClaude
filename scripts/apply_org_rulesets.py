#!/usr/bin/env python3
"""Apply the three IronClaude rulesets to ONE repo of an organisation, one repo per run.

The rule files in ``.github/rulesets/`` are the only source of the rules. This script
renders them for a repo's branches, checks the repo (a dry run that prints what would
change) and, only with ``--apply --confirm <digest>``, creates the rulesets and reads
each one back. It never edits or deletes a ruleset and it never posts the issue comment.

The file holds the pure rendering and comparing functions and the command runner
(``Runner``: the only place a ``gh`` process starts, behind a positive allowlist).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

EXIT_OK = 0
EXIT_USAGE = 64
EXIT_FAILED = 69

# The repo root is found from this file, never from the current working folder.
ROOT = Path(__file__).resolve().parent.parent
RULES_DIR = ROOT / ".github" / "rulesets"

BRANCH_RULES_FILE = "protect-master.json"
TAG_RULES_FILE = "protect-release-tags.json"

# The branches that get a ruleset first, in write order; any other default branch
# follows them.
FIXED_BRANCHES = ("integration", "master")

# Keys GitHub adds to a ruleset it returns. They are not part of the rules and are the
# only keys ``compare_bodies`` ignores.
SERVER_KEYS = frozenset(
    {
        "id",
        "source",
        "source_type",
        "node_id",
        "created_at",
        "updated_at",
        "current_user_can_bypass",
        "_links",
    }
)

# Keys whose list order does not matter.
_SET_KEYS = frozenset({"rules", "bypass_actors"})


def _load(name: str) -> dict:
    return json.loads((RULES_DIR / name).read_text(encoding="utf-8"))


def _canon(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def render_branch(branch: str) -> dict:
    """The branch ruleset body for ``branch``: ``protect-master.json`` with the name
    and the ref changed, nothing else."""
    if not branch or "*" in branch or "~" in branch or branch.startswith("refs/"):
        raise ValueError(f"not a plain branch name: {branch!r}")
    body = _load(BRANCH_RULES_FILE)
    body["name"] = f"protect-{branch}"
    body["conditions"]["ref_name"]["include"] = [f"refs/heads/{branch}"]
    return body


def render_tags() -> dict:
    """The release-tag ruleset body, exactly as the file holds it."""
    return _load(TAG_RULES_FILE)


def branch_set(default_branch: str, existing: object) -> list[str]:
    """The branches to protect: ``integration`` and ``master`` where they exist, plus
    the default branch, each once, in write order."""
    if not default_branch:
        raise ValueError("a repo with no default branch has no branch set")
    names = [b for b in FIXED_BRANCHES if b in set(existing)]
    if default_branch not in names:
        names.append(default_branch)
    return names


def plan_bodies(branches: list[str]) -> list[dict]:
    """Every body in write order: the tag ruleset, ``integration``, ``master``, then
    any other branch."""
    wanted = list(dict.fromkeys(branches))
    ordered = [b for b in FIXED_BRANCHES if b in wanted]
    ordered += [b for b in wanted if b not in FIXED_BRANCHES]
    return [render_tags()] + [render_branch(b) for b in ordered]


def payload_digest(bodies: list[dict]) -> str:
    """The sha256 of the bodies in order; ``--confirm`` must repeat it."""
    return hashlib.sha256(_canon(bodies).encode("utf-8")).hexdigest()


def _set_diff(key: str, want: object, got: object) -> list[str]:
    wanted = {_canon(x) for x in (want or [])}
    found = {_canon(x) for x in (got or [])}
    out = [f"{key}: missing {item}" for item in sorted(wanted - found)]
    out += [f"{key}: extra {item}" for item in sorted(found - wanted)]
    return out


def compare_bodies(rendered: dict, remote: dict) -> list[str]:
    """Differences between a body we rendered and the ruleset GitHub returned.

    ``rules`` and ``bypass_actors`` compare as sets (a rule is its type plus its
    complete parameters); the server keys in ``SERVER_KEYS`` are ignored; any other
    key on either side is a difference. An empty list means equal.
    """
    kept = {k: v for k, v in remote.items() if k not in SERVER_KEYS}
    diffs: list[str] = []
    for key in sorted(set(rendered) | set(kept)):
        if key not in kept:
            diffs.append(f"{key}: missing in the remote ruleset")
        elif key not in rendered:
            diffs.append(f"{key}: unexpected key in the remote ruleset")
        elif key in _SET_KEYS:
            diffs.extend(_set_diff(key, rendered[key], kept[key]))
        elif rendered[key] != kept[key]:
            diffs.append(
                f"{key}: expected {_canon(rendered[key])}, got {_canon(kept[key])}"
            )
    return diffs


# --- The command runner -------------------------------------------------------------

# The organisation that must never be touched, compared without letter case.
UPSTREAM_ORG = "superclaude-org"

TIMEOUT_SECONDS = 60


@dataclass(frozen=True)
class Result:
    returncode: int
    stdout: str
    stderr: str


# What a call that ran into TIMEOUT_SECONDS returns (never a hang).
TIMED_OUT = Result(124, "", f"timed out after {TIMEOUT_SECONDS} seconds")


@dataclass
class CommandRecord:
    """One accepted call. ``stdin_name`` is the ``name`` of a posted ruleset body."""

    argv: list[str]
    stdin_name: str | None = None


class RefusedCommand(Exception):
    """A call the allowlist or the read-only mode refused; no process was started."""


def check_org(org: str) -> str:
    """The organisation name, or ValueError for an empty one or the upstream one."""
    if not org or not _SEGMENT.fullmatch(org):
        raise ValueError(f"not an organisation name: {org!r}")
    if org.lower() == UPSTREAM_ORG:
        raise ValueError("the upstream organisation is never touched")
    return org


# One path segment: starts with a letter, digit, underscore or dot (never a dash, so
# it cannot look like an option); "." and ".." are rejected where segments are checked.
_SEGMENT = re.compile(r"[A-Za-z0-9_.][A-Za-z0-9_.-]*")
_QUERY_VALUE = re.compile(r"[A-Za-z0-9_.:/-]+")
_SHA = re.compile(r"[0-9a-f]{7,40}")
_ID = re.compile(r"[0-9]+")

# The query keys each kind of call may carry; a kind not listed carries none.
_QUERY_KEYS = {
    "activity": {"ref", "time_period", "per_page"},
    "commits": {"sha", "since", "per_page"},
    "rulesets": {"per_page"},
    "tags": {"per_page"},
}
# The list calls that may follow their pages.
_PAGINATED = frozenset(_QUERY_KEYS)


def _plain(parts: list[str]) -> bool:
    return bool(parts) and all(
        _SEGMENT.fullmatch(p) and p not in (".", "..") for p in parts
    )


def _kind(tail: list[str]) -> str:
    """Which allowed call a path below ``repos/<org>/<repo>`` is, or RefusedCommand."""
    if not tail:
        return "repo"
    if tail[0] == "branches" and _plain(tail[1:]):
        return "protection" if len(tail) > 2 and tail[-1] == "protection" else "branch"
    if tail == ["rulesets"]:
        return "rulesets"
    if len(tail) == 2 and tail[0] == "rulesets" and _ID.fullmatch(tail[1]):
        return "ruleset"
    if tail in (["activity"], ["commits"]):
        return tail[0]
    if len(tail) == 3 and tail[0] == "commits" and tail[2] == "pulls":
        return "pulls" if _SHA.fullmatch(tail[1]) else ""
    if tail == ["git", "matching-refs", "tags", "v"]:
        return "tags"
    return ""


def _check_path(path: str) -> str:
    """Check a ``gh api`` path against the allowed shapes; return its kind."""
    base, _, query = path.partition("?")
    parts = base.split("/")
    if len(parts) < 3 or parts[0] != "repos" or not _plain(parts[1:3]):
        raise RefusedCommand(f"path not under repos/<org>/<repo>: {path}")
    try:
        check_org(parts[1])
    except ValueError as exc:
        raise RefusedCommand(str(exc)) from exc
    kind = _kind(parts[3:])
    if not kind:
        raise RefusedCommand(f"path not on the allowlist: {path}")
    allowed = _QUERY_KEYS.get(kind, set())
    for pair in query.split("&") if query else []:
        key, eq, value = pair.partition("=")
        if not eq or key not in allowed or not _QUERY_VALUE.fullmatch(value):
            raise RefusedCommand(f"query not on the allowlist: {path}")
    return kind


@dataclass
class Runner:
    """The only way this script starts an outside program.

    ``check_allowed`` is a positive allowlist: ``gh api`` calls under
    ``repos/<org>/<repo>`` of the shapes this script needs, and nothing else. Every
    accepted call is recorded. A runner built with ``read_only=True`` (the dry run)
    refuses POST before any process starts.
    """

    read_only: bool = False
    commands: list[CommandRecord] = field(default_factory=list)
    # The environment ``gh`` runs in (its token); None means this process's own.
    env: Mapping[str, str] | None = None

    def check_allowed(self, argv: list[str], stdin: str | None = None) -> str | None:
        """Raise RefusedCommand unless ``argv`` is allowed. Return the ``name`` of the
        posted body for a POST, else None."""
        if not argv or argv[0] != "gh" or argv[1:2] != ["api"]:
            raise RefusedCommand("only gh api calls are allowed")
        method = source = path = None
        paginate = False
        i = 2
        while i < len(argv):
            token = argv[i]
            if token == "--method" and method is None and i + 1 < len(argv):
                method, i = argv[i + 1], i + 2
            elif token == "--input" and source is None and i + 1 < len(argv):
                source, i = argv[i + 1], i + 2
            elif token == "--paginate" and not paginate:
                paginate, i = True, i + 1
            elif token and not token.startswith("-") and path is None:
                path, i = token, i + 1
            else:
                raise RefusedCommand(f"gh api option not allowed: {token!r}")
        if path is None:
            raise RefusedCommand("gh api needs a path")
        kind = _check_path(path)
        if method is None:
            if source is not None or (paginate and kind not in _PAGINATED):
                raise RefusedCommand("option not allowed on this read")
            return None
        if method != "POST" or kind != "rulesets" or "?" in path:
            raise RefusedCommand("POST is allowed only on repos/<org>/<repo>/rulesets")
        if source != "-" or paginate or not stdin:
            raise RefusedCommand("a POST sends its body on stdin (--input -)")
        try:
            name = json.loads(stdin)["name"]
        except (ValueError, TypeError, KeyError) as exc:
            raise RefusedCommand("a POST body must be a ruleset with a name") from exc
        if not isinstance(name, str) or not name:
            raise RefusedCommand("a POST body must be a ruleset with a name")
        return name

    def run(self, argv: list[str], stdin: str | None = None) -> Result:
        name = self.check_allowed(argv, stdin)
        if self.read_only and name is not None:
            raise RefusedCommand("read-only runner: POST refused")
        self.commands.append(CommandRecord(list(argv), name))
        return self._execute(argv, stdin)

    def _execute(self, argv: list[str], stdin: str | None) -> Result:
        env = dict(os.environ if self.env is None else self.env, GH_PROMPT_DISABLED="1")
        try:
            proc = subprocess.run(
                argv,
                input=stdin,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=TIMEOUT_SECONDS,
                env=env,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return TIMED_OUT
        except OSError as exc:
            return Result(127, "", f"{type(exc).__name__}: {exc}")
        return Result(proc.returncode, proc.stdout, proc.stderr)


# --- Reads: the repo, the 90-day push check, what already exists ------------------

PUSH_WINDOW_DAYS = 90
PER_PAGE = 100
# More pages than this and a list answer counts as cut short.
PAGE_CAP = 10
# More commits than this and the pull-request lookups of one branch stop.
LOOKUP_CAP = 200
# The activity event types that are direct pushes (``pr_merge`` is not).
DIRECT_PUSH_TYPES = frozenset({"push", "force_push", "branch_deletion"})


def http_status(result: Result) -> int:
    """200 for a successful call, else the HTTP status ``gh`` printed, else 0."""
    if result.returncode == 0:
        return 200
    found = re.search(r"HTTP (\d{3})", result.stderr)
    return int(found.group(1)) if found else 0


def _items(result: Result) -> tuple[list, int]:
    """The items and the page count of a paginated list answer. ``gh --paginate``
    prints one JSON array per page back to back; anything else is a ValueError."""
    text = result.stdout.strip()
    if result.returncode != 0 or not text:
        raise ValueError("the call failed or gave no answer")
    decoder = json.JSONDecoder()
    items: list = []
    pages = pos = 0
    while pos < len(text):
        value, pos = decoder.raw_decode(text, pos)
        if not isinstance(value, list):
            raise ValueError("a page is not a list")
        items.extend(value)
        pages += 1
        while pos < len(text) and text[pos].isspace():
            pos += 1
    return items, pages


def _json_object(result: Result) -> dict | None:
    if http_status(result) != 200:
        return None
    try:
        data = json.loads(result.stdout)
    except ValueError:
        return None
    return data if isinstance(data, dict) else None


def read_repo(runner: Runner, org: str, repo: str) -> dict:
    """Facts about the repo, and the reasons the script must refuse it (``archived``,
    ``no-admin``, ``no-default-branch``, ``unreadable``, ``unreadable-branch``)."""
    answer = runner.run(["gh", "api", f"repos/{org}/{repo}"])
    info = {
        "owner": org,
        "name": repo,
        "archived": False,
        "default_branch": None,
        "admin": False,
        "existing": [],
        "refusals": [],
        "status": http_status(answer),
    }
    data = _json_object(answer)
    if data is None:
        info["refusals"].append("unreadable")
        return info
    info["owner"] = (data.get("owner") or {}).get("login") or org
    info["name"] = data.get("name") or repo
    info["archived"] = bool(data.get("archived"))
    info["default_branch"] = data.get("default_branch") or None
    info["admin"] = bool((data.get("permissions") or {}).get("admin"))
    if info["archived"]:
        info["refusals"].append("archived")
    if not info["admin"]:
        info["refusals"].append("no-admin")
    if not info["default_branch"]:
        info["refusals"].append("no-default-branch")
    base = f"repos/{info['owner']}/{info['name']}"
    for branch in FIXED_BRANCHES:
        status = http_status(runner.run(["gh", "api", f"{base}/branches/{branch}"]))
        if status == 200:
            info["existing"].append(branch)
        elif status != 404:
            info["refusals"].append("unreadable-branch")
    return info


def _stamp(text: str) -> datetime:
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def _push_activity(runner, org, repo, branch, cutoff):
    """The activity source for one branch, or None when it gives no full answer."""
    query = f"ref=refs/heads/{branch}&time_period=quarter&per_page={PER_PAGE}"
    answer = runner.run(
        ["gh", "api", "--paginate", f"repos/{org}/{repo}/activity?{query}"]
    )
    if answer.returncode != 0:
        return None
    try:
        items, pages = _items(answer)
        if pages > PAGE_CAP:
            return None
        window = [e for e in items if _stamp(e["timestamp"]) >= cutoff]
        direct = sum(1 for e in window if e["activity_type"] in DIRECT_PUSH_TYPES)
    except (ValueError, KeyError, TypeError):
        return None
    return {
        "result": "blocked" if direct else "pass",
        "source": "activity",
        "direct_pushes": direct,
        "examined": len(window),
    }


def _merged_into(pulls: object, branch: str) -> bool:
    if not isinstance(pulls, list):
        raise ValueError("not a list of pull requests")
    return any(
        isinstance(p, dict)
        and p.get("merged_at")
        and (p.get("base") or {}).get("ref", branch) == branch
        for p in pulls
    )


def _push_commits(runner, org, repo, branch, cutoff):
    """The fallback: a commit with no merged pull request is a direct push. It can
    report ``blocked`` but never ``pass``: ``since`` filters on commit dates, not on
    when the branch moved, so a push of an older commit is not visible here."""
    out = {"source": "commits", "direct_pushes": 0, "examined": 0}
    query = f"sha={branch}&since={_iso(cutoff)}&per_page={PER_PAGE}"
    answer = runner.run(
        ["gh", "api", "--paginate", f"repos/{org}/{repo}/commits?{query}"]
    )
    try:
        if answer.returncode != 0:
            raise ValueError("the commit list failed")
        commits, pages = _items(answer)
        shas = [c["sha"] for c in commits]
        if pages > PAGE_CAP:
            raise ValueError("the commit list was cut short")
    except (ValueError, KeyError, TypeError) as exc:
        return {**out, "result": "incomplete", "note": str(exc)}
    unknown = len(shas) > LOOKUP_CAP
    for sha in shas[:LOOKUP_CAP]:
        reply = runner.run(["gh", "api", f"repos/{org}/{repo}/commits/{sha}/pulls"])
        out["examined"] += 1
        try:
            if reply.returncode != 0:
                raise ValueError("a pull-request lookup failed")
            merged = _merged_into(json.loads(reply.stdout), branch)
        except ValueError:
            unknown = True
            continue
        if not merged:
            out["direct_pushes"] += 1
    if out["direct_pushes"]:
        return {**out, "result": "blocked"}
    note = "not every commit was checked"
    if not unknown:
        note = (
            "commit dates are not push dates, so an older commit pushed now is missed"
        )
    return {**out, "result": "incomplete", "note": note}


def _iso(moment: datetime) -> str:
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")


def check_push(
    runner: Runner, org: str, repo: str, branches: list[str], now: datetime
) -> dict:
    """The direct-push check, per branch, over the last 90 days.

    One UTC cutoff for the run. A branch is ``pass`` only with zero direct pushes
    from a source that gave a full answer, ``blocked`` with any, ``incomplete``
    otherwise. The overall result is ``pass`` only when every branch passes.
    """
    cutoff = now.astimezone(timezone.utc) - timedelta(days=PUSH_WINDOW_DAYS)
    per_branch = {}
    for branch in branches:
        found = _push_activity(runner, org, repo, branch, cutoff)
        per_branch[branch] = found or _push_commits(runner, org, repo, branch, cutoff)
    results = {v["result"] for v in per_branch.values()}
    if "blocked" in results:
        overall = "blocked"
    elif results == {"pass"}:
        overall = "pass"
    else:
        overall = "incomplete"
    return {"result": overall, "cutoff": _iso(cutoff), "branches": per_branch}


def read_existing(runner: Runner, org: str, repo: str, branches: list[str]) -> dict:
    """What the repo already has: ruleset names (``rulesets`` is None when the list
    could not be read), classic protection per branch (``classic``, ``none`` or
    ``unknown``) and the number of ``v*`` tags (None when unknown)."""
    base = f"repos/{org}/{repo}"
    listed = runner.run(
        ["gh", "api", "--paginate", f"{base}/rulesets?per_page={PER_PAGE}"]
    )
    rulesets = None
    try:
        items, _ = _items(listed)
        rulesets = {}
        for item in items:
            rulesets.setdefault(item["name"], item["id"])
    except (ValueError, KeyError, TypeError):
        rulesets = None
    protection = {}
    for branch in branches:
        status = http_status(
            runner.run(["gh", "api", f"{base}/branches/{branch}/protection"])
        )
        protection[branch] = {200: "classic", 404: "none"}.get(status, "unknown")
    tags = runner.run(
        [
            "gh",
            "api",
            "--paginate",
            f"{base}/git/matching-refs/tags/v?per_page={PER_PAGE}",
        ]
    )
    try:
        v_tags = len(_items(tags)[0])
    except (ValueError, TypeError):
        v_tags = None
    return {
        "rulesets": rulesets,
        "rulesets_status": http_status(listed),
        "protection": protection,
        "v_tags": v_tags,
    }


# --- The dry run and apply ----------------------------------------------------------

# The IronClaude rulesets. The script never names these ids in any call: a repo that
# lists one of them is refused.
PROTECTED_RULESET_IDS = frozenset({28081842, 28081844, 28081845})

_REFUSAL_TEXT = {
    "archived": "repo is archived",
    "no-admin": "no admin permission on the repo",
    "no-default-branch": "repo has no default branch",
    "unreadable": "repo cannot be read (HTTP {status})",
    "unreadable-branch": "a branch lookup failed",
}


def _assess(runner: Runner, org: str, repo: str, now: datetime) -> dict:
    """Everything a dry run and an apply both need, read fresh from GitHub. ``problems``
    names every check that makes ``--apply`` refuse (nothing is carried between runs)."""
    info = read_repo(runner, org, repo)
    problems = [
        _REFUSAL_TEXT[r].format(status=info["status"]) for r in info["refusals"]
    ]
    found = {"info": info, "problems": problems, "bodies": None, "digest": None}
    if "unreadable" in info["refusals"] or not info["default_branch"]:
        return found
    owner, name = info["owner"], info["name"]
    try:
        branches = branch_set(info["default_branch"], info["existing"])
        bodies = plan_bodies(branches)
    except ValueError as exc:
        problems.append(f"branch not supported: {exc}")
        return found
    push = check_push(runner, owner, name, branches, now)
    existing = read_existing(runner, owner, name, branches)
    if push["result"] != "pass":
        problems.append(f"push check is {push['result']}")
    for branch, state in existing["protection"].items():
        if state == "classic":
            problems.append(f"classic branch protection on {branch}")
        elif state == "unknown":
            problems.append(f"branch protection state unknown on {branch}")
    if existing["rulesets"] is None:
        status = existing["rulesets_status"]
        problems.append(f"ruleset list cannot be read (HTTP {status})")
    elif PROTECTED_RULESET_IDS & set(existing["rulesets"].values()):
        problems.append("repo lists a ruleset id this script never touches")
    else:
        found["same"] = _check_same_name(
            runner, owner, name, bodies, existing["rulesets"], problems
        )
    found.update(
        branches=branches,
        push=push,
        existing=existing,
        bodies=bodies,
        digest=payload_digest(bodies),
    )
    return found


def _check_same_name(runner, owner, name, bodies, names, problems) -> set[str]:
    """A ruleset that already has the name of a rendered body is skipped only when it
    equals that body. The names that do are returned; any other (different or
    unreadable) adds a problem, so ``--apply`` refuses and the operator decides."""
    identical = set()
    for body in bodies:
        rid = names.get(body["name"])
        if rid is None:
            continue
        got = runner.run(["gh", "api", f"repos/{owner}/{name}/rulesets/{rid}"])
        remote = _json_object(got)
        label = body["name"]
        if remote is None:
            problems.append(f"same-name ruleset {label} (id {rid}) cannot be read")
            continue
        diffs = compare_bodies(body, remote)
        if diffs:
            problems.append(
                f"same-name ruleset {label} (id {rid}) differs: " + "; ".join(diffs)
            )
        else:
            identical.add(label)
    return identical


def dry_run_report(runner: Runner, org: str, repo: str, now: datetime) -> list[str]:
    """The lines a dry run prints. It makes no write."""
    found = _assess(runner, org, repo, now)
    info = found["info"]
    lines = [
        f"repo: {info['owner']}/{info['name']} (default branch: "
        f"{info['default_branch'] or 'none'}, archived: "
        f"{'yes' if info['archived'] else 'no'}, admin: "
        f"{'yes' if info['admin'] else 'no'})"
    ]
    if found["bodies"] is None:
        lines += [f"would refuse --apply: {p}" for p in found["problems"]]
        return lines + ["no plan: the repo could not be planned"]
    push, existing = found["push"], found["existing"]
    lines.append(
        f"push check, last {PUSH_WINDOW_DAYS} days since {push['cutoff']}: "
        f"{push['result']}"
    )
    for branch, got in push["branches"].items():
        note = f", {got['note']}" if got.get("note") else ""
        lines.append(
            f"  {branch}: {got['result']} (source {got['source']}, "
            f"direct pushes {got['direct_pushes']}, examined {got['examined']}{note})"
        )
    names = existing["rulesets"]
    lines.append(
        "existing rulesets: "
        + ("unknown" if names is None else ", ".join(sorted(names)) or "none")
    )
    lines.append(
        "classic protection: "
        + ", ".join(f"{b} {s}" for b, s in existing["protection"].items())
    )
    tags = existing["v_tags"]
    lines.append(f"v* tags: {'unknown' if tags is None else tags}")
    lines.append(
        "WARNING: the tag ruleset blocks moving and deleting v* tags; check the "
        "release workflows of this repo by hand before applying."
    )
    lines.append("would create, in this order:")
    same = found.get("same", set())
    for number, body in enumerate(found["bodies"], 1):
        present = names is not None and body["name"] in names
        note = ""
        if present and body["name"] in same:
            note = " - skipped, an identical ruleset of this name already exists"
        elif present:
            note = " - not created, a ruleset of this name already exists"
        lines.append(f"  {number}. {body['name']} ({body['target']}){note}")
    lines += [f"would refuse --apply: {p}" for p in found["problems"]]
    lines.append(f"digest: {found['digest']}")
    lines.append(
        f"apply with: uv run python scripts/apply_org_rulesets.py --org {info['owner']}"
        f" --repo {info['name']} --out <DIR> --apply --confirm {found['digest']}"
    )
    return lines


def _before_state(runner, base, existing, digest, owner, name, now):
    """The saved before state, or a refusal text. Every existing ruleset is read by id
    (the list answer may hold summaries only); the branch protection of the set was
    read just before and is ``none`` on every branch, or the run would have refused."""
    rulesets = {}
    for rid in sorted(existing["rulesets"].values()):
        data = _json_object(runner.run(["gh", "api", f"{base}/rulesets/{rid}"]))
        if data is None:
            return None, f"before-state read failed for ruleset {rid}"
        rulesets[str(rid)] = data
    state = {
        "org": owner,
        "repo": name,
        "saved_at": _iso(now),
        "digest": digest,
        "rulesets": rulesets,
        "protection": dict.fromkeys(existing["protection"], "none"),
    }
    return state, None


def _adopt(runner: Runner, base: str, ruleset_name: str) -> int | None:
    """After a POST that timed out: the id of the ruleset of that name, if it exists."""
    listed = runner.run(
        ["gh", "api", "--paginate", f"{base}/rulesets?per_page={PER_PAGE}"]
    )
    try:
        items, _ = _items(listed)
        return next((i["id"] for i in items if i["name"] == ruleset_name), None)
    except (ValueError, KeyError, TypeError):
        return None


def apply_repo(
    runner: Runner,
    org: str,
    repo: str,
    out_dir: str | Path | None,
    confirm: str | None,
    now: datetime,
) -> dict:
    """Create the rulesets of one repo, each read back before the next write.

    Nothing is carried over from a dry run: every check is read again and ``confirm``
    must equal the digest of the bodies rendered now. Any refusal makes no write call
    and writes no file. Returns ``ok``, ``error``, ``refusals``, ``ids`` (name to id of
    what was created or adopted), ``skipped``, ``comment`` (the line for issue 838,
    never posted), ``rollback`` (manual DELETE commands) and ``before_file``.
    """
    result = {
        "ok": False,
        "error": None,
        "refusals": [],
        "ids": {},
        "skipped": [],
        "comment": None,
        "rollback": [],
        "before_file": None,
    }

    def stop(*messages: str) -> dict:
        result["error"] = "; ".join(messages)
        result["refusals"] = list(messages)
        return result

    if not out_dir:
        return stop("no --out folder given")
    found = _assess(runner, org, repo, now)
    info, problems = found["info"], list(found["problems"])
    if confirm != found["digest"]:
        problems.append("confirm digest does not match the rulesets rendered now")
    owner, name = info["owner"], info["name"]
    before_file = Path(out_dir) / f"{name}-before.json"
    if before_file.exists():
        problems.append(f"before-state file already exists: {before_file}")
    if problems:
        return stop(*problems)

    base = f"repos/{owner}/{name}"
    existing = found["existing"]
    state, problem = _before_state(
        runner, base, existing, found["digest"], owner, name, now
    )
    if problem:
        return stop(problem)
    try:
        before_file.parent.mkdir(parents=True, exist_ok=True)
        with open(before_file, "x", encoding="utf-8") as handle:
            json.dump(state, handle, indent=2, sort_keys=True)
            handle.write("\n")
    except FileExistsError:
        return stop(f"before-state file already exists: {before_file}")
    result["before_file"] = str(before_file)

    def fail(message: str) -> dict:
        result["error"] = message
        result["rollback"] = rollback()
        return result

    def rollback() -> list[str]:
        """Manual DELETE commands, newest first, for the ids this run created."""
        return [
            f"gh api --method DELETE {base}/rulesets/{rid}"
            for rid in reversed(list(result["ids"].values()))
        ]

    post = ["gh", "api", "--method", "POST", f"{base}/rulesets", "--input", "-"]
    for body in found["bodies"]:
        rname = body["name"]
        if rname in existing["rulesets"]:
            result["skipped"].append(rname)
            continue
        posted = runner.run(post, json.dumps(body))
        if posted == TIMED_OUT:
            rid = _adopt(runner, base, rname)
            if rid is None:
                return fail(
                    f"POST of {rname} timed out and no ruleset of that name found"
                )
        else:
            data = _json_object(posted)
            rid = data.get("id") if data else None
            if not isinstance(rid, int):
                status = http_status(posted)
                return fail(f"POST of {rname} failed (HTTP {status})")
        result["ids"][rname] = rid
        remote = _json_object(runner.run(["gh", "api", f"{base}/rulesets/{rid}"]))
        if remote is None:
            return fail(f"read-back of {rname} (id {rid}) failed")
        diffs = compare_bodies(body, remote)
        if diffs:
            return fail(f"read-back of {rname} (id {rid}) differs: " + "; ".join(diffs))
    result["ok"] = True
    ids = ", ".join(f"{n}={i}" for n, i in result["ids"].items()) or "none created"
    result["comment"] = (
        f"Applied rulesets to {owner}/{name} on {now.astimezone(timezone.utc):%Y-%m-%d}"
        f": {ids}"
    )
    result["rollback"] = rollback()
    return result


# --- The command line ---------------------------------------------------------------


class UsageError(Exception):
    """A command-line mistake; ``main`` prints it and exits ``EXIT_USAGE``."""


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise UsageError(message)


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = _Parser(
        prog="apply_org_rulesets",
        description="Apply the IronClaude rulesets to one repo. Without --apply it is "
        "a dry run that prints what would change and writes nothing.",
        allow_abbrev=False,
    )
    parser.add_argument("--org", required=True, help="the organisation (no default)")
    parser.add_argument(
        "--repo",
        required=True,
        action="append",
        help="the one repo to act on (one repo per run)",
    )
    parser.add_argument("--out", type=Path, help="folder for <repo>-before.json")
    parser.add_argument("--apply", action="store_true", help="create the rulesets")
    parser.add_argument(
        "--confirm", metavar="DIGEST", help="the digest the dry run printed"
    )
    args = parser.parse_args(argv)
    if (
        len(args.repo) != 1
        or args.repo[0] in (".", "..")
        or not _SEGMENT.fullmatch(args.repo[0])
    ):
        raise UsageError("--repo takes exactly one repo name")
    args.repo = args.repo[0]
    try:
        check_org(args.org)
    except ValueError as exc:
        raise UsageError(f"--org: {exc}") from exc
    if args.confirm is not None and not args.apply:
        raise UsageError("--confirm needs --apply")
    if args.apply and not args.confirm:
        raise UsageError("--apply needs --confirm DIGEST")
    return args


def _print_apply(result: dict) -> int:
    lines = []
    if result["before_file"]:
        lines.append(f"before state saved: {result['before_file']}")
    lines += [f"created: {n} (id {i})" for n, i in result["ids"].items()]
    lines += [f"skipped, already present: {n}" for n in result["skipped"]]
    if result["comment"]:
        lines.append(f"comment for issue 838: {result['comment']}")
    if result["rollback"]:
        lines.append("rollback by hand, only if you need to undo this:")
        lines += [f"  {command}" for command in result["rollback"]]
    if lines:
        print("\n".join(lines))
    if result["ok"]:
        return EXIT_OK
    label = "failed" if result["before_file"] else "refused"
    print(f"{label}: {result['error']}", file=sys.stderr)
    return EXIT_FAILED


def main(
    argv: list[str] | None = None,
    env: Mapping[str, str] | None = None,
    runner: Runner | None = None,
    now: datetime | None = None,
) -> int:
    try:
        args = parse_args(argv)
    except UsageError as exc:
        print(f"usage error: {exc}", file=sys.stderr)
        return EXIT_USAGE
    now = now or datetime.now(timezone.utc)
    runner = runner or Runner(read_only=not args.apply, env=env)
    try:
        if not args.apply:
            lines = dry_run_report(runner, args.org, args.repo, now)
            print("\n".join(lines))
            planned = any(line.startswith("digest: ") for line in lines)
            return EXIT_OK if planned else EXIT_FAILED
        result = apply_repo(runner, args.org, args.repo, args.out, args.confirm, now)
    except (RefusedCommand, OSError) as exc:
        # An OSError is a failed step too (an --out folder that cannot be created, a
        # rule file that cannot be read): named on stderr, never a traceback.
        label = "refused" if isinstance(exc, RefusedCommand) else "failed"
        print(f"{label}: {exc}", file=sys.stderr)
        return EXIT_FAILED
    return _print_apply(result)


if __name__ == "__main__":
    sys.exit(main())
