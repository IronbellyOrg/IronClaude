"""R3 evidence-validator: independently re-verify Reviewer-1's escalated
false-negative claims, then test the proposed one-line fix."""
import re

CURRENT = (
    r"(?:^|\n)\s*(?:#{1,6}\s+|[-*+]\s+|\d+\.\s+)?[_*]*(?i:verdict)[_*]*\s*:"
    r"[^a-zA-Z0-9\n:]*(PASS|FAIL)(?![A-Za-z])"
    r"(?!\s*(?:/|(?i:or))\s*(?:PASS|FAIL))"
)
# Proposed fix: lookahead -> same-line ([ \t] not \s) + value word-boundary
FIXED = (
    r"(?:^|\n)\s*(?:#{1,6}\s+|[-*+]\s+|\d+\.\s+)?[_*]*(?i:verdict)[_*]*\s*:"
    r"[^a-zA-Z0-9\n:]*(PASS|FAIL)(?![A-Za-z])"
    r"(?![ \t]*(?:/|(?i:or))[ \t]*(?:PASS|FAIL)(?![A-Za-z]))"
)


def acc(rx, s):
    return re.search(rx, s) is not None


print("REAL VERDICTS THAT SHOULD BE ACCEPTED (Reviewer-1's escalated false-negatives):")
real = [
    "Verdict: PASS or FAILURE expected",
    "Verdict: PASS or PASSED later",
    "Verdict: PASS or FAILS fast",
    "Verdict: PASS or FAIL-safe mode",
    "Verdict: PASS or FAILover cluster",
    "Verdict: PASS\nor FAIL would have aborted",
    "Verdict: PASS or revisit later",        # control: already accepted
    "Verdict: PASS — CONTINUE",               # control
]
for s in real:
    print(f"  cur={acc(CURRENT,s)!s:5} fix={acc(FIXED,s)!s:5}  {s!r}")

print("\nTEMPLATE PLACEHOLDERS THAT MUST STAY REJECTED:")
tmpl = [
    "Verdict: PASS/FAIL", "Verdict: FAIL/PASS", "Verdict: PASS / FAIL",
    "Verdict: PASS or FAIL", "Verdict: PASS OR FAIL", "1. Verdict: PASS/FAIL",
    "**Verdict:** PASS or FAIL",
]
for s in tmpl:
    print(f"  cur={acc(CURRENT,s)!s:5} fix={acc(FIXED,s)!s:5}  {s!r}  (both should be False)")

print("\nCORE ACCEPT controls (must stay True under FIX):")
for s in ["1. Verdict: PASS", "Verdict: _PASS_", "1. __Verdict__: ✅ __PASS__"]:
    print(f"  fix={acc(FIXED,s)!s:5}  {s!r}")
print("CORE REJECT controls (must stay False under FIX):")
for s in ["Verdict PASS", "Verdict: PASSING", "Verdict: FAILURE", "verdict pass"]:
    print(f"  fix={acc(FIXED,s)!s:5}  {s!r}")
