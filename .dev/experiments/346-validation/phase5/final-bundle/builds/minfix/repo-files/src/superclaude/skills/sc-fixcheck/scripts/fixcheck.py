"""fixcheck: per-finding fix budget checker for /sc:spec-panel-minfix.

Standard library only; run as
    uv run --no-project python "<base>/scripts/fixcheck.py" <subcommand> ...
Subcommands: hash, snapshot, check [--enforce]. Output is deterministic.
"""

import argparse
import difflib
import hashlib
import os
import re
import sys
import tempfile
from pathlib import Path

BUDGET_KEYS = (
    "gross", "net", "add-only", "entries", "heading", "id", "table-row",
    "normative", "universal", "condition", "check-recipe",
)
BUDGETS = {
    "C": dict(zip(BUDGET_KEYS, (120, 80, 80, 6, 0, 0, 1, 2, 1, 2, 1))),
    "M": dict(zip(BUDGET_KEYS, (80, 50, 50, 4, 0, 0, 1, 1, 1, 1, 1))),
    "m": dict(zip(BUDGET_KEYS, (0,) * 11)),
}
CYCLE_GROSS_WORDS = 600
CYCLE_GROSS_BYTES = 6144
RAW_SIZE_LIMIT = 6144
MAX_OVERRIDES = 1
EXIT = {"OK": 0, "POLICY": 1, "USAGE": 2, "INPUT": 3, "HASH": 4, "WRITE": 5, "INTERNAL": 70}

SEVERITIES = ("CRITICAL", "MAJOR", "MAJOR/FR-8", "MAJOR/FR-9", "MINOR")
CONFLICT_SEVERITIES = ("CRITICAL", "MAJOR/FR-8", "MAJOR/FR-9")
OPS = ("delete", "narrow", "replace", "add")
ID_RE = r"[A-Za-z][A-Za-z0-9_.-]*"


class FixcheckError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message


def fail(name, message):
    raise FixcheckError(EXIT[name], message)


def read_text(path):
    """Return (bytes, text) of a file; missing, unreadable or empty exits 3."""
    try:
        data = Path(path).read_bytes()
    except OSError as exc:
        fail("INPUT", f"cannot read {path}: {exc.strerror or exc}")
    text = data.decode("utf-8", errors="replace")
    if not text.strip():
        fail("INPUT", f"empty file {path}")
    return data, text


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def fenced_blocks(text, tag):
    """Yield the body lines of every fenced block opened by ```<tag>."""
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].strip() == "```" + tag:
            body = []
            i += 1
            while i < len(lines) and lines[i].strip() != "```":
                body.append(lines[i])
                i += 1
            if i == len(lines):
                fail("INPUT", f"unterminated {tag} block")
            yield body
        i += 1


class Finding:
    def __init__(self, fid, severity, grade, budget):
        self.id, self.severity, self.grade, self.budget = fid, severity, grade, budget
        self.cls = "m" if grade == "minor" else ("C" if severity == "CRITICAL" else "M")
        self.conflict = grade == "minor" and severity in CONFLICT_SEVERITIES

    def limits(self):
        lim = dict(BUDGETS[self.cls])
        if self.budget == "override":
            for key in ("gross", "net", "add-only", "entries"):
                lim[key] *= 2
        elif self.budget.startswith("gap:"):
            lim["condition"] = int(self.budget[4:])
        return lim


def parse_fixbudget(text):
    """Parse the report's fixbudget block; bad input exits 3."""
    blocks = list(fenced_blocks(text, "fixbudget"))
    if not blocks:
        fail("INPUT", "no fixbudget block in report")
    if len(blocks) > 1:
        fail("INPUT", "more than one fixbudget block in report")
    fb = {"review": None, "sha": None, "refs": None, "rows": {}, "order": [], "reasons": {}}
    for raw in blocks[0]:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = re.fullmatch(r"review:\s*([1-3])\s+of\s+3", line)
        if m:
            fb["review"] = int(m.group(1))
            continue
        m = re.fullmatch(r"reviewed_sha256:\s*([0-9a-f]{64})", line)
        if m:
            fb["sha"] = m.group(1)
            continue
        m = re.fullmatch(r"refs:\s*(\S.*)", line)
        if m:
            fb["refs"] = m.group(1)
            continue
        m = re.fullmatch(r"override-reason:\s*(" + ID_RE + r")\s+(\S.*)", line)
        if m:
            if m.group(1) in fb["reasons"]:
                fail("INPUT", f"second override-reason for {m.group(1)}")
            fb["reasons"][m.group(1)] = m.group(2)
            continue
        cells = [c.strip() for c in line.split("|")]
        if len(cells) != 4:
            fail("INPUT", f"malformed fixbudget line: {line}")
        fid, severity, grade, budget = cells
        if not re.fullmatch(ID_RE, fid) or severity not in SEVERITIES or grade not in ("blocking", "minor"):
            fail("INPUT", f"malformed fixbudget row: {line}")
        if not re.fullmatch(r"std|override|gap:[0-9]+|-", budget):
            fail("INPUT", f"malformed budget in row: {line}")
        if fid in fb["rows"]:
            fail("INPUT", f"duplicate id {fid}")
        if grade == "minor" and budget != "-":
            fail("INPUT", f"budget {budget} on minor row {fid}")
        if grade == "blocking" and budget == "-":
            fail("INPUT", f"blocking row {fid} has no budget")
        if budget.startswith("gap:") and severity not in ("MAJOR/FR-8", "MAJOR/FR-9"):
            fail("INPUT", f"gap budget on non FR-8/FR-9 row {fid}")
        fb["rows"][fid] = Finding(fid, severity, grade, budget)
        fb["order"].append(fid)
    for key, name in (("review", "review: N of 3"), ("sha", "reviewed_sha256"), ("refs", "refs")):
        if fb[key] is None:
            fail("INPUT", f"fixbudget block lacks {name}")
    overrides = [f for f in fb["rows"].values() if f.budget == "override"]
    if len(overrides) > MAX_OVERRIDES:
        fail("INPUT", "second override in fixbudget block")
    for f in overrides:
        if f.id not in fb["reasons"]:
            fail("INPUT", f"override on {f.id} without override-reason")
    for fid in fb["reasons"]:
        row = fb["rows"].get(fid)
        if row is None or row.budget != "override":
            fail("INPUT", f"override-reason for {fid}, which is not an override row")
    m = re.search(r"Fix only these blocking ids:\s*([^\n]*)", text)
    if m:
        ids = [t.strip(".,;:") for t in re.split(r"[\s,]+", m.group(1).split(". ")[0])]
        for fid in [t for t in ids if t and t != "and"]:
            row = fb["rows"].get(fid)
            if row is None or row.grade != "blocking":
                fail("INPUT", f"Reviser brief id {fid} is not a blocking id")
    return fb


