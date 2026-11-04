# Adversarial Debate Transcript

## Metadata
- Decision: D5, "Should Orca's nesting depth be raised?" (`.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:350-354`)
- Mode: A (compare existing files), assembled by the debate-orchestrator, 2026-11-02T16:23:15Z. The orchestrator did not argue for either variant.
- Variants: Variant 1 = `variant-1-original.md`, option (a), keep depth 1. Variant 2 = `variant-2-original.md`, option (b), raise depth. The Variant 2 advocate withdrew (b) in Round 2 and backed (a) with recorded conditions (see "Advocates' final recommendations").
- Depth: standard
- Rounds completed: 2 (Round 1 statements, Round 2 rebuttals), plus the Round 2.5 invariant probe (`invariant-probe.md`). Round 3 skipped: depth is standard, so Round 3 does not run.
- Convergence achieved: 95.2% (20 of 21 diff points agreed)
- Convergence threshold: 80%
- Convergence status: **BLOCKED_BY_INVARIANTS** (4 HIGH-severity UNADDRESSED invariants; see Convergence Assessment)
- Focus areas: All
- Advocate count: 2
- Inputs: `diff-analysis.md`, `rounds/r1-variant-1.md`, `rounds/r1-variant-2.md`, `rounds/r2-variant-1.md`, `rounds/r2-variant-2.md`, `invariant-probe.md`
- Layout note: the four round sections below are verbatim copies of the round files, so each copy keeps its own `#`/`##` headings. Each copy is fenced by `<!-- verbatim copy of ... -->` and `<!-- end verbatim copy -->` comments, and a line-by-line `diff` against the source file reported no differences.

## Round 1: Advocate Statements

### Variant 1 Advocate (option a, keep depth 1)
<!-- verbatim copy of rounds/r1-variant-1.md -->
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
<!-- end verbatim copy -->

### Variant 2 Advocate (option b, raise depth)
<!-- verbatim copy of rounds/r1-variant-2.md -->
# D5 Round 1: Variant 2 advocate (option b, raise nesting depth)

Citation key: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `INV-A:N` = `.dev/orca-command-refactor/inventory/commands-a.md:N`; `V1:N` / `V2:N` = the variant files; `DA` = `diff-analysis.md`. All cited lines re-read 2026-11-02.

## Position summary
Raise "Nested worker depth" from 1 to exactly 2, and use it only from a worker's top-level session acting on an explicit brief line, never from a command, so WC-8 and SA-2 stay intact (`SPEC:72`, `SPEC:170`). This buys data-dependent fan-out with real Orca records and top-level sub-workers, while the fence still holds at the new maximum (`CAPS:99-100`). My original variant argued for the command-calls-Orca design; I drop that form (see Concessions).

## Steelman
Variant 1's strongest case: depth 1 is Orca's shipped default and a deliberate fence ("1 means a coordinator dispatches workers and those workers may not dispatch further", `CAPS:97`); a malformed value cannot disable it (`CAPS:100`); a new Run does not reset it (`CAPS:101`). The setting is machine-wide, living in the only profile (`CAPS:98`), so any raise reaches every Orca run here. The spec is already built to need nothing deeper: commands never call Orca (WC-8, `SPEC:72`; SA-2, `SPEC:170`), and per-unit Task records come from the coordinator splitting work into Tasks with a fan-in rule (`SPEC:42`, `SPEC:87`). Four of the five rejection reasons for the command-calls-Orca design (R2-R5, `SPEC:37-40`) do not depend on depth at all. Cost is zero, and V1 gives an evidence gate for revisiting: raise only if P0 smoke runs show coordinator splitting is inadequate (`V1:19`, `SPEC:181`; DA U-001), the best single idea in either variant.

## Strengths claimed
1. **The worker-session route avoids R2, R3 and R4 (DA A-002).** WC-8 binds commands: "A command never calls `worker-start`, `dispatch` or `task-create`" (`SPEC:72`). SA-2 binds "command, skill or agent" files (`SPEC:170`). A worker's top-level session is neither; it already runs Orca verbs from its preamble (`SPEC:58`, `SPEC:67`). R2 (standalone breaks, `SPEC:37`) cannot fire, because only a session that received a preamble is a worker (`CAPS:148`); a person's plain session never sees the brief. R3 (`SPEC:38`) does not arise: the parent still sends its own `worker_done` from its own pane (`CAPS:150`). R4 (`SPEC:39`) does not arise: the guide says "Use the executable you used to run `skills get` for the entire run" (`CAPS:145`), so no command text carries platform logic. No command file changes at all.
2. **It covers fan-out the coordinator cannot plan up front (DA X-002).** Dependents are created only after inputs settle and are read (`SPEC:85`), so every split discovered at run time costs a full worker-done, read, re-plan, re-dispatch cycle through the coordinator. A depth-2 worker that finds, say, four independent hypotheses can dispatch four sub-workers itself and fan them in, with the same Task/Dispatch/retry records Orca keeps only for Orca workers (`CAPS:158`, first half; `CAPS:116`).
3. **Sub-workers are top-level sessions; Agent-tool subagents are not.** The command inventory records that nested Agent-tool subagents lose the Agent tool at Claude Code's depth limit and have MCP problems (`INV-A:95`). Top-level-only commands such as `/sc:pr-submit` "can be workers but not subagents of a worker" (`CAPS:161`). At depth 1, a worker that must run several fan-out commands in parallel has no route that keeps their tools; at depth 2 it has one.
4. **The fence moves; it is not removed (DA A-001, C-001).** The refusal names `(max ${maxDepth})` and fires at any maximum (`CAPS:99`); bad values still fall back to 1 (`CAPS:100`); new Runs still do not reset depth (`CAPS:101`); the three-failure circuit breaker still applies per Task (`CAPS:116`). Depth 2 bounds growth at one extra generation.
5. **Waiting on sub-workers is a liveness signal; waiting on subagents is not (DA C-004, corrected).** The guide: heartbeats are skipped "while blocked inside `ask` or `check --wait`; those calls are liveness signals" (`CAPS:64`). A parent in `check --wait` on its sub-workers therefore signals liveness, whereas a session held by Agent-tool fan-out cannot heartbeat at all, the gap WC-10 accepts (`SPEC:74`). UNVERIFIED: that a depth-2 worker's `worker_done` lands in the depth-1 parent's `check` rather than only in the Run mailbox.
6. **Cost is one setting plus one brief rule.** The setting is a desktop toggle (`CAPS:99`). The rule ("sub-workers only when the brief says `Sub-workers: allowed, max N`") lives in the coordinator half of `WORKER-CONTRACT.md` (`SPEC:58`); non-goal 2 already reserves exactly this choice to D5 (`SPEC:315`).

