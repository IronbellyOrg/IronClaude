"""Shared helpers for the PN3 offline phases (C5 locate, C9.3 parsing, source list)."""
import hashlib
import json
import pathlib
import re

SP = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad")
P11 = SP / "p11"
RUNS = P11 / "runs"
AUD2 = SP / "p12/baseline-audit2"
AB = SP / "p13/ab3"
CAT = SP / "p13/catalog"
D = ".dev/orca-command-refactor"
SPECREL = f"{D}/specs/orca-worker-contract-spec.md"
ORIG = SP / "exp346/.dev/experiments/346-validation/phase2/S1/inputs/repo-overlay" / SPECREL
SPEC_SHA = "d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d"
REV = f"{D}/review"

RUN_NAMES = [f"a{a}-r{r}" for a in (2, 3) for r in range(1, 7)]  # 12 primary occasions
ARM1 = [f"a1-r{r}" for r in (1, 2, 3)]
ALL_RUNS = ARM1 + RUN_NAMES


def r1_path(run):
    name = "spec-panel.md" if run.startswith("a1") else "round1.md"
    return RUNS / run / "ws" / REV / name


def final_spec(run):
    return RUNS / run / "ws" / SPECREL


def sources():
    """Ordered list of dict(source, run, step, report, doc ('original'|'final'), doc_path)."""
    out = []
    for run in ALL_RUNS:
        out.append(dict(source=f"{run}/R1", run=run, step="R1", report=r1_path(run), doc="original", doc_path=ORIG))
    for run in ALL_RUNS:
        out.append(dict(source=f"{run}/AUD", run=run, step="AUD", doc="final", doc_path=final_spec(run),
                        report=RUNS / run / "aud/ws" / REV / "audit.md"))
    for r in range(1, 7):
        run = f"a3-r{r}"
        out.append(dict(source=f"{run}/AUD2", run=run, step="AUD2", doc="final", doc_path=final_spec(run),
                        report=AUD2 / run / "ws" / REV / "audit.md"))
    return out


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


# ---------------------------------------------------------------- C5
def flat(s):
    return " ".join(s.split())


def locate(text, quote):
    """Every occurrence of flat(quote) in whitespace-flattened text as half-open 0-based line ranges."""
    q = flat(quote)
    if not q:
        return []
    chars, line_of = [], []
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
    out = []
    i = norm.find(q)
    while i != -1:
        out.append((line_of[i], line_of[i + len(q) - 1] + 1))
        i = norm.find(q, i + 1)
    return out


# ---------------------------------------------------------------- C9.3
THEMES = [("T3", r"AC-0\.4|\bP0\b|Phase 0"),
          ("T2", r"WC-4|contract (?:file )?(?:path|location)|--output"),
          ("T1", r"AC-1\.[12]|/sc:load|\bP1\b|Phase 1|command counts?|\b36\b")]
EXCL = {"FR", "AC", "SHA", "WC", "INV", "SPEC", "CMD", "P", "GC", "SA", "NFR", "D"}
ID_TOKEN = r"\b(?:R\d-)?[A-Z]{1,4}-?\d+\b"
IDS_LINE = r"(?im)^\W*(?:\*\*)?(?:Reviser brief\W*)?Blocking (?:finding )?ids?\b[^:\n]{0,60}:\s*(.+)$"
CITE = (r"(?i)(?:\b(?:spec(?:\.md)?|S)\s*:\s*|\blines?\s+|\bL(?=\d))"
        r"(\d{1,3}(?:\s*[-–]\s*\d{1,3})?(?:\s*(?:,|and)\s*\d{1,3}(?:\s*[-–]\s*\d{1,3})?)*)(?![\d.])")


def ids_from(report_path):
    t = pathlib.Path(report_path).read_text(errors="ignore")
    m = re.findall(IDS_LINE, t)
    if m:
        return m[-1].strip(" *.")
    sec = re.search(r"(?ms)^#+\s*Reviser brief[^\n]*\n(.*?)(?=^#+ |^verdict:|\Z)", t)
    if not sec:
        return None
    para = "\n".join([l for l in sec.group(1).splitlines() if l.strip()][:3])
    toks = []
    for x in re.findall(r"\b(?:R\d-)?[A-Z]{1,2}-?\d+\b", para):
        if x not in toks and not x.startswith(("FR", "AC", "SHA")):
            toks.append(x)
    return ", ".join(toks) or None


def parse_ids(raw):
    if raw is None or re.match(r"(?i)^\W*none\b", raw):
        return []
    raw = re.split(r"\.\s|\.$|\(|;|\n", raw, maxsplit=1)[0].replace("*", "")
    out = []
    for t in re.findall(ID_TOKEN, raw):
        lead = re.match(r"[A-Za-z]+", t.split("-", 1)[-1] if re.match(r"R\d-", t) else t)
        letters = re.match(r"(?:R\d-)?([A-Z]+)", t).group(1)
        if letters in EXCL:
            continue
        if t not in out:
            out.append(t)
    return out


def verdict_of(text):
    m = re.findall(r"(?im)^\W*verdict\W*:?\s*\**\s*(PASS|FAIL)", text)
    return m[-1].upper() if m else None


def find_section(text, fid, start=0):
    lines = text.splitlines()
    e = re.escape(fid) + r"(?![\w-])"
    pats = [("heading", re.compile(r"^\s*#{2,6}\s*(?:\*\*)?" + e)),
            ("bold", re.compile(r"^\s*(?:[-*]\s*)?\*\*" + e)),
            ("table", re.compile(r"^\s*\|\s*(?:\*\*)?" + e)),
            ("bracket", re.compile(r"^\s*[-*]\s*\[" + e.replace("(?![\\w-])", "") + r"\]"))]  # arm-1 extension
    stop = re.compile(r"^\s*#{1,6}\s|^\s*(?:[-*]\s*)?\*\*(?:R\d-)?[A-Z]{1,5}-?\d+\b")
    for kind, p in pats:
        for i, l in enumerate(lines):
            if i >= start and p.match(l):
                if kind in ("table", "bracket"):
                    return dict(kind=kind, line=i, heading=l, body="")
                j = i + 1
                while j < len(lines) and not stop.match(lines[j]):
                    j += 1
                return dict(kind=kind, line=i, heading=l, body="\n".join(lines[i + 1:j]))
    return None


def tag(heading, body):
    for src in (heading, next((l for l in body.splitlines() if l.strip()), "")):
        for name, rx in THEMES:
            if re.search(rx, src, re.I):
                return name
    return "other"


def cited(text):
    out = []
    for m in re.finditer(CITE, text):
        for part in re.split(r"\s*(?:,|and)\s*", m.group(1)):
            mm = re.match(r"(\d+)(?:\s*[-–]\s*(\d+))?$", part.strip())
            if not mm:
                continue
            a = int(mm.group(1))
            b = int(mm.group(2)) if mm.group(2) else a
            rng = range(a, b + 1) if 0 <= b - a <= 30 else [a, b]
            out.extend(n for n in rng if 1 <= n <= 400)
    seen = []
    for n in out:
        if n not in seen:
            seen.append(n)
    return seen
