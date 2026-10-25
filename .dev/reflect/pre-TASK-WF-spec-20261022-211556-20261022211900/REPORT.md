# Reflect report: pre-execution review of TASK-WF-spec-20261022-211556

```yaml
contract_version: 1.8.0
status: success
mode: pre
tier_reached: 2
confidence_calibrated: 0.84
citations_total: 38
citations_revalidated: 38
citations_dropped: 0
citations_inferred: 1
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

Paths are relative to the worktree root `/config/workspace/IronClaude/.dev/worktrees/ci-followup/`. `tasklist` = `.dev/tasks/to-do/TASK-WF-spec-20261022-211556/TASK-WF-spec-20261022-211556.md`; `source` = `.dev/tasks/to-do/TASK-WF-spec-20261022-211556/source.md`.

## Verdict

**Not ready.** The plan's scope, phase order and coverage of Fix 1 to Fix 4 are sound: no reviewer, advocate or the invariant probe found a high-severity defect or a missing fix. But the spec makes "every acceptance bullet must fail on a wrong edit" a rule (source:38), and acceptance bullets in Tasks 5, 6 and 8 pass a wrong edit, while bullets in Tasks 2, 6 and 9 can fail a correct run. These are text edits to the tasklist, not design changes.

- Tier 2: two read-only reviewers (sonnet analyzer; grok-4.7 on the haiku slot, qa), blind calibration by opus (C 0.86 and 0.82; Tier-1 card 0.75), adversarial merge (Mode A, standard depth): convergence 1.0, 17 of 17 points; invariant probe 19 findings, 0 high, 6 medium.
- Coverage: no labeled requirement IDs in the spec, so all 45 requirement rows were inferred with verbatim quotes (`coverage_degraded: parsed-sparse`); 38 of 45 matched (0.8444); the 7 unmatched rows are 4 wording misses, 2 plan-wide rules, and 1 real gap (INF-045, the path-filter question).
- Merged findings: 10 medium, 8 low, 0 high (adversarial/merged-verdict.yaml).

## Inferred requirements (Pass 2)

45 rows, all quote-verified against their cited source line by script (artifacts/coverage-matrix.yaml, `quote_mismatches: []`). Unmatched rows and their resolved verdicts:

| INF id | Quote (abridged) | Citation | Match result |
|---|---|---|---|
| INF-001 | "the sync job stops pushing unreviewed upstream content to master" | source:3 | covered (Task 6) |
| INF-003 | "Evidence files go under ./artifacts/ in the plan package." | source:7 | covered (Constraints) |
| INF-037 | "Every acceptance bullet must fail on a wrong edit" | source:38 | partial (see D-001, D-002, D-003) |
| INF-040 | "also require positive greps showing the expected edits happened" | source:39 | covered (Task 9) |
| INF-041 | "`Depends on:` lines name one task each; make real chains where order matters." | source:40 | partial (D-014) |
| INF-042 | "No numbered or checkbox lines in the tasklist." | source:40 | covered |
| INF-045 | "Do not add a task; raise it to me as a question after verifying against current GitHub docs." | source:47 | gap (D-011) |

## Deviations (plan defects)

### Deviation D-001: Task 5 warning and header checks pass a wrong reword (medium)
- **Location:** tasklist:88, tasklist:90
- **Spec section:** Fix 2; Quality rules (source:38)
- **Evidence:** the header check only forbids `gates` in lines 19-20 (tasklist:88); the warning check only forbids the exact old sentence (tasklist:90). Deleting the sentence, or writing "mandatory before merge", passes.
- **Classification:** drift (acceptance does not enforce the spec rule)
- **Default remediation:** require advisory wording on the `::warning` line and forbid "before merge"; check the header comment as a text-anchored block that must not contain "requiring this check" or "gates".
- **Sources:** R1-1, X-001

### Deviation D-002: Task 6 never compares the unchanged part of the sync step (medium)
- **Location:** tasklist:112, tasklist:113
- **Spec section:** Fix 1 (source:13: protected-file check and state-file handling stay unchanged)
- **Evidence:** only steps other than `Commit and Push Changes` are compared (tasklist:112); the step's own unchanged lines, including `git add -f docs/.framework-sync-commit` (.github/workflows/pull-sync-framework.yml:103-105), its `if` and `working-directory`, and `--base master --head sync/framework` are never asserted.
- **Default remediation:** assert the base run-body lines up to the `git commit` line are unchanged, compare the step's `if`/`working-directory`/`name`, and assert `--base master` and `--head sync/framework` on the `gh pr create` line.
- **Sources:** R1-5

### Deviation D-003: Task 8 README checks pass a wrong README (medium)
- **Location:** tasklist:141, tasklist:143
- **Spec section:** Fix 4 (source:34)
- **Evidence:** the badge check needs `IronbellyOrg/IronClaude` twice but never `actions/workflows/test.yml` (tasklist:141); the paragraph checks need only the words `advisory`, `sync/framework`, `pull request` (tasklist:143).
- **Default remediation:** require `actions/workflows/test.yml` in both badge URLs; require the boundary entry to say the job cannot block a merge and the sync entry to say it does not push to master.
- **Sources:** R2-4

### Deviation D-004: Task 6 stub run is unworkable as written (medium)
- **Location:** tasklist:114
- **Evidence:** "`git` push and `gh` replaced by PATH stubs" (tasklist:114), but the step also runs `git config`, `git add`, `git diff --cached`, `git commit` (.github/workflows/pull-sync-framework.yml:89-108). Run 2 (`gh pr list` returns 1) never reaches `gh` unless a fresh change is staged after run 1's commit, so a wrong edit that always creates a pull request still passes.
- **Default remediation:** the git stub logs and delegates every subcommand except `push` to real git; stage a fresh change before run 2 and assert `gh pr list` was called; export GITHUB_REPOSITORY; run with `bash -e` (the Actions default has no pipefail).
- **Sources:** R1-4, R2-2, INV-003, INV-007

### Deviation D-005: a failed `gh pr list` can end green with no pull request (medium)
- **Location:** tasklist:105, tasklist:114
- **Evidence:** the instruction only says create when the count is 0, otherwise echo "reused" (tasklist:105); no stub run covers a failing `gh`. A command substitution that fails yields an empty string and takes the "reused" branch.
- **Default remediation:** require the count to be captured and checked so a `gh` failure fails the step; add a stub run where `gh pr list` exits non-zero and assert the step fails.
- **Sources:** INV-004

### Deviation D-006: Tasks 6 and 7 do not prove "nothing else changed" (medium)
- **Location:** tasklist:112, tasklist:124, tasklist:125
- **Evidence:** only named steps are compared; the `on:` block (cron), job keys and step count of pull-sync-framework.yml and test.yml are never compared, so an inserted extra step or a changed schedule passes.
- **Default remediation:** compare the whole parsed document except the one changed step (or the one changed `with` mapping).
- **Sources:** INV-014

### Deviation D-007: Task 2's "file ends with Decision:" conflicts with Task 7 appending to the same file (medium)
- **Location:** tasklist:49, tasklist:121
- **Evidence:** Task 2 requires the file to end with `Decision:` (tasklist:49); Task 7 appends a line to that file (tasklist:121), so Task 2's check fails on a later re-run.
- **Default remediation:** have Task 7 write its note to a separate artifact, or change Task 2's check to "contains exactly one line beginning `Decision:`".
- **Sources:** INV-001

### Deviation D-008: Task 9's scope check can fail a correct run (medium)
- **Location:** tasklist:158
- **Evidence:** any new path outside .github/workflows/, scripts/README.md and the package fails (tasklist:158). `.dev/reflect/` is untracked and not ignored (artifacts/shared-assumption-checks.md), and the `/sc:implement` final review or retry ladder can write under `.dev/` after the Task 1 baseline. Porcelain parsing of renamed or deleted paths is not specified.
- **Default remediation:** exclude the executor's own output roots (`.dev/reflect/`, `.dev/troubleshoot/`, `.dev/workflow/`) from the comparison explicitly, and parse `git status --porcelain -uall -z`.
- **Sources:** R1-12 (trimmed: .venv and uv.lock are gitignored, .gitignore:56, .gitignore:215), INV-013

### Deviation D-009: the post-merge run record is not durable (medium)
- **Location:** tasklist:108
- **Evidence:** the user is told to append the `workflow_dispatch` result to ./artifacts/t6-fix1-notes.md (tasklist:108); the package is untracked inside a worktree under `.dev/worktrees/` (.gitignore:235) and is lost when the worktree is removed.
- **Default remediation:** record the run result somewhere durable (the pull request body or a committed note), and say so in Task 6.
- **Sources:** INV-002

### Deviation D-010: Task 5 line-number anchors and the broken backslash check (low)
- **Location:** tasklist:88, tasklist:94
- **Evidence:** `sed -n '19,20p'` breaks if the reword changes the line count (tasklist:88); the backslash-backtick grep sits in a broken inline code span (tasklist:94).
- **Default remediation:** anchor checks on text blocks; write the grep as a fenced command.
- **Sources:** R1-2, R2-6, R1-3, R2-1

### Deviation D-011: the 300 vs 3,000 path-filter question has no home (low)
- **Location:** source:47
- **Evidence:** the spec asks to verify and raise it as a question, without a task (source:47); no task or artifact mentions it.
- **Default remediation:** none needed in the tasklist: the workflow session verified it against current GitHub docs and raises it to the user directly.
- **Sources:** R1-8, R2-8

### Deviation D-012: scripts/README.md stays internally inconsistent (low, accepted by spec)
- **Location:** tasklist:150, scripts/README.md:3
- **Evidence:** only the paragraph at lines 7-12 is replaced (tasklist:150); line 3 still says publishing "is handled by the GitHub Actions workflow described below" (scripts/README.md:3). The leftover list misses line 5 heading, line 34 and lines 64-66.
- **Default remediation:** keep the scope (source:35 and source:44 decided it); add the missed lines to the leftover list and tell Task 9 to read the neighbouring lines first.
- **Sources:** R1-9, INV-016

### Deviation D-013: placeholders and setup gaps (low)
- **Evidence:** `<decided file input>` (tasklist:124) and `<t1-head>` are never defined for the executor; Task 4 does not say `git init -b master` or set a commit identity (tasklist:67); the Task 5 render SHAs are not pinned to an ancestor pair (tasklist:84).
- **Default remediation:** define both placeholders in Constraints; add `git init -b master` and a local identity; pin HEAD_SHA to a commit touching merge.py and BASE_SHA to its parent.
- **Sources:** R1-10, R2-7, R1-6, R1-7

### Deviation D-014: Depends on lines misstate real order (low)
- **Location:** tasklist:119
- **Evidence:** Task 7 depends on Task 6 (tasklist:119) but needs Task 2's Decision line; the linear chain is safe but over-links Tasks 3 and 4.
- **Default remediation:** Task 7 -> Task 2; Task 3 and Task 4 -> Task 1.
- **Sources:** R1-11, R2-5

## Rejected findings
- Ask the user before Task 9 whether neighbouring README lines may be edited (R2-3): rejected; the spec already decided (source:35, source:44).
- Coverage-matrix corrections (R2-9, R2-10): reflect-artifact bookkeeping, no tasklist change.

## Shared assumptions checked
- `gh` is authenticated and `can_approve_pull_request_reviews` is `true` (artifacts/shared-assumption-checks.md).
- PyYAML is a declared dependency (pyproject.toml:38).
- [INFERRED] tests/swarm/test_merge_boundary_guards.py passes on base a88f100b: not run during this read-only review; the executor's Task 5 will show it.

## Inferred-claim audit
- `citations_inferred: 1`
- Inferred-fraction: 1 / 38 = 0.03

## Recommendations

### Recommendation R-001: Tighten the Task 5, 6 and 8 acceptance bullets
- **File:** .dev/tasks/to-do/TASK-WF-spec-20261022-211556/TASK-WF-spec-20261022-211556.md
- **Change:** apply the remediations of D-001 to D-006.
- **Verifier:** re-run `/sc:reflect --mode pre` on the regenerated plan; no medium finding on Tasks 5, 6 or 8 remains.
- **Linked deviation(s):** D-001, D-002, D-003, D-004, D-005, D-006
- **Priority:** P0

### Recommendation R-002: Fix the checks that fail a correct run
- **File:** same tasklist
- **Change:** apply D-007, D-008, D-009.
- **Verifier:** re-run reflect; Task 2's Decision check, Task 9's scope check and the Task 6 run-record location no longer conflict.
- **Linked deviation(s):** D-007, D-008, D-009
- **Priority:** P1

### Recommendation R-003: Clean up anchors, placeholders and dependency lines
- **File:** same tasklist
- **Change:** apply D-010, D-012, D-013, D-014.
- **Verifier:** grep the regenerated tasklist: no `<t1-head>` or `<decided file input>` without a definition; no `sed -n '19,20p'`; Task 7 depends on Task 2.
- **Linked deviation(s):** D-010, D-012, D-013, D-014
- **Priority:** P2
