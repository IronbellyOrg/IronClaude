# Reflect report: P2 static plan (UC-1, pre-execution)

```yaml
contract_version: 1.8.0
status: partial   # 3 citations dropped by the evidence gate; convergence blocked by 2 HIGH invariants
mode: pre
tier_reached: 2
confidence_calibrated: 0.76   # mean of blind calibrations of the three Tier-2 cards (0.70, 0.78, 0.79)
citations_total: 184
citations_revalidated: 108
citations_dropped: 3
citations_inferred: 3
citation_budget_policy: sampled
coverage_degraded: parsed-sparse
```

> **Citation budget: sampled mode**
> - `citations_revalidated: 108` — size of the re-Read sample (every citation of the P1 deviations D-01..D-05, every Inferred-requirements row, every third citation of D-06..D-31).
> - `citations_dropped: 3` — drops observed in the sample only. This is the field that gates promotion (§14.5.2 condition 6a strict `== 0` check).
> - `citations_dropped_extrapolated: 5` — population-level estimate, `round(3 × (184 / 108))`. Recording-only; does not gate promotion. A non-zero value SHOULD prompt a follow-up `--depth deep` run that forces `full_reread`.
>
> The extrapolated value is telemetry, not a verdict. The sample-count is what the validator actually examined; the extrapolation is what it would have found if the budget had permitted a full re-Read.

## Summary

- **Subject.** Plan `.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md` (21 tasks, 7 phases) against its brief `source.md` and the worker-contract spec.
- **Coverage.** 30 requirement rows inferred from the brief (no requirement IDs, so `coverage_degraded: parsed-sparse`); all 30 map to plan tasks; INF-006 (the F1 "left out (WC-4)" rule) is only partly covered (D-09).
- **Tier 2.** Three read-only reviewers (sonnet analyzer, haiku-slot qa, opus refactorer), blind-calibrated 0.70 / 0.78 / 0.79; adversarial merge on base card 3 (score 0.844); 16/16 debate points agreed, but convergence is **BLOCKED_BY_INVARIANTS** (INV-001, INV-002).
- **Findings.** 31 merged findings: 5 P1, 13 P2, 13 P3; 8 need an owner decision. Every finding is a plan defect to fix before `/sc:implement`; none is an execution result.
- **Advisory.** This review never edits the plan (sc:workflow Wave 4 rule). The plan stays as written until the owner chooses what to change.

## Unaddressed invariants (blocking convergence)