class Entry:
    def __init__(self, num):
        self.num, self.fields = num, {}

    def __getattr__(self, name):
        if name.startswith("__"):
            raise AttributeError(name)
        return self.fields.get(name, "")


def parse_ledger_body(body, where):
    lines = [b for b in body if b.strip()]
    if not lines:
        fail("INPUT", f"empty fixledger block in {where}")
    m = re.fullmatch(r"report:\s*(\S.*)", lines[0].strip())
    if not m:
        fail("INPUT", f"fixledger block in {where} does not start with report:")
    ledger = {"report": os.path.basename(m.group(1).strip()), "entries": [], "deferred": {}}
    current, deferred = None, False
    for raw in lines[1:]:
        line = raw.strip()
        m = re.fullmatch(r"##\s*L([0-9]+)", line)
        if m:
            num = int(m.group(1))
            if any(e.num == num for e in ledger["entries"]):
                fail("INPUT", f"duplicate ledger entry L{num}")
            current, deferred = Entry(num), False
            ledger["entries"].append(current)
            continue
        if re.fullmatch(r"##\s*deferred", line):
            current, deferred = None, True
            continue
        if deferred:
            m = re.fullmatch(r"(?:-\s*)?(" + ID_RE + r"):\s*escalated:\s*(\S.*)", line)
            if not m:
                fail("INPUT", f"malformed deferred line: {line}")
            ledger["deferred"][m.group(1)] = m.group(2)
            continue
        m = re.fullmatch(r"(finding|op|old|anchor|new|considered|depends):\s*(.*)", line)
        if current is None or not m:
            fail("INPUT", f"malformed fixledger line: {line}")
        if m.group(1) in current.fields:
            fail("INPUT", f"duplicate key {m.group(1)} in L{current.num}")
        current.fields[m.group(1)] = m.group(2).strip()
    nums = {e.num for e in ledger["entries"]}
    for e in ledger["entries"]:
        if not re.fullmatch(ID_RE, e.finding) or e.op not in OPS:
            fail("INPUT", f"L{e.num} needs one finding id and an op in {'|'.join(OPS)}")
        if e.op == "add" and not (e.anchor and e.considered):
            fail("INPUT", f"L{e.num} op add needs anchor and considered")
        if e.op != "add" and not e.old:
            fail("INPUT", f"L{e.num} op {e.op} needs old")
        if e.op != "delete" and not e.new:
            fail("INPUT", f"L{e.num} op {e.op} needs new")
        if e.depends:
            m = re.fullmatch(r"L([0-9]+)", e.depends)
            if not m or int(m.group(1)) not in nums or int(m.group(1)) == e.num:
                fail("INPUT", f"L{e.num} depends on an unknown entry {e.depends}")
    return ledger


def parse_ledger(text, where="disposition"):
    """Parse the first fenced fixledger block of a disposition file; bad input exits 3."""
    blocks = list(fenced_blocks(text, "fixledger"))
    if not blocks:
        fail("INPUT", f"no fixledger block in {where}")
    return parse_ledger_body(blocks[0], where)


def ledger_report_name(text):
    """Return the report: names of the file's fixledger blocks, or [] when it has none."""
    names = []
    try:
        for body in fenced_blocks(text, "fixledger"):
            first = next((b.strip() for b in body if b.strip()), "")
            m = re.fullmatch(r"report:\s*(\S.*)", first)
            if m:
                names.append(os.path.basename(m.group(1).strip()))
    except FixcheckError:
        return []
    return names


