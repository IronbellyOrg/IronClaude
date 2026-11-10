review: 2 of 3
> verification (coordinator, VERIFY step VF2; verifier reply .dev/orca-command-refactor/review/verify-2.md): confirmed blocking ids: none. Rejected, kept as noted, unactioned and not prior blocking findings for the next re-review: M1 (verifier: The deferral is stated in the candidate itself, with an owner (P2) and a trigger (before the live check), and WC-4's default `<output-dir>/return-contract.yaml` applies to a row that names no path, so no wrong outcome follows from the text. The "revise1.md:71" cite is outside the candidate and cannot be checked in this sandbox.). The Reviser brief below is narrowed to the confirmed ids.

# Re-review: orca-worker-contract spec (spec-panel critique, focus requirements,architecture)

- candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 84aa3fdce83498845e1a3cf58e05e4b1f83a15e38b34520e6f0393658bd74d26
- baseline (--baseline): .dev/orca-command-refactor/specs/history/spec-v1.md sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
- prior (--re-review): .dev/orca-command-refactor/review/round1.md, header `review: 1 of 3` (round1.md:1), sha256 ea013be192f8bb8cca101971d804de1e462c69e12ecf522539dc5c9796978796
- lint (brief): .dev/orca-command-refactor/review/lint-2.md, sha256 86cecda645c022d763b32c040a66be31ec2ccb7636d7ecaec7b4bbe6a6d13b31. Its header records the candidate sha 84aa3fdc... (lint-2.md:1) and reads `Checks: REF. Findings: 0.` (lint-2.md:3,5). No lint id to address.
- reviewer model: claude-haiku-5-5
- N = prior N + 1 = 2 (round1.md:1 reads `review: 1 of 3`).
- rf-qa.md: neither `.claude/agents/rf-qa.md` nor `~/.claude/agents/rf-qa.md` lies inside the sandbox, so it was not read. The re-check follows the Review Loop rules in command.md:256-264 standing alone.
- Read before review: .dev/orca-command-refactor/README.md (shared context), review/revise1.md (reviser report; it defers the cli-portify location to P2 at revise1.md:71), review/verify-1.md (VERIFY reply: confirms M1-M8, M10, M11 and rejects M9 at verify-1.md:18).
- Byte sizes: revise1.md:12 states 57763 before and 60183 after; `wc -c` gives the same figures for spec-v1.md and the candidate.

## Step 1: evidence block

Roles, fixed: CANDIDATE = the @file (orca-worker-contract-spec.md); BASELINE = spec-v1.md; PRIOR = round1.md.
`diff -w BASELINE CANDIDATE` gives 14 changed lines on each side. Self-check, run after the diff:
- every AFTER line (`>`) is found verbatim in CANDIDATE: 14 of 14;
- every BEFORE line (`<`) is found verbatim in BASELINE: 14 of 14;
- BEFORE lines found in CANDIDATE: 0 of 14. Roles are confirmed.

Changed candidate lines: 62, 63, 69, 73, 76, 92, 112, 184, 185, 194, 195, 196, 200, 265 (diff hunks `62,63c62,63`, `69c69`, `73c73`, `76c76`, `92c92`, `112c112`, `184,185c184,185`, `194,196c194,196`, `200c200`, `265c265`).

BEFORE (baseline), lines starting `<`:

```text
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
< | WC-5 | **Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome failed` when the report says `failed` or `blocked`, or no report exists; `--outcome succeeded` otherwise, including `partial` and including an audit whose verdict is FAIL (the audit itself succeeded). The first sentence of the body states the report's status and verdict. | Worker session | `CAPS:73` (`[G]` lines 88-90, "Never encode failure only in prose"); `CAPS:76-77` |
< | WC-11 | **Parallel-safe writes.** Two workers in one worktree must never write the same file. Default output paths carry a timestamp or the slug the coordinator passes; single-owner shared files (for example memory keys overwritten whole) are not written in unattended mode. | Command | `cmd/save.md:42-45`; `CAPS:115` (`[G:placement]` lines 8-11: workers share the current worktree by default) |
< The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
< The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
< | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
< | load | no gate | none (see note) | n/a | none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |
< 5. `ORCA orchestration worker-read --dispatch <dispatch_id> --source transcript --json` and search the transcript for `AskUserQuestion`. **Pass:** no `AskUserQuestion` call.
< 6. `git status --short`. **Pass:** only files under the brief's output directory (and the command's documented artifacts) appear.
< | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
< | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
< | P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |
< | `/sc:load` handling | Add a report file; use it only inside another worker's brief | Use it inside a brief: its only output is context for the current session (`INV-B:65`); a report file would be an unrequested addition. Only its usage-line defect is fixed. |
```

AFTER (candidate), lines starting `>`:

```text
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). The path is that default; where a command's section 3 row names another path, the command writes there (M1): adversarial `<output>/adversarial/return-contract.yaml` (row 3.1), cleanup-audit (its fixed `.claude-audit/` directory), init-lite and tdd (the file `--output` names), and cli-portify (its row leaves the location unnamed, so P2 names it before its live check). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. `load` is exempt and writes no contract (M10; section 3.2 row and the Decisions table). Workflow (M11): P1 adds `--output <dir>`; a pre-creation STOP writes `<output-dir>/return-contract.yaml`, and after package creation the same contract is also written to `.dev/tasks/to-do/<id>/return-contract.yaml`, which the `<output-dir>` file lists under `artifacts`; the coordinator always reads the `<output-dir>` file. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
> | WC-5 | **Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome succeeded` only when the contract parses and its `status` is `succeeded` or `partial` (M3), including an audit whose verdict is FAIL (the audit itself succeeded). Every other case is `--outcome failed` (M3): `failed`, `blocked`, no report, an empty or unparseable contract, and a status outside the four values. The first sentence of the body states the report's status and verdict. | Worker session | `CAPS:73` (`[G]` lines 88-90, "Never encode failure only in prose"); `CAPS:76-77` |
> | WC-11 | **Parallel-safe writes.** Two workers in one worktree must never write the same file. Under `--unattended`, default output paths carry a timestamp or the slug the coordinator passes; standalone defaults are unchanged (SA-1, M4); single-owner shared files (for example memory keys overwritten whole) are not written in unattended mode. | Command | `cmd/save.md:42-45`; `CAPS:115` (`[G:placement]` lines 8-11: workers share the current worktree by default) |
> The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` (from P1 on; P0 briefs omit it, M2) and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
> The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file, at the path WC-4 or the row names (M1). Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
> | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") and add `--output <dir>` (M11) (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
> | load | no gate | none, exempt from WC-4 (M10) | n/a | none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |
> 5. `ORCA orchestration worker-read --dispatch <dispatch_id> --source transcript --json` and search the transcript for `AskUserQuestion` and for tool-use events named Agent or Task whose prompt is the `/sc:` command line (M7; the field that holds the tool name is UNVERIFIED until a P0 run records one). **Pass:** no `AskUserQuestion` call and no such Agent or Task event (WC-7).
> 6. `git status --short` before dispatch and again after the worker settles (M6). **Pass:** every entry new since the before-dispatch snapshot is under the brief's output directory or is one of the command's documented artifacts; entries already listed before dispatch (the phase's own uncommitted edits) are not counted.
> | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 is `test -s` on the command's existing report file (for troubleshoot, `REPORT.md`, `INV-B:49`), with no YAML field check, since no contract exists until P1 and the workflow contract has no `command` key (`INV-B:272`) (M5). P0 briefs omit `--unattended` (M2), so step 5 is judged on its Agent-tool check (M7), and its `AskUserQuestion` result is recorded but is not a pass condition here; WC-2 is first tested in AC-1.2. Record the results in the phase report; a failure here reopens section 1 |
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `load` (M10) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
> | P1 | AC-1.2 | 7.2 live check on each P1 command except `load` (M10) with `--unattended --output <dir>` | all steps pass |
> | P2 | AC-2.2 | Gate-trigger run per P2 command whose section 3.2 row names a blocked path (M8): a 7.2 live check with that row's trigger input. The nine are cli-eval (`run` with no `--suite`), tdd (`/sc:tdd "auth" --unattended --output <file>`, a bare topic), troubleshoot (`--depth deep` with a short input), task (confidence below 0.70), recommend (a goal that needs the clarifying question), review-translation (no pre-confirmed context input), release-split (`--r1-scope custom`), spec-panel (a TDD input with no `target_release`) and cli-portify (a run with no approval input). auggie-review, cleanup, improve, research, reflect and tasklist have a documented default in their section 3.2 rows and run AC-2.3 instead, recording that default in the contract | For the nine: `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |
> | `/sc:load` handling | Add a report file; use it only inside another worker's brief | Use it inside a brief: its only output is context for the current session (`INV-B:65`); a report file would be an unrequested addition. Only its usage-line defect is fixed; WC-4 exempts it from the contract (M10). |
```

## Prior blocking findings (round1.md)

| Id | Status | Where (candidate) | Basis |
|---|---|---|---|
| M1 | open (deferred part) | :62, :83, :92 now name the paths; cli-portify is still unnamed at :62 and :105 | revise1.md:71 leaves the cli-portify location to P2. The reviser's deferral counts as open. |
| M2 | resolved | :73 (P0 briefs omit `--unattended`), :194 (P0 clause) | |
| M3 | resolved | :63 (`succeeded` only for a parsed contract with status `succeeded` or `partial`) | The P0 consequence of WC-5 is R2.1, a separate finding. |
| M4 | resolved | :69 scoped to `--unattended`; SA-1 (:146) now consistent | |
| M5 | resolved | :194 step 4 is `test -s` with no YAML check; :183 is overridden for P0 | INV-B:49 (troubleshoot writes REPORT.md), INV-B:272 (workflow contract has no `command` key) |
| M6 | resolved | :185 before/after snapshot | Residual gap R2.3 (Medium). |
| M7 | resolved | :184 adds the Agent/Task check, cited at :194 | The tool-name field is UNVERIFIED (R2.4, Medium). |
| M8 | resolved | :200 gives nine blocked-path commands and AC-2.3 for six default commands | Together they cover the 15 P2 commands listed at :160. |
| M10 | resolved | :62 (`load` exempt), :112, :195, :196, :265 | |
| M11 | resolved | :62 and :92 (workflow `--output` in P1; pre-creation STOP path) | |

No prior id is regressed. M9 is carried as a note (see below).

## New findings on changed lines

### R2.1 (blocking; new; origin=unchanged text that the changed line at :194 depends on)

- Location: :194 (AC-0.4, "steps 1-3 and 5-7 pass", "since no contract exists until P1"); :182 (step 3); :63 (WC-5).
- Text: step 3 passes only if "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path" (:182). WC-5 says `--outcome succeeded` only "when the contract parses", and every other case, including "no report", is `--outcome failed` (:63).
- Grading sentence: An implementer who follows AC-0.4 runs `/sc:troubleshoot` as a P0 worker. The command writes REPORT.md and no contract (INV-B:49), so under WC-5 (:63) the worker sends `--outcome failed` and its report path is not a WC-4 contract path. Step 3 requires both to match a contract that does not exist, so a correct P0 run fails step 3, and AC-0.4 cannot pass as written.
- Wrong outcome: Phase 0 cannot close, and a correct run is recorded as failed.
- Recommendation: in P0, state step 3 against the command's existing report file and the outcome WC-5 produces without a contract, or drop the contract clause from step 3 for P0. Priority: high.

### R2.2 (blocking; new; changed line :62)

- Location: :62 (exception: "init-lite and tdd (the file `--output` names)"; default "`<output-dir>/return-contract.yaml`"); :90 (tdd row: "the TDD at `--output`"); :87 (init-lite row: `--output <file>`, report at `--output`); :195 (AC-1.1 requires a section "naming `return-contract.yaml`"); :183 (step 4 parses the contract as YAML).
- Grading sentence: An implementer who follows the :62 exception for `/sc:tdd "<prompt>" --unattended --output design.md` writes the contract into design.md, the TDD deliverable named at :90, so the TDD is overwritten or carries YAML fields. An implementer who follows the default writes `return-contract.yaml` beside design.md, which the exception forbids. The two stated texts contradict, and one of the two outcomes damages the deliverable.
- Recommendation: give file-valued commands one rule. Either the contract is `return-contract.yaml` in the directory of `--output` for tdd and init-lite, or a separate contract flag is added. Then correct :62, :87, :90 and AC-1.1. Priority: high.

## Guard Condition Boundary Table (guards on changed lines; FR-8 to FR-10)

Guards on changed lines: WC-5 outcome (:63), WC-4 path choice (:62), the step 6 pass rule (:185), and the AC-2.2 gate against default (:200). Pipeline Dimensional Analysis is not triggered, because no changed line adds a multi-stage count pipeline.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 WC-5 outcome | :63 | Zero/Empty | 0-byte contract | not succeeded | failed | OK |
| G1 WC-5 outcome | :63 | One/Minimal | status `partial` | succeeded | succeeded | OK |
| G1 WC-5 outcome | :63 | Typical | status `succeeded`, contract parses | succeeded | succeeded | OK |
| G1 WC-5 outcome | :63 | Sentinel Value Match | status `done` (outside the four values) | not succeeded | failed | OK |
| G1 WC-5 outcome | :63 | Legitimate Edge Case | status `succeeded`, audit verdict FAIL | succeeded | succeeded | OK |
| G1 WC-5 outcome | :63, :194 | P0 with no contract written | REPORT.md only | not succeeded | failed, while step 3 expects a match | GAP (R2.1) |
| G2 WC-4 path | :62 | Zero/Empty | `--unattended` without `--output` | no rule stated | none | GAP (R2.5, Medium) |
| G2 WC-4 path | :62, :83 | One/Minimal | adversarial with `--output d` | `d/adversarial/return-contract.yaml` | as written | OK |
| G2 WC-4 path | :62, :92 | Typical | workflow pre-creation STOP with `--output d` | `d/return-contract.yaml` | as written | OK |
| G2 WC-4 path | :62, :90 | Sentinel Value Match | tdd `--output design.md` (file-valued) | contract written into design.md | contradicts the default name and AC-1.1 | GAP (R2.2) |
| G2 WC-4 path | :62, :85 | Legitimate Edge Case | cleanup-audit fixed directory `.claude-audit/` | `.claude-audit/` | as written | OK |
| G2 WC-4 path | :62, :105 | cli-portify, location unnamed | deferred to P2 | no path before P2 | none | GAP (M1, open) |
| G3 step 6 | :185 | Zero/Empty | no entries before or after | pass | pass | OK |
| G3 step 6 | :185 | One/Minimal | one new entry outside the output directory | fail | fail | OK |
| G3 step 6 | :185 | Typical | new entry under the output directory | pass | pass | OK |
| G3 step 6 | :185 | Sentinel Value Match | file already dirty before dispatch, worker writes it outside the output directory | not counted, pass | pass | GAP (R2.3, Medium) |
| G3 step 6 | :185 | Legitimate Edge Case | the phase's own uncommitted edits | not counted | not counted | OK |
| G4 AC-2.2 gate | :200 | Typical | tdd with a bare topic | blocked | `status: blocked`, `worker_done --outcome failed` | OK |
| G4 AC-2.2 gate | :200 | One/Minimal | release-split `--r1-scope custom` | blocked | as written | OK |
| G4 AC-2.2 gate | :200 | Zero/Empty | cli-portify with no approval input | blocked | the row at :105 names the gates; the trigger is inferred | OK |
| G4 AC-2.2 gate | :200 | Legitimate Edge Case | cleanup with no flags (documented default) | not blocked | AC-2.3 path; default recorded | OK |

Left out, with reasons: Maximum/Overflow for G1, G2 and G3, because none of these guards has a numeric threshold (WC-5 tests a four-value set; WC-4 and step 6 have no count). Maximum/Overflow for G4 is also left out; the gate is a yes/no input.

## Follow-up candidates (Medium or minor; not blocking; not a revision trigger)

- R2.3 (Medium, :185): step 6 does not count entries already listed before dispatch, so a worker's write to an already-dirty out-of-scope file passes. The check's purpose is defeated, but no data is lost, because the phase's pre-dispatch edits are the coordinator's own.
- R2.4 (Medium, :184): step 5 names no transcript field for the tool name. The spec labels this UNVERIFIED, so an implementer must guess the field until a P0 run records it (revise1.md:62).
- R2.5 (Medium, :62): no stated behavior when `--unattended` is passed without `--output`. The default timestamp rule at :69 gives a result, so no wrong outcome is named.
- R2.6 (Medium, :83 against :62): the adversarial row fixes the contract filename with no unattended qualifier, while :62 scopes the default path to unattended mode. This is the same SA-1 question as noted M9 (round1.md:109). It is not blocking, because the rejected M9 is a note and the fix is a defect fix under SA-4 (:149).
- Minor (:92): the workflow row's "Brief must pass" column still lists only `--handoff none`, while the same row adds `--output <dir>` in P1.

## Noted, unactioned (verifier rejected; not a prior blocking finding)

- M9 (round1.md:102-109; verify-1.md:18): the roadmap row at :118 still removes the "Resume? [Y/n]" prompt with no `--unattended` qualifier. Carried as a note and not re-graded here.

## Coverage

- Covered: the 14 changed candidate lines; all 10 prior blocking ids; lint-2; the 14 changed lines checked by the self-check above; in-workspace citations on changed lines checked against the inventories.
- Inventory citations confirmed: INV-B:49 (troubleshoot writes REPORT.md as `report_path`); INV-B:272 (workflow contract fields, no `command` key, not written for pre-creation STOPs); INV-A:35 (adversarial writes `<output>/adversarial/return-contract.yaml` in real runs); INV-B:65 (load writes no file); CAPS:72-74 and CAPS:76-79 (worker_done flags, outcome, and the report path is a pointer whose handling is UNVERIFIED).
- Not covered: the sk/ and cmd/ paths cited on changed rows (outside the workspace, UNVERIFIED here; not the basis of any blocking finding); unchanged text beyond what the changed lines depend on.
- Scoped PASS line: not issued, because blocking findings are open.
- Coordinator: the blocking findings M1, R2.1 and R2.2 need the VERIFY prompt in a fresh context before any revision (document_review_loop_prompts.md, VERIFY). This is review 2 of 3, so one fix cycle and a third review remain.

## Reviser brief

Blocking finding ids: M1 (open: the cli-portify location at :62 and :105), R2.1, R2.2.
Restated Reviser contract: revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; cite the finding id on each added paragraph or table; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
