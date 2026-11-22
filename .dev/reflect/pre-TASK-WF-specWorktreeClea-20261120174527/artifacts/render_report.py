"""Render REPORT.md for the UC-1 reflect run from the merged verdict and the coverage matrix.

Usage: render_report.py <out-dir> [validation.json]
validation.json (optional, written after the evidence-validator gate):
  {"dropped": [{"finding": "M-1", "evidence_prefix": "PLAN:62", "reason": "..."}],
   "inf_dropped": [{"id": "INF-007", "reason": "..."}],
   "revalidated": <int>}
"""

import json
import sys
from pathlib import Path

import yaml

OUT = Path(sys.argv[1])
VAL = json.loads(Path(sys.argv[2]).read_text()) if len(sys.argv) > 2 else None
mv = yaml.safe_load((OUT / "adversarial/merged-verdict.yaml").read_text())
cm = json.loads((OUT / "coverage-matrix.json").read_text())
rows = cm["rows"]

# Recommendation targets per finding: (file, verifier). Priority follows severity.
PLAN = "the plan file in the workflow package (TASK-WF-specWorktreeClea-20261120-173546.md)"
REC = {
    "M-1": (PLAN + ", Tasks 2 to 13", "Re-read every acceptance bullet of Tasks 2 to 13: none may name a file or test that a later task creates; the mechanical gate still passes."),
    "M-2": (PLAN + ", last task or a closing note", "Read the plan end: either a task or an explicit note names `/sc:pr-submit --monitor 3` as the finish, matching source.md lines 276 and 379."),
    "M-3": (PLAN + ", Task 19", "Count the rows of source.md section 12 (lines 314 to 328) and compare with the number written in Task 19."),
    "M-4": (PLAN + ", Task 1 and Task 11", "Read Task 1: item 1 carries its own spec fallback (source.md:297) and Task 11 has a step for deregistering from Orca."),
    "M-5": (PLAN + ", Task 1", "Task 1 asks for the `OPEN` token on an open pull request (source.md:299) as well as `MERGED`."),
    "M-6": ("source.md lines 83 and 214 (owner decision)", "The owner states whether a patch-and-bundle save of tracked edits is in version 1; the plan then matches."),
    "M-7": (PLAN + ", Task 1 and Task 13", "Task 1 states that `branch-landed.sh` fetches; Task 13 tests the helper integration apart from canned replies."),
    "M-8": (PLAN + ", Task 6, Task 12 and Task 20", "A task writes the recorded command list into the JSON (or a sibling file) and Task 20 reads it from there."),
    "M-9": (PLAN + ", Task 2", "Task 2 holds a positive list of allowed command shapes and a test that `git reset` is refused."),
}

fm = [f for f in mv["findings"]]
n_evid = sum(len(f.get("evidence", [])) for f in fm)
dropped = VAL["dropped"] if VAL else []
dropped_keys = {(d["finding"], d["evidence_prefix"]) for d in dropped}
inf_dropped = {d["id"] for d in (VAL["inf_dropped"] if VAL else [])}
surviving = [r for r in rows if r["requirement_id"] not in inf_dropped]
n_inf = len(rows)
citations_total = n_evid + n_inf
dropped_total = len(dropped) + len(inf_dropped)
revalidated = VAL["revalidated"] if VAL else 0
matched = sum(1 for r in surviving if r["match_method"] == "containment")
cov_union = round(matched / len(surviving), 4) if surviving else None
unmapped = [r["requirement_id"] for r in surviving if r["match_method"] == "none"]
density = round(len(unmapped) / len(surviving), 4) if surviving else None

