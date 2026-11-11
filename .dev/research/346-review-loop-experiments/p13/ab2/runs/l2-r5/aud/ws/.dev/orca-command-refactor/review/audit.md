review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (labelled whole-document audit, first review)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (286 lines)
- candidate sha256: `6df71d66ba77941856614e39ef7598d78d9d296b701f694093bc4d5e6d1b9394`
- baseline: none (first review of the full document; no `--re-review`, no `--baseline`)
- reviewer model actually used: claude-sonnet-5-5
- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- review date: 2026-11-10
- prompt followed: FIRST-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full before reviewing)
- format: standard critique layout. The Improve step was not run: a first review writes no revised specification and the command forbids modifying the specification without consent (`command.md` Boundaries).
- panel: Wiegers (lead), Adzic, Cockburn (requirements); Fowler (lead), Newman, Hohpe, Nygard (architecture); Whittaker (adversarial, always active); Crispin (guard-table completeness).

## Coverage

Covered: every section of the candidate (1 to 9, Decisions, UNVERIFIED list). I checked the candidate against the three inventories, which are the only evidence in the workspace:
- `INV-A` = `.dev/orca-command-refactor/inventory/commands-a.md` (120 lines)
- `INV-B` = `.dev/orca-command-refactor/inventory/commands-b.md` (323 lines)
- `CAPS` = `.dev/orca-command-refactor/inventory/orca-capabilities.md` (188 lines)

I re-read these cited lines and they support the claim they are cited for (exceptions are findings below):
- `INV-A:3,14,35-55,62,65,66,76-83,90-92,94-98,106,113,118,120`
- `INV-B:3,31-52,57-65,65,105,285-287,289-301,311,320,323`
- `CAPS:44-47,52,58-80,84-92,97-103,107-116,128-130,135-139,145-151,155-161,178-188`

Arithmetic check: 21 + 22 = 43 commands (`INV-A:3`, `INV-B:3`); 10 ready (5 + 5, `INV-A:44`, `INV-B:278-280`), 27 needing change (13 + 14), 6 coordinator-only (3 + 3). Section 3.1 has 10 rows, section 3.2 has 27 rows, section 4 has 6 rows (`spec:81-92, 97-125, 130-137`). Phase lists at `spec:159-162` cover 9 + 15 + 4 + 3 = 31 commands plus load, which accounts for the 10 + 27 = 37 non-coordinator commands once the P1 "fixes to ready commands" are counted. The partition is conserved.

UNVERIFIED (not checkable inside the workspace, so I did not rely on them to grade any finding):
- `spec:11`: the claim that 11 locations were re-read on 2026-11-02 and found as cited, including all `sk/` and `cmd/` locations it names.
- `spec:25` (E5): the grep results over `src/superclaude/` and the `0` count in `HOW-WE-WORK.md`.
- `spec:285` (item 14): the claim that about 340 citations were independently re-checked.
- Every citation to `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md`, `.dev/codegraph-migration/...`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `src/superclaude/cli/install_core.py`, and the `cmd/`, `sk/` and `ag/` files, except as the inventories quote them.

Not covered: no command was run; Orca behaviour was taken from `CAPS` only.

## Findings table (ids are the only ids this report uses)

