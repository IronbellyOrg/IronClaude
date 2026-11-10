#!/usr/bin/env python3
"""keyscan.py [--fake VALUE] [--exclude PATH ...] [paths...]  (contract J2)

Scans every file under the paths (text and binary, files up to 50 MB) for the full API key and, when the key has
>= 20 characters, its first 10 characters. Prints `KEYSCAN OK files=<n>` or `KEYSCAN FAIL <path> <count>` lines
(never any part of the key) and exits 1 on any hit. The key comes from JEV_API_KEY, or --fake VALUE in tests.
Default paths: $SP/p15, $SP/central and the worker transcripts. `$SP/.jev.env` itself is always skipped.
With --fake the planning docs under $SP/p15/plans are also skipped (they quote the fake value); a real scan covers them."""
import glob
import os
import pathlib
import sys

SP = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad")
TRANSCRIPTS = "/tmp/claude-0/-home-user-IronClaude/*/tasks/*.output"
MAX_BYTES = 50 * 1024 * 1024
CHUNK = 1024 * 1024


def count_in_file(path, needles):
    """Number of hits of any needle (bytes) in the file, streaming with len(needle)-sized overlap."""
    maxlen = max(len(n) for n in needles)
    total = 0
    tail = b""
    with open(path, "rb") as f:
        while True:
            chunk = f.read(CHUNK)
            if not chunk:
                break
            buf = tail + chunk
            for n in needles:
                total += _count_new(buf, n, len(tail))
            tail = buf[-(maxlen - 1):] if maxlen > 1 else b""
    return total


def _count_new(buf, needle, tail_len):
    """Occurrences of needle in buf that end after the first tail_len bytes (i.e. not already counted)."""
    c, i = 0, 0
    while True:
        j = buf.find(needle, i)
        if j < 0:
            return c
        if j + len(needle) > tail_len:
            c += 1
        i = j + 1


def iter_files(paths, excludes):
    ex = [pathlib.Path(e).resolve() for e in excludes]
    skip = (SP / ".jev.env").resolve()
    for p in paths:
        p = pathlib.Path(p)
        cands = [p] if p.is_file() else (q for q in sorted(p.rglob("*")) if q.is_file())
        for q in cands:
            try:
                r = q.resolve()
            except OSError:
                continue
            if r == skip or any(e == r or e in r.parents for e in ex):
                continue
            yield q


def main(argv):
    args = list(argv)
    fake, excludes, paths = None, [], []
    while args:
        a = args.pop(0)
        if a == "--fake":
            fake = args.pop(0)
        elif a == "--exclude":
            excludes.append(args.pop(0))
        else:
            paths.append(a)
    if fake is not None:
        # The planning documents quote the fake value used by the acceptance command; they are static text written before any key
        # existed.  A real scan (no --fake) always covers them.
        excludes.append(str(SP / "p15/plans"))
    key = fake if fake is not None else os.environ.get("JEV_API_KEY", "")
    if not key:
        print("KEYSCAN SKIP no key in the environment (use --fake in tests)")
        return 2
    if not paths:
        paths = [str(SP / "p15"), str(SP / "central")] + glob.glob(TRANSCRIPTS)
    needles = [key.encode()]
    if len(key) >= 20:
        needles.append(key[:10].encode())
    n_files, bad = 0, 0
    for f in iter_files(paths, excludes):
        try:
            if f.stat().st_size > MAX_BYTES:
                print(f"KEYSCAN WARN skipped (over 50 MB) {f}")
                continue
            hits = count_in_file(f, needles)
        except OSError:
            continue
        n_files += 1
        if hits:
            bad += 1
            print(f"KEYSCAN FAIL {f} {hits}")
    if bad:
        return 1
    print(f"KEYSCAN OK files={n_files}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
