"""Generic offline worker driver (contract J9).  Each experiment's offline_advance.py is a 10-line wrapper around advance().

Ledger `offline/workers.json`: {"steps": [{"id", "kind", "model", "prompt", "out", "status", "relaunch"}]} (a bare list is accepted).
Prints `LAUNCH <abs prompt path> model=<m>`, `RUNNING n`, `MANUAL ...`, `ALL DONE`.  D6: no token or cost check exists in this file."""
import json
import os
import pathlib
import re
import time

from . import harnesslib as H


def _load(path):
    raw = json.load(open(path))
    return (raw, raw) if isinstance(raw, list) else (raw, raw["steps"])


def _save(path, raw):
    tmp = pathlib.Path(str(path) + ".tmp")
    tmp.write_text(json.dumps(raw, indent=1))
    os.replace(tmp, path)


def add_steps(ledger_path, steps) -> None:
    p = pathlib.Path(ledger_path)
    if p.exists():
        raw, cur = _load(p)
    else:
        raw = {"steps": []}; cur = raw["steps"]
    have = {s["id"] for s in cur}
    for s in steps:
        if s["id"] in have:
            continue
        cur.append({"status": "pending", "relaunch": 0, **s})
    p.parent.mkdir(parents=True, exist_ok=True)
    _save(p, raw)


def _transcripts(pattern_root):
    rx = re.compile(r"^Read (?P<path>\S+) and follow")
    out = {}
    for m, info in H.scan_by_first_message(H.tasks_glob(), rx):
        path = m.group("path")
        if re.search(pattern_root, path):
            out.setdefault(path, []).append(info)
    return out


def advance(ledger_path, pattern_root, max_concurrent: int = 6) -> int:
    p = pathlib.Path(ledger_path)
    raw, steps = _load(p)
    cap = min(max_concurrent, H.max_concurrent_env(max_concurrent))
    found = _transcripts(pattern_root)
    for s in steps:
        if s["status"] != "launched":
            continue
        out = pathlib.Path(s["out"])
        cands = found.get(s["prompt"], [])
        c = H.pick_transcript(cands, s["model"], key=s["id"]) if cands else None
        if c is not None and c["done"]:
            if out.exists():
                s["status"] = "done"
            else:
                print(f"MANUAL {s['id']} output missing")
                if s["relaunch"] >= 1:
                    s["status"] = "lost"
                    print(f"LOST {s['id']}: second failure (output missing)")
                else:
                    s["relaunch"] += 1
                    s["status"] = "pending"
        elif c is None and out.exists() and time.time() - out.stat().st_mtime >= H.QUIET_SECS:
            s["status"] = "done"
        elif c is None and not out.exists() and s.get("launched_at") \
                and time.time() - s["launched_at"] > H.STALE_SECS:
            print(f"WARN stale {s['id']}")
    running = sum(1 for s in steps if s["status"] == "launched")
    for s in steps:
        if s["status"] == "pending" and running < cap:
            print(f"LAUNCH {s['prompt']} model={s['model']}")
            s["status"] = "launched"; s["launched_at"] = time.time()
            running += 1
    _save(p, raw)
    open_steps = [s for s in steps if s["status"] in ("pending", "launched")]
    if not open_steps:
        lost = [s["id"] for s in steps if s["status"] == "lost"]
        if lost:
            print(f"MANUAL lost steps: {', '.join(lost)}")
        print("ALL DONE")
    else:
        print(f"RUNNING {running}")
    return 0
