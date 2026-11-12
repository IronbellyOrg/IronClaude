# Pairs P41 to P50 (detail version)

For each pair, read complaint A and complaint B. They come from two different reviewers of the same plan.
Question: would ONE edit to the plan (or spec) fix both complaints? If yes, they are the same problem.
Write yes or no after the colon on the line that starts with ANSWER. Do not change anything else.
If one complaint lists several problems, answer yes when one of those problems is the other's problem.

## P41

A (reviewer-1-card, finding F7): Common checks are not verified at the final state, although the Goal claims "every P0 check of section 7 passing" and the spec requires every common check to pass for the phase. AC-C1 and AC-C2 run only inside Task 4. Task 3 (possible plugin mirror) can run after Task 4 and is not re-checked. AC-...
   points at: source TASK-WF-orcaWorkerContra-20261102-231950.md:15-15 ; source TASK-WF-orcaWorkerContra-20261102-231950.md:19-19 ; source source.md:241-241 ; source source.md:216-216 ; source coverage-matrix.yaml:1407-1409

B (reviewer-2-card, finding R2-2): AC-0.6's pass condition says "7.2 step 5 follows that answer" and 7.2 step 5 (source.md:291) says that if transcripts do not name tool calls, step 5 uses --source terminal output instead and the phase report records the gap. Task 8 records the AC-0.6 yes/no (TL:122, TL:127) but never carries the ...
   points at: unresolved /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:291 ; unresolved /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:303 ; unresolved /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:122 ; unresolved /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:127 ; unresolved /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs/.dev/reflect/pre-TASK-WF-orcaWorkerContra-20261102-231950-20261102232329/artifacts/coverage-matrix.yaml:1413

ANSWER P41:

## P42

A (reviewer-1-card, finding R1-06): Task 7's exhaustion branch is answered statically: identify() reads the target's kernel session and jobs/<sid>.json, with no parent walk; F2.3/F2.6 describe the historical probe. Task 8 has no 'not applicable' state for those findings.
   points at: source launch-job-identity.sh:219-219 ; source launch-job-identity.sh:223-223 ; source launch-job-identity.sh:253-253 ; source actor-context-probe.sh:37-39 ; source review-2.md:9-9 ; source review-2.md:12-12

B (reviewer-3-card, finding R3-F2): Task 7 depends only on Task 5 but its criteria need depths from the Task 2-4 runs.
   points at: unresolved plan lines 99, 101, 104

ANSWER P42:

## P43

A (reviewer-1-card, finding R1-07): Task 5's 'helper does not compare boot identity' branch is dead (launch-job-identity.sh:234 compares both); editing the state copy risks rejecting for mode or hard-link reasons instead of the edited field.
   points at: source launch-job-identity.sh:234-234 ; source launch-job-identity.sh:83-83 ; source launch-job-identity.sh:149-149 ; source launch-job-identity.sh:218-244

B (reviewer-3-card, finding R3-F12): The twelve-run cap is not allocated and no criterion counts runs or cost; Tasks 2-4 plausibly need 9-14 runs.
   points at: unresolved plan lines 22, 44, 55, 66

ANSWER P43:

## P44

A (reviewer-1-card, finding F5): Task 4's 'keep the existing sentence that the scheduler is the owner's choice' does not say where that sentence lives.
   points at: source issue-watcher-setup.md:202-202

B (reviewer-2-card, finding QA-02): Plan weakens 'replace every guessed fixture' to 'replace whichever were captured'; Task 5 precondition (one capture per fixture, plan:108) contradicts its body (missing captures allowed, plan:110); coverage matrix row 14 overstates coverage.
   points at: spec source.md:22-22 ; plan TASK-WF-rollOutTheIssueW-20261109-000305.md:110-110 ; source coverage-matrix.md:14-14

ANSWER P44:

## P45

A (reviewer-1-card, finding R1-F3): Task 14 (tdd) says in task-builder/SKILL.md that "the CLI-mode reflect gate's staging step is not run", but not whether the gate's `superclaude reflect run --fix --promote` call itself still runs. `--fix` and `--promote` mutate and move files; the plan leaves the rest of that gate undefined under...
   points at: plan TASK-WF-writeTheP2Static-20261107-011441.md:261-261 ; spec source.md:150-150 ; source test_worker_contract.py:2044-2052

B (reviewer-3-card, finding R3-F12): [INFERRED] For the D-P2-1 research-light arm, brainstorm's enrichment table expects enrichment/research-light.md but /sc:research writes claudedocs/research_[topic]_[timestamp].md; the plan does not say which path brainstorm reads. The table also names `Skill sc-research-protocol`, which does not...
   points at: source SKILL.md:189-189 ; source research.md:103-103

ANSWER P45:

## P46

A (reviewer-1-card, finding 11): Drops the superclaude.* command form the design lists.
   points at: unresolved DESIGN:102-127 ; unresolved Task 9

B (reviewer-2-card, finding 3): Task 18 defines effective registrations as the exact command present under both events and hooks not globally disabled; a registration whose matcher excludes governed tools, or a prompt registration that cannot bind, would pass. Negative cases test missing, not present-but-ineffective, registrati...
   points at: unresolved DESIGN:342-352 ; unresolved PLAN:291

ANSWER P46:

## P47

A (reviewer-1-card, finding 13): T-REG-3 negatives do not match the AC-map module.
   points at: source merged-requirements.md:971-1108 ; unresolved Task 12

B (reviewer-2-card, finding 8): Task 16 requires panel F1-F8 regression cases but no resolvable source holds their definitions; the panel review file does not exist.
   points at: unresolved DESIGN:311; file .dev/brainstorms/20261105-170229-launch-level-hook/spec-panel-20261106/review.md is absent ; unresolved PLAN:266

ANSWER P47:

## P48

A (reviewer-1-card, finding 14): Pins non-git leaks as expected behaviour.
   points at: unresolved DESIGN:133-175 ; unresolved Task 16

B (reviewer-3-card, finding 10): Treats any skipped test as failure, but existing tests skip on non-Linux and as root.
   points at: source test_launch_job_identity.py:18-18 ; source test_freshness_subagent_start_policy.py:72-72 ; unresolved PLAN:349 (Task 22)

ANSWER P48:

## P49

A (reviewer-2-card, finding 1): Task 1 lets L1 proceed while B-CTX stays blocked; its acceptance checks the verdict document, not a stop condition; Task 2 supplies synthetic fixtures instead of completing OB-H1.
   points at: unresolved DESIGN:359-360 requires stopping enforcement implementation when the distinction cannot be established, then OB-H1 before the skeleton. Fix: make enforcement tasks conditional on the evidence, or obta ; unresolved PLAN:36

B (reviewer-3-card, finding 5): Task 19 reports a missing L2 as a status line on a launched claim; Task 20 then refuses that same case, so Task 19's tests describe a state that cannot exist after Task 20.
   points at: unresolved PLAN:305, PLAN:310, DESIGN:514 ; unresolved PLAN:301-312 vs PLAN:314-325

ANSWER P49:

## P50

A (reviewer-1-card, finding R1-F7): Task 65 hardcodes python3 -m http.server (plan addition, conflicts with UV-only rule); _fetch uses urllib urlopen with no scheme check so file:// likely works.
   points at: source CONSOLIDATED-PLAN.md:632-632 ; source models.py:255-268

B (reviewer-3-card, finding R3-F8): Markdownlint invocation differs from spec wording but matches the repo pre-commit pin (markdownlint-cli v0.38.0).
   points at: source .pre-commit-config.yaml:74-77 ; spec source.md:48-48

ANSWER P50:

