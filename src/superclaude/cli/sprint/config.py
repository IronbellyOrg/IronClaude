"""Sprint configuration — phase discovery, validation, and config loading."""

from __future__ import annotations

import logging
import re
from pathlib import Path

import click

from .models import Phase, SprintConfig, TaskEntry

_logger = logging.getLogger("superclaude.sprint.config")

# Canonical phase filename conventions (case-insensitive):
# 1) phase-1-tasklist.md
# 2) p1-tasklist.md
# 3) phase_1_tasklist.md
# 4) tasklist-p1.md
PHASE_FILE_PATTERN = re.compile(
    r"(?<![A-Za-z0-9])(?:phase-(\d+)-tasklist\.md"
    r"|p(\d+)-tasklist\.md"
    r"|phase_(\d+)_tasklist\.md"
    r"|tasklist-p(\d+)\.md)(?![A-Za-z0-9])",
    re.IGNORECASE,
)

# TUI v2 Wave 1 (v3.7): matches canonical task headings ``### T<PP>.<TT>``.
# Used by count_tasks_in_file for the pre-scan that populates
# SprintConfig.total_tasks (drives the Tasks progress bar, F3).
_TASK_ID_HEADING_RE = re.compile(
    r"^###\s+T\d{2}\.\d{2}\b",
    re.MULTILINE,
)


def count_tasks_in_file(phase_file: Path) -> int:
    """Return the number of ``### T<PP>.<TT>`` task headings in a phase file.

    Used to pre-scan total task count at sprint start (F3, dual progress
    bar) and to populate ``MonitorState.total_tasks_in_phase`` when the
    monitor is reset for a new phase. Missing/unreadable files return 0
    rather than raising — the TUI treats 0 as "progress bar disabled".
    """
    try:
        content = phase_file.read_text(errors="replace")
    except (FileNotFoundError, OSError):
        return 0
    return len(_TASK_ID_HEADING_RE.findall(content))


def discover_phases(index_path: Path) -> list[Phase]:
    """Discover phase files from the index and/or directory.

    Strategy 1: grep the index file for phase file references, also reading
    the optional ``Execution Mode`` column from the phase table.
    Strategy 2: scan the directory for files matching the pattern.
    Deduplicates by phase number, sorts ascending.
    """
    index_dir = index_path.parent
    index_name = index_path.name
    phases: dict[int, Phase] = {}

    # Strategy 1: parse index file
    index_text = index_path.read_text(errors="replace")

    # Try to extract Execution Mode column values from a markdown table that
    # contains a "File" column and optionally an "Execution Mode" column.
    # We build a mapping: filename -> execution_mode
    exec_mode_by_file: dict[str, str] = {}
    _exec_mode_re = re.compile(
        r"^\|(?P<cols>[^\n]+)\|$",
        re.MULTILINE,
    )
    # Locate all pipe-table rows and detect header
    table_rows = [m.group("cols") for m in _exec_mode_re.finditer(index_text)]
    if table_rows:
        # Find the header row that contains "File" (case-insensitive)
        header_idx = None
        for idx, row in enumerate(table_rows):
            cols = [c.strip().lower() for c in row.split("|")]
            if "file" in cols:
                header_idx = idx
                break
        if header_idx is not None:
            header_cols = [c.strip().lower() for c in table_rows[header_idx].split("|")]
            file_col_idx = header_cols.index("file")
            exec_mode_col_idx = (
                header_cols.index("execution mode")
                if "execution mode" in header_cols
                else None
            )
            # Rows after header (skip separator row which contains only dashes/colons/pipes)
            _sep_re = re.compile(r"^[\s\-|:]*$")
            for row in table_rows[header_idx + 1 :]:
                if _sep_re.match(row):
                    continue
                raw_cols = [c.strip() for c in row.split("|")]
                if len(raw_cols) > file_col_idx:
                    filename = raw_cols[file_col_idx].strip()
                    # Strip markdown link syntax if present: [text](url)
                    link_m = re.match(r"\[([^\]]+)\]\([^\)]+\)", filename)
                    if link_m:
                        filename = link_m.group(1)
                    if (
                        exec_mode_col_idx is not None
                        and len(raw_cols) > exec_mode_col_idx
                    ):
                        raw_mode = raw_cols[exec_mode_col_idx].strip().lower()
                        allowed = {"claude", "python", "skip"}
                        if raw_mode not in allowed:
                            raise click.ClickException(
                                f"Unknown execution mode '{raw_mode}' for file '{filename}'. "
                                f"Allowed: claude, python, skip"
                            )
                        exec_mode_by_file[filename] = raw_mode
                    else:
                        exec_mode_by_file[filename] = "claude"

    for match in PHASE_FILE_PATTERN.finditer(index_text):
        num = int(next(g for g in match.groups() if g is not None))
        filename = match.group(0)
        filepath = index_dir / filename
        if filepath.exists() and num not in phases:
            exec_mode = exec_mode_by_file.get(filename, "claude")
            phases[num] = Phase(number=num, file=filepath, execution_mode=exec_mode)

    # Strategy 2: scan directory if nothing found
    if not phases:
        for f in sorted(index_dir.iterdir()):
            if f.name == index_name or not f.is_file():
                continue
            m = PHASE_FILE_PATTERN.search(f.name)
            if m:
                num = int(next(g for g in m.groups() if g is not None))
                if num not in phases:
                    exec_mode = exec_mode_by_file.get(f.name, "claude")
                    phases[num] = Phase(number=num, file=f, execution_mode=exec_mode)

    return [phases[k] for k in sorted(phases)]