def find_ledger(report_path):
    """The one file in the report's directory whose fixledger block answers this report."""
    report = Path(report_path)
    matches = []
    for path in sorted(report.parent.iterdir()):
        if not path.is_file() or path.resolve() == report.resolve():
            continue
        try:
            text = path.read_bytes().decode("utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if report.name in ledger_report_name(text):
            matches.append(path)
    if len(matches) != 1:
        found = ", ".join(p.name for p in matches) or "none"
        fail("INPUT", f"need exactly one disposition file answering {report.name}; found {found}")
    return matches[0]


def load_ledger(report_path, ledger_path):
    path = Path(ledger_path) if ledger_path else find_ledger(report_path)
    data, text = read_text(path)
    ledger = parse_ledger(text, path.name)
    if ledger["report"] != Path(report_path).name:
        fail("INPUT", f"{path.name} answers {ledger['report']}, not {Path(report_path).name}")
    return path, data, ledger


WORD_SETS = {
    "normative": frozenset(("must", "shall", "never", "always")),
    "universal": frozenset(("only", "every", "exactly", "none", "total", "closed")),
    "condition": frozenset(("if", "unless", "when", "whenever", "where", "except", "otherwise")),
}
CITATION_RE = re.compile(r"(?=[^:]*[A-Za-z./])[\w./~@+-]+:\d+(?:-\d+)?")
NEW_ID_RE = re.compile(r"(?<![A-Za-z0-9_-])([A-Z]+-?\d+(?:\.\d+)*)(?![A-Za-z0-9_-])")
RECIPE_RE = re.compile(r"\bgrep\b|\bgit |\bdiff\b|\bfind |\buv |\||\$\(")
SPAN_RE = re.compile(r"`([^`\n]+)`")
SENTENCE_GAP_RE = re.compile(r"(?<=[.!?])\s+(?=\S)")
CURLY = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"'})
PUNCT = "()[]{}`'\",.;:!?*_"
OP_RANK = {"delete": 0, "narrow": 1, "replace": 2}


def norm_token(tok):
    """Normalise one whitespace-separated token: straight quotes, no emphasis marks."""
    return tok.translate(CURLY).replace("**", "").replace("__", "").strip("*")


def is_word(tok):
    """A counted word: has a letter or digit and is not a path:line citation."""
    if not re.search(r"[A-Za-z0-9]", tok):
        return False  # pipes, heading marks, bullets, dashes
    return not CITATION_RE.fullmatch(tok.strip(PUNCT))


class Unit:
    """One comparable piece of text: a sentence, a table cell, a heading or a code line."""

    def __init__(self, text, start, end, line, kind):
        self.start, self.end, self.line, self.kind = start, end, line, kind
        self.raw = text[start:end]
        self.toks = [(n, t) for n, t in ((norm_token(t), t) for t in self.raw.split()) if n]
        self.norm = " ".join(n for n, _ in self.toks)


def cell_spans(body):
    pipes = [i for i, ch in enumerate(body) if ch == "|" and (i == 0 or body[i - 1] != "\\")]
    spans = []
    for a, b in zip(pipes, pipes[1:] + [len(body)]):
        cell = body[a + 1:b]
        if cell.strip():
            s = a + 1 + len(cell) - len(cell.lstrip())
            spans.append((s, a + 1 + len(cell.rstrip())))
    return spans


def units(text):
    """Split text into units; returns (units, separators, tail) so text == seps+units+tail."""
    out, pos, line_no, fence = [], 0, 0, False
    for line in text.splitlines(keepends=True):
        line_no += 1
        body = line.rstrip("\r\n")
        stripped = body.strip()
        lead, end = len(body) - len(body.lstrip()), len(body.rstrip())
        spans = []
        if stripped.startswith(("```", "~~~")):
            spans, fence = [(lead, end, "fence")], not fence
        elif fence:
            spans = [(lead, end, "code")] if stripped else []
        elif not stripped:
            spans = []
        elif stripped.startswith("|"):
            cells = cell_spans(body)
            if all(re.fullmatch(r":?-+:?", body[s:e]) for s, e in cells):
                spans = [(lead, end, "sep")]
            else:
                spans = [(s, e, "cell") for s, e in cells]
        elif stripped.startswith("#"):
            spans = [(lead, end, "heading")]
        else:
            start = lead
            for m in SENTENCE_GAP_RE.finditer(body, lead):
                spans.append((start, m.start(), "text"))
                start = m.end()
            spans.append((start, end, "text"))
        for s, e, kind in spans:
            unit = Unit(text, pos + s, pos + e, line_no, kind)
            if unit.toks:
                out.append(unit)
        pos += len(line)
    seps, prev = [], 0
    for u in out:
        seps.append(text[prev:u.start])
        prev = u.end
    return out, seps, text[prev:]


def contains(seq, sub):
    n = len(sub)
    return n == 0 or any(seq[i:i + n] == sub for i in range(len(seq) - n + 1))


def locate(entry, bu):
    """Base unit span [a, b) of the entry's old/anchor quote, or None when it is not
    exactly once in the baseline (or shorter than 40 characters and not a whole unit)."""
    quote = " ".join(t for t in (norm_token(x) for x in (entry.old or entry.anchor).split())
                     if t and set(t) != {"|"})
    if not quote:
        return None
    offsets, joined, p = [], [], 0
    for u in bu:
        offsets.append(p)
        joined.append(u.norm)
        p += len(u.norm) + 1
    joined = " ".join(joined)
    hits, p = [], joined.find(quote)
    while p != -1:
        end = p + len(quote)
        if (p == 0 or joined[p - 1] == " ") and (end == len(joined) or joined[end] == " "):
            hits.append(p)
        p = joined.find(quote, p + 1)
    if len(hits) != 1:
        return None
    p, end = hits[0], hits[0] + len(quote)
    a = max(k for k, o in enumerate(offsets) if o <= p)
    b = max(k for k, o in enumerate(offsets) if o < end) + 1
    whole = p == offsets[a] and end == offsets[b - 1] + len(bu[b - 1].norm)
    if not whole and len(quote) < 40:
        return None
    return a, b


class Part:
    """A (sub-)hunk: base units [i1, i2) replaced by revised units [j1, j2)."""

    def __init__(self, i1, i2, j1, j2, claimant):
        self.i1, self.i2, self.j1, self.j2, self.claimant = i1, i2, j1, j2, claimant
        self.entry, self.reason, self.mislabel, self.k = None, "", "", 0


def pair_units(bu, ru, i1, i2, j1, j2):
    """Monotone pairing of similar units (token ratio >= 0.5) inside one diff region."""
    n, m = i2 - i1, j2 - j1
    if not n or not m or n * m > 40000:  # shortcut: very large rewrites stay unpaired; raise the cap if real specs hit it
        return []
    ratio, score = {}, [[0.0] * (m + 1) for _ in range(n + 1)]
    for a in range(1, n + 1):
        for b in range(1, m + 1):
            best = max(score[a - 1][b], score[a][b - 1])
            r = difflib.SequenceMatcher(None, [t for t, _ in bu[i1 + a - 1].toks],
                                        [t for t, _ in ru[j1 + b - 1].toks], autojunk=False).ratio()
            if r >= 0.5:
                ratio[(a, b)] = r
                best = max(best, score[a - 1][b - 1] + r)
            score[a][b] = best
    pairs, a, b = [], n, m
    while a and b:
        if (a, b) in ratio and score[a][b] == score[a - 1][b - 1] + ratio[(a, b)]:
            pairs.append((i1 + a - 1, j1 + b - 1))
            a, b = a - 1, b - 1
        elif score[a][b] == score[a - 1][b]:
            a -= 1
        else:
            b -= 1
    return pairs[::-1]


def split_region(i1, i2, j1, j2, located, bu, ru):
    """Split one diff region per ledger entry whose old/anchor unit range it touches (section 2.2).

    Similar units are paired. A paired or deleted unit belongs to the entry whose old quote covers
    it. An inserted unit belongs to the add entry anchored at its position, else to an entry of this
    region whose new words it holds, else (unless it is a fence or code line) to its neighbouring
    inserted unit, else to the deleted units it replaces (unattributed when they are), else to the
    pair before it, else the pair after it. Between two pairs, each owner's deleted and inserted
    units form one part, in order, so a revert restores text in place. Unowned units are unattributed,
    and a gap holding an unowned deleted unit and inserted text is unattributed as a whole."""
    local = [e for e in located
             if (e.op == "add" and i1 <= e.loc[1] <= i2) or (e.op != "add" and e.loc[0] < i2 and e.loc[1] > i1)]

    def pick(hits):
        return min(hits, key=lambda e: (e.loc[0], e.num)) if hits else None

    def base_owner(k):
        return pick([e for e in local if e.op != "add" and e.loc[0] <= k < e.loc[1]])

    def ins_owner(pos, k):
        toks = [n for n, _ in ru[k].toks]
        return pick([e for e in local if e.op == "add" and e.loc[1] == pos]
                    or [e for e in local if new_key(e) and contains(toks, new_key(e)[:3])])

    pairs = pair_units(bu, ru, i1, i2, j1, j2)
    segs, i, j, prev_pair = [], i1, j1, None
    for n, (pi, pj) in enumerate(pairs + [(i2, j2)]):
        dels = [base_owner(k) for k in range(i, pi)]
        ins = [ins_owner(pi, k) for k in range(j, pj)]
        # an unclaimed fence or code line is never charged to a neighbour: it changes the structure
        # of the text after it, so it stays unattributed and is reverted on its own
        solo = [ins[x] is None and ru[j + x].kind in ("fence", "code") for x in range(len(ins))]
        for x in list(range(1, len(ins))) + list(range(len(ins) - 2, -1, -1)):
            if ins[x] is None and not solo[x]:
                ins[x] = ins[x - 1] if x and ins[x - 1] is not None else (ins[x + 1] if x + 1 < len(ins) else None)
        next_pair = base_owner(pi) if n < len(pairs) else None
        # an unclaimed insertion that replaces deleted units goes with them (unattributed when they
        # are), so a revert never restores the old text while keeping its replacement
        fallback = dels[-1] if dels else (prev_pair if prev_pair is not None else next_pair)
        ins = [None if solo[x] else fallback if o is None else o for x, o in enumerate(ins)]
        if None in dels and ins:
            # undeclared deletions next to inserted text: the gap is reverted as a whole, or a kept
            # insertion could land after restored text it was meant to replace (pure deletions stay apart)
            dels, ins = [None] * len(dels), [None] * len(ins)
        d = x = 0
        while d < len(dels) or x < len(ins):
            owner = dels[d] if d < len(dels) else ins[x]
            dd, xx = d, x
            while dd < len(dels) and dels[dd] is owner:
                dd += 1
            while xx < len(ins) and ins[xx] is owner:
                xx += 1
            segs.append((i + d, i + dd, j + x, j + xx, owner))
            d, x = dd, xx
        if n < len(pairs):
            segs.append((pi, pi + 1, pj, pj + 1, next_pair))
            prev_pair = next_pair
        i, j = pi + 1, pj + 1
    parts = []
    for a, b, c, d, owner in segs:
        if parts and parts[-1].claimant is owner:
            parts[-1].i2, parts[-1].j2 = b, d
        else:
            parts.append(Part(a, b, c, d, owner))
    return parts


def analyze(base_data, base_text, rev_data, rev_text, fb, ledger):
    """Diff, attribute and score one fix cycle; returns a dict the report and --enforce use."""
    bu, bseps, btail = units(base_text)
    ru, rseps, rtail = units(rev_text)
    base_ids = set(NEW_ID_RE.findall(base_text))
    entries = ledger["entries"]
    located, unlocated = [], []
    for e in entries:
        e.loc = locate(e, bu)
        (located if e.loc else unlocated).append(e)
    opcodes, moved_b, moved_r = diff_hunks(bu, ru)
    regions, hunks = [], []
    for tag, i1, i2, j1, j2 in opcodes:
        if tag == "equal":
            regions.append(("equal", i1, i2, j1, j2))
            continue
        parts = split_region(i1, i2, j1, j2, located, bu, ru)
        regions.append(("parts", parts))
        for part in parts:
            part.b = [bu[i] for i in range(part.i1, part.i2) if i not in moved_b]
            part.r = [ru[j] for j in range(part.j1, part.j2) if j not in moved_r]
            if part.b or part.r:
                hunks.append(part)
    for k, h in enumerate(hunks, 1):
        h.k = k
        element_counts(h, base_ids)
        rev_lines = [u.line for u in (ru[j] for j in range(h.j1, h.j2))]
        if rev_lines:
            h.lines = (rev_lines[0], rev_lines[-1])
        else:
            at = ru[h.j1].line if h.j1 < len(ru) else rev_text.count("\n") + 1
            h.lines = (at, at)
    attribute(hunks, fb, unlocated)
    res = score(fb, ledger, hunks)
    res.update(cycle_checks(hunks, base_data, rev_data))
    res["result"] += res.pop("size")
    res["code"] = EXIT["POLICY"] if res["result"] else EXIT["OK"]
    res.update(regions=regions, moved_b=moved_b, moved_r=moved_r, bu=bu, bseps=bseps, btail=btail, ru=ru, rseps=rseps, rtail=rtail)
    return res


def diff_hunks(bu, ru):
    """Unit-level opcodes plus moved units: an inserted unit identical to a deleted one counts zero.

    A unit's identity is its kind and its normalised text, so a whitespace change that changes a
    unit's kind (a fence line joined onto a sentence, a table row cut to one word) is a hunk too.
    Known limit: a join that keeps every unit's kind and text (two table rows or two paragraphs put
    on one line) is no hunk, so plain check does not report it; --enforce still undoes it, because
    it restores the baseline's line breaks between unchanged words (restore_line_breaks)."""
    bk, rk = [(u.kind, u.norm) for u in bu], [(u.kind, u.norm) for u in ru]
    opcodes = difflib.SequenceMatcher(None, bk, rk, autojunk=False).get_opcodes()
    deleted = {}
    for tag, i1, i2, _, _ in opcodes:
        if tag != "equal":
            for i in range(i1, i2):
                deleted.setdefault(bk[i], []).append(i)
    moved_b, moved_r = {}, {}
    for tag, _, _, j1, j2 in opcodes:
        if tag != "equal":
            for j in range(j1, j2):
                pool = deleted.get(rk[j])
                if pool:
                    i = pool.pop(0)
                    moved_b[i], moved_r[j] = j, i
    return opcodes, moved_b, moved_r


def words(toks):
    """The counted words among (normalised, raw) tokens."""
    return [n for n, _ in toks if is_word(n)]


def element_counts(h, base_ids):
    """Word-level diff inside one hunk: added/deleted words, bytes, derived op and element counts."""
    bt = [t for u in h.b for t in u.toks]
    rt = [t for u in h.r for t in u.toks]
    sm = difflib.SequenceMatcher(None, [n for n, _ in bt], [n for n, _ in rt], autojunk=False)
    added, removed = [], []
    for tag, a1, a2, b1, b2 in sm.get_opcodes():
        if tag in ("replace", "delete"):
            removed += bt[a1:a2]
        if tag in ("replace", "insert"):
            added += rt[b1:b2]
    add_words = words(added)
    h.added, h.deleted = len(add_words), len(words(removed))
    h.bytes = sum(len(raw.encode("utf-8")) + 1 for _, raw in added)
    h.words_text = " ".join(raw for _, raw in added)
    if not h.b:
        h.op = "add"
    elif not add_words:
        h.op = "delete"
    else:
        h.op = "narrow" if h.added <= h.deleted else "replace"
    lower = [w.strip(PUNCT).lower() for w in add_words]
    c = {key: sum(w in vocab for w in lower) for key, vocab in WORD_SETS.items()}
    c["heading"] = max(0, sum(u.kind == "heading" for u in h.r) - sum(u.kind == "heading" for u in h.b))
    c["table-row"] = max(0, len({u.line for u in h.r if u.kind == "cell"})
                         - len({u.line for u in h.b if u.kind == "cell"}))
    c["id"] = sorted({i for w in add_words for i in NEW_ID_RE.findall(w.strip(PUNCT))} - base_ids)
    spans = {}
    for side, sign in ((h.r, 1), (h.b, -1)):
        for u in side:
            for span in SPAN_RE.findall(u.raw):
                if RECIPE_RE.search(span):
                    spans[span] = spans.get(span, 0) + sign
    fences = max(0, sum(u.kind == "fence" for u in h.r) - sum(u.kind == "fence" for u in h.b))
    c["check-recipe"] = sum(v for v in spans.values() if v > 0) + (fences + 1) // 2
    h.counts = c


def new_key(entry):
    """The entry's `new` words (at most 10), normalised."""
    return [n for n in (norm_token(t) for t in entry.new.split()) if n][:10]


def attribute(hunks, fb, unlocated):
    """Charge each hunk to its claiming entry, or leave it unattributed with a reason.

    An entry's hunks are judged together: its new words must appear in their revised text, and
    its real op is derived from all of them (no baseline text: add; no added words: delete;
    added <= deleted: narrow; else replace). A cheaper real op than the declared one is accepted."""
    by_entry = {}
    for h in hunks:
        if h.claimant is not None:
            by_entry.setdefault(h.claimant.num, []).append(h)
    for h in hunks:
        e = h.claimant
        if e is None:
            rnorm = [n for u in h.r for n, _ in u.toks]
            hit = next((u for u in unlocated if new_key(u) and contains(rnorm, new_key(u))), None)
            h.reason = f"quote not in baseline (L{hit.num})" if hit else "no ledger entry"
            continue
        group = by_entry[e.num]
        rnorm = [n for p in group for u in p.r for n, _ in u.toks]
        added, deleted = sum(p.added for p in group), sum(p.deleted for p in group)
        key = new_key(e)
        if e.finding not in fb["rows"]:
            h.reason = f"unknown finding {e.finding} (L{e.num})"
        elif key and not contains(rnorm, key):
            h.reason = f"new words not found (L{e.num})"
        elif not key and added:
            h.reason = f"delete entry adds words (L{e.num})"
        else:
            h.entry = e
            if not any(p.b for p in group):
                h.op = "add"
            elif not added:
                h.op = "delete"
            else:
                h.op = "narrow" if added <= deleted else "replace"
            ok = h.op == e.op or (e.op in OP_RANK and h.op in OP_RANK and OP_RANK[h.op] <= OP_RANK[e.op])
            if not ok and h is group[0]:
                h.mislabel = f"op L{e.num} {e.op}!={h.op}"


def natural(fid):
    return [int(x) if x.isdigit() else x for x in re.split(r"([0-9]+)", fid)]


def score(fb, ledger, hunks):
    """Per-finding totals, budget reasons and statuses (sections 2.2, 2.3)."""
    per = {fid: {"hunks": [], "entries": set(), "ops": set(), "ids": set(), "mislabel": [],
                 "totals": dict.fromkeys(BUDGET_KEYS, 0)} for fid in fb["order"]}
    for h in hunks:
        if h.entry is None:
            continue
        p = per[h.entry.finding]
        t = p["totals"]
        p["hunks"].append(h)
        p["entries"].add(h.entry.num)
        p["ops"].add(h.op)
        p["ids"].update(h.counts["id"])
        if h.mislabel:
            p["mislabel"].append(h.mislabel)
        t["gross"] += h.added
        t["net"] += h.added - h.deleted
        t["add-only"] += h.added if h.op == "add" else 0
        for key in ("heading", "table-row", "normative", "universal", "condition", "check-recipe"):
            t[key] += h.counts[key]
    for fid, p in per.items():
        f, t = fb["rows"][fid], p["totals"]
        t["entries"], t["id"] = len(p["entries"]), len(p["ids"])
        lim = f.limits()
        p["over"] = [f"{k} {t[k]}>{lim[k]}" for k in BUDGET_KEYS if t[k] > lim[k]]
        if f.cls == "m":
            p["status"] = "MINOR-EDIT" if p["hunks"] else "minor"
        elif p["over"] or p["mislabel"]:
            p["status"] = "OVER"
        elif fid in ledger["deferred"]:
            p["status"] = "escalated"
        elif p["hunks"]:
            p["status"] = "fixed"
        elif any(e.finding == fid for e in ledger["entries"]):
            p["status"] = "reverted"
        else:
            p["status"] = "unanswered"
    order = fb["order"]
    # attribution reasons print before size reasons
    result = [f"UNATTRIBUTED h{h.k}" for h in hunks if h.entry is None]
    result += [f"MISLABELLED {fid}" for fid in order if per[fid]["mislabel"]]
    result += [f"MINOR-EDIT {fid}" for fid in order if per[fid]["status"] == "MINOR-EDIT"]
    result += [f"OVER-BUDGET {fid}" for fid in order if per[fid]["over"] and fb["rows"][fid].cls != "m"]
    return {"hunks": hunks, "per": per, "result": result}


def cycle_checks(hunks, base_data, rev_data):
    """Cycle cap (600 words, 6,144 bytes added) and raw file growth (6,144 bytes)."""
    cycle_words = sum(h.added for h in hunks)
    cycle_bytes = sum(h.bytes for h in hunks)
    raw = len(rev_data) - len(base_data)
    size = []
    if cycle_words > CYCLE_GROSS_WORDS:
        size.append(f"CYCLE words {cycle_words}>{CYCLE_GROSS_WORDS}")
    if cycle_bytes > CYCLE_GROSS_BYTES:
        size.append(f"CYCLE bytes {cycle_bytes}>{CYCLE_GROSS_BYTES}")
    if raw > RAW_SIZE_LIMIT:
        size.append(f"RAW-SIZE +{raw}>{RAW_SIZE_LIMIT}")
    return {"cycle_words": cycle_words, "cycle_bytes": cycle_bytes, "raw": raw, "size": size}


def render_report(res, fb, ledger, base_data, rev_data, ledger_data):
    """The section 3.3 report: header, summary, one line per hunk, one per finding, totals."""
    hunks, per = res["hunks"], res["per"]
    attributed = sum(h.entry is not None for h in hunks)
    lines = [
        f"FIXCHECK cycle={fb['review']} exit={res['code']} base=sha:{sha256(base_data)[:8]} "
        f"revised=sha:{sha256(rev_data)[:8]} ledger=sha:{sha256(ledger_data)[:8]}",
        f"hunks={len(hunks)} attributed={attributed} unattributed={len(hunks) - attributed} "
        f"moved={len(res['moved_b'])} net={sum(h.added - h.deleted for h in hunks)} "
        f"cycle_words={res['cycle_words']}/{CYCLE_GROSS_WORDS} cycle_bytes={res['cycle_bytes']}/{CYCLE_GROSS_BYTES} "
        f"raw_size={res['raw']:+d}/{RAW_SIZE_LIMIT}",
    ]
    for h in hunks:
        who = f"L{h.entry.num} {h.entry.finding}" if h.entry else "unattributed -"
        line = f"h{h.k} {who} revised:{h.lines[0]}-{h.lines[1]} +{h.added}/-{h.deleted}"
        if h.entry is None:
            line += f" reason={h.reason}"
        lines.append(line + (f" {h.mislabel}" if h.mislabel else ""))
    for fid in fb["order"]:
        f, p = fb["rows"][fid], per[fid]
        counts = " ".join(f"{k}={p['totals'][k]}" for k in BUDGET_KEYS)
        detail = ", ".join(p["mislabel"] + p["over"])
        lines.append(f"finding {fid} cls={f.cls} grade={f.grade} budget={f.budget} "
                     f"op={'+'.join(sorted(p['ops'])) or '-'} {counts} status={p['status']}"
                     + (f" {detail}" if detail else ""))
    lines += [f"GRADE-CONFLICT {fid}" for fid in fb["order"] if fb["rows"][fid].conflict]
    unattr = [f'h{h.k} +{h.added} words "{" ".join(h.words_text.split()[:8])}"' for h in hunks if h.entry is None]
    lines.append("unattributed: " + ("; ".join(unattr) or "none"))
    esc = [f"{fid} ({need})" for fid, need in sorted(ledger["deferred"].items(), key=lambda kv: natural(kv[0]))]
    esc += [f"{fid} (reverted)" for fid in fb["order"] if per[fid]["status"] == "reverted"]
    lines.append("escalated: " + ("; ".join(esc) or "none"))
    carried = []
    for fid in sorted(fb["order"], key=natural):
        f, status = fb["rows"][fid], per[fid]["status"]
        if f.severity.startswith(("CRITICAL", "MAJOR")) and (
                f.grade == "minor" or status in ("escalated", "reverted", "unanswered", "OVER")):
            label = "GRADE-CONFLICT" if f.conflict and status == "minor" else status
            carried.append(f"{fid}({label})")
    lines.append(f"carried-open: n={len(carried)}" + "".join(" " + c for c in carried))
    lines.append("result: " + ("; ".join(res["result"]) or "ok"))
    lines.append(f"FIXCHECK exit={res['code']}")
    return lines


def load_check_inputs(args):
    base_data, base_text = read_text(args.baseline)
    rev_data, rev_text = read_text(args.revised)
    _, report_text = read_text(args.report)
    fb = parse_fixbudget(report_text)
    if sha256(base_data) != fb["sha"]:
        fail("HASH", "baseline sha256 differs from the report's reviewed_sha256")
    _, ledger_data, ledger = load_ledger(args.report, args.ledger)
    return base_data, base_text, rev_data, rev_text, fb, ledger, ledger_data


def atomic_write(path, data):
    """Write bytes via a temp file in the same directory, then rename; failure exits 5."""
    path = Path(path)
    tmp = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".fixcheck-", suffix=".tmp")
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
        os.replace(tmp, str(path))
    except OSError as exc:
        if tmp and os.path.exists(tmp):
            os.unlink(tmp)
        fail("WRITE", f"cannot write {path}: {exc.strerror or exc}")


