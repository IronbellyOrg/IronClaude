#!/usr/bin/env python3
"""diffgate: computed re-review surface and loop ledger for spec review loops.

Standard library only. Every subcommand prints one JSON object on stdout with
`ok`, `exit`, `message`, `review` plus its own fields. The script writes only
inside `--dir` and never writes the reviewed document.
"""

from __future__ import annotations

import argparse
import contextlib
import difflib
import hashlib
import json
import os
import re
import sys
import tempfile
from collections import namedtuple
from pathlib import Path

CAP_REVIEWS = 3  # the cap is a constant, never a flag
MERGE_GAP = 2
VIA_CAP = 2
FORMAT = "diffgate/1"

EXIT_OK, EXIT_REJECT, EXIT_USAGE, EXIT_INPUT, EXIT_CLOSED, EXIT_ORDER, EXIT_LEDGER = (
    0,
    1,
    2,
    3,
    4,
    5,
    6,
)

MAX_DOC_BYTES = 2 * 1024 * 1024
MAX_LINES = 100_000
MAX_MACHINE_LINES = 1_000
ANCHOR_MIN, ANCHOR_MAX = 12, 200

LEDGER = "ledger.json"
LOCK = ".lock"


def _spec_panel_blocking(sev: str, fr: int | None, outcome: str | None) -> bool:
    """CRITICAL, FR-8 or FR-9, or a MAJOR naming a concrete wrong outcome."""
    if sev == "critical" or fr in (8, 9):
        return True
    return sev == "major" and outcome not in (None, "", "-")


PROFILES = {
    "spec-panel": {
        "sev": ("critical", "major", "minor"),
        "blocking": _spec_panel_blocking,
    }
}

Token = namedtuple("Token", "text line start end")

NOTICES: list[str] = []
_HELD: dict[str, int] = {}


class Stop(Exception):
    """A non-zero exit with its message and extra JSON fields."""

    def __init__(self, code: int, message: str, **fields):
        super().__init__(message)
        self.code = code
        self.message = message
        self.fields = fields


# --------------------------------------------------------------------------
# Input


def read_text(path, what: str = "input") -> str:
    """Strict UTF-8 read; exit 3 names a missing, unreadable or empty file;
    exit 2 for a file over the limits."""
    p = Path(path)
    if not p.is_file():
        raise Stop(EXIT_INPUT, f"{what} missing or not a file: {path}", path=str(path))
    try:
        data = p.read_bytes()
    except OSError as exc:
        raise Stop(
            EXIT_INPUT, f"{what} unreadable: {path}: {exc}", path=str(path)
        ) from exc
    if len(data) > MAX_DOC_BYTES:
        raise Stop(EXIT_USAGE, f"{what} over the 2 MiB limit: {path}", path=str(path))
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Stop(
            EXIT_INPUT, f"{what} is not valid UTF-8: {path}: {exc}", path=str(path)
        ) from exc
    if not text.strip():
        raise Stop(EXIT_INPUT, f"{what} is empty: {path}", path=str(path))
    if len(text.splitlines()) > MAX_LINES:
        raise Stop(
            EXIT_USAGE,
            f"{what} over the {MAX_LINES} line limit: {path}",
            path=str(path),
        )
    return text


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------
# Diff engine


def tokens(lines, first: int = 1) -> list[Token]:
    """One Token(text, line, start, end) per whitespace-separated token."""
    out = []
    for offset, line in enumerate(lines):
        for m in re.finditer(r"\S+", line):
            out.append(Token(m.group(), first + offset, m.start(), m.end()))
    return out


_LIST = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s")
_HEAD = re.compile(r"^\s*#{1,6}\s")
_TABLE = re.compile(r"^\s*\|")


def _shape(lines) -> tuple[int, int, int]:
    """Counts of list, heading and table lines (a reflow that changes them is structural)."""
    return (
        sum(1 for x in lines if _LIST.match(x)),
        sum(1 for x in lines if _HEAD.match(x)),
        sum(1 for x in lines if _TABLE.match(x)),
    )


def _section(lines, lineno: int) -> str:
    for i in range(min(lineno, len(lines)) - 1, -1, -1):
        if _HEAD.match(lines[i]):
            return lines[i].strip().lstrip("#").strip()
    return "(top)"


def _span(t: Token) -> list:
    return [t.line, t.start, t.end, t.text]


def build_hunks(old: str, new: str, review: int):
    """Line pass, then a token pass inside changed blocks.

    Returns (hunks, ignored). Only changed tokens (new side) and removed tokens
    (old side) are eligible anchors. Changed blocks whose new-side lines lie
    within MERGE_GAP lines of each other share one hunk id H<review>.<n>; the
    gap lines never become eligible. Whitespace-only change and pure reflow go
    to `ignored`, unless the reflow changes the count of list, heading or table
    lines, which makes a hunk with `structural: yes`.
    """
    old_lines, new_lines = old.splitlines(), new.splitlines()
    sm = difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False)
    blocks, ignored = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        ot = tokens(old_lines[i1:i2], i1 + 1)
        nt = tokens(new_lines[j1:j2], j1 + 1)
        tsm = difflib.SequenceMatcher(
            None, [t.text for t in ot], [t.text for t in nt], autojunk=False
        )
        changed, removed = [], []
        for ttag, a1, a2, b1, b2 in tsm.get_opcodes():
            if ttag != "equal":
                removed += ot[a1:a2]
                changed += nt[b1:b2]
        structural = False
        if not changed and not removed:
            if _shape(old_lines[i1:i2]) == _shape(new_lines[j1:j2]):
                ignored.append(
                    {
                        "old": [i1 + 1, i2],
                        "new": [j1 + 1, j2],
                        "reason": "whitespace-or-reflow",
                    }
                )
                continue
            structural = True
        first = j1 + 1
        last = j2 if j2 > j1 else j1 + 1
        blocks.append(
            {
                "first": first,
                "last": last,
                "old": [i1 + 1, i2],
                "new": [j1 + 1, j2],
                "changed": [_span(t) for t in changed],
                "removed": [_span(t) for t in removed],
                "structural": structural,
            }
        )
    merged: list[dict] = []
    for b in blocks:
        if merged and b["first"] - merged[-1]["last"] <= MERGE_GAP:
            m = merged[-1]
            m["last"] = max(m["last"], b["last"])
            m["old"] = [min(m["old"][0], b["old"][0]), max(m["old"][1], b["old"][1])]
            m["new"] = [min(m["new"][0], b["new"][0]), max(m["new"][1], b["new"][1])]
            m["changed"] += b["changed"]
            m["removed"] += b["removed"]
            m["structural"] = m["structural"] or b["structural"]
        else:
            merged.append(dict(b))
    hunks = []
    for n, m in enumerate(merged, 1):
        hunks.append(
            {
                "id": f"H{review}.{n}",
                "new": m["new"],
                "old": m["old"],
                "first": m["first"],
                "last": m["last"],
                "changed": m["changed"],
                "removed": m["removed"],
                "structural": m["structural"],
                "section": _section(new_lines, m["first"]),
            }
        )
    return hunks, ignored


def coverage(hunks, new: str) -> float:
    total = max(1, len(new.splitlines()))
    lines = set()
    for h in hunks:
        lines.update(s[0] for s in h["changed"])
        if h["structural"]:
            lines.update(range(h["new"][0], h["new"][1] + 1))
    return round(len(lines) / total, 4)


