# State Machine (FSM) — the single source for all `--monitor` ordinals

This ref defines the **one** finite state machine that the `sc:pr-submit` skill drives.
There are **not four implementations** — there is a single FSM, and the `--monitor {0,1,2,3}`
ordinal is a **capability ceiling** compared at **three gates plus one override**, never four
divergent code paths (spec §5).

> **Core purity (NFR-6 / AC-9, T-N50).** This file contains ZERO shell or version-control
> command tokens. State transitions are described abstractly — the side-effecting I/O (the review
> poll, the push, the reply/resolve) is performed by the skill's bash scripts and the SKILL.md VAL
> validator, never named here. The deterministic core (`fsm.py`) likewise consumes
> already-fetched, already-classified data.

The Python state enums drop the spec's prime (an apostrophe is an illegal Python identifier
char): spec `S4'_HALT_BEFORE_PUSH` is enum member `S4_HALT_BEFORE_PUSH`. **This ref retains the
primed spec name** `S4'_HALT_BEFORE_PUSH` in prose; only `models.py`/`fsm.py` identifiers use the
unprimed form.

## 5.1 States and terminals

Working states:

- `S0_IDLE` — the FSM at rest. At **L0 (`--monitor 0`)** the FSM **never leaves `S0_IDLE`**: the
  skill opens the PR and returns, byte-for-byte identical to today (**AC-1**, zero regression).
- `S2_CLASSIFY` (a.k.a. POLLING) — armed; polling for the review, then classifying findings. The
  round-budget gate (`round_counter >= max_rounds`) is evaluated here.
- `S2b_VERIFY` — verify-before-remediate content gate (FR-3.5, C3a); see §5.2.
- `S3_DIAGNOSE` — diagnosis via `> Skill sc:troubleshoot-protocol` (verified findings only).
- `S3_FIXING` — the skill applies the diagnosed edits in the working tree (L2+).
- `S7_VALIDATING` — runs the §10 validation gates (VG-1..VG-6) on the working-tree edits.
- `S4_PUSHING` — the authorized push side-effect (L3, gated by the §5.3 conjunction).
- `S4'_HALT_BEFORE_PUSH` (Python `S4_HALT_BEFORE_PUSH`) — L2 ceiling: validate, then HALT,
  leaving changes in the working tree with no commit / no push / no reply.
- `S6_REPLYING` — reply on the finding thread citing the fix + SHA + passing validation.
- `RESOLVING` — resolve the thread (after the reply).
- `S5_AWAITING_REREVIEW` — waiting for the re-review attributed to our pushed SHA.
- `PROPOSED` — L1 ceiling: present "fix these? y/n", apply NO edits.
- `REPORT_ONLY` — a finding routed here is reported, not remediated; consumes NO round.

Terminals (the FSM never transitions out of these):

- `TERMINAL_CLEAN` — clean re-review (or no Medium+ findings); done.
- `HALT_MAX_ROUNDS` (terminal `terminal_max_rounds`) — round cap reached with residual findings.
- `HALT_HUMAN` (terminal `terminal_halted`) — a `needs_human_decision` finding short-circuited.
- `VALIDATION_FAIL` — validation failed beyond the retry budget.
- `TERMINAL_TIMEOUT` — the review never arrived within the wall-clock timeout.
- `TERMINAL_FAILED` — misrouted PR, corrupt run-log, or other unrecoverable failure.

## 5.2 The ordinal as a capability ceiling (transition table, NOT nested ifs)

The ordinal is compared at exactly **three gates** (expressed as one-line ordinal comparisons —
§5.4, never nested ifs):

| Gate | Predicate | L0 | L1 | L2 | L3 |
|------|-----------|----|----|----|----|
| **G-arm** | `ordinal >= 1` to leave `S0_IDLE` and enter polling (`S2_CLASSIFY`) | ✗ | ✓ | ✓ | ✓ |
| **G-edit** | `ordinal >= 2` to enter `S3_FIXING`; else route to `PROPOSED` (offer y/n, no edits) | — | ✗ → `PROPOSED` | ✓ | ✓ |
| **G-push** | `ordinal >= 3` **AND the §5.3 conjunction** to enter `S4_PUSHING`; else route to `S4'_HALT_BEFORE_PUSH` | — | — | ✗ → `S4'_HALT_BEFORE_PUSH` | conditional on §5.3 |

