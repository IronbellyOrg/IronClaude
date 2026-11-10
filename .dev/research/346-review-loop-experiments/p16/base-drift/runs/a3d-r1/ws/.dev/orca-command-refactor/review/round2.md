review: 2 of 3

# Spec-panel re-review: orca-worker-contract-spec.md

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md`
- Roles (fixed by the table in `~/.claude/rules/prompts/document_review_loop_prompts.md`, RE-REVIEW prompt): CANDIDATE = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; BASELINE = `.dev/orca-command-refactor/specs/history/spec-v1.md`; PRIOR = `.dev/orca-command-refactor/review/round1.md`.
- sha256 CANDIDATE: `0d7786a334196b491d4a4779d2dbbc71fedd95552ea14ed522742fd98a72bf68`
- sha256 BASELINE: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (equals the candidate hash recorded in `review/round1.md:6`, so the baseline is the text round 1 reviewed)
- sha256 PRIOR: `89d4645667efa5b95243f0bc30f184dcc94e927a87c5dabcae3d0709fbe363ba` (`review/round1.md:1` is `review: 1 of 3`, so N = 2; `verdict: FAIL` at `review/round1.md:155`, so the cap check does not stop the run)
- Reviewer model actually used: claude-sonnet-5-5
- Prompt followed: RE-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full): roles, Step 1, review number, self-check. The re-check of prior blockers is meant to follow steps 1-5 of the Fix Cycle process in `.claude/agents/rf-qa.md` or `~/.claude/agents/rf-qa.md`; neither file exists in the sandbox (UNVERIFIED), so the rules of `command.md` Review Loop (bullets 1-7) were applied on their own, as that section allows.
- No brief clause was overridden. The brief widens nothing and regrades nothing.
- Citation convention: `spec:N` = line N of the candidate; `base:N` = line N of the baseline; `r1:N` = line N of the prior report; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md` (the only evidence I could check). Any citation to `src/`, `CLAUDE.md`, `~/.claude/...` other than the prompt file, `.dev/evals/...`, `.dev/codegraph-migration/...` or Orca guides is UNVERIFIED unless an inventory quotes it.
- Focus: requirements and architecture. `--focus correctness` is not active, so no State Variable Registry is produced. `--iterations` is ignored and no revised specification is written (Review Loop bullet 4).

## Step 1: evidence block (`diff -w BASELINE CANDIDATE`)

The diff has 11 hunks (lines 62, 73, 76, 79, 83, 92, 149, 159, 162, 195, 198 of the candidate). Each `<` line is copied verbatim under BEFORE (baseline) and each `>` line under AFTER (candidate).


### Hunk 62c62

BEFORE (baseline):

```text
| WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
```

AFTER (candidate):

```text
| WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes the contract at a path the brief names: `<dir>/return-contract.yaml` when the coordinator passes a directory (`--output` / `--output-dir`), or `<file>.return-contract.yaml` beside the file when `--output` is a file (so two workers given `a.md` and `b.md` never share one, WC-11). Two named exceptions: adversarial writes `<output>/adversarial/return-contract.yaml`; workflow writes `.dev/tasks/to-do/<id>/return-contract.yaml`, whose `<id>` the command creates, so the worker finds the path after the package exists and a stop before the package exists writes no contract (WC-5: no report means `--outcome failed`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists (except workflow's pre-creation stops, above). Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
```


### Hunk 73c73

BEFORE (baseline):

```text
The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
```

AFTER (candidate):

```text
The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory or file, so the report path is known before dispatch (WC-4; workflow excepted); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
```


### Hunk 76c76

BEFORE (baseline):

```text
The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
```

AFTER (candidate):

