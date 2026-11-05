<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 3 (option c) -->
<!-- Merge date: 2026-11-02 -->

# D1 merged position: option (c) as amended, the flag is the only switch and the worker session refuses a brief that does not match the command

## Position
<!-- Source: Base (original, modified): the command side is kept from Variant 3 (V3:3); the guard's trigger, key, timing, scope and refusal cases are rewritten per Changes #6, #9, #10, #11, #18, #19, #20, #21, #23 to resolve X-005 and the HIGH invariants INV-001, INV-005, INV-015, INV-016 -->
Commands behave exactly as in option (a): only the standalone `--unattended` token, outside any quoted argument, switches them (`SPEC:55`); no command reads the environment or the conversation. In addition, from P1, the first phase with flag-accepting commands (`SPEC:182`), the worker session checks its brief before running anything. The worker session is only a session whose current prompt carries a live Orca preamble with Task and Dispatch IDs (`[G]` 38, 41; `CAPS:148`; `SPEC:53`). It checks every `Command:` line of its brief before it runs any of them, and refuses with `worker_done --outcome failed`, a body starting `guard refused:`, and nothing run, in these cases:
- Case 1: the line lacks a standalone `--unattended` while every existing copy of the command file has an `## Unattended mode` section.
- Case 2: the line has the flag while no existing copy has the section.
- Copies disagree: one existing copy of the command file has the section and another does not.
- Case 3: the command is on the never-as-worker list in `WORKER-CONTRACT.md`: the six section 4 commands (`SPEC:150-160`) plus `/sc:pr-submit` while D3 keeps it off workers (`SPEC:162`, `SPEC:341`).

The coordinator then fixes the brief in a new Task (WC-6, `SPEC:70`), with at most 2 brief fixes for the same work before it escalates to the person. "What the guard checks and when" gives the order of the checks, the copies read and the scope.

## Citation key
<!-- Source: Base (original, modified): the base's three keys are kept; the plan's further keys are added because the merged text cites them (refactor-plan.md citation key; REVIEW M10) -->
- `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`.
- `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`.
- `[G] N` = line N of `orca-ide skills get orchestration` (1.4.237).
- `CR01:N` = `.dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md:N`.
- `CORE-CLAUDE:N` = `src/superclaude/core/CLAUDE.md:N` (installed to `~/.claude/CLAUDE.md`).
- `ROOT-CLAUDE:N` = the repository-root `CLAUDE.md:N`.
- `WF:N` = `src/superclaude/skills/sc-workflow-protocol/SKILL.md:N`.
- `BS:N` = `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:N`.
- `INV-NNN` = row of `.dev/orca-command-refactor/decisions/D1/debate/adversarial/invariant-probe.md`.
- `R1-Vn:N`, `R2-Vn:N` = line N of `rounds/r1-variant-n.md`, `rounds/r2-variant-n.md` in the same directory; `R2-Vn #k` = row k of that file's "Responses to criticisms" table.

## Why this option
<!-- Source: Base (original), "Why a third option" (V3:8), restated one claim per bullet -->
- Option (a) leaves one failure open: a brief without the flag makes a command prompt, and the worker stalls with no `worker_done` while Orca reports it "healthy, not failed" (`SPEC:47`; `CAPS:52`, `CAPS:129`).
- Option (b) closes that hole by putting Orca detection into commands, which breaks SA-2 and non-goal 1 (`SPEC:170`, `SPEC:314`).

<!-- Source: Variant 2, Round 2 New evidence 2, merged per Change #8 (replaces the base's worker-list observation as the main reason; the observation is kept as supporting evidence only) -->
- On the environment route, (b) cannot tell a worker from a person's own Orca tab: `ORCA_TERMINAL_HANDLE` marks any live Orca terminal. This is inferred from Orca's identity error text (`CAPS:149`) plus one dispatched-worker observation (`CAPS:151`); UNVERIFIED item 13 (`SPEC:395`) is not directly resolved.
- Supporting observation only: on 2026-11-02 the session that drafted Variant 3 had `ORCA_TERMINAL_HANDLE` set but was not among the 11 workers `orca-ide orchestration worker-list --json` listed (V3:8).

<!-- Source: Variant 2, Reliability (V2:19), merged per Change #7 -->
- The repo's only headless precedent keys on `claude --print` with no TTY, and Orca launches Claude interactively with the task on the command line (`CAPS:47`), so it is assumed not to fire for an Orca worker (UNVERIFIED, `SPEC:391` item 9). Either way a worker needs an explicit switch.

<!-- Source: Round 2 debate (R2-V1:33, New evidence 1; R2-V2 New evidence 1), merged per Change #14 -->
- The flag crosses the Agent-tool boundary and the preamble does not: a command's own subagents receive the command line their caller writes, never the worker's preamble (`SPEC:71`, `SPEC:145`), so detection inside commands could not reach nested fan-out, while the token can.

