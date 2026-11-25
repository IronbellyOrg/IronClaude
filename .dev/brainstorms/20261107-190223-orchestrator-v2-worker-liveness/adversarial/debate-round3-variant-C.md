# Round 3 — Variant C Final Arguments

## 1. Final Position

Adopt a merge: A's observation tiers, B's status-body acknowledgement and small v1 handoff, and C's recovery gates.
Keep the five-minute due sweep, all-nine-type wake set, whole-batch inspection and bounded unknown-type reporting.
A heartbeat proves traffic, not useful work; fresh transcript entries do not prove useful work either.
Add explicit heartbeat-only observation, answered-ask-still-blocked and assignment-invalidated incidents now.
Unknown evidence must produce a bounded report, never an invented exact diagnosis or permission to restart.
Keep the input veto even when it prevents the terminal-copy remedy requested by the seed; document that safety exception.
Accept B's two replacements per rolling six hours and two per lineage, with two automatic nudges per lineage.
V1 adds duties and manual records; v2 adds durable timers, reconciliation and tested identity-aware adapters, not new stop authority.
All three HIGH resolutions below are accepted as proposed design changes, not claims that the runtime already implements them.

## 2. Resolution of HIGH items

Citation aliases (each denotes the absolute file, not an external authority):
- **Contract** = `/home/coder/workspaces/IronClaude/src/superclaude/core/WORKER-CONTRACT.md`.
- **Seed** = `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261107-190223-orchestrator-v2-worker-liveness/seed-brief.md`.
- **Probe** = `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261107-190223-orchestrator-v2-worker-liveness/adversarial/invariant-probe.md`.

All timing below is a design target while the coordinator and required probes are available. V1 policy is not a machine-enforced service guarantee. An unavailable probe must be reported as such by the next due sweep; it cannot silently count as healthy evidence.

### INV-005 — Heartbeats and a fresh transcript can conceal thrashing

**Proposed v1 resolution.** Add this coordinator duty alongside WC-10:

> Maintain separate last-traffic and last-corroborated-useful-progress observations. On every five-minute due sweep, inspect whether useful progress has actually been established. Heartbeats, byte growth, compaction entries and generic status repetition never renew useful progress. If useful progress has not been established for ten minutes, perform a bounded screen read as well as the available transcript probe, even when both traffic and transcript timestamps are fresh. With no conformant progress payload, use this same fallback; do not disable the timer. Repeat the screen observation on the next sweep if needed, and record/report the result no later than fifteen minutes from the last established useful progress, or dispatch if none exists.

The screen observation records explicit context-limit/compaction failure evidence and whether compaction is repeatedly occurring without a completed useful unit. It is not a single-literal match for one historical banner. Explicit failure evidence can establish `context-exhausted`; repeated compaction without corroborated progress establishes `thrash-suspected`. If the screen is unrecognized, missing or ambiguous, record `progress-unverified / thrash-not-excluded` and report, rather than `advancing`. A known long-running tool is recorded as such; it is not labelled thrashing from lack of output. The fixed read-only fallback still runs during declared windows. A first probe can report suspicion immediately; a second sample refines it, not delays the report past the target.

The response is L1 observation, then L5 report with evidence and a resume-plan draft where appropriate. No heartbeat-only or compaction-only condition supplies L4 proof. Changing banner wording can reduce diagnostic precision, but cannot leave the worker indefinitely classified as advancing. Exact thrash recognition on every harness remains unavailable; the portable guarantee is bounded disclosure of missing progress evidence, not a false promise of exact classification.

**Bucket and rules.** V1: amend WC-10 and add a coordinator “progress-unverified fallback” duty; no command-side Orca calls, cadence changes or required JSON payload. V2: independent timer, semantic-progress validation and versioned compaction classifiers with replay fixtures. Progress schema, compaction-event format, classifier accuracy and worst-case scheduling are **UNVERIFIED**. Screen/transcript reader availability is **documented**, not runtime-tested here; a harness without either takes the bounded degraded-report path.

**Evidence.** Probe:11 identifies the fresh-tail/payload-absent hole and missing screen fallback. Seed:65 documents that no semantic counter is native; Seed:68 marks attention-category coverage unknown; Seed:70 documents the screen/transcript readers; Seed:75 lists missing detection machinery. Contract:44 permits accepted long-tool gaps and forbids treating absence as death. These sources justify the fallback and its limits, not an existing detector.

