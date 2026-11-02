# Round 1 advocate: Variant 3 (option C, dedicated long-lived git session)

Persona: devops/architect (reliability, observability, orchestration mechanics) plus analyzer (evidence quality).
Debate: git ownership when an Orca coordinator runs IronClaude `/sc:` commands as workers.
Citation keys as in `variant-1-original.md`. Every citation below was re-read on 2026-11-02 (Orca CLI 1.4.237 guide via `orca-ide skills get orchestration ... | cat -n`; repo files via `sed -n`). Anything not re-read is marked UNVERIFIED.

## Position summary

A dedicated git worker should own every outward git and GitHub action (push, PR through `/sc:pr-submit --monitor 3`, review replies, issue or status comments), one Orca Task per action. That keeps the long pr-submit loop off the coordinator, gives each action an Orca record, and is the only option that does both. I concede that C should not own per-task local commits inside a sole-writer worker's run (E's rule is better there), and that C needs two spec changes (D3 (b), and a carve-out from `SPEC:156`'s "workers make no commits or pushes") before it is legal under the current spec.

## Steelman of each opposing variant

### A (coordinator runs all git in its main chat)
**Strongest form.** A has the fewest moving parts. The person gives an instruction and the same session acts on it, so the authorization cannot be lost, widened or forged on the way (V1 Safety). It is exactly what the spec already recommends: D3 (a) "Coordinator or person only (recommended)" (`SPEC:341`, `SPEC:343`) and D4 (b) for outward actions (`SPEC:347`). `/sc:pr-submit`'s top-level rule is met because the coordinator is the main orchestrating session (`sc-pr-submit-protocol/SKILL.md:47-49`). Only one session ever takes `index.lock`, and the only thing that can move HEAD is the coordinator, so the implement head-moved halt (`refs/retry.md:41,44`) is avoided by one rule. Cost is lowest: wording only (V1 Implementation cost). Its waiting problem is softened because Orca messages queue durably ([G] 73-74) and `check` replays the oldest Delivery until it is acknowledged ([G] 120-124).

**What it gets right.** Directness of authorization in an attended session, exact fit to the current spec text, and lowest implementation cost. These are real and I do not dispute them.

**Critique.**
1. The coordinator is the one session every worker depends on for answers. Workers' blocking questions go through `ask`, and the worker contract says "Resume the same message ID after an ask timeout" ([G] 80-82). While the coordinator sits in pr-submit's attended loop, whose per-wait budget is 600 s (`cmd/pr-submit.md:49`) and which can repeat over `--max-rounds` (default 2, hard cap 5, `cmd/pr-submit.md:47`), every blocked worker's `ask` times out and waits. Durable queueing ([G] 73-74) prevents loss, not delay. A trades throughput of the whole run for simplicity.
2. Orca's own guide says that if "the user's plan names a next owner, post-review fixes and PR preparation remain with that owner; the coordinator routes and synthesizes" ([G:cl] 62-65). V1 concedes this (V1 Weakness 3). A makes the coordinator both router and owner of PR preparation.
3. The "same session" advantage depends on an attended coordinator (A-001). If the person gives one instruction ("commit and open a PR when it passes") and leaves, A also acts on an up-front grant, the same kind C quotes in a brief.

### B (workers run their own git)
**Strongest form.** Only the worker knows when one of its own tasks ends, so only B (and E) can make the per-task commits #326 asks for (EVAL F1, `issue-326-evaluation.md:51`). Linked worktrees have separate index files and HEADs (GITDEMO), so one-worker-per-worktree has no lock contention and no cross-worker HEAD movement. A commit between one task's `complete` line and the next task's Q0 keeps the retry ladder valid, because Q0 records HEAD at each task's start (`sc-implement-protocol/SKILL.md:114`; `refs/retry.md:41`). Commits made before a crash survive, which is #326's stated point.

**What it gets right.** Per-task commits and crash survival of finished work. C does not solve either (C-002), and I concede it.

**Critique.**
1. Unsafe in the default layout. Orca's placement rule is "Use the current or an exact existing workspace by default. Create a worktree only when the user requested one or a concrete checkout or filesystem conflict makes sharing unsafe" ([G:pl] 8-11). B forces a worktree per committing worker, against that default (V2 Weakness 1).
2. Outward actions spread over N sessions. WC-9 exists to keep outward defaults off in workers (`SPEC:73`); B turns them on per worker. Each PR would need D3 (b) in every worker, against `SPEC:343`.
3. Highest cost and against the additive rule for Phases 1-3 (`SPEC:172`): every committing command needs a commit step, a stale-lock rule and a SHA field; implement currently says acceptance never "authorizes commit, PR, merge or release" (`refs/managed-workspace.md:63,67`, cited via `EVAL:63`, K3).
4. Merges back still need a single owner (V2 Weakness 4), so B is never complete alone.

### D (coordinator's Agent-tool subagent runs git)
**Strongest form.** D gives A's context relief with no Orca overhead: no 60 s readiness limit (`CAPS:44`), no retention request ([G:rc] 157), no Task bookkeeping. The subagent runs one at a time under the coordinator, so single-writer correctness equals A's. Subagents inherit the parent's permission mode, so a permission prompt still reaches the person (V4, AGENT-TOOL).

**What it gets right.** Cheapest way to move diff reading and commit-message drafting out of the coordinator's context for local commits.

**Critique.**
1. It cannot do the actions that matter most. `/sc:pr-submit` "MUST run in the main orchestrating session ... Do NOT run it inside an Agent-tool subagent" (`sc-pr-submit-protocol/SKILL.md:47-49`), and the main session must "Never hand a side effect to a background shell, detached loop, or subagent" (`SKILL.md:82-84`). So PRs, monitor pushes, replies and resolves fall back to A (V4 Weakness 1). D is a partial answer by design.
2. It breaks Orca provenance when provenance was requested: "Never substitute a non-Orca subagent tool when Orca orchestration provenance was requested" ([G] 46-47). A subagent is not a Task or Dispatch (`CAPS:155-158`), so git actions leave no Orca outcome.
3. Its "narrow tool list" benefit is void (X-005): V4 itself marks Bash-to-git-only restriction UNVERIFIED, and no agent in `src/superclaude/agents/` uses a `Bash(...)` pattern (V4 What D buys; I did not re-run that grep, UNVERIFIED by me).

### E (hybrid: sole-writer workers commit locally; coordinator owns outward)
**Strongest form.** E splits along the line the evidence actually draws. Local commits are safe for a worker exactly when it is the only writer in its worktree (separate index and HEAD per linked worktree, GITDEMO), and per-task commits are only possible where task boundaries are known (`SKILL.md:114`, `retry.md:41`, `SKILL.md:97` for batches). Outward actions stay where the person speaks and where pr-submit is allowed (`SKILL.md:47-49`), matching D3 (a) (`SPEC:341`) and leaving WC-9 as strict as today (`SPEC:73`). Its per-action ownership table (V5 The proposal) is the clearest statement of any variant, and its F3 guard on removing branches (no unmerged or open-PR branch removed without instruction, `EVAL` F3) is the only explicit cleanup rule.

**What it gets right.** Per-task commits (C-002), crash survival, the per-action table, the cleanup guard, and keeping outward actions out of ordinary workers. It is the strongest opponent.

**Critique.**
1. Its outward row inherits A's blocking problem unchanged: "Accepted as in A" (diff C-009). The pr-submit loop still holds the coordinator while workers wait on `ask` ([G] 80-82; `cmd/pr-submit.md:47,49`).
2. Its outward audit trail is the coordinator's transcript (V5 Safety), which is not an Orca record; nothing ties a push or PR to a Task outcome.
3. Two owners for local commits means two rule sets (V5 Weakness 1).
4. E's outward row and C are composable, not exclusive: E's table can name the git session as the owner of outward actions when the user opts in, with no change to E's worker-local commit row. That is my recommended merge (see Concessions).

## Strengths claimed

1. **Only C takes the pr-submit loop off the coordinator while still satisfying pr-submit's top-level rule.** A worker is a top-level session, so `/sc:pr-submit` may run there (`CAPS:161`; `sc-pr-submit-protocol/SKILL.md:47-49`). D cannot (`SKILL.md:47-49,82-84`); A and E accept the block (diff C-009). The loop's per-wait budget is 600 s (`cmd/pr-submit.md:49`) over up to `--max-rounds` cycles (default 2, cap 5, `cmd/pr-submit.md:47`). During that time a C coordinator keeps answering other workers' `ask` messages and validating `worker_done` ([G] 120-124). The spec already anticipates this case: D3 (b) exists "so several PRs can be monitored in parallel" (`SPEC:342`).

2. **One Orca record per action.** "A Task is work. A Dispatch is one authoritative Task attempt" ([G] 51-52). Each git action under C is its own Task with a brief (holding the quoted authorization), its own `worker_done` with an explicit `--outcome succeeded|failed` ("Never encode failure only in prose", [G] 88-90) and its own `return-contract.yaml` (WC-4). No other option gives a push or PR an Orca outcome: A and E keep outward actions in a transcript, D leaves no Orca record (`CAPS:155-158`), B scatters them across worker transcripts.

3. **Provenance-safe context relief.** C gives D's benefit (diffs, `git status` output and commit drafting stay out of the coordinator's context) without breaking "Never substitute a non-Orca subagent tool when Orca orchestration provenance was requested" ([G] 46-47).

