"""Pure functions: parse blocking ids, find finding sections, tag themes, match audit findings (plan B4)."""
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
    t = pathlib.Path(report_path).read_text(errors="ignore")
    m = re.findall(IDS_RE, t)
    if m:
        return m[-1].strip(" *.")
    sec = re.search(r"(?ms)^#+\s*Reviser brief[^\n]*\n(.*?)(?=^#+ |^verdict:|\Z)", t)
    if not sec:
        return None
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
        lead = re.split(r"[\d-]", tok, maxsplit=1)[0]
        if lead in EXCL or tok in out:
            continue
        out.append(tok)
    return out


def find_section(text, fid):
    lines = text.splitlines()
    e = re.escape(fid) + r"(?![\w-])"
    pats = [("h", re.compile(r"^\s*(#{2,6})\s*(?:\*\*)?" + e)),
            ("b", re.compile(r"^\s*(?:[-*]\s*)?\*\*" + e)),
            ("t", re.compile(r"^\s*\|\s*(?:\*\*)?" + e))]
    bold = re.compile(BOLD_ID)
    for kind, pat in pats:
        for i, ln in enumerate(lines):
            m = pat.match(ln)
            if not m:
                continue
            body = []
            if kind == "h":
                k = len(m.group(1))
                for ln2 in lines[i + 1:]:
                    hm = re.match(r"^\s*(#{1,6})\s", ln2)
                    if (hm and len(hm.group(1)) <= k) or bold.match(ln2):
                        break
                    body.append(ln2)
            elif kind == "b":
                for ln2 in lines[i + 1:]:
                    if re.match(r"^#{1,6} ", ln2) or bold.match(ln2):
                        break
                    body.append(ln2)
            return ln.strip(), "\n".join(body)
    return None, None


def tag(heading, body):
    heads = [heading or ""]
    first = next((ln for ln in (body or "").splitlines() if ln.strip()), "")
    for cand in (heads[0], first):
        for name, rx in THEMES:
            if re.search(rx, cand, re.I):
                return name
    return "other"


def cited(text):
    out = set()
    for m in re.finditer(CITE, text or ""):
        for part in re.split(r"\s*(?:,|and)\s*", m.group(1)):
            mm = re.match(r"(\d+)(?:\s*[-–]\s*(\d+))?$", part.strip())
            if not mm:
                continue
            a = int(mm.group(1))
            b = int(mm.group(2)) if mm.group(2) else a
            rng = [a] if (b < a or b - a > 30) else range(a, b + 1)
            out.update(n for n in rng if 1 <= n <= 400)
    return out


def jaccard(a, b):
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def same_defect(f, g):
    return f["theme"] == g["theme"] and jaccard(f["cited"], g["cited"]) >= 0.5


def matches_audit(f, a):
    if f["theme"] == a["theme"] and f["theme"] != "other" and (f["cited"] & a["cited"]):
        return True
    return f["theme"] == "other" and a["theme"] == "other" and jaccard(f["cited"], a["cited"]) >= 0.5


def verdict_of(text):
    vs = re.findall(r"verdict:\s*\**\s*(PASS|FAIL|INCOMPLETE)", text, re.I)
    return vs[-1].upper() if vs else "NONE"


def blocking_findings(path):
    text = pathlib.Path(path).read_text(errors="ignore")
    if verdict_of(text) != "FAIL":
        return []
    out = []
    for fid in parse_ids(ids_from(path)):
        heading, body = find_section(text, fid)
        out.append({"id": fid, "heading": heading, "body": body, "theme": tag(heading, body),
                    "cited": cited((heading or "") + "\n" + (body or ""))})
    return out
