# Reflect Reviewer — Deviation Findings

**Reviewer persona**: QA, focused on acceptance tests, verification evidence, and completion claims  
**Grounding root**: `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher`  
**Diff scope**: `e8db2fe660d9104cbe8cdbcdc6f2c967f4994f4b..26f551f41edece1f05c07a3c02d78325e365f6d1`  
**Timestamp**: `2026-11-08T04:47:59+00:00`  
**Total deviations**: 5  
**Verdict**: **FAIL**

| Status | Result |
|---|---|
| DONE | Independently inspected assertion bodies for the 12 assigned acceptance criteria, skip conditions, command registration, and recorded verification. |
| NEXT | Address the late-launch defect and prohibited test skips, then reverify the affected requirements. |

## Deviations

| # | Category | Location | What diverged | Evidence (file:line) | Severity |
|---|----------|----------|---------------|----------------------|----------|
| 1 | Regression | `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/cycle.py:1048` | **Blocking.** The last deadline check precedes the durable pending-state save. The launcher is then called unconditionally. If persistence advances elapsed time from 119 seconds to 121 seconds, a launch starts after the specified cutoff with its full 120-second timeout. This breaks the no-late-launch requirement and its 240-second budget calculation. Existing timing tests do not exercise a slow pending-state save. | Requirement: `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:647`. Unconditional call after save: `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/cycle.py:1060`. Persistence performs serialization, atomic writing, chmod, and directory synchronization: `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/record.py:370`. | HIGH |
| 2 | Drift | `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/tests/issue_watch/test_cli.py:1070` | **Blocking.** The task expressly prohibits test skips, but the suite contains four root-dependent skip expressions and one platform-dependent expression. The root conditions skip six test functions, comprising seven parametrized cases. Root runs therefore omit permission-denial checks for store reads, approver reads, lock opening, initialization, and reset behavior. Recorded non-root runs with zero skips do not establish compliance with the unconditional no-skip instruction. | Prohibition: `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:188`. Additional root conditions: `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/tests/issue_watch/test_cli.py:967`, `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/tests/issue_watch/test_record.py:739`, `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/tests/issue_watch/test_cycle.py:735`. Platform skip: `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/tests/issue_watch/test_cycle.py:4694`. | MEDIUM |
| 3 | Necessary deviation | `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/tests/issue_watch/test_cycle.py:4150` | **Non-blocking.** The acceptance test interprets “the rest launch” after the first 24 hours as subject to further rolling daily limits. It asserts at most six additional launches on day two, rather than exhaustion of the remaining issues for large inputs. This preserves the explicit six-per-rolling-24-hour invariant; interpreting the wording as requiring all remaining issues on day two would contradict that invariant for more than 12 issues. The task log discloses this interpretation. | Acceptance wording: `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/brainstorms/20261107-064825-github-issue-watcher/spec-final.md:363`. Narrowed second-day assertion: `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/tests/issue_watch/test_cycle.py:4154`. Disclosure: `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:1038`. | LOW |
| 4 | Authorized expansion | `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/phase-outputs/test-results/p9-g2-summary.md:2` | **Non-blocking.** The local acceptance gate uses the named affected test subsets rather than the original full-suite command. The decision register explicitly authorizes this replacement and assigns the full suite to CI. This is an authorized departure, not evidence that the full suite passed locally. | Authorization and superseded requirement: `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/06-gap-fill-decisions.md:28`. Recorded subset result and CI-only qualification: `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/phase-outputs/test-results/p9-g2-summary.md:8`. | LOW |
| 5 | Authorized expansion | `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/tests/issue_watch/test_module_boundaries.py:57` | **Non-blocking.** The boundary test permits the persistence module to import functions from the predicate module, rather than enforcing the design’s “types only” restriction. The executed task explicitly permits the parsing, formatting, and issue-number validation helpers. The test therefore enforces the task’s expanded boundary, not the original design table verbatim. | Original restriction: `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:239`. Explicit authorization: `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:332`. Test disclosure: `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/tests/issue_watch/test_module_boundaries.py:20`. | LOW |

