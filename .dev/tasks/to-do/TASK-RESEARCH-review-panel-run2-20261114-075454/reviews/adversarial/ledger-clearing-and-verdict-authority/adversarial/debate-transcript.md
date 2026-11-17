# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel, Round 2 sequential A then B) plus Round 2.5 invariant probe (independent fault-finder; see invariant-probe.md)
- Convergence achieved: 95.5% (21 of 22 diff points; S-002 unresolved)
- Convergence threshold: 80%
- Focus areas: correctness, risk, test-coverage
- Advocate count: 2 (Variant A advocate, Variant B advocate; both general-purpose agents, no model or persona override)
- Taxonomy coverage: L1 surface (S-001, S-002, C-011) covered; L2 structural (C-004, C-008, C-009, C-010, X-004, A-004) covered; L3 state mechanics (C-001, C-002, C-003, C-005, C-006, C-007, X-001, X-002, X-003, A-001, A-002, A-003, A-005) covered. No forced round needed.
- Orchestration note: the first Round 1 dispatch of both advocates returned no result to the orchestrator (no transcript file arrived); both advocates were re-dispatched with an assigned output file (round1-A.md, round1-B.md). Round 2 was run in sequence (A then B) with B reading A's file. The Round 1 and Round 2 statements below are the advocates' files verbatim.
- Omission check (A-001..A-005 responses): Advocate A answered all five in Round 1; Advocate B answered all five in Round 1. No [OMISSION] flags.

---

## Round 1: Advocate Statements

### Variant A Advocate (general-purpose agent; source file round1-A.md)

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


### Variant B Advocate (general-purpose agent; source file round1-B.md)

# Round 1 - Advocate for Variant B (slot C-02, ledger clearing and verdict authority)

## Position

A row must leave the open-equivalent states only on a mechanically checkable, attributed answer, and the checks must gate (fail closed), not warn. B is the better base for correctness and test-coverage because its guard has deterministic negative tests and does not depend on the quorum slot (C-03). I concede that B's blocking predicate and its status-writing `prior` rule need narrowing, and I name the narrowed forms below.

## Steelman of Variant A

A is the smaller, safer-looking change. It keeps the shipped grammar (no new `evidence` key, `findings.py:175-186` untouched) and keeps the pin `test_prior_lines_never_change_a_status` true in letter (`tests/review/test_review_ledger.py:318-338`). It leaves blocking authority with the reviewer, which matches the master loop's "grade by consequence" prose being delivered to reviewers (`document_review_loop_prompts.md:31`). It adds a counted-absent-reviewer rule through `--resolution`, which B does not address. Its `defer` carries owner and a round-number expiry so the read stays a pure function of the file. Its re-find of a deferred row returns it to `open`, so the loop can act on it again while `n < cap`. Its replay design includes B's semantics as a measured arm and states what would show A has the wrong strength (A section 5, item 4). Its candour is real: A's section 7 admits that a typed `resolved` is a self-report and that its own residue is the false affirmation. Because it is additive and keeps today's one-pass shape, it is the lower-regret choice if no measurement ever arrives.

## Strengths claimed (B)

1. **The default flow defeats A's guard; it does not defeat B's.** `panel.py:600` keeps only the fixed slot for a re-review unless `apply_to` lists it, and all 8 packaged templates carry `"apply_to": ["first"]` (grep: count 1 in each of the 8 `review-panel.*.json` files, re-run this session). So a re-review is one reviewer. With one reviewer, A's "at least Q complete reviewers typed `prior resolved`" is a free JSON line: the parser reads only `prior` and `status` (`findings.py:175-186`), so there is nothing to check. A's own section 3.1 item 4 says the examination record, not the count, does the work in the default flow. Also, zero valid blocks is already refused at `ledger.py:150-157`, so the quorum adds nothing at Q=1. B's `evidence` quote adds a check the ledger can run.
2. **The quote is not a new burden; the shipped brief already makes the reviewer produce quotes.** `document_review_loop_prompts.md:44` has the reviewer copy changed lines verbatim into BEFORE/AFTER and decide each prior blocker "by comparing its defect with the AFTER text only"; `:46` tells it to `grep -nF` each quote. Nothing machine-checks that today. B3 turns an existing prose self-check into a gate, using the occurrence test the anchor path already uses (`ledger.py:136`, `fnd.annotate`).
3. **Text binding has precedent in the same file.** `apply_revision` refuses a mismatched `--old` hash (`ledger.py:308-314`). `merge_round` only records `sha256_text(doc_text)` (`ledger.py:279`). B4 is the symmetric one-line check. A calls this "a separate defect" (A section 3.1 item 3), but without it any answer about "the new text" certifies text the ledger never saw (A-002).
4. **B ties down the dissent path; A leaves a bookkeeping hole.** A holds a dissent row at `resolved_check` and puts it in `brief_ids`. But `apply_revision` skips every row not in `open|regressed` (`ledger.py:328`). The reviser's fix of that row would be silently ignored (no `named_not_touched`, no `rejected_by_reviser`). A does not amend `apply_revision`. B moves a dissent row to `open`/`regressed`, which the existing code handles.
5. **B does not need C-03 to be decided.** A's strength is its Q parameter (A-005). B's rule is per row: one valid-block answer with a checkable quote, no re-find, bound text.
6. **Verdict authority gap is real and A leaves it.** `findings.py:100-101` rejects only MINOR with `blocking: true`. A `CRITICAL` with `blocking: false` is accepted and passes. `spec-panel.md:259` (bullet 2) says "CRITICAL is blocking". A cites `:262` as authority for the deferred rule but accepts the opposite on `:259`, and A's own objection section cites measured typed-blocking accuracy of 0/8 and 0.17 (research/08, not re-read here). The package already has a script rule for the reflect lens (`findings_v2.py:161-162`, re-read: `blocking != (severity != "MINOR")` is rejected).
7. **Test-coverage.** B's guard has deterministic negatives: quote absent from `doc_text`, hash mismatch, invalid-block reviewer, answer plus re-find. A's residue (a lazy "resolved") has no deterministic negative test; a test cannot tell a lazy yes from an examined yes.
8. **Additive file shape.** B only adds fields (`verify_ids`, `held_ids`, `new_sha256`). A removes `verdict`, `decision`, `brief_ids` from round records and concedes that old code reading a new file fails at `last["verdict"]` (`ledger.py:363-372`).

## Weaknesses identified in Variant A

