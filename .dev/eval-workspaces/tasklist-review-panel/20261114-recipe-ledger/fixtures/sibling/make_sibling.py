"""F-SIBLING: a fake sibling folder with Tier A, S, T and B files in chosen states (TESTING 2; DR-11, K8).

The file contents are invented one-line stubs. A canary file with a fixed old mtime lets a test prove that
nothing wrote into the folder: `snapshot()` lists every path with its size and mtime, directories included.
"""

import json
import os
import threading
from pathlib import Path

RL = Path(__file__).resolve().parents[2]
CANARY = "CANARY.txt"
OLD_MTIME = 1_000_000_000  # 2001-09-09, far from any real write


def load_list(list_path=None):
    return json.loads((list_path or RL / "config" / "shared-list.json").read_text())[
        "tiers"
    ]


def _write(root, rel, text):
    p = Path(root) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    return p


def build(root, tier_b="absent", missing_tier_a=None, tiers=None):
    """Build the folder `root`.

    tier_b: "absent" (no Tier B file), "present" (all of them) or a list of the Tier B paths that exist.
    missing_tier_a: one Tier A path to leave out.
    Returns the snapshot taken after the build (so a later `snapshot(root) == result` proves a read-only use).
    """
    tiers = tiers or load_list()
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    for tier in ("A", "S", "T"):
        for rel in tiers[tier]:
            if rel != missing_tier_a:
                _write(root, rel, f"fixture stub of {rel}\n")
    b_paths = [b["path"] for b in tiers["B"]]
    present = (
        b_paths if tier_b == "present" else ([] if tier_b == "absent" else list(tier_b))
    )
    for rel in present:
        _write(root, rel, f"fixture stub of {rel}, version 1\n")
    canary = _write(root, CANARY, "canary\n")
    os.utime(canary, (OLD_MTIME, OLD_MTIME))
    return snapshot(root)


def snapshot(root):
    """Every path under root (files and folders) mapped to (size, mtime_ns); atime is not read."""
    out = {}
    for p in sorted(Path(root).rglob("*")):
        st = p.stat()
        out[str(p.relative_to(root))] = (
            0 if p.is_dir() else st.st_size,
            st.st_mtime_ns,
        )
    return out


def canary_unchanged(root):
    st = (Path(root) / CANARY).stat()
    return (
        st.st_mtime_ns == OLD_MTIME * 1_000_000_000
        and (Path(root) / CANARY).read_text() == "canary\n"
    )


def change_later(root, rel, after_s):
    """Rewrite `rel` after `after_s` seconds, on a timer thread (a Tier B file that changes between two reads)."""
    t = threading.Timer(
        after_s, lambda: _write(root, rel, f"fixture stub of {rel}, version 2\n")
    )
    t.start()
    return t


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("root")
    ap.add_argument("--tier-b", default="absent", choices=("absent", "present"))
    ap.add_argument("--missing-tier-a")
    a = ap.parse_args()
    build(a.root, a.tier_b, a.missing_tier_a)
    print(f"built {a.root}")
