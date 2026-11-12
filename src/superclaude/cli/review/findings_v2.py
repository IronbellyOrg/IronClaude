"""Findings block findings-v2: the findings-v1 container with the fence info string findings-v2.

A line that findings-v1 accepts and whose keys are all in V1_FIELDS passes check_finding unchanged.
A findings-v1-valid line with other keys may be rejected: a line that carries calibrated_confidence is rejected.
Prior lines are rejected.
observed_rows is supplied by the caller.
"""

from __future__ import annotations

import json
from pathlib import PurePosixPath, PureWindowsPath
from typing import Any, Collection, Iterable

from superclaude.cli.review.findings import (
    _HEAD_FINDINGS,
    _ID,
    CATEGORIES,
    SEVERITIES,
    _blocks_after,
    _check_flat,
)

INFO = "findings-v2"
V1_FIELDS = (
    "id",
    "severity",
    "blocking",
    "category",
    "anchor",
    "anchor2",
    "refs",
    "claim",
)
ROLES = ("plan", "spec", "source", "test", "diff", "artifact")
LENSES = ("spec", "reflect-pre", "reflect-post")
CHANNELS = ("defect", "grounding-gap", "advisory")
DEVIATION_CLASSES = ("authorized", "necessary", "drift", "regression", "none")
# parse_block returns complete, truncated or invalid; failed and timed_out are for callers.
COMPLETION_STATES = ("complete", "truncated", "invalid", "failed", "timed_out")
REFLECT_CATEGORIES = {
    "ordering": ("other",),
    "acceptance": ("unpassable-check",),
    "coverage": ("missing-requirement",),
    "contradiction": ("contradiction",),
    "risk": ("safety", "other"),
    "deviation": ("other",),
}


def _one_of(value: Any, allowed: Collection[str]) -> bool:
    return isinstance(value, str) and value in allowed


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _check_citation(c: Any) -> str | None:
    if not isinstance(c, dict):
        return "a citation must be an object"
    if not _one_of(c.get("role"), ROLES):
        return "citation role must be plan, spec, source, test, diff or artifact"
    path = c.get("path")
    if not isinstance(path, str) or not path:
        return "citation path must be a non-empty string"
    win = PureWindowsPath(path)
    if (
        PurePosixPath(path).is_absolute()
        or win.is_absolute()
        or win.drive
        or path.startswith(("\\", "/"))
        or ".." in path.replace("\\", "/").split("/")
    ):
        return "citation path must be repo-relative"
    start, end = c.get("line_start"), c.get("line_end")
    if not _is_int(start) or not _is_int(end) or start < 1 or end < start:
        return "citation line_start and line_end must be integers with 1 <= line_start <= line_end"
    if c.get("quote") is not None:
        return _check_flat(c["quote"], "citation quote", 12, 200)
    return None


def check_finding(
    obj: dict,
    seen: set[str],
    *,
    lens: str | None = None,
    assigned_rows: Collection[str] | None = None,
) -> str | None:
    """An error message for one findings-v2 line, or None when the line is valid; obj is not changed.

    reflect_category, citations, deviation_class, coverage_rows, self_confidence, lens, channel, anchor2
    and a citation quote are treated as absent when set to null.
    """
    if "calibrated_confidence" in obj:
        return "calibrated_confidence is not allowed in a findings-v2 line"
    fid = obj.get("id")
    if not isinstance(fid, str) or not _ID.match(fid):
        return "id must match ^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$"
    if fid in seen:
        return f"duplicate id '{fid}'"
    if not _one_of(obj.get("severity"), SEVERITIES):
        return "severity must be CRITICAL, MAJOR or MINOR"
    if not isinstance(obj.get("blocking"), bool):
        return "blocking must be a boolean"
    if obj["blocking"] and obj["severity"] == "MINOR":
        return "a MINOR finding cannot be blocking"
    if not _one_of(obj.get("category"), CATEGORIES):
        return "category is not one of the allowed values"
    err = _check_flat(obj.get("claim"), "claim", None, 300)
    if err:
        return err
    refs = obj.get("refs", [])
    if (
        not isinstance(refs, list)
        or len(refs) > 8
        or not all(isinstance(r, str) for r in refs)
    ):
        return "refs must be a list of at most 8 strings"

    citations = obj.get("citations")
    if citations is None:
        if obj.get("anchor") is None:
            return "a finding needs an anchor or citations"
        err = _check_flat(obj["anchor"], "anchor", 12, 200)
    else:
        if not isinstance(citations, list) or not 1 <= len(citations) <= 8:
            return "citations must be a list of 1 to 8 citations"
        err = next((e for e in map(_check_citation, citations) if e), None)
        if not err and obj.get("anchor") is not None:
            err = _check_flat(obj["anchor"], "anchor", 12, 200)
    if err:
        return err
    if obj.get("anchor2") is not None:
        err = _check_flat(obj["anchor2"], "anchor2", 12, 200)
        if err:
            return err

    line_lens = obj.get("lens")
    if line_lens is not None and lens is not None and line_lens != lens:
        return f"the line's lens {line_lens!r} differs from the block lens {lens!r}"
    effective = line_lens if line_lens is not None else lens
    if effective is not None and not _one_of(effective, LENSES):
        return "lens must be spec, reflect-pre or reflect-post"

    dclass = obj.get("deviation_class")
    if dclass is None and effective == "reflect-post":
        return "deviation_class is required when the lens is reflect-post"
    if dclass is not None and not _one_of(dclass, DEVIATION_CLASSES):
        return (
            "deviation_class must be authorized, necessary, drift, regression or none"
        )

    rcat = obj.get("reflect_category")
    if rcat is not None:
        if not _one_of(rcat, REFLECT_CATEGORIES):
            return "reflect_category is not one of the allowed values"
        if obj["category"] not in REFLECT_CATEGORIES[rcat]:
            return f"reflect_category {rcat} needs category {' or '.join(REFLECT_CATEGORIES[rcat])}"
        if obj["blocking"] != (obj["severity"] != "MINOR"):
            return "with reflect_category set, a MAJOR or CRITICAL finding must be blocking and a MINOR one must not"
        if rcat == "deviation" and dclass is None:
            return "reflect_category deviation needs deviation_class"

    rows = obj.get("coverage_rows")
    if rows is not None:
        if not isinstance(rows, list) or not all(isinstance(r, str) for r in rows):
            return "coverage_rows must be a list of strings"
        if rows and assigned_rows is None:
            return (
                "coverage_rows is set but there is no Coverage slice to check against"
            )
        outside = [r for r in rows if r not in (assigned_rows or ())]
        if outside:
            return f"coverage_rows {outside} are not in the assigned Coverage slice"

    conf = obj.get("self_confidence")
    if conf is not None and not (
        isinstance(conf, (int, float)) and not isinstance(conf, bool) and 0 <= conf <= 1
    ):
        return "self_confidence must be a number from 0 to 1"

    channel = obj.get("channel")
    if channel is not None and not _one_of(channel, CHANNELS):
        return "channel must be defect, grounding-gap or advisory"
    return None


