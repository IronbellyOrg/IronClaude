review: 2 of 3

# Spec-panel critique, round 2 (re-review): orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md`
- CANDIDATE: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `746b5ffc5ac4b78a7e2053e0e341cc67756a46ac8a09ff6161b886dedded7fa2` (285 lines, 58530 bytes)
- BASELINE: `.dev/orca-command-refactor/specs/history/spec-v1.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (285 lines, 57763 bytes; equals the hash round 1 recorded for its candidate, `round1.md:6`)
- PRIOR: `.dev/orca-command-refactor/review/round1.md`, sha256 `bc3ad9f856237addbaf95880e81b1a84116b1e8beb97f931703815da53522810`, header `review: 1 of 3` (`round1.md:1`), final line `verdict: FAIL` (`round1.md:122`); N = 1 + 1 = 2, so the cap check (`review: 3` with FAIL) does not apply
- lint file: `.dev/orca-command-refactor/review/lint-2.md`, sha256 `a008528014b5fe6be221b30a5313648124ea735db397b1b51664ef29c4d94130`; its header hash `746b5ffc...7fa2` equals the candidate hash (`lint-2.md:1`), so it was produced on this exact file
- reviewer model actually used: claude-sonnet-5-5
- prompt followed: RE-REVIEW prompt and re-review core of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full); roles fixed by that file's table, not by reading order
- panel (fixed order, critique mode, focus requirements + architecture, Whittaker always active): Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe
- coverage: scoped PASS: changed lines + prior blockers

## Step 1: evidence block
Command run: `diff -w specs/history/spec-v1.md specs/orca-worker-contract-spec.md`. Six changed lines (62, 73, 92, 159, 195, 198; no line added or removed). Whitespace-only changes: none. Changed lines copied verbatim; `<` lines under BEFORE, `>` lines under AFTER.

### Line 62

BEFORE (baseline), `specs/history/spec-v1.md:62`:
```text
| WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
```
AFTER (candidate), `specs/orca-worker-contract-spec.md:62`:
```text
| WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. Exception (REQ-1): `workflow` mints its own package directory `<id>` and takes no output flag (`INV-B:272-273`), so its contract is `.dev/tasks/to-do/<id>/return-contract.yaml`, a path the worker reads from the command's final reply, not one known before dispatch; a stop before the package exists writes no file, which WC-5 maps to `--outcome failed` ("no report exists") with the stop reason in the body, and 7.2 steps 3-4 do not apply to that stop. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
```

### Line 73

BEFORE (baseline), `specs/history/spec-v1.md:73`:
```text
The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
```
AFTER (candidate), `specs/orca-worker-contract-spec.md:73`:
```text
The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4; `workflow` excepted, REQ-1); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
```

### Line 92

BEFORE (baseline), `specs/history/spec-v1.md:92`:
```text
| workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
```
AFTER (candidate), `specs/orca-worker-contract-spec.md:92`:
```text
| workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | State the package path in the final reply; pre-creation STOPs write no contract (WC-4 exception, REQ-1) (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
```

### Line 159

BEFORE (baseline), `specs/history/spec-v1.md:159`:
```text
| **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
```
AFTER (candidate), `specs/orca-worker-contract-spec.md:159`:
```text
| **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag and `## Unattended mode` section on each command whose own row is P1, plus the ready commands with no gate change (brainstorm, init-lite); every other command gets both in the phase of its row, together with its gate resolutions (REQ-2); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
```

### Line 195

BEFORE (baseline), `specs/history/spec-v1.md:195`:
```text
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
```
AFTER (candidate), `specs/orca-worker-contract-spec.md:195`:
```text
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 whose row phase is P1 or earlier, plus brainstorm and init-lite, has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md` (`load` exempt: it has no report, REQ-2), and that no section-4 command has one | passes |
```

### Line 198

BEFORE (baseline), `specs/history/spec-v1.md:198`:
```text
| P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |
```
AFTER (candidate), `specs/orca-worker-contract-spec.md:198`:
```text
| P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states the package path in its final reply (REQ-1) |
```

Self-check (run with `grep -nF`): each of the 6 AFTER lines (without `>`) was found in the CANDIDATE and each of the 6 BEFORE lines (without `<`) in the BASELINE; no quote missing, so roles are not swapped.

Coverage: the 6 changed lines above, the text they depend on (`spec:44-47,56-70,72-73,75-93,127-139,153-165,166-210,255-284`), the prior report (`round1.md:1-123`), the lint file (`lint-2.md:1-17`), the revise record (`revise1.md:1-25`, used as a claim to check, not as evidence), and the inventory lines the changes rely on (`INV-B:52,267-275`). UNVERIFIED (outside the workspace): every `CLAUDE.md:N`, `cmd/`, `sk/`, `src/`, `.dev/codegraph-migration/`, `.dev/evals/` and `/opt/Orca/` citation, as in round 1. The reviser's byte table (`revise1.md:8-12`) was checked in total only: 58530 - 57763 = +767 matches `wc -c`; the per-id split was not recomputed.

## Prior blocking findings

| Id | Status | Basis |
|---|---|---|
| REQ-1 | resolved | See below |
| REQ-2 | resolved | See below |

### REQ-1: resolved
Prior defect (`round1.md:28-32`): WC-4 required one contract at a coordinator-passed directory known before dispatch on every outcome, while the workflow row (`spec:92` before) put it at a command-minted `<id>` path and asked for a write on pre-creation stops.
AFTER text only: WC-4 now carries an explicit exception (`spec:62`): the workflow contract is `.dev/tasks/to-do/<id>/return-contract.yaml`, read by the worker from the command's final reply; a stop before the package exists writes no file, WC-5 maps that to `--outcome failed` (WC-5 at `spec:63` does say "or no report exists"), and 7.2 steps 3-4 do not apply to that stop. Section 2.3 (`spec:73`) excepts workflow from "known before dispatch". The workflow row (`spec:92`) and AC-1.4 (`spec:198`) now say the same thing (package path in the final reply, no contract for pre-creation stops). The inventory supports the premise: the contract is "Not written for pre-creation STOPs" and the skill never reuses a package (`INV-B:272-273`). The three texts no longer contradict each other and an implementer who follows them builds a workflow that does not need a path the brief cannot name. Grading sentence for any remaining wrong outcome: none holds without a further guess (see M-13, M-14, which are Medium).

### REQ-2: resolved
Prior defect (`round1.md:38-42`): P1 and AC-1.1 required `--unattended` and a contract-naming section on every command in 3.1-3.2, while gate resolutions and WC-9 off-switches for auggie-review, task, implement, post-release, pr-submit sit in P2/P4, and `/sc:load` has no report.
AFTER text only: P1 (`spec:159`) now gives the flag and section only to commands whose own row is P1, plus brainstorm and init-lite, and every other command gets both in the phase of its row with its gate resolutions. AC-1.1 (`spec:195`) asserts the section only for commands whose row phase is P1 or earlier plus brainstorm and init-lite, with `load` exempt. Checked against the rows: the P1 rows are analyze, build, business-panel, design, document, explain, index, test, load (`spec:99,101,102,106-108,111,112,123`), and 3.1 P1 fixes are adversarial, cleanup-audit, index-repo, workflow (`spec:83,85,86,92`); brainstorm and init-lite have "None" (`spec:84,87`); auggie-review, task (P2, `spec:100,121`) and implement, post-release, pr-submit (P4, `spec:109,113,114`) get the flag only with their gate resolutions. The P1 gate rows (business-panel `--mode socratic`, explain `--format interactive`, test `--watch`) carry their resolution in the same P1 row, so they are not half-wired. Phase counts still reconcile: P1 13 named + 2 = 15, P2 15, P3 4, P4 3 = 37 worker-capable commands, matching 43 - 6 (`spec:76`). The text no longer produces a P1 flag without its WC-9 off-switch, and the `load` section is exempt.

## Findings on changed lines
No blocking finding. Each item cites the changed line it depends on.

=== REQUIREMENTS ANALYSIS ===

- M-13 (Medium, origin=changed, Wiegers, Adzic) AC-1.2 (`spec:196`, unchanged) runs the 7.2 check "on each P1 command with `--unattended --output <dir>`", and `workflow` is a P1 command (`spec:159`, `spec:92`) that the changed WC-4 text (`spec:62`) says "takes no output flag" and whose contract path is not known before dispatch. Read literally, `--output <dir>` is passed to a command that has none. Grading: the implementer must guess to drop `--output` for workflow (the exception at `spec:62` and `spec:73` points that way), so Medium. Suggested follow-up: one clause in AC-1.2 naming workflow.
- M-14 (Medium, origin=changed, Wiegers) AC-1.4 (`spec:198`) greps `return-contract.yaml` in the adversarial skill and "the workflow return-contract ref" but its pass condition is now "workflow states the package path in its final reply". The final-reply wording lives in the workflow skill body or command, not necessarily in the return-contract ref (`INV-B:272` names the ref only for the contract fields and the pre-creation exception at `refs/return-contract.md:39`), so the grep target may not contain the text it checks. Whether the final reply already states the path is UNVERIFIED (also flagged at `revise1.md:17`).
- n-4 (minor) Lint ids LINT-REF-1 (`lint-2.md:5-10`, line 62) and LINT-REF-2 (`lint-2.md:12-17`, line 159): confirmed as real but harmless. The candidate now cites `REQ-1`/`REQ-2` (`spec:62,73,92,159,195,198`) and neither id is defined inside the spec; they are defined only in `round1.md:26,36`. An implementer builds the same thing either way, so this is a note, not a defect: quote `(REQ-1)` at `spec:92` and `(REQ-2)` at `spec:159`. Suggested follow-up: replace the ids with a plain reason or a pointer to `review/round1.md`.
- n-5 (minor) The new WC-4 sentence (`spec:62`) says workflow "takes no output flag" and cites `INV-B:272-273`; those lines state the contract path and that the package is never reused, not the absence of an output flag. The absence is implied by the brief column (`spec:92`, flags `--handoff none` only). UNVERIFIED against `cmd/workflow.md`.
- Carried, origin=unchanged, minor notes only: Medium and minor items M-1 to M-12 and n-1 to n-3 of `round1.md:94-110` were not touched by the diff and none quotes a changed line, so they stay minor notes and are not re-graded. Exception: M-3 and M-5 (contract path for fresh-dir retries and file-valued outputs) now sit beside the new WC-4 exception, which handles only workflow; they remain Medium follow-ups.

=== ARCHITECTURE ANALYSIS ===
No blocking architecture finding. The change adds no mechanism: it narrows WC-4 and P1/AC-1.1. The dependency check holds: nesting depth, coordinator-only set (`spec:127-139`) and `worker_done` ownership (WC-5, WC-7) are untouched, and 7.2 step 3's "report path is the WC-4 contract path" (`spec:182`) stays satisfiable for workflow because the exception defines that path.

=== ADVERSARIAL ANALYSIS (Whittaker, changed lines only) ===
- Sequence attack on the P1/P2 split: between P1 and P2 the ready commands reflect, release-split, tdd and troubleshoot have no `--unattended` (their rows are P2, `spec:88-91`), yet section 2.3 (`spec:73`) and 7.2 step 1 (`spec:180`) put `--unattended` in every command line. This is round 1's M-6, unchanged, but the narrowed P1 (`spec:159`) now makes it stricter: P0 and P1 live checks on those commands must omit the flag. Medium, origin=unchanged; no changed line makes it worse than M-6.
- Zero/empty attack on workflow pre-creation stops (`spec:62`): no file, `--outcome failed`, reason only in the body. A stop that is really a missing-input question would lose `blocked_question`. Workflow has no gate in 3.1 (`spec:92`), so no required behaviour is lost. Note only.

## Guard Condition Boundary Table (changed lines only)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| workflow contract path known before dispatch | `spec:62,73` | Zero/Empty | stop before the package exists | no file | `--outcome failed`, reason in body; 7.2 steps 3-4 do not apply (`spec:62`) | OK |
| workflow contract path known before dispatch | `spec:62` | Typical | post-creation outcome | file at `.dev/tasks/to-do/<id>/` | worker reads path from final reply (`spec:62`); final reply wording UNVERIFIED | OK (see M-14) |
| workflow contract path known before dispatch | `spec:62,196` | Legitimate Edge Case | AC-1.2 passes `--output <dir>` | workflow has no such flag | not stated | GAP (M-13, Medium) |
| P1 flag-and-section scope | `spec:159,195` | Zero/Empty | `load` (no report) | exempt | AC-1.1 exempts it (`spec:195`) | OK |
| P1 flag-and-section scope | `spec:159,195` | Typical | analyze (row P1) | flag and section in P1 | stated | OK |
| P1 flag-and-section scope | `spec:159,195` | Legitimate Edge Case | brainstorm, init-lite (row "None") | included by name | stated | OK |
| P1 flag-and-section scope | `spec:159,195` | Maximum/Overflow | P2/P4 commands with outward defaults (auggie-review, task, post-release, pr-submit) | no flag in P1 | flag arrives with gate resolution in own phase | OK |

Classes left out: One/Minimal (no distinct value for either guard), Sentinel Value Match (neither guard compares a sentinel). Guards on unchanged lines are not re-tabulated (re-review scope).

## Quantity Flow Diagram (changed phase partition)
```text
[Worker-capable commands: 37] --> [P1: 13 named + brainstorm, init-lite = 15] --> flag+section in P1: 14 (load exempt)
                              --> [P2: 15] --> flag+section in P2
                              --> [P3: 4]  --> flag+section in P3
                              --> [P4: 3]  --> flag+section in P4 (after D2-D4)
15 + 15 + 4 + 3 = 37, no mismatch.
```

## Follow-up candidates (Medium and minor; none triggers a revision)
Medium: M-13, M-14, plus the unchanged M-1 to M-12 from `round1.md:94-105`.
Minor: n-4, n-5, plus the unchanged n-1 to n-3 (`round1.md:108-110`).

Issue question: per the Review Loop (bullet 3) the session that ran the review asks the user once per loop whether to open an issue for the follow-up candidates and creates none without the answer. This run is unattended inside a sandbox: no question was asked and no issue was created. The coordinator should ask.

Brief clauses overridden: none. The brief named the baseline, prior and lint values and the RE-REVIEW prompt; all were followed as written.

## Reviser brief
No blocking finding is open (REQ-1 and REQ-2 resolved), so no revision is requested. Review loop bullet 6 applies only if a blocking finding appears: revise only text a blocking finding names; add nothing it does not call for; cite the finding id on each addition; prefer deleting or narrowing; report bytes before and after and added and deleted per id.

verdict: PASS
