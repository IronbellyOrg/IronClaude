review: 1 of 3
> verification (coordinator, VERIFY step VF1; verifier reply .dev/orca-command-refactor/review/verify-1.md): confirmed blocking ids: F1, F2. Rejected, kept as noted, unactioned and not prior blocking findings for the next re-review: none. The Reviser brief below is narrowed to the confirmed ids.

# Spec-panel review, round 1: orca-worker-contract-spec.md

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Prompt followed: FIRST-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (285 lines).
- Baseline / prior report: none given, so this is a first review of the full document.
- Reviewer model actually used: `claude-sonnet-5-5` (Sonnet 5.5).
- Mode: critique. Focus: requirements, architecture. Whittaker is active in every panel. `--focus correctness` is not active, so no State Variable Registry is produced.
- Citation shorthand: `S:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`. Any `cmd/`, `sk/`, `ag/` or `src/` path, `CLAUDE.md`, `EVIDENCE.md`, and any Orca guide or compiled-JS line is UNVERIFIED here: those files are not in the workspace, so I could check them only through the inventory line that quotes them.

## Result in one paragraph

The decision itself (Orca coordinates, commands stay units of work, `--unattended` plus a report file plus resume) is well supported by the checkable evidence and I found no wrong outcome in it. Two stated texts in the candidate contradict each other in ways that make a stated acceptance check impossible to pass: the P1 check AC-1.1 against the rollout and decisions (F1), and the WC-4 contract path against the adversarial and workflow rows and the live check (F2). Both are blocking. Twelve further findings are Medium (a missing rule or a reading the implementer must guess) and are listed under follow-up candidates, with five minor notes.

## Panel record (fixed review order)

1. Wiegers (lead, requirements): traceability and consistency between the WC rules, section 3, section 6 and section 7. Findings F1, F2, F4, F5, F9, F12, F13.
2. Adzic: examples and state traces for the blocked, retry and stale-file paths. Findings F3, F6.
3. Cockburn: primary actor is the coordinator, the goal is "run one command as a unit and read one trustworthy result". The Owner column of S:57-70 mixes three actors (command text, worker session, coordinator); F8 and F14 come from that.
4. Fowler (lead, architecture): interface and contract boundaries. Findings F2, F11, F14.
5. Nygard: failure modes and guard boundaries. Findings F7, F8, F10, and the Guard Condition Boundary Table.
6. Whittaker: five attacks, recorded in the adversarial analysis section.
7. Newman: contract evolution. Note N4 (no version field on a new shared contract while the existing workflow contract is versioned, INV-B:272).
8. Hohpe: message exchange for `ask`/`reply`/`worker_done`. Finding F6.
9. Crispin: completeness check of the guard table and testability. Finding F13.
10. Gregory: the spec records one author and one citation validator (S:11, S:285) and no one who will implement or operate the contract; no separate finding.
11. Hightower: operational concerns folded into F8 and F14 (install step, observability when no `worker_done` arrives).

Auto-suggestion (advisory only): the candidate has numeric thresholds (60 s, 5 min, 4 min, 240 s, depth 1) and several guards, so `--focus correctness` is worth running on the revised text.

## Coverage statement

Covered:
- All of S:1-285 read in full. Inventories read in full: INV-A (120 lines), INV-B (323), CAPS (188). README read in full.
- Every `INV-A:`, `INV-B:` and `CAPS:` citation in sections 1, 3, 4 and 7 and in the UNVERIFIED list was matched to its inventory line. All are on the right line; the inventory cells support the spec's rows (the 10 / 27 / 6 split, the per-row phase assignments, the 43 total).
- Count conservation: INV-A has 5 ready + 13 needs-change + 3 coordinator-only = 21 (INV-A:73); INV-B has 5 + 14 + 3 = 22 (INV-B:278); the spec has 10 + 27 + 6 = 43 (S:76). The 27 section 3.2 rows carry phases 9 (P1) + 11 (P2) + 4 (P3) + 3 (P4) = 27, and S:160 lists the same 11 P2 gate commands plus 4 ready commands. No mismatch.
- Pipeline Dimensional Analysis (FR-17): not triggered. The spec has no multi-stage data flow whose output count differs from its input count; the only counted flow is the 43-command partition, which conserves. No Quantity Flow Diagram is produced.

Not covered (UNVERIFIED, not in the workspace): every `cmd/`, `sk/`, `ag/`, `src/` line, `EVIDENCE.md`, `CLAUDE.md`, the Orca guide text and compiled JS, and the claims at S:11 (11 locations re-read) and S:285 (about 340 citations re-read, 9 defects fixed). I took those only as the inventories relay them.

Review-loop handling: no brief clause was overridden. The brief did not pass `--unattended` or `--report-dir`, so no `return-contract.yaml` is written (the brief says write only this file). The Improve step (Behavioral Flow step 6) was not run: the brief assigns only this report and the command's Boundaries forbid modifying a specification without consent. This session has no user channel, so the one-time question "open an issue for the follow-up candidates?" is left to the coordinator; nothing was created.

