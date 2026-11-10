"""Reviewer panel template, tier aliases and deterministic resolution.

A tier is an ALIAS for an ordered model list: the alias defaults to the first
model and the others are fallbacks, tried in list order when an earlier one is
unavailable. Panel slots name a tier alias and a strategy; the model lists live
only in the tier file, so one edit there rolls out to every panel that uses the
alias. Adding, removing or reordering a model is a data edit only.

Standard library only.
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import re
import subprocess
from datetime import date
from importlib import resources
from pathlib import Path
from typing import Any, Mapping, Sequence

PANEL_SCHEMA = "review-panel/1"
TIERS_SCHEMA = "review-tiers/1"
RESOLUTION_SCHEMA = "review-panel-resolution/1"

_SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
_TIER = re.compile(r"^tier[0-9]{1,2}[a-z]?$")
_SLOT = re.compile(r"^[a-z0-9]{1,8}$")
_TEMPLATE_ID = re.compile(r"^[a-z0-9][a-z0-9-]{0,31}$")
_ENV_NAME = re.compile(r"^[a-z0-9][a-z0-9-]{0,31}$")
_MODEL_ID = re.compile(r"^[A-Za-z0-9._/:\-\[\]]{1,128}$")
_STRATEGIES = ("fixed", "random", "round_robin")
_KINDS = ("first", "re-review")
_PANEL_KEYS = {
    "schema",
    "template_id",
    "version",
    "description",
    "distinct_across_slots",
    "apply_to",
    "slots",
}
_SLOT_KEYS = {"slot_id", "tier", "count", "strategy", "seed"}


class NoModelAvailable(Exception):
    """No model of a tier (nor a stand-in for it) is available in the environment."""

    def __init__(self, tier: str) -> None:
        super().__init__(f"no model available for {tier}")
        self.tier = tier


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


# ---------------------------------------------------------------- validation


def validate_panel(obj: Any, tiers: Mapping[str, Any] | None = None) -> list[str]:
    """Return the schema errors of a panel template (an empty list means valid)."""
    if not isinstance(obj, dict):
        return ["panel: must be a JSON object"]
    errors: list[str] = []
    for key in obj:
        if key not in _PANEL_KEYS:
            errors.append(f"unknown key '{key}'")
    if obj.get("schema") != PANEL_SCHEMA:
        errors.append(f"schema must be '{PANEL_SCHEMA}'")
    if not isinstance(obj.get("template_id"), str) or not _TEMPLATE_ID.match(
        obj["template_id"]
    ):
        errors.append("template_id must match ^[a-z0-9][a-z0-9-]{0,31}$")
    if not isinstance(obj.get("version"), str) or not _SEMVER.match(obj["version"]):
        errors.append("version must be MAJOR.MINOR.PATCH")
    if not isinstance(obj.get("distinct_across_slots"), bool):
        errors.append("distinct_across_slots must be a boolean")
    if "description" in obj and not isinstance(obj["description"], str):
        errors.append("description must be a string")
    apply_to = obj.get("apply_to")
    if (
        not isinstance(apply_to, list)
        or not apply_to
        or not all(a in _KINDS for a in apply_to)
        or len(set(apply_to)) != len(apply_to)
    ):
        errors.append("apply_to must be a non-empty subset of ['first', 're-review']")
    slots = obj.get("slots")
    if not isinstance(slots, list) or not slots:
        errors.append("slots must be a non-empty list")
        return errors
    seen: set[str] = set()
    fixed = 0
    total = 0
    aliases = (
        tiers.get("aliases")
        if isinstance(tiers, Mapping) and isinstance(tiers.get("aliases"), dict)
        else None
    )
    for i, slot in enumerate(slots):
        where = f"slots[{i}]"
        if not isinstance(slot, dict):
            errors.append(f"{where}: must be an object")
            continue
        for key in slot:
            if key not in _SLOT_KEYS:
                errors.append(f"{where}: unknown key '{key}'")
        sid = slot.get("slot_id")
        if not isinstance(sid, str) or not _SLOT.match(sid):
            errors.append(f"{where}: slot_id must match ^[a-z0-9]{{1,8}}$")
        elif sid in seen:
            errors.append(f"{where}: duplicate slot_id '{sid}'")
        else:
            seen.add(sid)
        tier = slot.get("tier")
        if not isinstance(tier, str) or not _TIER.match(tier):
            errors.append(f"{where}: tier must match ^tier[0-9]{{1,2}}[a-z]?$")
        elif aliases is not None and tier not in aliases:
            errors.append(f"{where}: tier '{tier}' is not defined in the tier file")
        count = slot.get("count")
        if not _is_int(count) or not 1 <= count <= 4:
            errors.append(f"{where}: count must be an integer 1..4")
        else:
            total += count
        strategy = slot.get("strategy")
        if strategy not in _STRATEGIES:
            errors.append(
                f"{where}: strategy must be one of fixed, random, round_robin"
            )
        elif strategy == "fixed":
            fixed += 1
        if "seed" in slot and (not _is_int(slot["seed"]) or strategy != "random"):
            errors.append(
                f"{where}: seed must be an integer and is allowed only with strategy random"
            )
    if fixed != 1:
        errors.append(f"exactly one slot must be 'fixed' (the anchor); found {fixed}")
    if not 1 <= total <= 8:
        errors.append(f"total reviewers must be 1..8; found {total}")
    return errors


def validate_tiers(obj: Any) -> list[str]:
    """Return the schema errors of a tier file (an empty list means valid)."""
    if not isinstance(obj, dict):
        return ["tiers: must be a JSON object"]
    errors: list[str] = []
    if obj.get("schema") != TIERS_SCHEMA:
        errors.append(f"schema must be '{TIERS_SCHEMA}'")
    if not isinstance(obj.get("version"), str) or not _SEMVER.match(obj["version"]):
        errors.append("version must be MAJOR.MINOR.PATCH")
    aliases = obj.get("aliases")
    if not isinstance(aliases, dict) or not aliases:
        errors.append("aliases must be a non-empty object")
        aliases = {}
    for name, entry in aliases.items():
        where = f"aliases.{name}"
        if not _TIER.match(str(name)):
            errors.append(f"{where}: tier name must match ^tier[0-9]{{1,2}}[a-z]?$")
        if not isinstance(entry, dict):
            errors.append(f"{where}: must be an object")
            continue
        alias = entry.get("alias")
        if not isinstance(alias, str) or not _MODEL_ID.match(alias):
            errors.append(
                f"{where}: alias must match ^[A-Za-z0-9._/:\\-\\[\\]]{{1,128}}$"
            )
        models = entry.get("models")
        if not isinstance(models, list) or not models:
            errors.append(f"{where}: models must be a non-empty list")
            continue
        for m in models:
            if not isinstance(m, str) or not _MODEL_ID.match(m):
                errors.append(f"{where}: bad model id {m!r}")
        if len(set(map(str, models))) != len(models):
            errors.append(f"{where}: duplicate model in the list")
    names = obj.get("names", {})
    if not isinstance(names, dict) or not all(
        isinstance(k, str) and isinstance(v, str) for k, v in names.items()
    ):
        errors.append("names must map model ids to display strings")
    envs = obj.get("environments")
    if not isinstance(envs, dict) or not envs:
        errors.append("environments must be a non-empty object")
        envs = {}
    for ename, env in envs.items():
        where = f"environments.{ename}"
        if not _ENV_NAME.match(str(ename)):
            errors.append(
                f"{where}: environment name must match ^[a-z0-9][a-z0-9-]{{0,31}}$"
            )
        if not isinstance(env, dict):
            errors.append(f"{where}: must be an object")
            continue
        available = env.get("available")
        if available != "all" and not (
            isinstance(available, list)
            and available
            and all(isinstance(a, str) and _MODEL_ID.match(a) for a in available)
        ):
            errors.append(
                f"{where}: available must be 'all' or a non-empty list of model ids"
            )
            available = None
        stand_ins = env.get("stand_ins")
        if not isinstance(stand_ins, dict):
            errors.append(f"{where}: stand_ins must be an object")
            stand_ins = {}
        for tier, ids in stand_ins.items():
            if tier not in aliases:
                errors.append(
                    f"{where}: stand_ins names tier '{tier}' that is not defined in aliases"
                )
            if (
                not isinstance(ids, list)
                or not ids
                or not all(isinstance(i, str) for i in ids)
            ):
                errors.append(
                    f"{where}: stand_ins.{tier} must be a non-empty list of model ids"
                )
                continue
            if isinstance(available, list):
                for i in ids:
                    if i not in available:
                        errors.append(
                            f"{where}: stand_ins.{tier} id '{i}' is not in available"
                        )
        launch = env.get("launch")
        if not isinstance(launch, dict) or not all(
            isinstance(k, str) and isinstance(v, str) for k, v in launch.items()
        ):
            errors.append(f"{where}: launch must map model ids to launcher strings")
        if "note" in env and not isinstance(env["note"], str):
            errors.append(f"{where}: note must be a string")
        for key in env:
            if key not in {"available", "stand_ins", "launch", "note"}:
                errors.append(f"{where}: unknown key '{key}'")
    return errors


# ---------------------------------------------------------------- loading


def _project_root() -> Path:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
        top = out.stdout.strip()
        if top:
            return Path(top)
    except (OSError, subprocess.SubprocessError):
        pass
    return Path.cwd()


def find_path(
    kind: str, explicit: str | None = None, environ: Mapping[str, str] | None = None
) -> Path | None:
    """First existing file of the lookup precedence, or None for the packaged default.

    kind is 'panel' or 'tiers'. Precedence: explicit path; the environment variable
    (SUPERCLAUDE_REVIEW_PANEL / SUPERCLAUDE_REVIEW_TIERS); <project>/.superclaude/review-<kind>.json;
    ~/.superclaude/review-<kind>.json.
    """
    env = os.environ if environ is None else environ
    if explicit:
        return Path(explicit)
    var = env.get(
        "SUPERCLAUDE_REVIEW_PANEL" if kind == "panel" else "SUPERCLAUDE_REVIEW_TIERS"
    )
    if var:
        return Path(var)
    fname = "review-panel.json" if kind == "panel" else "review-tiers.json"
    for base in (_project_root() / ".superclaude", Path.home() / ".superclaude"):
        candidate = base / fname
        if candidate.is_file():
            return candidate
    return None


def _default(name: str) -> dict:
    ref = resources.files("superclaude.cli.review") / "data" / name
    return json.loads(ref.read_text(encoding="utf-8"))


def load_panel(path: str | None = None) -> dict:
    found = find_path("panel", path)
    obj = (
        json.loads(found.read_text(encoding="utf-8"))
        if found
        else _default("review-panel.default.json")
    )
    errors = validate_panel(obj)
    if errors:
        raise ValueError(
            f"invalid panel template{f' {found}' if found else ''}: "
            + "; ".join(errors)
        )
    return obj


def load_tiers(path: str | None = None) -> dict:
    found = find_path("tiers", path)
    obj = (
        json.loads(found.read_text(encoding="utf-8"))
        if found
        else _default("review-tiers.default.json")
    )
    errors = validate_tiers(obj)
    if errors:
        raise ValueError(
            f"invalid tier file{f' {found}' if found else ''}: " + "; ".join(errors)
        )
    return obj


def select_env(env: str | None = None, environ: Mapping[str, str] | None = None) -> str:
    """--env; else $SUPERCLAUDE_REVIEW_ENV; else 'gateway' when $T3Model01 is non-empty; else 'anthropic-only'."""
    e = os.environ if environ is None else environ
    if env:
        return env
    if e.get("SUPERCLAUDE_REVIEW_ENV"):
        return e["SUPERCLAUDE_REVIEW_ENV"]
    if e.get("T3Model01"):
        return "gateway"
    return "anthropic-only"


# ---------------------------------------------------------------- resolution


def resolve_slot(
    models: Sequence[str],
    strategy: str,
    seed: Any,
    available: Any,
    stand_ins: Sequence[str],
    exclude: Sequence[str] = (),
) -> dict:
    """Pick one model for a slot instance. Pure and deterministic.

    models: the tier alias's ordered list. available: 'all' or a list of ids. stand_ins: the
    environment's ordered stand-in list for this tier. For round_robin, seed carries the sequence number.
    """
    candidates = [m for m in models if available == "all" or m in available]
    source = list(models)
    stand = False
    if not candidates:
        candidates = [m for m in stand_ins if available == "all" or m in available]
        source = list(stand_ins)
        stand = True
        if not candidates:
            raise NoModelAvailable(",".join(models))
    if strategy == "fixed":
        model = candidates[0]
    elif strategy == "random":
        pool = [m for m in candidates if m not in set(exclude)] or candidates
        model = random.Random(seed).choice(pool)
    elif strategy == "round_robin":
        model = candidates[int(seed) % len(candidates)]
    else:
        raise ValueError(f"unknown strategy {strategy!r}")
    k = candidates.index(model)
    return {
        "model": model,
        "fallback_depth": source.index(model),
        "stand_in": stand,
        "fallbacks": candidates[k + 1 :] + candidates[:k],
    }


def sha256_json(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def resolve(
    panel: Mapping[str, Any],
    tiers: Mapping[str, Any],
    env: str,
    run_id: str,
    review_kind: str = "first",
    seed: int | None = None,
    sequence: int | None = None,
) -> dict:
    """Resolve a panel template into the reviewer list (schema review-panel-resolution/1)."""
    environments = tiers["environments"]
    if env not in environments:
        raise ValueError(
            f"unknown environment '{env}' (known: {', '.join(sorted(environments))})"
        )
    environment = environments[env]
    available = environment["available"]
    launch = environment.get("launch", {})
    names = tiers.get("names", {})
    slots = list(panel["slots"])
    fixed = [s for s in slots if s["strategy"] == "fixed"]
    rest = [s for s in slots if s["strategy"] != "fixed"]
    if review_kind in panel["apply_to"]:
        order = fixed + rest
        expand = True
    else:
        order = fixed
        expand = False
    base = (
        seed
        if seed is not None
        else int(hashlib.sha256(run_id.encode("utf-8")).hexdigest()[:8], 16)
    )
    reviewers: list[dict] = []
    chosen: list[str] = []
    for slot in order:
        entry = tiers["aliases"][slot["tier"]]
        count = slot["count"] if expand else 1
        for i in range(1, count + 1):
            strategy = slot["strategy"]
            if strategy == "random":
                slot_seed: Any = (
                    f"{slot['seed'] if 'seed' in slot else base}|{slot['slot_id']}|{i}"
                )
            elif strategy == "round_robin":
                slot_seed = (
                    (sequence if sequence is not None else date.today().toordinal())
                    + i
                    - 1
                )
            else:
                slot_seed = None
            exclude = tuple(chosen) if panel["distinct_across_slots"] else ()
            picked = resolve_slot(
                entry["models"],
                strategy,
                slot_seed,
                available,
                environment.get("stand_ins", {}).get(slot["tier"], []),
                exclude,
            )
            chosen.append(picked["model"])
            reviewers.append(
                {
                    "reviewer_id": f"{slot['slot_id']}-{i}",
                    "slot_id": slot["slot_id"],
                    "tier": slot["tier"],
                    "alias": entry["alias"],
                    "strategy": strategy,
                    "seed": slot_seed,
                    "model": picked["model"],
                    "model_name": names.get(picked["model"], picked["model"]),
                    "fallback_depth": picked["fallback_depth"],
                    "stand_in": picked["stand_in"],
                    "fallbacks": picked["fallbacks"],
                    "launch": launch.get(picked["model"]),
                }
            )
    return {
        "schema": RESOLUTION_SCHEMA,
        "template_id": panel["template_id"],
        "template_version": panel["version"],
        "template_sha256": sha256_json(panel),
        "tiers_version": tiers["version"],
        "tiers_sha256": sha256_json(tiers),
        "environment": env,
        "run_id": run_id,
        "review_kind": review_kind,
        "reviewers": reviewers,
    }