def render_surface(
    review: int, hunks, priors, new: str = "", old: str = "", owners=None
) -> str:
    """Markdown surface for review N: hunk ids, sections, owner ids, the prior
    blocking table and the coverage line (warning above 50%)."""
    owners = owners or {}
    new_lines, old_lines = new.splitlines(), old.splitlines()
    cov = coverage(hunks, new) if new else 0.0
    out = [
        f"# Diffgate surface: review {review} of {CAP_REVIEWS}",
        "",
        f"format: {FORMAT}",
        f"coverage: {cov:.0%} of lines changed"
        + (
            " (warning: above 50%, the surface is close to the whole document)"
            if cov > 0.5
            else ""
        ),
        "",
        "Review only the changed tokens below. Anchor each new finding with `hunk=<id>` on a changed",
        "token, or `via=<id>` for an unchanged line a hunk breaks, or `cites=<prior id>`.",
        "",
        "## Prior blocking findings",
        "",
    ]
    if priors:
        out += ["| id | label | at | finding |", "|---|---|---|---|"]
        for p in priors:
            text = str(p.get("text", "")).replace("|", "\\|")
            out.append(
                f"| {p['id']} | {p.get('sev', '')} | {p.get('at', '')} | {text} |"
            )
    else:
        out.append("(none)")
    out += ["", "## Hunks", ""]
    if not hunks:
        out.append("(empty surface: every prior blocking finding stays open)")
    for h in hunks:
        owner = ",".join(owners.get(h["id"], [])) or "-"
        flag = " structural: yes" if h["structural"] else ""
        out.append(f"### {h['id']} (section: {h['section']}; owners: {owner}){flag}")
        out.append("")
        a, b = h["new"]
        if b >= a:
            out.append(f"New lines {a}-{b}:")
            out.append("```text")
            out += [
                f"{i:>5}: {new_lines[i - 1]}"
                for i in range(a, b + 1)
                if i <= len(new_lines)
            ]
            out.append("```")
        if h["changed"]:
            words = " ".join(f"`{s[3]}`@{s[0]}" for s in h["changed"])
            out.append(f"Changed tokens: {words}")
        if h["removed"]:
            oa, ob = h["old"]
            out.append(f"Removed from old lines {oa}-{ob} (anchor with `side=old`):")
            out.append("```text")
            out += [
                f"{i:>5}: {old_lines[i - 1]}"
                for i in range(oa, ob + 1)
                if i <= len(old_lines)
            ]
            out.append("```")
            out.append(
                "Removed tokens: " + " ".join(f"`{s[3]}`@{s[0]}" for s in h["removed"])
            )
        out.append("")
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------
# Report grammar, checker rules C1-C12 and derivation

BLOCK_HEADING = "## Diffgate findings"
_REVIEW_LINE = re.compile(r"^[#>*\s]*review:\s*(\d+)\s+of\s+3\b", re.M)
_KEY = re.compile(r"([a-z_]+)=")
_BARE = re.compile(r"\S*")
_AT = re.compile(r"^(\d+)(?:-(\d+))?$")
_HUNK_ID = re.compile(r"^H\d+\.\d+$")
_FID = re.compile(r"^R\d+\.\d+$")
PRIOR_STATUSES = ("resolved", "open", "regressed", "withdrawn")
FINDING_KEYS = {
    "sev",
    "at",
    "hunk",
    "anchor",
    "outcome",
    "via",
    "via_quote",
    "cites",
    "fr",
    "side",
}
PRIOR_KEYS = {
    "resolved": ({"by"}, set()),
    "open": ({"quote"}, set()),
    "regressed": ({"by", "quote"}, set()),
    "withdrawn": ({"quote", "reason"}, set()),
}
LABELS_COUNTED = ("critical", "major")


def _collapse(text: str) -> str:
    return " ".join(str(text).split())


def _kv(rest: str):
    """`key=value` pairs; a value is a JSON string (json.loads) or a bare token."""
    out, i, n = {}, 0, len(rest)
    dec = json.JSONDecoder()
    while i < n:
        while i < n and rest[i].isspace():
            i += 1
        if i >= n:
            break
        m = _KEY.match(rest, i)
        if not m:
            return out, f"cannot parse near {rest[i : i + 30]!r}"
        key, i = m.group(1), m.end()
        if key in out:
            return out, f"duplicate key {key}="
        if i < n and rest[i] == '"':
            try:
                val, i = dec.raw_decode(rest, i)
            except ValueError as exc:
                return out, f"bad JSON string for {key}=: {exc}"
        else:
            m2 = _BARE.match(rest, i)
            val, i = m2.group(), m2.end()
        out[key] = val
    return out, None


def parse_report(text: str) -> dict:
    """Parse the `## Diffgate findings` block: PRIOR / FINDING / FINDINGS none."""
    lines = text.splitlines()
    parsed = {
        "review": None,
        "block": False,
        "prior": [],
        "finding": [],
        "none": False,
        "bad": [],
        "prose_ids": [],
    }
    m = _REVIEW_LINE.search(text)
    parsed["review"] = int(m.group(1)) if m else None
    start = next((i for i, x in enumerate(lines) if x.strip() == BLOCK_HEADING), None)
    if start is None:
        prose, block = lines, []
    else:
        end = next(
            (
                i
                for i in range(start + 1, len(lines))
                if lines[i].startswith("# ") or lines[i].startswith("## ")
            ),
            len(lines),
        )
        block = list(enumerate(lines[start + 1 : end], start + 2))
        prose = lines[:start] + lines[end:]
        parsed["block"] = True
    parsed["prose_ids"] = sorted(set(re.findall(r"\bR\d+\.\d+\b", "\n".join(prose))))
    for lineno, raw in block:
        s = raw.strip()
        if not s or s.startswith("```"):
            continue
        if raw.rstrip() == "FINDINGS none":
            parsed["none"] = True
        elif raw.startswith("PRIOR "):
            parts = raw[6:].split(None, 2)
            pid = parts[0] if parts else ""
            status = parts[1] if len(parts) > 1 else ""
            kv, err = _kv(parts[2] if len(parts) > 2 else "")
            rec = {"line": lineno, "id": pid, "status": status, "kv": kv, "errors": []}
            if err:
                rec["errors"].append(("C2", err))
            parsed["prior"].append(rec)
        elif raw.startswith("FINDING "):
            head, sep, ftext = raw[8:].partition(" :: ")
            fid, _, rest = head.strip().partition(" ")
            kv, err = _kv(rest)
            rec = {
                "line": lineno,
                "id": fid,
                "kv": kv,
                "text": ftext.strip(),
                "errors": [],
            }
            if err:
                rec["errors"].append(("C2", err))
            if not sep or not ftext.strip():
                rec["errors"].append(("C2", "missing ` :: text` after the fields"))
            parsed["finding"].append(rec)
        else:
            parsed["bad"].append(
                {"line": lineno, "message": f"unparseable block line: {raw[:60]!r}"}
            )
    return parsed


def make_ctx(
    review: int,
    doc: str,
    old: str | None = None,
    hunks=(),
    priors=(),
    declined=(),
    owners=None,
    chains=None,
    held=None,
    scoped=None,
    spec_sha=None,
) -> dict:
    """Everything check_report and derive read besides the report itself.
    `spec_sha` is the current specification's hash (C3); None skips C3, as a
    replay of an earlier review does."""
    return {
        "review": review,
        "doc": doc,
        "old": old,
        "hunks": {h["id"]: h for h in hunks},
        "priors": list(priors),
        "declined": set(declined),
        "owners": dict(owners or {}),
        "chains": dict(chains or {}),
        "held": dict(held or {}),
        "scoped": dict(scoped or {}),
        "spec_sha": spec_sha,
    }


