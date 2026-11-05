# Refactoring Plan: Merge into Base (Variant 3)

Decision D1 (`.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:328-331`), /sc:adversarial Mode A, depth standard, Step 4. Drafted 2026-11-02T17:54Z by the debate orchestrator, resuming after the dev-environment restart at about 16:28Z. Steps 1-3 are used as written and not rescored.

Citation key: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `[G] N` = line N of `orca-ide skills get orchestration` (1.4.237); `Vn:N` = `variant-n-original.md`; `R1-Vn:N`, `R2-Vn:N` = `rounds/r1-variant-n.md`, `rounds/r2-variant-n.md`; `R2-Vn #k` = row k of that file's "Responses to criticisms" table; `DA:N` = `diff-analysis.md`; `BSel:N` = `base-selection.md`; `INV-NNN` = row of `invariant-probe.md`; `CORE-CLAUDE:N` = `src/superclaude/core/CLAUDE.md:N`; `WF:N` = `src/superclaude/skills/sc-workflow-protocol/SKILL.md:N`; `BS:N` = `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:N`; `CR01:N` = `.dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md:N`; `ROOT-CLAUDE:N` = the repository-root `CLAUDE.md:N`; `REVIEW` = `refactor-plan-review.md` (fresh-context review of this plan; its findings B1-B3 and M1-M14 are applied below and recorded under "Plan review").

## Overview
- Base: Variant 3, option (c): the `--unattended` flag is the only switch, plus a worker-session guard (`BSel:168-176`). Selected by the level-1 debate tiebreaker after a 0.036 score margin inside the 0.05 tie band (`BSel:160-161`).
- Incorporating strengths from: Variant 1, option (a) (`BSel:188-193`); Variant 2, option (b) (`BSel:195-198`); the Round 1 and Round 2 concessions and refinements (`BSel:200-209`); the five HIGH-severity UNADDRESSED invariants that block convergence (`debate-transcript.md:631-643`); and four user decisions made after the debate started, applied as fixed constraints, not debated.
- Fixed constraints (user decisions, not debate points):
  - K1. Every worktree is created by Orca at Orca's default path, never under `.dev/worktrees/` (`CR01:41`). This overrides `SPEC:235` for the 7.2 disposable worktree.
  - K2. SuperClaude upstream (`SuperClaude-Org/SuperClaude_Framework`) is never pushed to or interacted with (`CR01:45`; `ROOT-CLAUDE:41-66`).
  - K3. Merged PR #343 (commit `80f934de`): only blocking findings fail a review, minor findings are notes, and a review loop stops after 2 fix cycles (3 reviews) and escalates to the user (`git show 80f934de`, commit body: "at most 2 fix cycles (3 reviews), then escalate").
  - K4. Proposed change CR-01: one feature worktree, with child worktrees only when a trigger applies; every child gets setup before use (`CR01:14-24`).
- Planned changes: 24 (17 carried from `BSel:187-209`, 5 for the HIGH invariants, 1 bundle for the MEDIUM invariants, 1 for the fixed constraints).
- Risk level: Medium overall. Most changes are additive; changes 9, 18 and 20 rewrite the guard's trigger, key and timing, which are the parts the merged position rests on.

## Planned Changes

