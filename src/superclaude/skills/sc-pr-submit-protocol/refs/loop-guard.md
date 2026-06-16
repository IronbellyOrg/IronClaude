# Loop Guard (LG) — INV-001 round-counter + the §11 run-log schema

This ref pins the round-counter invariants (INV-001) and the write-ahead JSONL run-log schema (§11).
The loop-guard fence-post is the spec's named **P0 defect surface**: an off-by-one here is a P0 bug.

> **Core purity (NFR-6 / AC-9, T-N50).** This file and `loop_guard.py` contain ZERO shell or
> version-control command tokens. The round counter and the gate are pure arithmetic over already-
> observed events.

## INV-001 — round-counter (verbatim normative)

> `round_counter` = the count of **completed monitor-triggered remediation cycles**; increments by
> exactly 1 at the single FSM transition
> `S5_AWAITING_REREVIEW --[review_observed ∧ sha_attributed_to_our_push]--> S2_CLASSIFY`; increments
> **nowhere else** (not on inbound-review detection, diagnosis start, push emission, or validation
> retry); monotonic — a counted re-review that later vanishes does NOT decrement; gate
> `round_counter >= max_rounds ⇒ HALT_MAX_ROUNDS` evaluated before opening each fix cycle;
> user-facing label = `round_counter + 1`; `max_rounds=N` → exactly N pushes. Default 2, hard cap 5.

Load-bearing consequences:

- **The single increment site** is the `S5_AWAITING_REREVIEW → S2_CLASSIFY` edge, gated on
  `review_observed AND sha_attributed_to_our_push`. No other transition touches the counter.
- **The gate uses `>=`** (INV-5), NOT `>`. At `max_rounds=2` the counter reaches exactly 2 and exactly
  2 pushes occur (T-626 — the canonical off-by-one test).
- **Monotonic / irrevocable** (INV-4): a counted re-review that later vanishes does NOT decrement
  (T-VANISHED-MONO).
- **User-facing label** = `round_counter + 1` (so the first cycle reads as "round 1").

## INV-R1 / INV-R2 / INV-R3 — V1.1 re-trigger + fallback (verbatim normative)

V1.1 layers two re-review/fallback behaviors on top of INV-001 WITHOUT changing it. INV-001's edge,
its `>=` gate, monotonicity, and `max_rounds=N ⇒ N pushes` are PRESERVED verbatim; V1.1 only RELOCATES
the increment site (from an optimistic post-resolve tick to the real attributed re-review observed
AFTER the S5a re-trigger). The two counters below are INDEPENDENT and neither can re-open the other's loop.

> **INV-R1 (re-trigger boundedness).** A re-trigger comment is emitted at most once per
> completed push cycle, on the `RESOLVING → S5a_RETRIGGER_REVIEW` edge, and only when
> `applied_edits > 0`. `rereview_request_count` is monotonic and
> `rereview_request_count <= max_rounds`. The re-trigger does **not** itself increment
> `round_counter`; INV-001's edge and gate are unchanged.
>
> **INV-R2 (auggie strict-once + total-push bound).** `/sc:auggie-review` is invoked **at
> most once per PR**, guarded by the durable `auggie_review_invoked` idempotency set
> (comment-independent, survives resume). The fallback contributes **at most one** push.
> Consequently `push_count <= max_rounds + 1` for the whole run.
>
> **INV-R3 (clamp monotonicity / deterministic termination).** On fallback engage
> `effective_max_rounds := min(effective_max_rounds, 1)` — a one-way, monotone
> non-increasing clamp recorded once. The fallback sub-loop (`fallback_round_counter`,
> cap 1, no loop-back, no auggie re-invoke) guarantees termination structurally, not merely
> by budget. INV-001's monotonic `round_counter` and its `>=` HALT gate are preserved
> verbatim; the two counters are **independent** and neither can re-open the other's loop.

- **`fallback_round_counter` is a SEPARATE counter** from `round_counter`, with its own increment site
  (the single fallback remediation cycle) and the strict-once cap-1 clamp (`should_halt(fallback_round_counter, 1)`
  halts after one fallback cycle). `round_counter` is FROZEN at fallback entry — the fallback advances
  only `fallback_round_counter`. The clamp is recorded once via the `max_rounds_clamped` event (the
  run-log monotone-min fold guarantees a later higher value never raises it back).

## §11 — Run-log schema (the write-ahead JSONL substrate)

### Authority (§11.1)

The append-only `monitor-run-<PR>.jsonl` is **authoritative**; `state.snapshot.json` is a
materialized cache. On disagreement, **rebuild from the JSONL** (NFR-6). Every external action is
preceded by a **write-ahead** record fsynced BEFORE the side effect.

