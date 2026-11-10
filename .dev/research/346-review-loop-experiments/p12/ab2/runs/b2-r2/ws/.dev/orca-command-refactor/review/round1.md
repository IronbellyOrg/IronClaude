review: 1 of 3
> verification (coordinator, VERIFY step VF1; verifier reply .dev/orca-command-refactor/review/verify-1.md): confirmed blocking ids: B-1, B-2, B-3. Rejected, kept as noted, unactioned and not prior blocking findings for the next re-review: none. The Reviser brief below is narrowed to the confirmed ids.

# Spec-panel report, round 1: Orca worker contract spec

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (first review, no `--re-review`, no `--baseline`)
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (taken with `sha256sum` in the sandbox)
- Baseline: not given (first review of the full document)
- Reviewer model actually used: claude-sonnet-5-5
- Prompt followed: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full; `~` resolves to the sandbox `home/`)
- Panel (command order): Wiegers, Adzic, Cockburn (requirements lead Wiegers); Fowler, Nygard, Newman, Hohpe (architecture lead Fowler); Whittaker (active in every review, after Fowler and Nygard); Crispin joins only for the Guard Condition Boundary Table completeness check. Gregory and Hightower were not on the focus panels and are not used.
- Citation shorthand: `SPEC:N` = line N of the candidate; `README:N`; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md` (all under `.dev/orca-command-refactor/`). Every `path:line` into the repository outside those five files (`cmd/`, `sk/`, `CLAUDE.md`, `install_core.py`, `EVIDENCE.md`, `orca-ide` output) is UNVERIFIED here: the sandbox holds no such file. Where I rely on a fact from one of them, I cite the inventory line that quotes it.
- Brief clauses overridden: none. The brief asked for no widening and no regrading of a minor finding.

## Verification block

None. The VERIFY step belongs to the coordinator and has not run. No finding below was rejected by a verifier.

## Coverage

Read in full: the candidate (285 lines), README, `inventory/orca-capabilities.md` (188), `commands-a.md` (120), `commands-b.md` (323). Checked by arithmetic: 43 commands = 10 ready + 27 needing change + 6 coordinator-only (SPEC:76, SPEC:79-137), matching INV-A (5+13+3=21) and INV-B (5+14+3=22); the phase column of section 3 partitions as P1=9 (+4 fixes to ready commands), P2=11 (+4 ready), P3=4, P4=3 and agrees with the phase table (SPEC:159-162). Not checked: every `cmd/`, `sk/` and repo-file citation (UNVERIFIED, see above), the spec's own claim of 11 re-read locations and about 340 validated citations (SPEC:11, SPEC:285; UNVERIFIED), and every command or Orca behaviour not quoted in an inventory. The three inventories are the only evidence I could check, as the task brief states.

## Mandatory output artifacts

### Guard Condition Boundary Table (Nygard builds, Crispin checks completeness, Whittaker attacks)

Trigger: the spec contains threshold and boolean guards, so the table is produced. Status is `GAP` when the spec is silent or contradicts itself; each GAP is graded under FR-8/FR-9 and listed in the findings (blocking only where a finding below says so).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|--------------------|--------|
| G1 outcome map (status to `--outcome`) | SPEC:63 | Zero/Empty | contract file exists, 0 bytes or unparseable | not "no report exists" | unspecified (only a missing report maps to `failed`; `test -s` appears only in an acceptance step, SPEC:183) | GAP (M-6) |
| G1 | SPEC:63 | Typical | `status: succeeded` | true | `--outcome succeeded` | OK |
| G1 | SPEC:63 | Sentinel Value Match | `status` outside the four-value set (an existing contract's own value) | neither branch | unspecified; SPEC:62 says existing contracts "keep their fields" | GAP (M-6) |
| G1 | SPEC:63 | Legitimate Edge Case | `partial`; audit verdict FAIL; `blocked` | true | `partial` and FAIL-verdict map to `succeeded`; `blocked` maps to `failed` | OK |
| G2 contract location (`<output-dir>/return-contract.yaml`) | SPEC:62 | Zero/Empty | `--unattended` with no output directory passed | no directory | unspecified for analyze, build, design and others that only "add `--output`" (SPEC:99-111); explicit only for post-release and document (SPEC:107, SPEC:113) | GAP (M-2) |
| G2 | SPEC:62 | Typical | `--output <dir>` on brainstorm, reflect | true | `<dir>/return-contract.yaml` | OK |
| G2 | SPEC:62, SPEC:83 | Legitimate Edge Case | adversarial: contract fixed at `<output>/adversarial/return-contract.yaml` | WC-4 path differs | contradicts WC-4 | GAP (B-1) |
| G2 | SPEC:62, SPEC:87, SPEC:90 | Legitimate Edge Case | `--output <file>` (tdd, init-lite) | no directory passed | unspecified | GAP (B-1) |
| G2 | SPEC:62, SPEC:92 | Legitimate Edge Case | workflow: package id generated by the command; pre-creation STOP has no package directory | no directory passed | unspecified (SPEC:92 only says "write the contract for pre-creation STOPs too") | GAP (B-1) |
| G3 wait split (`> 5 min` triggers waits `<= 4 min`) | SPEC:68 | Zero/Empty | no blocking call (0 s) | false | no split, nothing to heartbeat | OK |
| G3 | SPEC:68 | Typical | 3 min call | false | no split | OK |
| G3 | SPEC:68, SPEC:210 | Legitimate Edge Case | 270 s call | false (not over 5 min) | WC-10 requires no split; AC-4.3 requires no call over 240 s | GAP (M-8) |
| G3 | SPEC:68 | Maximum/Overflow | 3600 s eval (cli-eval) | true | split into waits of at most 4 min (SPEC:104) | OK |
| G3 | SPEC:68 | Sentinel Value Match | exactly 300 s, equal to the 5-minute heartbeat cadence | false ("longer than") | no split; at the cadence edge | GAP (M-8, minor part) |
| G4 `--unattended` switch | SPEC:51, SPEC:146 | Zero/Empty | flag absent | false | today's behaviour (SA-1) | OK |
| G4 | SPEC:159 | One/Minimal | flag present, command has no gate | true | accepted, no-op | OK |
| G4 | SPEC:83-84, SPEC:89, SPEC:128 | Legitimate Edge Case | flag present together with `--interactive`; or on a section-4 command | true | brief rules say "never `--interactive`"; section 4 says no mode; no refusal behaviour stated | GAP (M-2) |
| G4 | SPEC:51 | Sentinel Value Match | the string `--unattended` inside a quoted prompt or topic (for example a tdd topic) | undetermined | unspecified | GAP (M-2) |
| G4 | SPEC:159, SPEC:160 | Legitimate Edge Case | flag present on a gated command before its gate phase (auggie-review, P2) | true | P1 text accepts the flag; the gate resolves only in P2 | GAP (M-4) |
| G5 confidence below 0.70 (`/sc:task`) | SPEC:121 | Zero/Empty | confidence 0.0 | true | blocked | OK |
| G5 | SPEC:121 | Typical | 0.50 | true | blocked | OK |
| G5 | SPEC:121 | Legitimate Edge Case | exactly 0.70 | false ("below 0.70") | proceeds | OK |
| G6 launch fallback "well inside" the 60 s readiness limit (WC-1) | SPEC:59 | Typical | 30 s fallback | true | passes (CAPS:49 quotes EVIDENCE: 34 s start succeeds) | OK |
| G6 | SPEC:59 | Legitimate Edge Case | 45 s fallback | undetermined | "well inside" has no number; CAPS:49 quotes EVIDENCE that about 45 s fails again | GAP (M-7) |
| G7 nesting depth 1 (WC-8) | SPEC:66, SPEC:33 | Typical | depth 1, command calls `worker-start` | true | refused; command must not call it | OK |
| G7 | SPEC:66, SPEC:252 | Maximum/Overflow | depth raised (D5 b) | false | WC-8 still forbids the call | OK |
| G8 `ask` timeout (WC-3) | SPEC:61 | Typical | one ask, answered | true | re-invoke with the answer as a flag | OK |
| G8 | SPEC:61 | Maximum/Overflow | ask times out repeatedly, coordinator never replies | true each time | resume same message ID; no cap, no give-up rule | GAP (M-3) |
| G8 | SPEC:61 | Zero/Empty | coordinator replies with an empty body | undetermined | unspecified | GAP (M-3) |
| G9 `consumer_fenced` (WC-12) | SPEC:70 | Zero/Empty | `check` returns nothing | false | continue | OK |
| G9 | SPEC:70 | Legitimate Edge Case | `consumer_fenced` | true | stop, no `worker_done` | OK |
| G10 `--monitor` ordinal (pr-submit) | SPEC:114 | Legitimate Edge Case | `--monitor 1` | true | refused under `--unattended` | OK |
| G10 | SPEC:114 | Legitimate Edge Case | `--monitor 0` or `2` | false | unspecified; INV-B:89 names a y/n gate only at level 1 (levels 0 and 2 UNVERIFIED) | GAP (UNVERIFIED, minor, N-7) |

Omitted input classes (one line each): G1 One/Minimal and Maximum have no cardinality; G2 One/Minimal and Maximum, and G5 One/Minimal, Maximum, Sentinel: the guard is a single threshold on one value; G3 One/Minimal is a duration, not a count; G6 Zero/One/Maximum/Sentinel: the guard is a duration compared to a fixed limit; G7 Zero/One/Sentinel: depth is a setting, and a malformed setting falls back to 1 (CAPS:100); G8 One/Minimal equals Typical; G9 One/Minimal, Maximum, Sentinel: a single event type; G10 Zero/One/Typical/Maximum/Sentinel: a four-value ordinal where only the edge levels are in question.

FR-10 check: every guard I found is enumerated and every input class has a row or a stated reason, so synthesis was not blocked. FR-8/FR-9: each GAP is graded in the findings below; none is blocking on its own except where B-1 names it.

### Pipeline Dimensional Analysis (Fowler leads, Whittaker attacks)

Trigger (FR-17): the spec describes a multi-stage count flow whose counts can differ (classification of commands, then phase assignment, then acceptance coverage). It is not CRUD-only, so the analysis runs.

```text
[Inventory: 43 commands, SPEC:76 / INV-A:3 21 + INV-B:3 22]
   --> [Classify]
        |-- ready today: 10 (SPEC:79-92) -------------+
        |-- needs change: 27 (SPEC:97-125) -----------+--> 37 dispatchable
        '-- coordinator-only: 6 (SPEC:131-137)        |
   --> [Phase assign, SPEC:156-162]                   |
        P1 scope text: "flag accepted by every command in 3.1 and 3.2" = 37 (SPEC:159)
        P1 named commands: 9 (3.2) + 4 fixes (3.1)    = 13   <-- N != M
        P2 = 15 (11 + 4), P3 = 4, P4 = 3
   --> [Acceptance coverage]
        AC-1.1 asserts a contract section on "every command in 3.1-3.2" = 37 (SPEC:195)
        7.2 step 4 requires a contract file; `load` (3.2) specifies none (SPEC:112) <-- N != M
