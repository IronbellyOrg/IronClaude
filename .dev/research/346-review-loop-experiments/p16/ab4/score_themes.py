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


_ID_LIST_TOK = r"\b(?:R\d-)?[A-Z]{1,2}-?\d+\b"
# Section start of the Reviser brief: a markdown heading OR a banner line ("=== REVISER BRIEF ===", fix ab4 item 4c).
BRIEF_SEC_RE = r"(?ims)^(?:#+|={3,})[ \t]*Reviser brief[^\n]*\n(.*?)(?=^#+ |^={3,}|^verdict:|\Z)"
# Inline label lines: "Blocking findings: B1, B2", "Blocking: F1, F2", "- Open blocking findings to escalate to the user: N2 (open) and N4 (new).",
# "Blocking findings open: 1 (B2, new in round 3)", "Open blocking findings: N3. Resolved: N2."  (review-3 reports have no Reviser brief.)
INLINE_RE = re.compile(r"(?im)^(?!\s*\|)\W*(?:\*\*)?(?:Open\s+)?Blocking(?:\s+findings?)?(?:\s+open)?(?:\s+to\s+escalate[^:\n]{0,40})?\W{0,3}:\s*(.+)$")


def _tokens(raw):
    toks = []
    for x in re.findall(_ID_LIST_TOK, raw):
        if x not in toks and not x.startswith(("FR", "AC", "SHA")):
            toks.append(x)
    return toks


def inline_ids(raw):
    """Ids named on one inline label line: cut at the first sentence end, ids outside parentheses first, else the ids inside them."""
    raw = raw.replace("*", "")
    m = re.search(r"\.\s|\.$|;", raw)
    if m:
        raw = raw[:m.start()] if raw[:m.start()].strip() else raw
    outside = re.sub(r"\([^)]*\)", " ", raw)
    toks = _tokens(outside)
    if toks:
        return toks
    inside = " ".join(re.findall(r"\(([^)]*)\)", raw))
    return _tokens(inside)


def ids_from(report_path):
    """Raw text of the blocking-ids line of a report (None if absent)."""
    t = pathlib.Path(report_path).read_text(errors="ignore")
    for cand in reversed(re.findall(IDS_RE, t)):
        # a match counts only if it names ids or says none (fix ab4: "Reviser brief (blocking finding ids only; ...): revise only ..." is prose)
        if re.match(r"(?i)^\W*none\b", cand) or parse_ids(cand):
            return cand.strip(" *.")
    sec = re.search(BRIEF_SEC_RE, t)
    if sec:
        body = sec.group(1)
        inl = re.search(r"(?im)^\W*Blocking findings\W*:[ \t]*([^\n]*\b[A-Z]{1,2}-?\d+[^\n]*)$", body)
        if inl:  # inline list "Blocking findings: N-1." (fix 2026-11-10, b2h-r4 R2 pulled minors/mediums)
            itoks = _tokens(inl.group(1))
            if itoks:
                return ", ".join(itoks)
        bl = re.search(r"(?ims)^\W*Blocking findings\W*:\s*\n(.*)\Z", body)
        if bl:  # explicit blocking list wins over ids named in "leave alone" prose (fix 2026-11-10, b2-r3 R2 mis-parse)
            btoks = []
            for x in re.findall(r"(?m)^\s*[-*]\s*\**((?:R\d-)?[A-Z]{1,2}-?\d+)\b", bl.group(1)):
                if x not in btoks and not x.startswith(("FR", "AC", "SHA")):
                    btoks.append(x)
            if btoks:
                return ", ".join(btoks)
        para = "\n".join([ln for ln in body.splitlines() if ln.strip()][:3])
        toks = _tokens(para)
        if toks:
            return ", ".join(toks)
    # no ids line and no usable Reviser brief: the last inline label line that names ids (review-3 reports, "Blocking: F1..F4")
    last = None
    for mm in INLINE_RE.finditer(t):
        toks = inline_ids(mm.group(1))
        if toks:
            last = toks
    return ", ".join(last) if last else None


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


# ---------------------------------------------------------------- finding blocks, cut and cleaned at source (ab4 item 4a)
# find_section() slices a finding to the next heading or bold id, so the LAST finding of a report ran on into the banner sections
# ("=== ARCHITECTURE ANALYSIS ===", guard tables, follow-up candidates, Reviser brief). cut_block() ends a finding there;
# clean_body() drops reviewer advice (recommendation / option / priority / origin lines and their indented children) so a verifier
# sees only the finding: its texts and its stated wrong outcome.
BANNER_RE = re.compile(r"^\s*={3,}")
NONFINDING_TITLE = (r"reviser brief|follow-up|architecture analysis|requirements analysis|adversarial analysis|guard condition|"
                    r"pipeline dimensional|consensus|synthesis|quality metrics|minor notes|expert notes|expert analysis|coverage|"
                    r"priority-ranked|noted, unactioned|medium|decisions|verdict summary|whittaker findings|counts")
CUT_RE = re.compile(rf"(?i)^\s*(?:#{{1,6}}\s*)(?:\*\*)?\s*(?:={{3,}}\s*)?(?:{NONFINDING_TITLE})\b|^\s*#{{1,6}}\s*={{3,}}|^\s*verdict\s*:|^\W*Reviser brief\b|^\W*Blocking finding ids?\b")
DROP_RE = re.compile(r"(?i)^\s*(?:[-*]\s*)?(?:\*\*)?\s*(recommendation|rationale|experts?|priority|quality impact|why blocking|suggested fix|"
                     r"proposed fix|fix|remedy|resolution|options?|origin|verification status|reviser brief(?: note)?)\b|^\s*(?:[-*]\s*)?\([a-d]\)\s")


def cut_block(lines):
    """Lines of one finding up to (not including) the first banner / non-finding section line."""
    out = []
    for ln in lines:
        if BANNER_RE.match(ln) or CUT_RE.match(ln):
            break
        out.append(ln)
    while out and not out[-1].strip():
        out.pop()
    return out


def clean_body(lines):
    """Drop advice lines and their indented children (a dropped bullet's sub-bullets and wrapped lines)."""
    out, skip_indent = [], None
    for ln in lines:
        ind = len(ln) - len(ln.lstrip())
        if skip_indent is not None:
            if not ln.strip() or ind > skip_indent:
                continue
            skip_indent = None
        if DROP_RE.match(ln):
            skip_indent = ind
            continue
        out.append(ln)
    while out and not out[-1].strip():
        out.pop()
    return out


def finding_block(text, fid, clean=False):
    """(heading, body) of finding fid with the structural cut; clean=True also drops advice lines. (None, None) if absent."""
    h, b = find_section(text, fid)
    if h is None:
        return None, None
    lines = cut_block((b or "").splitlines())
    if clean:
        lines = clean_body(lines)
    return h, "\n".join(lines)


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


def blocking_findings(path, ids=None, cut=False):
    """Blocking findings of a report. `ids` overrides parsing (manual ids). [] unless verdict FAIL.
    cut=True ends each finding at the first banner / non-finding section (used by merge; audit scoring keeps the ab1 slicing)."""
    t = pathlib.Path(path).read_text(errors="ignore")
    if verdict_of(t) != "FAIL":
        return []
    idl = list(ids) if ids else parse_ids(ids_from(path))
    out = []
    for fid in idl:
        heading, body = finding_block(t, fid) if cut else find_section(t, fid)
        out.append({"id": fid, "heading": heading, "body": body,
                    "theme": tag(heading, body),
                    "cited": cited((heading or "") + "\n" + (body or ""))})
    return out
