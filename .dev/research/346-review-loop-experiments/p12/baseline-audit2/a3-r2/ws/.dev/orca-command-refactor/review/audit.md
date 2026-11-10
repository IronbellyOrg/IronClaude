review: 1 of 3

# /sc:spec-panel audit (critique mode, focus requirements,architecture)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `466dcf239d1cdea564cc23de1d5abe284de1d002582065afb592d5d4494fa5a3`
- baseline: none (first review of the whole document; no `--re-review`, no `--baseline`)
- reviewer model actually used: Sonnet 5.5 (`claude-sonnet-5-5`)
- run type: labelled whole-document audit of the final spec, per the FIRST-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`. Brief clauses overridden: none.
- coverage line: whole document, all 286 lines, read in full. The three inventories under `.dev/orca-command-refactor/inventory/` were read in full and every INV-A, INV-B and CAPS reference in spec sections 1, 3.1, 3.2 and 4 was matched to its inventory line: no wrong line and no wrong topic found.
- verification limit: the workspace holds only `README.md`, the spec and the three inventories. Every `src/`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `EVIDENCE.md`, codegraph-migration and `HOW-WE-WORK.md` citation in the spec cannot be checked here and is UNVERIFIED except where an inventory quotes it. That includes the "11 re-read locations" claim (SPEC:11) and the citation-check claim (SPEC:285).
- issue offer for follow-up candidates: not made. This is a sandbox worker with no user channel and no `--unattended` report directory; the command asks the user once per loop, so the offer is left to the coordinator. No issue was created.

Shorthand: `SPEC:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`. `CMD:N` = `command.md` of /sc:spec-panel (the review command). Quality (0-10): Clarity 7, Completeness 6, Testability 6, Consistency 6.

## Summary of grading

- Blocking: 1 (B-1).
- Medium (follow-up candidates, never fail the review): 15 (M-1 to M-15).
- Minor notes: 12 (N-1 to N-12).

The decision (Orca coordinates, commands stay units of work), the 10/27/6 split, the WC-1 to WC-12 contract and the phase table are coherent and well cited. Counts are conserved across sections (see Quantity Flow Diagram). The single blocking finding is an acceptance criterion whose scope contradicts the rows it tests.

## Expert panel, in the fixed review order

1. **Wiegers (requirements quality).** Each WC row names owner and evidence (SPEC:57-70), which is good traceability. Gaps: several requirements have no acceptance check (M-6); two thresholds are not numbers ("well inside", M-15; the 4-5 minute band, M-7); the authorization flag in WC-9 is assumed, not defined (M-2).
2. **Adzic (examples).** Concrete examples exist for the brief (SPEC:228), for the tdd gate (SPEC:200) and for the 7.2 live check (SPEC:180-186). The cli-eval gate example in AC-2.2 has no stated contract location (M-1). No example shows a retry over an existing contract (M-3).
3. **Cockburn (actors and goals).** Three actors are clear: coordinator (SPEC:72-73), worker session (SPEC:57-70, Owner column), command. The `--unattended` caller who is not Orca (SPEC:51) has no stated duty for WC-3/WC-5, which need a preamble; WC-3 is conditional ("holds a preamble"), WC-5 is not (SPEC:61, 63). Minor, N-4.
4. **Fowler (architecture).** One shared contract file (SPEC:52) mixing launch-setup rules (WC-1), worker-session rules (WC-3, 5, 7, 12) and command rules is a mild interface-segregation smell, because commands read the whole file (N-4). Count divergence analysis is in the Quantity Flow Diagram; one mismatch (12 vs 8) is B-1.
5. **Nygard (failure modes).** Stale contract after a retry or crash (M-3); cap on blocked retries (N-12); heartbeat relevance unverified (M-7); phase gating when a flag is passed to the wrong command (M-4).
6. **Whittaker (adversarial).** Attacks are listed in the Adversarial Analysis section below.
7. **Newman (API evolution).** `--unattended` is added per command in phases (SPEC:154) so the flag surface evolves command by command; the spec does not say what a command does when it receives the flag before its phase (M-4). The contract schema (SPEC:62) has no version field, so a later field change cannot be told from an old contract (N-3).
8. **Hohpe (integration and data flow).** The signal path worker to coordinator is `worker_done` plus a pointer to a file (SPEC:62-63); Orca does not read the file (CAPS:79, SPEC:62). The spec handles this correctly by making the coordinator open the file (SPEC:73). `partial` maps to Orca `succeeded` (SPEC:63), which settles the Task and satisfies dependents (CAPS:90); see M-13.
9. **Crispin (testing).** Section 7 is concrete and mostly runnable. Coverage holes are in M-6. AC commands use `\|` inside code (N-1).
10. **Gregory (quality conversation).** The spec states its own evidence gaps (SPEC:41-45, 271-285), which is good practice. UNVERIFIED #14 is a verification claim, not an unverified item (N-2).
11. **Hightower (operations).** Orca executable naming and runtime-unavailable are handled (SPEC:34, 36; CAPS:145-147). Dispatch run-time bound is listed UNVERIFIED (SPEC:282). Hooks, templates and the plugin mirror are outside AC-C1 (N-5).

## === REQUIREMENTS ANALYSIS ===

### B-1 (blocking) AC-1.1 and AC-1.2 test 12 P1 commands; section 6 and the section 3 rows give the flag, the section and the contract to 8 or 9

- Severity: CRITICAL by FR-19 (dimensional mismatch with concrete counts), blocking on consequence. Experts: Wiegers, Fowler, Whittaker (Divergence Attack).
- Grading sentence: An implementer who follows the stated text builds either (a) `## Unattended mode` sections naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md` on all 12 commands whose section 3 phase is P1, or (b) the 8 or 9 commands section 6 lists. (a) is wrong because the load row says its report is "none (see note)" and that it is "use it as a step inside another worker's brief, not as its own Task" (SPEC:112), and the three ready P1 rows (adversarial, cleanup-audit, index-repo) specify only a filename or location fix, with no unattended gates and no contract (SPEC:83, 85, 86); section 6 says those three are "fixes", not flag recipients (SPEC:159). (b) is wrong because AC-1.1 is a test the same spec requires and it asserts the section on "every command whose section 3 phase is P1" (SPEC:195), so it fails on the commands not given one. Two stated texts contradict each other.
- Concrete count trace:
  - Section 3 rows with phase P1: ready rows adversarial (SPEC:83), cleanup-audit (SPEC:85), index-repo (SPEC:86) = 3; change rows analyze, build, business-panel, design, document, explain, index, load, test (SPEC:99, 101, 102, 106, 107, 108, 111, 112, 123) = 9. N = 12.
  - Section 6 P1 flag/section recipients: analyze, build, business-panel, design, document, explain, index, test = 8, plus load "(usage line only)" = 9 at most (SPEC:159).
  - AC-1.1 consumes N = 12 (SPEC:195). AC-1.2 runs "each P1 command with `--unattended --output <dir>`" (SPEC:196); index-repo and cleanup-audit have no `--output` flag and no `--unattended` flag in their rows (INV-A:42, 53), and load takes neither.
