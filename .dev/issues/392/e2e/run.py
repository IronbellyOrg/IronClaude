"""Isolated end-to-end proof. Run with uv run --extra dev python .../run.py [--live].

Never starts, stops or changes the shared shim. Child shims use free ports,
explicit upstreams and this checkout's code. Only model ids and error metadata
are captured from gateway traffic. Credentials come from the environment.
"""

import argparse
import contextlib
import http.server
import json
import os
import socket
import subprocess
import sys
import threading
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKILL = ROOT / "src/superclaude/skills/ccsession-tag"
sys.path.insert(0, str(SKILL))
import models  # noqa: E402


def redact(text):
    for key, value in os.environ.items():
        if value and key.endswith(
            ("_KEY", "_TOKEN", "_SECRET", "_PASSWORD", "_COOKIE")
        ):
            text = text.replace(value, "<REDACTED>")
    return text


def save(name, data):
    text = data if isinstance(data, str) else json.dumps(data, indent=2)
    (HERE / name).write_text(redact(text) + "\n")


def event(name, data):
    return f"event: {name}\ndata: {json.dumps(data)}\n\n".encode()


def success(model):
    return b"".join(
        [
            event(
                "message_start",
                {
                    "type": "message_start",
                    "message": {
                        "id": "msg_ccsession_e2e",
                        "type": "message",
                        "role": "assistant",
                        "model": model,
                        "content": [],
                        "stop_reason": None,
                        "stop_sequence": None,
                        "usage": {"input_tokens": 1, "output_tokens": 0},
                    },
                },
            ),
            event(
                "content_block_start",
                {
                    "type": "content_block_start",
                    "index": 0,
                    "content_block": {"type": "text", "text": ""},
                },
            ),
            event(
                "content_block_delta",
                {
                    "type": "content_block_delta",
                    "index": 0,
                    "delta": {"type": "text_delta", "text": "OK"},
                },
            ),
            event("content_block_stop", {"type": "content_block_stop", "index": 0}),
            event(
                "message_delta",
                {
                    "type": "message_delta",
                    "delta": {"stop_reason": "end_turn", "stop_sequence": None},
                    "usage": {"output_tokens": 1},
                },
            ),
            event("message_stop", {"type": "message_stop"}),
        ]
    )


class Gateway(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(
            json.dumps(
                {
                    "data": [
                        {"id": m, "type": "model", "display_name": m}
                        for m in self.server.listing
                    ]
                }
            ).encode()
        )

    def do_POST(self):
        obj = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        model = obj.get("model")
        if self.path.split("?")[0].endswith("count_tokens"):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"input_tokens":100}')
            return
        self.server.calls.append(model)
        count = self.server.calls.count(model)
        status, raw = 200, success(model)
        if (
            self.server.scenario == "tier"
            and model == self.server.primary
            and count <= 3
        ):
            status, raw = (
                500,
                json.dumps(
                    {
                        "type": "error",
                        "error": {
                            "type": "api_error",
                            "message": "Scripted internal server error",
                        },
                    }
                ).encode(),
            )
        if self.server.scenario == "named" and model == "claude-opus-5-5":
            status, raw = (
                429,
                json.dumps(
                    {
                        "type": "error",
                        "error": {
                            "type": "rate_limit_error",
                            "message": "All accounts are cooling down",
                        },
                    }
                ).encode(),
            )
        if self.server.scenario == "stream-error" and count == 1:
            raw = event(
                "error",
                {
                    "type": "error",
                    "error": {
                        "type": "overloaded_error",
                        "message": "Scripted overloaded",
                    },
                },
            )
        self.send_response(status)
        self.send_header(
            "Content-Type", "text/event-stream" if status == 200 else "application/json"
        )
        self.end_headers()
        self.wfile.write(raw)
        self.wfile.flush()


@contextlib.contextmanager
def shim(upstream, scenario, script=None):
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    env = os.environ.copy()
    env.update(
        GW_PROXY_UPSTREAM=upstream,
        GW_PROXY_PORT=str(port),
        CCSESSION_DIR=str(SKILL),
        GW_PROXY_LOGFILE=str(HERE / f"{scenario}-proxy.log"),
        CCSESSION_MODELS_REFRESH="0",
        CCSESSION_FIRST_BYTE_TIMEOUT="60",
        CCSESSION_FAILS_BEFORE_SWITCH="3",
        CCSESSION_PARK_SECONDS="300",
        CCSESSION_PARK_MAX_SECONDS="3600",
        CCSESSION_COOLDOWN_SECONDS="3600",
    )
    # Separate run labels preserve evidence from each attempt.
    with (HERE / f"{scenario}-stderr.log").open("w") as log:
        proc = subprocess.Popen(
            [sys.executable, str(script or SKILL / "local-gateway-alias-proxy.py")],
            env=env,
            stdout=log,
            stderr=log,
        )
        base = f"http://127.0.0.1:{port}"
        try:
            for _ in range(100):
                if proc.poll() is not None:
                    raise RuntimeError("Child shim exited before health check")
                try:
                    with urllib.request.urlopen(
                        base + "/__ccsession_shim", timeout=1
                    ) as response:
                        health = json.load(response)
                    assert health["pid"] == proc.pid
                    break
                except OSError:
                    time.sleep(0.1)
            else:
                raise RuntimeError("Child shim did not become healthy")
            yield base
        finally:
            proc.terminate()
            proc.wait(timeout=10)


