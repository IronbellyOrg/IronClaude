review: 2 of 3

# Spec-panel re-review: orca-worker-contract-spec, round 2

## Header
- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md` (re-review, `cmd:258`).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, SHA-256 `ba714118121e521fcaa6d0492fe49f39e1fe607a6399a97a6d4b5fc9f802ffdb`.
- Baseline: `.dev/orca-command-refactor/specs/history/spec-v1.md`, SHA-256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`.
- Prior report: `.dev/orca-command-refactor/review/round1.md`, SHA-256 `d27771185d14246478f25e581cb430a6fc7ea596780d320a0f5e8400dd32b62a`. Its header reads 1 of 3 (`r1:1`), so this is review 2 of 3 (`cmd:261`). The cap allows one more fix cycle after this review (`cmd:261`).
- Reviewer model actually used: `claude-haiku-5-5`.
- Citation shorthand: `spec:N` = candidate line N; `r1:N` = round1.md line N; `cmd:N` = command.md line N; `prompts:N` = `~/.claude/rules/prompts/document_review_loop_prompts.md` (sandbox home) line N; `README:N` = README.md line N.

## Coverage
- Read in full: `command.md` (491 lines), `prompts` (56 lines), `README.md` (39 lines), `round1.md` (151 lines), the candidate (285 lines), and `diff -w` of the baseline against the candidate.
- Not present in the sandbox: `~/.claude/WORKER-CONTRACT.md` (not needed, because this run passes no `--unattended`, `cmd:457`); `.claude/agents/rf-qa.md` and `~/.claude/agents/rf-qa.md` (the fix-cycle steps 1-5 named at `cmd:262` could not be read, so the rules in this report stand alone, as `cmd:262` allows).
- Inventories under `inventory/` were not re-read. No changed line adds an inventory citation: the eight hunks cite only spec sections, prior finding ids and the prior report.
- Scope: changed lines only, plus unchanged text where it quotes a changed line (`cmd:262`, `cmd:259`). Medium findings from round 1 were not re-graded; they are listed as carried.

## Step 1 evidence block

Command run: `diff -w BASELINE CANDIDATE` (exit 1). Changed hunks: 62c62, 64c64, 73c73, 76c76, 79c79, 147c147, 172c172, 195c195. Self-check (`prompts:45`): 16 of 16 quoted lines were found, each BEFORE line in the baseline and each AFTER line in the candidate, so no role was swapped.

### BEFORE (baseline), lines starting with `<`
```text
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
< | WC-6 | **Resume or safe re-run.** A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output. A command either resumes from its on-disk state when given its resume flag, or, if it has none, writes each run into a fresh output directory so a re-run starts clean. Section 3 names which applies per command. | Command | `CAPS:116` (retry and circuit breaker); resume mechanisms in column (e) of `INV-A:35-55`, `INV-B:31-52` |
< The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
< The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
< These run as workers now if the brief uses the stated flags; the worker reports the named file until Phase 1 adds the contract. The only command changes are the small fixes in the last column.
< | SA-2 | No command, skill or agent file runs an `orca` or `orca-ide` command, and none requires Orca to be installed or running. The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file. | Commands run in other projects (`CLAUDE.md:74`); without Orca the calls fail with `runtime_unavailable` (`CAPS:147`). | `CAPS:145-149`; today's baseline: only `sk/ccsession-tag/` mentions Orca (section 1.2, E5) |
< | AC-C1 | `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \| grep -v '^src/superclaude/skills/ccsession-tag/'` | prints nothing (SA-2, WC-8) |
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
```

