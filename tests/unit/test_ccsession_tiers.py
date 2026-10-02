"""Tier mode for ccsession: tier settings, launch selection, picker and failover.

Tier mode is the Coder-workspace behaviour (models and windows come from the
workspace env file); the Mac keeps profiles. These tests never touch the real
workspace env file, the network, or the model-data cache.
"""

from __future__ import annotations

import gzip
import http.server
import json
import os
import runpy
import socket
import stat
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "src" / "superclaude" / "skills" / "ccsession-tag"
sys.path.insert(0, str(SKILL_DIR))
import models  # noqa: E402

# The proposed Coder env block (spec 12.1), as it appears in defaults.sh.
TIER_BLOCK = """\
# AI defaults (non-secret)
export T0Model01_WINDOW_DOC=ignored
export T0_WINDOW=850000
export T0Model01=claude-fable-5-1
export T0Model01_WINDOW=1000000
export T0Model02=gpt-6-astra
export T0Model02_WINDOW=850000
export T1_WINDOW=850000
export T1Model01=claude-opus-5-5
export T1Model01_WINDOW=1000000
export T1Model02="gpt-6.1-sol"
export T1Model02_WINDOW=850000
export T1Model03=claude-sonnet-5-5
export T1Model03_WINDOW=1000000
export T2_WINDOW=500000
export T2Model01=muse-spark-1.3
export T2Model01_WINDOW=950000
export T2Model02=grok-4.7
export T2Model02_WINDOW=500000
export T2Model03='Qwen3.8-max'
export T2Model03_WINDOW=1000000
export T2Model04=glm-5.3
export T2Model04_WINDOW=1000000
export T3_WINDOW=850000
export T3Model01=gpt-6-luna
export T3Model01_WINDOW=850000
export CCSESSION_DEFAULT_TIER=tier2
export ANTHROPIC_MODEL="grok-4.6[1m]"
echo not-an-export
"""

# Today's Coder env (before the env change): tier models but no windows.
TODAY_BLOCK = """\
export T00Model01=gpt-6-astra
export T0Model01=gpt-6-sol
export T0Model02=claude-opus-5-5
export T1Model01=gpt-6-terra
export T2Model01=grok-4.7
export codex=gpt-codex
"""


@pytest.fixture(autouse=True)
def _isolated(monkeypatch, tmp_path_factory):
    """No network, private cache, and no tier settings unless a test adds them."""
    monkeypatch.setenv("CCSESSION_MODELS_REFRESH", "0")
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path_factory.mktemp("cache")))
    monkeypatch.setenv(
        "AIDEV_AI_DEFAULTS_PATH", "/nonexistent/ccsession-test/defaults.sh"
    )
    for name in list(os.environ):
        if name.startswith("T") and ("Model" in name or name.endswith("_WINDOW")):
            monkeypatch.delenv(name)
    for name in (
        "CCSESSION_DEFAULT_TIER",
        "CCSESSION_SHOW_ALL_MODELS",
        "CCSESSION_TIERS",
    ):
        monkeypatch.delenv(name, raising=False)


def _defaults(tmp_path: Path, text: str = TIER_BLOCK) -> Path:
    path = tmp_path / "aienv.d" / "defaults.sh"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


# --- tier settings (models.py) -------------------------------------------------


def test_defaults_file_is_parsed_not_sourced(tmp_path: Path) -> None:
    values = models.read_defaults_file(_defaults(tmp_path))
    assert values["T1Model02"] == "gpt-6.1-sol"  # double quotes dropped
    assert values["T2Model03"] == "Qwen3.8-max"  # single quotes dropped
    assert values["T2_WINDOW"] == "500000"
    assert values["CCSESSION_DEFAULT_TIER"] == "tier2"
    # Only tier settings are taken; other exports and commands are ignored.
    assert "ANTHROPIC_MODEL" not in values
    assert "T0Model01_WINDOW_DOC" not in values
    assert models.read_defaults_file(tmp_path / "missing.sh") == {}


def test_todays_coder_env_keeps_tier_mode_off(tmp_path: Path, monkeypatch) -> None:
    """Coder already sets T0Model01; only a tier window may switch tier mode on."""
    monkeypatch.setenv("AIDEV_AI_DEFAULTS_PATH", str(_defaults(tmp_path, TODAY_BLOCK)))
    assert not models.tier_mode()
    monkeypatch.setenv("AIDEV_AI_DEFAULTS_PATH", str(_defaults(tmp_path)))
    assert models.tier_mode()
    monkeypatch.setenv("CCSESSION_TIERS", "0")
    assert not models.tier_mode()


