# Debate Round 1: Advocate for Variant B (opus:analyzer)

- Round: 1 (deep)
- Advocate: Variant B, `variant-2-opus-analyzer.md`
- Ground truth used: `seed-brief.md`, `src/superclaude/core/WORKER-CONTRACT.md`, `.dev/issues/431/issue-body.md`, `adversarial/diff-analysis.md`

## Steelman of Opposing Variants

### Variant A (opus:architect)

A's strongest case: it treats "evidence, verdict, action" as three layers and backs that with real machinery rather than prose.

- **Absence can never become proof by accident.** Every observation carries `proof_class` (positive / absence / unknown) ("§3 Observation record", FR-002). A rule that acts on silence first needs an observation whose class is `absence`, and the ladder never promotes that to L4. This is the cleanest mechanical reading of WC-10 (`WORKER-CONTRACT.md:44`) and Orca's stall-proof rule (`seed-brief.md:71`).
- **Three orthogonal axes, state derived on read** (U-001). Process, interaction and progress come from different sources, so one wrong adapter value cannot silently rewrite the others. Case 1 (live process, flat progress, thrashing screen) falls out naturally.
- **Cost tiers T0/T1/T2** (U-003) put the expensive probes (screen, transcript) behind suspicion. NFR-004 and AC-14 then hold a healthy fleet to two fleet calls per sweep, a claim B makes and then breaks (X-015).
- **The safest ladder of the three on destructive actions.** L2 never uses `--interrupt` (FR-025). Context exhaustion ends at L5 with the person's go in v1 ("§8 State-to-ladder map"). This respects the brief's "a nudge into a working session must be harmless" (`seed-brief.md:37`) and WC-6 (`WORKER-CONTRACT.md:72-73`) without a loophole.
- **Engineering ergonomics.** There is one timing-parameter table, overridable per Task and never by the worker (U-007, NFR-003). Reply IDs are coordinator-assigned and carry a supersedes rule (U-004). The adapter `Receipt` separates accepted, submitted and `turn_started` (U-006), so "the text was typed" is never mistaken for "a turn started". The work unit is defined by the `replaces T<n>` chain (U-009), so a restart budget survives the new Task IDs that WC-6 requires (`:69`).
- **Read-ack placed on `status`, explicitly because heartbeats are not sent in `ask`** ("§7 Protocol"). That is WC-3 (`:56`) and the Heartbeats bullet (`:61`) applied correctly.

### Variant C (haiku:backend)

C's strongest case: it is the only variant that designs the supervisor as a distributed system that will crash, run twice and receive hostile input.

- **Fencing.** State is keyed by `(run_id, task_id, dispatch_id)` plus `attempt_epoch` (FR-005, U-022). A late heartbeat or ack from a superseded attempt cannot move the new attempt's state. Under WC-6 every retry is a new Task (`WORKER-CONTRACT.md:69`), so old and new attempts coexist for a while. A and B do not fence that window.
- **Crash safety.** Persist before acking the transport batch (NFR-005). A single-owner transactional ledger (NFR-006). `reconcile()` after any ambiguous side effect, with crash-at-every-boundary tests (U-029). Fail closed on storage or ownership errors (NFR-010). Because `check --ack` acknowledges the reader's own batch (`seed-brief.md:67`), acking before persisting loses messages on a coordinator crash. C is the only variant that closes this.
- **A resume note that can say "do not replay".** `uncertain_effects` in `resume-note.json` blocks automatic replay when the old attempt may have half-applied a side effect (FR-021, U-028). This directly serves "a restart must preserve on-disk progress" (`seed-brief.md:37`).
- **The strictest reading of the safety constraints.**
  - Typing happens only at a positively identified prompt (FR-019).
  - Never interrupt.
  - Never type while `ask` owns the input (FR-017).
  - "A context error alone is NOT an additional Orca stall-proof class" (FR-019).
  - C is the only variant that treats "typing into a working session is harmless" as unproven (X-011). It is in fact UNVERIFIED (A-018).
