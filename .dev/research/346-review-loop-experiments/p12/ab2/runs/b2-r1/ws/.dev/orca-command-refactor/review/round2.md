review: 2 of 3

# Spec-panel re-review, round 2: orca-worker-contract-spec.md

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md`
- Prompt followed: RE-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full), with CANDIDATE = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, BASELINE = `.dev/orca-command-refactor/specs/history/spec-v1.md`, PRIOR = `.dev/orca-command-refactor/review/round1.md`. N = 1 (the prior `review: 1 of 3` at `round1.md:1`) + 1 = 2.
- sha256 candidate: `395733f7a06e7778fe5ef57a893a4bf2e96dc6f3da91a7e9826eea38dedbd783` (58,588 bytes, 285 lines).
- sha256 baseline: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (57,763 bytes, 285 lines). This equals the candidate hash that `round1.md:8` records, so the baseline is the text the prior review saw.
- sha256 prior report: `d21cd97dc654bd822191b099cab32ec513ae32db0e3b2d38c57de24dc330b71c`.
- Reviewer model actually used: `claude-sonnet-5-5` (Sonnet 5.5).
- Mode: critique. Focus: requirements, architecture. Whittaker is active. `--focus correctness` is not active, so no State Variable Registry is produced. Behavioral Flow step 6 (Improve) is skipped under `--re-review`; no revised specification is written, and `--iterations` is ignored.
- Citation shorthand: `S:N` = line N of the candidate; `B:N` = line N of the baseline; `R1:N` = line N of the prior report. `INV-A:N`, `INV-B:N` = lines of `inventory/commands-a.md`, `inventory/commands-b.md`. `CAPS:N` = `inventory/orca-capabilities.md`. Every `cmd/`, `sk/`, `ag/`, `src/` path, `CLAUDE.md`, `EVIDENCE.md`, and any Orca guide line is UNVERIFIED here (not in the workspace); I checked them only through the inventory line that quotes them.
- Prior-report handling: `R1:2` carries the verification block (confirmed ids F1, F2; no rejected id), so the prior blocking findings are F1 and F2 only. F3-F14 are Medium and N1-N5 are notes in the prior report; they are not prior blocking findings.
- Reviser contract input: `review/revise1.md` (the reviser's own account) was read as context only. I decided every verdict below from the AFTER text.
- The project agent file `rf-qa.md` (`.claude/agents/rf-qa.md`, `~/.claude/agents/rf-qa.md`) does not exist in the sandbox, so the re-check of the prior blockers follows only the rules in the command's Review Loop section, which stand alone as the command allows.

## Step 1: evidence block (`diff -w BASELINE CANDIDATE`)

The diff has 9 changed lines (9 `<` lines, 9 `>` lines; the line count stays 285). Each quote is copied verbatim; the line numbers are the lines where the text was found by exact match.

BEFORE (baseline) S:62:
```text
| WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
```

AFTER (candidate) S:62:
```text
| WC-4 | **One report file, known before dispatch (one exception below), written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). The one exception is workflow: it writes into a package directory `<id>` that the command generates, so its contract path is not known before dispatch and the worker takes it from the package the command created (UNVERIFIED how the command reports `<id>`, `INV-B:272`; F2). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
```

BEFORE (baseline) S:73:
```text
The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
```

AFTER (candidate) S:73:
```text
The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` once the command's phase (section 6) has landed, and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4; not for workflow, F2); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
```

BEFORE (baseline) S:76:
```text
The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
```

AFTER (candidate) S:76:
```text
The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml` (for workflow, the file in its generated package directory, F2). Every changed command except load (usage line only) also gains the `## Unattended mode` section (section 2.1) and the `--unattended` flag in the phase named in its row, not earlier (F1). Phase numbers refer to section 6.
```

BEFORE (baseline) S:83:
```text
| adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
```

AFTER (candidate) S:83:
```text
| adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract filename to `<output>/return-contract.yaml`, the WC-4 path (P1; F2) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
```

BEFORE (baseline) S:92:
```text
| workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
```

AFTER (candidate) S:92:
```text
| workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` (`<id>` is generated by the command, so the path is not known before dispatch; WC-4 exception, F2) | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
```

BEFORE (baseline) S:159:
```text
| **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
```

AFTER (candidate) S:159:
```text
| **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by the commands named in this row, load excepted (a no-op where a command has no gate; F1); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
```

