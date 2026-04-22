"""Sidecar output monitor — daemon thread that watches output files.

Parses stream-json (NDJSON) output from ``claude --print --output-format stream-json``.
Each line is a JSON object with a ``type`` field.  The monitor extracts task IDs,
tool names, and file-change signals from these events to drive the TUI.
"""

from __future__ import annotations

import json
import logging
import re
import threading
import time
from pathlib import Path

from .config import count_tasks_in_file
from .debug_logger import debug_log
from .models import MonitorState

_dbg = logging.getLogger("superclaude.sprint.debug.monitor")

# Patterns to extract from stringified event content
TASK_ID_PATTERN = re.compile(r"T\d{2}\.\d{2}")
TOOL_PATTERN = re.compile(
    r"\b(Read|Edit|MultiEdit|Write|Grep|Glob|Bash|TodoWrite|TodoRead|Task)\b"
)
FILES_CHANGED_PATTERN = re.compile(
    r"(?:modified|created|edited|wrote|updated)\s+[`'\"]?([^\s`'\"]+\.\w+)"
)

# Pattern for detecting budget exhaustion in NDJSON output
ERROR_MAX_TURNS_PATTERN = re.compile(r'"subtype"\s*:\s*"error_max_turns"')
PROMPT_TOO_LONG_PATTERN = re.compile(r'"Prompt is too long"')


def detect_error_max_turns(output_path: Path) -> bool:
    """Check if the last NDJSON line indicates budget exhaustion.

    Scans the last non-empty line of the output file for the
    ``"subtype":"error_max_turns"`` pattern, which signals that a
    subprocess exhausted its turn budget.

    Returns True if error_max_turns is detected, False otherwise.
    """
    try:
        content = output_path.read_text(errors="replace")
    except (FileNotFoundError, OSError):
        return False

    if not content.strip():
        return False

    # Get last non-empty line
    lines = content.strip().splitlines()
    for line in reversed(lines):
        line = line.strip()
        if line:
            return bool(ERROR_MAX_TURNS_PATTERN.search(line))

    return False


def detect_prompt_too_long(
    output_path: Path, *, error_path: Path | None = None
) -> bool:
    """Check if NDJSON output contains a prompt-too-long error.

    Scans the last 10 non-empty lines of the output file for the
    ``"Prompt is too long"`` pattern, which signals that the subprocess
    context window was exhausted.

    If ``error_path`` is provided, the same last-10-lines scan is also
    applied to that file. Returns True if the pattern is found in either
    file.

    Returns True if the pattern is found, False otherwise.
    """

    def _scan(path: Path) -> bool:
        try:
            content = path.read_text(errors="replace")
        except (FileNotFoundError, OSError):
            return False

        if not content.strip():
            return False

        lines = content.strip().splitlines()
        # Scan last 10 non-empty lines (pattern may not be in the final line)
        count = 0
        for line in reversed(lines):
            line = line.strip()
            if not line:
                continue
            if PROMPT_TOO_LONG_PATTERN.search(line):
                return True
            count += 1
            if count >= 10:
                break
        return False

    if _scan(output_path):
        return True
    if error_path is not None and _scan(error_path):
        return True
    return False


# Pattern for counting assistant message turns in NDJSON output
# Each "assistant" type message represents one turn consumed.
_TURN_INDICATOR_PATTERN = re.compile(r'"type"\s*:\s*"assistant"')


# TUI v2 Wave 1 (v3.7) constants -----------------------------------------
# Activity log ring buffer: last 3 tool calls shown in the TUI (F1).
ACTIVITY_LOG_MAX = 3
# Error ring buffer: last 10 errors stored; TUI shows up to 5 (F4).
ERRORS_MAX = 10
# Truncation cap for the live "Agent:" context line (F5).
ASSISTANT_TEXT_MAX_LEN = 80
# Tool name shortening for the activity stream (F1). Any tool not in this
# map is rendered with its raw name. Intentionally conservative: only
# collapse names that would otherwise blow the activity line width.
TOOL_NAME_SHORTENING: dict[str, str] = {
    "TodoWrite": "Todo",
    "TodoRead": "Todo",
    "ToolSearch": "Search",
    "MultiEdit": "Multi",
    "WebSearch": "Web",
    "WebFetch": "Web",
}


def _shorten_tool_name(name: str) -> str:
    """Return the display name for a tool in the activity stream."""
    return TOOL_NAME_SHORTENING.get(name, name)


