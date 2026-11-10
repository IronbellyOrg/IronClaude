review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (labelled whole-document audit, first review)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 60747 bytes, 295 lines
- Candidate sha256: `feaa1a31e42a8514d14628b790b646be58d5aee3914f33cd26e8e8f6a0037350`
- Baseline: none given and no `--re-review`, so this is a first review of the whole document (no `baseline: missing` note applies; neither flag was passed).
- Reviewer model actually used: claude-sonnet-5-5
- Prompt followed: FIRST-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full). Shared context read first: `.dev/orca-command-refactor/README.md:1-38`.
- Format: default `standard` is a YAML shape; this report uses the critique-mode grouped layout the command defines (`command.md:123`). `--unattended` was not passed, so the follow-up question in the section below is asked of the user.

## Coverage statement (what was and was not checked)

Covered:
- Every section of the candidate was read in full (spec lines 1-295).
- Checked against the inventories (the only checkable evidence): the 43-command split (INV-A:3 lists 21, INV-B:3 lists 22; spec section 3 has 10 + 27 + 6 = 43 distinct commands, and the A/B sides split 13+5+3 and 14+5+3, matching INV-B's "Needs-change (14)" at `commands-b.md:289`); the Orca facts the spec cites (`orca-capabilities.md` lines 44-46, 52, 58-68, 72-80, 86, 92, 97-103, 115-116, 128-130, 145-151, 155-161, 178-188 all say what the spec says they say); the verdicts for adversarial, brainstorm, cleanup-audit, index-repo, implement, cli-portify, cli-eval, reflect, release-split, tdd, troubleshoot, workflow, pr-submit, post-release, tasklist (`commands-a.md:35-55`, `commands-b.md:31-52`).
- Internal consistency of requirements WC-1..WC-12, SA-1..SA-6, phases P0-P4, acceptance checks and decisions D1-D5.

Not covered, marked UNVERIFIED:
- Every `cmd/...` and `sk/...` path:line the spec cites (for example `sk/sc-pr-submit-protocol/SKILL.md:37-39`, `sk/sc-implement-protocol/refs/qa.md:231-238`, `cmd/auggie-review.md:51-54`) is not in this workspace. I could confirm only that the inventories quote the same lines (for example `commands-b.md:90` for pr-submit, `commands-a.md:51` and `:66` for implement, `commands-a.md:60` for adversarial). The 11 re-reads (spec:11) and the "about 340 citations" validator claim (spec:294) are the spec's own attestations and cannot be checked here.
- The grep results the spec reports as run (spec:25, E5) and `src/superclaude/cli/install_core.py`, `Makefile`, `pyproject.toml`, `CLAUDE.md` line cites are UNVERIFIED.
- `orca-ide` and Orca guide text is checkable only through `orca-capabilities.md` quotes.

Experts (fixed order, requirements + architecture focus): Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker (always active), Newman, Hohpe. The Pipeline Dimensional Analysis heuristic does not trigger: the spec describes no multi-stage data flow whose item counts change. The only count in play, 43 = 10 + 27 + 6, conserves (spec:76, 78, 94, 127). `--focus correctness` was not requested, so there is no State Variable Registry.

## Grading summary

| ID | Severity label | Grade | Open? | Section |
|---|---|---|---|---|
| F-01 | MAJOR | blocking | open | P1 accepts `--unattended` on gate commands while the brief rule uses it from P1 |
| F-02 | MAJOR | blocking | open | AC-1.1 cannot pass for `/sc:load` |
| M-01 | MAJOR | Medium | follow-up | WC-3 vs D2(b) |
| M-02 | MAJOR | Medium | follow-up | contract "beside the file" vs WC-11 |
| M-03 | MAJOR | Medium | follow-up | fixed contract path vs "fresh dir" retry |
| M-04 | MAJOR | Medium | follow-up | `--unattended` inside quoted free text |
| M-05 | MAJOR | Medium | follow-up | AC-C5 vs usage-line edits |
| M-06 | MINOR-labelled MAJOR | Medium | follow-up | AC-C1 scope and strength |
| M-07 | MAJOR | Medium | follow-up | `partial` maps to `succeeded` |
| M-08 | MAJOR | Medium | follow-up | WC-10 rests on an unverified cadence |
| M-09 | MAJOR | Medium | follow-up | tasklist departs from the inventory with no Decision row |
| M-10 | MAJOR | Medium | follow-up | recommended D3(a) leaves counts and P1 text stale |
| M-11 | MAJOR | Medium | follow-up | "safety boundary" undefined in WC-3 |
| M-12 | MAJOR | Medium | follow-up | no acceptance check for WC-1, WC-3 ask path, WC-6, WC-12 |
| N-01..N-04 | MINOR | note | n/a | see notes |

## === REQUIREMENTS ANALYSIS ===

### F-01 (CRITICAL-adjacent MAJOR, blocking) Sequence attack: P1 makes `--unattended` available on commands whose gates only convert in P2-P4

- Expert: Wiegers (lead), Whittaker (Sequence Attack), Cockburn.
- Where: spec:159 (P1: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)", refusing only auggie-review, task, pr-submit, post-release), spec:73 (the coordinator brief includes `--unattended` "from P1 on"), spec:60 (WC-2: under `--unattended` the command never prompts), spec:44 (section 1.4 item 2: a command prompt is a silent stall with no `worker_done`), spec:160-162 (gate conversion lands in P2, P3, P4).
- Grading check: An implementer who follows the stated text as written builds, at the end of P1, `/sc:cleanup`, `/sc:improve`, `/sc:cli-eval`, `/sc:cli-portify`, `/sc:tdd`, `/sc:troubleshoot`, `/sc:roadmap`, `/sc:review-translation`, `/sc:implement` and about ten more that accept `--unattended` and still stop on their approval gates; section 2.3 then tells the coordinator to pass `--unattended` to every worker from P1 on; and the worker parks on a prompt nobody can answer, which is exactly what WC-2 forbids and section 1.4 item 2 calls the real failure mode. The text needs no further assumption: P1 names only four commands to refuse, and every other gated command falls under "accepted".
- I can break this specification by **Sequence Attack**. The invariant at **WC-2 (spec:60)** fails when **a phase boundary is crossed in the middle of the rollout**. Concrete attack: state after P1 = {cleanup: flag accepted, gate "Approval Required" unchanged}; coordinator brief per spec:73 = `/sc:cleanup <dir> --unattended --output <dir>`; worker reaches the approval step (`commands-a.md:43`); state after = worker waiting, no `worker_done`, `worker-show` `agentWait` non-null (spec:189). The P1 acceptance check AC-1.2 (spec:204) tests only the P1 commands, so nothing catches it.
- Recommendation: extend the P1 refusal rule (spec:159) from "outward default" commands to every command whose gate converts in a later phase, until that phase lands, and state in spec:73 that the brief uses `--unattended` for a command only once its phase has landed. This narrows the flag surface rather than adding a mechanism.
- Priority: High. Quality impact: Testability and Consistency, about +2.

### F-02 (MAJOR, blocking) AC-1.1 contradicts the `/sc:load` row (zero/empty attack)

- Expert: Adzic (lead), Wiegers, Crispin-style completeness.
- Where: spec:203 (AC-1.1: "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`"), spec:112 (load: report "none (see note)", resume "n/a", "use it as a step inside another worker's brief, not as its own Task"), spec:159 (P1 includes load for "usage line only"), spec:62 (WC-4 requires a contract on every outcome), spec:274 (Decision: no report file for load, "a report file would be an unrequested addition").
- Grading check: An implementer who follows the stated text as written builds a load edit that adds only a usage-line fix and no contract (spec:112, spec:274), and AC-1.1 then fails, because it requires a section naming `return-contract.yaml` in every 3.1-3.2 command; or builds a contract for load, which spec:274 forbids. Both stated texts cannot hold, and the acceptance criterion cannot pass under the row as written.
- Recommendation: narrow AC-1.1 to name load as the exception (or exclude it from the loop), so no new text is needed for load.
- Priority: High. Quality impact: Testability, about +1.

## Medium findings (listed under follow-up candidates; none triggers a revision)

### M-01 WC-3 forbids a relayed answer that D2(b) offers (Divergence attack)
- Experts: Wiegers, Whittaker.
- Where: spec:61 (a gate guarding a Ruling resolves as blocked "and no `ask` answer supplies it") vs spec:244 (D2(b): the coordinator answers the worker's `ask` with the person's words, recorded as the Ruling) and spec:217 (AC-4.1 "unless D2 allows a relayed one").
- Why Medium: D2 is an open user decision, so the conflict only bites if the user picks (b); it then needs a WC-3 edit the spec does not list.
- Recommendation: add to D2(b) that choosing it amends WC-3.

### M-02 Contract "beside the output file" collides under WC-11 (Accumulation attack)
- Experts: Fowler, Nygard.
- Where: spec:62 (for file-valued output options, tdd and init-lite, the contract "sits beside that file"), spec:87 and 90, spec:69 (WC-11: two workers in one worktree never write the same file).
- Attack: two parallel `/sc:tdd` workers with `--output docs/a.md` and `--output docs/b.md` both write `docs/return-contract.yaml`; the coordinator reads whichever finished last. Needs the coordinator to place two outputs in one directory, hence Medium.
- Recommendation: name the file after the output file (for example `<output-stem>.return-contract.yaml`).

### M-03 Fixed contract path known before dispatch vs "fresh dir" retry
- Experts: Newman (evolution), Nygard.
- Where: spec:62 (path known before dispatch from the directory the coordinator passed), spec:64 (WC-6 owner is "Command": "writes each run into a fresh output directory"), spec:73 (section 2.3 never says the coordinator passes a new directory per attempt), spec:214 (AC-3.2: with an existing `<dir>/.session-memory.md` and no resume flag the command "starts fresh").
- Attack: `worker-start --retry-of` reuses the same `--output <dir>`; a command that overwrites in place destroys the first attempt (the WC-6 goal), and one that creates its own subdirectory writes the contract somewhere the coordinator did not pass in `--report-path` beforehand. The spec leaves unsaid who creates the fresh directory.
- Recommendation: state in section 2.3 that the brief passes a new directory per attempt, and that a non-empty `--output` without a resume flag is refused or blocked.

### M-04 `--unattended` as a sentinel inside free text (Sentinel Collision attack)
- Experts: Whittaker, Wiegers.
- Where: spec:51 and 60 define the switch but not how it is recognised. Free-text commands (tdd, troubleshoot, research, spec-panel with quoted content, recommend) take user prose.
- Attack: `/sc:troubleshoot "the CLI rejects --unattended"` flips the command into unattended mode; the reverse (flag inside quotes ignored) is also unspecified. The real `/sc:spec-panel` definition already resolves this (`command.md:459`: only a standalone argument token outside quoted content), so the pattern exists but the shared contract does not state it.
- Recommendation: add one sentence to WC-2 or section 2.1: the switch counts only as a standalone token outside quoted arguments.

### M-05 AC-C5 cannot pass for flag additions on a Usage line
- Experts: Crispin, Wiegers.
- Where: spec:176 (AC-C5: no removed lines in command diffs unless a named defect fix) vs spec:149 (SA-4: edits are additive "new flags") and spec:159.
- Attack: adding `[--unattended]` to an existing one-line Usage block deletes and re-adds that line, tripping `grep -E '^-[^-]'`. The same check passes if the flag goes on a new Usage line, as `command.md:22-23` does, but the spec does not say so. Needs a guess about layout, hence Medium.
- Recommendation: say that new flags go on their own added line.

### M-06 AC-C1 greps beyond SA-2 and misses the spec's own spelling
- Experts: Whittaker, Fowler.
- Where: spec:172 and 181 (pattern is lowercase `orca(-ide)? (orchestration|worktree|terminal|agent)` over commands, skills, agents and core), spec:150 and 158 (P0 adds an Orca section to `HOW-WE-WORK.md` and a contract file under `core/`), spec:147 (SA-2 covers command, skill and agent files only).
- Issue: AC-C1 runs in P0 over the core files P0 itself edits, so its pass depends on the wording of those new files; and the spec writes `ORCA orchestration ...` in capitals (spec:167, 188), which the case-sensitive grep would not match.
- Recommendation: align AC-C1 scope with SA-2 and add `-i`.

### M-07 `partial` reported as `succeeded` can release dependent Tasks
- Experts: Fowler, Nygard, Hohpe.
- Where: spec:63 (WC-5) and spec:272 (Decision), with the Orca fact that a valid `worker_done` settles the Task automatically (`orca-capabilities.md:77`) and dependent Tasks are scheduled from the ready view (`orca-capabilities.md:86`).
- Attack: a Task whose command ended `partial` is marked complete, so a dependent Task (for example adversarial on troubleshoot reports, spec:39) becomes ready on an incomplete input. The spec's mitigation is the first sentence of the body, which Orca does not act on.
- Recommendation: state in section 2.3 that the coordinator reads the contract `status` before it releases dependents.

### M-08 WC-10's 4-minute rule rests on a cadence the inventory marks unverified
- Experts: Nygard, Newman.
- Where: spec:68 (WC-10), vs `orca-capabilities.md:130` ("cadence (every 5 minutes) comes from this worker's own preamble, not from a guide; UNVERIFIED whether Orca uses heartbeat age") and `orca-capabilities.md:182`. The UNVERIFIED list (spec:280-294) has no entry for this; item 12 (spec:292) covers only the pr-submit poll runtime.
- Effect: cli-eval and pr-submit are asked to change (spec:104, 114) for a liveness rule whose effect Orca may not have.
- Recommendation: add the unverified item and mark WC-10 advisory until it is resolved.

### M-09 tasklist departs from the inventory with no Decision row
- Experts: Fowler, Wiegers.
- Where: spec:122 (pass `--unattended` to each reflect so the headless auto-accept applies) and spec:88 (reflect `--remediate` auto-accepts under `--unattended`) vs `commands-b.md:46` verdict ("drop `--remediate` in 10.5; ready with `--no-reflect`") and `commands-b.md:295`. The Decisions table (spec:267-278) does not record the change.
- Effect: an unattended tasklist run starts an auto-accepted remediation chain inside the worker, which the inventory advised removing, with no recorded reason.
- Recommendation: add the Decision row, or follow the inventory.

### M-10 Recommended D3(a) leaves counts and P1 text stale
- Experts: Cockburn, Fowler.
- Where: spec:249 and 139 (D3(a): pr-submit stays with the coordinator or person), spec:76 and 127 (counts of 27 and 6), spec:114, spec:159 and 203 (P1 refusal and AC-1.1 still treat pr-submit as a changed worker command).
- Recommendation: state which count, section and AC apply under D3(a), the recommended option.

### M-11 "Safety boundary" in WC-3 is undefined
- Experts: Wiegers, Cockburn.
- Where: spec:61 (WC-3 carve-out for "a Ruling, an outward action or a safety boundary"). Rulings and outward actions are enumerated (D2, D4, WC-9); safety boundaries are not, though cli-eval's W0 confirmation (spec:104) and cli-portify's approval gates (spec:105) could fall on either side.
- Recommendation: list the gates in section 3 that the carve-out covers.

### M-12 No acceptance check for several requirements
- Experts: Adzic, Crispin.
- Where: spec:166-219. No AC exercises WC-1 (readiness fallback), WC-3's `ask` path (AC-2.2 tests only the blocked outcome), WC-6 (`--retry-of`), or WC-12 (`consumer_fenced`).
- Recommendation: add one live check each, or say these are covered by the P0 smoke runs.

## === ARCHITECTURE ANALYSIS ===

Assessed and found sound: the core decision (Orca above, commands as units; spec:13-45) is supported by the inventory evidence (depth 1 at `orca-capabilities.md:97-103`; `worker_done` bound to the dispatched pane at `:76`, `:150`; standalone failure without Orca at `:147`). The rejected alternative's reasons R1-R5 (spec:31-37) each trace to a checked capability line, and R1 correctly labels the enforcing call sites UNVERIFIED (spec:33; `orca-capabilities.md:103`). The honest evidence-strength section (spec:41-45) matches `commands-b.md:323` and `orca-capabilities.md:156`, and Phase 0 tests the decision first (spec:158, 202). The coordinator-only list (spec:127-139) matches `commands-a.md:90-92` and `commands-b.md:285-287`. The sole shared file with installed-path references follows the repo rule (spec:52, 273).

Findings above that belong to this bucket: M-03 (retry/evolution), M-07 (hand-off semantics), M-09 (shared-contract divergence), M-10 (decision/option consistency). No blocking architecture finding.

Whittaker, sequence/accumulation probes that did not break an invariant:
- Fixed-path commands (cleanup-audit, index-repo) are serialized by section 2.3 and AC-1.5 (spec:73, 207); `workflow` uses a fresh package each run (spec:92).
- A retry cannot trip Orca's circuit breaker by reporting `failed` (spec:272; `orca-capabilities.md:80`).
- Nesting: the tasklist-to-reflect fan-out sits inside the three-layer limit the inventory cites (spec:122; `commands-a.md:14`); depth arithmetic is not shown but is plausible (UNVERIFIED).

## Guard Condition Boundary Table

Guards in the candidate: G1 readiness limit (spec:59), G2 outcome mapping (spec:63), G3 wait-size rule (spec:68), G4 switch recognition (spec:51, 60), G5 P1 refusal list (spec:159), G6 fixed-path serialization (spec:73, 207). Classes left out are given with their reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 readiness | spec:59 | Zero/Empty | no pre-ready prompt | true | passes as written | OK |
| G1 readiness | spec:59 | Typical | 30 s fallback | true | passes (`EVIDENCE.md:45` via spec:59) | OK |
| G1 readiness | spec:59 | Maximum/Overflow | fallback above about 45 s | false | fails again (spec:59), but "well inside" is not a number and no AC checks it | GAP (M-12) |
| G2 outcome | spec:63 | Zero/Empty | report missing or empty | `failed` | specified (M9) | OK |
| G2 outcome | spec:63 | Typical | `succeeded` | `succeeded` | specified | OK |
| G2 outcome | spec:63 | Sentinel Value Match | `partial` | `succeeded` | specified, but dependents are released (M-07) | GAP |
| G2 outcome | spec:63 | Legitimate Edge Case | audit verdict FAIL with `status: succeeded` | `succeeded` | specified | OK |
| G3 wait size | spec:68 | Zero/Empty | no long wait | n/a | none needed | OK |
| G3 wait size | spec:68 | Maximum/Overflow | single wait of 4 to 5 minutes | true and false | the two clauses ("longer than 5" and "at most 4") disagree on 4-5 minutes | GAP (note N-03) |
| G4 switch | spec:51, 60 | Sentinel Value Match | `--unattended` inside quoted text | undefined | unspecified | GAP (M-04) |
| G5 refusal list | spec:159 | Legitimate Edge Case | gated command pre-P2 | accepted | stalls | GAP (F-01) |
| G5 refusal list | spec:159 | Typical | auggie-review in P1 | refused | specified | OK |
| G6 serialization | spec:73, 207 | Maximum/Overflow | second audit while first runs | blocked by the coordinator | specified (M13) | OK |
| AC-1.1 loop | spec:203 | Zero/Empty | load has no contract | assertion fails | contradicts spec:112 | GAP (F-02) |

Left out: One/Minimal for G1-G6 (no distinct behavior from Typical); Sentinel and Maximum classes for G1, G2 beyond those shown (no sentinel value exists). GAP rows are graded in the findings above: F-01 and F-02 name a concrete wrong outcome (blocking); the rest are Medium.

## Panel notes (non-finding)

- Fowler/Newman: contract file, flag, report name and four-value status are one coherent seam; the single shared installed file avoids duplicate rules.
- Hohpe: the exchange pattern (task brief in, contract file out, one `worker_done`) is clear; the gap is only M-07.
- Cockburn: primary actors (coordinator, worker session, person) are named per requirement; D1-D5 each give a recommendation.

## Notes (MINOR, never fail the review)

- N-01: All `cmd/` and `sk/` path:line citations are UNVERIFIED in this sandbox (see coverage). The inventories quote them consistently with the spec.
- N-02: The spec cites pr-submit's top-level rule at `sk/sc-pr-submit-protocol/SKILL.md:37-39` (spec:65) while `orca-capabilities.md:161` cites the installed copy at lines 47-49; the two files differ, so this is not a contradiction.
- N-03: WC-10 says a call "longer than 5 minutes" must be split into waits "of at most 4 minutes" (spec:68); a 4-5 minute wait satisfies the first clause but not the second. Use one threshold.
- N-04: The spec's own UNVERIFIED item 14 (spec:294) and spec:11 are self-attestations about citation checks and cannot serve as evidence in a review.

## Follow-up candidates

Medium: M-01, M-02, M-03, M-04, M-05, M-06, M-07, M-08, M-09, M-10, M-11, M-12.
Minor: N-01, N-02, N-03, N-04.

Question for the user (asked once for this loop; no issue has been created): open an issue for the follow-up candidates above, yes or no?

## Reviser brief

Blocking finding ids: F-01, F-02.

Contract (restating the Review Loop, bullet 6): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Medium and minor findings are not part of this brief and must not be edited. Do not award yourself a PASS.

verdict: FAIL
