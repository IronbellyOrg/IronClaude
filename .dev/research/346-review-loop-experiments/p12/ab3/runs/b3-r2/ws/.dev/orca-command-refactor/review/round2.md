review: 2 of 3

# Spec-panel report, round 2 (re-review): orca-worker-contract-spec

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md`
- CANDIDATE (the revised text under review): `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 285 lines, 59339 bytes, sha256 `523f1629dc21eaacc3987537a70cf3e5944edf741f8b5368cdaad6f32cf68d9c`
- BASELINE (the text before the revision): `.dev/orca-command-refactor/specs/history/spec-v1.md`, 285 lines, 57763 bytes, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (equal to the candidate hash recorded at `round1.md:7`, so the baseline is the text round 1 reviewed)
- PRIOR (the previous review report): `.dev/orca-command-refactor/review/round1.md`, sha256 `5f2fc903c624ae9a7abd78b7215a7ef6d0ec54b58c40cb016a290159587e269b`; its first line is `review: 1 of 3` (`round1.md:1`) and its last line is `verdict: FAIL` (`round1.md:294`), so N = 1 + 1 = 2 and the "review 3 with FAIL" halt does not apply
- reviser report read for context only: `.dev/orca-command-refactor/review/revise1.md`
- reviewer model actually used: claude-sonnet-5-5
- format: standard (default); input type: neither TDD nor PRD (no TDD frontmatter, no PRD headings), so no `target_release` question applies
- prompt followed: RE-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full, lines 1-68): roles table, Step 1 evidence block, review number, self-check; grading by the FIRST-REVIEW grading check (that file, line 35)
- mode and scope: `--mode critique` with `--re-review` and `--baseline`; per `command.md:261` `--iterations` is ignored, the Improve step is skipped and no revised specification is written

## Citation legend

All paths are relative to the workspace root. A citation of a file that is not in the workspace is UNVERIFIED.

- `SPEC:N` = candidate line N (the candidate and the baseline have the same line count, so `SPEC:N` is also baseline line N except on the 15 changed lines)
- `BASE:N` = baseline line N
- `R1:N` = `.dev/orca-command-refactor/review/round1.md` line N
- `REV:N` = `.dev/orca-command-refactor/review/revise1.md` line N
- `README:N` = `.dev/orca-command-refactor/README.md` line N
- `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`
- `CMD:N` = `command.md` (the `/sc:spec-panel` definition) line N
- `sk/...`, `cmd/...` and every path outside the workspace: UNVERIFIED unless a workspace file quotes it

## Step 1. Evidence block

