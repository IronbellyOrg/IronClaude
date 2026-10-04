#!/usr/bin/env python3
"""
Local, zero-dependency name-alias proxy for Claude Code gateway model discovery.

WHY: Claude Code's model picker only shows gateway models whose id starts with
"claude" or "anthropic" (hardcoded client-side filter). The CPA gateway behind
LiteLLM's /cli passthrough serves ~58 non-claude models (gpt-*, grok-*, kimi-*,
qwen-*, glm-*, ...) that therefore never appear.

WHAT: This proxy sits between Claude Code and the upstream /cli base. It:
  - GET /v1/models   -> fetches upstream, rewrites each NON-claude id to a
                        claude-prefixed alias (claude-gw-<sanitized>), returns it.
  - POST /v1/messages (and anything else) -> if the request body names an alias,
                        swaps it back to the real id, then transparently forwards
                        (streaming) to upstream. Real claude models pass untouched.

Tier mode (Coder workspaces, see models.py): the picker shows tiers
(claude-gw-tier0 ...). A request for a tier goes to the tier's first model that
is not cooling down; when the gateway answers with an out-of-usage style error
(SWITCH_RULES) before any reply is streamed, the same request is resent to the
next model in the tier and the failed one cools down for an hour.

It changes NOTHING upstream. Point Claude Code at it:
  export ANTHROPIC_BASE_URL=http://127.0.0.1:4010
  export ANTHROPIC_AUTH_TOKEN=<your litellm key>
  export CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1
  rm -f ~/.claude/cache/gateway-models.json   # force a fresh discovery
"""

import datetime
import email.utils
import gzip
import http.client
import http.server
import json
import os
import re
import socket
import socketserver
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import zlib

# LiteLLM /cli passthrough base. This default is a placeholder: set your real
# gateway in ~/.claude/ccsession.env as ANTHROPIC_BASE_URL, which ccsession
# passes in as GW_PROXY_UPSTREAM. The URL must end in /cli.
UPSTREAM = os.environ.get("GW_PROXY_UPSTREAM", "http://127.0.0.1:4000/cli").rstrip("/")


def listen_port():
    """Read and validate the port passed by the ccsession wrapper."""
    raw = os.environ.get("GW_PROXY_PORT", "4010")
    try:
        port = int(raw)
    except ValueError:
        raise SystemExit(f"[proxy] ERROR: invalid GW_PROXY_PORT {raw!r}") from None
    if not 1 <= port <= 65535:
        raise SystemExit(
            f"[proxy] ERROR: GW_PROXY_PORT must be between 1 and 65535, got {port}"
        )
    return port


LISTEN = ("127.0.0.1", listen_port())
HEALTH_PATH = "/__ccsession_shim"
# Persistent audit file is OPT-IN. Unset (default) => log to the terminal only
# (ephemeral, never accumulates). Set GW_PROXY_LOGFILE=/path to also persist.
LOGFILE = os.environ.get("GW_PROXY_LOGFILE")

_lock = threading.Lock()
alias_to_real = {}  # claude-gw-... -> real upstream id
_cooldowns = {}  # real model id -> epoch seconds when it may be tried again

# Fixed for the life of this shim; ccsession gives a show-all session its own
# shim (port) so other sessions' pickers never change.
SHOW_ALL = os.environ.get("CCSESSION_SHOW_ALL_MODELS") == "1"


def _seconds(name, default):
    """A positive number of seconds from the environment, else the default."""
    raw = os.environ.get(name)
    try:
        value = float(raw) if raw else default
    except ValueError:
        value = 0
    if value <= 0:
        sys.stderr.write(
            f"[proxy] WARNING: {name}={raw!r} is not a positive number; using {default}\n"
        )
        value = default
    return value


