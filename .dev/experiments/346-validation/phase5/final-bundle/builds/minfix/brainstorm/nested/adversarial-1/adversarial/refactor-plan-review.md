# Refactor plan review

Verdict: FAIL (7 blocking issues, 10 minor notes)

Citation key: `P:n` = line n of `refactor-plan.md`; `A:n`, `B:n`, `C:n` = lines of the variant files as they are now (unmodified); `IP:n` = `invariant-probe.md`; `DT:n` = `debate-transcript.md`; `BS:n` = `base-selection.md`; `SP:n` = `src/superclaude/commands/spec-panel.md`. File content was read as data.

## Blocking issues

### PR-B1 Exit-code actions conflict between Changes 4, 13 and 21
- **Changes affected**: 4, 13, 21 (all three rewrite B:160 and brief step 4, B:288).
- **Evidence**:
  - P:107 (Change 4) says the reviser runs `check`, cuts down once, runs `check`, and "if still not 0, `check --enforce`".
  - P:243 (Change 21) says exits 3, 4, 5 and 70 mean "reviser edits nothing further and pastes the output".
  - Both cannot hold for a second `check` that returns 3, 4, 5 or 70. A's own trigger is exit 2 only (A:62 "if it still exits 2"), and A:108-110 stops on input errors.
  - P:179 (Change 13) folds B's exit 3 "ledger incomplete" into exit 1. B:160 and B:205 told the reviser to "add the missing entry" or "the entry or the deferral" for that case.
  - P:243 gives exit 1 only the action "cuts the named entries". A cut-down cannot repair a missing ledger entry, so `--enforce` would revert a valid fix that was merely unattributed. That is a wrong outcome.
- **Correction**: Replace the reviser sequence in Change 4 and Change 21 with one text. "Run `check`. On exit 1: cut the named entries down or add the missing entry or `## deferred` line, once, and run `check` again; if the second run still exits 1, run `check --enforce`. On exit 2: correct the call once and re-run; nothing is counted. On 3, 4, 5 or 70, at any run: edit nothing further and paste the output (Change 22 then applies)." Say that `--enforce` runs only after a second exit 1. Make P:107 and P:243 match this wording.

