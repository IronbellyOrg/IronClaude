review: 1 of 3

# Spec-panel critique, round 1: Orca worker-contract spec

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (57763 bytes, 285 lines), sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: none given, first review of the full document (no `--re-review`, no `--baseline`)
- reviewer model actually used: `claude-sonnet-5-5`
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full)
- panel (fixed review order, `command.md:99-113`): Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard (architecture); Whittaker (always active); Newman, Hohpe (architecture). Crispin, Gregory and Hightower are outside the requested focus areas and did not sit.
- brief clauses overridden: none. The brief did not widen scope or regrade anything (`command.md:264`).

Citation shorthand: `spec:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`. `command.md:N` = the `/sc:spec-panel` definition in the sandbox. `prompts:N` = the review-loop prompts file.

## What was covered, and what was not

Covered: the whole candidate (all 285 lines, sections 1-9, Decisions, UNVERIFIED list). Cross-checked against the three inventories (read in full) and the README.

Citations checked against files present in the workspace and found as cited:
- Every `CAPS:N` line the spec uses for Orca facts that I looked up (CAPS:44-47, 52, 58-61, 64, 66-68, 72-80, 84-92, 97-103, 107-116, 128-130, 135-139, 145-151, 155-162, 178, 180, 186-188). Each points at the capability the spec says it does.
- Every `INV-A:N` and `INV-B:N` row, note and summary line the spec uses (for example `INV-A:35-55`, `INV-A:76-83`, `INV-A:94-98`, `INV-B:31-52`, `INV-B:67-275` per-command ranges, `INV-B:289-299`, `INV-B:311`, `INV-B:320-323`).
- `README:6,11-17,30,31,35` match their use.
- The 10 / 27 / 6 split: `INV-A:73` (5 / 13 / 3) plus `INV-B:278` (5 / 14 / 3) gives 10 / 27 / 6, and the spec's section 3.1 table has 10 rows, section 3.2 has 27, section 4 has 6.

Not covered, marked UNVERIFIED: every citation of a file that is not in the workspace. That is `CLAUDE.md:*`, `src/superclaude/cli/install_core.py`, `src/superclaude/core/HOW-WE-WORK.md:*`, `pyproject.toml:38`, `Makefile:68-74`, all `cmd/*.md` and `sk/**` lines (they are checkable only through the inventory that quotes them), `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md:*`, `.dev/codegraph-migration/**`, the `grep` results at `spec:25`, and the spec's own claims of re-reading 11 locations (`spec:11`) and of an independent 340-citation check (`spec:285`). I did not treat any of these as wrong; I could not check them.

Advisory (`command.md:192`): the spec introduces 3+ mutable state variables (contract `status`, ledger, per-session memory keys) and guard thresholds (60 s, 5/4 min, 0.70, depth 1), so `--focus correctness` would be a reasonable follow-up run. Not forced.

## Guard Condition Boundary Table (hard gate, `command.md:311-334`)

