"""Re-baseline only the externally drifted fields. Never installs, never touches the backup.

Run: uv run python -I <this file>   (from the repo root)
Reuses current() from compatibility_state.py without running its phase dispatch.
"""

import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
src = (HERE / "compatibility_state.py").read_text().split("\nphase = sys.argv[1]")[0]
ns = {"__name__": "compatibility_state_lib"}
sys.argv = ["compatibility_state.py", "lib"]
exec(compile(src, str(HERE / "compatibility_state.py"), "exec"), ns)

before_path = HERE / "compatibility-before.json"
original = HERE / "compatibility-before.original.json"
assert not original.exists(), "already re-baselined; inspect evidence"
before = json.loads(before_path.read_text())
state = ns["current"]()
assert ns["verify_backup"](before) == before["backup"], "backup no longer verifies"

DRIFT_KEYS = ("settings", "other_installed_digest", "other_installed_entries")
for key in before:
    if key in DRIFT_KEYS or key in ("backup", "selected_mode_tightening", "differing_files"):
        continue
    assert state[key] == before[key], key + " changed beyond the approved drift"
assert state["installed"] == before["installed"], "target changed since backup"

home = Path("/home/coder/.claude")
moved = [p for p in before["settings"] if state["settings"][p] != before["settings"][p]]
assert moved == [str(home / "settings.json")], moved  # only the global file may differ
old =json.loads((home / "settings.json.bak").read_text())
new = json.loads((home / "settings.json").read_text())
old_sha = before["settings"][str(home / "settings.json")]["sha256"]
bak_sha = ns["file_state"](home / "settings.json.bak")["sha256"]
assert bak_sha == old_sha, "settings.json.bak is not the baseline copy"
changed_keys = sorted(k for k in set(old) | set(new) if old.get(k) != new.get(k))
record = {
    "reason": "Files outside the plan changed after the baseline; not made by this run.",
    "approval": {
        "ask_message": "msg_396f577fa3cd",
        "answer_message": "msg_da4599a5fd9c",
        "answer_text": "ok",
        "interpretation": "Literal answer 'ok' to a question that recommended rebaseline-and-continue; read as approval of that option.",
    },
    "settings_global": {
        "path": str(home / "settings.json"),
        "old_sha256": old_sha,
        "new_sha256": new and state["settings"][str(home / "settings.json")]["sha256"],
        "pre_change_copy": str(home / "settings.json.bak"),
        "top_level_keys_changed": changed_keys,
        "permissions_equal": old.get("permissions") == new.get("permissions"),
        "model_old": old.get("model"),
        "model_new": new.get("model"),
        "hooks_same_set": sorted(json.dumps(x, sort_keys=True) for v in old.get("hooks", {}).values() for x in v)
        == sorted(json.dumps(x, sort_keys=True) for v in new.get("hooks", {}).values() for x in v),
    },
    "other_installed": {
        "old_entries": before["other_installed_entries"],
        "new_entries": state["other_installed_entries"],
        "old_digest": before["other_installed_digest"],
        "new_digest": state["other_installed_digest"],
        "known_new_entry": "setup-bmad (created 2026-11-09T16:03Z, after the baseline at 15:43Z)",
    },
    "unchanged_and_rechecked": [
        "source", "installed", "profiles", "project_mirrors", "binding", "roster", "backup",
    ],
}
shutil.copy2(before_path, original)
before.update({k: state[k] for k in DRIFT_KEYS})
before["rebaseline"] = record
before_path.write_text(json.dumps(before, indent=2) + "\n")
(HERE / "rebaseline-record.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps({k: record[k] for k in ("settings_global", "other_installed")}, indent=2))
