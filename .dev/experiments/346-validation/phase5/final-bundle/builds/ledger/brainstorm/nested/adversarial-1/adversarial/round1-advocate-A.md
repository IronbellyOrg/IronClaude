# Round 1 advocate: Variant A (variant-1-opus-architect.md)

Advocate model: opus. Persona: architect (structure, dependencies, long-term impact). Custom focus: maintainability and extension scaffolding. Sources read in full: variant-1, variant-2, variant-3, diff-analysis.md, seed-brief.md. Section numbers below are each variant's own (A sN, B sN, C sN).

## Position

Variant A should be the skeleton of the merged spec: its kernel, contract and adapter split with a `PROFILES` table (A s2, s6), its single state document (A s3), its profile-computed `blocking` (A s3) and its subcommand-inferred actor (A s2) give the smallest durable core that four adopters can share. A loses on several loop rules, and the merge should take B's fresh-session sweep and soft-gated unclaimed hunks and C's anchor relocation, old-side diff ranges and split of loop decision from delivery outcome.

## Steelman of Variant B

The strongest version of B: it is the only variant that traced the failure it claims to fix in the real files. It shows that minor F22 was applied because the brief said "apply confirmed findings" (`F2D1:10`), which wrote the AC-0.4 WC-1 proof that became blocking N5, whose fix became N12 (B s1). From that trace B draws an honest conclusion that A and C do not state as plainly: "If the idea works on S1 it works mostly through the minor-row rule and the computed stop, not through a smaller read" (B s5), because all 8 ctl-r1 review-3 blockers and N12 already anchor inside changed lines. B then builds its measurement around the risk of its own design: a baseline sweep on the six existing final specs (B s9), a hidden-defect share H split by location (B s2 step 5, s9), and a convergence bound "B1 x r x r" that sets the honest ceiling at "escalate with 0 to 3 rows, not always PASS" (B s10). Its five-point self-attack on verify-only (B s10) is the best risk analysis in the set. B also catches two concrete repo traps A missed: a skill named `sc-spec-panel-ledger` would be skipped and deleted by `install_all_skills` (B s6), and copying `## Unattended mode` would break the `UNATTENDED_COMMANDS` set-equality test (B s6). Its sweep design is right on independence: "putting it inside review 3 would make the same session verify and then sweep, so the sweep would be anchored on the rows it just read" (B s4). Its unclaimed-hunk rule is the right middle ground: `revise-check` exits 7 and offers `revert-unclaimed`, while `open` only records, "so a reviser that skips the check does not stall the loop" (B s12 q2).

## Steelman of Variant C

The strongest version of C: it treats the ledger as a small database and takes correctness under failure seriously. Status is never stored, only replayed from an append-only event list (C s3), so there is no second store to drift. Every mutation carries `--op` and `--expect-seq`, request-digest idempotency and an advisory lock (C s6), so a retried or raced call cannot double-apply. C is the only variant that solves anchor drift properly: "Use unchanged-block line mapping first; then unique exact quote with exact before/after context. Line numbers are hints, never proof" with `anchor_state=missing|ambiguous` escalating (C s3). It is the only one that keeps old-side ranges and zero-width deletion boundaries (C s6), which fixes the coordinate bug in A (X-020) and the deletion blind spot (A-010). C's split of `loop_decision` and `delivery_outcome`, with "no final PASS artifact is emitted early" (C s4), resolves the hollow-PASS problem more cleanly than either A or B. C also adds `cannot-verify` as an honest verifier answer (C s6), says plainly that the sweep is an extra assessment ("Do not claim the total number of assessments is three", C s4), and draws the right line for implement: "Every archive attempt still needs a fresh independent full FINAL" (C s7).

## Key strengths claimed

