"""Capture Task 4's accepted resource and protected-product baseline before edits."""
import hashlib
import json
import subprocess
from pathlib import Path

out = Path(__file__).resolve().parent
root = out.parents[5]
contract = json.loads((out / "plugin-contract.json").read_text())
paths = set(contract["protected_sha256"]) | {row["destination"] for row in contract["candidate_resources"]}
record = {"head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(),
          "branch": subprocess.check_output(["git", "branch", "--show-current"], cwd=root, text=True).strip(),
          "status": subprocess.check_output(["git", "status", "--short"], cwd=root, text=True),
          "sha256": {path: hashlib.sha256((root / path).read_bytes()).hexdigest() for path in sorted(paths)},
          "task3_resource_sha256": {row["destination"]: hashlib.sha256((root / row["destination"]).read_bytes()).hexdigest() for row in contract["candidate_resources"]},
          "allowed_task4_product_edit": "commands/sc-reflect.md"}
target = out / "task4-baseline.json"
with target.open("x") as handle:
    json.dump(record, handle, indent=2)
    handle.write("\n")
print(target)