def _occurrences(text: str, a: int, b: int, quote: str) -> list[set]:
    """For each occurrence of the whitespace-collapsed quote inside lines a..b,
    the set of (line, start) keys of the tokens it overlaps."""
    toks = tokens(text.splitlines()[a - 1 : b], a)
    joined, spans = "", []
    for t in toks:
        if joined:
            joined += " "
        s0 = len(joined)
        joined += t.text
        spans.append((s0, len(joined), t))
    q = _collapse(quote)
    occ = []
    i = joined.find(q) if q else -1
    while i >= 0:
        e = i + len(q)
        occ.append({(t.line, t.start) for s0, e0, t in spans if s0 < e and e0 > i})
        i = joined.find(q, i + 1)
    return occ


def _keys(spans) -> set:
    return {(s[0], s[1]) for s in spans}


def _check_finding(f: dict, ctx: dict, profile: dict) -> None:
    """Rules C2 and C4 to C8 for one FINDING line; appends to f['errors']."""
    n, kv, errs = ctx["review"], f["kv"], f["errors"]
    for key in sorted(set(kv) - FINDING_KEYS):
        errs.append(("C2", f"unknown key {key}="))
    for key in ("sev", "at", "anchor"):
        if not kv.get(key):
            errs.append(("C2", f"missing {key}="))
    f["sev"] = kv.get("sev", "")
    if f["sev"] and f["sev"] not in profile["sev"]:
        errs.append(("C2", f"sev= must be one of {', '.join(profile['sev'])}"))
    f["fr"] = None
    if "fr" in kv:
        if kv["fr"] not in ("8", "9", "10"):
            errs.append(("C2", "fr= must be 8, 9 or 10"))
        else:
            f["fr"] = int(kv["fr"])
    for key in ("hunk", "via", "via_quote", "cites", "side", "outcome", "anchor"):
        f[key] = kv.get(key)
    if f["side"] not in (None, "old"):
        errs.append(("C2", "side= must be old"))
    if n == 1:
        bad = [k for k in ("hunk", "via", "via_quote", "cites", "side") if k in kv]
        if bad:
            errs.append(
                (
                    "C2",
                    f"review 1 has no surface and no priors: {', '.join(bad)} not allowed",
                )
            )
            return
    else:
        if f["hunk"] and (f["via"] or f["cites"]):
            errs.append(("C2", "a finding anchored by via= or cites= omits hunk="))
        if bool(f["via"]) != bool(f["via_quote"]):
            errs.append(("C2", "via= and via_quote= go together"))
        if f["side"] == "old" and not f["hunk"]:
            errs.append(("C2", "side=old needs hunk="))
    m = _AT.match(str(kv.get("at", "")))
    if not m:
        if kv.get("at"):
            errs.append(("C2", "at= must be a line or a-b"))
        return
    a, b = int(m.group(1)), int(m.group(2) or m.group(1))
    f["at"] = [a, b]
    side_text = ctx["old"] if f["side"] == "old" else ctx["doc"]
    if side_text is None:
        errs.append(("C4", "side=old needs a previous snapshot"))
        return
    total = len(side_text.splitlines())
    if not (1 <= a <= b <= total):
        errs.append(("C4", f"at={a}-{b} outside the snapshot (1-{total})"))
        return
    anchor = _collapse(f["anchor"] or "")
    if f["anchor"] and not (ANCHOR_MIN <= len(anchor) <= ANCHOR_MAX):
        errs.append(("C5", f"anchor must be {ANCHOR_MIN} to {ANCHOR_MAX} characters"))
        return
    occ = _occurrences(side_text, a, b, anchor) if anchor else []
    if anchor and not occ:
        errs.append(("C5", f"anchor not found on lines {a}-{b} of the named side"))
        return
    changed = set().union(*(_keys(h["changed"]) for h in ctx["hunks"].values()))
    f["on_changed"] = f["side"] != "old" and any(o & changed for o in occ)
    if f["hunk"]:
        h = ctx["hunks"].get(f["hunk"])
        if h is None:
            errs.append(("C6", f"no hunk {f['hunk']} in this surface"))
            return
        keys = _keys(h["removed"] if f["side"] == "old" else h["changed"])
        if not any(o & keys for o in occ):
            errs.append(
                ("C6", f"anchor does not overlap a changed token of {f['hunk']}")
            )
    if f["via"]:
        h = ctx["hunks"].get(f["via"])
        if h is None:
            errs.append(("C7", f"no hunk {f['via']} in this surface"))
            return
        lo, hi = h["new"][0], max(h["new"][0], h["new"][1])
        vq = _collapse(f["via_quote"] or "")
        vocc = _occurrences(ctx["doc"], lo, hi, vq) if vq else []
        if not any(o & _keys(h["changed"]) for o in vocc):
            errs.append(
                ("C7", f"via_quote does not overlap a changed token of {f['via']}")
            )
        if f["on_changed"]:
            errs.append(
                ("C6", "a via= anchor must sit on unchanged text; use hunk= instead")
            )
    if f["cites"] and f["cites"] not in {p["id"] for p in ctx["priors"]}:
        errs.append(("C8", f"cites={f['cites']} is not a prior blocking id"))


def check_report(parsed: dict, ctx: dict, profile=None) -> list[dict]:
    """Hard rules C1 to C10. C3 (the specification changed since `begin`)
    raises exit 5 with no error list, because a report repair cannot fix it.
    Returns error dicts; `structural` marks the failures a repair of single
    lines cannot fix."""
    profile = profile or PROFILES["spec-panel"]
    n = ctx["review"]
    if ctx.get("spec_sha") is not None and ctx["spec_sha"] != sha256(ctx["doc"]):
        raise Stop(
            EXIT_ORDER,
            f"C3: the specification changed during review {n}; "
            "a report repair cannot fix that",
            review=n,
        )
    errors = []

    def err(rule, message, line=None, fid=None, structural=False):
        errors.append(
            {
                "rule": rule,
                "line": line,
                "id": fid,
                "message": message,
                "structural": structural,
            }
        )

    has_lines = parsed["finding"] or parsed["none"] or parsed["prior"]
    if not parsed["block"] or not has_lines:
        err("C1", f"no parseable `{BLOCK_HEADING}` block", structural=True)
    if parsed["review"] != n:
        err(
            "C1",
            f"report header `review: {parsed['review']} of 3` differs from the ledger review {n}",
            structural=True,
        )
    if parsed["block"] and has_lines and not (parsed["finding"] or parsed["none"]):
        err("C1", "the block needs FINDING lines or the line `FINDINGS none`")
    if parsed["none"] and parsed["finding"]:
        err("C1", "`FINDINGS none` cannot stand beside FINDING lines")
    for b in parsed["bad"]:
        err("C2", b["message"], b["line"])
    ids = [f["id"] for f in parsed["finding"]]
    for pos, f in enumerate(parsed["finding"], 1):
        if f["id"] != f"R{n}.{pos}":
            f["errors"].append(
                ("C2", f"ids must run R{n}.1, R{n}.2, ... with no gap; got {f['id']}")
            )
        _check_finding(f, ctx, profile)
    for pid in parsed["prose_ids"]:
        if pid.startswith(f"R{n}.") and pid not in ids:
            err(
                "C2b",
                f"{pid} appears in the prose but not in the block",
                structural=True,
            )
    expected = {p["id"] for p in ctx["priors"]}
    seen = set()
    for p in parsed["prior"]:
        if n == 1:
            p["errors"].append(("C9", "review 1 has no prior findings"))
            continue
        if p["id"] not in expected:
            p["errors"].append(("C9", f"{p['id']} is not a prior blocking id"))
        elif p["id"] in seen:
            p["errors"].append(("C9", f"{p['id']} has more than one PRIOR line"))
        seen.add(p["id"])
        if p["status"] not in PRIOR_STATUSES:
            p["errors"].append(
                ("C2", f"status must be one of {', '.join(PRIOR_STATUSES)}")
            )
            continue
        need, _ = PRIOR_KEYS[p["status"]]
        for key in sorted(need - set(p["kv"])):
            rule = "C10" if key == "by" else "C2"
            p["errors"].append((rule, f"`{p['status']}` needs {key}="))
        for key in sorted(set(p["kv"]) - need):
            p["errors"].append(("C2", f"unknown key {key}= for `{p['status']}`"))
        by = p["kv"].get("by")
        if by and by not in ctx["hunks"]:
            p["errors"].append(("C10", f"by={by} is not a hunk of this surface"))
        if p["status"] == "withdrawn" and p["id"] not in ctx["declined"]:
            p["errors"].append(
                ("C9", f"{p['id']} can be withdrawn only after a `declined` map line")
            )
    for missing in sorted(expected - seen):
        err("C9", f"missing PRIOR line for {missing}", fid=missing)
    for rec in parsed["finding"] + parsed["prior"]:
        for rule, message in rec["errors"]:
            err(rule, message, rec["line"], rec["id"])
    return errors


