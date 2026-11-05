# Refactoring Plan (merge of three reviewer cards into one verdict card)

## Overview

- Base: Variant 3 (`variant-3-original.md`)
- Incorporated variants: V1 (`variant-1-original.md`), V2 (`variant-2-original.md`)
- Output: `merged-verdict-card.md` in this folder, using merged ids M-1.. (source ids kept in brackets)
- Review status: auto-approved (non-interactive)
- Overall risk: Low (additive, text-level merge; no repository files are touched)

## Planned Changes

| # | Change | Source | Target in base | Approach | Rationale (debate evidence) | Risk |
|---|---|---|---|---|---|---|
| 1 | Add R2-1 as blocking: Task 3 acceptance grep `models opus,sonnet` (plan:65) cannot pass with the mandated bullet "default models opus,sonnet,haiku" (plan:62); fix: grep for `--models` | V2 R2-1 | new blocking item after R3-2 | insert | C-004 won 95% unanimous; orchestrator re-read plan:62 and :65 | Low |
| 2 | Add R1-2 as blocking: `docs/testing/v5.0.0/user/D12-reflect.md:235` pins `--model claude-opus-4-8`; Task 2 changes the default; spec item (4) asks to update pinned strings; fix: add D12:235 to Task 2 | V1 R1-2 | new blocking item | insert | C-002 won 90% unanimous; orchestrator grep confirmed the line; classified blocking as a missing required deliverable (spec item 4) | Low |
| 3 | Add R1-1 as minor with an added acceptance criterion: Task 5 activates the primary retry ladder in workspaces that export the four variables (`defaults.sh:37,48,67,69`; `retry.md:162`); record it in `./artifacts/t5-notes.md` and in Task 6 "Known consequences" | V1 R1-1 | new minor item | insert | C-001 won 90% unanimous; severity kept minor by the blocking definition (intended consequence of the owner-requested rename, no wrong behaviour, no false claim); the calibrator argued blocking, the orchestrator decided minor | Low |
| 4 | Add R1-3, R1-4, R1-8 (merged with R3-3), R1-9 (merged with R3-6), R2-2/R3-7/R1-12 (one item for final-report.md:77), R2-3/R3-5/R1-10 (one scope item, plus the markdown-body scan gap raised by the calibrator), R2-4, R2-5, R1-5 (merged with R3-8 part) as minor items | V1, V2 | minor list | merge duplicates | C-003, C-007, C-009, C-010, C-011 | Low |
| 5 | Split R3-9 into separate minor items (ordering/link target, Task 9 dependency, duplicated sentence, test overlap, allow-list entry, Task 9 anchor correction) | V3 R3-9 | minor list | restructure | S-002 won by V1 60%: bundled findings hurt triage | Low |
| 6 | Add the legacy-slot note: the plan uses T1Model01/T1Model02, which `defaults.sh:63-65` calls legacy slots kept for swarm and reflect; state this in retry.md | V1 U-001 | minor list | insert | U-001 unique contribution | Low |

## Changes NOT Being Made

| Diff point | Non-base approach | Rationale |
|---|---|---|
| X-002 / C-012 | V1 R1-6 "Task 8 points at the wrong module" | Rejected: plan line 116 says "search tests/ for count_model_aliases" and names no path; V3 and the debate (C-012 won by V3, 65%) agree; the real location (`tests/swarm/test_coder_tier_env_2026_10.py`) is a useful hint, kept as a note |
| X-001 | V1 verdict PASS_WITH_NOTES | Rejected: unanimous debate; two advocates confirmed R2-1 and R3-1; V1's own R1-9 contradicts it |
| C-008 | R3-8 "Task 8 is scope creep" as a defect | Kept as a minor note only: Task 8 is not requested by the spec but is cheap and guards the follow-up; owner agreement is the open question |
| C-013 | R1-3 stays minor; the `unrecognized_model` notice is real (observed in the orchestrator's throwaway-HOME run, not recorded in the repo), so the fix is to cite or drop the sentence | Orchestrator evidence |
| R3-7 / R1-11 | Provenance claim "commit 70ef6486" | Resolved: `git log -S"model: sonnet"` on `audit-scanner.md` returns 70ef6486, so the claim holds for audit-scanner.md; the reviewer-1 doubt is withdrawn |

## Risk Summary

Text-level merge with no repository mutation. Rollback: delete `merged-verdict-card.md`; the three source cards are unchanged.

## Review Status

auto-approved (non-interactive run)
