"""Render REPORT.md from merged-verdict.yaml + inferred-requirements + coverage-matrix (Wave 5)."""
import yaml
mv = yaml.safe_load(open("adversarial/merged-verdict.yaml"))
inf = {r["id"]: r for r in yaml.safe_load(open("artifacts/inferred-requirements.yaml"))["rows"]}
cm = yaml.safe_load(open("artifacts/coverage-matrix.yaml"))
fix_tasks = {"INF-037": "Task 4", "INF-056": "Task 5"}  # M-15 correction
out = []
w = out.append
w("# sc:reflect UC-1 report: Phase 2 codegraph plan\n")
w("```yaml")
w("contract_version: 1.8.0\nstatus: partial\nmode: pre\ntier_reached: 2\nconfidence_calibrated: 0.71\n"
  "citations_total: 193\ncitations_revalidated: 189\ncitations_dropped: 0\ncitations_inferred: 0\n"
  "citation_budget_policy: sampled\ncoverage_degraded: parsed-sparse")
w("```\n")
w("Plan: `.dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/TASK-WF-phase2CodegraphI-20261029-192001.md` (\"plan:\"). Spec: `source.md` in the same package (\"source.md:\"). "
  f"Merge: `adversarial/merged-verdict.yaml` (method {mv['merge_method']}, convergence {mv['convergence_score']}, {mv['convergence_status']}; INV-001 and INV-006 applied as corrections in M-02 and M-18, not re-debated). "
  "Coverage: Pass 1 0 ids, Pass 2 104 rows, containment 64/104 (0.6154), manual triage leaves 0 real gaps (`artifacts/unmapped-triage.yaml`); spans §2.1-§2.11, §3.1, §3.3-§3.4 and §4.2 have no matrix rows and rest on the by-reference triage (M-16).\n")
w("Status `partial`: the evidence gate dropped 0 of 189 re-read citations (zero-drop flag recorded, §11.2), but the adversarial merge reports BLOCKED_BY_INVARIANTS: INV-001 and INV-006 were applied as corrections (M-02, M-18) without a further debate round.\n")
w("> **Citation budget: sampled mode**\n> - `citations_revalidated: 189` of 193.\n> - `citations_dropped: 0` (sample count).\n> - `citations_dropped_extrapolated: 0`.\n> The extrapolated value is telemetry, not a verdict. The sample-count is what the validator actually examined; the extrapolation is what it would have found if the budget had permitted a full re-Read.\n")
w("## Deviations\n")
for f in mv["findings"]:
    head = f["claim"].strip().splitlines()[0].lstrip("- ").strip()
    w(f"### Deviation D-{f['id']}: {head[:110]}\n")
    w(f"- **Location:** {f['plan_ref']}")
    w(f"- **Spec section:** {f['spec_ref']}")
    w(f"- **Classification:** {f['class']} (origin: {f['origin']}; severity: {f['severity']})")
    w(f"- **Sources:** {', '.join(('; '.join(f'{k}: {v}' for k, v in x.items()) if isinstance(x, dict) else str(x)) for x in f['sources'])}")
    w("- **Evidence / claim:** " + " ".join(l.strip() for l in f["claim"].strip().splitlines() if l.strip()))
    w("- **Default remediation:** " + " ".join(l.strip() for l in str(f["fix"]).strip().splitlines() if l.strip()))
    w("")
w("## Inferred requirements (Pass 2)\n")
w("| INF id | Verbatim quote (truncated to 120 chars) | Citation | Match result |")
w("|---|---|---|---|")
for m in cm["matrix"]:
    q = inf[m["requirement_id"]]["quote"].replace("|", "\\|")[:120]
    res = (m["matched_task_ids"][0] if m["matched_task_ids"] else "none (see unmapped-triage.yaml)")
    if m["requirement_id"] in fix_tasks: res += f" (false match, corrected to {fix_tasks[m['requirement_id']]} per M-15)"
    w(f"| {m['requirement_id']} | {q} | {m['citation']} | {res} |")
w("\nPostscript: evidence-validator checked all 104 rows; 0 dropped.\n")
w("## Inferred-claim audit\n\n- `citations_inferred: 0`\n- Inferred-fraction: `0 / 193` = 0.00\n")
w("## Recommendations\n")
prio = {"important": "P1", "minor": "P2"}
for f in sorted(mv["findings"], key=lambda f: (prio.get(str(f["severity"]).split()[0], "P2"), f["id"])):
    w(f"### Recommendation R-{f['id']}: apply the {f['id']} fix")
    w(f"- **File:** {'reflect artifacts' if f['origin']=='reflect-artifact' else 'plan (and the spec when origin is inherited-from-spec)'}")
    w("- **Change:** " + " ".join(l.strip() for l in str(f["fix"]).strip().splitlines() if l.strip()))
    w(f"- **Verifier:** re-Read {f['plan_ref']} after the edit and run the edited acceptance line under `bash -euo pipefail` where it is a command")
    w(f"- **Linked deviation(s):** D-{f['id']}")
    w(f"- **Priority:** {prio.get(str(f['severity']).split()[0], 'P2')}\n")
open("REPORT.md", "w").write("\n".join(out) + "\n")
print(len(mv["findings"]), "findings rendered")
