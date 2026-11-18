# Merge Log: cuts debate (Step 5, 2026-11-16)

- Merged output: `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/cuts-debate/final-cuts.md`
- Base: `variant-1-opus-architect.md`. Plan: `refactor-plan.md` (16 planned changes). Evidence: `variant-2-sonnet-analyzer.md`, `variant-3-haiku-qa.md`, `debate-transcript.md`, `base-selection.md`, `../source.md`.
- Executor: merge-executor. Edited nothing outside `cuts-debate/`; no commit, no staging.

## Applied changes

Section references are to `final-cuts.md`: (a) cut table, (b) per-package structure, (c) cross-package facts, (d) owner flags, (e) open items.

| # | Plan change | Status | Before (V1) | After (final-cuts.md) | Provenance tag |
|---|---|---|---|---|---|
| 1 | C1 classifier | APPLIED | cut S1 T5, T9 to T12, S2 T7, S0 T6, T8; keep S1 T13 as a safety scan | same cuts; the scan is rebuilt standalone with no dependence on the classifier or the codec (a) C1, (b) S1 task 1 | Base (modified); Variant 2 section 1 row C1 |
| 2 | C2 ledger tooling | APPLIED | cut the machinery, M1 drops the list file | no codec, ledger, sweep or command group; no new list file; one plain file only if the owner wants one list; capture failure reported as "no notes file" (a) C2, (d) 5, (b) S1 task 2 | Base (modified); Variant 1 M1; Variant 3 missed keep 1 |
| 3 | C3 carrier | APPLIED | shrink to print-only, cut S3 T10 | print of non-`superseded` `notes.md` minors plus the scan; `SKILL.md` and `refs/managed-workspace.md` only, never `refs/qa.md`; plugin twin copy (`test_h`) (a) C3, (b) S1 task 2 | Base (original); Variant 1 M4 |
| 4 | C4 skill folder and registry | APPLIED | cut S1 T1, T2, T3, T6, T14, T15; keep copy test and S3 T13 | same; adds installed-path protection and re-pin of three tests with consequence checks, no test deleted (a) C4, (b) S3 new 7, 9 | Base (modified); Variant 1 M3, M5; Variant 3 E3, missed keep 2 |
| 5 | C5 allow-list, MDTM, parity | APPLIED | shrink, copy S1 to S3 into the MDTM templates | no allow-list or registry concept; copy in the S3 copy task; pinned twins kept; retired files unedited (a) C5 | Base (original) |
| 6 | C6 seeded recall | APPLIED | cut S0 T7, S3 T3, T4; "regrade plus scan protects" | same cuts; regrade stated as a lower bound that cannot measure discovery (A-002), paired with RT1 and one small planted check after the switch (a) C6, (b) S0 new 2, S3 new 10 | Base (modified); Variant 2, Variant 3 |
| 7 | C7 shadow stage | APPLIED | cut stage 2 except S2 T3, cut S3 T1 | same; one active-flow smoke check added to S1 task 2; S2 T4 is cut as the plan says (see tension note below) (a) C7, (b) S1 task 2 | Base (modified); Variant 3 |
| 8 | C8 audit window | APPLIED | RT1 plus first five lists; cut S3 T2, T14 | RT1 worded "any real blocker found in a Medium list"; baselines cut; S3 T14 kept only as a short note carrying RT1, the first-five read, the small planted check and the safety rollback (a) C8, (b) S3 new 10 | Base (modified); Variant 2 section 1 row C8 |
| 9 | C9 stage 0 | APPLIED | cut T2, T3, T5 to T9; keep T1, T4; fold T10 | cut T2, T3, T5 to T8; keep T1, T4, T9 (errata, depends on T1 and T4 only); T10 folded into T4's output (a) C9, (b) S0 | Base (modified); Variant 1 and Variant 2 concessions |
| 10 | C10 summaries | APPLIED | cut all five summaries and the ledger fields | cut S1 T16, S2 T8, S4 T6, S0 T10 (folded); keep S3 T14 shortened because the S4 entry reads it; hash and ruling fields cut (a) C10, (b) S3 new 10, S4 new 1 | Base (modified); Variant 2 section 1 row C10 |
| 11 | C11 merge stages 3 and 4 | APPLIED | merge into one package | two packages kept; the atomic copy of S1 to S3 into all ten tuple files moves into one new stage 3 task in the same change as `pragmatic.md` (a) C11, (b) S3 new 3 | Base (modified); Variant 2, Variant 3; Variant 1 M2 |
| 12 | C12 defer prompts and templates | APPLIED | shrink, copy in the same change, defer the rest | do not defer the copy; the tuple is not weakened; beyond-copy doubt-wording edits stay in stage 4 with the reachability check owed (a) C12, (e) 1 | Base (modified); Variant 1 M2; Variant 3 |
| 13 | C13 Review Panel | APPLIED | cut the listed build items | five items built outside the 54-task count; quorum of two only when two or more reviewers launched; parsable-finding behaviour, Q68 log and integrity checks kept; launcher suitability verified; no code written (a) C13, (d) 7 | Base (modified); Variant 2; Variant 3 |
| 14 | C14 open questions | APPLIED | shrink to recommendations | recommendations pending the owner in pending, decided and out-of-v1 sections; OD3 stays open (a) C14, (d) 3, 4 | Base (modified); Variant 3 |
| 15 | Target structure | APPLIED | about 15 tasks in 3 packages | 3 + 2 + 0 + 10 + 4 = 19 tasks in 4 packages; 54 - 35 = 19 (b) Target structure, per-package tables with current task numbers, the rewired dependencies, renumbering note and acceptance lines to drop or rewrite | Base (modified); Variant 2 section 2 item 2 |
| 16 | Order and review | APPLIED | not in V1 | "Trim order and checks" at the end of (b): trim after the four running reviews stop; one mechanical dependency, removed-name and G10 check; one reviewer pass per trimmed package | Variant 2 section 2 item 4 and A-001; Variant 3 missed keep 4 |