- Recommendation (Reviser brief carries it): narrow AC-1.1 and AC-1.2 to the commands section 6 lists as flag recipients, name them, and state that load, adversarial, cleanup-audit and index-repo are tested only by their named fix (AC-1.4 already covers adversarial, SPEC:198). Do not add a section to load, adversarial, cleanup-audit or index-repo.
- Priority: High. Quality-impact estimate: +1 testability, +1 consistency.

### M-1 (Medium; label MAJOR) WC-4 has no contract location for rows that add no named output flag

- Expert: Wiegers, Whittaker (Zero/Empty). The rule gives three places (SPEC:62). Rows that only say "add a report path" or "add an output path" give no flag and no dir-versus-file type: analyze, build, business-panel, design, document, explain, cleanup, improve, index, test, cli-eval, cli-portify (SPEC:99, 101-103, 104-108, 110-111, 123). AC-2.2 runs `/sc:cli-eval run --unattended` with no `--suite` and expects a contract with `status: blocked` (SPEC:200); cli-eval has no output flag in its row (SPEC:104; INV-A:44). The same gap covers any `--unattended` run that omits the output flag: WC-4 requires a contract "including stops before any other output exists" (SPEC:62) but a command that is blocked before it knows an output location has no place to write it.
- Why Medium: the worker passes a real path in `--report-path` (SPEC:62) so a coordinator can still find it; the implementer must invent the location, which is a requirement the document never states.
- Recommendation: add one sentence to WC-4 naming the default location for a missing flag (for example refuse in chat, as WC-2 already allows for the person case) and state per row the flag name and whether it is a dir or file. Priority: Medium.

