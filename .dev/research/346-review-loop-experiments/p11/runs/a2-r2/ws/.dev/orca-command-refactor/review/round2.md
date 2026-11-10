review: 2 of 3

# Spec-panel re-review: orca-worker-contract-spec.md (round 2)

Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md`
Candidate not edited. No other review started. Only this file was written.

## Roles and inputs (fixed)

| Role | File | sha256 |
|---|---|---|
| CANDIDATE (`@file`) | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (58349 bytes, 285 lines) | `49b44eed9e9476353afbf46c4ab057a94b41cde7cfd310c3fc03ba949d765180` |
| BASELINE (`--baseline`) | `.dev/orca-command-refactor/specs/history/spec-v1.md` (57763 bytes, 285 lines) | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` |
| PRIOR (`--re-review`) | `.dev/orca-command-refactor/review/round1.md` (`review: 1 of 3`, `verdict: FAIL`, blocking B1 and B2) | `69b71779e1b2d4761302f324e4d586307fd2e159b38a274e5fcc9b6fd42e664c` |

The baseline hash equals the hash round 1 recorded for its candidate (`round1.md:6`), so the baseline is the text round 1 reviewed. All three inputs are readable and non-empty; the prior report has a `review: 1 of 3` header, so N = 1 + 1 = 2.