## Findings table (graded by consequence)

| Id | Label | Graded | Where | One line |
|---|---|---|---|---|
| F1 | MAJOR | Blocking | S:195, S:159, S:112, S:240, S:139, S:154 | AC-1.1 and the P1 scope contradict D3(a), the load row and the phase ordering |
| F2 | MAJOR | Blocking | S:62, S:83, S:92, S:182, S:198 | WC-4 contract path contradicts the adversarial and workflow rows and the live check |
| F3 | MAJOR | Medium | S:64, S:62, S:183, S:73 | A stale or first-attempt contract is accepted as this run's result |
| F4 | MAJOR | Medium | S:62, S:87, S:90, S:73 | WC-4 has no rule when `--output` is a file, absent, or fixed |
| F5 | MAJOR | Medium | S:73, S:158, S:194 | The P0 brief must carry `--unattended`, which P0 forbids adding |
| F6 | MAJOR | Medium | S:61, S:109, S:236 | WC-3 re-invoke has no cap, no resume carve-out, no Ruling carve-out |
| F7 | MAJOR | Medium | S:68, S:114, S:210 | WC-10 trigger (5 min) vs target (4 min) vs AC-4.3 (240 s); subagent waits unaddressed; pr-submit claim unverified |
| F8 | MAJOR | Medium | S:44, S:62, S:73 | No coordinator rule for a worker that never sends `worker_done` |
| F9 | MAJOR | Medium | S:62, S:63, S:183, S:261 | Status vocabulary of existing contracts unchecked; malformed contract unmapped |
| F10 | MAJOR | Medium | S:67, S:88 | WC-9 list omits reflect's default folder move and tracked-file write, and workflow staging |
| F11 | MAJOR | Medium | S:88, S:122 | tasklist/reflect row departs from the inventory's recommendation; nesting claim stated as fact |
| F12 | MAJOR | Medium | S:69, S:85-87 | WC-11 vs three "ready today" commands with fixed output paths |
| F13 | MAJOR | Medium | S:61, S:64, S:70, S:195-210 | WC-3, WC-6, WC-12 have no acceptance check; no WC-to-AC trace |
| F14 | MAJOR | Medium | S:52, S:158, S:172, S:147 | Contract file delivery in a checkout, and AC-C1 scans the folder the contract lives in |
| N1-N5 | MINOR | Note | see below | |

## === REQUIREMENTS ANALYSIS ===

### F1 (blocking) - AC-1.1 and the P1 scope cannot be satisfied alongside D3(a), the load row and the phase order
- Expert: Wiegers (lead), Cockburn. Severity: MAJOR, graded blocking. Priority: High. Quality impact: Consistency +2, Testability +1.
- Texts, all in the candidate:
  - AC-1.1 (S:195): the P1 test "asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one".
  - P1 scope (S:159): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)".
  - `/sc:pr-submit` is in section 3.2 (S:114), but D3(a), the recommended option, says "no pr-submit changes in Phase 4" (S:240), and S:139 says it "stays a worker candidate only if the user accepts open decision D3".
  - `/sc:load` is in section 3.2 with "Report (WC-4): none (see note)" and "use it as a step inside another worker's brief, not as its own Task" (S:112), and its phase is "P1 (usage line only)".
  - Phase order: "Later phases do not start until the earlier phase's checks in section 7 pass" (S:154); P4 "waits for answers to D2-D4" (S:154, S:162); gate resolution for auggie-review, cleanup, task, tasklist and the other P2 commands is assigned to P2 (S:100-122, S:160).
- Grading sentence: An implementer who follows S:195 and S:159 builds a P1 in which pr-submit, load, implement and post-release (and every P2 command) already carry a `## Unattended mode` section naming `return-contract.yaml` and accept `--unattended`, and X is wrong because S:240 says pr-submit gets no changes under the recommended D3(a), S:112 gives load no report, and S:60 and S:67 say a command under `--unattended` never prompts and never posts, yet between P1 and P2 `/sc:auggie-review <PR> --unattended` would still post to GitHub and offer remediation (INV-A:38) and `/sc:cleanup --unattended` would still prompt for approval (INV-A:43). The check AC-1.1 also cannot pass without that wrong build, which means P1 cannot be closed and S:154 blocks every later phase.
- Recommendation: narrow AC-1.1 to the P1-phase commands listed in S:159 and move the per-command assertion for each P2, P3 and P4 command into that phase's own check (AC-2.1, AC-3.x, AC-4.x already have the pattern). Delete "accepted by every command in sections 3.1 and 3.2" from the P1 row, or restrict it to commands with no gate. Remove load from the "has a section" set and state that pr-submit is in the set only under D3(b). Rationale: this deletes and narrows; it adds no rule.

