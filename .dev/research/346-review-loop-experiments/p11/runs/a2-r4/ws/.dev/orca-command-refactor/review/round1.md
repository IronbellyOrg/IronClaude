review: 1 of 3

# /sc:spec-panel critique, round 1: orca-worker-contract-spec.md

| Field | Value |
|---|---|
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines) |
| sha256 | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` |
| Mode / focus | critique / requirements, architecture |
| Run type | first review of the full document. No `--re-review` or `--baseline` was given, so there is no baseline and no prior-findings file. |
| Input status | complete. README, the candidate and all three inventories were read in full. Nothing was missing or unreadable. |
| Candidate edited | no. No revised specification was written (the Improve step is out of scope for this brief). |

Citation shorthand: `SPEC:N` is the candidate, `CAPS:N` / `INV-A:N` / `INV-B:N` are `inventory/orca-capabilities.md`, `commands-a.md`, `commands-b.md`, `README:N` is `.dev/orca-command-refactor/README.md`. Every `SPEC:` and inventory line was read in this run. A candidate citation to a file outside the README and inventories (`CLAUDE.md`, `src/...`, `EVIDENCE.md`, `Makefile`, `pyproject.toml`) is UNVERIFIED unless an inventory line quotes it, and I say so where it matters.

## What I covered

- All of section 2 (WC-1 to WC-12), sections 3.1, 3.2, 4, 5, 6, 7 (all of 7.1 to 7.3), 8 and 9, plus the Decisions and UNVERIFIED lists (`SPEC:1-285`).
- Every `CAPS:` and `INV-` citation in sections 1 and 2 against the inventory line it names (E1, E4, R1 to R4, WC-1, WC-3 to WC-8, WC-10 to WC-12). All matched the line cited, except the points listed in N-1 and N-6.
- Counts: 43 = 10 + 27 + 6 (`SPEC:76`) matches `INV-A:73` (5/13/3) plus `INV-B:278` (5/14/3). The 27 rows of 3.2 are all assigned a phase: 9 in P1, 11 in P2, 4 in P3, 3 in P4. The 10 ready commands are 4 in P1 fixes, 4 in P2 and 2 (brainstorm, init-lite) with no named fix.
- Dependencies the spec touches: the Orca behavior it relies on (`CAPS:44-80`, `CAPS:97-103`, `CAPS:145-161`) and the command behavior in the two inventories.
- Not covered: command and skill source files, `EVIDENCE.md`, `CLAUDE.md`, `HOW-WE-WORK.md`, `install_core.py` and the PR #329 run files. None is in the evidence set I may check, so those citations stay UNVERIFIED.

## Grading rules applied

- Review Loop bullet 2 says CRITICAL and FR-8/FR-9 findings are blocking and a MAJOR is blocking only with a concrete wrong outcome. The brief adds a grading check: blocking needs a sentence that holds with no further assumption. Otherwise the finding is Medium and goes under follow-up candidates even when labeled MAJOR. I applied the brief as a narrowing under bullet 7. The Boundary Table GAP rows below carry the FR-8 label of MAJOR minimum, and each is then graded by the brief's sentence test. If the coordinator reads bullet 2 as making every FR-8 GAP blocking regardless, then F-1, F-2, F-5, F-6 and F-9 (the GAP-backed findings) become blocking. I am flagging this so the call is the coordinator's, not mine.
- Pipeline Dimensional Analysis (FR-17) triggered on the command triage funnel. A count mismatch is CRITICAL under FR-19 and is B-1.
- `--focus correctness` is not active, so no State Variable Registry is produced. The Guard Condition Boundary Table is produced because the spec contains threshold and boolean guards.

## Guard Condition Boundary Table (Nygard builds, Crispin checks completeness, Whittaker attacks)

Six rows per guard. Status GAP means FR-8 MAJOR minimum, linked to the finding in the last column of the notes under the table. Table is complete: five guards, thirty rows, no blank cell.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 launch prompt vs readiness limit | `SPEC:59` WC-1; `CAPS:44-45` | Zero/Empty | no startup prompt | limit not hit | worker reaches `input_accepted` (`CAPS:49`) | OK |
| G1 | `SPEC:59` | One/Minimal | fallback 1 s | pass | passes (any fallback "well inside" the limit) | OK |
| G1 | `SPEC:59` | Typical | 30 s fallback | pass | start returned after 34 s, `ready` (`CAPS:49`) | OK |
| G1 | `SPEC:59` | Maximum/Overflow | fallback longer than the limit (default 60 s, or the start's `--timeout-ms`) | fail | `agent_readiness` timeout (`CAPS:49`); "well inside" is unquantified but conservative | OK |
| G1 | `SPEC:59` | Sentinel Value Match | `--timeout-ms` omitted | default 60 s | `CAPS:44` default applies | OK |
| G1 | `SPEC:59` | Legitimate Edge Case | fallback equal to limit | fail (race) | excluded by "well inside" | OK |
| G2 heartbeat split | `SPEC:68` WC-10 | Zero/Empty | step with no blocking call | not triggered | nothing to split | OK |
| G2 | `SPEC:68` | One/Minimal | one call under 1 s | not triggered | none needed | OK |
| G2 | `SPEC:68` | Typical | one 4-minute wait | not triggered | within the cap | OK |
| G2 | `SPEC:68`, `SPEC:104`, `SPEC:114` | Maximum/Overflow | one tool call over 5 min that is not a poll or an eval wait: an Agent-tool fan-out call, a project build or test run | triggered | unspecified. Only cli-eval and pr-submit get a split; the rest of the fan-out commands (`SPEC:24`) and `build`/`test` are silent | GAP (F-5) |
| G2 | `SPEC:114` | Sentinel Value Match | pr-submit `--timeout 600` equal to 600 s | depends on reading | the spec's gloss (cumulative budget) differs from `INV-B:95` ("up to 600 s per wait"); source UNVERIFIED | GAP (F-5) |
| G2 | `SPEC:68`, `CAPS:64` | Legitimate Edge Case | worker blocked in `ask` or `check --wait` | skip heartbeat | skipped (`CAPS:64`, `SPEC:61`) | OK |
| G3 outcome mapping | `SPEC:63` WC-5 | Zero/Empty | no report file | no report | `--outcome failed` | OK |
| G3 | `SPEC:63`, `SPEC:183` | One/Minimal | zero-byte or unparseable file, or `status` outside the four values | report "exists" | unspecified (WC-5 tests only "no report exists"; only AC step 4 rejects it) | GAP (F-6) |
| G3 | `SPEC:63` | Typical | `status: succeeded` | succeeded | `--outcome succeeded` | OK |
| G3 | `SPEC:62`, `SPEC:64` | Maximum/Overflow | a stale `succeeded` contract from an earlier attempt in the same directory, new attempt dies before writing | report "exists" | unspecified: no freshness rule | GAP (F-2) |
| G3 | `SPEC:62`, `SPEC:63` | Sentinel Value Match | `status: partial` | maps to succeeded | mapping stated, but when a command reports `partial` is never defined | GAP (F-6) |
| G3 | `SPEC:63` | Legitimate Edge Case | audit verdict FAIL | succeeded | `--outcome succeeded`, body states the verdict | OK |
| G4 `--unattended` and output dir | `SPEC:60`, `SPEC:62` | Zero/Empty | `--unattended` with no output directory | triggered | unspecified: no refusal rule and no place to write the `blocked` report | GAP (F-1) |
| G4 | `SPEC:60` | One/Minimal | `--unattended` on a command with no gate | triggered | no-op, contract still written (`SPEC:159`) | OK |
| G4 | `SPEC:62` | Typical | `--unattended --output <dir>` | triggered | `<dir>/return-contract.yaml` | OK |
| G4 | `SPEC:128` | Maximum/Overflow | `--unattended` passed to a section-4 command | not defined | unspecified: "no `--unattended` mode", with no stated outcome (refuse or ignore) | GAP (F-1) |
| G4 | `SPEC:87`, `SPEC:90` | Sentinel Value Match | `--output` is a file path (tdd, init-lite) | `<output-dir>` undefined | unspecified | GAP (F-1) |
| G4 | `SPEC:64` | Legitimate Edge Case | `--unattended` with the command's resume flag | resume | the resume flag governs (WC-6) | OK |
| G5 task confidence | `SPEC:121` | Zero/Empty | confidence 0 or not computed | below 0.70 | blocked, question in contract | OK |
| G5 | `SPEC:121` | One/Minimal | confidence 0.01 | below 0.70 | blocked | OK |
| G5 | `SPEC:121`; `INV-B:199` | Typical | confidence 0.85 | not below 0.70 | no gate in the spec row | OK |
| G5 | `SPEC:121` | Maximum/Overflow | confidence 1.0 | not below 0.70 | proceeds | OK |
| G5 | `SPEC:121` | Sentinel Value Match | confidence exactly 0.70 | not "below" | proceeds (text says "below") | OK |
| G5 | `SPEC:121`; `INV-B:199` | Legitimate Edge Case | confidence below 0.70 with `--compliance <tier>` already in the brief (the override the gate text offers) | unclear | unspecified: the row blocks without saying whether the override flag clears the gate | GAP (F-9) |

## Quantity Flow Diagram (FR-21)

```text
[43 commands: INV-A 21 + INV-B 22]  SPEC:76
   --> [Triage] --> 6 coordinator-only (SPEC:128)            : N=43, M=37 (diverges, handled)
   --> 37 worker-capable
        --> 10 ready (SPEC:78)            : P1 fixes 4, P2 4, no named fix 2 (brainstorm, init-lite)
        --> 27 needs change (SPEC:94)     : P1 9, P2 11, P3 4, P4 3 = 27 (conserved)
   --> [Consumer: AC-1.1, SPEC:195] expects a `## Unattended mode` section naming return-contract.yaml
       in all 37 after P1
   --> [Producer: load row, SPEC:112 and SPEC:159] gives load no contract and "usage line only"
       => 36 sections, 37 expected          <-- MISMATCH (B-1)
