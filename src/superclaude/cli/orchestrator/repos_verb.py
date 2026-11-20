"""The verb ``superclaude orchestrator repos``: keep ``repos.yaml`` current (design 4.4, 5.6).

    repos check
    repos add --repo <R> [--checkout <path>] [--clone-parent <path>] [--merge-method M]
              [--release-merge-method M] [--release-head <branch>] [--reviewers augment,codex|none]
              [--max-in-flight N] [--disabled]
    repos refresh [--repo <R>]
    repos set --key grants|reach_daily_max|merge_safety_files [--repo <R>] --value-json <json>
              --answer-ref <id>

``check`` validates the file with the poll's own validator and prints what it holds.
``add`` reads ``permissions``, ``default_branch``, the allowed merge methods and
``protected`` from ``gh api repos/<R>`` (and the branch), sets ``can_merge`` (push,
maintain or admin) and lists the repo; a repo the user cannot push to is stored with
``enabled: false`` and ``can_merge: false``. ``refresh`` repeats the read for one or every
repo and updates ``default_branch``, ``protected`` and ``can_merge``; a repo whose rights
fell to read-only is switched to ``enabled: false`` and named in the answer; it never
enables one. A merge method that the repo no longer allows is reported as a warning and not
changed.

``grants``, ``reach_daily_max`` and ``merge_safety_files`` are Clay's alone (5.6). Only
``set`` writes them, and ``set`` refuses (exit 2, nothing written) without an
``--answer-ref`` that ``answer-check`` accepted (``answer_ref_required``,
``answer_ref_unknown``, ``answer_ref_rejected``). The answer must have been checked for this
very question, ``answer-check --question-key repos:<key>:<repo, or - for grants>``
(``answer_ref_key_mismatch`` otherwise), so Clay's word on anything else never opens a
guarded key, and one ref pays for one write (``answer_ref_used``). The same refusal sits in
``repos_file.edit`` for every write, so ``add`` and ``refresh`` cannot change a guarded
key either. ``set`` is a fourth sub-command: the design lists ``check``, ``add`` and
``refresh`` and says the keys change only on Clay's word, but names no verb that writes
them; this is that verb, and it is what the refusal is tested on.

``gh`` runs through ``limits.GuardedRunner`` and is read only here.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Final

import click
import yaml

from superclaude.cli.issue_watch.predicates import valid_repo
from superclaude.cli.issue_watch.runner import Runner

from . import answer_check, common, ext, repos_file
from .state import EXIT_CONFLICT, EXIT_INVALID, StateError

_BRANCH: Final = re.compile(r"[A-Za-z0-9._/-]{1,200}")
_METHOD_KEYS: Final = (
    ("squash", "allow_squash_merge"),
    ("merge", "allow_merge_commit"),
    ("rebase", "allow_rebase_merge"),
)
_PUSH_RIGHTS: Final = ("push", "maintain", "admin")


def read_facts(runner: Runner, repo: str) -> dict[str, Any]:
    """What GitHub says about a repo: default branch, allowed methods, ``protected``, ``can_merge``."""
    try:
        meta = json.loads(ext.run_checked(runner, ["gh", "api", f"repos/{repo}"]))
        branch = meta["default_branch"]
        if not isinstance(branch, str) or _BRANCH.fullmatch(branch) is None:
            raise ValueError
        perms = meta["permissions"]
        tip = json.loads(
            ext.run_checked(runner, ["gh", "api", f"repos/{repo}/branches/{branch}"])
        )
        if not isinstance(perms, dict) or not isinstance(tip.get("protected"), bool):
            raise ValueError
    except (ValueError, KeyError, TypeError, AttributeError, RecursionError):
        raise StateError("external_unreadable", ext.EXIT_EXTERNAL) from None
    return {
        "default_branch": branch,
        "allowed_methods": [m for m, key in _METHOD_KEYS if meta.get(key) is True],
        "protected": tip["protected"],
        "can_merge": any(perms.get(right) is True for right in _PUSH_RIGHTS),
    }


def _find(entries: list[Any], repo: str) -> dict[str, Any] | None:
    return next(
        (
            e
            for e in entries
            if isinstance(e, dict) and str(e.get("repo")).lower() == repo.lower()
        ),
        None,
    )


@click.group(name="repos")
def repos_group() -> None:
    """Check, add and refresh the repos in repos.yaml (the keys that are Clay's alone go through set)."""


@repos_group.command("check")
def check_cmd() -> None:
    """Validate repos.yaml and print what it lists."""

    def action() -> dict[str, Any]:
        root = common.root()
        runner = ext.make_runner("repos")
        doc = repos_file.load_doc(root, runner)
        raw = {
            str(r["repo"]).lower(): r
            for r in yaml.safe_load(repos_file.read_text(root)).get("repos") or []
        }
        listed = []
        for entry in doc.repos:
            extra = raw.get(entry.repo.lower(), {})
            listed.append(
                {
                    "repo": entry.repo,
                    "short": entry.short,
                    "enabled": entry.enabled,
                    "checkout": str(entry.checkout) if entry.checkout else None,
                    "clone_parent": str(entry.clone_parent)
                    if entry.clone_parent
                    else None,
                    "merge_method": entry.merge_method,
                    "release_merge_method": entry.release_merge_method,
                    "release_head": entry.release_head,
                    "reviewers": list(entry.reviewers)
                    if entry.reviewers is not None
                    else None,
                    "merge_safety_files": (
                        list(entry.merge_safety_files)
                        if entry.merge_safety_files is not None
                        else None
                    ),
                    "max_in_flight": entry.max_in_flight,
                    "reach_daily_max": entry.reach_daily_max,
                    "plan_tier": entry.plan_tier,
                    "worker_tier": entry.worker_tier,
                    "orchestrator_tier": entry.orchestrator_tier,
                    "default_branch": extra.get("default_branch"),
                    "protected": extra.get("protected"),
                    "can_merge": extra.get("can_merge"),
                }
            )
        return {
            "orgs": list(doc.orgs),
            "grants": list(doc.grants),
            "tiers": list(doc.tiers),
            "repos": listed,
        }

    common.run(action)


def _method(value: str | None, allowed: list[str], default: str | None) -> str | None:
    if value is None:
        return default
    if value not in allowed:
        raise StateError("method_not_allowed", EXIT_INVALID)
    return value


@repos_group.command("add")
@click.option("--repo", required=True, help="owner/name of the repo to list.")
@click.option(
    "--checkout",
    type=click.Path(path_type=Path),
    default=None,
    help="Absolute path of the clone.",
)
@click.option(
    "--clone-parent",
    type=click.Path(path_type=Path),
    default=None,
    help="Absolute parent folder for a clone.",
)
@click.option(
    "--merge-method",
    default=None,
    help="squash, merge or rebase (one the repo allows).",
)
@click.option(
    "--release-merge-method",
    default=None,
    help="squash, merge or rebase (one the repo allows).",
)
@click.option(
    "--release-head", default=None, help="The release branch, such as integration."
)
@click.option("--reviewers", default=None, help="augment,codex or none.")
@click.option("--max-in-flight", type=click.IntRange(1, 10), default=None)
@click.option("--disabled", is_flag=True, help="List the repo with enabled: false.")
def add_cmd(
    repo,
    checkout,
    clone_parent,
    merge_method,
    release_merge_method,
    release_head,
    reviewers,
    max_in_flight,
    disabled,
) -> None:
    """List a repo: read its rights and settings from GitHub and write them to repos.yaml."""

    def action() -> dict[str, Any]:
        if not valid_repo(repo):
            raise StateError("invalid_input", EXIT_INVALID)
        root = common.root()
        runner = ext.make_runner("repos")
        facts = read_facts(runner, repo)
        allowed = facts["allowed_methods"]
        only = allowed[0] if len(allowed) == 1 else None
        entry: dict[str, Any] = {
            "repo": repo,
            "enabled": facts["can_merge"] and not disabled,
            "checkout": str(checkout) if checkout is not None else None,
            "clone_parent": str(clone_parent) if clone_parent is not None else None,
            "default_branch": facts["default_branch"],
            "merge_method": _method(merge_method, allowed, only),
            "release_merge_method": _method(release_merge_method, allowed, None),
            "release_head": release_head,
            "protected": facts["protected"],
            "can_merge": facts["can_merge"],
        }
        if reviewers is not None:
            entry["reviewers"] = "none" if reviewers == "none" else reviewers.split(",")
        if max_in_flight is not None:
            entry["max_in_flight"] = max_in_flight

        def change(new: dict[str, Any]) -> None:
            items = new.get("repos")
            if items is None:
                items = new["repos"] = []
            if _find(items, repo) is not None:
                raise StateError("already_listed", EXIT_CONFLICT)
            items.append(entry)

        result = repos_file.edit(root, runner, change)
        return {
            "repo": repo,
            "enabled": entry["enabled"],
            "can_merge": entry["can_merge"],
            "merge_method": entry["merge_method"],
            "allowed_methods": allowed,
            "guarded": result["guarded"],
        }

    common.run(action)


@repos_group.command("refresh")
@click.option(
    "--repo", default=None, help="Only this repo (default: every listed repo)."
)
def refresh_cmd(repo) -> None:
    """Read the rights and settings of the listed repos again and update repos.yaml."""

    def action() -> dict[str, Any]:
        root = common.root()
        runner = ext.make_runner("repos")
        text = repos_file.read_text(root)
        names = [
            str(e["repo"])
            for e in yaml.safe_load(text).get("repos") or []
            if isinstance(e, dict)
            and (repo is None or str(e["repo"]).lower() == repo.lower())
        ]
        if repo is not None and not names:
            raise StateError("repo_not_listed", EXIT_INVALID)
        facts = {name: read_facts(runner, name) for name in names}
        report: list[dict[str, Any]] = []

        def change(new: dict[str, Any]) -> None:
            report.clear()
            for name, fact in facts.items():
                entry = _find(new["repos"], name)
                if entry is None:
                    continue  # removed since the read; nothing to update
                changed: dict[str, Any] = {}
                for key in ("default_branch", "protected", "can_merge"):
                    if entry.get(key) != fact[key]:
                        changed[key] = fact[key]
                        entry[key] = fact[key]
                if not fact["can_merge"] and entry.get("enabled") is True:
                    entry["enabled"] = False
                    changed["enabled"] = False
                warnings = [
                    f"{key}_not_allowed"
                    for key in ("merge_method", "release_merge_method")
                    if entry.get(key) is not None
                    and entry[key] not in fact["allowed_methods"]
                ]
                report.append({"repo": name, "changed": changed, "warnings": warnings})

        result = repos_file.edit(root, runner, change)
        return {"repos": list(report), "guarded": result["guarded"]}

    common.run(action)


def question_key(key: str, repo: str | None) -> str:
    """The question key that Clay's answer must have been checked for: ``repos:<key>:<repo or ->``."""
    return f"repos:{key}:{repo if repo is not None else '-'}"


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(v, str) and v for v in value):
        raise StateError("invalid_value", EXIT_INVALID)
    return list(value)


