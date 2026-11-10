"""E2 passage extraction (shared machinery, identical for every router).

extract(doc_text) -> list[Passage].  Deterministic, pure.  Passage.text is an exact substring of the document (multi-line
passages are the original lines joined with "\\n").  Occurrence-specific ids (P0012) are assigned in emission order, so they
are stable for identical input.  No model, no network.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

STOP_IDS = {"UTF-8", "SHA-256", "ISO-8601", "HTTP-2", "TLS-1", "X-1"}
ID_RE = re.compile(r"(?<![\w`/.\-])((?:[A-Z]{1,5}-[A-Z]?\d+(?:\.\d+)*|[A-Z]{1,2}\d{1,3}))(?![\w\-])")
START_ID_RE = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)?\**\s*(?:\|\s*)?\**\s*([A-Z]{1,5}-[A-Z]?\d+(?:\.\d+)*|[A-Z]{1,2}\d{1,3})(?![\w\-])")
SECTION_REF_RE = re.compile(r"(?i)(?:\bsections?\b|§)\s*(\d+(?:\.\d+)*)((?:\s*(?:,|and|-|–|to)\s*\d+(?:\.\d+)*)*)")
BARE_NUM_RE = re.compile(r"(?<![\w.\-])(\d+\.\d+)(?!\w)(?!\.\d)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
HEAD_NUM_RE = re.compile(r"^(\d+(?:\.\d+)*)\.?\s+(.*)$")
TABLE_RE = re.compile(r"^\s*\|")
SEP_RE = re.compile(r"^\s*\|[\s:\-|]+\|?\s*$")
LIST_RE = re.compile(r"^(\s*)(?:[-*+]|\d+[.)])\s+")
FENCE_RE = re.compile(r"^\s*```")
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
EXT = r"(?:md|yaml|yml|json|jsonl|toml|py|sh|txt|cfg|ini|csv|log|conf)"
PATH_BARE_RE = re.compile(r"(?<![\w/.\-])((?:[\w.<>*\-]+/)*[\w\-]+\." + EXT + r")(?![\w])")
UNIT_RE = re.compile(
    r"(?<![\w.])(\d+(?:[.,]\d+)?)\s*(ms|milliseconds?|s|sec|seconds?|minutes?|min|hours?|h|days?|weeks?|months?|years?|"
    r"KB|MB|GB|TB|KiB|MiB|GiB|Mbit|kbit|%|percent|requests?|retries|bytes?|characters?|ticks?)(?![\w])", re.I)
UNIT_NORM = {"milliseconds": "ms", "millisecond": "ms", "sec": "s", "second": "s", "seconds": "s", "minute": "min", "minutes": "min",
             "hour": "h", "hours": "h", "day": "day", "days": "day", "week": "week", "weeks": "week", "month": "month", "months": "month",
             "year": "year", "years": "year", "percent": "%", "request": "request", "requests": "request", "byte": "byte",
             "bytes": "byte", "character": "char", "characters": "char", "tick": "tick", "ticks": "tick"}


@dataclass
class Passage:
    pid: str
    section_no: str
    section_title: str
    section_ord: int
    line_start: int
    line_end: int
    kind: str                      # heading | paragraph | list_item | table_row
    text: str
    ids_defined: tuple = ()
    ids_referenced: tuple = ()
    section_refs: tuple = ()
    paths: tuple = ()              # basenames of path-like tokens
    numbers_with_units: tuple = ()
    terms: tuple = ()              # backticked terms (lower-case)
    context: str = ""              # table rows: the header row
    is_header: bool = False        # table header row (never a candidate)


def _ids(text: str) -> list:
    out = []
    for m in ID_RE.finditer(text):
        t = m.group(1)
        if t in STOP_IDS or t in out:
            continue
        out.append(t)
    return out


def _first_cell(text: str) -> str:
    parts = text.strip().strip("|").split("|", 1)
    return parts[0] if parts else ""


BARE_CELL_RE = re.compile(r"^[\s*`]*([A-Z]{1,5}-[A-Z]?\d+(?:\.\d+)*|[A-Z]{1,2}\d{1,3})[\s*`]*$")


def _row_defined(text: str) -> list:
    """Ids a table row defines: those in its first cell, unless the first cell is a bare id and the second cell is one too
    (a Phase | ID | ... table), in which case the second cell's id is the one defined."""
    cells = [c for c in text.strip().strip("|").split("|")[:2]]
    if len(cells) == 2 and BARE_CELL_RE.match(cells[0]) and BARE_CELL_RE.match(cells[1]):
        return _ids(cells[1])
    return _ids(cells[0]) if cells else []


SIZE_CANON = {"kb": "KB", "mb": "MB", "gb": "GB", "tb": "TB", "kib": "KiB", "mib": "MiB", "gib": "GiB", "mbit": "Mbit", "kbit": "kbit"}


def _norm_unit(u: str) -> str:
    ul = u.lower()
    return SIZE_CANON.get(ul) or UNIT_NORM.get(ul, ul)


def _paths(text: str) -> list:
    cands = []
    for span in BACKTICK_RE.findall(text):
        s = span.strip()
        if "/" in s and " " not in s:
            cands.append(s)
        elif re.fullmatch(r"[\w.<>*\-]+\." + EXT, s):
            cands.append(s)
    cands += [m.group(1) for m in PATH_BARE_RE.finditer(text)]
    out = []
    for c in cands:
        c = re.sub(r":[\d,\-]+$", "", c).rstrip("/")
        base = c.rsplit("/", 1)[-1]
        base = re.sub(r":[\d,\-]+$", "", base)
        if base and re.search(r"[A-Za-z]", base) and base not in out:
            out.append(base.lower())
    return out