## Weaknesses identified
1. **"Nothing in the spec needs depth 2" is circular** (`V1:12`). The spec was written around depth 1, and it still names what that costs: an accepted heartbeat gap (`SPEC:74`) and the per-unit records the alternative "would have given" (`SPEC:42`).
2. **Task splitting covers only plannable fan-out** (DA X-002). V1's example, N troubleshoot workers then one merge (`V1:16`, `SPEC:87`), presumes the coordinator knows N and the split before dispatch.
3. **V1's revisit trigger cannot fire on the case that matters.** The P0 smoke runs are three single-command workers (`SPEC:181`); none has a composite brief whose split appears at run time, so "coordinator splitting is inadequate" is never tested.
4. **V1 drops a caveat.** "Agent-tool subagents are not counted by the fence" (`V1:12`) omits the source's "UNVERIFIED that Orca never limits them" (`CAPS:155`; DA spot-check 4).
5. **V1 treats depth 1 as the binding control** (DA A-003). Whether a depth-1 worker may `task-create` is UNVERIFIED (`CAPS:103`); if it may, worker-driven fan-out is already possible at depth 1 and is stopped only by the WC-8 contract text, the same kind of control my rule uses.

## Concessions
1. **My provenance claim was overstated** (DA X-001, spot-check 5). The rule at `CAPS:158` applies only "when Orca orchestration provenance was requested", and the same line concludes "the fan-out must be Orca workers from the coordinator". V1 is right on this point.
2. **Depth 2 does not reach inside a command.** Troubleshoot Tier 2's Agent-tool fan-out (`SPEC:74`) stays Agent-tool unless the command is rewritten, which SA-2 and non-goal 1 forbid (`SPEC:170`, `SPEC:314`). My original "each sub-unit its own Task" (`V2:8`) therefore contradicted `V2:16` and `V2:22` (DA X-003). The real benefit is at the worker-session level only.
3. **R5 still applies** (`SPEC:40`; DA U-002). A parent worker dispatching sub-workers is a second orchestrator. The brief rule limits it, but does not remove it.
4. **The setting is machine-wide** (`CAPS:98`; DA A-004, A-007): every Orca run here gets depth 2.
5. **More to clean up day to day.** Each sub-worker owes a release decision before its parent's turn ends (`CAPS:107`, `CAPS:113`), and the person sees more terminals and Tasks.
6. **V1's evidence gate is better timing.** The fair outcome is (b) as a defined, scoped option that the user switches on when a composite brief actually needs it, not a raise before any P0 evidence.

## Shared assumption responses
| A-NNN | Response | Reason |
|---|---|---|
| A-001 | REJECT | The refusal fires at any configured maximum (`CAPS:99`) and bad values fall back to 1 (`CAPS:100`); a raise widens the bound to one extra generation, it does not disable the fence. My own "Removes Orca's fence" (`V2:13`) was wrong. |
| A-002 | REJECT | A worker's top-level session is not a command, so WC-8 (`SPEC:72`) and SA-2 (`SPEC:170`) do not bind it; that route avoids R2-R4 (Strength 1). R5 and machine-wide scope still apply. |
| A-003 | QUALIFY | Depth is a mechanical control only where enforced, and the enforcing call sites and `task-create` at depth 1 are UNVERIFIED (`CAPS:103`). Contract rules (WC-8, the brief) are the real control under either option. |
| A-004 | ACCEPT | Only one profile exists (`CAPS:98`) and `worker-start` has no depth flag (`CAPS:135`); absence of an override is inferred, not proven. |
| A-005 | QUALIFY | Orca's fence does not count them, but this is UNVERIFIED (`CAPS:155`), and Claude Code's own nesting limit does bind them (`INV-A:95`), which is part of the case for top-level sub-workers. |
| A-006 | QUALIFY | The toggle is cheap (`CAPS:99`), but what happens to running depth-2 workers when it is lowered is UNVERIFIED in the sources (DA C-008), and briefs that rely on sub-workers would also need changing. |
| A-007 | ACCEPT | It counts against (b) (`CAPS:98`), though depth 2 is still bounded (A-001). |

## Per-point positions
| ID | Superior approach | Reason |
|---|---|---|
| S-001 | equal | Section order is presentation only. |
| S-002 | V1 | V2 framed itself around the rejected design; this round reframes it to the worker-session route. |
| S-003 | V1 | V1 states when to revisit (`V1:19`); V2 had no condition for choosing (b). |
| S-004 | V1 | V1 includes R5 (`SPEC:40`), which still applies to (b). |
| S-005 | equal | Comparable size and evidence density. |
| C-001 | V1 | Depth 1 is the tighter bound, though a raise moves the fence rather than removing it (`CAPS:99-100`). |
| C-002 | equal | Same conclusion, machine-wide (`CAPS:98`). |
| C-003 | equal | V1 wins for plannable fan-out (`SPEC:42`); V2 wins for splits found at run time via the worker session. |
| C-004 | V2 | A parent in `check --wait` is a liveness signal (`CAPS:64`); Agent-tool fan-out is not (`SPEC:74`). Delivery to the parent is UNVERIFIED. |
| C-005 | V1 | V1 lists R5; both are right that depth alone does not fix R2-R5 for commands. |
| C-006 | equal | Neither option changes standalone use under the worker-session route (`CAPS:148`). |
| C-007 | V1 | (a) costs nothing; (b) costs a setting plus a brief rule, with no command rewrite. |
| C-008 | V1 | V1 gives an evidence-gated revisit; lowering with live nested workers is UNVERIFIED. |
| C-009 | V1 | (b) adds terminals and release decisions (`CAPS:113`). |
| C-010 | V1 | `CAPS:158` points to coordinator fan-out; my provenance claim is withdrawn. |
| C-011 | equal | Both are incomplete; `CAPS:157` shows child rows that are not Tasks. |
| X-001 | V1 | Same as C-010. |
| X-002 | V2 | Coordinator splitting cannot cover splits decided at run time without a full round trip (`SPEC:85`). |
| X-003 | V1 | V2's benefit claim contradicted its own concessions; resolved here by dropping the command route. |
| A-002 | V2 | The worker-session route is real, leaves SA-2/WC-8 intact, and is the only form of (b) worth choosing. |
| A-003 | equal | Enforcement is UNVERIFIED (`CAPS:103`) under both options; contract rules carry the weight. |
<!-- end verbatim copy -->

