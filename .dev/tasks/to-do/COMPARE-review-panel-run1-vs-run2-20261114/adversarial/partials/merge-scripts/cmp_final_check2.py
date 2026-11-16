import difflib
from pathlib import Path

B = Path("/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do")
O = B / "COMPARE-review-panel-run1-vs-run2-20261114"
A = O / "adversarial"
M = (O / "MERGED-review-panel-unification.md").read_text().splitlines()

# base check with difflib
base = (A / "partials/merge-stage/base-corrected.md").read_text().splitlines()
sm = difflib.SequenceMatcher(None, base, M, autojunk=False)
matched = sum(b.size for b in sm.get_matching_blocks())
print("base lines", len(base), "matched in order", matched)
unmatched = []
last = 0
for b in sm.get_matching_blocks():
    for i in range(last, b.a):
        if base[i].strip():
            unmatched.append((i + 1, base[i][:150]))
    last = b.a + b.size
print("unmatched non-blank base lines:", len(unmatched))
for x in unmatched[:60]:
    print("  ", x)

def region(txt_lines):
    first = next((l for l in txt_lines if l.strip()), None)
    cands = [i for i, l in enumerate(M) if l == first]
    return cands

for name, d in (("M09-sec6.md", "v1-blocks"), ("M14-sec8-inventory.md", "v1-blocks"), ("M20-sec8-risk.md", "v1-blocks"), ("M00-merge-notes.md", "new-blocks"), ("M08-disposition-table.md", "new-blocks"), ("M22b-compare-artifacts-10B.md", "new-blocks"), ("M29-appendices-D-E.md", "new-blocks")):
    blk = (A / "partials/merge-stage" / d / name).read_text().splitlines()
    c = region(blk)
    print("==", name, "candidates", c[:3], "lines", len(blk))
    if not c:
        continue
    s = c[0]
    seg = M[s:s + len(blk) + 80]
    sm2 = difflib.SequenceMatcher(None, blk, seg, autojunk=False)
    n = 0
    for op, a1, a2, b1, b2 in sm2.get_opcodes():
        if op == "equal":
            continue
        n += 1
        if n <= 8:
            print("  ", op, "block", a1 + 1, a2, "->", "merged", s + b1 + 1, s + b2)
            for l in blk[a1:a2][:2]:
                print("     -", l[:170])
            for l in seg[b1:b2][:2]:
                print("     +", l[:170])
    print("   total diff ops:", n)
