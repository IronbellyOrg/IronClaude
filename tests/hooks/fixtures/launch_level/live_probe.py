"""Bounded, opt-in live CLI observation. Never stores raw streams or credentials."""

import argparse
import hashlib
import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,127}\Z")


def append(path, event):
    fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    try:
        os.write(fd, (json.dumps(event, sort_keys=True) + "\n").encode())
    finally:
        os.close(fd)


def identities(value):
    """Keep only selector results, never arbitrary tool output or stream text."""
    found = []
    if isinstance(value, dict):
        if value.get("status") in ("governed", "ordinary", "unknown"):
            item = {"status": value["status"]}
            sid = value.get("session_id")
            if isinstance(sid, str) and ID.fullmatch(sid):
                item["session_id"] = sid
            if value.get("reason") == "released":
                item["reason"] = "released"
            found.append(item)
        else:
            for item in value.values():
                found.extend(identities(item))
    elif isinstance(value, list):
        for item in value:
            found.extend(identities(item))
    elif isinstance(value, str):
        for line in value.splitlines():
            try:
                parsed = json.loads(line)
            except ValueError:
                continue
            if isinstance(parsed, (dict, list)):
                found.extend(identities(parsed))
    return found


def observe(args):
    raw = sys.stdin.buffer.read((1 << 20) + 1)
    payload = json.loads(raw)
    inputs = payload.get("tool_input") or {}
    record = {"kind": "actual_hook_input", "variant": args.variant}
    for field in (
        "hook_event_name",
        "session_id",
        "tool_use_id",
        "agent_id",
        "agent_type",
    ):
        value = payload.get(field)
        if isinstance(value, str) and ID.fullmatch(value):
            record[field] = value
    record["tool_name"] = (
        payload.get("tool_name") if payload.get("tool_name") == "Bash" else "other"
    )
    record["top_level_keys"] = sorted(payload)
    record["tool_input_keys"] = sorted(inputs) if isinstance(inputs, dict) else []
    if isinstance(inputs, dict):
        record["run_in_background"] = inputs.get("run_in_background") is True
        command = inputs.get("command")
        if isinstance(command, str):
            record["command_sha256"] = hashlib.sha256(command.encode()).hexdigest()
    record["cwd_is_fixture"] = payload.get("cwd") == args.cwd
    if payload.get("hook_event_name") == "PostToolUse":
        response = payload.get("tool_response")
        record["tool_response_keys"] = (
            sorted(response) if isinstance(response, dict) else []
        )
        record["selector_results"] = identities(response)
        append(args.log, record)
        return 0
    result = subprocess.run(
        ["/bin/bash", args.runner], input=raw, capture_output=True, timeout=8
    )
    record["adapter_exit"] = result.returncode
    record["rewritten"] = False
    if result.stdout:
        output = json.loads(result.stdout)
        specific = output.get("hookSpecificOutput", {})
        record["rewritten"] = "updatedInput" in specific
        record["permission_decision_present"] = "permissionDecision" in specific
    append(args.log, record)
    sys.stdout.buffer.write(result.stdout)
    sys.stderr.buffer.write(result.stderr)
    return result.returncode


def cleanup_jobs(home):
    for path in (home / ".claude/state/launch-level/jobs").glob("*.json"):
        value = json.loads(path.read_text())
        pid = value["pid"]
        try:
            fields = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()
            if int(fields[3]) != pid or int(fields[19]) != value["start"]:
                continue
            os.kill(pid, signal.SIGTERM)
            until = time.monotonic() + 3
            while Path(f"/proc/{pid}").exists() and time.monotonic() < until:
                time.sleep(0.03)
        except ProcessLookupError:
            pass
        except FileNotFoundError:
            pass


