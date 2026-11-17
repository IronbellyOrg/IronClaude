# Merge Log

- Base: variant 1 (`variant-1-original.md`, reviewer 1, analyzer, sonnet class)
- Plan: `refactor-plan.md` (PC-01 to PC-10, auto-approved)
- Output: `../merged-review-card.md` (path relative to this folder)
- Merge date: 2026-11-16T19:44Z
- Executor: merge-executor (opus class)

## Applied changes

### PC-01 (Medium risk): replace the C-001 repair

- Source: base R1-F1 (claim, consequence kept); variant 3 R3-F4 (REQ-02 citation); invariant probe INV-001, INV-002.
- Before: repair `CRITICAL=Blocking; IMPORTANT=Medium; MINOR=Note` in Task 3, a `model` cell calling these the default tier for a non-blocking row, an acceptance line, and a stage 2 note that a Blocking row is never written.
- After: N-F1 carries a "why three fixed values do not repair it" block (two readers of one cell; rf-qa.md line 111; the effect of `IMPORTANT=Blocking`, `IMPORTANT=Medium` and `MINOR=Note`), and the repair is one owner decision in two forms: form 1 `CRITICAL=Blocking;IMPORTANT=Blocking;MINOR=Medium` plus a stage 2 note that the importer takes blocking or non-blocking from the reviewer's own call and uses the cell only to split non-blocking rows into Medium and Note; form 2 a second column. Acceptance line in either form. Grade stays blocking; closest-call status (55, 76, 65 percent; third review) stated.
- Status: applied.
- Observation for the orchestrator (no change made): under form 1 no lens-scale label maps to Note and IMPORTANT maps to Blocking, so for a non-blocking IMPORTANT row "the cell only splits non-blocking rows into Medium and Note" gives no Medium-or-Note value. The plan text was applied as written; the owner's choice of form, or the stage 2 note's wording, has to settle that case.

### PC-02: family key versus `origin` (C-002)

- Source: variant 3 R3-F3 (mechanism, repair), variant 2 R2-F1 (same gap), base R1-F4 (Task 12 names no key source).
- Before: base had only R1-F4's line that the family key is among Task 12's missing inputs; no finding on `origin`.
- After: N-F2, non-blocking (2 of 3 advocates), with variant 3's repair (a `reviewers` column; resolution from the reviewing agent in `source`; a Task 11 case for an unmatched origin) and a pointer to N-F6 for the Task 12 inputs. The non-blocking reason cites STAGE2:28 and STAGE2:135 (from the debate scoring matrix, re-read).
- Status: applied. Variant 2's blocking grade and its integration-fixture repair were not carried (refactor plan: "Changes NOT Being Made").

### PC-03: `unsettled` tag unowned (C-003, INV-004)

- Source: variant 2 R2-F2; invariant probe INV-004.
- Before: absent from the base.
- After: N-F3, non-blocking, with the repair "Task 12 adds `unsettled` through the sole writer without clearing tags, or the stage 2 revision owns it", stated as a note with no owner today.
- Status: applied. The grep claim was re-run over `TASK-WF-blockerStage*` plans: one hit, PLAN:87.

### PC-07: consent and offer logic (C-005, INV-003)

- Source: base R1-F3; invariant probe INV-003.
- Before: R1-F3 non-blocking, repair "Filing is refused unless an Offers row with an explicit filing answer and a matching `set_digest` exists. A resume returns the pending offer without asking. A changed set or a changed body digest needs a new offer."
- After: N-F5, non-blocking; repair in PC-07's words (base's last clause kept, since PC-07's text is a subset of it); added PLAN:140, SPEC:421-428 and SPEC:923 to the evidence (from INV-003 and diff-analysis C-005, re-read); a "linked" line naming N-F7 as the same gap. The grep claim was re-run: hits only PLAN:82 and STAGE2:148.
- Status: applied. Not raised to blocking (refactor plan).

### PC-08: `pending` is an Offers state (C-007)

- Source: base R1-F5; variant 3 earlier-findings check (M-F3 line).
- Before: repair "say 'a `recorded` row'".
- After: N-F7 repair "say 'a `recorded` or `offered` row'; `pending` is an Offers state", with a pointer to N-F5.
- Status: applied.

