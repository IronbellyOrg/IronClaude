# Round 2 rebuttal: Variant A (variant-1-opus-architect.md)

Advocate model: opus. Persona: architect (structure, dependencies, long-term impact). Focus: maintainability and extension scaffolding. Inputs read: round1-advocate-A.md, round1-advocate-B.md, round1-advocate-C.md, diff-analysis.md, variant-1 (A), and the repo and experiment files cited under New evidence. Section numbers are each variant's own (A sN, B sN, C sN). "B-R1" and "C-R1" mean the Round 1 statements of advocates B and C.

## Response to criticisms

Criticisms are grouped by source. Where B and C raise the same point, I answer once and say so.

### From advocate B

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

### From advocate C

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

## Updated assessment

**Variant B after its defense.** B-R1 conceded both intra-B contradictions with repairs I accept: `blocking` becomes a profile output with a `rule` field (X-016), and `disputed` becomes a claim flag with a mandatory verifier ruling (X-017). It also dropped `--as` and offered to fold `render`, `verdict` and `show` into `close` and `status`, which removes most of my CLI-surface criticism (A-R1 weakness 4). Its remaining strengths are larger than I scored them: the F22 to N5 to N12 trace is the only causal account, the B1 x r x r bound is the only honest ceiling, and the baseline sweep is the only reference for "hiding". I now rank B's measurement section (s9, s10) as the base of the merged measurement, and A's as a source of the V1-ledger check only. My one standing objection is decision-coded exits from `close` (X-007): C already supplies a dedicated `verdict` subcommand that encodes the decision (C s6), which serves shell coordinators without making every CONTINUE look like a crash.

**Variant C after its defense.** C-R1 conceded X-018, X-019, X-011's comparability problem, its unsupported 1.5 forecast and the arbitrariness of the one-row discovery budget. With those removed, C's remaining core is strong and mostly additive to A: loop and delivery split, `cannot-verify`, anchor relocation with `missing|ambiguous`, old and new ranges, packet binding and operation ids. Two things I still reject. First, the coordinator-only mutation model, which C-R1 admits cannot run under the one-line brief rule. Second, the heavy publication layer (hard-link publish, directory sync, refusal of filesystems, fault injection at every boundary); `flock`, operation id, expected sequence and one atomic replace cover the failures this loop can have. C-R1's own concession 7 asks for "measured cost and filesystem tests" for that layer, which supports deferring it.

**What this does to A's role.** A remains the right skeleton for structure (kernel, contract, adapter; one state file; computed blocking; subcommand-inferred actor; derivable path; report-tail check), but most of A's loop rules lose: sweep session and authority, no-progress stop, `open -> verified`, coordinates, anchors and unclaimed-edit handling all move to B or C. A's measurement forecast is withdrawn. I count that honestly as A contributing the frame and B and C contributing most of the rules inside it.

## New evidence

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

## Proposed resolution of split points

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

## Positions table

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
