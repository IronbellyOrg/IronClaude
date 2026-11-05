# Refactoring Plan: Merge into Base (Variant 3)

## Overview
- Base: Variant 3 (option c, unsupervised orca-cli handoff to a person-owned tab), `variant-3-original.md`, selected by the level-1 tiebreaker (`base-selection.md`, "Combined Scoring").
- Incorporating strengths from: Variant 1 (option a, coordinator or person only) and Variant 2 (option b, worker with pre-authorization); plus the four HIGH invariants that the convergence gate made mandatory (`debate-transcript.md:655`: INV-006, INV-012, INV-017, INV-023) and selected MEDIUM items from `invariant-probe.md`.
- Fixed constraints applied as given by the team lead, not debated: (K1) every worktree is created by Orca at Orca's default path, never under `.dev/worktrees/` (`changes/CR-01-feature-worktree-hierarchy.md:41`); (K2) SuperClaude upstream is never pushed to or interacted with (`CR-01:45`); (K3) merged PR #343: only blocking findings fail a review, and review loops cap at 2 fix cycles, then escalate (commit `80f934de`); (K4) CR-01: each `/sc:pr-submit` run gets its own child worktree on the PR head (`CR-01:19`); (K5) a pr-submit run needs a PR-head checkout with no other writer for the whole loop (`~/.claude/skills/sc-pr-submit-protocol/SKILL.md:268,274,318`).
- Planned changes: 15
- Risk level: Medium overall. Two changes modify the base's core claim (Changes 2 and 13); the rest are additive wording.
- Drafted by the orchestrating agent after the restart (the debate-orchestrator role); reviewed by a separate analytical agent (`refactor-plan-review.md`); revised for its findings F-01 to F-17 (see "Review Status").
- Citation key: `SKILL.md:N` = `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:N` (the installed `~/.claude/skills/` copy is byte-identical, checked with `diff -q` on 2026-11-02); `refs/state-machine.md:N` = that skill's `refs/state-machine.md`; `commands/pr-submit.md:N` = `src/superclaude/commands/pr-submit.md:N`; `HWW:N` = `src/superclaude/core/HOW-WE-WORK.md:N`; `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `CR-01:N` = `.dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md:N`; `GO-BS:N` / `GO-RP:N` = `.dev/orca-command-refactor/decisions/git-ownership/debate/adversarial/base-selection.md:N` / `refactor-plan.md:N`; `V1:N` etc. = line N of `variant-N-original.md`; `[CLI] N` / `[G] N` = line N of `orca-ide skills get orca-cli` / `orca-ide skills get orchestration`; `worker-start --help` / `worktree create --help` line N = `orca-ide orchestration worker-start --help` / `orca-ide worktree create --help`.

## Planned Changes

### Change 1: Lead with "never an Orca worker"; one run per PR by default (from Variant 1)
- **Source**: Variant 1, Position (V1:3) and "How a person works day to day" (V1:17), without V1:17's "from the coordinator's session ... where they already talk to the coordinator" clause (Change 2 governs the carrier) and without its withdrawn "rarely needed" clause.
- **Target**: Base, Position (restructure).
- **Rationale**: S-003 (V1, 93%), C-002 (V1, 97%), A-004 (V1, 95%), X-005 (V1, 92%) are sole V1 wins; all three Round 2 recommendations make (a) the answer and the default (`debate-transcript.md:661-665`). INV-016 (single-PR case uses one session) is ADDRESSED. The base opens with the parallel route; the merge must open with the rule and the default, and make parallel tabs the case "when the person names several PRs".
- **Integration point**: Position paragraph: first sentence states the rule: under this decision pr-submit does not run as an Orca worker and gains no `--unattended` mode and no Phase 4 edits; (b) stays deferred under the conditions in Change 10 (review F-04: "never" would read as a rejection). Second sentence states the default (one ordinary top-level session per PR, after the workers finish). Third sentence introduces several tabs at once only when the person names several PRs.
- **Risk**: Medium. Restructures the base's opening; no claim is lost.

