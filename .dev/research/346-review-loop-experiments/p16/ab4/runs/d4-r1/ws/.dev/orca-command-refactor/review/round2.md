review: 2 of 3

# Re-review of the revised Orca worker contract spec (/sc:spec-panel --mode critique --focus requirements,architecture --re-review)

- candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md, sha256 62a2931158ca12b901593ce928e457d6e9134501cf22528ef812325749ee0041
- baseline: .dev/orca-command-refactor/specs/history/spec-v1.md, sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d (equals the candidate hash recorded in the prior report, round1.md:5)
- prior: .dev/orca-command-refactor/review/round1.md, sha256 479fac8f6c2214e132e40fd1af00d28f3f13890b3fd8dbf7253bc7f70cb07223, header `review: 1 of 3` (round1.md:1), so N = 2
- lint: .dev/orca-command-refactor/review/lint-2.md, sha256 of lint file not recorded by the tool; it names the candidate sha 62a29311... (lint-2.md:1), matching the candidate hash. Checks: REF. Findings: 0 (lint-2.md:3-5), so there is no lint id to confirm or dismiss.
- reviewer model actually used: claude-sonnet-5-5
- mode: critique, focus requirements,architecture; experts in fixed order (Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower), reviewing the changed lines and the prior blockers only
- rules applied: Review Loop bullets 1-7 of command.md; RE-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full). The rf-qa Fix Cycle file (`.claude/agents/rf-qa.md`, `~/.claude/agents/rf-qa.md`) does not exist inside the sandbox and was not read; the rules of Review Loop bullet 5 stand alone (UNVERIFIED against rf-qa steps 1-5).
- brief clauses overridden: none. The brief narrows nothing and widens nothing.
- README context read: `.dev/orca-command-refactor/README.md` (planning only; evidence limited to the files under inventory/; any citation to a file outside the workspace is UNVERIFIED here).

## Step 1: evidence block (diff -w BASELINE CANDIDATE)

Changed candidate lines: 62, 76, 92, 149, 159, 194-196, 198, 200 (20 diff lines). Whitespace-only changes are ignored by `diff -w`.


### hunk 62c62

BEFORE (baseline)
```text
| WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
```
AFTER (candidate)
```text
| WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. **Exceptions (M5):** adversarial `<output-dir>/adversarial/return-contract.yaml`; cleanup-audit `.claude-audit/return-contract.yaml` (fixed output dir, no `--output`); index-repo beside `PROJECT_INDEX.md`, at the location its P1 fix states; workflow `.dev/tasks/to-do/<id>/return-contract.yaml`, where the command generates `<id>`, so the worker reads the path from the command's output and a stop before the package exists writes no contract (WC-5 then applies: no report, `--outcome failed`). | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
```

### hunk 76c76

BEFORE (baseline)
```text
The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
```
AFTER (candidate)
```text
The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command except load (M3) also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
```

### hunk 92c92

BEFORE (baseline)
```text
| workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
```
AFTER (candidate)
```text
| workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | None | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
```

### hunk 149c149

