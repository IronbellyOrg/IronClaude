# QA Report — Research Gate (Gap-Detection Lens)

**Topic:** pr_submit V1.1 (FR-8/9/10, +2 FSM states, +3 invariants, +1 idempotency set, +4 EventType)
**Date:** 2026-06-12
**Phase:** research-gate
**Lens:** gap-detection
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## Adversarial stance

Assume the research is incomplete. Goal: find deltas the builder NEEDS but the research does not actionably cover. 0 issues requires demonstrated thorough cross-check of every §6 file-delta and §9.1 test file against research coverage.

---

## Files in scope (all read in full)

| File | Read | Role | Quality |
|------|------|------|---------|
| research-notes.md (scope map) | YES | EXISTING_FILES + delta map + suggested phases | Strong |
| 01-core-modules-current-state.md (R1) | YES | File inventory, 6 core .py + __init__ + adjacency | Strong, code-verified |
| 02-fsm-transition-runskill-anatomy.md (R2) | YES | fsm dual-surface trace, :793, RunConfig seams | Strong, highest-risk surface well-covered |
| 03-runlog-idempotency-enum-patterns.md (R3) | YES | idempotency/enum/fold idioms incl. monotone-min | Strong, authored the missing idiom |
| 04-skill-refs-scripts-conventions.md (R4) | YES | SKILL/refs/scripts + state-machine.md MOD flag | Strong |
| 05-test-infra-fixtures-markers.md (R5) | YES | conftest, fixtures schema, markers, verify cmds | Strong BUT one factual error (see C1) |
| 06-spec-delta-extraction.md (R6) | YES | builder spec index: FR→file→test matrix, INV verbatim | Strong |
| 07-doc-crossvalidate-anchors.md (R7) | YES | every spec anchor tagged CODE-VERIFIED | Strong, 0 contradicted |

## Independent source verification performed (tool evidence)

- `run_log.py:26-33` IDEMPOTENCY_SETS = EXACTLY 5 members (awk count = 5). Comment literal "The 5 idempotency sets".
- `fsm.py:792-793` `result.round_counter += 1` under comment "Re-review attributed to our push" — EXACT.
- `models.py` EventType members = EXACTLY 33 (awk count = 33).
- `tests/pr_submit/test_review_retrigger.py` + `test_auggie_fallback.py` ABSENT (correctly NEW).
- 5 EXT test modules (detection_contract, idempotency, loop_guard, run_log, static_grep) all PRESENT.
- `refs/state-machine.md` PRESENT (MOD target); `refs/review-retrigger.md` + `refs/auggie-fallback.md` ABSENT (correctly NEW).
- `pyproject.toml:111` `--strict-markers` ON; markers inv/loop_guard/autonomy/recovery/p0 registered (139-143); NO decline/auggie/fallback marker.
- `test_idempotency.py` references only `processed_finding_ids` + `replied_comment_ids` via record_idempotent (so existing tests do not enumerate all 5 — relevant to C1).

---

## Coverage assessment vs lens checklist

### Checklist item 1 — Coverage gaps per §6 file-delta + §9.1 test file

**models.py** — COVERED (R1 §models, R3 §4.1/§4.4). Enum +4, MonitorState +2 non-terminal (omit from TERMINAL_STATES), SkillResult +6 fields with exact defaults. The FIVE "33→37" places: R3 §4.1 enumerates all five — models.py:20 (class docstring), models.py:3-4 (module docstring), run_log.py:109 (ValueError), run_log.py:103-104 (append docstring), + the NET-NEW test count assertion. R5 confirms NO existing numeric count test (37-member assertion is net-new). MonitorState non-terminal additions explicit. ACTIONABLE.

**classifier.py + detection.py** — COVERED (R1 §classifier/§detection). STATE_DECLINED const; decline-before-clean/findings ordering; `is_decline(comment, contract, *, watermark) -> bool` signature; 3 new DetectionContract fields + from_yaml +3 data.get lines + defaults baked + detection-contract.md YAML stays locked:false. R1 §classifier:110 surfaces the open design choice (decline inside classify needing watermark threading vs separate is_decline) — flagged, not silently resolved. ACTIONABLE.

**run_log.py** — COVERED (R3 §1/§3/§4.2/§4.3). 6th set; the 3 rebuild_state folds incl. the monotone-min fold that has NO in-repo precedent — R3 §4.3 AUTHORS the exact None-safe idiom (`clamp if prev is None else min(prev, clamp)`) with rationale. The two new top-level state-dict keys (effective_max_rounds, rereview_request_count) called out. ACTIONABLE — the lens's specific worry (monotone-min fold idiom) is fully addressed.