- **Operating the supervisor itself.** A watchdog outside the coordinator turn (NFR-009, U-032) addresses A-001, which A and B leave as a risk. A controller lock prevents two coordinators (U-031). Input limits of 16 KiB and depth 8 apply to worker payloads (NFR-008). Rollout is staged: observe, then nudge, then replace (NFR-011).
- **The WC-7 amendment** (U-033): the top-level session must invoke the Skill; reading the Skill's definition is not running it. WC-7 (`:58`) today says only "runs the command directly", so C closes a real gap.

## Strengths of Variant B

1. **A root cause that explains all eight cases with one mechanism.**
   - Evidence: "§1.1 The root cause behind all eight cases" and "§5.1 What the root causes have in common".
   - B's claim: the coordinator treats evidence that something once happened (a heartbeat arrived, a file was touched) as evidence of what is happening now. It has no non-destructive action for silence, and WC-12 is pull-only (`WORKER-CONTRACT.md:59`).
   - B then separates the occurrence cause from the detection cause per case, each with a confidence (U-011, "§5 Mapping"). Neither A nor C gives the reader a way to see which fixes prevent a failure and which only detect it sooner.

2. **The arrival-versus-change matrix** ("§3.2 The arrival vs change matrix", U-010).
   - The brief's problem statement is literally "timer heartbeats whose status never changes" (`seed-brief.md:17`).
   - B's matrix is the only artifact that makes "arrived but unchanged" a first-class cell. That cell is distinct from "absent" and from "changed".
   - A-016 is stated by all three, but only B turns it into a decision table.

3. **A wait that never filters a type, verified against the binary.**
   - Evidence: FR-011 names all nine types, including `heartbeat` ("§6.1 Mechanism (verified)"). FR-012 processes the whole batch before `check --ack`.
   - This is the only literal satisfaction of "A coordinator wait never filters out a worker message type" (`seed-brief.md:43`) that also works in v1 (see X-001, X-021).
   - B checked `check --help` itself (U-021) and did not rely on the guide's filter, which the brief identifies as the case-4 mechanism (`seed-brief.md:66`).

4. **A read-ack that has a carrier in v1.**
   - Evidence: "§7.2 What the worker sends". The ack is a `status` message whose body line is the authority, `ack <message_id> <applied|queued|refused> <reason>`; the payload is optional.
   - `status` is an existing Orca type (`seed-brief.md:65`), sent by the top-level session (WC-7, `:58`). It is not a heartbeat, so the cadence the preamble owns (`:7`) is untouched, and it needs no payload parsing (A-007 is UNVERIFIED).
   - `queued` lets a worker in a long step acknowledge a read without pretending to have applied it. That is a partial answer to A-004, which A and C do not attempt.

5. **Cadence stays preamble-owned.**
   - Evidence: the adaptive silence window W = max(10 min, 2 × median observed heartbeat interval) (FR-010, U-014, "§4.1 Sweep loop").
   - A's fixed W and C's fixed figures both assume a cadence that the contract says only the preamble sets (`:7`, `:61`).
   - B derives the window from what the worker actually does, so a preamble change cannot cause false silences.

6. **The case-8 latency is attributed to a named rule.**
   - Evidence: "§4.1 Sweep loop", U-015.
   - The guide's only sweep trigger is "after three consecutive empty waits" (up to 45 minutes, `seed-brief.md:71`).
   - B replaces it with a sweep after every wake or timeout (FR-008). That is a v1-fixable policy change, not machinery.

7. **Worktree evidence scoped to the worker's own files.**
   - Evidence: SG-2 and SG-10 in "§3.1 Signal evaluation"; FR-009.
   - WC-11 (`:45`) says workers can share a feature worktree and write only their own report directory. Activity elsewhere in that worktree may belong to another worker.
   - B's scoping is therefore contract-correct. C's whole-worktree inventory (NFR-003) has to downgrade unattributed changes for exactly this reason.

8. **A ranked case-5 hypothesis set** (H1-H4, "§5 Mapping", U-012).
   - H1 is an ask timeout without resume, which is exactly the WC-3 edge (`:56`). H3 is a wrong `reply --id`.
   - Each hypothesis is testable from logs, so v1 can confirm or kill it.
   - A's "pull model probable" is one hypothesis. C declines to rank, which leaves no worker-side fix to prioritise.