BEFORE (baseline)
```text
| SA-4 | Command-file edits in Phases 1-3 are additive: a new `## Unattended mode` section and new flags. Existing lines change only where section 3 names a defect fix (roadmap and validate-roadmap drift, validate-tests target, adversarial and workflow contract gaps, explain tools, business-panel frontmatter, load usage line), and each such fix must keep the standalone behaviour or correct a documented defect. | Keeps the diff reviewable and SA-1 checkable. | Section 3 "Other required change" column |
```
AFTER (candidate)
```text
| SA-4 | Command-file edits in Phases 1-3 are additive: a new `## Unattended mode` section and new flags. Existing lines change only where section 3 names a defect fix (roadmap and validate-roadmap drift, validate-tests target, adversarial contract gap, explain tools, business-panel frontmatter, load usage line), and each such fix must keep the standalone behaviour or correct a documented defect. | Keeps the diff reviewable and SA-1 checkable. | Section 3 "Other required change" column |
```

### hunk 159c159

BEFORE (baseline)
```text
| **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
```
AFTER (candidate)
```text
| **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 except load (M3) (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
```

### hunk 194,196c194,196

BEFORE (baseline)
```text
| P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
```
BEFORE (baseline)
```text
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
```
BEFORE (baseline)
```text
| P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
```
AFTER (candidate)
```text
| P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1, 2 and 5-7 pass; in steps 3 and 4 (M1, M2) the report is the command's existing report file, since the contract arrives in P1: step 3 compares `--outcome` with that file's own status and checks that the reported path is that file, and step 4 is `test -s` on it. Record the results in the phase report; a failure here reopens section 1 |
```
AFTER (candidate)
```text
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except load (M3) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
```
AFTER (candidate)
```text
| P1 | AC-1.2 | 7.2 live check on each P1 command except load (M3) with `--unattended --output <dir>`, omitting `--output` for a command with none (WC-4 exceptions, M5) | all steps pass |
```

### hunk 198c198

BEFORE (baseline)
```text
| P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |
```
AFTER (candidate)
```text
| P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` | adversarial names one fixed path (the WC-4 exception) |
```

### hunk 200c200

BEFORE (baseline)
```text
| P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |
```
AFTER (candidate)
```text
| P2 | AC-2.2 | Gate-trigger run (M6) per P2 command whose section 3 row resolves a gate as blocked: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait`. For a P2 command whose row resolves the gate by a default (auggie-review, cleanup, improve, reflect, research, tasklist): the same run ends `--outcome succeeded` with the default applied, no `status: blocked`, and step 2 never shows `agentWait` |
```

Self-check (run, not assumed): every AFTER line above was found with `grep -nF` in the candidate and every BEFORE line in the baseline; zero lines missing, so the roles are not swapped.

## Prior blocking findings

| id | prior status | now | evidence (AFTER text only) |
|---|---|---|---|
| M1 | blocking | resolved | AFTER candidate:194 says "steps 1, 2 and 5-7 pass; in steps 3 and 4 (M1, M2) the report is the command's existing report file, since the contract arrives in P1: step 3 compares `--outcome` with that file's own status and checks that the reported path is that file, and step 4 is `test -s` on it". The contradiction with step 3 (candidate:182, "its report path is the WC-4 contract path") is now carved out in P0 only, in the check that gates P0, so AC-0.4 can pass and candidate:154 no longer bars P1 for this reason. The gate is also consistent with candidate:79 ("the worker reports the named file until Phase 1 adds the contract"). |
| M2 | blocking | resolved | Same AFTER text, candidate:194. The two stated texts the finding quotes (step 3 contract clauses, AC-0.4 exempting only step 4) no longer conflict: AC-0.4 names steps 3 and 4. |
| M3 | blocking | resolved | AFTER candidate:195 "every command in sections 3.1-3.2 except load (M3)", candidate:196 "each P1 command except load (M3)", candidate:159 "every command in sections 3.1 and 3.2 except load (M3)" and candidate:76 "Every changed command except load (M3)". The load row (candidate:112, "Report none (see note)") and the Decision at candidate:265 ("a report file would be an unrequested addition") now agree with AC-1.1 and AC-1.2. Residual wording note N5 below. |
| M5 | blocking | resolved | AFTER candidate:62 adds an explicit exception list inside WC-4: adversarial `<output-dir>/adversarial/return-contract.yaml` (matches candidate:83), cleanup-audit `.claude-audit/return-contract.yaml` (matches the fixed output dir at candidate:85), index-repo beside `PROJECT_INDEX.md`, workflow `.dev/tasks/to-do/<id>/return-contract.yaml` read from the command's output with no contract for a pre-package stop. Step 3 ("the WC-4 contract path", candidate:182) and step 4 now point at those paths because WC-4 owns them. AC-1.2 (candidate:196) omits `--output` for a command with none, matching the cleanup-audit, index-repo and workflow rows (candidate:85,86,92). AC-1.4 (candidate:198) drops the workflow pre-creation clause; row 92 drops the "write the contract for pre-creation STOPs" fix. Open points that need a guess are Medium: N2, N3. |
| M6 | blocking | resolved | AFTER candidate:200 limits the blocked assertion to P2 commands whose row resolves a gate as blocked and gives the six default-resolution rows their own pass condition: auggie-review (candidate:100), cleanup (103), improve (110), reflect (88), research (116), tasklist (122) end `--outcome succeeded` with the default applied, no `status: blocked`, no `agentWait`. The nine remaining P2 commands (cli-eval, cli-portify, recommend, review-translation, spec-panel, task, release-split, tdd, troubleshoot) all have a "blocked" resolution in their rows (rows at candidate:89-91, 104-105, 115, 117, 120, 121), so the two halves of AC-2.2 cover all 15 commands listed at candidate:160. |

M4 was rejected by the verifier (round1.md:11, 70) and is a note, not a prior blocking finding; it was not re-checked as a blocker. Nothing in the changed lines reopens it (the candidate still lists pr-submit, implement and post-release under AC-1.1 at candidate:195; the finding stays noted, unactioned).

## Findings on lines changed against the baseline

All four are Medium: each needs a guess that the implementer picks the worse of two readings, or concerns a requirement the document does not state. None names a wrong outcome that holds with no further assumption, so none is blocking.

### N1 (Medium, MAJOR label, Crispin / Wiegers, origin=changed)
- Location: candidate:194 (AC-0.4), step 3 text at candidate:182.
- Quoted AFTER: "step 3 compares `--outcome` with that file's own status".
- Defect: for troubleshoot the existing report is `REPORT.md` (candidate:91), and the inventory lists it only as `report_path` REPORT.md plus `audit.log` (`inventory/commands-b.md:49`); nothing read shows that `REPORT.md` carries a status field. For adversarial the existing contract filename is "not fixed" (candidate:83), so "that file" is not identified in P0. An implementer who follows AC-0.4 as written may be unable to evaluate "that file's own status". This needs the assumption that `REPORT.md` has no status, which no read text establishes (UNVERIFIED), so it is Medium.
- Recommendation (narrow, optional): name the P0 status source per smoke command (for example, "the report's status or verdict line").

### N2 (Medium, Hohpe / Cockburn, origin=changed)
- Location: candidate:62 (WC-4 exception for index-repo) with candidate:86.
- Quoted AFTER: "index-repo beside `PROJECT_INDEX.md`, at the location its P1 fix states". Row 86 says only "State the output location (P1)".
- Defect: the exception points at the P1 fix, and the P1 fix points back at nothing the spec states; the location of `PROJECT_INDEX.md` is "implied, UNVERIFIED" (`inventory/commands-a.md:53`, `:117`). WC-4's heading says "known before dispatch"; no acceptance check (AC-1.1 to AC-1.4) pins the stated location. The implementer chooses a location, which is a requirement the document never states, so Medium.

### N3 (Medium, Nygard / Whittaker, origin=changed)
- Location: candidate:62 (workflow exception).
- Quoted AFTER: "a stop before the package exists writes no contract (WC-5 then applies: no report, `--outcome failed`)", against WC-4's own opening "written on success, failure, blocked and partial outcomes, including stops before any other output exists" and its heading "written on every outcome" (same row).
- Defect: the exception is explicit, so the texts do not contradict. But the coordinator cannot tell a pre-package stop that is blocked on a question from a plain failure, because the blocked question has no file to live in; WC-3/WC-2 (c) route "blocked" through the contract (candidate:60-61). Whether a pre-package workflow stop can be a gate at all is not stated, so this needs a guess: Medium.

### N4 (Medium, Fowler / Hohpe, origin=unchanged, older defect newly noticed)
- Depends on changed line: candidate:200, "`/sc:tdd "auth" --unattended --output <file>` with a bare topic" expecting "contract `status: blocked`", and WC-4 at candidate:62 ("`<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)").
- Defect: tdd, spec-panel and recommend take `--output <file>` (tdd brief `--output <file>` at candidate:90; spec-panel "add `--output`" at candidate:120; recommend "write the handoff envelope to a file" at candidate:115), so for them `<output-dir>` has no stated value and the exception list at candidate:62 does not cover them. Origin: inherited from the baseline (same WC-4 sentence at baseline:62). The gap needs the guess that "directory containing the file" is meant, so Medium.

