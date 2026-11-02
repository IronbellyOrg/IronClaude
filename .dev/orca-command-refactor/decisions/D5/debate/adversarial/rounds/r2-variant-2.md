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
