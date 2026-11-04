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