### Change 1: Outward defaults turn off only under the flag (from Variant 1)
- **Source**: Variant 1, Safety (V1:10)
- **Target**: Base, Safety (append)
- **Rationale**: U-002, C-002; scored equal (V1, V3) at 75% because V3 inherits the behaviour but only V1 argued it (`debate-transcript.md:586`; R2-V3 #10).
- **Integration point**: New Safety bullet: WC-9 (`SPEC:73`) applies only under `--unattended`, so a person working in an Orca tab keeps auggie-review's posting default (`SPEC:169`).
- **Risk**: Low. Additive; states inherited behaviour.

### Change 2: Phase gating stated explicitly (from Variant 1)
- **Source**: Variant 1, Reliability (V1:15)
- **Target**: Base, Reliability (append)
- **Rationale**: U-003, C-013 (equal (V1, V3), 92%, `debate-transcript.md:597`).
- **Integration point**: Reliability bullet: a command accepts the flag only once its gates are converted (`SPEC:187-195`); the `## Unattended mode` section marks that.
- **Risk**: Low. Additive.

### Change 3: Quoted-argument example and its live check (from Variant 1)
- **Source**: Variant 1, Safety (V1:8)
- **Target**: Base, Safety (insert into the first bullet)
- **Rationale**: U-001-adjacent; C-001 unanimous equal (V1, V3) at 97% (`debate-transcript.md:585`).
- **Integration point**: Name `/sc:troubleshoot "the worker ignores --unattended"` as a person's run, checked by AC-2.8 (`SPEC:55`, `SPEC:269`).
- **Risk**: Low. Additive.

### Change 4: Honest wording that the parse and the guard are applied by a model (from Variant 1)
- **Source**: Variant 1, Implementation cost (V1:22)
- **Target**: Base, Reliability first bullet (replace "Deterministic")
- **Rationale**: X-003, unanimous equal at 95%; both V1 and V3 conceded "deterministic" (R1-V1:39, R1-V3:44; `debate-transcript.md:600`).
- **Integration point**: "The brief text can be checked by text tools; at run time both the command and the guard are a model applying a written rule."
- **Risk**: Medium. Modifies a base claim.

### Change 5: Named "Known weaknesses" section (from Variant 1, adapted)
- **Source**: Variant 1, "Known weakness" (V1:19); S-002, unanimous V1 at 96% (`debate-transcript.md:579`)
- **Target**: Base, new section after "How a person works day to day"
- **Rationale**: V3 offered no self-critique (DA:19; Completeness 2 NOT MET, `BSel:44`).
- **Integration point**: List the residual gaps the guard does not close (accepted risks from changes 22-23 and `invariant-probe.md:28`).
- **Risk**: Low. Additive.

### Change 6: Guard trigger is Orca's role table (from Variant 2)
- **Source**: Variant 2, Strongest case (V2:8); U-004, C-010 unanimous V3 at 93% (`debate-transcript.md:594`)
- **Target**: Base, Position and "Why a third option" (replace the `[G]` 78-82 citation)
- **Rationale**: V3's `[G]` 78-82 range was overstated for identity, conceded (R2-V3 #5; DA:100).
- **Integration point**: The guard applies only in a session whose current prompt carries a live Orca preamble with Task and Dispatch IDs (`[G]` 38, 41; `CAPS:148`; `SPEC:53`).
- **Risk**: Medium. Changes the cited trigger; same behaviour.

### Change 7: Reflect's `claude --print` precedent supports an explicit switch (from Variant 2)
- **Source**: Variant 2, Reliability (V2:19); U-006, C-012 unanimous V2 at 95% (`debate-transcript.md:596`)
- **Target**: Base, "Why a third option" (append)
- **Rationale**: The repo's only headless precedent keys on `claude --print` with no TTY, and Orca launches Claude interactively with the task on the command line (`CAPS:47`), so it is assumed not to fire for an Orca worker (UNVERIFIED, `SPEC:391` item 9). Either way a worker needs an explicit switch.
- **Integration point**: One sentence after the (b) critique.
- **Risk**: Low. Additive.

### Change 8: `ORCA_TERMINAL_HANDLE` marks any live Orca terminal (from Variant 2)
- **Source**: R2-V2 New evidence 2; `CAPS:149`, `CAPS:151`
- **Target**: Base, "Why a third option" (replace the `worker-list` observation as the main reason)
- **Rationale**: Closes the environment route on Orca's own identity rules rather than on the unverified `worker-list` reading (A-001; A-001 unanimous equal at 93%, `debate-transcript.md:605`). "Any live Orca terminal" is inferred from Orca's identity error text (`CAPS:149`) plus one dispatched-worker observation (`CAPS:151`); UNVERIFIED item 13 (`SPEC:395`) is not directly resolved.
- **Integration point**: Keep the 2026-11-02 observation as supporting evidence only.
- **Risk**: Low.

### Change 9: Key the guard to the command's `## Unattended mode` section (debate refinement)
- **Source**: R1-V3:16-21; X-005, majority V3 (corrected) at 78% (`debate-transcript.md:602`); INV-006 ADDRESSED
- **Target**: Base, Position (replace "if the command line in its Task has no standalone `--unattended`")
- **Rationale**: As written, V3:3 refused every flagless brief, including the spec's P0 smoke runs and `/sc:load` steps (`SPEC:191`, `SPEC:197`); conceded (R1-V3:42).
- **Integration point**: Rewrite the guard's case 1 as "the command has an `## Unattended mode` section and the command line lacks a standalone `--unattended`". The key is the copy actually loaded (change 18).
- **Risk**: High. Restructures the base's central rule.

### Change 10: Symmetric check (debate refinement)
- **Source**: R2-V1:35 (New evidence 3); R2-V3 #11; INV-007 ADDRESSED
- **Target**: Base, Position (append guard case 2)
- **Rationale**: `SPEC:79` invites the flag on a command that is not converted, for example `/sc:auggie-review <PR> --unattended` before P2, which would ignore the token and post by default (`SPEC:123`, `SPEC:169`, `SPEC:193`).
- **Integration point**: Case 2: refuse when the command line has the flag and the loaded command has no section.
- **Risk**: Medium. Adds a refusal path; misfires are caught by AC-1.2.

### Change 11: Ship the guard in P1, not P0 (debate refinement)
- **Source**: R1-V3:21; R2-V3 New evidence 1
- **Target**: Base, Implementation cost (replace "one live check in P0 or P1")
- **Rationale**: Clarity 1 NOT MET for "P0 or P1" (`BSel:76`); P0 has no sectioned command (`SPEC:191`).
- **Integration point**: "The guard ships with P1, the first phase with flag-accepting commands (`SPEC:182`)."
- **Risk**: Low.

### Change 12: Guard text travels in the brief template and in `WORKER-CONTRACT.md` (debate refinement)
- **Source**: R2-V1 #5; R2-V2 critique 2; R2-V3 #3
- **Target**: Base, Reliability second bullet (replace "one rule in one file")
- **Rationale**: `WORKER-CONTRACT.md` is an installed file that nothing in the spec loads automatically (`SPEC:58` names only where it is installed; the inference is R2-V3 #3); A-009 unanimous V3 at 93% only in the narrowed form (`debate-transcript.md:608`).
- **Integration point**: State both locations, and that a brief written without the template falls back to (a) (change 17).
- **Risk**: Medium. Modifies the base cost claim.

### Change 13: Amend `SPEC:79` (debate refinement)
- **Source**: R1-V1 A-005; R2-V1 #10; A-005 unanimous equal at 94% (`debate-transcript.md:607`)
- **Target**: Base, new section "Spec wording changes"
- **Rationale**: `SPEC:79` says every brief carries `--unattended`, which contradicts `SPEC:191` and `SPEC:197`.
- **Integration point**: "the exact command line, including `--unattended` where the command accepts it at this phase". `SPEC:329` ("writes it into every worker's command line") repeats the contradiction and gets the same qualifier (REVIEW M7).
- **Risk**: Low.

### Change 14: The flag crosses the Agent-tool boundary; the preamble does not (debate refinement)
- **Source**: R2-V1:33 (New evidence 1); R2-V2 New evidence 1; `SPEC:71`, `SPEC:145`
- **Target**: Base, "Why a third option" (append, as a further reason against (b))
- **Rationale**: C-005 unanimous equal (V1, V3) at 96% (`debate-transcript.md:589`).
- **Integration point**: One sentence.
- **Risk**: Low.

### Change 15: Guard scope is the Task's own command line (debate refinement, merged with change 21)
- **Source**: R2-V3 New evidence 2; INV-014 ADDRESSED
- **Target**: Base, new section "What the guard checks and when"
- **Rationale**: Nested Agent-tool fan-out runs below the worker session and relies on AC-2.1 (`SPEC:263`).
- **Integration point**: Combined with change 21. For nested commands, change 22 supersedes this change's "relies on AC-2.1": change 22 covers nesting through both the Skill tool and the Agent tool (REVIEW M13).
- **Risk**: Low.

### Change 16: Checks for the guard (debate refinement, extended by change 23)
- **Source**: R2-V3 New evidence 1; R2-V3:86-89
- **Target**: Base, Reliability (replace the one-run test)
- **Rationale**: C-003 unanimous V3 at 93% (`debate-transcript.md:587`).
- **Integration point**: Static assertion in `test_worker_contract.py`; AC-1.2 for false refusals; one P1 run per refusal case; the discriminating P2 bare-topic tdd run.
- **Risk**: Low.

### Change 17: A brief written without the template falls back to (a) (debate refinement)
- **Source**: R2-V3 #3; INV-019 ADDRESSED
- **Target**: Base, Known weaknesses (change 5)
- **Rationale**: The guard catches "template used, flag wrong", never "no template".
- **Integration point**: One bullet.
- **Risk**: Low.

### Change 18: The guard reads the command file that will actually be loaded (INV-001, HIGH)
- **Source**: INV-001; R2-V3 #7; K1 and K4 (`CR01:24`, `CR01:42`)
- **Target**: Base, "What the guard checks and when"; Known weaknesses; Spec wording changes (7.2)
- **Rationale**: AC-1.1 checks `src/superclaude/commands` (`SPEC:257`), but a worker loads `~/.claude/commands/sc/` or a project `.claude/commands/sc/` copy. An Orca-created worktree has no gitignored `.claude/` copies until setup runs (`CR01:24`), so a fresh worker normally loads the installed `~/.claude` copy, which lags `src/` until someone reinstalls. A stale copy without the section would really run attended, so refusing it is correct; the failure is the reason text and the check setup, not the refusal.
- **Integration point** (revised for REVIEW B1): (i) The guard reads every copy of the command file that exists: the project `.claude/commands/sc/<name>.md` in the worker's worktree and `~/.claude/commands/sc/<name>.md`. Which one Claude Code loads when both exist is UNVERIFIED (the repo's stated order for skills is `~/.claude/skills/` first, `ROOT-CLAUDE:88`), so the guard does not guess: cases 1 and 2 use "has the section" only when every existing copy agrees. (ii) When the copies disagree, the guard refuses with its own reason: `command copies disagree (stale copy): <paths>`. (iii) Case 2's reason names both causes: `loaded command has no Unattended mode section (not converted at this phase, or the loaded copy is stale)`. (iv) For a 7.2 run, the worktree's project copy is made current by `make sync-dev` inside that worktree, and `~/.claude` is never reinstalled for a check, because that would change the person's own global install. Whether Orca's `--setup run` performs `make sync-dev` is UNVERIFIED (`CR01:42`); if not, the coordinator runs it before dispatch. 7.2 step 1 then confirms the section in every existing copy. (v) Known weakness: the protocol skill that a command loads also exists in two copies and can skew the same way; the guard does not check skills.
- **Risk**: Medium. Adds one or two file reads per Task and a setup precondition to every 7.2 run.

### Change 19: pr-submit is refused while D3 is (a) (INV-005, HIGH)
- **Source**: INV-005; `SPEC:162`, `SPEC:197`, `SPEC:341`
- **Target**: Base, Position (guard case 3) and Safety
- **Rationale**: Under D3 (a) pr-submit is "Coordinator or person only" but is neither in the six-name list (`SPEC:150-160`) nor sectioned, so a flagless worker brief passes cases 1 and 2 and runs it attended with outward defaults on.
- **Integration point**: Case 3 refuses any command on a "never as a worker" list held in `WORKER-CONTRACT.md`: the six section 4 commands, plus `/sc:pr-submit` while D3's answer keeps it off workers. If D3 adds a worker route for pr-submit, D3 must also say how that route passes the guard.
- **Risk**: Low. One list entry; depends on D3's final text.

### Change 20: The guard runs on the brief before the command is invoked (INV-015, HIGH)
- **Source**: INV-015; `CORE-CLAUDE:74`
- **Target**: Base, "What the guard checks and when"
- **Rationale**: The installed rule makes the skill load blocking "before any other output" once a `/sc:` command is invoked (`CORE-CLAUDE:74`). A guard that fires after the command is loaded competes with it, and for `/sc:pm` or `/sc:agent` side effects could come first (`SPEC:155`, `SPEC:158`).
- **Integration point**: The guard is part of reading the Task, not part of running the command: the worker checks the brief's `Command:` line before it invokes anything. Case 3 is decided from the command name alone, with no file read. Cases 1 and 2 read the command file as a plain file read (change 18), which does not invoke the command. The brief template puts the preamble-facing instructions and the guard line before the `Command:` lines, so the Task text never starts with `/sc:`. The spec's own example briefs that start with `/sc:` (worked example `SPEC:90`, `SPEC:93`; AC-2.2 and AC-2.6 briefs) are rewritten to that layout (REVIEW M6). Two points are UNVERIFIED: whether Orca's Task text could still start with the command, and whether a command the worker invokes from a mid-brief `Command:` line still counts as run directly at the top level, as WC-7 and AC-0.4 require (`SPEC:71`, `SPEC:254`); AC-0.4's step-5 transcript check settles the second. The case-3 live run (change 23) confirms there are no side effects.
- **Risk**: High. Reverses R2-V3 #7's "no separate file read" refinement; the guard now costs one Read.

### Change 21: Scope is the brief's `Command:` line only (INV-016, HIGH)
- **Source**: INV-016; `WF:58`; R2-V3:33
- **Target**: Base, "What the guard checks and when"
- **Rationale**: workflow invokes `/sc:reflect --mode pre` via Skill in the same session with default flags (`WF:58`), and reflect gains its section in P2 (`SPEC:193`). If the guard checked that in-session load, every flagged workflow worker would be refused from P2.
- **Integration point**: The brief carries one labelled `Command:` line per command (for example a `/sc:load` line and then the converted command, the shape `SPEC:197` endorses). The guard checks every `Command:` line once, before the worker runs any of them, so a refusal means nothing ran, which also closes INV-013 (REVIEW M14). A command invoked by another command, through the Skill tool in the same session or through the Agent tool, is never checked by the guard. That case is governed by change 22.
- **Risk**: Low. Narrows scope; closes an undefined case.

### Change 22: `--unattended` propagates to nested commands, or the nested step is gate-free (INV-020, HIGH)
- **Source**: INV-020; `BS:185`; `SPEC:139`, `SPEC:145`
- **Target**: Base, new paragraph in "What the guard checks and when" and Spec wording changes (section 2.1 contract file rules)
- **Rationale**: A flagged P1 brainstorm worker auto-invokes research when the topic names an unknown framework (`BS:185`), with no `--unattended`; research needs the flag to pin `--strategy planning` (`SPEC:139`) and gains it only in P2 (`SPEC:193`). Only the tasklist row propagates the flag today (`SPEC:145`). The guard cannot help, because it checks only the top-level line (change 21).
- **Integration point**: New shared rule for `WORKER-CONTRACT.md`: under `--unattended`, a command that invokes another `/sc:` command or protocol skill (Skill tool or Agent tool) passes `--unattended` when the invoked command accepts it at this phase, together with its own report directory, `<caller report-dir>/nested/<command>-<n>/` (revised for REVIEW B2: without it the nested command would refuse under WC-4's exactly-one-report-directory rule, `SPEC:57`, `SPEC:68`, or overwrite the caller's contract, against WC-11, `SPEC:75`). The caller lists the nested contract in its `artifacts`; only the top-level contract drives WC-5. When the invoked command does not accept the flag yet, that step must be gate-free per its section 3 row, or the calling command skips it under `--unattended` and records the skip in its contract. Each command's `## Unattended mode` section names its nested invocations, and AC-2.1-style assertions check that each one passes both the flag and the nested report directory. Known cases: workflow invokes reflect (`WF:58`; reflect accepts the flag from P2) and brainstorm's automatic research enrichment (`BS:185`, run through Task agents, `BS:179`; research accepts the flag from P2). Both callers therefore need a P2 edit to their sections, although neither is in the P2 list (`SPEC:183`). Until P2, brainstorm turns automatic research enrichment off under `--unattended`; workflow's reflect step is already gate-free (no `--remediate`, `WF:58`). The merged position states "a worker never stalls" only for converted gates, and lists incomplete gate lists (INV-022) as a known weakness.
- **Risk**: Medium. Adds a rule each nesting command must follow and two P2 section edits; per-command details belong to the phase plans.

### Change 23: MEDIUM invariants bundle (INV-002, 008, 009, 010, 017, 018, 022, 023)
- **Source**: `invariant-probe.md:35`, `:41-44`, `:50-51`, `:55-56`
- **Target**: Base, "What the guard checks and when", Checks, Known weaknesses, Spec wording changes
- **Rationale**: Not blocking, but each changes what a person or coordinator sees.
- **Integration point**:
  - INV-008, INV-023: the guard sentence says it applies only in a session whose current prompt carries a live preamble with Task and Dispatch IDs; AC-1.3's manual part adds one flagless run of a converted command in the coordinator session with `WORKER-CONTRACT.md` loaded (pass: today's behaviour, no refusal).
  - INV-009: the guard checks the brief's labelled `Command:` line only, never the rest of the brief, so the guard's own wording cannot be read as the flag.
  - INV-018: the guard checks once, before the first run; WC-3's re-invocation after an answered `ask` is not re-checked by the guard, but the worker-session rule says the re-invoked line keeps every token of the brief's `Command:` line, `--unattended` included, and only adds the answer. A re-invocation that drops the token is a Known weakness (REVIEW M12).
  - INV-002: the coordinator decides whether to add the flag by the same test the guard uses, run on the copies the worker will see (the target worktree's project copy and `~/.claude`), not the coordinator's own copy, so it needs no installed phase table (REVIEW M9).
  - INV-010: one P1 live run per refusal case (1, 2, 3), with AC-1.5's pass conditions (`SPEC:261`). The case-3 run uses `/sc:help` (read-only, `SPEC:157`) in the disposable worktree, never `/sc:pm`, `/sc:agent`, `/sc:git` or `/sc:pr-submit`, so a guard failure has no side effects (REVIEW M5).
  - INV-017: section 2.3 gains: a `worker_done --outcome failed` with no contract whose body starts `guard refused:` is a guard refusal; the coordinator fixes the brief, never re-creates it unchanged, and allows at most 2 brief fixes for the same work (3 attempts); a third refusal escalates to the person, matching K3's 2-fix-cycle cap (REVIEW M1).
  - INV-022: Known weakness (incomplete gate list), caught only by 7.2 steps 2-3 (`SPEC:237-238`).
- **Risk**: Medium. Several small edits across the contract file and section 7.

### Change 24: Fixed user constraints K1-K4
- **Source**: K1-K4 in the Overview
- **Target**: Base, Spec wording changes and a new "Interactions" section
- **Rationale**: Applied as given, not debated.
- **Integration point**:
  - K1: 7.2's disposable worktree is created by Orca (`worker-start --worktree new-top-level` or `orca worktree create`) at Orca's default path, with setup before dispatch; `SPEC:235`'s `.dev/worktrees/` wording is replaced (`CR01:41`). Revised for REVIEW B3: Orca creates a worktree from a git base (`CR01:22`, `CR01:51`), so it holds only committed work, while phase edits stay uncommitted unless the user asks (`SPEC:229`; `ROOT-CLAUDE:37`). Before a 7.2 run, the phase's edits are therefore committed to the feature branch or a scratch branch, with the user's authorization (a user decision point each phase), and the disposable worktree is created with `--base-branch <that branch>`; after step 7 it is removed with `orca worktree rm`, because orchestration verbs never delete worktrees (`CR01:23`). This also feeds change 18.
  - K2: no part of D1 talks to GitHub; the guard and the flag add no outward action. No change beyond noting it.
  - K3: the guard-refusal escalation in change 23 uses the same 2-cycle cap; each phase's own `/sc:implement` QA follows PR #343's rules unchanged.
  - K4: the guard is per worker session and works the same in the shared feature worktree or a child worktree; CR-01 child setup (`CR01:24`) is the same step change 18 needs. Under D3 (a), CR-01's trigger T3 (pr-submit in a child) applies to the coordinator's or person's own pr-submit run, not to a worker (change 19). D3's debate converged on (a) as the default plus (c), a person-owned handoff tab (`D3/debate/adversarial/debate-transcript.md:665`); that tab carries no Orca preamble, so the guard never applies there and change 19 stays valid (REVIEW M8).
- **Risk**: Low.

## Invariant Coverage (HIGH UNADDRESSED)

The gate is `BLOCKED_BY_INVARIANTS` (`debate-transcript.md:638-653`). Depth standard allows no further round, so each blocking item gets one planned change or one explicit accepted-risk entry here. None of the five favours option (b) (`invariant-probe.md:104`).

| Item | Disposition | Planned change | What remains open |
|---|---|---|---|
| INV-001: guard key checked in `src/`, worker loads another copy | Planned change | 18 (guard reads every existing copy and refuses when they disagree; refusal reasons name staleness; 7.2 commits the phase edits to a branch, creates the Orca worktree from it and runs `make sync-dev` there, change 24) | Command precedence between project `.claude/commands/sc/` and `~/.claude/commands/sc/` is UNVERIFIED; the all-copies rule makes the guard independent of it. Skill copies can skew the same way and are not checked (Known weakness) |
| INV-005: pr-submit not covered under D3 (a) | Planned change | 19 (never-as-worker list adds pr-submit while D3 keeps it off workers) | Depends on D3's final text (D3 debate converged on (a) as default, `D3/debate/adversarial/debate-transcript.md:665`) |
| INV-015: guard order vs the blocking skill-first rule | Planned change | 20 (guard runs while reading the Task, before invoking; case 3 by name only) | Whether Orca's Task text can start with the `/sc:` line is UNVERIFIED; the case-3 live run checks there are no side effects |
| INV-016: in-session Skill nesting scope undefined | Planned change | 21 (scope = the brief's `Command:` line only) | None for the guard; nested stalls move to INV-020 |
| INV-020: flag does not reach nested in-session skills | Planned change plus accepted residual | 22 (propagation rule or gate-free nested step; per-command listing and assertions) | "Never stalls" holds only for converted gates; an incomplete gate list (INV-022) is accepted risk, caught after the fact by 7.2 steps 2-3 |

These are planned amendments, not debated ones: no advocate round tested them. The return contract therefore still lists all five items under `unaddressed_invariants` and reports `status: partial`, and the residuals above appear in the merged position's Known weaknesses as accepted risks, not as resolved.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|---|---|---|
| C-007, X-006 (V1 wins) | Option (a) alone: lowest cost, no guard | Unanimous that (a) is cheapest (96%), but the advocates of (a) recommend (c) (R2-V1:76). The extra cost is the guard rule in the template and the contract file, the never-as-worker list, one or two Reads per Task, a refusal-reading rule in section 2.3 and four live runs, with no command edits for the guard itself (R2-V3 #12). (a) stays the fallback: removing those guard parts (template guard line, contract-file guard rule, never-as-worker list, section 2.3 refusal rule, the four guard runs) returns (a); the `Command:` layout, the propagation rule (change 22) and the K1 setup are independent of the guard and stay (REVIEW M4). |
| X-004 | V1:23 "add detection later as an extra trigger" | Conceded wrong (R1-V1:40): detection in commands breaks SA-2 and non-goal 1 (`SPEC:170`, `SPEC:314`). The only cheap later home is the worker session, which is where the guard already sits. |
| C-001, C-009, A-001 | Option (b) environment route (`ORCA_TERMINAL_HANDLE`) | Withdrawn by its own advocate (R2-V2:86). The variable marks any live Orca terminal by design (`CAPS:149`, `CAPS:151`), so it cannot tell a worker from a person's tab (SA-1, `SPEC:169`). |
| X-001, X-002, C-005 | Option (b) preamble detection inside commands | Breaks SA-2 and non-goal 1, cannot reach Agent-tool subagents (`SPEC:71`, `SPEC:145`), and a miss changes what the command does, while under (c) a guard miss falls back to (a) (R2-V3 #6). |
| S-005 | V1's `SPEC`/`CAPS`-only citation style | Majority equal (72%): `[G]` lines need only an installed `orca-ide` (`CAPS:147`) and `CAPS:148` quotes them; the merged text cites both. |
| Not a diff point (considered while planning change 19) | An allowlist of commands that may run flagless, instead of a never-as-worker list | Rejected to keep the debate's "no second list that tracks phases" property (R2-V3 #2, R2-V1:34). The never-as-worker list changes only when section 4 or D3 changes, not per phase. |
| Not a diff point (considered while planning change 18) | R2-V3 #7's "no separate file read" (check the command text after loading it) | Superseded by change 20: checking after loading conflicts with the blocking skill-first rule (`CORE-CLAUDE:74`, INV-015). |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1, 2, 3, 5, 7, 8, 11, 13, 14, 15, 16, 17 | Low | Wording or citation gap; no behaviour change | Remove or revert the sentence |
| 4 | Medium | Overclaims or underclaims what is mechanical | Revert to V3's Reliability bullet with "Deterministic" struck |
| 6 | Medium | Wrong trigger citation | Revert to `CAPS:148` alone |
| 9 | High | Guard refuses legitimate flagless briefs (X-005) or misses a forgotten flag | Remove the guard parts listed under "Changes NOT Being Made" (C-007 row): the command side is exactly (a) |
| 10 | Medium | Correct flagged briefs refused | AC-1.2 catches it on the first P1 run; drop case 2 |
| 12 | Medium | Guard never reaches the worker | Falls back to (a) (INV-019) |
| 18 | Medium | Copies disagree or a stale copy refuses every flagged brief in a 7.2 run | Refusal reason names staleness and the paths; fix the branch base or `make sync-dev` step (change 24), not the guard |
| 19 | Low | pr-submit reaches a worker attended | Remove the list entry once D3 adds a sectioned worker route |
| 20 | High | Skill loads before the guard; coordinator-only side effects | Case-3 live run fails visibly; fall back to (a) plus section 4's prose ban |
| 21 | Low | A nested command is wrongly refused | Scope is already the narrowest; none needed |
| 22 | Medium | A flagged worker stalls inside a nested command | 7.2 steps 2-3 show the stall; fix the calling command's section |
| 23 | Medium | Coordinator loops on refusals, or the coordinator session refuses its own run | 2-refusal cap then escalation; AC-1.3 manual run catches the second |
| 24 | Medium | 7.2 run in a worktree without the phase's edits or without setup | Commit the edits to the base branch with user authorization, recreate the worktree, rerun setup (CR-01 item 5) |

## Review Status
- [x] Auto-approved (default; `--interactive` was not set)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-02T17:54Z
- Analytical review: see "Plan review" below (fresh-context reviewer, not the drafter).

## Plan review
- Review 1 (fresh-context reviewer, `refactor-plan-review.md`): `VERDICT: FAIL`, 3 blocking findings (B1 guard reads a guessed copy; B2 nested commands get no report directory; B3 an Orca-created worktree lacks uncommitted phase edits) and 14 minor notes.
- Fix cycle 1 (drafter, 2026-11-02): B1 applied to change 18; B2 to change 22; B3 to change 24 (K1). Minor notes applied where they changed wording or a fact: M1 (change 23), M2 (change 7), M3 (change 8), M4 ("Changes NOT Being Made" C-007 row, Risk Summary row 9), M5, M9, M12 (change 23), M6 (change 20), M7 (change 13), M8 (change 24), M10 (citation key), M11 (change 12), M13 (change 15), M14 (change 21).
- Under K3, minor notes are not rechecked; only the blocking fixes go to a second review if one is run. The merge executor (Step 5) is the next independent reader of this plan, and its post-merge validation re-scans for contradictions.
