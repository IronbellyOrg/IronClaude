"""PN3 harness: C4.1 findings parser, C5 anchors/fingerprint/same-defect, C6 ledger, C7 capture export.
Implemented from the shared contract; stdlib only. Not product code."""
import difflib
import hashlib
import json
import os
import re

SEV = ("CRITICAL", "MAJOR", "MINOR")
CAT = ("contradiction", "unpassable-check", "data-loss", "safety", "missing-requirement", "other")
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$")
FENCE = re.compile(r"(?ms)^```findings-v1[ \t]*\n(.*?)^```[ \t]*$")
FIXFENCE = re.compile(r"(?ms)^```fixmap-v1[ \t]*\n(.*?)^```[ \t]*$")


def flat(s):
    return " ".join(s.split())


# ------------------------------------------------------------------ C4.1 / C4.2
def parse_block(text):
    res = {"ok": True, "findings": [], "priors": [], "errors": []}
    idx = text.rfind("## Findings block")
    if idx < 0:
        res["ok"] = False
        res["errors"].append({"line": 0, "msg": "missing '## Findings block' heading"})
        return res
    tail = text[idx:]
    blocks = list(FENCE.finditer(tail))
    if not blocks:
        res["ok"] = False
        res["errors"].append({"line": 0, "msg": "missing findings-v1 fenced block"})
        return res
    if len(blocks) > 1:
        res["ok"] = False
        res["errors"].append({"line": 0, "msg": "more than one findings-v1 block; the last one is used"})
    body = blocks[-1].group(1)
    seen = set()
    for n, line in enumerate(body.splitlines(), 1):
        if not line.strip():
            continue
        try:
            o = json.loads(line)
        except ValueError as e:
            res["ok"] = False
            res["errors"].append({"line": n, "msg": f"invalid JSON: {e}"})
            continue
        if not isinstance(o, dict):
            res["ok"] = False
            res["errors"].append({"line": n, "msg": "not an object"})
            continue
        if "prior" in o:
            if o.get("status") not in ("resolved", "open", "regressed") or not isinstance(o["prior"], str):
                res["ok"] = False
                res["errors"].append({"line": n, "msg": "bad prior line"})
                continue
            res["priors"].append({"prior": o["prior"], "status": o["status"]})
            continue
        err = _check_finding(o)
        if not err and o["id"] in seen:
            err = "duplicate id"
        if err:
            res["ok"] = False
            res["errors"].append({"line": n, "msg": err})
            continue
        seen.add(o["id"])
        res["findings"].append(o)
    return res


def _check_finding(o):
    if not isinstance(o.get("id"), str) or not ID_RE.match(o["id"]):
        return "bad id"
    if o.get("severity") not in SEV:
        return "bad severity"
    if not isinstance(o.get("blocking"), bool):
        return "bad blocking"
    if o["blocking"] and o["severity"] == "MINOR":
        return "blocking MINOR"
    if o.get("category") not in CAT:
        return "bad category"
    for k in ("anchor", "anchor2"):
        if k in o and o[k] is not None:
            if not isinstance(o[k], str) or not 12 <= len(flat(o[k])) <= 200:
                return f"bad {k}"
        elif k == "anchor":
            return "missing anchor"
    refs = o.get("refs", [])
    if not isinstance(refs, list) or len(refs) > 8 or not all(isinstance(r, str) for r in refs):
        return "bad refs"
    if not isinstance(o.get("claim", ""), str) or len(o.get("claim", "")) > 300:
        return "bad claim"
    return None


def parse_fixmap(text):
    res = {"ok": True, "items": [], "errors": []}
    blocks = list(FIXFENCE.finditer(text))
    if not blocks:
        res["ok"] = False
        for m in re.finditer(r"(?im)^\|\s*([A-Za-z0-9._-]+)\s*\|\s*applied\b", text):
            res["items"].append({"id": m.group(1), "action": "applied", "reason": ""})
        return res
    for n, line in enumerate(blocks[-1].group(1).splitlines(), 1):
        if not line.strip():
            continue
        try:
            o = json.loads(line)
            assert o["action"] in ("applied", "rejected") and isinstance(o["id"], str)
        except Exception as e:  # noqa: BLE001
            res["ok"] = False
            res["errors"].append({"line": n, "msg": str(e)})
            continue
        res["items"].append(o)
    return res


# ------------------------------------------------------------------ C5
def locate(text, quote):
    q = flat(quote)
    if not q:
        return []
    chars, line_of = [], []
    line, prev = 0, True
    for ch in text:
        if ch.isspace():
            if not prev:
                chars.append(" ")
                line_of.append(line)
                prev = True
        else:
            chars.append(ch)
            line_of.append(line)
            prev = False
        if ch == "\n":
            line += 1
    norm = "".join(chars)
    out, i = [], norm.find(q)
    while i != -1:
        out.append((line_of[i], line_of[i + len(q) - 1] + 1))
        i = norm.find(q, i + 1)
    return out