## Round 2: Rebuttals

### Variant 1 Rebuttal
<!-- verbatim copy of rounds/r2-variant-1.md -->
# D5 Round 2: Variant 1 advocate rebuttal (option a, keep nesting depth 1)

Citation key: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `INV-A:N` / `INV-B:N` = `.dev/orca-command-refactor/inventory/commands-a.md:N` / `commands-b.md:N`; `R1-V1` / `R1-V2` = `rounds/r1-variant-1.md` / `rounds/r1-variant-2.md`; `DA` = `diff-analysis.md`. Every cited line re-read 2026-11-02. First in Round 2.

## Responses to criticisms

| # | Criticism (source) | Response | Concede / hold |
|---|---|---|---|
| 1 | "Nothing in the spec needs depth 2" is circular; the spec names what depth 1 costs (R1-V2 W1; `SPEC:42`, `SPEC:74`). | The phrasing argued from the spec's own design, a fair hit. But neither named cost is recovered by Variant 2's revised route: the `SPEC:74` gap is Agent-tool fan-out inside a command, which V2 concedes depth 2 cannot reach (R1-V2 concession 2); the `SPEC:42` per-unit records already come from coordinator Tasks. What remains is item 2 only. | Partial concede; hold conclusion |
| 2 | Task splitting covers only fan-out the coordinator can plan; a split found at run time costs a full worker-done, read, re-plan, re-dispatch round trip (R1-V2 W2, S2; DA X-002; `SPEC:85`). | The class exists. Its size is small: a brief carries "the exact command line" (`SPEC:79`), so a worker runs one command, and splits inside that command are out of reach (item 1). What depth 2 saves is one coordinator wake and read: each sub-worker still pays the same `worker-start` readiness wait (`CAPS:44-45`), and the fan-in rule's "settled and read" step (`SPEC:85-87`) still has to happen, just in the parent instead. See New evidence 1-2. | Concede the gap; hold that it does not justify the raise |
| 3 | V1's revisit trigger cannot fire: the P0 smoke runs are three single-command workers, none with a run-time split (R1-V2 W3; `SPEC:181`). | Correct. I replace the trigger: revisit D5 when a real coordinator run records a job whose split was knowable only at run time and the extra round trip was material, then choose (b) in the scoped form below, not the section 1.3 form. | Concede; trigger revised |
| 4 | V1 dropped the "UNVERIFIED that Orca never limits them" caveat (R1-V2 W4; DA spot-check 4; `CAPS:155`). | Already conceded in R1-V1 concession 2. Irrelevant to D5: depth governs Orca sub-workers, not Agent-tool subagents, under both options. | Concede |
| 5 | V1 treats depth as the binding control; `task-create` at depth 1 is UNVERIFIED, so contract text is the real control under both options (R1-V2 W5; DA A-003; `CAPS:103`). | Depth is not the only control. But the controls are not symmetric: at depth 1 a direct `worker-start` or `dispatch` from any worker of any Orca run is refused by Orca (presumed call sites, `CAPS:103`); at depth 2 the only restraint on depth-1 workers is V2's brief line, which exists only in IronClaude briefs, while the setting is machine-wide (`CAPS:98`). | Partial concede; hold |
| 6 | A parent in `check --wait` signals liveness, so V1's "the heartbeat gap moves to the parent" is wrong (R1-V2 S5; DA C-004; `CAPS:64`). | Correct: "Skip them while blocked inside `ask` or `check --wait`; those calls are liveness signals" (`CAPS:64`). I withdraw R1-V1 weakness 2. Two caveats stand: whether a depth-2 worker's `worker_done` reaches the parent's `check` is UNVERIFIED (V2's own S5), and the `SPEC:74` in-command gap is untouched. | Concede |
| 7 | At depth 1 a worker that must run several fan-out commands in parallel has no route that keeps their tools; Agent-tool nesting loses tools (R1-V2 S3; `INV-A:95`; `CAPS:161`). | At depth 1 the coordinator starts each such command as its own top-level worker in a parallel wave (`CAPS:86`; `SPEC:87`), so tools are kept. The difference again reduces to run-time splits (item 2). | Hold |
| 8 | V1 missed the worker-session route, which avoids R2-R4 because WC-8 and SA-2 bind commands only (R1-V2 S1; DA A-002; `SPEC:72`, `SPEC:170`). | Conceded in R1-V1 and confirmed: R2 cannot fire without a preamble (`CAPS:148`), R3 does not arise (`CAPS:150`), R4 does not arise (`CAPS:145`). R5 remains, and V2 concedes it (R1-V2 concession 3). | Concede the route; hold on R5 |
| 9 | "Fence" overstated as binary (DA A-001, C-001; R1-V2 S4; `CAPS:99-100`). | Conceded in R1-V1 concession 1. Depth 2 bounds growth at one extra generation; the bound is still looser and machine-wide. | Concede wording; hold ranking |
| 10 | Reversibility is one-directional (DA C-008, A-006). | Agreed; lowering with live nested workers is UNVERIFIED. This favours raising only on evidence. | Concede fact; hold conclusion |
| 11 | V1 never named what (a) gives up (DA S-001, U-005). | Fair. What (a) gives up: Orca records and parent-side fan-in for splits found at run time between commands. | Concede |
| 12 | (b) now costs only a setting plus one brief rule, with no command rewrite (R1-V2 S6), weakening V1's cost argument (C-007). | No command rewrite: conceded. "One brief rule" understates it: see New evidence 1-3 (a new worker role with coordinator duties, outside the one-command brief of `SPEC:79`). | Partial concede |

## Updated assessment of Variant 2

**Steelman.** The revised Variant 2 is a much stronger option than its original. It changes no command file, so SA-2 and WC-8 hold (`SPEC:72`, `SPEC:170`); it avoids R2-R4 (item 8); it keeps a fence at one extra generation (`CAPS:99-100`); a parent waiting in `check --wait` stays live (`CAPS:64`); sub-workers are top-level and keep their tools (`CAPS:161`); and the brief line `Sub-workers: allowed, max N` makes the route opt-in per Task. It also dropped every overreach the diff flagged: provenance (X-001), in-command reach (X-003), R5, machine-wide scope, and timing (R1-V2 concessions 1-6). Its own concession 6 already says the setting should not be raised before evidence.

