# R7 — Doc Cross-Validator: Spec Claims vs Current Code

**Task:** TASK-RF-pr-submit-v11-20260612-013419
**Researcher:** R7 (Doc Staleness / Code Cross-Validation)
**Spec under verification:** `.dev/brainstorms/20260610-234750-pr-review-auto-remediation/merged-spec-v1.1-addendum.md`
**Code roots:** `src/superclaude/pr_submit/`, `src/superclaude/skills/sc-pr-submit-protocol/`, `src/superclaude/commands/auggie-review.md`
**Date:** 2026-06-12

Status: COMPLETE

Tags: **[CODE-VERIFIED]** = confirmed at file:line | **[CODE-CONTRADICTED]** = code differs | **[UNVERIFIED]** = not found / planned

**Headline:** The spec's concrete code anchors are accurate. The single most-cited anchor (`fsm.py:793` optimistic increment) is EXACT. All "current state" claims (33 EventType members, 5 idempotency sets, 3-state classifier, missing decline fields, S5 present / no S5a/S5b, loop_guard signature, NFR-6 core purity) are CONFIRMED. The §6.5 NEW-vs-EXISTING ref/script split is accurate. The only stale anchors are the **§2 flag-table line numbers** for `auggie-review.md` — the flags and values all EXIST and are valid, but several cited line numbers are off by a few lines.

---

## Verification Table

| # | Claim (spec) | Spec loc | Current code state (file:line) | Tag |
|---|---|---|---|---|
| 1 | `fsm.py:793` holds optimistic `result.round_counter += 1` (FR-8.2: REMOVE) | §1, FR-8.2, §3.1, §6.4 | `fsm.py:793` is EXACTLY `result.round_counter += 1`, preceded by comment `# Re-review attributed to our push: tick the monotonic round counter (INV-001).` at :792 | **[CODE-VERIFIED]** |
| 2 | `fsm.run_skill` / `fsm.py:792-793` papers over loop with optimistic post-resolve increment | §1, FR-8.2 | `def run_skill(...)` at `fsm.py:679`; the increment at :793 fires unconditionally right after `do_push/do_reply/do_resolve` (:785-789) and after setting `state = S5_AWAITING_REREVIEW` (:790) — NO real re-review observation gates it. Confirms "optimistic, decoupled from any observed re-review." | **[CODE-VERIFIED]** |
| 3 | `models.EventType` docstring "EXACTLY 33 members" and there are exactly 33 (§6.1: 33→37) | §6.1, FR-G | `models.py:20` docstring `Closed enum ... — EXACTLY 33 members.`; member count = **33** (awk between `class EventType` and `class Severity`). `run_log.py:103-110` `append()` error msg also says "not one of the 33". | **[CODE-VERIFIED]** |
| 4 | `models.MonitorState` has `S5_AWAITING_REREVIEW`, NO S5a/S5b yet | §6.1 | `models.py:104` `S5_AWAITING_REREVIEW = "S5_AWAITING_REREVIEW"`. No `S5A_*` / `S5B_*` members present (members :94-113). | **[CODE-VERIFIED]** |
| 5 | `run_log.IDEMPOTENCY_SETS` currently has exactly 5 sets (§6.3 adds 6th) | §6.3, FR-10.1 | `run_log.py:27-33` tuple = `processed_review_ids`, `processed_finding_ids`, `replied_comment_ids`, `resolved_thread_ids`, `pushed_commit_shas` = **5**. Comment at :26 says "The 5 idempotency sets (§11.4)." No `auggie_review_invoked`. | **[CODE-VERIFIED]** |
| 6 | `classifier.classify()` returns polling/clean/findings (no `declined`) | §6.2, FR-9.1 | `classifier.py:17-19` `STATE_POLLING/CLEAN/FINDINGS`; `classify()` :60-86 returns only those three. No `declined`/`STATE_DECLINED`. | **[CODE-VERIFIED]** |
| 7 | `detection.DetectionContract` has `from_yaml` + `augment_bot_login`, NO decline_phrase_regex / decline_retrigger_regex / accepted_trigger_phrases | §6.2, FR-9.1 | `detection.py:55-89`: dataclass field `augment_bot_login` (:64); `from_yaml` classmethod (:74-89). Fields list (:64-72) has NONE of the three new keys; `from_yaml` (:77-88) does not parse them. | **[CODE-VERIFIED]** |
| 8 | `loop_guard.should_halt(round_counter, max_rounds)` exists with that signature | FR-10.3 | `loop_guard.py:23` `def should_halt(round_counter: int, max_rounds: int) -> bool:` returning `round_counter >= max_rounds` (:30). Exact signature match. | **[CODE-VERIFIED]** |
| 9a | `--depth quick` at `auggie-review.md:~49`, value `quick` valid | §2 | `auggie-review.md:49` row `\| --depth \| standard \| quick (auggie single-pass, ~2min)...`. **Line number EXACT**; flag+value valid. | **[CODE-VERIFIED]** |
| 9b | `--remediation-offer` default true at `~52` | §2 | `auggie-review.md:52` `\| --remediation-offer \| true \| After the review completes, offer to chain...`. **Line EXACT**; default `true` confirmed. | **[CODE-VERIFIED]** |
| 9c | `--auggie-model claude-sonnet-4-6` at `~55` (the exact example) | §2 | `auggie-review.md:55` `\| --auggie-model \| (auggie default) \| ...e.g., --auggie-model claude-sonnet-4-6`. **Line EXACT**; flag + exact example value confirmed. | **[CODE-VERIFIED]** |
| 9d | `--post-pr` default true for PR target at `~50` | §2 | `auggie-review.md:50` `\| --post-pr \| true when target is a PR \| Auto-post the markdown report...`. **Line EXACT**; default-true-for-PR confirmed. | **[CODE-VERIFIED]** |
| 9e | `<PR-number>` target resolved via `gh pr view` at `auggie-review.md:26-27,36` | §2 | `auggie-review.md:27` `Remote PR: <PR-number> or <PR-URL> (resolved via gh pr view)`; usage example `:36` `/sc:auggie-review 62 ...`. **Lines EXACT.** | **[CODE-VERIFIED]** |
| 10a | SKILL.md Wave 6 currently does push→reply→resolve (the [MOD] target) | §6.5, FR-8.1 | `SKILL.md:79` Wave-6 label `(L3) push + reply + resolve`; `:89` Wave-6 body: core decides push triad → SKILL does `git push` → reply → resolve via `reply-resolve-thread.sh` (reply FIRST, then resolve). NO re-trigger comment / S5a. Confirms the [MOD] insertion point. | **[CODE-VERIFIED]** |
| 10b | FR-8.5 trigger phrases sourced from DetectionContract, not a hard-coded literal | FR-8.5 | DetectionContract (`detection.py:55-72`) has NO `accepted_trigger_phrases` field yet (claim 7) — so the contract-sourced phrase list is a NEW field to ADD. Today there is no trigger-phrase literal anywhere in the core (no re-trigger code exists). Claim describes intended design, not current state. | **[UNVERIFIED]** (field does not yet exist; planned per §6.2) |
| 11a | EXISTING refs: augment-poll, loop-guard, state-machine, detection-contract | §6.5 | `refs/` contains: `augment-poll.md`, `detection-contract.md`, `finding-verify.md`, `loop-guard.md`, `severity-routing.md`, `state-machine.md`, `thread-reply.md`, `troubleshoot-dispatch.md` (8 refs). All four cited [MOD]-target refs EXIST. | **[CODE-VERIFIED]** |
| 11b | NEW refs do NOT exist yet: `review-retrigger.md`, `auggie-fallback.md` | §6.5 | Neither in `refs/` listing (8 files above). Correctly NEW. | **[CODE-VERIFIED]** (absent → must be created) |
| 11c | Scripts: `poll-augment-review.sh` + `reply-resolve-thread.sh` exist; `retrigger-review.sh` is NEW | §6.5 | `scripts/` = `poll-augment-review.sh`, `reply-resolve-thread.sh` (2 files). `retrigger-review.sh` ABSENT. Correctly NEW. | **[CODE-VERIFIED]** |
| 12 | NFR-6: no `gh`/`git` token in `pr_submit/*.py` (core purity held) | §10, NFR-6 | grep `\b(gh\|git)\b` over `pr_submit/*.py` → only DOCSTRING/COMMENT mentions (`__init__.py:13-14` purity note, `classifier.py:25` `gh pr view` in a docstring) and the credential-redaction REGEX (`run_log.py:40` `gh[pousr]_...`). NO executable `gh`/`git` command token. Core purity is currently held. | **[CODE-VERIFIED]** |

