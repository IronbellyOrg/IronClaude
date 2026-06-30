<!-- Provenance: produced by /sc:design (V1.1); EXTENDS .dev/brainstorms/20260610-234750-pr-review-auto-remediation/merged-spec.md (V1.0). Does NOT replace it. -->
---
contract_version: "1.1"
artifact: design-addendum
extends: ./merged-spec.md
topic: "PR Review Auto-Remediation Monitor — V1.1 (post-push re-trigger + oversized-PR auggie fallback)"
domain: qa
grounded_in:
  - src/superclaude/pr_submit/{fsm,run_log,recovery,detection,classifier,loop_guard,models,severity_router}.py
  - src/superclaude/skills/sc-pr-submit-protocol/{SKILL.md,refs/*}
  - src/superclaude/commands/auggie-review.md
  - memory: reference_augment_review_triggers
new_requirements: [FR-8, FR-9, FR-10]
new_invariants: [INV-R1, INV-R2, INV-R3]
new_idempotency_set: auggie_review_invoked
created: 2026-06-12
status: build-ready (hand to task-builder)
---

# V1.1 Design Addendum — Post-Push Re-Trigger + Oversized-PR Auggie Fallback

> **Reading order.** This is an **extension** of `merged-spec.md` (V1.0). Every V1.0
> FR/NFR/AC/INV/EC remains binding. This addendum adds **FR-8, FR-9, FR-10**, three
> invariants (**INV-R1/R2/R3**), one idempotency set (`auggie_review_invoked`), two FSM
> states, and a small closed-enum + run-log delta. Where a V1.0 line is *modified* (not
> just added to), the change is called out as **[MOD]** with the exact V1.0 anchor.

---

## 0. Naming reconciliation (binding) — `sc:pr-submit`, not `sc:submit-pr`

**[MOD]** V1.0 §1.1 names the skill `sc:submit-pr`. The **shipped code settled on
`sc:pr-submit`** (`src/superclaude/skills/sc-pr-submit-protocol/`,
`superclaude.pr_submit.*`, `fsm.PR_TARGET_REPO`, `SKILL.md:1` `name: sc:pr-submit-protocol`).
**V1.1 anchors to the live name `sc:pr-submit` / package `superclaude.pr_submit` / skill dir
`sc-pr-submit-protocol` / tests `tests/pr_submit/`.** All V1.0 references to `sc:submit-pr`,
`sc-submit-pr-protocol`, and `tests/submit_pr/` read as their `pr-submit`/`pr_submit`
equivalents. No behavior change; a name-faithfulness correction.

---

## 1. Root-cause statement (why V1.0's loop is broken)

V1.0's loop-guard ticks `round_counter` at the single edge
`S5_AWAITING_REREVIEW --[review_observed ∧ sha_attributed_to_our_push]--> S2_CLASSIFY`
(INV-001). V1.0 assumed that **pushing a remediation commit causes Augment to re-review**.

Per memory `reference_augment_review_triggers` (verified 2026-06-11): the **Augment Code
GitHub App** (`augmentcode[bot]`) reviews **only** on (a) PR open / draft→ready, or (b) a
PR **conversation comment** matching `auggie review` / `augment review` / `augmentcode review`.
**Pushing new commits to an existing PR does NOT auto-trigger a review** (no `synchronize`
review). Additionally, an **abnormally-large PR is DECLINED** with the comment:

> `This pull request is abnormally large and would use a significant amount of tokens to
> review. If you still wish to review it, comment "augment review" and we will review it.`

**Consequence:** after V1.0's L3 push, no re-review ever arrives → the `S5 → S2` edge is
unreachable → `round_counter` never advances → the loop stalls until `TERMINAL_TIMEOUT`.
The live code (`fsm.run_skill`, `fsm.py:792-793`) papers over this with an **optimistic
post-resolve increment** that does not correspond to any real re-review — so multi-round
remediation is fictional.

**V1.1 fixes this with three behaviors:**

| R | Behavior | Primary requirement |
|---|----------|---------------------|
| **R1** | After each L3 push, post one `auggie review` PR comment, then poll for the attributed `augmentcode[bot]` re-review. Bounded by `--max-rounds`. | **FR-8** |
| **R2** | If Augment instead posts the "abnormally large" decline, fall back to in-session `/sc:auggie-review <PR> --depth quick --remediation-offer --auggie-model claude-sonnet-4-6`. | **FR-9** |
| **R3** (HARD) | On fallback: clamp the fallback budget to `--max-rounds=1` **and** guarantee `/sc:auggie-review` is invoked **at most once per PR** via a new `auggie_review_invoked` idempotency set. | **FR-10** |

---

## 2. Flag validation (R2 fallback command) — VALIDATED against `auggie-review.md`

The R2 fallback string is `/sc:auggie-review <PR> --depth quick --remediation-offer
--auggie-model claude-sonnet-4-6`. Each flag verified against
`src/superclaude/commands/auggie-review.md`:

| Flag/value | Source line | Verdict |
|---|---|---|
| `--depth quick` | `auggie-review.md:49` — `quick\|standard\|deep`, `quick` = "auggie single-pass, ~2min" | ✅ valid value |
| `--remediation-offer` | `auggie-review.md:52` — documented flag (default `true`) | ✅ valid flag |
| `--auggie-model claude-sonnet-4-6` | `auggie-review.md:55` — **the exact example given** | ✅ valid flag + value |
| `<PR-number>` target | `auggie-review.md:26-27,36` — `<PR-number>` resolved via `gh pr view` | ✅ valid target |

Posting to the PR is implicit: `--post-pr` defaults `true` for a PR target
(`auggie-review.md:50`) — so the fallback review lands on the PR without an extra flag. We do
**not** pass `--no-post-pr`. (`--depth quick` is the deliberate token-bounded choice for R3.)

---

## 3. The two new behaviors, end-to-end

### 3.1 R1 — post-push re-trigger (the loop fix)

```
... S4_PUSHING → S6_REPLYING → RESOLVING
                                   │
                                   ▼
                        [S5a_RETRIGGER_REVIEW]      ← NEW (FR-8)
                        post ONE "auggie review" PR conversation comment
                        (gh api …/issues/<N>/comments), record rereview_requested,
                        rereview_request_count += 1   (INV-R1: ≤ max_rounds)
                                   │
                                   ▼
                        [S5_AWAITING_REREVIEW]       ← poll (reuse FR-2 poller + DET)
            ┌──────────────────────┼───────────────────────────┐
   attributed re-review      decline comment               timeout
   (review > decline)        (newer than watermark)            │
            │                      │                            ▼
   round_counter += 1        [S5b_AUGGIE_FALLBACK]      [TERMINAL_TIMEOUT]
   (INV-001 edge, UNCHANGED)       (FR-9 / FR-10)
            ▼
   [S2_CLASSIFY]  → gate round_counter >= max_rounds ? (unchanged)
```

**The only INV-001-touching change** is **[MOD]**: the increment moves from the live code's
optimistic post-resolve site (`fsm.run_skill`, the `result.round_counter += 1` at
`fsm.py:793`) to the **actually-observed attributed re-review** after the re-trigger. This
makes the code match INV-001's *literal* definition (which always said "at `S5 → S2` on an
attributed re-review"); the edge, the gate (`>=`), monotonicity, and `max_rounds=N ⇒ N pushes`
are all preserved verbatim.

### 3.2 R2/R3 — oversized-PR decline → in-session auggie fallback (strict-once)

```
[S5b_AUGGIE_FALLBACK]                                    ← NEW (FR-9 / FR-10)
   1. record decline_detected
   2. fallback_engaged := true; effective_max_rounds := min(max_rounds, 1)   (INV-R3, once)
   3. STRICT-ONCE GATE: record_idempotent("auggie_review_invoked", pr_number)
        already present → idempotency_skip → terminate (NEVER a 2nd invoke)   (INV-R2)
        newly recorded  → invoke /sc:auggie-review <PR> --depth quick
                          --remediation-offer --auggie-model claude-sonnet-4-6  (FR-9.3)
   4. auggie findings RE-ENTER the SAME pipeline:
        classify → re-grade (FR-3.1) → verify-before-remediate (FR-3.5)
        → route (FR-3.2) → S3_FIXING → S7_VALIDATING → S4_PUSHING …
      under a SEPARATE single-shot budget fallback_round_counter (cap 1).
   5. NO loop-back edge: after the one fallback cycle (or an immediate budget HALT),
      the FSM terminates. It NEVER re-enters S5a_RETRIGGER and NEVER re-invokes
      /sc:auggie-review. (The App declined; re-triggering it is futile and we
      deliberately do NOT take the decline comment's "comment augment review" bait —
      that is what R3 bounds.)
                                   │
                                   ▼
                 TERMINAL_CLEAN | HALT_MAX_ROUNDS (residual summary) | HALT_HUMAN
```

**Decline can fire at two poll points** (robustness): the **initial** `S2_CLASSIFY` poll
(the common case — an oversized PR is declined on PR-open before any push) **and** the
**`S5_AWAITING_REREVIEW`** re-trigger poll. Both route `declined → S5b_AUGGIE_FALLBACK`.

---

## 4. Functional Requirements (new)

### FR-8 — Post-push review re-trigger (R1)

| ID | Requirement | Test |
|----|-------------|------|
| FR-8.1 | After a successful L3 `push → reply → resolve`, the FSM enters `S5a_RETRIGGER_REVIEW`; the SKILL posts **exactly one** PR conversation comment with body `auggie review` via `gh api --method POST repos/IronbellyOrg/IronClaude/issues/<N>/comments -f body="auggie review"`. The DECISION (whether/when to re-trigger) is core; the `gh` post is SKILL I/O (NFR-6). | T-1101 |
| FR-8.2 | **[MOD]** `round_counter` increments **only** on the attributed re-review observed *after* the re-trigger (INV-001 edge unchanged); the V1.0 optimistic post-resolve increment (`fsm.py:793`) is REMOVED. A push with no subsequent attributed re-review does NOT advance the counter. | T-1102, **T-PUSH-WITHOUT-REREVIEW-NO-TICK** |
| FR-8.3 | The re-trigger comment is posted **at most once per remediation cycle**; `rereview_request_count <= max_rounds` (INV-R1). | T-1103 |
| FR-8.4 | The post-re-trigger poll waits for the `augmentcode[bot]` re-review **attributed to our pushed SHA** (reuse FR-2 poller; watermark = the re-trigger comment's `createdAt` / our `headRefOid`). A re-review not attributed to our push does NOT complete the cycle (INV-001 / INV-3). | T-1104 |
| FR-8.5 | The re-trigger token is one of the contract's accepted trigger phrases (`auggie review` canonical; `augment review` / `augmentcode review` also accepted), sourced from the locked `DetectionContract`, never a hard-coded literal in the deterministic core. | T-1105 (static grep: script emits `auggie review`; core holds no literal) |
| FR-8.6 | `S5a_RETRIGGER_REVIEW` is skipped (no comment posted) when the cycle did **not** push (`applied_edits == 0` / blocked G-push) — there is nothing to re-review. | T-1106 |

### FR-9 — Oversized-PR decline detection + auggie-review fallback (R2)

| ID | Requirement | Test |
|----|-------------|------|
| FR-9.1 | `classify()` gains a **4th state** `declined`. A comment is `declined` iff authored by `contract.augment_bot_login` **AND** body matches BOTH `contract.decline_phrase_regex` (default `/abnormally\s+large/i`) AND `contract.decline_retrigger_regex` (default `/comment\s+["']?(augment\|auggie\|augmentcode)\s+review["']?/i`) **AND** newer than the watermark. Requiring **both** phrase + re-trigger-instruction defeats false positives (e.g. a finding body that merely mentions "abnormally large"). | T-1110, T-1111, T-1112 |
| FR-9.2 | `declined` routes to `S5b_AUGGIE_FALLBACK` from **either** the initial `S2_CLASSIFY` poll (decline before any push) **or** the `S5_AWAITING_REREVIEW` re-trigger poll. | T-1113, T-1113b |
| FR-9.3 | The fallback invokes **`/sc:auggie-review <PR> --depth quick --remediation-offer --auggie-model claude-sonnet-4-6`** (exact flags; §2). The invocation is SKILL-side `> Skill sc:auggie-review-protocol`; the core only DECIDES to invoke (NFR-6). | T-1114, T-1115 (static parity vs `auggie-review.md`) |
| FR-9.4 | Fallback findings **re-enter the same pipeline**: `classify → re-grade (FR-3.1) → verify-before-remediate (FR-3.5) → route (FR-3.2) → S3_FIXING → S7_VALIDATING → S4_PUSHING`. They are NOT trusted verbatim — verify-before-remediate (C3a) still gates every fallback finding. | T-1116 |
| FR-9.5 | **Race / ordering:** at `S5_AWAITING_REREVIEW`, a genuine attributed re-review **wins over** a decline observed in the same poll window (review > decline — a real review means the App actually reviewed). A decline must be **watermarked after our re-trigger** comment; a stale pre-watermark decline is ignored (transient, keep polling). | T-1117, T-1118 |

### FR-10 — Fallback strict-once + budget clamp (R3, HARD safety constraint)

| ID | Requirement | Test |
|----|-------------|------|
| FR-10.1 | A **6th idempotency set** `auggie_review_invoked` (keyed on `pr_number`) is added to `run_log.IDEMPOTENCY_SETS`. The fallback gates on `record_idempotent("auggie_review_invoked", pr_number)`: first decline → record + invoke; any later decline → `idempotency_skip`, **never a second invoke**. `/sc:auggie-review` is invoked **AT MOST ONCE per PR**. | T-1120, **T-AUGGIE-AT-MOST-ONCE** |
| FR-10.2 | On first fallback engage, `effective_max_rounds := min(max_rounds, 1)`, recorded once via a `max_rounds_clamped` event; the value is **monotone non-increasing** over a run (INV-R3) — it can only tighten the bound. | T-1121 |
| FR-10.3 | The fallback runs a **separate single-shot sub-loop** governed by `fallback_round_counter` (cap 1, reusing `loop_guard.should_halt(fallback_round_counter, 1)`). It has **NO loop-back edge** (no `S5a_RETRIGGER`, no second `/sc:auggie-review`), so it terminates after **≤ 1** remediation cycle regardless of preceding Augment rounds. INV-001's `round_counter` is **frozen** at fallback entry and is untouched by the fallback. | T-1122, T-1123 |
| FR-10.4 | Strict-once and the clamp **survive `--resume`**: `auggie_review_invoked` and `effective_max_rounds` rebuild from the authoritative JSONL (`run_log.rebuild_state`). A resumed run that already invoked auggie-review NEVER invokes it again. | T-1124 |
| FR-10.5 | **Total push bound:** the Augment-driven loop pushes `≤ max_rounds`; the fallback adds `≤ 1` push (strict-once + cap-1). Therefore `push_count ≤ max_rounds + 1` (INV-R2). The `+1` is reachable at most once per PR. | T-1125 |

---

## 5. New Invariants (R3 normative)

> **INV-R1 (re-trigger boundedness).** A re-trigger comment is emitted at most once per
> completed push cycle, on the `RESOLVING → S5a_RETRIGGER_REVIEW` edge, and only when
> `applied_edits > 0`. `rereview_request_count` is monotonic and
> `rereview_request_count <= max_rounds`. The re-trigger does **not** itself increment
> `round_counter`; INV-001's edge and gate are unchanged.

> **INV-R2 (auggie strict-once + total-push bound).** `/sc:auggie-review` is invoked **at
> most once per PR**, guarded by the durable `auggie_review_invoked` idempotency set
> (comment-independent, survives resume). The fallback contributes **at most one** push.
> Consequently `push_count <= max_rounds + 1` for the whole run.

> **INV-R3 (clamp monotonicity / deterministic termination).** On fallback engage
> `effective_max_rounds := min(effective_max_rounds, 1)` — a one-way, monotone
> non-increasing clamp recorded once. The fallback sub-loop (`fallback_round_counter`,
> cap 1, no loop-back, no auggie re-invoke) guarantees termination structurally, not merely
> by budget. INV-001's monotonic `round_counter` and its `>=` HALT gate are preserved
> verbatim; the two counters are **independent** and neither can re-open the other's loop.

---

## 6. State-machine & core delta (build targets)

### 6.1 `models.py`

- **`MonitorState`** += `S5A_RETRIGGER_REVIEW = "S5a_RETRIGGER_REVIEW"`,
  `S5B_AUGGIE_FALLBACK = "S5b_AUGGIE_FALLBACK"`. Neither is terminal (omit from
  `TERMINAL_STATES`).
- **`EventType`** += (closed-enum delta — update the "EXACTLY N members" docstring):
  `REREVIEW_REQUESTED = "rereview_requested"`, `DECLINE_DETECTED = "decline_detected"`,
  `AUGGIE_FALLBACK_INVOKED = "auggie_fallback_invoked"`,
  `MAX_ROUNDS_CLAMPED = "max_rounds_clamped"`. (Reuse existing `FINDINGS_NORMALIZED`,
  `IDEMPOTENCY_SKIP`, the push triad, terminals for the fallback cycle.) → 33 → **37**.
- **`SkillResult`** += `rereview_request_count: int = 0`, `fallback_engaged: bool = False`,
  `auggie_review_invoked: bool = False`, `decline_detected: bool = False`,
  `effective_max_rounds: int | None = None`, `fallback_round_counter: int = 0`.

### 6.2 `classifier.py` / `detection.py`

- `STATE_DECLINED = "declined"`; `classify()` returns it when an Augment-authored comment
  matches the decline regexes (FR-9.1). Decline check runs **before** the clean/findings
  branch so a decline is never miscounted as findings.
- `DetectionContract` += `decline_phrase_regex`, `decline_retrigger_regex`,
  `accepted_trigger_phrases: list[str]` (defaults baked; probe-lockable). Extend
  `from_yaml`. Update the shipped `refs/detection-contract.md` YAML block with the new keys
  (still `locked: false` in source — T-210 unaffected).
- `is_decline(comment, contract, *, watermark) -> bool` — pure, watermark-aware.

### 6.3 `run_log.py`

- `IDEMPOTENCY_SETS += ("auggie_review_invoked",)` (now **6** sets).
- `rebuild_state()`: fold `AUGGIE_FALLBACK_INVOKED.pr_number` into `auggie_review_invoked`;
  fold `MAX_ROUNDS_CLAMPED.effective_max_rounds` into the rebuilt `effective_max_rounds`
  (take the **min** seen — monotone); count `REREVIEW_REQUESTED` into
  `rereview_request_count`.

### 6.4 `fsm.py`

- `transition()` new edges: `(RESOLVING, "resolved") → S5A_RETRIGGER_REVIEW` **[MOD]**
  (was `→ S5_AWAITING_REREVIEW`); `(S5A_RETRIGGER_REVIEW, "retriggered") → S5_AWAITING_REREVIEW`;
  `(S5_AWAITING_REREVIEW, "declined") → S5B_AUGGIE_FALLBACK`;
  `(S2_CLASSIFY, "declined") → S5B_AUGGIE_FALLBACK`;
  `(S5B_AUGGIE_FALLBACK, "fallback_findings") → S2_CLASSIFY` (re-enter, fallback budget);
  `(S5B_AUGGIE_FALLBACK, "fallback_skip") → HALT_MAX_ROUNDS|TERMINAL_CLEAN`.
- `run_skill()` **[MOD]**: remove the optimistic `round_counter += 1` (line 793); tick only
  on an injected attributed-re-review outcome after the re-trigger. New `RunConfig` seams:
  `do_retrigger: Callable[..., None] = _noop`, `invoke_auggie_review: Callable[..., None] = _noop`,
  and a per-cycle `rereview_outcome` sequence (`"attributed" | "declined" | "timeout"`) so the
  test harness drives R1/R2 deterministically.
- `clamp_max_rounds(effective, hard=1) -> int = min(effective, hard)` (pure).
- Fallback sub-loop uses `loop_guard.should_halt(fallback_round_counter, 1)`.
- **Core purity (NFR-6 / AC-9):** no `gh`/`git` token in any of the above; the `gh api`
  comment-post and the `> Skill sc:auggie-review-protocol` call are SKILL-only. T-N50 extended
  to scan the two new refs.

### 6.5 SKILL + refs

- **`SKILL.md`** Wave 6 [MOD]: after `reply → resolve`, post the `auggie review` comment
  (S5a) then poll (S5). New **Wave 6b (decline fallback)**: on `declined`, strict-once
  gate → `> Skill sc:auggie-review-protocol` with the §2 flags → re-enter Waves 2–6 once
  under the clamp. Update the Output Contract `status` enum with `terminal_fallback_*` if
  desired (or reuse `terminal_clean`/`terminal_max_rounds`).
- **New ref `refs/review-retrigger.md`** (R1): the re-trigger comment surface + watermark +
  INV-R1.
- **New ref `refs/auggie-fallback.md`** (R2/R3): decline detection, strict-once, clamp,
  re-entry contract, the §2 flag table, and the "do NOT take the App's `augment review`
  bait" rationale.
- **`refs/augment-poll.md`** [MOD]: document the 4th `declined` state + decline surfaces
  (`gh api …/issues/<N>/comments` for the conversation-comment decline).
- **`refs/loop-guard.md`** [MOD]: add INV-R1/R2/R3 and the independent `fallback_round_counter`.
- **New script `scripts/retrigger-review.sh`**: one `gh api …/issues/<N>/comments` POST of the
  trigger token (pins `--repo`/path to the fork).

---

## 7. Edge-Case & Boundary additions

| EC | Scenario | Expected | Test |
|----|----------|----------|------|
| EC-17 | Push lands, re-trigger posted, re-review attributed to our SHA | `round_counter += 1`; loop continues; `rereview_request_count == round_counter` | T-1101, T-1104 |
| EC-18 | Push lands, re-trigger posted, **no** re-review before timeout | `TERMINAL_TIMEOUT`; `round_counter` NOT advanced (the V1.0 bug, now caught) | T-PUSH-WITHOUT-REREVIEW-NO-TICK |
| EC-19 | PR oversized → decline on the **initial** poll (no push yet) | `S5b`; auggie-review invoked once; one fallback cycle; terminate | T-1113b, T-AUGGIE-AT-MOST-ONCE |
| EC-20 | Decline after a push (re-trigger declined) | `S5b`; round_counter frozen; fallback sub-loop ≤ 1 cycle | T-1113, T-1122 |
| EC-21 | **Two** declines in one run (e.g. decline → fallback push → decline again) | 2nd decline → `idempotency_skip`; auggie-review NOT re-invoked; terminate | T-AUGGIE-AT-MOST-ONCE |
| EC-22 | Re-review **and** decline both present at one `S5` poll | review wins (FR-9.5); proceed as attributed re-review | T-1117 |
| EC-23 | Stale decline (pre-watermark) at `S5` | ignored; keep polling | T-1118 |
| EC-24 | Resume after auggie-review already invoked | `auggie_review_invoked` rebuilt; no second invoke | T-1124 |

---

## 8. Acceptance Criteria (new)

| ID | Criterion | Verification |
|----|-----------|--------------|
| AC-16 | After an L3 push, exactly one `auggie review` comment is posted and the next round opens only on the attributed re-review (loop actually advances) | T-1101 + T-1104 |
| AC-17 | A push with no ensuing attributed re-review does NOT advance `round_counter` (V1.0 broken-loop regression) | T-PUSH-WITHOUT-REREVIEW-NO-TICK |
| AC-18 | `rereview_request_count <= max_rounds` for every run (INV-R1) | T-1103 |
| AC-19 | The "abnormally large" decline (and only it) → `declined` → `S5b` from both poll points; non-decline Augment comments do not trigger fallback | T-1111, T-1112, T-1113, T-1113b |
| AC-20 | The fallback invokes the exact `/sc:auggie-review … --depth quick --remediation-offer --auggie-model claude-sonnet-4-6` and its findings re-enter verify-before-remediate | T-1114, T-1116 |
| AC-21 (HARD) | `/sc:auggie-review` is invoked **at most once per PR** across declines, fallback cycles, and `--resume`; `push_count <= max_rounds + 1`; deterministic termination (no loop-back) | T-AUGGIE-AT-MOST-ONCE, T-1124, T-1125, T-1122 |

---

## 9. Coverage Matrix (new → test)

```
FR-8.1 → T-1101            FR-9.1 → T-1110, T-1111, T-1112      FR-10.1 → T-1120, T-AUGGIE-AT-MOST-ONCE
FR-8.2 → T-1102, T-PUSH-WITHOUT-REREVIEW-NO-TICK               FR-10.2 → T-1121
FR-8.3 → T-1103           FR-9.2 → T-1113, T-1113b             FR-10.3 → T-1122, T-1123
FR-8.4 → T-1104          FR-9.3 → T-1114, T-1115              FR-10.4 → T-1124
FR-8.5 → T-1105         FR-9.4 → T-1116                      FR-10.5 → T-1125
FR-8.6 → T-1106        FR-9.5 → T-1117, T-1118
INV-R1 → T-1103, EC-17/18      INV-R2 → T-AUGGIE-AT-MOST-ONCE, T-1125      INV-R3 → T-1121, T-1122
AC-16 → T-1101,T-1104  AC-17 → T-PUSH-WITHOUT-REREVIEW-NO-TICK  AC-18 → T-1103
AC-19 → T-1111,T-1112,T-1113,T-1113b  AC-20 → T-1114,T-1116  AC-21 → T-AUGGIE-AT-MOST-ONCE,T-1124,T-1125,T-1122
```

### 9.1 New / extended test files (`tests/pr_submit/`)

| File | Adds |
|------|------|
| `test_review_retrigger.py` (new) | T-1101..T-1106, T-PUSH-WITHOUT-REREVIEW-NO-TICK |
| `test_auggie_fallback.py` (new) | T-1110..T-1118, T-1120..T-1125, T-AUGGIE-AT-MOST-ONCE |
| `test_detection_contract.py` (ext) | decline regexes, 4th `declined` state, watermark |
| `test_idempotency.py` (ext) | `auggie_review_invoked` 6th set, resume strict-once |
| `test_loop_guard.py` (ext) | INV-R1/R3, deferred increment, `fallback_round_counter` cap-1 |
| `test_run_log.py` (ext) | 4 new event types, 37-member enum, clamp/min fold |
| `test_static_grep.py` (ext) | T-N50 scans `review-retrigger.md` + `auggie-fallback.md`; T-1105/T-1115 |
| `fixtures/` | `decline-comment.json`, `rereview-attributed.json`, `rereview-then-decline.json`, `decline-initial-poll.json`, `decline-twice.json`, `stale-decline-pre-watermark.json`, `auggie-fallback-findings.json` |

---

## 10. Preserved-constraints checklist (NFR fidelity)

- **NFR-6 core purity:** every new DECISION (re-trigger gating, decline classification,
  strict-once, clamp arithmetic, fallback budget) is pure in `superclaude.pr_submit`; the
  `gh api` comment-post and `/sc:auggie-review` invocation are SKILL I/O. T-N50 extended.
- **INV-001 verbatim:** unchanged edge, `>=` gate, monotonicity, `max_rounds=N ⇒ N pushes`
  for the Augment-driven loop. R1 only relocates the increment to the real attributed
  re-review (the code now matches the spec it always claimed).
- **Run-log / idempotency patterns:** the 6th set follows the existing
  `record_idempotent`/`rebuild_state` pattern; the 4 new events follow the closed-enum
  validation in `run_log.append`. Write-ahead discipline (§11.1) applies to
  `rereview_requested` and `auggie_fallback_invoked` (fsync **before** the SKILL acts).
- **Determinism:** two independent, monotone counters (`round_counter`,
  `fallback_round_counter`); no loop-back from the fallback; strict-once on auggie-review →
  the run is finite and replay-deterministic (NFR-8).

---

## 11. Open decisions for the operator (none blocking build)

1. **Status enum granularity:** reuse `terminal_clean`/`terminal_max_rounds` for fallback
   outcomes (default, minimal) vs add `terminal_fallback_clean`/`terminal_fallback_residual`
   for sharper telemetry. *Recommendation: reuse (smaller surface); revisit if dashboards need it.*
2. **Re-trigger token after a decline:** V1.1 deliberately does **not** re-comment
   `augment review` to force the App (R3 token-bounding). If a future operator wants a
   single forced App re-review before the in-session fallback, that is a V1.2 choice, not
   V1.1.

---

**Hand-off:** this addendum + `merged-spec.md` are jointly build-ready. Next:
`task-builder` → MDTM tasklist → `/sc:reflect --mode pre` (catches the INV-001 deferred-increment
and strict-once predicates) → execute.
