"""Capture the real detached boundary without repairing or substituting child argv."""
import json
import os
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path

ARTIFACTS = Path(__file__).resolve().parent
ROOT = ARTIFACTS.parents[4]
sys.path.insert(0, str(ROOT / "src"))
from superclaude.cli.swarm import tmux
from superclaude.cli.swarm.commands import _build_spec_from_lens

log = ARTIFACTS / "detached-check.txt"
if shutil.which("tmux") is None or "TMUX" in os.environ:
    record = {"check": "SKIP", "reason": "tmux missing or unsupported nesting", "repair_closure": "NOT PROVEN"}
    log.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record))
    sys.exit(0)
base = ARTIFACTS / "detached-cli"
if len(sys.argv) > 1:
    base = base / sys.argv[1]
base.mkdir(exist_ok=False)
home = base / "home"
home.mkdir()
out = base / "out"
target = base / "target.txt"
target.write_text("Review this isolated detached completion target.\n" * 10)
spec = _build_spec_from_lens("bare-review")
spec["job_id"] = "completion-" + uuid.uuid4().hex[:12]
spec["target"]["path"] = str(target)
spec["output"]["dir"] = str(out)
spec["transport"]["kind"] = "stub"
path = base / "spec.json"
path.write_text(json.dumps(spec))
env = dict(os.environ, HOME=str(home), PYTHONPATH=str(ROOT / "src"), PYTHONDONTWRITEBYTECODE="1")
command = ["uv", "run", "--no-project", "--python", sys.executable, "superclaude", "swarm", "run", str(path), "--detached", "--output", str(out)]
result = subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True, timeout=30)
try:
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline and not (out / "done.json").exists():
        if not tmux.has_session(spec["job_id"]):
            break
        time.sleep(0.1)
    record = {"command": command, "stdout": result.stdout, "stderr": result.stderr, "exit_code": result.returncode,
              "tmux_available": True, "nested": False, "deadline_seconds": 10,
              "artifacts": sorted(p.name for p in out.iterdir()) if out.exists() else [],
              "state_exists": (out / ".swarm-state.json").exists(), "contract_exists": (out / "return-contract.yaml").exists(),
              "marker_exists": (out / "done.json").exists(), "imported_package": str(ROOT / "src/superclaude/cli/swarm")}
    import inspect
    import yaml

    record["imported_package"] = inspect.getfile(_build_spec_from_lens)
    if record["marker_exists"] and record["state_exists"] and record["contract_exists"]:
        marker = json.loads((out / "done.json").read_text())
        contract = yaml.safe_load((out / "return-contract.yaml").read_text())
        state = json.loads((out / ".swarm-state.json").read_text())
        record.update(marker=marker, contract_status=contract["status"], state=state["state"])
        expected = {"atomic_write": True, "terminal_status": contract["status"],
                    "contract_path": str((out / "return-contract.yaml").resolve())}
        passed = result.returncode == 0 and marker == expected and contract["status"] == "success" and state["state"] == "terminal"
    else:
        passed = False
    record["check"] = "PASS" if passed else "FAIL"
    with log.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))
finally:
    if tmux.has_session(spec["job_id"]):
        tmux.kill(spec["job_id"])
sys.exit(0 if record["check"] == "PASS" else 1)
