review: 1 of 3

# Audit: orca-worker-contract-spec.md (spec-panel, critique mode, first review, whole document)

- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 286 lines, sha256 `de92cfbd1e91f7c9b127746790c558a078c2ca7c0cfa873d862dfcbd0dab1bb9`
- Baseline: none given. Prior findings: none given. This is a labelled whole-document first review (`.dev/orca-command-refactor/README.md` shared context read first).
- Reviewer model actually used: claude-sonnet-5-5
- Command: `/sc:spec-panel --mode critique --focus requirements,architecture`. Focus panel: Wiegers (lead), Adzic, Cockburn, Fowler (lead), Newman, Hohpe, Nygard, plus Whittaker (always active) and Crispin (boundary-table completeness), in the fixed review order of `command.md:101-113`.
- Prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full). Grading follows `command.md:259`.
- Improve step: not run. The brief says to edit nothing else, and the spec must not be changed without consent (`command.md:477-479`). No revised specification is written.
- Follow-up issue question (`command.md:260`): the session that ran this review must ask the user once whether to open an issue for the follow-up candidates. This sandbox run cannot ask, so none was created.

## Coverage

- Read in full: the candidate (all 286 lines), `README.md`, `inventory/commands-a.md` (120 lines), `inventory/commands-b.md` (323 lines), `inventory/orca-capabilities.md` (188 lines), `command.md`, and the review-loop prompts file.
- Checked: every `INV-A:n`, `INV-B:n` and `CAPS:n` citation in sections 1-4, 7 and 9 and the Decisions and UNVERIFIED lists, against the inventory line it names. I found none that cites the wrong line. The row verdict counts (10 / 27 / 6; P1 = 13, P2 = 15, P3 = 4, P4 = 3, no phase = 2) were recounted from the tables.
- UNVERIFIED, because the file is outside the workspace and cannot be checked here: `CLAUDE.md:*` citations, `src/superclaude/cli/install_core.py:*`, `pyproject.toml:38`, `HOW-WE-WORK.md:*`, `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md:*`, `.dev/codegraph-migration/**`, all `cmd/` and `sk/` line cites not echoed in an inventory, and the E5 grep results. The inventories echo the Orca guide text only as quotes (`CAPS:8-21`).
- Correctness focus is not active, so no State Variable Registry is produced. The Guard Condition Boundary Table is produced because the spec has thresholds and gates. The Quantity Flow Diagram is produced because section 3 splits one command count into several consumers.

=== REQUIREMENTS ANALYSIS ===

### B1. CRITICAL (blocking). Phase-0 gate AC-0.4 cannot pass, so no later phase can start
- Expert: Wiegers, Adzic. Priority: High. Quality impact: Completeness 4/10, Testability 3/10.
- Grading sentence: An implementer who follows the stated text as written builds a P0 gate whose step 3 needs a WC-4 `return-contract.yaml` with a `status`, and X is wrong because none of the three smoke commands has one in P0. `/sc:troubleshoot` writes `return-contract.yaml` only with `--caller task-unified` (`inventory/commands-b.md:242`). `/sc:adversarial` has no fixed contract filename until the P1 fix (`spec:83`, `inventory/commands-a.md:60`). `/sc:workflow` writes its contract at `.dev/tasks/to-do/<id>/`, not at a coordinator-passed `<output-dir>` (`spec:92`).
- Text in conflict:
  - AC-0.4 says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1" (`spec:194`).
  - Step 3 of the live check requires "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path" (`spec:182`).
  - The P1 contract does not exist in P0 (`spec:158-159`), and only step 4 is excepted.
  - Section 6 says "Later phases do not start until the earlier phase's checks in section 7 pass" (`spec:154`). AC-0.4 also says "a failure here reopens section 1" (`spec:194`), so a false failure sends the work back to re-open the core decision.
- Recommendation: narrow AC-0.4 to say step 3 for P0 checks only "exactly one `worker_done` with an explicit `--outcome`, and `--report-path` names the command's existing report file", and move the contract-status and contract-path conditions to P1. Rationale: the narrowing deletes text instead of adding a rule, and it keeps the smoke runs able to test the section 1 decision.

