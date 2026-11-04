# Recommendation D5: whether to raise Orca's nesting depth

Status: COMPLETE (2026-11-02). The `/sc:adversarial` debate finished all five steps; the spec is not edited.
Repo root: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs. Paths are repo-relative unless absolute.

## 1. Recommended option and how it compares with the spec
**Keep Orca's nesting depth at 1 (option a).** This **agrees with** the spec's current recommendation (`.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:352,354`, cited `SPEC:N`). The choice is unchanged; the reasons and the D5 text are not:
- The spec's question and option (b) describe the wrong thing. `SPEC:350` asks about raising depth "so commands could start their own Orca workers", and `SPEC:353` says a raise would "break R1's protection against runaway fan-out". Both advocates agreed that no setting lets commands call Orca (the standalone, ownership and executable-name reasons R2-R4 and the second-orchestrator reason R5 at `SPEC:37-40` still apply), and Orca's refusal fires at whatever maximum is set (`.dev/orca-command-refactor/inventory/orca-capabilities.md:99-100`, cited `CAPS:N`). The only real use of a raise would be a worker's own top-level session starting sub-workers.
- Option (a) has a precondition the spec never states: the coordinator must be a session the person opened (depth 0). A coordinator that was itself started with `worker-start` is depth 1, and at a maximum of 1 its own worker starts would be refused (presumed); a new Run does not reset depth (`CAPS:97,101,103`).
- The debate's headline reason, "depth 1 is a mechanical backstop that stops workers starting Orca work", is not demonstrated: which Orca calls check the depth was never traced (`CAPS:103`), and the worker's own session is bound by no contract rule (`SPEC:72` names the command as owner of WC-8; `SPEC:170` binds command, skill and agent files). The merged recommendation adds a contract rule (WC-13), a coordinator rule and three checks instead of relying on the presumed refusal.

Merged position: `.dev/orca-command-refactor/decisions/D5/debate/adversarial/merged-output.md`. Plan: `.dev/orca-command-refactor/decisions/D5/debate/adversarial/refactor-plan.md`.

## 2. Debate confidence and the strongest argument that lost
**Confidence: high on the choice, medium on the stated safeguards until the Phase 0 trace runs.**
- Scores: keep depth 1 scored 0.827, raise depth 0.694, a margin of 0.133 with no tiebreaker needed (`.dev/orca-command-refactor/decisions/D5/debate/adversarial/base-selection.md:189-195`). The two variants tie on the mechanical metrics (0.921 each); the whole margin is correctness and clarity (`base-selection.md:21,197`).
- Points: keep-depth-1 won 12 of 21 debated points, raise-depth won 3, 5 were equal and 1 unresolved; agreement 95.2% after two rounds (`debate/adversarial/debate-transcript.md:361-365`). Both advocates ended recommending keep-depth-1, and the raise-depth advocate withdrew its option (`debate-transcript.md:319`).
- Status was BLOCKED_BY_INVARIANTS: four high-severity gaps in the reasons given for keeping depth 1, not in the choice itself (`debate-transcript.md:404-410`; `debate/adversarial/invariant-probe.md:52`). The plan gives each a change; what the changes cannot close is listed as two open entries that wait for Phase 0 to read Orca's code (AR-1, AR-2) and one accepted risk, the person changing the setting (AR-3) (`refactor-plan.md`, "Invariant Coverage").

**Strongest argument that lost:** a worker sometimes learns mid-run that the work should be split. Under a raise to exactly 2, scoped to a worker's own session and only when its brief says `Sub-workers: allowed, max N`, that worker could start the pieces itself as Orca-tracked workers, each with its own record, liveness and retry, without any command calling Orca. That avoids the standalone, ownership and executable-name problems (R2-R4), and a parent waiting on them stays live (`CAPS:64`; round-2 concession at `debate-transcript.md:184`). It lost because a worker's brief carries one exact command line (`SPEC:79`), so there is nothing for a worker session to split; the saving is one coordinator round trip; and the cost is a second orchestrator sharing the coordinator's inbox and a looser limit for every Orca run on the machine (`debate-transcript.md:258-261,278,319`).

