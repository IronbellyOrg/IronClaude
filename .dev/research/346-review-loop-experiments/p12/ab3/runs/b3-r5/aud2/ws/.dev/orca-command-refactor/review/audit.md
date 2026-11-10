review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (labelled whole-document audit, first review; FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` read in full and followed)
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `7dee641ad4c0ea491b648c4d2ff91374c68f0b6c2b89647e79c56e099f02c9e8`
- Baseline / prior report: none given; neither `--re-review` nor `--baseline` was passed, so this is a first review of the full document (no baseline sha256 exists).
- Reviewer model actually used: Sonnet 5.5 (`claude-sonnet-5-5`)
- Shared context read first: `.dev/orca-command-refactor/README.md` (binding).
- Evidence I could check: `inventory/commands-a.md` (`INV-A`), `inventory/commands-b.md` (`INV-B`), `inventory/orca-capabilities.md` (`CAPS`), `README.md`. Every other citation (`src/...`, `CLAUDE.md`, `EVIDENCE.md`, `.dev/codegraph-migration/...`, `Makefile`, `pyproject.toml`, `cli-error.js`, Orca guides) is not in the workspace and is **UNVERIFIED** here; I took none of them as confirmed. Spec's own claim of having re-read 11 locations and run 340 citation checks (spec:11, spec:285) is likewise UNVERIFIED.
- Panel (critique mode, focus requirements + architecture, plus Whittaker, active on every panel): Wiegers, Adzic, Cockburn (requirements); Fowler, Newman, Hohpe, Nygard (architecture); Crispin (table completeness); Whittaker (adversarial).

## Coverage

Whole document read once: sections 1 to 9, Decisions, UNVERIFIED list. Cross-checked: the 43-command split (10 + 27 + 6) against the two inventories (consistent: INV-A:73 gives 5/13/3, INV-B gives 5/14/3); every section-3 row against the phase table in section 6; WC-1 to WC-12 against each other and against sections 5 and 7; every `INV-*`/`CAPS:*` line number I could open (about 45 spot checks; all matched except the one noted in M-8). Not covered: the contents of any command or skill file (not in the workspace), Orca behaviour, wording quality of the prose.

Not triggered: Pipeline Dimensional Analysis (the document has no multi-stage data flow whose item count diverges; coordinator to worker to report is one stage per Task, so no Quantity Flow Diagram is produced). State Variable Registry is a `--focus correctness` artifact and that focus was not requested.

## Guard Condition Boundary Table

Guards found: the WC-10 wait split, the WC-5 outcome mapping, the WC-1 readiness fallback, the task confidence threshold, the pr-submit `--monitor` ordinal, the WC-6 retry choice. Classes left out: "One/Minimal" is left out of every row unless shown (a single value cannot differ from "Typical" for these guards); "Sentinel Value Match" is left out for WC-10, the confidence threshold, WC-1 and WC-6 (no sentinel value is defined for them).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| wait-split (WC-10) | spec:68 | Zero/Empty | wait of 0 s | holds (at most 4 min) | no wait, nothing to split | OK |
| wait-split (WC-10) | spec:68, spec:114 | Typical | 600 s budget as poll-then-sleep iterations | holds per iteration | heartbeat between iterations | OK |
| wait-split (WC-10) | spec:68, spec:114, spec:283 | Maximum/Overflow | one iteration above 240 s (poll runtime unknown, or `--poll-interval` set above 240 s) | fails | spec only says "confirm each iteration stays under 4 minutes"; poll runtime UNVERIFIED; no cap on a person-supplied interval | GAP (Medium, M-6) |
| outcome-map (WC-5) | spec:63 | Zero/Empty | no report file | `failed` | `--outcome failed` | OK |
| outcome-map (WC-5) | spec:63 | Typical | `status: succeeded` | `succeeded` | `--outcome succeeded` | OK |
| outcome-map (WC-5) | spec:63, spec:263 | Legitimate Edge Case | `partial`, or an audit whose verdict is FAIL | `succeeded` | stated; first body sentence carries the status; "partial" itself is never defined | OK (definition gap noted in M-5) |
| outcome-map (WC-5) | spec:62, spec:63 | Sentinel Value Match | contract exists but `status` is outside the four values, or the YAML is unreadable | neither | unspecified (WC-5 covers only "no report exists") | GAP (Medium, M-5) |
| readiness fallback (WC-1) | spec:59 | Typical | 30 s fallback | within 60 s | passes (cited `EVIDENCE.md:45`, UNVERIFIED) | OK |
| readiness fallback (WC-1) | spec:59 | Maximum/Overflow | fallback of 50 s | unclear | the text says "well inside" 60 s with no number, while its own evidence says about 45 s fails again | GAP (Medium, M-7) |
| confidence gate (task) | spec:121 | Zero/Empty | confidence 0 | below 0.70 | blocked | OK |
| confidence gate (task) | spec:121 | Legitimate Edge Case | exactly 0.70 | not below 0.70 | not blocked ("below 0.70" is the stated rule; INV-B:199 gives `< 0.70` as the only prompt) | OK |
| monitor ordinal (pr-submit) | spec:114 | Zero/Empty | `--monitor 0` | n/a | silent; INV-B:89 only says `--monitor 1` has the y/n gate and 3 has none; 0 and 2 not described | GAP (Medium, UNVERIFIED which ordinals gate) |
| retry choice (WC-6) | spec:64, spec:62, spec:73 | Typical | `--retry-of` re-dispatch with the same brief | "fresh output directory" | who chooses the new directory is not stated | GAP (Medium, M-1) |

No row meets the blocking test of FR-8/FR-9 (each GAP needs the implementer to pick between two readings), so all are Medium and none stops synthesis.

## === REQUIREMENTS ANALYSIS ===

### B-1 | CRITICAL (blocking) | Wiegers, Nygard, Whittaker (Accumulation Attack) | priority High | quality impact: Consistency -2, Testability -1

**Issue.** WC-4 fixes the contract file name `return-contract.yaml` and places it, for a file-valued `--output`, "in the parent directory of the file" (spec:62). Rows for init-lite (spec:87), tdd (spec:90) and spec-panel (spec:120) use exactly that rule, and the workflow pre-creation fallback is the single shared path `.dev/tasks/to-do/return-contract.yaml` (spec:92). WC-11 says "Two workers in one worktree must never write the same file" (spec:69), and the Orca model the spec adopts is parallel workers in one worktree by default (`CAPS:115`; spec:69). Section 2.3 tells the coordinator only to supply "the output flag value" and compute the contract path from it (spec:73); it says nothing about separate directories.

**Grading sentence.** An implementer who follows the stated text as written builds init-lite, tdd and spec-panel workers that each write `<parent of --output>/return-contract.yaml`, so two parallel workers given `--output docs/tdd/a.md` and `--output docs/tdd/b.md` both write `docs/tdd/return-contract.yaml`; the later write replaces the earlier, and the earlier worker's `worker_done --report-path` then points at the other worker's status. That is wrong because WC-4 (one report per worker, "written on every outcome") and WC-11 (no shared file) contradict each other on this path, and the wrong file can turn a `blocked` or `failed` worker into a reported `succeeded` (WC-5 maps from the contract). Two stated texts contradict; no further assumption needed.

**Attack trace (Whittaker).** Before: no contract. Worker A (tdd, blocked, status `blocked`) writes the file at t1. Worker B (tdd, succeeded) writes at t2. After: file says `succeeded`; A's `worker_done --outcome failed` (WC-5) now disagrees with the file the coordinator opens from A's `--report-path`.

**Recommendation (narrow, no new mechanism).** Make the contract path a function of the output the brief already names, for example the file-valued `--output` gets `<output-stem>.return-contract.yaml`, or WC-4 requires the brief to give every worker its own output directory. Apply to the four rows above and to the workflow fallback. Prefer deleting the parent-directory rule over adding a rule.

### B-2 | MAJOR (blocking) | Wiegers, Cockburn | priority High | quality impact: Completeness -1, Testability -1

**Issue.** Section 3.1 says the ten ready commands report "the named file until Phase 1 adds the contract" (spec:79), and the init-lite row names a contract "in the parent directory of that file" (spec:87). The phase table gives P1 only nine commands plus "fixes to adversarial, cleanup-audit, index-repo, workflow" (spec:159), P2 fifteen commands (spec:160), P3 four (spec:161) and P4 three (spec:162). Count: 13 + 15 + 4 + 3 = 35 of the 37 worker-capable commands. Brainstorm (spec:84, small fix "None") and init-lite (spec:87, small fix "None") appear in no phase's Commands column. Section 6 says each phase "adds the flag and the section for its own commands" (spec:159), AC-1.1 asserts the section only for P1 commands (spec:195), and section 2.3 requires the brief to include `--unattended` (spec:73).

**Grading sentence.** An implementer who follows section 6 as written completes P0 to P4 and delivers no `## Unattended mode` section, no `--unattended` flag handling and, for init-lite, no `return-contract.yaml` at all; this is wrong because section 3.1 and section 2.3 tell the coordinator to brief those two commands with `--unattended` and to open a contract at a computed path, and the spec's acceptance checks (AC-1.1, AC-1.2) never test either command, so every check passes while the stated contract does not exist. The 3.1 lead-in sentence and the section 6 table contradict.

**Recommendation.** Assign brainstorm and init-lite to a phase (P1 is the natural one: no gate), or state in the 3.1 rows that they need no change and the brief must not pass `--unattended` to them. Cite this finding id on whichever line is added.

## === ARCHITECTURE ANALYSIS ===

No blocking architecture finding. The central decision (Orca coordinates, commands stay units of work, section 1) is supported by the evidence I could open (`CAPS:97-101,103` for depth, `CAPS:147-150` for standalone behaviour, `CAPS:158-161` for subagents). Its stated gaps (section 1.4) are honest and Phase 0 tests them.

## Follow-up candidates (Medium and minor; none blocks, none enters the Reviser brief)

Medium (warnings):

- **M-1 | Whittaker (Sequence Attack), Nygard | WC-6 "fresh dir" vs WC-4 pre-computed path.** Spec:64 says a command with no resume flag "writes each run into a fresh output directory", while WC-4 and section 2.3 require a path the coordinator computes before dispatch (spec:62, spec:73), and 20 rows in 3.2 say "fresh dir". Two readings: the command picks a new directory (then the coordinator opens a stale or missing path), or the coordinator gives a new directory per retry (then 2.3 should say so). Needs a guess, so Medium. Recommendation: add to the 2.3 brief duties "a new output path per `--retry-of`" and delete "writes each run into a fresh directory" from WC-6.
- **M-2 | Fowler, Newman | no general propagation of `--unattended` to nested commands.** Only the tasklist row passes the mode down (spec:122). pr-submit runs a "`/sc:auggie-review` fallback" (INV-B:91) whose defaults post to GitHub and wait on a person (INV-A:38, spec:100), and task's TFEP calls `/sc:troubleshoot` (INV-B:201). WC-2 says "the command never calls AskUserQuestion" (spec:60) without covering what it invokes. Recommendation: one sentence in WC-2 for nested invocations.
- **M-3 | Nygard | pr-submit "Will Not: run headless / imply a daemon" is not addressed.** INV-B:90 records `cmd/pr-submit.md:85` and `SKILL.md:225` as an explicit refusal; the pr-submit row (spec:114) and D3(b) (spec:241) never mention it. Applies only if D3(b) is chosen.
- **M-4 | Wiegers | auggie-review: "posting returns only with an explicit `--post-pr`" (spec:100, spec:244).** INV-A:38 shows only `--no-post-pr` exists (posting is the default). Nothing marks `--post-pr` as a new flag; an implementer must invent it. Say it is new or reuse the existing default.
- **M-5 | Adzic, Whittaker (Sentinel Collision Attack) | WC-4 "keep their fields" vs a fixed `status` vocabulary (spec:62, spec:262).** Workflow's contract already has a `status` field (INV-B:272); its allowed values are not recorded anywhere I can open, so "keep their fields and add the missing ones" may require two different meanings for one key. Also `partial` is never defined and WC-5 (spec:63) is silent on an out-of-set or unreadable `status` (see table).
- **M-6 | Nygard | WC-10 for pr-submit** (see table row): the 4-minute cap rests on an unmeasured poll runtime (spec:283 item 12) and ignores a larger `--poll-interval`.
- **M-7 | Wiegers | WC-1 gives no number.** "Well inside the readiness limit" (spec:59) next to evidence that about 45 s already fails. Owner is launch setup, outside commands, so low urgency.
- **M-8 | Adzic | citation defects.** (a) E2 cites `CAPS:161` for "`[H:worker-start]` line 38, `--agent claude`" (spec:22), but `CAPS:161` is the pr-submit top-level line; the `--agent claude` text sits at `CAPS:49` and the `[H:worker-start]` quote is not at line 161. (b) WC-9 cites `README.md:31` for a general rule (spec:67); README:31 is a rule for this run's workers ("No git commits, pushes, PRs or GitHub comments"), not product policy. (c) E1 cites `CAPS:92` and `CAPS:86` correctly; the others I opened matched.
- **M-9 | Crispin, Newman | AC-C1 against the P0 deliverables.** AC-C1 greps `src/superclaude/core` and exempts only `ccsession-tag` (spec:172), while P0 adds `WORKER-CONTRACT.md` (which carries WC-3 and WC-5 text about `ask` and `worker_done`) and an Orca section in `HOW-WE-WORK.md` (spec:158). Whether those texts contain the grepped phrase `orca orchestration` is not stated, so P0 may or may not pass its own common check. E5 (spec:25) says HOW-WE-WORK currently has 0 mentions (UNVERIFIED).
- **M-10 | Crispin | AC-C5 vs new flags.** AC-C5 requires no deleted line in command edits without a named defect (spec:176); adding `--unattended` or `--output` to a one-line Usage entry (SA-4, spec:149) removes the old line in `git diff -U0`. Whether usage lines are touched is not stated. UNVERIFIED (command files not in workspace).
- **M-11 | Wiegers | spec-panel row against the actual command definition.** The spec says to "add `--output`" and put the contract beside it (spec:120). The `/sc:spec-panel` command file given to this review already has `--output <file>` (command.md:23), a required `--report-dir`, and a contract at `<report-dir>/return-contract.yaml` (command.md:460-461), and it cites a "WC-4" rule that "paths git ignores are left out" (command.md:461) that spec WC-4 (spec:62) does not contain. The spec and the command have drifted; the spec is the stale side.

Minor (notes):

- N-1. Workflow's contract path cannot be computed before dispatch (spec:92), against the WC-4 title (spec:62); the spec acknowledges this (B-01 in spec:62) and routes it through `worker_done --report-path`.
- N-2. cleanup-audit (fixed `.claude-audit/`) and index-repo (fixed `PROJECT_INDEX.md`) allow one run per worktree (spec:85, spec:86); section 2.3 does not tell the coordinator to serialise them.
- N-3. `INV-A:95` is cited for "nesting loses tools at Claude Code's depth limit" (spec:65); that line actually says nesting is allowed up to three layers and lists the depth limit as a risk. The claim is supported in `INV-A:14`.
- N-4. Quoted specification text that contains the token `--unattended` is not addressed in the spec (D1(a), spec:228); the command definition handles it (command.md:459).
- N-5. About 150 of the spec's citations point at files outside the workspace and could not be opened (UNVERIFIED, see header).

Open question to the user (asked once for this loop; this sandbox cannot ask, so nothing was created): open an issue for the Medium and minor follow-up candidates above? No issue was created.

## Reviser brief

Blocking finding ids: B-1, B-2. Reviser contract (bullet 6 of the command's Review Loop, restated because the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Leave all Medium (M-*) and minor (N-*) findings alone. Return the candidate once and do not award yourself a PASS. B-1 covers spec:62, spec:87, spec:90, spec:92, spec:120 and spec:73; B-2 covers spec:79, spec:84, spec:87 and spec:159-162.

verdict: FAIL
