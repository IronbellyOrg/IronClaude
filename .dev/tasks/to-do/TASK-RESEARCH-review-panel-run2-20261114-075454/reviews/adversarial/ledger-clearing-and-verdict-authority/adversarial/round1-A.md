# Round 1, Advocate for Variant A (slot C-02, ledger clearing and verdict authority)

All file:line citations below were re-read in this session (ledger.py 80-480, findings.py 15-196, merge_cmd.py whole, test_review_ledger.py 193-217, 318-338, 376-405, document_review_loop_prompts.md 28-73, spec-panel.md 255-265, panel.py `apply_to` hits).

## Position

Variant A is the better core for clearing and blocking authority. In the default flow (one re-review reviewer) its gate is B's gate minus a quote that checks occurrence, not examination, and B's lens predicate misgrades the shipped grading rule. B is better on three narrower points: text-hash binding, the state a row takes on reviewer dissent, and a free pre-measurement. The merged result should be A's guard plus those three.

## Steelman of Variant B

B's strongest case is that silence is the defect and an explicit, attributed answer is the cure. The shipped brief already asks for one prior line per blocking row (`document_review_loop_prompts.md:49, 61`), so the reviewer-side cost is mostly paid and the ledger just throws the answers away (`ledger.py:259-272`). A quote that must occur in the new text catches a reviewer who never read the revision and invents an answer. The text-hash binding (B4) makes any text check meaningful, because `merge_round` hashes whatever text it is handed (`ledger.py:279`) and `merge_cmd.py:99-109` passes the `--doc` file through unchecked. A `prior open` moves the row back to `open` so the full fix-map gate applies again. The asymmetry argument is sound: a wrong hold ends at the cap, visible and bounded; a wrong clear is an invisible PASS. B also attacks the real residue of A, a CRITICAL typed `blocking: false` that passes, and its M2 pre-count of prior-line compliance costs nothing before any code is written.

## Strengths claimed for Variant A

1. **Default flow equivalence.** `panel.py:189-196` validates `apply_to` as a non-empty subset and `panel.py:600` resolves only the fixed slot unless the kind is in `apply_to`; both papers agree all 8 templates are `["first"]`. A re-review is one reviewer, so Q=1 and both variants demand that one reviewer's typed `prior resolved`. The only delta between A and B in the standard loop is the quote.
2. **The quote proves little.** B3 tests occurrence in `doc_text`. The prior line carries nothing tying the quote to the defect: `findings.py:175-186` parses `prior` and `status` only and keeps nothing else. A lazy reviewer quotes any line. The check catches fabrication, not laziness.
3. **The quote fails on the fix the loop prefers.** The revise brief says "Prefer deleting or narrowing text" (`document_review_loop_prompts.md:53`). A correct deletion removes the defective text, so there is nothing in the new text to quote. The reviewer quotes a neighbour (vacuous) or cannot quote (a false hold that feeds a cap escalation). B names no handling for this.
4. **Smaller blast radius, INV-C intact.** B needs the parser to carry a new key (`findings.py:186` appends only prior and status), an edited grammar line 61 plus line 70 plus the plugin mirror, quote normalisation B calls "module work", and hash plumbing in `apply_revision`. A edits the `ledger.py:254-258` loop and one clause at line 70. A adds no grammar.
5. **B6 misgrades the shipped rule.** Line 31 makes blocking require a sentence that "holds with no further assumption" and grades Medium any finding needing a guess "even when its label is MAJOR". B6 returns blocking for every MAJOR `contradiction`, `unpassable-check`, `data-loss`, `safety`, so a contradiction that needs a guess flips to blocking. `spec-panel.md:259` makes a MAJOR blocking when it names a concrete wrong outcome whatever its category, so B6's "`other` is non-blocking" is wrong in the other direction. The category is reviewer-typed too (`findings.py:102-103`), so authority is not moved off the reviewer, only onto a coarser field. The variant predicate B cites needs `wrong_outcome`, which findings-v1 does not have (`_check_finding`, `findings.py:90-121`, reads id, severity, blocking, category, anchor, anchor2, refs, claim). B concedes the flip risk itself (INV-J, MEDIUM).
6. **Pinned rule kept literally.** `test_prior_lines_never_change_a_status` (`test_review_ledger.py:318-338`) asserts prior lines on open rows change nothing. A keeps prior as an examination record and veto. B1 makes `prior resolved` clear a row and `prior open` set status; B's pin list (E7) omits this test.
7. **Better falsification design.** A's replay carries B's semantics as an arm, so it can show whether the cheap guard suffices. B's M1 compares only current against B.
8. **Auditability.** `held` events with a reason code and `unverified_ids` in the merge output are additive and explain each held row.