Completed before synthesis. Classes left out are named in the "left out" line under each guard. `GAP` rows are graded per FR-8/FR-9: blocking only with a concrete wrong outcome, otherwise Medium (follow-up). None of the GAP rows below is blocking on its own; they feed Medium findings.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `unattended-switch` | spec:51, spec:60, spec:228 | Zero/Empty | flag absent | false | Today's behaviour, SA-1 (spec:146) | OK |
| `unattended-switch` | spec:51, spec:228 | Typical | `--unattended` as a flag in the brief | true | WC-2 gate resolution per command (spec:60) | OK |
| `unattended-switch` | spec:228 | Sentinel Value Match | the string `--unattended` inside quoted topic or spec text | unspecified | Not stated. D1(a) claims it "cannot misfire on a person" (spec:228) but defines no token rule. `command.md:459` defines one (standalone token outside quotes) | GAP (F11) |
| `unattended-switch` | spec:60 | Legitimate Edge Case | `--unattended` together with `--interactive` | unspecified | Section 3 refuses it for cleanup, improve, roadmap, explain (spec:103,108,110,118) but not for adversarial, brainstorm, release-split, where the brief only says "never" (spec:83,84,89) | GAP (F11) |
| `wait-split` (WC-10) | spec:68 | Zero/Empty | no long wait | false | Heartbeat every 5 min applies; nothing to split | OK |
| `wait-split` (WC-10) | spec:68 | Typical | one 10 min poll call | true | Split into waits of at most 4 min | OK |
| `wait-split` (WC-10) | spec:68 | Legitimate Edge Case | one call of 4 to 5 min | false | Not "longer than 5", not "at most 4"; unspecified | GAP (N2, minor) |
| `wait-split` (WC-10) | spec:68 | Maximum/Overflow | one foreground Agent-tool call that fans out 7-8 agents over many minutes | true by the text | Splitting is not possible for a subagent fan-out call; not addressed. Examples: cleanup-audit waves (INV-A:42), tdd 10+ agents (INV-B:221) | GAP (F8) |
| `outcome-map` (WC-5) | spec:63 | Zero/Empty | contract file present but 0 bytes or no `status` key | unspecified | Text covers "no report exists" only | GAP (F10) |
| `outcome-map` (WC-5) | spec:63 | Typical | `status: succeeded` | true | `--outcome succeeded` | OK |
| `outcome-map` (WC-5) | spec:63 | Sentinel Value Match | `status` outside the four values, as an existing contract may carry | unspecified | Not stated; WC-4 says existing contracts "keep their fields" (spec:62) | GAP (F10) |
| `outcome-map` (WC-5) | spec:63, spec:263 | Legitimate Edge Case | `partial`; audit verdict FAIL; `blocked` | true | `succeeded`, `succeeded`, `failed` | OK |
| `report-dir` (WC-4) | spec:62, spec:73 | Zero/Empty | no output directory passed under `--unattended` | unspecified | Not stated. `command.md:460` refuses before any work, which cannot also "write the contract on every outcome" (spec:62) | GAP (F11) |
| `report-dir` (WC-4) | spec:62 | Typical | directory passed and writable | true | `<output-dir>/return-contract.yaml` | OK |
| `report-dir` (WC-4) | spec:62, spec:87, spec:90, spec:120 | Sentinel Value Match | `--output` is a file path (tdd, init-lite, spec-panel) | unspecified | `<output-dir>` is never defined for a file-valued flag; `command.md:460` says "`--output` is file-valued" | GAP (F3) |
| `report-dir` (WC-4/WC-6) | spec:62, spec:64 | Legitimate Edge Case | retry worker given the same directory that already holds attempt 1's contract | unspecified | WC-6 says "fresh output directory"; WC-4 says the directory is fixed before dispatch | GAP (F4) |
| `confidence-gate` (task) | spec:121 | Zero/Empty | confidence 0.0 | true | Resolves as blocked | OK |
| `confidence-gate` (task) | spec:121 | Legitimate Edge Case | confidence exactly 0.70 | false | "below 0.70" blocks, so 0.70 proceeds (matches INV-B:199 "< 0.70") | OK |
| `depth-limit` (R1) | spec:33, spec:250 | Typical | depth 1 | true | `worker-start` from a worker refused (CAPS:97-99) | OK |
| `depth-limit` (R1) | spec:252 | Maximum/Overflow | depth raised to 2 or more | false | D5(b): rejected alternative becomes possible; stated as a user decision | OK |
| `readiness-limit` (WC-1) | spec:59 | Typical | startup prompt with a 30 s fallback | true | Passes (CAPS:49) | OK |
| `readiness-limit` (WC-1) | spec:59 | Maximum/Overflow | fallback longer than the limit | unspecified number | Text says "well inside" 60 s, no number; the evidence quote says about 45 s because that run used a 45 s limit | GAP (N8, minor) |

Left out: `unattended-switch` One/Minimal and Maximum (a single flag has no capacity); `wait-split` Sentinel (no sentinel value); `outcome-map` One/Minimal (same as Typical); `confidence-gate` Sentinel and Maximum (1.0 proceeds, no sentinel); `depth-limit` Zero and Sentinel (a malformed setting falls back to 1, CAPS:100); `readiness-limit` Zero and Sentinel (no value to test).

## Quantity Flow Diagram (FR-21; pipeline "43 commands to phases")

