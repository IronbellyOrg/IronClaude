"""Behavior tests for `superclaude init-lite --context-optimized`.

Pins the safety, dry-run, scaffold, idempotency, and no-target-`.claude/`-write
invariants from research/03-report-scaffold-behavior.md and the test plan in
research/04-test-verification.md.

Tests exercise the live ``superclaude.cli.main:main`` Click group via
``CliRunner`` so registration regressions surface here as well.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.init_lite import (
    GENERATED_MARKER,
    _is_protected_target_path,
    classify_token_estimate,
    discover_surfaces,
    estimate_tokens,
)
from superclaude.cli.install_skills import (
    _command_name_for_skill,
    _has_corresponding_command,
)
from superclaude.cli.main import main

# ---------------------------------------------------------------------------
# Token estimate + classification
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("byte_count", "expected"),
    [
        (0, 0),
        (1, 1),
        (3, 1),
        (4, 1),
        (5, 2),
        (7, 2),
        (8, 2),
        (4001, 1001),
    ],
)
def test_estimate_tokens_is_ceil_of_bytes_over_four(byte_count: int, expected: int) -> None:
    assert estimate_tokens(byte_count) == expected


def test_estimate_tokens_rejects_negative() -> None:
    with pytest.raises(ValueError):
        estimate_tokens(-1)


@pytest.mark.parametrize(
    ("tokens", "bucket"),
    [
        (0, "low"),
        (999, "low"),
        (1000, "medium"),
        (4000, "medium"),
        (4001, "high"),
    ],
)
def test_classify_token_estimate_thresholds(tokens: int, bucket: str) -> None:
    assert classify_token_estimate(tokens) == bucket


# ---------------------------------------------------------------------------
# Surface discovery
# ---------------------------------------------------------------------------


def _seed_full_project(root: Path) -> None:
    (root / "CLAUDE.md").write_text("# project claude doc\n", encoding="utf-8")
    (root / ".mcp.json").write_text("{}\n", encoding="utf-8")
    (root / ".claude").mkdir()
    (root / ".claude" / "settings.json").write_text("{}\n", encoding="utf-8")
    (root / ".claude" / "commands" / "sc").mkdir(parents=True)
    (root / ".claude" / "commands" / "sc" / "foo.md").write_text("# foo\n", encoding="utf-8")
    (root / ".claude" / "skills" / "foo").mkdir(parents=True)
    (root / ".claude" / "skills" / "foo" / "SKILL.md").write_text("---\nname: foo\n---\n", encoding="utf-8")
    (root / ".claude" / "agents").mkdir()
    (root / ".claude" / "agents" / "foo.md").write_text("# agent foo\n", encoding="utf-8")


def test_discover_surfaces_finds_all_supported_categories(tmp_path: Path) -> None:
    _seed_full_project(tmp_path)

    surfaces = discover_surfaces(tmp_path)
    relpaths = sorted(str(s.relative_path) for s in surfaces)

    expected = sorted(
        [
            "CLAUDE.md",
            ".mcp.json",
            str(Path(".claude") / "settings.json"),
            str(Path(".claude") / "commands" / "sc" / "foo.md"),
            str(Path(".claude") / "skills" / "foo" / "SKILL.md"),
            str(Path(".claude") / "agents" / "foo.md"),
        ]
    )
    assert relpaths == expected


def test_discover_surfaces_empty_project_returns_no_surfaces(tmp_path: Path) -> None:
    assert discover_surfaces(tmp_path) == []


def test_discover_surfaces_skips_unrelated_files(tmp_path: Path) -> None:
    (tmp_path / "CLAUDE.md").write_text("x", encoding="utf-8")
    # Unrelated files we MUST NOT discover:
    (tmp_path / "README.md").write_text("y", encoding="utf-8")
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "hooks.json").write_text("{}", encoding="utf-8")

    relpaths = {str(s.relative_path) for s in discover_surfaces(tmp_path)}
    assert relpaths == {"CLAUDE.md"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _snapshot_claude_md(project: Path) -> tuple[bytes, str]:
    claude_md = project / "CLAUDE.md"
    return claude_md.read_bytes(), _hash_file(claude_md)


# ---------------------------------------------------------------------------
# Help / flag surface
# ---------------------------------------------------------------------------


def test_help_lists_required_flags(runner: CliRunner) -> None:
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
        assert flag in result.output, f"`{flag}` missing from --help output:\n{result.output}"


def test_missing_context_optimized_is_usage_error(runner: CliRunner, tmp_path: Path) -> None:
    result = runner.invoke(main, ["init-lite", "--project-root", str(tmp_path)])
    assert result.exit_code != 0
    assert "--context-optimized" in result.output


# ---------------------------------------------------------------------------
# Dry-run: writes nothing
# ---------------------------------------------------------------------------


def test_dry_run_writes_nothing(runner: CliRunner, tmp_path: Path) -> None:
    _seed_full_project(tmp_path)
    before_bytes, before_hash = _snapshot_claude_md(tmp_path)

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
    assert GENERATED_MARKER in result.output
    assert "[dry-run]" in result.output

    # No .dev/superclaude/ directory was created.
    assert not (tmp_path / ".dev").exists()

    # CLAUDE.md bytes preserved.
    after_bytes, after_hash = _snapshot_claude_md(tmp_path)
    assert before_bytes == after_bytes
    assert before_hash == after_hash


# ---------------------------------------------------------------------------
# Default report: writes report only, no scaffold
# ---------------------------------------------------------------------------


def test_default_run_writes_report_with_marker_and_no_scaffold(
    runner: CliRunner, tmp_path: Path
) -> None:
    _seed_full_project(tmp_path)
    before_bytes, before_hash = _snapshot_claude_md(tmp_path)

    result = runner.invoke(
        main,
        [
            "init-lite",
            "--context-optimized",
            "--project-root",
            str(tmp_path),
        ],
    )
    assert result.exit_code == 0, result.output

    report = tmp_path / ".dev" / "superclaude" / "context-audit.md"
    assert report.is_file()
    body = report.read_text(encoding="utf-8")
    assert body.startswith(GENERATED_MARKER + "\n")
    assert "Estimated tokens" in body
    assert "Surface Inventory" in body

    # Scaffold NOT created in default mode.
    assert not (tmp_path / ".dev" / "superclaude" / "project-guidance").exists()

    after_bytes, after_hash = _snapshot_claude_md(tmp_path)
    assert before_bytes == after_bytes
    assert before_hash == after_hash


def test_custom_output_flag_used(runner: CliRunner, tmp_path: Path) -> None:
    _seed_full_project(tmp_path)
    custom = tmp_path / "custom" / "audit.md"

    result = runner.invoke(
        main,
        [
            "init-lite",
            "--context-optimized",
            "--project-root",
            str(tmp_path),
            "--output",
            str(custom),
        ],
    )
    assert result.exit_code == 0, result.output
    assert custom.is_file()
    assert custom.read_text(encoding="utf-8").startswith(GENERATED_MARKER + "\n")
    # Default report path was NOT also written.
    assert not (tmp_path / ".dev" / "superclaude" / "context-audit.md").exists()


# ---------------------------------------------------------------------------
# Scaffold opt-in
# ---------------------------------------------------------------------------


def test_scaffold_creates_only_advisory_files(runner: CliRunner, tmp_path: Path) -> None:
    _seed_full_project(tmp_path)
    before_bytes, before_hash = _snapshot_claude_md(tmp_path)

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

    scaffold_root = tmp_path / ".dev" / "superclaude" / "project-guidance"
    assert (scaffold_root / "SKILL.md").is_file()
    assert (scaffold_root / "refs" / "README.md").is_file()

    # Nothing else under project-guidance.
    created = sorted(p.relative_to(scaffold_root).as_posix() for p in scaffold_root.rglob("*") if p.is_file())
    assert created == ["SKILL.md", "refs/README.md"]

    after_bytes, after_hash = _snapshot_claude_md(tmp_path)
    assert before_bytes == after_bytes
    assert before_hash == after_hash


def test_second_scaffold_run_is_idempotent(runner: CliRunner, tmp_path: Path) -> None:
    _seed_full_project(tmp_path)

    args = [
        "init-lite",
        "--context-optimized",
        "--project-root",
        str(tmp_path),
        "--scaffold",
    ]
    first = runner.invoke(main, args)
    assert first.exit_code == 0, first.output

    scaffold_skill = tmp_path / ".dev" / "superclaude" / "project-guidance" / "SKILL.md"
    skill_hash_after_first = _hash_file(scaffold_skill)

    second = runner.invoke(main, args)
    assert second.exit_code == 0, second.output
    # Without --force, scaffold content is left alone.
    assert _hash_file(scaffold_skill) == skill_hash_after_first
    assert "already present" in second.output


# ---------------------------------------------------------------------------
# CLAUDE.md byte preservation across all modes
# ---------------------------------------------------------------------------


def test_claude_md_bytes_preserved_across_all_modes(runner: CliRunner, tmp_path: Path) -> None:
    _seed_full_project(tmp_path)
    before_bytes, before_hash = _snapshot_claude_md(tmp_path)

    invocations = [
        ["init-lite", "--context-optimized", "--project-root", str(tmp_path), "--dry-run"],
        ["init-lite", "--context-optimized", "--project-root", str(tmp_path)],
        ["init-lite", "--context-optimized", "--project-root", str(tmp_path), "--scaffold"],
        ["init-lite", "--context-optimized", "--project-root", str(tmp_path), "--force"],
    ]
    for args in invocations:
        result = runner.invoke(main, args)
        assert result.exit_code == 0, f"{args}: {result.output}"
        after_bytes, after_hash = _snapshot_claude_md(tmp_path)
        assert after_bytes == before_bytes, f"CLAUDE.md bytes changed after {args}"
        assert after_hash == before_hash, f"CLAUDE.md hash changed after {args}"


# ---------------------------------------------------------------------------
# Marked-report idempotency + non-marked file refusal
# ---------------------------------------------------------------------------


def test_second_default_run_overwrites_marked_report(runner: CliRunner, tmp_path: Path) -> None:
    _seed_full_project(tmp_path)
    args = ["init-lite", "--context-optimized", "--project-root", str(tmp_path)]

    first = runner.invoke(main, args)
    assert first.exit_code == 0, first.output
    report = tmp_path / ".dev" / "superclaude" / "context-audit.md"
    assert report.read_text(encoding="utf-8").startswith(GENERATED_MARKER + "\n")

    # Mutate the report (still marker-tagged) and re-run; expect overwrite back to canonical.
    body = report.read_text(encoding="utf-8")
    report.write_text(body + "\n# Stale appended\n", encoding="utf-8")

    second = runner.invoke(main, args)
    assert second.exit_code == 0, second.output
    assert "# Stale appended" not in report.read_text(encoding="utf-8")


def test_refuses_to_overwrite_non_marker_output_without_force(
    runner: CliRunner, tmp_path: Path
) -> None:
    _seed_full_project(tmp_path)
    out = tmp_path / "existing.md"
    out.write_text("hand-written report\n", encoding="utf-8")

    args = [
        "init-lite",
        "--context-optimized",
        "--project-root",
        str(tmp_path),
        "--output",
        str(out),
    ]
    result = runner.invoke(main, args)
    assert result.exit_code != 0
    assert "init-lite generated marker" in result.output
    assert out.read_text(encoding="utf-8") == "hand-written report\n"

    # With --force, overwrite succeeds.
    forced = runner.invoke(main, args + ["--force"])
    assert forced.exit_code == 0, forced.output
    assert out.read_text(encoding="utf-8").startswith(GENERATED_MARKER + "\n")


# ---------------------------------------------------------------------------
# No writes under target-project .claude/
# ---------------------------------------------------------------------------


def _snapshot_dir(root: Path) -> dict[str, str]:
    return {
        str(p.relative_to(root)): _hash_file(p)
        for p in root.rglob("*")
        if p.is_file()
    }


def test_no_writes_under_claude_when_present(runner: CliRunner, tmp_path: Path) -> None:
    _seed_full_project(tmp_path)
    before = _snapshot_dir(tmp_path / ".claude")

    for args in (
        ["init-lite", "--context-optimized", "--project-root", str(tmp_path), "--dry-run"],
        ["init-lite", "--context-optimized", "--project-root", str(tmp_path)],
        ["init-lite", "--context-optimized", "--project-root", str(tmp_path), "--scaffold"],
        ["init-lite", "--context-optimized", "--project-root", str(tmp_path), "--force"],
    ):
        result = runner.invoke(main, args)
        assert result.exit_code == 0, f"{args}: {result.output}"

    after = _snapshot_dir(tmp_path / ".claude")
    assert before == after, f"`.claude/` mutated. before={before} after={after}"


def test_no_claude_dir_created_when_absent(runner: CliRunner, tmp_path: Path) -> None:
    # No .claude/ at all in the target project.
    (tmp_path / "CLAUDE.md").write_text("x", encoding="utf-8")

    for args in (
        ["init-lite", "--context-optimized", "--project-root", str(tmp_path), "--dry-run"],
        ["init-lite", "--context-optimized", "--project-root", str(tmp_path)],
        ["init-lite", "--context-optimized", "--project-root", str(tmp_path), "--scaffold"],
    ):
        result = runner.invoke(main, args)
        assert result.exit_code == 0, f"{args}: {result.output}"
        assert not (tmp_path / ".claude").exists()


# ---------------------------------------------------------------------------
# Installer mapping: sc-<command>-protocol → commands/<command>.md (Step 3.3)
# ---------------------------------------------------------------------------


def test_installer_maps_sc_init_lite_protocol_to_init_lite_command() -> None:
    """`sc-init-lite-protocol` must be treated as command-backed by `commands/init-lite.md`."""
    assert _has_corresponding_command("sc-init-lite-protocol") is True
    assert _command_name_for_skill("sc-init-lite-protocol") == "init-lite"


def test_installer_keeps_existing_sc_prefix_mapping() -> None:
    """Existing `sc-<command>` mapping behavior is unchanged when a command file exists."""
    # `sc-roadmap` maps to `commands/roadmap.md` which exists in this repo.
    assert _has_corresponding_command("sc-roadmap") is True
    assert _command_name_for_skill("sc-roadmap") == "roadmap"


def test_installer_rejects_non_sc_prefix() -> None:
    assert _has_corresponding_command("not-sc-prefixed") is False
    assert _command_name_for_skill("not-sc-prefixed") is None


def test_installer_rejects_sc_skill_without_matching_command() -> None:
    # `sc-totally-fictional` has no `commands/totally-fictional.md`.
    assert _has_corresponding_command("sc-totally-fictional") is False
    assert _command_name_for_skill("sc-totally-fictional") is None


def test_installer_rejects_protocol_skill_without_matching_command() -> None:
    # `sc-totally-fictional-protocol` has no `commands/totally-fictional.md`.
    assert _has_corresponding_command("sc-totally-fictional-protocol") is False
    assert _command_name_for_skill("sc-totally-fictional-protocol") is None


# ---------------------------------------------------------------------------
# Protected target-project paths: --output cannot redirect writes to
# CLAUDE.md, .mcp.json, .claude/settings.json, or anything under .claude/,
# even with --force. (rf-qa Invariant 5 remediation.)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "relpath",
    [
        "CLAUDE.md",
        ".mcp.json",
        str(Path(".claude") / "settings.json"),
        str(Path(".claude") / "commands" / "sc" / "foo.md"),
        str(Path(".claude") / "skills" / "foo" / "SKILL.md"),
        str(Path(".claude") / "agents" / "foo.md"),
        str(Path(".claude") / "hooks.json"),
    ],
)
@pytest.mark.parametrize("use_force", [False, True])
def test_output_to_protected_path_is_refused(
    runner: CliRunner, tmp_path: Path, relpath: str, use_force: bool
) -> None:
    """`--output <protected>` is refused regardless of `--force` (Invariant 5)."""
    _seed_full_project(tmp_path)
    target = tmp_path / relpath
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_text("preserved\n", encoding="utf-8")
    before_bytes = target.read_bytes()
    before_hash = _hash_file(target)

    args = [
        "init-lite",
        "--context-optimized",
        "--project-root",
        str(tmp_path),
        "--output",
        str(target),
    ]
    if use_force:
        args.append("--force")

    result = runner.invoke(main, args)
    assert result.exit_code != 0, result.output
    assert "protected target-project path" in result.output

    # Bytes preserved across the refusal — no partial write.
    assert target.read_bytes() == before_bytes
    assert _hash_file(target) == before_hash


def test_is_protected_target_path_unit() -> None:
    """Direct coverage of the denylist helper."""
    root = Path("/tmp/init-lite-probe").resolve()
    assert _is_protected_target_path(root, root / "CLAUDE.md") is True
    assert _is_protected_target_path(root, root / ".mcp.json") is True
    assert _is_protected_target_path(root, root / ".claude" / "settings.json") is True
    assert _is_protected_target_path(root, root / ".claude" / "commands" / "sc" / "x.md") is True
    assert _is_protected_target_path(root, root / ".claude" / "skills" / "x" / "SKILL.md") is True
    assert _is_protected_target_path(root, root / ".claude" / "agents" / "x.md") is True
    # Allowed paths
    assert _is_protected_target_path(root, root / ".dev" / "superclaude" / "context-audit.md") is False
    assert _is_protected_target_path(root, root / "custom" / "audit.md") is False
    # Paths outside the root are not project-relative; the marker-guard still applies elsewhere.
    assert _is_protected_target_path(root, Path("/tmp/elsewhere/CLAUDE.md").resolve()) is False
