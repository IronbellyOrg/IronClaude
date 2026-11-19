"""Read and validate ``repos.yaml`` of the orchestrator repository (design 4.4, 5.7 and 5.8).

The file is read with ``yaml.safe_load`` only. Every failure is
``ReposError`` (the audit reason ``repos_invalid``, exit 2): the poll never
guesses a value it could not read. The public functions are small and stable
because the ``repos`` and ``plan-check`` verbs of the orchestrator import them.

Model tiers (5.8): ``plan_tier``, ``worker_tier`` and ``orchestrator_tier`` name
a ccsession tier, never a model id. The tiers a user may use are the lines
``ccsession --tier <name>`` under "Tiers in this workspace" in ``ccsession
--help``. Validation accepts a tier name that is one of the known names
(``TIER_ORDER``) or is listed, and refuses anything else (a model id, ``tier9``)
and an unreadable list. A valid name that this user may not use (a Coder
Member sees tiers 2 to 4 only) is not a validation failure: ``resolve_tier``
moves it once to the next listed tier, and a configured tier with no listed
tier after it gives no tier (the poll then records ``no_session``). This reads
design 4.4 and 5.8 together, which say "validation accepts only a listed tier"
and "an unlisted tier falls once" in the same breath (question for the owner in
the build report).
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

import yaml

from .predicates import LOGIN_PATTERN, valid_repo
from .runner import Runner

SCHEMA_VERSION = 1
REPOS_FILE = "repos.yaml"

TIER_ORDER = ("tier0", "tier1a", "tier1b", "tier2", "tier2b", "tier3", "tier4")
"""The fallback order of 5.8 point 4."""

DEFAULT_TIERS = {
    "plan_tier": "tier1b",
    "worker_tier": "tier2",
    "orchestrator_tier": "tier1b",
}
TIER_KEYS = tuple(DEFAULT_TIERS)

_METHODS = frozenset({"squash", "merge", "rebase"})
_REVIEWERS = frozenset({"augment", "codex"})
_BRANCH = re.compile(r"[A-Za-z0-9._/-]{1,200}")
_TIER_LINE = re.compile(r"^\s*\*?\s*ccsession --tier (?P<name>[A-Za-z0-9]{1,16})\s*$")
_TIERS_HEADER = "Tiers in this workspace"
_MAX_BYTES = 1024 * 1024

MAX_IN_FLIGHT_DEFAULT = 3


class ReposError(Exception):
    """``repos.yaml`` cannot be used; the audit reason is ``repos_invalid``.

    ``detail`` is a short fixed text for the operator; it never holds a value
    read from the file.
    """

    reason = "repos_invalid"

    def __init__(self, detail: str) -> None:
        super().__init__(detail)
        self.detail = detail


@dataclass(frozen=True)
class RepoEntry:
    """One listed repository (the fields the poll and the orchestrator verbs read)."""

    repo: str
    short: str
    enabled: bool
    checkout: Path | None
    clone_parent: Path | None
    merge_method: str | None
    release_merge_method: str | None
    release_head: str | None
    reviewers: tuple[str, ...] | None
    merge_safety_files: tuple[str, ...] | None
    max_in_flight: int
    plan_tier: str
    worker_tier: str
    orchestrator_tier: str
    plan_effort: str | None
    worker_effort: str | None
    reach_daily_max: int


@dataclass(frozen=True)
class ReposDoc:
    """The validated file."""

    orgs: tuple[str, ...]
    repos: tuple[RepoEntry, ...]
    grants: tuple[str, ...]
    plan_tier: str
    worker_tier: str
    orchestrator_tier: str
    plan_effort: str | None
    worker_effort: str | None
    tiers: tuple[str, ...]

    def get(self, repo: str) -> RepoEntry | None:
        """The listed entry of ``repo`` (compared case-insensitively), or None."""
        wanted = repo.lower()
        return next((r for r in self.repos if r.repo.lower() == wanted), None)

    def has_grant(self, grant: str) -> bool:
        """True when ``grants`` lists ``grant``."""
        return grant in self.grants

    def owner_listed(self, owner: str) -> bool:
        """True when ``owner`` is one of the ``orgs`` (case-insensitive)."""
        return owner.lower() in {o.lower() for o in self.orgs}


def short_name(repo: str) -> str:
    """``<short>`` of a repository: its name lower-cased, only ``a-z0-9``, cut to 12.

    ``IronbellyOrg/IronClaude`` gives ``ironclaude``. An empty result (a name
    with no letter or digit) is refused by the validation.
    """
    name = repo.split("/", 1)[-1]
    return re.sub(r"[^a-z0-9]", "", name.lower())[:12]


def parse_tiers(text: str) -> tuple[str, ...]:
    """The tier names under "Tiers in this workspace" of ``ccsession --help``.

    A name is on a line ``ccsession --tier <name>`` (a ``*`` marks the default).
    Reading stops at the first blank line after the first tier line. No tier
    gives an empty tuple.
    """
    found: list[str] = []
    inside = False
    for line in text.splitlines():
        if not inside:
            inside = _TIERS_HEADER in line
            continue
        match = _TIER_LINE.match(line)
        if match is not None:
            found.append(match["name"])
        elif not line.strip() and found:
            break
    return tuple(found)


def listed_tiers(runner: Runner, timeout: float) -> tuple[str, ...] | None:
    """The tiers this user may use, read from ``ccsession --help``; None when unreadable."""
    result = runner.run(["ccsession", "--help"], timeout)
    if result.timed_out or result.spawn_error is not None or result.returncode != 0:
        return None
    tiers = parse_tiers(result.stdout)
    return tiers or None


def fallback_tier(tier: str, listed: tuple[str, ...]) -> str | None:
    """The next listed tier after ``tier`` in ``TIER_ORDER`` (one step), or None.

    None when no listed tier follows it, or when ``tier`` is not a known name.
    """
    if tier not in TIER_ORDER:
        return None
    for name in TIER_ORDER[TIER_ORDER.index(tier) + 1 :]:
        if name in listed:
            return name
    return None


def resolve_tier(
    configured: str, listed: tuple[str, ...]
) -> tuple[str | None, str | None]:
    """``(tier to use, fallback_from)`` for a configured tier (5.8 point 4).

    A listed tier is used as it is: ``(configured, None)``. An unlisted one falls
    once: ``(next listed tier, configured)``. With no listed tier left the first
    value is None: the start is a failed handoff (``no_session``).
    """
    if configured in listed:
        return configured, None
    return fallback_tier(configured, listed), configured


def _fail(detail: str) -> ReposError:
    return ReposError(detail)


def _str(value: object, what: str) -> str:
    if not isinstance(value, str) or not value or "\0" in value:
        raise _fail(f"{what} must be a non-empty string")
    return value


def _abs_path(value: object, what: str) -> Path | None:
    if value is None:
        return None
    text = _str(value, what)
    if not Path(text).is_absolute():
        raise _fail(f"{what} must be null or an absolute path")
    return Path(text)


def _tier(value: object, what: str, listed: tuple[str, ...]) -> str:
    if not isinstance(value, str) or (value not in TIER_ORDER and value not in listed):
        raise _fail(f"{what} must be a ccsession tier name, never a model id")
    return value


def _effort(value: object, what: str) -> str | None:
    return None if value is None else _str(value, what)


def _method(entry: Mapping, key: str) -> str | None:
    value = entry.get(key)
    if value is None:
        return None
    if value not in _METHODS:
        raise _fail(f"{key} must be squash, merge or rebase")
    return value


def _reviewers(value: object) -> tuple[str, ...] | None:
    if value is None:
        return None
    if value == "none":
        return ()
    if (
        not isinstance(value, list)
        or not value
        or not all(isinstance(v, str) and v in _REVIEWERS for v in value)
        or len(set(value)) != len(value)
    ):
        raise _fail("reviewers must be none or a non-empty list of augment and codex")
    return tuple(value)


def _safety_files(entry: Mapping) -> tuple[str, ...] | None:
    """Absent: the default list of wave 7 applies (None). ``[]`` is valid: no hold.

    A null or non-list value is invalid (finding F45 of issue 675).
    """
    if "merge_safety_files" not in entry:
        return None
    value = entry["merge_safety_files"]
    if not isinstance(value, list) or not all(isinstance(v, str) and v for v in value):
        raise _fail("merge_safety_files must be a list of non-empty glob strings")
    return tuple(value)


def _max_in_flight(entry: Mapping) -> int:
    value = entry.get("max_in_flight", MAX_IN_FLIGHT_DEFAULT)
    if type(value) is not int or not 1 <= value <= 10:
        raise _fail("max_in_flight must be an integer from 1 to 10")
    return value


def _reach_daily_max(entry: Mapping) -> int:
    value = entry.get("reach_daily_max")
    # Design 4.4 reads any value that is not an integer from 0 to 50 as 0. That
    # contradicts "never a guess" (finding F23 of issue 675); this implements the
    # spec text, and the exception is stated here and in the build report.
    if type(value) is int and 0 <= value <= 50:
        return value
    return 0


def parse_repos(text: str, listed: tuple[str, ...] | None) -> ReposDoc:
    """Validate the text of ``repos.yaml`` (design 4.4) against the tiers ``listed``.

    ``listed`` None (an unreadable ``ccsession --help``) is ``repos_invalid``,
    because no orchestrator session can be started without the list.
    """
    if listed is None or not listed:
        raise _fail("the list of ccsession tiers could not be read")
    try:
        raw = yaml.safe_load(text)
    except yaml.YAMLError:
        raise _fail("repos.yaml is not valid YAML") from None
    if not isinstance(raw, dict):
        raise _fail("the top level of repos.yaml must be a mapping")
    if type(raw.get("schema_version")) is not int or raw["schema_version"] != 1:
        raise _fail("schema_version must be the integer 1")
    orgs = raw.get("orgs")
    if (
        not isinstance(orgs, list)
        or not orgs
        or not all(isinstance(o, str) and LOGIN_PATTERN.fullmatch(o) for o in orgs)
    ):
        raise _fail("orgs must be a non-empty list of organisation names")
    grants = raw.get("grants", [])
    if not isinstance(grants, list) or not all(
        isinstance(g, str) and g for g in grants
    ):
        raise _fail("grants must be a list of strings")
    top = {
        key: _tier(raw.get(key, default), key, listed)
        for key, default in DEFAULT_TIERS.items()
    }
    top_plan_effort = _effort(raw.get("plan_effort"), "plan_effort")
    top_worker_effort = _effort(raw.get("worker_effort"), "worker_effort")
    owners = {o.lower() for o in orgs}
    items = raw.get("repos")
    if items is None:
        items = []
    if not isinstance(items, list):
        raise _fail("repos must be a list")
    entries: list[RepoEntry] = []
    names: set[str] = set()
    shorts: dict[str, str] = {}
    for item in items:
        if not isinstance(item, dict):
            raise _fail("every repos entry must be a mapping")
        repo = item.get("repo")
        if not valid_repo(repo):
            raise _fail("repo must be owner/name")
        if repo.split("/", 1)[0].lower() not in owners:
            raise _fail("the owner of a repo must be in orgs")
        if repo.lower() in names:
            raise _fail("a repo is listed twice")
        names.add(repo.lower())
        enabled = item.get("enabled")
        if type(enabled) is not bool:
            raise _fail("enabled must be true or false")
        release_head = item.get("release_head")
        if release_head is not None and (
            not isinstance(release_head, str) or _BRANCH.fullmatch(release_head) is None
        ):
            raise _fail("release_head must be a branch name or null")
        short = short_name(repo)
        if not short:
            raise _fail("a repo name must hold a letter or a digit")
        if short in shorts:
            raise _fail("two listed repos have the same short name")
        shorts[short] = repo
        tiers = {
            key: _tier(item.get(key, top[key]), f"{key} of a repo", listed)
            for key in TIER_KEYS
        }
        entries.append(
            RepoEntry(
                repo=repo,
                short=short,
                enabled=enabled,
                checkout=_abs_path(item.get("checkout"), "checkout"),
                clone_parent=_abs_path(item.get("clone_parent"), "clone_parent"),
                merge_method=_method(item, "merge_method"),
                release_merge_method=_method(item, "release_merge_method"),
                release_head=release_head,
                reviewers=_reviewers(item.get("reviewers")),
                merge_safety_files=_safety_files(item),
                max_in_flight=_max_in_flight(item),
                plan_tier=tiers["plan_tier"],
                worker_tier=tiers["worker_tier"],
                orchestrator_tier=tiers["orchestrator_tier"],
                plan_effort=_effort(item.get("plan_effort"), "plan_effort")
                or top_plan_effort,
                worker_effort=_effort(item.get("worker_effort"), "worker_effort")
                or top_worker_effort,
                reach_daily_max=_reach_daily_max(item),
            )
        )
    return ReposDoc(
        orgs=tuple(orgs),
        repos=tuple(entries),
        grants=tuple(grants),
        plan_tier=top["plan_tier"],
        worker_tier=top["worker_tier"],
        orchestrator_tier=top["orchestrator_tier"],
        plan_effort=top_plan_effort,
        worker_effort=top_worker_effort,
        tiers=listed,
    )


def load_repos(orchestrator_repo: Path, runner: Runner, timeout: float) -> ReposDoc:
    """Read ``<orchestrator_repo>/repos.yaml`` and validate it (every cycle, ``check-config``).

    Reads the tier list through ``runner``. A missing, unreadable, over-large or
    invalid file is ``ReposError``.
    """
    path = Path(orchestrator_repo) / REPOS_FILE
    try:
        with open(path, "rb") as handle:
            data = handle.read(_MAX_BYTES + 1)
        if len(data) > _MAX_BYTES:
            raise _fail("repos.yaml is too large")
        text = data.decode("utf-8")
    except (OSError, UnicodeDecodeError):
        raise _fail("repos.yaml is missing or cannot be read as UTF-8 text") from None
    return parse_repos(text, listed_tiers(runner, timeout))
