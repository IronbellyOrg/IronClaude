review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec.md (round 1)

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
Command: `/sc:spec-panel --mode critique --focus requirements,architecture` (first review, no `--re-review`, `baseline: missing` not applicable, full document).
Candidate not edited. No other review started.

Citation keys: `S:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`; `CMD:N` = line N of `command.md` (the panel command). Any citation to a file outside the workspace (`src/`, `CLAUDE.md`, `EVIDENCE.md`, `.dev/codegraph-migration/`, `plugins/`, `Makefile`, `pyproject.toml`, Orca binaries) is UNVERIFIED because it cannot be checked here; the candidate's own pointer to such a file is repeated only as the candidate's claim.

## What was covered

- Read in full: the candidate (285 lines), README, the three inventories, `command.md`.
- Cross-checked the candidate's `INV-A`, `INV-B`, `CAPS` and `README` line citations in sections 1.2 to 1.4, 2.2, 3.1, 3.2 (evidence and phase columns), 4, 8, 9 and the UNVERIFIED list against the inventories. No wrong line found. The 43 = 10 + 27 + 6 split, the 27 rows of section 3.2, the 6 rows of section 4 and the phase column (P1 9, P2 11 + 4, P3 4, P4 3) add up (checked by count).
- Experts run, in the fixed order: Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard, Newman, Hohpe (architecture); Whittaker (active in every panel review, placed after Fowler and Nygard). Crispin, Gregory, Hightower are outside the two focus areas and were not run.
- Mandatory artifacts produced: Guard Condition Boundary Table (below, before synthesis) and Quantity Flow Diagram (Pipeline Dimensional Analysis triggered: 43 commands go through a 3-way split and a 5-phase rollout whose counts differ).
- Not covered: behavior of the commands themselves (their files are not in the workspace; only the inventories are), Orca internals (only `CAPS`), and any live run. `--focus correctness` is advisory-suggested (the spec has 3+ mutable state variables: contract `status`, ledger, run-log, output dirs; and numeric thresholds 60 s, 5 min, 4 min) but was not activated, so no State Variable Registry is produced.

## Grading rule applied

Brief's Grading check applied to every finding. Blocking needs a sentence that holds with no further assumption (two stated texts that contradict, data loss or safety break, or a stated text an acceptance criterion cannot pass). A finding that names a requirement the document never states, or needs a guess between two allowed readings, is Medium and goes under follow-up candidates even when its label is MAJOR.

Interaction with the command: `CMD:259` makes FR-8/FR-9 findings blocking. `CMD:263` (bullet 7) lets a brief narrow, not widen. The brief's rule narrows FR-8/FR-9 findings that only name an unstated requirement to Medium, so they are graded Medium below. Under the command's unmodified bullet 2 the GAP-derived findings M2, M3, M6, M7, M8, M10, M11, M12 and M13 would count as blocking; the coordinator should know this choice was made.

## Guard Condition Boundary Table (hard gate FR-10: complete before synthesis)