def probe(args):
    log = Path(args.output_dir).resolve() / "live-harness-events.jsonl"
    runner = Path(args.runner).resolve()
    cli = shutil.which("claude")
    if not cli:
        append(log, {"kind": "probe_result", "status": "cli_unavailable"})
        print("live_cli=cli_unavailable")
        return 0
    with tempfile.TemporaryDirectory(prefix="launch-level-live-") as scratch:
        root = Path(scratch)
        home = root / "isolated-home"
        home.mkdir(mode=0o700)
        work = root / "trusted-fixture"
        work.mkdir()
        env = dict(
            os.environ,
            HOME=str(home),
            CLAUDE_CONFIG_DIR=str(home / ".claude"),
            XDG_CONFIG_HOME=str(home / ".config"),
            XDG_CACHE_HOME=str(home / ".cache"),
            UV_PYTHON=sys.executable,
            UV_PYTHON_DOWNLOADS="never",
        )
        # Keep CLAUDECODE and existing auth env intact: never evade a nested guard.
        git_env = {
            key: value for key, value in env.items() if not key.startswith("GIT_")
        }
        git_env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL="/dev/null")
        subprocess.run(
            ["git", "init", str(work)], env=git_env, capture_output=True, check=True
        )
        for variant in ("governed", "ordinary"):
            sid = str(uuid.uuid4())
            if variant == "governed":
                store = home / ".claude/state/launch-level"
                (store / "sessions").mkdir(parents=True, mode=0o700)
                store.chmod(0o700)
                level = store / "sessions" / sid
                level.write_text("worktree\n")
                level.chmod(0o600)
            observer = shlex.join(
                [
                    "uv",
                    "run",
                    "--no-project",
                    "python",
                    "-I",
                    str(Path(__file__).resolve()),
                    "observe",
                    "--runner",
                    str(runner),
                    "--log",
                    str(log),
                    "--variant",
                    variant,
                    "--cwd",
                    str(work),
                ]
            )
            settings = root / (variant + "-settings.json")
            settings.write_text(
                json.dumps(
                    {
                        "enabledPlugins": {},
                        "hooks": {
                            "PreToolUse": [
                                {
                                    "matcher": "Bash",
                                    "hooks": [
                                        {
                                            "type": "command",
                                            "command": observer,
                                            "timeout": 10,
                                        }
                                    ],
                                }
                            ],
                            "PostToolUse": [
                                {
                                    "matcher": "Bash",
                                    "hooks": [
                                        {
                                            "type": "command",
                                            "command": observer,
                                            "timeout": 10,
                                        }
                                    ],
                                }
                            ],
                        },
                    }
                )
            )
            command = (
                "printf 'LIVE_IDENTITY\\n'; /bin/bash "
                + shlex.quote(str(runner))
                + " identify; printf '%s\\n' \"$PWD\""
            )
            prompt = (
                "In this trusted disposable fixture, use Bash exactly once to execute this literal command, then report only its output: "
                + command
            )
            argv = [
                cli,
                "--print",
                "--setting-sources",
                "",
                "--settings",
                str(settings),
                "--session-id",
                sid,
                "--tools",
                "Bash",
                "--allowedTools",
                "Bash",
                "--permission-mode",
                "dontAsk",
                "--strict-mcp-config",
                "--mcp-config",
                '{"mcpServers":{}}',
                "--max-budget-usd",
                "0.25",
                "--output-format",
                "stream-json",
                "--include-hook-events",
                "--verbose",
                "--no-session-persistence",
                "--disable-slash-commands",
                "--no-chrome",
                prompt,
            ]
            process = subprocess.Popen(
                argv,
                env=env,
                cwd=work,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                errors="replace",
                start_new_session=True,
            )
            try:
                stdout, stderr = process.communicate(timeout=45)
                status = "completed" if process.returncode == 0 else "cli_error"
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    stdout, stderr = process.communicate(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    stdout, stderr = process.communicate(timeout=5)
                status = "timeout"
            finally:
                cleanup_jobs(home)
            if "cannot be launched inside another Claude Code session" in stderr:
                status = "nested_guard_blocked"
            elif any(
                text in stderr.lower()
                for text in ("not logged in", "invalid api key", "authentication")
            ):
                status = "authentication_unavailable"
            streams = []
            for line in stdout.splitlines():
                try:
                    event = json.loads(line)
                except ValueError:
                    continue
                if isinstance(event, dict):
                    streams.append(
                        {
                            "type": event.get("type"),
                            "subtype": event.get("subtype"),
                            "selector_results": identities(event.get("message", {})),
                        }
                    )
            result = {
                "kind": "probe_result",
                "variant": variant,
                "requested_session_id": sid,
                "status": status,
                "exit_code": process.returncode,
                "stdout_bytes": len(stdout.encode()),
                "stderr_bytes": len(stderr.encode()),
                "stream_events": streams,
                "unobserved": [
                    "persistent_cwd",
                    "background_scheduling",
                    "clear",
                    "resume",
                    "Monitor",
                    "auto_mode",
                    "concurrent_hook_composition",
                    "nested_subagent_payload",
                ],
            }
            if status == "nested_guard_blocked":
                result["observed_error"] = (
                    "Claude Code cannot be launched inside another Claude Code session."
                )
            append(log, result)
            print(
                "live_cli="
                + status
                + " variant="
                + variant
                + " exit="
                + str(process.returncode)
            )
            if status != "completed":
                break
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("probe", "observe"))
    parser.add_argument("--runner", required=True)
    parser.add_argument("--output-dir")
    parser.add_argument("--log")
    parser.add_argument("--variant")
    parser.add_argument("--cwd")
    args = parser.parse_args()
    return observe(args) if args.mode == "observe" else probe(args)


if __name__ == "__main__":
    sys.exit(main())
