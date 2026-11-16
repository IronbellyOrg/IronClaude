"""Plan reader (DESIGN section 3): a document becomes typed blocks.

    parse(data, fmt=None) -> Doc        data is bytes or str; fmt is a name in formats.FORMATS or a dictionary
    read(path, fmt=None) -> Doc         the same for a file

A block is a dict {kind, id, text, line_start, line_end, task, phase}. kind is one of KINDS. Lines are 1-based lines
of the document (CR before LF is ignored). `text` is cut from the document and never rebuilt: it is a contiguous
slice of the document's own lines (a list bullet loses only its marker), so `fnd.locate(doc.text, text)` finds it
and an anchor cut from it is an exact quote. `task` is the id of the enclosing task (`T1`) and `phase` the id of
the latest phase (`P1`), or None. An `edit_target` block also holds `path` (one block per path token of the
sentence) and `creates`.

The reader holds no format-specific text. Everything that tells one format from another is in formats.py, and a
new format needs a new dictionary there and no change here (REQ-37). It never fails on a document it does not
understand: unknown structure gives fewer blocks, down to none. It raises ReadError (a ValueError) on bytes that
are not text.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from sweep import formats, words

KINDS = ("task", "criterion", "constraint", "dictated_text", "edit_target", "gate")
_PREFIX = {
    "criterion": "C",
    "constraint": "K",
    "dictated_text": "D",
    "edit_target": "E",
    "gate": "G",
}
_BULLET = re.compile(r"^ ?(?:[-*+]|\d+[.)])[ \t]+")
_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
_HEADING = re.compile(r"^(#{1,6})[ \t]+(\S.*?)[ \t]*$")


class ReadError(ValueError):
    """The bytes are not a text document."""


@dataclass
class Doc:
    text: str
    format: str
    lines: list[str]
    blocks: list[dict]
    tasks: dict[str, dict]

    def of(self, *kinds: str) -> list[dict]:
        return [b for b in self.blocks if b["kind"] in kinds]


def decode(raw: bytes) -> str:
    """UTF-8 text (a leading byte order mark is dropped); anything else raises ReadError."""
    if b"\x00" in raw:
        raise ReadError("unreadable bytes: a NUL byte")
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError as e:
        raise ReadError(f"unreadable bytes: not UTF-8 ({e.reason})") from e


def read(path, fmt=None) -> Doc:
    """Read a file. A missing or unreadable file raises OSError; bytes that are not text raise ReadError."""
    return parse(Path(path).read_bytes(), fmt)


def parse(data, fmt=None) -> Doc:
    text = decode(data) if isinstance(data, bytes) else data
    if "\x00" in text:
        raise ReadError("unreadable bytes: a NUL byte")
    name, spec = _format(fmt)
    ctx = _Ctx(text, spec)
    _build_blocks(ctx)
    tasks = {
        t["id"]: {k: t[k] for k in ("id", "title", "line", "citations")}
        for t in ctx.task_list
    }
    return Doc(text, name, ctx.lines, ctx.blocks, tasks)


def _format(fmt):
    if isinstance(fmt, dict):
        return fmt.get("name", ""), fmt
    name = formats.DEFAULT if fmt is None else fmt
    try:
        return name, formats.FORMATS[name]
    except KeyError:
        raise ValueError(
            f"unknown format {name!r}; known: {sorted(formats.FORMATS)}"
        ) from None


# ---------------------------------------------------------------- word lists


def _wordlist(spec) -> tuple[str, ...]:
    """Words of a list name, a literal word, or a list of those."""
    if isinstance(spec, str):
        return tuple(words.LISTS[spec]) if spec in words.LISTS else (spec,)
    out: list[str] = []
    for item in spec:
        out.extend(_wordlist(item))
    return tuple(out)


@lru_cache(maxsize=None)
def _word_re(spec_key: tuple[str, ...]) -> re.Pattern:
    alts = sorted({w.lower() for w in spec_key}, key=lambda w: (-len(w), w))
    body = "|".join(re.escape(w).replace(r"\ ", r"\s+") for w in alts)
    return re.compile(rf"(?<![\w-])(?:{body})(?![\w-])", re.I)


def _wre(spec) -> re.Pattern:
    return _word_re(_wordlist(spec))


# ---------------------------------------------------------------- text helpers


def sentences(text: str) -> list[tuple[int, int, str]]:
    """(start, end, sentence) for each sentence of text; offsets index text and the sentence is text[start:end]."""
    cuts = [0] + [m.end() for m in re.finditer(formats.SENTENCE_END, text)]
    cuts.append(len(text))
    out = []
    for a, b in zip(cuts, cuts[1:]):
        seg = text[a:b]
        s = a + len(seg) - len(seg.lstrip())
        e = a + len(seg.rstrip())
        if e > s:
            out.append((s, e, text[s:e]))
    return out


# ---------------------------------------------------------------- document scan


class _Ctx:
    """The scanned document: lines, fences, headings, tasks and, per line, its task, phase and part."""

    def __init__(self, text: str, spec: dict):
        self.spec = spec
        self.text = text
        self.lines = [x.rstrip("\r") for x in text.split("\n")]
        self.n = len(self.lines)
        self.front = [False] * (self.n + 2)
        self.fence = [False] * (self.n + 2)
        self.head: list[dict | None] = [None] * (self.n + 2)
        self.fences: list[tuple[int, int, str]] = []
        self.out: dict[str, list[dict]] = {}
        self.blocks: list[dict] = []
        self.tasks: dict[str, dict] = {}
        self._scan()
        self._sections()
        self._contexts()

    def _scan(self) -> None:
        lines, n = self.lines, self.n
        if self.spec.get("front_matter") and n and lines[0].strip() == "---":
            for j in range(1, n):
                if lines[j].strip() == "---":
                    for k in range(1, j + 2):
                        self.front[k] = True
                    break
        opened = None  # (char, length, line, info)
        for i in range(1, n + 1):
            if self.front[i]:
                continue
            m = _FENCE.match(lines[i - 1])
            if opened is None:
                if m and not (m.group(1)[0] == "`" and "`" in m.group(2)):
                    opened = (m.group(1)[0], len(m.group(1)), i, m.group(2).strip())
                    self.fence[i] = True
            else:
                self.fence[i] = True
                if (
                    m
                    and m.group(1)[0] == opened[0]
                    and len(m.group(1)) >= opened[1]
                    and not m.group(2).strip()
                ):
                    self.fences.append((opened[2], i, opened[3]))
                    opened = None
        if opened is not None:
            self.fences.append((opened[2], n + 1, opened[3]))
        for i in range(1, n + 1):
            if self.front[i] or self.fence[i]:
                continue
            m = _HEADING.match(lines[i - 1])
            if m:
                self.head[i] = {
                    "line": i,
                    "level": len(m.group(1)),
                    "title": m.group(2),
                    "cls": None,
                    "groups": {},
                }

    def _sections(self) -> None:
        """Classify the headings, find where each section ends, and build the task list."""
        self.heads = [h for h in self.head if h]
        for h in self.heads:
            for cls, rx in self.spec.get("heads", {}).items():
                m = re.match(rx, self.lines[h["line"] - 1].rstrip(), re.I)
                if m:
                    h["cls"], h["groups"] = cls, m.groupdict()
                    break
        for k, h in enumerate(self.heads):
            h["end"] = self.n
            for g in self.heads[k + 1 :]:
                if g["level"] <= h["level"] or g["cls"]:
                    h["end"] = g["line"] - 1
                    break
        label = self.spec.get("label")
        self.task_list: list[dict] = []
        self.phases: list[tuple[int, str]] = []
        for k, h in enumerate(self.heads):
            if h["cls"] == "phase":
                self.phases.append(
                    (
                        h["line"],
                        _ident("P", h["groups"].get("id"), len(self.phases) + 1),
                    )
                )
            elif h["cls"] == "task":
                tid = _ident("T", h["groups"].get("id"), len(self.task_list) + 1)
                while tid in self.tasks:
                    tid += "_2"
                end = h["line"]
                for g in self.heads[k + 1 :]:
                    if g["level"] <= h["level"] or g["cls"] in ("task", "phase"):
                        end = g["line"] - 1
                        break
                else:
                    end = self.n
                t = {
                    "id": tid,
                    "title": (h["groups"].get("title") or h["title"]).strip(),
                    "line": h["line"],
                    "end": end,
                    "label": None,
                    "citations": [],
                }
                if label:
                    for i in range(h["line"] + 1, end + 1):
                        if not (self.front[i] or self.fence[i]) and re.match(
                            label, self.lines[i - 1].strip(), re.I
                        ):
                            t["label"] = i
                            break
                self.task_list.append(t)
                self.tasks[tid] = t

    def _contexts(self) -> None:
        n = self.n
        self.task_of: list[str | None] = [None] * (n + 2)
        self.part_of: list[str | None] = [None] * (n + 2)
        self.phase_of: list[str | None] = [None] * (n + 2)
        for t in self.task_list:
            for i in range(t["line"], t["end"] + 1):
                self.task_of[i] = t["id"]
                late = t["label"] is not None and i >= t["label"]
                self.part_of[i] = "criteria" if late else "body"
        cur = None
        marks = dict(self.phases)
        for i in range(1, n + 1):
            cur = marks.get(i, cur)
            self.phase_of[i] = cur
        for t in self.task_list:
            t["citations"] = _citations(self, t)


def _ident(prefix: str, value, seq: int) -> str:
    return f"{prefix}{value if value else seq}"


def _citations(ctx: _Ctx, t: dict) -> list[str]:
    spec = ctx.spec.get("citation")
    if not spec:
        return []
    stop = t["label"] or t["end"] + 1
    out: list[str] = []
    for i in range(t["line"] + 1, stop):
        if ctx.front[i] or ctx.fence[i]:
            continue
        m = re.match(spec["label"], ctx.lines[i - 1], re.I)
        if not m:
            continue
        cites = [m.group("cites")]
        for j in range(i + 1, stop):
            raw = ctx.lines[j - 1]
            if (
                not raw.strip()
                or ctx.head[j]
                or _BULLET.match(raw)
                or re.match(spec["label"], raw, re.I)
            ):
                break
            cites.append(raw)
        for c in re.finditer(spec["tokens"], " ".join(cites), re.I):
            if c.group("ref") not in out:
                out.append(c.group("ref"))
    return out


# ---------------------------------------------------------------- scope and shared pieces


def _in_scope(ctx: _Ctx, line: int, rule: dict) -> bool:
    if rule.get("in") == "task" and ctx.task_of[line] is None:
        return False
    return not (rule.get("part") and ctx.part_of[line] != rule["part"])


def _prose_ok(ctx: _Ctx, line: int, rule: dict) -> bool:
    return not (ctx.front[line] or ctx.fence[line] or ctx.head[line]) and _in_scope(
        ctx, line, rule
    )


def _trim(ctx: _Ctx, lo: int, hi: int):
    """(lo, hi) without blank lines at either end, or None when nothing is left."""
    while lo <= hi and not ctx.lines[lo - 1].strip():
        lo += 1
    while hi >= lo and not ctx.lines[hi - 1].strip():
        hi -= 1
    return (lo, hi) if lo <= hi else None


def _span_hit(ctx: _Ctx, lo: int, hi: int, **extra):
    t = _trim(ctx, lo, hi)
    if not t:
        return None
    return {
        "ls": t[0],
        "le": t[1],
        "text": "\n".join(ctx.lines[t[0] - 1 : t[1]]),
        **extra,
    }


def _bullets(ctx: _Ctx, lo: int, hi: int) -> list[dict]:
    """The top-level bullets of lines lo..hi; the lines that belong to a bullet are part of it."""
    out: list[dict] = []
    cur = None
    for i in range(lo, hi + 1):
        raw = ctx.lines[i - 1]
        if ctx.head[i]:
            break
        if ctx.fence[i]:
            if cur and raw[:1] in (" ", "\t"):
                cur["le"] = i
            else:
                cur = None
            continue
        if not raw.strip():
            continue
        m = _BULLET.match(raw)
        if m:
            cur = {"ls": i, "le": i, "cut": m.end()}
            out.append(cur)
        elif cur and (raw[:1] in (" ", "\t") or ctx.lines[i - 2].strip()):
            cur["le"] = i
        else:
            cur = None
    hits = []
    for b in out:
        rows = ctx.lines[b["ls"] - 1 : b["le"]]
        rows[0] = rows[0][b["cut"] :]
        hits.append({"ls": b["ls"], "le": b["le"], "text": "\n".join(rows).rstrip()})
    return hits


def _chunks(ctx: _Ctx, rule: dict) -> list[tuple[int, str]]:
    """(first line, raw text) of each run of prose lines: a blank line, a heading, a fence or a quote ends a run,
    a list bullet starts one (and loses its marker)."""
    chunks: list[list] = []
    cur = None
    for i in range(1, ctx.n + 1):
        raw = ctx.lines[i - 1]
        if (
            not _prose_ok(ctx, i, rule)
            or not raw.strip()
            or raw.lstrip().startswith(">")
        ):
            cur = None
            continue
        m = _BULLET.match(raw)
        if m or cur is None:
            cur = [i, [raw[m.end() :] if m else raw.lstrip()]]
            chunks.append(cur)
        else:
            cur[1].append(raw)
    return [(c[0], "\n".join(c[1])) for c in chunks]


def _sentence_hits(ctx: _Ctx, rule: dict):
    for first, raw in _chunks(ctx, rule):
        for s, e, sent in sentences(raw):
            yield {
                "ls": first + raw.count("\n", 0, s),
                "le": first + raw.count("\n", 0, e - 1),
                "text": sent,
                "_at": (first, raw, s),
            }


# ---------------------------------------------------------------- modes: each takes (ctx, rule) and gives hits


def _m_task_body(ctx, rule):
    for t in ctx.task_list:
        stop = t["label"] or t["end"] + 1
        h = _span_hit(ctx, t["line"] + 1, stop - 1, id=t["id"])
        if h:
            yield h


def _m_after_label(ctx, rule):
    label = rule.get("label") or ctx.spec.get("label")
    if not label:
        return
    for i in range(1, ctx.n + 1):
        if (
            ctx.front[i]
            or ctx.fence[i]
            or ctx.head[i]
            or not _in_scope(ctx, i, {"in": rule.get("in")})
            or not re.match(label, ctx.lines[i - 1].strip(), re.I)
        ):
            continue
        yield from _bullets(ctx, i + 1, ctx.n)


def _m_bullets(ctx, rule):
    for h in ctx.heads:
        if h["cls"] != rule["under"]:
            continue
        found = _bullets(ctx, h["line"] + 1, h["end"])
        if found:
            yield from found
        elif rule.get("fallback") == "section":
            yield from _m_section(ctx, {"under": h["cls"]}, only=h)


def _m_section(ctx, rule, only=None):
    for h in ctx.heads:
        if h["cls"] == rule["under"] and (only is None or h is only):
            hit = _span_hit(ctx, h["line"] + 1, h["end"])
            if hit:
                yield hit


def _m_line(ctx, rule):
    rx = re.compile(rule["pattern"], re.I)
    for i in range(1, ctx.n + 1):
        if not _prose_ok(ctx, i, rule):
            continue
        raw = ctx.lines[i - 1]
        m = rx.search(raw)
        if not m:
            continue
        if "text" in rx.groupindex:
            text = m.group("text").strip()
        else:
            b = _BULLET.match(raw)
            text = raw[b.end() :].strip() if b else raw.strip()
        if text:
            hit = {"ls": i, "le": i, "text": text}
            if rule.get("id"):
                hit["id"] = rule["id"]
            yield hit


def _m_sentences(ctx, rule):
    need = _wre(rule["words"]) if rule.get("words") else None
    for h in _sentence_hits(ctx, rule):
        if need is None or need.search(h["text"]):
            yield h


def _m_quoted_span(ctx, rule):
    need = _wre(rule["words"])
    for first, raw in _chunks(ctx, rule):
        for s, e, sent in sentences(raw):
            if not need.search(sent):
                continue
            for pat in formats.QUOTED_SPANS:
                for m in re.finditer(pat, sent):
                    a, b = m.span("q")
                    if b - a >= rule.get("min", 1):
                        yield {
                            "ls": first + raw.count("\n", 0, s + a),
                            "le": first + raw.count("\n", 0, s + b - 1),
                            "text": m.group("q"),
                        }


def _m_blockquote(ctx, rule):
    run: list[int] = []
    for i in range(1, ctx.n + 2):
        ok = (
            i <= ctx.n
            and not (ctx.front[i] or ctx.fence[i])
            and ctx.lines[i - 1].lstrip().startswith(">")
            and _in_scope(ctx, i, rule)
        )
        if ok:
            run.append(i)
        elif run:
            rows = ctx.lines[run[0] - 1 : run[-1]]
            first = rows[0].lstrip()[1:]
            rows[0] = first[1:] if first.startswith(" ") else first
            text = "\n".join(rows).strip()
            if text:
                yield {"ls": run[0], "le": run[-1], "text": text}
            run = []


def _m_fence(ctx, rule):
    allow = None if "info" not in rule else {x.lower() for x in rule["info"]}
    skip = {x.lower() for x in rule.get("skip_info", ())}
    for open_, close, info in ctx.fences:
        word = (info.split() or [""])[0].lower()
        if (allow is not None and word not in allow) or word in skip:
            continue
        if not _in_scope(ctx, open_, rule):
            continue
        hit = _span_hit(ctx, open_ + 1, min(close, ctx.n + 1) - 1)
        if hit:
            yield hit


def _m_last_task_criteria(ctx, rule):
    if not ctx.task_list:
        return
    t = ctx.task_list[-1]
    stop = t["label"] if t["label"] else t["end"] + 1
    body = "\n".join(ctx.lines[t["line"] : stop - 1])
    if not _wre(rule["words"]).search(t["title"] + "\n" + body):
        return
    for b in ctx.out.get("criterion", ()):
        if b["task"] == t["id"] and b["id"] != "goal":
            yield {"ls": b["line_start"], "le": b["line_end"], "text": b["text"]}


def _m_matching(ctx, rule):
    rx = re.compile(rule["pattern"], re.I)
    for b in ctx.out.get(rule["of"], ()):
        if b["id"] not in rule.get("skip", ()) and rx.search(b["text"]):
            yield {"ls": b["line_start"], "le": b["line_end"], "text": b["text"]}


MODES = {
    "task_body": _m_task_body,
    "after_label": _m_after_label,
    "bullets": _m_bullets,
    "section": _m_section,
    "line": _m_line,
    "sentences": _m_sentences,
    "quoted_span": _m_quoted_span,
    "blockquote": _m_blockquote,
    "fence": _m_fence,
    "last_task_criteria": _m_last_task_criteria,
    "matching": _m_matching,
}


# ---------------------------------------------------------------- blocks


def _explode(hits: list[dict], rule: dict) -> list[dict]:
    """One hit per path token of each hit, with `path` and `creates` (the nearest verb before the token decides)."""
    verbs = _wre(rule.get("verbs", ["edit_verbs", "create_verbs"]))
    creating = {w.lower() for w in _wordlist(rule.get("create_words", "create_verbs"))}
    out = []
    for h in hits:
        verb_at = [
            (m.start(), re.sub(r"\s+", " ", m.group(0).lower()))
            for m in verbs.finditer(h["text"])
        ]
        seen = set()
        for m in re.finditer(formats.PATH_TOKEN, h["text"]):
            if m.group(0) in seen:
                continue
            seen.add(m.group(0))
            before = [v for at, v in verb_at if at < m.start()]
            creates = (
                (before[-1] in creating)
                if before
                else any(v in creating for _, v in verb_at)
            )
            out.append({**h, "path": m.group(0), "creates": creates})
    return out


def _build_blocks(ctx: _Ctx) -> None:
    for kind in KINDS:
        hits: list[dict] = []
        for rule in ctx.spec.get("kinds", {}).get(kind, ()):
            found = list(MODES[rule["mode"]](ctx, rule))
            hits.extend(_explode(found, rule) if rule.get("explode_paths") else found)
        seen, ordered = set(), []
        for h in sorted(hits, key=lambda h: (h["ls"], h["le"], h.get("path", ""))):
            key = (h["ls"], h["le"], h["text"], h.get("path"))
            if key not in seen:
                seen.add(key)
                ordered.append(h)
        count: dict = {}
        for h in ordered:
            task = ctx.task_of[h["ls"]]
            if kind == "task":
                bid = h["id"]
            elif h.get("id"):
                bid = h["id"]
            else:
                count[task] = count.get(task, 0) + 1
                tag = f"{_PREFIX[kind]}{count[task]}"
                bid = f"{task}.{tag}" if task else tag
            block = {
                "kind": kind,
                "id": bid,
                "text": h["text"],
                "line_start": h["ls"],
                "line_end": h["le"],
                "task": task,
                "phase": ctx.phase_of[h["ls"]],
            }
            if "path" in h:
                block["path"], block["creates"] = h["path"], h["creates"]
            ctx.out.setdefault(kind, []).append(block)
            ctx.blocks.append(block)
