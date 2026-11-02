"""Independent check of cap-edits.yaml + sweep-edits.yaml against the live tree (run before any edit).

Usage (repo root): uv run python -I .dev/review-severity-rule/sweep/verify_tables.py
Checks: each old occurs exactly `occurrences` times; no two old occurrences overlap; new never contains old;
fixloop rows add "blocking"; applying both tables to an in-memory copy leaves the swept wordings only on allowed lines.
"""
import pathlib
import re
import subprocess
import sys

import yaml

R = pathlib.Path(".dev/review-severity-rule")
cap = yaml.safe_load((R / "cap-edits.yaml").read_text())["rows"]
swp = yaml.safe_load((R / "sweep-edits.yaml").read_text())["rows"]
errors = []
spans: dict[str, list] = {}
texts: dict[str, str] = {}
for r in cap + swp:
    f = r["file"]
    t = texts.setdefault(f, pathlib.Path(f).read_text())
    starts = [m.start() for m in re.finditer(re.escape(r["old"]), t)]
    if len(starts) != r.get("occurrences", 1):
        errors.append(f"{r['id']}: old occurs {len(starts)}x, expected {r.get('occurrences', 1)}")
    if r["old"] in r["new"]:
        errors.append(f"{r['id']}: new contains old")
    if r.get("group") == "fixloop" and "blocking" not in r["new"].lower():
        errors.append(f"{r['id']}: fixloop new lacks 'blocking'")
    for s in starts:
        spans.setdefault(f, []).append((s, s + len(r["old"]), r["id"]))
for f, ss in spans.items():
    ss.sort()
    for a, b in zip(ss, ss[1:]):
        if b[0] < a[1]:
            errors.append(f"overlap in {f}: {a[2]} and {b[2]}")
new_texts = dict(texts)
for r in cap + swp:
    if r["file"].startswith("tests/"):
        continue
    new_texts[r["file"]] = new_texts[r["file"]].replace(r["old"], r["new"])
sys.path.insert(0, str(R / "sweep"))
PAT = {k: re.compile(v, re.I) for k, v in {
    "F1": r"\bif (any )?(findings|issues) (exist|are found|found)\b", "F2": r"\bfinds new issues\b",
    "F3": r"\bissues remain unfixed\b",
    "F4": r"\b(apply|applies|applying|applied) (all|ALL) (the )?(consolidated |collected |fidelity )?(fixes|findings|corrections)\b",
    "F5": r"(fix(-| )agent|fix_authorization: true)[^\n]*\bconsolidated\b|\bconsolidated\b[^\n]*(fix(-| )agent|fix_authorization: true)",
    "F6": r"\bif (any )?(unresolved )?(issues|findings) remain",
    "BAN": r"FAIL: Issues found|strictly fewer issues|logged for human review|zero-tolerance policy for errors",
}.items()}
files = subprocess.run(["git", "ls-files", "-z", "--", "src", "plugins", "commands", "agents", "skills"],
                       capture_output=True, text=True, check=True).stdout.split("\0")
left = []
for f in filter(None, files):
    try:
        t = new_texts.get(f) or pathlib.Path(f).read_text()
    except (UnicodeDecodeError, IsADirectoryError):
        continue
    for n, line in enumerate(t.splitlines(), 1):
        hit = [k for k, p in PAT.items() if p.search(line) and (k == "BAN" or "blocking" not in line.lower())]
        if hit:
            left.append(f"{','.join(hit)} {f}:{n}")
print(f"{len(cap)} cap rows, {len(swp)} sweep rows; errors: {len(errors)}")
print(*errors, sep="\n")
print(f"after applying both tables, {len(left)} lines still match:")
print(*left, sep="\n")
