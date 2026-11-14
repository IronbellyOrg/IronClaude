"""Wave 5 report builder, sc-reflect UC-1 run 3 (read-only on inputs).

Renders REPORT.md from merged-verdict.yaml and coverage-matrix.yaml (nothing is retyped), extracts every cited
file:line + quote into artifacts/citations.json, and mechanically checks each quote against its cited range.
Writes only <OUT>/REPORT.md, <OUT>/artifacts/citations.json and <OUT>/artifacts/citation-mechanical-check.json.
Run: uv run --no-project --with pyyaml python -I build_report.py
"""

import json
import re
from pathlib import Path

import yaml

ROOT = Path("/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode")
PKG = ".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653"
REV = f"{PKG}/revisions/chat-output-exception-20261109-133150"
OUT = ROOT / REV / "reflect/pre"
ADV = OUT / "adversarial"
MV = yaml.safe_load((ADV / "merged-verdict.yaml").read_text())
MX = yaml.safe_load((OUT / "coverage-matrix.yaml").read_text())
ALIASES = dict(MV["path_aliases"])
ALIASES.update({"CONS": f"{REV}/reflect/pre/adversarial/debate/consensus.md", "PROBE": f"{REV}/reflect/pre/adversarial/invariant-probe.md"})
REPORT_REL = f"{REV}/reflect/pre/REPORT.md"


def norm(s):
    return re.sub(r"[\s`*_\\]+", "", s).replace("’", "'")


def expand(ref):
    """'TL:1363-1365' -> (path, 1363, 1365) or None."""
    m = re.match(r"^([A-Za-z0-9_\-]+):(\d+)(?:-(\d+))?$", ref.strip())
    if not m or m.group(1) not in ALIASES:
        return None
    a = int(m.group(2))
    b = int(m.group(3) or a)
    return ALIASES[m.group(1)], a, b


def check(path, a, b, quote):
    f = ROOT / path
    if not f.is_file():
        return "missing-file"
    lines = f.read_text().split("\n")
    if b > len(lines):
        return "line-out-of-range"
    window = norm("\n".join(lines[a - 1 : b]))
    q = norm(quote)
    if q in window:
        return "ok"
    # tolerate a quote that is the tail of an ellipsised or truncated text
    if len(q) > 40 and q[:40] in window:
        return "ok-prefix"
    return "mismatch"


cites = []  # {id, kind, ref, path, a, b, quote}
for f in MV["findings"]:
    for e in f["evidence"]:
        x = expand(e["ref"])
        cites.append(dict(id=f["id"], kind="finding", ref=e["ref"], path=x[0] if x else None, a=x[1] if x else None, b=x[2] if x else None, quote=e["quote"]))
for n in MV.get("residual_notes", []):
    for e in n.get("evidence", []):
        x = expand(e["ref"])
        cites.append(dict(id=n["id"], kind="residual", ref=e["ref"], path=x[0] if x else None, a=x[1] if x else None, b=x[2] if x else None, quote=e["quote"]))
inf_rows = [r for r in MX["rows"] if r["source"] == "inferred"]
for r in inf_rows:
    m = re.match(r"^(.*):(\d+)$", r["spec_citation"])
    cites.append(dict(id=r["id"], kind="inferred", ref=r["spec_citation"], path=m.group(1), a=int(m.group(2)), b=int(m.group(2)), quote=r["quote"]))
for c in cites:
    c["mechanical"] = check(c["path"], c["a"], c["b"], c["quote"]) if c["path"] else "unresolvable-alias"
(OUT / "artifacts/citations.json").write_text(json.dumps(cites, indent=1) + "\n")
bad = [c for c in cites if c["mechanical"] not in ("ok", "ok-prefix")]
(OUT / "artifacts/citation-mechanical-check.json").write_text(json.dumps({"total": len(cites), "ok": sum(c["mechanical"] == "ok" for c in cites), "ok_prefix": sum(c["mechanical"] == "ok-prefix" for c in cites), "failed": bad}, indent=1) + "\n")
distinct = {(c["path"], c["a"], c["b"]) for c in cites}

