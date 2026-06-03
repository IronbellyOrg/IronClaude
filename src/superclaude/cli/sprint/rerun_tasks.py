"""Sprint rerun-tasks — verb orchestration for granular per-task rerun.

Called by the `commands.py` `@sprint_group.command("rerun-tasks")` Click block
(v4.3.0). This module owns the end-to-end rerun flow for re-executing only the
named failed tasks within a single phase, then merging their results back into
the canonical results directory and tasklist.

The 7-stage orchestration flow owned by `run_rerun_tasks` is:
Acquire lock → Nominate → Extract subset → Walk deps → Stash deliverables →
Flip checkboxes → Run executor → Merge-back → Auto-verify-checkpoints →
Release lock. The merge-back and audit-log mechanics live in `recovery.py`;
this module owns extraction, dependency resolution, checkbox mutation,
deliverable stashing, and the abort/restore safety net.

Conventions mirror canonical `checkpoints.py` and the sibling `recovery.py`
(module docstring with em-dash subtitle, `from __future__ import annotations`
first, alphabetized import groups, section banners, atomic temp-file + replace
writes, `click.ClickException` for operator-facing aborts — never `sys.exit`).
Heavy CLI dependencies (`config.parse_tasklist`, `checkpoints.verify_checkpoint_files`,
`executor.execute_sprint`) are deferred to function-body lazy imports to avoid
module-import-time cycles (researcher 2 §1.7).
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import shutil
import subprocess
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Optional

import click

from .debug_logger import debug_log
from .models import PhaseResult, SprintConfig, TaskResult, TaskStatus
from .recovery import (
    ManualNominator,
    RecoveryBundle,
    RecoveryStatus,
    ReflectReportNominator,
    acquire_recovery_lock,
    compute_tasklist_sha256,
    merge_recovery_bundle,
    release_recovery_lock,
    retry_count_for_task,
    write_recovery_audit_log,
)

_rerun_logger = logging.getLogger("superclaude.sprint.rerun_tasks")

# Module-level typed regex constant (researcher 2 §1.1; TDD §T1 line 24).
# Matches one task block `### T<PP>.<TT> ...` up to (but not including) the next
# task heading or end-of-string. MULTILINE anchors `^` per line; DOTALL lets
# `.` span newlines so a full block body is captured in one match.
TASK_BLOCK_PATTERN: re.Pattern[str] = re.compile(
    r"^### (T\d{2}\.\d{2})\b.*?(?=^### T\d{2}\.\d{2}|\Z)",
    re.MULTILINE | re.DOTALL,
)

# Phase-number extractor: a task ID is ``T<PP>.<TT>`` so the two digits after
# ``T`` are the phase number (T07.11 → 7). Used to name bundle artifacts
# (``phase-Nr-tasklist.md``) and the ``rerun_of: phase-N`` frontmatter field.
_PHASE_FROM_TASK_ID = re.compile(r"^T(\d{2})\.\d{2}$")


def _phase_number_from_task_id(task_id: str) -> int:
    """Return the integer phase number encoded in a ``T<PP>.<TT>`` task ID.

    Raises ``click.ClickException`` for a malformed ID so a typo in ``--tasks``
    surfaces as an operator-facing abort rather than a downstream ``None``.
    """
    match = _PHASE_FROM_TASK_ID.match(task_id)
    if not match:
        raise click.ClickException(
            f"Malformed task ID {task_id!r}: expected T<PP>.<TT> (e.g. T07.11)."
        )
    return int(match.group(1))


# ---------------------------------------------------------------------------
# Section A — Task extraction (regex slice + round-trip parser validation)
# ---------------------------------------------------------------------------


def extract_phase_subset(
    source_path: Path,
    target_task_ids: list[str],
    bundle_dir: Path,
) -> Path:
    """Extract only the target task blocks from a phase tasklist into a bundle.

    Six-step extraction sequence (TDD §T1, lines 21-28):

    1. Read ``source_path`` with ``errors="replace"`` so an encoding glitch in
       one task block cannot abort the whole extraction (researcher 2 §1.6).
    2. Locate every ``### T<PP>.<TT>`` block via the module-level
       ``TASK_BLOCK_PATTERN`` (compiled once, reused per call).
    3. Preserve the verbatim preamble (frontmatter, phase-goal heading,
       dependencies, narrative) by slicing ``content[0:first_match.start()]``.
    4. Keep only the blocks whose T-ID is in ``target_task_ids``, in source
       order, preserving the original T-IDs (no renumbering).
    5. Round-trip validate (TDD line 27): re-parse the assembled slice through
       the same MDTM parser the executor uses and confirm it yields the same
       target tasks the full parse would —
       ``parsed(slice) != parsed(original).filter(target_ids)`` ⇒ ABORT with
       the verbatim message. This catches malformed MDTM before tokens spend.
    6. Capture ``compute_tasklist_sha256(source_path)`` BEFORE writing (so the
       recorded hash reflects pre-extraction state per TDD §T8.1), prepend the
       ``rerun_of`` / ``source_tasklist_sha256`` frontmatter, and atomic-write
       to ``<bundle_dir>/phase-Nr-tasklist.md``.

    Returns the path to the written sub-tasklist.

    Raises:
        click.ClickException: source missing/unreadable, no task blocks found,
            round-trip validation fails, or the bundle write fails — all are
            operator-facing aborts (never ``sys.exit``; researcher 2 §7).
    """
    # Local import: config.parse_tasklist transitively imports models and is a
    # heavy CLI dependency; deferring it here avoids a rerun_tasks ↔ config
    # import cycle at module-load time (researcher 2 §1.7).
    from .config import parse_tasklist

    if not target_task_ids:
        raise click.ClickException(
            "No target task IDs supplied to extract_phase_subset."
        )

    if not source_path.exists():
        raise click.ClickException(
            f"Source tasklist not found: {source_path}. Cannot extract rerun subset."
        )

    try:
        content = source_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise click.ClickException(
            f"Failed to read source tasklist {source_path}: {exc}"
        ) from exc

    matches = list(TASK_BLOCK_PATTERN.finditer(content))
    if not matches:
        raise click.ClickException(
            f"No task blocks (### T<PP>.<TT>) found in {source_path}. "
            "Cannot extract rerun subset."
        )

    target_set = set(target_task_ids)
    preamble = content[0 : matches[0].start()]
    selected_blocks = [m.group(0) for m in matches if m.group(1) in target_set]
    slice_text = preamble + "".join(selected_blocks)

    # Round-trip validation (TDD line 27): compare the parser's view of the
    # slice against the parser's view of the original filtered to the targets.
    parsed_slice_ids = {entry.task_id for entry in parse_tasklist(slice_text)}
    parsed_full_ids = {
        entry.task_id
        for entry in parse_tasklist(content)
        if entry.task_id in target_set
    }
    if parsed_slice_ids != parsed_full_ids:
        raise click.ClickException(
            "Sub-tasklist extraction failed round-trip validation. "
            "Inspect <bundle>/phase-Nr-tasklist.md vs source."
        )

    # SHA captured BEFORE the slice write so it records pre-extraction state
    # (TDD §T8.1 mid-flight-edit detection anchors on this hash).
    source_sha = compute_tasklist_sha256(source_path)
    phase_number = _phase_number_from_task_id(target_task_ids[0])
    out_path = bundle_dir / f"phase-{phase_number}r-tasklist.md"

    rerun_frontmatter = (
        f"rerun_of: phase-{phase_number}\nsource_tasklist_sha256: {source_sha}\n"
    )
    payload = rerun_frontmatter + slice_text

    try:
        bundle_dir.mkdir(parents=True, exist_ok=True)
        tmp = out_path.with_suffix(out_path.suffix + ".tmp")
        tmp.write_text(payload, encoding="utf-8")
        tmp.replace(out_path)
    except OSError as exc:
        raise click.ClickException(
            f"Failed to write rerun sub-tasklist {out_path}: {exc}"
        ) from exc

    debug_log(
        _rerun_logger,
        "extract_phase_subset_complete",
        source=str(source_path),
        bundle=str(out_path),
        target_ids=list(target_task_ids),
        source_sha256=source_sha,
    )
    return out_path


# ---------------------------------------------------------------------------
# Section B — Bundle directory + sub-index construction
# ---------------------------------------------------------------------------

# Phase number embedded in a (rerun or canonical) tasklist filename, e.g.
# ``phase-7r-tasklist.md`` or ``phase-7-tasklist.md`` → 7.
_PHASE_FROM_TASKLIST_NAME = re.compile(r"phase-(\d+)r?-tasklist", re.IGNORECASE)


def build_rerun_bundle_dir(results_dir: Path, override: Optional[Path] = None) -> Path:
    """Create (and atomically claim) the bundle directory for one rerun.

    Per TDD §T2 (line 36) the bundle lives at ``<results_dir>/rerun-<ts>/`` and
    holds ``tasklist-index-Nr.md``, ``phase-Nr-tasklist.md`` and
    ``recovery-bundle.json``. The timestamp uses ``%Y%m%dT%H%M%S`` (no colons,
    filesystem-safe).

    Collision handling (TDD §T8.6): if the timestamped base already exists
    (two reruns within the same second), try ``base-1`` … ``base-9`` in turn;
    if all ten candidates exist, raise ``click.ClickException`` directing the
    operator to ``--bundle-dir``. ``mkdir(exist_ok=False)`` is what atomically
    claims a fresh directory — the first caller to win the name proceeds, any
    racing caller falls through to the next suffix.

    When ``override`` is supplied (operator passed ``--bundle-dir``) it is used
    verbatim (created with ``exist_ok=True`` so pointing at an existing dir is
    allowed) and collision auto-suffixing is skipped.
    """
    if override is not None:
        try:
            override.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise click.ClickException(
                f"Failed to create --bundle-dir {override}: {exc}"
            ) from exc
        return override

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    base = results_dir / f"rerun-{stamp}"
    candidates = [base] + [base.with_name(f"{base.name}-{i}") for i in range(1, 10)]
    for candidate in candidates:
        try:
            candidate.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            continue
        except OSError as exc:
            raise click.ClickException(
                f"Failed to create rerun bundle directory {candidate}: {exc}"
            ) from exc
        debug_log(
            _rerun_logger,
            "build_rerun_bundle_dir",
            bundle_dir=str(candidate),
            results_dir=str(results_dir),
        )
        return candidate

    raise click.ClickException(
        "Bundle directory collision exhausted: 10 attempts. "
        "Use --bundle-dir to override."
    )


def build_sub_index(bundle_dir: Path, sub_tasklist: Path) -> Path:
    """Write the single-phase ``tasklist-index-Nr.md`` for a rerun bundle.

    The executor runs against this sub-index exactly like a normal single-phase
    sprint (TDD §T2 line 38). It mirrors the canonical ``tasklist-index.md``
    shape — a title, a small metadata block, and a ``## Phase Files`` table with
    a ``File`` column — but lists only the one rerun phase. ``discover_phases``
    locates the phase via that ``File`` cell (``PHASE_FILE_PATTERN``, widened in
    v4.3.0 to accept the ``phase-Nr-tasklist.md`` rerun form) and confirms the
    file exists in ``bundle_dir``.

    The parent ``tasklist-index.md`` is never touched (TDD §T2 line 40).

    Args:
        bundle_dir: The rerun bundle directory (sibling of ``sub_tasklist``).
        sub_tasklist: The ``phase-Nr-tasklist.md`` produced by
            ``extract_phase_subset`` — must already exist on disk.

    Returns the path to the written ``tasklist-index-Nr.md``.
    """
    name_match = _PHASE_FROM_TASKLIST_NAME.search(sub_tasklist.name)
    if not name_match:
        raise click.ClickException(
            f"Cannot derive phase number from sub-tasklist name {sub_tasklist.name!r} "
            "(expected phase-Nr-tasklist.md)."
        )
    phase_number = int(name_match.group(1))

    # Best-effort task-ID enumeration for the table's "Task IDs" column. A read
    # failure is non-fatal — the column is informational; discovery keys off the
    # File cell, not the task list.
    try:
        sub_content = sub_tasklist.read_text(encoding="utf-8", errors="replace")
        task_ids = TASK_BLOCK_PATTERN.findall(sub_content)
    except OSError:
        task_ids = []
    task_ids_cell = ", ".join(task_ids) if task_ids else "(see tasklist)"

    out_path = bundle_dir / f"tasklist-index-{phase_number}r.md"
    generated = datetime.now(timezone.utc).isoformat()
    body = (
        f"# TASKLIST INDEX -- Rerun of Phase {phase_number}\n"
        "\n"
        "## Metadata & Artifact Paths\n"
        "\n"
        "| Field | Value |\n"
        "|---|---|\n"
        "| Sprint Name | Granular rerun "
        f"(phase {phase_number}) |\n"
        "| Generator Version | rerun-tasks v4.3.0 |\n"
        f"| Generated | {generated} |\n"
        f"| TASKLIST_ROOT | `{bundle_dir}` |\n"
        "| Total Phases | 1 |\n"
        "\n"
        "## Phase Files\n"
        "\n"
        "| Phase | File | Phase Name | Task IDs |\n"
        "|---|---|---|---|\n"
        f"| {phase_number} | {sub_tasklist.name} | "
        f"Rerun of Phase {phase_number} | {task_ids_cell} |\n"
    )

    try:
        bundle_dir.mkdir(parents=True, exist_ok=True)
        tmp = out_path.with_suffix(out_path.suffix + ".tmp")
        tmp.write_text(body, encoding="utf-8")
        tmp.replace(out_path)
    except OSError as exc:
        raise click.ClickException(
            f"Failed to write rerun sub-index {out_path}: {exc}"
        ) from exc

    debug_log(
        _rerun_logger,
        "build_sub_index",
        sub_index=str(out_path),
        sub_tasklist=str(sub_tasklist),
        phase=phase_number,
        task_count=len(task_ids),
    )
    return out_path


# ---------------------------------------------------------------------------
# Section C — Dependency walker (walk-and-warn + transitive closure)
# ---------------------------------------------------------------------------
#
# DESIGN NOTE (v4.3.0, user-approved 2026-06-02 — supersedes TDD §T3's literal
# "[x]/[ ] in source tasklist" model). Sprint phase tasklists carry NO per-task
# checkboxes (verified across 30+ real tasklists; nothing in the pipeline writes
# them). Dependency completion is therefore read from the authoritative
# persisted record — ``PhaseResult.task_results`` loaded from
# ``phase-N-result.json`` — via each task's ``TaskStatus.is_success``. The
# signature is widened with ``phase_result`` and ``results_dir`` (the "results
# context") so ``run_rerun_tasks``, which holds the loaded ``SprintConfig`` and
# ``PhaseResult``, supplies them. The operator-facing WARN text keeps TDD line
# 52's wording ("which is unchecked") as natural phrasing for "not satisfied".


def walk_dependencies(
    phase_tasklist: Path,
    target_ids: list[str],
    *,
    phase_result: Optional[PhaseResult] = None,
    results_dir: Optional[Path] = None,
    include_transitive: bool = False,
    ignore_deps: bool = False,
) -> tuple[list[str], list[str]]:
    """Resolve and validate the dependency closure for a set of rerun targets.

    Four-step logic (TDD §T3, lines 46-55), results-driven (see DESIGN NOTE):

    1. Read each target's declared ``depends_on`` from the source tasklist via
       the lazily-imported ``config.parse_tasklist``.
    2. For each dependency: satisfied if it is itself being rerun (in
       ``target_ids``) or recorded ``is_success`` in ``phase_result``. An
       unsatisfied same-phase dependency emits the TDD line 52 WARN and ABORTs
       via ``click.ClickException`` unless ``ignore_deps`` is set.
    3. For a cross-phase dependency (different ``T<PP>``), confirm the
       prerequisite phase's checkpoint reports exist via
       ``checkpoints.verify_checkpoint_files`` (best-effort: requires
       ``results_dir``); missing/indeterminate → same WARN/ABORT semantics.
    4. With ``include_transitive``, auto-include unsatisfied dependency tasks up
       to a 50%-of-phase-cost ceiling (cost = summed ``turns_consumed`` from
       ``phase_result``). Exceeding the ceiling ABORTs with a pointer to
       ``sprint run --start N --end N``.

    Returns ``(resolved_target_ids, warnings)`` — ``resolved_target_ids`` is
    ``target_ids`` plus any transitively auto-included tasks; ``warnings`` are
    the non-fatal advisories accumulated (including downgraded aborts under
    ``ignore_deps``).

    Raises:
        click.ClickException: an unsatisfied dependency without ``ignore_deps``,
            or a transitive closure exceeding the 50% cost ceiling.
    """
    # Local import: heavy CLI dependency; deferred to avoid a rerun_tasks ↔
    # config module-import cycle (researcher 2 §1.7).
    from .config import parse_tasklist

    if not target_ids:
        return ([], [])

    this_phase = _phase_number_from_task_id(target_ids[0])

    try:
        source_text = phase_tasklist.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise click.ClickException(
            f"Failed to read phase tasklist {phase_tasklist}: {exc}"
        ) from exc
    entry_by_id = {e.task_id: e for e in parse_tasklist(source_text)}

    result_by_id = {}
    if phase_result is not None:
        result_by_id = {tr.task.task_id: tr for tr in phase_result.task_results}

    target_set = set(target_ids)
    resolved: list[str] = list(target_ids)
    warnings: list[str] = []
    auto_included_cost = 0
    total_cost = (
        sum(tr.turns_consumed for tr in phase_result.task_results)
        if phase_result is not None
        else 0
    )

    def _dependencies_of(task_id: str) -> list[str]:
        # Union of both declared-dependency sources — the parsed source tasklist
        # and the persisted result snapshot — so a dependency recorded in either
        # is checked (the two should agree; union is the safe superset if a
        # format quirk makes one incomplete). Order-preserving, de-duplicated.
        deps: list[str] = []
        entry = entry_by_id.get(task_id)
        if entry is not None:
            deps.extend(entry.dependencies)
        tr = result_by_id.get(task_id)
        if tr is not None:
            deps.extend(tr.task.dependencies)
        seen: set[str] = set()
        return [d for d in deps if not (d in seen or seen.add(d))]

    def _is_satisfied(dep: str) -> Optional[bool]:
        """True=satisfied, False=recorded-but-failed, None=no record/unknown."""
        if dep in target_set:
            return True
        tr = result_by_id.get(dep)
        if tr is not None:
            return tr.status.is_success
        return None

    def _cross_phase_checkpoints_ok(dep_phase: int) -> bool:
        if results_dir is None:
            return False
        # Local import: heavy CLI dependency; deferred to avoid a rerun_tasks ↔
        # checkpoints module-import cycle (researcher 2 §1.7).
        from .checkpoints import verify_checkpoint_files

        try:
            found = sorted(results_dir.glob(f"phase-{dep_phase}-cp*.md"))
        except OSError:
            return False
        if not found:
            return False
        verified = verify_checkpoint_files([(p.name, p) for p in found])
        return all(exists for _name, _path, exists in verified)

    for target_id in target_ids:
        for dep in _dependencies_of(target_id):
            if dep in target_set:
                continue  # being rerun alongside — satisfied by construction
            dep_phase = _phase_number_from_task_id(dep)
            satisfied = _is_satisfied(dep)
            if satisfied is True:
                continue
            if satisfied is None and dep_phase != this_phase:
                # Cross-phase prerequisite: fall back to checkpoint existence.
                if _cross_phase_checkpoints_ok(dep_phase):
                    continue

            warn = (
                f"{target_id} depends on {dep} which is unchecked. "
                "Rerun will likely fail. "
                f"Add {dep} to --tasks, pass --include-transitive, "
                "or pass --ignore-deps."
            )

            if include_transitive:
                dep_tr = result_by_id.get(dep)
                dep_cost = dep_tr.turns_consumed if dep_tr is not None else 0
                if (
                    total_cost > 0
                    and (auto_included_cost + dep_cost) > 0.5 * total_cost
                ):
                    raise click.ClickException(
                        "Transitive closure exceeds 50% cost ceiling — use "
                        f"`superclaude sprint run --start {this_phase} "
                        f"--end {this_phase}` instead."
                    )
                if dep not in resolved:
                    resolved.append(dep)
                    auto_included_cost += dep_cost
                    warnings.append(f"Auto-included transitive dependency {dep}.")
                continue

            if ignore_deps:
                warnings.append(warn)
                continue

            raise click.ClickException(warn)

    debug_log(
        _rerun_logger,
        "walk_dependencies_complete",
        targets=list(target_ids),
        resolved=list(resolved),
        warnings=len(warnings),
        include_transitive=include_transitive,
        ignore_deps=ignore_deps,
    )
    return (resolved, warnings)


# ---------------------------------------------------------------------------
# Section D — Legacy fallback (transcript inspection when phase-N-result.json missing)
# ---------------------------------------------------------------------------
#
# DIVERGENCE NOTE (v4.3.0): the task item suggested lazy-importing
# ``summarizer.extract_phase_signals`` as "the signal-extraction helper", but
# that function returns CONTENT categories (tasks/files/validations/errors), not
# the final-result-line ``is_error`` / ``output_tokens`` fields TDD §T6's
# heuristic requires. So this function parses the transcript's terminal
# ``{"type":"result", ...}`` event directly (matching the real stream-json
# format used across executor/monitor/summarizer) — no unused import.

# Task ID embedded in a transcript filename: ``phase-7-task-T07.11-output.txt``.
_TASK_ID_FROM_TRANSCRIPT = re.compile(r"phase-\d+-task-(T\d{2}\.\d{2})-")


def _classify_transcript(text: str) -> TaskStatus:
    """Apply the TDD §T6 (lines 122-126) classification to one transcript body.

    PASS = clean result with output; FAIL_RECOVERABLE = errored with a transient
    signal (``api_retry`` / ``ConnectionRefused`` / zero output tokens);
    FAIL_TERMINAL = errored with none of those (a genuine failure); INCOMPLETE =
    no terminal result event (killed / truncated mid-task).
    """
    result_event: Optional[dict] = None
    total_output_tokens = 0
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            continue
        if not isinstance(event, dict):
            continue
        message = event.get("message")
        usage = message.get("usage") if isinstance(message, dict) else None
        if usage is None:
            usage = event.get("usage")
        if isinstance(usage, dict) and isinstance(usage.get("output_tokens"), int):
            total_output_tokens += usage["output_tokens"]
        if event.get("type") == "result":
            result_event = event

    if result_event is None:
        return TaskStatus.INCOMPLETE  # killed / truncated — no terminal result

    subtype = str(result_event.get("subtype", ""))
    is_error = bool(result_event.get("is_error")) or subtype.startswith("error")

    if not is_error and total_output_tokens > 0:
        return TaskStatus.PASS

    transient = (
        "api_retry" in text or "ConnectionRefused" in text or total_output_tokens == 0
    )
    if is_error and transient:
        return TaskStatus.FAIL_RECOVERABLE
    if is_error:
        return TaskStatus.FAIL_TERMINAL
    # Not errored but produced no output — treat as incomplete (empty run).
    return TaskStatus.INCOMPLETE


def discover_failed_tasks_from_transcripts(
    results_dir: Path, phase: int
) -> list[tuple[str, TaskStatus]]:
    """Legacy fallback: classify a phase's tasks from on-disk transcripts.

    Used by ``run_rerun_tasks`` when ``phase-N-result.json`` is missing OR has an
    empty ``task_results`` (pre-v4.3.0 sprints; TDD §T6 line 130). Enumerates the
    ``phase-N-task-T<PP>.<TT>-output.txt`` transcripts (only ``-output.txt`` — the
    ``-errors.txt`` sibling carries no terminal result line and would duplicate
    the task ID), parses each terminal result event, and returns the non-PASS
    tasks as ``(task_id, TaskStatus)`` — the rerun candidates. Unreadable
    transcripts are skipped (researcher 2 §1.5), never fatal.
    """
    failed: list[tuple[str, TaskStatus]] = []
    try:
        transcripts = sorted(results_dir.glob(f"phase-{phase}-task-T*-output.txt"))
    except OSError:
        return failed

    for path in transcripts:
        id_match = _TASK_ID_FROM_TRANSCRIPT.search(str(path))
        if id_match is None:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        status = _classify_transcript(text)
        if status is not TaskStatus.PASS:
            failed.append((id_match.group(1), status))

    debug_log(
        _rerun_logger,
        "discover_failed_tasks_from_transcripts",
        results_dir=str(results_dir),
        phase=phase,
        transcripts=len(transcripts),
        failed=len(failed),
    )
    return failed


# ---------------------------------------------------------------------------
# Section E — Checkbox state mutation (flip + restore + finalize)
# ---------------------------------------------------------------------------
#
# DESIGN NOTE (v4.3.0, user-approved) — supersedes TDD §T4's literal checkbox
# model. Sprint phase tasklists have no per-task checkboxes, and NO parser reads
# their frontmatter (both verified). So the load-bearing part of §T4 here is the
# RERUN PROVENANCE block: a uniquely-delimited, YAML-content marker prepended to
# the source tasklist recording the in-flight rerun and, on success, an
# accumulating history. It is an audit / at-a-glance marker (invisible in
# rendered markdown; ignored by parse_tasklist + discover_phases), restorable
# verbatim on abort. The per-task `- [x]`/`- [ ]` flip is applied defensively —
# block-scoped to the task, a no-op when no checkbox is present — so it becomes
# automatically correct if checkbox-emission is added upstream (see Follow-Up).

_RERUN_BLOCK_START = "<!-- SUPERCLAUDE-RERUN"
_RERUN_BLOCK_END = "-->"
# Whole provenance block including trailing newline, for strip/replace.
_RERUN_BLOCK_RE = re.compile(r"<!-- SUPERCLAUDE-RERUN\b.*?-->\n?", re.DOTALL)


def _atomic_write_text(path: Path, text: str) -> None:
    """Write ``text`` to ``path`` via temp-file + replace (researcher 2 §1.6)."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def _audit_log_path(bundle_dir: Path) -> Path:
    """Canonical recovery audit log — sibling of the bundle dir (the results dir).

    Mirrors ``recovery.merge_recovery_bundle``'s ``results_dir/recovery-audit.log``
    (``bundle_dir`` is ``<results_dir>/rerun-<ts>/``, so its parent is results).
    """
    return bundle_dir.parent / "recovery-audit.log"


