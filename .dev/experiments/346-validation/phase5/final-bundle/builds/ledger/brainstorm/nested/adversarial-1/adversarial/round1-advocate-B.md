# Round 1 advocate: Variant B (variant-2-sonnet-analyzer.md, analyzer persona)

Advocate for Variant B. Opposing: Variant A (opus, architect), Variant C (haiku, backend). Inputs read in full: the three variants, `diff-analysis.md`, `seed-brief.md`. I also re-checked three code facts that the dispute depends on (X-009, the install naming trap, X-010); results are cited where used.

## Position

Variant B is the best base for the merged spec because it is the only one that traces the failure to a root cause in the real files (a minor finding F22 applied under a brief that said "apply confirmed findings", which made blocking N5, whose fix made N12), builds its mechanism and its predictions on that trace, and states plainly that its own conservative forecast probably misses the bar (P3s about 5.5). It has real defects (X-016, X-017, an undefined status for MAJOR rows filed as minor, a sixth session that breaks the one-line brief rule), and the merge should take A's computed-blocking profile and derivable ledger path and C's loop/delivery split, stale-answer binding and relocation handling, while rejecting C's one-row discovery budget and its transaction machinery.

## Steelman of Variant A

**Strongest version of A.** A treats the ledger as a reusable kernel, not a spec-panel patch. Three parts, each with one job: a script that is the only writer, a contract in `SKILL.md`, and a thin adapter command with a `PROFILES` table (A section 2, section 6). Adding reflect or rf-qa is "one table entry plus one parametrized test row, never a change to the transitions or the decision formula" (A section 6, U-001). That is the cleanest extension seam of the three.

A also gets several mechanical details right that B gets wrong or leaves open:
- `blocking` is computed from a profile "never from the model" (A section 3), so a reviewer cannot file a MAJOR with a real outcome as minor. B lets the reviewer pick `sev` (X-014).
- The default ledger path is derivable from the document path, so a lost `--ledger` flag cannot restart a first review (A section 3, X-008). B stops the run instead.
- `begin` refuses when the previous report's last line differs from the recorded verdict (`E-REPORT-EDITED`, U-002), and `E-NOT-CHANGED` stops a verifier from re-attacking text no hunk touched (U-004).
- A script-written `plan-r<k>.md` hands the verifier frozen severity, wrong outcome and old and new hunk text per row (U-003), and the V1-ledger validity check says a replicate whose reviewers never ran the script is not treatment (U-005).
- A PASS at review 1 needs no sweep because review 1 already was a whole-document pass (C-030). That is logically right and cheaper than B.
- Running the sweep in the review-3 session adds no session and keeps the S1 briefs close to the one-line substitution the seed brief demands (C-039).

What A genuinely gets right is the architecture of reuse and the amount of state the script owns without a second dispatch.

## Steelman of Variant C

**Strongest version of C.** C takes "the script, not a model, owns the state" to its logical end. The ledger is an event log: status is never stored, it is recomputed by replay, every mutation carries `--op` and `--expect-seq`, and a repeated operation with the same digest returns the original result (C section 3, section 6, U-019). Packets bind schema, round, document hash and ledger sequence, so a stale answer from an old or resumed session cannot advance newer state (U-024). Honest nonclaims run through the whole text: "Do not claim the total number of assessments is three" (C section 4), "A low raw B3 with a combined proxy above 3 is suppression, not convergence" (C section 9).

C also names things the others leave blurred:
- `loop_decision` versus `delivery_outcome`, with "no final PASS artifact emitted early" (U-021). This is the cleanest answer to the question of what a sweep blocker does to the verdict.
- `cannot-verify` as a legal verifier answer and a structural escalation term `X_r` plus an integrity predicate `I` (U-022, U-023), so the loop fails closed instead of guessing.
- A per-revision anchor mapping with a tombstone for deletions and `anchor_state=missing|ambiguous` (C section 3), the only variant that addresses what happens to an anchor after unrelated edits or a pure deletion (A-009, A-010).
- A sweep may challenge a previously verified row (C section 4), the only variant that gives the "edit elsewhere broke an accepted fix" case (A-011) a path into the count.
- Its headline R3 count includes deferred MAJOR notes (X-011), which is closer to what the control's whole-document review 3 would have reported.

