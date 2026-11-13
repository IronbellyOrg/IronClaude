"""Wave 5: render REPORT.md (UC-1) from the validated artifacts. Reads coverage-matrix.json, refactor-plan.md (finding table), merged-verdict.yaml."""
import json
import re
import sys

out = sys.argv[1]
base = ".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/"
SPEC, PLAN = base + "source.md", base + "TASK-WF-designSpec-20261107-075614.md"
cm = json.load(open(f"{out}/artifacts/coverage-matrix.json"))
plan = open(f"{out}/adversarial/adversarial/refactor-plan.md", encoding="utf-8").read()
tbl = plan.split("## Final merged findings")[1].split("## Risk Summary")[0]
findings = []
for line in tbl.splitlines():
    if line.startswith("| M-"):
        c = [x.strip() for x in line.strip("|").split("|")]
        findings.append(dict(id=c[0], sev=c[1], blocking=c[2], cat=c[3], src=c[4], claim=c[5], cites=c[6]))
assert len(findings) == 14
for f in findings:  # validator dropped PLAN 168 under M-001 (it is the criteria header; the criteria start at 169)
    if f["id"] == "M-001":
        f["cites"] = f["cites"].replace("PLAN 52-60, 168", "PLAN 52-60")


def expand(c):
    return c.replace("SPEC ", f"source.md:").replace("PLAN ", "tasklist:")


hdr = """```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.66
citations_total: 151
citations_revalidated: 72
citations_dropped: 1
citations_inferred: 0
citation_budget_policy: sampled
coverage_degraded: parsed-sparse
```

> **Citation budget: sampled mode**
> - `citations_revalidated: 72` — the validator re-Read all 61 citations of the 14 merged findings and 11 of the 90 inferred-requirement rows (the other 79 rows passed the script's verbatim-quote check, not a validator re-Read).
> - `citations_dropped: 1` — drops observed in the sample only (M-001, `tasklist:168` is the "Acceptance criteria:" header; the criteria start at 169). This is the field that gates promotion (not applicable in UC-1).
> - `citations_dropped_extrapolated: 2` — `round(1 x (151 / 72))`. Recording-only.
> The extrapolated value is telemetry, not a verdict. The sample-count is what the validator actually examined; the extrapolation is what it would have found if the budget had permitted a full re-Read.
"""

rep = [f"# Reflect REPORT: pre-execution audit of the pr-submit merge guard plan (UC-1)\n\n{hdr}\n"]
rep.append(f"""## Summary

- Spec: `{SPEC}` (design spec v3, 378 lines). Plan: `{PLAN}` (13 tasks).
- Result: **0 blocking findings, 6 MAJOR and 8 MINOR non-blocking.** The plan is executable with amendments; status is `partial` because the evidence validator dropped one citation, and the debate convergence is `BLOCKED_BY_INVARIANTS` (one HIGH invariant, INV-001, stayed unaddressed at depth standard).
- Coverage: `coverage_pct` null (the spec's FR-/F-/G-/O- labels do not match the ID regex, so 0 parsed ids); `coverage_pct_union` 0.8222 (74 of 90 inferred rows matched by word-overlap); `coverage_degraded: parsed-sparse` forced Tier 2 together with the `--tier 2` pin. All 16 unmatched rows have a covering task on a manual read, so the gap list below does not come from them.
- Tier 2 panel: 3 reviewers (analyzer / qa / refactorer) on the sonnet, haiku and opus classes, 3 of 3 complete, 19 findings, 19 of 19 calibrated; adversarial debate at depth standard (2 rounds plus invariant probe), convergence 0.9524 (20 of 21 points), merged into 14 findings.
- Attribution: the plan was already executed (PR #428). Findings are plan or spec defects only; nothing here rests on post-implementation HEAD state, except the corroboration noted in M-001 that the shipped code added a `REBIND` action (`src/superclaude/pr_submit/merge_guard.py:438-442`).
""")

rep.append("## Merged findings\n\nAll findings are Grounded (cited lines re-read by the evidence validator). UC-1 has no deviation classes; severity and blocking are the Round 2 rulings.\n")
for f in findings:
    rep.append(f"""### Finding {f['id']} ({f['sev']}, blocking: {f['blocking']}): {f['claim'].split(';')[0].split(',')[0][:110]}

- **Category:** {f['cat']}
- **Sources:** {f['src']}
- **Claim:** {f['claim']}
- **Citations:** {expand(f['cites'])} (SPEC = `source.md`, PLAN = `tasklist` in `{base}`)
""")

rep.append("## Inferred requirements (Pass 2)\n\n| INF id | Verbatim quote | Citation (file:line) | Match result |\n|---|---|---|---|\n")
for r in cm["rows"]:
    q = r["quote"].replace("|", "\\|").replace("\n", " ")
    m = f"{r['matched_task_ids'][0]} ({r['best_ratio']})" if r["matched_task_ids"] else f"none ({r['best_ratio']}); manual read: covered"
    rep.append(f"| {r['requirement_id']} | {q} | source.md:{r['citation_line']} | {m} |\n")
rep.append("\nPOSTSCRIPT: 0 inferred rows were dropped (all 90 quotes are verbatim on their cited line by script; 11 re-read by the validator, 11 of 11 founded). `coverage_pct_union` 0.8222, `unmapped_requirements_union` 16 ids (INF-004, 010, 013, 023, 034, 044, 045, 046, 048, 049, 052, 075, 078, 079, 080, 081), `S_dev_density` 0.1778, all unchanged by the validator.\n\n")