9. **Restarts defer to the commands' own resume rules.**
   - Evidence: "§8.5 Resume-note format", U-020. The `/sc:implement` D2 freeze and E-RESUME-NEEDED take priority over the coordinator's note.
   - This keeps the restart inside the command's Resume rule, which WC-6 already names as a retry input (`:69`).

10. **Worker rules have one home.**
    - Evidence: "§9.2 Why not the preamble or the commands".
    - The preamble is Orca-owned (`:7`). Commands may contain no Orca calls (WC-8, `:38`, and `:5`). The rules belong in contract section 3, which already "binds the top-level session" (`:49`).
    - This avoids C's split (FR-022) and A's v2 move into `## Unattended mode`.

11. **Degraded mode and replay fixtures.**
    - Evidence: "§11.3 Another harness", "§13.1" AC-1..AC-8, U-016, U-017.
    - A harness without a stall-proof adapter never reaches L4. That is the portability constraint (`seed-brief.md:34`) made safe by default.
    - Acceptance comes from replaying the 8 real cases, not from synthetic tests alone.

12. **A handoff file even on failure, plus pending acks closed at settlement.**
    - Evidence: WR-3 and FR-025 in "§9.1 Rules" and "§9.3"; FR-017 in "§7.3".
    - The resume input exists precisely when it is most needed, and no ack stays "pending" forever after the Task settles.

## Critiques of Variants A and C

### Critiques of Variant A

Each item says what would falsify it.

- **A1. The wake set excludes `heartbeat` (X-001).**
  - Location: FR-016, "§6 Wake set versus read set".
  - The brief's criterion is that "a coordinator wait never filters out a worker message type" (`seed-brief.md:43`). A's set is literally "every known type except heartbeat". `check --types` is only the wake condition (`seed-brief.md:66`), so no message is lost, but a heartbeat-only batch waits a full W.
  - That matters exactly where A's own design puts signal in the heartbeat: `pending_ack[]` and context `near_limit` in `ironclaude.progress/1` ("§3 S2"). A designs a context-pressure alarm and then removes it from the wake condition.
  - Falsified if: the brief's criterion is read as "never loses a type", not "never filters the wake". The diff analysis records that A satisfies it only under its own reading.

- **A2. The v2 WC-6 amendment redefines an Orca proof (X-004, C-022).**
  - Location: "§10 WC rules amended". Twice-confirmed exhaustion "counts as a positive stall proof".
  - Orca's stall proof has exactly three sources (`seed-brief.md:71`): `exited` liveness, the worker's own exit, and a final transcript turn with no `worker_done`. WC-6 settles only "after Orca's positive stall proof" (`WORKER-CONTRACT.md:73`), and WC-10 acts "only on Orca's stall proofs" (`:44`).
  - IronClaude cannot unilaterally widen a proof the contract attributes to Orca. B's C-9 sends it to Orca or the person as a policy change; C forbids it.
  - Falsified if: Orca documents context exhaustion as a stall proof (UNVERIFIED; not in the enrichment).

- **A3. A terminal copy is typed into a worker blocked in `ask` (X-010).**
  - Location: "§7 Protocol". A = 5 min in ask, then a `--wait-submit` copy.
  - While blocked in `ask` the foreground process is the `ask` call, and no heartbeat is sent (`:56`, `:61`). Text typed then lands in whatever owns the TTY. A does not say whether that is the agent's input or the `ask` process.
  - B shares this flaw (see Concessions); C's guard is right.
  - Falsified if: Orca shows `ask` returns control before typed text is read. UNVERIFIED.

- **A4. "The nudge is harmless to a working session" is asserted, not shown (X-011, A-018).**
  - Location: "§8 Nudge text". A's own open questions call mid-turn queueing UNVERIFIED, yet the template is labelled harmless.
  - B makes the same bet but writes the text for it ("If a step is running, ignore this and continue", "§8.3"). FR-020 also counts a nudge with no turn start as failed, so a lost nudge is not mistaken for a delivered one.

- **A5. No worktree activity in v1 ("§10 Delivery table").**
  - A drops the one cheap independent signal that the progress claim needs. FR-009 says S2 "needs a non-contradicting independent signal", but in v1 that signal can only be a T2 probe.
  - So every long step with a flat payload costs a screen or transcript read. B's per-contract-path `stat` is the cheap middle.
  - Falsified if: A's T2 probe count per long step is shown to stay at one or fewer.

