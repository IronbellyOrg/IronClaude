review: 2 of 3

# Spec-panel review, round 2 (re-review): Orca worker-contract spec

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md`
- Prompt followed: RE-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full). Roles: CANDIDATE = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; BASELINE = `.dev/orca-command-refactor/specs/history/spec-v1.md`; PRIOR = `.dev/orca-command-refactor/review/round1.md`. `N` = prior `review: 1 of 3` (`round1.md:1`) plus 1 = 2.
- Candidate sha256: `e588d816f4ebe8cc73b0f945a07b3aaec6c6e366428b45f3edd87fcc2d7056f5` (58308 bytes)
- Baseline sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (57763 bytes; equals the candidate hash recorded in `round1.md:7`, so the baseline is the text round 1 reviewed)
- Prior sha256: `0e17a98cf654309492342908f66be87f2153de46f53573b3f72d884e2471f96b`
- Reviewer model used: Sonnet 5.5 (`claude-sonnet-5-5`). Review date 2026-11-10.
- Citation shorthand: `SPEC:N` = line N of the candidate; `BASE:N` = line N of the baseline; `R1:N` = line N of `review/round1.md`; `REV:N` = line N of `review/revise1.md`.
- Brief clauses overridden: none. The brief asked for the RE-REVIEW prompt and asked nothing the command forbids.

## What I covered

- Read in full: command.md, the review-loop prompts file, README, `round1.md`, `revise1.md`; read candidate sections 2.2, 2.3, 3, 4, 5, 6, 7 and 9 (D2-D4), and ran `diff -w` over the whole file.
- Re-checked B-1, B-2, B-3 against the AFTER text only. Reviewed every changed line (6 changed blocks) and the dependencies they touch: AC-1.2, AC-2.2, AC-4.1, D2, D3, D4, WC-9, section 3 rows for load, tdd, init-lite, spec-panel.
- Byte accounting in `revise1.md:8-19` (57763 before, 58308 after, +545) matches `wc -c` of the two files.
- Medium and minor findings of round 1 were not re-graded and were not edited by the reviser (`REV:3`); they stay in `follow-up candidates`.
- Not covered: command file text under `cmd/`, `sk/`, `ag/`, `CLAUDE.md`, EVIDENCE.md and the Orca guides are outside the sandbox, so every such citation stays **UNVERIFIED** (candidate `SPEC:11,25,285` claims included). The rf-qa Fix Cycle file (`.claude/agents/rf-qa.md`, `~/.claude/agents/rf-qa.md`) does not exist in the sandbox, so the re-check followed the rules in command.md Review Loop bullet 5, which stand alone.
- `--focus correctness` is not active, so no State Variable Registry. No pipeline whose count changes on a changed line, so no Quantity Flow Diagram (the changed lines add no stage).

## Step 1: evidence block (`diff -w BASELINE CANDIDATE`)

Roles as fixed above. Changed lines copied verbatim from the diff (`<` = BEFORE/baseline, `>` = AFTER/candidate). Hunks are labelled by their candidate line numbers.

```text
61,62c61,62
< | WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag. On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11) |
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
---
> | WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag. The answer may supply only a value that no safety rule or outward-action rule reserves: `implement`'s Ruling (D2(a)) and every flag WC-9 keeps off are excluded, and those gates still resolve as blocked. On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11) |
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). Where `--output` is a file (tdd, init-lite, spec-panel), the contract is `<value of --output>.return-contract.yaml` beside it, never inside it. It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
73c73
< The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
---
> The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, or the output file for tdd, init-lite and spec-panel, so the contract path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
76c76
< The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
---
> The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command except `load` also gains the `## Unattended mode` section (section 2.1) in its own phase. Phase numbers refer to section 6.
159c159
< | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
---
> | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by the commands named in this row (a no-op where a command has no gate; the P2-P4 commands in sections 3.1 and 3.2 get it in their own phase); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
195c195
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
---
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that each command named in the P1 row of section 6, except `load`, has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that neither `load` nor any section-4 command has one | passes |
```

Self-check before the verdict: each AFTER line (without `>`) was matched with `grep -cxF` against the candidate and each BEFORE line (without `<`) against the baseline; all 12 returned a count of 1. Roles are not swapped.

## Prior blocking findings

| id | Status | Reason (AFTER text only) |
|---|---|---|
| B-1 | resolved | `SPEC:159` now says the flag is "accepted by the commands named in this row", with the P2-P4 commands getting it "in their own phase". `SPEC:195` (AC-1.1) asserts the section for "each command named in the P1 row of section 6, except `load`", and that "neither `load` nor any section-4 command has one". `SPEC:76` now reads "Every changed command except `load` also gains the `## Unattended mode` section ... in its own phase". These agree with the `load` row (`SPEC:112`, report "none (see note)"), with P4 waiting for D2-D4 (`SPEC:154,162`) and with D3(a) "no pr-submit changes" (`SPEC:240`). The P1 row names 9 section-3.2 commands (analyze, build, business-panel, design, document, explain, index, test, load) matching the 9 P1 rows at `SPEC:99-123`, plus 4 fixes in section 3.1 (`SPEC:83,85,86,92`). I found no remaining contradiction between AC-1.1 and these rows. |
| B-2 | resolved | `SPEC:61` (WC-3) now bars the answer from supplying "a value that no safety rule or outward-action rule reserves", and names `implement`'s Ruling (D2(a)) and "every flag WC-9 keeps off" as excluded, with "those gates still resolve as blocked". That agrees with D2(a) (`SPEC:234`), AC-4.1 (`SPEC:208`), WC-9 (`SPEC:67`) and D4(a) (`SPEC:245`). The state trace of `R1:108` (halted `implement`, coordinator replies "approved", re-invoke records a Ruling) no longer follows from the text. |
| B-3 | resolved | `SPEC:62` (WC-4) now says that where `--output` is a file (tdd, init-lite, spec-panel) the contract is `<value of --output>.return-contract.yaml` "beside it, never inside it". For `--output docs/x/TDD_FOO.md` that gives `docs/x/TDD_FOO.md.return-contract.yaml`; the TDD stays a file. `SPEC:73` (2.3) now has the brief name "the output file for tdd, init-lite and spec-panel", so the path is known before dispatch. AC-2.2 (`SPEC:200`) can read the contract at a defined path. |

