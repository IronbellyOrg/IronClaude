"""Atomic, locked bookkeeping for this diagnostic's discriminator emission."""
import fcntl
import json
import os
from pathlib import Path
import sys
import tempfile

store, snapshot = map(Path, sys.argv[1:3])
branch, venue = sys.argv[3:5]


def save(path, value):
    fd, name = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(value, stream, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


with store.with_suffix(store.suffix + ".lock").open("a") as lock:
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    data = json.loads(store.read_text()) if store.exists() else {}
    if not isinstance(data, dict):
        raise ValueError("Counter store is not a mapping")
    venues = data.setdefault(branch, {})
    if not isinstance(venues, dict):
        raise ValueError("Branch counter is not a mapping")
    previous = venues.get(venue, 0)
    if type(previous) is not int or previous < 0:
        raise ValueError("Counter is not a nonnegative integer")
    if snapshot.exists():
        prior = json.loads(snapshot.read_text())
        if prior.get("branch") != branch or prior.get("venue") != venue:
            raise ValueError("Snapshot identity mismatch")
        print("round=" + str(prior["round"]) + " (existing snapshot; unchanged)")
    else:
        venues[venue] = previous + 1
        save(store, data)
        save(snapshot, {"branch": branch, "venue": venue, "round": previous + 1})
        print("round=" + str(previous + 1))