def derive(
    parsed: dict, profile: dict, priors, ctx: dict, degrade: bool = False
) -> dict:
    """Blocking, origin, prior statuses, deferral, verdict, acceptance, fix
    chains and the counts `blocking` and `proxy_all` (owner rule: cumulative)."""
    n = ctx["review"]
    blocking_fn = profile["blocking"]
    findings, deferred, held = [], [], dict(ctx["held"])
    scoped = dict(ctx["scoped"])  # blocking-grade findings the script took out
    via_used = 0
    for f in parsed["finding"]:
        sev = f.get("sev") or f["kv"].get("sev", "")
        grade = blocking_fn(sev, f.get("fr"), f.get("outcome"))
        rec = {
            "id": f["id"],
            "sev": sev,
            "at": f.get("at"),
            "hunk": f.get("hunk"),
            "via": f.get("via"),
            "cites": f.get("cites"),
            "side": f.get("side"),
            "fr": f.get("fr"),
            "outcome": f.get("outcome"),
            "anchor": f.get("anchor"),
            "text": f["text"],
        }
        reason = None
        if f["errors"]:
            if n == 1:
                rec["unanchored"] = True
            else:
                reason = "unanchored"
        elif n >= 2 and f.get("via"):
            via_used += 1
            if via_used > VIA_CAP:
                reason = "via-cap"
        elif n >= 2 and not (f.get("hunk") or f.get("cites")):
            reason = "pre-existing"
        if n == 1:
            rec["origin"] = "full"
        elif (f.get("hunk") and not reason) or f.get("on_changed"):
            rec["origin"] = "changed"
        else:
            rec["origin"] = "unchanged"
        owners = ctx["owners"].get(rec["hunk"] or rec["via"] or "", [])
        rec["chain"] = (ctx["chains"].get(owners[0], [owners[0]]) if owners else []) + [
            rec["id"]
        ]
        if reason:
            rec.update(status="deferred", reason=reason, blocking=False)
            deferred.append({**rec, "review": n})
        elif rec["cites"]:
            rec.update(status="note", blocking=False)  # cites= adds no blocker
        else:
            rec.update(status="open" if grade else "minor", blocking=grade)
        rec["demoted"] = sev in LABELS_COUNTED and not rec["blocking"] and not reason
        why = reason or ("demoted" if rec["demoted"] else "cites")
        if sev in LABELS_COUNTED and (reason or rec["demoted"]):
            held.setdefault(rec["id"], {"review": n, "why": why, "sev": sev})
        if (grade and not rec["blocking"]) or rec["demoted"]:
            scoped.setdefault(rec["id"], {"review": n, "why": why, "sev": sev})
        findings.append(rec)
    given = {p["id"]: p for p in parsed["prior"] if not p["errors"]}
    prior_out, degraded = [], False
    for p in priors:
        line = given.get(p["id"])
        status = line["status"] if line else "open"
        if line is None:
            degraded = True
        if not ctx["hunks"] and status in ("resolved", "regressed"):
            status = "open"  # an empty surface leaves every prior blocker open
        prior_out.append(
            {**p, "status": status, "by": line["kv"].get("by") if line else None}
        )
        if status == "withdrawn":
            mark = {"review": n, "why": "withdrawn", "sev": p.get("sev")}
            scoped.setdefault(p["id"], mark)
            if p.get("sev") in LABELS_COUNTED:
                held.setdefault(p["id"], mark)
    degraded = degrade and (degraded or any(f["errors"] for f in parsed["finding"]))
    open_blocking = [
        {k: r[k] for k in ("id", "sev", "at", "hunk", "text", "chain", "anchor")}
        for r in findings
        if r["blocking"]
    ] + [
        {
            "id": p["id"],
            "sev": p.get("sev"),
            "at": p.get("at"),
            "hunk": p.get("hunk"),
            "text": p.get("text"),
            "chain": ctx["chains"].get(p["id"], [p["id"]]),
            "anchor": p.get("anchor"),
            "status": p["status"],
        }
        for p in prior_out
        if p["status"] in ("open", "regressed")
    ]
    counted = {r["id"] for r in findings if r["sev"] in LABELS_COUNTED}
    counted |= {
        p["id"]
        for p in prior_out
        if p["status"] in ("open", "regressed", "withdrawn")
        and p.get("sev") in LABELS_COUNTED
    }
    counted |= set(held)
    verdict = "FAIL" if open_blocking else "PASS"
    return {
        "review": n,
        "verdict": verdict,
        "verdict_line": f"verdict: {verdict}",
        "acceptance": "scoped" if scoped else "clean",
        "scoped": scoped,
        "blocking": len(open_blocking),
        "blocking_ids": [b["id"] for b in open_blocking],
        "open_blocking": open_blocking,
        "deferred": deferred,
        "degraded": degraded,
        "proxy_all": len(counted),
        "proxy_ids": sorted(counted),
        "held": held,
        "findings": findings,
        "priors": prior_out,
        "chains": {b["id"]: b["chain"] for b in open_blocking},
    }


def evaluate(report: str, ctx: dict, degrade: bool = False, profile=None):
    """Parse, check and (when acceptable) derive. Returns (errors, result);
    result is None when the report is rejected."""
    profile = profile or PROFILES["spec-panel"]
    parsed = parse_report(report)
    errors = check_report(parsed, ctx, profile)
    if any(e["structural"] for e in errors) or (errors and not degrade):
        return errors, None
    return errors, derive(parsed, profile, ctx["priors"], ctx, degrade)


# --------------------------------------------------------------------------
# Fix map rules M1 to M3

FIXMAP_HEADING = "## Diffgate fixmap"
_MAP_LINE = re.compile(r"^(H\d+\.\d+)\s+(R\d+\.\d+(?:\s*,\s*R\d+\.\d+)*)\s*$")
_DECLINE = re.compile(r"^declined\s+(R\d+\.\d+)\s+(\S.*)$")
_TAG = re.compile(r"R\d+\.\d+")


def map_block(text: str) -> str:
    """The lines under `## Diffgate fixmap` up to the next heading, so the map
    can live inside the reviser's disposition file; the whole text otherwise."""
    lines = text.splitlines()
    idx = next((i for i, x in enumerate(lines) if x.strip() == FIXMAP_HEADING), None)
    if idx is None:
        return text
    end = next(
        (
            i
            for i in range(idx + 1, len(lines))
            if lines[i].startswith("# ") or lines[i].startswith("## ")
        ),
        len(lines),
    )
    return "\n".join(lines[idx + 1 : end])


