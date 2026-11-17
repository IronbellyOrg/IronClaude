# Merge log

- Base: variant-2-original.md (reviewer-2, qa persona, opus class)
- Incorporated: variant-1-original.md (reviewer-1, haiku class) and invariant-probe.md (fault-finder)
- Plan: adversarial/refactor-plan.md (auto-approved)
- Output: ../merged-review-card.md

## Changes (plan Changes 1 to 16)

| Change | Plan instruction | Card finding | Status | Reason |
|---|---|---|---|---|
| 1 | V2 F1 widened, merge V1 F2; drop `rf-qa-qualitative.md:810`; `:796` a side remark | F3 | applied | Plan text inserted; :810 absent from the card; :796 kept only as a remark and one citation line |
| 2 | New F1 from V1 F1, upgraded by INV-001, INV-002, INV-011 | F1 | applied | Inserted as the first finding |
| 3 | New F2 from V1 F3 plus INV-003 | F2 | applied | Inserted as the second finding |
| 4 | V2 F3 arms, minor, hook qualification | F4 | applied | Plan text inserted |
| 5 | V2 F2 | F5 | applied | Plan text inserted |
| 6 | V2 F4 | F6 | applied | Plan text inserted |
| 7 | V2 F5 | F7 | applied | Plan text inserted |
| 8 | V2 F6 | F8 | applied | Plan text inserted |
| 9 | V2 F7 | F9 | applied | Plan text inserted |
| 10 | V2 F8 and V2 F9 (end-point claim dropped, hash description kept) | F10 | applied | Plan text inserted; no end-point text present |
| 11 | V1 F4 | F11 | applied | Plan text inserted |
| 12 | V2 F10 | F12 | applied | Plan text inserted |
| 13 | INV-007 follow-up | F13 | applied | Under "## Follow-up candidates" |
| 14 | INV-009 follow-up | F14 | applied | Under "## Follow-up candidates" |
| 15 | INV-010 follow-up | F15 | applied | Under "## Follow-up candidates" |
| 16 | INV-004 follow-up | F16 | applied | Under "## Follow-up candidates" |

Plan lists V2 F2, F4, F5, F6, F7, F8, F9, V1 F4, V2 F10 as F5 to F12 in that order; the final text maps them as F5=V2 F2, F6=V2 F4, F7=V2 F5, F8=V2 F6, F9=V2 F7, F10=V2 F8 plus the hash part of V2 F9, F11=V1 F4, F12=V2 F10. The card follows the final text.

## Provenance tags used (`<!-- Source: ... -->` above each finding)

| Finding | base | incorporated | debate points | probe ids |
|---|---|---|---|---|
| F1 | none (new from V1 F1) | V1 F1 | X-001, U-001, A-003 | INV-001, INV-002, INV-011 |
| F2 | none (new from V1 F3) | V1 F3 | U-002 | INV-003 |
| F3 | V2 F1 (widened) | V1 F2 | C-001, A-002 | INV-008 |
| F4 | V2 F3 | none | U-004 | none |
| F5 | V2 F2 | none | U-005 | none |
| F6 | V2 F4 | none | U-006 | none |
| F7 | V2 F5 | none | U-007 | none |
| F8 | V2 F6 | none | U-008 | none |
| F9 | V2 F7 | none | C-003, U-009 | INV-005 |
| F10 | V2 F8 and hash part of V2 F9 | none | X-002, U-010 | INV-008 |
| F11 | none (new from V1 F4) | V1 F4 | U-003 | none |
| F12 | V2 F10 | none | U-012 | INV-012 |
| F13 | none | none | none | INV-007 |
| F14 | none | none | none | INV-009 |
| F15 | none | none | none | INV-010 |
| F16 | none | none | none | INV-004 |

Note on tags: the plan states probe ids explicitly only for F1 (INV-001, INV-002, INV-011), F2 (INV-003) and F13 to F16. The ids INV-008 (F3, F10), INV-005 (F9) and INV-012 (F12) and the diff point ids (taken from diff-analysis.md) are my mapping from the content of the probe table and the diff analysis; they are tags only and add no fact or citation.

## Post-merge validation

(a) Structure. Headings found, in order: `## Verdict`, `## First-review findings`, `## Findings`, `## Follow-up candidates`, `## Checked`, `## Self-report`. The two HTML comment lines (merge header and alias line) are lines 1 and 2. Result: pass.

(b) Counts. Findings: 16 (F1 to F16, one line each). Blocking true: 3 (F1, F2, F3). Blocking false: 13 (F4 to F16). F1 to F12 sit under "## Findings", F13 to F16 under "## Follow-up candidates". Citation lines (lines `- <path>:<line> "<quote>"`): 72 in the card (Grep count), 72 in the plan. Per finding: F1 14, F2 4, F3 11, F4 5, F5 5, F6 4, F7 2, F8 4, F9 4, F10 4, F11 2, F12 4, F13 3, F14 2, F15 2, F16 2. Result: pass (16, 3 and 13, 72).

(c) Citation fidelity. The citation lines of the card and of the plan were listed with Grep (same pattern, content mode) and compared by reading, line by line and in the same order: all 72 are identical. Result: pass. No em dash or en dash in the card (Grep: 0 matches).

## Deviations from the plan

1. Section order. The plan's "Output format" item 2 lists `## Checked` before `## Follow-up candidates`; the plan's "Final text of the card" and the task instruction put `## Follow-up candidates` before `## Checked`. The card follows the final text and the instruction.
2. Heading text. The plan's final text has "Follow-up candidates (Medium, non-blocking)"; the card uses "## Follow-up candidates" as the instruction names it.
3. No other deviation: no text was added, dropped or reordered inside a finding.