### B2. CRITICAL (blocking). AC-1.1 and the P1 scope require work on commands that no phase, or a conditional phase, owns
- Expert: Wiegers (traceability), Fowler. Priority: High. Quality impact: Consistency 3/10, Completeness 4/10.
- Grading sentence: An implementer who follows the stated text as written builds the `## Unattended mode` section and the `--unattended` flag on all 36 commands of sections 3.1-3.2 in Phase 1, and X is wrong because that contradicts at least two other stated texts. The other texts are the per-row phases and "Apply the answers to D2-D4" in P4, and D3 option (a), which says "no pr-submit changes in Phase 4" (`spec:240`).
- Text in conflict:
  - AC-1.1 asserts "every command in sections 3.1-3.2 except `load`" has the section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one (`spec:195`). The P1 scope says "the `--unattended` flag accepted by every command in sections 3.1 and 3.2" (`spec:159`). The section 3 header repeats this (`spec:76`).
  - The P1 Commands column names only 13 commands (`spec:159`). The rest are scheduled for P2 (15), P3 (4) and P4 (3). `brainstorm` and `init-lite` are in no phase, because their small-fix cell says "None" (`spec:84`, `spec:87`).
  - `pr-submit` is scheduled for P4 and sits behind D3 (`spec:114`, `spec:162`). Under D3(a) it becomes coordinator-only, and AC-1.1 would then also forbid its section. Section 6 says phases 1-3 "need no user decision" (`spec:154`).
  - Consequence if P1 is built as AC-1.1 reads: `/sc:auggie-review --unattended` is accepted in P1, but the default PR posting is only turned off in P2 (`spec:100`, `inventory/commands-a.md:78`). A coordinator following section 2.3 would pass `--unattended` and get an unprompted GitHub post. That breaks WC-9 (`spec:67`) and WC-2 (`spec:60`).
- Recommendation: make AC-1.1 phase-scoped (assert the section only for the commands whose phase is the one just completed, using the Phase column), assign `brainstorm` and `init-lite` to P1, and state that a command whose gate conversion is not yet done refuses `--unattended`. Rationale: one assertion keyed to a column that already exists removes the conflict and the interim outward-action risk without adding a mechanism.

#### Quantity Flow Diagram (produced because B2 is a count divergence)
```text
[Inventories: 43 commands] --> [Verdict split] --> 10 ready (3.1) | 27 need change (3.2) | 6 coordinator-only (4)
  3.1 + 3.2 = 37 workers, less load (B-1) = 36 expected by AC-1.1  <-- consumer A: spec:195
  Phase assignment consumer: P1 = 13, P2 = 15, P3 = 4, P4 = 3 = 35 of 37; brainstorm, init-lite unassigned
  P1 consumer B (spec:159 scope text) = 37 accepting the flag  <-- MISMATCH with its own Commands column (13)
```

### Follow-up candidates (Medium, graded under `command.md:259`; none block)

- **M1. Report location is not uniform (MAJOR, graded Medium).** Wiegers. Priority Medium.
  - WC-4 says the contract goes in `<output-dir>`, "known before dispatch" (`spec:62`). The directory flag is named three ways: `--output` / `--output-dir` (`spec:62`), "a report path" (`spec:99`, `spec:101`) and "an output path" (`spec:102`). The brief template (`spec:73`) therefore cannot list exact flags per command.
  - `workflow`'s package id is generated at run time (`spec:92`), and `init-lite`, `cleanup-audit` and `tdd` use fixed or default locations (`spec:85`, `spec:87`, `spec:90`). The coordinator cannot know the path in advance for these, and `docs/[domain]/` for `tdd` is not "dedicated to this run" (`inventory/commands-b.md:222`).
  - Observation outside the spec's evidence set: the command definition used for this audit already chose `--report-dir` as a separate flag and keeps `--output` file-valued (`command.md:22`, `command.md:460`). That shows the drift this finding warns about.
  - Recommendation: add one column to section 3 with the exact flag and the contract path; for run-time ids, say the worker reports the path.