### F2 (blocking) - WC-4's contract path contradicts the adversarial row, the workflow row and the live-check pass condition
- Expert: Wiegers (lead), Adzic, Fowler. Severity: MAJOR, graded blocking. Priority: High. Quality impact: Consistency +2, Testability +1.
- Texts:
  - WC-4 (S:62): the command writes "`<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)"; the report file is "known before dispatch".
  - Section 2.3 (S:73): the brief states "the output directory, so the report path is known before dispatch (WC-4)".
  - Adversarial row (S:83): the brief passes `--output <dir>` and the small fix is "Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)"; AC-1.4 (S:198) checks that "adversarial names one fixed path". INV-A:60 confirms the two real nested locations that exist today.
  - Workflow row (S:92): the contract is `.dev/tasks/to-do/<id>/return-contract.yaml`, a package directory the command generates (INV-B:272-273 "never overwrites or reuses an existing package"); the brief passes no directory.
  - Live check step 3 (S:182): pass requires "its report path is the WC-4 contract path".
- Grading sentence: An implementer who follows WC-4 builds adversarial writing `<dir>/return-contract.yaml`, and X is wrong because S:83 and AC-1.4 (S:198) require `<dir>/adversarial/return-contract.yaml`; an implementer who follows S:83 builds the nested path and then S:182 cannot pass, because the nested file is not "the WC-4 contract path". For workflow the generated `<id>` directory is not a directory the coordinator passed, so "known before dispatch" (S:62, S:73) cannot hold.
- Recommendation: replace the single fixed pattern in WC-4 with "the path named in the command's row of section 3, which the brief or the command's documented default makes known before dispatch", and state in the workflow row that the coordinator learns the path from the worker's `--report-path` instead. Or change the adversarial row to `<output>/return-contract.yaml`. Either choice removes the contradiction; the first adds one clause and deletes the false generalisation.

### F3 (Medium) - a stale or first-attempt contract is accepted as this run's result
- Expert: Adzic, Wiegers. Severity: MAJOR, graded Medium (the wrong outcome needs the coordinator to reuse a directory). Priority: Medium. Quality impact: Testability +1.
- Texts: WC-6 (S:64) puts the "fresh output directory" duty on the Command, while WC-4 (S:62) and 2.3 (S:73) fix the directory as the one the coordinator passed. A retry with `worker-start --retry-of` re-sends the same brief. Live check step 4 (S:183) accepts any non-empty file with a valid `status` and a `command` value; it has no freshness test.
- Concrete trace (Adzic): attempt 1 of `/sc:analyze` with `--output D` writes `D/return-contract.yaml` with `status: failed`. Attempt 2 is dispatched with the same brief, crashes before writing (WC-4 says it is written on every outcome, S:62, but a killed session cannot honour that). The coordinator reads `D/return-contract.yaml`, sees attempt 1's file, and `test -s` and the YAML assertion pass.
- Recommendation: add to 2.3 that a retry brief names a new output directory, and add one pass condition to step 4 that the contract's mtime is later than the Dispatch start or that the contract records the Dispatch ID. Delete "writes each run into a fresh output directory" from WC-6 if the coordinator owns that.

### F4 (Medium) - WC-4 has no rule when `--output` is a file, is absent, or is fixed
- Expert: Wiegers, Whittaker (zero/empty attack). Severity: MAJOR, graded Medium (two readings). Priority: Medium. Quality impact: Completeness +1.
- Texts: WC-4 treats `--output` as a directory (S:62). Section 3.1 says tdd takes `--output <file>` (S:90) and init-lite takes `--output <file>` (S:87); cleanup-audit's output directory "is fixed" (S:85) and index-repo writes `PROJECT_INDEX.md` with the location "implied" (S:86). Section 2.3 relies on the coordinator to supply a directory (S:73), but no rule says what a command does under `--unattended` when none is supplied, or where a `blocked` contract goes when there is nowhere to write.
- Recommendation: add one sentence to WC-4: the contract goes in the directory named by `--output-dir`; for a file-valued `--output` it goes beside that file; with neither, the command stops with `blocked` printed in chat only. This is the smallest addition that makes AC-1.1's "naming `return-contract.yaml`" checkable for those commands.

