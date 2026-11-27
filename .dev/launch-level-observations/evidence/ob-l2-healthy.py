import sys, importlib.util
spec = importlib.util.spec_from_file_location("orca_worktree", "/home/coder/workspaces/worktrees/IronClaude/l2-refusal-test/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py")
m = importlib.util.module_from_spec(spec); sys.modules["orca_worktree"] = m; spec.loader.exec_module(m)
wt = sys.argv[1]
m.install_l2(wt)                       # same two calls as cmd_launch, orca_worktree.py lines 1797-1798
l2, l2_reason = m.l2_status(wt)
l2_notes = [("W-L2-ABSENT", m.L2_ABSENT_WHY + l2_reason)] if l2 != "owned" else []   # line 1799, copied
refused = bool(m.IR7_REFUSE and l2_notes)                                              # line 1800
print("l2_status:", (l2, l2_reason)); print("l2_notes:", l2_notes); print("IR7_REFUSE:", m.IR7_REFUSE)
print("launch refused at the L2 gate:", refused, "-> proceeds to publish_pending and the agent launch" if not refused else "")