```

## Expert review

Sequence follows the fixed order. Experts without a distinct finding give one line.

=== REQUIREMENTS ANALYSIS ===

### B-1. CRITICAL (blocking). P1's acceptance checks require a contract section that the spec's own `load` row removes.
- Experts: Wiegers (traceability), Crispin (acceptance criteria), Fowler (count divergence).
- Locations: `SPEC:112` (load: "Report: none", "use it as a step inside another worker's brief, not as its own Task", Phase "P1 (usage line only)"); `SPEC:159` (P1 lists "load (usage line only)"); `SPEC:265` (decision: "a report file would be an unrequested addition"); `SPEC:195` (AC-1.1); `SPEC:196` (AC-1.2); `SPEC:183` (7.2 step 4).
- Grading check: An implementer who follows the stated text as written builds a `load.md` with only its usage line fixed, with no `## Unattended mode` section and no contract, and that build is wrong because AC-1.1 asserts every command in sections 3.1-3.2 has an `## Unattended mode` section naming `return-contract.yaml` and AC-1.2 runs the 7.2 live check on each P1 command (load is one), whose step 4 does `test -s <contract>`. Phase 1 cannot pass, and satisfying the checks means writing a contract the load row and Decisions say must not exist.
- Count trace: 37 sections expected, 36 produced (diagram above). FR-19 classes a count mismatch CRITICAL.
- Recommendation: make the checks and the rows agree. Either exclude `load` by name from AC-1.1 and AC-1.2, or change the `load` row so it gets a one-line section stating that it writes no contract. Rationale: AC-1.1 is a mechanical test, so a single exception in the prose fails it every time.
- Priority: High. Quality impact: Consistency +1, Testability +1.

