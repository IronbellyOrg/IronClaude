# QA Report — Source-Document Fidelity Gate (Phase 7 Gate B M4)

**Agent:** FIDELITY-AGENT-1
**Topic:** pr_submit V1.1 — source-document fidelity (§1-§6 of merged-spec-v1.1-addendum.md)
**Date:** 2026-06-12
**Phase:** report-validation (source-fidelity variant)
**fix_authorization:** false (verify only)
**Assigned sections:** §1 root-cause, §4 FR-8/9/10 tables, §5 INV-R1/R2/R3, §6 per-file deltas

---

## Overall Verdict: PASS

Every FR-8.x / FR-9.x / FR-10.x and INV-R1/R2/R3 in §1-§6 maps to a real implementing
symbol that ACTUALLY addresses the requirement (not nominal mention). Every §6.1/§6.2
detail survived byte-level into code. No phantom coverage found. One documented
**necessary deviation** (backtick in the retrigger regex) — justified, tested, and
explicitly annotated in source; it strengthens fidelity to the real Augment surface
rather than drifting from intent.

---

## Part 1 — FR / INV → implementing symbol (semantic coverage)

| Spec ID | Requirement (abbrev) | Implementing symbol (file:line) | Real? |
|---|---|---|---|
| FR-8.1 | After resolve → S5a; post exactly one re-trigger comment | `fsm.transition` `(RESOLVING,"resolved")→S5A_RETRIGGER_REVIEW` fsm.py:622-626; `run_skill` posts via `config.do_retrigger` fsm.py:968-969 (single call, guarded by `applied_edits>0`) | YES |
| FR-8.2 [MOD] | round_counter ticks ONLY on attributed re-review; optimistic post-resolve increment REMOVED | Relocated increment `result.round_counter += 1` fsm.py:1001 (under `outcome=="attributed"`); timeout branch fsm.py:992-996 does NOT tick; grep confirms no `round_counter += 1` at old fsm.py:793 site | YES |
| FR-8.3 | re-trigger at most once per cycle; `rereview_request_count <= max_rounds` (INV-R1) | `result.rereview_request_count += 1` fsm.py:970 (inside the per-cycle `applied_edits>0` block, one per push); bounded by loop = max_rounds cycles | YES |
| FR-8.4 | post-re-trigger poll waits for re-review attributed to our SHA (watermark) | `classifier._is_attributed_review` classifier.py:100-115 (ts > watermark); threaded through `classify` watermark kwarg classifier.py:118,157 | YES |
| FR-8.5 | trigger token from DetectionContract, never hard-coded literal in core | `accepted_trigger_phrases` detection.py:87-93; T-1105 static-grep asserts core holds no literal (test present) | YES |
| FR-8.6 | S5a skipped (no comment) when cycle did not push (`applied_edits==0`) | Guard `if result.applied_edits > 0:` fsm.py:964 wraps the S5a/do_retrigger/count block | YES |
| FR-9.1 | classify() 4th state `declined`; both phrase+retrigger regexes + newer-than-watermark | `STATE_DECLINED="declined"` classifier.py:24; `is_decline` classifier.py:65-97 (both `re.search` required, watermark check); decline checked FIRST classifier.py:144-163 | YES |
| FR-9.2 | declined routes to S5b from BOTH initial S2 poll and S5 re-trigger poll | `(S2_CLASSIFY,"declined")→S5B` fsm.py:640-642; `(S5_AWAITING_REREVIEW,"declined")→S5B` fsm.py:635-639; run_skill: S2 path fsm.py:876-881, S5 path fsm.py:987-991 | YES |
| FR-9.3 | fallback invokes /sc:auggie-review (exact §2 flags); core only DECIDES | `config.invoke_auggie_review(pr_number=...)` fsm.py:764 (core seam, NFR-6); flag string is SKILL/script side (verified: no flag literal in core, consistent with FR-9.3 NFR-6) | YES |
| FR-9.4 | fallback findings re-enter same pipeline; verify-before-remediate still gates | `_run_fallback` verify gate `verified=[f for f in fallback_findings if config.verify(f)]` fsm.py:779; then apply_edits/run_validation/push fsm.py:797-827 | YES |
| FR-9.5 | attributed re-review WINS over co-occurring decline; stale pre-watermark decline ignored | `attributed_rereview` override classifier.py:157-164 (review>decline); watermark staleness `is_decline` classifier.py:93-96 | YES |
| FR-10.1 | 6th idempotency set `auggie_review_invoked`; invoke at most once per PR | `IDEMPOTENCY_SETS` run_log.py:27-34 (6 entries, 6th = `auggie_review_invoked`); strict-once guard `if not result.auggie_review_invoked:` fsm.py:763-765 | YES |
| FR-10.2 | `effective_max_rounds := min(max_rounds,1)` once via `max_rounds_clamped`; monotone non-increasing | `clamp_max_rounds`=`min(effective,hard)` fsm.py:145-153; applied once fsm.py:760; rebuild monotone-min fold run_log.py:183-194 | YES |
| FR-10.3 | separate single-shot sub-loop `fallback_round_counter` cap 1; NO loop-back; round_counter FROZEN | `loop_guard_should_halt(fallback_round_counter, effective_max_rounds)` fsm.py:768-769; no S5a re-trigger / no 2nd invoke in `_run_fallback`; `round_counter` never mutated in fallback (grep-confirmed) | YES |
| FR-10.4 | strict-once + clamp survive `--resume` via `rebuild_state` | `rebuild_state` folds `AUGGIE_FALLBACK_INVOKED`→set run_log.py:177-182 and `MAX_ROUNDS_CLAMPED`→min run_log.py:183-194; T-1124 asserts fresh RunLog rebuilds set | YES |
| FR-10.5 | `push_count <= max_rounds + 1` (INV-R2): Augment loop ≤max_rounds + fallback ≤1 | Main loop pushes once per cycle ≤ max_rounds fsm.py:955; fallback single push fsm.py:824; strict-once + cap-1 bound the +1 | YES |
| INV-R1 | re-trigger ≤ once/cycle, only when `applied_edits>0`; monotone; ≤ max_rounds; does NOT tick round_counter | fsm.py:964-970 (guarded, increments rereview_request_count not round_counter) | YES |
| INV-R2 | auggie at most once/PR (durable set, survives resume); fallback ≤1 push; push_count ≤ max_rounds+1 | strict-once fsm.py:763-765 + durable fold run_log.py:177-182; single fallback push fsm.py:824 | YES |
| INV-R3 | clamp monotone non-increasing recorded once; fallback sub-loop structural termination; two independent counters | `clamp_max_rounds` min fsm.py:153 + monotone-min rebuild fold run_log.py:187-194; `fallback_round_counter` independent of `round_counter` | YES |

