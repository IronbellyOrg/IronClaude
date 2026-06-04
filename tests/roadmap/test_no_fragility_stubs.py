"""Contract #5 CI lint -- no ``return True`` fragility stubs in the pipeline.

BUILD-REQUEST §Contract #5 forbids ``return True`` statements that carry a
*fragility comment* (``# ... fragile``, ``# ... too hard``, ``# ... for now``)
or an equivalent triple-quoted note -- the signature of a gate/check that was
stubbed out "to avoid blocking" rather than implemented fail-closed. R1.6
deleted the canonical instance (``_cross_refs_resolve`` in ``roadmap/gates.py``,
a structurally PASS-only stub) and audited every other ``return True`` site,
confirming the rest are legitimate early-exit heuristics (see the R1.6 cleanup
inventory §(b)).

This lint walks the entire ``src/superclaude/cli`` tree and asserts ZERO
fragility-commented returns remain (Acceptance Gate #7). It is a CI-only,
source-tree test: on a pipx-installed package there is no ``src/`` tree, so it
skips rather than failing spuriously.

NOTE on scope: the regex matches *comment-flagged* stubs. A structurally
PASS-only stub that carries no fragility comment (as the deleted
``_cross_refs_resolve`` did) is NOT caught by this regex -- it is caught by
code review and the structural reasoning recorded in the cleanup inventory.
The lint's standing value is preventing FUTURE comment-flagged stubs from
landing.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

# BUILD-REQUEST §Contract #5 pattern: ``return True`` immediately followed by a
# ``#`` comment or a ``"""`` note whose text contains a fragility marker.
_FRAGILITY_STUB_RE = re.compile(
    r'return True\s*(?:#|""")\s*.*(?:fragile|too\s+hard|for\s+now)'
)


def _cli_root() -> Path:
    """Resolve ``src/superclaude/cli`` from this test file's location."""
    # tests/roadmap/test_no_fragility_stubs.py -> parents[2] == repo root
    return Path(__file__).resolve().parents[2] / "src" / "superclaude" / "cli"


def test_no_return_true_fragility_stubs():
    """Every ``.py`` under ``src/superclaude/cli`` is free of fragility stubs."""
    cli_root = _cli_root()
    if not cli_root.is_dir():
        pytest.skip(
            f"CI-only source-tree lint: {cli_root} absent "
            "(expected on a pipx-installed package with no src/ tree)."
        )

    offenders: list[str] = []
    for py_file in sorted(cli_root.rglob("*.py")):
        text = py_file.read_text(encoding="utf-8")
        for match in _FRAGILITY_STUB_RE.finditer(text):
            line_no = text[: match.start()].count("\n") + 1
            offenders.append(f"{py_file}:{line_no}: {match.group().strip()!r}")

    assert not offenders, (
        "Contract #5 violation -- `return True` fragility stub(s) found in "
        "src/superclaude/cli (must be fail-closed or removed):\n" + "\n".join(offenders)
    )
