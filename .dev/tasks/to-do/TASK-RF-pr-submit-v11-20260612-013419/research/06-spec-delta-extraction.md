# R6 — Spec Delta Extraction (Builder's Spec Index)

**Track:** Solution/Spec Mapping + Template & Examples
**Researcher:** R6
**Status:** Complete
**Date:** 2026-06-12

## Purpose

This is the **builder's spec index**: a single authoritative mapping the task-builder
uses to create one checklist item per delta with its verifying test. It restates the
DESIGN INTENT (the spec is source-of-truth for intent; the codebase is source-of-truth
for current HOW — owned by R1-R5; spec citations verified by R7).

**Sources:**
- Driving spec: `.dev/brainstorms/20260610-234750-pr-review-auto-remediation/merged-spec-v1.1-addendum.md`
- Parent spec (V1.0): `.dev/brainstorms/20260610-234750-pr-review-auto-remediation/merged-spec.md` (where [MOD])
- MDTM template: `.claude/templates/workflow/02_mdtm_template_complex_task.md`
- V1.0 exemplar task: `.dev/tasks/to-do/TASK-RF-submit-pr-20260611-030241/TASK-RF-submit-pr-20260611-030241.md`

---

## 0. Naming reconciliation (binding) — `sc:pr-submit`, NOT `sc:submit-pr`

**[MOD]** (addendum §0). V1.0 §1.1 (merged-spec.md:33) named the skill `sc:submit-pr` and the
package `sc-submit-pr-protocol` / tests `tests/submit_pr/`. **The shipped code settled on
`sc:pr-submit`.** V1.1 anchors to the LIVE names — the builder MUST emit only these:

| V1.0 (stale) | V1.1 / LIVE (use these) |
|---|---|
| skill `sc:submit-pr` | `sc:pr-submit` |
| skill dir `sc-submit-pr-protocol` | `sc-pr-submit-protocol` (`SKILL.md:1` `name: sc:pr-submit-protocol`) |
| package `superclaude.submit_pr` | `superclaude.pr_submit` |
| tests `tests/submit_pr/` | `tests/pr_submit/` |
| const | `fsm.PR_TARGET_REPO` |

No behavior change — a name-faithfulness correction. Every V1.0 reference reads as its
`pr-submit`/`pr_submit` equivalent.

---

## 1. Root-cause (why this build exists — design intent)

V1.0's loop assumed **pushing a remediation commit causes Augment to re-review**. Per memory
`reference_augment_review_triggers` (verified 2026-06-11): `augmentcode[bot]` reviews **only** on
(a) PR open / draft→ready, or (b) a PR conversation comment matching `auggie review` /
`augment review` / `augmentcode review`. **Pushing commits does NOT auto-trigger a review.** An
abnormally-large PR is instead **DECLINED** with a comment.

**Consequence (the bug):** after V1.0's L3 push, no re-review arrives → the `S5 → S2` edge is
unreachable → `round_counter` never advances → loop stalls until `TERMINAL_TIMEOUT`. The live
code (spec claims `fsm.run_skill`, `fsm.py:792-793`) papers over this with an **optimistic
post-resolve increment** not tied to any real re-review → multi-round remediation is fictional.
*(Spec claim — R7 verifies `fsm.py:792-793`.)*

**V1.1's three behaviors (the build):**

| R | Behavior | Primary FR |
|---|----------|-----------|
| **R1** | After each L3 push, post one `auggie review` PR comment, then poll for attributed re-review. Bounded by `--max-rounds`. | **FR-8** |
| **R2** | If Augment posts "abnormally large" decline, fall back to in-session `/sc:auggie-review <PR> --depth quick --remediation-offer --auggie-model claude-sonnet-4-6`. | **FR-9** |
| **R3** (HARD) | On fallback: clamp budget to `--max-rounds=1` AND guarantee `/sc:auggie-review` invoked **at most once per PR** via new `auggie_review_invoked` idempotency set. | **FR-10** |