## Findings on changed lines

Findings are numbered fresh; they are not blocking prior ids. No new blocking finding was found.

| id | Severity | Blocking? | origin | Title |
|---|---|---|---|---|
| R2-M1 | Medium | no | changed | WC-3 hard-codes the D2(a) outcome while D2 is open |
| R2-M2 | Medium | no | changed | "safety rule" in WC-3 has no list beyond the Ruling and WC-9 flags |
| R2-M3 | Medium | no | changed | WC-4 file-valued rule covers three commands; other new output flags have no stated kind |
| R2-M4 | Medium | no | unchanged (quotes changed line `SPEC:159`/`SPEC:195`) | AC-1.2 "each P1 command" still includes `load`, which has no contract |
| R2-N1 | MINOR | no | changed | `SPEC:76` "Contract" definition still shows only the directory form |

### R2-M1 (Medium): WC-3 names D2(a) as fixed
`SPEC:61` excludes "`implement`'s Ruling (D2(a))". D2 is an open user decision (`SPEC:232-236`), and D2(b) lets the coordinator relay the person's words as a Ruling (`SPEC:235`). If the user chooses (b), WC-3 as written still forbids it, and AC-4.1 (`SPEC:208`) already carries the "unless D2 allows a relayed one" wording. Not a stated text that does harm today (the recommended path is (a)); needs the assumption that (b) is chosen. Medium.

### R2-M2 (Medium): "safety rule" undefined
`SPEC:61` excludes values "reserved" by "a safety rule or outward-action rule", and names two items. Other gates that exist for safety, such as task's confidence below 0.70 (`SPEC:121`) and the cleanup "Approval Required" items (`SPEC:103`), are not named as excluded or allowed. An implementer must guess. A requirement the document does not state, so Medium.

### R2-M3 (Medium): file-valued `--output` only for three commands
`SPEC:62` fixes the file-valued form for tdd, init-lite and spec-panel. Rows that add an output flag of unstated kind (analyze `SPEC:99`, design `SPEC:106`, document `SPEC:107`, explain `SPEC:108`, recommend `SPEC:115`, post-release `SPEC:113`) leave open whether it is a directory or a file. If one is a file, the pre-fix defect of B-3 returns for it. Not a text that does harm as written (the kind is simply unstated), so Medium.

### R2-M4 (Medium): AC-1.2 and `load`
`SPEC:159` still lists `load` among "the commands named in this row", and `SPEC:196` (AC-1.2) runs the live check "on each P1 command with `--unattended --output <dir>`". Step 3 and step 4 of 7.2 (`SPEC:182-183`) need a WC-4 contract path, but `load` has "none" (`SPEC:112`) and AC-1.1 now says it has no section (`SPEC:195`). Read literally the check cannot pass for `load`. This is an older defect (present at `BASE:196`) that the B-1 revision left behind; round 1 did not name AC-1.2. Medium because it needs the reading "each P1 command" includes `load`, which `SPEC:112` ("use it as a step inside another worker's brief, not as its own Task") argues against.

### R2-N1 (MINOR): `SPEC:76`
`SPEC:76` still defines "Contract" as `<output-dir>/return-contract.yaml`. WC-4 qualifies it, so this is a note.

## Adversarial analysis (Whittaker, changed lines only)

