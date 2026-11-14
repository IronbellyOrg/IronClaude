#!/usr/bin/env python3
"""Quantitative layer (scoring-protocol A.1) for slot C-04 reflect-tier2-engine-composition.

Deterministic, stdlib only. Reads variant-1-original.md (Proposal A) and
variant-2-original.md (Proposal B) next to this script and writes
quant-score-output.json and quant-score.md next to it. No timestamps, no randomness.

quant_score = RC*0.30 + IC*0.25 + SR*0.15 + DC*0.15 + SC*0.15

Run: uv run --no-project python quant-score.py
"""
import json
import re
from pathlib import Path

ADV = Path(__file__).resolve().parent
VARIANTS = {
    "variant_1": ADV / "variant-1-original.md",
    "variant_2": ADV / "variant-2-original.md",
}
WEIGHTS = {"RC": 0.30, "IC": 0.25, "SR": 0.15, "DC": 0.15, "SC": 0.15}

# ---------------------------------------------------------------- RC
# Source row C-04 of phase-outputs/discovery/undecidable-conflicts.md:
#   conflicts column  : RE-1, RE-4, CV-8 (intent), CV-4, CV-5
#   invariants column : INV-A (HIGH), INV-B (HIGH), INV-L (HIGH), INV-M (MEDIUM), INV-K (MEDIUM)
#   evidence column   : "06, 11, 01, 07; GQ-067"  (06/11/01/07 are research file numbers, not IDs)
# The list given in the assignment matches the row text exactly.
SOURCE_IDS = ["RE-1", "RE-4", "CV-8", "CV-4", "CV-5",
              "INV-A", "INV-B", "INV-L", "INV-M", "INV-K", "GQ-067"]

# ---------------------------------------------------------------- IC
# Intra-variant contradictions. Rule: a pair (or triple) of statements inside ONE variant
# that cannot both hold, where diff-analysis.md gives the evidence (intra rows X-008, X-009,
# or the intra side of an inter row together with its code-ledger row V-nn, or its own
# "also inconsistent inside B" note). Quotes are verified against the line text at run time.
CONTRADICTIONS = {
    "variant_1": [
        {"id": "X-008", "basis": "diff-analysis X-008 (intra-A), V-28",
         "statements": [(133, "headless output directories"),
                        (141, "passes the lint")],
         "note": "INV-M row says headless output directories are Preserved; M4 says a stub-lane "
                 "run passes the 1.8.0 lint, which reads directories the headless lane does not create."},
        {"id": "X-007(A side)", "basis": "own scan; diff-analysis X-007 and V-15",
         "statements": [(88, "that is a skill text edit"),
                        (121, "the `### 9.1` block is not edited"),
                        (131, "SKILL.md edits stay under")],
         "note": "Section 3.5 reconciles prose at SKILL.md :703, :839, :1317, :1481 as a text edit, "
                 "while INV-K says edits stay under ### 4.3a and INV-A says the ### 9.1 block is not "
                 "edited; V-15 shows those lines sit outside the allow-list and :838-839 inside 9.1."},
    ],
    "variant_2": [
        {"id": "X-009", "basis": "diff-analysis X-009 (intra-B), V-08",
         "statements": [(24, "CV-5 `merge_method: adversarial` means a disk-confirmed merge"),
                        (34, "own meaning and that EV-2")],
         "note": "Section 1 (i) says CV-5 makes adversarial mean a disk-confirmed merge; section 2 keeps "
                 "the count-derived label as engine A's own meaning."},
        {"id": "X-006(B side)", "basis": "own scan; diff-analysis X-006 ('also inconsistent inside B'), V-32",
         "statements": [(24, 'GQ-067: "does the wrapper switch to engine B'),
                        (149, "GQ-067 / OQ-8: readers outside")],
         "note": "Section 1 (and the section 5 trigger) uses GQ-067 as the owner question about the "
                 "wrapper switching engines; section 8 defines GQ-067/OQ-8 as the readers-of-ten-keys question."},
    ],
}
# strict variant of IC: only the two rows diff-analysis marks intra (X-008, X-009)
STRICT_IDS = {"X-008", "X-009"}