- **A6. A fixed Q = 10 and W = 5 against a preamble-owned cadence (`:7`).**
  - If the preamble sets a 10-minute heartbeat, A's flat-progress rules fire on schedule rather than on silence. B's adaptive W (FR-010) is immune.
  - Falsified if: A's parameter table is defined relative to cadence. It is not ("§4 Timing parameters").

- **A7. Case-5 cause ranked "probable" on one hypothesis ("§5 Mapping").**
  - WC-12 pull does explain an idle-at-prompt worker missing a reply.
  - But case 5 workers were not shown to be idle at the prompt (`.dev/issues/431/issue-body.md`; cause not established, `seed-brief.md:79` "UNVERIFIED as the cause"). The ack bounds the cost either way, but the worker-side fix differs.

- **No contradiction found with:**
  - WC-8. A's commands make no Orca calls; its v2 Stop hook is a harness hook, not a command.
  - WC-7. A does not amend it, and lifecycle messages stay top-level.
  - The no-sender-read-receipt fact. A's `Receipt` explicitly separates `accepted` from `turn_started`.

### Critiques of Variant C

- **C1. The read-ack rides the heartbeat channel (X-008, C-014). This contradicts the contract.**
  - Location: FR-016, "Reply Read-Acknowledgement Protocol". The ack is heartbeat `--payload` kind `read_ack`.
  - The contract says the preamble "is the authority for ... the heartbeat cadence" (`WORKER-CONTRACT.md:49`, `:7`). C concedes this: "the negotiated dispatch preamble must permit this immediate control acknowledgement", otherwise `ack_unsupported`.
  - WC-3 and the Heartbeats bullet forbid a heartbeat while blocked in `ask` (`:56`, `:61`). An `ask` timeout followed by a resumed `ask` on the same ID is exactly when an answer arrives.
  - So in v1 C's ack has no legal carrier. A and B both use `status`.
  - Falsified if: an Orca preamble is shown that already authorizes an off-cadence heartbeat. None is cited.

- **C2. C's v1 ack bounds cannot hold (X-009, C-041).**
  - Location: FR-017 sets suspicion at 2, copy at 5 and report at 10. Yet C's own v1 row says the worker confirms "at its first legal checkpoint", and its signal table says "worker may be unable to emit during blocking work".
  - A worker in a 20-minute step would be reported to the person at minute 10 for an answer it read correctly.
  - This is C contradicting itself, not just an assumption.

- **C3. The `blocked_ask` heartbeat mode conflicts with WC-3 (X-020).**
  - Location: FR-008. The `mode` enum includes `blocked_ask`, with `pending_question_id`.
  - A heartbeat can never be sent while blocked in `ask` (`:56`, `:61`). The mode is legal only if sent strictly before `ask` starts, and C does not say so.
  - As written, an implementer reads it as "report while blocked".

- **C4. The case-4 bound of 1 minute relies on v2 machinery (X-021).**
  - Location: "Mapping of the 8 Observed Cases" claims 1 minute via the unconditional drain. But the drain (FR-010, FR-013) sits in v2 in "Contract Changes: v1 Now vs v2 (#423)".
  - In v1 the bound is one 5-minute wait cycle, the same as A and B. The brief's target is "one wait cycle" (`seed-brief.md:42`), so C does not fail the target. It overstates its v1 bound.

- **C5. Context-exhausted can clear itself (X-007, C-003).**
  - Location: "Worker State Model". A worker returns to progressing on "evidence of useful resumed work".
  - In case 1 the thrashing worker kept emitting heartbeats and some activity for about four hours (`seed-brief.md:17`). "Useful resumed work" is precisely what a compact-thrashing session appears to produce between compactions.
  - C's own risk table says heartbeat volume cannot reset incident age. The exit rule reopens that hole through another signal.
  - Falsified if: C defines "useful" as a changed `progress_rev` plus a checkpoint sha change. If so, it should say so in the state model.

