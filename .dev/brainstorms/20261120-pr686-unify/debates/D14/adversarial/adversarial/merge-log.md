# Merge Log: D14 merged disposition

## Metadata

- Merge date: 2026-11-20 (UTC)
- Executor: merge-executor (Step 5 of the adversarial pipeline for debate D14)
- Base variant: Variant 1 (OURS), `ADV/variant-1-original.md`. Non-base: Variant 2 (CLAY), `ADV/variant-2-original.md`.
- Plan executed: `ADV/refactor-plan.md` (9 planned changes, 6 rejected alternatives, auto-approved, `--unattended`).
- Merged output: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D14/adversarial/merged-output.md` (11 sections, about 300 lines).
- ADV = `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D14/adversarial/adversarial/`.
- Nature of the merge: the plan says the merged output is a decision document built from the base paper's claim and facts plus the changes, not an edited copy of the OURS paper. The base's section set (Claim, Mechanism, Cited facts, Gets right, Costs, Risks) was therefore replaced by the eleven sections the task named; the base's facts and risks are carried into sections 2, 3, 9 and 11.
- Sources read: base variant, refactor plan, ROU and RCL (round 2), round 1 OURS and CLAY, `invariant-probe.md`, `diff-analysis.md`, `debate-transcript.md`, `base-selection.md`, the Actions tables of verdicts D01 to D13, and `inventory/clay-prs.md` (tables 2A to 2C and section 6).
- Nothing was written outside the two named files. No GitHub, Orca or git action was carried out.

## Changes Applied

### Change 1: Replace the claim of the base. APPLIED
- Before: "revert PR 682 first as a new PR; do not merge PR 686 as it stands, split it and close the original once the pieces are re-filed; keep 681 stamped, 683, 684, 690 with adaptations; keep 450, rescope 655."
- After (section 2): revert conditional on the owner's chat go; PR 686 not merged as it stands, adapted in place as a draft after planb lands; two lanes plus a hold step; the flip condition (Q1 "only the start gate").
- Provenance: `<!-- Source: Base modified ... ROU section 2 R-1 to R-3, RCL section 2 -->` on section 2.

### Change 2: Replace "split and close" by "adapt in place, keep open". APPLIED
- Before: split into additive pieces, re-file, close the original.
- After (section 3 row PR 686; section 9 CLAY point 2; section 10 row 3): REBASE-AND-ADAPT in place as a draft; evidence is the import check (10 of 13 `predicates` names missing on master; `hold.py`, `route.py`, `wake.py`, `repos.py` each need schema-2 `record.py` or other PR 686-only code), no verdict says CLOSE, CLAY round 1 strength 4. The split is kept in section 10 as a rejected alternative.
- Provenance: ROU R-2 and CLAY round 1 strength 4, tagged on sections 2, 3 and 10.

### Change 3: Add the per-item disposition table. APPLIED
- Before: base had a claim sentence naming the items, no table.
- After (section 3): 16 rows covering PR 686; PR 690 with branch `issue-655-pr-p`; issue 687 (marked an issue); issue 689 (marked an issue); PR 681; PR 682; PR 683; PR 684; issue 655; issue 450; PR 693; PR 685; contract and guard amendment PR (new); design amendment PR (new); the eight removal PRs; every other Clay PR (one KEEP row). Dispositions match the plan: 693 MERGE first; 690 REBASE-AND-ADAPT lane 1; 682 REVERT (recommendation only); 681 KEEP with banner, same-PR correction and later amendment; 686 REBASE-AND-ADAPT in place, draft; 683 KEEP; 684 KEEP-ADAPT; 685 KEEP and merge; 687 KEEP-ADAPT; 689 SPLIT and DEFER; 655 KEEP and RESCOPE; 450 KEEP open and answered; the eight KEEP.
- Note: the plan folds "a later owner-reviewed amendment PR" into the 681 row; the task asked for a separate row for the design amendment PR, so both exist and agree.
- Provenance: `<!-- Source: Variant 2 / ROU section 4 and RCL section 4 ... -->` on section 3.

### Change 4: Add the three-lane ordered operations list and the invariant fixes. APPLIED
- Before: no ordered list in the base.
- After (section 4): hold step H0; lane 1 (L1.1 to L1.3); lane 2 (L2.1 to L2.9); lane 3 pointer to section 8; a table mapping each INV to the step that handles it; a "figures corrected" list. Every step has "needs" and a pass check.
- Invariant fixes placed: INV-006 and INV-026 in H0; INV-018 in L2.9; INV-027 in L2.2, L2.3 and L2.5 (no PR B or PR E before the amendment); INV-005 in L2.1; INV-007 in section 5 check 3; INV-002 in L2.6; INV-019 and INV-020 in L2.4, L2.6 and Q4; INV-003 in L2.9; INV-009 in the "go" definition (section 1) and H0 limits; INV-010 and INV-011 as corrected counts; INV-008, 017, 028 as conditions or Unresolved items.
- Source conflicts settled (also listed in the output's "Figures corrected" subsection): planb entries 225 (ROU) vs 348 today (INV-010), use 348 with 69 code, tests and docs; planb overlap with PR 686 22 (RCL) vs 23 (INV-011), use 23; PR 693 and PR 690 shared files "three text files" (task wording) vs four (INV-016, ROU R-1), use four; "29 test modules" is import-crash fallout, not a file list (INV-012).
- Provenance: `<!-- Source: Variant 2 and base merged ... -->` on section 4.

### Change 5: Add the owner question list. APPLIED
- Before: base had no questions (all decisions "in chat").
- After (section 6): Q1 both gates stay; Q2 who adapts; Q3 hold plus ruleset on `master`; Q4 push planb as a draft and land it first (with the priced reversal); non-blocking NB-1 (eight removal PRs, blocks only L2.9) and NB-2 (reply to Clay on issue 450). One line per answer saying what it would do. ROU's Q5 is recorded as answered by the owner's order of 2026-11-17, pending Q01. ROU's Q3 (stamp the design doc) became a fact per RCL, so Q3 here is the hold and ruleset question, as the plan names it.
- Provenance: `<!-- Source: Variant 2 / ROU section 6 corrected by RCL section 4 ... -->` on section 6.

### Change 6: Add the cross-verdict tensions table. APPLIED (with two extra rows, see Summary)
- After (section 7): D03 vs D05; D03 vs D04; D01 vs D03; D07 vs D04, D06, D11; D09 vs PR 686; D12 vs D13 vs PR 693; D06 amendments at `WORKER-CONTRACT.md` lines 70 and 245; D08 renames before any 686 edit; D10 M1 as Rule A and Rule B plus the M2 fix.
- Added beyond the plan list: two "checked, no tension" rows from INV-022 and INV-023 (D08 rename vs D01 restore; restored verbs vs `record.py` schema 2). They are from a source the plan names; the orchestrator may delete them.
- Provenance: `<!-- Source: Variant 2 / round1 OURS T1 to T4, ROU R-2, R-4, R-5 ... -->` on section 7.

### Change 7: Add "verdict actions not in the order" as lane 3. APPLIED (with extra rows, see Summary)
- After (section 8): a table "verdict action | after | independent" with the plan's groups: D11 (contract note, two HIGH report rules, `session_id`); D05 (PR 685, staging probe, issue 442 rows); D10 (U5 spike, Coder 477 reply, typed line); D02 (five-field cron, Coder 515 wording, poll command contract, token rotation); D07 (design sections 4.4, 5.7, 6.2, cap, `owner/name` keys, Coder 515 and 516); D08 (glossary and renames); D13 (cleanup design approval, `git branch -d` ruling, issue 339); D12 (manual-claim warning); D06 (R25, R17, R9).
- Added beyond the plan list: D04 (grants file reach, `answer-check` identity, R10), D09 (dormant label code), D03 (R33 before R18) and D01 (MR-1, MR-2, trigger-sentence supersede) rows, taken from the verdict Actions tables and the probe's "no consensus step carries" list. D04 and D05's server-side rule are named in that probe list.
- Provenance: `<!-- Source: Variant 2 / RCL section 3 item 6 and section 4 ... -->` on section 8.

### Change 8: Add "disposition of other Clay PRs". APPLIED
- After (section 3, last two rows): the eight confirm-approval PRs KEEP (non-blocking question NB-1); every other PR in tables 2A to 2C as one KEEP row. Count by `grep` of table rows: table 2A has 9 rows (minus PR 686, 690, 684, 683, 682, 681 leaves 3), table 2B has 27 rows (minus the eight leaves 19), table 2C has 9 rows: 31 PRs. PR 682 REVERT and PRs 681 and 686 per their own rows.
- Provenance: tagged on section 3.

### Change 9: Add Unresolved and Unverified. APPLIED
- After (section 11): the plan's items (planb order if slow; resent-wake double delivery; dormant label writer; typed wake line; how Coder's template updates reach hosts; red CI on an unprotected `master`; the revert tree's full test run), plus INV-028 (contract, guard and hosts agree only on paper), the not-run merge trial, the process-independence note, and confidence (about 80 percent; 21 of 21 positions agreed, status partial because of 4 HIGH invariants; what would raise or lower it).
- Provenance: `<!-- Source: Variant 2 and base ... -->` on section 11.

### Changes NOT being made (the plan's rejected list). APPLIED as section 10
- All six alternatives appear with their reasons: merge 686 as is; keep 682; split and close; serial order; close 450 into 655; revert 681.
- Added: banner alone, a date for the planb order, a blanket `superclaude install`, the 10-name check, and reverting the eight removal PRs. Each comes from a named source (INV-027, ROU R-3 vs RCL R-3, INV-018, INV-007, RCL section 3 item 1).

## Post-Merge Validation

### Structural integrity: PASS
- One H1 (the title, line 2). Sections 1 to 11 are H2, in the required order. H3 appears only under sections 4, 9 and 11 and never skips a level (no H4). Verified with `grep -n -E '^#+ '`.
- Every section carries a `<!-- Source: ... -->` tag; the document has a header comment naming base Variant 1 and the merge date.
- Tables: all rows have the same number of cells as their header (no unescaped pipes inside cells).

### Internal references: PASS (after fixes)
- Section references inside the output: "section 1" (terms and "go"), "section 5" (merge checks), "section 8" (lane 3 table), "sections 3 and 4", "section 4 step L2.9" all resolve to existing sections. References such as "FULL-REPORT section 5", "inventory section 6" and "RCL section 3" point to outside files, not to the output.
- Step IDs H0, L1.1 to L1.3 and L2.1 to L2.9 are each defined once in section 4 and used consistently in sections 3, 6, 7 and 8. Questions Q1 to Q4, NB-1, NB-2 and the recorded-as-answered Q5 are defined in section 6.
- Fixed during validation: terms used before definition (ROU, RCL, ADV, R-1 to R-5, PR B and PR E, row labels, Q01) were added to section 1; two origin cells in section 10 that named "base paper" for ideas that came from ROU or CLAY were corrected.

### Contradiction re-scan: 5 items found, all fixed in the output
1. Section 3, PR 682 row, first draft said the code the verdicts keep imports names that PR 682's "sibling" PR 686 deletes (muddled actor, and the 3-day-old PRs 584 and 591 read as if merged by 682). Reworded to say what PR 682 deleted and what PR 686 deletes.
2. Section 6, Q3: "blocks every step that lists H0" would stall lane 1 if the owner answers "No to both", which contradicts the "No to both" answer line. Reworded so steps may proceed with the stated risk.
3. Section 8, the "Independent" column mixed "yes of 686", "no of L2.5" and plain yes or no. Normalised to "yes of PR 686; needs L1.3" style or plain yes or no.
4. Section 3 used the label "NEW PR" for two rows, which is not one of the eight labels the task allows. A note under the table now says so; the plan itself uses "NEW PR". Separately, INV-027 says a banner alone is not enough, so the 681 row, section 4 and section 10 all require the same-PR correction and the later amendment PR.
5. Source figures conflicted (225 vs 348 planb entries; 22 vs 23 overlap; three vs four shared text files). The output uses the probe's corrected figure and notes the change in section 4 "Figures corrected in this merge".
- Open checks: no sentence in either file states that an action (merge, revert, post, push, hold) was carried out; every disposition and step is written as a recommendation. A grep of both files for em dashes, en dashes and unfinished-text markers (the usual to-do words and the build marker used while writing) found none in the merged output; the 16 disposition rows and 11 source tags were counted; a column-count check on every table in the merged output reported no mismatch.

## Summary

- Planned changes: 9, plus the "Changes NOT being made" list (6 items).
- Applied: 9 of 9 (changes 1 to 9), and the rejected list applied as section 10 (6 of 6). Partially applied: 0. Skipped: 0.
- Additions beyond the plan text, all from sources the plan names and each flagged above for the orchestrator to keep or delete: 2 extra rows in the tensions table (INV-022, INV-023); 4 extra rows in the lane 3 table (D04, D09, D03, D01); 5 extra entries in the rejected list; a "Where each invariant is handled" table and a "Figures corrected" list in section 4; a "recorded as answered" note for Q5.
- Items marked UNVERIFIED are carried from the sources and listed in section 11 of the output.
- Escalations to the orchestrator: none required; every planned change could be applied.