---

## 2. R2 fallback command — VALIDATED flags (addendum §2)

Fallback string (exact): `/sc:auggie-review <PR> --depth quick --remediation-offer
--auggie-model claude-sonnet-4-6`. Each flag verified by the spec against
`src/superclaude/commands/auggie-review.md` *(spec claims; R7 re-verifies line refs)*:

| Flag/value | Spec-cited source line | Verdict |
|---|---|---|
| `--depth quick` | `auggie-review.md:49` (`quick\|standard\|deep`) | valid value |
| `--remediation-offer` | `auggie-review.md:52` (default `true`) | valid flag |
| `--auggie-model claude-sonnet-4-6` | `auggie-review.md:55` (exact example) | valid flag + value |
| `<PR-number>` target | `auggie-review.md:26-27,36` | valid target |

`--post-pr` defaults `true` for a PR target (`auggie-review.md:50`) → fallback review posts
WITHOUT an extra flag; do NOT pass `--no-post-pr`. `--depth quick` is the deliberate
token-bounded choice for R3.

---

## 3. Functional Requirements (TRANSCRIBED verbatim from addendum §4)

> Builder rule: **one checklist item per FR sub-ID, each carrying its test ID(s).**

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

## 4. New Invariants (TRANSCRIBED verbatim from addendum §5 — builder MUST embed for literal QA)

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

**[MOD] anchor for INV-001 (parent merged-spec.md §9.1, lines 600-606) — PRESERVED VERBATIM:**
> `round_counter` increments by exactly 1 at the single FSM transition
> `S5_AWAITING_REREVIEW --[review_observed ∧ sha_attributed_to_our_push]--> S2_CLASSIFY`, and
> **nowhere else**. Gate `round_counter >= max_rounds ⇒ HALT_MAX_ROUNDS` evaluated before opening
> each fix cycle. User-facing label = `round_counter + 1`. `max_rounds=N` → exactly N pushes.

V1.1 only **relocates** the increment from the live code's optimistic post-resolve site
(`fsm.py:793`) to the **actually-observed attributed re-review** after the re-trigger — making
the code match INV-001's literal definition. Edge, `>=` gate, monotonicity, `N⇒N pushes` all
unchanged. (FR-3.1 re-grade, FR-3.5 verify-before-remediate, FR-3.2 route also unchanged — the
fallback re-enters this same V1.0 pipeline.)

---

## 5. Build-target deltas — PER-FILE list (addendum §6)

> Builder rule: **one item per file-delta bullet.** Each names the exact symbol/constant to
> add. All `:line` are SPEC CLAIMS — R7 verifies; R1-R5 own current code state.

### 5.1 `src/superclaude/pr_submit/models.py` (§6.1)
- `MonitorState` += `S5A_RETRIGGER_REVIEW = "S5a_RETRIGGER_REVIEW"`, `S5B_AUGGIE_FALLBACK = "S5b_AUGGIE_FALLBACK"`. **Neither terminal** (omit from `TERMINAL_STATES`).
- `EventType` += 4 members: `REREVIEW_REQUESTED = "rereview_requested"`, `DECLINE_DETECTED = "decline_detected"`, `AUGGIE_FALLBACK_INVOKED = "auggie_fallback_invoked"`, `MAX_ROUNDS_CLAMPED = "max_rounds_clamped"`. **Closed-enum count delta: 33 → 37** (update the "EXACTLY N members" docstring). Reuse existing `FINDINGS_NORMALIZED`, `IDEMPOTENCY_SKIP`, push triad, terminals for the fallback cycle.
- `SkillResult` += 6 fields: `rereview_request_count: int = 0`, `fallback_engaged: bool = False`, `auggie_review_invoked: bool = False`, `decline_detected: bool = False`, `effective_max_rounds: int | None = None`, `fallback_round_counter: int = 0`.

