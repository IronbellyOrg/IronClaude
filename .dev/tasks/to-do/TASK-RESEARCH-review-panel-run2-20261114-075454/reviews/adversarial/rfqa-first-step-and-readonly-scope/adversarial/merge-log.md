# Merge Execution Log

## Metadata

- Base: Variant B (Proposal B, `variant-2-original.md`)
- Executor: merge-executor agent
- Changes applied: 11 of 11
- Status: success (merge execution). The merged document itself records a partial resolution: BLOCKED_BY_INVARIANTS, five unresolved points, six HIGH invariants UNADDRESSED, none decided by the merge.
- Timestamp: 2026-11-14T17:20:12Z (merge date in the provenance header, from `date -u`)
- Output: `../merged-output.md` (slot folder), 11 numbered H2 sections plus "Merged outcome"; 35 `<!-- Source: ... -->` tags; 10 visible correction notes.
- Section mapping (base number -> merged number): 4 -> 1; 1 -> 2; 2 -> 3 (new 3.3 from Change 7); new 4 (Change 11); 3 -> 5 (new 5.5); 5 -> 6 (new 6.3); 6 -> 7; 7 -> 8; 8 -> 9 (9.1 base, 9.2 Variant A); new 10 (Change 10); 9 -> 11. Cross-references in base text were renumbered accordingly.

## Changes Applied

### Change 1: Position paragraph and clauses B-1, B-2, B-3 rewritten as the hybrid position
- **Status**: Applied
- **Source**: Variant A Section 1 and Section 7 part 2; `round2-advocate-A.md` and `round2-advocate-B.md` Proposed resolution items 1, 6, 7, 8
- **Target**: Base Section 1 -> merged Section 2
- **Before**: Single-document gate as the first step; B-3 "the `/task` lens agents' tools and mode are not changed in the first change".
- **After**: Lens-level first change (one read-only lens-reviewer agent plus oracle, no engine); Q3 to the owner; B-1/B-2/B-3 rewritten per the plan text; pointer to section 4 for what is not changed; correction note quoting the original clauses with the concessions (B Concession 6, B-R2 response 3, B-R2 "Verification of N1-N3", A-R2 responses 1 and 7). Consequential edits under this change: Base Section 2 document-gate module and "Additive by construction" kept only as a correction note (3.2); Base Section 8 closing paragraph (B:109) kept as a correction note (9.2); INV-C/INV-D, INV-I, INV-L, INV-H lines adjusted (6.1, 6.2) so they no longer refer to a panel run in the first change.
- **Provenance tag**: `<!-- Source: Base (original, modified) — Base Section 1 rewritten as the hybrid position per Change 1 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 2: Reorder: consistency check first and a separate "What was not verified" section
- **Status**: Applied
- **Source**: Variant A Section 0 (table); Variant B Section 4 and Section 9
- **Target**: Base Section 4 -> merged Section 1; Base Section 9 -> merged Section 11
- **Before**: Consistency prose as Section 4, after the evidence.
- **After**: Two-column table (slot outcome as adjudicated / what this resolution does), with B's dependency statements (C-01 T-a; C-02 `next`, `--resolution`, C-02's INV-001..INV-003; C-03 `degrade`, floor 2, condition 7) attached to a later engine step; A's floor note restated (prose floors stay, C-011); X-006 stated (per-reviewer confidence, `rf-qa.md:505`; B Concession 3). Cross-references renumbered.
- **Provenance tag**: `<!-- Source: Variant A, Section 0 (table form) merged with Base Section 4 (dependency statements) — moved to the front per Change 2 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 3: Design consequence rewritten
- **Status**: Applied
- **Source**: Variant A Section 2 items 1-4; `round2-advocate-A.md` items 2-3; `round2-advocate-B.md` response items 2-3
- **Target**: Base Section 2 -> merged Section 3 (3.1 shared core, 3.2 new deliverables)
- **Before**: "No new core feature is needed"; template schema claim; "a plan-mode agent without Write, Edit or Bash"; new document-gate module.
- **After**: (a) shared core: no edit; (b) agent definition, agreed text plus three items labelled `B amendment, not answered by A` (exact tool list; S1-S3 verbatim with INV-013; first line states lens and slot); INV-016, INV-017 (and INV-014) recorded next to it; (c) subset guard with `Variant A text` and `Variant B text` mutator lists and a negative fixture, INV-005 and INV-004 noted; (d) "plan-mode agent" phrase replaced, correction note (B-R2 response 2); (e) unresolved points deferred to section 10.
- **Provenance tag**: `<!-- Source: round2-advocate-A.md and round2-advocate-B.md "Proposed resolution" items 2-4; Variant A Section 2 items 1-4; merged per Change 3 (b)-(e) ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 4: Evidence section corrected and extended
- **Status**: Applied
- **Source**: Variant B 3.1-3.4; Variant A 3.1 (E1-E9), 3.2, 3.3, 3.4, 3.5; `round2-advocate-A.md` N1-N6 and Pilot re-check; `round2-advocate-B.md` NB1-NB8 and Verification of N1-N3; fault-finder INV-005, INV-006, INV-008, INV-011
- **Target**: Base Section 3 -> merged Section 5 (5.1-5.4 extended, new 5.5)
- **Before**: B:16 schema-change claim; B:28 "must be installed"; B:33 "no evidence ... has ever modified a file"; B:38 two-implementations consequence; no run evidence.
- **After**: Corrections in place with visible notes: B:16 -> hash-neutral (X-002, B conceded; placed in 3.1 where B:16 stood); B:28 -> `_assert_present` (`test_cli_install.py:502-506`), real cost `make sync-dev` / `verify-sync` (A-006); B:33 -> N1; B:38 -> withdrawn (B-R2 response 4); B:31 "highest-traffic QA path" qualified by N2 (inline note). Variant A rows E1-E9 and the A 3.2-3.5 statements inserted as claim/evidence/tag tables per clause (S-003). New 5.5 with the corpus counts explained (366 = B Round 1 raw, no skip rule; 278 = same selection after the 117 skip; 571 = non-fix by exclusion; 517 = reflect-reviewer), the pilot table (raw against de-duplicated), N1 with B's two corrections (restored byte for byte; 3 replaced by 1 for about 5.6 minutes; damage count 2 or 3 unsettled; cause dispatch by line reference plus agent misreading), N2 (118 A / 107 B), N3 table with both advocates' figures (pytest 74/77; standard-lens subset pytest 1/2), NB5-NB7, N4 plus INV-005 counts, N5 with the fault-finder's 7 refused calls (INV-006), N6, INV-008 caveat. Figures copied, none recomputed.
- **Provenance tag**: `<!-- Source: round1-advocate-B.md Strengths 3-5 (pilot); round2-advocate-A.md "New evidence" N1-N6 and "Pilot re-check"; ... — new subsection per Change 4 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (two citation ranges for the worker-contract test, `:1715-1729` in A and `:1716-1730` in B, are both shown with attribution)

