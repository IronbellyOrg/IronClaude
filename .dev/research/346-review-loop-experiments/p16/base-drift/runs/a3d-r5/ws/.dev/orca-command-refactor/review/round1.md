review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: not applicable (first review; no `--re-review`, no `--baseline`)
- reviewer model actually used: claude-sonnet-5-5
- mode: critique; focus: requirements, architecture; `--unattended` not passed
- spec line numbers below are lines of the candidate; `INV-A`, `INV-B`, `CAPS` as defined at spec line 8-9.

## Coverage (what was and was not checked)

- Read in full: the candidate (285 lines), `README.md`, `inventory/commands-a.md`, `inventory/commands-b.md` (sections 1-60 and 105-116, 205-216, 268-323 closely; the rest skimmed), `inventory/orca-capabilities.md`.
- Mechanically checked: 60+ `INV-A:N`, `INV-B:N` and `CAPS:N` citations in the spec resolve to the line the spec says they support. I found no wrong inventory line.
- Counted: 10 + 27 + 6 = 43 commands; the phase lists in section 6 match the Phase column of sections 3.1 and 3.2 (P1 = 9 + 4 fixes, P2 = 15, P3 = 4, P4 = 3).
- UNVERIFIED (not checkable in this sandbox, which holds only the README, the spec and `inventory/`): every `cmd/...`, `sk/...`, `src/...`, `CLAUDE.md:N`, `EVIDENCE.md:N`, `.dev/codegraph-migration/...` and `/opt/Orca/...` citation, the spec's own grep results at E5 (line 25), and the claim at spec line 11 that 11 locations were re-read and at UNVERIFIED item 14 that about 340 citations were re-checked. I treated the inventories as the evidence, as the README instructs, and did not grade any finding on an unreachable source line.

## Panel (review order of the command)

Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower. Under `--focus requirements,architecture` the leads are Wiegers (requirements) and Fowler (architecture).

=== REQUIREMENTS ANALYSIS ===

### F-1 [MAJOR, blocking] The contract path rule (WC-4) contradicts the file-valued `--output` commands, so AC-2.3 cannot pass for them
- Experts: Wiegers (traceability), Adzic (no example), Whittaker (Divergence attack)
- Grading sentence: An implementer who follows the stated text as written builds a contract at `<output-dir>/return-contract.yaml` where `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)" (spec:62), and for `/sc:tdd` and `/sc:init-lite` the brief passes `--output <file>` (spec:87, 90); the contract path would be `<file>/return-contract.yaml`, which cannot exist, so the check "the WC-4 contract path" in the live check (spec:182, 183) and AC-2.3 (spec:201) cannot pass for tdd, and the "path known before dispatch" promise (spec:62, 73) is false.
- Evidence: WC-4 at spec:62; tdd and init-lite rows at spec:87, 90 (`--output <file>`; "the TDD at `--output`"); spec-panel row at spec:120 ("add `--output`", kind not stated); live check steps 3 and 4 at spec:182-183. Further commands in section 3.1 name a different contract location than WC-4 gives: adversarial `<output>/adversarial/return-contract.yaml` (spec:83), workflow `.dev/tasks/to-do/<id>/return-contract.yaml` with a generated `<id>` (spec:92; inventory `INV-B:272`), cleanup-audit `.claude-audit/pass<N>-summary.md` (spec:85). For these the coordinator brief (spec:73) passes no directory that the contract lands in.
- Recommendation: state one rule that covers both shapes, for example "the contract is `<dir>/return-contract.yaml` where `<dir>` is the `--output` directory, or the parent directory of a file-valued `--output`", and list the three or four commands whose fixed location differs. Narrow rather than add: one sentence in WC-4 plus the existing rows.
- Priority: High. Quality impact: acceptance checks for tdd, init-lite, spec-panel and workflow become executable.

### F-2 [CRITICAL, blocking] AC-1.1 requires an `## Unattended mode` section in commands that the spec elsewhere exempts or defers (count mismatch 37 expected, fewer real)
- Experts: Wiegers (consistency), Crispin (acceptance), Whittaker (Accumulation / Divergence), Fowler (dimensional analysis, FR-19)
- Grading sentence: An implementer who follows AC-1.1 as written (spec:195: "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`") builds that section into `/sc:load`, `/sc:pr-submit`, `/sc:implement` and `/sc:post-release` in Phase 1, and this is wrong because (a) the `/sc:load` row says "Report: none ... use it as a step inside another worker's brief, not as its own Task" (spec:112) and the Decisions row says "a report file would be an unrequested addition" (spec:265), so a section naming a contract contradicts both; (b) under the recommended D3(a) `/sc:pr-submit` is "Coordinator or person only ... no pr-submit changes in Phase 4" (spec:240) and spec:139 says it is a worker candidate "only if the user accepts D3", yet the P1 flag-acceptance rule (spec:159) and AC-1.1 include it, so Phases 0-3 "on the recommendations" (spec:225) produce an unattended mode for a command the recommendation says is not a worker; (c) the gate resolutions for implement, post-release and pr-submit depend on D2-D4 that Phase 4 waits for (spec:154, 162), so a Phase 1 section cannot state them.
- Quantity flow (see artifact below): 43 commands -> 37 in sections 3.1-3.2 -> AC-1.1 expects 37 sections; the spec's own text supports at most 33-34 in P1 (37 minus load, minus the 3 P4 commands whose gates await D2-D4) and 36 or fewer under D3(a).
- Recommendation: make AC-1.1 and the P1 sentence at spec:159 list the commands per phase (the same split as the Phase column), exclude `/sc:load`, and say the P4 commands get their section in Phase 4. This deletes an over-broad claim; it adds no mechanism.
- Priority: High. Quality impact: removes a Phase 1 acceptance test that fails by construction or forces an unwanted edit to a coordinator-side command.