```text
The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 contract file. Every changed command also gains the `## Unattended mode` section (section 2.1) in its own phase, except `load` (no contract, usage-line fix only) and `pr-submit` (changed only if D3 (b) is chosen). Until a command's phase passes, the coordinator does not put `--unattended` in its brief. Phase numbers refer to section 6.
```


### Hunk 79c79

BEFORE (baseline):

```text
These run as workers now if the brief uses the stated flags; the worker reports the named file until Phase 1 adds the contract. The only command changes are the small fixes in the last column.
```

AFTER (candidate):

```text
These run as workers now if the brief uses the stated flags; the worker reports the named file until the command's own phase (last column) adds the contract. `brainstorm` and `init-lite` have no change and no `## Unattended mode` section. The only command changes are the small fixes in the last column.
```


### Hunk 83c83

BEFORE (baseline):

```text
| adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
```

AFTER (candidate):

```text
| adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract filename to `<output>/adversarial/return-contract.yaml`, the WC-4 exception path (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
```


### Hunk 92c92

BEFORE (baseline):

```text
| workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
```

AFTER (candidate):

```text
| workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | None: a pre-creation STOP writes no contract and the worker reports `--outcome failed` (WC-4 exception, WC-5) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
```


### Hunk 149c149

BEFORE (baseline):

```text
| SA-4 | Command-file edits in Phases 1-3 are additive: a new `## Unattended mode` section and new flags. Existing lines change only where section 3 names a defect fix (roadmap and validate-roadmap drift, validate-tests target, adversarial and workflow contract gaps, explain tools, business-panel frontmatter, load usage line), and each such fix must keep the standalone behaviour or correct a documented defect. | Keeps the diff reviewable and SA-1 checkable. | Section 3 "Other required change" column |
```

AFTER (candidate):

```text
| SA-4 | Command-file edits in Phases 1-3 are additive: a new `## Unattended mode` section and new flags. Existing lines change only where section 3 names a defect fix (roadmap and validate-roadmap drift, validate-tests target, adversarial contract gap, explain tools, business-panel frontmatter, load usage line), and each such fix must keep the standalone behaviour or correct a documented defect. | Keeps the diff reviewable and SA-1 checkable. | Section 3 "Other required change" column |
```


### Hunk 159c159

BEFORE (baseline):

```text
| **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
```

AFTER (candidate):

```text
| **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by the commands listed in this row, except `load` (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
```


### Hunk 162c162

BEFORE (baseline):

```text
| **P4. Outward actions and safety rules** | Apply the answers to D2-D4: the implement halt path, post-release pre-authorization, pr-submit as a worker. | implement, post-release, pr-submit | Each one either changes a deliberate safety rule (`sk/sc-implement-protocol/refs/qa.md:238`) or performs outward actions (`sk/sc-pr-submit-protocol/SKILL.md:189,196`; `sk/sc-post-release-protocol/SKILL.md:340,351`), so it needs the user's decision first. |
```

AFTER (candidate):

```text
| **P4. Outward actions and safety rules** | Apply the answers to D2-D4: the implement halt path, post-release pre-authorization, pr-submit as a worker (only if D3 (b)). | implement, post-release, pr-submit | Each one either changes a deliberate safety rule (`sk/sc-implement-protocol/refs/qa.md:238`) or performs outward actions (`sk/sc-pr-submit-protocol/SKILL.md:189,196`; `sk/sc-post-release-protocol/SKILL.md:340,351`), so it needs the user's decision first. |
```


### Hunk 195c195

BEFORE (baseline):

```text
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
```

AFTER (candidate):

```text
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every P1 command (the commands listed in the P1 row, not `load`) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
```


### Hunk 198c198

BEFORE (baseline):

```text
| P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |
```

AFTER (candidate):

```text
| P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names the one fixed path `<output>/adversarial/return-contract.yaml` |
```


Self-check (run before the verdict): every AFTER line above (without `>`) was searched with `grep -nF` in the candidate and every BEFORE line (without `<`) in the baseline. All 11 AFTER quotes were found in the candidate and all 11 BEFORE quotes in the baseline. No role was swapped. Byte sizes: baseline 57763, candidate 58693 (`wc -c`), which matches `review/revise1.md` (before 57763, after 58693).

## Coverage

Covered: the whole diff (11 hunks), the dependants of each changed line (WC-2, WC-5, WC-11 for WC-4; section 2.3; the P1, P2, P4 rows; AC-0.4, AC-1.1 to AC-1.4, AC-2.2, 7.2 steps 3-4; SA-3, SA-4; sections 3.1, 3.2 and 4 rows for adversarial, workflow, load, pr-submit, tdd, spec-panel, init-lite, brainstorm), the six-guard check on changed lines, `review/revise1.md` (byte accounting and scope), and the inventories for the adversarial and workflow location facts (`INV-A:35`, `INV-B:272`, `INV-B:57-65`).

Not covered / UNVERIFIED: every `src/superclaude/...`, `CLAUDE.md`, `cmd/` and `sk/` line the spec cites (the workspace has no `src/`); the rf-qa agent file (absent). Unchanged text is not re-reviewed beyond what a changed line depends on.

## Prior blocking findings (table)

| Id | Status | Basis |
|---|---|---|
| B-1 | resolved | WC-4 (`spec:62`) now states the location for every case round 1 named: `<dir>/return-contract.yaml` for a directory value, `<file>.return-contract.yaml` beside the file for a file-valued `--output` (two workers given `a.md` and `b.md` get different files, which also keeps WC-11 at `spec:69`), adversarial at `<output>/adversarial/return-contract.yaml` (matches the observed runs, `INV-A:35`), and workflow at `.dev/tasks/to-do/<id>/return-contract.yaml` with the id created by the command (`INV-B:272`). The pre-creation workflow STOP is no longer promised a contract, which agrees with the command's own text that no contract is written there (`INV-B:272`, quoting `refs/return-contract.md:39`), and WC-5 (`spec:63`) maps "no report" to `--outcome failed`. The workflow row (`spec:92`), the adversarial row (`spec:83`), section 2.3 (`spec:73`), the section 3 intro (`spec:76`), SA-4 (`spec:149`), the P1 list (`spec:159`) and AC-1.4 (`spec:198`) all agree with WC-4. No remaining text asks for the contradicted behaviour. |
| B-2 | resolved | AC-1.1 (`spec:195`) now asserts the section only for "every P1 command (the commands listed in the P1 row, not `load`)", which matches the `load` row ("none (see note)", `spec:112`; `INV-B:57-65`). The P1 flag requirement (`spec:159`) is limited to the commands in that row, `load` excluded. `pr-submit` is excepted at `spec:76` and `spec:162` ("only if D3 (b)"), which matches D3 (a) (`spec:240`) and section 4 (`spec:139`). The interim state "flag accepted, gate not yet built" is handled by the brief-side rule at `spec:76` ("Until a command's phase passes, the coordinator does not put `--unattended` in its brief"); see M-11 for a flaw in that sentence that is not blocking. |

## Findings on changed lines

Guard Condition Boundary Table (guards on changed lines only, Review Loop bullet 5). Guards: G7' contract location rule (`spec:62`); G8 `--output` file versus directory (`spec:62`); G9 workflow pre-creation STOP (`spec:62,92`); G10 "until a command's phase passes" brief rule (`spec:76`); G11 AC-1.1 assertion set (`spec:195`). Classes left out: Maximum/Overflow and Sentinel for all five (no capacity or sentinel value in the text).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|--------------------|--------|
| G8 file vs dir | spec:62 | Typical | `--output .dev/out/` | directory | `.dev/out/return-contract.yaml` | OK |
| G8 | spec:62 | Legitimate Edge Case | `--output .dev/out/a.md` and `b.md` | file | `a.md.return-contract.yaml`, `b.md.return-contract.yaml`, distinct | OK |
| G8 | spec:62 | Zero/Empty | `--output` absent (adversarial, workflow) | neither | named exceptions give the path | OK |
| G9 workflow STOP | spec:62,92 | Zero/Empty | stop before the package exists | true | no contract, `--outcome failed` (WC-5) | OK |
| G9 | spec:62,92 | Legitimate Edge Case | stop after the package exists | false | contract written with `status` | OK |
| G10 phase rule | spec:76 | Typical | command's phase not passed | true | `--unattended` not in brief | OK |
| G10 | spec:76,196-203 | Legitimate Edge Case | the phase's own acceptance check needs `--unattended` | true | check passes it, rule forbids it | GAP (M-11, Medium) |
| G11 AC-1.1 | spec:195 | Typical | P1 command | in set | section asserted | OK |
| G11 | spec:195,112 | Legitimate Edge Case | `load` | out of set | no assertion | OK |
| G11 | spec:195,159 | Legitimate Edge Case | cleanup-audit, index-repo, adversarial ("fixes to" in the P1 row) | in set | section asserted, per `spec:76` ("every changed command") | OK |

FR-10: complete for the guards enumerated. The one GAP is graded Medium below (FR-8: it needs the reader to pick the worse of two readings of "passes").

No new blocking finding. Findings below are Medium or minor.

## === REQUIREMENTS ANALYSIS ===

### M-11 (Medium; Wiegers, Whittaker sequence attack). `origin=changed`. The brief-side rule "until a command's phase passes" collides with the phase checks.
`spec:76` says "Until a command's phase passes, the coordinator does not put `--unattended` in its brief." Section 6 (`spec:154`) says a phase passes when its section 7 checks pass. The checks themselves pass `--unattended` for that phase's commands before it can have passed (AC-1.2, `spec:196`; AC-2.2, `spec:200`). Read as written, the rule forbids the acceptance run. It becomes workable if "passes" means "has been implemented". The text allows both readings, so an implementer must guess; Medium, not blocking. Narrowest repair: say "implemented" (or "until the command's edit is merged") instead of "passes".

### M-12 (Medium; Wiegers). `origin=unchanged`, depends on the changed line `spec:195` ("every P1 command (the commands listed in the P1 row, not `load`)"). AC-1.2 still says "each P1 command" with `--unattended --output <dir>` (`spec:196`).
Under the new definition of "P1 command" the term excludes `load`, so the earlier `load` conflict is closed. What remains is that `--output <dir>` is passed to cleanup-audit and index-repo, which have a fixed output location and no output flag (`spec:85-86`; the P1 row adds output flags only "for commands that lack one", `spec:159`). The text does not say whether those two commands gain `--output`. Not blocking: no stated text is shown to build a wrong deliverable, it is an unstated edge case.

### M-13 (Medium; Nygard). `origin=changed`. A workflow stop before the package exists reaches the coordinator with no machine-readable reason.
WC-4 and the workflow row (`spec:62,92`) now say no contract is written, and WC-5 reports `--outcome failed` with a prose first sentence (`spec:63`). The coordinator cannot tell a pre-creation STOP from a crash without reading the transcript, and WC-2 (c) (`spec:60`) promises a `blocked` report with the question. The workflow row lists no gate for `--handoff none` (`INV-B:267-275`), so the promise is not broken today; Medium because it depends on what the pre-creation STOPs are, which the spec does not list.

## === ARCHITECTURE ANALYSIS ===

No blocking architectural defect on the changed lines. The two named exceptions in WC-4 are narrower than the prior text, and removing the workflow "pre-creation STOP" fix deletes a requirement instead of inventing an id-less path, which is the direction Review Loop bullet 6 asks for. The coordinator still opens one file per Task; the exception paths are stated in the same row, so the brief template (`spec:73`) can carry them.

## === OTHER MEDIUM AND MINOR FINDINGS ===

### M-14 (Medium; Adzic). `origin=unchanged`, depends on the changed line `spec:79`. AC-0.4 says "the contract arrives in P1" (`spec:194`); `spec:79` now says the contract arrives in each command's own phase, so for `/sc:troubleshoot` it arrives in P2 (`spec:91`) and for `/sc:workflow` never (`spec:92`). The P0 check only uses "the command's existing report file", so no wrong outcome follows. The reviser noted this residual (`review/revise1.md`, residual notes).

### M-15 (Medium; Fowler). `origin=changed`. `spec-panel` row (`spec:120`) says "add `--output`; contract", and the new file-valued rule gives `<file>.return-contract.yaml`. The command definition in the sandbox already names a directory-valued `--report-dir` for the contract and says "`--output` is file-valued" (`command.md:460-461`), so the two rules differ for that command. Which revision of the command the spec saw is UNVERIFIED (`r1:124`, n-4). Medium: the choice between two documented rules is a guess.

### Minor notes (never blocking)
- n-6: `spec:62` row is now about 2,000 characters in one table cell; a short list under the table would be easier to check (style).
- n-7: `spec:76` mixes a definition ("Contract" means ...) with three rules in one paragraph; consider splitting. Style only.
- Carry-over: prior Medium and minor findings M-1 to M-10 and n-1 to n-5 (`r1:89-125`) sit on unchanged lines that no changed line depends on, except M-3 and M-7 (see below); they are not re-graded.
  - M-3 (`r1:95`, fresh directory versus a path fixed before dispatch): WC-4 now says "a path the brief names" (`spec:62`), which narrows but does not close it. Still Medium, open.
  - M-7 (`r1:109`, SA-3 versus WC-4): unchanged; AC-1.3 (`spec:197`) is unchanged. Still Medium, open.

## Newly discovered older defects

None severe. No defect in unchanged text was found that is blocking.

## Consensus and disagreements

- Consensus: B-1 and B-2 are repaired by narrowing and deleting, with additions limited to the exception paths and the "only if D3 (b)" qualifiers. The revision stays inside the Reviser brief (`r1:146-153`): every changed hunk maps to B-1 (`spec:62,73,83,92,149,159,198`) or B-2 (`spec:76,79,159,162,195`); no Medium or minor finding was edited.
- Disagreement (Wiegers versus Fowler): Wiegers wants M-11 fixed now because the rule contradicts the checks; Fowler accepts the "implemented" reading as obvious. Both agree it is not blocking.

## Follow-up candidates (Medium and minor, not blocking, not in the Reviser brief)

M-11, M-12, M-13, M-14, M-15, n-6, n-7, plus the still-open prior M-1 to M-10 and n-1 to n-5 (`r1:140-142`). The session that ran this review would ask the user once whether to open an issue for them; this run is a non-interactive worker, created none and asked nothing. Unattended behaviour: list recorded only.

Coverage line: scoped PASS: changed lines + prior blockers

Reviser brief: none. No blocking finding is open (B-1 and B-2 resolved), so there is nothing to revise.

verdict: PASS
