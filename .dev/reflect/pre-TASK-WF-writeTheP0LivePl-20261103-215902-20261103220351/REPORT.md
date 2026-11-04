# Reflect report: pre-execution review of the P0 live plan

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.87
citations_total: 63
citations_revalidated: 63
citations_dropped: 0
citations_inferred: 0
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

Subject: `.dev/tasks/to-do/TASK-WF-writeTheP0LivePl-20261103-215902/TASK-WF-writeTheP0LivePl-20261103-215902.md` (the plan, called "plan" below; `plan:N` is its line N).
Driving request: `.dev/tasks/to-do/TASK-WF-writeTheP0LivePl-20261103-215902/source.md`.
Underlying spec cited by the plan: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (`spec:N`).

## Verdict

Run status is partial: the adversarial merge ran its five steps in one agent without separate advocate agents, which its own contract records as partial. Zero citations were dropped out of 63 (zero-drop flag set in audit.log).

FAIL: 2 blocking findings. Merged by sc:adversarial Mode A over three heterogeneous reviewers (sonnet analyzer, glm-5.3 qa, opus refactorer), convergence 0.76, unresolved conflicts 0, no unaddressed HIGH invariants. The merge ran its five steps in one agent without separate advocate agents (`adversarial/return-contract.yaml`: invocation_method manual, fallback_mode true).

Calibrated confidence: Tier 1 card 0.82; reviewer cards 0.87, 0.86, 0.87 (calibrator class fable, disjoint from every reviewer class). The header value 0.87 is the mean of the three Tier 2 cards, rounded.

Coverage: no labelled requirement IDs in the request (parsed 0), 24 inferred requirements, union coverage 0.75 (`artifacts/coverage-matrix.yaml`). The qa reviewer re-derived the six unmatched rows and found each covered in substance in different words (`reviewer-cards/reviewer-2-card.yaml`, self_audit).

Every fix must land in the plan before `/sc:implement` writes its first task start line; an edit after that halts the run with E-PLAN-CHANGED (`~/.claude/skills/sc-implement-protocol/refs/managed-workspace.md:43`).

## Findings

| ID | Severity | Finding | Evidence |
|---|---|---|---|
| D-001 | blocking | The executor's required `git add .dev/tasks` after the archive move stages the superseded package, after FINAL and after Task 5's unstage | `~/.claude/skills/sc-implement-protocol/refs/managed-workspace.md:36` |
| D-002 | blocking | Task 1's AC allows "four untracked folders"; five exist (this reflect folder is the fifth) and no saved status file backs the AC | plan:52 |
| D-003 | should-fix | Step 7 drops `--run`, so another session's reclaimable worker fails a correct check; the run Task 1 creates is never used | plan:38; spec:293 |
| D-004 | should-fix | No exit for a parked, stalled or failed-to-start worker; Step 3 waits with no bound | plan:33 |
| D-005 | should-fix | The managed FINAL may read intended failures (the 3 failing symptom tests, a recorded live-check FAIL) as issues and block the archive | `~/.claude/skills/sc-implement-protocol/refs/qa.md:310` |
| D-006 | should-fix | End-state ACs name live state (worktree list, HEAD) with no saved evidence file | plan:80 |
| D-007 | should-fix | Retry attempts A3-A5 would re-run a one-shot live check and move its evidence | `~/.claude/skills/sc-implement-protocol/refs/retry.md:11` |
| D-008 | should-fix | No resume rule; re-entering a live task can start a second worker | plan:25 |
| D-009 | should-fix | Orca flags and receipt fields are used without any check, and cannot be corrected once the run has started | `.dev/orca-command-refactor/inventory/orca-capabilities.md:115` |
| D-010 | should-fix | The branch-remaining check probably uses the wrong branch name | plan:39 |
| D-011 | should-fix | The workflow worker stages `.dev/tasks` in its worktree and nothing records it; plan:22 overclaims | plan:22 |
| D-012 | should-fix | The 240 s blocking wait outlives the default 120 s Bash tool timeout | plan:32 |
| D-013 | should-fix | Task 3's plan-file copy is only in the AC, not in the evidence-copy instruction, and Remove deletes the worktree | plan:37 |
| D-014 | minor | `--base-branch` may not resolve to the unpushed local commit | plan:29 |
| D-015 | minor | An absent `observation.agentWait` passes "never non-null" vacuously | `.dev/orca-command-refactor/inventory/orca-capabilities.md:129` |
| D-016 | minor | The unattended-section grep exits 1 on its passing result | plan:30 |
| D-017 | minor | AC-0.6 needs a transcript read the plan does not place | plan:73 |
| D-018 | minor | The brief's Worktree slot uses text the template does not offer | plan:67 |
| D-019 | minor | The live-check procedure sits inside Constraints; keep it there | plan:28 |
| D-020 | minor | Task 5 weakens spec line 291's heartbeat requirement | plan:139 |
| D-021 | minor | Step 3 does not say how `--report-path` is matched to the relative report file | plan:33 |
| D-022 | minor | The phase report omits the quoted AC-0.6 excerpt spec line 303 asks for | plan:139 |
| D-023 | minor | A step-2 turn can return the completion message; briefs need shell-safe quoting | plan:32 |