### F-3 [MAJOR, blocking] AC-2.3 expects a successful happy path for `/sc:cli-portify`, but its row makes every approval gate end the run as blocked and defines no flag that supplies approval
- Experts: Cockburn (goal), Adzic (scenario), Whittaker (Sequence attack)
- Grading sentence: An implementer who follows the cli-portify row as written (spec:105: "each of the three approval gates resolves as blocked with the artifact to review named in the contract"; the only added flag is `--resume <contract>`) builds a command whose first unattended run always stops at the first approval gate with `status: blocked`, and this is wrong against AC-2.3 (spec:201: "Happy-path run per P2 command with every required flag in the brief ... 7.2 passes with `--outcome succeeded`") because no brief can contain a flag that approves a gate; the row never says whether a resumed run skips the gate it stopped at, so a run to completion is not reachable from the stated text.
- Evidence: spec:105; inventory `INV-A:45` (three always-on approvals, resume flag absent from the command), `INV-A:68`; WC-2(b) allows "a value the caller supplied as a flag" (spec:60) but the row picks (c) for all three gates.
- Recommendation: either name the flag or resume semantics that approves a gate already reviewed (for example "`--resume <contract>` counts as approval of the gate named in the contract"), or change AC-2.3 for cli-portify to expect `blocked` at each gate in turn. Narrowest fix: one clause in the cli-portify row.
- Priority: High. Quality impact: the command becomes completable by a coordinator.

=== ARCHITECTURE ANALYSIS ===

Architecture verdict: the core decision (coordinator on top, commands as units of work, flag-selected mode, shared contract file, no Orca call inside commands) is consistent with `CAPS:97-103`, `CAPS:145-150` and the inventories; I found no contradiction in section 1 or section 4. The findings below are all at the edges of the contract, none at the decision.

## Follow-up candidates (Medium and minor; none blocks, none appears in the Reviser brief)

### M-1 [Medium] AC-C1 can fail on the spec's own Phase 0 deliverables
- Experts: Fowler, Crispin
- AC-C1 (spec:172) greps `src/superclaude/core` for `orca(-ide) orchestration|worktree|terminal|agent` and must print nothing; SA-2 allows an Orca mention "inside the contract file" only as an example (spec:147), but Phase 0 adds an Orca section to `HOW-WE-WORK.md` (spec:158, SA-5 at spec:150), and E5 records that file contains no "orca" today (spec:25). Whether either file will contain a matching command line is not stated; the implementer must guess. Narrow AC-C1 to `commands skills agents`, or say the two core files must name Orca without that command pattern.

### M-2 [Medium] WC-9 turns on outward actions "only through the command's own explicit flag", but several affected commands have none
- Experts: Nygard (safety boundary), Wiegers
- WC-9 (spec:67). Only auggie-review has a flag (`--post-pr`, spec:100). For post-release (spec:113, "unless the brief authorizes them"), task `commit`/`push` (spec:121) and pr-submit (D3b) the flag is not named, and D4(a) says the coordinator "passes the command's explicit flag" (spec:245). The text leaves the authorization channel to the implementer; the safe default (off) still holds, so no wrong outcome follows from the text as written. Name the flag per command in P4, or state in WC-9 that those actions stay off until a flag is added.