### Change 5: Invariants section updated
- **Status**: Applied
- **Source**: Variant B Section 5; Variant A Sections 4.1 and 4.2; `invariant-probe.md`
- **Target**: Base Section 5 -> merged Section 6 (6.1, 6.2, new 6.3)
- **Before**: INV-G "left unmet for the existing `/task` lens agents"; INV-J with `task/SKILL.md` not edited; INV-K install-list wording.
- **After**: INV-G per plan text (held for new reviewers; conditional for steps 3-4; unmet for skill-embedded and task-file items and executing lenses and verifiers, with the step-8 pair marked as following Variant B text); INV-J with the conditional edit and both edited-step texts; INV-K/INV-N with A-006; residuals INV-018 and INV-007; A's two endangered rows, conditioned on the switch; note on A's other rows; 6.3 table of all 18 INV rows (ID, severity, status, one line), with the counts 6 HIGH, 9 MEDIUM, 1 LOW UNADDRESSED, INV-005 and INV-011 ADDRESSED, BLOCKED_BY_INVARIANTS, no Round 3. No item is shown as resolved.
- **Provenance tag**: `<!-- Source: invariant-probe.md (18 rows and Summary); round2.5-fault-finder-raw.md — new subsection per Change 5. No item is resolved here. -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 6: Measurements merged into one ordered pipeline
- **Status**: Applied
- **Source**: Variant A Section 5; Variant B Section 6; A-R2 items 3-5, 9; B-R2 response items 3-5 and Proposed resolution items 3, 4, 5, 9
- **Target**: Base Section 6 -> merged Section 7 (replaced)
- **Before**: M-B1..M-B4 as independent measurements.
- **After**: Six ordered steps, each labelled with the clause it decides: (1) static guards; (2) full M-B1 audit, agreed classes plus `B amendment, not answered by A` items; (3) oracle with the deterministic arm as `Variant A text` / `Variant B text` and INV-003, INV-001, INV-016, INV-017 noted; (4) write-probe as `Variant A text` / `Variant B text`; (5) M-B3 with `task/SKILL.md` as the one allowed edited pinned file under the switch; (6) M-B4. Right/wrong rules rewritten for arm 1a (A's typed-`prior` criterion noted as leaving with Half 2). Correction notes for M-B2 as written and the first M-B1 rule.
- **Provenance tag**: `<!-- Source: Variant A Section 5 (ordered pipeline M1-M5, right/wrong rule) merged with Base Section 6 ... — replaces Base Section 6 per Change 6 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 7: Conditional standard-lens switch, executor persistence and step 10
- **Status**: Applied
- **Source**: A-R2 Proposed resolution item 7 and Final position table (A-003, A-004, C-002, C-006, C-008); B-R2 response item 7 and Proposed resolution item 7
- **Target**: Base Section 2 -> new merged subsection 3.3; Section 1 -> merged Section 2 (Q3 and the conditional in the position paragraph)
- **Before**: Section did not exist.
- **After**: Q3 (agreed text) plus B's amendment on where N1 occurred; agreed core; splits (i) step-8 pair, (ii) edited steps, (iii) lens-identity blocker (`B amendment, not answered by A`), (iv) exclusion scope, (v) pre-computed counts; INV-002, INV-015, INV-009, INV-012 listed as HIGH UNADDRESSED.
- **Provenance tag**: `<!-- Source: round2-advocate-A.md Proposed resolution items 6-7 and Final position table ...; round2-advocate-B.md Response items 6-7 and Proposed resolution items 6-7 — merged per Change 7 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 8: Future PR review and rf-qa replacement
- **Status**: Applied
- **Source**: Variant B Section 7; Variant A Section 6; A-R2 Final position table C-012
- **Target**: Base Section 7 -> merged Section 8
- **Before**: "PR code review: no effect in the first change"; prerequisites (a)-(f) for the M-B2-style oracle; "What B costs".
- **After**: C-012 hybrid (M5 and M13 in the first change; M4 and M9 wait) with a correction note; prerequisites (a)-(f) adjusted per plan; cost statement rewritten for the lens-level first change; A's list of what is left open added.
- **Provenance tag**: `<!-- Source: Base (original, modified) — Base Section 7 updated per Change 8 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 9: Strongest objection and answer
- **Status**: Applied
- **Source**: Variant B Section 8; Variant A Section 7; Round 2 of both advocates
- **Target**: Base Section 8 -> merged Section 9 (9.1, 9.2)
- **Before**: B's objection with an answer that relied on M-B1 not yet having run.
- **After**: 9.1 B's objection with the answer updated by N1 (B-3 refuted, hardening enters as the agent plus the conditional switch); 9.2 A's objection with the answer as the debate left it (no engine swap, conditional switch guarded by arm 1a and the unedited pinned suites; "selectable branch" dropped, A conceded; X-005; residual Bash-recall risk).
- **Provenance tag**: `<!-- Source: Variant A, Section 7 — objection and answer as the debate left them, merged per Change 9 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 10: Unresolved wording, open conditions and what was not verified
- **Status**: Applied
- **Source**: `debate-transcript.md` Convergence Assessment; A-R2 and B-R2 Proposed resolution items 10-12; Variant A Section 8; Variant B Section 9; fault-finder "Not verified"
- **Target**: New merged Section 10 (10.1, 10.2) before merged Section 11
- **Before**: Section did not exist (Section 11 existed as Base Section 9).
- **After**: Table of C-002, C-006, C-008, A-001, A-004 with verbatim `Variant A text` / `Variant B text`; the two clusters; the fault-finder's remark on the three disputes, stated as a remark; open conditions (i) with both texts and the `B amendment, not answered by A` no-clobber item, (ii) engine (agreed), (iii) evidence quality with the N1 damage count as a B amendment, (iv) the HIGH invariants stand. Section 11 is the union of the three not-verified lists, with notes where the debate later answered an item.
- **Provenance tag**: `<!-- Source: debate-transcript.md Convergence Assessment and Scoring Matrix; ... — new section per Change 10 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 11: Out-of-scope table and changes-not-made reflected in the document
- **Status**: Applied
- **Source**: A-R2 and B-R2 Proposed resolution item 8; `refactor-plan.md` "Changes NOT Being Made"
- **Target**: New merged Section 4, after the design-consequence section
- **Before**: Section did not exist (B:21 list inside Base Section 2).
- **After**: Agreed item-8 list with the one label difference (`Variant A text` / `Variant B text`); B:21 untouched list; plugin note (B:74 [CODE-VERIFIED], Variant B only; Variant A section 6 reports the four named agents absent by Glob and lists whether the plugin ships the `task` skill as not verified); table of Variant A items not carried; list of Variant B items not carried.
- **Provenance tag**: `<!-- Source: round2-advocate-A.md and round2-advocate-B.md "Proposed resolution" item 8; Base Section 2 ...; refactor-plan.md "Changes NOT Being Made" — new section per Change 11 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: PASS. Starts with one H1; H2 "Merged outcome" then H2 sections 1-11; H3 only under sections 3 (3.1-3.3), 5 (5.1-5.5), 6 (6.1-6.3), 9 (9.1-9.2) and 10 (10.1-10.2); no level gap (no H4 or deeper); no orphan subsection (every H3 group has at least two members). Checked with Grep `^#{1,6} ` over the merged file.
- Section ordering: PASS. Order as instructed: outcome, consistency check, position, design consequence, out of the first change, evidence (with 5.5 run evidence), invariants (with 6.3 Round 2.5 table), measurements, PR review and rf-qa replacement, objections, unresolved points and open conditions, what was not verified.
- Document flow: PASS. No stub placeholder left (Grep). Closing line separates document status (complete) from resolution status (partial) to avoid two conflicting "Status" lines.