**Acceptance example.** Heartbeats and transcript entries continue for twenty minutes, with no payload and a changed banner. By fifteen minutes the record must contain screen evidence and either a supported thrash diagnosis or a degraded progress-unverified report. It must not say advancing merely because timestamps changed, and must not restart.

### INV-020 — An answer is enqueued but the original ask remains blocked

**Proposed v1 resolution.** Name a distinct incident, `answered-ask-still-blocked`, keyed by Task, Dispatch, original question ID and answer identity. Record the first confirmed enqueue time once. Enqueue success is not a read receipt. At two minutes it becomes probe-due; the first five-minute due sweep after that threshold performs L1 correlation. If a current observation shows the same original ask still blocked, record this incident. If that observation cannot establish ask identity/state, record `answer-read-unknown / ask-state-unverified` instead. In either case report the unresolved incident by ten minutes from first enqueue; do not wait for repeated ask timeout loops or reset age when the same question resumes.

L1 checks the question/answer target correlation, the known send result and the current worker's waiting state using available documented observations. A send timeout means enqueue-unknown, not “not sent”; do not blindly resend an answer with uncertain delivery. Where the original send is known not to have enqueued, correct its target and answer the same question through the documented preamble route. A confirmed enqueue followed by a blocked ask goes to L5 with the original IDs and evidence, requesting person-side inspection of the ask/transport. No new question, no typed answer into a running ask, no induced interrupt, and no automatic restart. A person-directed recovery uses the settlement branch below only after the old attempt is actually quiescent.

After the ask returns, the worker sends the proposed status-body acknowledgement at its first legal reporting opportunity, naming the original question and answer and a disposition such as queued or applied. Reading and applying are separate facts. Close an unresolved acknowledgement as unacked-at-settlement when the attempt settles; never escalate that old incident against the replacement. For an independently confirmed idle empty prompt, a typed copy remains a separate conditional remedy with the same answer identity; prompt-binding/queue safety must be established, not inferred from ack age. If it is not established, report rather than type.

**Bucket and rules.** V1: amend WC-3 and WC-12 with legal-opportunity read acknowledgements; add the coordinator's bounded answered-ask anomaly duty; retain the no-emission-in-wait rule and independent input veto. V2: durable identity/digest tracking, ask-state adapter and reconciliation of uncertain sends. The status-body convention, runtime worker compliance, precise ask-state visibility, prompt binding and delivery reconciliation are **UNVERIFIED**. Durable enqueue versus read-receipt distinction and terminal-only turn-start receipt are **documented**. A turn-start receipt never closes the read-confirmation incident by itself.

**Evidence.** Probe:26 identifies the unbounded answered-but-blocked state. Contract:53-56 requires the same eligible ask/re-invocation and the same question ID after timeout; Contract:61 prohibits heartbeats during blocking waits; Contract:59 makes follow-ups pull-based. Seed:67 documents no sender read receipt and distinguishes enqueue from turn start. Thus legal waiting is not worker misconduct, but an already-answered ask remaining unresolved is now a named transport/consumption anomaly.

**Acceptance example.** An answer is confirmed enqueued at t=0; the same ask remains blocked and no acknowledgement can be sent. By t=10 the incident is reported with unchanged original age and question identity, with no typing or duplicate ask. This explicitly narrows Seed's terminal-copy requirement for unsafe-input cases; it does not pretend a safe automatic remedy exists for every mechanism.

### INV-023 — A person or harness clears the session in place

**Proposed v1 resolution.** Amend Terms, WC-5, WC-7 and WC-6 with an assignment-invalidation procedure:

> A clear or reset that removes the current live preamble ends that session's authority to act as the old worker. The cleared session must not resume lifecycle sends using IDs reconstructed from disk or chat. A normal compaction does not itself invalidate the assignment if the live assignment remains valid; if its continuity is uncertain, pause worker actions and report identity-unverified. Never clear a worker in place as an automatic recovery action.