### M-3 [Medium] `/sc:tasklist` under `--unattended` newly auto-accepts reflect remediation, and the nesting-limit claim is not established
- Experts: Fowler (count divergence), Hohpe, Nygard
- Spec:122 passes `--unattended` to each Stage 10.5 reflect "so the headless rule applies"; spec:88 makes `--remediate` follow the "headless auto-accept rule". Inventory B recommends the opposite remedy for tasklist: call reflect without `--remediate` (`INV-B:215`, `INV-B:295`), and records that an Orca worker is not `--print` (`INV-B:109`, `INV-B:310`). The spec's route means an unattended tasklist run starts the remediation handoff (a corrective `sc:workflow` package per phase) which no row of the brief authorizes (WC-9 covers outward actions, not extra local writes). The same row says the nested reflect "runs one layer below the worker, inside Claude Code's nesting limit (`INV-A:14`)", but `INV-B:209` and `INV-B:46` record the per-phase reflect spawning its own agents (worker -> reflect subagent -> reviewers -> adversarial advocates is more than one layer) and mark it UNVERIFIED. Prefer the inventory's narrower fix (no `--remediate` in 10.5 under `--unattended`) or state the extra writes and the depth analysis.

### M-4 [Medium] WC-11 (parallel-safe writes) conflicts with fixed output paths of ready commands
- Experts: Newman, Nygard
- WC-11 (spec:69) says default output paths carry a timestamp or slug. index-repo writes a fixed `PROJECT_INDEX.md` (spec:86), cleanup-audit a fixed `.claude-audit/` (spec:85, which concedes "one audit per worktree at a time"), init-lite a fixed default file (spec:87). Only cleanup-audit is acknowledged. Two index-repo workers in one worktree overwrite each other. Add the brief rule "one worker per fixed path" to section 2.3, or give index-repo an output flag in P1.

### M-5 [Medium] `reflect` and `tasklist` ordering inside P2 is unstated
- Experts: Hohpe, Crispin
- The tasklist row depends on the reflect `--unattended` change (spec:88, 122); both are P2 but no order is given, and AC-2.x checks them separately. State "reflect first" in section 6.

### M-6 [Medium] WC-3 re-invocation for commands whose resume is "fresh dir"
- Experts: Nygard, Gregory
- WC-3 (spec:61) lets the worker ask the coordinator, then "re-invoke or resume the command with the answer as a flag". For the 20+ commands whose Resume column says "fresh dir" (spec:99-125) a re-invocation repeats all work already done before the gate. No wrong outcome is stated, only cost. Say which commands gate before doing work.

### m-1 [minor] UNVERIFIED item 14 and the line-11 claim describe checks I could not reproduce (spec:11, 285). Fine as stated, flagged for the reader.
### m-2 [minor] Spec:76 says "27 needing a change" while the sections 3.1 "Small fix" column also lists changes for 10 ready commands; the sentence is accurate but a reader may sum 37 edited commands. 
### m-3 [minor] WC-1 (spec:59) has no owner or acceptance check beyond the generic `state: ready` in step 1 of 7.2.
### m-4 [minor] D1 option (b) (spec:229) and UNVERIFIED item 13 repeat the same fact; one could be dropped.

## Mandatory artifacts

