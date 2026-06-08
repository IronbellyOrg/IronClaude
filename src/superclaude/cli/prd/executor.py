"""PRD pipeline executor -- main orchestration loop.

Implements the PrdExecutor class that drives the 15-step PRD pipeline:
sequential dispatch for Stage A (Steps 1-9), dynamic step generation
for Stage B (Steps 10-14), and final Step 15.

Integrates all Phase 1 (models, gates, inventory, filtering), Phase 2
(prompts, config), and Phase 3 (monitor, process, logging_, diagnostics,
tui) modules.

NFR-PRD.1: Zero ``async def`` or ``await`` in this module.
NFR-PRD.3/F-007: Sentinel detection with ``^EXIT_RECOMMENDATION:``
    anchored regex, skipping code blocks.
NFR-PRD.4: TurnLedger budget guards before every subprocess launch.
NFR-PRD.7: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.
NFR-PRD.9: Signal-aware shutdown with state preservation.
NFR-PRD.11/GAP-004: Context injection for dependent steps.
"""

from __future__ import annotations

import inspect
import json
import re
import signal
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from ._artifact_patterns import (
    INVESTIGATION_FILENAME_RE,
    SYNTHESIS_FILENAME_RE,
    WEB_RESEARCH_FILENAME_RE,
)
from .diagnostics import (
    DiagnosticCollector,
    FailureClassifier,
    ReportGenerator,
)
from .filtering import (
    load_synthesis_mapping,
)
from .gates import GATE_CRITERIA
from .inventory import (
    check_existing_work,
    create_task_dirs,
    select_template,
)
from .logging_ import PrdLogger
from .models import (
    ExistingWorkState,
    PrdConfig,
    PrdPipelineResult,
    PrdStepResult,
    PrdStepStatus,
)
from .monitor import PrdMonitor
from .process import PrdClaudeProcess
from .tui import PrdTUI

# Prompt builders -- imported lazily in _get_prompt_builder to avoid
# pulling all 19 builders into the module namespace upfront.


# ---------------------------------------------------------------------------
# Sentinel detection (NFR-PRD.3 / F-007)
# ---------------------------------------------------------------------------

# Anchored regex: must start at line beginning
_EXIT_SENTINEL_PATTERN = re.compile(
    r"^EXIT_RECOMMENDATION:\s*(CONTINUE|HALT)", re.MULTILINE
)

# Fenced code block detection: ```...```
_CODE_BLOCK_PATTERN = re.compile(r"```[\s\S]*?```")


def _detect_sentinel(output: str) -> Optional[str]:
    """Extract EXIT_RECOMMENDATION from subprocess output.

    F-007: Uses ``^EXIT_RECOMMENDATION:`` anchored regex with
    ``re.MULTILINE``, skipping matches inside fenced code blocks.

    Returns:
        "CONTINUE" or "HALT" if a valid sentinel is found outside
        code blocks, None otherwise.
    """
    # Remove fenced code blocks before searching
    cleaned = _CODE_BLOCK_PATTERN.sub("", output)

    match = _EXIT_SENTINEL_PATTERN.search(cleaned)
    if match:
        return match.group(1)
    return None


# ---------------------------------------------------------------------------
# Stream-JSON text extraction
# ---------------------------------------------------------------------------


def _extract_text_from_stream_json(raw: str) -> str:
    """Extract assistant text content from stream-json (NDJSON) output.

    The subprocess writes NDJSON where assistant messages are nested as:
        {"type":"assistant","message":{"content":[{"type":"text","text":"..."}]}}

    Gate checks and sentinel detection expect plain text, so this function
    parses each line, extracts text blocks from assistant messages, and
    joins them. Falls back to raw content if no text blocks are found
    (e.g. if the output format changes or is already plain text).
    """
    texts: list[str] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            continue

        message = obj.get("message") or {}
        content = message.get("content")
        if not isinstance(content, list):
            continue
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                text = block.get("text", "")
                if text:
                    texts.append(text)

    return "\n".join(texts) if texts else raw


# ---------------------------------------------------------------------------
# Turn ledger (NFR-PRD.4)
# ---------------------------------------------------------------------------


@dataclass
class TurnLedger:
    """Budget tracker for subprocess turn allocation.

    Guards against budget exhaustion by tracking allocated and consumed
    turns across all subprocess launches.
    """

    total_budget: int = 300
    allocated: int = 0
    consumed: int = 0

    def can_allocate(self, turns: int) -> bool:
        """Check if the requested turns can be allocated."""
        return (self.allocated + turns) <= self.total_budget

    def allocate(self, turns: int) -> bool:
        """Allocate turns from the budget. Returns False if insufficient."""
        if not self.can_allocate(turns):
            return False
        self.allocated += turns
        return True

    def consume(self, turns: int) -> None:
        """Record turns actually consumed by a subprocess."""
        self.consumed += turns

    @property
    def remaining(self) -> int:
        """Turns remaining in the budget."""
        return max(self.total_budget - self.allocated, 0)


# ---------------------------------------------------------------------------
# Signal handler (NFR-PRD.9)
# ---------------------------------------------------------------------------


class PrdSignalHandler:
    """Register signal handlers for graceful PRD pipeline shutdown.

    On SIGINT/SIGTERM: set the shutdown flag so the executor loop
    can write resume state and exit gracefully.
    """

    def __init__(self) -> None:
        self.shutdown_requested = False
        self._original_sigint = None
        self._original_sigterm = None

    def install(self) -> None:
        """Install signal handlers."""
        self._original_sigint = signal.getsignal(signal.SIGINT)
        self._original_sigterm = signal.getsignal(signal.SIGTERM)
        signal.signal(signal.SIGINT, self._handle)
        signal.signal(signal.SIGTERM, self._handle)

    def uninstall(self) -> None:
        """Restore original signal handlers."""
        if self._original_sigint is not None:
            signal.signal(signal.SIGINT, self._original_sigint)
        if self._original_sigterm is not None:
            signal.signal(signal.SIGTERM, self._original_sigterm)

    def _handle(self, signum, frame) -> None:
        self.shutdown_requested = True