Full claims, sources and fixes: `adversarial/merged-verdict.yaml`. Debate record: `adversarial/debate-transcript.md`.

## Deviations from the driving spec

### Deviation D-003: Step 7 is not scoped to the run

- **Location:** plan:38
- **Mapped tasklist item:** Constraints (live-check procedure, Step 7); Tasks 2-4
- **Spec section:** 7.2 step 7
- **Evidence:** "then `orca orchestration worker-list --terminal-state reclaimable --json`" (plan:38) against "worker-list --run <run_id> --terminal-state reclaimable --json` returns no rows" (spec:293)
- **Classification:** drift
- **Classification rationale:** the plan restates a spec step without a qualifier the spec requires, with no rationale given.
- **Default remediation:** Use `worker-list --run <run_id from ./artifacts/live-run.json>` in Step 7.

### Deviation D-020: Heartbeat-length rule weakened

- **Location:** plan:139
- **Mapped tasklist item:** Task 5
- **Spec section:** 7.2 step 5
- **Evidence:** "Name at least one checked run that lasted longer than the heartbeat cadence, or state that none did" (plan:139) against "so each phase report names at least one checked run that lasted longer than the cadence" (spec:291)
- **Classification:** drift
- **Classification rationale:** the plan adds a fallback the spec does not allow, unmarked.
- **Default remediation:** Record "none did" as a flagged coverage gap in the P0 verdict, not a clean pass.

### Deviation D-022: AC-0.6 excerpt not in the phase report

- **Location:** plan:139
- **Mapped tasklist item:** Task 5
- **Spec section:** 7.3 AC-0.6 row
- **Evidence:** "AC-0.6 (`./artifacts/ac-0.6.md`), each with its verdict and evidence path" (plan:139) against "the phase report states yes or no with a quoted excerpt" (spec:303)
- **Classification:** drift
- **Classification rationale:** the spec places the excerpt in the phase report; the plan keeps it one file away.
- **Default remediation:** Require the AC-0.6 row of the phase report to carry the quoted excerpt.

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation (file:line) | Match result |
|---|---|---|---|
| INF-001 | /sc:troubleshoot "<real symptom>" --output-dir <dir> with no --fix and no --depth deep | source.md:1 | unmapped |
| INF-002 | /sc:workflow "<small change>" --handoff none | source.md:1 | T3 |
| INF-003 | /sc:adversarial --compare <two files> --depth quick --output <dir> | source.md:1 | T4 |
| INF-004 | each run directly by the worker with the AC-0.4 report-file and outcome rule in its brief | source.md:1 | C10 |
| INF-005 | AC-0.5 (timed worker-start under 45 s with the normal launch setup) | source.md:1 | C9 |
| INF-006 | AC-0.6 (whether worker-read --source transcript names tool calls, with a quoted excerpt) | source.md:1 | C10 |
| INF-007 | all seven section 7.2 steps per live check | source.md:1 | C2 |
| INF-008 | fresh disposable worktree created by Orca at its default path from branch ironbelly/OrcaCLICommandRefactor-Specs at 8db29f11, never under .dev/worktrees/ | source.md:1 | unmapped |
| INF-009 | make sync-dev inside it before dispatch unless --setup run is confirmed to do it | source.md:1 | C10 |
| INF-010 | orca worktree rm after step 7 | source.md:1 | C10 |
| INF-011 | a P0 phase report in the package artifacts that combines the static report (.dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/p0-static-report.md, cited not copied) with the live results and states the phase verdict | source.md:1 | unmapped |
| INF-012 | for troubleshoot use a real current symptom from the static run's accepted pre-existing failures (.dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t1-accepted-failures.md) | source.md:1 | unmapped |
| INF-013 | for workflow a small harmless change prompt | source.md:1 | unmapped |
| INF-014 | for adversarial two existing committed files under .dev/orca-command-refactor/ | source.md:1 | T4 |
| INF-015 | no edit to any source, command, skill, agent or test file | source.md:1 | C3 |
| INF-016 | no git commit, push, PR, gh write or superclaude install | source.md:1 | C4 |
| INF-017 | no interaction with the SuperClaude-Org upstream | source.md:1 | C4 |
| INF-018 | UV only | source.md:1 | T1 |
| INF-019 | never stage .claude/ | source.md:1 | C6 |
| INF-020 | leave the superseded package .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/ unstaged and untouched | source.md:1 | C6 |
| INF-021 | stage .dev/tasks at the end | source.md:1 | T5 |
| INF-022 | the live plan is executed by /sc:implement in a top-level session the person opens (depth 0, the coordinator), never inside an Orca worker, since its own live checks start Orca workers | source.md:1 | C1 |
| INF-023 | A failed live check is recorded in the phase report, not retried silently; per spec AC-0.4 a failure reopens section 1. | source.md:1 | C7 |
| INF-024 | The plan must fix concrete inputs in advance, not leave them to the executor | source.md:1 | unmapped |

