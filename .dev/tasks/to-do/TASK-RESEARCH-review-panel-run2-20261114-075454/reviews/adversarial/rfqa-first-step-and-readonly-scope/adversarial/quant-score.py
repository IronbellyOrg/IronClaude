#!/usr/bin/env python3
"""Deterministic quantitative layer (A.1) for the C-11 adversarial run.

Stdlib only. Run with: uv run python <this file>
Reads the two variants and diff-analysis.md, writes quant-score-output.json next to itself.
No clock, no randomness, no network: two runs give byte-identical output.
"""
import hashlib
import json
import re
from pathlib import Path

ADV = Path(
    "/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/"
    "TASK-RESEARCH-review-panel-run2-20261114-075454/reviews/adversarial/"
    "rfqa-first-step-and-readonly-scope/adversarial"
)
VARIANTS = {"A": ADV / "variant-1-original.md", "B": ADV / "variant-2-original.md"}
DIFF = ADV / "diff-analysis.md"
OUT = ADV / "quant-score-output.json"

WEIGHTS = {"RC": 0.30, "IC": 0.25, "SR": 0.15, "DC": 0.15, "SC": 0.15}

# ---- RC requirement list (row C-11 of undecidable-conflicts.md, plus decided-fact phrases) ----
REQ_IDS = ["CO-30", "CO-31", "FX-8", "FX-20", "INV-G", "INV-J", "INV-N", "INV-K", "GQ-181"]
REQ_PHRASES = ["read-only", "behavioural oracle", "eight lens", "Q3"]

# ---- shared regexes ----
FILE_LINE = re.compile(r"[\w./-]+\.(?:py|md|json|yaml):\d+")
NUMBER = re.compile(r"(?<![\w-])\d+(?:[.,]\d+)*%?(?![\w-])")
BACKTICK = re.compile(r"`[^`]+`")
PATH_LIKE = re.compile(r"[\w.-]+/[\w./-]+")
FILE_NAME = re.compile(r"\b[\w-]+\.(?:py|md|json|yaml|yml)\b")
ID_TOKEN = re.compile(r"\b[A-Z]{1,5}-[A-Z0-9]{1,4}\b")
VAGUE = [
    ("appropriate", re.compile(r"\bappropriate\b", re.I)),
    ("as needed", re.compile(r"\bas needed\b", re.I)),
    ("properly", re.compile(r"\bproperly\b", re.I)),
    ("adequate", re.compile(r"\badequate\b", re.I)),
    ("should consider", re.compile(r"\bshould consider\b", re.I)),
    ("might", re.compile(r"\bmight\b", re.I)),
    ("various", re.compile(r"\bvarious\b", re.I)),
    ("etc.", re.compile(r"\betc\b\.?", re.I)),
    ("best practices", re.compile(r"\bbest practices?\b", re.I)),
    ("industry standard", re.compile(r"\bindustry[- ]standard\b", re.I)),
]
CITED_ONLY = {"best practices", "industry standard"}  # vague only when no file:line citation
CLAIM_EXCLUDE = re.compile(r"\bas appropriate\b|\bas needed\b", re.I)
SEPARATOR = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
H_ANY = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
H_NUM = re.compile(r"^(\d+(?:\.\d+)*)[.)]?(?:\s|$)")
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z`\"(\[])")
BULLET = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
EXTERNAL_PRE = re.compile(r"^(?:r\d+(?:'s)?|S\d+|synth-\d+|C-\d+|[\w./-]+\.md|[\w./-]+\.py)$")
SEC_REF = re.compile(
    r"(?:(?P<pre>\S+)\s+)?\b[Ss]ections?\s+(?P<num>\d+(?:\.\d+)*)(?:\s+part\s+(?P<part>\d+))?"
)
SEE_REF = re.compile(r"\bSee\s+\[(?P<name>[^\]]+)\]")


def split_cells(row):
    """Split a markdown table row on '|' that is outside backtick spans."""
    cells, cur, in_tick = [], [], False
    for ch in row.strip():
        if ch == "`":
            in_tick = not in_tick
        if ch == "|" and not in_tick:
            cells.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    cells.append("".join(cur))
    if cells and cells[0].strip() == "":
        cells = cells[1:]
    if cells and cells[-1].strip() == "":
        cells = cells[:-1]
    return [c.strip() for c in cells if c.strip()]


def body_lines(text):
    """Return (lineno, line) for lines after the first H2 (header metadata dropped), not in fences."""
    lines = text.split("\n")
    first_h2 = next((i for i, l in enumerate(lines) if l.startswith("## ")), 0)
    out, fenced = [], False
    for i, l in enumerate(lines):
        if i < first_h2:
            continue
        if l.strip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        out.append((i + 1, l))
    return out


