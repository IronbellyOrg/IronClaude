# Reflect report: stage 3c plan, pre-execution (UC-1)

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.82
citations_total: 59
citations_revalidated: 59
citations_dropped: 1
citations_inferred: 0
citation_budget_policy: full_reread   # more than 20 citations allows sampling; the validator re-read all 59
coverage_degraded: parsed-sparse
```

- **Spec:** `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-WF-stage3CRequest-20261119-143901/source.md`
- **Plan:** `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-WF-stage3CRequest-20261119-143901/TASK-WF-stage3CRequest-20261119-143901.md`
- **Short cites:** `plan:N` = the plan; `source.md:N` = the spec; `agent:N` = `src/superclaude/agents/reflect-reviewer.md`; `Makefile:N` = the repository Makefile.
- **Route:** parsed requirement ids 0, inferred 43, so the parse-density guard forced Tier 2 (`artifacts/tier_decision.yaml`). Three `reflect-reviewer` cards (analyzer on sonnet, qa on haiku, refactorer on opus), blind-calibrated 0.79, 0.81 and 0.87 (`calibration/`); Tier 1 card calibrated 0.81. `confidence_calibrated` is the mean of the four, 0.82. Merge: `/sc:adversarial` Mode A, depth standard, convergence 1.0, status partial (blocked by one HIGH invariant, INV-003, folded into finding D-001's fix). Merged card: `adversarial/merged-output.md`.
- **Degraded:** codegraph index stale (Grep/Read floor); calibrator_diversity degraded (opus calibrators, all three classes are reviewers); t2_vendor_diversity single; executor class not resolved.

## Verdict

FAIL: two Blocking findings, one Medium, one Note (a second Note, D-004, was dropped by the evidence validator; see Grounding Gaps). Both Blocking findings are text the plan must add; neither changes the code edit. The edit itself is right: the passage inserted at the named anchor reproduces the measured variant byte for byte (`.dev/stage3c-variants/brainstorm/reflect-reviewer.md`, sha256 `7696a2b2…0ed8`, source.md:24), and both test needles match.

## Deviations

### Deviation D-001: no fresh branch from origin/master (Blocking (Missing))

- **Location:** plan:17-27 (Constraints), plan:31-61 (tasks)
- **Spec:** source.md:3 ("Run it on a fresh branch made from `origin/master`.")
- **Class:** Drift. Grade: `Blocking (Missing):` affected action: the branch Task 1's edits and the later PR land on.
- **Evidence:** no `branch` or `origin/master` text in the plan; all three cards raised it.
- **Added by the merge (INV-003):** the route must be named. Switching this worktree in place leaves gitignored `.claude/` dev copies of primitives that `origin/master` deleted; `make sync-dev` never deletes and `make verify-sync` fails on a `.claude` copy with no source, so Task 2's "`make verify-sync` passes" (plan:59) would fail on a correct edit. `make sync-dev` only copies (Makefile:109-163); the verify-sync reverse checks print "MISSING in src/superclaude/..." and set drift for skills (Makefile:188-200) and agents (Makefile:218-226). Orchestrator check on 2026-11-19: 14 `.claude/skills/` entries and 13 `.claude/commands/sc/` entries in this worktree have no source on the local `origin/master` (the merged card's figure of 53 counted differently and was not reproduced).
- **Remediation:** add a constraint beside the owner-go line (plan:19): run on a fresh branch from `origin/master`, either in a new Orca worktree (carry the package, the request file and the ledger edit into it) or in place after removing stale `.claude/` copies before `make sync-dev`.

### Deviation D-002: known limits not carried, and a judgment stated as fact (Blocking (Missing); Decision also holds)

- **Location:** plan:15, plan:21, plan:22
- **Spec:** source.md:65-69 ("Known limits to carry into the plan's summary")
- **Class:** Drift. Grade: `Blocking (Missing):` affected action: the owner's go decision and the later reading of the B/E re-runs.
- **Evidence:** the plan has no summary, keeps only part of limit 1, omits the small-measurement limit and the codepoint-order judgment, and plan:21 calls both spec B findings "two real gaps" where source.md:69 calls one a judgment. One calibrator graded this Medium; the merge debate rejected that (Missing needs no consequence test, agent:119).
- **Remediation:** add the three limits from source.md:67-69 to the plan (Goal and "Why" bullets) and reword plan:21.

### Deviation D-003: measured hash dropped; greps pin only start, end and join (Medium)

- **Location:** plan:22, plan:44-46
- **Spec:** source.md:24
- **Class:** Drift. Grade: `Medium:`.
- **Evidence:** `grep -c` counts lines and the bullet is one line (agent:122), so a wrong middle token still prints 1; pytest passes whether or not the two needles were added.
- **Remediation:** add a whole-file `sha256sum` check against `7696a2b21601ff914d7651085125ef4188238640998c0599907555c760ec0ed8` and one `grep -c` per new needle in the test file.

### Deviation D-005: "83 tests" claim cites another variant's record (Note)

- **Location:** plan:39. The 83-passed record is for the carry-scope variant (`.dev/stage3c-variants/brainstorm-deep/DESIGN.md:24`, titled "Third variant: carry-scope" at line 1); no acceptance line uses 83.

## Inferred requirements (Pass 2)

Pass 1 parsed 0 ids. Pass 2 rows (`artifacts/coverage-matrix.json`); coverage_pct null (parsed-only), coverage_pct_union 0.9070, unmapped union INF-001, INF-034, INF-037, INF-038; S_dev_density 0.0930.

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | Run it on a fresh branch made from `origin/master`. | source.md:3 | unmapped (none, 0.4286) |
| INF-002 | Do NOT run `/sc:implement` on the package until the owner says go in chat. | source.md:3 | Constraints (containment, 0.9) |
| INF-003 | The stage 3b package `TASK-WF-stage3BRequest-20261117-172514` is in the done subfolder of the repository task folder, and PR #605 is merged. | source.md:20 | Constraints (containment, 1.0) |
| INF-004 | There is no owner gate inside this package. The owner's go to run it is a separate chat message recorded in the stage ledger `stage-requests/README.md`. | source.md:20 | Constraints (containment, 0.9) |
| INF-005 | Task 1: edit `src/superclaude/agents/reflect-reviewer.md`. Re-read the place by its text first. | source.md:24 | Task 1 (containment, 1.0) |
| INF-006 | One edit only: in the bullet that begins "- The Severity column of the Deviations table (HIGH, MEDIUM, LOW) is a label, not the grade.", insert the passage below directly after the sentence "A deviation that meets a blocking condition is Blocking whatever its label says; a HIGH that is only wording is a Note." and before the sentence that begins "When no consumer can be established". | source.md:24 | Task 1 (containment, 0.9697) |
| INF-007 | Keep one space between sentences. | source.md:24 | Task 1 (containment, 1.0) |
| INF-008 | Copy the passage from the fenced block below; do not retype it. It is byte-identical to the measured text (source file `.dev/stage3c-variants/brainstorm/reflect-reviewer.md`, sha256 `7696a2b21601ff914d7651085125ef4188238640998c0599907555c760ec0ed8`, in the stage 0 to 3 worktree). | source.md:24 | Constraints (containment, 0.7037) |
| INF-009 | Before you write `Medium:`, ask whether someone following the text as written could produce behaviour the spec forbids, or pass a named acceptance check while a behaviour the spec states is absent or wrong (for example a missing message prefix, or a missing "no output written" rule). If so, correcting it changes a required behaviour or acceptance check: grade it `Blocking (Decision):` or `Blocking (Missing):`, not `Medium:`. | source.md:27 | Task 1 (containment, 0.6286) |
| INF-010 | In `tests/skills/test_review_severity_rule.py`, add two needles to the tuple in `test_c_reflect_reviewer_grade_bullets_pinned`: `"Before you write `Medium:`, ask whether someone following the text as written could produce behaviour the spec forbids"` and `"A behaviour that would happen anyway (for example exit 0 on success) is not that."`. Make each needle a Python string that holds the exact text, backticks included. | source.md:30 | Task 1 (containment, 0.9333) |
| INF-011 | Do not change the frontmatter, the Behavioral Mindset, the Boundaries list, the Correctness gaps section, the columns of the Deviations table, the S1, S2 and S3 bullets, the cap bullet, or the bullet that begins "- This grading applies". | source.md:32 | Task 1 (containment, 1.0) |
| INF-012 | Before editing, run `git grep -n "reflect-reviewer" -- tests src` and write its output to `./artifacts/stage3c-task1-notes.md`, with one sentence on which tests read the agent file. | source.md:34 | Task 1 (containment, 1.0) |
| INF-013 | After the edit, run every test file that output names once and record each result in the same file. | source.md:34 | Task 1 (containment, 1.0) |
| INF-014 | `grep -c "Before you write \`Medium:\`" src/superclaude/agents/reflect-reviewer.md` prints 1. | source.md:39 | Task 1 (containment, 1.0) |
| INF-015 | `grep -c "A behaviour that would happen anyway (for example exit 0 on success) is not that." src/superclaude/agents/reflect-reviewer.md` prints 1. | source.md:40 | Task 1 (containment, 1.0) |
| INF-016 | `grep -c "a HIGH that is only wording is a Note. Before you write" src/superclaude/agents/reflect-reviewer.md` prints 1. | source.md:41 | Task 1 (containment, 1.0) |
| INF-017 | `git diff -- src/superclaude/agents/reflect-reviewer.md` shows exactly one changed line, the Severity column bullet. The removed and added versions of that line differ only by the inserted passage plus one space. | source.md:42 | Task 1 (containment, 0.96) |
| INF-018 | `uv run pytest tests/skills/test_review_severity_rule.py -v` passes with the two new needles. | source.md:43 | Task 1 (containment, 1.0) |
| INF-019 | `uv run pytest tests/cli/reflect/test_reviewer_readonly_tools.py tests/cli/reflect/test_reviewer_brief_constraints.py tests/agents/test_codegraph_rosters.py tests/skills/test_review_severity_rule.py -v` passes. | source.md:44 | Task 1 (containment, 1.0) |
| INF-020 | the `git grep` output and its one sentence; | source.md:46 | Task 1 (containment, 1.0) |
| INF-021 | the results of the other test files that output names; | source.md:47 | Task 1 (containment, 1.0) |
| INF-022 | one line saying the reflect skill (`skills/sc-reflect-protocol`) and the adversarial merge were not edited. | source.md:48 | Task 1 (containment, 1.0) |
| INF-023 | Task 2: run `make sync-dev` and `make verify-sync`, then run the four test files above once more after the last edit. | source.md:50 | Task 2 (containment, 0.9333) |
| INF-024 | Write the pass counts and the `make verify-sync` result to `./artifacts/stage3c-final-run.md`. | source.md:50 | Task 2 (containment, 1.0) |
| INF-025 | Check that nothing under the project `.claude/` folder other than `.claude/settings.json` is staged. | source.md:50 | Constraints (containment, 0.7778) |
| INF-026 | `make verify-sync` passes. | source.md:54 | Task 2 (containment, 1.0) |
| INF-027 | The four test files pass. | source.md:55 | Task 1 (containment, 1.0) |
| INF-028 | `./artifacts/stage3c-final-run.md` exists. | source.md:56 | Constraints (containment, 0.8333) |
| INF-029 | That merge step is the reflect protocol's and the adversarial skill's, outside this file. No edit to `skills/sc-reflect-protocol`, the adversarial skill, or the merge text. | source.md:60 | Constraints (containment, 0.8667) |
| INF-030 | That is a detection problem, not a grading one, and is not addressed here. | source.md:61 | Constraints (containment, 0.7143) |
| INF-031 | No edit to the S1 to S3 bullets, `evidence-validator.md`, `sc-implement-protocol/refs/qa.md`, the own-scale primitives or `src/superclaude/cli/**/*.py`. No plugin surface. | source.md:62 | Constraints (containment, 1.0) |
| INF-032 | No new question in any command. No Jev call. | source.md:62 | Constraints (containment, 1.0) |
| INF-033 | The re-runs are not a task here. | source.md:63 | Constraints (containment, 1.0) |
| INF-034 | Known limits to carry into the plan's summary | source.md:65 | unmapped (none, 0.1667) |
| INF-035 | The passage names two kinds of finding from spec E ("a missing message prefix", "a missing 'no output written' rule") as examples. It was measured with them, so they stay. | source.md:67 | Constraints (containment, 0.8) |
| INF-036 | Its held-out result on spec B does not depend on them. | source.md:67 | Constraints (containment, 0.75) |
| INF-037 | The measurement was small: one reviewer model (sonnet), three reviewers per arm, one scorer and no second reader. The briefs carried first-pass coverage hints for every arm. | source.md:68 | unmapped (none, 0.35) |
| INF-038 | Whether dropping "plain codepoint order" is a real blocker is a judgment: it changes the order of digits and apostrophes, not of lowercase letters. | source.md:69 | unmapped (none, 0.2857) |
| INF-039 | `src/superclaude/` is the source of truth: edit there, then run `make sync-dev`. | source.md:73 | Constraints (containment, 1.0) |
| INF-040 | Stage nothing under the project `.claude/` folder; only `.claude/settings.json` is tracked. | source.md:74 | Constraints (containment, 0.8889) |
| INF-041 | Python work uses UV only (`uv run pytest ...`). | source.md:75 | Constraints (containment, 1.0) |
| INF-042 | `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included. Staging is not committing. | source.md:76 | Constraints (containment, 1.0) |
| INF-043 | Acceptance checks are by content and quote the sentence they protect. Line numbers in a task body are hints; re-read each place by its text. | source.md:77 | Constraints (containment, 1.0) |