### The 5 file locations (§11.2)

```text
<output-dir>/monitor-run-<PR_NUMBER>.jsonl   # authoritative append-only event log
<output-dir>/state.snapshot.json             # materialized cache (rebuildable)
<output-dir>/findings.latest.json            # latest normalized finding set
<output-dir>/validation/round-<N>/           # per-round stdout/stderr + exit codes
<output-dir>/troubleshoot/round-<N>/         # per-round troubleshoot prompts/outputs
```

Default `<output-dir>` = `<repo-root>/.dev/pr-monitor/pr-<N>-<YYYYMMDDHHMMSS>/` (cwd-relative; the
repo the operator runs `sc:pr-submit` from) unless `--resume` supplies an existing log dir.

### The 37 event types (§11.3 + §12.1 + V1.1 §6.1)

The closed `EventType` enum has EXACTLY 37 members — the 32 from §11.3 plus
`push_aborted_or_not_landed` (§12.1, the crash-window not-landed branch) — the 33 prior — plus the 4
V1.1 re-review/fallback events (`rereview_requested`, `decline_detected`, `auggie_fallback_invoked`,
`max_rounds_clamped`; addendum §6.1):
`run_started`, `environment_check`, `pr_create_attempted`, `pr_created`, `monitor_armed`,
`baseline_captured`, `poll_attempt`, `poll_result`, `api_backoff`, `classifier_unknown_shape`,
`review_detected`, `findings_normalized`, `finding_verified`, `finding_unverified`,
`round_incremented`, `route_decision`, `troubleshoot_started`, `troubleshoot_completed`,
`fix_applied`, `validation_started`, `validation_completed`, `push_decision`, `push_initiated`,
`push_completed`, `reply_posted`, `thread_resolved`, `idempotency_skip`, `terminal_clean`,
`terminal_timeout`, `terminal_max_rounds`, `terminal_halted`, `terminal_failed`,
`push_aborted_or_not_landed`, `rereview_requested`, `decline_detected`, `auggie_fallback_invoked`,
`max_rounds_clamped`.

Each line carries `schema_version`, a unique+monotonic `event_id`, `event_type`, `timestamp`,
`run_id`, `pr{repo,number,url,base,head}`, `state_before`, `state_after`,
`round_index`/`round_counter`, and `payload`.

> **Producer side of the 4 V1.1 events (NFR-6 boundary).** Per NFR-6 the deterministic core
> (`fsm.py`/`run_skill`) DECIDES but does not write the run-log — it imports no `run_log` and emits no
> events (exactly as it does not emit `round_incremented`/`push_completed` in V1.0). The SKILL's
> orchestration is the PRODUCER that appends these events as its waves act, so the §6.3 rebuild folds
> have a source: **S5a re-trigger (Wave 6, `applied_edits > 0`) → `rereview_requested`** (folded into
> `rereview_request_count`, INV-R1); **`declined` classification → `decline_detected`**; **fallback
> engage (Wave 6b) → `auggie_fallback_invoked{pr_number}`** (folded into the durable
> `auggie_review_invoked` set, INV-R2) **and `max_rounds_clamped{effective_max_rounds}`** (monotone-min
> fold, INV-R3). The SHA-attribution that resolves a re-review to `"attributed"` (gating the relocated
> INV-001 increment) is likewise a poll-side decision (`refs/review-retrigger.md` §3: re-review SHA
> matches `pushed_commit_shas`, newer than the watermark) surfaced to the core as the resolved outcome
> token — not computed inside the pure FSM.

### The 6 idempotency sets (§11.4 + V1.1 §6.3)

Maintained in materialized state; an `idempotency_skip` event is appended when an action is skipped:

- `processed_review_ids` — prevents re-processing the same review emission.
- `processed_finding_ids` — **keyed on `fix_key = sha256(path + line + finding_body)`**
  (comment_id-INDEPENDENT, per INV-009); prevents applying a fix twice (a fresh `comment_id` with the
  same `path+line+body` hashes to the same `fix_key` → `idempotency_skip`).
- `replied_comment_ids` — prevents duplicate thread replies (thread-scoped `reply_key`).
- `resolved_thread_ids` — prevents duplicate resolution calls.
- `pushed_commit_shas` — the SHA set INV-001 attributes re-reviews against.
- `auggie_review_invoked` — **keyed on `pr_number`** (comment-independent, survives resume); the durable
  INV-R2 strict-once gate that guarantees `/sc:auggie-review` is invoked at most once per PR.