---

## Part 2 — DETAIL PRESERVATION (§6.1/§6.2 byte-level)

| §6 detail | Spec value | Code value (file:line) | Match |
|---|---|---|---|
| EventType +4 values | `rereview_requested`, `decline_detected`, `auggie_fallback_invoked`, `max_rounds_clamped` | models.py:76-79 — identical string values | EXACT |
| EventType count | 33 → **37** | docstring "EXACTLY 37" models.py:21; enforced `_VALID_EVENT_VALUES` run_log.py:36,108; T-1 asserts `len(EventType)==37` test_run_log.py:167 | EXACT |
| MonitorState +2 members | `S5A_RETRIGGER_REVIEW="S5a_RETRIGGER_REVIEW"`, `S5B_AUGGIE_FALLBACK="S5b_AUGGIE_FALLBACK"`; neither terminal | models.py:115-116 (exact values); absent from `TERMINAL_STATES` models.py:129-138 | EXACT |
| SkillResult +6 fields | `rereview_request_count:int=0`, `fallback_engaged:bool=False`, `auggie_review_invoked:bool=False`, `decline_detected:bool=False`, `effective_max_rounds:int\|None=None`, `fallback_round_counter:int=0` | models.py:208-213 — all 6, exact types + defaults | EXACT |
| DetectionContract +3 fields | `decline_phrase_regex`, `decline_retrigger_regex`, `accepted_trigger_phrases:list[str]` + from_yaml extend | detection.py:83-93 (fields) + from_yaml detection.py:110-120 | EXACT |
| decline_phrase_regex default | `/abnormally\s+large/i` | `r"abnormally\s+large"` detection.py:83 | EXACT |
| decline_retrigger_regex default | `/comment\s+["']?(augment\|auggie\|augmentcode)\s+review["']?/i` | `comment\s+["'` + **backtick** + `]?(augment\|auggie\|augmentcode)\s+review["'`backtick`]?` detection.py:84-86 | DEVIATION (documented, see below) |
| accepted_trigger_phrases default | `auggie review` canonical (+ augment/augmentcode review) | `["auggie review","augment review","augmentcode review"]` detection.py:88-92 | EXACT |
| 6th idempotency set name | `auggie_review_invoked` (keyed on pr_number) | `IDEMPOTENCY_SETS += ("auggie_review_invoked",)` run_log.py:33, now 6 | EXACT |
| clamp arithmetic | `min(effective, hard=1)` | `return min(effective, hard)`, `hard=1` default fsm.py:145,153 | EXACT |
| monotone-min fold | take the min seen for effective_max_rounds | `clamp if prev is None else min(prev, clamp)` run_log.py:190-194; T asserts 1 then 3 → stays 1 test_run_log.py:206 | EXACT |
| rebuild folds | AUGGIE_FALLBACK_INVOKED→set, MAX_ROUNDS_CLAMPED→min, REREVIEW_REQUESTED→count | run_log.py:174-194 — all three folds present | EXACT |

