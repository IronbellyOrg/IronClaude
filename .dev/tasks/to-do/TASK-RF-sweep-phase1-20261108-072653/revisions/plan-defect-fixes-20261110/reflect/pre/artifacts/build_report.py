"""Wave 5 report builder, sc-reflect UC-1 run 4 (revision plan-defect-fixes-20261110). Read-only on inputs.

Renders REPORT.md from adversarial/merged-verdict.yaml and coverage-matrix.yaml (nothing is retyped), extracts every cited
file:line + quote into artifacts/citations.json, and mechanically checks each quote against its cited range.
Run: uv run --no-project --with pyyaml python -I build_report.py [--final]
Without --final the validator-result lines of the header say PENDING; with --final they are read from evidence-validation.yaml.
"""
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path("/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode")
PKG = ".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653"
REV = f"{PKG}/revisions/plan-defect-fixes-20261110"
OUT = ROOT / REV / "reflect/pre"
ADV = OUT / "adversarial"
MV = yaml.safe_load((ADV / "merged-verdict.yaml").read_text())
MX = yaml.safe_load((OUT / "coverage-matrix.yaml").read_text())
AL = dict(MV["path_aliases"])
FINAL = "--final" in sys.argv


def norm(s):
    return re.sub(r"[\s`*_\\\"']+", "", s).replace("’", "")


def expand(ref):
    m = re.match(r"^([A-Za-z0-9_\-]+):(\d+)(?:-(\d+))?$", ref.strip())
    if not m or m.group(1) not in AL:
        return None
    a = int(m.group(2))
    return AL[m.group(1)], a, int(m.group(3) or a)


def walk(o, p=""):
    if isinstance(o, dict):
        if "ref" in o and "quote" in o:
            yield p, o["ref"], o["quote"]
        for k, v in o.items():
            yield from walk(v, p + "/" + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, p + f"[{i}]")


cites = []
fails = []
for n, (where, ref, quote) in enumerate(walk(MV), 1):
    e = expand(ref)
    ok = False
    if e:
        path, a, b = e
        p = Path(path) if path.startswith("/") else ROOT / path
        if p.exists():
            ls = p.read_text().split("\n")[a - 1 : b]
            ok = norm(quote) in norm("\n".join(ls))
    cites.append({"n": n, "where": where, "ref": ref, "path": e[0] if e else None, "start": e[1] if e else None, "end": e[2] if e else None, "quote": quote, "mechanical_ok": ok})
    if not ok:
        fails.append((n, ref))
(OUT / "artifacts/citations.json").write_text(json.dumps(cites, indent=1))
distinct = len({(c["path"], c["start"], c["end"]) for c in cites})
(OUT / "artifacts/citation-mechanical-check.json").write_text(json.dumps({"entries": len(cites), "distinct_ranges": distinct, "failures": fails}))

ev = None
if FINAL:
    ev = yaml.safe_load((OUT / "evidence-validation.yaml").read_text())

F = MV["findings"]
L = []
w = L.append
tot = ev["totals"] if ev else None
w("# Reflection report: sc:reflect UC-1 pre-execution, run 4, second bounded revision (plan-defect fixes F-01 to F-10)")
w("")
w("```yaml")
w("run_id: reflect-pre-20261110T0540Z-TASK-RF-sweep-phase1-run4-plan-defect-fixes")
w("mode: pre")
w("tier_reached: 2")
w("depth: deep")
w("tcs: 1860")
w(f"status: {'partial' if MV['convergence_status'] != 'CONVERGED' else 'success'}   # adversarial convergence_status {MV['convergence_status']}; see Findings M-01 and M-02")
w("plan_sha256: eb291f0bdd1a787131a3b5295150b0f109b46943a1c43c638fd2ad4652d29f99")
w("spec_sha256: e4a06d0cf1c2e81df1c61138587a511c5ccd065cd896a42bb6f04ab329afacf3")
w(f"citations_total: {len(cites)}")
w(f"citations_distinct_ranges: {distinct}")
w(f"citations_mechanical_failures: {len(fails)}")
if ev:
    w(f"citations_revalidated: {tot['verified']}")
    w(f"citations_dropped: {tot['dropped']}")
else:
    w("citations_revalidated: PENDING   # Wave 5 evidence validators")
    w("citations_dropped: PENDING")
w(f"coverage_pct: {MX['summary']['coverage_pct']}")
w(f"coverage_pct_union: {MX['summary']['coverage_pct_union']}")
w("```")
w("")
w("## 1. Verdict")
w("")
w(MV["verdict_recommendation"])
w("")
w(f"Findings: HIGH {MV['severity_counts']['HIGH']}, MEDIUM {MV['severity_counts']['MEDIUM']}, LOW {MV['severity_counts']['LOW']} (total {MV['severity_counts']['total']}). Authorization split: {MV['authorization_counts']}.")
w("")
w("Convergence: " + MV["convergence_detail"] + f" Status: {MV['convergence_status']}.")
w("")
w("## 2. Findings")
w("")
w("| Id | Severity | Scope | Location | Claim |")
w("|---|---|---|---|---|")
for f in F:
    w(f"| {f['id']} | {f['severity']} | {f['authorization']} | {f['location']} | {f['claim'].strip()[:200].replace('|', '/')}... |")
