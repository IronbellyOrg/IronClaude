# Round 1 Statement — Advocate for Variant B (sonnet:backend)

## Position summary

Variant B should be the backbone of the final PR Review Auto-Remediation Monitor spec because it treats the monitor as a recoverable backend process, not merely an FSM sketch or a test matrix. Its defining thesis is explicit in Variant B: “Every externally visible action must be recoverable, idempotent, rate-limit safe, and auditable,” and V1 must “persist enough state to resume safely after session loss.” That is the reliability center of gravity for an unattended level-3 system that can commit, push, reply, and resolve review threads.

I would merge in Variant A’s hard detection-contract gate and Variant C’s fence-post tests, but neither replaces B’s durable process substrate: canonical states, write-ahead JSONL events, materialized snapshot cache, five idempotency sets, first-class `--resume`, explicit rate-limit/backoff rules, and 12 failure-mode recoveries.

## Steelman of Variant A before critique

Variant A’s strongest contribution is architectural boundary discipline. Its thesis says the feature is “not a script” but a “finite-state remediation reactor” and that the “single most consequential architectural decision” is a “hard seam” between unknown detection/parsing and deterministic state-machine/routing/loop-guard logic. That is exactly right: Augment’s emission shape is unknown, and guessing it inside parser code would be the highest-risk early failure.

Variant A also gets autonomy modeling right. It states there are “not four implementations,” only one FSM where the ordinal is checked at “exactly three transition gates” plus the `needs_human_decision` override. This avoids level-specific drift. Its detection-contract section is also stronger than B’s release-time wording: `locked:false` is a “hard stop,” the skill “refuses to arm,” and AC-8 proves the R1 dependency is mechanically enforced.

Finally, Variant A’s deterministic-core purity is valuable. It specifies that FSM/router/loop-guard contain “zero `gh`/`git` calls,” and adds static tests forbidding seam leakage. This should be retained.

### Critique of Variant A from backend/reliability lens

A’s run-log is underspecified for real recovery. It says RunLog is “also the resume checkpoint” and records `round` plus events, but the schema is only a minimal JSONL example with `ts`, `round`, `event`, `detail`, `state_from`, and `state_to`. It does not define event IDs, required event types, idempotency sets, snapshot conflict behavior, or crash-specific recovery paths. By contrast, B defines a JSONL event envelope with `schema_version`, `event_id`, `event_type`, `run_id`, PR identity, states, round index, and payload; defines 29 required event types; defines `state.snapshot.json` as a cache; and says if snapshot and JSONL disagree, “JSONL is authoritative.”

A also leaves several backend edge cases implicit: validation failure counter semantics are only “retry≤budget / HALT,” `--max-rounds=0` is undefined, ungroundable missing file:line findings are unspecified, and timeout basis is less precise than B’s “wall-clock elapsed time since entering `S3_WAITING_FOR_REVIEW` for the current review wait.”

## Steelman of Variant C before critique

Variant C’s strongest contribution is test rigor. It declares loop-guard off-by-one a P0 defect and provides a 90-test matrix. Its fence-post table is the clearest artifact for proving termination: T-626 explicitly asserts `round_counter == 2 NOT 3` and “no round 3 fix pushed” under `--max-rounds 2`. Its INV-6 explicitly states that validation failure does not increment the round counter, and QD-1 justifies that counting validation attempts would “waste round budget on self-inflicted failures.”

Variant C also captures race and edge conditions that backend specs often miss: review arrives during fix, timeout during remediation, multiple PRs in the same session, `gh` missing, review disappearance, malformed payloads, and non-Augment interleaving. Its tests for autonomy gates are concrete and adversarial, especially T-430 requiring L3 to halt with zero edits/pushes/replies on `needs_human_decision`.

### Critique of Variant C from backend/reliability lens

C is a verification harness more than an operational design. It says run-log observability is tested with valid JSONL assertions, but it does not provide B’s recovery schema, event envelope, materialized state, idempotency sets, or resume conflict rule. A test matrix can tell us a system is wrong; it cannot by itself make crash-after-push-before-reply safe.

C also takes an unsafe position on malformed or missing file:line findings: EC-9 says missing `file:line` means the “finding dropped per hallucination contract.” Dropping is too lossy for a monitor that must report residual risk. B’s position is safer: ungrounded findings “may still be reported” and “may not be auto-fixed at level 3 unless `/sc:troubleshoot` can ground them in a real file and the run-log records that grounding.” Backend reliability favors preserve-and-gate, not drop-and-forget.

C’s `--max-rounds=0` diagnostic semantics are user-friendly, but equating it to level 1 “regardless of `--monitor` value” is risky because it silently rewrites an explicit level-3 request into report-only behavior. B’s stricter rule is safer for mutation-bearing levels.