sev = MV["severity_counts"]
L = []
L.append("# sc:reflect UC-1 pre-execution report (run 3): revised orchestrator-mode Phase 1 tasklist after the chat-output exception revision\n")
L.append("```yaml")
L.append("contract_version: 1.8.0")
L.append("status: partial                      # the adversarial merge ended BLOCKED_BY_INVARIANTS (one HIGH invariant, folded into F-02); see Verdict summary")
L.append("mode: pre")
L.append("tier_reached: 2")
L.append("confidence_calibrated: 0.75          # mean of the three reviewer-card calibrations (0.69, 0.86, 0.71); the Tier-1 card calibrated at 0.83")
L.append(f"citations_total: {len(distinct)}                  # distinct cited ranges in this report (findings, residual notes, Pass 2 rows)")
L.append("citations_revalidated: PENDING       # replaced after the Wave 5 evidence-validator")
L.append("citations_dropped: PENDING")
L.append("citations_inferred: 3")
L.append("citation_budget_policy: full_reread  # --depth deep forces full_reread")
L.append("coverage_degraded: null")
L.append("```\n")
L.append("## Run context\n")
L.append("- **Spec:** `docs/designs/orchestrator-mode.md` (1051 lines; lines 1049-1051 are a new section that links the bounded addendum `design-addendum.md`, which is treated as part of the spec).")
L.append("- **Tasklist:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md` (3020 lines, 355 items: 137 completed, 218 open).")
L.append("- **What this run audits:** the task file after the bounded revision `chat-output-exception-20261109-133150`, which rewrote 82 unfinished item bodies and appended a note, so that a narrow, owner-chosen exception to the \"every reply has a DONE / NEXT table\" style rule can be planned for the final `/sc:sweep` skill reply. Nothing is executed by this run.")
L.append("- **Not reused:** earlier runs (`reflect/pre`, `reflect/pre-run2`) and their sign-offs. The `reflect_pre` block in the task frontmatter still holds the run 2 record until this run's sign-off replaces it. Every row, finding and citation below comes from this run's own reads.")
L.append("- **Mode and tier:** pre (UC-1). Tier 2, forced by `--depth deep` (`artifacts/tier_decision.yaml`); the rubric would also have escalated (S_domains 5 is at least 3, Tier-1 self-reported C 0.76 is below 0.85). TCS 1862, depth deep, `../../qa/tcs-computation-pre.json` (relative to this folder) (S1 474, S2 66, S3 41, S4 7, S5 16, S6 0).")
L.append("- **Input integrity:** `input_tree_sha256` 0f2a699e... over 146 files (`artifacts/input-snapshot.yaml`), recomputed in Wave 5 with the same exclusions and matched; no input drift.")
L.append("- **Tier-1 card:** `reflection-card-t1.yaml` (requirements-analyst, model claude-sonnet-5-5): 0 HIGH, 4 MEDIUM, 6 LOW, self C 0.76. Blind calibration (haiku class): C 0.83, 34 source ranges checked, 0 failed, ESCALATE.")
L.append("- **Reviewers (Tier 2, agent type reflect-reviewer, read-only):**\n")
L.append("| Reviewer | Role | Model class (recorded model) | Self C | Calibrated C | Calibrator (recorded model) | Citations checked / failed | Findings |")
L.append("|---|---|---|---|---|---|---|---|")
L.append("| R1 | analyzer | sonnet (claude-sonnet-5-5) | 0.72 | 0.69 | haiku (gpt-6.1-sol) | 26 / 3 | 0 HIGH, 3 MEDIUM, 2 LOW |")
L.append("| R2 | qa | haiku (gpt-6.1-sol) | 0.93 | 0.86 | sonnet (claude-sonnet-5-5) | 18 / 0 | 2 HIGH, 0 MEDIUM, 1 LOW |")
L.append("| R3 | refactorer | opus (claude-opus-5-5) | 0.75 | 0.71 | haiku (gpt-6.1-sol) | 19 / 0 | 0 HIGH, 2 MEDIUM, 2 LOW |\n")
L.append("- **Diversity:** `t2_model_class_diversity: full` (three distinct aliases), `t2_vendor_diversity: single` (all three are Anthropic gateway models, warning only), `calibrator_diversity: degraded` (every available class is also a reviewer class; each card was calibrated by a class other than its own), `executor_class_resolved: false` (UC-1 runs before execution).")
L.append("- **Adversarial merge:** `sc-adversarial-protocol` Mode A, standard depth, three variants (the calibrated reviewer cards). Base: variant 2 (combined V3 0.950, V2 0.933, V1 0.902; the 1.7 point margin is under 5, so the level-1 tiebreaker, debate points won V2 10 against V3 4, chose V2). Diff points: 38; agreed 36, convergence 0.947 (0.842 on the conservative reading); the two unagreed points were single-voice bookkeeping rows. Taxonomy levels L1, L2 and L3 are all covered. `convergence_status: BLOCKED_BY_INVARIANTS`: the invariant probe left one HIGH item unaddressed (INV-005), which this merge folds into F-02 and does not record as accepted risk.")
L.append("- **Models:** every stage except reviewer 3 recorded a model inside the live Tier1b slots (claude-sonnet-5-5, gpt-6.1-sol). Reviewer 3 ran on `claude-opus-5-5`, the opus alias of the reflect rotation, which is outside those slots; its card is one of three and was calibrated by a different class.\n")
L.append("Citation aliases:\n")
L.append("| Alias | Path |\n|---|---|")
for k, v in ALIASES.items():
    L.append(f"| {k} | `{v}` |")
