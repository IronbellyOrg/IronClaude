review: 1 of 3

# Spec-panel review, round 1: Orca worker-contract spec

| Field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (57763 bytes, 285 lines) |
| sha256 (candidate) | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` |
| Baseline | none (no `--re-review`, no `--baseline`: first review of the full document) |
| Reviewer model actually used | `claude-sonnet-5-5` |
| Review date | 2026-11-10 |
| Prompt followed | FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (home resolved to the sandbox `home/`), read in full before reviewing |
| Brief clauses overridden | none |

Citation shorthand: `spec:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. Everything under `src/`, `.dev/codegraph-migration/`, `.dev/evals/`, `CLAUDE.md` and `~/.claude` is not in the sandbox, so a citation that points only there is UNVERIFIED.

## Coverage (what was covered)

- Read in full: the candidate (285 lines), `README.md`, all three inventories, `command.md`, the review-loop prompts.
- Cross-checked: every `INV-A:`, `INV-B:` and `CAPS:` line target used in spec sections 1 to 4 against the inventory line (all aligned); sections 5 to 9 spot-checked.
- Count check: the section 3 split 43 = 10 ready + 27 needs-change + 6 coordinator-only matches `INV-A:73` (5+13+3) and `INV-B:278` (5+14+3). I enumerated the 10 rows at `spec:83-92`, the 27 rows at `spec:99-125` and the 6 rows at `spec:132-137`. Phase assignments in the section 3 rows match the section 6 table (`spec:159-162`).
- Not covered, UNVERIFIED: all `src/superclaude/...` line citations the spec carries from the inventories (`spec:11`), the claim that `cmd/` holds exactly 43 commands, `EVIDENCE.md`, and the PR #329 run files. The inventory texts that quote them are what I checked.
- Focus: requirements and architecture. All 11 panel experts spoke; Whittaker's attacks are in the findings.

## Verification block

None. This is a first review; the VERIFY step is the coordinator's.

## Panel record (review order)

1. **Wiegers**: the three blocking findings are requirement conflicts, not gaps: two stated texts cannot both be implemented (F-01, F-02, F-03). Traceability is otherwise strong (every WC has an evidence cell). WC-1, WC-3 and WC-12 have no acceptance check (F-10).
2. **Adzic**: examples are good where given (`spec:228`, `spec:200`). "Well inside the readiness limit" (`spec:59`) has no number.
3. **Cockburn**: primary actor and goal are clear (coordinator, run a command with no person). The second actor, the person who later runs the same command, is protected by SA-1 to SA-6. The coordinator's stall handling is a missing goal step (F-11).
4. **Fowler**: one shared contract file plus a short per-command section is the right seam (`spec:52`, `spec:264`). The coupling defect is the contract path: WC-4 states one rule, the rows state three (F-03).
5. **Nygard**: failure modes of the contract itself are thin: stale report, empty report, never-answered `ask` (F-06, F-07). The silent-stall mode is named (`spec:44`) but the coordinator is given no ceiling (F-11).
6. **Whittaker**: attacks below, in the finding text and in the Guard Condition Boundary Table.
7. **Newman**: the interface between coordinator and command is a flag (`--unattended`) plus a file. Versioning of that interface is not stated (a `return-contract.yaml` with no schema or version field, `spec:62`). Noted in N-05.
8. **Hohpe**: the exchange is message-then-pointer (`worker_done --report-path`, `spec:62-63`). Orca does not check the pointer (`CAPS:79`); the spec handles this by making the coordinator open the file. Two completion routes exist for a blocked gate (blocked report at `spec:60`, `ask` at `spec:61`) and the coordinator cannot tell in advance which it will get; acceptable, but only the first is tested (F-10).
9. **Crispin**: the static test plus live check design is sound. The common checks have edge defects (F-12, F-13). Unreachable P0 check: F-01.
10. **Gregory**: quality expectations per phase are explicit (`spec:166-210`); the open decisions are self-contained and each has a recommendation.
11. **Hightower**: operational concerns are covered by the cites to Orca release, retry and liveness (`spec:73`, `spec:68`); stall policy is the gap (F-11).

