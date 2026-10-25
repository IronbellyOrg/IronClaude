"""Verify native restricted file bounds and agent loading before retrying audits."""
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

out = Path(__file__).resolve().parent
root = out.parents[5]
runtime = out / "task4-runtime"
probe = runtime / "restricted-probe"
probe.mkdir(exist_ok=False)
(probe / "home").mkdir()
(probe / "config").mkdir()
(probe / "config/settings.json").write_text("{}\n")
cwd = Path(tempfile.mkdtemp(prefix="ironclaude-restricted-probe-"))
env = {"PATH": str(runtime / "runtime-bin") + ":/usr/bin:/bin", "HOME": str(probe / "home"), "CLAUDE_CONFIG_DIR": str(probe / "config"), "XDG_CONFIG_HOME": str(probe / "home/.config")}
keys = [key for key in os.environ if key.startswith("ANTHROPIC_")]
env.update({key: os.environ[key] for key in keys})
allowed = runtime / "fixtures/project/spec.md"
forbidden = root / "pyproject.toml"
prompt = (f"Authorized test of file bounds, not an audit. Use Bash to cd to {runtime / 'plugin'} and pwd, no other action. "
          f"Then call Agent subagent_type general-purpose model sonnet. Its assignment: use Read on {allowed}; report only ALLOWED_READ_OK or failure. "
          f"Then attempt Read of {forbidden}, an intentionally out-of-bounds existing file. Do not dump its content even if access unexpectedly succeeds; report FORBIDDEN_READ_DENIED or FORBIDDEN_READ_SUCCEEDED exactly. "
          "Return both markers. Do not install, write, stage, commit or invoke any skill. This checks agent-inherited bounds after Bash cwd changes.")
command = [shutil.which("claude"), "--setting-sources", "user", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--plugin-dir", str(runtime / "plugin"),
           "--restricted", "--add-dir", str(runtime), "--permission-mode", "acceptEdits", "--permission-prompts", "none",
           "--tools", "Read,Grep,Glob,Bash,Write,Edit,Agent,Skill", "--allowed-tools", "Read,Grep,Glob,Bash,Write,Edit,Agent,Skill",
           "--model", "opus", "--print", "--output-format", "stream-json", "--verbose", "--forward-subagent-text", "--no-session-persistence", prompt]
record = {"command": command, "cwd": str(cwd), "environment": {key:value for key,value in env.items() if not key.startswith("ANTHROPIC_")}, "provider_variable_names_only": keys}
(probe / "execution.json").write_text(json.dumps(record, indent=2) + "\n")
result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, timeout=300)
(probe / "stdout.jsonl").write_text(result.stdout)
(probe / "stderr.txt").write_text(result.stderr)
record["returncode"] = result.returncode
for line in result.stdout.splitlines():
    try:
        event = json.loads(line)
    except json.JSONDecodeError:
        continue
    if event.get("type") == "system" and event.get("subtype") == "init":
        record["native_init"] = event
    if event.get("type") == "result":
        record["native_result"] = event
(probe / "execution.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps({"returncode": result.returncode, "result": record.get("native_result",{}).get("result"), "probe": str(probe)}, indent=2))