COOLDOWN_SECONDS = _seconds("CCSESSION_COOLDOWN_SECONDS", 3600)
# Timers. NOTHING ever limits a reply once the gateway has started answering:
# a model may think or stream for hours, so the socket has no read timeout
# after the reply's status line arrives.
# - Opening the connection: no ccsession limit; the operating system's own
#   connect wait applies (about 1-2 minutes). Failing to connect means the
#   gateway is unreachable (passed back, never a model switch).
#   _CCSESSION_TEST_CONNECT_TIMEOUT sets a limit for tests only.
# - FIRST_BYTE_TIMEOUT: only for a streamed tier request (Claude Code's normal
#   kind, where a healthy gateway answers with headers at once), how long to
#   wait for the gateway to START answering before treating the model as
#   stalled and trying the next one (owner decision, spec 15 decision 6). Kept
#   under Claude Code's own 10-minute request timeout so the switch happens
#   before Claude Code gives up. Non-streamed requests wait without limit.
FIRST_BYTE_TIMEOUT = _seconds("CCSESSION_FIRST_BYTE_TIMEOUT", 300)
CONNECT_TIMEOUT = (
    _seconds("_CCSESSION_TEST_CONNECT_TIMEOUT", 60)
    if os.environ.get("_CCSESSION_TEST_CONNECT_TIMEOUT")
    else None
)
MAX_COOLDOWN = 7 * 86400  # cap on a gateway Retry-After
_active = 0  # requests being forwarded right now (reported in health)
TIER_PREFIX = "claude-gw-tier"


def audit(msg):
    """Persistent, timestamped ground-truth log of what actually routed."""
    line = f"{datetime.datetime.now().isoformat(timespec='seconds')} {msg}"
    sys.stderr.write("[proxy] " + line + "\n")
    sys.stderr.flush()
    if LOGFILE:
        try:
            with open(LOGFILE, "a") as f:
                f.write(line + "\n")
        except OSError:
            pass


HOP = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
    "content-length",
    "host",
}


def sanitize(rid):
    # One rule shared with ccsession's --model window lookup (models.py).
    return model_data.gateway_alias(rid)


def is_native(rid):
    return model_data.is_native_model(rid)


# --- curation: which real models to hide, and how to order what remains ---
# The lists live in ccsession-models.json (downloaded fresh by ccsession on
# every launch). They are re-read on every model-list request, so a running
# shim picks up new data without a restart.
sys.path.insert(
    0, os.environ.get("CCSESSION_DIR") or os.path.dirname(os.path.abspath(__file__))
)
import models as model_data  # noqa: E402

# The code this shim runs; a launch reuses the shim only on the same code.
CODE = model_data.code_digest(os.path.abspath(__file__))


def curation():
    """Return the active picker rules, tiers, and the data version.

    Model data and tier settings are re-read on every call, so a running shim
    picks up a new data file or a changed workspace env file without a restart.
    """
    data, _source = model_data.load()
    picker = data["picker"]
    tenv = model_data.tier_env()
    on = model_data.tier_mode(tenv=tenv)
    tiers, problem = {}, ""
    if on:
        try:
            tiers = model_data.resolve_tiers(data, tenv)
        except ValueError as exc:
            problem = str(exc)
    return {
        "show": picker["show"],
        "one_million_context": set(picker["one_million_context"]),
        "display_overrides": picker["display_overrides"],
        "version": data["version"],
        "tier_mode": on,
        "tiers": tiers,
        "tier_problem": problem,
    }


_ACR = {
    "gpt": "GPT",
    "glm": "GLM",
    "oss": "OSS",
    "ai": "AI",
    "xai": "xAI",
    "minimax": "MiniMax",
    "minimaxai": "MiniMax",
    "deepseek": "DeepSeek",
    "kimi": "Kimi",
    "qwen": "Qwen",
    "grok": "Grok",
    "claude": "Claude",
    "mistralai": "Mistral",
    "mistral": "Mistral",
    "nemo": "Nemo",
    "opus": "Opus",
    "sonnet": "Sonnet",
    "haiku": "Haiku",
    "fable": "Fable",
    "codex": "Codex",
    "instruct": "Instruct",
    "thinking": "Thinking",
    "reasoning": "Reasoning",
    "composer": "Composer",
    "build": "Build",
    "spark": "Spark",
    "latest": "Latest",
    "code": "Code",
    "highspeed": "Highspeed",
    "mini": "Mini",
    "fast": "Fast",
    "turbo": "Turbo",
    "pro": "Pro",
    "max": "Max",
    "luna": "Luna",
    "sol": "Sol",
    "terra": "Terra",
    "plus": "Plus",
    "review": "Review",
    "auto": "Auto",
    "non": "Non",
    "zai": "Z.ai",
}


