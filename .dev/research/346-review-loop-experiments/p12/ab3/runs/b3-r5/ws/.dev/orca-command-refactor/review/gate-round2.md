review: 2 of 3

# Gate loop re-review: Orca worker contract spec (round 2)

| Field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/gate.md --baseline .dev/orca-command-refactor/specs/history/spec-g.md` |
| Review kind | RE-REVIEW of the gate loop (the gate report numbers its own loop; its header is `review: 1 of 3`, `review/gate.md:1`, so N = 1 + 1 = 2) |
| Prompt followed | RE-REVIEW prompt and its core (roles, Step 1, review number, self-check), `~/.claude/rules/prompts/document_review_loop_prompts.md:38-52`, read in full before reviewing |
| Roles | CANDIDATE = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; BASELINE = `.dev/orca-command-refactor/specs/history/spec-g.md`; PRIOR = `.dev/orca-command-refactor/review/gate.md` |
| Candidate sha256 | `7dee641ad4c0ea491b648c4d2ff91374c68f0b6c2b89647e79c56e099f02c9e8` |
| Baseline sha256 | `a836576df87b59b039072268c20705696ba11a57c7fd7ec19d1e677d12268487` (equals the "Candidate sha256" printed in `review/gate.md:11`, so the baseline is the text the gate reviewed) |
| Prior report | `review/gate.md`, `review: 1 of 3`, final line `verdict: FAIL`, one blocking finding (B-01) |
| Reviser report read | `review/revise-gate.md` (as input only; its claims were checked against the diff, not trusted) |
| Reviewer model | `claude-sonnet-5-5` (Sonnet 5.5) |
| Date | 2026-11-10 |
| Citation notation | `SPEC:N` = line N of the candidate; `GATE:N` = line N of `review/gate.md`; `INV-A:N`, `INV-B:N` = lines of `inventory/commands-a.md`, `commands-b.md`; `PROMPTS:N` = the prompts file. |
| Evidence limit | Only `.dev/orca-command-refactor/` files and the prompts file were readable. Every `cmd/`, `sk/`, `CLAUDE.md`, `EVIDENCE.md` and Orca-source citation is UNVERIFIED here (checkable only through the inventory line that quotes it). `command.md` was read as the command definition. |

## Step 1: evidence block

Run: `diff -w specs/history/spec-g.md specs/orca-worker-contract-spec.md` (BASELINE then CANDIDATE). 11 changed lines (62, 73, 76, 83, 85, 87, 90, 92, 182, 198, 200); no other line differs apart from whitespace. Lines starting `<` are copied under BEFORE, lines starting `>` under AFTER, verbatim.

### BEFORE (baseline)

```text
- | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
```
```text
- The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
```
```text
- The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
```
```text
- | adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
```
```text
- | cleanup-audit | `--pass <N>` (single pass) | `.claude-audit/pass<N>-summary.md` | `progress.json` checkpoint | Name the `--pass all` final report; output dir is fixed, so one audit per worktree at a time (WC-11) (P1) | `sk/sc-cleanup-audit-protocol/SKILL.md:76,113`; `cmd/cleanup-audit.md:112-117`; `INV-A:42` |
```
```text
- | init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report | None | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
```
```text
- | tdd | a precise component prompt, not a bare topic; `--output <file>` | the TDD at `--output` | `--resume <task-file>` | Under `--unattended`, the topic-only clarification and nested `/task` "ask the user" lines resolve as blocked (P2) | `sk/tdd/SKILL.md:48,52-61,190`; `sk/task/SKILL.md:49,114`; `cmd/tdd.md:29`; `INV-B:47,217-225` |
```
```text
- | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
```
```text
- 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path.
```
```text
- | P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |
```
```text
- | P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |
```

### AFTER (candidate)

```text
- | WC-4 | **One report file, at a path the coordinator can compute before dispatch, written on every outcome.** In unattended mode the command writes `return-contract.yaml` at the path in its Report column of section 3; where that column says only "contract", the file is in the directory passed as `--output` / `--output-dir`, or in the parent directory of the file when `--output` is a file (B-01). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
```
```text
- The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output flag value, from which the coordinator computes the contract path in the command's section 3 Report column (WC-4; for workflow the path comes back in `worker_done --report-path`) (B-01); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
```
```text
- The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `return-contract.yaml`, at the path rule in WC-4 unless the row names a path (B-01). Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
```
```text
- | adversarial | `--output <dir>`; never `--interactive` | `<output>/adversarial/return-contract.yaml` (filename not fixed today) | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract filename to the Report-column path (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
```
```text
- | cleanup-audit | `--pass <N>` (single pass) | `.claude-audit/pass<N>-summary.md`; contract `.claude-audit/return-contract.yaml` (fixed directory, no `--output`) | `progress.json` checkpoint | Name the `--pass all` final report; output dir is fixed, so one audit per worktree at a time (WC-11) (P1) | `sk/sc-cleanup-audit-protocol/SKILL.md:76,113`; `cmd/cleanup-audit.md:112-117`; `INV-A:42` |
```
```text
- | init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output`; contract in the parent directory of that file | Re-run overwrites its marked report | None | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
```
```text
- | tdd | a precise component prompt, not a bare topic; `--output <file>` | the TDD at `--output`; contract in the parent directory of that file | `--resume <task-file>` | Under `--unattended`, the topic-only clarification and nested `/task` "ask the user" lines resolve as blocked (P2) | `sk/tdd/SKILL.md:48,52-61,190`; `sk/task/SKILL.md:49,114`; `cmd/tdd.md:29`; `INV-B:47,217-225` |
```
```text
- | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` (`<id>` is created by the command; the worker passes the real path as `worker_done --report-path`); for a stop before the package exists, `.dev/tasks/to-do/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too, at that fallback path (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
```
```text
- 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the contract path computed from section 3 (WC-4) (B-01).
```
```text
- | P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names `<output>/adversarial/return-contract.yaml`; workflow states the contract is written for pre-creation STOPs at `.dev/tasks/to-do/return-contract.yaml` |
```
```text
- | P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic, contract expected in the parent directory of `<file>`; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |
```

### Self-check

Every AFTER line (without its `>`) was searched with `grep -nF` in the candidate and every BEFORE line (without its `<`) in the baseline: 11 of 11 found on each side, so the roles are not swapped. The diff is not empty.

## Prior blocking findings

| Id | Prior status | Re-review status | Reason (AFTER text only) |
|---|---|---|---|
| B-01 | open (`GATE:86`, verdict FAIL) | **resolved** | See the three sub-defects below. |

B-01 had three parts (`GATE:89-93`). Each was compared with the AFTER text:

1. **`--output` is a file (tdd, init-lite).** Resolved. WC-4 now says the contract is "in the parent directory of the file when `--output` is a file" (`SPEC:62`); the tdd and init-lite rows say "contract in the parent directory of that file" (`SPEC:90`, `SPEC:87`); AC-2.2 expects the contract "in the parent directory of `<file>`" (`SPEC:200`). The three texts now agree, and `<file>/return-contract.yaml` is no longer required anywhere.
2. **adversarial.** Resolved. The row names `<output>/adversarial/return-contract.yaml` (`SPEC:83`), AC-1.4 checks that exact path (`SPEC:198`), and the `<output-dir>/return-contract.yaml` generalisation is gone from WC-4 (`SPEC:62`), section 3's intro (`SPEC:76`) and 7.2 step 3 (`SPEC:182`). The inventory records that real runs wrote that location (`INV-A:35`, `INV-A:60`). State trace: brief `--output .dev/x/`; 7.2 step 3 now computes `.dev/x/adversarial/return-contract.yaml` from the row; step 4 `test -s` on that path passes for a correct implementation of the row.
3. **workflow and cleanup-audit (path not computable before dispatch).** Resolved. cleanup-audit now has a fixed `.claude-audit/return-contract.yaml` (`SPEC:85`; fixed directory is at `INV-A:42`). workflow keeps `.dev/tasks/to-do/<id>/return-contract.yaml`, says the worker passes the real path as `worker_done --report-path`, and names a fallback `.dev/tasks/to-do/return-contract.yaml` for stops before the package exists (`SPEC:92`); 2.3 carves workflow out of the "computed from the flag" rule (`SPEC:73`). The text no longer sends the coordinator to a path that cannot exist. (Two small leftovers are recorded as R-02 and R-03, both Medium.)

No resolved finding regressed. No prior finding was deferred or withdrawn by the reviser (`review/revise-gate.md` lists B-01 as applied).

## Findings on changed lines

Grading used the FIRST-REVIEW grading check (`PROMPTS:35-36`): blocking needs "an implementer who follows the stated text as written builds X, and X is wrong because Y" with no further assumption. No new finding passes that test. All three below need a guess, or name a requirement the document never states, so they are Medium.

### R-01 (Medium, origin=changed) WC-4's lookup rule has no answer for most Report cells

- Where: WC-4 (`SPEC:62`), 2.3 (`SPEC:73`), 7.2 step 3 (`SPEC:182`), against the Report columns of section 3.
- Stated text: the contract is written "at the path in its Report column of section 3; where that column says only 'contract', the file is in the directory passed as `--output` / `--output-dir`, or in the parent directory of the file when `--output` is a file" (`SPEC:62`).
- Why it does not close cleanly: a Report cell holds one of four things, and the rule covers two of them. (a) A contract path: adversarial, brainstorm, reflect, cleanup-audit, workflow, init-lite, tdd (`SPEC:83-85`, `:87-88`, `:90`, `:92`). Covered. (b) A non-contract report file: index-repo `PROJECT_INDEX.md` with "location implied" and a brief that passes no flag (`SPEC:86`), release-split `<output>/release-split-report.md` (`SPEC:89`), troubleshoot `REPORT.md` (`SPEC:91`). "The path in its Report column" is then the markdown file, not a contract. (c) Cells such as "add `--output`; contract plus the report" (`SPEC:99`), "contract pointing at `REVIEW.md` in `--output-dir`" (`SPEC:100`) or "add a report path; contract" (`SPEC:101`, `:103`, `:110`, `:123`). None "says only 'contract'", so the literal fallback does not apply, and a "report path" flag is neither `--output` nor `--output-dir`. (d) "contract (fields already defined; file location unnamed)" (`SPEC:105`). The coordinator cannot compute the path from the cell, which 2.3 and 7.2 step 3 say it does.
- Likely reading: the contract sits in the output directory next to the report. That reading is obvious but is a guess, and it is the same gap that made B-01 matter (the coordinator and the command must agree on one path). No wrong outcome follows without the guess (the worker still passes the real path in `worker_done --report-path`, `SPEC:62`), so Medium.
- Expert: Wiegers, Whittaker (Divergence). Recommendation: one line in WC-4: "where the cell names no contract path, the contract is in the directory that holds the named report or output file; if the command has no output flag, the brief supplies the directory." Priority: High among follow-ups. Quality impact: +1 Consistency.

### R-02 (Medium, origin=changed) Shared-directory contract paths collide, against WC-11

- Where: WC-4's "parent directory of the file" rule (`SPEC:62`, `:87`, `:90`), the cleanup-audit fixed path (`SPEC:85`) and the workflow fallback `.dev/tasks/to-do/return-contract.yaml` (`SPEC:92`), against WC-11 "Two workers in one worktree must never write the same file" (`SPEC:69`).
- Attack (Accumulation/Sequence): two tdd workers with `--output .dev/tdd/a.md` and `--output .dev/tdd/b.md` both write `.dev/tdd/return-contract.yaml`; the second overwrites the first, and the coordinator reads the wrong `status` for the first Task. Two workflow workers that both stop before creating a package write the one fallback file; the revise report admits this and left it unmitigated (`review/revise-gate.md`, "Decision for the author"). A second cleanup-audit worker in the same worktree has the same fixed path, which the row already limits to one audit at a time (`SPEC:85`).
- Why Medium: it needs the coordinator to choose the same directory (or two pre-creation stops at once). Nothing in the text forces that, but nothing prevents it, and the new paths are invented by this revision: neither `.claude-audit/return-contract.yaml` nor `.dev/tasks/to-do/return-contract.yaml` appears in an inventory line (`INV-A:42`; `INV-B:272` says only that the contract is not written for pre-creation stops), and the Decisions table does not record them.
- Recommendation: record both paths in Decisions, and add a clause to WC-4: the coordinator gives each file-valued `--output` worker its own directory.

### R-03 (Medium, origin=changed) The "computable before dispatch" claim and 7.2 step 3 still assume it for workflow

- Where: WC-4 title "at a path the coordinator can compute before dispatch" (`SPEC:62`); 7.2 step 3 "its report path is the contract path computed from section 3" (`SPEC:182`); workflow row (`SPEC:92`); 2.3 (`SPEC:73`).
- The workflow cell contains `<id>`, created by the command, so step 3 cannot compute it, and 2.3 says the path comes back in `worker_done --report-path` for workflow. The 7.2 pass condition has no such exception, so the check cannot be run as written for workflow (a P0 smoke command, AC-0.4, `SPEC:194`). An implementer will compare against the pattern; the outcome is not wrong without a guess. Medium.
- Recommendation: add "(for workflow, matches `.dev/tasks/to-do/<id>/return-contract.yaml`)" to step 3, or drop "compute before dispatch" from the WC-4 title.

## Dependencies of the changed lines, checked

- Section 3 intro (`SPEC:76`) "Contract means the WC-4 file ... at the path rule in WC-4 unless the row names a path": consistent with WC-4; the same gap as R-01 applies to rows with no path.
- AC-1.2 (`SPEC:196`) runs every P1 command with `--output <dir>`; index-repo has no output flag and cleanup-audit has a fixed directory. This is the inherited gate finding M-06 (`GATE:108`), not a change of this revision; the changed text does not make it worse and does not cite it. Minor note N-R4.
- AC-2.2 and AC-2.3: the `tdd` gate-trigger example now names the contract location and is consistent with the row (`SPEC:200`, `:90`).
- Step 4 (`SPEC:183`) uses `<contract>`; step 3 defines it, so no edit was needed there. Agreed with `review/revise-gate.md`.
- Counts: the changed lines alter no count. 10 / 27 / 6 and the phase totals (`SPEC:76`, `:159-162`) are unchanged; no new Quantity Flow Diagram is needed.

## Guard Condition Boundary Table (changed lines only, per Review Loop bullet 5)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| Contract-path rule | WC-4 (`SPEC:62`) | Zero/Empty | cell names a path | true | contract at that path | OK |
| Contract-path rule | WC-4, rows `SPEC:86`, `:89`, `:91`, `:99-110` | One/Minimal | cell names a non-contract file or a bare "report path" | unspecified | not stated (R-01) | GAP (Medium, R-01) |
| Contract-path rule | WC-4 | Typical | `--output <dir>` | true | contract in `<dir>` (or the row path) | OK |
| Contract-path rule | WC-4, tdd/init-lite (`SPEC:87`, `:90`) | Legitimate Edge Case | `--output <file>` | true | parent directory of the file | OK |
| Contract-path rule | WC-4, init-lite (`SPEC:87`) | Legitimate Edge Case | no `--output`, default report | true | parent of the default report; implied, not stated | OK (inferable) |
| Contract-path rule | WC-4, workflow (`SPEC:92`) | Sentinel Value Match | `<id>` not yet created | true | worker passes real path; fallback file for pre-creation stops | OK |
| Contract-path rule | WC-4 vs WC-11 (`SPEC:62`, `:69`) | Maximum/Overflow | two workers, same parent directory or same fixed path | true | overwrite; not specified | GAP (Medium, R-02) |
| 7.2 step 3 path check | `SPEC:182` | Legitimate Edge Case | workflow, `<id>` unknown | unspecified | not stated (R-03) | GAP (Medium, R-03) |

Left out, with reason: Zero/Empty for the step 3 check and for the collision rule (a check with no worker, and zero workers, cannot occur); Maximum for the first four rows (no capacity is involved). FR-8 and FR-9: each GAP is graded by consequence and none names a concrete wrong outcome without a guess, so all are Medium. The table is complete under FR-10; synthesis follows.

## === REQUIREMENTS ANALYSIS ===

Experts: Wiegers (lead), Adzic, Cockburn, with Whittaker. The single blocking defect is closed: the central requirement WC-4 and the per-command rows no longer contradict each other for the five commands B-01 named. What remains is incompleteness of the new lookup rule (R-01), a second-order collision (R-02) and one acceptance-check exception (R-03). Adzic: the examples in AC-1.4 and AC-2.2 now state the path they expect, which makes both checks passable.

## === ARCHITECTURE ANALYSIS ===

Experts: Fowler (lead), Newman, Hohpe, Nygard. Fowler: moving the path from a generalised formula to a per-command column is the narrower interface and fits the existing split (a command owns where it writes; the coordinator reads the column). Hohpe: the `worker_done --report-path` return of the real path is the right fallback for a path the coordinator cannot know. Nygard: the collision cases (R-02) are the only new failure mode. Whittaker: all five attacks run against the changed guards; Divergence found R-01, Accumulation found R-02, Sequence found R-03 (a pre-creation stop followed by a created package gives two contract locations for one workflow run; the row says the first is a fallback and the second is the real one, so the coordinator relies on `--report-path`).

## Minor notes (never fail the review)

- N-R1 `review/revise-gate.md` gives net bytes per line, not bytes added and deleted per finding id, and says why (a character diff was not run). Reviser contract bullet 6 asks for both. Totals check: 57939 to 58817, +878 (matches `wc -c` and the per-line sum).
- N-R2 The rows edited at `SPEC:83`, `:85`, `:87`, `:90`, `:92`, `:198`, `:200` do not carry the `(B-01)` id inline; only `SPEC:62`, `:73`, `:76`, `:182` do. The revise report maps them. Table cells are not paragraphs, so this is a note.
- N-R3 `SPEC:76` was edited although the Reviser brief's line list (`GATE:168`) did not name it; the revise report discloses this and the line restated the same generalisation (`<output-dir>/return-contract.yaml`), so it is within the finding.
- N-R4 AC-1.2 `--output <dir>` for index-repo and cleanup-audit (inherited M-06, unchanged).
- N-R5 The inherited Medium findings M-01 to M-13 and minor notes N-01 to N-08 (`GATE:96-146`) were not re-graded and none was edited. No Medium or minor finding was edited by the reviser (compared against the diff: only the B-01 lines changed).

## Coverage

Coverage: scoped PASS: changed lines + prior blockers.

Covered: the full diff (11 lines), the prior blocking finding B-01 re-checked against the AFTER text, the section 3 rows and section 7 checks that depend on the changed lines, the inventory lines the changed rows cite (`INV-A:35`, `:42`, `:60`, `:55`; `INV-B:272`), and the candidate's own consistency across WC-4, 2.3, 3, 7.2, AC-1.4 and AC-2.2. Not covered: the whole document (needs a separate, labelled first review; the gate review already served that role and this is its one re-review, so no further review follows); every `cmd/`, `sk/` and Orca-source cite (UNVERIFIED); no command was run. A brief clause overrode: none.

## Follow-up candidates (Medium and minor, none blocking, none enters the Reviser brief)

New: R-01 (Report cells with no contract path), R-02 (shared-directory collision and unrecorded invented paths), R-03 (workflow in 7.2 step 3). Inherited and still open: M-01 to M-13, N-01 to N-08 (`GATE:158-160`). Notes: N-R1 to N-R5.

Issue offer: this run is a coordinator-driven re-review whose reply is limited to the output path, so the user was not asked whether to open an issue for the list above, and none was created. The coordinator should put that question to the user once for the loop.

## Gate loop status

This is the re-review of the one gate loop (`PROMPTS:60`, `:63`). It ends with a PASS; no further review, fix cycle or gate loop is started. Totals for the document: the gate review plus this re-review, one fix cycle, within the 5-review and 3-fix-cycle ceiling.

## Reviser brief

Blocking finding ids: none. No revision is requested.

verdict: PASS
