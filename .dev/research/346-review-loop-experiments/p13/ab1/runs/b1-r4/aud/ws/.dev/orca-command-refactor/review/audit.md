review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md

## Header
- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- label: first review of the whole document (labelled whole-document audit of the final spec). Prompt applied: FIRST-REVIEW in `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full).
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 295 lines
- candidate sha256: `4e04817fb543edcb9c65e6cba29debf913eabe4a8ae7675d2f06bb264208171f`
- baseline: missing (none given; neither `--re-review` nor `--baseline` was passed, so this is a first review)
- reviewer model actually used: claude-sonnet-5-5
- mode flags: `--unattended` not passed. The session that ran this review asks the user once whether to open an issue for the follow-up candidates; no issue is created here.

## Coverage
Covered: all 9 sections of the spec plus `## Decisions` and `## UNVERIFIED items`. I read the README (`.dev/orca-command-refactor/README.md:1-39`) and the three inventories (`INV-A` = `inventory/commands-a.md`, `INV-B` = `inventory/commands-b.md`, `CAPS` = `inventory/orca-capabilities.md`) in full. I checked these against the inventories:
- the 10 / 27 / 6 split, by counting the rows of 3.1, 3.2 and 4
- the phase column of every 3.2 row against section 6
- the per-command gates, report files and resume mechanisms against `INV-A:35-55` and `INV-B:31-52`
- each Orca claim against `CAPS`

