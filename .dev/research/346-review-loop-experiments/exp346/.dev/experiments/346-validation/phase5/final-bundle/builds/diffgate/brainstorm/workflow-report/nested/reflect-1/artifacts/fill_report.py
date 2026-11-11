"""Fill REPORT.md table placeholders from coverage-matrix.json and merged-verdict.yaml (Wave 5 rendering only)."""
import json
import sys
from pathlib import Path

import yaml

R = Path(sys.argv[1])
rep = R / "REPORT.md"
cov = json.loads((R / "artifacts/coverage-matrix.json").read_text(encoding="utf-8"))
mv = yaml.safe_load((R / "nested/adversarial-1/adversarial/merged-verdict.yaml").read_text(encoding="utf-8"))


def cell(s, n=None):
    s = " ".join(str(s).split()).replace("|", "\\|")
    return s if n is None or len(s) <= n else s[: n - 3] + "..."


def cites(c):
    c = c if isinstance(c, list) else [c]
    out = []
    for x in c:
        x = str(x).replace(".dev/tasks/to-do/TASK-WF-spec-20261108-181640/TASK-WF-spec-20261108-181640.md:", "plan:")
        out.append(x)
    return ", ".join(out)


inf = ["| INF id | Verbatim quote | Citation | Match result |", "|---|---|---|---|"]
for r in cov["matrix"]:
    res = f"Task {r['best_task']} ({r['match_method']}, ratio {r['ratio']})"
    inf.append(f"| {r['requirement_id']} | {cell(r['quote'])} | {r['citation']} | {res} |")
inf.append("")
inf.append("Postscript: 0 rows dropped at emission; every quote re-checked as a verbatim substring of its cited line by artifacts/coverage.py at Wave 1B and again at Wave 5.")

fnd = ["| ID | Severity | Class | Citation | Finding | Fix |", "|---|---|---|---|---|---|"]
for f in mv["findings"]:
    cls = f["class"] + (f" ({f['subtype']})" if f.get("subtype") else "")
    flag = " **Needs owner ruling.**" if f.get("needs_owner_ruling") else ""
    fnd.append(f"| {f['id']} | {f['severity']} | {cls} | {cell(cites(f['citation']))} | {cell(f['finding'], 420)}{flag} | {cell(f['fix'], 320)} |")
fnd.append("")
fnd.append(f"Counts: HIGH {mv['counts']['HIGH']}, MEDIUM {mv['counts']['MEDIUM']}, LOW {mv['counts']['LOW']}. Advisory: " + "; ".join(cell(a["id"] + ": " + a["text"]) for a in mv.get("advisory", [])))
fnd.append("")
fnd.append("Note on the coverage artifact (not a plan finding): " + cell([n for n in mv["notes"] if "Coverage artifact" in n][0]))

text = rep.read_text(encoding="utf-8")
text = text.replace("{{RF_PLACEHOLDER:inferred}}", "\n".join(inf)).replace("{{RF_PLACEHOLDER:findings}}", "\n".join(fnd))
rep.write_text(text, encoding="utf-8")
print("filled", len(cov["matrix"]), "INF rows and", len(mv["findings"]), "findings")