## Strengths claimed for Variant B with evidence

1. **Durable process substrate.** B defines the monitor as durable state reconstructed from a run-log: “The monitor maintains one durable `monitor_state` reconstructed from the run-log on startup and appended to after every transition.” It further requires every state transition append before starting work in the new state.

2. **Recovery-grade idempotency.** B tracks `processed_review_ids`, `processed_finding_ids`, `replied_comment_ids`, `resolved_thread_ids`, and `pushed_commit_shas`; it appends `idempotency_skip` when a duplicate action is skipped. This directly addresses duplicate polls, duplicate reviews, crash/resume, and operator re-arming.

3. **Write-ahead auditability.** B’s required event types include `route_decision` before troubleshoot, `validation_completed` before push, `push_completed`, `reply_posted`, and `thread_resolved`. Its NFR-5 requires every poll, classifier decision, route, validation command, push, reply, resolve, backoff, and terminal state be machine-readable.

4. **Crash-specific recovery.** B has explicit FM-6 “Crash after push before reply” and FM-7 “Crash after reply before resolve.” The recovery is precise: do not re-run fixes, do not duplicate replies, complete missing later actions only if validation and push evidence exist.

5. **Rate-limit correctness.** B classifies primary/secondary limits, HTTP 429, 5xx, and auth/config failures; backs off 30→60→120… capped at 300; honors `Retry-After`; resets after success; counts backoff against timeout; and refuses to sleep past the deadline.

6. **Fail-safe grounding.** B’s classifier refuses unknown bot identities, normalizes unknown severity to Medium, logs unknown emission shapes, and refuses level-3 auto-fix for missing path/line unless troubleshoot grounds it and the run-log records that grounding.

7. **Backend-operable resume.** B’s `--resume <absolute-run-log-path>` is a first-class command argument, and AC-16 requires rebuilding `state.snapshot.json` from JSONL when the snapshot is absent.

## Weaknesses in Variant B conceded honestly

1. **Detection contract should be hardened.** B says Augment identity “must be empirically captured before implementation is considered complete” and validated “before release,” but lacks A’s mechanical `locked:false` build/arm gate. This is a real weakness on C-001/X-004. Final spec should adopt A’s hard preflight/runtime refusal, backed by B’s centralized allowlist.

2. **Validation failure counter wording is ambiguous.** B says at level 3 one additional fix attempt may occur “only if `round_index < max_rounds`,” coupling validation retry to the round budget. C is clearer that validation failure does not consume a round. B should adopt C’s INV-6 while still limiting repeated validation retries with a separate retry counter.

3. **Test matrix is less exhaustive than C.** B has strong ACs and failure modes, but C’s T-620..T-629 and edge-case catalog are superior for proving loop-guard correctness. Final spec should import them.

4. **Autonomy as four declarative levels is less elegant than A’s ordinal-as-ceiling.** B’s FR-6.1..6.5 is clear, but A’s “one machine, four projections” reduces branch drift. Final spec should combine B’s 15 operational states with A’s gate model.

5. **Reply/resolve API is properly hedged but still unproven.** B’s FR-8.5 isolates endpoint differences in helper code, but the GitHub exact API path remains an assumption that requires fixture validation.

## Contested diff-point positions

### X-001 — `--max-rounds=0` semantics

**Winner: B.** Mutation-bearing levels should reject `0`. B states “Values below `1` are invalid when `--monitor 2` or `--monitor 3`; `--monitor 1` may accept `0` only if it is explicitly interpreted as diagnose/report with no remediation loop.” C’s diagnostic mode is useful, but “Equivalent to level 1 regardless of `--monitor` value” silently downgrades an explicit level-3 invocation. A is undefined.

### X-002 — Does validation failure consume a round?

**Winner: C, with B recovery controls.** C is clearest and safest: validation failure “does NOT increment `round_counter`” and retries are “within the same round.” B’s coupling of a correction attempt to `round_index < max_rounds` is less precise. Backend-safe final design should use C’s round semantics plus B’s separate `validation_history` and halt/failure events.

### X-003 — Reply dedup keying

**Winner: B.** B separates identities correctly: `processed_finding_ids` prevents duplicate fixes, while `replied_comment_ids` prevents duplicate replies and `resolved_thread_ids` prevents duplicate resolution. A only mentions replied `comment_id`s. C correctly says reply once per thread/comment, but its finding dedup by `file:line` + body hash is insufficient for crash recovery without B’s broader idempotency sets.

### X-004 — Detection contract: enforced build-gate vs advisory vs runtime HALT

**Winner: A.** B’s release-time validation is too weak. A’s `locked:false` hard stop, “skill refuses to arm,” and AC-8 make the unknown-boundary dependency enforceable. C’s runtime HALT is acceptable but less strong than A’s build/arm gate.

