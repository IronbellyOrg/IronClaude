review: 2 of 3

# /sc:spec-panel critique report, round 2 (re-review)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md`
- CANDIDATE: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `e83580105a91cbd66307f4ec8d971d860124f6e64bbad15157d508a0bfc3be1e`
- BASELINE: `.dev/orca-command-refactor/specs/history/spec-v1.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- PRIOR: `.dev/orca-command-refactor/review/round1.md`, sha256 `3959c9e309e510add709645a304fee0135f02296406fa370d0b79657a2c32212`; its header is `review: 1 of 3`, so N = 2 (round1.md:1).
- reviewer model actually used: `claude-sonnet-5-5`
- lint evidence: `.dev/orca-command-refactor/review/lint-2.md:1-5`, sha256 `e8358010...3bc1e` equals the candidate hash ("Checks: REF. Findings: 0. No findings."). There is no lint id on changed lines or new since round 1, so none to confirm or dismiss. A lint id never fails a review by itself.
- prompt followed: RE-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:35-49`. Prior blocking re-check followed the Fix Cycle process of `rf-qa` only in spirit: neither `.claude/agents/rf-qa.md` nor `~/.claude/agents/rf-qa.md` was read (outside this sandbox's workspace), so the rules of the command's Review Loop section 5 stand alone.
- brief clauses overridden: none. The coordinator's brief did not widen scope or regrade a minor finding.
- notation: `SPEC:N` = line N of the candidate; `BASE:N` = line N of the baseline; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `R1:N` = `round1.md` line N.

## Step 1: evidence block (`diff -w BASELINE CANDIDATE`)

Six hunks, all tagged F1. Roles were fixed by the brief, not by reading order. Quoted lines are abridged with `...` only where the middle is unchanged.

**BEFORE (baseline)**
- BASE:62 `| WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). ... including stops before any other output exists. Commands that already write a contract keep their fields ...`
- BASE:76 `... "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. ...`
- BASE:92 `... | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | ...`
- BASE:182 `... its report path is the WC-4 contract path.`
- BASE:196 `| P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |`
- BASE:198 `... | adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |`

**AFTER (candidate)**
- SPEC:62 `| WC-4 | **One report file, written on every outcome.** In unattended mode the command writes its contract at the path section 3 names for it, which is `<output-dir>/return-contract.yaml` when the row names none, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`) (F1). The coordinator derives that path from the brief; where it contains an id the command creates (workflow), the worker's `--report-path` gives it (F1). ... including stops before any other output exists, except a stop before the contract's directory exists, which writes none and is reported through the `worker_done` body without `--report-path` (F1). ...`
- SPEC:76 `... "Contract" means the WC-4 file at the path the row names, else `<output-dir>/return-contract.yaml` (F1). ...`
- SPEC:92 `... | None for pre-creation STOPs: no package directory exists, so no contract is written; the worker sends `--outcome failed` with the STOP reason in the body and no `--report-path` (WC-4, F1) | ...`
- SPEC:182 `... its report path is the contract path WC-4 gives for that command (F1).`
- SPEC:196 `| P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended` and the brief flags section 3 lists for it (F1) | all steps pass |`
- SPEC:198 `... | adversarial names one fixed path, `<output>/adversarial/return-contract.yaml`; workflow states pre-creation STOPs write no contract (F1) |`

Self-check done with `grep -cF`: each AFTER line was found once in the candidate and 0 times in the baseline; each BEFORE line was found once in the baseline and 0 times in the candidate. Roles are not swapped. The diff is not empty.

## Prior blocking findings

| id | prior status | now | evidence (AFTER text only) |
|---|---|---|---|
| F1 | blocking, open (R1:68-76) | **resolved** | (1) Adversarial vs WC-4: WC-4 now gives the path "section 3 names", so the adversarial row's `<output>/adversarial/return-contract.yaml` (SPEC:83, unchanged) is the contract path and no longer collides; it matches the real runs (INV-A:35, INV-A:60) and AC-1.4 (SPEC:198). (2) Workflow path unknowable before dispatch: SPEC:62 now says the worker's `--report-path` gives an id the command creates, and drops "known before dispatch" from the rule; the workflow row passes only `--handoff none` (SPEC:92), consistent with that. (3) Pre-creation workflow STOP: SPEC:92 and SPEC:62 now state no contract is written and the STOP is reported in the `worker_done` body without `--report-path`, matching INV-B:272 ("Not written for pre-creation STOPs") and CAPS:74 (no placeholder path); WC-5 already maps "no report exists" to `--outcome failed` (SPEC:63). (4) Check text: step 3 (SPEC:182) and AC-1.2 (SPEC:196) now refer to the per-command path and the section 3 brief flags, so AC-1.2 no longer forces an `--output <dir>` workflow does not take. No finding that the prior report marked resolved exists, so nothing is `regressed`. |

## Findings on changed lines (origin=changed) and dependents