## Guard Condition Boundary Table

Hard gate (FR-10): produced before synthesis. A spec with threshold checks, boolean guards and sentinel flags triggers it. Guards: G1 the `--unattended` switch (`spec:51`, `spec:60`), G2 the wait-size rule WC-10 (`spec:68`), G3 the outcome mapping WC-5 (`spec:63`), G4 the outward-action default WC-9 (`spec:67`), G5 the readiness fallback WC-1 (`spec:59`), G6 the `ask` loop WC-3 (`spec:61`), G7 the retry rule WC-6 (`spec:64`). Classes left out are listed in one line each under the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 `--unattended` | spec:51, 60, 146 | Zero/Empty | flag absent | false | today's behavior exactly (SA-1, `spec:146`) | OK |
| G1 `--unattended` | spec:62, 99 | One/Minimal | flag present, no output dir or output file given | true | none: WC-4 needs `<output-dir>` "the coordinator passed"; analyze row says "add `--output`" without saying what happens when it is missing | GAP (F-04) |
| G1 `--unattended` | spec:62, 228 | Typical | flag plus `--output <dir>` | true | contract at `<output-dir>/return-contract.yaml` | OK |
| G1 `--unattended` | spec:228 | Sentinel Value Match | the literal text `--unattended` inside a quoted free-text prompt (for example `/sc:troubleshoot "login fails --unattended"`) | true or false, unspecified | none; D1 says it "cannot misfire on a person" | GAP (F-05) |
| G1 `--unattended` | spec:128 | Legitimate Edge Case | flag passed to a section 4 command (`/sc:git`) | true | none; section 4 says those commands "get no `--unattended` mode" but not whether the flag is refused, ignored or accepted | GAP (F-05) |
| G2 wait split | spec:68 | Zero/Empty | no blocking call | false | none needed | OK |
| G2 wait split | spec:68 | Typical | single call of 240 s | false | allowed, heartbeat fits between calls | OK |
| G2 wait split | spec:68, 114, 266 | Maximum/Overflow | single call between 240 s and 300 s | false (rule fires only "longer than 5 minutes") | none: not split, and heartbeat cadence is 5 min (`spec:68`, `CAPS:130`); pr-submit row uses "under 4 minutes" (`spec:114`) | GAP (F-09) |
| G2 wait split | spec:68, 104 | Legitimate Edge Case | one eval of 3600 s (`spec:68`) | true | split into waits of at most 4 min (cli-eval row, `spec:104`) | OK |
| G3 outcome mapping | spec:63 | Zero/Empty | report file exists but is empty or has no `status` key | unspecified | none: only "no report exists" maps to failed | GAP (F-07) |
| G3 outcome mapping | spec:63 | Typical | `status: succeeded` | true | `--outcome succeeded` | OK |
| G3 outcome mapping | spec:62, 63 | Sentinel Value Match | existing contract whose `status` vocabulary differs from the four values (WC-4 says existing contracts "keep their fields") | unspecified | none: keep fields versus fixed four-value set (workflow vocabulary UNVERIFIED, `INV-B:272`) | GAP (F-07) |
| G3 outcome mapping | spec:62, 64 | Legitimate Edge Case | stale `status: succeeded` file from a first attempt in the same dir; retry worker dies before writing | true | none; worker would report succeeded | GAP (F-06) |
| G4 outward default | spec:67 | Zero/Empty | no authorization in brief | off | outward actions off | OK |
| G4 outward default | spec:67, 113, 121 | Legitimate Edge Case | `/sc:task` EXEMPT `commit`/`push`, or `/sc:post-release` VM and PR | off unless "the command's own explicit flag" | no such flag is named for task or post-release (rows say "unless authorized") | GAP (F-08) |
| G5 readiness | spec:59 | Typical | fallback 30 s | passes | start succeeds (`EVIDENCE.md:45` via `CAPS:49`) | OK |
| G5 readiness | spec:59 | Maximum/Overflow | fallback above about 45 s | fails | spec says "well inside (default 60 s)" but gives no number; the cited evidence says above about 45 s fails again | GAP (F-10, minor aspect) |
| G6 `ask` loop | spec:61 | Zero/Empty | session holds no preamble | ask unavailable | falls to blocked report (`spec:61` "holds a preamble") | OK |
| G6 `ask` loop | spec:61 | Maximum/Overflow | coordinator never answers; repeated timeouts | unspecified | resume the same message ID; no cap on repeats and no stop rule | GAP (F-11) |
| G7 retry rule | spec:64 | Typical | command has a resume flag, brief passes it | true | resumes | OK |
| G7 retry rule | spec:62, 64, 205 | Legitimate Edge Case | no resume flag and the coordinator passes the same output dir again | unspecified | WC-6 says "fresh output directory" but WC-4 fixes the dir the coordinator passed; AC-3.2 expects "starts fresh" in a dir that already holds `.session-memory.md` | GAP (F-06) |

