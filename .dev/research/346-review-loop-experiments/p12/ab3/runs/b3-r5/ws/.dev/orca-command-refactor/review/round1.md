review: 1 of 3

# /sc:spec-panel critique: orca-worker-contract-spec.md

## Header

| Item | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| Prompt followed | FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full) |
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 285 lines, 57763 bytes |
| Candidate sha256 | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` |
| Baseline | not given (first review; no `--re-review`, no `--baseline`) |
| Reviewer model | claude-sonnet-5-5 (Sonnet 5.5) |
| Mode and iterations | critique, one review; the Improve step (Behavioral Flow step 6) was not run because the brief assigns only this report file and the command forbids editing the spec without consent |
| Brief clauses overridden | none |
| Citation keys | `S:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = the three files under `.dev/orca-command-refactor/inventory/`; `README:N` = `.dev/orca-command-refactor/README.md`; `CMD:N` = the `command.md` definition in the sandbox. A citation to a file outside the workspace (`src/superclaude/...`, `CLAUDE.md`, `EVIDENCE.md`, Orca guides) is UNVERIFIED unless a workspace inventory line quotes it. |

Panel, in review order: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower (CMD:103-113). Focus experts: Wiegers (lead), Adzic, Cockburn for requirements; Fowler (lead), Newman, Hohpe, Nygard for architecture (CMD:133,144).

## What was covered

- Read in full: the candidate (S:1-285), the README (README:1-38), all three inventories (INV-A:1-120, INV-B:1-323, CAPS:1-188), the command definition and the loop prompts file.
- Checked against workspace evidence: every `INV-A`, `INV-B`, `CAPS` and `README` citation in sections 1-2 and the cross-references of section 3 (spot check of every row's inventory lines); the 10 / 27 / 6 partition and the per-phase counts; the internal consistency of WC-1..WC-12, SA-1..SA-6, section 6 (phases), section 7 (acceptance checks) and section 9 (decisions).
- Not checkable here (UNVERIFIED): every `src/superclaude/...` line number (S:83-125 cite them directly), `CLAUDE.md:N` citations, `EVIDENCE.md`, the codegraph-migration README and return contracts, the grep results quoted for E5 (S:25), and the "about 340 citations re-read" claim (S:285). They are accepted only where an inventory line quotes the same text.
- Mandatory artifacts produced: Guard Condition Boundary Table (guards exist), Quantity Flow Diagram (the 43-command partition is a multi-stage flow with count divergence). The State Variable Registry is not produced because `--focus correctness` was not requested.

## Panel result (consolidated)

Total findings: 1 blocking, 13 Medium, 5 minor. The spec's central decision (Orca coordinates, commands stay units of work) is supported by the inventories and its evidence statement is honest about the missing end-to-end run (S:43). The defect that blocks is a gap between the rollout plan and its own first acceptance gate.

## === REQUIREMENTS ANALYSIS ===

### F1 BLOCKING (CRITICAL, dimensional mismatch) Phase 1 gate asserts 37 commands, the plan assigns 9 to Phase 1
- Experts: Wiegers (traceability), Fowler (count annotation), Whittaker (divergence attack). Priority: High.
- Stated texts:
  - S:159 (P1 scope): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2".
  - S:195 (AC-1.1): the test "asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
  - S:154 and S:167: "Later phases do not start until the earlier phase's checks in section 7 pass" and "A phase passes only when every check in its block ... passes".
  - Against it: the per-row Phase column puts implement (S:109), post-release (S:113) and pr-submit (S:114) in P4, and S:154 and S:162 say Phase 4 "waits for answers to D2-D4". D3(a), the recommendation, says "no pr-submit changes in Phase 4" (S:240). load has "Report: none" (S:112), so a section "naming `return-contract.yaml`" has nothing to name.
- Wrong outcome: An implementer who follows the stated text as written adds an `## Unattended mode` section (and the flag) to pr-submit, implement, post-release and the P2/P3 commands during Phase 1, or leaves them out and fails AC-1.1. The first reading edits the three commands whose design depends on user decisions that S:154 says are not yet answered, and contradicts D3(a). The second reading makes AC-1.1 unpassable, and because later phases may not start until it passes (S:154), Phases 2-4 never start. Both outcomes are wrong, and the cause is the two stated texts, not a guess.
- Count trace (see Quantity Flow Diagram): the 3.2 Phase column sums to 9 (P1) + 11 (P2) + 4 (P3) + 3 (P4) = 27; the P1 row names 9 commands from 3.2 plus fixes to 4 ready commands (S:159); AC-1.1 and the P1 flag sentence consume 37 (10 + 27).
- Recommendation: narrow AC-1.1 and the S:159 flag sentence to the commands the Phase column assigns to P1 (the nine named at S:159 plus the section 3.1 fixes), and state that a later phase adds the section for its own commands. Delete rather than add: no new mechanism is needed.
- Quality impact: Testability 3/10 for the rollout plan until fixed.

### F2 Medium: AC-0.4 cannot pass step 3 for commands that write no contract yet
- Experts: Adzic, Crispin. Priority: Medium.
- S:182 (step 3 pass: "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path") versus S:194 (AC-0.4: "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1"). Only step 4 is relaxed. For `/sc:troubleshoot` the existing report is `REPORT.md` and a contract exists only with `--caller task-unified` (INV-B:242), so step 3's contract conditions have no object in Phase 0. S:194 adds "a failure here reopens section 1", so a literal reading would reopen the core decision on a check that cannot pass.
- Why Medium: the sentence needs a guess that the implementer reads the step-3 contract clauses literally rather than substituting the existing report as step 4 does.
- Recommendation: say that in P0 steps 3 and 4 both use the command's existing report file.

### F3 Medium: WC-4's path rule disagrees with the paths in section 3 rows
- Experts: Wiegers, Cockburn, Newman. Priority: Medium.
- S:62 fixes the file at `<output-dir>/return-contract.yaml`, "known before dispatch". S:83 and S:198 (AC-1.4) put adversarial's contract at `<output>/adversarial/return-contract.yaml`, one level below the directory the coordinator passes. S:92 keeps workflow's contract at `.dev/tasks/to-do/<id>/return-contract.yaml`, where `<id>` is generated by the skill (INV-B:272), so it is not known before dispatch. S:92 also says to write the contract "for pre-creation STOPs too", but a pre-creation STOP has no package directory yet (INV-B:272, "Not written for pre-creation STOPs"), and no other location is stated.
- Why Medium: an undefined location, not a stated text that does harm; an implementer must invent the path.
- Recommendation: state per command whether WC-4 or its existing path wins, and give workflow's pre-creation STOP a location (for example the coordinator's output directory).