1. **One extension seam, fixed in advance.** A splits the work into a kernel (only writer of state), a contract (`SKILL.md`) and an adapter (command plus profile name) (A s2 table). The `PROFILES` table "maps a profile name to its severity vocabulary, its blocking predicate and its cap"; "Adding an adopter is one table entry plus one parametrized test row, never a change to the transitions or the decision formula" (A s6). This is the property that makes reflect, rf-qa and implement adoption cheap and safe. B's alternative, `init --scale <grades> --needs-outcome <grades>` (B s7), pushes the grading rule onto every caller at call time, so two callers of the same tool can grade differently; C names the right idea ("each adapter pins its own grading/stop profile at init; unsupported profiles fail", C s7) but only as future work.
2. **`blocking` is computed, never chosen by a model.** "`blocking` comes from the profile, never from the model" with the 427 predicate copied verbatim (A s3, citing `spec-panel.md:259`). B lets the reviewer supply `sev` and only refuses MAJOR-blocking without `wrong_outcome` (B s2, s6), so a reviewer can file a CRITICAL as minor, and B has no field for the FR-8/FR-9 rule it states (X-016). C agrees with A (C s3, s6). Frozen severity only stops drift if the blocking flag cannot be chosen at creation either.
3. **A plain state document is the cheapest thing to maintain and inspect.** One pretty-printed JSON object with `rows`, each carrying `status`, `answers` and `history` (A s3). A maintainer can read it, `status --json` reports metrics from it directly (A s6, s9), and the per-row `history` already gives the audit trail C wants from replay. It reuses implement's `at`, `anchor`, `origin`, `resolved|open|regressed` vocabulary (A s3, citing `qa.md:137,143`), so adopters learn one vocabulary. C's event replay is stronger under crashes but makes every read a reducer and every schema change a replay migration (C s3, s11 "future unsupported schema versions stop without migration").
4. **The script is callable by the sessions that already exist.** Each session runs its own subcommand and "the actor column says whose input file may request the move, which the script infers from the subcommand" (A s3). That keeps the S1 coordinator unchanged and the brief change to a name plus `--ledger` (A s9). C's "coordinator alone runs ledger mutations" (C s2) contradicts its own one-line brief change (X-018). B's `--as` flag adds a declared role that B itself classes as "IDENTITY is PROSE" (B s11), so it adds a flag without adding enforcement.
5. **A lost flag can neither restart nor strand the loop.** The default ledger path "is derivable from the document path alone" and `init` refuses an existing ledger with `E-EXISTS` "so a lost flag can never restart a first review" (A s2, s3). B stops when `--ledger` is missing (B s6 bullet 1) and C's default contains a random `run-id` that no session can re-derive (X-019), so both depend on the coordinator keeping a path, which is the exact 427 failure the design cites (`spec-panel-review-loop.md:162`).
6. **Accepted text cannot be re-attacked, and the verifier gets a script-built plan.** `E-NOT-CHANGED` refuses `regressed` on a verified row whose span no hunk touched (A s3), and `begin` writes `plan-r<k>.md` with frozen severity, wrong outcome, old and new hunk text, unattributed hunks and `W-NO-ANSWERS` (A s2). This is the concrete replacement for 427's "reviewer re-reads the prior report and rebuilds the status table" (A s5).
7. **Verdict edits are detected.** `begin` refuses when "the prior report's last line equals the recorded verdict" fails (`E-REPORT-EDITED`, A s2, s4), and `body_sha256` gives `E-TAMPERED` (A s3). Neither B nor C checks the report tail at the next step.
8. **The validity check makes the experiment honest about compliance.** V1-ledger: "a replicate whose reviewers never ran the script counts as 'ledger not honoured' and is not treatment", with refusals counted as a covariate (A s9). Without it a replicate that ignored the script would be scored as a ledger result.
9. **The cap is tied to the code by a test.** `CAP_REVIEWS = 3`, `E-CAP` on a fourth `begin`, refusal of a third `answer` cycle, and "A test pins that the constant and the text agree" (A s4). The parity test against `spec-panel.md` (A s6) guards the 480 copied lines against silent drift.

## Weaknesses identified in Variant B

