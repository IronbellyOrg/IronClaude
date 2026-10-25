# Reflect report: pre-execution review of TASK-WF-specR1-20261023-031725 (refactor cycle 1)

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.80
citations_total: 41
citations_revalidated: 41
citations_dropped: 2
citations_inferred: 0
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

Paths are relative to `/config/workspace/IronClaude/.dev/worktrees/ci-followup/`. `tasklist` = `.dev/tasks/to-do/TASK-WF-specR1-20261023-031725/TASK-WF-specR1-20261023-031725.md`; `source` = `.dev/tasks/to-do/TASK-WF-specR1-20261023-031725/source.md`.

## Verdict

**Not ready, but much closer.** The regenerated plan fixes 16 of the 18 cycle-0 findings in full and the other 2 in part. No reviewer, advocate or the invariant probe found a high-severity defect. Five medium items remain: two acceptance checks that give the wrong answer (D-001 fails a correct run, D-002 passes a wrong edit), a dependency-chain miss against source:82 (D-003), a missing safety guard on the local stub runs (D-004), and a header-comment check that passes a half-edit (D-005).

- Tier 2: reviewers sonnet (analyzer, C 0.84) and grok-4.7 on the haiku slot (qa, C 0.76); Tier-1 card C 0.67; adversarial merge Mode A, standard depth: convergence 1.0 (13/13); invariant probe 14 findings, 0 high, 6 medium.
- Coverage: 69 inferred requirement rows (quote-verified), 59 matched (0.8551); every unmatched row was judged covered or partial by the reviewers.
- Merged findings: 5 medium, 11 low, 0 high (adversarial/merged-verdict.yaml).

## Inferred requirements (Pass 2)

69 rows in artifacts/coverage-matrix.yaml (`quote_mismatches: []`). Unmatched rows and resolved verdicts:

| INF id | Quote (abridged) | Citation | Match result |
|---|---|---|---|
| INF-001 | "the sync job stops pushing unreviewed upstream content to master" | source:3 | covered (Task 6) |
| INF-003 | "Evidence files go under ./artifacts/ in the plan package." | source:7 | covered (Constraints) |
| INF-023 | "no backslash may appear before a backtick" | source:24 | covered (Task 5 fenced grep) |
| INF-037 | "Every acceptance bullet must fail on a wrong edit" | source:38 | partial (D-001, D-002, D-005) |
| INF-040 | "also require positive greps showing the expected edits happened" | source:39 | covered (Task 9) |
| INF-042 | "No numbered or checkbox lines in the tasklist." | source:40 | covered |
| INF-045 | "Do not add a task; raise it to me as a question" | source:47 | covered (Task 3 quote, Task 9 item) |
| INF-050 | "compare the whole parsed document with the base except the planned changes" | source:57 | covered (Tasks 6, 7) |
| INF-057 | "Task 7 writes its UNVERIFIED note to its own artifact" | source:69 | partial (D-007) |
| INF-062 | "Write the backslash-before-backtick check as a fenced command" | source:76 | covered |

## Deviations (plan defects)

### Deviation D-001: Task 9's hash comparison can fail a correct run (medium)
- **Location:** tasklist:37, tasklist:183, tasklist:25
- **Evidence:** Task 1 hashes every baseline-listed path outside the allowed folders (tasklist:37); `cmp` of the before and after hash files must exit 0 (tasklist:183); the tooling-output exemption covers only new status entries (tasklist:25). The baseline already lists dozens of untracked `.dev/reflect/` files, so any rewrite of one of them fails a correct run.
- **Default remediation:** Task 1 skips `.dev/reflect/`, `.dev/troubleshoot/` and `.dev/workflow/` when writing the hash file and lists them in a separate file; widen the Constraints deviation to cover pre-existing tooling files.
- **Sources:** R1-1, INV-008

### Deviation D-002: nothing checks the `gh pr list` filters or the push-list-create order (medium)
- **Location:** tasklist:117, tasklist:128, tasklist:129
- **Evidence:** `--base` and `--head` are asserted only on `gh pr create` (tasklist:128); the gh stub prints a scripted count whatever arguments it gets (tasklist:129), so dropping `--head sync/framework` from the list call passes every run; the stub assertions count calls but not their order.
- **Default remediation:** require `--head sync/framework`, `--base master` and `--repo "$GITHUB_REPOSITORY"` on the `gh pr list` line; assert the stub log of runs (a) and (b) shows those arguments and the order push, then list, then create.
- **Sources:** R1-2, INV-004

### Deviation D-003: the Depends chain does not make the edit tasks ancestors of Tasks 8 and 9 (medium)
- **Location:** tasklist:138, tasklist:153, tasklist:172, tasklist:31; source:82
- **Evidence:** Task 7 depends on Task 2 (tasklist:138), Task 8 on Task 7 (tasklist:153), Task 9 on Task 8 (tasklist:172); Tasks 3-6 are not ancestors, which source:82 asks for. Runtime order is safe (`/sc:implement` runs in source order, ~/.claude/skills/sc-implement-protocol/SKILL.md:97), so this is a structural miss, not a runtime hazard.
- **Default remediation:** renumber so the Codecov research task sits just before the Codecov edit and chain each task on the one before it; rename artifacts and cross-references to the new numbers consistently (or keep the old artifact names and say so); move the Codecov research file's hash point to the end of the research task; record in Constraints that one-parent Depends lines cannot also keep the GitHub-settings task and the throwaway proof directly on the baseline task (source:82).
- **Sources:** R2-1, INV-001, INV-002, INV-003

