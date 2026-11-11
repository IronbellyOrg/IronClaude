"""Rebuild research/research-notes.md as it was before the Gate 1 fix agent edited it (no Write exists in the logs).

The file has only Edit events (all by one Gate 1 fix agent, 16:07 to 16:11 UTC). Reverse-apply them to the file on disk,
newest first (new_string -> old_string, each must match exactly once), then forward-replay the same edits on the
result and require the sha256 of the disk file again (round trip). Read-only on the Coder worktree and ~/.claude.

Usage: uv run --no-project python -I reverse_notes.py <disk_file> <out_file>
"""
import hashlib
import runpy
import sys
import os

here = os.path.dirname(os.path.abspath(__file__))
mod = runpy.run_path(os.path.join(here, "reconstruct.py"))
collect, apply_edit = mod["collect"], mod["apply_edit"]

disk, out = sys.argv[1], sys.argv[2]
final = open(disk, encoding="utf-8").read()
ev = [e for e in collect("research/research-notes.md") if e[3] == "Edit"]
print("edits:", len(ev), "agents:", sorted({e[1] for e in ev}), "first", ev[0][0], "last", ev[-1][0])
text = final
for ts, label, ln, name, inp in reversed(ev):
    new, old = inp["new_string"], inp["old_string"]
    if new == "":
        raise SystemExit(f"cannot reverse a deletion edit at {label} L{ln}")
    n = text.count(new)
    if inp.get("replace_all") or n != 1:
        raise SystemExit(f"reverse of {label} L{ln} ambiguous: new_string occurs {n} times")
    text = text.replace(new, old, 1)
open(out, "w", encoding="utf-8").write(text)
fwd = text
for ts, label, ln, name, inp in ev:
    fwd = apply_edit(fwd, inp["old_string"], inp["new_string"], bool(inp.get("replace_all")))
ok = hashlib.sha256(fwd.encode()).hexdigest() == hashlib.sha256(final.encode()).hexdigest()
print("round trip ok:", ok, "| derived size", len(text.encode()), "lines", text.count("\n"))