def candidates(hunks) -> dict:
    """Owner candidates per hunk from inline R<N>.<j> tags in its changed tokens."""
    out = {}
    for h in hunks:
        tags = []
        for span in h["changed"]:
            for tag in _TAG.findall(span[3]):
                if tag not in tags:
                    tags.append(tag)
        out[h["id"]] = tags
    return out


def candidate_map(hunks, doc_sha: str) -> str:
    cand = candidates(hunks)
    lines = [f"doc_sha: {doc_sha}"]
    lines += [f"{h['id']} {','.join(cand[h['id']])}".rstrip() for h in hunks]
    return "\n".join(lines) + "\n"


def check_fixmap(map_text: str, hunks, open_blocking, doc_sha: str) -> dict:
    """M1 every hunk is owned by one or more open blocking ids; M2 every open
    blocking id has a hunk or a `declined` line; M3 ids and hunks exist and the
    `doc_sha:` line matches the current document."""
    hunk_ids = [h["id"] for h in hunks]
    blocking = set(open_blocking)
    errors, owners, declined, stale = [], {}, {}, False
    body = [x.strip() for x in map_block(map_text).splitlines()]
    body = [x for x in body if x and not x.startswith("```")]
    if not body or not body[0].startswith("doc_sha:"):
        errors.append("M3: the first line must be `doc_sha: <sha>`")
    else:
        if body[0].split(":", 1)[1].strip() != doc_sha:
            stale = True
            errors.append("M3: stale doc_sha: the map was written for another version")
        body = body[1:]
    for line in body:
        m, d = _MAP_LINE.match(line), _DECLINE.match(line)
        if m:
            hid = m.group(1)
            ids = [x.strip() for x in m.group(2).split(",")]
            if hid not in hunk_ids:
                errors.append(f"M3: unknown hunk {hid}")
            elif hid in owners:
                errors.append(f"M3: {hid} has more than one map line")
            else:
                owners[hid] = ids
        elif d:
            if d.group(1) not in blocking:
                errors.append(f"M3: declined {d.group(1)} is not an open blocking id")
            declined[d.group(1)] = d.group(2)
        else:
            errors.append(f"M3: unparseable map line: {line[:60]!r}")
    unmapped = []
    for hid in hunk_ids:
        ids = owners.get(hid, [])
        bad = [x for x in ids if x not in blocking]
        if not ids or bad:
            unmapped.append(hid)
        if bad:
            errors.append(
                f"M1: {hid} names {', '.join(bad)}, not an open blocking id "
                "(minor findings, citation notes and unknown ids cannot own a hunk)"
            )
        elif not ids:
            errors.append(f"M1: {hid} has no owner")
    owned = {x for ids in owners.values() for x in ids}
    for bid in sorted(blocking - owned - set(declined)):
        errors.append(f"M2: {bid} has neither a hunk nor a `declined` line")
    by_id_bytes, by_id_hunks = {}, {}
    for h in hunks:
        size = sum(len(s[3].encode("utf-8")) for s in h["changed"])
        for x in owners.get(h["id"], []):
            by_id_bytes[x] = by_id_bytes.get(x, 0) + size
            by_id_hunks.setdefault(x, []).append(h["id"])
    return {
        "accepted": not errors and not unmapped,
        "stale": stale,
        "errors": errors,
        "unmapped": unmapped,
        "owners": owners,
        "declined": declined,
        "mapped": sorted(owners),
        "bytes_by_id": by_id_bytes,
        "hunks_by_id": by_id_hunks,
    }


# --------------------------------------------------------------------------
# Loop subcommands: begin, check, fixcheck, status, and the replay

DEFERRED_SENTENCE = (
    "PASS in this loop is scoped to the reviewed surfaces; "
    "deferred severity labels are the reviewer's, unvalidated."
)
REVISER_RULES = (
    "Revise only text a blocking finding names; add no rule, mechanism or section "
    "no blocking finding calls for; each added paragraph or table cites its finding "
    "id; write the fix map only inside your own disposition file, as a "
    "`## Diffgate fixmap` block with a `doc_sha:` first line and one line per changed "
    "hunk naming its blocking ids, or `declined <id> <reason>`; run the script's "
    "read-only `fixcheck --dry-run --map <disposition file>` until it exits 0; report "
    "the byte size before and after, which `fixcheck` prints. The next review refuses "
    "to open while any hunk maps to no listed finding."
)


def _closed_guard(led: dict) -> None:
    if led.get("closed"):
        halt = led.get("halt")
        raise Stop(
            EXIT_CLOSED,
            f"the loop is closed (halt: {halt}); do not review, escalate",
            halt=halt,
            review=led.get("review"),
        )


def _snapshot(d: Path, n: int, entry: dict) -> str:
    path = d / f"doc-r{n}.md"
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise Stop(EXIT_LEDGER, f"snapshot missing: {path}") from exc
    if sha256(text) != entry["doc_sha"]:
        raise Stop(EXIT_LEDGER, f"snapshot {path.name} differs from the ledger hash")
    return text


def _ctx(d: Path, led: dict, n: int, spec_sha=None) -> dict:
    entry = led["reviews"][str(n)]
    old = _snapshot(d, n - 1, led["reviews"][str(n - 1)]) if n > 1 else None
    return make_ctx(
        review=n,
        doc=_snapshot(d, n, entry),
        old=old,
        hunks=entry["hunks"],
        priors=entry["priors"],
        declined=entry["declined"],
        owners=entry["owners"],
        chains=entry["chains"],
        held=entry["held"],
        scoped=entry["scoped"],
        spec_sha=spec_sha,
    )


def _norm(obj):
    return json.loads(json.dumps(obj, sort_keys=True))


def replay(d: Path, led: dict) -> None:
    """Re-run every accepted check on its kept report copy and re-derive every
    review's inputs; any disagreement with the ledger exits 6."""
    prev = None
    for n in range(1, led["review"] + 1):
        entry = led["reviews"].get(str(n))
        if entry is None:
            raise Stop(EXIT_LEDGER, f"ledger has no review {n}")
        doc = _snapshot(d, n, entry)
        if prev is not None:
            old = _snapshot(d, n - 1, prev)
            want = {
                "hunks": build_hunks(old, doc, n)[0],
                "priors": _priors(prev),
                "held": prev["check"]["result"]["held"],
                "scoped": prev["check"]["result"]["scoped"],
                "owners": prev["fix"]["owners"],
                "declined": sorted(prev["fix"]["declined"]),
                "chains": prev["check"]["result"]["chains"],
            }
            for key, value in want.items():
                if _norm(value) != _norm(entry[key]):
                    raise Stop(EXIT_LEDGER, f"replay mismatch in review {n}: {key}")
        check = entry.get("check")
        if check:
            path = d / f"report-r{n}.md"
            try:
                report = path.read_text(encoding="utf-8")
            except OSError as exc:
                raise Stop(EXIT_LEDGER, f"kept report missing: {path}") from exc
            if sha256(report) != check["report_sha"]:
                raise Stop(EXIT_LEDGER, f"{path.name} differs from the ledger hash")
            _errors, result = evaluate(report, _ctx(d, led, n), check["degrade"])
            if result is None or _norm(result) != _norm(check["result"]):
                raise Stop(EXIT_LEDGER, f"replay of the review {n} check disagrees")
        fix = entry.get("fix") or {}
        if n < led["review"] and (
            not check
            or check["result"]["verdict"] != "FAIL"
            or not fix.get("accepted")
            or fix.get("fix_rejected")
        ):
            raise Stop(EXIT_LEDGER, f"replay: review {n} cannot be followed by another")
        prev = entry
    halt = _expected_halt(led)
    if bool(led.get("closed")) != (halt is not None) or led.get("halt") != halt:
        raise Stop(EXIT_LEDGER, "replay: the ledger's closed or halt flags disagree")