def region_edits(res, revert, base_text, rev_text):
    """One edit (start, end, replacement) on the revised text per diff region holding a reverted part.

    The region's text, from the end of the equal unit before it to the start of the equal unit after
    it, is composed again: kept parts give their revised units, reverted parts their baseline units.
    A unit whose emitted neighbour is its neighbour in its own file keeps its own separator. At any
    other junction the separator is split at its first line break: the part before the break (the end
    of the previous line) comes from the unit actually emitted before, the rest (the break and this
    line's prefix) from the unit's own file; a unit that continued a line whose earlier units were
    dropped takes the break that preceded the dropped run. Other regions are left byte for byte."""
    files = {"b": (res["bu"], res["bseps"], res["btail"]), "r": (res["ru"], res["rseps"], res["rtail"])}

    def own_sep(side, k):
        units, seps, tail = files[side]
        return seps[k] if k < len(units) else tail

    def trailer(side, k):
        after = own_sep(side, k + 1)
        return after.split("\n", 1)[0] if "\n" in after else after.rstrip()

    def separator(prev, pos, side, k):
        if prev is not None and prev[side] == k - 1:
            return own_sep(side, k)  # neighbours in the same file
        sep = own_sep(side, k)
        if "\n" not in sep and pos[side] < k:
            sep = own_sep(side, pos[side])  # it continued a line whose earlier units were dropped
        if "\n" not in sep or prev is None:
            return sep
        last = "b" if prev["b"] is not None and (prev["r"] is None or side == "b") else "r"
        return trailer(last, prev[last]) + sep[sep.index("\n"):]

    edits = []
    for region in res["regions"]:
        if region[0] != "parts" or not any(p in revert for p in region[1]):
            continue
        parts = region[1]
        i1, i2, j1, j2 = parts[0].i1, parts[-1].i2, parts[0].j1, parts[-1].j2
        prev = {"b": i1 - 1, "r": j1 - 1} if j1 or i1 else None  # the equal unit before the region
        pos, out = {"b": i1, "r": j1}, []
        for part in parts:
            side, lo, hi = ("b", part.i1, part.i2) if part in revert else ("r", part.j1, part.j2)
            for k in range(lo, hi):
                out.append(separator(prev, pos, side, k) + files[side][0][k].raw)
                prev = {"b": None, "r": None, side: k}
            if lo < hi:  # the part takes the place of the other file's span
                pos = {"b": part.i2, "r": part.j2}
        if prev is None or (prev["b"] is not None and prev["r"] is not None):
            side = "b" if parts[-1] in revert else "r"  # nothing emitted: the last part decides
        else:
            side = "b" if prev["b"] is not None else "r"
        out.append(separator(prev, pos, side, i2 if side == "b" else j2))
        start = res["ru"][j1 - 1].end if j1 else 0
        end = len(rev_text) if j2 == len(res["ru"]) else res["ru"][j2].start
        edits.append((start, end, "".join(out)))
    return edits


