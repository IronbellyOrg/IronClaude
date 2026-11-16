persona: analyzer
model_class: sonnet
model: claude-gw-tier1b[1m]
agent_type: reflect-reviewer

# Reviewer 1 (analyzer): pre-execution review of the stage 2 plan

I found 3 blocking and 5 minor findings. All four T1 leads reproduce. Each finding says whether an executor following the plan literally could still get it right.

**R1-1 (blocking). Nothing the task skill can call exists for the sweep or the follow-up writer.**
- PLAN:33 creates `sweep.py` as a function only. PLAN:50 tells the skill to write the ledger "through the follow-up writer", make "the one sweep call", and run the safety route.
- S1:110 builds `follow_ups.py` as a module with no command. S1:167 adds only the `classify` command.
- SKILL.md is prose that an agent follows, so the executor writes sentences that name nothing runnable. Live runs then record no ledger, and stage 2 yields no shadow data.
- A literal executor can pass every acceptance line and still deliver this.
- Smallest fix: Task 1 adds a `review sweep` command, and Task 2 names the exact commands for the writer, safety route, sweep and classify. The Task 2 acceptance greps for them.

**R1-2 (blocking). Task 2 never handles `--unattended`.**
- PLAN:50 puts "the end-of-run offer is shown with the halt message" at all three cap sentences, and the end-of-run offer in Post-Completion.
- SKILL.md:55 makes those halts return the findings to the caller. WORKER-CONTRACT.md:31 (WC-2) forbids chat offers. PSPEC:169 says an unattended run records the row and does not wait, and PSPEC:375 gives the offer state `unattended`.
- A literal executor writes an unconditional offer, which contradicts WC-2.
- The Task 4 test at PLAN:79 only checks contract text.
- `test_task_skill_returns_the_qa_halt_to_an_unattended_caller` (`test_worker_contract.py:1715`) pins the paragraph that begins "The same applies to the two other" in the skill, so it must stay green.
- No task makes `/task` return the three new keys to its caller.
- Smallest fix: add "attended runs only; under `--unattended` record the row and return ledger path, counts and capture state to the caller" to each offer site. Pin that wording in a Task 2 acceptance line.

**R1-3 (blocking). The safety-miss count cannot be computed from the ledgers.**
- PLAN:110 reads only run folders and `follow-ups.md`.
- S0:130(a) defines a miss as a row "a later review or the owner confirms" as a risk. The ledgers hold no such confirmation.
- A literal script can only print 0, and PLAN:114 then ties the stage 3 entry to "zero safety misses". A silent 0 reaches the owner at the safety gate.
- Smallest fix: add a `--confirmed-misses <file>` input. Without it the script prints "not computable; N unreviewed rows carry safety words" and never a bare 0.

**R1-4 (minor). The judge in live shadow runs is not named.**
- PLAN:50 says only "the classifier is called in shadow mode".
- `classify` needs a judge answers file (S1:171). Live runs have none, and only `ReviewerJudge` exists (S1:136).
- Per PSPEC:586, shadow agreement is then `unavailable` or trivially the reviewer's own label. M13 (PSPEC:975) wants every shadow metric split by judge id.
- An executor can still finish, but the number would mislead.
- Smallest fix: Task 7 splits the agreement figures by judge id and prints the `unavailable` count. The owner summary says agreement is empty when only `ReviewerJudge` ran.

**R1-5 (minor). Task 6 is silent on how three agents and three replicates become judge verdicts.**
- PLAN:98 gives no rule. S1:136 takes the median of 3 replicates per judge, and PSPEC:586 says results from different judges are not compared.
- It also does not say the agents must not see the panel consensus, old grades or reviewer labels. If they do, agreement is inflated.
- Smallest fix: treat each agent as its own judge id, with the replicate rule per agent. The agents get the blind table only. Report figures per agent.

**R1-6 (minor). The stage 3 entry sentence in Task 7 is incomplete.**
- PSPEC:947 requires "zero safety misses and no capture failure".
- PLAN:114 states only the first part, so a literal executor omits the capture-failure part.
- Smallest fix: add "and no capture failure" to the acceptance line.

**R1-7 (minor). Task 6 does not say where the 318 rows' text and panel consensus come from.**
- SRC:13 also names `stage0b-sample.md`, and PLAN:98 drops it.
- The 318 rows and their consensus live in PF `04-historical/master-table.md` and `05-scoring/consensus.md` (S0:82, S0:96). The plan names neither.
- The executor must guess the input and the consensus source.
- Smallest fix: name both PF files and add `stage0b-sample.md`.

**R1-8 (minor). "The Findings Consolidation step" is ambiguous.**
- PLAN:50 uses the singular. SKILL.md has the phase-gate item at line 252, Post-Completion Step 3 at lines 338-340, and fidelity Step 4 at line 405.
- If only the phase-gate step writes the ledger, final-gate findings never reach it. The final gate is where the sweep and offer run.
- Separately, PLAN:22 omits the SRC:19 no-edit list (`rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md`, templates and others). No task edits those files, so the risk is low.
- Smallest fix: name all three consolidation points, and copy the SRC:19 list into the plan's Constraints.

## Leads dropped

None of the T1 leads is wrong. T1-2 and T1-3 are confirmed as blocking (R1-2 and R1-3). T1-4 and T1-5 are confirmed and stay minor (R1-4 and R1-5).

## Earlier review findings

- **F6:** I found no acceptance line in this package that a later task makes false. PLAN:24 supplies the "until Task N" rule.
- **F7:** Task 6 resolves it, apart from R1-5 and R1-7.
- **F8:** Only partly resolved, because of R1-3 and R1-6.

Files read, all under `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/`:
- `.dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md`
- `.dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/source.md`
- `src/superclaude/skills/task/SKILL.md`
- `tests/skills/test_worker_contract.py`
- the stage 0 and stage 1 plans and `merged-requirements.md` (the spec)


```yaml
calibration:
  calibrator_model_class: opus
  calibrated_confidence: 0.84
  dimensions: {'citation': 0.9, 'coverage': 0.65, 'classification': 0.9, 'risk': 0.85, 'actionability': 0.88}
  citation_spot_check: "27 citations checked, 26 matched; R1-2 cites PSPEC:169 but the text is at PSPEC:434 and 438"
  coverage_gap: "tasks 3 and 5 not examined"
  inline_fallback: false
```