- **M2. Dangling references B-1 and B-2 (MINOR in effect, kept here for traceability).** Wiegers. The spec cites "B-1" (`spec:76`, `spec:195`, `spec:265`) and "B-2" (`spec:62`, `spec:200`) with no definition anywhere in the file. Recommendation: define them or inline the rule.
- **M3. SA-3 and WC-4 disagree on when a contract is written (MAJOR, graded Medium).** Wiegers. WC-4 writes the contract "In unattended mode" (`spec:62`). SA-3 also writes it "when the caller passes the new output flag" (`spec:148`). AC-1.3 only tests the case with neither (`spec:197`). A person who runs `/sc:analyze --output d` gets a contract under one reading and not the other. The implementer picks one of two readings, so this is Medium.
- **M4. WC-6 "fresh output directory" conflicts with the fixed contract path (MAJOR, graded Medium).** Wiegers, Nygard. Commands without a resume flag "write each run into a fresh output directory" (`spec:64`), which is the "fresh dir" cell on most section 3.2 rows. WC-4 fixes the contract at `<output-dir>/return-contract.yaml` (`spec:62`), and section 2.3 does not say the coordinator passes a new directory per `--retry-of` attempt (`spec:73`). Either the command makes a subdirectory (the contract path moves) or the coordinator supplies a new directory (unstated). No acceptance check covers either reading.
- **M5. Stale contract defeats "no report means failed" (MAJOR, graded Medium).** Whittaker, Sequence Attack (FR-2.4). The minimum contract fields have no run, dispatch or time field (`spec:62`), and WC-5 maps "no report exists" to `failed` (`spec:63`).
  - Concrete attack: attempt 1 writes `status: succeeded`; a follow-up Dispatch reusing the same `<output-dir>` is cut off by context exhaustion before it writes anything; the worker finds the old file, so no-report becomes report-exists, and it sends `--outcome succeeded`.
  - Related gap: a present but unparseable file, or a `status` outside the four values, has no stated outcome (see the boundary table).
  - Recommendation: add `dispatch_id` and a written-at time to the minimum fields. The contract also has no version field, though existing contracts carry one (the workflow contract is "contract 1.1", `inventory/commands-b.md:272`).
- **M6. Existing `status` vocabularies were never checked (MAJOR, graded Medium).** Newman. WC-4 says commands that already write a contract "keep their fields and add the missing ones" (`spec:62`), while the Decisions table fixes `status` to four values (`spec:262`). No inventory line lists the current `status` values of brainstorm, reflect, workflow or adversarial (`inventory/commands-b.md:272`, `inventory/commands-a.md:97`). If one differs, both statements cannot hold. UNVERIFIED either way.
- **M7. Requirements with no acceptance check (MAJOR, graded Medium).** Crispin, Wiegers. WC-6 (resume or safe re-run), WC-11 (parallel-safe writes, only `save` has AC-3.4 at `spec:207`) and WC-12 (`check` before `worker_done`) have no check in section 7. WC-10 (wait splitting) is verified only in AC-4.3, which is conditional on D3(b) (`spec:210`), although the `cli-eval` row also needs it (`spec:104`).
- **M8. Live check weaknesses (MAJOR, graded Medium).** Crispin.
  - Step 3 waits "until `worker_done` arrives" with no failure bound (`spec:182`). A worker that stalls on a plain chat question never raises `agentWait` (`inventory/commands-a.md:62`), so the loop never ends.
  - Step 6 requires that "only files under the brief's output directory" change (`spec:185`). That fails for the ready commands that write elsewhere by design: `reflect` writes `docs/memory/reflect/...` and moves a folder (`inventory/commands-b.md:114`), `tdd` writes `docs/[domain]/` and `.dev/tasks/to-do/` (`inventory/commands-b.md:222`), and `cleanup`/`improve` edit source.
  - Step 5 greps the transcript for the string `AskUserQuestion`, which also appears in loaded instruction text, so it can fail on text rather than on a call.
- **M9. Brief template demands `--unattended` where P0 commands do not accept it (MAJOR, graded Medium).** Wiegers. Section 2.3 says the brief carries "the exact command line including `--unattended`" (`spec:73`). The P0 smoke commands in AC-0.4 omit it (`spec:194`), correctly, since the flag arrives in P1. The exception is not stated in section 2.3.
- **M10. `--unattended` combined with person-mode flags is inconsistent (MAJOR, graded Medium).** Whittaker, Divergence Attack (FR-2.2). `--interactive` is refused under `--unattended` for `cleanup`, `improve`, `roadmap` (`spec:103`, `spec:110`, `spec:118`). For `adversarial`, `brainstorm`, `release-split` it is only "never" in the brief (`spec:83`, `spec:84`, `spec:89`). WC-2 says the command "never calls `AskUserQuestion`" under `--unattended` (`spec:60`), so the precedence for the second group is unstated.
- **M11. WC-9 "paid external run" is undefined (MAJOR, graded Medium).** Nygard. WC-9 turns off any default that "calls a paid external run" (`spec:67`). `research` and `review-translation` use Tavily web search (`inventory/commands-b.md:134`, `:144`), `release-split` defaults to opus models (`inventory/commands-b.md:121`), and `cli-eval run` executes real evals (`inventory/commands-a.md:44`). Their rows do not say whether these are off (`spec:116`, `spec:117`).
- **M12. `/sc:tasklist` Stage 10.5 gate is only partly resolved (MAJOR, graded Medium).** Nygard. The row passes `--unattended` to each reflect so the headless auto-accept rule applies (`spec:122`). Stage 10.5 also says `needs_human_decision` items HALT (`inventory/commands-b.md:209`), and no resolution under WC-2 is given. The row also contradicts the reflect advice to omit `--remediate` (`spec:88`, `inventory/commands-b.md:215`), and its safety rests on UNVERIFIED item 9 (`spec:280`).

