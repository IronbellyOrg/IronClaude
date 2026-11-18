#!/usr/bin/env python3
"""Quantitative layer (A.1 of refs/scoring-protocol.md) for slot X-14, scorer pass 1.

Run with:  uv run python quant-score.py
Stdlib only. No LLM judgment inside the numbers. Same input -> byte-identical output
(no timestamps, sorted JSON keys, fixed regex lists, no randomness).

Inputs : variant-1-original.md (Variant A), variant-2-original.md (Variant B), same folder.
Outputs: quant-score-output.json (same folder) and a table on stdout.

RULES (documented here and in score-pass1.md)
---------------------------------------------
(1) RC = matched requirements / 12. The 12 source requirements R1..R12 below are extracted by
    the scorer from the X-14 row of undecidable-conflicts.md and the proposal structure it asks
    for. The 14 items named in the scorer brief are merged to 12 as follows: "verify-run
    placement/ownership" + "design consequence for the shared core and named modules" = R3;
    "test or measurement" + "evidence with verification tags" = R10. A requirement is matched
    when ALL regexes of its list match somewhere in the variant (case-insensitive, whole file).
    Mere mention counts (the protocol's grep-match rule); the qualitative layer judges quality.
(2) IC = 1 - contradictions / total scorable claims. contradictions = INTRA-variant
    contradictions found by the scorer by reading (CONTRADICTIONS below; quotes in
    score-pass1.md). Debate-found false claims are NOT counted here (they go to Correctness).
    total scorable claims = sentences (headings, blank lines, table separators and metadata lines
    excluded; sentences of fewer than 4 words excluded) that contain a digit, a file path, a line
    reference, or a tag [CODE-VERIFIED]/[UNVERIFIED]/[CODE-CONTRADICTED]/[POST-BASELINE].
(3) SR = concrete / (concrete + vague) over the same sentence set. A sentence is concrete if it
    matches any CONCRETE regex, vague if it matches any VAGUE regex (a sentence can be both).
    CONCRETE = digit, backticked code span, INV-<letter>, file path, line ref, tag.
    VAGUE = appropriate, as needed, properly, adequate, should consider, might, various, etc.,
    best practice(s), industry standard.
(4) DC = resolved internal references / total internal references. Reference kinds:
      Section N  (resolves if an H2 numbered N exists)
      E-n / En   (normalised to n; resolves if an item line "E-n." / "En." / "**E-n." exists;
                  `En:` is a git citation form and is excluded; note: the study names E1/E2 also
                  match and resolve against evidence items of the same number, in both variants)
      M-n / Mn   (same, item lines "M-n." / "Mn.")
      P-n        (same, item lines "**P-n.")
      INV-X      (single letter; resolves if the id occurs inside the variant's Invariants H2;
                  numeric ids such as INV-003 belong to other documents and are excluded)
    The defining token at the start of an item line is not counted as a reference.
(5) SC = H2 count / max H2 count over the two variants.
"""
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
VARIANTS = {"A": HERE / "variant-1-original.md", "B": HERE / "variant-2-original.md"}
OUT = HERE / "quant-score-output.json"

# --- RC: 12 requirements, each a list of regexes that must ALL match ------------------------
REQS = [
    ("R1 acceptance model / tiers", [r"\btier[s]?\b|structural (exit )?gates?|exit gates?"]),
    ("R2 metric of record", [r"metric of record|any-severity", r"wrong[- ]blockers?"]),
    ("R3 verify-run placement/ownership + design consequence for shared core and named modules",
     [r"verify-run|verify_run", r"shared core|src/superclaude/cli/review", r"named modules?"]),
    ("R4 judge and ground-truth registry owner",
     [r"judge (wrapper|completion)|judge-completion", r"ground[- ]truth registry|CODEOWNERS|ground truth"]),
    ("R5 harness placement (.dev/ vs scripts/)", [r"\.dev/", r"scripts/"]),
    ("R6 INV-F", [r"INV-F"]),
    ("R7 INV-H", [r"INV-H"]),
    ("R8 INV-K", [r"INV-K"]),
    ("R9 PR review and rf-qa effect", [r"PR (code )?review|PR adapter", r"rf-qa"]),
    ("R10 test/measurement that shows right or wrong + verification-tagged evidence",
     [r"\b(right|wrong) if\b", r"\[CODE-VERIFIED\]", r"\[UNVERIFIED\]"]),
    ("R11 consistency with adjudicated slots C-01..C-03", [r"\bC-01\b", r"\bC-02\b", r"\bC-03\b"]),
    ("R12 strongest objection and answer", [r"strongest objection", r"\banswer\b"]),
]

# --- IC: intra-variant contradictions found by reading (details in score-pass1.md) -----------
CONTRADICTIONS = {
    "A": ["A-IC-1 sections 2/3 vs 5: 'Nothing below disagrees with a recorded outcome' while the "
          "design adds ledger-entry keys and section 5 says C-01 'says ledger passthrough keys "
          "were deferred'"],
    "B": ["B-IC-1 section 1 vs gate text: 'wrong-blocker counts are reported as descriptive "
          "columns, not gates' while the gate carries 'the control package's wrong-blocker ceiling'",
          "B-IC-2 E6 vs section 7 answer 2: E6 says the blocking-row metric has 'the same three "
          "easy catches inside it'; answer 2 says 'Presence.txt does not say which of the three "
          "easy items are blocking in implement, so I make no claim'"],
}

