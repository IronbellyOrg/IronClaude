"""Run one Makefile target's recipe the way GNU make does, for a host without make.

usage: mkrun.py <Makefile> <target>
Each logical recipe line (backslash continuations joined) runs in its own
`/bin/sh -c`; a leading `@` only suppresses the echo; `$$` becomes `$`.
Stops at the first non-zero line and exits with its status (make's default).
Refuses targets with prerequisites or recipes that use make variables `$(...)`
or `${...}`, because those need real make.
"""
import re
import subprocess
import sys

path, target = sys.argv[1], sys.argv[2]
lines = open(path, encoding="utf-8").read().splitlines()
SHELL = next((ln.split(":=", 1)[1].strip() for ln in lines if re.match(r"^SHELL\s*:?=", ln)), "/bin/sh")
start = next(i for i, ln in enumerate(lines) if re.match(rf"^{re.escape(target)}:", ln))
header = lines[start].split(":", 1)[1].strip()
if header:
    sys.exit(f"refused: {target} has prerequisites: {header}")
recipe, i = [], start + 1
while i < len(lines) and lines[i].startswith("\t"):
    logical = lines[i][1:]
    while logical.endswith("\\") and i + 1 < len(lines):
        i += 1
        nxt = lines[i][1:] if lines[i].startswith("\t") else lines[i]
        logical = logical + "\n" + nxt
    recipe.append(logical)
    i += 1
for logical in recipe:
    body = logical.replace("$$", "\0")
    if re.search(r"\$[({]", body):
        sys.exit(f"refused: make variable in recipe line: {logical[:80]}")
    cmd = body.replace("\0", "$").lstrip()
    silent = cmd.startswith("@")
    cmd = cmd.lstrip("@-+ ")
    if not silent:
        print(cmd, flush=True)
    rc = subprocess.run([SHELL, "-c", cmd]).returncode
    if rc:
        print(f"mkrun: *** [{target}] Error {rc}", flush=True)
        sys.exit(rc)