- **INV-001** (guard_conditions, HIGH): The consensus fix for X-001 (block `run` when the safety flags are missing) can be written as a test. Evidence-gate correction: the cli-eval skill does name its safety flags ("the safety flags from the digest (`--no-pty`, `--no-mcp`, `--json`, `--junit`, `--timeout-mult`, `--keep-home`, `--max-disk-mb`, `--output-dir`)", src/superclaude/skills/sc-cli-eval-protocol/SKILL.md:138), so the open owner question narrows to which of them a brief must carry for `run` not to be blocked.
- **INV-002** (state_variables, HIGH): Once callees accept `--unattended`, the caller handles every worker_status the nested callee can now return.

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation (file:line) | Match result |
|---|---|---|---|
| INF-001 | Static plan only: the edits and the checks that need no live Orca run. | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:1 | matched (plan:21, Task 21) |
| INF-002 | per .dev/orca-command-refactor/specs/orca-worker-contract-spec.md section 6 (row P2), section 7.1 and 7.3 (the P2 checks) and the section 3 rows of the P2 commands | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:1 | matched (plan:19, Tasks 2-16) |
| INF-003 | applying .dev/orca-command-refactor/decisions/APPROVED.md | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:1 | matched (plan:19) |
| INF-004 | The P1 static plan is the model for this plan's structure and conventions | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:3 | matched (plan:25-43, Task 1) |
| INF-005 | P1 verdict PASS (lc09 and lc10 reclassified PASS by the owner on 2026-11-05). P2 may start. | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:6 | matched (plan:19) |
| INF-006 | Each P2 command's `artifacts` clause lists only files the run wrote, names the ignored files it leaves out and points at WC-4 for the reason ("left out (WC-4)") | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:7 | matched (plan:19, plan:25 (skeleton), Tasks 2,3,4,13,14) |
| INF-007 | This static plan does not depend on it; list it as an open owner question in the plan. | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:8 | matched (plan:20, Task 21) |
| INF-008 | each default-on gate resolves per its section 3 row under `--unattended` | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:10 | matched (Tasks 2-16) |
| INF-009 | WC-10 wait splitting for cli-eval (eval waits of at most 240 s) | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:10 | matched (Task 13) |
| INF-010 | Commands gaining `--unattended` and a `## Unattended mode` section in P2 (15) | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:10 | matched (Tasks 2-16, Task 20) |
| INF-011 | workflow (its reflect step passes `--unattended` and a nested report directory `<report-dir>/nested/reflect-<n>/`) | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:10 | matched (Task 17) |
| INF-012 | brainstorm (its automatic research enrichment passes `--unattended` and a nested report directory instead of being off) | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:10 | matched (Task 18) |
| INF-013 | Where a command has an outward default (auggie-review posting, task's `commit`/`push` and committed TFEP report), P2 only turns it off under `--unattended` (WC-9). | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:10 | matched (Tasks 10, 12) |
| INF-014 | P2 touches no safety rule and adds no outward capability. | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:10 | matched (plan:23) |
| INF-015 | AC-2.1's deletions check on src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md must print nothing (SA-6). | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:10 | matched (Task 15, Task 21) |
| INF-016 | Decide, with the spec's nested-propagation rule (section 2.1), what each arm does under `--unattended` ... and record it as a plan decision for owner approval. | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:12 | matched (plan D-P2-1, Task 18) |
| INF-017 | pin each rule with an exact phrase, never a single token that a clause can contain while saying the opposite | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:14 | matched (plan:27) |
| INF-018 | a "phrase present" check that replaces old wording also asserts the old wording is absent, scoped to the line that carries the rule | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:14 | matched (plan:27, Tasks 17, 18) |
| INF-019 | the exact files to edit ... acceptance criteria that are observable (a command, a grep, a test), and the tests to add or extend | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:16 | matched (Tasks 1-21) |
| INF-020 | never hardcode src/superclaude/ paths inside installed primitives; edit the src/superclaude/ sources, byte-copy the pinned plugin mirrors, run make sync-dev | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:16 | matched (plan:23-24, Tasks 6, 17, 21) |
| INF-021 | extend UNATTENDED_EXPECT and the commands-with-a-section list to the P2 commands | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:16 | matched (Task 1, Tasks 2-18) |
| INF-022 | plus one assertion per gate as AC-2.1 lists | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:16 | matched (Task 20 (P2_GATES)) |
| INF-023 | and the nested-invocation assertions for workflow and brainstorm | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:16 | matched (Tasks 17, 18, 20) |
| INF-024 | Include the static checks of section 7.1 and 7.3 that apply to P2 (AC-2.1, AC-C1 to AC-C6) | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:16 | matched (Task 21) |
| INF-025 | make lint, the ruff format check with the pinned ruff (`uv run --extra dev ruff`), make verify-sync | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:16 | matched (plan:43, Task 21) |
| INF-026 | the pre-existing tests that read the edited files | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:16 | matched (plan:44, Task 21) |
| INF-027 | a static report that states each result and the exact list of paths for the owner-approved commit | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:16 | matched (Task 21) |
| INF-028 | Do not execute the plan: no /sc:implement, no commit, no push, no superclaude install, no live Orca run. Stage nothing under .claude/. | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:18 | matched (plan:22) |
| INF-029 | when a test reads a clause with `_artifacts_clause`, the text the test needs sits after the first backticked `artifacts` on that line | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:14 | matched (plan:27) |
| INF-030 | each check must fail on the pre-change text | .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:14 | matched (plan:27, Tasks 2, 17, 18, 19 ACs) |

Postscript: the evidence gate re-read all 30 rows; none was dropped, so `coverage_pct_union` stays 1.0 (INF-029 and INF-030 were added at Wave 5 from the qa reviewer's recall check, R2-F5).

## Grounding Gaps

Per SKILL.md §11.2, the dropped citations and the claims they were cited for. No `grounding-gaps.yaml` was written: no finding lacks evidence to classify; each drop removes one citation while the finding keeps its other evidence.

### Gap G-01

- **Hunk ref:** src/superclaude/skills/sc-cli-eval-protocol/SKILL.md:137-139 (cited by D-03)
- **Evidence missing:** support for "the run options carry no 'safety' label"; line 138 names them "the safety flags from the digest".
- **Why not classifiable:** the cited text contradicts the sub-claim; D-03 stands on spec:164 (which names no flag) and narrows as stated under INV-001 above.
- **Next evidence needed:** the owner's choice of which of the eight safety flags a `run` brief must carry.

### Gap G-02

- **Hunk ref:** src/superclaude/commands/troubleshoot.md:148 (cited by D-04)
- **Evidence missing:** the flag is not in the command file; line 148 is a closing code fence.
- **Why not classifiable:** wrong file; the claim itself is supported at src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:148 and :645 and refs/diagnosability-audit.md:245.
- **Next evidence needed:** none; D-04 stands on its remaining citations.

### Gap G-03

- **Hunk ref:** plan:46 (cited by D-20)
- **Evidence missing:** plan:46 is decision D-P2-1 (brainstorm research), not the cleanup Safety Threshold clause.
- **Why not classifiable:** wrong line; the clause is at plan:53 (D-P2-8) and plan:97 (Task 2).
- **Next evidence needed:** none; D-20 stands on its remaining citations.

Out-of-sample note from the validator: D-06 cites plan:306 for "the clause stays"; that text is at plan:303.

## Deviations

### Deviation D-01: Task 16 (tasklist) leaves the Stage 9 nested sc:task call without --unattended or a nested report directory

- **Merged id / severity:** M-01 / P1
- **Location:** src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1535-1557
- **Mapped tasklist item:** Task 16, Task 12, Task 15
- **Evidence:** src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1535-1557; src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1539-1542; src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1612-1635; src/superclaude/skills/sc-task-protocol/SKILL.md:61,266; src/superclaude/skills/sc-task-protocol/SKILL.md:94; .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:77; .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:72,79; .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:182; plan:25; plan:26; plan:79; plan:233; plan:284-295; plan:290
- **Claim:** Task 16 misses the nested `sc:task` call in tasklist Stage 9, which runs `sc:task` through Skill with `--compliance strict` and loops back to it. Task 12 gives task `--unattended`, and the plan's own rule (plan:26) says a caller passes `--unattended` and a nested report directory to every callee that accepts it at P2. Task 16 nests only the Stage 10.5 reflect call; its EXPECTED_NESTING is ["reflect"] and it depends only on Task 15. Under --unattended, Stage 9 passes no `--unattended` (SKILL.md:1539-1542), so the nested sc:task (a) runs attended and can prompt inside a worker; (b) commits conditionally: a TFEP inside it keeps the committed-report default (sc-task-protocol/SKILL.md:61,266), breaking WC-9 (spec:77); (c) at STRICT compliance its `sc:impact-protocol` call (sc-task-protocol/SKILL.md:94) writes `.dev/impact/task-<slug>` outside the report directory (WC-4, WC-11; spec:72,79). The test data would lock the gap in.
- **Classification:** drift
- **Classification rationale:** sources R3-F1, INV-010; base-modified: harm sentence replaced per B1 ("push" dropped; conditional commit and impact-path harms added; test-literal and Task 12 dependency added to the fix); INV-010 (LOW) folded into suggested_fix per C16.
- **Default remediation:** In Task 16, make every Stage 9 sc:task call (loop-backs included) pass `--unattended --report-dir <report-dir>/nested/task-<n>/` and keep `--compliance strict` (M-14). Place `--unattended` as a standalone token outside the quoted input string, since the switch fires only on a standalone token (plan:25; INV-010). Add "task" to the tasklist `UNATTENDED_EXPECT` nested list and to the Task 20 `EXPECTED_NESTING` literal (plan:79, plan:290; M-13), add "Depends on: Task 12", and record it as a decision or spec observation (spec row 182 names only Stage 10.5).

### Deviation D-02: Task 13 (cli-eval) has no blocked outcome when the brief lacks the safety flags

- **Merged id / severity:** M-02 / P1 / owner decision
- **Location:** .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:164
- **Mapped tasklist item:** Task 13
- **Evidence:** .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:164; plan:60; plan:248; plan:330; src/superclaude/skills/sc-cli-eval-protocol/SKILL.md:128-153; src/superclaude/skills/sc-cli-eval-protocol/SKILL.md:30-33; src/superclaude/skills/sc-cli-eval-protocol/SKILL.md:46-58
- **Claim:** Spec row 164 says cli-eval `run` needs `--suite` and the safety flags in the brief, else blocked. Task 13 blocks only a missing `--suite` (plan:248) and treats the command line as given as the confirmed invocation, so the P2_GATES assertion ("--suite") passes with the safety-flag gate absent; W3 asks the user to confirm the flags (plan:60). The brief may pass the flags (plan:330); the gap is the missing block, not a launch with no safety inputs.
- **Classification:** drift
- **Classification rationale:** sources R2-F1, R3-F2, R1-F2; incorporated: V2 R2-F1 per Change C1, replacing base R3-F2 (after B5: FR-G5 and --no-pty parts removed, settled at plan:248); severity P1 per X-001.
- **Default remediation:** In Task 13, block a `run` whose brief lacks the safety flags, and add two separate assertions: `run` with no `--suite` resolves blocked; `run` whose brief lacks the safety flags resolves blocked. The flag subset is nameable from sc-cli-eval-protocol/SKILL.md:128-153, with the eval-docs-loader digest authoritative (SKILL.md:30-33,46-58). Which subset is the owner's choice; until it is named, carry the section as blocked-pending-decision (M-03).

### Deviation D-03: INV-001 (blocking): the cli-eval safety-flag subset is undefined, so the M-02 block cannot be tested

- **Merged id / severity:** M-03 / P1 / owner decision
- **Location:** .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:164
- **Mapped tasklist item:** Task 13
- **Evidence:** .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:164; src/superclaude/skills/sc-cli-eval-protocol/SKILL.md:137-139; plan:248; .dev/reflect/pre-TASK-WF-writeTheP2Static-20261107-011441-20261107013500/adversarial/diff-analysis.md:64; .dev/reflect/pre-TASK-WF-writeTheP2Static-20261107-011441-20261107013500/adversarial/rounds/round2-advocate-3.md:46,56
- **Claim:** The consensus fix for X-001 cannot be written as a test: spec:164 names no flag, the cli-eval run options at sc-cli-eval-protocol/SKILL.md:137-139 carry no "safety" label, and plan:248 says only "the run flags the brief passes". A-001 was QUALIFIED as an owner decision. Until the owner names the subset, Task 13's gate has no executable condition and its reverse-outcome negative test has no input, so the P1 stays open after the merge.
- **Classification:** drift
- **Classification rationale:** sources INV-001, A-001; incorporated: invariant-probe INV-001 per Change C14 (P1 blocking, linked to M-02).
- **Default remediation:** The owner names the safety-flag subset in the plan (from sc-cli-eval-protocol/SKILL.md:128-153), or the plan carries the cli-eval section as blocked-pending-decision. Blocking until resolved.

### Deviation D-04: troubleshoot --diagnosability-handoff starts a nested sc:workflow-protocol that Task 11 does not cover

- **Merged id / severity:** M-04 / P1 / owner decision
- **Location:** src/superclaude/commands/troubleshoot.md:148
- **Mapped tasklist item:** Task 11
- **Evidence:** src/superclaude/commands/troubleshoot.md:148; src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md:245,250; src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:645; src/superclaude/skills/sc-workflow-protocol/SKILL.md:28; .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:77; plan:220
- **Claim:** The troubleshoot `--diagnosability-handoff` flag (parsed at troubleshoot.md:148) calls `Skill sc:workflow-protocol` (diagnosability-audit.md:245,250; SKILL.md:645). Task 11 nests only `adversarial` (plan:220), and "diagnosability" appears 0 times in the plan. Under --unattended the flag starts an unflagged nested workflow, which runs `git add .dev/tasks` (sc-workflow-protocol/SKILL.md:28); WC-9 forbids that in a worker (spec:77).
- **Classification:** drift
- **Classification rationale:** sources R2A3-s3.1, E-1; incorporated: Round 2 advocate 3 new finding (s3 item 1) with orchestrator evidence E-1, per Change C13.
- **Default remediation:** Owner choice between two branches. Nest: Task 11 adds `workflow` to troubleshoot's nested list and to the Task 20 `EXPECTED_NESTING` literal (M-13) and changes the handoff's return-contract read path (M-12). Refuse: the troubleshoot Unattended section refuses `--diagnosability-handoff` under --unattended, with an exact-phrase assertion.

### Deviation D-05: INV-002 (blocking): a nested blocked or failed status has no path into the caller's return contract

- **Merged id / severity:** M-05 / P1
- **Location:** src/superclaude/skills/sc-task-protocol/SKILL.md:218
- **Mapped tasklist item:** Task 11
- **Evidence:** src/superclaude/skills/sc-task-protocol/SKILL.md:218; src/superclaude/skills/sc-task-protocol/SKILL.md:225-235; src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1535-1557; src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1555; .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:62; plan:26; plan:214-225
- **Claim:** Task 11 maps troubleshoot's deep short-input STOP to `blocked` (plan:214-225), but sc-task Step 4 branches only on test_is_wrong, docs, success, `recommended_escalation` none/retry/escalate_depth/halt and failed -> FULL STOP; there is no `status == blocked` branch. Tasklist Stage 9 gates only on "sc:task reports completion", so a nested `sc:task` returning `blocked` (after the M-01 fix) has no mapping into tasklist's worker_status. No plan rule (plan:26) or spec rule (spec:62, "only the top-level contract drives WC-5") says how a nested blocked/failed result propagates into the caller's status and `blocked_question`. Falsifying path: tasklist --unattended -> Stage 9 nested sc:task -> TFEP nested troubleshoot returns blocked -> sc-task has no branch -> undefined top-level status.
- **Classification:** drift
- **Classification rationale:** sources INV-002; incorporated: invariant-probe INV-002 per Change C15 (P1 blocking, linked to M-01).
- **Default remediation:** Add a plan rule, with an AC, defining how a nested `blocked` or `failed` status reaches the outer return contract (the caller's worker_status and `blocked_question`), covering sc-task Step 4 and tasklist Stage 9. Blocking until resolved.

### Deviation D-06: workflow.md:72 and refs/return-contract.md keep the stale .dev/reflect/ artifacts clause after Task 17

- **Merged id / severity:** M-06 / P2 / owner decision
- **Location:** src/superclaude/commands/workflow.md:72
- **Mapped tasklist item:** Task 17
- **Evidence:** src/superclaude/commands/workflow.md:72; src/superclaude/commands/workflow.md:75; src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md; tests/skills/test_worker_contract.py:770-775; plan:41; plan:297-309; plan:303; plan:306; src/superclaude/skills/sc-reflect-protocol/SKILL.md:58-62; src/superclaude/commands/reflect.md:101
- **Claim:** After Task 17, workflow's reflect step writes to `<report-dir>/nested/reflect-<n>/`, but workflow.md:72 still says `artifacts` lists each file the reflect step wrote in its `.dev/reflect/` run directory, and the plan says the clause in refs/return-contract.md stays (plan:306). Check ADDITIVE lets workflow.md delete one line (plan:41), which Task 17 spends on line 75 (plan:303), so line 72 stays stale. `_artifacts_clause` reads the first matching line (test_worker_contract.py:770-775), so an added correcting line is invisible to the check, and no AC catches the stale clause.
- **Classification:** drift
- **Classification rationale:** sources R3-F3, R1-F1; base-modified: R3-F3 remedy replaced per C7 (V1 R1-F1 refs/return-contract.md point incorporated; test-pin claim at 837-844 removed); class drift per X-002.
- **Default remediation:** Correct the workflow.md:72 clause and add src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md to Task 17's coherence check. The fix must reach the line `_artifacts_clause` reads: widen the ADDITIVE exemption for workflow.md to two deleted lines, or scope the clause check (owner's choice, M-17). The test lines 837-844 pin tokens, not the path, and need no change.

### Deviation D-07: Task 8 (release-split) does not cover Part 4's nested sc:analyze call

- **Merged id / severity:** M-07 / P2
- **Location:** src/superclaude/skills/sc-release-split-protocol/SKILL.md:324
- **Mapped tasklist item:** Task 8
- **Evidence:** src/superclaude/skills/sc-release-split-protocol/SKILL.md:324; src/superclaude/skills/sc-release-split-protocol/SKILL.md:149; src/superclaude/skills/sc-release-split-protocol/SKILL.md:190; plan:179; tests/skills/test_worker_contract.py:509-517
- **Claim:** Task 8 handles the brainstorm and adversarial calls but not Part 4's "Invoke appropriate analysis (Skill `sc:analyze` or inline verification)"; under --unattended a nested analyze would run with no flag and no nested directory.
- **Classification:** drift
- **Classification rationale:** sources R3-F4, INV-005; base-modified: INV-005 (LOW) folded into suggested_fix per C16.
- **Default remediation:** State that Part 4 uses inline verification under --unattended, or nest analyze with `nested/analyze-<n>/` and add it to EXPECTED_NESTING (M-13). If the inline branch leaves the nested list empty, the section text must not contain the `nested/` token (test:516-517 asserts its absence), so the inline wording must not mention `nested/analyze-`.

### Deviation D-08: Task 15 (reflect) does not settle Wave 1B's optional tech-research call

- **Merged id / severity:** M-08 / P2
- **Location:** src/superclaude/skills/sc-reflect-protocol/SKILL.md:632
- **Mapped tasklist item:** Task 15
- **Evidence:** src/superclaude/skills/sc-reflect-protocol/SKILL.md:632; src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:190; plan:26; tests/skills/test_worker_contract.py:509-517
- **Claim:** Task 15 does not cover Wave 1B's optional `tech-research` call (`--depth deep` only); tech-research has no Unattended mode, the same case as brainstorm's research-deep arm, which the plan settles but this one it does not.
- **Classification:** drift
- **Classification rationale:** sources R3-F5, INV-005; base-modified: INV-005 (LOW) folded into suggested_fix per C16.
- **Default remediation:** In Task 15, "Under --unattended, the Wave 1B tech-research step is skipped and recorded", with an exact-phrase assertion; cite D-P2-1. Keep the `nested/` token out of the skip wording when reflect's nested list has no entry for it (test:516-517).

### Deviation D-09: "left out (WC-4)" is pinned for 2 of the 15 P2 commands

- **Merged id / severity:** M-09 / P2
- **Location:** .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:7
- **Mapped tasklist item:** plan-wide
- **Evidence:** .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:7; plan:97; plan:110; plan:123; plan:248; plan:261; .dev/reflect/pre-TASK-WF-writeTheP2Static-20261107-011441-20261107013500/artifacts/coverage-matrix.yaml:14
- **Claim:** source.md:7 asks each P2 command's `artifacts` clause to point at WC-4 ("left out (WC-4)"). Only plan:97 and plan:110 (cleanup, improve) pin the phrase; research, cli-eval and tdd describe exclusions without it (plan:123, plan:248, plan:261) and the rest say nothing. The coverage matrix overstates the pinned count (real count 2). No task assigns the short local sentence for reports that name where excluded files went.
- **Classification:** drift
- **Classification rationale:** sources R3-F11, R2-F3; base-modified: R3-F11 body replaced per C5 with V2 R2-F3 scope (all 15 commands, real pinned count 2); parametrized-test shape kept.
- **Default remediation:** One parametrized test over all 15 P2 commands: the text after the first backticked `artifacts` contains "left out (WC-4)" wherever the command can write ignored files, and never contains "git add". Assign the conditional report sentence explicitly and correct the matrix's test-coverage claim.

### Deviation D-10: Gate assertions pin labels, not condition-to-outcome resolutions

- **Merged id / severity:** M-10 / P2
- **Location:** .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:14
- **Mapped tasklist item:** Task 20, Task 13, Task 5, Task 16
- **Evidence:** .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:14; .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:16; plan:97; plan:136; plan:179; plan:248; plan:290; plan:345; tests/skills/test_worker_contract.py:509-512
- **Claim:** Task 20 derives gate-resolution assertions from the entries Tasks 2-16 add, but those entries often carry only labels: cleanup pins "Approval Required" and "not applied" separately, and release-split pins "blocked_question" without tying it to either blocked gate. `_check_unattended_section` checks presence only (test_worker_contract.py:509-512), so [INFERRED] reversing a resolution while keeping the labels passes. Per-gate gaps: Task 13 has no phrase for the safety-flag gate; Task 5 none for the improve gate beyond `improved-spec.md`; Task 16 none for the two Stage 10.5 HALT gates beyond the shared `blocked_question`.
- **Classification:** drift
- **Classification rationale:** sources R2-F2, R1-F10; incorporated: V2 R2-F2 per Change C2, with V1 R1-F10 per-gate inventory (Tasks 5, 13, 16).
- **Default remediation:** Give each gate its own exact phrase joining its condition to its outcome, scoped to the line that carries the rule. Add negative cases that reverse or remove the outcome while keeping the gate label, not only cases that delete labels.

### Deviation D-11: Task 14 leaves the rest of task-builder's CLI-mode reflect gate undefined under --unattended

- **Merged id / severity:** M-11 / P2
- **Location:** plan:261
- **Mapped tasklist item:** Task 14
- **Evidence:** plan:261; plan:276; .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:77; .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:150; src/superclaude/skills/task-builder/SKILL.md:2237; src/superclaude/skills/task-builder/SKILL.md:2239; tests/skills/test_worker_contract.py:2044-2052 ([INFERRED] exact gate text)
- **Claim:** Task 14 (tdd) says in task-builder/SKILL.md that "the CLI-mode reflect gate's staging step is not run", but not what happens to the rest of the gate at task-builder SKILL.md:2237. Its `git add -A` half is refused by WC-9 (spec:77). The `superclaude reflect run --fix --promote` half is a conditional integration question, partly covered by the plan's `--no-promote` brief row (plan:276); it is not an outward action. The gate writes its output at SKILL.md:2239.
- **Classification:** drift
- **Classification rationale:** sources R1-F3; incorporated: V1 R1-F3 per Change C3, corrected per Round 2 advocates 2 and 3 (`--fix --promote` is not an outward action).
- **Default remediation:** In Task 14, state whether the whole CLI-mode gate is skipped under --unattended or only its staging step (M-18), where its output goes, and add a phrase for it to the tdd entry.

### Deviation D-12: INV-003: the diagnosability handoff reads its return contract from a path a nested workflow does not write

- **Merged id / severity:** M-12 / P2 / owner decision
- **Location:** src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md:245,250,252
- **Mapped tasklist item:** Task 11
- **Evidence:** src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md:245,250,252; src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:645; .dev/reflect/pre-TASK-WF-writeTheP2Static-20261107-011441-20261107013500/adversarial/rounds/round2-advocate-3.md:34; plan:220
- **Claim:** Step 3 of the diagnosability handoff reads `.dev/tasks/to-do/<id>/return-contract.yaml`, but a nested unattended workflow writes its contract to `<report-dir>/nested/workflow-<n>/`. Adding `workflow` to troubleshoot's nested list (M-04, nest branch) is incomplete without changing that read path; each branch changes Task 11's text and the troubleshoot EXPECTED_NESTING differently.
- **Classification:** drift
- **Classification rationale:** sources INV-003; incorporated: invariant-probe INV-003 per Change C16 (linked to M-04).
- **Default remediation:** If M-04 takes the nest branch, Task 11 changes the step 3 read path to the nested workflow's contract under `<report-dir>/nested/workflow-<n>/`; the refuse branch needs no path change.

### Deviation D-13: INV-004: UNATTENDED_EXPECT nested lists in Tasks 8, 11 and 16 must equal the Task 20 literal

- **Merged id / severity:** M-13 / P2
- **Location:** plan:339-349
- **Mapped tasklist item:** Task 20, Task 12
- **Evidence:** plan:339-349; plan:79; plan:290; .dev/reflect/pre-TASK-WF-writeTheP2Static-20261107-011441-20261107013500/adversarial/rounds/round2-advocate-3.md:36; tests/skills/test_worker_contract.py:509-517
- **Claim:** Every accepted nesting fix edits the Task 20 EXPECTED_NESTING literal: tasklist -> [reflect, task]; troubleshoot -> [adversarial, workflow] (if nested, not refused); release-split -> + analyze (only if nested, not inline). The UNATTENDED_EXPECT `nested` lists in Tasks 8, 11 and 16 must equal the literal, or `test_nested_lists_match_the_p2_nesting` fails. The consensus states this only for tasklist. Task 20's 9 keys, `len(expect)==31` and Task 12's ">= 6 `--unattended` lines" are unaffected.
- **Classification:** drift
- **Classification rationale:** sources INV-004; incorporated: invariant-probe INV-004 per Change C16 (linked to M-01, M-04).
- **Default remediation:** When M-01, M-04 and M-07 are fixed, update the Task 8, 11 and 16 nested lists and the Task 20 literal together, in the same edit set.

### Deviation D-14: INV-009: no AC pins --report-dir and the retained --compliance strict on the nested task call

- **Merged id / severity:** M-14 / P2
- **Location:** plan:233
- **Mapped tasklist item:** Task 16
- **Evidence:** plan:233; plan:288; .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:58; .dev/reflect/pre-TASK-WF-writeTheP2Static-20261107-011441-20261107013500/adversarial/variant-3-original.md:25-26; src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1539-1542
- **Claim:** Task's report directory is `--report-dir` only (plan:233), while tasklist's own may be `--output` (Task 16). The M-01 fix must pass `--report-dir <report-dir>/nested/task-<n>/` and keep `--compliance strict`; spec:58 refuses a call that passes neither or both. The consensus fix text says `--report-dir`, but no AC pins it or the retained `--compliance strict`.
- **Classification:** drift
- **Classification rationale:** sources INV-009; incorporated: invariant-probe INV-009 per Change C16 (linked to M-01).
- **Default remediation:** Add a Task 16 AC with exact-phrase assertions that the Stage 9 call passes `--report-dir <report-dir>/nested/task-<n>/` and keeps `--compliance strict`.

### Deviation D-15: INV-011: cli-eval's spec-panel and document are command-only, and the agent route yields no nested directory

- **Merged id / severity:** M-15 / P2
- **Location:** src/superclaude/skills/sc-cli-eval-protocol/refs/integration-map.md:8-10
- **Mapped tasklist item:** plan-wide
- **Evidence:** src/superclaude/skills/sc-cli-eval-protocol/refs/integration-map.md:8-10; src/superclaude/skills/sc-cli-eval-protocol/refs/create-pipeline.md:57; .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:62; plan:242-253
- **Claim:** integration-map.md:8-10 says spec-panel and document are "command-only", invoked not via the Skill tool, while spec:62 scopes the nested rule to "the Skill tool or the Agent tool". create-pipeline.md:57 allows "the technical-writer agent" instead of /sc:document, which yields no `nested/document-<n>/` and no nested contract. EXPECTED_NESTING lists document unconditionally.
- **Classification:** drift
- **Classification rationale:** sources INV-011; incorporated: invariant-probe INV-011 per Change C16.
- **Default remediation:** Task 13 fixes the route (run spec-panel and document as commands with --unattended) or records the technical-writer agent path as a skip.

### Deviation D-16: INV-016: Task 12's report_path is undefined for a non-TFEP run

- **Merged id / severity:** M-16 / P2
- **Location:** plan:233
- **Mapped tasklist item:** Task 12
- **Evidence:** plan:233; .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:72
- **Claim:** Task 12 defines `report_path` as "the task summary the run produces", which no tier names for a non-TFEP run; a nested task under tasklist must hand a concrete path to the caller's `artifacts`.
- **Classification:** drift
- **Classification rationale:** sources INV-016; incorporated: invariant-probe INV-016 per Change C16.
- **Default remediation:** Task 12 names the concrete file each tier writes as `report_path` for a non-TFEP run.

### Deviation D-17: INV-017: the workflow.md:72 fix must widen the ADDITIVE exemption or scope the clause check

- **Merged id / severity:** M-17 / P2 / owner decision
- **Location:** tests/skills/test_worker_contract.py:770-775
- **Mapped tasklist item:** plan-wide
- **Evidence:** tests/skills/test_worker_contract.py:770-775; src/superclaude/commands/workflow.md:72; plan:41; plan:303; .dev/reflect/pre-TASK-WF-writeTheP2Static-20261107-011441-20261107013500/adversarial/rounds/round2-advocate-3.md:37
- **Claim:** Only two forms reach the line `_artifacts_clause` reads: widen the ADDITIVE exemption to a second deleted line (workflow.md:72), or scope the clause check. An added sentence after line 72 is invisible because `_artifacts_clause` reads the first matching line. The consensus states the constraint but picks no form, and A-002 QUALIFY leaves the cap change to the owner.
- **Classification:** drift
- **Classification rationale:** sources INV-017, A-002; incorporated: invariant-probe INV-017 per Change C16 (linked to M-06).
- **Default remediation:** The owner picks one form (two-line exemption for workflow.md, or a scoped clause check) and Task 17 records it.

### Deviation D-18: INV-018: task-builder CLI-mode gate scope (whole run vs staging only) is undecided

- **Merged id / severity:** M-18 / P2
- **Location:** src/superclaude/skills/task-builder/SKILL.md:43,59,2237
- **Mapped tasklist item:** plan-wide
- **Evidence:** src/superclaude/skills/task-builder/SKILL.md:43,59,2237; plan:261; .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:77; .dev/reflect/pre-TASK-WF-writeTheP2Static-20261107-011441-20261107013500/adversarial/rounds/round2-advocate-3.md:25,67
- **Claim:** The M-11 graft records the gap only: the `git add -A` half is refused by WC-9 (spec:77), but whether the whole gate is skipped or only its staging step, and what `--fix --promote` does, is undecided. Conditional on CLI_MODE (default false).
- **Classification:** drift
- **Classification rationale:** sources INV-018; incorporated: invariant-probe INV-018 per Change C16 (linked to M-11).
- **Default remediation:** Task 14 states the gate's scope under --unattended and what `--fix --promote` does, with a phrase in the tdd entry.

### Deviation D-19: brainstorm's tasklist-handoff skip reason becomes false after P2

- **Merged id / severity:** M-19 / P3
- **Location:** src/superclaude/commands/brainstorm.md:156-158
- **Mapped tasklist item:** Task 18
- **Evidence:** src/superclaude/commands/brainstorm.md:156-158; src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:349-352; src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:352; plan:41
- **Claim:** brainstorm.md:158 and sc-brainstorm-protocol/SKILL.md:352 say the handoff is skipped because its skill does "not accept the flag at this phase"; after P2 that reason is false for the tasklist handoff. (The task handoff calls `task-builder`, not `/sc:task`, SKILL.md:349-352, so it is not affected.) ADDITIVE allows only one deleted line in brainstorm.md, which Task 18 spends.
- **Classification:** drift
- **Classification rationale:** sources R3-F6; base-modified: narrowed to the tasklist handoff per B3.
- **Default remediation:** Record it as an open item in the Task 21 report, or add a line giving the post-P2 reason for the tasklist handoff.

### Deviation D-20: Task 3's "Same edits" for improve has no anchor for cleanup's Safety Threshold clause

- **Merged id / severity:** M-20 / P3
- **Location:** src/superclaude/commands/cleanup.md:107-127
- **Mapped tasklist item:** Task 3
- **Evidence:** src/superclaude/commands/cleanup.md:107-127; src/superclaude/commands/improve.md:117; src/superclaude/commands/improve.md:125; plan:46; plan:110
- **Claim:** Task 3 says improve gets the "Same edits" as cleanup, but cleanup's Safety Threshold clause (plan:46) has no counterpart in improve (Approval Required at :117, Explicitly Will NOT at :125); the executor has no anchor for that copied edit.
- **Classification:** drift
- **Classification rationale:** sources R3-F7; base-modified: narrowed to the Safety Threshold clause per B4.
- **Default remediation:** Name improve's own anchor for the Safety Threshold edit in Task 3.

### Deviation D-21: Task 12's edit to the task.md:44 flag-list line fails Check ADDITIVE

- **Merged id / severity:** M-21 / P3
- **Location:** src/superclaude/commands/task.md:44-48
- **Mapped tasklist item:** Task 12
- **Evidence:** src/superclaude/commands/task.md:44-48; plan:233; plan:41
- **Claim:** Task 12 says to add the flag "to the flag list line" (task.md:44, "Key flags:") but also "new lines only"; changing line 44 deletes a line and fails Check ADDITIVE.
- **Classification:** drift
- **Classification rationale:** sources R3-F8; base
- **Default remediation:** Say "add a new row to the flag table (lines 46-48)"; do not edit line 44.

### Deviation D-22: Plan instructions collide with its own ADDITIVE and WRITE_VERB_CLASSIFICATION checks

- **Merged id / severity:** M-22 / P3
- **Location:** plan:207
- **Mapped tasklist item:** Task 17
- **Evidence:** plan:207; plan:261; plan:276; plan:41; plan:303; tests/skills/test_worker_contract.py:1166
- **Claim:** Beside M-21: Task 17's edit runs against workflow.md's one-line deletion budget (M-06), and Tasks 10, 14 and 15 say "added sentence" at lines classified in WRITE_VERB_CLASSIFICATION, whose keys are exact line text; appending a sentence to such a line changes its key and breaks the stale-entry test.
- **Classification:** drift
- **Classification rationale:** sources R1-F8, R3-F8; incorporated: V1 R1-F8 wording, inserted beside base R3-F8 (M-21) per Change C11.
- **Default remediation:** Replace "added sentence" with "new line after the classified line" in Tasks 10, 14 and 15; add an AC that the classified keys are unchanged apart from the reason text.

### Deviation D-23: cleanup and improve declare no Write under Tool Coordination though their Unattended report writes a file

- **Merged id / severity:** M-23 / P3
- **Location:** src/superclaude/commands/cleanup.md:49
- **Mapped tasklist item:** plan-wide
- **Evidence:** src/superclaude/commands/cleanup.md:49; src/superclaude/commands/improve.md:49; tests/skills/test_worker_contract.py:847
- **Claim:** cleanup and improve list only Edit/MultiEdit under Tool Coordination; their Unattended report writes a file, and P1 pinned that kind of Write for explain. The plan adds no matching assertion.
- **Classification:** drift
- **Classification rationale:** sources R3-F9; base
- **Default remediation:** Add a Write line and a test like test_explain_declares_write_under_tool_coordination, or record why not.

### Deviation D-24: Task 1's format baseline omits a file Task 6 edits

- **Merged id / severity:** M-24 / P3
- **Location:** plan:73
- **Mapped tasklist item:** Task 1, Task 6
- **Evidence:** plan:73; plan:149
- **Claim:** The Task 1 format baseline omits tests/skills/test_sc_recommend_routing_contract.py, which Task 6 edits.
- **Classification:** drift
- **Classification rationale:** sources R3-F10; base
- **Default remediation:** Add that file to the baseline list.

### Deviation D-25: D-P2-1 does not say which output path brainstorm reads for the research-light arm

- **Merged id / severity:** M-25 / P3
- **Location:** src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:189
- **Mapped tasklist item:** plan-wide
- **Evidence:** src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:189; src/superclaude/commands/research.md:103
- **Claim:** [INFERRED] For the D-P2-1 research-light arm, brainstorm's enrichment table expects enrichment/research-light.md but /sc:research writes claudedocs/research_[topic]_[timestamp].md; the plan does not say which path brainstorm reads.
- **Classification:** drift
- **Classification rationale:** sources R3-F12; base-modified: second half (skill name) dropped per B6, already covered by D-P2-1.
- **Default remediation:** State the output path in D-P2-1.

### Deviation D-26: Task 21's exact path list omits the staged .dev/tasks package

- **Merged id / severity:** M-26 / P3
- **Location:** .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:16
- **Mapped tasklist item:** Task 21
- **Evidence:** .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:16; plan:367; plan:371; plan:372
- **Claim:** Task 21's acceptance criterion restricts the report's exact path list to src, tests and plugins (plan:372), while the same task stages the package's report and evidence under .dev/tasks, so those staged deliverables are excluded from the asserted list and the complete commit-path list the brief asks for cannot be delivered.
- **Classification:** drift
- **Classification rationale:** sources R2-F4, R3-F13; incorporated: V2 R2-F4 per Change C6, replacing base R3-F13 (after B2: the `.dev/reflect` dirty-folder example deleted).
- **Default remediation:** Compare the full commit manifest, including the task package and its artifacts, in the equality check; distinguish pre-existing unrelated changes from paths this plan produces.

### Deviation D-27: "drop the equality case" has no target under the subset rule

- **Merged id / severity:** M-27 / P3
- **Location:** tests/skills/test_worker_contract.py:898-903
- **Mapped tasklist item:** plan-wide
- **Evidence:** tests/skills/test_worker_contract.py:898-903; tests/skills/test_worker_contract.py:1001-1012
- **Claim:** Confirms T1-F2; under the subset rule every existing case still fails, so "drop the equality case" has no target.
- **Classification:** drift
- **Classification rationale:** sources R3-F14; base
- **Default remediation:** Remove the instruction.

### Deviation D-28: spec-panel --mode socratic "not wait" is an unlisted decision

- **Merged id / severity:** M-28 / P3 / owner decision
- **Location:** plan:136
- **Mapped tasklist item:** Task 5
- **Evidence:** plan:136; .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:162; .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:180; src/superclaude/commands/spec-panel.md:123-125
- **Claim:** Task 5 makes spec-panel `--mode socratic` write its questions into the report and "not wait"; the spec row is silent. The P1 precedent for business-panel refused `--mode socratic` because whether it waits was UNVERIFIED. D-P2-10 does not record this decision.
- **Classification:** drift
- **Classification rationale:** sources R1-F4; incorporated: V1 R1-F4 per Change C4.
- **Default remediation:** Record the socratic decision for owner approval; either refuse it as business-panel does or verify the mode does not wait.

### Deviation D-29: Task 16 does not say where depth-map.yaml goes under --unattended

- **Merged id / severity:** M-29 / P3
- **Location:** plan:290
- **Mapped tasklist item:** Task 16
- **Evidence:** plan:290; src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1631; src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1641
- **Claim:** Task 16 moves the Stage 10.5 phase outputs, but `depth-map.yaml` stays at `TASKLIST_ROOT/validation/reflect-pre/` (SKILL.md:1641) and the plan does not mention it.
- **Classification:** drift
- **Classification rationale:** sources R1-F6; incorporated: V1 R1-F6 per Change C8, narrowed to the depth-map.yaml part (D-P2-13 reading dropped).
- **Default remediation:** State where `depth-map.yaml` goes under --unattended.

### Deviation D-30: Task 16 has no grep AC for remaining readers of the old reflect-pre folder

- **Merged id / severity:** M-30 / P3
- **Location:** tests/tasklist/test_tasklist_cli.py:571-579
- **Mapped tasklist item:** Task 16
- **Evidence:** tests/tasklist/test_tasklist_cli.py:571-579; src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1628
- **Claim:** T1-F4 (readers of `reflect-pre`) resolves: src has one hit (the tasklist SKILL.md) and tests only comments and a string in tests/tasklist/test_tasklist_cli.py:571-579, so no code consumer reads the old folder; but no AC keeps it that way.
- **Classification:** drift
- **Classification rationale:** sources R1-F7; incorporated: V1 R1-F7 per Change C9, bounded to a grep acceptance criterion.
- **Default remediation:** Add the `reflect-pre` grep over src and tests to Task 16's ACs.

### Deviation D-31: D-P2-1 skips the research-deep arm; a /sc:research --depth deep alternative exists

- **Merged id / severity:** M-31 / P3 / owner decision
- **Location:** plan:317
- **Mapped tasklist item:** Task 18
- **Evidence:** plan:317; .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:142; .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:176; src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:189-195
- **Claim:** Task 18 skips research-deep (D-P2-1); the spec row says automatic enrichment "passes --unattended and a nested report directory" with no skipped arm, and an explicit `--research deep` is also skipped. The skip complies with the nested rule, but an alternative exists (map the deep arm to `/sc:research --depth deep --unattended`) that the owner should see. The light arm's `--strategy planning` is redundant with the research row's pin.
- **Classification:** necessary
- **Classification rationale:** sources R1-F5; incorporated: V1 R1-F5 per Change C12 (Necessary deviation, kept as an alternative only; Changes NOT Made row U-003).
- **Default remediation:** Keep D-P2-1; list the `/sc:research --depth deep` alternative as an owner choice (an alternative, not a requirement) and note that the explicit flag is overridden.

## Inferred-claim audit

- `citations_inferred: 3`
- Inferred-fraction: `3 / 184` = 0.02

## Recommendations

### Recommendation R-01: Fix M-01 before running /sc:implement

- **File:** .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md
- **Change:** In Task 16, make every Stage 9 sc:task call (loop-backs included) pass `--unattended --report-dir <report-dir>/nested/task-<n>/` and keep `--compliance strict` (M-14). Place `--unattended` as a standalone token outside the quoted input string, since the switch fires only on a standalone token (plan:25; INV-010). Add "task" to the tasklist `UNATTENDED_EXPECT` nested list and to the Task 20 `EXPECTED_NESTING` literal (plan:79, plan:290; M-13), add "Depends on: Task 12", and record it as a decision or spec observation (spec row 182 names only Stage 10.5).
- **Verifier:** re-run the sc:workflow gate on the edited plan and re-run `/sc:reflect --mode pre` on it; the finding's evidence lines no longer show the gap.
- **Linked deviation(s):** D-01
- **Priority:** P0

### Recommendation R-02: Fix M-02 before running /sc:implement

- **File:** .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md
- **Change:** In Task 13, block a `run` whose brief lacks the safety flags, and add two separate assertions: `run` with no `--suite` resolves blocked; `run` whose brief lacks the safety flags resolves blocked. The flag subset is nameable from sc-cli-eval-protocol/SKILL.md:128-153, with the eval-docs-loader digest authoritative (SKILL.md:30-33,46-58). Which subset is the owner's choice; until it is named, carry the section as blocked-pending-decision (M-03).
- **Verifier:** re-run the sc:workflow gate on the edited plan and re-run `/sc:reflect --mode pre` on it; the finding's evidence lines no longer show the gap.
- **Linked deviation(s):** D-02
- **Priority:** P0

### Recommendation R-03: Fix M-03 before running /sc:implement

- **File:** .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md
- **Change:** The owner names the safety-flag subset in the plan (from sc-cli-eval-protocol/SKILL.md:128-153), or the plan carries the cli-eval section as blocked-pending-decision. Blocking until resolved.
- **Verifier:** re-run the sc:workflow gate on the edited plan and re-run `/sc:reflect --mode pre` on it; the finding's evidence lines no longer show the gap.
- **Linked deviation(s):** D-03
- **Priority:** P0

### Recommendation R-04: Fix M-04 before running /sc:implement

- **File:** .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md
- **Change:** Owner choice between two branches. Nest: Task 11 adds `workflow` to troubleshoot's nested list and to the Task 20 `EXPECTED_NESTING` literal (M-13) and changes the handoff's return-contract read path (M-12). Refuse: the troubleshoot Unattended section refuses `--diagnosability-handoff` under --unattended, with an exact-phrase assertion.
- **Verifier:** re-run the sc:workflow gate on the edited plan and re-run `/sc:reflect --mode pre` on it; the finding's evidence lines no longer show the gap.
- **Linked deviation(s):** D-04
- **Priority:** P0

### Recommendation R-05: Fix M-05 before running /sc:implement

- **File:** .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md
- **Change:** Add a plan rule, with an AC, defining how a nested `blocked` or `failed` status reaches the outer return contract (the caller's worker_status and `blocked_question`), covering sc-task Step 4 and tasklist Stage 9. Blocking until resolved.
- **Verifier:** re-run the sc:workflow gate on the edited plan and re-run `/sc:reflect --mode pre` on it; the finding's evidence lines no longer show the gap.
- **Linked deviation(s):** D-05
- **Priority:** P0

### Recommendation R-06: Fix M-06 before running /sc:implement

- **File:** .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md
- **Change:** Correct the workflow.md:72 clause and add src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md to Task 17's coherence check. The fix must reach the line `_artifacts_clause` reads: widen the ADDITIVE exemption for workflow.md to two deleted lines, or scope the clause check (owner's choice, M-17). The test lines 837-844 pin tokens, not the path, and need no change.
- **Verifier:** re-run the sc:workflow gate on the edited plan and re-run `/sc:reflect --mode pre` on it; the finding's evidence lines no longer show the gap.
- **Linked deviation(s):** D-06
- **Priority:** P1

### Recommendation R-07: Fix M-07 before running /sc:implement

- **File:** .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md
- **Change:** State that Part 4 uses inline verification under --unattended, or nest analyze with `nested/analyze-<n>/` and add it to EXPECTED_NESTING (M-13). If the inline branch leaves the nested list empty, the section text must not contain the `nested/` token (test:516-517 asserts its absence), so the inline wording must not mention `nested/analyze-`.
- **Verifier:** re-run the sc:workflow gate on the edited plan and re-run `/sc:reflect --mode pre` on it; the finding's evidence lines no longer show the gap.
- **Linked deviation(s):** D-07
- **Priority:** P1

### Recommendation R-08: Fix M-08 before running /sc:implement

- **File:** .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md
- **Change:** In Task 15, "Under --unattended, the Wave 1B tech-research step is skipped and recorded", with an exact-phrase assertion; cite D-P2-1. Keep the `nested/` token out of the skip wording when reflect's nested list has no entry for it (test:516-517).
- **Verifier:** re-run the sc:workflow gate on the edited plan and re-run `/sc:reflect --mode pre` on it; the finding's evidence lines no longer show the gap.
- **Linked deviation(s):** D-08
- **Priority:** P1

### Recommendation R-09: Fix M-09 before running /sc:implement

- **File:** .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md
- **Change:** One parametrized test over all 15 P2 commands: the text after the first backticked `artifacts` contains "left out (WC-4)" wherever the command can write ignored files, and never contains "git add". Assign the conditional report sentence explicitly and correct the matrix's test-coverage claim.
- **Verifier:** re-run the sc:workflow gate on the edited plan and re-run `/sc:reflect --mode pre` on it; the finding's evidence lines no longer show the gap.
- **Linked deviation(s):** D-09
- **Priority:** P1

### Recommendation R-10: Fix M-10 before running /sc:implement

- **File:** .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md
- **Change:** Give each gate its own exact phrase joining its condition to its outcome, scoped to the line that carries the rule. Add negative cases that reverse or remove the outcome while keeping the gate label, not only cases that delete labels.
- **Verifier:** re-run the sc:workflow gate on the edited plan and re-run `/sc:reflect --mode pre` on it; the finding's evidence lines no longer show the gap.
- **Linked deviation(s):** D-10
- **Priority:** P1

### Recommendation R-11: Fix M-11 before running /sc:implement

- **File:** .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md
- **Change:** In Task 14, state whether the whole CLI-mode gate is skipped under --unattended or only its staging step (M-18), where its output goes, and add a phrase for it to the tdd entry.
- **Verifier:** re-run the sc:workflow gate on the edited plan and re-run `/sc:reflect --mode pre` on it; the finding's evidence lines no longer show the gap.
- **Linked deviation(s):** D-11
- **Priority:** P1

### Recommendation R-12: Fix M-12 before running /sc:implement

- **File:** .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md
- **Change:** If M-04 takes the nest branch, Task 11 changes the step 3 read path to the nested workflow's contract under `<report-dir>/nested/workflow-<n>/`; the refuse branch needs no path change.
- **Verifier:** re-run the sc:workflow gate on the edited plan and re-run `/sc:reflect --mode pre` on it; the finding's evidence lines no longer show the gap.
- **Linked deviation(s):** D-12
- **Priority:** P1

### Recommendation R-13: Fix M-13 before running /sc:implement

- **File:** .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md
- **Change:** When M-01, M-04 and M-07 are fixed, update the Task 8, 11 and 16 nested lists and the Task 20 literal together, in the same edit set.
- **Verifier:** re-run the sc:workflow gate on the edited plan and re-run `/sc:reflect --mode pre` on it; the finding's evidence lines no longer show the gap.
- **Linked deviation(s):** D-13
- **Priority:** P1

### Recommendation R-14: Fix M-14 before running /sc:implement

- **File:** .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md
- **Change:** Add a Task 16 AC with exact-phrase assertions that the Stage 9 call passes `--report-dir <report-dir>/nested/task-<n>/` and keeps `--compliance strict`.
- **Verifier:** re-run the sc:workflow gate on the edited plan and re-run `/sc:reflect --mode pre` on it; the finding's evidence lines no longer show the gap.
- **Linked deviation(s):** D-14
- **Priority:** P1

### Recommendation R-15: Fix M-15 before running /sc:implement

- **File:** .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md
- **Change:** Task 13 fixes the route (run spec-panel and document as commands with --unattended) or records the technical-writer agent path as a skip.
- **Verifier:** re-run the sc:workflow gate on the edited plan and re-run `/sc:reflect --mode pre` on it; the finding's evidence lines no longer show the gap.
- **Linked deviation(s):** D-15
- **Priority:** P1

### Recommendation R-16: Fix M-16 before running /sc:implement

- **File:** .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md
- **Change:** Task 12 names the concrete file each tier writes as `report_path` for a non-TFEP run.
- **Verifier:** re-run the sc:workflow gate on the edited plan and re-run `/sc:reflect --mode pre` on it; the finding's evidence lines no longer show the gap.
- **Linked deviation(s):** D-16
- **Priority:** P1

### Recommendation R-17: Fix M-17 before running /sc:implement

- **File:** .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md
- **Change:** The owner picks one form (two-line exemption for workflow.md, or a scoped clause check) and Task 17 records it.
- **Verifier:** re-run the sc:workflow gate on the edited plan and re-run `/sc:reflect --mode pre` on it; the finding's evidence lines no longer show the gap.
- **Linked deviation(s):** D-17
- **Priority:** P1

### Recommendation R-18: Fix M-18 before running /sc:implement

- **File:** .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md
- **Change:** Task 14 states the gate's scope under --unattended and what `--fix --promote` does, with a phrase in the tdd entry.
- **Verifier:** re-run the sc:workflow gate on the edited plan and re-run `/sc:reflect --mode pre` on it; the finding's evidence lines no longer show the gap.
- **Linked deviation(s):** D-18
- **Priority:** P1

P3 findings (D-19 to D-31) are recorded above and need no separate recommendation; fold them into the same plan edit.