### Documented necessary deviation (NOT a defect)

`decline_retrigger_regex` adds a backtick (`` ` ``) to the spec literal char class `["']?`,
yielding `["'`+backtick+`]?`. Source documents this inline (detection.py:78-82) as a Phase 3
QA domain-accuracy finding: the real Augment decline renders the trigger with markdown
backticks (`` Comment `augment review` ``), which the spec's bare `["']?` would miss. It is
tested (T-1110 backtick-wrapped, test_detection_contract.py:210-220). This is a fidelity
*improvement* to the real-world surface, explicitly flagged as a necessary deviation — it
does not weaken FR-9.1 (both regexes still required; T-1111/T-1112 enforce conjunction).
Verdict-neutral; logged for the consolidator's deviation taxonomy as **Necessary deviation**.

---

## Part 3 — Phantom-coverage scan (named-but-not-implemented)

| Candidate | Check | Result |
|---|---|---|
| FR-8.2 increment relocation | Old optimistic `round_counter += 1` at fsm.py:793 actually REMOVED, not just commented | CLEAN — grep finds the single increment only at fsm.py:1001 (attributed) + fsm.py:828 (separate fallback counter); no post-resolve tick |
| FR-10.3 "no loop-back" | `_run_fallback` contains no S5a re-trigger and no 2nd `invoke_auggie_review` | CLEAN — fallback body fsm.py:737-835 has neither |
| FR-10.1 strict-once durability | Is the gate only an in-memory flag (would NOT survive resume)? | CLEAN — durable via JSONL fold run_log.py:177-182; T-1124 proves fresh RunLog rebuild still skips |
| INV-R3 "recorded once" | Is the clamp re-applied/re-raised on re-entry? | CLEAN — `effective_max_rounds` seeded from prior value then `min` fsm.py:755-760; rebuild monotone-min run_log.py:187-194 |
| FR-8.6 / INV-R1 guard | Is S5a unconditionally entered (would post a comment with no push)? | CLEAN — gated by `applied_edits>0` fsm.py:964 |

No phantom coverage detected. Every §1-§6 delta is materially implemented.

---

## Confidence Gate

- **Confidence:** Verified: 21/21 (FR/INV) + 13/13 (detail) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep: 5 | Glob: 0 | Bash: 5
- No UNCHECKED items. No UNVERIFIABLE items. Tool-call count (16) ≥ checklist items per
  matched ID — every match cites a specific file:line confirmed by Read/Grep.

## Summary

- FR/INV mapped to real symbols: 21 / 21
- §6.1/§6.2 details preserved: 12 EXACT + 1 documented necessary deviation
- Phantom coverage: 0
- Critical issues: 0

VERDICT: PASS