### Internal References
- Section references ("section N" / "Section N" in prose, excluding provenance comments and references to sections of r13 or of the variants): 48 total, 48 resolved, 0 broken.
- "Change N" references: 40, all inside provenance comments, unique Change 1-11, all present in `refactor-plan.md`; 0 broken.
- Point ids (S-/C-/X-/A-/INV- followed by three digits): 261 occurrences. 49 unique diff or probe ids (S-001..S-005, C-001..C-012, X-001..X-007, A-001..A-006, A-008, INV-001..INV-018) all exist in `diff-analysis.md` or `invariant-probe.md`. 3 unique ids C-105, C-107, C-113 (10 occurrences) are cap-row ids of `tests/skills/fixtures/review_severity_cap_edits.yaml`, external, as cited in `variant-1-original.md:61` and `round2-advocate-B.md` NB8. 9 occurrences of INV-001..INV-003 are other slots' invariants and are always written with their slot (C-01's, C-02's, C-03 INV-003); they are not the fault-finder's ids. Broken: 0.
- Forbidden-content check (Grep over the merged file and this log for the two forbidden strings named in the assignment): 0 matches in the merged file; this log names neither string.

### Contradiction Re-Scan
- New contradictions introduced: 0 remaining (4 found during the scan and fixed within the plan's rules):
  1. INV-G line (plan text) said "unmet ... for verifiers", which reads as deciding split (i) for Variant B; fixed by marking it as following Variant B text and naming Variant A text.
  2. Base sentence "It is the highest-traffic QA path in the repository" (B:31) was in tension with N2; kept as a quoted, qualified note in 5.1 instead of an unmarked claim, and the cost statement in section 8 no longer calls the gate "highest-traffic".
  3. Closing "Status: Complete" against "Status of this resolution: partial"; closing line rewritten as document status versus resolution status.
  4. An evidence sentence that tied Advocate A's 155 transcripts to the difference between 571 and 278 was an executor inference; rewritten as Advocate A's note on the literal selection.
- Checked and consistent: packaged templates stated as 8 everywhere (9 appears only as Variant A's error, X-007); 366, 278, 571 and 517 each stated with what they count (5.5); N5 refused calls stated as 2 (Advocate A) and 7 (fault-finder, INV-006) with attribution; N2 118 (A) and 107 (B); pytest 74 (A) and 77 (B); N1 damage 2 or 3 unsettled; no split item (C-002, C-006, C-008, A-001, A-004, or the mutator list, deterministic arm and write-probe form) is shown as agreed; none of INV-002, INV-009, INV-012, INV-015, INV-016, INV-017 is shown as resolved.
- Residual, not a contradiction: the provenance-tag separator uses the template's literal ` — ` form (refs/artifact-templates.md Section 6).

## Summary
- Total changes planned: 11
- Successfully applied: 11
- Failed: 0
- Skipped: 0
- Post-merge validation: PASS (structure, references, contradiction re-scan, forbidden-content check)
- Not decided by the merge, as instructed: C-002, C-006, C-008, A-001, A-004; the six HIGH UNADDRESSED invariants.

Status: Complete