<!-- Source: Base (original, modified): the identity citation `[G]` 78-82 is replaced by Orca's role table per Change #6 (conceded at R2-V3 #5) -->
- Option (c) closes the hole where the check is already Orca-aware: the worker session. Orca's role table calls a session whose current prompt carries a live injected preamble with Task and Dispatch IDs a dispatched worker, and a session with no live preamble an ordinary terminal agent (`[G]` 38, 41; `CAPS:148`); the spec adopts that rule as "Worker run" (`SPEC:53`).
- The spec already gives the worker session Orca duties (WC-3, WC-5, WC-7, WC-12 at `SPEC:67-76`), and SA-2 governs command files, not the worker session (`SPEC:170`).

## What the guard checks and when
<!-- Source: Debate refinement and invariant probe, merged per Changes #6 and #23 (INV-008, INV-023): who applies the guard -->
### Who applies it
- Only a session whose current prompt carries a live Orca preamble with Task and Dispatch IDs (`[G]` 38, 41; `CAPS:148`; `SPEC:53`).
- A coordinator session, or a person's own session, that has `WORKER-CONTRACT.md` in context has no such preamble, so it never applies the guard to its own runs (INV-008, INV-023; checked by the AC-1.3 manual run in "Reliability and checks").

<!-- Source: Invariant probe INV-015, merged per Change #20 (supersedes R2-V3 #7's "no separate file read") -->
### When it runs
- The guard is part of reading the Task, not part of running the command: the worker checks the brief's `Command:` lines before it invokes anything.
- Reason: once a `/sc:` command is invoked, the installed rule makes its skill load blocking "before any other output" (`CORE-CLAUDE:74`). A guard that fired after the command loaded would compete with that rule, and for `/sc:pm` or `/sc:agent` side effects could come first (`SPEC:155`, `SPEC:158`).
- The brief template puts the preamble-facing instructions and the guard line before the `Command:` lines, so the Task text never starts with `/sc:`.
- UNVERIFIED: whether Orca's Task text could still start with the command.
- UNVERIFIED: whether a command the worker invokes from a mid-brief `Command:` line still counts as run directly at the top level, as WC-7 and AC-0.4 require (`SPEC:71`, `SPEC:254`). AC-0.4's step-5 transcript check settles it.

