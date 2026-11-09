# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (plus Round 2.5 invariant probe)
- Convergence achieved: 100% (85 of 85)
- Convergence threshold: 75%
- Focus areas: All
- Advocate count: 3
- Round 1 convergence: 74.1% (63 of 85)
- Convergence rule: a point is agreed when at least 2 of 3 advocates give the same normalized pick (computed by /tmp/bs346-tools/convergence.py from the positions tables)

## Round 1: Advocate Statements

### Variant A Advocate (opus:architect)

### Round 1 advocate: Variant A (variant-1-opus-architect.md)

Advocate model: opus. Persona: architect (structure, dependencies, long-term impact). Custom focus: maintainability and extension scaffolding. Sources read in full: variant-1, variant-2, variant-3, diff-analysis.md, seed-brief.md. Section numbers below are each variant's own (A sN, B sN, C sN).

#### Position

Variant A should be the skeleton of the merged spec: its kernel, contract and adapter split with a `PROFILES` table (A s2, s6), its single state document (A s3), its profile-computed `blocking` (A s3) and its subcommand-inferred actor (A s2) give the smallest durable core that four adopters can share. A loses on several loop rules, and the merge should take B's fresh-session sweep and soft-gated unclaimed hunks and C's anchor relocation, old-side diff ranges and split of loop decision from delivery outcome.

#### Steelman of Variant B

The strongest version of B: it is the only variant that traced the failure it claims to fix in the real files. It shows that minor F22 was applied because the brief said "apply confirmed findings" (`F2D1:10`), which wrote the AC-0.4 WC-1 proof that became blocking N5, whose fix became N12 (B s1). From that trace B draws an honest conclusion that A and C do not state as plainly: "If the idea works on S1 it works mostly through the minor-row rule and the computed stop, not through a smaller read" (B s5), because all 8 ctl-r1 review-3 blockers and N12 already anchor inside changed lines. B then builds its measurement around the risk of its own design: a baseline sweep on the six existing final specs (B s9), a hidden-defect share H split by location (B s2 step 5, s9), and a convergence bound "B1 x r x r" that sets the honest ceiling at "escalate with 0 to 3 rows, not always PASS" (B s10). Its five-point self-attack on verify-only (B s10) is the best risk analysis in the set. B also catches two concrete repo traps A missed: a skill named `sc-spec-panel-ledger` would be skipped and deleted by `install_all_skills` (B s6), and copying `## Unattended mode` would break the `UNATTENDED_COMMANDS` set-equality test (B s6). Its sweep design is right on independence: "putting it inside review 3 would make the same session verify and then sweep, so the sweep would be anchored on the rows it just read" (B s4). Its unclaimed-hunk rule is the right middle ground: `revise-check` exits 7 and offers `revert-unclaimed`, while `open` only records, "so a reviser that skips the check does not stall the loop" (B s12 q2).

#### Steelman of Variant C

The strongest version of C: it treats the ledger as a small database and takes correctness under failure seriously. Status is never stored, only replayed from an append-only event list (C s3), so there is no second store to drift. Every mutation carries `--op` and `--expect-seq`, request-digest idempotency and an advisory lock (C s6), so a retried or raced call cannot double-apply. C is the only variant that solves anchor drift properly: "Use unchanged-block line mapping first; then unique exact quote with exact before/after context. Line numbers are hints, never proof" with `anchor_state=missing|ambiguous` escalating (C s3). It is the only one that keeps old-side ranges and zero-width deletion boundaries (C s6), which fixes the coordinate bug in A (X-020) and the deletion blind spot (A-010). C's split of `loop_decision` and `delivery_outcome`, with "no final PASS artifact is emitted early" (C s4), resolves the hollow-PASS problem more cleanly than either A or B. C also adds `cannot-verify` as an honest verifier answer (C s6), says plainly that the sweep is an extra assessment ("Do not claim the total number of assessments is three", C s4), and draws the right line for implement: "Every archive attempt still needs a fresh independent full FINAL" (C s7).

#### Key strengths claimed

1. **One extension seam, fixed in advance.** A splits the work into a kernel (only writer of state), a contract (`SKILL.md`) and an adapter (command plus profile name) (A s2 table). The `PROFILES` table "maps a profile name to its severity vocabulary, its blocking predicate and its cap"; "Adding an adopter is one table entry plus one parametrized test row, never a change to the transitions or the decision formula" (A s6). This is the property that makes reflect, rf-qa and implement adoption cheap and safe. B's alternative, `init --scale <grades> --needs-outcome <grades>` (B s7), pushes the grading rule onto every caller at call time, so two callers of the same tool can grade differently; C names the right idea ("each adapter pins its own grading/stop profile at init; unsupported profiles fail", C s7) but only as future work.
2. **`blocking` is computed, never chosen by a model.** "`blocking` comes from the profile, never from the model" with the 427 predicate copied verbatim (A s3, citing `spec-panel.md:259`). B lets the reviewer supply `sev` and only refuses MAJOR-blocking without `wrong_outcome` (B s2, s6), so a reviewer can file a CRITICAL as minor, and B has no field for the FR-8/FR-9 rule it states (X-016). C agrees with A (C s3, s6). Frozen severity only stops drift if the blocking flag cannot be chosen at creation either.
3. **A plain state document is the cheapest thing to maintain and inspect.** One pretty-printed JSON object with `rows`, each carrying `status`, `answers` and `history` (A s3). A maintainer can read it, `status --json` reports metrics from it directly (A s6, s9), and the per-row `history` already gives the audit trail C wants from replay. It reuses implement's `at`, `anchor`, `origin`, `resolved|open|regressed` vocabulary (A s3, citing `qa.md:137,143`), so adopters learn one vocabulary. C's event replay is stronger under crashes but makes every read a reducer and every schema change a replay migration (C s3, s11 "future unsupported schema versions stop without migration").
4. **The script is callable by the sessions that already exist.** Each session runs its own subcommand and "the actor column says whose input file may request the move, which the script infers from the subcommand" (A s3). That keeps the S1 coordinator unchanged and the brief change to a name plus `--ledger` (A s9). C's "coordinator alone runs ledger mutations" (C s2) contradicts its own one-line brief change (X-018). B's `--as` flag adds a declared role that B itself classes as "IDENTITY is PROSE" (B s11), so it adds a flag without adding enforcement.
5. **A lost flag can neither restart nor strand the loop.** The default ledger path "is derivable from the document path alone" and `init` refuses an existing ledger with `E-EXISTS` "so a lost flag can never restart a first review" (A s2, s3). B stops when `--ledger` is missing (B s6 bullet 1) and C's default contains a random `run-id` that no session can re-derive (X-019), so both depend on the coordinator keeping a path, which is the exact 427 failure the design cites (`spec-panel-review-loop.md:162`).
6. **Accepted text cannot be re-attacked, and the verifier gets a script-built plan.** `E-NOT-CHANGED` refuses `regressed` on a verified row whose span no hunk touched (A s3), and `begin` writes `plan-r<k>.md` with frozen severity, wrong outcome, old and new hunk text, unattributed hunks and `W-NO-ANSWERS` (A s2). This is the concrete replacement for 427's "reviewer re-reads the prior report and rebuilds the status table" (A s5).
7. **Verdict edits are detected.** `begin` refuses when "the prior report's last line equals the recorded verdict" fails (`E-REPORT-EDITED`, A s2, s4), and `body_sha256` gives `E-TAMPERED` (A s3). Neither B nor C checks the report tail at the next step.
8. **The validity check makes the experiment honest about compliance.** V1-ledger: "a replicate whose reviewers never ran the script counts as 'ledger not honoured' and is not treatment", with refusals counted as a covariate (A s9). Without it a replicate that ignored the script would be scored as a ledger result.
9. **The cap is tied to the code by a test.** `CAP_REVIEWS = 3`, `E-CAP` on a fourth `begin`, refusal of a third `answer` cycle, and "A test pins that the constant and the text agree" (A s4). The parity test against `spec-panel.md` (A s6) guards the 480 copied lines against silent drift.

#### Weaknesses identified in Variant B

1. **Grading is a reviewer choice, not a computed field.** `add` rows carry `sev` and `grade` from the reviewer (B s6); the script only refuses `sev=blocking` on a MAJOR without `wrong_outcome` (B s2). A reviewer can file a CRITICAL as `sev=minor` and it is auto-deferred forever. The bullet "CRITICAL and FR-8/FR-9 are blocking" (B s6 bullet 3) has no field to carry the rule tag (X-016), so the script cannot check it.
2. **The adoption seam is call-time flags.** `init --scale ... --needs-outcome ...` (B s2, s7) means every caller restates the grading vocabulary on every run. A typo or a different caller silently changes what blocks. There is no named profile that a test can pin per adopter.
3. **Status set is ambiguous.** T4 keeps the status and sets `claim.action=disputed`, yet T8 lists `disputed` as a From state (B s3, X-017); the `mark` input domain is unclear.
4. **The CLI surface is large and mixes concerns.** Twelve subcommands (B s6) including `render`, `revert-unclaimed`, `show`, `verdict`, plus `close` exit codes 0/10/11 that encode the decision (X-007). A caller that treats non-zero as failure treats CONTINUE as a crash; B's own "the exit code of `close` outranks any sentence of a brief" (B s6 bullet 8) hard-wires that coupling.
5. **A missing flag stops the loop.** "`--ledger <path>` required; without `--ledger` stop and say so" (B s6 bullet 1) makes the run depend on the coordinator keeping the path, the failure mode 427 already has (`DES:162`, cited by B s5).
6. **No concurrency protection while claiming reuse by rf-qa.** B says itself "two parallel QA instances on one ledger lose updates; an adopter needs `fcntl.flock`" (B s7), yet orders rf-qa as the second adopter (B s7).
7. **The sweep's independence rests on prose.** "Sweep reviewer does not read `L`" is PROSE (B s11); the sixth session adds cost (B s11) and the measurement still depends on the instruction being followed.
8. **Forecast mixes a starting point the ledger does not share.** The 7 to 8 P3 for ctl-r1 (B s9 trace table) assumes verify meets the same 8 blockers, but those came from a control loop where minors were applied and the whole document was re-reviewed; the ledger changes both inputs, so the P3s 5.5 forecast is likely pessimistic for the same reason my 2.5 may be optimistic.

#### Weaknesses identified in Variant C

1. **The S1 arm it describes cannot run as stated.** "Only authored brief change: substitute ... on its invocation line" and "do not rewrite the surrounding brief" (C s9) contradict "The coordinator alone runs ledger mutations" (C s2) and "four reviewer sessions including the sweep" (C s11). The S1 coordinator and dispatch list must change (X-018), which is a changed experimental variable C does not record.
2. **The discovery budget cannot record the defect that motivated the theme.** Review 2 may add "at most one new finding C001" and review 3 has "No discovery check remains" (C s2). N12, the fix-induced MAJOR found at review 3 in flg-r2 (seed brief Known Context), could not be a row; a second candidate or more than 200 changed lines forces ESCALATE (C s2). In S1 ctl-r1 review 3 had 88 changed lines and 8 blockers (B s5), so one row per loop would escalate almost every run on overflow, testing the budget rather than the ledger (C s11 concedes "an overflow may dominate S1").
3. **Hard refusal of uncovered edits stalls an unattended reviser.** "each changed old/new line belongs to at least one submitted blocking-row span; uncovered edits fail revision admission" (C s3). A whitespace reflow or a needed FR-8/FR-9 gap fill outside the row span blocks the cycle with no recovery path other than manual work (C s11 "may require manual recovery").
4. **The default path cannot be re-derived.** `<run-id>` is "an opaque random identifier" while "No missing-ledger fallback to a new FIND is allowed" (C s3, s2; X-019). The default is useless unless every caller passes `--ledger` anyway.
5. **The transaction contract is heavier than the experiment needs.** No-replace hard-link publish, directory fsync, refusal of filesystems without these guarantees, fault injection at every sync boundary (C s6). For a single-writer local loop of about 15 calls, atomic temp-file replace (A and B) covers crash safety; the extra machinery multiplies test and maintenance cost and makes the script Linux-local only (C s12 q9).
6. **Event replay makes every reader a reducer.** Status "is obtained by replaying events" (C s3); `status`, metrics, reports and adopters all need the reducer, and a schema change cannot migrate (C s11). A per-row `history` array (A s3) keeps the same audit trail without that cost.
7. **The R3 proxy is not comparable to the control.** `U3` counts every CRITICAL or MAJOR row with "status != verified", including deferred review-1 notes that were never in a fix cycle (C s9, X-011), yet C forecasts the lowest number, 1.5 (C s9, X-012), with a two-sentence basis (S-010). The count and the forecast pull in opposite directions without explanation.
8. **Deferred sweep blockers inside `B_r` blur the two decisions.** "A deferred blocking sweep row also counts" in `B_r` (C s4) while C also has a separate `S` in `delivery_outcome`; the same row can enter both formulas.
9. **Script-written reports remove the panel's output format.** The script "writes `reports/review-N.md` from ledger state" and the coordinator copies it (C s2, s9), which C itself flags as reducing "formatting freedom" (C s12 q3) and breaks the reviewer's existing report contract.

#### Concessions

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

#### Shared assumptions

- **A-007: QUALIFY.** Inflation is a real risk because review 1 becomes the only grading moment and the briefs still say "any finding of any severity is FAIL" (seed brief). It is bounded in A and C because `blocking` is computed and a MAJOR blocks only with a non-empty `wrong_outcome` (A s3), but a model can still write filler outcomes. The merge should record the review-1 grade distribution as a covariate against Arm B's review 1 and let the command's grading bullet state that the brief cannot change a grade (B s6 bullet 8).
- **A-008: REJECT.** It does not hold: the fixed S1 dispatch sends revise 2 and review 3 regardless, and refusing `answer` after a final decision does not stop edits to `D`. The merge needs a mechanical check: after a final decision every later call (and `status`) compares the live `D` hash with the last snapshot and reports post-final edits (C s9 "measure both live D and the accepted snapshot"), and growth is measured on the accepted snapshot only.
- **A-009: REJECT.** For A and B an old anchor can become absent or repeated after unrelated edits. Adopt C's relocation (unchanged-block line map, then unique quote with context, then the reviser span) and escalate on `anchor_state=missing|ambiguous` (C s3).
- **A-010: REJECT.** A defect created by deleting an obligation has no new-side text. New verify-time rows must be allowed to anchor on an old-side range or a zero-width deletion boundary of a hunk (C s6), checked by `E-OUT-OF-SCOPE` against both sides.
- **A-011: QUALIFY.** It holds for local wording fixes but fails for cross-section interactions such as N15 (B s10 item 2). Mitigate inside the loop with B's `depends_on` (B s2 step 4) extended to verified rows: a verified row whose `depends_on` target a hunk touched goes back on the plan. The residual is left to the fresh sweep, whose challenges to verified rows count in the delivery outcome (C s4).
- **A-012: QUALIFY.** Using Arm B review-1 counts is the only data available, but review 1 under the ledger knows it is the only find pass and writes JSON rows, which may raise or lower the count. Forecasts should be stated as conditional on review-1 blocking count, and the measurement should report review-1 row and grade counts next to Arm B's so a shifted find pass is visible.

#### Positions table

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


### Variant B Advocate (sonnet:analyzer)

### Round 1 advocate: Variant B (variant-2-sonnet-analyzer.md, analyzer persona)

Advocate for Variant B. Opposing: Variant A (opus, architect), Variant C (haiku, backend). Inputs read in full: the three variants, `diff-analysis.md`, `seed-brief.md`. I also re-checked three code facts that the dispute depends on (X-009, the install naming trap, X-010); results are cited where used.

#### Position

Variant B is the best base for the merged spec because it is the only one that traces the failure to a root cause in the real files (a minor finding F22 applied under a brief that said "apply confirmed findings", which made blocking N5, whose fix made N12), builds its mechanism and its predictions on that trace, and states plainly that its own conservative forecast probably misses the bar (P3s about 5.5). It has real defects (X-016, X-017, an undefined status for MAJOR rows filed as minor, a sixth session that breaks the one-line brief rule), and the merge should take A's computed-blocking profile and derivable ledger path and C's loop/delivery split, stale-answer binding and relocation handling, while rejecting C's one-row discovery budget and its transaction machinery.

#### Steelman of Variant A

**Strongest version of A.** A treats the ledger as a reusable kernel, not a spec-panel patch. Three parts, each with one job: a script that is the only writer, a contract in `SKILL.md`, and a thin adapter command with a `PROFILES` table (A section 2, section 6). Adding reflect or rf-qa is "one table entry plus one parametrized test row, never a change to the transitions or the decision formula" (A section 6, U-001). That is the cleanest extension seam of the three.

A also gets several mechanical details right that B gets wrong or leaves open:
- `blocking` is computed from a profile "never from the model" (A section 3), so a reviewer cannot file a MAJOR with a real outcome as minor. B lets the reviewer pick `sev` (X-014).
- The default ledger path is derivable from the document path, so a lost `--ledger` flag cannot restart a first review (A section 3, X-008). B stops the run instead.
- `begin` refuses when the previous report's last line differs from the recorded verdict (`E-REPORT-EDITED`, U-002), and `E-NOT-CHANGED` stops a verifier from re-attacking text no hunk touched (U-004).
- A script-written `plan-r<k>.md` hands the verifier frozen severity, wrong outcome and old and new hunk text per row (U-003), and the V1-ledger validity check says a replicate whose reviewers never ran the script is not treatment (U-005).
- A PASS at review 1 needs no sweep because review 1 already was a whole-document pass (C-030). That is logically right and cheaper than B.
- Running the sweep in the review-3 session adds no session and keeps the S1 briefs close to the one-line substitution the seed brief demands (C-039).

What A genuinely gets right is the architecture of reuse and the amount of state the script owns without a second dispatch.

#### Steelman of Variant C

**Strongest version of C.** C takes "the script, not a model, owns the state" to its logical end. The ledger is an event log: status is never stored, it is recomputed by replay, every mutation carries `--op` and `--expect-seq`, and a repeated operation with the same digest returns the original result (C section 3, section 6, U-019). Packets bind schema, round, document hash and ledger sequence, so a stale answer from an old or resumed session cannot advance newer state (U-024). Honest nonclaims run through the whole text: "Do not claim the total number of assessments is three" (C section 4), "A low raw B3 with a combined proxy above 3 is suppression, not convergence" (C section 9).

C also names things the others leave blurred:
- `loop_decision` versus `delivery_outcome`, with "no final PASS artifact emitted early" (U-021). This is the cleanest answer to the question of what a sweep blocker does to the verdict.
- `cannot-verify` as a legal verifier answer and a structural escalation term `X_r` plus an integrity predicate `I` (U-022, U-023), so the loop fails closed instead of guessing.
- A per-revision anchor mapping with a tombstone for deletions and `anchor_state=missing|ambiguous` (C section 3), the only variant that addresses what happens to an anchor after unrelated edits or a pure deletion (A-009, A-010).
- A sweep may challenge a previously verified row (C section 4), the only variant that gives the "edit elsewhere broke an accepted fix" case (A-011) a path into the count.
- Its headline R3 count includes deferred MAJOR notes (X-011), which is closer to what the control's whole-document review 3 would have reported.

What C genuinely gets right is fail-closed integrity and a precise vocabulary for outcomes.

#### Key strengths claimed

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

#### Weaknesses identified in Variant A

