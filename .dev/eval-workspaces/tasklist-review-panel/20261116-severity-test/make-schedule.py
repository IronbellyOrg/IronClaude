"""Block-randomised schedule of the severity-rule test: per replicate (block), every document x {Z0, S}, order shuffled.

    uv run --no-project python -I make-schedule.py --docs HO-2,HO-3,HX-1,HX-3 --reps 5 --seed 20261121 --out schedule.tsv

Columns (tab separated, first line a comment with the seed): block, arm, doc, run. `arm` is Z0 (harness-z0, current brief)
or S (harness-s, brief with the narrowed contradiction clause). Run names start with `sev1-`, which is the stage prefix of
the judge batch. Same arguments give the same file.
"""
import argparse
import random

ap = argparse.ArgumentParser()
ap.add_argument("--docs", required=True)
ap.add_argument("--reps", type=int, required=True)
ap.add_argument("--seed", type=int, required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()
docs = [d for d in a.docs.split(",") if d]
rows = []
for b in range(1, a.reps + 1):
    block = [(arm, d) for d in docs for arm in ("Z0", "S")]
    random.Random(f"{a.seed}-{b}").shuffle(block)
    rows += [(b, arm, d, f"sev1-{arm.lower()}-{d}-r{b}") for arm, d in block]
with open(a.out, "w") as f:
    f.write(f"# severity-test schedule seed={a.seed}\n")
    f.write("block\tarm\tdoc\trun\n")
    for r in rows:
        f.write("\t".join(map(str, r)) + "\n")
print(len(rows), "rows")