def _extract_phase_name(phase_file: Path) -> str:
    """Try to extract a phase name from the first heading."""
    try:
        for line in phase_file.open():
            line = line.strip()
            if line.startswith("# "):
                # Strip markdown heading and phase number prefix
                name = re.sub(r"^#\s+(?:Phase\s+\d+\s*[-:—]\s*)?", "", line)
                return name[:50]  # truncate
    except OSError:
        pass
    return ""


def validate_phases(
    phases: list[Phase],
    start: int,
    end: int,
) -> dict[str, list[str]]:
    """Validate phase files exist and check for gaps.

    Returns separated buckets with keys: errors, warnings.
    """
    errors: list[str] = []
    warnings: list[str] = []
    active = [p for p in phases if start <= p.number <= end]

    # Check files exist
    for p in active:
        if not p.file.exists():
            errors.append(f"ERROR: Phase {p.number} file missing: {p.file}")

    # Check for gaps
    numbers = [p.number for p in active]
    for i in range(1, len(numbers)):
        if numbers[i] != numbers[i - 1] + 1:
            warnings.append(
                f"WARN: Gap in sequence: Phase {numbers[i - 1]} -> Phase {numbers[i]}"
            )

    return {"errors": errors, "warnings": warnings}


def _resolve_release_dir(index_path: Path) -> Path:
    """Resolve the release directory from a tasklist index path.

    The tasklist index may live directly in the release directory, or inside
    a ``tasklist/`` subdirectory created by ``sc:tasklist``. This function
    detects the subdirectory case by checking:

    1. Is the parent directory named ``tasklist``, ``tasklists``, or ``tasks``?
    2. Does the grandparent contain ``.roadmap-state.json`` or a spec file?

    When both conditions are met, the grandparent is the true release directory.
    Otherwise, falls back to ``index_path.parent`` (backward-compatible default).

    Note: Phase file discovery (``discover_phases``) always uses
    ``index_path.parent`` regardless of this function's output, because
    phase files live alongside the index.
    """
    parent = index_path.parent
    _known_subdir_names = {"tasklist", "tasklists", "tasks"}

    if parent.name.lower() in _known_subdir_names:
        grandparent = parent.parent
        # Check for release-directory indicators in the grandparent
        has_state_file = (grandparent / ".roadmap-state.json").exists()
        has_spec_files = bool(
            list(grandparent.glob("*spec*.md"))
            or list(grandparent.glob("*requirements*.md"))
        )
        if has_state_file or has_spec_files:
            _logger.info(
                "Resolved release_dir to grandparent: %s (index inside %s/)",
                grandparent,
                parent.name,
            )
            return grandparent

    return parent