### M-2 (Medium; MAJOR) WC-9 and D4 assume an explicit authorization flag that does not exist for post-release, task and pr-submit

- Expert: Wiegers. WC-9 says an outward default "turns on only through the command's own explicit flag written in the brief" (SPEC:67). D4(a) says the coordinator "passes the command's explicit flag" (SPEC:245). The rows name no such flag for post-release ("unless the brief authorizes them", SPEC:113), task ("refused unless authorized", SPEC:121) or pr-submit (SPEC:114). Today post-release's authorization is conversational: "unless the user pre-authorized them this session" (INV-B:79, 247). Also the post-release row requires "an explicit pre-tag choice" with no flag name (SPEC:113).
- Why Medium: not a stated text that does harm; the safe default (outward off) holds without a flag. The gap only blocks the authorized path.
- Recommendation: name the authorization flags in section 3 for these three rows, or state that authorization is out of scope until D4 is answered. Priority: Medium.

### M-3 (Medium; MAJOR) A retry or resume over an existing contract can leave a stale `status`

- Expert: Nygard, Whittaker (Sequence Attack). Concrete attack: attempt 1 of `/sc:tdd ... --resume` ends `blocked` and writes `<file>.return-contract.yaml` with `status: blocked`. The retry (`worker-start --retry-of`, SPEC:64) starts against the same `<file>`. If the session ends before the command rewrites the contract (context exhaustion, kill), the file still reads `blocked` and the coordinator, who opens the file as instructed (SPEC:73), reads attempt 1's result as attempt 2's. WC-4 says the file is written "on every outcome" (SPEC:62), which a killed session cannot do; WC-5 covers only "no report exists" (SPEC:63). WC-6 gives "resume or fresh dir" but does not say who chooses the fresh dir (SPEC:64) and the brief passes the dir (SPEC:73).
- Recommendation: add to WC-4 that the command writes `status` plus a run timestamp or run id at start and replaces it at the end, or that a retry brief must carry a new output path. Priority: Medium.

### M-4 (Medium; MAJOR) The `--unattended` switch has no parsing rule and no behaviour for a wrong-phase or coordinator-only target

- Expert: Whittaker (Sentinel Collision, Divergence). (a) D1(a) says the flag "cannot misfire on a person" (SPEC:228) but the spec never says the flag is read only as a standalone token outside quoted topic text. A topic such as `/sc:tdd "explain the --unattended flag"` is a legitimate input that collides with the control token; the result is a person's run losing its gates, which SA-1 forbids (SPEC:146). (b) Section 6 makes the coordinator responsible for passing the flag only after its phase (SPEC:154) but says nothing about what a command does with the flag before that; an unknown flag is likely treated as prompt text and the command then prompts, which is the stall the contract exists to prevent. (c) Section 4 says coordinator-only commands get no `--unattended` mode (SPEC:128) with no behaviour if one is passed.
- Recommendation: one sentence for each of (a), (b), (c) in section 2.1. Priority: Medium.

### M-5 (Medium; MAJOR) WC-5 depends on a status vocabulary the unchanged contract writers are not shown to use

- Expert: Wiegers, Whittaker (Zero/Empty, Divergence). WC-4 says commands that already write a contract "keep their fields and add the missing ones" (SPEC:62), but workflow and brainstorm are unchanged (SPEC:84, 92, 154) and reflect and adversarial get only a filename or gate fix (SPEC:83, 88). The inventories show workflow's contract carries `status`, `plan_path`, `reflect_report_path` (INV-B:272); no inventory line shows the values of `status` for workflow, brainstorm, reflect or adversarial. WC-5 maps `failed`/`blocked`/other (SPEC:63) and 7.2 step 4 asserts `status` is one of four values and that `command` is set (SPEC:183). A report that exists but is empty, unparseable, or has a status outside the set is not mapped.
- Recommendation: state the mapping for a status outside the set (treat as `failed`) and for an empty file; list which unchanged commands need a field addition. Priority: Medium. UNVERIFIED: the real status values of those four contracts.

### M-6 (Medium; MAJOR) Several requirements have no acceptance check

- Expert: Crispin, Wiegers. Requirement-to-check trace:

| Requirement | Check in section 7 | Covered |
|---|---|---|
| WC-1 no prompt before ready | 7.2 step 1 `state: ready` (SPEC:180) | partial (only for the commands run) |
| WC-2 no person-blocking step | 7.2 step 5, AC-2.2 | yes |
| WC-3 questions to coordinator | none | no |
| WC-4 report file | 7.2 step 4, AC-1.4 | yes |
| WC-5 outcome mapping | 7.2 step 3 | yes |
| WC-6 resume or safe re-run | none | no |
| WC-7 top level | AC-0.4 transcript check | yes (P0 only) |
| WC-8 no Orca from commands | AC-C1 | yes (see N-5) |
| WC-9 no outward action | AC-2.4, AC-4.2 | two commands only |
| WC-10 wait splitting | AC-4.3 | pr-submit only; cli-eval has none (SPEC:104, 188-210) |
| WC-11 parallel-safe writes | AC-3.4 | save only |
| WC-12 pull-based follow-ups | none | no |

- Why Medium: a missing check is a requirement the document never states. Recommendation: add one check each for WC-3, WC-6, WC-12 and for cli-eval under WC-10, or say they are covered by the live check. Priority: Medium.

### M-7 (Medium; MAJOR) WC-10 trigger and AC-4.3 limit disagree; heartbeat relevance is unverified but not listed

- Expert: Whittaker (Divergence), Nygard. WC-10 splits a step "longer than 5 minutes" into waits of at most 4 minutes (SPEC:68). AC-4.3 requires "no single tool call exceeds 240 s" (SPEC:210). A 4.5-minute wait passes WC-10 and fails AC-4.3; the band is 240-300 s. Separately, whether Orca uses heartbeat age in its liveness verdict is UNVERIFIED (CAPS:130, CAPS:182 item 7), yet WC-10 turns heartbeat gaps into command edits for cli-eval (SPEC:104) and pr-submit (SPEC:114), and the spec's own UNVERIFIED list does not carry this item (SPEC:272-285).
- Recommendation: use one number (4 minutes) in both places and add the heartbeat question to the UNVERIFIED list. Priority: Medium.

### M-8 (Medium; MAJOR) Phase sequencing statements disagree with each other

- Expert: Wiegers, Fowler. (a) SPEC:43 says "Phase 0 therefore starts with live smoke runs"; the P0 row builds the contract file, the `KNOWN_CORE_FILES` change, the HOW-WE-WORK Orca section and the test file first, then runs the smoke runs, and its own rationale says the smoke runs "test the decision before anything is built on it" (SPEC:158). If AC-0.4 fails and "reopens section 1" (SPEC:194), the routing guide edit is already made. (b) SPEC:154 says "Phases 1-3 need no user decision" and SPEC:225 says they "can proceed on the recommendations"; D1 (SPEC:227-230), which every phase depends on (SPEC:51), is open.
- Recommendation: reorder P0 (smoke runs before the core and routing edits) or reword the two statements. Priority: Medium.

### M-9 (Medium; MAJOR) tasklist and reflect unattended handling covers the yes/no offer only

- Expert: Fowler, Nygard. The tasklist row resolves Stage 10.5 by passing `--unattended` to each reflect so "the headless rule applies" (SPEC:122). The inventory records that the headless rule auto-accepts "for auto-fixable registers" (INV-B:109), that Stage 10.5 `needs_human_decision` items HALT, and that "who answers that offer inside a subagent is not stated: UNVERIFIED" (INV-B:209, INV-B:322). The spec states neither the HALT case nor the UNVERIFIED, and its UNVERIFIED list carries no tasklist item (SPEC:272-285). A HALT inside N reflect subagents is a person-blocking step that WC-2 forbids (SPEC:60). The reflect row also changes `--remediate` handling although the brief says to omit `--remediate` (SPEC:88).
- Recommendation: state what a non-auto-fixable or `needs_human_decision` item does under `--unattended`, and carry INV-B:322 into the UNVERIFIED list. Priority: Medium.

### M-10 (Medium; MINOR-label raised to Medium) The index row asserts behaviour that its own source calls UNVERIFIED

- Expert: Wiegers, Adzic. The index row says "state that knowledge-base mode does not wait (whether it does is UNVERIFIED)" (SPEC:111; INV-A:54, INV-A:113). The business-panel and explain rows pin or refuse the doubtful mode instead (SPEC:102, 108). An implementer can write the sentence without making it true.
- Recommendation: refuse or pin the knowledge-base mode under `--unattended` like the other two rows. Priority: Low.

