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

It changes NOTHING upstream. Point Claude Code at it:
  export ANTHROPIC_BASE_URL=http://127.0.0.1:4010
  export ANTHROPIC_AUTH_TOKEN=<your litellm key>
  export CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1
  rm -f ~/.claude/cache/gateway-models.json   # force a fresh discovery
"""

import datetime
import http.server
import json
import os
import re
import socketserver
import sys
import threading
import urllib.error
import urllib.request

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
    return "claude-gw-" + re.sub(r"[^A-Za-z0-9.]+", "-", rid).strip("-").lower()


def is_native(rid):
    return rid.startswith("claude") or rid.startswith("anthropic")


# --- curation: which real models to hide, and how to order what remains ---
# The lists live in ccsession-models.json (downloaded fresh by ccsession on
# every launch). They are re-read on every model-list request, so a running
# shim picks up new data without a restart.
sys.path.insert(
    0, os.environ.get("CCSESSION_DIR") or os.path.dirname(os.path.abspath(__file__))
)
import models as model_data  # noqa: E402


def curation():
    """Return the active picker rules and the data version they came from."""
    data, _source = model_data.load()
    picker = data["picker"]
    return {
        "remove": set(picker["remove"]),
        "pinned": picker["pinned"],
        "tail": picker["tail"],
        "one_million_context": set(picker["one_million_context"]),
        "display_overrides": picker["display_overrides"],
        "version": data["version"],
    }


FAMILY_ORDER = ["claude", "openai", "moonshot", "qwen", "gemini", "other"]


def family(rid):
    r = rid.lower()
    if r.startswith("claude"):
        return "claude"
    if r.startswith("qwen") or "/qwen" in r:
        return "qwen"
    if "kimi" in r or "moonshot" in r:
        return "moonshot"
    if "gpt" in r or "codex" in r:
        return "openai"
    if "gemini" in r:
        return "gemini"
    return "other"


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


def transform_models(payload):
    """Drop removed ids, order pinned/families/tail, alias non-claude ids."""
    rules = curation()
    remove, pinned, tail_ids = rules["remove"], rules["pinned"], rules["tail"]
    one_million = rules["one_million_context"]
    data = [m for m in payload.get("data", []) if m.get("id")]
    by_id = {m["id"]: m for m in data}

    ordered = [p for p in pinned if p in by_id and p not in remove]
    tail = [t for t in tail_ids if t in by_id and t not in remove]
    tail_set = set(tail)
    seen = set(ordered)
    buckets = {f: [] for f in FAMILY_ORDER}
    for m in data:  # preserve upstream order within each family
        rid = m["id"]
        if rid in remove or rid in seen or rid in tail_set:
            continue
        buckets[family(rid)].append(rid)
        seen.add(rid)
    for f in FAMILY_ORDER:
        ordered.extend(buckets[f])
    ordered.extend(tail)

    new_map, used, out = {}, set(), []
    for rid in ordered:
        m = dict(by_id[rid])
        if is_native(rid):
            # Claude-named ids route upstream untouched, so they never enter the
            # alias map. Some arrive without a label; give the picker one.
            if not m.get("display_name"):
                m["display_name"] = pretty(rid, rules["display_overrides"])
        else:
            a = sanitize(rid)
            cand, k = a, 2
            while cand in used:
                cand = f"{a}-{k}"
                k += 1
            used.add(cand)
            new_map[cand] = rid
            m["id"] = cand
            m["display_name"] = pretty(
                rid, rules["display_overrides"]
            )  # friendly picker label
        # Claude Code assumes 200K for any gateway model it cannot look up in
        # its own catalog. "[1m]" is the one suffix it honours, and it strips
        # the suffix before sending, so the id upstream stays unchanged.
        if rid in one_million:
            m["id"] = f"{m['id']}[1m]"
        out.append(m)
    payload["data"] = out
    with _lock:
        alias_to_real.clear()
        alias_to_real.update(new_map)
    return payload


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

    def do_GET(self):
        path = self.path.split("?")[0].rstrip("/")
        if path == HEALTH_PATH:
            return self._handle_health()
        if path.endswith("/v1/models"):
            return self._handle_models()
        return self._proxy(body=None)

    def _handle_health(self):
        payload = json.dumps(
            {
                "service": "ccsession-gateway-alias-proxy",
                "upstream": UPSTREAM,
                "port": LISTEN[1],
                "model_data": curation()["version"],
            }
        ).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        body = self.rfile.read(length) if length else b""
        # un-alias the model field on the way out
        if body:
            try:
                obj = json.loads(body)
                m = obj.get("model")
                if isinstance(m, str) and m.startswith("claude-gw-"):
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
                pass
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
        url = UPSTREAM + self.path
        req = urllib.request.Request(
            url, data=body, headers=self._fwd_headers(), method=self.command
        )
        try:
            resp = urllib.request.urlopen(req, timeout=600)
        except urllib.error.HTTPError as e:
            resp = e
        self.send_response(getattr(resp, "status", getattr(resp, "code", 502)))
        for k, v in resp.headers.items():
            if k.lower() not in HOP:
                self.send_header(k, v)
        self.end_headers()
        sniff = b""
        found = False
        while True:
            chunk = resp.read(8192)
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
