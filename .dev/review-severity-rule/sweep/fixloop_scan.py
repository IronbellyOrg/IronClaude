"""Fix-loop scope scan: lines that send non-blocking findings to a fix pass or restart a loop on any new issue.

Usage (repo root): uv run python -I .dev/review-severity-rule/sweep/fixloop_scan.py [--tsv]
Same patterns as tests/skills/test_review_severity_rule.py (FIX_LOOP_PATTERNS); a line that contains
"blocking" is in scope already and is not reported.
"""
import re
import subprocess
import sys

TREES = ["src", "plugins", "commands", "agents", "skills"]
PATTERNS = {
    "F1": r"\bif (any )?(findings|issues) (exist|are found|found)\b",
    "F2": r"\bfinds new issues\b",
    "F3": r"\bissues remain unfixed\b",
    "F4": r"\b(apply|applies|applying|applied) (all|ALL) (the )?(consolidated |collected |fidelity )?(fixes|findings|corrections)\b",
    "F5": r"(fix(-| )agent|fix_authorization: true)[^\n]*\bconsolidated\b|\bconsolidated\b[^\n]*(fix(-| )agent|fix_authorization: true)",
    "F6": r"\bif (any )?(unresolved )?(issues|findings) remain",
}

files = subprocess.run(["git", "ls-files", "-z", "--", *TREES], capture_output=True, text=True, check=True).stdout.split("\0")
rows = []
for f in filter(None, files):
    try:
        lines = open(f, encoding="utf-8").read().splitlines()
    except (UnicodeDecodeError, IsADirectoryError):
        continue
    for n, text in enumerate(lines, 1):
        if "blocking" in text.lower():
            continue
        ids = [k for k, p in PATTERNS.items() if re.search(p, text, re.IGNORECASE)]
        if ids:
            rows.append((",".join(ids), f, n, text.strip()))
for ids, f, n, text in rows:
    print(f"{ids}\t{f}:{n}\t{text[:200]}" if "--tsv" in sys.argv else f"{ids} {f}:{n}")
print(f"# {len(rows)} lines", file=sys.stderr)