Guards enumerated are the guard-type rules of the worker contract (the per-command gate resolutions of section 3 are covered by the findings, not row by row). 7 guards x 6 rows, all cells populated.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 `unattended_selector` | S:51,60,228 | Zero/Empty | flag absent | false | Standalone behavior unchanged (S:146) | OK |
| G1 | S:51,62 | One/Minimal | `--unattended` alone, no output dir | true | Unspecified: contract needs "the directory the coordinator passed" (S:62); no rule when none passed | GAP |
| G1 | S:159,228 | Typical | `--unattended --output <dir>` | true | Gates resolve per section 3 row; contract written (S:60,62) | OK |
| G1 | S:60,103,110,118 | Maximum/Overflow | `--unattended` plus `--interactive` (or flag twice) | true | Unspecified for all commands except the rows that say "refused" (cleanup, improve, roadmap, adversarial) | GAP |
| G1 | S:51,228 | Sentinel Value Match | `"login fails --unattended"` quoted inside the topic text | true? | Unspecified: spec never says the token counts only as a standalone unquoted argument; D1 says it "cannot misfire" (S:228) | GAP |
| G1 | S:159 | Legitimate Edge Case | command with no gate (analyze) | true | Accepted as a no-op (S:159) | OK |
| G2 `status_to_outcome` | S:62-63 | Zero/Empty | contract file absent | no report | `--outcome failed` (S:63) | OK |
| G2 | S:63,183 | One/Minimal | file present but 0 bytes, unparseable, or no `status` key | report exists | Unspecified: S:63 covers only "no report exists"; S:183 tests it but does not say what the worker sends | GAP |
| G2 | S:63 | Typical | `status: succeeded` | true | `--outcome succeeded` (S:63) | OK |
| G2 | S:62,261 | Maximum/Overflow | `status` outside the four-value set (a command keeps its existing contract fields, S:62) | not in set | Unspecified: S:62 says "keep their fields" and also fixes the four values | GAP |
| G2 | S:63,263 | Sentinel Value Match | `status: partial` | true | Maps to succeeded (S:63,263); what makes a run partial is never defined | GAP |
| G2 | S:63 | Legitimate Edge Case | audit verdict FAIL, run completed | true | `--outcome succeeded`, first sentence states the verdict (S:63) | OK |
| G3 `readiness_limit` | S:59 | Zero/Empty | no startup prompt (0 s) | pass | Ready (S:59, CAPS:44-47) | OK |
| G3 | S:59 | One/Minimal | prompt with 1 s fallback | pass | Falls back inside the limit (S:59) | OK |
| G3 | S:59 | Typical | 30 s fallback | pass | Passes (S:59; CAPS:49 shows a 34 s start) | OK |
| G3 | S:59 | Maximum/Overflow | fallback of 50 s or none | fail | S:59 says only "well inside" the limit; no number; CAPS:49 shows failure above about 45 s | GAP |
| G3 | S:59 | Sentinel Value Match | exactly 60 s, or `--timeout-ms` raised | boundary | Unspecified whether raising `--timeout-ms` is an allowed substitute for a fallback | GAP |
| G3 | S:44,60 | Legitimate Edge Case | `AskUserQuestion` after input is accepted | not a start failure | Not a `worker-start` failure; a silent stall; covered by WC-2 (S:44,60) | OK |
| G4 `wait_budget` | S:68 | Zero/Empty | no wait | n/a | Nothing to split (S:68) | OK |
| G4 | S:68 | One/Minimal | 1 s poll | under limit | No split needed (S:68) | OK |
| G4 | S:68 | Typical | 3 min wait | under limit | Heartbeat possible between calls (S:68) | OK |
| G4 | S:68,65 | Maximum/Overflow | one Agent-tool call (fan-out wave) lasting 20 min | over limit | Unspecified: S:68 covers "a single tool call" only for poll waits and long evals; subagents may not send heartbeats (S:65) | GAP |
| G4 | S:68,210 | Sentinel Value Match | one call of 4 min 30 s | boundary | S:68 splits only calls longer than 5 min; AC-4.3 (S:210) fails any call over 240 s | GAP |
| G4 | S:61,68 | Legitimate Edge Case | blocked inside `ask` or `check --wait` | heartbeat skipped | No heartbeat while blocked (S:61; CAPS:64) | OK |
| G5 `resume_or_fresh` | S:64 | Zero/Empty | no earlier output | fresh | Fresh run (S:64) | OK |
| G5 | S:64 | One/Minimal | retry, command has no resume flag | fresh dir | Writes a fresh output directory (S:64) | OK |
| G5 | S:64 | Typical | retry with resume flag passed | resume | Resumes from disk (S:64) | OK |
| G5 | S:64,205 | Maximum/Overflow | retry, command HAS a resume flag, brief omits it (roadmap, implement, cleanup-audit) | neither branch | Unspecified: S:64 offers only "flag given" or "no flag exists"; AC-3.2 (S:205) starts fresh in the same dir | GAP |
| G5 | S:62,183 | Sentinel Value Match | stale `return-contract.yaml` (`status: blocked`) from attempt 1, attempt 2 crashes before writing | file exists | Unspecified: S:62 lists no run or dispatch identifier; S:183 only tests existence and status | GAP |
| G5 | S:69,85 | Legitimate Edge Case | two workers, fixed-path outputs (cleanup-audit, index-repo, init-lite) | concurrent | Only cleanup-audit is told "one audit per worktree" (S:85); WC-11 says "must never write the same file" (S:69) but the other two rows keep their fixed paths (S:86,87) | GAP |
| G6 `ask_once` | S:61 | Zero/Empty | session holds no preamble | no ask | Resolves blocked, stops (S:61) | OK |
| G6 | S:61 | One/Minimal | one ask, answered | answer | Re-invoke with answer as flag (S:61) | OK |
| G6 | S:61,200 | Typical | gate blocked, preamble present | may ask | "may" ask and continue (S:61) while AC-2.2 requires `failed` and `blocked` (S:200) | GAP |
| G6 | S:61,105 | Maximum/Overflow | second gate after the first was answered (cli-portify has three) | repeat | "ask the coordinator once" (S:61): once per gate or per run is not stated | GAP |
| G6 | S:61 | Sentinel Value Match | ask timeout | pending | Resume same message ID, no duplicate (S:61; CAPS:60) | OK |
| G6 | S:109,233 | Legitimate Edge Case | implement halt needs a Ruling; coordinator is "another agent" | rejected by qa.md:238 (UNVERIFIED file) | WC-3 not scoped to exclude implement; D2 decides later (S:233-236) | GAP |
| G7 `outward_default` | S:67 | Zero/Empty | no outward flag in brief | off | Off (S:67) | OK |
| G7 | S:67,245 | One/Minimal | explicit flag plus quoted user instruction | on | On only then (S:67; D4 a, S:245) | OK |
| G7 | S:100 | Typical | auggie-review `--unattended` | off | `--no-post-pr`, `--no-remediation-offer` implied (S:100) | OK |
| G7 | S:114,238-242 | Maximum/Overflow | pr-submit, whose whole job is outward | decided by D3 | Deferred to D3/D4 by design (S:114,242) | OK |
| G7 | S:122,100 | Sentinel Value Match | nested invocation of an outward-capable command (pr-submit fallback to auggie-review, INV-B:91; workflow handoff) | flag not passed | Unspecified: only tasklist to reflect passes `--unattended` down (S:122) | GAP |
| G7 | S:121 | Legitimate Edge Case | `commit` or `push` keyword in a task prompt | refused | Refused unless authorized (S:121) | OK |