1. Self-report only: the false-affirmation path is as cheap as silence in the default one-reviewer flow (strength 1). A's reply, that the removed failure set is larger than the residue, is true for the three reproduced paths but leaves the likeliest real failure (a rubber-stamp yes) unguarded and untestable.
2. Dissent bookkeeping bug at `ledger.py:328` (strength 4).
3. `expires_round` is nearly inert. `_decision` gives ESCALATE at `n >= cap` (`ledger.py:93-96`) and VM-6 refuses any later round. The documented defect case, D-11 C, is a `defer` at round 3. There is no later round for the expiry to fire in. At rounds 1-2 an expiry of the next round returns the row to `open` before a human could have meant it to.
4. Re-find reopens a deferral a human made on purpose. That overrides an explicit accepted-risk decision with a machine event. B keeps the row terminal and counted open (so the verdict is never PASS), and surfaces the re-find.
5. Leaves text binding open, and removes stored round fields (strengths 3 and 8).
6. Leaves `CRITICAL`+`blocking:false` passing (strength 6).

## Concessions

1. **The quote proves reading, not fixing.** A reviewer can quote any AFTER line. A deletion fix cannot be quoted at all (the defective text is gone), and the revise brief prefers deletion (`document_review_loop_prompts.md:53`). B3 gains power against wrong-text and non-reading, not against wrong judgement. Narrowing available: require the quote to fall inside the row's current mapped span (`ledger.py:343-346` keeps spans current) or, when the span is `None`, accept any quote from the changed region. M1 measures the real gain.
2. **B6's category map does not equal the grading check.** I re-read `findings.py:15-22` (the six categories B names exist) and `document_review_loop_prompts.md:31`. The check blocks on a contradiction, data loss or a safety break, or an unpassable acceptance criterion, but only when the sentence holds "with no further assumption". It grades Medium when a guess is needed. A `contradiction` that needs a guess is Medium; a category predicate returns blocking (false block). A security-boundary risk typed `other` returns non-blocking (false pass); `spec-panel.md:259` makes that blocking. Category is necessary, not sufficient. Narrowing: the core enforces only the floor (`CRITICAL` => blocking, parser-side, as `findings_v2.py:161-162` does), keeps the typed value for MAJOR, and the lens predicate reports disagreement as a warning until M3 shows the flip rate.
3. **B1 breaks the name of a pinned test, and B's pin list omits it.** Under B, `prior` changes status (`resolved_check -> resolved`, `open|regressed` set). The assertions of `test_prior_lines_never_change_a_status` (L4 and L2 stay open, `prior_note` kept) probably still pass, because those rows are not `resolved_check`; the rule the name states is false. A keeps it true. Narrowing: only the clearing transition is prior-driven; a dissent routes the row to `open`/`regressed` through the ledger.
4. **B5 can produce REVISE with an empty Reviser brief** when only `verify_ids` remain. That burns a review (cap 3) with nothing to revise. It should be a re-review without a reviser pass, and the escalation text at `ledger.py:482` lists only `brief` ids, so held-only or unverified-only states print an empty list.
5. **Unlisted work, shared with A.** `render_merged_report` (`ledger.py:432-466`) shows a `resolved_check` row only as a table line (no claim, no anchor); the detailed section covers only `brief_ids`. The re-reviewer asked to answer `prior L1 resolved` does not see what L1 said. Both variants need this render change; B's paper understates its cost.
6. **No measurement exists.** M2 (prior-line compliance in existing re-review reports) was not run. If compliance is low, B converts silence into cap escalations.

## Shared-assumption responses