# ---------------------------------------------------------------------------
# JSON fencing removal
# ---------------------------------------------------------------------------

_JSON_FENCE_PATTERN = re.compile(
    r"```(?:json)?\s*\n(.*?)\n\s*```",
    re.DOTALL,
)


def _strip_json_fencing(text: str) -> str:
    """Extract JSON from text that may include commentary and code fencing.

    LLM subprocesses often include commentary before/after the JSON
    and wrap it in ```json ... ``` blocks.  This extracts the fenced
    content.  If no fence is found, attempts to find a raw JSON object
    starting with '{' as a last resort.
    """
    match = _JSON_FENCE_PATTERN.search(text)
    if match:
        return match.group(1).strip()

    # Fallback: find first '{' ... last '}' as raw JSON
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        return text[start : end + 1].strip()

    return text.strip()


# ---------------------------------------------------------------------------
# Step-to-artifact mapping
# ---------------------------------------------------------------------------

# Maps step IDs to the canonical artifact filename downstream prompt
# builders load from task_dir.  After a successful subprocess step the
# executor searches the working tree for files the subprocess may have
# written via Write/Edit (the subprocess picks its own path), then
# copies the best match to the canonical location.
_STEP_ARTIFACT_FILES: dict[str, str] = {
    "parse-request": "parsed-request.json",
    "scope-discovery": "scope-discovery-raw.md",
    "research-notes": "research-notes.md",
    "sufficiency-review": "sufficiency-review.md",
    # QA steps write their report to qa/; the NDJSON stdout only holds
    # commentary, so gate evaluation must read the report file on disk.
    "research-qa": "qa/qa-research-gate-report.md",
    "synthesis-qa": "qa/qa-synthesis-gate-report.md",
    "structural-qa": "qa/qa-report-validation.md",
    "qualitative-qa": "qa/qa-qualitative-review.md",
}


_STEP_ARTIFACT_PATTERNS: dict[str, list[str]] = {
    "scope-discovery": ["scope-discovery*.md"],  # agent may drop the -raw suffix
    "research-notes": ["research-notes*.md"],
    "sufficiency-review": [],  # stable; exact match
}
# Empty/missing entry → fall back to exact-name behavior.


def _pick_best_candidate(
    candidates: list[tuple[Path, str]], *, preferred_root: Path
) -> str:
    """Stable multi-match tiebreak.

    Priority (INV-006 — freshness MUST outrank raw size, else a stale longer
    file from a prior failed run silently wins over the current output):
      1. Inside preferred_root (task_dir) over external dirs.
      2. Most recently modified (mtime).
      3. Longest content.
      4. Most specific path (fewest parts).
    """
    if not candidates:
        return ""

    def _key(item: tuple[Path, str]) -> tuple[int, float, int, int]:
        path, content = item
        try:
            in_pref = (
                1 if path.resolve().is_relative_to(preferred_root.resolve()) else 0
            )
        except ValueError:
            in_pref = 0
        try:
            mtime = path.stat().st_mtime
        except OSError:
            # Candidate vanished or became unreadable between read_text() and
            # ranking; content is already captured in memory, so treat it as
            # oldest rather than crashing recoverable step recovery.
            mtime = 0.0
        return (in_pref, mtime, len(content), -len(path.parts))

    return max(candidates, key=_key)[1]