### 5.2 `src/superclaude/pr_submit/classifier.py` + `detection.py` (§6.2)
- `STATE_DECLINED = "declined"`; `classify()` returns it on Augment-authored comment matching decline regexes (FR-9.1). **Decline check runs BEFORE the clean/findings branch** (so a decline is never miscounted as findings).
- `DetectionContract` += `decline_phrase_regex`, `decline_retrigger_regex`, `accepted_trigger_phrases: list[str]` (defaults baked; probe-lockable). Extend `from_yaml`. Update shipped `refs/detection-contract.md` YAML block with new keys (**still `locked: false` in source — T-210 unaffected**).
- New pure fn `is_decline(comment, contract, *, watermark) -> bool` — watermark-aware.

### 5.3 `src/superclaude/pr_submit/run_log.py` (§6.3)
- `IDEMPOTENCY_SETS += ("auggie_review_invoked",)` → now **6 sets**.
- `rebuild_state()`: fold `AUGGIE_FALLBACK_INVOKED.pr_number` → `auggie_review_invoked`; fold `MAX_ROUNDS_CLAMPED.effective_max_rounds` → rebuilt `effective_max_rounds` (**take the min seen — monotone**); count `REREVIEW_REQUESTED` → `rereview_request_count`.

### 5.4 `src/superclaude/pr_submit/fsm.py` (§6.4)
- `transition()` new edges:
  - `(RESOLVING, "resolved") → S5A_RETRIGGER_REVIEW` **[MOD]** (was `→ S5_AWAITING_REREVIEW`)
  - `(S5A_RETRIGGER_REVIEW, "retriggered") → S5_AWAITING_REREVIEW`
  - `(S5_AWAITING_REREVIEW, "declined") → S5B_AUGGIE_FALLBACK`
  - `(S2_CLASSIFY, "declined") → S5B_AUGGIE_FALLBACK`
  - `(S5B_AUGGIE_FALLBACK, "fallback_findings") → S2_CLASSIFY` (re-enter, fallback budget)
  - `(S5B_AUGGIE_FALLBACK, "fallback_skip") → HALT_MAX_ROUNDS|TERMINAL_CLEAN`
- `run_skill()` **[MOD]**: **remove the optimistic `round_counter += 1` (spec claims line 793)**; tick only on an injected attributed-re-review outcome after the re-trigger. New `RunConfig` seams: `do_retrigger: Callable[..., None] = _noop`, `invoke_auggie_review: Callable[..., None] = _noop`, and a per-cycle `rereview_outcome` sequence (`"attributed" | "declined" | "timeout"`) for deterministic test driving.
- New pure fn `clamp_max_rounds(effective, hard=1) -> int = min(effective, hard)`.
- Fallback sub-loop uses `loop_guard.should_halt(fallback_round_counter, 1)`.
- **Core purity (NFR-6 / AC-9):** NO `gh`/`git` token in any of the above. T-N50 extended to scan the two new refs.

### 5.5 SKILL + refs + script (§6.5)
- **`refs/.../SKILL.md` Wave 6 [MOD]:** after `reply → resolve`, post `auggie review` comment (S5a) then poll (S5). New **Wave 6b (decline fallback):** on `declined`, strict-once gate → `> Skill sc:auggie-review-protocol` with §2 flags → re-enter Waves 2–6 once under the clamp. Optionally extend Output Contract `status` enum with `terminal_fallback_*` (or reuse `terminal_clean`/`terminal_max_rounds`).
- **NEW ref `refs/review-retrigger.md`** (R1): re-trigger comment surface + watermark + INV-R1.
- **NEW ref `refs/auggie-fallback.md`** (R2/R3): decline detection, strict-once, clamp, re-entry contract, §2 flag table, "do NOT take the App's `augment review` bait" rationale.
- **`refs/augment-poll.md` [MOD]:** document 4th `declined` state + decline surfaces (`gh api …/issues/<N>/comments`).
- **`refs/loop-guard.md` [MOD]:** add INV-R1/R2/R3 + the independent `fallback_round_counter`.
- **NEW script `scripts/retrigger-review.sh`:** one `gh api …/issues/<N>/comments` POST of the trigger token (pins `--repo`/path to the fork).

