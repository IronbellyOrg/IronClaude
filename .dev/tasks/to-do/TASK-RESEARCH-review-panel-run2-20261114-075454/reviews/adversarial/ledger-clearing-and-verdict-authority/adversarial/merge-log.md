# Merge Execution Log

## Metadata
- Base: Variant B (explicit per-row verification; `variant-2-original.md`, proposal-b.md)
- Executor: merge-executor agent (slot C-02)
- Changes applied: 10 of 10 planned
- Status: success
- Timestamp: 2026-11-14
- Merged output: `../merged-ledger-clearing-and-verdict-authority.md` (the parent folder of this adversarial folder)
- Frame kept: the base's 7 numbered sections (Position, Design consequence, Evidence, Invariants, Test or measurement, Effect on PR review and rf-qa, Strongest objection and answer) plus one closing unnumbered paragraph "Status of the debate" as the instruction asked
- Note on the plan: the plan says "Source of every rule below: the two advocates' Round 2 final positions"; each rule was taken from those tables and from the plan's integration points, with no rule added beyond them

## Changes Applied

### Change 1: Replace the quote-gated clearing rule with the quorum gate (from Variant A)
- **Status**: Applied
- **Source**: Variant A, Section 2 "Clearing rule" and "Requested reviewers" rows; debate C-001, X-002, X-003 (Round 2 final positions)
- **Target**: Base, Section 2.1 rule B1 (and B2), plus Section 1 paragraph (replace)
- **Before**: B1 cleared a `resolved_check` row only on a `prior resolved` line from a `block_ok` reviewer whose `evidence` quote occurs in `doc_text`, with no re-find; B2 filtered by `block_ok`; Section 1 described the quote-gated rule.
- **After**: B1 is the quorum gate: prior map built first; clear iff distinct `block_ok`-true `resolved` answers >= `need` (`need = min(Q, requested)`), no `block_ok`-true `open|regressed`, not re-found; C-03 asked for Q(re-review) = 1; failing rows stay `resolved_check` in `verify_ids`. B2 now counts distinct reviewer ids and records why the filter is required. Section 1 rewritten to the converged rule. The `--resolution`-absent fallback is recorded as an explicitly OPEN point (A: requested = reports passed; B: `need = Q`) in B1, Section 4.3 (INV-004) and Section 7.
- **Provenance tag**: `<!-- Source: Base (original, modified) - B1 replaced ... per Change 1 -->` and `<!-- Source: Variant A, Section 2 "Clearing rule" and "Requested reviewers" rows; debate outcomes C-001, X-002, X-003 - merged per Change 1 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (claims shown wrong by the debate are dropped: "recorded completion state is complete", "`--resolution` already carries requested ids", the quote gate; recorded in E23)

### Change 2: Make the `evidence` key record-only (from Variant A, key kept from Variant B)
- **Status**: Applied
- **Source**: Variant A Round 2 C-002 final position; Variant B Round 2 C-002 final position (converged)
- **Target**: Base, Section 2.1 rule B3 (replace "the ledger checks the quote" with "records the quote")
- **Before**: B3: the ledger checks that the quote occurs in `doc_text` ("exact normalisation is module work").
- **After**: B3: optional string `evidence`, at most 200 characters after flatten, a bad value ignored with no parser error (`findings.py:188-192`); the ledger writes it into `prior_note` with `quote_in_doc = bool(locate(doc_text, quote))`; never gating; promotion only on M1 evidence with a deletion carve-out and a lossy-span fix.
- **Provenance tag**: `<!-- Source: Base (original, modified) - B3 changed from "the ledger checks the quote" to "the ledger records the quote", per Change 2 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (the base's E-items that favour a gate, E8 and E13, now carry a sentence that the quote is recorded and does not gate)

### Change 3: Replace the blocking predicate with a typed authority plus a CRITICAL floor (from Variant A)
- **Status**: Applied
- **Source**: Variant A Section 2 `blocking` row; debate C-004, X-004, U-006 (Round 2 final positions)
- **Target**: Base, Section 2.1 rule B6 (replace)
- **Before**: B6: lens-owned `blocking(finding)` predicate over severity and category, `blocking_typed` kept, optional blind grader.
- **After**: B6: `blocking = typed or severity == "CRITICAL"` in `merge_round` at the annotate point (`ledger.py:135-138`); `blocking_typed` kept; each flip adds a warning; no category predicate, no grader in the core; `verdict:` line parser-neutral; M3 offline; no conflict with `findings_v2.py:161-162`; residual risk (MAJOR typed non-blocking still passes) cited as INV-016. Section 4.2 INV-J, Section 5 M3 and Section 6 M7 and "Blocking predicate" adjusted to match.
- **Provenance tag**: `<!-- Source: Base (original, modified) - B6 replaced ... per Change 3 -->` and `<!-- Source: Variant A Section 2 `blocking` row; debate outcomes C-004, X-004, U-006 - merged per Change 3 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (the base's predicate-based INV-J endangerment is removed, not left behind)

### Change 4: Narrow the pinned prior-line rule and route dissent to `regressed` (Variant A rule, Variant B state)
- **Status**: Applied
- **Source**: Variant A Section 2 "Prior lines" row and Round 2 C-005; Variant B Round 2 C-005 (converged)
- **Target**: Base, Section 2.1 rule B1 text "A `prior` of `open` or `regressed` sets the row" and Section 2.2 spec module paragraph (modify)
- **Before**: B1: "A `prior` of `open` or `regressed` sets the row to `open` or `regressed`" for any row; spec module paragraph silent on the docstring and the pinned test name.
- **After**: B1: a prior line moves only a `resolved_check` row (clear, or dissent to `regressed` with history event `dissent`); on any other status it is a `prior_note` plus a warning; same-reviewer duplicates resolve to dissent. Section 2.2: docstring `ledger.py:3-4` restated, `test_prior_lines_never_change_a_status` (`tests/review/test_review_ledger.py:318-338`) renamed with its assertions kept, `resolved_check` cases added. Section 3 E7 completes the base's pin list with that test.
- **Provenance tag**: `<!-- Source: Base (original, modified) - prior-line rule narrowed and dissent routed to `regressed`, per Change 4 -->` and `<!-- Source: Base (original, modified) - spec module paragraph narrowed per Change 4 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (the base's own B1 versus B7 contradiction, noted in base-selection.md, is removed by this narrowing)

### Change 5: Add the derived-verdict output surface and the empty-brief handling (Variant A text, Variant B VM-6 form)
- **Status**: Applied
- **Source**: Variant A Section 2 "Verdict" row; Variant A and B Round 2 C-008 final positions
- **Target**: Base, Section 2.1 rule B5 (extend) and rule B4 last sentence (VM-6)
- **Before**: B5 listed the three id lists and said the Reviser brief carries `brief_ids` only; B4 last sentence: a round after ESCALATE is refused (research 03 1.5 X1).
- **After**: B5: `ledger verdict` JSON gains `next` (`re-review` or `revise`); the Reviser-brief section prints the "no revision needed; re-review the same candidate against the same baseline to answer: <ids>" wording; the report detail section and Escalation paragraph list `brief_ids`, `verify_ids`, `held_ids`; empty-brief REVISE stays exit 10; the retry reuses the same BASELINE and CANDIDATE. B4 last sentence: VM-6 derived form (`len(rounds) >= cap_reviews` or derived decision ESCALATE before the merge). Open items cited: INV-003 (HIGH), INV-006.
- **Provenance tag**: `<!-- Source: Base (original, modified) - B5 extended ... per Change 5 -->` and `<!-- Source: Variant A Section 2 "Verdict" row and Section 3.4 item 8 - merged per Changes 5 and 6 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (the base sentence "The Reviser brief carries `brief_ids` only" is replaced, not kept beside the new wording)

### Change 6: Add `held` events, reason codes and `unverified_ids` to the merge output (from Variant A)
- **Status**: Applied
- **Source**: Variant A Section 2 Clearing-rule row, Section 3.4 item 8 and U-001
- **Target**: Base, Section 2.1 rule B5 and Section 5 test list (insert)
- **Before**: B5 had `verify_ids` and `held_ids` as derived lists only; the base test list had no `unverified_ids` or event check.
- **After**: B5: the merge JSON gains `unverified_ids` and `held_ids`; history events `held` (reason `no-examination-record` or `dissent`) and `refound_deferred`. Section 5 T1 asserts `unverified_ids`; T3 asserts `refound_deferred`.
- **Provenance tag**: `<!-- Source: Variant A Section 2 "Verdict" row and Section 3.4 item 8 - merged per Changes 5 and 6 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS with one flagged overlap (see Contradiction Re-Scan, note 1: `dissent` appears as a history event in B1 and as a `held` reason in B5, as the plan states both)

### Change 7: Keep terminal `defer`, drop expiry, add status guard tests (Variant B kept; Variant A tests added)
- **Status**: Applied
- **Source**: Variant B rule B7; Variant A Section 5 item 1 (D-11 A/B/C cases); debate C-006, C-007, U-002, U-003
- **Target**: Base, Section 2.1 rule B7 and Section 5 T3 (modify)
- **Before**: B7: `defer` took `--owner` and `--reason`; "An expiry may be recorded; it has no machine meaning"; the T3 set was generic.
- **After**: B7: no expiry in the core (nothing would read it); `defer` allowed on blocking `open|regressed|resolved_check`; no round record written; a re-found deferred row stays `deferred` and is listed as `refound_deferred` in the merge result and Escalation text; A's D-11 A/B/C reproductions as tests, two-row fixture for the re-find case (INV-007); no undefer command noted as INV-008.
- **Provenance tag**: `<!-- Source: Base (original, modified) - B7 modified ... per Change 7 -->` and `<!-- Source: Variant B rule B7; Variant A Section 5 item 1 (D-11 A/B/C cases); debate outcomes C-006, C-007, U-002, U-003 - merged per Change 7 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (Variant A's `expires_round` and reopen-on-refind are not carried; listed in "Changes NOT Being Made" of the plan)

### Change 8: Make the file shape change drop the stored keys and add the text-hash guard (debate refinements of the base)
- **Status**: Applied
- **Source**: Variant B Round 2 C-009 and C-003 final positions; `synth-06-conflict-log.md:178` (VM-3 wording, read by the B advocate); Variant A Round 2 conditional form
- **Target**: Base, Section 4 INV-D paragraph and Section 2.1 rule B4 (modify)
- **Before**: INV-D: "B adds fields only (`verify_ids`, `held_ids`, `new_sha256` ...)"; B4: `revise` stores `new_sha256`, `merge` refuses a different hash.
- **After**: B4: top-level `pending_new_sha256`; `merge_round` refuses on mismatch and then clears it; `apply_revision` refuses while one is pending (revise not idempotent, `ledger.py:343-347`). INV-D (Section 4.2): new round records drop `verdict`, `decision`, `brief_ids`; `verdict()` derives from rows and ignores old stored keys; schema string kept, `/2` open (LG-2); rollback "keep storing the keys until all readers upgrade". Variant A's snapshot form is not carried (a stored verdict under another name).
- **Provenance tag**: `<!-- Source: Base (original, modified) - B4 hash binding kept and specified ... per Changes 5 and 8 -->` and `<!-- Source: Base (original, modified) - INV-D rewritten for the dropped stored keys and the pending hash, per Change 8 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (B5 says "New round records drop `verdict`, `decision` and `brief_ids`", consistent with INV-D)

### Change 9: Merge the measurement plans (from Variant A and Variant B)
- **Status**: Applied
- **Source**: Variant A Section 5 items 3-4 (three-arm replay incl. the quote-verified arm, wrongness rule registered before the run); Variant B M2 and M3; debate C-010, U-004, U-008
- **Target**: Base, Section 5 (insert)
- **Before**: M1 compared current clearing against B only; M3 measured predicate agreement; the closing sentence named the quote check as the thing M1 could refute.
- **After**: Section 5 keeps T1-T5 (rewritten to the converged rules) and M1-M3; M1 has three arms (current silence-clear, quorum gate, quote-verified per-row) with a fake-fix condition; M2 counts compliance by ledger id and cites `anchor_status` (`findings.py:350`) as a free proxy; M3 counts floor flips; the wrongness rule is committed before the first run and fixes no numbers.
- **Provenance tag**: `<!-- Source: Variant A Section 5 items 1 to 4 ... - merged per Changes 7 and 9; Variant B M2 and M3; debate outcomes C-010, U-004, U-008 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS with one flagged wording point (see Contradiction Re-Scan, note 2: the plan calls `anchor_status` a "compliance proxy"; the debate text, Variant B Round 2 new evidence 4, calls it a proxy for the quote false-hold rate, and the merged text follows the debate text)

### Change 10: Record the open conditions the debate left unaddressed (from the invariant probe)
- **Status**: Applied
- **Source**: `invariant-probe.md` (INV-001 to INV-022); `return-contract.yaml` `unaddressed_invariants`
- **Target**: Base, Section 4 (insert a subsection "Open conditions left by the debate")
- **Before**: Section 4 had only the preserved and endangered lists; no open-condition record.
- **After**: Section 4.3 "Open conditions left by the debate": a table of INV-001, INV-002, INV-003 (HIGH, UNADDRESSED) quoting the assumption text from the probe, plus one line each for INV-004 to INV-011, INV-013, INV-014, INV-016, INV-018 and INV-020 (MEDIUM and LOW, UNADDRESSED), and a closing line naming the ADDRESSED ones (INV-012, 015, 017, 019, 021, 022). No new rule is added for any of them. Sections 4.1 and 4.2 keep which of INV-A..INV-N the converged design keeps or endangers (A, B, I, E, G, L, F kept; D, C, J, N, H and rule S1-S5 as endangered or low-risk, adjusted).
- **Provenance tag**: `<!-- Source: invariant-probe.md (INV-001 to INV-022), return-contract.yaml `unaddressed_invariants` - inserted per Change 10; no new rules -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (the return-contract.yaml file was not opened; the ids and assumption text were taken from invariant-probe.md and from the debate transcript's Round 2.5 summary)

## Post-Merge Validation

Checks were run on the merged file with Grep (headings, `TODO`, section references, rule and evidence ids, dash characters, provenance tags) and by reading the merged text against the Round 2 final positions in `debate-transcript.md`.

### Structural Integrity
- Heading hierarchy: PASS. One H1; seven numbered H2 sections in the base's order (1 Position, 2 Design consequence, 3 Evidence, 4 Invariants, 5 Test or measurement, 6 Effect on PR review and rf-qa, 7 Strongest objection and answer) plus one unnumbered closing H2 "Status of the debate"; H3 only under Section 2 (2.1, 2.2) and Section 4 (4.1, 4.2, 4.3); no level is skipped.
- Section ordering: PASS. The base's order is kept; the only additions are the H3 subsections and the closing paragraph. Section 4.3 "Open conditions left by the debate" sits last in Section 4, after the keep and endanger lists.
- Document flow: PASS. No `TODO` placeholder remains; each stub placeholder was replaced section by section. The merged file carries the three header provenance comments and 35 `<!-- Source: ... -->` tags (grep count of `<!-- Source:`).
- Dash and style check: PASS. No em dash or en dash in the merged file (grep count 0), no emoji.

### Internal References
- Total references: about 30 references to sections of the merged document ("section 2.1 B1", "section 4.3", "section 4.2", "section 4, INV-D", "section 5", "section 2.2", "section 6"), plus the rule and evidence ids used inside the document (B1 to B7, E1 to E23, T1 to T5, M1 to M3, INV-A to INV-N and the probe ids INV-001 to INV-022)
- Resolved: all
- Broken: 0. Checks made: B1 to B7 are each defined in Section 2.1 and every mention resolves; E17 to E23 are defined in Section 3 and the mentions of E20 and E23 in Section 7 resolve; INV-001 to INV-003 and the MEDIUM and LOW ids named in Sections 1, 2, 4.2 and 7 are all defined in Section 4.3. References that look like sections but point to outside documents ("research 03 section 1.3", "research 12 section 2.1", "round2-B.md section 6 item 6") were excluded from the count.

### Contradiction Re-Scan
- New contradictions introduced: 0 logical contradictions with the Round 2 final positions of either advocate. Rule-by-rule check against the final tables: C-001 (gate, dissent to `regressed`, `verify_ids`, `need = min(Q, requested)`, the `--resolution`-absent split kept OPEN), C-002 (record-only, 200 characters, bad value ignored, `quote_in_doc`), C-003 (`pending_new_sha256`, revise guard), C-004 (floor in `merge_round`, no predicate), C-005 and X-001 (narrowed rule, docstring, renamed test), C-006 (no expiry), C-007 (`refound_deferred`), C-008 (three lists, `next`, VM-6 derived form), C-009 (stored keys dropped), A-005 (`Q_kind` interface only).
- Claims dropped or corrected as the plan says: Variant A's "recorded completion state is `complete`" and "`--resolution` already carries requested ids" (recorded in E23), Variant A's `expires_round` and reopen-on-refind, Variant A's snapshot form of C-009, Variant B's quote gate (B3), Variant B's category predicate and optional grader (B6), Variant B's "`prior open` sets any row" (B1).
- Details (wording points for the orchestrator, none a contradiction):
  1. `dissent` appears twice by plan: as the history event on a row routed to `regressed` (Change 1, B1) and as a `held` reason code (Change 6, B5). The merged text keeps both as the plan states them; a dissent row is not left at `resolved_check`, so the `held` reason `dissent` has no row that waits at that status in the converged rules. Neither the plan nor the Round 2 final tables says which code the merge JSON uses for a dissent row. Not resolved by the merge.
  2. The plan calls `anchor_status` the "compliance proxy" (Change 9); the debate (Variant B Round 2 new evidence 4) describes it as a free proxy for the quote false-hold (miscopy) rate. The merged text follows the debate text in M2 and does not call it a compliance proxy.
  3. The base paper's E1 to E16 were kept even where the converged rules replace the rule they motivated (for example E13 favours verification over voting); each such item now carries one sentence saying the quote is recorded and does not gate (E8, E13, E15, E16).
- Additions not literally in the plan, all sourced from the debate or the plan's integration points and tagged `[debate R2]` so the reader sees that the merge did not re-read the code: evidence items E17 to E23, the extra text in E5, E6, E7, E12, E20 to E23, and the new tag `[debate R2]` itself. Existing `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]` and `[UNVERIFIED]` tags and every file:line citation of the base were kept as in the source. No code file was read by the merge.

## Summary

- Total changes planned: 10
- Successfully applied: 10
- Failed: 0
- Skipped: 0
- Post-merge validation: PASS
- Open items carried into the merged document (not merge failures): the `--resolution`-absent fallback (OPEN); the three HIGH invariant conditions INV-001, INV-002, INV-003 (UNADDRESSED, debate status BLOCKED_BY_INVARIANTS); the thirteen MEDIUM and LOW UNADDRESSED conditions listed in Section 4.3; the unresolved S-002 tag-discipline point (handled by explicit tags)
