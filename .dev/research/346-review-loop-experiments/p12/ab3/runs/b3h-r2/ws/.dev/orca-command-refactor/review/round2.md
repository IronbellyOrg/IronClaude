review: 2 of 3

# Spec-panel critique, round 2 (re-review): orca-worker-contract-spec.md

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (290 lines)
- candidate sha256: `7f3af35e63f12d24d6eebc453c30497ba2705a10886e04c84b5f7497272961d3`
- baseline: `.dev/orca-command-refactor/specs/history/spec-v1.md` (285 lines), sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (the text round 1 reviewed)
- prior: `.dev/orca-command-refactor/review/round1.md` (review: 1 of 3), sha256 `6c4ae9e12a3bc7517edaa49caee362e4c1e587406e0dcf5f665cc0fae66a082c`
- brief: RE-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md`, sha256 `0bf6d28fbffb08a2ce62010bdabda114a80065090d9fb4fc24beaa06471e7408`
- mode and focus: `--mode critique --focus requirements,architecture --re-review` with `--baseline`
- review number: N = 1 + 1 = 2
- reviewer model: claude-haiku-5-5
- evidence limits: checkable here are the README, the three inventories, the candidate, the baseline, round 1 and the command and prompt files. Citations into `src/`, `sk/`, `cmd/`, `.dev/evals/` and the Orca guides are UNVERIFIED; where an inventory line quotes one, I cite the inventory line.

Citation shorthand: `SPEC:N` = line N of the candidate; `BASE:N` = line N of the baseline; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of the inventories; `R1:N` = line N of round 1.

## Coverage

- Read in full: the `/sc:spec-panel` command file, the review-loop prompts file, README, the candidate, the baseline, round 1.
- Read in part: `INV-A:33-68` and `INV-B:265-276` (the rows and notes behind the changed commands), `INV-A:51-52`, `INV-A:55`, `INV-A:60`, `INV-A:66`, `INV-B:31`, `INV-B:52`, `INV-B:272`.
- Hashes: the candidate, baseline and prompts hashes were taken by `sha256sum` and match the values in the header. The round 1 hash of the candidate in `R1:6` equals the baseline hash above, which confirms that round 1 reviewed the baseline text.
- Step 1 self-check: every changed line on both sides was grepped with `grep -qxF` in its own file (AFTER lines in the candidate, BEFORE lines in the baseline). All were found. No quote failed, so the roles are not swapped.
- AC-C1 as revised (SPEC:178-181) was run on a sample line: `orca orchestration task-create` matched, exit 0.
- Not checked: `CAPS:` lines and every citation into `src/`, `sk/` and `cmd/`. Those stay UNVERIFIED here.

## Step 1: evidence block

Command: `diff -w BASELINE CANDIDATE`. Lines are copied verbatim from its output.

BEFORE (baseline):

```text
< | WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag. On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11) |
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
< | WC-11 | **Parallel-safe writes.** Two workers in one worktree must never write the same file. Default output paths carry a timestamp or the slug the coordinator passes; single-owner shared files (for example memory keys overwritten whole) are not written in unattended mode. | Command | `cmd/save.md:42-45`; `CAPS:115` (`[G:placement]` lines 8-11: workers share the current worktree by default) |
< The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
< | index-repo | none | `PROJECT_INDEX.md` (location implied) | `mode=update` | State the output location (P1) | `cmd/index-repo.md:72,140-144,170-173`; `INV-A:53` |
< | init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report | None | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
< | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
< | load | no gate | none (see note) | n/a | none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |
< | validate-tests | no gate | give the skill a way to write the `--report` file (it has neither Write nor Bash) | n/a | fix the default target `tests/sc-task/`, which does not exist | `cmd/validate-tests.md:6,22,33`; `sk/sc-validate-tests-protocol/SKILL.md:4`; `INV-B:51,257-265` | P3 |
< | SA-3 | The new contract file and report files are written only in unattended mode or when the caller passes the new output flag. A standalone default run writes the same files it writes today. | A new file appearing in a person's working tree is a visible change. | Section 3 rows that add a report path |
< | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
< | AC-C1 | `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \| grep -v '^src/superclaude/skills/ccsession-tag/'` | prints nothing (SA-2, WC-8) |
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
```

AFTER (candidate):

```text
> | WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag. A gate that needs a human Ruling (implement `E-HALT-QA` and `E-NO-RULING`, section 3.2) never takes a coordinator answer as a flag and resolves as blocked (F-03; INV-A:51-52 and INV-A:66 quote the Ruling rule). On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11) |
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes its contract to the path that WC-4 or its section 3 row names, and the brief states that exact path (F-01). The default is `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). Two named exceptions: adversarial writes `<output>/adversarial/return-contract.yaml` (INV-A:35), and workflow writes `<dir>/return-contract.yaml` under its new `--output <dir>` flag (INV-B:52, INV-B:272). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
> | WC-11 | **Parallel-safe writes.** Two workers in one worktree must never write the same file. Default output paths carry a timestamp or the slug the coordinator passes; single-owner shared files (for example memory keys overwritten whole) are not written in unattended mode. The coordinator never gives two workers the same output path (F-07; section 2.3). | Command | `cmd/save.md:42-45`; `CAPS:115` (`[G:placement]` lines 8-11: workers share the current worktree by default) |
> The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file at the path WC-4 gives for that command (F-01). Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
> | index-repo | `--output-dir <unique dir>` under `--unattended` (new flag, F-07) | `PROJECT_INDEX.md` (location implied) | `mode=update` | Add `--output-dir` (default unchanged); under `--unattended` both `PROJECT_INDEX.md` and `PROJECT_INDEX.json` go in the brief's unique directory, so two workers never share them (F-07, WC-11; P1) | `cmd/index-repo.md:72,140-144,170-173`; `INV-A:53` |
> | init-lite | `--output <file>` (under `--unattended`, unique per worker and attempt, F-05, F-07) | `.dev/superclaude/context-audit.md` or `--output` | Fresh file per attempt: a `--retry-of` brief passes a new `--output` path, so the first attempt's report is kept (F-05, WC-6) | Under `--unattended`, the contract goes beside the `--output` file (`<output-dir>` is that file's directory, WC-4), and each worker's own directory keeps two workers from sharing `context-audit.md` (F-07, WC-11) (P1) | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
> | workflow | `--handoff none`; `--output <dir>` under `--unattended` (new flag, F-01) | `.dev/tasks/to-do/<id>/return-contract.yaml` (post-creation only, INV-B:272) | Fresh package each run | Under `--unattended`, `--output <dir>` writes `<dir>/return-contract.yaml` on every outcome, including pre-creation STOPs (WC-4, F-01); the package copy is unchanged (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
> | load | no gate | none (F-02: no Task, so no contract; see note) | n/a | none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |
> | validate-tests | no gate | give the skill a way to write the `--report` file (it has neither Write nor Bash) | n/a | fix the default target `tests/sc-task/`, which does not exist; under `--unattended` the contract goes at `<dir of --report>/return-contract.yaml` (F-02) | `cmd/validate-tests.md:6,22,33`; `sk/sc-validate-tests-protocol/SKILL.md:4`; `INV-B:51,257-265` | P3 |
> | SA-3 | The new contract file and report files are written only in unattended mode or when the caller passes the new output flag. A standalone default run writes the same files it writes today, with one exception: the adversarial contract path that section 3.1 pins (F-04). Its nested `adversarial/adversarial/` variant (INV-A:60) is removed as a defect fix under SA-4. The other section 3 changes add files only under `--unattended` or a new flag (workflow's `--output` contract, index-repo's `--output-dir`), and the cleanup-audit row only names a file, with no change to what is written. | A new file appearing in a person's working tree is a visible change. | Section 3 rows that add a report path |
> | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, init-lite (F-05), workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
> | AC-C1 | the scan in the block below, which covers `src/superclaude/{commands,skills,agents}` only (SA-2; `core` is excluded because P0 adds an Orca section to `HOW-WE-WORK.md`, F-06) | prints nothing (SA-2, WC-8). Positive control (F-06): `tests/skills/test_worker_contract.py` asserts that the same pattern matches the fixture line `orca orchestration task-create` |
> ```bash
> # AC-C1 scan (F-06): ERE alternation uses a bare `|`; the table cell cannot carry it
> grep -rnE '\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents | grep -v '^src/superclaude/skills/ccsession-tag/'
> ```
> 
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `~/.claude/WORKER-CONTRACT.md`, that each of them except `load` also names `return-contract.yaml` (F-02: load has no Task and no contract, see its section 3.2 row), and that no section-4 command has one | passes |
```

