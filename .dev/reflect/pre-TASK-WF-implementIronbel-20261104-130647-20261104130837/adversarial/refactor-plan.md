# Refactoring Plan

## Overview
- Base: Variant 1 (sonnet:analyzer), reviewer-1 card
- Incorporated: Variant 3 (opus:refactorer), Variant 2 (haiku:qa), invariant-probe.md
- Output: merged-verdict.yaml (one merged reviewer verdict for sc:reflect)
- Planned changes: 9; rejected: 4
- Overall risk: Low (additive to a findings list; no source edits)

## Planned Changes

1. **Regrade R1-F5 to blocking and merge R3-F5** — source V3 R3-F5, V1 Round 2 concession; target: base finding R1-F5; approach: replace; rationale: X-002 95% (Done-when "runs bare python"); risk Low.
2. **Add the single-scanner amendment (blocking)** — source V3 R3-F2 (desync half), R3-F3 (desync half), V3 Round 2 evidence 1-3, INV-002, INV-004, INV-005, INV-006, INV-007, INV-008, INV-009, INV-010, INV-013; target: new finding M-SCANNER; approach: insert; rationale: C-003 90%, C-004 85%, C-006 95%, invariant blockers INV-004/INV-027; risk Low.
3. **Replace C-001 fix with the allowlist** — source INV-001 (git history: no freshness- Bash hook ever existed; policy says no Bash counter); target R1-F1 fix; approach: modify; rationale: fault-finder evidence supersedes the debate's freshness- filter; keeps V1's tests/hooks run and PR-body supersession note; risk Low.
4. **Add fail-open-by-construction + jq-missing test** — source R3-F7, R2-F3, INV-021, INV-017; target: base R1-F6; approach: merge; rationale C-008 85%; risk Low.
5. **Add large-command case** — source INV-003; target: base R1-F11 (timing); approach: modify (keep the < 1 s precedent, add ~200 KB stdin case); risk Low.
6. **Add Task 7 hardening** — source R3-F9, INV-016; target new finding M-TASK7; approach insert; risk Low.
7. **Add Constraints mislabel and array/ceiling notes** — source R3-F11, R3-F10, R3-F6, INV-011, INV-012, INV-014, INV-022, INV-026; target new findings; approach insert; risk Low.
8. **Add coverage-matrix note** — source R2-F5 (verified); approach insert (minor); risk Low.
9. **Extend Goal-wording finding** — source INV-019; target R1-F8; approach modify (record template line 965 as follow-up, out of scope).

## Base weaknesses addressed
- R1-F5 under-graded -> change 1.
- No lexer coverage -> change 2.
- C-001 fix filter ineffective -> change 3.

## Changes NOT Being Made
- C-001 V2 positive pin "only Bash registration is block-bare-python.sh" as originally argued for coverage reasons — superseded by change 3 (the allowlist is adopted for INV-001's reason, which V2 did not argue).
- R3-F4 blocking grade for continuation — rejected (X-001, V3 conceded); kept minor with tests inside the scanner (INV-005).
- R3-F2 text-half blocking grade — rejected (documented ceiling, line 40); kept minor with corrected header documentation.
- R1-F11 / R3-F8 "flaky" framing — rejected (repo precedent test_freshness_subagent_start_policy.py:86).

## Risk Summary
All changes edit only the merged findings list; rollback = use reviewer-1-card.yaml unchanged.

## Review Status
Auto-approved 2026-11-04 (non-interactive).