w("")
for f in F:
    w(f"### {f['id']} ({f['severity']}): {f['gap_class']}")
    w("")
    if f.get("severity_condition"):
        w(f"Condition: {f['severity_condition']}")
        w("")
    w(f"Tag: {f['tag']}. Location: {f['location']}. Authorization: {f['authorization']}.")
    w("")
    w(f"Claim: {f['claim'].strip()}")
    w("")
    w("Evidence:")
    w("")
    for e in f["evidence"]:
        w(f"- `{e['ref']}`: \"{e['quote']}\"")
    w("")
    w(f"Fix: {f['recommendation']['fix'].strip()}")
    w("")
    w(f"Verifier: {f['recommendation']['verifier'].strip()}")
    w("")
    if f.get("notes"):
        w("Notes:")
        for n_ in f["notes"]:
            w(f"- {n_}")
        w("")
w("## 3. Closure of the ten defects of run 3 (F-01 to F-10)")
w("")
w(MV["f_closure_summary"].strip() if isinstance(MV["f_closure_summary"], str) else str(MV["f_closure_summary"]))
w("")
w("| Id | Status | Scope status |")
w("|---|---|---|")
for c in MV["f_closure"]:
    w(f"| {c['id']} | {c['status']} | {str(c.get('scope_status', '')).replace('|', '/')} |")
w("")
for c in MV["f_closure"]:
    if c.get("evidence"):
        for e in c["evidence"]:
            w(f"- {c['id']} `{e['ref']}`: \"{e['quote']}\"")
w("")
w("## 4. Coverage (Wave 1)")
w("")
rc = MV["row_coverage"]
w(f"Parsed requirements covered: {rc['parsed']}. Union coverage: {rc['union']}. Unmapped (union): {rc['unmapped_union']}. The matrix (`coverage-matrix.yaml`) was rebuilt mechanically on the edited plan; INF-A06 and INF-A08 moved to covered after the second revision.")
w("")
for d in rc.get("dispositions", []):
    w(f"- {d.get('id')}: {d.get('matrix_status')} -> {str(d.get('disposition'))[:300]}")
w("")
w("## 5. Reviewers, calibration and merge")
w("")
w("| Card | Persona | Recorded model | Findings | Self C | Calibrated C | Calibrator |")
w("|---|---|---|---|---|---|---|")
w("| Tier 1 | requirements-analyst | claude-sonnet-5-5 | 0 HIGH, 0 MEDIUM, 9 LOW | 0.84 | 0.83 | haiku class (gpt-6.1-sol) |")
w("| Reviewer 1 | analyzer | claude-sonnet-5-5 | 0 HIGH, 4 MEDIUM, 1 LOW | 0.72 | 0.68 | haiku class (gpt-6.1-sol) |")
w("| Reviewer 2 | qa | gpt-6.1-sol | 2 HIGH | 0.89 | 0.86 | sonnet (claude-sonnet-5-5) |")
w("| Reviewer 3 | refactorer | claude-opus-5-5 (outside the Tier1b slots) | 3 LOW | 0.80 | 0.86 | sonnet (claude-sonnet-5-5) |")
w("")
w(f"Base variant: {MV['base_variant']}. Best-practice grade: {MV['best_practice_grade']} ({MV['best_practice_grade_reason']}). Calibrated confidence: {MV['confidence_calibrated']} ({MV['confidence_calibrated_basis']}).")
w("")
w("## 6. Invariant probe and what stays open")
w("")
w(f"Unaddressed HIGH: {json.dumps(MV['unaddressed_invariants_high'])[:900]}")
w("")
w(f"Consequence: {MV['consequence_note'].strip()}")
w("")
w("Residual notes:")
for r in MV["residual_notes"]:
    if isinstance(r, dict):
        w(f"- {r.get('note') or r.get('text') or json.dumps(r)[:400]}")
    else:
        w(f"- {r}")
w("")
w("## 7. Limits and disclosures")
w("")
w("- Reviewer 3 ran on claude-opus-5-5, outside the allowed Tier1b model slots; the other reflect stages ran on claude-sonnet-5-5 or gpt-6.1-sol.")
w("- Reviewers had no shell: they judged shell commands by reading; the operational QA agent simulated the F-01 commands in /tmp.")
w("- Reviewer briefs were slimmer than run 3's (a common file plus one lens file each, pointing at the live files and the diff against the baseline plan).")
w("- Reviewers and the Tier 1 analyst were launched in parallel; the deep override does not depend on the Tier 1 card.")
w("- The adversarial rubric passes were made by one merge-executor session (forward and reverse), not two independent judges.")
w("- Calibrator diversity is degraded (every available class is also a reviewer class). Vendor diversity is single.")
w("- The tracked file docs/memory/reflect/deviation-patterns-IronClaude.md was not written (avoids an unrelated tracked change).")
w("- Nothing was executed from the plan; model behaviour and installed activation are unverified.")
w("")
w("## 8. Citations (mechanical check)")
w("")
w(f"{len(cites)} cited quotes in `artifacts/citations.json`; {len(fails)} mechanical failures: {fails}.")
(OUT / "REPORT.md").write_text("\n".join(L) + "\n")
print(json.dumps({"entries": len(cites), "distinct": distinct, "failures": fails, "report_bytes": len("\n".join(L))}))
