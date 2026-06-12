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

Default `<output-dir>` = `/config/workspace/IronClaude/.dev/pr-monitor/pr-<N>-<YYYYMMDDHHMMSS>/`
unless `--resume` supplies an existing log dir.

### The 33 event types (§11.3 + §12.1)

The closed `EventType` enum has EXACTLY 33 members — the 32 from §11.3 plus
`push_aborted_or_not_landed` (§12.1, the crash-window not-landed branch):
`run_started`, `environment_check`, `pr_create_attempted`, `pr_created`, `monitor_armed`,
`baseline_captured`, `poll_attempt`, `poll_result`, `api_backoff`, `classifier_unknown_shape`,
`review_detected`, `findings_normalized`, `finding_verified`, `finding_unverified`,
`round_incremented`, `route_decision`, `troubleshoot_started`, `troubleshoot_completed`,
`fix_applied`, `validation_started`, `validation_completed`, `push_decision`, `push_initiated`,
`push_completed`, `reply_posted`, `thread_resolved`, `idempotency_skip`, `terminal_clean`,
`terminal_timeout`, `terminal_max_rounds`, `terminal_halted`, `terminal_failed`,
`push_aborted_or_not_landed`.

Each line carries `schema_version`, a unique+monotonic `event_id`, `event_type`, `timestamp`,
`run_id`, `pr{repo,number,url,base,head}`, `state_before`, `state_after`,
`round_index`/`round_counter`, and `payload`.

### The 5 idempotency sets (§11.4)

Maintained in materialized state; an `idempotency_skip` event is appended when an action is skipped:

- `processed_review_ids` — prevents re-processing the same review emission.
- `processed_finding_ids` — **keyed on `fix_key = sha256(path + line + finding_body)`**
  (comment_id-INDEPENDENT, per INV-009); prevents applying a fix twice (a fresh `comment_id` with the
  same `path+line+body` hashes to the same `fix_key` → `idempotency_skip`).
- `replied_comment_ids` — prevents duplicate thread replies (thread-scoped `reply_key`).
- `resolved_thread_ids` — prevents duplicate resolution calls.
- `pushed_commit_shas` — the SHA set INV-001 attributes re-reviews against.
