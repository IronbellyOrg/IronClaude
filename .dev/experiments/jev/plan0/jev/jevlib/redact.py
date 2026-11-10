"""Redaction of the current API key from any record (contract J2)."""
import os

from .config import KEY_ENV

MARK = "[REDACTED]"


def redact(obj):
    key = os.environ.get(KEY_ENV)
    if not key:
        return obj
    return _walk(obj, key)


def _walk(o, key):
    if isinstance(o, str):
        return o.replace(key, MARK)
    if isinstance(o, dict):
        return {(_walk(k, key) if isinstance(k, str) else k): _walk(v, key) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_walk(v, key) for v in o]
    return o
