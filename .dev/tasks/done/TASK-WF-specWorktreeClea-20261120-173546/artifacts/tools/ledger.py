"""Ledger and pin helper for the /sc:implement run of this package.

  ledger.py start <n>
  ledger.py pin <n> <k> <j>
  ledger.py complete <n> --ac A --evidence E --extras X --files F [--note LINE]... [--superseded LINE]...

Only appends to progress.md. The tree snapshot is the protocol's Q0 recipe: a temporary
index, so the user's index is never touched.
"""

import argparse
import os
import subprocess
import tempfile
from pathlib import Path

SLUG = "TASK-WF-specWorktreeClea-20261120-173546"
PKG = Path(".dev/tasks/to-do") / SLUG
LEDGER = PKG / "progress.md"
RETRIES = PKG / "artifacts" / "retries"


def git(*args: str, env: dict | None = None) -> str:
    r = subprocess.run(["git", *args], capture_output=True, text=True, env=env)
    return r.stdout.strip()


def snapshot() -> str:
    fd, idx = tempfile.mkstemp()
    os.close(fd)
    try:
        env = dict(os.environ, GIT_INDEX_FILE=idx)
        subprocess.run(["git", "read-tree", "HEAD"], env=env, check=True)
        subprocess.run(["git", "add", "-A"], env=env, check=True, capture_output=True)
        return git("write-tree", env=env)
    finally:
        os.unlink(idx)


def start(n: int) -> None:
    sha = snapshot()
    git("update-ref", f"refs/superclaude/implement/{SLUG}/T{n}", sha)
    d = RETRIES / f"T{n}"
    d.mkdir(parents=True, exist_ok=True)
    (d / "q0-head").write_text(git("rev-parse", "HEAD") + "\n", encoding="utf-8")
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(f"T{n}: start sha={sha}\n")
    print(sha)


def pin(n: int, k: int, j: int) -> None:
    tree = snapshot()
    git("update-ref", f"refs/superclaude/implement/{SLUG}/retry/T{n}/r{k}-{j}", tree)
    print(tree)


def start_sha(n: int) -> str:
    for line in reversed(LEDGER.read_text(encoding="utf-8").splitlines()):
        if line.startswith(f"T{n}: start sha="):
            return line.split("sha=", 1)[1]
    raise SystemExit("no start line")


def checkpoint(n: int, k: int) -> None:
    """Procedure step 1 of refs/retry.md: the open record first, then the checkpoint ref."""
    tree = snapshot()
    line = f"T{n}: retry n={k + 1} step=open checkpoint={tree} tier=unknown"
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    git("update-ref", f"refs/superclaude/implement/{SLUG}/retry/T{n}/a{k}", tree)
    print(tree)


def complete(args: argparse.Namespace) -> None:
    n = args.n
    sha = start_sha(n)
    token = ""
    if args.note or args.superseded:
        notes = RETRIES / f"T{n}" / "notes.md"
        lines = [sha] + list(args.note) + [f"superseded {s}" for s in args.superseded]
        notes.write_text("\n".join(lines) + "\n", encoding="utf-8")
        m = 1 + len(args.note) + len(args.superseded) if args.note else 1
        # lines 2 to m are the live lines; superseded lines follow line m
        m = 1 + len(args.note)
        token = f",notes@./artifacts/retries/T{n}/notes.md:1-{m}"
    line = (
        f"T{n}: complete verdict=compliant ac={args.ac} evidence={args.evidence}{token} "
        f"extras={args.extras} files={args.files}"
    )
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    # delete the Q0 pin and the reviewed-tree refs; keep sweep refs
    git("update-ref", "-d", f"refs/superclaude/implement/{SLUG}/T{n}")
    refs = git("for-each-ref", "--format=%(refname)", f"refs/superclaude/implement/{SLUG}/retry/T{n}/")
    for ref in refs.splitlines():
        if "/sweep-" in ref:
            continue  # the protocol keeps sweep refs; the final summary lists them
        git("update-ref", "-d", ref)
    print(line)


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("start")
    s.add_argument("n", type=int)
    p = sub.add_parser("pin")
    p.add_argument("n", type=int)
    p.add_argument("k", type=int)
    p.add_argument("j", type=int)
    cp = sub.add_parser("checkpoint")
    cp.add_argument("n", type=int)
    cp.add_argument("k", type=int)
    c = sub.add_parser("complete")
    c.add_argument("n", type=int)
    c.add_argument("--ac", required=True)
    c.add_argument("--evidence", required=True)
    c.add_argument("--extras", required=True)
    c.add_argument("--files", required=True)
    c.add_argument("--note", action="append", default=[])
    c.add_argument("--superseded", action="append", default=[])
    a = ap.parse_args()
    if a.cmd == "start":
        start(a.n)
    elif a.cmd == "pin":
        pin(a.n, a.k, a.j)
    elif a.cmd == "checkpoint":
        checkpoint(a.n, a.k)
    else:
        complete(a)


main()
