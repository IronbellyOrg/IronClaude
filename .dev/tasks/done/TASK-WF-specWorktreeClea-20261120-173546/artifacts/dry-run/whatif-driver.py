"""What-if dry run: the same `list`, but with an empty fake /proc, so rule 6 sees no process.

Read only: `list` never removes, writes no file and never passes --apply. This shows what rules
7 and 8 say about the worktrees that rule 6 held back because /proc/352 (a same-user Electron
sandbox helper) cannot be read. It is not a real answer: an empty /proc means "no process
anywhere", which the real script never assumes.
"""

import importlib.util
import os
import sys
import tempfile

spec = importlib.util.spec_from_file_location(
    "worktree_cleanup", "scripts/worktree_cleanup.py"
)
mod = importlib.util.module_from_spec(spec)
sys.modules["worktree_cleanup"] = mod
spec.loader.exec_module(mod)
empty = tempfile.mkdtemp(prefix="empty-proc-")
code = mod.main(["list"], proc_root=empty, cwd=os.getcwd())
print(f"exit={code}", file=sys.stderr)