def apply_edits(text, edits):
    out, pos = [], 0
    for start, end, repl in sorted(edits, key=lambda e: (e[0], e[1])):
        if start < pos:
            fail("INTERNAL", f"overlapping revert edits at offset {start}")
        out += [text[pos:start], repl]
        pos = end
    out.append(text[pos:])
    return "".join(out)


def depends_closure(bad, ledger, hunks, per):
    """Add the finding of every entry whose depends: names a reverted entry: one with no kept
    hunk attributed to it (section 2.2), whether its finding is reverted, its hunks are
    unattributed, its quote is not in the baseline, or it changed nothing."""
    grew = True
    while grew:
        kept = {h.entry.num for h in hunks if h.entry is not None and h.entry.finding not in bad}
        grew = False
        for e in ledger["entries"]:
            if e.depends and int(e.depends[1:]) not in kept and e.finding in per and e.finding not in bad:
                bad.add(e.finding)
                grew = True


def moved_closure(revert, res):
    """A reverted part restores its moved units, so their moved copies are reverted too."""
    owner_b, owner_r = {}, {}
    for region in res["regions"]:
        if region[0] == "parts":
            for part in region[1]:
                owner_b.update((i, part) for i in range(part.i1, part.i2))
                owner_r.update((j, part) for j in range(part.j1, part.j2))
    todo = list(revert)
    while todo:
        part = todo.pop()
        partners = [owner_r[res["moved_b"][i]] for i in range(part.i1, part.i2) if i in res["moved_b"]]
        partners += [owner_b[res["moved_r"][j]] for j in range(part.j1, part.j2) if j in res["moved_r"]]
        for q in partners:
            if q not in revert:
                revert.add(q)
                todo.append(q)


