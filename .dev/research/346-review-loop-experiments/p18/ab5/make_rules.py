#!/usr/bin/env python3
"""Build frozen/rules.md for ab5 from the two frozen sources (run once; the result is hash-pinned in decision.json).
rules-ab1.md  = the ab1 product rules file (three first reviews, MERGE, VERIFY)   [same file ab4 used, same sha]
rules-pn2.md  = the PN2 rules file (Stage 2 arm 3 + the two 'Lint evidence' bullets)
ab5 rules     = rules-ab1 + the two PN2 lint bullets copied verbatim at the PN2 positions (exactly as ab4's make_rules.py)
                + panel wording: three -> four first reviews (ab4 used two). Nothing else changes."""
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
SUBS = [("FIRST-REVIEW prompt, three times, then the MERGE rule", "FIRST-REVIEW prompt, four times, then the MERGE rule"),
        ("or after three first reviews for each merged finding", "or after four first reviews for each merged finding"),
        ("- **Three first reviews**: brief three reviewers", "- **Four first reviews**: brief four reviewers"),
        ("list every blocking finding of the three reports", "list every blocking finding of the four reports"),
        ("list the three reports' follow-up candidates by reference", "list the four reports' follow-up candidates by reference")]
for a, b in SUBS:
    assert t.count(a) == 1, a
    t = t.replace(a, b)
if __name__ == "__main__":
    (H / "rules.md").write_text(t)
    print(hashlib.sha256(t.encode()).hexdigest())
    print("remaining 'three':", [m.group(0) for m in re.finditer(r"(?i)[^.\n]*\bthree\b[^.\n]*", t)])


def full_rules():
    """ab5 variant `full`: the PN1 product rules file (rules-pn1.md, the file PN1's reviewers read, byte copy of
    p13/ab1/runs/b1-r1/home/.claude/rules/prompts/document_review_loop_prompts.md) + the two PN2 lint bullets at the same two anchor
    lines as above. PN1's text already describes the panel and the ledger merge, so nothing else changes."""
    t = []
    for ln in (H / "rules-pn1.md").read_text().split("\n"):
        t.append(ln)
        if ln == "Write `review: 1 of 3` once, as the first line of the report.":
            t.append(lint[0])
        if ln.startswith("Follow the re-review core below in order"):
            t.append(lint[1])
    out_ = "\n".join(t)
    assert out_.count("- **Lint evidence**") == 2
    return out_


if __name__ == "__main__":
    ft = full_rules()
    (H / "rules-full.md").write_text(ft)
    print("rules-full.md", hashlib.sha256(ft.encode()).hexdigest())