## 3. What this means in practice
**What a person sees and does differently**
- Nothing changes in Orca's settings. The "Nested worker depth" setting stays at 1.
- You start the coordinator yourself: open a Claude session in the feature's main worktree in Orca and give it the plan. Do not ask another Orca agent to start the coordinator for you. A coordinator started that way would most likely be unable to start any workers (Orca's refusal is presumed, not yet traced); Orca would answer each attempt with "Sub-worker dispatch is not permitted at depth ... Complete this task yourself." (`CAPS:99`).
- Workers never start other workers. When a worker finds that its job should be split, it says so in its completion message, and the coordinator starts the extra workers. You may see one extra round of waiting while the coordinator reads the result and plans.
- A long single-command job (for example a deep troubleshooting run) shows as one worker. Orca cannot show progress for the helpers working inside it, so a quiet stretch with no heartbeat is normal, as it already is today (`SPEC:74`).
- Each rollout phase's checks also read the depth setting. If you have raised it, for this project or another one, the check stops and asks you to confirm.
- If the coordinator finds a ready Orca task it did not create, it does not start it; it tells you about it instead.

**What could go wrong**
- Orca's refusal may not cover every way a worker could start another agent. Nobody has yet read the part of Orca's code that enforces it. Until Phase 0 does, the main protection is a written rule the worker follows, and a breach is caught only afterwards, when the check reads the worker's transcript.
- The setting is shared by every Orca run on the machine. If you raise it for another project, it also applies to IronClaude work until the next phase check notices.
- If the coordinator is started the wrong way, every worker start is refused (the likely case), or, if Orca's refusal turns out not to be enforced, workers quietly run one level deeper than intended.

**What it costs to change later**
- Raising the setting is one change in Orca's desktop app (`CAPS:99`). It does nothing useful on its own: IronClaude would first need a new kind of worker brief that allows a worker to split its own work, rules and tests for it, and a check of where the sub-workers' messages land.
- Lowering it again while deeper workers are running has not been verified, so raising is easy but undoing it may not be. That is why the recommendation says to raise it only after a real run shows the need.
- Keeping depth 1 costs no command changes. It adds to the spec one worker rule, one coordinator rule, a Phase 0 reading of Orca's code, a depth-setting check run at every phase, one item in the live worker check, a wider file scan, and wording fixes.

## 4. Exact spec wording change
Replace `SPEC:350-354` (the whole D5 entry in section 9) with this text, copied from `debate/adversarial/merged-output.md:220-226` (section M10):

> **D5. Should Orca's nesting depth be raised so that a worker could start its own Orca workers?**
> - Today the maximum is 1: the coordinator (depth 0) starts workers (depth 1), and Orca is presumed to refuse `worker-start` and `dispatch` from a worker; which calls check the depth, and whether a worker may `task-create`, is not traced (`CAPS:97-99`, `CAPS:103`; AC-0.7 traces it). The value is per Orca profile and applies to every run under that profile; `local-default` is the only profile on this machine (`CAPS:98`). Raising it is one desktop setting (`CAPS:99`); lowering it again while deeper workers are running is UNVERIFIED.
> - Depth cannot reach a command's Agent-tool fan-out, and commands still may not call Orca (SA-2, WC-8), so no setting revives section 1.3. The only use of a raise would be a worker's top-level session starting sub-workers.
> - (a) **Keep depth 1 (recommended).** Fan-out stays inside a command (Agent-tool subagents) or is split into Tasks by the coordinator (sections 1.3 and 2.3). It requires the coordinator to be a root session: one the person opens in the feature's top-level worktree, never one started with `worker-start`, because at depth 1 its own `worker-start` calls would be refused (presumed, `CAPS:103`) and a new Run does not reset depth (`CAPS:97`, `CAPS:101`). Child worktrees (CR-01) are placement chosen by that coordinator, not nested workers. What (a) gives up: Orca Task, liveness and retry records for fan-out that stays inside one command run (WC-10's heartbeat gap stays accepted, under either option), and one extra coordinator round trip when a worker's result shows work that could not be planned before dispatch.
> - (b) **Raise to exactly 2, scoped.** A worker's top-level session may start sub-workers only when its brief says `Sub-workers: allowed, max N`; no command file changes. Orca's fence stays, one generation wider: the refusal fires at the new maximum and bad values fall back to 1 (`CAPS:99-100`). Costs: a composite brief type this spec does not define (the brief carries one command line, section 2.3); the parent becomes a second orchestrator (R5) running the full coordinator loop (`CAPS:92`, `CAPS:107`, `CAPS:113`, `CAPS:116`); sub-worker questions would probably go to the coordinator's Run mailbox, not the parent (`CAPS:59`, `CAPS:92`; UNVERIFIED); WC-13 would have to be relaxed for briefs carrying the `Sub-workers:` line; the brief line restrains only IronClaude workers while the value applies to every run under the profile. It saves one coordinator wake, read and `task-create` per run-time split.
> - Revisit only when both hold: a composite brief type is defined in this spec, and the coordinator's run notes (section 2.3) record a real run whose split was knowable only at run time and whose extra round trip was material. Before any raise: AC-0.7's trace is done, and the mailbox that receives a depth-2 worker's questions and `worker_done` is established.
> - Recommendation: (a). The guard on worker fan-out is WC-13 (the worker session never starts Orca work) with the 7.2 step 5 transcript check, plus Orca's refusal for each call AC-0.7 confirms; depth 1 alone is not proof that a worker cannot start Orca work.

