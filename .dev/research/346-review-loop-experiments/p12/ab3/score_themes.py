"""Finding parsing and theme scoring (pure functions), plan section B4.

Tags are a keyword proxy for the three audit themes T1, T2, T3 (or "other").
"""
import pathlib
import re

THEMES = [("T3", r"AC-0\.4|\bP0\b|Phase 0"),
          ("T2", r"WC-4|contract (?:file )?(?:path|location)|--output"),
          ("T1", r"AC-1\.[12]|/sc:load|\bP1\b|Phase 1|command counts?|\b36\b")]   # re.I; first match wins
EXCL = {"FR", "AC", "SHA", "WC", "INV", "SPEC", "CMD", "P", "GC", "SA", "NFR", "D"}
ID_TOKEN = r"\b(?:R\d-)?[A-Z]{1,4}-?\d+(?:-\d+)?\b"
CITE = (r"(?i)(?:\b(?:spec(?:\.md)?|S)\s*:\s*|\blines?\s+|\bL(?=\d))"
        r"(\d{1,3}(?:\s*[-–]\s*\d{1,3})?(?:\s*(?:,|and)\s*\d{1,3}(?:\s*[-–]\s*\d{1,3})?)*)(?![\d.])")

IDS_LINE = r"(?im)^\W*(?:\*\*)?(?:Reviser brief\W*)?Blocking (?:finding )?ids?\b[^:\n]{0,60}:\s*(.+)$"
BOLD_ID_LINE = r"^\s*(?:[-*]\s*)?\*\*(?:R\d-)?[A-Z]{1,4}-?\d+\b"


def ids_from(report_path):
    """Raw text of the blocking-ids line (p11 logic with the B2-item-4 regex), or None."""
    t = pathlib.Path(report_path).read_text(errors="ignore")
    m = re.findall(IDS_LINE, t)
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
    cut = re.split(r"\.\s|\.$|\(|;|\n", raw, maxsplit=1)[0]
    cut = cut.replace("*", "")
    out = []
    for tok in re.findall(ID_TOKEN, cut):
        if re.match(r"[A-Z]+", tok).group(0) in EXCL:
            continue
        if tok not in out:
            out.append(tok)
    return out


def find_section(text, fid):
    lines = text.split("\n")
    tail = re.escape(fid) + r"(?![\w-])"
    pats = [("h", rf"^\s*(#{{2,6}})\s*(?:\*\*)?{tail}"),
            ("b", rf"^\s*(?:[-*]\s*)?\*\*{tail}"),
            ("t", rf"^\s*\|\s*(?:\*\*)?{tail}")]
    for kind, pat in pats:
        for i, ln in enumerate(lines):
            m = re.match(pat, ln)
            if not m:
                continue
            if kind == "t":
                return ln, ""
            body = []
            if kind == "h":
                k = len(m.group(1))
                for nl in lines[i + 1:]:
                    hm = re.match(r"^(#{1,6})\s", nl)
                    if hm and len(hm.group(1)) <= k:
                        break
                    if re.match(BOLD_ID_LINE, nl):
                        break
                    body.append(nl)
            else:
                for nl in lines[i + 1:]:
                    if re.match(r"^#{1,6} ", nl) or re.match(BOLD_ID_LINE, nl):
                        break
                    body.append(nl)
            return ln, "\n".join(body)
    return None, None


def tag(heading, body):
    for name, pat in THEMES:
        if heading and re.search(pat, heading, re.I):
            return name
    first = next((ln for ln in (body or "").split("\n") if ln.strip()), "")
    for name, pat in THEMES:
        if re.search(pat, first, re.I):
            return name
    return "other"


def cited(text):
    out = set()
    for m in re.finditer(CITE, text or ""):
        for part in re.split(r"\s*(?:,|and)\s*", m.group(1)):
            r = re.match(r"(\d+)(?:\s*[-–]\s*(\d+))?$", part.strip())
            if not r:
                continue
            a = int(r.group(1))
            b = int(r.group(2)) if r.group(2) else a
            if b < a or b - a > 30:
                b = a
            out.update(range(a, b + 1))
    return {n for n in out if 1 <= n <= 400}


def _jaccard(a, b):
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def same_defect(f, g):
    return f["theme"] == g["theme"] and _jaccard(f["cited"], g["cited"]) >= 0.5


def matches_audit(f, a):
    if f["theme"] == a["theme"] and f["theme"] != "other":
        return bool(f["cited"] & a["cited"])
    if f["theme"] == "other" and a["theme"] == "other":
        return _jaccard(f["cited"], a["cited"]) >= 0.5
    return False


def verdict_of(text):
    vs = re.findall(r"verdict:\s*\**\s*(PASS|FAIL|INCOMPLETE)", text, re.I)
    return vs[-1].upper() if vs else "NONE"


def _override(path, fid, th, overrides):
    """Overrides: {"<run>/<file>/<id>": "T2"}, or {"<run>/<subdir>/<file>/<id>": ...} with the directory after the run
    (aud, aud2, ws) to tell two audits of one run apart."""
    parts = pathlib.Path(path).parts
    fname = parts[-1]
    runi = next((i for i, x in enumerate(parts) if re.fullmatch(r"[ab]\d?h?-r\d+", x)), None)
    if runi is None:
        return th
    run, sub = parts[runi], (parts[runi + 1] if runi + 1 < len(parts) else "")
    for key in (f"{run}/{sub}/{fname}/{fid}", f"{run}/{fname}/{fid}"):
        if key in overrides:
            return overrides[key]
    return th


def blocking_findings(path, overrides=None, ids=None):
    """Blocking findings of a FAIL report.  `ids` (manual setids) replaces the parsed ids."""
    text = pathlib.Path(path).read_text(errors="ignore")
    if verdict_of(text) != "FAIL":
        return []
    out = []
    for fid in (list(ids) if ids is not None else parse_ids(ids_from(path))):
        heading, body = find_section(text, fid)
        th = tag(heading, body) if heading is not None else "other"
        if overrides:
            th = _override(path, fid, th, overrides)
        out.append({"id": fid, "heading": heading, "body": body, "theme": th,
                    "cited": cited((heading or "") + "\n" + (body or ""))})
    return out
