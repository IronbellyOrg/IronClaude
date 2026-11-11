"""Findings block (findings-v1), fix map (fixmap-v1), anchors, fingerprints and clusters.

Everything here is deterministic and uses the standard library only.
"""

from __future__ import annotations

import difflib
import hashlib
import json
import re
from typing import Any, Iterable, Sequence

SEVERITIES = ("CRITICAL", "MAJOR", "MINOR")
CATEGORIES = (
    "contradiction",
    "unpassable-check",
    "data-loss",
    "safety",
    "missing-requirement",
    "other",
)
PRIOR_STATUSES = ("resolved", "open", "regressed")
ACTIONS = ("applied", "rejected")

_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$")
_FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})\s*([^`\s]*)\s*$")
_HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$")
_REF_TOKEN = re.compile(r"\b(?:[A-Z]{1,4}-[0-9]+(?:\.[0-9]+)*|P[0-9])\b")
_SECTION_REF = re.compile(r"^\d+(?:\.\d+)*$")
_HEAD_FINDINGS = re.compile(r"^#{1,6}\s+Findings block\s*$", re.M | re.I)
_HEAD_FIXMAP = re.compile(r"^#{1,6}\s+Fix map\s*$", re.M | re.I)


# ---------------------------------------------------------------- blocks


def _blocks_after(
    text: str, heading: re.Pattern[str], info: str
) -> tuple[bool, list[tuple[int, list[tuple[int, str]], bool]]]:
    """(heading found, [(fence start line, [(line number, line text), ...], closed), ...]) for fences with this info string.

    closed is False when the scan reached the end of the text without the closing fence: a truncated block.
    """
    m = heading.search(text)
    if not m:
        return False, []
    start_line = text.count("\n", 0, m.start())
    lines = text.splitlines()
    out: list[tuple[int, list[tuple[int, str]], bool]] = []
    i = start_line + 1
    while i < len(lines):
        fm = _FENCE.match(lines[i])
        if not fm:
            i += 1
            continue
        marker, label = fm.group(1), fm.group(2)
        body: list[tuple[int, str]] = []
        j = i + 1
        closed = False
        while j < len(lines):
            close = _FENCE.match(lines[j])
            if (
                close
                and close.group(1)[0] == marker[0]
                and len(close.group(1)) >= len(marker)
                and not close.group(2)
            ):
                closed = True
                break
            body.append((j + 1, lines[j]))
            j += 1
        if label == info:
            out.append((i + 1, body, closed))
        i = j + 1
    return True, out


def _check_flat(value: Any, name: str, lo: int | None, hi: int) -> str | None:
    if not isinstance(value, str):
        return f"{name} must be a string"
    n = len(flat(value))
    if lo is not None and n < lo:
        return f"{name} must have at least {lo} characters after whitespace flattening"
    if n > hi:
        return f"{name} must have at most {hi} characters"
    return None


def _check_finding(obj: dict, seen: set[str]) -> str | None:
    fid = obj.get("id")
    if not isinstance(fid, str) or not _ID.match(fid):
        return "id must match ^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$"
    if fid in seen:
        return f"duplicate id '{fid}'"
    if obj.get("severity") not in SEVERITIES:
        return "severity must be CRITICAL, MAJOR or MINOR"
    if not isinstance(obj.get("blocking"), bool):
        return "blocking must be a boolean"
    if obj["blocking"] and obj["severity"] == "MINOR":
        return "a MINOR finding cannot be blocking"
    if obj.get("category") not in CATEGORIES:
        return "category is not one of the allowed values"
    err = _check_flat(obj.get("anchor"), "anchor", 12, 200)
    if err:
        return err
    if "anchor2" in obj and obj["anchor2"] is not None:
        err = _check_flat(obj["anchor2"], "anchor2", 12, 200)
        if err:
            return err
    refs = obj.get("refs", [])
    if (
        not isinstance(refs, list)
        or len(refs) > 8
        or not all(isinstance(r, str) for r in refs)
    ):
        return "refs must be a list of at most 8 strings"
    err = _check_flat(obj.get("claim"), "claim", None, 300)
    if err:
        return err
    return None


def parse_block(report_text: str) -> dict:
    """Parse the findings-v1 block of a review report (contract C4.1)."""
    found, blocks = _blocks_after(report_text, _HEAD_FINDINGS, "findings-v1")
    res: dict[str, Any] = {"ok": True, "findings": [], "priors": [], "errors": []}
    if not found:
        res["ok"] = False
        res["errors"].append(
            {"line": 0, "msg": "heading '## Findings block' is missing"}
        )
        return res
    if not blocks:
        res["ok"] = False
        res["errors"].append(
            {
                "line": 0,
                "msg": "no fenced block with info string findings-v1 after the heading",
            }
        )
        return res
    if len(blocks) > 1:
        res["ok"] = False
        res["errors"].append(
            {
                "line": blocks[-1][0],
                "msg": "more than one findings-v1 block; the last one is used",
            }
        )
    if not blocks[-1][2]:
        res["ok"] = False
        res["errors"].append(
            {
                "line": blocks[-1][0],
                "msg": "the findings-v1 block is not closed: the report ends inside it (truncated)",
            }
        )
    seen: set[str] = set()
    for lineno, raw in blocks[-1][1]:
        if not raw.strip():
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as exc:
            res["ok"] = False
            res["errors"].append({"line": lineno, "msg": f"not valid JSON: {exc.msg}"})
            continue
        if not isinstance(obj, dict):
            res["ok"] = False
            res["errors"].append(
                {"line": lineno, "msg": "a line must be a JSON object"}
            )
            continue
        if "prior" in obj:
            pid, status = obj.get("prior"), obj.get("status")
            if not isinstance(pid, str) or not pid or status not in PRIOR_STATUSES:
                res["ok"] = False
                res["errors"].append(
                    {
                        "line": lineno,
                        "msg": "prior line needs a prior id and status resolved, open or regressed",
                    }
                )
                continue
            res["priors"].append({"prior": pid, "status": status})
            continue
        err = _check_finding(obj, seen)
        if err:
            res["ok"] = False
            res["errors"].append({"line": lineno, "msg": err})
            continue
        seen.add(obj["id"])
        obj.setdefault("refs", [])
        res["findings"].append(obj)
    return res


_TABLE_APPLIED = re.compile(
    r"^\s*\|\s*\**\s*([A-Za-z0-9][A-Za-z0-9._-]*)\s*\**\s*\|\s*\**\s*applied\b",
    re.I | re.M,
)


def parse_fixmap(text: str) -> dict:
    """Parse the fixmap-v1 block of a reviser output (C4.2), with a table fallback."""
    found, blocks = _blocks_after(text, _HEAD_FIXMAP, "fixmap-v1")
    res: dict[str, Any] = {"ok": True, "items": [], "errors": []}
    if not found or not blocks:
        res["ok"] = False
        res["errors"].append(
            {
                "line": 0,
                "msg": "fix map block is missing"
                if found
                else "heading '## Fix map' is missing",
            }
        )
        res["items"] = [
            {"id": m.group(1), "action": "applied", "reason": ""}
            for m in _TABLE_APPLIED.finditer(text)
        ]
        return res
    if len(blocks) > 1:
        res["ok"] = False
        res["errors"].append(
            {
                "line": blocks[-1][0],
                "msg": "more than one fixmap-v1 block; the last one is used",
            }
        )
    if not blocks[-1][2]:
        res["ok"] = False
        res["errors"].append(
            {
                "line": blocks[-1][0],
                "msg": "the fixmap-v1 block is not closed: the output ends inside it (truncated)",
            }
        )
    for lineno, raw in blocks[-1][1]:
        if not raw.strip():
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as exc:
            res["ok"] = False
            res["errors"].append({"line": lineno, "msg": f"not valid JSON: {exc.msg}"})
            continue
        if (
            not isinstance(obj, dict)
            or not isinstance(obj.get("id"), str)
            or obj.get("action") not in ACTIONS
            or not isinstance(obj.get("reason", ""), str)
        ):
            res["ok"] = False
            res["errors"].append(
                {
                    "line": lineno,
                    "msg": "fix map line needs id, action applied or rejected, and a reason",
                }
            )
            continue
        res["items"].append(
            {"id": obj["id"], "action": obj["action"], "reason": obj.get("reason", "")}
        )
    return res


# ---------------------------------------------------------------- anchors


def flat(s: str) -> str:
    return " ".join(s.split())


def locate(text: str, quote: str) -> list[tuple[int, int]]:
    """Every occurrence of the whitespace-flattened quote as a half-open 0-based line range."""
    q = flat(quote)
    if not q:
        return []
    chars: list[str] = []
    line_of: list[int] = []
    line = 0
    prev_space = True
    for ch in text:
        if ch.isspace():
            if not prev_space:
                chars.append(" ")
                line_of.append(line)
                prev_space = True
        else:
            chars.append(ch)
            line_of.append(line)
            prev_space = False
        if ch == "\n":
            line += 1
    norm = "".join(chars)
    out: list[tuple[int, int]] = []
    pos = norm.find(q)
    while pos != -1:
        end = pos + len(q) - 1
        out.append((line_of[pos], line_of[end] + 1))
        pos = norm.find(q, pos + 1)
    return out


def section_of(text: str, line: int) -> str:
    """The section number (or slug) of the nearest heading at or above the 0-based line."""
    lines = text.splitlines()
    for i in range(min(line, len(lines) - 1), -1, -1):
        m = _HEADING.match(lines[i])
        if m:
            title = m.group(1)
            num = re.match(r"^(\d+(?:\.\d+)*)", title)
            if num:
                return num.group(1)
            return re.sub(r"[^a-z0-9]+", "-", title.lower())
    return "top"


def refs_norm(finding: dict) -> list[str]:
    """Uppercase, unique, sorted requirement ids and section numbers named by a finding."""
    pieces = [
        finding.get("anchor") or "",
        finding.get("anchor2") or "",
        finding.get("claim") or "",
    ]
    refs = [r for r in (finding.get("refs") or []) if isinstance(r, str)]
    pieces.extend(refs)
    found: set[str] = set()
    for piece in pieces:
        for m in _REF_TOKEN.finditer(piece):
            found.add(m.group(0).upper())
    for r in refs:
        if _SECTION_REF.match(r.strip()):
            found.add(r.strip())
    return sorted(t for t in found if not t.startswith("SHA-"))


def fingerprint(section: str, refs: Iterable[str]) -> str:
    return hashlib.sha256(
        ("v1|" + section + "|" + ",".join(refs)).encode("utf-8")
    ).hexdigest()[:16]


def annotate(finding: dict, text: str) -> dict:
    """Return a copy of a finding with span, span2, section, refs_norm, fp and anchor flags for a document version."""
    out = dict(finding)
    spans = locate(text, finding["anchor"])
    out["anchor_status"] = "found" if spans else "missing"
    out["anchor_ambiguous"] = len(spans) > 1
    out["span"] = spans[0] if spans else None
    out["span2"] = None
    if finding.get("anchor2"):
        spans2 = locate(text, finding["anchor2"])
        out["span2"] = spans2[0] if spans2 else None
    out["refs_norm"] = refs_norm(finding)
    out["section"] = section_of(text, out["span"][0]) if out["span"] else "none"
    out["fp"] = fingerprint(out["section"], out["refs_norm"])
    return out


def _spans(x: dict) -> list[tuple[int, int]]:
    return [tuple(s) for s in (x.get("span"), x.get("span2")) if s]  # type: ignore[misc]


def same_defect(a: dict, b: dict) -> bool:
    """Two findings (or a finding and a ledger row view) describe the same defect on one document version."""
    if a.get("fp") and a.get("fp") == b.get("fp"):
        return True
    ra, rb = set(a.get("refs_norm") or []), set(b.get("refs_norm") or [])
    if ra & rb or (not ra and not rb):
        for s1 in _spans(a):
            for s2 in _spans(b):
                if s1[0] <= s2[1] + 3 and s2[0] <= s1[1] + 3:
                    return True
    return False


def cluster(findings: Sequence[dict]) -> list[list[dict]]:
    """Union-find over annotated findings in input order; cluster order is the order of the first member."""
    n = len(findings)
    parent = list(range(n))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i in range(n):
        for j in range(i + 1, n):
            if same_defect(findings[i], findings[j]):
                ri, rj = find(i), find(j)
                if ri != rj:
                    parent[max(ri, rj)] = min(ri, rj)
    groups: dict[int, list[dict]] = {}
    order: list[int] = []
    for i in range(n):
        r = find(i)
        if r not in groups:
            groups[r] = []
            order.append(r)
        groups[r].append(findings[i])
    return [groups[r] for r in order]


# ---------------------------------------------------------------- span mapping


def opcodes(old_text: str, new_text: str) -> list[tuple[str, int, int, int, int]]:
    return difflib.SequenceMatcher(
        None, old_text.splitlines(), new_text.splitlines(), autojunk=False
    ).get_opcodes()


def _map_line(line: int, ops: Sequence[tuple[str, int, int, int, int]]) -> int:
    for tag, i1, i2, j1, j2 in ops:
        if i1 <= line < i2:
            return j1 + (line - i1) if tag == "equal" else j1
    # past the end of the old text (or an empty old text): follow the last opcode
    if ops:
        _tag, _i1, i2, _j1, j2 = ops[-1]
        return j2 + (line - i2)
    return line


def map_span(
    span: Sequence[int] | None, ops: Sequence[tuple[str, int, int, int, int]]
) -> tuple[int, int] | None:
    """Map a half-open old line range into the new version (a replaced or deleted line maps to the start of its new range)."""
    if span is None:
        return None
    s, e = span
    ns = _map_line(s, ops)
    ne = _map_line(max(e - 1, s), ops) + 1
    return (ns, max(ne, ns + 1))


def hunks_touch(
    span: Sequence[int] | None, ops: Sequence[tuple[str, int, int, int, int]]
) -> bool:
    """True when a non-equal hunk overlaps the old span (a zero-width hunk at p touches spans with start <= p <= end)."""
    if span is None:
        return False
    s, e = span
    for tag, i1, i2, _j1, _j2 in ops:
        if tag == "equal":
            continue
        if i1 == i2:
            if s <= i1 <= e:
                return True
        elif i1 < e and s < i2:
            return True
    return False