Planned: 16. Applied: 16. Not applied: 0.

## Rewiring consequences derived, not decided

The plan removes concepts (registry, skill folder, ledger, shadow stage) that other surviving tasks reference. Where a surviving task text needed an edit only because of a cut, the edit is listed in the (b) tables. Eight points the plan did not settle were not decided; they are listed in (e) items 5 to 12: location of the "kept mechanical gates" list, merge-rule phrase coverage without the allow-list, RT2 and the rate sample, stale spec sections, REQ-01 to bullet mapping, the safety command name and label, the refresh line of the S3 note, and the OD8, OD10, OD13, OD17 citation grep.

## Post-merge validation

1. **Structure.** One H1; five H2 sections (a) to (e) in the lead's order; (b) holds seven H3 subsections (target structure, S0, S1, S2 withdrawn, S3, S4, trim order and checks). No skipped heading level. Every section carries a `<!-- Source: ... -->` tag and the file starts with the provenance comment. No placeholder is left (`grep -c TODO` prints 0). No em dash or en dash in the file.
2. **Task numbers.** A scan of every `S<d> T<n>` citation in `final-cuts.md` against the `## Task N:` headings of the five plans (S0 10, S1 16, S2 8, S3 14, S4 6) found none out of range. Each of the 54 tasks has a fate: S0 keep T1, T4, T9, cut T2, T3, T5 to T8, T10 folded; S1 keep T13 (rebuilt), cut the other 15; S2 keep T3, cut the other 7; S3 keep T5 to T9 and T11 to T14, cut T1 to T4 and T10; S4 keep T1 and T2 (merged), T3, T4, T5, cut T6. Kept tasks: 3 + 1 + 1 + 9 + 1 new + 4 = 19.
3. **Dependency lines in (b).** Every `Depends on` names a task that exists in the trimmed plan and the graph is acyclic: S0 1, 2 (on 1), 3 (on 1, 2); S1 1, 2 (on 1); S3 1, 2, 3 (on 2), 4 and 5 (on 1, 3), 6 (on 2), 7 (on 2, 3, 4, 5), 8 (on 4, 5), 9 (on 3, 4, 5, 6), 10 (on 1 to 9); S4 1, 2 and 3 (on 1), 4 (on 1, 2, 3).
4. **References re-read at merge time:** `tests/skills/test_review_severity_rule.py:170-209` (tuple of ten, `S5_FILES = S1_S3_FILES[:6]` at `:193`); `test_review_severity_mapping.py:23` and `test_review_prompt_overrides.py:24` (both define the `STYLE` path to `pragmatic.md`); spec lines 666, 985, 986, 994, 1011, 1018; the `## Task N:` bodies of S0 T1, T4, T9, T10, S1 T13, S2 T1 to T3, all of S3 and S4; `OPEN-QUESTIONS.md` section 3.4 lines 108 to 114; the four rule-prompt grep. Carried from the variants and the Step 3 judge's spot-check, not re-read: `refs/qa.md:200, :225, :301`; `ledger.py:107-113`; `test_review_severity_rule.py:70, :79-96, :371`; `08-test/results.md:60`; `OPEN-QUESTIONS.md:5, :14, :15, :77, :96`.
5. **Contradiction re-scan against `debate-transcript.md`.** All 14 cut rows (C-001 to C-014), X-001 to X-005 and A-001, A-002, A-004, A-005 match the final text. One tension: the transcript row C-007 reads "cut stage 2 except the shrunk carrier print and tech-research writing its list" (V2's reduced S2 T4), while refactor-plan change 7 reads "cut stage 2 except the shrunk carrier print (C3) and keep one active-flow smoke check". `final-cuts.md` follows the plan, so S2 T4 is cut, and says `notes.md` is also a writer (A-004). If the orchestrator wants S2 T4 kept, S1 would gain a third task and the total would be 20.
6. **Facts corrected in passing.** `final-cuts.md` states that S0 T9's three drafted edits and the three staging decisions are dropped (they describe cut machinery), and that the opening of S1 stays so the old-sentence grep of the original S4 T5 cannot be kept as written; both follow from the plan and are in (b).

## Summary

16 of 16 planned changes applied, 0 not applied, 1 plan versus transcript tension reported (point 5), 8 plan-silent items listed in (e) and not decided.
