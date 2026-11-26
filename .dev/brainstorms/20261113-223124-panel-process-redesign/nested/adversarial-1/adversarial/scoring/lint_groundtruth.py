"""REQ-07 style lint: report any 4-word sequence of the draft instruction wording (blockquote lines) of the merged
specification that also occurs in a string field of the three study packages' ground-truth.json files.

Run: uv run python lint_groundtruth.py <merged-spec.md> <ground-truth.json>...
Prints the hits (shingle and the ground-truth file); exit code 1 if any hit.
"""
import json
import re
import sys
from pathlib import Path


def words(s):
    return re.findall(r"[a-z0-9_.\-/]+", s.lower())


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


def shingles(ws, n=4):
    return {" ".join(ws[i:i + n]) for i in range(len(ws) - n + 1)}


spec = Path(sys.argv[1]).read_text()
quoted = " \n".join(ln[1:] for ln in spec.splitlines() if ln.startswith(">"))
qsh = shingles(words(quoted))
hits = {}
for gt in sys.argv[2:]:
    data = json.loads(Path(gt).read_text())
    for s in strings(data):
        if len(s) < 25:
            continue
        for sh in shingles(words(s)) & qsh:
            hits.setdefault(sh, set()).add(Path(gt).parent.name)
print(f"blockquote shingles: {len(qsh)}; ground-truth files: {len(sys.argv) - 2}; hits: {len(hits)}")
for sh, files in sorted(hits.items()):
    print(f"  '{sh}'  <-  {sorted(files)}")
sys.exit(1 if hits else 0)