def part_fences(h):
    """Fence lines a hunk adds (positive) or removes (negative)."""
    return sum(u.kind == "fence" for u in h.r) - sum(u.kind == "fence" for u in h.b)


FENCE_MARK_RE = re.compile(r"(`{3,}|~{3,})\S*")
WORD_RE = re.compile(r"\S+")


def line_start(text, pos):
    return text.rfind("\n", 0, pos) + 1


def line_end(text, pos):
    end = text.find("\n", pos)
    return len(text) if end == -1 else end


def opens_line(text, start, word):
    """The word is a fence marker standing at the start of its line."""
    return bool(FENCE_MARK_RE.fullmatch(word)) and not text[line_start(text, start):start].strip()


def word_opcodes(base_text, rev_text):
    """Words of both files with offsets, aligned (the same alignment for every word-level step)."""
    bt = [(m.group(), m.start(), m.end()) for m in WORD_RE.finditer(base_text)]
    rt = [(m.group(), m.start(), m.end()) for m in WORD_RE.finditer(rev_text)]
    sm = difflib.SequenceMatcher(None, [w for w, _, _ in bt], [w for w, _, _ in rt], autojunk=False)
    return bt, rt, sm.get_opcodes()


def restore_line_breaks(base_text, rev_text):
    """Put back the baseline's line breaks between words that are unchanged on both sides.

    Wherever two neighbouring words are the same in both files and the whitespace between them has a
    different number of line breaks (a joined or split line, row or paragraph), the baseline's
    whitespace is restored. A ledger entry is word-based, so such a change is never part of a
    declared fix. Returns (text, number of breaks restored)."""
    bt, rt, opcodes = word_opcodes(base_text, rev_text)
    edits = []
    for tag, i1, i2, j1, _ in opcodes:
        if tag != "equal":
            continue
        for k in range(1, i2 - i1):
            bgap = base_text[bt[i1 + k - 1][2]:bt[i1 + k][1]]
            rstart, rend = rt[j1 + k - 1][2], rt[j1 + k][1]
            if bgap.count("\n") != rev_text[rstart:rend].count("\n"):
                edits.append((rstart, rend, bgap))
    return apply_edits(rev_text, edits), len(edits)


