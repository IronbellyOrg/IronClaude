"""T6 smoke: install_l2 on a temp repo with HOME pointing at copies of the hooks."""

import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

repo = Path(sys.argv[1])
mod_path = repo / "src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py"
base = Path(tempfile.mkdtemp(prefix="smoke441-"))
home = base / "home"
(home / ".claude/hooks").mkdir(parents=True)
for n in ("launch-level-pre-push.sh", "launch-job-identity.sh"):
    dst = home / ".claude/hooks" / n
    shutil.copy2(repo / "src/superclaude/hooks/scripts" / n, dst)
    dst.chmod(0o755)
os.environ["HOME"] = str(home)
wt = base / "wt"
subprocess.run(["git", "init", "-q", str(wt)], check=True)
spec = importlib.util.spec_from_file_location("ow", mod_path)
ow = importlib.util.module_from_spec(spec)
sys.modules["ow"] = ow
spec.loader.exec_module(ow)
hooks = wt / ".git/hooks"
(hooks / "pre-commit").write_text("#!/bin/sh\nexit 0\n")
before = {p.name: p.read_bytes() for p in hooks.iterdir()}
print("first:", ow.install_l2(str(wt)))
after = {p.name: p.read_bytes() for p in hooks.iterdir()}
print("others unchanged:", all(after[k] == v for k, v in before.items()),
      "new:", sorted(set(after) - set(before)))
print("second:", ow.install_l2(str(wt)))
hooks = wt / ".git/hooks"
print("entries:", sorted(p.name for p in hooks.iterdir() if "launch" in p.name or p.name == "pre-push" or p.name.startswith(".")))
(hooks / "pre-push.launch-level").write_text("x\n")
print("data-differs:", ow.install_l2(str(wt))[0])
(hooks / "pre-push.launch-level").unlink()
(hooks / "pre-push").unlink()
(hooks / "pre-push").write_text("#!/bin/sh\nexit 0\n")
print("foreign:", ow.install_l2(str(wt))[0])
subprocess.run(["git", "-C", str(wt), "config", "core.hooksPath", "x"], check=True)
print("hookspath:", ow.install_l2(str(wt)))
m = base / "main"
subprocess.run(["git", "init", "-q", str(m)], check=True)
g = ["git", "-C", str(m), "-c", "user.name=t", "-c", "user.email=t@t"]
subprocess.run([*g, "commit", "-q", "--allow-empty", "-m", "i"], check=True)
subprocess.run([*g, "worktree", "add", "-q", str(base / "lw")], check=True)
print("linked:", ow.install_l2(str(base / "lw")), (m / ".git/hooks/pre-push").is_file())
shutil.rmtree(base)