The D5 text names three new spec items, so these edits go in the same revision. Their exact text and command blocks are in `merged-output.md:109-213` (section M9); in short:
1. E4 (`SPEC:27`): add that Orca never limiting subagents is UNVERIFIED.
2. R1 (`SPEC:36`): replace "The two designs exclude each other unless the user raises the depth setting." with "Raising the depth would not make this design viable: R2-R5 still apply, and depth cannot reach a command's Agent-tool fan-out (D5)."
3. Non-goal 2 (`SPEC:315`): add that the coordinator is a session the person opened, never one started by `worker-start`.
4. New requirement WC-13 in section 2.2: the worker's own session never calls `worker-start`, `dispatch`, `task-create`, low-level dispatch, `worktree create --agent` or `agent launch`; it is added to the contract-file list (`SPEC:58`).
5. Section 2.3: the coordinator starts only Tasks it created, and records in its run notes each follow-up Task caused by work that could not be planned before dispatch.
6. Section 7.1: AC-C1 scans seven directories, ignoring case; new common check AC-C6 reads the depth value at every phase.
7. Section 7.2 step 5: the transcript shows no Orca fan-out call by the worker session.
8. Section 7.3: new Phase 0 check AC-0.7, a read-only trace of which Orca calls check depth and what depth a person-opened session gets.
9. Section 7.4: traceability row for WC-13.
10. UNVERIFIED item 5 (`SPEC:387`): resolved by AC-0.7.

None of these edits is applied yet: the spec is unchanged, as instructed. CR-01 is queued for the same consolidated revision (CR-01:3).