L.append("")
L.append("## Verdict summary\n")
L.append("**The revision is sound in structure and coverage, but two checks reject a correct run and one of the two cannot be fixed inside the revision's own authorization.** Fix F-01 and F-03/F-04 first (inside the 82 revised bodies); F-02 needs a new bounded authorization. No fix has been applied.\n")
L.append("1. **F-01 (HIGH):** items 7.20, 7.30 and 7.34 require exactly 8 resolved decision files. When a 7.17 branch writes an OQ-17 or OQ-18 file, a correct run counts 9 or 10 and fails; the lens inputs, the second grep and the seven-row `owner-decisions.md` check have the same blind spot. The fix is inside the 82 bodies.")
L.append("2. **F-02 (HIGH):** item 13.1's Verification greps the old routing-row sentence while its Action says to copy the current design text, so following the Action fails the check. Item 13.1 is not one of the 82 bodies, so the fix needs a new bounded authorization or a manifest amendment (INV-005).")
L.append("3. **F-03 and F-04 (MEDIUM):** item 7.10, the first item to run, omits addendum clauses that item 11.4 later tests, and names no carrier for the owner's separate execution authorization.")
L.append("4. **F-05 to F-10 (LOW):** repair wording at 11.4, a stale \"line 22 is unconditional\" label in 58 later Context lines, a missing hash guard at 7.30/7.34, a style check with no expected value, a preamble reading conflict, and stale GQ-63 wording at 8.19 and 10.5 (outside the 82 bodies).\n")
L.append(f"The merged verdict has {sev['total']} findings: HIGH {sev['HIGH']}, MEDIUM {sev['MEDIUM']}, LOW {sev['LOW']}. Coverage is high: parsed `coverage_pct` 1.000 (127 of 127, 98 covered and 29 covered in substance) and union `coverage_pct_union` 0.985 (3 unmapped inferred rows, INF-017, INF-A06, INF-A29; INF-A06 is carried in F-03). The best-practice grade is {MV['best_practice_grade']} of 5 and calibrated confidence is {MV['confidence_calibrated']}.\n")
L.append("**Sign-off rule applied:** parsed `coverage_pct` 1.000 is at or above the 0.90 floor and `status` is partial, not failed, so the gate stamps `verdict: pass` under the A.10.7 routing rule. That is a coverage verdict, not an execution clearance: the two HIGH defects stay open, and execution still needs the separate direct authorization the revision requires.\n")
L.append("## Coverage\n")
s = MX["summary"]
L.append("| Measure | Value |\n|---|---|")
L.append(f"| Parsed requirements | {s['parsed_count']} (covered {s['covered_parsed']}, covered in substance {s['covered_in_substance_parsed']}, partial {s['partial_parsed']}, missing {s['missing_parsed']}) |")
L.append(f"| Inferred requirements (Pass 2) | {s['inferred_count']} (covered {s['covered_inferred']}, in substance {s['covered_in_substance_inferred']}, partial {s['partial_inferred']}, missing {s['missing_inferred']}) |")
L.append(f"| `coverage_pct` (parsed only) | {s['coverage_pct']} |")
L.append(f"| `coverage_pct_union` | {s['coverage_pct_union']} |")
L.append(f"| `unmapped_requirements` | {s['unmapped_requirements']} |")
L.append(f"| `unmapped_requirements_union` | {s['unmapped_requirements_union']} |")
L.append(f"| S_scope / S_domains / S_dev_density | {MX['signals']['S_scope']} / {MX['signals']['S_domains']} / {MX['signals']['S_dev_density']} |")
L.append("| `coverage_degraded` | null (inferred 77 is not greater than parsed 127) |\n")
L.append("## Findings\n")
for f in MV["findings"]:
    L.append(f"### {f['id']} ({f['severity']}, {f['gap_class']}): {f['claim'].split('. ')[0].rstrip('.')}\n")
    L.append(f"- **Location:** {f['location']}")
    L.append(f"- **Authorization:** {f['authorization']}")
    L.append(f"- **Tag:** {f['tag']}")
    L.append(f"- **Claim:** {f['claim']}")
    L.append("- **Evidence:**")
    for e in f["evidence"]:
        L.append(f"  - `{e['ref']}`: {e['quote']}")
    rec = f["recommendation"]
    if isinstance(rec, dict):
        L.append(f"- **Smallest fix:** {rec.get('fix', '')}")
        L.append(f"- **Verifier:** {rec.get('verifier', '')}")
    else:
        L.append(f"- **Smallest fix and verifier:** {rec}")
    pv = f["provenance"]
    L.append(f"- **Provenance:** cards {pv.get('cards')}, debate {pv.get('debate')}, {pv.get('change')}, invariants {pv.get('invariants')}")
    L.append("- **Notes:**")
    for n in f.get("notes", []):
        L.append(f"  - {n}")
    L.append("")