<!-- Source: Debate refinements (R1-V3:16-21; R2-V3 #11) and invariant probe INV-001, INV-005, merged per Changes #9, #10, #18, #19, #20 -->
### Order of the checks
1. Case 3 is decided from the command name alone, with no file read: the command is on the never-as-worker list (`WORKER-CONTRACT.md`; six section 4 commands plus `/sc:pr-submit` while D3 keeps it off workers).
2. The guard reads every copy of the command file that exists, as a plain file read, which does not invoke the command: the project `.claude/commands/sc/<name>.md` in the worker's worktree and `~/.claude/commands/sc/<name>.md`.
3. If the copies disagree on whether they have an `## Unattended mode` section, the guard refuses with `guard refused: command copies disagree (stale copy): <paths>`.
4. Case 1: every existing copy has the section and the `Command:` line lacks a standalone `--unattended`. Reason: `guard refused: brief lacks --unattended`.
5. Case 2: no existing copy has the section and the `Command:` line has the flag. Reason: `guard refused: loaded command has no Unattended mode section (not converted at this phase, or the loaded copy is stale)`.
6. Otherwise the line passes. A flagless line for a command with no section in any copy passes, which keeps P0 smoke runs and `/sc:load` steps working (`SPEC:191`, `SPEC:197`).

<!-- Source: Invariant probe INV-001, merged per Change #18 (revised for REVIEW B1) -->
### Why every copy
- AC-1.1 checks `src/superclaude/commands` (`SPEC:257`), but a worker loads `~/.claude/commands/sc/` or a project `.claude/commands/sc/` copy.
- An Orca-created worktree has no gitignored `.claude/` copies until setup runs (`CR01:24`), so a fresh worker normally loads the installed `~/.claude` copy, which lags `src/` until someone reinstalls.
- Which copy Claude Code loads when both exist is UNVERIFIED (the repo's stated order for skills is `~/.claude/skills/` first, `ROOT-CLAUDE:88`). The guard therefore does not guess: cases 1 and 2 use "has the section" only when every existing copy agrees.
- A stale copy without the section would really run attended, so refusing it is correct; the refusal reasons name staleness so the fix goes to setup, not to the guard.

<!-- Source: Invariant probe INV-016, INV-009, INV-013, merged per Changes #21 and #23; Change #15 (R2-V3 New evidence 2, INV-014) merged here and superseded for nested commands by Change #22 -->
### Scope
- The brief carries one labelled `Command:` line per command, for example a `/sc:load` line and then the converted command, the shape `SPEC:197` endorses.
- The guard checks every `Command:` line once, before the worker runs any of them, so a refusal means nothing ran (INV-013).
- The guard checks only the labelled `Command:` lines, never the rest of the brief, so the guard's own wording, which contains the literal token `--unattended`, cannot be read as the flag (INV-009).
- A command invoked by another command, through the Skill tool in the same session or through the Agent tool, is never checked by the guard. Example: workflow invokes `/sc:reflect --mode pre` via Skill with default flags (`WF:58`), and reflect gains its section in P2 (`SPEC:193`); if the guard checked that load, every flagged workflow worker would be refused from P2. Nested commands are governed by the propagation rule below.
- The guard checks once, before the first run. WC-3's re-invocation after an answered `ask` (`SPEC:67`) is not re-checked by the guard; the worker-session rule says the re-invoked line keeps every token of the brief's `Command:` line, `--unattended` included, and only adds the answer (INV-018).

<!-- Source: Invariant probe INV-020, merged per Change #22 (revised for REVIEW B2); supersedes Change #15's "relies on AC-2.1" for nested commands (REVIEW M13) -->
### Nested commands: propagation rule
- New shared rule for `WORKER-CONTRACT.md`: under `--unattended`, a command that invokes another `/sc:` command or protocol skill (Skill tool or Agent tool) passes `--unattended` when the invoked command accepts it at this phase, together with its own report directory, `<caller report-dir>/nested/<command>-<n>/`.
- Without that directory the nested command would refuse under WC-4's exactly-one-report-directory rule (`SPEC:57`, `SPEC:68`), or overwrite the caller's contract, against WC-11 (`SPEC:75`).
- The caller lists the nested contract in its `artifacts`; only the top-level contract drives WC-5 (`SPEC:69`).
- When the invoked command does not accept the flag yet, that step must be gate-free per its section 3 row, or the calling command skips it under `--unattended` and records the skip in its contract.
- Each command's `## Unattended mode` section names its nested invocations, and AC-2.1-style assertions check that each one passes both the flag and the nested report directory.
- Today only the tasklist row propagates the flag (`SPEC:145`).
- Known nesting, workflow: workflow invokes reflect (`WF:58`); reflect accepts the flag from P2 (`SPEC:193`). Until then workflow's reflect step is already gate-free (no `--remediate`, `WF:58`).
- Known nesting, brainstorm: brainstorm's automatic research enrichment (`BS:185`), run through Task agents (`BS:179`); research needs the flag to pin `--strategy planning` (`SPEC:139`) and accepts it from P2 (`SPEC:193`). Until P2, brainstorm turns automatic research enrichment off under `--unattended`.
- Both callers therefore need a P2 edit to their sections, although neither is in the P2 list (`SPEC:183`).
- "A worker never stalls" is claimed only for converted gates (see Known weaknesses, INV-022).

<!-- Source: Invariant probe INV-002, merged per Change #23 (REVIEW M9) -->
### How the coordinator decides on the flag
- The coordinator decides whether a `Command:` line carries `--unattended` by the same test the guard uses, run on the copies the worker will see (the target worktree's project copy and `~/.claude`), not on its own copy, so it needs no installed phase table.

## Safety
<!-- Source: Base (original, modified): first bullet kept from V3:11; the quoted-argument example and its live check inserted per Change #3 (Variant 1, Safety, V1:8) -->
- Same as (a) for people: no command reads the environment or the conversation, so a person's tab cannot change behaviour (SA-1, `SPEC:169`).
- Only a standalone token outside any quoted argument counts, so `/sc:troubleshoot "the worker ignores --unattended"` stays a person's run (`SPEC:55`; checked live by AC-2.8, `SPEC:269`).

<!-- Source: Variant 1, Safety (V1:10), merged per Change #1 -->
- WC-9 (`SPEC:73`) applies only under `--unattended`, so a person working in an Orca tab keeps auggie-review's posting default (`SPEC:169`).

<!-- Source: Base (original) (V3:12) -->
- A wrong brief fails fast and visibly instead of stalling: the failure is a `worker_done --outcome failed` with a reason, which is the only failure signal Orca guarantees (`CAPS:73`, "Never encode failure only in prose").

<!-- Source: Base (original, modified): V3:13 kept and extended with pr-submit per Change #19 (INV-005) -->
- It also stops a coordinator-only command (for example `/sc:git` or `/sc:pm`) being run by a worker, which today only section 4's prose forbids (`SPEC:151`).
- It stops `/sc:pr-submit` reaching a worker while D3 keeps it off workers. Under D3 (a) pr-submit is "Coordinator or person only" (`SPEC:341`), yet it is neither in the six-name list (`SPEC:150-160`) nor sectioned (`SPEC:197`), so without the list entry a flagless worker brief would pass cases 1 and 2 and run it attended with outward defaults on (WC-9 applies only under the flag, `SPEC:73`).
- Case 3 is decided from the command name alone, before anything is invoked, so a refused coordinator-only command is never invoked (`SPEC:155`, `SPEC:158`; "What the guard checks and when"). This holds only if Orca's Task text does not itself start with the command (UNVERIFIED); the case-3 live run checks there are no side effects.

<!-- Source: Debate refinement (R2-V1:35, New evidence 3), merged per Change #10 (rationale) -->
- Case 2 stops a flagged brief for a command that is not converted yet. Example: `/sc:auggie-review <PR> --unattended` before P2 would ignore the token, because the command has no section until P2, and post by default (`SPEC:123`, `SPEC:169`, `SPEC:193`).

## Reliability and checks
<!-- Source: Base (original, modified): "Deterministic" replaced per Change #4 (Variant 1, Implementation cost, V1:22; X-003, conceded at R1-V3:44) -->
- The brief text can be checked by text tools; at run time both the command and the guard are a model applying a written rule.
- The check is decided before anything runs ("What the guard checks and when").

<!-- Source: Base (original, modified): "one rule in one file" replaced per Change #12 (R2-V1 #5; R2-V2 critique 2; R2-V3 #3; REVIEW M11) -->
- The guard rule is prose read by a model, like every WC row.
- It travels in two places: a guard line in the brief template and the guard rule in `WORKER-CONTRACT.md` (`SPEC:58`).
- Both are needed because nothing in the spec loads the installed contract file automatically: `SPEC:58` names only where it is installed, and the inference is R2-V3 #3.
- A brief written without the template carries no guard line and falls back to (a) (Known weaknesses).

<!-- Source: Variant 1, Reliability (V1:15), merged per Change #2; consequence for the guard from Change #9 -->
- Phase-gated: a command accepts the flag only once its gates are converted (`SPEC:187-195`), and its `## Unattended mode` section marks that; AC-1.1 ties the section to the phase table (`SPEC:257`).
- So the guard is inert in P0, where no command has a section (`SPEC:191`), and never refuses `/sc:load`, which never gains one (`SPEC:197`).

<!-- Source: Base (original, modified): the base's one-run test replaced per Change #16 (R2-V3 New evidence 1, R2-V3:86-89), extended per Changes #18, #20, #22, #23 (INV-010, INV-008, INV-023; REVIEW M5) -->
### Checks
- Static: `tests/skills/test_worker_contract.py` asserts that `WORKER-CONTRACT.md` states the guard rule, the never-as-worker list and the nested propagation rule, and that the brief template carries the guard line before the `Command:` lines.
- False refusals: AC-1.2 runs every P1 command with `--unattended` and its report directory (`SPEC:258`); a guard that refuses a correct brief fails it on the first run.
- Missed refusals: one P1 live run per refusal case (1, 2, 3), with AC-1.5's pass conditions (`SPEC:261`): nothing written (7.2 step 6 empty), and `worker_done --outcome failed` with no `--report-path`; here the body also starts `guard refused:`.
- The case-3 run uses `/sc:help` (read-only, `SPEC:157`) in the disposable worktree, never `/sc:pm`, `/sc:agent`, `/sc:git` or `/sc:pr-submit`, so a guard failure has no side effects. It also confirms that a refused command is not invoked first ("What the guard checks and when", When it runs).
- Discriminating run, P2: a bare-topic `/sc:tdd` brief with the flag omitted. Without the guard it stalls on tdd's gate (`SPEC:264`); with it, case 1 refuses at once (R2-V3 New evidence 1).
- Coordinator session, manual: AC-1.3's manual part adds one flagless run of a converted command in the coordinator session with `WORKER-CONTRACT.md` loaded. Pass: today's behaviour, no refusal (INV-008, INV-023).
- Nested commands, P2: AC-2.1-style assertions that each nested invocation a command's section names passes both `--unattended` and its nested report directory.
- Copies: for a command that accepts the flag at this phase, 7.2 step 1 confirms the section in every existing copy of the command file in the disposable worktree, after `make sync-dev` there (Interactions, K1).

## How a person works day to day
<!-- Source: Base (original) (V3:20) -->
- No change for people (SA-1, `SPEC:169`).
- Coordinators get an immediate, named failure for a forgotten flag instead of a stall they must diagnose with `worker-read` (`SPEC:238`).

<!-- Source: Invariant probe INV-017, merged per Change #23 (REVIEW M1), with the K3 cap per Change #24 -->
- A `worker_done --outcome failed` with no contract whose body starts `guard refused:` is a guard refusal, and nothing ran.
- The coordinator fixes the brief in a new Task, never re-creates it unchanged, and allows at most 2 brief fixes for the same work (3 attempts); a third refusal escalates to the person, matching K3's 2-fix-cycle cap.

<!-- Source: Fixed constraint K1, merged per Change #24 (revised for REVIEW B3) -->
- Each phase's 7.2 live checks add one decision for the user: authorizing a commit of the phase's edits to a branch so that an Orca-created worktree can hold them (Interactions, K1).

## Known weaknesses (accepted risks)
<!-- Source: Variant 1, "Known weakness" (V1:19), adapted per Change #5 to list the guard's own residual gaps; entries from Changes #17, #18, #20, #22, #23 and `invariant-probe.md:28` -->
- A brief written without the template carries no guard line and gets exactly (a)'s behaviour: the guard catches "template used, flag wrong", never "no template" (INV-019; R2-V3 #3).
- A command not yet converted, run flagless within its brief constraints, still stalls if its input hits a gate, under every option (`SPEC:102`; INV-021; R2-V3 #9).
- "A worker never stalls" holds only for converted gates. An incomplete gate list in a sectioned command is invisible to the guard and is caught only after the fact by 7.2 steps 2-3 (`SPEC:237-238`; INV-022). Possible waits of this kind: index knowledge-base mode, `--mode socratic` and `--format interactive` (whether they wait is UNVERIFIED, `SPEC:388`).
- The protocol skill that a command loads also exists in two copies (`~/.claude/skills/` and the project `.claude/skills/`) and can skew the same way; the guard does not check skills.
- Command precedence between the project `.claude/commands/sc/` copy and `~/.claude/commands/sc/` is UNVERIFIED; the all-copies rule makes the guard independent of it, at the cost of refusing whenever the copies disagree.
- A WC-3 re-invocation that drops the `--unattended` token runs attended and unguarded, because the guard checks only once, before the first run (INV-018).
- UNVERIFIED: whether Orca's Task text could still start with the command, and whether a command invoked from a mid-brief `Command:` line counts as run directly at the top level (`SPEC:71`, `SPEC:254`).
- Case 3 depends on D3's final text: if D3 adds a worker route for pr-submit, the list entry must change with it (INV-005).
- The amendments for the five HIGH invariants (INV-001, INV-005, INV-015, INV-016, INV-020) are planned, not debated: no advocate round tested them. They are accepted risks, not resolved ones.

## Implementation cost
<!-- Source: Base (original, modified): "one live check in P0 or P1" replaced per Change #11; the cost claim restated per Change #12 and the plan's rollback list ("Changes NOT Being Made", C-007 row; REVIEW M4) -->
- The guard ships with P1, the first phase with flag-accepting commands (`SPEC:182`).
- Guard parts: the guard line in the brief template; the guard rule and the never-as-worker list in `WORKER-CONTRACT.md`; one or two file reads per Task; the section 2.3 refusal-reading rule; four live runs (one per refusal case in P1, plus the P2 bare-topic tdd run). The guard needs no command edits (R2-V3 #12).
- Parts independent of the guard: the `Command:` brief layout, the nested propagation rule with its two P2 section edits (workflow, brainstorm), and the K1 worktree setup. They stay if the guard is removed; the propagation gap they close exists under (a) as well (INV-020; `invariant-probe.md:104`).
- Every other command-side cost and benefit of (a) is unchanged.
- Reversal: removing the guard parts listed above returns (a); the independent parts stay.

## Interactions with other decisions and fixed constraints
<!-- Source: Refactor plan fixed constraints K1-K4, merged per Change #24 (K1 revised for REVIEW B3; K4 revised for REVIEW M8); setup step shared with Change #18 (iv). Applied as given, not debated -->
### K1: worktrees are created by Orca at Orca's default path
- Every worktree is created by Orca at Orca's default path, never under `.dev/worktrees/` (`CR01:41`). This overrides `SPEC:235` for the 7.2 disposable worktree.
- Orca creates a worktree from a git base (`CR01:22`, `CR01:51`), so it holds only committed work, while phase edits stay uncommitted unless the user asks (`SPEC:229`; `ROOT-CLAUDE:37`).
- Before a 7.2 run, the phase's edits are therefore committed to the feature branch or a scratch branch, with the user's authorization (a user decision point each phase).
- The disposable worktree is then created by Orca from that branch (`worker-start --worktree new-top-level` or `orca worktree create`, with `--base-branch <that branch>`).
- The worktree's project `.claude/` copy is made current by `make sync-dev` inside that worktree. Whether Orca's `--setup run` performs `make sync-dev` is UNVERIFIED (`CR01:42`); if not, the coordinator runs it before dispatch. In that case the worktree is created with `orca worktree create` first, because `worker-start` sends the task as soon as the agent is ready (`CAPS:46-47`).
- `~/.claude` is never reinstalled for a check, because that would change the person's own global install.
- After 7.2 step 7 the worktree is removed with `orca worktree rm`, because orchestration verbs never delete worktrees (`CR01:23`).

### K2: SuperClaude upstream is never touched
- No part of D1 talks to GitHub; the guard and the flag add no outward action (`CR01:45`; `ROOT-CLAUDE:41-66`).

### K3: review loops stop after 2 fix cycles
- The guard-refusal escalation (at most 2 brief fixes, 3 attempts, then the person) uses the same cap as merged PR #343 (commit `80f934de`: "at most 2 fix cycles (3 reviews), then escalate").
- Each phase's own `/sc:implement` QA follows PR #343's rules unchanged: only blocking findings fail a review.

### K4: one feature worktree, child worktrees only on a trigger
- The guard is per worker session and works the same in the shared feature worktree or in a child worktree.
- CR-01's child setup before use (`CR01:24`) is the same step the all-copies rule needs.

<!-- Source: Invariant probe INV-005, merged per Change #19; D3 interaction per Change #24 (REVIEW M8) -->
### D3: pr-submit
- While D3's answer keeps pr-submit off workers, it is on the never-as-worker list (case 3).
- If D3 adds a worker route for pr-submit, D3 must also say how that route passes the guard.
- Under D3 (a), CR-01's trigger T3 (pr-submit in a child worktree, `CR01:19`) applies to the coordinator's or the person's own pr-submit run, not to a worker.
- D3's debate converged on (a) as the default plus (c), a person-owned handoff tab (`.dev/orca-command-refactor/decisions/D3/debate/adversarial/debate-transcript.md:665`). That tab carries no Orca preamble, so the guard never applies there and the pr-submit list entry stays valid.

## Spec wording changes
<!-- Source: Refactor plan, Changes #13, #18, #19, #20, #22, #23, #24 (spec-side parts) and Change #16 (section 7.3 checks); new section per Change #13 -->
These are proposed edits to `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. This merge does not edit the spec; the edits are for the next consolidated spec revision. Each item names its target line or lines as they read on 2026-11-02. Items are labelled W1 to W16 so that they are not confused with the guard's cases.

<!-- Source: Change #13 rationale and Change #8; SPEC:54 no longer open -->
### W1. `SPEC:54`, section 2.1, term "Unattended mode"
- Replace the sentence "How the mode is selected (flag versus detecting the preamble) is open decision D1 in section 9; this spec is written for the recommended flag." with:
  > The mode is selected only by the flag (decision D1, section 9: option (c) as amended). No command detects Orca, its preamble or its environment. The worker session separately applies the brief guard (section 2.1, "Brief guard").

<!-- Source: Changes #12, #19, #22 -->
### W2. `SPEC:58`, section 2.1, term "Contract file"
- Replace "The file holds the command-side rules (WC-2, WC-4, WC-8 to WC-11, the flag parse rule and the person-mode refusal above) and the coordinator's rules (WC-6 and section 2.3, including its brief template)." with:
  > The file holds the command-side rules (WC-2, WC-4, WC-8 to WC-11, the flag parse rule, the person-mode refusal above and the nested propagation rule below), the worker session's brief guard and the never-as-worker list below, and the coordinator's rules (WC-6 and section 2.3, including its brief template and the template's guard line).

<!-- Source: Changes #9, #10, #18, #19, #20, #21, #22, #23 (INV-009, INV-018) -->
### W3. Section 2.1, three new terms inserted after `SPEC:58`
- Insert:
  > - **Brief guard** (worker session, from P1): it applies only in a session whose current prompt carries a live Orca preamble with Task and Dispatch IDs (see "Worker run"). Before invoking anything, the worker checks every `Command:` line of its brief (section 2.3, "Brief layout"), and only those lines. It decides case 3 from the command name alone. For the other cases it reads, as plain files, every existing copy of the command file: the project `.claude/commands/sc/<name>.md` in its worktree and `~/.claude/commands/sc/<name>.md`. It refuses, runs nothing, writes no contract, and sends `worker_done --outcome failed` with no `--report-path` and a body starting `guard refused:` when: (case 1) every existing copy has an `## Unattended mode` section and the line lacks a standalone `--unattended` (`guard refused: brief lacks --unattended`); (case 2) no existing copy has the section and the line has the flag (`guard refused: loaded command has no Unattended mode section (not converted at this phase, or the loaded copy is stale)`); the copies disagree (`guard refused: command copies disagree (stale copy): <paths>`); (case 3) the command is on the never-as-worker list. A command invoked by another command, through the Skill tool or the Agent tool, is never checked; the nested propagation rule governs it. The guard checks once, before the first run: a WC-3 re-invocation keeps every token of the brief's `Command:` line, `--unattended` included, and only adds the answer.
  > - **Never-as-worker list**: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard` (section 4), plus `/sc:pr-submit` while the answer to D3 keeps it off workers. The list changes only when section 4 or D3 changes, never per phase. If D3 adds a worker route for pr-submit, D3 also states how that route passes the brief guard.
  > - **Nested propagation rule**: under `--unattended`, a command that invokes another `/sc:` command or protocol skill, through the Skill tool or the Agent tool, passes `--unattended` when the invoked command accepts it at this phase, together with its own report directory `<caller report-dir>/nested/<command>-<n>/` (WC-4, WC-11). The caller lists the nested contract in its `artifacts`; only the top-level contract drives WC-5. When the invoked command does not accept the flag yet, that step must be gate-free per its section 3 row, or the caller skips it under `--unattended` and records the skip in its contract. Each command's `## Unattended mode` section names its nested invocations.

<!-- Source: Change #13 (Round 1 and Round 2 debate, A-005) -->
### W4. `SPEC:79`, section 2.3, first sentence of the brief list
- Replace "the exact command line including `--unattended` and every flag section 3 lists as required" with:
  > the exact command line, including `--unattended` where the command accepts it at this phase, and every flag section 3 lists as required, written as a `Command:` line in the layout below

<!-- Source: Changes #12, #20, #21 (REVIEW M14), #23 (INV-002, INV-018) -->
### W5. Section 2.3, new paragraph "Brief layout" inserted after `SPEC:79`
- Insert:
  > **Brief layout.** The brief puts the preamble-facing instructions and the guard line before the commands, and gives each command its own labelled `Command:` line in run order (for example `Command: /sc:load ...`, then the converted command), so the Task text never starts with `/sc:`. Guard line: `Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".` The coordinator decides whether a `Command:` line carries `--unattended` by the guard's own test, run on the copies the worker will see (the target worktree's project `.claude/commands/sc/` copy and `~/.claude/commands/sc/`), not on its own copy. A WC-3 re-invocation keeps every token of the `Command:` line and only adds the answer.

<!-- Source: Change #23 (INV-017; REVIEW M1) and Change #24 (K3) -->
### W6. Section 2.3, "Reading a result", new bullet after `SPEC:84`
- Insert:
  > - No contract, and a `worker_done --outcome failed` body that starts `guard refused:`: a brief-guard refusal; nothing ran. The coordinator fixes the brief in a new Task (WC-6), never re-creates it unchanged, and allows at most 2 brief fixes for the same work (3 attempts); a third refusal escalates to the person.

<!-- Source: Change #20 (REVIEW M6) -->
### W7. Section 2.3 worked example, `SPEC:90` and `SPEC:93`
- Replace step 1 (`SPEC:90`) with:
  > 1. Task T1 brief, in the brief layout above: the guard line, `On a blocked gate: report blocked`, then `Command: /sc:tdd "auth" --unattended --output .dev/tdd/auth-1/tdd.md --report-dir .dev/tdd/auth-1/`.
- Replace step 4 (`SPEC:93`) with:
  > 4. The coordinator creates Task T2 with `task-create --spec` and a brief in the same layout: the guard line, `replaces T1`, then `Command: /sc:tdd "token-based login service: session issue, refresh and revoke" --unattended --output .dev/tdd/auth-2/tdd.md --report-dir .dev/tdd/auth-2/`. T1's contract stays untouched in `auth-1/`.

<!-- Source: Change #20 (REVIEW M6) -->
### W8. AC-2.2 (`SPEC:264`) and AC-2.6 (`SPEC:268`) briefs
- Append to the Check cell of each row:
  > Every brief in this check uses the section 2.3 brief layout, with the command on a `Command:` line.

<!-- Source: Change #13 (REVIEW M7) -->
### W9. `SPEC:329`, D1 option (a)
- Replace "- (a) **Explicit `--unattended` flag in the brief (recommended).** The coordinator writes it into every worker's command line; a person never types it." with:
  > - (a) **Explicit `--unattended` flag in the brief.** The coordinator writes it into a worker's command line where the command accepts it at this phase (section 6); a person never types it.
- The rest of the bullet (the example and the parse-rule sentence) is unchanged.

<!-- Source: Changes #8 and #14 -->
### W10. `SPEC:330`, D1 option (b)
- Replace the bullet with:
  > - (b) **Detect Orca.** The command checks `ORCA_TERMINAL_HANDLE` or looks for a worker preamble in the conversation. The environment route is closed: Orca's identity error text ties the variable to any live Orca terminal (`CAPS:149`), and it was observed set in a dispatched worker (`CAPS:151`), so it cannot tell a worker from a person's own Orca tab. This is inferred, not observed in a person's tab (item 13). Preamble detection depends on the model reading prose, cannot be tested mechanically, cannot reach a command's Agent-tool subagents, and puts Orca-specific branching into commands (SA-2, non-goal 1).

<!-- Source: Base (Variant 3 position) as amended by Changes #9, #10, #11, #18, #19, #21, #23 -->
### W11. `SPEC:329-331`, D1 option (c) and the recommendation
- Insert after the (b) bullet (`SPEC:330`):
  > - (c) **Flag plus a worker-session brief guard (recommended).** Commands behave exactly as in (a). From P1 the worker session checks every `Command:` line of its brief before running any, and refuses with `worker_done --outcome failed` (body starting `guard refused:`), running nothing, when the flag is missing while every existing copy of the command file has an `## Unattended mode` section, when the flag is present while no copy has it, when the copies disagree, or when the command is on the never-as-worker list (section 2.1, "Brief guard"). A forgotten flag becomes a named failure instead of a silent stall that Orca reports as healthy (`CAPS:52`, `CAPS:73`). Removing the guard parts returns (a).
- Replace `SPEC:331` "- Recommendation: (a)." with:
  > - Recommendation: (c), that is (a) plus the brief guard, as amended in `.dev/orca-command-refactor/decisions/D1/debate/adversarial/merged-output.md`.

<!-- Source: Change #8 (REVIEW M3) -->
### W12. `SPEC:395`, UNVERIFIED item 13
- Append:
  > D1 no longer depends on it: no option the spec keeps reads the variable. The reading that it marks any live Orca terminal is inferred from `CAPS:149` plus one observation (`CAPS:151`); this item stays open.

<!-- Source: Changes #18 (i), #20, #24 (UNVERIFIED points carried as the plan marks them; REVIEW M6, M9) -->
### W13. UNVERIFIED items, new items 24-27 after `SPEC:405`
- Insert:
  > 24. Which copy Claude Code loads when both the project `.claude/commands/sc/<name>.md` and `~/.claude/commands/sc/<name>.md` exist. The brief guard reads every copy and refuses when they disagree, so it does not depend on the answer.
  > 25. Whether Orca's Task text for a Claude worker could still start with the brief's first `/sc:` line despite the brief layout (section 2.3).
  > 26. Whether a command the worker invokes from a mid-brief `Command:` line counts as run directly at the top level (WC-7, AC-0.4). Resolve: AC-0.4's step-5 transcript check.
  > 27. Whether Orca's `--setup run` performs `make sync-dev` in a new worktree (`.dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md:42`). 7.2 step 1 runs it explicitly unless this is confirmed.

<!-- Source: Change #24 (K1, revised for REVIEW B3) and Change #18 (iv) -->
### W14. `SPEC:235-236`, section 7.2 disposable worktree and step 1
- Replace `SPEC:235` with:
  > For each command under test, the coordinator runs the steps below with one worker in a fresh disposable worktree that holds the phase's edits, so step 6 can attribute every change to the worker under test (WC-11 allows sharing a worktree in normal use; the check does not). Orca creates worktrees from a git base, and the phase's edits are uncommitted until the user asks (`CLAUDE.md:37`), so before the check the phase's edits are committed to the feature branch or a scratch branch with the user's authorization (a decision point each phase). The disposable worktree is created by Orca at Orca's default path from that branch, never under `.dev/worktrees/`. `make sync-dev` is run inside it before dispatch unless Orca's `--setup run` is confirmed to do it (UNVERIFIED item 27); `~/.claude` is never reinstalled for this check. After step 7 the worktree is removed with `orca worktree rm`, because orchestration verbs never delete worktrees (`CAPS:115`).
- Replace step 1 (`SPEC:236`) with:
  > 1. `ORCA orchestration task-create --spec "<brief per section 2.3>" --json`. Then either `ORCA orchestration worker-start --task <task_id> --worktree new-top-level --base-branch <branch> --setup run --agent claude --json`, when the setup is confirmed to run `make sync-dev`; or create the worktree first with `ORCA worktree create` from `<branch>`, run `make sync-dev` inside it, and start the worker with `--worktree path:<worktree>`. For a command that accepts `--unattended` at this phase, confirm before dispatch that every existing copy of its file (`<worktree>/.claude/commands/sc/<name>.md` and `~/.claude/commands/sc/<name>.md`) has its `## Unattended mode` section. **Pass:** exit 0 and `state: ready` (`CAPS:46`).
- This removes the UNVERIFIED question whether Orca accepts a worktree it did not create.

<!-- Source: Change #16, extended by Changes #22 and #23 (INV-008, INV-010, INV-023; REVIEW M5) -->
### W15. Section 7.3 and 7.4, new and extended checks
- AC-1.1 (`SPEC:257`), append to the Check cell:
  > The test also asserts that `WORKER-CONTRACT.md` states the brief guard (its four refusal conditions and reason texts), the never-as-worker list and the nested propagation rule; that the brief template carries the guard line before the `Command:` lines; and that brainstorm's `## Unattended mode` section turns automatic research enrichment off under `--unattended`.
- AC-1.3 (`SPEC:259`), append to the Check cell and the Pass cell:
  > Check: also one flagless run of a converted P1 command in the coordinator session with `WORKER-CONTRACT.md` loaded (manual). Pass: that run shows today's behaviour, with no brief-guard refusal.
- New row after AC-1.6 (`SPEC:262`):
  > | P1 | AC-1.7 | Brief-guard refusals (section 2.1), one 7.2 live check per case, with steps 3-4 replaced by this row's conditions. Case 1: a P1 command with its report directory and no `--unattended` (for example `/sc:analyze <path> --report-dir <dir>`). Case 2: `<command with no section at this phase> --unattended --report-dir <dir>`. Case 3: `/sc:help` in the disposable worktree, never `/sc:pm`, `/sc:agent`, `/sc:git` or `/sc:pr-submit`. | For each: no file written (step 6 empty); `worker_done --outcome failed` with no `--report-path` and a body starting `guard refused:`. For case 3, the step-5 transcript also shows the command was never invoked. |
- AC-2.1 (`SPEC:263`), append to the Check cell:
  > and, for each nested invocation a command's section names (workflow's reflect step, `sk/sc-workflow-protocol/SKILL.md:58`; brainstorm's research enrichment, `sk/sc-brainstorm-protocol/SKILL.md:185`), that it passes `--unattended` and `<caller report-dir>/nested/<command>-<n>/`
- New row after AC-2.6 (`SPEC:268`):
  > | P2 | AC-2.9 | Brief guard, discriminating run: `/sc:tdd "auth" --output <file> --report-dir <dir>` (bare topic, no `--unattended`) as a 7.2 live check, with steps 3-4 replaced by this row's conditions | Case 1 refusal: no file written (step 6 empty); `worker_done --outcome failed` with no `--report-path` and a body starting `guard refused:`; step 2 never shows `agentWait`. Without the guard this brief stalls on tdd's gate. |
- Section 7.4 (`SPEC:291-311`), insert rows:
  > | Brief guard (section 2.1) | AC-1.1 (static), AC-1.2 (false refusals), AC-1.7, AC-2.9, AC-1.3 (manual part, coordinator session) |
  > | Nested propagation rule (section 2.1) | AC-2.1 |

<!-- Source: Change #22 (revised for REVIEW B2) -->
### W16. Phase 2 edits for workflow and brainstorm
- `SPEC:183`, P2 row, append to the Commands cell:
  > ; plus `## Unattended mode` section edits for workflow (its reflect step passes `--unattended` and a nested report directory) and brainstorm (its automatic research enrichment does the same instead of being off), both of which accept the flag from P1
- `SPEC:107`, brainstorm row, replace the Small fix cell "None" with:
  > Under `--unattended`, automatic research enrichment (`sk/sc-brainstorm-protocol/SKILL.md:185`) is off (P1); from P2 it passes `--unattended` and a nested report directory (P2)
- `SPEC:115`, workflow row, append to the Small fix cell:
  > ; from P2, the reflect step (`sk/sc-workflow-protocol/SKILL.md:58`) passes `--unattended` and a nested report directory (P2)
