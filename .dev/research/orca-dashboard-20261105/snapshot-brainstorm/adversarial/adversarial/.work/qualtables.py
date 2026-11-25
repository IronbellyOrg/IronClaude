"""Render the base-selection qualitative tables from the scoring passes.

Usage: uv run python qualtables.py
Final verdict = pass 1 where both passes agree; the re-evaluation verdict
(qual-reeval.md) where they disagree. Evidence comes from the pass 1 row,
or from the re-evaluation row when that verdict is final. Replaces the
`<!-- TODO: qualitative-tables -->` placeholder in ../base-selection.md
and prints per-dimension totals.
"""
import re
from pathlib import Path

WORK = Path(__file__).resolve().parent
DIMS = [("CO", "Completeness"), ("CR", "Correctness"), ("ST", "Structure"),
        ("CL", "Clarity"), ("RK", "Risk Coverage"), ("IE", "Invariant & Edge Case Coverage")]
VS = ("V1", "V2", "V3")


def cells(ln):
    return [c.strip() for c in ln.strip().strip("|").split("|")]


def parse_pass(name):
    out, cur = {}, None
    for ln in (WORK / name).read_text().splitlines():
        h = re.match(r"^##\s+Variant\s+V?(\d)", ln)
        if h:
            cur = "V" + h.group(1)
            continue
        if cur and re.match(r"^\|\s*(CO|CR|ST|CL|RK|IE)\d\s*\|", ln):
            c = cells(ln)
            out[(cur, c[0])] = (c[-1].strip("*"), c[2].replace("|", "/"))
    return out


p1, p2 = parse_pass("qual-pass1.md"), parse_pass("qual-pass2.md")
reeval = {}
for ln in (WORK / "qual-reeval.md").read_text().splitlines():
    if re.match(r"^\|\s*V\d\s*\|", ln):
        c = cells(ln)
        reeval[(c[0], c[1])] = (c[-1], c[5])

final, bias = {}, []
for k, (v1, ev) in p1.items():
    if v1 == p2[k][0]:
        final[k] = (v1, ev)
    else:
        assert k in reeval, f"disagreement {k} not re-evaluated"
        final[k] = reeval[k]
        bias.append((k, v1, p2[k][0], reeval[k][0]))
assert len(final) == 90, len(final)

md = []
for code, name in DIMS:
    md += [f"### {name} (5 criteria)", "",
           "| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |",
           "|---|---|---|---|---|---|---|"]
    for i in range(1, 6):
        row = [f"{code}{i}"]
        for v in VS:
            verdict, ev = final[(v, f"{code}{i}")]
            row += [verdict, ev]
        md.append("| " + " | ".join(row) + " |")
    subs = [sum(final[(v, f"{code}{i}")][0] == "MET" for i in range(1, 6)) for v in VS]
    md += ["| **Subtotal** | **%d/5** | | **%d/5** | | **%d/5** | |" % tuple(subs), ""]
    print(name, dict(zip(VS, subs)))
md.append("Full Claim/Evidence/Verdict rows: `.work/qual-pass1.md` (order V1, V2, V3), "
          "`.work/qual-pass2.md` (order V3, V2, V1), `.work/qual-reeval.md` (disagreements).")

target = WORK.parent / "base-selection.md"
text = target.read_text()
assert "<!-- TODO: qualitative-tables -->" in text
target.write_text(text.replace("<!-- TODO: qualitative-tables -->", "\n".join(md)))
for v in VS:
    print(v, "total", sum(final[(v, f"{c}{i}")][0] == "MET" for c, _ in DIMS for i in range(1, 6)))
print("bias:", bias)