def pretty(rid, overrides=None):
    """Human-friendly picker label derived from the real upstream id."""
    overrides = curation()["display_overrides"] if overrides is None else overrides
    if rid in overrides:
        return overrides[rid]
    core = rid.split("/")[-1]  # drop provider path prefixes
    out = []
    for t in re.split(r"[-_]", core):
        if not t:
            continue
        tl = t.lower()
        if tl in _ACR:
            out.append(_ACR[tl])
        elif any(c.isdigit() for c in t):  # version tokens: 5.6, k2.7, 4.20, 0905
            out.append(t)
        else:
            out.append(t.capitalize())
    return " ".join(out)


def _entry(model_id, label):
    return {
        "type": "model",
        "id": model_id,
        "display_name": label,
        "created_at": "2026-01-01T00:00:00Z",
    }


def transform_models(payload):
    """Build the picker list and the alias map.

    Tier mode: the tiers, plus (show-all only) every model named in the tier
    settings. Otherwise: the allow list (picker.show) in order, keeping only
    models the gateway lists. Every gateway model gets an alias, shown or not,
    so a hidden model typed with /model or kept by a resumed session still
    routes.
    """
    rules = curation()
    labels = rules["display_overrides"]
    data = [m for m in payload.get("data", []) if m.get("id")]
    by_id = {m["id"]: m for m in data}
    tier_models = [m for t in rules["tiers"].values() for m in t["models"]]

    # Tier models are named first, so their picker ids never depend on the
    # gateway's list order and match the window map ccsession hands Claude Code.
    alias_of = model_data.assign_aliases(
        [model for _, model, _ in tier_models] + list(by_id)
    )
    new_map = {alias: rid for rid, alias in alias_of.items()}

    out = []
    if rules["tier_mode"]:
        for name, tier in rules["tiers"].items():
            names = ", ".join(pretty(m, labels) for _, m, _ in tier["models"])
            # "[1m]" lets Claude Code accept a long session; the real limit is
            # the tier window ccsession sets at launch.
            out.append(
                _entry(f"{TIER_PREFIX}{name[4:]}[1m]", f"{tier['label']}: {names}")
            )
        listed = []
        if SHOW_ALL:
            for _, model, window in tier_models:
                if model not in (r for r, _ in listed):
                    listed.append((model, window > model_data.DEFAULT_WINDOW))
    else:
        one_million = rules["one_million_context"]
        listed = [(r, r in one_million) for r in rules["show"] if r in by_id]

    for rid, big in listed:
        m = dict(by_id.get(rid) or _entry(rid, ""))
        if not is_native(rid):
            m["id"] = alias_of[rid]
        if not is_native(rid) or not m.get("display_name"):
            m["display_name"] = pretty(rid, labels)
        # Claude Code assumes 200K for any gateway model it cannot look up in
        # its own catalog. "[1m]" is the one suffix it honours, and it strips
        # the suffix before sending, so the id upstream stays unchanged.
        if big:
            m["id"] = f"{m['id']}[1m]"
        out.append(m)
    payload["data"] = out
    with _lock:
        alias_to_real.clear()
        alias_to_real.update(new_map)
    return payload


# --- failover -----------------------------------------------------------------
# Owner-approved switch rules (spec section 5.2): (status or None for any,
# body substrings, any one of which must appear; None = status alone). Matched
# case-insensitively on the error body the gateway sends before any reply.
# Anything else, including a plain 429 "Rate limited" and a 500, is passed back
# to Claude Code unchanged.
SWITCH_RULES = [
    (429, ("are cooling down",), "all accounts out of usage"),
    (429, ("exceed your account's rate limit",), "account rate limit"),
    (429, ("usage credits are required", "usage_limit_reached"), "out of credits"),
    (503, ("auth_unavailable",), "no usable account"),
    (402, None, "prepaid balance empty"),
    (None, ("billing_error",), "prepaid balance empty"),
    (403, ("usage limit",), "usage quota spent"),
    (529, None, "provider busy"),
    (None, ("overloaded",), "provider busy"),
    (400, ("unknown provider for model",), "model no longer routed"),
    (502, ("unknown provider for model",), "model no longer routed"),
    (404, ("not_found_error",), "retired model"),
    (401, ("incorrect api key",), "GATEWAY KEY BROKEN for this provider"),
    # Seen live 2026-10-01: Grok answers some requests with 426 "Your Grok CLI
    # version ... is outdated" (gateway-side login too old) and others with 503
    # auth_unavailable; both mean the model cannot answer.
    (426, ("is outdated",), "provider login outdated on the gateway"),
]
_TOO_LARGE = re.compile(
    r"prompt is too long|too many tokens|context length|context window|maximum context|too large",
    re.I,
)


