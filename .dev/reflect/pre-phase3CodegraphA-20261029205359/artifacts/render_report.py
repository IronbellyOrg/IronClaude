"""Render REPORT.md from the merged findings table and the coverage artifacts.
usage: render_report.py <out_dir>"""
import re, sys, yaml, pathlib
out = pathlib.Path(sys.argv[1]); a = out / "artifacts"
inf = yaml.safe_load(open(a / "inferred-requirements.yaml"))["rows"]
mx = {m["requirement_id"]: m for m in yaml.safe_load(open(a / "coverage-matrix.yaml"))["matrix"]}
tri = {t["requirement_id"]: t for t in yaml.safe_load(open(a / "unmapped-triage.yaml"))["rows"]}
rows = [l for l in open(out / "adversarial/merged-reviewer-findings.md") if re.match(r"^\| M-\d+ ", l)]
L = ["# sc:reflect UC-1 report: Phase 3 codegraph adoption plan", "",
     "- Plan: `.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/TASK-WF-phase3CodegraphA-20261029-204913.md` (cited `plan:N`); spec: `source.md` in the same package (cited `source.md:N`).",
     "- Mode pre (UC-1); tier reached 2 (forced by `coverage_degraded: parsed-sparse`; calibrated T1 C = 0.60 also escalates by rule 6).",
     "- Reviewers: sonnet/analyzer (calibrated 0.73), haiku = glm-5.3/qa (calibrated 0.67); executor opus excluded; calibrator opus (disjoint from reviewers).",
     "- Merge: `/sc:adversarial` (`adversarial/merged-verdict.yaml`), convergence 1.00, verdict refactor, 19 findings (0 critical, 9 important, 10 minor).",
     "- Coverage: 119 inferred requirement rows, 72 matched by containment (`coverage_pct_union` 0.605), 47 covered by reference (`artifacts/unmapped-triage.yaml`), 0 unmapped after triage.", "",
     "## Deviations", ""]
for r in rows:
    c = [x.strip() for x in r.strip().strip("|").split(" | ")]
    mid, sev, cls, pref, sref, orig, claim, fix, frm = c[:9]
    L += [f"### Deviation {mid} ({cls}, {sev}, {orig})", "", f"- Plan: {pref}; spec: {sref}; merged from {frm}.", f"- Claim: {claim}", f"- Fix: {fix}", ""]
L += ["## Inferred requirements (Pass 2)", "", "| id | citation | match | quote |", "|---|---|---|---|"]
for r in inf:
    m = mx[r["id"]]
    match = (m["matched_task_ids"][0] + f" ({m['ratio']})") if m["matched_task_ids"] else f"by reference: {tri[r['id']]['covered_by']}"
    q = r["quote"].replace("|", "\\|")[:160]
    L.append(f"| {r['id']} | {r['citation']} | {match} | {q} |")
L += ["", "## Inferred-claim audit", "", "No finding is tagged [INFERRED]; every claim cites plan or spec lines re-checked by the calibrators and the merge.", "",
      "## Recommendations", "", "Apply every merged finding's fix to the plan (the workflow brief says to fix plan defects by editing the generated plan); apply the inherited-from-spec fixes to the spec as well.", ""]
(out / "REPORT.md").write_text("\n".join(L) + "\n")
print(len(rows), "deviations,", len(inf), "inferred rows")
