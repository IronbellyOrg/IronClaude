review: 2 of 3

# Spec-panel re-review: orca-worker-contract-spec.md (review 2 of 3)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (288 lines)
- candidate sha256: `a6bb2fd31d271c13717322860b98be5dce7608e4f442926d61851162c5d899b7`
- baseline (`--baseline`): `.dev/orca-command-refactor/specs/history/spec-v1.md` (285 lines)
- baseline sha256: `d3cdbe57e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- prior report (`--re-review`): `.dev/orca-command-refactor/review/round1.md` (`review: 1 of 3`, `verdict: FAIL`)
- prior report sha256: `55c474b621cde1fb9b78b7dc5b9037881ac409ab0b74f3a58b31acc8e1995132`
- reviewer model: claude-haiku-5-5 (Haiku 5.5)
- mode: critique; focus: requirements, architecture; prompt: RE-REVIEW from `~/.claude/rules/prompts/document_review_loop_prompts.md` (sandbox home copy); N = prior 1 + 1 = 2
- Round1's header records candidate sha256 `d3cdbe...`, which is the baseline hash above. Round1 therefore reviewed the text now saved as spec-v1.md. Its findings quote v1 text and are checked here against the current candidate.

## Coverage and evidence limits

- Read in full: `round1.md`, `specs/history/spec-v1.md` (baseline), `specs/orca-worker-contract-spec.md` (candidate), `README.md`, `inventory/commands-a.md`, `inventory/commands-b.md`, `command.md`, the RE-REVIEW prompt file.
- Not in the sandbox: `.claude/agents/rf-qa.md` (project) and `~/.claude/agents/rf-qa.md`. Review Loop bullet 5 says its rules stand alone when that file is unread. This report applies bullets 5 and 7 of `command.md` as written and does not run steps 1-5 of the rf-qa Fix Cycle.
- No `--unattended` flag is in this run, so `~/.claude/WORKER-CONTRACT.md` was not needed and was not read.
- `inventory/orca-capabilities.md` was not read. CAPS:, `cmd/`, `sk/` and `src/` citations that the revision did not touch are not re-checked here and stay UNVERIFIED.
- Inventory citations checked in this loop: INV-A:14, :42, :53, :60, :95, :117; INV-B:38, :52, :132, :219, :239, :272.
- Git was not used. Only `review/round2.md` was written.

## Re-review guard table (guards on changed lines only)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| non-empty `--output` refusal | candidate line 73 | Zero/Empty: new per-attempt directory | empty directory | proceeds | writes contract | OK |
| non-empty `--output` refusal | candidate line 73 | Typical: plain re-run by a person into the same directory | non-empty directory | refuses | fails; writes no contract | GAP, blocking (F-08) |
| non-empty `--output` refusal | candidate line 73 | Legitimate edge: retry that passes a resume flag | non-empty directory | not refused (resume flag given) | resumes from disk | OK |
| non-empty `--output` refusal | candidate line 73 | Sentinel: first attempt wrote only a contract | non-empty directory | refuses | first attempt's contract stays in place | GAP, Medium (M-09) |
| implement Ruling exemption | candidate line 61 | Legitimate edge: gate is the implement Ruling | answer text | not relayed | blocked, per D2 | OK |
| open-gate rule | candidate line 159 | Typical: `--unattended` on a command whose gate row is still open | open gate | `status: blocked` | takes no default | OK |
| AC-1.5 expectation | candidate line 199 | Boundary: second run, same directory, no resume flag | non-empty directory | expected refusal | matches line 73 | OK (inherits F-08) |

## Step 1, evidence block

Roles are fixed as follows. BASELINE is `specs/history/spec-v1.md`. CANDIDATE is `specs/orca-worker-contract-spec.md`. The command run is `diff -w BASELINE CANDIDATE`. Lines starting `<` are BEFORE (baseline). Lines starting `>` are AFTER (candidate). The lines below are copied verbatim from that output.

```text
BEFORE (baseline), lines starting "<":
< | WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag. On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11) |
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
< The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
< The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
< ### 3.1 Ready today (10)
< | adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
< | cleanup-audit | `--pass <N>` (single pass) | `.claude-audit/pass<N>-summary.md` | `progress.json` checkpoint | Name the `--pass all` final report; output dir is fixed, so one audit per worktree at a time (WC-11) (P1) | `sk/sc-cleanup-audit-protocol/SKILL.md:76,113`; `cmd/cleanup-audit.md:112-117`; `INV-A:42` |
< | index-repo | none | `PROJECT_INDEX.md` (location implied) | `mode=update` | State the output location (P1) | `cmd/index-repo.md:72,140-144,170-173`; `INV-A:53` |
< | tdd | a precise component prompt, not a bare topic; `--output <file>` | the TDD at `--output` | `--resume <task-file>` | Under `--unattended`, the topic-only clarification and nested `/task` "ask the user" lines resolve as blocked (P2) | `sk/tdd/SKILL.md:48,52-61,190`; `sk/task/SKILL.md:49,114`; `cmd/tdd.md:29`; `INV-B:47,217-225` |
< | troubleshoot | no `--fix` | `REPORT.md` (`report_path`) | Fresh dir | Under `--unattended`, the `--depth deep` short-input STOP and the `--fix` offer resolve as blocked (P2) | `sk/sc-troubleshoot-protocol/SKILL.md:57,63-68,209`; `sk/sc-troubleshoot-protocol/refs/remediation-handoff.md:58`; `INV-B:49,237-245` |
< | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
< ### 3.2 Needs a change (27)
< | research | `--unattended` pins `--strategy planning` (the strategy that runs without clarification) | contract naming the generated `claudedocs/research_*.md` path | fresh file | none | `cmd/research.md:25,103,123-132`; `src/superclaude/agents/deep-research-agent.md:40-56`; `INV-B:38,127-135` | P2 |
< | SA-2 | No command, skill or agent file runs an `orca` or `orca-ide` command, and none requires Orca to be installed or running. The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file. | Commands run in other projects (`CLAUDE.md:74`); without Orca the calls fail with `runtime_unavailable` (`CAPS:147`). | `CAPS:145-149`; today's baseline: only `sk/ccsession-tag/` mentions Orca (section 1.2, E5) |
< | **P0. Contract and live baseline** (no command edits) | Write `src/superclaude/core/WORKER-CONTRACT.md` (section 2 rules plus a coordinator brief template listing the section 3.1 flags), add it to `KNOWN_CORE_FILES`, add an Orca section to `HOW-WE-WORK.md` and its two mirrored copies, and add the static test file `tests/skills/test_worker_contract.py` (proposed name). Then run three ready commands as real Orca workers, invoked directly, to close evidence gap 1.4 (1). | Smoke runs: `/sc:troubleshoot` (no `--fix`), `/sc:workflow --handoff none`, `/sc:adversarial --output <dir>` | Uses only the 10 ready commands, so the coordinator gets value before any command changes, and the smoke runs test the decision before anything is built on it. |
< | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
< | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
< | Inventory verdicts | Re-judge commands; keep the inventories' 10 / 27 / 6 split | Keep: both inventories were independently citation-checked (`INV-A:106`, `INV-B:320`) and nothing read in this task contradicted a verdict. `/sc:load` and `/sc:recommend` are noted as coordinator-side helpers without changing their verdict. |