### PC-09: stale stage 2 quotes (C-008)

- Source: base R1-F6 (STAGE2:27); variant 3 R3-F6 (STAGE2:57, nine modules).
- Before: R1-F6 on STAGE2:27 only.
- After: N-F8 covers both stage 2 sentences, cites `cli/review/__init__.py` lines 19-29 (nine names, re-read) and PLAN:192; repair rewords both.
- Status: applied.

### N-F6 (no PC; carried from base R1-F4)

- Before: R1-F4 listed the family key among the missing inputs and cited "Stage 2 `safety --judge-answers` and the stage 2 recorded fixtures".
- After: the family-key part points to N-F2 (PC-02); the two stage 2 references are cited as STAGE2:57 and STAGE2:135 (re-read; the base gave no line).
- Status: carried with citation added.

### PC-04: `doctor.py` literal versus T2 (C-009)

- Source: variant 3 R3-F1.
- Before: absent from the base.
- After: N-F9, non-blocking, with the repair (build the marker from parts; acceptance grep on `doctor.py`, valid until stage 4).
- Status: applied. Variant 3 called `doctor.py` "already a tracked file" from `run_doctor` existing; no git was run in this merge, so the card says "an existing source file" (doctor.py line 17, re-read) and states that it holds no `review-severity:digest` text today (grep of `src/` and `plugins/`: no match).

### PC-05: `STRICT_T2` effect and banned-phrase scans (C-010, C-011)

- Source: variant 3 R3-F2 and R3-F5.
- Before: absent from the base.
- After: N-F10 and N-F11, both non-blocking, with variant 3's repairs.
- Status: applied with two narrowings after re-reading. (1) Variant 3 said "the stage 1 files stay untracked (only `.dev/tasks` is staged)"; PLAN:30 only says `.dev/tasks/` is always staged, so the card says "the plan's staging instruction names `.dev/tasks/` only". (2) Variant 3 said "stage 2 is not allowed to edit stage 1 files"; the stage 2 plan says this only for `follow_ups.py` (STAGE2:57), so the clause was dropped. The `SWEEP_PHRASES` list was located at test line 390 and `BANNED_SEVERITY_PHRASES` at line 112 (re-read) and cited.

### PC-06: audit-artifact omission as a run note (C-012)

- Source: variant 2 R2-F3.
- Before: absent from the base.
- After: a "Run notes (not plan findings)" section with the C-012 note and a supplemental table of seven rows mapping source lines 51 to 53 to PLAN:36, 52, 72, 151, 160, 173, 192, 200, 213 and 234 (each re-read). Re-read of `artifacts/coverage-matrix.yaml` confirmed only INF-081 and INF-082 cite source line 53 and none cite lines 51 or 52; INF-082 is matched to Task 7 though its lint lines sit in Tasks 9, 10, 12 and 13, noted in the table. INV-006 and INV-007 were added to the same section as run notes, as the orchestrator's decisions list them.
- Status: partly applied. The plan says the supplemental rows go "in the inferred-requirements table"; this merge may write only the card and this log, so `artifacts/inferred-table.md` was not edited and the rows are carried in the card instead. The orchestrator can copy them into the table.

### PC-10: format (ids, verdict, checked and not-checked lists)

- Source: base; variant 3 "Checked and found clean" and "Not checked"; diff-analysis A-002, A-003.
- Before: ids `R3-F1` to `R3-F6` (a numbering slip); verdict "NEEDS-REVISION. confidence 0.6" plus "If the owner reads R3-F1 as non-blocking, this is PASS with notes ... confidence about 0.7"; "Other checks" list; no "Not checked" list.
- After: ids `N-F1` to `N-F11` in the order the orchestrator fixed; one verdict, "NEEDS-REVISION. Blocking: 1 (N-F1). Non-blocking: 10 (N-F2 to N-F11)", with the closest-call status and no alternative verdict; "Checked and found clean" merges the base "Other checks" with variant 3's list; "Not checked" has three items (no test run; section 9.3 defining files only partly; STAGE2 read as it stands today).
- Status: applied. Variant 3's "Brief decisions 1, 2, 4 and 5 are honoured" line was rebased on the stage ledger (`stage-requests/README.md` lines 38-41, re-read), because the brief's numbering was not among the merge inputs; the cited PLAN lines are 24, 25, 26 and 124. Variant 3's "Every allow-list path ... exist" and stoprule-absence claims were re-checked with a read-only batch (all allow-list paths present; the stoprule folder and `finding-grader.md` absent from `src/superclaude`, the expected outcome).