def _expected_halt(led: dict):
    """The terminal state the recorded steps imply (the cap is a constant)."""
    n = led["review"]
    cur = led["reviews"][str(n)]
    check = cur.get("check")
    if check and check["result"]["verdict"] == "PASS":
        return "pass"
    if check and n >= CAP_REVIEWS:
        return "escalate"
    if (cur.get("fix") or {}).get("fix_rejected"):
        return "escalate"
    if cur.get("structural_failures", 0) >= 2:
        return "invalid"
    return None


def _priors(entry: dict) -> list:
    """The open blocking findings of a checked review become the next priors."""
    keys = ("id", "sev", "at", "hunk", "text", "chain", "anchor")
    return [
        {k: b.get(k) for k in keys} for b in entry["check"]["result"]["open_blocking"]
    ]


def _new_entry(doc_sha: str, hunks=(), ignored=(), priors=(), prev=None, cov=None):
    fix = (prev or {}).get("fix") or {}
    result = ((prev or {}).get("check") or {}).get("result") or {}
    return {
        "doc_sha": doc_sha,
        "hunks": list(hunks),
        "ignored": len(ignored),
        "coverage": cov,
        "priors": list(priors),
        "declined": sorted(fix.get("declined", {})),
        "owners": fix.get("owners", {}),
        "chains": result.get("chains", {}),
        "held": result.get("held", {}),
        "scoped": result.get("scoped", {}),
        "finding_rejects": 0,
        "structural_failures": 0,
        "rebegin": False,
        "check": None,
        "fix": None,
    }


def _open_dir(args) -> Path:
    d = Path(args.dir)
    if d.is_symlink():
        raise Stop(EXIT_LEDGER, f"refusing a symlinked directory: {d}")
    return d


def cmd_begin(args) -> dict:
    d = _open_dir(args)
    doc_path = str(Path(args.doc).resolve())
    text, sha = args.doc_text, sha256(args.doc_text)
    d.mkdir(parents=True, exist_ok=True)
    with dir_lock(d):
        led = load_ledger(d)
        if led is None:
            if args.expect_round not in (None, 1):
                raise Stop(
                    EXIT_ORDER,
                    f"empty directory means review 1, not {args.expect_round}",
                    review=1,
                )
            led = {
                "format": FORMAT,
                "profile": "spec-panel",
                "doc": doc_path,
                "review": 1,
                "closed": False,
                "halt": None,
                "reviews": {"1": _new_entry(sha)},
            }
            write_file(d / "doc-r1.md", text)
            save_ledger(d, led)
            return {
                "review": 1,
                "message": "review 1 opened: review the full document",
                "surface": None,
                "hunks": [],
                "ignored": 0,
                "coverage": None,
                "priors": [],
            }
        _closed_guard(led)
        if led["doc"] != doc_path:
            raise Stop(
                EXIT_ORDER, f"--doc differs from the loop's document {led['doc']}"
            )
        n = led["review"]
        cur = led["reviews"][str(n)]
        if cur["check"] is None:
            if (
                cur["rebegin"]
                and sha == cur["doc_sha"]
                and args.expect_round in (None, n)
            ):
                cur["rebegin"] = False
                save_ledger(d, led)
                return {
                    "review": n,
                    "message": f"review {n} re-opened once on the same snapshot",
                    "surface": str(d / f"surface-r{n}.md") if n > 1 else None,
                    "hunks": [h["id"] for h in cur["hunks"]],
                    "ignored": cur["ignored"],
                    "coverage": cur["coverage"],
                    "priors": [p["id"] for p in cur["priors"]],
                }
            raise Stop(
                EXIT_ORDER,
                f"review {n} has no accepted check; run the step `status` names",
                review=n,
            )
        m = n + 1
        replay(d, led)
        if m > CAP_REVIEWS:
            raise Stop(
                EXIT_CLOSED,
                f"the cap is {CAP_REVIEWS} reviews; do not review, escalate",
                halt="escalate",
                review=n,
            )
        if args.expect_round is not None and args.expect_round != m:
            raise Stop(
                EXIT_ORDER,
                f"--expect-round {args.expect_round}, but the next review is {m}",
                review=m,
            )
        fix = cur.get("fix") or {}
        if not fix.get("accepted") or fix.get("doc_sha") != sha:
            raise Stop(
                EXIT_ORDER,
                f"no accepted fix map for the current document after review {n}; "
                "run fixcheck (none passed, or the document changed after it)",
                review=m,
            )
        old = _snapshot(d, n, cur)
        hunks, ignored = build_hunks(old, text, m)
        res = check_fixmap(
            fix["map"], hunks, cur["check"]["result"]["blocking_ids"], sha
        )
        if not res["accepted"]:
            raise Stop(
                EXIT_REJECT,
                "fix hunks without a blocking owner; send them back to the reviser",
                review=m,
                unmapped=res["unmapped"],
                errors=res["errors"],
            )
        cov = coverage(hunks, text)
        entry = _new_entry(sha, hunks, ignored, _priors(cur), cur, cov)
        write_file(d / f"doc-r{m}.md", text)
        surface = render_surface(m, hunks, entry["priors"], text, old, entry["owners"])
        write_file(d / f"surface-r{m}.md", surface)
        led["reviews"][str(m)] = entry
        led["review"] = m
        save_ledger(d, led)
        return {
            "review": m,
            "message": f"review {m} opened: review only {d / f'surface-r{m}.md'}",
            "surface": str(d / f"surface-r{m}.md"),
            "hunks": [h["id"] for h in hunks],
            "ignored": len(ignored),
            "coverage": cov,
            "priors": [p["id"] for p in entry["priors"]],
        }


def _deferred_md(led: dict) -> str:
    rows = []
    for n in range(1, led["review"] + 1):
        check = led["reviews"][str(n)].get("check")
        for x in (check or {}).get("result", {}).get("deferred", []):
            text = str(x.get("text", "")).replace("|", "\\|")
            rows.append(
                f"| {x['id']} | {x['sev']} | {x['reason']} | {x.get('at')} | {text} |"
            )
    out = ["# Deferred (pre-existing, not looped on)", "", DEFERRED_SENTENCE, ""]
    if rows:
        out += [
            "| id | reviewer label | reason | at | finding |",
            "|---|---|---|---|---|",
        ] + rows
    else:
        out.append("(none)")
    return "\n".join(out) + "\n"


def _reviser_brief(d: Path, n: int, result: dict) -> str:
    out = [
        f"# Reviser brief: review {n} of {CAP_REVIEWS}",
        "",
        "Your task list is this file, not the whole report. It lists the blocking",
        "findings only; minor findings never reach it.",
        "",
        "| id | label | at | hunk | chain | finding |",
        "|---|---|---|---|---|---|",
    ]
    for b in result["open_blocking"]:
        chain = " -> ".join(b.get("chain") or [b["id"]])
        text = str(b.get("text", "")).replace("|", "\\|")
        out.append(
            f"| {b['id']} | {b.get('sev')} | {b.get('at')} | {b.get('hunk') or '-'} | {chain} | {text} |"
        )
    out += [
        "",
        REVISER_RULES,
        "",
        f"Fix map hunk ids are H{n + 1}.<n>; `fixcheck` prints them.",
    ]
    return "\n".join(out) + "\n"


