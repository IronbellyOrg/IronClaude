# Merge log (step 5)

- Base variant: `variant-2-original.md` (reviewer-2, qa persona, opus class).
- Plan executed: `refactor-plan.md` (15 changes).
- Output: `<run>/adversarial/merged-review-card.md`.
- Merge date: 2026-11-16.
- Non-base sources: `variant-1-original.md` (reviewer-1, haiku class), `invariant-probe.md` (fault-finder).

## Applied changes

| Change | Finding | Status | Source note written above the finding in the card |
|---|---|---|---|
| 1 | F1 (MAJOR, blocking true, unpassable-check) | applied | base reviewer-2 F1; incorporated reviewer-1 F2; debate C-001, C-007, X-002; probe INV-001, INV-002 |
| 2 | F2 (MAJOR, blocking true, other) | applied | base reviewer-2 F4; incorporated reviewer-1 F3; reviewer-2 F2 part; debate C-002 |
| 3 | F3 (MAJOR, blocking true, unpassable-check) | applied | base reviewer-2 F2; incorporated reviewer-1 F4; debate C-003; probe INV-003, INV-012 |
| 4 | F4 (MAJOR, blocking true, missing-requirement) | applied | base none (new from reviewer-1 F1, narrowed by debate U-001 and round 2 of both advocates); probe INV-006, INV-014 |
| 5 | F5 (MAJOR, blocking true, missing-requirement) | applied | base reviewer-2 F6; debate U-004; probe INV-004, INV-010 |
| 6 | F6 (MAJOR, blocking true, contradiction) | applied | base none (new from reviewer-1 F6; debate U-002, strengthened by advocate 2 round 2) |
| 7 | F7 (MAJOR, blocking true, missing-requirement) | applied | base reviewer-2 F5; debate U-003; probe INV-013 |
| 8 | F8 (MINOR, blocking false, other) | applied | base reviewer-2 F3; incorporated reviewer-1 F5; debate C-004, graded minor |
| 9 | F9 (MINOR, blocking false, other) | applied | base reviewer-2 F10; incorporated reviewer-1 F8; debate C-005 |
| 10 | F10 (MINOR, blocking false, unpassable-check) | applied | base reviewer-2 F11; incorporated reviewer-1 F7; debate C-006, graded minor |
| 11 | F11 (MINOR, blocking false, missing-requirement) | applied | base reviewer-2 F7; debate U-005 |
| 12 | F12 (MINOR, blocking false, other) | applied | base reviewer-2 F8; debate U-006, graded minor after round 2; probe INV-005 |
| 13 | F13 (MINOR, blocking false, missing-requirement) | applied | new from probe INV-007; follow-up candidate |
| 14 | F14 (MINOR, blocking false, missing-requirement) | applied | new from probe INV-008; follow-up candidate |
| 15 | F15 (MINOR, blocking false, other) | applied | new from probe INV-009; follow-up candidate |

Notes on how changes were applied:

- Claim text, citations, severities, categories and blocking values were copied from the plan. No wording was added, dropped or changed. No typo fixes were needed.
- Four citations in the plan (Change 10 line 1, Change 15 lines 4 and 5) are delimited by backticks, not double quotes, because the quoted text itself holds double quotes. They are kept exactly as written in the plan.
- The `## Checked` section and the `## Self-report` section were written from the merge request's own text. The Verdict paragraph was written from the request's text.
- The aliases comment (line 2 of the card) lists PLAN, SRC, S0, S1, S2, SPEC and README as in the plan's Overview.
- The plan's "Changes NOT Being Made" list was honored: nothing from it is in the card.

## Post-merge validation

- Heading hierarchy: `## Verdict`, `## Findings`, `## Checked`, `## Self-report` only, in that order, no level skips. No leftover fill markers in the card (count 0).
- Findings in the card: 15 (F1 to F15), in order, each with a `<!-- Source: ... -->` comment above it.
- Findings with `blocking true`: 7 (F1 to F7). Findings with `blocking false`: 8 (F8 to F15).
- Every finding has at least one citation. Citation lines per finding: F1=9, F2=6, F3=5, F4=7, F5=9, F6=4, F7=7, F8=5, F9=3, F10=2, F11=2, F12=5, F13=4, F14=3, F15=5.
- Total citation lines in the `## Findings` section: 76 (the plan holds the same 76).
- Verbatim check: every one of the 76 citation lines was matched, as a whole line, against `refactor-plan.md` with a fixed-string full-line search. Missing: 0. Each of the 15 claim texts was found as a fixed string in the plan. Differences: 0.
- Contradiction re-scan: no new content was added, so no new contradiction was introduced. The claim in F6 (PLAN:162 states something false) and the citation of PLAN:162 in F4 point to the same plan line for different reasons, as in the plan.
- Line 1 and line 2 of the card are HTML comments in the requested form.

## Summary

| Measure | Count |
|---|---|
| Changes planned | 15 |
| Changes applied | 15 |
| Changes failed | 0 |
| Changes skipped | 0 |
| Escalations to the orchestrator | 0 |