4. **Serialization is enforced by Orca, not by convention.** A terminal that already owns an active Dispatch rejects another (`runtime_error`, "a target terminal that already owns an active Dispatch", [G:rc] 108). The git session can never run two git actions at once, so it never contends with itself for `index.lock` (GITDEMO). Honest scope: this does not stop the coordinator or another worker from running git; the "workers never run mutating git" rule still does that.

5. **Fits Orca's review-ownership rule.** The guide wants the coordinator to "route and synthesize", with PR preparation staying with "the next owner" the user's plan names ([G:cl] 62-65). C supplies that named owner. A violates the spirit of this unless the plan names the coordinator (V1 Weakness 3).

6. **C works without retention; retention is only an optimization.** If the user does not ask to keep the git terminal ([G:rc] 157), the coordinator releases it after each action ([G] 166-170) and starts a fresh git worker for the next action. That still gives strengths 1-5; the cost is a new readiness wait per action (limit 60 s, `CAPS:44`; a Claude worker start was observed at 34 s in the repo's own eval, quoted at `CAPS:47`). When the next git action is known at settlement time, same-terminal reuse is allowed with no user request ([G:cl] 48-55).

7. **Crash behaviour is clean and Orca-visible.** A git-session crash shows up in Orca liveness (`live` / `unverifiable` / `exited`, `CAPS:122-126`), the failed action is re-issued as a new Task (WC-6, `SPEC:70`), and a failed start still owns its terminal and is released, not closed by hand ([G:rc] 163-165). Under A a coordinator crash mid-action loses the actor and the record together.

8. **It is the orchestration-level form of #326's "central relay".** #326 asks to "evolve sc:git into a central relay for all other commands to use" (quoted at `EVAL:17`). Commands cannot call Orca or another session (SA-2, `SPEC:170`; WC-8, `SPEC:72`), so a relay cannot be something commands call. A session the coordinator feeds is the only relay shape the spec allows. If #326 later gives `/sc:git` an unattended mode, the git session runs it instead of raw git, with no design change.

## Weaknesses identified in other variants

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

## Concessions

1. **C conflicts with the spec as written, twice.** `SPEC:156` says of `/sc:git`: "Runs git itself, only when the user asked; workers make no commits or pushes." The git session is a worker, so C needs a named exception there. And running pr-submit in it is D3 (b), which the spec does not recommend: "Recommendation: (a), unless parallel PR monitoring is a real need" (`SPEC:343`). C is only legal after both changes.
2. **C does not solve per-task commits (C-002).** The coordinator sees only a worker's final `worker_done` ([G] 88-90), so it cannot time a commit between two tasks inside one implement run. E's sole-writer worker rule is better on this point, and I would adopt it unchanged.
3. **Retention is a stretch of its stated purpose.** `worker-retain --help` line 5 describes it as "Keep one supervised worker terminal live for debugging", and [G:rc] 157 allows it "only when the user explicitly wants the settled terminal kept live". A long-lived git session uses retention for something other than debugging. Strength 6 is my answer: C must be specified so that it works with a fresh git worker per action, and retention is an opt-in speed-up only.
4. **Reuse mechanics are partly UNVERIFIED.** For a Claude worker, Orca passes the task on the command line at launch (`CAPS:47`, `promptInjectionMode: 'argv'`); for a reused terminal Orca waits for an idle TUI instead (`CAPS:47`, the `n.reusesTerminal` branch), and how the next Task's text then reaches a running Claude session is UNVERIFIED. `worker-start --help` line 44 also says "Not every worker has a terminal" (the user's chat-tab setting, line 42), so whether `--terminal` reuse is available when workers run as chats is UNVERIFIED. What final cleanup of a reused terminal looks like is also UNVERIFIED: release leaves "Reused ... terminals ... retained" ([G:rc] 160-161).
5. **Authorization takes one hop** (X-001). The person's instruction reaches the git session only as a quote in the coordinator's brief (D4 (a), `SPEC:346`). In an attended session A is strictly more direct. C compensates with a per-action record, not with directness.
6. **For a local commit at a quiescent point in a shared worktree, C adds cost without adding correctness.** A, D and E get the same single-writer guarantee; C adds a Task, a brief and possibly a readiness wait (limit 60 s, `CAPS:44`) for a seconds-long action. On C-001 I rank E above C.
7. **Quiescence is still the coordinator's job** (A-003). The git session cannot know which workers write in a worktree; the coordinator must assert quiescence in each brief from its own placement map.
8. **The git session's own context grows over a long run** when reused, because reuse keeps the conversation (V3 Context load).

