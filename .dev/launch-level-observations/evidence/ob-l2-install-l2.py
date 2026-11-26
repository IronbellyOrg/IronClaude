import sys, importlib.util
spec = importlib.util.spec_from_file_location("orca_worktree", "/home/coder/workspaces/worktrees/IronClaude/l2-refusal-test/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py")
m = importlib.util.module_from_spec(spec); sys.modules["orca_worktree"] = m; spec.loader.exec_module(m)
wt = sys.argv[2]
print("IR7_REFUSE =", m.IR7_REFUSE)
if sys.argv[1] == "install":
    print("l2_status before:", m.l2_status(wt))
    print("install_l2:", m.install_l2(wt))
print("l2_status:", m.l2_status(wt))
