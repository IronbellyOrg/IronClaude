<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 3 (option c) -->
<!-- Merge date: 2026-11-02T18:19:27Z -->

# D3 merged position: pr-submit is not an Orca worker; one session per PR by default, one person-owned tab per PR when the person names several

<!-- Source: Variant 1, Position (V1:3) and "How a person works day to day" (V1:17), merged per Change #1; Base (original, modified) V3:3, launch command and handoff citations kept, adjusted per Change #2 (child worktree) -->
Position: under this decision `/sc:pr-submit` does not run as an Orca worker, and it gains no `--unattended` mode and no Phase 4 edits (`SPEC:341`); option (b) stays deferred, not rejected, under the conditions in "Implementation cost". By default, after the workers finish, one ordinary top-level session runs it for one PR, standing in that PR's own child worktree (see "Where the run happens"). Only when the person names several PRs does the coordinator, on the person's instruction, launch one tab per named PR as an Orca full handoff: a fresh Claude agent in that PR's child worktree with the slash command as its prompt (`ORCA agent launch --agent claude --worktree <id> --prompt "/sc:pr-submit --monitor 3 --head <branch> ..." --json`, `[CLI]` lines 49-52), gated by the launch check under "Reliability". Each new tab is an ordinary session the person owns; the coordinator does not create a Task or wait on it (`[CLI]` lines 27-31).