def restore_fences(base_text, rev_text, ledger):
    """Undo undeclared fence lines: a fence opens or closes a code block, so one added or dropped
    fence changes the kind of every unit after it and every later hunk would be judged out of
    context. On the word alignment, a fence marker at a line start that the revision adds is removed
    (the whole line and one blank line when it stands alone, else the marker and its spaces), unless
    the inserted words hold the new words of an entry that itself adds a fence; a fence line the
    revision drops is put back before the line that now follows it. Returns (text, changes)."""
    bt, rt, opcodes = word_opcodes(base_text, rev_text)
    declared = [new_key(e) for e in ledger["entries"] if FENCE_MARK_RE.search(e.new)]
    edits = []
    for tag, i1, i2, j1, j2 in opcodes:
        if tag == "equal":
            continue
        added = [(s, e) for w, s, e in rt[j1:j2] if opens_line(rev_text, s, w)]
        dropped = [(s, e) for w, s, e in bt[i1:i2] if opens_line(base_text, s, w)]
        run = [norm_token(w) for w, _, _ in rt[j1:j2]]
        if len(added) > len(dropped) and not any(k and contains(run, k) for k in declared):
            for s, _ in added[len(dropped):]:
                start, rest = line_start(rev_text, s), rev_text[s:line_end(rev_text, s)]
                if FENCE_MARK_RE.fullmatch(rest.strip()):
                    end = min(line_end(rev_text, s) + 1, len(rev_text))
                    if rev_text[end:end + 1] == "\n" and rev_text[max(0, start - 2):start] == "\n\n":
                        end += 1
                    edits.append((start, end, ""))
                else:
                    m = re.match(r"\S+\s*", rest)
                    edits.append((s, s + m.end(), ""))
        elif len(dropped) > len(added) and j2 < len(rt) and not rev_text[line_start(rev_text, rt[j2][1]):rt[j2][1]].strip():
            pos = line_start(rev_text, rt[j2][1])
            for s, _ in dropped[len(added):]:
                edits.append((pos, pos, base_text[line_start(base_text, s):line_end(base_text, s)] + "\n"))
    return apply_edits(rev_text, edits), len(edits)


def remove_stray_fences(base_data, base_text, rev_text, fb, ledger):
    """Undo the revision's undeclared layout changes before judging fixes, in memory: first the
    baseline's line breaks between unchanged words (restore_line_breaks), then undeclared fence lines
    (restore_fences), then line breaks again. Returns (text, its analysis, fence changes undone,
    line breaks restored)."""
    work_text, breaks = restore_line_breaks(base_text, rev_text)
    work_text, stray = restore_fences(base_text, work_text, ledger)
    if stray:  # a removed marker can leave two unchanged words with the wrong break between them
        work_text, more = restore_line_breaks(base_text, work_text)
        breaks += more
    res = analyze(base_data, base_text, work_text.encode("utf-8"), work_text, fb, ledger)
    return work_text, res, stray, breaks