What C genuinely gets right is fail-closed integrity and a precise vocabulary for outcomes.

## Key strengths claimed

1. **The root cause is traced in the real files, and the mechanism is aimed at it (B section 1, U-008).** F22 was non-blocking, yet it was applied (`F2D1:37`) because the brief said "apply confirmed findings" (`F2D1:10`), although 427 says minor findings never trigger a revision (`SP:259`). The F22 fix put the WC-1 proof into AC-0.4: lines naming AC-0.4 and WC-1 go from 0 in `HIST/spec-v1-draft.md` to 2 in `spec-v2-after-round1.md`. That became blocking N5 (`F2R2:119`), whose fix became N12 (`F2R3:84`). A prose rule lost to a brief. B's answer is the matching mechanical rule: `answer` on a deferred row exits 5 (B section 3), and `revise-check` lists hunks no blocking row claims with `revert-unclaimed` to undo them (B section 2). Neither A nor C traces the chain to its first link; A cites "9 of 15 minor applied" and C cites the enrichment file as a "secondary observation" (C section 10).
2. **Evidence-grounded predictions that admit the bar may be missed (B section 9, C-036, X-012).** B builds a trace table on the two real review-3 reports and predicts P3 mean 3.0 but P3s about 5.5, then writes "so bar (a) is probably NOT met on the conservative metric". Its growth figure is derived from measured byte shares (3,920 of 26,768 and 7,212 of 19,205 changed-line bytes carry only a minor finding id), labelled an upper bound from one replicate. A predicts 2.5 and C predicts 1.5, both without a trace; C even counts more rows (X-011) yet forecasts the lowest number. A merged spec needs a forecast a reader can falsify, and only B gives one.
3. **A convergence bound that tells the truth about two fix cycles (B section 10).** Expected review-3 blockers are about B1 x r x r; with B1 = 13 and the measured ratios 0.46 then 0.17 that gives 1.0, matching flg-r2's actual 1. So the honest ceiling is "escalate with 0 to 3 rows", not "always PASS". A and C predict PASS in some replicates (A: 1 of 2) without such a bound. The merged spec should not promise convergence.
4. **A self-attack on verify-only scoping, checked against data (B section 5, section 10, U-013).** B lists five ways verify-only hides defects, then tests the first against the traces: all 8 ctl-r1 review-3 blockers and N12 have an anchor inside the changed lines (`C1R3:181-189` against `C1R3:11`; `F2R3:85` against `F2R3:25`). It states the limit (two documents, one reviewer model). A and C assert the scoping is safe or "may hide real defects" without a check.
5. **A way to measure hiding instead of arguing about it (B section 9, U-010, U-011).** Baseline sweeps on the six existing final specs, a sweep that classifies each late row as `in_claimed_span`, `in_unclaimed_hunk` or `outside_hunks`, and a hidden-defect share H. A and C count sweep rows but have no reference for what a whole-document pass finds in a 427-loop document, so they cannot tell "ledger prevented defects" from "ledger stopped looking".
6. **An installation trap found and avoided (B section 6, U-009).** I re-read `install_skills.py:40-59`: `_has_corresponding_command` skips and deletes an installed `sc-<x>` skill when `commands/<x>.md` exists and does not activate it by name. A skill named `sc-spec-panel-ledger` would be silently removed. B names this and rejects a `superclaude ledger` CLI subcommand with the D9 reason (the machine binary is the owner's install). A picks the safe name `sc-review-ledger` without saying why, so a later rename would break it unnoticed.
7. **A drift test and a green-test discipline (B section 6, X-009, U-017).** I re-read `tests/skills/test_worker_contract.py:831-839`: `_check_no_unattended_sections` globs every `commands/*.md` that has a `## Unattended mode` heading and asserts set equality with `UNATTENDED_COMMANDS`. `spec-panel.md` has that heading at line 451. A's "byte-identical except three blocks" copy keeps the heading, so a new `spec-panel-ledger.md` would be an unexpected member and fail that check unless the set is edited. B omits the section and says so. B also defines a drift test (variant equals `spec-panel.md` outside the replaced sections) and runs `test_review_severity_rule.py` first.
8. **Cost stated from file times, not guessed (B section 11, C-041).** Disposition-to-next-report gaps of 9 to 16 minutes in flg-r2 (`ls -la`), 20 to 31 script calls, 6 sessions instead of 5. A says "about +20 calls, no added session"; C gives 0.1 to 2 seconds per call. Only B shows where the number came from.
9. **A complete rule-by-rule MECHANICAL/PROSE table with residual risk (B section 11).** Every rule is classed, and the residual risk names the case where the script is satisfied but the outcome is wrong (for example "a quote proves presence, not relevance; `wrong_outcome` can be filler"). C's inline labels carry the same information but scatter it; A's table is shorter.
10. **Small mechanisms that close real holes.** `depends_on` lets a new row sit on an unchanged line only if it quotes the changed line it depends on (U-014). `mark resolved=yes` requires an `evidence` quote that is byte-present in the current document, which at least proves the text was opened (B section 10). `revert-unclaimed` gives the reviser a recovery path (U-015). T10 records the user's own words for any demotion (U-016).

## Weaknesses identified in Variant A

1. **The sweep runs in the same session that just verified (A section 2 review 3 step 2; section 11 "Sessions: none added"; C-012, X-002).** That session has read every plan row and every hunk, so the one whole-document guard is anchored on exactly the rows it is meant to second-guess. A's own open question 3 asks whether it should be a separate session. Shared assumption A-017 ("the sweep reviewer has not been anchored") is contradicted by A's design. B and C both use a fresh session.
2. **Sweep blockers never change the verdict (A section 2; X-001, C-013).** A's report would print PASS next to `sweep: 2 blocking` (A section 11 risk 1 admits it). That is the "hollow PASS" B warns about (B section 10 point 4). It also makes the same S1 run PASS under A and ESCALATE under B and C. At minimum A needs C's `loop_decision` / `delivery_outcome` split.
3. **The no-progress ESCALATE at review 2 (A section 4; C-014, X-003).** A's rule `B(2) >= B(1)` counts fix-induced rows in B(2), so a reviser who fixes 2 of 3 blockers and introduces 2 new ones is escalated although the original blockers fell. On the real flg-r2 counts the blocking numbers went 13, 6, 1, so the rule would never fire there; its only effect is to end a loop one review early elsewhere. A admits it "changes what R3 means" (A section 12 question 1), which breaks the measurement: R3 is undefined for a loop that ended at review 2.
4. **A verifier can clear a row nobody fixed (A section 3 transition table, X-021).** A allows `open`, `fixed` and `reopened` to move to `verified`. A lazy `resolved` with any quote then shrinks `B(k)` without a fix. B refuses `mark` on anything but `fixed` or a ruled dispute, and C keeps unfixed rows open. This is the mechanical hole that the whole design is meant to close.
5. **Span coordinates are inconsistent (X-020).** A stores spans like `"span": "r2:220-220"` and defines hunks "as new-file line ranges", then allows `regressed` only if the stored span overlaps a hunk of this round. At review 3 an r2-coordinate span is compared with r3-coordinate hunks. Retouch detection can misfire in either direction, and misfires are refusals that stall an unattended loop. B stores claims as quotes and re-locates them; C stores old and new ranges.
6. **Unclaimed edits are reported but not undone (A section 11, X-005).** A's table says "Unlisted related edits: detected and reported, not prevented". The F22 chain is exactly an edit that survives in the document. A refuses the `answer` on a deferred row, but the text the reviser already wrote stays. B's `revert-unclaimed` removes it.
7. **The prediction basis looks mislabelled (A section 9).** A writes "R1 blocking in Arm B was about 5 to 6 under 427 grading (the R2 proxy fell from 16-17 to 5-6)". As I read it, 5 to 6 is the review-2 proxy of the flg runs, not review-1 blocking; B's trace puts flg-r2 review-1 blocking at 13 (`F2D1:39`). If so, A's 2.5 forecast rests on the wrong quantity (this is A-012 in its worst form).
8. **Copy keeps `## Unattended mode` (X-009).** See strength 7: the retained heading (spec-panel.md line 451) breaks the `UNATTENDED_COMMANDS` set-equality check unless that set is edited. I read lines 451 to 461 and they do not mention the removed re-review flags, so this is a test problem, not a wrong-flag problem. A could also keep the section and add the name to the set; it does not say so.
9. **Minor scope creep (X-010).** A edits `tests/unit/test_cli_install.py`; the check is presence-only (`_assert_present`, line 501), so the edit is not required.

## Weaknesses identified in Variant C

1. **C's S1 arm is not the one it claims (C section 9 against section 2 and section 11; X-018, A-006).** C says "Only authored brief change: substitute `/sc:spec-panel` with `/sc:spec-panel-ledger --ledger <absolute-run-path>`" and "do not rewrite the surrounding brief". But "The coordinator alone runs ledger mutations", reviewers receive packets, and the loop uses four reviewer sessions plus two reviser sessions. The coordinator and the dispatch list must change, which changes the experimental variable the seed brief fixes. B at least states its deviation (a sixth session) as a deviation.
2. **The one-row discovery budget would end the real trace at review 2 (C section 2 step 3; C-016, X-004).** C allows at most one new finding C001, only in review 2, and "two candidates or more than 200 changed lines yields ESCALATE". On flg-r2, review 2 found 6 new blocking rows (`F2R2:13`). C would ESCALATE there, so cycle 2 never runs and S1 tests the overflow rule, not convergence. C's own risk table admits it ("an overflow may dominate S1 rather than test convergence"; open question 2). With no discovery in review 3, an N12-type defect is not a row at all; it becomes a regression observation. C's forecast of 1.5 is not consistent with its own mechanism on the real data.
3. **A transaction contract far beyond what a two-cycle experiment needs (C section 6; C-025).** Advisory lock, fsync on every artifact, no-replace hard-link publication, directory sync, "Refuse filesystems without these local publication guarantees", and fault injection at every boundary. The S1 loop is five or six sequential sessions on one Linux host. Atomic `os.replace` plus a plain `flock` and an operation id gives the same safety for the failures that actually occur. The extra machinery is code that can itself fail and stall a loop; C lists 17 risk rows in section 11. This breaches the scope-discipline rule.
4. **Hard refusal of uncovered edits has no escape (C section 3; C-017, X-005).** "uncovered edits fail revision admission" with no way to revert. A reviser who fills an FR-8/FR-9 gap in text no row names (A's open question 4 cites `spec-panel-review-loop.md:73`) hits a refusal and an unattended run stalls. B pairs the check with `revert-unclaimed`; the merge should take C's strictness and B's escape together.
5. **The default ledger path cannot be derived (X-019, C-002).** The default includes a random `run-id`, so a session cannot re-derive it; the default only works if the coordinator passes `--ledger` on every call. That is the failure `DES:162` describes (coordinator drops the saved copy and the run becomes a first review), now moved to the coordinator's memory.
6. **No parity guard for the command body (C-028).** C's outline names six items and no copy rule or drift test, so the 486-line panel text can silently diverge from `spec-panel.md`. A and B both define a parity test.
7. **Exit 0 on ESCALATE (X-007).** "An operation may successfully commit an ESCALATE decision and exit 0". A shell-level coordinator that checks `$?` reads success. B's `close` returns 10 for CONTINUE and 11 for ESCALATE, and states that the exit code outranks any sentence of a brief, which is the exact failure in `F2R3:15`.
8. **No way out of a wrong frozen blocker (C section 3, C-007).** "No automatic blocking deferral or user-waiver API in version 1." A false first-pass blocker forces FAIL forever. B's T10 and A's escalation-to-user are at least recorded exits.
9. **Reduced reporting freedom (C section 12 question 3).** The script writes the report from ledger state, so the panel's own expert prose is replaced. A and B keep the reviewer's report and append script lines.

## Concessions

**The two intra-B contradictions.**

- **X-016 (FR-8/FR-9 blocking with no field to carry it): conceded.** Bullet 3 of the command says "CRITICAL and FR-8/FR-9 are blocking", but an `add` row carries only `sev`, `grade`, `anchor`, `finding`, `wrong_outcome` and optional fields, and `init` takes only `--scale` and `--needs-outcome`. The script cannot compute or check the FR rule; it rests on the reviewer's `sev`. This is the same defect as X-014. Repair: add a `rule` field to the row and make `blocking` a script output of a profile (A's `PROFILES` seam, C's predicate): CRITICAL, or rule FR-8 or FR-9, or MAJOR with a non-empty `wrong_outcome`. The reviewer supplies `grade`, `rule` and `wrong_outcome`, never `sev`. This keeps B's generic kernel (no spec-panel words in the core) and puts the spec-panel words in a named profile.
- **X-017 (`disputed` as a status): conceded.** T4 keeps the status ("stays; `claim.action=disputed`") while T8 lists `disputed` as a From state. Repair: `disputed` is a claim flag, never a status. T8 reads "From: `open` or `reopened` with `claim.action=disputed`; To: `verified` if the verifier accepts, else `reopened`; the note is required". The verifier's mandatory ruling on a dispute stays, because A and C leave a disputed row without a ruling.

**Other defects I found in B while analysing the others.**

- **A MAJOR row filed as `sev=minor` has no defined status.** T2 auto-defers only on grade MINOR. A MAJOR with no outcome and `sev=minor` is neither deferred nor blocking in the table. That also makes B's own P3 definition ("grade, not `sev`, so MAJOR rows 427 relabels as minor are counted") unrealizable, because P3 counts only statuses `open`, `fixed` or `reopened`. The profile repair above fixes it: non-blocking means `deferred`, and the headline R3 metric must include deferred CRITICAL/MAJOR rows (C's X-011 position), with B's P3 and P3s reported beside it.
- **The sixth session breaks the seed brief's constraint** ("one-line name substitution in the briefs"). B states it as a deviation, but A-006 is CONTRADICTED for B as well. Better route, not in any variant (UNVERIFIED whether S1 workers may spawn subagents): the review-3 command spawns the sweep as a fresh subagent that is told not to read the ledger. That keeps A's unchanged dispatch and B's independence.
- **`--as reviewer|reviser|coordinator` proves nothing.** My own table says identity is PROSE. The phase gate is the mechanical part, and A infers the role from the subcommand. Drop the flag.
- **Largest CLI surface of the three** (12 subcommands, 20 to 31 calls). Several (`render`, `verdict`, `show`) can fold into `close` and `status`.
- **No lock, no operation id.** B section 7 admits parallel writers lose updates. C's `flock` and operation id are worth taking; the hard-link and fsync layer is not.
- **Byte-exact anchors are brittle.** B's own risk 1 says a quote that differs in whitespace is refused. A's whitespace-normalized match with a 12-character floor is better.
- **No `cannot-verify` result and a yes/yes risk.** C's explicit answer fixes the case where the verifier cannot decide.
- **Sweep after a review-1 PASS is wasted.** A is right (C-030, X-013).
- **Where A and C beat B outright:** derivable ledger path (X-008), profile-computed blocking (C-009, X-014), report-edit check (U-002), `E-NOT-CHANGED` (U-004), relocation and deletion handling (C-019, A-009, A-010), `loop_decision` / `delivery_outcome` split (U-021).
- **B's own forecast says the bar is probably not met on the conservative metric.** That is honest, but the merged spec should present it as the expected result, not hide it behind P3 alone.

## Shared assumptions

- **A-007: QUALIFY.** The assumption is that brief text ("any finding of any severity is FAIL") does not inflate review-1 grades. It is not safe. The round-3 report still graded FAIL on that sentence (`F2R3:15`), so the brief has already beaten the command once. Review 1 is the only grading moment and grades freeze, so a MINOR filed as MAJOR with a filler `wrong_outcome` becomes a blocking row for the whole loop; my own table says "`wrong_outcome` can be filler". No variant measures it. Condition: treat it as a named risk, record the review-1 blocking count and the share of blocking rows whose `wrong_outcome` an analyst judges filler, compare with Arm B's review 1 (13 blocking in flg-r2), and keep the Precedence bullet that a brief cannot change a severity.
- **A-008: QUALIFY.** It holds only if something stops the S1 dispatch. With the verbatim briefs T05 to T09 (`DEC:59`, `DEC:64`) a revise-2 session still runs after an early PASS, and `answer` being refused in phase `closed` does not stop it editing the document. B omits the Reviser brief when the verdict is not CONTINUE, which tells that reviser there is nothing to do, but a brief that says "apply confirmed findings" can still push edits. Condition: measure growth at the snapshot of the final decision (C's carry-forward rule), surface any later change to the document as a mismatch, and make `close` print "no revision: do not edit" in the report.
- **A-009: QUALIFY.** An old anchor usually stays unique, because changed lines were 7.9% (flg-r2) and 24.2% (ctl-r1) of the document at review 3, but "usually" is not a check. B's `add` proves uniqueness only at creation, and `open` prints hunks only for `fixed` rows, so an unanswered `open` row has no relocation. A later insertion that repeats the phrase makes the row ambiguous. Condition: `open` re-resolves every unmoved row's anchor and reports `anchor_state=ok|missing|ambiguous` (C's idea), and a missing or ambiguous row yields ESCALATE with the row listed, never a guess.
- **A-010: REJECT.** It is false for a pure deletion: a fix that removes a sentence can lose an obligation, and the deleted text is not present on the new side, so B's rule that an anchor be byte-present in `DOC` and inside a hunk cannot file it. B's `depends_on` quotes a changed line, which for a deletion is also absent. Cheap repair: accept an anchor within the three context lines B already prints around a deletion hunk, mark the row `origin=deleted-near`, and keep the old-side range (C's deletion boundary). Until then such defects wait for the sweep.
- **A-011: REJECT.** An edit elsewhere can invalidate an accepted fix. N12 is that pattern: the N5 fix added a "record the agent command" step that interacted with other sections (`F2R3:35`), and N15 was an unchanged step contradicted by 2.3 (`F2R3:99-101`). B's own section 10 point 2 calls interaction defects "the likely casualties". T9 resets a verified row only when a hunk overlaps its claim span. Repair: take C's sweep challenges (a sweep may challenge a verified row, which enters the delivery count), and add a cheap lexical cross-check at `open` (a hunk that contains an identifier such as AC-0.4 or WC-1 named in a verified row's claim re-opens that row for a second look). This is a heuristic and must be labelled one.
- **A-012: QUALIFY.** All three forecasts lean on Arm B's review-1 counts, and under the ledger review 1 changes: the reviewer knows it is the only find pass and must write anchored JSON rows with a `wrong_outcome` for every blocking MAJOR. The count could rise or fall. B's formula B1 x r x r makes the sensitivity visible (B1 = 13 gives 1.0 at the measured ratios; B1 = 6 would give 0.5), and I would use it. Condition: pre-register that the S1 prediction is recomputed from the actual review-1 count, and report review-1 blocking per replicate as a covariate.

## Positions table

| Point | Preferred | Reason |
|---|---|---|
| S-001 | B | Outlines are identical; keep B's citation aliases for audit. |
| S-002 | B | Alias list with UNVERIFIED marks lets a reviewer recheck every claim. |
| S-003 | B | Step table shows who, reads, writes and calls at a glance. |
| S-004 | A | Kernel, contract, adapter table gives the clearest extension seam. |
| S-005 | A | One state document with per-row history is simplest to test; replay adds little. |
| S-006 | B | Phase column makes the phase gate checkable per transition. |
| S-007 | B | Decision table plus worked example on real flg-r2 counts. |
| S-008 | A+B | A lists main checks; B lists roles and exit codes. |
| S-009 | A+B | Named test cases from A, text pins and drift test from B. |
| S-010 | B | Predictions tied to traced rows can be checked and falsified. |
| S-011 | B | Evidence and verdict columns separate removed causes from left ones. |
| S-012 | B | End table with residual risk per rule; inline labels scatter it. |
| S-013 | A+B | One design doc suffices; user guide and schema file are speculative. |
| S-014 | B | Final UNVERIFIED list tells implementers what to check first. |
| S-015 | B | Dense tables with citations review fastest. |
| C-001 | A | Single JSON object with per-row history; JSON Lines gains nothing, replay is overbuilt. |
| C-002 | A | Path derivable from the document; a lost flag cannot restart a first review. |
| C-003 | A+C | A's snapshot timing; C's candidate hash catches out-of-band edits. |
| C-004 | A | Role follows from the subcommand; B's --as flag proves nothing. |
| C-005 | B | T1 to T11 with phase column is most complete; keep fixed-only verification. |
| C-006 | B | Verifier must rule on a dispute; A and C give no explicit ruling. |
| C-007 | B | User-quoted demotion keeps a wrong blocker from freezing the loop forever. |
| C-008 | A+C | A's wide key list plus C's frozen issue text. |
| C-009 | A+C | Script computes blocking from a profile; reviewer-supplied sev is a hole. |
| C-010 | B+C | B's unmarked-row refusal and sweep term; C's integrity and pending states. |
| C-011 | B | Separate U and Lt counters show loop and sweep outcome apart. |
| C-012 | B+C | Fresh session outside the cap keeps the sweep unanchored; label it sweep. |
| C-013 | B+C | Split loop_decision from delivery_outcome; late blockers must block a final PASS. |
| C-014 | B | Monotonic stop optional, default off; flg-r2 blocking fell 13, 6, 1. |
| C-015 | B | Auto-defer plus minor_touched metric detects edits that slip through. |
| C-016 | B | Hunk-bound checks in reviews 2 and 3; C's one-row budget escalates flg-r2. |
| C-017 | B+C | C's admission check, with B's revert-unclaimed as the recovery path. |
| C-018 | A+B | A's whitespace normalization and 12-character floor; B's --at for repeats. |
| C-019 | C | Only C handles missing, ambiguous and deleted anchors explicitly. |
| C-020 | B+C | C's raw old and new ranges cover deletions; B's HUNKS_LARGE warning. |
| C-021 | B+C | B's touched_ok forcing a child row; C's cannot-verify result. |
| C-022 | A+B | B's reset to fixed on retouch; A's refusal to re-attack untouched rows. |
| C-023 | A | Script computes caused_by from hunk attribution; reviewer-given parent can be wrong. |
| C-024 | A | Body hash plus report-edit check; add B's reseal command. |
| C-025 | B+C | Atomic replace plus flock and operation ids; skip hard-link and fsync machinery. |
| C-026 | B | Same layout, plus install-trap warning and reason to reject a CLI subcommand. |
| C-027 | B+C | B's decision-coded exits; C's delivery_outcome field in JSON. |
| C-028 | B | Copy with drift test; omit Unattended mode to keep its test green. |
| C-029 | A+B | Reviewer keeps panel prose; script appends verdict, footer and brief. |
| C-030 | A | Review 1 is already a full pass; a sweep after PASS is redundant. |
| C-031 | B+C | B's multi-file and caller-loop needs; C's rule that ledger PASS cannot promote. |
| C-032 | B+C | B's step mapping; C's rule to keep rf-qa's stricter halt order. |
| C-033 | B | Do not adopt in implement until an incident shows the pattern. |
| C-034 | B | File ledger, with a stateful session as the cheap fallback experiment. |
| C-035 | A+C | Union with sweep dedup; report ledger-only and sweep parts apart like B. |
| C-036 | B | Forecast built from traced rows; admits the bar is probably unmet. |
| C-037 | B | Growth derived from measured minor-only byte shares, stated as upper bound. |
| C-038 | A+B | B's baseline-sweep and minor_touched failures; A's ledger-honoured check. |
| C-039 | none | Run the sweep as a fresh subagent in review 3: independent, no new dispatch. |
| C-040 | B | Baseline sweeps on six existing finals are the only hidden-defect reference. |
| C-041 | B | Calls, sessions and minutes estimated from file times, not guessed. |
| C-042 | A+B | A's 12-character anchor floor; B's warn-only HUNKS_LARGE; no hard limits. |
| C-043 | A+B | A's constant tied to the cap text; B's exit 11 at the cap. |
| X-001 | B+C | A late blocker must block a clean final outcome, or PASS is hollow. |
| X-002 | B+C | Fresh session; a same-session sweep is anchored on rows it just read. |
| X-003 | B+C | No second stop; flg-r2 blocking fell 13, 6, 1 so it never fires. |
| X-004 | A+B | Both allow reviews 2 and 3; N12 arose at review 3. |
| X-005 | B+C | Hard check at admission, with revert-unclaimed as escape from stalls. |
| X-006 | A+B | Worker sessions run their own calls; coordinator-only changes the S1 arm. |
| X-007 | B+C | Decision-coded exit for close; JSON names the delivery outcome. |
| X-008 | A | Derivable default path; B's mandatory flag is a self-inflicted stall. |
| X-009 | B | Verified: the test needs Unattended-mode set equality; A's byte copy would fail it. |
| X-010 | B | Check is presence-only, so no edit is needed. |
| X-011 | C | The control counted all critical and major findings, so deferred MAJOR notes count. |
| X-012 | B | An honest forecast that the conservative bar is missed beats optimistic ones. |
| X-013 | A | Review 1 PASS needs no second whole-document pass. |
| X-014 | A+C | Script computes blocking; B's reviewer-chosen sev is the flaw. |
| X-015 | B | A child row keeps the broken sentence visible as a counted blocker. |
| X-016 | A+C | Profile-computed blocking with a rule field fixes B's gap. |
| X-017 | B | Keep the verifier ruling; make disputed a claim flag, not a status. |
| X-018 | A+B | Worker-run calls with declared brief edits; C's one-line claim is false. |
| X-019 | A | Derivable path; a random id forces every caller to pass the flag. |
| X-020 | B+C | Quote-based claims and old and new ranges avoid cross-snapshot coordinates. |
| X-021 | B+C | Only fixed rows become verified; unanswered blockers stay open. |
| A-007 | none | No variant measures review-1 inflation; add blocking count and wrong_outcome audit. |
| A-008 | B+C | C carries terminal state to R3; B's omitted Reviser brief says do not edit. |
| A-009 | C | C's anchor_state missing or ambiguous is the only handling. |
| A-010 | C | C keeps old spans and deletion boundaries; A and B cannot anchor deletions. |
| A-011 | C | Only C lets the sweep challenge verified rows. |
| A-012 | B | B's B1 x r x r formula exposes sensitivity to the review-1 count. |

