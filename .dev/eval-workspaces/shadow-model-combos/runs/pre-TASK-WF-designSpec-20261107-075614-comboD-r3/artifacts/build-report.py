"""Wave 5: render REPORT.md from the validated artifacts (stub-first template refs/report-template.md).
usage: uv run python build-report.py <out>   (run from the repo root)"""
import json, pathlib, sys, time

out = pathlib.Path(sys.argv[1])
cov = json.loads((out / "artifacts" / "coverage-matrix.json").read_text())
S, M = cov["summary"], cov["matrix"]
F = [json.loads(l) for l in (out / "artifacts" / "merged-findings.checked.jsonl").read_text().splitlines()]
SPEC = ".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md"
short = lambda p: "plan" if p.endswith("075614.md") else "spec"

hdr = """```yaml
contract_version: 1.8.0
status: success
mode: pre
tier_reached: 2
confidence_calibrated: 0.65
citations_total: 111
citations_revalidated: 111
citations_dropped: 0
citations_inferred: 0
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```
"""
lines = ["# Reflect REPORT: pre-execution audit of the pr-submit merge guard plan (UC-1, Tier 2, shadow engine)", "", hdr]
lines += [
"Spec: `%s` (378 lines). Plan: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` (200 lines, 13 tasks)." % SPEC,
"Run: `pre-TASK-WF-designSpec-20261107-075614-comboD-r3` (model combination D: orchestrator Sonnet class `claude-gw-tier1b`, reviewers Sonnet / Haiku / GPT 6 Luna).",
"",
"> Zero-drop flag: the evidence validator dropped 0 of 111 citations. Per the protocol a clean pass on a report this size is an audit flag, not proof; the validator's two partial-support caveats are listed under Grounding notes.",
"",
"## Verdict",
"",
"- The plan covers the spec. No finding is blocking: 17 merged findings, 0 blocking, 2 MAJOR non-blocking (M-15, M-16), 15 MINOR.",
"- The two MAJOR items are specification gaps the plan inherits: nothing says where the per-cycle edit count for the release decision comes from, and the fold's `cycle_id` update rule is never stated.",
"- Both reviewer-raised blockers were downgraded in debate: the Wave 0 bullet test wording (plan 137-140) and the cycle-id minting overlap (plan 124, 150). All three advocates ended at MINOR after reading the lines.",
"- Debate convergence 1.00 (17 of 17 diff points agreed), invariant probe found no HIGH item.",
"",
"## Coverage (UC-1)",
"",
"- Pass 1 found 0 labelled requirement IDs; Pass 2 extracted %d quote-pinned requirement rows. `coverage_pct` is null (no parsed IDs); `coverage_pct_union` = %s; `S_dev_density` = %s; `coverage_degraded` = parsed-sparse, so Tier 1 could not stop." % (S["inferred_count"], S["coverage_pct_union"], S["S_dev_density"]),
"- Lexically unmapped rows (%d): %s. Lexical containment is weak evidence; the reviewers' semantic checks (rows observed 20, 23 and 18 of their assigned 20, 24 and 18) replace it for the findings below." % (len(S["unmapped_requirements_union"]), ", ".join(S["unmapped_requirements_union"])),
"- Tasks by lexical hits: " + ", ".join("%s %d" % kv for kv in S["task_hit_counts"].items()) + ".",
"",
"## Merged findings",
"",
"Each finding below is one line of the merged findings block (`adversarial/adversarial/merged-output.md`); all quotes were re-read inside their cited line ranges by the evidence validator.",
""]
for f in F:
    lines.append("### Finding %s [%s%s]: %s" % (f["id"], f["severity"], "" if not f["blocking"] else ", blocking", f["claim"].split(".")[0][:110]))
    lines.append("")
    lines.append("- **Category:** %s. **Rows:** %s" % (f["category"], ", ".join(f["refs"]) or "none"))
    lines.append("- **Claim:** " + f["claim"])
    for c in f["citations"]:
        q = (" \"%s\"" % c["quote"]) if c.get("quote") else ""
        lines.append("- **Evidence (%s):** `%s:%d-%d`%s" % (c["role"], c["path"].rsplit("/", 1)[1] if False else c["path"], c["line_start"], c["line_end"], q))
    lines.append("")
