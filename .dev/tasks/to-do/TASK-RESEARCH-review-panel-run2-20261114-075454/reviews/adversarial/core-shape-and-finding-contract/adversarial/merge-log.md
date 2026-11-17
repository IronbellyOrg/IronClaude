# Merge Execution Log

## Metadata

- Base: Variant B (opus:architect+qa), `variant-2-original.md`
- Executor: merge-executor agent
- Changes applied: 11 of 11
- Status: success
- Timestamp: 2026-11-14
- Output: `../merged-core-shape-and-finding-contract.md`
- Code re-read during the merge (HEAD 50d4d2b9d, read-only): `findings.py:76-125,170-197,345-359,440-449` and Grep of `findings.py:29,124,350-351`; `ledger.py:90-269,320-469`; `cluster.py:126-182`; `findings_v2.py:76-140` and Grep of `:215`; `merge_cmd.py:111` (Grep); `tests/review/test_review_ledger.py:343-491`; `tests/review/test_review_cluster.py:277-294`; `tests/review/test_review_findings.py:108-119`. Lines carried from the variants or the debate and not re-read are tagged [CODE-VERIFIED] (by the variant author), [DEBATE-VERIFIED] or [UNVERIFIED] as the tag convention in the merged header states.

### Change 1: Withdraw the `LedgerError` guard and restate the boundary test
- **Status**: Applied
- **Source**: Debate Round 1 and Round 2 (both advocates, A-001 REJECT); Variant B 2.3, 4.1 INV-D, 5.2, E-3; Variant A section 6 T4
- **Target**: Base sections 1, 2.2 (spec-loop row), 2.3, 3.1 E-3, 4.1 INV-D, 5.2, 7 answer 2
- **Before**: 2.3 added a typed `LedgerError` in `merge_round` for a finding without an anchor; E-3 said a citation-only finding crashes the v1 ledger path; INV-D described the guard's failure mode; 5.2 asserted the new `LedgerError` naming the finding id; section 1 and 7 answer 2 cited "its guard (2.3)".
- **After**: 2.3 opens with "No guard is added; the boundary already exists in the v1 parser" and the verified rejection path (`ledger.py:128`, `findings.py:104`, `:80-81`, `:188-192`, `ledger.py:135-136`); E-3 corrected and tagged [CODE-VERIFIED, re-read in this merge] with the original claim marked [CODE-CONTRADICTED]; INV-D states that no guard is added and the existing refusal maps to exit 1; 5.2 (T4) pins today's rejection for one and several reviewers, with B's Round 2 assertion that the same reviewer's other valid lines are still merged; section 1 and 7 answer 2 no longer present the guard as part of the decision (7 answer 2 now states the warning-only loss conceded by advocate B).
- **Provenance tag**: `<!-- Source: Base (original, modified) - the typed LedgerError guard is withdrawn per Change 1 (...) -->` and the modified tags on sections 1, 2.2, 3.1, 4.1, 7 answer 2
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (remaining mentions of `LedgerError` are the withdrawn-guard statement in 2.3 and the existing no-valid-block refusal)

### Change 2: Withdraw the projection view
- **Status**: Applied
- **Source**: Debate Round 1 and Round 2 (advocate A weakness 5; advocate B concessions)
- **Target**: Base 2.1 table row and the paragraph after it; 5.1 totality condition; 2.4
- **Before**: 2.1 listed "Projection view" as a contract element with a paragraph on it; 5.1 required the projection to be total.
- **After**: The row and the paragraph are removed; a one-line note in 2.1 points to 2.4 item 5, which lists the projection view as deferred until a consumer exists; the totality condition is dropped from the merged 5.1 with a stated reason.
- **Provenance tag**: `<!-- Source: Base (original, modified) - "Projection view" row removed per Change 2; ... -->`; `<!-- Source: Base (original, modified) - item 3 reworded per Change 3; item 5 added per Change 2; ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (the word "projection" now appears only in the deferral note, 2.4 item 5, the 5.1 drop note, and as the ordinary word in E-5 and 7 answer 1)

### Change 3: Unknown-key policy
- **Status**: Applied
- **Source**: Variant A CO-4 answer; debate Round 2 N5; score matrix C-005 and X-004 (HYBRID)
- **Target**: Base 2.2 PR row "Unknown keys"; 2.4 item 3; section 1 and the header "Axis" line (consistency)
- **Before**: PR row "closed at the adapter, because the adapter is the only producer"; 2.4 item 3 "per module, as in 2.2"; section 1 "closed where one module owns both producer and consumer".
- **After**: PR row "open in the core (E-21); any adapter-side strictness is decided in slot C-10"; 2.4 item 3 "Any stricter unknown-key policy" with open keys in both parsers, `calibrated_confidence` still rejected by v2, adapter strictness to C-10; section 1 "unknown keys stay open in both parsers, as today". INV-C row (in-line `origin` keeps working) kept unchanged.
- **Provenance tag**: `<!-- Source: Base (original, modified) - spec-loop "Change needed" cell per Change 1 and Change 4; PR "Unknown keys" cell per Change 3; ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (no "closed at" phrase remains)