GAP rows: 17 (G1 x3, G2 x3, G3 x2, G4 x2, G5 x3, G6 x3, G7 x1). Each is carried into a finding below (FR-8/FR-9): G1 row 2 to M12; G1 rows 4 and 5 to M11; G2 rows 2 to 5 to M2; G3 rows 4 and 5 and G4 row 5 to M13; G4 row 4 to M7; G5 row 4 to M8; G5 row 5 to M2; G5 row 6 to M10; G6 rows 3, 4, 6 to M3; G7 row 5 to M6. Table is complete; synthesis proceeds.

## Quantity Flow Diagram (FR-21)

```text
[cmd/ commands: 43 (S:76)] --> [Classify] --> [3.1 ready: 10][3.2 change: 27][S4 coordinator-only: 6]   10+27+6 = 43  (no divergence)
                                  |
                                  v
[P1 scope: --unattended + "## Unattended mode" on 3.1 + 3.2 = 37 (S:159,76)]
        |-- N=37 --> [Consumer AC-1.1: expects 37 sections naming return-contract.yaml (S:195)]
        |-- 37 -> 36 --> [Contract-bearing: load has report "none" (S:112), decision "a report file would be an unrequested addition" (S:265)]
        |                  Consumer AC-1.1 uses N=37, producer yields 36 <-- MISMATCH (B1)
        |-- 37 -> 13 --> [P1 Commands cell names 9 (3.2) + 4 fixes (3.1) = 13 (S:159); brainstorm and init-lite appear in no phase list]
        |-- 37 -> 34 --> [P4 commands (implement, post-release, pr-submit) carry the flag from P1 but their gates land in P4 after D2-D4 (S:162,225)] <-- MISMATCH (M4)
        v
[Consumer AC-1.2: 7.2 live check on "each P1 command" = 13 (S:196)]   [Consumer AC-2.2: gate-trigger run on P2 commands = 15 (S:200)]
```

Phase command lists: P1 9 + 4 fixes = 13, P2 15, P3 4, P4 3 = 35 named, plus brainstorm and init-lite (named in no list) = 37. The one real divergence for a consumer is B1 (AC-1.1 assumes 37, load gives 36). Severity per FR-19: CRITICAL for B1; the P4 divergence is graded Medium under the brief (M4).

=== REQUIREMENTS ANALYSIS ===
Experts: Wiegers (lead), Adzic, Cockburn.

