# Pre-Execution Reflection Card 1 — Coverage Completeness

Reviewer: independent pre-execution reflection reviewer (UC-1, Tier 2)
Lens: COVERAGE COMPLETENESS

Driving spec: `/config/workspace/IronClaude/.dev/brainstorms/20260610-234750-pr-review-auto-remediation/merged-spec-v1.1-addendum.md`
Tasklist under review: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-pr-submit-v11-20260612-013419/TASK-RF-pr-submit-v11-20260612-013419.md`

Method: read both files in full, then mapped each named requirement/delta to a concrete checklist item or the tasklist's Normative Invariants section. Verdict is adversarial: a requirement is counted MAPPED only if the tasklist has an executable item, explicit invariant text, or a validation/fidelity gate that would catch omission.

## Coverage matrix — Functional requirements

| Requirement | Status | Tasklist coverage |
|---|---:|---|
| FR-8.1 post-push enters S5a and posts exactly one `auggie review` comment via skill I/O | MAPPED | Objective 4/5; Step 5.3 retargets `RESOLVING/resolved` to `S5A_RETRIGGER_REVIEW`; Step 5.4 calls `do_retrigger` only after a real push; Step 5.8 authors T-1101; Step 6.1 inserts Wave 6 S5a; Step 6.7 creates `scripts/retrigger-review.sh`; Step 6.8 adds static test coverage. |
| FR-8.2 deferred `round_counter` increment only on attributed re-review; remove optimistic `fsm.py:793`; push-without-review no tick | MAPPED | Normative Invariants section inlines INV-001; Step 5.4 explicitly removes the unconditional increment and relocates the single tick behind `rereview_outcome == "attributed"`; Step 5.8 authors T-1102 and T-PUSH-WITHOUT-REREVIEW-NO-TICK; Step 5.G4 re-audits exactly-one increment, `>=` gate, and N⇒N pushes. |
| FR-8.3 at most one re-trigger per cycle; `rereview_request_count <= max_rounds` | MAPPED | Normative INV-R1 block; Step 4.2 folds `REREVIEW_REQUESTED` into `rereview_request_count`; Step 5.8 authors T-1103; Step 5.10 extends loop-guard tests for INV-R1; Step 5.G4 verifies INV-R1 arithmetic. |
| FR-8.4 post-retrigger poll waits for attributed `augmentcode[bot]` review tied to pushed SHA; unattributed review does not complete | MAPPED | Step 5.4 only ticks on injected attributed outcome; Step 5.8 authors T-1104 and fixture coverage; Step 6.5 documents watermark/headRefOid attribution; Phase 7 source-fidelity gates require semantic coverage of FR-8 details. |
| FR-8.5 accepted trigger phrases come from DetectionContract; canonical script emits `auggie review`; deterministic core has no hard-coded trigger literal | MAPPED | Step 3.3 adds `accepted_trigger_phrases`; Step 6.7 creates script with exact body token; Step 6.8 adds T-1105 static parity/core-no-literal check. |
| FR-8.6 skip S5a when no push / `applied_edits == 0` | MAPPED | Step 5.4 gates `do_retrigger` on `applied_edits > 0`; Step 5.8 authors T-1106; Step 5.G3 domain lens specifically checks re-trigger skipped when no edits. |
| FR-9.1 classifier gains 4th `declined` state using bot login, both regexes, watermark; decline before clean/findings | MAPPED | Step 3.1 adds `STATE_DECLINED` and decline-first branch; Step 3.2 adds watermark-aware `is_decline`; Step 3.3 adds regex fields; Step 3.6 authors T-1110/T-1111/T-1112 + watermark test; Step 3.G2/G4 validate 4-state and branch order. |
| FR-9.2 `declined` routes to S5b from initial S2 and S5 poll | MAPPED | Step 5.3 adds `(S2_CLASSIFY,"declined")` and `(S5_AWAITING_REREVIEW,"declined")` edges; Step 5.9 authors T-1113/T-1113b; Step 5.G2 dual-surface lens verifies transition + run_skill agreement. |
| FR-9.3 fallback invokes exact `/sc:auggie-review <PR> --depth quick --remediation-offer --auggie-model claude-sonnet-4-6`; skill-side invocation only | MAPPED | Step 5.2 adds `invoke_auggie_review` seam; Step 5.5 gates invocation; Step 5.9 authors T-1114; Step 6.1 inserts Wave 6b with byte-exact flags; Step 6.6 documents flag table; Step 6.8 adds T-1115 static parity. |
| FR-9.4 fallback findings re-enter same pipeline and are verify-before-remediate gated | MAPPED | Step 5.5 explicitly requires re-entry through classify/re-grade/verify-before-remediate/route/fix/validate/push once; Step 5.9 authors T-1116; Step 5.G3 domain lens checks findings are not trusted verbatim. |
| FR-9.5 race ordering: real review wins over decline; stale pre-watermark decline ignored | MAPPED | Step 3.2 implements watermark-aware decline; Step 3.6 adds stale-decline test; Step 5.9 authors T-1117/T-1118 for review-wins and stale-decline; Step 6.5 documents watermark. |
| FR-10.1 6th idempotency set `auggie_review_invoked`; fallback gates on `record_idempotent`; at most once per PR | MAPPED | Normative INV-R2 block; Step 4.1 adds the 6th set; Step 4.4 extends idempotency tests and T-AUGGIE-AT-MOST-ONCE-style assertions; Step 5.5 gates `invoke_auggie_review` on the idempotency record; Step 5.9 authors T-AUGGIE-AT-MOST-ONCE. |
| FR-10.2 first fallback clamps `effective_max_rounds := min(max_rounds, 1)` once; monotone non-increasing | MAPPED | Normative INV-R3 block; Step 4.2 adds monotone-min rebuild fold; Step 5.1 adds `clamp_max_rounds`; Step 5.5 records `MAX_ROUNDS_CLAMPED`; Step 4.5/5.9 author clamp tests T-1121. |
| FR-10.3 separate single-shot fallback sub-loop; cap 1; no loop-back; round_counter frozen | MAPPED | Normative INV-R3 block; Step 5.5 defines cap-1 fallback sub-loop with no second re-trigger/invoke and frozen `round_counter`; Step 5.9 authors T-1122/T-1123; Step 5.10 tests fallback counter cap and counter independence. |
| FR-10.4 strict-once and clamp survive `--resume` via run_log rebuild | MAPPED | Step 4.2 rebuilds invoked set and effective max; Step 4.4 tests fresh RunLog rebuild/resume strict-once; Step 5.9 authors T-1124. |
| FR-10.5 total push bound `push_count <= max_rounds + 1` | MAPPED | Normative INV-R2 block; Step 5.5 requires total bound; Step 5.9 directly asserts `push_count <= max_rounds + 1` in T-1125; Step 5.G4/7.GA4 audit the arithmetic. |

## Coverage matrix — Invariants / preserved constraints

| Requirement | Status | Tasklist coverage |
|---|---:|---|
| INV-R1 re-trigger boundedness | MAPPED | Normative Invariants section copies INV-R1 verbatim; Step 4.2 counts `REREVIEW_REQUESTED`; Step 5.4/5.8/5.10 implement and test bounded re-trigger/no tick; Step 6.3 adds INV-R1 to loop-guard ref; final domain lenses re-audit. |
| INV-R2 strict-once + total-push bound | MAPPED | Normative Invariants section copies INV-R2 verbatim; Step 4.1/4.4 add and test idempotency; Step 5.5/5.9 implement and test at-most-once and push bound; Step 6.3/6.6 document it; final INV-fidelity gate checks it. |
| INV-R3 clamp monotonicity / deterministic termination | MAPPED | Normative Invariants section copies INV-R3 verbatim; Step 4.2 adds monotone-min fold; Step 5.1/5.5 implement clamp and structural termination; Step 5.10 tests independent counters; Step 6.3/6.6 document it; final gates check it. |
| INV-001 verbatim preservation | MAPPED | Normative Invariants section copies INV-001 verbatim; Step 5.3 preserves S5→S2 edge; Step 5.4 relocates the only tick and preserves `>=` gate ordering; Step 5.8/5.10 test deferred increment and existing fence-post semantics; Step 5.G4 requires worked N=2 trace. |
| NFR-6 core purity | MAPPED | Key Constraints section states zero `gh`/`git` executable tokens in core; Step 3.G4/5.6/5.G4/6.8/7.GA4/8.2 provide static greps and final verification; SKILL/script items keep I/O out of deterministic core. |

## Coverage matrix — Key build deltas (§6 universe)

| Build delta | Status | Tasklist coverage |
|---|---:|---|
| `models.py`: EventType +4 and count 33→37 | MAPPED | Step 2.2 adds the four named members and updates count docstrings; Step 4.5 adds `len(EventType)==37`; Step 7.GA4 closed-enum lens recounts. |
| `models.py`: MonitorState +2 S5a/S5b, non-terminal | MAPPED | Step 2.1 adds S5A/S5B and explicitly omits them from `TERMINAL_STATES`; Step 5.3 consumes them. |
| `models.py`: SkillResult +6 fields | MAPPED | Step 2.3 adds all six fields exactly; downstream Steps 4/5 tests consume them. |
| `classifier.py`: `STATE_DECLINED` | MAPPED | Step 3.1 adds state constant and branch; Step 3.G4 validates exactly four states. |
| `detection.py`/contract: `decline_phrase_regex` | MAPPED | Step 3.3 adds field/default/from_yaml read; Step 3.4 adds ref YAML; Step 3.6 tests. |
| `detection.py`/contract: `decline_retrigger_regex` | MAPPED | Step 3.3/3.4 add field and YAML; Step 3.6 tests both-regex AND behavior. |
| `detection.py`/contract: `accepted_trigger_phrases` | MAPPED | Step 3.3 adds list field; Step 6.8 static checks trigger token and core literal discipline. |
| `detection/classifier`: `is_decline` pure function | MAPPED | Step 3.2 adds pure watermark-aware `is_decline`; Step 3.6 tests watermark and false positives. |
| `DetectionContract.from_yaml` extension | MAPPED | Step 3.3 explicitly extends `from_yaml` with three `data.get(...)` reads; Step 3.G2 validates. |
| `run_log.py`: 6th idempotency set | MAPPED | Step 4.1 appends `auggie_review_invoked`; Step 4.4 tests membership, first/second record, resume. |
| `run_log.py`: rebuild fold counts `REREVIEW_REQUESTED` | MAPPED | Step 4.2 adds count fold; Step 4.5 tests. |
| `run_log.py`: rebuild fold adds `AUGGIE_FALLBACK_INVOKED.pr_number` to set | MAPPED | Step 4.2 adds add-to-set fold; Step 4.4/4.5 tests. |
| `run_log.py`: rebuild fold monotone-mins `MAX_ROUNDS_CLAMPED.effective_max_rounds` | MAPPED | Step 4.2 adds None-safe min fold; Step 4.5 tests decreasing-only behavior; Step 4.G4 audits arithmetic. |
| `run_log.py`: 33→37 prose/error-string updates | MAPPED | Step 4.3 updates both count-bearing strings and re-greps stale `33`; Step 7.GA4 closed-enum lens checks all count sites. |
| `fsm.py`: 6 new/modified edges | MAPPED | Step 5.3 lists all six edges; Step 5.G2 verifies both `transition()` and `run_skill()` surfaces. |
| `fsm.py`: remove optimistic `:793` increment and relocate to attributed re-review | MAPPED | Step 5.4 is explicit and contains the strongest wording; Step 5.8 authors the no-tick regression; Step 5.G4 verifies exactly-one site and N⇒N pushes. |
| `fsm.py`: `clamp_max_rounds` helper | MAPPED | Step 5.1 adds pure helper; Step 5.5 uses it at fallback entry. |
| `fsm.py`: fallback sub-loop | MAPPED | Step 5.5 implements strict-once, cap-1, no-loop-back fallback sub-loop; Step 5.9 tests T-1120..T-1125. |
| `SKILL.md`: Wave 6 S5a + Wave 6b fallback | MAPPED | Step 6.1 modifies Wave 6 and adds Wave 6b, lazy-load rows, exact flags, and output-contract fields. |
| `refs/augment-poll.md` MOD | MAPPED | Step 6.2 adds 4th `declined` state and decline raw-surface description. |
| `refs/loop-guard.md` MOD | MAPPED | Step 6.3 adds INV-R1/R2/R3, `fallback_round_counter`, and 33→37 / 5→6 count updates. |
| `refs/state-machine.md` MOD | MAPPED | Step 6.4 adds S5a/S5b topology and explicitly notes spec §6.5 omission as a flagged discrepancy. |
| NEW `refs/review-retrigger.md` | MAPPED | Step 6.5 creates the R1 ref with comment surface, watermark, and INV-R1. |
| NEW `refs/auggie-fallback.md` | MAPPED | Step 6.6 creates R2/R3 ref with decline detection, strict-once, clamp, re-entry, exact flag table, and bait rationale. |
| NEW `scripts/retrigger-review.sh` | MAPPED | Step 6.7 creates executable script with fork-pinned issue-comment POST and exact body. |
| NEW `test_review_retrigger.py` | MAPPED | Step 5.8 creates the module and covers T-1101..T-1106 plus T-PUSH-WITHOUT-REREVIEW-NO-TICK. |
| NEW `test_auggie_fallback.py` | MAPPED | Step 5.9 creates the module and covers T-1110..T-1118, T-1120..T-1125, and T-AUGGIE-AT-MOST-ONCE. |
| EXT `test_detection_contract.py` | MAPPED | Step 3.6 extends with decline regex, 4th state, and watermark tests. |
| EXT `test_idempotency.py` | MAPPED | Step 4.4 extends with 6th set and resume strict-once. |
| EXT `test_loop_guard.py` | MAPPED | Step 5.10 extends with INV-R1/R3, deferred increment, and fallback cap. |
| EXT `test_run_log.py` | MAPPED | Step 4.5 extends with 4 events, 37 count, clamp/min fold. |
| EXT `test_static_grep.py` | MAPPED | Step 6.8 extends purity/fork-pin/static parity tests T-1105/T-1115. |
| Seven NEW fixtures | MAPPED | Step 3.6 creates `decline-comment.json`, `decline-initial-poll.json`, `stale-decline-pre-watermark.json`; Step 4.4 creates `decline-twice.json`; Step 5.8 creates `rereview-attributed.json`, `rereview-then-decline.json`; Step 5.9 creates/reuses `decline-initial-poll.json` and creates `auggie-fallback-findings.json`. Combined set matches all 7 required fixtures. |

## Coverage matrix — Edge cases and acceptance criteria (not included in coverage_pct denominator)

| EC/AC | Status | Tasklist coverage |
|---|---:|---|
| EC-17 re-trigger posted, attributed re-review advances | MAPPED | Step 5.8 T-1101/T-1104; Step 5.G1 includes EC-17. |
| EC-18 re-trigger posted, no re-review before timeout; no tick | MAPPED | Step 5.8 T-PUSH-WITHOUT-REREVIEW-NO-TICK. |
| EC-19 initial oversized decline, no push yet | MAPPED | Step 5.9 T-1113b/T-AUGGIE-AT-MOST-ONCE. |
| EC-20 decline after push; round counter frozen; fallback ≤1 | MAPPED | Step 5.9 T-1113/T-1122. |
| EC-21 two declines, second idempotency skip | MAPPED | Step 4.4 `decline-twice.json`; Step 5.9 T-AUGGIE-AT-MOST-ONCE. |
| EC-22 re-review and decline in same poll, review wins | MAPPED | Step 5.9 T-1117. |
| EC-23 stale decline ignored | MAPPED | Step 3.6 watermark test; Step 5.9 T-1118. |
| EC-24 resume after auggie-review already invoked | MAPPED | Step 4.4 and Step 5.9 T-1124. |
| AC-16 exact re-trigger and next round only on attributed re-review | MAPPED | Step 5.8 T-1101/T-1104; Step 6.7 script. |
| AC-17 push with no attributed re-review does not tick | MAPPED | Step 5.8 T-PUSH-WITHOUT-REREVIEW-NO-TICK. |
| AC-18 `rereview_request_count <= max_rounds` | MAPPED | Step 5.8 T-1103; Step 5.10 INV-R1. |
| AC-19 decline only when expected and routes from both poll points | MAPPED | Step 3.6 T-1111/T-1112; Step 5.9 T-1113/T-1113b. |
| AC-20 exact fallback invocation and verify-before-remediate re-entry | MAPPED | Step 6.1/6.6 exact flags; Step 5.9 T-1114/T-1116. |
| AC-21 at most once, push bound, deterministic termination | MAPPED | Step 5.9 T-AUGGIE-AT-MOST-ONCE/T-1124/T-1125/T-1122; Step 5.G4 arithmetic audit. |

## High-risk predicate audit

### Predicate 1 — INV-001 deferred-increment (FR-8.2)

PASS.

Evidence of tasklist coverage:
- Step 5.4 explicitly removes the unconditional optimistic `result.round_counter += 1` and relocates the sole tick behind `config.rereview_outcome[cycle_index] == "attributed"`.
- Step 5.4 preserves ordering: tick after push and before next top-of-loop budget gate, preserving monotonicity and `max_rounds=N ⇒ N pushes`.
- Step 5.3 leaves the `S5_AWAITING_REREVIEW --rereview_attributed--> S2_CLASSIFY` edge intact and adds decline as a sibling edge.
- Step 5.8 authors T-PUSH-WITHOUT-REREVIEW-NO-TICK and requires it be non-vacuous: a timeout/no attributed re-review must leave `round_counter` unchanged.
- Step 5.G4 independently re-audits the single increment site, the `>=` gate, the edge, and an N=2 worked example.

Adversarial note: this is mapped strongly enough; the tasklist does not merely say "preserve INV-001" but names the old increment, the new condition, the ordering, and the regression test.

### Predicate 2 — Strict-once (FR-10.1, INV-R2)

PASS.

Evidence of tasklist coverage:
- Step 4.1 adds `auggie_review_invoked` as the 6th durable idempotency set.
- Step 4.4 tests `record_idempotent("auggie_review_invoked", pr_number)` True-then-False and a fresh RunLog rebuild for resume strict-once.
- Step 5.5 gates `config.invoke_auggie_review(...)` on the idempotency record and requires later declines to skip.
- Step 5.9 authors T-AUGGIE-AT-MOST-ONCE, explicitly asserting recorder call count is exactly one across two declines and resume.
- Step 5.9 also asserts `push_count <= max_rounds + 1`; Step 5.G4 re-checks INV-R2 arithmetic.

Adversarial note: strict-once is covered across data model/run-log, FSM behavior, tests, and invariant QA. Resume survival is not left to prose; it is directly tied to `rebuild_state()` and a test.

## Coverage calculation

Denominator used per user instruction: FR + INV + key build-deltas universe.

- Functional requirements: 16 / 16 mapped
- Invariants / preserved constraints: 5 / 5 mapped
- Key build deltas: 33 / 33 mapped
- Total mapped requirements: 54
- Total requirements counted: 54

coverage_pct = 100.0

## UNMAPPED list

none

## VERDICT

VERDICT: PASS — 100.0% coverage over the requested FR + INV + key build-deltas universe. The tasklist is unusually explicit on the two highest-risk predicates and includes both implementation items and non-vacuous test-authoring items for them. No coverage gap found.