### N5 (minor note, origin=changed)
- Candidate:76 and candidate:195-196 exclude load from the section, while section 2.1 still says "Each changed command adds a short `## Unattended mode` section" (candidate:51) and the load row is a P1 change (candidate:112). The M3 exception covers it in the places the acceptance checks read; the unedited 2.1 sentence is slightly broader. Note only.

## Dependency check (changed behavior and what it touches)

- Section 7.2 step 3-4 (candidate:182-183) are consumed by AC-0.4, AC-1.2 and AC-2.2; each of the three now carries its own carve-out (candidate:194, 196, 200). No other per-phase check requires the WC-4 path for load, adversarial, cleanup-audit, index-repo or workflow.
- AC-1.4 (candidate:198) greps the adversarial SKILL.md for one fixed path; the path it expects is the one WC-4 now lists (candidate:62), and row 83 states the same path.
- SA-4 (candidate:149) now names "adversarial contract gap" and no longer names the workflow gap; row 92 reads "None", so SA-4 and row 92 agree. AC-C5 (candidate:176) still checks additivity for edits without a named defect fix.
- P1 scope list (candidate:159) no longer lists workflow under fixes; workflow is still a 3.1 command, so AC-1.1 still requires its `## Unattended mode` section; no conflict found.
- Guard Condition Boundary Table: guards on changed lines only. The only guard-like conditions on changed lines are the "except load" exclusion and the "command with none" `--output` omission; both are fully specified in the AFTER text, no GAP and no blank Specified Behavior.