## Base text corrected or dropped

- Earlier findings check, F4: PLAN:122 is the `Depends on: Task 4` line; the ledger mapping decision is at PLAN:124. Corrected (orchestrator instruction).
- Earlier findings check, F8: the base cited PLAN:56 and PLAN:115 for "full path in the Task 2 grep; 'present today'". PLAN:115 does not hold "present today"; PLAN:192 does ("the review subcommands present today"). PLAN:115 was replaced by PLAN:192. PLAN:115 stays cited under M-F7, where it holds.
- Earlier findings check, id cross-references: "R3-F1" to N-F1, "R3-F5" to N-F7, "R3-F2" to N-F4, "R3-F4" to N-F6.
- Dropped: variant 1's reviewer metadata lines (persona, model class, model observed), its "Orchestrator note" on the id slip (resolved by PC-10), its blind calibration block and its confidence figures. These describe reviewer 1's card, not the merged card.
- Dropped: base R1-F1's original repair (replaced by PC-01, rollback text is variant 1 line 14).

## Validation

- Heading hierarchy: one `#` title; `##` sections Findings, Run notes, Earlier findings check, Checked and found clean, Not checked, Verdict; `###` only for N-F1 to N-F11 under Findings. No level is skipped. Pass.
- Finding ids: N-F1 to N-F11 each have one heading. Every N-F id referenced in the body (N-F1, N-F2, N-F4, N-F5, N-F6, N-F7, N-F8, N-F9, N-F11) exists. R-ids appear only inside provenance comments. Pass.
- Provenance: every `##` and `###` section after the title carries one `<!-- Source: ... -->` comment; the header comment names the base and the merge date. Pass.
- Grades and verdict: 1 blocking (N-F1), 10 non-blocking, verdict NEEDS-REVISION, no hedge, matching the orchestrator's decisions. Pass.
- Contradiction re-scan: the only blocking finding is N-F1; no section calls another finding blocking; the "Not checked" list does not contradict a "clean" item (section 9.3 files are listed as partly checked in one place only). Pass.
- Citations: 78 distinct PLAN, SPEC, STAGE2, STAGE3 and STAGE4 citations, each re-read during this merge (PLAN and STAGE2 read in full; SPEC lines 205-214, 350-391, 420-441, 525-544, 588-597, 733-746, 846-851, 914-947; STAGE4 lines 110-121; STAGE3 lines 189 and 240 by search). 20 further file:line citations re-read: `agents/rf-qa.md` 111; `tests/skills/test_review_severity_rule.py` 28, 36-51, 36-39, 112, 117, 172-176, 390; `cli/review/__init__.py` 19-29; `cli/doctor.py` 17; `cli/review/verify_cmd.py` 76; `origin_repo.py` 77 and 156; `contracts/__init__.py` 93 and 129; `stage-requests/README.md` 18 and 38-41; `coverage-matrix.yaml` 508-527; `source.md` 51-53; `pragmatic.md` 227. Total 98 re-read. Citations dropped as unconfirmable: PLAN:115 for "present today" (F8, replaced) and variant 3's "only `.dev/tasks` is staged" and "stage 2 is not allowed to edit stage 1 files" wording (narrowed or dropped, see PC-05).
- Batch note: the read-only batch reported `BATCH_FAIL failures=1`; the one non-zero block was the expected absence of the stoprule folder and `finding-grader.md` from `src/superclaude`, which is the fact the card states.
- Changes applied: 10 of 10 (PC-06 partly: the supplemental rows are in the card, not in `inferred-table.md`).