Grading used the prompt's grading check. None of the findings below passes the blocking test, because each needs a guess that the implementer picks the worse of two allowed readings, or concerns a requirement the text never states.

| id | bucket | label | grade | origin | spec location | expert |
|---|---|---|---|---|---|---|
| R2-M1 | requirements | MAJOR | Medium | unchanged (quotes changed line SPEC:62) | SPEC:73, SPEC:62, SPEC:92 | Wiegers |
| R2-M2 | requirements | MAJOR | Medium | changed | SPEC:182, SPEC:62 | Adzic |
| R2-M3 | requirements | MAJOR | Medium | changed | SPEC:62, SPEC:60, SPEC:200 | Whittaker |

## === REQUIREMENTS ANALYSIS ===

Wiegers (lead), Adzic, Cockburn.

- R2-M1 (Medium). Inherited section 2.3 still says the brief states "the output directory, so the report path is known before dispatch (WC-4)" for each Task (SPEC:73). The changed WC-4 no longer makes that claim and says the workflow path comes from the worker's `--report-path` (SPEC:62), and the workflow row's brief has no output directory (SPEC:92). An implementer building the brief template from 2.3 may add an output directory for workflow that its flags do not accept, or omit it; the text allows either reading, and the outcome is only a brief wording difference, not a lost contract. The reviser noted this residual (`revise1.md:17`). Not blocking.
- R2-M2 (Medium). Live check step 3 now says the report path must be "the contract path WC-4 gives for that command" (SPEC:182). For workflow, WC-4 says that path is given by the worker's own `--report-path` (SPEC:62), so for that one command the pass condition compares the value to itself and cannot fail on a wrong path. Step 4 still opens the file (`test -s`, status in set, SPEC:183), so a missing or empty contract is caught; only a worker reporting a different existing path goes unchecked. Say the workflow contract lives at `.dev/tasks/to-do/<id>/return-contract.yaml` for the `<id>` found by listing the directory.
- Requirements coverage otherwise: SPEC:76 now matches SPEC:62 and the rows (SPEC:83, SPEC:92); AC-1.2 (SPEC:196) and AC-1.4 (SPEC:198) are consistent with them. FR-8/FR-9 for changed guards are in the table below.

## === ARCHITECTURE ANALYSIS ===

Fowler (lead), Nygard, Newman, Hohpe.

- The change narrows rather than adds: net +615 bytes (`revise1.md:6-8`), one rule in WC-4 shared by the rows and the checks, in line with the Reviser brief (R1:185-192). Verified size of candidate 58378 bytes against 57763 for the baseline.
- Interface boundary unchanged: the contract is still written by the command, reported by the worker, read by the coordinator (SPEC:62). No new section, mechanism or mapping was added.
- The new exception in WC-4 does not conflict with WC-5 (SPEC:63) or WC-2(c) (SPEC:60) for the cases the rows name; the one reading risk is R2-M3.
- No architecture finding on changed lines.

## === ADVERSARIAL ANALYSIS (Whittaker) ===

Applied to the changed guard only (the WC-4 exception and path rule). One attack per methodology where one exists.

1. **Zero/Empty Attack.** No attack on changed lines beyond the prior M4 (unattended run with no output flag), which was not touched and stays a Medium follow-up from round 1.
2. **Divergence Attack.** Invariant at **WC-4 exception (SPEC:62)** fails when **a stop could be read as either "before any other output exists" or "before the contract's directory exists"**. Concrete attack: `/sc:tdd "auth" --unattended --output docs/x.md` (SPEC:200) with a bare topic. State before: `docs/` exists but the command has written nothing. WC-4 says write on "stops before any other output exists"; the exception says write none if the contract's directory does not exist. For a command given a not-yet-created `--output <dir>`, one implementer creates the directory and writes `status: blocked`, another applies the exception and sends the question only in the body; AC-2.2 expects a contract with a non-empty `blocked_question` (SPEC:200). Graded R2-M3 (Medium): the text allows both readings and the exception's examples name only workflow (SPEC:92).
3. **Sentinel Collision Attack.** The changed text adds no sentinel. Prior M3 and N3 are untouched.
4. **Sequence Attack.** The change adds no ordering. Prior M5 (stale contract in a reused directory) is untouched, and the workflow package is fresh each run (SPEC:92), so the changed row is not affected.
5. **Accumulation Attack.** Nothing accumulates in the changed lines.

R2-M3 (Medium, Whittaker): restate once that the exception applies to a directory the command itself would create only after the point of the STOP and that the coordinator passed no path for (workflow); everywhere else a coordinator-passed directory is created so the contract is written.

## Guard Condition Boundary Table (changed guards only)