Citation keys: `S:N` = line N of the candidate; `B:N` = line N of the baseline; `R1:N` = line N of PRIOR; `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `CMD:N` = line N of `command.md` (the panel command); `REV:N` = line N of `review/revise1.md`. Every citation to a file outside the workspace (`src/`, `CLAUDE.md`, `EVIDENCE.md`, `.dev/codegraph-migration/`, `cmd/` and `sk/` lines not echoed in an inventory) is UNVERIFIED.

## Step 1. Evidence block (`diff -w BASELINE CANDIDATE`)

Command run: `diff -w specs/history/spec-v1.md specs/orca-worker-contract-spec.md`. Not empty: 5 changed lines (hunks `62c62`, `76c76`, `83c83`, `92c92`, `195c195`; no line added or removed). Lines copied verbatim.

### BEFORE (baseline)

~~~~text
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
< The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
< | adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
< | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
~~~~

### AFTER (candidate)

~~~~text
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<contract-dir>/return-contract.yaml`, where `<contract-dir>` is the brief's `--output-dir` or directory-valued `--output`, or the parent directory of a file-valued `--output` (tdd, init-lite); an output flag added in P1-P3 is directory-valued, and a command that writes its contract elsewhere today also writes it here (adversarial, workflow, section 3.1). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
> The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<contract-dir>/return-contract.yaml`. Every changed command except `load` (no contract, row below) also gains the `## Unattended mode` section (section 2.1), in the phase its row names. Phase numbers refer to section 6.
> | adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Write the contract at `<output>/return-contract.yaml`, the WC-4 path; the skill names no file today (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
> | workflow | `--handoff none`; an output directory (new `--output-dir` flag, P1) | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Also write the contract to `<output-dir>/return-contract.yaml`, including for pre-creation STOPs (WC-4 "every outcome"), since `<id>` is unknown before dispatch (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `load` and the P4 commands (implement, post-release, pr-submit, which get theirs in P4 after D2-D4) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that `load` and no section-4 command has one | passes |
~~~~

Line map (same in both files): `62` = WC-4 row; `76` = section 3 preamble; `83` = adversarial row; `92` = workflow row; `195` = AC-1.1 row.

## What was covered

- Read in full: the candidate (285 lines), the baseline, PRIOR, `review/revise1.md`, README, `command.md`; read the inventory lines the changed text cites or depends on (`INV-A:35,39,51,55,60-61`, `INV-B:36,47,52,97-135,177-185,197-235,247-276`).
- Experts run, fixed order: Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard, Newman, Hohpe (architecture); Whittaker (active in every panel review). Crispin, Gregory, Hightower are outside the two focus areas and were not run.
- Scope: the 5 changed lines, the two prior blocking findings, and the text that depends on the changed lines (S:154, S:159, S:73, S:69, S:84, S:87, S:99-125, S:182, S:196-200, S:208-210, S:240, S:265). Inherited text is cited only through the changed line it depends on (Review Loop bullet 5). The 13 Medium findings M1 to M13 and N1 to N8 of round 1 were not acted on by the reviser (REV:25-26) and are not re-graded here; the changed lines do not touch their text except where stated below.
- `rf-qa.md` (Review Loop bullet 5, steps 1-5 of its Fix Cycle process): not present in the sandbox (`ws/.claude/agents/` and `home/.claude/agents/` do not exist), so it is unread; the rules in Review Loop bullet 5 were applied alone, as the command allows.
- Grading rule: command bullet 2 makes FR-8/FR-9 findings blocking. As in round 1, the brief ("Report concrete wrong outcomes ... list Medium and minor findings under follow-up candidates") narrows that: a table GAP becomes blocking only if it names a concrete wrong outcome that needs no further assumption; otherwise Medium. Bullet 7 allows a brief to narrow and not to widen; the coordinator should know this choice was made.
- Not covered: the commands' own behaviour (files outside the workspace), Orca internals beyond `CAPS`, any live run, and the `.dev/` wording of the Decisions rows other than the ones cited.

## Table 1. Prior blocking findings

| Id | Prior defect (R1) | AFTER text compared | Status |
|---|---|---|---|
| B1 | AC-1.1 (B:195) required a `## Unattended mode` section on `load`, which the load row (S:112) and Decisions (S:265) say has no contract; and on implement, post-release and pr-submit before D2-D4 (R1:98-103). | S:195 AFTER: "every command in sections 3.1-3.2 except `load` and the P4 commands (implement, post-release, pr-submit, which get theirs in P4 after D2-D4) ... and that `load` and no section-4 command has one". S:76 AFTER: "Every changed command except `load` (no contract, row below) also gains the `## Unattended mode` section". Load row S:112 ("none (see note)") and S:265 are unchanged and now agree with both. | **resolved** for the two cases R1 named. The same edit introduced a new contradiction, B3 below. |
| B2 | WC-4 (B:62) put the contract at `<output-dir>/return-contract.yaml` for the passed `--output`/`--output-dir`; four cases contradicted it: tdd and init-lite file-valued `--output`, adversarial subdirectory, workflow generated id and pre-creation STOP, spec-panel `--output` of unstated type (R1:138-143). | S:62 AFTER defines `<contract-dir>`: "the brief's `--output-dir` or directory-valued `--output`, or the parent directory of a file-valued `--output` (tdd, init-lite); an output flag added in P1-P3 is directory-valued, and a command that writes its contract elsewhere today also writes it here (adversarial, workflow, section 3.1)". Case 1: AC-2.2 (S:200) `/sc:tdd "auth" --unattended --output <file>` now has a derivable path (the parent directory). Case 2: S:83 AFTER writes `<output>/return-contract.yaml`. Case 3: S:92 AFTER adds an `--output-dir` (P1) and writes there "including for pre-creation STOPs ... since `<id>` is unknown before dispatch" (INV-B:272 says the package contract is not written for pre-creation STOPs; INV-B:52 lists no output flag for workflow). Case 4: S:120 "add `--output`" falls under "an output flag added in P1-P3 is directory-valued". 7.2 step 3 (S:182) and AC-1.2 (S:196) cite "the WC-4 contract path", which now resolves to one rule. | **resolved** for the four cases R1 named. Residuals that the new rule leaves are Medium (M14 to M17). |

## Guard Condition Boundary Table (hard gate FR-10: complete before synthesis)

Re-review scope: guards on changed lines only (Review Loop bullet 5). Guards: G1 `contract_dir` (S:62), G2 `ac11_section_set` (S:76, S:195), G3 `workflow_contract_site` (S:92). 3 guards x 6 rows, all cells populated.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 `contract_dir` | S:62 | Zero/Empty | `--unattended`, brief has no `--output`, `--output-dir` or added output flag (research S:116, review-translation S:117, validate-tests S:125, task S:121 name none) | no source for `<contract-dir>` | Unspecified: S:62 derives the directory only from those flags; the rows name a file or "contract naming ..." and no flag | GAP |
| G1 | S:62 | One/Minimal | `--output ./TDD.md` (parent `.`) | file-valued | Contract at `./return-contract.yaml` (parent-directory clause) | OK |
| G1 | S:62, S:200 | Typical | `--output-dir <d>`, or `--output <file>` for tdd (AC-2.2) | directory or file | `<d>/return-contract.yaml`, or the file's parent directory | OK |
| G1 | S:62, S:69 | Maximum/Overflow | two workers whose file-valued `--output` values share a parent (tdd default is `docs/[domain]/TDD_[COMPONENT-NAME].md`, INV-B:222) | same `<contract-dir>` | Both write `<parent>/return-contract.yaml`; S:69 (WC-11) says two workers never write the same file; no rule picks distinct parents | GAP |
| G1 | S:62 | Sentinel Value Match | brief passes both `--output-dir` and `--output`, or an added flag whose name equals an existing file-valued one (spec-panel, see N9) | two candidate directories | Unspecified which flag wins | GAP |
| G1 | S:62, S:83 | Legitimate Edge Case | adversarial or workflow, which "also" write the contract "here" | contract elsewhere today | S:62 says "also writes it here"; S:83 says "Write the contract at `<output>/return-contract.yaml`" with no second copy; S:92 says "Also write" | GAP |
| G2 `ac11_section_set` | S:76, S:112, S:195 | Zero/Empty | `load` (no contract) | excluded | Excluded in both S:76 and S:195; asserted to have none | OK |
| G2 | S:195, S:240 | One/Minimal | one P4 command, pr-submit under recommended D3(a) ("no pr-submit changes in Phase 4") | excluded from AC-1.1 | S:195 says P4 commands "get theirs in P4"; under D3(a) pr-submit gets none and no P4 check (S:208-210) asserts any P4 section | GAP |
| G2 | S:76, S:99, S:195 | Typical | analyze (row phase P1) at the P1 check | has section | Section lands in P1, asserted in P1 | OK |
| G2 | S:76, S:100, S:154, S:195 | Maximum/Overflow | auggie-review (row phase P2) at the P1 check; likewise the other 14 P2 commands and the 4 P3 commands | section due in P2, asserted in P1 | S:76 puts the section in "the phase its row names"; S:195 asserts it in P1; S:154 blocks P2 until P1 passes | GAP (B3) |
| G2 | S:76, S:84, S:87, S:195 | Sentinel Value Match | brainstorm and init-lite ("Small fix: None", no phase named) | in AC-1.1 set, in no phase | S:195 asserts a section; S:76 gives it only to "changed" commands in "the phase its row names"; S:79 says the only changes are the small fixes | GAP (B3) |
| G2 | S:76, S:159, S:195 | Legitimate Edge Case | command whose P1 scope is "flag accepted" only (S:159) | flag, no gate | Not stated whether its P1 section may be a stub | GAP |
| G3 `workflow_contract_site` | S:92 | Zero/Empty | brief omits `--output-dir` (the P0 smoke run, S:194) | no new copy | P0 uses the package contract; S:92 starts at P1 | OK |
| G3 | S:92 | One/Minimal | STOP before the package exists, `--output-dir` passed | `<id>` unknown | Contract written to `<output-dir>/return-contract.yaml` | OK |
| G3 | S:92 | Typical | successful run, `--output-dir` passed | both copies | Package copy "stays as today" plus the `<output-dir>` copy (S:62, S:92) | OK |
| G3 | S:92 | Maximum/Overflow | `--output-dir` missing, unwritable or a file | cannot write | Unspecified (the round 1 zero/empty case M12, now also on S:92) | GAP |
| G3 | S:79, S:92 | Sentinel Value Match | the 3.1 header says these commands "run as workers now if the brief uses the stated flags"; workflow's stated flag `--output-dir` does not exist until P1 | flag not yet present | Workflow is "ready today" only without the new flag; S:92 marks the flag "new ... P1" | OK |
| G3 | S:92, S:196 | Legitimate Edge Case | `worker_done --report-path` for workflow | two copies | WC-4 passes "the contract path" (S:62); the `<contract-dir>` copy is the WC-4 path by S:76 | OK |

GAP rows: 8 on changed lines (G1 x4, G2 x3, G3 x1), plus 1 G2 stub-row noted. Carried into findings: G2 rows 4 and 5 to B3 (blocking); G1 row 4 to M14; G1 row 1 to M16; G1 row 6 to N10; G2 row 2 to M18; G1 row 5 to N9; G2 row 6 and G3 row 4 to notes (no concrete wrong outcome). Table is complete; synthesis proceeds.

## Quantity Flow Diagram (FR-21)

Pipeline Dimensional Analysis applies: the commands pass through a 3-way split and a 5-phase rollout, and AC-1.1 is a consumer of those counts.

```text
[cmd/ commands: 43 (S:76)] --> [Classify] --> [3.1 ready: 10][3.2 change: 27][S4 coordinator-only: 6]   10+27+6 = 43
        |
        v
[AC-1.1 set at the P1 check (S:195): 3.1 + 3.2 = 37, minus load (1), minus P4 implement/post-release/pr-submit (3) = 33 sections asserted]
        |-- Producer by S:76 "in the phase its row names", sections due by the end of P1:
        |     3.2 rows phase P1, load excluded: analyze, build, business-panel, design, document, explain, index, test = 8
        |     3.1 rows with a P1 fix: adversarial, cleanup-audit, index-repo, workflow = 4
        |     = 12
        |-- brainstorm, init-lite: in the 33, named in no phase = 2
        |-- due in P2: 11 (3.2) + 4 (3.1: reflect, release-split, tdd, troubleshoot) = 15
        |-- due in P3: roadmap, save, validate-roadmap, validate-tests = 4
        |-- due in P4 (excluded from 33): 3;  load: 1;     12 + 2 + 15 + 4 + 3 + 1 = 37
        v
[Consumer AC-1.1 expects 33 at P1; producer yields 12 (14 with the two unphased)]   <-- MISMATCH 33 vs 12 (B3)
[S:154: P2 does not start until the P1 checks pass]  --> P1 cannot pass, P2 cannot start
```

Severity per FR-19: CRITICAL (B3).

=== REQUIREMENTS ANALYSIS ===
Experts: Wiegers (lead), Adzic, Cockburn.

### B3 CRITICAL, blocking. S:76 puts each `## Unattended mode` section in "the phase its row names"; AC-1.1 asserts them all at P1 (origin=changed)
- Issue: the revision added "in the phase its row names" to S:76 (AFTER line 76) and rewrote AC-1.1 (AFTER line 195) so that it exempts `load` and the three P4 commands only. The phase column (S:99-125) names P2 for 11 commands and P3 for 4; the 3.1 small-fix column names P2 for reflect, release-split, tdd and troubleshoot (S:88-91). AC-1.1 is a P1 check (S:195) over "every command in sections 3.1-3.2" except the exempt ones, so at the P1 check it asserts 33 sections (QFD) while S:76 makes only 12 due (14 counting brainstorm and init-lite, whose rows name no phase: S:84, S:87). S:154 says "Later phases do not start until the earlier phase's checks in section 7 pass". The exemption lists only P4 because that was the case R1 named (R1:102); the same reasoning applies to P2 and P3 and the revised text does not apply it.
- Severity: CRITICAL. Expert: Wiegers (traceability, testability), Adzic, Cockburn. Priority: High. Quality impact: Consistency 7 to 5 (new contradiction), Testability.
- Grading sentence: An implementer who follows S:76 as written adds auggie-review's `## Unattended mode` section in P2 (its row names P2, S:100), so the P1 test AC-1.1 fails on auggie-review and the other 14 P2 and 4 P3 commands, and S:154 then forbids starting P2; an implementer who instead writes every section in P1 breaks S:76's own "in the phase its row names". Two stated texts contradict, so the finding is blocking with no further assumption. It is not covered by B1's fix: B1 asked that AC-1.1 agree with the rows it tests (R1:103), and after the edit it still does not agree with the phase of 19 rows.
- Second case, same defect: brainstorm and init-lite are in AC-1.1's set (3.1, S:195) but are not "changed" (S:79: "The only command changes are the small fixes"; both rows say "None", S:84, S:87) and S:76 gives the section only to a changed command in a named phase. That part of the set mismatch existed in the baseline (round 1 N1) and is cited here only because it falls under the changed clause of S:76.
- Whittaker, Sequence Attack: run P1 to completion as S:76 prescribes; before, `uv run pytest tests/skills/test_worker_contract.py -q` has 0 failures; after P1, AC-1.1 fails for 19 commands (15 P2, 4 P3) and the gate on S:154 holds P2 closed.
- Recommendation: make AC-1.1 phase-scoped so that each phase's check asserts the sections of the commands that phase's rows name (P1: its 12; P2: its 15; P3: its 4; P4: after D2-D4), or delete "in the phase its row names" from S:76 and state that every section except `load`'s and the P4 commands' lands in P1. Name the phase for brainstorm and init-lite either way. Rationale: the acceptance test must agree with the rows it tests (R1:103).

=== ARCHITECTURE ANALYSIS ===
Experts: Fowler (lead), Nygard, Newman, Hohpe.

No new blocking finding. B2's fix is consistent with the rows it names (Table 1). The residuals below come from the new rule, not from the old defect.

## Follow-up candidates (Medium, not blocking)

- **M14 (origin=changed). Parent-directory rule can make two workers share one contract file** (G1 row 4). S:62 AFTER derives `<contract-dir>` from the parent directory of a file-valued `--output`. tdd's default output is `docs/[domain]/TDD_[COMPONENT-NAME].md` (INV-B:222), so two tdd workers for components of one domain write `docs/<domain>/return-contract.yaml`, and S:69 (WC-11) says two workers in one worktree never write the same file. Wrong outcome: the second worker's contract overwrites the first's, and the coordinator reads the wrong `status`. It needs the coordinator to pass sibling outputs, and S:73 lets the coordinator choose the directory, so Medium. Fix: say a file-valued `--output` must sit in a directory of its own, or name the contract after the output stem.
- **M15 (origin=changed). Adversarial's contract moves up one directory** (S:83 AFTER). Today it sits in `<output>/adversarial/` in real runs (INV-A:35,60), next to 6 artifacts. Parents that invoke adversarial (brainstorm, release-split, reflect Tier 2, cli-eval create: INV-A:39,44; INV-B:112,119) write their own `<output>/return-contract.yaml` (S:84, S:88). If a parent passes its own `--output` to the nested adversarial, both would write `<output>/return-contract.yaml`. Whether they pass the same directory is UNVERIFIED (not in the inventories). Medium, UNVERIFIED.
- **M16 (origin=unchanged, depends on changed S:62). Rows that name no output flag have no `<contract-dir>`** (G1 row 1). research (S:116), review-translation (S:117), task (S:121), validate-tests (S:125) and implement ("beside the ledger", S:109) give the contract a place by prose, not by a flag the brief passes; S:62 AFTER derives the directory only from the brief's `--output-dir`/`--output` or "an output flag added in P1-P3". Rows that say "add a report path" (S:101, S:103, S:110, S:123) or "write ... to a file" (S:108, S:115) do not say the added flag is a directory, which S:62 now requires. Medium: the document never states the flag for these rows.
- **M17 (origin=changed). Workflow is "ready today" only with a flag that does not exist yet.** S:79 says the 10 commands "run as workers now if the brief uses the stated flags"; workflow's stated flags (S:92) now include a new `--output-dir` (P1). Before P1 only the package contract exists. Whether `/sc:workflow` already has an output flag is UNVERIFIED (`INV-B:52` lists none).
- **M18 (origin=changed). No check asserts the P4 sections, and D3(a) gives pr-submit none.** S:195 AFTER says implement, post-release and pr-submit "get theirs in P4 after D2-D4"; AC-4.1 to AC-4.3 (S:208-210) do not assert a section, and D3(a), the recommended answer, says "no pr-submit changes in Phase 4" (S:240).
- M1 to M13 of round 1 (R1:237) remain as listed there; the revision did not touch them (REV:25-26). M4 (flag accepted in P1 before its gate row lands, S:159) is the one that interacts with B3: it is unchanged and still Medium.

Minor notes (never fail the review):
- N9 The panel command in this sandbox already lists `--output <file>` and `--report-dir` for spec-panel and says "`--output` is file-valued" (CMD:22, CMD:456), while the spec row says spec-panel gets a new `--output` (S:120) because INV-B:182 saw no output flag. Under S:62 AFTER either reading yields a derivable directory (added flag is a directory, or a file's parent), so there is no wrong outcome; the row is stale or the flag clashes with an existing one. The panel command is not part of the inventory evidence, so this is UNVERIFIED as evidence about `cmd/spec-panel.md`.
- N10 S:62 AFTER says a command that writes its contract elsewhere today "also writes it here (adversarial, workflow ...)"; for adversarial the skill names no file today (INV-A:35,60) and S:83 says only "Write ... at `<output>/return-contract.yaml`". The words "also" and the row differ on whether a second copy exists.
- N11 The quantities in REV:7-9 reconcile with the files: baseline 57763 bytes and candidate 58349 bytes (net +586) match `wc -c` run here; the edited lines (62, 76, 83, 92, 195) match the five diff hunks, so the reviser touched nothing else.
- N12 UNVERIFIED here (outside the workspace): every `cmd/` and `sk/` line in the changed lines (S:83 `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`, S:92 `sk/sc-workflow-protocol/...`), `pyproject.toml:38` (S:183), and the claim in S:285 that 340 citations were checked.

## Quality assessment and consensus

```yaml
specification_review:
  original_spec: ".dev/orca-command-refactor/specs/orca-worker-contract-spec.md"
  sha256: "49b44eed9e9476353afbf46c4ab057a94b41cde7cfd310c3fc03ba949d765180"
  baseline_sha256: "d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d"
  review_date: "2026-11-10"
  review: "2 of 3"
  expert_panel: [Wiegers, Adzic, Cockburn, Fowler, Nygard, Newman, Hohpe, Whittaker]
  focus_areas: [requirements, architecture]
quality_assessment:
  overall_score: 7.0
  clarity: 7
  completeness: 6
  testability: 6
  consistency: 7
critical_issues:
  - {id: B3, category: requirements, severity: CRITICAL, expert: Wiegers, issue: "AC-1.1 (P1) asserts sections that S:76 schedules for P2 and P3; P1 cannot pass and S:154 holds P2 closed", recommendation: "phase-scope AC-1.1 or drop the phase clause from S:76"}
expert_consensus:
  - "B1 and B2 are fixed for the cases round 1 named; the one-rule WC-4 path is a clear improvement (Fowler, Newman)."
  - "The B1 edit and the B2 edit were made without changing the P1 scope text, which leaves the section schedule and its acceptance test out of step (Wiegers, Adzic)."
improvement_roadmap:
  immediate: [B3]
  short_term: [M14, M16]
  long_term: [M15, M17, M18]
adversarial_analysis: "see B3 (Sequence Attack) and Table G1/G2/G3"
```

## Reviser brief

Blocking finding ids: B3. Contract for the reviser (restating Review Loop bullet 6): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; report the byte size of the candidate before and after. B3 names S:76 (the clause "in the phase its row names") and S:195 (AC-1.1, together with the phases of brainstorm and init-lite); S:154 and the rows are not to be edited. Do not act on M14 to M18, M1 to M13 or N1 to N12 in this cycle. One fix cycle remains after this one (the next report is `review: 3 of 3`).

## Self-check before the verdict

Run with `grep -nxF -- "<line without the > or <>" FILE`, stricter than `-nF` (whole-line match).
- Each AFTER line (without `>`) found in CANDIDATE: line 62, 76, 83, 92, 195, all found; 0 of the 5 found in BASELINE.
- Each BEFORE line (without `<`) found in BASELINE: line 62, 76, 83, 92, 195, all found; 0 of the 5 found in CANDIDATE.
- Roles confirmed, no swap. `diff -w` reports hunks 62c62, 76c76, 83c83, 92c92, 195c195 only.
- The AFTER text is not consistent with every requirement that depends on it: S:76 and S:195 contradict each other and S:154 (B3). That alone blocks a PASS.

verdict: FAIL
