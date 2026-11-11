#!/usr/bin/env python3
"""Pure functions: blocking-id parsing, finding sections, theme tags, cited lines (plan section B4).

No I/O except blocking_findings()/ids_from() reading a report file."""
import pathlib
import re

THEMES = [("T3", r"AC-0\.4|\bP0\b|Phase 0"),
          ("T2", r"WC-4|contract (?:file )?(?:path|location)|--output"),
          ("T1", r"AC-1\.[12]|/sc:load|\bP1\b|Phase 1|command counts?|\b36\b")]   # re.I; first match wins
EXCL = {"FR", "AC", "SHA", "WC", "INV", "SPEC", "CMD", "P", "GC", "SA", "NFR", "D"}
ID_TOKEN = r"\b(?:R\d-)?[A-Z]{1,4}-?\d+(?:-\d+)?\b"
CITE = (r"(?i)(?:\b(?:spec(?:\.md)?|S)\s*:\s*|\blines?\s+|\bL(?=\d))"
        r"(\d{1,3}(?:\s*[-–]\s*\d{1,3})?(?:\s*(?:,|and)\s*\d{1,3}(?:\s*[-–]\s*\d{1,3})?)*)(?![\d.])")
BOLD_ID = r"^\s*(?:[-*]\s*)?\*\*(?:R\d-)?[A-Z]{1,4}-?\d+\b"
IDS_RE = r"(?im)^\W*(?:\*\*)?(?:Reviser brief\W*)?Blocking (?:finding )?ids?\b[^:\n]{0,60}:\s*(.+)$"


def ids_from(report_path):
    """Raw text of the blocking-ids line of a report (None if absent)."""
    t = pathlib.Path(report_path).read_text(errors="ignore")
    m = re.findall(IDS_RE, t)
    if m:
        return m[-1].strip(" *.")
    sec = re.search(r"(?ms)^#+\s*Reviser brief[^\n]*\n(.*?)(?=^#+ |^verdict:|\Z)", t)
    if not sec:
        return None
    inl = re.search(r"(?im)^\W*Blocking findings\W*:[ \t]*([^\n]*\b[A-Z]{1,2}-?\d+[^\n]*)$", sec.group(1))
    if inl:  # inline list "Blocking findings: N-1." (fix 2026-11-10, b2h-r4 R2 pulled minors/mediums)
        itoks = []
        for x in re.findall(r"\b(?:R\d-)?[A-Z]{1,2}-?\d+\b", inl.group(1)):
            if x not in itoks and not x.startswith(("FR", "AC", "SHA")):
                itoks.append(x)
        if itoks:
            return ", ".join(itoks)
    bl = re.search(r"(?ims)^\W*Blocking findings\W*:\s*\n(.*)\Z", sec.group(1))
    if bl:  # explicit blocking list wins over ids named in "leave alone" prose (fix 2026-11-10, b2-r3 R2 mis-parse)
        btoks = []
        for x in re.findall(r"(?m)^\s*[-*]\s*\**((?:R\d-)?[A-Z]{1,2}-?\d+)\b", bl.group(1)):
            if x not in btoks and not x.startswith(("FR", "AC", "SHA")):
                btoks.append(x)
        if btoks:
            return ", ".join(btoks)
    para = "\n".join([ln for ln in sec.group(1).splitlines() if ln.strip()][:3])
    toks = []
    for x in re.findall(r"\b(?:R\d-)?[A-Z]{1,2}-?\d+\b", para):
        if x not in toks and not x.startswith(("FR", "AC", "SHA")):
            toks.append(x)
    return ", ".join(toks) or None


def parse_ids(raw):
    if raw is None or re.match(r"(?i)^\W*none\b", raw):
        return []
    m = re.search(r"\.\s|\.$|\(|;|\n", raw)
    if m:
        raw = raw[:m.start()]
    raw = raw.replace("*", "")
    out = []
    for tok in re.findall(ID_TOKEN, raw):
        lead = re.split(r"[\d-]", tok, maxsplit=1)[0]
        if lead in EXCL or tok in out:
            continue
        out.append(tok)
    return out


def find_section(text, fid):
    lines = text.splitlines()
    e = re.escape(fid) + r"(?![\w-])"
    pats = [("heading", re.compile(r"^\s*#{2,6}\s*(?:\*\*)?" + e)),
            ("bold", re.compile(r"^\s*(?:[-*]\s*)?\*\*" + e)),
            ("row", re.compile(r"^\s*\|\s*(?:\*\*)?" + e))]
    bold_id = re.compile(BOLD_ID)
    for kind, pat in pats:
        for i, ln in enumerate(lines):
            if not pat.match(ln):
                continue
            heading = ln.strip()
            if kind == "row":
                return heading, ""
            body = []
            if kind == "heading":
                k = len(re.match(r"^\s*(#+)", ln).group(1))
            for ln2 in lines[i + 1:]:
                if kind == "heading":
                    hm = re.match(r"^\s*(#+)\s", ln2)
                    if (hm and len(hm.group(1)) <= k) or bold_id.match(ln2):
                        break
                else:
                    if re.match(r"^#{1,6} ", ln2) or bold_id.match(ln2):
                        break
                body.append(ln2)
            return heading, "\n".join(body).strip("\n")
    return None, None


def tag(heading, body):
    texts = []
    if heading:
        texts.append(heading)
    for t in texts:
        for name, pat in THEMES:
            if re.search(pat, t, re.I):
                return name
    first = next((ln for ln in (body or "").splitlines() if ln.strip()), None)
    if first:
        for name, pat in THEMES:
            if re.search(pat, first, re.I):
                return name
    return "other"


def cited(text):
    out = set()
    for m in re.finditer(CITE, text or ""):
        for part in re.split(r"\s*(?:,|and)\s*", m.group(1).strip()):
            rng = re.split(r"\s*[-–]\s*", part)
            try:
                a = int(rng[0])
                b = int(rng[1]) if len(rng) > 1 else a
            except ValueError:
                continue
            if b < a or b - a > 30:
                b = a
            out.update(range(a, b + 1))
    return {n for n in out if 1 <= n <= 400}


def jaccard(a, b):
    a, b = set(a), set(b)
    return len(a & b) / len(a | b) if (a | b) else 0.0


def same_defect(f, g):
    return f["theme"] == g["theme"] and jaccard(f["cited"], g["cited"]) >= 0.5


def matches_audit(f, a):
    if f["theme"] == a["theme"] and f["theme"] != "other" and (set(f["cited"]) & set(a["cited"])):
        return True
    return f["theme"] == "other" and a["theme"] == "other" and jaccard(f["cited"], a["cited"]) >= 0.5


def verdict_of(text):
    vs = re.findall(r"verdict:\s*\**\s*(PASS|FAIL|INCOMPLETE)", text, re.I)
    return vs[-1].upper() if vs else "NONE"


def blocking_findings(path, ids=None):
    """Blocking findings of a report. `ids` overrides parsing (manual ids). [] unless verdict FAIL."""
    t = pathlib.Path(path).read_text(errors="ignore")
    if verdict_of(t) != "FAIL":
        return []
    idl = list(ids) if ids else parse_ids(ids_from(path))
    out = []
    for fid in idl:
        heading, body = find_section(t, fid)
        out.append({"id": fid, "heading": heading, "body": body,
                    "theme": tag(heading, body),
                    "cited": cited((heading or "") + "\n" + (body or ""))})
    return out
