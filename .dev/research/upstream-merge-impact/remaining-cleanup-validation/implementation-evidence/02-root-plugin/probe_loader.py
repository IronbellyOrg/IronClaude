"""Record native validation and session initialization with only the root plugin."""

import argparse
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

OUT = Path(__file__).resolve().parent
SANDBOX = OUT / "isolation-corrected"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", default="isolation-corrected")
    parser.add_argument("--label", default="external")
    args = parser.parse_args()
    sandbox = OUT / args.fixture
    label = args.label
    work = Path(tempfile.mkdtemp(prefix="ironclaude-root-plugin-"))
    env = {
        "PATH": "/usr/bin:/bin", "HOME": str(sandbox / "home"),
        "CLAUDE_CONFIG_DIR": str(sandbox / "config"),
        "XDG_CONFIG_HOME": str(sandbox / "home/.config"),
    }
    credential_keys = [k for k in os.environ if k.startswith("ANTHROPIC_")]
    env.update({k: os.environ[k] for k in credential_keys})
    client = shutil.which("claude")
    base = [client, "--setting-sources", "user", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--plugin-dir", str(sandbox / "plugin")]
    probes = {
        "validate": [client, "plugin", "validate", str(sandbox / "plugin")],
        "session": base + ["--print", "--output-format", "stream-json", "--verbose", "--tools", "Agent,Skill,Read", "--agent", "sc:sc-root-cause-analyst", "--no-session-persistence", "Reply INVENTORY_ONLY. Do not invoke any skills or perform any actions."],
    }
    records = {"cwd": str(work), "env": {k: v for k, v in env.items() if not k.startswith("ANTHROPIC_")}, "inherited_provider_variable_names_only": credential_keys, "probes": {}}
    for name, command in probes.items():
        try:
            process = subprocess.run(command, cwd=work, env=env, capture_output=True, text=True, timeout=90)
            stdout, stderr, rc = process.stdout, process.stderr, process.returncode
        except subprocess.TimeoutExpired as error:
            stdout = (error.stdout or b"").decode() if isinstance(error.stdout, bytes) else (error.stdout or "")
            stderr = (error.stderr or b"").decode() if isinstance(error.stderr, bytes) else (error.stderr or "")
            rc = "TIMEOUT"
        (OUT / f"loader-{label}-{name}.stdout.txt").write_text(stdout)
        (OUT / f"loader-{label}-{name}.stderr.txt").write_text(stderr)
        records["probes"][name] = {"command": command, "returncode": rc}
        (OUT / f"loader-{label}-probes.json").write_text(json.dumps(records, indent=2) + "\n")
        print(f"{name}: returncode={rc}")
        if name == "validate":
            print(stdout)
            print(stderr)
        else:
            for line in stdout.splitlines():
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if event.get("type") == "system" and event.get("subtype") == "init":
                    summary = {key: event.get(key) for key in ("type", "subtype", "plugins", "skills", "slash_commands", "agents", "mcp_servers")}
                    (OUT / f"loader-{label}-init.json").write_text(json.dumps(summary, indent=2) + "\n")
                    print(json.dumps(summary))
                if event.get("type") == "result":
                    print(json.dumps({key: event.get(key) for key in ("type", "subtype", "is_error", "result", "errors")}))
            print(stderr)


if __name__ == "__main__":
    main()
