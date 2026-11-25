# Refactoring Plan

## Overview

- Base variant: Variant 1 (opus:architect), combined score 0.960
- Incorporated variant: Variant 2 (sonnet:analyzer), combined score 0.867
- Planned changes: 17 (CH-1 to CH-17)
- Changes deliberately not made: 9 (listed below)
- Overall risk: Medium (the cost section and the trigger section are rebuilt; the rest is additive)
- Unresolved debate points adjudicated here: S-001, S-004, C-002, C-003, C-004, C-008, X-002, A-002, A-006

## Planned Changes

| # | Change | Source (variant, section) | Target in base | Rationale (debate evidence) | Approach | Risk |
|---|--------|---------------------------|----------------|-----------------------------|----------|------|
| CH-1 | Number the section headings | V2 sections 1 to 8 | All headings | S-001 adjudicated V2 (55%): easier to cite | restructure | Low |
| CH-2 | T1 and T2 skip paths the story lists as new | V2 section 3 | Triggers | X-005 agreed V2 (90%); V1 conceded; BMAD splits UPDATE and NEW (`bmad-create-story/SKILL.md` line 311) | replace | Low |
| CH-3 | T5 thresholds: more than 8 criteria or more than 12 top-level tasks | V2 T3 | Triggers (T5) | C-001 agreed MERGE (90%); V1 conceded it over-fires at 6 | replace | Medium |
| CH-4 | T4 regex: narrower, word-bounded list, keep `storage` and `protocol` | V2 T3 plus V1 T4 | Triggers (T4) | C-001 MERGE; the brief names storage and protocol as the architecture stories | replace | Medium |
| CH-5 | Shape stop before any trigger: zero criteria, a task without an `AC:` reference, or an unnumbered criteria list returns the story to BMAD; no Given/When/Then rule | V2 T4, adapted | Flow step 1 and Triggers | A-004 agreed V2 (85%); but a story with zero criteria cannot be repaired by a brainstorm, and the BMAD template makes criteria free-form text (`template.md` line 15) | insert | Medium |
| CH-6 | Rebuild the cost section: counting rule, component formulas, arm-split rows, reviser call counted, arithmetic corrected, script build cost, tokens and wall time logged | V2 section 4 plus V1 reviser | Cost comparison | S-002 V2 (85%); C-003 and X-002 adjudicated MERGE (70% and 65%); A-003 and A-007 agreed NEITHER (90% and 85%); scorer found 18 vs 17 and 31 vs 30 slips | replace | Medium |
| CH-7 | Store the story byte-exact as `source-story.md` | V2 R7 | Flow step 1, merge rule R7 | C-007 agreed V2 (85%) | append | Low |
| CH-8 | `ac-map.md` as data, predicted executor ids checked against the ledger at completion | V2 R3 | Merge rules R4 | C-006 agreed MERGE (90%) | append | Medium |
| CH-9 | Completion closure: a story is complete only when each id has a passing executor row or an approved change-log row | V2 R9 | Merge rules R9 | Agreed U-008 value High; closes the loop V1 lacked | append | Medium |
| CH-10 | Re-run the id checks after every reviser pass and after the repair | V2 R8 | Merge rules R8 | C-005 agreed V1 (90%) for the rebuild; V2's re-check kept as a second guard | append | Low |
| CH-11 | Provenance tag on every list item or section that IronClaude adds, with its source file | V2 R5, trimmed | Merge rules R10 | C-006 MERGE; per-line `[BOTH]` dropped because a script cannot test its meaning | append | Low |
| CH-12 | Trial plan: at least 12 stories, metrics M1 to M4, missed-conflict metric, AC-loss stop rule for option 2, trigger list frozen during the release | V2 section 6 | Trial plan | S-004 adjudicated MERGE (65%); C-008 MERGE (70%) | merge | Medium |
| CH-13 | Command flags: `--output` for brainstorm and adversarial, `--report-dir` for spec-panel and workflow | V2 (adversarial, brainstorm) plus V1 (panel, workflow) | Flow | C-009 agreed V1 (95%) on `--report-dir` where required; `~/.claude/WORKER-CONTRACT.md` brief table lists `--output <dir>` for brainstorm and adversarial; V1 passed `--report-dir` to both and its brainstorm merged path would not be fixed | replace | Medium |
| CH-14 | Define every acronym on first use; add the zero-criteria guard; add likelihood and impact to each risk | Debate (scorer CL4, E3, R1 for V2) | Whole document | Qualitative gaps found in the scoring | insert | Low |
| CH-15 | Candidate trigger for the next release: the one-call code accuracy check (`current` or `out_of_date`) | Debate A-005 | Trial plan | A-005 agreed NEITHER (85%): neither variant used it; it is part of coordinator-only `/sc:issue --claim` (`claim.md` line 58), so it is a candidate, not in the frozen list | insert | Low |
| CH-16 | State the coordinator dependency explicitly (keeps the review count, answers escalations) | Debate A-006 | Flow and risks | A-006 adjudicated MERGE (65%) | insert | Low |
| CH-17 | `/sc:workflow` depth follows story size: quick for simple, standard for medium and for the alternate arm, deep only when T3 and T4 both fired | V1 plus V2, plus `chains.md` rows | Flow | C-009; `~/.claude/skills/sc-issue-protocol/refs/chains.md` maps simple to quick and medium to standard | replace | Low |