Classes left out: G1 Maximum (boolean flag, no capacity); G2 One/Minimal (a 1 s wait behaves like Typical); G2 Sentinel (no sentinel in a duration); G3 Maximum (four-value enum); G4 One, Typical, Sentinel, Maximum (a flag is present or absent; the present case is the "turns on" half of `spec:67`); G5 Zero, One, Sentinel (a fallback of 0 s is not a design choice); G6 One, Typical, Sentinel (one `ask` and its answer is the normal path in `spec:61`); G7 Zero, One, Sentinel, Maximum (no countable input).

Status GAP rows are graded under FR-8 and FR-9: none names a concrete wrong outcome without a further assumption, except where a finding below is marked blocking. All the GAP rows are carried as Medium findings F-04 to F-11 under `follow-up candidates`. GAP rows are the priority invariant candidates for `sc:adversarial` AD-1.

Pipeline Dimensional Analysis: not triggered (no multi-stage data flow whose output count differs from input count). The one count flow is the command partition 43 = 10 + 27 + 6, which conserves (checked above). Advisory: the spec has numeric thresholds (4 min, 5 min, 60 s, depth 1), so a later round may add `--focus correctness`.

## Findings

Grading used: CRITICAL is blocking. A MAJOR is blocking only if the grading sentence below holds with no further assumption; otherwise it is Medium. For each blocking finding the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y" is written out.

=== REQUIREMENTS ANALYSIS ===

### F-01 (CRITICAL, blocking): P0 acceptance check AC-0.4 cannot pass, and P0 gates every later phase
- Expert: Wiegers (testability), Crispin (acceptance criteria), Whittaker (sequence).
- Quoted texts and locations:
  - `spec:158`: P0 is "(no command edits)".
  - `spec:154`: "Later phases do not start until the earlier phase's checks in section 7 pass."
  - `spec:182` (7.2 step 3) pass condition: "exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path."
  - `spec:194` (AC-0.4): "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1."
  - `spec:91-92`: the P0 commands report `REPORT.md` (troubleshoot) and `.dev/tasks/to-do/<id>/return-contract.yaml` (workflow); `INV-B:242` says troubleshoot writes `return-contract.yaml` only with `--caller task-unified`.
- Grading sentence: An implementer who follows AC-0.4 and step 3 as written runs the three P0 smoke runs on unedited commands, and the check can never pass, because step 3 is required to pass and demands a WC-4 contract and a contract `status` that P0 commands do not write until P1; only step 4 is carved out. Since `spec:154` forbids starting P1 until P0 passes, the whole rollout is blocked, and `spec:194` says a failure "reopens section 1".
- Recommendation: carve step 3's contract clauses out of AC-0.4 the same way step 4 is carved out (keep "exactly one `worker_done`" and take the report path from the command's existing report file). Rationale: narrowing the check, not adding a mechanism.
- Priority: High. Quality impact: Consistency +1, Testability +1.