**Recommended merge for later rounds.** Take E's table as the base and change one row: outward actions (push, PR via `/sc:pr-submit --monitor 3`, replies, comments) are owned by a dedicated git worker, one Task per action, when the user opts in or when parallel PR monitoring or coordinator responsiveness is needed (D3 (b)); otherwise they stay with the coordinator as in E. Local commits follow E's rows unchanged.

## Shared-assumption responses

- **A-001 (coordinator session is attended): QUALIFY.** True for the interactive case the variants describe, but no Orca mechanism guarantees it. When the person gives one instruction and leaves, every option acts on an up-front grant; A's "same session" advantage then shrinks to the same grant C quotes. In that case C's per-Task brief is the better record of which grant each action used.
- **A-002 (contract file lists are complete): REJECT.** Nothing makes `artifacts` plus `--files-modified` complete; [G] 91 only says to append `--files-modified` "with real values when applicable", not that every touched file is listed. Whoever commits should run `git status --porcelain` in that worktree at the quiescent point and report unlisted paths to the coordinator, never sweep them with `git add -A` and never silently drop them. A C git session is a natural place for that check because it already reads the diff.
- **A-003 (quiescence is knowable): QUALIFY.** Knowable only from the coordinator's own placement records; the claim that no Orca verb maps worktrees to running writers comes from the diff analysis and I did not re-verify it (UNVERIFIED by me). Under C the coordinator must state quiescence in each git brief; the git session cannot check it. E's sole-writer rule makes it true by construction for worker-local commits.
- **A-004 (a commit does not rewrite files): ACCEPT the diff's verdict (contradicted where hooks are installed).** Verified: `.pre-commit-config.yaml` defines `trailing-whitespace` (line 9), `end-of-file-fixer` (line 11), `ruff-format` (line 111) with `default_stages: [commit]` (line 143); this clone's hooks directory holds only `*.sample` files and `core.hooksPath` is unset (checked 2026-11-02). Where hooks are installed, any committer must commit only at quiescence and re-stage or report hook rewrites; this applies to every option equally.
- **A-005 (a standing instruction covers later commits): QUALIFY.** `CLAUDE.md:37` says only "commit only when asked". The #326 evaluation treats per-task commits as "an authorized option, never a default" and says the owner's issue comment "does not by itself authorize commits in a worker" (`EVAL:74`). A standing instruction should count only when it names its scope (this run, this branch, these action types); each C Task brief should quote it, so every commit shows which standing grant it relied on.

## Per-point positions

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