| id | severity (label) | grade | one line |
|---|---|---|---|
| F-1 | MAJOR | blocking | WC-4's single contract location contradicts the per-command rows (tdd, init-lite, adversarial, workflow) |
| F-2 | MAJOR | blocking | P0 acceptance check AC-0.4 cannot pass as written and gates every later phase |
| M-1 | MAJOR | Medium | P1 makes `--unattended` accepted everywhere before the P2/P4 gate conversions exist |
| M-2 | MAJOR | Medium | WC-6 "fresh dir" versus a coordinator-passed output directory (retry clobbers the first attempt) |
| M-3 | MAJOR | Medium | WC-10 splits at 5 minutes; section 3 and AC-4.3 require 4 |
| M-4 | MAJOR | Medium | AC-C1 grep forbids Orca text that P0's own deliverables and SA-2 allow |
| M-5 | MAJOR | Medium | Section 4 says workers make no commits or pushes; WC-9, D4 and three rows allow them |
| M-6 | MAJOR | Medium | pr-submit "Will Not: run headless" is never reconciled with the D3(b) worker option |
| M-7 | MAJOR | Medium | tasklist Stage 10.5 row departs from the inventory without a Decisions entry; HALT and nesting left open |
| M-8 | MAJOR | Medium | `--unattended` input classes the spec never states (section-4 command, `--interactive`, no output directory, quoted token) |
| M-9 | MINOR (label) | Medium | WC-1 has no number, no owner deliverable and no phase |
| M-10 | MAJOR | Medium | WC-4's fixed status set versus "keep their fields" for existing contracts |
| M-11 | MINOR (label) | Medium | AC-C5 (no deleted lines) versus adding a flag to an existing Usage line |
| M-12 | MINOR (label) | Medium | "Phases 1-3 need no user decision" versus D1 and D4 |
| N-1 | MINOR | note | Undefined references `B-1` and "ladder rung 2" |
| N-2 | MINOR | note | Section 3.1 says only small fixes; P1 gives every ready command a flag and a section |
| N-3 | MINOR | note | research row pins `--strategy planning` even if the caller names another |
| N-4 | MINOR | note | WC-3 has no cap on repeated `ask` timeouts |
| N-5 | MINOR | note | reflect is called ready although UC-2 writes a tracked file and moves a folder by default |

## === REQUIREMENTS ANALYSIS ===