- **Sentinel Collision Attack.** I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-4 (`SPEC:62`)** fails when `--output` names a file whose path already ends in `.return-contract.yaml`. Concrete attack: `--output x.return-contract.yaml` gives `x.return-contract.yaml.return-contract.yaml`. Benign; the name is still unique and beside the file. No finding.
- **Divergence Attack.** I can break this specification by **Divergence Attack**. The invariant at **WC-3 (`SPEC:61`)** fails where both branches apply: an answer that is both an ordinary value and a reserved flag (`post-release --output` plus an install flag in one reply). Concrete attack: before, gate blocked; the coordinator replies with two values, one allowed and one reserved; the text says the reserved one is excluded, "those gates still resolve as blocked" is ambiguous on whether the allowed one is applied. Medium, covered by R2-M2.
- **Sequence Attack.** I can break this specification by **Sequence Attack**. The invariant at **`SPEC:76`, `SPEC:159`, `SPEC:195`** fails if P1 ships `load` with a section. AC-1.1 now rejects that, so the sequence is caught. No finding.
- **Zero/Empty Attack.** `--unattended` with no `--output` and a tdd/init-lite/spec-panel command: `<value of --output>` is empty, so `SPEC:62` has no path. This is the unchanged M-5 of round 1 (`R1:76-78`); not recounted.
- **Accumulation Attack.** No counter or collection on a changed line.

## Guard Condition Boundary Table (changed lines only)

Classes left out, with the reason: "Maximum/Overflow" is left out for every guard (set membership and a path rule, not quantities); "One/Minimal" is folded into Typical.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-3 reserved-value exclusion | SPEC:61 | Typical | answer supplies `--suite` for cli-eval | not reserved | applied via re-invoke | OK |
| WC-3 reserved-value exclusion | SPEC:61 | Sentinel Value Match | answer to `E-HALT-QA` Ruling | reserved | gate resolves as blocked | OK |
| WC-3 reserved-value exclusion | SPEC:61 | Sentinel Value Match | answer for a flag WC-9 keeps off (`--post-pr`) | reserved | gate resolves as blocked | OK |
| WC-3 reserved-value exclusion | SPEC:61, SPEC:235 | Legitimate Edge Case | D2(b) chosen | reserved by text | still blocked; contradicts D2(b) | GAP (R2-M1, Medium: names no wrong outcome under the recommended D2(a)) |
| WC-3 reserved-value exclusion | SPEC:61, SPEC:121 | Legitimate Edge Case | task confidence below 0.70 answered by the coordinator | unspecified | unspecified | GAP (R2-M2, Medium) |
| WC-4 file-valued rule | SPEC:62 | Zero/Empty | `--output` absent | unspecified | unspecified | GAP (Medium, carries round-1 M-5) |
| WC-4 file-valued rule | SPEC:62 | Typical | `--output docs/x/TDD_FOO.md` | true | `docs/x/TDD_FOO.md.return-contract.yaml` | OK |
| WC-4 file-valued rule | SPEC:62 | Typical | `--output <dir>` for adversarial | false | `<dir>/return-contract.yaml` | OK |
| WC-4 file-valued rule | SPEC:62 | Legitimate Edge Case | new output flag of unstated kind (analyze, design, document, explain, recommend, post-release) | unspecified | unspecified | GAP (R2-M3, Medium) |
| P1 scope / AC-1.1 | SPEC:159, SPEC:195 | Typical | analyze | in P1 row, not `load` | section required | OK |
| P1 scope / AC-1.1 | SPEC:159, SPEC:195 | Legitimate Edge Case | `load` | in P1 row, excepted | no section | OK |
| P1 scope / AC-1.1 | SPEC:195 | Legitimate Edge Case | section-4 command | not in P1 row | no section | OK |
| P1 scope / AC-1.1 | SPEC:159, SPEC:196 | Legitimate Edge Case | `load` under AC-1.2 | in P1 row | live check needs a contract it does not have | GAP (R2-M4, Medium) |

FR-10 check: every guard on a changed line is enumerated, every cell is populated and omitted classes carry a reason. The table is complete. No GAP names a concrete wrong outcome an implementer produces from the stated text, so none is blocking.

## Follow-up candidates (Medium and minor findings)

These never trigger a revision. This sandbox has no user channel, so the once-per-loop question about opening an issue was not asked and no issue was created. The list is recorded here.

- R2-M1 WC-3 names D2(a) while D2 is open.
- R2-M2 "safety rule" in WC-3 undefined beyond two items.
- R2-M3 output-flag kind unstated for six commands.
- R2-M4 AC-1.2 still includes `load` (older defect, `BASE:196`; surfaced by the B-1 revision).
- R2-N1 `SPEC:76` "Contract" shows the directory form only.
- Round-1 Medium and minor findings M-1 to M-12, N-1, N-2 and the unnumbered GAP rows of `R1:205-223` were not edited (`REV:31-35`) and stay open as follow-up candidates.

coverage: scoped PASS: changed lines + prior blockers

verdict: PASS