The diff has 12 hunks: SPEC:61-62 (WC-3, WC-4), SPEC:69 (WC-11), SPEC:76 (section 3 intro), SPEC:86-87 (index-repo, init-lite), SPEC:92 (workflow), SPEC:112 (load), SPEC:125 (validate-tests), SPEC:148 (SA-3), SPEC:159 (P1), SPEC:172 and SPEC:178-181 (AC-C1 and its scan block), SPEC:200 (AC-1.1).

## Prior blocking findings (from R1)

| R1 id | Status | Basis (AFTER text only, except where a prior line is quoted) |
|---|---|---|
| F-01 | resolved | WC-4 (SPEC:62) now states the default `<output-dir>/return-contract.yaml` and names two exceptions: adversarial `<output>/adversarial/return-contract.yaml` (INV-A:35) and workflow `<dir>/return-contract.yaml` under its new `--output <dir>` flag (INV-B:52, INV-B:272). The adversarial row (SPEC:83), workflow row (SPEC:92) and the section 3 intro (SPEC:76) agree with it. The rule is stated once. Residual: SPEC:105 (cli-portify) still says "file location unnamed"; see R2-06. |
| F-02 | open (narrowed) | Fixed in AC-1.1 (SPEC:200), which now exempts `load` from naming `return-contract.yaml`, and in the validate-tests row (SPEC:125), which now gives it a contract. Still open: WC-4 (SPEC:62) says the command in section 3 "writes its contract ... written on every outcome" with no `load` exception. The load row (SPEC:112) says "none (F-02: no Task, so no contract ...)" and SPEC:265 (baseline text, unchanged) says a report file "would be an unrequested addition". Two stated texts contradict. |
| F-03 | resolved | WC-3 (SPEC:61) now says a gate that needs a human Ruling (implement `E-HALT-QA` and `E-NO-RULING`) "never takes a coordinator answer as a flag and resolves as blocked". The implement row (SPEC:109) and non-goal 6 (SPEC:218) agree. The quoted rule is at INV-A:51 and INV-A:66, both checked. Residual citation error: see R2-04. |
| F-04 | resolved | SA-3 (SPEC:148) now names the adversarial path as the one exception to "writes the same files it writes today" and cites SA-4. SA-4 (SPEC:149) lists "adversarial and workflow contract gaps" as defect fixes. INV-A:60 records two real paths on disk, which is the documented defect. |
| F-05 | open (narrowed) | The init-lite row (SPEC:87) now gives "Fresh file per attempt: a `--retry-of` brief passes a new `--output` path". WC-6 (SPEC:64) still requires that a re-run "writes each run into a fresh output directory". A new file in the same directory is a fresh file but not a fresh directory, and WC-4 (SPEC:62) puts the contract at `<output-dir>/return-contract.yaml`, which is the same path for both attempts. The retry therefore replaces attempt 1's contract, which WC-6 forbids. Two stated texts contradict. |
| F-06 | resolved | AC-C1 (SPEC:172, SPEC:178-181) now uses a bare `\|`-free alternation `(orchestration|worktree|terminal|agent)`, and the sample check matched. Its scope is `src/superclaude/{commands,skills,agents}`, which matches SA-2 (SPEC:147). The core file is excluded, which removes the P0 scope conflict. The positive control is named (SPEC:172) and is created in P0 (SPEC:158). |
| F-07 | resolved | index-repo (SPEC:86) and init-lite (SPEC:87) now write to a unique directory under `--unattended`. WC-11 (SPEC:69) adds the coordinator rule. Residual: WC-11 cites section 2.3 for that rule, and section 2.3 (SPEC:73) does not state it; see M2-02. |

