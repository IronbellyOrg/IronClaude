review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md (first review)

- command: /sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate sha256: 5c2917118a22814ab0c7a7bbdc9726f06dce161ded89ac5b03740fd58e13abc3
- baseline: not given (full first review; `--re-review` not used)
- reviewer model used: claude-sonnet-5-5
- label: whole-document audit of the final spec, a first review of the whole document
- brief clauses overridden: none
- coverage: all 285 lines read, plus `.dev/orca-command-refactor/README.md` and the three files under `inventory/`. Citation counts and phase assignments were recomputed. Only inventory and README citations could be checked against files in the workspace. Every citation to `src/`, `CLAUDE.md`, `EVIDENCE.md`, `orca-data.json`, `pyproject.toml` or Orca guide output that is not quoted in an inventory is UNVERIFIED here. This applies to the spec's own `cmd/` and `sk/` citations, and I did not re-check the 11 locations it says it re-read (spec line 11).

## Prior findings table
First review: no prior report, so there are no prior findings.

## Summary
The decision (Orca on top, commands stay units of work) is well argued. Its evidence gaps are stated openly (spec lines 41-45). The count split is internally consistent: 43 = 10 + 27 + 6, and per-phase counts add up (P1 9 + 4 fixes, P2 11 + 4, P3 4, P4 3; brainstorm and init-lite get no phase). Two blocking defects break the requirement-to-acceptance chain for the report contract (WC-4). Several Medium gaps remain.

## Expert panel (review order: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower)

Panel notes by expert, mapped to the findings below:
- Wiegers: WC-4 is the load-bearing requirement and is not allocated to all commands (B-1, B-2). Initial value, range and invariant of the `status` field are only partly specified (M-3).
- Adzic: examples exist (D1 command line, AC-2.2 bare-topic run); the retry scenario has none (M-1).
- Cockburn: primary actor and goal are clear (coordinator, worker; section 2.3). The person's role at a blocked report is specified for implement only.
- Fowler: separation is clean (shared contract file, per-command sections, SA-2 forbids Orca calls). The leak is the P0 Orca section in core versus AC-C1 (M-4).
- Nygard: stale or partial report files on crash and retry (M-1, M-2).
- Whittaker: attacks recorded in the guard table below.
- Newman: versioning of the contract file is unspecified (note N-2).
- Hohpe: message pattern (`ask`, `check`, `worker_done` once) is specified well. Delivery ordering of `check` before `worker_done` is covered by WC-12.
- Crispin: acceptance checks are strong (7.2). Defects are in AC-1.1/AC-2.2/AC-2.3 coverage (B-1, B-2) and AC-C5 (M-5).
- Gregory: D1-D5 are framed for the user with recommendations. D1 and D4 reach phases the spec says need no decision (M-6).
- Hightower: executable-name and standalone concerns are handled (R2, R4, SA-2).

=== REQUIREMENTS ANALYSIS ===

### B-1 [MAJOR, blocking] WC-4 contract is required for every unattended outcome, but no phase adds it to six "ready" commands
- Expert: Wiegers, Crispin.
- Stated text: WC-4 requires `<output-dir>/return-contract.yaml` "written on success, failure, blocked and partial outcomes" for commands run unattended (spec line 62). The 3.1 intro says the worker reports the named file "until Phase 1 adds the contract" (line 79). The P1 scope lists only "fixes to adversarial, cleanup-audit, index-repo, workflow" (line 159). The P1 fixes in the 3.1 rows are a contract filename for adversarial, a report name for cleanup-audit, an output location for index-repo and a pre-creation contract for workflow (lines 83, 85, 86, 92). The rows for init-lite and brainstorm say "None" (lines 84, 87). The tdd, troubleshoot and release-split rows change only gate resolution (P2) and name no contract (lines 89-91).
- Grading sentence: an implementer who follows the stated text as written builds P1 and P2 with no `return-contract.yaml` for troubleshoot, tdd, release-split, init-lite, cleanup-audit and index-repo (their listed fixes only name or locate an existing report). That is wrong because AC-2.3 (line 201) and 7.2 step 4 (line 183) require a parseable contract with `status` for each P2 command's happy path, and `test -s` plus the YAML assertion would fail.
- Recommendation: either state which phase adds the contract to each of those six commands (and name the commands in the AC-1.1 and AC-2.1 tests), or narrow WC-4 for "ready" commands to "existing named report file" and drop the YAML assertion for them.
- Priority: High. Quality impact: acceptance of P1 and P2 cannot pass as written.

