"""Deterministic requirements lint for markdown specs (``review-lint/1``).

Stdlib only, pure functions: text in, a result dict out. Every check reports a
mechanical inconsistency as evidence for a reviewer; nothing here decides a
verdict. The same input always gives byte-identical output.

Checks
------
REF    dangling reference (id or section/step referenced but never defined)
COUNT  count mismatch (heading count vs table rows, parts that do not sum, "all N" vs a list)
KV     conflicting value (same key or same quantity with different values in different sections)
PHASE  phase order (an acceptance row of phase Pk needs something introduced after Pk)
PATH   path template (same basename, path does not fit the template)
RFC    MUST/SHALL/SHOULD/MAY census per section (information only, never a finding)
"""

from __future__ import annotations

import fnmatch
import hashlib
import json
import re
from dataclasses import dataclass, field

SCHEMA = "review-lint/1"
CHECKS = ("REF", "COUNT", "KV", "PHASE", "PATH", "RFC")
MAX_QUOTE = 200

ID_RE = re.compile(r"\b(?:[A-Z]{1,4}-[0-9]+(?:\.[0-9]+)*|P[0-9])\b")
# Lint-specific token: the whole compound id (FR-L-16, T-ISO-9), never a fragment of one.
REF_ID_RE = re.compile(r"(?<![\w-])(?:[A-Z]{1,4}-)+[0-9]+(?:\.[0-9]+)*(?![\w-])|(?<![\w-])P[0-9](?![\w-])")
_ID_HEADERS = frozenset({"id", "ids", "ref", "requirement id", "check id", "#"})
_BOLD_SPAN_RE = re.compile(r"\*\*([^*]+?)\*\*")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
_NUMBER_RE = re.compile(r"^(\d+(?:\.\d+)*)")
_FENCE_RE = re.compile(r"^\s*(```|~~~)")
_SEP_RE = re.compile(r"^\|[\s:|\-]*-{3,}[\s:|\-]*$")
_LIST_RE = re.compile(r"^(\s*)(?:[-*+]|\d+[.)])\s+")
_BOLD_START_RE = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)?\*\*([^*]+?)\*\*")
_CODE_SPAN_RE = re.compile(r"`([^`\n]+)`")
_RFC_RE = re.compile(r"\b(MUST|SHALL|SHOULD|MAY)\b")
_SECTION_REF_RE = re.compile(
    r"(?:\b[Ss]ections?\s+|§\s*)(\d+(?:\.\d+)*)(?![\d]|\.\d)"
    r"((?:\s*(?:,|and|&)\s*\d+(?:\.\d+)*(?![\d]|\.\d))*)"
)
_STEP_REF_RE = re.compile(r"(?<![\w.\-])(\d+\.\d+|(?<=[Ss]ection )\d+)\s+step\s+(\d+)\b")
_PHASE_CELL_RE = re.compile(r"^\W*P(\d)\b")
_AC_RE = re.compile(r"\b[A-Z]{1,4}-(\d+)\.\d+\b")


@dataclass
class Heading:
    line: int
    level: int
    number: str | None
    title: str
    section: str = ""


@dataclass
class Table:
    start: int
    end: int
    header: list[str]
    rows: list[tuple[int, list[str]]]


@dataclass
class Doc:
    lines: list[str]
    code: list[bool]
    headings: list[Heading] = field(default_factory=list)
    tables: list[Table] = field(default_factory=list)
    sections: list[str] = field(default_factory=list)

    def text(self, n: int) -> str:
        return self.lines[n - 1]

    def section(self, n: int) -> str:
        return self.sections[n - 1]


