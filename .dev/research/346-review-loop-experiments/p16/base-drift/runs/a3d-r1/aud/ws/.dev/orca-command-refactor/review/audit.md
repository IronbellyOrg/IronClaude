review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  candidate_sha256: 0d7786a334196b491d4a4779d2dbbc71fedd95552ea14ed522742fd98a72bf68
  baseline: none given (neither --re-review nor --baseline): this is a first review of the whole document, labelled whole-document audit
  reviewer_model: claude-sonnet-5-5
  mode: critique
  focus_areas: [requirements, architecture]
  expert_panel: [Wiegers (lead), Adzic, Cockburn, Fowler (lead), Newman, Hohpe, Nygard, Whittaker]
  review_loop_prompt: FIRST-REVIEW prompt, ~/.claude/rules/prompts/document_review_loop_prompts.md:27-32 (read in full)
  brief_clauses_overridden: none
quality_assessment:   # 0-10
  clarity: 7
  completeness: 6
  testability: 5
  consistency: 6
```

Citation keys: `SPEC:N` = line N of the candidate. `INV-A`, `INV-B`, `CAPS` = line N of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = line N of `.dev/orca-command-refactor/README.md`. `CMD:N` = line N of the /sc:spec-panel definition read for this run.

## Coverage

- Read in full: the candidate (285 lines), README, all three inventories, the command definition, and the loop prompts file.
- Citation spot-check: about 60 `INV-A`/`INV-B`/`CAPS`/`README` line citations in the candidate were opened and matched what the candidate says they hold (for example `INV-A:35-55` rows, `INV-B:289-299`, `CAPS:97-101`, `README:31,35`). The 10 / 27 / 6 split in `SPEC:76-78` was recounted against section 3.1, 3.2 and 4 and against both inventory summaries (`INV-A:73`, `INV-B:278`): 5+5 ready, 13+14 needs-change, 3+3 coordinator-only, 43 total. The phase assignment also conserves (see the flow diagram).
- UNVERIFIED (not checkable inside this workspace): every `CLAUDE.md:N`, `src/superclaude/...:N`, `.dev/evals/.../EVIDENCE.md:N`, `.dev/codegraph-migration/...` and `HOW-WE-WORK.md:N` citation. Those files are not in the workspace, so the candidate's own claim that it re-read them (`SPEC:11`, `SPEC:285`) is taken as unverified. Where a claim below rests on one of them, it is stated through an inventory line instead.
- Not convened: Crispin, Gregory, Hightower as reviewers (focus `testing` and `compliance` not requested). Crispin's completeness role for the Guard Condition Boundary Table was applied, and acceptance-check gaps were noted by Wiegers and Adzic.
- Not produced: State Variable Registry (only for `--focus correctness`, not active); `--iterations`, `--improve` and `--re-review` not used, so no revised specification is written (`CMD:261`).
- The candidate was not edited.

## Grading summary

| Id | Severity label | Graded | Where |
|---|---|---|---|
| F-01 | CRITICAL | blocking | `SPEC:63,158,194,182`; `SPEC:79` |
| F-02 to F-13 | MAJOR | Medium (follow-up candidate) | see below |
| M-01 to M-06 | MINOR | note | see below |

## === REQUIREMENTS ANALYSIS ===

### F-01  CRITICAL, blocking. P0 cannot pass as written, and WC-5 gives a ready command with no contract the wrong outcome
Experts: Wiegers (lead), Adzic. Priority: High. Quality impact: testability 5 to 8 if fixed.

Texts that conflict:
- WC-5 (`SPEC:63`): `--outcome failed` "when the report says `failed` or `blocked`, or no report exists"; `--outcome succeeded` otherwise. WC-4 (`SPEC:62`) defines the report as the `return-contract.yaml`.
- Section 3.1 (`SPEC:79`): ready commands run as workers now and "the worker reports the named file until the command's own phase adds the contract". The named files are `REPORT.md` (troubleshoot, `SPEC:91`), the TDD (tdd), `PROJECT_INDEX.md` and so on, none of which carries a `status` field in the candidate or in the inventories (`INV-B:242`: troubleshoot writes `return-contract.yaml` only under `--caller task-unified`).
- AC-0.4 (`SPEC:194`): run `/sc:troubleshoot` as a P0 smoke test and require "steps 1-3 and 5-7 pass". Step 3 (`SPEC:182`) passes only when "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path". Only step 4 is relaxed ("uses the command's existing report file, since the contract arrives in P1").
- Section 6 (`SPEC:154`, `SPEC:158`): "Later phases do not start until the earlier phase's checks in section 7 pass", and P0 is the gate that "tests the decision before anything is built on it".

Grading sentence: An implementer who follows the stated text as written runs `/sc:troubleshoot` as the P0 smoke worker, which writes `REPORT.md` and no `return-contract.yaml` (its contract arrives in P2, `SPEC:160`, not P1 as AC-0.4 says); WC-5 then treats "no report" as `--outcome failed` for a run that succeeded, and step 3 cannot be satisfied because there is no WC-4 contract path to report; P0 therefore cannot pass, and by `SPEC:154` P1 to P4 never start. This holds with no further assumption: it follows from two stated texts (WC-5 / step 3 versus section 3.1 / AC-0.4) that cannot both be satisfied by the stated command behaviour, and from an acceptance criterion no run can pass.

Same defect for the other ready commands whose contract is not yet written at the time they are used (adversarial's contract path is fixed only in P1, `SPEC:83`; tdd, reflect pre-P2).

Recommendation (narrowest): in WC-5 state how the outcome is decided when the command has no contract yet (outcome from the worker's own reading of the named report file), and in AC-0.4 step 3 replace "the contract's `status`" and "the WC-4 contract path" with "the named report file" for P0, and correct "arrives in P1" to the phase that actually adds each command's contract.

### Medium findings (follow-up candidates, MAJOR label, none blocking)

Each needs a guess that the implementer picks the worse of two allowed readings, or is a requirement the document never states.

**F-02  MAJOR to Medium. WC-4 and WC-6 can leave a stale `blocked` contract at the path the coordinator opens.** Wiegers, Fowler. WC-4 fixes the contract at `<dir>/return-contract.yaml`, where `<dir>` is the directory the brief passes (`SPEC:62`). WC-6 says a command without a resume flag "writes each run into a fresh output directory" (`SPEC:64`), and 15 rows in section 3.2 use "fresh dir". WC-3 (`SPEC:61`) has a worker re-invoke a command after an `ask`. The text does not say who makes the fresh directory. If the command makes a new subdirectory, the first run's `status: blocked` contract stays at the brief-known path and the coordinator reads it; if the command reuses `<dir>`, the retry overwrites the first attempt, which WC-6 forbids. Section 2.3 (`SPEC:72`) does not tell the coordinator to pass a new path on a retry. Fix: say that for "fresh dir" commands the coordinator supplies a new `--output` per attempt, and the contract path is always the one the brief names.

**F-03  MAJOR to Medium. No capability or version check for `--unattended`.** Newman. Commands are installed per machine and run in other projects (`SPEC:34`). The spec says only that the coordinator "does not put `--unattended` in its brief" until a command's phase passes (`SPEC:75`), with no way for a coordinator to know which installed version it is dispatching to. A command definition that predates the flag may treat the token as ordinary text and show its prompts, producing the silent stall `SPEC:44` describes. Fix: a version or capability marker in the installed contract file that the brief template checks (for example, a documented command to read it).

**F-04  MAJOR to Medium. The `--unattended` switch is not defined as a parsed argument.** Whittaker (sentinel collision attack). Concrete attack: `/sc:tdd "explain the --unattended flag" ` or `/sc:spec-panel @file` where the file text contains the token. State trace: before, prompts allowed (SA-1); after, a loose match turns the mode on and gates resolve as blocked for a person. D1 (a) claims it "cannot misfire on a person" (`SPEC:228`) but nothing in section 2 says the token counts only as a standalone argument outside quoted content. The command definition used for this review states that rule for itself (`CMD:459`); the candidate does not require it of the 27 changed commands. Fix: one sentence in WC-2 or section 2.1.

**F-05  MAJOR to Medium. WC-4 does not say how a command tells a directory `--output` from a file `--output`.** Whittaker (zero/empty, divergence). `SPEC:62` picks `<dir>/return-contract.yaml` or `<file>.return-contract.yaml` by what the caller passed. A not-yet-existing path with no extension, or a path with no trailing slash, fits both. Two workers given different readings for the same flag produce different report paths than the brief expects. Fix: decide by the trailing slash or by existence, in one line.

**F-06  MAJOR to Medium. SA-3 and WC-4 disagree on when the contract is written.** Wiegers. WC-4: "In unattended mode the command writes the contract" (`SPEC:62`). SA-3: the contract is written "only in unattended mode or when the caller passes the new output flag" (`SPEC:148`). A run with the new `--output` and no `--unattended` is covered by one text and not the other; AC-1.3 (`SPEC:197`) tests only "no `--unattended` and no new output flag".

**F-07  MAJOR to Medium. SA-4 and AC-C5 disagree on a new flag.** Adzic. SA-4 calls "new flags" additive (`SPEC:149`); AC-C5 requires `grep -E '^-[^-]'` on the command diff to print nothing (`SPEC:176`). Documenting `--unattended` in the existing Usage line is a changed line, so a compliant edit fails AC-C5. The `load` row (`SPEC:112`) is itself a Usage-line edit that SA-4 names as a defect fix, which shows the Usage line is where new flags would go. Fix: say new flags go on a new line, or exempt the Usage line in AC-C5.

**F-08  MAJOR to Medium. AC-C1 can fail on the text SA-2 permits.** Adzic. SA-2 allows a mention of Orca "as an example of a caller's question channel inside the contract file" (`SPEC:147`). AC-C1 greps `src/superclaude/core` and excludes only `ccsession-tag` (`SPEC:172`), and the contract file lives in `core` (`SPEC:52`). If the example is written as `orca orchestration ask`, the grep matches and the common check fails. Fix: exclude `core/WORKER-CONTRACT.md` in AC-C1 or forbid the literal command in the example.

**F-09  MAJOR to Medium. Several requirements have no acceptance check.** Wiegers, Adzic. Mapping WC-1 to WC-12 to section 7: WC-1 (launch path), WC-3 (ask routing), WC-6 (resume or fresh run), WC-11 (parallel writes, only `save` is tested, AC-3.4 at `SPEC:207`) and WC-12 (check before `worker_done`) have no check that could fail. WC-3 and WC-6 are the two that decide whether a blocked worker can be recovered. Fix: add one live check each, or mark them as coordinator-practice rather than testable requirements.

**F-10  MAJOR to Medium. Section 2.3 omits the coordinator's duties while a worker runs.** Nygard, Cockburn. The coordinator "owes" the brief and the post-`worker_done` read (`SPEC:72`). Section 1.4 (2) says the failure mode is a silent stall seen only through `agentWait` or a missing report (`SPEC:44`), and 7.2 step 2 polls for it (`SPEC:181`), but that is a test, not a duty: the contract does not say what the coordinator does on a non-null `agentWait`, on no `worker_done` after a timeout, or on a worker that stops after writing `status: blocked` without `ask`. Related: WC-12 (`SPEC:70`) says the worker checks for follow-ups but not what it does with a coordinator instruction that changes the task.

**F-11  MAJOR to Medium. Shared-worktree edit conflicts are not covered.** Nygard, Fowler. WC-11 (`SPEC:69`) covers output paths and memory keys. Commands that edit source (cleanup, improve, document inline, test `--fix`, explain, implement) run in the shared worktree by default (`CAPS:115`), and 2.3 only lists "the worktree placement" without a rule for when a worker needs its own. Two workers on overlapping targets overwrite each other. Related: cleanup and improve rollback is UNVERIFIED (`INV-A:118`), yet the spec has them apply edits unattended with only a list of changed files (`SPEC:103`, `SPEC:110`).

**F-12  MAJOR to Medium. tasklist departs from its inventory recommendation without a Decisions entry, and its nesting claim is unchecked.** Fowler, Hohpe. `INV-B:215` and `INV-B:295` recommend that Stage 10.5 call reflect without `--remediate`. The spec instead passes `--unattended` to each reflect so the headless auto-accept rule runs (`SPEC:122`), which turns on remediation hand-offs the coordinator did not request, inside N subagents. The row's claim that this stays "inside Claude Code's nesting limit" cites `INV-A:14`, which gives a limit of three layers below the main session; the inventory itself marks nested spawning in this stage UNVERIFIED (`INV-B:210`, `INV-B:314`, `INV-B:322`). The Decisions table (`SPEC:255-269`) has no entry for this choice.

**F-13  MAJOR to Medium. WC-5 does not cover an empty, unparseable or off-vocabulary contract.** Whittaker. WC-5 handles "no report exists" and the four status values (`SPEC:63`). A zero-byte file, invalid YAML, or a command-specific status (for example an existing contract that says `complete`) is neither. Only 7.2 step 4 checks this, in tests (`SPEC:183`). Fix: treat any of these as "no report" in WC-5.

## === ARCHITECTURE ANALYSIS ===

Fowler (lead), Newman, Hohpe, Nygard. The core decision (Orca above, commands stay units of work, no Orca calls inside commands) is supported by the inventories: nesting depth 1 (`CAPS:97-101`), standalone use (`CAPS:147-149`), completion bound to the dispatched pane (`CAPS:150`), and the rejected-alternative table at `SPEC:31-37` matches those lines. The separation of concerns is sound: one contract file, per-command sections that list only their own gates (`SPEC:52`). Open issues are F-02, F-03, F-10, F-11, F-12 above. Observations that are not findings:

- The `--unattended` flag bundles three behaviours (no prompts, fixed report, outward defaults off). That is acceptable because WC-9 lets an explicit flag turn an outward action back on (`SPEC:67`), but the bundle means a coordinator cannot ask for "no prompts" alone.
- Hohpe: the message exchange is specified well for `ask` (resume by ID, no duplicate, `SPEC:61`) and `worker_done` (exactly once, `SPEC:63`). Delivery of coordinator follow-ups is pull-only (`SPEC:70`), consistent with `CAPS:66`.
- Nygard: WC-10 relies on a 5-minute heartbeat cadence taken from one dispatch preamble, not from an Orca guide (`SPEC:68`, `CAPS:130`); the spec states this source, so it is a risk, not a defect (M-04).

## === ADVERSARIAL ANALYSIS (Whittaker) ===

Active in every panel (`CMD:83`). Each finding uses the FR-3 template. Severity uses the grading above.

1. I can break this specification by **Sequence Attack**. The invariant at **WC-4 / WC-6 / WC-3** (`SPEC:61-64`) fails when **a worker's first run stops at a gate, asks, receives an answer and re-invokes a "fresh dir" command**. Concrete attack: (1) run writes `<dir>/return-contract.yaml` with `status: blocked`; (2) worker asks, gets the answer, re-invokes; (3) command creates `<dir>/run-2/` per WC-6; (4) worker sends `worker_done --report-path <dir>/return-contract.yaml` (the brief-known path); (5) coordinator opens the stale blocked file. Before: blocked, no result; after: `succeeded` outcome with a `blocked` contract. Graded Medium (F-02) because it needs the reading in which the command picks the subdirectory.
2. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-5** (`SPEC:63`) fails when **the contract exists but is empty**. Concrete attack: command crashes after creating the file; "no report exists" is false; the status lookup returns nothing; outcome is undefined. Medium (F-13).
3. I can break this specification by **Sentinel Collision Attack**. The invariant at **D1 (a)** (`SPEC:228`) fails when **a legitimate input contains the sentinel `--unattended`**. Concrete attack: see F-04. Medium.
4. I can break this specification by **Divergence Attack**. The invariant at **WC-4** (`SPEC:62`) fails when **`--output` is both a plausible directory and a plausible file**. Concrete attack: see F-05. Medium.
5. I can break this specification by **Sequence Attack**. The invariant at **section 6 gating** (`SPEC:154`) fails when **P0 is run exactly as AC-0.4 states**. Concrete attack: see F-01. Blocking.
6. I can break this specification by **Accumulation Attack**. The invariant at **WC-11** (`SPEC:69`) fails when **several workers run `save`-like or fixed-path commands in one worktree**: `cleanup-audit` keeps one fixed output directory and the row accepts "one audit per worktree at a time (WC-11)" (`SPEC:85`) although WC-11's owner is the command, not the coordinator, and `index-repo` (`PROJECT_INDEX.md`) and `init-lite` (a fixed default report path) have the same property. Medium (F-14 below).

**F-14  MAJOR to Medium. WC-11 is stated as a command duty but the ready rows satisfy it by a coordinator restriction.** Whittaker, Wiegers. `SPEC:69` ("must never write the same file", Owner: Command) against `SPEC:85-87`, where cleanup-audit, index-repo and init-lite keep fixed output paths and nothing assigns the serialisation to the coordinator in section 2.3. No check covers it (F-09).

## === GUARD CONDITION BOUNDARY TABLE ===

Triggered: the candidate contains thresholds and guards (readiness limit, wait size, status vocabulary, depth, flag presence, path kind). Construction: Nygard; completeness check: Crispin role (applied); attack: Whittaker. Classes not listed for a guard are left out for the stated reason. FR-8 and FR-9 findings are graded in the findings above; a GAP here is Medium unless it is F-01.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 report-exists check | `SPEC:63` | Zero/Empty | contract file of 0 bytes | undefined | Not specified (F-13) | GAP |
| WC-5 report-exists check | `SPEC:63` | One/Minimal | contract with only `status: succeeded` and `command` | true | `--outcome succeeded` | OK |
| WC-5 report-exists check | `SPEC:63` | Typical | full contract, `status: partial` | true | `--outcome succeeded`, body says partial | OK |
| WC-5 report-exists check | `SPEC:63,79` | Legitimate Edge Case | ready command with no contract yet (REPORT.md only) | false by WC-4, true by `SPEC:79` | Contradictory (F-01) | GAP |
| WC-5 status vocabulary | `SPEC:62-63` | Sentinel Value Match | `status: blocked` | true | `--outcome failed` | OK |
| WC-5 status vocabulary | `SPEC:62-63` | Legitimate Edge Case | command-specific status outside the four values | undefined | Not specified (F-13) | GAP |
| `--unattended` token | `SPEC:51,228` | Zero/Empty | token absent | false | Today's behaviour (SA-1, `SPEC:146`) | OK |
| `--unattended` token | `SPEC:51,228` | Typical | standalone argument | true | Mode on | OK |
| `--unattended` token | `SPEC:228` | Sentinel Value Match | token inside quoted prompt or input file text | undefined | Not specified (F-04) | GAP |
| contract path rule | `SPEC:62` | Zero/Empty | `--output` omitted | n/a | Not specified for commands that gain `--output` (rows say "add `--output`") | GAP |
| contract path rule | `SPEC:62` | Legitimate Edge Case | path with no extension, not yet created | undefined | Not specified (F-05) | GAP |
| wait-size guard (WC-10) | `SPEC:68` | Typical | one blocking call of 3 minutes | false | No split needed | OK |
| wait-size guard (WC-10) | `SPEC:68` | Maximum/Overflow | one blocking call over 5 minutes (eval up to 3600 s) | true | Split into waits of at most 4 minutes | OK |
| wait-size guard (WC-10) | `SPEC:68` | Legitimate Edge Case | call of 4 to 5 minutes | false | No split required; heartbeat still fits | OK |
| nesting depth (R1, D5) | `SPEC:33,249-253` | Typical | depth 1 | true (blocks nested start) | Command never starts workers (WC-8) | OK |
| nesting depth (R1, D5) | `SPEC:252` | Legitimate Edge Case | user raises depth | false | D5 (b) allows, spec keeps WC-8 regardless | OK |
| confidence gate for `task` | `SPEC:121` | Legitimate Edge Case | confidence exactly 0.70 | below 0.70 is false | Proceeds (the row says "below 0.70") | OK |
| readiness limit (WC-1) | `SPEC:59` | Legitimate Edge Case | fallback at 45 s | at the edge | "well inside" 60 s; evidence says above about 45 s fails | OK |
| `--monitor` under unattended (pr-submit) | `SPEC:114` | Zero/Empty | `--monitor 0` | undefined | Row refuses only `--monitor 1`; 0 not addressed | GAP |

Left out, with reasons: "One/Minimal" and "Maximum/Overflow" for the unattended token, the path rule and the confidence gate (a flag or path has no count; the gate is a ratio bounded at 1). "Sentinel Value Match" for the wait-size, depth and readiness guards (no sentinel value exists for a duration or a count). "Zero/Empty" for the wait-size guard (a zero-length wait never exceeds the limit). The one-row-per-class completeness rule (FR-10) is met by these reasons; every GAP above is already recorded as a finding or, for the last row, is the Medium note M-05.

## === PIPELINE DIMENSIONAL ANALYSIS ===

Triggered: the spec is a multi-stage classification and rollout (43 commands, then verdict groups, then phases). Fowler annotated counts; Whittaker attacked each divergence (N != M). No mismatch found: every count conserves, and no consumer assumes a different total.

```text
[43 commands in src/superclaude/commands]  (SPEC:76; INV-A:3 = 21, INV-B:3 = 22)
   --> [Verdict split]
        ready 10 (SPEC:78)            = A 5 + B 5   (INV-A:73, INV-B:278)
        needs change 27 (SPEC:94)     = A 13 + B 14
        coordinator-only 6 (SPEC:127) = A 3 + B 3
   --> [Phase assignment]
        ready 10   : P1 fixes 3 (adversarial, cleanup-audit, index-repo)
                     P2 gate edits 4 (reflect, release-split, tdd, troubleshoot)
                     no change 3 (brainstorm, init-lite, workflow)
        needs 27   : P1 9, P2 11, P3 4, P4 3
        coordinator-only 6 : no phase
   --> [Consumers] P2 list at SPEC:160 names 15 = 11 + 4 (consistent);
                   P1 list at SPEC:159 names 12 = 9 + 3 (consistent);
                   P3 = 4, P4 = 3 (consistent)
