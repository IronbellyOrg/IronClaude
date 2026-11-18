import json, re
from pathlib import Path
R = Path("/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/COMPARE-review-panel-run1-vs-run2-20261114/adversarial")
s = json.loads((R/"partials/r2-state.json").read_text())
pc = json.loads((R/"partials/point-cluster.json").read_text())
names = {}
for l in (R/"debate-points.md").read_text().splitlines():
    m = re.match(r"\| (CL-\d+) \| (L\d) \| ([^|]+) \|", l)
    if m: names[m.group(1)] = (m.group(2), m.group(3).strip())
out = ["# Emerging Consensus after Round 2 (input to Round 2.5)\n",
       "Per-point final verdicts of both advocates are in partials/r2-advocate-V1.md and partials/r2-advocate-V2.md (tables 'Final verdicts' and 'Verdict changes'); cluster-level state below is computed from them. Convergence after R2 = 224 of 234 = 0.957; 10 points still disputed (listed in partials/convergence-r2.md).\n",
       "| Cluster | Level | Topic | V1 advocate (final) | V2 advocate (final) |", "|---|---|---|---|---|"]
for c,(lv,n) in sorted(names.items()):
    out.append(f"| {c} | {lv} | {n} | {s['V1']['cluster'].get(c,'-')} | {s['V2']['cluster'].get(c,'-')} |")
out.append("\nStill-disputed points: " + ", ".join(s['disagree']))
(R/"partials/consensus-summary.md").write_text("\n".join(out)+"\n")
print("ok")