## Guard Condition Boundary Table (changed lines only)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| except-load exclusion | candidate:195-196 | Legitimate Edge Case | `load` | excluded | AC-1.1 and AC-1.2 skip `load`; usage-line fix only (candidate:112,159) | OK |
| except-load exclusion | candidate:195 | Zero/Empty | no `## Unattended mode` section in a section-4 command | asserted absent | test asserts none (candidate:195) | OK |
| `--output` omission | candidate:196 | Zero/Empty | command with no output flag (cleanup-audit, index-repo, workflow) | omit flag | contract path from WC-4 exception list (candidate:62) | OK (N2 Medium for index-repo location) |
| pre-package workflow stop | candidate:62 | Zero/Empty | no `<id>` directory | no contract | `--outcome failed`, no report (WC-5) | OK (N3 Medium) |
| default-resolution AC | candidate:200 | Sentinel Value Match | `status: blocked` absent | succeeded | `--outcome succeeded`, default applied | OK |

Other input classes (One/Minimal, Typical, Maximum/Overflow) cannot occur for these guards, which are set-membership choices over a fixed command list.

## Coverage

scoped PASS: changed lines + prior blockers

Covered: the 20 changed diff lines, the five confirmed prior blockers (M1, M2, M3, M5, M6) against the AFTER text, the dependent checks and rows named above, and the four WC-4 exception targets against section 3 rows. Not covered: whole-document assurance (needs a separate labelled first review), the rf-qa Fix Cycle file (unavailable in the sandbox), and any citation to a file outside the workspace (UNVERIFIED).

## Follow-up candidates

Medium: N1, N2, N3, N4. Minor: N5. Carried from review 1: M4 (noted, unactioned, round1.md:11) and the two source reports' follow-up candidates by reference (round1.md:78-80). The session that runs this loop asks the user once whether to open an issue for them; none is created here.

## Reviser brief

Blocking finding ids: none. No revision is called for. Rules if a reviser is ever briefed (restating Review Loop bullet 6): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report byte size before and after, with bytes added and deleted per finding id.

verdict: PASS
