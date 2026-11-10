"""Shared contract C9.3: prose parsing of Stage 2 style reports (audits and old reports). Standard library only."""
import pathlib, re

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
    for tok in re.findall(ID_TOKEN, raw):
        letters = re.match(r"(?:R\d-)?([A-Z]+)", tok).group(1)
        if letters in EXCL:
            continue
        if tok not in out:
            out.append(tok)
    return out


def find_section(text, fid):
    lines = text.splitlines()
    f = re.escape(fid) + r"(?![\w-])"
    pats = [rf"^\s*#{{2,6}}\s*(?:\*\*)?{f}", rf"^\s*(?:[-*]\s*)?\*\*{f}", rf"^\s*\|\s*(?:\*\*)?{f}"]
    for k, pat in enumerate(pats):          # headings first, then bold ids, then table rows
        for i, ln in enumerate(lines):
            if re.match(pat, ln):
                if k == 2:
                    return ln, ""
                body = []
                for ln2 in lines[i + 1:]:
                    if re.match(r"^\s*#{1,6}\s", ln2) or re.match(r"^\s*(?:[-*]\s*)?\*\*[A-Z][A-Za-z0-9-]*[.:)\s]", ln2):
                        break
                    body.append(ln2)
                return ln, "\n".join(body)
    return None


def tag(heading, body):
    for t, rx in THEMES:
        if re.search(rx, heading or "", re.I):
            return t
    first = next((l for l in (body or "").splitlines() if l.strip()), "")
    for t, rx in THEMES:
        if re.search(rx, first, re.I):
            return t
    return "other"


def cited(text):
    out = set()
    for m in re.finditer(CITE, text):
        for part in re.split(r"\s*(?:,|and)\s*", m.group(1)):
            mm = re.match(r"(\d{1,3})(?:\s*[-–]\s*(\d{1,3}))?$", part.strip())
            if not mm:
                continue
            a = int(mm.group(1)); b = int(mm.group(2)) if mm.group(2) else a
            rng = range(a, b + 1) if 0 <= b - a <= 30 else [a, b]
            out.update(x for x in rng if 1 <= x <= 400)
    return sorted(out)


def verdict_of(text):
    vs = re.findall(r"verdict:\s*\**\s*(PASS|FAIL|INCOMPLETE)", text, re.I)
    return vs[-1].upper() if vs else "NONE"


def blocking_tags(path, overrides=None):
    """[(id, theme)] of a Stage 2 style report; empty unless its verdict is FAIL. overrides: {(file stem, id): theme}."""
    t = pathlib.Path(path).read_text(errors="ignore")
    if verdict_of(t) != "FAIL":
        return []
    out = []
    for fid in parse_ids(ids_from(path)):
        sec = find_section(t, fid)
        th = tag(*sec) if sec else "other"
        if overrides and (pathlib.Path(path).parent.parent.parent.parent.parent.name, pathlib.Path(path).stem, fid) in overrides:
            th = overrides[(pathlib.Path(path).parent.parent.parent.parent.parent.name, pathlib.Path(path).stem, fid)]
        out.append((fid, th))
    return out