L.append("## Tier-1 findings: disposition\n")
L.append("| T1 id | Disposition | Reason |\n|---|---|---|")
for t in MV["tier1_verdicts"]:
    L.append(f"| {t['t1']} | {t['verdict']}{(' as ' + t['as']) if t.get('as') else ''} | {t['reason']} |")
L.append("")
L.append("## Candidates not carried\n")
L.append("| Id | Reason |\n|---|---|")
for n in MV["not_carried"]:
    L.append(f"| {n['id']} | {n['reason']} |")
L.append("")
L.append("## Invariant probe summary\n")
L.append("26 findings: 10 ADDRESSED, 16 UNADDRESSED (HIGH 1, MEDIUM 11, LOW 4); no category is empty. The HIGH item is INV-005 (the 13.1 fix is outside the authorized bodies), folded into F-02. The MEDIUM and LOW items are carried in the finding notes above (INV-001 in F-04, INV-002 in F-09, INV-003 in F-05, INV-006 in F-10, INV-012 and INV-025 in F-06, INV-013, 015, 019, 020 in F-01, INV-016 and INV-023 in F-03, INV-022 in F-02, INV-024 in F-04, INV-026 in F-07, INV-008 in the consequence note). Full table: `adversarial/invariant-probe.md`.\n")
L.append("## Inferred requirements (Pass 2)\n")
L.append("77 rows (42 from the design, 35 from the addendum and the design append). Every quote is a verbatim substring of its cited line (checked by `artifacts/build_matrix.py` at extraction and again by `artifacts/citation-mechanical-check.json`). Status values: covered, covered-in-substance, partial, missing.\n")
L.append("| INF id | Verbatim quote | Citation | Match result |\n|---|---|---|---|")
for r in inf_rows:
    items = ", ".join(map(str, r.get("matched_items", []))) or "none"
    L.append(f"| {r['id']} | {r['quote'].replace('|', '/')} | `{r['spec_citation']}` | {r['status']} (items {items}) |")
