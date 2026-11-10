review: 2 of 3

# Spec-panel review, round 2 (re-review): Orca worker-contract spec

| Header field | Value |
|---|---|
| command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md` |
| candidate (CANDIDATE) | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 285 lines, 59765 bytes |
| candidate sha256 | `cf9b3e748906ea7675896ba4ee5a7993c98b0ab7a8ec22a0e9311df04e7ebb69` |
| baseline (BASELINE) | `.dev/orca-command-refactor/specs/history/spec-v1.md`, 285 lines, 57763 bytes |
| baseline sha256 | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (equals the candidate hash recorded in round 1, `r1:9`) |
| prior (PRIOR) | `.dev/orca-command-refactor/review/round1.md`, header `review: 1 of 3`, final line `verdict: FAIL` |
| prior sha256 | `c05c1cba340bfc5272f7f7cdbc0d6141034661afda386add6cd36228c27db523` |
| reviewer model actually used | `claude-sonnet-5-5` (Sonnet 5.5) |
| prompt followed | RE-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:34-47`, read in full before this review (hard gate, `cmd:266-268`); N = 1 + 1 = 2 |
| date | 2026-11-10 |
| `--unattended` | not passed; no `return-contract.yaml` is written (`cmd:459`) |
| revised spec | none written: `--re-review` skips the Improve step (`cmd:261`); the candidate is not edited |
| rf-qa Fix Cycle steps 1-5 (`cmd:262`) | `.claude/agents/rf-qa.md` and `~/.claude/agents/rf-qa.md` are not in the sandbox, so the file was not read; the rules of `cmd:256-264` were applied on their own, as `cmd:262` allows |