def _close_md(d: Path, led: dict, n: int, result: dict) -> str:
    out = [""]
    if result["verdict"] == "PASS" or n == CAP_REVIEWS:
        out += [f"## Diffgate close (review {n} of {CAP_REVIEWS})", ""]
        if result["open_blocking"]:
            out.append("Open blocking findings with their fix chains:")
            for b in result["open_blocking"]:
                chain = " -> ".join(b.get("chain") or [b["id"]])
                out.append(f"- {b['id']} ({b.get('sev')}): {chain} :: {b.get('text')}")
        else:
            out.append("Open blocking findings: none.")
        out += [
            "",
            _deferred_md(led).replace("# Deferred", "## Deferred", 1).rstrip(),
            "",
        ]
        if result["verdict"] == "PASS" and result["acceptance"] == "scoped":
            out.append(
                f"scoped PASS: {len(result['held'])} critical or major finding(s) were "
                f"deferred, demoted or withdrawn by the script ({', '.join(sorted(result['held']))}); "
                f"proxy_all {result['proxy_all']}."
            )
        if result["verdict"] == "FAIL":
            out.append("halt: escalate")
    else:
        out += [
            f"Reviser brief: your task list is `{d / f'reviser-brief-r{n}.md'}` "
            f"(blocking ids {', '.join(result['blocking_ids'])}). {REVISER_RULES}",
        ]
    out += ["", result["verdict_line"]]
    return "\n".join(out) + "\n"


def cmd_check(args) -> dict:
    d = _open_dir(args)
    led = load_ledger(d) if d.is_dir() else None
    if led is None:
        raise Stop(EXIT_ORDER, "no ledger in --dir: run begin first")
    _closed_guard(led)
    n = led["review"]
    cur = led["reviews"][str(n)]
    if cur["check"] is not None:
        raise Stop(EXIT_ORDER, f"review {n} already has an accepted check", review=n)
    current = sha256(read_text(led["doc"], "document"))
    degrade = cur["finding_rejects"] >= 1
    errors, result = evaluate(args.report_text, _ctx(d, led, n, current), degrade)
    fields = {"review": n, "dry_run": bool(args.dry_run), "errors": errors}
    structural = any(e["structural"] for e in errors)
    if result is None:
        reject = "\n".join(
            f"{e['rule']} line {e['line']} {e['id'] or ''}: {e['message']}".replace(
                "  ", " "
            )
            for e in errors
        )
        fields.update(accepted=False, verdict=None, verdict_line=None, halt=None)
        if args.dry_run:
            return {
                **fields,
                "exit": EXIT_REJECT,
                "message": "dry run: report rejected; repair the named lines",
            }
        with dir_lock(d):
            if structural:
                cur["structural_failures"] += 1
                if cur["structural_failures"] >= 2:
                    led.update(closed=True, halt="invalid")
                    fields["halt"] = "invalid"
                else:
                    cur["rebegin"] = True
            else:
                cur["finding_rejects"] += 1
            write_file(d / f"reject-r{n}.txt", reject + "\n")
            save_ledger(d, led)
        kind = "structural failure" if structural else "rejected"
        return {
            **fields,
            "exit": EXIT_REJECT,
            "message": f"report {kind}: see {d / f'reject-r{n}.txt'}",
        }
    halt = None
    if result["verdict"] == "PASS":
        halt = "pass"
    elif n == CAP_REVIEWS:
        halt = "escalate"
    fields.update(
        accepted=not args.dry_run,
        verdict=result["verdict"],
        verdict_line=result["verdict_line"],
        acceptance=result["acceptance"],
        blocking=result["blocking"],
        blocking_ids=result["blocking_ids"],
        deferred=[x["id"] for x in result["deferred"]],
        degraded=result["degraded"],
        proxy_all=result["proxy_all"],
        halt=halt,
    )
    if args.dry_run:
        return {
            **fields,
            "message": "dry run: report would be accepted; nothing written",
        }
    with dir_lock(d):
        cur["check"] = {
            "report_sha": sha256(args.report_text),
            "degrade": degrade,
            "result": _norm(result),
        }
        if halt:
            led.update(closed=True, halt=halt)
        write_file(d / f"report-r{n}.md", args.report_text)
        write_file(d / f"result-r{n}.json", json.dumps(_norm(result), indent=1) + "\n")
        write_file(d / "deferred.md", _deferred_md(led))
        if result["verdict"] == "FAIL" and n < CAP_REVIEWS:
            write_file(d / f"reviser-brief-r{n}.md", _reviser_brief(d, n, result))
        write_file(d / f"close-r{n}.md", _close_md(d, led, n, result))
        save_ledger(d, led)
    return {
        **fields,
        "message": f"review {n} accepted; append {d / f'close-r{n}.md'} to the report",
    }


def cmd_fixcheck(args) -> dict:
    d = _open_dir(args)
    led = load_ledger(d) if d.is_dir() else None
    if led is None:
        raise Stop(EXIT_ORDER, "no ledger in --dir: run begin first")
    _closed_guard(led)
    n = led["review"]
    cur = led["reviews"][str(n)]
    if cur["check"] is None:
        raise Stop(EXIT_ORDER, f"review {n} has no accepted check yet", review=n)
    if str(Path(args.doc).resolve()) != led["doc"]:
        raise Stop(
            EXIT_ORDER, f"--doc differs from the loop's document {led['doc']}", review=n
        )
    text, sha = args.doc_text, sha256(args.doc_text)
    old = _snapshot(d, n, cur)
    hunks, _ignored = build_hunks(old, text, n + 1)
    blocking = cur["check"]["result"]["blocking_ids"]
    prefill = candidate_map(hunks, sha)
    map_text = args.map_text if args.map_text is not None else prefill
    res = check_fixmap(map_text, hunks, blocking, sha)
    fields = {
        "review": n,
        "dry_run": bool(args.dry_run),
        "doc_sha": sha,
        "hunks": [h["id"] for h in hunks],
        "candidates": prefill.splitlines(),
        "mapped": res["mapped"],
        "declined": sorted(res["declined"]),
        "withdrawn": sorted(res["declined"]),
        "bytes_by_id": res["bytes_by_id"],
        "hunks_by_id": res["hunks_by_id"],
        "unmapped": res["unmapped"],
        "errors": res["errors"],
        "bytes_before": len(old.encode("utf-8")),
        "bytes_after": len(text.encode("utf-8")),
        "accepted": res["accepted"] and not args.dry_run,
        "halt": None,
    }
    code = EXIT_OK if res["accepted"] else EXIT_REJECT
    if args.dry_run:
        word = "would be accepted" if res["accepted"] else "rejected"
        return {
            **fields,
            "exit": code,
            "message": f"dry run: fix map {word}; nothing written",
        }
    with dir_lock(d):
        fix = cur.get("fix") or {"failed_runs": 0}
        if args.map_text is None:
            write_file(d / f"fixmap-r{n}.txt", prefill)
        fix.update(
            doc_sha=sha,
            map=map_block(map_text),
            owners=res["owners"],
            declined=res["declined"],
        )
        if res["accepted"]:
            fix.update(accepted=True, fix_rejected=False)
            write_file(d / f"fixmap-r{n}.txt", map_block(map_text).strip() + "\n")
            message = f"fix map accepted for review {n}; the coordinator may run begin"
        else:
            fix["failed_runs"] = fix.get("failed_runs", 0) + 1
            fix["accepted"] = False
            message = (
                f"fix map rejected ({fix['failed_runs']} failing run(s) this cycle)"
            )
            if fix["failed_runs"] >= CAP_REVIEWS:
                fix["fix_rejected"] = True
                led.update(closed=True, halt="escalate")
                fields["halt"] = "escalate"
                message = "fix-rejected: three failing fixcheck runs in one fix cycle; escalate"
        cur["fix"] = fix
        save_ledger(d, led)
    return {**fields, "exit": code, "message": message}