**Critique.** What is left of the benefit is narrow: Orca-tracked fan-out for splits a worker discovers between commands, saving one coordinator round trip. Against that: (i) the parent becomes a second orchestrator (R5, `SPEC:40`), the role the inventories reserve for the coordinator because "two controllers would compete" (`INV-A:90`; `INV-B:285`); (ii) a worker whose brief lets it plan and dispatch sub-workers is no longer a one-command worker (`SPEC:79`), so the "one brief rule" is really a new worker type with coordinator duties; (iii) the brief line restrains only IronClaude workers, while the raised value applies to every Orca run on the machine (`CAPS:98`); (iv) delivery of a depth-2 `worker_done` to the parent is UNVERIFIED. The two variants now disagree only on timing and form: V2 wants the scoped route defined now, V1 wants it recorded as the form (b) takes if the revised trigger (item 3) ever fires.

## New evidence

1. **The brief is one command line.** The coordinator's brief states "the exact command line including `--unattended`" (`SPEC:79`). A worker that decides its own fan-out needs a brief type the spec does not define, plus contract-file text and tests (P0 already adds `tests/skills/test_worker_contract.py`, `SPEC:181`). This is the real cost of the scoped (b).
2. **The parent inherits the whole coordinator loop.** Orca "does not schedule or place workers"; the coordinator must start each ready Task itself (`CAPS:92`). A parent must therefore start, wait on, read, and make one release-or-retain decision per settled sub-worker (`CAPS:107`), must not end its turn while any is `reclaimable` (`CAPS:113`), and must respect the three-failure circuit breaker (`CAPS:116`). Its own `worker_done` waits on all of that, so its terminal is held for the whole sub-run.
3. **The saving is small.** Every sub-worker start pays the same readiness limit, 60 s plus 50 s client grace by default (`CAPS:44-45`), whoever starts it. Depth 2 removes only the parent's `worker_done` and one coordinator read and `task-create`, and the coordinator must still read the parent's contract before anything depends on it (`SPEC:81-85`).
4. **The restraint is not machine-wide.** The setting lives in the only profile (`CAPS:98`) and `worker-start` has no depth flag (`CAPS:135`). V2's brief line binds only briefs written from IronClaude's `WORKER-CONTRACT.md` (`SPEC:58`); workers of any other Orca run here would get depth 2 with no such rule.

## Updated shared assumption responses

| A-NNN | R1 response | R2 response | Reason |
|---|---|---|---|
| A-002 | QUALIFY | REJECT | The assumption is false: a worker's top-level session is a second route to depth > 1 that leaves SA-2 and WC-8 intact and avoids R2-R4 (item 8). The route still carries R5, a new worker type (`SPEC:79`), the coordinator loop (`CAPS:92`, `CAPS:107`, `CAPS:113`, `CAPS:116`) and machine-wide scope (`CAPS:98`), so rejecting the assumption does not change the D5 recommendation. |
| A-003 | QUALIFY | QUALIFY (reason sharpened) | Contract text matters under both options, but at depth 1 Orca also refuses direct dispatch from every worker of every run (presumed call sites, `CAPS:103`), while V2's brief line restrains only IronClaude workers (New evidence 4). |

All other A-NNN responses are unchanged from R1-V1.

## Final per-point positions

| ID | Superior approach | Changed since R1? | Reason |
|---|---|---|---|
| S-001 | V2 | No | V2's leading section names what (a) gives up; V1 had none (item 11). |
| S-002 | V1 | No | V1 is framed on the spec's recommendation; V2 reframed only in R1. |
| S-003 | V1 | No (trigger revised) | V1 has a revisit condition; R2 replaces the P0 trigger, which V2 showed cannot fire (item 3). |
| S-004 | V1 | No | R5 (`SPEC:40`) still applies to the scoped (b), as V2 concedes. |
| S-005 | equal | No | Size and style do not decide the question. |
| C-001 | V1 | No | Depth 1 is the tighter bound; a raise widens it machine-wide (`CAPS:98-99`). |
| C-002 | equal | No | Same conclusion. |
| C-003 | equal | Yes (was V1) | Coordinator Tasks cover plannable fan-out (`SPEC:42`); the scoped (b) covers run-time splits between commands, at small saving (New evidence 3). |
| C-004 | V2 | No (reason changed) | `check --wait` is a liveness signal (`CAPS:64`); my "gap moves" rebuttal is withdrawn. |
| C-005 | V1 | No | V1 lists R5; both agree depth fixes only R1 for commands. |
| C-006 | equal | No | Standalone use is unaffected by either option under the worker-session route (`CAPS:148`). |
| C-007 | V1 | No | (a) costs nothing; scoped (b) needs a new worker type and its tests (New evidence 1). |
| C-008 | V1 | No | V1 gives a revisit path; lowering with live nested workers is UNVERIFIED. |
| C-009 | V1 | No | (b) adds terminals, release decisions and a held parent terminal (`CAPS:107`, `CAPS:113`). |
| C-010 | V1 | No | `CAPS:158` routes Orca-tracked fan-out to the coordinator; V2 withdrew its claim. |
| C-011 | equal | No | Both incomplete; `CAPS:157` child rows are not Tasks. |
| X-001 | V1 | No | Same as C-010. |
| X-002 | V2 | No | The run-time-split gap is real; V2 named it. |
| X-003 | V1 | No | V1 is internally consistent; V2 resolved its contradiction only by dropping its original route. |
| A-002 | equal | Yes (was V1) | V2 is right that the route exists and avoids R2-R4; V1 is right that it keeps R5, coordinator duties and machine-wide scope. |
| A-003 | V1 | No | At depth 1 a mechanical refusal backs the contract on every run; under (b) only IronClaude briefs carry a restraint. |

## Overall recommendation

Keep depth 1 (option a). Round 1 narrowed the dispute: both sides now agree that depth cannot reach a command's internal fan-out, that the section 1.3 design stays rejected, that R5 and machine-wide scope count against (b), and that nothing should be raised before evidence. The only surviving benefit of (b) is Orca-tracked fan-out for splits a worker finds between commands, and it saves one coordinator round trip while adding a second orchestrator, a new worker type with the full coordinator loop, and a looser bound for every Orca run on the machine. I propose the D5 text record two things V2 contributed: that if (b) is ever chosen, it takes the scoped worker-session form (depth exactly 2, brief line `Sub-workers: allowed, max N`, no command changes), and that the revisit trigger is a real run where a split was knowable only at run time and the round trip was material, not the P0 smoke runs.
<!-- end verbatim copy -->

