#!/usr/bin/env python3
"""Quantitative layer (Step 3, scorer pass 1) for slot C-06 limits-repair-policy.

Run: uv run python quant-score.py
Reads variant-1-original.md (A) and variant-2-original.md (B) from this folder,
prints a JSON document and writes the same text to quant-score-output.json.
Deterministic: no clock, no randomness, sorted keys. The only judgement input is
the CONTRADICTIONS table below, which the scorer filled in by reading both
variants (each entry quotes both sides).

Metric choices (printed under "definitions" in the output):
  RC  14 source requirements; a requirement matches when >= 3 of its keyword
      stems are present (case-insensitive substring; "a|b" = either).
  IC  1 - contradictions / scorable_claims. Claims = sentences (prose lines
      split at ". ", "! ", "? " before an upper-case, backtick, bracket or
      paren start) and table rows (one unit per row) that contain a digit, a
      file:line cite, or a [CODE-VERIFIED]/[UNVERIFIED]/[CODE-CONTRADICTED]/
      [RECOMPUTED] tag. Headings, blank lines and table separator rows are not
      units. Contradictions = the CONTRADICTIONS table.
  SR  concrete/(concrete+vague). Body = all lines after the first 6 lines,
      minus headings, blank lines, table separators. concrete = body lines with
      a digit, a file:line cite or a backticked code identifier. vague =
      occurrences of the listed hedge phrases in the body.
  DC  internal refs = "section N" / "section N.N" (any case) in the text;
      resolved when a heading numbered N / N.N exists; a ref directly after a
      "research/..." token is external and excluded.
  SC  H2 ("## ") count / max H2 count over the two variants.
  quant_score = RC*0.30 + IC*0.25 + SR*0.15 + DC*0.15 + SC*0.15
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
VARIANTS = {
    "A": HERE / "variant-1-original.md",
    "B": HERE / "variant-2-original.md",
}

REQS = [
    ("R01", "policy for over-limit anchor/anchor2/claim lines", ["anchor", "claim", "200", "300", "over-limit|over limit|exceed|longer"]),
    ("R02", "bounded re-ask", ["re-ask", "one", "bounded"]),
    ("R03", "itemised record of dropped/repaired lines", ["itemis|itemiz|record", "dropped", "line"]),
    ("R04", "fail-closed handling of a dropped blocking line", ["blocking", "fail", "refus|fail-closed|fail closed"]),
    ("R05", "raise-the-limits / constants option", ["raise|raising", "limit", "constants"]),
    ("R06", "INV-C (findings-v1 grammar and review merge unchanged)", ["INV-C", "grammar|findings-v1", "merge"]),
    ("R07", "INV-I (a review that did not happen never certifies PASS)", ["INV-I", "PASS", "review"]),
    ("R08", "INV-G (reviewers blind and read-only)", ["INV-G", "blind|read-only|mutually", "reviewer"]),
    ("R09", "a test or measurement that shows the position right or wrong", ["measurement|replay", "wrong", "test"]),
    ("R10", "effect on PR code review and rf-qa", ["PR", "rf-qa", "review"]),
    ("R11", "strongest objection and answer", ["objection", "answer", "strongest"]),
    ("R12", "consistency with adjudicated slots C-01, C-02, C-03", ["C-01", "C-02", "C-03"]),
    ("R13", "both parsers / loss unit (v1 finding vs v2 reviewer)", ["v1", "v2", "loss unit|unit"]),
    ("R14", "the audit-D figures (92 dropped, 49 blocking, 88, 48)", ["92", "49", "88|48"]),
]

VAGUE = [
    "appropriate", "as needed", "properly", "adequate", "should consider",
    "might", "various", "etc.", "best practices", "industry standard",
]

TAG_RE = re.compile(r"\[(CODE-VERIFIED|UNVERIFIED|CODE-CONTRADICTED|RECOMPUTED)")
FILE_CITE_RE = re.compile(r"[\w/.\-]+\.(py|md|json|tsv|yaml|yml|sh):\d")
CODE_SPAN_RE = re.compile(r"`[^`\n]+`")
SEP_RE = re.compile(r"^\s*\|?[\s\-:|]+\|?\s*$")
HEADING_RE = re.compile(r"^#{1,6}\s")
NUM_HEADING_RE = re.compile(r"^#{2,6}\s+(\d+(?:\.\d+)*)\.?\s")
SECTION_REF_RE = re.compile(r"\b[Ss]ections?\s+(\d+(?:\.\d+)*)")
EXTERNAL_PREFIX_RE = re.compile(r"research/[\w\-./`]*\s*$")
SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z`\[(*])")
BULLET_RE = re.compile(r"^\s*(?:[-*]|\d+\.)\s+")

# Intra-variant contradictions identified by reading (quote both sides).
CONTRADICTIONS = {
    "A": [
        {
            "id": "A-X1",
            "side1": "section 1: \"It touches no field the limits do not name.\"",
            "side2": "section 5 'Reference tokens survive the cut': \"The step therefore copies any reference token found only in the cut text into `refs` while it has room (cap 8), and records `refs_lost` otherwise.\" (A itself adds: \"it is not in E2 R-02\")",
            "why": "The step writes to `refs`, which is not one of the fields the limits name (anchor, anchor2, quote, claim).",
        },
        {
            "id": "A-X2",
            "side1": "line 5: \"Truncate `anchor` and `anchor2` to 200 and `claim` to 300 as an exact prefix\"",
            "side2": "section 2 item 7: \"claim to 297 characters plus `...` ... Position A takes that exact rule as the claim cut\"",
            "why": "A claim of 297 characters plus a marker is not an exact prefix of the first 300 characters; A's own item 7 says only anchors, anchor2 and quote are cut as exact prefixes.",
        },
        {
            "id": "A-X3",
            "side1": "section 1: \"removes 88 of the 92 measured drops, so ... the expensive, unmeasured step (re-ask) is left with at most 4 lines\" (and section 3.4 \"at most 4 lines\")",
            "side2": "section 3.1: \"88 of 92 ... [derived upper bound, not measured]\" and section 5 M1: \"a lower number means a second violation on the same line\"",
            "why": "An upper bound on lines the cut can fix is a lower bound on the residual (at least 4); \"at most 4\" cannot follow from it, and A's own M1 allows a larger residual.",
        },
    ],
    "B": [
        {
            "id": "B-X1",
            "side1": "section 4.4 totals and 4.6: \"all 5 re-asked blocks recorded valid afterwards\" / \"5 of 5 re-asked blocks recorded valid\"",
            "side2": "section 4.4 table, row E3: \"reviewer 3 fully fixed; reviewer 2 still had two bad citations; '3 of 3 (to be confirmed by `review cluster`)'\"",
            "why": "B's own table shows a re-asked block that was still invalid and one outcome unconfirmed, so \"5 of 5 valid\" is not supported by the table beside it.",
        },
        {
            "id": "B-X2",
            "side1": "section 4.2 'What this gives B': \"and on none of the 42 merges where a blocking row survived\"",
            "side2": "section 4.2 table: \"49 rows in 44 distinct triples and 42 distinct (row, package) merges\" and \"4 rows in 3 merges\" where no blocking row was left",
            "why": "The 42 merges are all merges with a dropped blocking line, 3 of which have no surviving blocking row; the merges where a blocking row survived number 39, not 42.",
        },
        {
            "id": "B-X3",
            "side1": "sections 3.5 and 5 (INV-C, B-raise): \"rewrites four boundary assertions\"",
            "side2": "section 3.1 and section 2 INV-010 row: `card_convert.py` (`MAX_CLAIM = 300`) \"must import the same constants under either policy\"; its pin `tests/review/test_review_card_convert.py:500` asserts `len(f[\"claim\"]) == 300`",
            "why": "If card_convert imports the raised claim constant, a fifth pin (test_review_card_convert.py:500, read at HEAD) fails; B's count of four omits it.",
        },
    ],
}

CONSIDERED_NOT_COUNTED = {
    "A": [
        "section 2 item 8 (compliance metric computed from a repair=False parse) vs item 2 (cluster_cmd passes repair=True): A does not say where first-parse state is carried; an omission, not a stated opposite.",
        "section 2 item 6 ('--resume ... documented nowhere') vs section 3.3 (E2 spike S2 passed --resume): documented vs tested, not opposed.",
    ],
    "B": [
        "section 3.2 (re-ask only for blocking true/unknown drops) vs section 2 C-02 row (any over-limit line makes block_ok False until the re-ask): a reviewer whose only drops say blocking:false never regains a valid block; an unaddressed gap, not a stated opposite.",
        "section 4.5 bullet 4 (SKILL.md:343 forbids any normalisation by the orchestrator) vs last bullet (a code normaliser bears on where a repair may live): B qualifies itself in the same list; not opposed.",
    ],
}


def read(path):
    return path.read_text(encoding="utf-8")


def rc(text):
    low = text.lower()
    rows = []
    matched = 0
    for rid, desc, kws in REQS:
        hits = [any(alt.lower() in low for alt in kw.split("|")) for kw in kws]
        n = sum(hits)
        ok = n >= 3
        matched += ok
        rows.append({"id": rid, "stems_present": n, "stems_total": len(kws), "matched": ok})
    return matched / len(REQS), matched, rows


def units(text):
    out = []
    for line in text.splitlines():
        if not line.strip() or HEADING_RE.match(line):
            continue
        s = line.strip()
        if s.startswith("|"):
            if SEP_RE.match(s):
                continue
            out.append(s)
            continue
        s = BULLET_RE.sub("", line).strip()
        out.extend(p for p in SENT_SPLIT_RE.split(s) if p.strip())
    return out


def is_claim(u):
    return bool(re.search(r"\d", u) or TAG_RE.search(u) or FILE_CITE_RE.search(u))


def ic(text, key):
    us = units(text)
    claims = sum(1 for u in us if is_claim(u))
    contra = len(CONTRADICTIONS[key])
    return 1 - contra / claims, claims, contra, len(us)


def body_lines(text):
    lines = text.splitlines()[6:]
    return [l for l in lines if l.strip() and not HEADING_RE.match(l) and not SEP_RE.match(l.strip())]


def sr(text):
    body = body_lines(text)
    concrete = sum(1 for l in body if re.search(r"\d", l) or FILE_CITE_RE.search(l) or CODE_SPAN_RE.search(l))
    vague_detail = {}
    vague = 0
    for ph in VAGUE:
        pat = re.compile(r"\b" + re.escape(ph) + (r"" if ph.endswith(".") else r"\b"), re.I)
        n = sum(len(pat.findall(l)) for l in body)
        vague_detail[ph] = n
        vague += n
    den = concrete + vague
    return (concrete / den if den else 0.0), concrete, vague, vague_detail, len(body)


def dc(text):
    heads = set()
    for line in text.splitlines():
        m = NUM_HEADING_RE.match(line)
        if m:
            heads.add(m.group(1))
    refs = []
    external = []
    for line in text.splitlines():
        for m in SECTION_REF_RE.finditer(line):
            prefix = line[: m.start()][-40:]
            rec = {"ref": m.group(1), "resolved": m.group(1) in heads}
            if EXTERNAL_PREFIX_RE.search(prefix):
                external.append(m.group(1))
            else:
                refs.append(rec)
    resolved = sum(1 for r in refs if r["resolved"])
    return (resolved / len(refs) if refs else 1.0), resolved, len(refs), sorted(heads), refs, external


def h2(text):
    return sum(1 for l in text.splitlines() if re.match(r"^##\s", l))


def main():
    texts = {k: read(p) for k, p in VARIANTS.items()}
    h2s = {k: h2(t) for k, t in texts.items()}
    max_h2 = max(h2s.values())
    result = {
        "definitions": {
            "requirements": [{"id": r[0], "desc": r[1], "stems": r[2]} for r in REQS],
            "rc_rule": "matched when >= 3 stems present (case-insensitive substring; a|b = either)",
            "ic_rule": "1 - contradictions/claims; claims = sentences and table rows with a digit, file:line cite or evidence tag; contradictions = CONTRADICTIONS table (scorer reading)",
            "sr_rule": "concrete body lines / (concrete body lines + vague phrase occurrences); body = lines after first 6, minus headings, blanks, table separators",
            "dc_rule": "'section N[.N]' refs resolved by a numbered heading; refs right after 'research/...' are external and excluded",
            "sc_rule": "H2 count / max H2 count",
            "weights": {"RC": 0.30, "IC": 0.25, "SR": 0.15, "DC": 0.15, "SC": 0.15},
            "vague_phrases": VAGUE,
        },
        "variants": {},
    }
    for key in ("A", "B"):
        t = texts[key]
        rc_v, rc_n, rc_rows = rc(t)
        ic_v, claims, contra, n_units = ic(t, key)
        sr_v, conc, vag, vag_detail, n_body = sr(t)
        dc_v, dc_res, dc_tot, heads, refs, ext = dc(t)
        sc_v = h2s[key] / max_h2
        q = rc_v * 0.30 + ic_v * 0.25 + sr_v * 0.15 + dc_v * 0.15 + sc_v * 0.15
        result["variants"][key] = {
            "file": VARIANTS[key].name,
            "RC": round(rc_v, 4), "RC_matched": rc_n, "RC_total": len(REQS),
            "RC_rows": rc_rows,
            "IC": round(ic_v, 4), "IC_claims": claims, "IC_units": n_units, "IC_contradictions": contra,
            "IC_contradiction_list": CONTRADICTIONS[key],
            "IC_considered_not_counted": CONSIDERED_NOT_COUNTED[key],
            "SR": round(sr_v, 4), "SR_concrete_lines": conc, "SR_vague_occurrences": vag,
            "SR_vague_detail": vag_detail, "SR_body_lines": n_body,
            "DC": round(dc_v, 4), "DC_resolved": dc_res, "DC_total": dc_tot,
            "DC_numbered_headings": heads, "DC_refs": refs, "DC_external_excluded": ext,
            "SC": round(sc_v, 4), "SC_h2": h2s[key], "SC_max_h2": max_h2,
            "quant_score": round(q, 4),
        }
    out = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    (HERE / "quant-score-output.json").write_text(out, encoding="utf-8")
    print(out, end="")


if __name__ == "__main__":
    main()
