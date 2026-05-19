"""
Pytest configuration and shared fixtures for SuperClaude tests

This file is automatically loaded by pytest and provides
shared fixtures available to all test modules.
"""

from pathlib import Path

import pytest

# Exclude tests that require optional dependencies not in the project's declared deps.
collect_ignore = [
    "sprint/test_property_based.py",  # requires 'hypothesis' (not a declared dependency)
]

# Repo paths used by the FU-002 pollution-snapshot guard. Defined here (not in
# tests/unit/test_reflexion_pollution_guard.py) because the session-scoped
# autouse fixture must live in a conftest.py to fire at true session start —
# placing it in a test module defers its SETUP until the first test from that
# module is collected, which would miss any pollution from earlier-collected
# modules (e.g. tests/unit/test_reflexion.py, which sorts before this guard).
_FU002_REPO_ROOT = Path(__file__).resolve().parents[1]
_FU002_MISTAKES_DIR = _FU002_REPO_ROOT / "docs" / "mistakes"
_FU002_SOLUTIONS_FILE = _FU002_REPO_ROOT / "docs" / "memory" / "solutions_learned.jsonl"


@pytest.fixture(scope="session", autouse=True)
def _pollution_snapshot():
    """
    FU-002 regression guard — capture pre-session state of the reflexion
    storage paths and assert on session teardown that they were not mutated
    during the test run.

    Snapshots are DYNAMIC (captured at session start) so the test survives
    developers with different local pollution levels and any future
    deliberate edit to those files. No hard-coded baselines.

    Lives in ``tests/conftest.py`` (not in the guard test module) so
    pytest fires its SETUP before the first test of the session runs.
    A session-scoped autouse fixture in a test module is instantiated
    only when that module's first test is collected, which would let
    earlier-alphabetical modules pollute the repo before the snapshot
    is taken. See PR #59 review comment 3265618099.

    Both paths are guarded by ``.exists()`` so the fixture is a no-op
    on a fresh checkout where the cleansed paths do not yet exist.
    """
    pre_mistakes = (
        sorted(p.name for p in _FU002_MISTAKES_DIR.glob("*.md"))
        if _FU002_MISTAKES_DIR.exists()
        else []
    )
    pre_size = (
        _FU002_SOLUTIONS_FILE.stat().st_size if _FU002_SOLUTIONS_FILE.exists() else 0
    )

    yield

    post_mistakes = (
        sorted(p.name for p in _FU002_MISTAKES_DIR.glob("*.md"))
        if _FU002_MISTAKES_DIR.exists()
        else []
    )
    post_size = (
        _FU002_SOLUTIONS_FILE.stat().st_size if _FU002_SOLUTIONS_FILE.exists() else 0
    )

    added_files = sorted(set(post_mistakes) - set(pre_mistakes))
    assert not added_files, (
        f"Test session polluted {_FU002_MISTAKES_DIR}: "
        f"{len(added_files)} new file(s): {added_files}"
    )

    assert post_size == pre_size, (
        f"Test session polluted {_FU002_SOLUTIONS_FILE}: "
        f"{post_size - pre_size} new bytes "
        f"(pre={pre_size}, post={post_size})"
    )


