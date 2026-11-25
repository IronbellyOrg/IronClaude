"""Capture task verification using an existing dependency environment, without installs."""
import os
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
ARTIFACTS = Path(__file__).resolve().parent
log = (ARTIFACTS / sys.argv[1]).resolve()
if not log.is_relative_to(ARTIFACTS):
    raise ValueError("Log must stay in this package's artifacts")
env = dict(os.environ, PYTHONPATH=str(ROOT / "src"), PYTHONDONTWRITEBYTECODE="1")
command = ["uv", "run", "--no-project", "--python", "/opt/uv/tools/superclaude/bin/python", *sys.argv[2:]]
result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, timeout=600)
with log.open("a", encoding="utf-8") as stream:
    stream.write("COMMAND: " + shlex.join(command) + "\n")
    stream.write("PYTHONPATH: " + str(ROOT / "src") + "\n")
    stream.write(result.stdout + result.stderr + "\nEXIT: " + str(result.returncode) + "\n")
print(result.stdout + result.stderr)
print("EXIT:", result.returncode)
sys.exit(result.returncode)
