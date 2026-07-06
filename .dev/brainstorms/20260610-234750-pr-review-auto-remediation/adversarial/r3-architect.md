---
artifact: adversarial-round-3-resolution
role: architect
round: 3
topic: "PR Review Auto-Remediation Monitor (V1.0)"
created: 2026-06-11
owns: [INV-001, INV-016]
flags: [INV-007, INV-009]
---

# Round 3 — Architect Normative Resolution (FSM/seam invariants)

Final resolution for the two HIGH FSM/seam invariants the probe blocked on. Each
section gives the SINGLE NORMATIVE SENTENCE the merge adopts verbatim, the rationale,
and the re-derived fence-posts. I own INV-001 and INV-016; I flag constraints for
INV-007 and INV-009 (backend owns those next).

---

## INV-001 — The counter has ONE definition: completed, push-attributed cycles

### Root-cause restatement

The probe is correct that consensus #1 fused two non-equivalent variables: B's
"increment BEFORE diagnosis on the inbound review" (counts *reviews observed*) and C's
"increment AFTER fix→push→re-review" (counts *completed cycles*). They agree on
happy-path push count (INV-003) but disagree on every non-happy boundary because B's
counter ticks on a **transient detection event** (a review that can later vanish,
INV-014) while C's ticks on an **observable, durable side effect** (a re-review we
provably caused). The off-by-one re-enters through the seam between them. We must pick
the timing that makes the increment **attributable and un-revocable**.

### NORMATIVE RESOLUTION (adopt verbatim)

