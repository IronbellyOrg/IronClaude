#!/usr/bin/env python3
"""Remove the gateway address an older ccsession installer saved in ccsession.env.

Older installers copied the shell's ANTHROPIC_BASE_URL into ccsession.env so
Orca terminals, which then started from a cleared environment, could find the
gateway. Orca terminals, the Coder terminal and coder ssh now all get the
address from the workspace (Coder llm-env.tf), and ccsession sources
ccsession.env after the inherited environment, so a saved copy only overrides
the right value. Run inside a ccsession session, the old installer saved the
shim's own address (127.0.0.1:<port>), and every later launch then sent its
requests to a shim that was gone ("gateway unreachable ... Connection refused").

Only a file this installer fully owns is changed: exactly the shipped example
plus the installer's marker and one address line. It is put back to the
example. A file the user edited is never touched.

Usage: unseed-env.py <ccsession.env> <ccsession.env.example>
"""

import os
import re
import sys
import tempfile
from pathlib import Path

MARKER = "# Gateway address captured from the workspace by the ccsession installer."


def main() -> int:
    env_path, example_path = Path(sys.argv[1]), Path(sys.argv[2])
    if not env_path.is_file() or env_path.is_symlink():
        return 0
    example = example_path.read_text()
    current = env_path.read_text()
    owned = (
        re.escape(f"{example.rstrip()}\n\n{MARKER}\n")
        + r"export ANTHROPIC_BASE_URL=[^\n]*\n"
    )
    if not re.fullmatch(owned, current):
        return 0
    fd, staged = tempfile.mkstemp(dir=env_path.parent, prefix=".ccsession-env-")
    try:
        with os.fdopen(fd, "w") as handle:
            os.fchmod(handle.fileno(), 0o600)
            handle.write(example)
        os.replace(staged, env_path)
    finally:
        if os.path.exists(staged):
            os.unlink(staged)
    print(f"ccsession: removed the saved gateway address from {env_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