### F4 Medium: WC-6 "fresh output directory" conflicts with WC-4, and retries can read a stale contract
- Experts: Nygard, Whittaker (Sequence attack). Priority: Medium.
- S:64 says a command without a resume flag "writes each run into a fresh output directory"; most S:99-125 rows say "fresh dir". S:62 requires the contract path to be known before dispatch. If the command creates the fresh directory, the path is unknown; if the coordinator passes a new `--output` per attempt, S:73 (section 2.3) never tells it to, and a retry that reuses the old directory finds attempt 1's `return-contract.yaml`. S:63 says "or no report exists" maps to failed, so a stale `succeeded` report is read as success when attempt 2 dies before writing.
- Recommendation: add to section 2.3 that the brief passes a new output directory for every attempt including `--retry-of`, and that the coordinator reads the contract only from that directory.

### F5 Medium: unattended run with no output directory is undefined
- Expert: Whittaker (Zero/Empty attack). Priority: Medium.
- S:62 defines the contract path from "the directory the coordinator passed" and S:73 puts the duty on the coordinator, but no row says what a command does under `--unattended` when `--output` is absent or unwritable. The rows at S:99, S:101, S:106, S:107, S:111, S:123 add `--output` as a new flag and are silent. WC-4 says the contract is written "including stops before any other output exists", which presupposes a writable directory.
- Recommendation: one sentence in WC-4: no usable output directory means print `status: blocked` with the reason in chat and stop (the real `/sc:spec-panel` command definition refuses before any work in that case, CMD:460).