## Weaknesses identified in Variant B

1. Quote check is vacuous as evidence of examination (strengths 2 and 3), and adds a new false-hold source whose rate is unmeasured; B's own M2 is not run.
2. Adds grammar to a pinned line (`INS_B`, `test_review_rules_text.py:15` per B) while claiming INV-C only "MEDIUM".
3. The blocking predicate contradicts line 31 and `spec-panel.md:259` in both directions (strength 5), on a category list B tagged UNVERIFIED (S-002). I checked: the three blocking categories match line 31's three cases, but the "no further assumption" criterion is not encodable by category.
4. B7 records an expiry that "has no machine meaning": a field nothing reads.
5. B says it adds fields only, yet derives the verdict on read (VM-3). If `merge_round` still writes a stored `verdict`, a stale copy survives; B does not say.
6. Its `evidence` quote copies document text into ledger history; INV-H risk is rated LOW by B without a guard.

## Concessions

1. A's examination record is a self-report; a false affirmation clears as cheaply as silence. A shrinks the failure set but does not close it.
2. A leaves CRITICAL with `blocking: false` as PASS (`findings.py:98-101` rejects only MINOR plus blocking). A cheap script floor (CRITICAL is always blocking, per `spec-panel.md:259`) closes it with no category guess. A should take it.
3. **A dissent defect.** A holds a dissented row at `resolved_check`. `apply_revision` skips any row not in `open` or `regressed` (`ledger.py:328`), so a second fix on that row is ignored: no hunk-touch gate, no history event, and the status label is wrong. B's move to `open` or `regressed` is cleaner and A should adopt it. The pinned test's assertions still pass because its rows are already open.
4. Hash binding (B4) is real and A's "separate defect" dodge leaves `doc_text` unbound.
5. A's reopen-on-refind overrides a human park at every re-review, and a round-number expiry is almost meaningless under a 3-review cap (`_decision`, `ledger.py:93-96`). B's terminal deferral is simpler.
6. A's "complete reviewer" is `block_ok` only (`ledger.py:129, 147`). The `complete` completion state exists in `manifest.py:52` and `cluster_cmd.py:159`, not in this merge path. A reviewer that returns "incomplete" with a valid empty block still counts.
7. Both variants leave a held row invisible in detail: `render_merged_report` prints claim and anchor only for `brief_ids` (`ledger.py:438-466`), so the next reviewer sees a held row only in the table. A names `unverified_ids` in the merged report but not claim and anchor; B names neither. Both need the fix.

## Shared-assumption responses

- **A-001 (ids stable, prior keys the right row): QUALIFY.** The merged report prints lids in the table (`ledger.py:429-437`), but detail only for brief rows (point 7 above). The assumption holds for open rows and fails for held ones until the report lists them.
- **A-002 (examined text is `doc_text`): QUALIFY.** Nothing enforces it (`merge_cmd.py:99-109`); it holds only with B4's hash binding.
- **A-003 (ESCALATE is a safe terminal): ACCEPT.** `spec-panel.md:261` defines escalate-to-user at the cap as the terminal. Callers must read `ledger verdict` exit codes, since `merge` exits 0.
- **A-004 (reflect will not adopt the review ledger): QUALIFY.** True for this slot. If the unified panel makes reflect a consumer, INV-A, INV-B and DEGRADED interplay reopen; A takes no code from `derive_verdict`.
- **A-005 (C-03 independent): QUALIFY.** A takes Q as a parameter, so A's strength depends on C-03 more than B's does. In the one-reviewer default Q=1 and the point is moot.