1. **Grading is a reviewer choice, not a computed field.** `add` rows carry `sev` and `grade` from the reviewer (B s6); the script only refuses `sev=blocking` on a MAJOR without `wrong_outcome` (B s2). A reviewer can file a CRITICAL as `sev=minor` and it is auto-deferred forever. The bullet "CRITICAL and FR-8/FR-9 are blocking" (B s6 bullet 3) has no field to carry the rule tag (X-016), so the script cannot check it.
2. **The adoption seam is call-time flags.** `init --scale ... --needs-outcome ...` (B s2, s7) means every caller restates the grading vocabulary on every run. A typo or a different caller silently changes what blocks. There is no named profile that a test can pin per adopter.
3. **Status set is ambiguous.** T4 keeps the status and sets `claim.action=disputed`, yet T8 lists `disputed` as a From state (B s3, X-017); the `mark` input domain is unclear.
4. **The CLI surface is large and mixes concerns.** Twelve subcommands (B s6) including `render`, `revert-unclaimed`, `show`, `verdict`, plus `close` exit codes 0/10/11 that encode the decision (X-007). A caller that treats non-zero as failure treats CONTINUE as a crash; B's own "the exit code of `close` outranks any sentence of a brief" (B s6 bullet 8) hard-wires that coupling.
5. **A missing flag stops the loop.** "`--ledger <path>` required; without `--ledger` stop and say so" (B s6 bullet 1) makes the run depend on the coordinator keeping the path, the failure mode 427 already has (`DES:162`, cited by B s5).
6. **No concurrency protection while claiming reuse by rf-qa.** B says itself "two parallel QA instances on one ledger lose updates; an adopter needs `fcntl.flock`" (B s7), yet orders rf-qa as the second adopter (B s7).
7. **The sweep's independence rests on prose.** "Sweep reviewer does not read `L`" is PROSE (B s11); the sixth session adds cost (B s11) and the measurement still depends on the instruction being followed.
8. **Forecast mixes a starting point the ledger does not share.** The 7 to 8 P3 for ctl-r1 (B s9 trace table) assumes verify meets the same 8 blockers, but those came from a control loop where minors were applied and the whole document was re-reviewed; the ledger changes both inputs, so the P3s 5.5 forecast is likely pessimistic for the same reason my 2.5 may be optimistic.

## Weaknesses identified in Variant C

1. **The S1 arm it describes cannot run as stated.** "Only authored brief change: substitute ... on its invocation line" and "do not rewrite the surrounding brief" (C s9) contradict "The coordinator alone runs ledger mutations" (C s2) and "four reviewer sessions including the sweep" (C s11). The S1 coordinator and dispatch list must change (X-018), which is a changed experimental variable C does not record.
2. **The discovery budget cannot record the defect that motivated the theme.** Review 2 may add "at most one new finding C001" and review 3 has "No discovery check remains" (C s2). N12, the fix-induced MAJOR found at review 3 in flg-r2 (seed brief Known Context), could not be a row; a second candidate or more than 200 changed lines forces ESCALATE (C s2). In S1 ctl-r1 review 3 had 88 changed lines and 8 blockers (B s5), so one row per loop would escalate almost every run on overflow, testing the budget rather than the ledger (C s11 concedes "an overflow may dominate S1").
3. **Hard refusal of uncovered edits stalls an unattended reviser.** "each changed old/new line belongs to at least one submitted blocking-row span; uncovered edits fail revision admission" (C s3). A whitespace reflow or a needed FR-8/FR-9 gap fill outside the row span blocks the cycle with no recovery path other than manual work (C s11 "may require manual recovery").
4. **The default path cannot be re-derived.** `<run-id>` is "an opaque random identifier" while "No missing-ledger fallback to a new FIND is allowed" (C s3, s2; X-019). The default is useless unless every caller passes `--ledger` anyway.
5. **The transaction contract is heavier than the experiment needs.** No-replace hard-link publish, directory fsync, refusal of filesystems without these guarantees, fault injection at every sync boundary (C s6). For a single-writer local loop of about 15 calls, atomic temp-file replace (A and B) covers crash safety; the extra machinery multiplies test and maintenance cost and makes the script Linux-local only (C s12 q9).
6. **Event replay makes every reader a reducer.** Status "is obtained by replaying events" (C s3); `status`, metrics, reports and adopters all need the reducer, and a schema change cannot migrate (C s11). A per-row `history` array (A s3) keeps the same audit trail without that cost.
7. **The R3 proxy is not comparable to the control.** `U3` counts every CRITICAL or MAJOR row with "status != verified", including deferred review-1 notes that were never in a fix cycle (C s9, X-011), yet C forecasts the lowest number, 1.5 (C s9, X-012), with a two-sentence basis (S-010). The count and the forecast pull in opposite directions without explanation.
8. **Deferred sweep blockers inside `B_r` blur the two decisions.** "A deferred blocking sweep row also counts" in `B_r` (C s4) while C also has a separate `S` in `delivery_outcome`; the same row can enter both formulas.
9. **Script-written reports remove the panel's output format.** The script "writes `reports/review-N.md` from ledger state" and the coordinator copies it (C s2, s9), which C itself flags as reducing "formatting freedom" (C s12 q3) and breaks the reviewer's existing report contract.