### F6 Medium: section 2.3 tells the coordinator to pass `--unattended` before any command accepts it
- Experts: Wiegers, Adzic. Priority: Medium.
- S:73 requires the brief to state "the exact command line including `--unattended`". S:79 says the 10 ready commands run "now" with the section 3.1 flags, which do not include `--unattended` (S:83-92), and S:159 adds the flag in Phase 1. AC-0.4 (S:194) correctly omits it. For Phases 0 (and per row, 2-4) the flag is unknown to the command, and the spec does not say what an unrecognised `--unattended` does.
- Recommendation: say that `--unattended` belongs in the brief only for commands whose phase has landed.

### F7 Medium: WC-9 "paid external run" is undefined and can switch off commands the rows keep
- Experts: Wiegers, Hightower. Priority: Medium.
- S:67 turns off any default that "calls a paid external run" under `--unattended`. Web search through Tavily is a paid API in research (INV-B:134), review-translation (INV-B:144) and recommend `--plugin` (INV-B:104), yet S:116 makes `--unattended` pin research's planning strategy and run it. Neither a definition nor a list of covered calls is given.
- Why Medium: needs a guess whether web search counts.
- Recommendation: replace the phrase with a closed list taken from the inventories' field (f) (real-model proxy runs, installs, VM provisioning).

### F8 Medium: acceptance coverage is missing for WC-1, WC-3 and WC-12
- Experts: Crispin, Gregory. Priority: Medium.
- No AC in S:170-210 tests WC-1 (no prompt before ready), WC-3 (question goes to the coordinator, resume by message ID) or WC-12 (`check` before `worker_done`, `consumer_fenced` handling). AC-2.2 (S:200) checks only that `agentWait` is never non-null and does not test that `ask` was used; WC-3 says the worker "may" ask (S:61), so a gate that resolves as blocked can end `failed` or, after a coordinator answer, `succeeded`, and AC-2.2 expects `failed` unconditionally.
- Recommendation: state in AC-2.2 that the gate-trigger run uses a brief that forbids `ask`, or accept either outcome.

## === ARCHITECTURE ANALYSIS ===

### F9 Medium: WC-10 rests on an unverified liveness effect and cannot apply to Agent-tool waits
- Experts: Nygard, Hightower, Fowler. Priority: Medium.
- S:68 requires a heartbeat every 5 minutes and splitting any single blocking tool call over 5 minutes into waits of at most 4 minutes. The cadence comes from one worker's preamble (CAPS:130) and whether heartbeat age affects liveness is UNVERIFIED (CAPS:130, CAPS:182 item 7); S:271-285 omits that item. Separately, a command's own Agent-tool fan-out (tdd, post-release, troubleshoot Tier 2, cleanup-audit: S:90, S:113, S:91, S:85) blocks the top-level session for one tool call that cannot be split, and WC-7 (S:65) forbids subagents from heartbeating. The text covers "a poll wait, a long eval" only by example; the general sentence cannot be satisfied for these commands. AC-4.3 (S:210) requires "no single tool call exceeds 240 s" while WC-10 only triggers above 300 s, so a 270 s call passes WC-10 and fails AC-4.3.
- Recommendation: add heartbeat-age effect to the UNVERIFIED list, scope WC-10 to Bash waits, and align the 240 s and 300 s thresholds.

### F10 Medium: AC-C1 contradicts the SA-2 allowance and the Phase 0 deliverables
- Experts: Fowler, Newman. Priority: Medium.
- S:147 (SA-2) allows a mention of Orca "as an example of a caller's question channel inside the contract file"; S:52 and S:158 put that file in `src/superclaude/core/`, and Phase 0 adds an Orca section to `HOW-WE-WORK.md` (S:158), also in `core/`, which today has zero mentions (S:25). AC-C1 (S:172) greps `src/superclaude/core` for `orca(-ide)? (orchestration|worktree|terminal|agent)` and exempts only `skills/ccsession-tag/`, with pass condition "prints nothing", and it is a common check for every phase including P0 (S:167). A contract file or routing section that names `orca orchestration ask` fails Phase 0.
- Why Medium: needs a guess that the implementer writes the literal command string.
- Recommendation: exempt the two named core files in AC-C1, or forbid the literal command string in them.