def cmd_status(args) -> dict:
    d = Path(args.dir)
    led = load_ledger(d) if d.is_dir() else None
    lock = None
    if (d / LOCK).exists():
        try:
            pid = int((d / LOCK).read_text(encoding="utf-8").strip() or "0")
        except (OSError, ValueError):
            pid = 0
        lock = {
            "path": str(d / LOCK),
            "pid": pid,
            "running": pid > 0 and _pid_alive(pid),
        }
    base = {"lock": lock}
    if lock:
        base["recovery"] = (
            "wait for the running step"
            if lock["running"]
            else "the next writing step removes this stale lock"
        )
    if led is None:
        return {
            **base,
            "review": 0,
            "state": "none",
            "halt": None,
            "next": f"begin --dir {d} --doc <spec> --expect-round 1",
        }
    n = led["review"]
    cur = led["reviews"][str(n)]
    doc = led["doc"]
    if led.get("closed"):
        state = "invalid" if led.get("halt") == "invalid" else "closed"
        return {
            **base,
            "review": n,
            "state": state,
            "halt": led.get("halt"),
            "next": "none: the loop is closed; escalate with the open blocking findings",
        }
    if cur["check"] is None:
        state, nxt = "open", f"review {n}, then check --dir {d} --report <report>"
    else:
        fix = cur.get("fix") or {}
        try:
            current = sha256(Path(doc).read_text(encoding="utf-8"))
        except OSError:
            current = None
        if fix.get("accepted") and fix.get("doc_sha") == current:
            state, nxt = "fixed", f"begin --dir {d} --doc {doc} --expect-round {n + 1}"
        else:
            state = "checked"
            nxt = f"revise per {d / f'reviser-brief-r{n}.md'}, then fixcheck --dir {d} --doc {doc} --map <disposition file>"
    surface = str(d / f"surface-r{n}.md") if n > 1 else None
    return {
        **base,
        "review": n,
        "state": state,
        "halt": None,
        "surface": surface,
        "next": nxt,
    }


# --------------------------------------------------------------------------
# Ledger, lock and atomic writes


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


@contextlib.contextmanager
def dir_lock(d: Path):
    """Exclusive-create lock file holding our pid. Re-entrant in one process.
    A lock whose pid is not running is removed and reported; a live one exits 5."""
    d = Path(d)
    key = str(d.resolve())
    if _HELD.get(key):
        _HELD[key] += 1
        try:
            yield
        finally:
            _HELD[key] -= 1
        return
    lock = d / LOCK
    if lock.is_symlink():
        raise Stop(EXIT_LEDGER, f"refusing a symlinked lock file: {lock}")
    for _attempt in range(2):
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        except FileExistsError:
            try:
                pid = int(lock.read_text(encoding="utf-8").strip() or "0")
            except (OSError, ValueError):
                pid = 0
            if pid > 0 and _pid_alive(pid):
                raise Stop(
                    EXIT_ORDER,
                    f"lock held by running pid {pid}: {lock}; wait for that step to finish",
                    lock={"path": str(lock), "pid": pid},
                ) from None
            lock.unlink(missing_ok=True)
            NOTICES.append(f"removed stale lock of pid {pid} ({lock})")
            continue
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(str(os.getpid()))
        break
    else:
        raise Stop(EXIT_ORDER, f"could not take the lock: {lock}")
    _HELD[key] = 1
    try:
        yield
    finally:
        _HELD.pop(key, None)
        lock.unlink(missing_ok=True)


def write_file(path: Path, data: str) -> None:
    """Temp file plus os.replace; refuses a symlinked target or directory."""
    path = Path(path)
    if path.is_symlink() or path.parent.is_symlink():
        raise Stop(EXIT_LEDGER, f"refusing to write through a symlink: {path}")
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".tmp-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as fh:
            fh.write(data)
        os.replace(tmp, path)
    except BaseException:
        with contextlib.suppress(OSError):
            os.unlink(tmp)
        raise


def load_ledger(d):
    """Ledger dict, or None when the directory holds none. Exit 6 when corrupt."""
    path = Path(d) / LEDGER
    if path.is_symlink():
        raise Stop(EXIT_LEDGER, f"refusing a symlinked ledger: {path}")
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise Stop(EXIT_LEDGER, f"ledger corrupt: {path}: {exc}") from exc
    if not isinstance(data, dict) or data.get("format") != FORMAT:
        raise Stop(EXIT_LEDGER, f"ledger corrupt or of another format: {path}")
    return data


def save_ledger(d, data) -> None:
    d = Path(d)
    if d.is_symlink():
        raise Stop(EXIT_LEDGER, f"refusing a symlinked directory: {d}")
    with dir_lock(d):
        write_file(d / LEDGER, json.dumps(data, indent=1, sort_keys=True) + "\n")


# --------------------------------------------------------------------------
# CLI


class _Parser(argparse.ArgumentParser):
    def error(self, message):  # one JSON object, never argparse's usage text
        raise Stop(EXIT_USAGE, f"usage error: {message}")


def _parser() -> argparse.ArgumentParser:
    p = _Parser(prog="diffgate.py", description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True, parser_class=_Parser)
    b = sub.add_parser(
        "begin", help="open the next review (writes the ledger and snapshots)"
    )
    b.add_argument("--dir", required=True)
    b.add_argument("--doc", required=True)
    b.add_argument("--expect-round", type=int)
    c = sub.add_parser(
        "check", help="check a review report's ## Diffgate findings block"
    )
    c.add_argument("--dir", required=True)
    c.add_argument("--report", required=True)
    c.add_argument(
        "--dry-run", action="store_true", help="validate only; writes no file"
    )
    f = sub.add_parser(
        "fixcheck", help="check the reviser's fix map against the changed hunks"
    )
    f.add_argument("--dir", required=True)
    f.add_argument("--doc", required=True)
    f.add_argument("--map")
    f.add_argument(
        "--dry-run", action="store_true", help="validate only; writes no file"
    )
    s = sub.add_parser(
        "status", help="print the loop state and the next step (read-only)"
    )
    s.add_argument("--dir", required=True)
    return p


def _validate_inputs(args) -> None:
    """Limits and reads run before any subcommand body."""
    args.doc_text = (
        read_text(args.doc, "document") if getattr(args, "doc", None) else None
    )
    args.report_text = (
        read_text(args.report, "report") if getattr(args, "report", None) else None
    )
    if args.report_text is not None:
        machine = sum(
            1
            for line in args.report_text.splitlines()
            if line.startswith(("PRIOR ", "FINDING ", "FINDINGS "))
        )
        if machine > MAX_MACHINE_LINES:
            raise Stop(
                EXIT_USAGE,
                f"report over the {MAX_MACHINE_LINES} machine line limit "
                f"({machine} PRIOR/FINDING lines): {args.report}",
                path=str(args.report),
            )
    args.map_text = (
        read_text(args.map, "fix map") if getattr(args, "map", None) else None
    )


HANDLERS = {
    "begin": cmd_begin,
    "check": cmd_check,
    "fixcheck": cmd_fixcheck,
    "status": cmd_status,
}


def main(argv=None) -> int:
    NOTICES.clear()
    _HELD.clear()
    review = None
    try:
        args = _parser().parse_args(argv)
        _validate_inputs(args)
        out = HANDLERS[args.cmd](args)
        code = out.pop("exit", EXIT_OK)
        message = out.pop("message", "done")
        review = out.pop("review", None)
    except Stop as stop:
        code, message, out = stop.code, stop.message, dict(stop.fields)
        review = out.pop("review", None)
    if NOTICES:
        message = message + " | " + "; ".join(NOTICES)
    payload = {
        "ok": code == EXIT_OK,
        "exit": code,
        "message": message,
        "review": review,
    }
    payload.update(out)
    print(json.dumps(payload))
    return code


if __name__ == "__main__":
    sys.exit(main())