rep.append("""## Tier 2 panel and shadow-mode notes

- Panel resolution (`panel/resolution.json`): sonnet (t1b-1), haiku (t4-1), opus (t1a-1); `panel_parity: true`. This run's alias env: sonnet = `claude-gw-tier1b[1m]`, haiku = `claude-haiku-5-5`, opus = `gpt-6-luna`; the resolution records the class rotation, not the served model.
- Identity: `identity_source: requested-pinned`. Reviewer 3 self-reported `gpt-6-luna` against the pin `claude-opus-5-5`, so `identity_mismatch_suspected: true` (expected for this alias set, not an error). Reviewers 1 and 2 self-reported `claude-gw-tier1b[1m]` and `claude-haiku-5-5`. No claim of verified independence is made.
- Calibration: every card calibrated blind by the opus class; the opus class is also reviewer 3's class, so `calibrator_diversity: degraded`. Card scores 0.67 / 0.71 / 0.61; T1 card 0.64.
- Debate: orchestrator and judge are `claude-gw-tier1b[1m]` (sonnet class), the same class as reviewer 1, so `judge_class_collision: true`. The dual-pass position-bias check was not run as two independent evaluations (`fallback_mode: true`).
- Cluster agreement 0.3357 is telemetry only; the cluster command grouped seven distinct reviewer-1 findings with reviewer 3's single finding in cluster C1 (identical fingerprint with empty refs), so it understates both agreement and distinctness.
- Pre-check: 8 quote-not-found flags, all reviewer 2's quotes with markdown backticks stripped; the merged citations are line ranges and were re-read by the validator.

## Inferred-claim audit

- `citations_inferred: 0`
- Inferred-fraction: `0 / 151` = 0.00
""")

rep.append("""
## Recommendations

### Recommendation R-001: Define when the guard's cycle_id is set and how a later cycle reuses a held draft
- **File:** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md` (fold effect table and engage rows) and Task 3 of the plan
- **Change:** Add a fold effect row that sets `cycle_id` on a request and a decision for "later cycle finds the guard HELD" (rebind or refuse), and state which function enforces "once per cycle id".
- **Verifier:** a Task 3 fold test and a Task 4 engage test that fail if `cycle_id` stays stale or a RELEASED guard re-engages for the same id; `uv run pytest tests/pr_submit/test_merge_guard.py -q`
- **Linked deviation(s):** M-001
- **Priority:** P1

### Recommendation R-002: Resolve the zero-edit release against an unpublished earlier cycle
- **File:** `source.md` release table (rows 7 and 8) and plan Task 4
- **Change:** Say whether `applied_edits == 0` may release when an earlier cycle's fix is committed but unpublished, and add the missing release condition or an explicit accepted-risk sentence.
- **Verifier:** a Task 4 test with an earlier HOLD cycle followed by a zero-edit cycle asserts the chosen outcome
- **Linked deviation(s):** M-005, M-004
- **Priority:** P1

### Recommendation R-003: Restore spec sections 4.2 to 4.4 to Task 8 and add a call-site criterion for the per-cycle edit count
- **File:** plan Task 8 (source sections and acceptance criteria)
- **Change:** Change "sections 3, 4.1, 4.5, 4.6 and 5" to cover 3 and 4.1 to 4.4, 4.5, 4.6 and 5; add criteria that the ref names the event fields (`timeline_baseline`, `original_is_draft`, the idempotency key) and passes this cycle's applied-edit count, and make Task 1's O1 criterion require a single named source.
- **Verifier:** `uv run pytest tests/pr_submit/test_merge_guard_protocol.py -q` with new phrase assertions
- **Linked deviation(s):** M-002, M-004
- **Priority:** P1

### Recommendation R-004: Decide the failed-first-engage and resume row cases
- **File:** `source.md` engage row 6 and resume rows 4 to 6; plan Tasks 3, 4 and 11
- **Change:** Let engage row 6 check the live draft state, say where resume gets `target_sha`, give resume row 6 a phase condition, and add one test per case.
- **Verifier:** Task 4 parametrized tests per row; Task 11 crash scenario test
- **Linked deviation(s):** M-003, M-006, M-008
- **Priority:** P2

### Recommendation R-005: Give each body-only requirement an acceptance criterion and fix the dependency line
- **File:** plan Tasks 1, 9, 10, 11, 12
- **Change:** Add criteria for the flag-row and wave-line tests, the engage-failure message, the shared cycle id across guard, push and re-trigger events, the no `file:NNN` rule outside Task 8, the PR-body gate statement; add `Depends on: Task 8` to Task 10; replace Task 2's grep criterion with an exact-count assertion.
- **Verifier:** each new criterion is a named test; re-read the plan for one `Depends on:` line per consumed task
- **Linked deviation(s):** M-009, M-010, M-011, M-012, M-013
- **Priority:** P2

### Recommendation R-006: Reconcile `guard_status` with the unavailable halt
- **File:** `source.md` `guard_status` mapping and plan Task 3
- **Change:** State what is reported when an engage halt writes no event, and clarify the `OFF` wording.
- **Verifier:** a Task 3 `guard_status` case for the no-record halt
- **Linked deviation(s):** M-007, M-008
- **Priority:** P2
""")
open(f"{out}/REPORT.md", "w", encoding="utf-8").write("".join(rep))
print(len("".join(rep)), "chars")