### M-11 (Medium; MINOR) WC-11 "must never write the same file" is not met by fixed-output ready commands

- Expert: Crispin. cleanup-audit's output dir is fixed and the row resolves it by serializing audits (SPEC:85); index-repo writes `PROJECT_INDEX.md` at a fixed location and its row only says to state the location (SPEC:86; INV-A:53). Two index-repo workers in one worktree write the same file.
- Recommendation: add the same serialization sentence to the index-repo row. Priority: Low.

### M-12 (Medium; MINOR) WC-9 "paid external run" is undefined

- Expert: Wiegers. WC-9 turns off any default that "calls a paid external run" (SPEC:67). cli-eval `run` executes `uv run superclaude eval run` (INV-A:44) and research and review-translation use web search (INV-B:134, INV-B:144); the rows do not say whether these count, and AC-2.x does not test it. Priority: Low.

### M-13 (Medium; MINOR) `partial` and audit-FAIL settle as Orca `succeeded`

- Expert: Hohpe. `partial` maps to `succeeded` on the assumption that "a partial run left a usable deliverable" (SPEC:263), and so does an audit with verdict FAIL (SPEC:63). A `succeeded` settlement completes the Task and satisfies any Task that depends on it (CAPS:90 states the failed case; `task_not_startable` rule at CAPS:88). Orca does not auto-start ready Tasks (CAPS:92) so the coordinator can still read the report first (SPEC:73); the spec does not require it to do so before starting dependents. Priority: Low.

### M-14 (Medium; MINOR) E2 overstates its evidence

- Expert: Wiegers. E2 says a command run by a worker "has the same tools as a command a person runs" (SPEC:22). The cited evidence shows the worker reached `state: ready, stage: input_accepted` and answered (CAPS:49 quoting EVIDENCE.md:45); it does not show the tool set. The spec elsewhere leaves MCP and Monitor availability UNVERIFIED (INV-A:112, INV-B:314). Priority: Low.

### M-15 (Medium; MINOR) WC-1 "well inside the readiness limit" has no number

- Expert: Wiegers. The evidence gives 30 s passing and about 45 s failing at a 45-second limit (CAPS:49, SPEC:59); the requirement text gives no figure for the 31-59 s range. Priority: Low.

## === ARCHITECTURE ANALYSIS ===

No blocking architectural finding. The decision rests on E1 to E6 (SPEC:19-26) and rejected-alternative reasons R1 to R5 (SPEC:31-37), each of which matches an inventory line (CAPS:92, 86, 161, 155, 97-101, 103, 145-150; INV-A:90; INV-B:285-286). Evidence gaps are stated plainly (SPEC:41-45). Architecture items are carried as M-3, M-4, M-8, M-9 above and N-4, N-5, N-12 below.

### Quantity Flow Diagram (FR-21; Pipeline Dimensional Analysis, triggered by the 43-command inventory feeding a 4-phase rollout)

```text
[Source: 43 commands, INV-A:3 (21) + INV-B:3 (22)]
  --> [Verdict split, SPEC:76] --> ready 10 | needs-change 27 | coordinator-only 6   (10+27+6 = 43, conserved)
        ready 10 (SPEC:83-92):   P1 fix 3 (adversarial, cleanup-audit, index-repo)
                                 P2 gate 4 (reflect, release-split, tdd, troubleshoot)
                                 no change 3 (brainstorm, init-lite, workflow)
        needs-change 27 (SPEC:99-125): P1 9 | P2 11 | P3 4 | P4 3          (9+11+4+3 = 27, conserved)
        coordinator-only 6 (SPEC:132-137)
  --> [Phase buckets by section 3 phase column]
        P1 = 3 + 9 = 12 --> Consumer AC-1.1 expects 12 (SPEC:195)
                         --> Section 6 P1 flag/section recipients = 8, or 9 with load (SPEC:159)   <-- MISMATCH (B-1)
        P2 = 4 + 11 = 15 --> Section 6 P2 list = 15 (SPEC:160)                                     (conserved)
        P3 = 4           --> Section 6 P3 list = 4 (SPEC:161)                                       (conserved)
        P4 = 3           --> Section 6 P4 list = 3 (SPEC:162)                                       (conserved)
        no phase = 3 + 6 = 9
  total = 12 + 15 + 4 + 3 + 9 = 43
```

Only the P1 consumer diverges (12 vs 8 or 9). All other stage counts match.

