"""T01.07 — Structural layout of ``cli/swarm/``.

The role table below is the source of truth for what lives at the top level
of ``src/superclaude/cli/swarm/``; it must stay in sync with the docstring
in ``src/superclaude/cli/swarm/__init__.py``.

Top-level files (role):

    __init__.py, commands.py, config.py, models.py, logging_.py, tmux.py,
    tui.py          -- Click surface, frozen run config, shared models,
                       run logging, tmux session lifecycle and the TUI.
    preflight.py    -- Wave 0 gate: schema validation, lens resolution +
                       materialization, §11.5 / IMM-4 / INV-005 / INV-007
                       guards, Manifest emit (COMP-006, T02.02).
    state.py        -- DM-014 SwarmState + DM-015 EventRecord persistence.
    schema.py       -- DM-001 JobSpec JSON Schema + §11.5 cross-field
                       validators (COMP-005).
    dispatch.py     -- COMP-007 Wave 1 dispatcher (AC-004 / NFR-001 / IMM-3).
    normalize.py    -- COMP-008 Wave 2 normalize dispatcher.
    reduce.py       -- COMP-009 Wave 3 reduce orchestrator.
    merge.py        -- COMP-010 mechanical merge module.
    atomic.py       -- shared tmp file + fsync + ``os.replace`` byte write.

Sub-packages:

    transports/     -- Transport Protocol + impls (M3).
    lenses/         -- DM-010 LensEntry registry (8 entries).
    recipes/        -- DM-006 normalization recipes.
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SWARM_DIR = REPO_ROOT / "src" / "superclaude" / "cli" / "swarm"

# Top-level files that must exist.
CORE_FILES: tuple[str, ...] = (
    "__init__.py",
    "commands.py",
    "config.py",
    "models.py",
    "logging_.py",
    "tmux.py",
    "tui.py",
    "preflight.py",
)

# Further documented top-level files.
SWARM_ONLY_FILES: tuple[str, ...] = (
    "state.py",
    "schema.py",
    "dispatch.py",
    "normalize.py",
    "reduce.py",
    "merge.py",
    "atomic.py",
)
SWARM_ONLY_PACKAGES: tuple[str, ...] = ("transports", "lenses", "recipes")


def test_swarm_package_present() -> None:
    """Sanity: the package under test must exist."""
    assert SWARM_DIR.is_dir(), f"swarm package missing at {SWARM_DIR}"


@pytest.mark.parametrize("filename", CORE_FILES)
def test_core_file_present(filename: str) -> None:
    """Each documented core file exists."""
    target = SWARM_DIR / filename
    assert target.exists(), (
        f"swarm core file missing: {target.relative_to(REPO_ROOT)} "
        "-- restore it or update the role table + cli/swarm/__init__.py docstring."
    )


@pytest.mark.parametrize("filename", SWARM_ONLY_FILES)
def test_documented_swarm_only_file_exists(filename: str) -> None:
    """Swarm-specific files documented as divergences must actually exist."""
    target = SWARM_DIR / filename
    assert target.is_file(), (
        f"documented swarm-only file missing: {target.relative_to(REPO_ROOT)} "
        "-- either land the file or remove it from the list."
    )


@pytest.mark.parametrize("pkgname", SWARM_ONLY_PACKAGES)
def test_documented_swarm_only_subpackage_exists(pkgname: str) -> None:
    """Swarm-only subpackages (transports/, lenses/, recipes/) must be importable dirs."""
    target = SWARM_DIR / pkgname
    init = target / "__init__.py"
    assert target.is_dir() and init.is_file(), (
        f"documented swarm-only subpackage missing: {target.relative_to(REPO_ROOT)} "
        "-- subpackage requires __init__.py to be a Python package."
    )


def test_no_undocumented_top_level_files_in_swarm() -> None:
    """Every top-level *.py file in cli/swarm/ is a core file or a documented one."""
    documented: set[str] = set(CORE_FILES) | set(SWARM_ONLY_FILES)
    actual_files = {
        p.name for p in SWARM_DIR.iterdir() if p.is_file() and p.suffix == ".py"
    }
    undocumented = sorted(actual_files - documented)
    assert not undocumented, (
        "Undocumented file(s) in cli/swarm/: "
        f"{undocumented}. Document them in cli/swarm/__init__.py + "
        "CORE_FILES / SWARM_ONLY_FILES."
    )


def test_no_undocumented_top_level_subpackages_in_swarm() -> None:
    """Every subpackage in cli/swarm/ is documented."""
    documented = set(SWARM_ONLY_PACKAGES)
    actual_pkgs = {
        p.name
        for p in SWARM_DIR.iterdir()
        if p.is_dir() and p.name != "__pycache__" and (p / "__init__.py").exists()
    }
    undocumented = sorted(actual_pkgs - documented)
    assert not undocumented, (
        f"Undocumented subpackage(s) in cli/swarm/: {undocumented}. "
        "Document it in cli/swarm/__init__.py + SWARM_ONLY_PACKAGES."
    )