## Concessions

1. **The sweep must run in a fresh session.** A runs it "inside the last review session" (A s2, s11). B is right that this anchors the only whole-document guard on the rows the same session just verified (B s4; X-002, A-017 CONTRADICTED). I accept one added session and the stated S1 deviation (B s9).
2. **"Sweep rows never change the verdict" is wrong as a delivery claim.** A lets a PASS stand next to `sweep: 2 blocking` (A s11 risk 1). C's split is better: keep `loop_decision` for the cap and the `verdict:` line of each review, and emit a separate `delivery_outcome` that is ESCALATE when the sweep finds a blocker (C s4; X-001).
3. **My no-progress ESCALATE has no data behind it.** B shows the critique proxy fell from review 1 to review 2 in all six S1 runs, so a halt at n = 2 "would never have fired" (B s4). It should be an optional profile flag, default off for `spec-panel` and on for `rf-qa`.
4. **My stored spans are in the wrong coordinates.** Hunks are "new-file line ranges" while spans are stored as `r2:220-220`, so at review 3 an r2 span is compared with r3 hunks (X-020). C's old and new ranges per hunk and zero-width deletion boundaries fix it (C s6).
5. **My anchors break when unrelated edits move or duplicate a phrase.** A has no relocation rule for rows no answer moved (A-009) and cannot anchor a defect created by a pure deletion (A-010). C's relocation order and `anchor_state=missing|ambiguous` (C s3) should replace A's single-quote lookup.
6. **A verifier should not clear an unanswered blocker.** A allows `open -> verified` (A s3 table; X-021). B and C keep an unanswered row open. Only `fixed -> verified` should be legal.
7. **`broke_sentence` has no consequence in A** (X-015). B's rule is better: `touched_ok=no` requires a child row (B s3 T7).
8. **B found two install and test traps I missed:** the `## Unattended mode` set-equality test (B s6, X-009) and the skill naming trap (B s6, U-009). A's byte-identical copy would likely fail the first.
9. **B's forecast method is better grounded than mine.** A's 2.5 rests on one paragraph (A s9); B derives growth arithmetically from minor-only byte shares and traces each replicate (B s9). I keep my number as a forecast but rank B's method higher.
10. **The final report can be edited after the last `close` without detection** unless a coordinator runs `status` (A s11 rule table). That gap is still open in A.

## Shared assumptions