```text
[Source: 43 commands]                              spec:76, INV-A:3, INV-B:3
   --> [Stage 1: classify]
        --> [37 workers = 10 ready (spec:78-92) + 27 needs-change (spec:94-125)]
        --> [ 6 coordinator-only (spec:127-137)]   removed from the flow, no phase action
   --> [Stage 2: assign to phases, spec:156-162]
        P0 smoke runs   3 of the 10 ready                         (no command edits)
        P1  9 needs-change + 4 ready fixes   = 13   (analyze, build, business-panel, design,
                                                    document, explain, index, load, test;
                                                    adversarial, cleanup-audit, index-repo, workflow)
        P2 11 needs-change + 4 ready         = 15
        P3  4 needs-change                   =  4
        P4  3 needs-change                   =  3
        named with a phase action: 13 + 15 + 4 + 3 = 35
        brainstorm, init-lite: no row names a phase; covered only by the P1 blanket clause
          "--unattended accepted by every command in sections 3.1 and 3.2" (spec:159)   = 2
        total reached: 35 + 2 = 37  (count conserved)
   --> [Consumers]
        P1 scope text, spec:159:   expects 37 commands to accept --unattended
        AC-1.1, spec:195:          expects 37 commands to carry `## Unattended mode` naming return-contract.yaml
        AC-1.2, spec:196:          runs the 7.2 check, whose step 4 needs a contract, on "each P1 command" incl. load
        load row, spec:112 + Decision, spec:265:  gets "usage line only", no contract, no section   <-- MISMATCH (36 vs 37)
```

The only count mismatch is `load`. See F2.

## Standard-format summary

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  expert_panel: [Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe]
  focus_areas: [requirements, architecture]
quality_assessment:
  overall_score: 7.5
  clarity: 8
  completeness: 7
  testability: 6.5   # two acceptance checks cannot pass as written (F1, F2)
  consistency: 7
critical_issues:
  - {id: F1, severity: CRITICAL, expert: [Wiegers, Whittaker], category: acceptance-criteria}
  - {id: F2, severity: CRITICAL, expert: [Adzic, Whittaker],  category: acceptance-criteria}
adversarial_analysis: [F1 (Sequence Attack), F2 (Divergence Attack), F3, F4, F8, F10, F11]
```

## === REQUIREMENTS ANALYSIS ===

### Blocking findings

**F1. CRITICAL (blocking). Expert: Wiegers (testability), Whittaker (Sequence Attack). The P0 live check demands a contract that the same row says does not exist yet.**