In a re-review the table covers guards on changed lines only. The changed guard is the WC-4 path rule and its pre-creation exception (SPEC:62, SPEC:92). Nygard built it, Whittaker attacked it; Crispin was not seated (testing focus not requested) and completeness was checked by Nygard.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-4 path rule | SPEC:62 | Zero/Empty | row names no path and brief has no output directory | default path undefined | unspecified here (prior M4, unchanged) | GAP, Medium (M4) |
| WC-4 path rule | SPEC:62, 76 | One/Minimal | directory-valued `--output <dir>`, row silent | default applies | contract at `<dir>/return-contract.yaml` | OK |
| WC-4 path rule | SPEC:62, 83 | Typical | adversarial with `--output <dir>` | row names path | contract at `<dir>/adversarial/return-contract.yaml` | OK |
| WC-4 path rule | SPEC:62, 92 | Legitimate Edge Case | workflow, package created | id command-created | path from `--report-path` | OK, see R2-M2 for the check |
| WC-4 exception | SPEC:62, 92 | Zero/Empty (pre-creation stop) | workflow STOP before package exists | exception applies | no contract; `--outcome failed`, STOP reason in body, no `--report-path` | OK (INV-B:272, CAPS:74) |
| WC-4 exception | SPEC:62, 60, 200 | Legitimate Edge Case | `--output <dir>` not yet created, gate resolves blocked | ambiguous | contract or none: both readings allowed | GAP, Medium (R2-M3) |
| WC-4 path rule | SPEC:62 | Sentinel Value Match | `--output <file>` (tdd, init-lite) | undefined | unspecified (prior M1, unchanged) | GAP, Medium (M1) |
| WC-4 path rule | SPEC:62 | Maximum/Overflow | n/a: a path, no capacity | n/a | n/a | left out: no capacity |

Every cell is populated, every changed guard enumerated, the omitted class has its reason (FR-10 satisfied). Both GAP rows that are new on changed lines are Medium by the grading check; the unchanged-line rows are carried from round 1, not re-graded.

## Quantity Flow Diagram

No multi-stage count pipeline changed. The 10 / 27 / 6 split and phase totals sit in lines the diff did not touch (SPEC:76 changed only the definition of "Contract"; the 43-command sentence is identical to BASE:76). No dimensional mismatch; FR-19 does not apply.

## Coverage

scoped PASS: changed lines + prior blockers

Read in full: `command.md`, the review-loop prompts file, README, `round1.md`, `revise1.md`, `lint-2.md`, the diff of the six hunks, and the candidate lines 54-102 and 170-201 around them. Checked in the workspace: INV-B:272 and CAPS:74 (quotes confirm the pre-creation and placeholder rules), INV-A:35 and INV-A:60 (adversarial contract location), the `grep -nF` self-check above, and the three file hashes. Prior Medium findings M1-M10 and minor notes N1-N5 (R1:160-181) were not re-reviewed and stay as follow-up candidates; none sits on a changed line except that M3, M4 and M1 relate to the same rule (SPEC:62) as noted in the guard table.

UNVERIFIED (cited by the spec, not present in this workspace, not checked): every `cmd/...`, `sk/...`, `src/superclaude/...`, `tests/...`, `pyproject.toml`, `CLAUDE.md:N` citation, including `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41` (known here only via INV-B:272); `.dev/evals/...` and `.dev/codegraph-migration/...` citations; the spec's own claims at SPEC:11 and SPEC:285 about re-reads and an independent citation check. The revise note that `rf-qa.md` was not consulted for this check is recorded above. Not covered: testing and compliance focus areas (not requested); whole-document assurance (needs a separate, labelled first review); live behavior of any command.

## Follow-up candidates (Medium and minor; none blocks, none enters the Reviser brief)

New in this round (Medium):

- **R2-M1.** Section 2.3 (SPEC:73) still ties "the output directory" to "report path known before dispatch (WC-4)"; WC-4 (SPEC:62) no longer says that and workflow takes no output directory (SPEC:92). Reword 2.3 to "the output directory where the command takes one".
- **R2-M2.** Step 3 pass condition (SPEC:182) is self-referential for workflow (path from `--report-path`, SPEC:62). Name the workflow path pattern, or have step 4 locate the package by listing `.dev/tasks/to-do/`.
- **R2-M3.** WC-4 exception wording (SPEC:62) can be read to cover a coordinator-passed `--output <dir>` that does not yet exist, against AC-2.2 (SPEC:200). Say it applies only where the directory is command-created and was not in the brief.

Carried from round 1, unchanged and not re-graded: M1 to M10 (R1:164-173). N1 to N5 (R1:177-181) are minor notes.

Issue question: the session that ran the review asks the user once per loop whether to open an issue for the follow-up candidates and creates none without an answer. This run had no user to ask, so no issue was created and the list is only recorded; the coordinator carries the question.

## Reviser brief

None. No blocking finding is open, so no revision is requested and no fix cycle is spent. If the coordinator revises anyway, only text a blocking finding names may change, and no Medium finding (R2-M1 to R2-M3, M1 to M10) or minor note (N1 to N5) is a mandate to edit, including through "apply all findings".

verdict: PASS
