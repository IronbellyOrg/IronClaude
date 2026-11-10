review: 1 of 3

# Spec-panel critique, round 1

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (first review, no `--re-review`, no `--baseline`)
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines), sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Baseline sha256: none given (first review)
- Reviewer model actually used: Sonnet 5.5 (`claude-sonnet-5-5`)
- Prompt followed: FIRST-REVIEW in `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full). This is one of the two independent first reviews; the MERGE rule is the coordinator's.
- Panel (focus requirements: Wiegers lead, Adzic, Cockburn; focus architecture: Fowler lead, Newman, Hohpe, Nygard; Whittaker active in every panel, Crispin for guard-table completeness).

## Coverage

Read in full: README (`.dev/orca-command-refactor/README.md:1-38`), the candidate (lines 1-285), `review/lint-1.md`. Checked against the evidence inventories: `inventory/commands-a.md` (cited lines 3, 14, 35-39, 55, 60-66, 76-98, 106, 113, 118, 120), `inventory/commands-b.md` (lines 31-52, 65, 105, 112, 199-205, 272, 285-301, 311, 320, 323), `inventory/orca-capabilities.md` (lines 44-53, 58-80, 84-92, 97-103, 107-116, 126-139, 145-162, 178-188). I recounted the verdict split (10 ready, 27 needing change, 6 coordinator-only; 21 + 22 = 43) and the phase membership lists against section 3 rows; they match (candidate lines 76, 78-125, 128-137, 159-162).

Not covered: every `src/...`, `CLAUDE.md:N`, `Makefile`, `pyproject.toml`, `tests/` and `~/.claude/...` citation in the candidate. The workspace holds only `.dev/orca-command-refactor/`, so those are UNVERIFIED here (affected: candidate lines 11, 25, 34, 52, 83-125 per-command source lines, 146, 150, 164, 183). The candidate's own claim of an independent check of about 340 citations (line 285) is also UNVERIFIED here. The two inventories' own claims of citation checks (`commands-a.md:106`, `commands-b.md:320`) are carried, not re-done.

## Lint evidence

`review/lint-1.md:1-5`: header sha256 equals the candidate's hash above; "Checks: REF. Findings: 0." There is no lint id to confirm or dismiss. A clean lint is no evidence on the findings below, since REF checks references and not requirement consistency.

## Grading summary

| Id | Severity | Grade | Title |
|----|----------|-------|-------|
| F-1 | MAJOR | blocking | Acceptance check AC-1.1 contradicts the rows for load, brainstorm and init-lite |
| F-2 | MAJOR | blocking | WC-4's contract location cannot be satisfied for file-valued `--output` commands, and AC-2.2 / AC-1.4 cannot pass |
| M-1 to M-8 | MAJOR/MINOR | Medium | warnings, see `follow-up candidates` |

## === REQUIREMENTS ANALYSIS ===

### F-1 [MAJOR, blocking] Acceptance check AC-1.1 requires a contract section on commands that section 3 says get none

Experts: Wiegers (lead, traceability), Adzic (the checkable example fails), Crispin (acceptance test completeness).

Stated texts that contradict:
- Candidate line 195, AC-1.1: "the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
- Candidate line 112, `/sc:load` row: report column "none (see note)", "Other required change": "none: use it as a step inside another worker's brief, not as its own Task", phase "P1 (usage line only)". Line 159 repeats it ("load (usage line only)").
- Candidate line 265, Decisions: "a report file would be an unrequested addition. Only its usage-line defect is fixed."
- Candidate line 79 (3.1 intro): "The only command changes are the small fixes in the last column"; the `brainstorm` row (line 84) and `init-lite` row (line 87) say "None" in that column. Line 76 says only "changed" commands gain the section, and line 159 gives the P1 command list without brainstorm or init-lite.

Grading sentence: An implementer who follows line 112, line 265 and line 79 as written changes `/sc:load` only in its usage line and leaves `/sc:brainstorm` and `/sc:init-lite` untouched, and builds a Phase 1 whose own acceptance test (AC-1.1, line 195) fails on those three commands, because AC-1.1 requires every command in 3.1-3.2 to carry the section. The implementer who instead satisfies AC-1.1 adds a contract section to `/sc:load`, which line 265 rejects. The text itself offers no way to pass both. Two stated texts contradict, so this is blocking.

Attack (Whittaker, FR-2.2 Divergence): the AC-1.1 quantifier "every command in sections 3.1-3.2" and the per-row "change" column partition the 37 commands differently; the boundary case is the set difference (load, brainstorm, init-lite, plus any other row with "None").

Recommendation: narrow AC-1.1 to the commands whose rows add a section, or have the rows for these three say they gain the section. Prefer narrowing the test (smaller diff).

### F-2 [MAJOR, blocking] WC-4 defines the report path from a coordinator-passed directory, yet several commands take a file, and two acceptance criteria depend on that path

Experts: Cockburn (the coordinator's goal: open the contract), Wiegers (testable and unambiguous), Hohpe (the interface between command and coordinator), Whittaker (FR-2.3 Sentinel Collision: one flag name carries two meanings).

Stated texts:
- Candidate line 62, WC-4: the command writes `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)". Line 73 (2.3): the brief states "the output directory, so the report path is known before dispatch (WC-4)". Line 182 (7.2 step 3): "its report path is the WC-4 contract path".
- Candidate line 90, `tdd` row: brief must pass "`--output <file>`"; line 87, `init-lite`: "`--output <file>`"; line 120, `spec-panel`: "add `--output`" (the spec-panel `--output` is a file in the same row's evidence at `cmd/spec-panel.md`; UNVERIFIED here); line 200, AC-2.2: "`/sc:tdd "auth" --unattended --output <file>`" must yield a contract with `status: blocked` and a non-empty `blocked_question`.
- Candidate lines 92 and 198, `workflow` row and AC-1.4: the contract lives at `.dev/tasks/to-do/<id>/return-contract.yaml` and must now also be written "for pre-creation STOPs", where no `<id>` exists yet.

Grading sentence: An implementer who follows WC-4 as written builds the tdd contract at `<file>/return-contract.yaml` (the passed `--output` value is the TDD file, not a directory), and that path cannot exist as a directory entry beside a file of the same name; AC-2.2 and the 7.2 step 3 and step 4 checks then cannot locate or open the contract, so they cannot pass. For `workflow` the stated path needs an `<id>` that a pre-creation STOP does not have, so AC-1.4 has no defined location to check. A stated text that an acceptance criterion cannot pass is blocking.

Recommendation: state one rule for the contract location that covers a file-valued `--output` (for example a sibling file, or a separate `--report-dir` as the already-defined mechanism in other contract writers would suggest) and for workflow's pre-creation case; or have the brief always pass a dedicated directory flag for the contract.

## === ARCHITECTURE ANALYSIS ===

Positive points (no action): the split of Orca on top and commands as units is argued from evidence with stated gaps (candidate lines 13-45, supported by `orca-capabilities.md:97-103,147-150,155-161`); the verdict counts reconcile with both inventories; the rejected alternative R1-R5 is traced to `orca-capabilities.md` lines that exist as cited (lines 97-101, 145-150). Fowler and Newman raise no boundary objection to keeping Orca calls out of commands (SA-2, WC-8). Nygard: heartbeat and blocked-state handling follow `orca-capabilities.md:52,64,129-130`.

The architecture findings that matter are the Medium items below (M-1, M-2, M-3, M-6, M-7).

## Guard Condition Boundary Table

Guards found in the candidate: G1 the WC-10 wait threshold, G2 the WC-5 outcome map, G3 the WC-4 report presence, G4 WC-1 readiness fallback, G5 the WC-12 `consumer_fenced` branch. The class "Sentinel Value Match" is left out for G2 to G5 because none of them compares against a sentinel; "Maximum/Overflow" is left out for G3, G4, G5 because they have no numeric capacity.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G1 wait split | line 68 (WC-10), line 210 (AC-4.3) | Zero/Empty | wait of 0 s | no split needed | not stated, and cannot occur for a poll that sleeps at least `--poll-interval` (line 68) | OK (omitted as non-occurring) |
| G1 wait split | line 68 | One/Minimal | 1 s | no split | single call allowed | OK |
| G1 wait split | line 68 | Typical | 3 min | no split | allowed | OK |
| G1 wait split | line 68, line 210 | Legitimate Edge Case | 4.5 min single call | WC-10 "longer than 5 minutes": false, no split required; AC-4.3 "no single tool call exceeds 240 s": violated | WC-10 allows it, AC-4.3 rejects it, the row at line 114 says "stays under 4 minutes" | GAP |
| G1 wait split | line 68 | Maximum/Overflow | exactly 5 min, or 40 min | "longer than 5 minutes": exactly 5 min false | exactly 5 min neither requires a split nor meets "at most 4 minutes" | GAP |
| G2 outcome map | line 63 (WC-5) | Zero/Empty | contract file exists, 0 bytes | not covered ("no report exists" is the only absent case) | not specified | GAP |
| G2 outcome map | line 63 | One/Minimal | `status: partial` | true for "succeeded" | `--outcome succeeded`, body names `partial` | OK |
| G2 outcome map | line 63 | Typical | `status: failed` or `blocked` | true | `--outcome failed` | OK |
| G2 outcome map | line 63, line 183 | Legitimate Edge Case | existing command contract carries another vocabulary (e.g. a status value outside the four) | unknown | AC-1.2 step 4 asserts membership in the four values (line 183); how an existing contract's own value maps is not stated | GAP |
| G3 report present | line 62 (WC-4) | Zero/Empty | `--unattended` given with no `--output` | `<output-dir>` undefined | not specified; WC-4 says the contract is written "on every outcome" | GAP |
| G3 report present | line 62 | Typical | `--output <dir>` passed | true | contract in `<dir>` | OK |
| G3 report present | line 62, 90 | Legitimate Edge Case | `--output <file>` (tdd, init-lite) | `<output-dir>` is a file | see F-2 | GAP (blocking via F-2) |
| G4 readiness fallback | line 59 (WC-1) | Typical | fallback 30 s | inside 60 s | passes (evidence line 59, `EVIDENCE.md:45`) | OK |
| G4 readiness fallback | line 59 | Legitimate Edge Case | fallback 45 s to 60 s | "well inside" is not a number | not specified; the same line cites failure "above about 45 s" | GAP |
| G5 consumer_fenced | line 70 (WC-12) | Typical | `check` returns `consumer_fenced` | true | stop, send no `worker_done` | OK |
| G5 consumer_fenced | line 70 | Legitimate Edge Case | fenced after the report file was written | true | whether the contract stays as written, and whether the replacement worker may overwrite it, not stated | GAP (Medium; see M-7) |

GAP rows and grading (FR-8, FR-9): the F-2 row is blocking through F-2. The remaining GAP rows each describe a requirement the document never states, with no concrete wrong outcome that holds without a guess, so they are Medium and appear as M-2, M-5, M-6 and M-7 below. FR-10: the table is complete for the guards enumerated; the enumeration covers guards the candidate states as numeric or boolean thresholds.

Not triggered: Pipeline Dimensional Analysis and the Quantity Flow Diagram (the candidate describes no multi-stage data flow whose stage counts diverge; the phase list is a plan, not a data pipeline). Correctness focus is not active, so no State Variable Registry is required.

## Follow-up candidates (Medium and minor; none fails the review or goes to the reviser)

Medium (warnings):

- **M-1** `AC-C1` versus content that P0 itself adds. Candidate line 172 requires the grep over `src/superclaude/core` to print nothing (excluding only `ccsession-tag`), while line 158 (P0) adds `WORKER-CONTRACT.md` and an Orca section in `HOW-WE-WORK.md`, both under core, and line 147 (SA-2) allows an Orca mention "as an example of a caller's question channel inside the contract file". If that example is written as `orca orchestration ask` (the form `orca-capabilities.md:58` quotes), AC-C1 fails on P0. Whether it fails depends on the wording the implementer picks. Narrow either the grep path or SA-2.
- **M-2** `--unattended` without an output flag (G3 row). No text says what a command does; WC-4 promises a contract on every outcome. A refusal or a default directory would close it.
- **M-3** Phase membership versus the per-row phase column. Line 159 (P1) adds the flag and section to every command in 3.1 and 3.2, while the Phase column of section 3 rows places auggie-review, cleanup and others in P2 and `implement`, `post-release`, `pr-submit` in P4 (lines 100, 109, 113, 114). Line 154 says "Phases 1-3 need no user decision", yet D4 (line 244) lists `auggie-review --post-pr` and `task commit/push`, both changed in P2, and D3(a) (line 240) says "no pr-submit changes in Phase 4" while P1 would already give pr-submit an unattended section. Pick one source for what each phase edits.
- **M-4** `WC-6` "fresh output directory" (line 64) against the fixed contract path of WC-4 (line 62) and the same-brief retry (line 73): a retry given the same brief reuses the same directory. Say that the coordinator passes a new directory on each retry.
- **M-5** G1 wait threshold: WC-10 says "longer than 5 minutes" must split into "at most 4 minutes", AC-4.3 (line 210) and the pr-submit row (line 114) use 4 minutes as the limit for every call. Use 4 minutes in WC-10.
- **M-6** Evidence misuse: `.dev/orca-command-refactor/README.md:31` ("No git commits, pushes, PRs or GitHub comments") binds this planning run's workers (README lines 29-31, "Rules for every worker"). The candidate cites it as support for WC-9 (line 67) and for `/sc:git` needing the user's authorization in this repo (line 133). The git row stands on `cmd/git.md` (UNVERIFIED here); WC-9 stands on `cmd/auggie-review.md:51-54` (UNVERIFIED here). Drop the README citation from both.
- **M-7** G5 and G2 gaps: contract state after `consumer_fenced` and for an empty or foreign-vocabulary contract are not specified.
- **M-8** 7.2 step 2 (line 181) passes only if `observation.agentWait` is never non-null, but WC-3 (line 61) lets a worker block in `ask`, and `orca-capabilities.md:52,129` call a waiting worker "healthy"; whether an `ask` wait sets `agentWait` is not stated (`orca-capabilities.md:129` describes a prompt "only a human can answer"). A legitimate WC-3 run could fail the check. State that the check covers runs that take the blocked-and-stop path.

Minor notes:

- N-1 Line 23 (E3) cites `invocation_method: "skill-direct"` as support that the route "has worked before", and line 43 (1.4) says the same run "proves the nested route, not the direct route". Align the wording of E3 with 1.4. `commands-a.md:10` (adversarial row) calls the same record "Proven as a direct Orca-worker skill call".
- N-2 Line 114 (pr-submit row) says no wait splitting is needed; line 241 (D3 (b)) says to "Apply the section 3 row (wait splitting, ...)".
- N-3 Line 148 (SA-3) adds a second trigger for the contract ("or when the caller passes the new output flag") that WC-4 (line 62, "In unattended mode") does not have.
- N-4 Line 261 refers to "ladder rung 2", which the document does not define.
- N-5 Line 209 (AC-4.2) runs post-release "with no authorization flags" and expects a contract listing skipped steps, while the post-release row (line 113) says a missing explicit pre-tag choice resolves as blocked; the expected result then is `blocked`, not a run with skipped steps.
- N-6 Section 4 (line 128) says the six coordinator-only commands "get no `--unattended` mode", but no text says what happens when a brief passes the flag to one of them.
- N-7 Line 59 (WC-1) "well inside the readiness limit": give a number (the cited evidence at line 59 shows 30 s passes and about 45 s fails).

Per the command's Review Loop, the session that ran this review asks the user once per loop whether to open an issue for the Medium and minor list; none is created without an answer.

## Reviser brief

Blocking finding ids: F-1, F-2. (Pending the coordinator's MERGE and VERIFY steps.)

Rules for the reviser (restated from the command's Review Loop, bullet 6; the reviser reads this report, not the command):
- Revise only text a blocking finding names. Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings (M-1 to M-8, N-1 to N-7) alone; "apply all findings" is not an instruction here.
- F-1 names: candidate lines 195, 112, 159, 265, 79, 84, 87. F-2 names: candidate lines 62, 73, 87, 90, 92, 182, 198, 200.

No brief clause was overridden: no clause was supplied beyond the values and the lint file.

verdict: FAIL
