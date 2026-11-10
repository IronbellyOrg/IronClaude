"""Mechanical reviser for the S5 replay: apply the original fix cycle k to a package copy.

usage: uv run --no-project python -I apply_round.py <package-dir> <k> <deltas-dir>
  <package-dir>  .../.dev/tasks/to-do/TASK-WF-writeTheP0LivePl-20261103-215902 (your COPY, never the originals)
  k              1, 2 or 3 = the fix cycle that followed review k in the original run
  <deltas-dir>   inputs/round-deltas

Applies the logged Edit calls of that cycle (each old_string must occur exactly once) and, for k=2 and k=3,
appends the owner-accepted `ARCHIVE: Ruling:` line. It never writes `FINAL:` lines: those carry the
replay's own state digest and verdict and are written by the replayed /sc:implement archive gate.
"""
import json
import sys
from pathlib import Path

pkg, k, deltas = Path(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3])
CYCLE = {1: [2099, 2103, 2107, 2111], 2: [2242, 2246, 2261, 2302, 2316], 3: [2464]}
RULING = {2: "ledger-ruling-1.txt", 3: "ledger-ruling-2.txt"}
edits = {e["log_line"]: e for e in json.loads((deltas / "edits.json").read_text(encoding="utf-8"))}
for n in CYCLE[k]:
    e = edits[n]
    p = pkg / e["path"]
    text = p.read_text(encoding="utf-8")
    if text.count(e["old_string"]) != 1:
        sys.exit(f"edit L{n}: old_string occurs {text.count(e['old_string'])}x in {e['path']}")
    p.write_text(text.replace(e["old_string"], e["new_string"]), encoding="utf-8")
    print(f"applied L{n} -> {e['path']}")
if k in RULING:
    line = (deltas / RULING[k]).read_text(encoding="utf-8")
    led = pkg / "progress.md"
    with led.open("a", encoding="utf-8") as fh:
        fh.write(line)
    print(f"appended {RULING[k]} to progress.md (write it BEFORE the next FINAL review, as the protocol requires)")