def claude(base, model, scenario):
    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["ANTHROPIC_BASE_URL"] = base
    env["CLAUDE_CODE_MAX_RETRIES"] = "5"
    # Bare mode skips hooks/plugins/memory. No helper agents or tools can run.
    credential = (
        env.get("ANTHROPIC_AUTH_TOKEN")
        or env.get("ANTHROPIC_API_KEY")
        or env["LITELLM_API_KEY"]
    )
    env["ANTHROPIC_API_KEY"] = credential
    command = [
        "claude",
        "--bare",
        "-p",
        "Reply with the word OK",
        "--model",
        model,
        "--no-session-persistence",
        "--output-format",
        "json",
        "--tools",
        "",
        "--strict-mcp-config",
        "--mcp-config",
        '{"mcpServers":{}}',
    ]
    started = time.monotonic()
    result = subprocess.run(
        command, env=env, cwd=HERE, text=True, capture_output=True, timeout=300
    )
    save(
        f"{scenario}-claude.json",
        {
            "command": command,
            "returncode": result.returncode,
            "seconds": round(time.monotonic() - started, 2),
            "stdout": result.stdout,
            "stderr": result.stderr,
        },
    )
    assert result.returncode == 0, (
        f"{scenario}: Claude exited {result.returncode}; see evidence file"
    )
    events = json.loads(result.stdout)
    if isinstance(events, dict):
        events = [events]
    answer = next(e for e in reversed(events) if e.get("type") == "result")
    assert answer.get("result", "").strip() == "OK", f"{scenario}: unexpected answer"
    assert answer.get("subagent_stats", {}).get("spawned", 0) == 0
    save(
        f"{scenario}-summary.json",
        {
            "model_requested": model,
            "result": answer["result"],
            "returncode": result.returncode,
            "retries": [e for e in events if e.get("subtype") == "api_retry"],
            "answering_models": [
                e["message"]["model"] for e in events if e.get("type") == "assistant"
            ],
        },
    )
    return answer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--shim-script", type=Path)
    parser.add_argument("--named-model", default="claude-opus-5-5")
    parser.add_argument("--label", default="live")
    args = parser.parse_args()
    with urllib.request.urlopen(
        "http://127.0.0.1:4078/__ccsession_shim", timeout=5
    ) as response:
        shared = json.load(response)
    if args.live:
        # The upstream is used in memory only; no credentials or gateway URL saved.
        with shim(shared["upstream"], args.label, script=args.shim_script) as base:
            for label, model in (
                ("tier", "claude-gw-tier2"),
                ("named", args.named_model),
            ):
                claude(base, model, args.label + "-" + label)
        print(f"PASS: live tier2 and {args.named_model} requests answered OK")
    else:
        tiers = models.resolve_tiers()
        primary = tiers["tier2"]["models"][0][1]
        backup = next(
            m
            for _, m, window in tiers["tier2"]["models"][1:]
            if window >= tiers["tier2"]["window"]
        )
        for scenario, requested in (
            ("tier", "claude-gw-tier2"),
            ("named", "claude-opus-5-5"),
            ("stream-error", "claude-gw-tier2"),
        ):
            gateway = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Gateway)
            gateway.scenario, gateway.primary = scenario, primary
            gateway.listing = list(
                dict.fromkeys(m for t in tiers.values() for _, m, _ in t["models"])
            )
            gateway.calls = []
            threading.Thread(target=gateway.serve_forever, daemon=True).start()
            try:
                with shim(
                    f"http://127.0.0.1:{gateway.server_port}/cli", scenario
                ) as base:
                    claude(base, requested, scenario)
                save(f"{scenario}-calls.json", gateway.calls)
                if scenario == "tier":
                    assert gateway.calls == [primary] * 3 + [backup], gateway.calls
                elif scenario == "named":
                    assert gateway.calls == ["claude-opus-5-5", "claude-sonnet-5-5"], (
                        gateway.calls
                    )
                else:
                    assert len(gateway.calls) >= 2 and set(gateway.calls) == {
                        primary
                    }, gateway.calls
                print(f"PASS: {scenario}: {gateway.calls}")
            finally:
                gateway.shutdown()
                gateway.server_close()
    with urllib.request.urlopen(
        "http://127.0.0.1:4078/__ccsession_shim", timeout=5
    ) as response:
        after = json.load(response)
    assert after["pid"] == shared["pid"], "Shared shim identity changed"
    save(
        "shared-shim-check.json",
        {
            "pid_before": shared["pid"],
            "pid_after": after["pid"],
            "port": after["port"],
            "untouched": True,
        },
    )


if __name__ == "__main__":
    main()
