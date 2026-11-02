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
