"""Data-class privacy guard and per-experiment manifest (contract J3)."""
import json
import os
import pathlib
import re
from collections import defaultdict

from .config import ALLOWED_DATA_CLASSES, KEY_ENV
from .questions import canonical_bytes

# Contract J3 list. `sk-` and `ghp_` are anchored to token-like shapes so words such as "task-based" or "risk-based" are not refused.
_PATTERNS = [
    ("email", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")),
    ("path_home", re.compile(r"/home/")),
    ("path_root", re.compile(r"/root/")),
    ("path_tmp_claude", re.compile(r"/tmp/claude")),
    ("owner_org", re.compile(r"IronbellyOrg")),
    ("upstream_org", re.compile(r"SuperClaude-Org")),
    ("github_url", re.compile(r"github\.com/")),
    ("private_key", re.compile(r"BEGIN [A-Z ]*PRIVATE KEY")),
    ("github_token", re.compile(r"(?<![A-Za-z0-9])ghp_[A-Za-z0-9]{6,}")),
    ("secret_key", re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{6,}")),
    ("key_env_name", re.compile(KEY_ENV)),
]


def privacy_violation(req: dict, data_classes, allowed=ALLOWED_DATA_CLASSES):
    """None when the request may be sent, else a short reason string (never the matched text)."""
    if not data_classes or not set(data_classes) <= set(allowed):
        return f"data class not allowed: {sorted(set(data_classes or []) - set(allowed)) or 'none given'}"
    text = canonical_bytes(req).decode("utf-8")
    for name, rx in _PATTERNS:
        if rx.search(text):
            return f"pattern {name}"
    key = os.environ.get(KEY_ENV)
    if key and key in text:
        return "pattern key_value"
    return None


def update(journal_path, out_path) -> dict:
    counts = defaultdict(lambda: defaultdict(lambda: {"logical_calls": 0, "input_tokens": 0}))
    first = last = None
    models = set()
    for line in pathlib.Path(journal_path).read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        ts = r.get("ts_utc")
        if ts:
            first = ts if first is None or ts < first else first
            last = ts if last is None or ts > last else last
        if not r.get("final"):
            continue
        if r.get("model_returned"):
            models.add(r["model_returned"])
        tok = (r.get("usage") or {}).get("input_tokens")
        if tok is None:
            tok = 0
        for c in r.get("data_classes") or ["unknown"]:
            cell = counts[r.get("phase", "?")][c]
            cell["logical_calls"] += 1
            cell["input_tokens"] += tok
    out = {"schema": "jev-manifest/1", "journal": str(journal_path),
           "counts": {p: {c: v for c, v in d.items()} for p, d in counts.items()},
           "first_ts": first, "last_ts": last, "models": sorted(models)}
    pathlib.Path(out_path).write_text(json.dumps(out, indent=1))
    return out