Plus **one override** that ignores the ordinal entirely and is evaluated **pre-gate**:

> `needs_human_decision ⇒ HALT_HUMAN` — even at L3 (FR-4.4). This is the ONLY predicate allowed
> to short-circuit the capability ceiling.

**G-verify is a CONTENT gate, not an ordinal gate.** The `S2b_VERIFY` filter (FR-3.5) runs at
*every* armed ordinal (L1–L3) on the `S2_CLASSIFY → S3_DIAGNOSE` edge. It guards entry to
`S3_DIAGNOSE` on `verification_status == "verified"` and routes `unverified` findings to
`REPORT_ONLY` **without consuming a round**. It is independent of the capability ceiling — even L1
(diagnose/propose-only) verifies before proposing — so it never appears in the ordinal gate table.
INV-001's increment edge is unchanged: the round counter ticks only at
`S5_AWAITING_REREVIEW → S2_CLASSIFY`, and the round-budget gate is still evaluated at
`S2_CLASSIFY`; verification merely filters which findings (if any) open the fix cycle.

### 5.2a L2 ceiling behavior — `S3_FIXING → S7_VALIDATING → S4'_HALT_BEFORE_PUSH`

At **L2** (`G-edit` passes, `G-push` does not) the skill **applies the diagnosed edits ITSELF** in
the working tree at `S3_FIXING` — troubleshoot diagnoses, but it does NOT auto-apply, so
`sc:pr-submit` owns the edit application (FR-4.2). It then runs the §10 validation gates at
`S7_VALIDATING`, and — regardless of whether validation passes — **HALTs at**
`S4'_HALT_BEFORE_PUSH`, leaving the changes in the working tree with **NO commit, NO push, NO
reply** (T-410 files modified; T-411 push never; T-412 commit never; T-413 reply never). The L2
ceiling never reaches `S4_PUSHING`/`S6_REPLYING`/`RESOLVING`. The edge is:
`S3_DIAGNOSE → S3_FIXING → S7_VALIDATING → S4'_HALT_BEFORE_PUSH` (the `G-push` ordinal check
`ordinal >= 3` fails at L2, so the push branch is never taken). This edge is described abstractly
here (the actual edit/validation I/O is the SKILL's job; this ref stays core-pure).

## 5.3 G-push — the 5-predicate runtime conjunction (INV-016, verbatim)

> **INV-016.** A push is authorized at the `S4_PUSHING` transition if and only if ALL of the
> following runtime predicates hold, evaluated as a conjunction immediately before the push:
> (1) `monitor_ordinal >= 3`; (2) `validation_status == "validated"` (targeted tests + lint +
> format all green this cycle); (3) `needs_human_decision == false` for every finding in the cycle;
> (4) `round_counter < max_rounds`; (5) the cycle produced at least one grounded, applied edit
> (`applied_edits > 0` — never push an empty or ungroundable-only cycle). If any predicate is false
> the FSM routes to `HALT_*` (HALT_HUMAN for (3), HALT_MAX_ROUNDS for (4), TERMINAL_CLEAN/report for
> (5), report-only for (1)–(2)) and NO push occurs. Every push, authorized or blocked, writes a
> **write-ahead `push_decision` audit record** to the run-log naming which predicates held; this
> record is mandatory at L3 and is the audit primitive (not a per-push interactive prompt). A
> one-time per-run confirmation applies: the FIRST push of a run requires `--yes` OR an interactive
> confirm unless the run is non-interactive, in which case the `push_decision` record + the explicit
> `--monitor 3` arming stands as the recorded authorization.

Predicate (5) closes the "announce-resolved with nothing actually changed" hole. The
`push_decision` write-ahead record is the real safety layer (verified by **T-ZERO-EDIT-NO-PUSH**:
`applied_edits == 0` ⇒ `push_count == 0`, `push_decision.authorized == False`,
`push_decision.predicate_5_applied_edits == 0`).

## 5.4 Why a machine and not nested ifs

A nested-if implementation of four levels has 2³ = 8 reachable gate combinations; the bug surface
is every forgotten combination. The FSM has finite states × **3 one-line gate checks**, expressible
as a transition table that the C6 tests assert row-by-row (AC-2..AC-6 become table-row assertions).
The increment edge (INV-001), the push conjunction (INV-016), and the override are each a single
named predicate — not a branch nested inside another branch.
