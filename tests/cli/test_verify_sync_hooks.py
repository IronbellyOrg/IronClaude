"""Tests for `make verify-sync`'s hook-coverage sections.

These tests exercise the `=== Hooks ===`, `=== Installer Registration ===`,
and `=== Hooks Cross-Consistency ===` sections introduced by the
`hook-sync-and-matcher-fix` release (see release-spec §9 scenarios V1-V7).

WARNING — DO NOT RUN WITH pytest-xdist:
    The tests mutate real repository files in `src/superclaude/hooks/` and
    `src/superclaude/cli/install_hooks.py` via `try/finally` context managers
    and rely on the editable install resolving the on-disk source. Running
    these tests in parallel workers would race on shared files and corrupt
    the source tree. The tmp_path strategy was rejected during research
    (research-03 §4): the editable install resolves `_FRESHNESS_SCRIPTS`
    against the outer repo regardless of subprocess `cwd`, so any
    cross-source mutation MUST happen in-place.

Test scope:
    V1 — clean tree exits zero with `=== Hooks ===` block visible
    V2 — removing `.claude/hooks/auggie-flag-clear.sh` → MISSING error
    V3 — removing entry from `_FRESHNESS_SCRIPTS` → MISSING-from-installer
    V4 — adding fake `ghost-hook.sh` to `_FRESHNESS_SCRIPTS` → STALE
    V5 — `hooks.json` matcher loses one prefix → DRIFT
    V6 — `auggie-flag-clear.sh` case body loses one prefix → DRIFT
    V7 — regression-to-master (both files revert) → DRIFT
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from contextlib import contextmanager
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
HOOKS_JSON = REPO_ROOT / "src" / "superclaude" / "hooks" / "hooks.json"
AUGGIE_FLAG_CLEAR = REPO_ROOT / "src" / "superclaude" / "hooks" / "scripts" / "auggie-flag-clear.sh"
INSTALL_HOOKS_PY = REPO_ROOT / "src" / "superclaude" / "cli" / "install_hooks.py"
CLAUDE_HOOKS_DIR = REPO_ROOT / ".claude" / "hooks"

_HAS_JQ = shutil.which("jq") is not None
_HAS_MAKE = shutil.which("make") is not None

pytestmark = [
    pytest.mark.skipif(not _HAS_MAKE, reason="make required for verify-sync tests"),
    pytest.mark.skipif(
        not _HAS_JQ,
        reason="jq required by === Hooks Cross-Consistency === section in Makefile verify-sync",
    ),
]


def _run_verify_sync() -> subprocess.CompletedProcess:
    """Run `make verify-sync` and return the completed process."""
    return subprocess.run(
        ["make", "verify-sync"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )


@contextmanager
def _temporarily_replace_file(path: Path, new_content: str):
    """Replace `path`'s contents with `new_content` for the duration of the block."""
    original = path.read_text()
    try:
        path.write_text(new_content)
        yield
    finally:
        path.write_text(original)


@contextmanager
def _temporarily_remove_file(path: Path):
    """Move `path` aside for the duration of the block, restore on exit."""
    backup = path.with_suffix(path.suffix + ".pytestbak")
    path.rename(backup)
    try:
        yield
    finally:
        backup.rename(path)


@contextmanager
def _temporarily_mutate_freshness_list(
    *, remove: tuple[str, ...] = (), add: tuple[str, ...] = ()
):
    """Mutate the `_FRESHNESS_SCRIPTS` list literal in `install_hooks.py`.

    Uses regex to find the literal block, parses the script-name entries,
    applies remove/add, and writes back. Restores the original file in
    `finally`.
    """
    original = INSTALL_HOOKS_PY.read_text()
    block_re = re.compile(r"_FRESHNESS_SCRIPTS = \[.*?\]", re.DOTALL)
    match = block_re.search(original)
    if match is None:
        raise AssertionError(
            "Could not locate `_FRESHNESS_SCRIPTS = [...]` block in install_hooks.py"
        )
    current = re.findall(r'"([^"]+\.sh)"', match.group())
    new_list = [s for s in current if s not in remove] + list(add)
    new_block = (
        "_FRESHNESS_SCRIPTS = [\n"
        + "".join(f'    "{s}",\n' for s in new_list)
        + "]"
    )
    mutated = original[: match.start()] + new_block + original[match.end():]
    try:
        INSTALL_HOOKS_PY.write_text(mutated)
        yield
    finally:
        INSTALL_HOOKS_PY.write_text(original)


# ---


def test_V1_clean_tree_exits_zero():  # noqa: N802 — V1-V7 are release-spec §9 scenario IDs
    """V1 (release-spec §9): clean tree — make verify-sync exits 0, stdout contains '=== Hooks ===' block and at least one ✅ entry.

    Maps to: AC-1.1.

    NOTE: This test will fail until the .claude/hooks/auggie-bash-gate.sh
    sync-orphan and reject-workspace-writes.sh installer-orphan are resolved
    per release-spec §6 / Open Questions OQ-2 / OQ-3. Once those are
    addressed in a follow-up PR, this test should pass.
    """
    result = _run_verify_sync()
    assert result.returncode == 0, result.stdout + result.stderr
    assert "=== Hooks ===" in result.stdout
    assert "✅" in result.stdout