**fsm.py** — COVERED (R2 entire). The dual-surface lock-step (transition() chain-of-ifs AND the inline run_skill() loop that does NOT call transition()) is the headline of R2 §0/§6 — explicitly "both must be modified in lock-step or they drift." 6 new edges enumerated; :793 removal + relocation to attributed-re-review with the ordering-risk for `max_rounds=N ⇒ N pushes` (R2 §2/§5); clamp_max_rounds placement; fallback sub-loop via loop_guard.should_halt(fallback_round_counter, 1). RunConfig seam staticmethod trap captured. ACTIONABLE. (See I3 for one residual under-specification.)

**skill** — COVERED (R4 entire). 2 MOD refs (augment-poll, loop-guard) + 2 new refs (review-retrigger, auggie-fallback) + SKILL.md Wave 6 [MOD] + new Wave 6b + retrigger-review.sh shape (mirrors thread-reply.md:72) + Output Contract status enum question. R4 §D independently CONFIRMS the state-machine.md MOD gap the lens flagged. ACTIONABLE.

**tests** — COVERED (R5 entire). 2 new modules + 5 EXT + 7 fixtures with per-file schema assignment + the `--strict-markers` constraint (reuse existing markers or add to pyproject). Verify commands exact. ACTIONABLE — except the C1 factual error below.

### Checklist item 2 — Findings actionable? YES. Every research file gives file:line anchors, re-grep instructions, and exact symbol names. R3/R2 author net-new idioms rather than hand-waving.

### Checklist item 3 — Integration points. COVERED. __init__.py export surface (R1 §INIT — conditional on test-import style, correctly marked Unverified-until-test-audit; enum/field deltas auto-export). recovery.py touched-by-new-states (R1 §RECOVERY surfaces the latent Branch-A→S5 hardcode risk; R7 confirms rebuild_state resumes into string-states without code change). severity_router.py UNCHANGED (R1 §SEVROUTER, R7). loop_guard.py source NO-OP (R1, R2 — reuses existing signature).

### Checklist item 4 — Verify commands. COVERED (R5 §5, scope-map TEMPLATE_NOTES). make lint + `uv run ruff format --check src/ tests/` (the two-gate gotcha) + make verify-sync + make test + specific pytest selectors all given verbatim.

### Checklist item 5 — §11 open decision (status-enum granularity). COVERED as Open Question, NOT silently resolved. Scope-map AMBIGUITIES_FOR_USER + R6 §5.5 + R4 §I all flag it; R6 states the task will follow spec's RECOMMENDATION (reuse) and flag the alternative in Open Questions. Correct handling.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| C1 | IMPORTANT | research/05-test-infra-fixtures-markers.md §6 (lines 343-349) + §summary | R5 states "idempotency sets today = EXACTLY 4" and lists only 4 (drops `processed_review_ids`), then tells the builder to "reconcile the 6th-set wording — the code has only 4 today, so either the spec counts differently or V1.1 also lands a 5th." This is FACTUALLY WRONG: source `run_log.py:27-33` has EXACTLY 5 sets (verified by awk + read; comment literal says "The 5 idempotency sets"), and R1/R3/R7 all correctly state 5→6. If the builder trusts R5's reconciliation note, it could author a wrong test assertion (e.g. asserting a 5th set lands, or mis-stating the count). | Builder must DISREGARD R5's "EXACTLY 4 today" claim and use the source-verified count: 5 sets today → 6 with `auggie_review_invoked`. R3 §4.2 has the correct tuple+fold. The test assertion is `"auggie_review_invoked" in IDEMPOTENCY_SETS` + len==6 + record_idempotent True-then-False. R5's mirror-pattern guidance (record_idempotent idiom) is otherwise fine. |
| I2 | MINOR | research/04 §B (SKILL.md:64) | R4 says the SKILL.md loop-guard.md ref asserts "EXACTLY 33 EventType members" and "any new event type is a breaking [MOD] to loop-guard.md §11.3," implying loop-guard.md ALSO carries a 33-count that must become 37. R3's five-place "33→37" enumeration (§4.1) does NOT include loop-guard.md — it lists only models.py x2 + run_log.py x2 + test. If loop-guard.md indeed hardcodes "33" (R4 cites loop-guard.md:53-62), that is a SIXTH "33→37" site the §6 delta list misses. | Builder item for refs/loop-guard.md [MOD] must include re-grep for the literal "33" in loop-guard.md and update to 37 if present, so the "33→37" change set is complete across BOTH core .py and the skill ref. Low severity because the loop-guard.md MOD item already exists (INV-R1/R2/R3); this just adds the count-bump to its scope. |
| I3 | MINOR | research/02 §1 (edge table, fallback_skip row) | The `(S5B_AUGGIE_FALLBACK, "fallback_skip") → HALT_MAX_ROUNDS \| TERMINAL_CLEAN` edge is a conditional terminal whose SELECTOR is left as a disjunction — R2 explicitly says "builder must define the selector; spec leaves it as a disjunction." This is correctly FLAGGED (not a silent gap), but no research file proposes WHICH condition picks HALT_MAX_ROUNDS vs TERMINAL_CLEAN, leaving the builder to invent the predicate. | Acceptable as an Open Question, but the builder item should make the selector decision explicit (e.g. fallback findings exhausted-clean → TERMINAL_CLEAN; fallback produced residual findings but clamp/strict-once forbids another cycle → HALT_MAX_ROUNDS) and cite that it is builder-resolved, not spec-given. Surface in the task's Open Questions if the predicate is non-obvious from EC-19/EC-20. |
| I4 | MINOR | research/01 §RECOVERY (line 203) | The recovery.py Branch-A hard-resume to `S5_AWAITING_REREVIEW` (recovery.py:111) may, post-V1.1, semantically need `S5A_RETRIGGER_REVIEW` (a crash recovered as "landed" but where the re-trigger comment was not yet posted should resume at S5a, not S5). R1 marks this "Unverified whether spec intends a recovery change" and recommends a builder review item. Since recovery.py is NOT a §6 build target, there is a risk the builder drops it entirely. | Builder should carry a single review/risk checklist item (or Open Question) for the recovery.py Branch-A resume target vs the new S5a step, even though §6 omits recovery.py. Spec-silence here is a latent interaction, not a confirmed change — flag, do not auto-edit. |