### F-02 (CRITICAL, blocking): AC-1.1 requires an `## Unattended mode` section naming `return-contract.yaml` in commands the spec says get no contract or no change
- Expert: Wiegers (consistency), Crispin.
- Quoted texts and locations:
  - `spec:195` (AC-1.1): "the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
  - `spec:112`: load row: report "none (see note)", resume "n/a", "P1 (usage line only)".
  - `spec:265` (Decisions): load: "a report file would be an unrequested addition. Only its usage-line defect is fixed."
  - `spec:79`: 3.1 intro: "The only command changes are the small fixes in the last column"; `spec:84` and `spec:87` give "None" for brainstorm and init-lite.
- Grading sentence: An implementer who follows AC-1.1 as written adds an `## Unattended mode` section naming `return-contract.yaml` to `load.md` (and to brainstorm and init-lite), and that is wrong because the same document says load gets no report file and only a usage-line fix, and that the ready commands change only through the "small fix" column; if the implementer follows those rows instead, AC-1.1 fails. The two stated texts cannot both be satisfied.
- Recommendation: narrow AC-1.1 to the commands that gain a contract (exclude load), and state in `spec:79` that every 3.1 command also gains the `## Unattended mode` section in P1 (or drop it for brainstorm and init-lite). One sentence either way.
- Priority: High. Quality impact: Consistency +1.

### F-03 (CRITICAL, blocking): WC-4 fixes one contract path, but the adversarial and workflow rows and the live check use other paths
- Expert: Fowler (interface consistency), Wiegers, Whittaker (divergence).
- Quoted texts and locations:
  - `spec:62` (WC-4): the command "writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)".
  - `spec:83`: adversarial: brief passes `--output <dir>`; fix is "the contract filename to `<output>/adversarial/return-contract.yaml`"; `spec:198` (AC-1.4) checks that adversarial "names one fixed path".
  - `spec:92`: workflow: brief passes `--handoff none` (no output flag); report is `.dev/tasks/to-do/<id>/return-contract.yaml`, an id the command generates.
  - `spec:182` (step 3) and `spec:196` (AC-1.2): the worker's report path must be "the WC-4 contract path" for each P1 command.
- Grading sentence: An implementer who follows WC-4 puts adversarial's contract at `<dir>/return-contract.yaml`, while the adversarial row and AC-1.4 put it at `<dir>/adversarial/return-contract.yaml`; for workflow there is no coordinator-passed directory at all and the id is created by the command. AC-1.2 step 3 then requires the worker's report path to equal the WC-4 path, which one of the two stated paths cannot meet. Two stated texts contradict each other on the path of the same file, and the file's path is what the coordinator opens (`spec:62`, `spec:73`).
- Recommendation: restate WC-4 so the path is "the fixed path the command's `## Unattended mode` section names", and have the 3.1 and 3.2 rows list that path. This narrows WC-4 and removes the single-path claim; no new mechanism.
- Priority: High. Quality impact: Consistency +1, Completeness +0.5.