---

## 6. Edge-Case table (TRANSCRIBED verbatim from addendum §7)

| EC | Scenario | Expected | Test |
|----|----------|----------|------|
| EC-17 | Push lands, re-trigger posted, re-review attributed to our SHA | `round_counter += 1`; loop continues; `rereview_request_count == round_counter` | T-1101, T-1104 |
| EC-18 | Push lands, re-trigger posted, **no** re-review before timeout | `TERMINAL_TIMEOUT`; `round_counter` NOT advanced (the V1.0 bug, now caught) | T-PUSH-WITHOUT-REREVIEW-NO-TICK |
| EC-19 | PR oversized → decline on the **initial** poll (no push yet) | `S5b`; auggie-review invoked once; one fallback cycle; terminate | T-1113b, T-AUGGIE-AT-MOST-ONCE |
| EC-20 | Decline after a push (re-trigger declined) | `S5b`; round_counter frozen; fallback sub-loop ≤ 1 cycle | T-1113, T-1122 |
| EC-21 | **Two** declines in one run (decline → fallback push → decline again) | 2nd decline → `idempotency_skip`; auggie-review NOT re-invoked; terminate | T-AUGGIE-AT-MOST-ONCE |
| EC-22 | Re-review **and** decline both present at one `S5` poll | review wins (FR-9.5); proceed as attributed re-review | T-1117 |
| EC-23 | Stale decline (pre-watermark) at `S5` | ignored; keep polling | T-1118 |
| EC-24 | Resume after auggie-review already invoked | `auggie_review_invoked` rebuilt; no second invoke | T-1124 |

---

## 7. Acceptance Criteria (TRANSCRIBED verbatim from addendum §8)

| ID | Criterion | Verification |
|----|-----------|--------------|
| AC-16 | After an L3 push, exactly one `auggie review` comment is posted and the next round opens only on the attributed re-review (loop actually advances) | T-1101 + T-1104 |
| AC-17 | A push with no ensuing attributed re-review does NOT advance `round_counter` (V1.0 broken-loop regression) | T-PUSH-WITHOUT-REREVIEW-NO-TICK |
| AC-18 | `rereview_request_count <= max_rounds` for every run (INV-R1) | T-1103 |
| AC-19 | The "abnormally large" decline (and only it) → `declined` → `S5b` from both poll points; non-decline Augment comments do not trigger fallback | T-1111, T-1112, T-1113, T-1113b |
| AC-20 | The fallback invokes the exact `/sc:auggie-review … --depth quick --remediation-offer --auggie-model claude-sonnet-4-6` and its findings re-enter verify-before-remediate | T-1114, T-1116 |
| AC-21 (HARD) | `/sc:auggie-review` is invoked **at most once per PR** across declines, fallback cycles, and `--resume`; `push_count <= max_rounds + 1`; deterministic termination (no loop-back) | T-AUGGIE-AT-MOST-ONCE, T-1124, T-1125, T-1122 |

---

## 8. Coverage Matrix FR→test (TRANSCRIBED verbatim from addendum §9)

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

### 8.1 New/extended test files (TRANSCRIBED from addendum §9.1) — `tests/pr_submit/`

