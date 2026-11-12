"""Coordinator-owned run manifest of the reflect panel (`<out>/panel/manifest.json`, schema review-panel-manifest/1).

One coordinator writes the manifest; reviewer agents only return data. The run moves through the states
frozen -> resolved -> dispatched -> collected -> calibrated -> clustered -> debated -> validated -> published, one
step at a time, with the terminal state failed. A reader accepts only a manifest whose state is published
(`read_committed`); every other state is work in progress.

frozen records the reference to artifacts/input-snapshot.yaml with its input_tree_sha256, the template, tiers and
brief-template sha256, the schema ids, the run id, and the requested and effective engine. policy_sha256 is the sha256
of the canonical JSON of the template, tiers and brief-template hashes and the schema ids. Each later state records the
sha256 of its payload and of the outputs it committed, and the dependency hashes it was built on.

Idempotency identity: (run_id, input_tree_sha256, policy_sha256, stage, reviewer_id, attempt_id); the first three are
fixed by the manifest, so a submission is keyed by (stage, reviewer_id, attempt_id) inside it. The same payload hash
under the same identity is a no-op; a different payload under the same identity raises Conflict. A stage-level
submission has an empty reviewer_id and attempt_id. A new attempt of a reviewer supersedes an earlier attempt of that
reviewer only when the earlier one did not complete; it never adds a vote (reviewers_complete counts reviewers, not
attempts) and never clears a finding.

Counts are top-level keys: reviewers_requested and reviewers_resolved (set by the resolved stage) and
reviewers_complete (reviewers whose latest collected-stage attempt completed). Resume reuses a stage only when its
dependency hashes still match; a changed input_tree_sha256 (a changed plan or spec) or policy starts a new invocation.

Publish writes REPORT.md, return-contract.yaml and audit.log to same-directory temporaries, renames them, then commits
published in the manifest. In shadow mode the legacy writers stay authoritative for those three files: `published`
records their hashes after the legacy writers finish and does not rewrite them.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any, Callable

SCHEMA = "review-panel-manifest/1"
STATES = (
    "frozen",
    "resolved",
    "dispatched",
    "collected",
    "calibrated",
    "clustered",
    "debated",
    "validated",
    "published",
)
FAILED = "failed"
ENGINES = ("legacy", "shadow", "panel")
COMPLETIONS = ("complete", "truncated", "invalid", "failed", "timed_out")
PER_REVIEWER_STAGES = ("dispatched", "collected", "calibrated")
PUBLISH_FILES = ("REPORT.md", "return-contract.yaml", "audit.log")
FROZEN_FIELDS = (
    "snapshot_ref",
    "snapshot_sha256",
    "input_tree_sha256",
    "template_sha256",
    "tiers_sha256",
    "brief_template_sha256",
    "schema_ids",
)
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


class ManifestError(Exception):
    """Base class of every manifest refusal."""


class Conflict(ManifestError):
    """A different payload under an identity that already holds one, or a second vote for a reviewer."""


class OutOfOrder(ManifestError):
    """A stage submitted out of order, after failure, or after its stage was committed."""


class NotCommitted(ManifestError):
    """A reader met a manifest that is not in the published state."""


class Invalid(ManifestError):
    """A malformed payload or manifest."""


def sha256_json(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def policy_sha256(frozen: dict) -> str:
    return sha256_json(
        {
            k: frozen.get(k)
            for k in (
                "template_sha256",
                "tiers_sha256",
                "brief_template_sha256",
                "schema_ids",
            )
        }
    )


def new_manifest(
    *,
    run_id: str,
    frozen: dict,
    engine_requested: str,
    engine_effective: str,
    invocation: int = 1,
    history: list | None = None,
) -> dict:
    """A manifest in the frozen state."""
    m = {
        "schema": SCHEMA,
        "run_id": run_id,
        "invocation": invocation,
        "history": list(history or []),
        "t2_engine_requested": engine_requested,
        "t2_engine_effective": engine_effective,
        "frozen": {k: frozen.get(k) for k in FROZEN_FIELDS},
        "input_tree_sha256": frozen.get("input_tree_sha256"),
        "policy_sha256": policy_sha256(frozen),
        "state": "frozen",
        "stages": {
            "frozen": {
                "payload_sha256": sha256_json(
                    {k: frozen.get(k) for k in FROZEN_FIELDS}
                ),
                "outputs": {},
                "deps": {},
                "invocation": invocation,
            }
        },
        "attempts": [],
        "reviewers_requested": None,
        "reviewers_resolved": None,
        "reviewers_complete": 0,
    }
    errors = validate(m)
    if errors:
        raise Invalid("; ".join(errors))
    return m


# ---------------------------------------------------------------- reading and writing


def save(path: Path, manifest: dict) -> None:
    """Write the manifest atomically (same-directory temporary, then rename)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    tmp.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    os.replace(tmp, path)


