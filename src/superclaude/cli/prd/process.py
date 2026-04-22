"""PRD pipeline process management -- subprocess lifecycle for PRD agents.

Extends the base ``ClaudeProcess`` with PRD-specific prompt construction,
phase-aware ``--file`` arg scoping, subprocess timeout enforcement via
external watchdog, and launch retry with exponential backoff.

NFR-PRD.1: Zero ``async def`` or ``await`` in this module.
NFR-PRD.7: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.
NFR-PRD.12/GAP-011: Retry up to 2 times with exponential backoff on transient failures.
NFR-PRD.13/F-004: Subprocess timeout via Popen watchdog (SIGTERM -> 5s -> SIGKILL).
GAP-003: Phase-aware ``--file`` arg scoping.
"""

from __future__ import annotations

import logging
import os
import signal
import subprocess
import time
from pathlib import Path
from typing import Optional

from superclaude.cli.pipeline.process import ClaudeProcess

from .models import PrdConfig

_log = logging.getLogger("superclaude.prd.process")


# ---------------------------------------------------------------------------
# Transient failure detection
# ---------------------------------------------------------------------------

# Exit codes and stderr patterns that indicate transient failures
# (rate limiting, API unavailability, network errors).
_TRANSIENT_EXIT_CODES = frozenset({1, 2, 137})  # generic error, SIGKILL
_TRANSIENT_PATTERNS = (
    "rate limit",
    "rate_limit",
    "429",
    "503",
    "502",
    "connection refused",
    "connection reset",
    "timeout",
    "ETIMEDOUT",
    "ECONNRESET",
    "temporarily unavailable",
)

# Non-transient patterns that should NOT be retried
_NON_TRANSIENT_PATTERNS = (
    "permission denied",
    "invalid arg",
    "invalid option",
    "not found",
    "no such file",
    "usage:",
)


def _is_transient_failure(exit_code: int, stderr_text: str) -> bool:
    """Determine if a failure is transient and retryable.

    Returns True for rate limiting, API unavailability, and network
    errors. Returns False for invalid args, permission denied, etc.
    """
    stderr_lower = stderr_text.lower()

    # Non-transient patterns always fail immediately
    for pattern in _NON_TRANSIENT_PATTERNS:
        if pattern in stderr_lower:
            return False

    # Check for transient patterns
    for pattern in _TRANSIENT_PATTERNS:
        if pattern in stderr_lower:
            return True

    # Exit code 124 is timeout -- not transient (already timed out)
    if exit_code == 124:
        return False

    # Generic non-zero with no matching pattern: not transient
    return False


# ---------------------------------------------------------------------------
# Phase-to-allowed-refs mapping (GAP-003)
# ---------------------------------------------------------------------------

# Maps step IDs to the list of refs files each phase is allowed to read.
# Files > 50KB are passed as --file args; files < 50KB are inlined in prompt.
_PHASE_ALLOWED_REFS: dict[str, list[str]] = {
    "parse-request": [],
    "scope-discovery": [],
    "research-notes": [],
    "sufficiency-review": [],
    "template-triage": ["build-request-template.md"],
    "build-task-file": ["build-request-template.md", "operational-guidance.md"],
    "verify-task-file": ["validation-checklists.md"],
    "preparation": ["operational-guidance.md"],
    "investigation": ["operational-guidance.md"],
    "research-qa": ["validation-checklists.md"],
    "web-research": ["operational-guidance.md"],
    "synthesis": ["synthesis-mapping.md", "operational-guidance.md"],
    "synthesis-qa": ["validation-checklists.md"],
    "assembly": ["synthesis-mapping.md", "operational-guidance.md"],
    "structural-qa": ["validation-checklists.md"],
    "qualitative-qa": ["validation-checklists.md"],
    "present-complete": [],
}

_FILE_SIZE_THRESHOLD = 50_000  # 50KB: inline vs --file cutoff


# ---------------------------------------------------------------------------
# PrdClaudeProcess
# ---------------------------------------------------------------------------