| File | Status | Adds |
|------|--------|------|
| `test_review_retrigger.py` | NEW | T-1101..T-1106, T-PUSH-WITHOUT-REREVIEW-NO-TICK |
| `test_auggie_fallback.py` | NEW | T-1110..T-1118, T-1120..T-1125, T-AUGGIE-AT-MOST-ONCE |
| `test_detection_contract.py` | EXT | decline regexes, 4th `declined` state, watermark |
| `test_idempotency.py` | EXT | `auggie_review_invoked` 6th set, resume strict-once |
| `test_loop_guard.py` | EXT | INV-R1/R3, deferred increment, `fallback_round_counter` cap-1 |
| `test_run_log.py` | EXT | 4 new event types, 37-member enum, clamp/min fold |
| `test_static_grep.py` | EXT | T-N50 scans `review-retrigger.md` + `auggie-fallback.md`; T-1105/T-1115 |
| `fixtures/` | NEW | `decline-comment.json`, `rereview-attributed.json`, `rereview-then-decline.json`, `decline-initial-poll.json`, `decline-twice.json`, `stale-decline-pre-watermark.json`, `auggie-fallback-findings.json` |

---

## 9. Preserved-constraints checklist (TRANSCRIBED verbatim from addendum §10 — NFR fidelity)

- **NFR-6 core purity:** every new DECISION (re-trigger gating, decline classification, strict-once, clamp arithmetic, fallback budget) is pure in `superclaude.pr_submit`; the `gh api` comment-post and `/sc:auggie-review` invocation are SKILL I/O. T-N50 extended. *(Parent merged-spec.md:806 — NFR-6: "FSM, router, loop-guard contain zero `gh`/`git` calls"; AC-9 / T-N50 static scan.)*
- **INV-001 verbatim:** unchanged edge, `>=` gate, monotonicity, `max_rounds=N ⇒ N pushes` for the Augment-driven loop. R1 only relocates the increment to the real attributed re-review (the code now matches the spec it always claimed).
- **Run-log / idempotency patterns:** the 6th set follows the existing `record_idempotent`/`rebuild_state` pattern; the 4 new events follow closed-enum validation in `run_log.append`. Write-ahead discipline (parent §11.1) applies to `rereview_requested` and `auggie_fallback_invoked` (fsync **before** the SKILL acts).
- **Determinism:** two independent, monotone counters (`round_counter`, `fallback_round_counter`); no loop-back from fallback; strict-once on auggie-review → the run is finite and replay-deterministic (NFR-8).

### 9.1 Spec-cited line claims for R7 to verify (do NOT re-verify here)
- `fsm.py:792-793` — the optimistic post-resolve `round_counter += 1` to be REMOVED (addendum §1, §3.1, §6.4).
- `SKILL.md:1` — `name: sc:pr-submit-protocol` (addendum §0).
- `auggie-review.md:49,50,52,55,26-27,36` — fallback flag sources (addendum §2).
- `run_log.IDEMPOTENCY_SETS` currently has 5 sets (→6); `EventType` currently 33 members (→37) (addendum §6.1/§6.3 — R1-R5 confirm current counts).
- parent merged-spec.md:806 (NFR-6), :600-606 (INV-001), :236 (FR-6.3 INV-001 verbatim).

---

## 10. MDTM template rules the BUILDER MUST OBEY