### Change 4: Stuck row and unread anchor flags
- **Status**: Applied
- **Source**: Variant A E11, T5, section 4 FX-2 row; debate Round 2 N3, N4, N-B1, N-B2, N-B4 and the advocate B comparison table
- **Target**: Base 2.3 (new content after the Change 1 block); 2.2 spec-loop row; section 1
- **Before**: No answer to FX-2; 2.3 held the guard.
- **After**: 2.3 states the stuck-row defect with re-read citations, the fail-closed behaviour (`ledger.py:93-104`, `test_review_ledger.py:476-490`) and the manual exit `ledger defer` (`ledger.py:350-360`); the agreed change (surface found/missing/ambiguous in the `### Lx` block of `## Blocking findings` from `render_merged_report`, not in the reviser-brief id line pinned by `test_review_ledger.py:459-467`, no prompt-file change, no knobs, clearing to C-02); caveats INV-001 and INV-015; a two-row table recording the unreconciled disputes (policy as data versus hard-coded; "say it is gone" versus re-locate only), with the statement that the base approach is used for the first and the second is not decided. The 2.3 title is "No boundary guard; the stuck row is surfaced instead".
- **Provenance tag**: `<!-- Source: Variant A, E11 and T5 (...) - merged per Change 4, with placement from the Variant B advocate's Round 2 (...) -->` and `<!-- Source: Debate transcript, Round 2 (...) - recorded disagreement per Change 4 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 5: Per-row answer table
- **Status**: Applied
- **Source**: Variant A section 4, updated to the debate result
- **Target**: New subsection 2.5 "Answers to the routed rows" (after 2.4)
- **Before**: Section did not exist.
- **After**: Table with rows C-S1, CO-1, CO-2, CO-3, CO-4, CL-X11, FX-1, FX-2, each giving the answer as the plan lists it and the section where the detail sits. Placed as 2.5 (a subsection) so sections 3 to 7 keep their base numbers.
- **Provenance tag**: `<!-- Source: Variant A, section 4 - merged per Change 5, answers updated to the debate result (...) -->`
- **Validation**: Structural integrity PASS | References PASS (every "Where" cell resolves) | Contradictions PASS (answers match 2.1 to 2.4 and section 5)

### Change 6: Convergence trigger and precondition
- **Status**: Applied
- **Source**: Variant B 5.4; debate Round 2 (advocate A T-a, T-b, T-c and the precondition; advocate B agreed)
- **Target**: Base 5.4
- **Before**: Item 2 "two or more verified defects in one quarter"; closing note "The numbers are a proposal for the debate, not findings".
- **After**: Items labelled T-a, T-c (replacing item 2, checkable on the fix's diff), T-b; a note that item 2 replaced the unmeasured quarterly count; the precondition (anchor-span branch in `same_defect_v2` or a derived `spec`-role citation; `test_review_cluster.py:279-293` changes as a planned pin). The original closing note was replaced because it described the removed item.
- **Provenance tag**: `<!-- Source: Base (original, modified) - item 2 replaced by advocate A's T-c and the precondition added per Change 6 (...) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 7: Merged test set
- **Status**: Applied
- **Source**: Variant A section 6 (T1 to T5); Variant B 5.1 to 5.3; debate Round 2 test table (advocate A) and advocate B's additions
- **Target**: Base 5.1 to 5.3
- **Before**: 5.1 conformance suite (with projection totality), 5.2 guard boundary test, 5.3 location-type measurement.
- **After**: 5.1 "Pin parity and differential replay" (T1 with `test_review_cluster.py:279-293` and `test_rendered_merged_report` added to the named pins, INV-003 and INV-018 caveats; T2 merged with old 5.1, projection check dropped, INV-021 and INV-016 caveats); 5.2 "Rejection pin and stuck-row probe" (T4 merged with old 5.2; T5 with `named_not_touched` and the `ESCALATE` at the cap assertion, clearing left to C-02, INV-015 and INV-001 caveats); 5.3 "Location-type reliability measurement" (B's pre-registered rule plus A's per-finding record, run after the snapshot plumbing fix and after A-002 is stated). Grouping into three subsections keeps the base numbers 5.1 to 5.4, so every existing reference ("test 5.1", "test 5.3", "section 5.4") still resolves.
- **Provenance tag**: per-subsection tags, e.g. `<!-- Source: Variant A, section 6 T1 and T2; Base 5.1 (conformance golden set) - merged per Change 7; ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (no crash-based test remains)

### Change 8: Repair step placement
- **Status**: Applied
- **Source**: Debate Round 2 (advocate B N-B3; advocate A agreed)
- **Target**: Base 2.1 row "Limit constants and repair step"; associated consistency edits to section 1 and E-11
- **Before**: "one normalise-or-itemise function that runs before either `parse_block`"; v1 numbers tagged [UNVERIFIED] at `findings.py:104,108,111-117,118`.
- **After**: The function is called from inside both `parse_block` functions (`findings.py:124`, `findings_v2.py:215`) on each line before the check and must not invent an anchor; the reason a caller-side repair fails; policy C-06; names checked against INV-K; the qualifier naming INV-003 (HIGH), INV-004, INV-010, INV-014, INV-022, INV-024. The v1 line list was corrected to `findings.py:104,108,114,118` and tagged [CODE-VERIFIED, re-read in this merge] (the refs check `len(refs) > 8` is at line 114). Section 1 now says "called inside both parsers". E-11's last cell now names the inside-`parse_block` placement and the INV-004 caveat, because the original "removes the difference for both" conflicted with INV-004.
- **Provenance tag**: 2.1 table tag naming Change 8; E-11 covered by `<!-- Source: Base (original, modified) - row E-11 last cell adjusted per Change 8 (...) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (INV-003 is stated, not hidden)