@repos_group.command("set")
@click.option("--key", required=True, type=click.Choice(repos_file.GUARDED_KEYS))
@click.option(
    "--repo", default=None, help="The repo (every key but grants is per repo)."
)
@click.option("--value-json", required=True, help="The new value as JSON.")
@click.option(
    "--answer-ref",
    default=None,
    help="The id of an answer-check that accepted Clay's word.",
)
def set_cmd(key, repo, value_json, answer_ref) -> None:
    """Change grants, reach_daily_max or merge_safety_files, only on Clay's recorded word."""

    def action() -> dict[str, Any]:
        if answer_ref is None:
            raise StateError("answer_ref_required", EXIT_INVALID, keys=[key])
        root = common.root()
        # the OK must have been checked for this very question: an answer to anything
        # else, and an answer already used for a write, never opens a guarded key
        row = answer_check.require_accepted(root, answer_ref, question_key(key, repo))
        try:
            value = json.loads(value_json)
        except (ValueError, RecursionError):
            raise StateError("invalid_value", EXIT_INVALID) from None
        if key == "grants":
            if repo is not None:
                raise StateError("invalid_input", EXIT_INVALID)
            value = _string_list(value)
        else:
            if repo is None or not valid_repo(repo):
                raise StateError("invalid_input", EXIT_INVALID)
            if key == "reach_daily_max":
                if type(value) is not int or not 0 <= value <= 50:
                    raise StateError("invalid_value", EXIT_INVALID)
            else:
                value = _string_list(value)

        def change(new: dict[str, Any]) -> None:
            if key == "grants":
                new["grants"] = value
                return
            entry = _find(new.get("repos") or [], repo)
            if entry is None:
                raise StateError("repo_not_listed", EXIT_INVALID)
            entry[key] = value

        runner = ext.make_runner("repos")
        result = repos_file.edit(root, runner, change, answer_row=row)
        return {"key": key, "repo": repo, "guarded": result["guarded"]}

    common.run(action)
