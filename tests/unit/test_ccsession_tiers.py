"""Tier mode for ccsession: tier settings, launch selection, picker and failover.

Tier mode is the Coder-workspace behaviour (models and windows come from the
workspace env file); the Mac keeps profiles. These tests never touch the real
workspace env file, the network, or the model-data cache.
"""

from __future__ import annotations

import http.server
import json
import os
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
    monkeypatch.setenv("AIDEV_AI_DEFAULTS_PATH", str(_defaults(tmp_path)))
    assert models.shim_port(4010) == 4010
    monkeypatch.setenv("CCSESSION_SHOW_ALL_MODELS", "1")
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
    fake_curl.write_text(
        '#!/bin/sh\nprintf \'{"service":"ccsession-gateway-alias-proxy",'
        '"upstream":"http://gateway.example:4000/cli","port":4555,'
        '"model_data":"t","tiers":{},"show_all":false}\'\n'
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
    # Too large is not out of usage: Grok is not cooling down.
    gateway.script["muse-spark-1.3"] = [COOLING]
    _ask(base, "claude-gw-tier2")
    assert gateway.models_called()[-1] == "grok-4.7"


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
