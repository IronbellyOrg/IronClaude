# Reflect report: pre-execution audit of TASK-WF-fixTheScIssueWor-20261104-162205

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.77
citations_total: 22
citations_revalidated: 22   # 21 by evidence-validator; the D-M13 git-status claim re-run by the orchestrator (validator has no Bash)
citations_dropped: 0
citations_inferred: 1
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

Spec: `.dev/tasks/to-do/TASK-WF-fixTheScIssueWor-20261104-162205/source.md`
Tasklist: `.dev/tasks/to-do/TASK-WF-fixTheScIssueWor-20261104-162205/TASK-WF-fixTheScIssueWor-20261104-162205.md`
Status is `partial` because the adversarial merge left one split point (X-001) and its merged verdict is FAIL with one blocking finding (M-13). The verdict is advisory: /sc:workflow never edits the plan from it.

## Coverage

All 5 requirements in the spec (`source.md:1`, all inferred, no labeled IDs) map to tasks: coverage_pct_union 1.00, unmapped_requirements_union []. `coverage_degraded: parsed-sparse` forced Tier 2. Matrix: `artifacts/coverage-matrix.md`.

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | "add to each issue-worker-t*.md Rules section a rule that the files they write under .dev/issues/ are input files for the orchestrator's next tool calls (gh --body-file posts, /sc:recommend), not report files" | source.md:1 | Task 2 |
| INF-002 | "so the general harness note against writing report .md files does not apply to them" | source.md:1 | Task 2 |
| INF-003 | "and returning the content as text instead is a failure (E-WORKER-NO-OUTPUT)." | source.md:1 | Task 2 |
| INF-004 | "Add a regression test in tests/skills/test_issue_worker_agents.py that every issue-worker agent file carries that rule." | source.md:1 | Task 1 |
| INF-005 | "Files: src/superclaude/agents/issue-worker-t1.md, issue-worker-t2.md, issue-worker-t3.md, tests/skills/test_issue_worker_agents.py" | source.md:1 | Tasks 1, 2 |

## Deviations (merged verdict, `adversarial/merged-verdict.yaml`)

### Deviation D-M13 (blocking): git-diff acceptance checks are vacuous on untracked files

- **Location:** TASK-WF-fixTheScIssueWor-20261104-162205.md:53,65,75
- **Mapped tasklist item:** Tasks 1, 2, 3
- **Spec section:** n/a
- **Evidence:** `git status --short` prints `??` for src/superclaude/agents/issue-worker-t1.md, issue-worker-t2.md, issue-worker-t3.md, src/superclaude/skills/sc-issue-protocol/SKILL.md and tests/skills/test_issue_worker_agents.py (run 2026-11-04T17:08Z). `git diff` prints nothing for untracked files.
- **Classification:** grounding_gap (blocking)
- **Classification rationale:** three acceptance checks ("git diff on each file shows only those additions", "SKILL.md gains exactly that one line ... and no other change", "no existing test is changed") would pass on empty output.
- **Default remediation:** copy the five files to `./artifacts/pre/` before the first edit and prove each change with `git diff --no-index ./artifacts/pre/<f> <f>`, saved under `./artifacts/`.

### Minor findings

- D-M01 (grounding_gap): early-section placement is the plan author's inference from the retry evidence; the coordinator message is not stored in the package (plan:19).
- D-M02 (drift): Task 3 edits SKILL.md, outside the spec's Files list (source.md:1); plan:20 discloses it as the author's judgement.
- D-M03 (drift): the Rules bullet (plan:29) omits `E-WORKER-NO-OUTPUT` and the harness-note clause that source.md:1 puts in the Rules-section rule.
- D-M06 (grounding_gap): exact texts use nested backticks (plan:24-32); boundaries ambiguous.
- D-M07 (grounding_gap): `make verify-sync` can fail for unrelated files; no instruction (plan:77).
- D-M09 (drift): "the reports under `analysis/`" repeats the harness note's trigger words (plan:26); t1:17 and t2:17 say "save its report under `<D>/analysis/`".
- D-M11 (drift): "names each exact path" cannot hold for `analysis/` (refs/claim.md:58).
- D-M12 (drift): the helper does not check the Rules bullet's position after the "Writing only under" bullet (plan:27).
- D-M14 (grounding_gap): the tests prove text only; a live re-claim of #365 is the runtime proof (out of this plan's scope).
- D-M15 (grounding_gap): refs/claim.md and refs/create.md spawn steps stay unchanged (create.md:20).

## Inferred-claim audit

- `citations_inferred: 1`
- Inferred-fraction: 1 / 22 = 0.05
- Evidence-validator: 22 checked, 0 dropped (zero-drop-flag: true; it actively checked shifted line numbers, quote drift and wrong-file citations). Note: the R-003 verifier passes today because the phrase exists only in the plan; it guards the post-edit state.
- [INFERRED] The agent body is expected to outrank the injected harness line once the files are named explicitly; no test can show this, only a live run.

## Recommendations

### Recommendation R-001: Snapshot the five target files before editing (P0, D-M13)

- **File:** ./artifacts/pre/ in the plan package
- **Change:** copy the five untracked target files there before Task 1 and prove each task's "only these additions" criterion with `git diff --no-index`.
- **Verifier:** saved `git diff --no-index` outputs show only the planned added lines.
- **Linked deviation(s):** D-M13
- **Priority:** P0

### Recommendation R-002: Make the Rules bullet stand alone (P1, D-M03)

- **File:** src/superclaude/agents/issue-worker-t1.md, issue-worker-t2.md, issue-worker-t3.md
- **Change:** add the harness-note clause and `(E-WORKER-NO-OUTPUT)` to the Rules bullet.
- **Verifier:** the Task 1 helper's Rules-bullet constant contains `E-WORKER-NO-OUTPUT`.
- **Linked deviation(s):** D-M03
- **Priority:** P1

### Recommendation R-003: Replace "the reports under `analysis/`" with "the files under `analysis/`" (P1, D-M09)

- **File:** the plan's Constraints early-section text
- **Change:** drop the trigger word "reports" from the paragraph meant to defeat it.
- **Verifier:** `grep -c "reports under" src/superclaude/agents/issue-worker-t*.md` is 0.
- **Linked deviation(s):** D-M09
- **Priority:** P1