def _split_rerun_block(content: str) -> tuple[str, str]:
    """Return ``(existing_block_or_empty, content_without_block)``."""
    match = _RERUN_BLOCK_RE.search(content)
    if match is None:
        return ("", content)
    return (match.group(0), content[: match.start()] + content[match.end() :])


def _content_sha256_excluding_rerun_block(path: Path) -> str:
    """SHA256 of the tasklist with the SUPERCLAUDE-RERUN provenance block stripped.

    The §T8.1 mid-flight-edit guard must detect a real *operator* edit while
    ignoring the engine's own provenance write (step 10). Hashing the
    block-stripped content keeps the guard sensitive to task-content changes
    but blind to the rerun marker (R-F6).
    """
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return ""
    _, without_block = _split_rerun_block(content)
    return hashlib.sha256(without_block.encode("utf-8")).hexdigest()


def _normalize_whitespace(text: str) -> str:
    """Deterministically collapse whitespace so cosmetic-only edits hash equal.

    Per-line: collapse every run of intra-line whitespace (spaces, tabs) to a
    single space and strip leading/trailing whitespace (``" ".join(line.split())``).
    Then drop trailing blank lines and join with ``\\n``. Interior blank lines are
    preserved (as empty strings) so structural blank-line *removal* still registers
    as a content change. This is the F-3/CG-2 whitespace-tolerant normalization:
    a trailing-whitespace-only edit (AC-4) normalizes back to the baseline, while a
    material body/deliverable edit (AC-5 same-ID) does not.
    """
    lines = [" ".join(line.split()) for line in text.splitlines()]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def _content_sha256_ws_excluding_rerun_block(path: Path) -> str:
    """Whitespace-normalized SHA256 of the tasklist, rerun-block stripped (F-3/CG-2).

    Identical rerun-block exclusion to ``_content_sha256_excluding_rerun_block`` so
    the two hashes differ ONLY in whitespace tolerance, then hashes the
    ``_normalize_whitespace``-collapsed content. Persisted alongside
    ``tasklist_sha256`` as ``tasklist_sha256_ws`` so the auto-resume DriftAssessor
    can prove a same-ID change after a Tier-0 miss is whitespace-only (keep 0.9
    cosmetic, AC-4) versus material (score <0.8, AC-5). Backward-compatible: a
    result.json written before this field exists simply lacks the key, and drift
    falls back to the conservative <0.8 branch.
    """
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return ""
    _, without_block = _split_rerun_block(content)
    return hashlib.sha256(
        _normalize_whitespace(without_block).encode("utf-8")
    ).hexdigest()