class PrdClaudeProcess(ClaudeProcess):
    """PRD-specific subprocess extending the pipeline base ClaudeProcess.

    Adds:
    - Phase-aware ``--file`` arg construction (GAP-003)
    - Subprocess timeout enforcement via Popen watchdog (NFR-PRD.13/F-004)
    - Launch retry with exponential backoff (NFR-PRD.12/GAP-011)
    """

    def __init__(
        self,
        *,
        config: PrdConfig,
        step_id: str,
        prompt: str,
        output_file: Path,
        error_file: Path,
        timeout_seconds: int = 3600,
        max_retries: int = 2,
    ) -> None:
        self.prd_config = config
        self.step_id = step_id
        self._max_retries = max_retries
        self._retry_delays = [5.0, 15.0]  # exponential backoff

        # Build --file args from phase-allowed refs
        file_args = self._build_file_args(config, step_id)

        super().__init__(
            prompt=prompt,
            output_file=output_file,
            error_file=error_file,
            max_turns=config.max_turns,
            model=config.model,
            permission_flag=config.permission_flag,
            timeout_seconds=timeout_seconds,
            output_format="stream-json",
            extra_args=file_args,
        )

    @staticmethod
    def _build_file_args(config: PrdConfig, step_id: str) -> list[str]:
        """Build --file args for refs files allowed by this step.

        GAP-003: Each subprocess receives only refs files permitted
        for its phase. Files > 50KB are passed as --file args;
        files < 50KB would be inlined in the prompt by the prompt
        builder (not handled here).
        """
        # Normalize step_id: "investigation-3" -> "investigation"
        base_step = step_id.rsplit("-", 1)[0] if step_id[-1:].isdigit() else step_id

        allowed = _PHASE_ALLOWED_REFS.get(base_step, [])
        if not allowed:
            return []

        file_args: list[str] = []
        for ref_name in allowed:
            ref_path = config.skill_refs_dir / ref_name
            if ref_path.is_file():
                try:
                    size = ref_path.stat().st_size
                except OSError:
                    continue
                if size > _FILE_SIZE_THRESHOLD:
                    file_args.extend(["--file", str(ref_path)])

        return file_args

    def start_with_retry(self) -> subprocess.Popen:
        """Launch the process with retry on transient failures.

        NFR-PRD.12/GAP-011: Retry up to 2 times with exponential
        backoff (5s, 15s) on transient failures. Non-transient
        failures (invalid args, permission denied) fail immediately.

        Returns:
            The Popen process on success.

        Raises:
            RuntimeError: If all retries are exhausted or a
                non-transient failure occurs.
        """
        last_error: Optional[Exception] = None

        for attempt in range(self._max_retries + 1):
            try:
                proc = self.start()
                return proc
            except OSError as exc:
                last_error = exc
                stderr_text = str(exc)

                if not _is_transient_failure(1, stderr_text):
                    raise RuntimeError(
                        f"Non-transient launch failure for step "
                        f"{self.step_id!r}: {exc}"
                    ) from exc

                if attempt < self._max_retries:
                    delay = self._retry_delays[attempt]
                    _log.warning(
                        "Transient failure on attempt %d for step %s, "
                        "retrying in %.0fs: %s",
                        attempt + 1,
                        self.step_id,
                        delay,
                        exc,
                    )
                    time.sleep(delay)

        raise RuntimeError(
            f"All {self._max_retries + 1} launch attempts failed for "
            f"step {self.step_id!r}: {last_error}"
        )

    def terminate(self) -> None:
        """Graceful shutdown: SIGTERM -> 5s grace -> SIGKILL.

        NFR-PRD.13/F-004: Override base terminate to use 5s grace
        period instead of default 10s.
        """
        if self._process is None or self._process.poll() is not None:
            self._close_handles()
            return

        use_pgroup = all(hasattr(os, attr) for attr in ("getpgid", "killpg"))
        pgid = os.getpgid(self._process.pid) if use_pgroup else None

        try:
            if self._on_signal is not None:
                self._on_signal(self._process.pid, "SIGTERM")
            if use_pgroup and pgid is not None:
                os.killpg(pgid, signal.SIGTERM)
            else:
                self._process.terminate()
            _log.debug("SIGTERM sent to pid=%d", self._process.pid)
        except ProcessLookupError:
            self._close_handles()
            return

        try:
            self._process.wait(timeout=5)  # 5s grace per F-004
        except subprocess.TimeoutExpired:
            try:
                if use_pgroup and pgid is not None:
                    os.killpg(pgid, signal.SIGKILL)
                else:
                    self._process.kill()
                _log.debug("SIGKILL sent to pid=%d", self._process.pid)
                self._process.wait(timeout=5)
            except (ProcessLookupError, subprocess.TimeoutExpired):
                pass

        if self._on_exit is not None:
            self._on_exit(self._process.pid, self._process.returncode)
        self._close_handles()