---

## Summary

- Lens checklist items passed: 5/5 substantively covered (every §6 file-delta and §9.1 test file has actionable research).
- Issues found: 4 (CRITICAL: 0, IMPORTANT: 1, MINOR: 3).
- The single IMPORTANT issue (C1) is a cross-file factual contradiction: R5 miscounts idempotency sets (4) against the source truth (5), contradicting R1/R3/R7 and the actual code. It is a correctness landmine for the test-authoring item, not a missing-coverage gap — the correct data exists in R1/R3/R7, so it is fixable by the builder disregarding the one wrong note.
- No CRITICAL gaps: every delta the builder needs to write self-contained, executable items is present and code-grounded. The lens's specific worry-list (5-place 33→37, monotone-min fold, dual-surface fsm edit, state-machine.md MOD, marker constraint, §11 open question) is each addressed.

## Confidence

**Confidence:** Verified: 5/5 lens checklist items | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

(All 5 lens checklist items verified by reading all 7 research files in full + 8 independent source spot-checks. The 4 issues are quality/contradiction findings, not unchecked items — the coverage question itself is fully answered.)

**Tool engagement:** Read: 9 (scope map + 7 research files + report re-read) | Grep: 0 | Glob: 0 | Bash: 3 (idempotency/793/enum counts; file-existence; markers+contradiction). Total verification tool calls = 12 ≥ 5 lens items. No web research performed (all claims local/source-bound; Tavily not needed).

---

## VERDICT: FAIL

**Rationale:** Per the research-gate zero-tolerance rule, ANY issue regardless of severity = FAIL until resolved. There are no CRITICAL coverage gaps — the research is thorough and the builder COULD proceed for most items — but the IMPORTANT cross-file contradiction (C1: R5's wrong idempotency count) is a correctness hazard that must be resolved before synthesis/build, plus 3 MINOR items (I2 loop-guard.md "33" sixth site, I3 fallback_skip selector undefined, I4 recovery.py Branch-A latent interaction) that the builder must explicitly carry rather than drop.

**Remediation before proceeding:**
1. (C1, IMPORTANT) Correct or annotate R5's idempotency count to 5→6 (source truth), or instruct the builder to use R1/R3/R7's correct count and ignore R5 §6's "EXACTLY 4 today" reconciliation note.
2. (I2, MINOR) Add "re-grep + bump '33'→'37' in refs/loop-guard.md" to the loop-guard.md MOD item scope so the count change set is complete.
3. (I3, MINOR) Have the builder define the `fallback_skip` HALT_MAX_ROUNDS|TERMINAL_CLEAN selector explicitly (or list as Open Question).
4. (I4, MINOR) Add a recovery.py Branch-A resume-target review item / Open Question.

None of these require re-running research — all are either disregard-one-wrong-note (C1) or carry-an-explicit-item (I2/I3/I4). After remediation the gate should PASS.

## QA Complete