### B1 CRITICAL, blocking. AC-1.1 requires a contract section on every command, the load row and Decisions say load has none
- Issue: AC-1.1 (S:195) asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`. P1 (S:159) says `--unattended` is accepted by every command in 3.1 and 3.2. The `/sc:load` row (S:112) says report "none (see note)", resume "n/a", "use it as a step inside another worker's brief, not as its own Task", change "P1 (usage line only)". Decisions (S:265) chose "Use it inside a brief ... a report file would be an unrequested addition". Section 3's preamble (S:76) says every changed command gains the section, and WC-4 (S:62) says the contract is written on every outcome in unattended mode.
- Severity: CRITICAL. Expert: Wiegers (traceability, testability), Adzic. Priority: High. Quality impact: Consistency 6 to 8, Testability 5 to 7 once fixed.
- Grading sentence: An implementer who follows the stated text as written builds P1 with a `## Unattended mode` section naming `return-contract.yaml` on `/sc:load`, or builds load without one; either way a stated text is violated: the first breaks the load row and the Decisions entry (no report file), the second fails AC-1.1. Two stated texts contradict, so the finding is blocking with no further assumption.
- Same defect, same location, second case: pr-submit, implement and post-release are in 3.2 so AC-1.1 requires their section and the flag in P1, while S:162 and S:225 say their gate resolutions wait for D2 to D4, and D3(a) (the recommended answer, S:240) says "no pr-submit changes in Phase 4" and section 4's last paragraph (S:139) keeps pr-submit out of the worker set unless D3 allows it. Under the recommended D3(a), AC-1.1 still demands a pr-submit section.
- Recommendation: restate AC-1.1 as "every command that section 3 marks as producing a contract has the section" and list load as excluded (or give load a one-line section that says it writes no contract); say whether implement, post-release and pr-submit are exempt from AC-1.1 until D2 to D4 are answered. Rationale: the acceptance test must agree with the rows it tests.

### M1 MAJOR, graded Medium. AC-0.4 step 3 cannot pass in P0 as written
- Issue: P0 makes no command edits (S:158) and the WC-4 contract arrives in P1 (S:194). AC-0.4 (S:194) says steps 1 to 3 and 5 to 7 of 7.2 pass and only step 4 "uses the command's existing report file". Step 3 (S:182) requires the `--outcome` to match "the contract's status" and "its report path is the WC-4 contract path". `/sc:troubleshoot` writes only REPORT.md in this mode (the contract exists only with `--caller task-unified`, INV-B:242; S:91).
- Expert: Adzic (testable example). Priority: High. Quality impact: Testability.
- Grading sentence: An implementer who follows the stated text as written runs the three P0 smoke runs and finds step 3 unsatisfiable for troubleshoot, and that is wrong because a false P0 failure "reopens section 1" (S:194); this needs the guess that the carve-out for step 4 was not meant to cover step 3, so it is Medium.
- Recommendation: extend the carve-out to step 3 for P0 ("report path is the command's existing report; outcome matches the report's verdict").

### M2 MAJOR, graded Medium. Status vocabulary, `partial`, refusals and stale contracts are undefined (G2 rows 2, 4, 5; G5 row 5)
- Issue: (a) WC-4 (S:62) says commands that already write a contract "keep their fields and add the missing ones" and also fixes `status` to four values; the existing workflow contract has its own `status` field (INV-B:272) and the spec never lists existing vocabularies. (b) `partial` maps to succeeded (S:63,263) but no condition makes a run partial. (c) Refusals ("`--mode socratic` refused", `--watch`, `--monitor 1`, `--interactive`, S:102,103,110,114,123) have no stated status; `blocked` requires a `blocked_question` (S:62) and a refusal has none. (d) The required fields (S:62) carry no dispatch, run or timestamp identifier, so a stale contract from attempt 1 passes 7.2 step 4 (`test -s` plus a status check, S:183) if attempt 2 dies first.
- Expert: Wiegers (state assumptions), Whittaker (sequence attack). Priority: Medium. Quality impact: Completeness 6, Consistency.
- Grading sentence: An implementer who follows the stated text as written builds a contract whose `status` may collide with an existing field and whose refusal and partial cases are chosen by the implementer; that is wrong only if the implementer picks a reading the text allows, and the rule is a requirement the document never states, so Medium.
- Recommendation: add `contract_version`, `dispatch_id` (or finish timestamp), a rule that existing statuses map to the four values, a one-line definition of `partial`, and `status: failed` with a reason field for refusals.

### M3 MAJOR, graded Medium. WC-3 "may ask" conflicts with AC-2.2 and is not scoped for implement (G6 rows 3, 4, 6)
- Issue: WC-3 (S:61) lets the worker ask the coordinator "once" and then resume with the answer. AC-2.2 (S:200) requires, for gate-trigger input, `worker_done --outcome failed` with `status: blocked`. A worker that follows WC-3 and gets an answer ends `succeeded`; one that waits on an unanswered ask never ends. For `/sc:implement` a coordinator's answer is "another agent's message", which the Ruling rule does not accept (S:233; qa.md:238 UNVERIFIED), and D2(a) says the worker ends `failed` (S:234), but WC-3 is general.
- Expert: Adzic, Cockburn (actor and goal of the coordinator). Priority: Medium.
- Grading sentence: An implementer who follows WC-3 as written builds a worker that may ask and continue, and AC-2.2 then cannot pass deterministically; this depends on the guess that the worker picks the ask branch, so Medium.
- Recommendation: make AC-2.2 run with no coordinator reply and say whether "once" means per gate or per run; exclude implement's Ruling from WC-3.

