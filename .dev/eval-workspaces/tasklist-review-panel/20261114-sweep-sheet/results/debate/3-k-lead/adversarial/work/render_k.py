"""Render the K paragraph and report lengths of the Z0, K and SS briefs (read-only; no ground truth is opened)."""
import sys
sw = sys.argv[1]
sys.path.insert(0, sw)
from scaffold import briefs  # noqa: E402

doc = {"cand_sb": "/sandbox/plan.md", "sha": "0" * 64}
src = "/sandbox/source.md"
sheet = {"path": "/sandbox/sheets/r1.md", "text": "Items assigned to you: S1\n\n### S1   (class C4)\nWhere: Task 4\nText:  \"x\"\nTool output:\n  - none\nQuestion: q\nReply with one line in the ledger-v1 block: item S1, verdict OK, PROBLEM or UNSURE."}
k = briefs.k_paragraph()
print("K PARAGRAPH (%d chars, %d words):" % (len(k), len(k.split())))
print(k)
print()
lead = " ".join(l.strip() for l in open(sw + "/briefs/k-lead.txt").read().splitlines() if l.strip() and not l.startswith("# "))
print("LEAD-IN (%d chars, %d words): %s" % (len(lead), len(lead.split()), lead))
for arm in ("Z0", "K", "SS"):
    r = briefs.render(arm, doc, sheet if arm == "SS" else None, src)
    print(arm, "chars", len(r["text"]), "words", len(r["text"].split()), "parts", r["parts"])
z0 = briefs.render("Z0", doc, None, src)["text"]
print("K minus Z0 chars:", len(briefs.render("K", doc, None, src)["text"]) - len(z0))
print("ledger-rule chars:", len(open(sw + "/briefs/ledger-rule.txt").read()), " sheet-block chars:", len(open(sw + "/briefs/sheet-block.txt").read()))
print("\nFULL K BRIEF TAIL (last 1500 chars):\n", briefs.render("K", doc, None, src)["text"][-1500:])