def load_sprint_config(
    index_path: Path,
    start_phase: int = 1,
    end_phase: int = 0,
    max_turns: int = 100,
    model: str = "",
    dry_run: bool = False,
    permission_flag: str = "--dangerously-skip-permissions",
    debug: bool = False,
    stall_timeout: int = 0,
    stall_action: str = "warn",
    shadow_gates: bool = False,
) -> SprintConfig:
    """Load and validate a complete sprint configuration."""
    index_path = Path(index_path).resolve()

    if not index_path.exists():
        raise click.ClickException(f"Index file not found: {index_path}")

    phases = discover_phases(index_path)
    if not phases:
        raise click.ClickException(
            "No phase files discovered. Expected canonical filenames like: "
            "phase-1-tasklist.md, p1-tasklist.md, phase_1_tasklist.md, tasklist-p1.md"
        )

    # Enrich phases with names
    for phase in phases:
        phase.name = _extract_phase_name(phase.file)

    # Auto-detect end phase
    if end_phase == 0:
        end_phase = max(p.number for p in phases)

    # Validate
    validation = validate_phases(phases, start_phase, end_phase)
    errors = validation["errors"]
    warnings = validation["warnings"]
    if errors:
        for e in errors:
            click.echo(e, err=True)
        raise click.ClickException(f"{len(errors)} phase file(s) missing.")

    for w in warnings:
        click.echo(w, err=True)

    # TUI v2 Wave 1 (v3.7): pre-scan task count across every active phase
    # file. The dual progress bar (F3) uses this as the denominator. Count
    # only phases inside the [start_phase, end_phase] window so --start/--end
    # runs report an accurate total for the current sprint slice.
    total_tasks = sum(
        count_tasks_in_file(p.file)
        for p in phases
        if start_phase <= p.number <= end_phase
    )

    config = SprintConfig(
        index_path=index_path,
        # Resolves grandparent when index is inside tasklist/ subdir;
        # phase discovery still uses index_path.parent via discover_phases().
        release_dir=_resolve_release_dir(index_path),
        phases=phases,
        start_phase=start_phase,
        end_phase=end_phase,
        max_turns=max_turns,
        model=model,
        dry_run=dry_run,
        permission_flag=permission_flag,
        debug=debug,
        stall_timeout=stall_timeout,
        stall_action=stall_action,
        shadow_gates=shadow_gates,
        total_tasks=total_tasks,
    )

    # Validate that the requested range yields at least one active phase
    if not config.active_phases:
        available = [p.number for p in phases]
        raise click.ClickException(
            f"No phases in range [{start_phase}, {end_phase}]. "
            f"Available phase numbers: {available}"
        )

    return config


# ---------------------------------------------------------------------------
# Tasklist parser — extracts task inventory from phase markdown
# ---------------------------------------------------------------------------

_TASK_HEADING_RE = re.compile(
    r"^###\s+(T\d{2}\.\d{2})\s*(?:--|-—|—)\s*(.+)",
    re.MULTILINE,
)

_DEPENDENCY_RE = re.compile(
    r"\*\*Dependencies:\*\*\s*(.*)",
    re.IGNORECASE,
)

_TASK_ID_REF_RE = re.compile(r"T\d{2}\.\d{2}")

# Matches: **Command:** `some command` or **Command:** some command
_COMMAND_RE = re.compile(
    r"\*\*Command:\*\*\s*`?([^`\n]+)`?",
    re.IGNORECASE,
)