### F-1. MAJOR label, graded Medium. The WC-4 report location rule does not hold for commands the spec itself lists, and has no rule for a missing directory.
- Experts: Wiegers, Adzic, Whittaker (Zero/Empty, Sentinel Collision).
- Locations: `SPEC:62` (WC-4: contract at `<output-dir>/return-contract.yaml`, "known before dispatch"); `SPEC:83` (adversarial: `<output>/adversarial/return-contract.yaml`); `SPEC:92` (workflow: `.dev/tasks/to-do/<id>/return-contract.yaml`); `SPEC:87` and `SPEC:90` (init-lite and tdd take `--output <file>`); `SPEC:128` (section 4).
- Grading check: needs a guess about which reading the implementer picks. For adversarial and workflow the specific row plausibly overrides the general rule, so the sentence "builds X, and X is wrong" needs that guess. For tdd and init-lite `<output-dir>` is undefined, and the missing-directory case is a requirement the document never states. The workflow case is the sharpest: `<id>` is generated, so the coordinator cannot know the path before dispatch (`INV-B:272`), and a pre-creation STOP has no package directory to hold the contract.
- Wrong outcomes if the reading goes the bad way: a coordinator opens `<dir>/return-contract.yaml` and finds nothing for adversarial; a tdd run treats `--output docs/x/TDD.md` as a directory and fails to create `docs/x/TDD.md/return-contract.yaml` beside the file it is writing; `--unattended` with no directory has nowhere to write `status: blocked`.
- Recommendation: give the contract its own directory argument, separate from the file-valued `--output` flags (the command definition this review ran under uses `--report-dir`, `command.md:22-23,456`, outside the binding evidence set), and state the refusal for a missing directory and for section-4 commands.
- Priority: High. Quality impact: Clarity +1, Completeness +1.