When a person reports an in-place clear, or the coordinator obtains reliable reset evidence, record `assignment-invalidated` against the old Task/Dispatch, preserve reports/checkpoints, and stop admitting results or follow-up work from that identity. A statement in the person's own coordinator conversation identifying the affected attempt is acceptable manual evidence; another worker's assertion or a new file alone is not. If a reset is merely suspected, report unknown and do not settle on that suspicion. V1 has no documented automatic reset detector, so this procedure depends on disclosure or observable evidence; no bounded invisible-reset detection claim is made.

Separate the two settlement paths explicitly:
1. If the old worker process has exited and Orca reports positive exit proof, use existing WC-6. It does not matter whether the person caused that exit.
2. If the terminal/process remains live after a clear or person interruption, add a **new explicit WC-6 person-directed cancellation exception**, not a new Orca stall-proof class: the person, in their own conversation, identifies the old Task/Dispatch, confirms that its command and any subordinate writers have stopped, and directs its cancellation. The coordinator records that instruction and independently checks available quiescence evidence; uncertainty about running work blocks replacement. Then it records the old Task as failed/cancelled using the supported settlement route, confirms settlement, and only then creates a new Task. If the runtime refuses settlement of that live identity, or its effect is ambiguous, the person must complete settlement; the coordinator does not invent a bypass.

A clear alone is not proof that all tool processes stopped and is not automatic Task settlement. Record it as person/reset-invalidated first, then settle-by-person only through the explicit exception. The replacement receives a fresh dispatch preamble, a new report directory and a resume note pointing to preserved files; it remains in the original lineage with consumed budgets intact. Preserve all frozen-plan/Ruling restrictions. Never manufacture worker_done for the cleared session. Late lifecycle messages from the invalidated identity are quarantined for admission; if Orca has already accepted one and changed Task state, stop dependents and report the discrepancy rather than assuming local quarantine undoes that remote effect.

**Bucket and rules.** V1: Terms live-preamble validity, WC-5/WC-7 authority after reset, and the narrowly scoped WC-6 person-cancellation exception plus coordinator recovery procedure. V2: tested reset/compaction events, identity continuity checks, fencing and durable reconciliation. Those detectors, transport enforcement of invalidated identities, live-identity cancellation compatibility and subordinate-writer quiescence detection are **UNVERIFIED** release gates. Current new-Task retry/settlement rules and exit proof are **documented**; the person exception is proposed amendment text, not present permission.

**Evidence.** Probe:29 identifies the cleared-session violation and missing settlement; Probe:30 distinguishes process exit from a live PTY. Contract:11 and :16 bind worker/guard authority to the live preamble; Contract:57-58 binds completion and lifecycle ownership; Contract:69-73 requires a new Task and prior settlement. Seed:71 documents exit as existing positive proof. The probe's proposed “settled-by-person” label therefore needs the explicit quiescence/settlement steps above, not a bare clear-to-settled transition.

**Acceptance example.** A person clears a session while its terminal remains live. The new ordinary session sends no old lifecycle messages. The old Task stays blocked from replacement until the person's explicit cancellation, confirmed cessation of old writers and confirmed settlement; the next worker is a new Task/Dispatch, not a continuation using remembered IDs. A routine compaction preserving valid assignment identity does not spuriously cancel work.

## 3. Responses to the other 8 MEDIUM/LOW UNADDRESSED items

