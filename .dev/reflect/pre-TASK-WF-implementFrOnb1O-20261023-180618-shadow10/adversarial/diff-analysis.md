# Diff Analysis: reflect-pre reviewer cards (3 variants)
Generated: 2026-11-13T01:34:02Z. Variants: 3 (analyzer/sonnet t1b-1, qa/haiku t4-1, refactorer/opus t1a-1).

## Structural Differences
| # | Area | V1 (analyzer) | V2 (qa) | V3 (refactorer) | Severity |
|---|---|---|---|---|---|
| S-001 | Findings count | 3 | 6 | 1 | Low |
| S-002 | Scope sections | judgments on T1 candidates + T6/T7 | matrix-vs-spec + AC-vs-ledger | invariants only | Low |

## Content Differences
| # | Topic | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | CHANGELOG entry un-AC'd | F2 (cal 0.70) | F2 (cal 0.70) | not raised | Low (agreement) |
| C-002 | Plan bullets without AC | F3: 3.3 step 2, 3.1 step 1, 3.6 row, 3.4 step 1 (cal 0.45) | F3: T4 bullet 2, T5 key-desc reword, few-files re-check (cal 0.55) | not raised | Medium (partially competing item lists) |
| C-003 | Ledger anchor quality | not raised (T6 diff coverage confirmed instead) | F5 (5/10 doc anchors), F6 (T2.AC4 anchor) | not raised | Low |
| C-004 | T5 evidence scope | not raised | F1 (t5-checks vs t5.diff, cal 0.55) | prompts.py closed-list/example preservation confirmed instead | Medium |

## Contradictions
| # | Conflict | V1 | V2/V3 | Impact |
|---|---|---|---|---|
| X-001 | Is 3.4 step 1 --fix wording un-AC'd? | V1-F3 includes it as un-checked | Plan:70 (T2 AC3) reads "3.4, 3.7, 3.8 and 3.11 step 4 match the bullets above"; plan:62 bullet covers 3.4 step 1 | Medium — resolved by reading the AC text: 3.4 step 1 IS covered; V1-F3 sub-item dropped |
| X-002 | T5 evidence accurate or ambiguous? | V1 silent | V2-F1 says ambiguous/inaccurate | Low — t5-checks.log:5-6 header "key list and examples unchanged vs start"; scope of "key-list lines" undefined vs t5.diff:9-14 changing description lines inside the key block |

## Unique Contributions
| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V1 | F1: intermediate test:fail on T1/T2 expected-but-unnoted (t1/t2-extras.log) | Medium |
| U-002 | V2 | F4: INF-003 (Part A rows of 4.2) coverage asserted, rows never enumerated; spec absent | Medium |
| U-003 | V3 | F1: agent rule hand-copied twice, no test pin (known mirror-drift class) | Medium |

## Shared Assumptions
| # | Assumption | Source | Class | Promoted |
|---|---|---|---|---|
| A-001 | The archived ledger/diff artifacts are trustworthy records of the 2026-10-23 execution | all 3 cards | UNSTATED | yes |
| A-002 | ACs are the only gating instrument (ledger anchors are evidence, not gates) | V2 F5/F6 framing vs V1 acceptance of diff-as-proof | UNSTATED | yes |

## Summary
structural 2, content 4, contradictions 2, unique 3, shared assumptions 2 (both promoted). Highest severity: X-001 (Medium).