Regressed: none. Every prior blocking finding is resolved, open or regressed, and none is listed as regressed.

Open blocking findings after this review: F-02, F-05.

## Findings on changed lines

Each finding is on a changed line (origin=changed). Grades follow the FIRST-REVIEW grading check. None of these is blocking.

- R2-01 (Medium, origin=changed, SPEC:86, index-repo row). The Resume column still says `mode=update` (INV-A:53 says "`mode=update` updates an existing index"). Under `--unattended` the output moves to a brief-supplied unique directory. The row does not say where `mode=update` reads the prior index from. An implementer who follows the row either updates an empty directory or reads the repo-root copy, and the row does not say which. Grading sentence: an implementer who follows SPEC:86 has no stated input path for update, so the result is a guess. Recommendation: state the input path for update in the row.
- R2-02 (Medium, origin=changed, SPEC:69 WC-11 and SPEC:85 cleanup-audit row). WC-11 says "The coordinator never gives two workers the same output path (F-07; section 2.3)". Section 2.3 (SPEC:73) does not state that rule. The cleanup-audit row (SPEC:85) gives a fixed output dir and "one audit per worktree at a time (WC-11)", which is a coordinator obligation that appears only in a row. Recommendation: add the same-path and one-at-a-time rules to section 2.3.
- R2-03 (Medium, origin=changed, SPEC:61 WC-3 against SPEC:235 D2(b), SPEC:208 AC-4.1 and SPEC:218 non-goal 6). WC-3 now states "never" for the implement Ruling. D2 option (b) (SPEC:235) would allow a relayed Ruling, and AC-4.1 (SPEC:208) is written with "unless D2 allows a relayed one". Today there is no contradiction because D2 is open. If the user picks (b), WC-3 must be rewritten. Recommendation: say in D2 that choosing (b) rewrites WC-3 and AC-4.1.
- R2-04 (Minor, origin=changed, SPEC:61). WC-3 cites "INV-A:51-52" for the Ruling rule. INV-A:52 is the improve row, and the rule is at INV-A:51 (quoted at refs/qa.md:238) and INV-A:66. Recommendation: change the citation to INV-A:51 and INV-A:66.
- R2-05 (Medium, origin=changed, SPEC:62 WC-4 zero input). WC-4 does not say what an unattended run without `--output` or `--output-dir` does. This was round 1 M-12, which is carried here because it sits on a changed line. Recommendation: resolve such a run as blocked, as M-12 proposed.
- R2-06 (Minor, origin=unchanged, SPEC:105 cli-portify row). The row still says "file location unnamed". WC-4 now names the default. This line is unchanged, so it is a note.

