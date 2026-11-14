# Refactoring Plan (Q22)

## Overview
- Base: Variant 1 (proposal-A)
- Incorporated: Variant 3 (2 changes), Variant 2 (1 change), all advocates (1 change)
- Changes planned: 4; rejected: 3
- Overall risk: Low
- Merged output: `../merged-proposal.md`

## Planned Changes

### Change 1: key the rule on the producer's worst normal write gap
- Source: Variant 3 (round1-advocate-V3.md Strengths, C-002, X-003); Variant 1 advocate Concessions (proposed merge)
- Target: base "Answer" and step 1
- Approach: replace. Rule becomes: a file is stale when its `generatedAt` age exceeds the larger of (a) three times the producer's nominal interval and (b) the producer's documented longest normal gap between writes, backoff included. For the observer: interval 15 s, so (a) = 45 s; it rewrites the file once per cycle even after failures (`commands.py:294-297`) and waits up to 60 s after errors plus a cycle of up to 15 s (`collector.py:28-30`), so (b) is about 75 s (inference from the code, not measured); threshold about 75 s. If a measurement shows a longer gap, the note uses the measured value.
- Rationale: C-002 and X-003 won by V3 (70%); both V1 and V3 advocates proposed this hybrid.
- Risk: Low

### Change 2: two ages, never one
- Source: Variant 3 advocate (X-001), Variant 2 advocate (Strength 2)
- Target: base "What it unlocks", first bullet
- Approach: replace. File age (`generatedAt`, "is the writer still alive") is distinct from data age (the snapshot's `source.status` and `source.observedAt`, which already carry the observer's own 45 s feed verdict: `view.py:543-553`). Readers show both; "stale file" and "stale data" are separate words, in line with the mapping-table rule "never show one as the other" (ADJ line 250).
- Rationale: X-001 discussion; merged-requirements.md line 279.
- Risk: Low

### Change 3: clock rule
- Source: all three advocates' A-001 responses
- Target: base step 1 and "What stays unresolved"
- Approach: insert. The rule assumes the reader and producer share a host clock; a reader that computes a negative or implausible age prints "age unknown", never "current". CO-04 states a clock-skew allowance alongside its copy delay.
- Risk: Low

### Change 4: replace the interim rule in the note
- Source: Variant 2 advocate Concession 1
- Target: base step 1
- Approach: append. The note replaces ADJ's interim "older than one producer cycle" rule, which would flicker on ordinary timing.
- Risk: Low

## Changes NOT Being Made
| Diff point | Non-base approach | Why rejected |
|---|---|---|
| C-003 | V3: Coder record fixed at 2 minutes now | V1 won 88%; no Coder producer exists; V3 conceded |
| C-004 | V2: keep the placeholder | V1 won 70%; a rule closes it without a guess |
| C-005 | V3: deliver within 2 minutes | V1 won unanimously; budget too tight after a 75 s gap |

## Review Status
Auto-approved (non-interactive), 2026-11-14.