### Guard Condition Boundary Table (complete; FR-10 gate satisfied)

Trigger: the spec contains thresholds, boolean guards and sentinel comparisons. A class omitted for a guard has its one-line reason under the table. Every GAP is graded below the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 readiness fallback "well inside the limit" | SPEC:59 | Zero/Empty | no fallback (prompt waits) | violates WC-1 | forbidden: "must fall back on its own" | OK |
| G1 | SPEC:59 | Typical | fallback 30 s, limit 60 s | satisfies | passes, `EVIDENCE.md:45` via CAPS:49 | OK |
| G1 | SPEC:59 | Maximum/Overflow | fallback above about 45 s | violates | fails again, CAPS:49 | OK |
| G1 | SPEC:59 | Legitimate Edge Case | fallback 46-59 s against a 60 s limit | undefined | no number in the requirement text | GAP (M-15) |
| G2 WC-10 wait split | SPEC:68 | Typical | one poll iteration 600 s cumulative, split | true | split into iterations, session can heartbeat | OK |
| G2 | SPEC:68 | Maximum/Overflow | eval timeout 3600 s | true | split into waits of at most 4 minutes | OK |
| G2 | SPEC:68, 210 | Legitimate Edge Case | one wait of 270 s | false for WC-10 (not longer than 5 min), true for AC-4.3 | contradictory | GAP (M-7) |
| G3 WC-5 outcome mapping | SPEC:63 | Zero/Empty | no report exists | true | `--outcome failed` | OK |
| G3 | SPEC:63 | Zero/Empty | report file exists, empty or unparseable | unspecified | not stated | GAP (M-5) |
| G3 | SPEC:63 | Typical | `status: succeeded` | true | `--outcome succeeded` | OK |
| G3 | SPEC:63 | Legitimate Edge Case | `status: partial`; audit verdict FAIL | true | `--outcome succeeded`, first sentence states status and verdict | OK |
| G3 | SPEC:63 | Legitimate Edge Case | `status: blocked` | true | `--outcome failed` | OK |
| G3 | SPEC:62-63 | Sentinel Value Match | status value outside the four-value set | unspecified | not stated | GAP (M-5) |
| G4 `--unattended` token | SPEC:51, 228 | Zero/Empty | flag absent | false | today's behaviour, SA-1 | OK |
| G4 | SPEC:51 | Typical | standalone flag | true | unattended mode on | OK |
| G4 | SPEC:228 | Sentinel Value Match | `--unattended` inside a quoted topic argument | unspecified | not stated | GAP (M-4) |
| G4 | SPEC:154 | Legitimate Edge Case | flag passed to a command before its phase | unspecified | coordinator told not to; command behaviour not stated | GAP (M-4) |
| G4 | SPEC:128 | Legitimate Edge Case | flag passed to a coordinator-only command | unspecified | "get no `--unattended` mode"; behaviour not stated | GAP (M-4) |
| G5 WC-4 location rule | SPEC:62 | Zero/Empty | `--unattended` with no output flag | unspecified | not stated | GAP (M-1) |
| G5 | SPEC:62 | Typical | dir flag | true | `<dir>/return-contract.yaml` | OK |
| G5 | SPEC:62 | Typical | file flag | true | `<file>.return-contract.yaml` | OK |
| G5 | SPEC:62, 64 | Legitimate Edge Case | output path already holds a prior contract (retry/resume) | unspecified | not stated | GAP (M-3) |
| G5 | SPEC:99-123 | Legitimate Edge Case | row says only "add a report path" | unspecified | flag name and dir/file type not stated | GAP (M-1) |
| G6 WC-9 outward default off | SPEC:67 | Zero/Empty | no authorization in the brief | true | action stays off | OK |
| G6 | SPEC:67, 245 | Typical | authorization flag in the brief | true | action on | OK |
| G6 | SPEC:113, 121 | Legitimate Edge Case | action needs authorization but no flag exists (post-release, task, pr-submit) | unspecified | not stated | GAP (M-2) |
| G7 `/sc:task` confidence | SPEC:121 | Zero/Empty | confidence 0.0 | below 0.70 | blocked | OK |
| G7 | SPEC:121 | Typical | 0.85 | not below | proceeds (row names only the below-0.70 case) | OK |
| G7 | SPEC:121 | Legitimate Edge Case | exactly 0.70 | false ("below 0.70") | proceeds | OK |
| G7 | SPEC:121 | Maximum/Overflow | 1.0 | false | proceeds | OK |
| G8 AC-1.1 scope "phase is P1" | SPEC:195 | Typical | analyze | true | has the section | OK |
| G8 | SPEC:112, 195 | Legitimate Edge Case | load, phase cell "P1 (usage line only)" | true | row says no report; test requires `return-contract.yaml` | GAP (B-1) |
| G8 | SPEC:83, 85, 86, 195 | Legitimate Edge Case | adversarial, cleanup-audit, index-repo (phase P1, ready rows) | true | rows give no section and no contract | GAP (B-1) |
| G9 nesting depth | SPEC:33, 66 | Typical | depth 1 (this machine) | worker `worker-start` refused | WC-8: commands never call it | OK |
| G9 | SPEC:251-252 | Legitimate Edge Case | user raises depth (D5(b)) | n/a | D5 recommends keeping 1; WC-8 holds regardless | OK |