@pytest.fixture(autouse=True)
def _redirect_reflexion_writes(tmp_path, monkeypatch):
    """
    Autouse safety net — redirect all ReflexionPattern writes into tmp_path.

    Sets ``REFLEXION_OUTPUT_DIR=<tmp_path>/docs/memory`` for every test so
    any ``ReflexionPattern()`` constructed without an explicit ``memory_dir``
    argument resolves its storage path inside the per-test tmp_path instead
    of the repository's ``docs/memory/``.

    Three pollution vectors covered:
      1. The ``reflexion_pattern`` fixture in
         ``src/superclaude/pytest_plugin.py:71-93`` (belt-and-suspenders —
         that fixture also sets the env var, but this autouse catches any
         test that doesn't consume the fixture).
      2. The ``pytest_runtest_makereport`` hook in
         ``src/superclaude/pytest_plugin.py:172-196`` which constructs a
         bare ``ReflexionPattern()`` for any failing
         ``@pytest.mark.reflexion`` test.
      3. The 7 bare ``ReflexionPattern()`` constructions in
         ``tests/unit/test_reflexion.py`` at L17, L25, L39, L52, L73, L118,
         L165.

    Production-mirroring layout: ``memory_dir = tmp_path / "docs" / "memory"``,
    so ``mistakes_dir = memory_dir.parent / "mistakes" = tmp_path / "docs" /
    "mistakes"`` — sibling directories rooted in the per-test tmp_path,
    matching the production ``docs/memory/`` + ``docs/mistakes/`` layout
    used by ``ReflexionPattern.__init__``.
    """
    # Do not pre-create the directory; ``ReflexionPattern.__init__`` calls
    # ``mkdir(parents=True, exist_ok=True)`` on its own. Pre-creating here
    # would collide with sibling fixtures (e.g. ``temp_memory_dir``,
    # ``pm_context``) that call ``mkdir(parents=True)`` without
    # ``exist_ok=True`` on the same tmp_path-rooted directory.
    memory_dir = tmp_path / "docs" / "memory"
    monkeypatch.setenv("REFLEXION_OUTPUT_DIR", str(memory_dir))


@pytest.fixture
def sample_context():
    """
    Provide a sample context for confidence checking tests

    Returns:
        Dict with test context including various checks
    """
    return {
        "test_name": "test_sample_feature",
        "test_file": __file__,
        "duplicate_check_complete": True,
        "architecture_check_complete": True,
        "official_docs_verified": True,
        "oss_reference_complete": True,
        "root_cause_identified": True,
        "markers": ["unit", "confidence_check"],
    }


@pytest.fixture
def low_confidence_context():
    """
    Provide a context that should result in low confidence

    Returns:
        Dict with incomplete checks
    """
    return {
        "test_name": "test_unclear_feature",
        "test_file": __file__,
        "duplicate_check_complete": False,
        "architecture_check_complete": False,
        "official_docs_verified": False,
        "oss_reference_complete": False,
        "root_cause_identified": False,
        "markers": ["unit"],
    }


@pytest.fixture
def sample_implementation():
    """
    Provide a sample implementation for self-check validation

    Returns:
        Dict with implementation details
    """
    return {
        "tests_passed": True,
        "test_output": "✅ 5 tests passed in 0.42s",
        "requirements": ["Feature A", "Feature B", "Feature C"],
        "requirements_met": ["Feature A", "Feature B", "Feature C"],
        "assumptions": ["API returns JSON", "Database is PostgreSQL"],
        "assumptions_verified": ["API returns JSON", "Database is PostgreSQL"],
        "evidence": {
            "test_results": "✅ All tests passing",
            "code_changes": ["file1.py", "file2.py"],
            "validation": "Linting passed, type checking passed",
        },
        "status": "complete",
    }


@pytest.fixture
def failing_implementation():
    """
    Provide a failing implementation for self-check validation

    Returns:
        Dict with failing implementation details
    """
    return {
        "tests_passed": False,
        "test_output": "",
        "requirements": ["Feature A", "Feature B", "Feature C"],
        "requirements_met": ["Feature A"],
        "assumptions": ["API returns JSON", "Database is PostgreSQL"],
        "assumptions_verified": ["API returns JSON"],
        "evidence": {},
        "status": "complete",
        "errors": ["TypeError in module X"],
    }


@pytest.fixture
def temp_memory_dir(tmp_path):
    """
    Create temporary memory directory structure for PM Agent tests

    Args:
        tmp_path: pytest's temporary path fixture

    Returns:
        Path to temporary memory directory
    """
    memory_dir = tmp_path / "docs" / "memory"
    memory_dir.mkdir(parents=True)

    # Create empty memory files
    (memory_dir / "pm_context.md").write_text("# PM Context\n")
    (memory_dir / "last_session.md").write_text("# Last Session\n")
    (memory_dir / "next_actions.md").write_text("# Next Actions\n")
    (memory_dir / "reflexion.jsonl").write_text("")

    return memory_dir
