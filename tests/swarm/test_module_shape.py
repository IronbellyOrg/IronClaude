"""T01.07 — Structural mapping: ``cli/swarm/`` mirrors ``cli/sprint/``.

Enforces AC-003 / NFR-015 from the MultiModelSwarm roadmap: operators
who know the sprint layout must be able to navigate swarm without a
second mental model. The role-mapping table below is the source of
truth; it must stay in sync with the docstring in
``src/superclaude/cli/swarm/__init__.py``.

Role-mapping table (sprint → swarm):

    cli/sprint/__init__.py    -> cli/swarm/__init__.py
    cli/sprint/commands.py    -> cli/swarm/commands.py
    cli/sprint/config.py      -> cli/swarm/config.py
    cli/sprint/models.py      -> cli/swarm/models.py
    cli/sprint/logging_.py    -> cli/swarm/logging_.py
    cli/sprint/tmux.py        -> cli/swarm/tmux.py
    cli/sprint/tui.py         -> cli/swarm/tui.py
    cli/sprint/preflight.py   -> cli/swarm/preflight.py
                                 -- shared name, divergent concrete roles.
                                 Sprint: phase-step subprocess executor.
                                 Swarm: Wave 0 gate -- schema validation,
                                 lens resolution + materialization,
                                 §11.5 / IMM-4 / INV-005 / INV-007 guards,
                                 Manifest emit (COMP-006, T02.02). Both
                                 share the "pre-execution validation"
                                 abstract role so the counterpart slot
                                 fits.

Swarm-only (documented divergences, no sprint analogue):

    cli/swarm/state.py        -- DM-014 SwarmState + DM-015 EventRecord
                                 persistence (resume in M6 reads this
                                 independently; sprint folds run-state
                                 into executor.py).
    cli/swarm/schema.py       -- DM-001 JobSpec JSON Schema + §11.5
                                 cross-field validators (Wave 0
                                 preflight gate; COMP-005). Sprint has
                                 no equivalent because its tasklist
                                 surface is bespoke MDTM, not a
                                 schema-validated job spec.
    cli/swarm/dispatch.py     -- COMP-007 Wave 1 dispatcher. T03.01
                                 lands the wiring + sequential
                                 reference body; T03.02 replaces with
                                 the ParallelExecutor-driven fan-out
                                 (AC-004 / NFR-001 / IMM-3). Sprint
                                 routes phases sequentially through
                                 executor.py, so there is no parity
                                 file.
    cli/swarm/normalize.py    -- COMP-008 Wave 2 normalize dispatcher
                                 (T04.01). Selects recipe by
                                 NormalizationSpec.recipe, applies
                                 per worker, emits final_path body +
                                 meta sidecar. Sprint has no
                                 amalgamation step.
    cli/swarm/transports/     -- Transport Protocol + impls (M3).
    cli/swarm/lenses/         -- DM-010 LensEntry registry (8 entries).
    cli/swarm/recipes/        -- DM-006 normalization recipes.

Sprint-only (documented, no swarm analogue):

    executor.py, monitor.py, summarizer.py, checkpoints.py,
    retrospective.py, classifiers.py, diagnostics.py, debug_logger.py,
    kpi.py, notify.py, process.py
        -- sprint-specific phasing / KPI / shell-out concerns that the
           swarm ResultContract (DM-012), Manifest (DM-016), and
           DoneSentinel (DM-017) replace end-to-end.
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SPRINT_DIR = REPO_ROOT / "src" / "superclaude" / "cli" / "sprint"
SWARM_DIR = REPO_ROOT / "src" / "superclaude" / "cli" / "swarm"

# Files that must exist in BOTH packages with the same name (role parity).
COUNTERPART_FILES: tuple[str, ...] = (
    "__init__.py",
    "commands.py",
    "config.py",
    "models.py",
    "logging_.py",
    "tmux.py",
    "tui.py",
    # T02.02 -- preflight.py exists in both with divergent concrete
    # roles (sprint phase-step executor vs swarm Wave 0 gate) but the
    # same abstract "pre-execution validation" role. Documented in the
    # role-mapping table at the top of this module and in
    # ``cli/swarm/__init__.py``.
    "preflight.py",
)

# Files / subpackages that exist in swarm only -- documented divergences
# in cli/swarm/__init__.py.
SWARM_ONLY_FILES: tuple[str, ...] = (
    "state.py",
    "schema.py",
    "dispatch.py",
    "normalize.py",
    "reduce.py",
    "merge.py",
)
SWARM_ONLY_PACKAGES: tuple[str, ...] = ("transports", "lenses", "recipes")

# Files that exist in sprint only -- their absence from swarm is
# documented in cli/swarm/__init__.py. Any new sprint file appearing
# here-but-also-in-swarm would be an *undocumented* convergence and
# should force a docstring update before this test is loosened.
SPRINT_ONLY_FILES: tuple[str, ...] = (
    "executor.py",
    "monitor.py",
    "summarizer.py",
    "checkpoints.py",
    "retrospective.py",
    "classifiers.py",
    "diagnostics.py",
    "debug_logger.py",
    "kpi.py",
    "notify.py",
    "process.py",
)


def _missing(base: Path, names: tuple[str, ...]) -> list[str]:
    return [name for name in names if not (base / name).exists()]


def test_sprint_package_present_as_baseline() -> None:
    """Sanity: the parity baseline must exist; otherwise mapping is meaningless."""
    assert SPRINT_DIR.is_dir(), f"sprint package missing at {SPRINT_DIR}"
    assert SWARM_DIR.is_dir(), f"swarm package missing at {SWARM_DIR}"


@pytest.mark.parametrize("filename", COUNTERPART_FILES)
def test_counterpart_file_present_in_both(filename: str) -> None:
    """Each documented counterpart (AC-003) exists in sprint AND swarm."""
    sprint_file = SPRINT_DIR / filename
    swarm_file = SWARM_DIR / filename
    assert sprint_file.exists(), (
        f"baseline sprint counterpart missing: {sprint_file.relative_to(REPO_ROOT)} "
        "-- update the COUNTERPART_FILES table if the sprint role moved."
    )
    assert swarm_file.exists(), (
        f"swarm counterpart missing: {swarm_file.relative_to(REPO_ROOT)} "
        "-- AC-003 requires 1:1 role parity for documented counterparts."
    )


def test_all_counterpart_files_present_failure_lists_missing() -> None:
    """Aggregate check: failure message enumerates every missing counterpart."""
    missing_in_swarm = _missing(SWARM_DIR, COUNTERPART_FILES)
    missing_in_sprint = _missing(SPRINT_DIR, COUNTERPART_FILES)
    assert not missing_in_swarm and not missing_in_sprint, (
        "Module-shape parity broken (AC-003 / NFR-015).\n"
        f"  Missing in cli/swarm/ : {missing_in_swarm or 'none'}\n"
        f"  Missing in cli/sprint/: {missing_in_sprint or 'none'}\n"
        "Restore the file or update the role-mapping table + "
        "cli/swarm/__init__.py docstring to record the divergence."
    )


@pytest.mark.parametrize("filename", SWARM_ONLY_FILES)
def test_documented_swarm_only_file_exists(filename: str) -> None:
    """Swarm-specific files documented as divergences must actually exist."""
    target = SWARM_DIR / filename
    assert target.is_file(), (
        f"documented swarm-only file missing: {target.relative_to(REPO_ROOT)} "
        "-- either land the file or remove it from the divergence list."
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


@pytest.mark.parametrize("filename", SPRINT_ONLY_FILES)
def test_sprint_only_file_absent_from_swarm(filename: str) -> None:
    """Sprint-only files must NOT appear in swarm without doc-string update.

    A file landing here-and-in-swarm signals an undocumented convergence:
    update ``cli/swarm/__init__.py`` to record the new counterpart, add
    it to ``COUNTERPART_FILES``, and remove it from ``SPRINT_ONLY_FILES``
    before this assertion is loosened.
    """
    swarm_path = SWARM_DIR / filename
    assert not swarm_path.exists(), (
        f"undocumented convergence: {swarm_path.relative_to(REPO_ROOT)} "
        "exists in swarm but is listed as sprint-only. Update the "
        "role-mapping table + cli/swarm/__init__.py docstring."
    )


def test_no_undocumented_top_level_files_in_swarm() -> None:
    """Every top-level *.py file in cli/swarm/ is either a counterpart or a documented divergence."""
    documented: set[str] = set(COUNTERPART_FILES) | set(SWARM_ONLY_FILES)
    actual_files = {
        p.name
        for p in SWARM_DIR.iterdir()
        if p.is_file() and p.suffix == ".py"
    }
    undocumented = sorted(actual_files - documented)
    assert not undocumented, (
        "Undocumented file(s) in cli/swarm/: "
        f"{undocumented}. Either add a sprint counterpart (then add to "
        "COUNTERPART_FILES) or document it in cli/swarm/__init__.py + "
        "SWARM_ONLY_FILES."
    )


def test_no_undocumented_top_level_subpackages_in_swarm() -> None:
    """Every subpackage in cli/swarm/ is documented as a swarm-specific divergence."""
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