# claim proxy (identical for both variants)
TAG_RE = re.compile(r"\[(?:CODE-VERIFIED|UNVERIFIED|CODE-CONTRADICTED)")
CIT_RE = re.compile(r"(?<![\w/.-])(?:[\w./-]+\.(?:py|md|json|yaml|yml|sh|txt|toml))?"
                    r":\d{1,5}(?:-\d{1,5})?(?!\w)")
NUM_RE = re.compile(r"(?<![\w./-])\d+(?:\.\d+)?%?(?![\w-])")
META_RE = re.compile(r"^(?:Status|Position|Date|Code state|Writer|HEAD read at|Slot|Tag key[^:]*):")
SEP_RE = re.compile(r"^\|[\s:|-]+\|\s*$")

# SR vague indicators
VAGUE_RE = re.compile(
    r"\b(?:appropriate(?:ly)?|as needed|properly|adequate(?:ly)?|should consider|might|various|"
    r"best practices?|industry standard)\b|\betc\b\.?", re.I)
BACKTICK_RE = re.compile(r"`([^`\n]+)`")


def classify(lines):
    """Return list of dicts: n (1-based), text, kind, section (current H2 number or None)."""
    out = []
    seen_h2 = False
    section = None
    for i, text in enumerate(lines):
        n = i + 1
        s = text.strip()
        if text.startswith("## "):
            seen_h2 = True
            m = re.match(r"^## (\d+)", text)
            section = m.group(1) if m else text[3:].strip()
        if not s:
            kind = "blank"
        elif re.match(r"^#{1,6}\s", text):
            kind = "heading"
        elif (not seen_h2) or META_RE.match(s):
            kind = "meta"
        elif SEP_RE.match(s):
            kind = "sep"
        elif s.startswith("|"):
            nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
            kind = "table_header" if SEP_RE.match(nxt) else "table_row"
        else:
            kind = "text"
        out.append({"n": n, "text": text, "kind": kind, "section": section})
    return out


def count_claims(rows):
    c = 0
    for r in rows:
        if r["kind"] == "table_row":
            c += 1
        elif r["kind"] == "text":
            t = r["text"]
            if TAG_RE.search(t) or CIT_RE.search(t) or NUM_RE.search(t):
                c += 1
    return c


def specificity(rows):
    cit = ident = num = vague = 0
    for r in rows:
        if r["kind"] not in ("text", "table_row"):
            continue
        t = r["text"]
        vague += len(VAGUE_RE.findall(t))
        cits = CIT_RE.findall(t)
        cit += len(cits)
        t = CIT_RE.sub("\x00", t)
        for m in BACKTICK_RE.finditer(t):
            if re.sub(r"[\x00\s,:-]", "", m.group(1)):
                ident += 1
        t = BACKTICK_RE.sub("\x00", t)
        num += len(NUM_RE.findall(t))
    concrete = cit + ident + num
    sr = concrete / (concrete + vague) if (concrete + vague) else 0.0
    return {"citations": cit, "backtick_identifiers": ident, "numbers": num,
            "concrete": concrete, "vague": vague, "SR": sr}


# ---------------------------------------------------------------- DC
SEC_P1 = re.compile(r"(?:\bsections?|§)\s*(\d+(?:\.\d+)*(?:\s*(?:,|and|to|&)\s*\d+(?:\.\d+)*)*)", re.I)
SEC_P2 = re.compile(r"\b(?:see|in|under)\s+(\d\.\d(?:\.\d)?)(?![\d])", re.I)
SEC_P3 = re.compile(r"\((\d+\.\d+)\)")
EXT_BEFORE = re.compile(r"(?:research/\d+|\br\d{2}\b|\bs\d{2}\b|synth-\d+|\bSKILL\b|refs/)")
E_RE = re.compile(r"\bE(\d{1,2})\b")
M_RE = re.compile(r"\bM(\d{1,2})\b")
INV_RE = re.compile(r"\bINV-([A-N])\b")


def ext_context(text, start):
    return bool(EXT_BEFORE.search(text[max(0, start - 36):start]))


