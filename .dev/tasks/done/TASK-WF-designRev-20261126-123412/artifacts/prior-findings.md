# Reflect report: pre-execution review of the regenerated issue-290 plan

```yaml
contract_version: 1.9.0
status: partial                      # citations_dropped > 0 (2 partial and 1 unsupported citation, corrected below)
mode: pre
tier_reached: 2
confidence_calibrated: 0.77          # mean of the blind calibrations: Tier 1 card 0.62, reviewer cards 0.81 and 0.88
citations_total: 100
citations_revalidated: 47
citations_dropped: 3                 # sample-count; partial and unsupported citations counted as dropped, claims corrected in this report
citations_dropped_extrapolated: 6
citations_inferred: 0
citation_budget_policy: sampled
coverage_degraded: parsed-sparse
coverage_pct: null
coverage_pct_union: 0.8148
S_dev_density: 0.1852
finding_counts: {blocking: 3, label_high: 0, medium: 2, note: 8}
```

> **Citation budget: sampled mode**
> - `citations_revalidated: 47` of 100 (all 24 citations in the blocking findings, plus 23 of the other 76 by a fixed hash rule).
> - `citations_dropped: 3`: the validator found 2 partial citations (both on the B2 claim sentence) and 1 unsupported citation (N5's `source.md:130`); each is corrected in the text below.
> - `citations_dropped_extrapolated: 6`: round(3 x 100 / 47). Recording only.
> The extrapolated value is telemetry, not a verdict.

Package reviewed: `.dev/tasks/to-do/TASK-WF-designRev-20261126-045943/` (tasklist `TASK-WF-designRev-20261126-045943.md`, source `source.md`). This is the regenerated plan that replaced `TASK-WF-design-20261126-041053` after the first review. Output folder: `.dev/reflect/pre-designRevPlan-20261126115300/`.

## Summary

Verdict: **FAIL**, with two edits to Task 8's operator steps and one clause in Task 7 to fix; no redesign. The first review's seven blocking defects (its B1 to B7) are fixed. Tier 2 ran because the design has no labeled requirement ids (parse-density guard) and the Tier 1 card calibrated at 0.62 (below 0.85); two reviewers (qa and refactorer lenses, executor class excluded) were blind-calibrated (0.81 and 0.88) and merged through the adversarial pipeline (convergence 1.0, 13 of 13 diff points resolved; two HIGH invariants resolved by revised text, so the adversarial status is partial).

| Gate | Result |
|---|---|
| Tier | 2 (rule 6, calibrated confidence 0.62 below 0.85; parse-density guard `parsed-sparse`) |
| Reviewers | 2 (haiku class qa lens, opus class refactorer lens); calibrator sonnet class (equals the executor class, so the three-way partition is not fully disjoint) |
| Merge method | adversarial, base variant 2 (score 0.918 against 0.730), convergence 1.0 |
| Evidence validator | ran; 47 sampled; 44 supported, 2 partial, 1 unsupported |
| Blocking findings | 3 (B1 to B3); medium 2; notes 8 |
| Promotion (Wave 7) | not applicable: pre-execution mode |

## Inferred requirements (Pass 2)

Parsed ids: 0. Inferred rows: 54, each quote-pinned to a `source.md` line (all 54 re-checked against the cited lines by script: 0 dropped). Matching is deterministic word containment (>= 0.6 of content words in one task). Union coverage 0.8148 (44 of 54); unmapped: INF-001, INF-003, INF-005, INF-017, INF-027, INF-035, INF-036, INF-038, INF-041, INF-052. The unmapped rows are lexical misses (a design heading or guard line whose words are spread over several tasks); the merged card below names the real gaps.

| INF id | Verbatim quote | Citation | Match |
|---|---|---|---|
| INF-001 | The guide must be ASCII except one "Ruling:" line / tests/core/test_how_we_work_routing_table.py:329-334 / Draft text below is plain ASCII (straight quotes, hyphens) | source.md:16 | none (best T1 0.47) |
| INF-002 | The plugin copy must equal the guide byte for byte / tests/commands/test_routing_plugin_parity.py, tests/skills/test_review_prompt_overrides.py:134-135 / Copy after every guide edit | source.md:17 | T1 (0.87) |
| INF-003 | No sentence may match find ... at least one/N/digit or the removed phrases / tests/skills/test_review_prompt_overrides.py:140-185, 217-226 (scans every .md under src and plugins) / Draft text avoids the word "find" near "at least" | source.md:18 | none (best T1 0.44) |
| INF-004 | Deck commands and flags inside <code> or SVG text must exist in the guide; --plugin is read from src/superclaude/commands/recommend.md / tests/docs/test_onboarding_deck.py:14-23, 69-87 / New card may use /sc:help, /sc:recommend, --plugin inside <code> | source.md:19 | T7 (0.68) |
| INF-005 | The deck test checks only that the footer pattern exists, not its value / tests/docs/test_onboarding_deck.py:90-91 / The footer needs its own check (section 4 below) | source.md:20 | none (best T8 0.59) |
| INF-006 | The PR template line "Branch rebased onto origin/integration" is read by a test / tests/core/test_default_branch_agreement.py:20 / Additions only | source.md:21 | T6 (0.80) |
| INF-007 | Section numbers are cited by the deck and tests (## 4. ends at ## 5.) / tests/core/test_how_we_work_routing_table.py:322-326, 897 / No new heading in the guide | source.md:22 | T1 (0.60) |
| INF-008 | New form field ids: letters, digits, -, _; | source.md:23 | T4 (0.83) |
| INF-009 | A YAML plain scalar containing : breaks parsing / YAML / Quote every new description that contains a colon | source.md:24 | T4 (0.64) |
| INF-010 | Never stage .claude/ or .dev/issues/; .dev/tasks/ is always staged / Project CLAUDE.md, story step 9 / Stage source files and .dev/tasks only | source.md:25 | T8 (0.71) |
| INF-011 | New member on the GitHub web / Forms, PR template, CONTRIBUTING.md / Form fields and the CONTRIBUTING.md line carry the rule | source.md:46 | T8 (0.71) |
| INF-012 | Agent or CLI filing (/sc:issue --create, gh issue create) / No web form / Section 4 states what every proposal issue contains, "however filed" | source.md:47 | T1 (0.62) |
| INF-013 | Agent opening a PR (/sc:pr-submit, passes --body) / No PR template / The PR-template section does not gate anything; say so in the PR body | source.md:48 | T8 (0.75) |
| INF-014 | Reader following /sc:recommend / Only the three marker blocks of the guide, never section 4 / Accepted risk, owner follow-up 1 (a routing row) | source.md:49 | T8 (0.71) |
| INF-015 | Reader entering contributing-code.md by a deep link / May skip the top / Reminder under four headings | source.md:50 | T2 (0.67) |
| INF-016 | File: src/superclaude/core/HOW-WE-WORK.md. | source.md:57 | T1 (1.00) |
| INF-017 | Guards: FR-001 to FR-004 checks of the merged spec (words present; | source.md:67 | none (best T8 0.33) |
| INF-018 | File: docs/developer-guide/contributing-code.md. | source.md:70 | T2 (1.00) |
| INF-019 | Before ## Table of Contents (line 7): | source.md:71 | T2 (1.00) |
| INF-020 | A one-line reminder directly under ## Context File Guidelines (line 99), ## Development Workflow (160), ## Contributing to Components (237) and ### Issue Reporting (377): > Maintainer reference. | source.md:75 | T2 (0.79) |
| INF-021 | Directly under ### Pull Request Template (line 203), above the embedded example: > The template GitHub shows on new pull requests is .github/PULL_REQUEST_TEMPLATE.md; | source.md:76 | T2 (0.93) |
| INF-022 | Guards: git diff --stat zero deletions; | source.md:77 | T2 (0.83) |
| INF-023 | File: .github/ISSUE_TEMPLATE/feature_request.yml. | source.md:80 | T4 (1.00) |
| INF-024 | Intro markdown gains: You can also use this form to propose a skill, command or agent, or to report one that is missing or misbehaves. | source.md:81 | T4 (0.93) |
| INF-025 | proposal description becomes: 'Describe the change you want to see. | source.md:82 | T4 (0.88) |
| INF-026 | After alternatives, three fields, all validations: required: | source.md:83 | T4 (1.00) |
| INF-027 | Guards: yaml.safe_load (the loader existing tests use); | source.md:91 | none (best T8 0.57) |
| INF-028 | File: .github/ISSUE_TEMPLATE/bug_report.yml. | source.md:94 | T5 (1.00) |
| INF-029 | File: .github/PULL_REQUEST_TEMPLATE.md. | source.md:97 | T2 (1.00) |
| INF-030 | File: CONTRIBUTING.md. | source.md:114 | T1 (1.00) |
| INF-031 | File: docs/onboarding/ironclaude-onboarding.html, slide s12 (lines 515-530) and the footer (line 579). | source.md:117 | T7 (0.69) |
| INF-032 | Eyebrow (line 516): <b>12</b> · Contributing and open topics · GitHub issues #289 and #290. | source.md:118 | T7 (0.91) |
| INF-033 | Heading (line 517): Contributing, and one open topic. | source.md:119 | T7 (0.86) |
| INF-034 | Intro (line 518): The contributing rules are settled for now; | source.md:120 | T7 (0.86) |
| INF-035 | Replace the second card (lines 525-528) with: | source.md:121 | none (best T7 0.50) |
| INF-036 | The first card (lines 520-524, worktrees) stays byte-identical. | source.md:128 | none (best T7 0.56) |
| INF-037 | Footer (line 579): Built from HOW-WE-WORK.md at commit <8-character SHA of commit 1> (same width as the current f3c1ef06). | source.md:129 | T7 (0.64) |
| INF-038 | Guards: the deck test (tokens: | source.md:130 | none (best T8 0.50) |
| INF-039 | 0 / On origin/integration before editing: run the 16 test files that read the guide, the deck or the PR template (list in section 5) and record the result / Baseline recorded in the PR body | source.md:136 | T8 (0.75) |
| INF-040 | 1 / Commit 1: C1 (guide) and the plugin copy / cmp exits 0; | source.md:137 | T1 (1.00) |
| INF-041 | 2 / Commit 2: C2, C3, C4, C5, C6 / Zero-deletion diff; | source.md:138 | none (best T2 0.33) |
| INF-042 | 3 / If origin/integration moved, rebase now (project rule), then recompute commit 1's short SHA / git rev-parse --short=8 <commit 1> | source.md:139 | T8 (0.71) |
| INF-043 | 4 / Read every deck slide against the guide at commit 1 / Notes in the PR body | source.md:140 | T8 (0.89) |
| INF-044 | 5 / Commit 3: C7 with the footer set to the SHA from step 3 / git diff --quiet <sha> HEAD -- src/superclaude/core/HOW-WE-WORK.md and git diff --quiet <sha> -- src/superclaude/core/HOW-WE-WORK.md both exit 0 | source.md:141 | T8 (0.94) |
| INF-045 | 6 / After any later rebase or review-fix commit that touches the guide, repeat steps 3 and 5 / Same two commands | source.md:142 | T8 (0.83) |
| INF-046 | 7 / PR body: decisions table (D6 "deferred, no issue yet"), baseline and final test results, schema check, a request for a merge commit (squash and rebase merges rewrite SHAs and both are enabled), the PR-template note, same-link re-publication of the deck as an operator step, the owner follow-ups / Listed in section 6 | source.md:143 | T8 (0.89) |
| INF-047 | Baseline and final runs: every test file that reads the guide, the deck or the PR template: | source.md:147 | T8 (0.90) |
| INF-048 | make verify-sync proves nothing about the guide (its target does not compare core files); do not cite it for the guide. | source.md:148 | T8 (0.83) |
| INF-049 | Static checks: cmp of the guide and plugin copy; | source.md:149 | T8 (0.83) |
| INF-050 | Manual scenarios (recorded in the PR body): a missing-skill request, a broken-skill report answering "solution unknown", a non-primitive request, a primitive PR and a non-primitive PR ("Not applicable"); | source.md:150 | T8 (1.00) |
| INF-051 | These prove wording, parity and agreement of the five surfaces, not that the future gate works. | source.md:151 | T8 (0.89) |
| INF-052 | Owner inputs still missing (named, not filled): evaluation success metric; | source.md:155 | none (best T1 0.44) |
| INF-053 | Follow-ups for the owner, not done here: (1) a routing-table row sending "propose or change a skill, command or agent" to /sc:issue --create (accepted risk, INV-011: | source.md:157 | T8 (0.91) |
| INF-054 | Deviations from the issue text, for the owner to see: the bug-form sentence (C4) and the CONTRIBUTING.md paragraph (C6) go beyond the files the issue names; | source.md:159 | T8 (0.65) |

## Reviewer verdict (merged)

mode: pre-execution review of the tasklist against its design (UC-1, read-only)
paths: PLAN = .dev/tasks/to-do/TASK-WF-designRev-20261126-045943/TASK-WF-designRev-20261126-045943.md; DESIGN = source.md in the same folder
inputs: variant 1 (qa lens), variant 2 (refactorer lens, the base), debate rounds 1 and 2 (adversarial/debate/), the invariant probe (adversarial/invariant-probe.md) and the orchestrator's scratch-repo git checks (adversarial/debate/consensus-after-round2.md, section "Orchestrator's scratch-repo facts")

## Verdict

<!-- Source: variant 1 verdict word (diff point S-001, agreed by both advocates); variant 2 scope sentence; debate/consensus-after-round2.md "Agreed points", merged per R-01 -->
<!-- Source: refactor-plan.md corrections to the base (verdict word replaced; DESIGN:189 replaces "the plan cannot be edited after that"), merged per R-04 -->

**FAIL.** The plan must be edited before `/sc:implement` runs. Every blocking finding is an edit to Task 8 or Task 7 wording; none needs a redesign. The edits belong in the plan before it runs because a hand edit to a placed plan skips the gate, and hand edits after placement are not to be relied on (DESIGN:189).

The seven blocking findings of the earlier review (its B1 to B7) are fixed; variant 1 and variant 2 both checked each one (its B1 at PLAN:53, B2 at PLAN:221, B3 at PLAN:33, :54, :222, :223, B4 at PLAN:214, B6 at PLAN:174-177 and :184, B7 at PLAN:52 and :221). Its B5 text is present as worded (PLAN:204-213), but the sequence it copies is not operationally sound; that is the source of B1 and B2 below.

## Adherence summary

<!-- Source: refactor-plan.md R-01 adherence line; finding counts from R-02 and R-03, merged per R-01 -->

- Tasks: 8. Tasks 1 to 6 are adherent without blocking changes. Task 7 carries B3. Task 8 carries B1 and B2.
- Findings: 3 blocking (B1, B2, B3), 2 medium (M1, M2), 8 notes (N1 to N8).
- Earlier review: its B1 to B7 are fixed as worded; its B5 sequence is not operationally sound (see B1 and B2).
- Deviations: 3 drift items (the blocking findings), 1 necessary deviation, 1 authorized expansion (two additions), no regression.

## Blocking findings

<!-- Source: refactor-plan.md final blocking list (three findings; the reviewer's label is not the grade), merged per R-02 -->

### B1 - Task 8's rebase step cannot run with the deck edit uncommitted

<!-- Source: variant 1 F1, variant 2 F2, debate C-001, debate/consensus-after-round2.md (scratch-repo facts), invariant-probe.md INV-001, INV-002 and INV-011, merged per R-02 -->

- affected action: the operator's rebase step, and the `cmp` check, the 16-file test rerun and the scope check that follow it.
- claim: Blocking (Missing), also Decision: Task 7 leaves the deck edited but uncommitted because `/sc:implement` does not commit; the operator steps commit 1 and 2, then rebase, and commit the deck (commit 3) only after the rebase. Git refuses a rebase with uncommitted tracked changes or a non-empty index, and the step has no `git fetch`, so "if it moved" is judged against a stale ref. The failure happens only when a rebase is needed ("if it moved"), so "cannot complete as written" (variant 1) is overstated: the operator has to improvise, and in this environment the obvious improvisation, a bare `git stash`, uses a stash list shared with other sessions. Verified by the orchestrator in a scratch repo: plain `git rebase` gives "cannot rebase: You have unstaged changes. additionally, your index contains uncommitted changes."; `git rebase --autostash` prints "Created autostash: <sha>", rebases and re-applies; with a conflict it leaves conflict markers, keeps the entry `autostash` in the stash list, and keeps a staged new file staged.
- evidence: PLAN:23; PLAN:164-188; PLAN:205-210; PLAN:207; DESIGN:139-141; variant-1 F1 and variant-2 F2; debate/consensus-after-round2.md (scratch-repo facts); the first plan had the same gap (archived plan line 190, cited in variant-2 F1).
- recommendation: replace the rebase bullet at PLAN:207 with this text, in plain prose: "Run `git fetch origin`. If `git merge-base --is-ancestor origin/integration HEAD` exits non-zero, run `git rebase --autostash origin/integration`; it sets aside the uncommitted deck edit and any staged files and re-applies them. If git prints 'Applying autostash resulted in conflicts', resolve the markers so the second `s12` card equals Task 7's HTML, then find the kept 'autostash' entry by the SHA git printed at 'Created autostash:' (`git stash list --format='%h %gd'`) and drop only that entry; never run `git stash pop`. After the rebase, copy the guide over the plugin twin if `cmp` reports a difference (commit the twin on its own), then re-run `cmp` and the 16 test files. Check scope with `git diff --name-only origin/integration...HEAD -- . ':(exclude).dev/tasks'`: it lists the files committed so far (seven before commit 3, eight after it)." This text also closes probe items INV-001 (the file count differs before and after commit 3), INV-002 (the re-copy and re-test run after every rebase, not only when the guide changed) and INV-011 (how to drop the kept entry safely).
- verifier: after the step, the second `s12` card equals Task 7's HTML, no conflict markers remain, and any `.dev/tasks` changes are back in the working tree (their staged state is not required; the staging bullet at PLAN:212 stages them again); `git diff --name-only origin/integration...HEAD -- . ':(exclude).dev/tasks'` lists seven files before commit 3 and eight after.

### B2 - Task 8 does not re-set the deck footer after a later rebase or guide fix

<!-- Source: variant 1 F2, variant 2 F1, debate C-002 and C-003, invariant-probe.md INV-003, INV-004 and INV-005, merged per R-02 -->

- affected action: the commit-time steps that Task 8 writes into ./artifacts/pr-body-notes.md.
- claim: Blocking (Missing), also Decision: after any later rebase or review-fix commit the plan only repeats the two guide-equality checks (PLAN:211); it never recomputes the commit ID the footer must name or re-sets the footer (the first rebase is handled at PLAN:207-209). A rebase gives commit 1 a new commit ID while both checks still pass (the checks take `<sha>` from commit 1, not from the footer); a review-fix commit that changes the guide makes both checks against commit 1 fail with no new reference defined. The deck test checks only the footer pattern, so no check compares the footer value with the guide commit. The plan narrowed DESIGN:142 (step 6: repeat steps 3 and 5) to "repeat the two checks": B5's text of the earlier review is present as worded (PLAN:204-213) but the copied sequence is not operationally sound.
- evidence: PLAN:209; PLAN:211; DESIGN:139-142; DESIGN:181; `.dev/brainstorms/20261126-031900-primitive-contribution-rules/merged-requirements.md`:140 ("re-set the footer if the SHA changed"); tests/docs/test_onboarding_deck.py:90-91; project rule (CLAUDE.md pre-PR check 2): rebase onto `origin/integration` before push, and review-fix commits are expected by `/sc:pr-submit --monitor 3`.
- recommendation: replace the bullet at PLAN:211 with: "Run the two guide-equality checks `git diff --quiet <sha> HEAD -- src/superclaude/core/HOW-WE-WORK.md` and `git diff --quiet <sha> -- src/superclaude/core/HOW-WE-WORK.md`, where `<sha>` is commit 1 as it stands after any rebase; both must exit 0, and the footer must equal `<sha>` unless it is marked pending. After any later rebase (done as the rebase step above) or review-fix commit, set `<sha>` to `git rev-parse --short=8 $(git log -1 --format=%H origin/integration..HEAD -- src/superclaude/core/HOW-WE-WORK.md)`, the newest branch commit that changed the guide; if it prints nothing, stop and report. If the footer differs from `<sha>` and is not marked pending, redo the slide review against the guide at `<sha>` and apply the footer step above with `<sha>` in place of commit 1: move the footer and commit the deck only when the review is all 'consistent', otherwise leave it and mark it pending. Then run the two checks once more." This closes probe items INV-003 (the pending case has an exit), INV-004 (commit 1 as it stands after the rebase) and INV-005 (an empty result stops the run).
- verifier: after a content-preserving rebase, after a review fix that edits the guide, and in the pending case, both checks exit 0 and the footer equals `<sha>` unless marked pending. Orchestrator checks in a scratch repo: `git log -1 --format=%H origin/integration..HEAD -- <guide>` returns the branch's own newest guide commit; `git merge-base --is-ancestor origin/integration HEAD` exits 0 when no rebase is needed and 1 when upstream moved.

### B3 - The commands-and-flags acceptance at PLAN:186 does not say where it applies

<!-- Source: variant 2 F3, invariant-probe.md INV-016, debate/round1-advocate-2.md (F3 re-verified); graded blocking by the orchestrator as judge, merged per R-02 -->

- affected action: Task 7's compliance check, run by `/sc:implement`'s per-task reviewer.
- grade note: graded blocking by the orchestrator as judge, a departure from both advocates, who held it at medium with 60 confidence.
- claim: Blocking (Decision): Task 7's acceptance says commands and flags appear inside `<code>` only as `/sc:help`, `/sc:recommend` and `--plugin`. Read across the whole deck it fails correct work, because the deck already holds `<code>/sc:workflow</code>` (line 180), `<code>/sc:implement</code>` (line 511) and `<code>--plugin</code>` in the footer (line 580). Task 7's compliance check is run by `/sc:implement`'s per-task reviewer, which sees the deck; a literal reading fails Task 7 and halts the run, and the plan cannot be repaired after the first step starts without a new package (`/sc:implement` stops with E-PLAN-CHANGED when the plan is edited after the first step starts; DESIGN:189: a hand edit to a placed plan skips the gate). The earlier review graded the same kind of acceptance, one that a correct edit cannot pass (its B1), blocking. The byte-equality check at PLAN:184 already fixes the new card's `<code>` elements, so the clause adds nothing the fix removes.
- evidence: PLAN:186; PLAN:184; docs/onboarding/ironclaude-onboarding.html:180, :511, :580; docs/onboarding/ironclaude-onboarding.html:520-524 (the worktree card has no `<code>`); invariant-probe.md row INV-016; debate/round1-advocate-2.md (F3 re-verified); source.md:177 (the earlier B1).
- recommendation: at PLAN:186 change "Commands and flags appear inside `<code>` only as" to "In the new card, commands and flags appear inside `<code>` only as" (two words added; the rest of the bullet stays).
- verifier: the Task 7 compliance check reads the clause as applying to the new card; `uv run pytest tests/docs/test_onboarding_deck.py -q` passes.

## Medium findings

<!-- Source: variant 2 F6, invariant-probe.md INV-010 and INV-018, debate/consensus-after-round2.md "Medium and notes"; recorded, not repaired by the reviser, merged per R-03 -->

- Medium: **M1 (variant 2 F6, probe INV-010)**: a plain `git commit` for commits 1 and 2 sweeps a staged `.dev/tasks` into them.
  - claim: a plain `git commit` for commits 1 and 2 sweeps a staged `.dev/tasks` into them, and the post-rebase scope check had no expected list (the list is fixed inside the B1 text above; the staging part is not repaired).
  - evidence: PLAN:205-207; PLAN:212; variant-2 F6; probe INV-010.
  - recommendation: fix for a later pass: commit with explicit paths (`git commit -m "<message>" -- <files>`).
  - verifier: the commit 1 and commit 2 bullets name their files after `--`, and neither commit holds a path under `.dev/tasks`.
- Medium: **M2 (probe INV-018)**: the staging bullet points to a scope check the operator does not read.
  - claim: PLAN:212 says "the eight files listed in the scope check below", which points to PLAN:222, a line the operator does not read (the operator works from ./artifacts/pr-body-notes.md).
  - evidence: PLAN:203; PLAN:212; PLAN:222.
  - recommendation: none proposed in the sources; recorded for a later pass (the reviser repairs blocking findings only).
  - verifier: none until a fix is proposed.

## Notes

<!-- Source: variant 2 F4, F5, F7 and F8; invariant-probe.md INV-012, INV-014, INV-015 and INV-020; recorded, not repaired by the reviser, merged per R-03 -->

- Note: **N1 (variant 2 F4)**: the reminder's placement can pull `**Bug Reports:**` into the quote block.
  - claim: a reminder placed after the blank line under `### Issue Reporting` merges `**Bug Reports:**` into the quote block.
  - evidence: contributing-code.md:377-379; PLAN:71.
  - recommendation: add "followed by a blank line" to PLAN:71.
  - verifier: the Task 2 reviewer.
- Note: **N2 (variant 2 F5)**: a bare `git diff -U0` compares with the index, not with `<base>`.
  - claim: PLAN:51 and PLAN:185 use a bare `git diff -U0`, which compares with the index, while the Constraints say every scope check compares against `<base>` (PLAN:24). The results differ only if a file is staged.
  - evidence: PLAN:51; PLAN:185; PLAN:24.
  - recommendation: use `git diff -U0 <base> -- <file>` (PLAN:24).
  - verifier: the Task 1 and Task 7 reviewers find `<base>` in the `git diff -U0` checks at PLAN:51 and PLAN:185.
- Note: **N3 (variant 2 F7)**: the form name and the CONTRIBUTING.md link anchor.
  - claim: the form is named "Feature request" while PLAN:40 and PLAN:129 say "Suggest an improvement"; the CONTRIBUTING.md link has no section-4 anchor (PLAN:95).
  - evidence: feature_request.yml:1-2; PLAN:40; PLAN:129; PLAN:95; DESIGN:192.
  - recommendation: optional (DESIGN:192): name the form "Feature request" and add `#4-rules-everyone-follows` to the link.
  - verifier: if taken, PLAN:40 and PLAN:129 name "Feature request" and the link at PLAN:95 carries `#4-rules-everyone-follows`.
- Note: **N4 (variant 2 F8)**: PLAN:200 names one schema result for two forms.
  - claim: PLAN:200 names one schema result while the executor checks only feature_request.yml (PLAN:123) and the bug form is checked at operator commit 2 (PLAN:206).
  - evidence: PLAN:200; PLAN:123; PLAN:206.
  - recommendation: in PLAN:200, say that the operator checks both forms at commit 2.
  - verifier: the Task 8 reviewer finds that statement in the PLAN:200 item.
- Note: **N5 (probe INV-012)**: a conflict while replaying commits 1 or 2 is not covered.
  - claim: a conflict while replaying commits 1 or 2 is not covered; the autostash stays held until the rebase ends, so the deck edit is absent during that stop.
  - evidence: invariant-probe.md row INV-012; PLAN:207 (no conflict handling for the replay).
  - recommendation: none proposed in the sources; recorded for a later pass.
  - verifier: none until a fix is proposed.
- Note: **N6 (probe INV-014)**: the three-dot scope check assumes no extra branch commits.
  - claim: the three-dot scope check assumes no commits beyond 1 and 2; any extra branch commit changes the list.
  - evidence: invariant-probe.md row INV-014; PLAN:207.
  - recommendation: none proposed in the sources; recorded for a later pass.
  - verifier: none until a fix is proposed.
- Note: **N7 (probe INV-015)**: review fixes pushed later can change the guide after the footer is set.
  - claim: review fixes pushed by `/sc:pr-submit` can change the guide after the footer is set; the operator must notice.
  - evidence: invariant-probe.md row INV-015; PLAN:211; project CLAUDE.md pre-PR check 2.
  - recommendation: none beyond the B2 text; recorded (the probe accepts that the operator follows Task 8's notes as written, shared assumption A-003).
  - verifier: none until a fix is proposed.
- Note: **N8 (probe INV-020)**: the first guide-equality check proves nothing when `<sha>` is the newest guide commit.
  - claim: when `<sha>` is the newest guide commit, the first equality check always exits 0; the second check and footer equality are the real guards.
  - evidence: invariant-probe.md row INV-020.
  - recommendation: none proposed in the sources; recorded.
  - verifier: none until a fix is proposed.

## Deviations

<!-- Source: merge brief (four-class table); Drift row from the R-02 blocking list; footer deferral and the two additions as classed in the earlier review's table (.dev/reflect/pre-designPlan-20261126041502/REPORT.md:215-216), merged per R-02 -->

| Class | Item | Evidence | Disposition |
|---|---|---|---|
| Drift | B1 to B3: Task 8's rebase step (PLAN:207), Task 8's guide-equality and footer step (PLAN:211) and Task 7's `<code>` acceptance (PLAN:186) cannot pass as written or drop a design requirement | the three blocking findings above | blocking; edit the plan before `/sc:implement` runs |
| Necessary deviation | Deck footer deferred to commit time: `/sc:implement` does not commit, so no task can name the guide commit | PLAN:23; src/superclaude/commands/implement.md:100 | keep; Task 8's commit-time steps move the footer or mark it pending (PLAN:209, as revised by B2) |
| Authorized expansion | The two additions beyond the files the issue names: the bug-form sentence (C4) and the `CONTRIBUTING.md` paragraph (C6) | DESIGN:159; PLAN:217 | keep; recorded in Task 8's pull request notes |
| Regression | none | pre-execution review; no diff exists | none |

## Checked and sound

<!-- Source: variant 2 "Checked and sound" (kept), with the earlier review's B1 to B7 status from R-01 and the B5 wording of debate C-003, merged per R-04 -->

- Earlier B1 fixed (PLAN:53). The guide and its plugin twin have 0 non-ASCII lines today (grep), so a correct edit passes.
- Earlier B2 fixed (PLAN:221: "every item listed above", no count).
- Earlier B3 fixed (PLAN:33, :54, :222, :223, :207). Pytest leftovers are ignored by git (.gitignore:2, :40, :48).
- Earlier B4 fixed (PLAN:214 matches DESIGN:180).
- Earlier B5 text present as worded (PLAN:204-213 match each clause of DESIGN:181; PLAN:188 has no "footer unchanged" check), but B5 (DESIGN:181) narrowed DESIGN:142 step 6 to "repeat the two checks", so the copied sequence is not operationally sound; this is the source of B1 and B2 above.
- Earlier B6 fixed. The card at PLAN:174-177 is byte-identical to DESIGN:123-126 (whole-line grep, same count in both files), and PLAN:184 checks it.
- Earlier B7 fixed (PLAN:52, :221). D1 to V1 name no person (merged-requirements.md:45-56).
- Variant 1 checked each of the earlier B1 to B7 against the plan and reached the same status (variant-1 "Checked and sound").
- Draft text for all seven components matches the design line for line (exact-line greps, equal counts in both files). The 16 test files are exactly the set that reads these files.

## Invariant probe resolutions

<!-- Source: invariant-probe.md (status and severity per row), dispositions from refactor-plan.md R-05, merged per R-05 -->

| ID | Probe status | Severity | Disposition |
|---|---|---|---|
| INV-001 | UNADDRESSED | HIGH | resolved by the revised text of B1 (the scope check lists seven files before commit 3 and eight after it); decision recorded, not re-debated |
| INV-002 | UNADDRESSED | HIGH | resolved by the revised text of B1 (the re-copy and re-test run after every rebase); decision recorded, not re-debated |
| INV-003 | UNADDRESSED | MEDIUM | resolved in B2 (the pending case has an exit) |
| INV-004 | UNADDRESSED | LOW | resolved in B2 (commit 1 as it stands after the rebase) |
| INV-005 | UNADDRESSED | LOW | resolved in B2 (an empty result stops the run) |
| INV-006 | ADDRESSED | LOW | no change needed |
| INV-007 | ADDRESSED | LOW | no change needed |
| INV-008 | ADDRESSED | LOW | no change needed |
| INV-009 | ADDRESSED | LOW | no change needed |
| INV-010 | UNADDRESSED | MEDIUM | recorded as M1 |
| INV-011 | UNADDRESSED | LOW | resolved in B1 (how to drop the kept entry safely) |
| INV-012 | UNADDRESSED | LOW | recorded as N5 |
| INV-013 | ADDRESSED | LOW | no change needed |
| INV-014 | UNADDRESSED | LOW | recorded as N6 |
| INV-015 | UNADDRESSED | LOW | recorded as N7 |
| INV-016 | UNADDRESSED | MEDIUM | adopted as B3 |
| INV-017 | ADDRESSED | LOW | no change needed |
| INV-018 | UNADDRESSED | LOW | recorded as M2 |
| INV-019 | ADDRESSED | LOW | no change needed |
| INV-020 | UNADDRESSED | LOW | recorded as N8 |

## Not checked

<!-- Source: variant 2 "Self-reported confidence" scope statement, variant 1 closing statement, debate round 2 method lines; INFERRED premise settled per refactor-plan.md, merged per R-04 -->

- Not every one of the 16 test files was read in full (variant 2).
- No test, schema validation or browser check ran, and no file changed (variant 1). The plan was not executed, so B1 to B3 are traced from the written steps.
- The git behaviour behind B1 and B2 was run by the orchestrator in a scratch repo, not in this worktree; the advocates reasoned from git's documented behaviour. Variant 2's premise that git refuses the rebase is no longer INFERRED: the scratch repo verified it.

## Recommendations

### Recommendation R-001: Make Task 8's rebase step runnable
- **File:** `.dev/tasks/to-do/TASK-WF-designRev-20261126-045943/TASK-WF-designRev-20261126-045943.md` (Task 8, the rebase bullet at PLAN:207)
- **Change:** replace it with the text of B1 above (fetch, the `--is-ancestor` test, `git rebase --autostash`, safe drop of a kept entry, twin re-copy and re-test after every rebase, the scope check with seven files before commit 3 and eight after).
- **Verifier:** after the step the second `s12` card equals Task 7's HTML and no conflict markers remain; the scope check lists seven files before commit 3 and eight after.
- **Linked deviation(s):** B1
- **Priority:** P0

### Recommendation R-002: Re-set the deck footer after later rebases and guide fixes
- **File:** the same tasklist (Task 8, the guide-equality bullet at PLAN:211)
- **Change:** replace it with the text of B2 above.
- **Verifier:** after a content-preserving rebase, after a review fix that edits the guide, and in the pending case, both guide-equality checks exit 0 and the footer equals `<sha>` unless marked pending.
- **Linked deviation(s):** B2
- **Priority:** P0

### Recommendation R-003: Scope the commands-and-flags acceptance to the new card
- **File:** the same tasklist (Task 7, the bullet at PLAN:186)
- **Change:** add "In the new card, " in front of "commands and flags appear inside `<code>` only as ...".
- **Verifier:** the Task 7 compliance check reads the clause as applying to the new card; `uv run pytest tests/docs/test_onboarding_deck.py -q` passes.
- **Linked deviation(s):** B3
- **Priority:** P0

## Inferred-claim audit

- `citations_inferred: 0`
- Inferred-fraction: `0 / 100` = 0.00