- **A-007: QUALIFY.** Inflation is a real risk because review 1 becomes the only grading moment and the briefs still say "any finding of any severity is FAIL" (seed brief). It is bounded in A and C because `blocking` is computed and a MAJOR blocks only with a non-empty `wrong_outcome` (A s3), but a model can still write filler outcomes. The merge should record the review-1 grade distribution as a covariate against Arm B's review 1 and let the command's grading bullet state that the brief cannot change a grade (B s6 bullet 8).
- **A-008: REJECT.** It does not hold: the fixed S1 dispatch sends revise 2 and review 3 regardless, and refusing `answer` after a final decision does not stop edits to `D`. The merge needs a mechanical check: after a final decision every later call (and `status`) compares the live `D` hash with the last snapshot and reports post-final edits (C s9 "measure both live D and the accepted snapshot"), and growth is measured on the accepted snapshot only.
- **A-009: REJECT.** For A and B an old anchor can become absent or repeated after unrelated edits. Adopt C's relocation (unchanged-block line map, then unique quote with context, then the reviser span) and escalate on `anchor_state=missing|ambiguous` (C s3).
- **A-010: REJECT.** A defect created by deleting an obligation has no new-side text. New verify-time rows must be allowed to anchor on an old-side range or a zero-width deletion boundary of a hunk (C s6), checked by `E-OUT-OF-SCOPE` against both sides.
- **A-011: QUALIFY.** It holds for local wording fixes but fails for cross-section interactions such as N15 (B s10 item 2). Mitigate inside the loop with B's `depends_on` (B s2 step 4) extended to verified rows: a verified row whose `depends_on` target a hunk touched goes back on the plan. The residual is left to the fresh sweep, whose challenges to verified rows count in the delivery outcome (C s4).
- **A-012: QUALIFY.** Using Arm B review-1 counts is the only data available, but review 1 under the ledger knows it is the only find pass and writes JSON rows, which may raise or lower the count. Forecasts should be stated as conditional on review-1 blocking count, and the measurement should report review-1 row and grade counts next to Arm B's so a shifted find pass is visible.

## Positions table

