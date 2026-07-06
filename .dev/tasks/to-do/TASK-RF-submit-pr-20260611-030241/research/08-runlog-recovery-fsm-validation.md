# Research: Run-Log + Recovery + FSM + Validation (gap-fill)

**Status:** Complete
**Date:** 2026-06-11

---

This is a TARGETED GAP-FILL closing the ownership crack on four spec subsystems
(§11 Run-Log, §12 Failure/Recovery, §5 FSM/gates, §10 Validation gates). It
extracts the per-item detail the task-builder needs and maps each onto the R4
module layout (`research/04-test-infra-and-deterministic-core.md`):
`src/superclaude/submit_pr/` (underscored importable pkg) for the deterministic
core; `src/superclaude/skills/sc-submit-pr-protocol/refs/` for the markdown refs;
`tests/submit_pr/` for the pytest suite. Spec = `merged-spec.md` (line cites below).

This is EXTRACTION from a self-contained spec, not design invention.

---

## 1. §11 Run-Log Substrate (GAP-1, CRITICAL)

**Maps to:** `src/superclaude/submit_pr/run_log.py` (+ models in `models.py`) and
the `refs/loop-guard.md` ref. **Tests:** `tests/submit_pr/test_run_log.py`
(T-N20..T-N22), `tests/submit_pr/test_idempotency.py`
(T-N01, T-N02, T-FRESH-COMMENT-NO-DOUBLE-FIX). Spec §11 = merged-spec.md:697-745.

### 1.1 Authority rule (§11.1, merged-spec.md:701-705)

Per-item checklist facts the builder must encode in `run_log.py`:

- The append-only `monitor-run-<PR>.jsonl` is **AUTHORITATIVE**. (:702)
- `state.snapshot.json` is a **materialized cache** — derived, never authoritative. (:702)
- On disagreement between snapshot and JSONL ⇒ **rebuild state FROM JSONL** (NFR-6). (:702-703)
- **Every state transition appends a `state_transition` event.** (:703-704) (Note:
  the event-type enum at :724-731 names this `route_decision`/`*_started`/`*_completed`
  family + explicit lifecycle events; §11.1's prose "state_transition event" is the
  generic class — the run_log writer appends one envelope per FSM edge with
  `state_before`/`state_after` populated, see §1.3.)
- **Write-ahead discipline:** every external action is preceded by a write-ahead
  record that is **fsynced BEFORE the side effect** executes. (:704-705) This is the
  load-bearing crash-safety primitive — the push triad in §12.1 is its instance.

`run_log.py` therefore exposes: `append(event)` (fsync-on-write), `rebuild_state()`
(fold JSONL → snapshot), `materialize_snapshot()` (write cache), and a
`write_ahead(event)` helper that fsyncs before returning so the caller can perform
the side effect. T-N22 asserts JSONL validity; the rebuild path is the NFR-6 contract.

### 1.2 The 5 file locations (§11.2, merged-spec.md:707-716)

