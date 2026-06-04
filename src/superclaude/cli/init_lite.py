"""
init-lite --context-optimized

A safe, non-destructive context audit for project-local SuperClaude context
surfaces. By default it writes a generated audit report under
``.dev/superclaude/context-audit.md``; it never rewrites or mutates existing
target-project context inputs (``CLAUDE.md``, ``.mcp.json``,
``.claude/settings.json``, ``.claude/commands/**``, ``.claude/skills/**``,
``.claude/agents/**``). ``--dry-run`` writes nothing. ``--scaffold`` opt-in
creates advisory project-guidance files under ``.dev/superclaude/``.

Token weight is estimated deterministically as ``ceil(bytes / 4)``.
"""

from pathlib import Path
from typing import List, NamedTuple

import click

# Marker identifying a report this command owns. Reports bearing this marker
# may be overwritten on re-run (idempotent); a pre-existing output file lacking
# it is never overwritten without --force (and --force is itself scope-limited
# to artifacts under .dev/superclaude/ -- see _is_init_lite_owned).
GENERATED_MARKER = "<!-- generated-by: superclaude init-lite context-audit v1 -->"

# Relative output paths this command owns, anchored at <project-root>.
REPORT_RELPATH = Path(".dev/superclaude/context-audit.md")
SCAFFOLD_DIR_RELPATH = Path(".dev/superclaude/project-guidance")
OWNED_ROOT_RELPATH = Path(".dev/superclaude")

# Weight thresholds (token estimates). Not pre-existing code -- pinned by tests.
THRESHOLD_LOW_MAX = 1000  # estimate < 1000  -> "low"
THRESHOLD_HIGH_MIN = 4000  # estimate > 4000  -> "high"; [1000, 4000] -> "medium"


class Surface(NamedTuple):
    """A discovered project-local context surface."""

    rel_path: str
    size_bytes: int
    tokens: int
    weight: str


def estimate_tokens(size_bytes: int) -> int:
    """Deterministic token estimate: ``ceil(size_bytes / 4)`` via integer math."""
    if size_bytes <= 0:
        return 0
    return (size_bytes + 3) // 4


def classify_weight(tokens: int) -> str:
    """Classify a token estimate as ``low`` / ``medium`` / ``high``.

    low: estimate < 1000; medium: 1000 <= estimate <= 4000; high: estimate > 4000.
    """
    if tokens < THRESHOLD_LOW_MAX:
        return "low"
    if tokens > THRESHOLD_HIGH_MIN:
        return "high"
    return "medium"


def _add_surface(surfaces: List[Surface], root: Path, path: Path) -> None:
    """Append a Surface for ``path`` (relative to ``root``) if it is a file."""
    if not path.is_file():
        return
    size = path.stat().st_size
    tokens = estimate_tokens(size)
    surfaces.append(
        Surface(
            rel_path=path.relative_to(root).as_posix(),
            size_bytes=size,
            tokens=tokens,
            weight=classify_weight(tokens),
        )
    )


def discover_surfaces(project_root: Path) -> List[Surface]:
    """Discover only project-local SuperClaude context surfaces under ``project_root``.

    Surfaces: ``CLAUDE.md``, ``.mcp.json``, ``.claude/settings.json``,
    ``.claude/commands/**/*.md`` (markdown only), ``.claude/skills/**/SKILL.md``,
    ``.claude/agents/*.md``. Read-only: only file sizes are inspected.
    """
    surfaces: List[Surface] = []

    _add_surface(surfaces, project_root, project_root / "CLAUDE.md")
    _add_surface(surfaces, project_root, project_root / ".mcp.json")
    _add_surface(surfaces, project_root, project_root / ".claude" / "settings.json")

    commands_dir = project_root / ".claude" / "commands"
    if commands_dir.is_dir():
        # Command context surfaces are markdown files (consistent with the
        # agents=*.md and skills=SKILL.md filters); non-markdown files under
        # .claude/commands/ are not context surfaces and are excluded.
        for path in sorted(commands_dir.rglob("*.md")):
            _add_surface(surfaces, project_root, path)

    skills_dir = project_root / ".claude" / "skills"
    if skills_dir.is_dir():
        for path in sorted(skills_dir.rglob("SKILL.md")):
            _add_surface(surfaces, project_root, path)

    agents_dir = project_root / ".claude" / "agents"
    if agents_dir.is_dir():
        for path in sorted(agents_dir.glob("*.md")):
            _add_surface(surfaces, project_root, path)

    return sorted(surfaces, key=lambda s: s.rel_path)


