# Reflection report: pre-execution audit of the issue 834 plan against its spec (UC-1)

```yaml
contract_version: 1.9.0
status: success
mode: pre
tier_reached: 2
confidence_calibrated: 0.62      # Tier 1 card, blind-calibrated; reviewer cards 0.61 and 0.85
citations_total: 140
citations_revalidated: 140
citations_dropped: 0
citations_inferred: 5
citation_budget_policy: full_reread   # the evidence validator re-read every citation (140 of 140)
coverage_degraded: parsed-sparse
```

Short paths: PLAN = `.dev/tasks/to-do/TASK-WF-issueSummary-20261126-132314/TASK-WF-issueSummary-20261126-132314.md`; SPEC = the `source.md` beside it. The full graded table with evidence, fix and verifier columns is `adversarial/merged-reviewer-card.md`; this report renders it after the evidence gate (zero drops).

## What this audit found

The plan covers the scope change (scenario tests, controlled runs, evidence, gates, pull request notes), but three blocking gaps and ten medium gaps would let a wrong result pass.

- finding_counts: blocking 3, label_high 6, medium 10, note 5 (label_high counts the HIGH labels the reviewers put on the merged findings: M-01, M-02, M-03, M-04, M-05, M-06)
- Why Tier 2: the spec has no labelled requirement IDs, so Pass 1 found 0 and Pass 2 found 13 inferred rows. The parse-density guard (Step 1B.2b) forbids the Tier 1 stop (`coverage_degraded: parsed-sparse`). Mechanical coverage: 6 of 13 rows (`coverage_pct_union` 0.4615, `S_dev_density` 0.5385).
- Reviewers: reviewer 1 analyzer (haiku class, calibrated 0.61), reviewer 2 qa (opus class, calibrated 0.85). The executor class (sonnet) was removed from the pool, so the N=2 floor applies.
- Adversarial merge: convergence 0.94, base variant opus:qa (score 0.902 against 0.570), status partial because the invariant gate left four HIGH probe items open (INV-001, INV-002, INV-008, INV-011).

## Blocking findings

### Deviation M-01 (Blocking, Decision): the Phase 1 tests only check their own copy of the counting rule

- **Location:** PLAN:47-62, 81, 122-123, 139-141, 154, 171, 175
- **Mapped tasklist item:** Tasks 1 to 3, 9, 11
- **Spec section:** SPEC:23, 35, 43
- **Evidence:** `questions_for` is defined inside the test module (PLAN:47) and tied to the shipped rule only by phrase checks (PLAN:49). Phase 3 runs cover only additions-only, one user-stated-fact contradiction and the preserved flag (PLAN:122-123, 139-141, 154), yet PLAN:81 says the runs prove model behaviour and PLAN:171, 175 let the new tests back a criterion verdict. ACC:20 records the existing tests as "static wording/mutation tests".
- **Classification:** drift. The tests exist and nothing that worked is broken; the defect is what verdicts they may back.
- **Default remediation:** call the Phase 1 tests contract tests, cap acceptance criteria 2 and 5 at "partly evidenced" for every SPEC:43 scenario no controlled run exercises, add one run with several false facts and a record of whether additions survive in the contradiction runs.
- **Affected action:** the Task 9 verdicts on criteria 2 and 5 and the Task 11 closing-keyword decision.

### Deviation M-02 (Blocking, Missing, low margin): no stop when the harness cannot observe questions or block writes

- **Location:** PLAN:87-104 (90, 98, 102, 108, 111)
- **Evidence:** SPEC:35 says the estimate "must be revisited" if the isolated runner cannot intercept questions and GitHub posts; SPEC:43 forbids live test issues without asking the lead. Task 4 may answer "not available here" and Tasks 5 to 8 go ahead (PLAN:90, 98, 102). The self-test makes no model call (PLAN:108), so the question-observation half has no stop.
- **Classification:** drift. **Affected action:** the go or no-go between Task 4 and Task 5.
- **Default remediation:** Task 4 writes a stop report with a revised estimate to the lead when a dry print-mode run shows no `AskUserQuestion` event or write interception cannot be shown, and Task 5 does not start until the lead replies.

### Deviation M-03 (Blocking, Safety, open: unverified): GitHub writes other than through the `gh` binary, and unscanned run logs