> **INV-001.** `round_counter` is the count of **completed monitor-triggered
> remediation cycles**. A cycle completes — and `round_counter` increments by exactly
> 1 — at the single FSM transition where a re-review is observed AND that re-review is
> SHA-attributed to a push this run recorded (its `pushed_commit_shas` set). The
> counter increments **nowhere else**: not on inbound-review detection, not on
> diagnosis start, not on push emission, not on validation retry. The loop-guard gate
> is evaluated **before** opening each fix cycle as `round_counter >= max_rounds ⇒
> HALT_MAX_ROUNDS`; the user-facing label is `round_counter + 1` ("remediation round N
> of max M"). A counted re-review that is later observed to vanish does NOT decrement
> the counter (increments are monotonic and irrevocable).

### Re-derivation under this single definition

**(a) Exact increment point in the FSM transition table.**
There is exactly one incrementing edge:

```
S5_AWAITING_REREVIEW --[review_observed ∧ sha_attributed_to_our_push]--> S2_CLASSIFY
        side effect on this edge ONLY:  round_counter += 1  (write-ahead journaled)
```

No other transition touches `round_counter`. Push emission (`S4_PUSHING →
S5_AWAITING_REREVIEW`) does NOT increment; validation-failure self-loop in
`S4_PUSHING` does NOT increment (governed by the separate `validation_retry` cap,
INV-017); inbound-review detection at arm (`S2_CLASSIFY`) does NOT increment.

**(b) What a "round" counts.** A round = one COMPLETED cycle (fix → push →
*our-push-attributed* re-review). It counts cycles, NOT reviews. The very first
inbound review that arms the monitor is round 0 (zero cycles completed); it triggers
fix/push #1 but is itself never counted.

**(c) The gate predicate.** `round_counter >= max_rounds` evaluated at the
`S2_CLASSIFY → S3_DIAGNOSE` edge (i.e. before committing the NEXT fix cycle). `>=`
not `>` is load-bearing (C T-626 proves `>` pushes 3 at max_rounds=2).

**(d) Behavior when a counted review later vanishes (closes INV-014).** Irrevocable.
Once a re-review is SHA-attributed and the counter ticks, a subsequent poll showing
that review gone does NOT decrement and does NOT refund the round. Rationale: the
increment is bound to *our push having provably caused a re-review*, which already
happened; the review's later disappearance (Augment dismissed it, force-push, etc.)
cannot un-happen the cycle. This makes the budget strictly non-refundable and
therefore un-gameable into an infinite loop. (Under the rejected B-timing this
boundary was ambiguous; under INV-001 it is determinate.)

**(e) max_rounds push counts.**
- `max_rounds=2`: counter 0 → gate `0>=2` F → push#1 → attributed re-review → counter 1 → gate `1>=2` F → push#2 → attributed re-review → counter 2 → gate `2>=2` T → HALT. **2 pushes.**
- `max_rounds=1`: counter 0 → gate `0>=1` F → push#1 → attributed re-review → counter 1 → gate `1>=1` T → HALT. **1 push.**
- `max_rounds=0`: gate `0>=0` T at the first fix-cycle edge → HALT before any fix. **0 pushes** (report-only; arm-time WARN if ordinal>=2 per INV-005 compromise).

Push count equals `max_rounds` in every case — the property the whole feature exists
to guarantee, now provable from a single increment edge.

---

## INV-016 — G-push is a real runtime conjunction, not a bare ordinal

### Root-cause restatement

The probe is correct: `ordinal >= 3` is the level the operator already selected, not a
safety layer; calling it "opt-in default-off" overstates it. "Opt-in" must be promoted
from a config default to a runtime gate with concrete, independently-falsifiable
predicates AND a mandatory audit record.

### NORMATIVE RESOLUTION (adopt verbatim)

> **INV-016.** A push is authorized at the `S4_PUSHING` transition if and only if ALL
> of the following runtime predicates hold, evaluated as a conjunction immediately
> before `git push`: (1) `monitor_ordinal >= 3`; (2) `validation_status == "validated"`
> (targeted tests + lint + format all green this cycle); (3) `needs_human_decision ==
> false` for every finding in the cycle; (4) `round_counter < max_rounds`; (5) the
> cycle produced at least one grounded, applied edit (`applied_edits > 0` — never push
> an empty or ungroundable-only cycle). If any predicate is false the FSM routes to
> `HALT_*` (HALT_HUMAN for (3), HALT_MAX_ROUNDS for (4), TERMINAL_CLEAN/report for
> (5), report-only for (1)–(2)) and NO push occurs. Every push, authorized or
> blocked, writes a **write-ahead `push_decision` audit record** to the run-log
> naming which predicates held; this record is mandatory at L3 and is the audit
> primitive (not a per-push interactive prompt). A one-time per-run confirmation
> applies: the FIRST push of a run requires `--yes` OR an interactive confirm unless
> the run is non-interactive, in which case the `push_decision` record + the explicit
> `--monitor 3` arming stands as the recorded authorization.

### Why this makes "opt-in" real

- The push is now a **5-way conjunction of runtime state**, any one of which blocks it
  — not a single static ordinal. (1) is necessary but explicitly NOT sufficient.
- Predicate (5) (`applied_edits > 0`) is new and closes the "push/announce-resolved
  with nothing actually changed" hole that INV-009's reply-without-fix could otherwise
  feed (see flag below).
- The mandatory `push_decision` write-ahead record is the real safety layer: every
  auto-push is auditable and, combined with INV-015's honest posture, the spec states
  "validation authorizes a push within this gated envelope; it is NOT a correctness
  guarantee." The first-push confirmation gives a human a single real veto point
  without requiring per-push prompts that would defeat unattended operation.

---

## Constraints my counter definition imposes on backend's INV-007 / INV-009

**INV-007 (write-ahead push/log ordering).** INV-001 ties the *increment* to
SHA-attribution, so backend MUST journal the push **intent + target SHA** in a
write-ahead `push_initiated` record BEFORE `git push`, and `push_completed` after.
Constraint: `round_counter` may increment ONLY against a re-review whose SHA matches a
recorded `push_initiated.target_sha`. This means the idempotency token backend designs
must be the **pre-push SHA**, not the post-hoc `push_completed` SHA — otherwise a
crash in the push→log window (the probe's hole) leaves a re-review that attributes to
nothing and either strands or double-counts. Write-ahead the SHA, and resume can match
re-reviews to it deterministically.

**INV-009 (dedup vs unstable comment_id).** INV-016 predicate (5) `applied_edits > 0`
constrains the reply path: a reply/resolve may be posted on a fresh comment_id thread
(correct — new thread needs a reply), but it MUST carry the cycle's
`applied_edits`/`finding_dropped` status so a reply is never phrased "resolved" when
`applied_edits == 0` for that defect. Constraint on backend's fix-dedup key: because
INV-001 counts cycles (not findings) and INV-016 requires `applied_edits > 0`, the
fix-dedup hash MUST be comment_id-INDEPENDENT (finding body + file:line), so a fresh
comment_id on re-review does not defeat fix-dedup and silently burn a cycle on an
already-fixed defect.