### F11 Medium: AC-C5 conflicts with SA-4's "new flags"
- Experts: Fowler, Crispin. Priority: Medium.
- S:149 (SA-4) calls adding "new flags" additive; S:176 (AC-C5) fails any removed line (`^-[^-]`) in an edited command. A new flag is normally added to the command's existing Usage line, which shows as a removed line. S:176 exempts only "a named defect fix".
- Recommendation: say where a new flag is documented (a new line, or only in the `## Unattended mode` section).

### F12 Medium: `/sc:tasklist` under `--unattended` leaves reflect's HALT items unresolved
- Experts: Nygard, Whittaker (Divergence attack). Priority: Medium.
- S:122 passes `--unattended` to each reflect so "the headless rule applies". INV-B:209 says Stage 10.5's `needs_human_decision` items HALT, and the headless rule is described only as auto-accepting auto-fixable registers (INV-B:109). Which of the three WC-2 resolutions (default, flag, blocked) applies to a HALT item is not stated, and S:151 (SA-6) only promises the headless rule is reused. A stall here is the failure the spec exists to prevent.
- Recommendation: add one clause to the tasklist row: a HALT item resolves as `blocked`.

### F13 Medium: section 4 states a blanket rule that D3 and D4 contradict
- Experts: Fowler, Cockburn. Priority: Low-Medium.
- S:133 (git row): "workers make no commits or pushes". D4(a) (S:245), D3(b) (S:241) and the P4 rows (S:113-114) let a worker commit, push or open a PR when the brief authorises it. The sentence is not an operative requirement, but it is the only statement of the coordinator-side rule.
- Recommendation: replace with "unless authorised under D4".

### F14 Medium (UNVERIFIED): the 43-command partition is not tied to a directory listing
- Experts: Wiegers, Gregory. Priority: Low.
- S:76 asserts "The 43 commands in `cmd/`" and derives it from the two inventories' scope lists (INV-A:3, INV-B:3). No `ls` or count of `src/superclaude/commands/` appears in S:1-285 or the inventories; E5's grep (S:25) is the only directory-level evidence and it is UNVERIFIED here. This session's own command listing shows names (graph, impact, issue) that appear in neither inventory; whether they are in `cmd/` at the candidate's ref cannot be checked in the workspace.
- Recommendation: record the directory count as an AC or as an UNVERIFIED item.

## Minor notes (never fail the review)

- N1 (Newman): the WC-4 minimum fields (S:62) carry no contract version, while workflow's contract is versioned 1.1 (INV-B:272); two sources can drift.
- N2 (Cockburn): S:67 and S:133 cite `README:31`, a rule for this planning run, as evidence for a product requirement; it supports neither.
- N3 (Wiegers): S:285 (item 14) is a verification claim placed under "UNVERIFIED items", and S:11 says every other section-3 line is "carried ... without a second read", which item 14 contradicts.
- N4 (Hohpe): WORKER-CONTRACT.md is both what each command reads and the home of the coordinator brief template (S:52, S:158); every unattended run loads coordinator-only text.
- N5 (Wiegers): S:59 (WC-1) says "well inside" the 60 s limit with no number, although CAPS:49 shows 30 s passing and about 45 s failing at a 45 s limit.

## Guard Condition Boundary Table