- **C6. Idle verdicts at 6 minutes, with no wait cadence that can produce them (X-013).**
  - Location: "Detection Rules and Time Bounds". C claims idle at 6, nudge by 7 and report by 10.
  - That needs a 1-minute confirmation sample plus a 1-minute drain, both v2. In v1, with a 5-minute wait, the earliest second sample is 10 minutes.
  - C's figures are v2 figures labelled as bounds.

- **C7. Cumulative context cost is unbudgeted (C-039).**
  - A 1-minute drain is about 240 drains in 4 hours, each a tool call in the coordinator's context. C marks the cost UNVERIFIED and still schedules it.
  - A-001 and A-002 (the coordinator stays responsive) are the failure mode this run already showed in the workers.

- **C8. Whole-worktree inventory against WC-11 (`:45`).**
  - Shared feature worktrees hold other workers' writes. C downgrades unattributed changes to "supporting only" (NFR-003), so the expensive inventory buys a signal that cannot decide anything.
  - B's scoping to the worker's own report directory or child worktree gets the decisive part for one `stat` each.

- **C9. Rules split across three homes (X-018, FR-022).**
  - Chain logic and stage checkpoints in commands is acceptable: they are files, not Orca calls, so there is no WC-8 conflict (`:38`).
  - But putting "do not end a turn between chain steps" in commands means every chain-running command changes. The contract rule binds the top-level session once (`:49`).

- **No contradiction found with:**
  - The stall-proof sources. C is strictest here.
  - WC-7. C's amendment strengthens it.
  - WC-8.
  - "No sender read receipt". C's lifecycle keeps answer_enqueued separate from read_confirmed.

## Concessions

B is wrong on the following. The merged design should take the A or C position.

1. **The S6 interrupt rung is unsafe (X-002, C-017). Take A FR-025 / C "never interrupt".**
   - "§8.2 Response per state" sends `terminal send --interrupt` plus "write your handoff file now, then end your turn". B's S6 verdict can rest on a screen pattern seen twice (FR-007), so a false positive interrupts a working session.
   - That breaks the brief's "a nudge into a working session must be harmless" (`seed-brief.md:37`).

2. **B manufactures stall proof (X-003). This is the most serious error in B.**
   - Interrupting a session and then treating the turn end it provoked as "a transcript whose final agent turn sent no `worker_done`" games Orca's third proof source (`seed-brief.md:71`). The final turn ended because the coordinator ended it.
   - The same applies to B's C-7 wording ("§10.1", "§10.2"): an idle worker after two nudges plus one ask "has met Orca's stall proof". It has not. Only the transcript reading can be the proof, and the nudges add nothing to it.
   - B's §8.2 S3 path to L4 must be rewritten to rest on the transcript proof alone, read freshly (A-008).
   - WC-6 (`WORKER-CONTRACT.md:72-73`) and WC-10 (`:44`) require Orca's positive proof, not a proof the coordinator induced.

3. **The precedence S6 > S4 is wrong (X-005, C-002). Take A: person-prompt above context-exhausted.**
   - With B's order, a thrashing worker that also shows a permission dialog gets the interrupt on a person-only prompt.
   - The prompt is the stronger, cheaper-to-handle fact ("a waiting worker is healthy, not failed", `seed-brief.md:69`).

4. **AC-1 allows 20 minutes for case 1 (X-014),** above the brief's 15-minute target (`seed-brief.md:42`). "§4.2" itself states 15, so AC-1 should say 15.

5. **The NFR-004 call count is false as written (X-015).** "Three fleet-wide calls" plus "one `stat` per contract path" scales with the fleet. Take A's tiering: `stat` belongs at T1 for suspicious workers only, or the NFR should be restated as O(n) cheap local calls.

6. **Unreachable is reported at 30 minutes (X-016, C-036).** Take A or C at 10 minutes. B gives no reason a host loss should be reported three times later than every other state. Reporting is non-destructive, so the false-positive cost is low.

7. **The terminal copy has no ask-ownership guard (X-010). Take C FR-017:** never type while `ask` owns the input. The A3 critique above applies equally to B "§7.3".

8. **Fencing and crash safety are missing.** Take C's `attempt_epoch` (U-022), persist-before-ack (U-025), `reconcile` (U-029), `uncertain_effects` (U-028) and controller lock (U-031). B's R9 names the two-coordinator risk but gives no mechanism.