### AFTER (candidate), lines starting with `>`
```text
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). A retry gets a new directory from the coordinator, so the coordinator reads the contract of the attempt it last dispatched (F-02). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
> | WC-6 | **Resume or safe re-run.** A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output. A command either resumes from its on-disk state when given its resume flag, or, if it has none, runs in the output directory the coordinator passes; the coordinator passes a new directory for each retry, so a re-run starts clean (F-02). In unattended mode the command never chooses its own output directory (F-02). Section 3 names which applies per command. | Coordinator picks the retry directory (F-02); command resumes | `CAPS:116` (retry and circuit breaker); resume mechanisms in column (e) of `INV-A:35-55`, `INV-B:31-52` |
> The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4), and a new one for each retry (WC-6, F-02); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
> The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. "Fresh dir" in the resume column means the coordinator passes a new `<output-dir>` for a retry (WC-6, F-02). Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
> These run as workers now if the brief uses the stated flags; the worker reports the named file until Phase 1 adds the contract. The only command changes are the small fixes in the last column, plus the `--unattended` flag and the `## Unattended mode` section, which Phase 1 adds to all 37 commands in sections 3.1 and 3.2, including ready commands whose small fix is "None" (F-03). Every one of them except `load` also names the WC-4 contract; `load` writes none (its row and the Decisions table).
> | SA-2 | No command, skill or agent file runs an `orca` or `orca-ide` command, and none requires Orca to be installed or running. The only allowed mention of Orca is in the core contract file, as an example of a caller's question channel, and in the routing guide's Orca section (SA-5) (F-01). No changed command, skill or agent names Orca. | Commands run in other projects (`CLAUDE.md:74`); without Orca the calls fail with `runtime_unavailable` (`CAPS:147`). | `CAPS:145-149`; today's baseline: only `sk/ccsession-tag/` mentions Orca (section 1.2, E5) |
> | AC-C1 | `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents \| grep -v '^src/superclaude/skills/ccsession-tag/'` | prints nothing (SA-2, WC-8). Core files are not scanned because the contract file and the routing guide name Orca by design (F-01, SA-2, SA-5) |
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `load` has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, that `load`'s section names no contract (F-03), and that no section-4 command has one | passes |
```

## Prior blocking findings (`r1:34-51`)

| ID | Round-1 grade | Status | Basis |
|---|---|---|---|
| F-01 | blocking | resolved | AC-C1 (`spec:172`) now scans commands, skills and agents only. SA-2 (`spec:147`) names the core contract file and the SA-5 routing guide (`spec:150`) as the allowed Orca mentions, so the P0 gate (`spec:158`) no longer requires a grep that fails on them. Residual weakness: N-03. |
| F-02 | blocking | resolved as stated | The owner conflict is gone. WC-4 (`spec:62`) reads the contract of the last-dispatched attempt, WC-6 (`spec:64`) gives the directory to the coordinator, and 2.3 (`spec:73`) states a new directory per retry. The new per-retry text opens N-01. |
| F-03 | blocking | resolved | `spec:79` gives the flag and the section to all 37 commands in 3.1 and 3.2 (10 rows at `spec:83-92` plus 27 rows at `spec:99-125`, with `load` in 3.2). `load` is exempt at `spec:112`, `spec:195` and `spec:265`, and AC-1.1 (`spec:195`) matches. Residual: N-02 (flag timing) and N-04 (exemption against WC-4). |

No prior resolved finding fails again, so there is no `regressed` row.

## Findings on lines changed against the baseline

### N-01 BLOCKING (origin=changed; `spec:62`, `spec:64`, `spec:73`, `spec:76`)
The new-directory-per-retry rule contradicts the resume rule.
- Texts: WC-6 (`spec:64`) says a command "either resumes from its on-disk state when given its resume flag, or ... runs in the output directory the coordinator passes; the coordinator passes a new directory for each retry". WC-4 (`spec:62`) says "A retry gets a new directory from the coordinator". 2.3 (`spec:73`) says "a new one for each retry". Only the gloss at `spec:76` limits new directories to "Fresh dir" rows.
- Resume rows that need the first attempt's directory: adversarial `--pipeline-resume` (`spec:83`); cleanup-audit `progress.json` checkpoint in a fixed output dir (`spec:85`); brainstorm `--resume-from` (`spec:84`); tdd `--resume <task-file>` (`spec:90`); cli-portify `--resume <contract>` (`spec:105`); implement `--resume` (`spec:109`); pr-submit `--resume <run-log.jsonl>` (`spec:114`); roadmap explicit resume (`spec:118`).
- Sentence: An implementer who follows `spec:64` and `spec:73` gives a retry of `/sc:pr-submit --resume <run-log.jsonl>` (`spec:114`) a new output directory. The run log the resume flag reads is not there, so the run starts from zero and the first attempt's state is left behind. That is wrong because the Resume column and WC-6's first clause say the retry continues from that state.
- Grade: blocking. Two stated texts contradict for every resume-flag row, and an implementer following either text produces the wrong retry (`prompts:31`).
- Whittaker, sequence attack: "I can break this specification by **Sequence Attack**. The invariant at **WC-6 (`spec:64`)** fails when **a retry is dispatched to a command whose resume flag reads the first attempt's directory**. Concrete attack: `/sc:cleanup-audit` fails after its checkpoint is written (`spec:85`); the coordinator's retry gets a new `<output-dir>` per `spec:73`; the command finds no `progress.json`, restarts the pass from zero, and the first attempt's checkpoint is orphaned."
- For the reviser: scope the new-directory rule to rows whose Resume column is "fresh dir", and state that the coordinator passes the same directory together with the resume flag for every other row.

### N-02 BLOCKING (origin=changed; `spec:73`, `spec:79`, `spec:158`, `spec:180`, `spec:194`)
P0 cannot run as written.
- Texts: 2.3 (`spec:73`) says each brief states "the exact command line including `--unattended`". `spec:79` says the `--unattended` flag "which Phase 1 adds to all 37 commands". P0 (`spec:158`) runs "the 10 ready commands" as real workers before any command edit. The live check 7.2 step 1 (`spec:180`) builds its brief from 2.3. AC-0.4 (`spec:194`) runs `/sc:troubleshoot`, `/sc:workflow --handoff none` and `/sc:adversarial --output` in P0.
- Sentence: An implementer who follows `spec:73` puts `--unattended` into the P0 briefs. The three P0 commands do not accept it until P1 adds it (`spec:159`), so AC-0.4 steps 2 and 5 (`spec:181`, `spec:184`) check an unattended path that does not exist, and AC-0.4 cannot pass as written. An implementer who drops the flag to satisfy P0 breaks 2.3, and then the P0 run is not unattended at all.
- Grade: blocking, because an acceptance criterion cannot pass as written (`prompts:31`).
- For the reviser: either move the flag into P0 for the three P0 commands, or let 2.3 omit `--unattended` for P0 runs and say so in P0.

### N-03 MEDIUM (origin=changed; `spec:147`, `spec:172`)
- SA-2 (`spec:147`) ends "No changed command, skill or agent names Orca." AC-C1 (`spec:172`) matches only `orca(-ide)?` followed by orchestration, worktree, terminal or agent. A changed command that names Orca in any other form passes AC-C1 while breaking SA-2's last sentence.
- SA-2 also says "The only allowed mention of Orca is in the core contract file ... and in the routing guide's Orca section". The baseline mention in `sk/ccsession-tag/` (`spec:25`, E5) is excluded only by AC-C1 and no requirement addresses it. Read literally, SA-2 forbids it.
- Grade: Medium. Each reading needs a guess about what SA-2 means, and no single clear reading produces a wrong build (`prompts:31`).

### N-04 MEDIUM (origin=changed; `spec:79`, `spec:195`; against unchanged `spec:62`)
- WC-4 (`spec:62`, unchanged) says that in unattended mode "the command writes `<output-dir>/return-contract.yaml`" and that it is "written on success, failure, blocked and partial outcomes". `spec:79` (changed) says `load` "writes none", and AC-1.1 (`spec:195`) and the Decisions table (`spec:265`) exempt it. The intent is clear (`load` runs inside another worker's brief, `spec:112`, `spec:265`), but the spec never says that WC-4 yields to the exemption.
- Grade: Medium. It is a textual precedence gap, and no dispatched Task is affected because `load` is not run as its own Task (`spec:112`).

### M-03 MEDIUM, carried from round 1, sharpened by `spec:64` (origin=changed)
- The new sentence "In unattended mode the command never chooses its own output directory" (`spec:64`) combined with WC-4 (`spec:62`) leaves an unattended run with no `--output` or `--output-dir` without a defined outcome: refuse, fail, or use a default. The revision does not state one. A requirement the document never states is Medium (`prompts:31`).

## Guard Condition Boundary Table (changed guards only, `cmd:309-317`)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-6 retry directory | spec:64, spec:73 | One/Minimal: retry of a command whose resume flag is set | same directory needed | true | new directory passed; resume finds no state | GAP (N-01, blocking) |
| WC-6 retry directory | spec:64, spec:76 | Typical: retry of a "Fresh dir" command | new directory | true | starts clean | OK |
| WC-4 retry contract | spec:62 | Typical: coordinator reads after a retry | last dispatched attempt | true | reads that attempt's contract | OK |
| WC-4 output directory | spec:62, spec:64 | Zero/Empty: unattended run, no directory passed | no directory | true | not stated | GAP (M-03, Medium) |
| P0 brief flag | spec:73, spec:79, spec:158 | Zero/Empty: P0 run, flag not yet accepted | `--unattended` in brief, flag absent in command | true | not stated; AC-0.4 cannot pass | GAP (N-02, blocking) |
| SA-2 scope | spec:147, spec:172 | Sentinel Value Match: changed command names Orca in a form the grep does not match | "names Orca" | true | AC-C1 passes; SA-2 forbids it | GAP (N-03, Medium) |
| Load exemption | spec:79, spec:195 | Legitimate Edge Case: `load` under `--unattended` | no contract | true | exempt by `spec:79` against WC-4 | GAP (N-04, Medium) |
| Load section check | spec:195 | Legitimate Edge Case: `load`'s section | no contract named | false | must name no contract | OK |

Input classes left out (`cmd:317`, FR-10): Maximum/Overflow is omitted for WC-4 and WC-6 because the changed lines contain no count or capacity. Sentinel Value Match is omitted for the retry-directory guard because no sentinel value appears in the changed lines. Legitimate Edge Case for the retry guard is covered by the load row. The table is complete under FR-10.

## Whittaker probes (active in every review)
- Sequence attack on retry: N-01.
- Zero-directory attack on unattended runs: M-03 (no outcome for a missing directory).
- Divergence attack on the `load` exemption: N-04.
- Count check: 10 ready + 27 needing change = 37 commands with the new flag (`spec:79`), matching the rows at `spec:83-92` (10) and `spec:99-125` (27). The 43-command total (`spec:76`) reconciles.

## Consensus and disagreement
- Consensus: the F-01 and F-03 fixes hold, and the F-02 owner conflict is removed. The count reconciles.
- Disagreement: none new. Round 1's tasklist disagreement (M-06) is still unrecorded in the spec.

## Priority-ranked improvements
1. N-01: scope the new-directory rule to fresh-dir rows (blocking).
2. N-02: make P0 consistent with the flag timing (blocking).
3. N-03, N-04 and M-03: follow-up candidates.

## Carried Medium and minor findings (round 1, not re-graded, not in the Reviser brief)
- Medium, unchanged by the revision, no changed line depends on them: M-01 (`spec:88,122,151`), M-02 (`spec:60-61,97`), M-04 (`spec:111,277`), M-05 (2.3 at `spec:73` still lists no upstream report paths), M-06 (`spec:122`), M-07 (`spec:59,61,68-70`), M-08 (`spec:176`).
- Minor, unchanged: m-01 to m-05 (`r1:137-141`).

## Follow-up candidates (Medium and minor; not in the Reviser brief)
- N-03, N-04, M-03, and the carried M-01 to M-08 and m-01 to m-05 above.
- Per `cmd:259` and `prompts:31`, the coordinator asks the user once per loop whether to open issues for these. No issue has been created.

## Reviser brief
Blocking finding ids: N-01, N-02.

Restated bullet 6 (`cmd:263`): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not revised here, and no PASS is awarded.

verdict: FAIL