### Change 9: Corrected and added facts
- **Status**: Applied
- **Source**: Debate Round 2 N1, N2, N4, N5, N6, and the advocate B verifications (a) and (b)
- **Target**: Base section 3 (new subsection 3.5 with E-18 to E-22; E-3 correction applied under Change 1)
- **Before**: E-1 to E-17 only.
- **After**: 3.5 "Facts the debate added": E-18 (N1, `cluster_v2` cannot join anchor-only findings), E-19 (N2, clearing ignores block validity, pinned by `test_review_ledger.py:376-385`, bound to `resolved_check` rows, owner C-02 and C-03), E-20 (N4, anchor flags read only by tests), E-21 (N5, no key whitelist), E-22 (N6, duplicated limit literals). Each row tagged; facts re-read in this merge are [CODE-VERIFIED, re-read in this merge]; the `block_ok` read-site list and "read only by tests" are [DEBATE-VERIFIED]. The plan's "prior inert" item is carried in the 2.5 CO-2 answer with `ledger.py:259-272` rather than as a separate row; git history is already base E-5.
- **Provenance tag**: `<!-- Source: Debate transcript, Round 2 new evidence N1, N2, N4, N5, N6 (...) - merged per Change 9 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 10: Open invariants appendix
- **Status**: Applied
- **Source**: `invariant-probe.md` (INV-001 to INV-025; gate result CONVERGENCE BLOCKED on INV-003)
- **Target**: New final section 9 "Invariants the debate left unaddressed"; pointer added at the end of 4.2
- **Before**: Section did not exist.
- **After**: Section 9 opens with the required sentence "INV-003 (HIGH) blocks convergence under the protocol's invariant-probe gate; the debate ran at depth standard (no Round 3) and did not resolve it.", then a table of all 16 UNADDRESSED rows (INV-001, 002, 003, 004, 008, 009, 010, 014, 015, 016, 017, 018, 020, 021, 022, 024) with ID, category, assumption, severity and one-line evidence, then the probe summary and gate result. Changes 4, 7 and 8 reference it. A new section 8 "Debate result" (requested by the merge brief, not a plan change) sits before it and quotes the transcript metadata, the tally, the convergence status and the base-selection scores.
- **Provenance tag**: `<!-- Source: invariant-probe.md (...) - all 16 UNADDRESSED rows copied per Change 10 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (row count 16 matches the probe summary; HIGH 1, MEDIUM 14, LOW 1)