lines += [
"## Recommendations",
"",
"All targets are the plan file `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` unless stated.",
"",
"### Recommendation R-001: Pin the per-cycle edit count and the fold's cycle id rule",
"",
"- **File:** the plan, Tasks 3, 4 and 8 (and spec lines 107 and 190-206 if the owner agrees to amend the spec)",
"- **Change:** State where `release_decision` gets this cycle's `applied_edits` (for example, count `fix_applied` events carrying the guard's `cycle_id`), state when the fold sets or updates `cycle_id`, and name the `applied_edits` and `target_sha` that resume row 4 passes.",
"- **Verifier:** add a Task 3 test where fix-1 is released, fix-2 engages, a normal `push_completed` for fix-2 is logged, and `held_cycle_published` is true; it must fail on a fold that keeps `fix-1`. `grep -n \"cycle_id\" <plan>` shows the new criterion.",
"- **Linked findings:** M-15, M-16, M-17",
"- **Priority:** P1",
"",
"### Recommendation R-002: Carry the event, key and script contract into the protocol ref task",
"",
"- **File:** the plan, Task 8",
"- **Change:** Change the source list to spec sections 3 and 4.1 to 4.4 as spec line 240 states, and add criteria that the ref states the `draft_guard_requested` and `draft_guard_settled` payload fields, the `idempotency_key` format, the one retry of a failed release, and the engage-failure message that names `--merge-guard off` and prints the clear command.",
"- **Verifier:** the Task 8 protocol test asserts those four phrases; `uv run pytest tests/pr_submit/test_merge_guard_protocol.py -q` fails when any is removed.",
"- **Linked findings:** M-03, M-06, M-09",
"- **Priority:** P1",
"",
"### Recommendation R-003: Make the Wave 0 bullet test passable and complete",
"",
"- **File:** the plan, Task 9",
"- **Change:** Replace \"no `L3 only` or `draft` gate wording\" with an explicit list (for example: no \"only at L3\", no \"only with draft\" load condition) and add assertions for the second trigger (a run log that already holds guard events) and that the off line is printed once.",
"- **Verifier:** the Wave 0 test passes on a bullet that says \"at L3 with `--merge-guard off`\" and fails when the second trigger is missing.",
"- **Linked findings:** M-01, M-12",
"- **Priority:** P2",
"",
"### Recommendation R-004: Add the missing assertions to Tasks 3, 4, 7 and 11",
"",
"- **File:** the plan, Tasks 3, 4, 7 and 11",
"- **Change:** Assert `original_is_draft` after a first skip; assert `notes` carries `auto_merge_armed` on `ENGAGE`; name the `settled(ready, failed)` fold row and resume rows 7 and 8; test `--to ready` as a no-op on a ready PR; add a CI-fix engage case with cycle id `ci-1`; add a release-failure scenario (one retry, `release_pending`).",
"- **Verifier:** each new test fails against a stub that omits the behaviour; `uv run pytest tests/pr_submit -q` passes on the real implementation.",
"- **Linked findings:** M-04, M-05, M-06, M-07, M-08",
"- **Priority:** P2",
"",
"### Recommendation R-005: Tie the three cycle-id users to one id",
"",
"- **File:** the plan, Tasks 8 and 10",
"- **Change:** Require Task 10's Wave 3 bullet to name the single place Task 1 O1 finds, and extend the acceptance trace so the guard events, the push triad and `rereview_requested` carry the same `cycle_id`.",
"- **Verifier:** the trace test compares the `cycle_id` of the three event groups and fails when one differs.",
"- **Linked findings:** M-02",
"- **Priority:** P2",
"",
"### Recommendation R-006: Complete the dependency lines and enforce the two prose constraints",
"",
"- **File:** the plan, Tasks 8, 9, 10, 12 and 13",
"- **Change:** Add `Depends on:` lines (Task 12 on Tasks 9 and 10, Task 13 on Task 1) and add protocol-test assertions that the ref and the SKILL bullets carry no `file:NNN` pointer and the ref has no python fence.",
"- **Verifier:** `grep -n \"Depends on\" <plan>` lists the new lines; the protocol test fails on a `file:123` pointer.",
"- **Linked findings:** M-13, M-14",
"- **Priority:** P2",
"",
"### Recommendation R-007: Decide who states the release gate in the PR body and pin full sentences",
"",
"- **File:** the plan, Tasks 1, 10 and 12 (or the coordinator's PR checklist)",
"- **Change:** Name the owner of the PR-body gate statement, and store the full pinned sentences (not only their start) as constants for the byte-identical checks.",
"- **Verifier:** the Task 10 byte-identical test compares the full sentence and fails when a word later in the sentence changes.",
"- **Linked findings:** M-10, M-11",
"- **Priority:** P2",
"",
"## Reviewer ensemble and identity",
"",
"| Reviewer | Persona | Class requested | Pinned model (resolution.json) | Self-reported model | Calibrated C | Findings |",
"|---|---|---|---|---|---|---|",
"| 1 | analyzer | sonnet | claude-sonnet-5-5 | claude-gw-tier1b | 0.69 | 2 |",
"| 2 | qa | haiku | claude-haiku-5-5 | claude-haiku-5-5 | 0.55 | 12 |",
"| 3 | refactorer | opus | claude-opus-5-5 | gpt-6-luna | 0.71 | 2 |",
"",
"- The pins in `panel/resolution.json` record the class rotation, not the served model. Reviewer 3 reported `gpt-6-luna`, which is what the `ANTHROPIC_DEFAULT_OPUS_MODEL` alias of this run serves, so `identity_mismatch_suspected` is true and `identity_source` is `requested-pinned`: no verified-independence claim is made.",
"- Calibrator class: the opus class (served as `gpt-6-luna` by self-report); `calibrator_diversity: degraded` because all three reviewer classes are in use. T1 card calibration C = 0.69; mean of the three card calibrations = 0.65.",
"- Executor class unresolved (`executor_class_resolved: false`): this audit is of a plan, not of finished work.",
"- Vendor diversity: multi (Anthropic and OpenAI served classes); model-class diversity: full.",
"",
"## Debate (Wave 4)",
"",
"- Mode A, depth standard, three advocates (model inherited from the orchestrator session), Round 2 sequential, Round 2.5 invariant probe, base selection by hybrid score: variant 2 (0.7212 vs 0.6693 and 0.6648; margin 0.0519, no tiebreaker). Merge by the merge-executor agent; the 17-line findings block is byte-identical to the verified jsonl.",
"- The advocates of the two variants that carried a MAJOR/blocking finding (variants 2 and 3) conceded it in Round 1; the third advocate had already rated both MINOR. Each concession rested on plan lines all three could re-read, so the merged verdict contains no blocker that survived adversarial pressure. All three advocates ran on the orchestrator's own model, so this agreement is not an independent-vendor check.",
"- Invariant probe: 7 entries, 0 HIGH, 2 MEDIUM unaddressed (INV-001, INV-002, carried as M-15 and M-16), 3 LOW unaddressed (INV-003, INV-004, INV-006). The probe agent disclosed reading post-execution code in the working tree for import facts only.",
"- Judge: the sc-adversarial return contract names no judge, so `judge_identity` is unknown and `judge_class_collision` is unknown. The orchestrator session (claude-gw-tier1b) ran the scoring inline.",
"",
"## Grounding notes",
"",
"- Evidence validator (Sonnet class): 49 merged-finding citations and 62 inferred-requirement rows re-read; 0 unfounded. Caveat M-06: plan lines 60 and 73 already cover the release-failure fold and resume rows in blanket wording, so \"no behavioural criterion\" is broader than the evidence; the narrower reading (the retry, `release_pending` and the named rows have no specific assertion) holds. Caveat M-17: spec lines 155-156, which carry the row 7 before row 8 order, are uncited.",
"- Reviewer 2's original card had four citations whose quote was not on the cited line (spec 369, 280, 270, 268); the merge replaced them with lines 333, 234 and 232 (the F5 finding was dropped).",
"- Attribution: the feature this plan describes landed after the base commit `e8db2fe6` (commit `0b8a5801d`). Reviewer 2 saw two post-execution test file names in a grep and opened neither; the probe agent read working-tree code for import facts. No citation points into `.dev/tasks/done/`.",
"",
"## Inferred requirements (Pass 2)",
"",
"| INF id | Verbatim quote | Citation | Match result |",
"|---|---|---|---|",
]
for m in M:
    if m["source"] == "inferred":
        q = m["quote"].replace("|", "\\|")
        res = "%s (%s, ratio %s)" % (m["match_method"], ", ".join(m["matched_task_ids"]), m["ratio"]) if m["matched_task_ids"] else "none (best ratio %s)" % m["ratio"]
        lines.append("| %s | %s | `%s:%d` | %s |" % (m["requirement_id"], q, SPEC, m["spec_line"], res))
lines += [
"",
"Postscript: no inferred row was dropped by the evidence validator (62 of 62 quotes verbatim at their lines).",
"",
"## Inferred-claim audit",
"",
"- `citations_inferred: 0`",
"- Inferred-fraction: `0 / 111` = 0.00",
""]
(out / "REPORT.md").write_text("\n".join(lines) + "\n")
print("REPORT.md", len(lines), "lines")
