# Disposition of spec-panel findings: orca-worker-contract-spec.md

- Task: task_3cfe936a5705 (Task 6, revise the spec).
- Review: `.dev/orca-command-refactor/review/spec-panel.md` (review 1 of 3, verdict FAIL, 16 findings).
- Spec revised: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`.
- Repo root: /home/coder/workspaces/worktrees/IronClaude/exp346-v-ponytail-r3.

## 1. Evidence re-checked by the reviser
All checks read-only, run 2026-11-09 in this worktree. Spec line numbers `spec:N` refer to the spec as it stood before this revision (285 lines, 57,763 bytes).

| # | Check | Result |
|---|---|---|
| R1 | Existing contract `status` values | `status: success \| partial \| failed` at `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:7`; `success \| partial \| failed \| dry-run` at `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:341` and `src/superclaude/skills/sc-reflect-protocol/SKILL.md:665`; reflect branches on `status: success` at `src/superclaude/skills/sc-reflect-protocol/SKILL.md:334`. Finding 1 holds. |
| R2 | Adversarial contract shape | `status` sits under a `return_contract:` key, not at the top level: `src/superclaude/skills/sc-adversarial-protocol/SKILL.md:431,436`; real file `.dev/codegraph-migration/decisions/P3-command-set/adversarial/return-contract.yaml:1,5`. So 7.2 step 4's `d['status']` also fails on adversarial for a second reason (new fact, folded into Finding 1). |
| R3 | Workflow `--output` and pre-creation STOPs | `--output` is retired and STOPs with `E-LEGACY` (`src/superclaude/skills/sc-workflow-protocol/SKILL.md:24`); pre-creation STOPs write "no package directory, no yaml" (`refs/return-contract.md:39`); package path is `.dev/tasks/to-do/<id>/` (`refs/return-contract.md:3`). Finding 2 holds. |
| R4 | Retry reuses the Task | `worker-start --task <task_id> --retry-of <dispatch_id>`; "Do not route around that boundary with a new Run, Task, or unrelated Dispatch" (`.dev/orca-command-refactor/inventory/orca-capabilities.md:116`). Finding 3 holds, and it rules out the review's "coordinator creates a new Task" option. |
| R5 | Waiting worker is healthy | `.dev/orca-command-refactor/inventory/orca-capabilities.md:129`. Finding 4's stall outcome holds. |
| R6 | Install path for core files | `grep -n core Makefile` prints nothing (sync-dev never copies core); `KNOWN_CORE_FILES` at `src/superclaude/cli/install_core.py:13-24` lacks `WORKER-CONTRACT.md`; `superclaude install --force` exists (`src/superclaude/cli/main.py:35-39,46`). Finding 5 holds. |
| R7 | `grep -E '^-[^-]'` on a diff deleting `- a deleted bullet`, an empty line and `--flag deleted` | prints nothing, exit 1. Finding 6 holds. |
| R8 | `grep -cE` with `(orchestration\|worktree)` vs `(orchestration\|worktree)` written with a plain pipe, on `run orca worktree create` | escaped form prints `0`, plain form prints `1`. Finding 7 holds; table cells with `\|` are at spec:172, 175, 176, 193. |
| R9 | SA-2 vs AC-C1 | SA-2 allows an Orca mention in the contract file (spec:147); AC-C1 scans `src/superclaude/core` (spec:172). Finding 8 holds. |
| R10 | `ask` resume, no cap | spec:61; `.dev/orca-command-refactor/inventory/orca-capabilities.md:60,64`. Finding 9 holds. |
| R11 | WC-5 mapping | spec:63 maps only "no report exists" to failed. Finding 10 holds. |
| R12 | Heartbeat and release | Orca never releases on heartbeat (`orca-capabilities.md:111`); heartbeat-age use UNVERIFIED (`orca-capabilities.md:130`). Finding 11 holds as written (harm limited). |
| R13 | Readiness fallback | 45 s probe failed at `agent_readiness` (`.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md:39`); 30 s fallback passed, worker-start returned after 34 s (`EVIDENCE.md:45`); above about 45 s fails again (`EVIDENCE.md:56`). Finding 12 holds. |
| R14 | Spec repo root | spec:4 names `.../OrcaCLICommandRefactor-Specs`, the same root the binding README states (`.dev/orca-command-refactor/README.md:8`). Finding 13 is true for this machine but the spec matches its governing README. |
| R15 | Placeholders in the spec before revision | `grep -nE 'TODO\|TBD\|FIXME\|XXX\|RF_PLACEHOLDER\|\{\{'` printed nothing. |

## 2. Disposition per finding
"Where" cites the revised spec, `spec':N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N` after this revision. Every added sentence in the spec names its finding number.