Not covered:
- Every `src/`, `~/.claude/`, `CLAUDE.md`, `Makefile`, `pyproject.toml` and `.dev/evals|codegraph-migration` citation is UNVERIFIED here, because those files are not inside the sandbox workspace. This includes spec lines 11 and 25 (the author's re-reads and greps), 52, 83-125, 150, 164, 174 and 193.
- The Orca guide quotes are checked only against the `CAPS` lines that carry them. I could not run `orca-ide`.
- Nothing is implemented, so I could not run the commands in section 7.

## Experts and method
- Requirements focus: Wiegers (lead), Adzic, Cockburn.
- Architecture focus: Fowler (lead), Newman, Hohpe, Nygard.
- Whittaker is active in every panel. Review order follows the command's fixed sequence.
- Grading follows the Grading check at `~/.claude/rules/prompts/document_review_loop_prompts.md:31`: a finding is blocking only if the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y" holds with no further assumption.
- Result: 0 CRITICAL and 0 blocking findings. 9 Medium (graded down from MAJOR where the label alone would have made them blocking) and 6 minor.

## Strengths confirmed
These are verified inside the sandbox.
- The decision, its rejected alternative and its evidence gaps are stated plainly (spec lines 13-45).
- The counts reconcile: 10 + 27 + 6 = 43, and 21 + 22 = 43 (spec lines 76, 78, 94, 127; `INV-A:3`, `INV-B:3`).
- Every 3.2 row's phase matches the section 6 phase lists. Phase 1 has 9 of the 3.2 rows (analyze, build, business-panel, design, document, explain, index, test, load), phase 2 has 11, phase 3 has 4 and phase 4 has 3, which is 27 (spec lines 159-162).
- Verdicts agree with the inventories (`INV-A:73`, `INV-B:278`).
- The WC-9 outward-action default (spec line 67) matches the README rule against pushes and PRs (`README.md:31`).

## === REQUIREMENTS ANALYSIS ===

### Blocking findings
None.

### Medium findings (follow-up candidates, not blocking)

**F-01 (Medium, Wiegers/Adzic): AC-1.2 tells the tester to pass `--output <dir>` to every phase-1 command, but several do not take a directory-valued `--output`.**
- AC-1.2 (spec line 206) runs the 7.2 check "on each P1 command with `--unattended --output <dir>`".
- Section 3.1 says init-lite takes `--output <file>` (spec line 87).
- WC-4 says cleanup-audit and index-repo have no output flag (spec line 62), and 3.1 gives them none (spec lines 85-86).
- A tester following AC-1.2 literally passes a directory as init-lite's file, and passes an unknown flag to cleanup-audit and index-repo.
- This is Medium rather than blocking because the 3.1 "Brief must pass" column (spec line 81) lets the tester see the right form without guessing.
- Suggested follow-up: the AC should say "the output argument named in the command's 3.1/3.2 row".

**F-02 (Medium, Wiegers): the phase-1 scope and WC-4 disagree on whether commands without an output flag gain one.**
- The P1 row says "output flags for commands that lack one" (spec line 159).
- WC-4 says cleanup-audit, index-repo and troubleshoot "have no output flag" and write the contract beside their existing report (spec line 62). The 3.1 index-repo and cleanup-audit rows add only a state-the-location fix (spec lines 85-86).
- Consequence: for index-repo the contract lands next to `PROJECT_INDEX.md`. The inventory says that location is "implied, UNVERIFIED" and is the repo root (`INV-A:53`, `INV-A:117`).
- A contract file in the repo root is reachable by two parallel workers, which WC-11 forbids (spec line 69). Whether index-repo gains a flag is therefore underspecified (a requirement the document never settles).

**F-03 (Medium, Cockburn/Adzic): WC-5 as written conflicts with the P0 acceptance test, and the carve-out covers only P0.**
- WC-5 says `--outcome failed` when "no report exists, or its `status` is missing" (spec line 63).
- AC-0.4 and 7.2 step 3 expect `succeeded` for a P0 run with no contract (spec lines 192, 204). That carve-out is stated only for P0.
- Section 3.1 says ready commands "report the named file until the phase in its row adds the contract" (spec line 79). This covers reflect, release-split, tdd and troubleshoot until P2. It also covers workflow, brainstorm and adversarial, which already write contracts with their own status fields, between P0 and P1.
- Section 3.1 gives brainstorm and workflow "Small fix: None" (spec lines 84, 92), and WC-4's "keep their own status field and add `status` beside it" has no named owner for them until the P1 row says so.
- Why not blocking: the sentence needs the guess that a worker applies WC-5 to a P1/P2 interim command, and the 3.1 note and the 7.2 carve-out point the other way. A one-line "before its contract phase, a markdown report counts as `succeeded`" in WC-5 would remove the doubt.

**F-04 (Medium, Whittaker, FR-9): WC-9's trigger for outward actions is wider than D4 settles.**
- WC-9 turns an outward default on "only through the command's own explicit flag written in the brief" (spec line 67).
- D4 is an open decision on whether a brief may authorize outward actions at all (spec lines 254-257). Option (b) "Never" would contradict WC-9.
- Commands in P2 already depend on WC-9: auggie-review `--post-pr` and task `commit`/`push` (spec lines 100, 121). P2 is allowed to proceed on the recommendations (spec line 235).
- The recommendation (a) requires a quoted user instruction, but WC-9 does not carry that condition, so an implementer building from WC-9 alone accepts any brief flag. No outward action is turned on by default, so this stays Medium, but it is a hard-requirement text that outruns its pending decision.
- Fix candidate: add "(subject to D4)" to WC-9.

**F-05 (Medium, Whittaker): "calls a paid external run" in WC-9 is undefined.**
- It is unclear whether research and review-translation web search (Tavily) and cli-eval real-model runs count (spec lines 67, 116-117, 104; `INV-B:134`, `INV-B:144`).
- The 3.2 rows do not mention it for research or review-translation, so two implementers could differ.
- It is a missing definition, not a stated harmful text.

**F-06 (Medium, Adzic): AC-2.2 (gate-trigger runs) can fail for a reason that is not a defect.**
- AC-2.2 expects `worker_done --outcome failed` and a blocked contract (spec line 210).
- WC-3 lets the worker `ask` the coordinator first and then re-invoke (spec line 61), which would leave the worker waiting in `ask` until answered.
- The test brief therefore needs to say whether the worker may `ask`. The spec does not say so.

## === ARCHITECTURE ANALYSIS ===

### Blocking findings
None.

### Medium findings

**F-07 (Medium, Nygard/Fowler): liveness handling for long Agent-tool fan-out is not specified.**
- WC-10 splits only poll waits and evals into at most 4 minutes (spec line 68).
- E4 keeps each command's own Agent-tool fan-out unchanged (spec line 24), for example adversarial 2-10 agents, cleanup-audit waves and tdd research (`INV-A:35`, `INV-A:42`; `INV-B:47`).
- While the top-level session waits for subagents it cannot send the 5-minute heartbeat, and whether Orca uses heartbeat age is UNVERIFIED (`CAPS:130`, `CAPS:182`).
- This is not shown to break the worker, since the heartbeat is a liveness signal, so it stays a gap the document never states.
- Fix candidate: say that WC-10 applies to blocking waits only, or that fan-out is exempt.

**F-08 (Medium, Fowler/Hohpe): D3/D5 and WC-3 name a message path ("escalation") that WC-3 does not define.**
- The pr-submit row says operator HALTs resolve as blocked and "the worker may use `ask` or `escalation`" (spec line 114).
- WC-3 defines only `ask` (spec line 61), and the CAPS inventory documents `escalation` only as a valid type and a wait filter (`CAPS:63`, `CAPS:75`).
- It is a small undefined interface in a phase (P4) that waits for D3 anyway.

**F-09 (Medium, Newman/Nygard): the tasklist row hands an unbounded HALT to reflect without a gate resolution.**
- Under `--unattended`, Stage 10.5 passes `--unattended` to reflect so the headless auto-accept rule applies (spec line 122).
- The inventory records that `needs_human_decision` items HALT in that stage (`INV-B:209`) and that "who answers inside a subagent is not stated: UNVERIFIED".
- WC-2 forbids any person-blocking step in unattended mode (spec line 60). The tasklist row does not say how a `needs_human_decision` HALT resolves, and the reflect row covers only `--remediate` (spec line 88).
- UNVERIFIED #9 (spec line 290) is the same doubt about whether reflect treats a worker as headless.
- The wrong outcome needs a guess about reflect's behaviour, so Medium. A "needs_human_decision resolves as blocked" clause in the tasklist row would close it.

### Also noted (architecture)
- Fowler: the one-shared-contract-file design (`WORKER-CONTRACT.md` referenced by installed path, spec lines 52, 274) matches the repo's installed-path rule as summarised in the spec. Newman: the status vocabulary is versioned with `contract_version` (spec line 62).
- Hohpe: the report-file rendezvous (the worker passes a path, Orca does not check it, the coordinator opens it) is explicit and defensible (spec lines 62, 73; `CAPS:79`).

## Other findings

**F-10 (Medium, Wiegers): section 1.4 point 2 asserts an ordering that the evidence does not establish.**
- The text says a command's own `AskUserQuestion` "comes after readiness, so it does not fail `worker-start`" (spec line 44).
- `CAPS:47` records that for Claude the task is passed on the command line (argv injection), so the first command runs at launch. Whether Orca's readiness check completes before that first turn asks is not shown anywhere.
- The README states the opposite risk as the motivating fact (`README.md:14` area; `EVIDENCE.md:39` as cited by `CAPS:49`).
- Impact: the characterisation could be wrong for a command that asks on its first turn. WC-1/WC-2 remain correct either way, so the requirements are not harmed. Medium; the claim should be marked UNVERIFIED.

**F-11 (Medium, Adzic): AC-3.2 accepts a silent fresh start in a directory that holds a prior session.**
- AC-3.2 expects roadmap to "start fresh" with an existing `.session-memory.md` and no resume flag (spec line 215), matching the row at spec line 118.
- A retry worker whose brief lacks the resume flag would overwrite the earlier attempt's state in that directory. WC-6 asks that a retry not corrupt the first attempt's output (spec line 64), and the roadmap row's resume cell says only "reconcile" (spec line 118).
- Nothing says a fresh start must use a new directory.
- It is a missing restriction rather than a stated harmful text, so Medium.

## Guard Condition Boundary Table
Trigger: the spec has threshold and status guards, so the table is produced. Responsibility: Nygard (construction), Crispin (completeness), Whittaker (attack). The gaps are graded under FR-8/FR-9: none names a stated text that causes a concrete wrong outcome, so each is Medium and carried above or as a minor note. Classes omitted for a guard are listed with a one-line reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| outcome mapping (WC-5) | spec:63 | Zero/Empty | no report file | true (failed) | `--outcome failed` | OK |
| outcome mapping (WC-5) | spec:63 | Sentinel Value Match | `status: partial` | true (succeeded) | succeeded; body states `partial` | OK |
| outcome mapping (WC-5) | spec:63, 192, 204 | Legitimate Edge Case | P0 markdown report, no `status` | true (failed per WC-5) | AC-0.4 expects succeeded; carve-out at spec:192 only | GAP (F-03, Medium) |
| 4-minute wait split (WC-10) | spec:68 | Maximum/Overflow | one blocking tool call over 4 min | true | split into waits of at most 4 min | OK |
| 4-minute wait split (WC-10) | spec:68 | Legitimate Edge Case | long Agent-tool fan-out | not stated | unspecified | GAP (F-07, Medium) |
| `--unattended` gate resolution (WC-2) | spec:60 | One/Minimal | one gate per command | per 3.1/3.2 row | documented default, caller flag or blocked | OK |
| `--unattended` gate resolution (WC-2) | spec:122 | Legitimate Edge Case | `needs_human_decision` HALT in tasklist 10.5 | not stated | unspecified | GAP (F-09, Medium) |
| output-dir rule (WC-4) | spec:62 | Zero/Empty | no output given | true | command stops before work, no contract, worker ends failed | OK |
| output-dir rule (WC-4) | spec:62, 86 | Legitimate Edge Case | report at repo root (index-repo) | not stated | contract placed beside report; collision not addressed | GAP (F-02, Medium) |
| outward-action default (WC-9) | spec:67 | Sentinel Value Match | brief carries explicit flag | true | action on; user-instruction condition pending in D4 | GAP (F-04, Medium) |
| nested depth (R1) | spec:33 | Typical | depth 1 | true | `nested_worker_depth_exceeded`; call sites UNVERIFIED (`CAPS:103`) | OK |

Omitted classes: the Maximum class for WC-5 and WC-2, because the outcome enum is closed (four statuses plus missing); the Zero/Empty class for WC-10, because a zero-length wait never blocks.

## Pipeline Dimensional Analysis
Not triggered as a data-pipeline analysis, because the spec describes a rollout rather than a count-changing data flow. The only count flow is the command partition, and it is conserved: 43 commands = 10 ready + 27 needing change + 6 coordinator-only (spec lines 76, 78, 94, 127; `INV-A:3`, `INV-B:3`). No Quantity Flow Diagram is produced.

## Minor notes (never fail the review)
- N-1: undefined labels. The spec cites "L1", "L2", "L4", "L5" and "L17" with no legend (spec lines 62, 76, 92, 178, 183, 192, 203, 204), and `review/` holds no file that defines them. They appear to be finding ids from an earlier review. They should be removed or defined.
- N-2: SA-4 names a workflow contract-gap fix (spec line 149), while the 3.1 workflow row says "Small fix: None" (spec line 92).
- N-3: the 3.1 init-lite row says "None (P1)" for its small fix, while the P1 row adds its contract (spec lines 87, 159).
- N-4: the P1 row says "No person gate is involved" (spec line 159), while business-panel, explain and test carry refusals under `--unattended` (spec lines 102, 108, 123).
- N-5: for `/sc:workflow` the retry brief "names that directory" (WC-6) while WC-4 says the package id is generated (spec lines 62, 64, 92). The retry directory is therefore not nameable in advance.
- N-6: WC-1 and WC-12 have no acceptance check of their own. 7.2 step 1 covers readiness indirectly (spec lines 59, 70, 190).

## Cross-checks recorded as UNVERIFIED in this sandbox
- E5 grep results (spec line 25) and the "re-read 11 locations" statement (spec line 11).
- `install_core.py`, `Makefile`, `pyproject.toml` and `CLAUDE.md` line citations (spec lines 52, 150, 164, 174, 193).
- Spec line 295: "about 340 citations, 9 defects fixed" is the author's claim, not re-performed.

## Follow-up candidates (Medium and minor)
F-01, F-02, F-03, F-04, F-05, F-06, F-07, F-08, F-09, F-10, F-11 (Medium) and N-1 to N-6 (minor). None triggers a revision, fails this review or appears in a Reviser brief. The session that ran this review asks the user once whether to open an issue for them; no issue is created without the answer.

## Reviser brief
None: no blocking finding is open, so no revision is requested. (The brief contract: revise only text a blocking finding names, add no rule or section no blocking finding calls for, cite the finding id on each addition, prefer deleting or narrowing, and report the byte size before and after with bytes added and deleted per finding id.)

verdict: PASS