- **INV-001 — Accept fix:** after coordinator clear/compaction/resume, re-read run notes before any intervention; recover pending answers, latches, lineage and consumed budgets, and stop automatic actions if records are missing or inconsistent; v2 adds durable reconciliation.
- **INV-006 — Accept fix:** delete timeout-to-idle; retain pending-ask state through same-ID timeout/resume until a positive return, settlement or invalidation observation, with input veto on ambiguity.
- **INV-009 — Accept fix:** declare timestamp/finality capability explicitly; when stripped, use coordinator receipt times and spaced screen samples only for observation-duration claims, never reconstructed inactivity onset or final-turn proof; unavailable exact evidence yields a degraded report.
- **INV-010 — Accept fix:** all caps are conjunctive, earliest denial wins; reserve a replacement budget slot before each successor launch, including failed starts, retain ambiguous reservations until reconciled, and never reset totals on a new Task; guard-fix, unchanged-start and nudge limits remain additional ceilings.
- **INV-011 — Accept fix:** allocate a root lineage ID before first dispatch and record every predecessor; resume-note/report-path churn never creates a new lineage, and extend the unchanged-start comparison to ignore coordinator-only recovery metadata, not genuine command/answer changes; missing lineage means no automatic retry.
- **INV-016 — Accept fix:** on a failed fleet observation, or majority simultaneous unreachability with shared-endpoint errors, open one infrastructure incident, suspend per-worker typing/replacement and aggregate reports; after host/clock recovery reconcile immediately without resetting budgets or firing a backlog of actions.
- **INV-022 — Accept fix:** make pre-command silence declarations optional and coarse; unexpected internal fan-out is accepted without a declaration, commands gain no Orca calls, and fixed read-only probes plus WC-10 protect the gap.
- **INV-024 — Accept fix:** a person-caused process exit already follows existing positive-proof WC-6; only live-terminal interruption/reset needs the new explicit person-cancellation exception, with confirmed old-writer cessation and settlement before retry.

## 4. Final per-point positions

Only unresolved Round 2 predicates or numerical policies are listed. Earlier agreement claims do not settle a predicate another response explicitly left open. Confidence concerns the design choice, not measured runtime capability.

| Point | Final winner (A/B/C/merge) | Confidence % | One-line reason |
|---|---|---|---|---|
| C-003 | merge | 96 | Latch exhaustion until verified useful post-incident work or explicit person disposition; preserve contrary evidence and history. |
| X-007 | merge | 96 | A counter plus a changed artifact is necessary corroboration in that profile, not sufficient semantic progress. |
| C-005 | merge | 97 | Claims require completed-unit corroboration; payload absence triggers the screen/degraded fallback, not an advancing verdict. |
| C-011 | merge | 97 | Prefer a current capable transcript, but screen evidence and unknown fallbacks remain independent; no universal transcript authority. |
| C-018 | merge | 95 | Choose two automatic nudges per lineage with per-incident tracking; a new Task never replenishes the budget. |
| C-019 | B | 92 | Adopt two automatic replacements per rolling six hours and two per lineage, a conservative policy rather than an optimality claim. |
| X-012 | B | 92 | Same replacement ceiling; all stricter failed-start, guard-fix, authority and uncertainty gates still apply. |
| X-003 | C | 99 | Two unchanged reads never supply the missing fact that the assigned agent's final turn actually completed. |
| C-044 | C | 99 | Require positive assignment-bound completed-final-turn evidence; otherwise proof remains none. |
| C-045 | C | 98 | Persist clock-domain identity and reconcile after reboot/resume; raw persisted monotonic values are not portable elapsed time. |
| X-006 | merge | 97 | Finished-unreported needs the final outcome, no remaining command and no eligible ask/re-invocation; mtime alone proves no answer consumption. |
| C-015 | merge | 98 | Preserve enqueue age and add answered-ask-still-blocked; ack age never grants input ownership or restart authority. |
| X-009 | merge | 98 | Legal-opportunity status acknowledges reading/queuing; blocking waits need bounded unknown/anomaly reporting, not impossible mandatory acks. |
| C-033 | merge | 97 | Exhaustion goes to a ready person plan; in-place reset uses explicit invalidation and confirmed settlement, never implicit continuation. |
| X-013 | merge | 97 | Keep the fifteen-minute available-evidence default; tighter v2 latency remains optional and requires end-to-end capacity evidence. |

**Points now accepting another variant's position:** C-019 and X-012 accept B's restart window instead of C's one-hour window; C-011 accepts A/B's capable-transcript preference with explicit limits. Other rows retain or refine the merge/C positions rather than claiming new concessions.

**Final count:** 15 disputed point IDs finalized. All 3 HIGH items have accepted design resolutions, including explicit degraded-coverage and unsafe-input exceptions. These are C's final arguments for the merge, not a claim that A or B has already accepted this wording.

Design-only check: the output was stubbed first and filled in place; all eleven UNADDRESSED probe findings receive a disposition. No implementation, runtime tests, live-worker experiments, Git, GitHub or Orca calls were performed. The main remaining risk is unverified observation and cancellation capability; no automatic recovery may rely on it until tested.