### Variant 2 Rebuttal
<!-- verbatim copy of rounds/r2-variant-2.md -->
# D5 Round 2: Variant 2 advocate rebuttal (option b, raise nesting depth)

Citation key: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `INV-A:N` / `INV-B:N` = `.dev/orca-command-refactor/inventory/commands-a.md:N` / `commands-b.md:N`; `R1-V1` / `R1-V2` / `R2-V1` = `rounds/r1-variant-1.md` / `rounds/r1-variant-2.md` / `rounds/r2-variant-1.md`; `DA` = `diff-analysis.md`. Every cited line re-read 2026-11-02. Second in Round 2; sees R2-V1.

## Responses to criticisms

| # | Criticism (source) | Response | Concede / hold |
|---|---|---|---|
| 1 | Depth 2 cannot reach fan-out inside a command; V2's "each sub-unit its own Task" contradicts its own concessions (R1-V1 W1; DA X-003). | Already conceded (R1-V2 concession 2). Troubleshoot Tier 2 stays Agent-tool fan-out under both options, because only a command could start those sub-workers and SA-2 forbids it (`SPEC:170`, `SPEC:314`). | Concede |
| 2 | The heartbeat gap only moves to the parent (R1-V1 W2; DA C-004). | Held, and R2-V1 item 6 withdrew it: "Skip them while blocked inside `ask` or `check --wait`; those calls are liveness signals" (`CAPS:64`). New evidence 1 adds a caveat: the parent stays live, but may never be woken if sub-worker messages land in the coordinator's mailbox. | Hold (liveness only) |
| 3 | The provenance rule was misread (R1-V1 W3; DA X-001, spot-check 5). | `CAPS:158` is conditional and routes fan-out "from the coordinator". | Concede |
| 4 | The parent is a second orchestrator, R5 (R1-V1 W4; R2-V1 critique i; `SPEC:40`; `INV-A:90`; `INV-B:285`). | Conceded in R1 as "limited, not removed". It is worse than I said: in the same Run, sub-worker questions go to the Run mailbox, which is the coordinator's inbox (New evidence 1), so two controllers would read one inbox. | Concede (strengthened against me) |
| 5 | The parent inherits the coordinator loop: start, wait, read, one release decision per sub-worker, no turn end while any is `reclaimable`, the circuit breaker, a held terminal (R1-V1 W4; R2-V1 NE2; `CAPS:92`, `CAPS:107`, `CAPS:113`, `CAPS:116`). | Correct. The held terminal is live while in `check --wait` (`CAPS:64`), so it is a cost, not a fault. | Concede |
| 6 | The route buys nothing the coordinator cannot plan as Tasks (R1-V1 W4; R2-V1 items 2, 7). | My R1 case was splits found at run time (R1-V2 S2). Under the spec's brief, a worker runs "the exact command line" (`SPEC:79`), one command. Any split its session finds is a follow-up after that command, which is what the coordinator already does after it reads the contract (`SPEC:81-85`). At depth 1 the coordinator also starts each follow-up as a top-level worker in a parallel wave (`CAPS:86`), so tools are kept (my R1 S3 falls). The benefit needs a composite brief type the spec does not define. | Concede |
| 7 | The saving is small: every start pays the same readiness wait; the coordinator still reads the parent's contract (R2-V1 NE3; `CAPS:44-45`; `SPEC:81-85`). | Correct; the saving is one `worker_done`, one coordinator read and one `task-create`. | Concede |
| 8 | "One brief rule" understates the cost: it is a new worker type, outside the one-command brief, needing contract text and tests (R2-V1 item 12, NE1; `SPEC:79`, `SPEC:181`). | Correct, and item 6 shows that new type is the whole benefit, not an add-on. | Concede |
| 9 | The brief line restrains only IronClaude workers; the setting is machine-wide (R2-V1 item 5, NE4; `CAPS:98`, `CAPS:135`). | Correct. One qualifier: the depth-1 refusal is itself presumed for `worker-start` and `dispatch`, and unknown for `task-create` (`CAPS:103`; `SPEC:387`), so V1's "refused on every run" should be checked in P0. | Concede; qualifier on evidence |
| 10 | Depth 1 is the tighter bound, machine-wide (R1-V1 S1-S2; DA C-001, A-007). | Ranking conceded. The wording still matters: a raise widens the bound by one generation and the refusal still fires at the new maximum (`CAPS:99-100`). `SPEC:353` ("break R1's protection against runaway fan-out") should be corrected whatever is chosen. | Concede ranking; hold wording |
| 11 | "Nothing in the spec needs depth 2"; non-goal 2 (R1-V1 S3; `SPEC:315`). | I called this circular (R1-V2 W1). Item 6 shows it is true on substance: with a one-command brief, no worker session has fan-out to start. | Concede |
| 12 | Delivery of a depth-2 `worker_done` to the parent is UNVERIFIED (R2-V1 critique iv). | It was my own caveat (R1-V2 S5). New evidence 1 suggests delivery goes to the coordinator's Run mailbox unless the parent opens its own Run. | Concede |
| 13 | Reversibility is one-directional (DA C-008, A-006). | Lowering the value with live depth-2 workers is UNVERIFIED in the sources. | Concede |
| 14 | V2 stated no condition for choosing (b) and framed itself on the rejected design (DA S-002, S-003). | R1-V2 reframed it to the worker-session route. I now accept V1's revised trigger (R2-V1 item 3), with the precondition in New evidence 2. | Concede |
| 15 | More operator load: workers, Tasks, terminals to release (R1-V1 W5; DA C-009; `CAPS:113`). | Correct. | Concede |
| 16 | V2 omitted R5 (DA S-004, C-005). | Correct; R5 is the reason that still applies to the scoped route. | Concede |

## Updated assessment of Variant 1

**Steelman.** Variant 1's Round 2 is the stronger case and moved well past its original. It withdrew its weakest rebuttal (the heartbeat gap, R2-V1 item 6), conceded what (a) gives up (item 11), accepted that the worker-session route exists and avoids R2-R4 (item 8), and replaced a revisit trigger that could not fire with one tied to real runs (item 3). Its cost analysis is the decisive part: the brief is one command line (`SPEC:79`), so a worker that plans its own fan-out is a new worker type, and the parent must run the full coordinator loop (`CAPS:92`, `CAPS:107`, `CAPS:113`, `CAPS:116`) to save one coordinator read (`CAPS:44-45`; `SPEC:81-85`). Its point that the brief line restrains only IronClaude workers while the setting is machine-wide (`CAPS:98`) has no answer from me.