### Change 11: Open points section
- **Status**: Applied
- **Source**: Variant A section 9; debate Round 2 (A-002; the two disputes of Change 4; plumbing share of E1 flags)
- **Target**: New subsection 5.5 "Open points (carried, not resolved)", after the convergence trigger and before section 6 and the objection answer
- **Before**: Section did not exist.
- **After**: Six items: A-002 (how line numbers reach reviewers), whether v2 fingerprint line-insensitivity is intended, dispute 1, dispute 2, the clearing rule (C-02, C-03), and the plumbing share of E1 flags. Placed as subsection 5.5 so sections 6 and 7 keep their base numbers.
- **Provenance tag**: `<!-- Source: Variant A, section 9 - merged per Change 11, updated to the debate result (...) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Edits outside the eleven changes (reported for completeness)
- Header: title changed to "Merged position: slot C-01 (core-shape-and-finding-contract)"; Status line notes BLOCKED_BY_INVARIANTS; tag convention extended with [DEBATE-VERIFIED] and [design inference], and [CODE-VERIFIED] redefined to cover reads by either variant author or the merge executor. Requested by the merge brief.
- Section 8 "Debate result" added (merge brief).
- The trailing "Status: Complete" line of the base was dropped so the document ends with section 9, as the brief requires; the Status line at the top remains.

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: PASS. One H1; H2 sections 1 to 9 in order; H3 subsections 2.1 to 2.5, 3.1 to 3.5, 4.1 to 4.2, 5.1 to 5.5; no level is skipped (checked by Grep `^#`).
- Section ordering: PASS. Base order 1 to 7 kept; new material placed as subsections (2.5, 3.5, 5.5) so base numbers did not move; section 8 "Debate result" and section 9 "Invariants the debate left unaddressed" are last, as the brief requires.
- Document flow: PASS. No `TODO` placeholder remains (Grep). Every section and significant block carries a `<!-- Source: ... -->` tag (31 tags, counted by Grep); the three file-header provenance comments are present.

### Internal References
- Total references: 124 reference tokens (section numbers, E-numbers, INV ids) over 75 distinct targets, counted by `grep -oE` over the merged file.
- Resolved: 75 of 75 distinct targets. Section targets 2.1 to 2.5, 3.1 to 3.5, 4.1, 4.2, 5.1 to 5.5 and 9 exist; E-1 to E-22 are defined in section 3; INV-001 to INV-024 references point to rows in section 9; INV-A, B, C, D, E, F, J, L, N are rows of 4.1 and INV-I, INV-K items of 4.2. "section 2", "section 4" and "section 6" hits are references into named outside documents (research/03 section 2, Variant A sections 4 and 6), not into this file.
- Broken: 0.

### Contradiction Re-Scan
- New contradictions introduced: 0.
- Checks run (Grep over the merged file):
  - `LedgerError`: appears only in the 2.3 statement that the guard is withdrawn, in the existing no-valid-block refusal (2.3, 4.1 INV-D, 5.2) and in the provenance comment. The withdrawn guard is not described as part of the decision.
  - `projection`: the projection view appears only as deferred (2.1 note, 2.4 item 5) or dropped (5.1); other hits are the ordinary word in E-5 and 7 answer 1.
  - `crash`: section 1 and E-3 state that a citation-only finding does not crash the shipped path; no text states that a citation-only finding crashes `merge_round`.
  - `closed at`: no hit; unknown keys are open in every place they are mentioned.
  - `guard`: remaining hits are the withdrawn guard (1, 2.2, 2.3, 4.1, 7 answer 2) and the unrelated "chain guard" of v1 union-find (E-8, 7 answer 1).
- Residual wording inconsistencies, not contradictions of the decision (left as base text because no planned change targets them):
  - E-6 tags the `_REF_TOKEN` pattern text [UNVERIFIED] and E-7 tags the v1 limit lines [UNVERIFIED], while the edited 2.1 rows and E-22 tag the same lines [CODE-VERIFIED, re-read in this merge]. The stronger tag is correct (re-read at HEAD); the base rows are weaker, not wrong.
  - E-7, the 3.2 result paragraph and 4.2 item 3 still say the repair step runs "before" `parse_block` or both parsers, while 2.1 places the call inside both `parse_block` functions, before each line's check. The placement in 2.1 governs; the older phrases describe the same step at a coarser level.

## Summary
- Total changes planned: 11
- Successfully applied: 11
- Failed: 0
- Skipped: 0
- Post-merge validation: PASS
- Open item carried into the merged document, not resolved by the merge: INV-003 (HIGH), which keeps the debate status BLOCKED_BY_INVARIANTS; sixteen UNADDRESSED invariants are listed in section 9.
