# Diff Analysis: Position paper comparison (QG2 escalation channel and naming rule)

Variant A = `variant-1-original.md` (OURS). Variant B = `variant-2-original.md` (CLAY).

## Metadata
- Generated: 2026-11-20
- Variants compared: 2
- Total differences found: 20 (2 structural, 6 content, 2 contradictions, 7 unique, 3 shared assumptions); 12 are debate points
- Categories: structural (2), content (6), contradictions (2), unique (7), shared assumptions (3; 2 promoted)

## Structural Differences

| # | Area | Variant A | Variant B | Severity |
|---|------|-----------|-----------|----------|
| S-001 | Section set | Claim, Mechanism, Cited facts (9), Costs, Risks, Gets right | Same six sections, 8 cited facts | Low |
| S-002 | Mechanism layout | One bullet per OD (OD-3, OD-4, OD-5) | OD-3 and OD-4 merged in one bullet, OD-5 separate | Low |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity |
|---|-------|-------------------|-------------------|----------|
| C-001 | OD-3 scope of the naming rule | Scope B: scan only `report-entry` and `escalate`; run U54 first | Scope A: all writers incl. workers, via handoff prompt line | High |
| C-002 | Handoff-prompt line forbidding attribution lines in worker PR bodies | Not adopted (conflicts with 25 of 30 PR bodies and with tool conventions) | Adopted as item 5 of the nine handoff sections (D:841) | Medium |
| C-003 | OD-4 refused mandatory escalation | Fail open: write, mask matched span, log refusal | Fail closed: exit 2, nothing written, nothing sent | High |
| C-004 | OD-5 channel for audit escalations (AU4a, AU4c, AU5) | Entry lines only until owner rules on nine rows and cap | Entry lines plus the notice step (ClickUp DM or Orca unread mark) | High |
| C-005 | Daily notice cap | Unsettled (D:1177 open vs D:686 settled); default 0 = no cap = chatter risk | Cap makes the notice safe; over-cap notices are batched, entries never dropped | Medium |
| C-006 | Measurement of false refusals | U54 must run before the rule is switched on | U54 bounds the risk; run alongside; refusal already bounded by skip rules | Low |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|-------------------|-------------------|-------------------|--------|
| X-001 | Does a refusal-style check keep the person informed? | A fact 5 and INV-013: closed means the person is never told and the hold stays on silently | B fact 3: refusal is the design's one style for bad input; the coordinator "must rewrite the text" | High |
| X-002 | Is scope A mechanically enforceable? | A fact 2: no check can scan a worker PR body (D:847 quote) | B mechanism: tests scan every `gh` and `orca` body the end-to-end tests produce | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | Re-count read-only of merged PR bodies: 25 of 30; clayphi 17 of 21, ironbelly 8 of 9 | High |
| U-002 | A | Mask condition: never mask a path, sha or number; write unmasked and log | Medium |
| U-003 | A | Owner memory rule `orchestration-decision-ledger-only` as a standard for notice volume | Medium |
| U-004 | B | Escalation shape rules: one per PR never per finding, warnings never reach the person, entry always written, cap never drops an entry | High |
| U-005 | B | Nine-row table with "Was" column and `If you do not answer:` lines (D:676-680, D:692) | Medium |
| U-006 | B | Test coverage design: scan of every template and fixture, plus fake `launch.effective` test (D:847) | Medium |
| U-007 | B | Orca decision gate as the second of three delivery ways (D:682) | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Impact | Status |
|-------|------------|------------------|----------------|--------|--------|
| A-001 | `report-entry`, `escalate`, `names_check` and a notice sender will exist when the rule applies (none is in master, pr-a or pr-p) | Both discuss behaviour of these verbs | STATED (A fact 8; B "UNVERIFIED") | Medium | Not promoted |
| A-002 | Rulings 15, 27, 28, 39 are the owner's rulings | Both cite them as the rule's source | UNSTATED (the design's "owner" means Clay; no ironbelly record found) | High | Promoted |
| A-003 | A person reads the living-report entry lines in time to act on a post-merge violation | A treats entry lines as sufficient; B treats them as the base channel | UNSTATED | High | Promoted |

## Summary
- Total structural differences: 2
- Total content differences: 6
- Total contradictions: 2
- Total unique contributions: 7
- Total shared assumptions surfaced: 3 (UNSTATED: 2, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, C-003, C-004, X-001, A-002, A-003
- Debate points for convergence: S 2 + C 6 + X 2 + A 2 = 12

## Taxonomy tags
S-001 L1; S-002 L1; C-001 L2; C-002 L2; C-003 L3 (guard, validation rule); C-004 L2; C-005 L2; C-006 L1; X-001 L3; X-002 L2; A-002 L2; A-003 L3 (state, boundary: a person reads in time).