def _is_init_lite_owned(project_root: Path, target: Path) -> bool:
    """True iff ``target`` resolves under ``<project_root>/.dev/superclaude/``.

    This is the --force scope boundary: --force may only overwrite a
    marker-less file when that file is owned by init-lite under .dev/superclaude/.
    """
    owned_root = (project_root / OWNED_ROOT_RELPATH).resolve()
    try:
        target.resolve().relative_to(owned_root)
        return True
    except ValueError:
        return False


def render_report(project_root: Path, surfaces: List[Surface]) -> str:
    """Render the context-audit markdown report (begins with GENERATED_MARKER)."""
    total_tokens = sum(s.tokens for s in surfaces)
    total_bytes = sum(s.size_bytes for s in surfaces)
    top = sorted(surfaces, key=lambda s: s.tokens, reverse=True)[:5]

    lines: List[str] = [
        GENERATED_MARKER,
        "",
        "# SuperClaude Context Audit",
        "",
        f"- **Project root:** `{project_root.as_posix()}`",
        f"- **Surfaces discovered:** {len(surfaces)}",
        f"- **Estimated total tokens:** {total_tokens} (from {total_bytes} bytes, ceil(bytes/4))",
        "",
        "## Surfaces",
        "",
    ]
    if surfaces:
        lines.append("| Surface | Bytes | Est. tokens | Weight |")
        lines.append("|---------|-------|-------------|--------|")
        for s in surfaces:
            lines.append(
                f"| `{s.rel_path}` | {s.size_bytes} | {s.tokens} | {s.weight} |"
            )
    else:
        lines.append("_No project-local SuperClaude context surfaces found._")

    lines += ["", "## Recommendations (manual — no automatic migration)", ""]
    if top:
        lines.append("Biggest context contributors:")
        lines.append("")
        for s in top:
            lines.append(f"- `{s.rel_path}` (~{s.tokens} tokens, {s.weight})")
        lines += [
            "",
            "Consider moving large advisory sections of `CLAUDE.md` into project-guidance",
            "refs under `.dev/superclaude/project-guidance/refs/` and referencing them on",
            "demand, rather than loading them at session start. Apply changes by hand; this",
            "report performs no automatic section migration.",
        ]
    else:
        lines.append("No surfaces to optimize.")

    lines.append("")
    return "\n".join(lines)


# Advisory scaffold templates (copied into a *target* project for it to adapt).
_SCAFFOLD_SKILL = """\
# Project Guidance (advisory scaffold)

This is an advisory scaffold generated by `superclaude init-lite --scaffold`.
It is a starting point for project-specific guidance you load on demand rather
than at session start. Edit it freely; it is NOT a distributable SuperClaude
skill and is never synced into `.claude/`.

## How to use

- Move large, rarely-needed sections of `CLAUDE.md` here.
- Reference detailed material from `refs/` only when a task needs it.
"""

_SCAFFOLD_REFS_README = """\
# Project Guidance Refs (advisory scaffold)

Place detailed, on-demand reference material here. Files in this directory are
loaded only when explicitly needed, keeping session-start context small.
"""


def _is_protected_context_path(project_root: Path, target: Path) -> bool:
    """True iff ``target`` is a read-only target-project context input.

    Protected: ``CLAUDE.md``, ``.mcp.json``, and anything under ``.claude/``.
    Writing to these is forbidden under every flag combination.
    """
    target = target.resolve()
    protected_files = {
        (project_root / "CLAUDE.md").resolve(),
        (project_root / ".mcp.json").resolve(),
    }
    if target in protected_files:
        return True
    claude_dir = (project_root / ".claude").resolve()
    try:
        target.relative_to(claude_dir)
        return True
    except ValueError:
        return False


