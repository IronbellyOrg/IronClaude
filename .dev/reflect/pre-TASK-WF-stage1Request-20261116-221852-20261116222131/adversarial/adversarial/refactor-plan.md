# Refactoring Plan: merge the three reviewer cards onto Variant 3

## Overview
- Base: Variant 3 (opus:refactorer), `variant-3-original.md`, combined score 0.8635
- Incorporated variants: V2 (one blocking finding), V1 (three findings and one stronger acceptance)
- Planned changes: 9 (C1 to C9 below); not made: 4
- Overall risk: Low (additive findings and one verdict change; no fact is taken from a card without the cited file line in that card)
- Target file: `../merged-card.md` (the merged reviewer card; the folder `adversarial/` above this one holds the merged output because `--output` named it)

## Planned Changes

| # | Change | Source | Target in base | Rationale (debate evidence) | Integration | Risk |
|---|---|---|---|---|---|---|
| C1 | Replace the verdict line "ship" with "revise" and name the reason | V2 verdict, V1 verdict | Verdict line | X-001: V1 and V2 say revise; V3's advocate conceded its "ship" missed C-005 (convergence 95%) | replace | Low |
| C2 | Add the blocking finding: the Constraints bullet "code-assigned severity in `src/superclaude/cli/**/*.py`" (plan:23) contradicts Task 1's outcome function that returns Blocking for a hit (plan:38); fix: narrow the ban to exclude the safety-only raise (source.md:61 "GR12 raise-only rule") and give a check that the narrowed text names `safety_route.py`. Record the dissent: V1's advocate rated it medium. | V2 F1 | before base F1, as the first finding | C-005 and X-002: all three advocates verified the text; winner V2 at 81 percent and 80 percent | insert first | Medium (reorders ids) |
| C3 | Add the ledger finding: the go row (stage-requests/README.md:18) names `TASK-WF-blockerStage1-20261116-030154` and says "Package not yet runnable"; fix: the row must name this package's id | V1 F1 | after the base twin-pin finding | C-001 and A-004: V1 80 percent, all three confirm the id mismatch; the entry check passes literally | insert | Low |
| C4 | Add the omission: "the 35 percent target" is in source.md:22 and missing from plan:23 (Also-not-built); fix: add the phrase | V1 F5 | after the C3 insert | C-004: V1 77 percent, no advocate disputes it | insert | Low |
| C5 | Strengthen the smoke-check finding: require `./artifacts/print-smoke.txt` to hold the literal output of `superclaude review safety-scan` for the T1 notes file | V1 F9 | new finding after the lint finding | C-011: V1 68 percent against V2's view that the manual check has concrete pass conditions | insert | Low |
| C6 | Keep base F3 (lint baseline), F4 (partial and blocking wording), F5 (live lines), F2 (second twin pin), F6 (grep restricted to import lines) as findings, each unchanged | base | in place | C-006 94 percent, C-007 84, C-008 79, C-009 79, C-010 63 | keep | Low |
| C7 | Keep base F7 (stored-tag check) and note the unresolved sub-question: V1 asks to name the string in the plan sentence, V2 sees no defect, V3 asks for the grep acceptance; either V1's or V3's fix is acceptable | V3 F7, V1 F4 | in place | C-003 unresolved at 50 percent | annotate | Low |
| C8 | Replace the coverage_judgement with a combined one: about 93 percent (V1 90, V2 95, V3 95), misses: the stored-tag check, the 35 percent target, the ledger package id, and the Constraints/Task 1 conflict | V1, V2, V3 | coverage_judgement | S-003 tie at 73 percent | replace | Low |
| C9 | Add the shared-assumption results as a short section: A-002 accepted (a Constraints versus Task conflict is a defect), A-003 rejected (pytest list incomplete), A-004 qualified (passes literally, wrong package id) | debate | after coverage_judgement | A-002 75 percent, A-003 95 percent, A-004 65 percent | append | Low |

## Changes NOT Being Made

| Diff point | Non-base approach | Why rejected |
|---|---|---|
| C-002 | V1 F2/F6: the plan lacks an owner summary the ledger still expects | `stage-requests/README.md:47-50` (Revision 4) cancels per-stage owner summaries; lines 11 and 25 are stale ledger text, not a plan defect (V2 99 percent, V3 65 percent). Kept only as a one-line note that the ledger text is stale |
| C-012 | V2 F2: spans 3, 17, 51 lack dispositions | a coverage-note gap, not a plan defect (all three advocates, 55 to 93 percent); source:3 was met, source:51 is honoured by plan:36, source:17 has no case |
| C-010 (fix) | V1 F8: add "docstrings and comments avoid those words" to Task 1 | base F6 (restrict the grep to import lines) is the stronger fix and V1's advocate agreed; V1's wording stays as an optional alternative in the note |
| S-002 label | V2's "drift" label for the conflict | kept as `[drift] [blocking]`: V2's own class; no better label is proposed by any advocate |

## Risk Summary
- Inserting the blocking finding first renumbers the finding ids; the merged card renumbers F1 to F12 (this plan first said F13; the merge executor counted 8 base findings plus 4 added, and the merge log records the correction) and keeps a trailing source id on each finding (V2 F1, V3 F2, ...) so each can be traced.
- Dissent is recorded, not dropped (C2 severity, C7 unresolved sub-question).
- Rollback: the three original cards remain unchanged as `variant-N-original.md`.

## Review Status
Auto-approved (non-interactive run).
