"""T7 smoke: install_l2 and l2_status agree on a temp repo (HOME = copies of the hooks)."""

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
spec = importlib.util.spec_from_file_location("ow", mod_path)
ow = importlib.util.module_from_spec(spec)
sys.modules["ow"] = ow
spec.loader.exec_module(ow)


def both(label, wt):
    print(f"{label}: install={ow.install_l2(str(wt))} status={ow.l2_status(str(wt))}")


def status(label, wt):
    print(f"{label}: status={ow.l2_status(str(wt))}")


wt = base / "wt"
subprocess.run(["git", "init", "-q", str(wt)], check=True)
hooks = wt / ".git/hooks"
shutil.rmtree(hooks)
status("no-hooks-dir", wt)
print("no-hooks-dir created:", hooks.exists())
hooks.mkdir()
status("no-hook", wt)
both("first", wt)
both("second", wt)
(hooks / "pre-push.launch-level").write_text("x\n")
both("data-differs", wt)
(hooks / "pre-push.launch-level").unlink()
(hooks / "pre-push").unlink()
(hooks / "pre-push").write_text("#!/bin/sh\nexit 0\n")
both("foreign", wt)
(hooks / "pre-push").unlink()
pk = home / ".claude/hooks/launch-level-pre-push.sh"
saved = pk.read_bytes()
pk.unlink()
both("no-packaged", wt)
pk.write_bytes(saved)
pk.chmod(0o755)
subprocess.run(["git", "-C", str(wt), "config", "core.hooksPath", "x"], check=True)
both("hookspath", wt)
m = base / "main"
subprocess.run(["git", "init", "-q", str(m)], check=True)
g = ["git", "-C", str(m), "-c", "user.name=t", "-c", "user.email=t@t"]
subprocess.run([*g, "commit", "-q", "--allow-empty", "-m", "i"], check=True)
subprocess.run([*g, "worktree", "add", "-q", str(base / "lw")], check=True)
both("linked", base / "lw")
print("linked in common dir:", (m / ".git/hooks/pre-push").is_file())
nr = base / "not-a-repo"
nr.mkdir()
both("not-a-repo", nr)
shutil.rmtree(base)