def units(text):
    """Substantive statement units: sentences of prose lines and cells of table rows.
    Excludes headings, table separators, table header rows, blank lines, and 'Status:' metadata lines."""
    body = body_lines(text)
    res = []
    for idx, (no, l) in enumerate(body):
        s = l.strip()
        if not s or H_ANY.match(s) or SEPARATOR.match(s) or s.startswith("Status:"):
            continue
        if s.startswith("|"):
            nxt = body[idx + 1][1] if idx + 1 < len(body) else ""
            if SEPARATOR.match(nxt.strip()):
                continue  # table header row
            for c in split_cells(s):
                res.append((no, c))
            continue
        s = BULLET.sub("", s)
        for sent in SENT_SPLIT.split(s):
            sent = sent.strip()
            if sent:
                res.append((no, sent))
    return res


def is_claim(u):
    has_cite = bool(FILE_LINE.search(u))
    if CLAIM_EXCLUDE.search(u):
        return False
    if re.search(r"\bbest practices?\b", u, re.I) and not has_cite:
        return False
    return has_cite or bool(NUMBER.search(u))


def concrete_hits(u):
    hits = []
    if FILE_LINE.search(u):
        hits.append("file:line")
    if NUMBER.search(u):
        hits.append("number")
    if BACKTICK.search(u):
        hits.append("code-identifier")
    if PATH_LIKE.search(u) or FILE_NAME.search(u):
        hits.append("path")
    if ID_TOKEN.search(u):
        hits.append("named-id")
    return hits


def vague_hits(u):
    has_cite = bool(FILE_LINE.search(u))
    out = []
    for name, rx in VAGUE:
        if rx.search(u):
            if name in CITED_ONLY and has_cite:
                continue
            out.append(name)
    return out


def norm(s):
    return re.sub(r"\s+", " ", s.lower().replace("-", " "))


def match_phrase(phrase, text):
    words = norm(phrase).split()
    nt = norm(text)
    if len(words) >= 3:
        for i in range(len(words) - 2):
            tri = " ".join(words[i : i + 3])
            if re.search(r"(?<![a-z])" + re.escape(tri), nt):
                return True, "fuzzy-3gram:" + tri
        return False, ""
    if re.fullmatch(r"[A-Za-z]\d+", phrase):  # id-like token such as Q3, case-sensitive
        m = re.search(r"(?<![A-Za-z0-9])" + re.escape(phrase) + r"(?![A-Za-z0-9])", text)
        return bool(m), "exact-token" if m else ""
    m = re.search(r"(?<![a-z])" + re.escape(norm(phrase)), nt)
    return bool(m), "phrase" if m else ""


def metric_rc(text):
    matched, missing, how = [], [], {}
    for rid in REQ_IDS:
        pat = re.compile(r"(?<![A-Za-z0-9-])" + re.escape(rid) + r"(?![A-Za-z0-9])")
        n = len(pat.findall(text))
        if n:
            matched.append(rid)
            how[rid] = "id x%d" % n
        else:
            missing.append(rid)
    for ph in REQ_PHRASES:
        ok, mech = match_phrase(ph, text)
        if ok:
            matched.append(ph)
            how[ph] = mech
        else:
            missing.append(ph)
    total = len(REQ_IDS) + len(REQ_PHRASES)
    return {
        "value": len(matched) / total,
        "numerator": len(matched),
        "denominator": total,
        "detail": "matched %d of %d requirements (ids %d, phrases %d)"
        % (len(matched), total, len([m for m in matched if m in REQ_IDS]), len([m for m in matched if m in REQ_PHRASES])),
        "matched": matched,
        "unmatched": missing,
        "how": how,
    }


def parse_intra_contradictions():
    found = {"A": [], "B": []}
    for line in DIFF.read_text(encoding="utf-8").split("\n"):
        if not re.match(r"^\|\s*X-\d+\s*\|", line):
            continue
        cells = split_cells(line)
        point = cells[1].lower()
        for v in ("A", "B"):
            if "intra-variant " + v.lower() in point:
                found[v].append(cells[0])
    return found


def metric_ic(text, contradictions):
    claims = [u for _, u in units(text) if is_claim(u)]
    n = len(claims)
    c = len(contradictions)
    return {
        "value": 1 - c / n if n else 1.0,
        "numerator": n - c,
        "denominator": n,
        "detail": "total_claims=%d (units with a file:line citation or a standalone number, vague-phrase units excluded); "
        "intra-variant contradictions=%d %s from diff-analysis.md Contradictions table; cross-variant X-rows not counted"
        % (n, c, contradictions),
        "total_claims": n,
        "contradiction_ids": contradictions,
    }