### M4 MAJOR, graded Medium. P1 enables `--unattended` before the gate rows land, and for P4 commands before D2 to D4 (see QFD)
- Issue: P1 (S:159) says every command in 3.1 and 3.2 accepts `--unattended`; P2, P3 and P4 convert the gates (S:160-162). Section 2.3 (S:73) tells the coordinator to pass `--unattended` in every brief. Between P1 and P2 (or P4) a command such as cleanup, task or implement accepts the flag and still prompts or halts on a person, the silent stall WC-2 (S:60) forbids. No rule says the flag must be refused, or the command left out of dispatch, until its row has landed.
- Expert: Cockburn (primary actor: coordinator). Priority: Medium.
- Grading sentence: An implementer who follows P1 builds a flag that WC-2 forbids from prompting yet cannot yet keep that promise; wrong only if a coordinator dispatches such a command before its phase, which is a guess, so Medium.
- Recommendation: either accept the flag per command only when its gate row ships, or add "refuse with `status: blocked` until the command's phase" to P1.

### M5 MAJOR, graded Medium. AC-C1 conflicts with SA-2 and with what P0 puts into `core/`
- Issue: AC-C1 (S:172) requires the grep over `src/superclaude/core` to print nothing; SA-2 (S:147) allows an Orca mention in the contract file as an example of a question channel; P0 (S:158) adds `WORKER-CONTRACT.md` (section 2 rules, which name `worker_done`, `heartbeat`, `ask`, `check`) and an Orca section to `HOW-WE-WORK.md`, both under `core/`. Whether either file contains a line matching `orca <orchestration|worktree|terminal|agent>` is left to the author. The pattern also misses `ORCA orchestration ...` (placeholder form used in S:180-186), `orca-ide skills ...`, `orca status`, `orca open`.
- Expert: Wiegers (testability). Priority: Medium.
- Grading sentence: An implementer who follows the stated text as written may write `orca orchestration ask` in the contract file as SA-2 permits and then fail AC-C1 in P0; needs the guess that the author writes the literal command, so Medium.
- Recommendation: scope AC-C1 to `commands/`, `skills/`, `agents/` and exclude the two named core files, or ban literal commands in them.

=== ARCHITECTURE ANALYSIS ===
Experts: Fowler (lead), Nygard, Newman, Hohpe.

### B2 CRITICAL, blocking. WC-4's contract location rule contradicts the rows and acceptance criteria that use it
- Issue: WC-4 (S:62) puts the contract at `<output-dir>/return-contract.yaml`, "the directory the coordinator passed (`--output` / `--output-dir`)", known before dispatch. Four stated cases contradict that: (1) tdd and init-lite take `--output <file>` (S:87,90) and AC-2.2 (S:200) runs `/sc:tdd ... --output <file>` and requires a contract with `status: blocked`; a file cannot hold `return-contract.yaml`. (2) adversarial's fix is `<output>/adversarial/return-contract.yaml` (S:83,198), not the passed directory. (3) workflow's contract is `.dev/tasks/to-do/<id>/return-contract.yaml` (S:92), a generated id with no directory flag, so the path is not known before dispatch, and the P1 fix writes a contract for stops "before creation" (S:92) when no `<id>` exists. (4) spec-panel gets a new `--output` of unstated type (S:120). 7.2 step 3 (S:182) and AC-1.2 (S:196) then test "the WC-4 contract path".
- Corroboration (not spec evidence): the panel command itself avoids the clash by using `--report-dir` "only (`--output` is file-valued)" (`CMD:456`).
- Severity: CRITICAL. Expert: Fowler (interface consistency), Newman (versioned contract). Priority: High. Quality impact: Consistency, Testability.
- Grading sentence: An implementer who follows the stated text as written builds a contract at `<--output value>/return-contract.yaml` for every command, and that is wrong because for tdd and init-lite the same document passes a file (so the path cannot exist), and for adversarial and workflow its own rows put the contract elsewhere, so AC-1.2 and AC-2.2 cannot locate or pass it. Stated texts contradict; blocking.
- Recommendation: define one rule (for example "contract path = `--report-dir` if given, else the parent directory of a file-valued `--output`") and list the path per command in section 3; make the pre-creation workflow stop write to the passed report dir. Rationale: the coordinator and the tests must derive the path from the brief alone (S:62,73).