### F-2. MAJOR label, graded Medium. A retry or re-run into a directory that already holds a contract is undefined.
- Experts: Nygard, Whittaker (Sequence).
- Locations: `SPEC:62` (path fixed by the coordinator before dispatch); `SPEC:64` (WC-6: no resume flag means "a fresh output directory"); `SPEC:63` (only "no report exists" maps to failed); `SPEC:205` (AC-3.2: existing session memory in `<dir>`, no resume flag, "starts fresh"); `CAPS:116` (retry with `--retry-of`).
- Grading check: the text allows two readings (the command creates a fresh subdirectory, or the coordinator passes a new directory per attempt) and the implementer could pick the worse one, so Medium. A command that makes its own subdirectory breaks the WC-4 path. A command that overwrites in place breaks WC-6 and can leave a stale `succeeded` file for a crashed attempt, which WC-5 then reports as success.
- Recommendation: state who creates the fresh directory (the coordinator, in the retry brief) and require the command to refuse or version a non-empty target.
- Priority: High. Quality impact: Completeness +1.

### F-3. MAJOR label, graded Medium. How a worker runs "the command" is never specified, and AC-0.4 points at a check that does not exist.
- Experts: Cockburn (actor and goal), Crispin.
- Locations: `SPEC:16` ("one worker runs one command"); `SPEC:65` (WC-7: "runs the command directly"); `SPEC:73` (the brief carries "the exact command line"); `SPEC:194` (AC-0.4: "no Agent-tool wrapper, verified in the step-5 transcript"); `SPEC:184` (step 5 searches the transcript only for `AskUserQuestion`); `CAPS:47` (for Claude the task is passed on the command line, so the worker's first message is the preamble, not the `/sc:` line).
- Grading check: this is a requirement the document never states (the invocation mechanism: Skill tool, slash text, or reading the command file), not a stated text that does harm.
- Recommendation: add the invocation rule to WC-7 and give step 5 an explicit pass test for "no Agent-tool wrapper". The project's own command-invocation rule in `CLAUDE.md` is UNVERIFIED here (not in the evidence set).
- Priority: Medium. Quality impact: Testability +1.

### F-4. MAJOR label, graded Medium. Phase 1 ships `--unattended` on commands whose gates and outward defaults are only converted in Phases 2 to 4.
- Experts: Whittaker (Sequence), Adzic.
- Locations: `SPEC:159` (P1: flag accepted by "every command in sections 3.1 and 3.2"); `SPEC:160-162` (P2 to P4 convert the gates); `SPEC:67` (WC-9: under `--unattended` outward defaults are off); `SPEC:79` ("The only command changes are the small fixes").
- Grading check: needs a guess that a coordinator dispatches such a command between phases. The window is real: after P1, `/sc:auggie-review <PR> --unattended` is accepted yet still posts to GitHub without a prompt (`SPEC:100`, `INV-A:38`) until P2. The text also contradicts itself on whether a ready command changes (`SPEC:79` versus `SPEC:159`).
- Recommendation: either accept `--unattended` only on a command once its gates are converted, or state that the flag means nothing until the command's own phase.
- Priority: Medium. Quality impact: Consistency +1.

### F-5. MAJOR label, graded Medium. WC-10 is stated for every long wait but assigned only to cli-eval and pr-submit.
- Experts: Nygard, Newman.
- Locations: `SPEC:68` (WC-10); `SPEC:104`, `SPEC:114` (the only two rows); `SPEC:24` (E4: commands keep their Agent-tool fan-out); `CAPS:130` (heartbeat cadence comes from the preamble, not a guide; use of heartbeat age by Orca is UNVERIFIED, `CAPS:182`).
- Grading check: a requirement the document never states for the other commands. An Agent-tool call that fans out (tdd, cleanup-audit, troubleshoot Tier 2: `INV-B:221`, `INV-A:42`, `INV-B:241`) and a build or test run block one tool call for longer than 5 minutes and cannot be split by the command. The spec also reads `cmd/pr-submit.md:49` as a cumulative budget (`SPEC:68`, `SPEC:114`) where `INV-B:95` reads it as "up to 600 s per wait"; the source is UNVERIFIED.
- Recommendation: say what the coordinator does when heartbeats stop during an unsplittable call, or state that missing heartbeats are not a failure signal.
- Priority: Medium. Quality impact: Completeness +1.

### F-6. MAJOR label, graded Medium. The four-value `status` set is not reconciled with existing contracts, and `partial` is never defined.
- Experts: Wiegers, Adzic.
- Locations: `SPEC:62` ("commands that already write a contract keep their fields and add the missing ones"); `SPEC:262` (fixed set `succeeded / partial / failed / blocked`); `SPEC:263` (partial maps to succeeded); `SPEC:183` (step 4 rejects any other value); `INV-B:272` (workflow contract has a `status` field, vocabulary not recorded); `CAPS:90`, `CAPS:77` (a completed Task releases its dependents, a failed one keeps them blocked).
- Grading check: undefined state, not a stated text that does harm. Whether the existing workflow, brainstorm, reflect and adversarial contracts already use these four values is not in any inventory. If one does not, "keep their fields" and step 4 cannot both hold. `partial` becomes `succeeded` and so unblocks dependents, and no row says what makes a command report `partial`.
- Recommendation: add the existing status vocabularies to the inventory or to a mapping table, and define `partial`.
- Priority: Medium. Quality impact: Clarity +1.

### F-7. MAJOR label, graded Medium. `--unattended` is not required to reach nested invocations.
- Experts: Cockburn, Hohpe.
- Locations: `SPEC:60` (WC-2: "the command never calls `AskUserQuestion`"); `SPEC:122` (the only pass-through: tasklist to reflect); nested calls per `INV-A:39` (brainstorm to adversarial), `INV-B:119,121` (release-split), `INV-B:219` (tdd to `/task`), `INV-B:271` (workflow to reflect), `INV-B:151` (roadmap to adversarial).
- Grading check: a requirement the document never states. A nested skill that asks stalls the worker although the top command honored WC-2.
- Recommendation: add a general rule that a command passes the mode to every nested `/sc:` call.
- Priority: Medium.

### F-8. MAJOR label, graded Medium. Acceptance checks that do not discriminate or can fail a conforming worker.
- Experts: Crispin, Gregory.
- Locations: `SPEC:200` (AC-2.2 requires `--outcome failed` and `status: blocked` for a gate-trigger run) versus `SPEC:61` (WC-3: the worker "may" ask the coordinator and re-invoke instead, which ends `succeeded`); `SPEC:73` (the brief never says whether asking is allowed); `SPEC:172` (AC-C1 greps `src/superclaude/core` and excludes only `ccsession-tag`) versus `SPEC:147` (SA-2 allows an Orca mention "inside the contract file") and `SPEC:158` (P0 writes `WORKER-CONTRACT.md` and an Orca section in `HOW-WE-WORK.md`, both under `core`).
- Grading check: both need a guess (a worker takes the ask path; the new core text uses the exact `orca orchestration ...` wording). Neither is a stated text that harms.
- Recommendation: have the brief say "do not ask" for the gate-trigger runs, and add the contract file to AC-C1's exclusions or restrict its wording.
- Priority: Medium.

### F-9. MAJOR label, graded Medium. The task confidence gate does not say whether an explicit `--compliance` override clears it.
- Expert: Wiegers.
- Locations: `SPEC:121`; `INV-B:199` (the gate text offers "Override with `--compliance [tier]`").
- Grading check: undefined edge case (Boundary Table G5, last row). A brief that already passes the flag would still block.
- Recommendation: state that an explicit tier flag clears the gate.
- Priority: Low.

=== ARCHITECTURE ANALYSIS ===

- Fowler (interfaces): the core decision (Orca on top, commands unchanged units, one shared contract file, `SPEC:16`, `SPEC:52`) is sound and supported by `CAPS:97-103` (depth 1 forbids the alternative) and `CAPS:145-149` (standalone use). `--unattended` bundles five behaviors (gate defaults, outward-off, report write, wait splitting, mode flag) behind one switch. That is acceptable, and it is why F-4 and F-7 matter: the bundle only works if all five arrive together.
- Newman (versioning): the shared contract has no version field (N-5), while the workflow contract is already versioned 1.1 (`INV-B:272`). The contract file will evolve across four phases.
- Hohpe (message flow): the `ask`, `reply`, `check` and `worker_done` flow in WC-3, WC-5 and WC-12 matches `CAPS:58-67` and `CAPS:73-77`. One gap: a blocked command maps to `--outcome failed` (`SPEC:63`), which keeps the Task's dependents blocked (`CAPS:90`) and needs a `--retry-of` start; the spec does not say that is the path (see F-2).
- Nygard (failure modes): the readiness, nesting and silent-stall analysis in 1.4 is accurate against `CAPS:52`, `CAPS:129` and `CAPS:97-103`. Open: stale contract after a crash (F-2), heartbeat during unsplittable calls (F-5). A worker's own `failed` report does not trip the circuit breaker (`CAPS:80`), so a blocked-then-retry loop has no automatic stop; this is a note, not a finding, since the loop is the coordinator's.
- Hightower: no cloud-native concern beyond the above. The remote-worker choice is excluded (`SPEC:221`).

=== ADVERSARIAL ANALYSIS (Whittaker) ===

1. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 (`SPEC:62`)** fails when **`--unattended` is passed with no output directory**. Concrete attack: before, `/sc:analyze x --unattended`; the command must write `blocked` or `failed` to `<output-dir>/return-contract.yaml`, but there is no directory; after, no file exists, the worker reports `failed` by WC-5 with no reason for the coordinator to read. Severity: MAJOR label, Medium (F-1).
2. I can break this specification by **Divergence Attack**. The invariant at **WC-4 versus `SPEC:83` and `SPEC:92`** fails when **the coordinator passes `--output D` to adversarial**. Concrete attack: WC-4 says `D/return-contract.yaml`; the adversarial row says `D/adversarial/return-contract.yaml`; the coordinator reads the first, the command writes the second; step 4 (`test -s`) fails on a correct run. Severity: MAJOR label, Medium (F-1).
3. I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-5 (`SPEC:63`)** fails when **`status` holds `partial`**. Concrete attack: a sprint-style command finishes 1 of 5 pieces and writes `partial`; WC-5 sends `--outcome succeeded`; Orca marks the Task completed (`CAPS:77`) and its dependents become ready (`CAPS:90`). Severity: MAJOR label, Medium (F-6).
4. I can break this specification by **Sequence Attack**. The invariant at **P1 (`SPEC:159`) before P2 (`SPEC:160`)** fails when **a coordinator dispatches a command in between**. Concrete attack: after P1, `/sc:auggie-review <PR> --unattended` is accepted; the post-to-GitHub default is still on until P2; a review is posted although WC-9 says it is off. Severity: MAJOR label, Medium (F-4). Second attack: retry into the same directory (F-2).
5. I can break this specification by **Accumulation Attack**. The invariant at **AC-1.1 (`SPEC:195`)** fails when **the section count is accumulated across 37 commands**. Concrete attack: 37 sections expected, `load` contributes none, 36 exist, P1 never passes. Severity: CRITICAL (B-1).

## Quality assessment (0 to 10)

Clarity 7, Completeness 6, Testability 6, Consistency 6. The decision and evidence chain are strong and honest about gaps (`SPEC:41-45`, `SPEC:271-285`). The weak points are acceptance checks that do not match the rows they test, and the report-location rule.

## Consensus and disagreements

- Consensus: the architecture decision, the section 4 split and the standalone guarantees (section 5) are well supported by the inventories.
- Consensus: the single blocking item is a mechanical mismatch between AC-1.1/AC-1.2 and the `load` row.
- Disagreement flagged for the coordinator: whether FR-8 GAP rows are blocking regardless of the brief's sentence test (see Grading rules). I followed the brief.

## Blocking findings (open)

- B-1 (CRITICAL).

## Follow-up candidates (Medium and minor; none fails this review)

Medium: F-1 report location and missing directory; F-2 retry into a populated directory and stale contract; F-3 invocation mechanism and the AC-0.4 check; F-4 flag shipped before gate conversion; F-5 WC-10 coverage; F-6 status vocabulary and `partial`; F-7 pass-through to nested invocations; F-8 acceptance checks that cannot discriminate (AC-2.2, AC-C1); F-9 task override flag.

Minor notes:
- N-1. The evidence claim for E3 (`SPEC:23`) cites `invocation_method: "skill-direct"`, while 1.4(1) (`SPEC:43`) says the PR #329 run used an Agent-tool subagent and proves only the nested route; `CAPS:156` agrees with 1.4. `INV-A:35` still marks adversarial "proven", which the spec correctly does not repeat. The word "direct" carries two meanings.
- N-2. `README:31` is a rule for this planning run's workers, yet `SPEC:67` and `SPEC:133` use it as the basis for general outward-action policy.
- N-3. `SPEC:220` limits scope to defects that stop a command working as a worker, yet `SPEC:112` and `SPEC:149` fix the load usage line, which does not.
- N-4. `SPEC:240` recommends pr-submit stays coordinator-side (D3 a), but AC-1.1 (`SPEC:195`) and P1 (`SPEC:159`) count it among the commands that get the section.
- N-5. WC-4 lists fields as "at least" (`SPEC:62`) with no contract version field.
- N-6. `SPEC:59` cites about 45 s as the failure threshold; `CAPS:49` shows 45 s was the limit that test passed to `worker-start`, so the default 60 s leaves more room.
- N-7. The spec-panel row (`SPEC:120`) says the command lacks `--output`, while the command definition used for this review already has `--output`, `--report-dir` and an `## Unattended mode` section (`command.md:22-23,451-460`). The row may be stale; UNVERIFIED against the repo.
- N-8. SA-4 and AC-C5 (`SPEC:149`, `SPEC:176`) demand additive edits, but adding a flag to an existing Usage line removes a line in the diff. How to add flags additively is not stated.
- N-9. UNVERIFIED citations (not in the checkable evidence set): `CLAUDE.md:16,50,72-83,157,334,408`, `HOW-WE-WORK.md:171,249,254`, `install_core.py:4,13-24,33`, `pyproject.toml:38`, `Makefile:68-74`, `EVIDENCE.md:35-56`, the PR #329 files, and every `cmd/` and `sk/` line not quoted in an inventory. The spec's own claims of a second read (`SPEC:11`, `SPEC:285`) are also UNVERIFIED.

## Reviser brief

Blocking finding ids: B-1.
- Revise only text a blocking finding names. Here that is the `load` row (`SPEC:112`), P1 scope (`SPEC:159`), the `load` decision (`SPEC:265`), AC-1.1 (`SPEC:195`) and AC-1.2 (`SPEC:196`), as far as needed to make them agree.
- Add no rule, mechanism or section that no blocking finding calls for. F-1 to F-9 and N-1 to N-9 are not part of this revision.
- Each added paragraph or table cites its finding id (B-1).
- Report the candidate's byte size before and after the revision.

verdict: FAIL