### B-2 [MAJOR, blocking] Workflow's success contract location contradicts the WC-4 path that AC-1.2 checks
- Expert: Wiegers, Fowler.
- Stated text: WC-4 defines the report path as `<output-dir>/return-contract.yaml`, with `--report-dir` for workflow, and says it is "known before dispatch" (line 62). The workflow row says the report today is `.dev/tasks/to-do/<id>/return-contract.yaml` and the fix is to write the contract for pre-creation STOPs "too, into `--report-dir`" (line 92). AC-1.2 requires, for workflow, that the `worker_done` report path "is the WC-4 contract path" (lines 182, 196).
- Grading sentence: an implementer who follows the stated text as written keeps the success contract in the generated package directory and adds a second contract only for pre-creation STOPs in `--report-dir`. That is wrong because the path of a successful run is `<id>`-dependent, cannot be known before dispatch, and differs from the WC-4 path AC-1.2 tests, so AC-1.2 step 3 fails for every successful workflow run.
- Recommendation: state one rule for workflow: the contract is written to `<report-dir>/return-contract.yaml` on every outcome, and carries `plan_path` (or copy it there).
- Priority: High.

=== ARCHITECTURE ANALYSIS ===

## Medium findings (warnings; follow-up candidates, not blocking)

### M-1 Retry and "fresh dir" is ambiguous against a fixed brief output directory
- WC-6 says a retry "must not corrupt the first attempt's output" and that a command without resume writes each run into "a fresh output directory" (line 64). WC-4 and section 2.3 have the coordinator fix `<output-dir>` before dispatch (lines 62, 73). About twenty rows say "fresh dir" (for example lines 99, 101, 106). The text does not say whether the command creates a subdirectory (which breaks the known contract path) or the coordinator changes the directory on `--retry-of`. Two readings are allowed. It is Medium because the implementer picks one of them.
- A retry reusing the same directory could also leave the first attempt's `status: succeeded` file in place if the retry dies before writing, and WC-4 covers no crash (see M-2).

### M-2 No stale-report or crash rule
- WC-4 requires a contract on every outcome "including stops before any other output exists" (line 62) but does not say what the coordinator does when the worker session dies mid-command. WC-5 maps "no report exists" to failed (line 63), but a leftover file from an earlier attempt looks like a report. A requirement the document never states.

### M-3 Edge cases in the `status` and outcome mapping are not specified
- WC-5 maps `failed`/`blocked`/no-report to `--outcome failed` and the rest to succeeded (line 63). It does not say what happens when the file exists but is empty, unparseable, or has a `status` outside the four values. Step 4 of 7.2 only checks this in testing (line 183). `partial` mapping to succeeded is a recorded decision (line 263), but that decision lets a coordinator treat partial output as done.

### M-4 AC-C1 versus the P0 deliverables and SA-2
- AC-C1 greps `src/superclaude/core` for `orca(-ide)? (orchestration|worktree|terminal|agent)` with an exemption only for `skills/ccsession-tag/` (line 172). P0 adds `core/WORKER-CONTRACT.md` and an Orca section in `core/HOW-WE-WORK.md` (lines 158, 150). SA-2 allows an Orca mention "inside the contract file" as a question-channel example (line 147). If any of those texts spells a command form, AC-C1 fails and the phase cannot pass. Add the two files to the exemption or restrict the regex to `commands`, `skills` and `agents`.

### M-5 AC-C5 conflicts with adding flags to existing lines
- AC-C5 requires no deleted lines (`^-[^-]`) in command diffs without a named defect fix (line 176). Adding `--output` or `--unattended` to a Usage line or `argument-hint` (for example analyze, line 99) rewrites an existing line, so the check fails. SA-4 calls new flags additive (line 149). State that Usage-line and frontmatter flag additions are exempt, or require the flag to be added on a new line.

### M-6 "Phases 1-3 need no user decision" versus D1 and D4
- Line 154 and line 225 say phases 0-3 proceed on recommendations. D4 affects auggie-review `--post-pr` and task `commit`/`push` (line 244), both P2 (lines 100, 121), and WC-9 requires an "explicit flag" that those rows never define (task, line 121: "refused unless authorized"; post-release, line 113). The mechanism for authorizing an outward action is unspecified.

