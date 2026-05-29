"""TEST-006 / D-0063 — anthropic ban-import lint rule enforcement (FR-G1).

Pins the FR-G1 static contract: anywhere under ``src/superclaude/cli/eval/``,
an ``import anthropic`` (or any of the explicitly-banned attribute paths)
must fail ``uv run ruff check`` with TID251 (``flake8-tidy-imports``
banned-api). Coverage:

* **Clean tree exits 0.** ``uv run ruff check src/superclaude/cli/eval/``
  against the unmodified source tree must exit with status 0. Together
  with the synthetic-injection branch below, this pins that the ban
  rule is *configured* and *not silently no-op*.
* **Synthetic ``import anthropic`` exits non-zero.** A throwaway file
  is written under ``src/superclaude/cli/eval/_probe_synth/`` with a
  single ``import anthropic`` line; ``uv run ruff check`` must exit
  non-zero and the output must mention ``TID251`` and ``anthropic``.
  The probe file is removed in a ``finally`` block so the tree returns
  to the clean state regardless of test outcome.

The test deliberately uses subprocess invocations of ``uv run ruff``
instead of importing ruff in-process because (a) the linter behaviour we
are pinning is the **CLI** invocation invoked by CI / pre-commit hooks
and (b) ruff's Python API surface is not part of its public contract,
so a subprocess assertion is the durable interface.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
EVAL_PKG = REPO_ROOT / "src" / "superclaude" / "cli" / "eval"
PROBE_DIR = EVAL_PKG / "_probe_synth_ban_import_rule"


def _run_ruff(target: Path) -> subprocess.CompletedProcess[str]:
    """Run ``uv run ruff check <target>`` capturing exit code and output.

    Uses ``--no-cache`` so a previous run that cached a clean result
    cannot mask a freshly-injected ``import anthropic``. We deliberately
    do NOT pass ``--select`` here because the project-level
    ``pyproject.toml`` controls which rules are enabled — pinning that
    side of the contract is exactly what this test is for.
    """

    return subprocess.run(
        ["uv", "run", "ruff", "check", "--no-cache", str(target)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        check=False,
    )


@pytest.fixture
def cleanup_probe_dir():
    """Ensure the synthetic probe directory is removed after each test.

    Removing it before *and* after the test makes the fixture safe to
    re-enter even when a prior run was interrupted mid-test and left
    stale files behind.
    """

    if PROBE_DIR.exists():
        shutil.rmtree(PROBE_DIR)
    yield
    if PROBE_DIR.exists():
        shutil.rmtree(PROBE_DIR)


# ---------------------------------------------------------------------------
# AC1: clean tree → ruff exits 0
# ---------------------------------------------------------------------------


def test_clean_tree_passes_ruff_check(cleanup_probe_dir):
    """``uv run ruff check src/superclaude/cli/eval/`` exits 0 on master.

    The cleanup fixture guarantees no stale probe file is present at
    the start of this test, so a failure here is a real lint regression
    in the eval package, not a leaked artifact from another test.
    """

    result = _run_ruff(EVAL_PKG)
    assert result.returncode == 0, (
        f"Clean tree should pass ruff check but returned {result.returncode}.\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )


# ---------------------------------------------------------------------------
# AC2: synthetic ``import anthropic`` → ruff exits non-zero with TID251
# ---------------------------------------------------------------------------


def test_synthetic_import_anthropic_is_flagged_by_ruff(cleanup_probe_dir):
    """Injecting an ``import anthropic`` under cli/eval/ trips TID251.

    Writes a single throwaway file containing ``import anthropic`` plus
    a no-op usage so the import is not flagged solely as F401
    (unused-import). The expectation is that the ban-rule fires *first*
    because TID251 applies to the bare import regardless of usage.
    """

    PROBE_DIR.mkdir(parents=True, exist_ok=False)
    (PROBE_DIR / "__init__.py").write_text("", encoding="utf-8")
    probe_file = PROBE_DIR / "probe.py"
    probe_file.write_text(
        # The no-op assignment keeps F401 (unused-import) from being
        # the *only* error, so we can assert on the TID251 finding
        # explicitly rather than relying on a single-error stream.
        "import anthropic\n_ = anthropic\n",
        encoding="utf-8",
    )

    result = _run_ruff(EVAL_PKG)
    assert result.returncode != 0, (
        "Synthetic 'import anthropic' should have tripped ruff but it "
        f"exited 0.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    combined = result.stdout + result.stderr
    assert "TID251" in combined, f"expected TID251 in ruff output; got:\n{combined}"
    assert "anthropic" in combined, (
        f"expected 'anthropic' in ruff output; got:\n{combined}"
    )


# ---------------------------------------------------------------------------
# AC3: ban message references FR-G1 (rule is wired to the documented
#      remediation, not just a generic flake8-tidy-imports default)
# ---------------------------------------------------------------------------


def test_ban_message_references_fr_g1(cleanup_probe_dir):
    """The TID251 error includes the FR-G1 remediation hint from pyproject.

    The ``[tool.ruff.lint.flake8-tidy-imports.banned-api]`` entry in
    ``pyproject.toml`` carries an explicit ``msg`` pointing engineers
    at the real-subprocess path (PtyDriver / ClaudeProcessAdapter). If
    that message ever silently drops out of the config — for example
    via a TOML edit that replaces the table with a bare list — TID251
    would still fire but with a generic message, and engineers would
    not see the remediation. Pin the message text here so the
    documentation pathway survives.
    """

    PROBE_DIR.mkdir(parents=True, exist_ok=False)
    (PROBE_DIR / "__init__.py").write_text("", encoding="utf-8")
    (PROBE_DIR / "probe.py").write_text(
        "import anthropic\n_ = anthropic\n",
        encoding="utf-8",
    )

    result = _run_ruff(EVAL_PKG)
    combined = result.stdout + result.stderr
    assert "FR-G1" in combined, (
        "expected 'FR-G1' in ruff output to confirm the banned-api msg "
        f"survived; got:\n{combined}"
    )