<!-- Source: refactor-plan.md, Overview citation key (replaces the base's citation key line, V3:5) -->
Citation key: `SKILL.md:N` = `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:N` (the installed `~/.claude/skills/` copy is byte-identical, checked with `diff -q` on 2026-11-02); `refs/state-machine.md:N` = that skill's `refs/state-machine.md`; `commands/pr-submit.md:N` = `src/superclaude/commands/pr-submit.md:N`; `HWW:N` = `src/superclaude/core/HOW-WE-WORK.md:N`; `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `CR-01:N` = `.dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md:N`; `GO-BS:N` / `GO-RP:N` = `.dev/orca-command-refactor/decisions/git-ownership/debate/adversarial/base-selection.md:N` / `refactor-plan.md:N`; `V1:N` etc. = line N of `variant-N-original.md`; `[CLI] N` / `[G] N` = line N of `orca-ide skills get orca-cli` / `orca-ide skills get orchestration`; `worker-start --help` / `worktree create --help` line N = `orca-ide orchestration worker-start --help` / `orca-ide worktree create --help`.

## Where the run happens

<!-- Source: refactor-plan.md Change #2 (fixed constraints K1, K4, K5; closes INV-001 and INV-014, `invariant-probe.md:22,35`); new section -->
pr-submit has no worktree argument (`commands/pr-submit.md:8`). It binds to the checkout of the session it runs in, with `git branch --show-current` and `git rev-parse HEAD`, and requires the local branch name to equal the PR's head branch exactly (`SKILL.md:268`; `src/superclaude/pr_submit/fsm.py:548`). CR-01 gives each `/sc:pr-submit` run its own child worktree, because "its checkout must be the PR head with no other writer for the whole loop" (`CR-01:19`), while the coordinator runs in the feature's parent worktree (`CR-01:15`). The git-ownership merge reaches the same point from the other side: "under D3 (a) the coordinator itself must stand in the PR-head checkout", and it marks as UNVERIFIED whether a coordinator can move its session there mid-run (`GO-RP:35-36`). Whether a Claude Code session can keep a sibling worktree as its working checkout for every git, gh and script call of a 40-minute loop (for example after adding it as a working directory) is UNVERIFIED here too. The rules below are a judgment from K4, K5 and that UNVERIFIED behaviour, not a fixed constraint.

1. **One child worktree per PR.** It is created before the run, by Orca at Orca's default path, never under `.dev/worktrees/` (`CR-01:41`), with `orca worktree create --name <name> --parent-worktree <feature worktree> --base-branch <feature branch> --setup run --json` and without `--agent` (`worktree create --help` lines 3, 23, 32-33). The PR's head branch is that child's own branch and is checked out only there (git allows a branch in one worktree at a time, `invariant-probe.md:22`).
2. **The run's session stands in that child.** The session that runs pr-submit is a top-level Claude session whose checkout is that child worktree for the whole loop.
3. **Carrier order.** The coordinator's own session carries the run only after a check shows it can stand in the child for the whole loop; that is UNVERIFIED today, so this carrier is not yet usable. Until then, the carrier is an ordinary top-level session opened in the child, either by the person or launched by the coordinator for the person with the `agent launch` route from the Position (the start guard under "Safety" and the launch check under "Reliability" apply).
4. **Open gap for the consolidated revision.** CR-01 does not say whether the PR head is the feature branch (held by the parent worktree, `CR-01:15`) or the child's own branch. This decision requires the child's own branch.

- **Conflict with the git-ownership decision.** The git-ownership merge makes the coordinator, "in its main chat", the owner of every outward action, including the PR through `/sc:pr-submit --monitor 3` (`GO-BS:172`). Until the coordinator check in item 3 passes, this decision puts the PR and its fix pushes in a session opened in the child worktree, under the person's named instruction ("Safety"). The consolidated revision must either amend git-ownership row 1 to allow that carrier, or verify the coordinator check and drop the fallback. Both decisions already agree on the condition (the carrier stands in the PR-head checkout with no other writer); they differ only on which session can do it today.

## Before the run

<!-- Source: refactor-plan.md Change #4 (closes INV-017 and INV-007, `invariant-probe.md:38,28`); new section -->
pr-submit never commits the change or pushes the head branch: Wave 0 opens the PR with no push, and its only push is the cycle's one fix commit (`SKILL.md:267`, `SKILL.md:274`). On the create path Wave 0 rebases a branch that is behind `origin/<base>` (`SKILL.md:267`), and a rebased branch that was already pushed HALTs with `pr_head_mismatch` and "needs a force-push, which this skill never does for you" (`SKILL.md:268`). The fork's master is often ahead of the local master (`CLAUDE.md:65`). So the run depends on D4 through the pre-PR steps, which happen in this order, all before any run starts:

1. The change's commits are on the feature branch in the parent worktree, made by a worker only where D4 lets a brief authorize local commits, otherwise by the git owner.
2. The git owner rebases the feature branch onto `origin/<base>` in the parent worktree.
3. The git owner creates the PR's child worktree from it ("Where the run happens", item 1).
4. The git owner pushes the child's branch by name (`git push origin <child-branch>`) with the person's approval ("Push only with approval", `HWW:215`).
5. Only then is the run started.

No commit lands on the feature branch between steps 3 and 5. The git owner is the coordinator under the git-ownership merge (`GO-BS:172`; the owner role itself is at `CR-01:34`). Under D4 (b), (c) or (c′) workers never push (`SPEC:347`; `decisions/D4/option-c.md:3`; D4 converged on (c′), `decisions/D4/debate/adversarial/debate-transcript.md:720-722`), so steps 2-4 always sit with the coordinator or the person.

<!-- Source: refactor-plan.md Change #7 (INV-023 gate G7; INV-009, `invariant-probe.md:30`) -->
- **Readiness.** The child worktree's setup has succeeded (`CR-01:24`), `gh` is authenticated, and the review App is installed on the fork before a run starts; otherwise pr-submit STOPs at preflight (`commands/pr-submit.md:28-30`; "Monitored runs require the review App, matching PR head checkout/commit and CI-wait prerequisites", `HWW:223`).

<!-- Source: refactor-plan.md Change #15 (closes INV-023, `invariant-probe.md:44`; gate requirement `debate-transcript.md:655`) -->
**Gate list.** Each gate between "workers finish" and "a monitored loop is running" has an owner, checked in this order:

- [ ] G1 start authority: the start guard under "Safety".
- [ ] G2 commits exist, G3 head branch pushed, G4 branch not behind base: steps 1-4 above.
- [ ] G5 target repo from origin: passes unchanged (`SKILL.md:267`).
- [ ] G6 checkout equals PR head: "Where the run happens".
- [ ] G7 environment and review App: the readiness bullet above.
- [ ] G8 the launched prompt runs as a slash command on the person's surface: the launch check under "Reliability".
- [ ] G9 one monitor per PR: the one-monitor rule under "Reliability".
- [ ] G10 someone reads the terminal status: accepted risk. The person reads the tab; the coordinator does not track completion, by design (INV-003, `invariant-probe.md:24`; `[G]` line 39).

## Why not a worker now, and why a third route

<!-- Source: Variant 2, Strongest case (V2:9), merged per Change #10 (X-001 to V2, 95%, unanimous); replaces the base's V3:8 claim that an Orca worker is unattended and so conflicts with pr-submit -->
- **"Attended" means in-session, not watched.** pr-submit defines its loop as "an **attended, in-session** loop: closing the session loses it. Durability comes from the write-ahead JSONL run-log + `--resume`, never from detachment" (`SKILL.md:43-45`), and it never hands a side effect "to a background shell, detached loop, or subagent" (`SKILL.md:82-84`). Push authorization is the `--monitor 3` arming plus the `push_decision` record; there is no interactive confirmation before a push (`refs/state-machine.md:170-172`).
- **At `--monitor 2` or `3` nothing requires a person to watch.** At `--monitor 1` the run ends on a "fix these? y/n" proposal to the person (`SKILL.md:272`), which is why the spec refuses `--monitor 1` under `--unattended` (`SPEC:56`).
- **A terminal Orca worker meets that text.** It is a top-level Claude session (`CAPS:161`; `worker-start --help` line 38); `CAPS:47` shows only that its task arrives on the command line. Whether a chat-surface session (`outcome.kind` `structured`, `[CLI]` line 47) is a Claude Code session with the Skill and Task tools and long foreground Bash waits is UNVERIFIED. The same question applies to the tabs this decision launches, because both follow the person's Chat UI setting (`[CLI]` line 63; `worker-start --help` line 42).
- **So the "attended" rule does not rule (b) out.** (b) is deferred, not rejected, until the conditions under "Implementation cost" hold.

<!-- Source: Base (original, modified), V3:8: the non-conflated clause kept; the "unattended worker" clause removed per Change #10 -->
- **Why a third route.** (a) runs one PR per session; (c) gives several PRs at once with the command exactly as it is today, each run a normal top-level session in a visible tab.

## Safety

<!-- Source: Base (original, modified), V3:11, adjusted per Change #13 (Correctness 1 and 5; X-003, C-003; better variant V1:10); the `CAPS:52` readiness claim dropped -->
- pr-submit runs unchanged, with every HALT and guard as written (`commands/pr-submit.md:28`, `commands/pr-submit.md:85`). Every operator HALT (`pr_head_mismatch`, `push_range_mismatch`, `fix_commit_failed`, a `needs_human_decision` finding) ends the run with `terminal_halted`, and its recovery steps stay in that session or tab for the person (`SKILL.md:268,274,316-318,325`); the round cap ends the run with `terminal_max_rounds` (`SKILL.md:276`).

<!-- Source: Base (original, modified), V3:12, adjusted per Change #13 (quote `[G]` line 39 in full) -->
- Orca's guide makes the handoff the correct route for unsupervised work: "The user asks to hand off ownership or start another agent/worktree without supervision | Handoff owner | Use `orca-cli`; create no Run, Task, or Dispatch and do not monitor completion" (`[G]` line 39).

<!-- Source: refactor-plan.md Change #3 (closes INV-006, `invariant-probe.md:27`; INV-019 ADDRESSED); replaces the base's V3:13 -->
- **Start guard.** A pr-submit run is started, by the person or by the coordinator's launch, only when the person's own instruction names opening (or attaching to) the PR for that branch at `--monitor 3` ("Push only with approval", `HWW:215`; `--monitor 3` is a "Requested and authorized full loop", `HWW:221`; the coordinator runs git "only when the user asked", `SPEC:156`). Without that instruction the coordinator reports the ready branch, its child worktree and the exact command line, and starts nothing ("Recommending any branch performs no Git/GitHub action", `HWW:223`). The coordinator records the instruction text beside each launch it reports.

<!-- Source: Variant 1, Safety (V1:9), strength 2 in base-selection.md:173 (C-002); placed in Safety per the orchestrator's section list, not a numbered plan change -->
- At its default `--monitor 3` pr-submit commits, pushes the fixes without asking, and replies to and resolves the review comments it fixed (`CLAUDE.md:50`; `HWW:221`). So the safety difference between routes is visibility and who authorized the start, not a per-push approval.

<!-- Source: refactor-plan.md Change #8 (fixed constraint K3, commit `80f934de`, PR #343) -->
- **Two fix cycles, then the person decides.** Runs use the default `--max-rounds 2` and are never launched with a higher value (pr-submit itself still accepts up to 5, `commands/pr-submit.md:47`). At the cap the run ends `terminal_max_rounds` (`SKILL.md:276`) and the open findings go to the person, who decides. Low and Nit findings are reported, never fixed (`SKILL.md:270`), matching "only blocking findings fail a review". Exception: after an Augment decline, the single-shot fallback can add one more fix push for the whole run (`push_count <= max_rounds + 1`, `SKILL.md:275`); whether that counts as a third fix cycle under #343 is UNVERIFIED, so until it is settled it is reported to the person as a deviation from the 2-cycle rule, not as a pass. Whether #343's "blocking" grade maps exactly onto pr-submit's Medium-and-above routing is also UNVERIFIED (PR #343 did not touch pr-submit).

<!-- Source: refactor-plan.md Change #9 (fixed constraint K2, `CR-01:45`) -->
- **Fork only.** The PR is opened only by pr-submit on origin (`IronbellyOrg/IronClaude`; target repo from origin, `SKILL.md:267`; never an upstream parent, `SKILL.md:304`). Launches pass no Orca `--pr` / `--issue` linking, because Orca records this project as `github:superclaude-org/superclaude_framework` (`CR-01:45`).

## Reliability

<!-- Source: Base (original), V3:16; citations restated in the plan's citation key -->
- No worker-contract pieces at all: no heartbeat, no contract file, no `worker_done`. The run-log in `--output-dir` (`commands/pr-submit.md:55`) and `--resume` (`commands/pr-submit.md:56`) work as today.

<!-- Source: Base (original, modified), V3:17, adjusted per Change #13 (X-004: "or the coordinator reads the run-log file later" removed) -->
- Weakness: the coordinator gets no completion signal and does not track completion; the person reads each tab (`[G]` line 39).

<!-- Source: Variant 2, Reliability (V2:17) and Implementation cost (V2:24) as the model for a pass condition, merged per Change #6 (closes INV-008; INV-022); replaces the UNVERIFIED sentence of V3:17 -->
- **Launch check.** Whether a slash command passed as `--prompt` runs as a slash command is UNVERIFIED until this check passes; until then only the person-typed route is used. On the person's actual Chat UI setting (chat and terminal both, if both are used; `agent launch` follows that setting, `--surface chat|terminal` overrides it, `[CLI]` line 63), run `orca agent launch --agent claude --worktree <scratch child worktree> --prompt "/sc:pr-submit --monitor 1 --pr <scratch PR> --max-rounds 2" --json`. The scratch PR is on `IronbellyOrg/IronClaude`, and its head branch is that child worktree's own branch, pushed by the person beforehand (pr-submit requires the local branch name to equal the PR head exactly, `src/superclaude/pr_submit/fsm.py:548`). A run at `--monitor 1` reads and polls only: L1 applies no edits (`SKILL.md:272`) and the Augment poke is L3-only (`commands/pr-submit.md:50`). Pass: the launch's `prompt.outcome` is `journaled` or `handed-to-terminal` (`[CLI]` line 29); the tab shows the skill loaded; the run's output directory holds a run-log with at least one Wave 1 or Wave 8 poll event and no HALT; the PR gains no commit, comment or thread change. Whether several poll iterations occur on a PR the review App has already reviewed is UNVERIFIED, so use a PR the App has not yet reviewed when a long wait must be shown. The run ends on L1's "fix these? y/n" proposal (`SKILL.md:272`), which the person answers "n".

<!-- Source: refactor-plan.md Change #5 (closes INV-012, `invariant-probe.md:33`; addresses INV-002, `invariant-probe.md:23`) -->
- **One live monitor per PR.** At most one pr-submit run per PR at a time: pr-submit has no PR-level lock, by design (`SKILL.md:306`), so a second run in the same worktree could commit and push another run's unvalidated edits in its one fix commit (`invariant-probe.md:33`). Before any launch for a PR, the coordinator checks the PR's child worktree for a run-log under `.dev/pr-monitor/pr-<N>-*/` (`commands/pr-submit.md:55`) whose last event is not a terminal status, and for a live agent tab there; if either exists it launches nothing and tells the person to continue that run, or to `--resume` it after the tab is closed. A person who types the command checks the same thing. Whether a live tab can be detected reliably is UNVERIFIED.
- **Lost launches and resumes.** The coordinator records the worktree id, agent handle and `operationId` of each launch and repeats a lost launch only with `--retry-launch <operationId>` (`[CLI]` line 65). A resume uses `--resume <run-log>` in the same child worktree.
- **Keep the worktree until the run is over.** The child worktree holds the run-log, the only recovery state (`commands/pr-submit.md:55`). The git owner removes the child worktree (CR-01 cleanup, `CR-01:23`) only after the run reached a terminal status and the PR is merged or closed. That status is established once, at cleanup time, from the person's report or one read of the run-log's final event when the person asks for cleanup; this is a precondition check, not monitoring.

## How a person works day to day

<!-- Source: Variant 1, "How a person works day to day" (V1:17), merged per Change #1, without its coordinator-session clause (Change #2 governs the carrier) and without its withdrawn "rarely needed" clause (X-002) -->
- One PR, one session: the default. A single PR goes through one ordinary session the person directs (INV-016, `invariant-probe.md:37`).

<!-- Source: Base (original, modified), V3:20, scoped to the several-PR case per Change #1 -->
- Several named PRs: one tab per PR, each showing the review loop live; the person steps in on a HALT. The coordinator's session stays free.

<!-- Source: refactor-plan.md Change #14 (INV-018, `invariant-probe.md:39`) -->
- **Order of the coordinator's two roles.** The coordinator first settles its supervised Run (reads every contract, admits or rejects results, releases its workers; `[G]` line 37), then performs the pre-PR steps ("Before the run"), then launches the tabs, reports each worktree id, handle and the person's instruction, and does not watch the tabs (`[G]` line 39; `[CLI]` lines 27, 29). "Stops" means it does not monitor them, not that its other unrelated work ends.

## Implementation cost

<!-- Source: Variant 1, Implementation cost (V1:21), merged per Change #12 (S-004, C-009); replaces the base's V3:23 "no pr-submit edits, no AC-4.3" clause, which it repeats -->
- 35, not 36, commands accept `--unattended` (`SPEC:195`; `SPEC:197`); no pr-submit edits; no AC-4.3 (`SPEC:276`).

<!-- Source: Variant 2, Round 2 rebuttal (`debate-transcript.md:662`), merged per Change #11 (INV-010, INV-011); replaces the base's "One sentence in section 4 / D3 of the spec" (V3:23) -->
- **Spec corrections that hold whatever D3 decides:**
  1. The `SPEC:137` row drops "(the worker may use `ask` or `escalation`)", which contradicts WC-3 (`SPEC:67`).
  2. WC-7 (`SPEC:71`) and the `SPEC:137` row cite the top-level rule at `sk/sc-pr-submit-protocol/SKILL.md:47-49`, not `37-39`.
  3. The D3 text at `SPEC:340` cites the outward actions at `SKILL.md:267,274` and the attended loop at `SKILL.md:43-45,51-84`. Its `189,196` now point at S5 re-review attribution text, and `41-64` only partly covers the loop, which runs 51-80.
  4. Every other pr-submit citation in `SPEC:74` (WC-10) and `SPEC:137` is re-checked against the current file in the same revision.

<!-- Source: Variant 2, Implementation cost (V2:24), merged per Change #6 -->
- The launch check under "Reliability" costs one scratch PR on the fork.

<!-- Source: Variant 2, Strongest case (V2:9), reopening conditions merged per Change #10; Base (original) V3:23 "Cost to switch to (b) later is unchanged" kept -->
- **(b) is deferred until all of these hold:** tracked parallel monitoring is a stated need; D4 lets a brief authorize a worker's push (D4's converged (c′) does not, so under it a `--monitor 3` worker has no role, `HWW:223`; `decisions/D4/option-c.md:3`); AC-4.3 passes (`SPEC:276`); the chat-surface question under "Why not a worker now" is checked. Cost to switch to (b) later is unchanged.