### M-7 Brief template versus commands with no `--unattended`
- Section 2.3 says every brief carries the command line "including `--unattended`" (line 73) and D1 says the coordinator writes it into every worker's command line (line 228). Brainstorm and init-lite get no change in any phase (lines 84, 87), and reflect, release-split, tdd, troubleshoot and the P0 smoke commands accept it only from P1 or P2 (lines 88-91, 158). Section 3.1's "Brief must pass" column omits `--unattended`. What an unrecognised flag does is not stated.

### M-8 WC-10 versus AC-4.3
- WC-10 requires splitting only waits longer than 5 minutes into waits of at most 4 minutes (line 68). AC-4.3 fails any single tool call over 240 s (line 210). A 270 s call passes WC-10 and fails AC-4.3.

### M-9 Citation-check claims conflict
- Line 11 says every section-3 line other than 11 re-read locations is "carried from the inventories without a second read". Item 14 (line 285) says an evidence-validator re-read about 340 citations in this spec. Neither is checkable here. State one account.

### M-10 Reflect and tasklist headless path rests on an unread rule
- The reflect row makes `--remediate` "follow the existing headless auto-accept rule" under `--unattended` (line 88) and the tasklist row passes `--unattended` into each reflect (line 122). What auto-accept does (it hands off to a remediation workflow) is cited only to `sk/sc-reflect-protocol/refs/remediation-handoff.md:228,239-247`, which cannot be checked here (UNVERIFIED). The claim that tasklist's fan-out stays "inside Claude Code's nesting limit" cites only the generic nesting statement at `INV-A:14`; reflect Tier 2 adds reviewers below the Stage 10.5 subagents. UNVERIFIED depth count.

### M-11 Default output paths collide when two workers start in the same second
- WC-11 relies on "a timestamp or the slug the coordinator passes" (line 69). Timestamp granularity is not given, and cleanup-audit's output directory is fixed (line 85), which the spec notes only as "one audit per worktree".

## Minor notes
- N-1: Spec line 132 quotes `cmd/agent.md` as keeping "the user out of the loop". `INV-A:90` says the command "owns the user loop". The quote is UNVERIFIED and may be misworded.
- N-2: The contract file has no version field and no rule for evolving the status vocabulary (Newman).
- N-3: A `--unattended` token inside quoted topic text (for example `/sc:troubleshoot "login --unattended"`) is not covered; the spec-panel command defines a standalone-token rule, this spec does not.
- N-4: `/sc:load` is counted among the 27 commands "needing a change" but its only change is a usage line (lines 76, 112). Counts stay correct.
- N-5: Line 5 and the README (line 8) give an absolute worktree path outside this sandbox; not checkable here.