def section_of(text, line):
    lines = text.split("\n")
    for i in range(min(line, len(lines) - 1), -1, -1):
        m = re.match(r"^#{1,6}\s+(.*)$", lines[i])
        if m:
            h = m.group(1)
            n = re.match(r"^(\d+(?:\.\d+)*)", h)
            return n.group(1) if n else re.sub(r"[^a-z0-9]+", "-", h.lower())
    return "top"


REF_RE = re.compile(r"\b(?:[A-Z]{1,4}-[0-9]+(?:\.[0-9]+)*|P[0-9])\b")


def refs_norm(f):
    toks = set()
    parts = [f.get("anchor") or "", f.get("anchor2") or "", f.get("claim") or ""] + list(f.get("refs", []))
    for p in parts:
        toks.update(REF_RE.findall(p))
    for r in f.get("refs", []):
        if re.match(r"^\d+(?:\.\d+)*$", r):
            toks.add(r)
    return sorted(t.upper() for t in toks if not t.startswith("SHA-"))


def fingerprint(sec, refs):
    return hashlib.sha256(("v1|" + sec + "|" + ",".join(refs)).encode()).hexdigest()[:16]


def enrich(f, doc_text):
    """Add span, span2, anchor_status, anchor_ambiguous, refs_norm, fp to a finding dict (copy)."""
    g = dict(f)
    spans = locate(doc_text, f["anchor"])
    g["anchor_ambiguous"] = len(spans) > 1
    g["anchor_status"] = "ok" if spans else "missing"
    g["span"] = list(spans[0]) if spans else None
    g["span2"] = None
    if f.get("anchor2"):
        s2 = locate(doc_text, f["anchor2"])
        g["span2"] = list(s2[0]) if s2 else None
    g["refs_norm"] = refs_norm(f)
    g["fp"] = fingerprint(section_of(doc_text, g["span"][0]) if g["span"] else "none", g["refs_norm"])
    return g


def _spans(x):
    return [s for s in (x.get("span"), x.get("span2")) if s]


def same_defect(a, b):
    if a["fp"] == b["fp"]:
        return True
    sa, sb = _spans(a), _spans(b)
    if not sa or not sb:
        return False
    near = any(x[0] <= y[1] + 3 and y[0] <= x[1] + 3 for x in sa for y in sb)
    if not near:
        return False
    ra, rb = set(a["refs_norm"]), set(b["refs_norm"])
    return bool(ra & rb) or (not ra and not rb)


def span_map(old_text, new_text):
    old, new = old_text.split("\n"), new_text.split("\n")
    mp, hunks = {}, []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                mp[i1 + k] = j1 + k
        else:
            for k in range(i1, i2):
                mp[k] = j1
            hunks.append((i1, i2))
    return mp, hunks


def touches(hunk, span):
    if hunk[0] == hunk[1]:
        return span[0] <= hunk[0] <= span[1]
    return hunk[0] < span[1] and span[0] < hunk[1]


def _map_span(span, mp, n_new):
    if span is None:
        return None
    s = mp.get(span[0], 0)
    e = mp.get(span[1] - 1, s) + 1
    return [s, max(e, s + 1)]


# ------------------------------------------------------------------ C6
def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


