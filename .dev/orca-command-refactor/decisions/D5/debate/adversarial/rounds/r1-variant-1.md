# D5 Round 1: Variant 1 advocate (option a, keep nesting depth 1)

Citation key: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `V1:N` / `V2:N` = the variant files; `DA` = `diff-analysis.md`. All citations re-read 2026-11-02.

## Position summary
Keep depth 1. Nothing the spec builds uses a deeper setting, raising it widens a machine-wide bound for every Orca run, and the one real benefit claimed for raising it (Orca records for a command's internal fan-out) cannot be reached by depth alone without breaking SA-2 (`SPEC:170`). Revisit only if the P0 smoke runs (`SPEC:181`) show coordinator-side splitting is not enough.

## Steelman
Variant 2's strongest point is that option (a) leaves a real hole. Heavy fan-out that lives inside one command run, such as troubleshoot Tier 2 at "+4-15 min", is not an Orca Task: it has no Dispatch, no independent retry, and it holds the worker session past the heartbeat cadence, a gap the spec "accepted, not required away" (`SPEC:74`). Orca keeps per-unit records only for workers the coordinator starts (`SPEC:42`, `CAPS:158`), and the coordinator cannot lift that fan-out out of the command because it is decided inside the command's own logic (DA X-002). Depth 2 is the only Orca mechanism that could ever put those sub-units under Orca supervision, and the setting itself is one toggle (`CAPS:99`). The steelman is strongest in its narrow form from DA A-002: a worker's top-level session, not the command, could start sub-workers under its brief. That leaves SA-2 intact and sidesteps R2-R4, because WC-8 binds commands only (`SPEC:72`).

## Strengths claimed
1. **Tightest bound on fan-out, with Orca's own blessing (safety).** At depth 1 "a coordinator dispatches workers and those workers may not dispatch further" (`CAPS:97`); Orca's refusal advice is "Do the work in this terminal instead of dispatching a sub-worker" (`CAPS:99`); a malformed value "falls back to the default rather than disabling the fence" and a new Run does not reset depth (`CAPS:100-101`). Depth 1 is the default Orca ships, not a local restriction.
2. **The setting is machine-wide (safety, day to day).** It lives in the only profile, `local-default` (`CAPS:98`), and `worker-start` has no depth flag (`CAPS:135`). Raising it for IronClaude raises it for every Orca run on the machine, including runs unrelated to this spec. Both variants agree (DA A-007).
3. **Nothing in the spec needs it (reliability, cost).** WC-8 forbids commands from calling `worker-start`, `dispatch` or `task-create` (`SPEC:72`); SA-2 forbids any Orca call in a command (`SPEC:170`); non-goal 2 states "Nesting depth stays 1 unless the user decides otherwise" (`SPEC:315`). No phase uses depth 2, which Variant 2 itself concedes (`V2:22`).
4. **The record-keeping need is met another way.** Per-unit Task, liveness and retry come from the coordinator splitting work into Tasks, for example N `/sc:troubleshoot` workers then one `/sc:adversarial` merge, governed by the fan-in rule (`SPEC:42`, `SPEC:87`). Orca's provenance line itself names this route: "the fan-out must be Orca workers from the coordinator, not Agent-tool subagents inside one worker" (`CAPS:158`; DA X-001).
5. **Depth alone fixes only R1.** R2 (standalone use breaks without Orca), R3 (`worker_done` only from the dispatched pane), R4 (platform executable name) and R5 (a second orchestrator below the coordinator) all remain (`SPEC:37-40`). Variant 2 agrees on R2-R4 (`V2:16`) and omits R5.
6. **Evidence-gated, reversible path (cost).** Option (a) costs nothing now and keeps a named trigger to revisit: the P0 live smoke runs (`SPEC:181`), which exist to test the decision "before anything is built on it" (DA U-001).

## Weaknesses identified
1. **Variant 2's benefit is unreachable under its own concessions.** It claims depth 2 "would give each sub-unit its own Task and Dispatch" (`V2:8`), but the fan-out it names (troubleshoot Tier 2) happens inside the command. Only the command could start those sub-workers, which needs Orca calls, which SA-2 and non-goal 1 forbid (`SPEC:170`, `SPEC:314`) and which Variant 2 admits "No phase of the spec uses" (`V2:22`). DA X-003 records the unreconciled contradiction.
2. **The heartbeat gap moves, it does not disappear.** A parent worker waiting on its own sub-workers blocks in `check --wait` or `ask`, and heartbeats are skipped while blocked there (`CAPS:162`). The WC-10 gap (`SPEC:74`) shifts from the subagent fan-out to the parent's wait (DA C-004).
3. **The provenance rule is misread.** `CAPS:158` is conditional ("when Orca orchestration provenance was requested") and its consequence routes fan-out to the coordinator, not to depth 2 (DA X-001, spot-check 5 OVERSTATED).
4. **The narrow A-002 route still fails on R5 and on duties.** A worker session that starts sub-workers becomes a second orchestrator below the coordinator, the conflict the inventories already avoid by marking orchestrating commands coordinator-only (`SPEC:40`). It also inherits coordinator duties: one release-or-retain decision per settled worker and no ending its turn while any sub-worker is `reclaimable` (`CAPS:107`, `CAPS:113`), plus the three-failure circuit breaker per Task (`CAPS:116`). And it cannot reach fan-out decided inside a command, so it buys nothing the coordinator cannot already plan as Tasks.
5. **More operator load.** More workers, Tasks and terminals to release per run (`V2:19`, `CAPS:113`).

## Concessions
1. **"Fence" overstated as binary.** Raising depth widens the bound rather than removing it: the refusal still fires at the new maximum (`CAPS:99`, "(max ${maxDepth})"). The safety cost of (b) is a larger bound (workers of workers, width multiplying per level), not an unfenced Orca (DA A-001). Variant 1's text implied the stronger reading.
2. **`CAPS:155` overstated.** The source says the depth limit does not count Agent-tool subagents and marks "UNVERIFIED that Orca never limits them". Variant 1 dropped that caveat (DA spot-check 4). The point still holds for the decision, since depth does not touch Agent-tool subagents under either option.
3. **Variant 2 is right that a gap exists** (DA X-002). For fan-out that cannot be lifted out of one command run, option (a) gives no Orca Task, Dispatch or independent retry, and Variant 1's "nothing in the spec needs depth 2" (`V1:12`) did not name what (a) gives up. My position is that depth 2 cannot close that gap within SA-2, not that the gap is absent.
4. **Variant 1 missed the worker-session route (A-002)** and the indirect `task-create` route (A-003). Both are answered above, but neither was in the original.
5. **Reversibility is not fully known.** What happens to running nested workers if the value is lowered again is UNVERIFIED (DA C-008). This favours not raising it speculatively, but the "cheap to revisit" claim is one-directional.
6. **Variant 2 locates (b)'s cost better** (DA U-006): the setting is trivial, the command rewrite is the real cost.

## Shared assumption responses

| A-NNN | Response | Reason |
|---|---|---|
| A-001 | ACCEPT | The fence moves, not vanishes (`CAPS:99`, `CAPS:100`). The bound still grows from one generation of workers to workers of workers on a machine-wide setting (`CAPS:98`), so (b) remains the looser safety posture. |
| A-002 | QUALIFY | The route is real and Variant 1 missed it. It avoids SA-2 and R2-R4 but keeps R5 (`SPEC:40`), the parent's heartbeat gap (`CAPS:162`), release and circuit-breaker duties (`CAPS:113`, `CAPS:116`), and it cannot reach fan-out decided inside a command. The only fan-out it can reach is fan-out the brief can plan, which the coordinator can already plan as Tasks (`SPEC:42`). |
| A-003 | QUALIFY | Correct that depth is not the only control: whether a depth-1 worker may `task-create` is UNVERIFIED (`CAPS:103`), and WC-8 forbids it by contract (`SPEC:72`). This argues for keeping the contract rule (and checking `task-create` in P0), not for raising depth, which would add a direct route on top of the indirect one. |
| A-004 | ACCEPT | Supported by `CAPS:98` (only profile) and no depth flag on `worker-start` (`CAPS:135`); absence of an override is inferred, not proven. |
| A-005 | QUALIFY | `CAPS:155` marks "Orca never limits them" UNVERIFIED; Variant 1 should have kept that caveat. It does not change D5: the depth setting governs Orca sub-workers only, so any limit on Agent-tool subagents would apply equally under (a) and (b). |
| A-006 | QUALIFY | Raising is one desktop setting (`CAPS:99`), but lowering it with nested workers already running is UNVERIFIED. That asymmetry favours raising only on evidence (P0, `SPEC:181`), not speculatively. |
| A-007 | ACCEPT | Both variants state it; a profile-wide setting (`CAPS:98`) affects runs outside this spec. |

## Per-point positions

| ID | Superior approach | Reason |
|---|---|---|
| S-001 | V2 | Its leading "Strongest case" section states what (a) gives up; V1 had no such section. |
| S-002 | V1 | V1 anchors the option in the spec's recommendation (`SPEC:352`); V2 argues for a setting whose main use it calls rejected. |
| S-003 | V1 | V1 names an evidence-gated revisit trigger (`SPEC:181`); V2 states no condition for choosing (b). |
| S-004 | V1 | V1 cites R5 (`SPEC:40`), the reason that also defeats the A-002 worker-session route. |
| S-005 | equal | Size and citation style do not decide the question. |
| C-001 | V1 | Depth 1 is the tighter bound; both overstated "removes" (A-001), but the widened bound still counts against (b). |
| C-002 | equal | Same conclusion; V1 adds the direct profile-file citation. |
| C-003 | V1 | Coordinator splitting yields per-unit Tasks today (`SPEC:42`); V2's sub-unit Tasks need commands calling Orca (`SPEC:170`). |
| C-004 | V2 | V2 surfaces the WC-10 gap, though its remedy only moves the gap to the parent (`CAPS:162`). |
| C-005 | V1 | V1 includes R5; both agree depth fixes only R1. |
| C-006 | equal | Same conclusion via R2 and SA-2. |
| C-007 | V1 | V2's own cost analysis (command rewrite, `V2:22`) confirms (a) is the cheaper option. |
| C-008 | V1 | V1 gives a revisit path; neither checked lowering with running nested workers. |
| C-009 | V1 | (a) adds no workers, Tasks or terminals to release; V2 concedes (b) does (`CAPS:113`). |
| C-010 | V1 | `CAPS:158` routes Orca-tracked fan-out to the coordinator, matching V1. |
| C-011 | equal | V1 overstated `CAPS:155`; V2's "invisible" ignores UI child rows (`CAPS:157`). |
| X-001 | V1 | The cited provenance line concludes coordinator-side fan-out, not depth 2. |
| X-002 | V2 | The gap for un-liftable in-command fan-out is real; depth 2 cannot close it within SA-2, but V2 named it. |
| X-003 | V1 | V1 is internally consistent; V2's benefit claim conflicts with "No phase of the spec uses it". |
| A-002 | V1 | The worker-session route still hits R5, the parent heartbeat gap and coordinator duties, and adds nothing coordinator Tasks cannot do. |
| A-003 | V1 | The indirect route is closed by contract (WC-8) under (a); raising depth adds a direct route. |