def _resolve_step_content(step_id: str, task_dir: Path, ndjson_text: str) -> str:
    """Resolve the best content for gate evaluation and artifact persistence.

    Subprocesses may write their real output to disk via Write/Edit tools
    at unpredictable locations (``task_dir/results/``, ``.dev/``, etc.).
    The NDJSON stdout only captures the assistant's commentary.

    This function searches for files matching the artifact name under
    ``task_dir`` and its parent directory (the project root, where
    subprocesses may write to ``.dev/`` or ``results/``).  Picks the
    largest match and returns it.  Falls back to NDJSON text if no
    disk file is found.
    """
    # Special-case: build-task-file writes to a DYNAMIC filename
    # (TASK-PRD-{product_slug}.md per prompts.py:381), so it cannot
    # live in _STEP_ARTIFACT_FILES (which holds static filenames).
    #
    # IMPORTANT: do NOT add "build-task-file" to _STEP_ARTIFACT_FILES.
    # _persist_step_artifact keys on the same dict and writes
    # gate_content back to task_dir/<artifact_name>. Registering a
    # dict entry would cause it to clobber the LLM-authored task file
    # with gate_content on partial-fail paths.
    #
    # Glob is scoped to task_dir only (not task_dir.parent) because
    # prompts.py:381 writes the task file deterministically into
    # task_dir; widening the search would re-introduce multi-match
    # ambiguity (e.g. from prior failed runs in sibling directories).
    if step_id == "build-task-file":
        best_content = ""
        for match in task_dir.glob("TASK-PRD-*.md"):
            try:
                content = match.read_text(encoding="utf-8", errors="replace")
                if len(content) > len(best_content):
                    best_content = content
            except OSError:
                continue
        if best_content.strip():
            return best_content
        # Fall through to NDJSON fallback if no task file found.

    # Special-case: assembly writes the final PRD to a dynamic path under
    # results/ (or output_path). The NDJSON stdout only holds commentary,
    # so the gate (min_lines=800 + section checks) must read the PRD file.
    if step_id == "assembly":
        best_content = ""
        search_dirs = [task_dir / "results", task_dir, task_dir.parent]
        for d in search_dirs:
            if not d.is_dir():
                continue
            for match in d.glob("*.md"):
                if "-output.txt" in match.name:
                    continue
                # Only a PRD-named file is the assembled PRD. The pipeline
                # always writes the assembled document as PRD_*.md; a bare
                # markdown-heading probe would false-match Stage A artifact
                # files (research-notes.md, sufficiency-review.md, ...)
                # that the executor persists into task_dir.
                if "prd" not in match.name.lower():
                    continue
                try:
                    content = match.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
                if len(content) > len(best_content):
                    best_content = content
            # Skip the broader task_dir / task_dir.parent search once a
            # candidate has been found in an earlier (more specific) dir.
            if best_content:
                break
        if best_content.strip():
            return best_content
        # Fall through to NDJSON if nothing found.

    artifact_name = _STEP_ARTIFACT_FILES.get(step_id)
    if not artifact_name:
        return ndjson_text

    # Search task_dir and its parent (project root) — bounded scope
    # to avoid searching unrelated directories. Layer 2 (INV-005): also
    # add containment-checked WHERE dirs from parsed-request.json so a
    # variant document written into a writable WHERE source dir is still
    # recoverable, without re-introducing unbounded widening.
    search_roots: list[Path] = [task_dir]
    if task_dir.parent.exists():
        search_roots.append(task_dir.parent)

    # Hoisted so the per-candidate containment check below can re-validate every
    # matched file against repo_root regardless of whether parsed-request.json
    # contributed any WHERE roots.
    repo_root = task_dir.parent if task_dir.parent.exists() else task_dir

    parsed_path = task_dir / "parsed-request.json"
    if parsed_path.exists():
        try:
            parsed = json.loads(parsed_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            parsed = {}
        for where in parsed.get("WHERE") or []:
            where_path = repo_root / where
            # realpath containment (INV-005): reject traversal AND symlink escapes
            try:
                real = where_path.resolve(strict=True)
                real.relative_to(repo_root.resolve())
            except (ValueError, OSError):
                continue
            if where_path.is_symlink():  # reject symlinked roots outright
                continue
            if real.is_dir() and real not in search_roots:
                search_roots.append(real)

    patterns = _STEP_ARTIFACT_PATTERNS.get(step_id) or [Path(artifact_name).name]
    candidates: list[tuple[Path, str]] = []
    for root in search_roots:
        if not root.exists():
            continue
        for pattern in patterns:
            for match in root.rglob(pattern):
                if "-output.txt" in match.name or (
                    {"node_modules", ".git", "__pycache__"} & set(match.parts)
                ):
                    continue
                # INV-005 (per-candidate): a matched file may itself be — or sit
                # under — a symlink that escapes repo_root even when its WHERE
                # root was validated. Re-resolve and re-check containment before
                # reading so a symlinked candidate cannot leak content from
                # outside the contained roots.
                try:
                    match.resolve(strict=True).relative_to(repo_root.resolve())
                except (ValueError, OSError):
                    continue
                try:
                    content = match.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
                if content.strip():
                    candidates.append((match, content))

    best_content = _pick_best_candidate(candidates, preferred_root=task_dir)
    # Zero-match (INV-006a/INV-009): best_content == "" → caller falls back to
    # ndjson_text exactly as today (the only non-regressing default).
    return best_content if best_content.strip() else ndjson_text


# ---------------------------------------------------------------------------
# Step definitions
# ---------------------------------------------------------------------------

# Step tuples: (step_id, step_name, prompt_builder_name, is_parallel)
_STAGE_A_STEPS: list[tuple[str, str, str, bool]] = [
    ("check-existing", "Check Existing Work", "_check_existing", False),
    ("parse-request", "Parse Request", "build_parse_request_prompt", False),
    ("scope-discovery", "Scope Discovery", "build_scope_discovery_prompt", False),
    ("research-notes", "Research Notes", "build_research_notes_prompt", False),
    (
        "sufficiency-review",
        "Sufficiency Review",
        "build_sufficiency_review_prompt",
        False,
    ),
    ("template-triage", "Template Triage", "_template_triage", False),
    ("build-task-file", "Build Task File", "build_task_file_prompt", False),
    ("verify-task-file", "Verify Task File", "build_verify_task_file_prompt", False),
    ("preparation", "Preparation", "build_preparation_prompt", False),
]


# ---------------------------------------------------------------------------
# PrdExecutor
# ---------------------------------------------------------------------------


class PrdExecutor:
    """Main PRD pipeline executor.

    Drives the 15-step pipeline through sequential Stage A, dynamic
    parallel Stage B, and final completion step.
    """

    def __init__(self, config: PrdConfig) -> None:
        self._config = config
        self._ledger = TurnLedger(total_budget=config.max_turns)
        self._monitor = PrdMonitor()
        self._logger = PrdLogger(config.task_dir)
        self._diagnostics = DiagnosticCollector(config)
        self._classifier = FailureClassifier()
        self._report_gen = ReportGenerator()
        self._tui = PrdTUI()
        self._signal_handler = PrdSignalHandler()
        self._step_results: list[PrdStepResult] = []
        self._context_summaries: dict[str, str] = {}

    def run(self) -> PrdPipelineResult:
        """Execute the full PRD pipeline.

        Returns:
            PrdPipelineResult with all step outcomes.
        """
        result = PrdPipelineResult(config=self._config)

        # Dry-run mode: validate config only
        if self._config.dry_run:
            result.outcome = "dry_run"
            result.finished_at = datetime.now(timezone.utc)
            return result

        # Install signal handlers (NFR-PRD.9)
        self._signal_handler.install()

        try:
            # Create task directories
            create_task_dirs(self._config.task_dir)

            # Register steps in TUI
            all_step_ids = [(s[0], s[1]) for s in _STAGE_A_STEPS]
            self._tui.register_steps(all_step_ids)
            self._tui.start()

            # Stage A: Sequential steps 1-9
            # Honor resume_from: if set, skip steps before it (their artifacts
            # are assumed present from the prior run). Stage B targets skip
            # all of Stage A.
            resume_from = getattr(self._config, "resume_from", None)
            skip_until_idx = 0
            _stage_a_ids = {s[0] for s in _STAGE_A_STEPS}
            if resume_from:
                if resume_from in _stage_a_ids:
                    for i, (sid, _sn, _b, _p) in enumerate(_STAGE_A_STEPS):
                        if sid == resume_from:
                            skip_until_idx = i
                            break
                else:
                    skip_until_idx = len(_STAGE_A_STEPS)
            for idx, (step_id, step_name, builder_name, _) in enumerate(_STAGE_A_STEPS):
                if idx < skip_until_idx:
                    self._context_summaries[step_id] = (
                        f"{step_id}: skipped (resumed from {resume_from})"
                    )
                    continue
                if self._signal_handler.shutdown_requested:
                    self._handle_shutdown(result)
                    return result

                step_result = self._execute_step(step_id, step_name, builder_name)
                self._step_results.append(step_result)
                result.step_results.append(step_result)

                # Deterministically bind --spec FILES into parsed-request.json
                # right after parse-request persists it and before
                # scope-discovery (the next iteration) reads it. This is the
                # one chokepoint the LLM cannot evict (R3).
                if (
                    step_id == "parse-request"
                    and step_result.status.is_success
                    and self._config.spec_files
                ):
                    self._persist_bound_specs()

                # Halt on any hard execution failure (ERROR/TIMEOUT/
                # QA_FAIL_EXHAUSTED/HALT) regardless of gate tier, OR on a
                # STRICT-gate failure (preserving existing STRICT semantics).
                # The intentional non-fatal STANDARD VALIDATION_FAIL path
                # (exit 0, artifact written) is excluded from is_hard_failure
                # and is STANDARD-tier, so it does not halt here.
                if step_result.status.is_failure:
                    gate = GATE_CRITERIA.get(step_id)
                    strict_gate_fail = bool(
                        gate and gate.enforcement_tier == "STRICT"
                    )
                    if step_result.status.is_hard_failure or strict_gate_fail:
                        result.outcome = "halt"
                        result.halt_step = step_id
                        # Prefer a step-provided reason (e.g. Atom 2's
                        # missing-artifact message) so the specific cause
                        # surfaces at the pipeline level; otherwise fall back
                        # to the generic hard-failure / STRICT-gate template.
                        result.halt_reason = step_result.halt_reason or (
                            f"hard failure: {step_result.status.value}"
                            if step_result.status.is_hard_failure
                            else f"STRICT gate failure: {step_result.status.value}"
                        )
                        break

            # Stage B: Dynamic steps 10-14 (only if Stage A succeeded)
            if result.outcome != "halt":
                self._execute_stage_b(result)

            # Step 15: Completion (only if not halted)
            if result.outcome != "halt":
                if not self._signal_handler.shutdown_requested:
                    completion_result = self._execute_step(
                        "present-complete",
                        "Present & Complete",
                        "build_completion_prompt",
                    )
                    self._step_results.append(completion_result)
                    result.step_results.append(completion_result)

            # Finalize
            if result.outcome != "halt":
                result.outcome = "success"
            result.finished_at = datetime.now(timezone.utc)

        finally:
            self._signal_handler.uninstall()
            self._tui.stop()

        return result

    # -------------------------------------------------------------------
    # Step execution
    # -------------------------------------------------------------------

    def _execute_step(
        self,
        step_id: str,
        step_name: str,
        builder_name: str,
    ) -> PrdStepResult:
        """Execute a single pipeline step."""
        self._logger.log_step_start(step_id, step_name)
        self._tui.update_step(
            step_id, status=PrdStepStatus.RUNNING, gate_state="PENDING"
        )

        start_time = time.monotonic()
        step_result = PrdStepResult(status=PrdStepStatus.RUNNING)

        # Handle internal steps (no subprocess needed)
        if builder_name == "_check_existing":
            step_result = self._run_check_existing()
        elif builder_name == "_template_triage":
            step_result = self._run_template_triage()
        else:
            step_result = self._run_subprocess_step(step_id, step_name, builder_name)

        duration = time.monotonic() - start_time

        # Log completion
        self._logger.log_step_complete(
            step_id,
            step_result.status.value,
            duration_seconds=duration,
            exit_code=step_result.exit_code,
        )

        # Update TUI
        self._tui.update_step(
            step_id,
            status=step_result.status,
            duration=self._format_duration(duration),
        )

        # Record diagnostics
        self._diagnostics.record_step(step_result)

        # Store context summary for dependent steps (NFR-PRD.11/GAP-004)
        self._context_summaries[step_id] = f"{step_id}: {step_result.status.value}"

        return step_result

    def _run_subprocess_step(
        self,
        step_id: str,
        step_name: str,
        builder_name: str,
    ) -> PrdStepResult:
        """Run a step that requires a Claude subprocess."""
        # Budget guard (NFR-PRD.4)
        turns_needed = self._estimate_turns(step_id)
        if not self._ledger.can_allocate(turns_needed):
            return PrdStepResult(
                status=PrdStepStatus.QA_FAIL_EXHAUSTED,
                exit_code=-1,
            )
        self._ledger.allocate(turns_needed)

        # Build prompt. A REQUIRED upstream artifact may be missing (its
        # producer step failed without writing it). The required-read helpers
        # in prompts.py raise MissingArtifactError in that case; catch it here
        # at the real call site (NOT inside _build_prompt, which tests
        # monkeypatch) and convert it to a graceful HALT. HALT is a hard
        # failure (Atom 1), so the Stage-A loop halts the pipeline cleanly
        # instead of letting the exception escape run() as a raw traceback.
        from .prompts import MalformedArtifactError, MissingArtifactError

        try:
            prompt = self._build_prompt(builder_name, step_id=step_id)
        except MissingArtifactError as exc:
            # MalformedArtifactError is a subclass, caught here unchanged; derive
            # the verb so a present-but-corrupt artifact does not read as "missing".
            verb = "malformed" if isinstance(exc, MalformedArtifactError) else "missing"
            return PrdStepResult(
                status=PrdStepStatus.HALT,
                exit_code=-1,
                halt_reason=(
                    f"{verb} required artifact {exc.path.name} "
                    f"(producer: {exc.producer_step})"
                ),
            )

        # Create output files
        output_file = self._config.task_dir / f"{step_id}-output.txt"
        error_file = self._config.task_dir / f"{step_id}-error.txt"

        # Create and launch subprocess
        proc = PrdClaudeProcess(
            config=self._config,
            step_id=step_id,
            prompt=prompt,
            output_file=output_file,
            error_file=error_file,
            timeout_seconds=self._config.stall_timeout * 30,
        )

        try:
            proc.start_with_retry()
            exit_code = proc.wait()
        except RuntimeError:
            return PrdStepResult(
                status=PrdStepStatus.ERROR,
                exit_code=-1,
            )

        # Read output and extract assistant text from NDJSON
        raw_output = ""
        try:
            raw_output = output_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            pass

        output_text = _extract_text_from_stream_json(raw_output) if raw_output else ""

        # Resolve best content: prefer files written to disk by the
        # subprocess over extracted NDJSON commentary.
        #
        # INV-010 (binding contract — do NOT collapse these two channels):
        #   * output_text (NDJSON)  -> _determine_status, for EXIT_RECOMMENDATION/
        #     HALT/CONTINUE sentinel + QA verdict detection. These sentinels live
        #     ONLY in the assistant's stdout commentary, never in the disk artifact.
        #   * gate_content (disk-resolved; NDJSON only as the zero-match fallback)
        #     -> _evaluate_gate (min_lines + semantic_checks) and
        #     _persist_step_artifact (canonical-name write for resume).
        # A future refactor that feeds gate_content into _determine_status (or
        # vice-versa) would silently strip sentinel detection of its input and
        # break HALT/verdict handling. Keep these two inputs independent.
        gate_content = _resolve_step_content(
            step_id, self._config.task_dir, output_text
        )

        # Determine status (uses NDJSON output_text for sentinel detection — INV-010)
        status = self._determine_status(exit_code, output_text, step_id)

        # Gate evaluation (uses resolved disk gate_content — INV-010)
        gate = GATE_CRITERIA.get(step_id)
        if gate and status.is_success:
            gate_passed = self._evaluate_gate(step_id, gate, gate_content)
            if not gate_passed:
                if gate.enforcement_tier == "STRICT":
                    status = PrdStepStatus.HALT
                else:
                    status = PrdStepStatus.VALIDATION_FAIL
                self._tui.update_step(step_id, gate_state="FAIL")
                # R5: make silent degradation loud. When authoritative --spec
                # files were bound but scope-discovery still fails its
                # (non-fatal) STANDARD gate, the run is continuing on a thin
                # foundation despite the operator naming specs. Surface it.
                if step_id == "scope-discovery" and self._bound_spec_paths():
                    self._warn_spec_degradation()
            else:
                self._tui.update_step(step_id, gate_state="PASS")

        # Persist artifact file for downstream steps whenever the
        # subprocess completed (exit 0). STANDARD gate failures don't
        # halt the pipeline, so downstream steps still need the data.
        if exit_code == 0 and gate_content.strip():
            self._persist_step_artifact(step_id, gate_content)

        return PrdStepResult(
            status=status,
            exit_code=exit_code,
            output_bytes=len(raw_output.encode("utf-8", errors="replace")),
        )

    def _determine_status(
        self, exit_code: int, output: str, step_id: str
    ) -> PrdStepStatus:
        """Classify step outcome from exit code and output content.

        NFR-PRD.3/F-007: Sentinel detection with anchored regex,
        code block exclusion.
        """
        # Timeout
        if exit_code == 124:
            return PrdStepStatus.TIMEOUT

        # Crash
        if exit_code != 0:
            return PrdStepStatus.ERROR

        # Sentinel detection (F-007)
        sentinel = _detect_sentinel(output)
        if sentinel == "HALT":
            return PrdStepStatus.HALT
        if sentinel == "CONTINUE":
            return PrdStepStatus.PASS

        # QA steps: check for verdict
        if "qa" in step_id or "review" in step_id:
            if '"verdict": "FAIL"' in output or "verdict: FAIL" in output:
                return PrdStepStatus.QA_FAIL
            if '"verdict": "PASS"' in output or "verdict: PASS" in output:
                return PrdStepStatus.PASS

        # No sentinel found -- pass with caveat
        return PrdStepStatus.PASS_NO_SIGNAL

    def _evaluate_gate(
        self,
        step_id: str,
        gate,
        content: str,
    ) -> bool:
        """Evaluate gate criteria for a step's output."""

        # Check min lines
        if gate.min_lines > 0:
            line_count = len(content.splitlines())
            if line_count < gate.min_lines:
                self._diagnostics.record_gate_failure(
                    step_id,
                    f"Insufficient lines: {line_count} < {gate.min_lines}",
                    gate.enforcement_tier,
                )
                self._logger.log_gate_result(
                    step_id,
                    False,
                    f"Min lines: {line_count}/{gate.min_lines}",
                )
                return False

        # Run semantic checks
        if gate.semantic_checks:
            for check in gate.semantic_checks:
                result = check.check_fn(content)
                if result is not True:
                    msg = result if isinstance(result, str) else check.failure_message
                    self._diagnostics.record_gate_failure(
                        step_id, msg, gate.enforcement_tier
                    )
                    self._logger.log_gate_result(step_id, False, msg)
                    return False

        self._logger.log_gate_result(step_id, True, "All checks passed")
        return True

    # -------------------------------------------------------------------
    # Stage B: Dynamic step generation
    # -------------------------------------------------------------------

    def _execute_stage_b(self, result: PrdPipelineResult) -> None:
        """Execute Stage B: dynamic investigation, QA, synthesis, assembly."""
        if self._signal_handler.shutdown_requested:
            return

        # Resume support: when resuming, skip Stage B sub-stages whose
        # output artifacts already exist on disk. Honors config.resume_from.
        resume_from = getattr(self._config, "resume_from", None)
        stage_b_order = [
            "investigation",
            "research-qa",
            "web-research",
            "synthesis",
            "synthesis-qa",
            "assembly",
            "structural-qa",
            "qualitative-qa",
        ]
        resume_idx = 0
        if resume_from in stage_b_order:
            resume_idx = stage_b_order.index(resume_from)

        def _should_run(substage: str) -> bool:
            return stage_b_order.index(substage) >= resume_idx

        research_dir = self._config.research_dir
        synthesis_dir = self._config.synthesis_dir
        have_investigation = research_dir.is_dir() and any(
            INVESTIGATION_FILENAME_RE.match(p.name) for p in research_dir.glob("*.md")
        )
        have_web = research_dir.is_dir() and any(
            WEB_RESEARCH_FILENAME_RE.match(p.name) for p in research_dir.glob("*.md")
        )
        have_synthesis = synthesis_dir.is_dir() and any(
            SYNTHESIS_FILENAME_RE.match(p.name) for p in synthesis_dir.glob("*.md")
        )

        # Step 10: Investigation (parallel)
        if _should_run("investigation") and not have_investigation:
            investigation_steps = self._build_investigation_steps()
            if investigation_steps:
                self._execute_parallel_steps(
                    investigation_steps, result, "investigation"
                )
                result.research_agent_count = len(investigation_steps)

        # Step 11: Research QA + fix cycle
        if (
            _should_run("research-qa")
            and result.outcome != "halt"
            and not self._signal_handler.shutdown_requested
        ):
            self._execute_qa_fix_cycle(
                result,
                qa_step_id="research-qa",
                qa_builder="build_qa_research_gate_prompt",
                fix_builder="build_gap_filling_prompt",
                max_cycles=self._config.max_research_fix_cycles,
            )

        # Step 12: Web research (parallel, if needed)
        if (
            _should_run("web-research")
            and not have_web
            and result.outcome != "halt"
            and not self._signal_handler.shutdown_requested
        ):
            web_steps = self._build_web_research_steps()
            if web_steps:
                self._execute_parallel_steps(web_steps, result, "web-research")
                result.web_agent_count = len(web_steps)

        # Step 13a: Synthesis (parallel)
        if (
            _should_run("synthesis")
            and not have_synthesis
            and result.outcome != "halt"
            and not self._signal_handler.shutdown_requested
        ):
            synth_steps = self._build_synthesis_steps()
            if synth_steps:
                self._execute_parallel_steps(synth_steps, result, "synthesis")
                result.synthesis_agent_count = len(synth_steps)

        # Step 13b: Synthesis QA + fix cycle
        if (
            _should_run("synthesis-qa")
            and result.outcome != "halt"
            and not self._signal_handler.shutdown_requested
        ):
            self._execute_qa_fix_cycle(
                result,
                qa_step_id="synthesis-qa",
                qa_builder="build_qa_synthesis_gate_prompt",
                fix_builder="build_gap_filling_prompt",
                max_cycles=self._config.max_synthesis_fix_cycles,
            )

        # Step 14a: Assembly
        if (
            _should_run("assembly")
            and result.outcome != "halt"
            and not self._signal_handler.shutdown_requested
        ):
            assembly_result = self._execute_step(
                "assembly", "Assembly", "build_assembly_prompt"
            )
            self._step_results.append(assembly_result)
            result.step_results.append(assembly_result)

            if assembly_result.status.is_failure:
                gate = GATE_CRITERIA.get("assembly")
                if gate and gate.enforcement_tier == "STRICT":
                    result.outcome = "halt"
                    result.halt_step = "assembly"
                    return

        # Step 14b: Structural QA
        if (
            _should_run("structural-qa")
            and result.outcome != "halt"
            and not self._signal_handler.shutdown_requested
        ):
            struct_qa = self._execute_step(
                "structural-qa", "Structural QA", "build_structural_qa_prompt"
            )
            self._step_results.append(struct_qa)
            result.step_results.append(struct_qa)

        # Step 14c: Qualitative QA
        if (
            _should_run("qualitative-qa")
            and result.outcome != "halt"
            and not self._signal_handler.shutdown_requested
        ):
            qual_qa = self._execute_step(
                "qualitative-qa", "Qualitative QA", "build_qualitative_qa_prompt"
            )
            self._step_results.append(qual_qa)
            result.step_results.append(qual_qa)

    def _build_investigation_steps(
        self,
    ) -> list[tuple[str, str, str]]:
        """Generate dynamic investigation steps from research notes.

        F-012: Step count depends on tier:
        - lightweight: 2-3 agents
        - standard: 4-6 agents
        - heavyweight: 6-10 agents
        """
        tier = self._config.tier
        if tier == "lightweight":
            agent_count = 3
        elif tier == "heavyweight":
            agent_count = 8
        else:  # standard
            agent_count = 5

        steps = []
        for i in range(agent_count):
            step_id = f"investigation-{i + 1}"
            step_name = f"Investigation Agent {i + 1}"
            steps.append((step_id, step_name, "build_investigation_prompt"))

        return steps

    def _build_web_research_steps(self) -> list[tuple[str, str, str]]:
        """Generate web research steps based on tier."""
        tier = self._config.tier
        if tier == "lightweight":
            count = 1
        elif tier == "heavyweight":
            count = 3
        else:
            count = 2

        return [
            (
                f"web-research-{i + 1}",
                f"Web Research Agent {i + 1}",
                "build_web_research_prompt",
            )
            for i in range(count)
        ]

    def _build_synthesis_steps(self) -> list[tuple[str, str, str]]:
        """Generate synthesis steps from mapping table."""
        mapping = load_synthesis_mapping(self._config.skill_refs_dir)
        return [
            (
                f"synthesis-{i + 1}",
                f"Synthesis: {entry['synth_file']}",
                "build_synthesis_prompt",
            )
            for i, entry in enumerate(mapping)
        ]

    # -------------------------------------------------------------------
    # Parallel execution
    # -------------------------------------------------------------------

    def _execute_parallel_steps(
        self,
        steps: list[tuple[str, str, str]],
        result: PrdPipelineResult,
        group_name: str,
    ) -> None:
        """Execute steps in parallel via ThreadPoolExecutor.

        NFR-PRD.7: max_workers = min(len(steps), 10).
        Zero-step guard: empty list returns immediately.
        """
        if not steps:
            return

        max_workers = min(len(steps), 10)

        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {}
            for step_id, step_name, builder in steps:
                if self._signal_handler.shutdown_requested:
                    break
                future = pool.submit(self._execute_step, step_id, step_name, builder)
                futures[future] = step_id

            for future in as_completed(futures):
                step_id = futures[future]
                try:
                    step_result = future.result()
                except Exception:
                    step_result = PrdStepResult(
                        status=PrdStepStatus.ERROR,
                        exit_code=-1,
                    )
                self._step_results.append(step_result)
                result.step_results.append(step_result)

    # -------------------------------------------------------------------
    # Fix cycle loop (F-006)
    # -------------------------------------------------------------------

    def _execute_qa_fix_cycle(
        self,
        result: PrdPipelineResult,
        *,
        qa_step_id: str,
        qa_builder: str,
        fix_builder: str,
        max_cycles: int,
    ) -> None:
        """Execute QA -> fix -> re-QA loop.

        F-006: Budget deducted from main TurnLedger. Max cycles
        from config. Budget exhaustion mid-cycle produces
        QA_FAIL_EXHAUSTED with partial results in resume state.
        """
        for cycle in range(max_cycles + 1):  # +1 for initial QA
            if self._signal_handler.shutdown_requested:
                return

            # Budget check before QA
            if not self._ledger.can_allocate(10):
                qa_result = PrdStepResult(
                    status=PrdStepStatus.QA_FAIL_EXHAUSTED,
                    fix_cycle=cycle,
                )
                self._step_results.append(qa_result)
                result.step_results.append(qa_result)
                result.outcome = "halt"
                result.halt_step = qa_step_id
                result.halt_reason = "Budget exhausted during fix cycle"
                return

            # Run QA
            qa_result = self._execute_step(
                qa_step_id,
                f"QA ({qa_step_id}, cycle {cycle})",
                qa_builder,
            )
            self._step_results.append(qa_result)
            result.step_results.append(qa_result)

            self._diagnostics.record_fix_cycle(
                qa_step_id, cycle, qa_result.status.value
            )

            # QA passed -> done
            if qa_result.status.is_success:
                if qa_step_id == "research-qa":
                    result.research_fix_cycles = cycle
                else:
                    result.synthesis_fix_cycles = cycle
                return

            # QA failed but not a fix cycle trigger -> halt
            if not qa_result.status.needs_fix_cycle:
                if qa_result.status.is_failure:
                    gate = GATE_CRITERIA.get(qa_step_id)
                    if gate and gate.enforcement_tier == "STRICT":
                        result.outcome = "halt"
                        result.halt_step = qa_step_id
                        result.halt_reason = f"QA failure: {qa_result.status.value}"
                return

            # Last cycle exhausted -> halt with QA_FAIL_EXHAUSTED
            if cycle >= max_cycles:
                result.outcome = "halt"
                result.halt_step = qa_step_id
                result.halt_reason = "Fix cycles exhausted"
                return

            # Spawn gap-fillers and re-QA
            self._tui.update_step(
                qa_step_id,
                fix_cycle=cycle + 1,
                qa_verdict="FAIL",
            )

            fix_result = self._execute_step(
                f"{qa_step_id}-fix-{cycle + 1}",
                f"Gap Fill ({qa_step_id}, cycle {cycle + 1})",
                fix_builder,
            )
            self._step_results.append(fix_result)
            result.step_results.append(fix_result)

    # -------------------------------------------------------------------
    # Internal steps (no subprocess)
    # -------------------------------------------------------------------

    def _run_check_existing(self) -> PrdStepResult:
        """Step 1: Check for existing PRD work."""
        state = check_existing_work(self._config)

        if state == ExistingWorkState.ALREADY_COMPLETE:
            return PrdStepResult(status=PrdStepStatus.SKIPPED)

        if state == ExistingWorkState.RESUME_STAGE_A:
            self._context_summaries["check-existing"] = (
                "Resuming from Stage A (task dir exists, no research)"
            )

        if state == ExistingWorkState.RESUME_STAGE_B:
            self._context_summaries["check-existing"] = (
                "Resuming from Stage B (research exists, synthesis incomplete)"
            )

        return PrdStepResult(status=PrdStepStatus.PASS)

    def _run_template_triage(self) -> PrdStepResult:
        """Step 6: Select PRD template variant."""
        template_num = select_template(self._config.prd_scope)
        self._context_summaries["template-triage"] = (
            f"Template variant {template_num} selected for scope "
            f"{self._config.prd_scope!r}"
        )
        return PrdStepResult(status=PrdStepStatus.PASS)

    # -------------------------------------------------------------------
    # Prompt building
    # -------------------------------------------------------------------

    def _build_prompt(self, builder_name: str, step_id: str | None = None) -> str:
        """Build a prompt by calling the named builder function.

        NFR-PRD.11/GAP-004: Injects context summaries from prior steps.
        Verbose summaries for direct dependencies, terse for transitive.
        """
        from . import prompts

        builder_fn = getattr(prompts, builder_name, None)
        if builder_fn is None:
            return f"Execute step using builder {builder_name}"

        # Collect context summaries from prior steps
        summaries = list(self._context_summaries.values())

        # Dispatch by introspecting the builder's signature, rather than
        # probing call conventions via exceptions. A dual-mode builder
        # (*args/**kwargs) and a static (config, *, context_summaries=...)
        # builder are distinguished by which keyword params they accept;
        # a VAR_KEYWORD (**kwargs) builder accepts everything. The only
        # guarded call is inspect.signature itself — the builder body is
        # invoked outside the try so a TypeError raised *inside* the
        # builder surfaces as the real bug it is.
        try:
            params = inspect.signature(builder_fn).parameters
        except (TypeError, ValueError):
            return f"Execute step using builder {builder_name} (step={step_id})"

        accepts_var_kw = any(
            p.kind is inspect.Parameter.VAR_KEYWORD for p in params.values()
        )
        call_kwargs: dict = {}
        if accepts_var_kw or "context_summaries" in params:
            call_kwargs["context_summaries"] = summaries if summaries else None
        if accepts_var_kw or "step_id" in params:
            call_kwargs["step_id"] = step_id
        return builder_fn(self._config, **call_kwargs)

    # -------------------------------------------------------------------
    # Shutdown handling (NFR-PRD.9)
    # -------------------------------------------------------------------

    def _handle_shutdown(self, result: PrdPipelineResult) -> None:
        """Handle graceful shutdown: preserve state for resume."""
        result.outcome = "interrupted"
        result.finished_at = datetime.now(timezone.utc)

        # Find last completed step
        completed = [r for r in self._step_results if r.status.is_terminal]
        if completed:
            last = completed[-1]
            last_step = (
                getattr(last.step, "name", "unknown") if last.step else "unknown"
            )
            result.halt_step = last_step
            result.halt_reason = "Signal-interrupted shutdown"

    # -------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------

    def _persist_step_artifact(self, step_id: str, output_text: str) -> None:
        """Write step output to the expected artifact file.

        Downstream prompt builders load artifacts by filename from
        task_dir (e.g. ``parsed-request.json``, ``scope-discovery-raw.md``).
        The subprocess writes to stdout (captured as NDJSON); this method
        persists the extracted text so those files exist on disk.

        For JSON artifacts, strips markdown code fencing if present so
        ``json.loads()`` succeeds downstream.
        """
        artifact_name = _STEP_ARTIFACT_FILES.get(step_id)
        if not artifact_name:
            return

        content = output_text
        if artifact_name.endswith(".json"):
            content = _strip_json_fencing(content)

        artifact_path = self._config.task_dir / artifact_name
        try:
            artifact_path.write_text(content, encoding="utf-8")
        except OSError:
            self._logger.log_step_complete(
                step_id,
                "ARTIFACT_WRITE_FAIL",
                duration_seconds=0,
                exit_code=-1,
            )

    # -------------------------------------------------------------------
    # Spec binding (--spec FILE deterministic ingestion)
    # -------------------------------------------------------------------

    def _bind_specs(self, parsed: dict) -> dict:
        """Force authoritative ``--spec`` files into a parsed-request dict.

        Deterministic, pure-Python, post-LLM, pre-consumer. Adds a Python-owned
        ``SPECS`` array (objects: ``path``, ``size``, ``inlined``,
        ``truncated``) and prepends each spec's parent directory into the
        existing ``WHERE`` array so downstream scope-discovery/investigation
        steps cannot evict the operator's authoritative inputs.

        Idempotent: re-binding produces an identical ``SPECS`` array and never
        duplicates ``WHERE`` entries. No-op (returns *parsed* unchanged) when no
        ``spec_files`` are configured. Mutates and returns *parsed*.
        """
        spec_files = list(self._config.spec_files or [])
        if not spec_files:
            return parsed

        # Dedup duplicate --spec values (order-preserving): identical inputs must
        # not produce duplicate SPECS entries / repeated --file attachments.
        _seen: set[str] = set()
        _deduped: list[str] = []
        for sp in spec_files:
            key = str(Path(sp))
            if key not in _seen:
                _seen.add(key)
                _deduped.append(sp)
        spec_files = _deduped

        specs: list[dict] = []
        parent_dirs: list[str] = []
        for sp in spec_files:
            p = Path(sp)
            try:
                size = p.stat().st_size
            except OSError:
                size = 0
            specs.append(
                {
                    "path": str(p),
                    "size": size,
                    "inlined": False,  # Phase 1: paths-only binding
                    "truncated": False,
                }
            )
            parent = str(p.parent)
            if parent not in parent_dirs:
                parent_dirs.append(parent)

        existing_where = list(parsed.get("WHERE") or [])
        # Prepend spec parent dirs (dedup, order-preserving, idempotent).
        merged_where: list[str] = []
        for d in parent_dirs:
            if d not in existing_where and d not in merged_where:
                merged_where.append(d)
        merged_where.extend(existing_where)

        parsed["SPECS"] = specs
        parsed["WHERE"] = merged_where
        return parsed

    def _persist_bound_specs(self) -> None:
        """Read parsed-request.json, bind specs, and re-persist.

        Called from the Stage-A loop after parse-request persists the artifact
        and before scope-discovery reads it. Fails soft: a missing/corrupt
        artifact or write error leaves the pipeline running on the LLM's
        original WHERE (degraded, but not crashed).
        """
        parsed_path = self._config.task_dir / "parsed-request.json"
        try:
            parsed = json.loads(parsed_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return
        bound = self._bind_specs(parsed)
        try:
            parsed_path.write_text(json.dumps(bound, indent=2) + "\n", encoding="utf-8")
        except OSError:
            return

    def _warn_spec_degradation(self) -> None:
        """Loudly warn when bound specs did not lift scope-discovery past its gate.

        R5: the scope-discovery gate is intentionally STANDARD (non-fatal), so a
        thin scope doc would otherwise let the run continue silently on a weak
        foundation even though the operator named authoritative specs. Surface
        it to stderr and the run log.
        """
        import click

        specs = ", ".join(self._bound_spec_paths())
        message = (
            "WARNING: scope-discovery failed its quality gate even though "
            f"authoritative --spec files were provided ({specs}). The pipeline "
            "is continuing on a thin foundation; verify the agent actually read "
            "each spec in full."
        )
        click.echo(message, err=True)
        self._logger.log_gate_result("scope-discovery", False, message)

    def _bound_spec_paths(self) -> list[str]:
        """Authoritative spec paths for this run: from config, else from the
        persisted SPECS array in parsed-request.json. On `prd resume`, --spec is
        not re-passed, so config.spec_files is empty even though the original run
        bound SPECS; reading the persisted array makes R5 fire on any run path."""
        if self._config.spec_files:
            return list(self._config.spec_files)
        parsed_path = self._config.task_dir / "parsed-request.json"
        try:
            parsed = json.loads(parsed_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        specs = parsed.get("SPECS") or []
        return [s["path"] for s in specs if isinstance(s, dict) and s.get("path")]

    @staticmethod
    def _estimate_turns(step_id: str) -> int:
        """Estimate turns needed for a step (conservative)."""
        # QA and verification steps are lighter
        if "qa" in step_id or "verify" in step_id or "review" in step_id:
            return 10
        # Assembly and task file building are heavier
        if "assembly" in step_id or "build" in step_id:
            return 30
        # Investigation and synthesis are medium
        if "investigation" in step_id or "synthesis" in step_id:
            return 20
        # Default
        return 15

    @staticmethod
    def _format_duration(seconds: float) -> str:
        """Format duration for TUI display."""
        if seconds < 60:
            return f"{seconds:.1f}s"
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m{secs:.0f}s"