Guards identified: G1 readiness fallback (S:59), G2 wait split and heartbeat (S:68), G3 output directory (S:62), G4 outcome mapping (S:63), G5 task confidence (S:121), G6 `ask` timeout (S:61), G7 pr-submit `--monitor` (S:114). The Maximum, Sentinel and Edge classes are omitted where they cannot occur, with one-line reasons below the table. All cells are populated.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 fallback timer | S:59 WC-1 | Zero/Empty | no fallback timer | prompt blocks | "must fall back on its own"; the missing timer breaks the requirement, which the text forbids | OK |
| G1 fallback timer | S:59 WC-1 | Typical | 30 s | true | passes (CAPS:49 quoting EVIDENCE:45) | OK |
| G1 fallback timer | S:59 WC-1 | Maximum/Overflow | 45 s or more | false | "well inside" with no number; CAPS:49 shows failure at about 45 s with a 45 s limit | GAP |
| G1 fallback timer | S:59 WC-1 | Legitimate Edge Case | coordinator raises `--timeout-ms` | changes | CAPS:45 allows it; the spec's "default 60 s" does not say what "well inside" then means | GAP |
| G2 wait split | S:68 WC-10 | Typical | 3 min wait | false (no split) | no split needed | OK |
| G2 wait split | S:68 WC-10 | One/Minimal | exactly 4 min | n/a | "waits of at most 4 minutes" | OK |
| G2 wait split | S:68 WC-10 | Legitimate Edge Case | 4.5 min wait | false (trigger is above 5 min) | allowed by WC-10, rejected by AC-4.3 (S:210, 240 s) | GAP |
| G2 wait split | S:68 WC-10 | Maximum/Overflow | 3600 s eval | true | split into waits of at most 4 min (S:104) | OK |
| G2 wait split | S:68 WC-10 | Maximum/Overflow | Agent-tool call over 5 min | true | no split possible; WC-7 forbids subagent heartbeats; unspecified | GAP |
| G3 output dir | S:62 WC-4 | Zero/Empty | `--output` absent under `--unattended` | n/a | unspecified (F5) | GAP |
| G3 output dir | S:62 WC-4 | Typical | writable directory passed | true | contract written on every outcome | OK |
| G3 output dir | S:62 WC-4 | Legitimate Edge Case | workflow pre-creation STOP | no package dir | contract "for pre-creation STOPs too" (S:92), location unstated (F3) | GAP |
| G3 output dir | S:62 WC-4 | Legitimate Edge Case | retry into a used directory | stale contract present | unspecified (F4) | GAP |
| G4 outcome map | S:63 WC-5 | Typical | `status: succeeded` | true | `--outcome succeeded` | OK |
| G4 outcome map | S:63 WC-5 | Legitimate Edge Case | `partial`; audit verdict FAIL | true | `succeeded`, first sentence names the status | OK |
| G4 outcome map | S:63 WC-5 | Legitimate Edge Case | `blocked` | true | `--outcome failed` | OK |
| G4 outcome map | S:63 WC-5 | Sentinel Value Match | status outside the four values, or file unparseable | n/a | only "no report exists" is mapped; AC step 4 (S:183) checks the set but WC-5 is silent | GAP |
| G5 confidence | S:121 | Zero/Empty | 0.0 | true | blocked | OK |
| G5 confidence | S:121 | Sentinel Value Match | exactly 0.70 | false | not below 0.70, proceeds | OK |
| G6 `ask` timeout | S:61 WC-3 | Typical | one timeout | n/a | resume the same message ID (S:61) | OK |
| G6 `ask` timeout | S:61 WC-3 | Maximum/Overflow | repeated timeouts, no answer ever | n/a | no cap or fallback to `blocked`; a silent stall remains | GAP |
| G7 `--monitor` | S:114 | Typical | 3 | false | runs | OK |
| G7 `--monitor` | S:114 | Sentinel Value Match | 1 | true | refused under `--unattended` | OK |

Omitted classes: G1 One/Minimal (a 1 s fallback is a Typical case); G4 Zero/Empty and Maximum (no numeric input); G5 Maximum (1.0 is Typical); G6 Zero/Empty (a 0 ms timeout is the library default, UNVERIFIED, CAPS:68); G7 `--monitor` 0 and 2 (behaviour under `--unattended` is not stated in S:114 and the pr-submit skill is not readable in the workspace, UNVERIFIED).

GAP entries G1 (two), G2 (two), G3, G4, G6 are graded Medium: none names a concrete wrong outcome without a guess. The GAP at G3 (retry, stale contract) appears as F4.

