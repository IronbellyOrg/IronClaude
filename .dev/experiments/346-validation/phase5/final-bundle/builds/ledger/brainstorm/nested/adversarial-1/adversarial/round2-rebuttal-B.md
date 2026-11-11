# Round 2 rebuttal: Variant B (variant-2-sonnet-analyzer.md, analyzer persona)

Advocate for Variant B (sonnet, analyzer: evidence quality, logical consistency; focus on root cause and evidence). Inputs read: my Round 1 statement, `round1-advocate-A.md`, `round1-advocate-C.md`, `round2-rebuttal-A.md`, `diff-analysis.md`, variant B, and the experiment files cited under New evidence (read-only). Labels: "A s2" means section 2 of variant A, "B-R1" my Round 1 statement, "A-R2" A's rebuttal. Paths: `W` = `/home/coder/workspaces/worktrees/IronClaude`; `F2` = `W/exp346-ab-flg-r2/.dev/orca-command-refactor`; `EXP` = `W/exp346-p1-logs/.dev/experiments/346-validation`; `F2R3` = `F2/review/spec-panel-round3.md`; `F2D1` = `F2/review/disposition.md`; `ARMB-REPORT.md` = `EXP/phase4/ARMB-REPORT.md`; `DES:162` = the 427 design line cited in B-R1.

## Response to criticisms

Each item gives the criticism, then CONCEDE or COUNTER with the evidence. Where A and C made the same point I answer once.

### From advocate A (Round 1 and A-R2)

**A1. "Grading is a reviewer choice, not a computed field"; the FR-8/FR-9 bullet has no field (A-R1 weakness 1; X-014, X-016).** CONCEDE. Variant B's `add` row carries `sev`, `grade`, `anchor`, `finding`, `wrong_outcome` and `init` takes only `--scale` and `--needs-outcome` (variant B, Script CLI table), so the script cannot compute "CRITICAL and FR-8/FR-9 are blocking". Repair, now my rule: drop `sev` from the reviewer's input; add `rule` beside `grade` and `wrong_outcome`; `blocking` is a script output of the named profile `spec-panel`. The predicate is the 427 text at `src/superclaude/commands/spec-panel.md:259`: "CRITICAL and FR-8/FR-9 findings are blocking; MINOR is minor; a MAJOR is blocking only if it names a concrete wrong outcome an implementer would produce, otherwise minor". Written as code: blocking if grade is CRITICAL, or rule is FR-8 or FR-9, or grade is MAJOR with a non-empty `wrong_outcome`; every other row is `deferred`. This also closes the gap I admitted in B-R1 (a MAJOR filed as `sev=minor` had no defined status): it is now `deferred`, and it stays in the headline by grade (X-011). Residual, stated plainly: `grade` is still the reviewer's judgement, so a CRITICAL filed as MINOR is still deferred. A's version has the same residual; it is PROSE and is covered by A-007, not by the script.

**A2. "The adoption seam is call-time flags" (A-R1 weakness 2).** CONCEDE the form, KEEP the reason for it. My flags (`--scale CRITICAL,MAJOR,MINOR --needs-outcome MAJOR`) were meant to keep spec-panel words out of the kernel. A's `PROFILES` table does that better and removes the typo risk. Accepted: `init --profile spec-panel`; the script resolves the profile, writes its name and a hash of its table entry into the ledger header, and refuses any later call that disagrees. Take also the A-R2 refinement (C5): a profile entry carries an ordered list of guards from a fixed menu (`regression`, `monotonicity`, `cap`) with halt messages. A new guard kind is a kernel change with its own tests.

