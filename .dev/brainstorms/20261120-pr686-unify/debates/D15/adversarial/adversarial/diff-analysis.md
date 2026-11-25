# Diff Analysis: D15 Clay strengths bundle (OURS vs CLAY position papers)

## Metadata
- Generated: 2026-11-20 (UTC)
- Variants compared: 2 (Variant 1 = OURS, `position-OURS.md`; Variant 2 = CLAY, `position-CLAY.md`)
- Total differences found: 27
- Categories: structural (2), content (9), contradictions (2), unique (7), shared assumptions (7 raised: 5 UNSTATED, 1 CONTRADICTED, 1 STATED; 6 promoted to diff points)
- Input context for the debate: the 13 verdicts `debates/D01..D13/VERDICT.md` (every "Clay strengths to adopt" section), `FULL-REPORT.md` section 6, `H-design681-map.md` "Worth folding in".

## Structural Differences
| # | Area | Variant 1 (OURS) | Variant 2 (CLAY) | Severity |
|---|------|------------------|------------------|----------|
| S-001 | Section layout | Claim, Mechanism, 9 cited facts, costs, risks, gets-right | Same six sections, 8 cited facts | Low |
| S-002 | Evidence base | Facts cite verdicts, pr-a test lines, design lines | Facts cite PR inventory, design lines, verdicts | Low |

## Content Differences
| # | Topic | Variant 1 (OURS) approach | Variant 2 (CLAY) approach | Severity |
|---|-------|---------------------------|---------------------------|----------|
| C-001 | Unit of adoption | Per element: adopt as is, adopt with change, reject or defer | One interlocked set (grants, `E-NO-GRANT`, `answer-check`, `escalate`, merge gate, `refuse`, audit, hand-back) adopted with its test plan | High |
| C-002 | Status of the unbuilt verbs | Design text only (no `escalate`, `merge-gate`, `answer-check`, `asks.json` in master, pr-a, pr-p); adoption means writing them | One verb group with one JSON contract (ADD6, `orchestrator.md:140`), so build once | Medium |
| C-003 | The 62-reason audit table | Not adoptable as is: a test forbids 14 old approval reasons, which D01 needs back | A complete, test-pinned register of every skip and failure | Medium |
| C-004 | Wake transport | Two defects in Clay's code (M1 ack before state file, M2 abandoned wake lost) | Acknowledged delivery, 3 attempts, unread mark (no mention of the defects) | Medium |
| C-005 | Tier settings and hand-back | Tier path unverified (U28); `HANDBACK_MAX` = 3 not measured | Capabilities the owner's line lacks (hand-back of unfinished work, tiers) | Medium |
| C-006 | Contested rules carried inside the set | Reject them (assignment trigger, standing `pr.merge`, no guard, label writes, registry); keep owner's gates | Amend them one by one by owner override of named rows | High |
| C-007 | Who pays the rewrite | Every adopted row needs a rename and a re-home, so piecemeal costs more rows | Rewrite is paid per piece under cherry-picking, once under the set | Medium |
| C-008 | Readiness evidence | Unbuilt pieces carry no proof; PR 690 plan check is presence only | Closeout, report, PR 661 merged; PR 686 CI 6/6; PR 690 23,043 tests | Medium |
| C-009 | Where settings live | Per-repo config under `issue-watch.d/` (D07), not `repos.yaml` or the registry repo | `repos.yaml` keys (`grants`, tiers, `reach_daily_max`, merge keys) as the single settings home | Medium |

## Contradictions
| # | Point of conflict | Variant 1 position | Variant 2 position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Does "never ran live" or "unbuilt" count against a piece? | Counts: nine-row table, cap, `answer-check`, audit are spec text with no code (fact 4) | Does not count: the owner's `issue_pipeline` also never ran live (fact 8) | Medium |
| X-002 | Does piecemeal adoption multiply the rewrite? | Rewrite exists for every row in both approaches (rename D08, re-home D07), so the set does not avoid it (fact 9) | Rewrite is paid per piece instead of once (fact 6) | Medium |

## Unique Contributions
| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | OURS | Test at `pr-a/tests/issue_watch/test_audit.py:86-98` forbids the 14 approval reasons D01 needs | High |
| U-002 | OURS | Wake defects M1 and M2 (D10) | High |
| U-003 | OURS | `plan_check` placeholder gap (`<...>` passes) and `plan_body.py` presence-only check | Medium |
| U-004 | CLAY | Test plan T1 to T13, UNVERIFIED list and risk register (K11, K12, K14, K16) as one reusable live-test plan | High |
| U-005 | CLAY | PR 690 evidence (three review rounds, 23,043 tests) and PR 686 CI state | Medium |
| U-006 | CLAY | One verb group, one JSON contract, one refusal function (ADD6, `orchestrator.md:140, 767`) | Medium |
| U-007 | CLAY | Owner-column tables let the owner rule row by row (`orchestrator.md:109-140`) | Low |

## Shared Assumptions
| A-NNN | Assumption | Source Agreement | Classification | Impact | Status |
|-------|------------|------------------|----------------|--------|--------|
| A-001 | The verdicts D01 to D13 are the baseline although they are recommendations, not owner rulings (D01 R19, D04 R9/R10, D06 amendments await owner chat approval) | Both cite verdicts as settled | UNSTATED | High: every row's decision can flip if the owner overrules a verdict | Promoted |
| A-002 | Clay's pieces can be classified per element without breaking interlocks (for example `E-NO-GRANT` only sees verb-made writes; `refuse` binds only the verbs) | Both classify elements | UNSTATED | High: bundle versus piecemeal turns on it | Promoted |
| A-003 | A carrier PR exists for each element (PR 686, PR 690, or the unbuilt coordinator-skill PR); D14 has not yet chosen PR 686's fate | Both name PR 686, PR 690, "PR B" | UNSTATED | High: order and carrier of every row depend on D14 | Promoted |
| A-004 | The verbs bind what they claim: `refuse(argv)` sees only commands the verbs run; `answer-check` cannot tell a person from a script (D04, D05, D06) | Both treat them as controls | CONTRADICTED by D06 INV-003 and D05 K22 | High: "adopt" must not say "closes" | Promoted (as limit) |
| A-005 | The weighting rule applies to bundle choices as to single choices | Both argue under it | STATED (BRIEF-COMMON) | Medium | Not promoted |
| A-006 | A single file for per-repo settings will be chosen once (D07 per-repo config vs D04/D06 `repos.yaml` keys) | Neither paper settles it | UNSTATED | Medium | Promoted |
| A-007 | Names change before merge (`orchestrator` to `coordinator`, D08 action 8) for every element that carries a wire or verb name | Neither paper counts it | UNSTATED | Medium | Promoted |

## Summary
- Total structural differences: 2
- Total content differences: 9
- Total contradictions: 2
- Total unique contributions: 7
- Total shared assumptions surfaced: 7 (UNSTATED: 5, CONTRADICTED: 1, STATED: 1; 6 promoted to diff points)
- Highest-severity items: C-001, C-006, A-001, A-002, A-003, A-004
