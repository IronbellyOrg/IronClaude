#!/usr/bin/env python3
"""Build frozen/rules.md for ab4 from the two frozen sources (run once; the result is hash-pinned in decision.json).
rules-ab1.md  = the ab1 product rules file (three first reviews, MERGE, VERIFY)
rules-pn2.md  = the PN2 rules file (Stage 2 arm 3 + the two 'Lint evidence' bullets)
ab4 rules     = rules-ab1 + the two PN2 lint bullets copied verbatim at the PN2 positions + k=2 wording (three -> two first reviews)."""
import hashlib, pathlib, re
H = pathlib.Path(__file__).resolve().parent / "frozen"
ab1 = (H / "rules-ab1.md").read_text()
pn2 = (H / "rules-pn2.md").read_text()
lint = [ln for ln in pn2.splitlines() if ln.startswith("- **Lint evidence**")]
assert len(lint) == 2, lint
out = []
for ln in ab1.split("\n"):
    out.append(ln)
    if ln == "Write `review: 1 of 3` once, as the first line of the report.":
        out.append(lint[0])
    if ln.startswith("Follow the re-review core below in order"):
        out.append(lint[1])
t = "\n".join(out)
subs = [("FIRST-REVIEW prompt, three times, then the MERGE rule", "FIRST-REVIEW prompt, twice, then the MERGE rule"),
        ("or after three first reviews for each merged finding", "or after two first reviews for each merged finding"),
        ("- **Three first reviews**: brief three reviewers", "- **Two first reviews**: brief two reviewers"),
        ("list every blocking finding of the three reports", "list every blocking finding of the two reports"),
        ("list the three reports' follow-up candidates by reference", "list the two reports' follow-up candidates by reference")]
for a, b in subs:
    assert t.count(a) == 1, a
    t = t.replace(a, b)
(H / "rules.md").write_text(t)
print(hashlib.sha256(t.encode()).hexdigest())
left = [m.group(0) for m in re.finditer(r"(?i)[^.\n]*\bthree\b[^.\n]*", t)]
print("remaining 'three':", left)