## 5. Interactions with D1-D4, git ownership and CR-01
The D1-D4 debates were still running when this was written; their outcomes are UNVERIFIED here, so each line below is written against the spec's current recommendation for that decision and says whether the other option changes anything.
- **D1, how a command knows it runs without a person** (`SPEC:328-331`, recommended: the `--unattended` flag). No interaction. Neither D1 option has a command call Orca (option (b) reads an environment variable, `SPEC:330`). WC-13 is a rule on the worker's session, separate from the command's unattended mode.
- **D2, who may give a Ruling when `/sc:implement` halts** (`SPEC:333-337`, recommended: keep the rule). No interaction under either option at depth 1: under D2 (b) the Ruling travels person to coordinator to worker through one `ask` and `reply`. At depth 2 a sub-worker's question would probably land in the coordinator's mailbox, not its parent's (`CAPS:59`; UNVERIFIED), a second relay path D2 (b) does not define. Keeping depth 1 avoids that.
- **D3, whether `/sc:pr-submit` runs as a worker** (`SPEC:339-343`, recommended: coordinator or person only). Under D3 (b), a pr-submit worker keeps its fix work inside its own session; WC-13 forbids it starting Orca workers for fixes. CR-01 gives it its own child worktree (trigger T3, `.dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md:19`).
- **D4, whether a brief may authorize outward actions** (`SPEC:345-348`, recommended: only when the person's own instruction names the action). At depth 1 every worker is started by the coordinator, so every brief and every authorization quoted in it is written by one party. Under a raise, a parent worker would write its sub-workers' briefs, and whether an authorization passes down would need a new rule. Keeping depth 1 avoids that question.
- **Git ownership** (`decisions/git-ownership/`; its `RECOMMENDATION.md` is still a stub, so the final choice is UNVERIFIED; CR-01:34 records that all five options converged on hybrid E: workers commit locally only where granted, one owner pushes, opens PRs and comments). Consistent with depth 1: only the coordinator starts workers, so only it decides which worker may commit and in which worktree. WC-13 does not stop the git owner's own worktree work; it bans only a worker session starting agents or workers.
- **CR-01, feature worktree hierarchy** (fixed constraint). CR-01's "child worktrees" are placement, not nested workers: the coordinator (depth 0) starts a worker in a child with `worker-start --worktree new-child --base-branch <feature branch>` (CR-01:16), and Orca treats worktree lineage and coordination parentage as separate decisions (CR-01:22). Every worker, in the parent or a child worktree, is depth 1, so CR-01 needs no depth change. CR-01 puts the coordinator in the feature's top-level worktree (CR-01:15); with D5's precondition, the person opens that coordinator session there themselves. Worktrees go to Orca's default paths (CR-01:41); nothing in D5 creates one under `.dev/worktrees/`.
- **Upstream never touched** (fixed constraint). D5 involves no GitHub action. Changing the depth setting is a local Orca setting (`CAPS:98-99`).
- **Merged PR #343** (commit `80f934de`: only blocking findings fail a review; at most 2 fix cycles). A command's own review loops stay inside one command run and are capped there. At depth 1, a retry beyond that is a new Task from the coordinator (WC-6, `SPEC:70`), subject to Orca's three-failure circuit breaker (`CAPS:116`), so there are no nested retry chains. Under a raise, a parent worker running sub-workers would need its own cap rule.

## 6. Unverified items
1. Which Orca calls check the nesting depth (`worker-start` and `dispatch` presumed), and whether a depth-1 worker may call `task-create` (`CAPS:103`; `SPEC:387`). A read-only grep on 2026-11-02 found the refusal code named in three installed files, one of them a minified bundle; the per-call check was not traced. Resolve: new AC-0.7.
2. What depth Orca gives a session the person opens (0 presumed from `CAPS:97`). Resolve: AC-0.7.
3. Whether Orca's low-level dispatch, `orca-cli` `worktree create --agent` and `agent launch` are depth-fenced (`CAPS:101,139`). Resolve: AC-0.7.
4. Whether the running Orca app re-reads `nestedWorkerMaxDepth` from the profile file after a change. The file itself reads `"nestedWorkerMaxDepth":1` (command run 2026-11-02).
5. That no per-run depth override exists (inferred, not proven; `debate/adversarial/diff-analysis.md` A-004).
6. Whether lowering the depth again while deeper workers are running is safe.
7. Which mailbox receives a depth-2 worker's questions and completion (sources point to the coordinator's Run mailbox, `CAPS:59,92`). Matters only if D5 is ever revisited.
8. That Orca never limits Agent-tool subagents inside a worker (`CAPS:155`).
9. The final outcomes of D1-D4 and of git ownership (debates still running when this was written).

## 7. Sources
- Debate artifacts, all in `.dev/orca-command-refactor/decisions/D5/debate/adversarial/`: `diff-analysis.md`, `debate-transcript.md`, `rounds/r1-variant-1.md`, `rounds/r1-variant-2.md`, `rounds/r2-variant-1.md`, `rounds/r2-variant-2.md`, `invariant-probe.md`, `scoring/qual-pass-1.md`, `scoring/qual-pass-2.md`, `base-selection.md` (Steps 1-3, completed before the restart and not redone); `refactor-plan.md` (Step 4, completed here and reviewed once by a fresh agent: 3 blocking findings fixed); `merged-output.md` and `merge-log.md` (Step 5, written by a merge-executor agent; 19 of 19 changes applied, validation PASS); `return-contract.yaml` (status `partial`: the debate ended blocked by four high-severity gaps whose remaining parts stay open until Phase 0, and one debated point, C-003, is unresolved).
- Spec: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (`SPEC:N`), read, not edited.
- Orca capabilities inventory: `.dev/orca-command-refactor/inventory/orca-capabilities.md` (`CAPS:N`).
- CR-01: `.dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md`.
- PR #343: commit `80f934de` ("fix(qa): minor findings never fail a review; cap review loops at 2 rounds").
- Commands run on 2026-11-02, all read-only: `grep -rlE 'nested_worker_depth_exceeded|NESTED_WORKER_DEPTH_EXCEEDED_CODE' /opt/Orca/resources/app.asar.unpacked/out/` (3 files); the proposed AC-C6 command (printed `"nestedWorkerMaxDepth":1`); the proposed widened AC-C1 grep (printed nothing).