### X-005 — Round-counter start/indexing

**Winner: B.** B’s human-readable semantics are operationally clearer: Round 1 is the first post-arm actionable Augment review; Round 2 is the first re-review after the monitor’s push; a third actionable review under `--max-rounds 2` stops. A’s “initial review is round 0” is mathematically fine but exposes user-facing fence-post confusion. C mixes `round_counter starts at 0` with `round_counter == 2` after two zero-indexed rounds.

### X-006 — Where `needs_human_decision` is determined

**Winner: B.** B allows the classifier or troubleshoot to mark it and enumerates ambiguity domains: “API contract, security posture, user-facing behavior, or data migration decision.” That is reliable because ambiguity can be obvious during classification or emerge during diagnosis. A’s RoutedFinding-only placement is narrower; C’s troubleshoot-time fixtures are testable but incomplete.

### X-007 — Timeout clock basis

**Winner: B.** B explicitly defines timeout as wall-clock since entering the current `S3_WAITING_FOR_REVIEW`, counts backoff toward the deadline, and refuses to sleep past it. A says default 30 minutes but is less precise; C’s configurable timeout and mid-remediation behavior are useful edge tests to import.

### X-008 — Ungroundable/missing file:line finding handling

**Winner: B.** Preserve, report, and gate. B says findings without stable path/line may still be reported but may not be auto-fixed at L3 unless grounded and recorded. A is unspecified. C drops malformed/missing `file:line` findings, which risks hiding review risk.

### C-001 — Detection contract

**Winner: A+B hybrid; primary A.** A’s enforced lock is best; B’s centralized allowlist and unknown-shape logging should be included. C’s HALT test is valuable as verification.

### C-002 — Loop guard

**Winner: B+C hybrid; primary B for semantics.** B defines what the counter is and is not, baseline capture, observed-review sets, and termination order. C supplies the fence-post proof matrix. A’s SHA self-attribution and write-ahead increment are useful but less complete than B’s operational state.

### C-005 — Idempotency/run-log

**Winner: B.** The diff analysis correctly identifies B’s unique contribution: “29 typed events + `state.snapshot.json` cache + ‘JSONL is authoritative’ conflict rule.” Neither A nor C has equivalent crash-resume detail.

### S-002 / S-004 / S-007 — Cosmetic structural points

Concede. Top-level section count and requirement label style are not load-bearing. S-007 absolute paths favor B for this repository’s output-path discipline, but the final spec can use absolute implementation paths plus compact tables from C/A.

## High-severity content positions

- **C-001 detection contract:** adopt A’s hard gate, B’s centralized config/unknown-shape handling, and C’s T-210 runtime proof.
- **C-002 loop guard:** adopt B’s round definition and termination order, C’s validation-failure invariant and fence-post tests, and A’s write-ahead attribution discipline.
- **C-005 idempotency/run-log:** adopt B as authoritative; it is the only variant with enough recovery state for unattended side effects.

## Shared-assumption responses

- **A-001 — QUALIFY.** All variants poll `gh` surfaces per diff analysis, but B explicitly queries reviews, review comments, comments, and optional check-runs; still requires empirical proof.
- **A-002 — QUALIFY.** All route seeded findings to `/sc:troubleshoot`; B’s FR-5 relies on it, but the ingestion contract remains unstated and must be verified.
- **A-003 — REJECT as design assumption.** V1 may use Monitor, but B treats session death as FM-1/FM-10 risk and requires `--resume`; do not assume 30-minute liveness.
- **A-004 — QUALIFY.** A uses SHA-match and B/C count push-triggered re-review; attribution must be recorded via `pushed_commit_shas` and review head SHA, not assumed.
- **A-005 — ACCEPT.** All variants re-grade and B normalizes to `{Critical,High,Medium,Low,Nit}` with unknown/malformed to Medium.
- **A-006 — QUALIFY.** All variants require reply+resolve; B hedges endpoint differences in `thread-reply` helper and fixtures, so callable path must be validated.
- **A-007 — REJECT.** Local validation is necessary but not sufficient for “safe to push”; B mitigates with human-decision halt, validation history, and blast-radius escalation, not blind trust.
- **A-008 — QUALIFY.** B assumes IDs but protects with `processed_finding_ids`, `replied_comment_ids`, `resolved_thread_ids`, and stable hashes; empirical stability still needs proof.

## Final recommendation

Use Variant B as the final spec spine because it is the only one that can survive the backend failure modes inherent in level-3 automation: crash after push, duplicate review, partial reply/resolve, rate-limit backoff, corrupt snapshots, and re-armed sessions. Merge in A’s hard detection-contract gate and pure-seam tests, plus C’s loop-guard/edge-case test matrix, but do not replace B’s run-log/idempotency/recovery model.