### F-04 (MAJOR graded Medium): contract location undefined when `--unattended` has no directory, or `--output` names a file
- Expert: Wiegers, Whittaker (Zero/Empty attack).
- Texts: `spec:62` (`<output-dir>` is "the directory the coordinator passed"); `spec:90` and `spec:87` (tdd and init-lite take `--output <file>`); `spec:120` (spec-panel gains `--output`); `spec:99` (analyze "add `--output`"); `spec:73` (the brief states "the output directory").
- Concrete attack: **Zero/Empty Attack.** The invariant at WC-4 (`spec:62`) fails when `--unattended` is passed without a directory flag or with a file `--output`. State trace: before, `/sc:tdd "<component>" --unattended --output docs/x.md`; the contract path becomes `docs/x.md/return-contract.yaml` or the parent directory, unspecified; after, the coordinator's "known before dispatch" path (`spec:62`) is not known. The same hole exists for a pre-creation workflow STOP (`spec:92`): no package id exists yet to hold the contract.
- Why Medium: the sentence needs the guess that the implementer picks the worse of two readings (parent directory versus failure). The document never states a requirement (`spec:62`) for this case.
- Recommendation: add one clause to WC-4: with `--unattended` and no directory, the command is blocked and says so in chat; for a file `--output`, the contract sits beside the file. Priority: High. Quality impact: Completeness +1.

### F-05 (MAJOR graded Medium): `--unattended` collides with quoted prompt text and has no stated behavior on section 4 commands
- Expert: Whittaker (Sentinel Collision Attack), Cockburn.
- Texts: `spec:228` D1(a): the flag is "testable by grep and cannot misfire on a person"; `spec:128`: section 4 commands "get no `--unattended` mode"; `spec:51`.
- Concrete attack: **Sentinel Collision Attack.** The invariant at D1(a) (`spec:228`) fails when a person's free-text prompt contains the token. State trace: a person runs `/sc:troubleshoot "why does --unattended skip the prompt"`; before, interactive; after, a naive scan of the arguments turns unattended mode on and removes the person's gates, breaking SA-1. For `/sc:git --unattended` nothing says refuse, ignore or run.
- Why Medium: needs a guess about how the implementer scans arguments. Recommendation: add to the contract file that the switch counts only as a standalone token outside any quoted argument, and that section 4 commands refuse it. Priority: Medium. Quality impact: Clarity +0.5.

### F-06 (MAJOR graded Medium): stale report and "fresh directory" versus the coordinator-fixed directory
- Expert: Nygard, Whittaker (Sequence Attack).
- Texts: `spec:62` (WC-4: path known before dispatch); `spec:64` (WC-6: "writes each run into a fresh output directory so a re-run starts clean"); `spec:205` (AC-3.2: "starts fresh" in `<dir>` with an existing `.session-memory.md`); the 3.2 rows marked "fresh dir" (for example `spec:99`).
- Concrete attack: **Sequence Attack.** A first attempt wrote `status: succeeded`; a `--retry-of` worker is started with the same `--output <dir>`; it dies before writing; the worker (or the coordinator opening the file) reads the old contract and reports succeeded (`spec:63`). Separately, WC-6's fresh directory cannot be both created by the command and equal the directory the coordinator passed.
- Why Medium: it needs a retry that reuses the directory, which the text allows but does not require. Recommendation: say the coordinator passes a new directory per attempt, or the command deletes or overwrites the contract first thing. Priority: Medium. Quality impact: Consistency +0.5.

### F-07 (MAJOR graded Medium): outcome mapping covers "no report" but not an empty, invalid or foreign-vocabulary report
- Expert: Nygard, Whittaker (Divergence).
- Texts: `spec:63` (WC-5: failed "or no report exists"); `spec:62` (four-value `status`; existing contracts "keep their fields"); `spec:263` (decision: fixed four-value set).
- Concrete attack: **Divergence Attack.** A contract file exists with `status` missing, or with a command's own value (the workflow vocabulary is UNVERIFIED, `INV-B:272`). WC-5 gives no branch: neither failed nor succeeded is specified. Priority: Medium. Recommendation: one clause, "an unreadable or out-of-set `status` maps to failed". Quality impact: Completeness +0.5.

