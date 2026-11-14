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