1. **The sweep runs in the same session that just verified (A section 2 review 3 step 2; section 11 "Sessions: none added"; C-012, X-002).** That session has read every plan row and every hunk, so the one whole-document guard is anchored on exactly the rows it is meant to second-guess. A's own open question 3 asks whether it should be a separate session. Shared assumption A-017 ("the sweep reviewer has not been anchored") is contradicted by A's design. B and C both use a fresh session.
2. **Sweep blockers never change the verdict (A section 2; X-001, C-013).** A's report would print PASS next to `sweep: 2 blocking` (A section 11 risk 1 admits it). That is the "hollow PASS" B warns about (B section 10 point 4). It also makes the same S1 run PASS under A and ESCALATE under B and C. At minimum A needs C's `loop_decision` / `delivery_outcome` split.
3. **The no-progress ESCALATE at review 2 (A section 4; C-014, X-003).** A's rule `B(2) >= B(1)` counts fix-induced rows in B(2), so a reviser who fixes 2 of 3 blockers and introduces 2 new ones is escalated although the original blockers fell. On the real flg-r2 counts the blocking numbers went 13, 6, 1, so the rule would never fire there; its only effect is to end a loop one review early elsewhere. A admits it "changes what R3 means" (A section 12 question 1), which breaks the measurement: R3 is undefined for a loop that ended at review 2.
4. **A verifier can clear a row nobody fixed (A section 3 transition table, X-021).** A allows `open`, `fixed` and `reopened` to move to `verified`. A lazy `resolved` with any quote then shrinks `B(k)` without a fix. B refuses `mark` on anything but `fixed` or a ruled dispute, and C keeps unfixed rows open. This is the mechanical hole that the whole design is meant to close.
5. **Span coordinates are inconsistent (X-020).** A stores spans like `"span": "r2:220-220"` and defines hunks "as new-file line ranges", then allows `regressed` only if the stored span overlaps a hunk of this round. At review 3 an r2-coordinate span is compared with r3-coordinate hunks. Retouch detection can misfire in either direction, and misfires are refusals that stall an unattended loop. B stores claims as quotes and re-locates them; C stores old and new ranges.
6. **Unclaimed edits are reported but not undone (A section 11, X-005).** A's table says "Unlisted related edits: detected and reported, not prevented". The F22 chain is exactly an edit that survives in the document. A refuses the `answer` on a deferred row, but the text the reviser already wrote stays. B's `revert-unclaimed` removes it.
7. **The prediction basis looks mislabelled (A section 9).** A writes "R1 blocking in Arm B was about 5 to 6 under 427 grading (the R2 proxy fell from 16-17 to 5-6)". As I read it, 5 to 6 is the review-2 proxy of the flg runs, not review-1 blocking; B's trace puts flg-r2 review-1 blocking at 13 (`F2D1:39`). If so, A's 2.5 forecast rests on the wrong quantity (this is A-012 in its worst form).
8. **Copy keeps `## Unattended mode` (X-009).** See strength 7: the retained heading (spec-panel.md line 451) breaks the `UNATTENDED_COMMANDS` set-equality check unless that set is edited. I read lines 451 to 461 and they do not mention the removed re-review flags, so this is a test problem, not a wrong-flag problem. A could also keep the section and add the name to the set; it does not say so.
9. **Minor scope creep (X-010).** A edits `tests/unit/test_cli_install.py`; the check is presence-only (`_assert_present`, line 501), so the edit is not required.

#### Weaknesses identified in Variant C