### Change 2: The run's session must stand in the PR's own child worktree (fixed constraints K1, K4, K5; closes INV-001 and INV-014)
- **Source**: CR-01 T3 (`CR-01:19`), K4 and K5 (`SKILL.md:268,274,318`), INV-001 and INV-014 (`invariant-probe.md:22,35`); git-ownership merge row 1 (`GO-BS:172`) and its Change 3 (`GO-RP:35-36`).
- **Target**: Base, Position and a new section "Where the run happens" (insert after Position).
- **Rationale**: The consensus said the coordinator or person runs pr-submit "from the change's worktree", and INV-001 found no mechanism for the coordinator's session to be in another worktree: pr-submit has no worktree argument (`commands/pr-submit.md:8`) and binds to the session's own checkout with `git branch --show-current` / `git rev-parse HEAD`, requiring the local branch name to equal the PR's head branch exactly (`SKILL.md:268`; `src/superclaude/pr_submit/fsm.py:548`). Under K4 the run's checkout is the PR's child worktree, created by Orca at its default path (K1), while the coordinator runs in the feature's parent worktree (`CR-01:15`). The git-ownership merge reaches the same point from the other side: "under D3 (a) the coordinator itself must stand in the PR-head checkout", and it marks as UNVERIFIED whether a coordinator can move its session there mid-run (`GO-RP:35-36`). Whether a Claude Code session can keep a sibling worktree as its working checkout for every git, gh and script call of a 40-minute loop (for example after adding it as a working directory) is UNVERIFIED here too. This change is a judgment from K4, K5 and that UNVERIFIED behaviour, not a fixed constraint (review F-02).
- **Integration point**: New section listing: (1) one child worktree per PR, created before the run by `orca worktree create --name <name> --parent-worktree <feature worktree> --base-branch <feature branch> --setup run --json` without `--agent` (`worktree create --help` lines 3, 23, 32-33; review F-15); the PR's head branch is that child's own branch and is checked out only there (git allows a branch in one worktree at a time). (2) The session that runs pr-submit is a top-level Claude session whose checkout is that child for the whole loop. (3) Carrier order: the coordinator's own session only after a check shows it can stand in the child for the whole loop (UNVERIFIED today, so not yet usable); until then, an ordinary top-level session opened in the child, either by the person or launched by the coordinator for the person with the base's `agent launch` route (Change 3 guard and Change 6 check apply). (4) Open gap for the consolidated revision: CR-01 does not say whether the PR head is the feature branch (held by the parent, `CR-01:15`) or the child's own branch; this change requires the child's own branch.
- **Cross-decision conflict (review F-01)**: the git-ownership merge makes the coordinator, "in its main chat", the owner of every outward action including the PR through `/sc:pr-submit --monitor 3` (`GO-BS:172`). Until the coordinator check in (3) passes, this change puts the PR and its fix pushes in a session opened in the child worktree, under the person's named instruction (Change 3). The consolidated revision must either amend git-ownership row 1 to allow that carrier, or verify the coordinator check and drop the fallback. Both decisions already agree on the condition (the carrier stands in the PR-head checkout with no other writer); they differ only on which session can do it today.
- **Risk**: High. It changes who carries the default run until a check passes, and it touches another decision's owner row. Rollback: restore V1's "coordinator or person" wording and reopen INV-001.

### Change 3: Start only on the person's named instruction (closes INV-006; keeps base V3:13, re-anchored)
- **Source**: INV-006 (`invariant-probe.md:27`); `HWW:215` ("Push only with approval"), `HWW:221` (monitor 3 is a "Requested and authorized full loop"); base V3:13; INV-019 ADDRESSED (authority from `HWW:215` / `HWW:221`, not D4).
- **Target**: Base, Safety (replace V3:13).
- **Rationale**: R2-V1 #13 conceded the omission; every Round 2 (a) sentence lacked the guard (`invariant-probe.md:27`). `SPEC:156` already limits the coordinator to git "only when the user asked".
- **Integration point**: Safety bullet: a pr-submit run is started, by the person or by the coordinator's launch, only when the person's own instruction names opening (or attaching to) the PR for that branch at monitor 3; without it the coordinator reports the ready branch, its child worktree and the exact command line, and starts nothing (`HWW:223`: "Recommending any branch performs no Git/GitHub action"). The coordinator records the instruction text beside each launch it reports.
- **Risk**: Low. Additive.

