"""Live check: does closing the terminal that launched a ccsession shim kill it?

Runs the REAL ccsession from the worktree (fake claude), routes a slow streamed
reply through the shim it starts, then does what Orca does when it closes a
terminal: SIGTERM, then SIGKILL, every process descended from the terminal's
root. Prints whether the stream finished and whether the port still answers.
Only processes this script started are signalled.
"""

import http.server
import json
import os
import signal
import socket
import subprocess
import sys
import threading
import time
import urllib.request
from pathlib import Path

WORKTREE = Path(sys.argv[1])
SCRATCH = Path(sys.argv[2])
SKILL = WORKTREE / "src/superclaude/skills/ccsession-tag"
PAUSE = 5.0


class Upstream(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"

    def log_message(self, *a):
        pass

    def do_GET(self):
        body = json.dumps({"data": [{"id": "claude-opus-5-5"}]}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        self.rfile.read(int(self.headers["Content-Length"]))
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.end_headers()
        self.wfile.write(b'event: message_start\ndata: {"type":"message_start"}\n\n')
        self.wfile.flush()
        time.sleep(PAUSE)  # a long turn: the model is still thinking
        self.wfile.write(b'event: message_stop\ndata: {"type":"message_stop"}\n\n')


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def descendants(root):
    rows = subprocess.run(
        ["ps", "-axo", "pid=,ppid="], capture_output=True, text=True, check=True
    ).stdout.split("\n")
    kids = {}
    for row in rows:
        parts = row.split()
        if len(parts) == 2:
            kids.setdefault(int(parts[1]), []).append(int(parts[0]))
    out, todo = [], [root]
    while todo:
        for child in kids.get(todo.pop(), []):
            out.append(child)
            todo.append(child)
    return out


def main():
    up = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Upstream)
    threading.Thread(target=up.serve_forever, daemon=True).start()
    port = free_port()
    shim_copy = SCRATCH / "shim-under-test.py"
    shim_copy.write_text((SKILL / "local-gateway-alias-proxy.py").read_text())
    home = SCRATCH / "home"
    home.mkdir(exist_ok=True)
    fake = SCRATCH / "bin" / "claude"
    fake.parent.mkdir(exist_ok=True)
    fake.write_text('#!/bin/sh\necho "$ANTHROPIC_BASE_URL" > "$SEEN_FILE"\nexec sleep 300\n')
    fake.chmod(0o755)
    seen = SCRATCH / "seen"
    seen.unlink(missing_ok=True)
    env = {k: v for k, v in os.environ.items() if not k.startswith(("CCSESSION", "CC_SHIM", "AIDEV_"))}
    env.update(
        HOME=str(home),
        CLAUDE_BIN=str(fake),
        ANTHROPIC_BASE_URL=f"http://127.0.0.1:{up.server_port}/cli",
        ANTHROPIC_API_KEY="test-key",
        CC_SHIM_SCRIPT=str(shim_copy),
        CC_SHIM_PORT=str(port),
        SEEN_FILE=str(seen),
        AIDEV_AI_DEFAULTS_PATH=str(SCRATCH / "no-defaults.sh"),
    )
    # The "terminal": its own session, like an Orca pty root.
    term = subprocess.Popen(
        [str(SKILL / "ccsession"), "--shim", "--claude-args"],
        cwd=SCRATCH,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    for _ in range(200):
        if seen.exists() and seen.read_text().strip():
            break
        time.sleep(0.1)
    base = seen.read_text().strip()
    health = json.loads(urllib.request.urlopen(base + "/__ccsession_shim", timeout=3).read())
    shim_pid = health["pid"]
    print(f"terminal root pid={term.pid} shim pid={shim_pid} base={base}")
    print(f"shim is a descendant of the terminal: {shim_pid in descendants(term.pid)}")

    result = {}

    def stream():
        req = urllib.request.Request(
            base + "/v1/messages",
            data=json.dumps({"model": "claude-opus-5-5", "stream": True}).encode(),
            headers={"Content-Type": "application/json", "x-api-key": "test-key"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result["body"] = resp.read()
        except Exception as exc:  # noqa: BLE001 - reported below
            result["error"] = repr(exc)

    t = threading.Thread(target=stream)
    t.start()
    time.sleep(1.5)  # the reply has started; the model is "thinking"
    # Orca closes the terminal: SIGTERM every descendant and the root, then SIGKILL.
    victims = descendants(term.pid) + [term.pid]
    for pid in victims:
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
    time.sleep(1.0)
    for pid in victims:
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    term.wait(5)
    t.join(30)
    body = result.get("body", b"")
    print(f"stream finished: {b'message_stop' in body} error={result.get('error')} bytes={len(body)}")
    try:
        h = json.loads(urllib.request.urlopen(base + "/__ccsession_shim", timeout=3).read())
        print(f"port after close: answers (pid {h['pid']})")
    except Exception as exc:  # noqa: BLE001
        print(f"port after close: {exc!r}")
    # Clean up the shim if it survived (exact pid only).
    try:
        os.kill(shim_pid, signal.SIGTERM)
        print(f"cleanup: stopped surviving shim pid {shim_pid}")
    except ProcessLookupError:
        print(f"cleanup: shim pid {shim_pid} already gone")
    up.shutdown()


if __name__ == "__main__":
    main()