# Bash tool results that failed typically include the literal token
# ``exit_code`` followed by a non-zero integer. Detect that case so Bash
# errors are surfaced even when the SDK omits ``is_error: true``.
_NONZERO_EXIT_CODE_RE = re.compile(r'exit[_ ]code["\']?\s*[:=]\s*([1-9]\d*)', re.IGNORECASE)


def _flatten_tool_result_content(raw: object) -> str:
    """Coerce a tool_result ``content`` field to a short message string.

    The SDK may emit either a plain string or a list of content blocks
    (``{"type": "text", "text": "..."}``). Non-text blocks are skipped.
    Returns an empty string when nothing renderable is present.
    """
    if isinstance(raw, str):
        return raw
    if isinstance(raw, list):
        parts: list[str] = []
        for block in raw:
            if isinstance(block, dict):
                text = block.get("text")
                if isinstance(text, str):
                    parts.append(text)
            elif isinstance(block, str):
                parts.append(block)
        return " ".join(parts).strip()
    return ""


def _has_nonzero_exit_code(text: str) -> bool:
    """True if *text* contains a Bash-style ``exit_code`` with non-zero value."""
    if not text:
        return False
    return bool(_NONZERO_EXIT_CODE_RE.search(text))


_CONDENSE_PREFERRED_FIELDS: dict[str, tuple[str, ...]] = {
    "Read": ("file_path",),
    "Edit": ("file_path",),
    "MultiEdit": ("file_path",),
    "Write": ("file_path",),
    "Bash": ("description", "command"),
    "Grep": ("pattern", "path"),
    "Glob": ("pattern", "path"),
    "TodoWrite": (),  # nothing useful to summarise
    "Task": ("description", "subagent_type"),
    "WebFetch": ("url",),
    "WebSearch": ("query",),
}
_CONDENSE_FALLBACK_FIELDS: tuple[str, ...] = (
    "file_path",
    "path",
    "command",
    "pattern",
    "description",
)


def _condense_tool_input(tool_name: str, tool_input: object) -> str:
    """Produce a short human-readable summary of a tool_use input dict.

    Prefers the most identifying field per tool (file_path, command,
    pattern, description). Falls back to the first short string value or
    an empty string. The result is capped at 60 characters so the
    activity line fits inside the TUI active panel.
    """
    if not isinstance(tool_input, dict):
        return ""

    fields = _CONDENSE_PREFERRED_FIELDS.get(tool_name, _CONDENSE_FALLBACK_FIELDS)
    for f in fields:
        value = tool_input.get(f)
        if isinstance(value, str) and value:
            return value[:60]

    # Fallback: first short string value in the dict
    for value in tool_input.values():
        if isinstance(value, str) and 0 < len(value) <= 60:
            return value
    return ""


def count_turns_from_output(output_path: Path) -> int:
    """Extract the number of turns consumed from subprocess NDJSON output.

    Counts lines containing ``"type":"assistant"`` which represent
    individual assistant response turns. Each such line indicates
    one turn was consumed from the budget.

    Args:
        output_path: Path to the subprocess NDJSON output file.

    Returns:
        Number of turns counted. Returns 0 if file is missing or empty.
    """
    try:
        content = output_path.read_text(errors="replace")
    except (FileNotFoundError, OSError):
        return 0

    if not content.strip():
        return 0

    count = 0
    for line in content.splitlines():
        line = line.strip()
        if line and _TURN_INDICATOR_PATTERN.search(line):
            count += 1

    return count


