"""CI-check classifier for the ``sc:pr-submit`` monitor (spec PR-SUBMIT-CI).

Pure: consumes an already-fetched checks payload and (optionally) failed-job
logs. Does not import or name any version-control command tokens (NFR-6).
"""

from __future__ import annotations

import re

from .classifier import STATE_CLEAN, STATE_FINDINGS, STATE_POLLING
from .models import Finding

_MAX_FINDINGS = 10
_RUFF_LINE = re.compile(r"(?m)^(?P<path>\S+\.py):(?P<line>\d+):\d+:\s+\S+")
_PYTEST_LINE = re.compile(r"(?m)^(?P<path>\S+\.py):(?P<line>\d+):\s")
_HUMAN_NAME = "boundary"


def classify_checks(payload: dict, *, wait_sha: str | None = None) -> str:
    """Return ``polling`` / ``clean`` / ``findings``. Pure. No DetectionContract.

    If ``wait_sha`` is set and ``payload['head_sha']`` differs, return
    ``polling`` (PR head has not caught up to this wait).
    """
    if not isinstance(payload, dict):
        return STATE_CLEAN
    head = payload.get("head_sha")
    if wait_sha and head and head != wait_sha:
        return STATE_POLLING
    checks = payload.get("checks")
    if not isinstance(checks, list) or not checks:
        return STATE_CLEAN
    buckets = {str(c.get("bucket", "")).lower() for c in checks if isinstance(c, dict)}
    states = {str(c.get("state", "")).lower() for c in checks if isinstance(c, dict)}
    if "pending" in buckets:
        return STATE_POLLING
    if "fail" in buckets or "cancel" in buckets:
        return STATE_FINDINGS
    if any(s == "action_required" for s in states):
        return STATE_FINDINGS
    return STATE_CLEAN


def is_human_gate(check: dict) -> bool:
    """True for cancel, ``action_required``, or a name containing ``boundary``."""
    if not isinstance(check, dict):
        return False
    bucket = str(check.get("bucket", "")).lower()
    state = str(check.get("state", "")).lower()
    name = str(check.get("name") or check.get("workflow") or "")
    return (
        bucket == "cancel"
        or state == "action_required"
        or _HUMAN_NAME in name.lower()
    )


def findings_from_logs(
    checks: list[dict], logs_by_run: dict[str, str]
) -> list[Finding]:
    """Parse pytest/ruff ``file:line``. Empty list if none parse (no fake path)."""
    found: list[Finding] = []
    seen: set[tuple[str, int]] = set()
    for check in checks:
        if not isinstance(check, dict) or is_human_gate(check):
            continue
        log = _log_for(check, logs_by_run)
        if not log:
            continue
        for path, line, body in _parse_file_line(log):
            key = (path, line)
            if key in seen:
                continue
            seen.add(key)
            found.append(Finding(path=path, line=line, body=body))
            if len(found) >= _MAX_FINDINGS:
                return found
    return found


def _log_for(check: dict, logs_by_run: dict[str, str]) -> str:
    link = str(check.get("link") or "")
    for run_id, log in logs_by_run.items():
        if run_id and run_id in link:
            return log
    if len(logs_by_run) == 1:
        return next(iter(logs_by_run.values()))
    return ""


def _parse_file_line(log: str) -> list[tuple[str, int, str]]:
    """pytest ``path:line:`` and ruff ``path:line:col:`` only. First N unique."""
    hits: list[tuple[str, int, str]] = []
    seen: set[tuple[str, int]] = set()
    for rx in (_RUFF_LINE, _PYTEST_LINE):
        for match in rx.finditer(log):
            path = match.group("path")
            line = int(match.group("line"))
            key = (path, line)
            if line <= 0 or key in seen:
                continue
            seen.add(key)
            hits.append((path, line, match.group(0).strip()))
            if len(hits) >= _MAX_FINDINGS:
                return hits
    return hits