def switch_reason(status, body_text):
    """Return why this error should move the request to the next model, or ""."""
    text = body_text.lower()
    for want, needles, reason in SWITCH_RULES:
        if want is not None and status != want:
            continue
        if needles is None or any(n in text for n in needles):
            return reason
    return ""


def retry_after_seconds(value):
    """Seconds from a Retry-After header (seconds or HTTP date), else None."""
    if not value:
        return None
    value = value.strip()
    if value.isascii() and value.isdigit():
        # More than 9 digits is past any cap; int() of a huge string raises.
        return min(int(value), MAX_COOLDOWN) if len(value) <= 9 else MAX_COOLDOWN
    try:
        when = email.utils.parsedate_to_datetime(value)
    except (TypeError, ValueError, OverflowError):
        return None
    return min(max(0, int(when.timestamp() - time.time())), MAX_COOLDOWN)


def cool_down(model, retry_after=None):
    until = time.time() + (retry_after if retry_after is not None else COOLDOWN_SECONDS)
    with _lock:
        _cooldowns[model] = until
    return until


def cooling_until(model):
    with _lock:
        until = _cooldowns.get(model, 0)
    return until if until > time.time() else 0


def clock(epoch):
    return datetime.datetime.fromtimestamp(epoch).strftime("%H:%M")


def plain_body(headers, raw):
    """(body, headers) with any gzip/deflate encoding removed.

    Error bodies are matched against SWITCH_RULES and may get a note added, so
    they must be plain text; the Content-Encoding header goes with them.
    """
    encoding = (headers.get("Content-Encoding") or "").lower().strip()
    if encoding in ("gzip", "x-gzip", "deflate"):
        try:
            raw = gzip.decompress(raw) if "gzip" in encoding else zlib.decompress(raw)
        except (OSError, ValueError, EOFError, zlib.error):
            return raw, headers
        headers = {k: v for k, v in headers.items() if k.lower() != "content-encoding"}
    return raw, headers


def with_note(raw, note):
    """Add a ccsession note to a gateway error body (JSON or plain text).

    A JSON body stays valid JSON whatever its shape (the reply keeps its
    application/json content type); only a non-JSON body gets plain text.
    """
    try:
        obj = json.loads(raw)
    except (ValueError, TypeError):
        return raw + f" ({note})".encode()
    if not isinstance(obj, dict):
        obj = {
            "type": "error",
            "error": {"type": "api_error", "message": raw.decode("utf-8", "replace")},
        }
    err = obj.get("error")
    if isinstance(err, dict):
        message = err.get("message")
        err["message"] = f"{message} ({note})" if isinstance(message, str) else note
    elif isinstance(err, str):
        obj["error"] = f"{err} ({note})"
    elif isinstance(obj.get("message"), str):
        obj["message"] = f"{obj['message']} ({note})"
    else:
        obj["message"] = note
    return json.dumps(obj).encode()


class _FirstByteResponse(http.client.HTTPResponse):
    """A reply that may take at most `wait` seconds to send its first byte.

    The wait is on decoded reply bytes, so TLS records that are not reply data
    (TLS 1.3 session tickets) do not end it. From the first byte on (status
    line, headers, the whole body) nothing is timed.
    """

    wait = None

    def __init__(self, sock, *args, **kwargs):
        super().__init__(sock, *args, **kwargs)
        self._upstream_sock = sock

    def begin(self):
        if self.wait is not None and self.headers is None:
            self._upstream_sock.settimeout(self.wait)
            try:
                self.fp.peek(1)  # the byte stays buffered for the parser
            finally:
                self._upstream_sock.settimeout(None)
        super().begin()