```

Count conservation holds at classification (43 = 10 + 27 + 6) and at phase assignment (13 + 15 + 4 + 3 = 35 phase slots; the 2 ready commands brainstorm and init-lite have no phase, SPEC:84, SPEC:87, 35 + 2 = 37). The consistency check finds two divergence points, both traced to a consumer that assumes the larger count: AC-1.1 and AC-1.2 (consumers) assume 37 commands with a contract while `load` has none (traced to B-2), and P1's scope sentence assumes 37 flag-accepting commands while its command list names 13 (traced to M-4). FR-19 labels a dimensional mismatch CRITICAL; Review Loop bullet 2 requires grading by consequence, so the first is graded blocking (it names a failing acceptance check) and the second Medium (it needs a guess about which of two phase readings an implementer picks).

### Advisory

`--focus correctness` would apply (numeric thresholds 60 s, 5/4 min, 0.70; a multi-stage count flow). Advisory only; not activated, so no State Variable Registry is produced.

## === REQUIREMENTS ANALYSIS ===

Blocking findings first. Each carries the FIRST-REVIEW grading sentence.

### B-1 (CRITICAL, blocking). WC-4's single contract location contradicts the rows that fix a different location
- Expert: Wiegers (consistency of requirements), Whittaker (Divergence Attack)
- Texts:
  - SPEC:62 (WC-4): "`<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)".
  - SPEC:83 (section 3.1, adversarial, brief passes `--output <dir>`): "Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)". INV-A:35 shows `<output>` is the `--output` value ("Merged output + 6 artifacts under `<output>/adversarial/`").
  - SPEC:182 (7.2 step 3): "its report path is the WC-4 contract path"; SPEC:183 (step 4): `test -s <contract>`; SPEC:196 (AC-1.2): "all steps pass".
  - Same defect in three more rows: SPEC:90 and SPEC:87 pass `--output <file>` (tdd, init-lite) so no directory is passed, yet AC-2.2 (SPEC:200) uses `/sc:tdd "auth" --unattended --output <file>` and requires a contract; SPEC:92 and INV-B:272 put workflow's contract in `.dev/tasks/to-do/<id>/` where `<id>` is generated, and a pre-creation STOP (the case SPEC:92 adds) has no package directory.