### Change 4: Pre-PR steps and their owner (closes INV-017 and INV-007; INV-023 gates G2-G4)
- **Source**: INV-017 (`invariant-probe.md:38`), INV-007 (`:28`); `SKILL.md:267` (Wave 0 rebases if behind on the create path), `SKILL.md:268` (a rebased, already-pushed branch HALTs `pr_head_mismatch` and needs a force-push the skill never does); `CLAUDE.md:65`; D4 converged position (c′) (`decisions/D4/debate/adversarial/debate-transcript.md:720-722`; `decisions/D4/option-c.md:3`).
- **Target**: Base, new section "Before the run" (insert after "Where the run happens").
- **Rationale**: pr-submit never commits the change or pushes the head branch (`SKILL.md:267`, `:274`), so "(a) and (c) need no D4 answer" (C-008, 90%, with the INV-017 caveat) does not hold for the pre-PR steps.
- **Integration point**: Ordered steps, all before any run starts (review F-07): (1) the change's commits are on the feature branch in the parent worktree (made by a worker only where D4 lets a brief authorize local commits, otherwise by the git owner); (2) the git owner rebases the feature branch onto `origin/<base>` in the parent; (3) the git owner creates the PR's child worktree from it (Change 2); (4) the git owner pushes the child's branch by name (`git push origin <child-branch>`) with the person's approval (`HWW:215`); (5) only then is the run started. No commit lands on the feature branch between steps 3 and 5. The git owner is the coordinator under the git-ownership merge (`GO-BS:172`; the owner role itself is at `CR-01:34`). Under D4 (b), (c) or (c′) workers never push, so steps 2-4 always sit with the coordinator or the person.
- **Risk**: Medium. New content; it couples D3 wording to D4 and git ownership explicitly.

### Change 5: One live monitor per PR; keep the worktree until the run is over (closes INV-012; addresses INV-002)
- **Source**: INV-012 (`invariant-probe.md:33`), INV-002 (`:23`); `SKILL.md:306` (no lock file, by design), `commands/pr-submit.md:55` (run-log inside the worktree by default); `[CLI]` line 65 (`--retry-launch`).
- **Target**: Base, Reliability (append).
- **Rationale**: pr-submit has no PR-level lock, so a second run in the same worktree can commit and push another run's unvalidated edits in its one fix commit (`invariant-probe.md:33`). The child worktree holds the run-log, and `worktree rm --force` deletes the only recovery state.
- **Integration point**: Reliability bullets: at most one pr-submit run per PR at a time. Before any launch for a PR, the coordinator checks the PR's child worktree for a run-log under `.dev/pr-monitor/pr-<N>-*/` whose last event is not a terminal status, and for a live agent tab there; if either exists it launches nothing and tells the person to continue that run, or to `--resume` it after the tab is closed. A person who types the command checks the same thing (review F-05; whether a live tab can be detected reliably is UNVERIFIED). The coordinator records the worktree id, agent handle and `operationId` of each launch and repeats a lost launch only with `--retry-launch <operationId>` (`[CLI]` line 65). A resume uses `--resume <run-log>` in the same child worktree. The git owner removes the child worktree (CR-01 cleanup, `CR-01:23`) only after the run reached a terminal status and the PR is merged or closed; that status is established once, at cleanup time, from the person's report or one read of the run-log's final event when the person asks for cleanup, which is a precondition check, not monitoring (review F-06).
- **Risk**: Low. Additive.