### PR-B2 Change 18 does not resolve INV-001; its key claim is unsupported and the working fallback is deleted
- **Changes affected**: 18, 4 (removes `snapshot`), 9, 15, 22; the Overview and Review Status claims.
- **Evidence**:
  - P:219 says "The baseline is the saved copy 427 already keeps ... the Reviser brief names its path". The Reviser brief is written by the reviewer inside its report (SP:263). The reviewer is given no saved-copy path: SP:261 says the coordinator keeps it, and only the next review gets `--baseline <saved copy>`.
  - DT:789 (the analyst's own evidence) says "T06 and T08 do not name the path, so the reviser still cannot find it without a brief change; I keep `snapshot` as the fallback".
  - P:147 (Change 9) and A:37 forbid a brief change by the coordinator. So the stated source of the path does not exist, and P:219 deletes `snapshot`, the fallback the debate kept.
  - P:221 admits the gap only as a residual "pilot must check".
  - P:16 admits that without a working baseline every loop whose reviser obeys T08 stops at review 2.
- **Correction**: In Change 18, remove the unconditional sentence "the Reviser brief names its path".
  - Replace it with: "Baseline: the saved copy, when the review brief supplies its path (not true of T05/T07/T09 today, DT:789); otherwise Reviser brief step 1 runs `snapshot`, which writes only `<report dir>/.fixcheck/base-<N>.md` and refuses a changed spec (exit 4)."
  - Keep `snapshot` in the subcommand list of Change 4 as that named fallback.
  - Restore B:440's wording "none authored by the model; `.fixcheck/` is script output" in the 7.1 cost row.
  - Change 18 Risk becomes High. Add to the Review Status note that INV-001 is mitigated, not closed, until the one-replicate pilot shows either that a path can be named or that a T08-obeying reviser runs the script. Say that Change 22 turns a failed pilot into a justified escalation, not a silent stop.

### PR-B3 Change 10 carries stale A-only references and A's exit meanings
- **Changes affected**: 10, 13, 18.
- **Evidence**:
  - P:155 keeps A's "Not a test of the idea (re-run instead)" line and replaces only A's 16% ceiling.
  - A:330 reads "V-M1 to V-M3 fail, the checker exits 3 or 1 in any cycle, or growth exceeds the 16% ceiling while the checker reports `pass`".
  - V-M1 to V-M3 (A:308) are defined only in A and test `reviewed-copy:`, `fix-budget:` and `check:` lines and a `fixcheck.json` file. None of these exist in the merged design (Changes 5, 18). B's validity set is V1-V7.
  - A's "exit 3 or 1" means input error or crash (A:105-110). Under Change 13, exit 1 is the normal "over budget" policy failure, so the line would void almost every replicate.
- **Correction**: In Change 10 write the line as "Not a test of the idea (re-run instead): any of V1-V7 fails (V7 as restated by Change 18), the checker exits 3, 4, 5 or 70 in any cycle, or net growth exceeds Change 12's bound (14.7% words, 21.3% bytes) while the checker reports exit 0 (a checker bug)." State that A's V-M1 to V-M3 are not carried.

### PR-B4 Removal lists for receipt, `snapshot`, `verify`, `large` and the 10% cap are incomplete; the merged text would describe deleted mechanisms
- **Changes affected**: 18, 8, 5, 12 (and 9 for B:102).
- **Evidence**: Changes 8 and 18 delete the receipt, `.fixcheck/`, `snapshot` and `verify`. Change 5 deletes the `large` flag. Change 12 deletes `CYCLE-GROWTH`. A grep of the base (`receipt|\.fixcheck|snapshot|verify|large|10%`, lines at or after 100) finds these uncovered sites in the unmodified base:
  - receipt: B:102 ("The reviser snapshots the spec ... The script leaves a receipt; the next review verifies the receipt"), B:214 ("from the receipts"), B:316 (`check` "builds the report and the receipt"), B:322 ("the receipt carries no timestamp"), B:338, B:428, B:439, B:449, B:455 ("from the receipt's line map"), B:462, B:477.
  - `large`: B:123 (example block row `F3 | MAJOR | blocking | large`), B:281 (`std|large|-`), B:314 (`large_flags`), B:391 ("the ten percent per cycle cap and the `large` flags").
  - Change 9 appends to B:102 but leaves that false first-paragraph description in place. Change 20 and Change 22 touch B:214 but only append, so "from the receipts" stays.
  - B:383 loses its sources: the pasted "last `FIXCHECK` line" is only `FIXCHECK exit=<n>` (B:193). The ids `--enforce` reverted, the "escalated" needs and "hunks unattributed before enforce" are not in it.
- **Correction**: Add to Change 18 a sweep step like Change 30's.
  - After the merge, `grep -n -i 'receipt\|\.fixcheck\|snapshot\|verify\|large\|CYCLE-GROWTH\|ten percent'` over the merged file must return only lines that say the item is removed (or the `snapshot` fallback of PR-B2).
  - List the lines above as targets.
  - Rewrite B:214 to source the escalated-for-budget list "from the disposition file's `## deferred` lines and the pasted `--enforce` output".
  - Change the paste rule (B:161, brief step 5) to "paste the `result:`, `escalated:` and last `FIXCHECK` lines of the final run, and of the first run when it was not exit 0". Otherwise drop "hunks unattributed before enforce" from the B:383 metrics.

### PR-B5 Change 6 leaves test M2 unchanged although it changes bullet 6
- **Changes affected**: 6 (and 28, 29, which rewrite M2).
- **Evidence**:
  - B:331 (M2) says that after removing the frontmatter, the name substitution, bullet 8 and the `## Fix Budget` section, the file equals `spec-panel.md` line for line.
  - Change 6 (P:121, P:123) deletes bullet 8 and edits bullet 6 (id clause removed, one clause appended). Its target list names B:332 (M3) but not B:331 (M2).
  - As written, M2 fails on bullet 6. Changes 28 and 29 do list M2 and exclude their own lines, so the exclusion list is half-updated.
- **Correction**: Add B:331 to the Change 6 targets. M2 must exclude bullet 6 (compared by M3) instead of "bullet 8", and also the Usage line change (Change 29), the template-lookup line (Change 28) and the `## Unattended mode` section. Merge the three M2 edits into one sentence.

### PR-B6 Change 32's cascade reverts single entries, which recreates the half-fix that B:211 forbids
- **Changes affected**: 32 (with 4 and 23, which describe `--enforce`).
- **Evidence**: P:331 says "reverts every entry that depends on one of that finding's entries". B:211 states the invariant "a failing finding is reverted whole (all its hunks, so no half-fix remains)". Reverting one entry of finding F11 while keeping F11's other entries leaves a half-applied F11. The agreed amendment (DT:683, DT:852) is a coupled revert so that linked changes are "kept or dropped together".
- **Correction**: Change 32 integration point should read: "When `--enforce` reverts a finding, it also reverts, whole, every finding that owns an entry that `depends:` on one of the reverted finding's entries. Each such finding is listed `escalated` with its gross as the need." Test 14's dependent entry must assert that the owning finding's other entries are reverted too.

### PR-B7 Risk 1 is rejected against an explicit "must also fix" in the base selection
- **Changes affected**: none planned (missing change); the "Changes NOT Being Made" row at P:418.
- **Evidence**:
  - BS:289 lists, under "Base-specific defects the merge must also fix": "give each listed risk a probability (Risk 1)". Clarity 4 from the same sentence is done (Change 35).
  - P:418 rejects Risk 1 because "no measured probabilities exist; invented values would add unsupported text".
  - The debate already accepts labelled judgment for the forecast ("labelled judgment", DT:724). BS:126 shows that even one likelihood word without impact was rated NOT MET for A.
- **Correction**: Add a Change 37, or extend Change 35. Add a `likelihood / impact` pair (low, medium or high) to each row of the risk table in 7.2, labelled "judgment, UNVERIFIED", with one phrase of the reason taken from the row's existing "why" cell. Delete the P:418 row. If the owner wants to keep the rejection, the plan must say it overrides BS:289 and name the owner decision. A silent departure is not acceptable.

## Minor notes

- **PR-M1** Change 25 (P:275) keeps "the mean is about 3.0". The analyst withdrew the point forecast: DT:705 "The central 3.0 should not stand as a point forecast", DT:724 "central 3.3, band 1.1 to 5.6", DT:778 "a stated range ... not 2.5, 3.0 or 1.0". Write the range and, optionally, "central 3.3 (judgment)", and keep the arithmetic 3.0 only as "at R1 = 12".
- **PR-M2** Change 6 (P:123) leaves A's amendments to bullets 2 and 5 (A:163) unused without a stated reason. Add one sentence: the class lives in the `fixbudget` block (C-001) and the re-review duty in `## Fix Budget` (B:281).
- **PR-M3** Change 6 appends "the reviser follows `## Fix Budget`", but SP:263 says the reviser reads the report, not the command. Say "the Reviser brief carries the Fix Budget steps".
- **PR-M4** The minor-budget sweep (Changes 3 and 30) misses B:98 ("Minor cap 12: 17 of 17 ... over") and B:188 (example row "OVER minor budget (gross 56>12, net 56>0)"). Add both, or the Change 30 post-merge check ("no text gives the minor budget as 12") fails.
- **PR-M5** Deleting open question 6 (B:476) renumbers questions 7 to 11. B:471 says "(question 9)", and Change 36 and P:123 cite questions by number. Keep a "6. (removed)" placeholder, or renumber and update every cross-reference.
- **PR-M6** Change 28 applies the template-lookup edit to the experiment file too, which is a second change against X-014 (95%) and C-023 and the one-change-at-a-time rule (B:362). A reason is given (Completeness 1), so this is not blocking. Consider limiting the edit to the repository file, since S1 does not exercise the line (the plan marks this UNVERIFIED).
- **PR-M7** Change 35 cites "IP:20" for the FR-8/FR-9 gloss. IP:20 is INV-013 (words vs bytes). The FR-8/FR-9 text is in IP:12 and IP:30.
- **PR-M8** Change 12 calls B:184 "the report header". The `FIXCHECK cycle=...` header is B:183, and B:184 is the `hunks=...` line.
- **PR-M9** Change 22 covers a re-review stop and a pasted exit 3, 4, 5 or 70. The `E-FIXCHECK-MISSING` stop (B:106, kept by Change 15) happens before review 1 and is neither PASS nor escalation. Add "stop with `E-FIXCHECK-MISSING`, which is an install error reported to the owner, not a loop state".
- **PR-M10** The report-format `GRADE-CONFLICT` token (Change 20) is not added to the exit-code or report examples (B:182-194). Add it to the example so the format is testable.

## Self-Audit

**Check 1: diff points B lost.**
- Counted from the Scoring Matrix (DT:1012-1068): A wins 18 (S-004, S-005, C-004, C-011, C-014, C-016, C-017, C-018, C-022, C-026, C-028, X-001, X-002, X-003, X-006, X-012, X-013, A-003); C wins 7 (C-005, C-012, C-015, C-019, C-020, X-004, X-007). The totals match DT:1070.
- Every one maps to a Change through the Coverage map and the Change rationale lines (P:20-57): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16.
- The B-won points (28) match the 28 rows at P:381-408; the other 10 rows are L1, probe and rubric items, 38 in all.
- Contradictions of a winner, each with a stated reason:
  - C-015 (Change 20, INV-005)
  - C-009 mechanism (Change 18, INV-001; reason unsound, see PR-B2)
  - X-014 and C-023 (Change 28; PR-M6)
  - C-024 point forecast (Change 25; PR-M1)
  - C-016 bullets 2 and 5 (no stated reason; PR-M2)
- Contradiction of the base selection's "must also fix": Risk 1 (PR-B7).

**Check 2: the ten HIGH invariants.**

| Invariant | Result |
|---|---|
| INV-001 | Not resolved (PR-B2) |
| INV-002 | Change 19 resolves it; completeness rule B:159 then covers carried ids |
| INV-005 | Change 20 resolves it |
| INV-006 | Resolved in intent by Change 21; action text conflicts with Change 4 and loses the "add the missing entry" action (PR-B1) |
| INV-007 | Changes 15 and 22 resolve it; small gap PR-M9 |
| INV-012 | Change 23 resolves it |
| INV-023 | Change 24 plus Change 26 resolve it |
| INV-026 | Change 25 resolves it as a claim change plus a metric; PR-M1 on the point forecast |
| INV-027 | Change 26 resolves it (`where`, `when`, `if`, `unless`, `whenever`, `except`, `otherwise`) |
| INV-028 | Change 27 resolves it as a measurement |

The three departures from the probe's suggestions:
- **INV-005, warning not reclassification: sound.**
  - It removes the unrepairable stop.
  - It avoids the F22 to N5 to N12 chain (B:44-50 verified; B:45 says N12 was review 3's only blocking finding).
  - The grade stays with the reviewer, and the unfixed GAP is an owner question already stated at B:481.
  - Residual: a CRITICAL graded minor also only warns.
- **INV-012, largest-first within a class: sound.**
  - For a fixed word total, reverting the largest findings first reverts the fewest findings, and each reverted finding is a carried blocker.
  - The class order (blocking MAJOR before CRITICAL) matches the concession at DT:731 and DT:841.
  - The probe's "smallest first" would revert more findings.
- **INV-028, rate from the pilot: sound.**
  - Recorded loops had no checker and so no cut-down attempts; the harness can only give the over-cap denominator (B:98, B:94 verified).
  - The decision rule is Change 10's carried-count falsifier (A:326).

**Check 3: conflicts between changes.**
- Found PR-B1 (4, 13, 21), PR-B3 (10 against 13 and 18), PR-B5 (6 against M2) and PR-B6 (32 against B:211).
- Verified consistent:
  - override owner (the reviewer in Changes 5, 13 and 24; `override` and `gap:<n>` exclusive)
  - exit 4 means hash conflict everywhere it appears (Changes 13, 18, 21)
  - `deferred (minor, fixcheck budget 0)` (Changes 3 and 30)
  - the Change 33 cross-check reads the Reviser brief from `--report`, which is where SP:263 puts it
- Several changes edit B:128, B:160 and B:288. The executor must merge them into single sentences; the application order at P:16 is adequate except for the missing PR-B1 reconciliation.

**Check 4: facts about repo files, verified by reading.**
- SP:258-263 (Review Loop bullets 1-6), SP:220 (src path), SP:451 (`## Unattended mode`) and SP:313-329 (guard table, FR-8/FR-9) are as the plan states them.
- Line 218 of `plugins/superclaude/commands/spec-panel.md` holds the same src-path lookup.
- `tests/skills/test_worker_contract.py:831-839` is `_check_no_unattended_sections`. It globs `COMMANDS_DIR/*.md` (line 20, `src/superclaude/commands`) and asserts the exact set. So a new command file with the section would fail, and Change 29 is right.
- `tests/skills/test_spec_panel_review_loop.py` pins `spec-panel.md` (src and plugins) only: seven bullets at line 83, `Reviser brief` and `byte size before and after` at lines 101-102. It does not pin the minfix file, so M3 is the plan's own pin.
- `tests/skills/test_review_severity_rule.py` scans `src`, `plugins`, `commands`, `agents` and `skills` trees (lines 28, 174), so A:252 is true and the Change 6 risk note is right.
- The base line numbers in Changes 1-36 (B:100-214, 235-342, the table rows, the sites in the minor sweep, the open questions B:469-481, the risk rows B:446-456) were checked against the base. All matched except those noted in PR-B4, PR-M4 and PR-M8.
- The A and C citations (A:37, A:50, A:62, A:64-68, A:75-80, A:161-163, A:177-180, A:256-262, A:305, A:324-330; C:53, C:62, C:126, C:160, C:259-267, C:289, C:317) are true. A:80's condition-word list and the class limits (C 2, B 1) are true.
- The probe line numbers IP:8-16, IP:19, IP:30, IP:33-35 and IP:50-59 are true, except PR-M7.
- Arithmetic checked: 1,200 / 8,148 = 14.7%; 12,288 / 57,763 = 21.3%.
- Not verifiable here: citations into the experiment worktrees (`D2:61`, `R1:63`, `tR3:*`, `r2B:35`), taken from the probe and debate as given.

**Check 5: theme discipline.**
- Every added mechanism traces to a diff point or an invariant: `gap:<n>` (INV-023), `GRADE-CONFLICT` (INV-005), carried-id clause (INV-002), `depends:` (A-002 amendment), the brief-id cross-check (INV-009, MEDIUM, the plan chose to address it), the rename sentence (INV-015) and the definitions line (rubric Clarity 4).
- No change adds a mechanism that nothing calls for.
- The rejected Risk 1 is a requirement the plan skipped, not one it added (PR-B7).
- Net effect on text size matches the Overview's "adding less text".

**Not done:** no edits to the plan, no git, no network. The plan was read in 120-line pieces; the base was read in its full span from line 96 to 482.