| # | Path (relative to `<output-dir>`) | Role |
|---|---|---|
| 1 | `monitor-run-<PR_NUMBER>.jsonl` | authoritative append-only event log |
| 2 | `state.snapshot.json` | materialized cache (rebuildable from #1) |
| 3 | `findings.latest.json` | latest normalized finding set |
| 4 | `validation/round-<N>/` | per-round stdout/stderr + exit codes |
| 5 | `troubleshoot/round-<N>/` | per-round troubleshoot prompts/outputs |

**Default `<output-dir>`** (:715-716):
`/config/workspace/IronClaude/.dev/pr-monitor/pr-<N>-<YYYYMMDDHHMMSS>/`
— UNLESS `--resume` supplies an existing log path (then that log's dir is reused).

Builder item: `run_log.py` owns output-dir resolution (default vs `--resume`),
and creates the `validation/round-<N>/` + `troubleshoot/round-<N>/` subdirs
per round.

### 1.3 Event envelope fields (§11.3, merged-spec.md:718-721)

Each JSONL line is valid JSON with these envelope fields:

- `schema_version`
- `event_id` — **unique + monotonic** (builder: monotonic counter; T-N20/N22 assert)
- `event_type` — one of the 30 below
- `timestamp`
- `run_id`
- `pr{ repo, number, url, base, head }` (nested object, 5 keys)
- `state_before`
- `state_after`
- `round_index` / `round_counter`
- `payload`

### 1.3a ALL required event types (verbatim, merged-spec.md:723-731)

The builder MUST encode this as a closed enum (e.g. in `models.py`); T-N20
asserts per-event `timestamp + round + state`, so every emitter sets those.

```
 1. run_started
 2. environment_check
 3. pr_create_attempted
 4. pr_created
 5. monitor_armed
 6. baseline_captured
 7. poll_attempt
 8. poll_result
 9. api_backoff
10. classifier_unknown_shape
11. review_detected
12. findings_normalized
13. finding_verified
14. finding_unverified
15. round_incremented
16. route_decision
17. troubleshoot_started
18. troubleshoot_completed
19. fix_applied
20. validation_started
21. validation_completed
22. push_decision
23. push_initiated
24. push_completed
25. reply_posted
26. thread_resolved
27. idempotency_skip
28. terminal_clean
29. terminal_timeout
30. terminal_max_rounds
31. terminal_halted
32. terminal_failed
```

**EXTRACTION NOTE FOR BUILDER (spec arithmetic flag):** the prompt says "30 event
types"; the verbatim block :724-731 actually enumerates **32** distinct types (the
prompt undercounts by 2 — the 5 split `terminal_*` variants and the
`finding_verified`/`finding_unverified` 2-way split push it past 30). Additionally,
recovery rule §12.1 references a **33rd** event, `push_aborted_or_not_landed`
(:771), emitted only on the crash-window not-landed branch — it is NOT in the §11.3
list but IS required by §12.1. Builder: register **33** event types total
(32 from §11.3 + `push_aborted_or_not_landed` from §12.1). This is a real
spec-internal count gap to surface, not an invention.

The write-ahead push triad is `push_decision` → `push_initiated` → `push_completed`
(:732, detailed in §2.1).

### 1.4 The 5 idempotency sets (§11.4, merged-spec.md:735-744)

Maintained in materialized state; an `idempotency_skip` event is appended whenever
an action is skipped because its key is already present. Each set prevents a
distinct double-action:

| Set | Key | Prevents |
|---|---|---|
| `processed_review_ids` | review emission id | re-processing the same Augment review emission (:739) |
| `processed_finding_ids` | **`fix_key = sha256(path + line + finding_body)`** (comment_id-INDEPENDENT, per INV-009 / §5.4) | applying the same fix twice (:740-741) |
| `replied_comment_ids` | thread-scoped `reply_key` | duplicate thread replies (:742) |
| `resolved_thread_ids` | thread id | duplicate resolution calls (:743) |
| `pushed_commit_shas` | commit SHA | (this is the SHA set INV-001 attributes re-reviews against, §9/§12.1) (:744) |

**Critical builder detail — fix_key:** `processed_finding_ids` is keyed on
`sha256(path + line + finding_body)`, NOT on the GitHub `comment_id`. This is the
EC-4 / T-FRESH-COMMENT-NO-DOUBLE-FIX contract: a *fresh* `comment_id` re-raising the
*same* underlying finding (same path+line+body) hashes to the same `fix_key` ⇒
`idempotency_skip`, no double-fix. (merged-spec.md:529-535 EC-4, :740-741, :801 NFR-1.)

### 1.5 Test mapping (§11 → tests)

- **`test_run_log.py`** (Pattern 1, imports `submit_pr.run_log`):
  - **T-N20** — log existence + per-event `timestamp`/`round`/`state` populated.
  - **T-N21** — (per R4 §C) JSONL well-formedness / event ordering.
  - **T-N22** — JSONL validity (every line parses as JSON; `event_id` monotonic).
  - (:733 "T-N20..T-N22 assert log existence, per-event timestamp+round+state, and
    JSONL validity.")
- **`test_idempotency.py`** (Pattern 1 + mock, imports `submit_pr.run_log`/reply):
  - **T-N01** — replay findings twice → reply once per thread (:801).
  - **T-N02** — reply-tracking persisted across polls (:801).
  - **T-FRESH-COMMENT-NO-DOUBLE-FIX** — fresh `comment_id`, same `fix_key` ⇒ one fix
    only (the §1.4 fix_key contract; :801, EC-4 :529-535).

---

## 2. §12 Failure Modes & Recovery (GAP-2, CRITICAL)

**Maps to:** a recovery module in `src/superclaude/submit_pr/` — recommend
`recovery.py` (resume + crash-window logic) collaborating with `run_log.py`
(JSONL reconstruction) and `fsm.py` (`--resume` entry, S5 re-entry). **Tests:**
`tests/submit_pr/test_crash_recovery.py` (FM-1..FM-12, T-CRASH-WINDOW-NO-DOUBLE-PUSH).
Spec §12 = merged-spec.md:748-792. `--resume <run-log-path>` is a first-class path (:751-752).

### 2.1 INV-007 verbatim — write-ahead push triad ordering (§12.1, merged-spec.md:754-763)

The exact ordered sequence per authorized push (each step fsynced where noted).
**Builder: this ordering is load-bearing; the run_log records must land in this order:**

1. **`push_decision`** `{run_id, cycle_id, round_counter, predicates, authorized:true,
   pre_push_sha, target_branch, target_remote}` — **(fsync)** (:756-757)
2. **compute `target_sha`** (:758)
3. **`push_initiated`** `{run_id, cycle_id, idempotency_key, pre_push_sha, target_sha,
   target_branch, target_remote, remote_ref}` — **(fsync BEFORE `git push`)** (:758-759)
4. **`git push <target_remote> <target_sha>:<target_branch>`** (:759-760)
5. **`push_completed`** `{...pushed_at}` — **(fsync)** (:760)
6. Enter **`S5_AWAITING_REREVIEW`** (:760-761)

**SHA attribution on entry to S5:** only a re-review attributed to a recorded
`push_initiated.target_sha` may complete the cycle and tick `round_counter` (:761-762).
This is the join point with INV-001 (§9) and the `pushed_commit_shas` set (§1.4).

**PRE-push idempotency key (verbatim, :762-763):**
```
push:<run_id>:<cycle_id>:<pre_push_sha>:<target_branch>
```
Keyed on the **PRE-push SHA, not post-hoc** — so a crash between step 3 and step 5
leaves a deterministic key the resume path can look up.

### 2.2 Crash-window resume — 3-way branch (§12.1, merged-spec.md:765-773)

On `--resume`, if the latest event for an idempotency key is `push_initiated` with
**no matching `push_completed`**, the monitor **MUST NOT create another commit or
push** until it queries the remote for `target_sha`. Then branch on reachability:

| Branch | Remote state | Action | Resume state |
|---|---|---|---|
| **A — landed** | `target_sha` reachable from remote branch tip | append `push_completed{recovered:true}` | resume in `S5_AWAITING_REREVIEW` (:768-770) |
| **B — not landed** | `target_sha` NOT reachable (remote still at `pre_push_sha` / lacks commit) | append `push_aborted_or_not_landed{recovered:true}`, return to pre-push path for the SAME cycle **WITHOUT recomputing the fix** | re-drive push for same cycle (:770-772) |
| **C — ambiguous** | tip moved to an unrelated SHA | `HALT_HUMAN` with original fields + observed remote SHA | HALT (:773) |

**Critical builder details:**
- Branch B re-pushes WITHOUT recomputing the fix (the worktree edit is preserved; only
  the push side-effect is redone). This is why the fix is idempotent on `fix_key` (§1.4).
- Branch B emits `push_aborted_or_not_landed` — the 33rd event type flagged in §1.3a.
- The decision is gated on a **live remote query** for `target_sha`, never on a guess.

**T-CRASH-WINDOW-NO-DOUBLE-PUSH (verbatim, :775-776):**
```python
assert push_executor.push_count == 2
assert resume_state == S5_AWAITING_REREVIEW
assert push_completed.recovered == True
```
(Branch-A scenario: the push actually landed; resume must NOT push a second time,
total push_count stays at the legitimate count, and the recovered `push_completed`
is synthesized.)

### 2.3 FM-1..FM-12 catalog (§12.2, merged-spec.md:778-792)

Each row = one `test_crash_recovery.py` test. Trigger / Action / Recovery verbatim:

| FM | Trigger | Action | Recovery |
|----|---------|--------|----------|
| FM-1 | Review never arrives | `terminal_timeout`, no edits/push | `--resume` re-arm |
| FM-2 | Primary/secondary rate limit | `api_backoff`, exp backoff to 300s, continue to timeout | none unless timeout |
| FM-3 | Unknown Augment emission shape | `classifier_unknown_shape`, keep polling | add fixture before parser change |
| FM-4 | Unknown bot identity | ignore as no-review | re-probe + update DET constant |
| FM-5 | Validation failure | no push/reply/resolve; L2 halt; L3 one retry if in budget | inspect artifacts, resume |
| FM-6 | Crash after push before reply | resume: no re-fix; post missing replies once, then resolve | automatic via idempotency sets |
| FM-7 | Crash after reply before resolve | resume: resolve only missing thread, no duplicate reply | automatic |
| FM-8 | Duplicate review / poll payload | `idempotency_skip`; no route/fix/reply | none |
| FM-9 | Round cap with residual findings | `terminal_max_rounds`; optional L3 summary comment; no further fix | user re-runs with higher `--max-rounds` (≤5) |
| FM-10 | `needs_human_decision` finding | `terminal_halted`; no auto-mutation | user provides decision; resume |
| FM-11 | Misrouted PR URL | `terminal_failed`; do not monitor; instruct close | recreate with `--repo IronbellyOrg/IronClaude` |
| FM-12 | Corrupt run-log / snapshot | `terminal_failed`; require explicit recovery point | user picks last valid event ID; no guessing |

**Builder cross-links:** FM-6/FM-7 recovery is "automatic via idempotency sets"
(§1.4: `replied_comment_ids`, `resolved_thread_ids`) — they are the §11.4 sets in
action, so `test_crash_recovery.py` FM-6/FM-7 share fixtures/state with
`test_idempotency.py`. FM-9 ties to the §9 loop-guard (`terminal_max_rounds` =
INV-001 gate). FM-11 ties to VG-6 PR-target (§10/§3). FM-12 ties to §11.1 authority
rule (rebuild-from-JSONL; corrupt-both ⇒ `terminal_failed`, no guessing).

---

## 3. §5 FSM + §10 Validation Gates (GAP-3/GAP-4, IMPORTANT/MINOR)

**Maps to:** `src/superclaude/submit_pr/fsm.py` (+ `loop_guard.py`, `classifier.py`)
and the `refs/state-machine.md` ref; validation belongs in `fsm.py`'s
`S7_VALIDATING` driver (R4 maps `test_validation_gate.py` → `submit_pr.fsm`).
**Tests:** `tests/submit_pr/test_autonomy_gates.py`, `test_loop_guard.py`,
`test_validation_gate.py`. Spec §5 = merged-spec.md:249-340; §10 = :663-693.

### 3.1 §5.1 FSM states (merged-spec.md:253-292, R3 canonical lexicon)

The single FSM (all ordinals share ONE implementation, :255). Canonical states
(state-machine.md ref must list these; §15 glossary :947+ maps to A's 7-state and
B's S0..S14):

`S0_IDLE` → `S2_CLASSIFY/POLLING` → (`TERMINAL_CLEAN` | `S2b_VERIFY`) →
(`REPORT_ONLY` | `S3_DIAGNOSE`) → (`PROPOSED`→`HALT` | `S3_FIXING`) →
(`HALT_HUMAN` | `S7_VALIDATING`) → (`VALIDATION_FAIL` |
`S4'_HALT_BEFORE_PUSH` | `S4_PUSHING`) → `S6_REPLYING` → `RESOLVING` →
`S5_AWAITING_REREVIEW` → (loop back to `S2_CLASSIFY` on attributed re-review |
`TERMINAL_*`). Terminals: `TERMINAL_CLEAN`, `HALT_MAX_ROUNDS`, `HALT_HUMAN`,
`VALIDATION_FAIL`, `REPORT_ONLY`. (:259-292)

**S2b_VERIFY (verify-before-remediate, FR-3.5/C3a, :270-272, :305-311):** a CONTENT
gate, NOT an ordinal gate — runs at EVERY armed ordinal (L1–L3) on the
`S2_CLASSIFY → S3_DIAGNOSE` edge. Guards entry to `S3_DIAGNOSE` on
`verification_status == verified`; routes `unverified` findings to `REPORT_ONLY`
**without consuming a round**. INV-001's increment edge is unchanged.

### 3.2 §5.2 Gate table — ordinal = capability ceiling (merged-spec.md:294-314)

Three ordinal gates + one override. Builder encodes as a transition table (3 one-line
gate checks), NOT nested ifs (§5.4 :336-340 — 2³=8 nested-if combos is the bug surface):

| Gate | Predicate | Routes-to-on-fail |
|---|---|---|
| **G-arm** | `ordinal >= 1` to enter polling | (L0 stays `S0_IDLE`) |
| **G-edit** | `ordinal >= 2` to enter `S3_FIXING` | L1 → `PROPOSED` (offer y/n, no edits) |
| **G-push** | `ordinal >= 3` **AND §5.3 conjunction** to enter `S4_PUSHING` | L2 → `S4'_HALT_BEFORE_PUSH` |

L0/L1/L2/L3 capability matrix (:296-300):
- G-arm: L0 ✗ / L1 ✓ / L2 ✓ / L3 ✓
- G-edit: L0 — / L1 ✗(→PROPOSED) / L2 ✓ / L3 ✓
- G-push: L0 — / L1 — / L2 ✗(→HALT_BEFORE_PUSH) / L3 conditional

**Override (:302-303):** `needs_human_decision ⇒ HALT_HUMAN` even at L3 (FR-4.4) —
the ONLY predicate allowed to short-circuit the ceiling. Builder: this is a
pre-gate check evaluated before G-edit/G-push, routing straight to `HALT_HUMAN`.

**L0 (:313-314):** `--monitor 0` opens PR and returns, byte-for-byte identical to
today (AC-1) — FSM never leaves `S0_IDLE`.

### 3.3 §5.3 INV-016 — G-push 5-predicate conjunction (verbatim, merged-spec.md:316-334)

A push is authorized at `S4_PUSHING` **iff ALL 5 hold**, evaluated as a conjunction
immediately before `git push` (builder: this is G-push's second half, ANDed with
`ordinal >= 3`):

1. `monitor_ordinal >= 3`
2. `validation_status == "validated"` (targeted tests + lint + format all green this cycle)
3. `needs_human_decision == false` for EVERY finding in the cycle
4. `round_counter < max_rounds`
5. the cycle produced **at least one grounded, applied edit** (`applied_edits > 0` —
   never push an empty or ungroundable-only cycle)

**Fail routing (:324-326):** any false predicate routes to `HALT_*` —
HALT_HUMAN for (3), HALT_MAX_ROUNDS for (4), TERMINAL_CLEAN/report for (5),
report-only for (1)–(2). NO push occurs.

**Audit primitive (:327-331):** every push — authorized OR blocked — writes a
write-ahead `push_decision` record naming which predicates held. Mandatory at L3.
NOT a per-push interactive prompt. One-time per-run: the FIRST push requires `--yes`
OR interactive confirm unless non-interactive (then `push_decision` + explicit
`--monitor 3` arming = recorded authorization).

Predicate (5) closes the "announce-resolved with nothing changed" hole; verified by
**T-ZERO-EDIT-NO-PUSH** (:333-334, test body :878-887: asserts `push_count == 0`,
`push_decision.authorized == False`, `push_decision.predicate_5_applied_edits == 0`).

### 3.4 §10 VG-1..VG-6 — ORDERED validation gate list (merged-spec.md:663-693)

Runs in **this exact order** before any L3 push or thread resolution; all-green ⇒
`validation_status == "validated"` (the single definition consumed by §5.3
predicate (2), :666-667). Builder: `fsm.py` `S7_VALIDATING` drives these in order;
artifacts → `validation/round-<N>/` (§1.2).

| # | Gate | Command | Blocks | Test |
|---|------|---------|--------|------|
| **VG-1** | Targeted tests | `uv run pytest tests/<changed-area>/ -v` | push | T-501 |
| **VG-2** | Cross-cutting escalation | `make test` (`uv run pytest`) when ≥2 packages / shared infra / hooks / CLI parsing / run-log FSM touched, or High/Critical broad blast radius | push | T-502 |
| **VG-3** | Lint | `make lint` (`ruff check`) | push | T-510 |
| **VG-4** | Format | `uv run ruff format --check src/ tests/` | push | T-511 |
| **VG-5** | Sync (skill self-edits only) | `make verify-sync` | commit | — |
| **VG-6** | PR-target | URL == `IronbellyOrg/IronClaude` | arm | T-108 |

**VG-3 ≠ VG-4 — the load-bearing two-gate split (:678-679, KNOWN GOTCHA):**
`make lint` runs ONLY `ruff check`; CI separately runs `ruff format --check`. They
are encoded as **two distinct gates** so green lint alone CANNOT authorize a push.
Builder MUST keep these separate — collapsing them re-introduces the exact memory-note
bug (`reference_make_lint_vs_ci_ruff_format.md`). **T-511 is the regression test** for
this split. VG-5 blocks at COMMIT (not push) and only for skill self-edits; VG-6 blocks
at ARM (earliest gate) — the §3/§19 SoT/PR-target discipline (ties to FM-11).

**§10.1 no-push-on-failure (:681-685):** any required gate non-zero ⇒ append
`validation_completed{status:"failed"}`; no commit/push/reply-as-fixed/resolve. L2 halts.
L3 may attempt ONE correction only if `round_counter < max_rounds`; else HALT with
residual + validation details. **The validation retry does NOT increment
`round_counter`** (INV-6 / T-520) — builder: this is the §9 INV-6 corollary, distinct
from the round-budget gate.

**§10.2 commit-and-push gate (:687-693):** L3 commits/pushes only if working-tree diff
corresponds to current round's findings, validation passed after final diff, no active
`needs_human_decision`, branch still PR head, target is `origin` never `upstream`, AND
§5.3 conjunction holds. Commit message carries the co-author trailer
`Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.

### 3.5 Test mapping (§5/§10 → tests)

- **`test_autonomy_gates.py`** (Pattern 1, `submit_pr.classifier`/`fsm`): G-arm/G-edit/
  G-push ordinal ceiling table rows (AC-2..AC-6 as table-row asserts, :340), the
  `needs_human_decision ⇒ HALT_HUMAN` override (T-430), and T-ZERO-EDIT-NO-PUSH
  (predicate 5). §14 behavioral tests (:836-900) are the bodies: T-401/T-402 (zero
  edits L1), T-410..T-413 (zero pushes L2), T-430 (HALT on needs_human_decision),
  T-420=AC-2 (full E2E).
- **`test_loop_guard.py`** (Pattern 1, `submit_pr.loop_guard`): INV-001 fence-post —
  `round_counter` increments ONLY on `S5_AWAITING_REREVIEW → S2_CLASSIFY` (:602-606);
  gate uses `>=` not `>` (INV-5, :618-619); T-626-OFF-BY-ONE (:641-655,
  `round_counter==2` not 3 at max_rounds=2), T-VANISHED-MONO (INV-4 irrevocability,
  :657-659), fence-post matrix T-620..T-629 (:626-637).
- **`test_validation_gate.py`** (Pattern 1, `submit_pr.fsm`): VG-1..VG-6 ordered
  execution, VG-3≠VG-4 split (T-510 lint, T-511 format — the gotcha regression),
  no-push-on-failure (T-520 validation-retry-no-round-increment).

---

## SUMMARY — subsystem → module → test mapping

All four ownership cracks closed. Per-item detail extracted verbatim from a
self-contained spec; modules mapped onto R4's `src/superclaude/submit_pr/` layout.

| Spec § | Subsystem | Module (`src/superclaude/submit_pr/`) | Ref (`.../sc-submit-pr-protocol/refs/`) | Test file (`tests/submit_pr/`) | Key tests |
|---|---|---|---|---|---|
| §11 (GAP-1, CRITICAL) | Run-Log substrate (JSONL authority, 5 files, envelope+events, 5 idempotency sets) | `run_log.py` (+ event enum/`Finding` in `models.py`) | `loop-guard.md` | `test_run_log.py`, `test_idempotency.py` | T-N20, T-N21, T-N22 / T-N01, T-N02, T-FRESH-COMMENT-NO-DOUBLE-FIX |
| §12 (GAP-2, CRITICAL) | Failure modes & recovery (INV-007 push triad, crash-window 3-way, FM-1..12) | `recovery.py` (+ `run_log.py` rebuild, `fsm.py` `--resume`/S5) | `state-machine.md` | `test_crash_recovery.py` | FM-1..FM-12, T-CRASH-WINDOW-NO-DOUBLE-PUSH |
| §5 (GAP-3, IMPORTANT) | FSM states + ordinal-ceiling gates + INV-016 5-predicate conjunction + override | `fsm.py`, `loop_guard.py`, `classifier.py` | `state-machine.md` | `test_autonomy_gates.py`, `test_loop_guard.py` | T-401/402, T-410..413, T-430, T-ZERO-EDIT-NO-PUSH / T-626-OFF-BY-ONE, T-VANISHED-MONO, T-620..629 |
| §10 (GAP-4, MINOR) | Validation gates VG-1..VG-6 (ordered; VG-3≠VG-4 split) | `fsm.py` (`S7_VALIDATING` driver) | `state-machine.md` | `test_validation_gate.py` | T-501, T-502, T-510, T-511, T-520, T-108 |

**Three spec-internal findings to surface to the builder (not inventions):**

1. **Event-type count gap (§11.3 vs prompt vs §12.1).** The verbatim :724-731 block
   enumerates **32** event types (prompt said 30 — undercount by 2). §12.1 adds a
   **33rd**, `push_aborted_or_not_landed` (:771), absent from the §11.3 list but
   required on the crash-window not-landed branch. Register **33** total.
2. **VG-3≠VG-4 two-gate split is load-bearing** (:678-679). `make lint`=`ruff check`
   only; `ruff format --check` is a SEPARATE gate (VG-4/T-511). Collapsing them
   re-introduces the documented `reference_make_lint_vs_ci_ruff_format.md` bug.
3. **`fix_key = sha256(path+line+finding_body)`** (comment_id-INDEPENDENT, :740-741)
   is the single dedup key threading §11.4 (`processed_finding_ids`), EC-4, recovery
   branch B (re-push without recomputing fix), and FM-6/FM-7 idempotent resume.

**Module-naming note (inherited from R4):** the deterministic core lives in the
underscored `src/superclaude/submit_pr/` package (importable); the hyphenated
`skills/sc-submit-pr-protocol/` holds SKILL.md + `refs/` (`loop-guard.md`,
`state-machine.md`) + bash glue only. `recovery.py` is the recommended new module
name for §12 (R4 §★ listed `run_log.py` + `fsm.py` but did not name a dedicated
recovery module — the crash-window logic is substantial enough to warrant its own).

**Status:** Complete