| Point | Preferred | Reason |
|---|---|---|
| S-001 | A | Section titles name the real commands, easier to search later. |
| S-002 | B | Alias list plus UNVERIFIED marks make citations checkable. |
| S-003 | B | One step table shows who, reads, writes and calls at a glance. |
| S-004 | A | Explicit kernel, contract, adapter split is the reuse seam adopters need. |
| S-005 | A | Single state document with per-row history; simplest to read and maintain. |
| S-006 | A | Named error codes per edge make each refusal testable. |
| S-007 | B | Worked example on real flg-r2 counts proves the formula. |
| S-008 | A+C | A's table plus C's separate transaction and rerun subsection. |
| S-009 | A+C | A's named test cases plus C's fixtures folder. |
| S-010 | B | Per-replicate traces and arithmetic make the forecast auditable. |
| S-011 | B | Evidence column and REMOVED/LEFT verdict are more honest. |
| S-012 | A+B | One end table is easier to maintain than inline labels everywhere. |
| S-013 | A+B | One design doc suffices for an experimental variant; user guide premature. |
| S-014 | B | Explicit UNVERIFIED list is the most useful closing item. |
| S-015 | B | Dense tables carry more per line than one-sentence lines. |
| C-001 | A | Pretty-printed state object with history; C's seq can be added later. |
| C-002 | A | Path derivable from the document survives a lost flag. |
| C-003 | A+C | A's per-review snapshots plus C's stored diffs with old and new ranges. |
| C-004 | A | Sessions call their own subcommand; no coordinator change, actor inferred. |
| C-005 | A+B | A's status set plus B's T9 script reset on retouch. |
| C-006 | B | Disputed answer needs an explicit verifier ruling. |
| C-007 | B | User-only demotion with quoted words fills A's missing regrade path. |
| C-008 | A | Includes rule tag and caused_by; equivalent elsewhere otherwise. |
| C-009 | A | Profile computes blocking; reviewer cannot choose it. |
| C-010 | B+C | B's count without no-progress halt plus C's integrity and structural escalation. |
| C-011 | B | Count sweep blockers separately (Lt) instead of mixing into B. |
| C-012 | B+C | Outside the cap, in a fresh session. |
| C-013 | C | Separate loop decision and delivery outcome; no early final PASS. |
| C-014 | B | Data show no-progress halt never fires in S1; keep it optional. |
| C-015 | B | Refusal plus `minor_touched` metric detects edits over deferred spans. |
| C-016 | A+B | Reviews 2 and 3, no count cap, plus B's `depends_on` exception. |
| C-017 | B | Soft gate with revert; recording at `open` cannot stall the loop. |
| C-018 | A+B | Normalized unique quote with minimum length, `--at` to disambiguate. |
| C-019 | C | Only relocation algorithm that handles unrelated edits and deletions. |
| C-020 | C | Raw plus normalized sets and kept old spans fix coordinate and deletion gaps. |
| C-021 | A+C | A's result set plus C's `cannot-verify`. |
| C-022 | B | Script reset on retouch is mechanical, not plan-dependent. |
| C-023 | A | `caused_by` computed from hunk attribution, not reviewer-supplied. |
| C-024 | A | Body hash plus report-tail check catches both edit paths. |
| C-025 | A+B | Atomic replace and idempotent answer suffice for one local writer. |
| C-026 | A+B | `sc-review-ledger` name, with B's reason for avoiding the naming trap. |
| C-027 | A+C | A's lean subcommand set with C's JSON stdout and exit-code rule. |
| C-028 | A+B | Copy plus parity test, but omit `## Unattended mode` as B does. |
| C-029 | A | Reviewer keeps panel report; script appends computed tail only. |
| C-030 | A | Review-1 PASS made no edits; a second full read of same text adds little. |
| C-031 | A+C | Profile row plus C's rule that ledger PASS cannot authorize promotion. |
| C-032 | A+C | Profile row plus C's preserved guard order and halt messages. |
| C-033 | A+B | FINAL stays a full audit; defer implement adoption until evidence. |
| C-034 | A | All agree; A's statement is shortest and sufficient. |
| C-035 | A+C | A's dup-matched headline, publishing C's separate components including deferred MAJOR rows. |
| C-036 | B | Forecast derived from traced rows; A's basis is thinner. |
| C-037 | B | Growth derived arithmetically from measured minor-only byte shares. |
| C-038 | A+B | A's criteria plus B's baseline-sweep comparison and `minor_touched`. |
| C-039 | B | Honest about the added sweep dispatch once sweep is a fresh session. |
| C-040 | A+B | V1-ledger compliance check plus B's baseline sweeps and H share. |
| C-041 | B | Cost grounded in real file timestamps and counts six sessions. |
| C-042 | A+B | Minimum anchor length plus a warning, not refusals that stall runs. |
| C-043 | A | Constant tied to cap text by a test. |
| X-001 | C | Sweep blocker changes delivery outcome, not the loop verdict line. |
| X-002 | B+C | Fresh sweep session avoids anchoring on just-verified rows. |
| X-003 | B | No second stop by default; optional flag for rf-qa. |
| X-004 | A+B | Reviews 2 and 3 must record fix-induced rows like N12. |
| X-005 | B | Soft gate detects scope creep without deadlocking an unattended reviser. |
| X-006 | A | Each session calls its subcommand; S1 coordinator unchanged. |
| X-007 | C | Exit 0 for success; decision read from output, never inferred. |
| X-008 | A | Derivable default with override tolerates a lost flag. |
| X-009 | B | Omitting the section keeps the set-equality test green. |
| X-010 | A | One baseline line gives install coverage for the new command. |
| X-011 | A+C | Headline as A, with deferred MAJOR rows published as a separate component. |
| X-012 | B | Most grounded forecast; honest that the conservative bar may fail. |
| X-013 | A | No edits after a review-1 PASS, so the find pass is the sweep. |
| X-014 | A+C | Blocking computed by the script from severity, rule and outcome. |
| X-015 | B | Broken sentence must become a child row, not just a flag. |
| X-016 | A | A carries a `rule` field so FR-8/FR-9 can be computed. |
| X-017 | A | A keeps disputed answers as unchanged status with a reason, unambiguous. |
| X-018 | A+B | One-line brief change holds when sessions call the script; plus sweep dispatch. |
| X-019 | A | Derivable default path, no random id. |
| X-020 | C | Old and new ranges per hunk fix A's coordinate mismatch. |
| X-021 | B+C | Only `fixed` rows can become verified. |
| A-007 | none | Record review-1 grade distribution as covariate; no variant measures inflation. |
| A-008 | none | Add live-document hash check after final decision; growth from accepted snapshot. |
| A-009 | C | C's relocation and `anchor_state` handle drifted anchors. |
| A-010 | C | Old-side ranges and deletion boundaries let deletion defects be anchored. |
| A-011 | none | Extend `depends_on` to verified rows; sweep challenges cover the rest. |
| A-012 | none | State forecasts conditional on review-1 counts and report them beside Arm B. |
