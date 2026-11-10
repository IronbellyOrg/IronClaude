#!/usr/bin/env python3
"""Fix audit for one /sc:spec-panel-ponytail review loop (issue 346).

Subcommands: prepare, check, apply, verdict.
Standard library only. Exit codes: 0 ok, not-triggered or skipped; 1 an
unreadable input after the trigger check, a failed check or a stopped apply
(the spec is then byte-identical to D/current-before-audit.md); 2 a verdict
that is unparseable or inconsistent (its last line is then `verdict: FAIL`).
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path

# [A-Z][A-Z0-9]*(-[A-Z0-9]+)*[0-9] as whole words: single hyphens allowed inside, so R2-1 and C-R3-15 match.
ID_PAT = r"[A-Z](?:[A-Z0-9]|-(?=[A-Z0-9]))*[0-9]"
ID_RE = re.compile(rf"(?<![\w-])({ID_PAT})(?!\w)(?!-[A-Z0-9])")
LEAD = rf"(?:{ID_PAT})(?:\s*(?:,|/|&|\band\b)\s*(?:{ID_PAT}))*"
ID_CELL_RE = re.compile(rf"{LEAD}(?![\w-])")
BULLET_RE = re.compile(r"^\s*[-*+]\s")
RECORD_RE = re.compile(
    rf"^\s*(?:#+\s*)?(?:[0-9]+[.)]\s+)?(?:\*\*({LEAD})\.|({LEAD})\s*\(|({LEAD})\.(?:\s|$))"
)
YES_CELLS = {"yes", "y", "true"}
NO_CELLS = {"no", "n", "false"}
RANGE_RE = re.compile(r"^([A-Z]+)([0-9]+)-\1([0-9]+)$")
FR_RE = re.compile(r"^FR-[0-9]+$")
PROTECTED_RE = re.compile(r"(?<![\w-])FR-[89](?![\w])")
LABEL_RE = re.compile(r"\b(CRITICAL|MAJOR|MINOR)\b")
KEYED_RE = re.compile(r"\b(?:CRITICAL|MAJOR|MINOR)\s*,\s*([A-Z]{1,2})\b")
KEY_DEF_RE = re.compile(r"\b([A-Z]{1,2})\s*=\s*(non-blocking|blocking|minor)\b", re.I)
BLOCKING_RE = re.compile(r"(?<!non-)\bblocking\b")
STATUS_WORDS = {"open", "resolved", "regressed", "closed", "fixed"}
PRIOR_HEADING_RE = re.compile(r"\b(prior|resolution|previous|earlier)\b", re.I)
LABEL_RANK = {"unknown": 0, "MINOR": 1, "MAJOR": 2, "CRITICAL": 3}
BRIEF = Path(__file__).resolve().parent.parent / "refs" / "auditor-brief.md"


# ---------- shared helpers ----------


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_text(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


def split_lines(text: str) -> list[str]:
    """Lines with their own endings kept, so CRLF and a missing final newline survive."""
    return re.findall(r"[^\n]*\n|[^\n]+$", text)


def write_state(d: Path, state: dict) -> None:
    (d / "state.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def load_state(d: Path) -> dict:
    return json.loads((d / "state.json").read_text(encoding="utf-8"))


def id_tokens(text: str) -> list[str]:
    """Id-shaped whole words; a range such as N1-N11 becomes its members."""
    out: list[str] = []
    for tok in ID_RE.findall(text):
        m = RANGE_RE.match(tok)
        if m and int(m.group(2)) <= int(m.group(3)) <= int(m.group(2)) + 500:
            out.extend(
                f"{m.group(1)}{n}" for n in range(int(m.group(2)), int(m.group(3)) + 1)
            )
        else:
            out.append(tok)
    return out


def lead_ids(line: str) -> list[str]:
    """Ids of a prose record: a line opened by `**ID.`, `ID (` or `ID.` (after at most a
    heading `#` or a numbered-list marker). Bullet lines (`-`, `*`, `+`) and `ID:` lines
    define nothing."""
    if BULLET_RE.match(line):
        return []
    m = RECORD_RE.match(line)
    return id_tokens(next(g for g in m.groups() if g)) if m else []


def multiset_minus(a: list[str], b: list[str]) -> list[str]:
    """Distinct tokens of a whose count in a exceeds their count in b."""
    left: dict[str, int] = {}
    for t in b:
        left[t] = left.get(t, 0) + 1
    out = set()
    for t in a:
        if left.get(t, 0):
            left[t] -= 1
        else:
            out.add(t)
    return sorted(out)


def table_cells(line: str) -> list[str] | None:
    s = line.strip()
    if not s.startswith("|"):
        return None
    return [c.strip() for c in s.strip("|").split("|")]


def is_separator(cs: list[str]) -> bool:
    return any(cs) and all(re.fullmatch(r":?-{2,}:?", c) for c in cs if c)


def report_key(text: str) -> dict[str, str]:
    """Letter key for the `MAJOR, B` format (a report may define its own key)."""
    key = {"B": "blocking", "M": "minor", "NB": "minor"}
    for k, v in KEY_DEF_RE.findall(text):
        key[k] = "blocking" if v.lower() == "blocking" else "minor"
    return key


def parse_grade(line: str, key: dict[str, str]) -> tuple[str, bool | None, bool]:
    """(severity label, blocking flag or None when unknown, FR-8/FR-9 marker) of one line."""
    labels = set(LABEL_RE.findall(line))
    label = max(labels, key=LABEL_RANK.get) if labels else "unknown"
    low = line.lower()
    minor_word = "non-blocking" in low
    blocking_word = bool(BLOCKING_RE.search(low))
    for k in KEYED_RE.findall(line):
        if key.get(k) == "blocking":
            blocking_word = True
        elif key.get(k) == "minor":
            minor_word = True
    if len(labels) > 1 or blocking_word:
        blocking: bool | None = True  # a conflicting grade counts as blocking
    elif minor_word:
        blocking = False
    else:
        blocking = None
    return label, blocking, bool(PROTECTED_RE.search(line))


def parse_report(text: str) -> dict:
    """Graded records and prior-status rows of a review report.

    graded: {id: {label, blocking, protected}} for ids the report grades itself.
    prior: [[id, status]] rows of a prior-findings (resolution) table.
    """
    key = report_key(text)
    seen: dict[str, dict] = {}
    prior: list[list[str]] = []
    in_prior = False
    header: list[str] | None = None
    lines = text.splitlines()
    for n, line in enumerate(lines):
        cs = table_cells(line)
        status, bcell = "", None
        if cs is None:
            header = None
            if line.lstrip().startswith("#"):
                in_prior = bool(PRIOR_HEADING_RE.search(line))
            # a prose record is a non-bullet line opened by `**ID.`, `ID (` or `ID.`; bullets, totals and notes define nothing
            toks = lead_ids(line)
        else:
            if is_separator(cs):
                continue
            nxt = table_cells(lines[n + 1]) if n + 1 < len(lines) else None
            if nxt is not None and is_separator(nxt):
                header = [c.lower() for c in cs]
                continue
            # an id cell holds only ids, ranges and separators; a free-text first cell defines nothing
            cell = cs[0].strip("*` ")
            toks = id_tokens(cell) if ID_CELL_RE.fullmatch(cell) else []
            status = next((c.lower() for c in cs[1:] if c.lower() in STATUS_WORDS), "")
            col = next((i for i, h in enumerate(header or []) if "blocking" in h), None)
            if col is not None and col < len(cs):
                bcell = cs[col].lower()
        toks = [t for t in toks if not FR_RE.match(t)]
        if not toks:
            continue
        label, blocking, fr = parse_grade(line, key)
        if bcell in YES_CELLS:
            blocking = True
        elif bcell in NO_CELLS and blocking is None:
            blocking = False
        if in_prior or (status and label == "unknown"):
            prior.extend([t, status] for t in toks)
            continue
        if label == "unknown" and not fr:
            continue  # no severity label: an incidental mention, not a graded record
        for rid in toks:
            g = seen.setdefault(rid, {"label": "unknown", "flags": [], "fr": False})
            if LABEL_RANK[label] > LABEL_RANK[g["label"]]:
                g["label"] = label
            g["flags"].append(blocking)
            g["fr"] = g["fr"] or fr
    graded = {
        rid: {
            "label": g["label"],
            # unknown (None) or conflicting grades count as blocking
            "blocking": set(g["flags"]) != {False},
            "protected": g["label"] == "CRITICAL" or g["fr"],
        }
        for rid, g in seen.items()
    }
    return {"graded": graded, "prior": prior}


def last_line(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return lines[-1] if lines else ""


def hunks_of(b_lines: list[str], s_lines: list[str]) -> list[dict]:
    """Line-level hunks of B to S with whitespace-only lines ignored.

    Spans are 0-based half-open indices into the original line lists; an empty
    span is the insertion point after the previous non-blank line.
    """
    bi = [i for i, ln in enumerate(b_lines) if ln.strip()]
    si = [i for i, ln in enumerate(s_lines) if ln.strip()]
    bt = [b_lines[i].rstrip("\r\n") for i in bi]
    st = [s_lines[i].rstrip("\r\n") for i in si]

    def span(idx: list[int], a: int, z: int) -> list[int]:
        if a < z:
            return [idx[a], idx[z - 1] + 1]
        pos = idx[a - 1] + 1 if a > 0 else 0
        return [pos, pos]

    out = []
    sm = difflib.SequenceMatcher(None, bt, st, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal":
            out.append(
                {
                    "id": f"H{len(out) + 1}",
                    "tag": tag,
                    "s": span(si, j1, j2),
                    "b": span(bi, i1, i2),
                }
            )
    return out


def changed_lines(b_lines: list[str], s_lines: list[str]) -> int:
    """Lines of S that differ from B (whitespace-only lines ignored)."""
    return sum(h["s"][1] - h["s"][0] for h in hunks_of(b_lines, s_lines))


def disposition_lines(text: str, blocking_ids: set[str]) -> set[int]:
    """1-based S lines the disposition table's `Where` column lists under a blocking id."""
    out: set[int] = set()
    where = None
    for line in text.splitlines():
        cs = table_cells(line)
        if cs is None:
            where = None
            continue
        if where is None:
            low = [c.lower() for c in cs]
            # the header may say `Where` or `Where (revised spec)`
            where = next((i for i, c in enumerate(low) if c.startswith("where")), None)
            continue
        if is_separator(cs) or where >= len(cs):
            continue
        ids = {t for c in cs[:where] for t in id_tokens(c)}
        if ids & blocking_ids:
            for a, z in re.findall(r":([0-9]+)(?:-([0-9]+))?", cs[where]):
                out.update(range(int(a), int(z or a) + 1))
    return out


