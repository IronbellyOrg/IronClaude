<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (original, option A) -->
<!-- Merge date: 2026-11-07 -->

<!-- Source: Base (original) -->
# D-P2-23, option A (recommended): skip the whole CLI-mode reflect gate under --unattended

<!-- Source: Base (original) -->
`src/superclaude/skills/task-builder/SKILL.md` (the paragraph added at about line 410, after the Compute-subject text) says: when the build request says the caller runs under `--unattended`, the `.dev/tasks` staging is left to the coordinator and the whole CLI-mode reflect gate (its `git add -A` staging step, its `--fix` loop and its `--promote` move) is skipped, with `reflect gate skipped (unattended)` recorded in the task log and no output file written. The gate item is the generated task's "Independent post-execution reflection gate (wrapper shell-out)" (see the `--cli` POST item near lines 2236-2244), a flat `superclaude reflect run <task> --depth deep --fix --promote`.

<!-- Source: Base (original) -->
Why skip: `--fix` auto-runs a corrective `/task` (a second executor with edits and possible commits), `--promote` moves the task folder (the coordinator owns folder moves, the same reason `/sc:reflect` has `--no-promote`), and the gate begins by staging with `git add -A` (WC-9: a worker stages nothing outside what it is told).

<!-- Source: Base (original) -->
Claimed strengths: nothing outward happens under a worker; the skip is recorded; one sentence.
Claimed weakness: the task loses its independent post-execution audit; the coordinator must run reflect itself.

<!-- Source: Variant 2 (option B), Claimed strengths - merged per Change #1 -->
Recovery: the coordinator audits the finished task itself with `/sc:reflect --mode post --no-promote` (reflect row of spec section 3.1: no `--remediate`, `--no-promote` while the coordinator owns folder moves). This is a coordinator step in the run plan, not task-builder text.

<!-- Source: Base (original, modified) - decision summary added per debate-transcript.md Scoring Matrix -->
## Decision

Winner = option A (variant 1). Convergence 83.3% (10 of 12 points). Combined score 0.844 vs 0.724.

Reason: the gate starts with the `git add -A` that WC-9 refuses, the wrapper `superclaude reflect run` has no `--unattended` so spec 2.1 sends it to the skip-and-record branch, and `tdd.md:168` plus the pinned tests already commit to skip.

<!-- Source: Debate analysis (shared assumption A-001 and orchestrator reading of spec line 62) - merged per Change #2 and Change #3 -->
## Open items

- Change #2 (build time versus run time, shared assumption A-001): `SKILL.md:410` sits in build step A.3, while the gate item (`:2237`) is a checklist item run later by `/task`. The paragraph says the gate "is skipped" and that the log records it, without saying whether the builder omits the item or emits it in skip form. The debate did not resolve this and it is not changed here (scope discipline); it is stated so the owner can decide.
- Change #3 (UNVERIFIED; task log versus contract): spec 2.1 says the caller "records the skip in its contract", while `SKILL.md:410` and `tdd.md:168` record it "in the task log". `tdd.md:166` lists "the MDTM task folder files the run wrote" in `artifacts`, so the skip is reachable from the contract only if the task log is one of those files. UNVERIFIED; not a blocker, not changed here.

<!-- Source: Base (original) -->
## How to judge (the same for every decision)

Read the cited files in the working tree (they hold uncommitted P2 edits) before arguing. Judge each option on: (1) is the command or skill text true and unambiguous when a worker runs it under `--unattended`; (2) does it respect the spec: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` section 2.1 (nested propagation: a step whose callee does not accept `--unattended` is made gate-free or skipped and recorded), WC-4 (report and contract), WC-9 (no commit, push or staging by a worker; the coordinator owns outward actions) and WC-11 (parallel-safe writes), and SA-1/SA-4 (a standalone run behaves as today; edits to command files are additive unless a named defect fix); (3) size of the change and risk to existing pinned tests (`tests/skills/test_worker_contract.py`, the Check ADDITIVE rule, the write-verb classification table); (4) what a coordinator and the owner gain or lose. End with one recommended option and the one-sentence reason.
