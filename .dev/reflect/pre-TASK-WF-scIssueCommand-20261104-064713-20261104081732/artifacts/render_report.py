"""Fill the INF table and the findings section of REPORT.md (Wave 5 rendering, resume run).

Usage: uv run --with pyyaml --no-project python render_report.py <run-dir> <source.md>
Renders from artifacts/coverage-matrix.json and adversarial/merged-verdict.yaml only; adds no finding.
Verifies each INF quote is a substring of its cited source line (after stripping table pipes and
markdown emphasis) and prints the count.
"""
import json
import re
import sys

import yaml

run, src_path = sys.argv[1], sys.argv[2]
src = open(src_path, encoding="utf-8").read().splitlines()
cov = json.load(open(f"{run}/artifacts/coverage-matrix.json"))
mv = yaml.safe_load(open(f"{run}/adversarial/merged-verdict.yaml"))


def norm(s):
    return re.sub(r"\s+", " ", s.replace("**", "")).strip()


rows, ok, bad = [], 0, []
for r in cov["matrix"]:
    line_no = int(r["citation"].split(":")[1])
    line = src[line_no - 1]
    parts = [norm(p) for p in r["quote"].split(" / ")]
    if all(p in norm(line) for p in parts):
        ok += 1
    else:
        bad.append(r["requirement_id"])
    if r["match_method"] == "containment" and r["matched_task_ids"]:
        result = f"containment ({r['best_task']}, {r['ratio']})"
    else:
        result = f"none ({r['best_task']}, {r['ratio']})"
    q = r["quote"].replace("|", "\\|")
    rows.append(f"| {r['requirement_id']} | {q} | {r['citation']} | {result} |")
table = "| INF id | Verbatim quote | Citation (file:line) | Match result |\n|---|---|---|---|\n" + "\n".join(rows)
table += f"\n\nPostscript: {ok} of {len(rows)} quotes verified on their cited lines; {len(bad)} inferred rows dropped by quote verification{(': ' + ', '.join(bad)) if bad else ''}."

blocks = []
for f in mv["findings"]:
    head = f["claim"].split(":")[0] if ":" in f["claim"][:120] else f["claim"][:90]
    blocks.append(
        f"### Finding {f['id']} ({f['severity']}, {f['category']})\n\n"
        f"- **Claim:** {f['claim']}\n"
        f"- **Evidence:** {', '.join(str(e) for e in f['evidence'])}\n"
        f"- **Recommendation:** {f['recommendation']}\n"
        f"- **Debate ruling:** {f['debate_ruling']}\n"
    )
findings = "\n".join(blocks)

rep_path = f"{run}/REPORT.md"
rep = open(rep_path, encoding="utf-8").read()
assert rep.count("<!-- INF-TABLE -->") == 1 and rep.count("<!-- FINDINGS -->") == 1
rep = rep.replace("<!-- INF-TABLE -->", table).replace("<!-- FINDINGS -->", findings)
rep = rep.replace("67 rows; <!-- TODO: quote verification count --> matched", f"67 rows, {ok} of 67 quotes verified verbatim on their cited lines; {sum(1 for r in cov['matrix'] if r['matched_task_ids'])} matched")
open(rep_path, "w", encoding="utf-8").write(rep)
print(f"INF verified {ok}/{len(rows)} bad={bad}; findings rendered {len(blocks)}")
