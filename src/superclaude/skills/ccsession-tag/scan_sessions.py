#!/usr/bin/env python3
"""Batch helper for `ccsession --here` (and `--ask`, which shows that list): where is
each session's transcript, and which folder was it started in? One process for the
whole list instead of five or more per saved name.

    scan_sessions.py <projects-dir> <repo-keyed-folder> <session-id>...

Prints one record per session id, in the order given, each ended by a newline:

    <transcript path> US <status> US <start folder>

(US is the ASCII unit separator, 0x1f.) The transcript path is empty when the session
has none. <status> is empty when the record is final, and "x" when the caller must work
the row out itself (an id that is empty or is not a file name, a transcript that
contains a NUL byte where grep would treat the text as binary): ccsession then runs its
own code for that row.

The rules are the ones of ccsession's own code (find_transcript and session_home),
which this must keep byte for byte:

* transcript: the file in the repo-keyed folder when there is one, else the newest copy
  under <projects-dir>/*/<id>.jsonl (newest modification time first, then by path, the
  order of `ls -t`; hidden folders are not searched, as in a shell glob);
* start folder: only the first 256 KiB and the last 1 MiB are read (the tail only when
  the head found no folder that matches); every `"cwd":"..."` value in that text, in
  order and without repeats, is unescaped (`\\"` to `"`, then `\\\\` to `\\`, not JSON);
  the first one whose name, with every byte that is not a letter or digit turned into
  "-", equals the name of the transcript's folder is the answer, else the first one.

Nothing is written: files are only opened for reading. Any other failure exits non-zero
(ccsession then does all of it itself).
"""

from __future__ import annotations

import os
import re
import sys

HEAD = 262144
TAIL = 1048576
US = b"\x1f"
CWD = re.compile(rb'"cwd":"(?:[^"\\\n]|\\[^\n])*"')
SANITIZE = bytes(b if (chr(b).isalnum() and b < 128) else ord("-") for b in range(256))


def newest_copies(projects: bytes, wanted: set[bytes]) -> dict[bytes, bytes]:
    """The newest copy (by `ls -t` order) of each wanted id under projects/*/<id>.jsonl."""
    found: dict[bytes, list[tuple[int, bytes]]] = {}
    with os.scandir(projects) as top:
        folders = sorted(e.path for e in top if not e.name.startswith(b"."))
    for folder in folders:
        try:
            if not os.path.isdir(folder):
                continue
            with os.scandir(folder) as inner:
                for entry in inner:
                    name = entry.name
                    if not name.endswith(b".jsonl"):
                        continue
                    sid = name[: -len(b".jsonl")]
                    if sid in wanted and not name.startswith(b"."):
                        try:
                            mtime = os.lstat(entry.path).st_mtime_ns
                        except OSError:
                            continue
                        found.setdefault(sid, []).append((mtime, entry.path))
        except OSError:
            continue
    best = {}
    for sid, copies in found.items():
        copies.sort(key=lambda c: (-c[0], c[1]))
        best[sid] = copies[0][1]
    return best


def unescape(raw: bytes) -> bytes:
    """The value of a matched `"cwd":"..."`, unescaped in ccsession's two steps."""
    cwd = raw[len(b'"cwd":"') : -1]
    cwd = cwd.replace(b'\\"', b'"')
    return cwd.replace(b"\\\\", b"\\")


def start_folder(path: bytes) -> tuple[bytes | None, bool]:
    """(folder, ok). ok is False when grep would have treated the text as binary."""
    store = os.path.basename(os.path.dirname(path)) if b"/" in path else b"."
    try:
        with open(path, "rb") as fh:
            head = fh.read(HEAD)
            if b"\0" in head:
                return None, False
            first = None
            seen = set()
            chunks = [head]
            tail_read = False
            while chunks:
                for raw in CWD.findall(chunks.pop(0)):
                    if raw in seen:
                        continue
                    seen.add(raw)
                    cwd = unescape(raw)
                    if first is None:
                        first = cwd
                    if cwd.translate(SANITIZE) == store:
                        return cwd, True
                if not tail_read:
                    tail_read = True
                    size = os.fstat(fh.fileno()).st_size
                    fh.seek(max(size - TAIL, 0))
                    tail = fh.read()
                    if b"\0" in tail:
                        return None, False
                    chunks.append(tail)
            return (first if first is not None else b""), True
    except OSError:
        return b"", True


def main(argv: list[bytes]) -> int:
    if len(argv) < 4:
        sys.stderr.write(
            "usage: scan_sessions.py <projects> <repo-keyed-folder> <id>...\n"
        )
        return 2
    projects, repo_folder, ids = argv[1], argv[2], argv[3:]
    plain = [sid for sid in ids if sid and b"/" not in sid and b"\0" not in sid]
    copies = newest_copies(projects, set(plain))
    out = []
    homes: dict[bytes, bytes | None] = {}
    for sid in ids:
        if (
            not sid
            or sid.startswith(b".")
            or b"/" in sid
            or b"\0" in sid
            or b"*" in sid
            or b"?" in sid
            or b"[" in sid
        ):
            out.append(US + b"x" + US)
            continue
        own = repo_folder + b"/" + sid + b".jsonl"
        path = own if os.path.isfile(own) else copies.get(sid, b"")
        home: bytes | None = b""
        if path and os.path.isfile(path):
            if path not in homes:
                folder, ok = start_folder(path)
                homes[path] = folder if ok else None
            home = homes[path]
        if home is None:
            out.append(path + US + b"x" + US)
        else:
            out.append(path + US + US + home)
    sys.stdout.buffer.write(b"\n".join(out) + b"\n")
    return 0


if __name__ == "__main__":
    sys.exit(main([os.fsencode(a) for a in sys.argv]))