- Grading sentence: an implementer who follows the stated text as written builds a P0 gate whose step 3 requires the worker's report path to be "the WC-4 contract path" and its outcome to match "the contract's `status`" (`spec:182`), and the same acceptance row says "step 4 uses the command's existing report file, since the contract arrives in P1" (`spec:194`). The WC-4 contract is written only by P1 changes (`spec:159`), and P0 has "no command edits" (`spec:158`). So AC-0.4 step 3 cannot pass for any of its three commands, and Section 6 says "Later phases do not start until the earlier phase's checks in section 7 pass" (`spec:154`), so P1 can never start.
- I can break this specification by **Sequence Attack**. The invariant at **spec:154** (P1 starts only after P0's checks pass) fails when **AC-0.4 (spec:194) lists step 3 among the steps that must pass while step 3 (spec:182) requires an artifact only P1 creates**. Concrete attack: before P1, run `/sc:troubleshoot "<symptom>"` as a worker; it writes `REPORT.md` (`spec:91`) and no `return-contract.yaml`; the worker sends `worker_done --report-path REPORT.md`; the coordinator checks step 3 "report path is the WC-4 contract path": false. State before: P0 open, P1 blocked. State after: P0 still open, P1 still blocked. `/sc:workflow` (`spec:92`) and `/sc:adversarial` (`spec:83`) fail the same way.
- Recommendation: restate step 3's pass condition for P0 as "exactly one `worker_done`; `--outcome` matches the worker's own account; the report path is the command's existing report file", with the WC-4 wording applying from P1 on. Narrow one clause; add nothing.
- Priority: High. Quality impact: unblocks the only gate that tests the decision itself (`spec:43`, `spec:272`).

**F2. CRITICAL (blocking). Expert: Adzic (concrete examples), Wiegers, Whittaker (Divergence Attack). Two acceptance checks and the `load` row contradict each other.**

- Grading sentence: an implementer who follows the stated text as written gives `/sc:load` "usage line only" and no report file (`spec:112`, `spec:159`, Decision at `spec:265`: "a report file would be an unrequested addition. Only its usage-line defect is fixed"), and `load` is also named as a P1 command (`spec:159`). AC-1.1 asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` (`spec:195`), and AC-1.2 runs the 7.2 live check on each P1 command (`spec:196`), whose step 4 needs a contract file (`spec:183`). `load` is in section 3.2 (`spec:112`). So AC-1.1 and AC-1.2 cannot pass for `load` without breaking the stated Decision, and P1 cannot be declared passed.
- I can break this specification by **Divergence Attack**. The invariant at **spec:195** ("every command in sections 3.1-3.2") fails when **one command in the quantified set is explicitly exempt from the property (spec:112, spec:265)**. Concrete attack: the test iterates the 37 commands (Quantity Flow Diagram); 36 have the section, `load.md` has none (usage-line fix only); `uv run pytest tests/skills/test_worker_contract.py` fails; adding the section to make it pass makes `load` name a contract it never writes, or adds the "unrequested" report file the Decision rejects.
- Recommendation: either move `load` out of the AC-1.1 and AC-1.2 sets in one clause ("except `load`, usage-line fix only"), or move it to the list of commands that are not dispatched. Do not add a report file.
- Priority: High.

## === ARCHITECTURE ANALYSIS ===

No architecture finding reaches blocking. The decision itself (Orca on top, commands stay units, `spec:13-39`) is supported: its load-bearing Orca facts check against `CAPS:97-103` (depth 1), `CAPS:76` and `CAPS:150` (`worker_done` bound to the dispatched pane), `CAPS:145-149` (standalone behaviour). The rejected alternative R1-R5 (`spec:31-37`) follows from those lines. Fowler and Newman raise only Medium items below.

## Medium findings (warnings; follow-up candidates, never in the Reviser brief)

Each is a requirement the text leaves open or a conflict that needs a guess about which reading an implementer picks. Grading: Medium.

**F3. Medium. Wiegers, Fowler. WC-4's `<output-dir>/return-contract.yaml` is undefined for file-valued `--output` and for commands whose report path is not known before dispatch.** WC-4 says the path is "known before dispatch" and sits in "the directory the coordinator passed (`--output` / `--output-dir`)" (`spec:62`, `spec:73`). Rows contradict or leave it open: tdd, init-lite and spec-panel take a file-valued `--output` (`spec:87`, `spec:90`, `spec:120`; `command.md:460` says "`--output` is file-valued"); workflow's contract lives at `.dev/tasks/to-do/<id>/` with `<id>` created at run time and no output flag (`spec:92`; INV-B:272); troubleshoot's directory is `.dev/troubleshoot/<slug>-<timestamp>/` (INV-B:242); research's file name has a run-time timestamp and the row names no output flag (`spec:116`; INV-B:132); cleanup-audit (`spec:85`) and index-repo (`spec:86`) write to fixed locations; adversarial's row moves the contract to `<output>/adversarial/` (`spec:83`), not `<output-dir>/`. A reading that places a file-valued command's contract in the file's parent directory (for example `docs/<domain>/return-contract.yaml`) is allowed by the text and lets two workers overwrite each other (WC-11, `spec:69`). Recommend: one sentence that defines the contract path for a file-valued flag and lets a row override WC-4 with its own stated path.

**F4. Medium. Nygard, Fowler. WC-6 "writes each run into a fresh output directory" conflicts with WC-4's directory fixed before dispatch (`spec:62`, `spec:64`, `spec:73`).** About 20 rows say only "fresh dir" and need no command change (for example `spec:99`, `spec:101`, `spec:106`). If the coordinator reuses the brief on `--retry-of`, the retry writes into the first attempt's directory; if the command creates a new subdirectory, the contract is no longer where the brief said. The text does not say who allocates the fresh directory.

**F5. Medium. Cockburn, Wiegers. Section 2.3 requires `--unattended` in every worker command line, but the 10 "ready today" commands and the three P0 smoke runs do not have the flag until P1 (`spec:73`, `spec:79`, `spec:158-159`, `spec:194`).** AC-0.4 lists the smoke commands without it. A P0 brief template written from 2.3 would pass an unknown flag to commands that have no section for it.

**F6. Medium. Nygard, Whittaker (Sequence Attack). Between P1 and P2-P4 a command accepts `--unattended` but still has its gate.** P1 adds "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" (`spec:159`), while gate resolutions for 15 commands land in P2, four in P3, three in P4 (`spec:160-162`). A coordinator that reads the P1 contract could dispatch `/sc:cleanup --unattended` and get the silent stall WC-2 forbids (`spec:60`). The text does not say a not-yet-converted command refuses the flag or that the brief template lists which commands are converted.

**F7. Medium. Newman, Wiegers. WC-3 lets an `ask` answer re-enter as a flag, with no limit on the kind of gate.** WC-3: the session "may instead ask the coordinator once ... then re-invoke or resume the command with the answer as a flag" (`spec:61`). For `/sc:implement`, a Ruling must not come from "another agent" (INV-A:51, INV-A:66) and D2(a) says the worker "stops ... and ends `failed`" (`spec:234`); implement's Ruling is not a flag. For outward actions WC-9 says authorization comes through "the command's own explicit flag written in the brief" (`spec:67`) and D4(a) wants the user's own instruction quoted (`spec:245`). WC-3 as written also allows a coordinator `ask` answer to become an authorization. Recommend: one clause that WC-3 does not apply to safety-rule rulings (D2) or outward-action authorization (D4).

**F8. Medium. Nygard, Whittaker. WC-10's scope reaches calls that cannot be split.** "A command step that blocks a single tool call for longer than 5 minutes ... must be split into waits of at most 4 minutes" (`spec:68`). A foreground Agent-tool fan-out (cleanup-audit waves of 7-8 agents, INV-A:42; tdd 10+ agents, INV-B:221; adversarial, INV-A:35) is one such call, and those commands are marked ready with no WC-10 row (`spec:83,85,90`). Whether a missed heartbeat has any effect is itself UNVERIFIED (`CAPS:182`, item 7). Recommend: scope WC-10 to waits the command controls (poll, sleep, eval) and say so.

**F9. Medium. Hohpe, Fowler. AC-C1 cannot pass for the P0 deliverables as the spec describes them.** AC-C1 requires zero matches of `orca(-ide) orchestration|worktree|terminal|agent` under `src/superclaude/core` (`spec:172`), while P0 adds `WORKER-CONTRACT.md` to `core/` (`spec:52`, `spec:158`) and an "Orca section" to `HOW-WE-WORK.md` in `core/` (`spec:158`), and SA-2 explicitly allows Orca mentions in the contract file (`spec:147`). Any natural Orca section that names a coordinator command trips the check. Recommend: align the grep paths with SA-2 or exclude the two named files.

**F10. Medium. Wiegers, Whittaker (Sentinel Collision). The fixed four-value `status` is never checked against the contracts that already exist.** WC-4 says commands that already write a contract "keep their fields" (`spec:62`); the Decision fixes `succeeded / partial / failed / blocked` (`spec:262`); 7.2 step 4 asserts `d['status']` is one of the four (`spec:183`). The spec does not state the `status` values workflow, brainstorm, reflect and adversarial use today (INV-B:272, INV-A:39, INV-B:112, INV-A:35 name the files, not the values), and gives no rule for an empty or key-less file (WC-5, `spec:63`). UNVERIFIED whether they match.

**F11. Medium. Whittaker (Zero/Empty and Sentinel attacks), Wiegers. Three unspecified input cases for the switch and the report directory.** (a) No token rule for `--unattended`: D1(a) says it "cannot misfire on a person" (`spec:228`) but a topic or spec text that contains the string is not addressed; `command.md:459` shows the rule is writable. (b) `--unattended` with `--interactive` is refused in some rows (`spec:103,108,110,118`) and only discouraged in others (`spec:83,84,89`), while WC-2 says no `AskUserQuestion` at all (`spec:60`). (c) No output directory under `--unattended`: WC-4 says the contract is "written on every outcome, including stops before any other output exists" (`spec:62`), but with no directory there is nowhere to write it (`command.md:460` refuses in chat only).

**F12. Medium. Fowler. Section 6 calls P1 "commands with no gate" but P1 includes four commands that have a gate row.** `explain` (`--format interactive` refused, `spec:108`), `business-panel` (socratic refused, `spec:102`), `test` (`--watch` refused, `spec:123`), `index` (knowledge-base statement, `spec:111`). The gate-trigger acceptance check (AC-2.2, `spec:200`) is defined for P2 commands only, so P1 never tests those refusals.

**F13. Medium. Wiegers. WC-1 has no owner, phase or acceptance check.** WC-1 is owned by "Launch setup, not commands" (`spec:59`), no phase in `spec:156-162` implements it, and 7.2 step 1 (`spec:180`) only observes `state: ready`. Whether the launch path is already fixed is stated only as an observation (`CAPS:49`). It is a requirement nobody is told to build or verify.

**F14. Medium. Cockburn, Newman. D4(a) and D2(a) treat a relayed approval differently.** D2(a) rejects a relayed Ruling because "the rule exists to stop an agent approving its own work" (`spec:236`); D4(a) accepts a coordinator-quoted user instruction for push, PR and install (`spec:245-247`) and says it "matches the repo's own rule" that the user pre-authorized the step "this session". INV-B:79 quotes the rule as "unless the user pre-authorized them this session"; a brief is another agent's message in a different session. The recommendation is the user's to make, but the stated justification overstates the match.

## Minor findings (notes)

- **N1.** Tasklist row says its reflect fan-out "runs one layer below the worker" (`spec:122`). INV-B:210 describes N subagents each running reflect, which spawns its own agents (a second layer), and says nested spawning is UNVERIFIED (INV-B:314). The cited limit (INV-A:14, three layers) still holds; the "one layer" wording is imprecise.
- **N2.** WC-10 leaves single calls of 4 to 5 minutes unspecified (`spec:68`); harmless because the worker can heartbeat between calls.
- **N3.** SA-1 and SA-3 say standalone defaults and written files stay as today (`spec:146`, `spec:148`) while the defect fixes in SA-4 (`spec:149`) change defaults, for example the validate-tests default target (`spec:125`) and the adversarial contract filename (`spec:83`). SA-4 reconciles this in prose; the three statements could name the exception once.
- **N4.** Section 4's last sentence says pr-submit "stays a worker candidate only if the user accepts open decision D3" (`spec:139`); D3 has two options and only (b) makes it a worker.
- **N5.** E3 cites `invocation_method: "skill-direct"` as proof the route worked (`spec:23`) and section 1.4 says the same run proves only the nested route (`spec:43`). INV-A:13 reads it as the direct route. The spec's cautious reading is the safer one; the two places could agree.
- **N6.** `/sc:git` is coordinator-only because its operations "need the user's authorization in this repo" and the cited support is `README:31` (`spec:133`), a rule for the workers of this run, not a repo rule. INV-A:49 cites the same line.
- **N7.** "Phases 1-3 need no user decision" (`spec:154`) sits next to D4, which lists auggie-review `--post-pr` and task `commit`/`push`, both P2 rows (`spec:244`, `spec:100`, `spec:121`). `spec:225` says P0-P3 may proceed on the recommendations, so the two lines can be read together.
- **N8.** WC-1 gives no number: "well inside the readiness limit (default 60 s)" (`spec:59`), and the evidence quote of "about 45 s" comes from a run that used a 45 s limit (CAPS:49).

## Expert consensus and disagreement

- Consensus: the decision and the rejected alternative are well supported by checked lines; the contract vocabulary (`succeeded / partial / failed / blocked`, `spec:262`) is a sound reuse; the phase order by risk is reasonable (`spec:267`).
- Consensus: both blocking findings are small text repairs and do not change any decision or phase.
- Disagreement (not resolved): Newman would grade F7 as blocking on safety-boundary grounds; Nygard held it Medium because the outward-action rows resolve to "off", not "blocked", so WC-3 does not naturally reach them (`spec:113`, `spec:67`). Graded Medium: the reading needs a guess.

## Follow-up candidates

Medium: F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, F13, F14. Minor: N1, N2, N3, N4, N5, N6, N7, N8. These never trigger a revision, never fail a review and are not in the Reviser brief. The issue offer (`command.md:260`): the session that ran this review is a worker whose reply is limited to the output path, so it asked nothing and created no issue. The list is only recorded here for the coordinator to put to the user once.

## Reviser brief

Blocking finding ids to repair, and only these: **F1, F2**. The reviser reads this report, not the command. Rules (restating `command.md:263`):
- Revise only text a blocking finding names.
- Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size before and after (candidate was 57763 bytes, sha256 `d3cdbe57...25200d`), with the bytes added and deleted per finding id.
- Leave Medium and minor findings alone (F3-F14, N1-N8), including through any "apply all findings" wording.
- Return the candidate once and do not award yourself a PASS.

Suggested scope: F1 touches `spec:182` and `spec:194`; F2 touches `spec:195` and `spec:196` (or `spec:112` and `spec:159`).

verdict: FAIL


## Findings block

```findings-v1
{"id": "F1", "severity": "CRITICAL", "blocking": true, "category": "unpassable-check", "anchor": "its report path is the WC-4 contract path", "anchor2": "step 4 uses the command's existing report file, since the contract arrives in P1", "refs": ["AC-0.4", "WC-4"], "claim": "The P0 check demands a contract the same row says does not exist before P1."}
{"id": "F2", "severity": "CRITICAL", "blocking": true, "category": "contradiction", "anchor": "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`", "anchor2": "use it as a step inside another worker's brief, not as its own Task", "refs": ["AC-1.1", "AC-1.2"], "claim": "The load row says no section and no report, but the P1 checks require both for load."}
```