**Critique (residual).** Three gaps remain, none of which changes the choice. (i) V1's "Orca refuses direct dispatch from every worker of every run" rests on presumed call sites (`CAPS:103`); it should be confirmed in P0, together with `task-create` at depth 1 (`SPEC:387`). (ii) V1's revised trigger alone would not make (b) usable: with a one-command brief there is no worker-side fan-out to start, so the trigger also needs a defined brief type (New evidence 2). (iii) V1 proposes recording the scoped form of (b) but not correcting `SPEC:350` and `SPEC:353`, which still describe (b) as commands starting workers and as breaking the fence (New evidence 3).

## New evidence

1. **Sub-worker messages would land in the coordinator's inbox.** "A Run is a durable namespace and coordinator inbox" (`CAPS:92`); "From an active Dispatch, a new question defaults to its owning Run mailbox" (`CAPS:59`); the coordinator waits on `worker_done,escalation,question` (`CAPS:63`). A parent that starts sub-workers in the same Run would therefore send their questions, and probably their completions, to the coordinator, not to itself. The parent could open its own Run, which is allowed but does not reset depth (`CAPS:101`), and then it is a full coordinator of a second Run. Either way R5 becomes concrete, and my R1 claim that the parent fans in by itself (R1-V2 S2, S5) depends on an UNVERIFIED delivery path.
2. **The run-time-split benefit needs a brief type that does not exist.** The brief carries "the exact command line" (`SPEC:79`), and dependents are created only after inputs settle and are read (`SPEC:85`). A depth-2 worker session would therefore only relocate the coordinator's post-read planning. Any revisit of D5 needs both a defined composite brief and V1's real-run evidence.
3. **The D5 text is wrong under either choice.** `SPEC:350` asks whether depth should be raised "so commands could start their own Orca workers", the route both sides now reject; `SPEC:353` says (b) would "break R1's protection against runaway fan-out", while the refusal fires at any maximum and bad values fall back to 1 (`CAPS:99-100`).

## Updated shared assumption responses

| A-NNN | R1 response | R2 response | Reason |
|---|---|---|---|
| A-002 | REJECT | REJECT (reason narrowed) | The assumption is still false: a worker's top-level session is a second route that leaves SA-2 and WC-8 intact (`SPEC:72`, `SPEC:170`). But under the one-command brief (`SPEC:79`) the route has nothing to fan out, and it carries R5 through the shared Run inbox (New evidence 1), so rejecting the assumption does not favour (b) today. |
| A-003 | QUALIFY | QUALIFY (concede asymmetry) | Contract text carries weight under both options, but they are not symmetric: at depth 1 a presumed mechanical refusal (`CAPS:103`) backs WC-8 on every run on the machine; under (b) only IronClaude briefs carry a restraint (`CAPS:98`). Both the refusal call sites and `task-create` at depth 1 should be checked in P0 (`SPEC:387`). |

All other A-NNN responses are unchanged from R1-V2.

## Final per-point positions

| ID | Superior approach | Changed since R1? | Reason |
|---|---|---|---|
| S-001 | V2 | Yes (was equal) | Its leading section was the only statement of what (a) gives up (DA U-005); V1 agrees. |
| S-002 | V1 | No | V1 is framed on the spec's recommendation; V2 was framed on the rejected design. |
| S-003 | V1 | No | V1 has a revisit condition, now revised (R2-V1 item 3); V2 had none. |
| S-004 | V1 | No | R5 (`SPEC:40`) applies to the scoped route too. |
| S-005 | equal | No | Size and style do not decide the question. |
| C-001 | V1 | No | Depth 1 is the tighter bound; a raise widens it by one generation, machine-wide (`CAPS:98-100`). |
| C-002 | equal | No | Same conclusion. |
| C-003 | V1 | Yes (was equal) | With a one-command brief (`SPEC:79`), coordinator Tasks give the same per-unit records with no new worker type. |
| C-004 | V2 | No | `check --wait` is a liveness signal (`CAPS:64`); wake-up delivery is a separate, UNVERIFIED issue. |
| C-005 | V1 | No | V1 lists R5; both agree depth fixes only R1 for commands. |
| C-006 | equal | No | Standalone use is unaffected under the worker-session route (`CAPS:148`). |
| C-007 | V1 | No | (a) costs nothing; scoped (b) needs a new brief type, contract text and tests. |
| C-008 | V1 | No | V1 gives a revisit path; lowering with live depth-2 workers is UNVERIFIED. |
| C-009 | V1 | No | (b) adds terminals, release decisions and a held parent terminal (`CAPS:107`, `CAPS:113`). |
| C-010 | V1 | No | `CAPS:158` routes Orca-tracked fan-out to the coordinator. |
| C-011 | equal | No | Both incomplete; `CAPS:157` child rows are not Tasks. |
| X-001 | V1 | No | Same as C-010. |
| X-002 | V2 | No | The in-command gap is real and V2 named it, though neither option closes it. |
| X-003 | V1 | No | V1 is consistent; V2 resolved its contradiction only by dropping its original route. |
| A-002 | equal | Yes (was V2) | The route exists (V2), but under `SPEC:79` it has no use and it keeps R5 (V1). |
| A-003 | V1 | Yes (was equal) | At depth 1 a presumed mechanical refusal backs the contract on every run; under (b) only IronClaude briefs do. |

## Overall recommendation

Keep depth 1 (option a); I withdraw (b) as a choice for this spec. Round 2 showed that the scoped worker-session form has no use under the spec's one-command brief (`SPEC:79`), saves one coordinator read at the price of a second orchestrator that would share the coordinator's Run inbox (`CAPS:59`, `CAPS:92`), and loosens the bound for every Orca run on the machine (`CAPS:98`). Variant 2's lasting contributions should go into the D5 text: (1) reword the question and option (b) so they no longer describe commands starting workers or a broken fence (`SPEC:350`, `SPEC:353`; `CAPS:99-100`); (2) record that if (b) is ever chosen, it takes the scoped form (depth exactly 2, worker session only, brief line `Sub-workers: allowed, max N`, no command changes); (3) revisit only when a composite brief type is defined and a real run shows a split knowable only at run time whose round trip was material (R2-V1 item 3); (4) before any raise, verify the refusal call sites and `task-create` at depth 1 (`CAPS:103`, `SPEC:387`) and which mailbox receives a depth-2 worker's messages.
<!-- end verbatim copy -->

