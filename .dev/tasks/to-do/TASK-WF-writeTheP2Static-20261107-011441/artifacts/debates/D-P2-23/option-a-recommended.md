# D-P2-23, option A (recommended): skip the whole CLI-mode reflect gate under --unattended

`src/superclaude/skills/task-builder/SKILL.md` (the paragraph added at about line 410, after the Compute-subject text) says: when the build request says the caller runs under `--unattended`, the `.dev/tasks` staging is left to the coordinator and the whole CLI-mode reflect gate (its `git add -A` staging step, its `--fix` loop and its `--promote` move) is skipped, with `reflect gate skipped (unattended)` recorded in the task log and no output file written. The gate item is the generated task's "Independent post-execution reflection gate (wrapper shell-out)" (see the `--cli` POST item near lines 2236-2244), a flat `superclaude reflect run <task> --depth deep --fix --promote`.

Why skip: `--fix` auto-runs a corrective `/task` (a second executor with edits and possible commits), `--promote` moves the task folder (the coordinator owns folder moves, the same reason `/sc:reflect` has `--no-promote`), and the gate begins by staging with `git add -A` (WC-9: a worker stages nothing outside what it is told).

Claimed strengths: nothing outward happens under a worker; the skip is recorded; one sentence.
Claimed weakness: the task loses its independent post-execution audit; the coordinator must run reflect itself.

## How to judge (the same for every decision)

Read the cited files in the working tree (they hold uncommitted P2 edits) before arguing. Judge each option on: (1) is the command or skill text true and unambiguous when a worker runs it under `--unattended`; (2) does it respect the spec: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` section 2.1 (nested propagation: a step whose callee does not accept `--unattended` is made gate-free or skipped and recorded), WC-4 (report and contract), WC-9 (no commit, push or staging by a worker; the coordinator owns outward actions) and WC-11 (parallel-safe writes), and SA-1/SA-4 (a standalone run behaves as today; edits to command files are additive unless a named defect fix); (3) size of the change and risk to existing pinned tests (`tests/skills/test_worker_contract.py`, the Check ADDITIVE rule, the write-verb classification table); (4) what a coordinator and the owner gain or lose. End with one recommended option and the one-sentence reason.