class OutputMonitor:
    """Background thread that watches a stream-json output file.

    Reads incremental bytes, splits on newlines, and parses each complete
    line as JSON.  Partial lines are buffered across poll cycles so no
    data is lost when a write straddles a poll boundary.
    """

    def __init__(self, output_path: Path, poll_interval: float = 0.5):
        self.output_path = output_path
        self.poll_interval = poll_interval
        self.state = MonitorState()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._last_read_pos: int = 0
        self._line_buffer: str = ""
        self._seen_files: set[str] = set()

    def start(self):
        """Start the monitor thread."""
        self._stop_event.clear()
        self._last_read_pos = 0
        self._line_buffer = ""
        self._seen_files.clear()
        # Preserve any pre-populated state from reset() (e.g.
        # total_tasks_in_phase). Callers pattern is reset() then start();
        # clobbering here would drop the TUI v2 pre-scan.
        self._thread = threading.Thread(
            target=self._poll_loop,
            daemon=True,
            name="output-monitor",
        )
        self._thread.start()

    def stop(self):
        """Stop the monitor thread."""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2.0)

    def reset(self, new_output_path: Path, phase_file: Path | None = None):
        """Reset for a new phase (new output file).

        Args:
            new_output_path: Path to the stream-json file for the phase.
            phase_file: Optional path to the phase tasklist. When provided,
                the number of ``### T<PP>.<TT>`` headings is pre-counted
                into ``state.total_tasks_in_phase`` to drive the dual
                progress bar (TUI v2 F3). TUI-Q4 resolution.
        """
        self.output_path = new_output_path
        self._last_read_pos = 0
        self._line_buffer = ""
        self._seen_files.clear()
        new_state = MonitorState()
        if phase_file is not None:
            new_state.total_tasks_in_phase = count_tasks_in_file(phase_file)
        self.state = new_state

    def _poll_loop(self):
        while not self._stop_event.is_set():
            self._poll_once()
            self._stop_event.wait(self.poll_interval)

    def _poll_once(self):
        now = time.monotonic()

        try:
            size = self.output_path.stat().st_size
        except FileNotFoundError:
            return

        self.state.output_bytes_prev = self.state.output_bytes
        self.state.output_bytes = size

        if size > self._last_read_pos:
            # New data available — read incremental chunk
            chunk = self._read_new_chunk(size)
            if chunk:
                self._process_chunk(chunk, now)
        else:
            # No growth — update stall counter
            self.state.stall_seconds = now - self.state.last_event_time

        debug_log(
            _dbg,
            "output_file_stat",
            path=str(self.output_path),
            size=size,
            events_received=self.state.events_received,
            last_event_time=round(self.state.last_event_time, 1),
        )

        # Growth rate: exponential moving average
        delta = self.state.output_bytes - self.state.output_bytes_prev
        alpha = 0.3
        self.state.growth_rate_bps = (
            alpha * (delta / self.poll_interval)
            + (1 - alpha) * self.state.growth_rate_bps
        )

    def _read_new_chunk(self, current_size: int) -> str:
        """Read only the bytes added since last poll."""
        try:
            with open(self.output_path, errors="replace") as f:
                f.seek(self._last_read_pos)
                chunk = f.read(current_size - self._last_read_pos)
                self._last_read_pos = current_size
                return chunk
        except (OSError, UnicodeDecodeError):
            return ""

    def _process_chunk(self, chunk: str, now: float):
        """Split chunk into lines, parse complete NDJSON lines, buffer partials."""
        # Prepend any leftover partial line from previous poll
        data = self._line_buffer + chunk
        lines = data.split("\n")

        # Last element is either "" (if chunk ended with \n) or a partial line
        self._line_buffer = lines[-1]

        # Process all complete lines (everything except the last split element)
        for line in lines[:-1]:
            line = line.strip()
            if not line:
                continue

            # Update liveness on every complete line
            self.state.last_growth_time = now
            self.state.last_event_time = now
            self.state.stall_seconds = 0.0
            self.state.events_received += 1
            self.state.lines_total += 1

            # Try to parse as JSON
            try:
                event = json.loads(line)
            except (json.JSONDecodeError, ValueError):
                # Not valid JSON — still counts as a line for liveness,
                # but try text-mode signal extraction as fallback
                self._extract_signals_from_text(line)
                continue

            self._extract_signals_from_event(event)

    def _extract_signals_from_event(self, event: dict):
        """Extract task IDs, tool names, file paths from a parsed NDJSON event.

        TUI v2 Wave 1 (v3.7) expands this to cover the structured shape
        emitted by ``claude --print --output-format stream-json``:
        - ``type: assistant`` events carry ``message.content`` blocks
          (``thinking`` / ``text`` / ``tool_use``) and ``message.usage``
          token counts. Each such event also counts as one "turn" (F2).
        - ``type: user`` events wrap tool results whose content blocks
          may have ``is_error: true`` (F4).

        All v3.7 extraction is defensive: the regex fallback below still
        runs for task-id and files-changed extraction, so malformed
        events never break existing signal flows.
        """
        event_type = event.get("type", "")
        debug_log(_dbg, "ndjson_line_parsed", event_type=event_type, parsed=True)

        # Tool use events (legacy shape, kept for backward compatibility).
        if event_type == "tool_use":
            tool = event.get("tool", "")
            if tool:
                self.state.last_tool_used = tool

        # TUI v2 Wave 1 (v3.7): structured extraction from the real
        # Anthropic stream-json event shape.
        if event_type == "assistant":
            self._handle_assistant_event(event)
        elif event_type == "user":
            self._handle_user_event(event)

        # Stringify the event for regex-based signal extraction
        # This catches task IDs and file changes regardless of event structure
        text = json.dumps(event, default=str)
        self._extract_signals_from_text(text)

    def _handle_assistant_event(self, event: dict) -> None:
        """Extract F1/F2/F5/F6 signals from a ``type: assistant`` event."""
        # F2: each assistant event is exactly one turn.
        self.state.turns += 1

        message = event.get("message") or {}

        # F6: accumulate token counts. The SDK reports per-turn usage;
        # summing across turns gives the phase total. Cache tokens are
        # intentionally excluded so the displayed "input tokens" reflects
        # the billable/budgeted count.
        usage = message.get("usage") or {}
        in_tokens = usage.get("input_tokens")
        out_tokens = usage.get("output_tokens")
        if isinstance(in_tokens, int) and in_tokens > 0:
            self.state.tokens_in += in_tokens
        if isinstance(out_tokens, int) and out_tokens > 0:
            self.state.tokens_out += out_tokens

        content = message.get("content")
        if not isinstance(content, list):
            return

        for block in content:
            if not isinstance(block, dict):
                continue
            block_type = block.get("type")

            # F5: live "Agent:" context line — keep the tail of the last
            # non-empty text block.
            if block_type == "text":
                text = block.get("text")
                if isinstance(text, str) and text.strip():
                    tail = text.strip().replace("\n", " ")
                    if len(tail) > ASSISTANT_TEXT_MAX_LEN:
                        tail = tail[-ASSISTANT_TEXT_MAX_LEN:]
                    self.state.last_assistant_text = tail

            # F1: activity stream — one entry per tool_use content block.
            elif block_type == "tool_use":
                tool_name = block.get("name") or ""
                if not tool_name:
                    continue
                # Structured tool name extraction supersedes the regex fallback.
                self.state.last_tool_used = tool_name
                display_name = _shorten_tool_name(tool_name)
                summary = _condense_tool_input(tool_name, block.get("input"))
                self._append_activity(display_name, summary)

    def _handle_user_event(self, event: dict) -> None:
        """Extract F4 signals from a ``type: user`` event.

        Tool results are wrapped in user messages. Each ``tool_result``
        content block may carry ``is_error: true`` or, for Bash tools, a
        textual ``exit_code`` != 0. We record up to ERRORS_MAX entries
        as (task_id, tool_name, message) triples — the task_id and
        tool_name fall back to the most recently seen values so the
        error panel can still attribute the failure contextually.
        """
        message = event.get("message") or {}
        content = message.get("content")
        if not isinstance(content, list):
            return

        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") != "tool_result":
                continue

            is_error = bool(block.get("is_error"))
            raw = block.get("content")
            err_message = _flatten_tool_result_content(raw)
            # Bash tools encode failures as exit_code != 0 in the text
            # payload even when is_error is absent. Detect that case.
            if not is_error and _has_nonzero_exit_code(err_message):
                is_error = True
            if not is_error:
                continue

            self._append_error(err_message)

    def _append_activity(self, tool_name: str, description: str) -> None:
        """Push an entry onto the activity log, capping to ACTIVITY_LOG_MAX."""
        entry = (time.monotonic(), tool_name, description)
        self.state.activity_log.append(entry)
        if len(self.state.activity_log) > ACTIVITY_LOG_MAX:
            # Drop oldest; preserves FIFO semantics for the TUI renderer.
            del self.state.activity_log[: len(self.state.activity_log) - ACTIVITY_LOG_MAX]

    def _append_error(self, err_message: str) -> None:
        """Push an error entry onto the ring buffer, capped at ERRORS_MAX."""
        task_id = self.state.last_task_id or ""
        tool_name = self.state.last_tool_used or ""
        truncated = err_message[:200] if err_message else ""
        self.state.errors.append((task_id, tool_name, truncated))
        if len(self.state.errors) > ERRORS_MAX:
            del self.state.errors[: len(self.state.errors) - ERRORS_MAX]

    def _extract_signals_from_text(self, text: str):
        """Extract task IDs, tool names, file paths from text using regex."""
        # Last task ID (take the last match)
        task_matches = TASK_ID_PATTERN.findall(text)
        if task_matches:
            self.state.last_task_id = task_matches[-1]
            debug_log(
                _dbg, "signal_extracted", signal_type="task_id", value=task_matches[-1]
            )

        # Last tool used (only if not already set by structured extraction)
        tool_matches = TOOL_PATTERN.findall(text)
        if tool_matches:
            self.state.last_tool_used = tool_matches[-1]
            debug_log(
                _dbg,
                "signal_extracted",
                signal_type="tool_name",
                value=tool_matches[-1],
            )

        # Files changed (accumulate unique paths)
        file_matches = FILES_CHANGED_PATTERN.findall(text)
        for f in file_matches:
            self._seen_files.add(f)
        self.state.files_changed = len(self._seen_files)
