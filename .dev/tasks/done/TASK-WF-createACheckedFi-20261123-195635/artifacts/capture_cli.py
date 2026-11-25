"""Capture real CLI completion artifacts in a fresh task-owned root."""
import importlib
import json
import os
import subprocess
import sys
from pathlib import Path

import yaml

ARTIFACTS = Path(__file__).resolve().parent
ROOT = ARTIFACTS.parents[4]
log = ARTIFACTS / sys.argv[1]
out = ARTIFACTS / sys.argv[2]
assert log.resolve().is_relative_to(ARTIFACTS)
assert out.resolve().is_relative_to(ARTIFACTS)
home = out.parent / (out.name + "-home")
home.mkdir(exist_ok=False)
target = home / "target.txt"
target.write_text("Review this target for correctness.\n" * 10)
env = dict(os.environ, HOME=str(home), PYTHONPATH=str(ROOT / "src"), PYTHONDONTWRITEBYTECODE="1")
args = sys.argv[3:] or ["--lens", "bare-review", "--target", str(target)]
prefix = ["uv", "run", "--no-project", "--python", "/opt/uv/tools/superclaude/bin/python", "superclaude", "swarm", "run"]
seed_record = None
if args == ["resume"]:
    assert not out.exists(), "Resume evidence must begin in a fresh task-owned root"
    seed = prefix + ["--lens", "bare-review", "--target", str(target), "--transport", "stub", "--output", str(out)]
    seeded = subprocess.run(seed, env=env, cwd=ROOT, text=True, capture_output=True, timeout=60)
    seed_record = dict(command=seed, stdout=seeded.stdout, stderr=seeded.stderr, exit_code=seeded.returncode)
    assert seeded.returncode == 0, seed_record
    seed_record["removed_prior_marker"] = json.loads((out / "done.json").read_text())
    # Only this capture's newly created marker is removed, never historical evidence.
    (out / "done.json").unlink()
    assert not (out / "done.json").exists()
    args = ["--resume", json.loads((out / "manifest.json").read_text())["job_id"]]
command = [*prefix, *args, "--transport", "stub", "--output", str(out)]
result = subprocess.run(command, env=env, cwd=ROOT, text=True, capture_output=True, timeout=60)
record = {"command": command, "stdout": result.stdout, "stderr": result.stderr, "exit_code": result.returncode, "seed": seed_record}
log.write_text(json.dumps(record, indent=2) + "\n")
assert result.returncode == 0, record
state = json.loads((out / ".swarm-state.json").read_text())
contract = yaml.safe_load((out / "return-contract.yaml").read_text())
marker = json.loads((out / "done.json").read_text())
assert state["state"] == "terminal"
assert marker == {"atomic_write": True, "terminal_status": contract["status"], "contract_path": str((out / "return-contract.yaml").resolve())}
assert contract["status"] == "success"
sys.path.insert(0, str(ROOT / "src"))
module = importlib.import_module("superclaude.cli.swarm.commands")
assert Path(module.__file__).resolve() == ROOT / "src/superclaude/cli/swarm/commands.py"
record.update(state=state, contract_status=contract["status"], marker=marker, imported_commands=module.__file__, artifact_count=len(list(out.iterdir())), check="PASS")
log.write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, indent=2))