## Weaknesses of the base addressed

| Weakness | Better variant or fix | Fix approach |
|----------|----------------------|--------------|
| T1 fires on new files | V2 | CH-2 |
| Cost table unreconciled, no formulas | V2 | CH-6 |
| No malformed-story gate | V2 | CH-5 |
| `--report-dir` on brainstorm and adversarial leaves the merged-output path undefined | V2 | CH-13 |
| No completion closure | V2 | CH-9 |
| Acronyms not defined | none (both gaps) | CH-14 |
| Zero-criteria story passes the gate | none | CH-5 |

## Changes NOT Being Made

| Diff point | Non-base approach | Why the base approach stands |
|------------|-------------------|------------------------------|
| X-001 | V2 R4: mark one task `BLOCKED-AC-n` and continue the other tasks | `/sc:implement` Q8 stops at an incomplete task (SKILL.md line 150); V2 conceded |
| X-004 | V2: spec-panel and workflow calls without `--report-dir` | Both commands refuse the run (spec-panel.md line 458, workflow.md line 90); V2 conceded |
| C-005 | V2: treat the merged spec as the spec and re-check afterwards | V1 R7 removes the rewording risk by construction (90% agreed) |
| C-004 | V2: `AC-n` as the canonical key | `AC-n` collides across stories in one release; the full id is canonical, the short form is only an alias inside one story folder (55%) |
| C-001 | V2 T5: panel FAIL with at least 2 blocking findings | V1's location-based T6 separates code gaps from wording (C-002, 55%) |
| C-001 | V2 T4: Given/When/Then required in every criterion | The BMAD template makes criteria free-form numbered text; unverified assumption |
| C-006 | V2 R5: tag every line, including `[BOTH]` | Weakly enforceable; replaced by CH-11 |
| C-001 | V1 T1 and T5 as written (6 and 6) | CH-2 and CH-3 |
| U-006 | V2: a not-executable story goes to the alternate arm | A story with zero criteria needs BMAD, not a brainstorm; replaced by CH-5 |

## Risk Summary

| Change | Impact | Rollback |
|--------|--------|----------|
| CH-6 cost rebuild | A wrong formula misleads the trial design | The trial records measured calls; replace the table after the release |
| CH-4 and CH-3 thresholds | Over-fire or under-fire | Marked as estimates; the trial calibrates them; trigger-removal rule |
| CH-5 shape stop | Rejects stories BMAD would accept | Stop reason is recorded; BMAD re-runs `bmad-create-story` |
| CH-13 flags | A flag that a command does not accept | Each flag was read in the command file's Unattended mode section |

## Review Status

Auto-approved (non-interactive run, `--unattended`). Approval timestamp: 2026-11-22T21:10:00Z.