Classes left out, one line each:
- G1 One/Minimal: a fallback of 1 s behaves like Typical (satisfies); no separate behaviour.
- G1 Sentinel: no sentinel value is compared.
- G2 Zero/Empty and One/Minimal: a zero-length wait needs no splitting; not a distinct case.
- G2 Sentinel: no sentinel is compared.
- G3 One/Minimal and Maximum: the status is categorical, so there is no ordinal minimum or maximum; the empty and out-of-set cases are rows above.
- G4 One/Minimal and Maximum: the flag is present or absent; there is no count.
- G5 One/Minimal and Maximum: there is no count of contracts per path other than the retry case above.
- G5 Sentinel: no sentinel flag value is defined.
- G6 One/Minimal, Maximum, Sentinel: the guard is boolean (authorized or not).
- G7 Sentinel: no sentinel confidence value is defined.
- G8 Zero/Empty, Maximum, Sentinel: the guard is a membership test on a phase label.
- G9 Zero/Empty, One/Minimal, Maximum, Sentinel: depth is an Orca setting; the only values the spec reasons about are 1 and "raised".

GAP grading: G1 edge, G2 edge, G3 (two), G4 (three), G5 (three), G6 edge each name no concrete wrong outcome an implementer would produce from a stated text (they are requirements the spec never states), so each is Medium and listed in the M items. The G8 GAP rows are B-1.

## === ADVERSARIAL ANALYSIS (Whittaker) ===

