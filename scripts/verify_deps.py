#!/usr/bin/env python3
"""Verify the installed Python dependency tree against the AC3 allow-list.

T01.17 / R-015 — Enforces roadmap AC3: "no new external Python deps land
beyond pexpect (transitive via vendored ptytest) and jsonschema (already
transitive)."

The check is name-only (versions ignored). The allow-list lives in
`scripts/dependency_baseline.txt` so additions go through code review.

Exit codes:
  0  current install is a subset of the baseline allow-list
  1  one or more packages outside the allow-list are installed
  2  the baseline file is missing or unreadable
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BASELINE_FILE = REPO_ROOT / "scripts" / "dependency_baseline.txt"


def _normalise(name: str) -> str:
    """PEP 503 normalised package name (lowercase, hyphenated)."""
    return name.strip().lower().replace("_", "-")


def load_baseline(path: Path) -> set[str]:
    if not path.exists():
        print(f"ERROR: baseline file not found at {path}", file=sys.stderr)
        sys.exit(2)
    allowed: set[str] = set()
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        allowed.add(_normalise(line))
    if not allowed:
        print(f"ERROR: baseline file {path} is empty", file=sys.stderr)
        sys.exit(2)
    return allowed


def current_install() -> set[str]:
    try:
        proc = subprocess.run(
            ["uv", "pip", "list", "--format=json"],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        print("ERROR: `uv` is not on PATH; install uv to run verify-deps", file=sys.stderr)
        sys.exit(2)
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: `uv pip list` failed: {exc.stderr}", file=sys.stderr)
        sys.exit(2)
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        print(f"ERROR: `uv pip list` did not return JSON: {exc}", file=sys.stderr)
        sys.exit(2)
    return {_normalise(pkg["name"]) for pkg in payload if "name" in pkg}


def main() -> int:
    allowed = load_baseline(BASELINE_FILE)
    installed = current_install()

    unexpected = sorted(installed - allowed)
    missing = sorted(allowed - installed)

    print(f"Baseline allow-list size: {len(allowed)}")
    print(f"Currently installed:      {len(installed)}")
    if missing:
        print("Allow-listed but not installed (informational, not a failure):")
        for name in missing:
            print(f"  - {name}")
    if unexpected:
        print("")
        print("FAIL: new top-level dependencies detected outside AC3 allow-list:")
        for name in unexpected:
            print(f"  + {name}")
        print("")
        print("AC3 (R-015) permits only `pexpect` and `jsonschema` as additions.")
        print("If this addition is intentional and approved, update:")
        print(f"  {BASELINE_FILE.relative_to(REPO_ROOT)}")
        return 1

    print("")
    print("PASS: installed packages are a subset of the AC3 allow-list.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
