# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel statements, Round 2 sequential rebuttals A, B, C, D, E), plus Round 2.5 invariant probe. Round 3 skipped: depth=standard.
- Convergence achieved: 96% on diff points (24 of 25)
- Convergence threshold: 80%
- Taxonomy coverage: L1 (S-003, S-004), L2 and L3 all covered; no forced round needed.
- Invariant gate: BLOCKED_BY_INVARIANTS (5 HIGH UNADDRESSED: INV-006, INV-024, INV-025, INV-026, INV-032; see `invariant-probe.md`)
- Final status: BLOCKED_BY_INVARIANTS at max rounds for depth standard. Per the no-convergence rule, the base is force-selected by score (Step 3) and the five HIGH items become mandatory changes in the refactor plan (Step 4); flagged for user review.
- Focus areas: All
- Advocate count: 5 (one per variant; each a general-purpose Claude subagent with a persona: A architect+analyzer, B backend+analyzer, C devops/architect+analyzer, D security+analyzer, E qa+analyzer)
- Agent failures: none. Tool note: named advocates could not be spawned from a teammate session, so advocates were spawned unnamed and resumed by agent ID for Round 2.

## Orchestrator verification of new Round 2 evidence
Re-read by the orchestrator before scoring (2026-11-02):
- B's N1 (implement revert reaches other writers' files): `src/superclaude/skills/sc-implement-protocol/refs/retry.md:201-208` (domain = whole-worktree diff minus run-own and `.dev/` exclusions) and `:220` (restore or delete each domain path). Confirmed.
- C's M1 (pr-submit binds to and commits in the PR-head checkout): `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:268,274,318`. Confirmed.
- E's N1 (implement's private-index `git add -A`): `sc-implement-protocol/SKILL.md:111`, `refs/retry.md:236-241`. Confirmed. E's N3 MDTM `git add -A`: `src/superclaude/skills/task-builder/SKILL.md:2237`. Confirmed.
- Fault-finder INV-006: `sc-implement-protocol/refs/managed-workspace.md:85` ("non-cooperating checkout writers ... unsupported; ... The retry ladder reverts a non-cooperating writer's edits"). Confirmed.
- Fault-finder INV-024: `git add .dev/tasks` instructions at `sc-workflow-protocol/SKILL.md:28` and `sc-implement-protocol/refs/managed-workspace.md:36`. Confirmed. Correction: the probe also lists reflect, but `sc-reflect-protocol/SKILL.md:1561` says "Reflect does NOT `git add` moved files. Operator stages and commits", so reflect is not a staging case.
- Fault-finder INV-032: reflect's `git worktree remove --force` at `sc-reflect-protocol/SKILL.md:253`. Confirmed.
- `worker-retain --help` line 5: "Keep one supervised worker terminal live for debugging" (C's concession 3). Confirmed.

## Round 1: Advocate Statements
Full statements follow, verbatim from the round files.

### Round 1, advocate A (source: round1-advocate-a.md)

### Round 1 advocate: variant 1 (option A, coordinator runs every git and GitHub action in its main chat)

Persona: architect (structure, dependencies, long-term impact) plus analyzer (evidence quality).
Date: 2026-11-02. Citation keys as in `variant-1-original.md`.

**Verification note.** Every repo `path:line` and Orca guide line used below was re-read in this round (sed/awk on the files; `orca-ide skills get orchestration [--reference references/<name>.md] | cat -n`). GITDEMO (the index.lock and per-worktree index/HEAD demo) is variant 1's own recorded run; I did not re-run it, because this round forbids mutating git commands, even in a scratch repo. Its claims match documented git behaviour, but in this round they are **UNVERIFIED (not re-run)**. Checked this round: this clone has no active git hooks (`$(git rev-parse --git-common-dir)/hooks` holds only `*.sample`; `core.hooksPath` unset).

#### Position summary
Option A is the right **default and the right rule for the spec's current phases**: one session (the coordinator, where the person gives instructions) holds the only git index writer per worktree and performs every outward action. That needs no command changes and fits Orca's shared-worktree default and the repo's PR rules exactly. Option E's worker-commit lane is a legitimate **later extension**. It earns its place only once #326's per-task commit step (K3) exists. Until then it adds a second rule set for little gain beyond what A already delivers.

#### Steelman of each opposing variant

##### B (workers run their own git)
**Strongest version:** only the worker knows when a task inside a long `/sc:implement` run ends. Only a worker can therefore make the per-task commits the #326 owner asked for. Those commits make finished work survive a crash. A commit between tasks keeps the retry ladder valid, because each task records its own HEAD baseline at start (`src/superclaude/skills/sc-implement-protocol/SKILL.md:114`, verified: "write `<retries>/T<id>/q0-head` ... before the start line is appended"), and the ladder checks only that baseline (`refs/retry.md:41`, verified). With one worker per linked worktree, each worker has its own index and HEAD (GITDEMO, UNVERIFIED this round), so workers never contend. The worker also wrote its own files, so it can stage exact paths without reconstructing them.
**What it gets right:** the per-task timing argument is correct and is A's real gap (V1 weakness 1). EVAL F0 also shows the spec's "workers make no commits" wording rests on a run-local README rule, not repo policy (`.dev/orca-command-refactor/review/issue-326-evaluation.md:50`, verified).
**Critique:** B is safe only with one committing worker per worktree. V2 states this itself ("B forces a worktree per committing worker", V2 Correctness). Orca's placement default runs against it: "Use the current or an exact existing workspace by default. Create a worktree only when the user requested one or a concrete checkout or filesystem conflict makes sharing unsafe" (`[G:pl] 8-11`, verified). B also moves pushes, PRs and comments into workers, which the spec's WC-9 is built to switch off (`SPEC:73`, verified). It needs D3 (b), which the spec does not recommend (`SPEC:341-343`, verified). Merges still fall back to a single owner (V2 weakness 4), so B is A plus extra machinery, never a replacement for A.

##### C (dedicated long-lived git session as an Orca worker)
**Strongest version:** C gives A's single-writer property *and* frees the coordinator from `/sc:pr-submit`'s attended waits (600 s default per wait, `src/superclaude/commands/pr-submit.md:49`, verified). Orca serializes git actions for free, because a terminal that already owns an active Dispatch rejects a second one (`[G:rc] 108`, verified: "a target terminal that already owns an active Dispatch"). Each action becomes its own Task, Dispatch and `worker_done`, which gives the best per-action audit record. C is also the only honest orchestration-level reading of #326's "central relay", because commands cannot call another session (`SPEC:72`, verified, WC-8).
**What it gets right:** the per-action audit trail is genuinely stronger than A's single transcript. The serialization mechanism is real.
**Critique:** (1) Keeping the session alive between actions depends on user permission. Reuse needs "immediate follow-up work" (`[G:cl] 48-50`, verified). Otherwise "Retain only when the user explicitly wants the settled terminal kept live" (`[G:rc] 157`, verified). Without that, C degrades into a fresh 60 s readiness start per git action (`CAPS:44`, verified). (2) PRs in the git session are D3 (b), against the spec's recommendation (`SPEC:341-343`). The section 3 pr-submit row turns operator HALTs into `blocked` (`SPEC:137`, verified: "operator HALTs resolve as blocked"). So the attended remediation loop loses the person it was designed for. (3) Authorization takes one hop through a brief. (4) It does not solve per-task commits (V3 weakness 4). (5) The worker contract forbids a standing loop Task (`[G:wc] 77-80`, verified: "After `worker_done`, end the dispatched turn and idle. Do not poll"). So the "long-lived" property exists only through per-action reuse, which brings back problem (1).

##### D (coordinator's Agent-tool subagent runs git)
**Strongest version:** D keeps A's ownership and single-writer correctness and moves only the noisy part (diff reading, `git status`, commit-message drafting) into a disposable context. It needs no Orca overhead and costs one agent definition. Agent-tool subagents are outside Orca's depth fence (`CAPS:155`, verified).
**What it gets right:** it is the cheapest valid fix for A's main cost, coordinator context load. It changes nothing about who decides.
**Critique:** it cannot run the actions that matter most. `/sc:pr-submit` "MUST run in the main orchestrating session ... Do NOT run it inside an Agent-tool subagent" and must "Never hand a side effect to a background shell, detached loop, or subagent" (`src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:47-49,82-84`, verified). Its "narrow tool list" claim is unsupported: no evidence shows Bash can be limited to git subcommands (X-005; V4 itself marks it UNVERIFIED). When the user asks for Orca provenance, Orca's guide says "Never substitute a non-Orca subagent tool when Orca orchestration provenance was requested" (`[G] 46-47`, verified). D therefore makes the most sense as an **implementation detail of A** (the coordinator may delegate commit-message drafting), not as a separate ownership model.

##### E (hybrid: sole-writer workers may commit locally; coordinator owns all outward actions)
**Strongest version:** E keeps everything A gets right about outward actions and the shared worktree. It adds the one thing A cannot do: a worker that is the *sole writer* in its own worktree may commit locally between tasks, under a quoted user instruction, and never pushes. This matches the repo's own words, "Commit locally, show your lead what changed, and push only when they say go" (`src/superclaude/core/HOW-WE-WORK.md:282`, verified). It matches the evaluation's F1 boundary (commit between tasks, never inside a task's window, `issue-326-evaluation.md:51`, verified). With no commit authorization in the brief, E reduces exactly to A. It is also the only variant that states the F3 cleanup guard explicitly.
**What it gets right:** the per-action ownership table is the clearest structure in the set. Its outward-action column is identical to A.
**Critique:** (1) E's distinctive lane depends on K3, which does not exist yet. V5's own Implementation cost says "until it exists a worker commits only through steps its brief adds after the command finishes". That is a single end-of-run commit, which A's coordinator can also make, with direct authorization. (2) E has two rule sets for one action (local commit) and needs a test for each (V5 weakness 1). (3) The sole-writer condition is a placement fact that only the coordinator knows (A-003), so the coordinator still carries the safety check. (4) Shared refs: implement pins live under `refs/superclaude/implement/<slug>/T<id>` (`SKILL.md:113`, verified). Refs are shared across linked worktrees (GITDEMO, UNVERIFIED this round). V5 itself marks two runs of the same plan in two worktrees as UNVERIFIED.

#### Strengths claimed

1. **Correct under Orca's default placement, with no new placement rule.** Orca places workers in the current workspace by default (`[G:pl] 8-11`, verified; restated at `CAPS:115`, verified). In that layout any second git writer collides on `index.lock`, and any commit moves the shared HEAD. That halts a running `/sc:implement` task with `head-moved` (`refs/retry.md:41,44`, verified: check 3 "HEAD has not moved", and the halt list includes `reason=head-moved`). A is the only variant whose correctness holds in the default layout without adding a condition. B needs a worktree per committer. E needs the sole-writer test. C and D are single-writer only because they copy A's rule.
2. **Authorization and action sit in the same session.** The repo commits only when asked (`CLAUDE.md:37`, verified: "Staging is not committing: commit only when asked"). It pushes only after approval (`HWW:282`, verified). The person speaks to the coordinator, so under A no brief stands between the instruction and the action. D4 (a) exists *because* a brief is a lossy hop (`SPEC:346`, verified: the coordinator must quote the instruction). Under A, D4's question never arises for git, which is D4 (b) for outward actions (`SPEC:347`, verified).
3. **Exact fit with the PR rules and the spec's own D3 recommendation.** Every PR goes through `/sc:pr-submit --monitor 3` (`CLAUDE.md:50`, verified). That skill must run top-level and keep every side effect in that session (`sc-pr-submit-protocol/SKILL.md:47-49,82-84`, verified). The spec recommends D3 (a), coordinator or person only (`SPEC:341-343`, verified). A complies with no changes. C and B need D3 (b), and D cannot comply.
4. **Lowest implementation cost and no conflict with SA-4.** WC-9 already switches off every outward default in workers (`SPEC:73`, verified). SA-4 allows only additive edits to commands in Phases 1-3 (`SPEC:172`, verified). A needs spec wording only: section 2.3 coordinator duties and the `/sc:git` row (`SPEC:156`). B and E's worker lane add command behaviour (a commit step, stale-lock handling, SHA contract fields) or depend on K3 (`issue-326-evaluation.md:63`, verified).
5. **Quiescence is easiest to enforce where the placements are made.** The coordinator writes each brief's worktree placement (`SPEC:79`, verified: the brief states "the worktree placement"). Under A, the session that knows which workers run where is the same session that commits, so the rule "never commit in a worktree while an `/sc:implement` worker runs there" (U-008) needs no cross-session state.
6. **Smallest blast radius on crash.** A worker crash leaves no git state to repair. Only one session can leave a stale lock, and that session's transcript says what it was doing. Worker retries stay plain new Tasks (WC-6, `SPEC:70`, verified) with no stale-lock preamble.
7. **A absorbs D cleanly as an internal optimisation.** Because ownership stays in the main chat, A can delegate diff reading or message drafting to an Agent-tool subagent (D's benefit) while keeping pr-submit, pushes and comments top-level. A + D-as-helper is a strict improvement on A without a new ownership model.

#### Weaknesses identified in other variants

1. **B is unsafe by default and incomplete by design.** In the default shared worktree (`[G:pl] 8-11`), B's commits collide on the lock, `git add -A` sweeps other workers' files, and every commit halts sibling implement tasks with `head-moved` (`retry.md:41,44`). V2 concedes all three. Merges still need a single owner (V2 weakness 4). Outward actions from workers re-open what WC-9 closes (`SPEC:73`).
2. **B and C weaken the pr-submit operator loop.** Running pr-submit as a worker means "operator HALTs resolve as blocked" (`SPEC:137`, verified). The skill's attended poll loop was designed for a person in the session (`SKILL.md:47-49`). Moving it to a session nobody watches turns operator decisions into failed Tasks.
3. **C's persistence is user-gated and its idle rule forbids the obvious shortcut.** Retention needs an explicit user wish (`[G:rc] 157`). Reuse needs immediate follow-up work (`[G:cl] 48-50`). A standing poll Task breaks the worker contract (`[G:wc] 77-80`). V3 also marks as UNVERIFIED both how reuse injects the next Task into a running Claude session and what final release of a reused terminal does (`[G:rc] 160-161`, verified: "Reused ... terminals are retained").
4. **D cannot own what matters and leaves no Orca record.** pr-submit is barred from subagents (`SKILL.md:47-49,82-84`). Subagents are not Tasks or Dispatches (`CAPS:155-158`, verified). Where provenance is requested, Orca forbids substituting a non-Orca subagent (`[G] 46-47`). The narrow-tool claim is unverified (X-005).
5. **E's distinctive lane is latent today and doubles the rule surface.** Without K3 (`issue-326-evaluation.md:63`), E's worker commits happen only "through steps its brief adds after the command finishes" (V5 Implementation cost). That is one end-of-run commit, which A also provides. The added cost is a second commit owner, a sole-writer predicate the worker cannot check itself, and a shared-refs slug condition V5 marks UNVERIFIED.
6. **Every non-A option adds an authorization hop.** B, C, D and E's local lane all depend on a brief or prompt that quotes the user (`SPEC:346`). A brief cannot change after creation (`SPEC:70`, verified: "A Task's brief cannot change after creation"). If the person narrows or revokes an instruction mid-run, the worker still acts on the old brief until a new Task replaces it. Under A, the revocation takes effect at the coordinator's next action.

#### Concessions

1. **No per-task commits inside one `/sc:implement` run.** The coordinator sees only the run's single `worker_done` (`[G] 88-90`, verified: sent "exactly once"). This is A's real gap against the #326 owner's request. It can be closed only by B or E's worker lane once K3 exists.
2. **The "repo forbids worker commits" premise is wrong.** EVAL F0 shows the spec's `/sc:git` row cites the run-local README rule, not repo policy (`issue-326-evaluation.md:50`, verified). The repo allows a local commit when asked (`CLAUDE.md:37`; `HWW:282`). A's case must rest on correctness and authorization quality, not on a prohibition.
3. **Coordinator context load and pr-submit blocking are real costs.** Waits run up to 600 s each (`pr-submit.md:49`). Durable message queueing (`[G] 120-124`, verified: `check` "replays that batch until acknowledged") prevents loss but not delay. C solves the delay and A does not. A's mitigation is D3 (a)'s ordering (pr-submit after workers finish, `SPEC:341`) plus D-style subagents for diff reading.
4. **C's audit trail is better per action.** One Task, brief, `worker_done` and contract per git action is a stronger record than A's transcript plus `git log`.
5. **Orca's review-ownership rule cuts against an unnamed coordinator.** "If the user's plan names a next owner, post-review fixes and PR preparation remain with that owner; the coordinator routes and synthesizes" (`[G:cl] 62-65`, verified). A is clean only when the user's plan names the coordinator as git and PR owner, so the spec should say the coordinator brief template records that.
6. **A's "same session" advantage depends on an attended coordinator (A-001).** If the person gives one instruction and leaves, A also acts on an up-front grant. A's remaining edge is then fewer hops and top-level pr-submit, not live consent.
7. **E is a superset of A.** With no commit authorization in a brief, E is A. My disagreement is about sequencing and rule-surface cost, not about E's eventual shape.

#### Shared-assumption responses (A-001..A-005)

| ID | Response | Reason |
|---|---|---|
| A-001 (coordinator is attended) | **QUALIFY** | True for the day-to-day flow V1 describes, and it is what gives A's "same session" claim its full force. When unattended, every option runs on an up-front grant. A then keeps only a smaller edge: fewer hops, revocation effective at the next action (briefs are immutable, `SPEC:70`), and pr-submit staying top-level where operator HALTs are not converted to `blocked` (`SPEC:137`). The spec should require the up-front grant to name the run, the actions and the branch. |
| A-002 (contract file lists are complete) | **QUALIFY** | Not safe to assume, and it hurts A most, because A's coordinator stages from lists it did not write. Remedy under A: before staging, compare `git status --porcelain` for the worktree with the union of settled contracts' `artifacts`, `report_path` and `--files-modified`. Stage only the intersection plus `.dev/tasks` (`CLAUDE.md:37`). Report every unlisted path instead of sweeping it. Never `git add -A` in a shared worktree. B and E have a genuine edge here, since the author stages its own files. |
| A-003 (quiescence is knowable) | **QUALIFY** | No Orca verb maps worktrees to running writers, but the coordinator writes every placement (`SPEC:79`), so it can keep that map. A is the variant where map-keeper and committer are the same session. Writers outside Orca (a person editing, another non-Orca session) are still invisible. The spec should require the coordinator to record placements and to check `worker-list` for active Dispatches in that worktree before committing. |
| A-004 (a commit does not rewrite files) | **QUALIFY** | Contradicted wherever the repo's file-fixing hooks are installed (`.pre-commit-config.yaml` `trailing-whitespace`, `end-of-file-fixer`, `ruff-format`; `default_stages: [commit]`, verified). They are not installed in this clone (verified this round). A limits the harm, because commits happen only at quiescent points when no worker is editing. B in a shared worktree is the worst case. The spec should require the committer to re-run `git status` after a hook-modified or failed commit and never retry with `--no-verify`. |
| A-005 (a standing instruction covers later commits) | **QUALIFY** | `CLAUDE.md:37` does not say. A standing instruction should cover only the run, branch and action it names ("commit after each passing task on branch X"), never pushes or PRs, which need their own instruction (`HWW:282`). Under A the person is in the coordinator's chat, so per-step confirmation stays cheap when they want it. Under brief-based options the scope is frozen at Task creation (`SPEC:70`). |

#### Per-point positions

| Point | Superior variant | One-line reason |
|---|---|---|
| S-001 | V5 (E) | The per-action owner/condition table is the clearest, most testable proposal form. |
| S-002 | V3 (C) | Only C verified Orca persistence mechanics (reuse, one active Dispatch per terminal, retention, idle rule). |
| S-003 | V1 (A) | Only A records the GITDEMO procedure the others rely on. |
| S-004 | V3 (C) | Only C reasons explicitly about #326's "central relay" and why commands cannot call it (`SPEC:72`). |
| C-001 | V1 (A) | Coordinator staging explicit paths at quiescent points is correct under Orca's shared default (`[G:pl] 8-11`); E adopts the same rule. |
| C-002 | V5 (E) | Only E allows per-task commits under safe conditions (sole writer, between tasks, quoted authorization), though it stays latent until K3. |
| C-003 | V1 (A) | Outward actions belong in the top-level session the person talks to (`SPEC:341-343`; `SKILL.md:47-49`); E is identical. |
| C-004 | V1 (A) | Direct authorization beats a brief that cannot change after creation (`SPEC:70`). |
| C-005 | V3 (C) | One Task, brief, `worker_done` and contract per action is the strongest audit record. |
| C-006 | V4 (D) | A subagent cuts coordinator context for commits without adding a new owner or Orca overhead; best used inside A. |
| C-007 | V5 (E) | A crash leaves a lock only in that worktree, and earlier commits survive. |
| C-008 | V1 (A) | Works in the default shared worktree with no placement precondition. |
| C-009 | V1 (A) | D3 (a) sequencing plus durable queueing keeps pr-submit attended. C's fix converts operator HALTs to `blocked` (`SPEC:137`). |
| C-010 | V1 (A) | Spec wording only; no command change against SA-4 (`SPEC:172`). |
| C-011 | V5 (E) | Only E states the F3 guard (no removal of unmerged or open-PR branches without instruction) and the `.dev/worktrees/` location (`CLAUDE.md:299-302`). |
| X-001 | V1 (A) | Same-session authorization cannot be lost or broadened in transit, and it takes effect on revocation. |
| X-002 | V3 (C) | Per-action Orca records beat a single transcript for audit (conceded). |
| X-003 | V1 (A) | Coordinator main chat matches D3 (a) and pr-submit's top-level rule; E and D agree. |
| X-004 | V1 (A) | A concedes the rule and resolves it by having the user's plan name the coordinator as PR owner (`[G:cl] 62-65`); B and C imply a fit without checking it. |
| X-005 | V1 (A) | A does not rest on an unverified Bash restriction; D's narrow-tool benefit is unsupported. |
| A-001 | V1 (A) | Even unattended, A keeps fewest hops and pr-submit top-level (E is equal on outward actions). |
| A-002 | V5 (E) | A sole-writer worker staging its own files avoids the incomplete-list risk; the coordinator cross-check covers the rest. |
| A-003 | V1 (A) | Placement map-keeper and committer are the same session. |
| A-004 | V1 (A) | Commits only at quiescent points mean a hook rewrite cannot clobber a live worker's edits. |
| A-005 | V1 (A) | Scope can be re-confirmed cheaply in the coordinator chat; brief-based scope is frozen at Task creation. |

**Tally:** A 15, E 5, C 4, D 1, B 0. On my reading the debate should converge on **A as the base rule**, adopting E's per-action table format and F3 guard now, and E's worker-commit lane as a K3-gated amendment. C's per-action audit and D's context isolation should be considered as coordinator-side techniques, not ownership changes.

### Round 1, advocate B (source: round1-advocate-b.md)

### Round 1 advocate: Variant 2 (option B, workers run their own git under brief rules)

- Persona: backend (data integrity, scalability, fault tolerance) plus analyzer (evidence quality)
- Date: 2026-11-02
- Inputs read in full: variant-1..5-original.md, diff-analysis.md
- Citation keys follow the variants (`SPEC`, `CAPS`, `EVAL`, `HWW`, `[G:cl]`, `[G:rc]`, `[G:pl]`, `GITDEMO`). Every repo path:line below was re-read in this session (batch read of cited ranges, 2026-11-02) unless marked UNVERIFIED.

#### Position summary

The only safe, durable way to get #326's per-task commits and per-experiment branches is for the worker that knows its own task boundaries and its own files to commit them, in a worktree where it is the only writer. That makes worker-owned local commits the core of the right answer. Variant B's extension of worker ownership to pushes, PRs and comments is weaker than its local-commit core, and on outward actions I defend B only for the parallel-PR-monitoring case that spec D3 (b) names (`SPEC:342`).

#### Steelman of each opposing variant

**V1 (A, the coordinator runs all git in its main chat).**
- Strongest form: authorization and action sit in one session. The person who says "commit" or "open a PR" says it to the session that does it, so no brief can lose, broaden or forge the instruction (V1 Safety). It is the only option that needs no command changes (WC-9 already turns outward defaults off, `SPEC:73`). It fits the one hard top-level constraint exactly: `/sc:pr-submit` must run in the main orchestrating session and never hand a side effect to a subagent (`src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:47-49,82-84`). It also contributed the two best pieces of evidence in the debate: the GITDEMO procedure (U-004) and the quiescence rule (U-008), based on `retry.md:41,44`.
- What it gets right: outward actions (push, PR, comments) belong in the attended top-level session. I accept this for the default case.
- Critique: see Weaknesses 1-4. In short, A cannot do the thing #326 asks for (V1's own weakness 1), and its correctness depends on two facts the coordinator cannot reliably have: a complete file list (A-002) and a live map of which worktrees have running writers (A-003).

**V3 (C, a dedicated long-lived git session as an Orca worker).**
- Strongest form: one serialized actor for all git, where each action is its own Orca Task with a brief, `worker_done` and contract. That gives the best per-action audit record (C-005), free serialization because a terminal with an active Dispatch rejects a second one (`[G:rc] 108`, per V3), and a place to run the long `/sc:pr-submit` loop without blocking the coordinator. It is also the most careful variant on Orca mechanics (U-001), and it reads #326's "central relay" correctly as a session the coordinator feeds, not something commands call (U-007).
- What it gets right: the audit trail argument, and the fact that the pr-submit loop should not freeze the coordinator.
- Critique: see Weakness 5. C keeps the long-lived session alive only by an explicit user retention request (`[G:rc] 157`, verified), does not solve per-task commits (V3 weakness 4), and has one serialized git actor for N experiment worktrees. That actor is a throughput bottleneck, and it is the coordinator-fed version of the same quiescence problem.

**V4 (D, the coordinator's Agent-tool subagent runs git).**
- Strongest form: A's single-writer correctness and direct authorization, with the diff reading and message drafting moved out of the coordinator's context at almost no cost (one agent definition) and no Orca overhead (no 60 s readiness start, no retention request).
- What it gets right: context isolation for the mechanical part of a commit is real and cheap.
- Critique: see Weakness 6. It cannot run `/sc:pr-submit` (`SKILL.md:47-49,82-84`, verified), so it covers only local commits. It leaves no Orca record, its narrow-allowlist benefit cannot be shown for Bash (X-005), and it inherits all of A's limits on per-task commits and quiescence.

**V5 (E, hybrid: sole-writer workers may commit locally, the coordinator owns every outward action).**
- Strongest form: E keeps B's correct core (worker-owned local commits, safe exactly when the worker is the sole writer in its worktree) and A's correct core (outward actions where the person gives the instruction and where pr-submit must run). Its per-action table (U-002) states owner and condition per action, which is testable. It adds a real data-integrity finding B missed: implement's Q0 pins live in `refs/superclaude/implement/<slug>/T<id>` (`src/superclaude/skills/sc-implement-protocol/SKILL.md:113`, verified), and refs are shared across linked worktrees (GITDEMO), so two runs need distinct slugs (U-003).
- What it gets right: almost everything B gets right, minus B's overreach on outward actions.
- Critique: see Weakness 7. E's shared-worktree commit row still depends on A-002 and A-003. It serializes PR monitoring through the coordinator. And E's own implementation note admits that, inside the spec's phases, per-task commits within `/sc:implement` exist only after K3 (V5 Implementation cost). That is the same gap B has, so on this point E is not ahead of B.

#### Strengths claimed

1. **Per-task commits that keep the retry ladder valid require the worker as committer.** The ladder runs only if "HEAD has not moved" since the task's Q0 (`src/superclaude/skills/sc-implement-protocol/refs/retry.md:41`); otherwise it halts `head-moved` (`retry.md:44`). Q0 writes `q0-head` at each task's start (`SKILL.md:114`). So a commit is safe exactly in the gap between one task's `complete` line and the next task's Q0. Only the process running the ledger can see that gap. The coordinator sees only the whole run's `worker_done` (V1 concedes this, its weakness 1). EVAL F1 reaches the same constraint from the protocol (`EVAL:51`). This is B's central claim, and C and D concede they do not solve it (V3 weakness 4; V4 inherits A).
2. **A sole-writer worktree removes index contention by construction, not by scheduling.** Each linked worktree has its own index and HEAD (`.git/worktrees/<name>/index`, `.../HEAD`; GITDEMO in V1 Self-check). Two workers in two worktrees cannot contend for `index.lock` or move each other's HEAD. A, C and D get single-writer safety by keeping one actor, which then has to know when each worktree is quiet (A-003). B gets it from the filesystem layout, which needs no runtime knowledge.
3. **The committer knows the exact file set.** The worker wrote the files, and in a sole-writer worktree `git status` shows only its own changes. B therefore does not depend on contract file lists being complete (A-002). A drive-by edit or a formatter rewrite is visible to the worker's own `git status` and can be reviewed before staging. Under A/C/D/E-shared, a file missing from `artifacts` / `--files-modified` is silently left out.
4. **Durability under crashes.** Work committed before a crash survives (U-005, B's contribution). A stale `index.lock` from a crashed worker stays in that worker's worktree only (separate index files, GITDEMO), so every other worker continues. Under A and D, a coordinator crash mid-commit leaves the lock in the shared worktree where every worker writes. For #326 this is the actual point: work is not lost "until all of the work is done in a tasklist" (owner comment, quoted in V2; the issue text itself is UNVERIFIED in this session, I did not run `gh`).
5. **Experiment branches scale with workers, not with one actor.** #326 F2 asks for parallel experiments in their own worktrees (`EVAL:52`). Under B, N experiment workers commit on N branches in parallel. Under A the coordinator commits in each worktree serially (V1 weakness 4). Under C one git session serializes all of them. Neither is unsafe, but both turn a parallel run into a serial git queue, and the queue grows with the number of experiments.
6. **Parallel PR monitoring is a real capability only B (and C, serially) can offer.** `/sc:pr-submit` waits run on a 600 s per-wait default budget (`src/superclaude/commands/pr-submit.md:49`, verified) over up to 2 rounds by default (`--max-rounds`, same table). D3 (b) exists precisely "so several PRs can be monitored in parallel" (`SPEC:342`, verified). For a run that ends with 3 experiment PRs, A/E monitor them one after another in the coordinator's chat. A worker is a top-level session, so pr-submit's top-level rule is met there (`CAPS:161`, verified). I claim this only for the case the spec names; see Concessions.
7. **B corrects a spec error that the A-leaning variants inherit.** The spec's `/sc:git` row says "workers make no commits or pushes" (`SPEC:156`, verified), citing the run-local `.dev/orca-command-refactor/README.md:31`. EVAL F0 shows that citation is this planning run's own worker rule, not repo policy. The repo rule is "commit only when asked" (`CLAUDE.md:37`) and HOW-WE-WORK permits "Commit locally" before an approved push (`HWW:282`) and says "a commit needs authorization" (`HWW:324`) (all verified; `EVAL:50`). A's premise that workers must never commit therefore has no repo-policy basis. A worker local commit under a quoted authorization is consistent with repo policy.
8. **Lowest coordinator context load for commits.** The coordinator reads SHAs from contracts, not diffs (C-006). This preserves the coordinator's main job (routing workers' messages), which `[G:cl] 62-65` says it should keep: "the coordinator routes and synthesizes" (verified).

#### Weaknesses identified in other variants

1. **A cannot deliver #326's per-task commits, by its own admission.** V1 weakness 1 and Correctness "Honest limit" say per-task commits wait for K3. The reason is structural, not a missing flag: the coordinator learns only of the run's `worker_done`, never of the `complete`-to-Q0 gap that `retry.md:41` requires. Even after K3 lands, K3 puts the commit step inside `/sc:implement` (`EVAL:63`, "the flag or step that performs per-task commits inside `/sc:implement`", verified), which means a worker commits. So under K3 A becomes B for local commits.
2. **A's correctness depends on a quiescence map Orca does not provide (A-003).** A's rule "never commit in a worktree while an `/sc:implement` worker in that worktree is running" (V1 Correctness) needs the coordinator to know which running Dispatch writes in which worktree. The diff analysis notes no Orca verb maps worktrees to running writers; the coordinator keeps that map from its own placements. One wrong placement record makes a coordinator commit halt a running task with `head-moved` (`retry.md:44`).
3. **A's explicit-path staging is only as good as the contract (A-002).** WC-4 lists `artifacts` as "every other file written" (`SPEC` WC-4 row, verified), but this is a worker's self-report. A missed file is left uncommitted, and the fallback, a broad `git add`, is exactly the cross-worker sweep A was built to avoid.
4. **A's foundation is partly a run-local rule.** A cites `SPEC:156` ("workers make no commits or pushes"), whose basis is `.dev/orca-command-refactor/README.md:31`, a rule for this planning run, not repo policy (`EVAL:50`, F0, verified). A also has to concede `[G:cl] 62-65` (verified): the coordinator "routes and synthesizes", and PR preparation stays with the owner the user's plan names. A puts every git action in the session Orca's guide says should mainly route.
5. **C pays Orca overhead for a serialized bottleneck.** Retention requires an explicit user request (`[G:rc] 157`, verified); reused terminals are among those that "are retained" at release (`[G:rc] 160-161`, verified), so the end-of-run cleanup of the git session is unclear (V3 marks it UNVERIFIED). Without retention, each action pays a fresh start of up to 60 s (`CAPS:44`, per V3; not re-read here, UNVERIFIED by me). One git session serving N experiment worktrees runs their commits and PR loops one after another, and it still needs D3 (b), the same non-recommended spec option B needs (`SPEC:343`), without B's parallelism. It does not solve per-task commits (V3 weakness 4).
6. **D covers only the cheapest part.** pr-submit cannot run in a subagent (`SKILL.md:47-49`, verified), so pushes, PRs, review replies and thread resolution fall back to A (V4 "What D costs"). D adds an authorization hop (the same objection A raises against B) without adding an Orca record (U-006). Its tool-restriction benefit cannot be shown for Bash (X-005). D inherits A's weaknesses 1-3 unchanged.
7. **E keeps the A-002/A-003 dependence for its shared-worktree row and serializes PRs.** E's row "Local commit of settled work in a shared worktree: Coordinator, at a quiescent point; stage only paths named in settled contracts" (V5 table) is A's rule with A's two unverified assumptions. E routes every PR through the coordinator, so three experiment PRs are monitored serially (pr-submit 600 s per-wait budget, `pr-submit.md:49`). E's own cost section concedes that per-task commits inside `/sc:implement` do not exist until K3 ("until it exists a worker commits only through steps its brief adds after the command finishes", V5 Implementation cost), so E's C-002 advantage over B is wording, not capability. E also carries two rule sets to state and test (V5 weakness 1).
8. **A, C, D and E all keep commits in the shared worktree, where a pre-commit hook rewrites shared files (A-004).** `.pre-commit-config.yaml` defines `trailing-whitespace` (line 9), `end-of-file-fixer` (line 11), `ruff-format` (line 111) with `default_stages: [commit]` (line 143) (all verified). Hooks are not installed in this clone (verified 2026-11-02: no non-sample hooks, no `core.hooksPath`). Where they are installed, a commit by the coordinator or git session rewrites files in the worktree every worker shares; under B the rewrite is limited to the committing worker's own worktree.

#### Concessions

1. **B is unsafe in the default shared worktree.** Workers share the current worktree by default (`CAPS:115`; `[G:pl] 8-11`, via `SPEC` WC-11 row, verified). Two committing workers there collide on `index.lock`, a `git add -A` sweeps another worker's files, and any commit moves the shared HEAD and halts running implement tasks (`retry.md:41,44`). B is correct only with one committing worker per worktree. Orca's guide says to create a worktree only "when the user requested one or a concrete checkout or filesystem conflict makes sharing unsafe" (`CAPS:115`, verified). A committing worker is such a conflict, but B does turn every committing worker into a worktree to create and later clean up (F3, `EVAL:53`).
2. **Outward actions belong to the coordinator by default.** pr-submit must run top-level (`SKILL.md:47-49`), D3 recommends (a), the coordinator or person (`SPEC:341,343`, verified), and WC-9 exists to keep outward defaults off in workers (`SPEC:73`). Comments, pushes and PRs from many workers multiply irreversible, visible actions across sessions with authorization scattered over briefs. I withdraw B's general claim to worker-owned pushes, PRs and comments. B keeps only the D3 (b) case: parallel PR monitoring, when the user asks for it and the section 3 pr-submit row is implemented (`SPEC:137`).
3. **Authorization reaches the worker second-hand.** The brief is coordinator-written. D4 (a) makes this acceptable only when the brief quotes the user's instruction naming the action (`SPEC:346`, verified). For a local, reversible, unpushed commit I judge this sufficient. For outward actions A's direct path is better.
4. **`/sc:implement` today forbids reading acceptance as commit authority.** `managed-workspace.md:63,67` (verified): a FINAL pass "is not a commit, PR, merge, release or human approval", and acceptance never "authorizes commit, PR, merge or release". Worker commits inside implement are therefore a protocol change (K3), and B's in-run per-task commit is not available in the spec's P1-P3 phases, which are additive only (`SPEC:172`, SA-4, verified). Until K3, a B worker can commit only in steps its brief adds after the command finishes, which is what E says.
5. **B missed the shared-refs hazard.** Implement's pins under `refs/superclaude/implement/<slug>/T<id>` (`SKILL.md:113`) are shared across linked worktrees (GITDEMO). Separate worktrees do not isolate refs, so B's "worktrees isolate everything" framing is too strong. E found this (U-003). Two runs of the same plan in two worktrees would share slugs (UNVERIFIED whether that collides in practice; I did not run it).
6. **No command has a stale-lock step today.** B's crash recovery needs a "clear stale lock after proving no git process runs" step that no command has (V2 Recovery). This is new behaviour and new risk: a wrong "no git process" judgment deletes a live lock.
7. **Highest implementation cost, and merges still need A.** Every committing command needs a commit step, a SHA field and a stale-lock rule; the coordinator needs a worktree-per-committer rule and a merge step done in its own chat (V2 Context load, Implementation cost). B alone is never a complete design.
8. **Net effect:** the defensible form of B is E's worker-commit row plus B's D3 (b) exception for parallel PR monitoring. I will argue in Round 2 that E's shared-worktree coordinator-commit row should be reduced in favour of "put committing work in its own worktree", which removes E's dependence on A-002 and A-003.

#### Shared-assumption responses (A-001..A-005)

| ID | Response | Reason |
|---|---|---|
| A-001 (coordinator session is attended) | QUALIFY | It is true when the person is present, and then A/E's direct path is best for outward actions. In a long unattended run, which is what Orca workers are for, the person gives one instruction and leaves, so every option, A included, acts on an up-front grant. A's "same session" advantage then shrinks to "the grant is in the coordinator's transcript rather than quoted in a brief". The spec should state that attended approval is required for outward actions and that local commits may run on a quoted up-front grant. |
| A-002 (contract file lists are complete) | REJECT as a basis for staging | WC-4's `artifacts` is a self-report (`SPEC` WC-4 row), and drive-by edits, formatter rewrites and generated caches are exactly what self-reports miss. Under a sole-writer worktree the committer does not need the list: `git status` in its own worktree is the complete, ground-truth set, reviewed before staging. Where the shared-worktree coordinator commit remains (A, C, D, E), the committer should compare `git status` with the contract and stop on any unexplained path rather than trust the list. |
| A-003 (quiescence is knowable) | QUALIFY | It is not knowable from Orca: no verb maps worktrees to running writers, so it holds only as far as the coordinator's own placement records are correct. Worker commits in a sole-writer worktree (B, E's worker row) do not need it, because the committer is the only writer by construction. It still matters for the coordinator's merges back into the shared branch under every option, B included. |
| A-004 (a commit does not rewrite files) | QUALIFY | Verified true in this clone (no hooks installed, checked 2026-11-02) and false wherever `pre-commit install` has run (`.pre-commit-config.yaml:9,11,111,143`, verified). Under B the rewrite or hook failure lands only in the committing worker's own worktree, and the worker sees it and can re-stage. Under shared-worktree commits it can rewrite files other workers are editing, or fail mid-run. Every option should treat a hook rewrite or failure as a stop-and-report, not a retry. |
| A-005 (standing instruction covers later commits) | QUALIFY | B depends on it most, so B must scope it. `CLAUDE.md:37` ("commit only when asked", verified) does not say whether a standing instruction covers future commits. Proposal: a standing grant covers local commits only, only for the named Task or run, only on the named branch, and is quoted verbatim in the brief. It never covers push, PR or comments, which need their own instruction (D4 (a), `SPEC:346`). Local commits are reversible and invisible until pushed, so a scoped standing grant is proportionate; an outward action is not reversible, so it is not. |

#### Per-point positions

| Point | Superior variant | One-line reason |
|---|---|---|
| S-001 Proposal form | V5 (E) | A per-action table with owner and condition is testable; prose proposals (B included) leave conditions implicit. |
| S-002 Orca-mechanics coverage | V3 (C) | Only V3 verified reuse, serialization, retention and depth against the Orca guide; B has none and should borrow it for worktree placement and cleanup. |
| S-003 Evidence appendix | V1 (A) | V1 alone records the GITDEMO procedure that every other variant, B included, relies on. |
| S-004 #326 relation | V3 (C) | V3's explicit relay analysis is the clearest treatment, although B and E deliver more of #326's substance (per-task commits). |
| C-001 Who commits settled work in a shared worktree | V5 (E) | B's answer ("give every committer its own worktree") avoids the case rather than handling it; E covers both cases. Round 2: I will argue E's shared row should be the exception. |
| C-002 Per-task commits inside `/sc:implement` | V2 (B), tie with V5 | Only the worker sees the `complete`-to-Q0 gap (`retry.md:41`, `SKILL.md:114`); E adopts B's rule with the same batch exclusion (`SKILL.md:97`). |
| C-003 Owner of push, PR, replies, comments | V5 (E) | The top-level rule (`SKILL.md:47-49`), D3 (a) (`SPEC:341`) and WC-9 favour the coordinator; B keeps only the D3 (b) parallel-PR exception. |
| C-004 Authorization path | V5 (E) | Direct for outward, quoted-brief for reversible local commits matches the risk of each action. |
| C-005 Audit trail | V3 (C) | One Task, brief, `worker_done` and contract per action is the most complete record; B's is scattered across briefs. |
| C-006 Coordinator context load | V2 (B) | The coordinator reads SHAs, not diffs, and keeps its routing role (`[G:cl] 62-65`); merges remain its cost. |
| C-007 Crash mid-commit | V5 (E) | Same containment as B (lock only in that worktree, earlier commits survive) plus an explicit "retry Task checks first" rule. |
| C-008 Worktree layout required | V5 (E) | Sole-writer worker commits plus a coordinator-only rule for shared worktrees avoids B's blanket worktree-per-committer cost. |
| C-009 pr-submit loop blocking the coordinator | V2 (B) | Under D3 (b), workers run several PR loops in parallel (`SPEC:342`); C unblocks the coordinator but serializes; A/E block it. |
| C-010 Implementation cost | V1 (A) | Wording only; B is the most expensive (command steps, K3, stale-lock rule, merge step). |
| C-011 Run worktree and branch creation and removal | V5 (E) | Only E makes it explicit, with the F3 guard (`EVAL:53`); B leaves it implicit despite creating the most worktrees. |
| X-001 Is a quoted brief enough for a worker's local commit? | V5 (E) | Yes for reversible, unpushed local commits (consistent with `CLAUDE.md:37`, `HWW:282,324`, `EVAL:50` F0); no for outward actions, where A's direct path is better. |
| X-002 Best audit trail | V3 (C) | Per-action Orca records beat one long transcript (A) and scattered briefs (B). |
| X-003 Where pr-submit runs | V5 (E) | Coordinator by default per D3 (a); worker under D3 (b) only when parallel PR monitoring is requested (B's surviving case). |
| X-004 Meaning of `[G:cl] 62-65` | V1 (A) | V1 alone reads it honestly: it is conditional on the owner the user's plan names, so it neither forbids nor requires coordinator PR prep. |
| X-005 D's narrow tool list | V1 (A) | A makes no unprovable allowlist claim; D's benefit cannot restrict Bash to git (UNVERIFIED in V4). |
| A-001 Attended coordinator | V5 (E) | It keeps outward actions where attended approval is possible and limits up-front grants to reversible local commits. |
| A-002 Complete contract file lists | V2 (B) | A sole-writer committer stages from its own `git status`, not from a self-reported list. |
| A-003 Quiescence knowable | V2 (B) | Worker commits in a sole-writer worktree need no quiescence map; every coordinator-commit design does. |
| A-004 Commit does not rewrite files | V2 (B) | Hook rewrites stay inside the committing worker's own worktree instead of the shared one. |
| A-005 Standing instruction covers later commits | V5 (E) | It confines standing grants to local commits and keeps every outward action per-instruction. |

Tally: V5 11, V2 6 (one shared with V5), V3 4, V1 4, V4 0. B's wins cluster on the L3 state points (A-002, A-003, A-004, C-002) and on throughput (C-006, C-009). Those are the points where a worker that owns its own worktree removes a dependency the other designs cannot verify.

### Round 1, advocate C (source: round1-advocate-c.md)

### Round 1 advocate: Variant 3 (option C, dedicated long-lived git session)

Persona: devops/architect (reliability, observability, orchestration mechanics) plus analyzer (evidence quality).
Debate: git ownership when an Orca coordinator runs IronClaude `/sc:` commands as workers.
Citation keys as in `variant-1-original.md`. Every citation below was re-read on 2026-11-02 (Orca CLI 1.4.237 guide via `orca-ide skills get orchestration ... | cat -n`; repo files via `sed -n`). Anything not re-read is marked UNVERIFIED.

#### Position summary

A dedicated git worker should own every outward git and GitHub action (push, PR through `/sc:pr-submit --monitor 3`, review replies, issue or status comments), one Orca Task per action. That keeps the long pr-submit loop off the coordinator, gives each action an Orca record, and is the only option that does both. I concede that C should not own per-task local commits inside a sole-writer worker's run (E's rule is better there), and that C needs two spec changes (D3 (b), and a carve-out from `SPEC:156`'s "workers make no commits or pushes") before it is legal under the current spec.

#### Steelman of each opposing variant

##### A (coordinator runs all git in its main chat)
**Strongest form.** A has the fewest moving parts. The person gives an instruction and the same session acts on it, so the authorization cannot be lost, widened or forged on the way (V1 Safety). It is exactly what the spec already recommends: D3 (a) "Coordinator or person only (recommended)" (`SPEC:341`, `SPEC:343`) and D4 (b) for outward actions (`SPEC:347`). `/sc:pr-submit`'s top-level rule is met because the coordinator is the main orchestrating session (`sc-pr-submit-protocol/SKILL.md:47-49`). Only one session ever takes `index.lock`, and the only thing that can move HEAD is the coordinator, so the implement head-moved halt (`refs/retry.md:41,44`) is avoided by one rule. Cost is lowest: wording only (V1 Implementation cost). Its waiting problem is softened because Orca messages queue durably ([G] 73-74) and `check` replays the oldest Delivery until it is acknowledged ([G] 120-124).

**What it gets right.** Directness of authorization in an attended session, exact fit to the current spec text, and lowest implementation cost. These are real and I do not dispute them.

**Critique.**
1. The coordinator is the one session every worker depends on for answers. Workers' blocking questions go through `ask`, and the worker contract says "Resume the same message ID after an ask timeout" ([G] 80-82). While the coordinator sits in pr-submit's attended loop, whose per-wait budget is 600 s (`cmd/pr-submit.md:49`) and which can repeat over `--max-rounds` (default 2, hard cap 5, `cmd/pr-submit.md:47`), every blocked worker's `ask` times out and waits. Durable queueing ([G] 73-74) prevents loss, not delay. A trades throughput of the whole run for simplicity.
2. Orca's own guide says that if "the user's plan names a next owner, post-review fixes and PR preparation remain with that owner; the coordinator routes and synthesizes" ([G:cl] 62-65). V1 concedes this (V1 Weakness 3). A makes the coordinator both router and owner of PR preparation.
3. The "same session" advantage depends on an attended coordinator (A-001). If the person gives one instruction ("commit and open a PR when it passes") and leaves, A also acts on an up-front grant, the same kind C quotes in a brief.

##### B (workers run their own git)
**Strongest form.** Only the worker knows when one of its own tasks ends, so only B (and E) can make the per-task commits #326 asks for (EVAL F1, `issue-326-evaluation.md:51`). Linked worktrees have separate index files and HEADs (GITDEMO), so one-worker-per-worktree has no lock contention and no cross-worker HEAD movement. A commit between one task's `complete` line and the next task's Q0 keeps the retry ladder valid, because Q0 records HEAD at each task's start (`sc-implement-protocol/SKILL.md:114`; `refs/retry.md:41`). Commits made before a crash survive, which is #326's stated point.

**What it gets right.** Per-task commits and crash survival of finished work. C does not solve either (C-002), and I concede it.

**Critique.**
1. Unsafe in the default layout. Orca's placement rule is "Use the current or an exact existing workspace by default. Create a worktree only when the user requested one or a concrete checkout or filesystem conflict makes sharing unsafe" ([G:pl] 8-11). B forces a worktree per committing worker, against that default (V2 Weakness 1).
2. Outward actions spread over N sessions. WC-9 exists to keep outward defaults off in workers (`SPEC:73`); B turns them on per worker. Each PR would need D3 (b) in every worker, against `SPEC:343`.
3. Highest cost and against the additive rule for Phases 1-3 (`SPEC:172`): every committing command needs a commit step, a stale-lock rule and a SHA field; implement currently says acceptance never "authorizes commit, PR, merge or release" (`refs/managed-workspace.md:63,67`, cited via `EVAL:63`, K3).
4. Merges back still need a single owner (V2 Weakness 4), so B is never complete alone.

##### D (coordinator's Agent-tool subagent runs git)
**Strongest form.** D gives A's context relief with no Orca overhead: no 60 s readiness limit (`CAPS:44`), no retention request ([G:rc] 157), no Task bookkeeping. The subagent runs one at a time under the coordinator, so single-writer correctness equals A's. Subagents inherit the parent's permission mode, so a permission prompt still reaches the person (V4, AGENT-TOOL).

**What it gets right.** Cheapest way to move diff reading and commit-message drafting out of the coordinator's context for local commits.

**Critique.**
1. It cannot do the actions that matter most. `/sc:pr-submit` "MUST run in the main orchestrating session ... Do NOT run it inside an Agent-tool subagent" (`sc-pr-submit-protocol/SKILL.md:47-49`), and the main session must "Never hand a side effect to a background shell, detached loop, or subagent" (`SKILL.md:82-84`). So PRs, monitor pushes, replies and resolves fall back to A (V4 Weakness 1). D is a partial answer by design.
2. It breaks Orca provenance when provenance was requested: "Never substitute a non-Orca subagent tool when Orca orchestration provenance was requested" ([G] 46-47). A subagent is not a Task or Dispatch (`CAPS:155-158`), so git actions leave no Orca outcome.
3. Its "narrow tool list" benefit is void (X-005): V4 itself marks Bash-to-git-only restriction UNVERIFIED, and no agent in `src/superclaude/agents/` uses a `Bash(...)` pattern (V4 What D buys; I did not re-run that grep, UNVERIFIED by me).

##### E (hybrid: sole-writer workers commit locally; coordinator owns outward)
**Strongest form.** E splits along the line the evidence actually draws. Local commits are safe for a worker exactly when it is the only writer in its worktree (separate index and HEAD per linked worktree, GITDEMO), and per-task commits are only possible where task boundaries are known (`SKILL.md:114`, `retry.md:41`, `SKILL.md:97` for batches). Outward actions stay where the person speaks and where pr-submit is allowed (`SKILL.md:47-49`), matching D3 (a) (`SPEC:341`) and leaving WC-9 as strict as today (`SPEC:73`). Its per-action ownership table (V5 The proposal) is the clearest statement of any variant, and its F3 guard on removing branches (no unmerged or open-PR branch removed without instruction, `EVAL` F3) is the only explicit cleanup rule.

**What it gets right.** Per-task commits (C-002), crash survival, the per-action table, the cleanup guard, and keeping outward actions out of ordinary workers. It is the strongest opponent.

**Critique.**
1. Its outward row inherits A's blocking problem unchanged: "Accepted as in A" (diff C-009). The pr-submit loop still holds the coordinator while workers wait on `ask` ([G] 80-82; `cmd/pr-submit.md:47,49`).
2. Its outward audit trail is the coordinator's transcript (V5 Safety), which is not an Orca record; nothing ties a push or PR to a Task outcome.
3. Two owners for local commits means two rule sets (V5 Weakness 1).
4. E's outward row and C are composable, not exclusive: E's table can name the git session as the owner of outward actions when the user opts in, with no change to E's worker-local commit row. That is my recommended merge (see Concessions).

#### Strengths claimed

1. **Only C takes the pr-submit loop off the coordinator while still satisfying pr-submit's top-level rule.** A worker is a top-level session, so `/sc:pr-submit` may run there (`CAPS:161`; `sc-pr-submit-protocol/SKILL.md:47-49`). D cannot (`SKILL.md:47-49,82-84`); A and E accept the block (diff C-009). The loop's per-wait budget is 600 s (`cmd/pr-submit.md:49`) over up to `--max-rounds` cycles (default 2, cap 5, `cmd/pr-submit.md:47`). During that time a C coordinator keeps answering other workers' `ask` messages and validating `worker_done` ([G] 120-124). The spec already anticipates this case: D3 (b) exists "so several PRs can be monitored in parallel" (`SPEC:342`).

2. **One Orca record per action.** "A Task is work. A Dispatch is one authoritative Task attempt" ([G] 51-52). Each git action under C is its own Task with a brief (holding the quoted authorization), its own `worker_done` with an explicit `--outcome succeeded|failed` ("Never encode failure only in prose", [G] 88-90) and its own `return-contract.yaml` (WC-4). No other option gives a push or PR an Orca outcome: A and E keep outward actions in a transcript, D leaves no Orca record (`CAPS:155-158`), B scatters them across worker transcripts.

3. **Provenance-safe context relief.** C gives D's benefit (diffs, `git status` output and commit drafting stay out of the coordinator's context) without breaking "Never substitute a non-Orca subagent tool when Orca orchestration provenance was requested" ([G] 46-47).

4. **Serialization is enforced by Orca, not by convention.** A terminal that already owns an active Dispatch rejects another (`runtime_error`, "a target terminal that already owns an active Dispatch", [G:rc] 108). The git session can never run two git actions at once, so it never contends with itself for `index.lock` (GITDEMO). Honest scope: this does not stop the coordinator or another worker from running git; the "workers never run mutating git" rule still does that.

5. **Fits Orca's review-ownership rule.** The guide wants the coordinator to "route and synthesize", with PR preparation staying with "the next owner" the user's plan names ([G:cl] 62-65). C supplies that named owner. A violates the spirit of this unless the plan names the coordinator (V1 Weakness 3).

6. **C works without retention; retention is only an optimization.** If the user does not ask to keep the git terminal ([G:rc] 157), the coordinator releases it after each action ([G] 166-170) and starts a fresh git worker for the next action. That still gives strengths 1-5; the cost is a new readiness wait per action (limit 60 s, `CAPS:44`; a Claude worker start was observed at 34 s in the repo's own eval, quoted at `CAPS:47`). When the next git action is known at settlement time, same-terminal reuse is allowed with no user request ([G:cl] 48-55).

7. **Crash behaviour is clean and Orca-visible.** A git-session crash shows up in Orca liveness (`live` / `unverifiable` / `exited`, `CAPS:122-126`), the failed action is re-issued as a new Task (WC-6, `SPEC:70`), and a failed start still owns its terminal and is released, not closed by hand ([G:rc] 163-165). Under A a coordinator crash mid-action loses the actor and the record together.

8. **It is the orchestration-level form of #326's "central relay".** #326 asks to "evolve sc:git into a central relay for all other commands to use" (quoted at `EVAL:17`). Commands cannot call Orca or another session (SA-2, `SPEC:170`; WC-8, `SPEC:72`), so a relay cannot be something commands call. A session the coordinator feeds is the only relay shape the spec allows. If #326 later gives `/sc:git` an unattended mode, the git session runs it instead of raw git, with no design change.

#### Weaknesses identified in other variants

1. **A, E: the coordinator becomes a single point of delay during PR work.** pr-submit's loop runs "in the main orchestrating session" and performs every side effect itself (`SKILL.md:47-49,82-84`), with 600 s per-wait budgets (`cmd/pr-submit.md:49`) over up to 5 rounds (`cmd/pr-submit.md:47`). Workers that `ask` meanwhile hit timeouts and must resume the same message ([G] 80-82). Neither A nor E proposes a mitigation beyond "after the workers finish" (`SPEC:341`), which rules out PR work while any worker is still running.
2. **A: owner work in the router.** [G:cl] 62-65 keeps PR preparation with the owner the user's plan names, and says the coordinator "routes and synthesizes". V1 concedes the conflict (V1 Weakness 3).
3. **A, E: outward actions have no Orca outcome.** Their audit for a push or PR is the coordinator transcript (V1 Safety; V5 Safety). Orca's lifecycle authority comes "from the active Dispatch, not a ... provider transcript" ([G] 53-54), so for whether an action happened and how it ended, Orca itself ranks a transcript below a Dispatch record. (That line is about lifecycle authority; applying it to audit is my inference.)
4. **B: unsafe under Orca's default placement.** Workers share the current workspace by default ([G:pl] 8-11). Two committers in one worktree contend for `index.lock` (GITDEMO) and any commit moves the shared HEAD, halting every running implement task there with `head-moved` (`retry.md:41,44`). V2 concedes it (V2 Weakness 1).
5. **B: multiplies outward actions across sessions.** WC-9 turns every outward default off in workers (`SPEC:73`); B turns them back on per worker and needs D3 (b) in each (`SPEC:342-343`).
6. **B: highest cost, against SA-4.** Command edits in Phases 1-3 must be additive (`SPEC:172`); B needs new commit steps, stale-lock handling and SHA fields in every committing command (V2 Implementation cost).
7. **D: cannot run pr-submit at all.** `SKILL.md:47-49` forbids it in an Agent-tool subagent; `SKILL.md:82-84` forbids handing its side effects to a subagent. D therefore covers local commits only and falls back to A for every outward action (V4 What D costs).
8. **D: breaks provenance when provenance is requested** ([G] 46-47); a subagent is not a Task or Dispatch (`CAPS:155-158`).
9. **D: the narrow-tool benefit is unproven** (X-005; V4's own UNVERIFIED on restricting Bash to git subcommands).
10. **E: two rule sets for local commits** (V5 Weakness 1), and its worker-local commits depend on a K3 feature that does not exist yet; "until it exists a worker commits only through steps its brief adds after the command finishes" (V5 Implementation cost), so per-task commits inside one implement run are not available today under E either.

#### Concessions

1. **C conflicts with the spec as written, twice.** `SPEC:156` says of `/sc:git`: "Runs git itself, only when the user asked; workers make no commits or pushes." The git session is a worker, so C needs a named exception there. And running pr-submit in it is D3 (b), which the spec does not recommend: "Recommendation: (a), unless parallel PR monitoring is a real need" (`SPEC:343`). C is only legal after both changes.
2. **C does not solve per-task commits (C-002).** The coordinator sees only a worker's final `worker_done` ([G] 88-90), so it cannot time a commit between two tasks inside one implement run. E's sole-writer worker rule is better on this point, and I would adopt it unchanged.
3. **Retention is a stretch of its stated purpose.** `worker-retain --help` line 5 describes it as "Keep one supervised worker terminal live for debugging", and [G:rc] 157 allows it "only when the user explicitly wants the settled terminal kept live". A long-lived git session uses retention for something other than debugging. Strength 6 is my answer: C must be specified so that it works with a fresh git worker per action, and retention is an opt-in speed-up only.
4. **Reuse mechanics are partly UNVERIFIED.** For a Claude worker, Orca passes the task on the command line at launch (`CAPS:47`, `promptInjectionMode: 'argv'`); for a reused terminal Orca waits for an idle TUI instead (`CAPS:47`, the `n.reusesTerminal` branch), and how the next Task's text then reaches a running Claude session is UNVERIFIED. `worker-start --help` line 44 also says "Not every worker has a terminal" (the user's chat-tab setting, line 42), so whether `--terminal` reuse is available when workers run as chats is UNVERIFIED. What final cleanup of a reused terminal looks like is also UNVERIFIED: release leaves "Reused ... terminals ... retained" ([G:rc] 160-161).
5. **Authorization takes one hop** (X-001). The person's instruction reaches the git session only as a quote in the coordinator's brief (D4 (a), `SPEC:346`). In an attended session A is strictly more direct. C compensates with a per-action record, not with directness.
6. **For a local commit at a quiescent point in a shared worktree, C adds cost without adding correctness.** A, D and E get the same single-writer guarantee; C adds a Task, a brief and possibly a readiness wait (limit 60 s, `CAPS:44`) for a seconds-long action. On C-001 I rank E above C.
7. **Quiescence is still the coordinator's job** (A-003). The git session cannot know which workers write in a worktree; the coordinator must assert quiescence in each brief from its own placement map.
8. **The git session's own context grows over a long run** when reused, because reuse keeps the conversation (V3 Context load).

**Recommended merge for later rounds.** Take E's table as the base and change one row: outward actions (push, PR via `/sc:pr-submit --monitor 3`, replies, comments) are owned by a dedicated git worker, one Task per action, when the user opts in or when parallel PR monitoring or coordinator responsiveness is needed (D3 (b)); otherwise they stay with the coordinator as in E. Local commits follow E's rows unchanged.

#### Shared-assumption responses

- **A-001 (coordinator session is attended): QUALIFY.** True for the interactive case the variants describe, but no Orca mechanism guarantees it. When the person gives one instruction and leaves, every option acts on an up-front grant; A's "same session" advantage then shrinks to the same grant C quotes. In that case C's per-Task brief is the better record of which grant each action used.
- **A-002 (contract file lists are complete): REJECT.** Nothing makes `artifacts` plus `--files-modified` complete; [G] 91 only says to append `--files-modified` "with real values when applicable", not that every touched file is listed. Whoever commits should run `git status --porcelain` in that worktree at the quiescent point and report unlisted paths to the coordinator, never sweep them with `git add -A` and never silently drop them. A C git session is a natural place for that check because it already reads the diff.
- **A-003 (quiescence is knowable): QUALIFY.** Knowable only from the coordinator's own placement records; the claim that no Orca verb maps worktrees to running writers comes from the diff analysis and I did not re-verify it (UNVERIFIED by me). Under C the coordinator must state quiescence in each git brief; the git session cannot check it. E's sole-writer rule makes it true by construction for worker-local commits.
- **A-004 (a commit does not rewrite files): ACCEPT the diff's verdict (contradicted where hooks are installed).** Verified: `.pre-commit-config.yaml` defines `trailing-whitespace` (line 9), `end-of-file-fixer` (line 11), `ruff-format` (line 111) with `default_stages: [commit]` (line 143); this clone's hooks directory holds only `*.sample` files and `core.hooksPath` is unset (checked 2026-11-02). Where hooks are installed, any committer must commit only at quiescence and re-stage or report hook rewrites; this applies to every option equally.
- **A-005 (a standing instruction covers later commits): QUALIFY.** `CLAUDE.md:37` says only "commit only when asked". The #326 evaluation treats per-task commits as "an authorized option, never a default" and says the owner's issue comment "does not by itself authorize commits in a worker" (`EVAL:74`). A standing instruction should count only when it names its scope (this run, this branch, these action types); each C Task brief should quote it, so every commit shows which standing grant it relied on.

#### Per-point positions

| Point | Superior variant | One-line reason |
|---|---|---|
| S-001 | V5 (E) | The per-action ownership table states owner and condition for every action; prose leaves gaps. |
| S-002 | V3 (C) | Only C verifies the Orca mechanics (reuse, one active Dispatch per terminal, retention, idle rule) its design depends on. |
| S-003 | V1 (A) | V1 carries the actual GITDEMO procedure the others only cite. |
| S-004 | V3 (C) | Only C addresses #326's "central relay" directly and shows why commands cannot call one (`SPEC:72,170`; `EVAL:17`). |
| C-001 | V5 (E) | Single writer at quiescent points, explicit paths; C adds a Task and readiness wait for no correctness gain on a local commit. |
| C-002 | V5 (E) | Sole-writer worker commits between tasks keep the ladder valid (`SKILL.md:114`, `retry.md:41`) without B's shared-worktree hazards. |
| C-003 | V3 (C) | Outward actions in one dedicated worker keep the coordinator responsive and give each action an Orca outcome; requires D3 (b). |
| C-004 | V1 (A) | In an attended session, direct authorization beats any quoted hop; qualified by A-001. |
| C-005 | V3 (C) | One Task, brief, `worker_done` and contract per action is the only Orca-recorded audit ([G] 51-52, 88-90). |
| C-006 | V3 (C) | The git session absorbs both diffs and the pr-submit loop; D and E still leave pr-submit on the coordinator. |
| C-007 | V5 (E) | Lock confined to the worker's own worktree and earlier commits survive; C's recovery is clean but no better than A's for local state. |
| C-008 | V5 (E) | E states the precise layout condition (sole writer) for worker commits; C's `git -C` flexibility is compatible with it. |
| C-009 | V3 (C) | Only C runs pr-submit top-level (`CAPS:161`) without blocking the coordinator; D cannot (`SKILL.md:47-49`). |
| C-010 | V1 (A) | Wording only; no new briefs, contracts or agents. |
| C-011 | V5 (E) | Only E makes worktree and branch creation and removal explicit, with the F3 guard. |
| X-001 | V5 (E) | A quoted user instruction under D4 (a) (`SPEC:346`) is sufficient for a local commit; E bounds it with sole-writer and between-task conditions. |
| X-002 | V3 (C) | A per-action Dispatch record outranks a transcript for lifecycle facts ([G] 53-54). |
| X-003 | V3 (C) | Coordinator responsiveness and parallel PR monitoring are the reason D3 (b) exists (`SPEC:342`); conditional on adopting D3 (b), else V1/V5. |
| X-004 | V3 (C) | [G:cl] 62-65 keeps PR preparation with a named owner while the coordinator routes; C supplies that owner. |
| X-005 | V4 (D), its own caveat | V4's UNVERIFIED caveat is correct, so the narrow-tool benefit should be dropped; no variant should rely on it. |
| A-001 | V3 (C) | If the coordinator is unattended, a per-Task brief that quotes the grant is the best surviving record. |
| A-002 | V5 (E) | The worker that wrote the files commits them in its own worktree; elsewhere a `git status` check at quiescence is needed by all. |
| A-003 | V5 (E) | Sole-writer worker commits make quiescence true by construction; others rely on the coordinator's map. |
| A-004 | V5 (E) | Hook rewrites in a sole-writer worktree cannot touch another worker's files; shared-worktree commits need quiescence in every option. |
| A-005 | V3 (C) | Quoting the standing grant in each action's Task brief makes the scope of every commit auditable. |

### Round 1, advocate D (source: round1-advocate-d.md)

### Round 1 advocate: Variant 4 (option D, coordinator runs git through an Agent-tool subagent)

Persona: security (least privilege, attack surface, authorization) plus analyzer (evidence quality).
Date: 2026-11-02. Claude Code 2.1.316 (`claude --version`). Orca CLI guide read with `orca-ide skills get orchestration`.

Citation keys as in the variants. Added keys:
- `CC-SUB` = Claude Code subagent docs, https://code.claude.com/docs/en/sub-agents (fetched 2026-11-02).
- `CC-HOOKS` = Claude Code hooks docs, https://code.claude.com/docs/en/hooks (fetched 2026-11-02, first 100k characters only).
- `AGENT-TOOL` = the Agent tool description in this session.

#### Position summary
D is not a complete owner of git and GitHub actions, and I do not argue it is. My claim is narrower. The coordinator should keep every decision and every outward action, as in A and E. Local staging and committing should be done by a dedicated committer subagent whose own frontmatter `PreToolUse` hook blocks everything except an allowlist of git commands. That hook is the only mechanical, per-actor least-privilege control any of the five variants can offer. So the best answer is "A or E for ownership, D as the way local commits are executed."

#### Steelman of each opposing variant

**A (coordinator runs all git in its main chat).** Strongest form: authorization and action happen in the same session, so no prompt hop can lose, broaden or forge an instruction (V1 Safety). There is exactly one git writer per worktree, so `index.lock` collisions (GITDEMO) and unplanned HEAD moves cannot happen. The only HEAD-moving actor can follow the quiescence rule against `/sc:implement`'s `head-moved` halt (`src/superclaude/skills/sc-implement-protocol/refs/retry.md:41,44`, verified). It fits `/sc:pr-submit`'s top-level rule exactly (`src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:47-49,82-84`, verified), matches spec D3 (a) (`SPEC:341`, verified) and matches the `/sc:git` row "Runs git itself, only when the user asked; workers make no commits or pushes" (`SPEC:156`, verified). Cost: wording only. What it genuinely gets right: the authorization model, which I adopt for every outward action.
*Critique:* A's safety rests entirely on the model's prose discipline in the session with the largest context and the full Bash tool. The repo itself says prose rules are not enough here: the `.claude/` staging ban exists because "neither [mechanical gate] catches `git add -f` or hand-edited paste-ready commands" (`CLAUDE.md:31`, verified). A gives no mechanical layer for that rule or for "never `git add -A` in a shared worktree" (V1 Correctness). A's context cost is also real (V1 "Context load").

**B (workers run their own git).** Strongest form: only the worker knows when a task inside a long `/sc:implement` run ends, so only B (and E) can make the per-task commits #326 asks for. Separate linked worktrees have separate index and HEAD files (GITDEMO), so committing workers need never contend. Commits made before a crash survive (V2 Recovery).
*Critique:* B is unsafe in the default layout. Workers share the current worktree by default (`[G:pl] 8-11` via `CAPS:115`, verified): "Use the current or an exact existing workspace by default. Create a worktree only when the user requested one or a concrete checkout or filesystem conflict makes sharing unsafe." B multiplies the actors that hold mutating git and, under D3 (b), outward GitHub authority. That is the attack-surface growth WC-9 exists to prevent (`SPEC:73`, verified). It also has the highest implementation cost, against the additive-edits rule (V2 Implementation cost).

**C (dedicated long-lived git session as an Orca worker).** Strongest form: every git action is its own Orca Task with a brief, a `worker_done` and a contract. That is the best audit record of the five (V3 Safety). A terminal with an active Dispatch rejects a second one (`[G:rc] 108`), which gives strict serialization for free. And `/sc:pr-submit`'s long attended loop moves off the coordinator, because a worker is a top-level session (`CAPS:161`, verified). If Orca provenance for git actions is requested, C is the only variant that can satisfy `[G]` 46-47: "Never substitute a non-Orca subagent tool when Orca orchestration provenance was requested" (verified with `orca-ide skills get orchestration`).
*Critique:* C's main advantage, pr-submit off the coordinator, requires D3 (b), which the spec does not recommend (`SPEC:343`, verified). Without that, C pays a readiness start of up to 60 s per fresh start (`CAPS:44`, verified) plus a user retention request (`[G:rc] 157`) for local commits, which D does in-process. The git session is a whole Claude session with full Bash and its own permission mode. C's brief-borne authorization is the same one-hop structure D has, plus a cross-session hop. C offers no per-actor mechanical command restriction.

**E (hybrid: sole-writer workers may commit locally; coordinator owns every outward action).** Strongest form: it splits by the real safety line. Local commits are safe exactly when the committer is the sole writer of its worktree. Outward actions are safe only where the person authorizes directly. Its per-action table (V5 Proposal) is the most precise statement of ownership in the debate, and it is the only variant that both keeps WC-9 strict and allows #326's per-task commits. It is also the only variant that names the branch-removal guard (F3).
*Critique:* E's per-task benefit is deferred. Its own "Implementation cost" says the commit step inside `/sc:implement` "stays #326's feature (K3)". Until then a worker commits only "through steps its brief adds after the command finishes", which is no more granular than A. A sole-writer worker running raw git still has the full Bash tool and no mechanical guard (V5 Weakness 2). E's two rule sets double the surface to test (V5 Weakness 1).

#### Strengths claimed

1. **A mechanical per-actor guard (this corrects V4's own X-005 claim).** V4 claimed a narrow `tools:` list as the benefit. That mechanism does not work. CC-SUB: "A `disallowedTools` entry with a specifier, such as `Bash(git push *)`, still removes the whole tool from the subagent, not only the matching commands." The real mechanism is the `hooks` frontmatter field, which is "scoped to the subagent". CC-SUB names this use explicitly: "use `PreToolUse` hooks to validate operations before they execute. This is useful when you need to allow some operations of a tool while blocking others". Its example is a `tools: Bash` subagent with a `PreToolUse` `matcher: "Bash"` script that "exits with code 2 to block write operations". A committer agent can therefore be `tools: Bash, Read` with a hook that allows only `git status`, `git diff`, `git add -- <explicit paths>` and `git commit -m`. It can block `git add -A`, `git add .`, `-f`, any `.claude/` path other than `.claude/settings.json`, `push`, `gh`, `reset`, `checkout` and `rebase`.
   - This mechanizes the repo rule that `CLAUDE.md:31` says the existing gates miss: "neither catches `git add -f` or hand-edited paste-ready commands" (verified).
   - It mechanizes V1's "no cross-worker sweep" rule, which A, C and E leave to model discipline.
   - No variant can do this for a main chat or an Orca worker without blocking that session's other legitimate Bash use. Settings-level hooks fire inside subagents too and receive `agent_type` (CC-HOOKS), so a settings hook could also tell committer calls apart from other callers.
   - Evidence quality: documentation only. No such agent exists in the repo: `grep '^hooks:'` over `src/superclaude/agents/*.md` returned nothing. Not tested end to end: UNVERIFIED in practice.
2. **The same single-writer correctness as A.** The subagent runs in the coordinator's session against the same worktree, and the coordinator runs one at a time, so there is one `index.lock` holder (GITDEMO). HEAD moves only at the coordinator's chosen quiescent points (`retry.md:41,44`, verified).
3. **Fits the spec's coordinator-only git row and D3 (a) unchanged.** The `/sc:git` row says the coordinator "Runs git itself, only when the user asked; workers make no commits or pushes" (`SPEC:156`, verified). A subagent of the coordinator is still the coordinator's session, not a worker. The `/sc:pr-submit` ban covers only that skill's own side effects: "MUST run in the main orchestrating session ... Do NOT run it inside an Agent-tool subagent" and "Never hand a side effect to a background shell, detached loop, or subagent" (`SKILL.md:47-49,82-84`, verified). D keeps pr-submit in the main chat, so it breaks neither rule.
4. **Context isolation without Orca cost.** Diff reading, `git status` output and message drafting stay in the subagent. No readiness start (`CAPS:44`, 60 s default, verified), no retention request (`[G:rc] 157`), no Task bookkeeping. Agent-tool subagents are not counted by Orca's depth fence (`CAPS:155`, verified, with that file's own UNVERIFIED note).
5. **No self-elevation.** In a parent running `default` or `dontAsk`, a subagent that sets `bypassPermissions` "keeps the parent's mode" (CC-SUB, from v2.1.267; local version 2.1.316). The committer can be stricter than its parent but never looser. Adding `Agent` to `disallowedTools` stops it spawning further subagents (CC-SUB).
6. **Reconciliation off the coordinator.** A-002 (file lists may be incomplete) needs someone to compare `git status --porcelain` with the contract's `artifacts` and report anything extra instead of sweeping it. That is diff-heavy work. D does it outside the coordinator's context and returns only the list of extras for the coordinator to decide on.

#### Weaknesses identified in other variants

1. **A: no mechanical boundary, maximal ambient authority.** The session that holds git also holds every other tool and the whole run's context, including worker reports that could carry injected text. A's only defense against a wrong `git add` is the model (V1 Proposal). The repo calls that insufficient for `.claude/` staging (`CLAUDE.md:31`). A's context load is its own stated weakness 2.
2. **B: biggest attack surface, unsafe default layout.** Every committing worker holds mutating git, and under D3 (b) outward authority too (V2 Safety). Authorizations are "spread over many briefs and transcripts" (V2 Safety). Shared-worktree commits halt running implement tasks (`retry.md:41,44`), and sharing is the default (`CAPS:115`). B needs K3 (`EVAL:63`) and per-command changes.
3. **C: a whole session as the git actor.** The git session needs D3 (b) for its main benefit (`SPEC:343`). It needs a user retention request or it degrades to a fresh worker per action (V3 Weakness 2). Reuse injection into a running Claude session is UNVERIFIED by V3 itself (V3 Context load: "CAPS:47 shows argv injection only for fresh launches", consistent with `CAPS:47` `promptInjectionMode: 'argv'`, verified). Its authorization travels coordinator → brief → another session with its own permission mode. That hop is longer than D's, not shorter.
4. **E: its distinctive benefit is deferred and unguarded.** Per-task commits need K3, which E itself leaves to #326 (V5 Implementation cost). The sole-writer worker's raw git has no mechanical boundary (V5 Weakness 2). Sole-writer status is asserted by the coordinator's placement and is not checked by anything (see A-003).
5. **Evidence-quality note on the shared spec.** WC-7 cites the pr-submit top-level rule as `sk/sc-pr-submit-protocol/SKILL.md:37-39` (`SPEC:71`, verified). The rule is actually at lines 47-49 of the current file (verified). The variants all cite 47-49 correctly, but the spec citation is stale.

#### Concessions

1. **D cannot own outward actions.** Push, PR, review replies and status comments stay in the coordinator's main chat (`SKILL.md:47-49,82-84`). D is a way of carrying out A or E, not a sixth ownership model (V4 Weakness 1 stands).
2. **The authorization hop is real.** The user's instruction reaches the subagent only as the coordinator's prompt. The subagent's report comes back "in the same confident register as its findings" (AGENT-TOOL). The hook bounds what the subagent can do, but not whether the coordinator should have asked it.
3. **V4's permission-prompt claim was too broad.** V4 said a subagent's prompt "still reaches the person". That is true only in a `default` parent. If the parent runs `bypassPermissions`, `acceptEdits` or `auto`, "the subagent runs in that same mode and Claude Code ignores the `permissionMode` you set" (CC-SUB). An unattended coordinator would likely run in such a mode. The docs I read do not say whether a `PreToolUse` exit 2 still blocks under `bypassPermissions`; they state the exit-2 rule with no mode carve-out (CC-HOOKS). UNVERIFIED. This is the critical point for Strength 1 and needs a test.
4. **The guard can disappear in some installs.** Subagent `hooks` are "ignored for plugin subagents", and project-level agent hooks are skipped until the workspace is trusted (CC-SUB). The repo ships a plugin mirror (`plugins/superclaude/agents/*.md` exists, 21 files). A committer delivered as a plugin agent would lose its hook silently. The guard holds only for the user-level `~/.claude/agents/` install. That is UNVERIFIED in practice for user-level hooks.
5. **No Orca record.** If the user requests Orca provenance for git actions, `[G]` 46-47 rules D out and C wins. A has no Orca record either, so on this point D is equal to A, not worse.
6. **Implementation cost is higher than V4 said.** An allowlist hook script is new security-relevant code with its own tests (quoting, `--` handling, path rules). It is not "one agent definition". It is still lower than B or C.
7. **No per-task commits.** D, like A and C, sees only the run's end.
8. **Small saving per commit.** For a one-file commit the context saving may not pay for the hop (V4 Weakness 3). The security guard, not the context saving, is D's real justification.
9. **Configuration hazards.** The committer must not set `isolation: worktree`, because that runs it in a temporary worktree (CC-SUB) and would commit to the wrong tree. It must not set `omitClaudeMd`, because it needs the repo's staging rules.

#### Shared-assumption responses (A-001..A-005)

- **A-001 (coordinator session is attended): QUALIFY.** Every variant's authorization story assumes a person is watching. If the person gives one instruction and leaves, A's "same session" advantage becomes an up-front grant, as the diff analysis says. Prompt-based approval then reaches no one (and under a `bypassPermissions` parent it is not shown at all, CC-SUB). The only control left is a mechanical one, which strengthens D's hook argument, subject to the UNVERIFIED bypass interaction in Concession 3. The spec should say outright that outward actions need an attended coordinator or an explicit up-front grant that names them.
- **A-002 (contract file lists are complete): REJECT.** It cannot be relied on. Drive-by edits, formatter rewrites and generated files fall outside `artifacts` and `--files-modified`. The committer must compare `git status --porcelain` with the contract list and report the extra paths to the coordinator, never sweep them with `-A`. A hook that refuses `git add -A` and `git add .` makes the "never sweep" half mechanical.
- **A-003 (quiescence is knowable): QUALIFY.** It is knowable only from the coordinator's own placement records. Orca maps Dispatches to status, but no Orca verb maps a worktree to the workers writing in it (diff analysis A-003). The spec must require the coordinator to keep that map. A committer subagent can at least refuse when `git status` shows paths outside the contract lists, which is a weak signal of an active writer. E reduces how often this matters by moving commits into sole-writer worktrees.
- **A-004 (a commit does not rewrite files): REJECT.** Where `.pre-commit-config.yaml` hooks are installed, `trailing-whitespace`, `end-of-file-fixer` and `ruff-format` can rewrite files during commit (diff analysis A-004). Skipping them with `--no-verify` is not allowed: "Never turn off a quality check" (`HWW:280`, verified). So quiescence must cover every writer in the worktree, not only `/sc:implement` workers. A hook-fixed commit fails, then needs a re-stage and a second commit. That retry is diff-heavy work best kept out of the coordinator's context, which is a small D point.
- **A-005 (a standing instruction covers later commits): QUALIFY.** Accept it only when the instruction names its scope: which run, which branch, local only. The coordinator must also pass it word for word into each committer prompt or brief, so that every commit can be traced to the quoted words. `CLAUDE.md:37` ("commit only when asked", verified) does not settle scope. The spec should, and should never let a standing instruction stretch to cover pushes (`HWW:282`, verified).

#### Per-point positions

| Point | Superior variant | One-line reason |
|---|---|---|
| S-001 Proposal form | V5 (E) | A per-action table with owner and condition is the most testable statement of ownership. |
| S-002 Orca-mechanics coverage | V3 (C) | Only C verifies reuse, serialization and retention mechanics; D needs few Orca mechanics and so says little. |
| S-003 Evidence appendix | V1 (A) | GITDEMO is a reproducible procedure the others only cite. |
| S-004 #326 relation | V3 (C) | Only C explains why the "central relay" cannot be something commands call (SA-2, WC-8). |
| C-001 Who stages and commits in a shared worktree | V4 (D) | Same single-writer correctness as A, plus a subagent-scoped `PreToolUse` allowlist that blocks `-A`, `-f` and `.claude/` staging (CC-SUB); bypass interaction UNVERIFIED. |
| C-002 Per-task commits inside `/sc:implement` | V5 (E) | Only the task-boundary-aware worker can time them, and E limits it to sole-writer worktrees; still needs K3. |
| C-003 Owner of push, PR, replies, comments | V5 (E) | Coordinator main chat, matching `SKILL.md:47-49,82-84` and D3 (a), with explicit conditions per action. |
| C-004 Authorization path | V1 (A) | Fewest hops: the person and the actor are the same session; D and C add a prompt or brief hop. |
| C-005 Audit trail | V3 (C) | One Orca Task, brief, `worker_done` and contract per action; D leaves no Orca record (conceded). |
| C-006 Context load on coordinator | V4 (D) | Same commit-diff offload as C at no readiness or retention cost; pr-submit load is the same as C's under the spec-recommended D3 (a). |
| C-007 Crash mid-commit | V5 (E) | A stale lock stays in one worktree and earlier commits survive; D's subagent crash comes back to the coordinator but saves no work. |
| C-008 Worktree layout required | V5 (E) | Works in the default shared layout and uses separate worktrees only where a worker commits. |
| C-009 pr-submit loop blocking the coordinator | V1 (A) | Accepting the block with durable message queueing (`[G]` 73-74, 120-124) keeps D3 (a); C's fix needs D3 (b), which the spec rejects (`SPEC:343`). |
| C-010 Implementation cost | V1 (A) | Wording only; D's hook script is new security code (Concession 6). |
| C-011 Run worktree and branch creation and removal | V5 (E) | Only E states the owner and the F3 guard against removing unmerged or open-PR branches. |
| X-001 Is a quoted brief enough authorization for a local commit? | V5 (E) | Yes for local, reversible commits when the quote names the action and the run; never for outward actions (`HWW:282`). |
| X-002 Which audit trail is best | V3 (C) | Per-action Orca records beat a transcript for later review; A's transcript is second. |
| X-003 Where `/sc:pr-submit` runs | V1 (A) | Coordinator main chat, matching `SKILL.md:47-49` and `SPEC:341`; V4 and V5 agree. |
| X-004 Meaning of Orca's review-ownership rule (`[G:cl] 62-65`) | V1 (A) | Only A engages with it honestly: the coordinator does PR preparation only when the user's plan names it owner (verified text). |
| X-005 D's "narrow tool list" | V4 (D), as amended | The `tools:` specifier mechanism is wrong (it removes the whole tool, CC-SUB), but the subagent `hooks` field gives the claimed per-command restriction. |
| A-001 Coordinator session is attended | V4 (D) | When no one is watching, prompt approval fails and only a mechanical guard remains; D is the only variant with one (UNVERIFIED under bypass). |
| A-002 Contract file lists are complete | V4 (D) | The subagent does the porcelain-against-contract comparison out of the coordinator's context, and the hook makes "never sweep" mechanical. |
| A-003 Quiescence is knowable | V5 (E) | Sole-writer worktrees shrink the cases where quiescence must be proven; no variant has an Orca source for it. |
| A-004 A commit does not rewrite files | V5 (E) | Rewrites by pre-commit hooks stay inside a sole-writer worktree; in shared worktrees all variants need full quiescence. |
| A-005 A standing instruction covers later commits | V5 (E) | Only E makes per-Task quoting of a scoped instruction a stated condition for each commit. |

### Round 1, advocate E (source: round1-advocate-e.md)

### Round 1 advocate: Variant 5 (option E, hybrid)

Persona: qa (edge cases, failure scenarios) plus analyzer (evidence quality). Date 2026-11-02.

Citation keys as in the variants. Every `path:line` below was re-read in this session (sed/awk/cat -n on 2026-11-02). Orca guide lines were read with `orca-ide skills get orchestration [--reference references/<name>.md] | cat -n` (CLI as installed). `[G:cl]` = coordinator-loop, `[G:rc]` = recovery-and-cleanup, `[G:pl]` = placement-and-remote.

#### Position summary

The git owner should be decided per action by two facts git itself enforces: who else writes in the worktree, and whether the action leaves the machine. E is the only variant that follows both: a worker that is the sole writer in its own worktree may make brief-authorized local commits (the only way #326's per-task commits can ever be timed correctly), while every shared-worktree commit and every outward action (push, PR, comment, merge, branch removal) stays with the coordinator in the session where the person gave the instruction. E is also the shape the repo's own #326 evaluation already recommends (F0, F1, F3, F4 at `EVAL:50-54`).

#### Steelman of each opposing variant

**A (V1, coordinator does all git in its main chat).** Strongest form: one actor, one index-lock holder, one transcript. The person who authorizes and the session that acts are the same, so no hop can lose or broaden the grant (V1 Safety). It needs no command changes (WC-9 already turns outward defaults off, `SPEC:73`), matches D3 (a) (`SPEC:341`) and `/sc:pr-submit`'s top-level rule (`sc-pr-submit-protocol/SKILL.md:47-49,82-84`), and only the coordinator can move HEAD, so the implement ladder's "HEAD has not moved" check (`sc-implement-protocol/refs/retry.md:41`) is protected by one rule. A gets right: outward actions belong in the person's session; quiescent commits in shared worktrees; the GITDEMO evidence (U-004) and the quiescence rule (U-008).
Critique: A's own honest limit (V1 "Honest limit") is that it cannot produce per-task commits inside one `/sc:implement` run, because the coordinator sees only the run's `worker_done` (`[G] 88-90`). The fix A defers to, #326 K3 (`EVAL:63`), is a commit step inside `/sc:implement` itself, that is, a commit made by the worker. So A plus K3 is no longer A; it is E. A also concedes it serialises the commits of every experiment worktree through one session (V1 weakness 4) and that Orca's review-ownership rule cuts against a coordinator doing owner work unless the plan names it (`[G:cl] 62-65`).

**B (V2, workers run their own git).** Strongest form: only the worker knows when a task ends, so only the worker can commit between one task's `complete` line and the next task's Q0 (`sc-implement-protocol/SKILL.md:114`; `refs/retry.md:41`). Linked worktrees have separate index and HEAD (GITDEMO), so one worker per worktree has no lock or HEAD contention; committed work survives a crash (#326's stated point); the coordinator reads SHAs, not diffs. B gets right: per-task commits, crash survival, and that a parallel implement batch has no ladder (`SKILL.md:97`).
Critique: B extends worker git to places its own evidence calls unsafe. Workers share the current worktree by default (`CAPS:115`; `[G:pl] 8-11`), and B says it is unsafe there (V2 "Honest limit, shared worktree"). B lets workers push and open PRs under D3 (b), which the spec does not recommend (`SPEC:343`), multiplying the outward actions WC-9 exists to prevent (`SPEC:73`). Its cost is the highest and runs against the additive-edits rule (`SPEC:172`). Merges still need a single owner, so B "is never complete on its own" (V2 weakness 4). E keeps B's correct half and drops the unsafe half.

**C (V3, dedicated long-lived git session as an Orca worker).** Strongest form: every git action is its own Task with brief, `worker_done` and contract, so the audit trail is per-action and inside Orca; a terminal with an active Dispatch rejects a second one (`[G:rc] 108`), giving serialization for free; the long `/sc:pr-submit` monitor loop (600 s wait budget, `cmd/pr-submit.md:49` as cited by V3) runs off the coordinator, which keeps reacting to workers; and it is the orchestration-level reading of #326's "central relay" (U-007). C gets right: the best audit record (X-002), the only real answer to the coordinator blocking on pr-submit (C-009), and the only verified Orca-mechanics section (U-001).
Critique: retention needs the user's explicit request (`[G:rc] 157`: "Retain only when the user explicitly wants the settled terminal kept live"); reuse needs "immediate follow-up work" (`[G:cl] 48-50`); and "Reused ... terminals are retained" (`[G:rc] 160-161`) leaves the git session's final cleanup unclear (V3 marks it UNVERIFIED). Every outward action, pushes and PRs included, then runs on a quoted brief one hop from the person, under D3 (b), which the spec does not recommend (`SPEC:343`). C does not solve per-task commits (V3 weakness 4), and every fresh start pays up to a 60 s readiness budget (`CAPS:44`, Orca default `ORCHESTRATION_READINESS_TIMEOUT_MS = 60_000`).

**D (V4, coordinator's Agent-tool subagent runs git).** Strongest form: A's single-writer correctness with A's context cost removed and no Orca overhead; the subagent inherits the parent's permission mode, so prompts still reach the person (V4, AGENT-TOOL). D gets right: context isolation is real and cheap.
Critique: the actions that matter most cannot run there. `/sc:pr-submit` "MUST run in the main orchestrating session ... Do NOT run it inside an Agent-tool subagent", and the main session must "Never hand a side effect to a background shell, detached loop, or subagent" (`sc-pr-submit-protocol/SKILL.md:47-49,82-84`). So D covers local commits only, adds a hop without an Orca record, and its narrow-tool benefit cannot be shown to restrict Bash to git (X-005; V4 marks it UNVERIFIED). It does nothing for per-task commits.

#### Strengths claimed

1. **E's split follows git's own boundaries, not a policy preference.** Each linked worktree has its own index and HEAD while refs are shared (GITDEMO, V1 Self-check). E lets a worker commit only where it owns the index and HEAD (V5 table row 4, condition 2), and keeps every commit in a shared worktree with the coordinator at a quiescent point (row 3). The two failure modes every variant agrees on, the `index.lock` refusal and the `head-moved` halt (`refs/retry.md:41,44`), therefore cannot occur between two git writers under E in either layout.

2. **E is the only variant that can deliver #326's per-task commits without breaking the retry ladder.** The ladder runs only if HEAD equals the 40-hex recorded at the task's Q0 (`refs/retry.md:41`; Q0 writes `q0-head`, `SKILL.md:114`). A commit after one task's `complete` line and before the next task's Q0 is therefore compatible, and a parallel batch has no ladder to protect (`SKILL.md:97`: "A batch task gets no retry ladder"). E's condition (3), "only between tasks and never inside a parallel batch", is exactly that window. A and D cannot time it (V1 "Honest limit"); C does not solve it (V3 weakness 4); B can, but without E's sole-writer guard.

3. **E matches the repo's own evaluation of #326 almost row for row.** `EVAL:50` (F0): "workers make no pushes, merges or PRs; a worker makes a local commit only when its brief authorizes it (D4)". `EVAL:51` (F1): an authorized commit "stages the task's own files plus `.dev/tasks` ... and never pushes", and only "after a task's `complete` line and before the next task's Q0 start". `EVAL:53` (F3): the coordinator removes the worktrees and branches it created and "never removes a branch that has unmerged commits or an open PR without the user's instruction". `EVAL:54` (F4): progress posts to GitHub are coordinator-only outward actions. E's table rows 1, 2 and 4 are these four findings. No other variant matches F0 and F4 together.

4. **Every outward action keeps A's strongest property.** Push, PR, review replies, comments, remote branch deletion and merges stay in the coordinator's main chat (V5 row 1), the only place `/sc:pr-submit` may run (`sc-pr-submit-protocol/SKILL.md:47-49,82-84`), matching D3 (a) (`SPEC:341,343`), the PR rule (`CLAUDE.md:50`) and "Never push without approval. Commit locally, show your lead what changed, and push only when they say go" (`HOW-WE-WORK.md:282`). WC-9 stays exactly as strict as today for workers (`SPEC:73`). Authorization for anything visible outside the machine never crosses a hop.

5. **The authorization hop E does allow is proportional to the risk.** A worker's local commit is reversible and invisible until the coordinator pushes; the repo distinguishes it from outward action (`CLAUDE.md:37`, "commit only when asked"; `HOW-WE-WORK.md:282`, commit locally before an approved push). E requires the brief to quote the user's instruction for that Task (row 4, condition 1), the same mechanism the spec already recommends for outward actions (D4 (a), `SPEC:346`), so E asks less of the hop than the spec's own recommendation does.

6. **E works in the default layout without forcing a worktree per worker.** Orca's default is the current worktree; a new one only when "a concrete checkout or filesystem conflict makes sharing unsafe" (`[G:pl] 8-11`; `CAPS:115`). In a shared worktree E behaves as A (row 3, row 5); in an experiment worktree (#326's "Branching and worktrees when performing parallel experiments", `EVAL:52`) it behaves as B's safe case. B forces a worktree per committing worker (V2 "Honest limit").

7. **Sole-writer status is set at placement time, so E needs less runtime inference than quiescence does.** The coordinator creates a worker's worktree with `worker-start --worktree new-top-level|new-child` (`[G:pl] 15-21`). Whether that worker is the sole writer is a fact the coordinator fixes when it places the worker, not something it must infer later from `worker-list`, which has no worktree-to-writer map (diff A-003). Inside a sole-writer worktree, `git status` lists exactly that worker's changes, so a gap in the contract's file list (A-002) becomes detectable before staging instead of silently left behind.

8. **Crash recovery is the best of the field.** A worker crash mid-commit leaves a stale lock only in its own worktree (separate index, GITDEMO) and earlier per-task commits survive, which is #326's stated aim (V2 Recovery). No outward action can be half-done by a worker, because workers do none (V5 Recovery). A coordinator crash is A's case, no worse.

9. **Lowest implementation cost among variants that solve per-task commits.** Spec wording only in this spec's phases (WC-9, WC-11, 2.3, the `/sc:git` row, D4); no command changes, so SA-4's additive rule holds (`SPEC:172`). The commit step inside `/sc:implement` stays #326's K3 (`EVAL:63`), which E only bounds. B, the other per-task variant, needs command changes in every committing command (V2 Implementation cost).

10. **E is the only variant that names creation and removal of run worktrees and branches with a guard** (C-011): worktrees under `.dev/worktrees/` (`CLAUDE.md:299-302`), and no removal of an unmerged or open-PR branch without instruction (`EVAL:53`). Orca's `worker-stop`/`worker-release` never delete a worktree (`CAPS:115`), so without an owner the experiment worktrees #326 asks for leak.

#### Weaknesses identified in other variants

1. **A cannot absorb #326 K3 and stay A.** The per-task commit is a step inside `/sc:implement` (`EVAL:63`, K3), which runs in the worker. Once it exists, either A forbids it (and #326's per-task commits never happen) or A becomes E. A's own text defers to K3 (V1 "Honest limit"), so A is a stopping point, not an end state.
2. **A's single-session serialization scales badly with experiments.** Each experiment worktree ends on its own branch and the coordinator must commit in each (V1 weakness 4) while the same session may be blocked in a pr-submit wait of up to the 600 s budget (V1 Context load). Queued messages survive (`[G] 73-74`) but do not get answered.
3. **B is unsafe in the default layout and outward from workers.** Its own text: unsafe with a shared worktree (V2 "Honest limit"); workers share by default (`CAPS:115`). Its push/PR path needs D3 (b) against the spec's recommendation (`SPEC:343`). Its stale-lock step in a retry Task is "a step no command has today" (V2 Recovery).
4. **B scatters authorization across many briefs** (V2 Audit trail), and every outward action is second-hand. The diff's highest-severity points (C-003, C-004, X-001) all turn on this.
5. **C's persistence depends on a user request Orca will not infer.** `[G:rc] 157` allows retention only on the user's explicit wish, reuse needs immediate follow-up (`[G:cl] 48-50`), and a single long Task is ruled out by the worker contract ("After `worker_done`, end the dispatched turn and idle; do not poll", `[G] 91-93`). Without the request C degrades to "a fresh git worker per action" (V3 weakness 2), each paying a readiness start (`CAPS:44`).
6. **C moves PRs and pushes one hop from the person and onto D3 (b).** `SPEC:343` recommends (a). For outward actions C has exactly the hop E refuses to allow, while its gain (per-action audit) is a record of the hop, not a removal of it.
7. **C and D do not address per-task commits at all** (V3 weakness 4; V4 says nothing on it), the #326 owner's first ask (`EVAL:51`).
8. **D cannot perform the outward actions that dominate risk** (`sc-pr-submit-protocol/SKILL.md:47-49,82-84`; V4 weakness 1), so it is A plus a hop for local commits only, with no Orca record (V4 "No Orca record") and an unverifiable tool restriction (X-005).
9. **A, C and D share an undeclared hazard E surfaces: shared refs.** `/sc:implement` pins `refs/superclaude/implement/<slug>/T<id>` (`SKILL.md:113`), the slug is the package id in managed mode, and refs are shared across linked worktrees (GITDEMO). Two worktrees running the same plan (a natural #326 experiment) would write and delete the same pin names whoever owns commits. Only V5 names it (U-003). Its practical impact (a pruned tree before resume) is UNVERIFIED.

#### Concessions

1. **E's headline benefit is dormant until K3.** Today `/sc:implement` says acceptance never "authorizes commit, PR, merge or release" (`sc-implement-protocol/refs/managed-workspace.md:67`), and the in-run commit step is #326 K3 (`EVAL:63`). Until K3 lands, an E worker can commit only through steps its brief adds after the command finishes, which is one commit per run, not per task. In that interval E's practical difference from A is small: who writes the commit message.
2. **Two rule sets** (V5 weakness 1). The spec, the briefs and any test must state and check both the worker rule (four conditions) and the coordinator rule. A is simpler to state.
3. **E's recovery text overclaims one step.** V5 Recovery says "the retry Task (WC-6) checks for it [the stale lock] first", but no command has that step today (V2 Recovery says so explicitly). It must be written into the retry brief or WC-6; until then it is a manual step.
4. **"Sole writer" is narrower than V5 states.** It must also exclude the worker's own Agent-tool fan-out writing outside a batch, a person typing in that worktree's terminal (Orca lists "user-taken-over" terminals, `[G:rc] 160-161`), and any coordinator or hook writing there. V5 states only the parallel-batch case.
5. **A worker running raw git can still stage the wrong paths** (V5 weakness 2); only the coordinator's later review catches it before push. `/sc:git` cannot be the safer tool yet: it waits for confirmation on destructive operations (`commands/git.md:90`).
6. **More worktrees, more cleanup** (V5 weakness 3). E assigns the owner (row 2), but cleanup is still work.
7. **C has the better audit record** (X-002): one Orca Task per action beats contract SHAs plus a transcript.
8. **C is the only real fix for pr-submit blocking the coordinator** (C-009). E accepts A's mitigation (durable queues, `[G] 73-74`; pr-submit after workers finish, `SPEC:341`).
9. **A has the lowest implementation cost** (C-010).
10. **V5 is silent on Orca's review-ownership rule** (X-004, `[G:cl] 62-65`); V1 engages it honestly. E's answer (the coordinator does PR preparation only when the user's instruction names it, which makes the coordinator the named owner) is my reading, not text in V5.
11. **The quoted-brief hop is still a hop** (X-001). If the coordinator mis-quotes or broadens a grant, the worker cannot tell. E limits the damage to reversible local commits; it does not remove it.

#### Shared-assumption responses

- **A-001 (coordinator session is attended): QUALIFY.** All variants assume it, and none can enforce it. E reduces the cost of the assumption failing: if the person gives one instruction and leaves, E's workers can at most make local, reversible commits invisible outside the machine, and every push, PR and comment still waits for an instruction that names it (V5 row 1; `HOW-WE-WORK.md:282`). Under B and C an up-front grant reaches outward actions. The spec should state that an up-front grant names actions explicitly and that outward ones are not inferred.
- **A-002 (contract file lists are complete): REJECT as a safe basis for shared-worktree staging; QUALIFY for sole-writer worktrees.** A drive-by edit, a formatter rewrite or a generated cache can be missing from `artifacts` and `--files-modified` (`[G] 91`, "only with real values"). In a shared worktree the coordinator cannot distinguish a missing file from another worker's file, so it must stage explicit paths and report the leftovers, not sweep. In a sole-writer worktree `git status` lists exactly that worker's changes, so the worker (or the coordinator before merge) can compare it with the contract and close the gap.
- **A-003 (quiescence is knowable): QUALIFY.** Orca has no worktree-to-writer map; `worker-list` reports per Dispatch (`[G:rc]` "Inspect before acting"). The coordinator must keep the map from its own `worker-start --worktree ...` placements (`[G:pl] 15-21`). E needs that map only for shared worktrees; for worker commits the sole-writer fact is fixed at placement. Every variant that commits in a shared worktree (A, C, D, E) inherits this; the spec should make the placement map a coordinator duty in 2.3.
- **A-004 (a commit does not rewrite files): ACCEPT the diff's verdict (contradicted where hooks are installed).** Verified: `.pre-commit-config.yaml` has `trailing-whitespace` (line 9), `end-of-file-fixer` (line 11), `ruff-format` (line 111) and `default_stages: [commit]` (line 143); this clone's hooks directory (`/home/coder/workspaces/IronClaude/.git/hooks`, the common dir) holds only `*.sample` files (listed 2026-11-02). E is the variant least exposed: a worker commit rewrites only files in its own sole-writer worktree, and a coordinator commit happens only at quiescence, so no hook can rewrite a file another session is editing. A hook failure must still be handled (the commit is refused and the worker reports `failed` or `partial`); no variant specifies that.
- **A-005 (a standing instruction covers later commits): QUALIFY.** `CLAUDE.md:37` says only "commit only when asked". E scopes the grant per Task: the brief quotes the user's instruction "authorizing local commits for this Task" (V5 row 4, condition 1), so a standing instruction becomes per-Task authority the coordinator re-states in each brief and can withdraw by not quoting it. Outward actions get no standing grant under E beyond what the user's instruction names. The spec should say a standing commit instruction lasts for the named run only.

#### Per-point positions

| Point | Superior variant | One-line reason |
|---|---|---|
| S-001 | V5 (E) | A per-action table with owner and condition is directly testable and is what the spec's D4 and WC rows need. |
| S-002 | V3 (C) | Only C verifies Orca's reuse, serialization and retention mechanics (`[G:cl] 48-55`, `[G:rc] 108,157`). |
| S-003 | V1 (A) | V1 documents the GITDEMO procedure that every other variant relies on. |
| S-004 | V3 (C) | Only C relates its design to #326's "central relay" explicitly; E relates implicitly via F1/F3. |
| C-001 | V1 = V5 | Identical rule (coordinator, explicit paths, quiescent point); V1 originated it, V5 adds `.dev/tasks` staging (`CLAUDE.md:37`). |
| C-002 | V5 (E) | Per-task commits only in the window the ladder allows (`refs/retry.md:41`, `SKILL.md:97,114`) and only with a sole-writer guard B lacks. |
| C-003 | V1 = V5 | Outward actions in the coordinator's main chat match `/sc:pr-submit`'s top-level rule and D3 (a) (`SPEC:341,343`). |
| C-004 | V5 (E) | Direct authorization for outward actions plus a quoted brief only for reversible local commits is proportional; V1 is stricter but cannot do per-task commits. |
| C-005 | V3 (C) | One Orca Task, brief, `worker_done` and contract per action is the most complete record. |
| C-006 | V3 (C) | C removes both diffs and the pr-submit loop from the coordinator; E only removes per-task commit messages. |
| C-007 | V5 (E) | Lock scoped to one worktree, earlier commits survive, and no half-done outward action from a worker. |
| C-008 | V5 (E) | Works in Orca's default shared worktree (`CAPS:115`) and in experiment worktrees, without B's worktree-per-worker requirement. |
| C-009 | V3 (C) | The only variant that frees the coordinator during pr-submit waits, though at the cost of D3 (b). |
| C-010 | V1 (A) | Wording only, no new mechanism. |
| C-011 | V5 (E) | Only E names an owner and the F3 guard (`EVAL:53`); Orca never deletes worktrees itself (`CAPS:115`). |
| X-001 | V5 (E) | A quoted brief is sufficient for a reversible local commit (D4 (a), `SPEC:346`) but not for outward actions; E draws the line there. |
| X-002 | V3 (C) | Per-action Orca records beat a single transcript plus `git log`. |
| X-003 | V1 = V4 = V5 | Coordinator main chat is the only placement matching D3 (a), `SPEC:343` and `sc-pr-submit-protocol/SKILL.md:47-49`. |
| X-004 | V1 (A) | V1 alone reads `[G:cl] 62-65` honestly; E should adopt its reading (the user's instruction names the coordinator as owner). |
| X-005 | V1 (A) | A needs no tool restriction because no other actor runs git; D's claimed benefit is unverifiable. |
| A-001 | V5 (E) | If the person leaves, E's exposure is limited to reversible local commits; outward actions still need a named instruction. |
| A-002 | V5 (E) | In a sole-writer worktree `git status` exposes gaps in the contract list; in shared worktrees E stages explicit paths like A. |
| A-003 | V5 (E) | E's worker commits depend on a placement-time fact, not on runtime quiescence inference. |
| A-004 | V5 (E) | Both E commit paths (sole writer, quiescent coordinator) keep hook rewrites away from concurrent writers. |
| A-005 | V5 (E) | E scopes a standing commit grant per Task through the quoted brief and grants no standing outward authority. |

Tally: V5 superior on 15 points (three shared: C-001 and C-003 with V1, X-003 with V1 and V4), V3 on 6, V1 on 7 (three shared), V4 on 1 (shared). The 600 s wait is confirmed as a per-wait default (`commands/pr-submit.md:49`, `--timeout S` default 600). UNVERIFIED items carried: practical impact of the shared-ref slug collision for two runs of one plan in two worktrees; whether pre-commit hooks are installed in other clones.

## Round 2: Rebuttals
Sequential order A, B, C, D, E; each advocate read all Round 1 files and every earlier rebuttal.

### Round 2, advocate A (source: round2-advocate-a.md)

### Round 2 rebuttal: advocate A (variant 1, coordinator runs every git and GitHub action in its main chat)

Persona: architect plus analyzer. Date: 2026-11-02. Inputs read in full: `round1-advocate-a.md` .. `round1-advocate-e.md`, the five variants, `diff-analysis.md`. Citation keys as in the variants; `CC-HOOKS` = https://code.claude.com/docs/en/hooks (fetched this round, first 100k characters only).

#### 1. Response to criticisms

Every criticism of variant 1 raised in the four other Round 1 files, grouped where several advocates raised the same point. "Verified" means re-read this round.

| # | Criticism (raised by) | Response |
|---|---|---|
| R1 | A cannot make per-task commits inside one `/sc:implement` run. Once #326 K3 exists, the commit step runs inside the worker, so "A plus K3 is E" and A is a stopping point, not an end state (B weakness 1, E weakness 1, C critique of A) | **Conceded.** K3 is "the flag or step that performs per-task commits inside `/sc:implement`" (`issue-326-evaluation.md:63`, verified). That step runs in the worker, so pure A cannot absorb it. The spec has to fix K3's boundary now even though K3 is #326's feature: same row, same evaluation line, "The spec only fixes its boundary (F1 ...)". E's worker row is that boundary. This is the main reason I accept E as the merge base (section 2). |
| R2 | A depends on a quiescence map Orca does not provide (A-003) (B weakness 2, C, D, E) | **Partly conceded, partly rebutted.** True that no Orca verb maps worktrees to writers. But the coordinator creates every placement itself with `worker-start --worktree current \| new-child \| new-top-level` (`[G:pl] 15-21`, verified), so the map is the coordinator's own bookkeeping, not an inference. And the dependency does not go away under any variant. B concedes merges back into the shared branch still need it (B A-003 response). E's sole-writer predicate is the same placement fact. C's git session "cannot check it" (C A-003 response). The fix belongs in every option: section 2.3 should make the placement map a coordinator duty. |
| R3 | Explicit-path staging is only as good as the contract's self-reported file list (A-002) (B weakness 3, C, D) | **Conceded.** I added the remedy in Round 1 (`git status --porcelain` against the contract lists; report extras, never sweep). B is right that a sole-writer worker's own `git status` is ground truth, which is an E-row advantage. |
| R4 | A's foundation is partly a run-local rule (`SPEC:156` cites `.dev/orca-command-refactor/README.md:31`) (B weakness 4, B strength 7) | **Conceded in Round 1 (concession 2).** Repo policy is "commit only when asked" (`CLAUDE.md:37`, verified) and "a commit needs authorization" (`HWW:324`, verified). A's case never needed the prohibition. The evaluation also says per-task commits are "an authorized option, never a default" (`issue-326-evaluation.md:74`, verified), so the *default* stays A-shaped. |
| R5 | Owner work in the router: `[G:cl] 62-65` says the coordinator "routes and synthesizes" and PR preparation stays with the owner the user's plan names (B weakness 4, C weakness 2) | **Rebutted on the text, conceded on the spec wording.** The rule is conditional: "If the user's plan names a next owner ...", and "Dispatch or hand off fixes unless the user explicitly assigned them to the coordinator" (`[G:cl] 62-65`, verified). It does not forbid a coordinator owner. It requires that the plan *name* one. C's git session is legitimate under the same rule only if the plan names it, so C has no textual advantage. The spec's brief and run template should record the PR owner explicitly. |
| R6 | The coordinator becomes a single point of delay during `/sc:pr-submit`: 600 s per-wait budget over up to 5 rounds, worker `ask`s time out meanwhile, and "after the workers finish" rules out PR work while workers run (C weakness 1, E weakness 2) | **Partly conceded.** The budget is real (`commands/pr-submit.md:47,49`, verified). A timed-out `ask` is resumed by message ID, not lost (`[G] 80-82`, verified). That is delay, not loss. New evidence (section 3, N1): pr-submit is built to stop and resume ("Durability comes from the write-ahead JSONL run-log + `--resume`", `sc-pr-submit-protocol/SKILL.md:44`; `--resume <jsonl>`, `commands/pr-submit.md:56`, both verified). That bounds the cost, but HOW-WE-WORK discourages stopping a skill halfway (`HWW:278`, verified). So it is a recovery path, not a scheduling tool. I concede that when PR work must overlap running workers, or several PRs must be monitored at once, a D3 (b) opt-in is better. I accept that opt-in in section 2. |
| R7 | Outward actions under A have no Orca outcome; Orca ranks a transcript below a Dispatch for lifecycle authority (`[G] 53-54`) (C weakness 3) | **Rebutted in part.** `[G] 53-54` (verified) is about Orca lifecycle authority: which Dispatch may report. C itself calls applying it to audit an inference. The authoritative record of a push or PR is GitHub itself (SHA on origin, PR URL) plus pr-submit's write-ahead run-log `monitor-run-<PR>.jsonl`, which the spec already makes the contract artifact (`SPEC:137`, verified). Both exist under A. I keep the Round 1 concession that C's per-action Task record is the better *Orca* record (X-002). |
| R8 | Coordinator crash loses the actor and the record together; a stale lock lands in the shared worktree where every worker writes (C strength 7, B strength 4) | **Rebutted.** The record survives: the Run is durable (`[G] 51-52`, verified), and pr-submit's run-log survives for `--resume` (N1). A stale `.git/index.lock` in the shared worktree blocks no worker under A, because workers never write the user index. Even `/sc:implement`'s Q0 snapshot uses a private temporary index, "**without** staging in the user index" (`sc-implement-protocol/SKILL.md:110-111`, verified). Whether git locks only `$idx.lock` there is documented behaviour I did not run: UNVERIFIED. I concede that C's crash *detection* is better (Orca liveness, `CAPS:122-126`). |
| R9 | A has no mechanical boundary: its safety is the model's prose discipline in the session with the most context and full Bash, and the repo itself says prose is not enough (`CLAUDE.md:31`) (D weakness 1) | **The premise is verified, the conclusion rebutted.** `CLAUDE.md:31` says the existing gates miss `git add -f` and hand-edited commands (verified). But a mechanical guard is not unique to a subagent. Settings-level hooks "also run inside subagents" *and* in "the main conversation", and receive `agent_type` (CC-HOOKS, fetched). The repo already runs settings-level `PreToolUse` hooks in main sessions (`.claude/settings.json:3-21`, verified: `Write\|Edit` and `Skill` matchers). In this very session a user-level `PreToolUse` hook blocked my own Edit ("FRESHNESS BLOCK"). So A's coordinator can carry a `Bash` deny-list hook (`git add -A`, `git add .`, `-f`, `.claude/` paths other than `settings.json`, `--no-verify`, `push` outside pr-submit) without blocking its other Bash use. **Conceded:** D's subagent-scoped *allowlist* is stricter than a main-chat *deny-list*. Both share D's open question: whether exit 2 still blocks under `bypassPermissions`, on which CC-HOOKS says nothing in the part I read (UNVERIFIED). |
| R10 | Ambient authority: the git-holding session also reads worker reports that could carry injected text (D weakness 1) | **Conceded as real, but not specific to A.** Under C, D and E-shared rows, the git actor's instructions are written by the same coordinator after reading the same reports. Only a mechanical guard (R9) bounds it, and that guard is available to A. |
| R11 | A serializes commits for N experiment worktrees through one session (B strength 5, E weakness 2) | **Rebutted on magnitude.** A local commit takes seconds. A fresh worker start alone has a 60 s readiness budget (`CAPS:44`, verified in Round 1). The serial cost that matters is N pr-submit loops, which is R6's opt-in, not local commits. |
| R12 | Hooks may rewrite files during a shared-worktree commit (A-004) (B weakness 8) | **Rebutted for A, conceded on scope.** A commits only at quiescence, so no worker is editing then. D is right that quiescence must cover *every* writer in that worktree, not only `/sc:implement` workers. A hook failure must stop and report. It must never be retried with `--no-verify` ("Never turn off a quality check", `HWW:280`, verified). |
| R13 | A's "same session" advantage shrinks to an up-front grant when the person leaves (A-001) (B, C, D, E) | **Conceded in Round 1 (concession 6).** See the updated A-001 below: D adds that under a `bypassPermissions` parent no prompt reaches anyone, which makes a mechanical guard (R9) more important for A too. |
| R14 | Shared `refs/superclaude/implement/<slug>/...` pins collide across linked worktrees, a hazard A did not declare (E weakness 9) | **Conceded, with a correction that strengthens E's point.** Workers write these refs *whoever owns commits*: `git update-ref` at Q0 and at `complete` (`SKILL.md:113,116`), sweep refs (`refs/retry.md:371,431`), and `git restore --worktree` on a revert (`refs/retry.md:398`), all verified. So the slug-distinctness rule must be in the spec under every option, A included. |

#### 2. Updated assessment of the other variants

**Decision: I accept E as the merge base.** With no commit grant in any brief, E *is* A: every outward action and every shared-worktree commit stays with the coordinator at a quiescent point (V5 table rows 1, 3, 5). So accepting E gives up nothing A argued for on outward actions or the default layout. It adds the one row A cannot supply, the K3 boundary (R1). I accept it on four conditions. Each condition comes from evidence already in the debate.

1. **The worker-commit row is off by default and scoped.** Per-task commits are "an authorized option, never a default", and the owner's issue comment "does not by itself authorize commits in a worker" (`issue-326-evaluation.md:74`, verified). The row applies only when the brief quotes a user instruction naming local commits, this run and this branch (A-005). It never covers push, merge or PR (`HWW:282`, verified).
2. **"Sole writer" is a placement fact the coordinator records.** The worker must have been started with `--worktree new-child` or `new-top-level` for that Task (`[G:pl] 15-21`). The coordinator's placement map lists no other writer there. E's own concession 4 is included: no Agent-tool fan-out outside a batch, no user-taken-over terminal, no hook writing there.
3. **Until K3 lands, the row is dormant in practice.** E concedes a worker can then commit only "through steps its brief adds after the command finishes" (V5 cost; E concession 1). The spec should say so plainly instead of implying per-task commits exist.
4. **The worker invariant is restated precisely.** Workers never write the user index, never commit and never move HEAD or touch remotes, unless the E row applies. They already write refs and restore files in the ordinary course of `/sc:implement` (R14). Slugs must be distinct per run.

**B (now "E plus a D3 (b) exception").** B's move is honest: it dropped worker pushes, PRs and comments (B concessions 2, 7). What is left of B is E's worker row plus parallel PR monitoring. I reject B's Round 2 plan to shrink E's shared-worktree coordinator row in favour of "put committing work in its own worktree". Orca's default is to share: "Create a worktree only when the user requested one or a concrete checkout or filesystem conflict makes sharing unsafe" (`[G:pl] 8-11`, verified). Report-only workers have no such conflict. A worktree per committer also costs setup: `--setup run` (`[G:pl] 18,21`) and, per EVAL F2, `make sync-dev` in each new worktree (`issue-326-evaluation.md:52`, verified). B's claim that its layout removes A-003 is also overstated, because merges still need the map (B's own A-003 response).

**C (now "C for outward actions plus E for local commits").** C makes the best case against A on responsiveness and audit, and I keep my concessions on C-005 and X-002. I do not accept a dedicated git session as the *default* owner of outward actions:
- the spec recommends D3 (a) "unless parallel PR monitoring is a real need" (`SPEC:343`, verified);
- pr-submit run as a worker turns operator HALTs into `blocked` (`SPEC:137`, verified), which removes the person from a loop designed as "attended, in-session" (`sc-pr-submit-protocol/SKILL.md:43`, verified);
- one git session serializes PR loops anyway (B's critique of C), so it does not give parallel monitoring;
- C itself concedes the spec forbids it twice as written (C concession 1) and that retention is a stretch of `worker-retain`'s debugging purpose (C concession 3).

**What I accept from B and C together, as one opt-in:** when the user asks for parallel PR monitoring, or for PR work that overlaps running workers, apply D3 (b) with **one pr-submit Task per PR**. That uses C's per-action Task shape and record, and gives B's parallelism. The Task is not a long-lived session, so it needs no retention. The brief quotes the user's instruction naming the PR (D4 (a), `SPEC:346`). Without that request, outward actions stay in the coordinator's main chat.

**D (now "D as E's/A's committer mechanism with a PreToolUse hook").** I accept D as an **optional mechanism, not a spec dependency.** D's corrected Strength 1 is a real improvement on V4: `disallowedTools` with a specifier does not work; the frontmatter `hooks` field does (D, citing CC-SUB). But three things keep it optional:
- the same guard can run as a settings-level hook in the coordinator's main chat (R9);
- whether exit 2 blocks under `bypassPermissions` is UNVERIFIED (D concession 3; CC-HOOKS silent in the part I read);
- subagent hooks are ignored for plugin agents and wait on workspace trust for project agents (D concession 4; CC-HOOKS, fetched: "Frontmatter hooks in a project subagent run only after you accept the workspace trust dialog").

The spec should name the guard as a recommended control, and test it under the run's permission mode, before any rule depends on it.

**Merged shape I will argue for in Round 3:** E's table as written, plus the four conditions above, the D3 (b) per-PR opt-in, the placement-map duty (R2), the porcelain cross-check (R3), quiescence covering every writer (R12), the explicit PR-owner line (R5), and the git guard hook as a recommended, tested control.

#### 3. New evidence

None of the following appeared in any Round 1 file. All of it was verified this round.

- **N1. pr-submit is designed to resume from a write-ahead log.** "The monitor is an **attended, in-session** loop: closing the session loses it. Durability comes from the write-ahead JSONL run-log + `--resume`, never from detachment" (`src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:43-44`). The flag is `--resume <jsonl>`, "Reconstruct state from a write-ahead run-log" (`src/superclaude/commands/pr-submit.md:56`; usage at line 39). This bears on C-007 and C-009: a coordinator crash does not lose a PR loop's state. It does not license routinely stopping the loop to serve workers, because `HWW:278` says "Let a skill finish".
- **N2. Main-session `PreToolUse` hooks give A a mechanical git guard.** CC-HOOKS: hooks from settings files "also run inside subagents", tool events fire "the same configured hooks as in the main conversation", and the input carries `agent_id` / `agent_type`. Exit 2 "blocks the tool call", even over a JSON "allow". The repo already registers main-session `PreToolUse` hooks (`.claude/settings.json:3-21`). A user-level `PreToolUse` hook blocked an Edit in this session. This undercuts D's claim that only a subagent can carry a per-actor guard, though D's allowlist remains stricter. Under `bypassPermissions`: UNVERIFIED (not in the 100k characters read).
- **N3. Workers already run mutating git, just not on the user index or HEAD.** `/sc:implement` snapshots "**without** staging in the user index" using a temporary `GIT_INDEX_FILE` (`sc-implement-protocol/SKILL.md:110-111`). It writes and deletes refs (`SKILL.md:113,116`; `refs/retry.md:371,431`). It rewrites working-tree files on a revert with `git -C "$top" restore --source="$START" --worktree` (`refs/retry.md:398`). Variant 1's phrase "Workers never run a mutating git command" is therefore inaccurate. The real invariant every variant relies on is: workers never write the user index, never commit, and never move HEAD or touch remotes (except under E's row). It also confirms that E's shared-refs hazard (U-003) exists under every ownership option.
- **N4. The evaluation already rules on the default.** Per-task commits are "allowed as an authorized option, never a default", and the #326 owner's comment "does not by itself authorize commits in a worker" (`issue-326-evaluation.md:74`). This fixes A-005's scope and makes E's worker row default-off.
- **N5. `/sc:git` routing text separates commit from outward steps.** "Status-only stays inspection; a commit needs authorization. Do not append push, merge or PR creation" (`HWW:324`). This supports E's split between local commit (authorizable) and outward actions (separately named).
- **N6. Credit to D, verified:** the spec's WC-7 cites the pr-submit top-level rule at `sk/sc-pr-submit-protocol/SKILL.md:37-39` (`SPEC:71`). The rule is now at lines 47-49. The merged spec should fix that citation.

#### 4. Updated shared-assumption responses

All five responses stay **QUALIFY**. The reasons changed for A-001, A-003, A-004 and A-005. A-002 is unchanged (porcelain cross-check; never sweep).

| ID | Response | What changed |
|---|---|---|
| A-001 (coordinator attended) | **QUALIFY** | D showed that under a `bypassPermissions`, `acceptEdits` or `auto` parent, prompts reach no one (D concession 3). So an unattended coordinator's only remaining control is a mechanical one: a settings-level or subagent git guard (N2), still UNVERIFIED under bypass. E is now my preferred handling: with the person absent, a scoped grant can authorize at most reversible local commits, and outward actions still need an instruction that names them. |
| A-003 (quiescence knowable) | **QUALIFY** | The map comes from the coordinator's own `worker-start --worktree ...` calls (`[G:pl] 15-21`), so it is bookkeeping, not inference. Every variant needs it (merges under B, shared rows under E, briefs under C). The spec should make it a section 2.3 coordinator duty. |
| A-004 (commit does not rewrite files) | **QUALIFY** | Quiescence must cover every writer in the worktree, not only `/sc:implement` workers (from D). A hook rewrite or failure is stop-and-report and never `--no-verify` (`HWW:280`). |
| A-005 (standing instruction covers later commits) | **QUALIFY** | Now anchored in `issue-326-evaluation.md:74`: never a default, and an issue comment is not authorization. A standing grant covers local commits only, for the named run and branch, quoted in each brief, and never pushes (`HWW:282`). |

#### 5. Updated per-point table

| Point | Superior variant | Changed from Round 1? | Reason |
|---|---|---|---|
| S-001 | V5 (E) | No | The per-action owner/condition table is the merge base's form. |
| S-002 | V3 (C) | No | Only C verified Orca reuse, serialization, retention and idle-rule mechanics. |
| S-003 | V1 (A) | No | GITDEMO is the procedure everyone cites (not re-run this round: UNVERIFIED). |
| S-004 | V3 (C) | No | Only C explains why the #326 relay cannot be something commands call. |
| C-001 | V5 (E), rule originated in V1 | Yes (was V1) | Identical rule; E also states `.dev/tasks` staging and is the merge base. D's guard is an optional mechanism on top. |
| C-002 | V5 (E) | No | Only E times commits in the ladder-safe window with a sole-writer guard; dormant until K3. |
| C-003 | V1 = V5 | No (now shown as a tie) | Coordinator main chat by default; D3 (b) per-PR Task only on explicit request. |
| C-004 | V5 (E) | Yes (was V1) | A scoped, quoted, default-off grant is proportionate for reversible local commits (`issue-326-evaluation.md:74`); outward actions stay direct. |
| C-005 | V3 (C) | No | Per-action Orca Task record is the strongest audit; adopted for the D3 (b) opt-in. |
| C-006 | V4 (D) | No | Commit diff reading moves out of the coordinator without Orca cost; optional. |
| C-007 | V5 (E) | No | Lock confined to one worktree, earlier commits survive; pr-submit state survives via `--resume` under any owner (N1). |
| C-008 | V5 (E) | Yes (was V1) | E behaves as A in the default shared layout and safely in experiment worktrees; B's worktree-per-committer is rejected. |
| C-009 | V1 (A) default, D3 (b) per-PR opt-in | No (qualified) | Attended top-level loop by default (`SKILL.md:43`, `SPEC:343`); parallel or overlapping PR work uses one pr-submit Task per PR on request. |
| C-010 | V1 (A) | No | Wording only; E's spec cost is also wording only, so the gap is small. |
| C-011 | V5 (E) | No | Only E names the owner and the F3 guard. |
| X-001 | V5 (E) | Yes (was V1) | A quoted, scoped brief suffices for a reversible local commit; never for outward actions. |
| X-002 | V3 (C) | No | Per-action Orca records beat a transcript; GitHub and the pr-submit run-log remain the record for outward actions (R7). |
| X-003 | V1 = V4 = V5 | No | Coordinator main chat matches D3 (a) and pr-submit's top-level rule. |
| X-004 | V1 (A) | No | The rule is conditional on a named owner (`[G:cl] 62-65`); the fix is to name the PR owner in the plan, which no variant's mechanism replaces. |
| X-005 | V4 (D), as amended | Yes (was V1) | The frontmatter `hooks` mechanism makes the narrow-tool claim real; the same guard is also available in the main chat (N2); bypass behaviour UNVERIFIED. |
| A-001 | V5 (E) | Yes (was V1) | With the person gone, E caps exposure at reversible local commits; A's edge depends on attendance. |
| A-002 | V5 (E) | No | A sole-writer worker's `git status` is ground truth; shared rows use the porcelain cross-check. |
| A-003 | V5 (E) | Yes (was V1) | Worker commits rest on a placement-time fact (`[G:pl] 15-21`); shared rows need the same map A keeps. |
| A-004 | V5 (E) | Yes (was V1) | Both E commit paths keep hook rewrites away from concurrent writers, given quiescence over every writer. |
| A-005 | V5 (E) | Yes (was V1) | Per-Task quoting of a scoped, default-off grant (`issue-326-evaluation.md:74`). |

**Tally:** E 13 alone plus 2 shared (C-003, X-003), A 4 alone (S-003, C-009, C-010, X-004) plus 2 shared, C 4, D 2 (C-006, X-005) plus 1 shared, B 0. Nine points changed (C-001, C-004, C-008, X-001, X-005, A-001, A-003, A-004, A-005), all toward E or D. **Overall:** A's substance on outward actions, shared-worktree commits and the default survives intact inside E. A as a standalone rule does not, because the spec must fix K3's boundary now.

### Round 2, advocate B (source: round2-advocate-b.md)

### Round 2 rebuttal: advocate B (variant 2, workers run their own git under brief rules)

Persona: backend (data integrity, scalability, fault tolerance) plus analyzer (evidence quality). Date: 2026-11-02.
Inputs read in full: `round1-advocate-a.md` .. `round1-advocate-e.md`, `round2-advocate-a.md`, the five variants, `diff-analysis.md`.
Citation keys as in the variants. "Verified" means re-read this round with `sed -n`, `grep -n` or `orca-ide skills get orchestration --reference references/<name>.md | cat -n`. Protocol behaviour derived from text but not run is marked UNVERIFIED (live).

#### 1. Response to criticisms

Every criticism of variant 2 in the four other Round 1 files and in A's Round 2 file, grouped where several advocates raised the same point.

| # | Criticism (raised by) | Response |
|---|---|---|
| B1 | B is unsafe in Orca's default shared worktree: two committers collide on `index.lock`, `git add -A` sweeps other workers' files, and a commit moves HEAD and halts running implement tasks (A R1 critique and weakness 1; C critique 1, weakness 4; D critique; E critique, weakness 3) | **Conceded (Round 1 concession 1).** B is correct only with one committing writer per worktree. I add one point here. Section 3 (N1) shows that, independent of who commits, a `/sc:implement` worker whose retry ladder can revert must not share a worktree with any other source writer. The placement condition B needs is therefore one the spec needs anyway, for a reason unrelated to git ownership. |
| B2 | B forces a worktree per committing worker, against Orca's placement default "Use the current or an exact existing workspace by default. Create a worktree only when the user requested one or a concrete checkout or filesystem conflict makes sharing unsafe" (A R1 and R2 section 2; C critique 1; D critique; E critique) | **Partly conceded, partly rebutted.** Quote verified at `[G:pl] 8-11`. Conceded: a blanket "worktree for every committing worker" is wrong for report-only workers, whose WC-11 report directories (`SPEC:75`, verified) give them no conflict. Rebutted: the rule's own exception, "a concrete checkout or filesystem conflict makes sharing unsafe", is met by two cases. (a) A worker granted local commits: its commits move the shared HEAD (`retry.md:41,44`). (b) An implement worker whose revert can delete or restore other workers' files (N1). So my plan in section 2 is narrowed to those two cases, which Orca's own text licenses. |
| B3 | A worktree per committer has a setup cost: `--setup run` (`[G:pl] 18,21`) and `make sync-dev` in each new worktree (EVAL F2) (A R2 section 2) | **Conceded on cost, rebutted on the alternative.** Verified: `[G:pl] 18,21` pass `--setup run` for `new-child` and `new-top-level`; `issue-326-evaluation.md:52` requires "the same setup the 7.2 check needs ... `make sync-dev` run there". The cost is real, and it is paid once per worker, not per commit. The alternative for an implement worker sharing a worktree is either the N1 hazard or switching the retry ladder off. That trades a known one-time setup cost for a silent data-integrity risk, and "Never turn off a quality check" (`HWW:280`, verified) argues against switching the ladder off. |
| B4 | Outward actions from workers multiply what WC-9 is built to switch off, and need D3 (b), which the spec does not recommend (A, C, D, E) | **Conceded (Round 1 concession 2).** WC-9 (`SPEC:73`, verified) and D3's recommendation of (a) "unless parallel PR monitoring is a real need" (`SPEC:343`, verified) stand. B keeps only the parallel-PR case. A's Round 2 proposal (one pr-submit Task per PR, on explicit user request) is a better shape than B's, so I adopt it in place of B's version (section 2). |
| B5 | Authorization is second-hand and "spread over many briefs and transcripts" (D weakness 2; E weakness 4; A weakness 6, briefs cannot change after creation, `SPEC:70`) | **Conceded for outward actions; bounded for local commits.** Briefs are immutable (`SPEC:70`, verified), so a revoked grant persists until a new Task replaces it. For a local, unpushed commit the damage of a stale grant is bounded: the commit stays local and the coordinator can drop it before any push. With A's condition 1 (default-off, quoted, scoped to run and branch) and SHAs in the contract, every worker commit traces to one quoted grant in one brief. The "scattered" objection then reduces to "one brief per granted Task", which is the same per-action record C is credited for (C-005). |
| B6 | Highest implementation cost; every committing command needs a commit step, a stale-lock rule and SHA fields, against SA-4's additive rule (`SPEC:172`); implement says acceptance never authorizes a commit (`managed-workspace.md:63,67`) (A strength 4; C critique 3, weakness 6; D weakness 2; E critique) | **Conceded.** Under the merge base, the in-run commit step is #326's K3 (`issue-326-evaluation.md:63`, verified), not a spec P1-P3 change. That moves B's main cost out of this spec. The cost that remains is spec wording plus one placement rule (section 2). |
| B7 | Merges back still need a single owner, so B is never complete alone, and B's claim to remove A-003 is overstated because merges need the placement map (A R1 critique, R2 section 2; C critique 4) | **Conceded.** A merge into the shared branch moves the main worktree's HEAD, so it needs that worktree to be quiet, which needs the coordinator's placement map. I narrow the claim: worker commits in a sole-writer worktree need no quiescence map at commit time. The coordinator's merges still need it. |
| B8 | B's stale-lock recovery is "a step no command has today" (E weakness 3; V2's own Recovery) | **Conceded, with a safer replacement.** A worker should not delete a lock on its own judgement that "no git process runs", because a wrong judgement deletes a live lock. Proposed rule: a retry Task that finds `index.lock` in its own worktree stops with `worker_status: blocked` and names the path. The coordinator, or the person, removes the lock after checking. This needs no new command step: a blocked contract is already a WC-4 outcome (`SPEC` WC-4 row, verified). |
| B9 | A stale lock from a coordinator crash blocks no worker under A, because workers never write the user index; `/sc:implement`'s Q0 uses a private temporary index (`SKILL.md:110-111`) (A R8, against B strength 4) | **Conceded.** Verified: Q0 snapshots "**without** staging in the user index" with `GIT_INDEX_FILE="$idx"` (`SKILL.md:110-111`). My Round 1 claim that a coordinator crash leaves the lock "where every worker writes" was wrong for the index. B strength 4 is reduced to the survival of earlier commits, which E has too. |
| B10 | Serializing N experiment commits through one session costs seconds, not minutes; the serial cost that matters is N pr-submit loops (A R11, against B strength 5) | **Conceded.** Local commits are cheap to serialize. B's throughput argument survives only for PR monitoring, and the per-PR-Task opt-in covers that. |
| B11 | B has the biggest attack surface: every committing worker holds mutating git, with no mechanical guard (D critique and weakness 2) | **Partly conceded.** Under the merge base a granted worker holds local-commit authority only, in its own worktree, and never pushes. D's guard can bound it further: a settings-level `PreToolUse` hook runs in any Claude session, including an Orca worker's top-level session (A's N2, citing CC-HOOKS; I did not fetch CC-HOOKS this round, UNVERIFIED by me). A deny-list for push, `gh pr`, `--no-verify` and `-f` costs the worker nothing it needs. Whether exit 2 still blocks under `bypassPermissions` remains UNVERIFIED (D concession 3). |
| B12 | B missed the shared-refs hazard (`refs/superclaude/implement/<slug>/T<id>`) (E weakness 9; A R14) | **Conceded (Round 1 concession 5).** A's correction holds: workers write these refs whatever the commit ownership (`SKILL.md:113,116`, verified). Distinct slugs per run must be a spec rule under every option. |

#### 2. Updated assessment of the other variants

**Decision: I accept E plus A's four conditions as the merge base.** I also accept the D3 (b) per-PR opt-in and D's guard as an optional, tested control. Each condition matches a concession B already made.
- Condition 1 (default-off, scoped, quoted grant): matches `issue-326-evaluation.md:74` (verified): per-task commits are "allowed as an authorized option, never a default".
- Condition 2 (sole writer is a recorded placement fact): what B called "one worker per worktree".
- Condition 3 (dormant until K3): B concession 4.
- Condition 4 (worker invariant, distinct slugs): B12.
- One pr-submit Task per PR on explicit request replaces B's broader worker-PR claim (B4).

**What I still argue: my Round 1 plan, narrowed to what the evidence supports.** I withdraw "committing work should go in its own worktree by default" as a blanket rule; A is right that report-only workers should share (B2, B3). I keep, and now ground in new evidence, a placement rule with two triggers:

> **P1 (placement).** The coordinator places a worker in its own worktree (`--worktree new-child` or `new-top-level`) when either (a) its brief grants local commits, or (b) it runs `/sc:implement` with the retry ladder able to revert while any other worker writes outside `.dev/` in the same worktree. Report-only workers share the current worktree as Orca's default says.

Why this is more than a restatement of condition 2:
1. **Trigger (b) is needed whoever owns git.** N1 below shows that implement's revert can delete or restore another worker's files in a shared worktree. Under pure A, C or D the hazard is unchanged, because it comes from the ladder, not from commits. The spec's WC-11 ("Two workers in one worktree must never write the same file", `SPEC:75`, verified) is silently broken by the revert, which writes files the task never wrote.
2. **With P1, E's shared-worktree coordinator row shrinks to its safe core.** Once implement workers are not in the shared worktree:
   - the shared worktree holds report-only workers, which write their own WC-11 report directories;
   - the coordinator's explicit-path staging is then a list of report directories, so A-002 has little to miss;
   - no implement ladder runs there, so a coordinator commit cannot cause `head-moved` (`retry.md:41,44`).

   That is what I meant by making the coordinator's shared-worktree commit "the exception". It remains in the table, but only for the low-risk case.
3. **Orca's text licenses it.** Both triggers are "a concrete checkout or filesystem conflict" (`[G:pl] 8-11`, verified). P1 does not override Orca's default. It names the conflicts the coordinator must recognise.
4. **Cost.** P1 adds one `--setup run` and the F2 setup per isolated worker (B3). This is the price of keeping the retry ladder on (`HWW:280`).

**A (now inside E).** A's Round 2 is the most useful file in the debate, and I agree with its merged shape. A rejected my Round 1 plan for two reasons: the default is to share, and setup costs. Both apply to the blanket version, which I have withdrawn. Neither addresses trigger (b), which A did not consider. A's R8 rests on Q0 using a private index (`SKILL.md:110-111`). Its own N3 says the same protocol "rewrites working-tree files on a revert" (`retry.md:398`, per A; I verified the step at `retry.md:220`). That is the N1 hazard. A noted it as a fact about refs but not as a hazard to other workers' files.

**C.** I keep C's wins on S-002, S-004, C-005 and X-002. I accept A's case against a long-lived git session as the default outward owner. A's case has four parts: pr-submit as a worker turns operator HALTs into `blocked` (`SPEC:137`, verified); the loop is "attended, in-session" (`sc-pr-submit-protocol/SKILL.md:43`, verified); one git session serializes PR loops; and retention stretches `worker-retain`'s purpose (C concession 3). The per-PR Task opt-in keeps C's per-action record without retention.

**D.** I accept D's guard as optional and tested, as A proposes. For B's lane specifically, a settings-level deny-list in the worker session is the relevant form (B11). A subagent allowlist does not apply to a worker's own commits.

**E.** E is the base. It still needs three additions from this round:
- P1 (above), which E's "sole writer" condition presumes but never places;
- E's own concession 4, that "sole writer" also excludes user-taken-over terminals and hooks;
- B8's blocked-on-lock rule in place of E's "retry Task checks for it first" (E concession 3).

#### 3. New evidence

None of these points appears in any Round 1 file or in A's Round 2 file as stated here. All were verified this round.

- **N1. `/sc:implement`'s revert can delete or overwrite other workers' files in a shared worktree.**
  - **The domain.** "Domain = every path printed by `git -C "$top" diff -z --no-renames --name-only "$start" "$now"`", minus fixed exclusions (`src/superclaude/skills/sc-implement-protocol/refs/retry.md:201`). `now` is a fresh whole-worktree snapshot taken at revert time (`retry.md:199`). So any path another worker changed in that worktree after this task's Q0 is in the domain.
  - **The exclusions.** They protect the run dir, ledger, retries dir, source file, `.dev/troubleshoot/`, other `.dev/` paths not in this task's `files=`, and submodules (`retry.md:202-208`). They do not protect any other worker's file outside `.dev/`.
  - **Step 5.** It restores each domain path that existed at `$start` (`git restore --source="$start" --worktree`). It deletes each one that did not ("Otherwise `rm -f -- "$top/$p"`", `retry.md:220`).
  - **Consequence.** In a shared worktree, a concurrent worker's source edits are reverted, and its new files are deleted. One example is `/sc:research`'s `claudedocs/research_*.md` (`src/superclaude/commands/research.md:103`, verified), which is outside `.dev/`. The content survives only in the sweep ref pinned at step 3 (`retry.md:218`).
  - **Why the guard misses it.** Check 2 (the batch guard) looks only at this ledger's own tasks: "read from the ledger on every check" (`retry.md:40`). It cannot see other Orca workers.
  - **Second effect.** Step 6 flags "every path that `git -C "$top" diff --name-only "$now" "$v"` lists outside the domain" as residue (`retry.md:221`). A concurrent writer during a revert therefore also causes a spurious `E-RESUME-NEEDED` stop.
  - **Spec coverage.** `grep -n -i revert` over the spec returns nothing (verified), so the spec does not address this.
  - **Status.** The hazard follows from the protocol text but has not been observed in a run: UNVERIFIED (live). It exists under every ownership option. It is the strongest evidence that implement workers belong in their own worktree, and once they are there, E's worker-commit lane is available to them at no extra placement cost.
- **N2. WC-11 is the spec's only parallel-write rule, and N1 breaks it.** WC-11: "Two workers in one worktree must never write the same file" (`SPEC:75`, verified). The revert writes files the task never wrote, so WC-11 cannot be met by output-path discipline alone while an implement worker shares a worktree. P1 trigger (b) is the minimal fix.
- **N3. The evaluation's F2 line already draws the boundary P1 extends.** "Workers that edit the same source files as alternative attempts (an experiment) each get their own worktree ...; workers that write only their own report directories share the current worktree" (`issue-326-evaluation.md:52`, verified). P1 adds two triggers to F2's experiment case, granted commits and an active implement ladder, and keeps F2's sharing rule for report-only workers.
- **N4. A lock-deleting retry step is riskier than a blocked outcome.** The spec already has a `blocked` `worker_status` with `blocked_question` (`SPEC` WC-4 row, verified). Routing a found `index.lock` to `blocked` (B8) keeps lock removal with the coordinator or person, who can check for a live git process. No worker then deletes a lock on its own inference.

#### 4. Updated shared-assumption responses

A-002 is unchanged (REJECT as a basis for staging; stage from `git status` in a sole-writer worktree, porcelain cross-check elsewhere).

| ID | Response | What changed |
|---|---|---|
| A-001 (coordinator attended) | **QUALIFY** | I now prefer E's handling explicitly. With the person absent, a default-off grant (`issue-326-evaluation.md:74`) caps exposure at reversible local commits, and every outward action still needs an instruction that names it. |
| A-003 (quiescence knowable) | **QUALIFY** | Accept A's point that the map is the coordinator's own placement bookkeeping (`[G:pl] 15-21`, verified), and that merges need it under B too (B7). New: for an implement worker, "quiet" must hold for the **whole run**, not only at commit time. A revert can fire at any failed review (N1), so a commit-time check is not enough. P1 makes that true by placement. |
| A-004 (commit does not rewrite files) | **QUALIFY** | Add the agreed rule: a hook rewrite or failure is stop-and-report, never `--no-verify` ("Never turn off a quality check", `HWW:280`, verified). A worker in its own worktree reports `partial` or `blocked`. |
| A-005 (standing instruction covers later commits) | **QUALIFY** | Now anchored in `issue-326-evaluation.md:74` (verified): an authorized option, never a default, and an issue comment is not authorization. A standing grant covers local commits only, for the named run and branch, quoted in each brief, and never pushes. |

#### 5. Updated per-point table

| Point | Superior variant | Changed from Round 1? | Reason |
|---|---|---|---|
| S-001 | V5 (E) | No | The per-action owner/condition table is the merge base's form. |
| S-002 | V3 (C) | No | Only C verified Orca reuse, serialization, retention and idle-rule mechanics. |
| S-003 | V1 (A) | No | GITDEMO is the procedure everyone cites. |
| S-004 | V3 (C) | No | Only C explains why the #326 relay cannot be something commands call. |
| C-001 | V5 (E), with P1 | No (qualified) | Coordinator commits in a shared worktree at quiescence; P1 keeps implement ladders out of that worktree, so the row is safe (N1, N2). |
| C-002 | V5 (E) | Yes (was V2 tie V5) | E's row with A's four conditions is B's rule with the guards B lacked; dormant until K3. |
| C-003 | V1 = V5 | Yes (was V5) | Shown as a tie: coordinator main chat by default; one pr-submit Task per PR only on explicit request. |
| C-004 | V5 (E) | No | Direct for outward actions; scoped, quoted, default-off grant for reversible local commits. |
| C-005 | V3 (C) | No | Per-action Orca Task record; adopted for the per-PR opt-in. |
| C-006 | V5 (E) | Yes (was V2) | E keeps B's "read SHAs, not diffs" benefit for granted workers and adds nothing to outward load; B's lead depended on worker PRs, now dropped. |
| C-007 | V5 (E) | No | Lock confined to one worktree, earlier commits survive; with the B8 refinement (blocked, not lock deletion). |
| C-008 | V5 (E), with P1 | No (qualified) | Sole-writer worker commits plus shared default for report-only workers; P1 names when isolation is required. |
| C-009 | V1 (A) default, per-PR D3 (b) opt-in | Yes (was V2) | Attended top-level loop by default (`SKILL.md:43`, `SPEC:343`); A's one-Task-per-PR shape beats B's per-worker PRs. |
| C-010 | V1 (A) | No | Wording only; E's spec cost is also wording, plus P1. |
| C-011 | V5 (E) | No | Only E names the owner and the F3 guard; P1 increases the worktrees it must clean up. |
| X-001 | V5 (E) | No | A quoted, scoped grant suffices for a reversible local commit; never for outward actions. |
| X-002 | V3 (C) | No | Per-action Orca records beat a transcript; GitHub and pr-submit's run-log remain the outward record. |
| X-003 | V1 = V4 = V5 | Yes (was V5 alone) | Coordinator main chat matches D3 (a) and pr-submit's top-level rule; the opt-in is the only exception. |
| X-004 | V1 (A) | No | The rule is conditional on a named owner (`[G:cl] 62-65`); the plan should name the PR owner. |
| X-005 | V4 (D), as amended | Yes (was V1) | The frontmatter `hooks` mechanism makes D's restriction real; a settings-level deny-list also covers worker sessions; bypass behaviour UNVERIFIED. |
| A-001 | V5 (E) | No | With the person gone, E caps exposure at reversible local commits. |
| A-002 | V5 (E) | Yes (was V2) | Same mechanism B argued (sole writer stages from `git status`), now inside E; P1 shrinks the shared-row residue to report directories. |
| A-003 | V5 (E), with P1 | Yes (was V2) | Map is coordinator bookkeeping (A); P1 makes "no other writer for the whole implement run" true by placement (N1). |
| A-004 | V5 (E) | Yes (was V2) | Both E commit paths keep hook rewrites away from concurrent writers; stop-and-report, never `--no-verify`. |
| A-005 | V5 (E) | No | Per-Task quoting of a scoped, default-off grant (`issue-326-evaluation.md:74`). |

**Tally:** E 14 alone plus 2 shared (C-003, X-003), A 4 alone (S-003, C-009, C-010, X-004) plus 2 shared, C 4, D 1 alone (X-005) plus 1 shared, B 0. Nine points changed (C-002, C-003, C-006, C-009, X-003, X-005, A-002, A-003, A-004), all toward E, toward D's amended guard, or toward ties that keep outward actions with the coordinator.

**Overall:** B's substance (worker-owned local commits in a sole-writer worktree, per-task timing, crash survival, staging from ground truth) survives inside E. B's outward-action claims do not. B's remaining contribution to the merge is P1. That placement rule is needed for N1's revert hazard whoever owns git, and it is what makes E's worker lane and E's shared-worktree row safe together.

### Round 2, advocate C (source: round2-advocate-c.md)

### Round 2 rebuttal: advocate C (variant 3, dedicated long-lived git session)

Persona: devops/architect plus analyzer. Date: 2026-11-02. Third rebuttal, after A and B.
Inputs read in full: `round1-advocate-a.md` .. `round1-advocate-e.md`, `round2-advocate-a.md`, `round2-advocate-b.md`, the five variants, `diff-analysis.md`.
Citation keys as in the variants. "Verified" means re-read this round with `sed -n`, `grep -n` or `orca-ide skills get orchestration [--reference references/<name>.md] | cat -n`. Claims I took from another advocate without re-reading are marked UNVERIFIED (by me).

#### 1. Response to criticisms

Every criticism of variant 3 in the four other Round 1 files and in A's and B's Round 2 files, grouped where several advocates raised the same point.

| # | Criticism (raised by) | Response |
|---|---|---|
| C1 | Running pr-submit as a worker turns operator HALTs into `blocked` (`SPEC:137`). That removes the person from a loop designed as "attended, in-session" (`sc-pr-submit-protocol/SKILL.md:43`) (A R1 critique 2 and weakness 2; A R2 section 2; B R2) | **Conceded as a real cost of D3 (b). Rebutted as an argument for A's opt-in over C.** Both quotes verified (`SPEC:137`; `SKILL.md:43-45`: "The monitor is an **attended, in-session** loop: closing the session loses it"). Two corrections: (1) The same `SPEC:137` cell says "the worker may use `ask` or `escalation`". So a HALT reaches the coordinator, and through it the person if the person is present. The person is one hop away, not removed. (2) A's own D3 (b) per-PR Task is a pr-submit worker too, so the HALT-to-`blocked` conversion applies to it exactly as it does to C. This objection counts against D3 (b) in any form. It does not separate C from the opt-in A and B now accept. |
| C2 | One git session serializes PR loops anyway, so it gives no parallel monitoring (B R1 weakness 5; A R2 section 2) | **Conceded fully.** My own Round 1 strength 4 proves it: a terminal that already owns an active Dispatch rejects a second one (`[G:rc] 108`, verified). So one git session runs one pr-submit loop at a time. A second, mechanical reason is new evidence N1 below: each pr-submit loop needs a checkout at its own PR head, so N parallel loops need N checkouts. One session in one terminal is the wrong shape. One pr-submit Task per PR, each in its own worktree, is the right one. |
| C3 | The spec recommends D3 (a) "unless parallel PR monitoring is a real need" (`SPEC:343`); C needs D3 (b) as its default (A, B, D, E) | **Conceded.** Verified. With C2 conceded, C's only remaining default-path benefit is coordinator responsiveness during a single PR loop. The spec's (a) already handles that by ordering: pr-submit runs "after the workers finish" (`SPEC:341`, verified). N1 shows that ordering is also needed for correctness, not only convenience. |
| C4 | Retention needs an explicit user request (`[G:rc] 157`). `worker-retain` exists "for debugging". Reuse needs immediate follow-up work (`[G:cl] 48-50`). A standing loop Task breaks the idle rule (`[G:wc] 77-80`). So "long-lived" exists only through user-gated retention (A, B, D, E) | **Conceded; this was my Round 1 concession 3.** All four lines verified in Round 1, and `worker-retain --help` line 5 ("Keep one supervised worker terminal live for debugging") again this round. I withdraw the long-lived session. One part of the mechanics still applies to the opt-in (N3): reuse needs no retention when the follow-up is immediate. |
| C5 | Each fresh git worker pays a readiness start of up to 60 s (`CAPS:44`) for actions that take seconds (A, B, D, E) | **Conceded for local commits and short outward actions** (a comment, a push). Not material for a pr-submit Task, whose per-wait budget alone is 600 s (`commands/pr-submit.md:49`, verified Round 1). That supports confining delegation to pr-submit, as the opt-in does. |
| C6 | Reuse injection into a running Claude session, and final release of a reused terminal, are UNVERIFIED (`CAPS:47` argv only for fresh launches; `[G:rc] 160-161` "Reused ... terminals are retained") (A, D, E) | **Conceded; still UNVERIFIED.** No new evidence this round. Under the opt-in this matters only for N3's optional reuse; a fresh Task with `--resume` needs no reuse. |
| C7 | Authorization takes one hop through a brief. Briefs are immutable (`SPEC:70`), so a revoked grant persists until a new Task replaces it (A weakness 6; D; E weakness 6, "a record of the hop, not a removal of it") | **Conceded on the hop. Rebutted on revocation for C's shape.** `SPEC:70` verified: "A Task's brief cannot change after creation". Under C every action is its own short Task, so a brief lives for one action. Revocation therefore takes effect at the next action, the same timing A claims for itself. Immutability hurts long-running worker Tasks (B's and E's commit lanes) more than per-action Tasks. E's quip is correct: C records the hop and does not remove it. |
| C8 | C does not solve per-task commits (all) | **Conceded (Round 1 concession 2).** E's row with A's four conditions is the answer. |
| C9 | C has no textual advantage under `[G:cl] 62-65`, because the rule is conditional on the user's plan naming an owner (A R1 X-004; A R2 R5) | **Conceded.** Re-read in Round 1: "If the user's plan names a next owner, post-review fixes and PR preparation remain with that owner; the coordinator routes and synthesizes." A is right that this requires *naming* an owner and that C needs the same naming. I move X-004 to A. |
| C10 | Applying `[G] 53-54` (lifecycle authority) to audit is an inference. For outward actions the authoritative record is GitHub (SHA on origin, PR URL) plus pr-submit's write-ahead run-log, which `SPEC:137` already makes the contract artifact (A R2 R7) | **Conceded.** `SPEC:137` verified: the contract "points at `monitor-run-<PR>.jsonl`". I keep only the narrower claim A and B also keep: a per-action Task is the better *Orca* record (C-005, X-002). |
| C11 | A coordinator crash does not lose the record: the Run is durable (`[G] 51-52`) and pr-submit resumes from its run-log (A R2 R8, N1) | **Conceded on the record.** `SKILL.md:44` verified ("Durability comes from the write-ahead JSONL run-log + `--resume`"). C keeps only better crash *detection* (Orca liveness, `CAPS:122-126`), which A concedes. |
| C12 | The git session is a whole Claude session with full Bash and its own permission mode, with no per-actor mechanical restriction (D R1 critique, weakness 3) | **Rebutted in part.** A's N2 reports that settings-level `PreToolUse` hooks run in any Claude session's main conversation (CC-HOOKS; UNVERIFIED by me, I did not fetch it). This repo already registers main-session `PreToolUse` hooks (`.claude/settings.json:3-21`, per A), and a user-level `PreToolUse` freshness hook blocked my own first Edit in Round 1. So a git deny-list can run in a C worker's session as easily as in the coordinator's. D's subagent allowlist is stricter, and the bypass-mode question is UNVERIFIED for every form. |
| C13 | One git actor serving N worktrees is the coordinator-fed form of the quiescence problem (B R1 critique) | **Conceded.** The git session cannot see writers; the coordinator must assert quiescence in each brief (my Round 1 concession 7). P1 (B) and N1 below reduce how often it matters. |
| C14 | C conflicts with the spec twice as written (`SPEC:156`; D3 (b)) (A R2, citing my concession 1) | **Conceded, now moot for local git.** B's and A's evidence (EVAL F0, `issue-326-evaluation.md:50`) shows `SPEC:156`'s "workers make no commits or pushes" cites a run-local rule. Under the merge base, the only worker that pushes is a per-PR pr-submit Task under D3 (b). That needs exactly one carve-out in the `/sc:git` row, the same one A's opt-in needs. |

#### 2. Updated assessment

**Does a dedicated long-lived git session still add anything over the per-PR Task opt-in? No.** I withdraw it. My reasons:
- **Parallelism.** The per-PR opt-in gives it; one session cannot (C2, `[G:rc] 108`).
- **Retention.** The opt-in needs none (C4).
- **Pay-off.** The readiness start pays off only for long actions, and pr-submit is the only long one (C5).
- **What survives.** C's per-action audit record (C-005, X-002) and its relay reading (S-004) carry over into a per-action Task unchanged. Nothing C uniquely contributed needs the session to stay alive between actions.
- **Local commits.** A dedicated git session does nothing for local commits that the coordinator, D's optional subagent or E's sole-writer worker cannot do more cheaply.

**Do I accept the merge base? Yes.** It is E's table plus A's four conditions:
1. a default-off, scoped, quoted grant;
2. sole writer as a recorded placement fact;
3. the worker lane dormant until K3;
4. the worker invariant (no user-index writes, commits, HEAD moves or remote actions outside the E row), with distinct slugs.

To that I add the per-PR D3 (b) opt-in, D's guard as an optional tested control, and B's placement rule P1. Each of these matches a concession I have already made.

I ask for three additions. Each comes from new evidence in section 3, and each fills a gap in the opt-in as A and B stated it.

- **M1. Place each pr-submit run on its own PR-head checkout. This applies to the coordinator too.** pr-submit at L1+ requires the checkout to equal the PR head, or it HALTs `pr_head_mismatch` (`SKILL.md:268`, `316`). At L3 it commits one fix commit per cycle in that checkout (`SKILL.md:274`). So every pr-submit run moves HEAD in its checkout. It also treats every file in `git status` at the cycle's first edit as the operator's own pending work (`SKILL.md:272`). It refuses to commit those files, HALTing `fix_commit_failed` (`SKILL.md:318`).
  - Rule: a per-PR Task runs in the worktree whose branch is that PR's head, and no other worker writes there for the whole loop.
  - Under D3 (a), the coordinator's own pr-submit run in a shared worktree waits until no worker writes there, which is what "after the workers finish" (`SPEC:341`) already implies.
  - This is a third P1 trigger, alongside B's (a) granted commits and (b) an implement ladder that shares a worktree.
- **M2. Make the HALT path explicit in the opt-in.** A HALT in a per-PR Task gives `worker_status: blocked` (`SPEC:137`). The worker may `ask` the coordinator first. If it ends blocked, the retry is a new Task with `--resume <run-log.jsonl>` (`SPEC:137` Resume cell; WC-6, `SPEC:70`). A and B both noted that this conversion is the cost of D3 (b). The opt-in should say how a HALT is resumed, so the person is reached through the coordinator and the loop is not lost.
- **M3. Allow same-terminal reuse for the resume, as an optimization only.** If the coordinator holds the answer when it reads the blocked `worker_done`, the resume Task is "immediate follow-up work" for the same agent. It may reuse that terminal (`[G:cl] 48-55`), with no retention request. How the resume text reaches a running Claude session is UNVERIFIED (C6), so a fresh Task is the default.

**On A, B, D and E:**
- **A.** Its Round 2 case against C is correct on serialization, on D3 (a) as default and on retention. I have conceded all three. Its HALT objection (C1) applies equally to its own per-PR opt-in; M2 is the answer for both.
- **B.** P1 is well grounded. I re-read `refs/retry.md:199-221` this round: the domain is a whole-worktree diff from `$start` to `now`, and step 5 restores domain paths from `$start`. I did not separately confirm the `rm -f` branch at line 220 (UNVERIFIED by me). M1 is P1's third trigger.
- **D.** I accept the guard as optional and tested. Under the opt-in, the same settings-level deny-list should also run in each per-PR Task's session (C12).
- **E.** It is the base. My Round 1 recommended merge ("E's table with the outward row delegable to a git worker on request") becomes "E's table, with the D3 (b) per-PR Task opt-in in place of a git session".

#### 3. New evidence

None of the following appears in any Round 1 file or in A's or B's Round 2 file as stated here. All was verified this round unless marked.

- **N1. Every pr-submit run is a HEAD-moving writer bound to the PR head checkout.**
  - **Head binding (L1+).** Wave 0 reads `git branch --show-current` and `git rev-parse HEAD` and requires them to match the PR's `headRefName`/`headRefOid`. Otherwise it HALTs `terminal_halted`, reason `pr_head_mismatch` (`src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:268`; failure table `SKILL.md:316`).
  - **Fix commit (L3).** It commits "exactly one commit" per cycle with `git add -- <paths>` and `git commit --only -- <paths>`, and sets `target_sha := git rev-parse HEAD` (`SKILL.md:274`). That moves HEAD in the checkout.
  - **Operator pending files.** Before a cycle's first edit it records every modified, staged and untracked file (`git status --porcelain=v1 -z --untracked-files=all`) as `OPERATOR_PENDING`, and the fix commit refuses them (`SKILL.md:272`). A fix touching such a file HALTs `fix_commit_failed` (`SKILL.md:318`).
  - **Consequences:**
    - (a) Parallel PR monitoring needs one checkout per PR, because one worktree has one HEAD. This is why a single git session cannot do it (C2), and why each per-PR Task needs its own worktree.
    - (b) A pr-submit run in a worktree where an `/sc:implement` worker runs moves HEAD under it, which triggers that worker's `head-moved` halt (`refs/retry.md:41,44`, verified Round 1). That holds whether the coordinator or a Task runs pr-submit.
    - (c) Other workers' in-flight files in the same checkout become `OPERATOR_PENDING` and can cause spurious `fix_commit_failed` HALTs.
  - So D3 (a)'s "after the workers finish" (`SPEC:341`) is a correctness condition, not only scheduling. M1 states it.
- **N2. The HALT-to-`blocked` cost is shared by every D3 (b) form, and `SPEC:137` already gives the bridge.** The cell reads "operator HALTs resolve as blocked (the worker may use `ask` or `escalation`)", with Resume `--resume <run-log.jsonl>` (`SPEC:137`). The opt-in A and B accept (one pr-submit Task per PR) is a pr-submit worker, so it inherits this unchanged. The person is reached via `ask` to the coordinator. If the Task ends blocked, the loop's state survives in the run-log (`SKILL.md:44`) for a resume Task (M2).
- **N3. Reuse without retention fits the resume case.** Reuse is allowed when "the same exact agent has immediate follow-up work" (`[G:cl] 48-50`, verified Round 1), and needs no user request, unlike retention (`[G:rc] 157`). A blocked pr-submit Task whose answer the coordinator already holds is such a case. This is the one piece of C's persistence mechanics that survives into the merge (M3), with the injection path still UNVERIFIED (C6).
- **N4. pr-submit forbids headless or detached runs, and whether a chat-mode Orca worker counts is UNVERIFIED.** "Run headless / detached, or imply a background daemon" is in the skill's do-not list (`SKILL.md:303`). A terminal Orca worker is an interactive Claude TUI (`CAPS:47`, readiness waits for the agent's input box), which is not headless. But `worker-start --help` line 44 says "Not every worker has a terminal", and how a worker runs follows the user's own setting for new agent tabs (line 42). Whether a chat-tab worker satisfies "attended, in-session" (`SKILL.md:43`) is UNVERIFIED. This applies to every D3 (b) form, including the per-PR opt-in, and should be checked before the opt-in is specified.

#### 4. Updated shared-assumption responses

A-002 is unchanged (REJECT: compare porcelain status with the contract and report extras, never sweep). A-004 is unchanged in verdict.

| ID | Response | What changed |
|---|---|---|
| A-001 (coordinator attended) | **QUALIFY** | I no longer claim C's per-Task brief is the best answer when the person leaves. E's handling is better: a default-off grant (`issue-326-evaluation.md:74`, verified) caps unattended exposure at reversible local commits, and every outward action needs an instruction that names it. A per-PR Task is outward, so it needs that named instruction. |
| A-003 (quiescence knowable) | **QUALIFY** | Added: pr-submit needs quiescence for the **whole loop**, not only at commit time, because it moves HEAD each cycle and snapshots `OPERATOR_PENDING` per cycle (N1). This holds for the coordinator under D3 (a) and for a per-PR Task under D3 (b). Like B's implement-ladder point, it is best made true by placement (M1) rather than by a commit-time check. |
| A-005 (standing instruction covers later commits) | **QUALIFY** | Now anchored in `issue-326-evaluation.md:74` (verified Round 1): an authorized option, never a default. A standing grant covers local commits only, for the named run and branch. A per-PR Task needs an instruction naming that PR (D4 (a), `SPEC:346`). I drop my Round 1 claim that per-action quoting was C's distinct advantage, because E's per-Task quoting is the same mechanism. |

#### 5. Updated per-point table

| Point | Superior variant | Changed from Round 1? | Reason |
|---|---|---|---|
| S-001 | V5 (E) | No | The per-action owner/condition table is the merge base's form. |
| S-002 | V3 (C) | No | Only C verified Orca reuse, serialization, retention and idle-rule mechanics; they now explain why the session form fails and the per-PR form works. |
| S-003 | V1 (A) | No | GITDEMO is the procedure everyone cites. |
| S-004 | V3 (C) | No | Only C explains why the #326 relay cannot be something commands call; the per-action Task is that relay's honest shape. |
| C-001 | V5 (E), rule originated in V1, with P1 | No (qualified) | Coordinator commits in a shared worktree at quiescence; P1 keeps ladders and pr-submit loops out of it. |
| C-002 | V5 (E) | No | Only E times commits in the ladder-safe window with a sole-writer guard; dormant until K3. |
| C-003 | V1 = V5 | Yes (was V3) | Coordinator main chat by default; one pr-submit Task per PR only on explicit request (C2, C3). |
| C-004 | V5 (E) | Yes (was V1) | Direct for outward; scoped, quoted, default-off grant for reversible local commits (`issue-326-evaluation.md:74`). |
| C-005 | V3 (C) | No | One Task, brief, `worker_done` and contract per action is the best Orca record; carried by the per-PR opt-in. |
| C-006 | V3 (C), realized as the per-PR opt-in | No (qualified) | Taking the pr-submit loop off the coordinator is the largest context saving; the opt-in delivers it without a session. |
| C-007 | V5 (E) | No | Lock confined to one worktree, earlier commits survive; pr-submit resumes from its run-log under any owner (`SKILL.md:44`). |
| C-008 | V5 (E), with P1 and M1 | No (qualified) | Shared default for report-only workers; own worktree for granted committers, implement ladders and pr-submit loops. |
| C-009 | V1 (A) default, per-PR D3 (b) opt-in | Yes (was V3) | One session serializes loops (`[G:rc] 108`) and N loops need N checkouts (N1); per-PR Tasks give parallelism. |
| C-010 | V1 (A) | No | Wording only. |
| C-011 | V5 (E) | No | Only E names the owner and the F3 guard; P1 and M1 add worktrees it must clean up. |
| X-001 | V5 (E) | No | A quoted, scoped grant suffices for a reversible local commit; never for outward actions. |
| X-002 | V3 (C) | No | Per-action Orca records beat a transcript; GitHub and the pr-submit run-log remain the outward record (C10). |
| X-003 | V1 = V4 = V5, with per-PR opt-in | Yes (was V3) | Coordinator main chat matches D3 (a) and pr-submit's top-level rule; D3 (b) only as one Task per PR on request. |
| X-004 | V1 (A) | Yes (was V3) | The rule is conditional on a named owner (`[G:cl] 62-65`); C needs the same naming, so it has no textual edge (C9). |
| X-005 | V4 (D), as amended | Yes (was V4 caveat only) | Per A and B, the frontmatter `hooks` field gives the restriction (CC-SUB, UNVERIFIED by me); bypass-mode behaviour UNVERIFIED for every form. |
| A-001 | V5 (E) | Yes (was V3) | With the person gone, E caps exposure at reversible local commits. |
| A-002 | V5 (E) | No | A sole-writer worker's `git status` is ground truth; shared rows use the porcelain cross-check. |
| A-003 | V5 (E), with P1 and M1 | No (qualified) | Placement makes run-long quiescence true for ladders (B) and pr-submit loops (N1). |
| A-004 | V5 (E) | No | Both E commit paths keep hook rewrites away from concurrent writers; stop and report, never `--no-verify`. |
| A-005 | V5 (E) | Yes (was V3) | E's per-Task quoting of a scoped, default-off grant is the same mechanism I credited to C. |

**Tally:** E 13 alone plus 2 shared (C-003, X-003), C 5 (S-002, S-004, C-005, C-006, X-002; C-009 is counted for A even though the opt-in uses C's per-action shape), A 4 alone (S-003, C-009, C-010, X-004) plus 2 shared, D 1 alone (X-005) plus 1 shared, B 0. Eight points changed (C-003, C-004, C-009, X-003, X-004, X-005, A-001, A-005), all toward E, A's default or D's amended guard.

**Overall:** C as a long-lived session is withdrawn. Its per-action Task shape, its Orca mechanics and its relay reading survive as the D3 (b) per-PR opt-in, which I accept on top of the E merge base with M1 (pr-submit's own placement), M2 (explicit HALT resume) and M3 (reuse without retention for the resume).

### Round 2, advocate D (source: round2-advocate-d.md)

### Round 2 rebuttal: advocate D (variant 4, coordinator runs git through an Agent-tool subagent)

Persona: security (least privilege, attack surface, authorization) plus analyzer (evidence quality). Date: 2026-11-02. Fourth rebuttal, after A, B and C.
Inputs read in full: `round1-advocate-a.md` .. `round1-advocate-e.md`, `round2-advocate-a.md`, `round2-advocate-b.md`, `round2-advocate-c.md`, the five variants, `diff-analysis.md`.

Citation keys as in Round 1. Added keys:
- `CC-PERM` = https://code.claude.com/docs/en/permissions, fetched this round. Line numbers refer to the saved fetch.
- `CC-MODES` = https://code.claude.com/docs/en/permission-modes, fetched this round, first 100k characters.
- `CC-HOOKS` = https://code.claude.com/docs/en/hooks, characters 100k-200k read this round.

"Verified" means re-read this round.

#### 1. Response to criticisms

These are the criticisms of variant 4 in the four other Round 1 files and in A's, B's and C's Round 2 files. Where several advocates raised the same point, it is grouped into one row.

| # | Criticism (raised by) | Response |
|---|---|---|
| D1 | D cannot run `/sc:pr-submit`. That skill must run top-level and never hand a side effect to a subagent, so D covers local commits only and falls back to A for every outward action (A R1, B R1 weakness 6, C R1 critique 1 and weakness 7, E R1 weakness 8) | **Conceded. This was Round 1 concession 1.** Verified at `sc-pr-submit-protocol/SKILL.md:47-49,82-84`. D is a way of carrying out a commit, not an ownership model. In the merge base it executes a local commit in two places: the coordinator's shared-worktree commit row, and, optionally, a granted worker's own commit (D9). |
| D2 | The "narrow tool list" claim was unsupported: no evidence that Bash can be limited to git (X-005) (A R1, B R1, C R1, E R1) | **Conceded on V4's original mechanism, corrected in my Round 1.** A, B and C now credit the corrected mechanism (frontmatter `hooks`, CC-SUB) and moved X-005 to "V4 as amended". Section 3 adds evidence that the corrected guard works even under `bypassPermissions`. |
| D3 | D breaks provenance when provenance was requested: "Never substitute a non-Orca subagent tool when Orca orchestration provenance was requested" (`[G]` 46-47) (A R1, C R1 critique 2 and weakness 8) | **Conceded for that case, bounded otherwise.** Verified with `orca-ide skills get orchestration` in Round 1. When a user requests Orca provenance for git actions, the committer subagent must not be used. The action then goes to a per-action Task (C's shape) or stays in the coordinator's main chat. A coordinator's main-chat commit has no Orca record either, so this rule restricts D exactly as much as it restricts A's default. The spec should state the rule once, for both. |
| D4 | D adds an authorization hop (the coordinator's prompt) without adding an Orca record (B R1 weakness 6, E R1 weakness 8) | **Conceded on the hop, bounded on the harm.** The hop is inside one session's transcript, so the person sees the subagent prompt next to the reasoning that produced it. That is the same audit surface A has. The guard (section 2) limits the worst a mis-written prompt can cause to a wrong local commit of explicit paths. It cannot cause a push, a sweep, a force or a `.claude/` staging. Under E's default-off grant, nothing visible outside the machine depends on the hop. |
| D5 | D inherits A's limits: no per-task commits, quiescence must be known, contract file lists may be incomplete (B R1 weakness 6, E R1 weakness 7) | **Conceded on per-task commits; partly rebutted on the other two.** Per-task commits belong to E's worker row (D concession 7). On the file lists (A-002), the committer is the cheapest place for the `git status --porcelain` cross-check that A, B and C all now require. It reads the diff outside the coordinator's context and returns only the unlisted paths. On quiescence (A-003), no committer, D or otherwise, can see writers. P1 and M1 make quiescence a placement fact, which D adopts unchanged. |
| D6 | **A's N2:** a settings-level `PreToolUse` hook runs in the coordinator's main chat too, so a mechanical git guard is not unique to a subagent (A R2 R9 and N2; B R2 B11; C R2 C12) | **Conceded on uniqueness. Rebutted on equivalence.** My Round 1 Strength 1 said no variant could restrict a main chat "without blocking that session's other legitimate Bash use". A is right that a deny-list hook can run there, and I withdraw "only". The two forms are not equal, for two verified reasons. (1) **The main chat must keep push authority.** `/sc:pr-submit` performs "the actual `git push origin <target_sha>:<target_branch>`" itself from the main session (`SKILL.md:274`, verified) and stages with `git add -- <paths>` and commits there too. A hook sees only command text, not "this call is inside pr-submit". So a main-chat guard cannot block push, commit or add without breaking the mandatory PR path (`CLAUDE.md:50`). A's proposed "`push` outside pr-submit" rule cannot be expressed as a hook. The main-chat guard is limited to forms the repo forbids absolutely. A subagent allowlist removes push, `gh` and everything else from the committer entirely. (2) **Deny-lists on command text are not a security boundary; allowlists fail closed.** CC-PERM line 250 says a Bash rule "isn't a security boundary around the program": `Bash(git push *)` stops `git push origin main` but not `git -C . push origin main`, `git -c push.default=current push origin main` or `git 'push' origin main` (CC-PERM 252-256, verified). A deny-list hook has the same weakness unless it parses the command fully. An allowlist that accepts only one fixed grammar and rejects everything else blocks any form it does not recognise. So both forms belong in the spec, at different strengths (section 2). |
| D7 | Whether exit 2 blocks under `bypassPermissions` is UNVERIFIED, so the guard cannot be a spec dependency (A R2, B R2, C R2; my own Round 1 concession 3) | **Settled for settings-level hooks by documentation plus a live observation; frontmatter hooks remain inferred.** See section 3, N1. CC-PERM line 625: "PreToolUse hooks run before the permission prompt". Line 651: "A hook that exits with code 2 stops the tool call before permission rules are evaluated". CC-MODES says bypass "disables permission prompts and safety checks", which are steps that come after the hook. In this session, which runs with `--dangerously-skip-permissions`, a user-level `PreToolUse` hook exiting 2 blocked my Edit while I was a subagent. I still accept "optional, tested control" (section 2), because the frontmatter form has not been run. |
| D8 | Subagent hooks are ignored for plugin agents, and project-level agent hooks wait for workspace trust (A R2, citing my Round 1 concession 4) | **Conceded, with a spec rule.** The committer must not ship in `plugins/superclaude/agents/` (21 files there today, verified in Round 1). It installs only to `~/.claude/agents/` through `superclaude install`. The live test in section 2 must run against the installed copy. |
| D9 | A subagent allowlist does not apply to a worker's own commits; the relevant form for B's or E's lane is a settings-level deny-list in the worker session (B R2 B11 and section 2) | **Rebutted.** An Orca worker is a top-level Claude session and may spawn Agent-tool subagents. Orca's depth fence does not count them (`CAPS:155`, verified Round 1). WC-7 restricts only lifecycle messages and commands like pr-submit to the top-level session, not ordinary tool work (`SPEC:71`, verified Round 1). A granted E-row worker can therefore make its local commit through the same committer subagent and get the allowlist. The settings-level floor applies to it as well. |
| D10 | Taking the pr-submit loop off the coordinator is a larger context saving than D's commit offload; C-006 belongs to C's per-PR opt-in (C R2 table) | **Conceded for the opt-in case.** When the user requests D3 (b), the per-PR Task removes the largest load. In the default D3 (a) path, pr-submit stays on the coordinator in every variant, and D's commit offload is the only saving left. I record C-006 as split. |
| D11 | The authorization report returns "in the same confident register" whether right or wrong (my own Round 1 concession 2, echoed by A R1 weakness 6) | **Conceded; mitigated by the contract shape.** The committer returns machine-checkable facts: the commit SHA, `git show --stat --name-only <sha>`, and the unlisted paths. The coordinator compares the committed path list with the contract list before reporting to the person. The check is cheap and does not depend on trusting the subagent's prose. |

#### 2. Updated assessment

**Decision: I accept the merge base as stated, in full.** It is E's table plus A's four conditions:
1. the worker-commit lane is off by default, with a scoped, quoted grant;
2. "sole writer" is a placement fact the coordinator records;
3. the lane stays dormant until #326 K3;
4. workers otherwise never write the user index, commit, move HEAD or touch remotes.

On top of that I accept the per-PR D3 (b) opt-in, B's P1 and C's M1, M2 and M3. Reasons for each addition:
- **P1:** verified this round. The revert domain is the whole-worktree diff `$start`..`now` (`refs/retry.md:201`). The exclusions cover only the run's own files and `.dev/` paths (`retry.md:202-208`). Step 5 restores or `rm -f`s every domain path (`retry.md:220`). From a security view this is an integrity hazard: one actor silently rewrites another actor's files. It exists whoever owns git, so placement is the right control.
- **M1:** verified this round. pr-submit binds to the PR head (`SKILL.md:268`) and makes a fix commit with `git add -- <paths>` and a push from that checkout (`SKILL.md:274`). Every pr-submit run is therefore a HEAD-moving writer and needs a sole-writer checkout. The committer subagent must never run in a worktree while a pr-submit loop runs there.
- **M2 and M3:** accepted as C states them. M3's reuse path stays UNVERIFIED, as C says.

**What D becomes in the merge: the guard, as a two-layer control, optional for this spec's phases.** The spec should state it like this.

**Layer 1: floor deny-list (settings-level `PreToolUse` hook, matcher `Bash`).**
- **Where it runs.** It is installed by `superclaude install` into user-level `~/.claude/settings.json` hooks, so it runs in every session on the machine. That covers the coordinator's main chat, every Orca worker's top-level session and every subagent ("Hooks from settings files ... also run inside subagents", CC-HOOKS, verified Round 1).
- **What it blocks.** Only forms the repo forbids absolutely, so that it can never break `/sc:pr-submit`:
  - `git add` with `-A`, `--all`, `.` or `-f`/`--force` (`CLAUDE.md:22-23`, V1 "no cross-worker sweep");
  - any path under `.claude/` other than `.claude/settings.json` in `git add` (`CLAUDE.md:22`);
  - `--no-verify` on `git commit` or `git push`, or `-n` on `git commit` (on `git push`, `-n` means dry run and is allowed) (`HWW:280`, "Never turn off a quality check");
  - `push` with `--force`, `-f`, `--force-with-lease` or a `+` refspec (pr-submit itself says "never a force push", `SKILL.md:274`);
  - `push` to the remote named `upstream` (`CLAUDE.md:47`);
  - `gh pr create` without `--repo` (`CLAUDE.md:45`).
- **Parsing.** It parses `git` global options (`-C`, `-c`) and quoted subcommands before matching, because a plain text match misses those forms (CC-PERM 256). Any command it cannot parse that contains `git` or `gh` is blocked (exit 2 with a reason).
- **What it does not do.** It does not remove push or commit authority from the main chat. pr-submit needs both.

**Layer 2: committer allowlist (the D lane).**
- **Definition.** `src/superclaude/agents/git-committer.md`, installed to `~/.claude/agents/` only, never to `plugins/superclaude/agents/` (D8).
- **Frontmatter.** `tools: Bash, Read`. `disallowedTools: Agent`, so it spawns nothing. No `isolation` (`worktree` would commit in a temporary tree, CC-SUB). No `omitClaudeMd`, because it must see the repo's staging rules. No `permissionMode` (it cannot loosen its parent anyway, CC-SUB).
- **Hook.** `hooks: PreToolUse` with `matcher: "Bash"` and an allowlist script. The script accepts a call only if it is one simple command with no `;`, `&&`, `||`, `|`, `&`, newline, `$(`, backtick or redirect. The command must be `git` with an optional `-C <path>`, where `<path>` equals the worktree named in the prompt. The subcommand must be one of:
  - `status --porcelain[=v1] [-z] [--untracked-files=all]`;
  - `diff [--cached] [--stat|--name-only] [-- <paths>]`;
  - `add -- <explicit paths>`, with no directory equal to the worktree root and no `.claude/` path except `.claude/settings.json`;
  - `commit -m <msg>` or `commit -F <file in /tmp>`, with no `-a`, `--amend`, `--no-verify` or `-n`;
  - `show --stat --name-only <sha>` and `rev-parse HEAD`.

  Everything else exits 2.
- **Who may use it.**
  - The coordinator, for E's shared-worktree commit row at a quiescent point.
  - A granted E-row worker, for its own local commit (D9).
  - Never when the user requested Orca provenance for that git action (D3).
- **What it returns.** The SHA, the committed path list and the unlisted `git status` paths (D11).

**Tests that gate the guard before any rule relies on it.**
1. **Unit tests** (pytest, run with `uv run pytest`) for both scripts. Each feeds hook JSON on stdin (`tool_input.command`) and asserts the exit code over an allow/deny table. The deny rows include the CC-PERM 256 forms, quoted subcommands, `sh -c` wrappers and compound commands.
2. **A live smoke test under the run's own permission mode.** In a scratch repo outside the checkout, start `claude` once with `--dangerously-skip-permissions` and once in default mode, both with the installed user-level committer. Ask it to spawn the committer and run `git add -A`. Pass means the transcript shows the PreToolUse block and `git status` shows nothing staged. Repeat with a main-chat `git push --force` against Layer 1.
3. **A configuration check.** `make verify-sync` style: the committer file exists in `~/.claude/agents/` and is absent from `plugins/superclaude/agents/`.

Until tests 1 and 2 pass, the spec names the guard as a recommended control. No safety argument in the spec may depend on it. Once they pass, I would ask (Round 3) that Layer 1 be on by default, since it blocks nothing any command legitimately needs.

**On A, B, C, E.**
- **A.** Its N2 corrected an overclaim in my Round 1 and I accept it. Its R10 point holds too: ambient authority over injected worker-report text is not specific to A. Layer 1 is the shared answer, and it now applies to A's main chat.
- **B.** P1 is the best new evidence of the round. It also strengthens the security case: the revert hazard is an integrity breach between actors that no git-ownership rule prevents.
- **C.** Withdrawing the long-lived session removes my main objection (a full session holding all git and GitHub authority). The per-PR Task should also run with Layer 1 active. M1 makes its checkout a sole-writer one.
- **E.** E is the base. D adds the executor for E's local-commit rows and the floor under all of E's rows.

#### 3. New evidence

None of the following appears in any Round 1 file or in A's, B's or C's Round 2 file as stated here.

- **N1. A `PreToolUse` exit 2 blocks under `bypassPermissions`. Documented ordering plus a live observation; settled for settings-level hooks.**
  - **Docs on ordering.**
    - CC-PERM line 625: "When Claude Code makes a tool call, PreToolUse hooks run before the permission prompt, for every tool except `EndConversation`. The hook output can deny the tool call".
    - CC-PERM line 651: "A hook that exits with code 2 stops the tool call before permission rules are evaluated, so the block applies even when an allow rule would otherwise let the call proceed."
    - CC-PERM line 636: "A call that a `PreToolUse` hook blocked stays blocked, whichever settings file the hook comes from" (stated for the mod-approval path).
    - CC-HOOKS (100k-200k): "A hook that blocks by exiting 2 routes the same way as `"deny"`".
  - **Docs on what bypass removes.** CC-MODES: "`bypassPermissions` mode disables permission prompts and safety checks". CC-PERM line 81: it "Skips permission prompts". Neither page lists hooks among the things bypass skips. The hook step runs before the prompt step that bypass removes.
  - **What no doc says.** No sentence on these pages says "exit 2 blocks in `bypassPermissions`" in those words. I searched CC-PERM and the CC-MODES and CC-HOOKS portions I read for `bypassPermissions` and `PreToolUse` together and found none. So the docs settle the ordering, not the mode by name.
  - **Live observation (read-only, this session).**
    - This session's process is `claude --dangerously-skip-permissions ...` (`ps -o args -p $PPID`, 2026-11-02). That flag is equivalent to `bypassPermissions` (CC-MODES).
    - I run as a subagent, which inherits a `bypassPermissions` parent's mode (CC-SUB).
    - In Round 1 my first `Edit` was refused with `PreToolUse:Edit hook error: [~/.claude/hooks/freshness-pre-edit.sh]: FRESHNESS BLOCK`.
    - That script blocks by "stderr + exit 2" (`~/.claude/hooks/freshness-pre-edit.sh:3`, exit at line 138, verified).
    - It is registered as a user-level settings hook (`~/.claude/settings.json:185`, verified).
    - So a settings-level `PreToolUse` exit 2 blocked a tool call in a subagent under bypass.
  - **Limits.** The blocked tool was `Edit`, not `Bash`. The hook was settings-level, not subagent frontmatter. I changed no settings to test further, as instructed. Frontmatter hooks enter the same `PreToolUse` event (CC-SUB: hooks "scoped to the subagent"), so the same ordering should apply, but that remains UNVERIFIED until section 2's test 2 runs.
  - **Effect.** This removes the main open question that kept every advocate from relying on the guard. It is also why the spec should require test 2 under the exact mode Orca launches workers in.
- **N2. Claude Code's own docs say command-text deny rules are not a security boundary.** CC-PERM line 250: a Bash rule "covers the invocation Claude usually produces and isn't a security boundary around the program". Line 256: `Bash(git push *)` "Doesn't stop" `git -C . push origin main`, `git -c push.default=current push origin main` or `git 'push' origin main`. CC-PERM line 260 points to sandboxing for enforcement "that doesn't depend on the command text". Consequences:
  - A's proposed main-chat deny-list, and B's and C's worker-session deny-lists, must parse git's global options and quoting, and fail closed on what they cannot parse. Otherwise they are bypassable by the forms the docs list.
  - An allowlist that accepts one fixed grammar does not have this weakness. That is the concrete sense in which D's subagent-scoped allowlist is stricter than a main-chat deny-list, beyond "fewer commands".
- **N3. The main chat cannot shed push authority, because pr-submit pushes from it.** `SKILL.md:274` (verified): "the SKILL performs the actual `git push origin <target_sha>:<target_branch>` (never an upstream parent remote, never the repo's default/protected branch, never a force push)", after staging "only the files those edits changed (`git add -- <paths>`, never `git add -A` or `git add .`)". A hook cannot tell a pr-submit push from any other push. So in the coordinator's main chat, least privilege is reachable only by blocking the forms pr-submit itself forbids (Layer 1). Removing push altogether is possible only in an actor that never runs pr-submit, that is, the committer subagent (Layer 2). This is the precise security residue of D after A's N2.
- **N4. pr-submit's own forbidden forms match Layer 1 exactly.** The same line says never `git add -A` or `git add .`, never force push, and never the upstream parent remote. These are the forms Layer 1 blocks, alongside the repo's `.claude/` ban (`CLAUDE.md:22-23`), the "never `--no-verify`" rule (`HWW:280`) and `gh pr create` without `--repo` (`CLAUDE.md:45`). So Layer 1 turns into mechanism rules the repo and the mandatory PR skill already state in prose. It adds no new policy.

#### 4. Updated shared-assumption responses

Only the responses that changed are listed. A-004 is unchanged (REJECT: hooks can rewrite files; stop and report, never `--no-verify`).

| ID | Response | What changed |
|---|---|---|
| A-001 (coordinator attended) | **QUALIFY** | Round 1 said an unattended coordinator leaves "only a mechanical control", with bypass behaviour UNVERIFIED. N1 now shows settings-level `PreToolUse` blocks hold under bypass, so the floor works when no one is watching. I now rank E's cap (a default-off grant limits unattended exposure to reversible local commits, `issue-326-evaluation.md:74`, verified) as the primary control and the guard as the backstop. |
| A-002 (contract file lists complete) | **REJECT** (unchanged verdict) | Added: B is right that a sole-writer worker's own `git status` is ground truth, so the worker row is the stronger answer. For shared-worktree rows, the committer subagent runs the porcelain cross-check and returns unlisted paths (D5, D11). |
| A-003 (quiescence knowable) | **QUALIFY** | Added from B's N1 and C's N1: quiescence must hold for the whole run of an implement ladder or a pr-submit loop, not only at commit time. A committer cannot check that. P1 and M1 make it a placement fact. |
| A-005 (standing instruction covers later commits) | **QUALIFY** | Now anchored in `issue-326-evaluation.md:74` (verified): per-task commits are "allowed as an authorized option, never a default", and the owner's comment "does not by itself authorize commits in a worker". The committer prompt or worker brief must carry the scoped grant verbatim. |

#### 5. Updated per-point table

| Point | Superior variant | Changed from Round 1? | Reason |
|---|---|---|---|
| S-001 | V5 (E) | No | The per-action owner and condition table is the merge base's form. |
| S-002 | V3 (C) | No | Only C verified the Orca reuse, serialization, retention and idle-rule mechanics. |
| S-003 | V1 (A) | No | GITDEMO is the procedure everyone cites. |
| S-004 | V3 (C) | No | Only C explains why the #326 relay cannot be something commands call. |
| C-001 | V5 (E), rule from V1, with P1 | Yes (was V4) | Ownership is E's shared row at quiescence. D is an optional executor under it. A's N2 removed D's uniqueness claim. |
| C-002 | V5 (E) | No | Only E times commits in the ladder-safe window with a sole-writer guard; dormant until K3. |
| C-003 | V1 = V5 | Yes (was V5) | Shown as a tie: coordinator main chat by default; one pr-submit Task per PR only on explicit request. |
| C-004 | V5 (E) | Yes (was V1) | Direct authorization for outward actions; a scoped, quoted, default-off grant for reversible local commits (`issue-326-evaluation.md:74`). |
| C-005 | V3 (C) | No | A per-action Orca Task record, carried by the per-PR opt-in. |
| C-006 | V4 (D) for commits; V3 (C) per-PR opt-in for pr-submit | Yes (qualified) | In the default D3 (a) path, D's offload is the only saving; when D3 (b) is requested, the per-PR Task removes the larger load (D10). |
| C-007 | V5 (E) | No | Lock confined to one worktree, earlier commits survive; pr-submit resumes from its run-log. |
| C-008 | V5 (E), with P1 and M1 | Yes (qualified) | Shared worktree for report-only workers; own worktree for granted committers, implement ladders and pr-submit loops. |
| C-009 | V1 (A) default, per-PR D3 (b) opt-in | No (qualified) | Attended top-level loop by default; parallel or overlapping PR work as one Task per PR, with M2's HALT resume. |
| C-010 | V1 (A) | No | Wording only. The guard adds tested code, so it stays optional. |
| C-011 | V5 (E) | No | Only E names the owner and the F3 guard; P1 and M1 add worktrees to clean up. |
| X-001 | V5 (E) | No | A quoted, scoped grant suffices for a reversible local commit, never for outward actions. |
| X-002 | V3 (C) | No | Per-action Orca records beat a transcript; GitHub and pr-submit's run-log remain the outward record. |
| X-003 | V1 = V4 = V5, with per-PR opt-in | Yes (was V1) | Coordinator main chat matches D3 (a) and pr-submit's top-level rule; the opt-in is the only exception. |
| X-004 | V1 (A) | No | The rule is conditional on a named owner (`[G:cl] 62-65`); the plan should name the PR owner. |
| X-005 | V4 (D), as amended | No (strengthened) | The frontmatter `hooks` allowlist is the restriction (CC-SUB). Blocking under bypass is now shown for settings hooks (N1). It is stricter than a deny-list (N2, N3). |
| A-001 | V5 (E), guard as backstop | Yes (was V4) | E's default-off grant is the primary unattended control; the guard works under bypass (N1) but stays optional until tested. |
| A-002 | V5 (E) | Yes (was V4) | A sole-writer worker's `git status` is ground truth; the committer's cross-check covers shared rows. |
| A-003 | V5 (E), with P1 and M1 | No (qualified) | Placement makes run-long quiescence true for ladders and pr-submit loops. |
| A-004 | V5 (E) | No | Both E commit paths keep hook rewrites away from concurrent writers; stop and report, never `--no-verify`. |
| A-005 | V5 (E) | No | Per-Task quoting of a scoped, default-off grant. |

**Tally:**
- E: 13 alone (S-001, C-001, C-002, C-004, C-007, C-008, C-011, X-001, A-001, A-002, A-003, A-004, A-005), plus 2 shared (C-003, X-003).
- C: 4 alone (S-002, S-004, C-005, X-002), plus a share of C-006.
- A: 4 alone (S-003, C-009, C-010, X-004), plus 2 shared.
- D: 1 alone (X-005), plus a share of C-006 and of X-003.
- B: 0.

Ten points changed (C-001, C-003, C-004, C-006, C-008, X-003, X-005 strengthened, A-001, A-002, plus the A-003 qualifier). All moved toward E or toward ties that keep outward actions with the coordinator.

**Overall:** D is not an ownership model and I no longer argue for it as one. Its surviving contribution to the merge is the guard, specified in two layers:
- a Layer 1 floor of the repo's absolute prohibitions, enforced in every session;
- a Layer 2 committer allowlist for E's local-commit rows.

The guard works under `bypassPermissions` for settings hooks (N1). It is stated in section 2 with its tests, and it stays optional until those tests pass under the run's own permission mode.

### Round 2, advocate E (source: round2-advocate-e.md)

### Round 2 rebuttal: advocate E (variant 5, hybrid)

Persona: qa (edge cases, failure scenarios) plus analyzer (evidence quality). Date: 2026-11-02. Fifth and last rebuttal, after A, B, C and D.

Inputs read in full: `round1-advocate-a.md` .. `round1-advocate-e.md`, `round2-advocate-a.md` .. `round2-advocate-d.md`, the five variants and `diff-analysis.md`. Citation keys as in the variants. "Verified" means re-read this round with `sed -n`, `awk`, `grep -n` or `orca-ide skills get orchestration [--reference references/<name>.md] | cat -n`. Claims taken from another advocate without re-reading are marked "per <advocate>". Documentation I did not fetch (CC-SUB, CC-HOOKS, CC-PERM, CC-MODES) is cited only as "per D" or "per A".

#### 1. Response to criticisms

Every criticism of variant 5 in the other Round 1 files and in the A-D Round 2 files, grouped where several advocates raised the same point.

| # | Criticism (raised by) | Response |
|---|---|---|
| E1 | E's distinctive lane depends on #326 K3, which does not exist. Until then a worker commits only "through steps its brief adds after the command finishes", one end-of-run commit that A's coordinator can also make with direct authorization (A R1 critique 1 and weakness 5; B R1 weakness 7; C R1 weakness 10; D R1 critique and weakness 4) | **Conceded for `/sc:implement` (my Round 1 concession 1); rebutted for the spec as a whole.** `/sc:implement` acceptance never "authorizes commit, PR, merge or release" (`sc-implement-protocol/refs/managed-workspace.md:67`, verified Round 1), so its in-run commit is K3. Two counter-points: (1) the spec must fix K3's boundary now, because the evaluation says "The spec only fixes its boundary (F1 ...)" (`EVAL:63`, verified Round 1); A conceded this (A R2 R1). (2) **New (section 3, N3):** the spec already has a live worker commit lane today. `/sc:task` classes `commit` and `push` as EXEMPT and executes them immediately (`sc-task-protocol/SKILL.md:61`; `commands/task.md:80,99`, verified), and the spec's task row says "EXEMPT `commit`/`push` refused unless authorized (WC-9)" (`SPEC:144`, verified). So an authorized `/sc:task` worker may commit, and even push, under the spec as written. E's row is not dormant for that command; it is the missing guard on it. |
| E2 | Two owners for local commits means two rule sets to state and test (A, B, C, D; V5 weakness 1) | **Conceded on count, mitigated on content.** Both rows share four predicates: a named instruction, explicit paths plus `.dev/tasks` (`CLAUDE.md:37`), never push, report the SHA. They differ in one predicate: "sole writer for the whole run" (worker row) against "no writer during the commit" (coordinator row). One test table with one varying column covers both. |
| E3 | "Sole writer" is a placement fact only the coordinator knows; nothing checks it, so the coordinator still carries the safety check (A R1 critique 3; D R1 critique, weakness 4) | **Conceded that it is coordinator-asserted; rebutted that it is unchecked.** The coordinator fixes it when it places the worker (`worker-start --worktree new-child\|new-top-level`, `[G:pl] 15-21`, verified Round 1), which A now accepts as bookkeeping rather than inference (A R2 R2). I add a worker-side tripwire (merged rule W5 below): before each commit the worker compares `git status --porcelain` with its own touched set and commits nothing if an unexplained path appears. D calls this "a weak signal of an active writer" (D R1 A-003); weak, but it fails closed, and in a true sole-writer worktree it never fires. |
| E4 | Shared refs: implement pins `refs/superclaude/implement/<slug>/T<id>` are shared across linked worktrees, and E left two runs of one plan UNVERIFIED (A R1 critique 4, weakness 5) | **Conceded, with A's correction accepted.** Workers write and delete these refs whoever owns commits (`SKILL.md:113,116`, verified Round 1; A R2 R14). The slug-distinct rule belongs in the spec under every option. In managed mode the slug is the package id (`SKILL.md:113`), so two worktrees running one plan collide by construction. Rule: the coordinator never runs one managed package in two worktrees at once. Practical impact of a collision (a pruned tree before resume) stays UNVERIFIED. |
| E5 | The authorization hop: briefs are immutable (`SPEC:70`), so a revoked grant persists until a new Task replaces it; this hurts long-running worker Tasks (E's and B's lanes) more than per-action Tasks (A R1 weakness 6; B R2 B5; C R2 C7) | **Partly conceded, partly rebutted with new evidence.** `SPEC:70` verified: "A Task's brief cannot change after creation". But a worker must "Read coordinator follow-ups at each natural checkpoint — before starting a new file, after a test run — and once more immediately before `worker_done`" (`[G] 85-87`, verified). So a revocation sent by the coordinator reaches the worker at its next checkpoint. I add "and immediately before each commit" to the worker row (W4 below), and the rule that a follow-up may **revoke or narrow** a grant but never widen it (widening needs a new Task, consistent with WC-6's refusal to carry a brief by `send`, `SPEC:70`). Remaining concession: revocation is effective at the next checkpoint, not instantly, and C's per-action Tasks are no slower. |
| E6 | E's shared-worktree coordinator row still depends on A-002 (complete file lists) and A-003 (a quiescence map) (B R1 weakness 7) | **Conceded; P1 and M1 shrink it.** With B's P1 and C's M1, implement ladders and pr-submit loops leave the shared worktree, so what is left there is report-only workers. A-002 is closed further by N2 below (`git commit --only -- <paths>`). |
| E7 | E serializes PR monitoring and inherits A's pr-submit blocking of the coordinator (B R1 weakness 7; C R1 weakness 1 and C R2) | **Conceded.** I accept the per-PR D3 (b) opt-in (section 2). |
| E8 | E's C-002 advantage over B is wording, not capability (B R1 weakness 7) | **Conceded on capability, rebutted on safety.** The commit window is the same. E adds the guards B lacked (sole writer, batch exclusion, quoted grant), which B now accepts (B R2, C-002 moved to E). |
| E9 | E's outward audit is the coordinator transcript, not an Orca record (C R1 weakness 3) | **Rebutted, with A's evidence.** The authoritative outward record is GitHub (SHA on origin, PR URL) plus pr-submit's run-log, which `SPEC:137` already makes the contract artifact (verified Round 1; A R2 R7). C conceded this (C R2 C10). Under the per-PR opt-in, the Task record adds the Orca outcome C wanted. |
| E10 | A sole-writer worker running raw git has no mechanical guard (D R1 critique, weakness 4; V5 weakness 2) | **Conceded.** I accept D's guard as optional and tested, with the amendments in section 2 (Layer 1 as specified would break `/sc:implement`, N1). |
| E11 | E's recovery text overclaimed: "the retry Task (WC-6) checks for it [the stale lock] first", a step no command has (B R2 B8; my Round 1 concession 3) | **Conceded.** I adopt B's rule: a Task that finds `index.lock` in its worktree stops `worker_status: blocked` and names the path; only the coordinator or person removes it (`SPEC` WC-4 `blocked` outcome, per B). |
| E12 | "Sole writer" must also exclude Agent-tool fan-out outside a batch, user-taken-over terminals and hooks writing there (A R2 condition 2; B R2; my Round 1 concession 4) | **Conceded and adopted** into the predicate (W2 below). |
| E13 | E's sole-writer condition presumes a placement rule it never states (B R2, P1) | **Conceded; adopted with two amendments** (section 2). |
| E14 | "Workers never run a mutating git command" is inaccurate: implement writes refs and restores working-tree files (A R2 N3). This applies to V5's row 5 ("Anything mutating git in a worktree shared with other running workers: nobody but the coordinator") | **Conceded.** Row 5 is false as written for `/sc:implement` (Q0 `update-ref`, `SKILL.md:113`; revert `git restore --worktree` and `rm -f`, `refs/retry.md:220`, verified). It also misses a user-index write a worker command makes today (N3). Row 5 is restated as merged rule G4 below. |
| E15 | Every pr-submit run moves HEAD in its checkout and snapshots other writers' files as `OPERATOR_PENDING`, so E's row 1 (coordinator runs pr-submit) is safe only on a checkout no one else writes (C R2 N1) | **Conceded; verified.** Head binding to the session's checkout (`sc-pr-submit-protocol/SKILL.md:268`), fix commit with `git commit --only -- <paths>` and a HEAD move (`SKILL.md:274`), `OPERATOR_PENDING` (`SKILL.md:272`), HALT `fix_commit_failed` (`SKILL.md:318`). M1 accepted. |
| E16 | V5 is silent on Orca's review-ownership rule `[G:cl] 62-65` (diff X-004) | **Conceded (my Round 1 concession 10).** I adopt A's reading: the rule is conditional on the user's plan naming an owner, so the brief or run template records the PR owner (A R2 R5). |

#### 2. Updated assessment

##### 2.1 Each proposed addition, checked against E and the evidence

| Addition | Verdict | Evidence and reason |
|---|---|---|
| A1. Worker-commit lane off by default, scoped quoted grant | **Accept** | `EVAL:74` (verified): per-task commits are "allowed as an authorized option, never a default", and the owner's comment "does not by itself authorize commits in a worker". This tightens V5 row 4 condition 1 by naming scope (run, branch, local only). |
| A2. Sole writer is a placement fact the coordinator records; worker started with `--worktree new-child` or `new-top-level` for that Task | **Amend** | The fact-recording part is right. The "started with `new-*` for that Task" wording is wrong: an `/sc:implement` resume, and C's M2/M3 resume Task, must run in the **existing** worktree where the ledger or run-log lives. Orca places work there with an exact selector, `id:<repo-id>::<path>` (`[G:pl] 35-37`, verified). Amended: "placed, new or by exact selector, in a worktree the coordinator created for this run and records as having no other writer" (N4). |
| A3. Dormant until #326 K3 | **Amend** | True for `/sc:implement` (`managed-workspace.md:67`). False for `/sc:task`, whose authorized commit is live under `SPEC:144` today (N3). The spec should say: dormant for in-run implement commits; live for any command whose own authorized commit step the spec already allows. |
| A4. Workers otherwise never write the user index, commit, move HEAD or touch remotes | **Amend; conflicts found** | As a target rule, accept. As stated it conflicts with (i) the per-PR D3 (b) opt-in, whose worker commits a fix, moves HEAD and pushes (`sc-pr-submit-protocol/SKILL.md:274`), so it must be a named second exception; and (ii) today's commands: `/sc:task` may push when authorized (`SPEC:144`), and a task-builder MDTM task in CLI mode runs `git add -A` on the user index (N3). The spec must change those, not describe them as already compliant. |
| Per-PR D3 (b) opt-in, one short-lived pr-submit Task per PR on explicit request | **Accept, with two preconditions** | It keeps outward actions direct by default (`SPEC:341,343`, verified Round 1) and gives parallelism without retention (C R2 C2, `[G:rc] 108`). Preconditions: (1) `SPEC:343` licenses only "parallel PR monitoring"; A's second trigger ("PR work that overlaps running workers") needs new spec wording. (2) pr-submit forbids running "headless / detached" (`SKILL.md:303`, verified); whether a chat-tab Orca worker counts as attended is UNVERIFIED (C R2 N4) and must be tested before the opt-in is enabled. It also needs the `/sc:git` row carve-out (`SPEC:156`) and A4's exception. |
| B P1(a): own worktree when the brief grants commits | **Accept** | It is V5 row 4 condition 2 stated as a placement rule. |
| B P1(b): own worktree when an `/sc:implement` ladder shares a worktree with another worker writing outside `.dev/` | **Accept, with a clarification** | Verified this round: the domain is the whole-worktree diff `$start`..`now` (`refs/retry.md:201`); exclusion 6 protects "every other `.dev/` path that is not named in the `files=` field" of this task (`retry.md:207`); step 5 restores each domain path or runs `rm -f -- "$top/$p"` (`retry.md:220`). So the trigger is correct, and the coordinator can keep sharing possible by putting every WC-4 report directory under `.dev/` (N7). Commands with fixed outside locations (cleanup-audit's `.claude-audit/`, research's `claudedocs/`, both cited in `SPEC` WC-4 row) still trigger it. |
| C M1: each pr-submit run gets its own PR-head checkout with no other writer, coordinator included | **Accept, with a D3 (a) clarification** | Verified (`SKILL.md:268,272,274,318`). pr-submit has no path or worktree flag: its arguments are `--monitor`, `--max-rounds`, `--poll-interval`, `--timeout`, `--silence-timeout`, `--base`, `--head`, `--title`, `--body`, `--pr`, `--output-dir`, `--resume` (`commands/pr-submit.md:8`, verified), and it STOPs if "your checkout is not the PR's head branch and commit" (`pr-submit.md:28`). So under D3 (a) the coordinator must run it from the PR-head checkout itself. When that head is an experiment worktree's branch, the coordinator's main chat must work from that checkout (whether a coordinator can switch its session's directory mid-run without side effects is UNVERIFIED), or the opt-in Task is used (N5). |
| C M2: a HALT ends a pr-submit Task `blocked`; resume is a new Task with `--resume` | **Accept** | `SPEC:137` (verified Round 1): "operator HALTs resolve as blocked (the worker may use `ask` or `escalation`)", Resume `--resume <run-log.jsonl>`. Consistent with WC-6 (new Task, own report directory, `SPEC:70`). |
| C M3: optional same-terminal reuse for that resume | **Accept as optional only** | No conflict with WC-6: reuse is `worker-start --task <next_task_id> --terminal <handle>` (`[G:cl] 53-54`, verified Round 1), a new Task, not the `--retry-of` WC-6 forbids. How the next Task's text reaches a running Claude session is UNVERIFIED (C R2 C6), so a fresh Task stays the default. |
| D Layer 1: settings-level deny-list floor in every session | **Amend; reject "on by default" for now** | As specified it blocks "`git add` with `-A`, `--all`, `.`" and every git/gh command it cannot parse (D R2 section 2). That breaks `/sc:implement`'s Q0 snapshot and its revert snapshot, which run `GIT_INDEX_FILE="$idx" git add -A` inside a compound `&&` command with `$(...)` (`SKILL.md:111`; `refs/retry.md:199,239`, verified). D's statement that Layer 1 "blocks nothing any command legitimately needs" is therefore false (N1). Amended: exempt `git add -A` when `GIT_INDEX_FILE` names a temporary index; require a corpus test that every git and gh command template in the installed skills passes; then decide on default-on. Installing a user-level hook into every session on the machine also reaches beyond Orca runs, so default-on needs a separate decision. |
| D Layer 2: optional committer-subagent allowlist | **Accept as optional** | It can execute C1 and W6 below. D9 (a granted worker may use it) is consistent with WC-7, which forbids wrapping the *command* in a subagent, not a commit step (`SPEC:71`, per D). It must not be used when Orca provenance is requested (`[G] 46-47`, per A, C and D), and must not ship in the plugin mirror (D R2 D8). Its allowlist must permit `commit --only` (N2), which D's grammar (`commit -m <msg>`) does not list. |

##### 2.2 Conflicts between additions, or with the spec

- **K1. A4 against the per-PR opt-in.** The opt-in worker commits, moves HEAD and pushes. A4 must list it as a second named exception, or the two rules contradict each other.
- **K2. A4 against today's spec and commands.** `SPEC:144` lets an authorized `/sc:task` worker push; the merged rule makes every push coordinator-only (except the opt-in). `SPEC:144` must change to "push refused under `--unattended`; commit only under the worker-commit lane". The MDTM CLI-mode `git add -A` (N3) needs a refusal under `--unattended` or a P1 placement.
- **K3. D Layer 1 against `/sc:implement`** (N1), and against D's own fail-closed parsing of compound commands.
- **K4. A2 against M2, M3 and implement resumes** (N4).
- **K5. C M1 against D3 (a) when the PR head is not the coordinator's checkout** (N5).
- **K6. The opt-in's "overlapping PR work" trigger against `SPEC:343`'s wording**, which names only parallel monitoring.
- **K7. D's Layer 2 grammar against N2:** the allowlist must accept `git commit --only -- <paths>`.

No addition conflicts with E's core split (outward actions with the coordinator; local commits by a sole writer or by the coordinator at quiescence).

##### 2.3 Final merged rule set I would defend

**Outward actions**
- **O1.** Push, PR (always `/sc:pr-submit --monitor 3`, `CLAUDE.md:50`), review replies, issue or status comments, project updates, remote branch deletion and merges into a shared branch belong to the coordinator, in its main chat, only when the user's instruction names that action (D4 (a)/(b) split as in V5). The plan or brief records the PR owner (`[G:cl] 62-65`).
- **O2.** The coordinator runs pr-submit (D3 (a)) only from the PR-head checkout, with no other writer there for the whole loop (M1, N5).
- **O3. Opt-in.** When the user explicitly asks for parallel PR monitoring (or, after a spec change, PR work that overlaps running workers), each PR gets one pr-submit Task. The Task runs in that PR's head worktree with no other writer (M1). Its brief quotes the instruction naming the PR (`SPEC:346`). A HALT ends it `blocked`; resume is a new Task with `--resume` (M2), on a fresh terminal by default or the same terminal as an optimization (M3). Enabled only after the attended-mode question (`SKILL.md:303`) is tested.

**Coordinator local work**
- **C1.** Local commit in a shared worktree: only when no worker writes there (placement map plus `worker-list`); compare `git status --porcelain` with the settled contracts and report unlisted paths; stage explicit paths plus `.dev/tasks` (`CLAUDE.md:37`); commit with `git commit --only -- <paths>` (N2); a hook rewrite or failure is stop-and-report, never `--no-verify` (`HWW:280`).
- **C2.** The coordinator creates and removes run worktrees and branches under `.dev/worktrees/` (`CLAUDE.md:299-302`). It never removes a branch with unmerged commits or an open PR without the user's instruction (`EVAL:53`), and never runs one managed package in two worktrees at once (E4).
- **C3.** The coordinator keeps the placement map (which Task writes in which worktree) as a section 2.3 duty.

**Placement (P1, amended)**
- **P1.** Every WC-4 report directory goes under `.dev/` (N7). A worker gets its own worktree when (a) its brief grants local commits; (b) it runs `/sc:implement` with the retry ladder while another worker writes outside `.dev/` in that worktree; (c) it runs a pr-submit loop; (d) its command writes the user index (N3), unless that step is refused under `--unattended`. Report-only workers share the current worktree (`[G:pl] 8-11`).

**Worker local-commit lane (default off)**
- **W1.** Allowed only when the brief quotes the user's instruction naming local commits for this run and branch (`EVAL:74`). It never covers push, merge or PR.
- **W2.** Sole writer: placed by the coordinator (new, or by exact selector for a resume) in a worktree created for this run and recorded with no other writer: no other worker, no coordinator git, no user-taken-over terminal, no Agent-tool fan-out outside a batch.
- **W3.** Timing: for `/sc:implement`, only between a task's `complete` line and the next task's Q0, never inside a parallel batch (`refs/retry.md:41`; `SKILL.md:97,114`); this needs K3. For other commands, at the command's own authorized commit step (`/sc:task`, `SPEC:144` amended) or after the command finishes.
- **W4.** Immediately before each commit the worker reads coordinator follow-ups (`[G] 85-87`). A follow-up may revoke or narrow the grant, never widen it.
- **W5.** Tripwire: if `git status --porcelain` shows a path the worker did not touch, it commits nothing and reports `blocked`.
- **W6.** It stages explicit paths plus `.dev/tasks`, commits with `--only`, lists each SHA in the contract's `artifacts`; a hook rewrite or failure gives `partial` or `blocked`, never `--no-verify`; a found `index.lock` gives `blocked` with the path (B8).

**Invariant and guard**
- **G1.** Outside W1-W6 and O3, a worker never writes the user index, never commits, never moves HEAD and never touches a remote. `/sc:implement`'s private-index snapshots, its refs and its revert stay allowed, with the revert confined by P1(b). Spec changes this requires: `SPEC:156` (`/sc:git` row, per EVAL F0), `SPEC:144` (`/sc:task` push refused under `--unattended`), and a `--unattended` refusal of the MDTM CLI-mode `git add -A` step (or P1(d)).
- **G2.** Run slugs are distinct across concurrent worktrees.
- **G3.** D's guard is a recommended control, not a dependency: Layer 1 with the `GIT_INDEX_FILE` exemption and a corpus test over every installed git/gh command template; Layer 2 as an optional executor for C1 and W6 that accepts `commit --only`. Default-on is decided after the tests pass under the run's permission mode.

#### 3. New evidence

None of the following appears in any Round 1 file or in the A-D Round 2 files as stated here. All was verified this round unless marked.

- **N1. D's Layer 1, as specified, would block `/sc:implement`.** Q0 snapshots with `idx=$(mktemp); GIT_INDEX_FILE="$idx" git read-tree HEAD && GIT_INDEX_FILE="$idx" git add -A && start=$(GIT_INDEX_FILE="$idx" git write-tree); rm -f "$idx"` (`src/superclaude/skills/sc-implement-protocol/SKILL.md:111`). The revert takes `now` "with the Q0 temp-index sequence" (`refs/retry.md:199`), and the retry helper runs `GIT_INDEX_FILE="$idx" git -C "$1" add -A` (`refs/retry.md:239`). Layer 1 blocks `git add -A` and fails closed on unparsed compound git commands (D R2 section 2). Either rule stops Q0, so every implement task would fail at start, and every revert would fail. These `add -A` calls write a private index, not the user index, so they are exactly the kind of call the floor must allow. A grep for `git add -A`, `--all` or `.` over `src/superclaude/{skills,commands,agents}` finds `sc-implement-protocol/SKILL.md:111`, task-builder's MDTM step (N3) and pr-submit's own "never `git add -A`" text; a second search for `git -C ... add` finds `refs/retry.md:239`. Any Layer 1 rule must be tested against all of them.
- **N2. The coordinator's shared-worktree commit must use `git commit --only -- <paths>`.** Explicit-path `git add` is not enough if anything else is already staged in the user index: a plain `git commit` commits the whole index. pr-submit already guards against this: "committing with `git commit --only -- <paths>` so nothing else already in the index is committed" (`sc-pr-submit-protocol/SKILL.md:274`). N3 shows a worker command that can leave other paths staged. No variant's commit rule mentioned `--only`.
- **N3. Two worker commands already write git state the merge base forbids.**
  - `/sc:task` classes `commit` and `push` as EXEMPT (`src/superclaude/skills/sc-task-protocol/SKILL.md:61`; `src/superclaude/commands/task.md:80`), and EXEMPT means "Execute immediately" (`task.md:99`). The spec's task row keeps them, "refused unless authorized (WC-9)" (`SPEC:144`). So under the spec as written an authorized `/sc:task` worker may push. That contradicts O1 and every advocate's Round 2 position.
  - A task-builder-generated MDTM task, when its POST gate is in CLI mode, tells the executor to "Ensure new task artifacts are staged ... (`git add -A` ...)" (`src/superclaude/skills/task-builder/SKILL.md:2237`). CLI mode is "default OFF" (`task-builder/SKILL.md:43`). In a shared worktree that step sweeps every other worker's files into the user index. Whether the MDTM `/task` executor is in the spec's worker set is UNVERIFIED (I found the `/sc:task` row at `SPEC:144`, not a `/task` row).
  - Consequence: A's condition 4 describes a target, not today's behaviour, and the spec needs explicit changes (G1).
- **N4. Resumes run in an existing worktree.** Orca places work in an existing worktree with an exact selector, `id:<newFullWorktreeId>` (`[G:pl] 35-37`). An `/sc:implement` resume needs its ledger and retries directory, which live in that worktree (`refs/retry.md:22`, per its `<run dir>` definition, re-read this round), and a pr-submit resume needs its run-log (`SPEC:137`). A2's "started with `new-*` for that Task" would wrongly bar those Tasks from the commit lane.
- **N5. pr-submit cannot be pointed at another checkout.** Its argument list (`src/superclaude/commands/pr-submit.md:8`) has no path or worktree flag, and it STOPs when "your checkout is not the PR's head branch and commit" (`pr-submit.md:28`; head binding `SKILL.md:268`). M1 therefore constrains where the coordinator itself must stand under D3 (a), not only where an opt-in Task is placed.
- **N6. Workers already have a revocation path.** A worker must "Read coordinator follow-ups at each natural checkpoint — before starting a new file, after a test run — and once more immediately before `worker_done`" (`orca-ide skills get orchestration | cat -n`, lines 85-87). Adding "immediately before each commit" (W4) gives a revoked grant effect before the next commit, which answers most of the immutable-brief objection (`SPEC:70`).
- **N7. Report directories under `.dev/` are outside the revert's reach.** Revert exclusion 6 removes "every other `.dev/` path that is not named in the `files=` field" of the reverting task (`refs/retry.md:207`). A report-only worker whose WC-4 report directory is under `.dev/` therefore never has files reverted, so it can share a worktree with an implement ladder. This narrows P1(b) to workers that write outside `.dev/`, which is how B worded it, and gives the coordinator a cheap way to keep the default shared layout.

#### 4. Updated shared-assumption responses

| ID | Response | What changed |
|---|---|---|
| A-001 (coordinator attended) | **QUALIFY** (unchanged verdict) | All four other advocates now rank E's cap (a default-off grant limits unattended exposure to reversible local commits, `EVAL:74`) as the primary control. Added: D's guard as a backstop. D reports that a settings-level `PreToolUse` exit 2 blocked a call under `--dangerously-skip-permissions` (D R2 N1, per D); my own Round 1 Edit was blocked by the same freshness hook in this session, but I did not check the session's permission mode. |
| A-002 (contract file lists complete) | **REJECT as a basis for staging** (was QUALIFY for sole-writer worktrees, REJECT for shared) | Added N2 and N3: even explicit-path staging is unsafe if the user index already holds other staged paths, so every commit (C1, W6) uses `git commit --only -- <paths>`, and the porcelain cross-check reports extras. In a sole-writer worktree the worker's own `git status` remains ground truth (W5). |
| A-003 (quiescence knowable) | **QUALIFY** | From B and C: quiescence must hold for the whole run of an implement ladder or a pr-submit loop, not only at commit time. P1 (b) and (c) make it a placement fact, and C3 makes the placement map a coordinator duty. N4: a resume Task inherits its worktree's recorded sole-writer status. |
| A-004 (commit does not rewrite files) | **ACCEPT the diff's verdict** (unchanged) | Added the agreed rule: a hook rewrite or failure is stop-and-report, never `--no-verify` (`HWW:280`); pr-submit already leaves "edits (and any hook changes) ... in the working tree" on `fix_commit_failed` (`SKILL.md:318`, verified). |
| A-005 (standing instruction covers later commits) | **QUALIFY** | Now anchored in `EVAL:74` (verified). Added: a standing grant covers local commits for the named run and branch only; a coordinator follow-up may narrow or revoke it at the next checkpoint (W4, N6), never widen it; and it can never authorize a push, which requires amending `SPEC:144` (N3). |

#### 5. Updated per-point table

| Point | Superior variant | Changed from Round 1? | Reason |
|---|---|---|---|
| S-001 | V5 (E) | No | The per-action owner/condition table is the merge base's form. |
| S-002 | V3 (C) | No | Only C verified the Orca reuse, serialization, retention and idle-rule mechanics; they now explain why the per-PR Task works and the session does not. |
| S-003 | V1 (A) | No | GITDEMO is the procedure every variant cites. |
| S-004 | V3 (C) | No | Only C explains why the #326 relay cannot be something commands call. |
| C-001 | V5 (E), rule from V1, with P1 and `--only` | Yes (was V1 = V5) | E is the merge base; C1 adds the porcelain cross-check and `git commit --only` (N2); P1 keeps ladders and pr-submit loops out of the shared worktree. |
| C-002 | V5 (E) | No | Only E times commits in the ladder-safe window with a sole-writer guard; dormant for implement until K3, live for `/sc:task` (N3). |
| C-003 | V1 = V5, with per-PR opt-in | No (qualified) | Coordinator main chat by default; one pr-submit Task per PR only on explicit request (O3). |
| C-004 | V5 (E) | No | Direct for outward actions; scoped, quoted, default-off, revocable grant for reversible local commits (`EVAL:74`, W4). |
| C-005 | V3 (C) | No | A per-action Orca Task record, carried by the per-PR opt-in. |
| C-006 | V3 (C) shape via per-PR opt-in; V4 (D) for commit diffs | Yes (was V3) | Under the default D3 (a), D's optional committer is the only saving; when the opt-in is used, the per-PR Task removes the larger load. |
| C-007 | V5 (E) | No (refined) | Lock confined to one worktree, earlier commits survive; B8's blocked-on-lock rule replaces my overclaimed "retry checks first". |
| C-008 | V5 (E), with P1 and M1 | No (qualified) | Shared default for report-only workers with report dirs under `.dev/` (N7); own worktree for granted committers, ladders that share with outside writers, and pr-submit loops. |
| C-009 | V1 (A) default, per-PR D3 (b) opt-in | Yes (was V3) | One session serializes loops (`[G:rc] 108`) and N loops need N head checkouts (C R2 N1, N5); per-PR Tasks give parallelism. |
| C-010 | V1 (A) | No | Wording only; the merge base adds spec wording plus the `SPEC:144` and MDTM changes (N3). |
| C-011 | V5 (E) | No | Only E names the owner and the F3 guard; adds the one-package-one-worktree rule (E4). |
| X-001 | V5 (E) | No | A quoted, scoped grant suffices for a reversible local commit, revocable at the next checkpoint (N6); never for outward actions. |
| X-002 | V3 (C) | No | Per-action Orca records beat a transcript; GitHub and pr-submit's run-log remain the outward record. |
| X-003 | V1 = V4 = V5, with per-PR opt-in | No (qualified) | Coordinator main chat matches D3 (a) and pr-submit's top-level rule; the opt-in is the only exception, and it needs the K1 exception in G1. |
| X-004 | V1 (A) | No | The rule is conditional on a named owner (`[G:cl] 62-65`); E adopts A's reading (O1). |
| X-005 | V4 (D), as amended | Yes (was V1) | The frontmatter `hooks` allowlist makes the restriction real (per D); Layer 1 needs the `GIT_INDEX_FILE` exemption (N1) and Layer 2 must accept `commit --only` (N2). |
| A-001 | V5 (E), guard as backstop | No (qualified) | E's default-off grant caps unattended exposure at reversible local commits. |
| A-002 | V5 (E) | No (strengthened) | Sole-writer `git status` is ground truth; every commit uses `--only` (N2). |
| A-003 | V5 (E), with P1 and M1 | No (qualified) | Placement makes run-long quiescence true for ladders and pr-submit loops. |
| A-004 | V5 (E) | No | Both commit paths keep hook rewrites away from concurrent writers; stop and report, never `--no-verify`. |
| A-005 | V5 (E) | No | Per-Task quoting of a scoped, default-off, revocable grant; never a push (`SPEC:144` amended). |

**Tally:** E 13 alone (S-001, C-001, C-002, C-004, C-007, C-008, C-011, X-001, A-001 to A-005) plus 2 shared (C-003, X-003); C 4 alone (S-002, S-004, C-005, X-002) plus a share of C-006; A 4 alone (S-003, C-009, C-010, X-004) plus 2 shared; D 1 alone (X-005) plus shares of C-006 and X-003; B 0. Four points changed (C-001, C-006, C-009, X-005), all toward the merge base or D's amended guard.

**Overall:** the debate has converged on E's split. My additions are corrections that keep the merged rules consistent: `--only` on every commit (N2), a `GIT_INDEX_FILE` exemption in Layer 1 (N1), amendments to `SPEC:144` and the MDTM staging step (N3), exact-selector resumes (N4), the coordinator's own position for pr-submit (N5), revocation at checkpoints (N6) and report directories under `.dev/` (N7).

## Round 2.5: Invariant Probe
Independent fault-finder (not an advocate) probed the Round 2 consensus rule set (`round2-advocate-e.md` section 2.3). Full table: `invariant-probe.md`. 33 findings: 8 ADDRESSED, 25 UNADDRESSED (5 HIGH, 14 MEDIUM, 6 LOW).

HIGH UNADDRESSED (block convergence):
- INV-006: P1(b) misses the single-implement-worker case in the coordinator's own worktree; the ladder can revert the coordinator's or the person's files (`managed-workspace.md:85`, `retry.md:220`).
- INV-024: every worker session is told to `git add .dev/tasks` (`CLAUDE.md:37`; workflow and implement skills), so report-only workers sharing a worktree still write the user index and contend for `index.lock`.
- INV-025: "merge into a shared branch" has no quiescence condition, yet it moves HEAD where workers run.
- INV-026: spec D4 (a) still lets a brief authorize worker outward actions (post-release commit/push/PR, auggie-review `--post-pr`), contradicting the consensus that outward actions belong to the coordinator.
- INV-032: the rule set alone is not sufficient; no audit of git and gh write verbs in installed primitives has been done (reflect's `git worktree add/remove`, post-release's worktree, and the cases above).

MEDIUM warnings (do not block): INV-001, 002, 003, 004, 007, 008, 009, 015, 017, 022, 027, 028, 029, 033.

## Scoring Matrix
Winner per diff point after Round 2 (agreement counted across the five advocates' Round 2 tables; "agree" = at least 4 of 5).

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | V5 (E) | 95% | All five chose E's per-action owner/condition table as the merge form. |
| S-002 | V3 (C) | 95% | All five: only C verified Orca reuse, serialization, retention and idle-rule mechanics. |
| S-003 | V1 (A) | 92% | All five: GITDEMO procedure is A's; A itself marked it not re-run in Round 2. |
| S-004 | V3 (C) | 93% | All five: only C explains why the #326 relay cannot be something commands call. |
| C-001 | V5 (E), rule from V1, with P1 and `--only` | 92% | All five; E adds the porcelain cross-check and `git commit --only`. |
| C-002 | V5 (E) | 95% | All five; B conceded its guards; dormant for implement until #326 K3. |
| C-003 | V1 = V5, per-PR opt-in | 93% | All five: coordinator main chat by default; one pr-submit Task per PR only on explicit request. |
| C-004 | V5 (E) | 90% | All five (A and C moved): direct for outward, scoped quoted default-off grant for local commits. |
| C-005 | V3 (C) | 90% | All five: per-action Orca record, carried by the per-PR opt-in. |
| C-006 | Split | 55% | A and D: D's committer offload; C, D and E: per-PR Task offload; B: E. Unresolved. |
| C-007 | V5 (E) | 92% | All five: lock confined to one worktree; earlier commits survive. |
| C-008 | V5 (E), with P1 and M1 | 92% | All five. |
| C-009 | V1 (A) default, per-PR opt-in | 90% | All five (B, C, E moved). |
| C-010 | V1 (A) | 95% | All five: wording only. |
| C-011 | V5 (E) | 95% | All five: only E names the owner and the F3 guard. |
| X-001 | V5 (E) | 92% | All five (A moved): quoted scoped grant suffices for reversible local commits, never for outward actions. |
| X-002 | V3 (C) | 90% | All five; GitHub plus pr-submit run-log remain the outward record. |
| X-003 | V1 = V4 = V5, per-PR opt-in | 93% | All five (C moved). |
| X-004 | V1 (A) | 90% | All five (C moved): the rule is conditional on a named owner. |
| X-005 | V4 (D), as amended | 85% | All five: frontmatter hooks make the restriction real; settings-level exit 2 observed blocking under bypass (D N1). |
| A-001 | V5 (E), guard as backstop | 90% | All five (C, D moved). |
| A-002 | V5 (E) | 90% | All five (B, D moved). |
| A-003 | V5 (E), with P1 and M1 | 90% | All five (B moved). |
| A-004 | V5 (E) | 90% | All five (B moved). |
| A-005 | V5 (E) | 90% | All five (C moved). |

Points won: V5 (E) 15 alone plus 2 shared; V3 (C) 4 alone; V1 (A) 4 alone plus 2 shared; V4 (D) 1 alone plus 1 shared; V2 (B) 0; 1 split.

## Convergence Assessment
- Points resolved: 24 of 25
- Alignment: 96%
- Threshold: 80%
- Taxonomy gate: passed (L1, L2, L3 all covered)
- Invariant gate: FAILED (5 HIGH UNADDRESSED)
- Status: BLOCKED_BY_INVARIANTS
- Unresolved points: C-006 (diff point); INV-006, INV-024, INV-025, INV-026, INV-032 (invariants)
- Handling: depth standard has no Round 3. Base force-selected by score in Step 3; the five HIGH invariants are made mandatory changes in `refactor-plan.md`; the return contract reports `status: partial` and lists them.