TAG = r"\[(?:CODE-VERIFIED|UNVERIFIED|CODE-CONTRADICTED|POST-BASELINE)\]"
PATH = r"[\w./-]+\.(?:py|md|sh|json|yml|yaml|toml|txt|tsv)\b"
CLAIM_RE = re.compile(r"\d|" + TAG + "|" + PATH + r"|:\d+|\bline \d+")
CONCRETE_RE = re.compile(r"\d|`[^`]+`|INV-[A-Z]\b|" + TAG + "|" + PATH)
VAGUE_RE = re.compile(
    r"\b(appropriate|as needed|properly|adequate|should consider|might|various|best practices?|"
    r"industry standard)\b|\betc\b\.?", re.I)
META_RE = re.compile(r"^(Status:|Slot:|Position:|Code state|Citation forms|Tags?:|Slot note|Mode:)", re.I)
SENT_SPLIT = re.compile(r"(?<=[.;!?])\s+(?=[A-Z\[`(*\d])")


def sentences(text):
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or META_RE.match(s) or re.fullmatch(r"[|\-: ]+", s):
            continue
        s = re.sub(r"^[-*]\s+|^\d+\.\s+", "", s).replace("|", " ")
        for part in SENT_SPLIT.split(s):
            if len(part.split()) >= 4:
                out.append(part)
    return out


def h2_sections(text):
    return [(m.group(1), m.group(0)) for m in re.finditer(r"^## (\d+)\.\s.*$", text, re.M)]


def invariants_block(text):
    m = re.search(r"^## \d+\.\s+Invariants.*?(?=^## |\Z)", text, re.M | re.S)
    return m.group(0) if m else ""


def dc(text):
    sec_nums = {n for n, _ in h2_sections(text)}
    inv_block = invariants_block(text)
    item_re = re.compile(r"^\**([EMP])-?(\d+)\.", re.M)
    defined = {(k, n) for k, n in item_re.findall(text)}
    total = resolved = 0
    unresolved = []

    def hit(ok, label):
        nonlocal total, resolved
        total += 1
        if ok:
            resolved += 1
        else:
            unresolved.append(label)

    for m in re.finditer(r"\b[Ss]ection (\d+)\b", text):
        hit(m.group(1) in sec_nums, "Section " + m.group(1))
    def_pos = {m.start(1) for m in item_re.finditer(text)}
    for m in re.finditer(r"(?<![\w/])([EMP])-?(\d+)\b(?!:)", text):
        if m.start() in def_pos:
            continue  # the defining token itself is not a reference
        hit((m.group(1), m.group(2)) in defined, f"{m.group(1)}-{m.group(2)}")
    for m in re.finditer(r"\bINV-([A-Z])\b", text):
        if m.start() >= text.find(inv_block) and m.end() <= text.find(inv_block) + len(inv_block) \
                and inv_block:
            continue  # occurrences inside the definition block are the definitions
        hit(f"INV-{m.group(1)}" in inv_block, f"INV-{m.group(1)}")
    return resolved, total, unresolved


def score(label, text, max_h2):
    low = text
    matched = []
    for name, pats in REQS:
        if all(re.search(p, low, re.I) for p in pats):
            matched.append(name)
    rc = len(matched) / len(REQS)

    sents = sentences(text)
    claims = [s for s in sents if CLAIM_RE.search(s)]
    n_contra = len(CONTRADICTIONS[label])
    ic = 1 - n_contra / len(claims)

    concrete = sum(1 for s in claims if CONCRETE_RE.search(s))
    vague = sum(1 for s in sents if VAGUE_RE.search(s))
    sr = concrete / (concrete + vague)

    r, t, unres = dc(text)
    dcv = r / t if t else 1.0
    h2 = len(h2_sections(text))
    sc = h2 / max_h2
    quant = 0.30 * rc + 0.25 * ic + 0.15 * sr + 0.15 * dcv + 0.15 * sc
    return {
        "RC": round(rc, 4), "IC": round(ic, 4), "SR": round(sr, 4), "DC": round(dcv, 4),
        "SC": round(sc, 4), "quant_score": round(quant, 4),
        "detail": {
            "requirements_matched": matched,
            "requirements_missed": [n for n, _ in REQS if n not in matched],
            "sentences_total": len(sents), "scorable_claims": len(claims),
            "contradictions": n_contra, "concrete": concrete, "vague": vague,
            "refs_resolved": r, "refs_total": t, "refs_unresolved": sorted(set(unres)),
            "h2_count": h2,
        },
    }


def main():
    texts = {k: p.read_text(encoding="utf-8") for k, p in VARIANTS.items()}
    max_h2 = max(len(h2_sections(t)) for t in texts.values())
    res = {k: score(k, t, max_h2) for k, t in texts.items()}
    res["input_sha256"] = {k: hashlib.sha256(t.encode()).hexdigest() for k, t in texts.items()}
    OUT.write_text(json.dumps(res, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{'metric':<14}{'weight':>7}{'Variant A':>12}{'Variant B':>12}")
    for m, w in (("RC", .30), ("IC", .25), ("SR", .15), ("DC", .15), ("SC", .15)):
        print(f"{m:<14}{w:>7.2f}{res['A'][m]:>12.4f}{res['B'][m]:>12.4f}")
    print(f"{'quant_score':<14}{'':>7}{res['A']['quant_score']:>12.4f}{res['B']['quant_score']:>12.4f}")


if __name__ == "__main__":
    main()