### M6 MAJOR, graded Medium. No rule passes `--unattended` to nested `/sc:` invocations (G7 row 5)
- Issue: only tasklist to reflect is stated (S:122). Other nested chains: tasklist Stage 9 runs `sc:task --compliance strict` (INV-B:211), whose confidence and TFEP gates are person-blocking (S:121); pr-submit may run `/sc:auggie-review` as a fallback (INV-B:91), which posts to GitHub by default (S:100); release-split and brainstorm call adversarial (INV-B:119); cli-eval create runs spec-panel and adversarial (INV-A:44); workflow can hand off to implement (INV-B:274). WC-2, WC-9 (S:60,67) bind "the command" but not commands it invokes.
- Expert: Fowler, Hohpe (message flow). Priority: Medium.
- Grading sentence: An implementer who follows the tasklist row builds Stage 10.5 with the flag and Stage 9 without; wrong only if Stage 9's task hits a gate, a guess, so Medium.
- Recommendation: add to WC-2 "a command passes `--unattended` to every `/sc:` command or skill it invokes".

### M7 MAJOR, graded Medium. WC-10 covers only Bash waits; long Agent-tool calls get no heartbeat (G4 row 4)
- Issue: WC-10 (S:68) splits waits that block "a single tool call" (poll waits, long evals). The heavy fan-out commands (tdd, cleanup-audit waves of 7 to 8 agents, troubleshoot Tier 2, tasklist 2N validators, INV-A:42, INV-B:221) hold the top-level session in an Agent-tool call that may run past 5 minutes, and WC-7 forbids the subagents from sending heartbeats (S:65). The spec says Orca's use of heartbeat age is UNVERIFIED (CAPS:130), so the effect is unknown. AC-4.3 checks heartbeats only for pr-submit (S:210).
- Expert: Nygard (liveness). Priority: Medium.
- Grading sentence: An implementer who follows WC-10 builds wait splitting for polls and evals only; wrong only if a silent session is treated as dead, which the spec itself marks UNVERIFIED, so Medium.
- Recommendation: state whether a missing heartbeat during a fan-out call is acceptable, and test one fan-out command in 7.2.

### M8 MAJOR, graded Medium. WC-6 omits commands that have a resume flag but are run without it (G5 row 4)
- Issue: WC-6 (S:64) offers "resume when given its flag" or "fresh directory if it has none". Roadmap has a flag, and AC-3.2 (S:205) starts fresh in the same directory that holds a `.session-memory.md`, overwriting the first attempt's outputs, the case WC-6 says a retry "must not corrupt". Implement resumes implicitly from a matching ledger (S:109). Cleanup-audit uses a fixed `.claude-audit/` with `progress.json` (S:85).
- Expert: Nygard. Priority: Medium.
- Grading sentence: An implementer who follows WC-6 builds roadmap that, with no flag, restarts in the old directory and loses the partial outputs; wrong only if the retry brief omits the flag, a guess, so Medium.
- Recommendation: for commands that have a resume flag, require a fresh directory when the flag is absent.

### M9 MAJOR, graded Medium. Nothing states how the worker-session rules reach the worker
- Issue: WC-3, WC-5, WC-7 and WC-12 are owned by the "worker session" (S:61,63,65,70), not by commands. Their only home is `WORKER-CONTRACT.md` (S:52), which commands point to from the `## Unattended mode` section (S:52,76). Section 2.3 (S:73) lists what the brief states and does not include "read the contract file". A worker running a command whose section has not landed yet (see M4), or whose installed `~/.claude/` lacks the new core file, has no source for WC-5's outcome mapping and no fallback is stated. Also the contract file would carry `worker_done`/`check` rules while SA-2 (S:147) limits Orca mentions to "an example of a caller's question channel" (see M5).
- Expert: Newman, Hohpe. Priority: Medium.
- Grading sentence: An implementer who follows the text builds the contract file and the section pointers, but no step makes a worker read it; wrong only if the worker session skips it, a guess, so Medium.
- Recommendation: add "read `~/.claude/WORKER-CONTRACT.md`" to the brief template in 2.3 and say what a command does when the file is missing (stop with `status: failed`).