def test_defaults_file_wins_over_stale_shell_env(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("T2Model01", "old-model")
    monkeypatch.setenv("T2_WINDOW", "200000")
    assert models.tier_mode()  # env fallback when there is no file
    monkeypatch.setenv("AIDEV_AI_DEFAULTS_PATH", str(_defaults(tmp_path)))
    tiers = models.resolve_tiers()
    assert tiers["tier2"]["models"][0] == ("T2Model01", "muse-spark-1.3", 950000)
    assert tiers["tier2"]["window"] == 500000
    assert [m for _, m, _ in tiers["tier1"]["models"]] == [
        "claude-opus-5-5",
        "gpt-6.1-sol",
        "claude-sonnet-5-5",
    ]


def test_missing_tier_variable_is_named(tmp_path: Path, monkeypatch) -> None:
    text = TIER_BLOCK.replace("export T2Model03_WINDOW=1000000\n", "")
    monkeypatch.setenv("AIDEV_AI_DEFAULTS_PATH", str(_defaults(tmp_path, text)))
    with pytest.raises(ValueError, match="T2Model03_WINDOW"):
        models.resolve_tiers()
    text = TIER_BLOCK.replace("export T1_WINDOW=850000\n", "")
    monkeypatch.setenv("AIDEV_AI_DEFAULTS_PATH", str(_defaults(tmp_path, text)))
    with pytest.raises(ValueError, match="T1_WINDOW"):
        models.resolve_tiers()


def test_named_model_window_comes_from_its_tier_slot(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setenv("AIDEV_AI_DEFAULTS_PATH", str(_defaults(tmp_path)))
    assert models.model_window("gpt-6-astra") == (850000, "T0Model02")
    assert models.model_window("grok-4.7") == (500000, "T2Model02")
    assert models.model_window("some-new-model") == (200000, "not in any tier")
    data = json.loads(models.BUNDLED.read_text())
    data["picker"]["one_million_context"].append("big-new-model")
    assert models.model_window("big-new-model", data=data) == (
        models.ONE_MILLION,
        "not in any tier; 1M list",
    )


def test_version_order_is_numeric() -> None:
    assert models._version_key("2026-10-01.10") > models._version_key("2026-10-01.9")
    assert models._version_key("2026-10-02.1") > models._version_key("2026-10-01.99")


def test_load_prefers_numerically_newer_copy(tmp_path: Path, monkeypatch) -> None:
    bundled = json.loads(models.BUNDLED.read_text())
    cache = Path(os.environ["XDG_CACHE_HOME"]) / "ccsession"
    cache.mkdir(parents=True)
    newer = dict(bundled, version=bundled["version"].split(".")[0] + ".10")
    (cache / "models.json").write_text(json.dumps(newer))
    monkeypatch.setattr(models, "BUNDLED", tmp_path / "bundled.json")
    (tmp_path / "bundled.json").write_text(
        json.dumps(dict(bundled, version=bundled["version"].split(".")[0] + ".9"))
    )
    assert models.load()[0]["version"].endswith(".10")


def test_old_picker_keys_are_rejected() -> None:
    data = json.loads(models.BUNDLED.read_text())
    assert models.validate(data) == ""
    data["picker"]["remove"] = []
    assert "replaced by picker.show" in models.validate(data)
    data = json.loads(models.BUNDLED.read_text())
    data["tiers"]["tier9"] = {"models_env": ["ANTHROPIC_MODEL"]}
    assert "models_env" in models.validate(data)


def test_shim_port_separates_show_all_and_env_settings(
    tmp_path: Path, monkeypatch
) -> None:
    path = _defaults(tmp_path)
    monkeypatch.setenv("AIDEV_AI_DEFAULTS_PATH", str(path))
    # A file other than the standard one is a different setting.
    assert models.shim_port(4010) != 4010
    monkeypatch.setattr(models, "DEFAULTS_FILE", str(path))
    assert models.shim_port(4010) == 4010
    shared = models.settings_digest()
    monkeypatch.setenv("CCSESSION_SHOW_ALL_MODELS", "1")
    assert models.settings_digest() != shared
    show_all = models.shim_port(4010)
    assert 4011 <= show_all <= 4107
    monkeypatch.delenv("CCSESSION_SHOW_ALL_MODELS")
    monkeypatch.setenv("AIDEV_AI_DEFAULTS_PATH", str(tmp_path / "none.sh"))
    monkeypatch.setenv("T2_WINDOW", "500000")
    first = models.shim_port(4010)
    monkeypatch.setenv("T2_WINDOW", "400000")
    assert first != 4010 and models.shim_port(4010) != first


def test_refresh_never_replaces_a_newer_cache(tmp_path: Path, monkeypatch) -> None:
    """A CDN node still serving the previous file must not roll the cache back."""
    bundled = json.loads(models.BUNDLED.read_text())
    cache = Path(os.environ["XDG_CACHE_HOME"]) / "ccsession"
    cache.mkdir(parents=True)
    newer = dict(bundled, version="2099-01-01.2")
    (cache / "models.json").write_text(json.dumps(newer))
    older = json.dumps(dict(bundled, version="2099-01-01.1")).encode()

    class Old(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("ETag", '"old"')
            self.end_headers()
            self.wfile.write(older)

        def log_message(self, *args):
            pass

    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Old)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        result = {}
        models._fetch(f"http://127.0.0.1:{server.server_port}/m.json", result)
    finally:
        server.shutdown()
    assert result["status"] == "kept newer cached 2099-01-01.2"
    assert json.loads((cache / "models.json").read_text())["version"] == "2099-01-01.2"


# --- launch selection (ccsession) ---------------------------------------------


def _launch(
    tmp_path: Path, *args: str, defaults: str | None = TIER_BLOCK, **extra: str
):
    """Run ccsession with a fake claude and a fake running shim; return (rc, out, err, seen)."""
    home = tmp_path / "home"
    home.mkdir(exist_ok=True)
    fake_claude = tmp_path / "claude"
    fake_claude.write_text(
        """#!/usr/bin/env python3
import json, os, sys
json.dump({
    "argv": sys.argv[1:],
    "context": os.environ.get("CLAUDE_CODE_MAX_CONTEXT_TOKENS", ""),
    "compact": os.environ.get("CLAUDE_CODE_AUTO_COMPACT_WINDOW", ""),
    "custom": os.environ.get("ANTHROPIC_CUSTOM_MODEL_OPTION", ""),
    "base_url": os.environ.get("ANTHROPIC_BASE_URL", ""),
}, open(os.environ["SEEN_FILE"], "w"))
"""
    )
    fake_lsof = tmp_path / "lsof"
    fake_lsof.write_text("#!/bin/sh\nprintf '4242\\n'\n")
    fake_curl = tmp_path / "curl"
    # A running shim with this session's settings (digest from models.py).
    fake_curl.write_text(
        f"#!/bin/sh\nd=$(python3 {SKILL_DIR / 'models.py'} settings-digest)\n"
        'printf \'{"service":"ccsession-gateway-alias-proxy",'
        '"upstream":"http://gateway.example:4000/cli","port":4555,'
        '"model_data":"t","tiers":{},"show_all":false,"settings":"%s"}\' "$d"\n'
    )
    for f in (fake_claude, fake_lsof, fake_curl):
        f.chmod(f.stat().st_mode | stat.S_IXUSR)
    env = os.environ.copy()
    for inherited in (
        "CLAUDE_CODE_MAX_CONTEXT_TOKENS",
        "CLAUDE_CODE_AUTO_COMPACT_WINDOW",
    ):
        env.pop(
            inherited, None
        )  # set when the test runner itself runs inside Claude Code
    env.update(
        {
            "HOME": str(home),
            "CLAUDE_BIN": str(fake_claude),
            "PATH": f"{tmp_path}:{env['PATH']}",
            "ANTHROPIC_BASE_URL": "http://gateway.example:4000/cli",
            "CC_SHIM_PORT": "4555",
            "CC_SHIM_SCRIPT": str(SKILL_DIR / "local-gateway-alias-proxy.py"),
            "SEEN_FILE": str(tmp_path / "seen.json"),
            "AIDEV_AI_DEFAULTS_PATH": str(_defaults(tmp_path, defaults))
            if defaults is not None
            else str(tmp_path / "no-defaults.sh"),
        }
    )
    env.update(extra)
    (tmp_path / "seen.json").unlink(missing_ok=True)
    proc = subprocess.run(
        [str(SKILL_DIR / "ccsession"), *args],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    seen = (
        json.loads((tmp_path / "seen.json").read_text())
        if (tmp_path / "seen.json").exists()
        else None
    )
    return proc.returncode, proc.stdout, proc.stderr, seen


def _model_arg(seen: dict) -> str:
    argv = seen["argv"]
    return argv[argv.index("--model") + 1]


def test_default_tier_sets_model_and_tier_window(tmp_path: Path) -> None:
    rc, out, err, seen = _launch(tmp_path, "work")
    assert rc == 0, err
    assert _model_arg(seen) == "claude-gw-tier2[1m]"
    assert seen["context"] == seen["compact"] == "500000"
    assert seen["custom"] == ""  # tiers are already in the picker
    assert seen["base_url"] == "http://127.0.0.1:4555"  # shim is always on
    assert "tier2" in out and "muse-spark-1.3" in out


def test_tier_flag_and_named_model(tmp_path: Path) -> None:
    rc, _, err, seen = _launch(tmp_path, "work", "--tier", "tier0")
    assert rc == 0, err
    assert _model_arg(seen) == "claude-gw-tier0[1m]"
    assert seen["context"] == "850000"
    rc, _, err, seen = _launch(tmp_path, "work", "--tier", "1")
    assert rc == 0 and _model_arg(seen) == "claude-gw-tier1[1m]"
    rc, _, err, seen = _launch(tmp_path, "work", "--model", "gpt-6-astra")
    assert rc == 0, err
    assert _model_arg(seen) == "gpt-6-astra"
    assert seen["context"] == seen["compact"] == "850000"
    assert seen["custom"] == "gpt-6-astra"
    rc, _, err, seen = _launch(tmp_path, "work", "--model", "claude-opus-5-5")
    assert rc == 0 and _model_arg(seen) == "claude-opus-5-5[1m]"
    assert seen["context"] == "1000000"
    rc, _, err, seen = _launch(tmp_path, "work", "--model", "brand-new-model")
    assert rc == 0 and seen["context"] == "200000"
    assert "not in any tier" in err


def test_tier_mode_refuses_profiles_and_bad_tiers(tmp_path: Path) -> None:
    rc, _, err, seen = _launch(tmp_path, "work", "--profile", "gpt", "--shim")
    assert rc == 2 and seen is None
    assert "--tier" in err and "--model" in err
    rc, _, err, seen = _launch(tmp_path, "work", "--tier", "tier7")
    assert rc == 2 and seen is None and "tier7" in err
    broken = TIER_BLOCK.replace("export T2Model02_WINDOW=500000\n", "")
    rc, _, err, seen = _launch(tmp_path, "work", defaults=broken)
    assert rc == 2 and seen is None and "T2Model02_WINDOW" in err


def test_mac_and_todays_coder_env_keep_profiles(tmp_path: Path) -> None:
    for defaults in (None, TODAY_BLOCK):
        rc, out, err, seen = _launch(
            tmp_path, "work", "--profile", "gpt", "--shim", defaults=defaults
        )
        assert rc == 0, err
        assert _model_arg(seen) == "gpt-6.1-sol"
        assert seen["context"] == "850000"
        # Without tier mode --model is Claude Code's flag, passed through as given.
        rc, _, err, seen = _launch(
            tmp_path, "work", "--model", "sonnet", defaults=defaults
        )
        assert rc == 0, err
        assert _model_arg(seen) == "sonnet" and seen["context"] == ""
        rc, _, err, _ = _launch(tmp_path, "work", "--tier", "tier2", defaults=defaults)
        assert rc == 2 and "T<N>_WINDOW" in err


def test_help_lists_tiers_in_tier_mode(tmp_path: Path) -> None:
    rc, out, err, _ = _launch(tmp_path, "--help")
    assert rc == 0, err
    assert "* ccsession --tier tier2" in out
    assert "gpt-6-luna" in out and "--profile" in out  # usage text still mentions it
    rc, out, _, _ = _launch(tmp_path, "--help", defaults=None)
    assert "ccsession --profile gpt --shim" in out and "--tier tier" not in out


# --- picker and failover (shim) -------------------------------------------------

OK_SSE = (
    b'event: message_start\ndata: {"type":"message_start","message":{"model":"%s"}}\n\n'
    b'event: message_stop\ndata: {"type":"message_stop"}\n\n'
)
COOLING = (
    429,
    b'{"type":"error","error":{"type":"rate_limit_error","message":"All credentials for model x are cooling down"}}',
)
RATE_LIMITED = (
    429,
    b'{"type":"error","error":{"type":"rate_limit_error","message":"Rate limited"}}',
)
SERVER_ERROR = (
    500,
    b'{"type":"error","error":{"type":"api_error","message":"Internal server error"}}',
)
TOO_LONG = (
    400,
    b'{"type":"error","error":{"type":"invalid_request_error","message":"prompt is too long: 900000 tokens"}}',
)


class StandInGateway:
    """Scripted gateway: per model, a list of replies used in order (last repeats)."""

    def __init__(self):
        self.script: dict[str, list] = {}
        self.calls: list[tuple[str, dict]] = []
        gateway = self

        class Handler(http.server.BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.0"

            def log_message(self, *args):
                pass

            def do_GET(self):
                body = json.dumps(
                    {
                        "data": [
                            {"id": m}
                            for m in (
                                "claude-opus-5-5",
                                "gpt-6.1-sol",
                                "grok-4.7",
                                "kimi-k3",
                            )
                        ]
                    }
                ).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(body)

            def do_POST(self):
                req = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                gateway.calls.append((self.path, req))
                steps = gateway.script.get(req["model"], [])
                step = steps.pop(0) if len(steps) > 1 else (steps[0] if steps else None)
                if step and step[0] == "sleep":
                    time.sleep(step[1])
                    step = None
                if step and step[0] in ("pause-stream", "cut-stream"):
                    # Headers and the first event, then a pause; then either
                    # the rest (pause-stream) or a dropped connection.
                    self.send_response(200)
                    self.send_header("Content-Type", "text/event-stream")
                    self.end_headers()
                    first, rest = (OK_SSE % req["model"].encode()).split(b"\n\n", 1)
                    self.wfile.write(first + b"\n\n")
                    self.wfile.flush()
                    time.sleep(step[1])
                    if step[0] == "pause-stream":
                        self.wfile.write(rest)
                    return
                if step is None:
                    self.send_response(200)
                    self.send_header("Content-Type", "text/event-stream")
                    self.end_headers()
                    self.wfile.write(OK_SSE % req["model"].encode())
                    return
                status, body, *headers = step
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                for k, v in (headers[0] if headers else {}).items():
                    self.send_header(k, v)
                self.end_headers()
                self.wfile.write(body)

        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.server.server_port}/cli"

    def models_called(self):
        return [body["model"] for _, body in self.calls]

    def close(self):
        self.server.shutdown()
        self.server.server_close()


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture
def shim(tmp_path: Path):
    """Start the real shim against a stand-in gateway in tier mode."""
    gateway = StandInGateway()
    port = _free_port()
    procs = []

    def start(defaults: str = TIER_BLOCK, **extra: str):
        env = os.environ.copy()
        env.update(
            {
                "GW_PROXY_UPSTREAM": gateway.url,
                "GW_PROXY_PORT": str(port),
                "CCSESSION_DIR": str(SKILL_DIR),
                "AIDEV_AI_DEFAULTS_PATH": str(_defaults(tmp_path, defaults)),
                "CCSESSION_COOLDOWN_SECONDS": "3600",
                "CCSESSION_FIRST_BYTE_TIMEOUT": "2",
            }
        )
        env.update(extra)
        proc = subprocess.Popen(
            [sys.executable, str(SKILL_DIR / "local-gateway-alias-proxy.py")],
            env=env,
            stderr=open(tmp_path / "shim.log", "w"),
        )
        procs.append(proc)
        for _ in range(50):
            try:
                urllib.request.urlopen(
                    f"http://127.0.0.1:{port}/__ccsession_shim", timeout=1
                )
                break
            except OSError:
                time.sleep(0.1)
        return f"http://127.0.0.1:{port}"

    yield gateway, start, tmp_path / "shim.log"
    for proc in procs:
        proc.terminate()
        proc.wait(timeout=5)
    gateway.close()


def _ask(base: str, model: str, extra: dict | None = None):
    body = {
        "model": model,
        "max_tokens": 10,
        "stream": True,
        "messages": [{"role": "user", "content": "hi"}],
    }
    body.update(extra or {})
    req = urllib.request.Request(
        f"{base}/v1/messages",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-api-key": "test"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


def test_picker_shows_tiers_and_show_all_adds_env_models(shim) -> None:
    gateway, start, _ = shim
    base = start()
    listing = json.loads(urllib.request.urlopen(f"{base}/v1/models", timeout=5).read())[
        "data"
    ]
    ids = [m["id"] for m in listing]
    assert ids == [f"claude-gw-tier{n}[1m]" for n in range(4)]
    assert "Muse Spark 1.3" in listing[2]["display_name"]
    health = json.loads(
        urllib.request.urlopen(f"{base}/__ccsession_shim", timeout=5).read()
    )
    assert health["tier_mode"] is True and health["show_all"] is False
    assert health["tiers"]["tier1"] == [
        "claude-opus-5-5",
        "gpt-6.1-sol",
        "claude-sonnet-5-5",
    ]


def test_show_all_lists_every_tier_model_with_env_windows(shim) -> None:
    gateway, start, _ = shim
    base = start(CCSESSION_SHOW_ALL_MODELS="1")
    ids = [
        m["id"]
        for m in json.loads(
            urllib.request.urlopen(f"{base}/v1/models", timeout=5).read()
        )["data"]
    ]
    assert ids[:4] == [f"claude-gw-tier{n}[1m]" for n in range(4)]
    assert ids[4:] == [
        "claude-fable-5-1[1m]",
        "claude-gw-gpt-6-astra[1m]",
        "claude-opus-5-5[1m]",
        "claude-gw-gpt-6.1-sol[1m]",
        "claude-sonnet-5-5[1m]",
        "claude-gw-muse-spark-1.3[1m]",
        "claude-gw-grok-4.7[1m]",
        "claude-gw-qwen3.8-max[1m]",
        "claude-gw-glm-5.3[1m]",
        "claude-gw-gpt-6-luna[1m]",
    ]
    # A model listed only by show-all, and a hidden gateway model, both route.
    status, _ = _ask(base, "claude-gw-glm-5.3")
    status2, _ = _ask(base, "claude-gw-kimi-k3")
    assert status == status2 == 200
    assert gateway.models_called() == ["glm-5.3", "kimi-k3"]


def test_out_of_usage_switches_and_cools_down(shim) -> None:
    gateway, start, log = shim
    base = start()
    gateway.script["muse-spark-1.3"] = [COOLING]
    thinking = {
        "messages": [
            {"role": "user", "content": "hi"},
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "thinking",
                        "thinking": "x",
                        "signature": "sig-from-claude",
                    },
                    {
                        "type": "tool_use",
                        "id": "t1",
                        "name": "Read",
                        "input": {"path": "a"},
                    },
                ],
            },
            {
                "role": "user",
                "content": [
                    {"type": "tool_result", "tool_use_id": "t1", "content": "ok"}
                ],
            },
        ]
    }
    status, body = _ask(base, "claude-gw-tier2", thinking)
    assert status == 200 and b"grok-4.7" in body
    assert gateway.models_called() == ["muse-spark-1.3", "grok-4.7"]
    # The backup gets the same conversation; only the model name changes.
    first, second = gateway.calls[0][1], gateway.calls[1][1]
    assert {**first, "model": "x"} == {**second, "model": "x"}
    # Cooling down: the next request skips Muse without asking the gateway.
    status, _ = _ask(base, "claude-gw-tier2")
    assert status == 200 and gateway.models_called()[-1] == "grok-4.7"
    assert gateway.models_called().count("muse-spark-1.3") == 1
    assert (
        "T2Model01 muse-spark-1.3 -> next model (429 all accounts out of usage)"
        in log.read_text()
    )


@pytest.mark.parametrize(
    "reply",
    [
        COOLING,
        (429, b"You exceed your account's rate limit"),
        (429, b'{"error":{"type":"usage_limit_reached"}}'),
        (503, b'{"error":{"message":"auth_unavailable: no account"}}'),
        (402, b"payment required"),
        (400, b'{"error":{"type":"billing_error"}}'),
        (403, b"weekly usage limit reached"),
        (529, b"busy"),
        (500, b'{"error":{"type":"overloaded_error","message":"Overloaded"}}'),
        (400, b"unknown provider for model muse-spark-1.3"),
        (502, b"unknown provider for model muse-spark-1.3"),
        (404, b'{"error":{"type":"not_found_error"}}'),
        (401, b"Incorrect API key provided"),
        (426, b'{"error":"Your Grok CLI version (0.2.120) is outdated."}'),
    ],
)
def test_every_switch_rule_moves_to_the_next_model(shim, reply) -> None:
    gateway, start, _ = shim
    base = start()
    gateway.script["muse-spark-1.3"] = [reply]
    status, _ = _ask(base, "claude-gw-tier2")
    assert status == 200
    assert gateway.models_called() == ["muse-spark-1.3", "grok-4.7"]


@pytest.mark.parametrize(
    "reply",
    [
        RATE_LIMITED,
        SERVER_ERROR,
        TOO_LONG,
        (400, b'{"error":{"message":"context_management is not supported"}}'),
    ],
)
def test_errors_outside_the_rules_pass_back_unchanged(shim, reply) -> None:
    gateway, start, _ = shim
    base = start()
    gateway.script["muse-spark-1.3"] = [reply]
    status, body = _ask(base, "claude-gw-tier2")
    assert (status, body) == reply
    assert gateway.models_called() == ["muse-spark-1.3"]


def test_backup_too_small_for_the_tier_is_never_used(shim) -> None:
    gateway, start, _ = shim
    # Tier 0 window 850000: shrink Astra's own window below it.
    base = start(
        TIER_BLOCK.replace("T0Model02_WINDOW=850000", "T0Model02_WINDOW=400000")
    )
    gateway.script["claude-fable-5-1"] = [COOLING]
    status, body = _ask(base, "claude-gw-tier0")
    assert status == 429 and b"all Tier 0 models are out of usage" in body
    assert gateway.models_called() == ["claude-fable-5-1"]


def test_backup_rejecting_size_tries_the_next_one(shim) -> None:
    gateway, start, _ = shim
    base = start()
    gateway.script["muse-spark-1.3"] = [COOLING]
    gateway.script["grok-4.7"] = [TOO_LONG]
    status, body = _ask(base, "claude-gw-tier2")
    assert status == 200 and b"Qwen3.8-max" in body
    assert gateway.models_called() == ["muse-spark-1.3", "grok-4.7", "Qwen3.8-max"]
    # Muse is now cooling, so Grok is the first model tried. Too large is not
    # out of usage (Grok is not cooling) and the next backup still answers.
    status, body = _ask(base, "claude-gw-tier2")
    assert status == 200 and b"Qwen3.8-max" in body
    assert gateway.models_called()[3:] == ["grok-4.7", "Qwen3.8-max"]


def test_no_backup_can_hold_it_passes_the_error_back(shim) -> None:
    gateway, start, _ = shim
    base = start()
    gateway.script["muse-spark-1.3"] = [COOLING]
    for m in ("grok-4.7", "Qwen3.8-max", "glm-5.3"):
        gateway.script[m] = [TOO_LONG]
    status, body = _ask(base, "claude-gw-tier2")
    assert status == 400
    message = json.loads(body)["error"]["message"]
    assert "prompt is too long" in message and "can hold this conversation" in message
    assert "out of usage" not in message


def test_all_models_out_returns_last_error_with_note(shim) -> None:
    gateway, start, _ = shim
    base = start()
    for m in ("muse-spark-1.3", "grok-4.7", "Qwen3.8-max", "glm-5.3"):
        gateway.script[m] = [COOLING]
    status, body = _ask(base, "claude-gw-tier2")
    assert status == 429
    message = json.loads(body)["error"]["message"]
    assert (
        "cooling down" in message
        and "all Tier 2 models are out of usage; next retry at" in message
    )
    calls = len(gateway.calls)
    status, body = _ask(base, "claude-gw-tier2")  # everything cooling: nothing sent
    assert status == 429 and len(gateway.calls) == calls
    assert json.loads(body)["error"]["type"] == "rate_limit_error"


def test_cooldown_expires_and_repeats(shim) -> None:
    gateway, start, _ = shim
    base = start(CCSESSION_COOLDOWN_SECONDS="1")
    gateway.script["muse-spark-1.3"] = [COOLING, COOLING, ("ok",)]
    gateway.script["muse-spark-1.3"][-1] = None  # third try succeeds
    _ask(base, "claude-gw-tier2")
    time.sleep(1.2)
    _ask(base, "claude-gw-tier2")  # retried once, still out: cools again
    _ask(base, "claude-gw-tier2")  # within the new cooldown: skipped
    time.sleep(1.2)
    status, body = _ask(base, "claude-gw-tier2")  # back in use
    assert status == 200 and b"muse-spark-1.3" in body
    assert gateway.models_called().count("muse-spark-1.3") == 3


def test_retry_after_sets_the_cooldown(shim) -> None:
    gateway, start, _ = shim
    base = start()  # default cooldown is an hour
    gateway.script["muse-spark-1.3"] = [(*COOLING, {"Retry-After": "1"}), None]
    _ask(base, "claude-gw-tier2")
    time.sleep(1.2)
    status, body = _ask(base, "claude-gw-tier2")
    assert status == 200 and b"muse-spark-1.3" in body


def test_no_reply_before_timeout_switches(shim) -> None:
    gateway, start, log = shim
    base = start(CCSESSION_FIRST_BYTE_TIMEOUT="1")
    gateway.script["muse-spark-1.3"] = [("sleep", 3)]
    status, body = _ask(base, "claude-gw-tier2")
    assert status == 200 and b"grok-4.7" in body
    assert "gave no reply in 1s" in log.read_text()


def test_unreachable_gateway_is_not_a_switch(shim, tmp_path) -> None:
    gateway, start, _ = shim
    base = start(GW_PROXY_UPSTREAM=f"http://127.0.0.1:{_free_port()}/cli")
    status, body = _ask(base, "claude-gw-tier2")
    assert status == 502 and b"gateway unreachable" in body


def test_named_model_has_no_failover(shim) -> None:
    gateway, start, _ = shim
    base = start()
    gateway.script["gpt-6.1-sol"] = [COOLING]
    status, _ = _ask(base, "gpt-6.1-sol")
    assert status == 429 and gateway.models_called() == ["gpt-6.1-sol"]


def test_changed_env_file_applies_to_a_running_shim(shim, tmp_path) -> None:
    gateway, start, _ = shim
    base = start()
    _defaults(
        tmp_path, TIER_BLOCK.replace("T2Model01=muse-spark-1.3", "T2Model01=glm-5.3")
    )
    _ask(base, "claude-gw-tier2")
    assert gateway.models_called() == ["glm-5.3"]


def test_long_pause_after_a_reply_starts_is_not_cut(shim) -> None:
    """The first-byte limit applies only until the reply starts (QA F2)."""
    gateway, start, _ = shim
    base = start(CCSESSION_FIRST_BYTE_TIMEOUT="1")
    gateway.script["muse-spark-1.3"] = [("pause-stream", 2.5)]
    status, body = _ask(base, "claude-gw-tier2")
    assert status == 200 and b"message_stop" in body
    assert gateway.models_called() == ["muse-spark-1.3"]


def test_failure_after_the_reply_starts_passes_through(shim) -> None:
    gateway, start, _ = shim
    base = start()
    gateway.script["muse-spark-1.3"] = [("cut-stream", 0.2)]
    status, body = _ask(base, "claude-gw-tier2")
    assert status == 200 and b"message_start" in body and b"message_stop" not in body
    assert gateway.models_called() == ["muse-spark-1.3"]  # no switch mid-stream


def test_connect_timeout_is_unreachable_not_a_switch(shim) -> None:
    """A gateway that cannot be reached must not cool down every model (QA F1)."""
    gateway, start, log = shim
    # 192.0.2.1 is TEST-NET-1: connection attempts hang until the timeout.
    base = start(
        GW_PROXY_UPSTREAM="http://192.0.2.1:9/cli", _CCSESSION_TEST_CONNECT_TIMEOUT="1"
    )
    for _ in range(2):
        status, body = _ask(base, "claude-gw-tier2")
        assert status == 502 and b"gateway unreachable" in body
    assert "cooling down" not in log.read_text()


def test_cooldown_with_an_injected_clock() -> None:
    module = runpy.run_path(
        str(SKILL_DIR / "local-gateway-alias-proxy.py"), run_name="clock_test"
    )

    class Clock:
        now = 1000.0

        def time(self):
            return self.now

    clock = Clock()
    module["cool_down"].__globals__["time"] = clock
    module["cool_down"]("m1")
    assert module["cooling_until"]("m1") == 1000.0 + module["COOLDOWN_SECONDS"]
    clock.now += module["COOLDOWN_SECONDS"] - 1
    assert module["cooling_until"]("m1")
    clock.now += 2
    assert not module["cooling_until"]("m1")
    module["cool_down"]("m1", retry_after=30)
    clock.now += 31
    assert not module["cooling_until"]("m1")


def test_compact_overrides_still_apply_in_tier_mode(tmp_path: Path) -> None:
    rc, _, err, seen = _launch(tmp_path, "work", CCSESSION_COMPACT_WINDOW="300000")
    assert rc == 0, err
    assert seen["context"] == "500000" and seen["compact"] == "300000"


def test_addon_profile_on_a_tier_machine_skips_tier_mode(tmp_path: Path) -> None:
    profiles = tmp_path / "home" / ".config" / "ccsession" / "profiles.d"
    profiles.mkdir(parents=True)
    addon = profiles / "mine.sh"
    addon.write_text(
        'ccsession_profile_mine() { PROFILE_MODEL="addon-model"; PROFILE_CONTEXT=123456;'
        " PROFILE_COMPACT_WINDOW=123456; PROFILE_REQUIRES_SHIM=0; }\n"
    )
    addon.chmod(0o600)
    rc, _, err, seen = _launch(tmp_path, "work", "--profile", "mine")
    assert rc == 0, err
    assert _model_arg(seen) == "addon-model" and seen["context"] == "123456"
    assert seen["base_url"] == "http://gateway.example:4000/cli"  # no tier shim


def test_model_with_1m_suffix_finds_its_tier_window(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setenv("AIDEV_AI_DEFAULTS_PATH", str(_defaults(tmp_path)))
    assert models.model_window("claude-opus-5-5[1m]") == (1000000, "T1Model01")


def test_show_all_launch_runs_its_own_shim(tmp_path: Path) -> None:
    """Through the real script and a real shim: show-all gets another port."""
    home = tmp_path / "home"
    home.mkdir()
    fake_claude = tmp_path / "bin" / "claude"
    fake_claude.parent.mkdir()
    fake_claude.write_text('#!/bin/sh\necho "$ANTHROPIC_BASE_URL" > "$SEEN_FILE"\n')
    fake_claude.chmod(0o755)
    path = _defaults(tmp_path)
    shim_copy = tmp_path / "shim-under-test.py"
    shim_copy.write_text((SKILL_DIR / "local-gateway-alias-proxy.py").read_text())
    env = os.environ.copy()
    for k in ("CC_SHIM_PORT",):
        env.pop(k, None)
    env.update(
        HOME=str(home),
        CLAUDE_BIN=str(fake_claude),
        ANTHROPIC_BASE_URL="http://127.0.0.1:9/cli",
        # A private copy, so cleanup can find exactly this shim (the Coder
        # image has no lsof).
        CC_SHIM_SCRIPT=str(shim_copy),
        CCSESSION_DIR=str(SKILL_DIR),
        SEEN_FILE=str(tmp_path / "seen"),
        AIDEV_AI_DEFAULTS_PATH=str(path),
        CCSESSION_SHOW_ALL_MODELS="1",
    )
    expected = subprocess.run(
        [sys.executable, str(SKILL_DIR / "models.py"), "shim-port", "4010"],
        env=env,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    assert expected != "4010"
    with socket.socket() as probe:
        if probe.connect_ex(("127.0.0.1", int(expected))) == 0:
            pytest.skip(f"port {expected} is in use by a real shim on this machine")
    try:
        proc = subprocess.run(
            [str(SKILL_DIR / "ccsession"), "work"],
            cwd=tmp_path,
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert proc.returncode == 0, proc.stderr
        assert (tmp_path / "seen").read_text().strip() == f"http://127.0.0.1:{expected}"
        health = json.loads(
            urllib.request.urlopen(
                f"http://127.0.0.1:{expected}/__ccsession_shim", timeout=5
            ).read()
        )
        assert health["show_all"] is True and health["port"] == int(expected)
    finally:
        subprocess.run(["pkill", "-f", str(shim_copy)], check=False)


def _ask_raw(base: str, model: str, stream: bool, timeout: float = 120):
    body = {
        "model": model,
        "max_tokens": 10,
        "stream": stream,
        "messages": [{"role": "user", "content": "hi"}],
    }
    req = urllib.request.Request(
        f"{base}/v1/messages",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-api-key": "test"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.read()


@pytest.mark.parametrize(
    "model", ["claude-gw-tier2", "claude-gw-kimi-k3", "gpt-6.1-sol"]
)
def test_no_time_limit_once_a_reply_starts(shim, model) -> None:
    """Silence mid-reply, longer than every shim timer, never cuts the reply.

    Covers the tier path and the plain forwarding path (aliased and real
    names). Timers are shrunk to 1s; the gateway goes quiet for 8s.
    """
    gateway, start, _ = shim
    base = start(CCSESSION_FIRST_BYTE_TIMEOUT="1", _CCSESSION_TEST_CONNECT_TIMEOUT="1")
    for m in ("muse-spark-1.3", "kimi-k3", "gpt-6.1-sol"):
        gateway.script[m] = [("pause-stream", 8)]
    status, body = _ask_raw(base, model, stream=True)
    assert status == 200 and b"message_stop" in body
    assert len(gateway.calls) == 1


def test_non_streamed_tier_request_waits_without_limit(shim) -> None:
    """A non-streamed request only answers when done; never treated as stalled."""
    gateway, start, log = shim
    base = start(CCSESSION_FIRST_BYTE_TIMEOUT="1")
    gateway.script["muse-spark-1.3"] = [("sleep", 4)]
    status, body = _ask_raw(base, "claude-gw-tier2", stream=False)
    assert status == 200
    assert gateway.models_called() == ["muse-spark-1.3"]
    assert "gave no reply" not in log.read_text()


# --- round 2 review findings ------------------------------------------------


class ChunkedGateway:
    """HTTP/1.1 chunked stand-in: one small event, a pause, then the rest."""

    def __init__(self, pause: float):
        self.first_seen = None

        class Handler(http.server.BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, *args):
                pass

            def do_POST(self):
                self.rfile.read(int(self.headers["Content-Length"]))
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Transfer-Encoding", "chunked")
                self.end_headers()

                def chunk(data: bytes):
                    self.wfile.write(b"%x\r\n%s\r\n" % (len(data), data))
                    self.wfile.flush()

                chunk(b'event: ping\ndata: {"type":"ping"}\n\n')
                time.sleep(pause)
                chunk(b'event: message_stop\ndata: {"type":"message_stop"}\n\n')
                self.wfile.write(b"0\r\n\r\n")

        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.server.server_port}/cli"

    def close(self):
        self.server.shutdown()
        self.server.server_close()


@pytest.mark.parametrize("model", ["claude-gw-tier2", "gpt-6.1-sol"])
def test_small_streamed_events_are_passed_on_at_once(shim, model) -> None:
    """A lone keep-alive or thinking event must not wait for 8 KB (round 2 C2)."""
    _, start, _ = shim
    gateway = ChunkedGateway(pause=4)
    try:
        base = start(GW_PROXY_UPSTREAM=gateway.url)
        body = json.dumps(
            {
                "model": model,
                "max_tokens": 5,
                "stream": True,
                "messages": [{"role": "user", "content": "hi"}],
            }
        ).encode()
        req = urllib.request.Request(
            f"{base}/v1/messages",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=30) as resp:
            first = resp.fp.read1(4096) if hasattr(resp.fp, "read1") else resp.read(10)
            first_at = time.time() - t0
            rest = resp.read()
        assert b"ping" in first and first_at < 2, (first, first_at)
        assert b"message_stop" in rest
    finally:
        gateway.close()


class GzipGateway:
    """Compresses error bodies when the client accepts gzip (like real servers)."""

    def __init__(self):
        gateway = self
        self.calls = []

        class Handler(http.server.BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.0"

            def log_message(self, *args):
                pass

            def do_POST(self):
                req = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                gateway.calls.append(
                    (req["model"], self.headers.get_all("Accept-Encoding"))
                )
                if req["model"] == "muse-spark-1.3":
                    body = COOLING[1]
                    if "gzip" in (self.headers.get("Accept-Encoding") or ""):
                        body = gzip.compress(body)
                        self.send_response(429)
                        self.send_header("Content-Encoding", "gzip")
                    else:
                        self.send_response(429)
                    self.end_headers()
                    self.wfile.write(body)
                    return
                self.send_response(200)
                self.end_headers()
                self.wfile.write(OK_SSE % req["model"].encode())

        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.server.server_port}/cli"

    def close(self):
        self.server.shutdown()
        self.server.server_close()


def test_lowercase_accept_encoding_still_fails_over(shim) -> None:
    """Round 2 H2: a client header `accept-encoding: gzip` must not disable failover."""
    _, start, _ = shim
    gateway = GzipGateway()
    try:
        base = start(GW_PROXY_UPSTREAM=gateway.url)
        conn = __import__("http.client").client.HTTPConnection(
            "127.0.0.1", int(base.rsplit(":", 1)[1])
        )
        body = json.dumps(
            {
                "model": "claude-gw-tier2",
                "max_tokens": 5,
                "stream": True,
                "messages": [{"role": "user", "content": "hi"}],
            }
        )
        conn.putrequest("POST", "/v1/messages", skip_accept_encoding=True)
        conn.putheader("content-type", "application/json")
        conn.putheader("accept-encoding", "gzip, br")
        conn.putheader("content-length", str(len(body)))
        conn.endheaders(body.encode())
        resp = conn.getresponse()
        data = resp.read()
        assert resp.status == 200 and b"grok-4.7" in data
        assert [m for m, _ in gateway.calls] == ["muse-spark-1.3", "grok-4.7"]
        assert all(enc == ["identity"] for _, enc in gateway.calls)
    finally:
        gateway.close()


def test_plain_body_decodes_a_compressed_error() -> None:
    module = runpy.run_path(
        str(SKILL_DIR / "local-gateway-alias-proxy.py"), run_name="gz_test"
    )
    raw, headers = module["plain_body"](
        {"Content-Encoding": "gzip", "X": "1"}, gzip.compress(b"cooling")
    )
    assert (
        raw == b"cooling" and "Content-Encoding" not in headers and headers["X"] == "1"
    )


def test_headers_slow_after_the_first_byte_are_not_a_stall(shim, tmp_path) -> None:
    """Round 2 M1: once the gateway sends its first byte, nothing is timed."""
    _, start, log = shim
    srv = socket.socket()
    srv.bind(("127.0.0.1", 0))
    srv.listen(1)
    calls = []

    def serve():
        conn, _ = srv.accept()
        data = b""
        while b"\r\n\r\n" not in data:
            data += conn.recv(65536)
        head, _, body = data.partition(b"\r\n\r\n")
        length = int(
            [h for h in head.split(b"\r\n") if h.lower().startswith(b"content-length")][
                0
            ].split(b":")[1]
        )
        while len(body) < length:
            body += conn.recv(65536)
        calls.append(json.loads(body)["model"])
        conn.sendall(b"HTTP/1.0 200 OK\r\n")
        time.sleep(3)  # longer than the 1s start-of-reply limit
        conn.sendall(
            b"Content-Type: text/event-stream\r\n\r\n" + OK_SSE % b"muse-spark-1.3"
        )
        conn.close()

    threading.Thread(target=serve, daemon=True).start()
    try:
        base = start(
            GW_PROXY_UPSTREAM=f"http://127.0.0.1:{srv.getsockname()[1]}/cli",
            CCSESSION_FIRST_BYTE_TIMEOUT="1",
        )
        status, body = _ask_raw(base, "claude-gw-tier2", stream=True)
        assert status == 200 and b"message_stop" in body
        assert calls == ["muse-spark-1.3"] and "gave no reply" not in log.read_text()
    finally:
        srv.close()


def test_huge_retry_after_is_capped() -> None:
    module = runpy.run_path(
        str(SKILL_DIR / "local-gateway-alias-proxy.py"), run_name="ra_test"
    )
    assert module["retry_after_seconds"]("99999999999999") == module["MAX_COOLDOWN"]
    until = module["cool_down"]("m", module["retry_after_seconds"]("99999999999999"))
    assert module["clock"](until)  # formats without error


def test_default_tier_unset_or_invalid_is_reported(tmp_path: Path) -> None:
    text = TIER_BLOCK.replace("export CCSESSION_DEFAULT_TIER=tier2\n", "")
    rc, _, err, seen = _launch(tmp_path, "work", defaults=text)
    assert rc == 0 and "CCSESSION_DEFAULT_TIER is not set" in err
    assert _model_arg(seen) == "claude-gw-tier2[1m]"
    bad = TIER_BLOCK.replace(
        "CCSESSION_DEFAULT_TIER=tier2", "CCSESSION_DEFAULT_TIER=fast"
    )
    rc, _, err, seen = _launch(tmp_path, "work", defaults=bad)
    assert rc == 2 and seen is None and "CCSESSION_DEFAULT_TIER" in err


def test_settings_that_change_the_shim_get_their_own_shim(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.setenv("AIDEV_AI_DEFAULTS_PATH", str(_defaults(tmp_path)))
    monkeypatch.setattr(
        models, "DEFAULTS_FILE", str(tmp_path / "aienv.d" / "defaults.sh")
    )
    shared = models.settings_digest()
    for name, value in (
        ("CCSESSION_TIERS", "0"),
        ("CCSESSION_COOLDOWN_SECONDS", "60"),
        ("CCSESSION_FIRST_BYTE_TIMEOUT", "30"),
    ):
        monkeypatch.setenv(name, value)
        assert models.settings_digest() != shared, name
        assert models.shim_port(4010) != 4010, name
        monkeypatch.delenv(name)
    assert models.settings_digest() == shared


def _real_launch(tmp_path: Path, port: int, **extra: str):
    """Launch the real script (fake claude) so it starts or reuses real shims."""
    fake = tmp_path / "bin" / "claude"
    fake.parent.mkdir(exist_ok=True)
    fake.write_text('#!/bin/sh\necho "$ANTHROPIC_BASE_URL" > "$SEEN_FILE"\n')
    fake.chmod(0o755)
    env = os.environ.copy()
    env.update(
        HOME=str(tmp_path / "home"),
        CLAUDE_BIN=str(fake),
        ANTHROPIC_BASE_URL=extra.pop("upstream"),
        CC_SHIM_PORT=str(port),
        CC_SHIM_SCRIPT=str(tmp_path / "shim-under-test.py"),
        SEEN_FILE=str(tmp_path / "seen"),
        AIDEV_AI_DEFAULTS_PATH=str(_defaults(tmp_path)),
    )
    env.update(extra)
    (tmp_path / "home").mkdir(exist_ok=True)
    proc = subprocess.run(
        [str(SKILL_DIR / "ccsession"), "work"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, proc.stderr
    return proc.stdout, (tmp_path / "seen").read_text().strip()


def test_a_busy_shim_is_never_stopped_by_a_new_launch(tmp_path: Path) -> None:
    """Round 2 C1: a launch with other settings must not cut other sessions' replies."""
    (tmp_path / "shim-under-test.py").write_text(
        (SKILL_DIR / "local-gateway-alias-proxy.py").read_text()
    )
    gateway = StandInGateway()
    gateway.script["muse-spark-1.3"] = [("pause-stream", 6)]
    port = _free_port()
    try:
        out, url = _real_launch(tmp_path, port, upstream=gateway.url)
        assert url == f"http://127.0.0.1:{port}"
        result = {}
        streaming = threading.Thread(
            target=lambda: result.update(
                r=_ask_raw(url, "claude-gw-tier2", stream=True)
            )
        )
        streaming.start()
        time.sleep(1)  # the reply has started and is paused
        out, url2 = _real_launch(
            tmp_path, port, upstream=gateway.url, CCSESSION_SHOW_ALL_MODELS="1"
        )
        assert url2 == f"http://127.0.0.1:{port + 101}", out
        assert "leaving it running" in out
        streaming.join(30)
        status, body = result["r"]
        assert status == 200 and b"message_stop" in body  # never cut
        # Now idle: the next launch with other settings may replace it.
        out, url3 = _real_launch(
            tmp_path, port, upstream=gateway.url, CCSESSION_COOLDOWN_SECONDS="60"
        )
        assert url3 == f"http://127.0.0.1:{port}" and "Replacing idle" in out
    finally:
        subprocess.run(
            ["pkill", "-f", str(tmp_path / "shim-under-test.py")], check=False
        )
        gateway.close()
