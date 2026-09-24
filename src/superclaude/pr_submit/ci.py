"""CI-check classifier for the ``sc:pr-submit`` monitor (spec PR-SUBMIT-CI).

Pure: consumes an already-fetched checks payload and (optionally) failed-job
logs. Does not import or name any version-control command tokens (NFR-6).
"""

from __future__ import annotations

import re

from .classifier import STATE_CLEAN, STATE_FINDINGS, STATE_POLLING
from .models import Finding

_MAX_FINDINGS = 10
# Job logs prefix each line (`job<TAB>step<TAB>`); do not require start-of-line.
_RUFF_LINE = re.compile(r"(?P<path>(?:src|tests)/\S+\.py):(?P<line>\d+):\d+:\s+\S+")
_PYTEST_LINE = re.compile(r"(?P<path>(?:src|tests)/\S+\.py):(?P<line>\d+):\s")
_RUN_ID = re.compile(r"/actions/runs/(\d+)")
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
        bucket == "cancel" or state == "action_required" or _HUMAN_NAME in name.lower()
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
        n_this = 0
        for path, line, body in _parse_file_line(log):
            key = (path, line)
            if key in seen:
                continue
            seen.add(key)
            found.append(Finding(path=path, line=line, body=body))
            n_this += 1
            if n_this >= _MAX_FINDINGS:
                break
    return found


def _run_id_from_link(link: str) -> str:
    match = _RUN_ID.search(link)
    return match.group(1) if match else ""


def _log_for(check: dict, logs_by_run: dict[str, str]) -> str:
    rid = _run_id_from_link(str(check.get("link") or ""))
    if rid and rid in logs_by_run:
        return logs_by_run[rid]
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
