"""Record completion-claim searches, local links and captured marker comparisons."""
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

import yaml

ARTIFACTS = Path(__file__).resolve().parent
ROOT = ARTIFACTS.parents[4]
ALL = ["README.md", "command-reference.md", "user-guide.md", "monitoring-patterns.md", "observability-procedure.md", "operator-runbook.md"]
names = ALL[:3] if sys.argv[1] == "reference" else ALL
log = ARTIFACTS / ("reference-doc-check.txt" if sys.argv[1] == "reference" else "monitoring-doc-check.txt")
lines = ["CHECK: completion claims, related local links and captured marker fields"]
errors = []
search = re.compile(r"done\.json|sentinel|write_done_sentinel|terminal_status|contract_path|test_quickstart", re.I)
stale = re.compile(r"test_quickstart_does_not_emit_done_sentinel|written only by.{0,30}kill|absent on inline runs|default inline.{0,40}(?:does not|never)|Not.{0,20}emitted by a run.{0,20}done\.json", re.I)

def anchors(text):
    result = set()
    for heading in re.findall(r"^#{1,6}\s+(.+)$", text, re.M):
        plain = re.sub(r"[`*_~]", "", heading).lower().strip()
        plain = "".join(c for c in plain if c in " -_" or unicodedata.category(c)[0] in "LN")
        result.add(plain.replace(" ", "-"))
    result.update(re.findall(r'(?:id|name)=[\"\']([^\"\']+)[\"\']', text))
    return result

for name in names:
    path = ROOT / "docs/swarm" / name
    text = path.read_text()
    if name in ("README.md", "command-reference.md"):
        rows = text.splitlines()
        marker_rows = [i for i, row in enumerate(rows) if row.startswith("| `done.json` |")]
        if len(marker_rows) != 1 or marker_rows[0] == 0 or not rows[marker_rows[0] - 1].startswith("| `return-contract.yaml` |"):
            errors.append(f"done.json is not inside the artifact table in {name}")
        else:
            lines.append(f"TABLE OK {name}: done.json follows contract row without a table break")
    for number, line in enumerate(text.splitlines(), 1):
        if search.search(line):
            lines.append(f"HIT {path.relative_to(ROOT)}:{number}: {line}")
    if stale.search(text):
        errors.append(f"stale completion claim in {name}")
    for destination in re.findall(r"\[[^\]\n]*\]\(([^\s)]+)\)", text):
        if re.match(r"[a-z]+:", destination, re.I):
            continue
        file_part, _, fragment = unquote(destination).partition("#")
        target = (path.parent / file_part).resolve() if file_part else path
        if not target.is_file():
            errors.append(f"missing link {name} -> {destination}")
        elif fragment and fragment not in anchors(target.read_text()):
            # Identify unchanged baseline anchor defects, without repairing unrelated docs.
            before = subprocess.run(["git", "show", f"HEAD:{target.relative_to(ROOT)}"], cwd=ROOT, capture_output=True, text=True)
            source_before = subprocess.run(["git", "show", f"HEAD:{path.relative_to(ROOT)}"], cwd=ROOT, capture_output=True, text=True)
            if before.returncode == source_before.returncode == 0 and destination in source_before.stdout and fragment not in anchors(before.stdout):
                lines.append(f"PREEXISTING anchor mismatch (unchanged): {name} -> {destination}")
            else:
                errors.append(f"new anchor mismatch {name} -> {destination}")
        else:
            lines.append(f"LINK OK {name} -> {destination}")

out = ARTIFACTS / "foreground-cli"
marker = json.loads((out / "done.json").read_text())
contract = yaml.safe_load((out / "return-contract.yaml").read_text())
state = json.loads((out / ".swarm-state.json").read_text())
expected = {"atomic_write": True, "terminal_status": contract["status"], "contract_path": str((out / "return-contract.yaml").resolve())}
if marker != expected or state["state"] != "terminal":
    errors.append("captured marker does not match persisted result/state")
count = sum(1 for p in out.iterdir() if p.is_file())
if count != 13:
    errors.append(f"captured stub output count is {count}, not 13")
lines.append(f"CAPTURE: marker fields/status/path match; state={state['state']}; default foreground file count={count}")
lines.extend("ERROR " + error for error in errors)
lines.append("CHECK: " + ("FAIL" if errors else "PASS"))
with log.open("a", encoding="utf-8") as stream:
    stream.write("\n".join(lines) + "\n")
print("\n".join(lines))
sys.exit(bool(errors))