## POINT POSITIONS

| ID | Superior | Conf | Evidence, and merge (U-points) |
|---|---|---|---|
| S-001 | TIE | 50% | Table versus bullets; presentation only |
| S-002 | A | 55% | B built B6 on a line it had not re-read; I verified line 31 |
| C-001 | HYBRID: A's gate (typed prior resolved from block_ok reviewers, same-round re-find wins) plus B's move to open or regressed on dissent | 65% | Default-flow equivalence; `ledger.py:328` dissent defect |
| C-002 | HYBRID: A's gate, with an optional non-gating `evidence` key recorded and an occurrence flag logged | 60% | Quote is vacuous and fails on deletions (`prompts:53`), but logging feeds M1 and A's own section 7 fallback |
| C-003 | B | 75% | `ledger.py:279` hashes unchecked text; `merge_cmd.py:99-109` |
| C-004 | HYBRID: A's typed authority plus a CRITICAL floor; keep `blocking_typed` and report disagreement; no category predicate | 65% | Line 31 and `spec-panel.md:259`; `findings.py:98-101` |
| C-005 | B | 60% | Row state honest on dissent; pin assertions survive (`test_review_ledger.py:318-338`) but its rule name needs restating |
| C-006 | TIE | 50% | Owner and reason required in both; expiry weak under a 3-review cap |
| C-007 | B | 55% | Both close the wrong PASS by counting deferred as open; B respects the human park |
| C-008 | TIE | 50% | Hybrid C-001 puts dissent rows in `brief_ids` naturally |
| C-009 | B | 55% | Additive fields are safer for old readers; A concedes MEDIUM (`ledger.py:363-372`) |
| C-010 | HYBRID: A's three-arm replay plus B's M2 and M3 | 65% | A includes the opposing arm; M2 is free |
| C-011 | A | 65% | One clause at line 70 versus lines 61 and 70 plus mirror |
| X-001 | A | 55% | Assertions at `:318-338` survive both; A keeps the rule literal |
| X-002 | A | 60% | Occurrence is not examination; B concedes not proof |
| X-003 | TIE | 55% | Q=1 default makes A's gate B's minus the quote |
| X-004 | A | 70% | B6 flips shipped grading; `wrong_outcome` absent from findings-v1 |
| U-001 | A | 60% | Veto, `held` reason codes, `unverified_ids`; YES |
| U-002 | HYBRID: record `expires_round` as an audit field, no automatic reopen | 45% | Pure-function point valid; reopen weak at cap 3; YES (audit only) |
| U-003 | TIE | 55% | B7 refuses the same rows; A's D-11 A/B/C cases are the better test list; YES |
| U-004 | A | 70% | Replay with the opposing arm; YES |
| U-005 | B | 75% | Hash binding independent of clearing semantics; YES |
| U-006 | HYBRID: keep `blocking_typed` and the disagreement warning; drop the predicate flip and the optional grader | 60% | Warning is cheap data for M3; the predicate misgrades; YES (partial) |
| U-007 | TIE | 55% | Both fail closed (A's INV-I row); YES as a stated principle |
| U-008 | B | 70% | Free pre-count of prior-line compliance; YES |
| U-009 | B | 55% | More detailed rf-qa mapping; A gives the same derivable input; YES (partial) |
| U-010 | TIE | 60% | Asymmetry applies equally to A; YES as shared rationale |
| A-001 | TIE | 60% | QUALIFY: held rows lack detail in the merged report |
| A-002 | B | 65% | QUALIFY: only B4 enforces the text binding |
| A-003 | TIE | 65% | ACCEPT: cap escalation is the defined terminal |
| A-004 | TIE | 60% | QUALIFY: holds for this slot only |
| A-005 | B | 55% | QUALIFY: A's Q ties it to C-03; B needs no count |
