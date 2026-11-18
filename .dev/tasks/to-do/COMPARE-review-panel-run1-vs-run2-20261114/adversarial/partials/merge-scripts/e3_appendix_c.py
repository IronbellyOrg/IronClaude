#!/usr/bin/env python3
"""Merge executor E3: generate Appendix C (contradiction register, M-28 of refactor-plan.md).

Reads (read-only): diff-analysis.md (Contradictions table, Orchestrator Verification table),
partials/matrix.json (per-point winners), partials/scoring-matrix.md (confidence),
partials/r2-state.json (per-advocate point verdicts, used only to flag inherited verdicts).
Writes: partials/merge-stage/new-blocks/M28-appendix-C.md.
Run: uv run --no-project python e3_appendix_c.py
The "Where handled" column is a hand-kept map (WHERE) taken from refactor-plan.md M-00..M-29;
every other cell is derived from the artifacts.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ADV = Path(__file__).resolve().parents[2]
DIFF = (ADV / "diff-analysis.md").read_text(encoding="utf-8").split("\n")
MATRIX = json.loads((ADV / "partials" / "matrix.json").read_text(encoding="utf-8"))
SCORE = (ADV / "partials" / "scoring-matrix.md").read_text(encoding="utf-8").split("\n")
STATE = json.loads((ADV / "partials" / "r2-state.json").read_text(encoding="utf-8"))
OUT = ADV / "partials" / "merge-stage" / "new-blocks" / "M28-appendix-C.md"


def cells(line: str) -> list[str]:
    """Split a markdown table row on unescaped pipes."""
    parts = re.split(r"(?<!\\)\|", line.strip())
    return [p.strip() for p in parts[1:-1]]


# --- 1. contradiction rows -------------------------------------------------
start = DIFF.index("## Contradictions")
rows = {}
for ln in DIFF[start:]:
    if ln.startswith("### ") or (ln.startswith("## ") and ln != "## Contradictions"):
        break
    m = re.match(r"^\| (X-\d{3}) ", ln)
    if m:
        c = cells(ln)
        if m.group(1) == "X-054" and len(c) == 6:
            # the V1 cell quotes a table row ("C-17 | fix ...") with an unescaped pipe
            c = c[:2] + [c[2] + " \\| " + c[3]] + c[4:]
        assert len(c) == 5, (m.group(1), len(c))
        rows[m.group(1)] = c[1:]  # point, V1 position, V2 position, impact (id cell dropped)
assert len(rows) == 63, len(rows)
assert sorted(rows) == [f"X-{i:03d}" for i in range(1, 64)]

# --- 2. orchestrator verification -----------------------------------------
ostart = DIFF.index("## Orchestrator Verification of Contradictions (independent re-check, read-only, 2026-11-14)")
orch = {}
for ln in DIFF[ostart:]:
    if ln.startswith("## Appendix"):
        break
    if ln.startswith("| X-"):
        c = cells(ln)
        for xid in re.findall(r"X-\d{3}", c[0]):
            orch[xid] = c[4]
assert len(orch) == 25, len(orch)  # 14 groups; the artifact says "about 22 X rows", the table names 25
design_line = next(ln for ln in DIFF[ostart:] if ln.startswith("Rows left as design choices"))
DESIGN = set()
for a, b in re.findall(r"X-(\d{3})(?: to X-(\d{3}))?", design_line):
    DESIGN.update(f"X-{i:03d}" for i in range(int(a), int(b or a) + 1))
assert len(DESIGN) == 20, sorted(DESIGN)


def orch_class(v: str) -> str:
    if re.match(r"VERIFIED-(V1|V2|BOTH)", v):
        return "VERIFIED-" + re.match(r"VERIFIED-(V1|V2|BOTH)", v).group(1)
    if "status quo VERIFIED-BOTH" in v:
        return "status quo VERIFIED-BOTH (design choice)"
    if v.startswith("Fact VERIFIED-BOTH"):
        return "fact VERIFIED-BOTH (rating is a judgement)"
    if "(6)" in v:
        return "count: neither report's figure (5 lines, 7 occurrences)"
    raise SystemExit(f"unclassified orchestrator verdict: {v}")


# --- 3. debate verdicts ----------------------------------------------------
winners = MATRIX["winners"]
conf = {}
for ln in SCORE:
    m = re.match(r"^\| (X-\d{3}) .*?\| (CL-\d+) \| ([^|]+) \| (\d+)% \|", ln)
    if m:
        conf[m.group(1)] = (m.group(2), m.group(3).strip(), m.group(4))
assert len(conf) == 63, len(conf)
for x, (_, w, _) in conf.items():
    assert winners[x] == w, (x, winners[x], w)

NORM = {"V1": "Variant 1", "V2": "Variant 2", "BOTH": "Both (merge)", "MERGE": "Both (merge)",
        "OPEN": "Open (owner or evidence)"}
inherited = []
for x in rows:
    a = STATE["V1"]["point"].get(x)
    b = STATE["V2"]["point"].get(x)
    if a and b and NORM.get(a) == NORM.get(b) and NORM.get(a) != winners[x]:
        inherited.append((x, a, b, winners[x]))

# --- 4. where handled (from refactor-plan.md) -----------------------------
BASECORR_KEY = "base sites corrected in place (Appendix E, M-24 item 1)"
RF = "unit note at the base rf-* sites (Appendix E, M-24 item 7; counts with units)"
WHERE = {
    "X-001": "Baseline and Conventions, merge addendum; Merge Notes (e)",
    "X-002": "base delta table governs (V2:1134-1135); run 1's single contract in 3.6 and 7.4 (recorded alternative); 6.13.0 R1-C-01",
    "X-003": "base delta row G-03/G-17 governs; run 1's R1-D4 in 4.7; 6.13.0 R1-C-05",
    "X-004": "base A-3 and run 1's quorum rows both carried (3.6, 4.7); source of `requested` open in 9.12",
    "X-005": "base A-13 (C-05) governs; run 1's R1-MS-08 (4.7) and R1-Q-03 (9.11) as run 1's view; 7.0.2 C-05",
    "X-006": "base 7.1 I-4 governs; run 1's R1-SC-11 (3.6) and R1-BL-03 (4.7) as run 1's view",
    "X-007": "base C-10 / A-14 governs; run 1's R1-BL-18 (4.7) and R1-M4-04 (8.4, status CONFLICTS)",
    "X-008": "7.0.2 C-11 (changed, OPEN); 9.12 per-slot keys",
    "X-009": "base C-07 governs; run 1's R1-MS-06 and R1-MS-20 (4.7); 6.13.0 R1-C-09",
    "X-010": "7.0.2 C-08 and X-14; 6.13.0 R1-C-07",
    "X-011": "4.7 lead (both ratings shown; the base rating cell is not edited)",
    "X-012": "4.7 lead (both ratings shown)",
    "X-013": "4.7 lead (both ratings shown; the base rating cell is not edited)",
    "X-014": "4.7 lead (both ratings shown; the base rating cell is not edited)",
    "X-015": "4.7 lead (both ratings shown; the base rating cell is not edited)",
    "X-016": "4.7 lead (both ratings shown)",
    "X-017": "4.7 lead (both ratings shown); base count \"(6)\" corrected (Appendix E, M-24 item 8)",
    "X-018": "4.7 lead (both ratings shown; the base rating cell is not edited)",
    "X-019": "4.7 lead (both ratings shown; split per row)",
    "X-020": BASECORR_KEY,
    "X-021": "base sites V2:874, 1027, 1368, 3743 corrected (Appendix E, M-24 item 13)",
    "X-022": RF,
    "X-023": "note at the base key-count sites (Appendix E, M-24 item 6; counts with units)",
    "X-024": "note at the base key-count sites (Appendix E, M-24 item 6; counts with units)",
    "X-025": "carried run 1 text corrected in 2.10 (Appendix E, M-25, V1:204)",
    "X-026": "carried run 1 text corrected in 2.10 (Appendix E, M-25, V1:201)",
    "X-027": "note at base V2:215 (Appendix E, M-24 item 10)",
    "X-028": "note at base V2:216, 874 (Appendix E, M-24 item 11)",
    "X-029": RF,
    "X-030": "base tags corrected at V2:891, 3323, 1033, 3474 (Appendix E, M-24 item 3); run 1's text kept",
    "X-031": "carried run 1 text corrected in 2.10 (Appendix E, M-25, V1:305)",
    "X-032": "note in base 2.1 / 2.9.0 (Appendix E, M-24 item 12)",
    "X-033": "base 2.7 governs; run 1's 2.6 matrix not carried (M-03)",
    "X-034": "base 2.4 governs (verified by run 2 only); run 1's 2.3 not carried (M-03)",
    "X-035": "both lists carried (base 5.4.1; run 1 in 5.6); not fetched",
    "X-036": "base sentences marked [SOURCE WITHDRAWN] (Appendix E, M-24 item 2); run 1's exclusion carried in 5.6",
    "X-037": "both carried (base 5.4.4; run 1 in 5.6); not fetched",
    "X-038": "7.0.2 C-01; run 1's start point in 6.13 and 7.4 (recorded alternative)",
    "X-039": "base 6.4 governs; 6.13.0 R1-C-05",
    "X-040": "9.12 claim cut; 7.0.2 C-06; 6.13.0 R1-C-02",
    "X-041": "9.12 distinctness default; 7.0.2 C-09; 6.13.0 R1-C-04",
    "X-042": "7.0.2 C-01; 6.13.0 R1-C-12; 9.12 (R25-INV-024, R25-INV-029)",
    "X-043": "7.0.2 C-04; 6.13.0 R1-C-17; 9.12 post-gate engine",
    "X-044": "base 6.4 governs; 6.13.0 R1-C-19",
    "X-045": "base C-07 governs; 6.13.0 R1-C-09",
    "X-046": "7.0.2 C-02; 6.13.0 R1-C-13; version skew in 8.6 and 9.12",
    "X-047": "base C-05 governs; run 1's 6.D row R1-D14 in 6.13; 7.0.2 C-05",
    "X-048": "base tags corrected at V2:891, 3323, 1033, 3474 (Appendix E, M-24 item 3); run 1's text kept",
    "X-049": BASECORR_KEY,
    "X-050": "6.13.0 R1-C-08",
    "X-051": "Merge Notes (a); 3.6 and 7.4 lead sentences (both positions)",
    "X-052": "head note of 6.13 and lead of 6.13.0",
    "X-053": BASECORR_KEY,
    "X-054": "7.0.2 C-04; 6.13.0 R1-C-17; 9.12 post-gate engine",
    "X-055": "base A-4 and 6.4 govern; 6.13.0 R1-C-05",
    "X-056": "9.12 claim cut; 7.0.2 C-06; 6.13.0 R1-C-02",
    "X-057": "9.12 distinctness default; 7.0.2 C-09; 6.13.0 R1-C-04",
    "X-058": "9.12 exit code 12; 7.0.2 C-03; 6.13.0 R1-C-19",
    "X-059": "base C-10 / A-14 governs; run 1's R1-M4-04 (8.4, status CONFLICTS)",
    "X-060": "base A-13 (C-05) governs; run 1's R1-Q-03 (9.11) as run 1's view; 7.0.2 C-05",
    "X-061": RF,
    "X-062": "Baseline and Conventions, merge addendum; Merge Notes (e)",
    "X-063": "Baseline and Conventions, merge addendum; Merge Notes (f)",
}
assert sorted(WHERE) == sorted(rows)

# Notes on design rows whose debate outcome changes a run 2 adjudicated default.
CHANGES = {
    "X-008": "changes run 2's C-11 withdrawal; not re-debated",
    "X-043": "changes run 2's C-04 default; not re-debated; OPEN owner decision",
    "X-054": "changes run 2's C-04 default; not re-debated; OPEN owner decision",
    "X-042": "applying the remedy to both clusterers meets T-c; OPEN owner decision",
}


# --- 5. cell shortening ----------------------------------------------------
CITE = re.compile(r"\bV[12]:\d+(?:-\d+)?")
MARK = re.compile(r"\s(?:Verification:|VERIFIED|UNVERIFIED|Facts agree)")


def balance(text: str) -> str:
    if text.count("`") % 2:
        text += "`"
    if text.count("(") > text.count(")"):
        text += ")" * (text.count("(") - text.count(")"))
    if len(re.findall(r'(?<!\\)"', text)) % 2:
        text += '"'
    return text


def short(text: str, side: str, limit: int = 230) -> str:
    text = re.sub(r"\bL(\d{2,4})(?=\b)", lambda m: f"{side}:{m.group(1)}", text)
    text = re.sub(rf"\b{side} {side}:", f"{side}:", text)  # "(V1 L3019)" -> "(V1:3019)"
    m = MARK.search(text)
    if m:
        text = text[: m.start()].rstrip(" .;:")
        if len(re.findall(r'(?<!\\)"', text)) % 2:  # the marker sat inside a quote
            text += ' …"'
        text = balance(text)
    full_cites = list(dict.fromkeys(CITE.findall(text)))
    if len(text) > limit:
        cut = text.rfind(" ", 0, limit)
        text = balance(text[: cut if cut > 0 else limit].rstrip(" ,;:("))
        missing = [c for c in full_cites if c not in text]
        text += " …" + (f" ({', '.join(missing)})" if missing else "")
    return text


def point(text: str) -> str:
    return re.sub(r"\s*\[src [^\]]+\]", "", text)


RATING = {f"X-{i:03d}" for i in range(11, 20)}
# Facts re-checked outside the orchestrator table, by the named artifact.
EXTRA = {
    "X-036": ("withdrawn source (fault-finder fetch of arxiv.org/abs/2606.19544, notes section 1 row 26; "
              "run 2 QA P6-054)"),
}


def resolution(x: str) -> tuple[str, str]:
    """Return (category, cell)."""
    cl, w, pct = conf[x]
    if w == "Open (owner or evidence)":
        return "OPEN", "OPEN (both advocates: not decidable by the evidence; owner decision); both versions stand"
    if w == "Unresolved split":
        return "OPEN (label split)", (
            "OPEN, label split: run 1 advocate Both (run 1's core kept as the one-engine target), "
            "run 2 advocate Variant 2 governing with run 1 detail carried; run 2's shape governs as the adjudicated default")
    debate = f"debate: {'severity rating, ' if x in RATING else ''}{w} ({pct}%)"
    if x in orch:
        oc = orch_class(orch[x])
        cat, res = f"{oc} (orchestrator)", f"{oc} (orchestrator); {debate}"
    elif x in EXTRA:
        cat, res = "fact re-checked (fault-finder)", f"{EXTRA[x]}; {debate}"
    elif x in DESIGN:
        cat, res = "design choice (orchestrator list)", f"design choice, not falsifiable by code (orchestrator list); {debate}"
    else:
        tag = re.search(r"\[?(VERIFIED-(?:V1|V2|BOTH)|UNVERIFIED)", " ".join(rows[x][2:]))
        cat = f"analyst {tag.group(1)}" if tag else "debate verdict only"
        res = f"{cat}; {debate}"
    if x in CHANGES:
        res += f"; {CHANGES[x]}"
    return cat, res


# --- 6. output -------------------------------------------------------------
out = [
    "<!-- Source: new text — merged per Change #M-28 -->",
    "",
    "## Appendix C: Contradiction register (run 1 vs run 2)",
    "",
    "Generated by `adversarial/partials/merge-scripts/e3_appendix_c.py` from `diff-analysis.md` (section Contradictions, 63 rows X-001 to X-063, and section \"Orchestrator Verification of Contradictions\"), `partials/matrix.json` and `partials/scoring-matrix.md`. "
    "Columns 2 to 4 are the diff analysts' cells, shortened (a cut is marked `…` and keeps the cut line citations in brackets; the analysts' verification notes are left out of the position columns); `L<n>` in a position cell is written `V1:<n>` or `V2:<n>`. Inside the quoted position cells, ids keep each report's own spelling: a run 1 id there (for example BL-18 or C-17) has no `R1-` prefix, and a two-digit C-nn there is that report's own id. "
    "Resolution: a fact the compare orchestrator re-derived is marked VERIFIED-V1, VERIFIED-V2 or VERIFIED-BOTH (or \"status quo VERIFIED-BOTH (design choice)\" where only today's code was checked); a row the orchestrator lists as a design choice that code cannot falsify is marked so; X-036 cites the fault-finder's fetch; otherwise the analysts' tag is named when the row has one. Every row also gives the final point verdict of the debate and its confidence (for X-011 to X-019 the verdict is on the severity rating; the facts agree). "
    "A row resolved OPEN shows both versions in columns 3 and 4. \"Where handled\" names the place in this document; ids `R1-…` are run 1 ids, three-digit C-/X- ids are compare diff ids.",
    "",
    "| X id | Point | Variant 1 (run 1) position | Variant 2 (run 2) position | Resolution | Where handled in this document |",
    "|---|---|---|---|---|---|",
]
counts = {}
for x in sorted(rows):
    c = rows[x]
    key, res = resolution(x)
    counts[key] = counts.get(key, 0) + 1
    out.append("| " + " | ".join([x, point(c[0]), short(c[1], "V1"), short(c[2], "V2"), res, WHERE[x]]) + " |")
assert sum(counts.values()) == 63
out += ["", "Rows by basis of the resolution: " + "; ".join(f"{k}: {v}" for k, v in sorted(counts.items())) + " (63 rows; each row also carries the debate's point verdict)."]
OUT.write_text("\n".join(out) + "\n", encoding="utf-8")

print("rows", len(rows), "orch", len(orch), "conf", len(conf))
print("counts", counts)
print("inherited-verdict flags (both advocates agree, matrix differs):", inherited or "none")
print("open/split rows:", [x for x in sorted(rows) if conf[x][1] in ("Open (owner or evidence)", "Unresolved split")])
print("written", OUT)