class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"  # close-delimited => trivial streaming
    server_version = "gw-alias-proxy/1.0"

    def log_message(self, fmt, *args):
        sys.stderr.write("[proxy] " + (fmt % args) + "\n")

    def _fwd_headers(self):
        h = {}
        for k, v in self.headers.items():
            if k.lower() not in HOP:
                h[k] = v
        return h

    def _model_headers(self):
        """Request plain JSON because model discovery rewrites the response body."""
        headers = self._fwd_headers()
        headers["Accept-Encoding"] = "identity"
        return headers

    def _counted(self, handler, *args):
        """Run a forwarding handler while counting it as in flight (health)."""
        global _active
        with _lock:
            _active += 1
        try:
            return handler(*args)
        finally:
            with _lock:
                _active -= 1

    def do_GET(self):
        path = self.path.split("?")[0].rstrip("/")
        if path == HEALTH_PATH:
            return self._handle_health()
        if path.endswith("/v1/models"):
            return self._handle_models()
        return self._counted(self._proxy, None)

    def _handle_health(self):
        rules = curation()
        payload = json.dumps(
            {
                "service": "ccsession-gateway-alias-proxy",
                "upstream": UPSTREAM,
                "port": LISTEN[1],
                "model_data": rules["version"],
                "show_all": SHOW_ALL,
                "settings": model_data.settings_digest(),
                "code": CODE,
                "pid": os.getpid(),
                "active": _active,
                "tier_mode": rules["tier_mode"],
                "tiers": {
                    name: [m for _, m, _ in t["models"]]
                    for name, t in rules["tiers"].items()
                },
            }
        ).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):
        return self._counted(self._post)

    def _post(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        body = self.rfile.read(length) if length else b""
        # un-alias the model field on the way out
        tier_name = ""
        if body:
            try:
                obj = json.loads(body)
                m = obj.get("model")
                tier = (
                    m[len(TIER_PREFIX) :]
                    if isinstance(m, str) and m.startswith(TIER_PREFIX)
                    else ""
                )
                if tier.isdigit() and tier.isascii():
                    tier_name = f"tier{tier}"
                elif isinstance(m, str) and m.startswith("claude-gw-"):
                    with _lock:
                        known = m in alias_to_real
                    if not known:  # cold map: self-heal from upstream
                        self._refresh_models()
                    with _lock:
                        real = alias_to_real.get(m)
                    if real:
                        obj["model"] = real
                        body = json.dumps(obj).encode()
                        audit(f"REQUEST  {self.path}  alias={m}  -> real={real}")
                    else:
                        audit(f"WARN  unknown alias {m} (not in upstream /v1/models)")
            except (ValueError, TypeError):
                tier_name = ""
        if tier_name:
            # Outside the parse guard: an error while routing must never send
            # the request on again under its alias name.
            return self._forward_tier(tier_name, obj)
        return self._proxy(body=body)

    def _refresh_models(self):
        """Rebuild alias map from upstream using this request's auth header."""
        try:
            req = urllib.request.Request(
                UPSTREAM + "/v1/models", headers=self._model_headers(), method="GET"
            )
            transform_models(json.loads(urllib.request.urlopen(req, timeout=10).read()))
            with _lock:
                audit(f"map refreshed: {len(alias_to_real)} aliases")
        except Exception as e:  # noqa: BLE001 - best-effort refresh
            audit(f"map refresh failed: {e}")

    def _handle_models(self):
        url = UPSTREAM + self.path
        req = urllib.request.Request(url, headers=self._model_headers(), method="GET")
        try:
            resp = urllib.request.urlopen(req, timeout=10)
            raw = resp.read()
            status = resp.status
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.end_headers()
            self.wfile.write(e.read())
            return
        try:
            payload = transform_models(json.loads(raw))
            out = json.dumps(payload).encode()
        except ValueError:
            out = raw
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)
        with _lock:
            self.log_message("/v1/models -> %d aliases exposed", len(alias_to_real))

    def _proxy(self, body):
        """Forward any request unchanged and stream the reply, with no time limit."""
        result = self._open_upstream(body, wait=None, identity=False)
        if result[0] != "reply":
            return self._send_error_json(
                502, "api_error", f"ccsession: gateway unreachable: {result[-1]}"
            )
        _, conn, resp = result
        try:
            self._stream(resp.status, resp.headers, resp)
        finally:
            conn.close()

    def _send_body(self, status, headers, raw):
        self.send_response(status)
        for k, v in headers.items():
            if k.lower() not in HOP:
                self.send_header(k, v)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _send_error_json(self, status, err_type, message):
        raw = json.dumps(
            {"type": "error", "error": {"type": err_type, "message": message}}
        ).encode()
        self._send_body(status, {"Content-Type": "application/json"}, raw)

    def _open_upstream(self, body, wait=None, identity=True):
        """Send this request upstream.

        Returns ("reply", conn, resp), ("timeout", None) or ("unreachable", exc).
        `wait` limits only the time until the gateway STARTS answering (None =
        no limit). After the status line arrives there is no timeout at all.
        `identity` asks for an uncompressed reply (error bodies are matched
        against SWITCH_RULES); plain forwarding keeps the client's choice.
        """
        u = urllib.parse.urlsplit(UPSTREAM + self.path)
        cls = (
            http.client.HTTPSConnection
            if u.scheme == "https"
            else http.client.HTTPConnection
        )
        conn = cls(u.hostname, u.port, timeout=CONNECT_TIMEOUT)
        headers = self._fwd_headers()
        if identity:
            # Header names arrive in any case; replace every variant.
            headers = {
                k: v for k, v in headers.items() if k.lower() != "accept-encoding"
            }
            headers["Accept-Encoding"] = "identity"
        if body is not None:
            headers["Content-Length"] = str(len(body))
        target = u.path + (f"?{u.query}" if u.query else "")
        try:
            conn.connect()
        except OSError as exc:  # includes a connect timeout: the gateway is down
            conn.close()
            return ("unreachable", exc)
        conn.sock.settimeout(None)
        if wait is not None:
            # The only limit: until the gateway sends its FIRST byte.
            conn.response_class = type(
                "_WaitedResponse", (_FirstByteResponse,), {"wait": wait}
            )
        try:
            conn.request(self.command, target, body=body, headers=headers)
            resp = conn.getresponse()
        except socket.timeout:  # only the first-byte wait sets a timeout
            conn.close()
            return ("timeout", None)
        except (OSError, http.client.HTTPException) as exc:
            # HTTPException: a malformed or cut-off status line or headers.
            conn.close()
            return ("unreachable", exc)
        return ("reply", conn, resp)

    def _forward_tier(self, name, obj):
        """Send the request to the tier's models in order until one answers."""
        rules = curation()
        tier = rules["tiers"].get(name)
        if not tier:
            why = rules["tier_problem"] or f"{name} is not defined"
            audit(f"TIER {name}: cannot route ({why})")
            return self._send_error_json(
                400, "invalid_request_error", f"ccsession {name}: {why}"
            )
        tier_window = tier["window"]
        last = None  # (status, headers, raw) of the last error seen
        # A backup that could not hold the conversation. Kept even when later
        # models fail on usage, so the reply never hides the size problem.
        size_error = None
        for position, (slot, model, window) in enumerate(tier["models"]):
            if window < tier_window:
                continue  # cannot hold this tier's context (spec section 6)
            if cooling_until(model):
                continue
            obj["model"] = model
            # Only a streamed request gets the start-of-reply limit.
            wait = FIRST_BYTE_TIMEOUT if obj.get("stream") else None
            result = self._open_upstream(json.dumps(obj).encode(), wait=wait)
            if result[0] == "unreachable":
                audit(f"TIER {name}: gateway unreachable ({result[1]}); not switching")
                return self._send_error_json(
                    502, "api_error", f"ccsession: gateway unreachable: {result[1]}"
                )
            if result[0] == "timeout":
                until = cool_down(model)
                audit(
                    f"TIER {name}: {slot} {model} gave no reply in {FIRST_BYTE_TIMEOUT:.0f}s; cooling down until {clock(until)}"
                )
                last = (
                    504,
                    {"Content-Type": "application/json"},
                    json.dumps(
                        {
                            "type": "error",
                            "error": {
                                "type": "timeout_error",
                                "message": f"{model}: no reply in {FIRST_BYTE_TIMEOUT:.0f}s",
                            },
                        }
                    ).encode(),
                )
                continue
            _, conn, resp = result
            if resp.status < 400:
                audit(f"TIER {name}: {slot} -> {model}")
                try:
                    return self._stream(resp.status, resp.headers, resp)
                finally:
                    conn.close()
            try:
                raw, headers = plain_body(resp.headers, resp.read())
            except (OSError, http.client.HTTPException) as exc:
                # The gateway dropped its error reply part-way.
                audit(
                    f"TIER {name}: {model} error reply cut off ({exc!r}); not switching"
                )
                return self._send_error_json(
                    502,
                    "api_error",
                    f"ccsession: gateway error reply from {model} was cut off: {exc!r}",
                )
            finally:
                conn.close()
            text = raw.decode("utf-8", "replace")
            reason = switch_reason(resp.status, text)
            if reason:
                until = cool_down(
                    model,
                    retry_after_seconds(
                        next(
                            (
                                v
                                for k, v in headers.items()
                                if k.lower() == "retry-after"
                            ),
                            None,
                        )
                    ),
                )
                audit(
                    f"TIER {name}: {slot} {model} -> next model ({resp.status} {reason}); cooling down until {clock(until)}"
                )
                last = (resp.status, headers, raw)
                continue
            # A backup (not the tier's main model) that cannot hold the
            # conversation: try the next backup (spec section 6).
            if position > 0 and _TOO_LARGE.search(text):
                audit(
                    f"TIER {name}: backup {model} rejected the request as too large; trying the next one"
                )
                last = size_error = (resp.status, headers, raw)
                continue
            return self._send_body(resp.status, headers, raw)  # not a switch error
        waits = [cooling_until(m) for _, m, w in tier["models"] if w >= tier_window]
        waits = [w for w in waits if w]
        retry = f"; next retry at {clock(min(waits))}" if waits else ""
        if size_error:
            # At least one available model was too small for the conversation:
            # report that, not only "out of usage" (which depends on order).
            note = f"ccsession: no available {tier['label']} model can hold this conversation"
            if waits:
                note += f"; the others are out of usage{retry}"
            audit(f"TIER {name}: {note}")
            status, headers, raw = size_error
            return self._send_body(status, headers, with_note(raw, note))
        note = f"ccsession: all {tier['label']} models are out of usage{retry}"
        audit(f"TIER {name}: {note}")
        if last:
            status, headers, raw = last
            return self._send_body(status, headers, with_note(raw, note))
        return self._send_error_json(429, "rate_limit_error", note)

    def _stream(self, status, headers, resp):
        self.send_response(status)
        for k, v in headers.items():
            if k.lower() not in HOP:
                self.send_header(k, v)
        self.end_headers()
        sniff = b""
        found = False
        while True:
            # read1: hand over whatever has arrived, however small (a lone
            # keep-alive or thinking event), instead of waiting for 8 KB.
            chunk = resp.read1(8192)
            if not chunk:
                break
            if not found and len(sniff) < 8192:
                sniff += chunk
                mm = re.search(rb'"model"\s*:\s*"([^"]+)"', sniff)
                if mm:
                    audit(
                        f"RESPONSE {self.path}  backend served model={mm.group(1).decode()}"
                    )
                    found = True
            try:
                self.wfile.write(chunk)
                self.wfile.flush()
            except BrokenPipeError:
                break


class ThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == "__main__":
    host, port = LISTEN
    try:
        srv = ThreadingServer(LISTEN, Handler)
    except OSError as e:
        if e.errno == 48:  # EADDRINUSE
            print(
                f"[proxy] ERROR: port {port} is already in use "
                f"(a proxy is likely already running).\n"
                f"[proxy] Stop the old one first:  lsof -ti:{port} | xargs kill",
                file=sys.stderr,
            )
            sys.exit(1)
        raise
    print(f"[proxy] listening on http://{host}:{port}  ->  {UPSTREAM}", file=sys.stderr)
    srv.serve_forever()