def load(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise Invalid(f"cannot read manifest {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise Invalid(f"manifest {path} is not a JSON object")
    return data


def read_committed(path: Path) -> dict:
    """A reader's entry point: the manifest, only when it is valid and in the published state."""
    manifest = load(path)
    errors = validate(manifest)
    if errors:
        raise Invalid("; ".join(errors))
    if manifest["state"] != "published":
        raise NotCommitted(
            f"manifest state is {manifest['state']!r}, not 'published'; a reader accepts only a committed manifest"
        )
    return manifest


# ---------------------------------------------------------------- validation


def validate(m: Any) -> list[str]:
    """Structural errors of a manifest (an empty list means valid)."""
    if not isinstance(m, dict):
        return ["manifest must be a JSON object"]
    errors: list[str] = []
    if m.get("schema") != SCHEMA:
        errors.append(f"schema must be {SCHEMA!r}")
    if not isinstance(m.get("run_id"), str) or not m.get("run_id"):
        errors.append("run_id must be a non-empty string")
    for key in ("t2_engine_requested", "t2_engine_effective"):
        if m.get(key) not in ENGINES:
            errors.append(f"{key} is missing or not one of {', '.join(ENGINES)}")
    frozen = m.get("frozen")
    if not isinstance(frozen, dict):
        errors.append("frozen must be an object")
    else:
        for key in (
            "input_tree_sha256",
            "template_sha256",
            "tiers_sha256",
            "brief_template_sha256",
        ):
            if not isinstance(frozen.get(key), str) or not _HEX64.match(frozen[key]):
                errors.append(
                    f"frozen.{key} must be a 64-character lowercase hex sha256"
                )
        if not isinstance(frozen.get("snapshot_ref"), str) or not frozen.get(
            "snapshot_ref"
        ):
            errors.append("frozen.snapshot_ref must be a non-empty string")
        ids = frozen.get("schema_ids")
        if (
            not isinstance(ids, list)
            or not ids
            or not all(isinstance(i, str) for i in ids)
        ):
            errors.append("frozen.schema_ids must be a non-empty list of strings")
        if m.get("input_tree_sha256") != frozen.get("input_tree_sha256"):
            errors.append("input_tree_sha256 differs from frozen.input_tree_sha256")
        if m.get("policy_sha256") != policy_sha256(frozen):
            errors.append("policy_sha256 does not match the frozen policy fields")
    state = m.get("state")
    if state not in (*STATES, FAILED):
        errors.append(f"state must be one of {', '.join((*STATES, FAILED))}")
    stages = m.get("stages")
    if not isinstance(stages, dict):
        errors.append("stages must be an object")
    elif state in STATES:
        # every stage from frozen up to the state has been committed, none skipped
        for s in STATES[: STATES.index(state) + 1]:
            if s not in stages:
                errors.append(f"stage {s!r} is missing although the state is {state!r}")
    for key in ("reviewers_requested", "reviewers_resolved"):
        v = m.get(key)
        if v is not None and (isinstance(v, bool) or not isinstance(v, int) or v < 0):
            errors.append(f"{key} must be null or a non-negative integer")
    v = m.get("reviewers_complete")
    if isinstance(v, bool) or not isinstance(v, int) or v < 0:
        errors.append("reviewers_complete must be a non-negative integer")
    if not isinstance(m.get("attempts"), list):
        errors.append("attempts must be a list")
    return errors


# ---------------------------------------------------------------- advancing


def _next_state(state: str) -> str | None:
    if state not in STATES or state == STATES[-1]:
        return None
    return STATES[STATES.index(state) + 1]


def _prev_hash(m: dict, stage: str) -> str:
    return m["stages"][STATES[STATES.index(stage) - 1]]["payload_sha256"]


def _recount(m: dict) -> None:
    latest: dict[str, str] = {}
    for a in m["attempts"]:
        if a["stage"] == "collected":
            latest[a["reviewer_id"]] = a["completion"]
    m["reviewers_complete"] = sum(1 for c in latest.values() if c == "complete")


def advance_stage(m: dict, stage: str, payload: dict | None = None) -> bool:
    """Commit `stage` with `payload`; True when the manifest changed, False for an identical replay."""
    payload = payload or {}
    if stage not in STATES or stage == "frozen":
        raise OutOfOrder(f"{stage!r} is not a stage that can be advanced to")
    if not isinstance(payload, dict):
        raise Invalid("payload must be a JSON object")
    outputs = payload.get("outputs", {})
    if not isinstance(outputs, dict) or not all(
        isinstance(k, str) and isinstance(v, str) and _HEX64.match(v)
        for k, v in outputs.items()
    ):
        raise Invalid(
            "payload.outputs must map names to 64-character lowercase hex sha256 values"
        )
    digest = sha256_json(payload)
    existing = m["stages"].get(stage)
    if existing is not None:
        if existing["payload_sha256"] == digest:
            return False
        raise Conflict(
            f"stage {stage!r} already holds a different payload for this run, input and policy"
        )
    if m["state"] == FAILED:
        raise OutOfOrder("the run has failed; no stage can be advanced")
    expected = _next_state(m["state"])
    if stage != expected:
        raise OutOfOrder(
            f"cannot advance to {stage!r}: the state is {m['state']!r} and the next stage is {expected!r}"
        )
    if stage == "resolved":
        req, res = payload.get("reviewers_requested"), payload.get("reviewers_resolved")
        for name, value in (("reviewers_requested", req), ("reviewers_resolved", res)):
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise Invalid(
                    f"the resolved payload needs {name} as a non-negative integer"
                )
        if res > req:
            raise Invalid("reviewers_resolved cannot exceed reviewers_requested")
        m["reviewers_requested"], m["reviewers_resolved"] = req, res
    m["stages"][stage] = {
        "payload_sha256": digest,
        "outputs": dict(outputs),
        "deps": {
            "prev": _prev_hash(m, stage),
            "input_tree_sha256": m["input_tree_sha256"],
            "policy_sha256": m["policy_sha256"],
        },
        "invocation": m["invocation"],
    }
    m["state"] = stage
    return True


def record_attempt(
    m: dict,
    stage: str,
    reviewer_id: str,
    attempt_id: str,
    completion: str,
    payload: dict | None = None,
) -> bool:
    """Record one attempt of one reviewer in an open per-reviewer stage; False for an identical replay."""
    if stage not in PER_REVIEWER_STAGES:
        raise OutOfOrder(
            f"attempts are recorded only for {', '.join(PER_REVIEWER_STAGES)}"
        )
    if completion not in COMPLETIONS:
        raise Invalid(f"completion must be one of {', '.join(COMPLETIONS)}")
    if not reviewer_id or not attempt_id:
        raise Invalid("reviewer_id and attempt_id are required for an attempt")
    entry = {
        "stage": stage,
        "reviewer_id": reviewer_id,
        "attempt_id": attempt_id,
        "completion": completion,
        "payload_sha256": sha256_json({"completion": completion, **(payload or {})}),
    }
    for a in m["attempts"]:
        if (a["stage"], a["reviewer_id"], a["attempt_id"]) == (
            stage,
            reviewer_id,
            attempt_id,
        ):
            if (a["completion"], a["payload_sha256"]) == (
                completion,
                entry["payload_sha256"],
            ):
                return False
            raise Conflict(
                f"attempt {attempt_id!r} of {reviewer_id!r} in {stage!r} already holds a different payload"
            )
    if m["state"] == FAILED:
        raise OutOfOrder("the run has failed; no attempt can be recorded")
    if stage in m["stages"] or _next_state(m["state"]) != stage:
        raise OutOfOrder(f"stage {stage!r} is not open: the state is {m['state']!r}")
    earlier = [
        a
        for a in m["attempts"]
        if a["stage"] == stage and a["reviewer_id"] == reviewer_id
    ]
    if earlier and earlier[-1]["completion"] == "complete":
        raise Conflict(
            f"{reviewer_id!r} already completed {stage!r}; a new attempt would add a vote"
        )
    if earlier:
        earlier[-1]["superseded_by"] = attempt_id
    m["attempts"].append(entry)
    _recount(m)
    return True


def fail(m: dict, reason: str) -> None:
    """Move the run to the terminal failed state (no-op when already failed)."""
    if m["state"] == "published":
        raise OutOfOrder("a published run cannot fail")
    if m["state"] == FAILED:
        return  # the first failure reason stays
    m["state"] = FAILED
    m["failure_reason"] = reason


# ---------------------------------------------------------------- resume


def reusable_stages(m: dict) -> list[str]:
    """The committed stages whose dependency hashes still match, as a prefix of the stage order."""
    reusable: list[str] = []
    for stage in STATES[1:]:
        rec = m["stages"].get(stage)
        prev = m["stages"].get(STATES[STATES.index(stage) - 1])
        deps = (rec or {}).get("deps")
        if (
            rec is None
            or prev is None
            or not isinstance(deps, dict)
            or deps.get("input_tree_sha256") != m["input_tree_sha256"]
            or deps.get("policy_sha256") != m["policy_sha256"]
            or deps.get("prev") != prev["payload_sha256"]
        ):
            break
        reusable.append(stage)
    return reusable


def resume(
    m: dict,
    *,
    frozen: dict,
    run_id: str | None = None,
    engine_requested: str | None = None,
    engine_effective: str | None = None,
) -> tuple[dict, bool]:
    """(manifest, new_invocation): the same manifest when the freshly computed frozen fields match, else a new one.

    A changed input_tree_sha256 (a changed plan or spec), policy hash or engine decision starts a new invocation at
    frozen; the earlier invocation is kept in `history`. A different run_id is a different run and raises Conflict:
    it must not inherit this run's stages and attempts. The run id and engines default to the stored values.
    """
    if run_id is not None and run_id != m["run_id"]:
        raise Conflict(
            f"manifest belongs to run {m['run_id']!r}, not {run_id!r}; use another output directory"
        )
    requested = engine_requested or m["t2_engine_requested"]
    effective = engine_effective or m["t2_engine_effective"]
    now = {k: frozen.get(k) for k in FROZEN_FIELDS}
    same = (
        now["input_tree_sha256"] == m["frozen"].get("input_tree_sha256")
        and policy_sha256(now) == m["policy_sha256"]
        and (requested, effective)
        == (m["t2_engine_requested"], m["t2_engine_effective"])
    )
    if same:
        return m, False
    history = [
        *m.get("history", []),
        {
            "invocation": m["invocation"],
            "input_tree_sha256": m["input_tree_sha256"],
            "policy_sha256": m["policy_sha256"],
            "state": m["state"],
        },
    ]
    return (
        new_manifest(
            run_id=m["run_id"],
            frozen=now,
            engine_requested=requested,
            engine_effective=effective,
            invocation=m["invocation"] + 1,
            history=history,
        ),
        True,
    )


# ---------------------------------------------------------------- publish


def publish_files(
    out_dir: Path,
    contents: dict[str, bytes],
    manifest_path: Path,
    *,
    commit: Callable[[Path, dict[str, str]], None] | None = None,
) -> dict[str, str]:
    """Write `contents` (REPORT.md, return-contract.yaml, audit.log) atomically, then commit `published`.

    Each file goes to a same-directory temporary and is renamed into place; only after all renames does `commit`
    (default: advance the manifest to published with the files' hashes) run. A crash between the renames and the
    commit leaves a manifest without `published`, which `read_committed` refuses. Returns the sha256 of each file.
    Before any file is written the manifest must be in the validated state and its effective engine must not be
    shadow (the legacy writers own the files there); a manifest already published accepts only identical files.
    """
    if set(contents) != set(PUBLISH_FILES):
        raise Invalid(f"publish needs exactly {', '.join(PUBLISH_FILES)}")
    hashes = {name: hashlib.sha256(data).hexdigest() for name, data in contents.items()}
    # Check that the manifest can accept `published` BEFORE any file is touched.
    manifest = load(manifest_path)
    if manifest.get("t2_engine_effective") == "shadow":
        raise OutOfOrder(
            "shadow mode: the legacy writers stay authoritative for the published files; record their hashes "
            "with `advance published` instead of publishing"
        )
    if manifest.get("state") == "published":
        if manifest["stages"]["published"]["outputs"] == hashes:
            return hashes  # identical replay: nothing to write
        raise Conflict("stage 'published' already holds different files for this run")
    if manifest.get("state") != "validated":
        raise OutOfOrder(
            f"cannot publish: the state is {manifest.get('state')!r}, not 'validated'"
        )
    out_dir.mkdir(parents=True, exist_ok=True)
    temporaries = {}
    for name, data in contents.items():
        tmp = out_dir / f".{name}.tmp-{os.getpid()}"
        tmp.write_bytes(data)
        temporaries[name] = tmp
    for name, tmp in temporaries.items():
        os.replace(tmp, out_dir / name)
    (commit or commit_published)(manifest_path, hashes)
    return hashes


def commit_published(manifest_path: Path, hashes: dict[str, str]) -> None:
    m = load(manifest_path)
    advance_stage(m, "published", {"outputs": hashes})
    save(manifest_path, m)


def hash_published_files(out_dir: Path) -> dict[str, str]:
    """sha256 of the three publish files already in out_dir (shadow mode: the legacy writers wrote them)."""
    missing = [n for n in PUBLISH_FILES if not (out_dir / n).is_file()]
    if missing:
        raise Invalid(
            f"cannot record published: {', '.join(missing)} not found in {out_dir}"
        )
    return {n: sha256_file(out_dir / n) for n in PUBLISH_FILES}
