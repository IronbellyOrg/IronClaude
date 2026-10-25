"""Check Task 1 preservation, including the exact user-approved manifest exception."""

import hashlib
import json
import subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[6]


def main():
    contract = json.loads((OUT / "plugin-contract.json").read_text())
    original_manifest = (OUT / "isolation/plugin/.claude-plugin/plugin.json").read_bytes()
    current_manifest = (ROOT / ".claude-plugin/plugin.json").read_bytes()
    manifest_ok = current_manifest == original_manifest.replace(b'  "homepage": "",\n', b"", 1)
    changed = [name for name, digest in contract["protected_sha256"].items() if name != ".claude-plugin/plugin.json" and (not (ROOT / name).is_file() or hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != digest)]
    retired = [".github/workflows/pull-sync-framework.yml", "scripts/sync_from_framework.py", "docs/.framework-sync-commit", "commands/sc-estimate.md", "commands/sc-sc.md", "commands/sc-select-tool.md"]
    restored = [name for name in retired if (ROOT / name).exists() or (ROOT / name).is_symlink()]
    added_resources = [row["destination"] for row in contract["candidate_resources"] if (ROOT / row["destination"]).exists()]
    tracked_diff = subprocess.check_output(["git", "diff", "--name-only", contract["baseline"]["head"]], cwd=ROOT, text=True).splitlines()
    index_diff = subprocess.check_output(["git", "diff", "--cached", "--name-only"], cwd=ROOT, text=True).splitlines()
    forbidden_diff = [name for name in tracked_diff if name != ".claude-plugin/plugin.json"]
    init = json.loads((OUT / "loader-candidates-init.json").read_text())
    loaded = any(row["name"] == "sc" for row in init["plugins"])
    mappings_ok = all(row["verified"] for row in contract["commands"] + contract["existing_agents"] + contract["candidate_resources"] + contract["skills"])
    record = {
        "protected_hash_count": len(contract["protected_sha256"]), "changed_protected": changed,
        "manifest_exact_authorized_change": manifest_ok, "retired_restored": restored,
        "candidate_resources_added": added_resources, "tracked_diff_paths": tracked_diff,
        "index_diff_paths": index_diff,
        "preservation": "PASS" if manifest_ok and not (changed or restored or added_resources or forbidden_diff or index_diff) else "FAIL",
        "plugin_loaded": loaded, "mappings_verified": mappings_ok,
        "required_closure_present": contract["required_closure"] is not None,
        "runtime_audit_proofs": "NOT RUN: Task 4 only",
    }
    (OUT / "preservation-revised.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))
    if record["preservation"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