| # | Severity (review) | Verified? | Disposition | Where / reason |
|---|---|---|---|---|
| 1 | CRITICAL, blocking | Yes (R1, R2) | **Applied** | WC-4 keeps `success` from existing producers and reads it as `succeeded`, and reads `status` from under `return_contract:` for adversarial (spec':62); 7.2 step 4 assert accepts `success` and unwraps `return_contract` (spec':207); Decisions row "Status vocabulary" (spec':291). Producers are not renamed, so `/sc:reflect`'s `status: success` branch keeps working. |
| 2 | CRITICAL, blocking | Yes (R3) | **Applied** | WC-4 states one default location plus a per-command exception table with flag, contract path and when the coordinator knows it (spec':62, 72-82); workflow: never `--output`, the worker reports the generated path, pre-creation STOP maps to `failed` (spec':77, 104); 2.3 brief duty (spec':85); section 3 "Contract" definition (spec':88); 7.2 step 3 report-path check, with the workflow pattern (spec':206); AC-1.4 drops the workflow clause (spec':222). Consistency edits without their own finding tag: P1 command list no longer lists a workflow fix (spec':171), SA-4 no longer lists a workflow contract gap (spec':161). |
| 3 | MAJOR (FR-8), blocking | Yes (R4) | **Applied** | WC-6 assigns retry handling to the worker session: detect a non-empty output location, then add the resume flag or rename the location to `<location>.attempt-<k>` and rerun; attempt 1's contract is kept (rename) or rewritten by the resumed run (spec':64). The review's other option, a new Task per retry, was not used: Orca's guide forbids routing around the circuit breaker with a new Task (`.dev/orca-command-refactor/inventory/orca-capabilities.md:116`). |
| 4 | MAJOR, blocking | Yes (R5) | **Applied** | P1 adds `--unattended` and `## Unattended mode` only to the P1 commands and the six gate-free ready commands; each later phase adds them with its gate conversions; until then the coordinator dispatches such commands without `--unattended` per 3.1 (spec':171). AC-1.1 test is cumulative and asserts later-phase commands carry no section yet (spec':219). |
| 5 | MAJOR, blocking | Yes (R6) | **Applied** | New 7.2 step 0: `make sync-dev`, `uv run superclaude install --force`, and `cmp` of the source and installed `WORKER-CONTRACT.md` (spec':203). |
| 6 | MAJOR, blocking | Yes (R7) | **Applied** | AC-C5 and AC-0.3 use `git diff --numstat ... \| awk '$2 != 0'` (deleted-line count) in fenced blocks (spec':188, 190, 197-198, 217, 237-238). Re-checked: the filter prints the line for a file with 1 deleted line and nothing for 0, and AC-C5 prints nothing for an unedited command today. |
| 7 | MAJOR, blocking | Yes (R8) | **Applied** | AC-C1, AC-C4, AC-C5 and AC-0.3 moved out of table cells into fenced `sh` blocks with plain `\|` (table rows spec':184, 187, 188, 217; blocks spec':192-199, 236-239); explanation at spec':190. Re-checked: AC-C1 prints nothing on today's tree and matches a positive-control line `orca orchestration ask`. Only remaining `\|` in the spec is the prose explanation at spec':190. |
| 8 | MAJOR, blocking | Yes (R9) | **Applied** | SA-2 now allows the Orca mention in the contract file and the `HOW-WE-WORK.md` Orca section as prose only ("the preamble's `ask` command"), never a runnable `orca`/`orca-ide` line, so AC-C1 keeps scanning `src/superclaude/core` without an exclusion (spec':159). Chosen over excluding the file from AC-C1 because it keeps the check stronger. |
| 9 | MAJOR (FR-8), blocking | Yes (R10) | **Applied** | WC-3 caps resumes at one; a second timeout or a declining reply resolves the gate as blocked; re-invocation follows the WC-6 re-run rule (spec':61). 7.2 step 3 gives the coordinator a fixed reply for AC-2.2 runs and makes any other `question` a check failure (spec':206). |
| 10 | MAJOR (FR-8), blocking | Yes (R11) | **Applied** | WC-5 maps a missing, empty, non-YAML or status-less report to `--outcome failed` (spec':63). |
| 11 | MAJOR (FR-8), blocking | Yes (R12) | **Applied** | WC-10: heartbeat before and after each foreground Agent-tool call; lapses during it are allowed; the coordinator judges by `worker-show`/`worker-list` liveness (spec':68). AC-4.3 limits its 5-minute heartbeat and 240 s checks to outside Agent-tool calls and to Bash calls (spec':234). |
| 12 | MAJOR (FR-8), blocking | Yes (R13) | **Applied** | WC-1 states the number: fall back within 30 s at the default 60 s limit; above about 45 s fails (spec':59). |
| 13 | MINOR, not blocking | True on this machine (R14) | **Rejected** | The spec's root (spec':4) is the root the binding run README states (`.dev/orca-command-refactor/README.md:8`); changing it would make the spec disagree with its governing README. The review's reviser brief says minor findings need no change (`.dev/orca-command-refactor/review/spec-panel.md:185`). Recorded here as a note for the coordinator. |
| 14 | MINOR, not blocking | Yes | **Rejected** | WC-1 is owned by launch setup, which the spec places outside the command phases on purpose (spec':59 owner column); WC-12 needs no command change (spec':70). Adding phase and check rows would be a new mechanism no blocking finding calls for (`.dev/orca-command-refactor/review/spec-panel.md:185`). |
| 15 | MINOR, not blocking | Yes (`orca-capabilities.md:115`) | **Rejected** | Minor per the review (`spec-panel.md:160`); the reviser brief forbids changes for minor findings (`spec-panel.md:185`). Live checks can be run one at a time or in separate worktrees without a spec change; left as a note for the phase plans. |
| 16 | MINOR, not blocking | Yes (`src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:6`) | **Rejected** | Minor per the review (`spec-panel.md:161`); after Finding 1's fix the coordinator reads `status` the same way from old and new contracts, so a version field is not needed to read the outcome. Adding one would be a new field no blocking finding requires (`spec-panel.md:185`). |

Totals: 16 findings; 12 applied (all blocking), 4 rejected (all minor).

## 3. Spec size and placeholder check
| Check | Before | After |
|---|---|---|
| `wc -lc` on the spec | 285 lines, 57,763 bytes | 314 lines, 64,738 bytes |
| `grep -nE 'TODO\|TBD\|FIXME\|XXX\|RF_PLACEHOLDER\|\{\{'` on the spec | no match | no match (exit 1) |
| Every blocking finding cited in the spec | n/a | Findings 1-12 each appear at least once (`grep -o 'Finding[s]\? [0-9, ]*'`) |
| AC-C1 as now written, on today's tree | n/a | prints nothing (exit 1); positive control on `orca orchestration ask` matches |
| `git status --short` | `?? .dev/orca-command-refactor/` | `?? .dev/orca-command-refactor/` (no tracked file changed) |

Angle-bracket names such as `<dir>`, `<id>` and `<name>` in the spec are command-line arguments the coordinator fills per Task, not unfinished text.

## Decisions
| Decision | Options considered | Rationale |
|---|---|---|
| Minor findings 13-16 | Fix them too; record and reject | Rejected with reasons: the review's reviser brief says minor findings need no change and forbids adding mechanisms no blocking finding calls for (`.dev/orca-command-refactor/review/spec-panel.md:185`). |
| Workflow pre-creation STOPs (Finding 2) | Keep the P1 fix "write the contract for pre-creation STOPs" and invent a location; drop it | Dropped. Before the package exists there is no known directory (`sk/sc-workflow-protocol/refs/return-contract.md:39`), so any location would be a new mechanism; WC-5's "report missing → failed" already gives the right outcome. This also removes one existing-line change from workflow. |
| Retry owner (Finding 3) | Command writes per-run subdirectories; coordinator creates a new Task; worker session renames the old output aside | Worker session. A new Task routes around Orca's circuit breaker, which its guide forbids (`orca-capabilities.md:116`); per-run subdirectories would make the contract path unknown before dispatch, breaking WC-4. Renaming keeps attempt 1 and the known path. |
| AC-C1 vs contract file (Finding 8) | Exclude `WORKER-CONTRACT.md` from AC-C1; forbid runnable Orca lines in core files | Forbid: keeps AC-C1 covering every core file, and the worker already has the exact `ask` command in its preamble. |
| Unanswered or AC-2.2 questions (Finding 9) | Worker must never ask during AC-2.2; coordinator replies with a fixed refusal | Fixed refusal: the worker cannot know it is in a test run, but the coordinator does. |
| Adversarial `return_contract:` nesting | Leave step 4 as `d['status']`; unwrap the key | Unwrap: found while verifying Finding 1 (R2); without it step 4 fails on every adversarial contract, which is the same defect Finding 1 names. |
| Line citations | Cite pre-revision lines; cite post-revision lines | Section 1 cites the pre-revision spec as the review did; section 2 cites the revised spec (`spec':N`) so a reader can find each change. |

## UNVERIFIED items
1. Whether `worker-start --retry-of` lets the coordinator change the brief (`spec-panel.md:180`); the WC-6 fix does not depend on it, because the worker session handles a reused brief.
2. Whether the worker preamble tells a retry worker it is a retry; WC-6 detects a retry from a non-empty output location instead.
3. Whether `uv run superclaude install --force` overwrites every edited primitive a worker reads, and whether Claude Code reads the project `.claude/` copy or the `~/.claude/` copy first (`spec-panel.md:178`); 7.2 step 0 runs both `make sync-dev` and the install so either order loads the edited files, and checks only the core file by `cmp`.
4. Whether Orca uses heartbeat age in its liveness verdict (`orca-capabilities.md:130`); the WC-10 fix relies only on the verified fact that release never happens on heartbeat (`orca-capabilities.md:111`).
5. The review loop is at review 1 of 3 (`spec-panel.md:3`); this revision has not been re-reviewed. A fresh reviewer must confirm the fixes before the spec is treated as passing.
