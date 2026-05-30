"""Smoke test: repo-inventory.sh non-git fallback honours TARGET=`.`.

Regression guard for the bug where `find . -type f` emits `./`-prefixed paths,
which DEFAULT_EXCLUDES (`^(\\.|.*/\\.)`) would otherwise reject wholesale —
making the non-git fallback report `Total files: 0` for the common
TARGET=`.` invocation. The fix normalises find's output to match
`git ls-files`'s un-prefixed shape via `sed 's|^\\./||'`.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "superclaude"
    / "skills"
    / "sc-cleanup-audit-protocol"
    / "scripts"
    / "repo-inventory.sh"
)


def _populate(root: Path) -> None:
    (root / "a.txt").write_text("alpha\n")
    sub = root / "sub"
    sub.mkdir()
    (sub / "b.py").write_text("print('beta')\n")
    # A genuinely-hidden file the default excludes MUST still drop.
    (root / ".secret").write_text("nope\n")


def _run(target: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["sh", str(SCRIPT), target],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def _total(stdout: str) -> int:
    m = re.search(r"Total files:\s+(\d+)", stdout)
    assert m, f"no 'Total files' line in output:\n{stdout}"
    return int(m.group(1))


def test_nongit_target_dot_counts_files(tmp_path: Path) -> None:
    """TARGET=`.` in a non-git dir should count visible files, not zero."""
    _populate(tmp_path)
    result = _run(".", tmp_path)
    assert result.returncode == 0, result.stderr
    assert _total(result.stdout) == 2, result.stdout


def test_nongit_target_dot_still_excludes_hidden(tmp_path: Path) -> None:
    """The fix must NOT weaken DEFAULT_EXCLUDES — `.secret` stays excluded."""
    _populate(tmp_path)
    result = _run(".", tmp_path)
    assert ".secret" not in result.stdout, result.stdout


def test_nongit_target_absolute_unchanged(tmp_path: Path) -> None:
    """Absolute TARGET path was already working; guard against regression."""
    _populate(tmp_path)
    result = _run(str(tmp_path), tmp_path.parent)
    assert result.returncode == 0, result.stderr
    assert _total(result.stdout) == 2, result.stdout


def test_no_illegal_number_noise(tmp_path: Path) -> None:
    """Regression guard for the `||echo 0` bug.

    `grep -c` on no-match exits 1 with stdout `0`; the prior idiom
    `... || echo 0` then appended a second `0`, yielding `"0\\n0"` in
    domain/total counters. Downstream `-gt` / arithmetic then died with
    `[: Illegal number: 0` on every empty domain bucket. The fix
    replaces `|| echo 0` with `|| true` at three sites.
    """
    _populate(tmp_path)
    result = _run(".", tmp_path)
    assert "Illegal number" not in result.stderr, result.stderr


def test_empty_target_no_noise(tmp_path: Path) -> None:
    """Empty non-git target must report zero cleanly — no Illegal-number spew."""
    result = _run(".", tmp_path)
    assert result.returncode == 0, result.stderr
    assert _total(result.stdout) == 0, result.stdout
    assert "Illegal number" not in result.stderr, result.stderr