### M10 MAJOR, graded Medium. WC-11 is unscoped and conflicts with the fixed-path rows (G5 row 6)
- Issue: WC-11 (S:69) says default output paths carry a timestamp or slug and two workers in one worktree never write the same file. It is not limited to unattended mode, while SA-1 (S:146) freezes every default output path without the flag. Rows keep fixed paths: cleanup-audit (`.claude-audit/`, S:85), index-repo (`PROJECT_INDEX.md`, S:86), init-lite (S:87), and there is no "slug the coordinator passes" flag in any row. Source files edited by cleanup, improve, document, test `--fix`, implement are not covered at all; the coordinator duty to give disjoint scopes or worktrees is not stated (S:73 mentions only placement).
- Expert: Fowler. Priority: Medium.
- Grading sentence: An implementer who follows WC-11 as written must change fixed default paths that three rows leave alone; which text wins is a guess, so Medium.
- Recommendation: scope WC-11 to unattended mode and add a coordinator rule: one writer per worktree for fixed-path and source-editing commands.

### M13 MAJOR, graded Medium. Two numeric thresholds are unquantified or disagree (G3 rows 4, 5; G4 row 5)
- Issue: WC-1 (S:59) says fallbacks must be "well inside" the 60 s limit; the evidence shows failure above about 45 s (CAPS:49) and the spec gives no number or owner (the owner is "launch setup", S:59, with no phase deliverable in S:158-162). WC-10 (S:68) splits calls longer than 5 minutes into waits of at most 4 minutes while AC-4.3 (S:210) fails any call over 240 s, so a 4 min 30 s call passes WC-10 and fails AC-4.3.
- Expert: Wiegers (measurability). Priority: Medium.
- Grading sentence: An implementer who follows WC-10 builds 4.5-minute waits that AC-4.3 rejects; the wrong outcome needs the guess that such a wait is built, so Medium.
- Recommendation: state "each tool call at most 240 s" in WC-10 and "fallback at most 30 s" in WC-1, and name who owns WC-1.

=== ADVERSARIAL ANALYSIS (Whittaker) ===

Findings with no other home are written in full here; the rest are the attack traces behind the findings above.

### M11 MAJOR, graded Medium. Sentinel collision on the `--unattended` token (G1 rows 4, 5)
I can break this specification by **Sentinel Collision Attack**. The invariant at **S:51 and S:228 (D1 a: "cannot misfire on a person")** fails when **the flag text appears inside a quoted argument or together with `--interactive`**. Concrete attack: before, a person runs `/sc:troubleshoot "login fails after --unattended was added"` in a plain session, state `mode=attended`; the command sees the token, state becomes `mode=unattended`, gates resolve silently (S:60) and a contract file appears (SA-3, S:148 broken). Second trace: `/sc:cleanup src --interactive --unattended`: S:103 says `--interactive` is refused, no other row says which flag wins.
- Expert: Whittaker. Priority: Medium. Quality impact: Correctness (SA-1).
- Grading sentence: An implementer who follows D1 (a) builds substring or token matching; wrong only if matching is not limited to a standalone token, which the text does not require, so Medium.
- Recommendation: add "counts only as a standalone unquoted argument" to the contract (the panel command already does this, `CMD:455`) and a precedence rule against person-mode flags.