# Matches a pipe-table row: | Classifier | value |
_CLASSIFIER_RE = re.compile(
    r"^\|\s*Classifier\s*\|\s*([^|]+)\|",
    re.IGNORECASE | re.MULTILINE,
)


def parse_tasklist(content: str, execution_mode: str = "claude") -> list[TaskEntry]:
    """Parse phase tasklist markdown into a structured task inventory.

    Extracts task ID, title, dependency annotations, command, and classifier
    from each ``### T<PP>.<TT> -- Title`` block. Malformed input (missing
    headings, invalid IDs, empty content) is handled gracefully — invalid
    blocks are skipped with a logged warning.

    Args:
        content: Raw markdown text of a phase tasklist file.
        execution_mode: The phase execution mode (``claude``, ``python``, or
            ``skip``). When ``python``, every task must have a non-empty
            ``**Command:**`` field; a :class:`click.ClickException` is raised
            on the first task found without one.

    Returns:
        Ordered list of :class:`TaskEntry` instances.
    """
    if not content or not content.strip():
        return []

    headings = list(_TASK_HEADING_RE.finditer(content))
    if not headings:
        _logger.warning("No task headings (### T<PP>.<TT>) found in tasklist content")
        return []

    tasks: list[TaskEntry] = []
    for i, match in enumerate(headings):
        task_id = match.group(1)
        title = match.group(2).strip()

        # Extract the block body between this heading and the next (or EOF)
        block_start = match.end()
        block_end = headings[i + 1].start() if i + 1 < len(headings) else len(content)
        block = content[block_start:block_end]

        # Extract dependencies
        dependencies: list[str] = []
        dep_match = _DEPENDENCY_RE.search(block)
        if dep_match:
            dep_text = dep_match.group(1).strip()
            if dep_text.lower() not in ("none", ""):
                dependencies = _TASK_ID_REF_RE.findall(dep_text)

        # Extract **Command:** field (strip surrounding backticks)
        command = ""
        cmd_match = _COMMAND_RE.search(block)
        if cmd_match:
            command = cmd_match.group(1).strip().strip("`")

        # Extract | Classifier | table row
        classifier = ""
        cls_match = _CLASSIFIER_RE.search(block)
        if cls_match:
            classifier = cls_match.group(1).strip()

        # Build description from the deliverables section if present
        description = ""
        for line in block.splitlines():
            stripped = line.strip()
            if stripped.startswith("**Deliverables:**"):
                # Grab the next non-empty line(s) after "Deliverables:"
                idx = block.index(stripped) + len(stripped)
                rest = block[idx:].strip()
                desc_lines = []
                for dline in rest.splitlines():
                    dline = dline.strip()
                    if not dline or dline.startswith("**"):
                        break
                    # Strip leading "- " from markdown list items
                    if dline.startswith("- "):
                        dline = dline[2:]
                    desc_lines.append(dline)
                description = " ".join(desc_lines)
                break

        # Validate python-mode tasks have a command (fail fast at parse time)
        if execution_mode == "python" and not command:
            raise click.ClickException(
                f"Task {task_id} in python-mode phase has no command"
            )

        tasks.append(
            TaskEntry(
                task_id=task_id,
                title=title,
                description=description,
                dependencies=dependencies,
                command=command,
                classifier=classifier,
            )
        )

    return tasks


def parse_tasklist_file(path: Path, execution_mode: str = "claude") -> list[TaskEntry]:
    """Read a phase tasklist file and parse it into a task inventory.

    Args:
        path: Path to the phase tasklist markdown file.
        execution_mode: The phase execution mode (passed to :func:`parse_tasklist`).

    Returns:
        Ordered list of :class:`TaskEntry` instances.

    Raises:
        FileNotFoundError: If the path does not exist.
    """
    content = path.read_text(errors="replace")
    return parse_tasklist(content, execution_mode=execution_mode)
