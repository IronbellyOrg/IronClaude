"""Post-phase summary pipeline (TUI v2 Wave 3, v3.7).

For every completed phase the executor hands a :class:`~.models.Phase`
and its :class:`~.models.PhaseResult` to a :class:`SummaryWorker`, which
spawns a daemon thread that:

1. Re-parses the phase's stream-json output file to extract five
   structured categories — task status, files changed, validation
   evidence, agent reasoning excerpts, and errors — into a
   :class:`PhaseSummary`.
2. Invokes ``claude --print --model claude-haiku-4-5`` (non-interactive,
   30 s timeout) to render a 3-5 sentence narrative. Failure is
   silently swallowed; the summary is still written without the
   narrative section.
3. Writes ``results/phase-<N>-summary.md`` next to the other phase
   artifacts.

All thread bodies are wrapped in a catch-all ``try/except`` so a summary
failure can never abort the running sprint. The internal ``_summaries``
dict is protected by a :class:`threading.Lock` because the worker has a
pool of concurrent writers (unlike the single-writer ``OutputMonitor``).

Spec refs: §3.2 (F8), §6.3 (Haiku subprocess conventions), §6.4 (hook
ordering), §7.6 (PhaseSummary dataclass).
"""

from __future__ import annotations

import json
import logging
import os
import re
import shutil
import subprocess
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

from .models import Phase, PhaseResult, SprintConfig

_logger = logging.getLogger("superclaude.sprint.summarizer")

# Haiku subprocess conventions (Section 6.3).
HAIKU_MODEL = "claude-haiku-4-5"
HAIKU_TIMEOUT_SECONDS = 30
# Environment variables that must be stripped before launching Haiku to
# avoid spawning a recursive Claude Code session when the sprint itself
# is running inside one.
_HAIKU_STRIP_ENV_VARS: tuple[str, ...] = (
    "CLAUDECODE",
    "CLAUDE_CODE_ENTRYPOINT",
)

# Reasoning excerpt window: keep ~3 substantive text blocks of ≤400 chars.
_REASONING_MAX_BLOCKS = 3
_REASONING_MAX_CHARS = 400

# Task status extraction. Tasks are identified in the stream-json by
# their canonical ID; a STATUS marker in nearby text classifies them.
_TASK_ID_RE = re.compile(r"\bT\d{2}\.\d{2}\b")
_STATUS_MARKER_RE = re.compile(
    r"\b(PASS|FAIL|COMPLETE(?:D)?|DONE|BLOCKED|SKIP(?:PED)?)\b", re.IGNORECASE
)

