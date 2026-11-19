```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.77
citations_total: 31
citations_revalidated: 31
citations_dropped: 1
citations_inferred: 0
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

# Reflect report (pre-execution): plan TASK-WF-refactorScIssueC-20261118-041634

Verdict on the plan: **FAIL as written** (one blocking finding, four medium findings). The plan covers both parts of the request (5 of 5 inferred requirements mapped), but Task 3 relaxes a stop rule that the request never asked to change. Status is `partial` because the adversarial merge ran one scoring pass instead of two (see Run notes).

Plan: .dev/tasks/to-do/TASK-WF-refactorScIssueC-20261118-041634/TASK-WF-refactorScIssueC-20261118-041634.md. Spec: the source.md beside it. Paths below are repo-relative.

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | "(1) remove /sc:brainstorm from the simple feature row of refs/chains.md so it becomes /sc:workflow --depth quick then /sc:implement" | source.md:1 | Task 1, Task 2 |
| INF-002 | "(2) default --pipeline to full when a person types the command" | source.md:1 | Tasks 3 to 9 |
| INF-003 | "leaving the issue watcher on its explicit --pipeline none" | source.md:1 | Constraints bullet 2, Task 5 acceptance |
| INF-004 | "Code: src/superclaude/commands/issue.md, src/superclaude/skills/sc-issue-protocol/, tests/commands/test_issue_command.py, tests/issue_watch/test_launch.py." | source.md:1 | Tasks 3, 4, 5 (test_launch.py is deliberately not edited) |
| INF-005 | "claim-handoff-planb edits the same files." | source.md:1 | Constraints bullet 4 |

Union coverage is 5 of 5 (1.00). The parsed-only figure is null because the source has no labelled requirement IDs, which sets `coverage_degraded: parsed-sparse` and forced Tier 2.

## Findings (merged verdict: adversarial/merged-verdict.yaml)

### Finding M1 (BLOCKING): Task 3 relaxes the E-SUBMIT-NEEDS-FULL stop rule

- **Location:** src/superclaude/commands/issue.md:57
- **Mapped tasklist item:** Task 3, Task 4, Task 5, Task 7
- **Spec section:** source.md:1 "(2) default --pipeline to full" (asks for a default level only)
- **Evidence:** the rule today reads "`--submit` with a value, or without `--pipeline full`: STOP `E-SUBMIT-NEEDS-FULL`" (src/superclaude/commands/issue.md:57); the same wording sits in src/superclaude/skills/sc-issue-protocol/SKILL.md:154 and docs/user-guide/commands.md:371; the design record requires the opposite of the plan: "`--submit` with a value, or with `--pipeline worktree` or `--pipeline none` or no `--pipeline`: STOP" (docs/designs/sc-issue-claim-pipeline-flag.md:85); the script checks only the resolved level (src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1900-1901).
- **Classification:** n/a (UC-1 plan finding); graded blocking on the safety rule: following Task 3 lets a bare `--submit` commit, push and open a PR, which nobody authorized.
- **Classification rationale:** all three reviewers agreed after Round 2 that the rule must stay; the Round 2.5 probe (INV-005) showed that keeping the old words is not enough, because once the table says "Omitted means `full`" a model can read "without `--pipeline full`" as satisfied.
- **Default remediation:** keep the rule, copy the design wording "or no `--pipeline`" into issue.md:57, SKILL.md:154 and commands.md:371, and make Task 5 assert that phrase and that a bare `--submit` still stops.

### Finding M2 (medium): the launch-result text is wrong for the new default

- **Location:** src/superclaude/skills/sc-issue-protocol/refs/claim.md:142
- **Mapped tasklist item:** Task 4 (does not touch it)
- **Evidence:** the `launched` text opens "It stops at the plan boundary and waits; run the printed implement command" and then adds a separate sentence for `full` (src/superclaude/skills/sc-issue-protocol/refs/claim.md:142). The wording is older than the plan; the default makes it the common path.
- **Default remediation:** in Task 4 restrict the "waits; run ..." sentence to `worktree` and add a test that the `full` branch does not carry it.

### Finding M3 (medium): Task 10 staging leaves out the task package

- **Location:** .dev/tasks/to-do/TASK-WF-refactorScIssueC-20261118-041634/TASK-WF-refactorScIssueC-20261118-041634.md:118
- **Evidence:** Task 10 says "Stage only the `src/`, `tests/`, `docs/` and `plugins/` side", while the project rule says `.dev/tasks/` is always staged (CLAUDE.md:35-37).
- **Default remediation:** add `.dev/tasks/` to the staged list and an acceptance check that it is staged.

### Finding M4 (medium): the architecture reference still states the old default

- **Location:** docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:1557 and :1635
- **Evidence:** line 1557 gives `--pipeline` as `worktree` and cites issue.md:43-44; line 1635 repeats the old E-SUBMIT condition; no task updates this file.
- **Default remediation:** add the file to Task 7.

### Finding M5 (medium): a bare claim on a coordinator-owned issue starts a second agent at full

- **Location:** src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1515-1523, :1703-1708
- **Evidence:** a worker started by the coordinator writes only a pending nonce (orca_worktree.py:1515-1523), only the launch step writes a `launch` entry (src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1619-1631), and a later launch returns already_launched only when it reads one (orca_worktree.py:1703-1708); a re-claim by the same login is allowed (src/superclaude/skills/sc-issue-protocol/refs/claim.md:43). After the plan the unflagged path is `full`.
- **Default remediation:** record this as a known risk in the plan, or add one sentence to Task 3 or 4 saying not to bare-claim an issue a coordinator owns.

### Notes and low findings (M6 to M12)

- **M6 (note):** design-record lines still state the old default or chain: docs/designs/sc-issue-claim-pipeline-flag.md:66, :78, :87 and docs/designs/sc-issue-command.md:44, :238. Add to Task 8, with a "superseded" line under :238.
- **M7 (note):** record as out of scope: src/superclaude/cli/issue_pipeline/templates/worker-brief.txt:17-19 (coordinator path still starts the simple chain with brainstorm) and the owner-run bare launch prompts at docs/designs/issue-watcher-setup.md:616-619. Assumption A-004 ("no other bare caller") is therefore contradicted.
- **M8 (low):** for an already_launched result, `pipeline_level` must be the running agent's level, not the omitted-flag default (src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1705-1721).
- **M9 (low):** Wave 8 uses `<L>` without defining it (src/superclaude/skills/sc-issue-protocol/refs/claim.md:120); add "the same `<L>` as Wave 5".
- **M10 (low):** the simple-feature row is only a suggested route (src/superclaude/skills/sc-issue-protocol/refs/chains.md:7); state the plan goal as "the default simple-feature row".
- **M11 (note):** the command version stays 1.1.0 although the design bumped it when claim behaviour changed (tests/commands/test_issue_command.py:80-81).
- **M12 (note):** Task 9 copies the routing guide byte for byte; redo the copy after rebasing onto claim-handoff-planb instead of merging by hand.

## Tier and calibration

- Tier 1 card calibrated at 0.70 (self-reported 0.82); with `coverage_degraded: parsed-sparse` the Tier 1 stop is forbidden, so Tier 2 ran: three reviewers (sonnet, haiku, opus classes), blind-calibrated at 0.80, 0.71 and 0.79 (self-reported 0.80, 0.95, 0.80). Calibrator class could not be disjoint from the reviewers (`calibrator_diversity: degraded`).
- Debate: 2 rounds plus the invariant probe; 15 of 15 diff points converged. Reviewer 1 withdrew its ship-gate finding; reviewer 2 withdrew its blocking grade and its missing-test finding; reviewer 3 replaced its owner-decision finding with a definite plan change. No HIGH invariant stayed unaddressed.

## Run notes (departures from the protocol, all listed in the contract)

- Position-bias mitigation: one scoring pass, not two (`position_bias_passes: 1`); margin 0.11 so no tiebreak.
- Executor class unknown (`executor_class_resolved: false`): the anti-self-confirmation guarantee is weakened.
- Vendor diversity could not be derived from alias names (`t2_vendor_diversity: single`, warn-only).
- Evidence gate: the validator re-read all 31 citations and dropped 1 (the write-side citation of M5, restored above with the exact lines); that drop sets `status: partial`.
- Memory: `.superclaude/memory/reflect/last-pass-refactorScIssueC.md` written (gitignored); the tracked `docs/memory/reflect/deviation-patterns-*.md` file was not written because it would add an unrequested tracked file to the branch.
- This report was written whole instead of stub-first.

## Inferred-claim audit

- `citations_inferred: 0`
- Inferred-fraction: `0 / 31` = 0.00

## Recommendations

### Recommendation R-001: keep the E-SUBMIT-NEEDS-FULL rule and make its wording survive a stated default

- **File:** src/superclaude/commands/issue.md (also src/superclaude/skills/sc-issue-protocol/SKILL.md and docs/user-guide/commands.md)
- **Change:** keep the rule at issue.md:57; add "or no `--pipeline`" in all three places; drop the rewrite from Tasks 3, 4 and 7; Task 5 asserts the phrase and that a bare `--submit` still stops.
- **Verifier:** `uv run pytest tests/commands/test_issue_command.py -v` passes with a new assertion on the phrase; re-Read the three lines.
- **Linked deviation(s):** M1
- **Priority:** P0

### Recommendation R-002: restrict the "waits; run the printed implement command" text to worktree

- **File:** src/superclaude/skills/sc-issue-protocol/refs/claim.md
- **Change:** add this edit to Task 4 and add a test that the `full` branch does not carry the sentence.
- **Verifier:** `uv run pytest tests/skills/test_issue_protocol.py -v` passes with the new test.
- **Linked deviation(s):** M2
- **Priority:** P1

### Recommendation R-003: fix Task 10 staging

- **File:** the plan, Task 10
- **Change:** add `.dev/tasks/` to the staged paths and an acceptance check.
- **Verifier:** `git status --short` shows the task package staged and nothing under `.claude/`.
- **Linked deviation(s):** M3
- **Priority:** P1

### Recommendation R-004: widen Tasks 7 and 8 and record the out-of-scope items

- **File:** the plan, Tasks 7 and 8 and its out-of-scope list
- **Change:** add docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md (lines 1557, 1635) to Task 7; name docs/designs/sc-issue-claim-pipeline-flag.md lines 66, 78, 87 and docs/designs/sc-issue-command.md lines 44 and 238 in Task 8; list worker-brief.txt and issue-watcher-setup.md:616-619 as out of scope with reasons.
- **Verifier:** `grep -n -E "worktree. \(default|default .--pipeline worktree|unflagged claim is" docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md docs/designs/sc-issue-command.md docs/designs/sc-issue-claim-pipeline-flag.md` prints only lines that carry an "Amended 2026-11-18" or "superseded" note.
- **Linked deviation(s):** M4, M6, M7
- **Priority:** P1

### Recommendation R-005: state the coordinator-owned re-claim risk

- **File:** the plan, Constraints or Task 3
- **Change:** add one sentence: do not bare-claim an issue a coordinator already owns, because the unflagged path now starts an agent at `full`.
- **Verifier:** re-Read the plan constraint.
- **Linked deviation(s):** M5
- **Priority:** P2
