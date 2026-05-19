"""
Regression guard for FU-002 — ReflexionPattern test pollution.

Asserts that running the test suite leaves the repository's reflexion
storage paths untouched. The heavy lifting — the session-scoped pre/post
snapshot of ``docs/mistakes/`` file list and
``docs/memory/solutions_learned.jsonl`` byte size — lives in the
``_pollution_snapshot`` session-scoped autouse fixture in
``tests/conftest.py`` (PR #59 review #3265618099 hoist).

This module retains only the per-test fingerprint check
``test_no_dated_mistake_files_created_today`` — a cheap diagnostic that
matches the exact pollution signature observed before the fix
(e.g. ``test_database_connection-2026-05-18.md``, ``unknown-2026-05-18.md``).

Coverage of pollution vectors (see ``src/superclaude/pm_agent/reflexion.py``
and ``src/superclaude/pytest_plugin.py``):
  1. The ``reflexion_pattern`` fixture (function-scoped, env-var seeded).
  2. The ``pytest_runtest_makereport`` hook (bare construction).
  3. The 7 bare ``ReflexionPattern()`` calls in
     ``tests/unit/test_reflexion.py``.

The autouse fixture in ``tests/conftest.py`` redirects all three vectors
to ``tmp_path/docs/memory/`` via ``REFLEXION_OUTPUT_DIR``; the snapshot
fixture (also in ``tests/conftest.py``) verifies that redirect held for
the whole session.
"""

from datetime import datetime
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
MISTAKES_DIR = REPO_ROOT / "docs" / "mistakes"


def test_no_dated_mistake_files_created_today():
    """
    Fingerprint check — no ``test_*-<today>.md`` or ``unknown-<today>.md``
    files in ``docs/mistakes/``.

    Cheap, diagnostic, and matches the exact pollution signature observed
    before the fix (e.g. ``test_database_connection-2026-05-18.md``,
    ``unknown-2026-05-18.md``).
    """
    if not MISTAKES_DIR.exists():
        pytest.skip(f"{MISTAKES_DIR} does not exist — guard inert on fresh checkout")

    today = datetime.now().strftime("%Y-%m-%d")
    today_files = list(MISTAKES_DIR.glob(f"test_*-{today}.md"))
    today_files += list(MISTAKES_DIR.glob(f"unknown-{today}.md"))

    assert not today_files, (
        "Reflexion test pollution detected in docs/mistakes/: "
        f"{[f.name for f in today_files]}"
    )