L = []
A = L.append
A("# Reflect report (UC-1, pre-execution)")
A("")
A("```yaml")
A('contract_version: 1.8.0')
A('status: partial')
A('mode: pre')
A('tier_reached: 2')
A('confidence_calibrated: 0.76')
A(f'citations_total: {citations_total}')
A(f'citations_revalidated: {revalidated}')
A(f'citations_dropped: {dropped_total}')
A('citations_inferred: 0')
A('citation_budget_policy: sampled')
A('coverage_degraded: parsed-sparse')
A("```")
A("")
A("> **Citation budget: sampled mode**")
A(f"> - `citations_revalidated: {revalidated}` - size of the re-Read sample (the finding citations in full, plus a sample of the inferred-requirement rows; every inferred row was also checked verbatim by `artifacts/coverage_match.py`).")
A(f"> - `citations_dropped: {dropped_total}` - drops observed in the sample only.")
A("> - The extrapolated value is telemetry, not a verdict. The sample-count is what the validator actually examined.")
A("")
A(f"**Verdict: {mv['verdict']}** (advisory). The plan `TASK-WF-specWorktreeClea-20261120-173546.md` is checked against `source.md` (the issue 687 spec). Why `status: partial`: convergence of the debate is blocked by four HIGH invariants, one grade dispute is open, and both reviewer cards were cut off by a transport limit. Reflect never edits the plan.")
A("")
A("Run facts: Tier 2 (forced by the parse-density guard: 0 labeled requirements, 82 inferred rows); reviewers opus class (analyzer) and haiku class (qa), executor class sonnet excluded, calibrator sonnet class; Tier 1 card calibrated 0.65, reviewer cards 0.75 and 0.76; adversarial convergence 0.9231 over 13 diff points; base variant 2; codegraph index fresh (checked 2026-11-20T17:38:06Z); no verification run (UC-1).")
A("")
A("## Coverage")
A("")
A(f"- Parsed requirements: 0 (`coverage_pct` null, `coverage_undefined` false). Inferred requirements: {len(surviving)}. `coverage_pct_union`: {cov_union}. `S_dev_density`: {density}.")
A(f"- Unmapped by the lexical containment rule (union): {', '.join(unmapped) or 'none'}. The rule is lexical, so the Tier 1 calibrator also found wrong-task matches (for example INF-082, INF-002, INF-057); the matrix is a lead, not a proof.")
A("")
A("## Findings")
A("")
for f in fm:
    keep = [e for e in f.get("evidence", []) if (f["id"], e.split(" ")[0]) not in dropped_keys]
    A(f"### Finding {f['id']} ({f['severity']}, ground: {f.get('grade_ground', 'none')})")
    A("")
    A(f"- **Claim:** {f['claim']}")
    A("- **Evidence:**")
    for e in keep:
        A(f"  - {e}")
    if len(keep) < len(f.get("evidence", [])):
        A(f"  - (dropped by the evidence gate: {len(f['evidence']) - len(keep)})")
    A(f"- **Consequence:** {f['consequence']}")
    A(f"- **Suggested fix:** {f['suggested_fix']}")
    A(f"- **Provenance:** {f['provenance']}")
    A("")
A("## Unresolved conflicts")
A("")
for c in mv["unresolved_conflicts"]:
    A(f"- {c['id']}: {c['topic']}. Variant 2: {c['position_variant_2']} Variant 1 and the calibrator: {c['position_variant_1_advocate_and_calibrator']} Used: {c['resolution_used']}")
A("")
A("## Checked and found sound")
A("")
for s in mv["checked_and_found_sound"]:
    A(f"- {s}")
A("")
A("## Coverage gaps")
A("")
for s in mv["coverage_gaps"]:
    A(f"- {s}")
A("")
A("## Inferred requirements (Pass 2)")
A("")
A("| INF id | Verbatim quote | Citation (file:line) | Match result |")
A("|---|---|---|---|")
for r in surviving:
    q = r["quote"].replace("|", "\\|")
    res = ", ".join(r["matched_task_ids"]) + f" (containment {r['best_ratio']})" if r["matched_task_ids"] else f"none ({r['best_ratio']})"
    A(f"| {r['requirement_id']} | {q} | {r['citation']} | {res} |")
A("")
if inf_dropped:
    A("Postscript: dropped inferred rows (quote did not match the cited lines): " + ", ".join(sorted(inf_dropped)) + ".")
    A("")
A("## Inferred-claim audit")
A("")
A("- `citations_inferred: 0`")
A(f"- Inferred-fraction: `0 / {citations_total}` = 0.00")
A("")
A("## Recommendations")
A("")
order = {"BLOCKING": "P0", "MEDIUM": "P1", "NOTE": "P2"}
n = 0
for f in sorted(fm, key=lambda x: ["BLOCKING", "MEDIUM", "NOTE"].index(x["severity"])):
    n += 1
    tgt, ver = REC.get(f["id"], (PLAN, "Re-read the cited lines after the change and confirm the finding no longer applies."))
    A(f"### Recommendation R-{n:03d}: {f['suggested_fix'].split('.')[0][:110]}")
    A("")
    A(f"- **File:** {tgt}")
    A(f"- **Change:** {f['suggested_fix']}")
    A(f"- **Verifier:** {ver}")
    A(f"- **Linked finding:** {f['id']}")
    A(f"- **Priority:** {order[f['severity']]}")
    A("")
(OUT / "REPORT.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("citations_total", citations_total, "finding_evidence", n_evid, "inf", n_inf, "dropped", dropped_total)
