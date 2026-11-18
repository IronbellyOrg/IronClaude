#!/usr/bin/env python3
"""E4 post-merge validation (refactor-plan M-30) of MERGED-review-panel-unification.md.

Reads the merged file, partials/merge-stage/e4-blocks.json (written by e4_assemble.py),
variant-1-original.md, diff-analysis.md and partials/matrix.json. Read-only except for the
report it writes: partials/merge-stage/E4-validation-report.md.
Exit code 0 when every check passes, 1 otherwise.

Run: uv run --no-project python partials/merge-scripts/e4_validate.py
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

ADV = Path(__file__).resolve().parents[2]
STAGE = ADV / "partials" / "merge-stage"
MERGED = ADV.parent / "MERGED-review-panel-unification.md"
REPORT = STAGE / "E4-validation-report.md"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from e4_assemble import clean_heading, gh_slug, headings, slugs_for  # noqa: E402

text = MERGED.read_text(encoding="utf-8")
L = text.rstrip("\n").split("\n")              # L[i] is line i+1
meta = json.loads((STAGE / "e4-blocks.json").read_text())
PARTS = meta["parts"]
NEW = set(meta["new_text_lines"])
V1 = (ADV / "variant-1-original.md").read_text(encoding="utf-8").split("\n")
DIFF = (ADV / "diff-analysis.md").read_text(encoding="utf-8")
WIN = json.loads((ADV / "partials" / "matrix.json").read_text())["winners"]

results: "OrderedDict[str, tuple[str, list[str]]]" = OrderedDict()


def rec(name: str, ok: bool, lines: list[str]):
    results[name] = ("PASS" if ok else "FAIL", lines)


def part(name_prefix: str) -> dict:
    hits = [p for p in PARTS if p["name"].startswith(name_prefix)]
    assert len(hits) == 1, (name_prefix, hits)
    return hits[0]


def lines_of(p: dict) -> list[tuple[int, str]]:
    return [(n, L[n - 1]) for n in range(p["start"], p["end"] + 1)]


def text_of(p: dict) -> str:
    return "\n".join(L[p["start"] - 1:p["end"]])


HD = list(headings(L))                    # (index0, level, text)

# 1. H2 sections ------------------------------------------------------------
h2 = [clean_heading(t) for _i, lvl, t in HD if lvl == 2]
allowed = (["Merge Notes", "Table of Contents", "Baseline and Conventions"]
           + [f"{n}." for n in range(1, 11)] + [f"Appendix {c}" for c in "ABCDEF"])
seq_ok = len(h2) == len(allowed) and all(h.startswith(a) for h, a in zip(h2, allowed))
rec("1 H2 sections: Merge Notes, ToC, Baseline, 1-10 in order, Appendix A-F; no other H2", seq_ok,
    [f"{len(h2)} H2 headings"] + [f"- {h}" for h in h2])

# 2. heading levels ---------------------------------------------------------
gaps, prev = [], 0
for i, lvl, t in HD:
    if prev and lvl > prev + 1:
        gaps.append(f"line {i + 1}: H{prev} -> H{lvl} `{clean_heading(t)[:80]}`")
    prev = lvl
h1 = [i + 1 for i, lvl, _t in HD if lvl == 1]
rec("2 Heading levels: one H1, no level gaps", not gaps and len(h1) == 1,
    [f"H1 at lines {h1}", f"level jumps: {len(gaps)}"] + gaps[:20])

# 3. Source comments --------------------------------------------------------
miss = []
for p in PARTS:
    if p["name"] == "Provenance header":
        ok = L[0].startswith("<!-- Provenance:") and L[1].startswith("<!-- Base:") and L[2].startswith("<!-- Merge date:")
    else:
        first = [ln for _n, ln in lines_of(p) if ln.strip() and ln.strip() != "---"][0]
        ok = first.startswith("<!-- Source:")
    if not ok:
        miss.append(p["name"])
rec("3 Every block carries a Source comment (provenance header first)", not miss,
    [f"{len(PARTS)} parts checked; first three lines are the provenance header: "
     f"{L[0].startswith('<!-- Provenance:')}"] + [f"missing: {m}" for m in miss])

# 4. closed-item prefix (plan-review escalation R3-B1) ------------------------
bad = [f"line {n}: {m.group(0)}" for n, ln in enumerate(L, 1)
       for m in re.finditer(r"(?i)(closed items?\s+\(?R1-C-\d\d|GQ[: ]R1-C-\d\d)", ln)]
cls = len(re.findall(r"R1-CLS-\d\d", text))
rec("4 No `Closed item R1-C-` / `GQ:R1-C-` / `GQ R1-C-` token (R3-B1 escalation)", not bad,
    [f"R1-CLS-nn tokens in the merged file: {cls}", f"bad tokens: {len(bad)}"] + bad[:20])

# 5. the four deleted Dependencies lines --------------------------------------
def norm(s: str) -> str:
    s = s.replace("R1-", "")
    return re.sub(r"(\b[A-Z]{1,2}\d{1,2})\.\.(\1|[A-Z]{1,2}\d{1,2})", r"\1-\2", s)


mnorm = set(norm(ln) for ln in L)
p84 = part("8.4 ")
deps = []
for v in (3829, 3860, 3879, 3897):
    orig = V1[v - 1]
    present = orig in L or norm(orig) in mnorm or orig[:60] in text
    deps.append(f"V1:{v} `{orig[:70]}...`: {'PRESENT' if present else 'absent'}")
lead_dep = [n for n, ln in lines_of(p84) if ln.startswith("**Dependencies:**")]
rec("5 The four deleted `**Dependencies:**` lines (V1:3829, 3860, 3879, 3897) are absent",
    all(d.endswith("absent") for d in deps) and not lead_dep,
    deps + [f"lines starting `**Dependencies:**` in 8.4: {lead_dep}"])

# 6. 48 step ids with a status in 8.4 ------------------------------------------
steps = [f"R1-M1-{i:02d}" for i in range(1, 23)] + [f"R1-M2-{i:02d}" for i in range(1, 11)] + \
        [f"R1-M3-{i:02d}" for i in range(1, 10)] + [f"R1-M4-{i:02d}" for i in range(1, 8)]
status = {}
for n, ln in lines_of(p84):
    m = re.match(r"^\| (CONFLICTS|PARTLY COMPATIBLE|COMPATIBLE)[^|]*\| (R1-M[1-4]-\d\d) \|", ln)
    if m:
        status.setdefault(m.group(2), []).append(m.group(1))
missing = [s for s in steps if len(status.get(s, [])) != 1]
cnt = Counter(v[0] for v in status.values())
rec("6 All 48 run 1 step ids R1-M1-01..R1-M4-07 appear in 8.4 with a status", not missing and len(status) == 48,
    [f"step rows with status: {len(status)}; counts {dict(cnt)}"] + [f"missing or duplicated: {m}" for m in missing])

# 7. Appendix C 63 rows -----------------------------------------------------------
pC = part("Appendix C")
xs = [m.group(1) for _n, ln in lines_of(pC) for m in [re.match(r"^\| (X-\d{3}) \|", ln)] if m]
want = [f"X-{i:03d}" for i in range(1, 64)]
rec("7 Appendix C has all 63 X rows", sorted(set(xs)) == want and len(xs) == 63,
    [f"rows {len(xs)}, unique {len(set(xs))}"])

# 8. 18 promoted assumptions --------------------------------------------------------
PROMOTED = ["A-002", "A-006", "A-008", "A-012", "A-018", "A-019", "A-024", "A-027", "A-036",
            "A-037", "A-038", "A-041", "A-052", "A-055", "A-056", "A-057", "A-058", "A-059"]
zones = {"Merge Notes": part("Merge Notes"), "9.12": part("9.12 "), "Appendix C": pC,
         "Appendix D/E": part("Appendices D and E")}
arows, aok = [], True
for a in PROMOTED:
    where = []
    for zn, zp in zones.items():
        for n, ln in lines_of(zp):
            if re.search(rf"(?<![\w-]){a}(?!\d)", ln):
                sub = "E.3" if zn == "Appendix D/E" and n > next(k for k, x in lines_of(zp) if x.startswith("### E.3")) else (
                    "Appendix D" if zn == "Appendix D/E" and n < next(k for k, x in lines_of(zp) if x.startswith("## Appendix E")) else zn)
                where.append(f"{sub} (line {n})")
    aok &= bool(where)
    arows.append(f"| {a} | {'; '.join(sorted(set(where))[:3]) or 'NOT ADDRESSED'} |")
rec("8 Every promoted shared assumption is addressed (Merge Notes, 9.12, Appendix C/D/E)", aok,
    ["| A id | Where (first hits) |", "|---|---|"] + arows)

# 9. git-ref constraint --------------------------------------------------------------
c4 = [ln for ln in L if ln.startswith("| C4 |")]
p87 = part("8.7 ")
t87 = text_of(p87)
phrase = "`feat/review-panel` and `feat/review-panel/<name>` cannot both exist"
g_ok = len(c4) == 1 and phrase in c4[0] and phrase in t87 and "`feat_review-panel/<name>`" in t87
rec("9 Git-ref constraint in base C4 and in 8.7; owner prefix `feat_review-panel/<name>` in 8.7", g_ok,
    [f"C4 rows: {len(c4)}; phrase in C4: {bool(c4) and phrase in c4[0]}",
     f"phrase in 8.7: {t87.count(phrase)} times", f"`feat_review-panel/<name>` in 8.7: {t87.count('`feat_review-panel/<name>`')} times"])

# 10. no-regression in base 8.2(b) and run 1 8.5 ----------------------------------------
p8b = part("8. Value Inventory")
i82b = next(n for n, ln in lines_of(p8b) if ln.startswith("#### (b) No-regression gates"))
i82c = next(n for n, ln in lines_of(p8b) if ln.startswith("#### (c) "))
nr_b = sum(1 for n in range(i82b, i82c) if re.search(r"(?i)no-regression", L[n - 1]))
p85 = part("8.5 ")
nr_5 = sum(1 for _n, ln in lines_of(p85) if re.search(r"(?i)no-regression", ln))
by_part = Counter(next(p["name"] for p in PARTS if p["start"] <= n <= p["end"])
                  for n, ln in enumerate(L, 1) if re.search(r"(?i)no-regression", ln))
rec("10 `no-regression` occurs in run 2's 8.2(b) and in run 1's 8.5", nr_b > 0 and nr_5 > 0,
    [f"lines in 8.2(b): {nr_b}; lines in 8.5: {nr_5}", "lines per part: " + "; ".join(f"{k}: {v}" for k, v in by_part.items())])

# 11. High U rows have a home ---------------------------------------------------------
U_TOKENS = {
    "U-001": ["R1-MS-14", "unauthorized_deviation_present"], "U-002": ["R1-MS-24"], "U-003": ["R1-ENS-4"],
    "U-005": ["R1 4.3 Critical and Important rows by track"], "U-010": ["R1-SC-6", "R1-SC-10"],
    "U-018": ["G-03/G-17"], "U-020": ["G-14", "G-15"], "U-021": ["G-70"], "U-022": ["Sweep Sheet"],
    "U-023": ["044809e3"], "U-024": ["model_scores"], "U-025": ["G-133"], "U-026": ["G-146"],
    "U-027": ["G-55"], "U-029": ["G-86"], "U-031": ["G-108"], "U-032": ["D-14"], "U-035": ["ec259f1b7"],
    "U-036": ["insufficient"], "U-037": ["reflect_shadow_exit.py:313"], "U-040": ["lib/"],
    "U-042": ["snap.py:4"], "U-044": ["install_commands.py:41-79"], "U-045": ["T2bModel01"],
    "U-046": ["P-d"], "U-047": ["DR-171"], "U-048": ["tasklist validate"], "U-049": ["lint-architecture"],
    "U-051": ["verify-run"], "U-054": ["--bare"], "U-056": ["rdjson"], "U-058": ["Reflect v2 shares it?"],
    "U-064": ["R1 5.2 "], "U-065": ["R1 5.4 "], "U-066": ["R1 5.3 "], "U-068": ["R1 5.5 "],
    "U-071": ["189"], "U-072": ["60 HIGH"], "U-073": ["INV-N"], "U-074": ["17 of 17"], "U-075": ["CO-14"],
    "U-076": ["M14"], "U-077": ["CO-34"], "U-086": ["R1-D-1", "R1-C-14"], "U-087": ["R1 6.D "],
    "U-088": ["R1 6.E "], "U-096": ["R1-M1-01", "R1-M4-07"], "U-097": ["R1-G2"], "U-098": ["1182", "R1-G-pr"],
    "U-099": ["`feat/review-panel/<name>`"], "U-100": ["review-panel-manifest/1"], "U-101": ["##### Gap coverage"],
    "U-102": ["R1-X14", "R1 7.2 "], "U-110": ["synth-08-value-inventory"], "U-111": ["P3-014"],
    "U-112": ["| C29 |"], "U-113": ["| D26 |"], "U-114": ["AE-15"], "U-115": ["A-20"], "U-116": ["7.2.4"],
    "U-117": ["rowcheck"], "U-118": ["Q-40"],
}
highU = [(m.group(1), m.group(2)) for m in re.finditer(r"^\| (U-\d{3}) \[src [^\]]+\] \| (V[12]) \|.*\| High \|", DIFF, re.M)]
urows, u_ok = ["| U id | Report | Token(s) | Found |", "|---|---|---|---|"], True
for uid, rep in highU:
    toks = U_TOKENS.get(uid)
    if not toks:
        u_ok = False
        urows.append(f"| {uid} | {rep} | (no token mapped) | NO |")
        continue
    found = all(t in text for t in toks)
    u_ok &= found
    urows.append(f"| {uid} | {rep} | {', '.join('`' + t.replace('|', '') .strip() + '`' for t in toks)} | {'yes' if found else 'NO'} |")
extra = {"Appendix A pointer": "## Appendix A", "C29": "| C29 |", "G27": "G27", "AE-15": "AE-15", "ENS-4": "R1-ENS-4",
         "MS-24": "R1-MS-24", "R1-D1": "R1-D1", "R1-C-14": "R1-C-14", "R1-V-001": "R1-V-001", "R1-M1-01": "R1-M1-01", "G-133": "G-133"}
for k, t in extra.items():
    u_ok &= t in text
rec("11 High-value unique rows of both variants have a home (token check)", u_ok,
    [f"High U rows in diff-analysis.md: {len(highU)} (V1 {sum(1 for _u, r in highU if r == 'V1')}, V2 {sum(1 for _u, r in highU if r == 'V2')})",
     "Prompt tokens: " + "; ".join(f"{k}: {'yes' if t in text else 'NO'}" for k, t in extra.items()),
     "U-099: only the git constraint is required; the layout table V1:4063-4069 is dropped on purpose (M-19, M-23)", ""] + urows)

# 12. internal references in NEW text ---------------------------------------------------
numbers = set()
for _i, lvl, t in HD:
    m = re.match(r"(\d+(?:\.\d+)*|\d+\.[A-B]|[A-F]\.\d)\.?\s", clean_heading(t))
    if m:
        numbers.add(m.group(1).rstrip("."))
    m = re.match(r"Appendix ([A-F])\b", clean_heading(t))
    if m:
        numbers.add("Appendix " + m.group(1))
unres, nref = [], 0
for n in sorted(NEW):
    ln = L[n - 1]
    for m in re.finditer(r"\bSections? (\d+(?:\.\d+)*(?:\.[A-B])?)", ln):
        nref += 1
        if m.group(1) not in numbers:
            unres.append(f"line {n}: `{m.group(0)}`")
    for m in re.finditer(r"\bAppendix(?:es)? ([A-F])(?:\.(\d))?\b", ln):
        nref += 1
        key = "Appendix " + m.group(1)
        if key not in numbers or (m.group(2) and f"{m.group(1)}.{m.group(2)}" not in numbers):
            unres.append(f"line {n}: `{m.group(0)}`")
# the merged-numbering pointers the Merge Notes and new blocks use
POINTERS = ["2.10", "3.6", "4.7", "4.8", "5.6", "6.13", "6.13.0", "7.0.2", "7.4", "8.3", "8.4", "8.5", "8.6", "8.7",
            "8.8", "9.11", "9.12", "10.A", "10.B", "E.1", "E.2", "E.3", "F.1", "F.2"]
pmiss = [p for p in POINTERS if p not in numbers]
rec("12 Internal references in new text resolve to headings", not unres and not pmiss,
    [f"`Section n.m` / `Appendix X` references in new text: {nref}; unresolved: {len(unres)}",
     f"merged-numbering pointers checked: {len(POINTERS)}; missing headings: {pmiss}"] + unres[:30])

# 13. roadmap / schedule / PR-plan words in new text ----------------------------------------
WORDS = re.compile(r"(?i)\b(roadmap|sprint|schedul\w*|weeks?|Phase 1|PR plan|pull-request plan|branch plan|milestones?)\b|\bETA\b")
NEG = re.compile(r"(?i)\b(no|not|nor|without|adds no|never)\b")
hits, bad13 = [], []
for n in sorted(NEW):
    ln = L[n - 1]
    for m in WORDS.finditer(ln):
        seg = ln[max(0, m.start() - 160):m.end() + 40]
        if NEG.search(ln[max(0, m.start() - 160):m.start()]) or re.search(r"(?i)\bnot (scheduled|a plan)", seg):
            why = "negation or scope exclusion (states that the document adds no such content)"
        elif "dropped as a branch plan" in ln or "is a branch plan" in ln or "Branch layouts are excluded" in ln:
            why = "names the run 1 content that was dropped as a branch plan"
        elif re.search(r"Combined Scoring|base-selection", ln):
            why = "quotes a compare artifact"
        else:
            why = "REVIEW"
            bad13.append(n)
        hits.append(f"| {n} | `{m.group(0)}` | {why} | {seg.strip()[:150].replace('|', '/')} |")
rec("13 New text adds no roadmap, schedule, PR plan or branch plan (every hit justified)", not bad13,
    [f"new-text lines scanned: {len(NEW)}; hits: {len(hits)}", "", "| Line | Word | Justification | Context |", "|---|---|---|---|"] + hits)

# 14. contradiction re-scan against Appendix C ---------------------------------------------
cr = []
def chk(label: str, cond: bool, detail: str = ""):
    cr.append((label, cond, detail))

# text outside new text and outside HTML comments (new text quotes the wrong values on purpose)
OLDTXT = {n: re.sub(r"<!--.*?-->", "", ln) for n, ln in enumerate(L, 1) if n not in NEW}


def stale_hits(s: str, ok_marker: str | None = None) -> list[int]:
    return [n for n, ln in OLDTXT.items() if s in ln and not (ok_marker and ok_marker in ln)]


chk("X-021: no `195 of 1,398` left in base or carried text", not stale_hits("195 of 1,398"),
    "; ".join(map(str, stale_hits("195 of 1,398"))))
chk("X-025: every `3 of 3 slots` in carried text carries the X-025 correction", not stale_hits("3 of 3 slots", "X-025"),
    "; ".join(map(str, stale_hits("3 of 3 slots", "X-025"))))
chk("X-026: no `3 plus a merge that lost` left in carried text", not stale_hits("3 plus a merge that lost"),
    "; ".join(map(str, stale_hits("3 plus a merge that lost"))))
chk("X-030/X-048: no `reflect's 5 [UNVERIFIED]` left", "reflect's 5 [UNVERIFIED]" not in "\n".join(L[n - 1] for n in range(1, len(L) + 1) if n not in NEW))
chk("X-017: base count \"SKILL.md` (6)\" corrected", all(("corrected" in ln) or n in NEW for n, ln in enumerate(L, 1) if "SKILL.md` (6)" in ln),
    "; ".join(str(n) for n, ln in enumerate(L, 1) if "SKILL.md` (6)" in ln))
chk("X-031: run 1 `same_defect` line carries the both-empty-refs branch", "OR (refs intersect or both refs empty)" in text)
pr50 = [n for n, ln in OLDTXT.items()
        if re.search(r"(?<![-:\w])50 (`tests/pr_submit/?` )?(test )?files|(?<![-:\w])50 files, 47", ln) and "corrected" not in ln]
chk("pr_submit count: no uncorrected `50 ... files` statement in base or carried text", not pr50,
    "; ".join(f"{n}" for n in pr50))
wd = [n for n, ln in enumerate(L, 1) if "2606.19544" in ln and "SOURCE WITHDRAWN" not in ln and "withdrawn" not in ln.lower() and n not in NEW]
part_of = lambda n: next(p["name"] for p in PARTS if p["start"] <= n <= p["end"])
wd_base = [n for n in wd if part_of(n).startswith(("5. ", "6. ", "7. ", "Appendix A"))]
chk("X-036: every base line citing arXiv 2606.19544 is marked withdrawn", not wd_base,
    "unmarked lines outside base: " + "; ".join(f"{n} ({part_of(n)[:20]})" for n in wd))
ke = [n for n, ln in enumerate(L, 1) if "KeyError" in ln and n not in NEW and "Source: Base (original, modified)" not in ln
      and next(p for p in PARTS if p["start"] <= n <= p["end"])["kind"] == "base"]
chk("X-020/X-049/X-053: base `KeyError` lines are corrected or are the two kept sites", len(ke) <= 2,
    "uncorrected base lines: " + "; ".join(str(n) for n in ke))
c43 = [n for n, ln in enumerate(L, 1) if re.search(r"\b43 (spawning |rf-\* spawning )?call sites", ln) and "unit not stated" not in ln and n not in NEW]
chk("X-022/X-029/X-061: every carried `43 call sites` carries the unit note", not c43, "; ".join(str(n) for n in c43))
xr_where_bad = []
for _n, ln in lines_of(pC):
    m = re.match(r"^\| (X-\d{3}) \|", ln)
    if not m:
        continue
    cells = ln.split(" | ")
    where = cells[-1]
    for tok in re.findall(r"(?<![\w.:-])(\d{1,2}\.(?:\d{1,2}|[AB])(?:\.\d)?)(?![\w.])", where):
        if tok not in numbers:
            xr_where_bad.append(f"{m.group(1)}: {tok}")
    v = re.search(r"debate: (?:severity rating, )?(Variant 1|Variant 2|Both \(merge\))", ln)
    w = WIN[m.group(1)]
    if v and v.group(1) != w:
        xr_where_bad.append(f"{m.group(1)}: debate verdict {v.group(1)} vs matrix {w}")
    if not v and w not in ("Open (owner or evidence)", "Unresolved split"):
        xr_where_bad.append(f"{m.group(1)}: no verdict, matrix {w}")
chk("Appendix C: every `Where handled` section exists and every verdict equals the regenerated matrix", not xr_where_bad,
    "; ".join(xr_where_bad[:20]))
open_rows = [x for x in want if WIN[x] in ("Open (owner or evidence)", "Unresolved split")]
open_in_912 = [x for x in open_rows if x in text_of(part("9.12 ")) or x == "X-051"]
chk("Appendix C OPEN rows are carried as open items (9.12) or as the label split (X-051, Merge Notes)", open_in_912 == open_rows,
    f"open rows {open_rows}")
rec("14 Contradiction re-scan against Appendix C", all(c for _l, c, _d in cr),
    [f"- {'PASS' if c else 'FAIL'}: {l}" + (f" ({d})" if d else "") for l, c, d in cr])

# 15. stale debate numbers and leftovers --------------------------------------------------------
STALE = ["218 of 234", "93.2%", "95.7%", "10 split", "7 artefacts", "130 of 234", "62 needed", "run 1's 26",
         "Variant 1 (run 1) 26", "0.93162"]
stale = [f"line {n}: `{s}`" for n in sorted(NEW) for s in STALE if s in L[n - 1]]
left = [f"line {n}: marker" for n, ln in enumerate(L, 1) if "insertion point" in ln and ln.startswith("<!-- M-") or "<!-- APPENDIX-E -->" in ln]
dup = [n for n, ln in enumerate(L, 1) if "[Compare-merge baseline note:" in ln and ":787" in ln]
dbl = [f"line {n}: {m.group(0)}" for n, ln in enumerate(L, 1) for m in re.finditer(r"R1-R1-|R1-R25-", ln)]
rec("15 No stale debate numbers in new text; no leftover markers; no double prefixes; V2:108 note de-duplicated",
    not stale and not left and not dup and not dbl,
    [f"stale tokens: {len(stale)}", f"markers left: {len(left)}", f"duplicate origin/master note: {dup}", f"double prefixes: {len(dbl)}"]
    + stale + left + dbl[:10])

# 16. ToC -------------------------------------------------------------------------------------
sl = slugs_for(L)
slug_count = Counter(sl.values())
pT = part("Table of Contents")
entries = [(n, m.group(1), m.group(2)) for n, ln in lines_of(pT) for m in [re.match(r"^\s*- \[(.*)\]\(#([^)]+)\)$", ln)] if m]
bad_e = [f"line {n}: #{s}" for n, _t, s in entries if slug_count.get(s, 0) != 1]
toc_slugs = set(s for _n, _t, s in entries)
missing_h = [f"line {i + 1}: {clean_heading(t)}" for i, lvl, t in HD if lvl in (2, 3) and clean_heading(t) != "Table of Contents" and sl[i] not in toc_slugs]
sep_ok = L[pT["end"] - 1] == "---"
rec("16 Table of Contents: every entry matches exactly one heading; every H2/H3 has an entry; `---` after the ToC",
    not bad_e and not missing_h and sep_ok,
    [f"entries {len(entries)} (H2 {sum(1 for i, lvl, t in HD if lvl == 2) - 1}, H3 {sum(1 for _i, lvl, _t in HD if lvl == 3)}, "
     f"H4 entries for 6.13 and 7.4 {sum(1 for n, _t, _s in entries if L[n - 1].startswith('    - '))})",
     f"entries without exactly one heading: {len(bad_e)}", f"H2/H3 without an entry: {len(missing_h)}", f"`---` after ToC: {sep_ok}"]
    + bad_e[:10] + missing_h[:10])

# 17. counts -------------------------------------------------------------------------------------
sec_rows = ["| H2 section | Start line | Lines | Headings (H2-H6) |", "|---|---|---|---|"]
h2pos = [(i + 1, clean_heading(t)) for i, lvl, t in HD if lvl == 2]
for k, (s, name) in enumerate(h2pos):
    e = h2pos[k + 1][0] - 1 if k + 1 < len(h2pos) else len(L)
    nh = sum(1 for i, _lvl, _t in HD if s <= i + 1 <= e)
    sec_rows.append(f"| {name[:70]} | {s} | {e - s + 1} | {nh} |")
lvl_count = Counter(lvl for _i, lvl, _t in HD)
r1 = len(re.findall(r"(?<![\w-])R1-[A-Za-z0-9]", text))
r25 = len(re.findall(r"R25-INV-\d{3}", text))
results["17 Counts (report)"] = ("INFO", [
    f"total lines: {len(L)}; bytes: {MERGED.stat().st_size}",
    f"headings by level: {dict(sorted(lvl_count.items()))}",
    f"R1- prefixed tokens: {r1}; R1-CLS-nn: {cls}; R25-INV-nnn: {r25}",
    f"new-text lines (assembler list): {len(NEW)}", ""] + sec_rows)

# ---------------------------------------------------------------- report
fails = [k for k, (s, _l) in results.items() if s == "FAIL"]
out = ["# E4 validation report (M-30)", "",
       f"File: `{MERGED.relative_to(ADV.parent)}`", f"Result: {'PASS' if not fails else 'FAIL: ' + ', '.join(fails)}", "",
       "Run by `adversarial/partials/merge-scripts/e4_validate.py` (read-only; this report is its only output).", ""]
for k, (s, lines) in results.items():
    out += [f"## {k}: {s}", ""] + lines + [""]
REPORT.write_text("\n".join(out), encoding="utf-8")
for k, (s, _l) in results.items():
    print(f"{s:4} {k}")
print("RESULT:", "PASS" if not fails else "FAIL " + ", ".join(fails))
sys.exit(1 if fails else 0)