Source: `.claude/templates/workflow/02_mdtm_template_complex_task.md`. Rule ID + 1-line summary
+ the line anchor (for the builder to quote into the task file's compliance header).

### Granularity & item-shape rules

| Rule | Line | 1-line summary (builder obligation) |
|------|------|-------------------------------------|
| **A3 — Complete Granular Breakdown** | :108 | Break EVERY phase into atomic, verifiable items; **one item per file/component/iteration**; NO bulk ops; exact paths + measurable outcomes. → one item per §6 file-delta + one per FR sub-ID. |
| **A4 — Iterative Process Structure** | :114 | For any multi-item process: **pre-enumerate ALL items** in an initial step → one item each → incremental updates → consolidation step last. (Step X.1 enumerate / X.2 per-item / X.3 consolidate.) |
| **B2 — Self-Contained Item (6-element shape)** | :159 | EVERY item is a complete standalone paragraph embedding: (1) Context-ref + WHY, (2) Action + WHY, (3) Output spec (exact path/template), (4) Integrated "ensuring…" verification (no fabrication; 100% source-derived), (5) Evidence-on-failure-only to Task Log, (6) explicit completion gate. **One full paragraph, not bullets** (B3). NO standalone "read context" items (B5). |

### QA-gate rules

| Rule | Line | 1-line summary (builder obligation) |
|------|------|-------------------------------------|
| **M3 — Lens-Based QA Sequence** | :1059 | The MANDATORY 8-step gate (replaces deprecated M1): **Step1** aggregate (L6) → **Step2** rf-qa structural lenses in PARALLEL `fix_authorization:false` → **Step3** rf-qa-qualitative content lenses PARALLEL → **Step4** domain lenses (if any) → **Step5** consolidate to `${TASK_DIR}qa/qa-consolidated-findings.md` → **Step6** ONE fix agent `fix_authorization:true` → **Step7** ≥2 verification agents (1 rf-qa + 1 rf-qa-qualitative) `false` → **Step8** conditional proceed (L5; FAIL → repeat 5-7, max cycles per I16). EVERY step is its own `- [ ]` item (no collapsing). |
| **M4 — Source-Document Fidelity Gate** | :1098 | Runs AFTER M3. Agents read BOTH source inputs AND output to verify faithful representation. Applicability per I21. |
| **I19 — Lens-Based QA Minimum Agents** | :699 | FLOORS (full intensity): Final/Assembled output <500 ln = **6** (3 rf-qa + 3 rf-qa-qualitative); 500-1500 = **8**; 1500-3000 = **10**; >3000 = **12**. Intermediate gates = **5** (research: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative; synthesis: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative; task-integrity: 2 rf-qa + 2 rf-qa-qualitative + 1 rf-analyst). Domain lenses ADD on top. Gates below floor are REJECTED at validation. Adversarial framing mandatory ("Assume ≥N errors on your lens; N=5/10/15/20 by size"). I22 reduces these at lite/standard intensity. |
| **I20 — Serialized Fix Authorization** | :745 | When 3+ agents touch the same file, fixes MUST serialize: (1) all report `false`, (2) consolidate, (3) **ONE** fix agent `true` applies ALL, (4) ≥2 verify, (5) re-cycle from consolidation if verify fails (max per I16; HALT+escalate after 3). Parallel fix authorization PROHIBITED. Applies at ALL intensity levels (:838). |
| **I21 — Source-Document Fidelity Gate Requirement** | :759 | Mandatory when outputs derive from source docs. Checks: semantic coverage, detail preservation, cross-source contradiction, **phantom-coverage detection** (verify each matrix ID by reading the actual task/section, not just ID presence), operational/compliance completeness. Min **2** fidelity agents (3-4 if source >1000 ln). Report `${TASK_DIR}qa/qa-source-fidelity-report.md`. Runs AFTER M3. |

**Builder-relevant nuances for THIS task:**
- **I21 applicability:** This is a *code-from-spec* build (source = the V1.1 addendum + V1.0 spec). Per I21's list ("Any task where the orchestrator reads source documents to produce output"), a fidelity gate is in-scope — fidelity agents check the FR/INV/EC/AC deltas land in code+tests, with **phantom-coverage detection** especially relevant against the §9 coverage matrix (verify each T-ID is a real test, not just a row).
- **M3 lens sizing:** the produced TASK FILE itself is the assembled output the post-completion M3 gate validates; agent floor scales by its line count per I19.
- **Domain lenses to add on top (recommended by spec shape):** an **INV-fidelity lens** (INV-001 verbatim + INV-R1/R2/R3 arithmetic — `push_count ≤ max_rounds+1`, monotone clamp), a **closed-enum lens** (33→37 EventType, 5→6 idempotency sets), and a **core-purity lens** (NFR-6: no `gh`/`git` token in core) — these mirror the sc:reflect blindspots called out in the addendum hand-off (§11) and memory `feedback_sc_reflect_vs_inline_rfqa`.

---