## Guard Condition Boundary Table (Nygard, Crispin, Whittaker)
Input classes not listed for a guard cannot occur for it (reason in the Notes column).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| outcome mapping on report `status` | WC-5, line 63 | Zero/Empty | no file, empty file, `status` missing | no report: failed | "no report exists" gives failed; empty or unparseable file unspecified | GAP (M-3) |
| outcome mapping | WC-5, line 63 | Typical | `succeeded` or `partial` | succeeded | succeeded | OK |
| outcome mapping | WC-5, line 63 | Sentinel Value Match | `blocked`/`failed` | failed | failed | OK |
| outcome mapping | WC-5, line 63 | Legitimate Edge Case | stale file from earlier attempt | n/a | unspecified | GAP (M-2) |
| contract written on every outcome | WC-4, line 62 | Zero/Empty | stop before any output | true | contract still written | OK |
| contract written on every outcome | WC-4, line 62 | Legitimate Edge Case | worker session dies | n/a | unspecified | GAP (M-2) |
| contract required of command | WC-4 vs lines 84-91 | Typical | troubleshoot, tdd, release-split, init-lite, cleanup-audit, index-repo happy path | required | no phase adds it | GAP (B-1) |
| contract path `<output-dir>` | WC-4 vs line 92 | Legitimate Edge Case | workflow success (`<id>` unknown) | n/a | success contract in package dir, not report-dir | GAP (B-2) |
| heartbeat wait split | WC-10, line 68 | Typical | single call 270 s | not > 5 min: true | no split; AC-4.3 fails it | GAP (M-8) |
| heartbeat wait split | WC-10, line 68 | Maximum/Overflow | call > 5 min | split to <= 4 min | specified | OK |
| heartbeat wait split | WC-10, line 68 | One/Minimal | call exactly 5 min | boundary of "longer than" | not split | OK (the cadence allows a heartbeat between calls) |
| task confidence gate | line 121 | Typical | 0.69 | true | blocked | OK |
| task confidence gate | line 121 | Sentinel Value Match | exactly 0.70 | false | not stated in this spec (inherited from the command) | GAP (minor: the 0.70 boundary is inherited; UNVERIFIED) |
| same-second output path | WC-11, line 69 | Zero/Empty | two workers, no slug passed | collision | unspecified granularity | GAP (M-11) |
| `--unattended` flag recognition | D1, line 228 | Sentinel Value Match | flag inside quoted text | n/a | unspecified | GAP (N-3) |
| `--unattended` passed to command without the mode | line 73 vs 84, 87 | Typical | brainstorm, init-lite | n/a | unspecified | GAP (M-7) |
| retry directory | WC-6, line 64 | Typical | `--retry-of` with same brief dir | n/a | ambiguous | GAP (M-1) |
| ask timeout | WC-3, line 61 | Maximum/Overflow | timeout | resume same message ID | specified | OK |
| circuit breaker | line 263, `CAPS:80` | Maximum/Overflow | 3 consecutive failures | opens | worker-reported failed does not count (per `CAPS:80`, read in the workspace) | OK |

FR-8/FR-9 grading: none of the GAP rows names a concrete wrong outcome beyond B-1 and B-2 (which are graded above) or a security, data-loss or safety-boundary risk; the rest are Medium. Table complete (FR-10): every guard enumerated; classes left out cannot occur because these guards take no numeric input other than the ones shown.

## Whittaker attacks (five methodologies)
- Zero/Empty: empty contract file or missing `status` (M-3).
- Divergence: workflow success versus pre-creation paths (B-2); "fresh dir" per retry (M-1).
- Sentinel Collision: the literal `--unattended` token in user text (N-3); `status: partial` mapped to succeeded.
- Sequence: contract left over from attempt 1 read after attempt 2 crashes (M-2); `check` then `worker_done` is covered by WC-12.
- Accumulation: same-second default paths (M-11); phases add flags in P1/P2 that earlier P0 smoke runs assume (M-7).

## Pipeline Dimensional Analysis
The only multi-stage flow whose counts could diverge is the command inventory to phase assignment. Counts conserved: 21 + 22 = 43; 10 + 27 + 6 = 43; phase totals recomputed in the Summary. Brainstorm and init-lite have no phase (still ready). No count mismatch.

Quantity flow: [43 commands] --> [6 coordinator-only] --> [37 workers] --> [10 ready (2 never touched) + 27 changed].

## Evidence status
- Checkable and found as cited: `INV-A:3,14,62,90,95,97,106,113,118,120`; `INV-B:3,31,36,37,47,65,105,112,272,285-287,289,292,294,296,301,311,320,323`; `CAPS:44-47,52,58,64,66,68,72,73,76,79,80,97-99,103,107,115,116,129,130,145,147-151,155,158-161,177-188`; README lines 6, 8, 11-17, 30, 31.
- Inventory B verdicts for troubleshoot, release-split, tdd, reflect and workflow are "ready" (`INV-B:36,37,47,49,52`); the spec adds P2 gate changes on top. That is a reasoned upgrade, not a contradiction.
- Everything cited to `src/`, `CLAUDE.md`, `EVIDENCE.md`, `pyproject.toml` and `Makefile` that the inventories do not quote: UNVERIFIED.

## Follow-up candidates (Medium and minor; not blocking)
M-1 to M-11 and N-1 to N-5 above. The session that ran this review would ask the user once whether to open an issue for them; this run is a labelled audit with a single-line reply, so no question was asked and no issue was created.

## Reviser brief
Blocking finding ids: B-1, B-2. Only these. Rules for the reviser: revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id; leave minor and Medium findings alone; return the candidate once and do not award yourself a PASS.

verdict: FAIL
