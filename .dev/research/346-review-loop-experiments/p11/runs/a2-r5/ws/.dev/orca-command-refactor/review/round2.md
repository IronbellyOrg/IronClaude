review: 2 of 3

# Spec-panel re-review, round 2: Orca worker contract spec

Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md`

Citation keys. `SPEC:N` = line N of the CANDIDATE. `BASE:N` = line N of the BASELINE. `R1:N` = line N of PRIOR. `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`. These files are the only evidence checkable in the workspace. A citation of a file outside the workspace (`src/...`, `CLAUDE.md`, `EVIDENCE.md`, `pyproject.toml`) is UNVERIFIED unless an inventory line quotes it.

## Roles and inputs

| Role | File | Size | sha256 |
|---|---|---|---|
| CANDIDATE | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` | 58629 bytes, 285 lines | `7cfc46955e89212267b7b42612208b7b453942bd61bda42b47e3e96f605b89ff` |
| BASELINE | `.dev/orca-command-refactor/specs/history/spec-v1.md` | 57763 bytes, 285 lines | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` |
| PRIOR | `.dev/orca-command-refactor/review/round1.md` | 40510 bytes, 280 lines | `d1c7868eca2a3789831cbb2829a3e82a10b295822c7410da9cdb531ed474b7d5` |

The baseline's hash and size match the candidate that PRIOR reviewed (`R1:6`: 57763 bytes, sha256 `d3cdbe57...5200d`), so BASELINE is the text PRIOR saw. PRIOR's header carries N = 1, so this report is the second review (the header is on line 1). All three inputs were readable. `~/.claude/agents/rf-qa.md` and `.claude/agents/rf-qa.md` are not in the sandbox, so the re-check below uses the Review Loop rules as written in the command, which stand alone.

## Step 1. Evidence block

`diff -w BASELINE CANDIDATE` is not empty (exit 1). It reports 12 changed hunks, each one line replaced by one line (hunks at 62, 73, 76, 79, 83, 92, 159, 182-183, 194, 196, 200). The changed lines, verbatim:

### BEFORE (baseline)

```text
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
< The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
< The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
< These run as workers now if the brief uses the stated flags; the worker reports the named file until Phase 1 adds the contract. The only command changes are the small fixes in the last column.
< | adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
< | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
< | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
< 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path.
< 4. `test -s <contract>` and `uv run python -c "import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); assert d['status'] in {'succeeded','partial','failed','blocked'}; assert d['command']" <contract>` (PyYAML is a declared dependency, `pyproject.toml:38`). **Pass:** both exit 0.
< | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
< | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
< | P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |
```

### AFTER (candidate)

```text
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<contract-dir>/return-contract.yaml`, where `<contract-dir>` is the directory the brief passes as `--contract-dir <dir>`. When the command's `--output` / `--output-dir` is already a directory and `--contract-dir` is absent, that directory is `<contract-dir>`; for every other command (a file-valued output flag, no output flag, or a generated or fixed location) the brief must pass `--contract-dir` (B-1). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
> The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the contract directory (`--contract-dir`), so the report path is known before dispatch (WC-4, B-1); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
> The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<contract-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
> These run as workers now if the brief uses the stated flags; the worker reports the named file until Phase 1 adds the contract; from Phase 1 the brief also passes `--contract-dir <dir>` (WC-4, B-1). The only command changes are the small fixes in the last column.
> | adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Write the contract at `<contract-dir>/return-contract.yaml` (WC-4) instead of the unnamed, inconsistent path (P1, B-1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
> | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Also write the contract to `<contract-dir>` on every outcome, pre-creation STOPs included (WC-4); the package copy stays (P1, B-1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
> | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate) and the directory-valued `--contract-dir` (B-1); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
> 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path. In P0, before the contract exists, the command's existing report file stands in for it: `--outcome` follows WC-5 applied to that report and the report path is that file (B-2).
> 4. `test -s <contract>` (`<contract>` = `<contract-dir>/return-contract.yaml`, WC-4, B-1) and `uv run python -c "import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); assert d['status'] in {'succeeded','partial','failed','blocked'}; assert d['command']" <contract>` (PyYAML is a declared dependency, `pyproject.toml:38`). **Pass:** both exit 0.
> | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass, with the existing report file standing in for the contract in step 3 (B-2); step 4 is `test -s` on that file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
> | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --contract-dir <dir>` (B-1) | all steps pass |
> | P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file> --contract-dir <dir>` (B-1) with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |
```