def test_V2_missing_claude_hook_detected():  # noqa: N802 — V1-V7 are release-spec §9 scenario IDs
    """V2 (release-spec §9): rm .claude/hooks/auggie-flag-clear.sh → verify-sync reports MISSING, exit != 0. Maps to: AC-1.2."""
    claude_hook = CLAUDE_HOOKS_DIR / "auggie-flag-clear.sh"
    with _temporarily_remove_file(claude_hook):
        result = _run_verify_sync()
    assert result.returncode != 0
    assert "MISSING in .claude/hooks/: auggie-flag-clear.sh" in result.stdout


def test_V3_missing_from_freshness_scripts():  # noqa: N802 — V1-V7 are release-spec §9 scenario IDs
    """V3 (release-spec §9): remove one entry from _FRESHNESS_SCRIPTS → verify-sync reports MISSING-from-installer error. Maps to: AC-1.3."""
    with _temporarily_mutate_freshness_list(remove=("auggie-flag-clear.sh",)):
        result = _run_verify_sync()
    assert result.returncode != 0
    assert "MISSING from _FRESHNESS_SCRIPTS" in result.stdout
    assert "auggie-flag-clear.sh" in result.stdout


def test_V4_stale_in_freshness_scripts():  # noqa: N802 — V1-V7 are release-spec §9 scenario IDs
    """V4 (release-spec §9): add a fake entry 'ghost-hook.sh' to _FRESHNESS_SCRIPTS → verify-sync reports STALE-installer error."""
    with _temporarily_mutate_freshness_list(add=("ghost-hook.sh",)):
        result = _run_verify_sync()
    assert result.returncode != 0
    assert "STALE in _FRESHNESS_SCRIPTS" in result.stdout
    assert "ghost-hook.sh" in result.stdout


def test_V5_matcher_drift_detected():  # noqa: N802 — V1-V7 are release-spec §9 scenario IDs
    """V5 (release-spec §9): hooks.json matcher loses one prefix, case body unchanged → DRIFT. Maps to: AC-3.2/AC-3.3."""
    new_data = json.loads(HOOKS_JSON.read_text())
    for reg in new_data["hooks"]["PostToolUse"]:
        for h in reg.get("hooks", []):
            if "auggie-flag-clear" in h.get("command", ""):
                reg["matcher"] = reg["matcher"].replace("|mcp__auggie-mcp__.*", "")
    with _temporarily_replace_file(HOOKS_JSON, json.dumps(new_data, indent=2)):
        result = _run_verify_sync()
    assert result.returncode != 0
    assert "DRIFT" in result.stdout
    assert "auggie-flag-clear.sh" in result.stdout


def test_V6_case_body_drift_detected():  # noqa: N802 — V1-V7 are release-spec §9 scenario IDs
    """V6 (release-spec §9): auggie-flag-clear.sh case body loses one prefix, matcher unchanged → DRIFT (mirror of V5)."""
    original = AUGGIE_FLAG_CLEAR.read_text()
    mutated = original.replace("|mcp__auggie-mcp__*", "")
    with _temporarily_replace_file(AUGGIE_FLAG_CLEAR, mutated):
        result = _run_verify_sync()
    assert result.returncode != 0
    assert "DRIFT" in result.stdout


def test_V7_regression_to_master():  # noqa: N802 — V1-V7 are release-spec §9 scenario IDs
    """V7 (release-spec §9): both files reverted to current-master matcher gap → DRIFT or DIFFERS, root cause = the matcher-and-case-body gap that Part 2 fixed.

    Note: under the tightened (case-body-only) Cross-Consistency extraction,
    a symmetric revert of BOTH files puts matcher and case body back in
    mutual lockstep (both lacking `mcp__auggie-mcp__`), so the
    `=== Hooks Cross-Consistency ===` check correctly emits ✅ instead of
    ❌ DRIFT. The regression signal in this test is the `⚠️ DIFFERS:
    auggie-flag-clear.sh` message from the `=== Hooks ===` src↔.claude
    forward check, because the test mutates only `src/...` (not `.claude/`)
    so the two copies diverge. Either signal (DRIFT or DIFFERS) is an
    acceptable regression-guard for Part 2.
    """
    new_data = json.loads(HOOKS_JSON.read_text())
    for reg in new_data["hooks"]["PostToolUse"]:
        for h in reg.get("hooks", []):
            if "auggie-flag-clear" in h.get("command", ""):
                reg["matcher"] = (
                    "mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*"
                )
    original_script = AUGGIE_FLAG_CLEAR.read_text()
    mutated_script = original_script.replace("|mcp__auggie-mcp__*", "")
    with _temporarily_replace_file(HOOKS_JSON, json.dumps(new_data, indent=2)):
        with _temporarily_replace_file(AUGGIE_FLAG_CLEAR, mutated_script):
            result = _run_verify_sync()
    assert result.returncode != 0
    assert "DRIFT" in result.stdout or "DIFFERS" in result.stdout