## Quantity Flow Diagram

```text
[Source: 43 commands (INV-A 21 + INV-B 22)]
   --> [Classify: INV verdicts]
        --> ready 10 (A 5 + B 5)               --> S:3.1 (10)   [consumer: AC-1.1 expects 10]
        --> needs-change 27 (A 13 + B 14)      --> S:3.2 (27)
        --> coordinator-only 6 (A 3 + B 3)     --> S:4 (6)      [consumer: AC-1.1 expects 0 sections]
   --> [Phase split of the 27 (S:3.2 Phase column)]
        P1 9 | P2 11 | P3 4 | P4 3                               (sum 27, conserved)
   --> [P2 row (S:160) adds 4 ready commands]  P2 total 15
   --> [P1 row (S:159) flag/section consumer: "every command in 3.1 and 3.2" = 37]  <-- MISMATCH
   --> [AC-1.1 (S:195) consumer: 37 sections at the end of P1, phase work done = 9 + 4 fixes]  <-- MISMATCH
```

Divergence: the Phase column conserves 27, but the Phase 1 flag sentence and AC-1.1 consume 37 where Phase 1 handles 9 (plus 4 small fixes). Finding F1.

## Adversarial analysis (Whittaker)

- I can break this specification by **Divergence Attack**. The invariant at **S:195 (AC-1.1) and S:159 (P1 scope)** fails when **the Phase column assigns pr-submit, implement and post-release to P4 (S:109, S:113, S:114) and S:154 holds Phase 4 until D2-D4 are answered**. Concrete attack: before = 0 sections; P1 completes the nine commands plus four fixes = 13; AC-1.1 requires 37; the test fails; later phases may not start (S:154). Finding F1.
- I can break this specification by **Sequence Attack**. The invariant at **S:63-64 (WC-5, WC-6)** fails when **a retry worker reuses the first attempt's output directory and dies before writing**. Concrete attack: attempt 1 writes `status: succeeded`, the coordinator retries with the same `--output`, attempt 2 stops at startup; the old file exists, WC-5 maps "report exists, succeeded" to `--outcome succeeded` for a run that produced nothing. Finding F4.
- I can break this specification by **Zero/Empty Attack**. The invariant at **S:62 (WC-4)** fails when **the brief omits the output directory**. Concrete attack: `/sc:analyze` with `--unattended` and no `--output` has no contract path; "written on every outcome" has no place to write. Finding F5.
- I can break this specification by **Accumulation Attack**. The invariant at **S:68 (WC-10)** fails when **one tool call runs between 240 s and 300 s, or an Agent-tool call runs longer than 300 s**. Concrete attack: tdd Tier 3 fan-out blocks the top-level session for 12 minutes; no heartbeat can be sent and WC-10 offers no split. Finding F9.
- I can break this specification by **Sentinel Collision Attack**. The invariant at **S:63 (WC-5)** fails when **a command writes `status: blocked` and the worker maps it to `--outcome failed`**. Concrete attack: Orca marks the Task `failed`, so its dependents stay blocked until a `--retry-of` replacement completes (CAPS:90); the spec does not say that a coordinator answer to a blocked question starts a retry rather than a new Task. Medium, recorded here, not a finding id.

## Follow-up candidates (Medium and minor; none triggers a revision)

F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, F13, F14; notes N1-N5; the Sentinel Collision note above. The review session asks the user once per loop whether to open an issue for these (CMD:260); this worker cannot ask, so no issue was created and none is requested here.

## Reviser brief

Blocking finding ids: F1.

Rules for the reviser (restating CMD:263; the reviser reads this report, not the command):
- Revise only text a blocking finding names: S:159 (the flag sentence of the P1 row) and S:195 (AC-1.1).
- Add no rule, mechanism or section that F1 does not call for; cite the finding id on every addition.
- Prefer deleting or narrowing to adding: narrow both texts to the commands the Phase column assigns to Phase 1.
- Report the byte size of the spec before (57763) and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings alone, including F2-F14 and N1-N5.
- Return the candidate once and do not award yourself a PASS.

verdict: FAIL
