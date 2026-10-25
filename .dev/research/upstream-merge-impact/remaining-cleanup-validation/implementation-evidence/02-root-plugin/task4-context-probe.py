"""Measure actual nested shell cwd/Git roots without reading project contents."""
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

out = Path(__file__).resolve().parent
runtime = out / "task4-runtime-bounded"
probe = runtime / "context-probe"
(probe / "artifacts").mkdir(parents=True, exist_ok=False)
(probe / "home").mkdir()
(probe / "config").mkdir()
(probe / "config/settings.json").write_text("{}\n")
cwd = Path(tempfile.mkdtemp(prefix="ironclaude-context-probe-"))
project = runtime / "fixtures/project"
env = {"PATH": str(runtime / "runtime-bin") + ":/usr/bin:/bin", "HOME": str(probe / "home"), "CLAUDE_CONFIG_DIR": str(probe / "config"), "XDG_CONFIG_HOME": str(probe / "home/.config")}
keys = [key for key in os.environ if key.startswith("ANTHROPIC_")]
env.update({key: os.environ[key] for key in keys})
prompt = (f"Authorized context measurement only, not an audit. First use Bash to cd to {probe / 'artifacts'} and run pwd -P. "
          f"Then invoke general-purpose Agent on model sonnet. Pass only this assignment: run Bash 'pwd -P; git rev-parse --show-toplevel; git -C {project} rev-parse --show-toplevel'. "
          "Return those exact command outputs. Read no files, perform no other inspection, write nothing, and do not stage or commit. "
          "This measures actual inherited nested shell cwd versus the explicit synthetic fixture root; do not guess expected results.")
command = [shutil.which("claude"), "--setting-sources", "user", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--plugin-dir", str(runtime / "plugin"),
           "--restricted", "--add-dir", str(project), str(probe), str(runtime / "plugin"), "--permission-mode", "acceptEdits", "--permission-prompts", "none",
           "--tools", "Read,Grep,Glob,Bash,Write,Edit,Agent,Skill", "--allowed-tools", "Read,Grep,Glob,Bash,Write,Edit,Agent,Skill", "--model", "opus",
           "--print", "--output-format", "stream-json", "--verbose", "--forward-subagent-text", "--no-session-persistence", prompt]
record = {"command": command, "cwd": str(cwd), "environment": {key:value for key,value in env.items() if not key.startswith("ANTHROPIC_")}, "provider_variable_names_only": keys}
(probe / "execution.json").write_text(json.dumps(record, indent=2) + "\n")
result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, timeout=300)
(probe / "stdout.jsonl").write_text(result.stdout)
(probe / "stderr.txt").write_text(result.stderr)
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
(probe / "execution.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps({"returncode": result.returncode, "result": record.get("native_result",{}).get("result"), "probe": str(probe)}, indent=2))