### Guard Condition Boundary Table
Guards found in the spec: G1 WC-5 outcome mapping (status vs `--outcome`), G2 WC-10 wait-size rule (heartbeat 5 min / wait 4 min), G3 WC-8 and R1 nesting depth (1), G4 WC-1 readiness limit (60 s; wrapper fallback 30 s), G5 task confidence guard `< 0.70` (spec:121). The One/Minimal and Overflow classes are left out where they cannot occur, with the reason in the Specified Behavior cell.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G1 outcome mapping | WC-5 (spec:63) | Zero/Empty | no report file exists | `failed` branch | `--outcome failed` ("or no report exists") | OK |
| G1 outcome mapping | WC-5 | Typical | `status: succeeded` | `succeeded` branch | `--outcome succeeded` | OK |
| G1 outcome mapping | WC-5 | Legitimate Edge Case | `status: partial` / audit verdict FAIL | `succeeded` branch | `--outcome succeeded`, body states status (spec:63, 263) | OK |
| G1 outcome mapping | WC-5 / WC-4 | Sentinel Value Match | report exists but `status` is outside the four values (7.2 step 4 asserts membership, spec:183) | not mapped | WC-5 gives no outcome for an unknown status | GAP (Medium; the check in 7.2 catches it, no stated behavior) |
| G2 wait size | WC-10 (spec:68) | Zero/Empty | wait of 0 s | n/a | left out: a zero wait cannot block a heartbeat | OK |
| G2 wait size | WC-10 | Typical | 3 min wait | within 4 min | heartbeat between waits | OK |
| G2 wait size | WC-10 | Maximum/Overflow | single call of 3600 s (cli-eval, spec:104) | exceeds 4 min | must be split into waits of at most 4 min | OK |
| G2 wait size | WC-10 | Legitimate Edge Case | exactly 4 min and a 5 min cadence | within margin | allowed (Decisions, spec:266) | OK |
| G3 depth | WC-8 / R1 (spec:33, 66) | Typical | command calls `worker-start` at depth 1 | refused (`nested_worker_depth_exceeded`) | forbidden; refusal presumed (UNVERIFIED call sites, spec:33) | OK |
| G3 depth | WC-8 | Legitimate Edge Case | depth setting raised by the user | guard off | D5 keeps depth 1; behavior when raised is "would break R1's protection" (spec:252) | OK |
| G4 readiness | WC-1 (spec:59) | Typical | fallback 30 s | passes | start succeeds in 34 s (EVIDENCE.md:45 via CAPS:49) | OK |
| G4 readiness | WC-1 | Maximum/Overflow | fallback above about 45 s | fails | fails at `agent_readiness` (CAPS:49) | OK |
| G4 readiness | WC-1 | Legitimate Edge Case | `--timeout-ms` raised | passes | "raisable"; upper bound UNVERIFIED (CAPS:54) | OK |
| G5 confidence | task row (spec:121) | Typical | 0.69 | true | blocked | OK |
| G5 confidence | task row | Legitimate Edge Case | exactly 0.70 | false | the row says "below 0.70" resolves blocked; the 0.70-0.89 band keeps today's behavior (not restated) | GAP (Medium; today's text governs, not restated) |
| G5 confidence | task row | Zero/Empty | no confidence value computed | undefined | unspecified | GAP (Medium; no concrete wrong outcome follows) |

FR-8/FR-9 grading: none of the three GAP entries names a concrete wrong outcome or a safety-boundary risk, so each is Medium under `follow-up candidates` (recorded here as M-7).

### M-7 [Medium] Boundary-table GAPs
- Unknown `status` value in WC-5 mapping; exactly-0.70 and missing confidence in the task row. Add one sentence each, or leave to the commands' own text.

### Quantity Flow Diagram (Pipeline Dimensional Analysis, triggered: multi-stage flow with count change)

```text
[Commands in cmd/: 43] --> [Inventory split: 10 ready + 27 change + 6 coordinator-only]
                                  |
                                  v
                [Worker-capable: 37 (spec:76, 3.1 + 3.2)]
                                  |
          +-----------------------+--------------------------+
          v                       v                          v
 [P1 sections written: 37?]   [P2: 15 commands]        [P4: 3 commands wait on D2-D4]
 [AC-1.1 expects 37 sections]  [AC-2.x per gate]        [load: exempt (spec:112,265)]
          |
          +--> real P1 sections <= 37 - 1 (load) - 3 (P4, gates unknown) = 33 ; 36 or fewer under D3(a)
          +--> Consumer AC-1.1: expects 37  <-- MISMATCH (F-2)
```

### Whittaker attacks (selected)
- Divergence Attack on F-1: the invariant at WC-4 ("contract in `<output-dir>`") fails when `--output` names a file. Concrete attack: brief `/sc:tdd "X" --unattended --output .dev/tdd/x.md`; the command derives `.dev/tdd/x.md/return-contract.yaml`; before: no such path; after: the write errors, the worker has no report, `--outcome failed`.
- Sequence Attack on F-3: the invariant at the cli-portify row (gate then resume) fails when the resumed run reaches the next gate. Concrete attack: run 1 stops at gate 1 (blocked); run 2 `--resume` is not specified to pass gate 1; it stops again; the loop never reaches delivery.
- Accumulation Attack on F-2: AC-1.1 counts 37 required sections; the exempt/deferred commands reduce the real count; the test fails with 3-4 missing.

### Downstream propagation
GAP entries G1/Sentinel, G5/edge and G5/Zero are propagated as invariant candidates for `sc:adversarial` AD-1 (all Medium).

## Blocking findings (open): F-1, F-2, F-3

Follow-up candidates (not asked to the user in this sandbox run): M-1, M-2, M-3, M-4, M-5, M-6, M-7, m-1, m-2, m-3, m-4. The session that runs the review asks once per loop whether to open an issue for them; no issue was created.

## Reviser brief

Repair only the blocking findings F-1, F-2, F-3 in the revised candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Revise only text a blocking finding names. Add no rule, mechanism or section that a listed finding does not call for, and cite the finding id on every added paragraph or table. Prefer deleting or narrowing text over adding when the requirements are still met. Report the byte size of the candidate before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone, including when a brief says "apply all findings". Return the candidate once and do not award yourself a PASS.

verdict: FAIL