9. **Observation provenance.** A's `proof_class` (U-002) is a better guard against absence-as-proof than B's prose list in "§8.6". B should adopt it.

10. **Restart budget.** C's per-lineage cap (2 over the whole lineage) is safer than B's 2 per 6 hours for a 12-hour run (X-012). The brief's case 8 is a recurrence loop. Merge: 2 per 6 hours and at most 2 per lineage without the person's go.

11. **The parameter table.** A's single table (U-007) beats B's thresholds scattered over FR-008..FR-010 (S-011).

## Shared Assumption Responses

| ID | ACCEPT/REJECT/QUALIFY | Reason |
|---|---|---|
| A-001 | QUALIFY | Needed for every bound, but cannot be assumed. Adopt C's watchdog outside the coordinator turn (NFR-009); its scheduler is UNVERIFIED, so in v1 the person-visible fallback is a run note listing the last sweep time |
| A-002 | REJECT | Unbudgeted context growth is the failure this issue is about, moved to the coordinator. A 5-minute sweep is about 48 per 4 h; the design must cap sweep output (summary line per healthy worker) and say so. UNVERIFIED cost |
| A-003 | QUALIFY | An empty timeout return is small but not zero. It is acceptable at 5 minutes (48 per 4 h); not shown acceptable at C's 1 minute. UNVERIFIED |
| A-004 | REJECT | A worker inside a long tool call cannot ack. Bounds must count from the worker's next checkpoint, or the ack must allow `queued` (B "§7.2"). Escalate to a terminal copy only when other evidence shows the worker is idle, not merely unacked |
| A-005 | QUALIFY | Use `agentWait` as the primary case-6 signal (`seed-brief.md:69`), with a screen probe as backup when the worker is silent past W. The brief notes that `Notification` did not fire in one harness. UNVERIFIED reliability |
| A-006 | ACCEPT | Matches `seed-brief.md:67`. All three define a no-terminal fallback that goes straight to reporting |
| A-007 | QUALIFY | Do not make v1 correctness depend on the payload. B's body-line-is-authority rule for the ack and the phase-text fallback for progress keep v1 working if the payload is mangled. UNVERIFIED |
| A-008 | QUALIFY | Transcript stall proof needs two reads at least S apart with no new entries and no tool call in flight. A single tail read may be mid-turn (B "§4.2" UNVERIFIED note) |
| A-009 | ACCEPT | `seed-brief.md:71`: "Nudge and ask are not forbidden". WC-10 (`WORKER-CONTRACT.md:44`) forbids only stop, retry and release on absence |
| A-010 | QUALIFY | Compliance is probable, not certain. Case 7 (turn ended between chain steps) is itself a compliance failure. Detection (S3 idle) must stay as the backstop; A's v2 Stop hook is a reasonable accelerator |
| A-011 | QUALIFY | Use coordinator receipt time (monotonic) for all ages, as C does. Use worker or transcript timestamps only as ordering within one source |
| A-012 | QUALIFY | Holds for `/sc:implement` (D2, E-RESUME-NEEDED; B "§8.5"). For other commands, the resume note is advisory input only, and C's "verified resume interface only" rule should gate automatic restart |
| A-013 | QUALIFY | Must be enforced, not assumed. Adopt C's controller lock; B R9 only names the risk |
| A-014 | QUALIFY | Treat a projection older than two sweeps as unknown (A FR-006). B's FR-004 10-minute rule is equivalent |
| A-015 | ACCEPT | It loses nothing in transit, provided the coordinator persists its handling before `--ack` (C NFR-005). Without that a coordinator crash loses the batch |
| A-016 | ACCEPT | This is the core of B "§3.2" and the brief's problem statement (`seed-brief.md:17`) |
| A-017 | ACCEPT | B verified it from `check --help` ("§6.1"). Runtime wake behaviour per type is still not observed live (`seed-brief.md:61`), so the replay fixtures should test it |
| A-018 | REJECT | Not established. Until shown, typed text goes only to a positively identified prompt (C FR-019). A working-session nudge is a v2 option once queueing is observed. B and A both assumed this too readily |

