"""Capture once before edits, then statically verify the bounded retirement.

Run with uv run --no-sync python <this-file> [--capture].
Never runs the retired script, Make recipes, installers, or remote operations.
"""

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

EVIDENCE = Path(__file__).resolve().parent
ROOT = EVIDENCE.parents[5]
BASELINE = EVIDENCE / "baseline.json"
LEDGER = ROOT / ".dev/implement/01-legacy-uninstall-070d29db"
PRODUCT = (
    "Makefile",
    "docs/getting-started/installation.md",
    "scripts/uninstall_legacy.sh",
)
REMOVALS = {
    "Makefile": (
        " uninstall-legacy",
        '\t@echo "  make uninstall-legacy - Remove old SuperClaude files from ~/.claude"\n',
        "\n# Remove legacy SuperClaude files from ~/.claude directory\n"
        "uninstall-legacy:\n"
        '\t@echo "🧹 Cleaning up legacy SuperClaude files..."\n'
        "\t@bash scripts/uninstall_legacy.sh\n"
        '\t@echo ""\n',
    ),
    "docs/getting-started/installation.md": (
        "\n# Remove the old Claude Code plugin install\nmake uninstall-legacy\n",
        "`make uninstall-legacy` (run from a repository checkout) runs `scripts/uninstall_legacy.sh`. "
        "It removes only the old Claude Code plugin install: `~/.claude/plugins/superclaude@superclaude`, "
        "`~/.claude/superclaude.json`, `~/.claude/superclaude_config.json`, and the "
        "`superclaude@superclaude` entry in `enabledPlugins` in `~/.claude/settings.json`. "
        "It backs these up to `~/.claude-superclaude-backup-<timestamp>` first. "
        "It does not remove anything `superclaude install` put in `~/.claude/`.\n\n",
    ),
}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def owned(name):
    path = ROOT / name
    return path.is_relative_to(EVIDENCE) or path.is_relative_to(LEDGER)


def paths():
    return set(
        os.fsdecode(
            git("ls-files", "-z", "--cached", "--others", "--exclude-standard")
        ).split("\0")
    ) - {""}


def fingerprint(name):
    path = ROOT / name
    if not os.path.lexists(path):
        return None
    if path.is_dir() and not path.is_symlink():
        return {
            "gitlink": git("ls-files", "--stage", "--", name).decode(),
            "status": git("status", "--porcelain", "--", name).decode(),
            "mode": path.lstat().st_mode,
        }
    content = os.fsencode(os.readlink(path)) if path.is_symlink() else path.read_bytes()
    return {"sha256": hashlib.sha256(content).hexdigest(), "mode": path.lstat().st_mode}


def expected(name, original):
    for fragment in REMOVALS[name]:
        # The phony token also occurs in the help line, removed separately below.
        count = 1 if fragment == " uninstall-legacy" else original.count(fragment)
        assert count == 1, (
            f"baseline fragment missing or ambiguous: {name}: {fragment!r}"
        )
        original = original.replace(fragment, "", 1)
    return original


def capture():
    assert not BASELINE.exists(), "refusing to replace an existing baseline"
    data = {
        "root": str(ROOT),
        "head": git("rev-parse", "HEAD").decode().strip(),
        "branch": git("branch", "--show-current").decode().strip(),
        "snapshot_tree": git(
            "rev-parse", "refs/superclaude/implement/01-legacy-uninstall-070d29db/T1"
        )
        .decode()
        .strip(),
        "status": git("status", "--short", "--branch").decode(),
        "staged_diff": git("diff", "--cached", "--binary").decode(),
        "ignored_inventory_only": git(
            "ls-files", "--others", "--ignored", "--exclude-standard", "--directory"
        ).decode(),
        "files": {
            name: fingerprint(name) for name in sorted(paths()) if not owned(name)
        },
        "original": {name: (ROOT / name).read_text() for name in PRODUCT},
        "caller_search": git(
            "grep",
            "-n",
            "-I",
            "-E",
            "uninstall-legacy|uninstall_legacy\\.sh",
            "--",
            ".",
            ":!.dev",
        ).decode(),
    }
    assert data["branch"].startswith("feature/"), "not a feature branch"
    for name in REMOVALS:
        expected(name, data["original"][name])
    with BASELINE.open("x") as output:
        json.dump(data, output, indent=2, ensure_ascii=False)
        output.write("\n")
    print(
        f"CAPTURED: original contents and hashes, {len(data['files'])} preserved paths, ignored inventory"
    )


def check():
    data = json.loads(BASELINE.read_text())
    assert str(ROOT) == data["root"], "wrong checkout"
    assert git("rev-parse", "HEAD").decode().strip() == data["head"], "HEAD changed"
    assert git("branch", "--show-current").decode().strip() == data["branch"], (
        "branch changed"
    )
    assert git("diff", "--cached", "--binary").decode() == data["staged_diff"], (
        "user staging changed"
    )
    for name in REMOVALS:
        assert (ROOT / name).read_text() == expected(name, data["original"][name]), (
            f"unexpected edit: {name}"
        )
        assert (ROOT / name).lstat().st_mode == data["files"][name]["mode"], (
            f"mode changed: {name}"
        )
    assert not os.path.lexists(ROOT / PRODUCT[2]), (
        "retired script or dangling symlink remains"
    )
    for name, before in data["files"].items():
        if name not in PRODUCT:
            assert fingerprint(name) == before, f"pre-existing work changed: {name}"
    added = {name for name in paths() - data["files"].keys() if not owned(name)}
    assert not added, f"unrequested new files: {sorted(added)}"
    result = subprocess.run(
        [
            "git",
            "grep",
            "-n",
            "-I",
            "-E",
            "uninstall-legacy|uninstall_legacy\\.sh",
            "--",
            ".",
            ":!.dev",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1, (
        f"caller search failed or found references: rc={result.returncode}\n{result.stdout}{result.stderr}"
    )
    assert not result.stdout and not result.stderr, "unexpected search output"
    print(
        "PASS: exact Makefile and guide edits; script absent, including dangling symlinks"
    )
    print(
        "PASS: no active tracked callers; all other baseline files and user staging preserved"
    )
    print(
        "LIMIT: ignored paths inventoried only; external callers and future runtime outcomes UNVERIFIED"
    )


if __name__ == "__main__":
    if sys.argv[1:] == ["--capture"]:
        capture()
    elif not sys.argv[1:]:
        check()
    else:
        raise SystemExit("usage: check_retirement.py [--capture]")