AFTER (candidate), lines starting ">":
> | WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag. The implement Ruling gate is exempt from this relay unless the user chooses D2(b) (F-01). On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11) |
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists, except the non-empty-directory refusal in section 2.3 (F-05). Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
> The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). For a retry (`worker-start --retry-of`, `CAPS:116`) the coordinator passes a new `--output` for each attempt, for example `<dir>/attempt-2/`. A command with no resume flag refuses a non-empty `--output` directory: it stops before writing into it, writes no contract there (the one outcome without a contract under WC-4), and states the refusal in the `worker_done` body (F-05). Until a command has a per-run output path (the `--slug` flag added in P1), the coordinator runs at most one worker of that command per worktree (WC-11, F-06). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
> The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 7 ready today, 30 needing a change and 6 coordinator-only (section 4). Workflow, index-repo and cleanup-audit moved from ready to needing a change (F-04, F-06). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
> ### 3.1 Ready today (7)
> | adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Write the contract at the WC-4 path `<output-dir>/return-contract.yaml`, not under `<output>/adversarial/` (P1; the skill names no file, `INV-A:60`) (F-04) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
> | tdd | a precise component prompt, not a bare topic, that names one task file (the nested `/task` asks when several match, `INV-B:219`); `--output <file>` (F-07) | the TDD at `--output` | `--resume <task-file>` | Under `--unattended`, the topic-only clarification and nested `/task` "ask the user" lines resolve as blocked (P2) | `sk/tdd/SKILL.md:48,52-61,190`; `sk/task/SKILL.md:49,114`; `cmd/tdd.md:29`; `INV-B:47,217-225` |
> | troubleshoot | no `--fix`; no `--depth deep`, whose short-input STOP is unflagged until P2 (`INV-B:239`) (F-07) | `REPORT.md` (`report_path`) | Fresh dir | Under `--unattended`, the `--depth deep` short-input STOP and the `--fix` offer resolve as blocked (P2) | `sk/sc-troubleshoot-protocol/SKILL.md:57,63-68,209`; `sk/sc-troubleshoot-protocol/refs/remediation-handoff.md:58`; `INV-B:49,237-245` |
> ### 3.2 Needs a change (30)
> | cleanup-audit | no gate | `<output-dir>/return-contract.yaml` (WC-4) plus `.claude-audit/pass<N>-summary.md`; the `--pass all` final-report name is UNVERIFIED | `progress.json` checkpoint | add a `--slug` flag that names the `.claude-audit/` subdirectory, so two workers in one worktree never write the same summary (F-06); name the `--pass all` final report | `sk/sc-cleanup-audit-protocol/SKILL.md:76,113`; `cmd/cleanup-audit.md:112-117`; `INV-A:42` | P1 |
> | index-repo | no gate | `<output-dir>/return-contract.yaml` (WC-4) plus `PROJECT_INDEX.md`, whose location is implied, not stated (UNVERIFIED) | `mode=update` | add a `--slug` flag that names the index file, so two workers in one worktree never overwrite each other's index (F-06) | `cmd/index-repo.md:72,140-144,170-173`; `INV-A:53` | P1 |
> | research | `--unattended` pins `--strategy planning` (the strategy that runs without clarification) | `<output-dir>/return-contract.yaml` naming the generated `claudedocs/research_*.md` path it wrote | fresh file | add `--output` so the contract path is known before dispatch (F-04) | `cmd/research.md:25,103,123-132`; `src/superclaude/agents/deep-research-agent.md:40-56`; `INV-B:38,127-135` | P2 |
> | workflow | `--handoff none`; pre-creation STOPs resolve as blocked, with a contract | add `--output <dir>`; the contract is `<output-dir>/return-contract.yaml` for every outcome, including pre-creation STOPs; today it is `.dev/tasks/to-do/<id>/return-contract.yaml`, and `<id>` is created at run time (F-04) | fresh package each run | none beyond the contract | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` | P1 |
> | SA-2 | No command, skill, agent or core file (the contract file included) runs or names an `orca` or `orca-ide` command, and none requires Orca to be installed or running. The contract describes the question channel only as the preamble's `ask` command (F-03). | Commands run in other projects (`CLAUDE.md:74`); without Orca the calls fail with `runtime_unavailable` (`CAPS:147`). | `CAPS:145-149`; today's baseline: only `sk/ccsession-tag/` mentions Orca (section 1.2, E5) |
> | **P0. Contract and live baseline** (no command edits) | Write `src/superclaude/core/WORKER-CONTRACT.md` (section 2 rules plus a coordinator brief template listing the section 3.1 flags), add it to `KNOWN_CORE_FILES`, add an Orca section to `HOW-WE-WORK.md` and its two mirrored copies, and add the static test file `tests/skills/test_worker_contract.py` (proposed name). Then run three ready commands as real Orca workers, invoked directly, to close evidence gap 1.4 (1). | Smoke runs: `/sc:troubleshoot` (no `--fix`, no `--depth deep`), `/sc:brainstorm --output <dir>`, `/sc:adversarial --output <dir>` | Uses only the 7 ready commands, so the coordinator gets value before any command changes, and the smoke runs test the decision before anything is built on it. |
> | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate; on a command whose gate row is still open, it writes `status: blocked` at that gate and takes no default there) (F-02); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit and index-repo (the `--slug` flag, F-06), workflow contract (F-04) | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
> | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:brainstorm "<topic>" --output <dir>`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
> | P1 | AC-1.5 | `/sc:analyze <target> --unattended --output <dir>` run twice with the same `<dir>` and no resume flag on the second run; `sha256sum` of the first run's files taken before the second run | second run refuses, `worker_done --outcome failed`, the first run's files unchanged (F-05, WC-6) |
> | P1 | AC-1.6 | `/sc:auggie-review <PR> --unattended` run during P1, before P2 converts its gate; comment counts as in AC-2.4 | `status: blocked` written; both counts unchanged (F-02) |
> | P1 | AC-1.7 | `/sc:index-repo --unattended --slug a` and `--slug b` run in one worktree | two files exist and neither is overwritten (F-06) |
> | Inventory verdicts | Re-judge commands; keep the inventories' 10 / 27 / 6 split | Keep the split except three moves to needs-change: workflow, index-repo and cleanup-audit, whose report paths cannot be known before dispatch (F-04, F-06). Otherwise keep: both inventories were independently citation-checked (`INV-A:106`, `INV-B:320`) and nothing read in this task contradicted a verdict. `/sc:load` and `/sc:recommend` are noted as coordinator-side helpers without changing their verdict. |
```

## Self-check

`grep -nF` of each AFTER line (without its `>`) in the candidate: 21 of 21 found. `grep -nF` of each BEFORE line (without its `<`) in the baseline: 18 of 18 found. The roles are confirmed and no swap occurred.

## Prior blocking findings (round1)

| Prior id | Status | Evidence (candidate) |
|---|---|---|
| F-01 | resolved | WC-3 (line 61) now says "The implement Ruling gate is exempt from this relay unless the user chooses D2(b)". The implement row (line 106) keeps the Ruling rule. §8 item 6 (line 221) and §9 D2 agree. |
| F-02 | resolved | P1 (line 159) now says a command whose gate row is still open "writes `status: blocked` at that gate and takes no default there". AC-1.6 (line 200) tests it. |
| F-03 | resolved | SA-2 (line 147) no longer permits an Orca mention. WC-3 (line 61) names only "the preamble's `ask` command". AC-C1 (line 172) is unchanged. The routing-guide tension this leaves is M-10. |
| F-04 | resolved | adversarial (line 83) writes the WC-4 path. research (line 115) and workflow (line 125) each take `--output` and write `<output-dir>/return-contract.yaml`. INV-A:60 and INV-B:132 support the change. |
| F-05 | resolved as to overwrite; scope defect is new F-08 | §2.3 (line 73) adds a new `--output` per attempt and refuses a non-empty directory. AC-1.5 (line 199) tests it. The retry overwrite that F-05 named is closed. The refusal's scope is F-08. |
| F-06 | resolved | cleanup-audit (line 107) and index-repo (line 110) moved from ready to needs-change with `--slug` (§3.1 now has 7 rows). §2.3 (line 73) gives the one-worker-per-worktree rule. AC-1.7 (line 201) tests it. |
| F-07 | resolved | tdd (line 88) requires a precise prompt that names one task file. troubleshoot (line 89) excludes `--depth deep`. INV-B:219 and INV-B:239 support both. |

No prior blocking finding is open. One new blocking finding (F-08) is raised below.

## Findings on changed lines

Origin is `changed` unless marked otherwise.

### F-08 (new), blocking: the `--output` refusal is not scoped to unattended mode (candidate line 73)

- Stated text (§2.3, line 73): "A command with no resume flag refuses a non-empty `--output` directory: it stops before writing into it, writes no contract there (the one outcome without a contract under WC-4), and states the refusal in the `worker_done` body (F-05)."
- Sentence test: an implementer who follows that text as written builds commands that refuse any non-empty `--output` directory without a resume flag, including a person's plain re-run. That is wrong because SA-1 (line 146) says that without `--unattended` every output path "stays as it is today", and §5 (line 141) makes standalone behaviour a hard requirement on every phase.
- Evidence the behaviour changes today: the ready rows for brainstorm (line 84) and adversarial (line 83) already take `--output <dir>`, and today a second run into that directory is not refused. SA-3 (line 148) has the same rule for files.
- Why it is blocking: two stated texts contradict each other. The line 73 sentence does not say "in unattended mode". WC-4 (line 62) is scoped to unattended mode, so the implementer has to infer the scope.
- Fix for the reviser: scope the refusal to unattended mode in line 73 and keep the F-05 data-loss protection for worker runs.

### M-09 (Medium), origin unchanged, quotes changed line 73: a refused retry can pass the live check

- §7.2 steps 3 and 4 (candidate lines 182-183) are unchanged. A refused retry in a directory that still holds the first attempt's contract passes `test -s <contract>`, and the step 3 path check (the WC-4 path) also matches the first attempt's file.
- The refusal writes no contract (line 73). `worker_done --report-path` therefore has no real file to name, which CAPS:72-74 (quoted by WC-4, line 62) says the flag must not do.
- Consequence: the live check can accept a stale contract. There is no data loss, so this is Medium.

### M-10 (Medium), origin changed, lines 147 against 150, 158 and 172: routing-guide Orca text

- SA-2 (line 147) now covers core files and says no core file "runs or names" an `orca` or `orca-ide` command.
- P0 (line 158) adds an Orca section to `HOW-WE-WORK.md`, which is a core file, and SA-5 (line 150) requires it.
- AC-C1 (line 172) greps `src/superclaude/core` with no exclusion for the routing guide.
- Prose-only Orca text passes all three. A section that names an Orca command fails SA-2 and AC-C1. The spec does not say which is intended. Nothing forces a failure, so this is Medium.
- Fix: exclude the routing guide's Orca section from SA-2 and AC-C1, or forbid Orca commands in it.

### M-11 (Medium), origin changed, line 201: AC-1.7 names no path to inspect

- AC-1.7 asserts that two index files exist. The location of `PROJECT_INDEX.md` is UNVERIFIED (INV-A:53; INV-A:117), and the index-repo row (line 110) says so too. The check does not name a directory to look in.
- Fix: state the directory in AC-1.7 or in the row.

### Changed lines checked with no finding

- Line 61 (the F-01 resolution), line 62 (its refusal clause belongs to F-08).
- Line 76: counts 7 + 30 + 6 = 43, checked against the rows at lines 83-89 and the §3.2 rows.
- Lines 78 and 83: consistent with WC-4 (line 62) and INV-A:60.
- Lines 88-89: see note N-02.
- Lines 107, 110, 115, 125: consistent with INV-A:42, INV-A:53, INV-B:38, INV-B:52, INV-B:132 and INV-B:272.
- Lines 158-159: the P0 smoke runs use only §3.1 rows, and the P1 scope matches the §3.2 rows.
- Line 194 (AC-0.4): consistent with the P0 row.
- Lines 199-200 (AC-1.5, AC-1.6): testable as written, subject to F-08 and M-09.
- Line 271: 10 rows, of which 3 moved, giving 7 ready and 30 needing a change.
- Deleted lines (cleanup-audit and index-repo from §3.1, between candidate lines 84 and 85): covered by F-06.

## Follow-up candidates (Medium and minor; not blocking; none created)

These need the user's answer before any issue is opened. None is created.

- **M-09, M-10, M-11**: listed above.
- **Round1 M-01** (§1.2 E2): "same tools" and "answered" are still overstated or uncited. Open, unchanged.
- **Round1 M-02** (§1.3 R1): "would be refused with `nested_worker_depth_exceeded`" is still stated as fact. Open, unchanged.
- **Round1 M-03** (WC-5, line 63): `partial` still maps to `succeeded` and still unblocks dependents. Open, unchanged.
- **Round1 M-04** (missing checks): partly addressed. WC-6 now has AC-1.5 (line 199). WC-3 (ask flow) and WC-10 (long waits) still lack a §7 check. Partly open.
- **Round1 M-05** (AC-C5, line 176): the Usage-line addition is still undecided. Open, unchanged.
- **Round1 M-06** (reflect headless rule under `--unattended`; §3.1 reflect row and SA-6): open, unchanged.
- **Round1 M-07** (WC-7, line 65): still cites INV-A:95 for "nesting loses tools". INV-A:95 says nesting is allowed up to three layers. The loss statement is at INV-A:14. Open, a citation fix.
- **Round1 M-08** (WC-9, line 67 against D4): open, unchanged.

## Notes (not graded)

- N-01: citations to `cmd/`, `sk/`, `src/`, CAPS and `.dev/evals/` are not re-checked in this loop and stay UNVERIFIED, as in round1 N-01.
- N-02: the tdd row (line 88) closes the INV-B:219 prompt only if the named task file resolves to exactly one match. How `/task` resolves a named file is in `sk/task/SKILL.md`, which is not in the sandbox. UNVERIFIED.
- N-03: round1 N-02 (§6 should say Phase 2 depends on D4) is not reflected. The §6 text is unchanged.
- N-04: `review/revise1.md` is in the workspace but was not read. It is not a review input.

## Reviser brief

Blocking ids: F-08.

Revise only text a blocking finding names. Add no rule, mechanism or section that no blocking finding calls for. Each added paragraph or table cites its finding id. Prefer deleting or narrowing to adding. Report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not revised here.

verdict: FAIL
