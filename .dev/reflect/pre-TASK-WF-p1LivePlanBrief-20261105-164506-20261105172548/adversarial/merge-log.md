# Merge Execution Log

## Metadata
- Base: Variant 1 (reviewer-1 card, analyzer class; `variant-1-original.md`)
- Executor: merge-executor agent
- Changes applied: 11 of 11 planned (`refactor-plan.md`); 3 carry an interpretation, recorded under the change (changes 4, 9 and 11)
- Status: success
- Timestamp: 2026-11-05
- Output: `merged-review-card.md` in this folder
- Rejected changes not applied (as listed in the plan): U-005 (skills install exclusion); V2's "No Regression found"; V3's Drift label for the grant swap (X-002); V1's C-002 "checks conflict at plan:58 and plan:65" as a stand-alone Drift (merged into row 2)

## Changes Applied

### Change 1: Correct C-002 (V1 #2)
- **Status**: Applied
- **Source**: Variant 1 #2 (base), Variant 3 #3 (no-commit rule, plan:24, :52), `invariant-probe.md` INV-001
- **Target**: Base row 2 -> merged row 2
- **Before**: "the tree already had tracked changes (APPROVED.md, plan file); plan:65 tolerates baseline-modified files, so the checks conflict"; MEDIUM
- **After**: the check fails for any uncommitted edit to a tracked file (INV-001); the tree is clean at 0b443745 so it is dormant until the first plan edit; plan:65 does not conflict; fix scoped to `src plugins tests` (alternative: commit before launch, noted as needing the user's request per INV-015); severity kept MEDIUM
- **Provenance tag**: `<!-- Source: Base (Variant 1 #2), modified - change 1 -->` (carried in the per-row comment block under the table)
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅
- **Note**: the plan names the scope as `src plugins tests`; the round 2 advocates and INV-001 also list `.claude/`. The plan's text was applied; the orchestrator may add `.claude/` if wanted.

### Change 2: Raise C-001 evidence (row 1)
- **Status**: Applied
- **Source**: round1 advocates 1 to 3, `round2-advocate-3.md` E1/E2, `round2-advocate-1.md` row 1; Variant 3 #1 (plan:21, :36, :61)
- **Target**: Base row 1 -> merged row 1
- **Before**: Evidence = installer lines only
- **After**: appended "reproduced by three advocates: `cmp` rc=2 on README.md and `__init__.py`; introduced by revision 1 of the plan" with the post-fix-rechecks.md row 2 pointer; Fix column filled with the consensus fix; Finding names the contradiction with source.md:17 and plan:21 and the strictness wording added by revision 1
- **Provenance tag**: `<!-- Source: Base (Variant 1 #1), modified - change 2 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅
- **Note**: `post-fix-rechecks.md` is cited as quoted in round2-advocate-3 E1; it was not re-read for this merge.

### Change 3: C-003 severity LOW, baseline-diff fix (row 7)
- **Status**: Applied
- **Source**: Variant 1 #7 (base), V2/V3 rebuttals, `round2-advocate-1.md` E3, `round2-advocate-3.md` E3, INV-009; Variant 3 #2 (source.md:78)
- **Target**: Base row 7 -> merged row 7
- **Before**: MEDIUM, "cannot hold ... no pre-run baseline is saved"
- **After**: LOW; wording changed to "PASS clause drops the exemption that source.md:78 keeps"; fix = compare `ac13-find.txt` with `git ls-files '*return-contract.yaml'` in the same worktree, or move the exemption into the PASS clause; count corrected to 325 (INV-009)
- **Provenance tag**: `<!-- Source: Base (Variant 1 #7), modified - change 3 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 4: Split C-004 (rows 3 and 4)
- **Status**: Applied (interpretation: the "markers" fix)
- **Source**: Variant 1 #3 and #4 (base), Variant 2 #1 (G1, APPROVED.md:66-71), `round2-advocate-1.md` E1/E4, Variant 3 #5 (consequence note), `base-selection.md` strengths 2 and 9
- **Target**: Base rows 3 and 4 -> merged rows 3 (quoting, Drift LOW) and 4 (swap, Necessary LOW)
- **Before**: #3 Drift MEDIUM with "still reads NOT YET GIVEN is a fuzzy test"; #4 Necessary LOW citing source.md:79 only
- **After**: row 3 is Drift LOW, "fuzzy test" removed, fix "markers" written as: mark the owner sentence, state it replaces `NOT YET GIVEN`, copy only the marked sentence at plan:556; row 4 is Necessary LOW citing APPROVED.md:66-71 (G1), with the consequence link to row 2 and the provenance gap (plan cites only H1 at plan:31)
- **Provenance tag**: `<!-- Source: Base (Variant 1 #3, #4) merged with Variant 2 #1 - change 4 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅
- **Note**: the plan says only "fix: markers"; the expansion follows `base-selection.md` strength 2 (E4 fix) and `round2-advocate-1.md` E4. The consequence note and the plan:31 provenance gap come from base-selection strengths 4 and 9, which the plan lists as merge inputs; they are not separate planned changes.

### Change 5: Demote C-013 to a note
- **Status**: Applied
- **Source**: Variant 1 #8 (base), `round2-advocate-2.md` section 2, `round2-advocate-3.md` section 2
- **Target**: Base row 8 -> Notes section
- **Before**: Drift LOW row #8 (static report covers 7127c247, not the tested tip)
- **After**: removed from the table; kept as a note with the reason (spec line 238 has no "same tree" clause; plan:19 documents the move; Task 1 checks the ancestor)
- **Provenance tag**: `<!-- Source: Variant 1 #8 (C-013, demoted per change 5) ... -->` (section tag of Notes)
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 6: Add U-003 (watcher listing self-match), lc18 only
- **Status**: Applied
- **Source**: Variant 3 advisory 1, `round2-advocate-3.md` E5, INV-010
- **Target**: Base Advisory section, new item 3
- **Before**: Section did not exist in this form (base advisory had 2 items)
- **After**: advisory 3, scoped to lc18 (plan:451, :465; source.md:72); lc08 (plan:227) excluded; fix from `round2-advocate-1.md` E5; LOW-MEDIUM; reproduced by advocates 1 and 3 and the probe
- **Provenance tag**: `<!-- Source: ... Variant 3 advisory 1 and 2 (changes 6 and 7) ... -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 7: Add U-004 (report-path comparison)
- **Status**: Applied
- **Source**: Variant 3 advisory 2, INV-011
- **Target**: Base Advisory section, new item 4
- **Before**: Did not exist
- **After**: advisory 4 with plan:41, :43, :73, the `...//return-contract.yaml` cause and fix `realpath -m`; LOW-MEDIUM
- **Provenance tag**: same Advisory section tag
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 8: Add INV-012 (Task 1 retry creates a second Orca run)
- **Status**: Applied
- **Source**: `invariant-probe.md` INV-012
- **Target**: Base Advisory section, new item 5
- **Before**: Did not exist
- **After**: advisory 5 (MEDIUM) with plan:28, :58; fix worded as "a retry reuses an existing `live-run.json`" (the probe asks for a guard; the exact wording is the executor's reading of it)
- **Provenance tag**: same Advisory section tag
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 9: Add C-009, U-006 and C-010 (as a process note)
- **Status**: Applied (interpretation: placement)
- **Source**: Variant 2 #4 (C-009), Variant 2 #6 (C-010), Variant 2 advisory (U-006), `round2-advocate-2.md` N1, N2, N5
- **Target**: Advisory (U-006) and Notes (C-009, C-010)
- **Before**: Did not exist
- **After**: U-006 is advisory 6 (LOW); C-009 is a note ("no deviation; Necessary if filed") with the plan:49 wording residue; C-010 is a process note with the N2 point (source.md:78 and :87 are uncovered) and the matrix-row remedy
- **Provenance tag**: `<!-- Source: Variant 1 #8 ..., Variant 2 #4 and #6 (C-009 and C-010, change 9) ... -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅
- **Note (decision for the orchestrator)**: the plan's change 9 says "rows 4 to 6 and notes", and change 11 fixes the Necessary count at 3. The base already has 3 Necessary rows (rows 4, 6, 8 of the merged card), so a C-009 row would make Necessary 4 and the total 12, which breaks change 11. C-009 was therefore placed in Notes, which also matches the round 2 position (advocates 2 and 3: "Necessary/no-deviation item"). If a C-009 table row is wanted, the title must read Necessary 4 and 12 deviations.

### Change 10: Add a scope note (not checked)
- **Status**: Applied
- **Source**: Variant 3 notes, `round2-advocate-3.md` E4/E5, INV-005, Variant 1 advisory 1
- **Target**: Notes section, "Not checked"
- **Before**: Did not exist
- **After**: five bullets: `--parent-worktree active` run-time effect; `coordinator_handle` field name; `/sc:implement` behaviour on a failed Task 1 acceptance; the worker argv source for lc18; and the note that the measurements were not re-run for this merge
- **Provenance tag**: Notes section tag
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅
- **Note**: Variant 3's own "not checked" item (install_skills.py:88-98) is the rejected U-005 and was not carried over.

### Change 11: Reclassify with the debate result; counts in the title
- **Status**: Applied (interpretation: the Fix column)
- **Source**: all variants, `base-selection.md`
- **Target**: Title and Class column
- **Before**: "12 deviations (Regression 1, Drift 6, Necessary 3, Authorized 2)"; 6 columns (#, Class, Location, Finding, Evidence, Sev)
- **After**: "11 deviations (Regression 1, Drift 5, Necessary 3, Authorized 2)" with 11 rows; the table gains the Fix column the task asked for (7 columns); where the sources state no fix the cell says so, and "implied" marks the two fixes the executor derived from the finding (rows 5 and 11)
- **Provenance tag**: `<!-- Source: Base (Variant 1 table structure, 11 rows) ... -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: ✅ one H1 (title), H2 `Findings`, `Advisory`, `Notes and not checked`, with H3 `Notes` and `Not checked` under the last; no skipped levels (checked with a heading grep).
- Section ordering: ✅ path key, findings table, per-row origin comment, advisory, notes and not checked.
- Document flow: ✅ the table has 13 lines (header, separator, 11 rows), every line with 7 columns (pipe count checked); class tally from the rows is Regression 1, Drift 5, Necessary 3, Authorized 2 = 11, equal to the title. The provenance header (three comment lines) is at the top; 4 section-level `<!-- Source: ... -->` tags plus one per-row origin comment block.

### Internal References
- Total references: 7 (three to row 2: from row 4, advisory 5 and Not checked; "rows 7 and 1" from the C-010 note; advisory 5 and advisory 1 named from Not checked)
- Resolved: 7
- Broken: 0
- External citations (plan, source.md, spec, installer, APPROVED.md, p0-live-orca-help.txt, post-fix-rechecks.md, coverage-matrix.yaml) were copied from the source cards, rebuttals and probe; none was added by the executor, and the file:line evidence of every source row is kept. Rows with no source fix say "Not stated in the sources".

### Contradiction Re-Scan
- New contradictions introduced: 0
- Details: row 1 says the strict wording was added by revision 1 while also saying source.md:87 says "every file under"; both hold (inherited wording, sharpened by revision 1), as `round2-advocate-3.md` E2 states. Row 4 (Necessary) and the Drift-excluded reading agree with the plan's rejected-change list. Row 2 no longer says the plan:58 and plan:65 checks conflict, and row 7 no longer says "cannot hold" as MEDIUM; both stale claims were removed. The title counts, the row classes and the Notes (C-013, C-009, C-010 outside the table) agree.
- Left open, outside the plan (not applied): INV-014 (plan:19 "revised once" goes stale after a second fix pass, and post-fix-rechecks.md row 2 gives "spec says every file" as its reason, which round2-advocate-3 E1 says the spec does not say) and the shared assumptions A-001 to A-004 of `diff-analysis.md`. Neither is in the 11 planned changes.

## Summary
- Total changes planned: 11
- Successfully applied: 11
- Failed: 0
- Skipped: 0 (4 rejected changes were not applied, as the plan directs)
- Interpretations to confirm: scope list for the row 2 fix (plan says `src plugins tests`; the advocates also list `.claude/`); the "markers" fix wording (row 3); C-009 placed in Notes to keep Necessary at 3 (change 9 against change 11)
- Post-merge validation: PASS