def internal_refs(rows):
    # definitions -----------------------------------------------------------
    sections, e_defs, m_defs, inv_defs = set(), set(), set(), set()
    for r in rows:
        t = r["text"]
        if r["kind"] == "heading":
            m = re.match(r"^#{2,4}\s+(\d+(?:\.\d+)*)[.\s]", t)
            if m:
                sections.add(m.group(1))
        m = re.match(r"^\|\s*(E\d+)\s*\|", t)
        if m:
            e_defs.add(m.group(1))
        m = re.match(r"^\|\s*(M\d+)\s*\|", t) or re.match(r"^\s*[-*]\s+(M\d+)\b", t)
        if m and r["kind"] in ("text", "table_row"):
            m_defs.add(m.group(1))
        m = re.match(r"^\|\s*INV-([A-N])\b", t)
        if m:
            inv_defs.add("INV-" + m.group(1))
    # sections that cite research/13 section 8 use that file's M1-M14 labels, not this doc's
    r13_sections = {r["section"] for r in rows if "research/13 section 8" in r["text"]}
    # references ------------------------------------------------------------
    refs = []
    for r in rows:
        if r["kind"] not in ("text", "table_row", "table_header"):
            continue
        t, n = r["text"], r["n"]
        seen = set()
        for pat in (SEC_P1, SEC_P2, SEC_P3):
            for m in pat.finditer(t):
                if (m.start(1) in seen) or ext_context(t, m.start()):
                    continue
                seen.add(m.start(1))
                for num in re.findall(r"\d+(?:\.\d+)*", m.group(1)):
                    refs.append({"line": n, "kind": "section", "ref": num,
                                 "resolved": num in sections, "text": m.group(0)})
        first_cell_end = t.index("|", 1) if t.startswith("|") and "|" in t[1:] else 0
        defs_row = re.match(r"^\|\s*E\d+\s*\|", t) is not None
        for m in E_RE.finditer(t):
            if defs_row and m.start() < first_cell_end:
                continue
            if re.match(r"-F\d", t[m.end():m.end() + 3]):
                continue
            if m.group(0) == "E1" and ("research/07" in t or "r07" in t):
                continue
            lab = "E" + m.group(1)
            refs.append({"line": n, "kind": "E", "ref": lab, "resolved": lab in e_defs, "text": lab})
        for m in M_RE.finditer(t):
            lab = "M" + m.group(1)
            lead = re.match(r"^(?:\|\s*|\s*[-*]\s+)" + lab + r"\b", t)
            if lead and m.start() == lead.end() - len(lab):
                continue  # definition position
            before = t[max(0, m.start() - 12):m.start()]
            if re.search(r"(?:r13|research/13)\s+(?:row\s+)?$", before):
                continue
            if r["section"] in r13_sections and not before.endswith("measurement "):
                continue
            refs.append({"line": n, "kind": "M", "ref": lab, "resolved": lab in m_defs, "text": lab})
        for m in INV_RE.finditer(t):
            lab = "INV-" + m.group(1)
            lead = re.match(r"^\|\s*" + lab + r"\b", t)
            if lead and m.start() == lead.end() - len(lab):
                continue  # definition position
            refs.append({"line": n, "kind": "INV", "ref": lab, "resolved": lab in inv_defs, "text": lab})
    total = len(refs)
    resolved = sum(1 for x in refs if x["resolved"])
    return {"total": total, "resolved": resolved,
            "DC": (resolved / total) if total else 1.0,
            "defined": {"sections": sorted(sections), "E": sorted(e_defs),
                        "M": sorted(m_defs), "INV": sorted(inv_defs)},
            "unresolved": [x for x in refs if not x["resolved"]],
            "all_refs": refs}