### Deviation D-004: the Task 6 stub runs have no guard against touching the real repository (medium)
- **Location:** tasklist:129, tasklist:75 (validator correction; the original citation tasklist:69 was dropped)
- **Evidence:** the stub passes `config`, `add` and `commit` to the real git (tasklist:129), and the step body writes `git config user.name` (.github/workflows/pull-sync-framework.yml:89-90); Task 4 proves its temp directory is outside the repository but Task 6 does not. Run in the wrong directory, it would write the bot identity into the shared repository config and commit on the feature branch.
- **Default remediation:** Task 6 must prove `pwd` is outside the repository and that `git config --get user.name` in the worktree is unchanged after the runs.
- **Sources:** INV-005

### Deviation D-005: the header-comment check passes a half-edit (medium)
- **Location:** tasklist:82, tasklist:94, tasklist:97
- **Evidence:** the header instruction asks to say the job "cannot block a merge" (tasklist:82) but the check only bans `gates` and `requiring this check` and requires `advisory` (tasklist:94); "until a human acknowledges" can survive. Summary item 3 only bans `branch protection must require` (tasklist:97), so "should require" passes.
- **Default remediation:** require `cannot block` in the header block and forbid `until a human acknowledges`; forbid `must require` and `should require` in summary item 3.
- **Sources:** INV-006

### Low findings (D-006 to D-016)
- D-006: `-z` renames are emitted new path then old path; record both, old as MISSING (tasklist:37). Sources R1-6, R2-3.
- D-007: Task 7's "do not edit Task 2's file" is checked only by the Decision count (tasklist:140, tasklist:147); hash-compare the file. Sources R2-5.
- D-008: the job-name check forbids the bare word `required` (tasklist:95); forbid `human review required` instead. Source R2-4.
- D-009: the Decision line needs a fixed format such as `Decision: file-input=files; token=secrets.CODECOV_TOKEN`. Sources R1-5.
- D-010: say "zero `<` characters" and forbid a heredoc PR body (tasklist:128). Sources R1-10, R2-6.
- D-011 (optional): whole-document comparison for boundary-guard.yml. Source R1-3.
- D-012 (optional): Task 9 accepts any path under .github/workflows/ (tasklist:184); source:39 states directory-level scope. Sources R1-4, R2-2.
- D-013: the `::warning` instruction should name the word `advisory` (tasklist:96 already checks it; validator correction, original citation tasklist:94 dropped). Sources R1-7, R2-7.
- D-014: renders must list the five guarded paths, not "(diff unavailable)" (tasklist:100). Source INV-007.
- D-015: Task 9's positive status check should use the same flags as Task 1. Source INV-009.
- D-016: leftover line numbers are base-file numbers; say so. Source INV-010.

## Rejected findings
- R1-8 and R1-9: the plan follows source:80 and source:81; both advocates withdrew them.
- R2-8: reflect coverage-matrix bookkeeping, no tasklist change.

## Shared assumptions checked
- `/sc:implement` runs tasks sequentially in source order unless marked independent (~/.claude/skills/sc-implement-protocol/SKILL.md:97).
- The sync step calls `git` only by bare name, so a PATH stub intercepts it (artifacts/shared-assumption-checks.md).

## Inferred-claim audit
- `citations_inferred: 0`
- Inferred-fraction: 0 / 41 = 0.00

## Recommendations

### Recommendation R-001: Fix the two wrong-answer checks and the stub guard
- **File:** .dev/tasks/to-do/TASK-WF-specR1-20261023-031725/TASK-WF-specR1-20261023-031725.md
- **Change:** apply D-001, D-002, D-004, D-005.
- **Verifier:** re-run `/sc:reflect --mode pre` on the regenerated plan; no medium finding on Tasks 1, 5, 6 or 9 remains.
- **Linked deviation(s):** D-001, D-002, D-004, D-005
- **Priority:** P0

### Recommendation R-002: Renumber and re-chain
- **File:** same tasklist
- **Change:** apply D-003 with consistent artifact names and the recorded source:82 deviation.
- **Verifier:** every Depends on names the preceding task; `grep -c '^Depends on:'` equals 8; artifact names match task numbers.
- **Linked deviation(s):** D-003
- **Priority:** P1

### Recommendation R-003: Apply the low findings
- **File:** same tasklist
- **Change:** apply D-006 to D-016 (D-011 and D-012 optional).
- **Verifier:** reflect re-run reports no low finding from this list.
- **Linked deviation(s):** D-006 to D-016
- **Priority:** P2

## Grounding Gaps (dropped citations)

### Gap G-001
- **Hunk ref:** tasklist:69 (cited for D-004)
- **Evidence missing:** line 69 is Task 4's `Depends on: Task 1`; the outside-repository proof is Task 4's second acceptance bullet.
- **Why not classifiable:** the cited line does not support the claim.
- **Next evidence needed:** none; the validator located the supporting line at tasklist:75, now cited instead.

### Gap G-002
- **Hunk ref:** tasklist:94 (cited for D-013)
- **Evidence missing:** line 94 is the header-block check, not the `::warning` check.
- **Why not classifiable:** the cited line does not support the claim.
- **Next evidence needed:** none; the validator located the supporting line at tasklist:96, now cited instead.
