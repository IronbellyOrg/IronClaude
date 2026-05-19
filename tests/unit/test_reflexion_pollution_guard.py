"""
Regression guard for FU-002 — ReflexionPattern test pollution.

Asserts that running the test suite leaves the repository's reflexion
storage paths untouched:

  - ``docs/mistakes/`` — file count must not increase during the session.
  - ``docs/memory/solutions_learned.jsonl`` — byte size must not change
    during the session.

Snapshots are DYNAMIC (captured at session start) so the test survives
developers with different local pollution levels and any future
deliberate edit to those files. No hard-coded baselines.

Coverage of pollution vectors (see ``src/superclaude/pm_agent/reflexion.py``
and ``src/superclaude/pytest_plugin.py``):
  1. The ``reflexion_pattern`` fixture (function-scoped, env-var seeded).
  2. The ``pytest_runtest_makereport`` hook (bare construction).
  3. The 7 bare ``ReflexionPattern()`` calls in
     ``tests/unit/test_reflexion.py``.

The autouse fixture in ``tests/conftest.py`` redirects all three vectors
to ``tmp_path/docs/memory/`` via ``REFLEXION_OUTPUT_DIR``. This file
verifies that redirect held for the whole session.
"""

from datetime import datetime
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
MISTAKES_DIR = REPO_ROOT / "docs" / "mistakes"
SOLUTIONS_FILE = REPO_ROOT / "docs" / "memory" / "solutions_learned.jsonl"


@pytest.fixture(scope="session", autouse=True)
def _pollution_snapshot():
    """
    Capture pre-session counts of ``docs/mistakes/`` and the size of
    ``docs/memory/solutions_learned.jsonl``; on session teardown assert
    that the post-session values match.

    Both paths are guarded by ``.exists()`` so the test passes cleanly on
    a fresh checkout where the cleansed paths do not exist.
    """
    pre_mistakes = (
        sorted(p.name for p in MISTAKES_DIR.glob("*.md"))
        if MISTAKES_DIR.exists()
        else []
    )
    pre_size = SOLUTIONS_FILE.stat().st_size if SOLUTIONS_FILE.exists() else 0

    yield

    post_mistakes = (
        sorted(p.name for p in MISTAKES_DIR.glob("*.md"))
        if MISTAKES_DIR.exists()
        else []
    )
    post_size = SOLUTIONS_FILE.stat().st_size if SOLUTIONS_FILE.exists() else 0

    added_files = sorted(set(post_mistakes) - set(pre_mistakes))
    assert not added_files, (
        f"Test session polluted {MISTAKES_DIR}: "
        f"{len(added_files)} new file(s): {added_files}"
    )

    assert post_size == pre_size, (
        f"Test session polluted {SOLUTIONS_FILE}: "
        f"{post_size - pre_size} new bytes "
        f"(pre={pre_size}, post={post_size})"
    )


def test_no_dated_mistake_files_created_today():
    """
    Fingerprint check — no ``test_*-<today>.md`` or ``unknown-<today>.md``
    files in ``docs/mistakes/``.

    Cheap, diagnostic, and matches the exact pollution signature observed
    before the fix (e.g. ``test_database_connection-2026-05-18.md``,
    ``unknown-2026-05-18.md``).
    """
    if not MISTAKES_DIR.exists():
        return  # nothing to check on a fresh checkout

    today = datetime.now().strftime("%Y-%m-%d")
    today_files = list(MISTAKES_DIR.glob(f"test_*-{today}.md"))
    today_files += list(MISTAKES_DIR.glob(f"unknown-{today}.md"))

    assert not today_files, (
        "Reflexion test pollution detected in docs/mistakes/: "
        f"{[f.name for f in today_files]}"
    )