## Per-Point Positions

| Point | Preferred variant (A/B/C/merge) | Confidence 0-1 | One-line reason |
|---|---|---|---|
| X-001 | B | 0.75 | All nine types named in the wake set; literal fit to `seed-brief.md:43` and works in v1 (C's drain is v2) |
| X-002 | A | 0.9 | Never `--interrupt` (FR-025); B's S6 interrupt breaks the harmless-nudge constraint (conceded) |
| X-003 | C | 0.85 | The coordinator never manufactures stall proof; only the three Orca sources count (`seed-brief.md:71`); B's induced turn end is conceded |
| X-004 | B | 0.7 | A new proof kind needs Orca or the person; A's v2 WC-6 rewrite redefines an Orca-owned proof |
| X-005 | A | 0.8 | Person-prompt above context-exhausted, so no rung lands on a person-only prompt (conceded) |
| X-006 | B | 0.6 | Finished-unreported evidence is stronger and its response (nudge for report) is cheaper than a restart path |
| X-007 | B | 0.75 | No self-exit from context-exhausted (A agrees); C's "useful resumed work" is what thrashing looks like |
| X-008 | B | 0.7 | `status` with an authoritative body line; no dependence on payload transport (A-007) or preamble permission |
| X-009 | B | 0.6 | C's v1 bounds are self-contradictory; B's `queued` disposition lets a busy worker ack honestly |
| X-010 | C | 0.8 | Never type while `ask` owns the input; A and B lack the guard (conceded) |
| X-011 | C | 0.65 | Typing into a working session is UNVERIFIED (A-018); restrict typing to an identified prompt until it is observed |
| X-012 | merge | 0.7 | 2 per 6 h (A/B) plus C's cap of 2 per lineage without the person's go |
| X-013 | B | 0.55 | 15 min is achievable in v1 and meets the target; C's 6 min needs v2 samples; B's W derives from the observed cadence |
| X-014 | A | 0.8 | B's AC-1 at 20 min exceeds the 15-min target; A meets it (conceded) |
| X-015 | A | 0.8 | A's tiered sweep keeps the constant-cost claim true; B's NFR-004 is false as written (conceded) |
| X-016 | A | 0.8 | Report unreachable at 10 min; reporting is non-destructive (conceded) |
| X-017 | B | 0.6 | Ranked, testable H1-H4 beat one "probable" hypothesis or no ranking |
| X-018 | B | 0.6 | Contract section 3 binds the top-level session once (`WORKER-CONTRACT.md:49`); commands stay unchanged |
| X-019 | merge | 0.5 | v2 hook forwarding (B) plus A's capped Stop hook as an opt-in, never compulsory (C) |
| X-020 | A | 0.7 | No heartbeat in `ask`, with the reason stated (`:56`, `:61`); C's `blocked_ask` mode conflicts |
| X-021 | B | 0.7 | The v1 bound is one wait cycle; C's 1-min claim needs the v2 drain |
| C-001 | merge | 0.7 | A's three axes plus B's separate freshness, keyed by C's `(run, task, dispatch, attempt_epoch)` |
| C-002 | merge | 0.65 | A's person-prompt over context-exhausted; B's finished-unreported over context-exhausted; exited first |
| C-003 | B | 0.75 | No self-recovery; leave only by restart or person action |
| C-004 | merge | 0.6 | A's field set, B's phase-text fallback for v1, C's epoch fields in v2 |
| C-005 | A | 0.7 | The payload is a claim that needs a non-contradicting independent signal (FR-009) |
| C-006 | B | 0.75 | Wake on all nine, whole batch, then ack; no v2 drain needed |
| C-007 | A | 0.7 | Cost tiers; `stat` and screen only for suspicious workers |
| C-008 | B | 0.6 | Sweep after every wake or timeout removes the three-empty-waits latency (case 8) |
| C-009 | merge | 0.6 | A/B v1 bounds (15) as commitments; C's figures as v2 targets once timers exist |
| C-010 | B | 0.6 | Idle needs transcript age, an empty-prompt classification and no pending ask; two sources, not a clock |
| C-011 | B | 0.65 | Screen confirming only; transcript primary for idle vs progressing |
| C-012 | merge | 0.6 | A's two-source confirmation; C's rule that a compaction count alone only raises suspicion |
| C-013 | B | 0.65 | `stat` on the worker's own contract path is cheap and WC-11-correct (`:45`) |
| C-014 | B | 0.65 | `status` body line keyed by Orca message ID; A's reply-id marker is a compatible add-on |
| C-015 | merge | 0.65 | A's clock restart and second-timeout path, C's ask guard, B's no-terminal route straight to the person |
| C-016 | C | 0.6 | Dedup key includes `attempt_epoch`; persist disposition first |
| C-017 | A | 0.8 | L0-L5 without interrupt; L4 only on positive evidence |
| C-018 | A | 0.6 | Caps per state episode and per Task are clearer than B's per-60-min count |
| C-019 | merge | 0.7 | Same as X-012 |
| C-020 | A | 0.6 | Same cause: plan must change and the person approves |
| C-021 | merge | 0.65 | B's text note with `/sc:implement` D2 priority, plus C's `uncertain_effects` blocker |
| C-022 | B | 0.6 | C-9 as a policy question for Orca or the person; drop B's §8.2 induced proof (conceded under X-003) |
| C-023 | B | 0.6 | Contract only; the preamble is Orca-owned and commands stay Orca-free |
| C-024 | merge | 0.55 | B's markdown handoff written even on failure, with C's atomic publish and sha |
| C-025 | C | 0.55 | The 80-line rule plus a byte limit for long physical lines |
| C-026 | B | 0.5 | Two separate rules (chain continuity; reads and handoffs) are easier to cite than one combined rule |
| C-027 | merge | 0.6 | The A/B amendment list plus C's WC-7 Skill-invocation clarification |
| C-028 | merge | 0.65 | A/B v1 ack and sweep policy; C's ledger, fencing and drain in v2 |
| C-029 | merge | 0.65 | A's `Receipt` plus C's `reconcile()`; drop B's interrupt op |
| C-030 | merge | 0.55 | Same as X-019 |
| C-031 | B | 0.65 | Ranked hypotheses give a worker-side fix order; the ack protocol bounds cost regardless |
| C-032 | B | 0.6 | The acked-whole-batch secondary hypothesis is testable and fixed by FR-012 |
| C-033 | A | 0.75 | Restart with the person's authorization in v1; no interrupt |
| C-034 | merge | 0.6 | B's text, sent only at an identified prompt (C) via `--wait-submit` |
| C-035 | merge | 0.55 | Surface verbatim (A/B) with C's bounded raw evidence and poison-input tolerance |
| C-036 | A | 0.75 | Report at 10 min; never auto-restart |
| C-037 | C | 0.75 | Transactional ledger, persist before ack, fail closed |
| C-038 | merge | 0.6 | B's degraded mode, A's porting checklist, C's no-terminal fixture |
| C-039 | merge | 0.6 | None budgets it; add an explicit per-sweep output cap |
| C-040 | merge | 0.5 | State the assumption and measure it in the replay fixtures |
| C-041 | B | 0.55 | `queued` disposition plus counting from the next checkpoint |
| C-042 | merge | 0.55 | `agentWait` primary with a screen backup past W |
| C-043 | B | 0.6 | Body-line authority makes v1 independent of payload transport |
| C-044 | C | 0.6 | Requires a durable final-turn boundary; two reads S apart |
| C-045 | C | 0.7 | Monotonic coordinator receipt time |
| C-046 | C | 0.65 | Automatic restart only through a verified resume interface |
| C-047 | C | 0.7 | Controller lock, not an assumption |
| S-005 | merge | 0.6 | A's named schemas, C's field bounds, B's minimal v1 fallback |
| S-006 | B | 0.75 | Occurrence cause vs detection cause with confidence per case |
| S-007 | B | 0.6 | The C-1..C-14 table with v1/v2 and constraint columns is the most checkable layout |
| S-008 | C | 0.75 | Dedicated durability, input-safety and rollout NFRs |
| S-010 | B | 0.55 | Unreachable and exited differ in proof status (exited is an Orca stall proof, unreachable is not), so they deserve separate states |

Counts across the 73 positions: A 13, B 27, C 11, merge 22.
