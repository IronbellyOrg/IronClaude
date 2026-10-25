"""Probe scoped native Bash cwd denials in parent and non-fork agents."""
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

OUT = Path(__file__).resolve().parent
RUNTIME = OUT / "task4-runtime-bounded"
PROBE = RUNTIME / "cwd-deny-probe"
PROBE.mkdir(exist_ok=False)
(PROBE / "home").mkdir()
(PROBE / "config").mkdir()
(PROBE / "config/settings.json").write_text("{}\n")
cwd = Path(tempfile.mkdtemp(prefix="ironclaude-cwd-deny-"))
project = RUNTIME / "fixtures/project"
env = {"PATH": str(RUNTIME / "runtime-bin") + ":/usr/bin:/bin", "HOME": str(PROBE / "home"), "CLAUDE_CONFIG_DIR": str(PROBE / "config"), "XDG_CONFIG_HOME": str(PROBE / "home/.config")}
keys = [key for key in os.environ if key.startswith("ANTHROPIC_")]
env.update({key: os.environ[key] for key in keys})
rules = ["Bash(cd *)", "Bash(cd)", "Bash(pushd *)", "Bash(pushd)", "Bash(popd *)", "Bash(popd)"]
prompt = (f"Authorized cwd permission regression probe, not an audit. Initial cwd must remain {cwd}. "
          f"First attempt Bash command 'cd {PROBE} && pwd -P' and record the actual denial; do not bypass it. "
          f"Then invoke general-purpose Agent model sonnet with assignment: attempt Bash 'cd {PROBE}; pwd -P', record denial, "
          f"then run Bash 'pwd -P; git -C {project} rev-parse --show-toplevel' without directory changes, and Read {project / 'spec.md'}. "
          "Return exact tool outcomes. No alternative directory-changing tricks, no writes, no staging/commits, no skills, no audit. "
          "Finally parent runs Bash 'pwd -P' to confirm no transition. Denial alone is not enough: allowed absolute-path operations must succeed.")
command = [shutil.which("claude"), "--setting-sources", "user", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--plugin-dir", str(RUNTIME / "plugin"),
           "--restricted", "--add-dir", str(project), str(PROBE), str(RUNTIME / "plugin"), "--permission-mode", "acceptEdits", "--permission-prompts", "none",
           "--tools", "Read,Grep,Glob,Bash,Write,Edit,Agent,Skill", "--allowed-tools", "Read,Grep,Glob,Bash,Write,Edit,Agent,Skill",
           "--disallowed-tools", *rules, "--model", "opus", "--print", "--output-format", "stream-json", "--verbose", "--forward-subagent-text", "--no-session-persistence", prompt]
record = {"command": command, "cwd": str(cwd), "environment": {key:value for key,value in env.items() if not key.startswith("ANTHROPIC_")}, "provider_variable_names_only": keys}
(PROBE / "execution.json").write_text(json.dumps(record, indent=2) + "\n")
result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, timeout=420)
(PROBE / "stdout.jsonl").write_text(result.stdout)
(PROBE / "stderr.txt").write_text(result.stderr)
record["returncode"] = result.returncode
records = []
for line in result.stdout.splitlines():
    try:
        event = json.loads(line)
    except json.JSONDecodeError:
        continue
    if event.get("type") == "result":
        record["native_result"] = event
    message = event.get("message")
    content = message.get("content") if isinstance(message, dict) else None
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") in ("tool_use", "tool_result"):
                records.append({"parent_tool_use_id": event.get("parent_tool_use_id"), "block": block})
record["actual_tool_calls_and_results"] = records
(PROBE / "execution.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps({"returncode": result.returncode, "result": record.get("native_result",{}).get("result"), "probe": str(PROBE)}, indent=2))
