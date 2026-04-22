"""PRD pipeline monitor -- NDJSON output parsing and stall detection.

Parses subprocess NDJSON stdout lines and updates PrdMonitorState
for TUI consumption. Detects PRD-specific signals: research file
completion, QA verdict extraction, fix cycle counting, synthesis
completion.

NFR-PRD.1: Zero ``async def`` or ``await`` in this module.
NFR-PRD.7: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.
GAP-002: No imports from executor.py or tui.py.
"""

from __future__ import annotations

import json
import re
import time
from typing import Optional

from .models import PrdMonitorState


# ---------------------------------------------------------------------------
# Signal detection patterns (PRD-specific)
# ---------------------------------------------------------------------------

# Research file creation: research/NN-*.md
_RESEARCH_FILE_PATTERN = re.compile(r"research/\d{2}-[\w-]+\.md")

# Synthesis file creation: synthesis/synth-*.md
_SYNTH_FILE_PATTERN = re.compile(r"synthesis/synth-\d{2}-[\w-]+\.md")

# QA verdict extraction: "verdict": "PASS" or verdict: PASS
_QA_VERDICT_JSON_PATTERN = re.compile(r'"verdict"\s*:\s*"(PASS|FAIL)"')
_QA_VERDICT_MD_PATTERN = re.compile(
    r"(?:^|\n)\s*\*{0,2}[Vv]erdict\*{0,2}\s*:\s*(PASS|FAIL)"
)

# Fix cycle counter: "fix_cycle": N or fix cycle N
_FIX_CYCLE_PATTERN = re.compile(r'"fix_cycle"\s*:\s*(\d+)')
_FIX_CYCLE_TEXT_PATTERN = re.compile(r"fix\s+cycle\s+(\d+)", re.IGNORECASE)

# Agent type detection
_AGENT_TYPE_PATTERN = re.compile(
    r'"agent_type"\s*:\s*"(research|synthesis|web|qa|assembly)"'
)

# Step ID detection
_STEP_ID_PATTERN = re.compile(r'"step_id"\s*:\s*"([^"]+)"')


# ---------------------------------------------------------------------------
# PrdMonitor
# ---------------------------------------------------------------------------


class PrdMonitor:
    """Parses NDJSON output lines and maintains PrdMonitorState.

    Designed to be called from the executor's main loop or a sidecar
    thread. Each call to ``parse_line`` updates the internal state
    which the TUI reads via ``get_state``.

    No imports from executor.py or tui.py (GAP-002).
    """

    def __init__(self) -> None:
        self._state = PrdMonitorState()

    def parse_line(self, line: str) -> None:
        """Parse a single NDJSON line and update monitor state.

        Args:
            line: A single line from subprocess stdout (may be JSON
                  or plain text).
        """
        line = line.strip()
        if not line:
            return

        # Update liveness on every non-empty line
        now = time.monotonic()
        self._state.last_event_time = now
        self._state.events_received += 1
        self._state.output_bytes += len(line.encode("utf-8", errors="replace"))

        # Try JSON parse first
        event: Optional[dict] = None
        try:
            event = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            pass

        if event is not None:
            self._extract_from_event(event)

        # Always run text-based signal extraction (covers both JSON
        # stringified content and plain text lines)
        self._extract_from_text(line)

    def check_stall(self, threshold_seconds: float) -> bool:
        """Check if the monitor has stalled (no events within threshold).

        NFR-PRD.5: Stall detection comparing last_event_time to now.

        Args:
            threshold_seconds: Maximum allowed seconds since last event.

        Returns:
            True if stalled (no events within threshold), False otherwise.
        """
        elapsed = time.monotonic() - self._state.last_event_time
        return elapsed > threshold_seconds

    def get_state(self) -> PrdMonitorState:
        """Return the current monitor state for TUI consumption."""
        return self._state

    def reset(self) -> None:
        """Reset monitor state for a new step or phase."""
        self._state = PrdMonitorState()

    # -------------------------------------------------------------------
    # Internal extraction
    # -------------------------------------------------------------------

    def _extract_from_event(self, event: dict) -> None:
        """Extract signals from a parsed JSON event."""
        # Step ID
        step_id = event.get("step_id", "")
        if step_id:
            self._state.last_step_id = step_id

        # Agent type
        agent_type = event.get("agent_type", "")
        if agent_type:
            self._state.current_agent_type = agent_type

        # Current artifact
        artifact = event.get("artifact", "") or event.get("file", "")
        if artifact:
            self._state.current_artifact = artifact

        # QA verdict from structured event
        verdict = event.get("verdict", "")
        if verdict in ("PASS", "FAIL"):
            self._state.qa_verdict = verdict

        # Fix cycle from structured event
        fix_cycle = event.get("fix_cycle")
        if isinstance(fix_cycle, int):
            self._state.fix_cycle_count = max(
                self._state.fix_cycle_count, fix_cycle
            )

    def _extract_from_text(self, text: str) -> None:
        """Extract signals from text using regex patterns."""
        # Research file completion
        research_matches = _RESEARCH_FILE_PATTERN.findall(text)
        if research_matches:
            self._state.research_files_completed += len(research_matches)
            self._state.current_artifact = research_matches[-1]

        # Synthesis file completion
        synth_matches = _SYNTH_FILE_PATTERN.findall(text)
        if synth_matches:
            self._state.synth_files_completed += len(synth_matches)
            self._state.current_artifact = synth_matches[-1]

        # QA verdict (JSON format)
        verdict_match = _QA_VERDICT_JSON_PATTERN.search(text)
        if verdict_match:
            self._state.qa_verdict = verdict_match.group(1)

        # QA verdict (Markdown format)
        if not verdict_match:
            md_match = _QA_VERDICT_MD_PATTERN.search(text)
            if md_match:
                self._state.qa_verdict = md_match.group(1)

        # Fix cycle counter (JSON)
        cycle_match = _FIX_CYCLE_PATTERN.search(text)
        if cycle_match:
            cycle_num = int(cycle_match.group(1))
            self._state.fix_cycle_count = max(
                self._state.fix_cycle_count, cycle_num
            )

        # Fix cycle counter (text)
        if not cycle_match:
            text_cycle = _FIX_CYCLE_TEXT_PATTERN.search(text)
            if text_cycle:
                cycle_num = int(text_cycle.group(1))
                self._state.fix_cycle_count = max(
                    self._state.fix_cycle_count, cycle_num
                )

        # Agent type
        agent_match = _AGENT_TYPE_PATTERN.search(text)
        if agent_match:
            self._state.current_agent_type = agent_match.group(1)

        # Step ID
        step_match = _STEP_ID_PATTERN.search(text)
        if step_match:
            self._state.last_step_id = step_match.group(1)