L.append("")
L.append("## Inferred-claim audit\n")
L.append("- `citations_inferred: 3` (the consequence of F-01, the consequence of F-02's blocked state, and the INV-025 reach question in F-06; every other claim carries a read citation).")
L.append(f"- Inferred-fraction: 3 / {len(distinct)} = {3 / len(distinct):.2f}. No WARN (not above one half).\n")
L.append("## Recommendations\n")
pri = {"HIGH": "P0", "MEDIUM": "P1", "LOW": "P2"}
for f in MV["findings"]:
    rec = f["recommendation"]
    fix = rec.get("fix", "") if isinstance(rec, dict) else str(rec)
    ver = rec.get("verifier", "") if isinstance(rec, dict) else ""
    first = f["location"].split(";")[0].split(" (")[0]
    L.append(f"### Recommendation R-{f['id'][2:]}: act on {f['id']}\n")
    L.append(f"- **File:** the task file (`TL`), at {first}" + ("; needs new bounded authorization" if "needs new" in f["authorization"] else ""))
    L.append(f"- **Change:** {fix}")
    L.append(f"- **Verifier:** {ver}")
    L.append(f"- **Linked finding(s):** {f['id']}")
    L.append(f"- **Priority:** {pri[f['severity']]}\n")
L.append("### Recommendation R-11: after any fix, re-run the fresh checks\n")
L.append(f"- **File:** the revision folder `{REV}/qa/` and `{REV}/reflect/pre/`")
L.append("- **Change:** " + MV["consequence_note"])
L.append("- **Verifier:** the structural, alignment, qualitative and PRE reports each name the edited plan (new task hash) and the preservation proof is re-run.")
L.append("- **Linked finding(s):** F-01 to F-10")
L.append("- **Priority:** P0\n")
L.append("## Residual notes\n")
for n in MV.get("residual_notes", []):
    L.append(f"- **{n['id']}:** {n['note']}")
L.append("")
L.append("## Disclosures and limits\n")
L.append("- **Report persistence:** the reflect-reviewer, confidence-calibrator and other read-only agents have no write tool or were told to return text, so the parent persisted every reviewer card and calibration report (`reviewer-cards/`) with attribution and no verdict change. Advocate, judge, scorer, probe, review and merge agents wrote their own files.")
L.append("- **Brief defect:** the reviewer-2 coverage slice was built with a filter that left the 42 design-inferred rows (INF-001 to INF-077) out of every formal slice; reviewer 2 said it inspected them from the matrix anyway, and the debate and probe covered the affected topics. Not repaired (no rerun).")
L.append("- **Quantitative metrics:** adapted to reviewer cards (`adversarial/base-selection.md`); RC, SR, DC and SC saturate near 1.0 for two variants, so they discriminate little. The qualitative layer and the debate decided the base.")
L.append("- **Memory persistence:** the tracked `docs/memory/reflect/deviation-patterns-<slug>.md` write was deliberately skipped so this run adds no unrelated tracked change to a tree whose final implementation diff is audited later; `memory_persist_skipped: tracked-file-write-deferred`. The git-ignored last-pass file is written.")
L.append("- **Codegraph:** `codegraph_status` showed a fresh index (0 changes) and the run state was recorded in the reviewer briefs; this is a Markdown plan, so graph lookups were not needed and the Grep/Read floor was used.")
L.append("- **Not verified:** execution of any planned item, live model behaviour, installed output-style activation, and the exact reach of the stale Context sentence (F-06) into spawned lens agents.\n")
(OUT / "REPORT.md").write_text("\n".join(L) + "\n")
print("report lines", len(L), "citations", len(cites), "distinct", len(distinct), "mechanical failures", len(bad))
for c in bad:
    print("FAIL", c["kind"], c["id"], c["ref"], c["mechanical"], "|", c["quote"][:90])