def _numunits(text: str) -> list:
    out = []
    for m in UNIT_RE.finditer(text):
        num = m.group(1).replace(",", "")
        key = f"{num} {_norm_unit(m.group(2))}"
        if key not in out:
            out.append(key)
    return out


def _section_refs(text: str) -> list:
    out = []
    for m in SECTION_REF_RE.finditer(text):
        nums = [m.group(1)] + re.findall(r"\d+(?:\.\d+)*", m.group(2) or "")
        for n in nums:
            if n not in out:
                out.append(n)
    return out


def extract(doc_text: str) -> list:
    lines = doc_text.split("\n")
    raw = []          # (kind, l1, l2, text, context, is_header, section_no, section_title, section_ord)
    sec_no, sec_title, sec_ord = "", "", 0
    para = None       # [l1, l2, [lines]]
    item = None
    in_fence = None
    table_ctx = None  # header row of the current table block
    i = 0
    n = len(lines)

    def flush_para():
        nonlocal para
        if para:
            raw.append(("paragraph", para[0], para[1], "\n".join(para[2]), "", False, sec_no, sec_title, sec_ord))
        para = None

    def flush_item():
        nonlocal item
        if item:
            raw.append(("list_item", item[0], item[1], "\n".join(item[2]), "", False, sec_no, sec_title, sec_ord))
        item = None

    while i < n:
        ln = lines[i]
        ls = i + 1
        if in_fence is not None:
            in_fence[2].append(ln)
            in_fence[1] = ls
            if FENCE_RE.match(ln):
                raw.append(("paragraph", in_fence[0], in_fence[1], "\n".join(in_fence[2]), "", False, sec_no, sec_title, sec_ord))
                in_fence = None
            i += 1
            continue
        if not ln.strip():
            flush_para(); flush_item(); table_ctx = None
            i += 1
            continue
        if FENCE_RE.match(ln):
            flush_para(); flush_item(); table_ctx = None
            in_fence = [ls, ls, [ln]]
            i += 1
            continue
        hm = HEADING_RE.match(ln)
        if hm:
            flush_para(); flush_item(); table_ctx = None
            title = hm.group(2)
            nm = HEAD_NUM_RE.match(title)
            sec_ord += 1
            if nm:
                sec_no, sec_title = nm.group(1), nm.group(2).strip()
            else:
                sec_no, sec_title = "", title.strip()
            raw.append(("heading", ls, ls, ln, "", False, sec_no, sec_title, sec_ord))
            i += 1
            continue
        if TABLE_RE.match(ln):
            flush_para(); flush_item()
            if SEP_RE.match(ln):
                i += 1
                continue
            is_head = table_ctx is None and i + 1 < n and bool(SEP_RE.match(lines[i + 1]))
            if is_head:
                table_ctx = ln
                raw.append(("table_row", ls, ls, ln, "", True, sec_no, sec_title, sec_ord))
            else:
                raw.append(("table_row", ls, ls, ln, table_ctx or "", False, sec_no, sec_title, sec_ord))
            i += 1
            continue
        lm = LIST_RE.match(ln)
        if lm:
            flush_para(); flush_item(); table_ctx = None
            item = [ls, ls, [ln]]
            i += 1
            continue
        if item and ln[:1] in (" ", "\t"):
            item[1] = ls; item[2].append(ln)
            i += 1
            continue
        flush_item(); table_ctx = None
        if para:
            para[1] = ls; para[2].append(ln)
        else:
            para = [ls, ls, [ln]]
        i += 1
    flush_para(); flush_item()
    if in_fence is not None:
        raw.append(("paragraph", in_fence[0], in_fence[1], "\n".join(in_fence[2]), "", False, sec_no, sec_title, sec_ord))

    section_nos = {r[6] for r in raw if r[6]}
    out = []
    for idx, (kind, l1, l2, text, ctx, is_head, sno, stitle, sord) in enumerate(raw):
        pid = f"P{idx + 1:04d}"
        all_ids = _ids(text)
        if kind == "table_row":
            defined = _row_defined(text)
        elif kind == "heading":
            defined = list(all_ids)
        else:
            sm = START_ID_RE.match(text)
            defined = [sm.group(1)] if sm and sm.group(1) not in STOP_IDS else []
        refs = [t for t in all_ids if t not in defined]
        sref = _section_refs(text)
        for m in BARE_NUM_RE.finditer(text):
            if m.group(1) in section_nos and m.group(1) not in sref:
                sref.append(m.group(1))
        sref = [x for x in sref if x != sno]
        terms = []
        for span in BACKTICK_RE.findall(text):
            t = span.strip().lower()
            if len(t) >= 2 and not re.fullmatch(r"[\d.,\-]+", t) and t not in terms:
                terms.append(t)
        out.append(Passage(pid=pid, section_no=sno, section_title=stitle, section_ord=sord, line_start=l1, line_end=l2, kind=kind,
                           text=text, ids_defined=tuple(defined), ids_referenced=tuple(refs), section_refs=tuple(sref),
                           paths=tuple(_paths(text)), numbers_with_units=tuple(_numunits(text)), terms=tuple(terms),
                           context=ctx, is_header=is_head))
    return out


def find_quote(passages, quote: str) -> list:
    """Passages whose text contains `quote` exactly (used to resolve authored evidence quotes to pids)."""
    return [p for p in passages if quote in p.text]
