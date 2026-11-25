"""Issue 597 closeout replay: merged rule 11 (origin/integration) vs the same file without it; 6 paid sessions, Sonnet 5.5 only."""
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
MODEL = "claude-sonnet-5-5"
GUIDE_DESCRIPTION = (
    'Use this agent when the user asks questions ("Can Claude...", "Does Claude...", "How do I...") '
    "about: (1) Claude Code (the CLI tool) - features, hooks, slash commands, MCP servers, settings, "
    "IDE integrations, keyboard shortcuts; (2) Claude Agent SDK - building custom agents; "
    "(3) Claude API (formerly Anthropic API) - Messages API, tool use, prompt caching, and general "
    "Anthropic SDK usage."
)
GUIDE = {
    "claude-code-guide": {
        "description": GUIDE_DESCRIPTION,
        "prompt": "You are the Claude Code guide. Answer the question using the tools you have.",
        "tools": ["Glob", "Grep", "Read", "WebFetch", "WebSearch"],
        "model": MODEL,
    }
}
DOCS = "In Next.js 15, how do I write a route handler that streams a response? Give me the API and a short example."
PLAYWRIGHT = "What is the latest stable release version of Playwright, and what changed in it?"
NATURAL = "How do I configure a PreToolUse hook in Claude Code's settings.json so it blocks a specific Bash command?"
SUBAGENT = ("Use a subagent to do the research if you can. Question: how do I hide thinking and "
            "tool-call details in the Claude Code terminal output?")
# (case, arm, repeat, prompt, guide_agent, mcp_connected)
PLAN = [
    ("D1-docs", "after", 1, DOCS, False, True),
    ("T1-current", "after", 1, PLAYWRIGHT, False, True),
    ("G1-natural-guide", "before", 1, NATURAL, True, True),
    ("G1-natural-guide", "after", 1, NATURAL, True, True),
    ("G2-subagent-guide", "before", 1, SUBAGENT, True, True),
    ("G2-subagent-guide", "after", 1, SUBAGENT, True, True),
]


def run_case(case, arm, repeat, prompt, guide, mcp_on, context, research, env):
    name = f"{case}-{arm}-r{repeat}"
    folder = OUT / name
    folder.mkdir()
    marker = folder / "attempt.json"
    (folder / "core-context.md").write_text(context)
    (folder / "prompt.txt").write_text(prompt + "\n")
    tools = "Read,Grep,Glob,Agent,WebFetch,WebSearch"
    allowed = tools + ",Task,mcp__litellm__context7-*,mcp__litellm__Tavily-*"
    with tempfile.TemporaryDirectory(prefix="delegation-") as private:
        mcp = Path(private) / "mcp.json"
        mcp.write_text(json.dumps({"mcpServers": {"litellm": research} if mcp_on else {}}))
        mcp.chmod(0o600)
        command = [
            "claude", "--print", "--model", MODEL, "--max-turns", "6", "--max-budget-usd", "1",
            "--output-format", "stream-json", "--verbose", "--no-session-persistence",
            "--permission-mode", "dontAsk", "--permission-prompts", "none", "--setting-sources", "",
            "--tools", tools, "--allowedTools", allowed,
            "--disallowedTools", "Bash,Edit,Write,NotebookEdit",
            "--strict-mcp-config", "--mcp-config", str(mcp),
            "--append-system-prompt", context,
        ]
        if guide:
            command += ["--agents", json.dumps(GUIDE)]
        safe = [("<private>" if a == str(mcp) else a) for a in command]
        safe[safe.index("--append-system-prompt") + 1] = "<core-context.md bytes>"
        info = {
            "name": name, "state": "running", "model_requested": MODEL, "command": safe,
            "guide_agent": guide, "mcp_connected": mcp_on,
            "context_sha256": hashlib.sha256(context.encode()).hexdigest(),
            "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
            "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        marker.write_text(json.dumps(info, indent=2) + "\n")
        started = time.monotonic()
        timed_out = False
        with (folder / "stream.jsonl").open("w") as out, (folder / "stderr.txt").open("w") as err:
            proc = subprocess.Popen(command, cwd=ROOT, env=env, stdin=subprocess.PIPE, stdout=out,
                                    stderr=err, text=True, start_new_session=True)
            try:
                proc.communicate(prompt, timeout=240)
            except subprocess.TimeoutExpired:
                timed_out = True
                os.killpg(proc.pid, signal.SIGTERM)
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    os.killpg(proc.pid, signal.SIGKILL)
                    proc.wait()
    info.update(state="timeout" if timed_out else "finished", exit_code=proc.returncode,
                duration_sec=round(time.monotonic() - started, 3))
    marker.write_text(json.dumps(info, indent=2) + "\n")
    print(json.dumps({k: info[k] for k in ("name", "state", "exit_code", "duration_sec")}), flush=True)


def main():
    assert "opus" not in MODEL.lower() and len(PLAN) <= 8
    with (OUT / "started.json").open("x") as stream:
        json.dump({"model": MODEL, "sessions": len(PLAN), "per_session_usd": 1}, stream)
    after = subprocess.run(["git", "show", "origin/integration:src/superclaude/core/CLAUDE.md"], cwd=ROOT,
                           check=True, text=True, capture_output=True).stdout
    rule = next(l for l in after.splitlines() if l.startswith("11. **Research routing**"))
    baseline = after.replace(rule + "\n", "", 1)
    assert baseline != after
    (OUT / "changed-rule.txt").write_text(rule + "\n")
    research = json.loads((Path.home() / ".claude.json").read_text())["mcpServers"]["litellm"]
    env = os.environ.copy()
    for key in ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_SESSION_ID", "ORCA_TERMINAL_ID",
                "ORCA_PANE_KEY", "ORCA_AGENT_HOOK_PORT", "ORCA_AGENT_HOOK_TOKEN"):
        env.pop(key, None)
    for case, arm, repeat, prompt, guide, mcp_on in PLAN:
        run_case(case, arm, repeat, prompt, guide, mcp_on, baseline if arm == "before" else after,
                 research, env)
    print(json.dumps({"finished": True}), flush=True)


if __name__ == "__main__":
    main()