- Grading sentence: An implementer who follows the adversarial row as written writes the contract at `<output>/adversarial/return-contract.yaml`; the coordinator, following WC-4 and section 2.3 (SPEC:73), opens `<output>/return-contract.yaml`, finds no report, and by WC-5 (SPEC:63, "or no report exists") sends `--outcome failed` for a run that succeeded; and acceptance step 4 cannot pass for adversarial, tdd or init-lite as written.
- Recommendation: state contract location per command in one place (a column in section 3 or a one-line rule that the file lives beside the command's own fixed location), and say which `--output` form (directory or file) each command in 3.1 takes, so that "known before dispatch" (SPEC:62) is true for every row. Rationale: WC-4 is the coordinator's only read path, and its rule and four rows disagree.
- Priority: High. Quality impact: Consistency +2, Testability +1.

### B-2 (CRITICAL, blocking). `load` is required to have no report file and also a contract section
- Expert: Wiegers (traceability), Adzic (acceptance examples)
- Texts:
  - SPEC:112 (section 3.2, load): Report column "none (see note)", note "use it as a step inside another worker's brief, not as its own Task".
  - SPEC:265 (Decisions): "a report file would be an unrequested addition. Only its usage-line defect is fixed."
  - SPEC:159 (P1): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2" and, in the same row, "load (usage line only)".
  - SPEC:195 (AC-1.1): the test asserts "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`"; SPEC:196 (AC-1.2): a 7.2 live check "on each P1 command", whose step 4 needs a contract file (SPEC:183). `load` is a P1 command (SPEC:159).
- Grading sentence: An implementer who follows the load row and the Decision adds only the usage line, no `## Unattended mode` section and no contract, and X is wrong because AC-1.1 (every command in 3.1-3.2) and AC-1.2 step 4 (`test -s <contract>`) then fail for `load`; an implementer who satisfies AC-1.1 instead adds a section and a contract to `load`, which the row and the Decision say not to do.
- Recommendation: narrow AC-1.1 and AC-1.2 to the commands that write a contract (exclude `load`, and every command whose phase is later than P1 for the P1 run), or move `load` out of the section 3.2 count; do not add a contract to `load`. Rationale: deleting a clause is cheaper than adding a feature the Decisions row rejects.
- Priority: High. Quality impact: Consistency +1, Testability +1.

### B-3 (MAJOR, blocking). The P0 gate cannot pass as written, and a failure "reopens section 1"
- Expert: Wiegers (testability), Nygard (failure of the gate itself)
- Texts:
  - SPEC:158 (P0): "(no command edits)", smoke runs of `/sc:troubleshoot`, `/sc:workflow` and `/sc:adversarial`.
  - SPEC:194 (AC-0.4): "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1 ... a failure here reopens section 1".
  - SPEC:182 (7.2 step 3), pass condition: "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path".
- Grading sentence: An implementer or coordinator who follows AC-0.4 as written runs steps 1-3 for commands that, by SPEC:158, still write no WC-4 contract (troubleshoot's report is `REPORT.md`, SPEC:91), so step 3's pass condition cannot be met, the relaxation names step 4 only, and the stated consequence of failing is to reopen the core decision (section 1) on a false negative.
- Recommendation: extend the AC-0.4 relaxation to step 3 ("outcome matches the command's own report; report path is the command's existing report file"). One clause; no new mechanism. Rationale: the relaxation already exists for step 4 and must cover the sibling step that reads the same file.
- Priority: High. Quality impact: Testability +2.

## Follow-up candidates (Medium and minor; none triggers a revision)

These are Medium (a warning) or minor (a note). The report does not ask the user about opening an issue: this run has no user channel, so the list is only recorded and no issue is created.

### Medium

- **M-1 (Medium, was MAJOR label). "Fresh dir" re-runs have no defined mechanism; a stale contract can be read as success.** SPEC:64 (WC-6) says a command without a resume flag "writes each run into a fresh output directory"; about 20 rows in section 3.2 use "fresh dir". SPEC:62 (WC-4) fixes the contract path to the directory the coordinator passed, and section 2.3 (SPEC:73) says the brief fixes it before dispatch. A `--retry-of` worker reuses the Task's brief, so either the command invents a subdirectory (the contract is not at the WC-4 path) or the coordinator must pass a new directory per attempt (section 2.3 does not say so). If neither happens, a first attempt's `status: succeeded` file survives a second attempt that crashes before writing, which WC-4's "written on every outcome" (SPEC:62) does not cover (a crash is not a stop). Needs a guess about which reading an implementer picks. Expert: Nygard, Whittaker (Sequence). Recommendation: add to section 2.3 that the coordinator passes a new output directory per attempt. Priority: Medium. Quality impact: Consistency +1.
- **M-2 (Medium). `--unattended` edge inputs are unspecified.** (a) No output directory passed (G2): analyze, build, design, explain, index, test and others only "add `--output`" (SPEC:99-111); only post-release and document say "require" it (SPEC:107, SPEC:113). (b) `--unattended` together with `--interactive` is a brief rule ("never `--interactive`", SPEC:83-84, SPEC:89), not a command-side refusal like cleanup (SPEC:103). (c) `--unattended` passed to a section-4 command (SPEC:128 says they "get no `--unattended` mode") has no stated outcome; `/sc:git` mutates the repo. (d) The token inside a quoted prompt or topic is not excluded (SPEC:51). Expert: Whittaker (Zero/Empty, Divergence, Sentinel Collision). Priority: Medium.
- **M-3 (Medium). WC-3 has no bound on repeated `ask` resumes and no empty-reply rule.** SPEC:61 says the session resumes the same message ID on timeout, "never creates a duplicate", and sends no heartbeat while blocked. A coordinator that never replies leaves the worker blocked indefinitely; there is no "after N timeouts write `status: blocked` and stop". Orca's 60-second limit does not apply after start (CAPS:52), so nothing else ends it (CAPS:188, whether Orca bounds a Dispatch's run time, is UNVERIFIED). Expert: Whittaker (Accumulation), Hohpe (delivery guarantees). Priority: Medium.
- **M-4 (Medium). P1 text and AC-1.1 conflict with the per-row phases; a window exists where `--unattended` is accepted but gates and outward defaults are unconverted.** SPEC:159 says P1 makes every 3.1 and 3.2 command accept `--unattended` ("a no-op where a command has no gate"), while section 3 assigns the gate resolution of auggie-review, task, cleanup and others to P2 and pr-submit, post-release and implement to P4 (SPEC:100, SPEC:121, SPEC:160, SPEC:162). WC-9 (SPEC:67) says outward defaults are off "under `--unattended`", yet auggie-review posts to GitHub by default (SPEC:100, INV-A:38) until P2. Section 6 says each phase "is independently useful" (SPEC:154) but does not forbid dispatching a command before its phase. Whether the P1 flag on a gated command is a no-op or a partial section is a reading the text allows both ways, so this is Medium; the safest fix is one sentence in section 6 that a command is not dispatched with `--unattended` before its own phase. Expert: Fowler, Whittaker (Sequence). Priority: Medium. See the Pipeline Dimensional Analysis above.
- **M-6 (Medium). Status vocabulary and empty or unparseable contracts.** SPEC:62 requires `status` in four values and says commands with an existing contract "keep their fields and add the missing ones"; SPEC:261 chooses `return-contract.yaml` because workflow, brainstorm, reflect and adversarial already write it. No inventory line gives the existing `status` values (INV-B:272 lists `status`, `plan_path`, `reflect_report_path` only), so keeping a field and requiring the four values may conflict (UNVERIFIED). Step 4's YAML assertion (SPEC:183) rejects any other value. WC-5 (SPEC:63) does not cover an empty or unparseable file. Expert: Newman (contract evolution), Wiegers. Priority: Medium.
- **M-7 (Medium). WC-1 is not testable as written.** SPEC:59 says a startup prompt must fall back "well inside the readiness limit (default 60 s)". The evidence quoted at CAPS:49 gives two points: a 30 s fallback passes (34 s start) and above about 45 s it fails again. The requirement states no number, and the only check is `state: ready` in 7.2 step 1 (SPEC:180). Owner is "Launch setup, not commands", so no command change is in scope. Expert: Wiegers. Priority: Medium.
- **M-8 (Medium). WC-10 and AC-4.3 disagree in the 240-300 s band; the 5-minute heartbeat rests on one worker's preamble.** SPEC:68 triggers splitting only for a call "longer than 5 minutes" (waits then at most 4 minutes); SPEC:210 fails any "single tool call exceeds 240 s"; SPEC:114 says "stays under 4 minutes". A 270 s pr-submit iteration passes WC-10 and fails AC-4.3. The cadence is cited to "the dispatch preamble, not a guide" (SPEC:68, CAPS:130), which CAPS:130 describes as this inventory worker's own preamble, with use of heartbeat age by Orca UNVERIFIED. Expert: Nygard, Crispin. Priority: Medium. Quality impact: Consistency +1.
- **M-9 (Medium). The tasklist nesting claim is stated as fact; the inventories mark it UNVERIFIED.** SPEC:122 says tasklist's reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`". INV-B:210 says Stage 10.5 dispatches N subagents that each run `/sc:reflect`, which itself spawns agents ("subagent to agent nesting ... UNVERIFIED whether nested spawning works"); INV-A:14 says an agent at the depth limit "silently loses its Agent tool". The reflect-in-subagent chain is at least two layers below the worker, and the item is absent from the spec's UNVERIFIED list (SPEC:271-285) though INV-B:314 and INV-B:322 carry it. Expert: Fowler, Nygard. Priority: Medium.
- **M-10 (Medium). AC-C1 can fail on P0's own deliverables.** SPEC:172 (AC-C1) requires `grep ... src/superclaude/core` to print nothing for `orca (orchestration|worktree|terminal|agent)`. SPEC:147 (SA-2) allows an Orca mention "as an example of a caller's question channel inside the contract file", which is `src/superclaude/core/WORKER-CONTRACT.md` (SPEC:52), and SPEC:158 adds "an Orca section" to `HOW-WE-WORK.md`, also under `core`. An example written as `orca orchestration ask` would print and fail the phase. Needs a guess about the wording used. Expert: Fowler (boundaries), Wiegers. Priority: Medium.
- **M-11 (Medium). No acceptance check for WC-3, WC-6 and WC-12.** Traceability from the requirement table (SPEC:61, SPEC:64, SPEC:70) to section 7: WC-1 (7.2 step 1), WC-2 (steps 2, 5), WC-4/5 (steps 3, 4), WC-7 (step 5), WC-8 (AC-C1), WC-9 (AC-2.4, AC-4.2), WC-10 (AC-4.3), WC-11 (AC-3.4 for `save` only) each have one; the ask path (WC-3), retry and resume (WC-6) and `consumer_fenced` (WC-12) have none. Expert: Wiegers (traceability), Crispin. Priority: Medium.

### Minor notes

- **N-1.** SPEC:79 says the ten ready commands "run as workers now", while section 1.4 (SPEC:43) and UNVERIFIED item 1 (SPEC:272) say no direct-route run exists. Also E3 (SPEC:23) cites `invocation_method: "skill-direct"` as evidence while SPEC:43 says the PR #329 brief used an Agent-tool subagent; INV-A:13 and INV-A:35 treat the same file as a direct call. The two are not reconciled in the text. No wrong outcome, since Phase 0 tests it.
- **N-2.** Section 3.2 counts `pr-submit` among the 27 commands needing a change (SPEC:76, SPEC:114) although D3(a), the recommendation, leaves it unchanged (SPEC:240) and SPEC:139 calls it a worker candidate only under D3(a)'s alternative.
- **N-3.** WC-4 has no schema or version field, though workflow's own contract is versioned (INV-B:272, "contract 1.1"). Expert: Newman.
- **N-4.** 7.2 step 5 (SPEC:184) greps the transcript for `AskUserQuestion`; the command's own "never call `AskUserQuestion`" text can appear in a loaded transcript and give a false failure.
- **N-5.** AC-C5 (SPEC:176) uses `grep -E '^-[^-]'`, which skips a removed line that itself starts with `--`; additive-only is not fully checked.
- **N-6.** WC-9 (SPEC:67) lists "a paid external run" without a definition; research and review-translation call Tavily (INV-B:134, INV-B:144) and are not covered. Section 2.3 gives no worked example brief (Adzic).
- **N-7.** `--monitor 0` and `2` behaviour for pr-submit under `--unattended` is not stated (SPEC:114; INV-B:89); only level 1 has a stated gate (UNVERIFIED for the others).

## === ARCHITECTURE ANALYSIS ===

- **Fowler (lead, boundaries).** The decision is sound: Orca above, commands as units, one shared contract file plus a short per-command section (SPEC:16, SPEC:52) keeps the interface segregated, and section 1.3 gives five reasons against commands calling Orca with citations I could check against the inventory (CAPS:97-103, CAPS:145-150, INV-A:90). The boundary defect is the contract location rule (B-1) and the P0 gate (B-3). Pipeline findings: see the Quantity Flow Diagram.
- **Newman (evolution).** Contract has no version (N-3); the status vocabulary can collide with existing contracts (M-6).
- **Hohpe (messaging).** Exactly-once `worker_done`, pull-only follow-ups and the `ask`/`reply` path are correctly taken from the capabilities inventory (CAPS:58-67, CAPS:73-77). Open points: unbounded `ask` resumes (M-3); a contract written but no `worker_done` sent (a crash after the report) is covered only by UNVERIFIED item 11 (SPEC:282), so the coordinator has no stated path.
- **Nygard (failure modes).** Stale contract on retry (M-1); wait-size band (M-8); ask loop (M-3). The spec handles liveness and release correctly by reference to Orca's own rules (SPEC:73, CAPS:107-113).
- **Cockburn.** Primary actor (the coordinator) and goal are explicit (SPEC:16, SPEC:73); the person at the keyboard keeps today's behaviour (section 5).
- **Adzic.** AC-2.x give concrete live examples; a full example brief is missing (N-6).

## === ADVERSARIAL ANALYSIS (Whittaker) ===

- I can break this specification by **Divergence Attack**. The invariant at **SPEC:62 (WC-4) with SPEC:83** fails when **a command's fixed contract path differs from the passed directory**. Concrete attack: `/sc:adversarial --compare a.md b.md --output out/ --unattended`; before: no contract; after the P1 fix: file at `out/adversarial/return-contract.yaml`; the coordinator reads `out/return-contract.yaml` (absent) and WC-5 maps "no report" to `failed`. Maps to B-1.
- I can break this specification by **Zero/Empty Attack**. The invariant at **SPEC:62** fails when **no output directory is passed or the passed value is a file**. Concrete attack: `/sc:tdd "auth component" --unattended --output docs/TDD_AUTH.md`: `docs/TDD_AUTH.md/return-contract.yaml` cannot exist; the parent directory option puts two workers' contracts in `docs/`. Maps to B-1, M-2.
- I can break this specification by **Sequence Attack**. The invariant at **SPEC:159-160** fails when **a command is dispatched with `--unattended` after P1 and before P2**. Concrete attack: `/sc:auggie-review 123 --unattended` after P1: flag accepted, posting default still on, a review is posted to the PR. Maps to M-4.
- I can break this specification by **Sentinel Collision Attack**. The invariant at **SPEC:62 and SPEC:261** fails when **a legitimate existing `status` value or filename collides with the new fixed vocabulary or the shared name `return-contract.yaml`**. Concrete attack: a nested run (workflow calling reflect, brainstorm calling adversarial) forwards one `--output` directory; two commands write `return-contract.yaml` with different schemas, and the later write decides the coordinator's status. The spec states a `--unattended` pass-through only for tasklist to reflect (SPEC:122). Maps to M-5 below and M-6.
- I can break this specification by **Accumulation Attack**. The invariant at **SPEC:61** fails when **ask timeouts accumulate without bound**. Concrete attack: three `ask` timeouts in a row with no coordinator reply; the worker stays in `ask`, sends no heartbeat (SPEC:61) and never writes `status: blocked`. Maps to M-3.

- **M-5 (Medium, nested invocation propagation).** The rule that a parent passes `--unattended` to a nested command appears once (tasklist to reflect, SPEC:122). The same defect class exists where a nested command has its own gate or outward default: pr-submit's optional auggie-review fallback posts by default (INV-B:91, INV-A:38), cli-eval create calls spec-panel and adversarial (INV-A:44), task calls troubleshoot (INV-B:201). The spec states no general rule and no shared `--output` rule for nested contracts. Expert: Whittaker, Fowler. Priority: Medium.

## Quality metrics (0-10)

Clarity 8, Completeness 7, Testability 6, Consistency 6. Overall 6.75.

## Standard-format summary

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review: 1 of 3
  expert_panel: [wiegers, adzic, cockburn, fowler, nygard, newman, hohpe, whittaker]
  focus_areas: [requirements, architecture]
quality_assessment: {overall_score: 6.75, clarity: 8, completeness: 7, testability: 6, consistency: 6}
critical_issues:
  - {id: B-1, severity: CRITICAL, blocking: true, expert: wiegers/whittaker}
  - {id: B-2, severity: CRITICAL, blocking: true, expert: wiegers/adzic}
  - {id: B-3, severity: MAJOR, blocking: true, expert: wiegers/nygard}
follow_up_candidates:
  medium: [M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, M-10, M-11]
  minor: [N-1, N-2, N-3, N-4, N-5, N-6, N-7]
expert_consensus:
  - Decision (Orca coordinates, commands stay units) is supported by the checkable evidence.
  - Counts conserve (43 = 10 + 27 + 6); three acceptance/location texts contradict the rows they test.
improvement_roadmap:
  immediate: [B-1, B-2, B-3]
  short_term: [M-1, M-2, M-3, M-4, M-8, M-10]
  long_term: [M-5, M-6, M-7, M-9, M-11, minor notes]
adversarial_analysis: [B-1, M-1, M-3, M-4, M-5, M-6]
```

## Reviser brief

Blocking finding ids: B-1, B-2, B-3. Nothing else is to be touched.

Contract for the reviser (restated from the command, since the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size of the candidate before and after, and the bytes added and deleted per finding id; leave Medium and minor findings alone; return the candidate once and do not award yourself a PASS.

verdict: FAIL
