# D-P2-22, option A (recommended): a two-line exemption for workflow.md

`src/superclaude/commands/workflow.md` replaces exactly two P1 lines in its `## Unattended mode` section: the "Contract" bullet (line 72) and the "Nested invocations" bullet (line 75). The old "Nested invocations" line says the reflect step "runs as today, without `--unattended`"; under P2 it receives `--unattended --output <report-dir>/nested/reflect-<n>/`, so the old sentence would be false. The old "Contract" line names the `.dev/reflect/` run directory for the reflect files; with the nested directory that wording is false too. The Check ADDITIVE rule (zero deleted lines per command file) gets a named exemption for exactly these two lines of workflow.md (and one line of brainstorm.md, D-P2-1).

Evidence: `git diff HEAD -U0 -- src/superclaude/commands/workflow.md` shows 2 added and 2 deleted lines; `.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/ac-c5.txt`; the spec text "the spec's own P2 row changes them" (spec section 6 row P2 gives workflow's reflect step the flag).

Claimed strengths: the section stays true and has one rule per fact; no contradicting leftovers for a worker or reviewer to resolve.
Claimed weakness: a hand-made exception to a spec check (SA-4, additive edits); tests and reports must name it.

## How to judge (the same for every decision)

Read the cited files in the working tree (they hold uncommitted P2 edits) before arguing. Judge each option on: (1) is the command or skill text true and unambiguous when a worker runs it under `--unattended`; (2) does it respect the spec: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` section 2.1 (nested propagation: a step whose callee does not accept `--unattended` is made gate-free or skipped and recorded), WC-4 (report and contract), WC-9 (no commit, push or staging by a worker; the coordinator owns outward actions) and WC-11 (parallel-safe writes), and SA-1/SA-4 (a standalone run behaves as today; edits to command files are additive unless a named defect fix); (3) size of the change and risk to existing pinned tests (`tests/skills/test_worker_contract.py`, the Check ADDITIVE rule, the write-verb classification table); (4) what a coordinator and the owner gain or lose. End with one recommended option and the one-sentence reason.