- **Location:** PLAN:22, 88-89, 91, 108, 132, 159
- **Evidence:** "No GitHub writes of any kind" (PLAN:22) is enforced and checked only for `gh`. The run clone keeps the real fork URL as `origin` and "no push is ever made" is an assertion (PLAN:91). Raw event logs and run trees are written under the always-staged package `artifacts/` (PLAN:108; CLAUDE.md:37) with no secret scan before staging; `.gitignore:85` re-includes `.dev/tasks/**/*.log` and a `.jsonl` log has no ignore rule. `claude_process.py:233-241` documents that the run helper passes the operator environment to the child (the code behind it is `src/superclaude/cli/pipeline/process.py:175-178`, `os.environ.copy()`).
- **Not verified:** whether a credential helper, `insteadOf` rewrite, GitHub-capable MCP server or reachable token could actually write, and whether a run model could print its environment. No user config was read. The claim that `git check-ignore` confirmed the `.jsonl` point could not be confirmed by Read; the conclusion stands on the repository's ignore rules.
- **Classification:** drift. An unverified safety claim stays open; it is not dropped.
- **Default remediation:** isolated HOME and config outside the package, no GitHub-capable MCP server and no credential helper in a run, a non-pushable remote, a read-only after-run check of fork activity recorded in each run, and a scan of every run output for secret patterns before `git add .dev/tasks`.

## Medium findings (recorded; the workflow fix pass leaves them alone, the regenerated plan is asked not to repeat them)

- M-04 PLAN:171: says the six criteria are "quoted in ./source.md through the summary"; they are in ACC:16-21 and the SPEC:32-33 links do not resolve inside the package. Fix: quote the six criteria in Task 9 and add the claim-boundary files (SKILL:76,102-103, refs/claim.md:83,89-95, templates/launch-prompt.md:23-28) to criterion 4's citations.
- M-05 PLAN:148: only questions have an expected count; add an expected `issue create` count of 1 per run and treat a plain-text question or a missing post as a finding.
- M-06 PLAN:131: the contradiction runs never say which answer they supply; require "keep my wording" and a body comparison.
- M-07 PLAN:24: carries the 13:14 UTC closed observation as current fact; add a read-only `gh issue view` check.
- M-08 PLAN:171: nothing checks the claim posting and plan-approval boundary; add the file reads and an empty diff for those files.
- M-09 PLAN:141: the preserved-flag description says "Feature:" while the flag is `--mode bug`; use a description with no mode word.
- M-10 PLAN:165: criterion 6 is graded before its gates and pull request exist; mark it "pending" and refresh it in Task 11.
- M-11 PLAN:159: the matrix-wide stop sits only in Task 8; move it before Task 6.
- M-12 PLAN:200: `git diff --name-only origin/integration` misses untracked files; use `origin/integration...HEAD` plus `git ls-files --others --exclude-standard`.
- M-13 PLAN:112: the proof that runs loaded the `src/` workers is the harness's own hash list; require each run record to list the paths read from its own event log.

## Notes

- M-14 PLAN:92 "Task 7" should read "Tasks 6 to 8". M-15 PLAN:23 ties the claim-file differences to #852; they come from earlier changes. M-16 PLAN:33 should say to ignore the `<!-- -->` block. M-17 PLAN:73, 78 should limit the sentence check to the Wave 2 section. M-18 PLAN:68, 87, 111, 184: clarify the fragment constant and the `./artifacts/` base.

## Inferred requirements (Pass 2)

Spec has no labelled IDs, so all 13 rows are inferred; each quote is verbatim from the cited line (checked by `artifacts/coverage_match.py`). Containment match, threshold 0.6, single task.

| INF id | Verbatim quote (start) | Citation | Match result |
|---|---|---|---|
| INF-001 | "What remains is scenario regression coverage and recorded quick, standard and deep create runs ..." | SPEC:11 | none (best Task 9, 0.4231); covered across tasks, partly (M-05, M-06) |
| INF-002 | "The merged secrets rule deliberately adds a question-triggering exception ..." | SPEC:11 | none (best Task 9, 0.2857); covered by Constraints, Tasks 3 and 9 |
| INF-003 | "so the orchestrator must re-check that state and not treat these files as permission to reopen it ..." | SPEC:11 | none (best Task 11, 0.4167); reopening half in Constraints, re-check half missing (M-07) |
| INF-004 | "They do not execute notes-state scenarios or measure questions/posts. Keep them and add genuinely exercised cases." | SPEC:23 | none (best Task 3, 0.5385); see M-01 |
| INF-005 | "Preserve claim's direct posting, staged-recommendation distinction and worktree-only plan approval boundary." | SPEC:26 | none (best Task 9, 0.4615); see M-08 |
| INF-006 | "Controlled runs must load the revised skill, not a stale installed copy. No new production decision service is requested." | SPEC:27 | containment, Task 4 (0.6667) |
| INF-007 | "Assumption: an isolated runner can intercept question and GitHub-post tools ..." | SPEC:35 | none (best Task 2, 0.3333); see M-02 |
| INF-008 | "(1) regression tests for added-material-only, empty, contradiction-only and mixed notes ..." | SPEC:43 | containment, Task 3 (0.68) |
| INF-009 | "(2) the controlled-run evidence of actual question and post counts ..." | SPEC:43 | none (best Task 9, 0.5185); covered by Tasks 5 to 8, see M-05 |
| INF-010 | "If a criterion is already delivered, say so with the file and line." | SPEC:43 | containment, Task 11 (1.0); the real coverage is Task 9 |
| INF-011 | "Base branch is integration, not master." | SPEC:43 | containment, Task 11 (0.8) |
| INF-012 | "The pull request is opened with `Refs #834` unless it delivers every criterion." | SPEC:43 | containment, Task 11 (0.7778) |
| INF-013 | "Reopening is the lead's decision." | SPEC:45 | containment, Task 11 (0.75) |

The qa reviewer also found six requirement-bearing spans the matrix lacks (SPEC:11 first sentence, SPEC:18 no-preview rule, SPEC:20 depth paths, SPEC:33 linked criterion text, SPEC:43 "Do only what 852 left undone", SPEC:43 integration start); no inferred row was dropped by the evidence validator.

## Inferred-claim audit

- `citations_inferred: 5` (the "Not verified" header line, M-03's open safety status, M-03's exploit paths, M-13's plugin-directory resolution, the hook remark on line 44 of the merged card)
- Inferred-fraction: 5 / 140 = 0.04

## Degraded components and honest limits

- `codegraph`: index truncated (`graph:truncated`), lookup tools not listed (`graph:unlisted`); Grep, Glob and Read were the evidence floor.
- Executor class resolved from the session model (claude-gw-tier1b = the `sonnet` alias class), not from a flag, environment variable or commit hint (`executor_class_source: unknown` in the enum; the exclusion was applied anyway). The calibrator class is also sonnet, so executor and calibrator are not separated; `calibrator_diversity: degraded` against the executor, disjoint from the reviewers.
- Vendor diversity: single (all gateway tiers).
- Tier 1 card was written by the orchestrator (`hypothesis_source: inline-fallback`).
- Reviewer isolation: `disabled` (reviewers read the live tree, read-only agent type).
- The reviewer outputs were flagged by the harness as instruction-shaped; their directive-looking sentences were treated as findings.
- Memory: the tracked `docs/memory/reflect/deviation-patterns-issue-834-rest.md` was NOT written, so this pull request carries no unrelated tracked file (`memory_persist_skipped: tracked-file-out-of-scope`); the gitignored `.superclaude/memory/reflect/last-pass-issue-834-rest.md` was written.

## Recommendations

### Recommendation R-001: Limit what the Phase 1 tests may back
- **File:** the plan (Tasks 3, 9, 11)
- **Change:** call the Phase 1 tests contract tests; cap criteria 2 and 5 at "partly evidenced" for scenarios no run exercises; add a multiple-contradiction run and a mixed-notes record.
- **Verifier:** PLAN no longer says Phase 3 proves the Phase 1 scenarios; Task 9's matrix has a run row or a cap for each of the seven SPEC:43 scenarios.
- **Linked deviation(s):** M-01. **Priority:** P0

### Recommendation R-002: Add the stop-and-report step to Task 4
- **File:** the plan (Task 4, Task 5 dependency)
- **Change:** a stop report with a revised estimate when question observation or write interception is not available; Task 5 waits for the lead.
- **Verifier:** Task 4's file has a "stop report" section; Task 5's `Depends on` line names the lead's reply.
- **Linked deviation(s):** M-02, M-11. **Priority:** P0

### Recommendation R-003: Close the GitHub write paths and scan the run logs
- **File:** the plan (Tasks 4, 5, 6 to 8)
- **Change:** isolated HOME, no MCP or credential helper, non-pushable remote, fork-activity check per run, secret scan before staging.
- **Verifier:** `harness-feasibility.md` lists each control with its command and output; each `summary.json` carries the fork-activity result; a token-pattern search of `./artifacts/runs/` returns nothing.
- **Linked deviation(s):** M-03. **Priority:** P0

### Recommendation R-004: Fix the ten medium findings in the regenerated plan
- **File:** the plan (Tasks 6 to 9, 11)
- **Change:** apply the per-row fixes M-04 to M-13 above when the plan is rebuilt.
- **Verifier:** each row's own verifier in `adversarial/merged-reviewer-card.md`.
- **Linked deviation(s):** M-04 to M-13. **Priority:** P1