def _extract_history(block_text: str) -> list[str]:
    """Pull the ``  - {...}`` history entry lines out of a prior provenance block."""
    history: list[str] = []
    in_history = False
    for line in block_text.splitlines():
        if line.strip() == "rerun_history:":
            in_history = True
            continue
        if in_history:
            if line.startswith("  - "):
                history.append(line)
            elif line.strip() and line.strip() != _RERUN_BLOCK_END:
                in_history = False
    return history


def _id_list(ids: list[str]) -> str:
    return "[" + ", ".join(ids) + "]"


def _render_rerun_block(*, in_progress: Optional[dict], history: list[str]) -> str:
    lines = [_RERUN_BLOCK_START]
    if in_progress is not None:
        lines.append("rerun_in_progress:")
        lines.append(f"  tasks: {_id_list(in_progress['tasks'])}")
        lines.append(f"  bundle: {in_progress['bundle']}")
        lines.append(f"  started_at: {in_progress['started_at']}")
    if history:
        lines.append("rerun_history:")
        lines.extend(history)
    lines.append(_RERUN_BLOCK_END)
    return "\n".join(lines) + "\n"


def _flip_checkbox_in_block(
    content: str, task_id: str, frm: str, to: str
) -> tuple[str, bool]:
    """Flip the first ``- [frm]`` → ``- [to]`` *within* ``task_id``'s block only.

    Anchored to the specific ``### T<id>`` heading and bounded by the next task
    heading (or EOF) so neighbours are never touched. ``re.escape`` on the T-ID
    guards against regex injection from a malformed ID. Returns
    ``(new_content, flipped)``; ``flipped`` is False when the task block or its
    checkbox is absent (the no-op case on real tasklists).
    """
    block_re = re.compile(
        r"(^### " + re.escape(task_id) + r"\b.*?)(?=^### T\d{2}\.\d{2}|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = block_re.search(content)
    if match is None:
        return (content, False)
    block = match.group(1)
    new_block, count = re.subn(r"- \[" + frm + r"\]", f"- [{to}]", block, count=1)
    if count == 0:
        return (content, False)
    return (content[: match.start(1)] + new_block + content[match.end(1) :], True)


def flip_target_checkboxes(
    phase_tasklist: Path, target_ids: list[str], bundle_dir: Path
) -> dict:
    """Mark a rerun in progress on the source tasklist; return restore info.

    Writes a ``rerun_in_progress:`` provenance block (preserving any prior
    ``rerun_history:``) and defensively flips each target's ``- [x]`` → ``- [ ]``
    if present (TDD §T4 line 62-63). Returns the dict ``restore_checkboxes_on_abort``
    needs to revert to the exact pre-rerun state.
    """
    try:
        content = phase_tasklist.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise click.ClickException(
            f"Failed to read phase tasklist {phase_tasklist}: {exc}"
        ) from exc

    prior_block, body = _split_rerun_block(content)
    history = _extract_history(prior_block)

    original_states: dict[str, str] = {}
    for task_id in target_ids:
        body, flipped = _flip_checkbox_in_block(body, task_id, "x", " ")
        original_states[task_id] = "[x]" if flipped else "[ ]"

    started_at = datetime.now(timezone.utc).isoformat()
    block = _render_rerun_block(
        in_progress={
            "tasks": list(target_ids),
            "bundle": str(bundle_dir),
            "started_at": started_at,
        },
        history=history,
    )
    _atomic_write_text(phase_tasklist, block + body)

    write_recovery_audit_log(
        _audit_log_path(bundle_dir),
        {
            "event": "rerun_checkboxes_flipped",
            "tasklist": str(phase_tasklist),
            "tasks": list(target_ids),
            "bundle": str(bundle_dir),
            "started_at": started_at,
        },
    )
    return {
        "original_checkbox_states": original_states,
        "prior_block": prior_block,
        "bundle_dir": str(bundle_dir),
        "phase_tasklist": str(phase_tasklist),
    }


def restore_checkboxes_on_abort(phase_tasklist: Path, restore_info: dict) -> None:
    """Revert the source tasklist to its exact pre-rerun state (TDD §T4 line 65).

    Removes the in-progress provenance block, restores any prior block verbatim,
    and re-checks (``- [ ]`` → ``- [x]``) every task that was originally ``[x]``.
    Idempotent: a second call is a no-op once state is restored.
    """
    try:
        content = phase_tasklist.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise click.ClickException(
            f"Failed to read phase tasklist {phase_tasklist}: {exc}"
        ) from exc

    _current_block, body = _split_rerun_block(content)
    for task_id, original in restore_info.get("original_checkbox_states", {}).items():
        if original == "[x]":
            body, _ = _flip_checkbox_in_block(body, task_id, " ", "x")

    prior_block = restore_info.get("prior_block", "")
    _atomic_write_text(phase_tasklist, (prior_block or "") + body)

    bundle_dir = Path(restore_info.get("bundle_dir", phase_tasklist.parent))
    write_recovery_audit_log(
        _audit_log_path(bundle_dir),
        {
            "event": "rerun_checkboxes_restored",
            "tasklist": str(phase_tasklist),
            "restored": [
                tid
                for tid, st in restore_info.get("original_checkbox_states", {}).items()
                if st == "[x]"
            ],
        },
    )


def finalize_checkboxes_on_success(
    phase_tasklist: Path, target_ids: list[str], bundle_dir: Path
) -> None:
    """Finalize a successful rerun on the source tasklist (TDD §T4 line 64).

    Re-checks the finalized tasks (defensive ``- [ ]`` → ``- [x]``) and moves the
    in-progress record into an accumulating ``rerun_history:`` entry stamped with
    a completion timestamp.
    """
    try:
        content = phase_tasklist.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise click.ClickException(
            f"Failed to read phase tasklist {phase_tasklist}: {exc}"
        ) from exc

    prior_block, body = _split_rerun_block(content)
    history = _extract_history(prior_block)

    for task_id in target_ids:
        body, _ = _flip_checkbox_in_block(body, task_id, " ", "x")

    completed_at = datetime.now(timezone.utc).isoformat()
    history.append(
        f"  - {{tasks: {_id_list(list(target_ids))}, "
        f"bundle: {bundle_dir}, completed_at: {completed_at}}}"
    )
    block = _render_rerun_block(in_progress=None, history=history)
    _atomic_write_text(phase_tasklist, block + body)

    write_recovery_audit_log(
        _audit_log_path(bundle_dir),
        {
            "event": "rerun_checkboxes_finalized",
            "tasklist": str(phase_tasklist),
            "tasks": list(target_ids),
            "bundle": str(bundle_dir),
            "completed_at": completed_at,
        },
    )


# ---------------------------------------------------------------------------
# Section F — Stash and restore for partial deliverables
# ---------------------------------------------------------------------------
#
# DIVERGENCE NOTE (v4.3.0): the item said to read deliverable files from the
# tasklist's "### Acceptance Criteria" via parse_tasklist. Verified: (a)
# acceptance-criteria bullets are grep-assertions, not files; the real
# deliverable FILES live under `**Artifacts (Intended Paths):**`; (b) TaskEntry
# exposes no deliverables/artifacts field, so parse_tasklist cannot surface
# them; (c) the given signature has no tasklist path. So the signature is
# widened with `source_tasklist` (supplied by run_rerun_tasks via
# `phase_obj.file`) and artifact bullets are parsed directly. The reliably
# present results artifacts (`phase-N-task-T*-*`) are always stashed; declared
# deliverable files are stashed best-effort when the tasklist is provided.

# A `- `path`` artifact bullet whose backticked content is a path (no spaces —
# which naturally excludes the `- `grep ...`` acceptance-criteria command lines).
_ARTIFACT_BULLET_RE = re.compile(r"^\s*-\s+`([^`\s]+)`\s*$", re.MULTILINE)
_ARTIFACTS_SECTION_RE = re.compile(
    r"\*\*Artifacts \(Intended Paths\):\*\*(.*?)(?=\n\*\*|\Z)",
    re.DOTALL,
)


def _declared_deliverables(source_tasklist: Path, task_id: str) -> list[Path]:
    """Best-effort: deliverable file paths declared for ``task_id``.

    Parses the task's block for the ``**Artifacts (Intended Paths):**`` section
    and returns each backticked path (resolved against cwd when relative — the
    pipeline runs from the repo root). Never raises; returns ``[]`` on any read
    or parse failure.
    """
    try:
        content = source_tasklist.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    block_re = re.compile(
        r"(^### " + re.escape(task_id) + r"\b.*?)(?=^### T\d{2}\.\d{2}|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    block_match = block_re.search(content)
    if block_match is None:
        return []
    paths: list[Path] = []
    for section in _ARTIFACTS_SECTION_RE.findall(block_match.group(1)):
        for raw in _ARTIFACT_BULLET_RE.findall(section):
            p = Path(raw)
            paths.append(p if p.is_absolute() else (Path.cwd() / p))
    return paths


def _preserved_dest(preserved_root: Path, canonical: Path, results_dir: Path) -> Path:
    """Map a canonical file to its copy under ``preserved/`` preserving structure."""
    for anchor in (results_dir, Path.cwd()):
        try:
            return preserved_root / canonical.relative_to(anchor)
        except ValueError:
            continue
    return preserved_root / "_abs" / canonical.name


def stash_and_restore_deliverables(
    target_ids: list[str],
    results_dir: Path,
    bundle_dir: Path,
    *,
    source_tasklist: Optional[Path] = None,
) -> None:
    """Stash the target tasks' on-disk artifacts before a rerun (TDD §T8.4).

    Copies (``shutil.copy2`` — preserves mtime/permissions; this is a COPY, not
    a move, so the atomic-rename pattern does not apply) each target's results
    artifacts (``phase-N-task-T*-*``) and, when ``source_tasklist`` is given, its
    declared ``**Artifacts (Intended Paths):**`` deliverable files into
    ``<bundle_dir>/preserved/`` with an enumerating ``manifest.json`` (indent=2 +
    trailing newline). ``restore_from_bundle`` reverses this on ``--restore`` or
    a mid-rerun abort.
    """
    if not target_ids:
        return
    phase = _phase_number_from_task_id(target_ids[0])
    preserved_root = bundle_dir / "preserved"
    entries: list[dict] = []

    for task_id in target_ids:
        candidates: list[Path] = []
        try:
            candidates.extend(
                sorted(results_dir.glob(f"phase-{phase}-task-{task_id}-*"))
            )
        except OSError:
            pass
        if source_tasklist is not None:
            candidates.extend(_declared_deliverables(source_tasklist, task_id))

        for canonical in candidates:
            try:
                if not canonical.is_file():
                    continue
            except OSError:
                continue
            dest = _preserved_dest(preserved_root, canonical, results_dir)
            try:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(canonical, dest)
            except OSError:
                continue
            entries.append(
                {
                    "task_id": task_id,
                    "canonical": str(canonical),
                    "preserved": str(dest),
                }
            )

    try:
        preserved_root.mkdir(parents=True, exist_ok=True)
        manifest_path = preserved_root / "manifest.json"
        manifest_path.write_text(
            json.dumps({"entries": entries}, indent=2) + "\n", encoding="utf-8"
        )
    except OSError as exc:
        raise click.ClickException(
            f"Failed to write deliverable stash manifest in {preserved_root}: {exc}"
        ) from exc

    write_recovery_audit_log(
        _audit_log_path(bundle_dir),
        {
            "event": "deliverables_stashed",
            "tasks": list(target_ids),
            "bundle": str(bundle_dir),
            "stashed": len(entries),
        },
    )
    debug_log(
        _rerun_logger,
        "stash_and_restore_deliverables",
        bundle=str(bundle_dir),
        stashed=len(entries),
    )


def restore_from_bundle(bundle_dir: Path, results_dir: Path) -> int:
    """Restore stashed deliverables from ``bundle_dir`` (the ``--restore`` path).

    Reads ``<bundle_dir>/preserved/manifest.json`` and copies each preserved file
    back to its canonical location. Returns the number of files restored. Missing
    manifest or unreadable entries degrade gracefully (researcher 2 §1.5).
    """
    manifest_path = bundle_dir / "preserved" / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return 0

    restored = 0
    for entry in manifest.get("entries", []):
        preserved = Path(entry.get("preserved", ""))
        canonical = Path(entry.get("canonical", ""))
        if not preserved or not canonical:
            continue
        try:
            if not preserved.is_file():
                continue
            canonical.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(preserved, canonical)
            restored += 1
        except OSError:
            continue

    write_recovery_audit_log(
        _audit_log_path(bundle_dir),
        {
            "event": "deliverables_restored",
            "bundle": str(bundle_dir),
            "restored": restored,
        },
    )
    debug_log(
        _rerun_logger,
        "restore_from_bundle",
        bundle=str(bundle_dir),
        restored=restored,
    )
    return restored


def most_recent_bundle(results_dir: Path) -> Optional[Path]:
    """Newest ``rerun-*`` bundle dir under ``results_dir`` (for ``--restore``)."""
    try:
        bundles = sorted(
            (p for p in results_dir.glob("rerun-*") if p.is_dir()), reverse=True
        )
    except OSError:
        return None
    return bundles[0] if bundles else None


# ---------------------------------------------------------------------------
# Section F2 — Default task nomination (FAIL_RECOVERABLE auto-pick)
# ---------------------------------------------------------------------------


def select_default_recoverable_tasks(phase_result_json: Path) -> list[str]:
    """Task IDs to rerun when ``--tasks`` is omitted (TDD Open-Question #3, line 256).

    ``rerun-tasks`` without an explicit ``--tasks`` defaults to only the
    ``FAIL_RECOVERABLE`` tasks of the named phase. Reads the serialized
    ``PhaseResult`` at ``phase_result_json`` and returns the T-IDs whose
    serialized ``status`` is ``"fail_recoverable"`` (the wire value of
    ``TaskStatus.FAIL_RECOVERABLE``; the JSON holds strings, not enum members).

    Pure / side-effect-free. A missing or unreadable/empty JSON returns ``[]`` —
    the caller then falls back to ``discover_failed_tasks_from_transcripts``.
    The task ID is read from the nested ``task.task_id`` produced by
    ``TaskResult.to_dict`` (with a flat ``task_id`` fallback for robustness).
    """
    try:
        data = json.loads(phase_result_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []

    recoverable: list[str] = []
    for entry in data.get("task_results", []) if isinstance(data, dict) else []:
        if not isinstance(entry, dict) or entry.get("status") != "fail_recoverable":
            continue
        task = entry.get("task")
        task_id = (
            task.get("task_id") if isinstance(task, dict) else entry.get("task_id")
        )
        if task_id:
            recoverable.append(task_id)
    return recoverable


# ---------------------------------------------------------------------------
# Section G — Orchestration entrypoint (called from commands.py Click block)
# ---------------------------------------------------------------------------
#
# DIVERGENCE NOTES (v4.3.0), verified against source for Step 3.9:
#  * `execute_sprint(config)` returns None and runs off `config.active_phases`
#    (derived from `config.phases`) — NOT re-discovered from `index_path`. So
#    the sub-config replaces `phases` (re-discovered from the sub-index, with
#    the original phase's execution_mode preserved), `release_dir` (→ bundle,
#    for results isolation), and `start_phase`/`end_phase` (→ the one phase).
#    Rerun success is then read back from the bundle's phase-N-result.json.
#  * walk_dependencies / retry_count_for_task are fed a reconstructed
#    PhaseResult view (real TaskResult.from_dict objects + recovery_history).
#  * R-F6 (SHA mid-flight-edit) is step 12; R-F7 (retry-cap-3) is step 8.


def _load_phase_result_view(phase_result_json: Path) -> SimpleNamespace:
    """Reconstruct a PhaseResult-like view from a phase-N-result.json on disk.

    Provides the two attributes the rerun engine consumes: ``task_results``
    (real ``TaskResult`` objects via ``from_dict`` so ``status.is_success`` /
    ``turns_consumed`` / ``task.dependencies`` all work) and ``recovery_history``
    (raw list for ``retry_count_for_task``). Degrades to empty on any failure.
    """
    try:
        data = json.loads(phase_result_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        data = {}
    task_results = []
    for entry in data.get("task_results", []) if isinstance(data, dict) else []:
        try:
            task_results.append(TaskResult.from_dict(entry))
        except (KeyError, ValueError, TypeError):
            continue
    history = data.get("recovery_history", []) if isinstance(data, dict) else []
    return SimpleNamespace(task_results=task_results, recovery_history=history)


def _rerun_targets_passed(phase_result_json: Path, targets: list[str]) -> bool:
    """True iff every ``targets`` task is recorded PASS in the rerun's result JSON."""
    try:
        data = json.loads(phase_result_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    status_by_id = {}
    for entry in data.get("task_results", []) if isinstance(data, dict) else []:
        task = entry.get("task") if isinstance(entry, dict) else None
        tid = task.get("task_id") if isinstance(task, dict) else None
        if tid:
            status_by_id[tid] = entry.get("status")
    return bool(targets) and all(status_by_id.get(t) == "pass" for t in targets)


def _print_investigation_summary(phase_result_json: Path, nominated: list[str]) -> None:
    """Print a human "where to start" pointer derived from phase-N-result.json.

    Serves the operator's quick-investigation need (the audit/at-a-glance intent
    behind the rerun provenance): last PASS task, recoverable candidates, and
    terminal failures — authoritative, drift-free, derived from the result JSON.
    """
    view = _load_phase_result_view(phase_result_json)
    last_pass = ""
    recoverable: list[str] = []
    terminal: list[str] = []
    for tr in view.task_results:
        if tr.status is TaskStatus.PASS:
            last_pass = tr.task.task_id
        elif tr.status is TaskStatus.FAIL_RECOVERABLE:
            recoverable.append(tr.task.task_id)
        elif tr.status is TaskStatus.FAIL_TERMINAL:
            terminal.append(tr.task.task_id)
    click.echo("  investigation pointer (from phase-N-result.json):")
    click.echo(f"    last PASS task : {last_pass or '(none recorded)'}")
    click.echo(f"    recoverable    : {', '.join(recoverable) or '(none)'}")
    click.echo(f"    terminal fails : {', '.join(terminal) or '(none)'}")
    click.echo(f"    nominated      : {', '.join(nominated)}")


def run_rerun_tasks(
    config: SprintConfig,
    *,
    phase: Optional[int],
    tasks: Optional[list[str]],
    from_reflect_report: Optional[Path],
    merge_back: bool,
    dry_run: bool,
    include_transitive: bool,
    ignore_deps: bool,
    force_merge: bool,
    allow_loop: bool,
    no_verify_checkpoints: bool,
    bundle_dir: Optional[Path],
    restore: bool,
) -> int:
    """Orchestrate a granular per-task rerun (15-step sequence; TDD §T1-§T9).

    Returns the process exit code (0 success, non-zero on abort/failure). The
    lock release and abort auto-restore both run in ``finally`` for crash safety.
    """
    if phase is None:
        if from_reflect_report is not None:
            # --from-reflect-report is a v4.3.0 forward-compat stub: the
            # ReflectReportNominator schema co-ships with SprintRunReflect in
            # v4.4.0 (TDD Resolution #2 / Option A). Until then there is no
            # working nomination source for it, so abort honestly rather than
            # surfacing the misleading "--phase is required" contradiction
            # (the --help text advertises reflect-report as an alternative to
            # --phase). Use --phase/--tasks for manual nomination in v4.3.0.
            raise click.ClickException(
                "--from-reflect-report is not available in v4.3.0 "
                "(reflect-report nomination ships with SprintRunReflect in "
                "v4.4.0). Use --phase N --tasks T<PP>.<TT>[,...] to nominate "
                "tasks manually."
            )
        raise click.ClickException("--phase is required for rerun-tasks.")
    phase_obj = next((p for p in config.phases if p.number == phase), None)
    if phase_obj is None:
        raise click.ClickException(f"Phase {phase} not found in {config.index_path}.")

    lock_path: Optional[Path] = None
    restore_info: Optional[dict] = None
    exit_code = 0
    try:
        # Step 1 — acquire the concurrent-recovery lock (TDD §T8.5).
        lock_path = acquire_recovery_lock(config.results_dir, phase)
        debug_log(_rerun_logger, "rerun_step_1_lock", lock=str(lock_path), phase=phase)

        # --restore short-circuit: replay a bundle's stashed deliverables, done.
        if restore:
            target_bundle = bundle_dir or most_recent_bundle(config.results_dir)
            if target_bundle is None:
                raise click.ClickException("No rerun bundle found to --restore from.")
            count = restore_from_bundle(target_bundle, config.results_dir)
            click.echo(f"Restored {count} file(s) from {target_bundle}.")
            return 0

        parent_view = _load_phase_result_view(config.phase_result_json(phase_obj))

        # Step 2 — nominate the task IDs to rerun.
        if from_reflect_report is not None:
            nominated = ReflectReportNominator(from_reflect_report).nominate({})
        elif tasks:
            nominated = ManualNominator(phase, tasks).nominate({})
        else:
            default_ids = select_default_recoverable_tasks(
                config.phase_result_json(phase_obj)
            )
            if not default_ids:  # legacy fallback (pre-v4.3.0 sprint)
                default_ids = [
                    tid
                    for tid, _status in discover_failed_tasks_from_transcripts(
                        config.results_dir, phase
                    )
                ]
            nominated = ManualNominator(phase, default_ids).nominate({})
        if not nominated:
            raise click.ClickException(
                f"No tasks nominated for phase {phase} rerun. Pass --tasks explicitly."
            )
        debug_log(_rerun_logger, "rerun_step_2_nominate", nominated=nominated)

        # Step 3 — echo the equivalent manual command for a reflect-driven run.
        if from_reflect_report is not None:
            click.echo(
                "Equivalent manual command: superclaude sprint rerun-tasks "
                f"--phase {phase} --tasks {','.join(nominated)}"
            )

        # Step 4 — claim a bundle dir + capture the pre-rerun source SHA (T8.1).
        bundle = build_rerun_bundle_dir(config.results_dir, bundle_dir)
        source_sha = _content_sha256_excluding_rerun_block(phase_obj.file)
        debug_log(
            _rerun_logger, "rerun_step_4_bundle", bundle=str(bundle), sha=source_sha
        )

        # Step 5 — extract the target task subset into the bundle (T1).
        sub_tasklist = extract_phase_subset(phase_obj.file, nominated, bundle)

        # Step 6 — resolve + validate dependencies, results-driven (T3).
        resolved, warnings = walk_dependencies(
            phase_obj.file,
            nominated,
            phase_result=parent_view,
            results_dir=config.results_dir,
            include_transitive=include_transitive,
            ignore_deps=ignore_deps,
        )
        for warning in warnings:
            click.echo(f"WARNING: {warning}")

        # Step 7 — dry-run early exit BEFORE any state mutation (TDD line 256).
        if dry_run:
            click.echo(f"[dry-run] Phase {phase} rerun plan:")
            click.echo(f"  nominated         : {', '.join(nominated)}")
            click.echo(f"  resolved (w/ deps): {', '.join(resolved)}")
            click.echo(f"  bundle            : {bundle}")
            click.echo(f"  sub-tasklist      : {sub_tasklist}")
            _print_investigation_summary(config.phase_result_json(phase_obj), nominated)
            return 0

        # Step 8 — retry-cap-3 abort (R-F7 / TDD §T8.2).
        if not allow_loop:
            for tid in resolved:
                if retry_count_for_task(parent_view, tid) >= 3:
                    bundles = sorted(str(b) for b in config.results_dir.glob("rerun-*"))
                    raise click.ClickException(
                        f"Task {tid} has been rerun 3 times. Manual intervention "
                        f"required. Inspect bundles: {bundles}"
                    )

        # Step 9 — stash partial deliverables before mutating anything (T8.4).
        stash_and_restore_deliverables(
            resolved, config.results_dir, bundle, source_tasklist=phase_obj.file
        )

        # Step 10 — write rerun provenance + (defensive) checkbox flip (T4).
        restore_info = flip_target_checkboxes(phase_obj.file, resolved, bundle)

        # Step 11 — build sub-index and run the executor against an ISOLATED
        # sub-config (own results dir = bundle, only the rerun phase active).
        sub_index = build_sub_index(bundle, sub_tasklist)
        from .config import discover_phases  # local: cycle-avoidance (§1.7)
        from .executor import execute_sprint  # local: heavy CLI dependency

        sub_phases = [
            replace(sp, execution_mode=phase_obj.execution_mode)
            for sp in discover_phases(sub_index)
        ]
        sub_config = replace(
            config,
            index_path=sub_index,
            release_dir=bundle,
            phases=sub_phases,
            start_phase=phase,
            end_phase=phase,
        )
        rerun_error: Optional[BaseException] = None
        try:
            execute_sprint(sub_config)
        except (SystemExit, Exception) as exc:  # executor failure → rerun failed
            rerun_error = exc

        sub_phase_obj = sub_phases[0] if sub_phases else phase_obj
        rerun_succeeded = rerun_error is None and _rerun_targets_passed(
            sub_config.phase_result_json(sub_phase_obj), resolved
        )

        if rerun_succeeded and merge_back:
            # Step 12 — re-hash source (R-F6 / T8.1) then merge back.
            current_sha = _content_sha256_excluding_rerun_block(phase_obj.file)
            if current_sha != source_sha and not force_merge:
                raise click.ClickException(
                    "Source tasklist modified since rerun started. Bundle "
                    f"preserved at {bundle}. To force, use --force-merge."
                )
            produced = sorted(
                p for p in (bundle / "results").glob(f"phase-{phase}-*") if p.is_file()
            )
            attempt = 1 + max(
                (retry_count_for_task(parent_view, tid) for tid in resolved),
                default=0,
            )
            recovery = RecoveryBundle(
                bundle_id=bundle.name,
                affected_phase=phase,
                affected_tasks=list(resolved),
                artifacts_produced=produced,
                source_tasklist_sha256=source_sha,
                status=RecoveryStatus.SUCCESS,
                rerun_attempt=attempt,
            )
            # Sidecar: serialize the rerun's refreshed task_results so
            # merge_recovery_bundle step 7 can splice the new statuses into the
            # canonical phase-N-result.json (TASK-SIDECAR-GAP / AC-1). Without it
            # the merge has no replacement results and the canonical per-task status
            # stays stale (fail_recoverable) after a successful rerun.
            if produced:
                _bundle_result = sub_config.phase_result_json(sub_phase_obj)
                if _bundle_result.exists():
                    _bdata = json.loads(_bundle_result.read_text(encoding="utf-8"))
                    _refreshed = [
                        tr
                        for tr in _bdata.get("task_results", [])
                        if tr.get("task", {}).get("task_id") in set(resolved)
                    ]
                    # Only write when the sidecar covers EVERY resolved task: the
                    # merge replaces affected entries with the sidecar, so a partial
                    # sidecar would drop an uncovered task with no replacement (data
                    # loss). Incomplete -> skip the write -> R-F3 preserve (AC-4).
                    _covered = {tr.get("task", {}).get("task_id") for tr in _refreshed}
                    if set(resolved).issubset(_covered):
                        _atomic_write_text(
                            produced[0].parent / "task-results.json",
                            json.dumps(_refreshed, indent=2) + "\n",
                        )
            merge_recovery_bundle(
                recovery, config.index_path, release_dir=config.release_dir
            )
            finalize_checkboxes_on_success(phase_obj.file, resolved, bundle)
            restore_info = None  # finalized — suppress the finally restore
            click.echo(
                f"Rerun merged: {len(resolved)} task(s) re-executed for phase {phase}."
            )
            exit_code = 0
        else:
            # Step 13 — abort before merge: leave restore to the finally block.
            exit_code = 1
            if rerun_error is not None:
                click.echo(f"Rerun failed ({rerun_error}); source restored, no merge.")
            elif not merge_back:
                click.echo(
                    "Rerun complete; --no-merge-back set, results left in bundle."
                )
                exit_code = 0
            else:
                click.echo(
                    "Rerun did not bring all target tasks to PASS; merge skipped."
                )

        # Step 14 — auto-invoke verify-checkpoints --recover (gated; TDD §T9).
        if exit_code == 0 and merge_back and not no_verify_checkpoints:
            try:
                subprocess.run(
                    [
                        "uv",
                        "run",
                        "superclaude",
                        "sprint",
                        "verify-checkpoints",
                        "--recover",
                        "--phase",
                        str(phase),
                        "--quiet",
                    ],
                    check=False,
                )
            except OSError as exc:
                click.echo(f"verify-checkpoints invocation failed: {exc}")

        return exit_code
    finally:
        # Step 15 — abort auto-restore (T8) + ALWAYS release the lock.
        if restore_info is not None:
            try:
                restore_checkboxes_on_abort(phase_obj.file, restore_info)
            except Exception:  # never mask the original error / block lock release
                pass
        if lock_path is not None:
            release_recovery_lock(lock_path)
        debug_log(_rerun_logger, "rerun_step_15_release_lock", phase=phase)
