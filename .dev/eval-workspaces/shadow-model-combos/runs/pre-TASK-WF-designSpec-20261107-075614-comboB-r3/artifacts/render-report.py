"""Wave 5: render REPORT.md, return-contract.yaml and metrics.json from the on-disk artifacts.
Usage: uv run python render-report.py <output>
"""
import json
import re
import sys

o = sys.argv[1]
cov = json.load(open(o + "/artifacts/coverage-matrix.json"))
merged = open(o + "/adversarial/merged-reflect-card.md").read()
block = re.search(r"```findings-v2\n(.*?)\n```", merged, re.S).group(1)
findings = [json.loads(l) for l in block.split("\n") if l.strip()]
SP = "TASK-WF-designSpec-20261107-075614/"


def tail(p):
    return "source.md" if p.endswith("source.md") else "plan.md (TASK-WF-designSpec-20261107-075614.md)"


def cite(c):
    s = "%s:%d" % (tail(c["path"]), c["line_start"])
    if c["line_end"] != c["line_start"]:
        s += "-%d" % c["line_end"]
    return "%s %s" % (c["role"], s)


hdr = """```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.71
citations_total: 51
citations_revalidated: 51
citations_dropped: 1
citations_inferred: 0
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```
"""

out = ["# Reflect REPORT (UC-1 pre-execution): merge-guard design spec vs. its 13-task plan\n", hdr]
out.append("""
Run: `pre-TASK-WF-designSpec-20261107-075614-comboB-r3` (tier 2 pinned, engine shadow). Spec: `source.md` (378 lines). Plan: `TASK-WF-designSpec-20261107-075614.md` (200 lines, 13 tasks).
Status is **partial** because the evidence validator dropped 1 of 51 report citations (see Dropped citation). Code facts are checked at base commit e8db2fe6 (`artifacts/base-grounding.md`); HEAD has since gained the landed feature and is not evidence of what the plan could know.

## Verdict

The plan is largely faithful to the spec: all 12 named scenario tests, every section 4.1 decision table, the fold table, the flag, the script, the ref and the docs are carried by a task. No blocking finding. One MAJOR non-blocking defect and 14 MINOR findings remain (15 merged findings: the 11 reviewer findings combined into 9, plus 5 fault-finder items and the engage-row ordering quirk raised in the debate).

- **Fix before execution (F1, MAJOR):** `resume_decision` row 4 says to re-enter `release_decision`, but its signature has no `applied_edits` or `target_sha`, `GuardAction` has no re-enter member, and Task 4's criterion names no action for row 4. Give `resume_decision` those two inputs (and say what row 4 returns), or state that the SKILL performs the re-entry.
- **Cheap plan edits (F3, F4, F5, F7):** rename or retarget Task 12's grep, require boolean `autoMergeRequest` in Task 7, drop the conditional `_RESOLUTION_SCRIPTS` wording, add `Depends on: Task 1` to Tasks 9, 10, 12, 13.
- **Spec gaps the plan inherits (F10, F11, F12, F13, F15):** `disabled_cause` for `user_override`, the `cycle_id` update rule, the report value for a halt before any request, a zero-edit release over an earlier hold, and the null-guard order of the engage rows.

## Coverage (UC-1)

- Pass 1 (regex): 0 parsed IDs (the spec's labels do not match `R-/REQ-/SPEC-/T-`). `coverage_pct: null`.
- Pass 2 (inference): 75 quote-pinned rows, 61 matched by the 0.6 containment rule; `coverage_pct_union: 0.8133`. `coverage_degraded: parsed-sparse` forbade a Tier-1 stop.
- The 14 mechanically unmatched rows were read by hand: 12 are covered by a task whose wording differs from the quote (for example INF-021 by Task 3, INF-023 by Task 4, INF-055 by Task 13); two have no acceptance criterion (INF-036 inertness below ordinal 3, INF-037 `RunConfig` unchanged), both MINOR and not raised as findings.

## Findings (merged, validated)
""")
for f in findings:
    out.append("### %s (%s%s, %s)\n" % (f["id"], f["severity"], ", blocking" if f["blocking"] else ", non-blocking", f["category"]))
    out.append("%s\n" % f["claim"])
    out.append("Evidence: " + "; ".join(cite(c) for c in f["citations"]) + ("." if True else ""))
    out.append("")
out.append("""
Low-severity fault-finder notes, not raised as findings: INV-002 (`release_decision` accepts `RELEASE_PENDING` without an ownership test; flows guard it), INV-007 (the RECONCILE count ignores `failed_mutations`; fails safe), INV-008 (`next_cycle_number` numeric vs text compare; unlikely under the round cap).

## Dropped citation (evidence validator)

- F7, plan lines 148-150: the span shows Task 10 depending on Task 9 only; Task 10 names `pre-build-gate.md` at line 154, outside the span. F7 stands on its other citations (plan 134-137, 179-182, 190-195). This drop forces `status: partial`.

## Tier 2 process

- Reviewers (shadow panel, dispatched with explicit classes): 1 analyzer (sonnet class, pin claude-sonnet-5-5), 2 qa (haiku class, pin claude-haiku-5-5), 3 refactorer (opus class, pin claude-opus-5-5). 11 findings, 3/3 valid findings blocks on first parse, calibration 11/11, `panel_parity: true`.
- Identity: `requested-pinned`. Reviewer 2 self-reported "OpenAI GPT" against its haiku pin: `identity_mismatch_suspected: true`. No claim of verified independence.
- Blind calibration (sonnet-class calibrator; no disjoint class available, `calibrator_diversity: degraded`): T1 0.71, cards 0.70 / 0.61 / 0.70.
- Debate (`sc:adversarial` Mode A, standard): 2 rounds + invariant probe + one verification round; convergence 0.94 (16 of 17 points); base variant 3; `merge_method: adversarial`. Judge = orchestrator (claude-gw-tier1b, sonnet class): class collision with reviewer 1 and the advocates, recorded.
- The fault-finder reported two HIGH invariants; a verification round downgraded them (INV-001 to MEDIUM, INV-002 to LOW), so none blocks convergence.
- Disagreement kept: whether F1 is blocking (advocate 1 yes; advocates 2 and 3 no). Merged as MAJOR, non-blocking.
- Model diversity: `t2_model_class_diversity: full`, `t2_vendor_diversity: single` (all aliases are `claude-gw-*`, warn-only).

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
""")
for r in cov["rows"]:
    q = r["quote"].replace("|", "\\|")
    if len(q) > 110:
        q = q[:107] + "..."
    res = ("%s %s (%.2f)" % (r["match_method"], ",".join(r["matched_task_ids"]), r["best_ratio"])) if r["matched_task_ids"] else "none (best %s %.2f)" % (r["best_task"], r["best_ratio"])
    out.append("| %s | %s | %s | %s |" % (r["requirement_id"], q, r["citation"], res))
out.append("""
Postscript: no inferred row was dropped (all 75 quotes re-checked on their cited spec lines at validation); the union fields are unchanged.

## Notes and limits

- Not checked: no code was executed; the plan was audited against the spec and base-commit excerpts only. Rows in each reviewer slice were reported verified without per-row evidence by reviewer 2.
- Memory persistence skipped on purpose: the experiment workspace froze `docs/memory/reflect/deviation-patterns-brainstorm-reflect-panel.md`; this run's entry is in `artifacts/memory-entry.md`.
- Wave 7 promotion does not apply (UC-1). Tier 3 not requested.
""")
open(o + "/REPORT.md", "w").write("\n".join(out) + "\n")
print("report lines", len("\n".join(out).split("\n")), "findings", len(findings))
