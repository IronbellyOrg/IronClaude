# Refactoring Plan: merge into the final cut list (Step 4, 2026-11-16)

## Overview

- Base variant: `variant-1-opus-architect.md` (combined 0.864; won the tiebreaker on debate points 8.2 to 4.95).
- Incorporated: V2 (`variant-2-sonnet-analyzer.md`) and V3 (`variant-3-haiku-qa.md`) strengths listed in `base-selection.md` section 5, and the converged positions in `debate-transcript.md` (scoring matrix).
- Merged output to produce: `../final-cuts.md` (the final list the owner reads and the trim agents execute).
- Approval: auto-approved (non-interactive).

## Planned Changes (apply to V1's section 3 "Final list of cuts")

1. **C1** keep as V1: cut the classifier (S1 T5, T9, T10, T11, T12; S2 T7; S0 T6, T8). Keep the safety vocabulary scan, rebuilt standalone (V2): it no longer depends on the classifier or the ledger codec.
2. **C2** (V1 plus M1, narrowed by V3): cut the `follow-ups/1` codec, 16-column table, observation, offer and filing tables, nine states, filing state machine, sweep, `follow-ups` command group, worker-contract keys and shadow summary (S1 T4, T7, T8; S2 T1, T2, T5, T6, T8). No new list file: the list is the reviewers' own "follow-up candidates" section plus `notes.md`. One plain file only if the owner later wants one cross-reviewer list per run. Keep capture-failure handling (V3): a missing notes file is reported as "no notes file", never as "no findings".
3. **C3** as V1 shrink (print-only): the `/sc:implement` final step prints every non-superseded minor line of the tasks' `notes.md` and runs the safety scan over them; edit `SKILL.md` and `refs/managed-workspace.md`, never `refs/qa.md`; copy to the plugin twin (M4, `test_h`). Cut S3 T10 (promote switch), the sweep, the new command group.
4. **C4** as V1: no skill folder, registry, scale map, doctor check or T1 to T17 (S1 T1, T2, T3, T6, T14, T15). Keep the existing `test_c_s1_s3_copied_verbatim`, one reverse scan (S3 T13, target the old sentence after the opening, M5), and the installed-path protection (V3). S3 T11 and T12 keep re-pinning and add M3 (`test_review_severity_mapping.py:23`, `test_review_prompt_overrides.py:24`); replace changed literals with consequence checks, never delete tests (V3).
5. **C5** as V1 shrink: no allow-list or registry concept; copy S1 to S3 into the two MDTM templates; keep pinned plugin twins; retired `/sc:task` and task-builder files stay unedited.
6. **C6** corrected (V2, V3): cut the seeded-recall experiment and the hash-bound rulings (S0 T7, S3 T3, T4). State that the stage 0 T4 regrade is a lower bound and cannot measure discovery (A-002). Pair it with RT1 and keep one small planted-defect check as part of the live RT1 audit after the switch.
7. **C7** as V1: cut stage 2 except the shrunk carrier print (C3) and keep one active-flow smoke check (V3); cut S3 T1. The five-run gate goes.
8. **C8** shrunk: RT1 worded "any real blocker found in a Medium list" (V2), plus the owner reading the first five runs' Medium lists; cut baselines M1, M12, M10b (S3 T2). Keep S3 T14 only as a short note that carries RT1, the first-five-list read, the small planted check and the safety rollback; stage 4's entry check reads it.
9. **C9** corrected: cut S0 T2, T3, T5 to T8; keep T1 and T4; fold T10 into T4's output; keep T9 as a short errata note (V1 and V2 concede), rewired to depend on T1 and T4 only.
10. **C10** corrected: cut hash and ruling fields; keep a summary only where a later entry check reads it (stage 3 note read by stage 4). Cut S1 T16, S2 T8, S4 T6, S0 T10 (folded).
11. **C11** corrected (V2, V3; V1 conceded): keep stage 3 and stage 4 as separate packages. Move the atomic copy of S1 to S3 into all ten tuple files into stage 3, in the same change as `pragmatic.md` (M2; one task checked by `uv run pytest tests/skills/test_review_severity_rule.py`). Stage 4 keeps the merge-rule lines, spec-panel and the doubt-wording rewrites.
12. **C12** corrected: do not defer and do not weaken the tuple; copy atomically (all three agree). Defer only edits beyond the copy, with the reachability check of who dispatches the four rule prompts still owed.
13. **C13** corrected (V2): build the five Review Panel items; quorum of two valid reports only when two or more reviewers were launched; keep parsable-finding behaviour, Q68 run log and integrity checks; verify launcher suitability (V3); do not build the rest. These are not part of the 54-task count and no code is written in this run.
14. **C14** corrected (V1, V3): record the "answer today / defer / drop" items as recommendations pending the owner in pending, decided and out-of-v1 sections; do not convert any into an owner answer; OD3 stays open.
15. **Target structure** (recompute without double-counting rewards): stage 0 = 3 tasks (T1, T4 with the results folded in, T9 errata); stage 1 = 2 tasks (standalone safety scan with its command and tests; the `/sc:implement` print with the scan call, plugin twin copy and tests, including the active-flow smoke check); stage 2 package withdrawn (merged into stage 1); stage 3 = 10 tasks (post-fix helper T5, `pragmatic.md` v2 with the per-run offer, the atomic ten-file copy, `rf-qa`, `rf-qa-qualitative` with OD16, `rf-analyst`, re-pins T11 and T12 extended by M3, reverse scan T13, short note T14; cut T1, T2, T3, T4, T10); stage 4 = 4 tasks (doubt-wording rewrites in templates and rule prompts beyond the atomic copy, merge-rule lines in four skills, spec-panel narrowing and its re-pin, one final pinning test run; cut T5 strict switch and T6 summary). Total 19 tasks in 4 packages, from 54 in 5.
16. **Order and review:** trim the plans only after the four running plan reviews are stopped. After the trim: one mechanical dependency check (every `Depends on` names a live task, no removed command or path remains in installed text, G10 path check) plus one reviewer pass per trimmed package (V2, V3 on A-001).

## Changes NOT Being Made

- Reversing the owner's approval of the `/sc:implement` carrier (C3): kept in print-only form (all three variants converged).
- Merging stages 3 and 4 into one package (C11): rejected by V2 and V3; V1 conceded.
- Weakening or narrowing the `S1_S3_FILES` tuple to avoid editing the prompts and templates: rejected (V1, V3; V2 conceded).
- Cutting the post-fix helper (S3 T5) with the ledger tooling (V3): kept, purpose unverified.
- Dropping Q68 run log checks, parsable-finding handling, CI mirror check, G10 or static QA checks (owner-kept).

## Risk Summary

| Change | Risk | Mitigation |
|---|---|---|
| Cutting classifier and ledger machinery | no structured evidence for a later classifier | the rule text and the scan carry S and D; Jev stays deferred under OD3 |
| Cutting seeded recall | recall of planted defects unmeasured before the switch | RT1 live audit plus a small planted check after the switch; the regrade is stated as a lower bound |
| Atomic ten-file copy in stage 3 | one larger change set | one check, `test_review_severity_rule.py`; no registry or staging needed |
| Re-pinning tests | removing real checks | consequence checks replace literals; no test deleted wholesale |
| Trimmed plans unreviewed | new defects from dependency rewiring | mechanical dependency check plus one reviewer pass |

## Review Status

Auto-approved 2026-11-16.
