"""Apply re-evaluated verdicts to the two passes; print final per-dimension subtotals and CEV tables.
Usage: uv run python scoring/final_qual.py [--tables]"""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reconcile import p1, p2  # noqa: E402  (reconcile prints its own report on import)

REEVAL = {  # (variant, criterion): (verdict, reason) - orchestrator re-evaluation citing both passes
    ("V1", "CR3"): ("NOT MET", "'B' is both the baseline time (V1:171) and issue prefix B1-B8 (V1:17); 'T1' is both Theory 1 and a time (V1:323)"),
    ("V1", "CR4"): ("MET", "the 'follow-up work in section 4' line (V1:111) is a dangling reference, not a contradiction between claims"),
    ("V2", "CP5"): ("MET", "explicit exclusions: D3-D5 deferred (V2:496), no Opus or sonnet reviewer in the experiment"),
    ("V2", "CR4"): ("NOT MET", "V2:182 '135 s or later gets none' contradicts its own formula, which gives 0 from 128 s (diff-analysis grid)"),
    ("V3", "CP5"): ("MET", "explicit exclusions: R3-R5 deferred (V3:154), glm/Qwen excluded, harness fixes separate (V3:126)"),
    ("V3", "CR4"): ("NOT MET", "R1 'complete replacement findings-v1 block' (V3:73) vs req 6 'outside the fenced block' (V3:176); diff-analysis X-006"),
    ("V3", "CR5"): ("NOT MET", "V3:67 haiku 'breaks the cap' contradicts the per-baseline cap (SEED:30); gains do not follow from stated inputs (diff-analysis grid ERRORs)"),
    ("V4", "CP5"): ("MET", "explicit exclusions: grok in no design (V4:610), transports rejected for every design, Redesigns 1/4/5 deferred from the experiment"),
    ("V5", "CR4"): ("NOT MET", "V5:3 'Nothing was run for this variant' vs V5:106 'Verified in this build. claude --help lists ...'"),
    ("V5", "RK1"): ("NOT MET", "probabilities exist for moves (V5:190) but no 3 risks carry probability and impact; failure modes are rated qualitatively"),
}
final = {}
for k in p1:
    final[k] = REEVAL[k][0] if k in REEVAL else p1[k][0]
    assert k in REEVAL or p1[k][0] == p2[k][0], k
DIMS = ["CP", "CR", "ST", "CL", "RK", "IV"]
print("\n| Dimension | V1 | V2 | V3 | V4 | V5 |\n|---|---|---|---|---|---|")
tot = Counter()
for d in DIMS:
    cells = []
    for v in [f"V{i}" for i in range(1, 6)]:
        n = sum(final[(v, f"{d}{j}")] == "MET" for j in range(1, 6))
        tot[v] += n
        cells.append(f"{n}/5")
    print(f"| {d} | " + " | ".join(cells) + " |")
print("| total | " + " | ".join(f"{tot[v]}/30 = {tot[v]/30:.3f}" for v in sorted(tot)) + " |")
if "--tables" in sys.argv:
    for d in DIMS:
        print(f"\n### {d}\n\n| Criterion | " + " | ".join(f"V{i}" for i in range(1, 6)) + " |\n|---|---|---|---|---|---|")
        for j in range(1, 6):
            c = f"{d}{j}"
            cells = []
            for i in range(1, 6):
                k = (f"V{i}", c)
                ev = REEVAL[k][1] if k in REEVAL else p1[k][1]
                cells.append(f"{final[k]}: {ev[:160].replace('|', '/')}")
            print(f"| {c} | " + " | ".join(cells) + " |")