BEFORE (baseline) S:182:
```text
3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path.
```

AFTER (candidate) S:182:
```text
3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path (for workflow, an existing `.dev/tasks/to-do/<id>/return-contract.yaml`, F2).
```

BEFORE (baseline) S:195:
```text
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
```

AFTER (candidate) S:195:
```text
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command named in the P1 row of section 6, load excepted, has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that neither load nor any section-4 command has one (F1) | passes |
```

BEFORE (baseline) S:198:
```text
| P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |
```

AFTER (candidate) S:198:
```text
| P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names the one fixed path `<output>/return-contract.yaml` (F2); workflow states the contract is written for pre-creation STOPs |
```

Self-check (before the verdict): each AFTER line above was matched with an exact-string search (without its `>`) in the candidate and each BEFORE line (without its `<`) in the baseline. All 9 AFTER and all 9 BEFORE lines were found at the line numbers shown. No role swap.

## Prior blocking findings

| Id | Prior defect (R1:68-88, R1:233-234) | Status | Decided from the AFTER text |
|---|---|---|---|
| F1 | AC-1.1 and the P1 scope required a `## Unattended mode` section and the `--unattended` flag on every command in sections 3.1-3.2, which contradicts D3(a) (no pr-submit change), the load row (no report) and the phase order | **resolved** | AFTER S:195 now scopes the AC-1.1 test to "every command named in the P1 row of section 6, load excepted", and asserts "neither load nor any section-4 command has one". AFTER S:159 now limits the flag to "the commands named in this row, load excepted". AFTER S:76 now gives the section and the flag only "in the phase named in its row, not earlier", and excepts load. AFTER S:73 puts `--unattended` in the brief only "once the command's phase (section 6) has landed". I cross-checked the P1 row (S:159) against the phase column: the P1 rows in 3.2 are analyze, build, business-panel, design, document, explain, index, load, test (S:99,101,102,106-108,111,112,123) and the 3.1 P1 fixes are adversarial, cleanup-audit, index-repo, workflow (S:83,85,86,92); this is exactly the S:159 list (9 + 4). The P2 list at S:160 (15) equals the 11 P2 rows of 3.2 plus reflect, release-split, tdd, troubleshoot (S:88-91). The phase counts of 3.2 are 9 + 11 + 4 + 3 = 27 (S:99-125), unchanged. pr-submit's row phase is P4 (S:114) and D3(a) says "no pr-submit changes in Phase 4" (S:240); with AFTER S:76 ("in the phase named in its row") the two no longer conflict, and no P4 check asserts a pr-submit section unconditionally (AC-4.3 is conditional on D3, S:210). Between P1 and P2, auggie-review and cleanup do not yet accept the flag, so S:60 and S:67 are not contradicted. |
| F2 | WC-4's `<output-dir>/return-contract.yaml` contradicted the adversarial row (`<output>/adversarial/return-contract.yaml`), the workflow row (generated `<id>` directory) and live-check step 3 | **resolved** | Adversarial: AFTER S:83 and AFTER S:198 both now say `<output>/return-contract.yaml`, the same string as WC-4 (S:62), so step 3 (S:182) can pass for adversarial. `INV-A:35` still places the other artifacts under `<output>/adversarial/`, which WC-4's `artifacts` field covers (S:62). Workflow: AFTER S:62 names workflow as the one exception, AFTER S:73 says "not for workflow", AFTER S:76 and AFTER S:92 repeat it, and AFTER S:182 reads "for workflow, an existing `.dev/tasks/to-do/<id>/return-contract.yaml`". `INV-B:52` and `INV-B:272` confirm the generated `<id>` and "never overwrites or reuses an existing package". I grepped the candidate for "before dispatch": its only hits are S:62 (qualified), S:73 (qualified) and S:92 (the exception itself), so no unqualified universal claim is left. One residual gap in the workflow leg (pre-creation STOPs) is a requirement the text never states, not a contradiction; it is Medium M2 below. |

Counts: prior blocking findings 2; resolved 2; open 0; regressed 0.

## Findings on lines changed against the baseline

The changed lines are S:62, 73, 76, 83, 92, 159, 182, 195, 198 (whitespace-only changes ignored; there are none). Findings below are graded by consequence with the grading sentence of the FIRST-REVIEW grading check; none holds without a further assumption, so none is blocking.

