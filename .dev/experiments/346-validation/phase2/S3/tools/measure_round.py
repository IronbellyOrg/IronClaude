"""Measure one review round: M2 (blocking, minor, verdict) and M4 (plan bytes, lines).

Usage: uv run python -I measure_round.py <plan-file> <review-file>
Prints one JSON object. The review counts are read from the review's own header lines
("## Verdict: FAIL", "- Blocking findings: N", "- Minor findings: N"), the format all three
original reviews used. If a header line is missing the field is null: count by hand and say so.
"""
import json
import re
import sys
from pathlib import Path

plan, review = Path(sys.argv[1]), Path(sys.argv[2])
b = plan.read_bytes()
t = review.read_text(encoding="utf-8")
head = "\n".join(t.split("\n")[:30])  # headers sit in the first lines of every original review


def first(pat, text=head):
    m = re.search(pat, text, re.M | re.I)
    return m.group(1) if m else None


v = first(r"^#+\s*Verdict:\s*(PASS|FAIL)")
bl = first(r"^[-*]\s*Blocking findings:\s*(\d+)")
mi = first(r"^[-*]\s*Minor findings:\s*(\d+)")
print(json.dumps({
    "plan": plan.name, "plan_bytes": len(b),
    "plan_lines": b.count(b"\n") + (0 if b.endswith(b"\n") else 1),
    "review": review.name, "verdict": v,
    "blocking": int(bl) if bl else None, "minor": int(mi) if mi else None,
}))