class Ledger:
    def __init__(self, doc="", cap=3, data=None):
        self.d = data or {"schema": "review-ledger/1", "doc": doc, "cap_reviews": cap, "rounds": [], "rows": []}

    @property
    def rows(self):
        return self.d["rows"]

    def _next_lid(self):
        return f"L{len(self.rows) + 1}"

    def add_round(self, n, doc_text, reviewers):
        """reviewers: ordered list of dict(reviewer_id, model, report (path), text). Returns cluster/round info."""
        findings, rinfo = [], []
        for rv in reviewers:
            pb = parse_block(rv["text"])
            rinfo.append({"reviewer_id": rv["reviewer_id"], "model": rv.get("model"), "report": rv.get("report"),
                          "report_sha256": sha(rv["text"]), "block_ok": pb["ok"]})
            for f in pb["findings"]:
                g = enrich(f, doc_text)
                g["reviewer_id"] = rv["reviewer_id"]
                findings.append(g)
        # clusters: union-find over findings of this round
        par = list(range(len(findings)))

        def find(x):
            while par[x] != x:
                par[x] = par[par[x]]
                x = par[x]
            return x

        for i in range(len(findings)):
            for j in range(i + 1, len(findings)):
                if same_defect(findings[i], findings[j]):
                    par[max(find(i), find(j))] = min(find(i), find(j))
        groups = {}
        for i in range(len(findings)):
            groups.setdefault(find(i), []).append(findings[i])
        clusters = sorted(groups.values(), key=lambda g: findings.index(g[0]))
        matched = set()
        for cl in clusters:
            row = next((r for r in self.rows if any(self._row_matches(r, f) for f in cl)), None)
            blocking = any(f["blocking"] for f in cl)
            members = [{"round": n, "reviewer_id": f["reviewer_id"], "fid": f["id"], "blocking": f["blocking"]} for f in cl]
            distinct = len({f["reviewer_id"] for f in cl})
            if row is None:
                first = cl[0]
                sev = min((f["severity"] for f in cl), key=SEV.index)
                row = {"lid": self._next_lid(), "fp": first["fp"], "blocking": blocking, "severity_max": sev,
                       "category": first["category"], "confidence": "overlap" if distinct >= 2 else "single",
                       "status": "open", "anchor": first["anchor"], "anchor2": first.get("anchor2"),
                       "span": first["span"], "span2": first["span2"], "refs": first["refs_norm"], "members": members,
                       "history": [{"round": n, "event": "opened"}]}
                self.rows.append(row)
            else:
                matched.add(row["lid"])
                row["members"].extend(members)
                row["blocking"] = row["blocking"] or blocking
                row["severity_max"] = min([row["severity_max"]] + [f["severity"] for f in cl], key=SEV.index)
                if distinct >= 2:
                    row["confidence"] = "overlap"
                if row["status"] in ("resolved_check", "resolved"):
                    row["status"] = "regressed"
                row["history"].append({"round": n, "event": "refound"})
            matched.add(row["lid"])
        for r in self.rows:
            if r["status"] == "resolved_check" and r["lid"] not in matched:
                r["status"] = "resolved"
                r["history"].append({"round": n, "event": "cleared"})
        verdict = self.verdict()
        rd = {"n": n, "doc_sha256": sha(doc_text), "reviewers": rinfo, "verdict": verdict,
              "decision": self.decision(verdict, n)}
        self.d["rounds"].append(rd)
        return {"round": rd, "clusters": len(clusters), "findings": len(findings)}

    @staticmethod
    def _row_matches(row, f):
        pseudo = {"fp": row["fp"], "span": row["span"], "span2": row["span2"], "refs_norm": row["refs"]}
        return same_defect(f, pseudo)

    def verdict(self):
        return "FAIL" if any(r["blocking"] and r["status"] in ("open", "regressed") for r in self.rows) else "PASS"

    def decision(self, verdict, n):
        if verdict == "PASS":
            return "PASS"
        return "REVISE" if n < self.d["cap_reviews"] else "ESCALATE"

    def open_blocking(self):
        return [r["lid"] for r in self.rows if r["blocking"] and r["status"] in ("open", "regressed")]

    def apply_revision(self, old_text, new_text, fixmap_items):
        mp, hunks = span_map(old_text, new_text)
        named = {i["id"]: i["action"] for i in fixmap_items}
        for r in self.rows:
            act = named.get(r["lid"])
            sp = [s for s in (r["span"], r["span2"]) if s]
            if act == "applied":
                if any(touches(h, s) for h in hunks for s in sp):
                    r["status"] = "resolved_check"
                    r["history"].append({"round": None, "event": "resolved_check"})
                else:
                    r["history"].append({"round": None, "event": "named_not_touched"})
            elif act == "rejected":
                r["history"].append({"round": None, "event": "rejected_by_reviser"})
            n_new = len(new_text.split("\n"))
            r["span"] = _map_span(r["span"], mp, n_new)
            r["span2"] = _map_span(r["span2"], mp, n_new)

    def defer(self, lid):
        for r in self.rows:
            if r["lid"] == lid:
                r["status"] = "deferred"

    def capture(self, n, source="ledger"):
        rd = next(x for x in self.d["rounds"] if x["n"] == n)
        occ = [x["reviewer_id"] for x in rd["reviewers"]]
        defects = []
        for r in self.rows:
            ms = [m for m in r["members"] if m["round"] == n]
            if not ms:
                continue
            defects.append({"key": r["lid"], "blocking": any(m["blocking"] for m in ms),
                            "captured_by": [o for o in occ if any(m["reviewer_id"] == o for m in ms)]})
        return {"schema": "review-capture/1", "source": source, "round": n, "doc_sha256": rd["doc_sha256"],
                "occasions": occ, "defects": defects}

    def save(self, path):
        tmp = f"{path}.tmp"
        with open(tmp, "w") as fh:
            json.dump(self.d, fh, indent=1)
        os.replace(tmp, path)

    @classmethod
    def load(cls, path):
        return cls(data=json.load(open(path)))