### F-08 (MAJOR graded Medium): WC-9 authorization flags are not defined for task and post-release
- Expert: Cockburn (stakeholder authority), Nygard.
- Texts: `spec:67` (outward actions turn on "only through the command's own explicit flag written in the brief"); `spec:121` (task: commit and push "refused unless authorized (WC-9)"); `spec:113` (post-release: "unless the brief authorizes them"); `spec:244-246` (D4).
- Gap: `INV-B:204` shows task's `commit`/`push` run as EXEMPT keywords with no flag; no flag exists to name. An implementer cannot write the P2 and P4 gate without inventing one. Priority: Medium (decided by D4, a user decision). Recommendation: name the flag per command in the rows, or say it is defined with the D4 answer. Quality impact: Completeness +0.5.

=== ARCHITECTURE ANALYSIS ===

### F-09 (MINOR graded Medium): WC-10 leaves a 4 to 5 minute band and states two thresholds
- Expert: Nygard, Crispin (boundary).
- Texts: `spec:68` (split only a call "longer than 5 minutes" into waits "of at most 4 minutes"); `spec:114` (pr-submit: each iteration "under 4 minutes"); `spec:266` (decision: "4 minutes leaves a margin under the 5-minute heartbeat cadence").
- Gap: a single call of 4 to 5 minutes is neither split nor margin-safe; the margin the decision claims is not in the rule. Recommendation: make the trigger "longer than 4 minutes". Priority: Low. Quality impact: Clarity +0.3.

### F-10 (MAJOR graded Medium): requirements with no owner phase or no acceptance check
- Expert: Wiegers (traceability), Gregory, Hohpe.
- Texts: `spec:59` (WC-1 owner "Launch setup, not commands"; "well inside" has no number, while its evidence says above about 45 s fails, `CAPS:49`); `spec:158-162` (no phase touches launch setup); `spec:61` (WC-3 `ask` path); `spec:70` (WC-12); `spec:104` (cli-eval wait splitting).
- Gap: `spec:166-210` has no check for WC-1, WC-3, WC-12 or the cli-eval half of WC-10; only AC-4.3 (`spec:210`) tests heartbeats. Priority: Medium. Recommendation: one row per uncovered WC, or mark it "not tested". Quality impact: Testability +1.

### F-11 (MAJOR graded Medium): coordinator side has no stall ceiling, and `ask` has no repeat cap
- Expert: Nygard, Hightower.
- Texts: `spec:44` (a command prompt stall is "silent", seen only through `agentWait` or a missing report); `spec:73` (section 2.3 lists briefing and post-completion steps only); `spec:181` (checks `worker-show` at least every 5 minutes, but states no stop rule); `spec:61` (WC-3 resumes the same message "and never creates a duplicate", no cap). `CAPS:111` and `CAPS:125-126` say silence never authorizes release or stop, so a coordinator needs the rule written down.
- Priority: Medium. Recommendation: add a one-line coordinator rule: "a non-null `agentWait` or no `worker_done` within N minutes is escalated to the person; never released on silence". Quality impact: Completeness +0.5.

### F-12 (MINOR graded Medium): AC-C5 additive check conflicts with editing existing Usage lines
- Expert: Crispin, Fowler.
- Texts: `spec:159` (P1: flag "accepted by every command"); `spec:176` (AC-C5: no `^-[^-]` line in the diff); `spec:149` (SA-4: additive).
- Gap: adding `[--unattended]` to an existing Usage line is a changed line, so AC-C5 fails unless the implementer adds a second Usage line instead (the pattern used elsewhere is a second line). The text allows both. Priority: Low. Quality impact: Clarity +0.3.

### F-13 (MINOR graded Medium): AC-C1 pattern is narrower than SA-2 and does not exclude the contract file
- Expert: Crispin, Newman.
- Texts: `spec:172` (AC-C1 pattern: `orca(-ide)? (orchestration|worktree|terminal|agent)`, over `src/superclaude/core` too); `spec:147` (SA-2 allows an Orca mention "inside the contract file"; the contract file lives in `core`).
- Gap: the pattern misses `orca-ide skills get` and `orca status`, and would trip on a contract file that spells `orca orchestration ask`. Priority: Low. Quality impact: Testability +0.3.

