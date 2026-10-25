"""Capture product hashes and a clean plugin-only native inventory, without installs."""

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
OUT = Path(__file__).resolve().parent


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def main():
    contract_path = OUT / "plugin-contract.json"
    contract = json.loads(contract_path.read_text())
    if contract["baseline"] is not None:
        raise SystemExit("Refusing to replace a captured baseline")
    inventory = json.loads((OUT.parents[1] / "plugin-inventory.json").read_text())
    paths = git("ls-files", "-z").split("\0")
    hashes = {}
    for name in paths:
        path = ROOT / name
        if name and not name.startswith(".dev/") and path.is_file():
            hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    for directory in ("commands", "agents", "skills/confidence-check"):
        for path in (ROOT / directory).rglob("*"):
            if path.is_file():
                hashes[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    contract["baseline"] = {
        "checkout": str(ROOT), "branch": git("branch", "--show-current"),
        "head": git("rev-parse", "HEAD"), "status": git("status", "--porcelain=v1"),
        "index_diff": git("diff", "--cached", "--stat"),
    }
    contract["protected_sha256"] = hashes
    contract["allowed_command_edits"] = list(inventory["namespace_matches"])
    contract["candidate_resources"] = inventory["candidate_resources"]
    contract["commands"] = [{"path": str(p.relative_to(ROOT)), "plugin": "sc", "expected_frontend": "sc:" + p.stem, "verified": False} for p in sorted((ROOT / "commands").glob("*.md"))]
    contract["existing_agents"] = [{"path": str(p.relative_to(ROOT)), "expected_frontend": "sc:" + p.stem, "verified": False} for p in sorted((ROOT / "agents").glob("*.md"))]
    contract["lookup_rule"] = "UNVERIFIED: plugin-qualified frontends and ${CLAUDE_PLUGIN_ROOT}-relative files, no global fallbacks"
    contract_path.write_text(json.dumps(contract, indent=2) + "\n")
    sandbox = OUT / "isolation"
    sandbox.mkdir()
    plugin = sandbox / "plugin"
    plugin.mkdir()
    for directory in (".claude-plugin", "commands", "agents", "skills"):
        shutil.copytree(ROOT / directory, plugin / directory)
    (sandbox / "home").mkdir()
    (sandbox / "config").mkdir()
    (sandbox / "work").mkdir()
    env = {"PATH": "/usr/bin:/bin", "HOME": str(sandbox / "home"), "CLAUDE_CONFIG_DIR": str(sandbox / "config"), "XDG_CONFIG_HOME": str(sandbox / "home/.config")}
    command = [shutil.which("claude"), "--setting-sources", "user", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--plugin-dir", str(plugin), "plugin", "details", "sc"]
    result = subprocess.run(command, cwd=sandbox / "work", env=env, capture_output=True, text=True, timeout=45)
    (OUT / "native-inventory.stdout.txt").write_text(result.stdout)
    (OUT / "native-inventory.stderr.txt").write_text(result.stderr)
    (OUT / "native-inventory.json").write_text(json.dumps({"command": command, "cwd": str(sandbox / "work"), "env": env, "returncode": result.returncode, "plugin_copy": str(plugin), "copied_directories": [".claude-plugin", "commands", "agents", "skills"], "global_resources": False, "package_resources": False, "mcp_servers": []}, indent=2) + "\n")
    print(f"Captured {len(hashes)} file hashes; inventory exit={result.returncode}")
    print(result.stdout)
    print(result.stderr)


if __name__ == "__main__":
    main()
