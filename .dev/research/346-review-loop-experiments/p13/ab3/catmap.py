"""Map findings / ledger rows to catalog clusters (approximate: anchor span within 3 lines of the cluster's orig_span and theme or refs agree).
Used by shadow.py (F3) and analyze.py (residual decomposition). Others become new clusters ('N<i>')."""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "offline"))
import common as c  # noqa: E402
import extract as X  # noqa: E402

REF = re.compile(r"\b(?:[A-Z]{1,4}-[0-9]+(?:\.[0-9]+)*|P[0-9])\b")
_CAT = None
_ORIG = None


def catalog(path=None):
    global _CAT
    if path:
        return json.load(open(path))
    if _CAT is None:
        _CAT = json.load(open(c.CAT / "catalog.json"))
    return _CAT


def orig_text():
    global _ORIG
    if _ORIG is None:
        _ORIG = c.ORIG.read_text()
    return _ORIG


def span_of(quotes):
    for q in quotes:
        s = c.locate(orig_text(), q)
        if s:
            return list(s[0])
    return None


def map_to_cluster(quotes, text, cat=None):
    """Return a catalog cid or None (new cluster)."""
    cat = cat or catalog()
    sp = span_of(quotes)
    if sp is None:
        return None
    theme = c.tag("", text)
    refs = set(REF.findall(text))
    best = None
    for cl in cat["clusters"]:
        a = cl["orig_span"]
        gap = max(a[0] - sp[1], sp[0] - a[1], 0)
        if gap > 3:
            continue
        agree = (theme != "other" and theme == cl["theme"]) or bool(refs & set(REF.findall(cl["anchor"] + " " + cl["label"])))
        if agree and (best is None or gap < best[0]):
            best = (gap, cl["cid"])
    return best[1] if best else None


def audit_findings(audit_path):
    """Blocking findings of an audit (C9.3) -> list of dict(fid, quotes, text)."""
    t = pathlib.Path(audit_path).read_text(errors="ignore")
    if c.verdict_of(t) != "FAIL":
        return []
    out = []
    for fid in c.parse_ids(c.ids_from(audit_path)):
        sec = c.find_section(t, fid)
        if not sec:
            out.append({"fid": fid, "quotes": [], "text": ""})
            continue
        text = sec["heading"] + "\n" + sec["body"]
        out.append({"fid": fid, "quotes": X.quotes_of(text), "text": text})
    return out
