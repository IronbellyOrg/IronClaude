"""M4: document size at start and after each round for incident I5.

usage: uv run --no-project python -I m4.py <recon-dir> <final-package-dir> <delivery-list.json>
  recon-dir          folder with R1..R4/<id>/ (output of recon.py: package at the START of review k)
  final-package-dir  .dev/tasks/done/<id> from git b5c09e90 (package after review 4, archived)
  delivery-list.json output of `archive_workspace.py --print-state` (the 57 delivery files)
Sizes: bytes = sum of file sizes; lines = number of newline characters. "Round k" = review k plus the fix cycle after it,
so "after round k" is the state at the start of review k+1; "after round 4" is the final archived package.
"""
import json
import sys
from pathlib import Path

recon, final, dl = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
ID = "TASK-WF-writeTheP0LivePl-20261103-215902"
delivery = [f.split(ID + "/", 1)[1] for f in json.loads(dl.read_text())["files"]]


def size(paths):
    b = l = 0
    for p in paths:
        data = p.read_bytes()
        b += len(data)
        l += data.count(b"\n")
    return b, l


def measure(root):
    allf = sorted(p for p in root.rglob("*") if p.is_file())
    out = {}
    out["package_all_files"] = dict(zip(("bytes", "lines"), size(allf)), files=len(allf))
    out["delivery_files_57"] = dict(zip(("bytes", "lines"), size([root / d for d in delivery])), files=len(delivery))
    for name, rel in (("p0_phase_report", "artifacts/p0-phase-report.md"), ("ledger_progress_md", "progress.md"), ("plan", ID + ".md")):
        out[name] = dict(zip(("bytes", "lines"), size([root / rel])))
    return out


states = {
    "start_before_round1": measure(recon / "R1" / ID),
    "after_round1_fix": measure(recon / "R2" / ID),
    "after_round2_fix": measure(recon / "R3" / ID),
    "after_round3_fix": measure(recon / "R4" / ID),
    "after_round4_final_archived": measure(final),
}
base = states["start_before_round1"]
for st in states.values():
    for k, v in st.items():
        b0 = base[k]["bytes"]
        v["growth_pct_bytes_vs_start"] = round(100.0 * (v["bytes"] - b0) / b0, 3)
print(json.dumps(states, indent=1))