=== ARCHITECTURE ANALYSIS ===

No additional blocking finding. The core decision (Orca on top, commands unchanged as units of work, section 1) is sound against the evidence: every cited R1-R5 and E1-E6 line was found at its inventory line (`inventory/orca-capabilities.md:97-103,145-150,155-161`). The following are Medium or minor.

- **M13. Ask has no upper bound (MAJOR, graded Medium).** Nygard. WC-3 lets a worker `ask` once, wait, and resume the same message id on timeout, and sends no heartbeat while blocked (`spec:61`; `inventory/orca-capabilities.md:60,64`). If the coordinator is gone or never answers, the worker waits forever. Whether Orca bounds a Dispatch is UNVERIFIED (`spec:282`; `inventory/orca-capabilities.md:188`). Recommendation: state a maximum number of resumes, after which the gate resolves as blocked.
- **M14. Contract is a runtime-read shared file with no version or missing-file rule (MAJOR, graded Medium).** Newman, Fowler. Every command points to `~/.claude/WORKER-CONTRACT.md` and defers its rules to it (`spec:52`). What a command does under `--unattended` if that file is absent (older install) is not stated, and the file has no version marker, so commands and contract can drift apart. This compounds M5 and M6.
- **Hohpe note (no finding):** report-by-pointer plus `worker_done` (`spec:62-63`) has the right ordering invariant, because the contract is written when the command ends, before the worker sends. The one weak point is staleness (M5).

### Minor notes (never fail the review)

- N1. Section 1.2 E3 cites `invocation_method: "skill-direct"` as support for the direct route (`spec:23`), while section 1.4 (1) says the PR #329 run proves only the nested route (`spec:43`). Inventory A calls the same run "proven as a direct Orca-worker skill call" (`inventory/commands-a.md:35`). The spec's reading is the more cautious one; reword E3.
- N2. D5(b) says raising depth would "break R1's protection against runaway fan-out" (`spec:252`), but R1 is a reason for rejecting the alternative, not a protection (`spec:33`).
- N3. Contract `status: blocked` shares its word with Orca's Task status `blocked`, which Orca sets from unmet dependencies (`inventory/orca-capabilities.md:89`). A coordinator reading both could confuse them.
- N4. The spec says 43 commands (`spec:76`). The inventories list exactly 21 + 22 (`inventory/commands-a.md:3`, `inventory/commands-b.md:3`). The session's installed command list also shows `sc:graph`, `sc:impact` and `sc:issue`, which neither inventory covers. UNVERIFIED: no `cmd/` directory in this workspace, and the date of those commands is unknown.
- N5. The AC-C1 and AC-C5 commands escape `|` as `\|` inside table cells (`spec:172`, `spec:176`); copied as shown they are not runnable.
- N6. The checks that use `grep -E '^-[^-]'` (AC-C5, AC-0.3, `spec:176`, `spec:193`) cannot see a deleted markdown bullet. Deleting `- item` gives the diff line `-- item`, which `^-[^-]` skips. A deletion would pass an "additive only" check (SA-4, SA-5). Use `grep '^-' | grep -v '^---'`. This is also a Medium candidate; graded here as a note because it narrows a verification, not the requirement.
- N7. SA-2 allows an example of "a caller's question channel" in the contract file (`spec:147`), but AC-C1 greps all of `src/superclaude/core` for `orca orchestration|worktree|terminal|agent` and expects nothing (`spec:172`). P0 adds a contract file and an Orca section to `HOW-WE-WORK.md` there (`spec:158`), so wording must avoid those exact strings or AC-C1 fails. Medium if it fires; no wrong outcome is forced by the text.

## Guard Condition Boundary Table