| Id | origin | Graded | Where | One line |
|---|---|---|---|---|
| M1 | unchanged (quotes changed S:159, S:73, S:92) | Medium | S:196, S:159, S:112, S:92, S:86 | AC-1.2 runs the live check on "each P1 command" with `--output <dir>`, which load, workflow and index-repo cannot take |
| M2 | changed (S:62, S:92) | Medium | S:62, S:92, S:198, `INV-B:272` | Where workflow's contract goes on a pre-creation STOP is not stated, and how the worker learns `<id>` is marked UNVERIFIED |
| M3 | unchanged (quotes changed S:182) | Medium | S:182, S:194 | P0 step 3 asks for "the WC-4 contract path" before any contract exists |
| N6 | changed | minor | S:62, 73, 76, 83, 92, 159, 182, 195, 198 | Finding ids F1 and F2 are now cited inside the specification body |
| N7 | changed (S:73) | minor | S:73, S:84, S:87 | brainstorm and init-lite appear in no phase, so "once the command's phase has landed" never occurs for them |

### === REQUIREMENTS ANALYSIS ===

#### M1 (Medium, origin=unchanged) - AC-1.2 applies the contract live check to every P1 command, including commands the revision exempts or that take no output directory
- Expert: Wiegers (lead), Whittaker (zero/empty attack). Severity label: MAJOR, graded Medium. Priority: Medium. Quality impact: Testability +1.
- Quoted changed lines it depends on: AFTER S:159 ("the commands named in this row, load excepted"), AFTER S:73 ("the output directory, so the report path is known before dispatch (WC-4; not for workflow, F2)"), AFTER S:92 (workflow brief passes `--handoff none` only).
- Text: AC-1.2 (S:196, unchanged): "7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass". Step 4 of 7.2 (S:183) needs a contract file. load has "Report (WC-4): none" and "use it as a step inside another worker's brief, not as its own Task" (S:112); index-repo's brief passes no flag and its output location is "implied" (S:86); workflow takes no output directory (S:92, S:73).
- Why Medium: "each P1 command" can be read as the commands that run as their own Task (7.2 is defined "for each command under test", S:179), which excludes load. The implementer picks the worse of two readings the text allows, so the grading sentence needs a guess. This is the same class as the resolved F1, but here the text a reader would follow first (S:112) already tells them load is not a Task.
- Recommendation (follow-up only): name the P1 commands under live check in AC-1.2, leave out load, and say that workflow and index-repo run without `--output`.

#### M2 (Medium, origin=changed) - workflow's contract location on a pre-creation STOP, and how the worker learns `<id>`
- Expert: Nygard (lead), Fowler. Severity label: MAJOR, graded Medium. Priority: Medium. Quality impact: Completeness +1.
- Texts: AFTER S:62 says the worker "takes it from the package the command created (UNVERIFIED how the command reports `<id>`, `INV-B:272`; F2)" and WC-4 still requires the file "including stops before any other output exists". S:92 and AC-1.4 (AFTER S:198) still require workflow to write the contract for pre-creation STOPs. `INV-B:272` says the contract is "Not written for pre-creation STOPs" today and that `<id>` is a generated package. For such a STOP no package exists, so the path "from the package the command created" is empty.
- Why Medium: this is a requirement the document never states (where the file goes when there is no package), not a stated text that does harm. The reviser recorded the same gap (`review/revise1.md`, "Not changed"). F2 named only "known before dispatch", so this is outside the prior blocking scope.
- Consequence if built as written: a pre-creation STOP of `/sc:workflow` leaves no contract the coordinator can open; WC-5 then maps "no report exists" to `--outcome failed` (S:63), so the run still ends in a defined state, but without the blocked question.
- Recommendation (follow-up only): state in the workflow row where a pre-creation STOP is reported (for example, only in chat and `--outcome failed`), or narrow "every outcome" for workflow.

#### M3 (Medium, origin=unchanged) - P0 step 3 asks for a contract path that P0 does not have
- Expert: Adzic, Wiegers. Severity label: MAJOR, graded Medium. Priority: Low. Quality impact: Consistency +1.
- Quoted changed line: AFTER S:182 ("its report path is the WC-4 contract path (for workflow, an existing `.dev/tasks/to-do/<id>/return-contract.yaml`, F2)").
- Text: AC-0.4 (S:194, unchanged) requires "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1". For `/sc:troubleshoot` the report today is `REPORT.md` (S:91) and for adversarial the contract filename is "not fixed" (S:83 before P1). Step 3 still compares the `worker_done` report path to "the WC-4 contract path", which does not exist in P0 for those two. Only workflow has the file in P0 (`INV-B:272`).
- Why Medium: the exemption sentence for step 4 reads naturally as covering step 3 too; the implementer must guess.
- Recommendation (follow-up only): in AC-0.4 extend the exemption to "steps 3 and 4".

