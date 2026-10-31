# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis (fault-finder model: fable)

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | Passing the marker updated_at to _thread_findings is enough to select Codex roots | UNADDRESSED | HIGH | classifier.py:301,317-319 reject roots created after completion; Augment completion is the formal review (submitted before/with its roots), Codex completion chosen as summary updated_at (design:177,185) with no recorded ordering vs root createdAt. Fix: completion = max(marker updated_at, Codex formal review submitted_at for expected_head); fixture with root createdAt > marker updated_at. |
| INV-002 | state_variables | Sticky absence is computable from the wait-outcome inputs | UNADDRESSED | HIGH | design:323-324 / plan:102 signatures take no absence input; in S5 a silent Augment returns S2_CLASSIFY (fsm.py:705) -> pending -> merge keeps polling until 600 s although Codex is done; strict-once poke (run_log.py:199-208). Fix: pass absent set into the wait outcomes; absent reviewers are never pending. |
| INV-003 | interaction_effects | X-004 fix makes the between-posts crash recoverable | UNADDRESSED | MEDIUM | Watermark lives only in session memory (review-retrigger.md:42-45); after resume watermark None forces Augment polling (SKILL.md:87-90). Fix: carry watermark on rereview_requested{cycle_id, reviewer, watermark} and rebuild per-reviewer watermarks. |
| INV-004 | guard_conditions | Rewording terminal_augment_no_response is the only SKILL change for Augment-silent-Codex-present | UNADDRESSED | MEDIUM | SKILL.md:61,186,199,241 treat it as terminal before any merge; design:125-127 requires continuing with Codex. |
| INV-005 | sufficiency_challenge | "Two summary comments -> polling" is harmless | UNADDRESSED | MEDIUM | design:172-174 exactly-one rule makes a second summary permanent polling; Augment picks the latest candidate (classifier.py:230-234). Fix: newest valid marker wins, ambiguous only on identical times. |
| INV-006 | count_divergence | INV-R1 holds after crash-resume repost | UNADDRESSED | MEDIUM | Resume must reuse the dangling record's cycle_id (recovery.py:136-141); a new cycle_id re-posts both. |
| INV-007 | collection_boundaries | Same-line findings always share a dedup key | UNADDRESSED | LOW | Outdated Codex thread (line null, old original_line) vs current Augment line differ (design:224, classifier.py:298-299). |
| INV-008 | collection_boundaries | reviewer_absent is one-shot; disabled reviewer is never present | UNADDRESSED | LOW | plan:50,54 do not pin set semantics; blank identity should be absent immediately (design:108). |
| INV-009 | guard_conditions | X-001 fallback fully specified | UNADDRESSED | LOW | `get(key) or DEFAULT` would re-enable Codex on explicit ""; key-presence semantics needed. |
| INV-010 | interaction_effects | Present-but-never-completing Codex costs only one event | ADDRESSED | LOW | Intended fail-open; costs up to --timeout per wait (design:144,154). |
| INV-011 | state_variables | Resume state carries everything the two-reviewer loop needs | UNADDRESSED | LOW | absent_reviewers must be seeded in the initial state dict (run_log.py:167-180). |
| INV-012 | count_divergence | All texts of rereview_request_count updated | ADDRESSED | LOW | fsm.py:1143 ticks once per cycle; stale texts covered by C-005/U-009. |

## Summary

- **Total findings**: 12
- **ADDRESSED**: 2
- **UNADDRESSED**: 10
  - HIGH: 2 (INV-001, INV-002)
  - MEDIUM: 4 (INV-003, INV-004, INV-005, INV-006)
  - LOW: 4 (INV-007, INV-008, INV-009, INV-011)

CONVERGENCE BLOCKED: 2 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-001, INV-002
Resolution: no Round 3 at --depth standard; both items are carried into the merged verdict as required remediation (refactor-plan Change #2), and the debate status is recorded as BLOCKED_BY_INVARIANTS.