## Adherence summary

- **Spec units audited: 13.** The 12 assigned acceptance criteria, plus the separate unconditional no-skip task requirement.
- **Fully adherent: 8.**
- **Authorized expansion: 2 | Necessary deviation: 1 | Drift: 1 | Regression: 1.**
- Each affected unit is counted once. The explicitly authorized split of timeout testing is incorporated into the deadline assessment, not counted again as a separate deviation.

## Notes

### Acceptance-test assessment

- Actual assertions substantiate durable pending state before launch, integer-only prompts, fixed launcher arguments and outcomes, real two-process locking, dry-run store immutability, audit fallback and rotation, exit precedence, and crash/restart at-most-once behavior.
- The seeded hostile-input tests use an independent input-validity oracle and literal prompt expectations. They are not merely comparisons against production-generated expected values.
- Deadline tests cover elapsed time crossing the cutoff during issue rereading and origin checking. They do not cover the persistence interval identified in finding 1. The authorized split between a real sleeping child and injected-clock orchestration tests does not authorize a late launch.
- The multi-day acceptance test proves the first two daily windows. For large inputs, it does not itself demonstrate eventual dispatch of every remaining issue over all subsequent days.

### Runtime registration

The six-symbol runtime ledger correctly identifies a limitation of static reachability through Click decorators and registration, not missing command wiring. The group is imported and registered in `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/main.py:563`. The real-subprocess tests exercise initialization and a polling cycle; the other commands have in-process command-runner coverage rather than equivalent subprocess coverage.

### Verification and completion claims

- Supplied verification reports record 2,635 watcher tests passing with zero skips, clean lint and formatting, and a passing affected-registration subset with one pre-existing skip outside the watcher.
- Gate records distinguish the passing local subset from a historical full-suite run that had four failures outside the watcher. I did not independently reproduce or establish the causes of those failures.
- Reviewed process boundaries, temporary executable stubs, isolated test environments, and write destinations support the test suite’s no-live-GitHub/Orca/network claim. They do not independently prove every historical executor action.
- Dependency, marker, and protected-file change claims rely partly on supplied comparison evidence. I did not independently execute a Git comparison.
- The gate verdicts are on disk, but their PASS labels do not resolve the source-level deadline defect or the explicit no-skip violation.

**Recommended action:** Remediate findings 1 and 2. The deadline correction must preserve both durable-before-launch ordering and the specified budget-exhausted outcome; add a test whose pending-state save crosses the cutoff.

No files were changed and no tests or commands were run by this reviewer. The deadline defect is established from source control flow, not a runtime reproduction.

## Blind calibration (attached by the orchestrator; full report: reviewer-2-calibration.md)

- Reviewer model class: haiku (persona qa). Calibrator class: opus (calibrator_diversity degraded).
- Calibrated confidence C = 0.82 (citation grounding 0.85, coverage completeness 0.75, deviation-classification clarity 0.90, risk surface 0.85, recommendation actionability 0.75). C < 0.85.
- Citation spot-check: 21 of 22 exact, 1 one line off (p9-g2-summary.md:9 not :8); none wrong.
- Finding 1 (Regression, HIGH): the calibrator re-read cycle.py:1039-1062 and confirms the control flow (no deadline check between the last check at 1048 and launch at 1062; save at record.py:370-378). Calibrator view: the Regression label is defensible against design 647, but the HIGH/blocking severity has no likelihood reasoning (the save is a local fsync; network filesystems are rejected for state_dir at cycle.py:50-52; worst case about 241 s of a 300 s cadence), and the card's own fix conflicts with design 647 ("the step ends with no entry"), because a check after the save would leave a pending entry with no launch.
- Finding 2 (Drift, skips): task line 188 bans skip/skipif/xfail outright; the code uses them; Drift is defensible.