def channel_of(f: dict) -> str:
    """The finding's channel, or defect when the channel is absent or not an allowed value."""
    ch = f.get("channel")
    return ch if _one_of(ch, CHANNELS) else "defect"


def parse_block(
    text: str,
    *,
    lens: str | None = None,
    assigned_rows: Iterable[str] | None = None,
    observed_rows: Iterable[str] = (),
) -> dict:
    """Parse the findings-v2 block of text into {ok, state, findings, errors}; ok is True only when the state is complete.

    The state is truncated when the block is not closed, invalid on any other error, else complete.
    A closed, error-free empty block is complete only when assigned_rows is non-empty and every assigned row is in observed_rows.
    """
    res: dict[str, Any] = {
        "ok": True,
        "state": "complete",
        "findings": [],
        "errors": [],
    }
    found, blocks = _blocks_after(text, _HEAD_FINDINGS, INFO)
    if not found:
        res["errors"].append(
            {"line": 0, "msg": "heading '## Findings block' is missing"}
        )
    elif not blocks:
        res["errors"].append(
            {
                "line": 0,
                "msg": f"no fenced block with info string {INFO} after the heading",
            }
        )
    closed = True
    if blocks:
        if len(blocks) > 1:
            res["errors"].append(
                {
                    "line": blocks[-1][0],
                    "msg": f"more than one {INFO} block; the last one is used",
                }
            )
        closed = blocks[-1][2]
        if not closed:
            res["errors"].append(
                {
                    "line": blocks[-1][0],
                    "msg": f"the {INFO} block is not closed: the text ends inside it (truncated)",
                }
            )
        rows = None if assigned_rows is None else set(map(str, assigned_rows))
        seen: set[str] = set()
        for lineno, raw in blocks[-1][1]:
            if not raw.strip():
                continue
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError as exc:
                res["errors"].append(
                    {"line": lineno, "msg": f"not valid JSON: {exc.msg}"}
                )
                continue
            if not isinstance(obj, dict):
                res["errors"].append(
                    {"line": lineno, "msg": "a line must be a JSON object"}
                )
                continue
            if "prior" in obj:
                res["errors"].append(
                    {"line": lineno, "msg": f"{INFO} does not accept prior lines"}
                )
                continue
            err = check_finding(obj, seen, lens=lens, assigned_rows=rows)
            if err:
                res["errors"].append({"line": lineno, "msg": err})
                continue
            seen.add(obj["id"])
            obj.setdefault("refs", [])
            res["findings"].append(obj)
        if closed and not res["errors"] and not res["findings"]:
            if not rows or not rows <= set(observed_rows):
                res["errors"].append(
                    {
                        "line": blocks[-1][0],
                        "msg": "an empty block is complete only with a coverage observation for every assigned row",
                    }
                )
    if not closed:
        res["state"] = "truncated"
    elif res["errors"]:
        res["state"] = "invalid"
    res["ok"] = res["state"] == "complete"
    return res