Roles are fixed by the brief: CANDIDATE is the `@file`, BASELINE is `--baseline`, PRIOR is `--re-review`. Command run: `diff -w .dev/orca-command-refactor/specs/history/spec-v1.md .dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (exit 1, 10 hunks, 15 changed lines; the same 15 lines appear without `-w`, so no change is whitespace-only). The lines below are copied by script from that output, without edits.

### BEFORE (baseline), lines starting `<`

```text
62c62
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
64c64
< | WC-6 | **Resume or safe re-run.** A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output. A command either resumes from its on-disk state when given its resume flag, or, if it has none, writes each run into a fresh output directory so a re-run starts clean. Section 3 names which applies per command. | Command | `CAPS:116` (retry and circuit breaker); resume mechanisms in column (e) of `INV-A:35-55`, `INV-B:31-52` |
73c73
< The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
76c76
< The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
83,87c83,87
< | adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
< | brainstorm | `--output <dir>`; never `--interactive` | `<output>/return-contract.yaml` | `--resume-from <seed-brief>` | None | `sk/sc-brainstorm-protocol/SKILL.md:134,335`; `cmd/brainstorm.md:59-63`; `INV-A:39` |
< | cleanup-audit | `--pass <N>` (single pass) | `.claude-audit/pass<N>-summary.md` | `progress.json` checkpoint | Name the `--pass all` final report; output dir is fixed, so one audit per worktree at a time (WC-11) (P1) | `sk/sc-cleanup-audit-protocol/SKILL.md:76,113`; `cmd/cleanup-audit.md:112-117`; `INV-A:42` |
< | index-repo | none | `PROJECT_INDEX.md` (location implied) | `mode=update` | State the output location (P1) | `cmd/index-repo.md:72,140-144,170-173`; `INV-A:53` |
< | init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report | None | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
92c92
< | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
159c159
< | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
182c182
< 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path.
195,196c195,196
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
< | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
205c205
< | P3 | AC-3.2 | `/sc:roadmap <spec> --unattended --output <dir>` with an existing `<dir>/.session-memory.md` and no resume flag | starts fresh, no `[Y/n]` in the transcript, contract written |
```

### AFTER (candidate), lines starting `>`

```text
62c62
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`), unless the command's section 3 row names another contract path. Where `--output` is a file (init-lite, tdd, and the new spec-panel flag) the contract is written beside that file as `<file name>.return-contract.yaml`. The path is known before dispatch, except for workflow, whose row says why. It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
64c64
> | WC-6 | **Resume or safe re-run.** A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output. A command either resumes from its on-disk state when given its resume flag, or, if it has none, writes each run into a fresh output directory that the coordinator passes (section 2.3), so a re-run starts clean. Section 3 names which applies per command. | Command | `CAPS:116` (retry and circuit breaker); resume mechanisms in column (e) of `INV-A:35-55`, `INV-B:31-52` |
73c73
> The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory (or output file), so the report path is known before dispatch (WC-4; workflow is the exception its row names); which outward actions, if any, are authorized (WC-9); on a `--retry-of` retry, either the command's resume flag with the first attempt's directory or, for a command with no resume flag, a new output directory, never the first attempt's (WC-6); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
76c76
> The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`, or the contract path the row names. Every changed command except `load` (it has no report file, so no contract to name) also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
83,87c83,87
> | adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract filename to `<output>/adversarial/return-contract.yaml`, which is its contract path (WC-4 exception) (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
> | brainstorm | `--output <dir>`; never `--interactive` | `<output>/return-contract.yaml` | `--resume-from <seed-brief>` | None; gains the `## Unattended mode` section (P1) | `sk/sc-brainstorm-protocol/SKILL.md:134,335`; `cmd/brainstorm.md:59-63`; `INV-A:39` |
> | cleanup-audit | `--pass <N>` (single pass) | `.claude-audit/pass<N>-summary.md` | `progress.json` checkpoint | Name the `--pass all` final report; contract path `.claude-audit/return-contract.yaml` (WC-4 exception, no output flag); output dir is fixed, so one audit per worktree at a time (WC-11) (P1) | `sk/sc-cleanup-audit-protocol/SKILL.md:76,113`; `cmd/cleanup-audit.md:112-117`; `INV-A:42` |
> | index-repo | none | `PROJECT_INDEX.md` (location implied) | `mode=update` | State the output location; contract path `PROJECT_INDEX.md.return-contract.yaml` beside it (WC-4 file rule) (P1) | `cmd/index-repo.md:72,140-144,170-173`; `INV-A:53` |
> | init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report | None; gains the `## Unattended mode` section (P1) | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
92c92
> | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome"); its path `.dev/tasks/to-do/<id>/return-contract.yaml` has a run-time `<id>`, so the worker names it in `worker_done` and the coordinator cannot know it before dispatch (WC-4 exception; whether the command prints the package path, and where a pre-creation STOP writes, are UNVERIFIED) (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
159c159
> | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command listed in this row (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only; no `## Unattended mode` section); fixes to adversarial, cleanup-audit, index-repo, workflow; brainstorm and init-lite (the section only) | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
182c182
> 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the contract path WC-4 or the command's section 3 row gives.
195,196c195,196
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command listed in the P1 row of section 6, except `load` (no contract to name), has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
> | P1 | AC-1.2 | 7.2 live check on each P1 command except `load`, with `--unattended` and, where its section 3 row takes one, `--output <dir>` | all steps pass |
205c205
> | P3 | AC-3.2 | `/sc:roadmap <spec> --unattended --output <dir2>`, where `<dir2>` is a copy of an earlier run's `<dir>` that holds `.session-memory.md`, with no resume flag | starts fresh in `<dir2>`, no `[Y/n]` in the transcript, contract written; `<dir>` is not touched (WC-6) |
```

### Self-check

`grep -nF -x` of each AFTER line (without its `>`) in the candidate: 15 of 15 found, at the line numbers the hunk headers give (62, 64, 73, 76, 83-87, 92, 159, 182, 195, 196, 205). `grep -nF -x` of each BEFORE line (without its `<`) in the baseline: 15 of 15 found at the same numbers. No role swap. Size check: `wc -c` gives 57763 before and 59339 after; a character-level diff of the 15 lines gives 1617 bytes added and 41 deleted (net +1576), which matches `REV:16-24`. The per-id split in `REV:21-23` could not be re-derived from the diff alone and is taken as written.

## Prior blocking findings: status against the AFTER text

| id | prior grade (R1) | status | deciding AFTER text |
|---|---|---|---|
| B-1 | blocking, CRITICAL (`R1:65-90`) | resolved | SPEC:195 (AC-1.1 limited to the P1 row, `load` excluded), SPEC:159 (row list and flag scope agree; brainstorm and init-lite placed), SPEC:84 and SPEC:87 (phase given), SPEC:76 (`load` exempt), SPEC:196 (AC-1.2 same scope) |
| B-2 | blocking, MAJOR (`R1:130-140`) | resolved | SPEC:62 (default path, row-named exception, file rule), SPEC:83, 85, 86, 92 (row paths), SPEC:73 and SPEC:182 (dependents) |
| B-3 | blocking, MAJOR (`R1:142-150`) | resolved | SPEC:64 (fresh directory is one the coordinator passes), SPEC:73 (retry clause), SPEC:205 (AC-3.2 uses a copy) |

No finding is open and none regressed (no prior finding was marked resolved in R1, so the `regressed` state cannot occur this round). No prior blocking finding was deferred or withdrawn by the reviser (`REV:5-6`).

### B-1 resolved: re-check against the AFTER text only

Prior defect (`R1:69-76`): AC-1.1 asserted the `## Unattended mode` section in all 37 commands of sections 3.1-3.2 at the end of Phase 1, while `load`, `pr-submit`, `brainstorm`, `init-lite` and the Phase 2-4 commands could not or did not receive it, and the rule at SPEC:154 then stops Phase 2.

- AC-1.1 (SPEC:195) now asserts the section only for "every command listed in the P1 row of section 6, except `load`". The P1 row (SPEC:159) lists 15 commands: 9 needs-change commands (analyze, build, business-panel, design, document, explain, index, test, load; each is `P1` in SPEC:99, 101, 102, 106, 107, 108, 111, 112, 123), 4 ready commands with fixes (adversarial, cleanup-audit, index-repo, workflow; SPEC:83, 85, 86, 92) and 2 ready commands that gain the section only (brainstorm, init-lite; SPEC:84, 87). Minus `load` that is 14 commands, each of which is edited in P1, so the assertion is passable.
- `pr-submit` (P4, SPEC:162) is no longer in AC-1.1, so SPEC:240 (D3 option (a): no pr-submit change in Phase 4) and SPEC:225 (Phases 0-3 proceed on the recommendations) no longer conflict with the P1 check.
- The sentence/list disagreement of `R1:76` is gone: SPEC:159 now says "every command listed in this row" and `grep -n 'sections 3.1' <candidate>` prints no match.
- Every one of the 10 ready commands of section 3.1 now has a phase: P1 for adversarial, brainstorm, cleanup-audit, index-repo, init-lite, workflow (SPEC:83-87, 92); P2 for reflect, release-split, tdd, troubleshoot (SPEC:88-91, 160).
- AC-1.2 (SPEC:196) gets the same scope. SPEC:154 therefore no longer blocks Phase 2 on an assertion that cannot pass.

### B-2 resolved: re-check against the AFTER text only

Prior defect (`R1:134-138`): WC-4's `<output-dir>/return-contract.yaml` contradicted the adversarial row (`<output>/adversarial/...`), the workflow row (run-time `<id>`), the file-valued `--output` commands and the fixed-location commands, and the live check required the report path to equal "the WC-4 contract path".

- SPEC:62 now says the default holds "unless the command's section 3 row names another contract path", gives one rule for file-valued `--output` (init-lite, tdd, the new spec-panel flag: `<file name>.return-contract.yaml` beside the file) and names workflow as the one exception to "known before dispatch".
- Each differing row now names its path: adversarial `<output>/adversarial/return-contract.yaml` (SPEC:83; consistent with `INV-A:35`, which records the two paths real runs used, and with AC-1.4 at SPEC:198); cleanup-audit `.claude-audit/return-contract.yaml` (SPEC:85; the directory is `INV-A:42`); index-repo `PROJECT_INDEX.md.return-contract.yaml` (SPEC:86; the location of `PROJECT_INDEX.md` is itself "implied, UNVERIFIED", `INV-A:53`); workflow `.dev/tasks/to-do/<id>/return-contract.yaml` with a run-time id (SPEC:92; `INV-B:272`).
- The live check (SPEC:182) now requires "the contract path WC-4 or the command's section 3 row gives", so adversarial and workflow can pass it; SPEC:73 matches (output "directory (or output file)", workflow the named exception).
- The contradiction named in `R1:134` (one run cannot satisfy WC-4 and the adversarial row and AC-1.4) is removed. Residual gaps that the new text leaves are not contradictions and are graded Medium below (M-12, M-13, M-15).

### B-3 resolved: re-check against the AFTER text only

Prior defect (`R1:146-148`): WC-6 offered a fresh output directory, AC-3.2 started a run fresh inside the same `<dir>` that held attempt 1, and nothing told the coordinator to pass a new directory.

- WC-6 (SPEC:64) now says the fresh directory is one "that the coordinator passes (section 2.3)"; section 2.3 (SPEC:73) now tells the coordinator, on a `--retry-of` retry, to pass either the resume flag with the first attempt's directory or, for a command with no resume flag, a new output directory, "never the first attempt's".
- AC-3.2 (SPEC:205) now runs `/sc:roadmap` into `<dir2>`, a copy of an earlier run's `<dir>`, so the first attempt's `roadmap.md` and contract are not overwritten; the pass condition keeps the `[Y/n]` test (the roadmap row, SPEC:118, replaces that prompt with the resume flag).
- The Sequence Attack of `R1:148` no longer works against the stated text: a retry that follows SPEC:73 either resumes or moves. Gaps in how SPEC:73 applies to individual commands are not a contradiction and are graded Medium (M-14).

## Findings index (findings on lines changed against the baseline)

| id | grade | label | bucket | lead expert | SPEC location | origin |
|---|---|---|---|---|---|---|
| M-12 | Medium | MAJOR | requirements | Wiegers / Adzic | SPEC:62, 73, 99, 101-102, 105-109, 111, 114-117, 119, 123, 196 | changed |
| M-13 | Medium | MAJOR | architecture | Nygard / Whittaker | SPEC:85, 86, 62, 63, 69 | changed |
| M-14 | Medium | MAJOR | architecture | Fowler / Nygard | SPEC:64, 73, 83, 85, 86, 88, 92, 116 | changed |
| M-15 | Medium | MAJOR | requirements | Whittaker | SPEC:92, 198, 62 | changed |
| N-8 | minor | MINOR | requirements | Wiegers | SPEC:52, 76, 112, 159 | changed |
| N-9 | minor | MINOR | requirements | Crispin | SPEC:196, 87 | changed |
| N-10 | minor | MINOR | requirements | Wiegers | SPEC:261, 62, 86 | unchanged, quotes changed SPEC:62 |
| N-11 | minor | MINOR | requirements | Crispin | SPEC:205, 64 | changed |
| N-12 | minor | MINOR | requirements | Crispin | SPEC:73, 194, 79 | unchanged, quotes changed SPEC:73 |

Blocking findings: none. Medium and minor findings are repeated under `follow-up candidates`.

## Panel

Seated by the focus areas: Wiegers (lead), Adzic, Cockburn (requirements); Fowler (lead), Newman, Hohpe, Nygard (architecture). Whittaker is active in every review (CMD:83). Crispin is seated for the Guard Condition Boundary Table (CMD:315). Order of CMD:101-113: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin. Cockburn, Newman and Hohpe found nothing on the changed lines (no actor/goal change, no service or integration boundary changed). Gregory and Hightower are not seated.

What the panel agrees on:

- The three prior blocking findings are resolved by clause-level edits only: the diff changes 15 existing lines, adds no paragraph, table or section (`REV:26`), and the line count is 285 before and after (checked with `wc -l`).
- The phase counts reconcile after the revision (see the Quantity Flow Diagram): 10 ready + 27 needs-change + 6 coordinator-only = 43 (SPEC:76); phases cover 37 commands (15 + 15 + 4 + 3).
- Disagreement: none recorded.

## === REQUIREMENTS ANALYSIS ===

### M-12 (Medium, MAJOR; origin=changed). WC-4 states that the contract path is known before dispatch for every command except workflow, but the rows leave the shape of a new output flag, or the contract location, unstated for many commands

Experts: Wiegers (traceability), Adzic (concrete example).

Grading check. An implementer who follows the stated text as written builds, for `/sc:build`, a new "report path" flag (SPEC:101) and a contract at `<output-dir>/return-contract.yaml` where `<output-dir>` is "the directory the coordinator passed" (SPEC:62). That may be wrong, because the file rule of WC-4 is a closed list ("init-lite, tdd, and the new spec-panel flag", SPEC:62) and `build`'s flag is not on it: if the implementer makes the flag a file, the literal path is `<file>/return-contract.yaml`, the path shape that `R1:137` showed cannot exist. The text allows both readings (a directory flag or a file flag) and never says which, so this is Medium, not blocking. The same gap covers: analyze "add `--output`" (SPEC:99), business-panel, design, index "add an output path" (SPEC:102, 106, 111), document "require an explicit output" (SPEC:107), explain "write the explanation to a file" (SPEC:108), test "add a report path" (SPEC:123). These eight are all P1 commands, and AC-1.2 (SPEC:196) runs the live check on them, where step 4 needs the contract path (SPEC:182-183).

Second part. SPEC:62 also says "The path is known before dispatch, except for workflow", yet these rows name no contract location at all: cli-portify "file location unnamed" (SPEC:105), implement "beside the ledger `progress.md`", whose `<slug>` or package directory the row does not give (SPEC:109; `INV-A:51`), pr-submit "beside `monitor-run-<PR>.jsonl`" (SPEC:114), recommend "write the handoff envelope to a file" (SPEC:115), research "contract naming the generated `claudedocs/research_*.md` path" (SPEC:116), review-translation (SPEC:117), save (SPEC:119). Whether the coordinator can know these before dispatch is not stated, so the "except workflow" claim is not backed by the rows. The prior round did not name these rows (`R1:134-138`), the claim is new text on a changed line, and no stated text yields a known wrong build, hence Medium.

Recommendation. Add to WC-4 one sentence: a command whose new output flag takes a file follows the file rule, and the row says which flag shape it adds; narrow "except for workflow" to "except where the row says the path is derived at run time". Priority: Medium. Quality impact: Consistency +1, Testability +1.

### M-15 (Medium, MAJOR; origin=changed). Where workflow writes its contract for a pre-creation STOP is not defined

Expert: Whittaker (Zero/Empty Attack).

I can break this specification by **Zero/Empty Attack**. The invariant at **SPEC:62 (the contract is written on every outcome, "including stops before any other output exists", and the worker passes its path as `worker_done --report-path`)** fails when **workflow stops before it has created its package, so no `<id>` exists**. Concrete attack: before state, `/sc:workflow "<change>" --handoff none --unattended` is dispatched and the command STOPs on a missing input, before it names a package directory (`INV-B:272`: the contract is "Not written for pre-creation STOPs"); the P1 fix asks for a contract anyway (SPEC:92) but the row says where it goes is UNVERIFIED; after state, the implementer chooses a path (for example `.dev/tasks/to-do/return-contract.yaml`), the worker has no path to name, finds no report, and sends `--outcome failed` with no `blocked_question` (SPEC:63), which is the silent stall that WC-4 exists to prevent. AC-1.4 (SPEC:198) only checks that the workflow ref "states the contract is written for pre-creation STOPs", not where. The row marks the question UNVERIFIED, which keeps the text honest, but the requirement stays open. Medium: needs the implementer to choose a path. Recommendation: name one path for a pre-creation STOP (or say it goes in the brief's output directory when the brief passes one). Priority: Medium.

### N-8 (minor; origin=changed). `load` is both inside and outside the P1 contract text

Expert: Wiegers. SPEC:159 says the `--unattended` flag is "accepted by every command listed in this row" and lists `load` "(usage line only; no `## Unattended mode` section)"; SPEC:112 says only `--checkpoint` is missing from its usage line; SPEC:52 still says "Each changed command adds a short `## Unattended mode` section", while SPEC:76 now exempts `load`. A reader cannot tell whether `load` accepts `--unattended` or gains the section. No consequence for the checks, because AC-1.1 and AC-1.2 both exclude `load` (SPEC:195-196). Note only.

### N-9 (minor; origin=changed). AC-1.2 names `--output <dir>` for a command whose output flag takes a file

Expert: Crispin. SPEC:196 says "where its section 3 row takes one, `--output <dir>`", and init-lite's row takes `--output <file>` (SPEC:87), whose contract is then `<file name>.return-contract.yaml` (SPEC:62). The `<dir>` is read as a placeholder for "an output path"; a tester who follows it literally passes a directory to a file flag. Note only.

### N-10 (minor; origin=unchanged, quotes changed SPEC:62 and SPEC:86). The one-name decision now covers four file names

Expert: Wiegers. SPEC:261 justifies reuse of `return-contract.yaml` because "one name lets the coordinator check every worker the same way". After the revision the file is `return-contract.yaml`, `<file name>.return-contract.yaml` (SPEC:62), `PROJECT_INDEX.md.return-contract.yaml` (SPEC:86) or a row path, so the coordinator needs the row to find it. The live check handles this generically (SPEC:182-183), so there is no failure; the Decisions row is slightly out of date. Note only.

### N-11 (minor; origin=changed). The AC-3.2 pass clause "`<dir>` is not touched" cannot fail

Expert: Crispin. SPEC:205 passes only `<dir2>` to the command, so `<dir>` is never reachable by the run and the clause is true by construction; it does not test the WC-6 property (a retry must not corrupt the first attempt). The `[Y/n]` and fresh-start parts of the check are meaningful. Note only.

### N-12 (minor; origin=unchanged, quotes changed SPEC:73). P0 smoke runs cannot use the `--unattended` form that the brief rule asks for

Expert: Crispin. SPEC:73 says the brief states "the exact command line including `--unattended`", while the P0 live checks (SPEC:194) are written without it and the flag arrives in P1/P2 (SPEC:159-160); SPEC:79 says the ready commands run "if the brief uses the stated flags". Older text; no consequence for the decision. Note only.

## === ARCHITECTURE ANALYSIS ===

### M-13 (Medium, MAJOR; origin=changed). A fixed contract path is reused by every run, so a stale contract can be read as the new one

Experts: Nygard (failure and recovery), Whittaker (Sequence Attack).

I can break this specification by **Sequence Attack**. The invariant at **SPEC:85 and SPEC:86 (fixed contract paths `.claude-audit/return-contract.yaml` and `PROJECT_INDEX.md.return-contract.yaml`)** fails when **a second run of the same command starts and ends without writing its contract**. Concrete attack: before state, pass 1 of `/sc:cleanup-audit --pass 1 --unattended` finished and left `.claude-audit/return-contract.yaml` with `status: succeeded`; the coordinator dispatches pass 2 (`--pass <N>`, SPEC:85); the pass-2 session ends abnormally before it writes anything (WC-4 writes "on every outcome", but a crash is not an outcome); after state, the worker finds the old file and, by WC-5's rule that only "no report exists" maps to `failed` (SPEC:63), sends `--outcome succeeded` for a pass that never completed. WC-11 says two workers in one worktree never write one file (SPEC:69); SPEC:85 admits "one audit per worktree at a time (WC-11)", SPEC:86 (index-repo, two runs in one worktree write the same index and contract) says nothing, and the carried-over Medium M-11 (`R1:267-269`) is the same effect for the index file. Medium: needs an abnormal end plus a reused path. Recommendation: require the contract of a fixed-path command to be removed or overwritten with `status: failed` at the start of the run, or to carry the run's start time. Priority: Medium.

### M-14 (Medium, MAJOR; origin=changed). The retry clause assumes every command has either a usable resume flag or an output-directory flag

Experts: Fowler (interface consistency), Nygard.

Grading check. An implementer who follows SPEC:73 literally ("either the command's resume flag with the first attempt's directory or, for a command with no resume flag, a new output directory, never the first attempt's") builds the retry brief for `/sc:reflect` by passing its resume flag with the first directory. That would be wrong if the flag does not resume the work: the reflect row says its `--promote-resume` "covers promotion only" and the retry is a "Fresh dir" (SPEC:88). The text allows both readings, and SPEC:64 adds "Section 3 names which applies per command", so the row decides; hence Medium. The same sentence has no case for a command with neither flag: cleanup-audit and index-repo have a fixed output directory and no resume flag (SPEC:85-86, "output dir is fixed"; `mode=update` is not a resume flag), workflow takes no output directory (SPEC:92, "Fresh package each run"), research writes a "fresh file" (SPEC:116). "A new output directory" cannot be passed to them. Adversarial's `--pipeline-resume` works in pipeline mode only (SPEC:83). Recommendation: one clause that the row's "Resume (WC-6)" cell decides, and that a command with no output flag creates its own fresh location. Priority: Medium.

## === ADVERSARIAL ANALYSIS (Whittaker) ===

Attacks applied to the changed text: Zero/Empty (M-15, M-12), Divergence (WC-4 path rules against the rows), Sentinel Collision, Sequence (M-13, B-3 re-check), Accumulation. The full attack text of M-13 and M-15 is in the buckets above. The other attacks found no wrong outcome:

- Divergence at the WC-4 boundary: a file-valued `--output` that is also the report (tdd, SPEC:90) and a directory-valued `--output` (adversarial, SPEC:83) now resolve through different rules, but no input can match both, because the row states which flag shape the command takes. No wrong outcome.
- Sentinel Collision: the name `return-contract.yaml` as a suffix cannot collide with a user file in the file rule, because the suffix is appended to the file name (`<file name>.return-contract.yaml`). No wrong outcome.
- Accumulation: AC-1.1 asserts 14 commands, the P1 row lists 15, and the phase rows cover 37 of 37 non-coordinator-only commands, so no count is lost (see the diagram).
- Sequence (B-3 re-check): attempt 1 blocked in `<dir>`; the retry brief passes `--resume` plus `<dir>` or a new directory (SPEC:73); the attack of `R1:148` has no stated route left.

## === GUARD CONDITION BOUNDARY TABLE === (changed lines only, per `command.md:262`)

Triggered: the changed lines contain guards and thresholds (CMD:313). Constructed by Nygard, completeness checked by Crispin, attacked by Whittaker. Guards on changed lines: G-1 WC-4 contract path selection (SPEC:62, 73, 83-86); G-2 the "known before dispatch" exception (SPEC:62, 73, 92, 182); G-3 AC-1.1 scope (SPEC:195, 159); G-4 AC-1.2 scope and output flag (SPEC:196); G-5 retry predicate (SPEC:64, 73); G-6 AC-3.2 fresh-start predicate (SPEC:205); G-7 P1 flag acceptance (SPEC:159, 76).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G-1 contract path | SPEC:62, 73 | Zero/Empty | brief passes no output directory or file | unknown | not stated (carried-over Medium M-5, `R1:100-102`) | GAP (Medium, carried over) |
| G-1 contract path | SPEC:62 | Typical | `--output <dir>` | default rule | `<dir>/return-contract.yaml` | OK |
| G-1 contract path | SPEC:62 | One/Minimal | `--output <file>` (init-lite, tdd, spec-panel) | file rule | `<file name>.return-contract.yaml` beside the file | OK |
| G-1 contract path | SPEC:62, 83, 85, 86 | Legitimate Edge Case | row names its own path (adversarial, cleanup-audit, index-repo) | exception applies | the row's path | OK |
| G-1 contract path | SPEC:62, 99, 101, 102, 106-108, 111, 123 | Legitimate Edge Case | new output flag whose shape (file or directory) the row does not give | unknown | not stated | GAP (M-12) |
| G-1 contract path | SPEC:85, 86 | Maximum/Overflow (second run reuses the fixed path) | a fixed contract file already exists | overwrite or stale read | not stated | GAP (M-13) |
| G-2 known before dispatch | SPEC:62, 73 | Typical | path derived from the brief's output flag | true | known before dispatch | OK |
| G-2 known before dispatch | SPEC:62, 92 | Legitimate Edge Case | workflow run-time `<id>` | false | worker names the path in `worker_done` | OK |
| G-2 known before dispatch | SPEC:92, 198 | Zero/Empty (no `<id>` yet) | workflow stops before creating its package | undefined | location UNVERIFIED in the row | GAP (M-15) |
| G-2 known before dispatch | SPEC:105, 109, 114-117, 119 | Legitimate Edge Case | rows that name no contract location | unknown | not stated | GAP (M-12) |
| G-3 AC-1.1 scope | SPEC:195, 159 | Typical | command in the P1 row | asserted | section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md` | OK |
| G-3 AC-1.1 scope | SPEC:195, 112 | Zero/Empty (no report file) | `load` | excluded | not asserted | OK |
| G-3 AC-1.1 scope | SPEC:195, 160-162 | One/Minimal | command outside the P1 row (reflect, pr-submit, ...) | not asserted | checked in its own phase | OK |
| G-3 AC-1.1 scope | SPEC:195, 128 | Legitimate Edge Case | section-4 command | asserted absent | no section | OK |
| G-4 AC-1.2 scope | SPEC:196 | Typical | P1 command with a directory output flag | live check with `--output <dir>` | all 7.2 steps pass | OK |
| G-4 AC-1.2 scope | SPEC:196 | Zero/Empty | P1 command with no output flag (index-repo, cleanup-audit, workflow) | flag omitted | "where its row takes one" | OK |
| G-4 AC-1.2 scope | SPEC:196, 87 | Legitimate Edge Case | P1 command whose flag takes a file (init-lite) | placeholder says `<dir>` | not stated | GAP (N-9, minor) |
| G-5 retry predicate | SPEC:64, 73 | Typical | command with a resume flag | true | flag plus first directory | OK |
| G-5 retry predicate | SPEC:64, 73 | One/Minimal | command with an output flag and no resume flag | false | new directory, never the first | OK |
| G-5 retry predicate | SPEC:73, 83, 88 | Legitimate Edge Case | flag that resumes only part of the run (`--promote-resume`, `--pipeline-resume`) | ambiguous | row decides (SPEC:64) but SPEC:73 does not say so | GAP (M-14) |
| G-5 retry predicate | SPEC:73, 85, 86, 92, 116 | Zero/Empty | no resume flag and no output flag | new directory cannot be passed | not stated | GAP (M-14) |
| G-6 AC-3.2 predicate | SPEC:205 | Typical | `<dir2>` copy holds `.session-memory.md`, no resume flag | true | starts fresh in `<dir2>`, no `[Y/n]`, contract written | OK |
| G-6 AC-3.2 predicate | SPEC:205 | Legitimate Edge Case | `<dir>` of attempt 1 | never passed to the run | "not touched" is true by construction | OK (N-11, minor) |
| G-7 P1 flag acceptance | SPEC:159 | Typical | command in the P1 row | accepted | flag accepted, no-op where no gate | OK |
| G-7 P1 flag acceptance | SPEC:159, 112, 76 | Legitimate Edge Case | `load` ("usage line only") | unstated | not stated | GAP (N-8, minor) |
| G-7 P1 flag acceptance | SPEC:159, 100 | One/Minimal | command outside the P1 row (auggie-review) | not accepted in P1 | accepted from P2 | OK |

Left out, with the reason: G-1 Sentinel Value Match (the suffix is appended to a file name, so no user value equals a control value; see the Sentinel Collision attack above); G-2 Maximum/Overflow (no count is involved); G-3 Maximum/Overflow and Sentinel (the set of commands is fixed at 15, no capacity or sentinel); G-4 Maximum/Overflow and Sentinel (same); G-5 Maximum/Overflow (the number of retries is Orca's circuit breaker, `CAPS:116`, not a guard on changed lines) and Sentinel (no sentinel); G-6 Zero/Empty and Maximum (the check names one fixed setup); G-7 Zero/Empty and Maximum (a boolean flag has neither). FR-8, FR-9 and FR-10: every GAP is tied to a finding id; none names a concrete wrong outcome that follows with no further assumption, so each is Medium or minor under the grading check. The table is complete under FR-10 for the seven guards listed.

## Quantity Flow Diagram (Pipeline Dimensional Analysis: the 43-command classification to phase flow)

```text
[Inventories: 21 (INV-A:3) + 22 (INV-B:3)] --> [43 commands, SPEC:76]
   |--> [3.1 ready: 10]      --> P1 6 (adversarial, brainstorm, cleanup-audit, index-repo, init-lite, workflow; SPEC:83-87, 92, 159)
   |                         --> P2 4 (reflect, release-split, tdd, troubleshoot; SPEC:88-91, 160)   = 10 in, 10 out (round 1: 8 out)
   |--> [3.2 needs change: 27] --> P1 9 + P2 11 + P3 4 + P4 3 = 27 in, 27 out
   |--> [section 4: 6]         --> no phase, no mode (SPEC:128)
[P1 row SPEC:159: 15 commands listed = 6 + 9] --> [AC-1.1 asserts the section in 14 (all but load, SPEC:195)]
                                              --> [AC-1.2 live-checks 14 (all but load, SPEC:196)]    no MISMATCH
[Phase totals: 15 (P1) + 15 (P2) + 4 (P3) + 3 (P4) = 37 = 43 - 6 section-4]                            no MISMATCH
```

The CRITICAL mismatch of round 1 (37 asserted against at most 13 edited, `R1:78-88`) no longer exists in the candidate.

## Standard-format summary

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  expert_panel: [Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin]
  focus_areas: [requirements, architecture]
  review: "2 of 3"
quality_assessment:
  overall_score: 6.6
  clarity: 7
  completeness: 6
  testability: 7
  consistency: 6.5
critical_issues: []
prior_blocking:
  - {id: B-1, status: resolved}
  - {id: B-2, status: resolved}
  - {id: B-3, status: resolved}
expert_consensus:
  - "The three blocking findings are repaired by 15 changed lines and no new section."
  - "Remaining gaps are Medium: the shape of new output flags, run-reuse of fixed contract paths, the retry clause for commands without flags, and the workflow pre-creation STOP."
improvement_roadmap:
  immediate: []
  short_term: [M-12, M-13, M-14, M-15]
  long_term: [carried-over Medium findings of round 1]
adversarial_analysis:
  - {methodology: Sequence, severity: Medium, invariant_location: "SPEC:85-86", triggering_condition: "second run of a fixed-path command ends without writing", scenario: "M-13"}
  - {methodology: Zero/Empty, severity: Medium, invariant_location: "SPEC:62, 92", triggering_condition: "workflow stops before a package id exists", scenario: "M-15"}
```

## Carried-over findings (lines unchanged; not re-audited)

M-1 to M-11 and N-1 to N-7 of `R1:24-48` sit on lines that the revision did not touch (the 15 changed lines are listed in the evidence block), so they keep the grades given in round 1 and are not repeated in full. Two interactions with the changed lines, both Medium or lower, are recorded here:

- M-9 (`R1:168-170`): SPEC:159 now limits the P1 flag acceptance to the commands listed in the row, so `/sc:auggie-review` (P2, SPEC:100) no longer accepts `--unattended` in Phase 1. The revision narrowed M-9 as a side effect (`REV:81`); for the example `R1:170` gave, the P1 flag is no longer accepted before its gates are converted. M-9 is not re-graded.
- M-2 (`R1:92-94`): AC-1.2 (SPEC:196) now live-checks brainstorm, whose existing contract keeps its fields (SPEC:62) while step 4 asserts the four-value status set (SPEC:183). Brainstorm's status words are not in the inventories (`INV-A:39`, `INV-A:97` name only the file), so the conflict stays a guess and M-2 stays Medium.

Also from the Reviser contract: the reviser edited SPEC:196 (AC-1.2), which B-1 did not name by line (`R1:65-76` names AC-1.1 and SPEC:159); `REV:40` explains it as the same defect in the neighbouring check. The edit is a narrowing and affects only the `load` exclusion and the output flag clause, so it is a process note, not a finding. No paragraph or table was added, so the "cite the finding id on every addition" duty has nothing to attach to (`REV:26`).

## Coverage

scoped PASS: changed lines + prior blockers

Covered: the 15 changed lines (SPEC:62, 64, 73, 76, 83-87, 92, 159, 182, 195, 196, 205) against the baseline text of the same lines; the lines that depend on them (SPEC:52, 79, 112, 154, 160-162, 198, 225, 240, 261, and the rows of section 3.2 cited above); the three prior blocking findings (`R1:65-150`); the counts of the 43-command flow; `README:1-38`, the inventories at the lines cited above (`INV-A:35, 39, 42, 45, 51, 53, 55, 94-98`; `INV-B:112, 272`), `CMD:1-491` and the review-loop prompts file. The byte totals of `REV:16-24` were re-derived by a character-level diff (1617 added, 41 deleted, net +1576).

Not covered, so UNVERIFIED: every citation of a file outside the workspace (`sk/...`, `cmd/...`, `CLAUDE.md`, `src/superclaude/...`, `.dev/evals/...`, `.dev/codegraph-migration/...`); the claim that `/sc:workflow` prints its package path and where it writes a pre-creation STOP (the row marks both UNVERIFIED); the per-id byte split of `REV:21-23`. Whole-document assurance is not given by this report: lines the revision did not change were not re-graded, and a gate review is a separate, labelled first review (see Next step).

Steps not run: the Improve step (Behavioral Flow step 6) and TDD/PRD scoping (6a-6d), because `--re-review` skips Improve (`command.md:261`) and the brief assigns this single output file. `--iterations` was ignored for the same reason. No Reviser step was run.

Brief clauses overridden: none. The follow-up question (whether to open an issue for the Medium and minor findings) was not asked in this worker run, which has no user to ask, and no issue was created.

## Follow-up candidates

Medium (new): M-12, M-13, M-14, M-15.
Medium (carried over, unchanged): M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9 (narrowed by SPEC:159), M-10, M-11.
Minor (new): N-8, N-9, N-10, N-11, N-12.
Minor (carried over, unchanged): N-1, N-2, N-3, N-4, N-5, N-6, N-7.

Medium and minor findings never trigger a revision and are not in the Reviser brief.

## Next step

This is a scoped re-review. Per `~/.claude/rules/prompts/document_review_loop_prompts.md:57-64` the coordinator now runs the GATE prompt once, as a separate first review of the whole document in a fresh context that has seen no report of this loop; this report does not start it and does not count toward its numbering.

## Reviser brief

Blocking finding ids: none. No revision is requested. For any later brief that uses this report: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding and report the byte size before and after, with the bytes added and deleted per finding id; Medium and minor findings are not part of any brief and a brief cannot make one of them blocking.

verdict: PASS
