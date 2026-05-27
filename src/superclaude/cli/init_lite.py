"""init-lite --context-optimized CLI command.

Audits project-local SuperClaude context surfaces, estimates context weight
deterministically, writes a non-destructive report by default, and optionally
scaffolds advisory project-guidance files under ``.dev/superclaude/``.

Never mutates target-project ``CLAUDE.md``, ``.mcp.json``,
``.claude/settings.json``, ``.claude/commands/**``, ``.claude/skills/**``, or
``.claude/agents/**``. ``--dry-run`` writes nothing.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import click

GENERATED_MARKER = "<!-- generated-by: superclaude init-lite context-audit v1 -->"
DEFAULT_REPORT_RELPATH = Path(".dev/superclaude/context-audit.md")
SCAFFOLD_ROOT_RELPATH = Path(".dev/superclaude/project-guidance")
SCAFFOLD_SKILL_RELPATH = SCAFFOLD_ROOT_RELPATH / "SKILL.md"
SCAFFOLD_REFS_RELPATH = SCAFFOLD_ROOT_RELPATH / "refs" / "README.md"

LOW_THRESHOLD = 1000
HIGH_THRESHOLD = 4000


def estimate_tokens(byte_count: int) -> int:
    """Deterministic token estimate: ``ceil(bytes / 4)``."""
    if byte_count < 0:
        raise ValueError("byte_count must be non-negative")
    return math.ceil(byte_count / 4)


def classify_token_estimate(tokens: int) -> str:
    """Classify a token estimate as ``low``, ``medium``, or ``high``."""
    if tokens < LOW_THRESHOLD:
        return "low"
    if tokens <= HIGH_THRESHOLD:
        return "medium"
    return "high"


@dataclass(frozen=True)
class ContextSurface:
    """A discovered project-local SuperClaude context surface."""

    path: Path
    relative_path: Path
    byte_count: int

    @property
    def token_estimate(self) -> int:
        return estimate_tokens(self.byte_count)

    @property
    def bucket(self) -> str:
        return classify_token_estimate(self.token_estimate)


def _make_surface(project_root: Path, path: Path) -> ContextSurface:
    return ContextSurface(
        path=path,
        relative_path=path.relative_to(project_root),
        byte_count=path.stat().st_size,
    )


def discover_surfaces(project_root: Path) -> List[ContextSurface]:
    """Discover project-local SuperClaude context surfaces.

    Scope (read-only): ``CLAUDE.md``, ``.mcp.json``, ``.claude/settings.json``,
    ``.claude/commands/**/*.md``, ``.claude/skills/**/SKILL.md``,
    ``.claude/agents/*.md``.
    """
    surfaces: List[ContextSurface] = []

    for rel in ("CLAUDE.md", ".mcp.json", ".claude/settings.json"):
        candidate = project_root / rel
        if candidate.is_file():
            surfaces.append(_make_surface(project_root, candidate))

    commands_dir = project_root / ".claude" / "commands"
    if commands_dir.is_dir():
        for candidate in sorted(commands_dir.rglob("*.md")):
            if candidate.is_file():
                surfaces.append(_make_surface(project_root, candidate))

    skills_dir = project_root / ".claude" / "skills"
    if skills_dir.is_dir():
        for candidate in sorted(skills_dir.rglob("SKILL.md")):
            if candidate.is_file():
                surfaces.append(_make_surface(project_root, candidate))

    agents_dir = project_root / ".claude" / "agents"
    if agents_dir.is_dir():
        for candidate in sorted(agents_dir.glob("*.md")):
            if candidate.is_file():
                surfaces.append(_make_surface(project_root, candidate))

    return surfaces


def render_report(project_root: Path, surfaces: List[ContextSurface]) -> str:
    """Render the audit report markdown (always starts with the generated marker)."""
    total_bytes = sum(s.byte_count for s in surfaces)
    total_tokens = sum(s.token_estimate for s in surfaces)
    overall_bucket = classify_token_estimate(total_tokens)

    lines: List[str] = [
        GENERATED_MARKER,
        "",
        "# SuperClaude Context Audit",
        "",
        f"**Project root:** `{project_root}`",
        f"**Surfaces discovered:** {len(surfaces)}",
        f"**Total bytes:** {total_bytes}",
        f"**Estimated tokens (ceil(bytes / 4)):** {total_tokens}",
        (
            f"**Overall bucket:** {overall_bucket} "
            f"(low < {LOW_THRESHOLD}, medium {LOW_THRESHOLD}-{HIGH_THRESHOLD}, "
            f"high > {HIGH_THRESHOLD})"
        ),
        "",
        "## Surface Inventory",
        "",
        "| Path | Bytes | Est. tokens | Bucket |",
        "| --- | ---: | ---: | --- |",
    ]
    for surface in surfaces:
        lines.append(
            f"| `{surface.relative_path}` | {surface.byte_count} "
            f"| {surface.token_estimate} | {surface.bucket} |"
        )

    lines.extend(
        [
            "",
            "## Recommendations",
            "",
            (
                "Advisory only. `superclaude init-lite` never mutates context "
                "inputs; it suggests manual moves you can adopt selectively."
            ),
            "",
        ]
    )

    if not surfaces:
        lines.append("- No project-local SuperClaude context surfaces detected.")
    else:
        biggest = max(surfaces, key=lambda surface: surface.token_estimate)
        lines.append(
            f"- Biggest contributor: `{biggest.relative_path}` "
            f"(~{biggest.token_estimate} tokens, {biggest.bucket})."
        )
        if biggest.bucket == "high":
            lines.append(
                f"- Consider moving non-essential reference material out of "
                f"`{biggest.relative_path}` into "
                "`.dev/superclaude/project-guidance/refs/`."
            )
        lines.append(
            "- Copyable patch snippet (advisory): move bulky sections into "
            "`.dev/superclaude/project-guidance/refs/<topic>.md` and link from "
            "`CLAUDE.md` instead of inlining them."
        )

    return "\n".join(lines) + "\n"


SCAFFOLD_SKILL_BODY = """# Project Guidance (Advisory Template)

This file is an advisory example scaffolded by
`superclaude init-lite --scaffold`. It is intentionally placed under
`.dev/superclaude/project-guidance/` so it never collides with distributable
IronClaude skill assets under `.claude/skills/`.

Edit, copy, or discard freely. `superclaude init-lite` will not overwrite this
file unless `--force` is passed.
"""

SCAFFOLD_REFS_README_BODY = """# Project Guidance Refs

Place lazily-loaded reference material here (e.g., long-form context, examples,
templates) that you would otherwise inline into `CLAUDE.md`. Link to these
files from `CLAUDE.md` rather than duplicating their contents.
"""


def _output_owned_by_init_lite(output_path: Path) -> bool:
    """Return True if ``output_path`` is absent or starts with the generated marker."""
    if not output_path.exists():
        return True
    try:
        with output_path.open("r", encoding="utf-8") as handle:
            first_line = handle.readline().rstrip("\n")
    except OSError:
        return False
    return first_line == GENERATED_MARKER


def _is_protected_target_path(project_root: Path, candidate: Path) -> bool:
    """Return True if ``candidate`` is a target-project context input the feature must never write.

    Protected paths under ``project_root``:

    * ``CLAUDE.md``
    * ``.mcp.json``
    * ``.claude/settings.json``
    * anything anywhere under ``.claude/``

    Paths outside ``project_root`` are NOT considered protected by this check
    (the operator pointed ``--output`` at an external location deliberately);
    the marker-ownership refusal still applies to those paths.
    """
    candidate_resolved = candidate.resolve(strict=False)
    root_resolved = project_root.resolve(strict=False)

    try:
        rel = candidate_resolved.relative_to(root_resolved)
    except ValueError:
        return False

    rel_str = rel.as_posix()
    if rel_str in {"CLAUDE.md", ".mcp.json", ".claude/settings.json"}:
        return True
    if rel_str == ".claude" or rel_str.startswith(".claude/"):
        return True
    return False


@click.command("init-lite")
@click.option(
    "--context-optimized",
    "context_optimized",
    is_flag=True,
    default=False,
    help="Run the context-optimized init-lite audit (required).",
)
@click.option(
    "--project-root",
    "project_root",
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    default=None,
    help="Project root to audit (default: current working directory).",
)
@click.option(
    "--output",
    "output",
    type=click.Path(file_okay=True, dir_okay=False, path_type=Path),
    default=None,
    help="Report output path (default: .dev/superclaude/context-audit.md).",
)
@click.option(
    "--dry-run",
    "dry_run",
    is_flag=True,
    default=False,
    help="Render the report to stdout. Writes nothing to disk.",
)
@click.option(
    "--scaffold",
    "scaffold",
    is_flag=True,
    default=False,
    help="Also create advisory .dev/superclaude/project-guidance/ scaffold files.",
)
@click.option(
    "--force",
    "force",
    is_flag=True,
    default=False,
    help=(
        "Overwrite owned report/scaffold files. Never overwrites target-project "
        "CLAUDE.md, .mcp.json, .claude/settings.json, or any .claude/ asset."
    ),
)
def init_lite_command(
    context_optimized: bool,
    project_root: Optional[Path],
    output: Optional[Path],
    dry_run: bool,
    scaffold: bool,
    force: bool,
) -> None:
    """Audit project-local SuperClaude context surfaces (non-destructive).

    Default mode: write a markdown audit report under ``.dev/superclaude/``.
    With ``--dry-run``: render the report to stdout, writing nothing.
    With ``--scaffold``: also create advisory project-guidance files under
    ``.dev/superclaude/project-guidance/``.

    Never modifies ``CLAUDE.md``, ``.mcp.json``, ``.claude/settings.json``, or
    any ``.claude/`` asset in the target project.
    """
    if not context_optimized:
        raise click.UsageError(
            "--context-optimized is required. Re-run with "
            "`superclaude init-lite --context-optimized ...`."
        )

    root = (project_root or Path.cwd()).resolve()
    if not root.is_dir():
        raise click.UsageError(f"--project-root '{root}' is not a directory.")

    surfaces = discover_surfaces(root)
    report_body = render_report(root, surfaces)

    if dry_run:
        click.echo(report_body)
        click.echo("[dry-run] No files written.")
        return

    if output is None:
        output_path = root / DEFAULT_REPORT_RELPATH
    else:
        output_path = output if output.is_absolute() else (root / output)
    output_path = output_path.resolve()

    if _is_protected_target_path(root, output_path):
        raise click.ClickException(
            f"Refusing to write to protected target-project path '{output_path}'. "
            "init-lite never writes to CLAUDE.md, .mcp.json, .claude/settings.json, "
            "or anything under .claude/, even with --force."
        )

    if output_path.exists() and not _output_owned_by_init_lite(output_path):
        if not force:
            raise click.ClickException(
                f"Refusing to overwrite '{output_path}': it does not contain "
                "the init-lite generated marker. Re-run with --force if you "
                "intend to replace this file."
            )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_body, encoding="utf-8")
    click.echo(f"Wrote context audit report to {output_path}")

    if scaffold:
        scaffold_skill = root / SCAFFOLD_SKILL_RELPATH
        scaffold_refs = root / SCAFFOLD_REFS_RELPATH

        scaffold_skill.parent.mkdir(parents=True, exist_ok=True)
        scaffold_refs.parent.mkdir(parents=True, exist_ok=True)

        for path, body in (
            (scaffold_skill, SCAFFOLD_SKILL_BODY),
            (scaffold_refs, SCAFFOLD_REFS_README_BODY),
        ):
            if path.exists() and not force:
                click.echo(
                    f"Scaffold already present (use --force to overwrite): "
                    f"{path.relative_to(root)}"
                )
                continue
            path.write_text(body, encoding="utf-8")
            click.echo(f"Wrote scaffold {path.relative_to(root)}")