Carried, not re-graded: round 1 items M-01 to M-19 sit on unchanged lines (origin=unchanged) and remain follow-up candidates. They are not re-graded here, except M-12 (see R2-05).

## Mandatory output artifacts (changed guards only)

Covered: the guard conditions on changed lines, per FR-8 to FR-10. The guard list is limited to rows and clauses this review changed.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-3 Ruling gate | SPEC:61, SPEC:109 | Sentinel Value Match | implement `E-NO-RULING`, coordinator answer present | not taken as a flag | blocked (stated) | OK |
| WC-3 Ruling gate | SPEC:61 | Typical | non-Ruling gate, coordinator answer present | re-invoke with the answer as a flag | stated | OK |
| WC-4 output dir | SPEC:62 | Zero/Empty | `--unattended` without `--output` or `--output-dir` | n/a | not stated (R2-05) | GAP, Medium |
| WC-4 path | SPEC:62 vs SPEC:112 | Zero/Empty | `load`, no contract | n/a | WC-4 requires one; load row says none (F-02) | GAP, F-02 |
| WC-4 path | SPEC:62 vs SPEC:83 | Typical | adversarial `--output D` | `D/adversarial/return-contract.yaml` | stated | OK |
| WC-6 retry | SPEC:87 vs SPEC:64 | Typical | `--retry-of` with a new `--output` file in the same directory | same `return-contract.yaml` path | WC-6 requires a fresh output directory (F-05) | GAP, F-05 |
| WC-11 index-repo | SPEC:86 | Typical | two index-repo workers, unique dirs | no shared path | stated | OK |
| SA-3 adversarial | SPEC:148, SPEC:83 | Typical | standalone adversarial run | renamed contract | exception stated | OK |
| AC-C1 scan | SPEC:172, SPEC:180 | Legitimate Edge | `orca orchestration task-create` in a command file | match | matches (tested) | OK |
| AC-C1 scan | SPEC:172 | Sentinel | `orca-ide worktree` in `src/superclaude/core` | excluded | scope stated | OK |

Pipeline Dimensional Analysis: not triggered by this review. The fan-in text (SPEC:39) did not change.

## Follow-up candidates (Medium and minor; not blocking; not in any reviser brief)

The coordinator asks the user once whether to open an issue for these. No issue has been created.

- R2-01 to R2-06 (above).
- M-01 to M-19 from round 1, unchanged lines, carried as they were.

## Decisions (this worker)

| Decision | Options | Rationale |
|---|---|---|
| F-02 and F-05 graded open rather than resolved | (1) resolved, because AC-1.1 and the rows now agree; (2) open, because WC-4 and WC-6 still contradict the row text | (2). The grading check asks for two stated texts that contradict, and both pairs still do. The fix is narrow, so the reviser's work is small. |
| F-07 graded resolved | (1) open, because of the section 2.3 cross-reference; (2) resolved, with the cross-reference as Medium | (2). The duplicate-output risk the finding named is removed on the rows that caused it, and the cross-reference is a documentation defect. |
| R2-01 graded Medium, not blocking | (1) blocking, because update's input is unstated; (2) Medium, because the spec does not say which reading applies and the rule does not require a guess | (2). It is a guess between two readings, so it is Medium under the rule. |
| Review number | 2 of 3, from the prior header `review: 1 of 3` | As the RE-REVIEW prompt says. |

## Reviser brief

Blocking findings to revise: F-02, F-05.

Restating the reviser contract (this review's bullet 6): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; the reviser prefers deleting or narrowing to adding and reports the byte size before and after, with the bytes added and deleted per finding id.

Suggested narrowest repairs (for the reviser to check, not a mandate): F-02: one sentence in WC-4 that a command with no Task (`load`) writes no contract, matching SPEC:112 and AC-1.1. F-05: change the init-lite row to require a fresh output directory per attempt, matching WC-6.

verdict: FAIL