Completed before synthesis (FR-10). Guards found: G1 outcome mapping (WC-5), G2 ask wait (WC-3), G3 output-directory flag (WC-4), G4 wait splitting and heartbeat (WC-10), G5 flag combination, G6 task confidence gate, G7 nesting depth (WC-8), G8 outward-default switch (WC-9), G9 readiness limit (WC-1). Responsibility: Nygard (build), Crispin (completeness), Whittaker (attack).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G1 outcome mapping | spec:63 (WC-5) | Zero/Empty | no contract file | true | `--outcome failed` | OK |
| G1 outcome mapping | spec:63 | Typical | `status: succeeded` | true | `--outcome succeeded` | OK |
| G1 outcome mapping | spec:63 | Sentinel Value Match | `partial` | true | maps to `succeeded`, first body sentence says partial | OK |
| G1 outcome mapping | spec:62-63 | Legitimate Edge Case | file present but unparseable, or `status` outside the four values | unspecified | none stated | GAP (M5; Medium) |
| G1 outcome mapping | spec:62-63 | Legitimate Edge Case | stale file from an earlier Dispatch in the same directory | file found | read as this run's report | GAP (M5; Medium) |
| G2 ask wait | spec:61 (WC-3) | Typical | answer arrives | true | re-invoke or resume with answer as flag | OK |
| G2 ask wait | spec:61 | Maximum/Overflow | no answer ever / repeated timeouts | resumes same id | no limit, no fallback to blocked | GAP (M13; Medium) |
| G3 output flag | spec:62 (WC-4) | Zero/Empty | `--unattended` without any output flag | unspecified | only `post-release` says blocked (`spec:113`) | GAP (M1; Medium) |
| G3 output flag | spec:62, 90 | Legitimate Edge Case | `--output` file whose parent is a shared directory (`tdd` default `docs/[domain]/`) | "dedicated" required | B-2 undefined | GAP (M1/M2; Medium) |
| G4 wait/heartbeat | spec:68 (WC-10) | Typical | waits of at most 4 minutes | true | heartbeat between waits | OK |
| G4 wait/heartbeat | spec:68, 114 | Maximum/Overflow | one poll-plus-sleep over 4 minutes | unknown | "confirm" (open item 12, `spec:283`) | OK (open item stated) |
| G4 wait/heartbeat | spec:68, 104 | Maximum/Overflow | single eval of up to 3600 s | true | must split into waits | OK |
| G5 flag combination | spec:83-118 | Sentinel Value Match | `--unattended --interactive` on adversarial, brainstorm, release-split | unspecified | "never" only in the brief | GAP (M10; Medium) |
| G5 flag combination | spec:103,110,118 | Sentinel Value Match | `--unattended --interactive` on cleanup, improve, roadmap | true | refused | OK |
| G6 task confidence | spec:121 | Zero/Empty | confidence 0 | true | blocked | OK |
| G6 task confidence | spec:121 | Legitimate Edge Case | exactly 0.70 | false | not below 0.70, proceeds | OK |
| G7 nesting depth | spec:66, 252 (WC-8) | Typical | depth 1 | true | command may not call `worker-start` | OK |
| G7 nesting depth | spec:66, 252 | Legitimate Edge Case | user raises depth (D5 b) | true | WC-8 still forbids | OK |
| G8 outward default | spec:67 (WC-9) | Typical | default push, PR, post | true | off | OK |
| G8 outward default | spec:67 | Legitimate Edge Case | "paid external run" (Tavily, opus models, real evals) | unspecified | no definition | GAP (M11; Medium) |
| G9 readiness | spec:59 (WC-1) | Maximum/Overflow | startup fallback above about 45 s | true | fails readiness | OK (`EVIDENCE.md:56` UNVERIFIED) |
| G9 readiness | spec:59 | Zero/Empty | `--timeout-ms 0` | falls back to 60 s | not needed by the contract | OK (`inventory/orca-capabilities.md:45`) |

Omitted classes (one line each): G1 One/Minimal (no count semantics); G2 Zero/Empty (a missing question cannot arise, the worker creates it); G4 Zero/Empty (no wait means nothing to split); G5, G6 One/Minimal (flag presence is boolean); G7 Zero/Empty (depth is at least 1, `inventory/orca-capabilities.md:100`); G8 Zero/Empty (no default means nothing to turn off); G9 Sentinel (no sentinel value).

## Attack summary (Whittaker)

- Sequence attack: stale contract versus the no-report rule, M5.
- Divergence attack: `--unattended` plus a person-mode flag, M10.
- Sentinel collision: `status: blocked` versus Orca Task `blocked`, N3.
- Zero/empty attack: no output flag under `--unattended`, M1.
- Accumulation attack: repeated `ask` resumes with no limit, M13.

## Verification statement

- Blocking findings: B1, B2.
- Medium findings are listed under follow-up candidates (M1-M14). Minor notes are N1-N7. None of these triggers a revision.
- No brief clause was overridden: the brief did not widen or narrow the review scope.
- Inventory evidence cited for the section 3 rows and the section 4 reasons was found at the cited lines. Findings that depend on files outside the workspace are marked UNVERIFIED above.

## Reviser brief

Repair only the blocking findings B1 and B2.
- Revise only text a blocking finding names.
- Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave minor and Medium findings alone.
- Return the candidate once and do not award yourself a PASS.

verdict: FAIL