### F-14 (MINOR graded Medium): phase-decision statements disagree
- Expert: Cockburn, Wiegers.
- Texts: `spec:154` ("Phases 1-3 need no user decision"); `spec:225` ("Phases 0-3 can proceed on the recommendations"); `spec:244` (D4 affects the auggie-review and task rows, which are P2, `spec:100`, `spec:121`); `spec:51` (D1 underlies every phase).
- Gap: whether D1 and D4 must be answered before P1 and P2 is stated two ways. Priority: Low. Quality impact: Consistency +0.3.

## Minor notes (never fail the review)

- N-01: E3 (`spec:23`) offers `invocation_method: "skill-direct"` as proof it "has worked before" while `spec:43` says the PR #329 run "proves the nested route, not the direct route this spec requires". The two are reconciled by section 1.4; E3's wording is stronger than the evidence.
- N-02: The tasklist row (`spec:122`) says its reflect fan-out runs "one layer below the worker"; `INV-B:210` describes reflect running inside N subagents that spawn their own agents, which is two layers. Conclusion (within the three-layer limit, `INV-A:14`) is unchanged.
- N-03: `spec:22` E2 says the worker "answered"; the quoted `EVIDENCE.md:45` line (via `CAPS:49`) shows `state: ready, stage: input_accepted` only. UNVERIFIED.
- N-04: `spec:11` and `spec:76` claim `cmd/` holds exactly 43 commands; the inventories list their own scope (`INV-A:3`, `INV-B:3`) but a directory listing is not in the sandbox. UNVERIFIED.
- N-05: The contract has no `version` or schema field (`spec:62`); a later field change is silent for the coordinator (Newman). A one-line addition if a later round wants it.
- N-06: 7.2 step 5 (`spec:184`) searches the transcript for the string `AskUserQuestion`; the `## Unattended mode` sections the spec adds mention that word, so the search should look for a tool call, which the pass condition already says ("no `AskUserQuestion` call").
- N-07: Observation from the supplied `command.md`, not from the inventories, and not graded: it already shows `--output <file>`, `--report-dir` and an `## Unattended mode` section for spec-panel (`command.md:22-24`, `command.md:455-465`), where the spec's spec-panel row says to "add `--output`" (`spec:120`) and `INV-B:182` says no `--output` flag exists. The spec may predate that edit.
- N-08: The `document` row (`spec:107`) says "require an explicit output"; if read as a standalone requirement it would conflict with SA-1 (`spec:146`). The column heading is the WC-4 unattended report, which gives the intended reading.

## Follow-up candidates (Medium and minor, no revision, no effect on the verdict)

F-04, F-05, F-06, F-07, F-08, F-09, F-10, F-11, F-12, F-13, F-14, and notes N-01 to N-08.

Issue question: the command asks the user once per loop whether to open an issue for these. This worker's final reply is restricted to the output path, so the question is left to the coordinator or user; no issue was created.

## Quality scores (0-10)

| Dimension | Score | Basis |
|---|---|---|
| Clarity | 8 | Terms, tables and per-command rows are precise; F-04, F-09 are the loose spots |
| Completeness | 7 | Every command classified with evidence; coordinator stall policy, WC authorization flags and edge outputs missing (F-04, F-08, F-11) |
| Testability | 6 | Strong 7.2 live check; P0 check unpassable (F-01), several WC unchecked (F-10) |
| Consistency | 6 | Counts and phase mapping conserve; three path and scope contradictions (F-01, F-02, F-03) |

## Reviser brief

Blocking finding ids: F-01, F-02, F-03.

Contract for the reviser (restating the review loop's reviser rule): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size of the candidate before and after, with the bytes added and deleted per finding id. Leave Medium and minor findings alone. Return the candidate once and do not award yourself a PASS.

verdict: FAIL