---

## Stale / imprecise anchors (for the builder — do NOT anchor items on these as-written)

1. **`fsm.py:792-793` "papers over the loop" (§1) — ACCURATE but note context.** Line 793 is the optimistic increment; line 792 is its (misleading) comment claiming "Re-review attributed to our push". The comment ALSO must be removed/rewritten when FR-8.2 relocates the increment — flag the comment, not just the statement.

2. **§2 flag-table line numbers — ALL EXACT in current source.** Seed list said "~49/~52/~55/~50"; current `auggie-review.md` matches those lines precisely (49/52/55/50). No staleness. (If `auggie-review.md` is edited before build, re-verify — the spec hard-codes these.)

3. **No CODE-CONTRADICTED findings.** Every concrete current-state claim in the spec matches the source. The only **[UNVERIFIED]** is claim 10b's `accepted_trigger_phrases` provenance — which is correctly a TO-BE-ADDED field (§6.2), not a stale citation. The builder can treat all §6.x deltas as additive against a faithfully-described baseline.

## Cross-check notes for the builder

- The spec's `grounded_in` frontmatter lists `severity_router.py` — it EXISTS (`pr_submit/severity_router.py`), and `recovery.py` (cited for `--resume` / FR-10.4 `rebuild_state`) EXISTS. `rebuild_state()` is in `run_log.py:145-190` (folds JSONL → state; currently folds `ROUND_INCREMENTED/PUSH_COMPLETED/REPLY_POSTED/THREAD_RESOLVED/FINDINGS_NORMALIZED/FIX_APPLIED` — the spec's §6.3 fold of `AUGGIE_FALLBACK_INVOKED/MAX_ROUNDS_CLAMPED/REREVIEW_REQUESTED` is a NEW addition, none present today). **[CODE-VERIFIED]**
- `record_idempotent(set_name, key)` (`run_log.py:200-219`) raises `ValueError` on an unknown set name (:207-208) — so FR-10.1's new `auggie_review_invoked` set MUST be added to `IDEMPOTENCY_SETS` (:27-33) BEFORE `record_idempotent("auggie_review_invoked", ...)` will work. The builder item for the 6th set is a hard prerequisite of the strict-once gate item. **[CODE-VERIFIED]**
- `SkillResult` (`models.py:165-188`) today has NO `rereview_request_count/fallback_engaged/auggie_review_invoked/decline_detected/effective_max_rounds/fallback_round_counter` — all six §6.1 `SkillResult` additions are NEW. **[CODE-VERIFIED]**
- `TERMINAL_STATES` frozenset (`models.py:117-126`) — spec §6.1 correctly says the two new states are NOT terminal (omit from this set). **[CODE-VERIFIED]**

Status: COMPLETE — all 12 seed claims + extensions cross-validated against live source; one [UNVERIFIED] (planned field), zero [CODE-CONTRADICTED].