- **A-001: QUALIFY.** Ids are stable (`render_merged_report` prints the `lid` table, `ledger.py:432-437`). But a `resolved_check` row carries no claim text in the report (`ledger.py:438-466`), and an unknown id yields only a warning (`ledger.py:263`). Needs a render change for both variants.
- **A-002: REJECT.** The ledger does not bind the merged text to the revision output: `merge_round` only hashes it (`ledger.py:279`); only the old side is checked (`ledger.py:308-314`).
- **A-003: QUALIFY.** ESCALATE is safe only if the report names the held rows; `ledger.py:482` lists `brief` ids only.
- **A-004: ACCEPT** for this slot (no import between `cli/review` and `cli/reflect`, per both papers' greps; I did not re-run that grep). It would need re-opening if a unified panel makes reflect a ledger consumer.
- **A-005: QUALIFY.** True for B (per-row rule). False for A: its guard strength is Q, and at Q=1 in the default flow it is a free line.

## POINT POSITIONS

| ID | Superior | Conf. | One clause of evidence | Incorporate (U-points) |
|---|---|---|---|---|
| S-001 | TIE | 85% | Layout only; no behavioural content | n/a |
| S-002 | B | 65% | A tags second-hand claims "CODE-VERIFIED via research"; B tags honestly, though its `:31` claim checked out when re-read | n/a |
| C-001 | HYBRID: B's answer rule plus A's `held` reason codes | 70% | One-reviewer default makes A's count vacuous (`panel.py:600`, 8/8 templates `["first"]`) | n/a |
| C-002 | B | 70% | Quote is checkable; shipped brief already produces quotes (`prompts.md:44,46`); concession 1 on its limit | n/a |
| C-003 | B | 80% | Symmetric to `apply_revision` hash check (`ledger.py:308-314`) | n/a |
| C-004 | HYBRID: enforce CRITICAL=>blocking floor, keep typed MAJOR, lens predicate as warning | 60% | `findings.py:100-101` lets CRITICAL+false pass; category map overshoots `prompts.md:31` | n/a |
| C-005 | B | 72% | A's dissent rows stay `resolved_check` and `apply_revision` skips them (`ledger.py:328`); concession 3 on the pin name | n/a |
| C-006 | HYBRID: B's terminal-and-counted, expiry recorded as metadata | 60% | Expiry cannot fire at the cap (`ledger.py:93-96`) | n/a |
| C-007 | B | 55% | Keeps a human's accepted-risk decision; verdict still FAIL/ESCALATE; A's reopen is more loop-forward while `n < cap` | n/a |
| C-008 | B | 65% | `verify_ids` not in the Reviser brief; dissent goes to `open` anyway | n/a |
| C-009 | B | 60% | Additive fields vs A removing stored round fields (A concedes old-reader failure) | n/a |
| C-010 | HYBRID: B's M2/M3 plus A's three-arm replay | 65% | M2 is free; A's opposing arm is the cleaner experiment | n/a |
| C-011 | TIE | 55% | Both keep pinned text; B's edit is larger but states the rule | n/a |
| X-001 | A | 65% | Name of the pin stays true under A; B's pin list omits it (concession 3); A's own hole is `ledger.py:328` | n/a |
| X-002 | B | 60% | Attributed and mechanically testable, though not proof of a fix (concession 1) | n/a |
| X-003 | B | 65% | A's quorum is vacuous at Q=1 and depends on C-03; `ledger.py:150-157` already refuses zero valid blocks | n/a |
| X-004 | HYBRID: floor plus warning | 60% | Six categories verified (`findings.py:15-22`); `prompts.md:31` Medium clause ("needs a guess") is not category-expressible | n/a |
| U-001 | A | 60% | Reason codes and `unverified_ids` are cheap and useful | YES |
| U-002 | B | 60% | Round-number expiry inert at the cap and VM-6 | NO |
| U-003 | TIE | 85% | Both refuse `defer` on non-blocking-open rows; A's D-11 cases are good tests | YES |
| U-004 | A | 70% | Including the opposing semantics as a measured arm is honest design | YES |
| U-005 | B | 85% | Closes the unbound-`doc_text` gap (`ledger.py:279`) | YES |
| U-006 | HYBRID | 60% | Keep `blocking_typed` and the optional grader; narrow to the floor plus warning (concession 2) | YES (narrowed) |
| U-007 | B | 80% | Gating, not warning; matches the `stoprule.py` "silence never passes" lesson per B's E15 (not re-read) | YES |
| U-008 | B | 85% | Free to run before any code is written | YES |
| U-009 | B | 60% | rf-qa regression and monotonicity guards need per-item recorded state (`rf-qa.md:403-415` per B) | YES |
| U-010 | B | 70% | Bounded visible cap escalation versus an invisible wrong PASS | YES |
| A-001 | QUALIFY | 75% | See above | n/a |
| A-002 | REJECT | 85% | See above | n/a |
| A-003 | QUALIFY | 70% | See above | n/a |
| A-004 | ACCEPT | 75% | Papers' greps; not re-run | n/a |
| A-005 | QUALIFY | 75% | See above | n/a |


---

## Round 2: Rebuttals (sequential)

### Variant A Rebuttal (source file round2-A.md)

# Round 2 rebuttal, Advocate for Variant A (slot C-02, ledger clearing and verdict authority)

Date: 2026-11-14. Cited lines were re-read this session: `ledger.py` 1-80 and 80-494, `merge_cmd.py` whole, `ledger_cmd.py` whole, `findings.py` 90-196, `document_review_loop_prompts.md` 26-75, `spec-panel.md` 254-265, `tests/review/test_review_ledger.py` 316-339, `panel.py` (grep of `apply_to`). Not re-read: synth-06 (so I do not quote VM-3's exact wording), `stoprule.py`, research files.

## 1. Replies to the criticisms of A in round1-B.md

| B's criticism of A | Reply |
|---|---|
| W1 / strength 1: in the one-reviewer default, A's gate is "a free JSON line"; a rubber-stamp yes is untestable | Concede the residue. Two things stay true. Without a quote, A's gate still removes the three reproduced non-dishonest paths (unrelated empty block clears; invalid-block reviewer clears; absent reviewer counts). And B's quote does not remove the rubber stamp either: B conceded it proves reading, not fixing (B Concession 1). B's own narrowing ("when the span is None accept any quote from the changed region") makes the check vacuous exactly where `map_span` returns None for a deletion (`ledger.py:345-346`). |
| Strength 2: the shipped brief already makes the reviewer produce quotes, so a gate on them is free | Partly wrong. The quotes at `prompts.md:44, 46` are diff lines copied into the report's BEFORE/AFTER block for a role-swap self-check. The prior line at `prompts.md:61` carries no quote, and `findings.py:186` keeps only `prior` and `status`. A per-row quote is new reviewer work, not an existing one turned into a gate. |
| W2 / strength 4: dissent bookkeeping, `apply_revision` skips non-open rows (`ledger.py:328`) | Concede. Confirmed: `if row["status"] not in ("open", "regressed"): continue`. A held row left in `resolved_check` would swallow the next fix silently. Fixed in section 4 (C-001). |
| W3: `expires_round` is nearly inert under the cap | Concede with a stronger reason than B gave (section 3, new evidence 5). |
| W4: re-find reopening overrides a human park | Concede. Row stays `deferred` (C-007). |
| W5 / strength 3 and 8: text binding left open; stored fields removed | Concede text binding (C-003). Concede the file-shape point in part (C-009). |
| W6 / strength 6: CRITICAL with `blocking: false` passes | Concede. A's own round 1 said it would not touch it; `spec-panel.md:259` says "CRITICAL is blocking". Floor adopted (C-004). |
| Strength 7: deterministic negative tests exist for B's guard but not for a lazy yes | True and not answerable: no test separates a lazy yes from an examined yes. A's guard has its own deterministic negatives (dissent, invalid-block answerer, absent reviewer, re-find in same round), so it is testable, only weaker. |

## 2. Updated assessment of B

B is better than A on: text-hash binding; the state a dissent row takes; not reopening a human park; the free M2 pre-count; additive file shape; the fail-closed stance that the answer must gate, not warn. B is not better on the quote as a gate and not better on the category predicate. B has now conceded both in its own round 1 (Concessions 1 and 2), so the two papers differ in the merged design only on whether the `evidence` key is recorded. I accept from B: B2 (only valid-block answers count), B4 (hash binding), B5's three lists, B7 (terminal deferral), U-007 as a stated principle, M2, M3.

## 3. New evidence not yet presented (all re-read this session)

1. **Priors from invalid-block reviewers are collected.** `parse_block` appends a valid prior line to `res["priors"]` (`findings.py:186`) even when other lines make `ok` false (`:190`). `merge_round` collects every prior with no `block_ok` test (`ledger.py:139-140`). So any prior-driven gate must filter by `block_ok[reviewer_id]`; B2 is necessary, not optional.
2. **Priors are not de-duplicated.** `seen` guards only finding ids (`findings.py:159, 193`), so one reviewer can type `resolved` and `open` for one lid. Rule needed: any `open|regressed` from a valid reviewer beats any `resolved`.
3. **Order of operations.** The clearing loop (`ledger.py:254-258`) runs before the prior loop (`:259-272`). A prior-gated clear needs the prior map built first; this is a reorder, not an addition.
4. **A same-round re-find already beats a `resolved` answer.** A re-found `resolved_check` row becomes `regressed` at `ledger.py:235-238`, before the clearing loop tests `status == "resolved_check"`. B's "re-find wins" clause needs no new code.
5. **Expiry is inert for a stronger reason.** Deferred rows are already outside `_brief_ids` (`ledger.py:99-104`), and when only deferred rows remain both papers return ESCALATE, after which VM-6 refuses further rounds. A deferral therefore never meets a later round in which an expiry could fire.
6. **The module docstring states the pinned rule too** (`ledger.py:3-4`: "a reviewer's own prior lines are recorded as notes and never change one"). Any dissent routing that moves a row changes that sentence, not only a test name.
7. **A's round-1 claim about `--resolution` was overstated.** `merge_cmd.py:73-83` reads `reviewers` only to build a `models` map; requested ids are not counted anywhere. Counting requested-but-absent reviewers is new code in `merge_cmd.py`.
8. **A quorum deadlock if C-03 sets Q above the re-review panel size.** Re-review resolves one reviewer by default (`panel.py:600`, `apply_to` validated at `:189-196`; all 8 templates `["first"]` per both papers). A fixed Q of 2 would make a one-reviewer re-review unable to clear any row, so every loop ends at the cap.
9. **The empty-diff trap for a verify-only retry.** `prompts.md:44` and `spec-panel.md:262` say an empty diff leaves every prior blocker open. A retry that asks only for missing prior lines must therefore reuse the same BASELINE and CANDIDATE (non-empty diff), not a second `revise` with an empty fix map.
10. **No existing review test pairs CRITICAL with `blocking: false`** (grep of `tests/review` found none, a pattern-limited check), so a CRITICAL floor breaks no pin by that search.
11. **A parser-side CRITICAL floor would be wrong.** A parser error sets `ok` false and drops the line (`findings.py:188-192`); that is the C-06 whole-line-drop cost A named. The floor belongs in `merge_round`.
12. **Only `defer` and `verdict()` read round-record `verdict`/`decision`/`brief_ids`** inside `cli/review` (grep: `ledger.py:358-370`, `ledger_cmd.py:109`).

## 4. Final positions (the exact rule for the merged design)

**C-001 Clearing gate and dissent state.** A `resolved_check` row becomes `resolved` in `merge_round` only if (a) the count of `block_ok`-true reviewers that typed `prior <lid> resolved` is at least `need = min(Q, number of reviewers requested this round)`, (b) no `block_ok`-true reviewer typed `open` or `regressed` for it, and (c) it is not re-found this round. Build the prior map before the clearing loop. A `block_ok`-true `open|regressed` prior moves a `resolved_check` row to `regressed` (history event `dissent`), the route a re-find already takes, so `apply_revision` accepts it (`ledger.py:328`) and `brief_ids` picks it up (`:103`). `open` and `regressed` are one signal to the ledger. A row failing the gate without dissent stays `resolved_check` and is listed in `verify_ids`. Silence never clears. Priors never move a row that is not `resolved_check`.

**C-002 The `evidence` quote.** Recorded only, never gating, optional. The parser keeps an optional string `evidence` on a prior line (one-line change at `findings.py:186`); the ledger puts it in the `prior_note` event with a boolean `quote_in_doc`. It does not gate because the deletion fix, which the revise brief prefers (`prompts.md:53`), leaves nothing in the new text to quote, so a gate would hold correct deletions and feed cap escalations; and a lazy reviewer can quote any line. The recorded flag is the data M1 needs to show whether a gate would add power. If B's measurement later shows it does, promote it to a gate only with a deletion carve-out (a quote from BASELINE absent from CANDIDATE).

**C-003 Text-hash binding.** Adopt B4. `apply_revision` stores `pending_new_sha256 = sha256_text(new_text)` as a top-level ledger key; `merge_round` refuses (LedgerError, ledger unchanged) when it is set and `sha256_text(doc_text)` differs, then clears it. `load` accepts extra top-level keys (`ledger.py:47-48`), so this is additive. If `revise` was never run, no check applies; that gap cannot be closed in the ledger.

**C-004 Blocking authority.** Typed `blocking` stays the authority, plus a CRITICAL floor applied in `merge_round` (not the parser): `blocking = typed or severity == "CRITICAL"`; member records keep `blocking_typed`; each flip adds a warning (`CRITICAL typed non-blocking, floor applied`). No category predicate, no grader in the core, `verdict:` line stays parser-neutral. Declared risk: `prompts.md:31, 60` tell reviewers to type `blocking` only after the grading check, while `spec-panel.md:259` says CRITICAL is blocking; the floor chooses the second. The warning count is M3's data. A lens that wants a stricter rule may add one later.

**C-005 / X-001 The pinned test.** The module docstring (`ledger.py:3-4`), the test name and the rule are restated: "A prior line never changes the status of a row that is not `resolved_check`. On a `resolved_check` row it is the only reviewer input accepted as an examination answer: `resolved` is a precondition of the merge-loop clear, `open|regressed` routes to `regressed`." `test_prior_lines_never_change_a_status` (`test_review_ledger.py:318-338`) keeps passing unchanged, because L4 and L2 are `open` rows; it should be renamed, and new tests added for the `resolved_check` cases. I concede the name read literally is too broad.

**C-006 Defer.** `defer` requires `--owner` and `--reason`; allowed only on a blocking row in `open`, `regressed` or `resolved_check`; touches no round record; row is terminal for the machine and counts open. No expiry field in the core: nothing would read it (evidence 5). A lens with a wall-clock policy may add metadata.

**C-007 Re-find of a deferred row.** Stays `deferred`; the existing `refound` history entry (`ledger.py:232`) stays and the merge result lists `refound_deferred`; the Escalation text lists it.

**C-008 Outputs and the empty-brief REVISE.** `brief_ids` = blocking `open|regressed`; `verify_ids` = blocking `resolved_check`; `held_ids` = blocking `deferred`. PASS only when all three are empty; else FAIL, REVISE below the cap, ESCALATE at the cap or when only `held_ids` remain. Exit codes stay 0/10/11 (`ledger_cmd.py:13`). When `brief_ids` is empty and `verify_ids` is not, the decision stays REVISE (no new exit code) but the Reviser-brief section prints "no revision needed; re-review the same candidate against the same baseline to answer: L1, L3" and `ledger verdict` adds an additive `next` field (`re-review` or `revise`). The retry uses the same BASELINE and CANDIDATE (evidence 9). It costs one review of the cap; that is accepted and bounded.

**C-009 File shape.** Additive. Round records keep writing `verdict`, `decision`, `brief_ids` as a merge-time snapshot that nothing reads (only `verdict()` and `defer` read them, evidence 12); `verdict()` computes from rows; `defer` stops writing them. New fields: `verify_ids`, `held_ids`, `pending_new_sha256`, `blocking_typed`, `owner`. Schema string kept. Conditional: if synth-06 VM-3 literally says "never stored", drop the three snapshot keys instead and keep readers tolerant of old files (A's round-1 form). Whether `review-ledger/2` is needed stays open (LG-2).

**`render_merged_report` gap (`ledger.py:438-466`, `:482`).** Both papers need it. The detailed section prints claim and anchor for every row in `brief_ids + verify_ids + held_ids` under three headings, and the Escalation paragraph lists all three lists (today it lists `brief` only). Open point: whether PRIOR in the re-review brief is this merged report or a single reviewer report; I did not verify it, and if it is a single report the verify rows must be restated in the re-review brief instead.

**A-005 and C-03.** Independent except for one parameter: C-02 owns `need = min(Q, requested)`, C-03 owns Q and the round-1 partial-panel rule. The `min` prevents the deadlock in evidence 8. Counting requested reviewers needs `merge_cmd` to pass the `--resolution` reviewer ids into `merge_round` (evidence 7); without `--resolution`, requested is the reports passed.

## 5. Positions changed since Round 1

| ID | Old (round 1) | New | Why |
|---|---|---|---|
| C-001 | HYBRID: A's gate; dissent withholds at `resolved_check` | Dissent routes to `regressed`; gate uses `need = min(Q, requested)` | `ledger.py:328` skips non-open rows; deadlock risk (evidence 8) |
| C-002 | HYBRID: non-gating key with an occurrence flag | Unchanged in substance, now specified: parser keeps key, `quote_in_doc` flag, promotion rule with deletion carve-out | `prompts.md:53` deletion problem; B conceded the same limit |
| C-004 | HYBRID: typed plus CRITICAL floor | Floor lives in `merge_round`, not the parser | `findings.py:188-192` drops the line and invalidates the block |
| C-005 / X-001 | A: pinned rule "stays true" | Rule narrowed to rows not in `resolved_check`; test renamed; docstring edited | `ledger.py:3-4`; dissent now writes a status |
| C-006 | A: `expires_round` that reopens the row | No expiry in the core | evidence 5 |
| C-007 | B (kept my earlier concession) | B: stays `deferred`, `refound_deferred` surfaced | unchanged from round 1 table, now with the Escalation-text requirement |
| C-009 | B (additive) | Additive snapshot kept, with a VM-3 conditional | evidence 12; synth-06 not re-read |
| A-005 | B | Independent except `need = min(Q, requested)` | evidence 8 |
| C-003 | B | B, specified as a top-level `pending_new_sha256` | `ledger.py:47-48` tolerates new keys |
| Round-1 claim | `--resolution` "already carries" requested ids for counting | Corrected: counting is new code | `merge_cmd.py:73-83` |


### Variant B Rebuttal (source file round2-B.md; read A rebuttal first)

# Round 2 rebuttal, Advocate for Variant B (slot C-02, ledger clearing and verdict authority)

Date: 2026-11-14. Re-read this session: `ledger.py` 1-494, `findings.py` 85-196 and 276-298 and 340-457, `findings_v2.py` 140-179, `merge_cmd.py` whole, `ledger_cmd.py` whole, `panel.py` 186-199 and 590-610, `document_review_loop_prompts.md` 26-75, `spec-panel.md` 254-265, `tests/review/test_review_ledger.py` 15-40, 66-88, 316-340, 518-546 and grep hits, `synth-06-conflict-log.md` VM-3/VM-6 rows (178, 181, 400), all five adversarial papers. Not re-read: `test_review_rules_text.py`, `stoprule.py`, research files, `locate` past line 298.

## 1. Replies to the criticisms of B (round1-A.md, round2-A.md)

| Criticism | Reply |
|---|---|
| A-R1 W1/W2: the quote is not evidence of examination and adds an unmeasured false-hold source | Concede, and act on it (C-002 below). New reason beyond A's: the span a row carries is lossy for replacements (`findings.py:431` docstring "maps to the start of its new range"; the author's own comment at `ledger.py:224-225` says a defect can sit farther down the replacement), so a span-restricted quote check, my round-1 narrowing, falsely holds long replacements. A deletion leaves no AFTER text to quote at all. |
| A-R2 §1: "B's narrowing is vacuous exactly where `map_span` returns None for a deletion (`ledger.py:345-346`)" | **Wrong reason, right conclusion.** `map_span` returns `None` only when the input span is `None` (`findings.py:434-435`); a deleted line maps to `(j1, j1+1)`, the line after the deletion (`findings.py:419-427, 439`). And a row can reach `resolved_check` only if `hunks_touch` is true on `span` or `span2` (`ledger.py:331-333`), and `hunks_touch(None)` is false (`findings.py:446-447`), so a reached row always has a live span. The check is not vacuous there; it is satisfiable by quoting a neighbour, which is the same "proves reading, not fixing" limit I conceded in round 1. |
| A-R2 §1: the shipped quotes (`prompts.md:44,46`) are diff lines for a role-swap check, not per-row quotes | Concede. My round-1 strength 2 was overstated. The AFTER lines exist; a per-row quote is new reviewer work. |
| A-R1 W3 / A-R2: B6 predicate misgrades line 31 and `spec-panel.md:259` | Concede, re-read `prompts.md:31`: Medium "even when its label is MAJOR" is not category-expressible. Predicate dropped (C-004). |
| A-R1 W4: B7 expiry "has no machine meaning" | Concede; no expiry in the core (C-006). |
| A-R1 W5: B derives the verdict on read but may leave a stored copy | Concede, and VM-3 is stricter than I treated it (C-009). |
| A-R1 W6 / INV-H: quote copies document text into history | Mitigated, not removed: `evidence` bounded at 200 characters and never copied into telemetry (anchors already live in rows). |
| A-R1 W2 / X-001: B1 breaks the pinned rule and B's pin list omits the test | Concede. Re-read `test_review_ledger.py:318-338`: its assertions (L4, L2 stay `open`) survive, the stated rule does not. B1 also wrote "`prior open` sets the row" for any row, which would let a hearsay line reopen a human-deferred row, the thing I attacked A for. Narrowed (C-005). |

## 2. Updated assessment of A's final positions

**Accept**: need gate with `block_ok` filter, priors map built first, dissent routed to `regressed`, no quote gate, CRITICAL floor in `merge_round`, no expiry, terminal deferral with `refound_deferred`, `verify_ids`/`held_ids` and the `next` field, `pending_new_sha256`.

Checks of A's new claims (all hold unless noted):
- Priors from invalid-block reviewers are collected: `findings.py:186` appends before `ok` goes false at `:190`; `ledger.py:139-140` collects without a `block_ok` test. Confirmed.
- Priors not de-duplicated: the prior branch `continue`s at `findings.py:187`, before `seen.add` at `:193`. Confirmed. Count distinct reviewers, not lines.
- Clear loop runs before the prior loop (`ledger.py:254-258` vs `:259-272`). Confirmed. Also `lid not in members_by_lid` is redundant: a re-found row was already set to `regressed` at `:235-238`, so any row still `resolved_check` at `:254` was not re-found.
- `apply_revision` skips non-open rows (`ledger.py:328`). Confirmed.
- `--resolution`: A's correction is right (`merge_cmd.py:73-83` builds only a model map), but the ids are in hand there; the real gap is that `--resolution` is optional (`merge_cmd.py:50-56`).
- No test pairs CRITICAL with `blocking: false`: confirmed for the ledger tests. `fl` defaults `severity="CRITICAL"` (`test_review_ledger.py:28`), but all four `blocking=False` calls pass `severity="MINOR"` (`:77-78, :313, :537-538, :560`). Caveat: a future `fl(..., blocking=False)` without severity hits the floor.
- Parser-side floor wrong: confirmed (`findings.py:188-192` drops the line and sets `ok` false).
- Only `defer` and `verdict()` read stored round keys in `cli/review` (grep outside reflect: `ledger.py:358-370`, `ledger_cmd.py:109` through `verdict()`). Tests do read them (`test_review_ledger.py:133-134`, and `:280-298` where the variable source was not re-read).
- **CRITICAL floor vs `findings_v2.py:161-162`: no conflict.** That rule applies only when `reflect_category` is set and demands `blocking == (severity != "MINOR")`, so CRITICAL must be blocking there too; the floor is a subset. They differ in action (v2 returns an error; the floor flips and warns), one behaviour per lens, a minor inconsistency.
- **VM-3 exact wording** (`synth-06-conflict-log.md:178`, repeated `:400`): "The verdict is derived from rows on every read and is never stored", status DECIDED-BY-EVIDENCE [CODE-VERIFIED]. A's primary C-009 form (keep a merge-time snapshot of `verdict`, `decision`) is a stored verdict under another name, so A's own conditional fires. I take the drop form.
- VM-6 is decided but unbuilt: `merge_round` checks only `n == len(rounds)+1` (`ledger.py:114-118`); the row is a "plan item" (`synth-06:181`). A's evidence 5 holds only once it lands; I supply a derived form in C-008.

**Still dispute**: (a) A's fallback "without `--resolution`, requested is the reports passed" silently weakens the gate; (b) A is silent on `revise` non-idempotency (section 3); (c) A's primary C-009 form.

## 3. New evidence

1. **`ledger revise` is not idempotent.** `ledger.py:343-347` maps every row's span through the old-to-new opcodes on each call; a second call with the same files re-maps spans already in new coordinates (nothing checks that a revision is pending; the old-hash check at `:308-314` passes again). C-003's recovery from a hash mismatch invites exactly that re-run. The pending hash is the natural guard.
2. **`locate` already solves quote normalisation** (`findings.py:276-298`: whitespace-flattened, returns half-open 0-based line ranges). The record-only flag is one call; my round-1 "module work" hand-wave was unneeded.
3. **A bad optional key must not be able to kill a line.** Any parser error drops the line and sets `ok` false (`findings.py:188-192`). An overlong or non-string `evidence` that raised an error would invalidate the reviewer's whole block and lose every clear. Rule: ignore a bad `evidence`, no error.
4. **A free proxy for quote false-hold rate**: `annotate` already computes `anchor_status` missing/found (`findings.py:350`); the miss rate of anchors in existing reports is the miscopy rate a quote gate would inherit. Not yet measured.
5. **Dissent can be masked by a same-round non-blocking re-find**: `ledger.py:213-218` lets `current` (not blocking) overwrite `row["blocking"]`, so `prior L1 open` plus a MINOR re-find leaves a `regressed`, non-blocking row outside `brief_ids` (pinned by `test_review_ledger.py:518-546`, which has no prior line).

## 4. Final positions (exact rules for the merged design)

| ID | Final rule | Differs from A's final? |
|---|---|---|
| C-001 | Build the prior map first (`ledger.py:259-272` moves above `:254`). A `resolved_check` row becomes `resolved` iff (a) distinct `block_ok`-true reviewers typing `resolved` for it >= `need`, (b) no `block_ok`-true reviewer typed `open` or `regressed`, (c) not re-found this round. A `block_ok`-true `open|regressed` moves it to `regressed` (history `dissent`). Unanswered: stays `resolved_check`, listed in `verify_ids`. `need = min(Q_kind, requested)` where `requested` = reviewers in `--resolution` when given; **when absent, `need = Q_kind` (fail closed), not the report count.** Ask C-03 to set `Q_kind(re-review) = 1` so the unknown case cannot deadlock the standard flow (`panel.py:600`). | Yes: the `--resolution`-absent rule and the `Q_kind` request. |
| C-002 | Optional string `evidence` on a prior line, kept only if it is a string of at most 200 characters after flatten, else ignored with no error. Ledger writes it to the `prior_note` event with `quote_in_doc = bool(fnd.locate(doc_text, quote))`. Never gating. Reviewers are asked for it (line 61) so M1 has data. Promotion to a gate only on M1 evidence, and only with both a deletion carve-out and a fix for the lossy replacement span. | No (converged). |
| C-003 | `apply_revision` stores top-level `pending_new_sha256`; `merge_round` refuses (ledger unchanged) on mismatch, then clears it; **`apply_revision` refuses while one is pending** (guard for evidence 1). Recovery from a mismatch: restore the file to the stored hash. | Addition (the revise guard). |
| C-004 | In `merge_round`, at the point findings are annotated (`ledger.py:135-138`): `blocking = typed or severity == "CRITICAL"`; member records keep `blocking_typed`; each flip adds a warning. No category predicate in the core, `verdict:` line stays parser-neutral. M3 stays an offline measurement, not a code path. | No. |
| C-005 / X-001 | A `prior` line moves only a `resolved_check` row (clear or dissent). On any other status it is a `prior_note` plus a warning. Edit docstring `ledger.py:3-4`; rename `test_prior_lines_never_change_a_status`; add `resolved_check` cases. | No. |
| C-006 | `defer` needs `--owner` and `--reason`, allowed on a blocking row in `open`, `regressed` or `resolved_check`; writes no round record; terminal and counted open; no expiry. | No. |
| C-007 | Re-found deferred row stays `deferred`; `refound_deferred` in the merge result and in the Escalation text. | No. |
| C-008 | `brief_ids` = blocking `open|regressed`; `verify_ids` = blocking `resolved_check`; `held_ids` = blocking `deferred`; all derived on read. PASS iff all three empty; else FAIL, REVISE while `n < cap`, ESCALATE at the cap or when only `held_ids` remain. Exit codes 0/10/11 unchanged. Empty `brief_ids` with non-empty `verify_ids`: Reviser-brief section says "no revision needed; re-review the same candidate against the same baseline"; `verdict` JSON adds `next`. The report detail section and the Escalation paragraph list all three lists (`ledger.py:438-466, 482` today cover `brief` only). **VM-6 derived form**: `merge_round` refuses when `len(rounds) >= cap_reviews` or the derived decision before the merge is ESCALATE. | Addition (VM-6 form). |
| C-009 | **Drop** `verdict`, `decision`, `brief_ids` from new round records; `defer` stops writing them; `verdict()` derives from rows and ignores stored keys in old files; schema string kept. Store facts (`pending_new_sha256`, `blocking_typed`, `owner`, history), derive judgments (`verify_ids`, `held_ids` too). | Yes (A's primary is the snapshot; this is A's conditional form, triggered by VM-3). |
| A-005 | Independent of C-03 except the `Q_kind` interface above. | Minor. |

## 5. Positions changed since Round 1

| ID | Old (round 1) | New | Why |
|---|---|---|---|
| C-001 | Per-row quoted answer, B-style | Quorum gate `need`, dissent to `regressed`, no quote | Gate power of the quote is unmeasured (X-002); A's gate plus dissent route covers the reproduced paths; `ledger.py:328` |
| C-002 | Quote gates clearing | Record-only with `quote_in_doc` | Span lossy (`findings.py:431`, `ledger.py:224-225`), deletions leave nothing to quote, no test separates a lazy yes |
| C-004 | Parser-side floor; lens predicate as warning | Floor in `merge_round`; no predicate | `findings.py:188-192` drops the line; `prompts.md:31` is not category-expressible |
| C-005 | `prior open|regressed` sets any row | Only `resolved_check` rows move | Would reopen a human park; `ledger.py:3-4` |
| C-009 | Additive; stale `verdict` meaning changes | Drop stored `verdict`, `decision`, `brief_ids` | VM-3 literal wording (`synth-06:178`) |
| C-006 | Expiry recorded as metadata | No expiry | Nothing reads it |
| C-003 | Hash binding | Same, plus refuse `revise` while pending | Non-idempotent revise |
| C-008 | `verify_ids` outside brief | Accept A's `next` field and VM-6 derived refusal | Exit code stays 10 with no pinned change |
| A-005 | QUALIFY | Independent except `Q_kind` | `panel.py:600` one-reviewer re-review |

## 6. Unaddressed by either side (for the fault-finder)

1. **Exit-code-only callers.** `ledger verdict` exits 10 (REVISE) when `brief_ids` is empty and only `verify_ids` remain. A caller that reads the code alone runs a reviser with no ids, then re-reviews an empty diff, and the brief says an empty diff leaves every prior blocker open (`prompts.md:44`, `spec-panel.md:262`): the verify rows regress. The `next` field helps only callers that read it, and `prompts.md:70` does not tell coordinators to.
2. **Unanswered burns a review of the cap.** Alternative not weighed: refuse-and-rerun (like the zero-valid-block refusal, `ledger.py:150-157`), which costs no cap but is unbounded without a coordinator retry limit.
3. **Id vocabulary.** Priors key on ledger ids `L<n>` (`ledger.py:185, 261`); reviewers type finding ids `F<n>`. Whether PRIOR is the merged report (which carries `L` ids, and claim detail only for brief rows, `ledger.py:438-466`) is UNVERIFIED (`prompts.md:43` says "previous review report"). A wrong-vocabulary answer only warns (`ledger.py:263`) and holds. M2 must count compliance by ledger id, not presence of prior lines.
4. **Dissent from an invalid-block reviewer is ignored** though `findings.py:186` collects it. Fail-closed asymmetry argues for a hold-only (no status move) veto; unspecified.
5. **Completion state.** `block_ok` is the only reviewer-quality test; a reviewer that returned "incomplete" with a valid block (`prompts.md:48`) counts toward `need` (A's round-1 concession 6, absent from A's final).
6. **Dissent plus same-round non-blocking re-find** (new evidence 5): the row can drop out of every list. Rule needed: a valid `open|regressed` prior stops `row["blocking"]` being lowered this round.
7. **No undefer or reopen command**: a mistaken `defer` is permanent; a deferred `resolved_check` row loses its fix state.
8. **Held-only ESCALATE at `n < cap` plus VM-6** refuses any further round, so a human who defers the last open row cannot get a confirming re-review. Policy question.
9. **Mid-loop version change**: an older installed `verdict()` reads `last["verdict"]` (`ledger.py:366-369`) and `ledger_cmd.py:104-107` catches only `LedgerError`.
10. **Test churn**: stored-key reads at `test_review_ledger.py:133-134` (and probably `:280-298`), plus the silence-clear pins (`:193-217`, `:376-385` per B's round-1 E7, not re-read).

---

## Scoring Matrix

Winner = the approach both advocates' final (Round 2) positions support. "HYBRID" names what the debate itself produced. Confidence is the orchestrator's calibration from the two advocates' stated confidences and their Round 2 concessions (never 100%: no point was conceded verbatim by both sides). Taxonomy level in brackets.

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|------------|-------|--------|------------|-----------------|
| S-001 | L1 | TIE | 85% | Both advocates: layout only, no behavioural content |
| S-002 | L1 | UNRESOLVED (A 55% / B 65% in Round 1, not revisited) | 50% | A: B built B6 on a line it had not re-read; B: A tags second-hand claims "CODE-VERIFIED via research". Low stakes, both sides re-read line 31 in Round 2 |
| C-001 | L3 | HYBRID: A's gate (`need = min(Q, requested)`, `block_ok` filter, prior map built before the clearing loop, same-round re-find wins) plus B's dissent routing (`open|regressed` prior moves a `resolved_check` row to `regressed`) | 85% | Default re-review is one reviewer (`panel.py:600`, 8/8 templates `["first"]`); `apply_revision` skips non-open rows (`ledger.py:328`) so A's "held at resolved_check on dissent" swallows the next fix (A conceded). Residual: when `--resolution` is absent B says `need = Q_kind` (fail closed), A says requested = reports passed |
| C-002 | L3 | A (no gate), keeping B's optional bounded `evidence` key as recorded data with `quote_in_doc` | 88% | Quote proves reading not fixing (B conceded); deletion fix leaves nothing to quote (`document_review_loop_prompts.md:53`); span lossy (`findings.py:431`, `ledger.py:224-225`); promotion to a gate only on M1 evidence |
| C-003 | L3 | B (text-hash binding `pending_new_sha256`, plus `revise` refuses while one is pending) | 90% | Symmetric to `apply_revision` old-hash check (`ledger.py:308-314`); `merge_round` hashes unchecked text (`ledger.py:279`); A conceded; B added the non-idempotent-revise guard |
| C-004 | L2 | A (typed `blocking` stays authority) plus CRITICAL floor in `merge_round` and a flip warning; no category predicate, no grader in the core | 85% | Predicate misgrades `document_review_loop_prompts.md:31` ("needs a guess" is not category-expressible); parser-side floor would drop the line (`findings.py:188-192`); floor is a subset of `findings_v2.py:161-162`; B conceded the predicate |
| C-005 | L3 | HYBRID: B's dissent state, A's narrowed pin rule (a prior moves only a `resolved_check` row) | 88% | Both final positions identical; docstring `ledger.py:3-4` edited, test renamed |
| C-006 | L3 | B (owner and reason required, terminal and counted open, no expiry in the core) | 88% | Expiry cannot fire: deferred rows leave `brief_ids`, held-only is ESCALATE, VM-6 refuses later rounds; A conceded |
| C-007 | L3 | B (re-found deferred row stays `deferred`, `refound_deferred` surfaced) | 88% | Respects the human park; verdict still FAIL/ESCALATE; A conceded |
| C-008 | L2 | HYBRID: `brief_ids` / `verify_ids` / `held_ids` derived on read, `next` field, report and Escalation list all three, VM-6 derived refusal | 85% | A supplied the empty-brief REVISE handling, B supplied the derived VM-6 form; both final tables match |
| C-009 | L2 | B (drop stored `verdict`, `decision`, `brief_ids` from new round records; derive on read; schema string kept) | 75% | `synth-06-conflict-log.md:178` (read by B): "derived from rows on every read and is never stored"; A's conditional form fires. A did not re-read synth-06 and did not affirm after B's check |
| C-010 | L2 | HYBRID: A's three-arm replay plus B's M2 (free compliance pre-count by ledger id) and M3 | 80% | Both Round 1 and Round 2 agree |
| C-011 | L1 | HYBRID / TIE: prompt line 61 asks for the optional `evidence` key, line 70 restated, plugin mirror in step | 70% | A R1 favoured one clause; B R1 TIE; converged C-002 makes the line 61 ask a recorded-data ask |
| X-001 | L3 | A (pin rule kept true, narrowed to rows not in `resolved_check`; test renamed) | 85% | `test_review_ledger.py:318-338` assertions survive, the stated rule needs the narrowing; B conceded its pin list omission |
| X-002 | L3 | A (occurrence of a quote is not evidence of examination) | 85% | B conceded "proves reading, not fixing"; both end on record-only |
| X-003 | L3 | HYBRID: A's gate with `need = min(Q, requested)`; C-03 asked to set `Q_kind(re-review) = 1` | 80% | A's deadlock evidence (Q above panel size makes every row unclearable); B agreed and added the Q_kind interface |
| X-004 | L2 | A (no spec predicate; floor plus warning) | 85% | `findings-v1` has no `rule`/`wrong_outcome`; B6 flips the shipped grading; both converged |
| A-001 | L3 | QUALIFY (both) | 80% | Prior ids are ledger ids `L<n>`; the merged report prints claim only for `brief_ids` (`ledger.py:438-466`); both final positions render all three lists. Whether PRIOR is the merged report remains UNVERIFIED |
| A-002 | L3 | RESOLVED by B's B4 (A: QUALIFY, B: REJECT; both adopt hash binding) | 85% | `merge_cmd.py:99-109` passes `--doc` unchecked; `pending_new_sha256` binds it |
| A-003 | L3 | QUALIFY (A ACCEPT in Round 1, B QUALIFY; both final rules require the report and Escalation text to name held and verify rows) | 80% | `ledger.py:482` lists `brief` ids only today |
| A-004 | L2 | QUALIFY (both): holds for this slot; reopens if the unified panel makes reflect a ledger consumer | 75% | No import between `cli/review` and `cli/reflect`; neither side re-ran a repository-wide search of reflect call sites |
| A-005 | L3 | RESOLVED: independent of C-03 except the `Q_kind` interface and `need = min(Q, requested)` | 80% | `panel.py:600` one-reviewer re-review |

Tally of decided points: A wins 5 (C-002, C-004, X-001, X-002, X-004); B wins 5 (C-003, C-006, C-007, C-009, A-002 resolved); hybrid 6 (C-001, C-005, C-008, C-010, C-011, X-003); tie 1 (S-001); QUALIFY or independent 4 (A-001, A-003, A-004, A-005); unresolved 1 (S-002). Debate-performance tiebreaker input: 5 to 5.

## Positions changed across rounds (per advocate, from their own Round 2 tables)
- Advocate A: C-001 (dissent to `regressed`, `need = min(Q, requested)`), C-002 (specified record-only), C-004 (floor in `merge_round`), C-005/X-001 (rule narrowed), C-006 (expiry dropped), C-009 (additive snapshot with VM-3 conditional), A-005, C-003 (B4 adopted); corrected its own Round 1 claim that `--resolution` already carries requested ids (`merge_cmd.py:73-83`).
- Advocate B: C-001 (quote gate to quorum gate plus dissent route), C-002 (gate to record-only), C-004 (parser floor and predicate to `merge_round` floor, no predicate), C-005 (only `resolved_check` rows move), C-006 (expiry dropped), C-008 (accepts `next` field and VM-6 derived form), C-009 (drop stored keys), C-003 (revise guard added), A-005.

## Round 2.5: Invariant Probe (summary; full table in invariant-probe.md)

Independent fault-finder agent (c02-fault-finder-r25), not an advocate. It probed the 6-category checklist against the converged design (the Round 2 final positions of both advocates). Result: 22 findings, 6 ADDRESSED, 16 UNADDRESSED (HIGH 3, MEDIUM 12, LOW 1).

HIGH and UNADDRESSED (blocking per the invariant-probe gate):
- INV-001 (collection_boundaries): `need = min(Q, requested)` can be 0 if `--resolution` carries an empty reviewers list (`merge_cmd.py:73-83` accepts it), which would let silence clear again; no `max(1, ...)` floor is specified.
- INV-002 (interaction_effects): a valid `prior open` plus a same-round non-blocking re-find leaves a `regressed`, non-blocking row in none of `brief_ids`, `verify_ids`, `held_ids` (`ledger.py:213-218`, `:235-238`), so the round can pass over the dissent; B listed this in round2-B.md section 6 item 6 and no rule was agreed.
- INV-003 (sufficiency_challenge): the state "empty `brief_ids`, non-empty `verify_ids`" is exit 10 for exit-code-only callers; the `next` field is only in `ledger verdict` JSON and `document_review_loop_prompts.md:70` does not tell coordinators to read it; a reviser run with no ids followed by an empty-diff re-review regresses fixed rows (`document_review_loop_prompts.md:44`, `spec-panel.md:262`).

ADDRESSED and confirmed by branch trace: INV-012 (D-1 A and D-1 C closed for silence), INV-015 (D-2 C closed by the `merge_round` floor), INV-017 (D-11 A/B/C closed in the status-guard and verdict part; the expiry part of D-11 B is dropped by decision C-006), INV-019 (distinct-reviewer counting and the VM-6 cap comparison), INV-021, INV-022.

MEDIUM and LOW UNADDRESSED items (INV-004 to INV-011, INV-013, INV-014, INV-016, INV-018, INV-020) are listed in invariant-probe.md; they do not block convergence and are logged as warnings.

## Convergence Assessment
- Points resolved: 21 of 22
- Alignment: 95.5% (computed on diff-analysis denominator S + C + X + A = 22)
- Threshold: 80%
- Taxonomy coverage gate: PASSED (L1, L2, L3 all covered)
- Invariant probe gate: BLOCKED (3 HIGH-severity UNADDRESSED invariants: INV-001, INV-002, INV-003)
- Status: BLOCKED_BY_INVARIANTS (diff-point agreement above threshold, taxonomy covered, HIGH UNADDRESSED invariants remain)
- CONVERGENCE BLOCKED: 3 HIGH-severity UNADDRESSED invariant(s) detected. Blocking items: INV-001, INV-002, INV-003. Depth is `standard`, so there is no Round 3 in which to address them; they are carried into the return contract (`unaddressed_invariants`) and the merge result as open conditions.
- Unresolved points: S-002 (tag-discipline split, Low); residual disagreements inside converged points: C-001 `--resolution`-absent fallback (A: reports passed, B: need = Q), C-009 (A not on record after B verified VM-3 wording)
- MEDIUM unaddressed warnings: INV-004, INV-005, INV-006, INV-007, INV-008, INV-009, INV-010, INV-011, INV-013, INV-014, INV-016, INV-018