- I can break this specification by **Divergence Attack**. The invariant at **SPEC:195 (AC-1.1)** fails when **the scope predicate "section 3 phase is P1" is evaluated against the rows**. Concrete attack: build exactly what SPEC:159 lists (8 commands get the section) -> run `test_worker_contract.py` -> the assertion over 12 P1 rows fails on load, adversarial, cleanup-audit and index-repo (4 failures, before: 8 pass, after: 4 fail). CRITICAL by FR-19; blocking: B-1.
- I can break this specification by **Divergence Attack**. The invariant at **SPEC:68 and SPEC:210** fails when **a wait lasts 270 s**. Concrete attack: a pr-submit poll step blocks 270 s -> WC-10 says compliant (not longer than 5 minutes) -> AC-4.3 says fail (over 240 s). MAJOR, Medium: M-7.
- I can break this specification by **Sentinel Collision Attack**. The invariant at **SPEC:51 and SPEC:228** (the switch cannot misfire on a person) fails when **the string `--unattended` appears inside a quoted topic**. Concrete attack: `/sc:tdd "explain the --unattended flag"` typed by a person -> command enters unattended mode -> its topic-only clarification gate resolves as blocked instead of asking, contradicting SA-1 (SPEC:146). MAJOR, Medium: M-4.
- I can break this specification by **Sequence Attack**. The invariant at **SPEC:62 and SPEC:64** (a contract reflects the current outcome) fails when **a retry reuses an output path and ends before writing**. Concrete attack: attempt 1 writes `status: blocked`; attempt 2 is killed at minute 3; the coordinator reads the file and sees attempt 1's result. MAJOR, Medium: M-3.
- I can break this specification by **Zero/Empty Attack**. The invariant at **SPEC:62** (a contract exists on every outcome, even a stop before other output) fails when **the brief passes `--unattended` with no output flag**. Concrete attack: `/sc:cli-eval run --unattended` (the AC-2.2 example, SPEC:200) -> blocked at the suite check -> no location rule -> contract written wherever the implementer chose, or not at all. MAJOR, Medium: M-1.
- I can break this specification by **Accumulation Attack**. The invariant at **SPEC:263** (a worker's own `failed` report does not trip the circuit breaker, CAPS:80) fails when **the same command blocks on the same gate repeatedly**. Concrete attack: a coordinator retries a blocked tdd Task 10 times with the same bare topic -> each run ends `failed` by WC-5 -> the breaker never counts it -> unbounded retries. MINOR: N-12.

## Follow-up candidates (Medium and minor; none fails the review, none enters the Reviser brief)

Medium: M-1 to M-15 above (headline list: M-1 contract location, M-2 authorization flags, M-3 stale contract, M-4 `--unattended` token rules, M-5 status vocabulary, M-6 acceptance coverage, M-7 4/5-minute band, M-8 phase sequencing wording, M-9 tasklist HALT, M-10 index KB mode, M-11 index-repo collision, M-12 "paid external run", M-13 `partial` settles, M-14 E2 wording, M-15 "well inside").

Minor notes:
- N-1: AC-C1, AC-C4, AC-C5 and others write the shell pipe and the alternation as `\|` inside code (SPEC:172, 175, 176). Rendered in a table it reads as `|`; copied from the raw file, `grep -E` treats `\|` as a literal pipe and AC-C1 would match nothing and "pass".
- N-2: UNVERIFIED #14 (SPEC:285) is a verification claim (a fresh `evidence-validator` re-read about 340 citations and found 9 defects), not an unverified item; it cannot be checked in this workspace.
- N-3: WC-4 names init-lite as a file-flag example (SPEC:62) although section 6 says init-lite is unchanged and never gets `--unattended` (SPEC:154). The contract has no version field (SPEC:62).
- N-4: SPEC:16 and SPEC:51 say the command-side change is "limited to" the worker contract and `--unattended` is "the only command-side change besides report files and resume"; section 3 and SA-4 add drift fixes, tools and frontmatter edits (SPEC:102, 108, 118-125, 149). WC-3 and WC-5 owner text does not say what a non-Orca unattended caller does without a preamble.
- N-5: AC-C1 and E5 scan `commands, skills, agents, core` (SPEC:25, 172); `hooks`, `templates`, `scripts` and the `plugins/superclaude/` mirror are not scanned (UNVERIFIED #8, SPEC:279). AC-C1 also scans `core`, where P0 adds the contract file and an Orca section in HOW-WE-WORK (SPEC:150, 158) that may name `orca orchestration` verbs; whether the grep would fire on them is unstated.
- N-6: the pr-submit top-level rule is cited as `SKILL.md:37-39` in `src` (SPEC:11, 65; INV-B:90) and as `:47-49` in the installed `~/.claude` copy (CAPS:40, CAPS:161): same quote, ten lines apart. UNVERIFIED which copy the spec's read used.
- N-7: help is coordinator-only because it writes nothing the coordinator can read (SPEC:134), while load also writes nothing and stays in the 27 needing change (SPEC:112, 139).
- N-8: `README:31` is a rule for this planning run and is cited as repo-wide evidence for git authorization and the WC-9 default (SPEC:67, 133).
- N-9: D2 says a Ruling is also accepted "from a valid existing operator Ruling" (SPEC:233); the inventories cite only the "clear user confirmation" clause (INV-A:51). UNVERIFIED.
- N-10: P4 "changes a deliberate safety rule" (SPEC:162) while D2's recommendation (a) keeps the rule (SPEC:234).
- N-11: 7.2 step 5 searches the transcript for the string `AskUserQuestion` (SPEC:184); a skill read through the Read tool can contain the word (INV-B:239 quotes "never AskUserQuestion"). The criterion says "call", so a careful reader distinguishes.
- N-12: no cap on how often a blocked Task is retried (see Accumulation Attack).

## Reviser brief

Blocking finding ids: B-1

Restated contract (the reviser reads the report, not the command): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Leave minor and Medium findings alone. For B-1 the text to repair is AC-1.1 and AC-1.2 (SPEC:195-196) and, only if needed to remove the contradiction, the P1 row of section 6 (SPEC:159) and the load row (SPEC:112). Narrow the criteria to the commands section 6 lists as flag recipients; do not add `## Unattended mode` to load, adversarial, cleanup-audit or index-repo.

verdict: FAIL