**A3 / C4. "`disputed` as a status" (X-017).** CONCEDE, repair already stated in B-R1 and adopted by A-R2: `disputed` is a claim flag, never a status. T8 reads "From `open` or `reopened` with `claim.action=disputed`; To `verified` if the verifier rules `dispute=accepted`, else `reopened`; the note is required." An unruled dispute at the cap counts as an open blocker (A-R2's addition, accepted). C asked for dispute as evidence, not state; this is that.

**A4. "Large CLI surface; close exit codes 10/11 make CONTINUE look like a crash" (A-R1 weakness 4; A-R2 "one standing objection"; X-007).** CONCEDE on exit codes, with the root cause stated. I coupled the exit code to the decision because the 427 failure was a brief beating the command (`F2R3:15`: "Under the brief, any finding of any severity is FAIL"), and I wanted the machine, not a sentence, to say stop (variant B Precedence bullet: "the exit code of `close` outranks any sentence of a brief"). The flaw is in the carrier: an LLM reads a Bash result whose non-zero code is shown as an error, so CONTINUE (10) can invite a rerun of `close`, which my own table answers with exit 4. That effect is UNVERIFIED for the S1 workers but cheap to avoid, and the stop does not depend on it: the cap is a refusal in `open`, the report's last line is script output, and the JSON names the decision. New rule: every committed operation exits 0; refusals keep my distinct non-zero codes (4 already closed, 6 unmarked `fixed` rows, 7 unclaimed hunks); a read-only `verdict` subcommand maps PASS, CONTINUE, ESCALATE to 0, 10, 11 for shell callers. On surface size: fold `render` and `show` into `status` and `open`, drop `--as` (my own table classes identity as PROSE, so the flag proved nothing; the phase gate is the mechanical part and the actor follows from the subcommand). About nine subcommands remain.

**A5. "A missing flag stops the loop" (A-R1 weakness 5; X-008, X-019).** CONCEDE. Variant B's Mode bullet ("`--ledger <path>` required; without `--ledger` stop and say so") moves 427's lost-saved-copy failure (`DES:162`) into the coordinator's memory. Adopt A's derivable default path plus `init` refusing an existing ledger (`E-EXISTS`), with `--ledger` as an override. One tension to record, not hide: a derivable path means the fresh sweep reviewer could find the ledger by convention. The sweep prompt must not name the path, and "do not read the ledger" stays PROSE in the rule table; H (hidden-defect share) is how we notice a breach.

**A6. "No concurrency protection while rf-qa is the second adopter" (A-R1 weakness 6; C1).** CONCEDE. I wrote "two parallel QA instances on one ledger lose updates" (variant B section 7) and deferred the lock, which means shipping a known lost-update window in the kernel. Accept `fcntl.flock` per call, `--op` and an expected sequence in the header, idempotent replay of the same op (resolution of C-025 below). I still reject C's hard-link publish, directory sync and filesystem refusal for version 1.

**A7. "The sweep's independence rests on prose" (A-R1 weakness 7).** PARTLY CONCEDE. Freshness is mechanical: a new session, or a subagent, has no memory of the rows the review-3 session verified. Only "does not read L" is PROSE, and the rule table says so with its residual risk. The record that shows a breach is mechanical too: V1-ledger checks whether the sweep report cites ledger row ids.

**A8. "The forecast mixes a starting point the ledger does not share; P3s 5.5 is likely pessimistic" (A-R1 weakness 8).** PARTLY CONCEDE. The ledger changes review 1 (one find pass, anchored JSON rows), so B1 can move. But the counter-forecast was built on the wrong row: A-R2 B7 now verifies that `ARMB-REPORT.md:13` gives the review-1 proxy as 16 and 17 and the review-2 proxy as 5 and 6, and `F2D1:39` says "all 13 blocking". So the only argued direction is mine, with a formula that exposes its input (expected review-3 blockers about B1 x r x r; B1 = 13, ratios 0.46 then 0.17 give 1.0). Merged rule: pre-register the formula, recompute from each replicate's measured review-1 blocking count, and report both P3 and P3s. Neither 2.5 nor 5.5 is a prediction; the formula is.

**A-R2 proposals addressed to B's design.** Accepted: A-R2 on C-017 (hard admission at `answer` and `begin`, scripted recovery), on C-021, C-022, C-025 and X-017 (details below). One caveat on A-R2's C-029: "`close` refuses a report that has its own status table or `verdict:` line". Refusal is right, but the message must name the offending lines and the exact fix, because a panel reviewer's habit under 427 is to end with `verdict:` itself; a silent strip would edit model text and a bare refusal stalls the run.

### From advocate C (Round 1)

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

### Resolution of X-016 and X-017

- **X-016** (blocking FR-8/FR-9 with no field): fixed as in A1. The reviewer supplies `grade`, `rule`, `wrong_outcome`; the script computes `blocking` and freezes it. Test: a row with `rule=FR-8` and `grade=MINOR` is `blocking` and not `deferred`.
- **X-017** (`disputed` as status): fixed as in A3. Five statuses only: `open`, `deferred`, `fixed`, `verified`, `reopened`. A dispute is `claim.action=disputed` on an `open` or `reopened` row, and the verifier's ruling is mandatory.

## Updated assessment

**Variant A.** A is the right frame and the wrong loop. Its frame is what I now adopt: kernel, contract and adapter with a `PROFILES` table; one state object with per-row history; `blocking` computed from the profile; actor inferred from the subcommand; a ledger path derivable from the document; the report-tail check (`E-REPORT-EDITED`); `E-NOT-CHANGED`; the script-written `plan-r<k>.md`; and the V1-ledger compliance check. A-R2 then conceded the loop rules I attacked (fresh sweep session, sweep blockers changing delivery, no early stop at review 2, `open -> verified`, coordinates, unclaimed edits, the wrong forecast row, the `## Unattended mode` copy, the `test_cli_install.py` edit). What is left of A is its architecture, and I rate that higher than in Round 1. A's remaining weaknesses: its extension claim needed narrowing (A-R2 C5 does that), and its "sweep as a fresh subagent" route is a proposal that is UNVERIFIED for S1 and has a heartbeat cost (see New evidence 1).

**Variant C.** After its Round 1 concessions (X-018, X-019, the unsupported 1.5 forecast, the one-row discovery budget), C's value is a set of additive parts, and I take most of them: `loop_decision` versus `delivery_outcome`, `cannot-verify`, anchor relocation with `anchor_state=missing|ambiguous`, old and new ranges with deletion boundaries, packet binding to round, document hash and ledger sequence, `--op` with expected sequence, and the integrity term. I still reject four things: coordinator-only mutation (C-R1 concession 1 admits it cannot run under the one-line brief rule), event replay as the only store (a second reducer every reader must trust; A's per-row `history` gives the same audit trail), the hard-link and directory-sync publication layer (C-R1 concession 7 itself asks for measured cost first), and the script writing the whole report. I also reject C's dependency-passage tracking for verified rows in version 1: in the one replicate where both verify rounds are on file, zero of 19 verified rows regressed (New evidence 2).

**Variant B (myself).** I concede more than in Round 1: `sev` and `--as` go; exit codes move off `close`; the ledger path becomes derivable; locking and operation ids come in; unclaimed edits are refused with a scripted recovery; `disputed` is a flag; P3s gets a union rule. What I keep is what only B supplies: the traced root cause (F22 applied under "apply confirmed findings", then N5, then N12), the B1 x r x r bound and its honest "escalate with 0 to 3 rows" ceiling, the baseline sweeps and hidden-defect share H as the only measure of whether the ledger stopped looking, the install and test traps (`sc-spec-panel-ledger` skipped by `install_skills.py`; `## Unattended mode` set equality), and the end table of rules with residual risk. The merged spec should be A's frame, B's measurement and loop rules for scope, C's outcome vocabulary and integrity rules.

## New evidence

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

## Proposed resolution of split points

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

## Positions table

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