1. **C's S1 arm is not the one it claims (C section 9 against section 2 and section 11; X-018, A-006).** C says "Only authored brief change: substitute `/sc:spec-panel` with `/sc:spec-panel-ledger --ledger <absolute-run-path>`" and "do not rewrite the surrounding brief". But "The coordinator alone runs ledger mutations", reviewers receive packets, and the loop uses four reviewer sessions plus two reviser sessions. The coordinator and the dispatch list must change, which changes the experimental variable the seed brief fixes. B at least states its deviation (a sixth session) as a deviation.
2. **The one-row discovery budget would end the real trace at review 2 (C section 2 step 3; C-016, X-004).** C allows at most one new finding C001, only in review 2, and "two candidates or more than 200 changed lines yields ESCALATE". On flg-r2, review 2 found 6 new blocking rows (`F2R2:13`). C would ESCALATE there, so cycle 2 never runs and S1 tests the overflow rule, not convergence. C's own risk table admits it ("an overflow may dominate S1 rather than test convergence"; open question 2). With no discovery in review 3, an N12-type defect is not a row at all; it becomes a regression observation. C's forecast of 1.5 is not consistent with its own mechanism on the real data.
3. **A transaction contract far beyond what a two-cycle experiment needs (C section 6; C-025).** Advisory lock, fsync on every artifact, no-replace hard-link publication, directory sync, "Refuse filesystems without these local publication guarantees", and fault injection at every boundary. The S1 loop is five or six sequential sessions on one Linux host. Atomic `os.replace` plus a plain `flock` and an operation id gives the same safety for the failures that actually occur. The extra machinery is code that can itself fail and stall a loop; C lists 17 risk rows in section 11. This breaches the scope-discipline rule.
4. **Hard refusal of uncovered edits has no escape (C section 3; C-017, X-005).** "uncovered edits fail revision admission" with no way to revert. A reviser who fills an FR-8/FR-9 gap in text no row names (A's open question 4 cites `spec-panel-review-loop.md:73`) hits a refusal and an unattended run stalls. B pairs the check with `revert-unclaimed`; the merge should take C's strictness and B's escape together.
5. **The default ledger path cannot be derived (X-019, C-002).** The default includes a random `run-id`, so a session cannot re-derive it; the default only works if the coordinator passes `--ledger` on every call. That is the failure `DES:162` describes (coordinator drops the saved copy and the run becomes a first review), now moved to the coordinator's memory.
6. **No parity guard for the command body (C-028).** C's outline names six items and no copy rule or drift test, so the 486-line panel text can silently diverge from `spec-panel.md`. A and B both define a parity test.
7. **Exit 0 on ESCALATE (X-007).** "An operation may successfully commit an ESCALATE decision and exit 0". A shell-level coordinator that checks `$?` reads success. B's `close` returns 10 for CONTINUE and 11 for ESCALATE, and states that the exit code outranks any sentence of a brief, which is the exact failure in `F2R3:15`.
8. **No way out of a wrong frozen blocker (C section 3, C-007).** "No automatic blocking deferral or user-waiver API in version 1." A false first-pass blocker forces FAIL forever. B's T10 and A's escalation-to-user are at least recorded exits.
9. **Reduced reporting freedom (C section 12 question 3).** The script writes the report from ledger state, so the panel's own expert prose is replaced. A and B keep the reviewer's report and append script lines.

#### Concessions

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

#### Shared assumptions

- **A-007: QUALIFY.** The assumption is that brief text ("any finding of any severity is FAIL") does not inflate review-1 grades. It is not safe. The round-3 report still graded FAIL on that sentence (`F2R3:15`), so the brief has already beaten the command once. Review 1 is the only grading moment and grades freeze, so a MINOR filed as MAJOR with a filler `wrong_outcome` becomes a blocking row for the whole loop; my own table says "`wrong_outcome` can be filler". No variant measures it. Condition: treat it as a named risk, record the review-1 blocking count and the share of blocking rows whose `wrong_outcome` an analyst judges filler, compare with Arm B's review 1 (13 blocking in flg-r2), and keep the Precedence bullet that a brief cannot change a severity.
- **A-008: QUALIFY.** It holds only if something stops the S1 dispatch. With the verbatim briefs T05 to T09 (`DEC:59`, `DEC:64`) a revise-2 session still runs after an early PASS, and `answer` being refused in phase `closed` does not stop it editing the document. B omits the Reviser brief when the verdict is not CONTINUE, which tells that reviser there is nothing to do, but a brief that says "apply confirmed findings" can still push edits. Condition: measure growth at the snapshot of the final decision (C's carry-forward rule), surface any later change to the document as a mismatch, and make `close` print "no revision: do not edit" in the report.
- **A-009: QUALIFY.** An old anchor usually stays unique, because changed lines were 7.9% (flg-r2) and 24.2% (ctl-r1) of the document at review 3, but "usually" is not a check. B's `add` proves uniqueness only at creation, and `open` prints hunks only for `fixed` rows, so an unanswered `open` row has no relocation. A later insertion that repeats the phrase makes the row ambiguous. Condition: `open` re-resolves every unmoved row's anchor and reports `anchor_state=ok|missing|ambiguous` (C's idea), and a missing or ambiguous row yields ESCALATE with the row listed, never a guess.
- **A-010: REJECT.** It is false for a pure deletion: a fix that removes a sentence can lose an obligation, and the deleted text is not present on the new side, so B's rule that an anchor be byte-present in `DOC` and inside a hunk cannot file it. B's `depends_on` quotes a changed line, which for a deletion is also absent. Cheap repair: accept an anchor within the three context lines B already prints around a deletion hunk, mark the row `origin=deleted-near`, and keep the old-side range (C's deletion boundary). Until then such defects wait for the sweep.
- **A-011: REJECT.** An edit elsewhere can invalidate an accepted fix. N12 is that pattern: the N5 fix added a "record the agent command" step that interacted with other sections (`F2R3:35`), and N15 was an unchanged step contradicted by 2.3 (`F2R3:99-101`). B's own section 10 point 2 calls interaction defects "the likely casualties". T9 resets a verified row only when a hunk overlaps its claim span. Repair: take C's sweep challenges (a sweep may challenge a verified row, which enters the delivery count), and add a cheap lexical cross-check at `open` (a hunk that contains an identifier such as AC-0.4 or WC-1 named in a verified row's claim re-opens that row for a second look). This is a heuristic and must be labelled one.
- **A-012: QUALIFY.** All three forecasts lean on Arm B's review-1 counts, and under the ledger review 1 changes: the reviewer knows it is the only find pass and must write anchored JSON rows with a `wrong_outcome` for every blocking MAJOR. The count could rise or fall. B's formula B1 x r x r makes the sensitivity visible (B1 = 13 gives 1.0 at the measured ratios; B1 = 6 would give 0.5), and I would use it. Condition: pre-register that the S1 prediction is recomputed from the actual review-1 count, and report review-1 blocking per replicate as a covariate.

#### Positions table

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



### Variant C Advocate (haiku:backend)

### Round 1 Advocate C

#### Position

Variant C supplies the strongest transaction and response contract: retries cannot consume extra reviews, stale answers cannot advance the run, and a sweep blocker cannot coexist with a final clean PASS. Merge that foundation with A's component boundaries and B's traced failure analysis, but correct C's experiment contradictions, replace its unsupported optimistic forecast, and do not confuse fewer admitted findings with fewer document defects.

#### Steelman of Variant A

A offers the clearest maintainable division of work. Section 2 makes the kernel the "ONLY writer of ledger state", separates its contract from the adapter, and hands fresh verifiers a generated plan rather than another prose report to reinterpret. Section 3 refuses regrading and forbids reopening untouched accepted text, directly addressing moving goalposts without requiring one persistent reviewer conversation.

A also resists a measurement shortcut. Section 9 says "counting the ledger alone would let the ledger win by not looking" and includes sweep findings in its headline proxy. Its strongest case is a small reusable kernel, predictable review packets, and visible evidence of remaining defects, not merely a nicer status table. Those strengths should survive the merge even where its outcome and coordinate rules need correction.

#### Steelman of Variant B

B provides the strongest account of what actually causes work to grow. Section 1 traces the minor F22 edit into blocking N5 and then N12, explicitly showing how "A prose rule lost to a brief." Section 5 concedes that "the review surface does not shrink much" because the real blockers already had changed-line anchors. That is important counter-evidence against claiming that narrow VERIFY alone solves convergence.

B also makes the strongest experimental challenge to its own proposal. Section 9 adds baseline sweeps and predicts "P3s: mean about 5.5", while section 10 explains that "The reviser still writes the defects." Its fresh sweep and separate final outcome protect against declaring success merely because discovery moved later. Its strongest argument is that ledger machinery should be tested as a limited control on edits and counting, not sold as an automatic improvement in semantic quality.

#### Key strengths claimed

1. **Retries and races have explicit meanings.** C section 6 requires a "nonblocking OS advisory lock", `--op`, and `--expect-seq`. "An identical op and request digest returns its original prefix-derived result without appending"; changed content under the same operation is refused. This is real idempotency, unlike treating a repeated command that errors as equivalent to recovering its result. The lock and sequence check protect against duplicate dispatch even when one coordinator is the intended writer.
2. **The ledger has one authoritative history.** C section 3 says "The only authoritative state is ledger.json" and "A row's current status is obtained by replaying events." Section 6 publishes immutable dependencies before committing their references and describes crash outcomes on either side of ledger publication. Reports can be rebuilt without guessing whether a report footer or a separate status object won a partial update.
3. **Actor responses are bound to the state they reviewed.** C section 2 says packets bind "response schema, round, document hash and ledger sequence". Section 6 requires exact answer coverage, snapshot-range evidence, and closed input shapes. A syntactically valid answer from an older session cannot silently certify a newer revision. This is validation of evidence, not authentication of the actor or proof that its judgment is true.
4. **Clean PASS is a delivery contract, not a provisional count.** C section 4 says "Before sweep completion, PASS is explicitly loop_decision, never delivery_outcome" and "no final PASS artifact is emitted early." A new sweep blocker, challenge to an old verification, or unresolved uncertainty forces delivery escalation. This genuinely improves A's contract while making B's two-stage outcome explicit.
5. **Edit ownership is checked before acceptance.** C section 3 requires "each changed old/new line" to belong to a submitted blocking-row span; uncovered edits fail admission. Section 6 keeps raw hunks for ownership and excludes whitespace-only changes only from discovery. This closes the path where skipping an optional check admits unrelated edits. It does not prove that a claimed edit was necessary.
6. **Deletion and relocation have defined failure outcomes.** C section 3 says "An empty replacement is a tombstone, not proof of resolution" and rejects silent nearest-match selection for repeated quotes. Section 6 retains old deletion spans and new insertion boundaries. Missing or ambiguous evidence cannot turn into a successful verification simply because the offending words disappeared.
7. **Operational uncertainty is surfaced instead of rounded down.** C section 4 uses integrity `I`, structural failures `X_r`, and an explicit pending result. Section 6 separates successful operation execution from document outcome: "callers inspect JSON, never infer PASS from process success." Section 11 openly limits the system to local storage and calls its history "crash safety, not tamper-proof audit storage".

#### Weaknesses identified in Variant A

1. **Its final verdict can contradict its evidence.** A section 2 says "Sweep rows never change the verdict"; section 11 accepts that "a PASS can stand next to sweep: 2 blocking". This fails the goal of a clean PASS or justified escalation. C section 4's separate delivery outcome fixes that without permitting another automatic fix cycle.
2. **Scope enforcement can be bypassed by omission.** A section 11 says "unattributed hunks are reported, not refused" and that rows can verify without answers under `W-NO-ANSWERS`. Reporting is useful, but cannot mechanically stop the minor-edit chain that B traced. C section 3's admission check is stronger, provided refusals include a safe recovery path.
3. **Its retouch check compares incompletely specified coordinates.** A section 3 describes hunks as "new-file line ranges", while its stored example span belongs to the prior snapshot. Requiring overlap without old-side ranges or relocation can miss a retouch when earlier lines move. C sections 3 and 6 retain snapshot-qualified mappings and both sides of the diff. This is X-020, not a stylistic preference.
4. **Its early stop changes policy without evidence of necessity.** A section 4 escalates at review 2 when `B(2) >= B(1)`. B section 4 explains that the analogous proxy decreased in all six observed S1 runs, while C preserves the existing cap without importing rf-qa's policy. Equal counts can also conceal replacement of difficult blockers with simpler ones. Preserve rf-qa's stricter rule in its own adapter instead of adding it to spec-panel.
5. **Its reusable-profile claim is too broad.** A section 6 says an adopter requires "one table entry plus one parametrized test row, never a change to the transitions or the decision formula." Yet C section 7 identifies rf-qa's ordered halt guards and implement's mandatory fresh FINALs. Reuse storage and validation; do not assume every tool's authority and stop policy reduce to severity plus a cap.

#### Weaknesses identified in Variant B

1. **Atomic replacement does not prevent lost updates.** B section 7 acknowledges that "two parallel QA instances on one ledger lose updates" and defers locking. Even a nominally single-writer experiment can receive retried or overlapping dispatches. C section 6's lock, expected sequence, and request identity are preferable before admitting any mutations.
2. **The blocking contract has a missing input.** B section 6 promises "CRITICAL and FR-8/FR-9 are blocking", but its `add` schema has no rule or criterion field and accepts reviewer-supplied `sev`. A and C instead derive blocking from an explicit profile and criterion. B's current contract cannot mechanically enforce its own stated FR exceptions, as X-016 observes.
3. **Its scope gate remains optional in effect.** B section 12 says that a reviser skipping `revise-check` "does not stall the loop" because `open` only records unclaimed hunks. That avoids an unattended refusal but also admits the very scope expansion being tested. C's admission boundary is stronger. Automatic `revert-unclaimed` is not a substitute for a preimage check and explicit authorization to discard live edits.
4. **Its dispute representation is inconsistent.** B section 3 T4 preserves status and sets `claim.action=disputed`, while T8 starts from a status named `disputed`. That ambiguity matters to exact row coverage and unresolved counts. Keep the five-state model and represent a dispute as evidence, not a sixth state introduced accidentally. C conservatively escalates unresolved disputes; a later human ruling needs a separate explicit contract.
5. **Its headline metric needs identity-based deduplication.** B section 9 defines P3s as P3 "plus the sweep's rows" without specifying the union rule A and C provide. A fresh blinded sweep may rediscover an open row. Counting it twice inflates failure; discarding a challenge to a verified row hides failure. Keep B's baseline sweeps, but adjudicate duplicates and challenges before applying either arm's bar.

#### Concessions

1. **X-018 is a real contradiction, not a wording issue.** C section 9 promises "Only authored brief change" is an invocation substitution, but section 2 makes the coordinator run every mutation and section 11 requires four reviewer sessions. The existing fixed dispatch cannot acquire that behavior from a renamed command alone. Keep actor briefs unchanged apart from the invocation, but explicitly preregister the coordinator state checks and added sweep dispatch as treatment changes. B section 9 is more honest about the sixth session. If the one-line restriction also forbids coordinator changes, C as written is not executable under that restriction; report the conflict instead of claiming compliance.
2. **X-019 requires removing the resumable-default claim.** C section 3's random run directory cannot be re-derived after losing its path. For version 1, require the same explicit absolute ledger path on initialization and resume, with no random default selection by the command. A random run id can remain metadata. If the path is lost or missing, stop, never silently create a replacement FIND. A's deterministic location is more convenient, but silently choosing among runs is unacceptable.
3. **X-011 changes the metric, so C's forecast is not comparable as printed.** C section 9 counts every unverified CRITICAL/MAJOR row, including deferred MAJOR notes. A and B omit those notes from their raw unresolved sets. Counting them is conservative, but it changes the historical proxy's population. Preregister a common, independently adjudicated end-state proxy for both arms, deduplicate sweep identities, include challenges to verified rows, and publish deferred MAJOR notes separately. Until controls are rescored under the same rule, do not compare C's 1.5 directly with control 6.0 as an estimated treatment effect.
4. **C's optimistic forecast is unsupported.** Section 9 predicts headline counts 1 and 2, mean 1.5, and growth 20% and 25%, mean 22.5%. Its stricter count and missing trace-based derivation do not justify the lowest forecast. B's roughly 5.5 combined proxy and 23% growth are better planning estimates, still unmeasured and not transferable without adjustment to C's stricter mechanism. The quality bar of 3 may fail even if the growth bar of 44.4% passes. Keep control 6.0 and 63.5% as the supplied reference, not proof that C will beat it.
5. **C's one-row discovery quota is arbitrary.** C section 2 permits only C001 at review 2 and no discovery at review 3. It can record a later N12-like harm as an escalation observation, but should retain the complete structured allegation for audit and measurement rather than make identity depend on an exhausted quota. Prefer finite changed-range packets in both VERIFY rounds, with explicit completeness and overflow escalation; a row-count cap must not suppress evidence. Large repairs may justifiably escalate, but that is not convergence.
6. **The extra sweep violates a literal three-assessment interpretation.** C section 4 correctly admits "Do not claim the total number of assessments is three." Three remediation reviews plus one terminal sweep is the proposed contract, not three total assessments. Obtain an explicit policy decision if the goal instead means three total reviewer assessments. Neither renaming the fourth pass nor running it in the third session resolves that semantic conflict.
7. **Other limits remain real.** A shared operating-system account can bypass the helper, freeze can preserve an inflated first grade, and exact evidence does not prove a correct fix. C's supporting-context rule does not define enough dependency coverage to prevent cross-section regressions. Its duplicated schema validator needs executable parity fixtures; its durability machinery needs measured cost and filesystem tests. For this debate I read the supplied variants, diff analysis, and brief, not the underlying experiment logs or implementation sources, and ran no implementation tests.

#### Shared assumptions

- **A-007: REJECT.** Freezing severity cannot prevent brief-driven inflation before the freeze. C section 11 already admits bad first-pass grading, but none measures this pressure. Retain raw review-1 grades and obtain blinded independent grading under the same rubric in both arms; report disagreement rather than silently modifying frozen operational rows.
- **A-008: QUALIFY.** Early termination is valid only if the dispatcher checks the authoritative next action before every actor launch and no previously launched reviser remains active. A refused ledger transition does not undo edits to the live document. Add and test that dispatch gate, record terminal bytes, and treat later live-document changes as an integrity failure. This is a disclosed coordinator change, not an assumed property of unchanged briefs.
- **A-009: REJECT.** A unique initial quote can later disappear or become duplicated. Use C section 3's snapshot-qualified relocation, exact context, and missing/ambiguous outcomes for every live row; unchanged status is not proof of a valid anchor.
- **A-010: REJECT.** Removing a requirement can create harm without leaving any new-side quote. C section 6's old ranges and tombstone boundaries are necessary evidence locations, followed by a semantic check that deleting the obligation was legitimate.
- **A-011: REJECT.** A remote change can contradict a previously correct fix without touching its sentence. C's undefined supporting context is not enough. Record explicit supporting passages and requirement dependencies, invalidate verification when those change, and escalate uncertain dependency coverage. Keep the independent sweep for undeclared interactions; do not claim this completely solves semantic dependency discovery.
- **A-012: QUALIFY.** Historical review-1 counts are useful planning priors, not invariants. Knowing FIND is unique, writing structured rows, and responding to an unchanged aggressive brief can alter findings and grades. Measure review-1 count, grading distribution, output cost, and blinded grading disagreement; condition forecasts on those observations instead of assuming Arm B equivalence.

#### Positions table

Preferences select the strongest supplied approach unless `none` explicitly proposes a correction absent from all three. Forecast preferences rate support for the estimate, not a measured result. Cross-variant combinations retain their useful parts, not every quoted claim.

| Point | Preferred | Reason |
|---|---|---|
| S-001 | A | Specific titles expose compatibility obligations instead of hiding adopter differences. |
| S-002 | B | Explicit citation aliases and unverified markers make provenance easier to audit. |
| S-003 | B | Actor, input, output, and call order are visible together. |
| S-004 | A | Kernel, contract, and adapter boundaries clarify ownership; adapter policy still needs testing. |
| S-005 | C | Replay avoids inconsistent current-state and history stores in this bounded ledger. |
| S-006 | B | Numbered transitions and phase columns improve coverage, after fixing disputed-state inconsistency. |
| S-007 | B+C | Combine worked decisions with explicit integrity, pending, and delivery states. |
| S-008 | B+C | Use a command table plus closed schemas and transaction guarantees. |
| S-009 | C | Fixtures and crash-boundary tests directly exercise persistence and evidence failures. |
| S-010 | B | Trace-based estimates expose assumptions better than unsupported optimistic point forecasts. |
| S-011 | B | Evidence, residual causes, and self-attack prevent overstating what the ledger fixes. |
| S-012 | C | Local labels distinguish structural enforcement from semantic judgment where each rule appears. |
| S-013 | C | Schemas, fixtures, and recovery guidance support an executable contract rather than prose alone. |
| S-014 | B | An explicit unverified inventory is more honest than prematurely declaring completion. |
| S-015 | A | Moderate prose and tables are easier to scan than either dense aliases or repeated labels. |
| C-001 | C | Closed event schemas, stable operations, and replay provide a precise durable contract. |
| C-002 | B | Require an explicit ledger path; missing identity must not create a new run. |
| C-003 | C | Snapshot admission and old/new diff ranges bind each accepted revision to its evidence. |
| C-004 | C | Coordinator-owned mutations keep model responses as untrusted evidence, not direct state changes. |
| C-005 | C | History-derived reopening and retouch invalidation preserve the meaning of prior verification. |
| C-006 | A+C | Preserve unresolved state and dispute evidence; do not invent an ambiguous disputed status. |
| C-007 | A+C | Escalate grading disputes; avoid a waiver API whose quoted authority cannot be authenticated. |
| C-008 | C | Freeze issue text as well as severity so verification cannot redefine the original defect. |
| C-009 | A+C | Compute blocking from an explicit criterion and profile, never reviewer-supplied blocking labels. |
| C-010 | C | Incomplete evidence, uncertainty, and integrity failures cannot yield an accidental PASS. |
| C-011 | B+C | Every unresolved blocker affects delivery; keep loop and sweep counts explicit and nonoverlapping. |
| C-012 | C | Count the extra assessment honestly; session naming cannot erase its cost. |
| C-013 | C | Distinct provisional and delivery outcomes prevent publishing PASS before the sweep. |
| C-014 | B+C | Preserve spec-panel's cap; structural uncertainty escalates without importing rf-qa's monotonicity policy. |
| C-015 | B+C | Combine admission refusal for note-sponsored edits with measured minor-span touches. |
| C-016 | none | Inspect finite changed packets both rounds; retain all allegations and escalate incomplete coverage. |
| C-017 | C | Reject uncovered edits before acceptance; recording them later does not enforce scope. |
| C-018 | C | Exact context and snapshot identity disambiguate anchors without trusting line hints alone. |
| C-019 | C | Explicit relocation and deletion tombstones avoid silent nearest-match errors. |
| C-020 | C | Raw ownership and dual-sided ranges preserve deletions and whitespace-sensitive evidence. |
| C-021 | C | Snapshot-range evidence and cannot-verify distinguish uncertainty from an asserted resolution. |
| C-022 | none | Track explicit dependency passages; invalidate verification when relevant remote supporting text changes. |
| C-023 | C | Hunk overlap proves location, not causation; preserve independent causal adjudication. |
| C-024 | A+C | Add accidental-edit checksums to packet binding; neither mechanism authenticates deliberate editors. |
| C-025 | C | Locks, sequence checks, durable publication, and stable operation retries prevent lost or duplicate reviews. |
| C-026 | B | Its installation naming analysis supplies the clearest packaging and activation contract. |
| C-027 | C | Machine-readable outcomes separate successful commits from review decisions and operational failures. |
| C-028 | B | Drift tests preserve the panel while explicitly excluding unsupported unattended behavior. |
| C-029 | C | Generate reports from authoritative state rather than combining conflicting model tables and computed tails. |
| C-030 | B+C | Even review-1 PASS requires an independent terminal sweep under the proposed sweep policy. |
| C-031 | C | Merge before assigning identities; ledger cleanliness cannot grant promotion authority. |
| C-032 | C | Preserve regression, monotonicity, and cap order rather than flattening rf-qa's stop rules. |
| C-033 | B+C | Defer adoption; any later sidecar must preserve mandatory fresh independent FINALs. |
| C-034 | C | Session continuity is optional; packet identity and file state remain authoritative. |
| C-035 | none | Preregister one deduplicated proxy for both arms; report deferred MAJOR notes separately. |
| C-036 | B | Its conservative estimate has trace-based support and acknowledges likely quality-bar failure. |
| C-037 | B | Byte-share arithmetic is stronger evidence than an unexplained growth forecast. |
| C-038 | B+C | Preserve fixed bars and spread rules; add baseline-sweep, leakage, and operational failure checks. |
| C-039 | none | Disclose coordinator gating and the added sweep separately from unchanged actor brief text. |
| C-040 | B+C | Baseline sweeps detect hidden defects; hashes and snapshot comparisons verify actual treatment activation. |
| C-041 | B+C | Count the sixth session and all calls; distinguish estimates from observed durations. |
| C-042 | none | Calibrate resource limits before preregistration; arbitrary discovery quotas must never discard evidence. |
| C-043 | A+C | Preserve pinned cap tests and history-derived refusal of repeated FIND, extra fixes, and sweeps. |
| X-001 | B+C | A sweep blocker prevents final PASS without authorizing another automatic fix cycle. |
| X-002 | B+C | A fresh terminal reviewer reduces anchoring; count its extra session explicitly. |
| X-003 | B+C | No evidence requires an additional spec-panel monotonicity stop; retain adopter-specific guards separately. |
| X-004 | none | Both VERIFY rounds need complete bounded packets, not C's arbitrary one-row discovery allowance. |
| X-005 | C | Admission must reject unclaimed edits even when a reviser skips optional checks. |
| X-006 | C | One mutation owner plus typed evidence simplifies coordination and retry responsibility. |
| X-007 | C | A committed escalation is operational success; consumers must inspect the explicit decision field. |
| X-008 | B | Missing explicit ledger identity must stop execution rather than select a new run. |
| X-009 | B | Its explicit omission avoids claiming an unattended contract the variant has not established. |
| X-010 | B | Presence-only baseline checks do not justify changing unrelated installation lists. |
| X-011 | none | Reconcile deferred-MAJOR treatment through a common rescored proxy before comparing headline counts. |
| X-012 | B | Trace-based pessimism is more credible than C's unexplained lowest forecast. |
| X-013 | B+C | FIND alone is not independent validation; terminal PASS still needs the fresh sweep. |
| X-014 | A+C | The script derives blocking from criteria instead of trusting reviewer-selected severity classes. |
| X-015 | B | Preserve original resolution plus an explicit graded child; do not accept an unexplained broken-sentence flag. |
| X-016 | A+C | Include criterion in the input and derive FR blocking mechanically. |
| X-017 | A+C | Keep dispute evidence separate from the five-state status machine. |
| X-018 | none | Admit additional coordinator and dispatch changes; one-line substitution alone cannot execute C. |
| X-019 | B | Require an explicit persistent path; keep random identifiers as metadata, not resume discovery. |
| X-020 | C | Snapshot-qualified relocation and old/new diff ranges avoid cross-version coordinate comparisons. |
| X-021 | B+C | Require a supported fix or explicit dispute ruling; unanswered rows cannot silently become verified. |
| A-007 | none | Measure blinded review-1 grading disagreement; frozen grades do not prevent initial inflation. |
| A-008 | none | Gate every dispatch on terminal state and detect edits from already-running revisers. |
| A-009 | C | Relocate every live anchor and escalate missing or ambiguous mappings. |
| A-010 | C | Old-side evidence and deletion boundaries allow lost obligations to remain reportable. |
| A-011 | none | Explicit dependency passages must invalidate verification when remote supporting text changes. |
| A-012 | none | Measure changed FIND behavior; historical initial counts are priors, not treatment invariants. |


## Round 2: Rebuttals

### Variant A Rebuttal

### Round 2 rebuttal: Variant A (variant-1-opus-architect.md)

Advocate model: opus. Persona: architect (structure, dependencies, long-term impact). Focus: maintainability and extension scaffolding. Inputs read: round1-advocate-A.md, round1-advocate-B.md, round1-advocate-C.md, diff-analysis.md, variant-1 (A), and the repo and experiment files cited under New evidence. Section numbers are each variant's own (A sN, B sN, C sN). "B-R1" and "C-R1" mean the Round 1 statements of advocates B and C.

#### Response to criticisms

Criticisms are grouped by source. Where B and C raise the same point, I answer once and say so.

##### From advocate B

**B1. The sweep runs in the session that just verified (A s2 review 3, s11 "Sessions: none added"; X-002).** Conceded, as in my Round 1 concession 1. A's own open question 3 already doubted it. I now also accept B-R1's new route as the first choice for S1: the review-3 command spawns the sweep as a fresh subagent told not to read the ledger, which keeps A's unchanged dispatch list and gets B's independence. Whether an S1 worker may spawn a subagent is UNVERIFIED; if it may not, the sweep is a sixth dispatch stated as a deviation (B s9).

**B2. Sweep blockers never change the verdict (A s2, s11 risk 1; X-001).** Conceded (Round 1 concession 2). A's "a PASS can stand next to `sweep: 2 blocking`" is a hollow PASS. Take C's `loop_decision` and `delivery_outcome` split (C s4). C makes the same criticism (C-R1 weakness 1); same answer.

**B3. No-progress ESCALATE at review 2 (A s4; X-003).** Conceded (Round 1 concession 3). New evidence below (rf-qa.md:401, 407) shows the monotonicity guard belongs in the rf-qa profile with its own ordering, not in spec-panel. C-R1 weakness 4 is the same point; same answer.

**B4. A verifier can clear a row nobody fixed (A s3 table; X-021).** Conceded (Round 1 concession 6). Only `fixed -> verified`, plus a verifier ruling on a disputed claim (see X-017 below).

**B5. Span coordinates are inconsistent (X-020).** Conceded (Round 1 concession 4). A writes "giving hunks as new-file line ranges" (A s3 Changed lines) while spans are stored as `"r2:220-220"`. Take C's old and new ranges per hunk and zero-width deletion boundaries (C s6). C-R1 weakness 3 is the same point.

**B6. Unclaimed edits are reported but not undone (A s11, X-005).** Partly conceded. A's table says "Unlisted related edits: detected and reported, not prevented" (A s10 row 3), and that does leave a "related defect" edit in the document. But A's refusal of `answer` on a deferred row (`E-ILLEGAL`, A s3) already closes the exact F22 route, because F22 was a minor row the reviser applied (`disposition.md:37,39`). What A leaves open is the edit no row names. I accept a stronger gate: hard admission check (C) with a script recovery path (B's `revert-unclaimed`). The merged rule is under C-017 below. C-R1 weakness 2 is the same point; same answer.

**B7. The prediction basis looks mislabelled (A s9).** Conceded, and verified. A wrote "R1 blocking in Arm B was about 5 to 6 under 427 grading (the R2 proxy fell from 16-17 to 5-6, `ARMB-REPORT.md:13`)". Line 13 of that file is the row "Critical+major proxy R1 / R2 / R3: 16 / 5 / 6 and 17 / 6 / 1". So 16 to 17 is the R1 proxy and 5 to 6 is the R2 proxy; R1 blocking under 427 grading in flg-r2 was 13 (`disposition.md:39`: "all 13 blocking"). A's 2.5 forecast rests on the wrong quantity. I withdraw it as a forecast and adopt B's B1 x r x r derivation with B1 measured per replicate (A-012 below).

**B8. The copy keeps `## Unattended mode` (X-009).** Conceded, and verified: `_check_no_unattended_sections` globs every command file with that heading and asserts set equality with `UNATTENDED_COMMANDS` (`tests/skills/test_worker_contract.py:831-839`), and `spec-panel.md:451` carries the heading. A's "byte-identical except three blocks" copy would fail it. Omit the section, as B does, and make the parity test exclude it.

**B9. Editing `tests/unit/test_cli_install.py` is scope creep (X-010).** Conceded. The check is presence-only (`_assert_present`, `test_cli_install.py:501`), so the edit is not needed for a green suite. It would add coverage, but it was not asked for; drop it.

**B on C-030 / X-013 (B's steelman agrees with A).** No rebuttal needed; B and I agree that a review-1 PASS made no edits, so a second whole-document pass of the same text adds nothing.

##### From advocate C

**C1. "Its final verdict can contradict its evidence" (C-R1 weakness 1).** Same as B2. Conceded.

**C2. "Scope enforcement can be bypassed by omission" (`W-NO-ANSWERS`, unattributed hunks reported).** Same as B6, plus one more point: under A, a reviser who never runs `answer` makes every hunk unattributed and the rows still verify (A s11 rule table). Conceded. In the merge, `begin` runs the same admission check as `answer`, so skipping `answer` cannot admit edits; `begin` refuses with the exact `revert-unclaimed` command, which the verifier session can run itself, so the loop cannot stall.

**C3. Retouch check compares incompletely specified coordinates.** Same as B5. Conceded.

**C4. The early stop changes policy without evidence.** Same as B3. Conceded.

**C5. "Its reusable-profile claim is too broad" (A s6 "one table entry plus one parametrized test row, never a change to the transitions or the decision formula").** Partly conceded, and checked. rf-qa's rules (`src/superclaude/agents/rf-qa.md:401`, `:407`) are a four-step precedence, "regression -> monotonicity -> hard-cap -> proceed", with byte-exact halt messages. That is not severity plus a cap, so A's sentence is wrong as written. The seam itself survives: a profile entry should carry an ordered list of stop guards chosen from a fixed menu the kernel implements (`regression`, `monotonicity`, `cap`) plus each guard's halt message. Adding a profile that uses existing guards is still one table entry and one test row. Adding a new guard kind is a kernel change with its own tests, and the spec must say so. Implement's mandatory fresh FINAL (C s7) is outside the ledger entirely, which is why I keep implement adoption deferred (C-033).

**C on positions where C preferred its own design over A (argued in C-R1's table rather than its weaknesses list).**

- *C-004 / X-006, coordinator owns all mutations.* Not conceded. C-R1 itself concedes its arm "is not executable under that restriction" (C-R1 concession 1). C's real gain is that model output is untrusted input, and A already gets that: every model-written fact enters through a JSON input file the script validates (A s2 step 3, s6 `E-SCHEMA`). I accept C's packet binding (round, document hash, ledger sequence) on top, so a stale input from an old session is refused, without moving the calls to the coordinator.
- *C-001 / S-005, event replay.* Not conceded. C-R1 strength 2 says reports "can be rebuilt without guessing whether a report footer or a separate status object won a partial update". With one atomic replace of one file there is no partial update to guess about, and A's per-row `history` keeps the audit trail. I accept C's operation id and expected sequence number as header fields, which buys the idempotency C-R1 strength 1 wants without a reducer.
- *C-029, script writes the report.* Not conceded. C-R1's reason is to avoid "combining conflicting model tables and computed tails". Merged fix: the reviewer's prose may not carry its own status table or `verdict:` line; `close` refuses a report that does, appends the rendered table and verdict, and the next `begin` checks the tail (`E-REPORT-EDITED`, A s2). That removes the conflict and keeps the panel output.
- *C-002 / X-008 / X-019, explicit path required.* Not conceded. C-R1 concession 2 drops the random run id and asks for an explicit path. A's derivable default plus `init` refusing an existing ledger (`E-EXISTS`) gives the same safety: a lost flag can neither create a second run nor restart review 1. C's worry, "silently choosing among runs", cannot happen because there is exactly one default per document; `--ledger` stays as an override.

#### Updated assessment

**Variant B after its defense.** B-R1 conceded both intra-B contradictions with repairs I accept: `blocking` becomes a profile output with a `rule` field (X-016), and `disputed` becomes a claim flag with a mandatory verifier ruling (X-017). It also dropped `--as` and offered to fold `render`, `verdict` and `show` into `close` and `status`, which removes most of my CLI-surface criticism (A-R1 weakness 4). Its remaining strengths are larger than I scored them: the F22 to N5 to N12 trace is the only causal account, the B1 x r x r bound is the only honest ceiling, and the baseline sweep is the only reference for "hiding". I now rank B's measurement section (s9, s10) as the base of the merged measurement, and A's as a source of the V1-ledger check only. My one standing objection is decision-coded exits from `close` (X-007): C already supplies a dedicated `verdict` subcommand that encodes the decision (C s6), which serves shell coordinators without making every CONTINUE look like a crash.

**Variant C after its defense.** C-R1 conceded X-018, X-019, X-011's comparability problem, its unsupported 1.5 forecast and the arbitrariness of the one-row discovery budget. With those removed, C's remaining core is strong and mostly additive to A: loop and delivery split, `cannot-verify`, anchor relocation with `missing|ambiguous`, old and new ranges, packet binding and operation ids. Two things I still reject. First, the coordinator-only mutation model, which C-R1 admits cannot run under the one-line brief rule. Second, the heavy publication layer (hard-link publish, directory sync, refusal of filesystems, fault injection at every boundary); `flock`, operation id, expected sequence and one atomic replace cover the failures this loop can have. C-R1's own concession 7 asks for "measured cost and filesystem tests" for that layer, which supports deferring it.

**What this does to A's role.** A remains the right skeleton for structure (kernel, contract, adapter; one state file; computed blocking; subcommand-inferred actor; derivable path; report-tail check), but most of A's loop rules lose: sweep session and authority, no-progress stop, `open -> verified`, coordinates, anchors and unclaimed-edit handling all move to B or C. A's measurement forecast is withdrawn. I count that honestly as A contributing the frame and B and C contributing most of the rules inside it.

#### New evidence

Paths: `W` = `/home/coder/workspaces/worktrees/IronClaude`; `ARMB` = `W/exp346-p1-logs/.dev/experiments/346-validation/phase4/ARMB-REPORT.md`; `DEC` = `W/exp346-p1-logs/.dev/experiments/346-validation/DECISIONS.md`; `F2D1` = `W/exp346-ab-flg-r2/.dev/orca-command-refactor/review/disposition.md`; `F2R3` = `.../spec-panel-round3.md` in the same folder; repo paths are under `W/bs346-ledger/`.

1. **The Arm B proxy counts by grade, not by blocking, so deferred MAJOR rows belong in the ledger headline (X-011, C-035).** `ARMB:37`: "The 427 grading relabels some MAJOR findings as minor (flg-r1: R3-7 and R3-8), so proxy and blocking differ in Arm B and nowhere else. Both are shown." `ARMB:13-14` give the proxy (6 and 1) and the 427 blocking count (4 and 1) as separate rows. The control proxy is therefore "every CRITICAL or MAJOR finding present", graded MAJOR even when 427 called it minor. A ledger headline that skips a MAJOR deferred at review 1 (A s9, B s9) would count fewer things than the control. This moves me from A+C to C on X-011: deferred CRITICAL or MAJOR rows count in the headline, with the blocking-only count published beside it.

2. **A's forecast basis was the wrong row (C-036).** `ARMB:13` "Critical+major proxy R1 / R2 / R3 | ... | 16 / 5 / 6 | 17 / 6 / 1" and `F2D1:39` "21 applied (all 13 blocking, 8 of 9 non-blocking)". R1 blocking for flg-r2 was 13, not 5 to 6. B's B1 = 13 is the correct input.

3. **The existing experiment already uses A's validity rule, so V1-ledger is a continuation, not new machinery (C-040).** `DEC:64` (D11): "a report that ignores the flags is recorded as 'flags not honoured' and does not count as treatment." A's V1-ledger ("a replicate whose reviewers never ran the script counts as 'ledger not honoured'", A s9) is the same rule applied to the new arm. It should be kept next to B's baseline sweeps and C's hash recording; the three check different failures (compliance, hiding, wrong install).

4. **rf-qa's stop rules are ordered guards, not a cap (C-032, C-014, C5 above).** `src/superclaude/agents/rf-qa.md:401`: "see the Retry Monotonicity Protocol below for the full 4-step precedence (regression -> monotonicity -> hard-cap -> proceed)"; `:407`: "Regression detection (runs FIRST per cycle transition)". A profile must carry an ordered guard list with byte-exact halt messages. This confirms C's adoption point and narrows A's extension claim.

5. **The install naming trap is conditional (C-026, U-009).** `src/superclaude/cli/install_skills.py:57`: `return command_path.exists() and skill_name not in skill_activation_targets(command_path)`. A skill `sc-spec-panel-ledger` is skipped only when `commands/spec-panel-ledger.md` does not activate it by name. B's warning is right to avoid the name, but the reason to give implementers is "the name couples the skill to one command and depends on the activation regex", which is also why `sc-review-ledger` (no matching command) is the safer shared name for four adopters.

6. **The Unattended-mode set test is real (X-009, C-028).** `tests/skills/test_worker_contract.py:831-839` asserts `set(have) == set(UNATTENDED_COMMANDS)` over every `commands/*.md` with `^## Unattended mode`; `src/superclaude/commands/spec-panel.md:451` has that heading and `:256` has `## Review Loop`. The parity test must exclude both replaced blocks and the omitted section.

7. **`test_cli_install.py` needs no edit (X-010).** `tests/unit/test_cli_install.py:501` `_assert_present` only checks that listed names exist.

8. **The brief does override the command at review 3, which supports measuring A-007.** `F2R3:15`: "Under the brief, any finding of any severity is FAIL; under the command's own grading the result is also FAIL". The brief's sentence is still applied by the reviewer next to the command's grading, so grade inflation at review 1 is a live risk once review 1 is the only grading moment.

Not checked: whether an S1 worker may spawn a subagent (needed for B-R1's subagent sweep); I did not open the S1 briefs T05 to T09.

#### Proposed resolution of split points

| Point | Proposed merged rule | My pick |
|---|---|---|
| C-005 status set and who may change it | Five statuses `open`, `deferred`, `fixed`, `verified`, `reopened`, written as B's numbered transitions with a phase column; the script sets `deferred` and resets `verified -> fixed` when a hunk overlaps the row's mapped span, `open` versus `reopened` comes from history (C), the reviser requests only `fixed`, the verifier requests `verified` only from `fixed` (or from a ruled dispute) and otherwise `reopened`. | B+C |
| C-008 frozen fields | Freeze A's list (`id`, `label`, `round_found`, `origin`, `caused_by`, `severity`, `rule`, `wrong_outcome`, `blocking`, `anchor`, `at`) plus C's original issue text, so a verifier cannot redefine the defect it is checking; a later input carrying any of them is refused. | A+C |
| C-016 bounded new-defect check | Reviews 2 and 3 both run the check over this round's hunks, on both old and new sides including deletion boundaries, with B's `depends_on` exception; no row-count cap; a verifier that cannot cover every hunk answers `cannot-verify`, which escalates (C's completeness rule without its one-row quota). | A+B |
| C-017 reviser edits outside listed rows | Every non-whitespace changed line must lie in a span claimed by a listed blocking row; `answer` refuses otherwise and names the hunks; `begin` repeats the check so skipping `answer` admits nothing; both refusals print the exact `revert-unclaimed` command, which restores those hunks from the snapshot only if the live text still equals what the check saw, so any session can recover without manual work. | B+C |
| C-021 verifier answer per row | Result `resolved`, `open`, `regressed` or `cannot-verify`; an evidence quote or snapshot range present in the new snapshot; `sentence_sound=no` requires a child row (B's T7); a disputed claim requires an explicit `dispute=accepted|rejected` ruling. | B+C |
| C-022 re-checking verified rows | The script resets `verified -> fixed` when a hunk overlaps the row's span or a supporting passage the verifier recorded at verification time; otherwise `regressed` on a verified row is refused (`E-NOT-CHANGED`), and only the fresh sweep may challenge it, which counts in the delivery outcome. | A+B |
| C-025 crash, idempotency, concurrency | Write to a temp file, fsync it, `os.replace`; hold a nonblocking `fcntl.flock` per call; every mutation carries `--op` and the expected sequence, and a repeated op with the same request digest returns the original result; no hard-link publish, directory-sync contract or filesystem refusal in version 1. | B+C |
| C-027 script CLI and exit codes | A's lean subcommands plus `revert-unclaimed` and `verdict`; JSON on stdout; exit 0 for any committed operation whatever the decision, nonzero only for usage, input or state refusals; `verdict` alone maps PASS, CONTINUE, ESCALATE to distinct exit codes for shell callers (C's rule, which also answers B's concern). | A+C |
| C-029 report writing and verdict line | The reviewer writes the panel report without its own status table or `verdict:` line; `close` refuses a report that has one, then appends the script-rendered row table, the Reviser brief (CONTINUE only) and the verdict line; the next `begin` refuses an edited tail. | A+B |
| C-031 reflect adoption | Future work only: a `reflect` profile, multi-file `--doc` and a caller-owned loop (B), rows sealed after the evidence-validator gate and merged ids, and "ledger PASS cannot authorize promotion" (C); blocking classes stay UNVERIFIED until the reflect grading text is read. | B+C |
| C-032 rf-qa adoption | Future work only: an `rf-qa` profile whose ordered guards are regression, then monotonicity, then cap, with the existing byte-exact halt messages (`rf-qa.md:401,407`), and a file lock before parallel instances share a ledger (B). | B+C |
| C-033 implement final review | Do not adopt in this change; if ever adopted, a ledger may only record per-task re-review rows and every archive attempt still needs a fresh full FINAL (C). | B+C |
| C-034 stateful session vs file ledger | File ledger is authoritative with fresh sessions; any resumed or cached session output must carry the current packet digest or be refused (C); a stateful-session arm is an open question, not part of this change. | C |
| C-040 validity checks and controls | Three checks, each catching a different failure: V1-ledger compliance (a replicate whose reviewers never ran the script is not treatment, as `DEC:64` already does for Arm B), B's baseline sweeps with hidden-defect share H, and C's recorded command, skill and script hashes plus live document versus snapshot mismatch. | A+B |
| C-043 cap enforcement | `CAP_REVIEWS = 3` tied to the cap text by a test; refuse a fourth review, a third fix cycle, a second sweep and a second `find` on an existing ledger even under a new op id; `close` never returns CONTINUE at review 3. | A+C |
| S-008 CLI spec form | One subcommand table (role, inputs, writes, output, checks, exit) followed by a separate transaction and rerun subsection. | A+C |
| S-009 test plan placement | A's named test cases in the spec, C's fixtures folder in the file table, and B's text pins and drift test in one "Tests" subsection. | A+C |
| S-012 rule classification placement | One MECHANICAL/PROSE table at the end with a residual-risk column (B); no inline labels elsewhere. | B |
| X-005 unclaimed reviser edits | As C-017: hard admission at `answer` and `begin`, with `revert-unclaimed` (preimage-checked) as the scripted recovery. | B+C |
| X-006 who calls the script | Each session runs its own subcommand and the actor is inferred from the subcommand (no `--as`); all model facts arrive as JSON input files the script validates, bound to round, document hash and ledger sequence (C's packet binding); the coordinator only dispatches and runs `status` before each dispatch to stop after a final decision (A-008). | A |
| X-011 deferred MAJOR rows in R3 | Headline counts every CRITICAL or MAJOR row by grade that is not `verified` after review 3, deferred ones included, plus deduplicated sweep CRITICAL or MAJOR rows; publish the blocking-only count and the deferred share beside it; controls stay comparable because the Arm B proxy also counted by grade (`ARMB:37`). | C |
| X-017 intra-B disputed status | `disputed` is a claim flag, never a status; the verifier must rule on each disputed claim; an unruled dispute at the cap counts as an open blocker. | B |

#### Positions table

Rows marked "(changed)" differ from my Round 1 table.

| Point | Preferred | Reason |
|---|---|---|
| S-001 | A | Section titles name the real commands, easier to search later. |
| S-002 | B | Alias list plus UNVERIFIED marks make citations checkable. |
| S-003 | B | One step table shows who, reads, writes and calls at a glance. |
| S-004 | A | Explicit kernel, contract, adapter split is the reuse seam adopters need. |
| S-005 | A | Single state document with per-row history; simplest to read and maintain. |
| S-006 | A+B | (changed) B's numbered transitions with phase column, carrying A's named error codes. |
| S-007 | B | Worked example on real flg-r2 counts proves the formula. |
| S-008 | A+C | A's table plus C's separate transaction and rerun subsection. |
| S-009 | A+C | A's named test cases plus C's fixtures folder, with B's drift test. |
| S-010 | B | Per-replicate traces and arithmetic make the forecast auditable. |
| S-011 | B | Evidence column and REMOVED/LEFT verdict are more honest. |
| S-012 | B | (changed) One end table with residual risk per rule; same as A's place, better content. |
| S-013 | A+B | One design doc suffices for an experimental variant; user guide premature. |
| S-014 | B | Explicit UNVERIFIED list is the most useful closing item. |
| S-015 | B | Dense tables carry more per line than one-sentence lines. |
| C-001 | A | One pretty-printed state object with history, plus C's op id and sequence as header fields. |
| C-002 | A | Path derivable from the document survives a lost flag; `E-EXISTS` stops a second run. |
| C-003 | A+C | A's per-review snapshots plus C's stored diffs with old and new ranges. |
| C-004 | A | Sessions call their own subcommand; actor inferred; C's packet binding added. |
| C-005 | B+C | (changed) B's transition table with phase column and retouch reset; C's history-derived reopen. |
| C-006 | B | Disputed answer needs an explicit verifier ruling. |
| C-007 | B | User-only demotion with quoted words, recorded after ESCALATE; no automatic path. |
| C-008 | A+C | (changed) A's key list plus C's frozen issue text. |
| C-009 | A | Profile computes blocking; reviewer cannot choose it. |
| C-010 | B+C | B's count without no-progress halt plus C's integrity and structural escalation. |
| C-011 | B | Count sweep blockers separately (Lt) instead of mixing into B. |
| C-012 | B+C | Outside the cap, fresh context (subagent if allowed, else a stated sixth dispatch). |
| C-013 | C | Separate loop decision and delivery outcome; no early final PASS. |
| C-014 | B | Data show no-progress halt never fires in S1; guard lives in the rf-qa profile only. |
| C-015 | B+C | (changed) Refusal on deferred rows, admission check on note-sponsored edits, `minor_touched` metric. |
| C-016 | A+B | Reviews 2 and 3, no count cap, `depends_on`, both diff sides, cannot-verify on incomplete cover. |
| C-017 | B+C | (changed) Hard admission at `answer` and `begin`, with preimage-checked `revert-unclaimed`. |
| C-018 | A+B | Normalized unique quote with minimum length, `--at` to disambiguate. |
| C-019 | C | Only relocation algorithm that handles unrelated edits and deletions. |
| C-020 | C | Raw plus normalized sets and kept old spans fix coordinate and deletion gaps. |
| C-021 | B+C | (changed) C's result set with cannot-verify; B's child row on a broken sentence and dispute ruling. |
| C-022 | A+B | (changed) B's script reset on retouch plus A's refusal to re-attack untouched rows. |
| C-023 | A+C | (changed) Script computes location attribution; analyst adjudicates causation for M3. |
| C-024 | A | Body hash plus report-tail check catches both edit paths. |
| C-025 | B+C | (changed) Atomic replace plus flock, op id and expected sequence; no hard-link layer. |
| C-026 | A+B | `sc-review-ledger` name, with B's reason (made precise by install_skills.py:57). |
| C-027 | A+C | A's lean subcommand set with C's JSON stdout and decision-coded `verdict` only. |
| C-028 | A+B | Copy plus parity test, but omit `## Unattended mode` as B does. |
| C-029 | A+B | (changed) Reviewer keeps panel prose without its own table or verdict; script appends tail. |
| C-030 | A | Review-1 PASS made no edits; a second full read of same text adds little. |
| C-031 | B+C | (changed) B's multi-file and caller-loop needs; C's rule that ledger PASS cannot promote. |
| C-032 | B+C | (changed) rf-qa.md:401,407 order must be kept; B's lock need; A's profile is the vehicle. |
| C-033 | B+C | (changed) Defer adoption; any later use keeps mandatory fresh full FINALs. |
| C-034 | C | (changed) File ledger authoritative; resumed output must carry the current packet digest. |
| C-035 | A+C | A's dup matching, C's count of deferred MAJOR rows by grade (ARMB:37). |
| C-036 | B | Forecast derived from traced rows; A's basis used the wrong row (ARMB:13). |
| C-037 | B | Growth derived arithmetically from measured minor-only byte shares. |
| C-038 | A+B | A's criteria plus B's baseline-sweep comparison and `minor_touched`. |
| C-039 | none | (changed) Sweep as a fresh subagent in review 3 if workers may spawn one, else a disclosed sixth dispatch. |
| C-040 | A+B | V1-ledger (as DEC:64 for Arm B) plus B's baseline sweeps; add C's hash recording. |
| C-041 | B | Cost grounded in real file timestamps and counts six sessions. |
| C-042 | A+B | Minimum anchor length plus a warning, not refusals that stall runs. |
| C-043 | A+C | (changed) A's constant tied to cap text; C's refusal of second sweep and repeated find. |
| X-001 | B+C | (changed) Sweep blocker forces delivery ESCALATE; C's split is the form. |
| X-002 | B+C | Fresh context avoids anchoring on just-verified rows. |
| X-003 | B | No second stop by default; guard kept for the rf-qa profile. |
| X-004 | A+B | Reviews 2 and 3 must record fix-induced rows like N12. |
| X-005 | B+C | (changed) Hard admission check with a scripted recovery path, so no stall. |
| X-006 | A | Each session calls its subcommand; S1 coordinator only dispatches and checks status. |
| X-007 | C | Exit 0 for committed operations; decision in JSON and in `verdict` only. |
| X-008 | A | Derivable default with override tolerates a lost flag. |
| X-009 | B | Verified: test_worker_contract.py:831-839 would fail on A's copy. |
| X-010 | B | (changed) Presence-only check (test_cli_install.py:501); no edit needed. |
| X-011 | C | (changed) Arm B proxy counted MAJOR by grade (ARMB:37), so deferred MAJOR rows count. |
| X-012 | B | Most grounded forecast; honest that the conservative bar may fail. |
| X-013 | A | No edits after a review-1 PASS, so the find pass is the sweep. |
| X-014 | A+C | Blocking computed by the script from severity, rule and outcome. |
| X-015 | B | Broken sentence must become a child row, not just a flag. |
| X-016 | A+C | (changed) A's `rule` field or C's criterion; both let FR-8/FR-9 be computed. |
| X-017 | B | (changed) B's repair: disputed is a claim flag with a mandatory verifier ruling. |
| X-018 | A+B | One-line brief change holds when sessions call the script; sweep dispatch disclosed if needed. |
| X-019 | A | Derivable default path, no random id. |
| X-020 | C | Old and new ranges per hunk fix A's coordinate mismatch. |
| X-021 | B+C | Only `fixed` rows (or ruled disputes) can become verified. |
| A-007 | none | Record review-1 grade distribution and filler-outcome share as covariates (F2R3:15 shows brief pressure). |
| A-008 | none | Coordinator runs `status` before each dispatch; growth from accepted snapshot; later edits flagged. |
| A-009 | C | C's relocation and `anchor_state` handle drifted anchors. |
| A-010 | C | Old-side ranges and deletion boundaries let deletion defects be anchored. |
| A-011 | none | Record supporting passages at verification and re-queue on change; sweep challenges cover the rest. |
| A-012 | none | Recompute forecasts from each replicate's measured review-1 blocking count (B1 x r x r). |


### Variant B Rebuttal

### Round 2 rebuttal: Variant B (variant-2-sonnet-analyzer.md, analyzer persona)

Advocate for Variant B (sonnet, analyzer: evidence quality, logical consistency; focus on root cause and evidence). Inputs read: my Round 1 statement, `round1-advocate-A.md`, `round1-advocate-C.md`, `round2-rebuttal-A.md`, `diff-analysis.md`, variant B, and the experiment files cited under New evidence (read-only). Labels: "A s2" means section 2 of variant A, "B-R1" my Round 1 statement, "A-R2" A's rebuttal. Paths: `W` = `/home/coder/workspaces/worktrees/IronClaude`; `F2` = `W/exp346-ab-flg-r2/.dev/orca-command-refactor`; `EXP` = `W/exp346-p1-logs/.dev/experiments/346-validation`; `F2R3` = `F2/review/spec-panel-round3.md`; `F2D1` = `F2/review/disposition.md`; `ARMB-REPORT.md` = `EXP/phase4/ARMB-REPORT.md`; `DES:162` = the 427 design line cited in B-R1.

#### Response to criticisms

Each item gives the criticism, then CONCEDE or COUNTER with the evidence. Where A and C made the same point I answer once.

##### From advocate A (Round 1 and A-R2)

**A1. "Grading is a reviewer choice, not a computed field"; the FR-8/FR-9 bullet has no field (A-R1 weakness 1; X-014, X-016).** CONCEDE. Variant B's `add` row carries `sev`, `grade`, `anchor`, `finding`, `wrong_outcome` and `init` takes only `--scale` and `--needs-outcome` (variant B, Script CLI table), so the script cannot compute "CRITICAL and FR-8/FR-9 are blocking". Repair, now my rule: drop `sev` from the reviewer's input; add `rule` beside `grade` and `wrong_outcome`; `blocking` is a script output of the named profile `spec-panel`. The predicate is the 427 text at `src/superclaude/commands/spec-panel.md:259`: "CRITICAL and FR-8/FR-9 findings are blocking; MINOR is minor; a MAJOR is blocking only if it names a concrete wrong outcome an implementer would produce, otherwise minor". Written as code: blocking if grade is CRITICAL, or rule is FR-8 or FR-9, or grade is MAJOR with a non-empty `wrong_outcome`; every other row is `deferred`. This also closes the gap I admitted in B-R1 (a MAJOR filed as `sev=minor` had no defined status): it is now `deferred`, and it stays in the headline by grade (X-011). Residual, stated plainly: `grade` is still the reviewer's judgement, so a CRITICAL filed as MINOR is still deferred. A's version has the same residual; it is PROSE and is covered by A-007, not by the script.

**A2. "The adoption seam is call-time flags" (A-R1 weakness 2).** CONCEDE the form, KEEP the reason for it. My flags (`--scale CRITICAL,MAJOR,MINOR --needs-outcome MAJOR`) were meant to keep spec-panel words out of the kernel. A's `PROFILES` table does that better and removes the typo risk. Accepted: `init --profile spec-panel`; the script resolves the profile, writes its name and a hash of its table entry into the ledger header, and refuses any later call that disagrees. Take also the A-R2 refinement (C5): a profile entry carries an ordered list of guards from a fixed menu (`regression`, `monotonicity`, `cap`) with halt messages. A new guard kind is a kernel change with its own tests.

**A3 / C4. "`disputed` as a status" (X-017).** CONCEDE, repair already stated in B-R1 and adopted by A-R2: `disputed` is a claim flag, never a status. T8 reads "From `open` or `reopened` with `claim.action=disputed`; To `verified` if the verifier rules `dispute=accepted`, else `reopened`; the note is required." An unruled dispute at the cap counts as an open blocker (A-R2's addition, accepted). C asked for dispute as evidence, not state; this is that.

**A4. "Large CLI surface; close exit codes 10/11 make CONTINUE look like a crash" (A-R1 weakness 4; A-R2 "one standing objection"; X-007).** CONCEDE on exit codes, with the root cause stated. I coupled the exit code to the decision because the 427 failure was a brief beating the command (`F2R3:15`: "Under the brief, any finding of any severity is FAIL"), and I wanted the machine, not a sentence, to say stop (variant B Precedence bullet: "the exit code of `close` outranks any sentence of a brief"). The flaw is in the carrier: an LLM reads a Bash result whose non-zero code is shown as an error, so CONTINUE (10) can invite a rerun of `close`, which my own table answers with exit 4. That effect is UNVERIFIED for the S1 workers but cheap to avoid, and the stop does not depend on it: the cap is a refusal in `open`, the report's last line is script output, and the JSON names the decision. New rule: every committed operation exits 0; refusals keep my distinct non-zero codes (4 already closed, 6 unmarked `fixed` rows, 7 unclaimed hunks); a read-only `verdict` subcommand maps PASS, CONTINUE, ESCALATE to 0, 10, 11 for shell callers. On surface size: fold `render` and `show` into `status` and `open`, drop `--as` (my own table classes identity as PROSE, so the flag proved nothing; the phase gate is the mechanical part and the actor follows from the subcommand). About nine subcommands remain.

**A5. "A missing flag stops the loop" (A-R1 weakness 5; X-008, X-019).** CONCEDE. Variant B's Mode bullet ("`--ledger <path>` required; without `--ledger` stop and say so") moves 427's lost-saved-copy failure (`DES:162`) into the coordinator's memory. Adopt A's derivable default path plus `init` refusing an existing ledger (`E-EXISTS`), with `--ledger` as an override. One tension to record, not hide: a derivable path means the fresh sweep reviewer could find the ledger by convention. The sweep prompt must not name the path, and "do not read the ledger" stays PROSE in the rule table; H (hidden-defect share) is how we notice a breach.

**A6. "No concurrency protection while rf-qa is the second adopter" (A-R1 weakness 6; C1).** CONCEDE. I wrote "two parallel QA instances on one ledger lose updates" (variant B section 7) and deferred the lock, which means shipping a known lost-update window in the kernel. Accept `fcntl.flock` per call, `--op` and an expected sequence in the header, idempotent replay of the same op (resolution of C-025 below). I still reject C's hard-link publish, directory sync and filesystem refusal for version 1.

**A7. "The sweep's independence rests on prose" (A-R1 weakness 7).** PARTLY CONCEDE. Freshness is mechanical: a new session, or a subagent, has no memory of the rows the review-3 session verified. Only "does not read L" is PROSE, and the rule table says so with its residual risk. The record that shows a breach is mechanical too: V1-ledger checks whether the sweep report cites ledger row ids.

**A8. "The forecast mixes a starting point the ledger does not share; P3s 5.5 is likely pessimistic" (A-R1 weakness 8).** PARTLY CONCEDE. The ledger changes review 1 (one find pass, anchored JSON rows), so B1 can move. But the counter-forecast was built on the wrong row: A-R2 B7 now verifies that `ARMB-REPORT.md:13` gives the review-1 proxy as 16 and 17 and the review-2 proxy as 5 and 6, and `F2D1:39` says "all 13 blocking". So the only argued direction is mine, with a formula that exposes its input (expected review-3 blockers about B1 x r x r; B1 = 13, ratios 0.46 then 0.17 give 1.0). Merged rule: pre-register the formula, recompute from each replicate's measured review-1 blocking count, and report both P3 and P3s. Neither 2.5 nor 5.5 is a prediction; the formula is.

**A-R2 proposals addressed to B's design.** Accepted: A-R2 on C-017 (hard admission at `answer` and `begin`, scripted recovery), on C-021, C-022, C-025 and X-017 (details below). One caveat on A-R2's C-029: "`close` refuses a report that has its own status table or `verdict:` line". Refusal is right, but the message must name the offending lines and the exact fix, because a panel reviewer's habit under 427 is to end with `verdict:` itself; a silent strip would edit model text and a bare refusal stalls the run.

##### From advocate C (Round 1)

**C1. "Atomic replacement does not prevent lost updates" (C-R1 weakness 1).** CONCEDE, same as A6.

**C2. "The blocking contract has a missing input" (C-R1 weakness 2; X-016).** CONCEDE, same as A1.

**C3. "Its scope gate remains optional in effect; `revert-unclaimed` without a preimage check is not a substitute" (C-R1 weakness 3; X-005).** CONCEDE. Variant B's open question 2 chose a soft gate ("`open` only records them ... Making `open` refuse is stricter but can deadlock an unattended run") for the stall reason. The stall is removable: refuse hard, and make every refusal print its own recovery. Merged rule: `answer` and `begin` both run the admission check; each refusal lists the hunks and the exact `revert-unclaimed --hunk <id> --expect <hash>` command; the revert restores from `L.snap/r<n>.md` only if the live text still hashes to what the check saw, otherwise it refuses and lists the difference. That is C's strictness, A's both-ends check, and my escape together. Honest limit: a legitimate edit outside every listed row (A's open question 4, filling an FR-8/FR-9 gap) is reverted too; the reviser records the gap in its disposition note and the sweep or next verify pass must find it. I accept that cost, because the F22 chain (below) is exactly the case where an unlisted-but-reasonable edit became the next blocker.

**C4. "Dispute representation inconsistent" (C-R1 weakness 4; X-017).** CONCEDE, same as A3.

**C5. "P3s needs an identity-based deduplication rule" (C-R1 weakness 5).** CONCEDE. Variant B defines P3s as "P3 plus the sweep's rows of grade CRITICAL or MAJOR" (variant B section 9) with no union rule. Merged rule: a sweep row whose normalized anchor quote equals, or whose span overlaps, an existing row is stored as `dup_of=<id>` and counted once; a sweep row that attacks a `verified` row is stored as a `challenge` and counts in the delivery outcome; the report prints raw and deduplicated counts side by side. A and C are right that publishing only one of the two would either inflate failure or hide it.

**C6. C's table positions against B.**
- *C-030 "even a review-1 PASS requires a terminal sweep".* COUNTER. A review-1 PASS means no reviser ran, so the document is the same bytes review 1 already read as a whole-document pass. A sweep would be a second sample of the same reviewer model on identical text. That measures recall (which B's baseline sweeps on the six existing finals already do, variant B section 9), not whether a fix introduced a defect. Keep A's rule; record "no sweep: review-1 PASS" in the report.
- *C-007 "no waiver API; quoted authority cannot be authenticated".* PARTLY CONCEDE. I keep the user-quoted demotion (T10), because a false first-pass blocker otherwise forces FAIL forever (C's own design has no exit, C section 3). I add: T10 never changes the recorded verdict; it sets `demoted=true` with the quoted words, the delivery outcome stays ESCALATE, and the report lists demoted rows by id. That removes the authentication objection, since nothing depends on the quote being true.
- *C-029 "script writes the whole report".* COUNTER. A and C-R1's own concession 4 agree the panel's prose has value; the conflict C wants to avoid (model status table next to computed tail) is solved by the refusal in A-R2, which keeps the reviewer's expert text.
- *S-012 inline labels.* COUNTER, low stakes. One end table with a residual-risk column lets a reader audit all classifications at once; inline labels scatter them (diff-analysis S-012).
- *A-007 "measure blinded review-1 grading disagreement".* ACCEPT as an optional covariate: an analyst blind to arm judges whether each review-1 `wrong_outcome` is filler. It costs one pass over about 13 rows per replicate.

**C7. "The sweep is an extra assessment; do not claim three" (C-R1 concession 6, section 4).** AGREE and adopt the wording. The sweep stays outside the three-review cap and is disclosed as a fourth assessment: "three remediation reviews plus one terminal sweep". The owner decides whether "3 reviews" in the goal means that or three assessments in total; until then P3 (without sweep) and P3s (with it) are both reported, which is how variant B was already built.

**Settled by others' concessions.** A-R2 items B1 to B9 (sweep session, sweep authority, early stop, `open -> verified`, coordinates, unclaimed edits, forecast row, `## Unattended mode`, `test_cli_install.py`) and C-R1 concessions 1 to 7 settle the disputes over A's and C's own text. I do not re-argue them.

##### Resolution of X-016 and X-017

- **X-016** (blocking FR-8/FR-9 with no field): fixed as in A1. The reviewer supplies `grade`, `rule`, `wrong_outcome`; the script computes `blocking` and freezes it. Test: a row with `rule=FR-8` and `grade=MINOR` is `blocking` and not `deferred`.
- **X-017** (`disputed` as status): fixed as in A3. Five statuses only: `open`, `deferred`, `fixed`, `verified`, `reopened`. A dispute is `claim.action=disputed` on an `open` or `reopened` row, and the verifier's ruling is mandatory.

#### Updated assessment

**Variant A.** A is the right frame and the wrong loop. Its frame is what I now adopt: kernel, contract and adapter with a `PROFILES` table; one state object with per-row history; `blocking` computed from the profile; actor inferred from the subcommand; a ledger path derivable from the document; the report-tail check (`E-REPORT-EDITED`); `E-NOT-CHANGED`; the script-written `plan-r<k>.md`; and the V1-ledger compliance check. A-R2 then conceded the loop rules I attacked (fresh sweep session, sweep blockers changing delivery, no early stop at review 2, `open -> verified`, coordinates, unclaimed edits, the wrong forecast row, the `## Unattended mode` copy, the `test_cli_install.py` edit). What is left of A is its architecture, and I rate that higher than in Round 1. A's remaining weaknesses: its extension claim needed narrowing (A-R2 C5 does that), and its "sweep as a fresh subagent" route is a proposal that is UNVERIFIED for S1 and has a heartbeat cost (see New evidence 1).

**Variant C.** After its Round 1 concessions (X-018, X-019, the unsupported 1.5 forecast, the one-row discovery budget), C's value is a set of additive parts, and I take most of them: `loop_decision` versus `delivery_outcome`, `cannot-verify`, anchor relocation with `anchor_state=missing|ambiguous`, old and new ranges with deletion boundaries, packet binding to round, document hash and ledger sequence, `--op` with expected sequence, and the integrity term. I still reject four things: coordinator-only mutation (C-R1 concession 1 admits it cannot run under the one-line brief rule), event replay as the only store (a second reducer every reader must trust; A's per-row `history` gives the same audit trail), the hard-link and directory-sync publication layer (C-R1 concession 7 itself asks for measured cost first), and the script writing the whole report. I also reject C's dependency-passage tracking for verified rows in version 1: in the one replicate where both verify rounds are on file, zero of 19 verified rows regressed (New evidence 2).

**Variant B (myself).** I concede more than in Round 1: `sev` and `--as` go; exit codes move off `close`; the ledger path becomes derivable; locking and operation ids come in; unclaimed edits are refused with a scripted recovery; `disputed` is a flag; P3s gets a union rule. What I keep is what only B supplies: the traced root cause (F22 applied under "apply confirmed findings", then N5, then N12), the B1 x r x r bound and its honest "escalate with 0 to 3 rows" ceiling, the baseline sweeps and hidden-defect share H as the only measure of whether the ledger stopped looking, the install and test traps (`sc-spec-panel-ledger` skipped by `install_skills.py`; `## Unattended mode` set equality), and the end table of rules with residual risk. The merged spec should be A's frame, B's measurement and loop rules for scope, C's outcome vocabulary and integrity rules.

#### New evidence

Paths: `F2R2` = `F2/review/spec-panel-round2.md`; `F2R3` = `F2/review/spec-panel-round3.md`; `F2D1` = `F2/review/disposition.md`; `ARMB` = `EXP/phase4/ARMB-REPORT.md`; `DEC` = `EXP/DECISIONS.md`; `DES` = the 427 design note cited in B-R1. Repo paths are under `W/bs346-ledger/`. I read experiment files only, in pieces of 80 lines or fewer.

**1. Can an S1 worker spawn a subagent (A-R2's open question; C-039, X-002)? Verdict: UNVERIFIED for S1; documented as possible; nothing observed either way.**

What I found:
- *The S1 briefs say nothing either way.* The verbatim worker briefs `EXP/phase2/S1/briefs/T05-...md` to `T17-...md` hold the Orca wrapper (lines 1 to 83 in T09; the `=== TASK ===` marker is line 84) and the coordinator text (line 85). I grepped all of T01 to T17 (briefs and `task-text/`) for `subagent|sub-agent|Agent tool|Task tool`, without any filter. The only hits are one line each in the three setup tasks T01 to T03 (line 85, their inventory targets); T04 to T17, including every review and revise brief T05 to T10, have zero. T09's task text asks the worker to "run /sc:spec-panel ... for new defects" directly (`T09-R3-reviewer-L11-1c9a7ec8.md:85`); it neither allows nor forbids a subagent.
- *No S1 report shows a spawn or a failed spawn.* The same grep over `EXP/phase3/coordinator-log.md`, `phase4/coordinator-log.md`, `phase5/coordinator-log.md`, `phase4/AB-REPORT.md`, `phase4/ARMB-REPORT.md`, `phase2/S1/ANALYSIS.md`, `phase2/S1/REPLAY.md` and `DEC` returned no lines. So there is no observation of an S1 worker using the Agent tool.
- *The documents say it is possible and that Orca does not fence it.* `F2/inventory/commands-a.md:13`: "An Orca worker is itself a top-level Claude session ... launches a normal Claude process"; `commands-a.md:14` quotes the Claude Code docs, "By default, a subagent can spawn subagents of its own, up to three layers below the main conversation". `F2/inventory/orca-capabilities.md:155`: "Agent-tool subagents are not Orca workers, so the depth limit does not count them", resting on the fence being about "Sub-worker dispatch" (`nested-worker-depth.js:7-11`), but the same line says it is UNVERIFIED that Orca never limits them. `F2/specs/orca-worker-contract-spec.md:25` (E4) states the same and `:46` says "Agent-tool fan-out inside a worker has no proven limit, but no proof of none either".
- *The nearest prior run is not proof.* `orca-capabilities.md:156` records that the PR #329 run told workers to "spawn an agent (Agent tool)", and says "UNVERIFIED in this report whether every such spawn succeeded; the worker transcripts were not read" (also `orca-worker-contract-spec.md:44`).
- *Main sessions in this setup spawn subagents, but they are not Orca-dispatched workers.* `EXP/phase1/REPORT.md:243` (34 reviewer subagent logs in one `/sc:implement` session) and `:298` (a specs coordinator with 156 subagents).

Conclusion and cheapest settlement: treat the subagent sweep as plausible and unproven. Before replicate 1, run one throwaway dispatched worker with the T09 wrapper, have it spawn one subagent that reads a file and prints its hash, and record yes or no. If no, the sweep is a sixth dispatch, disclosed as a deviation (variant B section 9). The ledger design does not depend on the answer: `open --sweep` and `add` work the same from a session or a subagent, because the actor follows from the subcommand.

A cost of the subagent route that neither A-R2 nor B-R1 counted: heartbeats. The wrapper requires "Send a heartbeat every 5 minutes" (`T09-R3-reviewer-L11-1c9a7ec8.md:31`). A whole-document sweep inside one Agent call can run longer than that: the flg-r2 panel itself raised it as F14, "The heartbeat rule cannot hold for long Agent-tool calls" (`F2/review/spec-panel.md:112`), and the S1 baseline lists whether a late heartbeat harms Orca's liveness verdict as UNVERIFIED (`EXP/phase2/S1/baseline-outputs/disposition.md:69`). A sixth dispatch has its own heartbeats and avoids this. So the subagent route is better only if the smoke check passes and the sweep is bounded or preceded by a heartbeat.

**2. Zero of 19 verified rows regressed in flg-r2; both late defects arrived as new rows (C-022, A-011, X-004).** `F2R2:50`: "13 prior blocking findings: 13 resolved, 0 open, 0 regressed (the F10 fix creates new blocking finding N1)". `F2R3:47`: "6 prior blocking findings (N1-N6): 6 resolved, 0 open, 0 regressed ... The N5 fix introduces new blocking finding N12". So in this replicate the accepted-fix-broken-by-edit-elsewhere case (A-011) has no observed instance, and both fix-induced defects (N1 from the F10 fix, N12 from the N5 fix) were new rows anchored in changed text. That supports: (a) verify rounds 2 and 3 must both be able to file new rows over this round's hunks (C-016, X-004), which also refutes C's one-row budget a second time (two fix-induced rows in two rounds); (b) B's script reset on retouch and A's `E-NOT-CHANGED` suffice for version 1; (c) C's supporting-context tracking and A-R2's "record supporting passages" are not needed in version 1, and a lexical cross-check (a hunk containing an identifier such as AC-0.4 that a verified row's claim names) should be a warning line in the plan, not a status change. Limit: one replicate (the other five I did not re-open in this round); with the tracing in B-R1 (ctl-r1) the pattern is the same, but that is two documents and one reviewer model.

**3. rf-qa's monotonicity rule counts differently from the one A proposed for spec-panel (C-014, C-032).** `src/superclaude/agents/rf-qa.md:401`: "Each cycle MUST have strictly fewer blocking issues than the previous one (`|F_{n+1}| < |F_n|` when `|F_n| > 0` ...; new minor findings are notes and do not count)", and `:407`: "Regression detection (runs FIRST per cycle transition)." I confirm A-R2's reading independently. Consequence: rf-qa's guard counts open blocking findings per cycle, fix-induced ones included, which is the same count A's proposed spec-panel stop (`B(2) >= B(1)`) used. rf-qa has that rule in its own text, so it belongs in the rf-qa profile and stays off by default for spec-panel, where flg-r2 blocking fell 13, 6, 1 (13 from `F2D1:39`; the 6 and the 1 as cited in B-R1 from `F2R2` and `F2R3`, and `F2R3:47` names the one new row, N12).

**4. The compliance rule already exists for Arm B (C-040).** `DEC:64` carries the rule that a report that ignores the flags is recorded as "flags not honoured" and does not count as treatment (long line; A-R2 cites it, I checked the line holds the text). V1-ledger is the same rule applied to the ledger arm, so I withdraw my preference for baseline sweeps alone: the two checks catch different failures (compliance versus hiding), and both stay.

**5. The grading predicate is a quoted text, not a paraphrase.** `src/superclaude/commands/spec-panel.md:259` (quoted under A1) is the source for the profile; `:256-264` also states that "The coordinator keeps the review count, the prior-findings file and the saved copy; without them the run is a first review", which is the failure the derivable ledger path removes.

#### Proposed resolution of split points

Column "A-R2" says where I take A's Round 2 proposal (ACCEPT), change it (MODIFY) or replace it (DIFFER). Where I MODIFY, the change is stated in the rule.

| Point | Merged rule | A-R2 |
|---|---|---|
| C-005 status set and who may change it | Five statuses (`open`, `deferred`, `fixed`, `verified`, `reopened`); numbered transitions with a phase column and A's error codes; the script sets `deferred` from the profile and resets `verified -> fixed` when a hunk overlaps the row's claim; `open` versus `reopened` comes from history (C); the reviser requests only `fixed`, the verifier moves only `fixed` (or a ruled dispute) to `verified`, else `reopened`; `disputed` is a claim flag. | ACCEPT |
| C-008 frozen fields | Freeze `id`, `label`, `round_found`, `origin`, `caused_by`, `grade`, `rule`, `wrong_outcome`, `blocking`, `anchor`, `at` and the original finding text; any later input carrying one is refused (`E-FROZEN`). | ACCEPT (I add `grade` and `rule`, needed because `sev` is gone) |
| C-016 bounded new-defect check | Reviews 2 and 3 both check this round's hunks on both old and new sides, including deletion boundaries, with B's `depends_on` exception; no row-count cap; a verifier that cannot cover every hunk answers `cannot-verify` and the loop escalates; oversize hunks only warn (`HUNKS_LARGE`). Evidence: both fix-induced defects in flg-r2 (N1 at review 2, N12 at review 3) were new rows (`F2R2:50`, `F2R3:47`). | ACCEPT |
| C-017 reviser edits outside listed rows | `answer` and `begin` both refuse any non-whitespace changed line outside a span claimed by a listed blocking row; each refusal prints the exact `revert-unclaimed --hunk <id> --expect <hash>` command; the revert restores from the snapshot only if the live text still matches what the check saw. The gap the reviser could not edit goes in its disposition note for the next verify pass or the sweep. | ACCEPT (I add the preimage hash, from C's objection) |
| C-021 verifier answer per row | Result `resolved`, `open`, `regressed` or `cannot-verify`; evidence is a quote or snapshot range present in the new snapshot; `touched_ok=no` requires a child row; a disputed claim needs `dispute=accepted` or `rejected`; an unruled dispute at the cap counts as open. | ACCEPT |
| C-022 re-checking verified rows | The script resets `verified -> fixed` when a hunk overlaps the row's claim; `regressed` on an untouched verified row is refused (`E-NOT-CHANGED`); only the fresh sweep may challenge such a row and that counts in the delivery outcome; a lexical cross-check (identifier named in a verified claim appears in a hunk) is a warning line in the plan, not a status change. No supporting-passage tracking in version 1: 0 of 19 verified rows regressed in flg-r2. | MODIFY (A-R2 records supporting passages and re-queues on change; I keep it out of version 1) |
| C-025 crash, idempotency, concurrency | Temp file, fsync of that file, `os.replace`; nonblocking `fcntl.flock` per call; `--op` and expected sequence in the header; a repeated op with the same request digest returns the first result; `init` refuses an existing ledger. No hard-link publish, directory sync or filesystem refusal in version 1. | ACCEPT |
| C-027 script CLI and exit codes | About nine subcommands, JSON on stdout; every committed operation exits 0 whatever the decision; refusals use distinct non-zero codes (4 closed, 6 unmarked `fixed`, 7 unclaimed, plus usage and input errors); only `verdict` maps PASS, CONTINUE, ESCALATE to 0, 10, 11. | ACCEPT (I give up `close` exit 10/11) |
| C-029 report writing and verdict line | Reviewer keeps the panel prose and must not write its own status table or `verdict:` line; `close` refuses a report that does, naming the lines and the fix, then appends the rendered table, the Reviser brief (CONTINUE only), the ledger verdict line and the final `verdict:` line; the next `begin` refuses an edited tail. | ACCEPT (I add the named-fix message) |
| C-031 reflect adoption | Future work, not in this change: a `reflect` profile, multi-file `--doc` and a caller-owned loop, rows sealed after the evidence-validator gate and merged ids, and "ledger PASS cannot authorize promotion"; blocking classes stay UNVERIFIED until the reflect grading text is read. | ACCEPT |
| C-032 rf-qa adoption | Future work: an `rf-qa` profile with ordered guards regression, monotonicity, cap and the existing halt messages (`rf-qa.md:401,407`, verified), and a file lock for parallel instances (now in the kernel via C-025). | ACCEPT |
| C-033 implement final review | Not adopted in this change. If ever adopted, the ledger may hold per-task re-review rows only; every archive attempt still needs a fresh full FINAL. | ACCEPT |
| C-034 stateful session vs file ledger | File ledger is authoritative with fresh sessions; resumed or cached output must carry the current packet digest or be refused; a stateful-session arm is an open experiment outside this change. | MODIFY (A-R2 says C; I keep B's note that the stateful arm is a cheap fallback to test later) |
| C-040 validity checks and controls | Three checks: V1-ledger compliance (the same rule `DEC:64` applies to Arm B), baseline sweeps on the six existing finals with hidden-defect share H, and recorded command, skill and script hashes with live-document-versus-snapshot mismatch. | ACCEPT |
| C-043 cap enforcement mechanics | `CAP_REVIEWS = 3` with a test tying the constant to the cap text; the script refuses a fourth review, a third fix cycle, a second sweep and a second `init` even under a new op id; `begin` and `verdict` never return CONTINUE at review 3. | ACCEPT |
| S-008 CLI spec form | One subcommand table (role, inputs, writes, output, checks, exit) followed by a separate "Transaction, crash and rerun" subsection. | ACCEPT |
| S-009 test plan placement | One "Tests" subsection: A's named cases, C's fixtures folder in the file table, B's text pins and the drift test (variant equals `spec-panel.md` outside the replaced sections, excluding `## Unattended mode`). | ACCEPT |
| S-012 rule classification placement | One MECHANICAL/PROSE table at the end with a residual-risk column; no inline labels. | ACCEPT |
| X-005 unclaimed reviser edits | Same as C-017. | ACCEPT |
| X-006 who calls the script | Each session runs its own subcommand and the actor follows from the subcommand (no `--as`); model facts arrive as JSON input files bound to round, document hash and ledger sequence; the coordinator dispatches and runs `status` before each dispatch so nothing launches after a final decision. | ACCEPT |
| X-011 deferred MAJOR rows in the R3 count | Headline counts every CRITICAL or MAJOR row by grade that is not `verified` after review 3, deferred rows included, plus deduplicated sweep rows and sweep challenges; print the blocking-only count, the deferred share and raw-versus-deduplicated sweep counts beside it. Basis: the Arm B proxy also counted MAJOR by grade (`ARMB-REPORT.md:37`, as A-R2 cites). | ACCEPT |
| X-017 `disputed` as a status | `disputed` is a claim flag, never a status; the verifier must rule; an unruled dispute at the cap counts as an open blocker. | ACCEPT |

Where I do not move: C-030/X-013 (no sweep after a review-1 PASS), C-007 (user-quoted demotion kept, but it cannot change the recorded verdict), C-039 (sweep as fresh subagent only if the smoke check in New evidence 1 passes, else a disclosed sixth dispatch).

#### Positions table

Rows marked "(changed)" differ from my Round 1 table; all others are copied unchanged.

| Point | Preferred | Reason |
|---|---|---|
| S-001 | B | Outlines are identical; keep B's citation aliases for audit. |
| S-002 | B | Alias list with UNVERIFIED marks lets a reviewer recheck every claim. |
| S-003 | B | Step table shows who, reads, writes and calls at a glance. |
| S-004 | A | Kernel, contract, adapter table gives the clearest extension seam. |
| S-005 | A | One state document with per-row history is simplest to test; replay adds little. |
| S-006 | A+B | (changed) B's numbered transitions with phase column, carrying A's named error codes. |
| S-007 | B | Decision table plus worked example on real flg-r2 counts. |
| S-008 | A+C | (changed) Subcommand table plus C's separate transaction and rerun subsection; B's exit-code list no longer fits once `close` exits 0. |
| S-009 | A+C | (changed) A's named cases and C's fixtures folder; B's text pins and drift test stay inside it. |
| S-010 | B | Predictions tied to traced rows can be checked and falsified. |
| S-011 | B | Evidence and verdict columns separate removed causes from left ones. |
| S-012 | B | End table with residual risk per rule; inline labels scatter it. |
| S-013 | A+B | One design doc suffices; user guide and schema file are speculative. |
| S-014 | B | Final UNVERIFIED list tells implementers what to check first. |
| S-015 | B | Dense tables with citations review fastest. |
| C-001 | A | Single JSON object with per-row history; add C's op id and sequence as header fields. |
| C-002 | A | Path derivable from the document; a lost flag cannot restart a first review. |
| C-003 | A+C | A's snapshot timing; C's candidate hash catches out-of-band edits. |
| C-004 | A | Role follows from the subcommand; B's --as flag proves nothing. |
| C-005 | B+C | (changed) B's transition table with phase column and retouch reset; C's history-derived reopen. |
| C-006 | B | Verifier must rule on a dispute; A and C give no explicit ruling. |
| C-007 | B | User-quoted demotion keeps a wrong blocker from freezing the loop; it cannot change the recorded verdict. |
| C-008 | A+C | A's wide key list plus C's frozen issue text. |
| C-009 | A+C | Script computes blocking from a profile; reviewer-supplied sev is a hole. |
| C-010 | B+C | B's unmarked-row refusal and sweep term; C's integrity and pending states. |
| C-011 | B | Separate U and Lt counters show loop and sweep outcome apart. |
| C-012 | B+C | Fresh session outside the cap keeps the sweep unanchored; label it sweep. |
| C-013 | C | (changed) C's loop_decision and delivery_outcome split is the clean form; B's U and Lt counters feed it. |
| C-014 | B | Monotonic stop optional, default off; flg-r2 blocking fell 13, 6, 1. Guard lives in the rf-qa profile. |
| C-015 | B+C | (changed) B's auto-defer plus minor_touched metric; C's admission refusal covers edits over deferred spans. |
| C-016 | A+B | (changed) Reviews 2 and 3, no count cap, depends_on, both diff sides; both fix-induced defects in flg-r2 were new rows. |
| C-017 | B+C | C's admission check at answer and begin, with B's revert-unclaimed (preimage-checked) as recovery. |
| C-018 | A+B | A's whitespace normalization and 12-character floor; B's --at for repeats. |
| C-019 | C | Only C handles missing, ambiguous and deleted anchors explicitly. |
| C-020 | B+C | C's raw old and new ranges cover deletions; B's HUNKS_LARGE warning. |
| C-021 | B+C | B's touched_ok forcing a child row and dispute ruling; C's cannot-verify result. |
| C-022 | A+B | B's reset to fixed on retouch; A's refusal to re-attack untouched rows; 0 of 19 verified rows regressed in flg-r2. |
| C-023 | A+C | (changed) Script computes location attribution; the analyst adjudicates causation for M3, since hunk overlap proves location not cause. |
| C-024 | A | Body hash plus report-edit check; add B's reseal command. |
| C-025 | B+C | Atomic replace plus flock, op id and expected sequence; skip hard-link and directory-sync machinery. |
| C-026 | B | Same layout, plus install-trap warning and reason to reject a CLI subcommand. |
| C-027 | A+C | (changed) Lean subcommand set, JSON stdout, `verdict` alone carries decision exit codes; B's distinct refusal codes kept. |
| C-028 | B | Copy with drift test; omit Unattended mode to keep its test green. |
| C-029 | A+B | Reviewer keeps panel prose; script appends verdict, footer and brief; `close` refuses a report with its own verdict line and names the fix. |
| C-030 | A | Review 1 is already a full pass; a sweep after PASS reads identical bytes. |
| C-031 | B+C | B's multi-file and caller-loop needs; C's rule that ledger PASS cannot promote. Future work. |
| C-032 | B+C | B's step mapping and lock need; C's rule to keep rf-qa's regression, monotonicity, cap order (rf-qa.md:401,407). Future work. |
| C-033 | B+C | (changed) Do not adopt now; any later use keeps mandatory fresh full FINALs. |
| C-034 | B+C | (changed) File ledger authoritative; resumed output must carry the current packet digest; stateful session stays a later experiment. |
| C-035 | A+C | A's dup matching; C's sweep challenges; report ledger-only and sweep parts apart like B. |
| C-036 | B | Forecast built from traced rows; admits the bar is probably unmet; recompute from measured review-1 blocking. |
| C-037 | B | Growth derived from measured minor-only byte shares, stated as upper bound. |
| C-038 | A+B | B's baseline-sweep and minor_touched failures; A's ledger-honoured check. |
| C-039 | none | Fresh subagent in review 3 only if a smoke check shows S1 workers can spawn one (UNVERIFIED now); else a disclosed sixth dispatch. |
| C-040 | A+B | (changed) A's V1-ledger compliance (same rule as DEC:64) plus B's baseline sweeps with H; add C's hash recording. |
| C-041 | B | Calls, sessions and minutes estimated from file times, not guessed. |
| C-042 | A+B | A's 12-character anchor floor; B's warn-only HUNKS_LARGE; no hard limits. |
| C-043 | A+C | (changed) A's constant tied to the cap text; C's refusal of a second sweep and a repeated init under a new op id. |
| X-001 | B+C | A late blocker must block a clean final outcome, or PASS is hollow. |
| X-002 | B+C | Fresh context; a same-session sweep is anchored on rows it just read. |
| X-003 | B+C | No second stop for spec-panel; flg-r2 blocking fell 13, 6, 1 so it never fires. |
| X-004 | A+B | Both allow reviews 2 and 3; N1 arose at review 2 and N12 at review 3. |
| X-005 | B+C | Hard check at admission, with revert-unclaimed as the escape from stalls. |
| X-006 | A | (changed) Each session runs its own call and the actor follows from the subcommand; C's coordinator-only claim is false. |
| X-007 | C | (changed) Committed operations exit 0; decision in JSON and in `verdict` only; a non-zero CONTINUE can look like a crash. |
| X-008 | A | Derivable default path; B's mandatory flag is a self-inflicted stall. |
| X-009 | B | Verified: the test needs Unattended-mode set equality; A's byte copy would fail it. |
| X-010 | B | Check is presence-only, so no edit is needed. |
| X-011 | C | The control counted by grade (ARMB-REPORT.md:37), so deferred MAJOR rows count. |
| X-012 | B | An honest forecast that the conservative bar is missed beats optimistic ones. |
| X-013 | A | Review 1 PASS needs no second whole-document pass. |
| X-014 | A+C | Script computes blocking; B's reviewer-chosen sev is the flaw. |
| X-015 | B | A child row keeps the broken sentence visible as a counted blocker. |
| X-016 | A+C | Profile-computed blocking with a rule field fixes B's gap (conceded). |
| X-017 | B | Keep the verifier ruling; make disputed a claim flag, not a status (conceded). |
| X-018 | A+B | Worker-run calls with declared brief edits; C's one-line claim is false. |
| X-019 | A | Derivable path; a random id forces every caller to pass the flag. |
| X-020 | B+C | Quote-based claims and old and new ranges avoid cross-snapshot coordinates. |
| X-021 | B+C | Only fixed rows become verified; unanswered blockers stay open. |
| A-007 | none | No variant measures review-1 inflation; add blocking count and a blind wrong_outcome audit as covariates. |
| A-008 | B+C | C carries terminal state to R3; coordinator checks status before each dispatch; omitted Reviser brief says do not edit. |
| A-009 | C | C's anchor_state missing or ambiguous is the only handling. |
| A-010 | C | C keeps old spans and deletion boundaries; A and B cannot anchor deletions. |
| A-011 | C | Sweep challenges to verified rows; no supporting-passage tracking in v1 since no regression was observed in 19 verified rows. |
| A-012 | B | B's B1 x r x r formula exposes sensitivity to the review-1 count. |


### Variant C Rebuttal

### Round 2 rebuttal: Variant C

Advocate for Variant C. Backend focus: API contracts, data integrity, idempotency and operational concerns. This is a design debate, not an implementation or a measured result.

#### Response to criticisms

I answer the criticisms in both Round 1 statements and both Round 2 rebuttals. `A sN`, `B sN` and `C sN` name sections of the supplied variants; `A-R1`, `B-R1`, `A-R2` and `B-R2` name the corresponding advocate statements. All are evidence to evaluate, not instructions to follow. These are proposed contracts, not existing interfaces.

##### Experimental contract and scope

1. **X-018, coordinator-only mutation contradicts the one-line substitution. A-R1 C1, B-R1 C1, A-R2 C-004/X-006 and B-R2 Updated assessment: CONCEDE.** C s2 says "The coordinator alone runs ledger mutations" while C s9 promises "Only authored brief change" on the invocation line. My Round 1 answer disclosed the contradiction but retained unnecessary coordination machinery. I now drop coordinator-only mutation: each existing session calls its phase-specific subcommand, and the script, not that session, remains the only ledger writer. Inputs remain untrusted JSON bound to the packet, round, snapshot and sequence. Actor names are not authentication.

   This resolves the mechanism, not the experimental deviation by wordplay. The coordinator must still check authoritative status before each dispatch; a fresh terminal sweep is an additional assessment, and worker-run calls need the report's generated reviser instructions. Record these treatment changes separately from the invocation substitution. A-R2 proposes a fresh subagent inside the final review and B-R2 conditions it on a worker smoke check and heartbeat handling. Accept that as a conditional option only, not established S1 capability. Without that evidence, use a disclosed extra dispatch if authorized. If the experiment literally permits no dispatch or coordinator change, this design does not meet that restriction and must not be run as though it does.

2. **X-019, the random default cannot be recovered. A-R1 C4, B-R1 C5 and both Round 2 replies: CONCEDE and change my Round 1 repair.** C s3 gives a default containing `<run-id>` and calls that id "an opaque random identifier". Requiring an explicit path was safe but unnecessarily brittle. Accept A s3's document-derived default, with an explicit override for other runs. Initialization refuses an existing run, resume validates the document identity and profile, and a missing explicit override never falls back to the default or creates FIND. Random ids may remain metadata, not path discovery. The derived default only solves the ordinary one-run case; concurrent experimental runs must use distinct explicit paths recorded before dispatch.

3. **One-row discovery and the 200-line refusal test overflow rather than convergence. A-R1 C2, B-R1 C2, X-004 and B-R2 New evidence 2: CONCEDE.** C s2 explicitly says "at most one new finding C001" and review 3 has "No discovery check remains". My Round 1 concession stands: drop both restrictions, not merely raise the quota. Reviews 2 and 3 each inspect the finite changed packet on both diff sides, including deletion boundaries and B's evidenced dependency exception. Retain every structured allegation; inability to complete the packet yields `cannot-verify` and an incomplete/escalated result, not truncation or apparent convergence. Large packets warn, not automatically fail at 200 lines.

4. **Hard admission has no recovery for reflow or an unlisted legitimate gap. A-R1 C3, B-R1 C4, A-R2 C-017/X-005 and B-R2 C3: PARTLY CONCEDE.** C s3 says "uncovered edits fail revision admission", and C s11 acknowledges "may require manual recovery". The admission boundary is needed because an optional check does not enforce the experiment. Accept A's checks at both `answer` and `begin` and B's preimage-checked `revert-unclaimed`, with offending hunks and recovery instructions in the refusal. A necessary FR-8/FR-9 edit must have an explicit blocking-row claim with precise old/new spans; an unrelated gap belongs in the disposition and later assessment, not an invented claim.

   Two qualifications prevent data loss. Retain raw hunks and map every non-whitespace change to an explicit claim; whitespace-only reflow may be recorded without sponsoring discovery, but whitespace that changes document structure is not harmless. Revert only the named unclaimed hunks, only under existing edit authorization and exclusive reviser ownership of the document, and only when the checked preimage still matches. A verifier's ability to invoke a helper does not grant permission to discard edits. Recovery can itself refuse after a race, so replace A-R2's "the loop cannot stall" with an honest tested recovery path and a reported stop when safety cannot be established.

##### Storage and API contract

5. **The transaction machinery is too heavy. A-R1 C5, B-R1 C3 and both Round 2 assessments: MOSTLY CONCEDE.** C s6 requires no-replace hard-link publication, directory sync and refusal of unsupported filesystems. Those are stronger durability requirements than this bounded single-host experiment needs. Keep a small process-crash-safe commit protocol, not a filesystem certification project. Atomic replacement alone does not prevent lost updates or duplicate logical operations; both advocates now accept the lock, operation id and expected sequence. The exact retained and dropped parts are listed below.

6. **Replay makes every reader a reducer and every schema change harder. A-R1 C6, A-R2 S-005/C-001 and B-R2 Updated assessment: CONCEDE THE NEED, QUALIFY THE DESCRIPTION.** C s3 says "A row's current status is obtained by replaying events". That could use one shared reducer rather than several implementations, but it still adds a reducer and replay-version obligations we do not need. Adopt A's single state object containing current rows, per-row history, sequence and operation results, updated together in one atomic replacement. Reports and plans remain disposable projections. There must not be a second independently writable history or counts file.

7. **Exit 0 on ESCALATE can mislead a shell coordinator. B-R1 C7: COUNTER, now resolved by B-R2 A4.** C s6 explicitly says "callers inspect JSON, never infer PASS from process success". That is the contract, not an accidental permission to continue. A committed ESCALATE is a successful state change; a nonzero CONTINUE looks like an operational failure and can encourage a duplicate call. Accept A-R2 and B-R2's resolution: committed mutations exit 0, JSON names decision and next action, nonzero means refusal/error, and the read-only `verdict` command alone provides decision-coded exits for shell callers. Dispatch must use current status, never just the previous process exit.

8. **C lacks the command-copy parity guard. B-R1 C6: CONCEDE.** C s6's outline and "unchanged original-command contract" test do not specify a drift test for the new panel body. Accept B s6's copy-and-drift test, including the explicitly omitted Unattended-mode section, while keeping the original command and pinned severity tests unchanged. I do not claim that C's outline already provided that coverage.

9. **A wrong frozen blocker has no way out. B-R1 C8 and B-R2 C6: PARTLY CONCEDE.** C s3 says "Disputed blockers escalate honestly" and rejects a user-waiver API. That is a bounded exit to the user, not FAIL forever; however, it lacks B's explicit dispute ruling. Accept a dispute as a claim flag with an evidence-bearing verifier ruling. An accepted dispute may close an invalid finding only when current-snapshot evidence proves the original alleged harm absent, not merely because somebody dislikes its grade. An unruled or uncertain blocker remains unresolved. Also accept B-R2's narrower post-escalation annotation of claimed user demotion only if it changes neither frozen grading, counted history nor delivery outcome. A quoted string is not permission, and no automatic waiver path belongs in this experiment.

10. **Script-written reports remove the panel's expert prose. A-R1 C9, A-R2 C-029 and B-R1 C9/B-R2 C6: CONCEDE.** C s2 says the script "writes reports/review-1.md from ledger state" and C s12 explicitly acknowledges "reduced formatting freedom". My Round 1 defense protected authoritative counts, not a good reason to replace the whole narrative. Accept A-R2's split: reviewer-owned expert prose without its own authoritative row-status table or verdict, followed by the script-rendered table, next action and verdict. Accept B-R2's actionable refusal naming conflicting lines instead of silently rewriting the prose. Store the admitted narrative digest so a crash after ledger commit can rebuild exactly one generated tail rather than append a second one.

##### Outcomes, measurements and remaining safeguards

11. **C counts more rows but forecasts the lowest result. A-R1 C7, B-R1 C2 and A/B's forecast criticisms: CONCEDE THE FORECAST, REVISE MY ROUND 1 METRIC HESITATION.** C s9 says "A MAJOR note still belongs to the critical+major proxy" yet predicts mean 1.5 without a trace. Withdraw 1.5 and 22.5% as supported forecasts. Both Round 2 advocates now accept deferred MAJOR rows in the headline because the historical proxy counted grade separately from blocking. I re-read that report: its line 37 expressly distinguishes those counts. Restore C's grade-based unresolved set, union it with deduplicated sweep findings and challenges, and publish blocking-only and deferred shares separately. This fixes a population mismatch, not evidence that the ledger will hit the bar. Use B's conditional B1 x r1 x r2 sensitivity analysis as a planning aid, not a measured or calibrated prediction of the combined sweep proxy.

12. **Sweep blockers appear in both B and S. A-R1 C8: CONCEDE THE AMBIGUITY.** C s4 says "A deferred blocking sweep row also counts" in B, then defines S separately. Use disjoint sources: loop unresolved blockers in B, terminal sweep allegations/challenges in S, with identity-based union for the headline proxy. A sweep blocker forces delivery ESCALATE even when loop decision was PASS, but it cannot buy another fix cycle. No addition counts the same defect twice.

13. **A sweep after review-1 PASS rereads identical bytes. B-R2 C6 and both advocates' C-030/X-013: ACCEPT THE SMALLER POLICY.** C s2 requires a sweep "even early PASS". For this experiment, accept A's exception when no revision occurred and the live document still hashes to the FIND snapshot: record `sweep_skipped=review1_pass`, actual assessments and the unchanged terminal bytes. This is a cost choice, not proof that the first reviewer was exhaustive or that another sample would find nothing. Any terminal decision after a revision still needs the fresh full-document sweep. Baseline recall checks remain measurement work, not concealed remediation assessments.

14. **Dependency-passage tracking is unsupported scope in version 1. B-R2 Updated assessment/New evidence 2 against C-R1 C-022/A-011: ACCEPT DEFERRAL, REJECT THE SAFETY INFERENCE.** C s3 carries verification only when mapped text and "supporting context" are unchanged, but never defines complete supporting context. I accept B-R2's retouch reset plus lexical warning and sweep challenges for version 1 rather than a dependency graph. The reported zero regressions among 19 prior-blocker resolutions do not establish that remote changes cannot invalidate a fix: those reports classified N1 and N12 as new findings. State the limitation plainly and measure sweep challenges and outside-hunk harms. A known explicit dependency may still support a new VERIFY allegation under B's existing `depends_on` rule; do not discard a valid allegation because its original sentence is untouched.

15. **Inline rule labels scatter the contract. A-R1 S-012 and B-R2 C6: CONCEDE.** C s2 labels rules throughout the document. Accept one end table with MECHANICAL/PROSE and a residual-risk column, as B s11 provides. Closed input schemas, answer completeness and clear errors remain mandatory even without repeated labels. Defer C's separate user guide and duplicated external schema validator; one contract, one validator and executable fixtures are enough for the experiment.

16. **Shared limits and the added assessment. Both advocates' A-007/A-008 and B-R2 C7: AGREE, WITH NO IMPLEMENTATION CLAIM.** C s4 says "Do not claim the total number of assessments is three"; keep that wording for full runs, count a fresh subagent as an assessment too, and require a decision on any literal three-assessment restriction. Keep blind grading checks, actual command/skill/script hashes, pre-dispatch status checks, terminal-byte recording and live-versus-accepted mismatch checks. A ledger cannot stop a previously launched reviser editing the live document, establish semantic truth, authenticate shared-account actors or prove sweep independence from its row counts. No such guarantee follows from file hashes.

##### Which parts of C's transaction machinery this experiment needs

| C machinery | Decision for this experiment | Reason and replacement |
|---|---|---|
| Event replay as the authoritative store | Drop from version 1. | One atomic state object holds current rows, history, sequence and saved operation results; a shared validator checks it. Replay is not required for idempotency. |
| No-replace hard-link artifact publish | Drop. | Under the stable per-ledger lock, publish snapshots/diffs by same-directory temporary file and atomic replacement before publishing their references; an existing immutable artifact must match its recorded hash or the call refuses. |
| fsync | Keep file sync for committed state and newly referenced snapshot/diff files; defer directory sync and host-power-loss guarantees. | This targets interrupted processes on the stated local host, not guaranteed persistence of every rename after a host/storage failure. Missing or corrupt dependencies stop resume; they never turn into a new FIND or PASS. |
| Advisory lock | Keep a nonblocking per-ledger lock. | It serializes helper calls, including retry races; use a stable lock file, not the replaceable ledger inode, and do not steal a lock on a timer. It does not lock model edits to the document. |
| `--op` and request-digest idempotency | Keep. | Same operation and payload returns the saved result without consuming a review; changed payload under that operation refuses. Save result and state in the same commit. |
| `--expect-seq` | Keep. | After looking for an already committed identical operation, reject stale new operations. Packet identity and document hash bind the reviewed bytes independently of call ordering. |
| Coordinator-only mutation | Drop. | Sessions call phase-specific commands; the script remains the only state writer and validates every input. The coordinator gates dispatch on current status. |
| 200-line discovery limit | Drop. | Complete finite changed packets in both VERIFY rounds, warn on size, and explicitly stop if coverage cannot be completed; never truncate evidence. |
| One-row discovery budget | Drop. | Retain all in-scope allegations in both rounds. This experiments on edit control and counting, not on how often an arbitrary quota forces escalation. |

Keep small failure tests around dependency publication and ledger replacement, duplicate/different-op retries, stale sequence refusal, two helper writers and regeneration of reports after a committed state change. Defer the exhaustive hard-link/directory-sync fault matrix and unsupported-filesystem certification. A retry returns its original result, which may describe an older sequence; every dispatch therefore reads fresh status instead of blindly following an old returned `next_action`.

#### Updated assessment

**A is the best implementation frame after its Round 2 corrections.** I now accept its single current-state object with per-row history, document-derived default, kernel/contract/adapter separation, script-built plan and subcommand-inferred role. A-R2 properly narrows the profile claim: profiles can reuse existing guards, but a new guard requires kernel work and tests; that does not justify implementing future adopter guards in the S1 version. Its concessions on outcome authority, unanswered rows, coordinates and hard admission remove the main reliability objections I raised. I still reject a guarantee that any session can safely revert document changes or that a recovery command makes stalling impossible. Report projection also needs an idempotent crash path, not just a check of the previous report's last line.

**B supplies the best failure analysis and measurement frame, strengthened by its repairs.** Its named profile, rule field, removed role flag, explicit dispute ruling, lock, operation identity, accepted sequence check and hard admission repair are substantial improvements. I accept its simpler version-1 retouch policy, while treating zero observed status regressions as limited evidence rather than a semantic guarantee. Two Round 2 claims need correction: a sweep's hidden-defect share cannot prove whether it read the ledger, and equal anchors or overlapping spans are only duplicate candidates, not proof of the same defect. The same sentence can contain the resolved original harm and a new child defect. Preserve separate allegations and use blinded semantic adjudication for measurement instead of dropping rows on overlap alone.

**C should contribute safeguards, not a miniature event-storage platform.** Retain packet/snapshot binding, exact response coverage, `cannot-verify`, relocation and tombstones, raw old/new diffs, strict admission, operation idempotency, expected sequence and the loop/delivery split. Drop replay-only storage, coordinator-only calls, hard links, directory-sync guarantees, arbitrary discovery quotas, whole-report ownership and extra version-1 documentation/schema machinery. Adopt the no-revision review-1 PASS exception and the grade-based proxy, but retain a fresh sweep after every terminal decision involving a revision. No implementation, installation, live sweep or worker capability test was performed for this rebuttal.

#### New evidence

These source passages were opened for Round 2. They strengthen or qualify Round 1 claims; the proposed safeguards below them are design inferences, not observed implementation behavior.

1. **The historical proxy counted grade separately from operational blocking.** `/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase4/ARMB-REPORT.md:37` says "The 427 grading relabels some MAJOR findings as minor ... so proxy and blocking differ". This supports A-R2 and B-R2's adoption of C's deferred-MAJOR inclusion and changes my Round 1 `none` pick on X-011 to C. It does not prove exact comparability between an accumulated finding ledger and a fresh end-state critique, so publish components and baseline sweeps too.

2. **Zero recorded regressions is a reporting category, not zero fix-induced harm.** `/home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r2/.dev/orca-command-refactor/review/spec-panel-round2.md:50` says "13 resolved, 0 open, 0 regressed" and immediately says "the F10 fix creates new blocking finding N1". `/home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r2/.dev/orca-command-refactor/review/spec-panel-round3.md:47` similarly says "6 resolved, 0 open, 0 regressed" and "The N5 fix introduces new blocking finding N12". B-R2's 19 total is arithmetically right, but these are prior-blocker resolution counts in successive reviews, not 19 independent tests showing that every verified fix remains safe under remote edits. They justify retaining discovery in both VERIFY rounds, not declaring the dependency problem solved.

3. **Overlap is insufficient to deduplicate a child defect.** `/home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r2/.dev/orca-command-refactor/review/spec-panel-round3.md:35` calls N5 "resolved as asked; the fix introduces N12" and locates both the replacement and the new failure in AC-0.4. This directly qualifies B-R2's overlap-based union proposal: overlapping evidence can describe distinct harms. The helper can suggest `dup_of`, but a semantic ruling must distinguish duplicate, independent child and challenge to a verified row; preserve the raw allegations in all cases.

4. **The stronger adopter has more than an ordered severity count.** `/home/coder/workspaces/worktrees/IronClaude/bs346-ledger/src/superclaude/agents/rf-qa.md:401` requires strictly shrinking open blockers; `:407-412` requires regression detection first; `:414` says a repeated synthetic finding with the same dedup key "is a DEDUP case, not a regression". This confirms A-R2's narrowed profile seam and C's warning against flattening rf-qa into spec-panel. A later adapter must preserve identity/dedup semantics as well as halt order; do not build that adopter in the S1 experiment.

Not newly verified here: worker permission/capability to spawn a fresh sweep subagent, heartbeat behavior during that call, filesystem timings, full historical byte attribution, or semantic grading of all six controls. I use the advocates' smoke-check proposal as a prerequisite, not a claimed result.

#### Proposed resolution of split points

The 22 split points are all covered below. Acceptance names the Round 2 proposal, including the stated qualifications; it does not adopt every claim in that variant.

| Point | Concrete merged rule | Round 2 proposal accepted |
|---|---|---|
| C-005 status set and who may change it | Use only `open`, `deferred`, `fixed`, `verified`, `reopened`: the script derives initial deferral and retouch resets, the reviser requests `fixed`, and the verifier verifies a supported fix or rules on an evidenced dispute. Number transitions with phase/error columns, and distinguish `open` from `reopened` by whether an earlier verification exists, not simply by the previous status. | Accept A-R2 and B-R2, with the history distinction made explicit. |
| C-008 frozen fields | Freeze id, label, discovery round, origin, parent attribution, grade, rule, wrong outcome, computed blocking, original finding text and original snapshot-qualified anchor/location at creation. Later inputs cannot replace them; relocation mappings and later evidence are separate records. | Accept A-R2 and B-R2. |
| C-016 bounded new-defect check | In both VERIFY rounds inspect all changed old/new ranges and deletion boundaries, accepting a row on unchanged text only with an explicit changed-range dependency; no one-row or 200-line discovery cap remains. Oversize packets warn, while incomplete coverage is recorded as `cannot-verify` and escalates rather than silently omitting allegations. | Accept A-R2 and B-R2. |
| C-017 reviser edits outside listed rows | Both `answer` and `begin` refuse admission of non-whitespace edits outside precise spans claimed for listed blocking rows, and preserve raw old/new hunks for inspection. Refusals identify unclaimed hunks and offer preimage-checked restoration under existing reviser authorization; structurally meaningful whitespace is not exempt, and recovery is allowed to stop safely on a race. | Accept A-R2/B-R2's hard gate and recovery; qualify authorization, whitespace and the no-stall claim. |
| C-021 verifier answer per row | Require exactly one `resolved`, `open`, `regressed` or `cannot-verify` answer per planned row with snapshot-bound evidence and touched-sentence assessment; deletion evidence cites the old span and new boundary, not a nonexistent new quote. A broken replacement requires a separately graded child allegation, and a disputed claim requires an explicit evidence-bearing ruling rather than an automatic waiver. | Accept A-R2 and B-R2, adding the deletion evidence case from C. |
| C-022 re-checking verified rows | Reset a verified row to `fixed` when raw mapped claim text is retouched, refuse direct regression of untouched rows, and defer a supporting-passage dependency system in version 1. Keep B-R2's lexical warning, allow evidenced dependent allegations as new rows, and count fresh-sweep challenges to carried verifications in delivery and measurement. | Accept B-R2's smaller version-1 policy, not A-R2's new passage-tracking requirement. |
| C-025 crash, idempotency, concurrency | Under a stable nonblocking per-ledger advisory lock, validate all inputs, publish file-synced snapshot/diff dependencies, then atomically replace the single file-synced state object containing history, sequence and operation result. Check identical operations before rejecting an old expected sequence, refuse changed payloads or stale new operations, and drop hard links/directory-sync guarantees while failing closed on missing dependencies. | Accept A-R2 and B-R2's reduced transaction, with dependency ordering and original-result storage explicit. |
| C-027 script CLI and exit codes | Use A's eight commands (`init`, `find`, `answer`, `begin`, `verify`, `sweep`, `close`, `status`) plus `revert-unclaimed` and read-only `verdict`, with JSON stdout and distinct refusal/error codes. Committed mutations exit 0 regardless of outcome; only `verdict` maps PASS/CONTINUE/ESCALATE to 0/10/11, and incomplete state never defaults to PASS. | Accept A-R2 and B-R2; no role flag, separate renderer or waiver command. |
| C-029 report writing and verdict line | Reviewer prose contains no competing row-status table or verdict; `close` identifies conflicts and asks for correction, then renders one authoritative table, next action, CONTINUE-only reviser brief and final verdict when required assessments are complete. Pin the admitted narrative and regenerate the tail idempotently after a crash, check its digest/tail on later calls and perform a final status check rather than relying only on the next review. | Accept A-R2 and B-R2, adding the crash/retry and final-check requirements. |
| C-031 reflect adoption | Defer adoption: a later adapter admits canonical rows only after synthesis, merge and the evidence gate, supports the actual multi-file/caller-owned loop, and pins its own grading policy. It must preserve reviewer diversity/evidence validation and cannot treat ledger PASS as promotion authority. | Accept A-R2 and B-R2. |
| C-032 rf-qa adoption | Defer adoption: a later adapter preserves regression before monotonicity before cap, current halt messages and synthetic-finding dedup identity, with profile-specific grades rather than spec-panel defaults. Existing guards may be selected by a profile, but a new guard requires kernel changes and its own tests; build only the spec-panel profile now. | Accept A-R2 and B-R2, explicitly preserving dedup semantics and version-1 scope. |
| C-033 implement final review adoption | Do not adopt in this experiment; any later ledger use may track repair rows but cannot replace or narrow the fresh full FINAL required for each archive attempt. Its own retry and archive gates remain separate. | Accept A-R2 and B-R2. |
| C-034 stateful session vs file ledger | The file ledger is authoritative and fresh sessions consume its packets; resumed/cached output must match the current packet digest or be refused. A stateful-session comparison is a later experiment, not an alternate source of truth in this one. | Accept A-R2 and B-R2. |
| C-040 validity checks and controls | Combine script-use/phase compliance, baseline full sweeps on the six historical finals with hidden-defect measurements, and recorded command/skill/script hashes plus live-versus-snapshot checks. Count refusals, incomplete runs, post-terminal edits and all sweep costs; neither a low hidden-defect share nor absence of row ids proves an independent sweep. | Accept A-R2 and B-R2's three-part checks, rejecting an independence guarantee from the metrics. |
| C-043 cap enforcement mechanics | Pin `CAP_REVIEWS = 3` to the canonical cap text and refuse a fourth review, third fix, second sweep or repeated FIND/init on an existing run even under a new operation id. No committed review-3 decision authorizes CONTINUE; identical retries return the old committed result rather than consume a slot. | Accept A-R2 and B-R2. |
| S-008 CLI spec form | Use one table showing command, caller, inputs, state/artifact writes, output, checks and exits, followed by one transaction/crash/rerun subsection. Include the difference between successful execution, pending work and a delivery verdict. | Accept A-R2 and B-R2. |
| S-009 test plan placement | Put named behavior tests, command pins and parity tests in one Tests subsection and list executable fixture files in the file table. Include stale packets, partial inputs, deletions, ambiguous relocation, both admission gates, checked restoration, retry races, dependency publication and report regeneration; defer the discarded durability matrix. | Accept A-R2 and B-R2's placement, reducing tests with the removed mechanisms. |
| S-012 rule classification placement | Use one end table with MECHANICAL/PROSE and residual-risk columns, not repeated inline labels. Separate schema validity, evidence presence and semantic truth instead of calling all three mechanically proven. | Accept A-R2 and B-R2. |
| X-005 unclaimed reviser edits | Enforce the C-017 admission check even when the reviser skipped its own check, and keep a preimage-checked recovery that cannot silently erase newer or authorized claimed work. A refusal is a surfaced failure or recoverable stop, not a counted clean review. | Accept A-R2 and B-R2, with authorization and loss-prevention qualifications. |
| X-006 who calls the script | Each session invokes its phase-specific subcommand; the script validates JSON evidence bound to round, snapshot and sequence, and actor identity is not claimed authenticated. The coordinator checks current next action before every dispatch, never follows a stale retry response and never launches another reviser after termination. | Accept A-R2 and B-R2; drop C's coordinator-only mutation. |
| X-011 deferred MAJOR rows in R3 count | Count unverified CRITICAL/MAJOR findings by grade, including deferred notes, unioned with new sweep findings and challenges to verified rows, and publish loop-only, blocking-only, deferred and raw/deduplicated sweep components. Use overlap only to suggest duplicates, with blinded semantic adjudication preserving distinct harms; carry early terminal bytes/counts to the R3 horizon without inventing a review. | Accept A-R2 and B-R2 on C's grade-based set, qualify B-R2's automatic overlap matching. |
| X-017 intra-B disputed status | `disputed` is a claim flag on an unresolved row, never a sixth status, and the verifier must accept or reject it with evidence about the original alleged harm. Unruled, rejected or uncertain disputes remain unresolved; a quote claiming user permission cannot clear a real blocker or change a recorded escalation. | Accept A-R2 and B-R2, with the evidence/waiver distinction explicit. |

#### Positions table

All 85 points are included. Unchanged rows are copied from my Round 1 table; `(changed)` marks a changed pick or reason. Combinations select useful parts, not every original claim. Forecast picks rate the support for a planning method, not evidence of an achieved result.

| Point | Preferred | Reason |
|---|---|---|
| S-001 | A | Specific titles expose compatibility obligations instead of hiding adopter differences. |
| S-002 | B | Explicit citation aliases and unverified markers make provenance easier to audit. |
| S-003 | B | Actor, input, output, and call order are visible together. |
| S-004 | A | Kernel, contract, and adapter boundaries clarify ownership; adapter policy still needs testing. |
| S-005 | A | (changed) One atomic state object with per-row history avoids an unnecessary replay reducer. |
| S-006 | A+B | (changed) B's numbered phase table with A's named refusal codes makes the corrected transitions testable. |
| S-007 | B+C | Combine worked decisions with explicit integrity, pending, and delivery states. |
| S-008 | A+C | (changed) Use A's command table followed by C's closed-input and reduced transaction/rerun contract. |
| S-009 | A+C | (changed) Named cases and executable fixtures belong in one Tests subsection, with B's parity pins included. |
| S-010 | B | Trace-based estimates expose assumptions better than unsupported optimistic point forecasts. |
| S-011 | B | Evidence, residual causes, and self-attack prevent overstating what the ledger fixes. |
| S-012 | B | (changed) One end table with residual risks is easier to audit than scattered inline labels. |
| S-013 | A+B | (changed) One design/contract and executable fixtures suffice; defer the separate guide and duplicated schema machinery. |
| S-014 | B | An explicit unverified inventory is more honest than prematurely declaring completion. |
| S-015 | A | Moderate prose and tables are easier to scan than either dense aliases or repeated labels. |
| C-001 | A | (changed) Current rows, history, sequence and operation results commit together in one closed-schema state object. |
| C-002 | A | (changed) Derive the ordinary default from the document; explicit overrides never fall back or restart FIND. |
| C-003 | C | Snapshot admission and old/new diff ranges bind each accepted revision to its evidence. |
| C-004 | A | (changed) Sessions invoke phase-specific commands; the script validates typed evidence and remains the only state writer. |
| C-005 | B+C | (changed) B's phase table and script retouch reset combine with C's history-based open versus reopened distinction. |
| C-006 | B+C | (changed) Keep disputes as claims and require an evidence-bearing ruling; uncertainty remains unresolved. |
| C-007 | A+C | Escalate grading disputes; avoid a waiver API whose quoted authority cannot be authenticated. |
| C-008 | A+C | (changed) Freeze A's identity/grade/rule fields plus C's original issue text; keep relocation separate. |
| C-009 | A+C | Compute blocking from an explicit criterion and profile, never reviewer-supplied blocking labels. |
| C-010 | C | Incomplete evidence, uncertainty, and integrity failures cannot yield an accidental PASS. |
| C-011 | B+C | Every unresolved blocker affects delivery; keep loop and sweep counts explicit and nonoverlapping. |
| C-012 | C | Count the extra assessment honestly; session naming cannot erase its cost. |
| C-013 | C | Distinct provisional and delivery outcomes prevent publishing PASS before the sweep. |
| C-014 | B+C | Preserve spec-panel's cap; structural uncertainty escalates without importing rf-qa's monotonicity policy. |
| C-015 | B+C | Combine admission refusal for note-sponsored edits with measured minor-span touches. |
| C-016 | A+B | (changed) Both VERIFY rounds inspect complete changed packets without a row quota; C's cannot-verify protects incomplete coverage. |
| C-017 | B+C | (changed) Hard admission at both ends with preimage-checked, authorized restoration is stronger than either original alone. |
| C-018 | C | Exact context and snapshot identity disambiguate anchors without trusting line hints alone. |
| C-019 | C | Explicit relocation and deletion tombstones avoid silent nearest-match errors. |
| C-020 | C | Raw ownership and dual-sided ranges preserve deletions and whitespace-sensitive evidence. |
| C-021 | B+C | (changed) Require explicit uncertainty and snapshot evidence, plus B's graded child allegation and dispute ruling. |
| C-022 | A+B | (changed) Version 1 uses mapped retouch resets and warnings, not a new dependency system; the sweep remains a residual safeguard. |
| C-023 | C | Hunk overlap proves location, not causation; preserve independent causal adjudication. |
| C-024 | A+C | Add accidental-edit checksums to packet binding; neither mechanism authenticates deliberate editors. |
| C-025 | B+C | (changed) Keep lock, operation id, sequence and file-synced atomic state; drop hard links and directory durability guarantees. |
| C-026 | B | Its installation naming analysis supplies the clearest packaging and activation contract. |
| C-027 | A+C | (changed) A's lean command set and C's JSON/decision separation survive; only verdict supplies decision-coded exits. |
| C-028 | B | Drift tests preserve the panel while explicitly excluding unsupported unattended behavior. |
| C-029 | A+B | (changed) Preserve panel prose but generate the authoritative table/tail, with conflict checks and idempotent regeneration. |
| C-030 | A | (changed) Skip the sweep only for a no-revision review-1 PASS on identical pinned bytes, recording the exception. |
| C-031 | B+C | (changed) Defer multi-file/caller-owned adoption; merge and validate before ids, and never grant promotion authority. |
| C-032 | B+C | (changed) Defer adoption while preserving ordered guards, existing halt messages and synthetic dedup identity. |
| C-033 | B+C | Defer adoption; any later sidecar must preserve mandatory fresh independent FINALs. |
| C-034 | C | Session continuity is optional; packet identity and file state remain authoritative. |
| C-035 | A+C | (changed) Use a grade-based unresolved set including deferred MAJORs, unioned with adjudicated sweep findings and challenges. |
| C-036 | B | (changed) The traced conditional formula is useful for sensitivity, not a calibrated combined-proxy forecast. |
| C-037 | B | Byte-share arithmetic is stronger evidence than an unexplained growth forecast. |
| C-038 | B+C | Preserve fixed bars and spread rules; add baseline-sweep, leakage, and operational failure checks. |
| C-039 | none | Disclose coordinator gating and the added sweep separately from unchanged actor brief text. |
| C-040 | A+B | (changed) Combine compliance and baseline sweeps, adding C's activation hashes and live/snapshot checks. |
| C-041 | B+C | Count the sixth session and all calls; distinguish estimates from observed durations. |
| C-042 | B | (changed) Warn on large changed packets and retain allegations; arbitrary discovery thresholds must not manufacture convergence. |
| C-043 | A+C | Preserve pinned cap tests and history-derived refusal of repeated FIND, extra fixes, and sweeps. |
| X-001 | B+C | A sweep blocker prevents final PASS without authorizing another automatic fix cycle. |
| X-002 | B+C | A fresh terminal reviewer reduces anchoring; count its extra session explicitly. |
| X-003 | B+C | No evidence requires an additional spec-panel monotonicity stop; retain adopter-specific guards separately. |
| X-004 | A+B | (changed) Both rounds must retain fix-induced rows; quota removal corrects C rather than hiding the later defect. |
| X-005 | B+C | (changed) Mandatory admission plus checked recovery closes skipped-check bypasses without silently discarding newer edits. |
| X-006 | A | (changed) Sessions call their subcommands; coordinator-only calls add no authentication and are unnecessary. |
| X-007 | C | A committed escalation is operational success; consumers must inspect the explicit decision field. |
| X-008 | A | (changed) A document-derived default tolerates a lost ordinary flag; a missing explicit override still fails closed. |
| X-009 | B | Its explicit omission avoids claiming an unattended contract the variant has not established. |
| X-010 | B | Presence-only baseline checks do not justify changing unrelated installation lists. |
| X-011 | C | (changed) Historical proxy grading supports including deferred MAJORs; publish the blocking and deferred components separately. |
| X-012 | B | Trace-based pessimism is more credible than C's unexplained lowest forecast. |
| X-013 | A | (changed) No revision means unchanged FIND bytes; record a skipped sweep rather than charge an unnecessary remediation assessment. |
| X-014 | A+C | The script derives blocking from criteria instead of trusting reviewer-selected severity classes. |
| X-015 | B | Preserve original resolution plus an explicit graded child; do not accept an unexplained broken-sentence flag. |
| X-016 | A+C | Include criterion in the input and derive FR blocking mechanically. |
| X-017 | B | (changed) B's repaired claim flag and mandatory evidence-based ruling resolve the contradictory sixth status. |
| X-018 | A+B | (changed) Worker-run calls remove C's coordinator-only contradiction, but status gating and sweep changes remain disclosed treatment variables. |
| X-019 | A | (changed) Derive the default from the document, reject existing initialization, and keep random ids as metadata only. |
| X-020 | C | Snapshot-qualified relocation and old/new diff ranges avoid cross-version coordinate comparisons. |
| X-021 | B+C | Require a supported fix or explicit dispute ruling; unanswered rows cannot silently become verified. |
| A-007 | none | Measure blinded review-1 grading disagreement; frozen grades do not prevent initial inflation. |
| A-008 | none | Gate every dispatch on terminal state and detect edits from already-running revisers. |
| A-009 | C | Relocate every live anchor and escalate missing or ambiguous mappings. |
| A-010 | C | Old-side evidence and deletion boundaries allow lost obligations to remain reportable. |
| A-011 | C | (changed) Defer passage tracking, retain sweep challenges and evidenced new dependency allegations, and do not infer safety from zero recorded regressions. |
| A-012 | none | Measure changed FIND behavior; historical initial counts are priors, not treatment invariants. |


## Round 2.5: Invariant Probe

See `invariant-probe.md`. Gate: BLOCKED: 9 HIGH-severity UNADDRESSED invariants (INV-004, INV-006, INV-007, INV-008, INV-013, INV-021, INV-022, INV-027, INV-028); 16 MEDIUM logged as warnings. Depth standard has no Round 3, so the HIGH items are carried into refactor-plan.md as mandatory fixes and the run status is partial.

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| A-007 | none | 90% | Record review-1 grade distribution and filler-outcome share as covariates (F2R3:15 shows brief pressure). |
| A-008 | none | 70% | Coordinator runs `status` before each dispatch; growth from accepted snapshot; later edits flagged. |
| A-009 | Variant C | 90% | C's relocation and `anchor_state` handle drifted anchors. |
| A-010 | Variant C | 90% | Old-side ranges and deletion boundaries let deletion defects be anchored. |
| A-011 | Variant C | 70% | Sweep challenges to verified rows; no supporting-passage tracking in v1 since no regression was observed in 19 verified rows. |
| A-012 | none | 70% | Recompute forecasts from each replicate's measured review-1 blocking count (B1 x r x r). |
| C-001 | Variant A | 90% | One pretty-printed state object with history, plus C's op id and sequence as header fields. |
| C-002 | Variant A | 90% | Path derivable from the document survives a lost flag; `E-EXISTS` stops a second run. |
| C-003 | Variant A + C | 70% | A's per-review snapshots plus C's stored diffs with old and new ranges. |
| C-004 | Variant A | 90% | Sessions call their own subcommand; actor inferred; C's packet binding added. |
| C-005 | Variant B + C | 90% | (changed) B's transition table with phase column and retouch reset; C's history-derived reopen. |
| C-006 | Variant B | 70% | Disputed answer needs an explicit verifier ruling. |
| C-007 | Variant B | 70% | User-only demotion with quoted words, recorded after ESCALATE; no automatic path. |
| C-008 | Variant A + C | 90% | (changed) A's key list plus C's frozen issue text. |
| C-009 | Variant A + C | 70% | Script computes blocking from a profile; reviewer-supplied sev is a hole. |
| C-010 | Variant B + C | 70% | B's count without no-progress halt plus C's integrity and structural escalation. |
| C-011 | Variant B | 70% | Count sweep blockers separately (Lt) instead of mixing into B. |
| C-012 | Variant B + C | 70% | Outside the cap, fresh context (subagent if allowed, else a stated sixth dispatch). |
| C-013 | Variant C | 90% | Separate loop decision and delivery outcome; no early final PASS. |
| C-014 | Variant B | 70% | Data show no-progress halt never fires in S1; guard lives in the rf-qa profile only. |
| C-015 | Variant B + C | 90% | (changed) Refusal on deferred rows, admission check on note-sponsored edits, `minor_touched` metric. |
| C-016 | Variant A + B | 90% | Reviews 2 and 3, no count cap, `depends_on`, both diff sides, cannot-verify on incomplete cover. |
| C-017 | Variant B + C | 90% | (changed) Hard admission at `answer` and `begin`, with preimage-checked `revert-unclaimed`. |
| C-018 | Variant A + B | 70% | Normalized unique quote with minimum length, `--at` to disambiguate. |
| C-019 | Variant C | 90% | Only relocation algorithm that handles unrelated edits and deletions. |
| C-020 | Variant C | 70% | Raw plus normalized sets and kept old spans fix coordinate and deletion gaps. |
| C-021 | Variant B + C | 90% | (changed) C's result set with cannot-verify; B's child row on a broken sentence and dispute ruling. |
| C-022 | Variant A + B | 90% | (changed) B's script reset on retouch plus A's refusal to re-attack untouched rows. |
| C-023 | Variant A + C | 70% | (changed) Script computes location attribution; analyst adjudicates causation for M3. |
| C-024 | Variant A | 70% | Body hash plus report-tail check catches both edit paths. |
| C-025 | Variant B + C | 90% | (changed) Atomic replace plus flock, op id and expected sequence; no hard-link layer. |
| C-026 | Variant B | 70% | Same layout, plus install-trap warning and reason to reject a CLI subcommand. |
| C-027 | Variant A + C | 90% | A's lean subcommand set with C's JSON stdout and decision-coded `verdict` only. |
| C-028 | Variant B | 70% | Copy with drift test; omit Unattended mode to keep its test green. |
| C-029 | Variant A + B | 90% | (changed) Reviewer keeps panel prose without its own table or verdict; script appends tail. |
| C-030 | Variant A | 90% | Review-1 PASS made no edits; a second full read of same text adds little. |
| C-031 | Variant B + C | 90% | (changed) B's multi-file and caller-loop needs; C's rule that ledger PASS cannot promote. |
| C-032 | Variant B + C | 90% | (changed) rf-qa.md:401,407 order must be kept; B's lock need; A's profile is the vehicle. |
| C-033 | Variant B + C | 90% | (changed) Defer adoption; any later use keeps mandatory fresh full FINALs. |
| C-034 | Variant C | 70% | (changed) File ledger authoritative; resumed output must carry the current packet digest. |
| C-035 | Variant A + C | 90% | A's dup matching, C's count of deferred MAJOR rows by grade (ARMB:37). |
| C-036 | Variant B | 90% | Forecast derived from traced rows; A's basis used the wrong row (ARMB:13). |
| C-037 | Variant B | 90% | Growth derived arithmetically from measured minor-only byte shares. |
| C-038 | Variant A + B | 70% | A's criteria plus B's baseline-sweep comparison and `minor_touched`. |
| C-039 | none | 90% | (changed) Sweep as a fresh subagent in review 3 if workers may spawn one, else a disclosed sixth dispatch. |
| C-040 | Variant A + B | 90% | V1-ledger (as DEC:64 for Arm B) plus B's baseline sweeps; add C's hash recording. |
| C-041 | Variant B | 70% | Cost grounded in real file timestamps and counts six sessions. |
| C-042 | Variant A + B | 70% | Minimum anchor length plus a warning, not refusals that stall runs. |
| C-043 | Variant A + C | 90% | (changed) A's constant tied to cap text; C's refusal of second sweep and repeated find. |
| S-001 | Variant A | 70% | Section titles name the real commands, easier to search later. |
| S-002 | Variant B | 90% | Alias list plus UNVERIFIED marks make citations checkable. |
| S-003 | Variant B | 90% | One step table shows who, reads, writes and calls at a glance. |
| S-004 | Variant A | 90% | Explicit kernel, contract, adapter split is the reuse seam adopters need. |
| S-005 | Variant A | 90% | Single state document with per-row history; simplest to read and maintain. |
| S-006 | Variant A + B | 90% | (changed) B's numbered transitions with phase column, carrying A's named error codes. |
| S-007 | Variant B | 70% | Worked example on real flg-r2 counts proves the formula. |
| S-008 | Variant A + C | 90% | A's table plus C's separate transaction and rerun subsection. |
| S-009 | Variant A + C | 90% | A's named test cases plus C's fixtures folder, with B's drift test. |
| S-010 | Variant B | 90% | Per-replicate traces and arithmetic make the forecast auditable. |
| S-011 | Variant B | 90% | Evidence column and REMOVED/LEFT verdict are more honest. |
| S-012 | Variant B | 90% | (changed) One end table with residual risk per rule; same as A's place, better content. |
| S-013 | Variant A + B | 90% | One design doc suffices for an experimental variant; user guide premature. |
| S-014 | Variant B | 90% | Explicit UNVERIFIED list is the most useful closing item. |
| S-015 | Variant B | 70% | Dense tables carry more per line than one-sentence lines. |
| X-001 | Variant B + C | 90% | (changed) Sweep blocker forces delivery ESCALATE; C's split is the form. |
| X-002 | Variant B + C | 90% | Fresh context avoids anchoring on just-verified rows. |
| X-003 | Variant B + C | 70% | No second stop for spec-panel; flg-r2 blocking fell 13, 6, 1 so it never fires. |
| X-004 | Variant A + B | 90% | Reviews 2 and 3 must record fix-induced rows like N12. |
| X-005 | Variant B + C | 90% | (changed) Hard admission check with a scripted recovery path, so no stall. |
| X-006 | Variant A | 90% | Each session calls its subcommand; S1 coordinator only dispatches and checks status. |
| X-007 | Variant C | 90% | Exit 0 for committed operations; decision in JSON and in `verdict` only. |
| X-008 | Variant A | 90% | Derivable default with override tolerates a lost flag. |
| X-009 | Variant B | 90% | Verified: test_worker_contract.py:831-839 would fail on A's copy. |
| X-010 | Variant B | 90% | (changed) Presence-only check (test_cli_install.py:501); no edit needed. |
| X-011 | Variant C | 90% | (changed) Arm B proxy counted MAJOR by grade (ARMB:37), so deferred MAJOR rows count. |
| X-012 | Variant B | 90% | Most grounded forecast; honest that the conservative bar may fail. |
| X-013 | Variant A | 90% | No edits after a review-1 PASS, so the find pass is the sweep. |
| X-014 | Variant A + C | 90% | Blocking computed by the script from severity, rule and outcome. |
| X-015 | Variant B | 90% | Broken sentence must become a child row, not just a flag. |
| X-016 | Variant A + C | 90% | (changed) A's `rule` field or C's criterion; both let FR-8/FR-9 be computed. |
| X-017 | Variant B | 90% | (changed) B's repair: disputed is a claim flag with a mandatory verifier ruling. |
| X-018 | Variant A + B | 90% | One-line brief change holds when sessions call the script; sweep dispatch disclosed if needed. |
| X-019 | Variant A | 90% | Derivable default path, no random id. |
| X-020 | Variant C | 70% | Old and new ranges per hunk fix A's coordinate mismatch. |
| X-021 | Variant B + C | 90% | Only `fixed` rows (or ruled disputes) can become verified. |

## Convergence Assessment
- Points resolved: 85 of 85
- Alignment: 100% (85 of 85)
- Threshold: 75%
- Taxonomy coverage: L1, L2 and L3 all have points (diff-analysis.md Taxonomy tags)
- Invariant gate: BLOCKED: 9 HIGH-severity UNADDRESSED invariants (INV-004, INV-006, INV-007, INV-008, INV-013, INV-021, INV-022, INV-027, INV-028); 16 MEDIUM logged as warnings. Depth standard has no Round 3, so the HIGH items are carried into refactor-plan.md as mandatory fixes and the run status is partial.
- Status: BLOCKED_BY_INVARIANTS
- Unresolved points: none
