"""C9.3 prose parsing of Stage 2 style reports (verbatim definitions from the shared contract)."""
import re, pathlib
THEMES = [("T3", r"AC-0\.4|\bP0\b|Phase 0"),
          ("T2", r"WC-4|contract (?:file )?(?:path|location)|--output"),
          ("T1", r"AC-1\.[12]|/sc:load|\bP1\b|Phase 1|command counts?|\b36\b")]   # re.I; first match wins
EXCL = {"FR", "AC", "SHA", "WC", "INV", "SPEC", "CMD", "P", "GC", "SA", "NFR", "D"}
ID_TOKEN = r"\b(?:R\d-)?[A-Z]{1,4}-?\d+\b"
IDS_LINE = r"(?im)^\W*(?:\*\*)?(?:Reviser brief\W*)?Blocking (?:finding )?ids?\b[^:\n]{0,60}:\s*(.+)$"
CITE = (r"(?i)(?:\b(?:spec(?:\.md)?|S)\s*:\s*|\blines?\s+|\bL(?=\d))"
        r"(\d{1,3}(?:\s*[-–]\s*\d{1,3})?(?:\s*(?:,|and)\s*\d{1,3}(?:\s*[-–]\s*\d{1,3})?)*)(?![\d.])")

def ids_from(path):
    t = pathlib.Path(path).read_text(errors="ignore")
    m = re.findall(IDS_LINE, t)
    if m: return m[-1].strip(" *.")
    sec = re.search(r"(?ms)^#+\s*Reviser brief[^\n]*\n(.*?)(?=^#+ |^verdict:|\Z)", t)
    if not sec: return None
    para = "\n".join([l for l in sec.group(1).splitlines() if l.strip()][:3])
    toks = []
    for x in re.findall(r"\b(?:R\d-)?[A-Z]{1,2}-?\d+\b", para):
        if x not in toks and not x.startswith(("FR", "AC", "SHA")): toks.append(x)
    return ", ".join(toks) or None

def parse_ids(raw):
    if raw is None or re.match(r"(?i)^\W*none\b", raw): return []
    m = re.search(r"\.\s|\.$|\(|;|\n", raw)
    if m: raw = raw[:m.start()]
    raw = raw.replace("*", "")
    out = []
    for x in re.findall(ID_TOKEN, raw):
        letters = re.match(r"(?:R\d-)?([A-Z]+)", x).group(1)
        if letters in EXCL: continue
        if x not in out: out.append(x)
    return out

def find_section(text, fid):
    lines = text.split("\n")
    pats = [r"^\s*#{2,6}\s*(?:\*\*)?", r"^\s*(?:[-*]\s*)?\*\*", r"^\s*\|\s*(?:\*\*)?"]
    for pi, pre in enumerate(pats):
        rx = re.compile(pre + re.escape(fid) + r"(?![\w-])")
        for i, ln in enumerate(lines):
            if rx.match(ln):
                if pi == 2: return ln, "", i + 1, i + 1
                j = i + 1
                while j < len(lines) and not re.match(r"^\s*#{1,6}\s", lines[j]) and not re.match(r"^\s*(?:[-*]\s*)?\*\*[A-Z]", lines[j]):
                    j += 1
                return ln, "\n".join(lines[i + 1:j]), i + 1, j
    return None

def tag(heading, body):
    def th(s):
        for name, rx in THEMES:
            if re.search(rx, s, re.I): return name
        return None
    t = th(heading)
    if t: return t
    for ln in body.split("\n"):
        if ln.strip():
            t = th(ln)
            if t: return t
            break
    return "other"

def cited(text):
    out = set()
    for m in re.finditer(CITE, text):
        for part in re.split(r"\s*(?:,|and)\s*", m.group(1)):
            mm = re.match(r"(\d{1,3})(?:\s*[-–]\s*(\d{1,3}))?$", part.strip())
            if not mm: continue
            a = int(mm.group(1)); b = int(mm.group(2)) if mm.group(2) else a
            rng = range(a, b + 1) if 0 <= b - a <= 30 else [a, b]
            out.update(n for n in rng if 1 <= n <= 400)
    return sorted(out)
