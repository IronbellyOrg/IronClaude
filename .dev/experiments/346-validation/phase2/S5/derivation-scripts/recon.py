"""Rebuild the I5 package as it stood at the start of each final review (R1..R4).

Input : final package tree (git b5c09e90, .dev/tasks/done/<id>) and the executor session log.
Method: reverse the logged Edit calls (new_string -> old_string) newest first, and cut the
        ledger to the number of lines it had when the review began.
Output: <out>/R<k>/<id>/...  plus <out>/edits.json (the verbatim Edit inputs, in log order).
"""
import json
import shutil
import sys
from pathlib import Path

LOG, FINAL, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
ID = "TASK-WF-writeTheP0LivePl-20261103-215902"
ABS = "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/" + ID + "/"

# log line -> after which review the edit was made
EDIT_LINES = [2099, 2103, 2107, 2111, 2242, 2246, 2261, 2302, 2316, 2464]
# edits that must be reversed to reach the state at the START of review k
UNDO = {
    1: EDIT_LINES,                                  # all ten
    2: [2242, 2246, 2261, 2302, 2316, 2464],        # R1 fixes stay applied
    3: [2464],
    4: [],
}
LEDGER_LINES = {1: 12, 2: 13, 3: 15, 4: 17}

lines = LOG.read_text(encoding="utf-8").splitlines()
edits = {}
for n in EDIT_LINES:
    rec = json.loads(lines[n - 1])
    use = [b for b in rec["message"]["content"] if b.get("type") == "tool_use" and b["name"] == "Edit"][0]
    inp = use["input"]
    assert inp["file_path"].startswith(ABS), inp["file_path"]
    edits[n] = {
        "log_line": n,
        "path": inp["file_path"][len(ABS):],
        "old_string": inp["old_string"],
        "new_string": inp["new_string"],
        "replace_all": bool(inp.get("replace_all", False)),
    }
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "edits.json").write_text(json.dumps(list(edits.values()), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

for k in (1, 2, 3, 4):
    dst = OUT / f"R{k}" / ID
    if dst.parent.exists():
        shutil.rmtree(dst.parent)
    shutil.copytree(FINAL, dst)
    for n in sorted(UNDO[k], reverse=True):
        e = edits[n]
        p = dst / e["path"]
        text = p.read_text(encoding="utf-8")
        if n == 2316:
            # new_string is a bare newline; anchor on the heading that followed the removed block
            anchor = "\n\n## Post-archive check"
            if text.count(anchor) != 1:
                sys.exit("L2316 anchor not unique")
            p.write_text(text.replace(anchor, e["old_string"] + "\n## Post-archive check"), encoding="utf-8")
            continue
        cnt = text.count(e["new_string"])
        want = cnt if e["replace_all"] else 1
        if cnt != want or cnt == 0:
            sys.exit(f"R{k}: edit L{n} new_string occurs {cnt}x in {e['path']}")
        p.write_text(text.replace(e["new_string"], e["old_string"]), encoding="utf-8")
    led = dst / "progress.md"
    keep = led.read_text(encoding="utf-8").splitlines(keepends=True)[: LEDGER_LINES[k]]
    led.write_text("".join(keep), encoding="utf-8")
    print(f"R{k}: ok, reversed {len(UNDO[k])} edits, ledger {LEDGER_LINES[k]} lines")
