"""Read-only measurement: what would each candidate rule do to this host's worktrees.

Only key names, counts and paths are printed; config values are never printed.
Every git call is read-only and runs with -c core.fsmonitor=false (the readers
themselves start a program if fsmonitor is set; measured in repro2.sh).
"""
import json
import subprocess
from pathlib import Path

ps = json.loads(
    subprocess.run(
        ["orca-ide", "worktree", "ps", "--json"], capture_output=True, text=True, check=True
    ).stdout
)
items = ps["result"]["worktrees"]
print("worktrees listed:", len(items), "truncated:", ps["result"].get("truncated"))
seen = []
for it in items:
    p = Path(it["path"]).resolve()
    if p not in seen:
        seen.append(p)
print("distinct paths:", len(seen))


def git(path, *a, inp=None):
    return subprocess.run(
        ["git", "--no-optional-locks", "-c", "core.fsmonitor=false", "-C", str(path), *a],
        capture_output=True, input=inp, timeout=60,
    )


rows = []
for p in seen:
    r = {"path": str(p), "reasons": []}
    if not p.exists():
        r["reasons"].append("path missing")
        rows.append(r)
        continue
    c = git(p, "config", "--show-origin", "--list", "-z")
    if c.returncode != 0:
        r["reasons"].append("config unreadable")
        rows.append(r)
        continue
    entries = [e for e in c.stdout.decode("utf-8", "replace").split("\0") if e]
    # -z with --show-origin: origin\0key\nvalue\0  -> pairs
    cfg = []
    it2 = iter(entries)
    for origin in it2:
        kv = next(it2, "")
        k, _, v = kv.partition("\n")
        cfg.append((origin, k.lower(), v))
    fsm = [(o, v) for o, k, v in cfg if k == "core.fsmonitor"]
    live_fsm = [(o, v) for o, v in fsm if v.strip().lower() not in ("false", "0", "no", "off", "")]
    r["fsmonitor_set"] = len(live_fsm)
    if live_fsm:
        r["reasons"].append("core.fsmonitor set (" + ",".join(sorted({o.split(":")[0] for o, _ in live_fsm})) + ")")
    drivers = {}
    for o, k, v in cfg:
        parts = k.split(".")
        if len(parts) >= 3 and parts[0] == "filter" and parts[-1] in ("clean", "process") and v.strip():
            drivers.setdefault(".".join(parts[1:-1]), set()).add(o.split(":")[0])
    r["driver_names"] = sorted(drivers)
    r["driver_origins"] = {k: sorted(v) for k, v in drivers.items()}
    env_keys = sorted({o for o, k, v in cfg if o.startswith("command line")})
    r["has_command_line_scope"] = bool(env_keys)
    if drivers:
        ls = git(p, "ls-files", "-z")
        paths = ls.stdout
        ca = git(p, "check-attr", "--stdin", "-z", "filter", inp=paths)
        parts = ca.stdout.decode("utf-8", "replace").split("\0")
        used = {}
        for i in range(0, len(parts) - 2, 3):
            val = parts[i + 2]
            if val in drivers:
                used[val] = used.get(val, 0) + 1
        r["drivers_selected_by_tracked_paths"] = used
        for d in used:
            r["reasons"].append(f"filter '{d}' selected by {used[d]} tracked path(s), origin {sorted(drivers[d])}")
    # submodules (gitlinks)
    ls = git(p, "ls-files", "-s", "-z")
    r["submodules"] = sum(1 for e in ls.stdout.split(b"\0") if e.startswith(b"160000"))
    rows.append(r)

refused = [r for r in rows if r["reasons"]]
print("\nPROPOSED rule (refuse on fsmonitor OR a selected filter): refused", len(refused), "of", len(rows))
for r in refused:
    print("  -", r["path"], "::", "; ".join(r["reasons"]))
fs_only = [r for r in rows if r.get("fsmonitor_set")]
print("\nworktrees with a live core.fsmonitor:", len(fs_only))
flt = [r for r in rows if r.get("drivers_selected_by_tracked_paths")]
print("worktrees with a filter selected by a tracked path:", len(flt))
print("worktrees defining any filter driver with clean/process (any origin):", sum(1 for r in rows if r.get("driver_names")))
orig = {}
for r in rows:
    for d, o in r.get("driver_origins", {}).items():
        orig[(d, tuple(o))] = orig.get((d, tuple(o)), 0) + 1
print("driver name/origin tally:", orig)
print("worktrees with submodules:", sum(1 for r in rows if r.get("submodules")))
print("worktrees with command-line config scope (env/-c):", sum(1 for r in rows if r.get("has_command_line_scope")))
print("unreadable/missing:", [r["path"] + ": " + ",".join(r["reasons"]) for r in rows if any("unreadable" in x or "missing" in x for x in r["reasons"])])