def _write_report(
    project_root: Path, out_path: Path, content: str, force: bool
) -> None:
    """Write the report to ``out_path``, honoring marker/force/no-mutation rules."""
    if _is_protected_context_path(project_root, out_path):
        raise click.ClickException(
            f"Refusing to write {out_path}: target-project context inputs "
            f"(CLAUDE.md, .mcp.json, .claude/**) are read-only."
        )

    if out_path.exists():
        existing = out_path.read_text(encoding="utf-8", errors="replace")
        if GENERATED_MARKER not in existing and not (
            force and _is_init_lite_owned(project_root, out_path)
        ):
            raise click.ClickException(
                f"Refusing to overwrite {out_path}: it lacks the init-lite generated "
                f"marker. Re-runs overwrite only marked reports; --force overwrites a "
                f"marker-less file only when it is init-lite-owned under .dev/superclaude/."
            )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")


def _write_scaffold(project_root: Path, force: bool) -> List[str]:
    """Create advisory project-guidance scaffold files; idempotent unless ``force``."""
    guidance = project_root / SCAFFOLD_DIR_RELPATH
    targets = (
        (guidance / "SKILL.md", _SCAFFOLD_SKILL),
        (guidance / "refs" / "README.md", _SCAFFOLD_REFS_README),
    )
    created: List[str] = []
    for path, body in targets:
        if path.exists() and not force:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
        created.append(path.as_posix())
    return created


@click.command("init-lite")
@click.option(
    "--context-optimized",
    "context_optimized",
    is_flag=True,
    required=True,
    help="Audit project-local SuperClaude context surfaces and estimate their weight.",
)
@click.option(
    "--project-root",
    "project_root",
    default=".",
    type=click.Path(file_okay=False, path_type=Path),
    help="Project directory to audit (default: current directory).",
)
@click.option(
    "--output",
    "output",
    default=None,
    type=click.Path(dir_okay=False, path_type=Path),
    help="Report output path (default: <project-root>/.dev/superclaude/context-audit.md).",
)
@click.option(
    "--dry-run",
    "dry_run",
    is_flag=True,
    help="Render the report to stdout and write nothing (does not create .dev/superclaude/).",
)
@click.option(
    "--scaffold",
    is_flag=True,
    help="Also create advisory project-guidance files under .dev/superclaude/project-guidance/.",
)
@click.option(
    "--force",
    is_flag=True,
    help="Overwrite init-lite-owned generated artifacts under .dev/superclaude/ (never context inputs).",
)
def init_lite_command(
    context_optimized: bool,
    project_root: Path,
    output: Path,
    dry_run: bool,
    scaffold: bool,
    force: bool,
) -> None:
    """Safely audit project-local SuperClaude context surfaces.

    Default: writes a context-audit report under .dev/superclaude/. Never mutates
    CLAUDE.md, .mcp.json, or any .claude/ context input. --dry-run writes nothing;
    --scaffold opts into advisory project-guidance files.
    """
    root = Path(project_root).resolve()
    surfaces = discover_surfaces(root)
    report = render_report(root, surfaces)

    out_path = Path(output).resolve() if output else (root / REPORT_RELPATH)
    total_tokens = sum(s.tokens for s in surfaces)

    if dry_run:
        click.echo(report)
        click.echo("")
        click.echo("[dry-run] No files written; .dev/superclaude/ not created.")
        return

    _write_report(root, out_path, report, force)
    click.echo(f"Context audit written to {out_path}")
    click.echo(f"Surfaces: {len(surfaces)}; estimated tokens: {total_tokens}")

    if scaffold:
        for created_path in _write_scaffold(root, force):
            click.echo(f"Scaffold: {created_path}")