def main():
    result = {"formula": "quant_score = RC*0.30 + IC*0.25 + SR*0.15 + DC*0.15 + SC*0.15",
              "weights": WEIGHTS, "source_ids": SOURCE_IDS, "variants": {}}
    h2_counts = {}
    for key, path in VARIANTS.items():
        text = path.read_text(encoding="utf-8")
        lines = text.split("\n")
        rows = classify(lines)
        h2_counts[key] = sum(1 for ln in lines if ln.startswith("## "))
        # RC
        found, missing = [], []
        for i in SOURCE_IDS:
            pat = re.compile(r"(?<![A-Za-z0-9])" + re.escape(i) + r"(?![A-Za-z0-9])")
            (found if pat.search(text) else missing).append(i)
        rc = len(found) / len(SOURCE_IDS)
        # IC
        claims = count_claims(rows)
        cons = []
        for c in CONTRADICTIONS[key]:
            quotes = []
            for ln, snip in c["statements"]:
                assert snip in lines[ln - 1], f"{key} line {ln}: snippet not found: {snip!r}"
                quotes.append({"line": ln, "quote": snip})
            cons.append({"id": c["id"], "basis": c["basis"], "statements": quotes, "note": c["note"]})
        ic = 1 - len(cons) / claims
        strict_n = sum(1 for c in cons if c["id"] in STRICT_IDS)
        ic_strict = 1 - strict_n / claims
        # SR, DC
        sr = specificity(rows)
        dc = internal_refs(rows)
        result["variants"][key] = {
            "file": path.name,
            "RC": {"found": found, "missing": missing, "matched": len(found),
                   "total": len(SOURCE_IDS), "value": rc},
            "IC": {"total_claims": claims, "contradictions": len(cons), "value": ic,
                   "strict_value_diff_analysis_intra_rows_only": ic_strict,
                   "contradiction_list": cons},
            "SR": sr,
            "DC": {k: v for k, v in dc.items() if k != "all_refs"},
            "DC_all_refs": dc["all_refs"],
            "SC": {"h2_count": h2_counts[key]},
        }
    mx = max(h2_counts.values())
    for key, v in result["variants"].items():
        v["SC"]["max_h2"] = mx
        v["SC"]["value"] = v["SC"]["h2_count"] / mx
        parts = {"RC": v["RC"]["value"], "IC": v["IC"]["value"], "SR": v["SR"]["SR"],
                 "DC": v["DC"]["DC"], "SC": v["SC"]["value"]}
        v["metrics"] = {k: round(x, 6) for k, x in parts.items()}
        v["quant_score"] = round(sum(parts[k] * WEIGHTS[k] for k in WEIGHTS), 6)
        strict = dict(parts)
        strict["IC"] = v["IC"]["strict_value_diff_analysis_intra_rows_only"]
        v["quant_score_ic_strict"] = round(sum(strict[k] * WEIGHTS[k] for k in WEIGHTS), 6)

    (ADV / "quant-score-output.json").write_text(
        json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    (ADV / "quant-score.md").write_text(render_md(result), encoding="utf-8")


def f(x):
    return f"{x:.4f}"


def render_md(res):
    a, b = res["variants"]["variant_1"], res["variants"]["variant_2"]
    L = ["# Quantitative layer (A.1) - slot C-04 reflect-tier2-engine-composition", "",
         "Variant 1 = Proposal A (compose). Variant 2 = Proposal B (reconcile at the contract). "
         "Produced by `quant-score.py` (stdlib, deterministic); numbers in `quant-score-output.json`.", "",
         "`quant_score = RC*0.30 + IC*0.25 + SR*0.15 + DC*0.15 + SC*0.15`", "",
         "| Metric | Weight | Variant 1 (A) | Variant 2 (B) | Basis |", "|---|---|---|---|---|"]
    L.append(f"| RC requirement coverage | 0.30 | {f(a['RC']['value'])} ({a['RC']['matched']}/{a['RC']['total']}) | "
             f"{f(b['RC']['value'])} ({b['RC']['matched']}/{b['RC']['total']}) | ID regex over whole file |")
    L.append(f"| IC internal consistency | 0.25 | {f(a['IC']['value'])} ({a['IC']['contradictions']}/{a['IC']['total_claims']}) | "
             f"{f(b['IC']['value'])} ({b['IC']['contradictions']}/{b['IC']['total_claims']}) | 1 - contradictions/claim lines |")
    L.append(f"| SR specificity ratio | 0.15 | {f(a['SR']['SR'])} ({a['SR']['concrete']} / {a['SR']['concrete'] + a['SR']['vague']}) | "
             f"{f(b['SR']['SR'])} ({b['SR']['concrete']} / {b['SR']['concrete'] + b['SR']['vague']}) | concrete/(concrete+vague) |")
    L.append(f"| DC dependency completeness | 0.15 | {f(a['DC']['DC'])} ({a['DC']['resolved']}/{a['DC']['total']}) | "
             f"{f(b['DC']['DC'])} ({b['DC']['resolved']}/{b['DC']['total']}) | resolved/total internal refs |")
    L.append(f"| SC section coverage | 0.15 | {f(a['SC']['value'])} ({a['SC']['h2_count']}/{a['SC']['max_h2']}) | "
             f"{f(b['SC']['value'])} ({b['SC']['h2_count']}/{b['SC']['max_h2']}) | H2 count / max |")
    L.append(f"| **quant_score** | 1.00 | **{f(a['quant_score'])}** | **{f(b['quant_score'])}** | weighted sum |")
    L.append(f"| quant_score, IC from diff-analysis intra rows only (X-008, X-009) | | {f(a['quant_score_ic_strict'])} | "
             f"{f(b['quant_score_ic_strict'])} | sensitivity |")
    L += ["", "## Rules", "",
          "- RC source list (row C-04, verified against the row text): " + ", ".join(res["source_ids"]) +
          ". `06, 11, 01, 07` in the row are research file numbers, not IDs. Match = whole-token regex anywhere in the file.",
          "- IC claim proxy (same for both): non-heading, non-metadata, non-separator lines that are table body rows, "
          "or contain a `[CODE-VERIFIED]`/`[UNVERIFIED]`/`[CODE-CONTRADICTED]` tag, a file:line or `:NNN` citation, or a number. "
          "Metadata = lines before the first H2 and `Status:`/`Position:`/`Date:`/`Code state:`/`Writer:`/`HEAD read at:`/`Slot:` lines. "
          "Contradiction = pair of statements inside one variant that cannot both hold, evidenced by diff-analysis.md (intra rows X-008, X-009; "
          "intra side of X-007 and X-006 with ledger rows V-15, V-32).",
          "- SR: concrete = file:line citations + backtick identifiers (not pure citations) + standalone numbers (IDs such as CV-8, r06, s6.2 excluded); "
          "vague = appropriate/as needed/properly/adequate/should consider/might/various/etc./best practice(s)/industry standard. "
          "Headings, metadata, blank and table-separator/header lines excluded.",
          "- DC scope: `section N`/`sections N and M`/`§N`, `see|in|under N.M`, parenthesised `(N.M)`, `E<N>`, `INV-<A-N>`, `M<N>` labels. "
          "Resolved = heading number, table-row first cell (E, INV, M) or bullet-leading M label defined in the same file. "
          "Excluded as external: references within 36 chars after `research/NN`, `rNN`, `sNN`, `synth-NN`, `SKILL`, `refs/`; `E1-F<N>` and E1 on lines citing research/07 "
          "(research experiment labels); M labels preceded by `r13`/`research/13` (optionally plus `row`), and M labels in a section citing `research/13 section 8` unless preceded by `measurement`.",
          "- SC: lines matching `^## `, divided by the larger of the two counts.", ""]
    for name, v in (("Variant 1 (A)", a), ("Variant 2 (B)", b)):
        L += [f"## {name}", "",
              f"- Missing requirement IDs: {', '.join(v['RC']['missing']) if v['RC']['missing'] else 'none'}",
              f"- SR counts: citations {v['SR']['citations']}, backtick identifiers {v['SR']['backtick_identifiers']}, "
              f"numbers {v['SR']['numbers']}, vague {v['SR']['vague']}",
              f"- Defined internal targets: sections {', '.join(v['DC']['defined']['sections'])}; "
              f"E {', '.join(v['DC']['defined']['E']) or 'none'}; M {', '.join(v['DC']['defined']['M']) or 'none'}; "
              f"INV {', '.join(v['DC']['defined']['INV']) or 'none'}",
              "- Intra-variant contradictions:"]
        for c in v["IC"]["contradiction_list"]:
            qs = "; ".join(f"line {q['line']}: \"{q['quote']}\"" for q in c["statements"])
            L.append(f"  - {c['id']} ({c['basis']}): {qs}. {c['note']}")
        L.append("- Unresolved internal references:")
        if v["DC"]["unresolved"]:
            for u in v["DC"]["unresolved"]:
                L.append(f"  - line {u['line']}: {u['kind']} `{u['ref']}` (matched `{u['text']}`)")
        else:
            L.append("  - none")
        L.append("")
    return "\n".join(L)


if __name__ == "__main__":
    main()