## Inferred-claim audit

- `citations_inferred: 0`
- Inferred-fraction: 0 / 63 = 0.00

## Recommendations

### Recommendation R-001: Re-unstage the superseded package after every `git add .dev/tasks`

- **File:** plan (Constraints)
- **Change:** Add a bullet: every `git add .dev/tasks` in this run, including the executor's re-add after the archive move, is followed by `git restore --staged -- .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950`; retitle `staged.txt` as the pre-archive snapshot and have the phase report name the post-archive `git diff --cached --name-only` check.
- **Verifier:** after the run, `git diff --cached --name-only` lists nothing under `TASK-WF-orcaWorkerContra-20261102-231950`.
- **Linked deviation(s):** D-001
- **Priority:** P0

### Recommendation R-002: Replace the four-folder AC with a saved baseline comparison

- **File:** plan (Task 1, Constraints)
- **Change:** Task 1 first saves `git status --porcelain` to `./artifacts/status-baseline.txt`; the AC compares a saved end status against it and this package; add `.dev/reflect/` to the leave-untouched list.
- **Verifier:** re-read plan:52 and plan:24; the AC names two saved files and no folder count.
- **Linked deviation(s):** D-002
- **Priority:** P0

### Recommendation R-003: Check every Orca flag before the run starts

- **File:** plan (Constraints, Task 1)
- **Change:** Before `/sc:implement` starts, run `orca <verb> --help` for every verb the procedure uses and correct the plan text (including `--run`, `check --ack`, `worker-read --cursor`, `worktree create --no-parent`, `worktree rm --worktree path:`, the run-create receipt field, and whether `--base-branch` takes a local branch); Task 1 saves the help output to `./artifacts/orca-help.txt`; a Constraint says a usage error is recorded, never corrected at run time.
- **Verifier:** every flag in the procedure appears in `./artifacts/orca-help.txt`.
- **Linked deviation(s):** D-003, D-009, D-014
- **Priority:** P1

### Recommendation R-004: Add failure branches, a resume rule and a no-rerun rule for retries

- **File:** plan (Constraints, live-check procedure)
- **Change:** Add branches for a failed start (release, then Step 7 and Remove), a parked or stalled worker (record, wait to a stated cap, stop only on Orca's stall proof or the person's go-ahead, then `task-update --status failed --result cancelled`); a resume rule that reuses an existing `p0-live-<name>` worktree or worker; and a rule that fix passes and retries on Tasks 2-4 only rebuild artifacts from saved evidence.
- **Verifier:** re-read the procedure; each branch names its commands and the evidence file it writes.
- **Linked deviation(s):** D-004, D-007, D-008
- **Priority:** P1

### Recommendation R-005: Name expected-failure logs and verdict files for the final review

- **File:** plan (Constraints)
- **Change:** State that `symptom-check.txt` passes when it shows exactly the three named failures, that step files and a P0 FAIL are recorded results, and that each `lc<N>-result.md` ends with a recording-status line the executor cites.
- **Verifier:** re-read the new Constraint against `~/.claude/skills/sc-implement-protocol/refs/qa.md:310`.
- **Linked deviation(s):** D-005
- **Priority:** P1

### Recommendation R-006: Save evidence for every live-state AC and the branch and index state

- **File:** plan (Remove bullet, Step 6, Tasks 2-5)
- **Change:** Save `orca worktree list --json`, the feature worktree HEAD, `git -C <path> branch --show-current` and `git -C <path> diff --cached --name-only` to `./artifacts/lc<N>-*` files; Task 5 saves `head-final.txt`; Task 3 also copies the new package's plan file; each AC cites its file; reword plan:22.
- **Verifier:** every AC in Tasks 1-5 names a `./artifacts/` file.
- **Linked deviation(s):** D-006, D-010, D-011, D-013
- **Priority:** P1

### Recommendation R-007: Run waits with a Bash timeout above the wait length

- **File:** plan (Step 2)
- **Change:** Add: run every `check --wait` with a Bash tool timeout of at least 300000 ms; a tool timeout is re-issued, not a check failure.
- **Verifier:** re-read plan:32.
- **Linked deviation(s):** D-012
- **Priority:** P1

### Recommendation R-008: Apply the minor wording fixes

- **File:** plan
- **Change:** Apply the fixes listed for D-015 to D-023 in `adversarial/merged-verdict.yaml` (null vs absent samples, grep exit code, AC-0.6 read placement, Worktree slot note, heartbeat gap, report-path rule, AC-0.6 excerpt, step-2 message handling and brief files).
- **Verifier:** re-read each cited plan line.
- **Linked deviation(s):** D-020, D-022
- **Priority:** P2