### === ARCHITECTURE ANALYSIS ===

No new architecture finding on the changed lines. The F2 repair keeps one contract name and path rule (`<output-dir>/return-contract.yaml`), adds one stated exception, and does not move any responsibility between the command, the worker session and the coordinator (Owner column, S:57-70, unchanged). Fowler's boundary check: the exception for workflow is stated at its source (WC-4, S:62), at the consumer (S:73, S:182) and at the row (S:92), so the three places that must agree do agree.

### === ADVERSARIAL ANALYSIS (Whittaker) ===

Probes were run only against the changed lines and the prior blockers.

1. I can break this specification by **Divergence Attack**. The invariant at **S:76 ("the phase named in its row") against S:159 and S:160** was probed at the boundary: a ready-today command whose small fix is "None" (brainstorm S:84, init-lite S:87) has no phase. Concrete attack: before, brainstorm gets no section and no flag; after the edit the same, and S:73 says the flag goes in the brief "once the command's phase has landed", which never happens. Result: the text is silent, the behaviour is inferrable (the brief omits the flag), so MINOR (N7). No state corruption.
2. I can break this specification by **Sequence Attack**. The invariant at **S:154 (a later phase starts after the earlier phase's checks pass) with AC-1.1 (S:195)** was probed with the order P1 then P2: before the edit AC-1.1 required P2-P4 sections during P1; after the edit it requires only the P1-row commands, and P2's own AC-2.1 (S:199) adds the per-gate assertions. The out-of-order case (P2 command edited during P1) is excluded by "not earlier" (S:76). The invariant holds.
3. I can break this specification by **Sentinel Collision Attack**. The invariant at **S:62 "one exception"** was probed for another command whose contract directory is not "the directory the coordinator passed": tdd and init-lite take a file-valued `--output` (S:87, S:90), cleanup-audit's directory is fixed (S:85), research writes a generated `claudedocs/` path (S:116). Concrete attack: the text says there is "one exception", but the contract directory for these is not stated. This is the pre-existing F4 (Medium, R1:96-99), not a regression; the path stays derivable before dispatch for all but workflow.
4. Zero/Empty and Accumulation attacks on the changed lines found nothing the prior report has not already recorded.

### === GUARD CONDITION BOUNDARY TABLE ===

Scope for a re-review: guards on changed lines only. The changed lines contain two guards: the phase gate "once the command's phase has landed / not earlier" (S:73, S:76) and the workflow exception to "known before dispatch" (S:62, S:73, S:182). Nygard built it, Crispin checked completeness, Whittaker attacked entries. Classes left out are named in the note after the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `phase_landed` | S:73, S:76 | Zero/Empty | command with no phase row (brainstorm, init-lite) | never true | no section, no flag; the brief omits `--unattended`; inferrable | OK |
| `phase_landed` | S:73, S:76 | One/Minimal | command in P1 (analyze), P1 check not yet passed | true once P1 lands | section and flag added in P1 only | OK |
| `phase_landed` | S:73, S:76 | Typical | command in P2 (tdd), P2 not landed | false | flag not in the brief; P0/P1 live checks run without it | OK |
| `phase_landed` | S:76, S:159 | Legitimate Edge Case | load (P1, "usage line only") | true for the usage line, excepted for section and flag | AFTER S:76 and S:159 except load explicitly | OK |
| `phase_landed` | S:76, S:114, S:240 | Legitimate Edge Case | pr-submit under D3(a) | false in P4 | no change under D3(a); phase-named rule agrees | OK |
| `contract_path_known` | S:62, S:73 | Typical | analyze with `--output <dir>` | true | `<dir>/return-contract.yaml` | OK |
| `contract_path_known` | S:62, S:83, S:198 | Legitimate Edge Case | adversarial with `--output <dir>` | true | `<dir>/return-contract.yaml`, same in all three places | OK |
| `contract_path_known` | S:62, S:92, S:182 | Legitimate Edge Case | workflow, post-creation outcome | false before dispatch | path taken from the created package; step 3 checks an existing file; how `<id>` is reported is UNVERIFIED | OK |
| `contract_path_known` | S:62, S:92, S:198 | Zero/Empty | workflow, pre-creation STOP (no package) | undefined | not stated where the contract goes (M2) | GAP |
| `contract_path_known` | S:62, S:87, S:90 | Legitimate Edge Case | tdd or init-lite with a file-valued `--output` | undefined | not stated (carried from F4, unchanged text) | GAP |

Classes omitted, each with its reason: `phase_landed` Maximum/Overflow (a phase is a label, not a capacity) and Sentinel Value Match (no sentinel value is defined); `contract_path_known` One/Minimal (no scalar to vary), Maximum/Overflow (a path has no capacity in the spec) and Sentinel Value Match (no sentinel value is defined). Both GAP rows are graded Medium (M2 for the first; the second is the prior Medium F4, whose text is not on a changed line). Neither names a concrete wrong outcome that follows from the stated text without a guess, so FR-8 and FR-9 give no blocking finding.

## Coverage statement

Covered:
- All of S:1-285 read in full, and the full diff (9 changed lines).
- Every changed line (S:62, 73, 76, 83, 92, 159, 182, 195, 198) against the prior blocking findings F1 and F2, and against every line that depends on it: S:57-70 (WC rules), S:79, S:99-125 (phase column), S:149 (SA-4), S:154-162 (phases), S:166-210 (checks), S:238-247 (D3, D4).
- Count conservation after the edit: 43 = 10 + 27 + 6 (S:76, unchanged); phases of 3.2 = 9 + 11 + 4 + 3 = 27; P1 row = 9 + 4 commands, each matching a P1 phase cell; P2 row = 15, each matching a P2 phase cell. No mismatch.
- Inventory lines checked for the changed claims: `INV-B:52` and `INV-B:265-276` (workflow row and section, including "Not written for pre-creation STOPs"), `INV-A:35` and `INV-A:58-63` (adversarial artifacts and return-contract location). They support the spec's statements.
- Pipeline Dimensional Analysis (FR-17): not triggered; no multi-stage data flow with differing counts. No Quantity Flow Diagram.

Not covered / UNVERIFIED (not in the workspace): every `cmd/`, `sk/`, `ag/`, `src/` line cited in the changed rows, `EVIDENCE.md`, `CLAUDE.md`, the Orca guide text; the claims at S:11 and S:285 (about 340 citations re-read, 9 defects fixed); whether `/sc:workflow` can report its generated `<id>` to the worker; the real status words in existing contracts (prior F9). Text outside the changed lines and the prior blockers was not re-reviewed: this is a scoped review. The prior Medium findings F3-F14 and notes N1-N5 (R1:90-123, R1:124-157, R1:217-223) were not re-opened; F5 is partly met by AFTER S:73 ("once the command's phase has landed"), and the rest are unchanged against the baseline.

Review-loop handling: no brief clause was overridden, and the brief did not widen scope. The brief did not pass `--unattended` or `--report-dir`, so no `return-contract.yaml` is written (the brief says write only this file). The one-time question "open an issue for the follow-up candidates?" is left to the coordinator, because this session has no user channel; nothing was created. A severe older defect was searched for (the instruction to record one if newly discovered): none found; M1 and M3 are older but not severe.

## Follow-up candidates (Medium and minor; none triggers a revision)

Medium: M1, M2, M3. Minor: N6 (finding ids F1 and F2 now sit inside the spec text at S:62, 73, 76, 83, 92, 159, 182, 195, 198 and will dangle once the review files are archived; delete them when the loop ends), N7 (brainstorm and init-lite never get the flag; S:73 could say "if the command has a phase row"). Carried unchanged from round 1 and still open as Medium follow-ups: F3, F4, F6, F7, F8, F9, F10, F11, F12, F13, F14 (R1:225-227); F5 is partly addressed. Minor notes N1-N5 are unchanged. Under the loop rules the coordinator asks the user once whether to open an issue for these; this run created none.

## Coverage line

scoped PASS: changed lines + prior blockers

## Reviser brief

None: no blocking finding is open, so no revision is requested. Restated for completeness: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after with bytes added and deleted per finding id. Medium and minor findings (M1-M3, N6, N7, and the carried F3-F14) are not to be edited under this brief, including through "apply all findings".

verdict: PASS