def metric_sr(text):
    conc = vague = 0
    vague_examples = []
    for no, u in units(text):
        if concrete_hits(u):
            conc += 1
        vh = vague_hits(u)
        if vh:
            vague += 1
            vague_examples.append("line %d: %s" % (no, ",".join(vh)))
    d = conc + vague
    return {
        "value": conc / d if d else 0.0,
        "numerator": conc,
        "denominator": d,
        "detail": "concrete units=%d (number, file:line, path, code identifier or named id), vague units=%d; a unit can count in both"
        % (conc, vague),
        "concrete_units": conc,
        "vague_units": vague,
        "vague_hits": vague_examples,
    }


def heading_numbers_and_titles(text):
    nums, titles = set(), set()
    fenced = False
    for l in text.split("\n"):
        if l.strip().startswith("```"):
            fenced = not fenced
        if fenced:
            continue
        m = H_ANY.match(l)
        if not m:
            continue
        title = m.group(2)
        titles.add(re.sub(r"\s+", " ", title.lower()))
        n = H_NUM.match(title)
        if n:
            nums.add(n.group(1))
    return nums, titles


def metric_dc(text):
    nums, titles = heading_numbers_and_titles(text)
    refs = []  # (lineno, ref text, status, resolved)
    for no, l in body_lines(text):
        if H_ANY.match(l.strip()) or SEPARATOR.match(l.strip()):
            continue
        for m in SEC_REF.finditer(l):
            pre = (m.group("pre") or "").strip("`()[]\",;:")
            label = m.group(0).strip()
            if pre and EXTERNAL_PRE.match(pre):
                refs.append((no, label, "external", None))
                continue
            ok = m.group("num") in nums
            refs.append((no, label, "internal", ok))
        for m in SEE_REF.finditer(l):
            name = re.sub(r"\s+", " ", m.group("name").lower())
            ok = any(name in t for t in titles)
            refs.append((no, m.group(0), "internal", ok))
    internal = [r for r in refs if r[2] == "internal"]
    resolved = [r for r in internal if r[3]]
    return {
        "value": len(resolved) / len(internal) if internal else 1.0,
        "numerator": len(resolved),
        "denominator": len(internal),
        "detail": "internal references=%d, resolved=%d, external excluded=%d; heading numbers present=%s"
        % (len(internal), len(resolved), len(refs) - len(internal), sorted(nums, key=lambda s: [int(x) for x in s.split(".")])),
        "internal_refs": ["line %d: %s -> %s" % (r[0], r[1], "resolved" if r[3] else "UNRESOLVED") for r in internal],
        "external_refs_excluded": ["line %d: %s" % (r[0], r[1]) for r in refs if r[2] == "external"],
    }


def h2_count(text):
    fenced, n = False, 0
    for l in text.split("\n"):
        if l.strip().startswith("```"):
            fenced = not fenced
        if not fenced and re.match(r"^## \S", l):
            n += 1
    return n


def main():
    texts = {k: p.read_text(encoding="utf-8") for k, p in VARIANTS.items()}
    intra = parse_intra_contradictions()
    h2 = {k: h2_count(t) for k, t in texts.items()}
    max_h2 = max(h2.values())
    result = {
        "protocol": "sc-adversarial-protocol refs/scoring-protocol.md section A.1",
        "weights": WEIGHTS,
        "inputs": {
            k: {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for k, p in VARIANTS.items()
        },
        "requirement_ids": REQ_IDS,
        "requirement_phrases": REQ_PHRASES,
        "variants": {},
    }
    for k, t in texts.items():
        rc = metric_rc(t)
        ic = metric_ic(t, intra[k])
        sr = metric_sr(t)
        dc = metric_dc(t)
        sc = {
            "value": h2[k] / max_h2,
            "numerator": h2[k],
            "denominator": max_h2,
            "detail": "H2 count %d / max H2 count %d" % (h2[k], max_h2),
        }
        metrics = {"RC": rc, "IC": ic, "SR": sr, "DC": dc, "SC": sc}
        score = sum(WEIGHTS[m] * metrics[m]["value"] for m in WEIGHTS)
        for m in metrics.values():
            m["value"] = round(m["value"], 6)
        result["variants"][k] = {
            "file": VARIANTS[k].name,
            "metrics": metrics,
            "quant_score": round(score, 4),
        }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")
    for k, v in result["variants"].items():
        print(k, {m: v["metrics"][m]["value"] for m in WEIGHTS}, "quant_score=%.4f" % v["quant_score"])


if __name__ == "__main__":
    main()