def _slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def _split_cells(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    cells: list[str] = []
    cur: list[str] = []
    in_code = False
    i = 0
    while i < len(body):
        ch = body[i]
        if ch == "\\" and i + 1 < len(body) and body[i + 1] == "|":
            cur.append("|")
            i += 2
            continue
        if ch == "`":
            in_code = not in_code
        if ch == "|" and not in_code:
            cells.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
        i += 1
    cells.append("".join(cur).strip())
    return cells


def parse(text: str) -> Doc:
    lines = [ln.rstrip("\r") for ln in text.split("\n")]
    code = [False] * len(lines)
    fence: str | None = None
    for i, ln in enumerate(lines):
        m = _FENCE_RE.match(ln)
        if fence is None:
            if m:
                fence = m.group(1)
                code[i] = True
        else:
            code[i] = True
            if m and m.group(1) == fence:
                fence = None
    doc = Doc(lines=lines, code=code)
    for i, ln in enumerate(lines):
        if code[i]:
            continue
        m = _HEADING_RE.match(ln)
        if m:
            title = m.group(2)
            num = _NUMBER_RE.match(title)
            number = num.group(1) if num else None
            sect = number if number else _slug(title)
            doc.headings.append(Heading(i + 1, len(m.group(1)), number, title, sect))
    # section_of per line
    cur = "top"
    hi = 0
    for i in range(len(lines)):
        while hi < len(doc.headings) and doc.headings[hi].line <= i + 1:
            cur = doc.headings[hi].section
            hi += 1
        doc.sections.append(cur)
    # tables
    i = 0
    n = len(lines)
    while i < n:
        if not code[i] and lines[i].lstrip().startswith("|"):
            j = i
            while j < n and not code[j] and lines[j].lstrip().startswith("|"):
                j += 1
            block = list(range(i, j))
            sep = next((k for k in block if _SEP_RE.match(lines[k].strip())), None)
            if sep is not None and sep >= 1 and sep - 1 >= block[0]:
                header = _split_cells(lines[sep - 1])
                rows = [(k + 1, _split_cells(lines[k])) for k in block if k > sep]
                # start = 1-based line of the header row, end = 1-based line of the last row
                doc.tables.append(Table(sep, j, header, rows))
            i = j
        else:
            i += 1
    return doc


def _flat(s: str) -> str:
    return " ".join(s.split())


def _clip(s: str) -> str:
    s = _flat(s)
    return s if len(s) <= MAX_QUOTE else s[: MAX_QUOTE - 3] + "..."


def _clean_cell(cell: str) -> str:
    return cell.replace("**", "").replace("`", "").strip()


def _noncode_lines(doc: Doc):
    for i, ln in enumerate(doc.lines):
        if not doc.code[i]:
            yield i + 1, ln


def _heading_at(doc: Doc, line: int) -> Heading | None:
    for h in doc.headings:
        if h.line == line:
            return h
    return None


# --- definitions -------------------------------------------------------------


def _definitions(doc: Doc) -> tuple[dict[str, int], dict[str, list[tuple[str, int]]]]:
    """Return (id -> first defining line, section number -> [(id, line)] for ids defined in it).

    Defined = an id in the first cell of a table row or in a column headed ID/Ref; an id that
    starts a bold span (anywhere in a line) or is listed in a bold span at a line start; an id
    in a heading.
    """
    defined: dict[str, int] = {}
    by_section: dict[str, list[tuple[str, int]]] = {}

    def add(token: str, line: int) -> None:
        defined.setdefault(token, line)
        by_section.setdefault(doc.section(line), []).append((token, line))

    for table in doc.tables:
        cols = {0} | {i for i, h in enumerate(table.header) if _clean_cell(h).lower() in _ID_HEADERS}
        for line, cells in table.rows:
            for col in cols:
                if col < len(cells):
                    for tok in REF_ID_RE.findall(_clean_cell(cells[col])):
                        add(tok, line)
    for line, text in _noncode_lines(doc):
        for bm in _BOLD_SPAN_RE.finditer(text):
            inner = bm.group(1)
            at_start = bool(re.match(r"^\s*(?:\||[-*+]\s+|\d+[.)]\s+)?\s*$", text[: bm.start()]))
            if at_start and not text.lstrip().startswith("|"):
                toks = REF_ID_RE.findall(inner)
            else:
                first = REF_ID_RE.match(inner.lstrip(" (`"))
                toks = [first.group(0)] if first else []
            for tok in toks:
                add(tok, line)
        h = _heading_at(doc, line)
        if h:
            for tok in REF_ID_RE.findall(h.title):
                add(tok, line)
    return defined, by_section


def _heading_numbers(doc: Doc) -> dict[str, Heading]:
    out: dict[str, Heading] = {}
    for h in doc.headings:
        if h.number:
            out.setdefault(h.number, h)
    return out


def _section_body_items(doc: Doc, h: Heading) -> set[int]:
    """Numbers of the numbered list items directly in the section body of heading ``h``."""
    items: set[int] = set()
    for line, text in _noncode_lines(doc):
        if line <= h.line:
            continue
        hh = _heading_at(doc, line)
        if hh is not None and hh.level <= h.level:
            break
        m = re.match(r"^\s*(\d+)[.)]\s", text)
        if m:
            items.add(int(m.group(1)))
    return items


def _section_refs(text: str) -> list[tuple[str, str]]:
    """Return (kind, value) for section / step references on one line."""
    refs: list[tuple[str, str]] = []
    for m in _SECTION_REF_RE.finditer(text):
        refs.append(("section", m.group(1)))
        for extra in re.findall(r"\d+(?:\.\d+)*", m.group(2) or ""):
            refs.append(("section", extra))
    for m in _STEP_REF_RE.finditer(text):
        refs.append(("step", f"{m.group(1)}|{m.group(2)}"))
    return refs


# --- result helper -----------------------------------------------------------


def _finding(
    check: str,
    cls: str,
    lines: tuple[int, int],
    quote: str,
    message: str,
    other: tuple[int, int] | None = None,
) -> dict:
    return {
        "lint_id": "",
        "check": check,
        "class": cls,
        "lines": [lines[0], lines[1]],
        "quote": _clip(quote),
        "other_lines": [other[0], other[1]] if other else None,
        "message": message,
    }


# --- REF ---------------------------------------------------------------------


def check_ref(doc: Doc) -> list[dict]:
    defined, _ = _definitions(doc)
    numbers = _heading_numbers(doc)
    def_lines = set(defined.values())
    out: list[dict] = []
    seen_ids: dict[str, list[int]] = {}
    seen_sections: dict[str, list[int]] = {}
    for line, text in _noncode_lines(doc):
        h = _heading_at(doc, line)
        scan = text
        for m in REF_ID_RE.finditer(scan):
            tok = m.group(0)
            if tok.startswith("SHA-"):
                continue
            if tok in defined:
                continue
            if line in def_lines and tok in defined:
                continue
            seen_ids.setdefault(tok, []).append(line)
        for kind, value in _section_refs(text):
            if kind == "section":
                if value not in numbers:
                    seen_sections.setdefault(value, []).append(line)
            else:
                sec, step = value.split("|")
                if sec not in numbers:
                    seen_sections.setdefault(sec, []).append(line)
                elif int(step) not in _section_body_items(doc, numbers[sec]):
                    out.append(
                        _finding(
                            "REF",
                            "fact",
                            (line, line),
                            text,
                            f"Step {step} of section {sec} is referenced but section {sec} has no numbered item {step}.",
                            (numbers[sec].line, numbers[sec].line),
                        )
                    )
        del h
    for tok, occ in seen_ids.items():
        extra = f" ({len(occ)} references)" if len(occ) > 1 else ""
        out.append(
            _finding(
                "REF",
                "fact",
                (occ[0], occ[0]),
                doc.text(occ[0]),
                f"{tok} is referenced but never defined{extra}.",
            )
        )
    for sec, occ in seen_sections.items():
        extra = f" ({len(occ)} references)" if len(occ) > 1 else ""
        out.append(
            _finding(
                "REF",
                "fact",
                (occ[0], occ[0]),
                doc.text(occ[0]),
                f"Section {sec} is referenced but no heading has that number{extra}.",
            )
        )
    return out


# --- COUNT -------------------------------------------------------------------

_PAREN_COUNT_RE = re.compile(r"\(\s*(\d+\s+in\s[^()]*)\)")
_ALL_N_RE = re.compile(r"\b(?:all|the|All|The)\s+(\d+)\s+([A-Za-z][\w-]*)")


def _blank_code(text: str) -> str:
    return _CODE_SPAN_RE.sub("X", text)


def _last_number(text: str) -> int | None:
    found = None
    for m in re.finditer(r"(?<![\w.\-])(\d+)(?![\w]|\.\d)", text):
        found = int(m.group(1))
    return found


def _list_count(doc: Doc, start: int) -> int:
    """Count top-level list items of the list starting at 1-based line ``start``."""
    m = _LIST_RE.match(doc.text(start))
    assert m
    base = len(m.group(1))
    count = 0
    i = start
    n = len(doc.lines)
    while i <= n:
        if doc.code[i - 1]:
            break
        ln = doc.text(i)
        if not ln.strip():
            j = i + 1
            while j <= n and not doc.text(j).strip():
                j += 1
            if j > n:
                break
            nxt = doc.text(j)
            lm = _LIST_RE.match(nxt)
            if (lm and len(lm.group(1)) >= base) or (len(nxt) - len(nxt.lstrip()) > base):
                i = j
                continue
            break
        lm = _LIST_RE.match(ln)
        indent = len(ln) - len(ln.lstrip())
        if lm and len(lm.group(1)) == base:
            count += 1
        elif lm and len(lm.group(1)) > base:
            pass
        elif indent > base:
            pass
        else:
            break
        i += 1
    return count


def check_count(doc: Doc) -> list[dict]:
    out: list[dict] = []
    # (a) heading (N) versus the first table below it
    for idx, h in enumerate(doc.headings):
        m = re.search(r"\((\d+)\)\s*$", h.title)
        if not m:
            continue
        stop = doc.headings[idx + 1].line if idx + 1 < len(doc.headings) else len(doc.lines) + 1
        table = next((t for t in doc.tables if h.line < t.start < stop), None)
        if table is None:
            continue
        want = int(m.group(1))
        got = len(table.rows)
        if want != got:
            out.append(
                _finding(
                    "COUNT",
                    "fact",
                    (h.line, h.line),
                    doc.text(h.line),
                    f"The heading says ({want}) but the table below has {got} data rows.",
                    (table.start, table.end),
                )
            )
    # (b) parts that do not sum
    for line, text in _noncode_lines(doc):
        if text.lstrip().startswith(("|", "#")):
            continue
        plain = _blank_code(text)
        for pm in _PAREN_COUNT_RE.finditer(plain):
            parts = [int(x) for x in re.findall(r"(\d+)\s+in\s", pm.group(1))]
            if len(parts) < 2:
                continue
            before = plain[: pm.start()]
            total = _last_number(before)
            if total is None or len(before.split()) - len(before[: before.rfind(str(total))].split()) > 8:
                continue
            if total != sum(parts):
                out.append(
                    _finding(
                        "COUNT",
                        "fact",
                        (line, line),
                        text,
                        f"{total} is split as {' + '.join(map(str, parts))} = {sum(parts)}.",
                    )
                )
        sm = re.search(r"\bsplits?\s+into\s+(.*)", plain)
        if sm:
            before = re.sub(r"\([^()]*\)", " ", plain[: sm.start()])
            total = _last_number(before)
            clause = re.sub(r"\([^()]*\)", " ", re.split(r"[.;]\s|[.;]$", sm.group(1))[0])
            pieces = [p.strip() for p in re.split(r",\s*(?:and\s+)?|\s+and\s+", clause) if p.strip()]
            nums = [int(m2.group(1)) for p in pieces if (m2 := re.match(r"(\d+)\s", p))]
            if total is not None and len(nums) >= 2 and len(nums) == len(pieces) and total != sum(nums):
                out.append(
                    _finding(
                        "COUNT",
                        "fact",
                        (line, line),
                        text,
                        f"{total} is split into {' + '.join(map(str, nums))} = {sum(nums)}.",
                    )
                )
    # (c) "all N" / "the N <noun>" next to a list or table
    n = len(doc.lines)
    for line, text in _noncode_lines(doc):
        if text.lstrip().startswith(("|", "#")):
            continue
        m = _ALL_N_RE.search(_blank_code(text))
        if not m or _LIST_RE.match(text) or not text.rstrip().endswith(":"):
            continue
        want = int(m.group(1))
        j = line + 1
        while j <= n and not doc.text(j).strip() and j <= line + 2:
            j += 1
        if j > n or doc.code[j - 1]:
            continue
        nxt = doc.text(j)
        if _LIST_RE.match(nxt):
            got = _list_count(doc, j)
            span = (j, j)
        elif nxt.lstrip().startswith("|"):
            table = next((t for t in doc.tables if t.start <= j <= t.end), None)
            if table is None:
                continue
            got = len(table.rows)
            span = (table.start, table.end)
        else:
            continue
        if got != want:
            out.append(
                _finding(
                    "COUNT",
                    "fact",
                    (line, line),
                    text,
                    f'The text says "{m.group(0)}" but the {"table" if nxt.lstrip().startswith("|") else "list"} next to it has {got} items.',
                    span,
                )
            )
    return out


# --- KV ----------------------------------------------------------------------

_KEY_EQ_RE = re.compile(r"`([A-Za-z_][\w.\-]*)`\s*=\s*(`[^`]+`|[^\s,;)]+)")
_KEY_COLON_RE = re.compile(r"`([A-Za-z_][\w.\-]*)`\s*:\s+(`[^`]+`|[^\s,;)]+)")
_UNIT_RE = re.compile(
    r"(?<![\w.\-])(\d+(?:\.\d+)?)[\s-]*(times?|attempts?|retry|retries|seconds?|secs?|minutes?|mins?|hours?|hrs?|days?|KiB|MB)\b"
)
_STOP = frozenset(
    "a an the at most least up to of for is are be by in on after within every each than more less about over "
    "under only and or not no per has have with that it its this these those as if then once twice into".split()
)
_UNIT_NORM = {
    "time": "times", "times": "times", "attempt": "attempts", "attempts": "attempts",
    "retry": "retries", "retries": "retries", "second": "seconds", "seconds": "seconds",
    "sec": "seconds", "secs": "seconds", "minute": "minutes", "minutes": "minutes",
    "min": "minutes", "mins": "minutes", "hour": "hours", "hours": "hours", "hr": "hours",
    "hrs": "hours", "day": "days", "days": "days", "kib": "KiB", "mb": "MB",
}  # fmt: skip
HEAD_WORDS = 6
STEM_LEN = 4
MIN_SHARED = 2
_GENERIC_STEMS = frozenset({"call", "wait", "abov", "belo", "time", "tota", "seco", "minu", "hour", "days", "atte"})


def _norm_value(v: str) -> str:
    return v.replace("`", "").replace("*", "").strip().rstrip(".").lower()


def check_kv(doc: Doc) -> list[dict]:
    out: list[dict] = []
    # key bindings: inline `key` = v and `key`: v only (table cells hold column semantics, not bindings)
    bindings: dict[str, list[tuple[int, str, str]]] = {}
    table_lines = {ln for t in doc.tables for ln, _ in t.rows}
    for line, text in _noncode_lines(doc):
        if line in table_lines:
            continue
        for rx in (_KEY_EQ_RE, _KEY_COLON_RE):
            for m in rx.finditer(text):
                bindings.setdefault(m.group(1), []).append((line, _norm_value(m.group(2)), m.group(2)))
    for key, occ in bindings.items():
        occ.sort()
        first_by_section: list[tuple[int, str, str]] = []
        for line, val, raw in occ:
            clash = next(
                (o for o in first_by_section if o[1] != val and doc.section(o[0]) != doc.section(line)),
                None,
            )
            if clash:
                out.append(
                    _finding(
                        "KV",
                        "possible",
                        (line, line),
                        doc.text(line),
                        f"`{key}` is bound to {_clip(raw)} here (section {doc.section(line)}) and to {_clip(clash[2])} "
                        f"at line {clash[0]} (section {doc.section(clash[0])}).",
                        (clash[0], clash[0]),
                    )
                )
            else:
                first_by_section.append((line, val, raw))
    # quantities: same unit, at least MIN_SHARED head-word stems in common, different numbers, different sections
    quantities: list[tuple[int, float, str, set[str], str]] = []
    heading_lines = {h.line for h in doc.headings}
    table_header_lines = {t.start for t in doc.tables}
    for line, text in _noncode_lines(doc):
        if line in heading_lines or line in table_header_lines:
            continue
        for m in _UNIT_RE.finditer(text):
            words = re.findall(r"[A-Za-z]+", text[: m.start()])[-HEAD_WORDS:]
            stems = {w.lower()[:STEM_LEN] for w in words if w.lower() not in _STOP and len(w) > 2} - _GENERIC_STEMS
            unit = _UNIT_NORM[m.group(2).lower()]
            quantities.append((line, float(m.group(1)), unit, stems, m.group(0)))
    reported: set[tuple[int, str]] = set()
    kept: list[tuple[int, float, str, set[str], str]] = []
    for q in quantities:
        clash = next(
            (
                k
                for k in kept
                if k[2] == q[2]
                and k[1] != q[1]
                and len(k[3] & q[3]) >= MIN_SHARED
                and doc.section(k[0]) != doc.section(q[0])
            ),
            None,
        )
        if clash and (q[0], q[2]) not in reported:
            reported.add((q[0], q[2]))
            shared = ", ".join(sorted(clash[3] & q[3]))
            out.append(
                _finding(
                    "KV",
                    "possible",
                    (q[0], q[0]),
                    doc.text(q[0]),
                    f'"{q[4]}" here (section {doc.section(q[0])}) and "{clash[4]}" at line {clash[0]} '
                    f"(section {doc.section(clash[0])}) share the head words {shared}.",
                    (clash[0], clash[0]),
                )
            )
        elif not clash:
            kept.append(q)
    return out


# --- PHASE -------------------------------------------------------------------


def _row_phase(cells: list[str]) -> int | None:
    if not cells:
        return None
    m = _PHASE_CELL_RE.match(cells[0])
    return int(m.group(1)) if m else None


def _rollout_table(doc: Doc) -> Table | None:
    best: Table | None = None
    for t in doc.tables:
        phases = [_row_phase(c) for _, c in t.rows]
        got = [p for p in phases if p is not None]
        if len(got) >= 2 and len(set(got)) == len(got):
            if best is None or len(got) > len([p for p in (_row_phase(c) for _, c in best.rows) if p is not None]):
                best = t
    return best


_DEFER_RE = re.compile(r"\b(?:no|not|until|before|since|interim|arrives?|yet|none)\b", re.I)
_BARE_SECTION_RE = re.compile(r"(?<![\w.\-])(\d+\.\d+)(?![\w]|\.\d)")


def _deferred(text: str, tok: str) -> bool:
    """True when every occurrence of ``tok`` in ``text`` sits near a negation or deferral word."""
    spots = [m.start() for m in re.finditer(re.escape(tok) + r"(?![\w-])", text)]
    if not spots:
        return False
    return all(_DEFER_RE.search(text[max(0, i - 60) : i + len(tok) + 60]) for i in spots)


def _section_ids(doc: Doc, step: str | None, heading: Heading) -> set[str]:
    """Ids mentioned in the section of ``heading`` (or only in its numbered item ``step``)."""
    out: set[str] = set()
    inside = step is None
    for line, text in _noncode_lines(doc):
        if line <= heading.line:
            continue
        hh = _heading_at(doc, line)
        if hh is not None and hh.level <= heading.level:
            break
        if step is not None:
            m = re.match(r"^\s*(\d+)[.)]\s", text)
            if m:
                inside = m.group(1) == step
        if inside:
            out.update(t for t in REF_ID_RE.findall(text) if not re.fullmatch(r"P\d", t))
    return out


def check_phase(doc: Doc) -> list[dict]:
    rollout = _rollout_table(doc)
    if rollout is None:
        return []
    first_phase: dict[str, tuple[int, int]] = {}
    for line, cells in rollout.rows:
        k = _row_phase(cells)
        if k is None:
            continue
        row_text = " ".join(cells)
        for tok in REF_ID_RE.findall(row_text):
            if re.fullmatch(r"P\d", tok):
                continue
            cur = first_phase.get(tok)
            if cur is None or k < cur[0]:
                first_phase[tok] = (k, line)
    numbers = _heading_numbers(doc)
    out: list[dict] = []
    for t in doc.tables:
        if t is rollout:
            continue
        for line, cells in t.rows:
            k = _row_phase(cells)
            if k is None:
                continue
            row_text = " ".join(cells)
            own = {m.group(0) for m in _AC_RE.finditer(row_text) if int(m.group(1)) == k}
            if not own:
                continue
            ac = sorted(own)[0]
            reported: set[str] = set()
            for tok in REF_ID_RE.findall(row_text):
                if tok in own or re.fullmatch(r"P\d", tok) or tok in reported:
                    continue
                fp = first_phase.get(tok)
                if fp and fp[0] > k and not _deferred(row_text, tok):
                    reported.add(tok)
                    out.append(
                        _finding(
                            "PHASE",
                            "fact",
                            (line, line),
                            doc.text(line),
                            f"The P{k} row ({ac}) uses {tok}, which the rollout table first introduces in P{fp[0]}.",
                            (fp[1], fp[1]),
                        )
                    )
            refs = [(kind, value.split("|")[0], (value.split("|") + [None])[1]) for kind, value in _section_refs(row_text)]
            refs += [("section", m.group(1), None) for m in _BARE_SECTION_RE.finditer(row_text)]
            seen_sec: set[str] = set()
            for _kind, sec, step in refs:
                if sec in seen_sec or sec not in numbers:
                    continue
                seen_sec.add(sec)
                later = sorted(
                    (tok, first_phase[tok])
                    for tok in _section_ids(doc, step, numbers[sec])
                    if tok in first_phase and first_phase[tok][0] > k and tok not in own and tok not in reported
                )
                if later:
                    reported.update(tok for tok, _ in later)
                    desc = ", ".join(f"{tok} (P{fp[0]})" for tok, fp in later)
                    out.append(
                        _finding(
                            "PHASE",
                            "fact",
                            (line, line),
                            doc.text(line),
                            f"The P{k} row ({ac}) refers to section {sec}"
                            + (f" step {step}" if step else "")
                            + f", which uses {desc}; the rollout table first introduces each in a later phase.",
                            (numbers[sec].line, numbers[sec].line),
                        )
                    )
    return out


# --- PATH --------------------------------------------------------------------

_PLACEHOLDER_RE = re.compile(r"<[^<>\s]+>")


def _spans(cell: str) -> list[str]:
    return [m.group(1).strip() for m in _CODE_SPAN_RE.finditer(cell)]


def _segment_match(span: str, template: str) -> bool:
    """fnmatch with the placeholder standing for exactly one path segment."""
    pattern = _PLACEHOLDER_RE.sub("*", template)
    return fnmatch.fnmatchcase(span.replace("<", "*").replace(">", ""), pattern) and span.count("/") == template.count("/")


def check_path(doc: Doc) -> list[dict]:
    # one family of templates per requirement row (a row may list several allowed places)
    families: list[tuple[int, str, list[str]]] = []  # (line, basename, templates)
    candidates: list[tuple[str, str, int]] = []
    for t in doc.tables:
        for line, cells in t.rows:
            is_req = bool(cells) and bool(REF_ID_RE.search(_clean_cell(cells[0])))
            row_templates: dict[str, list[str]] = {}
            for cell in cells:
                for span in _spans(cell):
                    base = span.rsplit("/", 1)[-1]
                    if not base or "<" in base or "*" in base or " " in span:
                        continue
                    if is_req and "/" in span and _PLACEHOLDER_RE.search(span):
                        row_templates.setdefault(base, []).append(span)
                    if "/" in span:
                        candidates.append((span, base, line))
            for base, spans in row_templates.items():
                if not any(f[1] == base for f in families):  # the first requirement row that defines a basename rules
                    families.append((line, base, spans))
    out: list[dict] = []
    seen: set[tuple[int, str, int]] = set()
    for tline, tbase, tspans in families:
        for span, base, line in candidates:
            if base != tbase or line == tline or (tline, span, line) in seen:
                continue
            if span in tspans or any(_segment_match(span, tp) for tp in tspans):
                continue
            seen.add((tline, span, line))
            shown = " or ".join(f"`{tp}`" for tp in tspans)
            out.append(
                _finding(
                    "PATH",
                    "possible",
                    (line, line),
                    doc.text(line),
                    f"`{span}` has the basename of the template {shown} (line {tline}) but fits none of them.",
                    (tline, tline),
                )
            )
    return out


# --- RFC ---------------------------------------------------------------------


def census_rfc(doc: Doc) -> tuple[dict, dict]:
    per: dict[str, dict[str, int]] = {}
    total = {"MUST": 0, "SHALL": 0, "SHOULD": 0, "MAY": 0}
    for line, text in _noncode_lines(doc):
        for m in _RFC_RE.finditer(text):
            sec = per.setdefault(doc.section(line), {"MUST": 0, "SHALL": 0, "SHOULD": 0, "MAY": 0})
            sec[m.group(1)] += 1
            total[m.group(1)] += 1
    return per, total


# --- driver ------------------------------------------------------------------

_CHECK_FUNCS = {
    "REF": check_ref,
    "COUNT": check_count,
    "KV": check_kv,
    "PHASE": check_phase,
    "PATH": check_path,
}


def parse_checks(spec: str | None) -> tuple[str, ...]:
    """Parse a comma list of check names (any case) into canonical order; None means all."""
    if spec is None or not spec.strip():
        return CHECKS
    wanted = {p.strip().upper() for p in spec.split(",") if p.strip()}
    unknown = sorted(wanted - set(CHECKS))
    if unknown:
        raise ValueError(f"unknown check(s): {', '.join(unknown)}; valid: {', '.join(CHECKS)}")
    return tuple(c for c in CHECKS if c in wanted)


def run_lint(data: bytes, checks: tuple[str, ...] | None = None) -> dict:
    checks = CHECKS if checks is None else tuple(c for c in CHECKS if c in checks)
    text = data.decode("utf-8", errors="replace")
    doc = parse(text)
    findings: list[dict] = []
    for name in checks:
        func = _CHECK_FUNCS.get(name)
        if func:
            findings.extend(func(doc))
    findings.sort(key=lambda f: (f["lines"][0], CHECKS.index(f["check"]), f["lines"][1], f["message"]))
    counters: dict[str, int] = {}
    for f in findings:
        counters[f["check"]] = counters.get(f["check"], 0) + 1
        f["lint_id"] = f"LINT-{f['check']}-{counters[f['check']]}"
    census: dict = {}
    if "RFC" in checks:
        per, total = census_rfc(doc)
        census = {"rfc2119": per, "rfc2119_total": total}
    return {
        "schema": SCHEMA,
        "doc_sha256": hashlib.sha256(data).hexdigest(),
        "doc_bytes": len(data),
        "checks": list(checks),
        "findings": findings,
        "census": census,
    }


def run_lint_text(text: str, checks: tuple[str, ...] | None = None) -> dict:
    return run_lint(text.encode("utf-8"), checks)


def render_json(result: dict) -> str:
    return json.dumps(result, indent=2, ensure_ascii=False) + "\n"


def _span_text(lines: list[int]) -> str:
    return str(lines[0]) if lines[0] == lines[1] else f"{lines[0]}-{lines[1]}"


def render_md(result: dict) -> str:
    out = [f"lint: superclaude review lint, {result['schema']}, sha256 {result['doc_sha256']}", ""]
    out.append(f"Checks: {', '.join(result['checks'])}. Findings: {len(result['findings'])}.")
    out.append("")
    for f in result["findings"]:
        out.append(f"### {f['lint_id']}")
        out.append("")
        out.append(f"- check: {f['check']} ({f['class']})")
        out.append(f"- lines: {_span_text(f['lines'])}")
        if f["other_lines"]:
            out.append(f"- other lines: {_span_text(f['other_lines'])}")
        out.append(f"- quote: {f['quote']}")
        out.append(f"- message: {f['message']}")
        out.append("")
    if not result["findings"]:
        out.append("No findings.")
        out.append("")
    census = result["census"].get("rfc2119")
    if census is not None:
        out.append("## Census")
        out.append("")
        out.append("| Section | MUST | SHALL | SHOULD | MAY |")
        out.append("|---|---|---|---|---|")
        for sec, c in census.items():
            out.append(f"| {sec} | {c['MUST']} | {c['SHALL']} | {c['SHOULD']} | {c['MAY']} |")
        t = result["census"]["rfc2119_total"]
        out.append(f"| total | {t['MUST']} | {t['SHALL']} | {t['SHOULD']} | {t['MAY']} |")
        out.append("")
    return "\n".join(out)
