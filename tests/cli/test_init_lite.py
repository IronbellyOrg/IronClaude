"""Behavior tests for `superclaude init-lite --context-optimized`.

These pin the safety contract of the context-audit feature: deterministic
`ceil(bytes/4)` token estimates, low/medium/high thresholds, project-local
surface discovery, the dry-run no-write invariant, default report creation with
the generated marker, opt-in scaffold scope, `CLAUDE.md` byte preservation
across every mode, idempotency, help-flag exposure, and the hard invariant that
no target-project `.claude/` asset is ever created or modified.

The suite uses Click's :class:`CliRunner` to exercise the live
`superclaude.cli.main:main` Click object without spawning a subprocess, and
imports the focused helpers directly for unit-level assertions.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.init_lite import (
    GENERATED_MARKER,
    classify_weight,
    discover_surfaces,
    estimate_tokens,
)
from superclaude.cli.main import main

CLAUDE_MD_CONTENT = "# CLAUDE.md\n\nProject instructions that must never be mutated.\n"


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def _make_project(root: Path) -> None:
    """Create one of each discoverable surface plus several non-surfaces."""
    (root / "CLAUDE.md").write_text(CLAUDE_MD_CONTENT, encoding="utf-8")
    (root / ".mcp.json").write_text('{"mcpServers": {}}\n', encoding="utf-8")

    claude = root / ".claude"
    (claude / "commands" / "sc").mkdir(parents=True, exist_ok=True)
    (claude / "skills" / "foo").mkdir(parents=True, exist_ok=True)
    (claude / "agents").mkdir(parents=True, exist_ok=True)

    (claude / "settings.json").write_text('{"hooks": {}}\n', encoding="utf-8")
    (claude / "commands" / "sc" / "foo.md").write_text(
        "# foo command\n", encoding="utf-8"
    )
    (claude / "skills" / "foo" / "SKILL.md").write_text(
        "# foo skill\n", encoding="utf-8"
    )
    (claude / "agents" / "foo.md").write_text("# foo agent\n", encoding="utf-8")

    # Markdown under .claude/commands is a surface even when it is not an sc/*.md
    # command file; non-markdown command files and non-SKILL/agent files are not.
    (claude / "commands" / "README.md").write_text(
        "command markdown surface\n", encoding="utf-8"
    )
    (claude / "commands" / "sc" / "foo.txt").write_text(
        "not markdown\n", encoding="utf-8"
    )
    (claude / "skills" / "foo" / "refs.md").write_text(
        "not a SKILL.md\n", encoding="utf-8"
    )
    (claude / "agents" / "foo.txt").write_text("not markdown\n", encoding="utf-8")
    (root / "README.md").write_text("not a context surface\n", encoding="utf-8")


# --- Unit: token estimate (ceil(bytes/4)) ---------------------------------


@pytest.mark.parametrize(
    "size_bytes, expected",
    [
        (0, 0),
        (1, 1),
        (3, 1),
        (4, 1),
        (5, 2),
        (7, 2),
        (8, 2),
        (4000, 1000),
        (4001, 1001),
    ],
)
def test_estimate_tokens_is_ceil_bytes_over_4(size_bytes: int, expected: int) -> None:
    assert estimate_tokens(size_bytes) == expected


# --- Unit: weight thresholds (low <1000, medium 1000-4000, high >4000) -----


@pytest.mark.parametrize(
    "tokens, expected",
    [
        (0, "low"),
        (999, "low"),
        (1000, "medium"),
        (4000, "medium"),
        (4001, "high"),
        (9999, "high"),
    ],
)
def test_classify_weight_thresholds(tokens: int, expected: str) -> None:
    assert classify_weight(tokens) == expected


# --- Unit: surface discovery (exactly the allowed set) ---------------------


def test_discover_surfaces_returns_only_allowed_surfaces(tmp_path: Path) -> None:
    _make_project(tmp_path)
    discovered = {s.rel_path for s in discover_surfaces(tmp_path)}
    # Command surfaces are markdown (any depth under .claude/commands), so the
    # top-level README.md is included; the non-markdown foo.txt is excluded.
    assert discovered == {
        "CLAUDE.md",
        ".mcp.json",
        ".claude/settings.json",
        ".claude/commands/README.md",
        ".claude/commands/sc/foo.md",
        ".claude/skills/foo/SKILL.md",
        ".claude/agents/foo.md",
    }


def test_discover_surfaces_empty_project_is_empty(tmp_path: Path) -> None:
    assert discover_surfaces(tmp_path) == []


# --- CLI: required flag + help --------------------------------------------


def test_context_optimized_is_required(runner: CliRunner, tmp_path: Path) -> None:
    result = runner.invoke(main, ["init-lite", "--project-root", str(tmp_path)])
    assert result.exit_code == 2  # Click usage error when required flag is absent


def test_help_lists_all_flags(runner: CliRunner) -> None:
    result = runner.invoke(main, ["init-lite", "--help"])
    assert result.exit_code == 0, result.output
    for flag in (
        "--context-optimized",
        "--project-root",
        "--output",
        "--dry-run",
        "--scaffold",
        "--force",
    ):
        assert flag in result.output, flag


# --- CLI: dry-run writes nothing ------------------------------------------


def test_dry_run_writes_nothing(runner: CliRunner, tmp_path: Path) -> None:
    _make_project(tmp_path)
    result = runner.invoke(
        main,
        [
            "init-lite",
            "--context-optimized",
            "--project-root",
            str(tmp_path),
            "--dry-run",
        ],
    )
    assert result.exit_code == 0, result.output
    assert GENERATED_MARKER in result.output  # rendered to stdout
    assert not (tmp_path / ".dev").exists()
    assert not (tmp_path / ".dev" / "superclaude").exists()


# --- CLI: default report --------------------------------------------------


def test_default_writes_marked_report_and_no_scaffold(
    runner: CliRunner, tmp_path: Path
) -> None:
    _make_project(tmp_path)
    result = runner.invoke(
        main, ["init-lite", "--context-optimized", "--project-root", str(tmp_path)]
    )
    assert result.exit_code == 0, result.output
    report = tmp_path / ".dev" / "superclaude" / "context-audit.md"
    assert report.is_file()
    assert GENERATED_MARKER in report.read_text(encoding="utf-8")
    assert not (tmp_path / ".dev" / "superclaude" / "project-guidance").exists()


def test_explicit_output_path_is_honored(runner: CliRunner, tmp_path: Path) -> None:
    _make_project(tmp_path)
    out = tmp_path / ".dev" / "superclaude" / "custom.md"
    result = runner.invoke(
        main,
        [
            "init-lite",
            "--context-optimized",
            "--project-root",
            str(tmp_path),
            "--output",
            str(out),
        ],
    )
    assert result.exit_code == 0, result.output
    assert out.is_file()
    assert GENERATED_MARKER in out.read_text(encoding="utf-8")


# --- CLI: scaffold opt-in -------------------------------------------------


def test_scaffold_creates_only_two_files(runner: CliRunner, tmp_path: Path) -> None:
    _make_project(tmp_path)
    result = runner.invoke(
        main,
        [
            "init-lite",
            "--context-optimized",
            "--project-root",
            str(tmp_path),
            "--scaffold",
        ],
    )
    assert result.exit_code == 0, result.output
    guidance = tmp_path / ".dev" / "superclaude" / "project-guidance"
    assert (guidance / "SKILL.md").is_file()
    assert (guidance / "refs" / "README.md").is_file()
    created = {
        p.relative_to(guidance).as_posix() for p in guidance.rglob("*") if p.is_file()
    }
    assert created == {"SKILL.md", "refs/README.md"}


# --- CLI: CLAUDE.md byte preservation across all modes --------------------


@pytest.mark.parametrize(
    "extra_flags", [["--dry-run"], [], ["--scaffold"], ["--force"]]
)
def test_claude_md_bytes_never_change(
    runner: CliRunner, tmp_path: Path, extra_flags: list[str]
) -> None:
    _make_project(tmp_path)
    claude_md = tmp_path / "CLAUDE.md"
    before = claude_md.read_bytes()
    result = runner.invoke(
        main,
        [
            "init-lite",
            "--context-optimized",
            "--project-root",
            str(tmp_path),
            *extra_flags,
        ],
    )
    assert result.exit_code == 0, result.output
    assert claude_md.read_bytes() == before


# --- CLI: idempotency -----------------------------------------------------


def test_default_run_is_idempotent(runner: CliRunner, tmp_path: Path) -> None:
    _make_project(tmp_path)
    args = ["init-lite", "--context-optimized", "--project-root", str(tmp_path)]
    first = runner.invoke(main, args)
    second = runner.invoke(main, args)
    assert first.exit_code == 0, first.output
    assert second.exit_code == 0, second.output  # marked report overwrites cleanly


def test_scaffold_rerun_does_not_fail(runner: CliRunner, tmp_path: Path) -> None:
    _make_project(tmp_path)
    args = [
        "init-lite",
        "--context-optimized",
        "--project-root",
        str(tmp_path),
        "--scaffold",
    ]
    assert runner.invoke(main, args).exit_code == 0
    assert runner.invoke(main, args).exit_code == 0


# --- CLI: no target-project .claude/ writes -------------------------------


def test_no_claude_dir_created_when_absent(runner: CliRunner, tmp_path: Path) -> None:
    # Project with only CLAUDE.md; no .claude/ directory at all.
    (tmp_path / "CLAUDE.md").write_text(CLAUDE_MD_CONTENT, encoding="utf-8")
    result = runner.invoke(
        main,
        [
            "init-lite",
            "--context-optimized",
            "--project-root",
            str(tmp_path),
            "--scaffold",
        ],
    )
    assert result.exit_code == 0, result.output
    assert not (tmp_path / ".claude").exists()


def test_existing_claude_dir_is_not_written(runner: CliRunner, tmp_path: Path) -> None:
    _make_project(tmp_path)
    claude = tmp_path / ".claude"
    before = {p: p.read_bytes() for p in claude.rglob("*") if p.is_file()}
    result = runner.invoke(
        main,
        [
            "init-lite",
            "--context-optimized",
            "--project-root",
            str(tmp_path),
            "--scaffold",
            "--force",
        ],
    )
    assert result.exit_code == 0, result.output
    after = {p: p.read_bytes() for p in claude.rglob("*") if p.is_file()}
    assert after == before  # no .claude/ file created, removed, or modified


# --- CLI: --force scope + protected-path refusal --------------------------


def test_force_refuses_markerless_file_outside_owned_root(
    runner: CliRunner, tmp_path: Path
) -> None:
    _make_project(tmp_path)
    outside = tmp_path / "notes.md"
    outside.write_text("hand-written, no marker\n", encoding="utf-8")
    before = outside.read_bytes()
    result = runner.invoke(
        main,
        [
            "init-lite",
            "--context-optimized",
            "--project-root",
            str(tmp_path),
            "--output",
            str(outside),
            "--force",
        ],
    )
    assert result.exit_code != 0  # refused: markerless file outside .dev/superclaude/
    assert outside.read_bytes() == before


@pytest.mark.parametrize(
    "protected_relpath",
    [
        "CLAUDE.md",
        ".mcp.json",
        ".claude/settings.json",
        ".claude/commands/sc/foo.md",
        ".claude/skills/foo/SKILL.md",
        ".claude/agents/foo.md",
    ],
)
def test_force_refuses_to_write_protected_context_inputs(
    runner: CliRunner, tmp_path: Path, protected_relpath: str
) -> None:
    _make_project(tmp_path)
    protected_path = tmp_path / protected_relpath
    before = protected_path.read_bytes()
    result = runner.invoke(
        main,
        [
            "init-lite",
            "--context-optimized",
            "--project-root",
            str(tmp_path),
            "--output",
            str(protected_path),
            "--force",
        ],
    )
    assert result.exit_code != 0  # protected context input refused under --force
    assert protected_path.read_bytes() == before