### Change 6: A defined smoke test for the coordinator-launched route (from Variant 2's success criterion; closes INV-008; INV-022)
- **Source**: Variant 2, Reliability (V2:17) and Cost (V2:24): an explicit pass condition (Completeness 4, only V2 met it); INV-008 (`invariant-probe.md:29`); INV-022; `[CLI]` line 63 (launch follows the person's Chat UI setting; `--surface chat|terminal` overrides).
- **Target**: Base, Reliability (replace the UNVERIFIED sentence of V3:17 with the check that resolves it) and Implementation cost.
- **Rationale**: The consensus gated (c) on a smoke test with no target or pass condition. A run at `--monitor 1` against an existing scratch PR on the fork reads and polls only: L1 applies no edits (`SKILL.md:272`) and the Augment poke is L3-only (`commands/pr-submit.md:50`).
- **Integration point**: Acceptance check: on the person's actual Chat UI setting (chat and terminal both, if both are used), `orca agent launch --agent claude --worktree <scratch child worktree> --prompt "/sc:pr-submit --monitor 1 --pr <scratch PR> --max-rounds 2" --json`, where the scratch PR is on `IronbellyOrg/IronClaude` and its head branch is that child worktree's own branch, pushed by the person beforehand (review F-08: pr-submit requires the local branch name to equal the PR head exactly, `src/superclaude/pr_submit/fsm.py:548`). Pass: the launch's `prompt.outcome` is `journaled` or `handed-to-terminal` (`[CLI]` line 29); the tab shows the skill loaded; the run's output directory holds a run-log with at least one Wave 1 or Wave 8 poll event and no HALT; the PR gains no commit, comment or thread change. Whether several poll iterations occur on a PR the review App has already reviewed is UNVERIFIED, so use a PR the App has not yet reviewed when a long wait must be shown. The run ends on L1's "fix these? y/n" proposal (`SKILL.md:272`), which the person answers "n". Until the check passes, only the person-typed route is used.
- **Risk**: Low. Additive; it costs one scratch PR.

### Change 7: Readiness before the run (INV-023 gate G7; INV-009; CR-01 setup)
- **Source**: INV-009 (`invariant-probe.md:30`); `commands/pr-submit.md:28-30` (STOPs on head mismatch and CI-wait preflight); `HWW:223` ("Monitored runs require the review App, matching PR head checkout/commit and CI-wait prerequisites"); `CR-01:24` (children get setup before use).
- **Target**: Base, "Before the run" section (append).
- **Rationale**: A fresh Orca child worktree lacks `.claude/` copies, the Python environment and the code-graph index until its setup succeeds (`CR-01:24`); pr-submit's preflight imports `superclaude.pr_submit.ci`.
- **Integration point**: One bullet: the child worktree's setup has succeeded, `gh` is authenticated, and the review App is installed on the fork before a run starts; otherwise pr-submit STOPs at preflight.
- **Risk**: Low. Additive.

### Change 8: Two fix cycles, then the person decides (fixed constraint K3)
- **Source**: K3 (commit `80f934de`, PR #343); `commands/pr-submit.md:47` (`--max-rounds` default 2, hard cap 5); `SKILL.md:270` (Medium and above are fixed; Low/Nit are report-only); `SKILL.md:276` (HALT at `round_counter >= max_rounds`).
- **Target**: Base, Safety (append).
- **Rationale**: PR #343 did not edit pr-submit (its stat lists no pr-submit file), and pr-submit still accepts up to 5 rounds. The merged rule keeps every run at the 2-cycle cap.
- **Integration point**: Safety bullet: runs use the default `--max-rounds 2` and are never launched with a higher value; at the cap the run ends `terminal_max_rounds` and the open findings go to the person, who decides. Low and Nit findings are reported, never fixed, matching "only blocking findings fail a review". Exception (review F-09): after an Augment decline, the single-shot fallback can add one more fix push for the whole run (`push_count <= max_rounds + 1`, `SKILL.md:275`); whether that counts as a third fix cycle under #343 is UNVERIFIED, so until settled it is reported to the person as a deviation from the 2-cycle rule, not as a pass. Whether #343's "blocking" grade maps exactly onto pr-submit's Medium-and-above routing is also UNVERIFIED (PR #343 did not touch pr-submit).
- **Risk**: Low. Additive.

### Change 9: Fork only; no Orca PR or issue linking (fixed constraint K2)
- **Source**: K2 (`CR-01:45`); `SKILL.md:267` (target repo from origin), `SKILL.md:304` (never an upstream parent).
- **Target**: Base, Safety (append).
- **Integration point**: One bullet: the PR is opened only by pr-submit on origin (`IronbellyOrg/IronClaude`); launches pass no Orca `--pr` / `--issue` linking, because Orca records this project as `github:superclaude-org/superclaude_framework` (`CR-01:45`).
- **Risk**: Low. Additive.

### Change 10: "Attended" means in-session; (b) is deferred, not rejected (from Variant 2; X-001)
- **Source**: Variant 2, Strongest case (V2:9); X-001 to V2 (95%, unanimous); `SKILL.md:43-45`, `SKILL.md:82-84`; `refs/state-machine.md:170-172` (no interactive confirmation before a push); `CAPS:161`; `orca-ide orchestration worker-start --help` lines 42-44; `[CLI]` lines 47, 63.
- **Target**: Base, "Why a third option" (replace V3:8) and Implementation cost (append the reopening conditions).
- **Rationale**: The base's V3:8 repeats the headless/unattended conflation (Correctness 3, NOT MET). The re-check requested by the team lead: pr-submit defines "attended, in-session" as "closing the session loses it ... never from detachment" (`SKILL.md:43-45`) and forbids handing side effects to "a background shell, detached loop, or subagent" (`SKILL.md:82-84`); push authorization is the monitor-3 arming plus the `push_decision` record, with no confirmation step (`refs/state-machine.md:170-172`). At `--monitor 2` or `3` nothing requires a person to watch; at `--monitor 1` the run ends on a "fix these? y/n" proposal to the person (`SKILL.md:272`), which is why `SPEC:56` refuses it under `--unattended` (review F-11). A terminal Orca worker is a top-level Claude session (`CAPS:161`; `worker-start --help` line 38) and meets that text; `CAPS:47` shows only that its task arrives on the command line (review F-12). Whether a chat-surface session (`outcome.kind: structured`, `[CLI]` line 47) is a Claude Code session with the Skill and Task tools and long foreground Bash waits is UNVERIFIED, and the same question applies to the base's launched tabs, because both follow the person's Chat UI setting (`[CLI]` line 63; `worker-start --help` line 42). So the "attended" rule does not rule (b) out.
- **Integration point**: Replace V3:8 with the corrected meaning; append to Cost: (b) is deferred until all hold: tracked parallel monitoring is a stated need; D4 lets a brief authorize a worker's push (D4's converged (c′) does not, so under it a monitor-3 worker has no role, `HWW:223`); AC-4.3 passes (`SPEC:276`); the chat-surface question is checked.
- **Risk**: Low. Corrects a term and adds conditions.

### Change 11: Spec corrections that hold whatever D3 decides (from Variant 2's rebuttal; INV-010, INV-011)
- **Source**: R2-V2 #4 and "Overall recommendation" (`debate-transcript.md:662`); INV-010, INV-011; `SPEC:67` (WC-3), `SPEC:137`, `SPEC:71`, `SPEC:340`.
- **Target**: Base, Implementation cost (replace "One sentence in section 4 / D3" with the exact list).
- **Integration point**: (1) the `SPEC:137` row drops "(the worker may use `ask` or `escalation`)", which contradicts WC-3; (2) WC-7 and the `SPEC:137` row cite the top-level rule at `sk/sc-pr-submit-protocol/SKILL.md:47-49`, not `37-39`; (3) the D3 text at `SPEC:340` cites the outward actions at `SKILL.md:267,274` and the attended loop at `SKILL.md:43-45,51-84` (its `189,196` now point at S5 re-review attribution text, and `41-64` only partly covers the loop, which runs 51-80; review F-14); (4) every other pr-submit citation in `SPEC:74` (WC-10) and `SPEC:137` is re-checked against the current file in the same revision.
- **Risk**: Low.

### Change 12: Zero build cost and the command count (from Variant 1)
- **Source**: Variant 1, Implementation cost (V1:21); `SPEC:195-197`.
- **Target**: Base, Implementation cost (append).
- **Rationale**: S-004 and C-009 (V1 = V3, 95-96%).
- **Integration point**: "35, not 36, commands accept `--unattended` (`SPEC:195`); no pr-submit edits; no AC-4.3."
- **Risk**: Low.

### Change 13: Repair the base's factual errors (base weaknesses)
- **Source**: Correctness 1, 4, 5 NOT MET for V3 (`base-selection.md`); DA spot-checks 3 and 4; X-004 (V1 = V2, 97%); X-003 and C-003 (V1 = V3: HALTs end the run with `terminal_halted`, `SKILL.md:268,274`).
- **Target**: Base, Safety V3:11-12 and Reliability V3:17 (replace).
- **Better variant**: Variant 1 (V1:10, HALT text written for the operator in the session holding the run).
- **Fix approach**: V3:11 becomes "every operator HALT (`pr_head_mismatch`, `push_range_mismatch`, `fix_commit_failed`, a `needs_human_decision` finding) ends the run with `terminal_halted`, and its recovery steps stay in that tab for the person (`SKILL.md:268,274,316-318,325`); the round cap ends with `terminal_max_rounds` (`SKILL.md:276`)", dropping the `CAPS:52` readiness claim (review F-10). V3:12 quotes `[G]` line 39 in full, including "and do not monitor completion". V3:17 drops "or the coordinator reads the run-log file later" (X-004): the coordinator does not track completion; the person reads each tab.
- **Risk**: Medium. Modifies existing base claims.

### Change 14: Order of the coordinator's two roles (INV-018)
- **Source**: INV-018 (`invariant-probe.md:39`); `[G]` lines 37 and 39; `[CLI]` lines 27 and 29.
- **Target**: Base, "How a person works day to day" (append).
- **Integration point**: The coordinator first settles its supervised Run (reads every contract, admits or rejects results, releases its workers), then performs the pre-PR steps, then launches the tabs, reports each worktree id, handle and the person's instruction, and does not watch the tabs. "Stops" means it does not monitor them, not that its other unrelated work ends.
- **Risk**: Low.

### Change 15: One gate list that closes INV-023 (review F-17)
- **Source**: INV-023 (`invariant-probe.md:44`); gate requirement `debate-transcript.md:655`.
- **Target**: Base, end of "Before the run" (append a short checklist).
- **Rationale**: INV-023 found the consensus necessary but not sufficient: 7 of 10 gates between "workers finish" and "a monitored loop is running" were not shown to pass. Each gate now has an owner change.
- **Integration point**: Checklist, in order: G1 start authority → Change 3; G2 commits exist, G3 head branch pushed, G4 branch not behind base → Change 4; G5 target repo from origin → passes unchanged (`SKILL.md:267`); G6 checkout equals PR head → Change 2; G7 environment and review App → Change 7; G8 launched prompt runs as a slash command on the person's surface → Change 6; G9 one monitor per PR → Change 5; G10 someone reads the terminal status → accepted risk: the person reads the tab; the coordinator does not track completion by design (INV-003, `[G]` line 39).
- **Risk**: Low. Additive.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base (or for leaving it out) |
|---|---|---|
| C-006, S-006 | V2: run pr-submit as a supervised worker so the coordinator gets `worker_done` and a contract per PR | V2 won C-006 (97%), but every advocate deferred (b) (`debate-transcript.md:665`); under D4's converged (c′) a worker never pushes, so a monitor-3 worker has no role (`HWW:223`, `decisions/D4/option-c.md:3`). Kept only as the deferral conditions in Change 10. |
| C-001, X-001 | V1: "a worker is headless, so it contradicts the command's design" (V1:8) | Withdrawn (R2-V1 #4-5); X-001 went to V2 unanimously. Change 10 records the corrected meaning instead. |
| X-002 | V1: "parallel PR monitoring is rarely needed" (V1:17) | Unsourced and withdrawn (R2-V1 #1). The need is left to the person (`SPEC:343`). |
| C-008 | V2: "Depends on D4 (a) or (c) for any push" (V2:24) | WRONG (DA spot-check 6; `decisions/D4/option-c.md:3`). Change 4 states the true D4 coupling (pre-PR steps). |
| C-005, A-006 | V1: the coordinator runs the loop in its own session | Kept as the first carrier but gated (Change 2): under K4/K5 the run's checkout is the PR's child worktree, pr-submit has no worktree argument (`commands/pr-submit.md:8`, `SKILL.md:268`), and whether the coordinator's session can stand there for the whole loop is UNVERIFIED (also in `GO-RP:35-36`). Until a check passes, the fallback is a session opened in the child. This is a judgment, not a debate result; the debate had kept the coordinator as a carrier with "friction" (R2-V1 #16). |
| X-004 | V3 (base): "the coordinator reads the run-log file later" (V3:17) | Removed by Change 13: the handoff route says "do not monitor completion" (`[G]` line 39), conceded R1-V3 Concession 1. |
| INV-015 | Probe: an upper bound on the number of parallel tabs | No number is set, because none is evidenced. The bound is the PRs the person names (Change 1); rate limits stay pr-submit's own backoff (`SKILL.md:324`). |
| INV-004 (LOW) | Probe: record the person's authority inside the tab or run-log | Accepted risk: the instruction is recorded in the coordinator's launch report (Change 3); the launch prompt carries only the slash command, because extra prompt text could stop it running as a slash command (UNVERIFIED either way). |
| INV-005, INV-013 (LOW) | Probe: coordinator context and the real length of its hold under (a) | Not needed: under Change 2 the coordinator never holds the loop. |
| C-012 | V2: PR results as worker reports | Not adopted: the person reads each tab (Change 13); the coordinator reports only launch handles (Change 14). |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1 | Medium | Position reads as (c)-first again; default unclear | Revert to base Position |
| 2 | High | Conflicts with git-ownership row 1 (`GO-BS:172`) until the coordinator check passes or row 1 is amended; if CR-01's PR-head wording is not fixed, child and parent fight over one branch | Restore V1's "coordinator or person" wording, reopen INV-001 |
| 3 | Low | A run starts without the person's request | Remove the bullet (reopens INV-006, HIGH) |
| 4 | Medium | Run reaches Wave 0 with no pushed branch, or HALTs `pr_head_mismatch` after a rebase | Remove the section (reopens INV-017 and INV-007) |
| 5 | Low | Two monitors on one PR, or a deleted run-log | Remove the bullets (reopens INV-012, INV-002) |
| 6 | Low | The launched route is enabled without proof | Remove the check; launched route stays disabled |
| 7 | Low | Run STOPs at preflight in a fresh child | Remove the bullet |
| 8 | Low | A run exceeds the 2-cycle cap | Remove the bullet |
| 9 | Low | Orca links the worktree to the upstream project id | Remove the bullet |
| 10 | Low | (b) read as rejected, or "attended" misread again | Revert to V3:8 |
| 11 | Low | Spec keeps a WC-3 contradiction and stale citations | Drop the list |
| 12 | Low | None (count only) | Drop the sentence |
| 13 | Medium | Base keeps three factual errors | Revert to V3:11-12, V3:17 |
| 14 | Low | Coordinator launches tabs while its Run still has reclaimable workers | Remove the bullet |
| 15 | Low | INV-023 closed only piecemeal | Remove the checklist |

## Review Status
- [x] Auto-approved (default; the run is non-interactive)
- [ ] User-approved (--interactive)
- Approved by: auto, after analytical review
- Review cycle 1: FAIL, 1 CRITICAL, 8 IMPORTANT, 8 MINOR (`refactor-plan-review.md`). All 17 findings applied in this revision: F-01, F-02, F-15 → Change 2; F-03, F-04 → Change 1; F-05, F-06 → Change 5; F-07, F-13 → Change 4; F-08 → Change 6; F-09 → Change 8; F-10 → Change 13; F-11, F-12 → Change 10; F-14 → Change 11; F-16 → Overview citation key; F-17 → new Change 15.
- Review cycle 2: PASS (`refactor-plan-review.md`, section "Cycle 2"): all 17 findings fixed; 5 new MINOR notes (N-01 to N-05). Under the PR #343 rule, minor findings are notes and trigger no fix pass, so the plan is not revised again; the notes are carried into `merge-log.md` as known minor wording issues.
- Approval timestamp: 2026-11-02 (after review cycle 2)
