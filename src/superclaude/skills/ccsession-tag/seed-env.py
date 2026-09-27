#!/usr/bin/env python3
"""Record the workspace gateway address in an installer-owned ccsession.env.

Coder workspaces receive ANTHROPIC_BASE_URL as a user secret, but Orca starts
its terminals from a cleared environment and loses it. Saving the address in
ccsession.env lets every ccsession launch find it. Only a file that still
matches the shipped example, or one this script wrote, is changed; a file the
user edited is never touched. The key is never written here: ccsession reads
it from the environment at launch.

Usage: seed-env.py <ccsession.env> <ccsession.env.example>
"""

import os
import re
import shlex
import sys
import tempfile
from pathlib import Path

MARKER = "# Gateway address captured from the workspace by the ccsession installer."


def valid_gateway(url: str) -> bool:
    # Rejects empty values, unexpanded shell text, and .invalid placeholders.
    match = re.fullmatch(r"https?://([^/\s$]+)(/\S*)?", url)
    return bool(match) and not match.group(1).split(":")[0].endswith(".invalid")


def main() -> int:
    env_path, example_path = Path(sys.argv[1]), Path(sys.argv[2])
    url = os.environ.get("ANTHROPIC_BASE_URL", "").strip()
    if not valid_gateway(url) or not env_path.is_file() or env_path.is_symlink():
        return 0
    example = example_path.read_text()
    current = env_path.read_text()
    # Rewrite only files this installer fully owns: the untouched example, or
    # exactly the example plus the marker and one address line. Any other
    # change means the user edited it, so it is left alone.
    owned = (
        re.escape(f"{example.rstrip()}\n\n{MARKER}\n")
        + r"export ANTHROPIC_BASE_URL=[^\n]*\n"
    )
    if current != example and not re.fullmatch(owned, current):
        return 0
    seeded = f"{example.rstrip()}\n\n{MARKER}\nexport ANTHROPIC_BASE_URL={shlex.quote(url)}\n"
    if seeded == current:
        return 0
    fd, staged = tempfile.mkstemp(dir=env_path.parent, prefix=".ccsession-env-")
    try:
        with os.fdopen(fd, "w") as handle:
            os.fchmod(handle.fileno(), 0o600)
            handle.write(seeded)
        os.replace(staged, env_path)
    finally:
        if os.path.exists(staged):
            os.unlink(staged)
    print(f"ccsession: recorded gateway address in {env_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