### F-1 (MAJOR, blocking, High priority). WC-4 contract location contradicts four section-3 rows
- Experts: Wiegers (traceability, consistency), Adzic (no example works for these four commands).
- Location: `spec:62` (WC-4), `spec:73` (section 2.3), `spec:83` (adversarial), `spec:87` and `spec:90` (init-lite, tdd), `spec:92` (workflow), `spec:85-86` (cleanup-audit, index-repo), `spec:200` (AC-2.2).
- Text that conflicts:
  - WC-4 requires the file at `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed with `--output` / `--output-dir`, "known before dispatch" (`spec:62`); section 2.3 makes the brief state "the output directory" (`spec:73`); step 3 of the live check requires the `worker_done` report path to be "the WC-4 contract path" (`spec:182`).
  - tdd and init-lite take a file: "`--output <file>`" (`spec:87`, `spec:90`), and AC-2.2 runs `/sc:tdd "auth" --unattended --output <file>` and expects a contract with `status: blocked` (`spec:200`).
  - adversarial's fix is `<output>/adversarial/return-contract.yaml` (`spec:83`), one directory below WC-4's path; the on-disk evidence is `adversarial/adversarial/return-contract.yaml` (`INV-A:60`).
  - workflow's contract lives in `.dev/tasks/to-do/<id>/` (`spec:92`); the brief passes only `--handoff none`, no output directory, and the package id is generated at run time and never reused (`INV-B:272-273`). The row also asks for a contract on "pre-creation STOPs" (`spec:92`), when no `<id>` directory exists yet.
- Grading sentence: an implementer who follows the stated text as written builds, for `/sc:tdd`, a contract at `<file>/return-contract.yaml` (a path below a file), and for adversarial and workflow a contract at a different path from the one the brief and live check 7.2 step 3 expect; that is wrong because WC-4 requires the path to be known to the coordinator before dispatch and equal to `<output-dir>/return-contract.yaml`, and no stated text lets the coordinator derive `<id>` or the adversarial subdirectory in advance. The acceptance checks AC-2.2 and 7.2 step 3 cannot pass for these four commands as written.
- Recommendation: state one location rule that holds for every command (for example a directory-valued flag distinct from the file-valued `--output`, with the contract always directly inside it), or list each exception with how the coordinator learns the path before dispatch. Delete the adversarial subdirectory path or move WC-4's path to match it; say where workflow writes its pre-creation STOP contract. Narrow, do not add a new mechanism.
- Quality impact: Consistency +2, Testability +1.

### F-2 (MAJOR, blocking, High priority). AC-0.4 cannot pass as written and gates every later phase
- Experts: Crispin (acceptance criteria), Whittaker (sequence attack), Wiegers.
- Location: `spec:194` (AC-0.4), `spec:182` (7.2 step 3), `spec:73` (2.3), `spec:158-159` (P0, P1), `spec:154` (phase gate).
- Text that conflicts:
  - AC-0.4 says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file" (`spec:194`). Step 3 requires "its report path is the WC-4 contract path" (`spec:182`).
  - In P0 no WC-4 contract exists: the contract arrives in P1 (`spec:159`, and AC-0.4 itself says "the contract arrives in P1"). The three P0 commands report `REPORT.md` for troubleshoot (`spec:91`), a contract at the workflow package path (`spec:92`) and an unnamed contract file for adversarial (`spec:83`), so none reports `<output-dir>/return-contract.yaml`.
  - Section 2.3 says the brief states the exact command line "including `--unattended`" (`spec:73`), and 7.2 step 1 builds the brief "per section 2.3" (`spec:180`); the flag is added in P1 (`spec:159`). AC-0.4 lists the three command lines without it (`spec:194`).
  - "Later phases do not start until the earlier phase's checks in section 7 pass" (`spec:154`), and "a failure here reopens section 1" (`spec:194`).
- Grading sentence: an implementer who follows the stated text as written runs the three smoke commands and finds step 3 fails for troubleshoot and adversarial (and the brief template cannot include a flag that does not exist), and that is wrong because AC-0.4 declares the check passable while its own step 3 cannot hold before P1; under `spec:154` P1 can then never start, and under `spec:194` a false failure reopens the core decision in section 1.
- Recommendation: in AC-0.4 replace step 3's pass condition with "the report path is the command's existing report file", and state that the P0 brief omits `--unattended`.
- Quality impact: Testability +2.

### M-1 (Medium). P1 accepts `--unattended` everywhere before the gate conversions exist
- Expert: Cockburn (goal and actor), Nygard (failure on transition).
- Location: `spec:159` (P1: flag "accepted by every command in sections 3.1 and 3.2 except `/sc:load` ... a no-op where a command has no gate"), `spec:195` (AC-1.1), `spec:160` and `spec:162` (P2 and P4 do the conversions), `spec:67` (WC-9), `spec:100`, `spec:113-114` (auggie-review, post-release, pr-submit).
- Issue: after P1, `/sc:auggie-review <PR> --unattended` is accepted, yet posting stays on until P2 (`spec:100`, `spec:160`), and pr-submit, post-release and implement prompts stay until P4. The phase text says nothing about what the flag does for a gated command in the interim.
- Why Medium: the harm needs the guess that a coordinator dispatches such a command between phases.
- Recommendation: P1 accepts the flag only on commands with no gate, or the flag on a gated command is refused until its phase lands. Priority: Medium. Quality impact: Consistency +1.

### M-2 (Medium). WC-6 "fresh dir" versus a coordinator-passed output directory
- Experts: Wiegers, Nygard.
- Location: `spec:64` (WC-6), `spec:62` (WC-4), `spec:99-125` ("fresh dir" in about 20 rows), `spec:73`, `spec:205` (AC-3.2).
- Issue: WC-6 says a command without a resume flag "writes each run into a fresh output directory", but WC-4 and 2.3 have the coordinator choose the directory before dispatch. A `--retry-of` worker given the same brief writes into the same directory and either overwrites or finds the first attempt's `return-contract.yaml`. That is the corruption WC-6 forbids, and a stale `succeeded` contract would satisfy WC-5's "report exists" test for a retry that crashed before writing. AC-3.2 (`spec:205`) literally starts "fresh" in a directory that already holds `.session-memory.md`.
- Why Medium: it needs the guess that the coordinator reuses the directory; the text does not say who makes the directory fresh.
- Recommendation: say in 2.3 that the coordinator passes a new directory per attempt, and that WC-6's "fresh dir" means the coordinator's choice. Priority: High among Medium. Quality impact: Consistency +1.

### M-3 (Medium). WC-10 splits at 5 minutes; 3.2 and AC-4.3 require 4
- Experts: Crispin, Whittaker (divergence attack).
- Location: `spec:68` (WC-10: splits calls "longer than 5 minutes" into waits "of at most 4 minutes"), `spec:114` ("each single iteration ... stays under 4 minutes"), `spec:210` (AC-4.3: "no single tool call exceeds 240 s"), `spec:266` (Decisions).
- Issue: a 270-second wait satisfies WC-10 (it is not longer than 5 minutes) and fails AC-4.3 and the pr-submit row.
- Recommendation: make the rule one number (waits at most 4 minutes) in WC-10. Priority: Medium. Quality impact: Testability +1.

### M-8 (Medium). `--unattended` input classes the spec never states
- Experts: Whittaker (zero/empty and sentinel attacks), Wiegers.
- Location: `spec:51` (term definition), `spec:128` (section 4: "get no `--unattended` mode"), `spec:83-84, 89` ("never `--interactive`" only as a brief instruction), `spec:62` (WC-4), `spec:90` (tdd "precise component prompt").
- Issue: the text does not say what happens when (a) `--unattended` is passed to one of the six section-4 commands, (b) `--unattended` is combined with `--interactive` on a command whose row does not refuse it (adversarial, brainstorm, release-split), (c) `--unattended` is passed with no output directory, so WC-4's file has no location, (d) the word appears inside a quoted topic or specification text. Compare guard rows G1 and G2 below.
- Why Medium: each is a missing restriction the document never states, not stated text that causes harm.
- Recommendation: one sentence per class (refuse with a message, or ignore), in the contract file. Priority: Medium. Quality impact: Completeness +1.

### M-9 (Medium). WC-1 has no number, no deliverable and no phase
- Experts: Wiegers, Nygard.
- Location: `spec:59` (WC-1), `spec:158-162` (no phase lists it), `spec:178-186` (live check only observes `state: ready`).
- Issue: the requirement says the fallback must come "well inside" the 60-second limit; its own evidence says 30 seconds passes and about 45 fails (`spec:59`). No number is stated, its owner is "launch setup, not commands" and no phase delivers or checks that setup beyond a generic ready result.
- Recommendation: state the number from the evidence and name the phase that checks it. Priority: Low-Medium.

### M-10 (Medium). Fixed status set versus "keep their fields"
- Experts: Wiegers, Adzic.
- Location: `spec:62` (WC-4: "Commands that already write a contract keep their fields and add the missing ones"; status "one of" four values), `spec:183` (check asserts the four values), `spec:262` (Decisions).
- Issue: neither inventory shows what `status` values existing contracts use (`INV-B:272` lists `status`, `plan_path`, `reflect_report_path` for workflow only); if any existing value differs, "keep their fields" and the check at `spec:183` disagree. UNVERIFIED in this workspace.
- Recommendation: list the existing values, or state that the four-value field is added beside them. Priority: Medium.

### M-12 (Medium). "Phases 1-3 need no user decision" versus D1 and D4
- Experts: Cockburn, Wiegers.
- Location: `spec:154`, `spec:225`, `spec:228-230` (D1), `spec:244-247` (D4: "affects ... auggie-review `--post-pr`, task `commit`/`push`", both P2 commands, `spec:160`).
- Issue: P0-P3 are said to proceed on recommendations, but D4 option (b) "Never" would change WC-9 and two P2 rows, and D1 option (b) would change every command's section. The statement is true only if the recommendations are accepted.
- Recommendation: say "proceed on the recommendations; a different answer reopens the named rows". Priority: Low.

### N-1 to N-4 (MINOR notes)
- N-1: `B-1` is cited at `spec:159`, `spec:195`, `spec:196` and defined nowhere; "ladder rung 2" at `spec:261` is also undefined.
- N-2: `spec:79` says the only command changes for the 10 ready commands are the small fixes, but P1 gives every ready command the flag (`spec:159`) and AC-1.1 requires a section for each (`spec:195`), including brainstorm and init-lite whose fix is "None" (`spec:84, 87`).
- N-3: the research row pins `--strategy planning` under `--unattended` (`spec:116`); `INV-B:135` offers "pin in the brief, or route the questions through ask", and the row does not say what happens when the caller passes `--strategy intent`.
- N-4: WC-3 lets the worker resume the same message ID after an `ask` timeout (`spec:61`) with no limit on repeats; `CAPS:58-61` give none either.

## === ARCHITECTURE ANALYSIS ===

### M-4 (Medium). AC-C1 forbids Orca text that P0 and SA-2 allow
- Experts: Fowler (boundaries), Newman (evolution), Crispin.
- Location: `spec:172` (AC-C1 greps `src/superclaude/{commands,skills,agents,core}`, excluding only `skills/ccsession-tag/`), `spec:147` (SA-2 allows an Orca mention "inside the contract file"), `spec:158` (P0 adds `WORKER-CONTRACT.md` with a brief template and an Orca section in `HOW-WE-WORK.md`, both under `core`), `spec:25` (E5).
- Issue: the contract file and the routing-guide section are in `core/`, which AC-C1 greps. Text such as `orca orchestration ask` there matches the pattern, so a P0 deliverable that SA-2 permits fails the check that every phase must pass. The regex can only be judged from the text; whether the P0 text contains a match is a guess.
- Recommendation: exclude the two core files from AC-C1, or drop the SA-2 permission. Priority: Medium.

### M-5 (Medium). Section 4 says workers make no commits or pushes
- Experts: Fowler, Nygard.
- Location: `spec:133` (`/sc:git` row: "workers make no commits or pushes"), `spec:67` (WC-9), `spec:121` (task commit/push when authorized), `spec:113` (post-release commit and PR), `spec:245` (D4(a)).
- Issue: the git row states a rule that WC-9 and D4(a) allow brief authorization to override, so the stated reason for keeping git coordinator-only overstates the design.
- Recommendation: change the row to "workers make no commits or pushes unless WC-9 authorizes them". Priority: Low-Medium.

### M-6 (Medium). pr-submit "Will Not: run headless" never reconciled
- Experts: Newman (service boundary), Nygard.
- Location: `spec:114`, `spec:241` (D3(b)), `spec:210` (AC-4.3); `INV-B:90` quotes "Will Not: run headless / imply a daemon" (`cmd/pr-submit.md:85`, `SKILL.md:225`).
- Issue: D3(b) and the P4 row ask pr-submit to run unattended under a worker, but the command's own boundary says it will not run headless. The inventory marks this; the spec does not mention it. P4 and D3(b) are gated by a user decision and the recommendation is (a), so no wrong outcome is forced.
- Recommendation: if D3(b) stays, add one line saying how the Will-Not line changes. Priority: Medium.

### M-7 (Medium). tasklist Stage 10.5 departs from the inventory with no Decisions entry
- Experts: Fowler (nesting and data flow), Whittaker.
- Location: `spec:122` (tasklist row), `spec:88` (reflect row), `spec:151` (SA-6); `INV-B:209, 215, 295` (the inventory says drop `--remediate`), `INV-B:209` (`needs_human_decision` items HALT, `SKILL.md:1631`), `INV-B:210`, `INV-A:14` (nesting depth).
- Issue: the spec keeps `--remediate` in Stage 10.5 and passes `--unattended` so reflect's headless auto-accept applies, and claims the reflect fan-out runs "one layer below the worker, inside Claude Code's nesting limit". Three things are left open: the departure from the inventory's "drop `--remediate`" is not recorded in the Decisions table (`spec:258-269`); the `needs_human_decision` HALT is a person-blocking step with no WC-2 resolution; and an auto-accepted remediation hands off to workflow or task-builder, which fan out further, so "one layer" is not shown for that chain.
- Why Medium: each needs a guess about what the headless rule and the hand-off do.
- Recommendation: either follow the inventory (call reflect without `--remediate`) or add the missing resolution and the nesting count. Priority: Medium.

### M-11 (Medium). AC-C5 versus adding a flag to a Usage line
- Experts: Fowler, Newman.
- Location: `spec:149` (SA-4: additive edits, existing lines change only for named defect fixes), `spec:176` (AC-C5 prints nothing for any `-` line), `spec:111-112` (load usage line is a named fix).
- Issue: adding `--unattended` or an output flag to an existing Usage or `argument-hint` line changes that line and trips AC-C5 unless the flag goes on a new line. The text does not say which.
- Recommendation: state that new flags are documented in the new section only. Priority: Low.

### N-5 (MINOR note). reflect is "ready" although UC-2 has default writes
- Location: `spec:88`; `INV-B:114` (UC-2 moves the validated work-unit folder by default and writes the tracked file `docs/memory/reflect/deviation-patterns-<slug>.md`). The row mentions only `--no-promote`; step 6 of the live check (`spec:185`) tolerates "documented artifacts", so no check fails.

## === ADVERSARIAL ANALYSIS (Whittaker) ===

- I can break this specification by **Sequence Attack**. The invariant at **`spec:154` plus `spec:194`** fails when **P0's AC-0.4 is run in order**. Concrete attack: before state: no contract exists, no `--unattended` flag exists; step 3 asks for the WC-4 path; troubleshoot returns `REPORT.md`; after state: step 3 fails, P1 may not start, and section 1 is "reopened". See F-2.
- I can break this specification by **Divergence Attack**. The invariant at **`spec:68` (WC-10)** fails when **a single wait is 270 s**. Concrete attack: before state: poll iteration 270 s; WC-10 branch ">5 minutes" is false, so no split; AC-4.3 branch "exceeds 240 s" is true; after state: both texts apply, with opposite results. See M-3.
- I can break this specification by **Zero/Empty Attack**. The invariant at **`spec:62` (WC-4)** fails when **`--unattended` is given with no output directory**. Concrete attack: before state: `/sc:analyze src --unattended`; WC-4 needs `<output-dir>`; after state: no path for `return-contract.yaml`, the worker cannot pass `--report-path`, and WC-5 sends `failed` with no report. See M-8.
- I can break this specification by **Sentinel Collision Attack**. The invariant at **`spec:62` (WC-4 status set)** fails when **an existing contract uses a status outside the four values**. Concrete attack: before state: workflow's contract carries its own `status`; the check at `spec:183` asserts membership of the four values; after state: the check fails on a correct existing contract. See M-10 (existing values UNVERIFIED).
- I can break this specification by **Accumulation Attack**. The invariant at **`spec:64` (WC-6)** fails when **a retry reuses the first attempt's directory**. Concrete attack: before state: attempt 1 wrote `return-contract.yaml` with `status: succeeded` then the worker died before sending `worker_done`; after state: attempt 2 crashes early, the stale file satisfies "report exists", and WC-5 reports `succeeded`. See M-2.

## Guard Condition Boundary Table

Guards were identified (conditional logic, thresholds, boolean switches). The table is complete: every guard has the rows that apply, and the omitted classes are listed with their reason below it.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 `--unattended` token | `spec:51`, `spec:60` (WC-2) | Zero/Empty | flag absent | false | today's behaviour (SA-1, `spec:146`) | OK |
| G1 `--unattended` token | `spec:60` | Typical | flag on a section-3 command | true | gate resolves per row; contract written | OK |
| G1 `--unattended` token | `spec:128` | Sentinel Value Match | flag on a section-4 command | true | unspecified (section 4 says only "no `--unattended` mode") | GAP (M-8, Medium) |
| G1 `--unattended` token | `spec:83-84, 89` | Legitimate Edge Case | flag together with `--interactive` | true | refused only for cleanup, improve, roadmap, explain, test; unspecified for adversarial, brainstorm, release-split | GAP (M-8, Medium) |
| G1 `--unattended` token | `spec:90` | Legitimate Edge Case | the word inside a quoted topic | ambiguous | unspecified | GAP (M-8, Medium) |
| G2 output directory | `spec:62` (WC-4) | Zero/Empty | no `--output` / output-dir | no path | unspecified | GAP (M-8, Medium) |
| G2 output directory | `spec:62` | Typical | `--output <dir>` | true | `<dir>/return-contract.yaml` | OK |
| G2 output directory | `spec:87, 90, 200` | Legitimate Edge Case | `--output <file>` (tdd, init-lite) | file, not directory | contradicts WC-4 | GAP (F-1, blocking) |
| G2 output directory | `spec:83, 92` | Legitimate Edge Case | fixed subdirectory or generated `<id>` | path not known before dispatch | contradicts WC-4 and 7.2 step 3 | GAP (F-1, blocking) |
| G2 output directory | `spec:64` | Maximum/Overflow | retry reuses the directory | true | "fresh dir" with no owner | GAP (M-2, Medium) |
| G3 wait split | `spec:68` (WC-10) | Typical | wait of 2 minutes | no split | none needed | OK |
| G3 wait split | `spec:68`, `spec:210` | Legitimate Edge Case | wait of 270 s (between 4 and 5 minutes) | WC-10 false, AC-4.3 true | two texts differ | GAP (M-3, Medium) |
| G3 wait split | `spec:68` | Maximum/Overflow | wait longer than 5 minutes | true | split into waits of at most 4 minutes | OK |
| G4 outcome map | `spec:63` (WC-5) | Zero/Empty | no report file | true | `--outcome failed` | OK |
| G4 outcome map | `spec:63` | Typical | status `succeeded` | true | `--outcome succeeded` | OK |
| G4 outcome map | `spec:63, 263` | Sentinel Value Match | status `partial` | true | `succeeded`, body says `partial` | OK |
| G4 outcome map | `spec:63` | Legitimate Edge Case | report present but unparseable or stale | unknown | unspecified | GAP (stale case: M-2, Medium; unparseable case: minor note, no id) |
| G5 outward default off | `spec:67` (WC-9) | Typical | no authorizing flag | true | action off | OK |
| G5 outward default off | `spec:67, 245` | Legitimate Edge Case | flag present, no user quote in brief | true | WC-9 says on; D4(a) says quote needed; D4 open | GAP (M-12, Medium) |
| G6 task confidence | `spec:121` | Zero/Empty | confidence 0 | below 0.70 | blocked | OK |
| G6 task confidence | `spec:121` | Legitimate Edge Case | exactly 0.70 | false ("below 0.70") | proceeds (`INV-B:199`: "< 0.70") | OK |
| G7 nesting depth | `spec:33`, `spec:66` | Typical | depth 1 | true | no Orca fan-out from a command | OK |
| G7 nesting depth | `spec:252` | Maximum/Overflow | depth raised (D5 b) | true | WC-8 still forbids | OK |
| G8 phase gate | `spec:154`, `spec:194` | Legitimate Edge Case | AC-0.4 run as written | step 3 fails | blocks P1 | GAP (F-2, blocking) |
| G8 phase gate | `spec:154`, `spec:162` | Zero/Empty | no answer to D2-D4 | true | P4 does not start | OK |
| G9 readiness limit | `spec:59` (WC-1) | Maximum/Overflow | fallback of 45 s or more | fails readiness (`EVIDENCE.md:45,56` as quoted) | "well inside the limit" with no number | GAP (M-9, Medium) |
| G10 ask resume | `spec:61` (WC-3) | Maximum/Overflow | repeated timeouts | true | resume same ID; no cap | GAP (N-4, minor) |

Classes left out, one line each:
- G1: One/Minimal and Maximum/Overflow cannot occur for a present-or-absent flag.
- G2: One/Minimal: a directory is either given or not; Sentinel: no reserved value.
- G3: Zero/Empty is a wait of 0, which is not a wait; One/Minimal and Sentinel have no distinct behaviour.
- G4: One/Minimal and Maximum/Overflow: the status is one value from a set.
- G5: Zero/Empty is the typical case (no flag); Maximum and Sentinel do not apply to a boolean.
- G6: One/Minimal, Maximum and Sentinel are covered by the 0 and 0.70 rows (above 0.70 proceeds unchanged).
- G7: Zero/Empty: depth below 1 falls back to 1 (`CAPS:100`); One/Minimal is the typical row.
- G8: One/Minimal and Sentinel do not apply to a gate on a check result.
- G9: Zero/Empty and One/Minimal: no prompt is the typical case; Sentinel does not apply.
- G10: Zero/Empty: no timeout means no resume; Sentinel does not apply.

Completion criteria: no blank "Specified Behavior" cell remains except the entries marked "unspecified", each of which is a GAP finding with a grade above (FR-9). Three GAP rows map to blocking findings (F-1, F-2); the others are Medium because each names a missing requirement or needs a guess (FR-8). The table is complete, so synthesis is not blocked (FR-10). Downstream: GAP entries are priority probes for `sc:adversarial` AD-1 if the loop continues.

## Pipeline Dimensional Analysis

Not triggered. The specification describes a coordinator-to-worker process, not a data pipeline with counts that diverge between stages. The only count flow is the 43-command partition (21 + 22 = 10 + 27 + 6), conserved as shown in Coverage.

## Quality assessment (0-10)

Clarity 7, Completeness 7, Testability 6, Consistency 6. Overall 6.5. The design decision (section 1) and the inventory traceability are strong; the blocking defects are in the contract's location rule and in the first acceptance check.

## Expert consensus and disagreements

- Consensus: keep the decision "Orca coordinates, commands stay units of work"; the evidence and the stated gaps in section 1.4 are honest, and `CAPS` supports R1-R5.
- Wiegers and Crispin: the requirement set is traceable to inventory lines; WC-4 and AC-0.4 are the two places where the stated text cannot be satisfied.
- Fowler and Newman: the architecture is sound; the fixes needed are boundary statements (M-4, M-5, M-7), not new mechanisms.
- Disagreement: Nygard would grade M-1 and M-2 as blocking (interim-state hazards); under the grading rule they need a guess about coordinator behaviour, so they stay Medium.

## Follow-up candidates (Medium and minor; never trigger a revision)

M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, M-10, M-11, M-12, N-1, N-2, N-3, N-4, N-5.

Issue offer: the review session could not ask the user whether to open an issue for these (no user channel in this run). No issue was created. The coordinator should ask once for this loop.

Brief clauses overridden: none. The brief did not widen scope or regrade any finding.

## Reviser brief

Blocking finding ids: F-1, F-2.

Rules for the reviser (restating the Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size of the candidate before and after, and the bytes added and deleted per finding id; leave Medium and minor findings alone; return the candidate once and do not award yourself a PASS.

verdict: FAIL