# ---------- prepare ----------


def classify(h: dict, graded: dict, prior_only: set[str], disp: set[int] | None) -> str:
    known = [t for t in h["cited"] if t in graded or t in prior_only]
    if not known:
        return "unattributed"
    if any(t in prior_only for t in known):
        return "foreign-id"
    overlaps = disp is not None and any(h["s"][0] < n <= h["s"][1] for n in disp)
    if (
        disp is None
        or overlaps
        or any(graded[t]["blocking"] or graded[t]["protected"] for t in known)
    ):
        return "blocking-involved"
    return "minor-only"


def cmd_prepare(a: argparse.Namespace) -> int:
    d = Path(a.out)
    d.mkdir(parents=True, exist_ok=True)
    b, s, r = Path(a.baseline), Path(a.current), Path(a.report)
    state: dict = {
        "baseline": str(b.resolve()),
        "current": str(s.resolve()),
        "report": str(r.resolve()),
        "dispositions": str(Path(a.dispositions).resolve()) if a.dispositions else None,
        "out": str(d.resolve()),
        "ids": {},
        "prior_only": [],
    }

    def stop(audit: str) -> int:
        state["audit"] = audit
        write_state(d, state)
        print(f"audit: {audit}")
        return 0

    try:
        rtext = read_text(r)
    except (OSError, UnicodeDecodeError):
        state["trigger"] = "report unreadable"
        return stop("not-triggered(report unreadable)")
    parsed = parse_report(rtext)
    graded = parsed["graded"]
    prior_only = sorted({p[0] for p in parsed["prior"]} - set(graded))
    state["ids"], state["prior_only"] = graded, prior_only
    if not any(ln.startswith("review: 2 of 3") for ln in rtext.splitlines()):
        state["trigger"] = "no review: 2 of 3 line"
        return stop("not-triggered(not review 2 of 3)")
    if last_line(rtext) != "verdict: FAIL":
        state["trigger"] = "last line is not verdict: FAIL"
        return stop("not-triggered(review 2 did not fail)")
    try:
        btext, stext = read_text(b), read_text(s)
    except (OSError, UnicodeDecodeError):
        state["trigger"] = "spec or baseline unreadable"
        return stop("not-triggered(spec or baseline unreadable)")
    b_lines, s_lines = split_lines(btext), split_lines(stext)
    hunks = hunks_of(b_lines, s_lines)
    if not hunks:
        state["trigger"] = "empty diff"
        return stop("not-triggered(empty diff)")
    state["trigger"] = "triggered"

    disp = None
    if a.dispositions:
        try:
            dtext = read_text(Path(a.dispositions))
        except (OSError, UnicodeDecodeError) as e:
            print(f"error: dispositions unreadable: {e}", file=sys.stderr)
            return 1
        blocking_ids = {i for i, g in graded.items() if g["blocking"] or g["protected"]}
        disp = disposition_lines(dtext, blocking_ids)

    state["sha256_current"], state["sha256_baseline"] = sha256(s), sha256(b)
    (d / "current-before-audit.md").write_bytes(s.read_bytes())
    for h in hunks:
        s_txt = "".join(s_lines[h["s"][0] : h["s"][1]])
        b_txt = "".join(b_lines[h["b"][0] : h["b"][1]])
        h["cited"] = multiset_minus(id_tokens(s_txt), id_tokens(b_txt))
        h["added"] = len(s_txt.encode("utf-8"))
        h["removed"] = len(b_txt.encode("utf-8"))
        h["class"] = classify(h, graded, set(prior_only), disp)
        known = [t for t in h["cited"] if t in graded]
        h["grade"] = (
            ",".join(
                f"{t}:{'blocking' if graded[t]['blocking'] else 'minor'}" for t in known
            )
            or "-"
        )
    state["hunks"] = hunks
    if sum(h["class"] == "unattributed" for h in hunks) * 2 > len(hunks):
        return stop("skipped(ids not citable)")

    rows = [
        "| hunk | lines in S | lines in B | bytes added | bytes removed | ids cited | grade | class |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for h in hunks:
        known = [t for t in h["cited"] if t in graded or t in prior_only]
        rows.append(
            f"| {h['id']} | {h['s'][0] + 1}-{h['s'][1]} | {h['b'][0] + 1}-{h['b'][1]} | "
            f"{h['added']} | {h['removed']} | {', '.join(known) or '-'} | {h['grade']} | {h['class']} |"
        )
    (d / "fix-list.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    brief = BRIEF.read_text(encoding="utf-8")
    for ph, val in (
        ("<DISP>", state["dispositions"] or "none"),
        ("<D>", state["out"]),
        ("<R>", state["report"]),
        ("<B>", state["baseline"]),
        ("<S>", state["current"]),
    ):
        brief = brief.replace(ph, val)
    (d / "brief.md").write_text(brief, encoding="utf-8")
    return stop("prepared")


# ---------- check ----------

AUDIT_COLS = [
    "id",
    "hunks",
    "claimed",
    "validated",
    "necessary",
    "smaller alternative",
    "verdict",
    "evidence",
]
AUDITORS = {"auditor: ponytail-review", "auditor: inline-rubric"}
ENUMS = {
    "validated": {"blocking", "minor"},
    "necessary": {"yes", "no"},
    "verdict": {"keep", "shrink", "revert"},
}
WORD_RE = re.compile(r"\S+")


def parse_audit(text: str) -> tuple[list[dict], list[dict], list[tuple[str, str]]]:
    """Table rows, json edit rows and K2 failures of audit.md."""
    fails: list[tuple[str, str]] = []
    lines = text.splitlines()
    head = [ln.strip() for ln in lines if ln.strip()][:2]
    if not head or head[0] not in AUDITORS:
        fails.append(("K2", "auditor header"))
    if len(head) < 2 or head[1] != "auditor-isolation: own-session":
        fails.append(("K2", "auditor-isolation header"))
    blocks: list[list[str]] = []
    fences: list[list[str]] = []
    fence: list[str] | None = None
    in_table = False
    for ln in lines:
        s = ln.strip()
        if fence is not None:
            if s.startswith("```"):
                fences.append(fence)
                fence = None
            else:
                fence.append(ln)
            continue
        if s.startswith("```"):
            fence, in_table = [], False
            continue
        if s.startswith("|"):
            if not in_table:
                blocks.append([])
            blocks[-1].append(s)
            in_table = True
        else:
            in_table = False
    if fence is not None:
        fails.append(("K2", "unclosed json block"))
    rows: list[dict] = []
    if len(blocks) != 1:
        fails.append(("K2", f"{len(blocks)} tables, need exactly 1"))
    else:
        tbl = [table_cells(r) or [] for r in blocks[0]]
        if [c.lower() for c in tbl[0]] != AUDIT_COLS:
            fails.append(("K2", "table columns"))
        body = tbl[2:] if len(tbl) > 1 and is_separator(tbl[1]) else tbl[1:]
        for cs in body:
            if len(cs) != len(AUDIT_COLS):
                fails.append(("K2", f"row {cs[0] if cs else '?'} has {len(cs)} cells"))
                continue
            r = dict(zip(AUDIT_COLS, cs))
            r["hunk_ids"] = re.findall(r"\bH[0-9]+\b", r["hunks"])
            rows.append(r)
    edits: list[dict] = []
    if len(fences) > 1:
        fails.append(("K2", f"{len(fences)} json blocks"))
    for f in fences[:1]:
        try:
            data = json.loads("\n".join(f))
            if not isinstance(data, list):
                raise ValueError("not a list")
            for e in data:
                keys = ("id", "hunk", "op", "old", "new")
                if not (
                    isinstance(e, dict) and all(isinstance(e.get(k), str) for k in keys)
                ):
                    raise ValueError("an edit row needs string id, hunk, op, old, new")
                if e["op"] not in ("delete", "restore"):
                    raise ValueError(f"op {e['op']!r}")
            edits = data
        except ValueError as e:  # json.JSONDecodeError is a ValueError
            fails.append(("K2", f"json block: {e}"))
    return rows, edits, fails


def word_spans(text: str, base: int = 0) -> list[tuple[int, int, str]]:
    return [
        (base + m.start(), base + m.end(), m.group()) for m in WORD_RE.finditer(text)
    ]


def line_offsets(lines: list[str]) -> list[int]:
    out = [0]
    for ln in lines:
        out.append(out[-1] + len(ln))
    return out


def check_edit(e, h, stext, btext, s_off, b_off, ids, prior_only):
    """K7 (delete) or K8 (restore) failures of one edit row; returns (fails, span)."""
    rule = "K7" if e["op"] == "delete" else "K8"
    tag = f"{e['id']}/{e['hunk']}"
    n = stext.count(e["old"]) if e["old"] else 0
    if n != 1:
        return [(rule, f"{tag} old occurs {n} times in S")], None
    pos = stext.index(e["old"])
    end = pos + len(e["old"])
    cs, ce = s_off[h["s"][0]], s_off[h["s"][1]]
    if not (cs <= pos and end <= ce):
        return [(rule, f"{tag} old is outside hunk {e['hunk']}")], None
    s_words = word_spans(stext[cs:ce], cs)
    b_text = btext[b_off[h["b"][0]] : b_off[h["b"][1]]]
    b_words = word_spans(b_text)
    ops = difflib.SequenceMatcher(
        None, [w[2] for w in b_words], [w[2] for w in s_words], autojunk=False
    ).get_opcodes()
    fails = []
    if e["op"] == "delete":
        ow = [w[2] for w in word_spans(e["old"])]
        nw = [w[2] for w in word_spans(e["new"])]
        dops = difflib.SequenceMatcher(None, ow, nw, autojunk=False).get_opcodes()
        if any(t not in ("equal", "delete") for t, *_ in dops):
            return [("K7", f"{tag} new is not old with words removed")], (pos, end)
        added = {
            s_words[j][0]
            for t, _, _, j1, j2 in ops
            if t != "equal"
            for j in range(j1, j2)
        }
        old_words = word_spans(e["old"], pos)
        removed = [
            old_words[i]
            for t, i1, i2, _, _ in dops
            if t == "delete"
            for i in range(i1, i2)
        ]
        bad = [w[2] for w in removed if w[0] not in added]
        if bad:
            fails.append(("K7", f"{tag} removes baseline words {bad}"))
        kept = set(id_tokens(stext[cs:pos] + e["new"] + stext[end:ce]))
        lost = [
            t for t in h["cited"] if (t in ids or t in prior_only) and t not in kept
        ]
        if lost:
            fails.append(("K7", f"{tag} drops the hunk's id {lost}"))
        return fails, (pos, end)
    if h["class"] != "minor-only":
        return [("K8", f"{tag} restore in a {h['class']} hunk")], (pos, end)
    starts, ends = [w[0] for w in s_words], [w[1] for w in s_words]
    if pos not in starts or end not in ends:
        return [("K8", f"{tag} old does not start and end on whole words")], (pos, end)
    ta, tb = starts.index(pos), ends.index(end) + 1

    def to_b(x: int) -> int | None:
        """Baseline word index aligned with S word boundary x, or None inside a change."""
        for t, i1, i2, j1, j2 in ops:
            if t == "equal" and j1 <= x <= j2:
                return i1 + (x - j1)
            if x == j1:
                return i1
            if x == j2:
                return i2
        return None

    ba, bb = to_b(ta), to_b(tb)
    if ba is None or bb is None or ba > bb:
        return [("K8", f"{tag} old is not an aligned span")], (pos, end)
    aligned = b_text[b_words[ba][0] : b_words[bb - 1][1]] if ba < bb else ""
    if e["new"] != aligned:
        fails.append(("K8", f"{tag} new is not the aligned baseline span"))
    return fails, (pos, end)


def run_checks(d: Path, state: dict) -> tuple[list[tuple[str, str]], list[str], dict]:
    """K1-K10 over D. Returns failures, DOWNGRADE/UPGRADE lines and the parsed audit."""
    fails: list[tuple[str, str]] = []
    logs: list[str] = []
    s, b = Path(state["current"]), Path(state["baseline"])
    try:
        if sha256(s) != state["sha256_current"]:
            fails.append(("K1", "spec sha256 changed"))
        if sha256(b) != state["sha256_baseline"]:
            fails.append(("K1", "baseline sha256 changed"))
        stext, btext = read_text(s), read_text(b)
        audit_text = read_text(d / "audit.md")
        fix_list = read_text(d / "fix-list.md")
    except (OSError, UnicodeDecodeError) as e:
        return fails + [("K2", f"unreadable input: {e}")], logs, {}
    ids, prior_only = state["ids"], set(state["prior_only"])
    hunks = {h["id"]: h for h in state["hunks"]}
    if re.findall(r"^\|\s*(H[0-9]+)\s*\|", fix_list, re.M) != list(hunks):
        fails.append(("K3", "fix-list.md does not match state.json"))
    rows, edits, k2 = parse_audit(audit_text)
    fails += k2

    def rdef(h: dict) -> list[str]:
        return [t for t in h["cited"] if t in ids]

    # K3 coverage
    by_id: dict[str, dict] = {}
    dash: dict[str, dict] = {}
    for r in rows:
        rid = r["id"]
        for hid in r["hunk_ids"]:
            if hid not in hunks:
                fails.append(("K3", f"{rid} names unknown hunk {hid}"))
        if rid == "-":
            if not r["hunk_ids"]:
                fails.append(("K3", "- row names no hunk"))
            for hid in r["hunk_ids"]:
                if hid in hunks and rdef(hunks[hid]):
                    fails.append(
                        ("K3", f"- row for {hid}, which cites an id R defines")
                    )
                if hid in dash:
                    fails.append(("K3", f"duplicate - row for {hid}"))
                dash[hid] = r
            continue
        if rid not in ids:
            fails.append(("K3", f"{rid} is not an id R defines"))
            continue
        if rid in by_id:
            fails.append(("K3", f"duplicate row {rid}"))
        by_id[rid] = r
        for hid in r["hunk_ids"]:
            if hid in hunks and rid not in hunks[hid]["cited"]:
                fails.append(("K3", f"{rid} names {hid}, which does not cite it"))
    covered = {hid for r in rows for hid in r["hunk_ids"]}
    missing: set[str] = set()
    for hid, h in hunks.items():
        if hid not in covered:
            fails.append(("K3", f"{hid} is in no row"))
        if not rdef(h) and hid not in dash:
            fails.append(("K3", f"{hid} cites no id R defines and has no - row"))
        for t in rdef(h):
            if t not in by_id and t not in missing:
                fails.append(("K3", f"missing row {t}"))
                missing.add(t)

    # K4, K5, K10 per row; K6 revert conditions and the drift log
    for r in rows:
        rid = r["id"]
        if rid in ids:
            want = "blocking" if ids[rid]["blocking"] else "minor"
            if r["claimed"] != want:
                fails.append(("K4", f"{rid} claimed {r['claimed']!r}, R grades {want}"))
            if r["validated"] == "minor" and ids[rid]["blocking"]:
                logs.append(f"DOWNGRADE {rid}")
            elif r["validated"] == "blocking" and not ids[rid]["blocking"]:
                logs.append(f"UPGRADE {rid}")
        elif rid == "-" and r["claimed"] != "-":
            fails.append(("K4", f"- row claimed {r['claimed']!r}"))
        for col, allowed in ENUMS.items():
            if r[col] not in allowed:
                fails.append(("K5", f"{rid} {col} {r[col]!r}"))
        needs = r["verdict"] == "revert" or (
            r["verdict"] == "keep" and r["validated"] == "blocking"
        )
        if needs and len(r["evidence"]) < 20:
            fails.append(("K10", f"{rid} evidence shorter than 20 characters"))
        if r["verdict"] != "revert":
            continue
        for hid in r["hunk_ids"]:
            h = hunks.get(hid)
            if h is None:
                continue
            if h["class"] != "minor-only":
                fails.append(("K6", f"{rid} revert of {h['class']} hunk {hid}"))
                continue
            for t in rdef(h):
                g, tr = ids[t], by_id.get(t, {})
                if g["blocking"] or g["protected"] or tr.get("validated") != "minor":
                    fails.append(
                        (
                            "K6",
                            f"{rid} revert of {hid}: {t} is not minor in R and validated minor",
                        )
                    )

    # K7, K8 edit rows; K9 overlap and shrink rows
    s_off, b_off = line_offsets(split_lines(stext)), line_offsets(split_lines(btext))
    spans: list[tuple[int, int, int]] = []
    for n, e in enumerate(edits, 1):
        h = hunks.get(e["hunk"])
        r = dash.get(e["hunk"]) if e["id"] == "-" else by_id.get(e["id"])
        if h is None or r is None or e["hunk"] not in r["hunk_ids"]:
            fails.append(
                (
                    "K9",
                    f"edit row {n} ({e['id']}/{e['hunk']}) has no table row for that id and hunk",
                )
            )
            continue
        f, span = check_edit(e, h, stext, btext, s_off, b_off, ids, prior_only)
        fails += f
        if span:
            spans.append((span[0], span[1], n))
    spans.sort()
    for (_, a1, an), (b0, _, bn) in zip(spans, spans[1:]):
        if b0 < a1:
            fails.append(("K9", f"edit rows {an} and {bn} overlap"))
    for i, e in enumerate(edits, 1):
        for j, f in enumerate(edits, 1):
            if i != j and f["old"] and f["old"] in e["new"]:
                fails.append(("K9", f"edit row {i} new contains edit row {j} old"))
    for r in rows:
        if r["verdict"] == "shrink" and not any(e["id"] == r["id"] for e in edits):
            fails.append(("K9", f"{r['id']} shrink has no edit row"))
    return fails, logs, {"rows": rows, "edits": edits, "by_id": by_id, "dash": dash}


def not_ready(state: dict, verb: str) -> int | None:
    """Exit code when there is nothing to check or apply, else None."""
    audit = state.get("audit", "")
    if audit in ("prepared", "checked"):
        return None
    print(f"nothing to {verb}: audit: {audit}")
    return 0 if audit.startswith(("not-triggered", "skipped(ids")) else 1


def record_check(d: Path, state: dict) -> tuple[bool, dict]:
    """Run K1-K10, write check.log and the audit state; True when the check passed."""
    fails, logs, parsed = run_checks(d, state)
    out = [f"CHECK_FAIL {rule} {row}" for rule, row in fails] or ["CHECK_OK"]
    (d / "check.log").write_text("\n".join(out + logs) + "\n", encoding="utf-8")
    state["audit"] = "skipped(check failed)" if fails else "checked"
    write_state(d, state)
    print("\n".join(out + logs))
    if fails:
        print(f"audit: {state['audit']}")
    return not fails, parsed


def cmd_check(a: argparse.Namespace) -> int:
    d = Path(a.dir)
    state = load_state(d)
    code = not_ready(state, "check")
    if code is not None:
        return code
    ok, _ = record_check(d, state)
    if ok:
        print(f"audit: {state['audit']}")
    return 0 if ok else 1


# ---------- apply ----------

STRENGTH = {"revert": 1, "shrink": 2, "keep": 3}  # keep over shrink over revert


def atomic_write(path: Path, data: bytes) -> None:
    """Temp file in the same folder, then os.replace; the mode of `path` is kept."""
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp, os.stat(path).st_mode & 0o7777)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def cmd_apply(a: argparse.Namespace) -> int:
    d = Path(a.dir)
    state = load_state(d)
    s, b = Path(state["current"]), Path(state["baseline"])
    log_path = d / "apply-log.md"
    if log_path.exists():
        m = re.search(r"^sha256 after: ([0-9a-f]{64})$", read_text(log_path), re.M)
        if m and s.exists() and sha256(s) == m.group(1):
            print("already applied")
            return 0
    code = not_ready(state, "apply")
    if code is not None:
        return code
    ok, parsed = record_check(d, state)
    if not ok:
        return 1

    def stop(why: str) -> int:
        state["audit"] = "skipped(apply stopped)"
        write_state(d, state)
        print(f"APPLY_STOP: nothing written ({why})")
        print(f"audit: {state['audit']}")
        return 1

    stext, btext = read_text(s), read_text(b)
    s_lines, b_lines = split_lines(stext), split_lines(btext)
    s_off = line_offsets(s_lines)
    ids, hunks = state["ids"], {h["id"]: h for h in state["hunks"]}
    rows, edits, by_id = parsed["rows"], parsed["edits"], parsed["by_id"]

    def rdef(h: dict) -> list[str]:
        return [t for t in h["cited"] if t in ids]

    verdicts: dict[str, list[str]] = {hid: [] for hid in hunks}
    for r in rows:
        for hid in r["hunk_ids"]:
            verdicts.setdefault(hid, []).append(r["verdict"])
    strongest = {hid: max(v, key=STRENGTH.get) for hid, v in verdicts.items() if v}
    # a hunk goes back to B only when every id on it has verdict revert
    reverted = {
        hid
        for hid, h in hunks.items()
        if verdicts[hid]
        and strongest[hid] == "revert"
        and all(by_id.get(t, {}).get("verdict") == "revert" for t in rdef(h))
    }
    actions: list[tuple[int, int, str]] = []
    log: list[str] = []
    for hid in sorted(reverted, key=lambda x: hunks[x]["s"][0]):
        h = hunks[hid]
        old = "".join(s_lines[h["s"][0] : h["s"][1]])
        new = "".join(
            b_lines[h["b"][0] : h["b"][1]]
        )  # the baseline lines, never model text
        actions.append((s_off[h["s"][0]], s_off[h["s"][1]], new))
        who = ",".join(rdef(h)) or "-"
        log.append(
            f"applied {who} {hid} revert bytes {len(old.encode())} -> {len(new.encode())}"
        )
    shrunk: set[str] = set()

    def hunk_bytes(hid: str) -> int:
        h = hunks.get(hid)
        return len("".join(s_lines[h["s"][0] : h["s"][1]]).encode()) if h else 0

    for r in rows:
        rid = r["id"]
        if r["verdict"] == "revert":
            for hid in r["hunk_ids"]:
                if hid not in reverted:
                    n_b = hunk_bytes(hid)
                    log.append(f"REVERT_SHARED {rid}")
                    log.append(
                        f"SKIP {rid} {hid} revert shared with a kept or shrunk id bytes {n_b} -> {n_b}"
                    )
        elif r["verdict"] == "keep":
            for hid in r["hunk_ids"]:
                n_b = hunk_bytes(hid)
                log.append(f"SKIP {rid} {hid} keep bytes {n_b} -> {n_b}")
    for n, e in enumerate(edits, 1):
        tag = f"{e['id']} {e['hunk']} {e['op']} row {n}"
        if strongest.get(e["hunk"]) != "shrink":
            n_b = len(e["old"].encode())
            log.append(
                f"SKIP {tag} ({strongest.get(e['hunk'])} wins on {e['hunk']}) bytes {n_b} -> {n_b}"
            )
            continue
        if stext.count(e["old"]) != 1:
            return stop(f"{tag}: old does not occur exactly once")
        pos = stext.index(e["old"])
        actions.append((pos, pos + len(e["old"]), e["new"]))
        shrunk.add(e["hunk"])
        log.append(
            f"applied {tag} bytes {len(e['old'].encode())} -> {len(e['new'].encode())}"
        )
    actions.sort()
    for (a0, a1, _), (b0, b1, _) in zip(actions, actions[1:]):
        if b0 < a1 or (a0 == b0 and (a0 == a1 or b0 == b1)):
            return stop("two rows overlap")
    new_text = stext
    for start, end, repl in reversed(actions):  # bottom-up keeps earlier offsets valid
        new_text = new_text[:start] + repl + new_text[end:]
    data = new_text.encode("utf-8")
    before = sha256(s)
    try:
        atomic_write(s, data)
        if s.read_bytes() != data:
            raise OSError("read-back differs")
    except OSError as e:
        atomic_write(s, (d / "current-before-audit.md").read_bytes())
        return stop(f"write failed: {e}")
    closed = [
        f"{t} {ids[t]['label']}"
        for t in sorted({t for h in hunks.values() for t in rdef(h)})
        if all(hid in reverted for hid, h in hunks.items() if t in rdef(h))
    ]
    kept = len(hunks) - len(reverted) - len(shrunk - reverted)
    summary = f"applied(reverted={len(reverted)}, shrunk={len(shrunk - reverted)}, kept={kept})"
    applied = sum(ln.startswith("applied") for ln in log)
    log += [
        f"totals: applied={applied} skipped={sum(ln.startswith('SKIP') for ln in log)}",
        f"sha256 before: {before}",
        f"sha256 after: {sha256(s)}",
        f"changed lines vs baseline before: {changed_lines(b_lines, s_lines)}",
        f"changed lines vs baseline after: {changed_lines(b_lines, split_lines(new_text))}",
    ]
    (d / "apply-log.md").write_text("\n".join(log) + "\n", encoding="utf-8")
    (d / "closed-minor.txt").write_text(
        "".join(c + "\n" for c in closed), encoding="utf-8"
    )
    state["audit"] = summary
    write_state(d, state)
    print(f"audit: {summary}")
    return 0


# ---------- verdict ----------

VERDICT_RE = re.compile(r"verdict: (PASS|FAIL)")
CM = ("CRITICAL", "MAJOR")


def unlabelled_blocking(text: str, r2_ids: set[str] = frozenset()) -> list[str]:
    """Ids of review-3 table rows outside the resolution table that carry no severity
    label and are not read as non-blocking: parse_report needs a label, but an unknown
    grade still counts as blocking here (fail closed). A status-word row of review-2
    ids is a resolution note only when it does not grade them blocking."""
    key = report_key(text)
    out: list[str] = []
    in_prior = False
    header: list[str] | None = None
    lines = text.splitlines()
    for n, line in enumerate(lines):
        if line.lstrip().startswith("#"):
            in_prior, header = bool(PRIOR_HEADING_RE.search(line)), None
            continue
        cs = table_cells(line)
        if not cs:
            header = None
            continue
        if in_prior or is_separator(cs):
            continue
        nxt = table_cells(lines[n + 1]) if n + 1 < len(lines) else None
        if nxt is not None and is_separator(nxt):
            header = [c.lower() for c in cs]
            continue  # a header row
        cell = cs[0].strip("*` ")
        if not ID_CELL_RE.fullmatch(cell) or LABEL_RE.search(line):
            continue
        toks = [t for t in id_tokens(cell) if not FR_RE.match(t)]
        blocking = parse_grade(line, key)[1]
        col = next((i for i, h in enumerate(header or []) if "blocking" in h), None)
        if col is not None and col < len(cs):
            if cs[col].lower() in YES_CELLS:
                blocking = True
            elif cs[col].lower() in NO_CELLS and blocking is None:
                blocking = False
        # a row that grades its ids blocking is a finding, never a resolution note
        if (
            blocking is not True
            and any(c.lower() in STATUS_WORDS for c in cs[1:])
            and set(toks) <= r2_ids
        ):
            continue
        if blocking is not False:
            out += toks
    return out


def closed_blocking_rows(text: str, closed: set[str]) -> list[str]:
    """Closed ids that a review-3 table row grades blocking explicitly, in any section,
    the resolution table included (a bare label stays a note; only a positive blocking
    grade is a relabelling dispute)."""
    key = report_key(text)
    hits: list[str] = []
    header: list[str] | None = None
    lines = text.splitlines()
    for n, line in enumerate(lines):
        cs = table_cells(line)
        if not cs:
            header = None
            continue
        if is_separator(cs):
            continue
        nxt = table_cells(lines[n + 1]) if n + 1 < len(lines) else None
        if nxt is not None and is_separator(nxt):
            header = [c.lower() for c in cs]
            continue
        cell = cs[0].strip("*` ")
        if not ID_CELL_RE.fullmatch(cell):
            continue
        blocking = parse_grade(line, key)[1] is True
        col = next((i for i, h in enumerate(header or []) if "blocking" in h), None)
        if col is not None and col < len(cs) and cs[col].lower() in YES_CELLS:
            blocking = True
        if blocking:
            hits += [t for t in id_tokens(cell) if t in closed]
    return list(dict.fromkeys(hits))


def cmd_verdict(a: argparse.Namespace) -> int:
    """Compute review 3's verdict from files; never turns a FAIL into a PASS."""
    d = Path(a.dir)
    out: list[str] = []
    unparseable: list[str] = []
    try:
        state = load_state(d)
    except (OSError, ValueError):
        state, unparseable = {}, ["state.json unreadable"]
    audit = state.get("audit", "missing")
    ids = state.get("ids", {})
    applied = audit.startswith("applied(")
    closed: list[str] = []
    if applied and (d / "closed-minor.txt").exists():
        closed = [
            ln.split()[0]
            for ln in read_text(d / "closed-minor.txt").splitlines()
            if ln.strip()
        ]
    downgrades: list[str] = []
    if (d / "check.log").exists():
        downgrades = [
            ln.split()[1]
            for ln in read_text(d / "check.log").splitlines()
            if ln.startswith("DOWNGRADE ")
        ]
    # owner decision: deferred (closed) and demoted (DOWNGRADE) findings stay open in the
    # owner count, whatever the audit state; nothing here lowers it
    held = closed + [t for t in dict.fromkeys(downgrades) if t not in closed]
    try:
        r3 = read_text(Path(a.report))
    except (OSError, UnicodeDecodeError) as e:
        r3, unparseable = "", unparseable + [f"review-3 report unreadable: {e}"]
    parsed = parse_report(r3)
    prior, new = parsed["prior"], parsed["graded"]
    if r3 and not prior:
        unparseable.append("no resolution table rows in the review-3 report")
    blank = [t for t, st in prior if not st]
    if blank:
        unparseable.append(
            f"resolution rows without a status ({', '.join(sorted(STATUS_WORDS))}): {', '.join(blank)}"
        )
    report_line = last_line(r3)
    m = VERDICT_RE.fullmatch(report_line)
    if r3 and not m:
        unparseable.append("the review-3 report does not end with a verdict line")

    listed_open = [t for t, st in prior if st in ("open", "regressed")]
    prior_open = [t for t in listed_open if ids.get(t, {}).get("blocking")]
    new_blocking = list(
        dict.fromkeys(
            [t for t, g in new.items() if g["blocking"]]
            + unlabelled_blocking(r3, set(ids) | set(state.get("prior_only", [])))
        )
    )
    open_ids = list(dict.fromkeys(prior_open + new_blocking))
    disagree = list(
        dict.fromkeys(
            [t for t in closed if t in new_blocking]
            + closed_blocking_rows(r3, set(closed))
        )
    )
    computed = "FAIL" if open_ids else "PASS"
    if a.report_rule == "427" and m and m.group(1) != computed:
        disagree.append(f"report says {m.group(1)}, computed {computed}")
    new_cm = sum(g["label"] in CM for g in new.values())
    # a held id is skipped only when new_cm already counts it, so the count never drops below the held total
    held_cm = sum(
        ids.get(t, {}).get("label") in CM and not (t in new and new[t]["label"] in CM)
        for t in held
    )

    out.append(f"open blocking: {', '.join(open_ids) or 'none'}")
    out.append(
        f"closed-minor (deferred, counted open in the owner count): {', '.join(closed) or 'none'}"
    )
    out += [f"closed-minor, listed open: {t}" for t in closed if t in listed_open]
    out.append(f"downgrades logged: {', '.join(downgrades) or 'none'}")
    held_txt = ", ".join(f"{t} {ids.get(t, {}).get('label', 'unknown')}" for t in held)
    out.append(f"held open (deferred or demoted): {held_txt or 'none'}")
    out.append(f"review-3 new critical+major: {new_cm}")
    out.append(
        f"review-3 critical+major (owner count, held findings included): {new_cm + held_cm}"
    )
    out.append(f"audit: {audit}")
    if a.report_rule == "any-severity":
        out.append(f"t09-verdict: {report_line}")
    else:
        out.append(f"report verdict: {report_line}")
    out += [f"unparseable: {u}" for u in unparseable]
    if disagree:
        out.append(f"consistency: DISAGREE ({'; '.join(disagree)})")
    fail = bool(open_ids or disagree or unparseable)
    if m and m.group(1) == "FAIL":
        # the stricter line wins; in any-severity mode the T09 line is not cross-checked
        # (no DISAGREE), but a FAIL is still never turned into a PASS
        fail = True
    out.append(f"verdict: {'FAIL' if fail else 'PASS'}")
    (d / "final-verdict.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))
    return 2 if (unparseable or disagree) else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="fix_audit.py", description=__doc__.splitlines()[0]
    )
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser(
        "prepare", help="split the cycle-2 fix diff into classified hunks"
    )
    p.add_argument("--baseline", required=True)
    p.add_argument("--current", required=True)
    p.add_argument("--report", required=True)
    p.add_argument("--dispositions")
    p.add_argument("--out", required=True)
    p.set_defaults(fn=cmd_prepare)
    c = sub.add_parser(
        "check", help="check audit.md against K1-K10; never writes the spec"
    )
    c.add_argument("--dir", required=True)
    c.set_defaults(fn=cmd_check)
    ap_ = sub.add_parser(
        "apply", help="re-check, then apply revert and edit rows all or nothing"
    )
    ap_.add_argument("--dir", required=True)
    ap_.set_defaults(fn=cmd_apply)
    v = sub.add_parser(
        "verdict", help="compute the review-3 verdict and the owner count"
    )
    v.add_argument("--dir", required=True)
    v.add_argument("--report", required=True)
    v.add_argument("--report-rule", choices=("427", "any-severity"), default="427")
    v.set_defaults(fn=cmd_verdict)
    a = ap.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