def enforce(args, base_data, base_text, rev_data, rev_text, fb, ledger, ledger_data):
    """One revert pass (section 2.3), one atomic write of the spec, then the re-check."""
    if not ledger["entries"]:
        fail("INPUT", "--enforce needs a ledger with at least one entry")

    work_text, res, stray, breaks = remove_stray_fences(base_data, base_text, rev_text, fb, ledger)
    per, hunks = res["per"], res["hunks"]
    bad = {fid for fid, p in per.items() if p["status"] in ("OVER", "MINOR-EDIT")}
    depends_closure(bad, ledger, hunks, per)

    def reverted_parts():
        return {h for h in hunks if h.entry is None or h.entry.finding in bad}

    # cycle cap: blocking MAJOR before CRITICAL, largest first, then by id
    for fid in sorted((f for f in per if f not in bad and per[f]["hunks"]),
                      key=lambda f: (fb["rows"][f].cls != "M", -per[f]["totals"]["gross"], natural(f))):
        kept = [h for h in hunks if h not in reverted_parts()]
        if sum(h.added for h in kept) <= CYCLE_GROSS_WORDS and sum(h.bytes for h in kept) <= CYCLE_GROSS_BYTES:
            break
        bad.add(fid)
        depends_closure(bad, ledger, hunks, per)
    def compose():
        while True:
            revert = reverted_parts()
            moved_closure(revert, res)
            # a kept finding whose part must go back with a moved unit is reverted whole
            extra = {p.entry.finding for p in revert if p.entry is not None and p.entry.finding not in bad}
            if not extra:
                text = apply_edits(work_text, region_edits(res, revert, base_text, work_text))
                return revert, text, text.encode("utf-8")
            bad.update(extra)
            depends_closure(bad, ledger, hunks, per)

    def fence_delta(f):
        return sum(part_fences(h) for h in per[f]["hunks"])

    revert, text, data = compose()
    structure, recheck = [], []
    while len(data) - len(base_data) <= RAW_SIZE_LIMIT:
        again = analyze(base_data, base_text, data, text, fb, ledger)
        if again["code"] == EXIT["OK"]:
            break
        # A kept fix changed the structure of the text after it (an unmatched fence opens a code
        # block): fences are the only state carried across lines, so revert the earliest kept finding
        # whose own hunks change the fence count. Else revert the kept findings the re-check itself
        # names (their text, read in the restored context, fails). Then compose again.
        fences = sorted((f for f in per if f not in bad and per[f]["hunks"] and fence_delta(f)),
                        key=lambda f: per[f]["hunks"][0].k)
        named = sorted({h.claimant.finding for h in again["hunks"] if h.entry is None and h.claimant is not None}
                       | {f for f, p in again["per"].items() if p["status"] in ("OVER", "MINOR-EDIT")}, key=natural)
        named = [f for f in named if f in per and f not in bad]
        if fences:
            structure.append(fences[0])
            bad.add(fences[0])
        elif named:
            recheck += named
            bad.update(named)
        else:
            break
        depends_closure(bad, ledger, hunks, per)
        revert, text, data = compose()
    restored = len(data) - len(base_data) > RAW_SIZE_LIMIT
    if restored:
        data, text = base_data, base_text
        bad |= {fid for fid in fb["order"] if fb["rows"][fid].grade == "blocking"}
    if data != rev_data:
        atomic_write(args.revised, data)
    print(f"ENFORCE reverted={','.join(sorted(bad, key=natural)) or '-'} "
          f"hunks={','.join(f'h{h.k}' for h in sorted(revert, key=lambda h: h.k) if h.k) or '-'} "
          f"restored-baseline={'yes reason=raw-size' if restored else 'no'} "
          f"structure={','.join(structure) or '-'} recheck={','.join(recheck) or '-'} stray-fence-hunks={stray} line-breaks={breaks}")
    print("escalated-by-enforce: " + (" ".join(sorted(bad, key=natural)) or "none"))
    rev_data, rev_text = read_text(args.revised)
    final = analyze(base_data, base_text, rev_data, rev_text, fb, ledger)
    print("\n".join(render_report(final, fb, ledger, base_data, rev_data, ledger_data)))
    return final["code"]


def cmd_hash(args):
    data, _ = read_text(args.file)
    print(sha256(data))
    return EXIT["OK"]


def cmd_snapshot(args):
    spec_data, _ = read_text(args.spec)
    _, report_text = read_text(args.report)
    fb = parse_fixbudget(report_text)
    if sha256(spec_data) != fb["sha"]:
        fail("HASH", "STALE-BASE: the spec changed since this review (sha256 differs from reviewed_sha256)")
    target = Path(args.report).parent / ".fixcheck" / f"base-{fb['review']}.md"
    atomic_write(target, spec_data)
    print(f"snapshot: {target}")
    return EXIT["OK"]


def cmd_check(args):
    base_data, base_text, rev_data, rev_text, fb, ledger, ledger_data = load_check_inputs(args)
    if args.enforce:
        return enforce(args, base_data, base_text, rev_data, rev_text, fb, ledger, ledger_data)
    res = analyze(base_data, base_text, rev_data, rev_text, fb, ledger)
    print("\n".join(render_report(res, fb, ledger, base_data, rev_data, ledger_data)))
    return res["code"]


def build_parser():
    parser = argparse.ArgumentParser(prog="fixcheck.py", description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("hash", help="print the sha256 of a file")
    p.add_argument("--file", required=True)
    p.set_defaults(func=cmd_hash)
    p = sub.add_parser("snapshot", help="save the reviewed spec as <report dir>/.fixcheck/base-<N>.md")
    p.add_argument("--spec", required=True)
    p.add_argument("--report", required=True)
    p.set_defaults(func=cmd_snapshot)
    p = sub.add_parser("check", help="score the fix against the report's fixbudget block")
    p.add_argument("--baseline", required=True)
    p.add_argument("--revised", required=True)
    p.add_argument("--report", required=True)
    p.add_argument("--ledger")
    p.add_argument("--enforce", action="store_true", help="revert what is over budget, then re-check")
    p.set_defaults(func=cmd_check)
    return parser


def main(argv=None):
    try:
        args = build_parser().parse_args(argv)
    except SystemExit as exc:
        return exc.code if isinstance(exc.code, int) else EXIT["USAGE"]
    try:
        return args.func(args)
    except FixcheckError as exc:
        print(f"error: {exc.message}", file=sys.stderr)
        print(f"FIXCHECK exit={exc.code}")
        return exc.code
    except Exception as exc:  # any uncaught error is an internal error, exit 70
        print(f"internal error: {type(exc).__name__}: {exc}", file=sys.stderr)
        print(f"FIXCHECK exit={EXIT['INTERNAL']}")
        return EXIT["INTERNAL"]


if __name__ == "__main__":
    sys.exit(main())