```

Note M-01: the intro of 3.1 (`SPEC:79`) says "`brainstorm` and `init-lite` have no change" while the table shows a third no-change command, `workflow`.

## Notes (MINOR)

- **M-01** `SPEC:79` lists two no-change commands; the table at `SPEC:92` shows three (see the diagram above).
- **M-02** `SPEC:112` says "none (see note)" for `load`; the note is in section 4's last paragraph (`SPEC:139`) and the Decisions table (`SPEC:265`), not under the table.
- **M-03** `SPEC:17` says only 11 section-3 locations were re-read by this worker and the rest were "carried from the inventories without a second read", while `SPEC:285` says a validator re-read about 340 citations in this spec. Reconcile or say which applies to section 3. Also E2 (`SPEC:22`) is worded as proof that a worker "has the same tools as a command a person runs", while section 1.4 (1) (`SPEC:43`) says no command was run end to end as a worker.
- **M-04** The 5-minute heartbeat cadence and the 4-minute wait size rest on one dispatch preamble (`SPEC:68`, `SPEC:266`, `CAPS:130`); a coordinator with another cadence changes WC-10.
- **M-05** `pr-submit` under `--unattended` with `--monitor 0` is not addressed (`SPEC:114`); only `--monitor 1` is refused.
- **M-06** The command definition read for this review describes its own unattended mode with `--report-dir` and an `--output` that is file-valued (`CMD:457-463`), while the spec-panel row says "add `--output`; contract" (`SPEC:120`) and WC-4 describes `--output` as either a directory or a file (`SPEC:62`). The command definition is not part of the shared evidence (`README:11-17`), so this is a note only: a phase plan for spec-panel should read the installed command first.

## Follow-up candidates (Medium and minor, never blocking)

Medium: F-02, F-03, F-04, F-05, F-06, F-07, F-08, F-09, F-10, F-11, F-12, F-13, F-14.
Minor: M-01, M-02, M-03, M-04, M-05, M-06.

This run is an unattended worker run with a fixed final reply, so the once-per-loop question to the user about opening an issue for these items was not asked. The list is recorded here and no issue was created (`CMD:260`).

## Reviser brief

Blocking finding ids: F-01

Rules for the reviser (this section restates the Reviser contract; the reviser reads this report, not the command):
- Revise only text a blocking finding names.
- Add no rule, mechanism or section that a blocking finding does not call for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings alone; do not apply them.

verdict: FAIL