Citation keys: `spec:N` = line N of the candidate. `v1:N` = line N of the baseline. `r1:N` = line N of PRIOR. `rev1:N` = line N of `review/revise1.md` (the reviser's report; read as a claim, not as evidence). `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`. `cmd:N` = line N of the sandbox `command.md`. `prompts:N` = line N of the review-loop prompts file. A citation to a file that is not in the sandbox (`src/`, `CLAUDE.md`, `EVIDENCE.md`, Orca binaries) is UNVERIFIED; the spec, the three inventories and the files above are the only evidence I could check.

Brief clauses overridden: none. The brief narrowed nothing and widened nothing (`cmd:264`).

## Step 1: evidence block (before any finding)

Roles are fixed by the table of `prompts:38-42`, not by reading order: CANDIDATE is the `@file`, BASELINE is `--baseline`, PRIOR is `--re-review`. Command run: `diff -w BASELINE CANDIDATE`. It reported 12 changed lines and no added or removed line (both files have 285 lines). The 12 lines sit at the same line numbers in both files: 62, 64, 73, 76, 92, 149, 159, 182, 195, 196, 198, 200. Lines are copied verbatim, in that order, with no `<` or `>` prefix, so each can be searched with `grep -nF`.

BEFORE (baseline), the 12 lines starting `<`:

```text
| WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
| WC-6 | **Resume or safe re-run.** A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output. A command either resumes from its on-disk state when given its resume flag, or, if it has none, writes each run into a fresh output directory so a re-run starts clean. Section 3 names which applies per command. | Command | `CAPS:116` (retry and circuit breaker); resume mechanisms in column (e) of `INV-A:35-55`, `INV-B:31-52` |
The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
| workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
| SA-4 | Command-file edits in Phases 1-3 are additive: a new `## Unattended mode` section and new flags. Existing lines change only where section 3 names a defect fix (roadmap and validate-roadmap drift, validate-tests target, adversarial and workflow contract gaps, explain tools, business-panel frontmatter, load usage line), and each such fix must keep the standalone behaviour or correct a documented defect. | Keeps the diff reviewable and SA-1 checkable. | Section 3 "Other required change" column |
| **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path.
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
| P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
| P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |
| P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |
```

AFTER (candidate), the 12 lines starting `>`:

```text
| WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed for this dispatch (`--output` / `--output-dir`). Exceptions (REQ-1): where the output flag names a file (tdd, init-lite, spec-panel; an output flag a section 3 row adds is a directory unless listed here), the contract is the sibling `<file>.return-contract.yaml`; adversarial writes `<output>/adversarial/return-contract.yaml`, cleanup-audit `.claude-audit/return-contract.yaml` (fixed directory, no flag) and workflow `.dev/tasks/to-do/<id>/return-contract.yaml` (`<id>` exists only once the package is created, so the worker reports the path it finds). If the brief gives no output path and this paragraph names none, the command stops with a chat-only refusal that names the missing flag and writes no file; WC-5 then sends `--outcome failed`. It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists, wherever a contract path is known (workflow's pre-creation STOPs have no package directory, so they write no contract and end `failed`; REQ-1). Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
| WC-6 | **Resume or safe re-run.** A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output. A command either resumes from its on-disk state when given its resume flag, or, if it has none, writes each run into the output directory the coordinator passed for that dispatch, never one an earlier dispatch used (section 2.3; ARCH-1), so a re-run starts clean. Section 3 names which applies per command. | Command | `CAPS:116` (retry and circuit breaker); resume mechanisms in column (e) of `INV-A:35-55`, `INV-B:31-52` |
The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` (except for the section 3.1 commands that have no `## Unattended mode` section, which take the flags in their row; REQ-2) and every flag section 3 lists as required; a distinct output directory (for tdd, init-lite and spec-panel an output file) for this dispatch, never reused from an earlier dispatch of the same Task, a `--retry-of` retry included, so the report path is known before dispatch (WC-4, WC-6; ARCH-1; the exceptions are cleanup-audit, whose retry resumes in its fixed directory and rewrites the contract there, and workflow, whose package and `<id>` are new each run; REQ-1); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file, at the path WC-4 gives for that command (REQ-1). Every 3.2 command gains the `## Unattended mode` section (section 2.1) in the phase of its own row, except `/sc:load` (usage line only). A 3.1 command gains it only where its small-fix column adds an unattended gate resolution (reflect, release-split, tdd, troubleshoot, all P2); adversarial, brainstorm, cleanup-audit, index-repo, init-lite and workflow gain none (REQ-2). Phase numbers refer to section 6.
| workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | None: a pre-creation STOP has no package directory, so it writes no contract and ends `failed` (WC-4; REQ-1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
| SA-4 | Command-file edits in Phases 1-3 are additive: a new `## Unattended mode` section and new flags. Existing lines change only where section 3 names a defect fix (roadmap and validate-roadmap drift, validate-tests target, adversarial contract gap, explain tools, business-panel frontmatter, load usage line), and each such fix must keep the standalone behaviour or correct a documented defect. | Keeps the diff reviewable and SA-1 checkable. | Section 3 "Other required change" column |
| **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag and `## Unattended mode` section on the eight P1 commands of section 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands (REQ-2). | analyze, build, business-panel, design, document, explain, index, test (flag, section, contract); load (usage line only, no section); fixes only to adversarial, cleanup-audit, index-repo (no section) | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the contract path WC-4 gives for that command (REQ-1).
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that each of the eight P1 commands (analyze, build, business-panel, design, document, explain, index, test) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one (REQ-2) | passes |
| P1 | AC-1.2 | 7.2 live check on each command named in AC-1.1 with `--unattended --output <dir>` | all steps pass |
| P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` | adversarial names one fixed path (REQ-1) |
| P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait`; then a `worker-start --retry-of` retry with a new `<output-dir>` writes its contract there and leaves the first contract unchanged (ARCH-1) |
```

Self-check before the verdict (`prompts:45`): each of the 12 AFTER lines was searched as a fixed string in the candidate, and each of the 12 BEFORE lines in the baseline: 24 of 24 found, so no role swap. As a second check, none of the 12 AFTER lines occurs in the baseline and none of the 12 BEFORE lines occurs in the candidate. Both file hashes above were taken with `sha256sum`; the candidate hash and size (59765 bytes, +2002 over the baseline) equal the figures in `rev1:11-12`.

Change map (which finding each changed line answers, from the AFTER text itself, which cites the id): line 62 (WC-4) REQ-1 and ARCH-1; 64 (WC-6) ARCH-1; 73 (section 2.3) REQ-2, ARCH-1, REQ-1; 76 (section 3 intro) REQ-1, REQ-2; 92 (workflow row) REQ-1; 149 (SA-4) follows from line 92; 159 (P1 scope) REQ-2; 182 (live check step 3) REQ-1; 195, 196, 198 (AC-1.1, AC-1.2, AC-1.4) REQ-2 and REQ-1; 200 (AC-2.2) ARCH-1. No changed line lies outside the three blocking ids' scope. The reviser contract (`cmd:263`) was met in form: line 196 and the words "for this dispatch" in line 62 carry no id of their own but are parts of cited edits; the byte total matches (`rev1:11-12`); the per-id byte split (`rev1:17-22`) cannot be rechecked from the two files and is taken as stated.

## Prior blocking findings (`cmd:262`)

Each is decided by comparing its defect with the AFTER text only.

| Id | Status | Basis |
|---|---|---|
| REQ-1 | resolved | The defect was that the contract path of WC-4 is undefined or contradicted (`r1:85-99`). AFTER spec:62 now gives the path for every case round 1 named: file-valued `--output` (tdd, init-lite, spec-panel) -> sibling `<file>.return-contract.yaml`; adversarial -> `<output>/adversarial/return-contract.yaml`, which equals the path in row spec:83; cleanup-audit -> `.claude-audit/return-contract.yaml`, the fixed directory of row spec:85; workflow -> `.dev/tasks/to-do/<id>/return-contract.yaml`, reported by the worker because `<id>` is unknown before the run (`INV-B:272`); with no path in the brief and none named, a chat-only refusal that writes no file, mapped by WC-5 to `--outcome failed` (spec:62-63). The workflow pre-creation STOP no longer demands a contract (spec:92), which matches `INV-B:272` ("Not written for pre-creation STOPs"). Live-check step 3 now says "the contract path WC-4 gives for that command" (spec:182). Leftovers are graded Medium or Minor (M-11, M-12, M-13, N-6), not blocking, because each needs a guess about which of two texts wins or lies in a part no acceptance check exercises. |
| REQ-2 | resolved | The defect was that AC-1.1 required a `## Unattended mode` section on every 3.1 and 3.2 command while the rows exempt several and schedule others later (`r1:101-115`). AFTER spec:195 asserts the section on exactly the eight P1 commands of 3.2 (analyze, build, business-panel, design, document, explain, index, test); spec:159 lists the same eight plus load (usage line only) and "fixes only" to adversarial, cleanup-audit, index-repo; spec:76 states per phase which commands gain the section; rows spec:84, 87, 112 ("None", "P1 (usage line only)") now agree. Checked: the P1 rows of 3.2 are analyze, build, business-panel, design, document, explain, index, test (spec:99, 101, 102, 106, 107, 108, 111, 123) plus load (spec:112); P2 3.1 commands (reflect, release-split, tdd, troubleshoot, spec:88-91) are in the P2 list (spec:160). The P1 test and the rows can all hold. |
| ARCH-1 | resolved | The defect was that WC-4 and WC-6 cannot both hold on a retry (`r1:119-132`). AFTER spec:64 reads the "fresh directory" as the directory passed for that dispatch, spec:73 requires a distinct directory per dispatch with `--retry-of` named, and spec:200 adds a retry case. For a command with no resume flag all three texts agree, so the stale-contract trace of `r1:130` no longer occurs. The same rule creates a new conflict for commands that do resume; that is the new finding NEW-1 below, not a failure of ARCH-1 as written. |

No prior blocking finding is open or regressed. A finding the reviser deferred or withdrew would count as open (`cmd:262`); none was (`rev1:26-32`).

## What I covered

- Read in full: the candidate (285 lines), the baseline, PRIOR, `rev1`, `README`, `command.md`, the prompts file; read the inventory lines cited in the findings below (`INV-A:35, 42, 51, 55`; `INV-B:92-93, 131, 152-153, 222, 272`).
- Computed the 12-line diff and ran the self-check above.
- Re-checked each prior blocking finding against the AFTER text; scanned every changed line against the requirements that depend on it (WC-1 to WC-12, SA-1 to SA-6, sections 2.3, 3, 6, 7), and read the unchanged rows that the changed lines point at (3.1 and 3.2 rows, P0 to P3 acceptance checks).
- Per `cmd:262` the Guard Condition Boundary Table covers guards on changed lines only. Unchanged guards (AC-C5/AC-0.3 regex, WC-3 `ask` cap, WC-10 split) were not re-audited; their round 1 findings M-1 to M-10 and N-1 to N-5 are untouched by the revision (the diff has no line for them) and stay as recorded in `r1:155-174`.
- Not covered (UNVERIFIED here): every `src/`, `CLAUDE.md`, `EVIDENCE.md` and Orca citation; the "11 locations re-read" and "340 citations re-checked" claims (spec:11, spec:285); where `.roadmap-state.json` and adversarial's `pipeline-manifest.yaml` live; `rev1`'s per-finding byte split.
- Correctness focus was not requested, so no State Variable Registry is produced (`cmd:186-188`). Panel (fixed order, `cmd:101-113`, restricted to the selected focus areas plus Whittaker): Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe.

## Guard Condition Boundary Table (hard gate, changed lines only)

Trigger: the changed lines contain guards (a refusal on a missing path, a file-versus-directory switch, a per-dispatch uniqueness rule, a test scope) (`cmd:313`). Nygard builds, Whittaker attacks; Crispin is not on this panel, so completeness is checked by me (`cmd:315`, `cmd:317`).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 WC-4 no-path refusal | spec:62 | Zero/Empty | tdd with `--unattended` and no `--output` in the brief | refusal true | chat-only refusal naming the missing flag, no file, WC-5 -> `--outcome failed` | OK |
| G1 | spec:62, 108, 115, 116 | Legitimate Edge Case | explain, recommend, research: the row names a contract but adds no output flag (`INV-B:131` lists none for research) | refusal true | row says "contract"; WC-4 says no file; where the contract goes is stated nowhere | GAP (Medium, M-11) |
| G1 | spec:62 | Sentinel Value Match | `--output docs/x/` (a directory) for a file-valued command | sibling rule applies | `docs/x/.return-contract.yaml` (hidden file); not stated | GAP (Minor, N-6) |
| G2 file-or-directory switch | spec:62, 101, 103, 110, 123 | Legitimate Edge Case | a row adds "a report path" (build, cleanup, improve, test) | "a directory unless listed here" | a "path" named like a file is read as a directory; not stated | GAP (Minor, N-6) |
| G3 distinct output dir per dispatch | spec:73 | Zero/Empty | first dispatch of a Task (no earlier dispatch) | rule vacuously met | any new directory | OK |
| G3 | spec:73, 64 | One/Minimal | retry (`--retry-of`) of a command with no resume flag | distinct dir | new dir, contract at the passed path, first attempt untouched | OK (ARCH-1 resolved) |
| G3 | spec:73, 64, 118, 205 | Legitimate Edge Case | retry of roadmap with `--resume`; its resume state is `<output_dir>/.session-memory.md` (`INV-B:153`, spec:205) | "never reused" true | "never reused" forbids the directory that holds the state WC-6 says to resume from | GAP (blocking, NEW-1) |
| G3 | spec:73, 85, 92 | Sentinel Value Match | cleanup-audit (fixed dir), workflow (new package each run) | exception listed | stated | OK |
| G4 workflow pre-creation STOP | spec:62, 92 | Zero/Empty | stop before any package exists | no contract path | no contract, `--outcome failed` | OK |
| G5 AC-1.1 scope | spec:195 | Zero/Empty | a P1 command without the section | test fails | stated | OK |
| G5 | spec:195, 112, 76 | Legitimate Edge Case | load (usage line only) and section-4 commands | not asserted / asserted absent | stated | OK |
| G6 AC-2.2 retry check | spec:200 | One/Minimal | retry with a new `<output-dir>` after a `blocked` first run | first contract unchanged | stated | OK |
| G6 | spec:200, 90 | Legitimate Edge Case | tdd: the "new `<output-dir>`" is an output file | wording says directory | not stated | GAP (Minor, N-6) |
| G6 | spec:200, 118 | Legitimate Edge Case | a resume command (roadmap) | retry must use a new dir | same conflict as G3 | GAP (blocking, NEW-1) |
| G7 live-check step 3 | spec:182, 194, 91 | Typical | P0 troubleshoot run: the report is `REPORT.md`, no contract until P2 | "report path is the contract path WC-4 gives" false | AC-0.4 says steps 1-3 pass and only step 4 uses the existing file | GAP (Medium, M-13) |
| G8 WC-4 contract clauses for commands with no unattended mode | spec:62, 76, 85, 87, 159 | Legitimate Edge Case | cleanup-audit and init-lite: WC-4 names a contract file; spec:76, the rows and P1 give them no section and no contract | no `--unattended` path reaches them | file named, no phase creates it | GAP (Medium, M-12) |

Classes left out, one line each (`cmd:317`, `cmd:334`): G1 Maximum/One (a path has no capacity; one path behaves like typical); G2 Zero/Maximum (the switch has two values); G3 Maximum (n retries give n directories; no cap or cleanup rule is stated, a resource note that harms no output, so not graded); G4 Maximum/Sentinel (a package either exists or not); G5 and G6 Maximum (a test scope has no capacity); G7 Zero (P0 always runs three commands); G8 Zero/Maximum (a clause either names a file or not).

FR-10 gate: every guard on a changed line is enumerated and every cell is populated, so synthesis proceeds. GAP rows are graded by consequence (FR-8, FR-9, `cmd:332-333`): NEW-1 is blocking; M-11, M-12, M-13 are Medium; N-6 is minor.

## Pipeline Dimensional Analysis (triggered: dispatch count differs from directory count)

The coordinator -> dispatch -> output directory -> contract flow has 4 stages and the count changes on a retry (`CAPS:116`, `cmd:353`). The changed section 2.3 sets "one directory per dispatch". Quantity Flow Diagram for a resume command:

```text
[Task T1: 1] --> [dispatch d1 (stalls), d2 (--retry-of d1): 2]
                      |
                      v
              [2.3: one output dir per dispatch: D1, D2 = 2 dirs]
                      |
                      v
              [roadmap --resume reads state from its own output dir]
                      |
                      v
              [state present: 1 dir (D1) | state read by d2: 0 dirs (D2 is empty)]  <-- MISMATCH
```

Concrete counts: 1 Task, 2 dispatches, 2 directories, 1 directory holding resume state, and the retry reads the other one. This is NEW-1 (FR-19 label CRITICAL; blocking by the grading check).

## === REQUIREMENTS ANALYSIS ===

### Re-checked prior findings

REQ-1 and REQ-2 resolved: see the table above.

### M-11 (Medium, Wiegers lead; origin=changed): the new WC-4 refusal rule leaves rows that name a contract without a place for it

Where: `spec:62` (changed), rows `spec:108`, `spec:115`, `spec:116` (unchanged), `spec:73` (changed). Text: WC-4 now ends "If the brief gives no output path and this paragraph names none, the command stops with a chat-only refusal ... and writes no file" (spec:62). Row spec:116 says research reports a "contract naming the generated `claudedocs/research_*.md` path" and adds no output flag; the inventory lists none (`INV-B:131`, `INV-B:127-135`); rows spec:108 (explain: "write the explanation to a file; contract") and spec:115 (recommend: "write the handoff envelope to a file; contract") also add no flag that carries a directory. Section 2.3 requires the brief to carry a distinct output directory (spec:73), which the brief cannot do for a command with no such flag. Grading: the sentence "an implementer builds X and X is wrong" needs a guess (whether the row or the refusal wins, or whether a flag is added); the row names a contract and WC-4 names a refusal, neither says where the contract goes. Medium. The reviser listed this as a residual risk (`rev1:36`). Recommendation (narrowing): name in each of these rows the output flag it adds or the fixed location of its contract.

### M-12 (Medium, Fowler with Hohpe; origin=changed): WC-4 names contract files for cleanup-audit and init-lite that no row, phase or check creates

Where: `spec:62` (changed), `spec:76` (changed), `spec:159` (changed), `spec:79` (unchanged), rows `spec:85`, `spec:87` (unchanged), `spec:182` (changed). Text: WC-4 says cleanup-audit writes `.claude-audit/return-contract.yaml` and init-lite writes `<file>.return-contract.yaml` "in unattended mode" (spec:62). But spec:76 says cleanup-audit and init-lite gain no `## Unattended mode` section, the init-lite row says "Small fix: None" (spec:87), the cleanup-audit row's fix is only "Name the `--pass all` final report" (spec:85), and P1 gives cleanup-audit "fixes only ... (no section)" (spec:159). Their report today is `pass<N>-summary.md` or `context-audit.md` (spec:85, 87). The inventory names no contract file for either (`INV-A:42`, `INV-A:55`; `rev1:37`). Section 3.1 still says the worker reports the named file "until Phase 1 adds the contract" (spec:79), and Phase 1 adds no contract for these two. A coordinator that applies WC-5 and live-check step 3-4 (spec:63, 182-183) to these commands looks for a file nothing writes. Grading: no acceptance criterion runs the live check on them (AC-0.4 uses troubleshoot, workflow, adversarial, spec:194; AC-1.2 only the eight P1 commands, spec:196), and the stale sentence at spec:79 gives a reading under which the "report today" file is used, so the wrong outcome needs a guess. Medium. Recommendation (narrowing): delete the two clauses from spec:62, or say these commands report their "Report today" file.

### M-13 (Medium, Adzic; origin=changed): AC-0.4 step 3 cannot pass for troubleshoot in P0 as worded

Where: `spec:182` (changed), `spec:194` (unchanged), row `spec:91`. Step 3 requires the report path to be "the contract path WC-4 gives for that command" (spec:182); troubleshoot's report in P0 is `REPORT.md` and its contract exists only from P2 (spec:91, `INV-B:242`); AC-0.4 says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file" (spec:194). This text is older than the revision (the same step existed at `v1:182`); only the words after "contract path" changed. Medium: the intent is readable, but the pass condition as written needs a guess.

### N-6 (Minor, Wiegers; origin=changed): file-or-directory wording

(a) WC-4 says a row-added output flag "is a directory unless listed here" (spec:62), while rows add "a report path" (build, cleanup, improve, test; spec:101, 103, 110, 123). (b) A directory given to a file-valued command (tdd, init-lite, spec-panel) yields a hidden file `.return-contract.yaml`. (c) AC-2.2 says "a new `<output-dir>`" for tdd, whose flag is a file (spec:200, spec:90). A note only.

## === ARCHITECTURE ANALYSIS ===

### NEW-1 (blocking, CRITICAL label under FR-19, Fowler lead, Whittaker attack W-R2-1; origin=changed; newly discovered): section 2.3 forbids reusing the output directory on a retry, but WC-6 and the roadmap row require a retry to resume from state kept in that directory

Where: `spec:73` (changed, section 2.3), `spec:64` (changed, WC-6), rows `spec:83` and `spec:118` (unchanged), `spec:205` (AC-3.2, unchanged), `INV-B:153`, `INV-A:35`. Came from: the revision of ARCH-1; round 1's own recommendation (`r1:132`) was to require a distinct directory per dispatch, and the exception list written into AFTER spec:73 names only cleanup-audit and workflow.

Text as written:
- spec:73 (AFTER): the brief states "a distinct output directory ... for this dispatch, never reused from an earlier dispatch of the same Task, a `--retry-of` retry included"; "the exceptions are cleanup-audit ... and workflow".
- spec:64 (WC-6, AFTER): "A command either resumes from its on-disk state when given its resume flag, or, if it has none, writes each run into the output directory the coordinator passed for that dispatch, never one an earlier dispatch used". The first branch is unchanged: a command with a resume flag resumes from its on-disk state on a retry.
- spec:118 (roadmap): "the 'Resume?' prompt is replaced by the explicit resume flag (resume only when passed)". Its resume state is `<output_dir>/.session-memory.md` (`INV-B:153`); AC-3.2 itself puts that file in `<dir>` (spec:205: "existing `<dir>/.session-memory.md` and no resume flag" -> "starts fresh").
- spec:83 (adversarial): `--pipeline-resume` for pipeline mode with `--output <dir>`; where `pipeline-manifest.yaml` lives is not stated (`INV-A:35`), so I do not rely on this row.

Grading check: An implementer who follows the stated text as written builds a coordinator brief template that gives every retry dispatch, `--retry-of` included, a new `--output` directory with only cleanup-audit and workflow excepted; a stalled `/sc:roadmap` worker is then retried with `--resume --output D2`, where D2 holds no `.session-memory.md`, so the retry starts from the first wave exactly as AC-3.2 shows for a directory without that state; and that is wrong because WC-6 requires a command with a resume flag to resume from its on-disk state on a retry, and the only directory that holds that state is the one spec:73 forbids. The two stated texts cannot both hold for roadmap.

State trace: Task T1; d1 `/sc:roadmap <spec> --unattended --output D1` stalls after Wave 2 (`D1/.session-memory.md` records Wave 2). d2 `worker-start --retry-of d1`, brief per spec:73 `--output D2 --resume`. D2 is empty, so Waves 0-2 run again. If the coordinator instead passes D1 to d2, the brief breaks spec:73. Counts: 2 dispatches, 2 directories, 1 directory with state (Quantity Flow Diagram above). Not every resume command is hit: tdd (`--resume <task-file>`, task file under `.dev/tasks/to-do/TASK-TDD-<ts>/`, `INV-B:222`), brainstorm (`--resume-from <seed-brief>`, `INV-A:39`) and release-split (`--resume-from <file>`, `INV-B:123`) take an explicit file path and keep working with a new output directory. pr-submit resumes from `--resume <run-log.jsonl>` while its contract sits "beside `monitor-run-<PR>.jsonl`" (spec:114, `INV-B:92-93`); whether that conflicts is UNVERIFIED and it is in P4 behind D3, so I do not grade it.

Recommendation (narrowing, no new mechanism): in spec:73 replace "never reused ..." by "never reused unless the retry resumes (WC-6) from state kept in that directory, in which case the retry brief passes that directory and its resume flag", and name roadmap as the case; keep the AC-2.2 retry case for commands without a resume flag.

## === ADVERSARIAL ANALYSIS (Whittaker, review order 6) ===

Format per `cmd:82`. Labels use CRITICAL / MAJOR / MINOR; the review-loop grade is given after each.

- W-R2-1. I can break this specification by **Sequence Attack**. The invariant at **section 2.3 and WC-6 (spec:73, 64)** fails when **a retry follows a stalled resume-capable command**. Concrete attack: see NEW-1 (d1 stalls after Wave 2, d2 gets a new empty directory and re-runs Waves 0-2). Label CRITICAL (FR-19); review-loop grade blocking.
- W-R2-2. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 (spec:62)** fails when **the command has no output flag, for example `/sc:research --strategy planning --unattended`**. Concrete attack: the brief cannot carry a directory (spec:116 adds none), WC-4 refuses and writes no file, WC-5 sends `--outcome failed`, and the happy-path check AC-2.3 (spec:201) cannot reach `succeeded`. Label MAJOR; grade Medium (M-11), because the row text allows a reading in which the contract goes next to the report.
- W-R2-3. I can break this specification by **Divergence Attack**. The invariant at **WC-4 (spec:62) versus rows spec:85, 87** fails when **cleanup-audit finishes its pass**. Concrete attack: the worker looks for `.claude-audit/return-contract.yaml`, finds only `pass1-summary.md`, and WC-5 ("no report exists" -> failed, spec:63) sends `--outcome failed` for a good audit. Label MAJOR; grade Medium (M-12), because spec:79 lets the worker report the file named in the row.
- No attack found on the changed lines for the Accumulation, Sentinel Collision methodologies beyond the above; the `<id>` sentinel for workflow (spec:62) is handled by "the worker reports the path it finds".

## Findings on changed lines (`cmd:262`)

| Id | origin | Label | Grade | One-line wrong outcome |
|---|---|---|---|---|
| NEW-1 | changed | CRITICAL | blocking | spec:73 forbids reusing the directory that holds a resume command's state; a roadmap retry restarts from Wave 0 against WC-6 |
| M-11 | changed | MAJOR | Medium | WC-4 refusal vs rows that name a contract but no output flag (research, explain, recommend) |
| M-12 | changed | MAJOR | Medium | WC-4 names contracts for cleanup-audit and init-lite that nothing creates |
| M-13 | changed | MAJOR | Medium | AC-0.4 step 3 cannot pass for troubleshoot in P0 as worded |
| N-6 | changed | MINOR | note | file-or-directory wording of row-added output flags |

Findings of origin=unchanged: none that quote a changed line and meet the blocking test. Unchanged text I did not re-grade (M-1 to M-10, N-1 to N-5 of round 1) is untouched by the revision and is carried as recorded in `r1:155-174`; none enters the Reviser brief.

### follow-up candidates (Medium and minor; none fails the review, none enters the Reviser brief)

Medium (warnings): M-11, M-12, M-13 above. Carried from round 1, unchanged and not re-graded: M-1 to M-10 (`r1:157-167`).

Minor notes: N-6 above. Carried from round 1: N-1 to N-5 (`r1:169-174`). Additional notes: N-7. Spec:79 still says "The only command changes are the small fixes in the last column" and "until Phase 1 adds the contract"; after the revision Phase 1 adds a contract to no 3.1 command except through the adversarial path fix, so the second phrase is stale (covered by M-12). N-8. `rev1` says the section 3 "Fresh dir" cells were left alone because they fit the new reading (`rev1:32`); that holds except for resume commands (NEW-1).

The follow-up issue offer (`cmd:260`) is not asked: this run is a single-turn worker with no user in the loop, so the list is recorded only.

## Quality assessment (standard format, scores 0-10)

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  review: 2 of 3
  expert_panel: [Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe]
  focus_areas: [requirements, architecture]
  scope: changed lines + prior blocking findings
quality_assessment:
  overall_score: 8.0
  clarity: 8.0
  completeness: 7.5
  testability: 8.0
  consistency: 7.5
critical_issues:
  - {category: architecture, severity: CRITICAL, expert: Fowler, issue: "NEW-1 distinct output dir per dispatch vs resume from state kept in that dir", recommendation: "allow the retry to reuse the dir when it resumes (WC-6)"}
expert_consensus:
  - "The three round 1 blockers are repaired by narrowing edits; the revision stays inside the blocking ids."
  - "The one open blocker is a side effect of the per-dispatch directory rule."
improvement_roadmap:
  immediate: [NEW-1]
  short_term: [M-11, M-12, M-13]
  long_term: [N-6]
adversarial_analysis: [W-R2-1, W-R2-2, W-R2-3]
```

Strengths: the revision is small and traceable (12 lines, same line count, every edit cites its id); the path table in WC-4 matches the rows it points at for adversarial, tdd, workflow; the REQ-2 scoping is internally consistent across spec:76, 159, 195, 196.

Coverage line: the PASS-only line `scoped PASS: changed lines + prior blockers` is not written, because one blocking finding is open (`cmd:262`). Whole-document assurance would need a separate, labelled first review (`cmd:262`).

## Reviser brief

Blocking finding ids: NEW-1. Nothing else. REQ-1, REQ-2 and ARCH-1 are resolved and are not listed.

Rules for the reviser (restating `cmd:263`; the reviser reads this report, not the command): revise only text a blocking finding names (here spec:73, with spec:64 only if needed); add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size of the candidate before and after, and the bytes added and deleted per finding id. Leave every Medium and minor item above untouched (M-1 to M-13, N-1 to N-8). Return the candidate once and do not award yourself a PASS. A brief cannot make a Medium or minor finding fail the review or authorize editing one, including through "apply all findings" (`cmd:264`).

verdict: FAIL