## Grounding Gaps

### Gap G-001: dropped citation, finding D-004 (Note)

- **Original claim:** "D-004 authorized narrowing (Note): plan:61, plan:37, plan:60. Narrows the spec; crosses no exclusion."
- **Why dropped:** the evidence validator re-read the ranges: plan:37 restates source.md:32, and plan:60 and plan:61 restate or tighten source.md:55 and source.md:50 rather than narrow them. The cited ranges do not support "narrows".
- **Next evidence needed:** none; the finding was a Note and is removed from the counts.
- **decision_needed_by_user:** false

INV-003 (the debate's open invariant) is folded into D-001 and is not an evidence gap.

## Recommendations

### Recommendation R-001: add the branch constraint with its route (D-001)
- **File:** plan, Constraints (beside plan:19). **Change:** one constraint line naming the fresh-branch route. **Verifier:** `grep -c "origin/master" <plan>` prints 1 or more.

### Recommendation R-002: carry the known limits and reword the "real gaps" sentence (D-002)
- **File:** plan:15, plan:21-22. **Change:** add the three limits; reword plan:21. **Verifier:** the plan contains "one model", "no second reader" and "judgment".

### Recommendation R-003: pin the whole passage and the needles (D-003, optional)
- **File:** plan:44-46. **Change:** add the sha256 check and two needle greps. **Verifier:** the plan contains the full hash.

## Inferred-claim audit

citations_inferred: 0.