### M12 MAJOR, graded Medium. Zero/empty attack: `--unattended` with no output directory, and no contract on a crash (G1 row 2)
I can break this specification by **Zero/Empty Attack**. The invariant at **S:62 ("written on every outcome") and S:73 (coordinator passes the directory)** fails when **the brief omits the directory, the directory is unwritable, or the process is killed**. Concrete attack: brief `/sc:analyze src/x.py --unattended`; before, no contract; after, the command runs, finds no `<output-dir>`, and has nowhere to write the contract; WC-5 then sends `failed` (S:63) with no report, and the analysis is lost. Crash trace: context exhaustion mid-run leaves no file, yet "every outcome" (S:62) is promised.
- Expert: Whittaker, Nygard. Priority: Medium.
- Grading sentence: An implementer who follows WC-4 builds no behavior for a missing directory; the text never states one, so Medium.
- Recommendation: under `--unattended` with no directory, refuse before work with a chat-only message (the panel command's own rule, `CMD:456`), and write a stub contract at the start of the run, updated at the end.

Attack traces behind earlier findings:
- **Divergence Attack** on S:61 vs S:200 (M3): condition "gate blocked and preamble present" has two allowed branches (ask or stop); both can apply; AC-2.2 accepts one.
- **Sequence Attack** on S:159-162 (M4): execute P1 without P2; `/sc:cleanup --unattended` accepted, then prompts (S:103 is P2).
- **Sequence Attack** on S:62,183 (M2): attempt 1 writes `blocked`; attempt 2 starts, dies; coordinator reads attempt 1's file as current.
- **Accumulation Attack** on S:68 (M7): 20-minute Agent-tool wave, zero heartbeats from a session that cannot send while waiting.
- **Divergence Attack** on S:195 vs S:112 (B1): count 37 expected, 36 produced.

## Quality assessment and consensus

```yaml
specification_review:
  original_spec: ".dev/orca-command-refactor/specs/orca-worker-contract-spec.md"
  sha256: "d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d"
  review_date: "2026-11-10"
  expert_panel: [Wiegers, Adzic, Cockburn, Fowler, Nygard, Newman, Hohpe, Whittaker]
  focus_areas: [requirements, architecture]
quality_assessment:
  overall_score: 6.5
  clarity: 7
  completeness: 6
  testability: 6
  consistency: 6
critical_issues:
  - {id: B1, category: requirements, severity: CRITICAL, expert: Wiegers, issue: "AC-1.1 requires a contract section on load, which the load row and Decisions say has none", recommendation: "align AC-1.1 with the rows"}
  - {id: B2, category: architecture, severity: CRITICAL, expert: Fowler, issue: "WC-4 contract path contradicts file-valued --output (tdd, init-lite, AC-2.2), adversarial subdir and workflow generated id", recommendation: "one path rule, listed per command"}
expert_consensus:
  - "The decision (Orca on top, commands as workers) is well supported and the evidence limits are stated honestly (S:41-45)."
  - "The contract is the right mechanism; its location, status and acceptance tests need to agree with each other."
  - "No command, skill or agent mention of Orca is required; SA-2 is a sound boundary."
improvement_roadmap:
  immediate: [B1, B2]
  short_term: [M1, M2, M3, M4, M5, M11, M12]
  long_term: [M6, M7, M8, M9, M10, M13]
adversarial_analysis: "see section above"
```

Panel note: the spec introduces 3+ mutable state variables and numeric thresholds, so `--focus correctness` is advisory-recommended for review 2.

## Follow-up candidates (Medium, not blocking)

M1 AC-0.4 step 3 in P0; M2 status vocabulary, `partial`, refusals, stale contract; M3 WC-3 vs AC-2.2 and implement Ruling; M4 flag before gate rows land; M5 AC-C1 vs SA-2 and P0 content; M6 no propagation of `--unattended` to nested commands; M7 WC-10 covers Bash waits only; M8 WC-6 resume-flag-omitted case; M9 delivery of worker-session rules; M10 WC-11 scope and fixed paths; M11 `--unattended` token collision; M12 no output dir and crash; M13 unquantified thresholds (WC-1, WC-10 vs AC-4.3).

Minor notes (never fail the review):
- N1 S:79 says "the only command changes are the small fixes" while P1 (S:159) adds the contract and flag to all ten; brainstorm and init-lite appear in no phase command list (S:158-162).
- N2 The tasklist row (S:122) differs from the inventory's recommendation (drop `--remediate` or use `--no-reflect`, INV-B:215) and no Decisions entry records why; what the reflect headless auto-accept does to `--remediate` under `--unattended` is UNVERIFIED (INV-B:109).
- N3 `cleanup` row (S:103) covers the "Approval Required" list but not the "If unsure, prompt user" rule (INV-A:43); research "pins" `--strategy planning` (S:116) with no rule for an explicit conflicting `--strategy` in the brief; cli-eval "the safety flags" (S:104) are never listed.
- N4 7.2 step 5 (S:184) searches the transcript for the string `AskUserQuestion`, which also appears in loaded command and skill text (for example INV-B:239 "never AskUserQuestion"); "no call" is the pass condition but the method can mislead.
- N5 AC-2.4 (S:202) uses `...` in place of the full `gh api` path, so it is not runnable as written; AC-1.3 (S:197) says "scratch worktree" without saying it is created through Orca (README rules; `CLAUDE.md` worktree rule UNVERIFIED here).
- N6 The invocation mechanism is not stated: Orca wraps the brief in a preamble (CAPS:47), so a leading `/sc:` slash command is not guaranteed to parse as one; the spec treats this as the thing P0 tests (S:43), which is acceptable.
- N7 Under D3(a) the "27 need change" count includes pr-submit although it would get no change (S:76,240).
- N8 UNVERIFIED here (outside the workspace): S:11 "re-read 11 locations", S:52 `install_core.py` lines, S:25 grep results, S:183 `pyproject.toml:38`, S:279 `Makefile:68-74`, S:285 "340 citations checked", `.dev/codegraph-migration/orchestration/README.md:33,42`, all `cmd/` and `sk/` line cites not echoed in an inventory.

## Reviser brief

Blocking finding ids: B1, B2. Contract for the reviser (restating Review Loop bullet 6): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; report the byte size of the candidate before and after. Do not act on M1 to M13 or N1 to N8 in this cycle.

verdict: FAIL