### F5 (Medium) - the P0 brief must carry `--unattended`, which P0 forbids adding
- Expert: Wiegers. Severity: MAJOR, graded Medium (the specific AC-0.4 lines omit the flag). Priority: Medium. Quality impact: Consistency +1.
- Texts: 2.3 (S:73): the brief states "the exact command line including `--unattended`". 7.2 step 1 builds the brief "per section 2.3" (S:180). P0 is "no command edits" (S:158) and the flag arrives in P1 (S:159). AC-0.4 (S:194) lists the P0 command lines without it.
- Consequence: an implementer who builds the P0 brief template from 2.3 hands the three smoke commands a flag they do not define (adversarial's flag parsing is not shown anywhere I can read), and AC-0.4 can pass only if they ignore it.
- Recommendation: in 2.3 say the flag is included "once the command defines it (P1 onward)", and say in AC-0.4 that P0 runs without it.

### F9 (Medium) - the status vocabulary of the existing contracts is unchecked, and a malformed contract is not mapped
- Expert: Wiegers, Whittaker (sentinel collision). Severity: MAJOR, graded Medium (UNVERIFIED either way). Priority: Medium. Quality impact: Testability +1.
- Texts: WC-4 (S:62) "Commands that already write a contract keep their fields and add the missing ones"; WC-5 (S:63) maps only four `status` values; step 4 (S:183) asserts `d['status'] in {'succeeded','partial','failed','blocked'}` for every command, including adversarial, brainstorm, reflect and workflow whose contracts already exist (S:261 cites INV-B:272, INV-A:39, INV-B:112, INV-A:35). None of those inventory cells lists the existing `status` values; INV-B:272 says only that a `status` field exists. If an existing contract uses another vocabulary, "keep their fields" and the fixed set conflict. WC-5 says "or no report exists" (S:63) but gives no outcome for an empty or unparseable file.
- Recommendation: add a one-line check to P1 that lists each existing contract's `status` values from the skill text before the vocabulary is fixed, and add "unreadable counts as no report" to WC-5.

### F12 (Medium) - WC-11 against three commands the spec calls ready today
- Expert: Wiegers. Severity: MAJOR, graded Medium (3.1 already names the one-audit limit for cleanup-audit). Priority: Low. Quality impact: Consistency +1.
- Texts: WC-11 (S:69): "Two workers in one worktree must never write the same file. Default output paths carry a timestamp or the slug the coordinator passes". Section 3.1: cleanup-audit "output dir is fixed, so one audit per worktree at a time (WC-11)" (S:85); index-repo writes `PROJECT_INDEX.md` (S:86); init-lite writes `.dev/superclaude/context-audit.md` by default (S:87). Section 2.3 (S:73) does not require the coordinator to serialise these or give each its own worktree.
- Recommendation: either list in 2.3 "one worker per worktree for commands whose output path is fixed" or weaken WC-11 for the three rows. One sentence, no new mechanism.

### F13 (Medium) - WC-3, WC-6 and WC-12 have no acceptance check, and there is no WC-to-AC trace
- Expert: Wiegers, Crispin. Severity: MAJOR, graded Medium (a missing check, not a wrong text). Priority: Medium. Quality impact: Testability +2.
- Evidence: I traced each requirement to section 7. WC-1 (step 1, S:180), WC-2 (AC-2.2, S:200), WC-4 (step 4, S:183), WC-5 (step 3, S:182), WC-7 (AC-0.4 transcript, S:194), WC-8 (AC-C1, S:172), WC-9 (AC-2.4, AC-4.2, S:202, S:209), WC-10 (AC-4.3 only, S:210), WC-11 (AC-3.4 for save only, S:207). WC-3 (ask path, S:61), WC-6 (retry or safe re-run, S:64) and WC-12 (`consumer_fenced`, S:70) appear in no check. AC-2.2 (S:200) tests the blocked contract but not the `ask` route the spec offers instead.
- Recommendation: add a trace column to the WC table naming the AC id, and add one check each for WC-3 (a worker that receives an `ask` reply continues), WC-6 (`--retry-of` leaves the first attempt's directory unchanged) and WC-12, or mark them "not tested in this plan".

## === ARCHITECTURE ANALYSIS ===

### F6 (Medium) - WC-3's re-invoke has no cap, no resume carve-out and no Ruling carve-out
- Expert: Hohpe (lead), Fowler, Adzic. Severity: MAJOR, graded Medium. Priority: Medium. Quality impact: Completeness +1.
- Texts: WC-3 (S:61): the worker "may instead ask the coordinator once, wait, then re-invoke or resume the command with the answer as a flag". Section 3.2 gives cli-portify three gates (S:105) and task several (S:121). Most rows say Resume is "fresh dir" (S:99-125), so re-invoking is a full re-run. D2(a) (S:234) says the implement worker ends `failed` and nobody relays a Ruling, and S:218 (non-goal 6) keeps the rule.
- Traces: (1) "once" is per run or per gate? With cli-portify's three gates the run could ask three times. (2) For a "fresh dir" command, re-invoking repeats all fan-out and writes into a new directory, so the first `blocked` contract and the second run's contract are in different places (see F2 and F3). (3) WC-3 does not exclude implement, so a worker could relay the coordinator's answer as a Ruling, which D2(a) rules out.
- Recommendation: state in WC-3 "once per gate, at most as many times as the command has gates", limit the re-invoke route to commands that have a resume flag in section 3, and say it does not apply to the implement Ruling unless D2(b) is chosen.

### F7 (Medium) - WC-10's trigger, target and acceptance threshold disagree; subagent waits are not covered; the pr-submit budget claim is unverified
- Expert: Nygard (lead), Whittaker. Severity: MAJOR, graded Medium. Priority: Medium. Quality impact: Consistency +1, Completeness +1.
- Texts: WC-10 (S:68): a step that blocks "for longer than 5 minutes" must be "split into waits of at most 4 minutes", and the worker "sends a heartbeat every 5 minutes". AC-4.3 (S:210): "no single tool call exceeds 240 s". A 270 s wait is not "longer than 5 minutes", so WC-10 allows it, and AC-4.3 rejects it.
- Second gap: WC-7 (S:65) forbids a subagent from sending a heartbeat, and a foreground Agent-tool wave (cleanup-audit, tdd, post-release, per INV-A:42, INV-B:221, INV-B:81) blocks the top-level session just as a poll does. WC-10 names only "a poll wait, a long eval". The consequence of a missed heartbeat is itself UNVERIFIED (CAPS:130, CAPS:182 item 7), so WC-10 is a hard rule on an unproven effect.
- Third: S:68 and S:114 assert that pr-submit's 600 s "is a cumulative per-wait budget made of repeated iterations... not one blocking call", citing `cmd/pr-submit.md:49` and `sk/sc-pr-submit-protocol/SKILL.md:46-64`. Those lines are not in the set the spec says it re-read (S:11), and INV-B:95 says only that the loop "waits up to `--timeout` 600 s per wait over several rounds". UNVERIFIED; the P4 text depends on it.
- Recommendation: use one number in WC-10 and AC-4.3 (split anything over 4 minutes), name foreground Agent-tool waves in WC-10 or list them as an accepted gap, and mark the pr-submit budget reading UNVERIFIED in S:68 and S:114.

### F8 (Medium) - no coordinator rule for a worker that never sends `worker_done`
- Expert: Nygard (lead), Hightower, Cockburn. Severity: MAJOR, graded Medium. Priority: Medium. Quality impact: Completeness +1.
- Texts: S:44 says the real failure mode of a command prompt "is a silent stall with no `worker_done`, which the coordinator sees only through `worker-show`'s `agentWait` or a missing report. Section 2 covers both cases." Section 2 has WC-1 and WC-2, which prevent the stall; it has no coordinator action when `agentWait` is non-null, when the session exits without a report, or when the contract is absent. WC-4's "written on every outcome" (S:62) cannot hold for a killed or exhausted session. The only stall handling is an acceptance observation at 7.2 step 2 (S:181). Section 2.3 (S:73) lists only what happens after `worker_done`.
- Recommendation: add to 2.3 one line: on a non-null `agentWait`, no `worker_done`, or a missing contract, the coordinator reads the transcript (`worker-read`, CAPS:131), then retries with a new output directory (F3) or reports failure; it never releases on silence (CAPS:111). Correct S:44 to say what section 2 actually covers.

### F10 (Medium) - WC-9's list omits actions the inventories show are on by default
- Expert: Nygard, Fowler. Severity: MAJOR, graded Medium (the harm needs the brief to omit a flag). Priority: Medium. Quality impact: Completeness +1.
- Texts: WC-9 (S:67) turns off "pushes, opens a PR, posts to GitHub, installs, provisions or calls a paid external run". INV-B:114 records that `/sc:reflect` UC-2 by default moves the validated work-unit folder to its destination and writes the tracked file `docs/memory/reflect/deviation-patterns-<slug>.md`; the spec's reflect row (S:88) offers `--no-promote` only "when the coordinator owns folder moves", so the default stays on. INV-B:274 records that workflow's skill says `.dev/tasks/` "is always staged" and that it is UNVERIFIED whether the skill runs `git add`; the workflow row (S:92) says nothing. INV-B:134 records research's Tavily and Playwright web access (S:116 treats it as harmless).
- Recommendation: in the reflect and workflow rows, state the folder move, the tracked-file write and the staging as outward actions that are off under `--unattended` unless the brief names them. If that is judged too large, record them under UNVERIFIED instead.

### F11 (Medium) - the tasklist/reflect row departs from the inventory's recommendation without a recorded decision, and a nesting claim is stated as fact
- Expert: Fowler, Newman. Severity: MAJOR, graded Medium. Priority: Medium. Quality impact: Consistency +1.
- Texts: S:122: "Stage 10.5 passes `--unattended` to each reflect so the headless rule applies... (its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`)". INV-B:215 recommends the opposite: "Stage 10.5 should call reflect without `--remediate` (or headless) so no yes/no offer can fire". INV-B:210 and UNVERIFIED items 1 and 8 (INV-B:314, INV-B:322) say it is UNVERIFIED whether nested spawning works and who answers the offer. The spec's UNVERIFIED list (S:271-285) lacks that item, and no row in Decisions (S:255-269) records the choice. S:88 maps reflect's `--remediate` to "the existing headless auto-accept rule", but INV-B:109 says that rule auto-accepts only "auto-fixable registers", and INV-B:209 says `needs_human_decision` items HALT; the spec gives that HALT no resolution under WC-2.
- Consequence if built as written: every tasklist phase auto-accepts a remediation handoff inside an unattended worker, and a `needs_human_decision` HALT inside a subagent has no WC-2 outcome.
- Recommendation: either follow INV-B:215 (drop `--remediate` under `--unattended`) or record the decision, add the nesting question to UNVERIFIED, and map `needs_human_decision` to `blocked`.

### F14 (Medium) - how the shared contract file reaches a session, and AC-C1 scans the folder it lives in
- Expert: Newman, Hightower, Fowler. Severity: MAJOR, graded Medium. Priority: Medium. Quality impact: Testability +1.
- Texts: S:52 puts the contract at `src/superclaude/core/WORKER-CONTRACT.md`, installed to `~/.claude/WORKER-CONTRACT.md`; each command points to the installed path. P0 live runs (S:194) need that file to exist where the worker reads it, but the plan never includes `superclaude install` or any sync step before the smoke runs (the spec's own pointer to the repo rule is `CLAUDE.md:72-83`, UNVERIFIED here, and the project instructions list `make sync-dev` as copying skills, agents, commands, hooks and templates, not core files). AC-C1 (S:172) requires no match for `orca(-ide)? (orchestration|worktree|terminal|agent)` under `src/superclaude/core`, the directory that will hold WORKER-CONTRACT.md, while SA-2 (S:147) permits the contract file to mention Orca "as an example of a caller's question channel", and the P0 task also adds an Orca section to HOW-WE-WORK.md in that same directory (S:158). A mention such as "the preamble's `orca orchestration ask`" fails AC-C1.
- Recommendation: add an install-or-copy step to the P0 live check, and exclude `core/WORKER-CONTRACT.md` (or the one Orca section) from AC-C1 by path, so SA-2 and AC-C1 agree.

## === ADVERSARIAL ANALYSIS (Whittaker) ===

Severity here uses CRITICAL / MAJOR / MINOR; the graded column says how each was graded by consequence.

1. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 / 2.3 (S:62, S:73)** fails when **a coordinator dispatches `/sc:analyze ... --unattended` with no output directory**. Concrete attack: before, the brief has no `--output`; the command reaches a gate and resolves `blocked` (WC-2 c); after, the contract has nowhere to be written (the command has no default under S:99), the worker's `--report-path` has no real value (CAPS:74), and the coordinator sees `worker_done --outcome failed` with no readable question. MAJOR, graded Medium. See F4.
2. I can break this specification by **Divergence Attack**. The invariant at **WC-10 (S:68) vs AC-4.3 (S:210)** fails when **a wait is 270 s**. Concrete attack: WC-10 does not trigger (270 s is not above 300 s), the implementer leaves the poll alone, AC-4.3 fails the P4 check on a 240 s limit. MAJOR, graded Medium. See F7.
3. I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-5 (S:63) and step 4 (S:183)** fails when **an existing contract carries `status: success` or another word outside the fixed four**. Concrete attack: adversarial's own contract reports `success`, WC-4 says keep the field, the step-4 assertion rejects the file, and a successful run reads as a failed check. A second collision: `blocked` and `failed` both map to `--outcome failed` (S:63), so the Orca record alone cannot tell a gate stop from a crash; only the file can. MAJOR, graded Medium. See F9.
4. I can break this specification by **Sequence Attack**. The invariant at **WC-6 / WC-4 / step 4 (S:64, S:62, S:183)** fails when **a retry reuses the first attempt's directory**. Concrete attack: attempt 1 leaves `D/return-contract.yaml` (`failed`); attempt 2 under `--retry-of` writes nothing; the coordinator's `test -s D/return-contract.yaml` passes. A second sequence break is rollout order: P1's check (S:195) requires sections that the spec places in P2 to P4 (S:154, S:160, S:162). MAJOR; the second is blocking. See F3 and F1.
5. I can break this specification by **Accumulation Attack**. The invariant at **WC-3 "ask the coordinator once" (S:61)** fails when **a command has several gates**. Concrete attack: cli-portify blocks at gate 1 (S:105); the worker asks once and re-invokes with the answer; gate 2 blocks; WC-3 does not say whether a second `ask` is allowed or how many re-runs are allowed, and for a command with "fresh dir" resume each re-invoke repeats the whole fan-out. MAJOR, graded Medium. See F6.

## === GUARD CONDITION BOUNDARY TABLE ===

Nygard built it, Crispin checked completeness, Whittaker attacked entries. Classes left out are named with a one-line reason in the notes after the table. Every guard found in the spec is listed.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `readiness_fallback` | WC-1, S:59 | Zero/Empty | no startup prompt, no fallback (`null`) | pass (no prompt to wait on) | no prompt may wait on a person before the input box is ready | OK |
| `readiness_fallback` | WC-1, S:59 | Typical | prompt with 30 s auto-fallback | pass | cited as passing at EVIDENCE.md:45 (UNVERIFIED here, via S:59) | OK |
| `readiness_fallback` | WC-1, S:59 | Maximum/Overflow | fallback 50 s, default limit 60 s | undefined | "well inside the readiness limit" has no number; the cited 45 s figure is the timeout used in that test, not the 60 s default | GAP |
| `wait_split` | WC-10, S:68 | Zero/Empty | 0 s wait | not triggered | no split needed | OK |
| `wait_split` | WC-10, S:68 | Typical | 3 min wait | not triggered | no split needed | OK |
| `wait_split` | WC-10, S:68 / AC-4.3, S:210 | Legitimate Edge Case | 270 s wait | WC-10 not triggered; AC-4.3 fails | the two thresholds (300 s, 240 s) disagree | GAP |
| `wait_split` | WC-10, S:68 | Maximum/Overflow | 3600 s eval | triggered | split into waits of at most 4 min (cli-eval row, S:104) | OK |
| `wait_split` | WC-10, S:68 / WC-7, S:65 | Legitimate Edge Case | foreground Agent-tool wave over 5 min | undefined | WC-7 bars subagent heartbeats; WC-10 names polls and evals only | GAP |
| `outcome_map` | WC-5, S:63 | Zero/Empty | no contract file | `failed` | "or no report exists" gives `--outcome failed` | OK |
| `outcome_map` | WC-5, S:63 | One/Minimal | empty or unparseable contract (`""`) | undefined | not stated; only "no report exists" is mapped | GAP |
| `outcome_map` | WC-5, S:63 | Typical | `status: succeeded` | `succeeded` | `--outcome succeeded` | OK |
| `outcome_map` | WC-5, S:63 | Legitimate Edge Case | `status: partial`, or audit verdict FAIL | `succeeded` | stated, with the first sentence naming the status | OK |
| `outcome_map` | WC-5, S:63 | Sentinel Value Match | `status` outside the four (an existing contract's own word) | undefined | not stated; step 4 (S:183) rejects it | GAP |
| `gate_resolution` | WC-2, S:60 | Zero/Empty | `--unattended` with no output directory | undefined | no rule where the `blocked` contract is written | GAP |
| `gate_resolution` | WC-2, S:60 | Typical | gate with the answering flag in the brief | (b) | the flag resolves it | OK |
| `gate_resolution` | WC-2, S:60 / research row, S:116 | Sentinel Value Match | brief passes `--strategy intent`, `--unattended` pins `planning` | undefined | precedence between pin and explicit flag not stated | GAP |
| `gate_resolution` | WC-2, S:60 | Legitimate Edge Case | gate reached after partial outputs exist (cli-portify phase 3) | (c) | contract `blocked` with artifacts listed (S:62) | OK |
| `outward_default_off` | WC-9, S:67 | Zero/Empty | brief names no authorisation | off | stated | OK |
| `outward_default_off` | WC-9, S:67 | Typical | brief names the command's own flag | on | stated, subject to D4 (S:244) | OK |
| `outward_default_off` | WC-9, S:67 / S:88, S:92 | Legitimate Edge Case | reflect default folder move and tracked-file write, workflow staging | undefined | not in the WC-9 list | GAP |
| `contract_written` | SA-3, S:148 / WC-4, S:62 | Zero/Empty | standalone run, no flags | no file | stated | OK |
| `contract_written` | SA-3, S:148 / WC-4, S:62 | Legitimate Edge Case | standalone run with the new output flag, no `--unattended` | undefined | SA-3 allows a contract; WC-4 requires one only under `--unattended` | GAP |
| `ask_budget` | WC-3, S:61 | Zero/Empty | no preamble in the session | `blocked` | the worker session may ask only if it holds a preamble | OK |
| `ask_budget` | WC-3, S:61 | One/Minimal | one gate, one `ask` | reply received | re-invoke with the answer as a flag | OK |
| `ask_budget` | WC-3, S:61 | Maximum/Overflow | cli-portify, three gates (S:105) | undefined | "once" per run or per gate not stated; no cap on re-invokes | GAP |
| `ask_budget` | WC-3, S:61 / S:234 | Legitimate Edge Case | implement Ruling relayed by `ask` | undefined | WC-3 does not exclude it; D2(a) forbids it | GAP |
| `nesting_depth` | R1, S:33 / WC-8, S:66 | Typical | depth 1, command calls `worker-start` | refused | `nested_worker_depth_exceeded` (CAPS:99) | OK |
| `nesting_depth` | D5, S:249-252 | Legitimate Edge Case | depth raised | allowed | D5(b) says it breaks R1's protection | OK |
| `partition_count` | S:76 | One/Minimal | one command in two buckets | would break the count | none occurs: 43 = 10 + 27 + 6, checked above | OK |

Classes omitted, with reasons: `readiness_fallback` Sentinel (no sentinel value; `--timeout-ms` omitted just selects the 60 s default, CAPS:44); `wait_split` Sentinel (the 5 min cadence is a constant, not an input that can collide); `outcome_map` Maximum/Overflow (a status string has no capacity); `outward_default_off` Maximum and Sentinel (the guard is a boolean per action; no sentinel is defined); `contract_written` Typical and Maximum (covered by the two rows); `nesting_depth` Zero/Empty (CAPS:100 says a malformed value falls back to depth 1, and the spec need not restate it); `nesting_depth` Maximum (depth is a setting of the user, D5); `partition_count` Zero, Typical, Maximum, Sentinel (a fixed count, not an input); the AC-C5 additive-diff guard (S:176) is not tabled because the layout of the command files is not in the workspace (UNVERIFIED).

GAP entries are the priority targets for the next adversarial round. The GAP rows that become blocking are the ones named F1 and F2; the others are Medium findings above.

## Quality assessment (0-10)

| Dimension | Score | Basis |
|---|---|---|
| Clarity | 7 | Section 1 and the section 3 tables are precise; the Owner column mixes three actors (S:57). |
| Completeness | 7 | Strong on evidence and non-goals; the gaps are F4, F6, F8, F10. |
| Testability | 6 | Section 7 is concrete, but F1 and F2 make two checks unpassable and F13 lists three untested rules. |
| Consistency | 5 | F1, F2, F5, F7, F11, F12 are internal contradictions or divergences from the inventories. |

## Minor notes

- N1: E3 (S:23) says "It has worked before", while section 1.4 (1) (S:43) says the PR #329 run proves "the nested route, not the direct route" and INV-A:35 calls the same run "proven as a direct Orca-worker skill call". The two readings of `invocation_method: "skill-direct"` should be reconciled in one sentence; section 1.4 is the accurate one.
- N2: D1(a) (S:228) says the flag "cannot misfire on a person". A quoted topic that contains the text `--unattended` (for example `/sc:research "what does --unattended do"`) is not addressed; say the flag counts only as a standalone token outside quoted content.
- N3: Section 1.1 (S:16) says what changes in commands "is limited to" unattended mode, a report file and resume, while section 3.2 adds interface-drift fixes, a frontmatter move, a tool addition and the load usage line (S:102, S:108, S:112, S:124), and non-goal 8 (S:220) says only defects that stop a command working as a worker are in scope. The load usage line and the business-panel frontmatter do not stop a worker. Align the wording.
- N4: The new shared contract has no version field (S:62) although the existing workflow contract is versioned ("contract 1.1", INV-B:272). A version field costs one word and lets the coordinator reject a contract it does not understand.
- N5: The provenance claims at S:11 and S:285 (11 locations re-read; about 340 citations re-read by a validator, 9 defects fixed) cannot be checked from the inventories. They are accurate or not independently of this review; none of my findings depends on them.

## Follow-up candidates (Medium and minor; none triggers a revision)

Medium: F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, F13, F14. Minor: N1, N2, N3, N4, N5. Under the loop rules the coordinator asks the user once whether to open an issue for these; this run created none.

## Reviser brief

Blocking finding ids: F1, F2. Revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding, and report the byte size before and after, with the bytes added and deleted per finding id. Leave Medium and minor findings alone.

- F1: texts at S:195 (AC-1.1 "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"), S:159 (P1 "the `--unattended` flag accepted by every command in sections 3.1 and 3.2"), S:112 (load "Report (WC-4): none"), S:240 (D3(a) "no pr-submit changes in Phase 4"), S:154 ("Later phases do not start until the earlier phase's checks in section 7 pass"). Stated wrong outcome: a P1 build that gives pr-submit, load and every P2-P4 command a section and the flag before their gates are converted, so P1's check passes only if S:240 and S:112 are broken and `--unattended` is accepted by commands that still prompt or post.
- F2: texts at S:62 (WC-4 `<output-dir>/return-contract.yaml`, "known before dispatch"), S:83 (adversarial `<output>/adversarial/return-contract.yaml`), S:92 (workflow `.dev/tasks/to-do/<id>/return-contract.yaml`), S:182 (live check step 3 "report path is the WC-4 contract path"), S:198 (AC-1.4). Stated wrong outcome: adversarial's contract cannot be both `<dir>/return-contract.yaml` and `<dir>/adversarial/return-contract.yaml`, so step 3 cannot pass; workflow's path cannot be known before dispatch.

verdict: FAIL