## Round 2.5: Invariant Probe
The full probe is in `invariant-probe.md` (fault-finder, not an advocate). Summary of its table:

- 17 findings: 4 ADDRESSED (INV-003, INV-008, INV-015, INV-016, all LOW); 13 UNADDRESSED (HIGH 4, MEDIUM 7, LOW 2).
- HIGH UNADDRESSED: INV-001 (option (a) assumes a root coordinator at depth 0), INV-004 (the depth-1 refusal's call sites were never traced and nothing verifies them under (a)), INV-005 (no contract rule stops a worker's top-level session from calling `worker-start`, `dispatch` or `task-create`), INV-017 (the claim "keeping depth 1, by itself, stops workers from starting Orca work" is not demonstrated: routes (a), (b), (c), (f), (g), (h) are open or unverified).
- MEDIUM UNADDRESSED: INV-002, INV-006, INV-007, INV-011, INV-012, INV-013, INV-014.
- LOW UNADDRESSED: INV-009, INV-010.
- The probe's own reading: none of the four HIGH items reverses the choice of option (a); they show that the debate's stated reason ("depth 1 is a mechanical backstop on worker fan-out") is not demonstrated and that (a) carries an unstated root-coordinator precondition.

## Round 3: Final Arguments
Not run. Round 3 is conditional and runs only at depth `deep`; this debate ran at depth `standard`. The early-termination condition "stable majority" also holds: agreement was 81.0% after Round 1 (17 of 21) and 95.2% after Round 2 (20 of 21), both at or above the 80% threshold, and all three taxonomy levels were covered in both rounds.

## Scoring Matrix
Method. One row per S-NNN, C-NNN and X-NNN in `diff-analysis.md`, plus the two promoted `[SHARED-ASSUMPTION]` points (A-002, A-003; status UNSTATED). A-001 (CONTRADICTED) and A-004 to A-007 (STATED) are not promoted, so they are not scored. Positions come from each advocate's Round 2 "Final per-point positions" table; every point has a Round 2 entry, so no Round 1 fallback was needed. With two advocates, a point is agreed only when both name the same answer (V1, V2 or "equal"). Confidence: unanimous 90-100%, +10% (capped) when the losing advocate conceded the point in writing; an unresolved point is 50%. Tier is the diff analysis tag (L1 surface, L2 structural, L3 state mechanics).

| Diff Point | Tier | V1 advocate (R2) | V2 advocate (R2) | Agreed | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|---|---|---|
| S-001 | L1 | V2 | V2 | Yes | Variant 2 | 95% | V2's leading "Strongest case" section was the only statement of what (a) gives up (DA U-005). The V1 advocate conceded this (R2-V1 item 11). |
| S-002 | L2 | V1 | V1 | Yes | Variant 1 | 95% | V1 is framed on the spec's own recommendation (`SPEC:352`); V2 argued for the design section 1.3 rejects. The V2 advocate conceded (R2-V2 item 14). |
| S-003 | L2 | V1 | V1 | Yes | Variant 1 | 90% | V1 has a revisit condition and V2 had none (R2-V2 item 14). Confidence held at the floor because V1's original trigger (P0 smoke runs) was conceded unable to fire and was replaced (R2-V1 item 3). |
| S-004 | L2 | V1 | V1 | Yes | Variant 1 | 96% | V1 cites R5 (`SPEC:40`), the reason that still applies to the scoped (b). The V2 advocate conceded the omission (R2-V2 item 16). |
| S-005 | L1 | equal | equal | Yes | equal | 92% | Size and citation style do not decide the question; both advocates held this in both rounds. |
| C-001 | L3 | V1 | V1 | Yes | Variant 1 | 90% | Depth 1 is the tighter bound; a raise widens it by one generation, machine-wide (`CAPS:98-100`). Both sides conceded that "removes the fence" was wrong (R1-V1 concession 1; R1-V2 A-001). |
| C-002 | L2 | equal | equal | Yes | equal | 95% | Same conclusion: the setting lives in the only profile and `worker-start` has no depth flag (`CAPS:98`, `CAPS:135`). |
| C-003 | L3 | equal | V1 | **No** | unresolved | 50% | V1 advocate: coordinator Tasks cover plannable fan-out and scoped (b) covers run-time splits at small saving (R2-V1 Final C-003). V2 advocate: under the one-command brief (`SPEC:79`) coordinator Tasks give the same records with no new worker type (R2-V2 Final C-003). The two advocates swapped positions between rounds. |
| C-004 | L3 | V2 | V2 | Yes | Variant 2 | 94% | A parent blocked in `check --wait` is a liveness signal (`CAPS:64`); the V1 advocate withdrew its "gap moves" rebuttal (R2-V1 item 6). Delivery of sub-worker messages to the parent stays UNVERIFIED. |
| C-005 | L2 | V1 | V1 | Yes | Variant 1 | 96% | V1 lists R5; both agree depth fixes only R1 for commands (`SPEC:36-40`). V2 conceded the omission (R2-V2 item 16). |
| C-006 | L2 | equal | equal | Yes | equal | 93% | Standalone use is unaffected by either option under the worker-session route (`CAPS:148`). |
| C-007 | L2 | V1 | V1 | Yes | Variant 1 | 95% | (a) costs nothing; scoped (b) needs a new brief type, contract text and tests (R2-V1 NE1). The V2 advocate conceded (R2-V2 item 8). |
| C-008 | L2 | V1 | V1 | Yes | Variant 1 | 90% | V1 gives a revisit path; both agree lowering the value with live nested workers is UNVERIFIED (R2-V1 item 10; R2-V2 item 13). |
| C-009 | L2 | V1 | V1 | Yes | Variant 1 | 97% | (b) adds terminals, release decisions and a held parent terminal (`CAPS:107`, `CAPS:113`). The V2 advocate conceded (R2-V2 item 15). |
| C-010 | L2 | V1 | V1 | Yes | Variant 1 | 98% | `CAPS:158` routes Orca-tracked fan-out to the coordinator; the V2 advocate withdrew its provenance claim (R1-V2 concession 1; R2-V2 item 3). |
| C-011 | L3 | equal | equal | Yes | equal | 90% | Both texts are incomplete: V1 dropped the `CAPS:155` UNVERIFIED caveat and V2's "invisible to Orca" ignores the UI child rows at `CAPS:157`. |
| X-001 | L2 | V1 | V1 | Yes | Variant 1 | 98% | The cited provenance line concludes "the fan-out must be Orca workers from the coordinator" (`CAPS:158`). The V2 advocate conceded (R1-V2 concession 1). |
| X-002 | L3 | V2 | V2 | Yes | Variant 2 | 94% | The gap for fan-out that cannot be lifted out of one command run is real and V2 named it; the V1 advocate conceded (R1-V1 concession 3). Neither option closes it. |
| X-003 | L2 | V1 | V1 | Yes | Variant 1 | 97% | V1 is internally consistent; V2's per-sub-unit benefit (`V2:8`) contradicted `V2:16` and `V2:22`, which its advocate conceded (R1-V2 concession 2). |
| A-002 | L2 | equal | equal | Yes | equal | 88% | The worker-session route exists and avoids R2-R4 (V2's point), but it keeps R5, the coordinator loop and machine-wide scope and has no use under `SPEC:79` (V1's point). Both advocates moved to "equal" only in Round 2, so the agreement is one round old. |
| A-003 | L3 | V1 | V1 | Yes | Variant 1 | 90% | Both advocates say a presumed mechanical refusal at depth 1 backs the contract on every run, while under (b) only IronClaude briefs carry a restraint (R2-V1 A-003; R2-V2 A-003). Confidence held at the floor because the refusal's call sites are UNVERIFIED (`CAPS:103`) and the probe marks the backstop claim not demonstrated (INV-004, INV-017). |