Changed lines in the candidate: SPEC:62, 73, 76, 79, 83, 92, 159, 182, 183, 194, 196, 200 (same line numbers in the baseline; the file has 285 lines in both).

### Self-check (run before the verdict)

Each AFTER line above, without its `>`, was searched with `grep -xF` in the CANDIDATE, and each BEFORE line, without its `<`, in the BASELINE. Result: 12 of 12 AFTER lines found in the candidate and in none of the baseline lines; 12 of 12 BEFORE lines found in the baseline and in none of the candidate lines. No quote is missing, so no roles were swapped. The size check matches too: baseline 57763 bytes (equal to `R1:6`), candidate 58629 bytes, +866.

## What was covered

- Read in full: the command definition, `README` (38 lines), PRIOR (280 lines), the diff, and the candidate in full (285 lines). Read in part: the inventory lines that the changed rows rest on (`INV-A:35,60,61,97`, `INV-B:33-52,82,267-275`).
- Re-checked both prior blocking findings (B-1, B-2) against the AFTER text only.
- Reviewed the 12 changed lines and the text that depends on them: WC-4's dependants (`--output` rows in sections 3.1 and 3.2, SPEC:109, 114, 185, 209, 210), the P0 and P1 checks (SPEC:158-159, 182-183, 194-198), SA-3 (SPEC:148), D1's example (SPEC:228) and the phase counts (P1-P4 cover 9 + 11 + 4 + 3 = 27 rows of 3.2 plus the 4 ready commands moved to P1/P2 fixes; counts unchanged).
- Guard Condition Boundary Table: built for the guards on changed lines only (WC-4's directory rule and the P0 stand-in clause).
- Reviser contract (Review Loop bullet 6) checked against the diff: every changed line is either a text B-1 or B-2 named (SPEC:62, 73, 83, 92, 182, 194, 200) or a consequence needed to keep one of those consistent (SPEC:76, 79, 159, 183, 196). Each cites its finding id. No new section or requirement was added. The one new mechanism, `--contract-dir`, is the input B-1's recommendation asked for (R1:95). Byte size before and after, 57763 and 58629, checked with `wc -c`. `review/revise1.md` is not a named input and was not read.
- Not covered, UNVERIFIED: every `src/superclaude/...`, `CLAUDE.md`, `EVIDENCE.md`, `pyproject.toml` citation, and the self-reported checks at SPEC:11 and SPEC:285. Medium and minor items of PRIOR on unchanged lines were not re-reviewed; they stay open as follow-up candidates.
- Not active: `--focus correctness` was not passed, so no State Variable Registry. No pipeline was introduced or changed, so Pipeline Dimensional Analysis was not triggered.

## Grading used

Same reading as PRIOR (`R1:24`), restated because the verdict depends on it. Review Loop bullet 2 calls FR-8/FR-9 findings blocking. The brief says to report concrete wrong outcomes and to list Medium findings as follow-up candidates, which narrows the scope (bullet 7 allows a brief to narrow). So a GAP row blocks only if its finding passes this sentence: "An implementer who follows the stated text as written builds X, and X is wrong because Y." Otherwise it is a Medium follow-up candidate. If the coordinator holds the strict reading (every GAP row blocking), the three GAP rows below would make this review FAIL; that reading is also what PRIOR chose not to apply, and the coordinator accepted it by revising only B-1 and B-2.

## Prior blocking findings

| Finding | Prior status | Re-check status | Basis (AFTER text only) |
|---|---|---|---|
| B-1 Contract location rule cannot be satisfied for most of the commands it covers | blocking (R1:87) | **resolved** | The location is now an explicit brief input: `<contract-dir>` is "the directory the brief passes as `--contract-dir <dir>`" (SPEC:62), with the old `--output`/`--output-dir` reading kept only when that flag is already a directory and `--contract-dir` is absent. The three failures PRIOR named are closed. (1) File-valued output: the tdd example now passes both flags, `--output <file> --contract-dir <dir>` (SPEC:200), so the contract is at `<dir>/return-contract.yaml`, not under a regular file. (2) No output flag or a generated or fixed location (workflow, tasklist, research, implement, index-repo, cleanup-audit, review-translation): SPEC:62 requires the brief to pass `--contract-dir` for "every other command", SPEC:73 lists it in the brief, and workflow's pre-creation STOP now has a directory to write into (SPEC:92). (3) Existing contract elsewhere: adversarial writes at `<contract-dir>/return-contract.yaml` (SPEC:83). The check is runnable: step 4 defines `<contract>` = `<contract-dir>/return-contract.yaml` (SPEC:183), and AC-1.2 and AC-2.2 pass the flag (SPEC:196, 200). Consistent with every requirement that depends on it except the notes F-2 and n-2, n-3 below. |
| B-2 P0 acceptance check requires a contract that P0 does not build | blocking (R1:97) | **resolved** | Step 3 now says that in P0 "the command's existing report file stands in" for the contract, with `--outcome` following WC-5 applied to that report and the report path being that file (SPEC:182). AC-0.4 repeats the stand-in for step 3 and defines step 4 as `test -s` on that file (SPEC:194). Both steps can now pass with what P0 builds (P0 makes no command edit, SPEC:158). Residual gap on one command, F-1 below, is a Medium follow-up. |

No prior blocking finding is open or regressed.

## Mandatory artifact: Guard Condition Boundary Table (guards on changed lines only)

Triggered by two guards on changed lines: the directory rule in WC-4 (SPEC:62) and the P0 stand-in clause (SPEC:182, 194). The table is complete (all cells populated, both guards enumerated) before the synthesis, as FR-10 requires. Nygard builds, Crispin validates completeness, Whittaker attacks the entries.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-4 directory rule: "output flag already a directory and `--contract-dir` absent" | SPEC:62 | Zero/Empty | `--contract-dir` absent, output flag file-valued (tdd) or missing (workflow) | false | "the brief must pass `--contract-dir`"; nothing says what the command does if the brief breaks the rule | GAP |
| WC-4 | SPEC:62, 83 | One/Minimal | `--contract-dir .` | n/a | contract at `./return-contract.yaml` | OK |
| WC-4 | SPEC:62, 200 | Typical | tdd with `--output <file> --contract-dir <dir>` | n/a | contract at `<dir>/return-contract.yaml`; AC-2.2 reads it | OK |
| WC-4 | SPEC:62 | Maximum/Overflow | `--output <dir>` and `--contract-dir <other>` both given | false (flag present) | contract at `<other>`; the output directory is used only when the flag is absent | OK |
| WC-4 | SPEC:62, 83 | Sentinel Value Match | adversarial `--output <dir>`, no `--contract-dir`, and the legacy path `<dir>/adversarial/return-contract.yaml` | true | contract at `<dir>/return-contract.yaml`; the legacy path is retired by the row | OK |
| WC-4 | SPEC:62 | Legitimate Edge Case | `--contract-dir` names a directory that cannot be created or written, or is a regular file | n/a | not stated (the unchanged WC-4 clause "on every outcome" cannot hold; carried from M-9) | GAP |
| P0 stand-in: "before the contract exists, the existing report file stands in" | SPEC:182, 194 | Zero/Empty | existing report absent or 0 bytes | true | absent: WC-5 gives `--outcome failed`; 0 bytes: `test -s` fails | OK |
| P0 stand-in | SPEC:182, 91 | One/Minimal | troubleshoot with one `REPORT.md` | true | `report_path` is that file (INV-B:49) | OK |
| P0 stand-in | SPEC:182, 92 | Typical | workflow, whose package contract already exists in P0 (INV-B:272) | true | the reported path is the package contract; WC-5 applied to it | OK |
| P0 stand-in | SPEC:182, 83 | Maximum/Overflow | adversarial: a merged output plus 6 artifacts and a contract with no fixed name (INV-A:35, INV-A:60) | true | which file is "that file" is not stated | GAP |
| P0 stand-in | SPEC:182 | Sentinel Value Match | the contract exists and the existing report also exists (a P0 check re-run after P1) | false ("before the contract exists" no longer holds) | normal step 3 and step 4 apply | OK |
| P0 stand-in | SPEC:182 | Legitimate Edge Case | existing report is free-form markdown with no `status` field (troubleshoot `REPORT.md`) | true | "WC-5 applied to that report": failed or blocked only if the report says so; else succeeded | OK |

GAP rows: 3 (rows 1, 6, 10). Under the grading above none passes the sentence by itself: rows 1 and 6 feed follow-up F-3 (carried M-9 family; the AC-2.2 example passes the flag), row 10 feeds F-1.

## === REQUIREMENTS ANALYSIS === (findings on changed lines and their dependants)

No blocking finding. Wiegers, Adzic and Cockburn reviewed WC-4 as revised and the checks that use it. The directory rule is now testable: for a given command the contract path is a function of the brief, and the tdd example in AC-2.2 shows the form.

### F-1 AC-0.4 does not say which existing file stands in for adversarial (Medium; origin=changed)

- Severity label MAJOR, graded Medium (a guess between allowed readings). Experts: Crispin (lead), Wiegers. Priority: Medium. Impact: Testability.
- Issue. Step 3 and AC-0.4 say "the command's existing report file stands in" and "the report path is that file" (SPEC:182, 194). For troubleshoot the file is `REPORT.md` and for workflow the package contract (SPEC:91-92). For adversarial the row says "contract, but filename not fixed" (SPEC:83) and the inventory records two paths in use plus a merged output with 6 artifacts (INV-A:35, INV-A:60). The tester must choose, and step 3's "report path is that file" and step 4's `test -s` then compare against the tester's own choice.
- Grading. Any existing file the worker reports lets the check pass, so no wrong outcome follows from the text; the defect is a missing choice. Medium.
- Recommendation. Name the file (for example "the merged output named in the command's own return text") or say the tester takes the path the worker reports.

### F-2 Rows still place the contract "beside" a file, while WC-4 puts it in `<contract-dir>` (Medium; origin=unchanged, depends on changed SPEC:62)

- Experts: Wiegers, Newman. Priority: Medium. Impact: Consistency.
- Issue. The changed WC-4 line fixes the location as `<contract-dir>/return-contract.yaml` set by the brief, and SPEC:76 defines "Contract" that way (both changed lines). Three unchanged lines name a different location: implement, "contract beside the ledger `progress.md`" (SPEC:109; the ledger has a derived slug, INV-A:51); pr-submit, "markdown summary and contract beside `monitor-run-<PR>.jsonl`" (SPEC:114); AC-4.3, "a markdown summary and contract exist beside `monitor-run-<PR>.jsonl`" (SPEC:210). Both commands have no directory-valued output flag today, so SPEC:62 requires the brief to pass `--contract-dir`, and the file would then sit apart from the ledger or the run log.
- Grading. SPEC:76 and SPEC:62 are normative and SPEC:183 reads `<contract-dir>`, so an implementer who follows the stated rule builds the contract at `<contract-dir>`; "beside" then reads as a description of a second copy or a location hint. P4 waits on decisions D2-D4 before it starts (SPEC:154), so the row is not built until then. No concrete wrong outcome without a further assumption: Medium.
- Recommendation. Say "contract at `<contract-dir>`; the ledger or the run log stays where it is", or have the brief pass `--contract-dir` equal to that directory.

### F-3 No rule for an unusable `--contract-dir` (Medium; origin=changed guard, same defect class as carried M-9)

- Severity label MAJOR, graded Medium. Experts: Nygard (lead), Crispin. Priority: Medium. Impact: Completeness.
- Issue. WC-4 now relies on a brief-supplied directory (SPEC:62), but nothing says what the command does when the brief omits it for a command that needs it, or when the directory cannot be created or written (rows 1 and 6 of the table). The clause "written on every outcome ... including stops before any other output exists" (SPEC:62) cannot hold then.
- Grading. The worst case is a missing contract, which step 4 and step 3 catch at the coordinator (SPEC:182-183), and AC-2.2 supplies the flag. No concrete wrong outcome follows from the stated text: Medium. M-9 already asks for a refusal rule for an unusable directory (R1:160-164).
- Recommendation. One sentence: under `--unattended` a command with no usable contract directory refuses before any work and prints the refusal in chat.

## === ARCHITECTURE ANALYSIS ===

No blocking architecture finding. Fowler and Hohpe checked that the new flag keeps the decision intact: `--contract-dir` is a plain command input, not an Orca call, so SA-2 (SPEC:147) and AC-C1 (SPEC:172) are unaffected. The directory rule has one default and one explicit form, so it does not add a second mechanism. Newman notes that the flag is the contract's only new input and that WC-4 names it.

## Adversarial analysis (Whittaker; changed lines)

1. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 (SPEC:62)** fails when **the brief omits `--contract-dir` for a command with a file-valued or missing output flag**. Concrete attack: before: brief `/sc:tdd "auth" --unattended --output t.md`, no `--contract-dir`; step: the command has no stated behaviour for the missing directory; after: either no contract (coordinator's step 3 sees no report, `--outcome failed`) or one guessed location. Severity MAJOR, graded Medium (F-3): the rule tells the brief to pass the flag and the AC-2.2 example does.
2. I can break this specification by **Divergence Attack**. The invariant at **WC-4 against SPEC:109, 114 (changed line SPEC:62)** fails when **the contract directory and the ledger or run-log directory differ**. Concrete attack: before: `/sc:implement <plan> --unattended --contract-dir /tmp/c`; step: the command writes `progress.md` under a derived slug and the contract "beside the ledger" per SPEC:109; after: `worker_done --report-path /tmp/c/return-contract.yaml` names a missing file. Severity MAJOR, graded Medium (F-2): SPEC:62 and SPEC:76 govern.
3. I can break this specification by **Sentinel Collision Attack**. The invariant at **SPEC:182 (P0 stand-in)** fails when **the stand-in file's name collides with the contract name**. Concrete attack: before: P0 adversarial run, the legacy contract is written at `<dir>/adversarial/return-contract.yaml` (INV-A:35); step: the tester treats it as the stand-in and the doubled path `.../adversarial/adversarial/` as another run (INV-A:60); after: step 3's "that file" differs between testers. Severity MAJOR, graded Medium (F-1).
4. **Sequence Attack**, **Accumulation Attack**: no new break on changed lines. The ordering of contract write and `worker_done`, and parallel writers in one worktree, are carried M-17 and M-11 on unchanged lines.

## Minor notes (never fail the review)

- n-1 (origin=unchanged, quotes changed SPEC:62). Step 6 passes only if git shows "files under the brief's output directory (and the command's documented artifacts)" (SPEC:185). With tdd, the output is a file and the contract goes to a separate `--contract-dir` (SPEC:200); the contract file is a documented artifact (SPEC:62), so the step can pass, but the sentence does not say so.
- n-2 (origin=unchanged, quotes changed SPEC:62). SA-3 allows the contract and report files "only in unattended mode or when the caller passes the new output flag" (SPEC:148). `--contract-dir` is a second new flag. What a command does with `--contract-dir` and no `--unattended` is not stated (SPEC:62 says "in unattended mode"). AC-1.3 tests only the case with neither (SPEC:197).
- n-3 (origin=unchanged, quotes changed SPEC:196). AC-1.2 now runs the live check with `--contract-dir` on every P1 command, and load is a P1 command with no contract (SPEC:112, 159). This is carried M-14 and stays Medium.
- n-4 (origin=unchanged). Self-reported checks at SPEC:11 and SPEC:285 ("11 locations re-read", "about 340 citations", "no verdict or phase changed") predate the revision and cannot be checked from the workspace. UNVERIFIED.
- n-5 (origin=unchanged). AC-1.4 expects adversarial to name "one fixed path" (SPEC:198) while SPEC:83 now gives a path that depends on the brief (`<contract-dir>/...`). The grep still passes; the wording is looser than before.

## Follow-up candidates

Medium (changed or depending on changed lines): F-1, F-2, F-3.
Medium (carried from PRIOR, unchanged lines, not re-reviewed): M-1 to M-12, M-13, M-14, M-15, M-16, M-17, M-20, M-21 (R1:264).
Minor: n-1 to n-5 above; PRIOR's n-1 to n-9 (R1:265).
None of these blocks the verdict. No severe defect was newly discovered in older text during this review.

## Expert panel notes (review order)

1. Wiegers: B-1's requirement is now satisfiable and measurable; F-2 is a wording conflict between two requirement statements.
2. Adzic: the tdd example with both flags (SPEC:200) is the concrete case that was missing.
3. Cockburn: the coordinator's goal (a known report path before dispatch) now holds for every command through the brief; the person is still absent from the blocked flow (carried M-2).
4. Fowler: `--contract-dir` is a clean, Orca-free input; SA-2 holds.
5. Nygard: the unusable-directory failure mode is still open (F-3, M-9).
6. Whittaker: three attacks above, none blocking.
7. Newman: contract location now has one source of truth in WC-4; three rows still describe it differently (F-2).
8. Hohpe: the contract path is fixed before dispatch; write-then-notify ordering is carried M-17.
9. Crispin: B-2's fix makes AC-0.4 satisfiable; F-1 closes the last ambiguity for adversarial.
10. Gregory: the live check reads in order; step 6 could name the contract file (n-1).
11. Hightower: no operational change in this revision.

## Reviser brief

Blocking finding ids: none. No blocking finding is open, so no revision is required.

Restated reviser contract (Review Loop bullet 6; the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; report the byte size before and after (before this review: 58629 bytes). F-1, F-2, F-3, n-1 to n-5 and the carried Medium items are follow-up candidates and are not to be acted on in a fix cycle.

verdict: PASS