# Validation-evidence heuristics: pytest / make / gate phrasing.
_VALIDATION_EVIDENCE_RE = re.compile(
    r"(?P<label>pytest|make\s+test|gate|lint|ruff|mypy|type[- ]check|verify-sync)"
    r"[^\n]{0,80}?\b(?P<verdict>passed|failed|ok|error|green|red|\d+\s+passed|\d+\s+failed)\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class PhaseSummary:
    """Structured summary of a single completed phase (spec §7.6).

    ``narrative`` is the Haiku-generated prose; empty string when the
    subprocess was unavailable or timed out. ``path`` is set by
    :meth:`PhaseSummarizer.write` to the actual markdown destination
    (``results/phase-<N>-summary.md``) so downstream fanout (tmux
    summary pane, `--no-tmux` notification) does not have to rebuild
    it.
    """

    phase: Phase
    phase_result: PhaseResult
    tasks: list[dict] = field(default_factory=list)
    files_changed: list[dict] = field(default_factory=list)
    validations: list[dict] = field(default_factory=list)
    reasoning_excerpts: list[str] = field(default_factory=list)
    errors: list[dict] = field(default_factory=list)
    narrative: str = ""
    # TUI v2 Wave 4 (v3.7, F9): populated once the markdown file lands.
    path: Optional[Path] = None


# ``PhaseResult`` does not carry a ``output_path_hint`` field; we attach
# it via getattr so existing callers that build :class:`PhaseResult`
# manually keep working. :meth:`summary_path` gracefully degrades when
# the attribute is absent.
def _phase_results_dir(phase_result: PhaseResult, config: SprintConfig) -> Path:
    """Return the ``results/`` dir for the given phase_result."""
    return config.results_dir


# ---------------------------------------------------------------------------
# NDJSON extraction helpers
# ---------------------------------------------------------------------------


def _iter_stream_json(path: Path):
    """Yield parsed NDJSON events from *path*, skipping malformed lines."""
    try:
        with path.open(errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except (json.JSONDecodeError, ValueError):
                    continue
    except (FileNotFoundError, OSError):
        return


def _extract_reasoning_and_task_text(content: list) -> tuple[str, str]:
    """Split an assistant ``content`` list into (reasoning_text, tool_text).

    The reasoning text concatenates every ``type: text`` block; the
    tool-oriented text is unused right now but preserved for potential
    future extraction (kept to a tuple to avoid signature churn).
    """
    reasoning_parts: list[str] = []
    for block in content or []:
        if not isinstance(block, dict):
            continue
        if block.get("type") == "text":
            txt = block.get("text")
            if isinstance(txt, str) and txt.strip():
                reasoning_parts.append(txt.strip())
    return "\n\n".join(reasoning_parts), ""


def _classify_task_status(line: str) -> str:
    """Return a STATUS label for *line* or ``"TOUCHED"`` if only mentioned."""
    m = _STATUS_MARKER_RE.search(line)
    if not m:
        return "TOUCHED"
    raw = m.group(1).upper()
    if raw in ("COMPLETE", "COMPLETED", "DONE"):
        return "PASS"
    if raw in ("SKIP", "SKIPPED"):
        return "SKIPPED"
    return raw


def extract_phase_signals(output_path: Path) -> dict:
    """Scan *output_path* and return the five summary categories.

    Returns a dict with keys ``tasks``, ``files_changed``,
    ``validations``, ``reasoning_excerpts``, and ``errors``. Each value
    is a list of plain dicts (no custom classes) so the summary can be
    trivially serialised to JSON or markdown.
    """
    tasks_by_id: dict[str, dict] = {}
    files_by_path: dict[str, dict] = {}
    validations: list[dict] = []
    reasoning: list[str] = []
    errors: list[dict] = []

    seen_validation: set[tuple[str, str]] = set()
    last_task_id: str = ""
    last_tool_name: str = ""

    for event in _iter_stream_json(output_path):
        etype = event.get("type")
        message = event.get("message") or {}
        content = message.get("content") if isinstance(message, dict) else None

        if etype == "assistant" and isinstance(content, list):
            reasoning_text, _ = _extract_reasoning_and_task_text(content)
            if reasoning_text and len(reasoning) < _REASONING_MAX_BLOCKS:
                reasoning.append(reasoning_text[:_REASONING_MAX_CHARS])

            # Task status heuristic: every T<PP>.<TT> seen in a text
            # block is considered touched; when a status marker shows up
            # on the same line, upgrade the classification.
            for block in content:
                if not isinstance(block, dict):
                    continue
                btype = block.get("type")
                if btype == "text":
                    txt = block.get("text") or ""
                    for line in txt.splitlines():
                        for task_id in _TASK_ID_RE.findall(line):
                            last_task_id = task_id
                            status = _classify_task_status(line)
                            existing = tasks_by_id.get(task_id)
                            # Keep the most informative status we see
                            # (PASS/FAIL/BLOCKED beats TOUCHED).
                            if not existing or (existing["status"] == "TOUCHED" and status != "TOUCHED"):
                                tasks_by_id[task_id] = {
                                    "task_id": task_id,
                                    "status": status,
                                }
                    # Validation evidence.
                    for m in _VALIDATION_EVIDENCE_RE.finditer(txt):
                        key = (m.group("label").lower(), m.group("verdict").lower())
                        if key in seen_validation:
                            continue
                        seen_validation.add(key)
                        validations.append(
                            {
                                "check": m.group("label"),
                                "verdict": m.group("verdict"),
                                "snippet": txt[max(0, m.start() - 20) : m.end() + 20].strip(),
                            }
                        )
                elif btype == "tool_use":
                    name = block.get("name") or ""
                    if name:
                        last_tool_name = name
                    input_ = block.get("input") or {}
                    # File-changing tools: record their target path.
                    if name in ("Edit", "MultiEdit", "Write") and isinstance(input_, dict):
                        fp = input_.get("file_path")
                        if isinstance(fp, str) and fp:
                            files_by_path.setdefault(
                                fp, {"path": fp, "tool": name}
                            )

        elif etype == "user" and isinstance(content, list):
            for block in content:
                if not isinstance(block, dict) or block.get("type") != "tool_result":
                    continue
                is_error = bool(block.get("is_error"))
                raw = block.get("content")
                msg = _flatten(raw)
                if not is_error and _has_nonzero_exit_code(msg):
                    is_error = True
                if not is_error:
                    continue
                errors.append(
                    {
                        "task_id": last_task_id,
                        "tool": last_tool_name,
                        "message": msg[:500],
                    }
                )

    return {
        "tasks": sorted(tasks_by_id.values(), key=lambda d: d["task_id"]),
        "files_changed": sorted(files_by_path.values(), key=lambda d: d["path"]),
        "validations": validations,
        "reasoning_excerpts": reasoning,
        "errors": errors,
    }


_NONZERO_EXIT_CODE_RE = re.compile(
    r"exit[_ ]code[\"']?\s*[:=]\s*([1-9]\d*)", re.IGNORECASE
)


def _has_nonzero_exit_code(text: str) -> bool:
    if not text:
        return False
    return bool(_NONZERO_EXIT_CODE_RE.search(text))


def _flatten(raw: object) -> str:
    """Coerce a tool_result ``content`` payload to a plain string."""
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


# ---------------------------------------------------------------------------
# Haiku subprocess helper (shared with RetrospectiveGenerator)
# ---------------------------------------------------------------------------


def invoke_haiku(prompt: str, *, timeout: float = HAIKU_TIMEOUT_SECONDS) -> str:
    """Run ``claude --print --model <haiku> -p <prompt>`` and return stdout.

    Returns the empty string on any failure (claude not on PATH, non-zero
    exit, timeout, OS error). Never raises. Per Section 6.3:
    - Strip ``CLAUDECODE`` / ``CLAUDE_CODE_ENTRYPOINT`` so we do not
      accidentally launch a nested Claude Code session.
    - ``--max-turns 1 --dangerously-skip-permissions`` keeps the call
      non-interactive.
    - ``stdin=DEVNULL`` so any parent fd is not inherited.
    """
    claude_bin = shutil.which("claude")
    if not claude_bin:
        _logger.debug("invoke_haiku: claude not on PATH — skipping narrative")
        return ""

    env = {k: v for k, v in os.environ.items() if k not in _HAIKU_STRIP_ENV_VARS}
    cmd = [
        claude_bin,
        "--print",
        "--model",
        HAIKU_MODEL,
        "--max-turns",
        "1",
        "--dangerously-skip-permissions",
        "-p",
        prompt,
    ]
    try:
        proc = subprocess.run(
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        _logger.warning("invoke_haiku: timed out after %ds", int(timeout))
        return ""
    except OSError as exc:
        _logger.warning("invoke_haiku: OSError %s", exc)
        return ""

    if proc.returncode != 0:
        _logger.warning(
            "invoke_haiku: exit=%s stderr=%r",
            proc.returncode,
            (proc.stderr or b"")[:200],
        )
        return ""

    try:
        return (proc.stdout or b"").decode("utf-8", errors="replace").strip()
    except Exception as exc:  # noqa: BLE001 - defensive
        _logger.warning("invoke_haiku: decode failed: %s", exc)
        return ""


# ---------------------------------------------------------------------------
# PhaseSummarizer
# ---------------------------------------------------------------------------


def _build_phase_narrative_prompt(summary: PhaseSummary) -> str:
    """Render the structured data to a compact prompt for the Haiku model."""
    p = summary.phase_result
    lines: list[str] = [
        (
            f"Phase {summary.phase.number} ({summary.phase.display_name}) "
            f"finished with status {p.status.value.upper()} in "
            f"{p.duration_display} ({p.turns} turns, "
            f"{p.tokens_in} in / {p.tokens_out} out tokens)."
        ),
        "",
    ]
    if summary.tasks:
        lines.append("Tasks:")
        for t in summary.tasks[:20]:
            lines.append(f"- {t['task_id']}: {t['status']}")
        lines.append("")
    if summary.files_changed:
        lines.append(f"Files changed ({len(summary.files_changed)}):")
        for f in summary.files_changed[:20]:
            lines.append(f"- {f['path']} ({f['tool']})")
        lines.append("")
    if summary.validations:
        lines.append("Validation evidence:")
        for v in summary.validations[:10]:
            lines.append(f"- {v['check']}: {v['verdict']}")
        lines.append("")
    if summary.errors:
        lines.append(f"Errors ({len(summary.errors)}):")
        for e in summary.errors[:10]:
            lines.append(f"- {e['task_id']} {e['tool']}: {e['message'][:120]}")
        lines.append("")
    if summary.reasoning_excerpts:
        lines.append("Reasoning excerpts:")
        for r in summary.reasoning_excerpts[:2]:
            lines.append(f"> {r[:300]}")
        lines.append("")
    lines.append(
        "Write a concise 3-5 sentence narrative summarising what was "
        "accomplished, notable risks, and whether the phase is ready for "
        "the next one. Plain text only, no markdown."
    )
    return "\n".join(lines)


def _render_phase_summary_markdown(summary: PhaseSummary) -> str:
    """Render ``PhaseSummary`` as the ``results/phase-N-summary.md`` body."""
    p = summary.phase_result
    out: list[str] = [
        f"# Phase {summary.phase.number} Summary — {summary.phase.display_name}",
        "",
        f"**Status:** {p.status.value.upper()}  ",
        f"**Duration:** {p.duration_display}  ",
        f"**Turns:** {p.turns}  ",
        f"**Tokens:** in={p.tokens_in} / out={p.tokens_out}  ",
        f"**Output:** {p.output_bytes} bytes  ",
        f"**Files changed:** {p.files_changed}",
        "",
    ]
    if summary.narrative:
        out.extend(["## Narrative", "", summary.narrative.strip(), ""])
    else:
        out.extend(
            ["## Narrative", "", "_Narrative unavailable (Haiku subprocess failed or skipped)._", ""]
        )

    out.append("## Tasks")
    out.append("")
    if summary.tasks:
        out.append("| Task | Status |")
        out.append("|------|--------|")
        for t in summary.tasks:
            out.append(f"| {t['task_id']} | {t['status']} |")
    else:
        out.append("_No task IDs found in phase output._")
    out.append("")

    out.append("## Files Changed")
    out.append("")
    if summary.files_changed:
        for f in summary.files_changed:
            out.append(f"- `{f['path']}` ({f['tool']})")
    else:
        out.append("_None detected._")
    out.append("")

    out.append("## Validation Evidence")
    out.append("")
    if summary.validations:
        for v in summary.validations:
            out.append(f"- **{v['check']}** → {v['verdict']}")
    else:
        out.append("_None detected._")
    out.append("")

    out.append("## Errors")
    out.append("")
    if summary.errors:
        for e in summary.errors:
            task = e["task_id"] or "-"
            tool = e["tool"] or "-"
            msg = e["message"].replace("\n", " ")
            out.append(f"- `{task}` / `{tool}` — {msg}")
    else:
        out.append("_None detected._")
    out.append("")

    return "\n".join(out)


class PhaseSummarizer:
    """Extract + narrate + write a :class:`PhaseSummary` for a phase."""

    def __init__(self, config: SprintConfig):
        self.config = config

    # Hook points intentionally left overridable for tests that want to
    # inject deterministic output without touching the filesystem.
    def extract(self, phase: Phase, phase_result: PhaseResult) -> dict:
        """Parse the NDJSON output file and return the 5 signal lists."""
        output_path = self.config.output_file(phase)
        return extract_phase_signals(output_path)

    def narrate(self, summary: PhaseSummary) -> str:
        """Build prompt + invoke Haiku; return narrative or empty string."""
        prompt = _build_phase_narrative_prompt(summary)
        return invoke_haiku(prompt)

    def write(self, summary: PhaseSummary) -> Path:
        """Serialise ``summary`` to ``results/phase-<N>-summary.md``.

        Stamps ``summary.path`` with the destination so downstream
        consumers (Wave 4 tmux fanout, `--no-tmux` notification) can
        read it without re-deriving the path.
        """
        target = self.config.results_dir / f"phase-{summary.phase.number}-summary.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(_render_phase_summary_markdown(summary))
        summary.path = target
        return target

    def summarize(self, phase: Phase, phase_result: PhaseResult) -> PhaseSummary:
        """Run the full extraction → narrate → write pipeline for a phase.

        Narrative generation failure is silently tolerated; the summary
        file is still written so operators retain the structured report.
        """
        signals = self.extract(phase, phase_result)
        summary = PhaseSummary(
            phase=phase,
            phase_result=phase_result,
            tasks=list(signals.get("tasks", [])),
            files_changed=list(signals.get("files_changed", [])),
            validations=list(signals.get("validations", [])),
            reasoning_excerpts=list(signals.get("reasoning_excerpts", [])),
            errors=list(signals.get("errors", [])),
        )
        try:
            summary.narrative = self.narrate(summary)
        except Exception as exc:  # noqa: BLE001 - narrative must never abort
            _logger.warning(
                "PhaseSummarizer: narrative step raised %s for phase %d",
                exc,
                phase.number,
            )
            summary.narrative = ""
        try:
            self.write(summary)
        except Exception as exc:  # noqa: BLE001 - write failure must not abort
            _logger.warning(
                "PhaseSummarizer: write step raised %s for phase %d",
                exc,
                phase.number,
            )
        return summary


# ---------------------------------------------------------------------------
# SummaryWorker — daemon thread pool
# ---------------------------------------------------------------------------


class SummaryWorker:
    """Background daemon-thread pool that runs :class:`PhaseSummarizer`.

    One thread per :meth:`submit` call. All access to ``_summaries`` is
    guarded by a :class:`threading.Lock` so concurrent writers do not
    race. The entire thread body is wrapped in a catch-all
    ``try/except`` — summary failures never propagate and never affect
    the calling sprint.

    TUI v2 Wave 4 (v3.7, F9): ``on_summary_ready`` is an optional
    callback fired from within the worker thread (after the summary has
    been committed to the internal dict) so consumers can refresh the
    tmux summary pane or update the ``latest_summary_notification``
    field. The callback is exception-isolated: a raising callback logs
    a warning but never aborts the worker thread.
    """

    def __init__(
        self,
        summarizer: PhaseSummarizer,
        *,
        on_summary_ready: Optional[Callable[[PhaseSummary], None]] = None,
    ):
        self.summarizer = summarizer
        self._summaries: dict[int, PhaseSummary] = {}
        self._lock = threading.Lock()
        self._threads: list[threading.Thread] = []
        self._on_summary_ready = on_summary_ready

    def submit(self, phase: Phase, phase_result: PhaseResult) -> threading.Thread:
        """Spawn a daemon thread that computes a summary for *phase*.

        Returns the thread so tests can ``join()`` deterministically.
        """
        thread = threading.Thread(
            target=self._run,
            args=(phase, phase_result),
            daemon=True,
            name=f"summary-worker-p{phase.number}",
        )
        thread.start()
        self._threads.append(thread)
        return thread

    def _run(self, phase: Phase, phase_result: PhaseResult) -> None:
        try:
            summary = self.summarizer.summarize(phase, phase_result)
            with self._lock:
                self._summaries[phase.number] = summary
        except Exception as exc:  # noqa: BLE001 - sprint-safety boundary
            _logger.warning(
                "SummaryWorker: phase %d summary thread raised %s",
                phase.number,
                exc,
            )
            return
        # Fire the fanout callback after the commit so observers always
        # see a fully-populated summary. Exception-isolated.
        if self._on_summary_ready is not None:
            try:
                self._on_summary_ready(summary)
            except Exception as exc:  # noqa: BLE001 - sprint-safety boundary
                _logger.warning(
                    "SummaryWorker: on_summary_ready callback raised %s for "
                    "phase %d",
                    exc,
                    phase.number,
                )

    def wait(self, timeout: Optional[float] = None) -> None:
        """Block until every submitted thread finishes or *timeout* elapses.

        Threads that fail to finish within ``timeout`` are left running;
        the caller may still read ``get_summaries`` for whatever has
        completed. Individual join deadlines are clipped so the total
        wall-clock wait stays bounded.
        """
        deadline = None if timeout is None else time.monotonic() + timeout
        for t in self._threads:
            if deadline is None:
                t.join()
                continue
            remaining = max(0.0, deadline - time.monotonic())
            t.join(timeout=remaining)

    def get_summaries(self) -> dict[int, PhaseSummary]:
        """Return a thread-safe snapshot of collected summaries."""
        with self._lock:
            return dict(self._summaries)