Tally: Variant 1 wins 12 (S-002, S-003, S-004, C-001, C-005, C-007, C-008, C-009, C-010, X-001, X-003, A-003); Variant 2 wins 3 (S-001, C-004, X-002); equal 5 (S-005, C-002, C-006, C-011, A-002); unresolved 1 (C-003). Total 21.

## Convergence Assessment
- Points resolved: 20 of 21 (`total = S 5 + C 11 + X 3 + promoted A 2`)
- Alignment: 95.2% (20 / 21)
- Threshold: 80%
- Round history: Round 1 81.0% (17 / 21; split on S-001, C-003, A-002, A-003); Round 2 95.2% (20 / 21; split on C-003 only)
- Unresolved points: C-003. Its two positions crossed between rounds (V1 advocate: V1 then equal; V2 advocate: equal then V1), so it is flagged as an oscillating point. It does not affect the base choice: both advocates' readings reject raising depth for it.

### Taxonomy coverage
| Level | Points | Addressed in the rounds | Covered |
|---|---|---|---|
| L1 surface | 2 (S-001, S-005) | 2 | Yes |
| L2 structural | 13 (S-002, S-003, S-004, C-002, C-005, C-006, C-007, C-008, C-009, C-010, X-001, X-003, A-002) | 13 | Yes |
| L3 state mechanics | 6 (C-001, C-003, C-004, C-011, X-002, A-003) | 6 | Yes |

All three levels have coverage, so no forced round is triggered.

### Invariant probe gate
HIGH-severity UNADDRESSED invariants (from `invariant-probe.md`):

| ID | Category | Finding (short) |
|---|---|---|
| INV-001 | state_variables | Option (a) silently assumes the coordinator is a root session at depth 0. If the coordinator is itself a dispatched worker (depth 1), a maximum of 1 refuses every `worker-start` it makes, and a new Run does not reset depth (`CAPS:97`, `CAPS:101`, `CAPS:151`). |
| INV-004 | guard_conditions | The depth-1 refusal is presumed for `worker-start` and `dispatch`; its call sites were never traced, `task-create` at depth 1 is unknown, and nothing under (a) verifies them (`CAPS:103`; `SPEC:36`; `SPEC:387`). |
| INV-005 | guard_conditions | No contract rule binds a worker's top-level session: WC-8's owner is "Command" and SA-2 binds command, skill and agent files (`SPEC:72`, `SPEC:170`); the worker-session rules (WC-3, WC-5, WC-7, WC-12) contain no ban on `worker-start`, `dispatch` or `task-create`. |
| INV-017 | sufficiency_challenge | "Keeping depth 1, by itself, stops workers from starting Orca work" is not demonstrated: direct dispatch, `task-create` picked up by the coordinator's ready scan, low-level dispatch and `orca-cli` launch routes, and a later machine-wide raise are open or unverified, and the worker session has no contract backstop. |

```
CONVERGENCE BLOCKED: 4 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-001, INV-004, INV-005, INV-017
These invariant violations must be resolved before convergence can be declared.
Action: Address the flagged items in a subsequent debate round or acknowledge as accepted risk.
```

```
WARNING: 7 MEDIUM-severity UNADDRESSED invariant(s) detected
Items: INV-002, INV-006, INV-007, INV-011, INV-012, INV-013, INV-014
These items do not block convergence but should be reviewed.
```

LOW UNADDRESSED (no gate action, recorded): INV-009, INV-010.

### Status
- Diff-point agreement: 95.2%, at or above 80%: PASS
- Taxonomy gate (all levels covered): PASS
- Invariant gate (zero HIGH UNADDRESSED): FAIL (4)
- **Status: BLOCKED_BY_INVARIANTS**

What the block means for D5: the two advocates agree on the choice (keep depth 1), and none of the four HIGH items argues for raising depth. The block is on the stated reasons and preconditions of option (a), not on its selection. `refactor-plan.md` carries one planned change or one explicit accepted-risk entry per blocking item, so the block can be cleared by applying that plan to the D5 text and the spec, or by the user accepting the listed risks.

## Advocates' final recommendations
- **Variant 1 advocate (R2-V1 "Overall recommendation"):** "Keep depth 1 (option a)." It asks the D5 text to record the scoped form of (b) (depth exactly 2, brief line `Sub-workers: allowed, max N`, no command changes) and a revisit trigger tied to a real run with a split knowable only at run time, not the P0 smoke runs.
- **Variant 2 advocate (R2-V2 "Overall recommendation"):** "Keep depth 1 (option a); I withdraw (b) as a choice for this spec." It asks the D5 text to reword `SPEC:350` and `SPEC:353`, record the same scoped form of (b), revisit only when a composite brief type is defined and a real run shows a material run-time split, and verify the refusal call sites, `task-create` at depth 1 and depth-2 mailbox delivery before any raise.
